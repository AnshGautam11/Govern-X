from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_governance_history_endpoint():
    response = client.get("/governance/history")

    assert response.status_code == 200

    data = response.json()

    assert "history" in data
    assert isinstance(data["history"], list)


def test_governance_submission_is_added_to_history():
    payload = {
        "risk_owner_assigned": True,
        "security_policy_reviewed": False,
        "incident_response_plan_exists": True,
        "third_party_risk_reviewed": False,
    }

    submit_response = client.post(
        "/governance/responses",
        json=payload,
    )

    assert submit_response.status_code == 201

    history_response = client.get(
        "/governance/history"
    )

    assert history_response.status_code == 200

    history = history_response.json()["history"]

    assert len(history) >= 1

    latest_submission = history[0]

    assert "submission_id" in latest_submission
    assert "submitted_at" in latest_submission
    assert "responses" in latest_submission

    answers = {
        item["question_key"]: item["answer"]
        for item in latest_submission["responses"]
    }

    for question_key, expected_answer in payload.items():
        assert answers[question_key] == expected_answer