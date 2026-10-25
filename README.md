# AI Trading Agent for Zerodha Kite MCP

This repository is a starter for an AI-driven trading agent that:
- connects to the Zerodha Kite MCP server,
- fetches live quotes for symbols,
- evaluates market conditions with configurable strategies,
- decides which strategy to apply under your control,
- generates a trade decision,
- optionally executes the trade through the Kite MCP server.

The design is deliberately conservative:
- market data comes from Kite MCP,
- strategy selection is explicit and controllable,
- order execution is disabled by default unless you explicitly enable live trading,
- all trading credentials must be stored in environment variables and never committed to Git.

## Architecture

- `app/config.py` — settings and environment configuration
- `app/zerodha_client.py` — MCP client wrapper for Kite
- `app/strategies.py` — strategy implementations and signal generation
- `app/agent.py` — AI / rule-based decision engine
- `app/execution.py` — broker order execution layer
- `main.py` — CLI entry point

## Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

3. Review the values in `.env`.

4. Dry-run a sample quote analysis:

```bash
python main.py --symbol NIFTY 50 --dry-run
```

The repo is intentionally safe by default. The agent will not place a live trade unless you explicitly enable execution and provide a valid Kite account configuration.

## Required Kite MCP setup

You should point the agent at the Kite MCP endpoint you are using. The official Zerodha MCP integration is documented here:

- https://zerodha.com/z-connect/featured/connect-your-zerodha-account-to-ai-assistants-with-kite-mcp
- https://github.com/zerodha/kite-mcp-server

The exact tool names exposed by the MCP server may vary by version. This project supports environment-based configuration for the quote and order tools so you can map the real tool names from your connected server.

## Safe execution policy

This starter enforces guardrails:
- no live trade execution unless `ENABLE_LIVE_TRADING=true`
- order quantity is validated against `MAX_POSITION_SIZE`
- daily loss limits are enforced in the execution layer
- a strategy must produce a valid action (BUY/SELL/HOLD)

## Future extension

This repo can later be extended with:
- OpenAI / Azure OpenAI reasoning layer
- portfolio-level risk engine
- watchlist-based scanning
- multi-symbol automation
- paper trading mode
- webhook / dashboard notifications

## Important

This repository is a template and does not guarantee live-trading correctness. Always test in paper mode or with very small quantities before using real capital.
