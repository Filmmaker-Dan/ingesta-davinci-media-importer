@echo off
REM Double-click installer for Windows.
cd /d "%~dp0"
echo Installing Ingesta - Media Importer...
python install.py
if errorlevel 1 (
  echo.
  echo Install failed. If this was a permission error, right-click install.bat
  echo and choose "Run as administrator".
  echo.
  pause
  exit /b 1
)
echo.
echo Done.
pause
