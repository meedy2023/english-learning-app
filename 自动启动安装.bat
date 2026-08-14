@echo off
chcp 65001 >nul
title Install Auto-Start

echo ===============================================
echo   Install Auto-Start Service
echo ===============================================
echo.

REM Get current directory
set "APP_DIR=%~dp0"
set "START_BAT=%APP_DIR%start.bat"

REM Create shortcut using VBScript
set "VBS_FILE=%TEMP%\create_shortcut.vbs"

(
    echo Set WshShell = WScript.CreateObject("WScript.Shell"^)
    echo Set shortcut = WshShell.CreateShortcut("WScript.Shell.Application^".SpecialFolders("Startup"^) ^& "\EnglishLearningApp.lnk"^)
    echo shortcut.TargetPath = "%START_BAT%"
    echo shortcut.WorkingDirectory = "%APP_DIR%"
    echo shortcut.WindowStyle = 7
    echo shortcut.Description = "English Learning App"
    echo shortcut.Save
) > "%VBS_FILE%"

cscript //nologo "%VBS_FILE%"
del "%VBS_FILE%" 2>nul

echo.
echo [OK] Auto-start installed!
echo.
echo App will now start automatically when you log in to Windows.
echo.
echo To uninstall, run: 卸载自启动.bat
echo.
pause