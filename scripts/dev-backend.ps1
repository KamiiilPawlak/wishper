$ErrorActionPreference = "Stop"

$backendDir = Join-Path $PSScriptRoot "..\backend"

Push-Location $backendDir
try {
    uv run uvicorn app.main:app --reload
}
finally {
    Pop-Location
}
