@echo off
echo ========================================
echo    QUICK TEST - CAB BOOKING APP
echo ========================================

cd "c:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\cab-project\backend"

echo 1. Testing Leaflet Map Service...
python test_leaflet.py

echo.
echo 2. Opening Test Map in Browser...
start "" "c:\Users\shruti chohan\OneDrive\Desktop\Cab_booking_project\test_leaflet_map.html"

echo.
echo ========================================
echo    TEST COMPLETED!
echo ========================================
echo - Leaflet service tested
echo - Test map opened in browser
echo - Ready to start full app!
echo ========================================

pause