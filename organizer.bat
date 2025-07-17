@echo off
title Organizer Application - Complete Manager
setlocal enabledelayedexpansion
cls

:MAIN_MENU
echo.
echo ================================================
echo         Organizer Application Manager
echo ================================================
echo.
echo What would you like to do?
echo.
echo [1] Quick Start - Run Application
echo [2] Check Dependencies
echo [3] Install All Dependencies
echo [4] Install Core Dependencies Only
echo [5] Install Optional Dependencies
echo [6] Repair Installation
echo [7] View System Information
echo [8] Exit
echo.
set /p "CHOICE=Enter your choice (1-8): "

if "%CHOICE%"=="1" goto QUICK_START
if "%CHOICE%"=="2" goto CHECK_DEPS
if "%CHOICE%"=="3" goto INSTALL_ALL
if "%CHOICE%"=="4" goto INSTALL_CORE
if "%CHOICE%"=="5" goto INSTALL_OPTIONAL
if "%CHOICE%"=="6" goto REPAIR
if "%CHOICE%"=="7" goto SYSTEM_INFO
if "%CHOICE%"=="8" goto EXIT
echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MAIN_MENU

:QUICK_START
cls
echo ================================================
echo         Quick Start - Running Application
echo ================================================
echo.

REM Check if we're in the correct directory
if not exist "main.py" (
    echo X main.py not found. Please run this from the ORG-MASTER directory.
    echo Current directory: %CD%
    echo.
    pause
    goto MAIN_MENU
)

REM Quick Python check
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X Python not found. Please install Python first.
    echo.
    echo Press any key to go to dependency installation...
    pause >nul
    goto INSTALL_CORE
)

echo + Python found
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo   %%i

REM Quick Pillow check
python -c "import PIL" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ! Pillow missing - installing now...
    pip install Pillow
    if %ERRORLEVEL% NEQ 0 (
        echo X Failed to install Pillow
        echo Press any key to continue anyway...
        pause >nul
    )
)

echo.
echo >> Starting Organizer Application...
echo.
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo X Application encountered an error
    echo.
    set /p "FIX_CHOICE=Try to fix dependencies? (y/n): "
    if /i "!FIX_CHOICE!"=="y" goto REPAIR
)

echo.
pause
goto MAIN_MENU

:CHECK_DEPS
cls
echo ================================================
echo           Dependency Check
echo ================================================
echo.

set "DEPS_OK=1"
set "MISSING_DEPS="

REM Directory check
if not exist "main.py" (
    echo X main.py not found
    set "DEPS_OK=0"
    goto CHECK_RESULT
)

echo [1/8] Checking project structure...
set "REQUIRED_DIRS=ui core utils config"
for %%d in (%REQUIRED_DIRS%) do (
    if not exist "%%d\" (
        echo X Missing directory: %%d\
        set "DEPS_OK=0"
    ) else (
        echo + Directory %%d\ found
    )
)

echo.
echo [2/8] Checking Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X Python not found
    set "DEPS_OK=0"
    set "MISSING_DEPS=!MISSING_DEPS! Python"
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo + %%i
)

echo.
echo [3/8] Checking core dependencies...
python -c "import tkinter" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X tkinter not available
    set "DEPS_OK=0"
) else (
    echo + tkinter available
)

python -c "import PIL" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X Pillow not found
    set "DEPS_OK=0"
    set "MISSING_DEPS=!MISSING_DEPS! Pillow"
) else (
    echo + Pillow available
)

echo.
echo [4/8] Checking Office support...
python -c "import docx" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ! python-docx not found (Word support disabled)
) else (
    echo + python-docx available
)

python -c "import openpyxl" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ! openpyxl not found (Excel support disabled)
) else (
    echo + openpyxl available
)

python -c "import pptx" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ! python-pptx not found (PowerPoint support disabled)
) else (
    echo + python-pptx available
)

python -c "import PyPDF2" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ! PyPDF2 not found (PDF support disabled)
) else (
    echo + PyPDF2 available
)

echo.
echo [5/8] Checking AI Assistant...
python -c "import openai" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ! openai not found (AI Assistant disabled)
) else (
    echo + openai available
)

echo.
echo [6/8] Checking imports...
python -c "from ui.main_window import OrganizerExplorer" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X Main window import failed
    set "DEPS_OK=0"
) else (
    echo + Main window import successful
)

echo.
echo [7/8] Checking file operations...
python -c "from utils.file_utils import get_file_icon" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X File utils import failed
    set "DEPS_OK=0"
) else (
    echo + File utils import successful
)

echo.
echo [8/8] Final assessment...

:CHECK_RESULT
if "%DEPS_OK%"=="1" (
    echo.
    echo + ALL DEPENDENCIES SATISFIED!
    echo.
    echo Your Organizer Application is ready to run.
    echo Optional features may be limited based on installed packages.
    echo.
    set /p "RUN_NOW=Run application now? (y/n): "
    if /i "!RUN_NOW!"=="y" (
        python main.py
    )
) else (
    echo.
    echo X DEPENDENCY CHECK FAILED
    echo.
    echo Missing: !MISSING_DEPS!
    echo.
    set /p "INSTALL_NOW=Install missing dependencies? (y/n): "
    if /i "!INSTALL_NOW!"=="y" goto INSTALL_ALL
)

echo.
pause
goto MAIN_MENU

:INSTALL_ALL
cls
echo ================================================
echo        Install All Dependencies
echo ================================================
echo.

REM Check Python first
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X Python not found. Please install Python first.
    echo   Download from: https://python.org
    echo.
    pause
    goto MAIN_MENU
)

echo + Python found
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo   %%i
echo.

echo Installing all packages...
echo.

echo [1/4] Core dependencies...
pip install Pillow
echo.

echo [2/4] Office support...
pip install python-docx openpyxl python-pptx PyPDF2
echo.

echo [3/4] AI Assistant...
pip install openai
echo.

echo [4/4] Additional utilities...
pip install chardet
echo.

echo Verifying installation...
python -c "import PIL, docx, openpyxl, pptx, PyPDF2, openai; print('All packages verified!')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ! Some packages may not have installed correctly
    echo   This is normal - optional features will be disabled
) else (
    echo + All packages installed and verified!
)

echo.
echo Installation complete!
echo.
set /p "RUN_NOW=Run application now? (y/n): "
if /i "%RUN_NOW%"=="y" (
    python main.py
)

echo.
pause
goto MAIN_MENU

:INSTALL_CORE
cls
echo ================================================
echo        Install Core Dependencies Only
echo ================================================
echo.

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X Python not found
    pause
    goto MAIN_MENU
)

echo + Installing core requirements...
echo.

pip install Pillow
if %ERRORLEVEL% NEQ 0 (
    echo X Failed to install Pillow
) else (
    echo + Pillow installed successfully
)

echo.
echo Core installation complete!
echo Note: Only basic functionality will be available.
echo Use "Install All Dependencies" for full features.
echo.
pause
goto MAIN_MENU

:INSTALL_OPTIONAL
cls
echo ================================================
echo        Install Optional Dependencies
echo ================================================
echo.

echo Installing optional packages for enhanced features...
echo.

echo Office file support...
pip install python-docx openpyxl python-pptx PyPDF2

echo.
echo AI Assistant support...
pip install openai

echo.
echo Additional utilities...
pip install chardet

echo.
echo Optional installation complete!
echo.
pause
goto MAIN_MENU

:REPAIR
cls
echo ================================================
echo           Repair Installation
echo ================================================
echo.

echo Attempting to repair common issues...
echo.

echo [1/5] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/5] Reinstalling core packages...
pip uninstall Pillow -y
pip install Pillow

echo.
echo [3/5] Checking Python path...
python -c "import sys; print('Python executable:', sys.executable)"

echo.
echo [4/5] Verifying imports...
python -c "import tkinter; print('tkinter: OK')" 2>nul || echo "tkinter: FAILED"
python -c "import PIL; print('Pillow: OK')" 2>nul || echo "Pillow: FAILED"

echo.
echo [5/5] Testing application import...
python -c "from ui.main_window import OrganizerExplorer; print('Main application: OK')" 2>nul || echo "Main application: FAILED"

echo.
echo Repair complete!
echo.
pause
goto MAIN_MENU

:SYSTEM_INFO
cls
echo ================================================
echo           System Information
echo ================================================
echo.

echo Operating System:
ver

echo.
echo Python Information:
python --version 2>nul || echo "Python not found"
python -c "import sys; print('Python path:', sys.executable)" 2>nul

echo.
echo Current Directory:
echo %CD%

echo.
echo Project Structure:
if exist "main.py" (echo + main.py) else (echo - main.py)
if exist "ui\" (echo + ui\) else (echo - ui\)
if exist "core\" (echo + core\) else (echo - core\)
if exist "utils\" (echo + utils\) else (echo - utils\)
if exist "config\" (echo + config\) else (echo - config\)

echo.
echo Installed Python Packages:
pip list | findstr -i "pillow docx openpyxl pptx pypdf2 openai chardet" 2>nul

echo.
echo Environment Variables:
echo PATH (Python entries):
echo %PATH% | findstr -i python

echo.
pause
goto MAIN_MENU

:EXIT
echo.
echo Thank you for using Organizer Application!
echo.
exit /b 0
