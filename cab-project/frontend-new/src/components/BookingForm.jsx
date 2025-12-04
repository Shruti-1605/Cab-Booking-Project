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
    onSuccess: (data) => {
      console.log('Booking success:', data);
      dispatch(setBookingStatus('success'));
      alert('Cab booked successfully!');
    },
    onError: (error) => {
      console.error('Booking error:', error);
      alert('Booking failed: ' + error.message);
    },
  });

  const handleBooking = () => {
    console.log('Booking attempt:', { selectedCab, pickup, destination });
    
    if (selectedCab && pickup && destination) {
      const bookingData = {
        user_name: 'Current User',
        cab_id: selectedCab.id,
        pickup,
        destination,
      };
      console.log('Sending booking data:', bookingData);
      bookMutation.mutate(bookingData);
    } else {
      alert('Please fill all fields and select a cab');
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
          disabled={!selectedCab || !pickup || !destination || bookMutation.isPending}
          className={`w-full p-3 rounded-lg ${
            !selectedCab || !pickup || !destination 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700 cursor-pointer'
          } text-white`}
        >
          {bookMutation.isPending ? 'Booking...' : 
           (!selectedCab ? 'Select a Cab First' : 
            (!pickup || !destination ? 'Fill Pickup & Destination' : 'Book Cab'))}
        </button>
        {bookMutation.isError && (
          <div className="text-red-600 text-sm mt-2">
            Error: {bookMutation.error?.message}
          </div>
        )}
      </div>
    </div>
  );
};

export default BookingForm;