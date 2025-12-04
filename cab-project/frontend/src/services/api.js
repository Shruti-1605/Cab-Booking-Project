import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (userData) => api.post('/api/auth/register', userData),
  login: (email, password) => api.post('/api/auth/login', { email, password }),
};

export const rideAPI = {
  requestRide: (rideData) => api.post('/api/rides/request', rideData),
  getNearbyDrivers: (lat, lng) => api.get(`/api/rides/nearby-drivers?lat=${lat}&lng=${lng}`),
  acceptRide: (rideId) => api.post(`/api/rides/${rideId}/accept`),
  getRideHistory: () => api.get('/api/rides/history'),
};

export const paymentAPI = {
  createPaymentIntent: (paymentData) => api.post('/api/payments/intent', paymentData),
  createCustomer: (customerData) => api.post('/api/payments/customer', customerData),
  getPaymentStatus: (paymentId) => api.get(`/api/payments/status/${paymentId}`),
};

export const reviewAPI = {
  createReview: (reviewData) => api.post('/reviews', reviewData),
};

export default api;