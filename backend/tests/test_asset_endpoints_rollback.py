"""
W3-Day4 — test that a failed asset save rolls back cleanly and doesn't
poison the session for subsequent requests in the same test run.
"""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_session_still_usable_after_a_failed_create():
    """A bad request that trips validation shouldn't break later requests."""
    bad_response = client.post(
        "/assets",
        json={"name": "Bad Asset", "value": -1.0, "criticality": "low"},
    )
    assert bad_response.status_code == 422

    good_response = client.post(
        "/assets",
        json={"name": "Good Asset", "value": 500.0, "criticality": "low"},
    )
    assert good_response.status_code == 201

    list_response = client.get("/assets")
    assert list_response.status_code == 200
    names = [a["name"] for a in list_response.json()["assets"]]
    assert "Good Asset" in names