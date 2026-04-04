import { apiClient } from './client';

export const getMyClaims = async () => {
  const localUserStr = localStorage.getItem('drizzle_local_user');
  if (localUserStr) {
    const worker = JSON.parse(localUserStr);
    return Promise.resolve({
      data: {
        claims: [
          {
            claim_id: 'clm_a9b8c7',
            policy_id: worker.uid + '_pol1',
            worker_id: worker.uid,
            zone: worker.zone || 'OMR-Chennai',
            lat: 13.0827,
            lon: 80.2707,
            primary_cause: 'weather',
            fused_score: 0.65,
            weather_score: 0.8,
            traffic_score: 0.5,
            social_score: 0.1,
            payout_amount: 850,
            status: 'approved',
            created_at: new Date(Date.now() - 3600000).toISOString(),
            fraud_check: { verdict: 'clean', fraud_score: 0.0 }
          },
          {
            claim_id: 'clm_x3y2z1',
            policy_id: worker.uid + '_pol1',
            worker_id: worker.uid,
            zone: worker.zone || 'OMR-Chennai',
            lat: 13.0827,
            lon: 80.2707,
            primary_cause: 'traffic',
            fused_score: 0.45,
            weather_score: 0.1,
            traffic_score: 0.7,
            social_score: 0.2,
            payout_amount: 0,
            status: 'pending',
            created_at: new Date(Date.now() - 86400000).toISOString(),
            fraud_check: { verdict: 'clean', fraud_score: 0.1 }
          }
        ]
      }
    });
  }
  return apiClient.get('/claims/my-claims');
};

export const listClaims = (status = null, limit = 50) => {
  const params = { limit };
  if (status) params.claim_status = status;
  return apiClient.get('/claims/', { params });
};

export const getClaim = (claimId) => apiClient.get(`/claims/${claimId}`);

export const getWorkerClaims = (workerId) =>
  apiClient.get(`/claims/worker/${workerId}`);

export const triggerClaim = async (data) => {
  const localUserStr = localStorage.getItem('drizzle_local_user');
  if (localUserStr) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: {
            claim_id: 'clm_new_' + Math.floor(Math.random() * 10000),
            status: 'approved',
            payout_amount: 1500,
            primary_cause: 'weather',
            confidence: 'HIGH',
            fused_score: 0.85,
            weather_score: 0.9,
            traffic_score: 0.6,
            social_score: 0.2,
            claim_triggered: true,
            notes: data.notes || '',
            fraud_check: { verdict: 'clean', fraud_score: 0.05 },
            explanation: 'Disruption score exceeded 0.6. Approved automatically.'
          }
        });
      }, 1500); // simulate 1.5s delay
    });
  }
  return apiClient.post('/claims/trigger', data);
};

export const reviewClaim = (claimId, action, notes = null) =>
  apiClient.post(`/claims/${claimId}/review`, { action, notes });
