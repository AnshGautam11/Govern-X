
import pytest

from mock_aws.account import MockAWSAccount, MockIAMUser, SecurityAuditPolicy


def test_mock_aws_account_creates_readonly_audit_user():
    account = MockAWSAccount("123456789012")
    user = account.create_iam_user("audit-readonly")

    assert user.name == "audit-readonly"
    assert user.is_read_only is True
    assert user.attached_policies == [SecurityAuditPolicy.ARN]
    assert account.find_user("audit-readonly") == user


def test_security_audit_policy_is_read_only():
    policy = SecurityAuditPolicy()

    assert policy.name == "SecurityAudit"
    assert "iam:Get*" in policy.allowed_actions
    assert "ec2:Describe*" in policy.allowed_actions
    assert "s3:GetObject" in policy.allowed_actions

    assert "iam:CreateUser" in policy.blocked_actions
    assert "iam:DeleteUser" in policy.blocked_actions
    assert "ec2:AuthorizeSecurityGroupIngress" in policy.blocked_actions


def test_verify_read_only_access_for_user():
    account = MockAWSAccount("123456789012")
    user = account.create_iam_user("audit-readonly")

    result = account.verify_read_only_access(user)

    assert result["user"] == "audit-readonly"
    assert result["read_only"] is True
    assert result["allowed_actions"][0] == "iam:Get*"
    assert result["blocked_actions"]


def test_non_readonly_user_is_detected_as_failure():
    account = MockAWSAccount("123456789012")

    user = MockIAMUser(name="unsafe-user")

    account.users[user.name] = user

    result = account.verify_read_only_access(user)

    assert result["read_only"] is False
    assert result["user"] == "unsafe-user"


def test_unknown_user_is_rejected():
    account = MockAWSAccount("123456789012")

    with pytest.raises(KeyError, match="User not found"):
        account.verify_read_only_access("missing-user")


def test_readonly_user_cannot_have_write_actions_in_allowed_list():
    account = MockAWSAccount("123456789012")
    user = account.create_iam_user("audit-readonly")

    result = account.verify_read_only_access(user)

    forbidden_actions = {
        "iam:CreateUser",
        "iam:DeleteUser",
        "iam:AttachUserPolicy",
        "ec2:AuthorizeSecurityGroupIngress",
        "ec2:RevokeSecurityGroupIngress",
        "s3:PutObject",
        "s3:DeleteObject",
    }

    assert not forbidden_actions.intersection(result["allowed_actions"])
