4. **Non-negotiable:** every dashboard/API surface showing financial figures must carry the "sample/assumed data, not real organizational figures" disclaimer already present in `monte_carlo.py`'s docstring — do not let it get lost as this gets wired into UI.3. Combined report (Day 5, Sujal): joins compliance score + risk assessment + governance responses into one view.2. Governance questionnaire: new DB table (Mounika, Day 1) + `GET/POST /governance/responses` endpoints (Mounika, Day 2).1. New endpoint `POST /risk/assess` — accepts a sector key (e.g. "financial"), pulls parameters from `MOCK_ASSET_DATA[sector]`, runs `run_monte_carlo()`, returns `summarize()` output (p10/expected/p90 loss).
## Risk engine wiring plan

Existing scaffold (`risk_engine/monte_carlo.py`, Week 1): `run_monte_carlo()` and `summarize()`.

Plan:
**Scope decision:** build the questionnaire as 4 yes/no fields mapped to these 4 categories for Week 3 — matching the honest-narrow-scope precedent set in Week 1 (12 checks, not 100+). Do not claim full GV.SC (10 subcategories) or GV.RM coverage from one field each.
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
