// API Service - Backend Communication
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

// Model info
export const getModelInfo = async () => {
  const response = await api.get('/api/model/info');
  return response.data;
};

// Train model
export const trainModel = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/train', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Retrain model
export const retrainModel = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/retrain', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Predict
export const predict = async (data) => {
  const response = await api.post('/api/predict', data);
  return response.data;
};

// Get metrics
export const getMetrics = async () => {
  const response = await api.get('/api/metrics');
  return response.data;
};

// Get feature importance
export const getFeatureImportance = async () => {
  const response = await api.get('/api/features/importance');
  return response.data;
};

export default api;
