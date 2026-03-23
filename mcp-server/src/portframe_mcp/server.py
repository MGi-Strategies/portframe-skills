import json
import logging
import sys

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from portframe_mcp.config import API_BASE_URL, load_token, load_sessions, save_session

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("portframe-mcp")

mcp = FastMCP(
    "portframe",
    instructions="PortFrame AI — create, backtest, and analyze investment portfolios",
)

AUTH_ERROR = (
    "No PortFrame API token found. "
    "The user needs to authenticate first. Run: python3 -m portframe_mcp.auth"
)


def _get_token() -> str:
    token = load_token()
    if not token:
        raise ToolError(AUTH_ERROR)
    return token


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


@mcp.tool()
async def portframe_request(message: str, session_id: str = "", language: str = "en") -> str:
    """Submit a portfolio request to PortFrame AI. Returns a session_id you must poll with portframe_check_status.

    Args:
        message: Your portfolio request (e.g. "Build an AI focused portfolio")
        session_id: Optional existing session ID to continue a previous conversation
        language: Response language code (default: en)
    """
    token = _get_token()

    body: dict = {"message": message, "language": language}
    if session_id:
        body["session_id"] = session_id

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{API_BASE_URL}/api/v1/skill/request",
                headers=_headers(token),
                json=body,
            )
    except httpx.ConnectError as e:
        raise ToolError(f"Could not connect to PortFrame API: {e}")
    except httpx.TimeoutException:
        raise ToolError("Request to PortFrame API timed out after 30 seconds")

    if resp.status_code == 401:
        raise ToolError(
            "Authentication failed (401). Token may be invalid or expired. "
            "Run: python3 -m portframe_mcp.auth"
        )
    if resp.status_code == 400:
        raise ToolError(f"Bad request: {resp.text}")
    if resp.status_code >= 500:
        raise ToolError(f"PortFrame server error ({resp.status_code}): {resp.text}")
    if resp.status_code not in (200, 201, 202):
        raise ToolError(f"Unexpected response ({resp.status_code}): {resp.text}")

    data = resp.json()
    sid = data.get("session_id", "")

    logger.info(f"Request submitted, session_id={sid}")

    return json.dumps({
        "session_id": sid,
        "status": data.get("status", "processing"),
        "next_step": "Call portframe_check_status with this session_id every 5-10 seconds until status is 'complete'. Backtests can take 1-5 minutes.",
    })


@mcp.tool()
async def portframe_check_status(session_id: str) -> str:
    """Check the status of a PortFrame request and get results when complete.

    Poll this every 5-10 seconds until status is "complete". Backtests can take 1-5 minutes — be patient.

    Args:
        session_id: The session ID from portframe_request
    """
    token = _get_token()

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(
                f"{API_BASE_URL}/api/v1/skill/session/{session_id}",
                headers=_headers(token),
            )
    except httpx.ConnectError as e:
        raise ToolError(f"Could not connect to PortFrame API: {e}")
    except httpx.TimeoutException:
        raise ToolError("Request to PortFrame API timed out after 30 seconds")

    if resp.status_code == 401:
        raise ToolError(
            "Authentication failed (401). Token may be invalid or expired. "
            "Run: python3 -m portframe_mcp.auth"
        )
    if resp.status_code == 404:
        raise ToolError(f"Session '{session_id}' not found. It may have expired or belong to a different user.")
    if resp.status_code >= 500:
        raise ToolError(f"PortFrame server error ({resp.status_code}): {resp.text}")

    data = resp.json()
    status = data.get("status", "unknown")

    if status == "complete":
        save_session(
            session_id=session_id,
            description=data.get("messages_markdown", "")[:100],
            portfolio_ids=[],
        )

    result = {
        "session_id": session_id,
        "status": status,
    }

    if status == "complete":
        result["messages_markdown"] = data.get("messages_markdown", "")
        result["portfolio_links"] = data.get("portfolio_links", [])
    elif status == "processing":
        result["next_step"] = "Still processing. Call portframe_check_status again in 5-10 seconds."
    elif status == "error":
        result["error"] = data.get("error", "Unknown error")

    return json.dumps(result)


@mcp.tool()
async def portframe_list_sessions() -> str:
    """List previous PortFrame sessions. Use a session_id with portframe_request to continue a conversation."""
    sessions = load_sessions()

    if not sessions:
        return json.dumps({"sessions": [], "message": "No previous sessions found."})

    return json.dumps({
        "sessions": [
            {
                "session_id": s.get("session_id", ""),
                "description": s.get("description", ""),
                "created_at": s.get("created_at", ""),
                "last_accessed": s.get("last_accessed", ""),
            }
            for s in sessions
        ]
    })


def main():
    mcp.run(transport="stdio")
