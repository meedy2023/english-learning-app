@echo off
chcp 65001 >nul
title English Learning App

echo.
echo  ========================================
echo     English Learning App - Starting...
echo  ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    pause
    exit /b 1
)

pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Installing dependencies...
    pip install fastapi uvicorn -q
)

echo [CLEAN] Closing old processes...
taskkill /F /FI "WINDOWTITLE eq Backend*" >nul 2>&1

echo [1/2] Starting backend (port 8080)...
cd /d "%~dp0backend"
start "Backend Service" cmd /c "chcp 65001 >nul & uvicorn main:app --host 0.0.0.0 --port 8080"

echo [WAIT] Backend starting...
timeout /t 3 /nobreak >nul

curl -s http://localhost:8080/api/modules >nul 2>&1
if errorlevel 1 (
    echo [WARN] Backend may have issues
) else (
    echo [OK] Backend: http://localhost:8080
)

echo.
echo [2/2] Opening frontend...
echo.
echo  ========================================
echo   Backend: http://localhost:8080
echo   API Doc: http://localhost:8080/docs
echo  ========================================
echo.
echo  Press any key to open frontend...
pause >nul

start "" "%~dp0frontend\index.html"
echo.
echo [DONE] App started
pause