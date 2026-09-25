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


def _validate_range(name: str, values: tuple[float, float], minimum: float, maximum: float | None = None) -> tuple[float, float]:
    if len(values) != 2:
        raise ValueError(f"{name} must contain exactly two values.")
    low, high = (float(value) for value in values)
    if not np.isfinite(low) or not np.isfinite(high) or low < minimum or high < low:
        raise ValueError(f"{name} must be finite, ordered, and at least {minimum}.")
    if maximum is not None and high > maximum:
        raise ValueError(f"{name} must not exceed {maximum}.")
    return low, high


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
    asset_value_range = _validate_range("asset_value_range", asset_value_range, 0.0)
    exposure_factor_range = _validate_range("exposure_factor_range", exposure_factor_range, 0.0, 1.0)
    annual_rate_of_occurrence = float(annual_rate_of_occurrence)
    if not np.isfinite(annual_rate_of_occurrence) or annual_rate_of_occurrence < 0:
        raise ValueError("annual_rate_of_occurrence must be a finite non-negative number.")
    if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations <= 0:
        raise ValueError("iterations must be a positive integer.")

    rng = np.random.default_rng(seed)
    asset_values = rng.uniform(*asset_value_range, size=iterations)
    exposure_factors = rng.uniform(*exposure_factor_range, size=iterations)
    occurrences = rng.poisson(annual_rate_of_occurrence, size=iterations)

    sle = asset_values * exposure_factors
    ale = sle * occurrences
    return ale


def summarize(losses: np.ndarray) -> dict:
    losses = np.asarray(losses, dtype=float)
    if losses.size == 0:
        return {"p10": 0.0, "p50": 0.0, "expected": 0.0, "p90": 0.0, "p95": 0.0, "p99": 0.0}
    if not np.all(np.isfinite(losses)) or np.any(losses < 0):
        raise ValueError("losses must contain finite non-negative values.")
    return {
        "p10": float(np.percentile(losses, 10)),
        "p50": float(np.percentile(losses, 50)),
        "expected": float(np.mean(losses)),
        "p90": float(np.percentile(losses, 90)),
        "p95": float(np.percentile(losses, 95)),
        "p99": float(np.percentile(losses, 99)),
    }


def distribution_percentages(losses: np.ndarray, bins: int = 12) -> list[float]:
    """Return normalized histogram heights for a compact dashboard chart."""
    if not isinstance(bins, int) or bins <= 0:
        raise ValueError("bins must be a positive integer.")
    losses = np.asarray(losses, dtype=float)
    if losses.size == 0:
        return [0.0] * bins
    if not np.all(np.isfinite(losses)) or np.any(losses < 0):
        raise ValueError("losses must contain finite non-negative values.")
    counts, _ = np.histogram(losses, bins=bins)
    maximum = counts.max(initial=0)
    if maximum == 0:
        return [0.0] * bins
    return [round(float(count / maximum * 100), 1) for count in counts]
