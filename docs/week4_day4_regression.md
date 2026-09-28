# Week 4, Day 4: Regression

**Author:** Harshal Ghatbandhe

## Backend endpoints (local server, port 8080)
health, scan/history, governance/score, risk/summary, reports/combined, report/pdf and dashboard/maturity all returned HTTP 200.

## Test suite
149 passed. The demo database row count (scan_results) was unchanged by the test run, confirming tests use the isolated temp database.

## Known data issue
scan_results still holds fixture rows written by test runs before isolation was added (Week 3, Day 6). The history panel therefore shows mixed pass/fail results for the same resource at the same timestamp. Cleanup planned before the demo.

## Dashboard and PDF download
Not verified in the browser: dashboard risk cards, sample-data disclaimer on the dashboard, and the Download Report button were not checked in this session.

## Findings
- After merging teammates' Week 4 work the suite briefly failed (1 failed, 148 passed); after the next pull it was 149 passed.
- /risk/summary returns "unavailable" (missing_asset_risk_parameters) while /risk/financial-summary prices the same scan (exposure 875,000). The two risk paths use different asset tables (assets vs financial_assets). The dashboard reads /risk/summary.
- The assets table still holds test fixture rows from before test isolation was added.
- A stale uvicorn process kept serving old code after a fix; restart it (check port 8080) after every merge.
