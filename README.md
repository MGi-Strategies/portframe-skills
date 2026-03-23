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

Paste one command in your terminal. Pick your editor:

**Claude Code** (Mac / Linux)
```bash
rm -rf /tmp/pf-skills ~/.claude/skills/portframe && git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && cp -r /tmp/pf-skills/skills/portframe ~/.claude/skills/portframe && rm -rf /tmp/pf-skills
```

**Cursor** (Mac / Linux)
```bash
rm -rf /tmp/pf-skills ~/.cursor/skills/portframe && git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && mkdir -p ~/.cursor/skills && cp -r /tmp/pf-skills/skills/portframe ~/.cursor/skills/portframe && rm -rf /tmp/pf-skills
```

**Cursor** (Windows PowerShell)
```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.cursor\skills\portframe" -ErrorAction SilentlyContinue; git clone https://github.com/MGi-Strategies/portframe-skills.git $env:TEMP\pf-skills; New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cursor\skills" | Out-Null; Copy-Item -Recurse "$env:TEMP\pf-skills\skills\portframe" "$env:USERPROFILE\.cursor\skills\portframe"; Remove-Item -Recurse -Force "$env:TEMP\pf-skills"
```

**Windsurf** (Mac / Linux)
```bash
rm -rf /tmp/pf-skills ~/.windsurf/skills/portframe && git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && mkdir -p ~/.windsurf/skills && cp -r /tmp/pf-skills/skills/portframe ~/.windsurf/skills/portframe && rm -rf /tmp/pf-skills
```

**Windsurf** (Windows PowerShell)
```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.windsurf\skills\portframe" -ErrorAction SilentlyContinue; git clone https://github.com/MGi-Strategies/portframe-skills.git $env:TEMP\pf-skills; New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.windsurf\skills" | Out-Null; Copy-Item -Recurse "$env:TEMP\pf-skills\skills\portframe" "$env:USERPROFILE\.windsurf\skills\portframe"; Remove-Item -Recurse -Force "$env:TEMP\pf-skills"
```

> **Cursor / Windsurf:** Start a new chat session after installing for the skill to be discovered.
>
> These editors also load skills from `~/.claude/skills/`, so the Claude Code command works for all three.

## Getting Started

1. Install using one of the commands above
2. Open your editor and ask your AI assistant to create a portfolio
3. On first use, a browser window will open for you to sign in to PortFrame
4. That's it — your token is saved locally and you're ready to go

## License

MIT
