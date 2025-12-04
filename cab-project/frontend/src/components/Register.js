import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { authAPI } from '../services/api';
import { loginSuccess } from '../store/authSlice';

const Register = ({ onToggle }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    role: 'rider'
  });
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await authAPI.register(formData);
      // Auto login after successful registration
      const loginResponse = await authAPI.login(formData.email, formData.password);
      dispatch(loginSuccess({
        user: loginResponse.data.user,
        token: loginResponse.data.access_token
      }));
      alert('Registration successful! Welcome!');
    } catch (error) {
      alert('Registration failed: ' + (error.response?.data?.detail || 'Unknown error'));
    }
    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Full Name"
          className="w-full p-3 border rounded mb-3"
          value={formData.name}
          onChange={(e) => setFormData({...formData, name: e.target.value})}
          required
        />
        <input
          type="email"
          placeholder="Email"
          className="w-full p-3 border rounded mb-3"
          value={formData.email}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
          required
        />
        <input
          type="tel"
          placeholder="Phone Number"
          className="w-full p-3 border rounded mb-3"
          value={formData.phone}
          onChange={(e) => setFormData({...formData, phone: e.target.value})}
          required
        />
        <select
          className="w-full p-3 border rounded mb-3"
          value={formData.role}
          onChange={(e) => setFormData({...formData, role: e.target.value})}
        >
          <option value="rider">Rider</option>
          <option value="driver">Driver</option>
          <option value="admin">Admin</option>
        </select>
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
          className="w-full bg-green-500 text-white p-3 rounded hover:bg-green-600"
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      <p className="mt-4 text-center">
        Already have an account?{' '}
        <button onClick={onToggle} className="text-blue-500 hover:underline">
          Login
        </button>
      </p>
    </div>
  );
};

export default Register;