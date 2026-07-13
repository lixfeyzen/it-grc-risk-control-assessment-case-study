#!/usr/bin/env python3
"""Generate restrained data charts and a recruiter-facing PDF from real public evidence."""

from __future__ import annotations

import csv
import html
import textwrap
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    Image as ReportImage,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
PDF_DIR = ROOT / "output" / "pdf"

NAVY = "#17324D"
BLUE = "#2F6B8A"
TEAL = "#3B7D78"
AMBER = "#B7791F"
RED = "#A44A3F"
GRAY = "#5F6B76"
MID_GRAY = "#A8B0B8"
LIGHT_GRAY = "#E8ECEF"
PALE = "#F5F7F8"
WHITE = "#FFFFFF"


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> float:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def wrap_pixels(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if not current or text_width(draw, candidate, font) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    font: ImageFont.ImageFont,
    fill: str,
    width: int,
    line_height: int,
    max_lines: int | None = None,
) -> int:
    lines = wrap_pixels(draw, text, font, width)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and text_width(draw, last + "...", font) > width:
            last = last[:-1]
        lines[-1] = last.rstrip() + "..."
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def chart_canvas(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (1600, 900), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1600, 14), fill=NAVY)
    draw.text((90, 58), title, font=load_font(42, bold=True), fill=NAVY)
    draw.text((90, 118), subtitle, font=load_font(21), fill=GRAY)
    draw.line((90, 162, 1510, 162), fill=LIGHT_GRAY, width=2)
    return image, draw


def save_chart(image: Image.Image, name: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    image.save(ASSETS / name, format="PNG", optimize=True)


def generate_timeline(rows: list[dict[str, str]]) -> None:
    image, draw = chart_canvas(
        "Public incident timeline",
        "Attributed facts and statements - not a forensic reconstruction",
    )
    date_font = load_font(21, bold=True)
    title_font = load_font(23, bold=True)
    body_font = load_font(17)
    meta_font = load_font(15, bold=True)
    line_x = 315
    start_y = 215
    step = 91
    draw.line((line_x, start_y, line_x, start_y + step * (len(rows) - 1)), fill=MID_GRAY, width=4)
    classification_colors = {
        "Confirmed public fact": TEAL,
        "Issuer statement": BLUE,
        "Issuer statement with explicit caveat": AMBER,
        "Reported third-party claim": RED,
    }
    for index, row in enumerate(rows):
        y = start_y + index * step
        color = classification_colors.get(row["evidence_classification"], GRAY)
        draw.text((90, y - 14), row["event_date"], font=date_font, fill=NAVY)
        draw.ellipse((line_x - 10, y - 10, line_x + 10, y + 10), fill=color, outline=WHITE, width=3)
        draw.text((355, y - 22), row["event_title"], font=title_font, fill=NAVY)
        short = row["publicly_supported_fact"]
        draw_wrapped(draw, short, 355, y + 9, body_font, GRAY, 950, 22, max_lines=2)
        draw.text(
            (1335, y - 14),
            row["source_ids"],
            font=meta_font,
            fill=color,
        )
    draw.text(
        (90, 840),
        "Source: data/incident_timeline.csv | Research cut-off: 13 July 2026",
        font=load_font(15),
        fill=GRAY,
    )
    save_chart(image, "incident_timeline.png")


def claim_group(classification: str) -> str:
    if classification == "Reported third-party claim":
        return "Reported claim"
    if classification == "Not publicly observable":
        return "Not publicly observable"
    return "Confirmed or attributed evidence"


def generate_horizontal_bars(
    title: str,
    subtitle: str,
    labels: list[str],
    values: list[int],
    palette: list[str],
    filename: str,
    footnote: str,
) -> None:
    image, draw = chart_canvas(title, subtitle)
    max_value = max(values) if values else 1
    label_font = load_font(24, bold=True)
    count_font = load_font(25, bold=True)
    detail_font = load_font(17)
    bar_x = 620
    bar_width = 720
    start_y = 260
    gap = 165
    for index, (label, value, color) in enumerate(zip(labels, values, palette)):
        y = start_y + index * gap
        draw.text((100, y + 12), label, font=label_font, fill=NAVY)
        draw.rectangle((bar_x, y, bar_x + bar_width, y + 72), fill=PALE, outline=LIGHT_GRAY, width=2)
        width = int(bar_width * value / max_value)
        draw.rectangle((bar_x, y, bar_x + width, y + 72), fill=color)
        draw.text((bar_x + width + 20, y + 17), str(value), font=count_font, fill=NAVY)
        share = value / sum(values) if sum(values) else 0
        draw.text((100, y + 54), f"{share:.0%} of records", font=detail_font, fill=GRAY)
    draw.text((90, 840), footnote, font=load_font(15), fill=GRAY)
    save_chart(image, filename)


def generate_recommendation_chart(rows: list[dict[str, str]]) -> None:
    counts = Counter((row["priority"], row["time_horizon"]) for row in rows)
    labels = [
        "P1 | 0-30 days",
        "P1 | 31-90 days",
        "P2 | 0-30 days",
        "P2 | 31-90 days",
    ]
    values = [counts[("P1", "0-30 days")], counts[("P1", "31-90 days")], counts[("P2", "0-30 days")], counts[("P2", "31-90 days")]]
    generate_horizontal_bars(
        "Proposed action priority",
        "Analyst recommendations - not BSI commitments",
        labels,
        values,
        [RED, AMBER, MID_GRAY, BLUE],
        "recommendation_priority.png",
        "Source: data/recommendation_register.csv | P1 supports incident closure, recovery assurance, or data-impact decisions",
    )


def register_report_font() -> tuple[str, str]:
    regular = Path("C:/Windows/Fonts/arial.ttf")
    bold = Path("C:/Windows/Fonts/arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("ReportSans", str(regular)))
        pdfmetrics.registerFont(TTFont("ReportSans-Bold", str(bold)))
        return "ReportSans", "ReportSans-Bold"
    return "Helvetica", "Helvetica-Bold"


def report_table(
    rows: list[list[object]],
    widths: list[float],
    body_style: ParagraphStyle,
    header_style: ParagraphStyle,
    font_size: float = 7.2,
    repeat_rows: int = 1,
) -> Table:
    formatted: list[list[object]] = []
    for row_index, row in enumerate(rows):
        style = header_style if row_index == 0 else body_style
        converted: list[object] = []
        for cell in row:
            if isinstance(cell, Paragraph):
                converted.append(cell)
            else:
                converted.append(Paragraph(html.escape(str(cell)), style))
        formatted.append(converted)
    table = Table(formatted, colWidths=widths, repeatRows=repeat_rows, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), header_style.fontName),
                ("FONTSIZE", (0, 0), (-1, -1), font_size),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D0D6")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor(PALE)]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def make_pdf(
    sources: list[dict[str, str]],
    timeline: list[dict[str, str]],
    claims: list[dict[str, str]],
    controls_rows: list[dict[str, str]],
    recommendations: list[dict[str, str]],
) -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    path = PDF_DIR / "Public_Evidence_Banking_Cyber_Incident_GRC_Assessment.pdf"
    regular, bold = register_report_font()
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName=bold,
        fontSize=24,
        leading=29,
        textColor=colors.HexColor(NAVY),
        alignment=TA_LEFT,
        spaceAfter=7,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName=regular,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor(GRAY),
        spaceAfter=10,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName=bold,
        fontSize=15,
        leading=19,
        textColor=colors.HexColor(NAVY),
        spaceBefore=3,
        spaceAfter=7,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName=bold,
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor(NAVY),
        spaceBefore=5,
        spaceAfter=4,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName=regular,
        fontSize=8.6,
        leading=12.2,
        textColor=colors.HexColor("#263442"),
        spaceAfter=5,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=7.1,
        leading=9.2,
        spaceAfter=1,
    )
    header_cell = ParagraphStyle(
        "HeaderCell",
        parent=small,
        fontName=bold,
        textColor=colors.white,
        alignment=TA_LEFT,
    )
    body_cell = ParagraphStyle("BodyCell", parent=small, fontName=regular)
    metric_value = ParagraphStyle(
        "MetricValue",
        parent=body,
        fontName=bold,
        fontSize=18,
        leading=21,
        alignment=TA_CENTER,
        textColor=colors.HexColor(NAVY),
    )
    metric_label = ParagraphStyle(
        "MetricLabel",
        parent=small,
        alignment=TA_CENTER,
        textColor=colors.HexColor(GRAY),
    )

    def footer(canvas, doc) -> None:  # type: ignore[no-untyped-def]
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor(LIGHT_GRAY))
        canvas.line(18 * mm, 15 * mm, 192 * mm, 15 * mm)
        canvas.setFont(regular, 6.8)
        canvas.setFillColor(colors.HexColor(GRAY))
        canvas.drawString(18 * mm, 10 * mm, "Independent portfolio assessment - public evidence only - not a BSI audit")
        canvas.drawRightString(192 * mm, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()

    document = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=17 * mm,
        bottomMargin=20 * mm,
        title="Public-Evidence Banking Cyber Incident and IT GRC Assessment",
        author="Yohanes Wiliam Hadiprojo",
        subject="Independent public-evidence IT GRC portfolio assessment",
    )

    claim_counts = Counter(claim_group(row["classification"]) for row in claims)
    control_counts = Counter(row["observability_status"] for row in controls_rows)
    story: list[object] = []

    # Page 1
    story.append(Paragraph("Public-Evidence Banking Cyber Incident and IT GRC Assessment", title))
    story.append(Paragraph("Bank Syariah Indonesia service disruption - May 2023", subtitle))
    disclaimer = Table(
        [[Paragraph("<b>Scope boundary</b><br/>Independent portfolio work using public sources only. No internal access, no leaked data, no forensic conclusion, and no control-effectiveness opinion.", body)]],
        colWidths=[174 * mm],
    )
    disclaimer.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF3F5")), ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor(BLUE)), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    story.extend([disclaimer, Spacer(1, 8)])
    metric_cells: list[Paragraph] = []
    for value, label in [(len(sources), "public sources"), (len(timeline), "dated events"), (len(claims), "claims classified"), (len(controls_rows), "control domains")]:
        metric_cells.append(Paragraph(f"{value}<br/><font size='7' color='{GRAY}'>{label}</font>", metric_value))
    metrics = Table([metric_cells], colWidths=[43.5 * mm] * 4, rowHeights=[18 * mm])
    metrics.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8D0D6")), ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8D0D6")), ("BACKGROUND", (0, 0), (-1, -1), colors.white), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.extend([metrics, Spacer(1, 9), Paragraph("Executive conclusion", h1)])
    story.append(Paragraph("BSI and OJK public records establish a service disruption, a cyber-incident indication, staged recovery, forensic work, supervisory coordination, and later corrective-action statements. The reviewed sources do not establish a final root cause, initial access vector, verified affected-data population, or internal control-test result.", body))
    findings = [
        "The 8 May disruption and cyber-incident status are supported by BSI's official disclosure and year-end filing.",
        "LockBit's data claim remains a reported third-party claim and is excluded from confirmed-fact metrics.",
        f"Control observability: {control_counts['Observed public action']} observed actions, {control_counts['Partial public evidence']} partial, and {control_counts['Not publicly observable']} not publicly observable.",
        "Priority proposals focus on forensic closure, recovery metrics, scenario testing, and personal-data impact assessment.",
    ]
    for item in findings:
        story.append(Paragraph(f"- {html.escape(item)}", body))
    story.append(Paragraph("Evidence model", h2))
    evidence_model = [
        ["Class", "Treatment"],
        ["Confirmed or authoritative statement", "Use with source attribution and the source's stated boundary."],
        ["Reported third-party claim", "Document the allegation; do not convert it into a verified incident fact."],
        ["Not publicly observable", "Leave unresolved; do not call the control failed or invent a technical answer."],
    ]
    story.append(report_table(evidence_model, [57 * mm, 117 * mm], body_cell, header_cell, font_size=7.5))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Research cut-off: 13 July 2026 | Core source IDs: S-001 to S-009", small))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("1. Public incident chronology", h1))
    story.append(Paragraph("The chart preserves source attribution and does not treat service statements as independent uptime telemetry.", body))
    story.append(ReportImage(str(ASSETS / "incident_timeline.png"), width=174 * mm, height=98 * mm))
    timeline_rows: list[list[object]] = [["Date", "Event", "Classification", "Sources"]]
    for row in timeline:
        timeline_rows.append([row["event_date"], row["event_title"], row["evidence_classification"], row["source_ids"]])
    story.extend([Spacer(1, 5), report_table(timeline_rows, [25 * mm, 75 * mm, 51 * mm, 23 * mm], body_cell, header_cell, font_size=6.8)])
    story.append(Spacer(1, 5))
    story.append(Paragraph("Interpretation: the three-calendar-day interval from 8 to 11 May is not measured downtime. BSI's 11 May normal-service wording and OJK's 13 May progressive-normalization wording are retained as separate observations.", small))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("2. Evidence classification and control observability", h1))
    image_table = Table(
        [[ReportImage(str(ASSETS / "evidence_classification.png"), width=85 * mm, height=48 * mm), ReportImage(str(ASSETS / "control_observability.png"), width=85 * mm, height=48 * mm)]],
        colWidths=[87 * mm, 87 * mm],
    )
    image_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    story.append(image_table)
    story.append(Paragraph("Material unknowns", h2))
    unknown_rows = [["Claim", "Unknown", "Required treatment"]]
    for row in claims:
        if row["classification"] == "Not publicly observable":
            unknown_rows.append([row["claim_id"], row["claim_text"], row["analyst_treatment"]])
    story.append(report_table(unknown_rows, [17 * mm, 83 * mm, 74 * mm], body_cell, header_cell, font_size=6.7))
    story.append(Paragraph("Control-domain summary", h2))
    control_table = [["Domain", "Public status", "Safe conclusion"]]
    for row in controls_rows:
        control_table.append([row["control_domain"], row["observability_status"], row["assessment_conclusion"]])
    story.append(report_table(control_table, [44 * mm, 47 * mm, 83 * mm], body_cell, header_cell, font_size=6.2))
    story.append(PageBreak())

    # Page 4
    story.append(Paragraph("3. Proposed evidence and remediation priorities", h1))
    story.append(Paragraph("These actions are analyst proposals for a similar regulated-bank environment. They are not attributed to BSI and are not BSI commitments.", body))
    story.append(ReportImage(str(ASSETS / "recommendation_priority.png"), width=174 * mm, height=98 * mm))
    rec_table: list[list[object]] = [["ID", "Pri", "Horizon", "Domain", "Recommendation", "Expected evidence"]]
    for row in recommendations:
        rec_table.append([row["recommendation_id"], row["priority"], row["time_horizon"], row["control_domain"], row["recommendation"], row["deliverable"]])
    story.extend([Spacer(1, 5), report_table(rec_table, [13 * mm, 10 * mm, 22 * mm, 27 * mm, 60 * mm, 42 * mm], body_cell, header_cell, font_size=5.8)])
    story.append(Spacer(1, 4))
    story.append(Paragraph("Closure principle: a written policy is not enough. Closure requires implementation evidence, validation results, accountable approval, and explicit acceptance of remaining risk.", small))
    story.append(PageBreak())

    # Page 5
    story.append(Paragraph("4. Source register, method, and limitations", h1))
    source_table: list[list[object]] = [["ID", "Publisher", "Date", "Type", "Locator", "Primary use"]]
    for row in sources:
        linked = Paragraph(f"<link href='{html.escape(row['url'])}' color='{BLUE}'><u>{row['source_id']}</u></link>", body_cell)
        source_table.append([linked, row["publisher"], row["publication_date"], row["source_type"], row["source_locator"], row["primary_use"]])
    story.append(report_table(source_table, [13 * mm, 35 * mm, 23 * mm, 27 * mm, 32 * mm, 44 * mm], body_cell, header_cell, font_size=5.7))
    story.append(Paragraph("Assessment method", h2))
    story.append(Paragraph("Collect public sources -> classify authority and claims -> reconstruct timeline -> map regulatory expectations -> assess public observability -> propose evidence-backed actions -> validate data, SQL, wording, links, charts, and PDF.", body))
    story.append(Paragraph("Limitations", h2))
    limitations = [
        "No internal logs, tickets, policies, contracts, control workpapers, or final forensic report were reviewed.",
        "Issuer and management statements are attributed and are not treated as independent cyber assurance.",
        "No alleged leaked data was accessed, inspected, or redistributed.",
        "Public non-disclosure does not imply control failure; it limits assessment confidence.",
        "Later disclosures may change the evidence set and should be added as new source records.",
    ]
    for item in limitations:
        story.append(Paragraph(f"- {html.escape(item)}", body))
    story.append(Paragraph("Portfolio purpose", h2))
    story.append(Paragraph("Demonstrates source evaluation, incident reconstruction, regulatory mapping, SQL, evidence design, remediation planning, uncertainty management, and executive reporting for an IT Officer or junior IT GRC role.", body))

    document.build(story, onFirstPage=footer, onLaterPages=footer)


def main() -> None:
    legacy = [
        ASSETS / "grc_workflow.png",
        ASSETS / "risk_heatmap.png",
        ASSETS / "control_gap_summary.png",
        ASSETS / "remediation_status_summary.png",
        PDF_DIR / "IT_GRC_Project_Summary.pdf",
    ]
    for path in legacy:
        if path.exists():
            path.unlink()

    sources = read_csv("source_catalog.csv")
    timeline = read_csv("incident_timeline.csv")
    claims = read_csv("evidence_claims.csv")
    controls_rows = read_csv("control_observability.csv")
    recommendations = read_csv("recommendation_register.csv")

    generate_timeline(timeline)
    claim_counts = Counter(claim_group(row["classification"]) for row in claims)
    generate_horizontal_bars(
        "Evidence classification",
        "Claims are separated by evidentiary status",
        ["Confirmed or attributed evidence", "Reported claim", "Not publicly observable"],
        [claim_counts["Confirmed or attributed evidence"], claim_counts["Reported claim"], claim_counts["Not publicly observable"]],
        [TEAL, RED, MID_GRAY],
        "evidence_classification.png",
        "Source: data/evidence_claims.csv | External claims are excluded from confirmed-fact metrics",
    )
    control_counts = Counter(row["observability_status"] for row in controls_rows)
    generate_horizontal_bars(
        "Control observability",
        "Public evidence is not an internal control test",
        ["Observed public action", "Partial public evidence", "Not publicly observable"],
        [control_counts["Observed public action"], control_counts["Partial public evidence"], control_counts["Not publicly observable"]],
        [TEAL, AMBER, MID_GRAY],
        "control_observability.png",
        "Source: data/control_observability.csv | Not publicly observable does not mean failed",
    )
    generate_recommendation_chart(recommendations)
    make_pdf(sources, timeline, claims, controls_rows, recommendations)
    print("artifacts_generated=5")
    print("visual_style=flat_data_report")
    print("pdf_pages_target=5")


if __name__ == "__main__":
    main()
