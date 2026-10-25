"""Momentum breakout strategy."""

from __future__ import annotations

from app.strategies.base import MarketSnapshot, Strategy, TradeSignal


class MomentumBreakoutStrategy(Strategy):
    name = "momentum_breakout"

    def evaluate(self, snapshot: MarketSnapshot) -> TradeSignal:
        if snapshot.last_price <= 0 or snapshot.previous_close <= 0:
            return TradeSignal(
                symbol=snapshot.symbol,
                action="HOLD",
                confidence=0.0,
                reason="Invalid price data for breakout testing.",
                strategy_name=self.name,
            )

        breakout_pct = (snapshot.last_price - snapshot.previous_close) / snapshot.previous_close
        if breakout_pct > 0.012:
            return TradeSignal(
                symbol=snapshot.symbol,
                action="BUY",
                confidence=0.7,
                reason="Price is breaking above previous close with bullish momentum.",
                strategy_name=self.name,
                entry_price=snapshot.last_price,
                stop_loss=snapshot.last_price * 0.985,
                target=snapshot.last_price * 1.05,
            )

        if breakout_pct < -0.012:
            return TradeSignal(
                symbol=snapshot.symbol,
                action="SELL",
                confidence=0.7,
                reason="Price is breaking below previous close with bearish momentum.",
                strategy_name=self.name,
                entry_price=snapshot.last_price,
                stop_loss=snapshot.last_price * 1.015,
                target=snapshot.last_price * 0.95,
            )

        return TradeSignal(
            symbol=snapshot.symbol,
            action="HOLD",
            confidence=0.3,
            reason="No strong breakout momentum detected.",
            strategy_name=self.name,
        )
