@echo off
echo Installing required packages...
pip install sounddevice numpy

echo.
echo Starting GUI Headphone Tester...
python headphone_test_gui.py

pause
