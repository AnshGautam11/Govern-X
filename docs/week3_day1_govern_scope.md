
## Govern function overview (verified against NIST CSF 2.0)

Govern has 6 categories, 31 subcategories total:

| Category | Code | Automatable via API? |
|---|---|---|
| Organizational Context | GV.OC | No — questionnaire |
| Risk Management Strategy | GV.RM | No — questionnaire |
| Roles, Responsibilities, Authorities | GV.RR | No — questionnaire |
| Policy | GV.PO | No — questionnaire |

All 4 mock questionnaire fields already added to `risk_engine/mock_data.py` map to real categories:

| Mock field | CSF 2.0 mapping | Notes |
|---|---|---|
| `risk_owner_assigned` | GV.RR (Roles, Responsibilities, Authorities) | Cybersecurity ownership assigned at leadership level |
| `security_policy_reviewed` | GV.PO (Policy) | Policy established and periodically reviewed |
| `incident_response_plan_exists` | GV.OV (Oversight) | Oversight of whether IR capability exists; adjacent to Respond function, kept under Govern per project scope |
| `third_party_risk_reviewed` | GV.SC (Supply Chain Risk Management) | GV.SC has 10 subcategories on its own — this single yes/no field is a coarse proxy, not full coverage || Oversight | GV.OV | No — questionnaire |
| Supply Chain Risk Management | GV.SC | No — questionnaire |

Confirms the Week 1 finding: none of Govern is scannable via boto3.# Week 3, Day 1 — Govern Function Scope Review + Risk Engine Wiring Plan

**Author:** Harshal Ghatbandhe 
