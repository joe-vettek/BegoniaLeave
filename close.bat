cd /d %~dp0
for /f "tokens=1" %%i in ('wmic process where "commandline like '%%bin\\python\\python.exe%%'" get processid ^| findstr /r "[0-9][0-9]*"') do taskkill /f /pid %%i

pause