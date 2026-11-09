---
name: rhino-mcp-connection
description: Connects Claude to a running Rhino 8 session (and Grasshopper) - either McNeel's official Rhino MCP Platform connector or the community RhinoMCP plugin - so Claude can read, model and script in the open .3dm. Use whenever the user wants to connect Claude to Rhino or Grasshopper, install the Rhino connector/.mcpb, set up or fix the Rhino MCP entry in claude_desktop_config.json, or troubleshoot it (server disconnected, mcpstart/MCPStart issues, nothing on port 1999 or 10500, spawn uvx ENOENT, Intel Mac failures), even if they never say MCP.
---

# Rhino MCP Connection

Gets Claude talking to the Rhino file open on the user's computer. The person is
usually an architect or designer, not a developer: do the file and terminal work
for them, and leave only installs and in-app clicks to them.

Both options need **Rhino 8** running on the same computer, and Claude Desktop or
Claude Code (claude.ai on the web can't reach a local Rhino). Pick one and stick
with it - running both at once gives Claude two overlapping tool sets.

## Step 1 - Pick the route

| | **A. McNeel official (Rhino MCP Platform)** | **B. Community RhinoMCP** |
|---|---|---|
| Who | McNeel (Rhino's maker), early v0.1.x | jingcheng-chen/rhinomcp, open source |
| Setup | Install a `.mcpb` extension in Claude Desktop; no config editing | Package Manager plugin + config entry (script below) |
| Mac | **Apple Silicon only** (Intel Macs fail) | Windows and Mac |
| Strengths | Python + Rhino commands, viewport capture, Grasshopper 1 | Large typed toolset: booleans, loft/sweep, layers, analysis, deep Grasshopper editing (add/connect components, set values, build graphs) |
| Port | 10500 (HTTP, via `MCPStart`) | 1999 (local TCP, via `mcpstart`) |

Default: **A** for a quick Claude Desktop setup on Windows or an Apple Silicon Mac.
Choose **B** for an Intel Mac, for heavy Grasshopper work, or if A won't connect.
Ask only if the request doesn't make it obvious.

## Route A - McNeel official connector

The release moves quickly, so get the current links from the docs before giving
steps: https://mcneel.github.io/RhinoAI/docs/getting-started/ (Claude Desktop guide:
`/connector`, Claude Code guide: `/cc-plugin`). As of the latest check:

**Claude Desktop**
1. Download `connector.mcpb` from the newest `connector-v*` release at
   https://github.com/mcneel/RhinoAI/releases
2. Claude Desktop -> Settings -> Extensions -> Advanced settings -> Install Extension
   -> pick the file -> Install. (Menu names have shifted between Desktop versions;
   if it isn't there, look for Extensions under Customize.)
3. Install the Rhino plugin **Rhino-MCP-Platform**: in Rhino run `PackageManager`,
   search for it, install, restart Rhino. If Package Manager fails, Rhino's bundled
   Yak CLI works:
   - Windows: `"C:\Program Files\Rhino 8\System\Yak.exe" install Rhino-MCP-Platform`
   - Mac: `"/Applications/Rhino 8.app/Contents/Resources/bin/yak" install Rhino-MCP-Platform`
   (The connector can also install the plugin itself if asked.)
4. In Rhino run `MCPStart` and accept the default port (10500).
5. New chat in Claude Desktop: *"What's in my Rhino file?"*

**Claude Code**: install the plugin as above, run `MCPConnect` in Rhino, and paste
the prompt it gives into a new Claude Code session.

**If A won't connect**: confirm Rhino 8 (not 7), that `MCPStart` printed a port, and
on Mac that it's Apple Silicon. Don't hand-write a `claude_desktop_config.json` entry
for this route - forum attempts with `mcp-remote` to port 10500 failed; send the user
to the McNeel forum (discourse.mcneel.com, "Rhino MCP Server" thread) or switch to B.

## Route B - Community RhinoMCP

### What the user does themselves

1. Rhino 8 -> Tools -> **Package Manager** -> search **rhinomcp** -> Install ->
   restart Rhino.
2. Open a file and type **`mcpstart`** in the command line. Needed once per Rhino
   session (`mcpstop` turns it off). It listens on 127.0.0.1:1999.

### What you automate

You need a shell on the user's computer (Claude Code, Claude Desktop with a terminal
tool, or the remote-device shell). Without one, use "Manual fallback".

**Claude Code users**: one line does it - `claude mcp add rhino -- uvx rhinomcp@latest`
(install uv first, below). Stop here.

**Install uv** (provides `uvx` and a Python to run the script) if `uv --version` fails:

- Windows (PowerShell): `powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh`

Then open a new terminal (or use the full path, usually `~/.local/bin/uv`).

**Diagnose, then write the Claude Desktop config:**

```
uv run --no-project scripts/configure_mcp.py --check
uv run --no-project scripts/configure_mcp.py
```

Optional flags: `--version <x>` pins the server to match the Rhino plugin version
(the server logs a warning on mismatch), `--no-code-exec` switches off the Python,
C# and run_command tools, `--port`, `--name` (default `Rhino`), `--config`, `--uvx`.

The script finds `claude_desktop_config.json` (including the Microsoft Store path on
Windows), writes the **absolute path to uvx** (Claude Desktop doesn't inherit the
terminal's PATH), checks port 1999, backs up the config, changes only
`mcpServers.Rhino`, and restores the backup if the result isn't valid JSON. It
refuses to edit a config that's already broken.

Then tell the user: **fully quit Claude Desktop** (tray / menu-bar icon -> Quit;
closing the window isn't enough), reopen it, and ask: *"Summarize my Rhino document."*

### Manual fallback (no shell available)

Claude Desktop -> Settings -> Developer -> Edit Config; merge into the existing
`mcpServers` block, don't replace other servers:

```json
{
  "mcpServers": {
    "Rhino": {
      "command": "uvx",
      "args": ["rhinomcp@latest"],
      "env": { "RHINO_MCP_HOST": "127.0.0.1" }
    }
  }
}
```

If it fails with "spawn uvx ENOENT", replace `"uvx"` with the full path from
`where uvx` (Windows; every backslash doubled as `\\`) or `which uvx` (Mac).

## Safety note to pass on

Both routes let Claude run Python/C# and Rhino commands inside Rhino - that's what
makes complex modeling work, and it also means file and system access. Tell the
user: keep tool approvals on in Claude Desktop (don't "always allow" script tools on
client files), save before big requests, and Rhino's Undo reverses changes. For
Route B, `--no-code-exec` closes the scripting tools if they want a locked-down setup.
The link is unauthenticated local TCP - never expose it beyond 127.0.0.1.

## Troubleshooting (Route B, in order of likelihood)

- **Tools appear but every call fails to connect** - `mcpstart` wasn't run this
  session, or Rhino is closed. `--check` shows whether port 1999 answers.
- **Server shows disconnected / never appears** - Claude Desktop wasn't fully quit,
  invalid JSON, or uvx not on Claude's PATH. Run `--check`, then reproduce exactly
  what Claude runs: `"<uvx path from config>" rhinomcp@latest` - the real error prints.
  Claude Desktop log: Settings -> Developer -> open logs folder (`mcp-server-Rhino.log`).
- **Version mismatch warning / odd failures after an update** - update the plugin in
  Package Manager, then fully restart Claude Desktop (it reads the tool list only at
  launch). Or pin with `--version`.
- **Two Rhino servers fighting** - only one RhinoMCP server at a time; remove the
  official connector (or this entry) so one remains.
- **Sizes come out wrong** - check the document's units (`Units` in Rhino) and
  state units explicitly in prompts.

## First prompts that prove it works

- "Summarize my Rhino document: layers, object counts, units."
- "Capture the current viewport."
- "Make a 10 x 10 x 3 m box on a new layer called Test, then undo it."
- Grasshopper (Route B): "Open Grasshopper and build a slider-driven circle array."
