"""
Compliance & maturity scoring — Week 2 scope.

Turns a list of MappedFinding into per-function scores and a Tier
1-4 maturity rating. Left as a stub for Week 2; see the project's
Week 2 task list before implementing.
"""

from models.schemas import MappedFinding


def score_function(findings: list[MappedFinding], function_name: str) -> float:
    """Return a 0-100 score for one CSF function based on pass/fail findings."""
    raise NotImplementedError("Week 2 scope — implement maturity scoring logic here")
