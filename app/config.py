from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    kite_mcp_url: str = "https://mcp.kite.trade/mcp"
    kite_mcp_quote_tool: str = "get_quote"
    kite_mcp_order_tool: str = "place_order"

    enable_live_trading: bool = False
    environment: str = "development"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    default_strategy: str = "trend_following"
    strategy_mode: str = "rule_based"

    max_position_size: int = 1
    max_daily_loss_percent: float = 2.0
    max_drawdown_percent: float = 5.0

    watchlist: str = "NIFTY 50,RELIANCE,INFY"
    alert_symbol: str = "NIFTY 50"

    order_type: str = "LIMIT"
    quantity: int = 1
    ttl_seconds: int = 60


settings = Settings()
