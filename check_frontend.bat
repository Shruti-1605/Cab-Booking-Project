@echo off
echo ========================================
echo    CHECKING FRONTEND
echo ========================================

cd "c:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\frontend"

echo.
echo 1. Installing npm dependencies...
npm install

echo.
echo 2. Starting development server...
echo Frontend will run on: http://localhost:3000
echo.
npm run dev