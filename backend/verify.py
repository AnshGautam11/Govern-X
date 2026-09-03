"""
Manual verification for GovernX S3 and EBS encryption checks.

Runs:
1. s3_encryption_at_rest
2. ebs_encryption

against a local Moto-backed mock AWS account.

No real AWS credentials or network calls are required.
"""

from collectors.aws_collector import (
    check_s3_encryption_at_rest,
    check_ebs_encryption,
)
from mock_aws import MockAWSEnvironment


def print_results(title, results):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    for result in results:
        print(
            f"{result.resource_id:<30} "
            f"{result.status.value.upper():<8} "
            f"{result.detail}"
        )


def main():
    with MockAWSEnvironment() as aws:

        print("Creating mock AWS resources...")

        aws.create_s3_bucket(
            "governx-encrypted-bucket",
            encrypted=True,
        )

        aws.create_s3_bucket(
            "governx-unencrypted-bucket",
            encrypted=False,
        )

        aws.create_ebs_volume(
            encrypted=True
        )

        aws.create_ebs_volume(
            encrypted=False
        )

        s3_results = (
            check_s3_encryption_at_rest()
        )

        ebs_results = (
            check_ebs_encryption()
        )

        print_results(
            "S3 ENCRYPTION AT REST",
            s3_results,
        )

        print_results(
            "EBS ENCRYPTION",
            ebs_results,
        )

        print()
        print("Final encryption checks verification completed.")


if __name__ == "__main__":
    main()