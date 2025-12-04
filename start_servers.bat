@echo off
echo Starting Cab Booking Application...

echo Starting Backend Server...
start "Backend" cmd /k "cd /d C:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\backend && uvicorn main_advanced:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3

echo Starting Frontend Server...
start "Frontend" cmd /k "cd /d C:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\frontend-new && npm run dev"

echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
pause