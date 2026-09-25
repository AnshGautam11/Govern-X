"""
Shared data contracts between collectors, mapping, compliance, and risk
engine modules. Keep this the single source of truth for shapes — every
module should import from here rather than redefining its own dict shape.
"""

from datetime import datetime
from enum import Enum

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

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


class RiskAssessmentRequest(BaseModel):
    """Input for a Monte Carlo risk assessment scenario."""

    sector: str = "financial"


class RiskAssessmentResponse(BaseModel):
    """Monte Carlo financial risk summary returned by the risk API."""

    sector: str
    p10: float
    p50: float
    expected: float
    p90: float
    p95: float
    p99: float
    iterations: int
    confidence_level: float
    distribution: list[float] = []
    generated_at: datetime
    data_quality: str
    disclaimer: str

class GovernanceResponseRequest(BaseModel):
    """Payload submitted by the governance questionnaire."""

    model_config = ConfigDict(extra="forbid")

    risk_owner_assigned: bool
    security_policy_reviewed: bool
    incident_response_plan_exists: bool
    third_party_risk_reviewed: bool


class GovernanceAnswerResponse(BaseModel):
    """One stored governance questionnaire response."""

    id: int
    question_id: int
    question_key: str
    question_text: str
    csf_category: str
    answer: bool
    notes: str | None = None
    answered_at: datetime

class GovernanceResponsesResponse(BaseModel):
    """Response containing the latest governance answers."""

    responses: list[GovernanceAnswerResponse]


class AssetCreateRequest(BaseModel):
    """Payload for adding a new asset to the inventory (W3-Day2)."""

    model_config = ConfigDict(extra="forbid")

    name: str
    value: float = Field(gt=0, description="Estimated dollar value of the asset.")
    criticality: Literal["low", "medium", "high", "critical"]


class AssetResponse(BaseModel):
    """One asset inventory entry."""

    id: int
    name: str
    value: float
    criticality: str
    created_at: datetime


class AssetListResponse(BaseModel):
    """Full asset inventory listing."""

    assets: list[AssetResponse]


class GovernanceProfile(BaseModel):
    organization_name: str = "Demo Enterprise"
    industry: str = "Technology"
    organization_size: str = "500-1000 employees"
    security_policy_status: str = "Mostly implemented"
    cybersecurity_policy_review_frequency: str = "Quarterly"
    risk_management_policy: str = "Documented"
    access_control_policy: str = "Implemented"
    data_protection_policy: str = "Implemented"
    incident_response_policy: str = "Implemented"
    business_continuity_policy: str = "Implemented"
    vendor_supplier_security_policy: str = "Required"
    third_party_risk_management: str = "Formal review"
    security_awareness_training: str = "Quarterly"
    asset_ownership: str = "Assigned by business owners"
    risk_appetite: str = "Low to moderate"
    compliance_requirements: list[str] = ["NIST CSF 2.0", "SOC 2"]
    policy_owner: str = "CISO"
    last_policy_review_date: str = "2026-09-01"


class SupplyChainVendor(BaseModel):
    vendor_name: str
    vendor_type: str
    criticality: str
    service_provided: str
    data_access: bool
    privileged_access: bool
    security_assessment_status: str
    contract_security_requirements: str
    last_assessment: str
    risk_level: str
    associated_technical_controls: list[str] = []


class GovernanceControlMapping(BaseModel):
    policy: str
    governance_requirement: str
    technical_control: str
    aws_finding: str
    nist: str
    risk: str


class GovernanceSummary(BaseModel):
    policy_coverage: float
    supply_chain_risk: float
    governance_control_coverage: float
    governance_maturity: float
    governance_gaps: list[str] = []
    critical_governance_controls: list[str] = []
    policy_review_status: str = "Current"
    vendor_risk: list[SupplyChainVendor] = []
    control_mappings: list[GovernanceControlMapping] = []


class FinancialAssetCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(..., description="Stable asset identifier.")
    asset_name: str = Field(..., description="Business or technical asset name.")
    asset_type: str = "Application"
    cloud_provider: str = "AWS"
    business_function: str = "Core platform"
    data_sensitivity: str = "Sensitive"
    criticality: Literal["low", "medium", "high", "critical"] = "high"
    asset_value: float = Field(gt=0, description="Asset value in INR.")
    revenue_dependency: float = Field(default=0.5, ge=0, le=1)
    customer_dependency: float = Field(default=0.5, ge=0, le=1)
    recovery_cost: float = Field(default=0.0, ge=0)
    regulatory_exposure: float = Field(default=0.0, ge=0, le=1)


class FinancialAssetResponse(BaseModel):
    asset_id: str
    asset_name: str
    asset_type: str
    cloud_provider: str
    business_function: str
    data_sensitivity: str
    criticality: str
    asset_value: float
    revenue_dependency: float
    customer_dependency: float
    recovery_cost: float
    regulatory_exposure: float


class FinancialRiskCalculationRequest(BaseModel):
    check_id: str = "iam_policy_wildcard_admin"
    asset_name: str = "Production API"
    asset_value: float = 4000000.0
    exposure_factor: float = 0.4
    annual_rate_of_occurrence: float = 1.5


class FinancialRiskCalculationResponse(BaseModel):
    check_id: str
    asset_name: str
    control: str
    asset_value: float
    exposure_factor: float
    likelihood: float
    sle: float
    aro: float
    ale: float
    estimated_loss: float
    risk_level: str
    nist_function: str
    currency: str = "INR"


class FinancialSummaryResponse(BaseModel):
    total_asset_value: float
    estimated_financial_exposure: float
    potential_loss: float
    high_risk_assets: int
    critical_control_failures: int
    assets: list[FinancialAssetResponse] = []
    findings: list[dict] = []
    generated_at: datetime


class RiskHistoryEntry(BaseModel):
    timestamp: datetime
    label: str
    total_asset_value: float
    estimated_financial_exposure: float
    high_risk_assets: int


class RiskHistoryResponse(BaseModel):
    history: list[RiskHistoryEntry]
