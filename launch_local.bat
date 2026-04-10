@echo off
setlocal
cd /d "%~dp0"

set "VENV_PY=%~dp0.venv\Scripts\python.exe"
set "BOOTSTRAP=%~dp0setup_bootstrap.py"
set "SERVER_URL=http://127.0.0.1:8000/login/"

if exist "%~dp0setup.done" if exist "%VENV_PY%" (
    echo Setup already completed. Starting the local server...
    start "" "%VENV_PY%" manage.py runserver 127.0.0.1:8000 --noreload
    timeout /t 3 /nobreak >nul
    start "" "%SERVER_URL%"
    exit /b 0
)

if exist "%VENV_PY%" (
    echo Starting the bootstrap flow with the existing virtual environment...
    "%VENV_PY%" "%BOOTSTRAP%"
    if errorlevel 1 pause
    exit /b %errorlevel%
)

where py >nul 2>&1
if %errorlevel%==0 (
    echo Starting the bootstrap flow using Python Launcher...
    py -3 "%BOOTSTRAP%"
    if errorlevel 1 pause
    exit /b %errorlevel%
)

where python >nul 2>&1
if %errorlevel%==0 (
    echo Starting the bootstrap flow using Python on PATH...
    python "%BOOTSTRAP%"
    if errorlevel 1 pause
    exit /b %errorlevel%
)

echo Python was not found on this PC.
echo Install Python 3.10+ and make sure it is added to PATH.
pause
exit /b 1
