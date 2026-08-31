"""
Smoke tests for the Week 1 scaffold — no real AWS calls, just proves
the module structure imports cleanly and the check registry populates.
Run with: pytest tests/test_scaffold.py
"""

from collectors.aws_collector import CHECK_REGISTRY
from mappings.csf_mappings import CSF_MAPPINGS
from collectors.aws_collector import (
    check_s3_encryption_at_rest,
    check_ebs_encryption,
    check_iam_root_mfa,
    check_iam_password_policy,
)
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError


def test_check_registry_populated():
    assert "s3_public_access_block" in CHECK_REGISTRY
    assert "iam_user_mfa" in CHECK_REGISTRY


def test_every_registered_check_has_a_mapping():
    """Catches the case where someone adds a check but forgets the CSF mapping row."""
    for check_id in CHECK_REGISTRY:
        assert check_id in CSF_MAPPINGS, f"{check_id} is missing a CSFMapping row"


def test_s3_encryption_at_rest_pass():
    """S3 bucket with encryption configuration should pass."""

    mock_s3 = MagicMock()

    mock_s3.list_buckets.return_value = {
        "Buckets": [
            {"Name": "encrypted-bucket"}
        ]
    }

    mock_s3.get_bucket_encryption.return_value = {
        "ServerSideEncryptionConfiguration": {
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        }
    }

    with patch(
        "collectors.aws_collector.get_client",
        return_value=mock_s3
    ):
        results = check_s3_encryption_at_rest()

    assert len(results) == 1
    assert results[0].check_id == "s3_encryption_at_rest"
    assert results[0].resource_id == "encrypted-bucket"
    assert results[0].status.value == "pass"


def test_s3_encryption_at_rest_fail():
    """S3 bucket without encryption should fail."""

    mock_s3 = MagicMock()

    mock_s3.list_buckets.return_value = {
        "Buckets": [
            {"Name": "unencrypted-bucket"}
        ]
    }

    error_response = {
        "Error": {
            "Code": "ServerSideEncryptionConfigurationNotFoundError",
            "Message": "The bucket has no encryption configuration."
        }
    }

    mock_s3.get_bucket_encryption.side_effect = ClientError(
        error_response,
        "GetBucketEncryption"
    )

    with patch(
        "collectors.aws_collector.get_client",
        return_value=mock_s3
    ):
        results = check_s3_encryption_at_rest()

    assert len(results) == 1
    assert results[0].check_id == "s3_encryption_at_rest"
    assert results[0].resource_id == "unencrypted-bucket"
    assert results[0].status.value == "fail"

def test_ebs_encryption_pass():
    """EBS volume with encryption enabled should pass."""

    mock_ec2 = MagicMock()

    mock_ec2.describe_volumes.return_value = {
        "Volumes": [
            {
                "VolumeId": "vol-encrypted",
                "Encrypted": True,
            }
        ]
    }

    with patch(
        "collectors.aws_collector.get_client",
        return_value=mock_ec2
    ):
        results = check_ebs_encryption()

    assert len(results) == 1
    assert results[0].check_id == "ebs_encryption"
    assert results[0].resource_id == "vol-encrypted"
    assert results[0].status.value == "pass"


def test_ebs_encryption_fail():
    """EBS volume without encryption should fail."""

    mock_ec2 = MagicMock()

    mock_ec2.describe_volumes.return_value = {
        "Volumes": [
            {
                "VolumeId": "vol-unencrypted",
                "Encrypted": False,
            }
        ]
    }

    with patch(
        "collectors.aws_collector.get_client",
        return_value=mock_ec2
    ):
        results = check_ebs_encryption()

    assert len(results) == 1
    assert results[0].check_id == "ebs_encryption"
    assert results[0].resource_id == "vol-unencrypted"
    assert results[0].status.value == "fail"


def test_iam_root_mfa_pass():
    mock_iam = MagicMock()
    mock_iam.get_account_summary.return_value = {
        "SummaryMap": {"AccountMFAEnabled": 1}
    }

    with patch("collectors.aws_collector.get_client", return_value=mock_iam):
        results = check_iam_root_mfa()

    assert results[0].status.value == "pass"


def test_iam_root_mfa_fail():
    mock_iam = MagicMock()
    mock_iam.get_account_summary.return_value = {
        "SummaryMap": {"AccountMFAEnabled": 0}
    }

    with patch("collectors.aws_collector.get_client", return_value=mock_iam):
        results = check_iam_root_mfa()

    assert results[0].status.value == "fail"


def test_iam_password_policy_pass():
    mock_iam = MagicMock()
    mock_iam.get_account_password_policy.return_value = {
        "PasswordPolicy": {
            "MinimumPasswordLength": 14,
            "RequireSymbols": True,
            "RequireNumbers": True,
        }
    }

    with patch("collectors.aws_collector.get_client", return_value=mock_iam):
        results = check_iam_password_policy()

    assert results[0].status.value == "pass"


def test_iam_password_policy_fail_no_policy():
    mock_iam = MagicMock()
    mock_iam.get_account_password_policy.side_effect = ClientError(
        {"Error": {"Code": "NoSuchEntity", "Message": "No policy set"}},
        "GetAccountPasswordPolicy",
    )

    with patch("collectors.aws_collector.get_client", return_value=mock_iam):
        results = check_iam_password_policy()

    assert results[0].status.value == "fail"