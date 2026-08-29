"""
Smoke tests for the Week 1 scaffold — no real AWS calls, just proves
the module structure imports cleanly and the check registry populates.
Run with: pytest tests/test_scaffold.py
"""

from collectors.aws_collector import CHECK_REGISTRY
from mappings.csf_mappings import CSF_MAPPINGS
from collectors.aws_collector import check_s3_encryption_at_rest
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
