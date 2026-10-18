$ErrorActionPreference = "Stop"

$repoRoot = Join-Path $PSScriptRoot ".."

Push-Location $repoRoot
try {
    docker compose up -d --build
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
    Pop-Location
}
