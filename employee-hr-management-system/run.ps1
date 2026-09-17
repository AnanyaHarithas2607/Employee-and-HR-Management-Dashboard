# Employee & HR Management System Launcher
Set-Location $PSScriptRoot

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Launching Employee & HR Management Dashboard...       " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

if (Test-Path ".\.venv\Scripts\python.exe") {
    Write-Host "Using virtual environment (.venv)..." -ForegroundColor Green
    & ".\.venv\Scripts\python.exe" -m streamlit run app.py
} else {
    Write-Host "Using system Python..." -ForegroundColor Yellow
    python -m streamlit run app.py
}
