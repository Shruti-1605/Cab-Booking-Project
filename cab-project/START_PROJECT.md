# 🚀 Cab Booking Project - Quick Start Guide

## Step 1: Start Backend Server

```bash
cd backend
python run_server.py
```

**Server will start at:** http://localhost:8000

## Step 2: Open Map Interface

Open this file in your browser:
```
frontend/leaflet-map.html
```

## Step 3: Test APIs

Visit: http://localhost:8000/docs (FastAPI Swagger UI)

## 🔧 Available Features

### ✅ Working Features:
- **Maps**: Leaflet integration (no API key needed)
- **Payments**: Stripe integration (your key working)
- **Geocoding**: Address to coordinates
- **Routing**: Route calculation
- **Driver Tracking**: Mock nearby drivers

### 📍 API Endpoints:
- `GET /docs` - API documentation
- `POST /api/maps/geocode` - Address to coordinates
- `POST /api/maps/route` - Get route
- `POST /api/payments/intent` - Create payment
- `POST /api/payments/ride` - Ride payment

### 🗺️ Map Features:
- Interactive map with Leaflet
- Search pickup/drop locations
- Find route between points
- Show nearby drivers
- Click map for location info

## 🧪 Quick Test:

1. **Start server**: `python run_server.py`
2. **Open map**: `leaflet-map.html` in browser
3. **Enter locations**: Type pickup and drop addresses
4. **Click "Find Route"**: See route on map
5. **Click "Find Drivers"**: See nearby drivers

## 🔑 Environment Variables:

Your `.env` file is configured with:
- ✅ Stripe Secret Key (working)
- ⚠️ Stripe Publishable Key (add if needed)
- ⚠️ Google Maps API (not needed for Leaflet)

## 🚨 Troubleshooting:

**If server doesn't start:**
```bash
pip install fastapi uvicorn sqlalchemy python-dotenv requests
```

**If map doesn't load:**
- Check if server is running on port 8000
- Open browser console for errors

## 📱 Next Steps:

1. Add frontend React/Vue app
2. Implement user authentication
3. Add real driver database
4. Deploy to cloud

---
**Your project is ready to run! 🎉**