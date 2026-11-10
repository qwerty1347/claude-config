# Refresh this repo from this PC's ~/.claude (agents, skills, global CLAUDE.md).
$ErrorActionPreference = 'Stop'
$src = Join-Path $env:USERPROFILE '.claude'

robocopy (Join-Path $src 'agents') (Join-Path $PSScriptRoot 'agents') *.md /MIR /NJH /NJS /NDL /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "agents copy failed ($LASTEXITCODE)" }

# synced = Claude-managed skill cache, not a skill
robocopy (Join-Path $src 'skills') (Join-Path $PSScriptRoot 'skills') /MIR /XD synced __pycache__ node_modules /NJH /NJS /NDL /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "skills copy failed ($LASTEXITCODE)" }

Copy-Item (Join-Path $src 'CLAUDE.md') (Join-Path $PSScriptRoot 'CLAUDE.md') -Force
$global:LASTEXITCODE = 0
Write-Host "exported: agents, skills, CLAUDE.md"
