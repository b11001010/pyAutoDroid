set DEVICE=127.0.0.1:62001
set ADB=%APPDATA%\Nox\bin\nox_adb

%ADB% -s %DEVICE% shell screencap -p /sdcard/screen.png
%ADB% -s %DEVICE% pull /sdcard/screen.png .
%ADB% -s %DEVICE% shell rm /sdcard/screen.png
pause