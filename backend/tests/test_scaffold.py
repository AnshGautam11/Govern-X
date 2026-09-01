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
from models.schemas import CheckStatus

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
def test_security_group_open_ingress_pass():
    """Security group without unrestricted ingress should pass."""
    from collectors.aws_collector import check_security_group_open_ingress

    mock_ec2 = MagicMock()

    mock_ec2.describe_security_groups.return_value = {
        "SecurityGroups": [
            {
                "GroupId": "sg-123",
                "GroupName": "restricted-sg",
                "IpPermissions": [],
            }
        ]
    }

    with patch("collectors.aws_collector.get_client", return_value=mock_ec2):
        results = check_security_group_open_ingress()

    assert len(results) == 1
    assert results[0].status == CheckStatus.PASS


def test_security_group_open_ingress_fail():
    """Security group allowing 0.0.0.0/0 should fail."""
    from collectors.aws_collector import check_security_group_open_ingress

    mock_ec2 = MagicMock()

    mock_ec2.describe_security_groups.return_value = {
        "SecurityGroups": [
            {
                "GroupId": "sg-456",
                "GroupName": "open-sg",
                "IpPermissions": [
                    {
                        "IpRanges": [
                            {"CidrIp": "0.0.0.0/0"}
                        ],
                        "Ipv6Ranges": [],
                    }
                ],
            }
        ]
    }

    with patch("collectors.aws_collector.get_client", return_value=mock_ec2):
        results = check_security_group_open_ingress()

    assert len(results) == 1
    assert results[0].status == CheckStatus.FAIL
def test_rds_public_accessibility_pass():
    """RDS instance that is not publicly accessible should pass."""
    from collectors.aws_collector import check_rds_public_accessibility

    mock_rds = MagicMock()

    mock_rds.get_paginator.return_value.paginate.return_value = [
        {
            "DBInstances": [
                {
                    "DBInstanceIdentifier": "private-db",
                    "PubliclyAccessible": False,
                }
            ]
        }
    ]

    with patch("collectors.aws_collector.get_client", return_value=mock_rds):
        results = check_rds_public_accessibility()

    assert len(results) == 1
    assert results[0].status == CheckStatus.PASS


def test_rds_public_accessibility_fail():
    """RDS instance that is publicly accessible should fail."""
    from collectors.aws_collector import check_rds_public_accessibility

    mock_rds = MagicMock()

    mock_rds.get_paginator.return_value.paginate.return_value = [
        {
            "DBInstances": [
                {
                    "DBInstanceIdentifier": "public-db",
                    "PubliclyAccessible": True,
                }
            ]
        }
    ]

    with patch("collectors.aws_collector.get_client", return_value=mock_rds):
        results = check_rds_public_accessibility()

    assert len(results) == 1
    assert results[0].status == CheckStatus.FAIL
def test_vpc_flow_logs_enabled_pass():
    """Active VPC Flow Logs should pass."""
    from collectors.aws_collector import check_vpc_flow_logs_enabled

    mock_ec2 = MagicMock()

    mock_ec2.describe_flow_logs.return_value = {
        "FlowLogs": [
            {
                "FlowLogId": "fl-123",
                "ResourceId": "vpc-123",
                "FlowLogStatus": "ACTIVE",
            }
        ]
    }

    with patch("collectors.aws_collector.get_client", return_value=mock_ec2):
        results = check_vpc_flow_logs_enabled()

    assert len(results) == 1
    assert results[0].check_id == "vpc_flow_logs_enabled"
    assert results[0].resource_id == "fl-123"
    assert results[0].status == CheckStatus.PASS


def test_vpc_flow_logs_enabled_fail():
    """Missing active VPC Flow Logs should fail."""
    from collectors.aws_collector import check_vpc_flow_logs_enabled

    mock_ec2 = MagicMock()

    mock_ec2.describe_flow_logs.return_value = {
        "FlowLogs": []
    }

    with patch("collectors.aws_collector.get_client", return_value=mock_ec2):
        results = check_vpc_flow_logs_enabled()

    assert len(results) == 1
    assert results[0].check_id == "vpc_flow_logs_enabled"
    assert results[0].status == CheckStatus.FAIL
def test_vpc_flow_logs_enabled_pass():
    """VPC with active flow logs should pass."""
    from collectors.aws_collector import check_vpc_flow_logs_enabled

    mock_ec2 = MagicMock()

    mock_ec2.describe_vpcs.return_value = {
        "Vpcs": [
            {
                "VpcId": "vpc-123"
            }
        ]
    }

    mock_ec2.describe_flow_logs.return_value = {
        "FlowLogs": [
            {
                "FlowLogId": "fl-123",
                "ResourceId": "vpc-123",
                "FlowLogStatus": "ACTIVE"
            }
        ]
    }

    with patch("collectors.aws_collector.get_client", return_value=mock_ec2):
        results = check_vpc_flow_logs_enabled()

    assert len(results) == 1
    assert results[0].check_id == "vpc_flow_logs_enabled"
    assert results[0].resource_id == "vpc-123"
    assert results[0].status == CheckStatus.PASS


def test_vpc_flow_logs_enabled_fail():
    """VPC without active flow logs should fail."""
    from collectors.aws_collector import check_vpc_flow_logs_enabled

    mock_ec2 = MagicMock()

    mock_ec2.describe_vpcs.return_value = {
        "Vpcs": [
            {
                "VpcId": "vpc-456"
            }
        ]
    }

    mock_ec2.describe_flow_logs.return_value = {
        "FlowLogs": []
    }

    with patch("collectors.aws_collector.get_client", return_value=mock_ec2):
        results = check_vpc_flow_logs_enabled()

    assert len(results) == 1
    assert results[0].check_id == "vpc_flow_logs_enabled"
    assert results[0].resource_id == "vpc-456"
    assert results[0].status == CheckStatus.FAIL
