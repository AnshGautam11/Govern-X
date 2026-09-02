from models.schemas import CSFMapping


CSF_MAPPINGS: dict[str, CSFMapping] = {

    "s3_public_access_block": CSFMapping(
        check_id="s3_public_access_block",
        csf_function="Protect",
        csf_subcategory="PR.DS-01",
        justification="S3 public access blocking helps prevent unauthorized access to stored data.",
    ),

    "iam_user_mfa": CSFMapping(
        check_id="iam_user_mfa",
        csf_function="Protect",
        csf_subcategory="PR.AA-03",
        justification="MFA strengthens authentication and reduces the risk of unauthorized access.",
    ),

    "s3_encryption_at_rest": CSFMapping(
        check_id="s3_encryption_at_rest",
        csf_function="Protect",
        csf_subcategory="PR.DS-01",
        justification="Encryption at rest protects stored data from unauthorized disclosure.",
    ),

    "iam_access_key_age": CSFMapping(
        check_id="iam_access_key_age",
        csf_function="Protect",
        csf_subcategory="PR.AA-01",
        justification="Regular access key rotation reduces the risk window associated with compromised credentials.",
    ),

    "iam_policy_wildcard_admin": CSFMapping(
        check_id="iam_policy_wildcard_admin",
        csf_function="Protect",
        csf_subcategory="PR.AA-05",
        justification="Wildcard admin policies violate least privilege by granting unrestricted access to all actions and resources.",
    ),

    "security_group_open_ingress": CSFMapping(
        check_id="security_group_open_ingress",
        csf_function="Protect",
        csf_subcategory="PR.IR-01",
        justification="Restricting open security-group ingress helps protect networks and environments from unauthorized logical access.",
    ),

    "ebs_encryption": CSFMapping(
        check_id="ebs_encryption",
        csf_function="Protect",
        csf_subcategory="PR.DS-01",
        justification="EBS encryption protects stored data from unauthorized disclosure.",
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
        justification="A strong, enforced password policy supports identity and credential management for IAM users.",
    ),

    "rds_public_accessibility": CSFMapping(
        check_id="rds_public_accessibility",
        csf_function="Protect",
        csf_subcategory="PR.IR-01",
        justification="Restricting public accessibility of RDS databases helps prevent unauthorized access to data resources.",
    ),

    "cloudtrail_enabled": CSFMapping(
        check_id="cloudtrail_enabled",
        csf_function="Detect",
        csf_subcategory="DE.CM-03",
        justification="CloudTrail monitoring helps detect and record personnel activity and technology usage through AWS API activity.",
    ),

    "vpc_flow_logs_enabled": CSFMapping(
    check_id="vpc_flow_logs_enabled",
    csf_function="Detect",
    csf_subcategory="DE.CM-01",
    justification=(
        "VPC Flow Logs provide network traffic visibility and"
        "support monitoring of networks and network services."
    ),
),
    ),
}


def get_mapping(check_id: str) -> CSFMapping | None:
    return CSF_MAPPINGS.get(check_id)
