$ErrorActionPreference = "Stop"

$repoRoot = Join-Path $PSScriptRoot ".."
$backendDir = Join-Path $repoRoot "backend"

$targets = @(
    (Join-Path $backendDir ".pytest_cache"),
    (Join-Path $backendDir ".mypy_cache"),
    (Join-Path $backendDir ".ruff_cache"),
    (Join-Path $repoRoot ".mypy_cache"),
    (Join-Path $repoRoot ".ruff_cache")
)

foreach ($target in $targets) {
    if (Test-Path $target) {
        Write-Host "Usuwam $target" -ForegroundColor Yellow
        Remove-Item -Path $target -Recurse -Force
    }
}

Get-ChildItem -Path $backendDir -Directory -Recurse -Filter "__pycache__" |
    Where-Object { $_.FullName -notmatch '\\\.venv\\' } |
    ForEach-Object {
        Write-Host "Usuwam $($_.FullName)" -ForegroundColor Yellow
        Remove-Item -Path $_.FullName -Recurse -Force
    }

Write-Host "Backend cleanup: OK" -ForegroundColor Green
