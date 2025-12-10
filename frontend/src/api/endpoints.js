import apiClient from './axios';

// Authentication endpoints
export const authApi = {
  register: (email, password) =>
    apiClient.post('/auth/register', { email, password }),
  login: (email, password) =>
    apiClient.post('/auth/login', { email, password }),
  getCurrentUser: () =>
    apiClient.get('/auth/me'),
  deleteAccount: () =>
    apiClient.delete('/auth/me'),
};

// Tracker endpoints
export const trackerApi = {
  getAll: () =>
    apiClient.get('/trackers'),
  getById: (id) =>
    apiClient.get(`/trackers/${id}`),
  create: (productUrl, targetPrice, pollingIntervalMinutes = 60) =>
    apiClient.post('/trackers', {
      product_url: productUrl,
      target_price: targetPrice,
      polling_interval_minutes: pollingIntervalMinutes,
    }),
  update: (id, data) =>
    apiClient.put(`/trackers/${id}`, data),
  delete: (id) =>
    apiClient.delete(`/trackers/${id}`),
  getPriceHistory: (id) =>
    apiClient.get(`/trackers/${id}/history`),
};

export default {
  auth: authApi,
  tracker: trackerApi,
};
