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


class FunctionScore(BaseModel):
    score: float | None
    tier: str

class ScanResponse(BaseModel):
    results: list[CheckResult]
    scores: dict[str, FunctionScore] = {}
    overall: FunctionScore | None = None
    gaps: dict[str, list[dict]] = {}
    scan_id: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    findings: list[MappedFinding] = []
    nist_mapping: list[CSFMapping] = []
    pillar_scores: dict[str, FunctionScore] = {}
    overall_score: float | None = None
    overall_tier: int | None = None
    tier_name: str = "No Data"


class ScanHistoryEntry(BaseModel):
    """One persisted scan result row, as returned by GET /scan/history."""

    id: int
    check_id: str
    resource_id: str
    status: CheckStatus
    detail: str
    scanned_at: datetime


class ScanHistoryResponse(BaseModel):
    entries: list[ScanHistoryEntry]


class ScanCompareResponse(BaseModel):
    """W2-Day5 — diff between the two most recent scans."""

    current_scanned_at: datetime | None
    previous_scanned_at: datetime | None
    newly_passing: list[str]
    newly_failing: list[str]
    unchanged: list[str]
    new_checks: list[str]
    removed_checks: list[str]


class PillarMaturity(BaseModel):
    function: str
    percentage: float | None = 0
    tier: int | None = None
    tier_name: str = "No Data"
    trend: float = 0
    status: str = "No Data"


class MaturityOverview(BaseModel):
    percentage: float | None = 0
    tier: int | None = None
    tier_name: str = "No Data"
    trend: float = 0
    status: str = "No Data"


class DashboardMaturityResponse(BaseModel):
    overall: MaturityOverview
    pillars: list[PillarMaturity] = []
