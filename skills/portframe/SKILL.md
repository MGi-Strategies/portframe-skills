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
- `messages_markdown`: Full session results in markdown
- `portfolio_links`: URLs to view portfolios in the PortFrame Pro web app

Present the `messages_markdown` content to the user. Always include the portfolio links so the user can view their portfolios at pro.portframe.com.

## Step 5: Save Session Context

After receiving results, update `~/.portframe/sessions.json` with the session metadata:

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

When the user wants to continue working on a previous portfolio or follow up:
- Check `~/.portframe/sessions.json` for recent sessions
- Include the `session_id` in the request body to continue that conversation

**Create a NEW session** (omit session_id) when the user wants something unrelated.

## Portfolio Types

PortFrame supports 5 types. The PortFrame AI agent chooses the right type, but context helps:

1. **Thematic** — concept-based: "AI companies", "clean energy", "obesity drugs"
2. **Composite (Factor)** — strategy-based: "growth portfolio", "value + momentum"
3. **Precision** — quantitative: "P/E < 15 and ROE > 20%", "top 25% by revenue"
4. **Fixed** — specific stocks: "AAPL, MSFT, GOOGL, AMZN"
5. **Asset Allocation** — multi-asset: "60/40 stock-bond", "retirement glidepath"

## Follow-up Actions

After presenting results, suggest:
- "Would you like to run a backtest on this portfolio?"
- "Would you like to analyze the portfolio holdings?"
- "Would you like to create another portfolio?"

## Error Handling

- **401 Unauthorized**: Token invalid. Delete `~/.portframe/sessions.json` and re-run `scripts/auth.py`.
- **404 Not Found**: Session doesn't exist. Start a new session.
- **400 Bad Request**: Missing `message` field.
- **500 Server Error**: Wait and try again.
- **Empty curl output**: Network/proxy issue. Tell the user.

## API Base URL

All requests go to: `https://ai-portframe.ngrok.app`

## Notes

- Add `"language": "zh"` to the request body for other languages.
- Portfolio links open in the PortFrame Pro web app at pro.portframe.com.
