@echo off
echo Starting Cab Booking Application...

echo.
echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python -m uvicorn main_advanced:app --reload --port 8000"

echo.
echo [2/2] Starting Frontend Server...
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd frontend-new && npm run dev"

echo.
echo ✅ Both servers started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo Test Page: Open test_app.html in browser
echo.
pause