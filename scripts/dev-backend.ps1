$ErrorActionPreference = "Stop"

$backendDir = Join-Path $PSScriptRoot "..\backend"
$healthUrl = "http://127.0.0.1:8000/api/v1/health"

$env:PYTHONUNBUFFERED = "1"

Push-Location $backendDir
try {
    $process = Start-Process -FilePath "uv" -ArgumentList @("run", "uvicorn", "app.main:app", "--reload") -NoNewWindow -PassThru

    try {
        $ready = $false
        $elapsed = 0
        while (-not $process.HasExited) {
            if (-not $ready -and $elapsed -lt 30) {
                try {
                    $response = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 2
                    if ($response.StatusCode -eq 200) {
                        Write-Host "Health check OK: $($response.Content)"
                        $ready = $true
                    }
                }
                catch {
                    # server not up yet, keep polling
                }
                $elapsed++
            }
            elseif (-not $ready) {
                Write-Warning "Health endpoint did not respond within 30s."
                $ready = $true
            }

            Start-Sleep -Seconds 1
        }
    }
    finally {
        if (-not $process.HasExited) {
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        }
    }
}
finally {
    Pop-Location
}
