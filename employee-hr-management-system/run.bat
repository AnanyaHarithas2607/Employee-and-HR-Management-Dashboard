@echo off
TITLE Employee & HR Management Dashboard
echo ========================================================
echo   Starting Employee & HR Management System Dashboard...
echo ========================================================
cd /d "%~dp0"

IF EXIST ".venv\Scripts\python.exe" (
    echo Using virtual environment in .venv...
    ".venv\Scripts\python.exe" -m streamlit run app.py
) ELSE (
    echo Using system Python...
    python -m streamlit run app.py
)

pause
