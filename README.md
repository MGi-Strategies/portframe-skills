# PortFrame Skills

Give your AI coding assistant the power to create, backtest, and analyze investment portfolios — just by asking.

## What Can It Do?

- "Build me a portfolio focused on AI companies"
- "Create a value and momentum portfolio"
- "Find companies with P/E < 15 and ROE > 20%"
- "Build a portfolio with AAPL, MSFT, GOOGL"
- "Create a 60/40 stock-bond allocation"
- "Backtest this portfolio over the last 5 years"
- "Research NVIDIA's fundamentals"

## Install

**Requires:** Python 3.10+

### Cursor / Windsurf / VS Code (MCP server)

```bash
git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && python3 -m pip install /tmp/pf-skills/mcp-server && python3 -m portframe_mcp.install && rm -rf /tmp/pf-skills
```

This installs the MCP server and auto-configures it for any detected IDEs. Run this from inside your project directory so the project-level config gets written too.

### Claude Code

```bash
git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && python3 -m pip install /tmp/pf-skills/mcp-server && python3 -m portframe_mcp.install && rm -rf /tmp/pf-skills
```

The installer auto-detects Claude Code and registers the MCP server via `claude mcp add`. You can also install the skill directly:

```bash
rm -rf /tmp/pf-skills ~/.claude/skills/portframe && git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && cp -r /tmp/pf-skills/skills/portframe ~/.claude/skills/portframe && rm -rf /tmp/pf-skills
```

## Getting Started

1. Install using one of the methods above
2. Restart your IDE and start a new chat session
3. Ask your AI assistant to create a portfolio
4. On first use, you'll be prompted to sign in to PortFrame
5. That's it — your token is saved locally and you're ready to go

## How It Works

The MCP server provides 3 tools to your AI assistant:
- **portframe_request** — Submit portfolio requests to PortFrame AI
- **portframe_check_status** — Poll for results (backtests can take 1-5 minutes)
- **portframe_list_sessions** — Continue previous conversations

The MCP server runs outside the IDE sandbox, so it works reliably in Cursor, Claude Code, and other editors without network configuration issues.

## License

MIT
