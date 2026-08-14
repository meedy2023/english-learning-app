@echo off
chcp 65001 >nul
title My IP Address

echo ===============================================
echo   Your Network Information
echo ===============================================
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=*" %%b in ("%%a") do (
        echo Your IP: %%b
        echo.
        echo Mobile/Pad access URL: http://%%b:8080
    )
)

echo.
echo Make sure your device is on the same WiFi network!
echo.
pause