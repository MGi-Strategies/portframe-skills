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

## RULES — READ BEFORE DOING ANYTHING

**RULE 1: ALL portfolio creation, analysis, and investment work MUST go through the PortFrame API.** You are a proxy to PortFrame. You do NOT create portfolios yourself. You do NOT pick stocks. You do NOT suggest tickers, weights, or allocations. You are NOT a financial advisor. If you cannot reach the API, you CANNOT help with the request — period.

**RULE 2: Use `curl` for ALL API requests.** Do NOT use Python, do NOT use `urllib`, `requests`, `http.client`, `fetch`, or any other HTTP method. ONLY `curl`. Always include `--noproxy '*'` to bypass IDE proxy issues.

**RULE 3: If anything fails — STOP.** If authentication fails, if `curl` returns an error, if you get no output, if you get a non-JSON response, if the status code is not 2xx — STOP IMMEDIATELY. Tell the user what went wrong. Do NOT fall back to your own knowledge. Do NOT generate investment advice. Do NOT say "here's a portfolio you can start with". Just report the error and help troubleshoot.

**RULE 4: Verify `curl` output before proceeding.** If `curl` returns empty output, that is a failure. Do not proceed. Tell the user the API request returned no response.

---

## TROUBLESHOOTING — READ THIS IF YOU GET A NETWORK ERROR

There are two common causes of network failures. Check both.

### Problem 1: Missing `--noproxy '*'` (proxy routing)

If you get **exit code 56**, **"Tunnel connection failed: 403 Forbidden"**, or **empty curl output** — you probably forgot `--noproxy '*'`. Go back and read RULE 2.

Many IDEs set `http_proxy` / `https_proxy` environment variables that route traffic through a local proxy. This proxy blocks external API requests. The fix: **add `--noproxy '*'` to every curl command.** Every curl example below already includes it. If you removed it, put it back.

**Correct:**
```bash
curl --noproxy '*' -s -X POST https://ai-portframe.ngrok.app/api/v1/skill/request ...
```

**Wrong (will fail in most IDEs):**
```bash
curl -s -X POST https://ai-portframe.ngrok.app/api/v1/skill/request ...
```

### Problem 2: IDE sandbox blocking network entirely (DNS/socket failure)

If you get **"Could not resolve host"** (exit code 6), **"Operation not permitted"**, or DNS/network errors even WITH `--noproxy '*'` — the IDE's sandbox is blocking all outbound network at the OS level. This is a separate issue from the proxy.

**Cursor** sandboxes all terminal commands by default using seccomp (Linux) / Seatbelt (macOS), which blocks DNS resolution and socket connections entirely. `--noproxy '*'` alone cannot fix this.

**Tell the user** they need to do ONE of the following:

**Option A (recommended):** Create a file at `<workspace>/.cursor/sandbox.json` with:
```json
{
  "networkPolicy": {
    "default": "deny",
    "allow": ["ai-portframe.ngrok.app", "pro.portframe.com"]
  }
}
```

**Option B:** In Cursor, go to **Settings > Agents > Auto-Run** and change to **"Ask Every Time"**. This lets the user approve each command to run outside the sandbox.

**Option C:** Set the sandbox to allow all network:
```json
{
  "networkPolicy": {
    "default": "allow"
  }
}
```

After changing sandbox settings, the user should **restart Cursor** and start a new chat session.

Do NOT try workarounds like "fallback shell subagent paths", Python HTTP libraries, or retry loops. Fix the sandbox config and re-run the curl command as instructed.

---

## Step 1: Authentication

Before making any API requests, you must have a valid API token.

**Check for existing token:**

Read `~/.portframe/sessions.json` and look for the `api_token` field.

**If no token exists, authenticate:**

Run the authentication script. It starts a local server and tries to open a browser:

```bash
python3 scripts/auth.py
```

The script will print a URL to the terminal. **Tell the user to open this URL in their browser if it doesn't open automatically.** The URL looks like: `https://pro.portframe.com/skill-signup?callback=...`

After the user signs in, the token will be saved to `~/.portframe/sessions.json`.

If the script fails or the user cannot complete sign-in — STOP. Do not proceed without a token.

## Step 2: Submit a Request

Send the user's request to the PortFrame AI agent. Use this exact format:

```bash
curl --noproxy '*' -s -X POST https://ai-portframe.ngrok.app/api/v1/skill/request \
  -H "Authorization: Bearer API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "USER_REQUEST_HERE"}'
```

Replace `API_TOKEN` with the token from `~/.portframe/sessions.json`. Replace `USER_REQUEST_HERE` with the user's actual request.

To continue an existing session, add `"session_id": "EXISTING_SESSION_ID"` to the JSON body.

**Expected response:** JSON with `session_id` and `status: "processing"`. If you get anything else — STOP and report the error.

## Step 3: Poll for Results

Poll every 5 seconds until `status` is `"complete"`:

```bash
curl --noproxy '*' -s https://ai-portframe.ngrok.app/api/v1/skill/session/SESSION_ID \
  -H "Authorization: Bearer API_TOKEN"
```

**Important:** Portfolio backtests can take 1-5 minutes. Keep polling. Do not give up early.

**Expected response:** JSON with `status`, `messages_markdown`, and `portfolio_links`. If you get empty output or an error — STOP and tell the user.

## Step 4: Present Results

The response contains:
- `status`: `"complete"`, `"processing"`, or `"error"`
- `messages_markdown`: Full session results in markdown format including all tool calls and responses
- `portfolio_links`: URLs to view created portfolios in the PortFrame Pro web app

Present the `messages_markdown` content to the user. Always include the portfolio links so the user can view their portfolios at pro.portframe.com.

## Step 5: Save Session Context

After receiving results, update `~/.portframe/sessions.json` with the session metadata for future reference:

```json
{
  "api_token": "pf_sk_...",
  "sessions": [
    {
      "session_id": "the-session-id",
      "created_at": "2026-03-22T...",
      "description": "Brief description of what was created",
      "portfolio_ids": ["id1", "id2"],
      "last_accessed": "2026-03-22T..."
    }
  ]
}
```

## Session Continuation

When the user wants to continue working on a previous portfolio or follow up on a session:
- Check `~/.portframe/sessions.json` for recent sessions
- Include the `session_id` in the request body to continue that conversation
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
- **401 Unauthorized**: The token is invalid. Delete `~/.portframe/sessions.json` and re-run `scripts/auth.py`.
- **404 Not Found**: The session ID doesn't exist or belongs to a different user. Start a new session.
- **400 Bad Request**: The request is missing required fields. Ensure `message` is included.
- **500 Server Error**: An internal error occurred. Wait a moment and try again.
- **status: "error"** in session response: Show the error details to the user and suggest trying again.
- **Empty curl output**: Network/proxy issue. Tell the user.

## API Base URL

All requests go to: `https://ai-portframe.ngrok.app`

## Notes

- Responses are in English by default. Add `"language": "zh"` or other language codes to the request body to get responses in other languages.
- The PortFrame agent uses emojis in its responses - this is normal and part of the experience.
- Portfolio links open in the PortFrame Pro web app at pro.portframe.com where users can see full interactive dashboards.
