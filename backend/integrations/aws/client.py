"""
boto3 session/client factory.

Use a dedicated read-only IAM policy for the credentials GovernX runs
with (SecurityAudit managed policy is a good starting point). GovernX
should never need write access to the accounts it audits.
"""

import boto3

from config.settings import get_settings


def get_session() -> boto3.Session:
    settings = get_settings()
    kwargs: dict = {"region_name": settings.aws_region}
    if settings.aws_profile:
        kwargs["profile_name"] = settings.aws_profile
    return boto3.Session(**kwargs)


def get_client(service_name: str):
    return get_session().client(service_name)
