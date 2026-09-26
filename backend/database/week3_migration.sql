-- GovernX Week 3 database migration
-- Keeps persisted financial-risk and governance-profile
-- tables aligned with database/models.py.

CREATE TABLE IF NOT EXISTS financial_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id TEXT NOT NULL UNIQUE,
    asset_name TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    cloud_provider TEXT NOT NULL,
    business_function TEXT NOT NULL,
    data_sensitivity TEXT NOT NULL,
    criticality TEXT NOT NULL,
    asset_value REAL NOT NULL,
    revenue_dependency REAL NOT NULL DEFAULT 0,
    customer_dependency REAL NOT NULL DEFAULT 0,
    recovery_cost REAL NOT NULL DEFAULT 0,
    regulatory_exposure REAL NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_financial_assets_asset_id
ON financial_assets(asset_id);

CREATE INDEX IF NOT EXISTS idx_financial_assets_criticality
ON financial_assets(criticality);

CREATE TABLE IF NOT EXISTS governance_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_name TEXT NOT NULL DEFAULT 'Demo Enterprise',
    industry TEXT NOT NULL DEFAULT 'Technology',
    organization_size TEXT NOT NULL DEFAULT '500-1000 employees',
    security_policy_status TEXT NOT NULL DEFAULT 'Mostly implemented',
    cybersecurity_policy_review_frequency TEXT NOT NULL DEFAULT 'Quarterly',
    risk_management_policy TEXT NOT NULL DEFAULT 'Documented',
    access_control_policy TEXT NOT NULL DEFAULT 'Implemented',
    data_protection_policy TEXT NOT NULL DEFAULT 'Implemented',
    incident_response_policy TEXT NOT NULL DEFAULT 'Implemented',
    business_continuity_policy TEXT NOT NULL DEFAULT 'Implemented',
    vendor_supplier_security_policy TEXT NOT NULL DEFAULT 'Required',
    third_party_risk_management TEXT NOT NULL DEFAULT 'Formal review',
    security_awareness_training TEXT NOT NULL DEFAULT 'Quarterly',
    asset_ownership TEXT NOT NULL DEFAULT 'Assigned by business owners',
    risk_appetite TEXT NOT NULL DEFAULT 'Low to moderate',
    compliance_requirements TEXT,
    policy_owner TEXT NOT NULL DEFAULT 'CISO',
    last_policy_review_date TEXT NOT NULL DEFAULT '2026-09-01',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);