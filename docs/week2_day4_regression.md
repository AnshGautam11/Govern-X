# Week 2, Day 4 — Regression Check

**Performed by:** Harshal Ghatbandhe (Lead)
**Result:** PASS — no regressions found

## What was verified

1. **Full test suite:** 61/61 tests passing (up from 55 on Day 3)
2. **All 12 Week 1 checks intact** after today's aws_collector.py cleanup (59 lines removed — confirmed dead code, not a dropped check)
3. **All 12 checks still correctly CSF-mapped** — zero missing mappings
4. **Week 2 Day 1-2 scoring work intact:** all 12 scorer + integration tests passing after today's app.py changes
5. **Live endpoint verification** (not just unit tests):
   - `GET /health` — responding correctly
   - `POST /scan/aws` — schema still includes `scores` and `overall` fields
   - `GET /scan/history` — new endpoint (Sujal, Day 2) confirmed live and correctly wired to the persistence layer

## What landed since Day 3

- `app.py`, `models/schemas.py`, `database/persistence.py` extended for `/scan/history`
- `aws_collector.py` cleaned up (dead code removed, checks unaffected)
- New tests: `test_scan_history_endpoint.py`, expanded `test_mock_aws.py`

## Conclusion

Safe for the team to continue building Day 5 work (UI polish, scan comparison, gap analysis) on top of the current main branch.
