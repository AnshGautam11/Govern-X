"""
W2-Day2 tests for GET /scan/history.

Uses FastAPI's TestClient against the real app, but seeds data through
an isolated in-memory DB session so these tests don't depend on
governx.db having real scan data in it.
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from database.db import Base
from database.persistence import save_scan_results
from models.schemas import CheckResult, CheckStatus, Severity

client = TestClient(app)


def _seed_history():
    """Write a couple of scan results into the real (test-run) DB via the
    same persistence function /scan/aws uses, so /scan/history has
    something to return."""
    results = [
        CheckResult(
            check_id="s3_public_access_block",
            resource_id="bucket-a",
            status=CheckStatus.PASS,
            severity=Severity.HIGH,
            detail="Public access block fully enabled",
        ),
        CheckResult(
            check_id="iam_root_mfa",
            resource_id="root-account",
            status=CheckStatus.FAIL,
            severity=Severity.CRITICAL,
            detail="Root account MFA is NOT enabled",
        ),
    ]
    save_scan_results(results)


def test_scan_history_returns_entries():
    _seed_history()

    response = client.get("/scan/history")

    assert response.status_code == 200
    data = response.json()
    assert "entries" in data
    assert len(data["entries"]) >= 2

    first = data["entries"][0]
    assert "id" in first
    assert "check_id" in first
    assert "resource_id" in first
    assert "status" in first
    assert "detail" in first
    assert "scanned_at" in first


def test_scan_history_respects_limit():
    _seed_history()
    _seed_history()

    response = client.get("/scan/history?limit=1")

    assert response.status_code == 200
    data = response.json()
    assert len(data["entries"]) == 1


def test_scan_history_newest_first():
    _seed_history()

    response = client.get("/scan/history?limit=2")
    data = response.json()

    timestamps = [entry["scanned_at"] for entry in data["entries"]]
    assert timestamps == sorted(timestamps, reverse=True)