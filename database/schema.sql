-- GovernX core schema
-- Applies to SQLite (dev) and PostgreSQL (prod) with minor type tweaks.

CREATE TABLE IF NOT EXISTS checks (
    id TEXT PRIMARY KEY,              -- e.g. 's3_public_access_block'
    description TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical'))
);

CREATE TABLE IF NOT EXISTS csf_mappings (
    check_id TEXT PRIMARY KEY REFERENCES checks(id),
    csf_function TEXT NOT NULL CHECK (
        csf_function IN ('Govern', 'Identify', 'Protect', 'Detect', 'Respond', 'Recover')
    ),
    csf_subcategory TEXT NOT NULL,    -- e.g. 'PR.DS-01'
    justification TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scan_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    check_id TEXT NOT NULL REFERENCES checks(id),
    resource_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pass', 'fail', 'error')),
    severity TEXT,
    detail TEXT,
    scanned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_scan_results_check_id ON scan_results(check_id);
CREATE INDEX IF NOT EXISTS idx_scan_results_scanned_at ON scan_results(scanned_at);

CREATE INDEX IF NOT EXISTS idx_scan_results_check_id
ON scan_results(check_id);

CREATE INDEX IF NOT EXISTS idx_scan_results_scanned_at
ON scan_results(scanned_at);

CREATE INDEX IF NOT EXISTS idx_scan_results_scanned_at_check_id
ON scan_results(scanned_at, check_id);

-- Week 3: Govern questionnaire

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

CREATE INDEX IF NOT EXISTS idx_governance_responses_question
ON governance_responses(question_id);

CREATE INDEX IF NOT EXISTS idx_governance_responses_answered_at
ON governance_responses(answered_at);

CREATE INDEX IF NOT EXISTS idx_governance_evidence_response
ON governance_evidence(response_id);


-- Week 3: Asset inventory (financial risk / Monte Carlo model)

CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    value REAL NOT NULL CHECK (value >= 0),
    criticality TEXT NOT NULL CHECK (criticality IN ('low', 'medium', 'high', 'critical')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_assets_criticality ON assets(criticality);

-- Week 3: Financial risk assets

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

-- Week 3: Governance profile

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