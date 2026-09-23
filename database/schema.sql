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