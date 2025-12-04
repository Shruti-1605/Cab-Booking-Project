import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { authAPI } from '../services/api';
import { loginSuccess } from '../store/authSlice';

const Login = ({ onToggle }) => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await authAPI.login(formData.email, formData.password);
      dispatch(loginSuccess({
        user: response.data.user,
        token: response.data.access_token
      }));
    } catch (error) {
      alert('Login failed: ' + (error.response?.data?.detail || 'Unknown error'));
    }
    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          className="w-full p-3 border rounded mb-3"
          value={formData.email}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-3 border rounded mb-3"
          value={formData.password}
          onChange={(e) => setFormData({...formData, password: e.target.value})}
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-500 text-white p-3 rounded hover:bg-blue-600"
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p className="mt-4 text-center">
        Don't have an account?{' '}
        <button onClick={onToggle} className="text-blue-500 hover:underline">
          Register
        </button>
      </p>
    </div>
  );
};

export default Login;