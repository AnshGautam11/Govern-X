from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_post_governance_responses():
    payload = {
        "risk_owner_assigned": True,
        "security_policy_reviewed": True,
        "incident_response_plan_exists": False,
        "third_party_risk_reviewed": True,
    }

    response = client.post("/governance/responses", json=payload)

    assert response.status_code in (200, 201)


def test_get_governance_responses():
    response = client.get("/governance/responses")

    assert response.status_code == 200


def test_governance_questionnaire_all_fields():
    payload = {
        "risk_owner_assigned": True,
        "security_policy_reviewed": False,
        "incident_response_plan_exists": True,
        "third_party_risk_reviewed": False,
    }

    response = client.post("/governance/responses", json=payload)

    assert response.status_code in (200, 201)