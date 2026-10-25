from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TradeOrder:
    symbol: str
    side: str
    quantity: int
    order_type: str = "LIMIT"
    price: float | None = None
    exchange: str | None = None
