$ErrorActionPreference = "Stop"

$backendDir = Join-Path $PSScriptRoot "..\backend"

Push-Location $backendDir
try {
    Write-Host "== Ruff lint ==" -ForegroundColor Cyan
    uv run ruff check .
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "== Ruff format check ==" -ForegroundColor Cyan
    uv run ruff format --check .
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "== mypy ==" -ForegroundColor Cyan
    uv run mypy
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "== pytest ==" -ForegroundColor Cyan
    uv run pytest
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "Backend quality gate: OK" -ForegroundColor Green
}
finally {
    Pop-Location
}
