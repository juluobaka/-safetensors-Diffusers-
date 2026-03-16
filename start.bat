@echo off
chcp 65001 >nul
title 模型转换工具 (端口9524)

cd /d "%~dp0"

if not exist "main.py" (
    echo [错误] 未找到 main.py
    pause
    exit /b
)

set VENV_NAME=venv
if not exist "%VENV_NAME%\Scripts\python.exe" (
    echo [错误] 未找到虚拟环境 %VENV_NAME%
    pause
    exit /b
)

"%VENV_NAME%\Scripts\python.exe" main.py
pause