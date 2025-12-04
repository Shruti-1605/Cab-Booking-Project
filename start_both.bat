@echo off
echo ========================================
echo    STARTING CAB BOOKING APP
echo ========================================

echo Installing Backend Dependencies...
cd "c:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\backend"
pip install fastapi uvicorn sqlalchemy pydantic requests python-multipart

echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d \"c:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\backend\" && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo Installing Frontend Dependencies...
cd "c:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\frontend"
call npm install

echo.
echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d \"c:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\frontend\" && npm start"

echo.
echo ========================================
echo    BOTH SERVERS STARTING...
echo ========================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo ========================================

timeout /t 5 /nobreak >nul
echo Opening browser...
start http://localhost:3000
start http://localhost:8000/docs

pause