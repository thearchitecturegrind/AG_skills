---
name: archicad-mcp-connection
description: Connects Claude Desktop to a running Archicad project through the Tapir add-on and the tapir-archicad-mcp server, so Claude can read and edit the live model (elements, properties, classifications, layers, views, IFC). Use whenever the user wants to connect Claude to Archicad, set up or fix the Archicad/Tapir MCP entry in claude_desktop_config.json, install the Tapir add-on for AI use, or troubleshoot it (server disconnected, no Archicad instances found, spawn uvx ENOENT, commands failing), even if they never say MCP or Tapir.
---

# Archicad MCP Connection

Gets Claude talking to the Archicad project open on the user's computer. The person
is usually an architect, not a developer: do the file and terminal work for them,
and leave only installer runs and in-app clicks to them.

How it fits together: Claude Desktop runs a small Python MCP server
(`tapir-archicad-mcp`, fetched automatically by `uvx`). That server finds every
running Archicad on this computer through Archicad's built-in JSON API (one local
port per open instance, starting at 19723) and adds the extra commands registered by
the **Tapir** add-on - 190+ commands in total. Archicad must be running with a
project open; there's no cloud option.

Works on Windows and macOS, Archicad 25-29 (Tapir publishes builds per version).
Requires Claude Desktop or Claude Code - claude.ai on the web can't launch local
MCP servers.

## What the user does themselves

1. **Install Tapir** (recommended: the installer, which detects every installed
   Archicad version and puts the matching add-on in place):
   - Windows: https://github.com/ENZYME-APD/tapir-archicad-automation/releases/latest/download/TapirInstaller_Win.exe
     - asks for admin rights; it isn't code-signed, so on the SmartScreen warning
     click **More info -> Run anyway**.
   - macOS: https://github.com/ENZYME-APD/tapir-archicad-automation/releases/latest/download/TapirInstaller_Mac.zip
     - unzip and open (signed and notarized).

   Manual alternative (e.g. no admin rights): download the `.apx` (Win) or `.zip`
   (Mac) for their exact Archicad version from the Tapir README, then in Archicad
   **Options -> Add-On Manager -> Edit List of Available Add-Ons -> Add**, pick the
   file, OK.
2. **Restart Archicad and open a project.** A project must be open, not just the
   start dialog.

Tapir is technically optional (the official JSON API alone gives a smaller command
set), but install it - most useful edits come from Tapir's commands.

## What you automate

You need a shell on the user's computer (Claude Code, Claude Desktop with a terminal
tool, or the remote-device shell). Without one, use "Manual fallback" below.

**Install uv** (provides `uvx` and a Python to run the script) if `uv --version` fails:

- Windows (PowerShell): `powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh`

Then open a new terminal (or use the full path, usually `~/.local/bin/uv`).

**Diagnose, then write the config:**

```
uv run --no-project scripts/configure_mcp.py --check
uv run --no-project scripts/configure_mcp.py
```

Optional flags: `--version 0.5.3` pins the server package (use when a new release
misbehaves), `--name` changes the entry name (default `Archicad`), `--config` /
`--uvx` give explicit paths.

The script finds `claude_desktop_config.json` (including the Microsoft Store install
path on Windows), writes the **absolute path to uvx** (Claude Desktop doesn't inherit
your terminal's PATH), checks ports 19723-19744 for a running Archicad, backs up the
config, changes only `mcpServers.Archicad`, and restores the backup if the result
isn't valid JSON. It refuses to edit a config that's already broken.

The first launch downloads the server and its Python (3.12+) - allow a minute.

Then tell the user: **fully quit Claude Desktop** (tray / menu-bar icon -> Quit;
closing the window isn't enough), reopen it, and ask:
*"What Archicad projects do I have running?"*

## Manual fallback (no shell available)

Claude Desktop -> Settings -> Developer -> Edit Config, and merge this into the
existing `mcpServers` block (don't replace other servers):

```json
{
  "mcpServers": {
    "Archicad": {
      "command": "uvx",
      "args": ["--from", "tapir-archicad-mcp", "archicad-server"]
    }
  }
}
```

If it fails with "spawn uvx ENOENT", replace `"uvx"` with the full path from
`where uvx` (Windows; every backslash doubled as `\\`) or `which uvx` (Mac).

## How Claude should use it once connected

The server deliberately exposes only a few tools, so the context isn't flooded:

1. `discovery_list_active_archicads` - finds open instances and their **port**.
   With several projects open, confirm which one by name before editing.
2. `archicad_list_commands` - look up the right command name.
3. `archicad_get_command_schema` - get its exact parameters.
4. `archicad_call_tool` - run it with the command name, port and parameters.

Always read before writing (get elements / properties first), and do edits on
a saved project or a copy - Archicad's Undo covers them, but Teamwork projects
need the elements reserved first or the edit fails.

## Troubleshooting (in order of likelihood)

- **"No running Archicad found" / empty instance list** - Archicad is closed, still
  on the start dialog, or busy with a modal dialog. Open a project and close any
  dialogs. `--check` reports whether ports 19723-19744 answer.
- **Archicad found, but Tapir commands missing or failing** - Tapir isn't loaded for
  this Archicad version. Check Options -> Add-On Manager for Tapir; re-run the
  installer after upgrading Archicad (each version needs its own build).
- **Server shows disconnected / tools never appear** - Claude Desktop wasn't fully
  quit, the config JSON is invalid, or uvx isn't on Claude's PATH. Run `--check`, then
  reproduce exactly what Claude runs and read the real error:
  `"<uvx path from config>" --from tapir-archicad-mcp archicad-server`
  Claude Desktop's own log: Settings -> Developer -> open logs folder
  (`mcp-server-Archicad.log`).
- **Windows firewall prompt** - allow local access; everything stays on 127.0.0.1.
- **Edits rejected in a Teamwork project** - reserve the elements in Archicad first (or
  have Claude look for a reservation command in `archicad_list_commands` and use it).

## First prompts that prove it works

- "What Archicad projects do I have running?"
- "How many walls, doors and windows are in the model, by story?"
- "List the zones with their names, numbers and areas."
