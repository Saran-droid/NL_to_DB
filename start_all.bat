@echo off
echo ========================================
echo Starting Natural Language to SQL System
echo ========================================
echo.
echo Starting Backend Server...
start "NL-to-SQL Backend" cmd /k "cd /d %~dp0 && python scripts\start_backend.py"
timeout /t 3 /nobreak > nul
echo.
echo Starting Frontend...
start "NL-to-SQL Frontend" cmd /k "cd /d %~dp0 && python scripts\start_frontend.py"
echo.
echo ========================================
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo ========================================
echo.
echo Press any key to exit (servers will keep running)
pause > nul
