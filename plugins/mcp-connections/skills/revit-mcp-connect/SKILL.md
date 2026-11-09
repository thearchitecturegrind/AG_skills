---
name: revit-mcp-connect
description: Wires up or repairs the Claude Desktop to Revit MCP connection (mcp-servers-for-revit/mcp-server-for-revit-python running over pyRevit Routes), after the extension itself has already been installed manually. Use this whenever the user wants to connect Claude to Revit, add/fix the "Revit Connector" (or similarly named) entry in claude_desktop_config.json, or is troubleshooting that connection - including symptoms like the server showing "disconnected" right after starting, tool calls timing out, ModuleNotFoundError in an MCP server log, or Claude not seeing Revit tools at all. Also use it if the user mentions RevitMCP, pyRevit Routes server, or asks why their Revit MCP setup stopped working after it briefly showed as running.
---

# Revit MCP Connect

Connects Claude Desktop to a running Revit session through the
`mcp-servers-for-revit/mcp-server-for-revit-python` pyRevit extension. This skill
picks up right after the extension itself has been installed by hand - it automates
the remaining file/CLI work: finding where the extension landed, installing `uv`,
and writing the Claude Desktop config correctly. It intentionally does **not** try to
automate anything that requires clicking inside an application UI, or the extension
install itself (see Prerequisites) - those are quick for a person to do, worth
walking through on camera, and fragile to script against a GUI.

This is meant to be a fast-path for someone who just watched (or is watching) a
walkthrough of this setup and wants to skip the fiddly last-mile steps: install the
extension and flip the two Revit settings yourself, then run the script for
everything else.

## Prerequisites (the user must do these themselves)

1. pyRevit installed, with the pyRevit tab visible in Revit's ribbon. (If not, point
   them to https://pyrevitlabs.io/docs/pyrevit/installer - this skill doesn't install
   pyRevit itself.)
2. The `mcp-server-for-revit-python` extension installed - `git clone
   https://github.com/mcp-servers-for-revit/mcp-server-for-revit-python` into
   `%APPDATA%\pyRevit\Extensions`, with the cloned folder renamed to end in
   `.extension` (e.g. `mcp-server-for-revit-python.extension`). This is a good step
   to do live in a video since it's just a clone + rename.
3. In Revit: pyRevit tab -> Settings -> Routes -> enable "Routes Server", then restart
   Revit. Windows Firewall may prompt for permission the first time - allow it.
4. Revit open with an actual project loaded (the Routes server reports
   `revit_available: false` otherwise, and Claude's tool calls will fail).

Everything else - installing `uv` and editing the Claude Desktop config - the script
below handles.

## What this skill automates

```
powershell -ExecutionPolicy Bypass -File scripts/setup_revit_mcp.ps1
```

This script:

1. **Finds the already-installed extension.** It searches pyRevit's Extensions
   directories for a folder containing both `main.py` and `pyproject.toml`. If
   nothing's found, it errors out with a reminder to complete Prerequisite 2 first
   (or pass `-ExtensionDir` if it was installed somewhere custom).
2. **Ensures `uv` is installed** and resolves its *full* executable path. This
   matters: Claude Desktop launches MCP servers as subprocesses without your shell's
   PATH, so a bare `"command": "uv"` can fail even though `uv` works fine in a normal
   terminal. The script always writes the absolute path to `uv.exe`, installing it
   via the official installer if it's not already present.
3. **Checks the Routes server** at `http://localhost:48884/revit_mcp/status/` and
   warns (but doesn't block) if it's unreachable or Revit isn't available - a good
   nudge if the person skipped a prerequisite step.
4. **Patches `claude_desktop_config.json`**, touching only the one
   `mcpServers.<ServerName>` entry (default name `"Revit Connector"`) - it never
   overwrites unrelated keys like other MCP servers or app preferences that may live
   in the same file. It backs up the file first (`.bak-<timestamp>`) and rolls back
   automatically if the result doesn't parse as valid JSON.
5. **Writes the working invocation**: `uv run --directory <extension-dir> main.py`.

After it finishes, tell the user to fully quit Claude Desktop (tray icon -> Quit -
closing the window is not enough) and reopen it, then try a prompt like "get Revit
project info."

## Why the invocation matters (read this before improvising a different command)

This extension ships its own `pyproject.toml` and `uv.lock` pinning ~28 dependencies
(httpx, mcp, uvicorn, etc.). `uv run --directory <dir> main.py` uses that lockfile to
build a proper virtual environment before running the script.

A different, more generic-looking form shows up in some setup guides:

```json
"args": ["run", "--with", "mcp[cli]", "mcp", "run", "<path>/main.py"]
```

This only installs the bare `mcp` package into an ephemeral environment. It will
often start successfully and even show "running" for a second, then crash the moment
`main.py` hits `import httpx` (or any other dependency `mcp[cli]` doesn't happen to
pull in) - which surfaces in Claude Desktop simply as "server disconnected" with no
obvious cause. If you see that symptom and the config uses the `--with "mcp[cli]"
mcp run` form, switch it to `--directory <dir> main.py` instead.

## Diagnosing "server disconnected" or other failures

If the script's checks all pass but Claude Desktop still shows the server as
disconnected, don't guess - run the exact command Claude Desktop runs and read the
real error:

```
& "<uv-path-from-config>" run --directory "<extension-dir-from-config>" main.py
```

Common causes, in order of likelihood:

- **Invalid JSON in the config file.** Windows paths need `\\` for every backslash
  (`"C:\\Users\\..."`, not `"C:\\Users\..."` or `"C:\Users\..."`). A malformed config
  fails to parse and Claude Desktop won't load the server at all - it won't
  necessarily give a clear error about *why*. Validate with:
  `Get-Content <path> -Raw | ConvertFrom-Json`
- **Missing dependencies** (`ModuleNotFoundError`) - almost always means the config
  is using the generic `mcp run` form instead of `--directory <dir> main.py`; see above.
- **Routes server unreachable** - Revit isn't open, no project is loaded, or Routes
  Server isn't enabled in pyRevit Settings.
- **Stale config not picked up** - Claude Desktop caches the config at startup; a
  config edit needs a full quit-and-reopen (not just closing the window) to take
  effect.

When editing `claude_desktop_config.json` directly instead of via the script, always
read the current file first and change only the relevant `mcpServers` entry - other
tools and unrelated app preferences commonly live in the same file, and clobbering
them is an easy way to reintroduce a fresh problem while fixing this one.
