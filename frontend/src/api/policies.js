import { apiClient } from './client';

export const getMyPolicies = async () => {
  const localUserStr = localStorage.getItem('drizzle_local_user');
  if (localUserStr) {
    const worker = JSON.parse(localUserStr);
    return Promise.resolve({
      data: {
        policies: [
          {
            policy_id: worker.uid + '_pol1',
            worker_id: worker.uid,
            zone: worker.zone || 'OMR-Chennai',
            vehicle_type: worker.vehicle_type || 'bike',
            coverage_type: 'comprehensive',
            coverage_days: 30,
            sum_insured: 35000,
            premium: 1250,
            status: 'active',
            created_at: new Date().toISOString(),
            end_date: new Date(Date.now() + 30 * 86400000).toISOString()
          }
        ]
      }
    });
  }
  return apiClient.get('/policies/my-policies');
};

export const listPolicies = (status = null, zone = null, limit = 50) => {
  const params = { limit };
  if (status) params.policy_status = status;
  if (zone) params.zone = zone;
  return apiClient.get('/policies/', { params });
};

export const getPolicyDetail = (policyId) =>
  apiClient.get(`/policies/detail/${policyId}`);

export const getWorkerPolicies = (workerId) =>
  apiClient.get(`/policies/${workerId}`);

export const createPolicy = (data) => apiClient.post('/policies/create', data);

export const calculatePremium = (data) =>
  apiClient.post('/policies/calculate-premium', data);
