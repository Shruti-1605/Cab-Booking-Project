import React, { useState, useEffect } from 'react';
import api from '../services/api';

const VehicleSelector = ({ onVehicleSelect, selectedVehicle, onCarSelect, selectedCar }) => {
  const [vehicleTypes, setVehicleTypes] = useState({});
  const [loading, setLoading] = useState(true);
  const [expandedVehicle, setExpandedVehicle] = useState(null);

  useEffect(() => {
    fetchVehicleTypes();
  }, []);

  const fetchVehicleTypes = async () => {
    try {
      const response = await api.get('/api/vehicle-types');
      setVehicleTypes(response.data);
    } catch (error) {
      console.error('Failed to fetch vehicle types:', error);
      // Fallback data with multiple cars
      setVehicleTypes({
        mini: { 
          name: "Mini", base_fare: 40, per_km: 8, 
          examples: ["Maruti Alto 800", "Maruti Alto K10", "Hyundai Eon", "Tata Nano", "Maruti WagonR", "Hyundai Santro", "Tata Tiago", "Maruti Celerio"] 
        },
        sedan: { 
          name: "Sedan", base_fare: 60, per_km: 12, 
          examples: ["Honda City", "Maruti Dzire", "Hyundai Verna", "Toyota Yaris", "Volkswagen Vento", "Skoda Rapid", "Honda Amaze", "Tata Tigor"] 
        },
        suv: { 
          name: "SUV", base_fare: 80, per_km: 15, 
          examples: ["Toyota Innova Crysta", "Mahindra Scorpio", "Tata Safari", "Ford Endeavour", "Toyota Fortuner", "Mahindra XUV500", "Tata Hexa", "Kia Seltos"] 
        },
        luxury: { 
          name: "Luxury", base_fare: 150, per_km: 25, 
          examples: ["BMW 3 Series", "Audi A4", "Mercedes C-Class", "Jaguar XE", "BMW 5 Series", "Audi A6", "Mercedes E-Class", "Volvo S60"] 
        },
        auto: {
          name: "Auto Rickshaw", base_fare: 25, per_km: 6,
          examples: ["Bajaj RE Auto", "TVS King", "Mahindra Alfa", "Piaggio Ape", "Bajaj Maxima", "Force Trax"]
        }
      });
    }
    setLoading(false);
  };

  if (loading) {
    return <div className="text-center">Loading vehicle types...</div>;
  }

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold mb-3">Select Vehicle Type</h3>
      <div className="grid grid-cols-2 gap-3">
        {Object.entries(vehicleTypes).map(([key, vehicle]) => (
          <div key={key}>
            <div
              onClick={() => onVehicleSelect(key)}
              className={`p-4 border rounded-lg cursor-pointer transition-all ${
                selectedVehicle === key
                  ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                  : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">{vehicle.name}</h4>
                  <p className="text-sm text-gray-600">
                    ₹{vehicle.base_fare} base + ₹{vehicle.per_km}/km
                  </p>
                  <p className="text-xs text-gray-500">
                    {vehicle.examples?.length || 0} cars available
                  </p>
                </div>
                <div className="text-2xl">
                  {key === 'mini' && '🚗'}
                  {key === 'sedan' && '🚙'}
                  {key === 'suv' && '🚐'}
                  {key === 'luxury' && '🏎️'}
                  {key === 'auto' && '🛺'}
                </div>
              </div>
              
              {selectedVehicle === key && (
                <div className="mt-3 pt-3 border-t border-blue-200">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setExpandedVehicle(expandedVehicle === key ? null : key);
                    }}
                    className="w-full text-sm text-blue-600 hover:text-blue-800 bg-blue-100 hover:bg-blue-200 py-2 px-3 rounded transition-colors"
                  >
                    {expandedVehicle === key ? '▲ Hide Available Cars' : '▼ Show Available Cars'}
                  </button>
                </div>
              )}
            </div>
            
            {selectedVehicle === key && expandedVehicle === key && (
              <div className="mt-2 p-3 bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg">
                <h5 className="font-medium text-sm mb-3 text-blue-800">
                  🚗 Available {vehicle.name} Cars ({vehicle.examples?.length})
                </h5>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  {vehicle.examples?.map((car, index) => (
                    <div 
                      key={index} 
                      onClick={() => onCarSelect && onCarSelect(car)}
                      className={`p-2 rounded-md border text-center cursor-pointer transition-colors shadow-sm ${
                        selectedCar === car 
                          ? 'bg-green-100 border-green-400 text-green-800' 
                          : 'bg-white border-gray-200 hover:bg-blue-50'
                      }`}
                    >
                      • {car}
                    </div>
                  ))}
                </div>
                {selectedCar && selectedVehicle === key && (
                  <div className="mt-3 p-2 bg-green-50 border border-green-200 rounded text-center">
                    <p className="text-sm font-medium text-green-800">
                      ✓ Selected: {selectedCar}
                    </p>
                  </div>
                )}
                <p className="text-xs text-gray-600 mt-2 text-center">
                  💰 Base Fare: ₹{vehicle.base_fare} | Per KM: ₹{vehicle.per_km}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default VehicleSelector;