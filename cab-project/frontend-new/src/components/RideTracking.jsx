import React, { useState, useEffect } from 'react';
import { MapPin, Clock, Phone, MessageCircle } from 'lucide-react';
import MapComponent from './MapComponent';

const RideTracking = ({ rideId, onClose }) => {
  const [rideData, setRideData] = useState(null);
  const [driverLocation, setDriverLocation] = useState(null);

  useEffect(() => {
    // Fetch initial ride data
    fetchRideData();
    
    // Set up real-time tracking
    const interval = setInterval(() => {
      updateDriverLocation();
    }, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, [rideId]);

  const fetchRideData = async () => {
    try {
      const response = await fetch(`http://localhost:8000/ride/track/${rideId}`);
      const data = await response.json();
      setRideData(data);
      setDriverLocation(data.driver_location);
    } catch (error) {
      console.error('Error fetching ride data:', error);
    }
  };

  const updateDriverLocation = async () => {
    try {
      const response = await fetch(`http://localhost:8000/driver/location/${rideId}`);
      const data = await response.json();
      setDriverLocation(data.location);
    } catch (error) {
      console.error('Error updating driver location:', error);
    }
  };

  if (!rideData) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-semibold">Track Your Ride</h2>
          <button 
            onClick={onClose}
            className="text-white hover:text-gray-200"
          >
            ✕
          </button>
        </div>
        <p className="text-blue-100 text-sm">Ride ID: {rideId}</p>
      </div>

      {/* Map */}
      <div className="h-64">
        <MapComponent
          pickup={rideData.pickup_location}
          dropoff={rideData.destination}
          driverLocation={driverLocation}
          showRoute={true}
          height="100%"
        />
      </div>

      {/* Ride Status */}
      <div className="p-4 border-b">
        <div className="flex items-center gap-3 mb-3">
          <div className={`w-3 h-3 rounded-full ${
            rideData.status === 'in_progress' ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'
          }`}></div>
          <span className="font-medium capitalize">
            {rideData.status.replace('_', ' ')}
          </span>
        </div>
        
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-gray-500" />
            <span>ETA: {rideData.estimated_arrival}</span>
          </div>
          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4 text-gray-500" />
            <span>{rideData.distance_remaining} remaining</span>
          </div>
        </div>
      </div>

      {/* Driver Info */}
      <div className="p-4 border-b">
        <h3 className="font-medium mb-3">Driver Details</h3>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
              👤
            </div>
            <div>
              <p className="font-medium">John Doe</p>
              <p className="text-sm text-gray-600">Honda Civic • ⭐ 4.8</p>
              <p className="text-sm text-gray-600">KA 01 AB 1234</p>
            </div>
          </div>
          
          <div className="flex gap-2">
            <button className="p-2 bg-green-100 text-green-600 rounded-full hover:bg-green-200">
              <Phone className="w-4 h-4" />
            </button>
            <button className="p-2 bg-blue-100 text-blue-600 rounded-full hover:bg-blue-200">
              <MessageCircle className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Trip Progress */}
      <div className="p-4">
        <h3 className="font-medium mb-3">Trip Progress</h3>
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm font-medium">Pickup Location</p>
              <p className="text-xs text-gray-600">Completed</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
            <div className="flex-1">
              <p className="text-sm font-medium">En Route</p>
              <p className="text-xs text-gray-600">Current status</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-gray-300 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm font-medium">Drop Location</p>
              <p className="text-xs text-gray-600">Pending</p>
            </div>
          </div>
        </div>
      </div>

      {/* Emergency Button */}
      <div className="p-4 bg-gray-50">
        <button className="w-full bg-red-600 text-white py-2 rounded-lg font-medium hover:bg-red-700">
          🚨 Emergency Help
        </button>
      </div>
    </div>
  );
};

export default RideTracking;