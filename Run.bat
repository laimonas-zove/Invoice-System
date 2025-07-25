@echo off
cd /d "%~dp0"

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate
) else (
    echo [ERROR] Virtual environment not found. Please reinstall the app.
    pause
    exit /b
)

echo Starting EasyInvoice...
start "" /B python run.py
ping 127.0.0.1 -n 3 > nul
start http://127.0.0.1:5000