from __future__ import annotations

from copy import deepcopy


def mock_governance_profile() -> dict:
    return {
        "organization_name": "Demo Enterprise",
        "industry": "Technology",
        "organization_size": "500-1000 employees",
        "security_policy_status": "Mostly implemented",
        "cybersecurity_policy_review_frequency": "Quarterly",
        "risk_management_policy": "Documented",
        "access_control_policy": "Implemented",
        "data_protection_policy": "Implemented",
        "incident_response_policy": "Implemented",
        "business_continuity_policy": "Implemented",
        "vendor_supplier_security_policy": "Required",
        "third_party_risk_management": "Formal review",
        "security_awareness_training": "Quarterly",
        "asset_ownership": "Assigned by business owners",
        "risk_appetite": "Low to moderate",
        "compliance_requirements": ["NIST CSF 2.0", "SOC 2"],
        "policy_owner": "CISO",
        "last_policy_review_date": "2026-09-01",
        "policy_coverage": 88.0,
        "supply_chain_risk": 32.5,
        "governance_control_coverage": 76.0,
        "governance_maturity": 81.0,
        "governance_gaps": [
            "Third-party contract security clauses require review",
            "Privileged access reviews are not fully quarterly",
        ],
        "critical_governance_controls": [
            "IAM least privilege",
            "Vendor security review",
            "Incident response readiness",
        ],
        "policy_review_status": "Current",
        "vendor_risk": [
            {
                "vendor_name": "Cloud Monitoring Provider",
                "vendor_type": "SaaS",
                "criticality": "High",
                "service_provided": "Telemetry ingestion",
                "data_access": True,
                "privileged_access": True,
                "security_assessment_status": "Review pending",
                "contract_security_requirements": "SOC 2 + MFA enforcement",
                "last_assessment": "2026-08-20",
                "risk_level": "Moderate",
                "associated_technical_controls": ["IAM least privilege", "MFA enforcement"],
            }
        ],
        "control_mappings": [
            {
                "policy": "Access Control Policy",
                "governance_requirement": "Privileged access must be restricted",
                "technical_control": "IAM least privilege",
                "aws_finding": "Wildcard administrative policy detected",
                "nist": "Govern / Protect",
                "risk": "High",
            },
            {
                "policy": "Vendor Security Policy",
                "governance_requirement": "Third-party risk must be assessed",
                "technical_control": "Vendor security review",
                "aws_finding": "Cloud Monitoring provider with privileged access",
                "nist": "Govern",
                "risk": "Medium",
            },
        ],
    }


def build_governance_summary(profile: dict | None = None) -> dict:
    source = deepcopy(profile or mock_governance_profile())
    policy_coverage = float(source.get("policy_coverage", 0.0) or 0.0)
    supply_chain_risk = float(source.get("supply_chain_risk", 0.0) or 0.0)
    governance_control_coverage = float(source.get("governance_control_coverage", 0.0) or 0.0)
    governance_maturity = float(source.get("governance_maturity", 0.0) or 0.0)

    return {
        "organization_name": source.get("organization_name", "Demo Enterprise"),
        "policy_coverage": round(policy_coverage, 1),
        "supply_chain_risk": round(supply_chain_risk, 1),
        "governance_control_coverage": round(governance_control_coverage, 1),
        "governance_maturity": round(governance_maturity, 1),
        "governance_gaps": source.get("governance_gaps", []),
        "critical_governance_controls": source.get("critical_governance_controls", []),
        "policy_review_status": source.get("policy_review_status", "Current"),
        "vendor_risk": source.get("vendor_risk", []),
        "control_mappings": source.get("control_mappings", []),
    }
