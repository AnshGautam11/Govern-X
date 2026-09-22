"""
Week 3, Day 3 code review: verify Monte Carlo risk math is statistically
sound, and the sample-data disclaimer remains documented.
"""

import numpy as np
from risk_engine.monte_carlo import run_monte_carlo, summarize
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
