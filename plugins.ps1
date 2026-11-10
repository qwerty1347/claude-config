# Plugins to install (source of truth for the plugin list). Re-running is safe.
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
foreach ($m in $marketplaces) { claude plugin marketplace add $m }
foreach ($p in $plugins) { claude plugin install $p }
