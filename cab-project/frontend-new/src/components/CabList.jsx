import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useDispatch } from 'react-redux';
import { bookingAPI } from '../services/api';
import { setSelectedCab } from '../store/bookingSlice';

const CabList = () => {
  const dispatch = useDispatch();
  
  const { data: cabs, isLoading, error } = useQuery({
    queryKey: ['cabs'],
    queryFn: bookingAPI.getCabs,
  });

  console.log('CabList - Loading:', isLoading);
  console.log('CabList - Error:', error);
  console.log('CabList - Data:', cabs);

  if (isLoading) return <div className="text-center p-4 bg-yellow-100">Loading cabs...</div>;
  if (error) return <div className="text-center p-4 bg-red-100 text-red-700">Error: {error.message}</div>;
  
  const cabsArray = cabs?.data || cabs || [];
  console.log('CabList - Final array:', cabsArray);

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-bold mb-4">Available Cabs</h3>
      <div className="space-y-3">
        {cabsArray.length === 0 ? (
          <div className="text-center p-4 bg-gray-100">No cabs available</div>
        ) : (
          cabsArray.map((cab) => (
            <div key={cab.id} className="border p-4 rounded-lg flex justify-between items-center">
              <div>
                <h4 className="font-semibold">{cab.driver_name}</h4>
                <p className="text-gray-600">{cab.car_model}</p>
                <p className="text-sm text-green-600">₹{cab.price}/km</p>
              </div>
              <button
                onClick={() => {
                  console.log('Selecting cab:', cab);
                  dispatch(setSelectedCab(cab));
                }}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                Select
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default CabList;