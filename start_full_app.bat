@echo off
echo ========================================
echo    STARTING FULL CAB BOOKING APP
echo ========================================

echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d \"c:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\backend\" && python main.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d \"c:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\frontend\" && npm run dev"

echo.
echo ========================================
echo    SERVERS STARTING...
echo ========================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo Leaflet Map: http://localhost:3000/leaflet-map.html
echo ========================================

pause