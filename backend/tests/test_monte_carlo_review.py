"""
Week 3, Day 3 code review: verify Monte Carlo risk math is statistically
sound, and the sample-data disclaimer remains documented.
"""

import numpy as np
from risk_engine.monte_carlo import run_monte_carlo, summarize
from risk_engine.mock_data import MOCK_ASSET_DATA
