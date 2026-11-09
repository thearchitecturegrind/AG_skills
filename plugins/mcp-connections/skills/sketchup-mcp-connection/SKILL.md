---
name: sketchup-mcp-connection
description: Connects Claude to SketchUp - either the official Trimble SketchUp connector (cloud, makes new .skp files) or a live link to the user's open SketchUp model via the sketchup-mcp2 extension and Claude Desktop. Use whenever the user wants to connect Claude to SketchUp, control or read their open SketchUp model from Claude, set up or fix the SketchUp MCP server or claude_desktop_config.json entry, or troubleshoot it (server disconnected, "SketchUp not running or extension not started", spawn uvx ENOENT, IncompatibleVersionError, timeouts), even if they never say MCP.
---

# SketchUp MCP Connection

Gets Claude talking to SketchUp. The person on the other end is usually an
architect, not a developer: keep instructions plain, do the file and terminal work
for them, and leave only the in-app clicks to them.

## Step 1 - Pick the route (ask if it isn't obvious)

There are two different things people mean by "connect SketchUp to Claude":

| | **A. Official Trimble connector** | **B. Live model link (sketchup-mcp2)** |
|---|---|---|
| What it does | Claude builds a *new* model in a cloud SketchUp session and hands back a .skp download + preview | Claude reads and edits the model *open on your computer* right now |
| Needs | SketchUp subscription + Trimble ID, any Claude app (web, desktop, mobile) | SketchUp 2021+ desktop (Windows or Mac), Claude Desktop or Claude Code, ~10 min setup |
| Good for | Massing studies, furniture, quick concepts from a prompt or sketch | Inspecting/cleaning an existing model, batch edits, materials, exports, scripted geometry |

Ask one question if the request doesn't say: *"Do you want Claude to make new models
for you to download, or to work inside the SketchUp model you have open?"*
They can have both.

## Route A - Official Trimble SketchUp connector

No install. Tell the user:

1. In Claude: Settings -> Connectors -> Browse connectors, find **Trimble SketchUp**,
   click Connect, and sign in with their Trimble ID. (Team/Enterprise: an org owner
   has to enable it first.)
2. Start a chat and describe the model ("a 30x40 ft two-story massing with a 6/12
   gable roof"). Claude returns a preview and a .skp download link; ask for revisions
   in the same chat - it keeps version history within that chat.

If the connector's tools are already in your tool list (names like
`build_model`, `save_model`, `read_skill`), it's already connected - read its own
skills with `list_skills`/`read_skill` before modeling, and go.

Limits to state honestly: it doesn't touch the user's local model, and it works
best with basic shapes and curved surfaces, not detailed construction models.

## Route B - Live link to the open model

Architecture: Claude Desktop runs a small Python MCP server (`sketchup-mcp2`, fetched
automatically by `uvx`), which talks over local TCP port 9876 to a Ruby extension
running inside SketchUp. Both halves must be running.

### What the user does themselves (in-app clicks)

1. Download the latest `.rbz` from https://github.com/zinin/sketchup-mcp2/releases
2. SketchUp -> Window -> Extension Manager -> Install Extension -> pick the .rbz ->
   restart SketchUp.
3. With a model open: **Extensions** menu (older versions label it **Plugins**) ->
   **MCP Server -> Start Server**. It listens on 127.0.0.1:9876. Assume this is needed
   every time SketchUp is reopened.

Note which `.rbz` version they installed (it's in the filename, e.g.
`mcp_for_sketchup_v0.3.1.rbz`) - the Python side should match it.

### What you automate

You need a shell on the user's computer (Claude Code, Claude Desktop with a
terminal tool, or the remote-device shell). If you don't have one, skip to
"Manual fallback" below.

**Install uv** (provides `uvx` and a Python to run the script) if `uv --version` fails:

- Windows (PowerShell): `powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh`

Then open a new terminal (or use the full path, usually `~/.local/bin/uv`).

**Diagnose, then write the config:**

```
uv run --no-project scripts/configure_mcp.py --check
uv run --no-project scripts/configure_mcp.py --version <rbz version>
```

(`--version` is optional but prevents IncompatibleVersionError when PyPI moves ahead
of the extension they installed. Other flags: `--name`, `--port`, `--config`, `--uvx`.)

The script finds `claude_desktop_config.json` (including the Microsoft Store install
path on Windows), writes the **absolute path to uvx**, probes port 9876, backs up the
config, changes only `mcpServers.SketchUp`, and restores the backup if the result
isn't valid JSON. It refuses to touch a config that's already broken - fix that first.

Then tell the user: **fully quit Claude Desktop** (tray / menu-bar icon -> Quit;
closing the window isn't enough), reopen it, and try:
*"What's in my SketchUp model right now?"*

### Manual fallback (no shell available)

Give them this to paste into the config (Claude Desktop -> Settings -> Developer ->
Edit Config), merging into any existing `mcpServers` block rather than replacing it:

```json
{
  "mcpServers": {
    "SketchUp": {
      "command": "uvx",
      "args": ["sketchup-mcp2"],
      "env": { "SKETCHUP_MCP_PORT": "9876", "SKETCHUP_MCP_TIMEOUT": "120" }
    }
  }
}
```

If it then fails with "spawn uvx ENOENT", replace `"uvx"` with the full path from
`where uvx` (Windows; use `\\` for every backslash) or `which uvx` (Mac).

## Safety note to pass on

The extension ships with `eval_ruby` **on** - Claude can run any Ruby inside
SketchUp, which means full file and shell access. That's what makes complex modeling
possible, and Claude Desktop shows each call for approval. Tell the user to keep
approvals on (don't "always allow" eval_ruby on client work), save before big
requests, and that one Edit -> Undo reverses a whole tool call. To close the gate:
MCP Server -> Settings -> uncheck "Enable Ruby evaluation". Never bind the host to
0.0.0.0.

## Troubleshooting (in order of likelihood)

- **"SketchUp not running or extension not started"** - SketchUp is closed or
  Start Server wasn't clicked. The Python side retries on the next call; no restart
  of Claude needed.
- **Server shows disconnected / never appears** - Claude Desktop wasn't fully quit,
  the config JSON is invalid (Windows backslashes need `\\`), or `uvx` isn't on
  Claude's PATH. Run `--check`, then reproduce exactly what Claude runs:
  `"<uvx path from config>" sketchup-mcp2` - the real error prints in the terminal.
  Claude Desktop's own logs: Settings -> Developer -> open logs folder
  (`mcp-server-SketchUp.log`).
- **IncompatibleVersionError** - Python package and .rbz don't match. Re-run the
  script with `--version <rbz version>`, or install the newest .rbz.
- **Timeouts on big requests** - re-run with a larger timeout (edit
  `SKETCHUP_MCP_TIMEOUT`) and break the request into smaller steps; a long
  `eval_ruby` freezes SketchUp until it returns.
- **Units look wrong** - the typed tools use millimeters and degrees; SketchUp
  templates are often inches. Say units explicitly in prompts.
- **Port 9876 in use** - change the port in MCP Server -> Settings, then re-run the
  script with `--port <new>`.

## First prompts that prove it works

- "List the components and tags in my model."
- "Take a viewport screenshot" (needs SketchUp 2026+).
- "Add a 3000 x 600 x 900 mm box called Counter at the origin, then undo it."
