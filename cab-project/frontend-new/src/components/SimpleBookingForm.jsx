import React, { useState } from 'react';

const SimpleBookingForm = () => {
  const [pickup, setPickup] = useState('');
  const [dropoff, setDropoff] = useState('');
  const [fareData, setFareData] = useState(null);
  const [selectedCab, setSelectedCab] = useState(null);
  const [loading, setLoading] = useState(false);

  const cabs = [
    { id: 1, driver_name: "John Doe", car_model: "Mini Cooper", price: 10, rating: 4.8, trips: 1250, eta: "3 mins", distance: "0.5 km" },
    { id: 2, driver_name: "Jane Smith", car_model: "Honda Civic", price: 15, rating: 4.9, trips: 890, eta: "5 mins", distance: "1.2 km" },
    { id: 3, driver_name: "Mike Johnson", car_model: "Toyota SUV", price: 20, rating: 4.7, trips: 2100, eta: "7 mins", distance: "2.1 km" }
  ];

  const handleFareEstimate = async () => {
    if (!pickup || !dropoff) {
      alert('Please enter both pickup and drop locations');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/fare/estimate?pickup=${encodeURIComponent(pickup)}&destination=${encodeURIComponent(dropoff)}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Fare data:', data);
      setFareData(data);
      alert(`✅ Fare Estimate:\nDistance: ${data.distance_km} km\nTime: ${data.estimated_time}\nFare: ₹${data.final_fare}`);
    } catch (error) {
      console.error('Fare Error:', error);
      alert(`❌ Error: ${error.message}\n\nMake sure backend is running on http://localhost:8000`);
    }
    setLoading(false);
  };

  const handleBooking = async () => {
    if (!selectedCab || !pickup || !dropoff) {
      alert('Please select a cab and enter locations');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_name: 'Test User',
          cab_id: selectedCab.id,
          pickup,
          destination: dropoff
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      alert(`✅ Booking successful!\nOTP: ${data.otp}\nFare: ₹${data.fare}`);
    } catch (error) {
      console.error('Booking Error:', error);
      alert(`❌ Booking failed: ${error.message}`);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-2xl mx-auto bg-white p-8 rounded-2xl shadow-xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">🚗 QuickCab</h1>
          <p className="text-gray-600">Book your ride in seconds</p>
        </div>
      
        {/* Location Inputs */}
        <div className="space-y-4 mb-6">
          <div className="relative">
            <input
              type="text"
              placeholder="📍 Pickup Location"
              value={pickup}
              onChange={(e) => setPickup(e.target.value)}
              className="w-full p-4 pl-12 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            />
            <div className="absolute left-4 top-4 text-green-500 text-xl">📍</div>
          </div>
          <div className="relative">
            <input
              type="text"
              placeholder="🎯 Drop Location"
              value={dropoff}
              onChange={(e) => setDropoff(e.target.value)}
              className="w-full p-4 pl-12 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            />
            <div className="absolute left-4 top-4 text-red-500 text-xl">🎯</div>
          </div>
        </div>

        {/* Fare Estimate Button */}
        <button
          onClick={handleFareEstimate}
          disabled={loading || !pickup || !dropoff}
          className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-xl mb-6 hover:from-blue-600 hover:to-blue-700 disabled:from-gray-300 disabled:to-gray-400 transition-all duration-200 font-semibold shadow-lg"
        >
          {loading ? '🔄 Calculating...' : '💰 Get Fare Estimate'}
        </button>

        {/* Fare Display */}
        {fareData && (
          <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-xl mb-6 border border-green-200">
            <h3 className="font-bold text-lg mb-4 text-gray-800">💰 Fare Estimate</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="bg-white p-3 rounded-lg text-center">
                <div className="text-2xl mb-1">📏</div>
                <div className="font-semibold text-gray-800">{fareData.distance_km} km</div>
                <div className="text-gray-600">Distance</div>
              </div>
              <div className="bg-white p-3 rounded-lg text-center">
                <div className="text-2xl mb-1">⏱️</div>
                <div className="font-semibold text-gray-800">{fareData.estimated_time}</div>
                <div className="text-gray-600">Duration</div>
              </div>
            </div>
            <div className="mt-4 bg-white p-4 rounded-lg text-center">
              <div className="text-3xl mb-2">💸</div>
              <div className="text-2xl font-bold text-green-600">₹{fareData.final_fare}</div>
              <div className="text-gray-600">Total Fare</div>
            </div>
          </div>
        )}

        {/* Available Cabs */}
        <div className="mb-6">
          <h3 className="font-bold text-lg mb-4 text-gray-800">🚕 Available Cabs</h3>
          <div className="space-y-3">
            {cabs.map((cab) => (
              <div
                key={cab.id}
                onClick={() => setSelectedCab(cab)}
                className={`p-4 border-2 rounded-xl cursor-pointer transition-all duration-200 hover:shadow-lg ${
                  selectedCab?.id === cab.id 
                    ? 'border-blue-500 bg-blue-50 shadow-md transform scale-[1.02]' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex justify-between items-center">
                  <div className="flex items-center space-x-3">
                    <div className="text-3xl">
                      {cab.car_model.includes('Mini') ? '🚗' : 
                       cab.car_model.includes('SUV') ? '🚙' : '🚘'}
                    </div>
                    <div>
                      <p className="font-semibold text-gray-800">{cab.driver_name}</p>
                      <p className="text-sm text-gray-600">{cab.car_model}</p>
                      <div className="flex items-center space-x-2 text-sm">
                        <span className="text-yellow-500">⭐ {cab.rating}</span>
                        <span className="text-gray-500">•</span>
                        <span className="text-gray-600">{cab.trips} trips</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-lg text-green-600">₹{cab.price}/km</p>
                    <p className="text-sm text-blue-600 font-medium">{cab.eta}</p>
                    <p className="text-xs text-gray-500">{cab.distance} away</p>
                  </div>
                </div>
                {selectedCab?.id === cab.id && (
                  <div className="mt-3 pt-3 border-t border-blue-200">
                    <div className="text-sm text-blue-700 font-medium">✅ Selected</div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Book Button */}
        <button
          onClick={handleBooking}
          disabled={loading || !selectedCab || !pickup || !dropoff}
          className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white p-4 rounded-xl hover:from-green-600 hover:to-green-700 disabled:from-gray-300 disabled:to-gray-400 transition-all duration-200 font-bold text-lg shadow-lg"
        >
          {loading ? '🔄 Booking...' : '🚀 Book Cab Now'}
        </button>
      </div>
    </div>
  );
};

export default SimpleBookingForm;