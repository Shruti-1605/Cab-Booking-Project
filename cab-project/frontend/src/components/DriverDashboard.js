import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import MapComponent from './MapComponent';

const DriverDashboard = () => {
  const [isOnline, setIsOnline] = useState(false);
  const [rideRequests, setRideRequests] = useState([]);
  const [currentRide, setCurrentRide] = useState(null);
  const [driverLocation, setDriverLocation] = useState({ lat: 28.6139, lng: 77.2090, address: 'Current Location' });
  const [showMap, setShowMap] = useState(true);
  const { user } = useSelector(state => state.auth);

  const toggleOnlineStatus = () => {
    setIsOnline(!isOnline);
    if (!isOnline) {
      // Simulate getting ride requests when going online
      setTimeout(() => {
        setRideRequests([
          {
            id: 1,
            pickup: "Connaught Place",
            destination: "Airport",
            fare: 450,
            distance: "12 km"
          },
          {
            id: 2,
            pickup: "Railway Station",
            destination: "Mall",
            fare: 200,
            distance: "5 km"
          }
        ]);
      }, 2000);
    } else {
      setRideRequests([]);
    }
  };

  const acceptRide = (ride) => {
    setCurrentRide(ride);
    setRideRequests(rideRequests.filter(r => r.id !== ride.id));
  };

  const completeRide = () => {
    setCurrentRide(null);
    alert('Ride completed successfully!');
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Driver Dashboard</h2>
          <div className="flex items-center space-x-4">
            <span className={`px-3 py-1 rounded-full text-sm ${isOnline ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
              {isOnline ? 'Online' : 'Offline'}
            </span>
            <button
              onClick={toggleOnlineStatus}
              className={`px-4 py-2 rounded ${isOnline ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'} text-white`}
            >
              {isOnline ? 'Go Offline' : 'Go Online'}
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-3 gap-4 text-center">
          <div className="bg-blue-50 p-4 rounded">
            <h3 className="text-lg font-semibold text-blue-800">Today's Rides</h3>
            <p className="text-2xl font-bold text-blue-600">8</p>
          </div>
          <div className="bg-green-50 p-4 rounded">
            <h3 className="text-lg font-semibold text-green-800">Earnings</h3>
            <p className="text-2xl font-bold text-green-600">₹2,400</p>
          </div>
          <div className="bg-purple-50 p-4 rounded">
            <h3 className="text-lg font-semibold text-purple-800">Rating</h3>
            <p className="text-2xl font-bold text-purple-600">4.8 ⭐</p>
          </div>
        </div>
      </div>

      {currentRide && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6">
          <h3 className="text-xl font-bold text-yellow-800 mb-4">Current Ride</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p><strong>Pickup:</strong> {currentRide.pickup}</p>
              <p><strong>Destination:</strong> {currentRide.destination}</p>
            </div>
            <div>
              <p><strong>Fare:</strong> ₹{currentRide.fare}</p>
              <p><strong>Distance:</strong> {currentRide.distance}</p>
            </div>
          </div>
          <button
            onClick={completeRide}
            className="mt-4 bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600"
          >
            Complete Ride
          </button>
        </div>
      )}

      {isOnline && rideRequests.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold mb-4">Ride Requests</h3>
          <div className="space-y-4">
            {rideRequests.map(ride => (
              <div key={ride.id} className="border border-gray-200 rounded-lg p-4 flex justify-between items-center">
                <div>
                  <p><strong>From:</strong> {ride.pickup}</p>
                  <p><strong>To:</strong> {ride.destination}</p>
                  <p className="text-sm text-gray-600">{ride.distance} • ₹{ride.fare}</p>
                </div>
                <button
                  onClick={() => acceptRide(ride)}
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Accept
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {isOnline && rideRequests.length === 0 && !currentRide && (
        <div className="bg-white rounded-lg shadow-md p-6 text-center">
          <p className="text-gray-600">Waiting for ride requests...</p>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md p-6 mt-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">Driver Map</h3>
          <button
            onClick={() => setShowMap(!showMap)}
            className="text-blue-500 hover:underline"
          >
            {showMap ? 'Hide Map' : 'Show Map'}
          </button>
        </div>
        
        {showMap && (
          <div>
            <MapComponent 
              pickup={driverLocation}
              destination={currentRide ? { lat: currentRide.pickup_lat || 28.6200, lng: currentRide.pickup_lng || 77.2100, address: currentRide.pickup } : { lat: null, lng: null, address: '' }}
              onLocationSelect={(lat, lng) => {
                setDriverLocation({ lat, lng, address: `Driver Location ${lat.toFixed(4)}, ${lng.toFixed(4)}` });
              }}
            />
            <div className="mt-4 grid grid-cols-2 gap-4">
              <button
                onClick={() => {
                  if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition((position) => {
                      setDriverLocation({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                        address: 'Current GPS Location'
                      });
                    });
                  }
                }}
                className="bg-green-500 text-white p-2 rounded hover:bg-green-600"
              >
                📍 Update GPS Location
              </button>
              <button
                onClick={() => {
                  setDriverLocation({ lat: 28.6139, lng: 77.2090, address: 'Delhi Center' });
                }}
                className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
              >
                🏙️ Go to Delhi Center
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DriverDashboard;