@echo off
echo Starting Cab Booking Project...

echo Installing backend dependencies...
cd backend
pip install -r requirements.txt

echo Starting backend server...
start cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Installing frontend dependencies...
cd ../frontend
npm install

echo Starting frontend server...
start cmd /k "npm start"

echo Project started! 
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
pause