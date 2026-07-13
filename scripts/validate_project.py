#!/usr/bin/env python3
"""Validate CSV integrity, SQL monitoring queries, and repository safety."""

from __future__ import annotations

import csv
import re
import sqlite3
from datetime import date
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SQL_DIR = ROOT / "sql"

SPECS = {
    "asset_inventory.csv": ("asset_id", 12),
    "risk_register.csv": ("risk_id", 15),
    "control_matrix.csv": ("control_id", 15),
    "control_assessment_results.csv": ("assessment_id", 15),
    "remediation_plan_poam.csv": ("poam_id", 15),
    "evidence_tracker.csv": ("evidence_id", 15),
}


def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA_DIR / name
    if not path.exists():
        raise AssertionError(f"Missing required dataset: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise AssertionError(f"Dataset has no rows: {name}")
    return rows


def split_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def assert_unique(rows: list[dict[str, str]], field: str, expected_count: int, name: str) -> None:
    values = [row[field] for row in rows]
    assert len(rows) == expected_count, f"{name}: expected {expected_count} rows, found {len(rows)}"
    assert all(values), f"{name}: blank {field}"
    assert len(values) == len(set(values)), f"{name}: duplicate {field}"


def validate_relationships(data: dict[str, list[dict[str, str]]]) -> None:
    asset_ids = {row["asset_id"] for row in data["assets"]}
    risk_ids = {row["risk_id"] for row in data["risks"]}
    control_ids = {row["control_id"] for row in data["controls"]}
    assessment_ids = {row["assessment_id"] for row in data["assessments"]}
    poam_ids = {row["poam_id"] for row in data["poam"]}

    for row in data["risks"]:
        assert set(split_ids(row["asset_id"])) <= asset_ids, f"{row['risk_id']}: unknown asset"
        assert row["existing_control_id"] in control_ids, f"{row['risk_id']}: unknown control"
        likelihood = int(row["likelihood_score"])
        impact = int(row["impact_score"])
        inherent = int(row["inherent_risk_score"])
        residual = int(row["residual_risk_score"])
        assert 1 <= likelihood <= 5 and 1 <= impact <= 5, f"{row['risk_id']}: score outside 1-5"
        assert inherent == likelihood * impact, f"{row['risk_id']}: inherent score mismatch"
        assert 1 <= residual <= inherent, f"{row['risk_id']}: invalid residual score"

    for row in data["controls"]:
        assert set(split_ids(row["mapped_asset_id"])) <= asset_ids, f"{row['control_id']}: unknown asset"
        assert set(split_ids(row["mapped_risk_id"])) <= risk_ids, f"{row['control_id']}: unknown risk"

    for row in data["assessments"]:
        assert row["control_id"] in control_ids, f"{row['assessment_id']}: unknown control"

    for row in data["poam"]:
        assert row["related_control_id"] in control_ids, f"{row['poam_id']}: unknown control"
        assert set(split_ids(row["related_risk_id"])) <= risk_ids, f"{row['poam_id']}: unknown risk"
        date.fromisoformat(row["target_date"])

    for row in data["evidence"]:
        assert row["control_id"] in control_ids, f"{row['evidence_id']}: unknown control"
        assert row["assessment_id"] in assessment_ids, f"{row['evidence_id']}: unknown assessment"
        assert row["poam_id"] in poam_ids, f"{row['evidence_id']}: unknown POA&M"
        assert row["evidence_repository_path"] == "Not collected - synthetic case study", (
            f"{row['evidence_id']}: unexpected evidence claim"
        )


def load_sqlite(data: dict[str, list[dict[str, str]]]) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript((SQL_DIR / "01_create_tables.sql").read_text(encoding="utf-8"))
    table_map = [
        ("assets", data["assets"]),
        ("controls", data["controls"]),
        ("risks", data["risks"]),
        ("assessments", data["assessments"]),
        ("poam", data["poam"]),
        ("evidence_tracker", data["evidence"]),
    ]
    for table, rows in table_map:
        columns = list(rows[0].keys())
        sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)})"
        connection.executemany(sql, [[row[column] for column in columns] for row in rows])
    connection.commit()
    connection.executescript((SQL_DIR / "03_grc_monitoring_queries.sql").read_text(encoding="utf-8"))
    return connection


def validate_sql_results(connection: sqlite3.Connection) -> None:
    assert connection.execute("SELECT COUNT(*) FROM v_risk_control_overview").fetchone()[0] == 15
    assert connection.execute("SELECT COUNT(*) FROM v_assessment_poam_evidence").fetchone()[0] == 15
    summary = dict(connection.execute("SELECT metric, value FROM v_management_summary").fetchall())
    expected = {
        "assets_in_scope": 12,
        "risks_assessed": 15,
        "high_priority_risks": 8,
        "controls_assessed": 15,
        "high_severity_findings": 7,
        "evidence_unavailable": 6,
        "poam_open": 5,
        "poam_in_progress": 4,
    }
    assert summary == expected, f"Management summary mismatch: {summary}"


def validate_repository_safety() -> None:
    patterns = [
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        re.compile(r"(?i)\b(?:password|access_token|api_key)\s*=\s*[^\s<>{}\[\]]{8,}"),
    ]
    excluded = {"validate_project.py"}
    text_suffixes = {".md", ".csv", ".sql", ".py", ".txt", ".json", ".yml", ".yaml"}
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in text_suffixes or path.name in excluded:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(pattern.search(text) for pattern in patterns):
            findings.append(str(path.relative_to(ROOT)))
    assert not findings, f"Potential secrets found in: {findings}"


def validate_repository_artifacts() -> None:
    required = [
        ROOT / "assets" / "grc_workflow.png",
        ROOT / "assets" / "risk_heatmap.png",
        ROOT / "assets" / "control_gap_summary.png",
        ROOT / "assets" / "remediation_status_summary.png",
        ROOT / "output" / "pdf" / "IT_GRC_Project_Summary.pdf",
    ]
    for path in required:
        assert path.exists() and path.stat().st_size > 0, f"Missing artifact: {path.relative_to(ROOT)}"
        signature = path.read_bytes()[:8]
        if path.suffix.lower() == ".png":
            assert signature == b"\x89PNG\r\n\x1a\n", f"Invalid PNG: {path.relative_to(ROOT)}"
        elif path.suffix.lower() == ".pdf":
            assert signature.startswith(b"%PDF-"), f"Invalid PDF: {path.relative_to(ROOT)}"


def validate_markdown_links() -> None:
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    broken: list[str] = []
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            linked_path = (path.parent / unquote(target)).resolve()
            if not linked_path.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    assert not broken, f"Broken local Markdown links: {broken}"


def main() -> None:
    loaded = {name: read_csv(name) for name in SPECS}
    for name, (id_field, expected_count) in SPECS.items():
        assert_unique(loaded[name], id_field, expected_count, name)
    data = {
        "assets": loaded["asset_inventory.csv"],
        "risks": loaded["risk_register.csv"],
        "controls": loaded["control_matrix.csv"],
        "assessments": loaded["control_assessment_results.csv"],
        "poam": loaded["remediation_plan_poam.csv"],
        "evidence": loaded["evidence_tracker.csv"],
    }
    validate_relationships(data)
    connection = load_sqlite(data)
    validate_sql_results(connection)
    validate_repository_safety()
    validate_repository_artifacts()
    validate_markdown_links()
    print("validation=passed")
    print("csv_rows=87")
    print("relationship_checks=passed")
    print("risk_score_checks=passed")
    print("sql_schema_and_queries=passed")
    print("secret_scan=passed")
    print("artifact_integrity=passed")
    print("markdown_links=passed")


if __name__ == "__main__":
    main()
