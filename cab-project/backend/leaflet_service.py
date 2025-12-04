import requests
import os
from typing import Dict, List, Tuple, Optional
import random
import math

class LeafletMapService:
    def __init__(self):
        # Leaflet doesn't need API key for basic maps
        # But you can use different tile providers
        self.tile_providers = {
            'openstreetmap': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            'cartodb': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
            'satellite': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        }
        
        # For geocoding, we can use Nominatim (free) or other services
        self.nominatim_url = "https://nominatim.openstreetmap.org"
    
    def get_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """Get latitude and longitude from address using Nominatim"""
        try:
            params = {
                'q': address,
                'format': 'json',
                'limit': 1
            }
            
            response = requests.get(f"{self.nominatim_url}/search", params=params)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return (float(data[0]['lat']), float(data[0]['lon']))
            
            # Fallback to mock coordinates
            return self._get_mock_coordinates(address)
            
        except Exception as e:
            print(f"Geocoding error: {e}")
            return self._get_mock_coordinates(address)
    
    def get_address(self, lat: float, lng: float) -> Optional[str]:
        """Get address from coordinates using reverse geocoding"""
        try:
            params = {
                'lat': lat,
                'lon': lng,
                'format': 'json'
            }
            
            response = requests.get(f"{self.nominatim_url}/reverse", params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('display_name', f"Location at {lat:.4f}, {lng:.4f}")
            
            return f"Location at {lat:.4f}, {lng:.4f}"
            
        except Exception as e:
            print(f"Reverse geocoding error: {e}")
            return f"Location at {lat:.4f}, {lng:.4f}"
    
    def calculate_distance_duration(self, origin_lat: float, origin_lng: float, 
                                  dest_lat: float, dest_lng: float) -> Dict:
        """Calculate distance and duration between two points"""
        # Calculate straight-line distance using Haversine formula
        distance_km = self._haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng)
        
        # Estimate road distance (usually 1.3x straight line)
        road_distance_km = distance_km * 1.3
        
        # Determine speed based on distance (inter-city vs local)
        if road_distance_km > 100:  # Inter-city travel
            avg_speed = random.uniform(60, 80)  # Highway speed
        elif road_distance_km > 20:  # City to city
            avg_speed = random.uniform(40, 60)  # Mixed roads
        else:  # Local travel
            avg_speed = random.uniform(25, 35)  # City traffic
            
        duration_minutes = (road_distance_km / avg_speed) * 60
        
        return {
            'distance_meters': int(road_distance_km * 1000),
            'distance_text': f'{road_distance_km:.1f} km',
            'duration_seconds': int(duration_minutes * 60),
            'duration_text': f'{int(duration_minutes)} mins',
            'start_address': f"{origin_lat:.4f}, {origin_lng:.4f}",
            'end_address': f"{dest_lat:.4f}, {dest_lng:.4f}"
        }
    
    def get_route(self, origin_lat: float, origin_lng: float, 
                  dest_lat: float, dest_lng: float) -> Dict:
        """Get route coordinates for drawing on map"""
        try:
            # Using OSRM (Open Source Routing Machine) - free routing service
            url = f"http://router.project-osrm.org/route/v1/driving/{origin_lng},{origin_lat};{dest_lng},{dest_lat}"
            params = {
                'overview': 'full',
                'geometries': 'geojson'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['routes']:
                    route = data['routes'][0]
                    return {
                        'coordinates': route['geometry']['coordinates'],
                        'distance': route['distance'],
                        'duration': route['duration']
                    }
            
            # Fallback to straight line
            return {
                'coordinates': [[origin_lng, origin_lat], [dest_lng, dest_lat]],
                'distance': self._haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng) * 1000,
                'duration': 900  # 15 minutes default
            }
            
        except Exception as e:
            print(f"Routing error: {e}")
            return {
                'coordinates': [[origin_lng, origin_lat], [dest_lng, dest_lat]],
                'distance': self._haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng) * 1000,
                'duration': 900
            }
    
    def find_nearby_drivers(self, lat: float, lng: float, radius_km: float = 5) -> List[Dict]:
        """Generate mock nearby drivers"""
        drivers = []
        num_drivers = random.randint(3, 8)
        
        for i in range(num_drivers):
            # Generate random location within radius
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0.1, radius_km)
            
            # Convert to lat/lng offset
            lat_offset = (distance / 111.0) * math.cos(angle)  # 1 degree ≈ 111 km
            lng_offset = (distance / (111.0 * math.cos(math.radians(lat)))) * math.sin(angle)
            
            driver_lat = lat + lat_offset
            driver_lng = lng + lng_offset
            
            drivers.append({
                'id': f'driver_{i+1}',
                'name': f'Driver {i+1}',
                'lat': round(driver_lat, 6),
                'lng': round(driver_lng, 6),
                'rating': round(random.uniform(3.5, 5.0), 1),
                'distance_km': round(distance, 2),
                'eta_minutes': int(distance * 2.5)  # Rough ETA calculation
            })
        
        return sorted(drivers, key=lambda x: x['distance_km'])
    
    def _haversine_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _get_mock_coordinates(self, address: str) -> Tuple[float, float]:
        """Generate mock coordinates based on address"""
        # Major Indian cities coordinates
        city_coords = {
            'jaipur': (26.9124, 75.7873),
            'indore': (22.7196, 75.8577),
            'mumbai': (19.0760, 72.8777),
            'delhi': (28.6139, 77.2090),
            'bangalore': (12.9716, 77.5946),
            'chennai': (13.0827, 80.2707),
            'kolkata': (22.5726, 88.3639),
            'hyderabad': (17.3850, 78.4867),
            'pune': (18.5204, 73.8567),
            'ahmedabad': (23.0225, 72.5714)
        }
        
        address_lower = address.lower()
        for city, coords in city_coords.items():
            if city in address_lower:
                return coords
        
        # Default to Delhi with some randomness
        base_lat = 28.6139
        base_lng = 77.2090
        hash_val = hash(address_lower) % 1000
        lat_offset = (hash_val % 100 - 50) * 0.001
        lng_offset = ((hash_val // 100) % 100 - 50) * 0.001
        
        return (base_lat + lat_offset, base_lng + lng_offset)
    
    def get_map_config(self, center_lat: float = 28.6139, center_lng: float = 77.2090, 
                      zoom: int = 13, tile_provider: str = 'openstreetmap') -> Dict:
        """Get map configuration for frontend"""
        return {
            'center': [center_lat, center_lng],
            'zoom': zoom,
            'tile_url': self.tile_providers.get(tile_provider, self.tile_providers['openstreetmap']),
            'attribution': '© OpenStreetMap contributors'
        }

# Global instance
leaflet_service = LeafletMapService()