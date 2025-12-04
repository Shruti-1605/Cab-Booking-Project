import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminDashboard = () => {
  const [stats, setStats] = useState({});
  const [users, setUsers] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [rides, setRides] = useState([]);
  const [payments, setPayments] = useState([]);
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, usersRes, driversRes, ridesRes, paymentsRes] = await Promise.all([
        axios.get('http://localhost:8000/admin/stats'),
        axios.get('http://localhost:8000/admin/users'),
        axios.get('http://localhost:8000/admin/drivers'),
        axios.get('http://localhost:8000/admin/rides'),
        axios.get('http://localhost:8000/admin/payments')
      ]);

      setStats(statsRes.data);
      setUsers(usersRes.data);
      setDrivers(driversRes.data);
      setRides(ridesRes.data);
      setPayments(paymentsRes.data);
    } catch (error) {
      console.error('Error fetching admin data:', error);
    }
  };

  const renderDashboard = () => (
    <div>
      <h2 className="text-2xl font-bold mb-6">📊 Admin Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
          <h3 className="text-lg font-semibold text-blue-800">Total Users</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.total_users}</p>
        </div>
        <div className="bg-green-50 p-6 rounded-lg border border-green-200">
          <h3 className="text-lg font-semibold text-green-800">Total Drivers</h3>
          <p className="text-3xl font-bold text-green-600">{stats.total_drivers}</p>
        </div>
        <div className="bg-purple-50 p-6 rounded-lg border border-purple-200">
          <h3 className="text-lg font-semibold text-purple-800">Total Rides</h3>
          <p className="text-3xl font-bold text-purple-600">{stats.total_rides}</p>
        </div>
        <div className="bg-yellow-50 p-6 rounded-lg border border-yellow-200">
          <h3 className="text-lg font-semibold text-yellow-800">Total Revenue</h3>
          <p className="text-3xl font-bold text-yellow-600">₹{stats.total_revenue}</p>
        </div>
      </div>
    </div>
  );

  const renderUsers = () => (
    <div>
      <h2 className="text-2xl font-bold mb-6">👥 Users Management</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phone</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rides</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {users.map(user => (
              <tr key={user.id}>
                <td className="px-6 py-4 whitespace-nowrap">{user.name}</td>
                <td className="px-6 py-4 whitespace-nowrap">{user.email}</td>
                <td className="px-6 py-4 whitespace-nowrap">{user.phone}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs rounded-full ${user.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {user.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">{user.rides}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderDrivers = () => (
    <div>
      <h2 className="text-2xl font-bold mb-6">🚗 Drivers Management</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phone</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vehicle</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">License</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rating</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {drivers.map(driver => (
              <tr key={driver.id}>
                <td className="px-6 py-4 whitespace-nowrap">{driver.name}</td>
                <td className="px-6 py-4 whitespace-nowrap">{driver.phone}</td>
                <td className="px-6 py-4 whitespace-nowrap">{driver.vehicle}</td>
                <td className="px-6 py-4 whitespace-nowrap">{driver.license}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs rounded-full ${driver.status === 'Verified' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {driver.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">⭐ {driver.rating}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderRides = () => (
    <div>
      <h2 className="text-2xl font-bold mb-6">🚕 Rides Management</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Driver</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Route</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fare</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {rides.map(ride => (
              <tr key={ride.id}>
                <td className="px-6 py-4 whitespace-nowrap">{ride.user}</td>
                <td className="px-6 py-4 whitespace-nowrap">{ride.driver}</td>
                <td className="px-6 py-4 whitespace-nowrap">{ride.pickup} → {ride.destination}</td>
                <td className="px-6 py-4 whitespace-nowrap">₹{ride.fare}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs rounded-full ${ride.status === 'Completed' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>
                    {ride.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">{ride.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderPayments = () => (
    <div>
      <h2 className="text-2xl font-bold mb-6">💳 Payments Management</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ride ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Method</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {payments.map(payment => (
              <tr key={payment.id}>
                <td className="px-6 py-4 whitespace-nowrap">#{payment.ride_id}</td>
                <td className="px-6 py-4 whitespace-nowrap">{payment.user}</td>
                <td className="px-6 py-4 whitespace-nowrap">₹{payment.amount}</td>
                <td className="px-6 py-4 whitespace-nowrap">{payment.method}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs rounded-full ${payment.status === 'Success' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {payment.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">{payment.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex space-x-8">
            {[
              { id: 'dashboard', label: '📊 Dashboard' },
              { id: 'users', label: '👥 Users' },
              { id: 'drivers', label: '🚗 Drivers' },
              { id: 'rides', label: '🚕 Rides' },
              { id: 'payments', label: '💳 Payments' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto py-6 px-4">
        {activeTab === 'dashboard' && renderDashboard()}
        {activeTab === 'users' && renderUsers()}
        {activeTab === 'drivers' && renderDrivers()}
        {activeTab === 'rides' && renderRides()}
        {activeTab === 'payments' && renderPayments()}
      </div>
    </div>
  );
};

export default AdminDashboard;