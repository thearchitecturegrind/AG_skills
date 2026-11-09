# Wires up (or repairs) the "Revit Connector" entry in Claude Desktop's config so it
# talks to the mcp-servers-for-revit/mcp-server-for-revit-python pyRevit extension.
#
# Safe to re-run: it only ever touches the single mcpServers.<ServerName> key, and it
# backs up the config before writing.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File setup_revit_mcp.ps1 [-ServerName "Revit Connector"] [-ExtensionDir <path>]
#
# Assumes the mcp-server-for-revit-python extension has already been installed
# manually (git clone into pyRevit's Extensions folder, or the pyRevit extension
# installer) - this script does not install it for you.

param(
    [string]$ServerName = "Revit Connector",
    [string]$ExtensionDir = ""
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Output "==> $msg" }

# 1. Find the already-installed extension folder (must contain both main.py and
#    pyproject.toml — that pyproject.toml + uv.lock pair is what lets `uv run`
#    build a working venv).
if (-not $ExtensionDir) {
    Write-Step "Searching for the mcp-server-for-revit-python extension under pyRevit Extensions..."
    $candidates = @()
    $extRoots = @("$env:APPDATA\pyRevit\Extensions", "$env:PROGRAMDATA\pyRevit\Extensions")
    foreach ($root in $extRoots) {
        if (Test-Path $root) {
            $candidates += Get-ChildItem $root -Directory -ErrorAction SilentlyContinue |
                Where-Object {
                    (Test-Path (Join-Path $_.FullName "main.py")) -and
                    (Test-Path (Join-Path $_.FullName "pyproject.toml"))
                }
        }
    }
    if ($candidates.Count -eq 0) {
        throw "Could not find an extension folder with main.py + pyproject.toml under pyRevit\Extensions. Install the mcp-server-for-revit-python extension first (git clone it into %APPDATA%\pyRevit\Extensions with a folder name ending in .extension), or pass -ExtensionDir if you put it somewhere custom."
    }
    $ExtensionDir = $candidates[0].FullName
}
if (-not (Test-Path (Join-Path $ExtensionDir "main.py"))) {
    throw "No main.py found in $ExtensionDir"
}
Write-Step "Using extension directory: $ExtensionDir"

# 2. Make sure uv is installed, and get its full path (Claude Desktop launches
#    subprocesses without your shell's PATH updates, so a bare "uv" command can fail
#    even when `uv` works fine in your own terminal).
$uvCmd = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvCmd) {
    $uvLocal = "$env:USERPROFILE\.local\bin\uv.exe"
    if (Test-Path $uvLocal) {
        $uvPath = $uvLocal
    } else {
        Write-Step "uv not found - installing via the official installer script..."
        powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex" | Out-Null
        if (-not (Test-Path $uvLocal)) {
            throw "uv installation did not produce $uvLocal - check the installer output above."
        }
        $uvPath = $uvLocal
    }
} else {
    $uvPath = $uvCmd.Source
}
Write-Step "Using uv at: $uvPath"

# 3. Check the Routes server is actually reachable before wiring up Claude Desktop -
#    a config pointed at a correct path is still useless if Revit itself isn't listening.
Write-Step "Checking pyRevit Routes server at http://localhost:48884/ ..."
try {
    $status = Invoke-RestMethod -Uri "http://localhost:48884/revit_mcp/status/" -TimeoutSec 3
    if ($status.revit_available) {
        Write-Step "Routes server is up and Revit is available."
    } else {
        Write-Warning "Routes server responded but revit_available=false. Make sure a project is open in Revit."
    }
} catch {
    Write-Warning "Could not reach the Routes server. Open Revit, load a project, and enable pyRevit -> Settings -> Routes -> Routes Server before testing the connection. Continuing to write the config anyway."
}

# 4. Patch claude_desktop_config.json, touching only mcpServers.<ServerName>.
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
if (-not (Test-Path $configPath)) {
    throw "Claude Desktop config not found at $configPath. Open Claude Desktop -> Settings -> Developer at least once to generate it."
}

$backupPath = "$configPath.bak-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item $configPath $backupPath
Write-Step "Backed up existing config to $backupPath"

$config = Get-Content $configPath -Raw | ConvertFrom-Json

if (-not ($config.PSObject.Properties.Name -contains "mcpServers")) {
    $config | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value ([PSCustomObject]@{})
}

# The working invocation relies on the extension's own pyproject.toml/uv.lock to
# resolve dependencies (httpx, mcp, etc.) into a venv. The generic
# `uv run --with "mcp[cli]" mcp run main.py` form some guides show only installs the
# mcp package itself and will crash on import errors seconds after starting.
$serverEntry = [PSCustomObject]@{
    command = $uvPath
    args    = @("run", "--directory", $ExtensionDir, "main.py")
}

if ($config.mcpServers.PSObject.Properties.Name -contains $ServerName) {
    $config.mcpServers.$ServerName = $serverEntry
} else {
    $config.mcpServers | Add-Member -MemberType NoteProperty -Name $ServerName -Value $serverEntry
}

$json = $config | ConvertTo-Json -Depth 20
# Set-Content -Encoding utf8 writes a BOM, which some JSON parsers reject as a
# leading garbage character. Write plain UTF-8 without one to match what the app
# itself writes.
[System.IO.File]::WriteAllText($configPath, $json, (New-Object System.Text.UTF8Encoding($false)))

# 5. Validate the result actually parses before declaring victory.
try {
    Get-Content $configPath -Raw | ConvertFrom-Json | Out-Null
    Write-Step "Config written and validated as JSON: $configPath"
} catch {
    Copy-Item $backupPath $configPath -Force
    throw "Generated config failed to parse as JSON - restored the backup. Error: $($_.Exception.Message)"
}

Write-Step "Done. Fully quit Claude Desktop (tray icon -> Quit, not just closing the window) and reopen it."
Write-Step "Then, with Revit open and a project loaded, ask Claude something like 'get Revit project info'."
