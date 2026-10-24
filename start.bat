@echo off
title MasteryLoop Platform Launcher
echo ========================================================
echo           MasteryLoop - Starting Full Stack
echo ========================================================
echo.

echo [1/2] Launching FastAPI Backend on http://127.0.0.1:8000 ...
start "MasteryLoop - Backend (Port 8000)" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Launching React Vite Frontend on http://127.0.0.1:5173 ...
start "MasteryLoop - Frontend (Port 5173)" cmd /k "cd /d "%~dp0frontend" && npm run dev"

timeout /t 3 /nobreak >nul
echo.
echo Opening http://127.0.0.1:5173/ in your browser...
start http://127.0.0.1:5173/

echo.
echo ========================================================
echo Both servers are now running!
echo Web App URL:  http://127.0.0.1:5173/
echo API Swagger:  http://127.0.0.1:8000/docs
echo ========================================================
echo.
echo To stop the servers, simply close the opened command windows.
pause
