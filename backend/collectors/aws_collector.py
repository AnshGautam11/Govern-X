"""
AWS configuration collector.

Pattern: each check is a small function registered in CHECK_REGISTRY.
`run_all_checks()` runs every registered check and returns a flat list
of CheckResult. Keep each check function focused on ONE control —
this keeps the CSF mapping table (mappings/csf_mappings.py) clean,
since it maps 1 check_id -> 1 subcategory.

Scope for Week 1: implement the 12 checks agreed in the project scope
doc. Two are implemented below as a reference pattern — copy the shape
for the remaining ones. Do not expand past the agreed 12 without
updating docs/architecture.md first (see the scope-creep note from
project planning).
"""

from botocore.exceptions import ClientError

from integrations.aws.client import get_client
from models.schemas import CheckResult, CheckStatus, Severity

CHECK_REGISTRY: dict[str, callable] = {}


def register_check(check_id: str):
    """Decorator to add a function to the check registry under check_id."""

    def wrapper(func):
        CHECK_REGISTRY[check_id] = func
        return func

    return wrapper


@register_check("s3_public_access_block")
def check_s3_public_access_block() -> list[CheckResult]:
    """PR.DS-01 — S3 buckets should have public access blocked."""
    s3 = get_client("s3")
    results: list[CheckResult] = []

    buckets = s3.list_buckets().get("Buckets", [])
    for bucket in buckets:
        name = bucket["Name"]
        try:
            config = s3.get_public_access_block(Bucket=name)
            block_config = config["PublicAccessBlockConfiguration"]
            is_blocked = all(block_config.values())
            results.append(
                CheckResult(
                    check_id="s3_public_access_block",
                    resource_id=name,
                    status=CheckStatus.PASS if is_blocked else CheckStatus.FAIL,
                    severity=Severity.HIGH,
                    detail=(
                        f"Public access block {'fully enabled' if is_blocked else 'NOT fully enabled'} on {name}"
                    ),
                )
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchPublicAccessBlockConfiguration":
                results.append(
                    CheckResult(
                        check_id="s3_public_access_block",
                        resource_id=name,
                        status=CheckStatus.FAIL,
                        severity=Severity.HIGH,
                        detail=f"No public access block configuration found on {name}",
                    )
                )
            else:
                results.append(
                    CheckResult(
                        check_id="s3_public_access_block",
                        resource_id=name,
                        status=CheckStatus.ERROR,
                        severity=Severity.HIGH,
                        detail=f"Could not evaluate {name}: {e.response['Error']['Message']}",
                    )
                )
    return results


@register_check("iam_user_mfa")
def check_iam_user_mfa() -> list[CheckResult]:
    """PR.AC-07 — IAM users with console access should have MFA enabled."""
    iam = get_client("iam")
    results: list[CheckResult] = []

    paginator = iam.get_paginator("list_users")
    for page in paginator.paginate():
        for user in page["Users"]:
            username = user["UserName"]
            mfa_devices = iam.list_mfa_devices(UserName=username)["MFADevices"]
            has_mfa = len(mfa_devices) > 0
            results.append(
                CheckResult(
                    check_id="iam_user_mfa",
                    resource_id=username,
                    status=CheckStatus.PASS if has_mfa else CheckStatus.FAIL,
                    severity=Severity.CRITICAL,
                    detail=f"MFA {'enabled' if has_mfa else 'NOT enabled'} for user {username}",
                )
            )
    return results

@register_check("s3_encryption_at_rest")
def check_s3_encryption_at_rest() -> list[CheckResult]:
    """PR.DS-01 — S3 buckets should have encryption at rest enabled."""
    s3 = get_client("s3")
    results: list[CheckResult] = []

    buckets = s3.list_buckets().get("Buckets", [])

    for bucket in buckets:
        name = bucket["Name"]

        try:
            encryption = s3.get_bucket_encryption(Bucket=name)

            rules = encryption.get(
                "ServerSideEncryptionConfiguration",
                {}
            ).get("Rules", [])

            has_encryption = len(rules) > 0

            results.append(
                CheckResult(
                    check_id="s3_encryption_at_rest",
                    resource_id=name,
                    status=(
                        CheckStatus.PASS
                        if has_encryption
                        else CheckStatus.FAIL
                    ),
                    severity=Severity.HIGH,
                    detail=(
                        f"Encryption at rest is "
                        f"{'enabled' if has_encryption else 'NOT enabled'} "
                        f"for bucket {name}"
                    ),
                )
            )

        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code in (
                "ServerSideEncryptionConfigurationNotFoundError",
                "NoSuchBucket",
            ):
                results.append(
                    CheckResult(
                        check_id="s3_encryption_at_rest",
                        resource_id=name,
                        status=CheckStatus.FAIL,
                        severity=Severity.HIGH,
                        detail=(
                            f"Encryption at rest is NOT enabled "
                            f"for bucket {name}"
                        ),
                    )
                )
            else:
                results.append(
                    CheckResult(
                        check_id="s3_encryption_at_rest",
                        resource_id=name,
                        status=CheckStatus.ERROR,
                        severity=Severity.HIGH,
                        detail=(
                            f"Could not evaluate encryption for "
                            f"{name}: "
                            f"{e.response['Error']['Message']}"
                        ),
                    )
                )

    return results


@register_check("iam_access_key_age")
def check_iam_access_key_age(max_age_days: int = 90) -> list[CheckResult]:
    """PR.AA-01 - IAM access keys should be rotated within 90 days."""
    from datetime import datetime, timezone

    iam = get_client("iam")
    results: list[CheckResult] = []

    paginator = iam.get_paginator("list_users")
    for page in paginator.paginate():
        for user in page["Users"]:
            username = user["UserName"]
            keys = iam.list_access_keys(UserName=username)["AccessKeyMetadata"]

            if not keys:
                continue

            for key in keys:
                key_id = key["AccessKeyId"]
                created = key["CreateDate"]
                age_days = (datetime.now(timezone.utc) - created).days
                is_old = age_days > max_age_days

                results.append(
                    CheckResult(
                        check_id="iam_access_key_age",
                        resource_id=f"{username}/{key_id}",
                        status=CheckStatus.FAIL if is_old else CheckStatus.PASS,
                        severity=Severity.MEDIUM,
                        detail=(
                            f"Access key {key_id} for user {username} is {age_days} days old "
                            f"({'exceeds' if is_old else 'within'} the {max_age_days}-day rotation limit)"
                        ),
                    )
                )
    return results
 
# --- Remaining Week 1 scope checks (stubs — implement following the pattern above) ---
#
# @register_check("s3_encryption_at_rest")           -> PR.DS-01
# @register_check("iam_root_mfa")                     -> PR.AC-07
# @register_check("security_group_open_ingress")      -> PR.AC-04 / PR.IR-01
# @register_check("iam_policy_wildcard_admin")         -> PR.AC-04
# @register_check("ebs_encryption")                    -> PR.DS-01
# @register_check("rds_public_accessibility")          -> PR.AC-04
# @register_check("cloudtrail_enabled")                -> DE.CM-01
# @register_check("iam_password_policy")               -> PR.AC-01
# @register_check("iam_access_key_age")                -> PR.AC-01
# @register_check("vpc_flow_logs_enabled")             -> DE.CM-01


@register_check("ebs_encryption")
def check_ebs_encryption() -> list[CheckResult]:
    """PR.DS-01 — EBS volumes should have encryption at rest enabled."""
    ec2 = get_client("ec2")
    results: list[CheckResult] = []

    try:
        volumes = ec2.describe_volumes().get("Volumes", [])

        for volume in volumes:
            volume_id = volume["VolumeId"]
            is_encrypted = volume.get("Encrypted", False)

            results.append(
                CheckResult(
                    check_id="ebs_encryption",
                    resource_id=volume_id,
                    status=(
                        CheckStatus.PASS
                        if is_encrypted
                        else CheckStatus.FAIL
                    ),
                    severity=Severity.HIGH,
                    detail=(
                        f"EBS encryption is "
                        f"{'enabled' if is_encrypted else 'NOT enabled'} "
                        f"for volume {volume_id}"
                    ),
                )
            )

    except ClientError as e:
        results.append(
            CheckResult(
                check_id="ebs_encryption",
                resource_id="unknown",
                status=CheckStatus.ERROR,
                severity=Severity.HIGH,
                detail=(
                    f"Could not evaluate EBS encryption: "
                    f"{e.response['Error']['Message']}"
                ),
            )
        )

    return results


@register_check("iam_root_mfa")
def check_iam_root_mfa() -> list[CheckResult]:
    """PR.AA-03 — the root account should have MFA enabled."""
    iam = get_client("iam")

    try:
        summary = iam.get_account_summary()["SummaryMap"]
        has_mfa = summary.get("AccountMFAEnabled", 0) == 1

        return [
            CheckResult(
                check_id="iam_root_mfa",
                resource_id="root-account",
                status=CheckStatus.PASS if has_mfa else CheckStatus.FAIL,
                severity=Severity.CRITICAL,
                detail=(
                    f"Root account MFA is "
                    f"{'enabled' if has_mfa else 'NOT enabled'}"
                ),
            )
        ]

    except ClientError as e:
        return [
            CheckResult(
                check_id="iam_root_mfa",
                resource_id="root-account",
                status=CheckStatus.ERROR,
                severity=Severity.CRITICAL,
                detail=(
                    f"Could not evaluate root MFA status: "
                    f"{e.response['Error']['Message']}"
                ),
            )
        ]


@register_check("iam_password_policy")
def check_iam_password_policy(min_length: int = 14) -> list[CheckResult]:
    """PR.AA-01 — account should enforce a strong IAM password policy."""
    iam = get_client("iam")

    try:
        policy = iam.get_account_password_policy()["PasswordPolicy"]

        length_ok = policy.get("MinimumPasswordLength", 0) >= min_length
        requires_symbols = policy.get("RequireSymbols", False)
        requires_numbers = policy.get("RequireNumbers", False)
        is_strong = length_ok and requires_symbols and requires_numbers

        return [
            CheckResult(
                check_id="iam_password_policy",
                resource_id="account-password-policy",
                status=CheckStatus.PASS if is_strong else CheckStatus.FAIL,
                severity=Severity.MEDIUM,
                detail=(
                    f"Password policy "
                    f"{'meets' if is_strong else 'does NOT meet'} "
                    f"minimum requirements (min length {min_length}, "
                    f"symbols required, numbers required)"
                ),
            )
        ]

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchEntity":
            return [
                CheckResult(
                    check_id="iam_password_policy",
                    resource_id="account-password-policy",
                    status=CheckStatus.FAIL,
                    severity=Severity.MEDIUM,
                    detail="No account password policy is configured",
                )
            ]
        return [
            CheckResult(
                check_id="iam_password_policy",
                resource_id="account-password-policy",
                status=CheckStatus.ERROR,
                severity=Severity.MEDIUM,
                detail=(
                    f"Could not evaluate password policy: "
                    f"{e.response['Error']['Message']}"
                ),
            )
        ]


def run_all_checks() -> list[CheckResult]:
    """Run every registered check and return a flat list of results."""
    all_results: list[CheckResult] = []
    for check_id, check_fn in CHECK_REGISTRY.items():
        try:
            all_results.extend(check_fn())
        except ClientError as e:
            all_results.append(
                CheckResult(
                    check_id=check_id,
                    resource_id="unknown",
                    status=CheckStatus.ERROR,
                    severity=Severity.LOW,
                    detail=f"Check failed to run: {e.response['Error']['Message']}",
                )
            )
    return all_results