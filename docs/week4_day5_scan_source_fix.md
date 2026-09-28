# Week 4, Day 5: Scan Source Fix and Report Check

**Author:** Harshal Ghatbandhe

## Problem
/scan/aws fell back to a hardcoded all-PASS list because both mock stages imported code that does not exist, so the dashboard showed $0 at risk.

## Fix
The real collectors now run inside a moto mock AWS account when live AWS is unavailable. Two bugs were found on the way: the client stand-in returned None for services other than ec2/s3/iam/cloudtrail (rds check crashed), and a stale uvicorn process kept serving old code after the fix.

## Result
A scan now records real failing controls (root MFA, password policy, CloudTrail, VPC flow logs, EBS encryption). The data comes from a moto mock account, NOT a live AWS environment. Live AWS scanning is not verified.

## Report PDF
Remediation items with severity and CSF subcategory are present; disclaimers and the self-attested governance label are present.

## Known gap
/risk/summary reports missing_asset_risk_parameters for the new findings, so expected loss is None until asset parameters are defined for those checks.
