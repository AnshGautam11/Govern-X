"""Simple mock AWS account environment for read-only IAM validation.

This intentionally avoids any real AWS network calls and only models the
minimum behavior needed for local testing and demo scenarios.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class SecurityAuditPolicy:
    """Mocked AWS managed policy used for read-only auditing."""

    name = "SecurityAudit"
    ARN = "arn:aws:iam::aws:policy/SecurityAudit"
    allowed_actions = [
        "iam:Get*",
        "ec2:Describe*",
        "s3:GetObject",
        "s3:ListBucket",
        "logs:DescribeLogGroups",
        "config:Describe*",
        "guardduty:List*",
        "cloudtrail:LookupEvents",
    ]
    blocked_actions = [
        "iam:CreateUser",
        "iam:DeleteUser",
        "iam:AttachUserPolicy",
        "ec2:AuthorizeSecurityGroupIngress",
        "ec2:RevokeSecurityGroupIngress",
        "s3:PutObject",
        "s3:DeleteObject",
    ]


@dataclass
class MockIAMUser:
    name: str
    attached_policies: list[str] = field(default_factory=list)

    @property
    def is_read_only(self) -> bool:
        return SecurityAuditPolicy.ARN in self.attached_policies


class MockAWSAccount:
    """Minimal AWS-like account model with IAM user and policy attach support."""

    def __init__(self, account_id: str):
        self.account_id = account_id
        self.users: dict[str, MockIAMUser] = {}
        self.policies: dict[str, Any] = {SecurityAuditPolicy.ARN: SecurityAuditPolicy()}

    def create_iam_user(self, username: str) -> MockIAMUser:
        if username in self.users:
            return self.users[username]

        user = MockIAMUser(name=username)
        self.attach_policy(user, SecurityAuditPolicy.ARN)
        self.users[username] = user
        return user

    def attach_policy(self, user: MockIAMUser, policy_arn: str) -> None:
        if policy_arn not in user.attached_policies:
            user.attached_policies.append(policy_arn)

    def find_user(self, username: str) -> MockIAMUser | None:
        return self.users.get(username)

    def verify_read_only_access(self, user: MockIAMUser | str) -> dict[str, Any]:
        target_user = self.users.get(user) if isinstance(user, str) else user
        if target_user is None:
            raise KeyError("User not found in mock AWS account")

        read_only = target_user.is_read_only
        allowed_actions = list(SecurityAuditPolicy.allowed_actions)
        blocked_actions = list(SecurityAuditPolicy.blocked_actions)

        return {
            "user": target_user.name,
            "read_only": read_only,
            "allowed_actions": allowed_actions,
            "blocked_actions": blocked_actions,
        }


class MockAWSEnvironment:
    """
    Moto-backed AWS environment used for local GovernX integration tests.

    This allows boto3 checks to run against simulated AWS resources
    without requiring real AWS credentials or making network calls.
    """

    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name
        self._mock = None

    def __enter__(self):
        import os
        import boto3
        from moto import mock_aws

        # Fake credentials are required by boto3,
        # but Moto prevents real AWS network calls.
        os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
        os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
        os.environ.setdefault("AWS_SESSION_TOKEN", "testing")
        os.environ.setdefault("AWS_SECURITY_TOKEN", "testing")
        os.environ.setdefault("AWS_DEFAULT_REGION", self.region_name)

        self._mock = mock_aws()
        self._mock.start()

        self.s3 = boto3.client(
            "s3",
            region_name=self.region_name,
        )

        self.ec2 = boto3.client(
            "ec2",
            region_name=self.region_name,
        )

        self.cloudtrail = boto3.client(
            "cloudtrail",
            region_name=self.region_name,
        )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._mock is not None:
            self._mock.stop()

    def create_s3_bucket(
        self,
        name: str,
        encrypted: bool = False,
    ) -> str:
        """Create a mock S3 bucket with optional encryption."""

        self.s3.create_bucket(Bucket=name)

        if encrypted:
            self.s3.put_bucket_encryption(
                Bucket=name,
                ServerSideEncryptionConfiguration={
                    "Rules": [
                        {
                            "ApplyServerSideEncryptionByDefault": {
                                "SSEAlgorithm": "AES256"
                            }
                        }
                    ]
                },
            )

        return name

    def create_ebs_volume(
        self,
        encrypted: bool = False,
    ) -> str:
        """Create a mock EBS volume."""

        response = self.ec2.create_volume(
            AvailabilityZone=f"{self.region_name}a",
            Size=8,
            Encrypted=encrypted,
            VolumeType="gp3",
        )

        return response["VolumeId"]

    def create_cloudtrail_trail(
        self,
        name: str = "governx-audit-trail",
    ) -> str:
        """Create a mock CloudTrail trail."""

        bucket_name = f"{name}-bucket"

        self.s3.create_bucket(
            Bucket=bucket_name
        )

        self.cloudtrail.create_trail(
            Name=name,
            S3BucketName=bucket_name,
        )

        self.cloudtrail.start_logging(
            Name=name
        )

        return name

    def create_vpc(
        self,
        cidr_block: str = "10.0.0.0/16",
    ) -> str:
        """Create a mock VPC."""

        response = self.ec2.create_vpc(
            CidrBlock=cidr_block
        )

        return response["Vpc"]["VpcId"]

    def create_vpc_flow_logs(
        self,
        vpc_id: str,
    ):
        """Create mock VPC flow logs."""

        return self.ec2.create_flow_logs(
            ResourceIds=[vpc_id],
            ResourceType="VPC",
            TrafficType="ALL",
            LogDestinationType="cloud-watch-logs",
            LogGroupName="governx-flow-logs",
            DeliverLogsPermissionArn=(
                "arn:aws:iam::123456789012:"
                "role/flow-log-role"
            ),
        )

if __name__ == "__main__":
    account = MockAWSAccount("123456789012")
    user = account.create_iam_user("audit-readonly")
    print(f"Created user: {user.name}")
    print(f"Policies: {user.attached_policies}")
    print(account.verify_read_only_access(user))