@echo off
title Lynra
color 0d

title Lynra Webhook Spammer
echo [*] Checking for Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found. Downloading Python...

    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -OutFile python-installer.exe"

    echo [*] Installing Python silently...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

    del python-installer.exe

    echo [✓] Python installed.
)

echo [*] Installing required packages...
python -m pip install --upgrade pip
python -m pip install requests colorama

cls
echo [✓] All dependencies installed.
echo.
echo [>] Launching the program...
cls
python main.py

pause