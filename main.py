from __future__ import annotations

from app.config import settings
from app.execution import ExecutionManager
from app.strategies import (
    MeanReversionStrategy,
    MomentumBreakoutStrategy,
    Strategy,
    TradeSignal,
    TrendFollowingStrategy,
    build_market_snapshot,
)


class TradingAgent:
    def __init__(self, client):
        self.client = client
        self.executor = ExecutionManager(client)
        self.strategies: dict[str, Strategy] = {
            "trend_following": TrendFollowingStrategy(),
            "mean_reversion": MeanReversionStrategy(),
            "momentum_breakout": MomentumBreakoutStrategy(),
        }

    def choose_strategy(self, snapshot) -> Strategy:
        if settings.strategy_mode == "rule_based":
            if snapshot.volatility is not None and snapshot.volatility > 0.015:
                return self.strategies["momentum_breakout"]
            if snapshot.trend_strength > 0.02:
                return self.strategies["trend_following"]
            return self.strategies["mean_reversion"]

        strategy_name = settings.default_strategy
        return self.strategies.get(strategy_name, self.strategies["trend_following"])

    async def analyze_symbol(self, symbol: str):
        quote_payload = await self.client.get_quote(symbol)

        if isinstance(quote_payload, dict):
            payload = quote_payload
        elif hasattr(quote_payload, "content"):
            payload = getattr(quote_payload, "content")
        else:
            payload = {"last_price": 0.0}

        snapshot = build_market_snapshot(symbol, payload)
        strategy = self.choose_strategy(snapshot)
        signal = strategy.evaluate(snapshot)
        signal.quantity = settings.quantity

        if signal.action == "HOLD":
            return {"status": "hold", "symbol": symbol, "signal": signal}

        return await self.executor.execute(signal)

    async def analyze_watchlist(self):
        results = []
        for symbol in [item.strip() for item in settings.watchlist.split(",") if item.strip()]:
            results.append(await self.analyze_symbol(symbol))
        return results

