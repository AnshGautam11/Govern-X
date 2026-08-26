"""
Smoke tests for the Week 1 scaffold — no real AWS calls, just proves
the module structure imports cleanly and the check registry populates.
Run with: pytest tests/test_scaffold.py
"""

from collectors.aws_collector import CHECK_REGISTRY
from mappings.csf_mappings import CSF_MAPPINGS


def test_check_registry_populated():
    assert "s3_public_access_block" in CHECK_REGISTRY
    assert "iam_user_mfa" in CHECK_REGISTRY


def test_every_registered_check_has_a_mapping():
    """Catches the case where someone adds a check but forgets the CSF mapping row."""
    for check_id in CHECK_REGISTRY:
        assert check_id in CSF_MAPPINGS, f"{check_id} is missing a CSFMapping row"
