@echo off
echo Starting Cab Booking Project...

echo.
echo [1/4] Installing Backend Dependencies...
cd backend
pip install -r requirements.txt

echo.
echo [2/4] Starting Backend Server...
start "Backend Server" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo [3/4] Installing Frontend Dependencies...
cd ../frontend
npm install

echo.
echo [4/4] Starting Frontend Server...
start "Frontend Server" cmd /k "npm start"

echo.
echo ========================================
echo   CAB BOOKING PROJECT STARTED!
echo ========================================
echo Backend API: http://localhost:8000
echo Frontend App: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
pause