$ErrorActionPreference = "Stop"

$frontendDir = Join-Path $PSScriptRoot "..\frontend"

$targets = @(
    (Join-Path $frontendDir "node_modules"),
    (Join-Path $frontendDir "dist"),
    (Join-Path $frontendDir "build"),
    (Join-Path $frontendDir ".next"),
    (Join-Path $frontendDir "coverage")
)

foreach ($target in $targets) {
    if (Test-Path $target) {
        Write-Host "Usuwam $target" -ForegroundColor Yellow
        Remove-Item -Path $target -Recurse -Force
    }
}

Write-Host "Frontend cleanup: OK" -ForegroundColor Green
