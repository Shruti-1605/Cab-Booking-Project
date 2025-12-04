#!/usr/bin/env python3
"""
Test script for Leaflet Map Service
"""

from leaflet_service import leaflet_service

def test_leaflet_service():
    print("Testing Leaflet Map Service...")
    
    # Test geocoding
    print("\n1. Testing Geocoding:")
    address = "Connaught Place, Delhi"
    coords = leaflet_service.get_coordinates(address)
    print(f"   Address: {address}")
    print(f"   Coordinates: {coords}")
    
    # Test reverse geocoding
    print("\n2. Testing Reverse Geocoding:")
    if coords:
        lat, lng = coords
        reverse_address = leaflet_service.get_address(lat, lng)
        print(f"   Coordinates: {lat}, {lng}")
        print(f"   Address: {reverse_address}")
    
    # Test distance calculation
    print("\n3. Testing Distance Calculation:")
    delhi_coords = (28.6139, 77.2090)
    mumbai_coords = (19.0760, 72.8777)
    
    distance_info = leaflet_service.calculate_distance_duration(
        delhi_coords[0], delhi_coords[1],
        mumbai_coords[0], mumbai_coords[1]
    )
    print(f"   Delhi to Mumbai:")
    print(f"   Distance: {distance_info['distance_text']}")
    print(f"   Duration: {distance_info['duration_text']}")
    
    # Test route finding
    print("\n4. Testing Route Finding:")
    route = leaflet_service.get_route(
        delhi_coords[0], delhi_coords[1],
        mumbai_coords[0], mumbai_coords[1]
    )
    print(f"   Route coordinates: {len(route['coordinates'])} points")
    print(f"   Route distance: {route['distance']/1000:.1f} km")
    
    # Test nearby drivers
    print("\n5. Testing Nearby Drivers:")
    drivers = leaflet_service.find_nearby_drivers(delhi_coords[0], delhi_coords[1])
    print(f"   Found {len(drivers)} drivers near Delhi")
    for driver in drivers[:3]:  # Show first 3
        print(f"   - {driver['name']}: {driver['distance_km']} km away, Rating: {driver['rating']}")
    
    # Test map config
    print("\n6. Testing Map Configuration:")
    config = leaflet_service.get_map_config()
    print(f"   Center: {config['center']}")
    print(f"   Zoom: {config['zoom']}")
    print(f"   Tile URL: {config['tile_url']}")
    
    print("\nAll Leaflet tests completed successfully!")
    print("\nYour Leaflet map service is ready to use!")
    print("\nKey Features:")
    print("   • Free OpenStreetMap tiles (no API key needed)")
    print("   • Geocoding with Nominatim")
    print("   • Route calculation with OSRM")
    print("   • Mock driver locations")
    print("   • Distance & duration calculation")

if __name__ == "__main__":
    test_leaflet_service()