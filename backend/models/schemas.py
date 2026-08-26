"""
Shared data contracts between collectors, mapping, compliance, and risk
engine modules. Keep this the single source of truth for shapes — every
module should import from here rather than redefining its own dict shape.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class CheckStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"  # check could not run (e.g. missing permission)


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CheckResult(BaseModel):
    """Raw output of a single boto3 check, before CSF mapping is applied."""

    check_id: str = Field(..., description="Stable slug, e.g. 's3_public_access_block'")
    resource_id: str = Field(..., description="ARN or identifier of the audited resource")
    status: CheckStatus
    severity: Severity
    detail: str = Field(..., description="Human-readable explanation of the finding")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CSFMapping(BaseModel):
    """One row of the Framework Mapping Matrix — links a check to CSF 2.0."""

    check_id: str
    csf_function: str = Field(..., description="One of Govern/Identify/Protect/Detect/Respond/Recover")
    csf_subcategory: str = Field(..., description="e.g. PR.DS-01")
    justification: str = Field(..., description="One-line reason this check maps to this subcategory")


class MappedFinding(BaseModel):
    """A CheckResult joined with its CSF mapping — what the dashboard consumes."""

    result: CheckResult
    mapping: CSFMapping


class ScanResponse(BaseModel):
    results: list[CheckResult]
