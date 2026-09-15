-- GovernX Week 2 database migration
-- Creates the tables required for NIST CSF mapping
-- and persistent scan history.

CREATE TABLE IF NOT EXISTS checks (
    id TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    severity TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS csf_mappings (
    check_id TEXT PRIMARY KEY,
    csf_function TEXT NOT NULL,
    csf_subcategory TEXT NOT NULL,
    justification TEXT NOT NULL,
    FOREIGN KEY (check_id) REFERENCES checks(id)
);

CREATE TABLE IF NOT EXISTS scan_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    check_id TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    status TEXT NOT NULL,
    detail TEXT,
    scanned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (check_id) REFERENCES checks(id)
);

CREATE INDEX IF NOT EXISTS idx_scan_results_check_id
ON scan_results(check_id);

CREATE INDEX IF NOT EXISTS idx_scan_results_scanned_at
ON scan_results(scanned_at);

CREATE TABLE IF NOT EXISTS mock_scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_name TEXT NOT NULL,
    check_id TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    detail TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_mock_scenarios_name
ON mock_scenarios(scenario_name);

CREATE INDEX IF NOT EXISTS idx_scan_results_scanned_at_check_id
ON scan_results(scanned_at, check_id);