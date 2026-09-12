
## Additional finding: /scan/history not yet used by frontend

**Update:** Closed this gap same day. Built `fetchScanHistory()` API function, `ScanHistoryPanel` component with loading/error/empty states, styling, and wired it into the Dashboard. Live-verified in browser — correctly displays real persisted scan results with color-coded pass/fail status. Found and fixed one bug during verification (status column was missing from the table, silently only showing 3 of 4 columns).
Verified `GET /scan/history` directly — it works correctly and returns real persisted scan data (10 entries from actual test runs, Sep 9-10). However, the frontend does not call this endpoint anywhere yet (confirmed via `src/lib/api.js`). The backend piece of this feature is complete and tested; the UI to display scan history/trends is still unbuilt. Flagging for the team rather than building it myself, since scan history UI wasn't part of my assigned scope this week.
## Final verification (Day 6 close-out)

Full test suite: 76/76 passing. Dashboard confirmed connected to live backend data end-to-end (not placeholder values) after the CORS/port fix above.
## Known open items going into Week 3

1. Real AWS account verification still pending (unchanged from Week 1) — the dashboard now correctly and honestly displays "No Data" / "Needs attention" for this, rather than hiding it.
2. Scoring and gap analysis are built and tested against mocked data; broader validation against a fuller real-world dataset (once live AWS is connected) is still outstanding.

## Conclusion

Week 2 delivered a working scoring and gap-analysis layer, fully wired from backend to frontend, verified end-to-end rather than just unit-tested in isolation. That end-to-end check caught a real bug (masked placeholder data) that unit tests alone would not have surfaced — reinforcing that live verification remains a necessary step, not an optional formality, even when component tests are green.
## Bug found and fixed during Day 6 end-to-end verification

The dashboard was silently showing hardcoded demo numbers (82%, 76%, 88%, etc.) instead of real backend data. Root cause: `.env.example` pointed to `http://localhost:8000`, which had an unrelated service running on it, causing a CORS-blocked request that silently fell back to placeholder values. Fixed by correcting the default port to `8080` (where the backend actually runs) in `.env.example`. After the fix, the dashboard correctly shows the honest current state: 0% / Tier 1 / "Needs attention" — accurately reflecting that live AWS scanning isn't yet connected (see Week 1 scope doc's known open items), rather than masking it with fake data.
## What was built

- **Scoring engine** (`compliance/scorer.py`): `score_function()`, `get_tier()`, `score_all_functions()`, `score_overall()`, `gap_analysis()` — all with explicit handling for the "no data yet" case (never silently shown as Tier 1)
- **API integration:** `/scan/aws` now returns `scores`, `overall`, and `gaps` alongside raw check results
- **Persistence:** scan results now saved to a `scan_results` table, with a `GET /scan/history` endpoint
- **Dashboard endpoint:** `GET /dashboard/maturity` — purpose-built for the frontend's six-pillar Tier badge display
- **Frontend:** live Tier badges, per-pillar detail pages, connected to real backend data (not placeholder numbers)# GovernX — Week 2 Scope Document

**Project:** Project 3 — Automated NIST CSF 2.0 Compliance Engine (Week 2: NIST Ontology + Maturity Scoring)
**Company:** AXLERO Innovating Solutions
**Team:** Ansh Gautam, Mounika Dunna, Sujal Waghmode, Amrita, Yannam Chittikumari, Harshal Ghatbandhe (Lead)

## Summary

Week 2 moved the Week 1 check-to-CSF mapping into a real database and added a maturity scoring layer — turning raw pass/fail results into Tier 1–4 ratings per CSF function, plus gap analysis identifying which specific checks are limiting a tier.
