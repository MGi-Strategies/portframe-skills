#!/usr/bin/env python3
"""Configure Cursor sandbox to allow PortFrame API access.

Merges PortFrame domains into the existing ~/.cursor/sandbox.json
without overwriting other settings. Creates the file if it doesn't exist.
"""
import json
import os

DOMAINS = ["ai.portframe.com", "pro.portframe.com"]
SANDBOX_PATH = os.path.expanduser("~/.cursor/sandbox.json")


def setup():
    if os.path.exists(SANDBOX_PATH):
        with open(SANDBOX_PATH) as f:
            data = json.load(f)
    else:
        data = {}

    network = data.setdefault("networkPolicy", {})
    network.setdefault("default", "deny")
    allow = set(network.get("allow", []))
    allow.update(DOMAINS)
    network["allow"] = sorted(allow)

    os.makedirs(os.path.dirname(SANDBOX_PATH), exist_ok=True)
    with open(SANDBOX_PATH, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"Cursor sandbox configured: {', '.join(DOMAINS)} allowed", flush=True)
    print(f"Config: {SANDBOX_PATH}", flush=True)


if __name__ == "__main__":
    setup()
