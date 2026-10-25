from __future__ import annotations

from app.config import settings
from app.execution import ExecutionManager
from app.strategies.base import build_market_snapshot
from app.strategies.registry import get_strategies


class TradingAgent:
    def __init__(self, client):
        self.client = client
        self.executor = ExecutionManager(client)
        self.strategies = get_strategies()

    def choose_strategy(self, snapshot):
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

        payload = quote_payload
        if isinstance(quote_payload, list):
            payload = quote_payload[0] if quote_payload else {}
        elif isinstance(quote_payload, dict) and isinstance(quote_payload.get("data"), list):
            payload = quote_payload["data"][0] if quote_payload["data"] else {}
        elif hasattr(quote_payload, "content"):
            payload = getattr(quote_payload, "content")

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
