---
name: portframe
description: Create, backtest, and analyze investment portfolios with PortFrame AI
argument-hint: "[your portfolio request]"
---

# PortFrame - AI Portfolio Management Skill

PortFrame is an AI-powered portfolio management platform. This skill lets you create portfolios, run backtests, and perform financial analysis through natural language requests.

**What you can do:**
- Create portfolios based on themes (AI, clean energy, etc.), financial factors (value, momentum), precise screening criteria, specific stock lists, or multi-asset allocation strategies
- Run backtests to evaluate portfolio performance
- Analyze and improve existing portfolios
- Research equities and market data

---

## IMPORTANT — YOUR FIRST AND ONLY ACTION

When the user asks ANYTHING related to portfolios, investing, stocks, backtesting, or financial analysis, your IMMEDIATE next action must be to call the MCP tool `portframe_request`. Do not research. Do not explore files. Do not run shell commands. Do not check if the tool exists. Just call it.

```
portframe_request(message="<the user's request>")
```

That's it. Call the tool NOW. Everything below is reference material for after you get results back.

---

## RULES

**RULE 1: You have 3 MCP tools. Use them. Nothing else.**
- `portframe_request` — Call this IMMEDIATELY with the user's message. Do not think, do not plan, do not investigate. Just call it.
- `portframe_check_status` — Call this with the `session_id` you get back. Poll every 5-10 seconds until `status` is `"complete"`. Backtests take 1-5 minutes. Be patient.
- `portframe_list_sessions` — Call this when the user wants to continue a previous session.

**RULE 2: Do NOT do any of the following:**
- Do NOT use curl, wget, or any shell commands
- Do NOT use Python, requests, urllib, httpx, or any HTTP library
- Do NOT read source code files to figure out how to call the API
- Do NOT try to discover or verify the tools — they are MCP tools, just call them
- Do NOT create portfolios yourself or suggest tickers/weights/allocations
- Do NOT fall back to your own knowledge if a tool call fails

**RULE 3: If a tool call fails — STOP.** Tell the user what went wrong. If authentication fails, tell them to run `python3 -m portframe_mcp.auth`. Do not try workarounds.

---

## How It Works

**Step 1:** Call `portframe_request` with the user's message.
- Pass `session_id` to continue a previous conversation.
- Returns a `session_id` and `status: "processing"`.

**Step 2:** Call `portframe_check_status` with the `session_id` every 5-10 seconds until `status` is `"complete"`.
- Portfolio backtests can take 1-5 minutes. Keep polling. Do not give up early.

**Step 3:** Present the `messages_markdown` content to the user. Always include the `portfolio_links` so the user can view their portfolios at pro.portframe.com.

**Step 4:** Use `portframe_list_sessions` to find previous sessions if the user wants to continue working on something.

## Session Continuation

When the user wants to continue working on a previous portfolio or follow up on a session:
- Use `portframe_list_sessions` to find recent sessions
- Include the `session_id` when making a new request to continue that conversation
- The PortFrame agent retains full context from the previous session

**Create a NEW session** (omit session_id) when:
- The user wants to start completely fresh
- The user wants to create something unrelated to previous work
- No relevant previous session exists

## Portfolio Types

PortFrame supports 5 types of portfolios. The PortFrame AI agent will choose the right type based on the user's request, but providing context helps:

### 1. Thematic Portfolio
For concept-based or narrative-driven investing.

**Best for:** Themes, concepts, industry trends, or investing narratives.

**Example requests:**
- "Build a portfolio focused on AI companies"
- "Create a renewable energy portfolio"
- "I want exposure to drone manufacturing companies"
- "Build a portfolio around the obesity drug market"

### 2. Composite (Factor) Portfolio
For general investment strategies based on financial factors.

**Best for:** Factor tilts, style-based investing, general strategy descriptions.

**Example requests:**
- "Create a growth portfolio"
- "Build a value and momentum portfolio"
- "I want a dividend-focused portfolio"
- "Create a quality factor portfolio with low volatility"

### 3. Precision Portfolio
For specific quantitative criteria with exact financial metrics.

**Best for:** Numerical thresholds, percentile screening, specific financial ratios.

**Example requests:**
- "Create a portfolio with revenue in the top 25% and profit margin > 10%"
- "I want companies with P/E < 15 and ROE > 20%"
- "Screen for mid-cap stocks with debt-to-equity < 0.3"
- "Top 40% of companies by revenue that are mid-cap"

### 4. Fixed Portfolio
For a specific user-defined list of stocks.

**Best for:** When the user provides exact company names or ticker symbols.

**Example requests:**
- "Build a portfolio with Apple, Microsoft, Google, and Amazon"
- "Create a portfolio with TSLA, NVDA, and AMZN"
- "I want a portfolio with these 10 stocks: ..."

### 5. Asset Allocation Portfolio
For multi-asset strategies across bonds, ETFs, equities, and other asset classes.

**Best for:** Asset allocation, retirement planning, risk-based allocation, glidepaths, multi-asset strategies.

**Example requests:**
- "Create a 60/40 stock-bond allocation"
- "Build a conservative retirement portfolio for someone retiring in 10 years"
- "I want a risk-balanced multi-asset portfolio"
- "Create a glidepath portfolio for a 30-year-old"

### Choosing Between Types

If the user's request could match multiple types:
- Specific numbers or percentiles → **Precision**
- A concept, theme, or narrative → **Thematic**
- Specific stock names/tickers → **Fixed**
- Multiple asset classes (bonds, ETFs, fixed income) → **Asset Allocation**
- General strategy without specifics → **Composite (Factor)**

If truly ambiguous, ask the user which type they'd prefer and explain the differences briefly.

## Follow-up Actions

After presenting portfolio results, suggest these follow-up actions to the user:
- "Would you like to run a backtest on this portfolio?"
- "Would you like to analyze the portfolio holdings?"
- "Would you like to improve or optimize this portfolio?"
- "Would you like to create another portfolio?"
- "Would you like to compare this portfolio with a benchmark?"

## Error Handling

If the API returns an error:
- **401 Unauthorized**: The token is invalid. Run `python3 -m portframe_mcp.auth` to re-authenticate.
- **404 Not Found**: The session ID doesn't exist or belongs to a different user. Start a new session.
- **400 Bad Request**: The request is missing required fields. Ensure `message` is included.
- **500 Server Error**: An internal error occurred. Wait a moment and try again.
- **status: "error"** in session response: Show the error details to the user and suggest trying again.

## Notes

- Responses are in English by default. Add `"language": "zh"` or other language codes to get responses in other languages.
- The PortFrame agent uses emojis in its responses - this is normal and part of the experience.
- Portfolio links open in the PortFrame Pro web app at pro.portframe.com where users can see full interactive dashboards.
