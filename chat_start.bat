@echo off
setlocal

REM Установить текущий каталог как рабочий
cd /d %~dp0

REM Запустить PowerShell скрипт
powershell -ExecutionPolicy Bypass -File "%~dp0chat_start.ps1"

endlocal
