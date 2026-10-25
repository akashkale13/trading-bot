"""Strategy registry for the trading bot."""

from __future__ import annotations

from app.strategies.mean_reversion import MeanReversionStrategy
from app.strategies.momentum_breakout import MomentumBreakoutStrategy
from app.strategies.trend_following import TrendFollowingStrategy


def get_strategies() -> dict[str, object]:
    return {
        "trend_following": TrendFollowingStrategy(),
        "mean_reversion": MeanReversionStrategy(),
        "momentum_breakout": MomentumBreakoutStrategy(),
    }
