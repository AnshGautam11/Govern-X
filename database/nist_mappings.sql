-- Seed data: the 12 checks agreed in the project scope doc.
-- Keep this file in sync with backend/mappings/csf_mappings.py — the
-- Python dict is the source of truth used at runtime; this file seeds
-- the DB for the dashboard/reporting layer to query directly.

INSERT INTO checks (id, description, severity) VALUES
    ('s3_public_access_block', 'S3 buckets must have public access blocked', 'high'),
    ('iam_user_mfa', 'IAM users with console access must have MFA enabled', 'critical'),
    ('s3_encryption_at_rest', 'S3 buckets must have default encryption enabled', 'high'),
    ('iam_root_mfa', 'Root account must have MFA enabled', 'critical'),
    ('security_group_open_ingress', 'Security groups must not allow 0.0.0.0/0 on SSH/RDP', 'critical'),
    ('iam_policy_wildcard_admin', 'IAM policies must not grant *:* admin access', 'critical'),
    ('ebs_encryption', 'EBS volumes must be encrypted', 'high'),
    ('rds_public_accessibility', 'RDS instances must not be publicly accessible', 'critical'),
    ('cloudtrail_enabled', 'CloudTrail must be enabled and multi-region', 'high'),
    ('iam_password_policy', 'IAM password policy must meet minimum strength requirements', 'medium'),
    ('iam_access_key_age', 'IAM access keys must be rotated within 90 days', 'medium'),
    ('vpc_flow_logs_enabled', 'VPC flow logs must be enabled', 'medium');

-- Only s3_public_access_block and iam_user_mfa are implemented as of
-- Week 1 scaffold. Add the corresponding csf_mappings row here as each
-- check is implemented in backend/mappings/csf_mappings.py.

INSERT INTO csf_mappings (check_id, csf_function, csf_subcategory, justification) VALUES
    ('s3_public_access_block', 'Protect', 'PR.DS-01',
     'Public access block directly enforces data-at-rest protection from unauthorized exposure.'),
    ('iam_user_mfa', 'Protect', 'PR.AA-03',
     'MFA is the primary control for the "users, services, and hardware are authenticated" outcome. PR.AC-07 (CSF 1.1) was withdrawn and folded into PR.AA in 2.0.');
