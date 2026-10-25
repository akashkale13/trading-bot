"""Common trading market model classes."""

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
