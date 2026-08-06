@echo off
REM R0 legacy inventory only. Run on an authorized isolated XP/Vista/7/8.x system.
REM This script does not call WMIC product and does not change configuration.
set "OUT=%~1"
if "%OUT%"=="" exit /b 10
if not exist "%OUT%" mkdir "%OUT%"
systeminfo > "%OUT%\systeminfo.txt" 2>&1
ipconfig /all > "%OUT%\ipconfig.txt" 2>&1
driverquery /v /fo csv > "%OUT%\drivers.csv" 2>&1
sc query type= service state= all > "%OUT%\services.txt" 2>&1
exit /b 0
