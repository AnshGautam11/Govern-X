# Week 3 Scope: Govern Function and Risk Translation

**Author:** Harshal Ghatbandhe

## Govern function
GV.OC, GV.RM, GV.RR, GV.PO, GV.OV and GV.SC are organizational and policy-based, so they cannot be scanned through boto3. They are covered by a self-attestation questionnaire (/governance/*). See docs/week3_day1_govern_scope.md.

## Risk translation
/risk/* turns failed checks into a financial view using a Monte Carlo model (risk_engine/monte_carlo.py). Asset values and Annual Rate of Occurrence are ASSUMED sample data, not real organizational figures. The dashboard and demo must say so.

## Verified live (Day 6, local server on port 8001)
| Endpoint | Result |
|---|---|
| /governance/score | 200 |
| /risk/summary | 200 |
| /risk/financial-summary | 200 |
| /scan/history | 200 |

## Known gaps
- No combined report route (compliance + risk + governance) exists in the API. Registered routes are /scan/*, /governance/*, /risk/*, /findings, /gaps and /health.
- /scan/history holds mixed runs from manual and mock scenarios. Start the demo from a fresh scan.
