# PortFrame Skills

AI agent skills for [PortFrame](https://portframe.com) — create, backtest, and analyze investment portfolios through natural language.

Built on the [Agent Skills](https://agentskills.io) open standard. Works with Claude Code, Cursor, Windsurf, GitHub Copilot, and any SKILL.md-compatible platform.

## Available Skills

| Skill | Description |
|-------|-------------|
| **portframe** | Create portfolios, run backtests, research equities, and perform financial analysis |

## Quick Install (One-Liner)

### Claude Code

```bash
# Linux / macOS
git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && cp -r /tmp/pf-skills/skills/portframe ~/.claude/skills/portframe && rm -rf /tmp/pf-skills

# Or use the plugin marketplace
# /plugin marketplace add MGi-Strategies/portframe-skills
# /plugin install portframe@portframe-skills
```

### Cursor

```bash
# Linux / macOS
git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && mkdir -p ~/.cursor/skills && cp -r /tmp/pf-skills/skills/portframe ~/.cursor/skills/portframe && rm -rf /tmp/pf-skills

# Windows (PowerShell)
git clone https://github.com/MGi-Strategies/portframe-skills.git $env:TEMP\pf-skills; New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cursor\skills"; Copy-Item -Recurse "$env:TEMP\pf-skills\skills\portframe" "$env:USERPROFILE\.cursor\skills\portframe"; Remove-Item -Recurse -Force "$env:TEMP\pf-skills"
```

### Windsurf

```bash
# Linux / macOS
git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && mkdir -p ~/.windsurf/skills && cp -r /tmp/pf-skills/skills/portframe ~/.windsurf/skills/portframe && rm -rf /tmp/pf-skills

# Windows (PowerShell)
git clone https://github.com/MGi-Strategies/portframe-skills.git $env:TEMP\pf-skills; New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.windsurf\skills"; Copy-Item -Recurse "$env:TEMP\pf-skills\skills\portframe" "$env:USERPROFILE\.windsurf\skills\portframe"; Remove-Item -Recurse -Force "$env:TEMP\pf-skills"
```

### GitHub Copilot

```bash
# Linux / macOS — copies skill as custom instructions
git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && mkdir -p .github && cp /tmp/pf-skills/skills/portframe/SKILL.md .github/copilot-instructions.md && cp -r /tmp/pf-skills/skills/portframe/scripts .github/portframe-scripts && rm -rf /tmp/pf-skills

# Windows (PowerShell)
git clone https://github.com/MGi-Strategies/portframe-skills.git $env:TEMP\pf-skills; New-Item -ItemType Directory -Force -Path ".github"; Copy-Item "$env:TEMP\pf-skills\skills\portframe\SKILL.md" ".github\copilot-instructions.md"; Copy-Item -Recurse "$env:TEMP\pf-skills\skills\portframe\scripts" ".github\portframe-scripts"; Remove-Item -Recurse -Force "$env:TEMP\pf-skills"
```

### Project-Level (Any Tool)

Add the skill directly to your project so all contributors get it:

```bash
# Claude Code
git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && mkdir -p .claude/skills && cp -r /tmp/pf-skills/skills/portframe .claude/skills/portframe && rm -rf /tmp/pf-skills

# Cursor
git clone https://github.com/MGi-Strategies/portframe-skills.git /tmp/pf-skills && mkdir -p .cursor/skills && cp -r /tmp/pf-skills/skills/portframe .cursor/skills/portframe && rm -rf /tmp/pf-skills
```

## Usage

Once installed, invoke the skill:

```
/portframe Build a portfolio focused on AI companies
```

Or just ask your agent to create a portfolio — it will automatically use the skill.

### First-Time Setup

On first use, the skill will open your browser to authenticate with PortFrame. This generates an API token stored locally at `~/.portframe/sessions.json`. No keys are stored in this repo.

### What You Can Do

- **Thematic portfolios** — "Build a portfolio around clean energy"
- **Factor portfolios** — "Create a value and momentum portfolio"
- **Precision portfolios** — "Companies with P/E < 15 and ROE > 20%"
- **Fixed portfolios** — "Build a portfolio with AAPL, MSFT, GOOGL"
- **Asset allocation** — "Create a 60/40 stock-bond allocation"
- **Backtesting** — "Backtest this portfolio over the last 5 years"
- **Research** — "Research NVIDIA's fundamentals"

## Repository Structure

```
portframe-skills/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace registry
├── skills/
│   └── portframe/
│       ├── SKILL.md          # Skill instructions (Agent Skills standard)
│       └── scripts/
│           └── auth.py       # Authentication script (Python stdlib only)
├── README.md
└── LICENSE
```

## Compatibility

| Platform | Install Location | Status |
|----------|-----------------|--------|
| Claude Code | `~/.claude/skills/` | Fully supported |
| Cursor | `~/.cursor/skills/` | Fully supported |
| Windsurf | `~/.windsurf/skills/` | Fully supported |
| GitHub Copilot | `.github/copilot-instructions.md` | Works as custom instructions |
| OpenClaw | `skills/` | Compatible |
| Any SKILL.md platform | Varies | Compatible (agentskills.io standard) |

## License

MIT
