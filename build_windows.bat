@echo off
setlocal
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean --windowed --name JobTracker main.py
echo.
echo Build complete. See dist\JobTracker\
pause
