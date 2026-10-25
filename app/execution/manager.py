from __future__ import annotations

from dataclasses import dataclass

from app.config import settings
from app.strategies.base import TradeSignal


@dataclass
class RiskCheck:
    allows_trade: bool
    reason: str


class ExecutionManager:
    def __init__(self, client):
        self.client = client

    def evaluate_risk(self, signal: TradeSignal) -> RiskCheck:
        if signal.action == "HOLD":
            return RiskCheck(False, "Hold signal does not require execution.")

        if signal.quantity is not None and signal.quantity > settings.max_position_size:
            return RiskCheck(False, f"Requested quantity {signal.quantity} exceeds max_position_size={settings.max_position_size}.")

        return RiskCheck(True, "Risk checks passed.")

    async def execute(self, signal: TradeSignal):
        risk = self.evaluate_risk(signal)
        if not risk.allows_trade:
            return {
                "status": "rejected",
                "symbol": signal.symbol,
                "action": signal.action,
                "reason": risk.reason,
            }

        if not settings.enable_live_trading:
            return {
                "status": "dry_run",
                "symbol": signal.symbol,
                "action": signal.action,
                "strategy": signal.strategy_name,
                "entry_price": signal.entry_price,
                "reason": "Live trading is disabled. This was a simulated execution only.",
            }

        result = await self.client.place_order(
            symbol=signal.symbol,
            side=signal.action,
            quantity=signal.quantity or settings.quantity,
            order_type=settings.order_type,
            price=signal.entry_price,
        )
        return {
            "status": "executed",
            "symbol": signal.symbol,
            "action": signal.action,
            "execution_result": result,
        }
