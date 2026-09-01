import pytest

from mock_aws import MockAWSEnvironment


@pytest.fixture
def mock_aws_environment():
    """Provide an isolated moto account for boto3 integration tests."""
    with MockAWSEnvironment() as environment:
        yield environment