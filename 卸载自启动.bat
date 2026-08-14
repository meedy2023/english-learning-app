@echo off
chcp 65001 >nul
title Uninstall Auto-Start

echo ===============================================
echo   Uninstall Auto-Start Service
echo ===============================================
echo.

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
del /f /q "%STARTUP_FOLDER%\EnglishLearningApp.lnk" 2>nul

if exist "%STARTUP_FOLDER%\EnglishLearningApp.lnk" (
    echo [ERROR] Failed to remove!
) else (
    echo [OK] Auto-start removed!
)

echo.
pause