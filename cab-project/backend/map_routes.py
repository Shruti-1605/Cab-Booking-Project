from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from leaflet_service import leaflet_service

router = APIRouter(prefix="/api/maps", tags=["maps"])

class LocationRequest(BaseModel):
    address: str

class RouteRequest(BaseModel):
    origin_lat: float
    origin_lng: float
    dest_lat: float
    dest_lng: float

class NearbyDriversRequest(BaseModel):
    lat: float
    lng: float
    radius_km: Optional[float] = 5.0

@router.post("/geocode")
async def geocode_address(request: LocationRequest):
    """Convert address to coordinates"""
    try:
        coordinates = leaflet_service.get_coordinates(request.address)
        if coordinates:
            return {
                "lat": coordinates[0],
                "lng": coordinates[1],
                "address": request.address
            }
        else:
            raise HTTPException(status_code=404, detail="Address not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reverse-geocode")
async def reverse_geocode(lat: float, lng: float):
    """Convert coordinates to address"""
    try:
        address = leaflet_service.get_address(lat, lng)
        return {
            "lat": lat,
            "lng": lng,
            "address": address
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/route")
async def get_route(request: RouteRequest):
    """Get route between two points"""
    try:
        route_data = leaflet_service.get_route(
            request.origin_lat, request.origin_lng,
            request.dest_lat, request.dest_lng
        )
        
        distance_duration = leaflet_service.calculate_distance_duration(
            request.origin_lat, request.origin_lng,
            request.dest_lat, request.dest_lng
        )
        
        return {
            "route": route_data,
            "distance": distance_duration,
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/nearby-drivers")
async def find_nearby_drivers(request: NearbyDriversRequest):
    """Find nearby drivers"""
    try:
        drivers = leaflet_service.find_nearby_drivers(
            request.lat, request.lng, request.radius_km
        )
        return {
            "drivers": drivers,
            "count": len(drivers)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/config")
async def get_map_config(lat: Optional[float] = 28.6139, lng: Optional[float] = 77.2090, 
                        zoom: Optional[int] = 13, provider: Optional[str] = "openstreetmap"):
    """Get map configuration"""
    try:
        config = leaflet_service.get_map_config(lat, lng, zoom, provider)
        return config
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/distance")
async def calculate_distance(origin_lat: float, origin_lng: float, 
                           dest_lat: float, dest_lng: float):
    """Calculate distance and duration between two points"""
    try:
        result = leaflet_service.calculate_distance_duration(
            origin_lat, origin_lng, dest_lat, dest_lng
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))