# Cài HW02 skills vào Cursor (project scope)
$source = Join-Path $PSScriptRoot "skills"
$target = Join-Path (Split-Path $PSScriptRoot -Parent) ".cursor\skills"

if (-not (Test-Path $target)) {
    New-Item -ItemType Directory -Path $target -Force | Out-Null
}

Get-ChildItem $source -Directory | ForEach-Object {
    $dest = Join-Path $target $_.Name
    if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
    Copy-Item $_.FullName $dest -Recurse -Force
    Write-Host "Installed: $($_.Name)"
}

Write-Host ""
Write-Host "Done. Restart Cursor chat, then type @hw02-workflow"
