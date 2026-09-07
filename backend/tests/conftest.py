import pytest
from unittest.mock import patch

from mock_aws import MockAWSEnvironment


@pytest.fixture
def mock_aws_environment():
    """Provide an isolated Moto AWS environment."""
    with MockAWSEnvironment() as environment:
        with patch("collectors.aws_collector.get_client") as mock_get_client:
            mock_get_client.side_effect = {
                "ec2": environment.ec2,
                "s3": environment.s3,
                "iam": environment.iam,
                "cloudtrail": environment.cloudtrail,
            }.get

            yield environment
