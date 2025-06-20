@echo off
echo Starting Switchboard...
echo Current directory: %CD%
echo Python version:
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found in PATH!
    pause
    exit /B 1
)

cd /d "%~dp0"
echo Switchboard directory: %CD%
set PYTHONPATH=%~dp0;%PYTHONPATH%
echo PYTHONPATH: %PYTHONPATH%

echo Launching Switchboard...
python -m switchboard %*
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to launch Switchboard!
    pause
    exit /B %ERRORLEVEL%
)

echo Switchboard closed.
pause
