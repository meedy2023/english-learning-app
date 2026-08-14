@echo off
chcp 65001 >nul
title Update API IP

cd /d %~dp0
python 更新IP配置.py
pause