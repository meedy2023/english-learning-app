@echo off
chcp 65001 >nul
title Backend Service

echo.
echo  ========================================
echo     Backend Service (port 8080)
echo  ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    pause
    exit /b 1
)

cd /d "%~dp0backend"

if not exist "main.py" (
    echo [ERROR] main.py not found
    pause
    exit /b 1
)

echo [START] Uvicorn server...
echo [TIP] Press Ctrl+C to stop
echo [DOC] http://localhost:8080/docs
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8080