from collectors.aws_collector import (
    check_s3_encryption_at_rest,
    check_ebs_encryption,
)
from models.schemas import CheckStatus
from unittest.mock import MagicMock, patch


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


def test_day5_s3_encryption_result_details(
    mock_aws_environment,
):
    """
    Day 5 review test.

    Confirm the finalized S3 check reports the correct
    resource ID, severity, and human-readable details.
    """

    bucket_name = mock_aws_environment.create_s3_bucket(
        "governx-day5-encrypted",
        encrypted=True,
    )

    results = check_s3_encryption_at_rest()

    result = next(
        item
        for item in results
        if item.resource_id == bucket_name
    )

    assert result.check_id == "s3_encryption_at_rest"
    assert result.status == CheckStatus.PASS
    assert "enabled" in result.detail
    assert bucket_name in result.detail


def test_day5_ebs_encryption_result_details(
    mock_aws_environment,
):
    """
    Day 5 review test.

    Confirm the finalized EBS check reports the correct
    resource ID and human-readable result.
    """

    volume_id = mock_aws_environment.create_ebs_volume(
        encrypted=True,
    )

    results = check_ebs_encryption()

    result = next(
        item
        for item in results
        if item.resource_id == volume_id
    )

    assert result.check_id == "ebs_encryption"
    assert result.status == CheckStatus.PASS
    assert "enabled" in result.detail
    assert volume_id in result.detail


def test_day5_ebs_encryption_checks_all_pages():
    """
    Day 5 review test.

    Ensure EBS encryption auditing processes all pages
    returned by the AWS describe_volumes paginator.
    """

    mock_ec2 = MagicMock()
    mock_paginator = MagicMock()

    mock_ec2.get_paginator.return_value = mock_paginator

    mock_paginator.paginate.return_value = [
        {
            "Volumes": [
                {
                    "VolumeId": "vol-page-one",
                    "Encrypted": True,
                }
            ]
        },
        {
            "Volumes": [
                {
                    "VolumeId": "vol-page-two",
                    "Encrypted": False,
                }
            ]
        },
    ]

    with patch(
        "collectors.aws_collector.get_client",
        return_value=mock_ec2,
    ):
        results = check_ebs_encryption()

    result_by_volume = {
        result.resource_id: result
        for result in results
    }

    assert len(results) == 2

    assert (
        result_by_volume["vol-page-one"].status
        == CheckStatus.PASS
    )

    assert (
        result_by_volume["vol-page-two"].status
        == CheckStatus.FAIL
    )

    mock_ec2.get_paginator.assert_called_once_with(
        "describe_volumes"
    )

def test_day6_own_checks_are_registered():
    """
    Day 6 final verification.

    Confirm both Week 1 encryption checks remain registered
    in the shared AWS check registry.
    """
    from collectors.aws_collector import CHECK_REGISTRY

    assert "s3_encryption_at_rest" in CHECK_REGISTRY
    assert "ebs_encryption" in CHECK_REGISTRY


def test_day6_own_checks_have_csf_mappings():
    """
    Day 6 final verification.

    Confirm both encryption checks have their required
    NIST CSF 2.0 PR.DS-01 mappings.
    """
    from mappings.csf_mappings import CSF_MAPPINGS

    s3_mapping = CSF_MAPPINGS["s3_encryption_at_rest"]
    ebs_mapping = CSF_MAPPINGS["ebs_encryption"]

    assert s3_mapping.check_id == "s3_encryption_at_rest"
    assert s3_mapping.csf_function == "Protect"
    assert s3_mapping.csf_subcategory == "PR.DS-01"

    assert ebs_mapping.check_id == "ebs_encryption"
    assert ebs_mapping.csf_function == "Protect"
    assert ebs_mapping.csf_subcategory == "PR.DS-01"