"""
Financial risk quantifier — Week 3 scope.

Simplified ALE model: ALE = SLE x ARO, where SLE = Asset Value x
Exposure Factor. Monte Carlo simulation samples distributions over
asset value, exposure factor, and annual rate of occurrence to
produce a loss distribution rather than a single point estimate.

IMPORTANT: asset values and ARO in the demo are ASSUMED/SAMPLE data,
not real organizational figures. Say this explicitly in the writeup
and dashboard — do not imply board-ready accuracy from synthetic inputs.
"""

import numpy as np


def run_monte_carlo(
    asset_value_range: tuple[float, float],
    exposure_factor_range: tuple[float, float],
    annual_rate_of_occurrence: float,
    iterations: int = 10_000,
    seed: int | None = None,
) -> np.ndarray:
    """
    Return an array of `iterations` simulated annual loss values.

    asset_value_range / exposure_factor_range: (low, high) for a
    uniform distribution — swap for a triangular/PERT distribution
    once you have more realistic estimates.
    """
    rng = np.random.default_rng(seed)
    asset_values = rng.uniform(*asset_value_range, size=iterations)
    exposure_factors = rng.uniform(*exposure_factor_range, size=iterations)
    occurrences = rng.poisson(annual_rate_of_occurrence, size=iterations)

    sle = asset_values * exposure_factors
    ale = sle * occurrences
    return ale


def summarize(losses: np.ndarray) -> dict:
    return {
        "p10": float(np.percentile(losses, 10)),
        "expected": float(np.mean(losses)),
        "p90": float(np.percentile(losses, 90)),
    }
