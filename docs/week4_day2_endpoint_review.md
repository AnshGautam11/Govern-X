# Week 4, Day 2: Endpoint Review

**Author:** Harshal Ghatbandhe

## Endpoint wiring
- GET /report/pdf is registered in app.py and returns HTTP 200 with a valid PDF (starts with %PDF-).
- reportlab and pypdf are declared in requirements.txt; a stale local venv caused an initial 500 (ModuleNotFoundError), not a repo defect.

## Check IDs
- The generated report uses real check IDs (iam_password_policy, cloudtrail_enabled, vpc_flow_logs_enabled) mapped to CSF subcategories (PR.AA-01, DE.CM-03, DE.CM-01).
- The mock-prefixed IDs (check_ebs_encryption, check_s3_encryption_at_rest) do not appear in the report. Those IDs exist only in old scan_results rows written by verify.py-style runs and are not in csf_mappings.py.

## Gap
- The report does not state whether live AWS scanning is verified; scan data currently comes from a moto mock account.
