# Map integration and business logic
from leaflet_service import leaflet_service
from typing import Optional

def get_directions(pickup_lat: float, pickup_lng: float, drop_lat: float, drop_lng: float) -> Optional[dict]:
    """Get directions and distance using Leaflet service"""
    try:
        result = leaflet_service.calculate_distance_duration(
            pickup_lat, pickup_lng, drop_lat, drop_lng
        )
        return {
            "distance": result["distance_meters"],
            "duration": result["duration_seconds"],
            "route": "Leaflet route data"
        }
    except Exception as e:
        print(f"Directions API error: {e}")
        return None

def get_fare_estimate(distance_meters: int, duration_seconds: int) -> float:
    """Calculate fare based on distance and time"""
    base_fare = 50.0  # Base fare in rupees
    per_km_rate = 12.0  # Rate per kilometer
    per_minute_rate = 2.0  # Rate per minute
    
    distance_km = distance_meters / 1000
    duration_minutes = duration_seconds / 60
    
    fare = base_fare + (distance_km * per_km_rate) + (duration_minutes * per_minute_rate)
    return round(fare, 2)

def find_nearby_drivers(pickup_lat: float, pickup_lng: float, radius_km: float = 5.0):
    """Find nearby available drivers using Leaflet service"""
    try:
        drivers = leaflet_service.find_nearby_drivers(pickup_lat, pickup_lng, radius_km)
        return [
            {
                "driver_id": driver["id"],
                "distance": driver["distance_km"],
                "eta": driver["eta_minutes"]
            }
            for driver in drivers
        ]
    except Exception as e:
        print(f"Driver search error: {e}")
        return []