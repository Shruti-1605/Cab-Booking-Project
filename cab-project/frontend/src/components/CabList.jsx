import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useDispatch } from 'react-redux';
import { bookingAPI } from '../services/api';
import { setSelectedCab } from '../store/bookingSlice';

const CabList = () => {
  const dispatch = useDispatch();
  
  const { data: cabs, isLoading } = useQuery({
    queryKey: ['cabs'],
    queryFn: bookingAPI.getCabs,
  });

  if (isLoading) return <div className="text-center">Loading cabs...</div>;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-bold mb-4">Available Cabs</h3>
      <div className="space-y-3">
        {cabs?.data?.map((cab) => (
          <div key={cab.id} className="border p-4 rounded-lg flex justify-between items-center">
            <div>
              <h4 className="font-semibold">{cab.driver_name}</h4>
              <p className="text-gray-600">{cab.car_model}</p>
            </div>
            <button
              onClick={() => dispatch(setSelectedCab(cab))}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              Select
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CabList;