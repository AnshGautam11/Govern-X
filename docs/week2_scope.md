
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
