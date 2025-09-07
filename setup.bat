@echo off
echo 🚀 Setting up DV Lottery Photo Corrector Bot...
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Run setup script
echo Running setup script...
python setup.py

echo.
echo Setup completed! Press any key to exit...
pause >nul
