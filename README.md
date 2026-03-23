# PortFrame Skills

AI agent skills for [PortFrame](https://portframe.com) — create, backtest, and analyze investment portfolios through natural language.

## Available Skills

| Skill | Description |
|-------|-------------|
| **portframe** | Create portfolios, run backtests, research equities, and perform financial analysis |

## Installation

### Claude Code (Plugin Marketplace)

```
/plugin marketplace add MGi-Strategies/portframe-skills
/plugin install portframe@portframe-skills
```

### Claude Code (Manual)

Copy the skill directory to your Claude Code skills folder:

```bash
cp -r skills/portframe ~/.claude/skills/portframe
```

Or add it to your project:

```bash
cp -r skills/portframe .claude/skills/portframe
```

### Other AI Agents

Copy the `skills/portframe/SKILL.md` file to your agent's skill directory. The skill follows the [Agent Skills](https://agentskills.io) open standard and is compatible with any platform that supports `SKILL.md` files.

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
│       ├── SKILL.md          # Skill instructions
│       └── scripts/
│           └── auth.py       # Authentication script
├── README.md
└── LICENSE
```

## License

MIT
