from collectors.aws_collector import (
    check_s3_encryption_at_rest,
    check_ebs_encryption,
)
from models.schemas import CheckStatus


def test_day4_s3_encryption_against_mock_aws(
    mock_aws_environment,
):
    """
    Day 4 integration test.

    Verify s3_encryption_at_rest against a Moto-backed
    mock AWS account containing both compliant and
    non-compliant buckets.
    """

    encrypted_bucket = (
        mock_aws_environment.create_s3_bucket(
            "governx-day4-encrypted",
            encrypted=True,
        )
    )

    unencrypted_bucket = (
        mock_aws_environment.create_s3_bucket(
            "governx-day4-unencrypted",
            encrypted=False,
        )
    )

    results = check_s3_encryption_at_rest()

    result_by_bucket = {
        result.resource_id: result
        for result in results
    }

    assert (
        result_by_bucket[encrypted_bucket].status
        == CheckStatus.PASS
    )

    assert (
        result_by_bucket[unencrypted_bucket].status
        == CheckStatus.FAIL
    )

def test_day4_ebs_encryption_against_mock_aws(
    mock_aws_environment,
):
    """
    Day 4 integration test.

    Verify ebs_encryption against a Moto-backed
    mock AWS account containing both encrypted
    and unencrypted EBS volumes.
    """

    encrypted_volume = (
        mock_aws_environment.create_ebs_volume(
            encrypted=True
        )
    )

    unencrypted_volume = (
        mock_aws_environment.create_ebs_volume(
            encrypted=False
        )
    )

    results = check_ebs_encryption()

    result_by_volume = {
        result.resource_id: result
        for result in results
    }

    assert (
        result_by_volume[encrypted_volume].status
        == CheckStatus.PASS
    )

    assert (
        result_by_volume[unencrypted_volume].status
        == CheckStatus.FAIL
    )