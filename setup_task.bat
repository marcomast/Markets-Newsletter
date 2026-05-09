@echo off
REM Market Newsletter Generator - Task Scheduler Setup
REM This script creates a Windows Task Scheduler task to run the newsletter daily

echo.
echo ========================================
echo Task Scheduler Setup
echo ========================================
echo.
echo This script will set up an automated daily task to run the market newsletter.
echo.

REM Get the current directory
setlocal enabledelayedexpansion
set SCRIPT_DIR=%~dp0
set PYTHON_EXE=%1

if "%PYTHON_EXE%"=="" (
    echo What time should the newsletter run daily?
    echo Enter as HH:MM in 24-hour format ^(e.g., 18:00 for 6 PM^)
    set /p TASK_TIME="Time: "
) else (
    set TASK_TIME=%2
)

if "%TASK_TIME%"=="" (
    set TASK_TIME=18:00
    echo Using default time: 18:00 ^(6 PM^)
)

echo.
echo Task will run at: %TASK_TIME%
echo Script location: %SCRIPT_DIR%
echo.

REM Find Python executable
for /f "tokens=*" %%i in ('where python') do set PYTHON_EXE=%%i

if "%PYTHON_EXE%"=="" (
    echo Error: Python not found in PATH
    pause
    exit /b 1
)

echo Python found at: %PYTHON_EXE%
echo.

REM Create task
echo Creating scheduled task...
echo.

schtasks /create ^
    /tn "Market Newsletter Generator" ^
    /tr "\"%PYTHON_EXE%\" \"%SCRIPT_DIR%main.py\"" ^
    /sc daily ^
    /st %TASK_TIME% ^
    /f

if errorlevel 1 (
    echo Error: Failed to create task. You may need to run as Administrator.
    echo.
    echo To run as Administrator:
    echo   1. Right-click Command Prompt
    echo   2. Select "Run as administrator"
    echo   3. Navigate to this folder
    echo   4. Run: setup_task.bat
    pause
    exit /b 1
)

echo.
echo ========================================
echo Task created successfully!
echo ========================================
echo.
echo Task name: Market Newsletter Generator
echo Schedule: Daily at %TASK_TIME%
echo.
echo To view or modify the task:
echo   - Open Task Scheduler ^(search "Task Scheduler"^)
echo   - Find "Market Newsletter Generator" under Task Scheduler Library
echo.
echo To run immediately for testing:
echo   - Right-click the task and select "Run"
echo.
echo To delete the task:
echo   schtasks /delete "Market Newsletter Generator" /f
echo.

pause
