"""Mean reversion strategy."""

from __future__ import annotations

from app.strategies.base import MarketSnapshot, Strategy, TradeSignal


class MeanReversionStrategy(Strategy):
    name = "mean_reversion"

    def evaluate(self, snapshot: MarketSnapshot) -> TradeSignal:
        if snapshot.ma_20 is None:
            return TradeSignal(
                symbol=snapshot.symbol,
                action="HOLD",
                confidence=0.0,
                reason="Insufficient moving-average information for mean reversion.",
                strategy_name=self.name,
            )

        spread = snapshot.last_price - snapshot.ma_20
        if spread < -0.02 * snapshot.ma_20:
            return TradeSignal(
                symbol=snapshot.symbol,
                action="BUY",
                confidence=0.68,
                reason="Price is materially below its short moving average, suggesting a reversion opportunity.",
                strategy_name=self.name,
                entry_price=snapshot.last_price,
                stop_loss=snapshot.last_price * 0.97,
                target=snapshot.last_price * 1.03,
            )

        if spread > 0.02 * snapshot.ma_20:
            return TradeSignal(
                symbol=snapshot.symbol,
                action="SELL",
                confidence=0.68,
                reason="Price is materially above its short moving average, suggesting a mean-reversion sell.",
                strategy_name=self.name,
                entry_price=snapshot.last_price,
                stop_loss=snapshot.last_price * 1.03,
                target=snapshot.last_price * 0.97,
            )

        return TradeSignal(
            symbol=snapshot.symbol,
            action="HOLD",
            confidence=0.35,
            reason="Price is close to its mean; no strong reversion signal.",
            strategy_name=self.name,
        )
