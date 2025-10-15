@echo off
set SCRIPT=crunchyroll_gui_checker_2025.py

python -m nuitka ^
--standalone ^
--onefile ^
--remove-output ^
--windows-disable-console ^
--jobs=12 ^
--include-module=httpx ^
--include-module=colorama ^
--include-module=customtkinter ^
--output-dir=. ^
%SCRIPT%

echo Build complete!
pause
