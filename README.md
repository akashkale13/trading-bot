# AI Trading Bot

This repository is a modular trading bot framework designed to make it easy to connect a live market data provider, run strategy evaluation, validate risk, and optionally execute trades.

The current default provider is Zerodha via the Kite MCP server, but the system is intentionally built so that other providers can be plugged in later without changing the strategy and execution layers.

## What this repo includes

- live market data integration layer
- strategy evaluation modules
- risk guardrails and execution safety checks
- a simple agent/orchestrator that chooses the strategy based on market conditions
- a dry-run default mode so live trading is never enabled by accident

## Current architecture

- `app/market/` — provider abstraction and market adapters
  - `provider.py` — common interface for market providers
  - `zerodha.py` — Zerodha Kite MCP implementation
- `app/strategies/` — strategy implementations and registration
  - `base.py` — shared model definitions and strategy contract
  - `trend_following.py`
  - `mean_reversion.py`
  - `momentum_breakout.py`
  - `registry.py`
- `app/agent.py` — orchestration layer selecting strategy and processing signals
- `app/execution.py` — order execution and risk validation
- `app/config.py` — application configuration and environment variables
- `main.py` — CLI entry point

## Why this structure

This repo is not limited to Kite MCP. It is designed around a provider pattern:

- The market data provider is abstracted behind a common interface
- Strategies only care about market snapshots and signal output
- The execution layer can be swapped or extended independently
- A future provider such as Polygon, Alpaca, or another broker can be added by implementing the same interface

This makes the bot easier to evolve without mixing broker-specific logic into strategy code.

## Default provider: Zerodha Kite MCP

The default implementation currently connects to Zerodha through the Kite MCP server.

Official references:
- https://zerodha.com/z-connect/featured/connect-your-zerodha-account-to-ai-assistants-with-kite-mcp
- https://github.com/zerodha/kite-mcp-server

## Quick start

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example env file:

```bash
cp .env.example .env
```

4. Update `.env` with your provider and execution settings.

5. Run a dry-run example:

```bash
python main.py --symbol "NIFTY 50" --dry-run
```

## Safety defaults

This repository is intentionally conservative:

- live trading is disabled by default
- strategy selection is rule-driven by default
- position size is capped by configuration
- execution checks reject invalid or unsafe trade actions
- credentials should never be committed to Git

## Future extension ideas

- add a paper trading mode
- add more strategies
- add portfolio-level risk checks
- add watchlist scanning
- add backtesting and simulation mode
- add LLM-based decision support while keeping trade execution rules strict

## Important

This project is a framework and starter implementation, not a guarantee of profitable live trading. Always validate in dry-run, paper trading, or very small quantities before using real capital.
