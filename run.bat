@echo off
REM Sleep Quality Assessment - Quick Start Script for Windows

echo.
echo ========================================
echo   Sleep Quality Assessment System
echo   Quick Start for Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found
    echo Please run this script from the project directory
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✓ Dependencies installed successfully
echo.

REM Check if model exists
if not exist "sleep_model.h5" (
    echo WARNING: sleep_model.h5 not found
    echo The model file is required for predictions
    echo Please ensure it's in the project directory
    pause
)

echo.
echo ========================================
echo   Starting Sleep Quality Assessment
echo ========================================
echo.
echo Opening browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Start Flask app
timeout /t 2 >nul
start http://localhost:5000
python app.py

pause
