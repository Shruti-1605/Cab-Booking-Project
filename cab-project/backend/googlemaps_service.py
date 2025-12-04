import googlemaps
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class GoogleMapsService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY", "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjliMDVkNDkyOGJiNjQ2Yjc5OTk4Y2RlYjYyMWJlZmI0IiwiaCI6Im11cm11cjY0In0=")
        try:
            if self.api_key != "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjliMDVkNDkyOGJiNjQ2Yjc5OTk4Y2RlYjYyMWJlZmI0IiwiaCI6Im11cm11cjY0In0=":
                self.client = googlemaps.Client(key=self.api_key)
            else:
                self.client = None
        except Exception:
            self.client = None
    
    def get_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """Get latitude and longitude from address"""
        if self.client:
            try:
                geocode_result = self.client.geocode(address)
                if geocode_result:
                    location = geocode_result[0]['geometry']['location']
                    return (location['lat'], location['lng'])
            except Exception as e:
                print(f"Geocoding error: {e}")
        
        # Mock coordinates for demo
        import random
        return (28.6139 + random.uniform(-0.1, 0.1), 77.2090 + random.uniform(-0.1, 0.1))
    
    def get_address(self, lat: float, lng: float) -> Optional[str]:
        """Get address from coordinates"""
        if self.client:
            try:
                reverse_geocode_result = self.client.reverse_geocode((lat, lng))
                if reverse_geocode_result:
                    return reverse_geocode_result[0]['formatted_address']
            except Exception as e:
                print(f"Reverse geocoding error: {e}")
        
        # Mock address for demo
        return f"Address near {lat:.4f}, {lng:.4f}"
    
    def calculate_distance_duration(self, origin: str, destination: str) -> Dict:
        """Calculate distance and duration between two points"""
        # Simple distance calculation based on location names
        import random
        
        # Calculate rough distance based on location names
        origin_lower = origin.lower()
        destination_lower = destination.lower()
        
        # Different city distances
        if any(city in origin_lower for city in ['mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata']):
            if any(city in destination_lower for city in ['mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata']):
                # Inter-city travel
                base_distance = random.randint(15, 50)
            else:
                # City to local area
                base_distance = random.randint(8, 25)
        else:
            # Local travel
            base_distance = random.randint(2, 15)
        
        # Add some randomness based on location length (more specific = shorter)
        location_factor = max(0.5, min(2.0, (len(origin) + len(destination)) / 50))
        final_distance = int(base_distance * location_factor)
        
        # Calculate time (assuming 30-40 km/h average speed)
        time_minutes = int(final_distance * random.uniform(2.5, 4.0))
        
        return {
            'distance_meters': final_distance * 1000,
            'distance_text': f'{final_distance} km',
            'duration_seconds': time_minutes * 60,
            'duration_text': f'{time_minutes} mins',
            'start_address': origin,
            'end_address': destination
        }
    
    def calculate_fare(self, distance_km: float, duration_minutes: float, 
                      base_rate: float = 50, per_km_rate: float = 12, 
                      per_minute_rate: float = 2, surge_multiplier: float = 1.0) -> Dict:
        """Calculate fare based on distance and time"""
        base_fare = base_rate
        distance_fare = distance_km * per_km_rate
        time_fare = duration_minutes * per_minute_rate
        
        subtotal = base_fare + distance_fare + time_fare
        surge_amount = subtotal * (surge_multiplier - 1) if surge_multiplier > 1 else 0
        total_fare = subtotal + surge_amount
        
        return {
            'base_fare': base_fare,
            'distance_fare': distance_fare,
            'time_fare': time_fare,
            'surge_amount': surge_amount,
            'surge_multiplier': surge_multiplier,
            'subtotal': subtotal,
            'total_fare': round(total_fare, 2),
            'distance_km': distance_km,
            'duration_minutes': duration_minutes
        }
    
    def find_nearby_drivers(self, lat: float, lng: float, radius_km: float = 5) -> List[Dict]:
        """Find nearby drivers"""
        import random
        
        # Generate mock drivers for demo
        drivers = []
        for i in range(random.randint(3, 7)):
            driver_lat = lat + random.uniform(-0.01, 0.01)
            driver_lng = lng + random.uniform(-0.01, 0.01)
            drivers.append({
                'id': f'driver_{i+1}',
                'name': f'Driver {i+1}',
                'lat': driver_lat,
                'lng': driver_lng,
                'rating': round(random.uniform(3.5, 5.0), 1),
                'distance_km': self._calculate_distance(lat, lng, driver_lat, driver_lng)
            })
        
        return sorted(drivers, key=lambda x: x['distance_km'])
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        from math import radians, cos, sin, asin, sqrt
        
        # Convert to radians
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        
        # Haversine formula
        dlng = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers
        
        return round(c * r, 2)

# Global instance
maps_service = GoogleMapsService()