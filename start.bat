@echo off
chcp 65001 >nul
title English Learning App

echo ===============================================
echo   English Learning App - Starting...
echo ===============================================
echo.

cd /d %~dp0

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    echo Please install Python 3 from https://www.python.org/downloads/
    echo Remember to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "backend\.installed" (
    echo [INFO] Installing dependencies for first time...
    python -m pip install fastapi uvicorn --quiet
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
    type nul > "backend\.installed"
    echo [OK] Dependencies installed
)

REM Start the app
echo.
echo [INFO] Starting app...
echo.

start "English App" python start_app.py

echo ===============================================
echo   App is starting!
echo ===============================================
echo.
echo After 3 seconds, browser will open automatically.
echo.
echo Mobile/Pad access: Check IP address after startup.
echo.
timeout /t 5 /nobreak >nul

exit