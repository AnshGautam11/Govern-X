from __future__ import annotations

from datetime import datetime, timezone


FINDING_TO_CONTROL = {
    "iam_policy_wildcard_admin": "IAM least privilege",
    "security_group_open_ingress": "Security group hardening",
    "s3_encryption_at_rest": "Encryption at rest",
    "cloudtrail_enabled": "CloudTrail logging",
    "ebs_encryption": "EBS encryption",
    "rds_encryption_at_rest": "RDS encryption",
}

FINDING_TO_ASSET = {
    "iam_policy_wildcard_admin": "Production API",
    "security_group_open_ingress": "Production Web Server",
    "s3_encryption_at_rest": "Customer Data Bucket",
    "cloudtrail_enabled": "Security Operations Workspace",
    "ebs_encryption": "Production Database",
    "rds_encryption_at_rest": "Analytics Database",
}

FINANCIAL_ASSET_LIBRARY = [
    {
        "asset_id": "asset-prod-api",
        "asset_name": "Production API",
        "asset_type": "Application",
        "cloud_provider": "AWS",
        "business_function": "Customer transactions",
        "data_sensitivity": "Highly Sensitive",
        "criticality": "critical",
        "asset_value": 4000000.0,
        "revenue_dependency": 0.85,
        "customer_dependency": 0.8,
        "recovery_cost": 550000.0,
        "regulatory_exposure": 0.7,
    },
    {
        "asset_id": "asset-web-tier",
        "asset_name": "Production Web Server",
        "asset_type": "Compute",
        "cloud_provider": "AWS",
        "business_function": "Web hosting",
        "data_sensitivity": "Sensitive",
        "criticality": "high",
        "asset_value": 2500000.0,
        "revenue_dependency": 0.7,
        "customer_dependency": 0.65,
        "recovery_cost": 300000.0,
        "regulatory_exposure": 0.45,
    },
    {
        "asset_id": "asset-critical-db",
        "asset_name": "Production Customer Database",
        "asset_type": "Database",
        "cloud_provider": "AWS",
        "business_function": "Transactional data",
        "data_sensitivity": "Highly Sensitive",
        "criticality": "critical",
        "asset_value": 5000000.0,
        "revenue_dependency": 0.9,
        "customer_dependency": 0.95,
        "recovery_cost": 800000.0,
        "regulatory_exposure": 0.8,
    },
]


def calculate_sle(asset_value: float, exposure_factor: float) -> float:
    return round(float(asset_value) * float(exposure_factor), 2)


def calculate_ale(sle: float, aro: float) -> float:
    return round(float(sle) * float(aro), 2)


def get_asset_by_name(asset_name: str) -> dict | None:
    for asset in FINANCIAL_ASSET_LIBRARY:
        if asset["asset_name"] == asset_name:
            return asset
    return None


def calculate_risk_for_finding(
    check_id: str,
    asset_value: float,
    exposure_factor: float,
    annual_rate_of_occurrence: float,
    asset_name: str | None = None,
) -> dict:
    asset_name = asset_name or FINDING_TO_ASSET.get(check_id, "Production API")
    asset = get_asset_by_name(asset_name) or {"asset_name": asset_name, "criticality": "high"}
    exposure = float(exposure_factor)
    likelihood = float(annual_rate_of_occurrence)
    sle = calculate_sle(asset_value, exposure)
    ale = calculate_ale(sle, likelihood)
    estimated_loss = ale
    if exposure < 0.15:
        risk_level = "low"
    elif exposure < 0.35:
        risk_level = "medium"
    elif exposure < 0.6:
        risk_level = "high"
    else:
        risk_level = "critical"

    return {
        "check_id": check_id,
        "asset_name": asset_name,
        "asset_value": float(asset_value),
        "exposure_factor": exposure,
        "likelihood": likelihood,
        "sle": sle,
        "aro": likelihood,
        "ale": ale,
        "estimated_loss": estimated_loss,
        "risk_level": risk_level,
        "control": FINDING_TO_CONTROL.get(check_id, "Security control review"),
        "nist_function": "Protect",
        "asset_criticality": asset.get("criticality", "high"),
        "currency": "INR",
    }


def summarize_financial_risk() -> dict:
    assets = FINANCIAL_ASSET_LIBRARY
    total_asset_value = sum(float(item["asset_value"]) for item in assets)
    findings = []
    total_estimated_exposure = 0.0
    high_risk_assets = 0
    for asset in assets:
        for check_id in ["iam_policy_wildcard_admin", "security_group_open_ingress", "s3_encryption_at_rest"]:
            estimate = calculate_risk_for_finding(
                check_id=check_id,
                asset_value=float(asset["asset_value"]),
                exposure_factor=0.35 if asset["criticality"] == "critical" else 0.25,
                annual_rate_of_occurrence=1.5,
                asset_name=asset["asset_name"],
            )
            findings.append(estimate)
            total_estimated_exposure += estimate["estimated_loss"]
            if estimate["risk_level"] in {"high", "critical"}:
                high_risk_assets += 1
    return {
        "total_asset_value": total_asset_value,
        "estimated_financial_exposure": round(total_estimated_exposure, 2),
        "potential_loss": round(total_estimated_exposure * 0.7, 2),
        "high_risk_assets": high_risk_assets,
        "critical_control_failures": len(findings),
        "assets": assets,
        "findings": findings,
        "generated_at": datetime.now(timezone.utc),
    }
