import React, { useState } from 'react';
import { Provider, useSelector, useDispatch } from 'react-redux';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { store } from './store/store';
import Login from './components/Login';
import Register from './components/Register';
import RideBooking from './components/RideBooking';
import DriverDashboard from './components/DriverDashboard';
import AdminDashboard from './components/AdminDashboard';
import { logout } from './store/authSlice';

const queryClient = new QueryClient();

function AppContent() {
  const [showLogin, setShowLogin] = useState(true);
  const { isAuthenticated, user } = useSelector(state => state.auth);
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(logout());
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        {showLogin ? (
          <Login onToggle={() => setShowLogin(false)} />
        ) : (
          <Register onToggle={() => setShowLogin(true)} />
        )}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-md p-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">CabBooking</h1>
          <div className="flex items-center space-x-4">
            <span>Welcome, {user?.name}</span>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="container mx-auto py-8">
        {/* Debug info */}
        <div className="mb-4 p-2 bg-yellow-100 rounded text-sm">
          <strong>Debug:</strong> User Role = {user?.role || 'undefined'} | Name = {user?.name || 'undefined'}
        </div>
        
        {user?.role === 'rider' ? (
          <div>
            <h2 className="text-xl font-bold mb-4 text-green-600">🚗 RIDER DASHBOARD</h2>
            <RideBooking />
          </div>
        ) : user?.role === 'driver' ? (
          <div>
            <h2 className="text-xl font-bold mb-4 text-blue-600">🚕 DRIVER DASHBOARD</h2>
            <DriverDashboard />
          </div>
        ) : user?.role === 'admin' ? (
          <AdminDashboard />
        ) : (
          <div className="text-center">
            <h2 className="text-xl font-bold mb-4 text-red-600">❌ UNKNOWN ROLE</h2>
            <p>Role: {user?.role}</p>
            <p>Please logout and register again with proper role selection.</p>
          </div>
        )}
      </div>
    </div>
  );
}

function App() {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <AppContent />
      </QueryClientProvider>
    </Provider>
  );
}

export default App;