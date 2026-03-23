#!/usr/bin/env python3
"""
PortFrame Skill Authentication Script

Starts a local HTTP server on port 8023, opens the browser to the PortFrame
skill-signup page, and waits for the OAuth callback with the API token.

No external dependencies required - uses Python stdlib only.
"""

import http.server
import json
import os
import platform
import subprocess
import sys
import threading
import urllib.parse
import webbrowser
from pathlib import Path

PORTFRAME_DIR = Path.home() / ".portframe"
SESSIONS_FILE = PORTFRAME_DIR / "sessions.json"
CALLBACK_PORT = 8023
SIGNUP_URL = "https://pro.portframe.com/skill-signup"

received_token = None
server_should_stop = threading.Event()


def log(msg=""):
    print(msg, flush=True)


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global received_token
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/callback" and "token" in params:
            received_token = params["token"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = """
            <html>
            <body style="font-family: system-ui, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #f9fafb;">
                <div style="text-align: center; padding: 2rem;">
                    <h1 style="color: #16a34a; font-size: 1.5rem;">Authentication Successful!</h1>
                    <p style="color: #6b7280; margin-top: 0.5rem;">You can close this window and return to your terminal.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            server_should_stop.set()
        else:
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Invalid callback</h1></body></html>")

    def log_message(self, format, *args):
        pass


def read_sessions_file():
    if SESSIONS_FILE.exists():
        try:
            return json.loads(SESSIONS_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return {"api_token": None, "sessions": []}


def write_sessions_file(data):
    PORTFRAME_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_FILE.write_text(json.dumps(data, indent=2))


def open_browser(url: str) -> bool:
    system = platform.system()
    try:
        if system == "Darwin":
            result = subprocess.run(["open", url], capture_output=True, timeout=5)
            if result.returncode == 0:
                return True
        elif system == "Windows":
            os.startfile(url)
            return True
        elif system == "Linux":
            for cmd in ["xdg-open", "sensible-browser", "x-www-browser"]:
                try:
                    subprocess.Popen([cmd, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return True
                except FileNotFoundError:
                    continue
    except Exception:
        pass
    try:
        webbrowser.open(url)
        return True
    except Exception:
        return False


def authenticate():
    global received_token

    sessions_data = read_sessions_file()
    if sessions_data.get("api_token"):
        token = sessions_data["api_token"]
        log(f"Already authenticated. Token prefix: {token[:12]}...")
        log(f"Token file: {SESSIONS_FILE}")
        log()
        log("To re-authenticate, delete the token from ~/.portframe/sessions.json and run this script again.")
        return token

    try:
        server = http.server.HTTPServer(("localhost", CALLBACK_PORT), CallbackHandler)
    except OSError as e:
        log(f"Error: Could not start server on port {CALLBACK_PORT}: {e}")
        log(f"Is another process using port {CALLBACK_PORT}?")
        sys.exit(1)

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    callback_url = f"http://localhost:{CALLBACK_PORT}/callback"
    signup_url = f"{SIGNUP_URL}?callback={urllib.parse.quote(callback_url)}"

    log("=" * 60)
    log("  PortFrame Skill Authentication")
    log("=" * 60)
    log()
    log(f"Server listening on port {CALLBACK_PORT}...")
    log()

    browser_opened = open_browser(signup_url)

    if browser_opened:
        log("Browser opened. Complete sign-in to continue.")
    else:
        log("Could not open browser automatically.")

    log()
    log("If the browser didn't open, copy and paste this URL:")
    log()
    log(f"  {signup_url}")
    log()
    log("Waiting for callback (5 min timeout)...")
    log()

    server_should_stop.wait(timeout=300)
    server.shutdown()

    if not received_token:
        log("Authentication timed out after 5 minutes.")
        log("Please try again.")
        sys.exit(1)

    sessions_data["api_token"] = received_token
    write_sessions_file(sessions_data)

    log("=" * 60)
    log("  Authentication Successful!")
    log("=" * 60)
    log()
    log(f"Token prefix: {received_token[:12]}...")
    log(f"Token saved to: {SESSIONS_FILE}")
    log()
    log("You can now use PortFrame through your AI agent.")
    return received_token


if __name__ == "__main__":
    authenticate()
