"""
W3-Day5 tests for GET /reports/combined — the unified compliance + risk +
governance report.
"""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_combined_report_returns_all_three_sections():
    response = client.get("/reports/combined")

    assert response.status_code == 200
    data = response.json()

    assert "maturity" in data
    assert "governance" in data
    assert "risk" in data
    assert "generated_at" in data


def test_combined_report_maturity_has_pillars():
    response = client.get("/reports/combined")
    data = response.json()

    assert "pillars" in data["maturity"]
    assert "overall" in data["maturity"]


def test_combined_report_governance_has_responses_list():
    response = client.get("/reports/combined")
    data = response.json()

    assert "responses" in data["governance"]
    assert isinstance(data["governance"]["responses"], list)


def test_combined_report_risk_includes_disclaimer():
    """The Week 3 tracker requires the sample-data disclaimer to always be present."""
    response = client.get("/reports/combined")
    data = response.json()

    assert "disclaimer" in data["risk"]
    assert "assumed" in data["risk"]["disclaimer"].lower()


def test_combined_report_rejects_unsupported_sector():
    response = client.get("/reports/combined?sector=not-a-real-sector")
    assert response.status_code == 422