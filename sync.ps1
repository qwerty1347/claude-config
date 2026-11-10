# Make this PC's ~/.claude match this repo. Safe to re-run (run again after every git pull).
#  - agents, skills : junction to this repo, so edits land in the repo and git pull syncs them
#  - CLAUDE.md      : copied from this repo (file symlinks need admin on Windows)
#  - plugins        : user-scope plugins made to match $plugins
#                     missing -> install, disabled -> enable, not listed -> disable (never uninstalled)
#                     project/local-scope plugins are left alone
$ErrorActionPreference = 'Stop'

$marketplaces = @(
    'anthropics/claude-plugins-official'
    'nextlevelbuilder/ui-ux-pro-max-skill'
    'DietrichGebert/ponytail'
)
$plugins = @(
    'frontend-design@claude-plugins-official'
    'ui-ux-pro-max@ui-ux-pro-max-skill'
    'skill-creator@claude-plugins-official'
    'ponytail@ponytail'
)

$repo = $PSScriptRoot
$dst = Join-Path $env:USERPROFILE '.claude'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
New-Item -ItemType Directory -Force $dst | Out-Null

# --- agents, skills -> junction to repo
foreach ($name in 'agents', 'skills') {
    $target = Join-Path $dst $name
    $want = Join-Path $repo $name
    if (Test-Path $target) {
        $item = Get-Item $target -Force
        $old = "$(@($item.Target)[0])".TrimEnd('\')
        if ($item.LinkType -and ($old -eq $want)) {
            Write-Host "ok: $name"
            continue
        }
        if ($item.LinkType) {
            # rmdir on a junction removes only the link, never the folder it points to
            cmd /c rmdir "$target"
            Write-Host "unlinked: $name (was -> $old)"
        } else {
            Rename-Item $target "$name.bak-$stamp"
            Write-Host "backup: $name.bak-$stamp"
        }
    }
    New-Item -ItemType Junction -Path $target -Target $want | Out-Null
    Write-Host "linked: $name -> $want"
}

# --- CLAUDE.md -> copy
$cm = Join-Path $dst 'CLAUDE.md'
$src = Join-Path $repo 'CLAUDE.md'
if ((Test-Path $cm) -and ((Get-FileHash $cm).Hash -ne (Get-FileHash $src).Hash)) {
    Copy-Item $cm "$cm.bak-$stamp"
    Write-Host "backup: CLAUDE.md.bak-$stamp"
}
Copy-Item $src $cm -Force
Write-Host "copied: CLAUDE.md"

# global CLAUDE.md finds this repo through this file (clone location differs per PC)
Set-Content (Join-Path $dst 'claude-config-path.txt') $repo -Encoding ascii
# commits to this repo must use this account (repo-local, global git config untouched)
git -C $repo config user.email 'qwertys1347@gmail.com'

# --- plugins (user scope)
foreach ($m in $marketplaces) { claude plugin marketplace add $m | Out-Null }
# PS 5.1 ConvertFrom-Json emits a JSON array as one object; foreach enumerates it
$all = claude plugin list --json | Out-String | ConvertFrom-Json
$installed = @(foreach ($x in $all) { if ($x.scope -eq 'user') { $x } })
foreach ($p in $plugins) {
    $cur = $installed | Where-Object { $_.id -eq $p } | Select-Object -First 1
    if (-not $cur) { claude plugin install $p --scope user }
    elseif (-not $cur.enabled) { claude plugin enable $p --scope user }
    else { Write-Host "ok: $p" }
}
foreach ($cur in $installed) {
    if ($plugins -notcontains $cur.id -and $cur.enabled) { claude plugin disable $cur.id --scope user }
}

$global:LASTEXITCODE = 0
Write-Host "done. Restart Claude Code."
