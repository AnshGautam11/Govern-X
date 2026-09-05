"""
Compliance & maturity scoring — Week 2.

Turns a list of MappedFinding (CheckResult + CSFMapping) into per-function
scores and a Tier 1-4 maturity rating.

Scoring formula (reviewed Week 2 Day 1):
    score_function() = (# PASS / # PASS+FAIL, excluding ERROR) * 100

ERROR results are excluded from the denominator — a check that couldn't
run (e.g. missing permission) should not silently count as a failure or
inflate a pass rate; it's a data-quality gap, not a compliance gap.

Tier boundaries (percent pass rate):
    Tier 1: 0-25%      Tier 2: 26-50%
    Tier 3: 51-75%     Tier 4: 76-100%

A function with zero eligible findings (no PASS/FAIL results at all)
returns None for score and "No Data" for tier — this must be handled
explicitly by callers (e.g. the dashboard) rather than silently shown
as Tier 1, which would misrepresent "not scanned" as "non-compliant".
"""

from models.schemas import MappedFinding, CheckStatus

TIER_BOUNDARIES = [
    (25, "Tier 1"),
    (50, "Tier 2"),
    (75, "Tier 3"),
    (100, "Tier 4"),
]


def score_function(findings: list[MappedFinding], function_name: str) -> float | None:
    """
    Return a 0-100 pass-rate score for one CSF function.

    Returns None if there are no eligible (PASS/FAIL) findings for this
    function — callers must handle None as "not yet scanned", not as 0.
    """
    relevant = [
        f for f in findings
        if f.mapping.csf_function == function_name
        and f.result.status in (CheckStatus.PASS, CheckStatus.FAIL)
    ]
    if not relevant:
        return None

    passed = sum(1 for f in relevant if f.result.status == CheckStatus.PASS)
    return round((passed / len(relevant)) * 100, 1)


def get_tier(score: float | None) -> str:
    """Map a 0-100 score to a Tier 1-4 label. None -> 'No Data'."""
    if score is None:
        return "No Data"
    for threshold, label in TIER_BOUNDARIES:
        if score <= threshold:
            return label
    return "Tier 4"


def score_all_functions(findings: list[MappedFinding]) -> dict[str, dict]:
    """
    Score every CSF function present in the findings.

    Returns e.g.:
        {"Protect": {"score": 83.3, "tier": "Tier 4"}, "Detect": {"score": None, "tier": "No Data"}, ...}
    """
    functions = sorted({f.mapping.csf_function for f in findings})
    return {
        fn: {"score": (s := score_function(findings, fn)), "tier": get_tier(s)}
        for fn in functions
    }


def score_overall(findings: list[MappedFinding]) -> dict:
    """
    Aggregate maturity score across all 6 CSF functions.

    Uses only functions with eligible data — a function with no findings
    yet does not drag down the overall score to zero.
    """
    per_function = score_all_functions(findings)
    scored = [v["score"] for v in per_function.values() if v["score"] is not None]
    if not scored:
        return {"score": None, "tier": "No Data"}
    overall = round(sum(scored) / len(scored), 1)
    return {"score": overall, "tier": get_tier(overall)}
