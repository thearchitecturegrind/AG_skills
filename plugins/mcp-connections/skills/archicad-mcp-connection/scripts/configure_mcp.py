#!/usr/bin/env python3
"""
Add (or repair) one MCP server entry in Claude Desktop's config file.

Run it through uv so nobody needs Python installed separately:

    uv run --no-project scripts/configure_mcp.py            # write the entry
    uv run --no-project scripts/configure_mcp.py --check    # diagnose only, change nothing

What it does:
  1. Finds claude_desktop_config.json (Windows normal + Microsoft Store installs, macOS).
  2. Resolves the ABSOLUTE path to `uvx` - Claude Desktop launches servers without
     your shell's PATH, so a bare "uvx" often fails with "spawn uvx ENOENT".
  3. Probes the app-side listener (Archicad JSON API ports) and warns if it's not up.
  4. Backs up the config, changes ONLY mcpServers.<name>, re-validates the JSON,
     and restores the backup automatically if anything goes wrong.
"""

import argparse
import datetime as dt
import json
import os
import platform
import shutil
import socket
import sys
from pathlib import Path

# ---- Defaults for this skill -------------------------------------------------
DEFAULT_NAME = "Archicad"
PACKAGE = "tapir-archicad-mcp"       # PyPI package that provides the MCP server
UVX_ARGS = ["--from", PACKAGE, "archicad-server"]   # uvx <args...>
ENV = {}
PROBE_PORTS = list(range(19723, 19745))  # Archicad JSON API port range (one per open instance)
APP_LABEL = "Archicad with a project loaded (Tapir add-on installed)"
# -------------------------------------------------------------------------------

IS_WIN = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"


def candidate_config_paths():
    home = Path.home()
    paths = []
    if IS_WIN:
        appdata = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
        local = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))
        # Microsoft Store builds redirect %APPDATA% into a package sandbox.
        pkgs = local / "Packages"
        if pkgs.is_dir():
            for p in sorted(pkgs.glob("Claude_*")):
                paths.append(p / "LocalCache" / "Roaming" / "Claude" / "claude_desktop_config.json")
        paths.append(appdata / "Claude" / "claude_desktop_config.json")
    elif IS_MAC:
        paths.append(home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json")
    else:
        paths.append(home / ".config" / "Claude" / "claude_desktop_config.json")
    return paths


def find_config(explicit):
    if explicit:
        return Path(explicit).expanduser()
    cands = candidate_config_paths()
    for p in cands:
        if p.exists():
            return p
    # Nothing exists yet: create in the first folder that exists, else the standard spot.
    for p in cands:
        if p.parent.is_dir():
            return p
    return cands[-1]


def find_uvx():
    exe = "uvx.exe" if IS_WIN else "uvx"
    hit = shutil.which("uvx")
    if hit:
        return str(Path(hit).resolve())
    home = Path.home()
    guesses = [
        home / ".local" / "bin" / exe,
        home / ".cargo" / "bin" / exe,
        Path("/opt/homebrew/bin/uvx"),
        Path("/usr/local/bin/uvx"),
    ]
    if IS_WIN:
        local = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))
        guesses += [local / "Programs" / "uv" / exe, local / "uv" / exe]
    # uv itself sets UV when running a script; uvx lives beside it.
    uv_env = os.environ.get("UV")
    if uv_env:
        guesses.insert(0, Path(uv_env).with_name(exe))
    for g in guesses:
        if g.exists():
            return str(g)
    return None


def port_open(port, host="127.0.0.1", timeout=1.5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def load_json(path):
    if not path.exists() or path.stat().st_size == 0:
        return {}
    text = path.read_text(encoding="utf-8-sig")
    return json.loads(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default=DEFAULT_NAME, help="Entry name under mcpServers")
    ap.add_argument("--config", help="Explicit path to claude_desktop_config.json")
    ap.add_argument("--uvx", help="Explicit path to uvx")
    ap.add_argument("--version", help=f"Pin {PACKAGE} to this version (match your extension)")
    ap.add_argument("--port", help="Override the app-side port")
    ap.add_argument("--check", action="store_true", help="Diagnose only; write nothing")
    a = ap.parse_args()

    ok = True
    cfg = find_config(a.config)
    print(f"[config] {cfg}  ({'exists' if cfg.exists() else 'will be created'})")

    uvx = a.uvx or find_uvx()
    if uvx:
        print(f"[uvx]    {uvx}")
    else:
        ok = False
        print("[uvx]    NOT FOUND - install uv first (see SKILL.md, step 'Install uv').")

    ports = [int(a.port)] if a.port else PROBE_PORTS
    live = [p for p in ports if port_open(p)]
    if live:
        print(f"[app]    listening on port {live[0]} - good")
    else:
        span = f"{ports[0]}" if len(ports) == 1 else f"{ports[0]}-{ports[-1]}"
        print(f"[app]    nothing listening on port {span} - open {APP_LABEL}. "
              "(Not blocking: the config can be written first.)")

    try:
        data = load_json(cfg)
        if not isinstance(data, dict):
            raise ValueError("top level is not a JSON object")
        print("[json]   current config parses OK")
    except Exception as e:
        print(f"[json]   current config is INVALID: {e}")
        print("         Fix or rename that file by hand first; refusing to overwrite it.")
        return 2

    existing = data.get("mcpServers", {}).get(a.name)
    if existing:
        print(f"[entry]  existing '{a.name}': {json.dumps(existing)}")

    if a.check:
        return 0 if ok else 1
    if not uvx:
        return 1

    args = list(UVX_ARGS)
    if a.version:
        args = [f"{PACKAGE}=={a.version}" if x == PACKAGE else x for x in args]
    entry = {"command": uvx, "args": args}
    env = dict(ENV)
    if a.port:
        for k in env:
            if k.endswith("_PORT"):
                env[k] = str(a.port)
    if env:
        entry["env"] = env

    data.setdefault("mcpServers", {})
    if not isinstance(data["mcpServers"], dict):
        print("[json]   'mcpServers' is not an object - fix by hand.")
        return 2
    data["mcpServers"][a.name] = entry

    cfg.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if cfg.exists():
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup = cfg.with_name(cfg.name + f".bak-{stamp}")
        shutil.copy2(cfg, backup)
        print(f"[backup] {backup}")

    try:
        cfg.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        json.loads(cfg.read_text(encoding="utf-8"))  # round-trip check
    except Exception as e:
        if backup:
            shutil.copy2(backup, cfg)
            print(f"[error]  write failed ({e}); restored backup.")
        else:
            print(f"[error]  write failed ({e}).")
        return 2

    others = [k for k in data["mcpServers"] if k != a.name]
    print(f"[done]   wrote mcpServers.{a.name}; left {len(others)} other server(s) untouched"
          + (f": {', '.join(others)}" if others else ""))
    print("NEXT: fully QUIT Claude Desktop (tray/menu-bar icon -> Quit), reopen it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
