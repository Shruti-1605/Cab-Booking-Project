@echo off
echo 🚗 Starting Complete Cab Booking App...
echo.

cd /d "%~dp0"

echo [1/2] Starting Backend Server...
start "Backend" cmd /k "cd backend && python -m uvicorn main_advanced:app --reload --port 8000"

echo [2/2] Starting Frontend Server...
timeout /t 3 /nobreak >nul
start "Frontend" cmd /k "cd frontend-new && npm run dev"

echo.
echo ✅ App Started Successfully!
echo 📱 Frontend: http://localhost:5173
echo 🔧 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >nul