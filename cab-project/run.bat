@echo off
echo Starting Cab Booking App...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173

start cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"
timeout /t 3
start cmd /k "cd frontend-new && npm run dev"

echo Both servers started!
pause