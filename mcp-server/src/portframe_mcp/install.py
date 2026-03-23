"""
PortFrame MCP Server — IDE Installer

Detects installed IDEs and registers the PortFrame MCP server
in each one's configuration. Merges into existing configs without
overwriting other MCP servers.

Run: python3 -m portframe_mcp.install
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def log(msg: str = "") -> None:
    print(msg, flush=True)


def _has_claude_cli() -> bool:
    return shutil.which("claude") is not None


def _mcp_server_entry() -> dict:
    return {"command": sys.executable, "args": ["-m", "portframe_mcp"]}


def _merge_mcp_config(config_path: Path, root_key: str, server_entry: dict) -> bool:
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
    cursor_dir = Path.home() / ".cursor"
    if not cursor_dir.exists():
        return False

    log("Cursor detected")

    global_config = cursor_dir / "mcp.json"
    _merge_mcp_config(global_config, "mcpServers", server_entry)
    log(f"  Global config: {global_config}")

    project_config = Path.cwd() / ".cursor" / "mcp.json"
    _merge_mcp_config(project_config, "mcpServers", server_entry)
    log(f"  Project config: {project_config}")

    return True


def _setup_claude_code(server_entry: dict) -> bool:
    if _has_claude_cli():
        log("Claude Code detected (CLI available)")
        try:
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

    server_entry = _mcp_server_entry()

    log(f"MCP command: {server_entry['command']} {' '.join(server_entry['args'])}")
    log()

    configured = []

    if _setup_cursor(server_entry):
        configured.append("Cursor")
    if _setup_claude_code(server_entry):
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
    try:
        has_token = sessions_file.exists() and json.loads(sessions_file.read_text()).get("api_token")
    except (json.JSONDecodeError, IOError):
        has_token = False

    if not has_token:
        log("Note: You haven't authenticated yet.")
        log(f"  Run: {sys.executable} -m portframe_mcp.auth")
        log("  (The agent will also prompt you on first use)")
    log()


if __name__ == "__main__":
    install()
