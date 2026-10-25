"""Trend following strategy."""

from __future__ import annotations

from app.strategies.base import MarketSnapshot, Strategy, TradeSignal


class TrendFollowingStrategy(Strategy):
    name = "trend_following"

    def evaluate(self, snapshot: MarketSnapshot) -> TradeSignal:
        if snapshot.ma_20 is None or snapshot.ma_50 is None:
            return TradeSignal(
                symbol=snapshot.symbol,
                action="HOLD",
                confidence=0.0,
                reason="Insufficient moving-average data for trend-following strategy.",
                strategy_name=self.name,
            )

        if snapshot.last_price > snapshot.ma_20 and snapshot.ma_20 > snapshot.ma_50:
            return TradeSignal(
                symbol=snapshot.symbol,
                action="BUY",
                confidence=0.72,
                reason="Price is above short and long moving averages, indicating bullish momentum.",
                strategy_name=self.name,
                entry_price=snapshot.last_price,
                stop_loss=snapshot.last_price * 0.98,
                target=snapshot.last_price * 1.04,
            )

        if snapshot.last_price < snapshot.ma_20 and snapshot.ma_20 < snapshot.ma_50:
            return TradeSignal(
                symbol=snapshot.symbol,
                action="SELL",
                confidence=0.72,
                reason="Price is below short and long moving averages, indicating bearish momentum.",
                strategy_name=self.name,
                entry_price=snapshot.last_price,
                stop_loss=snapshot.last_price * 1.02,
                target=snapshot.last_price * 0.96,
            )

        return TradeSignal(
            symbol=snapshot.symbol,
            action="HOLD",
            confidence=0.4,
            reason="Trend is neutral; no strong directional conviction.",
            strategy_name=self.name,
        )
