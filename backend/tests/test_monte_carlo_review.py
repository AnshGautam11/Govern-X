"""
Week 3, Day 3 code review: verify Monte Carlo risk math is statistically
sound, and the sample-data disclaimer remains documented.
"""

import numpy as np
import pytest
from risk_engine.monte_carlo import distribution_percentages, run_monte_carlo, summarize
from risk_engine.mock_data import MOCK_ASSET_DATA


def test_disclaimer_still_documented():
    """The sample-data disclaimer must never be silently removed."""
    content = open("risk_engine/monte_carlo.py", encoding="utf-8").read()
    assert "sample" in content.lower() or "assumed" in content.lower()
    assert "not real" in content.lower()


def test_monte_carlo_percentiles_are_ordered():
    for sector, params in MOCK_ASSET_DATA.items():
        losses = run_monte_carlo(
            asset_value_range=params["asset_value_range"],
            exposure_factor_range=params["exposure_factor_range"],
            annual_rate_of_occurrence=params["annual_rate_of_occurrence"],
            iterations=5_000,
            seed=42,
        )
        result = summarize(losses)
        assert result["p10"] <= result["expected"] <= result["p90"], sector
        assert result["p10"] >= 0, sector


def test_monte_carlo_within_plausible_bounds():
    for sector, params in MOCK_ASSET_DATA.items():
        losses = run_monte_carlo(
            asset_value_range=params["asset_value_range"],
            exposure_factor_range=params["exposure_factor_range"],
            annual_rate_of_occurrence=params["annual_rate_of_occurrence"],
            iterations=5_000,
            seed=42,
        )
        result = summarize(losses)
        max_possible = (
            params["asset_value_range"][1]
            * params["exposure_factor_range"][1]
            * (params["annual_rate_of_occurrence"] + 4)
        )
        assert result["p90"] < max_possible, sector


def test_monte_carlo_zero_exposure_or_occurrence_has_zero_loss():
    losses = run_monte_carlo((0, 1_000_000), (0, 0), 4, iterations=50, seed=1)
    assert np.all(losses == 0)
    assert summarize(losses)["p99"] == 0

    no_occurrences = run_monte_carlo((100, 100), (0.5, 0.5), 0, iterations=50, seed=1)
    assert np.all(no_occurrences == 0)


def test_monte_carlo_empty_summaries_are_zero_and_keep_distribution_shape():
    assert summarize(np.array([])) == {
        "p10": 0.0,
        "p50": 0.0,
        "expected": 0.0,
        "p90": 0.0,
        "p95": 0.0,
        "p99": 0.0,
    }
    assert distribution_percentages(np.array([]), bins=5) == [0.0] * 5


@pytest.mark.parametrize(
    "kwargs",
    [
        {"asset_value_range": (-1, 2)},
        {"asset_value_range": (2, 1)},
        {"exposure_factor_range": (0, 1.1)},
        {"annual_rate_of_occurrence": -0.1},
        {"iterations": 0},
    ],
)
def test_monte_carlo_rejects_invalid_inputs(kwargs):
    parameters = {
        "asset_value_range": (1, 2),
        "exposure_factor_range": (0, 1),
        "annual_rate_of_occurrence": 1,
        "iterations": 10,
    }
    parameters.update(kwargs)
    with pytest.raises(ValueError):
        run_monte_carlo(**parameters)


def test_summary_includes_requested_loss_percentiles():
    result = summarize(np.arange(1, 101, dtype=float))
    assert result["p10"] <= result["p50"] <= result["p90"] <= result["p95"] <= result["p99"]
