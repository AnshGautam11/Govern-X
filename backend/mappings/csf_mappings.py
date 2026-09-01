"""
The Framework Mapping Matrix.

This is the most interview-defensible artifact in the project: it is
the explicit, auditable link between "what we scan" and "what NIST
CSF 2.0 subcategory it evidences." Keep every entry to ONE check_id
per row and require a real justification — no blank/placeholder rows.

Only the 12 checks in the agreed Week 1 scope belong here. Do not add
a row for a check that isn't implemented in collectors/aws_collector.py.
"""

from models.schemas import CSFMapping

CSF_MAPPINGS: dict[str, CSFMapping] = {
    "s3_public_access_block": CSFMapping(
        check_id="s3_public_access_block",
        csf_function="Protect",
        csf_subcategory="PR.DS-01",
        justification="Public access block directly enforces data-at-rest protection from unauthorized exposure.",
    ),

    "s3_encryption_at_rest": CSFMapping(
        check_id="s3_encryption_at_rest",
        csf_function="Protect",
        csf_subcategory="PR.DS-01",
        justification=(
            "S3 server-side encryption protects stored data from "
            "unauthorized disclosure by encrypting data at rest."
        ),
    ),

    "ebs_encryption": CSFMapping(
        check_id="ebs_encryption",
        csf_function="Protect",
        csf_subcategory="PR.DS-01",
        justification=(
            "EBS encryption protects data stored on EBS volumes "
            "from unauthorized disclosure by encrypting data at rest."
        ),
    ),

    "iam_user_mfa": CSFMapping(
        check_id="iam_user_mfa",
        csf_function="Protect",
        csf_subcategory="PR.AA-03",
        justification="MFA is the primary control for the 'users, services, and hardware are authenticated' outcome. (Note: PR.AC-07 from CSF 1.1 was withdrawn and folded into PR.AA in 2.0.)",
    ),
    "iam_access_key_age": CSFMapping(
        check_id="iam_access_key_age",
        csf_function="Protect",
        csf_subcategory="PR.AA-01",
        justification="Regular access key rotation reduces the risk window if a key is compromised, supporting identity and credential management.",
    ),
       "iam_policy_wildcard_admin": CSFMapping(
        check_id="iam_policy_wildcard_admin",
        csf_function="Protect",
        csf_subcategory="PR.AA-05",
        justification="Wildcard admin policies violate least privilege by granting unrestricted access to all actions and resources.",
    ),

    "iam_root_mfa": CSFMapping(
        check_id="iam_root_mfa",
        csf_function="Protect",
        csf_subcategory="PR.AA-03",
        justification="Root account MFA is the primary control for authenticating the account's highest-privilege identity.",
    ),

    "iam_password_policy": CSFMapping(
        check_id="iam_password_policy",
        csf_function="Protect",
        csf_subcategory="PR.AA-01",
        justification="A strong, enforced password policy supports identity and credential management for all IAM users.",
    ),

    # --- Remaining checks, mapped for when each is implemented in aws_collector.py ---
    # "security_group_open_ingress": PR.IR-01 - "Networks and environments are protected from unauthorized logical access"
    # "iam_policy_wildcard_admin": PR.AA-05 - "Access permissions... incorporate least privilege"
    # "rds_public_accessibility": PR.IR-01
    # "cloudtrail_enabled": DE.CM-03 - "Personnel activity and technology usage are monitored" (API activity monitoring, not network traffic)
    # "vpc_flow_logs_enabled": DE.CM-01 - "Networks and network services are monitored"
    "security_group_open_ingress": CSFMapping(
        check_id="security_group_open_ingress",
        csf_function="Protect",
        csf_subcategory="PR.IR-01",
        justification=(
            "Restricting open security-group ingress helps protect "
            "networks and environments from unauthorized logical access."
        ),
    ),
}


def get_mapping(check_id: str) -> CSFMapping | None:
    return CSF_MAPPINGS.get(check_id)
