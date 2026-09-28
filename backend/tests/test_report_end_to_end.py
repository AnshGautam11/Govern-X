from io import BytesIO
from datetime import datetime

from pypdf import PdfReader

from database.models import ScanResultDB
from database.persistence import SessionLocal
from reports.report_service import build_report_data
from reports.pdf_report import build_executive_pdf


def test_scan_to_score_to_report_to_pdf():

    db = SessionLocal()

    try:
        db.query(ScanResultDB).delete()
        db.commit()

        timestamp = datetime.utcnow()

        db.add_all(
            [
                ScanResultDB(
                    check_id="cloudtrail_enabled",
                    resource_id="demo-trail",
                    status="pass",
                    severity="high",
                    detail="CloudTrail is enabled.",
                    scanned_at=timestamp,
                ),
                ScanResultDB(
                    check_id="vpc_flow_logs_enabled",
                    resource_id="demo-vpc",
                    status="fail",
                    severity="high",
                    detail="VPC Flow Logs are not enabled.",
                    scanned_at=timestamp,
                ),
            ]
        )

        db.commit()

        # Scan results -> scored executive report
        report = build_report_data(db)

        assert report["status"] == "ready"
        assert report["summary"]["total_checks"] == 2
        assert report["summary"]["passed"] == 1
        assert report["summary"]["failed"] == 1
        assert report["summary"]["overall_score"] is not None

        # Executive report -> PDF
        pdf = build_executive_pdf(report)

        assert pdf.startswith(b"%PDF")

        reader = PdfReader(BytesIO(pdf))

        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        assert "Executive Compliance Report" in text
        assert "Compliance score" in text
        assert "demo-vpc" in text

    finally:
        db.close()