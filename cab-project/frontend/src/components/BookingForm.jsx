import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useMutation } from '@tanstack/react-query';
import { setPickup, setDestination, setBookingStatus } from '../store/bookingSlice';
import { bookingAPI } from '../services/api';

const BookingForm = () => {
  const dispatch = useDispatch();
  const { pickup, destination, selectedCab } = useSelector((state) => state.booking);

  const bookMutation = useMutation({
    mutationFn: bookingAPI.bookCab,
    onSuccess: () => {
      dispatch(setBookingStatus('success'));
      alert('Cab booked successfully!');
    },
  });

  const handleBooking = () => {
    if (selectedCab && pickup && destination) {
      bookMutation.mutate({
        user_name: 'Current User',
        cab_id: selectedCab.id,
        pickup,
        destination,
      });
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Book Your Cab</h2>
      <div className="space-y-4">
        <input
          type="text"
          placeholder="Pickup Location"
          value={pickup}
          onChange={(e) => dispatch(setPickup(e.target.value))}
          className="w-full p-3 border rounded-lg"
        />
        <input
          type="text"
          placeholder="Destination"
          value={destination}
          onChange={(e) => dispatch(setDestination(e.target.value))}
          className="w-full p-3 border rounded-lg"
        />
        {selectedCab && (
          <div className="p-3 bg-green-100 rounded-lg">
            <p>Selected: {selectedCab.driver_name} - {selectedCab.car_model}</p>
          </div>
        )}
        <button 
          onClick={handleBooking}
          disabled={!selectedCab || !pickup || !destination}
          className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
        >
          {selectedCab ? 'Book Cab' : 'Select a Cab First'}
        </button>
      </div>
    </div>
  );
};

export default BookingForm;