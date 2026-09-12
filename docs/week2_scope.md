
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
