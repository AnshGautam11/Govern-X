"""
Day 4 integration tests for iam_root_mfa and iam_password_policy —
run against the moto-backed mock AWS account, not just unit mocks.
"""

from collectors.aws_collector import (
    check_iam_root_mfa,
    check_iam_password_policy,
)
from models.schemas import CheckStatus


def test_day4_iam_root_mfa_against_mock_aws(mock_aws_environment):
    """
    moto cannot simulate root MFA being enabled (AccountMFAEnabled
    is always 0 in the mock backend), so this only proves the FAIL
    path against a live mock account. The PASS path is covered by
    the MagicMock-based unit test in test_scaffold.py instead.
    """
    results = check_iam_root_mfa()

    assert len(results) == 1
    assert results[0].status == CheckStatus.FAIL


def test_day4_iam_password_policy_fail_when_unset(mock_aws_environment):
    """No password policy configured -> should fail."""
    results = check_iam_password_policy()

    assert len(results) == 1
    assert results[0].status == CheckStatus.FAIL


def test_day4_iam_password_policy_pass_when_strong(mock_aws_environment):
    """Strong policy configured -> should pass."""
    mock_aws_environment.set_account_password_policy(
        min_length=14,
        require_symbols=True,
        require_numbers=True,
    )

    results = check_iam_password_policy()

    assert len(results) == 1
    assert results[0].status == CheckStatus.PASS


def test_day4_iam_password_policy_fail_when_weak(mock_aws_environment):
    """Policy exists but too weak (short, no symbols) -> should fail."""
    mock_aws_environment.set_account_password_policy(
        min_length=6,
        require_symbols=False,
        require_numbers=False,
    )

    results = check_iam_password_policy()

    assert len(results) == 1
    assert results[0].status == CheckStatus.FAIL