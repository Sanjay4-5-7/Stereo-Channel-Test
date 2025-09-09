@echo off
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Choose version:
echo 1. GUI Version (recommended)
echo 2. Simple CLI Version
echo 3. Original Full Version
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo Starting GUI version...
    python headphone_test_gui.py
) else if "%choice%"=="2" (
    echo Starting simple CLI version...
    python headphone_test_simple.py
) else if "%choice%"=="3" (
    echo Starting original version...
    python headphone_test.py
) else (
    echo Invalid choice, starting GUI version...
    python headphone_test_gui.py
)

pause
