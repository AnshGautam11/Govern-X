"""
Compliance & maturity scoring — Week 2/Week 3.

Turns a list of MappedFinding (CheckResult + CSFMapping) into
per-function scores and a Tier 1-4 maturity rating.

Scoring formula:
    score_function() = (# PASS / # PASS+FAIL, excluding ERROR) * 100

ERROR results are excluded from the denominator.

Tier boundaries:
    Tier 1: 0-25%
    Tier 2: 26-50%
    Tier 3: 51-75%
    Tier 4: 76-100%

Week 3 governance scoring:
    Governance questionnaire answers are converted into a completion
    percentage and used as the Govern function score.

Gap analysis also estimates financial impact using the existing
synthetic risk model:

    SLE = Asset Value × Exposure Factor
    ALE = SLE × Annual Rate of Occurrence

All financial values are synthetic/demo values.
"""

from models.schemas import MappedFinding, CheckStatus
from risk_engine.mock_data import MOCK_ASSET_DATA


TIER_BOUNDARIES = [
    (25, "Tier 1"),
    (50, "Tier 2"),
    (75, "Tier 3"),
    (100, "Tier 4"),
]


def score_governance_completion(answers: dict[str, bool]) -> float | None:
    """
    Calculate the governance questionnaire completion score.

    True represents a completed governance requirement.
    False represents an incomplete governance requirement.

    Returns None when no governance answers are supplied.
    """
    if not answers:
        return None

    valid_answers = [
        answer
        for answer in answers.values()
        if isinstance(answer, bool)
    ]

    if not valid_answers:
        return None

    completed = sum(1 for answer in valid_answers if answer)

    return round((completed / len(valid_answers)) * 100, 1)


def score_function(
    findings: list[MappedFinding],
    function_name: str,
) -> float | None:
    """
    Return a 0-100 pass-rate score for one CSF function.

    Returns None if there are no eligible PASS/FAIL findings.
    """
    relevant = [
        f
        for f in findings
        if f.mapping.csf_function == function_name
        and f.result.status in (CheckStatus.PASS, CheckStatus.FAIL)
    ]

    if not relevant:
        return None

    passed = sum(
        1
        for f in relevant
        if f.result.status == CheckStatus.PASS
    )

    return round((passed / len(relevant)) * 100, 1)


def get_tier(score: float | None) -> str:
    """Map a 0-100 score to a Tier 1-4 label. None -> 'No Data'."""
    if score is None:
        return "No Data"

    for threshold, label in TIER_BOUNDARIES:
        if score <= threshold:
            return label

    return "Tier 4"


def score_all_functions(
    findings: list[MappedFinding],
    governance_score: float | None = None,
) -> dict[str, dict]:
    """
    Score every CSF function present in the findings.

    If governance_score is supplied, include it as the Govern
    function score.
    """
    functions = sorted(
        {f.mapping.csf_function for f in findings}
    )

    scores = {
        fn: {
            "score": (s := score_function(findings, fn)),
            "tier": get_tier(s),
        }
        for fn in functions
    }

    if governance_score is not None:
        scores["Govern"] = {
            "score": governance_score,
            "tier": get_tier(governance_score),
        }

    return scores


def score_overall(
    findings: list[MappedFinding],
    governance_score: float | None = None,
) -> dict:
    """
    Aggregate maturity score across all CSF functions.

    Functions with no eligible data are excluded.
    """
    per_function = score_all_functions(
        findings,
        governance_score=governance_score,
    )

    scored = [
        v["score"]
        for v in per_function.values()
        if v["score"] is not None
    ]

    if not scored:
        return {
            "score": None,
            "tier": "No Data",
        }

    overall = round(sum(scored) / len(scored), 1)

    return {
        "score": overall,
        "tier": get_tier(overall),
    }


def _financial_impact_per_resource() -> float:
    """
    Calculate the estimated annual financial impact for one failed resource.

    Formula:
        SLE = Asset Value × Exposure Factor
        ALE = SLE × Annual Rate of Occurrence

    The midpoint of the configured synthetic ranges is used so the
    gap-analysis result remains deterministic and testable.
    """
    financial = MOCK_ASSET_DATA["financial"]

    asset_value = sum(
        financial["asset_value_range"]
    ) / 2

    exposure_factor = sum(
        financial["exposure_factor_range"]
    ) / 2

    annual_rate = financial["annual_rate_of_occurrence"]

    sle = asset_value * exposure_factor
    ale = sle * annual_rate

    return round(ale, 2)


def gap_analysis(
    findings: list[MappedFinding],
    function_name: str,
) -> list[dict]:
    """
    List the specific checks dragging down a CSF function's tier.

    Each gap includes:
        - check_id
        - csf_subcategory
        - failing_resource_count
        - resource_ids
        - detail
        - financial_impact

    Financial impact is estimated using the existing synthetic financial
    risk model:

        ALE = Asset Value × Exposure Factor × Annual Rate of Occurrence

    The estimated impact is multiplied by the number of failing resources.
    """
    failing = [
        f
        for f in findings
        if f.mapping.csf_function == function_name
        and f.result.status == CheckStatus.FAIL
    ]

    grouped: dict[str, list] = {}

    for f in failing:
        grouped.setdefault(
            f.result.check_id,
            [],
        ).append(f)

    financial_impact_per_resource = _financial_impact_per_resource()

    gaps = []

    for check_id, group in grouped.items():
        failing_resource_count = len(group)

        financial_impact = round(
            financial_impact_per_resource
            * failing_resource_count,
            2,
        )

        gaps.append({
            "check_id": check_id,
            "csf_subcategory": group[0].mapping.csf_subcategory,
            "failing_resource_count": failing_resource_count,
            "resource_ids": [
                g.result.resource_id
                for g in group
            ],
            "detail": group[0].result.detail,
            "financial_impact": financial_impact,
        })

    gaps.sort(
        key=lambda g: g["financial_impact"],
        reverse=True,
    )

    return gaps