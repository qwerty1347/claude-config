# Apply this repo to this PC's ~/.claude. Existing items are renamed to *.bak-<timestamp> first.
$ErrorActionPreference = 'Stop'
$dst = Join-Path $env:USERPROFILE '.claude'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
New-Item -ItemType Directory -Force $dst | Out-Null

foreach ($name in 'agents', 'skills', 'CLAUDE.md') {
    $target = Join-Path $dst $name
    if (Test-Path $target) {
        $item = Get-Item $target -Force
        if ($item.LinkType) {
            # never write through a junction/symlink into another repo
            Write-Warning "$target is a $($item.LinkType) - skipped. Remove the link to import it."
            continue
        }
        Rename-Item $target "$name.bak-$stamp"
        Write-Host "backup: $name.bak-$stamp"
    }
    Copy-Item (Join-Path $PSScriptRoot $name) $target -Recurse
    Write-Host "imported: $name"
}

& (Join-Path $PSScriptRoot 'plugins.ps1')
Write-Host "done. Restart Claude Code."
