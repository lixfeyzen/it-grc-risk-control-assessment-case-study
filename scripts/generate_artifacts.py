#!/usr/bin/env python3
"""Generate the evidence tracker, portfolio visuals, and executive PDF.

All outputs are derived from the synthetic CSV datasets in ``data/``. The
script does not claim that real control evidence was collected or reviewed.
"""

from __future__ import annotations

import csv
import html
from collections import Counter
from pathlib import Path

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
PDF_DIR = ROOT / "output" / "pdf"

NAVY = "#17324D"
BLUE = "#2563A6"
LIGHT_BLUE = "#E8F1FA"
RED = "#C2413B"
AMBER = "#D97706"
GREEN = "#2F855A"
GRAY = "#5D6975"
LIGHT_GRAY = "#EEF2F5"
WHITE = "#FFFFFF"
BLACK = "#17202A"


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA_DIR / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_project_data() -> dict[str, list[dict[str, str]]]:
    return {
        "assets": read_csv("asset_inventory.csv"),
        "risks": read_csv("risk_register.csv"),
        "controls": read_csv("control_matrix.csv"),
        "assessments": read_csv("control_assessment_results.csv"),
        "poam": read_csv("remediation_plan_poam.csv"),
    }


def evidence_review_outcome(status: str) -> str:
    return {
        "Partial": "Review incomplete - evidence set is partial",
        "Not Available": "Not reviewable - evidence is unavailable",
        "Available": "Reviewable - evidence is available",
    }.get(status, "Not assessed")


def generate_evidence_tracker(data: dict[str, list[dict[str, str]]]) -> Path:
    assessments = {row["control_id"]: row for row in data["assessments"]}
    poam = {row["related_control_id"]: row for row in data["poam"]}
    fields = [
        "evidence_id",
        "control_id",
        "assessment_id",
        "poam_id",
        "control_area",
        "evidence_required",
        "evidence_owner",
        "collection_frequency",
        "evidence_status",
        "review_outcome",
        "evidence_repository_path",
        "reviewer_role",
        "gap_or_issue",
        "action_required",
        "evidence_due_date",
        "confidentiality_classification",
        "retention_guidance",
        "notes",
    ]

    rows: list[dict[str, str]] = []
    for index, control in enumerate(data["controls"], start=1):
        assessment = assessments[control["control_id"]]
        remediation = poam[control["control_id"]]
        rows.append(
            {
                "evidence_id": f"E-{index:03d}",
                "control_id": control["control_id"],
                "assessment_id": assessment["assessment_id"],
                "poam_id": remediation["poam_id"],
                "control_area": control["control_area"],
                "evidence_required": control["evidence_required"],
                "evidence_owner": control["control_owner"],
                "collection_frequency": control["frequency"],
                "evidence_status": assessment["evidence_status"],
                "review_outcome": evidence_review_outcome(assessment["evidence_status"]),
                "evidence_repository_path": "Not collected - synthetic case study",
                "reviewer_role": "IT GRC Analyst (simulated)",
                "gap_or_issue": assessment["finding"],
                "action_required": remediation["remediation_action"],
                "evidence_due_date": remediation["target_date"],
                "confidentiality_classification": "Internal - Synthetic",
                "retention_guidance": "Organization-specific; not assessed in this simulation",
                "notes": (
                    "Tracker row derived from simulated assessment data. No real evidence "
                    "file, review, audit, or certification result is claimed."
                ),
            }
        )

    output = DATA_DIR / "evidence_tracker.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return output


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def canvas(title: str, subtitle: str = "") -> tuple[PILImage.Image, ImageDraw.ImageDraw]:
    image = PILImage.new("RGB", (1600, 900), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1600, 112), fill=NAVY)
    draw.text((70, 30), title, fill=WHITE, font=load_font(38, bold=True))
    if subtitle:
        draw.text((72, 78), subtitle, fill="#D7E5F2", font=load_font(18))
    return image, draw


def save_image(image: PILImage.Image, name: str) -> Path:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    output = ASSETS_DIR / name
    image.save(output, format="PNG", optimize=True)
    return output


def draw_workflow() -> Path:
    image, draw = canvas(
        "IT GRC Assessment Workflow",
        "Synthetic portfolio case study - evidence-based traceability from assets to management reporting",
    )
    steps = [
        ("1", "Asset\nInventory"),
        ("2", "Risk\nRegister"),
        ("3", "Control\nMatrix"),
        ("4", "Control\nAssessment"),
        ("5", "POA&M"),
        ("6", "Evidence &\nReporting"),
    ]
    box_w, box_h, gap = 205, 180, 36
    start_x, y = 70, 300
    for index, (number, label) in enumerate(steps):
        x = start_x + index * (box_w + gap)
        draw.rounded_rectangle((x, y, x + box_w, y + box_h), radius=22, fill=LIGHT_BLUE, outline=BLUE, width=4)
        draw.ellipse((x + 18, y + 18, x + 70, y + 70), fill=BLUE)
        draw.text((x + 36, y + 27), number, anchor="mm", fill=WHITE, font=load_font(24, bold=True))
        for line_index, line in enumerate(label.split("\n")):
            draw.text((x + box_w / 2, y + 100 + line_index * 38), line, anchor="mm", fill=NAVY, font=load_font(26, bold=True))
        if index < len(steps) - 1:
            arrow_x = x + box_w + 7
            draw.line((arrow_x, y + box_h / 2, arrow_x + gap - 14, y + box_h / 2), fill=AMBER, width=7)
            draw.polygon(
                [(arrow_x + gap - 14, y + box_h / 2 - 12), (arrow_x + gap, y + box_h / 2), (arrow_x + gap - 14, y + box_h / 2 + 12)],
                fill=AMBER,
            )
    draw.rounded_rectangle((150, 620, 1450, 770), radius=20, fill=LIGHT_GRAY)
    draw.text((190, 660), "Traceability rule", fill=NAVY, font=load_font(26, bold=True))
    draw.text(
        (190, 710),
        "Every remediation and evidence-tracker row links back to a control, assessment finding, risk, and asset context.",
        fill=BLACK,
        font=load_font(23),
    )
    return save_image(image, "grc_workflow.png")


def risk_color(score: int) -> str:
    if score >= 17:
        return "#B91C1C"
    if score >= 10:
        return "#EA580C"
    if score >= 5:
        return "#F4C95D"
    return "#8BC99A"


def draw_risk_heatmap(risks: list[dict[str, str]]) -> Path:
    image, draw = canvas("Inherent Risk Heatmap", "15 synthetic risks plotted by likelihood and impact")
    counts = Counter((int(row["likelihood_score"]), int(row["impact_score"])) for row in risks)
    cell = 112
    left, top = 430, 190
    for impact in range(1, 6):
        for likelihood in range(1, 6):
            x = left + (likelihood - 1) * cell
            y = top + (5 - impact) * cell
            score = likelihood * impact
            draw.rectangle((x, y, x + cell, y + cell), fill=risk_color(score), outline=WHITE, width=4)
            draw.text((x + cell / 2, y + 42), str(counts[(likelihood, impact)]), anchor="mm", fill=WHITE if score >= 10 else NAVY, font=load_font(34, bold=True))
            draw.text((x + cell / 2, y + 80), f"score {score}", anchor="mm", fill=WHITE if score >= 10 else NAVY, font=load_font(16))
    for value in range(1, 6):
        draw.text((left + (value - 0.5) * cell, top + 5 * cell + 30), str(value), anchor="mm", fill=BLACK, font=load_font(22, bold=True))
        draw.text((left - 35, top + (5 - value + 0.5) * cell), str(value), anchor="mm", fill=BLACK, font=load_font(22, bold=True))
    draw.text((left + 2.5 * cell, top + 5 * cell + 72), "Likelihood", anchor="mm", fill=NAVY, font=load_font(26, bold=True))
    draw.text((left - 105, top + 2.5 * cell), "Impact", anchor="mm", fill=NAVY, font=load_font(26, bold=True))
    high = sum(1 for row in risks if row["priority"] == "High")
    draw.rounded_rectangle((1120, 230, 1480, 510), radius=18, fill=LIGHT_GRAY)
    draw.text((1160, 270), "Portfolio snapshot", fill=NAVY, font=load_font(27, bold=True))
    draw.text((1160, 330), f"High-priority risks: {high}", fill=RED, font=load_font(24, bold=True))
    draw.text((1160, 385), f"Medium-priority risks: {len(risks) - high}", fill=AMBER, font=load_font(23, bold=True))
    draw.text((1160, 440), "No Low-rated risks", fill=GRAY, font=load_font(22))
    return save_image(image, "risk_heatmap.png")


def draw_bar_panel(
    draw: ImageDraw.ImageDraw,
    values: list[tuple[str, int]],
    bounds: tuple[int, int, int, int],
    title: str,
    palette: list[str],
) -> None:
    x1, y1, x2, y2 = bounds
    draw.rounded_rectangle(bounds, radius=20, fill=LIGHT_GRAY)
    draw.text((x1 + 35, y1 + 30), title, fill=NAVY, font=load_font(26, bold=True))
    max_value = max(value for _, value in values) or 1
    bar_left = x1 + 210
    bar_width = x2 - bar_left - 70
    row_height = (y2 - y1 - 100) / len(values)
    for index, (label, value) in enumerate(values):
        y = y1 + 90 + index * row_height
        draw.text((x1 + 35, y + 8), label, fill=BLACK, font=load_font(20, bold=True))
        width = int(bar_width * value / max_value)
        draw.rounded_rectangle((bar_left, y, bar_left + width, y + 38), radius=10, fill=palette[index % len(palette)])
        draw.text((bar_left + width + 15, y + 19), str(value), anchor="lm", fill=BLACK, font=load_font(22, bold=True))


def draw_control_gap_summary(controls: list[dict[str, str]]) -> Path:
    image, draw = canvas("Control Implementation Status", "15 controls assessed across governance, security, resilience, and operations")
    counts = Counter(row["implementation_status"] for row in controls)
    values = [(name, counts[name]) for name in ("Partial", "Missing", "Weak", "Planned")]
    draw_bar_panel(draw, values, (160, 190, 1440, 710), "Implementation status", [BLUE, RED, AMBER, GRAY])
    draw.text((190, 780), "Key message: no control is represented as fully implemented in this simulated baseline.", fill=NAVY, font=load_font(24, bold=True))
    return save_image(image, "control_gap_summary.png")


def draw_remediation_summary(poam: list[dict[str, str]]) -> Path:
    image, draw = canvas("Remediation Portfolio", "15 POA&M actions with explicit owners, target dates, evidence, and closure criteria")
    status = Counter(row["status"] for row in poam)
    priority = Counter(row["priority"] for row in poam)
    draw_bar_panel(
        draw,
        [(name, status[name]) for name in ("Open", "In Progress", "Planned")],
        (90, 190, 780, 710),
        "Status",
        [RED, BLUE, GRAY],
    )
    draw_bar_panel(
        draw,
        [(name, priority[name]) for name in ("High", "Medium")],
        (820, 190, 1510, 710),
        "Priority",
        [RED, AMBER],
    )
    draw.text((130, 780), "Assessment cut-off: 13 July 2026. Dates and owners are simulated for portfolio demonstration.", fill=NAVY, font=load_font(23, bold=True))
    return save_image(image, "remediation_status_summary.png")


def report_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=28,
            textColor=colors.HexColor(NAVY),
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor(GRAY),
            spaceAfter=12,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor(NAVY),
            spaceBefore=8,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor(BLUE),
            spaceBefore=6,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=13.2,
            textColor=colors.HexColor(BLACK),
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor(BLACK),
        ),
        "card_number": ParagraphStyle(
            "CardNumber",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=20,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "card_label": ParagraphStyle(
            "CardLabel",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
            textColor=colors.HexColor(GRAY),
            alignment=TA_CENTER,
        ),
    }


def metric_card(value: str, label: str, styles: dict[str, ParagraphStyle]) -> Table:
    table = Table([[Paragraph(value, styles["card_number"])], [Paragraph(label, styles["card_label"])]], colWidths=[39 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(LIGHT_BLUE)),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9CCE0")),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
                ("TOPPADDING", (0, 1), (-1, 1), 2),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
            ]
        )
    )
    return table


def report_table(rows: list[list[object]], widths: list[float], header: bool = True) -> Table:
    header_style = ParagraphStyle(
        "TableHeader",
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9,
        textColor=colors.white,
    )
    body_style = ParagraphStyle(
        "TableBody",
        fontName="Helvetica",
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor(BLACK),
    )
    processed_rows: list[list[object]] = []
    for row_index, row in enumerate(rows):
        processed_row: list[object] = []
        for cell in row:
            if isinstance(cell, Paragraph):
                processed_row.append(cell)
            else:
                style = header_style if header and row_index == 0 else body_style
                processed_row.append(Paragraph(html.escape(str(cell)), style))
        processed_rows.append(processed_row)
    table = Table(processed_rows, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9D2DA")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 7.5),
            ]
        )
        commands.append(("FONTNAME", (0, 1), (-1, -1), "Helvetica"))
        commands.append(("FONTSIZE", (0, 1), (-1, -1), 7.2))
    table.setStyle(TableStyle(commands))
    return table


def footer(canvas_obj, doc) -> None:
    canvas_obj.saveState()
    width, _ = A4
    canvas_obj.setStrokeColor(colors.HexColor("#D7DEE5"))
    canvas_obj.line(18 * mm, 13 * mm, width - 18 * mm, 13 * mm)
    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.setFillColor(colors.HexColor(GRAY))
    canvas_obj.drawString(18 * mm, 8 * mm, "Synthetic portfolio case study - not an audit or certification assessment")
    canvas_obj.drawRightString(width - 18 * mm, 8 * mm, f"Page {doc.page}")
    canvas_obj.restoreState()


def generate_pdf(data: dict[str, list[dict[str, str]]], images: dict[str, Path]) -> Path:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    output = PDF_DIR / "IT_GRC_Project_Summary.pdf"
    styles = report_styles()
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
        title="IT GRC Risk and Control Assessment Case Study",
        author="Yohanes Wiliam Hadiprojo",
        subject="Synthetic IT governance, risk, control, evidence, and remediation portfolio",
    )

    assets = data["assets"]
    risks = data["risks"]
    controls = data["controls"]
    assessments = data["assessments"]
    poam = data["poam"]
    evidence = read_csv("evidence_tracker.csv")

    risk_priority = Counter(row["priority"] for row in risks)
    control_status = Counter(row["implementation_status"] for row in controls)
    evidence_status = Counter(row["evidence_status"] for row in evidence)
    poam_status = Counter(row["status"] for row in poam)

    story: list[object] = []
    story.append(Paragraph("IT GRC Risk &amp; Control Assessment", styles["title"]))
    story.append(Paragraph("Executive portfolio summary | Assessment cut-off: 13 July 2026", styles["subtitle"]))
    story.append(
        Paragraph(
            "A synthetic, evidence-led case study that connects assets, risks, controls, assessment findings, remediation actions, and management reporting for an internal academic services system.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 4 * mm))
    cards = [
        metric_card(str(len(assets)), "Assets in scope", styles),
        metric_card(str(len(risks)), "Risks assessed", styles),
        metric_card(str(risk_priority["High"]), "High-priority risks", styles),
        metric_card(str(len(controls)), "Controls assessed", styles),
    ]
    story.append(Table([cards], colWidths=[42 * mm] * 4, hAlign="LEFT"))
    story.append(Spacer(1, 4 * mm))
    cards2 = [
        metric_card(str(control_status["Missing"] + control_status["Weak"]), "Missing or weak controls", styles),
        metric_card(str(evidence_status["Not Available"]), "Evidence unavailable", styles),
        metric_card(str(poam_status["Open"]), "Open POA&M actions", styles),
        metric_card(str(poam_status["In Progress"]), "Actions in progress", styles),
    ]
    story.append(Table([cards2], colWidths=[42 * mm] * 4, hAlign="LEFT"))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Executive conclusion", styles["h1"]))
    conclusion_rows = [
        ["Theme", "Evidence-based conclusion"],
        ["Access governance", "The highest residual risk is privileged access management (R-001, residual score 15). Quarterly recertification evidence is incomplete."],
        ["Detection and resilience", "Admin log review, vulnerability tracking, and restore-test evidence are missing or insufficiently documented."],
        ["Audit readiness", "Nine evidence sets are partial and six are unavailable. No control is presented as fully evidenced in the baseline."],
        ["Remediation", "Fifteen POA&M actions define owners, target dates, evidence requirements, dependencies, and closure criteria."],
    ]
    story.append(report_table(conclusion_rows, [37 * mm, 133 * mm]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Scope boundary", styles["h2"]))
    story.append(
        Paragraph(
            "This is a self-directed portfolio exercise using synthetic data. It is not a real company engagement, legal opinion, ISO/IEC 27001 certification audit, COBIT capability assessment, or claim of operating control effectiveness.",
            styles["body"],
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("Risk and control posture", styles["title"]))
    story.append(Image(str(images["risk"]), width=150 * mm, height=84.4 * mm))
    story.append(Spacer(1, 3 * mm))
    top_risks = sorted(risks, key=lambda row: int(row["residual_risk_score"]), reverse=True)[:7]
    top_rows: list[list[object]] = [["Risk", "Area", "Inherent", "Residual", "Priority"]]
    for row in top_risks:
        top_rows.append([row["risk_id"], row["risk_area"], row["inherent_risk_score"], row["residual_risk_score"], row["priority"]])
    story.append(KeepTogether([Paragraph("Highest residual risks", styles["h2"]), report_table(top_rows, [18 * mm, 80 * mm, 24 * mm, 24 * mm, 24 * mm])]))
    story.append(Spacer(1, 4 * mm))
    story.append(Spacer(1, 2 * mm))
    story.append(Image(str(images["controls"]), width=150 * mm, height=84.4 * mm))

    story.append(PageBreak())
    story.append(Paragraph("Remediation and evidence readiness", styles["title"]))
    story.append(Image(str(images["remediation"]), width=170 * mm, height=95.6 * mm))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("High-priority remediation portfolio", styles["h2"]))
    high_poam = [row for row in poam if row["priority"] == "High"]
    poam_rows: list[list[object]] = [["POA&M", "Control area", "Target", "Status", "Owner"]]
    for row in high_poam:
        poam_rows.append([row["poam_id"], row["control_area"], row["target_date"], row["status"], row["owner"]])
    story.append(report_table(poam_rows, [18 * mm, 50 * mm, 26 * mm, 25 * mm, 51 * mm]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Evidence interpretation", styles["h2"]))
    story.append(
        Paragraph(
            f"The evidence tracker contains {len(evidence)} rows: {evidence_status['Partial']} partial and {evidence_status['Not Available']} unavailable. The repository records required evidence and remediation ownership but deliberately does not fabricate evidence files or successful review dates.",
            styles["body"],
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("Methodology, traceability, and sources", styles["title"]))
    story.append(Image(str(images["workflow"]), width=170 * mm, height=95.6 * mm))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Assessment approach", styles["h2"]))
    methodology = [
        "Define scope through a 12-asset inventory.",
        "Identify 15 risk scenarios using likelihood, impact, inherent risk, existing controls, and residual risk.",
        "Map 15 controls to risk, asset, evidence, owner, frequency, and public framework concepts.",
        "Assess design, implementation, operating effectiveness, and evidence status using simulated test procedures.",
        "Translate findings into 15 POA&M actions and a centralized evidence tracker.",
        "Validate referential integrity and run management queries in an in-memory SQLite database.",
    ]
    for item in methodology:
        story.append(Paragraph(f"- {html.escape(item)}", styles["body"]))
    story.append(Paragraph("Primary public references", styles["h2"]))
    sources = [
        ("NIST Cybersecurity Framework 2.0", "https://www.nist.gov/cyberframework"),
        ("NIST SP 800-30 Rev. 1", "https://csrc.nist.gov/pubs/sp/800/30/r1/final"),
        ("NIST SP 800-53 Rev. 5", "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final"),
        ("NIST SP 800-53A Rev. 5", "https://csrc.nist.gov/pubs/sp/800/53/a/r5/final"),
        ("ISO/IEC 27001:2022 public overview", "https://www.iso.org/standard/27001"),
        ("CIS Critical Security Controls v8.1", "https://www.cisecurity.org/controls"),
        ("ISACA COBIT resources", "https://www.isaca.org/resources/cobit"),
        ("Indonesia Law No. 27 of 2022 on Personal Data Protection", "https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022"),
    ]
    source_rows: list[list[object]] = [["Reference", "Official URL"]]
    for name, url in sources:
        source_rows.append([Paragraph(name, styles["small"]), Paragraph(f'<link href="{url}" color="#2563A6">{url}</link>', styles["small"])])
    story.append(report_table(source_rows, [62 * mm, 108 * mm]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Important limitation", styles["h2"]))
    story.append(
        Paragraph(
            "ISO/IEC 27001 mappings are limited to publicly described ISMS and confidentiality, integrity, availability, and risk-management concepts. The project does not reproduce copyrighted standard text or claim clause-level conformity.",
            styles["body"],
        )
    )

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return output


def main() -> None:
    data = load_project_data()
    evidence_path = generate_evidence_tracker(data)
    images = {
        "workflow": draw_workflow(),
        "risk": draw_risk_heatmap(data["risks"]),
        "controls": draw_control_gap_summary(data["controls"]),
        "remediation": draw_remediation_summary(data["poam"]),
    }
    pdf_path = generate_pdf(data, images)
    print(f"generated={evidence_path.relative_to(ROOT)}")
    for path in images.values():
        print(f"generated={path.relative_to(ROOT)}")
    print(f"generated={pdf_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
