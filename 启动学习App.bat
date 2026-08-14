@echo off
chcp 65001 > nul
echo.
echo  ==============================================
echo       English Learning App - Starting...
echo  ==============================================
echo.

REM Kill any existing backend on port 8080
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do (
    echo Stopping existing backend (PID: %%a)...
    taskkill /F /PID %%a > nul 2>&1
)

REM Start backend in new window
echo [1/2] Starting backend server...
cd /d "%~dp0backend"
start "English App Backend" cmd /k "python -m uvicorn main:app --reload --port 8080"

REM Wait for backend to start
timeout /t 3 /nobreak > nul

REM Open frontend in browser
echo [2/2] Opening browser...
start "" "frontend\index.html"

echo.
echo  ==============================================
echo   Backend:  http://localhost:8080
echo   Frontend: frontend\index.html (opened)
echo  ==============================================
echo.
echo  Press Ctrl+C in backend window to stop.
pause