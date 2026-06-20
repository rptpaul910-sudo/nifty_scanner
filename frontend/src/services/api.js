import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const stocksApi = {
  getTopGainers: async (limit = 10) => {
    const response = await api.get(`/api/top-gainers?limit=${limit}`);
    return response.data;
  },

  getTopLosers: async (limit = 10) => {
    const response = await api.get(`/api/top-losers?limit=${limit}`);
    return response.data;
  },

  getAllStocks: async () => {
    const response = await api.get('/api/all-stocks');
    return response.data;
  },

  getMarketSummary: async () => {
    const response = await api.get('/api/market-summary');
    return response.data;
  },

  refreshData: async () => {
    const response = await api.post('/api/refresh');
    return response.data;
  },

  getHistoricalGainers: async (limit = 10, days = 7) => {
    const response = await api.get(`/api/historical-gainers?limit=${limit}&days=${days}`);
    return response.data;
  },
};

export default api;
