@echo off
chcp 65001 >nul
title Install Dependencies

echo ===============================================
echo   Install Python Dependencies
echo ===============================================
echo.

cd /d %~dp0

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    echo Please install Python 3 from https://www.python.org/downloads/
    echo Remember to check "Add Python to PATH"!
    pause
    exit /b 1
)

echo [INFO] Installing fastapi and uvicorn...
python -m pip install fastapi uvicorn --upgrade

if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed!
    pause
    exit /b 1
)

REM Mark as installed
type nul > "backend\.installed"

echo.
echo ===============================================
echo   [OK] All dependencies installed!
echo ===============================================
echo.
echo You can now run: start.bat
echo.
pause