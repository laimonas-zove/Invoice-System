@echo off
echo Setting up EasyInvoice Python environment...
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM Check for Python 3.13 in different locations
set "PYTHON_EXE="
if exist "C:\Program Files\Python313\python.exe" (
    set "PYTHON_EXE=C:\Program Files\Python313\python.exe"
    echo Found Python 3.13 in Program Files
) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
    set "PYTHON_EXE=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe"
    echo Found Python 3.13 in user directory
) else (
    python --version 2>nul | findstr "3.13" >nul
    if !errorlevel! equ 0 (
        set "PYTHON_EXE=python"
        echo Found Python 3.13 in PATH
    ) else (
        echo ERROR: Python 3.13 not found
        echo Please install Python 3.13 first
        pause
        exit /b 1
    )
)

echo Using Python: !PYTHON_EXE!

REM Check if virtual environment already exists
if exist ".venv\Scripts\python.exe" (
    echo Virtual environment already exists, skipping creation...
) else (
    echo Creating virtual environment...
    "!PYTHON_EXE!" -m venv .venv
    if !errorlevel! neq 0 (
        echo ERROR: Failed to create virtual environment
        echo Please ensure Python 3.13 is installed correctly
        pause
        exit /b 1
    )
)

REM Installing dependencies
echo Installing dependencies from requirements.txt...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo ERROR: Failed to install dependencies
    echo Please check your requirements.txt file
    pause
    exit /b 1
)

REM Check if Playwright is already installed
.venv\Scripts\python.exe -c "import playwright" 2>nul
if !errorlevel! neq 0 (
    echo Installing Playwright...
    .venv\Scripts\python.exe -m pip install playwright
    if !errorlevel! neq 0 (
        echo ERROR: Failed to install Playwright
        pause
        exit /b 1
    )
)

echo Installing Playwright browsers (this may take a few minutes)...
.venv\Scripts\python.exe -m playwright install chromium
if !errorlevel! neq 0 (
    echo ERROR: Failed to install Playwright browsers
    echo You can install them later by running: .venv\Scripts\python.exe -m playwright install chromium
    pause
    exit /b 1
)

echo Setup completed successfully!
echo EasyInvoice is ready to use.
