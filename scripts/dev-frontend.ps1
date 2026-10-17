$ErrorActionPreference = "Stop"

$frontendDir = Join-Path $PSScriptRoot "..\frontend"
$packageJson = Join-Path $frontendDir "package.json"

if (-not (Test-Path $packageJson)) {
    Write-Host "Frontend nie jest jeszcze zainicjalizowany (brak frontend/package.json)." -ForegroundColor Yellow
    exit 1
}

Push-Location $frontendDir
try {
    npm run dev
}
finally {
    Pop-Location
}
