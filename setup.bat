@echo off
REM Market Newsletter Generator - Setup Script for Windows

echo.
echo ========================================
echo Market Newsletter Generator - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python is installed
python --version
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Dependencies installed successfully!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Create a .env file by copying .env.example:
echo    copy .env.example .env
echo.
echo 2. Edit .env and add your API keys:
echo    - OpenAI API key from https://platform.openai.com/api-keys
echo    - NewsAPI key from https://newsapi.org
echo    - Gmail address and app password
echo.
echo 3. Run the script:
echo    python main.py
echo.
echo For detailed setup instructions, see README.md
echo.

pause
