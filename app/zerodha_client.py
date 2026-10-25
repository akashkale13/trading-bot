from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Action = Literal["BUY", "SELL", "HOLD"]


@dataclass
class TradeSignal:
    symbol: str
    action: Action
    confidence: float
    reason: str
    strategy_name: str
    entry_price: float | None = None
    stop_loss: float | None = None
    target: float | None = None
    quantity: int | None = None


@dataclass
class MarketSnapshot:
    symbol: str
    last_price: float
    previous_close: float
    ma_20: float | None = None
    ma_50: float | None = None
    volume: float | None = None
    volatility: float | None = None
    rsi: float | None = None

    @property
    def trend_strength(self) -> float:
        if self.ma_20 is None or self.ma_50 is None:
            return 0.0
        if self.ma_50 == 0:
            return 0.0
        return (self.ma_20 - self.ma_50) / self.ma_50


class Strategy:
    name: str = "base"

    def evaluate(self, snapshot: MarketSnapshot) -> TradeSignal:
        raise NotImplementedError


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


def build_market_snapshot(symbol: str, quote_payload: dict) -> MarketSnapshot:
    price = float(quote_payload.get("last_price", quote_payload.get("ltp", 0.0)))
    previous_close = float(quote_payload.get("previous_close", price))
    ma_20 = quote_payload.get("ma_20")
    ma_50 = quote_payload.get("ma_50")
    volume = quote_payload.get("volume")
    volatility = quote_payload.get("volatility")
    rsi = quote_payload.get("rsi")

    return MarketSnapshot(
        symbol=symbol,
        last_price=price,
        previous_close=previous_close,
        ma_20=float(ma_20) if ma_20 is not None else None,
        ma_50=float(ma_50) if ma_50 is not None else None,
        volume=float(volume) if volume is not None else None,
        volatility=float(volatility) if volatility is not None else None,
        rsi=float(rsi) if rsi is not None else None,
    )
