import { apiClient } from './client';

export const getWorkerDashboard = async () => {
  const localUserStr = localStorage.getItem('drizzle_local_user');
  if (localUserStr) {
    const worker = JSON.parse(localUserStr);
    return Promise.resolve({
      data: {
        worker,
        policies: {
          active: 1,
          total: 1,
          list: [
            {
              policy_id: worker.uid + '_pol1',
              status: 'active',
              coverage_type: 'comprehensive',
              coverage_days: 30,
              sum_insured: 35000,
              premium: 1250,
            }
          ]
        },
        claims: {
          total: 2,
          pending: 1,
          total_payout: 850,
          list: [
            {
              claim_id: 'clm_a9b8c7',
              zone: worker.zone || 'OMR-Chennai',
              primary_cause: 'weather',
              payout_amount: 850,
              status: 'approved',
              created_at: new Date().toISOString()
            },
            {
              claim_id: 'clm_x3y2z1',
              zone: worker.zone || 'OMR-Chennai',
              primary_cause: 'traffic',
              payout_amount: 0,
              status: 'pending',
              created_at: new Date(Date.now() - 86400000).toISOString()
            }
          ]
        }
      }
    });
  }
  return apiClient.get('/dashboard/worker');
};

export const getAdminDashboard = () => apiClient.get('/dashboard/admin');

export const getSuperAdminDashboard = () => apiClient.get('/dashboard/super-admin');

export const getWorkerDashboardById = (workerId) =>
  apiClient.get(`/dashboard/worker/${workerId}`);
