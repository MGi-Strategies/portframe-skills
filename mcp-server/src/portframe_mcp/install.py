"""
PortFrame MCP Server — IDE Installer

Detects installed IDEs and registers the PortFrame MCP server
in each one's configuration. Merges into existing configs without
overwriting other MCP servers.

Run: python -m portframe_mcp.install
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def log(msg: str = "") -> None:
    print(msg, flush=True)


def _has_uvx() -> bool:
    return shutil.which("uvx") is not None


def _has_claude_cli() -> bool:
    return shutil.which("claude") is not None


def _mcp_server_entry(use_uvx: bool) -> dict:
    if use_uvx:
        return {"command": "uvx", "args": ["portframe-mcp"]}

    python_path = sys.executable
    return {"command": python_path, "args": ["-m", "portframe_mcp"]}


def _merge_mcp_config(config_path: Path, root_key: str, server_entry: dict) -> bool:
    """Merge portframe server into an mcp.json file. Returns True if changed."""
    data = {}
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text())
        except (json.JSONDecodeError, IOError):
            log(f"  Warning: {config_path} exists but is invalid JSON, overwriting")
            data = {}

    servers = data.setdefault(root_key, {})
    servers["portframe"] = server_entry

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(data, indent=2) + "\n")
    return True


def _setup_cursor(server_entry: dict) -> bool:
    config_path = Path.home() / ".cursor" / "mcp.json"
    if not (Path.home() / ".cursor").exists():
        return False

    log("Cursor detected")
    _merge_mcp_config(config_path, "mcpServers", server_entry)
    log(f"  Configured: {config_path}")
    return True


def _setup_claude_code(server_entry: dict, use_uvx: bool) -> bool:
    if _has_claude_cli():
        log("Claude Code detected (CLI available)")
        try:
            if use_uvx:
                cmd = [
                    "claude", "mcp", "add",
                    "--transport", "stdio",
                    "--scope", "user",
                    "portframe",
                    "--",
                    "uvx", "portframe-mcp",
                ]
            else:
                cmd = [
                    "claude", "mcp", "add",
                    "--transport", "stdio",
                    "--scope", "user",
                    "portframe",
                    "--",
                    sys.executable, "-m", "portframe_mcp",
                ]
            subprocess.run(cmd, capture_output=True, timeout=10)
            log("  Configured via: claude mcp add")
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            log(f"  Warning: claude mcp add failed: {e}")

    claude_dir = Path.home() / ".claude"
    if not claude_dir.exists():
        return False

    log("Claude Code detected (~/.claude exists)")
    config_path = claude_dir / "mcp.json"
    _merge_mcp_config(config_path, "mcpServers", server_entry)
    log(f"  Configured: {config_path}")
    return True


def _setup_windsurf(server_entry: dict) -> bool:
    config_path = Path.home() / ".codeium" / "windsurf" / "mcp_config.json"
    if not (Path.home() / ".codeium" / "windsurf").exists():
        return False

    log("Windsurf detected")
    _merge_mcp_config(config_path, "mcpServers", server_entry)
    log(f"  Configured: {config_path}")
    return True


def _setup_vscode(server_entry: dict) -> bool:
    vscode_dir = Path.home() / ".vscode"
    if not vscode_dir.exists():
        return False

    log("VS Code detected")
    vscode_entry = {"type": "stdio", **server_entry}
    config_path = vscode_dir / "mcp.json"
    _merge_mcp_config(config_path, "servers", vscode_entry)
    log(f"  Configured: {config_path}")
    return True


def install() -> None:
    log("=" * 50)
    log("  PortFrame MCP Server — Installer")
    log("=" * 50)
    log()

    use_uvx = _has_uvx()
    if use_uvx:
        log(f"uvx found: will use 'uvx portframe-mcp'")
    else:
        log(f"uvx not found: will use '{sys.executable} -m portframe_mcp'")
    log()

    server_entry = _mcp_server_entry(use_uvx)
    configured = []

    if _setup_cursor(server_entry):
        configured.append("Cursor")
    if _setup_claude_code(server_entry, use_uvx):
        configured.append("Claude Code")
    if _setup_windsurf(server_entry):
        configured.append("Windsurf")
    if _setup_vscode(server_entry):
        configured.append("VS Code")

    log()
    if configured:
        log(f"Configured for: {', '.join(configured)}")
    else:
        log("No supported IDEs detected. You can manually add PortFrame to your IDE's MCP config.")
        log()
        log("Example (add to your IDE's mcp.json):")
        log(json.dumps({"mcpServers": {"portframe": server_entry}}, indent=2))

    log()
    log("Next steps:")
    log("  1. Restart your IDE")
    log("  2. Start a new chat session")
    log("  3. Ask: 'Build me an AI focused portfolio'")
    log()

    sessions_file = Path.home() / ".portframe" / "sessions.json"
    if not sessions_file.exists() or not json.loads(sessions_file.read_text()).get("api_token"):
        log("Note: You haven't authenticated yet.")
        log("  Run: python3 -m portframe_mcp.auth")
        log("  (The agent will also prompt you on first use)")
    log()


if __name__ == "__main__":
    install()
