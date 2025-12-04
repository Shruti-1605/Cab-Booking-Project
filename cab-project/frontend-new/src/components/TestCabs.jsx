import React, { useState, useEffect } from 'react';

const TestCabs = () => {
  const [cabs, setCabs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/cabs')
      .then(response => response.json())
      .then(data => {
        console.log('Direct fetch result:', data);
        setCabs(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Fetch error:', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-bold mb-4">Test Cabs (Direct Fetch)</h3>
      {cabs.map(cab => (
        <div key={cab.id} className="border p-2 mb-2">
          <p>{cab.driver_name} - {cab.car_model}</p>
          <button className="bg-blue-500 text-white px-2 py-1 rounded">
            Select {cab.driver_name}
          </button>
        </div>
      ))}
    </div>
  );
};

export default TestCabs;