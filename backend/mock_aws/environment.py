"""Moto-backed mock AWS environment for local integration tests."""

from __future__ import annotations

import boto3


class MockAWSEnvironment:
    """Provide an isolated Moto AWS environment for tests."""

    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self._mock = None
        self.ec2 = None
        self.cloudtrail = None
        self._flow_logs = []
        self._created_vpcs = []

    def __enter__(self):
        from moto import mock_aws

        self._mock = mock_aws()
        self._mock.start()

        self.ec2 = boto3.client("ec2", region_name=self.region)
        self.cloudtrail = boto3.client("cloudtrail", region_name=self.region)

        # Only expose VPCs explicitly created by our tests.
        original_describe_vpcs = self.ec2.describe_vpcs

        def describe_vpcs(*args, **kwargs):
            response = original_describe_vpcs(*args, **kwargs)
            response["Vpcs"] = [
                vpc
                for vpc in response.get("Vpcs", [])
                if vpc.get("VpcId") in self._created_vpcs
            ]
            return response

        self.ec2.describe_vpcs = describe_vpcs

        # Expose our in-memory flow logs to the collector.
        def describe_flow_logs(Filters=None, **kwargs):
            logs = list(self._flow_logs)

            if Filters:
                for item in Filters:
                    if item.get("Name") == "resource-id":
                        resource_ids = set(item.get("Values", []))
                        logs = [
                            log
                            for log in logs
                            if log.get("ResourceId") in resource_ids
                        ]

            return {"FlowLogs": logs}

        self.ec2.describe_flow_logs = describe_flow_logs

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._mock is not None:
            self._mock.stop()
            self._mock = None

    def create_vpc(self, cidr_block: str = "10.0.0.0/16") -> str:
        response = self.ec2.create_vpc(CidrBlock=cidr_block)
        vpc_id = response["Vpc"]["VpcId"]
        self._created_vpcs.append(vpc_id)
        return vpc_id

    def create_vpc_flow_logs(self, vpc_id: str) -> str:
        flow_log_id = f"fl-{vpc_id.removeprefix('vpc-')}"

        self._flow_logs.append(
            {
                "FlowLogId": flow_log_id,
                "ResourceId": vpc_id,
                "ResourceType": "VPC",
                "FlowLogStatus": "ACTIVE",
                "TrafficType": "ALL",
            }
        )

        return flow_log_id

    def describe_flow_logs(self):
        return {"FlowLogs": list(self._flow_logs)}

    def create_cloudtrail_trail(
        self,
        name: str = "governx-trail",
        bucket_name: str = "governx-audit-bucket",
    ) -> str:
        s3 = boto3.client("s3", region_name=self.region)
        s3.create_bucket(Bucket=bucket_name)

        response = self.cloudtrail.create_trail(
            Name=name,
            S3BucketName=bucket_name,
        )

        self.cloudtrail.start_logging(Name=name)

        return response["TrailARN"]
