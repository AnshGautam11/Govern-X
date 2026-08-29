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


if __name__ == "__main__":
    account = MockAWSAccount("123456789012")
    user = account.create_iam_user("audit-readonly")
    print(f"Created user: {user.name}")
    print(f"Policies: {user.attached_policies}")
    print(account.verify_read_only_access(user))