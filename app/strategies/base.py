from __future__ import annotations

from typing import Any

from mcp import Client

from app.market.provider import MarketDataProvider


class ZerodhaMCPClient(MarketDataProvider):
    """Concrete market data and execution provider for Zerodha Kite MCP."""

    def __init__(self, base_url: str, quote_tool: str = "get_quotes", order_tool: str = "place_order"):
        self.base_url = base_url
        self.quote_tool = quote_tool
        self.order_tool = order_tool
        self.session = None
        self._client: Client | None = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def connect(self):
        self._client = Client(self.base_url)
        self.session = await self._client.__aenter__()

    async def disconnect(self):
        if self._client is not None:
            await self._client.__aexit__(None, None, None)
            self._client = None
        self.session = None

    async def list_tools(self):
        if self.session is None:
            raise RuntimeError("MCP client is not connected.")
        response = await self.session.list_tools()
        return response.tools if hasattr(response, "tools") else response

    async def call_tool(self, tool_name: str, arguments: dict[str, Any] | None = None):
        if self.session is None:
            raise RuntimeError("MCP client is not connected.")
        payload = arguments or {}
        return await self.session.call_tool(tool_name, payload)

    @staticmethod
    def normalize_symbol(symbol: str) -> str:
        cleaned = symbol.strip()
        if not cleaned:
            raise ValueError("Empty symbol provided.")
        if ":" in cleaned:
            return cleaned
        return f"NSE:{cleaned.upper()}"

    async def get_quote(self, symbol: str) -> dict[str, Any]:
        normalized_symbol = self.normalize_symbol(symbol)
        tool_names = [self.quote_tool, "get_quotes", "get_quote", "quote", "ltp", "market_quote"]

        last_error: Exception | None = None
        for tool_name in tool_names:
            if not tool_name:
                continue
            try:
                return await self.call_tool(tool_name, {"instruments": [normalized_symbol]})
            except Exception as exc:
                last_error = exc
                continue

        raise RuntimeError(
            f"Unable to resolve quote data for {symbol} using Kite MCP tool names. "
            f"Last error: {last_error}"
        )

    async def place_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "LIMIT",
        price: float | None = None,
    ) -> dict[str, Any]:
        for tool_name in [self.order_tool, "place_order", "create_order", "order_place"]:
            if not tool_name:
                continue
            try:
                return await self.call_tool(
                    tool_name,
                    {
                        "symbol": symbol,
                        "side": side,
                        "quantity": quantity,
                        "order_type": order_type,
                        "price": price,
                    },
                )
            except Exception:
                continue
        raise RuntimeError(f"Unable to place order through Kite MCP for {symbol}. Check server tooling and env vars.")
