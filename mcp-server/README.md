# portframe-mcp

MCP server for PortFrame AI — create, backtest, and analyze investment portfolios from any AI coding assistant.

## Install

```bash
git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && pip install /tmp/pf-skills/mcp-server && python -m portframe_mcp.install && rm -rf /tmp/pf-skills
```

This installs the MCP server and auto-configures it for any detected IDEs (Cursor, Claude Code, Windsurf, VS Code).

## Tools

- **portframe_request** — Submit portfolio requests to PortFrame AI
- **portframe_check_status** — Poll for results (backtests can take 1-5 minutes)
- **portframe_list_sessions** — Continue previous conversations

## Authentication

On first use, the AI assistant will prompt you to authenticate:

```bash
python3 -m portframe_mcp.auth
```

This opens a browser for sign-in. Your token is saved locally at `~/.portframe/sessions.json`.

## Requirements

- Python 3.10+

## License

MIT
