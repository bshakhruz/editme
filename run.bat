@echo off
echo 🤖 Starting DV Lottery Photo Corrector Bot...
echo ================================================

REM Check if .env file exists
if not exist .env (
    echo ❌ .env file not found
    echo Please run setup.bat first or create .env file manually
    pause
    exit /b 1
)

REM Check if image.png exists
if not exist image.png (
    echo ⚠️  Warning: image.png not found
    echo Please add your sample image as 'image.png'
    echo.
)

echo ✅ Starting bot...
python telegram_bot.py

echo.
echo Bot stopped. Press any key to exit...
pause >nul
