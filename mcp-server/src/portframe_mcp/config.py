import json
import sys
from datetime import datetime, timezone
from pathlib import Path

API_BASE_URL = "https://ai-portframe.ngrok.app"
SESSIONS_FILE = Path.home() / ".portframe" / "sessions.json"


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def _read_sessions_file() -> dict:
    if SESSIONS_FILE.exists():
        try:
            return json.loads(SESSIONS_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return {"api_token": None, "sessions": []}


def _write_sessions_file(data: dict) -> None:
    SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SESSIONS_FILE.write_text(json.dumps(data, indent=2) + "\n")


def load_token() -> str | None:
    data = _read_sessions_file()
    return data.get("api_token")


def load_sessions() -> list[dict]:
    data = _read_sessions_file()
    return data.get("sessions", [])


def save_session(session_id: str, description: str, portfolio_ids: list[str] | None = None) -> None:
    data = _read_sessions_file()
    sessions = data.get("sessions", [])

    now = datetime.now(timezone.utc).isoformat()
    existing = next((s for s in sessions if s.get("session_id") == session_id), None)

    if existing:
        existing["last_accessed"] = now
        if description:
            existing["description"] = description
        if portfolio_ids:
            existing["portfolio_ids"] = portfolio_ids
    else:
        sessions.append({
            "session_id": session_id,
            "created_at": now,
            "description": description,
            "portfolio_ids": portfolio_ids or [],
            "last_accessed": now,
        })

    data["sessions"] = sessions
    _write_sessions_file(data)
