from io import BytesIO

from pypdf import PdfReader

from reports.pdf_report import build_executive_pdf


def test_pdf_contains_required_disclaimers():

    report = {
        "generated_at": "2026-09-28T00:00:00Z",
        "status": "no_data",
        "summary": {
            "overall_score": None,
            "tier": None,
            "tier_name": "No Data",
            "total_checks": None,
            "passed": None,
            "failed": None,
            "errors": None,
        },
        "pillars": [
            {
                "function": name,
                "score": None,
                "tier": None,
                "tier_name": "No Data",
            }
            for name in [
                "Govern",
                "Identify",
                "Protect",
                "Detect",
                "Respond",
                "Recover",
            ]
        ],
        "gaps": [],
        "remediation": [],
        "governance": {
            "answered": 0,
            "total": 4,
            "score": None,
            "completion": 0,
            "self_attested": True,
        },
        "roi": {
            "status": "no_gap_data",
            "items": [],
            "message": "No failed controls.",
        },
        "disclaimers": [
            "Financial figures are sample/assumed data.",
            "Governance answers are self-attested.",
            "No Data is shown when no scan has been persisted.",
        ],
    }

    pdf = build_executive_pdf(report)

    assert pdf.startswith(b"%PDF")

    reader = PdfReader(
        BytesIO(pdf)
    )

    text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    assert "Executive Compliance Report" in text
    assert "sample/assumed data" in text
    assert "self-attested" in text
    assert "No Data" in text