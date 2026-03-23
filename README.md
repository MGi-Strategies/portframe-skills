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

### Option 1: Install from source

```bash
git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && pip install /tmp/pf-skills/mcp-server && python -m portframe_mcp.install && rm -rf /tmp/pf-skills
```

This installs the MCP server and auto-configures it for any detected IDEs (Cursor, Claude Code, Windsurf, VS Code).

### Option 2: Manual skill install (no MCP)

If you prefer the skill-only approach (uses curl instead of MCP):

**Claude Code** (Mac / Linux)
```bash
rm -rf /tmp/pf-skills ~/.claude/skills/portframe && git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && cp -r /tmp/pf-skills/skills/portframe ~/.claude/skills/portframe && rm -rf /tmp/pf-skills
```

**Cursor** (Mac / Linux)
```bash
rm -rf /tmp/pf-skills ~/.cursor/skills/portframe && git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && mkdir -p ~/.cursor/skills && cp -r /tmp/pf-skills/skills/portframe ~/.cursor/skills/portframe && rm -rf /tmp/pf-skills
```

> **Note:** The skill-only install uses curl for API calls, which may be blocked by Cursor's sandbox. The MCP install (Option 1) avoids this issue entirely.

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
