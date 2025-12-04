@echo off
echo Quick Start - Cab Booking Project

echo Starting Backend...
cd backend
start "Backend" cmd /k "python -m uvicorn main:app --reload --port 8000"

echo Starting Frontend...
cd ../frontend
start "Frontend" cmd /k "npm start"

echo.
echo Project Started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000