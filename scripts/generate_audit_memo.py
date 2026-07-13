#!/usr/bin/env python3
"""Generate a plain, source-traceable audit memorandum without infographics."""

from __future__ import annotations

import csv
import html
from collections import Counter
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PDF_DIR = ROOT / "output" / "pdf"
PDF_PATH = PDF_DIR / "BSI_Public_Evidence_GRC_Assessment_Memo.pdf"

BLACK = colors.HexColor("#111111")
DARK_GRAY = colors.HexColor("#404040")
MID_GRAY = colors.HexColor("#808080")
LIGHT_GRAY = colors.HexColor("#D9D9D9")
PALE_GRAY = colors.HexColor("#E7E6E6")
WHITE = colors.white


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def clean_text(value: object) -> str:
    return (
        str(value)
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )


def register_fonts() -> tuple[str, str]:
    regular = Path("C:/Windows/Fonts/arial.ttf")
    bold = Path("C:/Windows/Fonts/arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("MemoSans", str(regular)))
        pdfmetrics.registerFont(TTFont("MemoSans-Bold", str(bold)))
        return "MemoSans", "MemoSans-Bold"
    return "Helvetica", "Helvetica-Bold"


def make_styles(regular: str, bold: str) -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "MemoTitle",
            parent=base["Heading1"],
            fontName=bold,
            fontSize=14,
            leading=17,
            textColor=BLACK,
            spaceAfter=7,
        ),
        "h1": ParagraphStyle(
            "MemoH1",
            parent=base["Heading2"],
            fontName=bold,
            fontSize=10.5,
            leading=13,
            textColor=BLACK,
            spaceBefore=5,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "MemoBody",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=8.6,
            leading=12,
            textColor=BLACK,
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "MemoSmall",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=7.2,
            leading=9.2,
            textColor=DARK_GRAY,
            spaceAfter=3,
        ),
        "cell": ParagraphStyle(
            "MemoCell",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=6.2,
            leading=7.5,
            textColor=BLACK,
        ),
        "header_cell": ParagraphStyle(
            "MemoHeaderCell",
            parent=base["BodyText"],
            fontName=bold,
            fontSize=6.2,
            leading=7.5,
            textColor=WHITE,
        ),
        "meta_label": ParagraphStyle(
            "MemoMetaLabel",
            parent=base["BodyText"],
            fontName=bold,
            fontSize=7.4,
            leading=9.2,
            textColor=BLACK,
        ),
        "meta_value": ParagraphStyle(
            "MemoMetaValue",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=7.4,
            leading=9.2,
            textColor=BLACK,
        ),
    }


def paragraph(value: object, style: ParagraphStyle) -> Paragraph:
    return Paragraph(html.escape(clean_text(value)), style)


def linked_source(source_id: str, url: str, style: ParagraphStyle) -> Paragraph:
    safe_id = html.escape(clean_text(source_id))
    safe_url = html.escape(url, quote=True)
    return Paragraph(f"<link href='{safe_url}'><u>{safe_id}</u></link>", style)


def memo_table(
    rows: list[list[object]],
    widths: list[float],
    styles: dict[str, ParagraphStyle],
    font_size: float = 6.2,
) -> Table:
    body_style = ParagraphStyle(
        f"MemoCell{font_size}",
        parent=styles["cell"],
        fontSize=font_size,
        leading=font_size + 1.3,
    )
    header_style = ParagraphStyle(
        f"MemoHeaderCell{font_size}",
        parent=styles["header_cell"],
        fontSize=font_size,
        leading=font_size + 1.3,
    )
    formatted: list[list[object]] = []
    for row_index, row in enumerate(rows):
        row_style = header_style if row_index == 0 else body_style
        formatted.append(
            [cell if isinstance(cell, Paragraph) else paragraph(cell, row_style) for cell in row]
        )
    table = Table(formatted, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), DARK_GRAY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LINEBELOW", (0, 0), (-1, 0), 0.75, BLACK),
                ("LINEBELOW", (0, 1), (-1, -2), 0.25, LIGHT_GRAY),
                ("LINEBELOW", (0, -1), (-1, -1), 0.5, MID_GRAY),
            ]
        )
    )
    return table


def page_frame(canvas, document) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(DARK_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, height - 16 * mm, width - 18 * mm, height - 16 * mm)
    canvas.setFont("Helvetica-Bold", 7)
    canvas.setFillColor(DARK_GRAY)
    canvas.drawString(18 * mm, height - 12.5 * mm, "PUBLIC-EVIDENCE INCIDENT ASSESSMENT MEMORANDUM")
    canvas.setFont("Helvetica", 6.5)
    canvas.drawRightString(width - 18 * mm, height - 12.5 * mm, "PT BANK SYARIAH INDONESIA TBK | MAY 2023")
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.drawString(18 * mm, 10 * mm, "Portfolio workpaper | Public sources only | Not an internal audit")
    canvas.drawRightString(width - 18 * mm, 10 * mm, f"Page {document.page}")
    canvas.restoreState()


def bullet(text: str, styles: dict[str, ParagraphStyle]) -> Paragraph:
    return Paragraph(f"- {html.escape(clean_text(text))}", styles["body"])


def build_pdf() -> None:
    sources = read_csv("source_catalog.csv")
    timeline = read_csv("incident_timeline.csv")
    claims = read_csv("evidence_claims.csv")
    controls = read_csv("control_observability.csv")
    recommendations = read_csv("recommendation_register.csv")

    regular, bold = register_fonts()
    styles = make_styles(regular, bold)
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    old_pdf = PDF_DIR / "Public_Evidence_Banking_Cyber_Incident_GRC_Assessment.pdf"
    if old_pdf.exists():
        old_pdf.unlink()

    document = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=19 * mm,
        title="BSI Public-Evidence IT GRC Assessment Memorandum",
        author="Independent portfolio case study",
        subject="Public-evidence cyber incident and control observability assessment",
    )

    story: list[object] = []

    # Page 1 - memorandum summary
    story.append(paragraph("Assessment memorandum", styles["title"]))
    metadata = [
        ["Subject", "Bank Syariah Indonesia - May 2023 service disruption and cyber incident"],
        ["Assessment", "Independent public-evidence IT GRC case study"],
        ["Research cut-off", "13 July 2026"],
        ["Purpose", "Portfolio review and interview discussion"],
        ["Boundary", "Public observability only; no internal control-effectiveness opinion"],
    ]
    meta_rows = [
        [paragraph(label, styles["meta_label"]), paragraph(value, styles["meta_value"])]
        for label, value in metadata
    ]
    meta_table = Table(meta_rows, colWidths=[30 * mm, 144 * mm], hAlign="LEFT")
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), PALE_GRAY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LINEBELOW", (0, 0), (-1, -2), 0.25, LIGHT_GRAY),
                ("LINEBELOW", (0, -1), (-1, -1), 0.5, MID_GRAY),
            ]
        )
    )
    story.extend([meta_table, Spacer(1, 6)])

    story.append(paragraph("Question assessed", styles["h1"]))
    story.append(
        paragraph(
            "What do public BSI, OJK, audited-filing, legal, regulatory, technical, and reputable media sources establish about the incident, and what control areas merit follow-up without pretending to have internal audit access?",
            styles["body"],
        )
    )
    story.append(paragraph("Executive conclusion", styles["h1"]))
    story.append(
        paragraph(
            "The disruption, staged service recovery, cyber-incident indication, forensic work, regulatory coordination, and later corrective-action statement are supported by attributed public evidence. The reviewed source set does not establish a final forensic root cause, initial-access vector, verified affected-record inventory, or internal control test result. Those facts must remain unresolved unless additional evidence is obtained.",
            styles["body"],
        )
    )

    claim_counts = Counter(
        "reported" if row["classification"] == "Reported third-party claim" else
        "unknown" if row["classification"] == "Not publicly observable" else
        "supported"
        for row in claims
    )
    control_counts = Counter(row["observability_status"] for row in controls)
    summary_rows = [
        ["CONTROL TOTAL", "RESULT", "INTERPRETATION"],
        ["Public sources", len(sources), "Eight primary sources and one secondary source used for attributed claim context"],
        ["Incident events", len(timeline), "Chronology reconstructed from issuer, regulator, filing, and Reuters reporting"],
        ["Evidence claims", len(claims), f"{claim_counts['supported']} supported or attributed; {claim_counts['reported']} reported claim; {claim_counts['unknown']} not publicly observable"],
        ["Control domains", len(controls), f"{control_counts['Observed public action']} observed action; {control_counts['Partial public evidence']} partial evidence; {control_counts['Not publicly observable']} not publicly observable"],
        ["Recommendations", len(recommendations), "Analyst proposals for a comparable regulated-bank environment; not BSI commitments"],
    ]
    story.append(memo_table(summary_rows, [43 * mm, 19 * mm, 112 * mm], styles, font_size=7.0))
    story.append(Spacer(1, 6))
    story.append(paragraph("Assessment boundary", styles["h1"]))
    story.append(bullet("No BSI systems were accessed, scanned, or tested.", styles))
    story.append(bullet("No internal logs, tickets, policies, contracts, control workpapers, or final forensic report were reviewed.", styles))
    story.append(bullet("A missing public disclosure is an evidence limitation, not proof of a failed control.", styles))
    story.append(bullet("No alleged leaked data was accessed, inspected, or redistributed.", styles))
    story.append(PageBreak())

    # Page 2 - chronology
    story.append(paragraph("1. Public incident chronology", styles["title"]))
    story.append(paragraph("The chronology preserves source attribution and does not convert public statements into independently measured uptime or forensic conclusions.", styles["small"]))
    timeline_rows: list[list[object]] = [["Date", "Event", "Publicly supported fact", "Classification", "Source"]]
    for row in timeline:
        timeline_rows.append([
            row["event_date"],
            row["event_title"],
            row["publicly_supported_fact"],
            row["evidence_classification"],
            row["source_ids"],
        ])
    story.append(memo_table(timeline_rows, [20 * mm, 40 * mm, 68 * mm, 31 * mm, 15 * mm], styles, font_size=6.5))
    story.append(Spacer(1, 6))
    story.append(paragraph("Reviewer note", styles["h1"]))
    story.append(paragraph("The interval between 8 and 11 May is not treated as measured downtime. BSI's 11 May normal-service wording and OJK's 13 May progressive-normalization wording are retained as separate observations from different dates and viewpoints.", styles["body"]))
    story.append(PageBreak())

    # Page 3 - claims
    story.append(paragraph("2. Evidence claim register", styles["title"]))
    story.append(paragraph("Reported claims and non-observable facts are kept outside confirmed-fact counts. Analyst treatment states the safe use of each claim.", styles["small"]))
    claim_rows: list[list[object]] = [["ID", "Category", "Claim", "Classification", "Confidence", "Analyst treatment"]]
    for row in claims:
        claim_rows.append([
            row["claim_id"],
            row["claim_category"],
            row["claim_text"],
            row["classification"],
            row["confidence"],
            row["analyst_treatment"],
        ])
    story.append(memo_table(claim_rows, [12 * mm, 23 * mm, 61 * mm, 30 * mm, 17 * mm, 31 * mm], styles, font_size=5.9))
    story.append(PageBreak())

    # Page 4 - controls
    story.append(paragraph("3. Control observability working paper", styles["title"]))
    story.append(paragraph("This working paper compares public evidence with regulatory or technical expectations. It does not test design or operating effectiveness.", styles["small"]))
    control_rows: list[list[object]] = [["ID", "Domain", "Reference expectation", "Public evidence", "Status", "Conclusion"]]
    for row in controls:
        control_rows.append([
            row["control_id"],
            row["control_domain"],
            row["reference_expectation"],
            row["public_evidence"],
            row["observability_status"],
            row["assessment_conclusion"],
        ])
    story.append(memo_table(control_rows, [12 * mm, 24 * mm, 39 * mm, 49 * mm, 25 * mm, 25 * mm], styles, font_size=5.7))
    story.append(PageBreak())

    # Page 5 - recommendations
    story.append(paragraph("4. Recommendation register", styles["title"]))
    story.append(paragraph("All actions below are analyst proposals for a comparable regulated-bank environment. They are not attributed to BSI and are not BSI commitments.", styles["small"]))
    recommendation_rows: list[list[object]] = [["ID", "Pri", "Horizon", "Domain", "Recommendation", "Expected evidence", "Suggested owner"]]
    for row in recommendations:
        recommendation_rows.append([
            row["recommendation_id"],
            row["priority"],
            row["time_horizon"],
            row["control_domain"],
            row["recommendation"],
            row["deliverable"],
            row["ownership_model"],
        ])
    story.append(memo_table(recommendation_rows, [12 * mm, 9 * mm, 18 * mm, 22 * mm, 52 * mm, 35 * mm, 26 * mm], styles, font_size=5.7))
    story.append(Spacer(1, 6))
    story.append(paragraph("Closure principle", styles["h1"]))
    story.append(paragraph("A written policy alone is not closure. Closure requires implementation evidence, validation results, accountable approval, and explicit acceptance of remaining risk.", styles["body"]))
    story.append(PageBreak())

    # Page 6 - source register and limitations
    story.append(paragraph("5. Source register and limitations", styles["title"]))
    source_rows: list[list[object]] = [["ID", "Publisher", "Date", "Type", "Locator", "Primary use"]]
    for row in sources:
        source_rows.append([
            linked_source(row["source_id"], row["url"], styles["cell"]),
            row["publisher"],
            row["publication_date"],
            row["source_type"],
            row["source_locator"],
            row["primary_use"],
        ])
    story.append(memo_table(source_rows, [12 * mm, 31 * mm, 18 * mm, 24 * mm, 34 * mm, 55 * mm], styles, font_size=5.7))
    story.append(Spacer(1, 5))
    story.append(paragraph("Method", styles["h1"]))
    story.append(paragraph("Register sources -> classify claim authority -> reconstruct events -> preserve conflicting wording -> map control expectations -> assess public observability -> propose required evidence and accountable follow-up.", styles["body"]))
    story.append(paragraph("Limitations", styles["h1"]))
    story.append(bullet("Issuer and management statements are attributed and are not independent cyber assurance.", styles))
    story.append(bullet("Service-recovery statements are not independent availability measurements.", styles))
    story.append(bullet("The source set does not include a published final forensic report or verified affected-record inventory.", styles))
    story.append(bullet("Later disclosures may change the evidence set and should be added as new source records.", styles))

    document.build(story, onFirstPage=page_frame, onLaterPages=page_frame)


def main() -> None:
    build_pdf()
    print(f"pdf={PDF_PATH}")
    print("presentation=audit_memorandum")
    print("charts=0")


if __name__ == "__main__":
    main()
