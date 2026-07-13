#!/usr/bin/env python3
"""Validate real-source traceability, claim guardrails, SQL outputs, and artifacts."""

from __future__ import annotations

import csv
import re
import sqlite3
import zipfile
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SQL = ROOT / "sql"

SPECS = {
    "source_catalog.csv": ("source_id", 9),
    "incident_timeline.csv": ("event_id", 7),
    "evidence_claims.csv": ("claim_id", 12),
    "control_observability.csv": ("control_id", 10),
    "recommendation_register.csv": ("recommendation_id", 8),
}


def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA / name
    assert path.exists(), f"Missing required dataset: {path.relative_to(ROOT)}"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows, f"Empty dataset: {name}"
    return rows


def split_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def validate_shape(loaded: dict[str, list[dict[str, str]]]) -> None:
    for name, (id_field, expected_count) in SPECS.items():
        rows = loaded[name]
        values = [row[id_field] for row in rows]
        assert len(rows) == expected_count, f"{name}: expected {expected_count}, found {len(rows)}"
        assert all(values), f"{name}: blank {id_field}"
        assert len(values) == len(set(values)), f"{name}: duplicate {id_field}"
        assert all(all(value.strip() for value in row.values()) for row in rows), f"{name}: blank cell"


def validate_sources(data: dict[str, list[dict[str, str]]]) -> None:
    sources = data["sources"]
    source_ids = {row["source_id"] for row in sources}
    allowed_domains = {
        "ir.bankbsi.co.id",
        "www.ojk.go.id",
        "ojk.go.id",
        "www.marketscreener.com",
        "peraturan.bpk.go.id",
        "csrc.nist.gov",
    }
    assert sum(row["authority_level"] == "Primary" for row in sources) == 8
    assert sum(row["authority_level"] == "Secondary" for row in sources) == 1
    for row in sources:
        date.fromisoformat(row["publication_date"])
        date.fromisoformat(row["accessed_date"])
        parsed = urlparse(row["url"])
        assert parsed.scheme == "https" and parsed.netloc in allowed_domains, f"Unapproved source URL: {row['url']}"

    reference_fields = [
        (data["timeline"], "event_id", "source_ids"),
        (data["claims"], "claim_id", "source_ids"),
        (data["controls"], "control_id", "source_ids"),
        (data["controls"], "control_id", "reference_ids"),
        (data["recommendations"], "recommendation_id", "reference_ids"),
    ]
    for rows, key, field in reference_fields:
        for row in rows:
            refs = split_ids(row[field])
            assert refs, f"{row[key]}: blank {field}"
            unknown = set(refs) - source_ids
            assert not unknown, f"{row[key]}: unknown source IDs {unknown}"


def validate_claim_guardrails(data: dict[str, list[dict[str, str]]]) -> None:
    timeline = data["timeline"]
    claims = data["claims"]
    controls = data["controls"]
    recommendations = data["recommendations"]

    timeline_dates = [(row["event_date"], int(row["event_order"])) for row in timeline]
    assert timeline_dates == sorted(timeline_dates), "Timeline is not chronologically ordered"
    assert next(row for row in timeline if row["event_id"] == "E-007")["evidence_classification"] == "Reported third-party claim"

    reported = [row for row in claims if row["classification"] == "Reported third-party claim"]
    unknowns = [row for row in claims if row["classification"] == "Not publicly observable"]
    assert len(reported) == 1 and reported[0]["claim_id"] == "C-009"
    assert split_ids(reported[0]["source_ids"]) == ["S-004"]
    assert len(unknowns) == 3
    assert all(row["confidence"] == "Not assessable" for row in unknowns)

    claim_groups = {
        "Confirmed or attributed public evidence": sum(
            row["classification"] not in {"Reported third-party claim", "Not publicly observable"}
            for row in claims
        ),
        "Reported claim": len(reported),
        "Not publicly observable": len(unknowns),
    }
    assert claim_groups == {
        "Confirmed or attributed public evidence": 8,
        "Reported claim": 1,
        "Not publicly observable": 3,
    }

    control_summary = {
        status: sum(row["observability_status"] == status for row in controls)
        for status in {row["observability_status"] for row in controls}
    }
    assert control_summary == {
        "Observed public action": 2,
        "Partial public evidence": 3,
        "Not publicly observable": 5,
    }
    assert all("failed" not in row["observability_status"].lower() for row in controls)
    assert all(row["status"] == "Analyst proposal - not a BSI commitment" for row in recommendations)
    assert sum(row["priority"] == "P1" for row in recommendations) == 5
    assert sum(row["priority"] == "P2" for row in recommendations) == 3

    prohibited = [
        re.compile(r"lockbit definitely", re.IGNORECASE),
        re.compile(r"attack entered through", re.IGNORECASE),
        re.compile(r"controls? (?:definitely )?failed", re.IGNORECASE),
        re.compile(r"forensic audit proved", re.IGNORECASE),
    ]
    for name in ["incident_timeline.csv", "evidence_claims.csv", "control_observability.csv", "recommendation_register.csv"]:
        text = (DATA / name).read_text(encoding="utf-8")
        assert not any(pattern.search(text) for pattern in prohibited), f"Unsupported assertion in {name}"


def load_sqlite(data: dict[str, list[dict[str, str]]]) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.executescript((SQL / "01_create_tables.sql").read_text(encoding="utf-8"))
    table_map = [
        ("source_catalog", data["sources"]),
        ("incident_timeline", data["timeline"]),
        ("evidence_claims", data["claims"]),
        ("control_observability", data["controls"]),
        ("recommendation_register", data["recommendations"]),
    ]
    for table, rows in table_map:
        columns = list(rows[0].keys())
        placeholders = ",".join("?" for _ in columns)
        insert = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
        connection.executemany(insert, [[row[column] for column in columns] for row in rows])
    connection.commit()
    connection.executescript((SQL / "02_analysis_queries.sql").read_text(encoding="utf-8"))
    return connection


def validate_sql(connection: sqlite3.Connection) -> None:
    claim_summary = dict(connection.execute("SELECT claim_group, claim_count FROM v_claim_classification_summary"))
    assert claim_summary == {
        "Confirmed or attributed public evidence": 8,
        "Reported claim": 1,
        "Not publicly observable": 3,
    }
    control_summary = dict(connection.execute("SELECT observability_status, control_count FROM v_control_observability_summary"))
    assert control_summary == {
        "Observed public action": 2,
        "Partial public evidence": 3,
        "Not publicly observable": 5,
    }
    rec_count = connection.execute("SELECT SUM(recommendation_count) FROM v_recommendation_priority_summary").fetchone()[0]
    assert rec_count == 8
    source_usage = connection.execute("SELECT COUNT(*) FROM v_source_usage WHERE timeline_rows + claim_rows + control_rows + recommendation_rows > 0").fetchone()[0]
    assert source_usage == 9


def validate_workbook() -> None:
    workbook = ROOT / "output" / "workbook" / "BSI_Public_Evidence_GRC_Workpaper.xlsx"
    assert workbook.exists() and workbook.stat().st_size > 15_000, "Missing or small Excel workpaper"
    assert zipfile.is_zipfile(workbook), "Excel workpaper is not a valid XLSX package"

    with zipfile.ZipFile(workbook) as archive:
        names = set(archive.namelist())
        assert "xl/workbook.xml" in names, "XLSX workbook metadata is missing"
        assert "xl/worksheets/sheet1.xml" in names, "XLSX worksheets are missing"
        workbook_xml = ElementTree.fromstring(archive.read("xl/workbook.xml"))
        namespace = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        sheet_names = [element.attrib["name"] for element in workbook_xml.findall(".//x:sheet", namespace)]
        assert sheet_names == [
            "Source_Catalog",
            "Incident_Timeline",
            "Evidence_Claims",
            "Control_Observability",
            "Recommendations",
            "Cover",
        ], f"Unexpected workbook sheets: {sheet_names}"

        xml_text = "\n".join(
            archive.read(name).decode("utf-8", errors="ignore")
            for name in names
            if name.endswith(".xml")
        )
        required_text = [
            "PUBLIC-EVIDENCE INCIDENT ASSESSMENT WORKPAPER",
            "COUNTA(Source_Catalog!A2:A10)",
            "Not publicly observable",
            "Analyst proposal - not a BSI commitment",
        ]
        for phrase in required_text:
            assert phrase in xml_text, f"Workbook missing expected content: {phrase}"
        assert not re.search(r"#(?:REF!|DIV/0!|VALUE!|NAME\?|N/A)", xml_text), "Workbook contains a formula error"


def validate_pdf() -> None:
    pdf = ROOT / "output" / "pdf" / "BSI_Public_Evidence_GRC_Assessment_Memo.pdf"
    assert pdf.exists() and pdf.stat().st_size > 50_000, "Missing or small PDF memorandum"
    reader = PdfReader(str(pdf))
    assert len(reader.pages) == 6, f"Expected 6 PDF pages, found {len(reader.pages)}"
    page_text = [(page.extract_text() or "") for page in reader.pages]
    expected = [
        "Assessment memorandum",
        "Public incident chronology",
        "Evidence claim register",
        "Control observability working paper",
        "Recommendation register",
        "Source register and limitations",
    ]
    for index, phrase in enumerate(expected):
        assert phrase in page_text[index], f"Page {index + 1} missing title: {phrase}"
        assert len(page_text[index].strip()) > 250, f"Page {index + 1} has too little extractable text"


def validate_no_infographics() -> None:
    assets = ROOT / "assets"
    assert not list(assets.glob("*.png")), "PNG infographic remains in assets/"
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "![" not in readme, "README still embeds an image"
    assert ".png" not in readme.lower(), "README still references a PNG"

    legacy = [
        assets / "incident_timeline.png",
        assets / "evidence_classification.png",
        assets / "control_observability.png",
        assets / "recommendation_priority.png",
        ROOT / "output" / "pdf" / "Public_Evidence_Banking_Cyber_Incident_GRC_Assessment.pdf",
        ROOT / "scripts" / "generate_artifacts.py",
    ]
    assert not any(path.exists() for path in legacy), "Legacy infographic artifact remains"


def validate_markdown_links() -> None:
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    broken: list[str] = []
    for path in ROOT.rglob("*.md"):
        for target in pattern.findall(path.read_text(encoding="utf-8")):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("https://", "http://", "mailto:")):
                continue
            linked = (path.parent / unquote(target)).resolve()
            if not linked.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    assert not broken, f"Broken local Markdown links: {broken}"


def validate_repository_safety() -> None:
    patterns = [
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        re.compile(r"(?i)\b(?:password|access_token|api_key)\s*=\s*[^\s<>{}\[\]]{8,}"),
    ]
    suffixes = {".md", ".csv", ".sql", ".py", ".txt", ".json", ".yml", ".yaml"}
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes or path.name == "validate_project.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(pattern.search(text) for pattern in patterns):
            findings.append(str(path.relative_to(ROOT)))
    assert not findings, f"Potential secrets found: {findings}"


def main() -> None:
    loaded = {name: read_csv(name) for name in SPECS}
    validate_shape(loaded)
    data = {
        "sources": loaded["source_catalog.csv"],
        "timeline": loaded["incident_timeline.csv"],
        "claims": loaded["evidence_claims.csv"],
        "controls": loaded["control_observability.csv"],
        "recommendations": loaded["recommendation_register.csv"],
    }
    validate_sources(data)
    validate_claim_guardrails(data)
    connection = load_sqlite(data)
    validate_sql(connection)
    validate_workbook()
    validate_pdf()
    validate_no_infographics()
    validate_markdown_links()
    validate_repository_safety()

    print("validation=passed")
    print("sources=9")
    print("timeline_events=7")
    print("evidence_claims=12")
    print("control_domains=10")
    print("recommendations=8")
    print("source_traceability=passed")
    print("claim_guardrails=passed")
    print("sql_queries=passed")
    print("workbook_integrity=passed")
    print("pdf_integrity=passed")
    print("no_infographics=passed")
    print("markdown_links=passed")
    print("secret_scan=passed")


if __name__ == "__main__":
    main()
