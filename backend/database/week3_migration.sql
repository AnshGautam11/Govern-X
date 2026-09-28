-- GovernX Week 3 database migration
-- Keeps persisted financial-risk and governance-profile
-- tables aligned with database/models.py.

-- Core governance questionnaire tables (W3)
CREATE TABLE IF NOT EXISTS governance_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_key TEXT NOT NULL UNIQUE,
    question_text TEXT NOT NULL,
    csf_category TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS governance_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    answer BOOLEAN NOT NULL,
    notes TEXT,
    answered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES governance_questions(id)
);

CREATE TABLE IF NOT EXISTS governance_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response_id INTEGER NOT NULL,
    evidence_type TEXT NOT NULL,
    evidence_reference TEXT NOT NULL,
    description TEXT,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (response_id) REFERENCES governance_responses(id)
);

CREATE INDEX IF NOT EXISTS idx_governance_questions_key
ON governance_questions(question_key);

CREATE INDEX IF NOT EXISTS idx_governance_questions_category_active
ON governance_questions(csf_category, active);

CREATE INDEX IF NOT EXISTS idx_governance_responses_question
ON governance_responses(question_id);

CREATE INDEX IF NOT EXISTS idx_governance_responses_answered_at
ON governance_responses(answered_at);

CREATE INDEX IF NOT EXISTS idx_governance_responses_question_answered
ON governance_responses(question_id, answered_at);

CREATE INDEX IF NOT EXISTS idx_governance_audit_question_submitted
ON governance_response_audit(question_id, submitted_at);

CREATE INDEX IF NOT EXISTS idx_governance_evidence_response
ON governance_evidence(response_id);

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

-- Governance response audit trail (W3-Day5)
-- Stores immutable snapshots of questionnaire submissions.

CREATE TABLE IF NOT EXISTS governance_response_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id TEXT NOT NULL,
    question_id INTEGER NOT NULL,
    answer BOOLEAN NOT NULL,
    notes TEXT,
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES governance_questions(id)
);

CREATE INDEX IF NOT EXISTS idx_governance_audit_submission
ON governance_response_audit(submission_id);

CREATE INDEX IF NOT EXISTS idx_governance_audit_submitted_at
ON governance_response_audit(submitted_at);