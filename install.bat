@echo off
pip install win10toast-persist PIL

echo cd "%cd%" > "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\cmmnotifier.bat"
echo "%cd%\runModule.bat" >> "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\cmmnotifier.bat"
echo pause >> "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\cmmnotifier.bat"