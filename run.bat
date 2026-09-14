@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>&1
if errorlevel 1 (
  echo Python was not found. Install Python 3.11-3.13 and try again.
  pause
  exit /b 1
)
echo ===============================================
echo   Hospitality Academy V8.4
 echo   Training Operating System - Windows Start
 echo ===============================================
echo.
python -c "import sys; print('Python:',sys.version)"
python -m pip install --user --no-cache-dir -r requirements.txt
if errorlevel 1 (
  echo.
  echo Dependency installation failed.
  echo If you see Errno 28 / No space left on device, free space and rerun.
  pause
  exit /b 1
)
echo.
echo Starting server at http://127.0.0.1:8000 ...
start "Hospitality Academy" http://127.0.0.1:8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
