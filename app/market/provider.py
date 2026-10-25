from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MarketDataProvider(ABC):
    """Interface for any market-data provider such as Zerodha, Polygon, Alpaca, etc."""

    @abstractmethod
    async def get_quote(self, symbol: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def place_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "LIMIT",
        price: float | None = None,
    ) -> dict[str, Any]:
        raise NotImplementedError
