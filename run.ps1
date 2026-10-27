
param(
    [Parameter(Position = 0, Mandatory = $true)]
    [ValidateSet("quality-backend", "quality-frontend", "quality", "cleanup-backend", "cleanup-frontend", "cleanup", "dev-backend", "dev-frontend", "docker-up", "venv", "venv-stop")]
    [string]$Command
)

$ErrorActionPreference = "Stop"
$scriptsDir = Join-Path $PSScriptRoot "scripts"

function Invoke-QualityBackend {
    & (Join-Path $scriptsDir "quality-tools-backend.ps1")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Invoke-QualityFrontend {
    & (Join-Path $scriptsDir "quality-tools-frontend.ps1")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Invoke-CleanupBackend {
    & (Join-Path $scriptsDir "cleanup-backend.ps1")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Invoke-CleanupFrontend {
    & (Join-Path $scriptsDir "cleanup-frontend.ps1")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Invoke-VenvActivate {
    $activateScript = Join-Path $PSScriptRoot "backend\.venv\Scripts\Activate.ps1"
    if (-not (Test-Path $activateScript)) {
        Write-Error "Nie znaleziono $activateScript. Uruchom 'uv sync' w backend/, aby utworzyc .venv."
        exit 1
    }
    & $activateScript
    Write-Host "Backend .venv aktywowane ($env:VIRTUAL_ENV)." -ForegroundColor Green
}

function Invoke-VenvDeactivate {
    if (Get-Command deactivate -ErrorAction SilentlyContinue) {
        deactivate
        Write-Host "Backend .venv deaktywowane." -ForegroundColor Yellow
    }
    else {
        Write-Warning "Brak aktywnego venv w tej sesji."
    }
}

switch ($Command) {
    "quality-backend" { Invoke-QualityBackend }
    "quality-frontend" { Invoke-QualityFrontend }
    "quality" {
        Invoke-QualityBackend
        Invoke-QualityFrontend
    }
    "cleanup-backend" { Invoke-CleanupBackend }
    "cleanup-frontend" { Invoke-CleanupFrontend }
    "cleanup" {
        Invoke-CleanupBackend
        Invoke-CleanupFrontend
    }
    "dev-backend" { & (Join-Path $scriptsDir "dev-backend.ps1") }
    "dev-frontend" { & (Join-Path $scriptsDir "dev-frontend.ps1") }
    "docker-up" { & (Join-Path $scriptsDir "docker-up.ps1") }
    "venv" { Invoke-VenvActivate }
    "venv-stop" { Invoke-VenvDeactivate }
}
