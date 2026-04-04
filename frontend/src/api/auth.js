import { apiClient } from './client';

export const getMe = () => apiClient.get('/auth/me');

export const listUsers = (role = null, limit = 50) => {
  const params = { limit };
  if (role) params.role = role;
  return apiClient.get('/auth/users', { params });
};

export const promoteUser = (targetUid, newRole) =>
  apiClient.post('/auth/promote', null, {
    params: { target_uid: targetUid, new_role: newRole },
  });

/** First super_admin only — requires DRIZZLE_BOOTSTRAP_SECRET on the server */
export const bootstrapSuperAdmin = (secret) =>
  apiClient.post('/auth/bootstrap-super-admin', { secret });
