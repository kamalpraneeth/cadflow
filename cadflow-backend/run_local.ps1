Write-Host "Loading environment variables from .env..."
if (Test-Path .env) {
    Get-Content .env | Foreach-Object {
        if ($_ -match '^(?!#)([^=]+)=(.*)$') {
            [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim('"' + "'").Trim(), "Process")
        }
    }
} else {
    Write-Host "Warning: .env file not found!"
}
Write-Host "Setting up Python Virtual Environment..."
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Write-Host "Starting CADFlow Monolith API in background..."
Start-Process -NoNewWindow -FilePath ".\venv\Scripts\uvicorn.exe" -ArgumentList "app.main:app --port 8050" -RedirectStandardOutput "api.log" -RedirectStandardError "api_err.log"

Write-Host "Starting Celery Worker in background..."
Start-Process -NoNewWindow -FilePath ".\venv\Scripts\celery.exe" -ArgumentList "-A app.celery_app worker --loglevel=info" -RedirectStandardOutput "celery.log" -RedirectStandardError "celery_err.log"

Write-Host "All services started! Check api.log and celery.log"
