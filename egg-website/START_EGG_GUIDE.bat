@echo off
setlocal
cd /d "%~dp0"
echo Opening the Egg Guide...
start "" "%~dp0index.html"
echo.
echo This is a static website. No Node.js, npm install, or build step is required.
echo You can close this window.
pause
