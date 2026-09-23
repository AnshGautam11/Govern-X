"""
W3-Day1 tests for the asset inventory DB schema.

Mirrors database/schema.sql's `assets` table: name, value, criticality —
used by the Week 3 financial risk (Monte Carlo) model to attach a dollar
value and criticality tier to resources.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.db import Base
from database.models import AssetDB


def _make_test_session():
    """Isolated in-memory SQLite DB, separate from the real governx.db file."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)
    return TestSession()


def test_create_asset_with_name_value_criticality():
    db = _make_test_session()

    asset = AssetDB(
        name="Customer Database",
        value=85000.0,
        criticality="critical",
    )
    db.add(asset)
    db.commit()

    rows = db.query(AssetDB).all()
    assert len(rows) == 1
    assert rows[0].name == "Customer Database"
    assert rows[0].value == 85000.0
    assert rows[0].criticality == "critical"
    assert rows[0].id is not None
    assert rows[0].created_at is not None


def test_create_multiple_assets_with_different_criticality():
    db = _make_test_session()

    assets = [
        AssetDB(name="Web Server", value=20000.0, criticality="medium"),
        AssetDB(name="Payment Processing System", value=150000.0, criticality="critical"),
        AssetDB(name="Internal Wiki", value=5000.0, criticality="low"),
    ]
    db.add_all(assets)
    db.commit()

    rows = db.query(AssetDB).order_by(AssetDB.value.desc()).all()
    assert len(rows) == 3
    assert rows[0].name == "Payment Processing System"
    assert rows[-1].name == "Internal Wiki"


def test_asset_query_by_criticality():
    db = _make_test_session()

    db.add_all(
        [
            AssetDB(name="Backup Server", value=15000.0, criticality="low"),
            AssetDB(name="Core Banking API", value=200000.0, criticality="critical"),
        ]
    )
    db.commit()

    critical_assets = (
        db.query(AssetDB).filter(AssetDB.criticality == "critical").all()
    )
    assert len(critical_assets) == 1
    assert critical_assets[0].name == "Core Banking API"