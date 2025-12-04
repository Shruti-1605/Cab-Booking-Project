@echo off
echo Starting Cab Booking App...

echo Starting Backend...
start "Backend Server" cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"

timeout /t 3

echo Starting Frontend...
start "Frontend Server" cmd /k "cd frontend-new && npm run dev"

echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Both servers are running in separate windows!
pause