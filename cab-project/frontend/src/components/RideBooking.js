import React, { useState, useEffect } from 'react';
import { rideAPI } from '../services/api';
import MapComponent from './MapComponent';
import PaymentComponent from './PaymentComponent';
import VehicleSelector from './VehicleSelector';

const RideBooking = () => {
  const [pickup, setPickup] = useState({ lat: null, lng: null, address: '' });
  const [destination, setDestination] = useState({ lat: null, lng: null, address: '' });
  const [selectedVehicle, setSelectedVehicle] = useState('sedan');
  const [selectedCar, setSelectedCar] = useState(null);
  const [fareEstimate, setFareEstimate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [rideId, setRideId] = useState(null);
  const [showMap, setShowMap] = useState(true);
  const [showPayment, setShowPayment] = useState(false);
  const [estimatedFare, setEstimatedFare] = useState(null);
  const [routeInfo, setRouteInfo] = useState(null);

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        setPickup({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
          address: 'Current Location'
        });
      });
    }
  };

  // Simple geocoding function (for demo - uses approximate coordinates)
  const geocodeAddress = (address) => {
    // Real coordinates for major Indian cities
    const locations = {
      // Major cities
      'mumbai': { lat: 19.0760, lng: 72.8777 },
      'delhi': { lat: 28.6139, lng: 77.2090 },
      'bangalore': { lat: 12.9716, lng: 77.5946 },
      'pune': { lat: 18.5204, lng: 73.8567 },
      'chennai': { lat: 13.0827, lng: 80.2707 },
      'kolkata': { lat: 22.5726, lng: 88.3639 },
      'hyderabad': { lat: 17.3850, lng: 78.4867 },
      'ahmedabad': { lat: 23.0225, lng: 72.5714 },
      'jaipur': { lat: 26.9124, lng: 75.7873 },
      'indore': { lat: 22.7196, lng: 75.8577 },
      
      // MP cities
      'bhopal': { lat: 23.2599, lng: 77.4126 },
      'indore': { lat: 22.7196, lng: 75.8577 },
      'gwalior': { lat: 26.2183, lng: 78.1828 },
      'jabalpur': { lat: 23.1815, lng: 79.9864 },
      'ujjain': { lat: 23.1765, lng: 75.7885 },
      'sagar': { lat: 23.8388, lng: 78.7378 },
      'dewas': { lat: 22.9676, lng: 76.0534 },
      'satna': { lat: 24.5854, lng: 80.8322 },
      'ratlam': { lat: 23.3315, lng: 75.0367 },
      'harda': { lat: 22.3442, lng: 77.0953 },
      'handiya': { lat: 22.9676, lng: 76.0534 }, // Near Dewas
      
      // Common locations
      'airport': { lat: 28.5562, lng: 77.1000 },
      'railway station': { lat: 28.6430, lng: 77.2197 },
      'current location': { lat: 28.6139, lng: 77.2090 }
    };
    
    const key = address.toLowerCase().trim();
    
    // Exact match first
    if (locations[key]) {
      return locations[key];
    }
    
    // Partial match
    for (let loc in locations) {
      if (key.includes(loc) || loc.includes(key)) {
        return locations[loc];
      }
    }
    
    // Default to Delhi if no match
    return { lat: 28.6139, lng: 77.2090 };
  };

  const calculateRouteInfo = (pickupCoords, destCoords) => {
    // Real distance calculation using Haversine formula
    const R = 6371; // Earth's radius in km
    const dLat = (destCoords.lat - pickupCoords.lat) * Math.PI / 180;
    const dLng = (destCoords.lng - pickupCoords.lng) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(pickupCoords.lat * Math.PI / 180) * Math.cos(destCoords.lat * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    let distance = R * c;
    
    // Road distance is typically 1.2-1.4x straight line distance
    distance = distance * 1.3;
    
    // Realistic speed calculation based on distance
    let avgSpeed;
    if (distance > 100) {
      avgSpeed = 60; // Highway speed
    } else if (distance > 20) {
      avgSpeed = 45; // City roads
    } else if (distance > 5) {
      avgSpeed = 30; // Local roads
    } else {
      avgSpeed = 20; // City traffic
    }
    
    const timeHours = distance / avgSpeed;
    const timeMinutes = Math.round(timeHours * 60);
    
    // Fare calculation based on distance
    let baseFare = 50;
    let perKmRate = 12;
    if (distance > 100) {
      perKmRate = 8; // Lower rate for long distance
      baseFare = 200;
    } else if (distance > 50) {
      perKmRate = 10;
      baseFare = 100;
    }
    
    const fare = Math.round(baseFare + (distance * perKmRate));
    
    return {
      distance: distance.toFixed(1),
      timeMinutes: timeMinutes,
      timeText: timeMinutes > 60 ? 
        `${Math.floor(timeMinutes/60)}h ${timeMinutes%60}m` : 
        `${timeMinutes} mins`,
      fare: fare
    };
  };

  const handleBookRide = async () => {
    if (!pickup.address || !destination.address) {
      alert('Please enter both pickup and destination addresses');
      return;
    }

    // Set coordinates if not already set
    let pickupCoords = pickup;
    let destCoords = destination;
    
    if (!pickup.lat) {
      const coords = geocodeAddress(pickup.address);
      pickupCoords = { ...pickup, lat: coords.lat, lng: coords.lng };
      setPickup(pickupCoords);
    }
    
    if (!destination.lat) {
      const coords = geocodeAddress(destination.address);
      destCoords = { ...destination, lat: coords.lat, lng: coords.lng };
      setDestination(destCoords);
    }

    setLoading(true);
    try {
      // Mock successful booking for demo
      const mockRideId = Math.floor(Math.random() * 10000);
      const routeData = calculateRouteInfo(pickupCoords, destCoords);
      
      setRideId(mockRideId);
      setEstimatedFare(routeData.fare);
      
      // Show success message
      alert(`Ride booked successfully! \nRide ID: ${mockRideId}\nFare: ₹${routeData.fare}\nVehicle: ${selectedCar || selectedVehicle}`);
      
    } catch (error) {
      console.error('Ride booking error:', error);
      alert('Failed to book ride: Please try again');
    }
    setLoading(false);
  };

  const handleLocationSelect = (lat, lng) => {
    if (!pickup.lat) {
      setPickup({ lat, lng, address: `Location ${lat.toFixed(4)}, ${lng.toFixed(4)}` });
    } else if (!destination.lat) {
      setDestination({ lat, lng, address: `Location ${lat.toFixed(4)}, ${lng.toFixed(4)}` });
    }
  };

  const handlePaymentSuccess = (paymentData) => {
    setShowPayment(false);
    alert(`Payment successful! Ride confirmed. Transaction ID: ${paymentData.transaction_id}`);
  };

  useEffect(() => {
    getCurrentLocation();
  }, []);

  if (showPayment) {
    return (
      <PaymentComponent 
        rideId={rideId}
        amount={estimatedFare}
        onPaymentSuccess={handlePaymentSuccess}
      />
    );
  }

  return (
    <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Book a Ride</h2>
      
      <VehicleSelector 
        onVehicleSelect={(vehicle) => {
          setSelectedVehicle(vehicle);
          setSelectedCar(null); // Reset car selection when vehicle type changes
        }}
        selectedVehicle={selectedVehicle}
        onCarSelect={setSelectedCar}
        selectedCar={selectedCar}
      />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
      
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Pickup Location</label>
        <input
          type="text"
          placeholder="Enter pickup address"
          className="w-full p-3 border rounded"
          value={pickup.address}
          onChange={(e) => setPickup({...pickup, address: e.target.value})}
        />
        <button
          onClick={getCurrentLocation}
          className="mt-2 text-blue-500 hover:underline text-sm"
        >
          Use Current Location
        </button>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Destination</label>
        <input
          type="text"
          placeholder="Enter destination address"
          className="w-full p-3 border rounded"
          value={destination.address}
          onChange={(e) => setDestination({...destination, address: e.target.value})}
        />
      </div>

      {routeInfo && (
        <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 className="font-semibold text-blue-800 mb-2">📍 Route Information</h4>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-600">Distance:</p>
              <p className="font-semibold text-blue-700">{routeInfo.distance} km</p>
            </div>
            <div>
              <p className="text-gray-600">Duration:</p>
              <p className="font-semibold text-blue-700">{routeInfo.timeText}</p>
            </div>
            <div>
              <p className="text-gray-600">Estimated Fare:</p>
              <p className="font-semibold text-green-600">₹{routeInfo.fare}</p>
            </div>
            <div>
              <p className="text-gray-600">Vehicle:</p>
              <p className="font-semibold text-purple-600">
                {selectedVehicle === 'mini' && '🚗'}
                {selectedVehicle === 'sedan' && '🚙'}
                {selectedVehicle === 'suv' && '🚐'}
                {selectedVehicle === 'luxury' && '🏎️'}
                {selectedVehicle === 'auto' && '🛺'}
                {selectedCar || selectedVehicle.charAt(0).toUpperCase() + selectedVehicle.slice(1)}
              </p>
            </div>
          </div>
        </div>
      )}

      <button
        onClick={handleBookRide}
        disabled={loading || !pickup.address || !destination.address}
        className="w-full bg-blue-500 text-white p-3 rounded hover:bg-blue-600 disabled:bg-gray-400"
      >
        {loading ? 'Booking...' : routeInfo ? `🚗 Book Ride - ₹${routeInfo.fare}` : '🚗 Book Ride'}
      </button>
      
          {rideId && (
            <div className="mt-4 p-3 bg-blue-100 rounded">
              <p className="text-blue-800">Ride ID: {rideId}</p>
              <p className="text-sm text-blue-600">Looking for nearby drivers...</p>
            </div>
          )}
        </div>
        
        <div>
          <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-lg font-medium">Map</h3>
              <button
                onClick={() => setShowMap(!showMap)}
                className="text-blue-500 hover:underline text-sm"
              >
                {showMap ? 'Hide Map' : 'Show Map'}
              </button>
            </div>
            {showMap && (
              <MapComponent 
                pickup={pickup}
                destination={destination}
                onLocationSelect={handleLocationSelect}
              />
            )}
          </div>
          
          <div className="mt-4">
            <h3 className="text-lg font-medium mb-2">Quick Actions</h3>
            <div className="space-y-2">
              <button
                onClick={() => setShowPayment(true)}
                className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600"
              >
                💳 Payment
              </button>
              <button
                onClick={() => {
                  if (pickup.address && destination.address) {
                    const pickupCoords = pickup.lat ? pickup : { ...pickup, ...geocodeAddress(pickup.address) };
                    const destCoords = destination.lat ? destination : { ...destination, ...geocodeAddress(destination.address) };
                    const routeData = calculateRouteInfo(pickupCoords, destCoords);
                    setRouteInfo(routeData);
                    setPickup(pickupCoords);
                    setDestination(destCoords);
                  }
                }}
                disabled={!pickup.address || !destination.address}
                className="w-full bg-orange-500 text-white p-2 rounded hover:bg-orange-600 disabled:bg-gray-400"
              >
                📊 Calculate Fare
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RideBooking;