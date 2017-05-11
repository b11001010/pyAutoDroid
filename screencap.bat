set DEVICE=127.0.0.1:62001
set ADB="C:\Program Files (x86)\Nox\bin\nox_adb.exe"

%ADB% -s %DEVICE% shell screencap -p /sdcard/screen.png
%ADB% -s %DEVICE% pull /sdcard/screen.png .
%ADB% -s %DEVICE% shell rm /sdcard/screen.png
pause