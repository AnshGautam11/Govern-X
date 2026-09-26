from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from database.db import Base
from database.models import (
    FinancialAssetDB,
    GovernanceProfileDB,
)
from database.persistence import (
    save_financial_asset,
    upsert_governance_profile,
)


def _make_test_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    TestSession = sessionmaker(bind=engine)

    return TestSession()


def test_financial_asset_upsert_updates_existing_record():
    db = _make_test_session()

    first = {
        "asset_id": "asset-1",
        "asset_name": "Payments API",
        "asset_type": "Application",
        "cloud_provider": "AWS",
        "business_function": "Payments",
        "data_sensitivity": "Sensitive",
        "criticality": "high",
        "asset_value": 1000000.0,
    }

    updated = {
        **first,
        "asset_value": 1500000.0,
    }

    save_financial_asset(first, db=db)
    save_financial_asset(updated, db=db)

    rows = db.query(FinancialAssetDB).all()

    assert len(rows) == 1
    assert rows[0].asset_value == 1500000.0


def test_financial_asset_failure_rolls_back_session():
    db = _make_test_session()

    valid = {
        "asset_id": "asset-2",
        "asset_name": "Reporting DB",
        "asset_type": "Database",
        "cloud_provider": "AWS",
        "business_function": "Reporting",
        "data_sensitivity": "Sensitive",
        "criticality": "medium",
        "asset_value": 500000.0,
    }

    save_financial_asset(valid, db=db)

    with pytest.raises(KeyError):
        save_financial_asset(
            {
                "asset_name": "Broken asset"
            },
            db=db,
        )

    assert db.query(FinancialAssetDB).count() == 1


def test_governance_profile_upsert_updates_existing_record():
    db = _make_test_session()

    first = {
        "organization_name": "Demo Enterprise",
        "industry": "Technology",
    }

    updated = {
        "organization_name": "Demo Enterprise",
        "industry": "Finance",
    }

    upsert_governance_profile(first, db=db)
    upsert_governance_profile(updated, db=db)

    rows = db.query(GovernanceProfileDB).all()

    assert len(rows) == 1
    assert rows[0].industry == "Finance"


def test_governance_profile_failure_rolls_back_session():
    db = _make_test_session()

    upsert_governance_profile(
        {
            "organization_name": "Demo Enterprise"
        },
        db=db,
    )

    with pytest.raises(Exception):
        upsert_governance_profile(
            {
                "organization_name": None
            },
            db=db,
        )

    assert db.query(GovernanceProfileDB).count() == 1