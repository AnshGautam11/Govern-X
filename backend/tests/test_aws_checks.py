from unittest.mock import MagicMock, patch

from collectors.aws_collector import (
    check_cloudtrail_enabled,
    check_vpc_flow_logs_enabled,
)
from models.schemas import CheckStatus


def test_cloudtrail_enabled(mock_aws_environment):
    mock_aws_environment.create_cloudtrail_trail()

    result = check_cloudtrail_enabled()[0]

    assert result.status == CheckStatus.PASS
    assert result.detail == "CloudTrail is enabled"


def test_cloudtrail_missing_fails(mock_aws_environment):
    result = check_cloudtrail_enabled()[0]

    assert result.status == CheckStatus.FAIL
    assert result.detail == "CloudTrail is not enabled"


def test_cloudtrail_empty_response_fails_gracefully():
    mock_cloudtrail = MagicMock()
    mock_cloudtrail.list_trails.return_value = {}

    with patch("collectors.aws_collector.get_client", return_value=mock_cloudtrail):
        result = check_cloudtrail_enabled()[0]

    assert result.status == CheckStatus.FAIL


def test_vpc_flow_logs_enabled(mock_aws_environment):
    vpc_id = mock_aws_environment.create_vpc()
    mock_aws_environment.create_vpc_flow_logs(vpc_id)

    result = check_vpc_flow_logs_enabled()[0]

    assert result.status == CheckStatus.PASS
    assert result.detail == "VPC Flow Logs are enabled"


def test_vpc_flow_logs_missing_fails(mock_aws_environment):
    mock_aws_environment.create_vpc()

    result = check_vpc_flow_logs_enabled()[0]

    assert result.status == CheckStatus.FAIL


def test_vpc_flow_logs_requires_logs_for_multiple_vpcs(mock_aws_environment):
    first_vpc = mock_aws_environment.create_vpc("10.0.0.0/16")
    mock_aws_environment.create_vpc_flow_logs(first_vpc)
    mock_aws_environment.create_vpc("10.1.0.0/16")

    result = check_vpc_flow_logs_enabled()[0]

    assert result.status == CheckStatus.FAIL


def test_vpc_flow_logs_empty_response_fails_gracefully():
    mock_ec2 = MagicMock()
    mock_ec2.describe_vpcs.return_value = {}

    with patch("collectors.aws_collector.get_client", return_value=mock_ec2):
        result = check_vpc_flow_logs_enabled()[0]

    assert result.status == CheckStatus.FAIL