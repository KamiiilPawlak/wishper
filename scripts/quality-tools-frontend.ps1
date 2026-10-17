$ErrorActionPreference = "Stop"

$frontendDir = Join-Path $PSScriptRoot "..\frontend"
$packageJson = Join-Path $frontendDir "package.json"

if (-not (Test-Path $packageJson)) {
    Write-Host "Frontend nie jest jeszcze zainicjalizowany (brak frontend/package.json) - pomijam." -ForegroundColor Yellow
    exit 0
}

Push-Location $frontendDir
try {
    Write-Host "== Lint ==" -ForegroundColor Cyan
    npm run lint
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "== Type check ==" -ForegroundColor Cyan
    npm run typecheck
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "== Test ==" -ForegroundColor Cyan
    npm run test
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "Frontend quality gate: OK" -ForegroundColor Green
}
finally {
    Pop-Location
}
