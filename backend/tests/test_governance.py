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


def test_governance_questions_use_persisted_catalog_and_latest_answers():
    submitted = {
        "risk_owner_assigned": True,
        "security_policy_reviewed": False,
        "incident_response_plan_exists": True,
        "third_party_risk_reviewed": False,
    }

    assert client.post("/governance/responses", json=submitted).status_code == 201
    response = client.get("/governance/questions")

    assert response.status_code == 200
    questions = {question["id"]: question for question in response.json()}
    assert set(questions) == set(submitted)
    assert {key: questions[key]["answer"] for key in submitted} == submitted
    assert all(question["category"] == "Govern" for question in questions.values())


def test_governance_score_is_calculated_from_latest_database_responses():
    response = client.get("/governance/score")

    assert response.status_code == 200
    score = response.json()
    assert score["total"] == 4
    assert score["answered"] == 4
    assert score["completion_percentage"] == 100.0
    assert score["score"] == 50.0
    assert score["by_function"]["GOVERN"] == 50.0