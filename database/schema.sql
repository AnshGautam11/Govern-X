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
