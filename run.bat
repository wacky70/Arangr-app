@echo off
title Organizer Application
cls

echo.
echo ================================================
echo           Organizer Application
echo        Starting Application...
echo ================================================
echo.

REM Check if we're in the correct directory
if not exist "main.py" (
    echo X main.py not found. Please run this from the ORG-MASTER directory.
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

REM Check Python installation
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X Python not found in PATH
    echo.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Display Python version
echo + Python found
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo   %%i

REM Check for required directories
if not exist "ui\" (
    echo X UI directory missing. Project structure may be incomplete.
    pause
    exit /b 1
)

REM Check for Pillow (required dependency)
python -c "import PIL" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ! Pillow not found. Installing...
    pip install Pillow
    if %ERRORLEVEL% NEQ 0 (
        echo X Failed to install Pillow. Please run: pip install Pillow
        pause
        exit /b 1
    )
    echo + Pillow installed successfully
)

echo.
echo >> Starting application...
echo.

REM Run the application
python main.py

REM Check exit code
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo X Application exited with error code %ERRORLEVEL%
    echo.
    echo Common solutions:
    echo   - Install missing dependencies: pip install -r requirements.txt
    echo   - Check if all files are present in the project directory
    echo   - Ensure Python version is 3.6 or higher
    echo.
    pause
) else (
    echo.
    echo + Application closed successfully
)

REM Clean exit
exit /b 0