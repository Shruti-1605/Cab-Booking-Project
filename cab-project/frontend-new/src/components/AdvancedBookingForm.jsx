import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useMutation, useQuery } from '@tanstack/react-query';
import { setPickup, setDestination, setBookingStatus } from '../store/bookingSlice';
import { bookingAPI } from '../services/api';
import LocationPicker from './LocationPicker';
import MapComponent from './MapComponent';

const AdvancedBookingForm = () => {
  const dispatch = useDispatch();
  const { pickup, destination, selectedCab } = useSelector((state) => state.booking);
  
  const [promoCode, setPromoCode] = useState('');
  const [promoApplied, setPromoApplied] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState('wallet');
  const [fareEstimate, setFareEstimate] = useState(null);

  // Fare estimation query
  const { data: fareData, refetch: getFareEstimate } = useQuery({
    queryKey: ['fareEstimate', pickup, destination],
    queryFn: () => bookingAPI.getFareEstimate(pickup, destination),
    enabled: false
  });

  // Promo validation mutation
  const promoMutation = useMutation({
    mutationFn: (code) => bookingAPI.validatePromo(code),
    onSuccess: (data) => {
      setPromoApplied(data);
      alert(`Promo applied! ${data.discount}% off`);
    },
    onError: () => {
      alert('Invalid promo code');
      setPromoApplied(null);
    }
  });

  // Booking mutation
  const bookMutation = useMutation({
    mutationFn: bookingAPI.bookCab,
    onSuccess: (data) => {
      dispatch(setBookingStatus('success'));
      alert(`Booking confirmed! OTP: ${data.otp}`);
    },
    onError: (error) => {
      alert('Booking failed: ' + error.message);
    }
  });

  const handleFareEstimate = async () => {
    if (pickup && destination) {
      const result = await getFareEstimate();
      setFareEstimate(result.data);
    }
  };

  const handlePromoApply = () => {
    if (promoCode.trim()) {
      promoMutation.mutate({ code: promoCode, discount_percent: 0 });
    }
  };

  const handleBooking = () => {
    if (selectedCab && pickup && destination) {
      const bookingData = {
        user_name: 'Current User',
        cab_id: selectedCab.id,
        pickup,
        destination,
        promo_code: promoApplied?.code,
        payment_method: paymentMethod
      };
      bookMutation.mutate(bookingData);
    }
  };

  const calculateFinalFare = () => {
    if (!fareEstimate) return 0;
    let fare = fareEstimate.final_fare;
    if (promoApplied) {
      if (promoApplied.type === 'percentage') {
        fare = fare * (1 - promoApplied.discount / 100);
      } else {
        fare = fare - promoApplied.discount;
      }
    }
    return Math.max(fare, 0);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
      <h2 className="text-2xl font-bold mb-4">Book Your Cab</h2>
      
      {/* Location Inputs */}
      <div className="space-y-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            📍 Pickup Location
          </label>
          <LocationPicker
            placeholder="Enter pickup location"
            value={pickup}
            onLocationSelect={(location) => dispatch(setPickup(location.address))}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🎯 Destination
          </label>
          <LocationPicker
            placeholder="Enter destination"
            value={destination}
            onLocationSelect={(location) => dispatch(setDestination(location.address))}
          />
        </div>
      </div>

      {/* Map Preview */}
      {pickup && destination && (
        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🗺️ Route Preview
          </label>
          <MapComponent
            pickup={{ lat: 28.6139, lng: 77.2090 }}
            dropoff={{ lat: 28.5355, lng: 77.3910 }}
            showRoute={true}
            height="250px"
          />
        </div>
      )}

      {/* Fare Estimate Button */}
      <button
        onClick={handleFareEstimate}
        disabled={!pickup || !destination}
        className="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-300"
      >
        Get Fare Estimate
      </button>

      {/* Fare Breakdown */}
      {fareEstimate && (
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="font-semibold mb-2">Fare Breakdown</h3>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span>Distance:</span>
              <span>{fareEstimate.distance_km} km</span>
            </div>
            <div className="flex justify-between">
              <span>Time:</span>
              <span>{fareEstimate.estimated_time}</span>
            </div>
            <div className="flex justify-between">
              <span>Base Fare:</span>
              <span>₹{fareEstimate.base_fare}</span>
            </div>
            {fareEstimate.surge_multiplier > 1 && (
              <div className="flex justify-between text-orange-600">
                <span>Surge ({fareEstimate.surge_multiplier}x):</span>
                <span>₹{fareEstimate.breakdown.surge}</span>
              </div>
            )}
            <hr className="my-2" />
            <div className="flex justify-between font-semibold">
              <span>Total:</span>
              <span>₹{calculateFinalFare()}</span>
            </div>
          </div>
        </div>
      )}

      {/* Promo Code */}
      <div className="space-y-2">
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="🎫 Enter promo code"
            value={promoCode}
            onChange={(e) => setPromoCode(e.target.value.toUpperCase())}
            className="flex-1 p-2 border rounded-lg"
          />
          <button
            onClick={handlePromoApply}
            disabled={!promoCode.trim() || promoMutation.isPending}
            className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 disabled:bg-gray-300"
          >
            Apply
          </button>
        </div>
        
        {promoApplied && (
          <div className="bg-green-100 p-2 rounded text-green-800 text-sm">
            ✅ Promo "{promoApplied.code}" applied! {promoApplied.discount}% discount
          </div>
        )}
        
        <div className="text-xs text-gray-500">
          Try: FIRST50, SAVE20, NEWUSER
        </div>
      </div>

      {/* Payment Method */}
      <div className="space-y-2">
        <label className="block text-sm font-medium">Payment Method</label>
        <div className="flex gap-4">
          <label className="flex items-center">
            <input
              type="radio"
              value="wallet"
              checked={paymentMethod === 'wallet'}
              onChange={(e) => setPaymentMethod(e.target.value)}
              className="mr-2"
            />
            💳 Wallet
          </label>
          <label className="flex items-center">
            <input
              type="radio"
              value="card"
              checked={paymentMethod === 'card'}
              onChange={(e) => setPaymentMethod(e.target.value)}
              className="mr-2"
            />
            💰 Card
          </label>
          <label className="flex items-center">
            <input
              type="radio"
              value="cash"
              checked={paymentMethod === 'cash'}
              onChange={(e) => setPaymentMethod(e.target.value)}
              className="mr-2"
            />
            💵 Cash
          </label>
        </div>
      </div>

      {/* Selected Cab Info */}
      {selectedCab && (
        <div className="bg-green-50 p-3 rounded-lg border border-green-200">
          <div className="flex justify-between items-center">
            <div>
              <p className="font-semibold">{selectedCab.driver_name}</p>
              <p className="text-sm text-gray-600">{selectedCab.car_model}</p>
              <p className="text-sm">⭐ {selectedCab.rating} • {selectedCab.trips} trips</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">ETA: {selectedCab.eta}</p>
              <p className="text-sm text-gray-600">{selectedCab.distance} away</p>
            </div>
          </div>
        </div>
      )}

      {/* Book Button */}
      <button 
        onClick={handleBooking}
        disabled={!selectedCab || !pickup || !destination || bookMutation.isPending}
        className={`w-full p-3 rounded-lg font-semibold ${
          !selectedCab || !pickup || !destination 
            ? 'bg-gray-400 cursor-not-allowed' 
            : 'bg-blue-600 hover:bg-blue-700 cursor-pointer'
        } text-white`}
      >
        {bookMutation.isPending ? 'Booking...' : 
         (!selectedCab ? 'Select a Cab First' : 
          (!pickup || !destination ? 'Enter Pickup & Destination' : 
           `Book Cab - ₹${calculateFinalFare()}`
          )
         )}
      </button>

      {/* Booking Status */}
      {bookMutation.isError && (
        <div className="text-red-600 text-sm mt-2 p-2 bg-red-50 rounded">
          ❌ {bookMutation.error?.message}
        </div>
      )}
    </div>
  );
};

export default AdvancedBookingForm;