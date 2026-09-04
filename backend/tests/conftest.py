import pytest
from unittest.mock import patch

from mock_aws import MockAWSEnvironment


@pytest.fixture
def mock_aws_environment():
    with MockAWSEnvironment() as environment:
        # Remove Moto's automatically-created default VPC.
        for vpc in environment.ec2.describe_vpcs()["Vpcs"]:
            if vpc.get("IsDefault"):
                try:
                    environment.ec2.delete_vpc(VpcId=vpc["VpcId"])
                except Exception:
                    pass

        with patch("collectors.aws_collector.get_client") as mock_get_client:
            mock_get_client.side_effect = {
                "ec2": environment.ec2,
                "cloudtrail": environment.cloudtrail,
            }.get
            yield environment
