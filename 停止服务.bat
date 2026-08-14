@echo off
chcp 65001 >nul
title Stop English App

echo Stopping English Learning App...

REM Kill python processes for the app
taskkill /F /FI "WINDOWTITLE eq English App*" /T 2>nul
taskkill /F /IM python.exe /FI "MEMUSAGE gt 50000" /T 2>nul

REM Alternative: kill uvicorn specifically
for /f "tokens=*" %%i in ('netstat -ano ^| findstr ":8080" ^| findstr LISTENING') do (
    set "pid=%%i"
    for /f "tokens=4" %%j in ("%%i") do (
        echo Killing PID %%j on port 8080
        taskkill /F /PID %%j /T 2>nul
    )
)

echo.
echo Done! App stopped.
timeout /t 3 /nobreak >nul
exit