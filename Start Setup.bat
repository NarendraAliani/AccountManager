@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if %errorlevel%==0 (
    py -3 "%~dp0setup_bootstrap.py"
    if errorlevel 1 pause
    exit /b %errorlevel%
)

where python >nul 2>&1
if %errorlevel%==0 (
    python "%~dp0setup_bootstrap.py"
    if errorlevel 1 pause
    exit /b %errorlevel%
)

echo Python was not found on this PC.
echo Install Python 3.10 or newer and make sure it is added to PATH.
pause
exit /b 1
