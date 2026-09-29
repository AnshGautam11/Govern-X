"""
Executive PDF renderer for GovernX Week 4.
"""

from __future__ import annotations

from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


PAGE_WIDTH, PAGE_HEIGHT = A4


def _money(value: Any) -> str:
    if value is None:
        return "No Data"

    return f"INR {float(value):,.0f}"


def _score(value: Any) -> str:
    if value is None:
        return "No Data"

    return f"{float(value):.1f}%"


def _footer(canvas, doc):
    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        7,
    )

    canvas.setFillColor(
        colors.HexColor("#64748B")
    )

    canvas.drawString(
        18 * mm,
        10 * mm,
        "GovernX — Executive Compliance Report",
    )

    canvas.drawRightString(
        PAGE_WIDTH - 18 * mm,
        10 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()


def build_executive_pdf(
    report: dict[str, Any],
) -> bytes:

    buffer = BytesIO()

    frame = Frame(
        18 * mm,
        17 * mm,
        PAGE_WIDTH - 36 * mm,
        PAGE_HEIGHT - 35 * mm,
        id="normal",
    )

    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=17 * mm,
        bottomMargin=17 * mm,
        title="GovernX Executive Compliance Report",
        author="GovernX",
    )

    doc.addPageTemplates(
        [
            PageTemplate(
                id="report",
                frames=frame,
                onPage=_footer,
            )
        ]
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=8,
        spaceAfter=7,
    )

    body_style = ParagraphStyle(
        "BodySmall",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
    )

    story = []

    summary = report["summary"]
    governance = report["governance"]

    story.append(
        Paragraph(
            "GOVERNX",
            ParagraphStyle(
                "Kicker",
                parent=styles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=8,
                textColor=colors.HexColor("#0284C7"),
            ),
        )
    )

    story.append(
        Paragraph(
            "Executive Compliance Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "NIST CSF 2.0 posture, governance self-attestation, prioritized remediation and modeled risk.",
            body_style,
        )
    )

    story.append(Spacer(1, 5 * mm))

    status = (
        "No Data"
        if report["status"] == "no_data"
        else "Assessment available"
    )

    executive_rows = [
        [
            "Posture",
            status,
            "Maturity tier",
            summary["tier_name"],
        ],
        [
            "Compliance score",
            _score(summary["overall_score"]),
            "Open gaps",
            (
                summary["failed"]
                if summary["failed"] is not None
                else "No Data"
            ),
        ],
        [
            "Governance",
            _score(governance["score"]),
            "Governance source",
            "Self-attested",
        ],
    ]

    table = Table(
        executive_rows,
        colWidths=[
            34 * mm,
            48 * mm,
            36 * mm,
            52 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#F8FAFC"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (2, 0),
                    (2, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8.5,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(table)

    story.append(
        Paragraph(
            "NIST CSF 2.0 Summary",
            section_style,
        )
    )

    pillar_rows = [
        ["Function", "Score", "Tier"]
    ]

    for pillar in report["pillars"]:
        pillar_rows.append(
            [
                pillar["function"],
                _score(pillar["score"]),
                pillar["tier_name"],
            ]
        )

    pillar_table = Table(
        pillar_rows,
        colWidths=[
            55 * mm,
            45 * mm,
            70 * mm,
        ],
    )

    pillar_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#E2E8F0"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F8FAFC"),
                    ],
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8.5,
                ),
            ]
        )
    )

    tier_backgrounds = {
    "Partial": "#FEE2E2",
    "Risk Informed": "#FEF3C7",
    "Repeatable": "#DBEAFE",
    "Adaptive": "#DCFCE7",
    "No Data": "#F1F5F9",
    }

    pillar_style = [
    (
        "BACKGROUND",
        (0, 0),
        (-1, 0),
        colors.HexColor("#E2E8F0"),
    ),
    (
        "FONTNAME",
        (0, 0),
        (-1, 0),
        "Helvetica-Bold",
    ),
    (
        "GRID",
        (0, 0),
        (-1, -1),
        0.3,
        colors.HexColor("#CBD5E1"),
    ),
]

    for row_index, pillar in enumerate(
    report["pillars"],
    start=1,
    ):
        
        pillar_style.append(
        (
            "BACKGROUND",
            (2, row_index),
            (2, row_index),
            colors.HexColor(
                tier_backgrounds.get(
                    pillar["tier_name"],
                    "#F1F5F9",
                )
            ),
        )
    )

        pillar_table.setStyle(
          TableStyle(pillar_style)
        )
    
    story.append(pillar_table)

    story.append(
        Paragraph(
            "Top Compliance Gaps",
            section_style,
        )
    )

    if not report["gaps"]:
        story.append(
            Paragraph(
                "No Data — no persisted scan gaps are available.",
                body_style,
            )
        )
    else:
        gap_rows = [
            [
                "Control",
                "Severity",
                "NIST",
                "Resource",
            ]
        ]

        for gap in report["gaps"][:8]:
            gap_rows.append(
                [
                    gap["check_id"],
                    gap["severity"].upper(),
                    gap["csf_subcategory"],
                    gap["resource_id"],
                ]
            )

        gap_table = Table(
            gap_rows,
            colWidths=[
                52 * mm,
                25 * mm,
                28 * mm,
                65 * mm,
            ],
            repeatRows=1,
        )

        gap_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#E2E8F0"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.3,
                        colors.HexColor("#CBD5E1"),
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7.5,
                    ),
                ]
            )
        )

        story.append(gap_table)
    remediation_items = report.get("remediation") or []
    if remediation_items:
        cell_style = ParagraphStyle(
            "cell_style",
            parent=body_style,
            fontSize=7,
            leading=9,
        )

        story.append(Paragraph("Prioritized Remediation", section_style))

        rem_rows = [["#", "Control", "Severity", "NIST", "Rationale"]]
        for item in remediation_items:
            rem_rows.append(
                [
                    str(item["rank"]),
                    Paragraph(item["check_id"], cell_style),
                    item["severity"].upper(),
                    item["csf_subcategory"],
                    Paragraph(item["remediation"], cell_style),
                ]
            )

        rem_table = Table(
            rem_rows,
            colWidths=[9 * mm, 36 * mm, 18 * mm, 20 * mm, 82 * mm],
            repeatRows=1,
        )
        rem_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CBD5E1")),
                    ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        story.append(rem_table)
        story.append(Spacer(1, 4 * mm))

    roi = report.get("roi") or {}
    roi_items = roi.get("items") or []
    if roi_items:
        story.append(Paragraph("Remediation ROI (Sample Data)", section_style))

        roi_rows = [
            ["Control", "Baseline loss", "Risk reduced", "Remediation cost", "ROI ratio"]
        ]
        for item in roi_items:
            roi_rows.append(
                [
                    item["check_id"],
                    _money(item["baseline_expected_loss"]),
                    _money(item["risk_reduced"]),
                    _money(item["assumed_remediation_cost"]),
                    f"{item['roi_ratio']:.2f}x",
                ]
            )

        roi_table = Table(
            roi_rows,
            colWidths=[45 * mm, 30 * mm, 30 * mm, 32 * mm, 20 * mm],
            repeatRows=1,
        )
        roi_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CBD5E1")),
                    ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ]
            )
        )
        story.append(roi_table)

        if roi.get("message"):
            story.append(Spacer(1, 1.5 * mm))
            story.append(Paragraph(roi["message"], body_style))
        story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "Governance Evidence Status",
            section_style,
        )
    )

    story.append(
        Paragraph(
            f"Questions answered: {governance['answered']} / "
            f"{governance['total']}. "
            f"Completion: {_score(governance['completion'])}. "
            "Governance responses are self-attested and are not independently verified evidence.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Important Disclaimers",
            section_style,
        )
    )

    for disclaimer in report["disclaimers"]:
        story.append(
            Paragraph(
                f"• {disclaimer}",
                body_style,
            )
        )
        story.append(Spacer(1, 1.5 * mm))

    doc.build(story)

    return buffer.getvalue()

