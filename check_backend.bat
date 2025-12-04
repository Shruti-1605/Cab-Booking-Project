@echo off
echo ========================================
echo    CHECKING BACKEND SERVER
echo ========================================

cd "c:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\backend"

echo.
echo 1. Installing requirements...
pip install -r requirements.txt

echo.
echo 2. Testing Leaflet service...
python test_leaflet.py

echo.
echo 3. Starting FastAPI server...
echo Backend will run on: http://localhost:8000
echo API docs available at: http://localhost:8000/docs
echo.
python main.py