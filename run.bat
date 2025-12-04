@echo off
cd "cab-project\backend"
start "Backend" cmd /k "python -m uvicorn main:app --reload --port 8000"
timeout /t 2 /nobreak >nul
cd ..\frontend
start "Frontend" cmd /k "npm start"
echo Servers starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000