@echo off
cd /d "C:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\backend"
uvicorn main_advanced:app --host 0.0.0.0 --port 8000 --reload
pause