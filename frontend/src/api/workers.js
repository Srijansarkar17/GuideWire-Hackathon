import { apiClient } from './client';

export const getMyProfile = () => apiClient.get('/workers/me');

export const listWorkers = (zone = null, limit = 50) => {
  const params = { limit };
  if (zone) params.zone = zone;
  return apiClient.get('/workers/', { params });
};

export const getWorker = (workerId) => apiClient.get(`/workers/${workerId}`);

export const registerWorker = (data) => apiClient.post('/workers/register', data);
