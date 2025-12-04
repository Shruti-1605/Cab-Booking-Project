import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const bookingAPI = {
  getCabs: () => api.get('/cabs'),
  bookCab: (bookingData) => api.post('/bookings', bookingData),
  getBookings: () => api.get('/bookings'),
  getFareEstimate: (pickup, destination) => api.get(`/fare/estimate?pickup=${pickup}&destination=${destination}`),
  validatePromo: (promoData) => api.post('/promo/validate', promoData),
  getWalletBalance: (userId) => api.get(`/wallet/${userId}`),
  topupWallet: (topupData) => api.post('/wallet/topup', topupData),
  submitReview: (reviewData) => api.post('/reviews', reviewData),
  getNotifications: (userId) => api.get(`/notifications/${userId}`),
  trackRide: (rideId) => api.get(`/ride/track/${rideId}`),
  getDriverLocation: (driverId) => api.get(`/driver/location/${driverId}`),
};

export default api;