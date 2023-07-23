echo off

pyinstaller --noconfirm --onefile --windowed --icon "icon.ico" "main.py"


rmdir /s /q __pycache__
rmdir /s /q build

:cmd
pause null