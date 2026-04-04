import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import {
  getWorkerDashboard,
  getAdminDashboard,
  getSuperAdminDashboard,
} from '../api/dashboard';
import StatCard from '../components/ui/StatCard';
import StatusBadge from '../components/ui/StatusBadge';
import Loader from '../components/ui/Loader';
import {
  Users,
  Shield,
  FileText,
  DollarSign,
  AlertTriangle,
  CheckCircle2,
  Clock,
  TrendingUp,
  CloudRain,
  Car,
  Megaphone,
} from 'lucide-react';

export default function DashboardPage() {
  const { role } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      setLoading(true);
      try {
        let res;
        if (role === 'super_admin') {
          res = await getSuperAdminDashboard();
        } else if (role === 'admin') {
          res = await getAdminDashboard();
        } else {
          res = await getWorkerDashboard();
        }
        setData(res.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load dashboard');
      }
      setLoading(false);
    };
    fetchDashboard();
  }, [role]);

  if (loading) return <Loader message="Loading dashboard..." />;

  if (error) {
    return (
      <div className="empty-state">
        <AlertTriangle size={48} />
        <h3>Error loading dashboard</h3>
        <p className="text-sm text-muted">{error}</p>
      </div>
    );
  }

  if (role === 'worker') return <WorkerDashboard data={data} />;
  return <AdminDashboard data={data} role={role} />;
}

function WorkerDashboard({ data }) {
  const worker = data?.worker || {};
  // API returns { list, total, active, ... } — not a raw array
  const policiesBlock = Array.isArray(data?.policies)
    ? { list: data.policies }
    : (data?.policies ?? {});
  const claimsBlock = Array.isArray(data?.claims)
    ? { list: data.claims }
    : (data?.claims ?? {});
  const policies = policiesBlock.list ?? [];
  const claims = claimsBlock.list ?? [];

  const totalPayout =
    typeof claimsBlock.total_payout === 'number'
      ? claimsBlock.total_payout
      : claims.reduce((sum, c) => sum + (c.payout_amount || 0), 0);
  const totalClaimsCount =
    typeof claimsBlock.total === 'number' ? claimsBlock.total : claims.length;
  const pendingClaimsCount =
    typeof claimsBlock.pending === 'number'
      ? claimsBlock.pending
      : claims.filter((c) => c.status === 'pending').length;
  const activePoliciesCount =
    typeof policiesBlock.active === 'number'
      ? policiesBlock.active
      : policies.filter((p) => p.status === 'active').length;

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1>Welcome back, {worker.display_name || 'Worker'} 👋</h1>
          <p className="page-subtitle">
            Zone: {worker.zone || '—'} &middot; Vehicle: {worker.vehicle_type || '—'}
          </p>
        </div>
      </div>

      <div className="dashboard-grid stagger">
        <StatCard
          icon={<Shield size={20} />}
          label="Active Policies"
          value={activePoliciesCount}
          color="blue"
          delay={0}
        />
        <StatCard
          icon={<FileText size={20} />}
          label="Total Claims"
          value={totalClaimsCount}
          color="indigo"
          delay={60}
        />
        <StatCard
          icon={<DollarSign size={20} />}
          label="Total Payouts"
          value={`₹${totalPayout.toLocaleString('en-IN')}`}
          color="green"
          delay={120}
        />
        <StatCard
          icon={<Clock size={20} />}
          label="Pending Claims"
          value={pendingClaimsCount}
          color="amber"
          delay={180}
        />
      </div>

      {/* Recent Claims */}
      <div className="dashboard-section">
        <div className="dashboard-section-header">
          <h3>Recent Claims</h3>
        </div>
        {claims.length === 0 ? (
          <div className="card text-center text-muted" style={{ padding: '2rem' }}>
            No claims yet. Your claims will appear here.
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Claim ID</th>
                  <th>Zone</th>
                  <th>Cause</th>
                  <th>Payout</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {claims.slice(0, 5).map((claim) => (
                  <tr key={claim.claim_id}>
                    <td className="font-medium">{claim.claim_id?.slice(0, 12)}...</td>
                    <td>{claim.zone}</td>
                    <td style={{ textTransform: 'capitalize' }}>{claim.primary_cause || '—'}</td>
                    <td className="font-semibold">₹{(claim.payout_amount || 0).toLocaleString('en-IN')}</td>
                    <td><StatusBadge status={claim.status} /></td>
                    <td className="text-muted text-sm">
                      {claim.created_at ? new Date(claim.created_at).toLocaleDateString() : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Policies */}
      <div className="dashboard-section">
        <div className="dashboard-section-header">
          <h3>My Policies</h3>
        </div>
        {policies.length === 0 ? (
          <div className="card text-center text-muted" style={{ padding: '2rem' }}>
            No policies yet. Contact an admin to get insured.
          </div>
        ) : (
          <div className="grid-2 stagger">
            {policies.map((policy, i) => (
              <div key={policy.policy_id} className="card animate-fade-in-up" style={{ animationDelay: `${i * 80}ms` }}>
                <div className="flex items-center justify-between mb-sm">
                  <span className="text-sm font-semibold text-primary">
                    {policy.policy_id?.slice(0, 16)}
                  </span>
                  <StatusBadge status={policy.status} />
                </div>
                <div className="text-xs text-muted mb-sm" style={{ textTransform: 'capitalize' }}>
                  {policy.coverage_type} Coverage &middot; {policy.coverage_days} days
                </div>
                <div className="flex justify-between items-center mt-md">
                  <div>
                    <div className="text-xs text-muted">Sum Insured</div>
                    <div className="font-bold">₹{policy.sum_insured?.toLocaleString('en-IN')}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-muted">Premium</div>
                    <div className="font-bold text-primary">₹{policy.premium?.toLocaleString('en-IN')}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function AdminDashboard({ data, role }) {
  const zoneBreakdown = data?.zone_breakdown || {};
  const claimStatusBreakdown = data?.claim_status_breakdown || {};

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1>{role === 'super_admin' ? 'Super Admin' : 'Admin'} Dashboard</h1>
          <p className="page-subtitle">Platform-wide overview and analytics</p>
        </div>
      </div>

      <div className="dashboard-grid stagger">
        <StatCard
          icon={<Users size={20} />}
          label="Total Workers"
          value={data?.total_workers || 0}
          color="blue"
          delay={0}
        />
        <StatCard
          icon={<Shield size={20} />}
          label="Active Policies"
          value={data?.active_policies || 0}
          color="green"
          delay={60}
        />
        <StatCard
          icon={<FileText size={20} />}
          label="Total Claims"
          value={data?.total_claims || 0}
          color="indigo"
          delay={120}
        />
        <StatCard
          icon={<DollarSign size={20} />}
          label="Total Payouts"
          value={`₹${(data?.total_payout || 0).toLocaleString('en-IN')}`}
          color="green"
          delay={180}
        />
      </div>

      {/* Second row of stats */}
      <div className="dashboard-grid stagger" style={{ marginTop: 0 }}>
        <StatCard
          icon={<Clock size={20} />}
          label="Pending Claims"
          value={data?.pending_claims || 0}
          color="amber"
          delay={240}
        />
        <StatCard
          icon={<CheckCircle2 size={20} />}
          label="Approved Claims"
          value={data?.approved_claims || 0}
          color="green"
          delay={300}
        />
        <StatCard
          icon={<AlertTriangle size={20} />}
          label="Avg Fraud Score"
          value={(data?.avg_fraud_score || 0).toFixed(3)}
          color="red"
          delay={360}
        />
        <StatCard
          icon={<TrendingUp size={20} />}
          label="Total Policies"
          value={data?.total_policies || 0}
          color="blue"
          delay={420}
        />
      </div>

      {/* Zone Breakdown */}
      {Object.keys(zoneBreakdown).length > 0 && (
        <div className="dashboard-section">
          <div className="dashboard-section-header">
            <h3>Zone Breakdown</h3>
          </div>
          <div className="grid-3 stagger">
            {Object.entries(zoneBreakdown).map(([zone, stats], i) => (
              <div key={zone} className="card animate-fade-in-up" style={{ animationDelay: `${i * 60}ms` }}>
                <h4 style={{ marginBottom: 8 }}>{zone}</h4>
                <div className="flex flex-col gap-xs">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted">Workers</span>
                    <span className="font-semibold">{stats.workers || 0}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted">Policies</span>
                    <span className="font-semibold">{stats.policies || 0}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted">Claims</span>
                    <span className="font-semibold">{stats.claims || 0}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted">Payouts</span>
                    <span className="font-semibold text-accent">₹{(stats.payouts || 0).toLocaleString('en-IN')}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Claim Status Breakdown */}
      {Object.keys(claimStatusBreakdown).length > 0 && (
        <div className="dashboard-section">
          <div className="dashboard-section-header">
            <h3>Claim Status Distribution</h3>
          </div>
          <div className="card">
            <div className="flex gap-lg" style={{ flexWrap: 'wrap' }}>
              {Object.entries(claimStatusBreakdown).map(([status, count]) => (
                <div key={status} className="flex items-center gap-sm">
                  <StatusBadge status={status} />
                  <span className="font-bold">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Super Admin: Role Distribution */}
      {role === 'super_admin' && data?.role_distribution && (
        <div className="dashboard-section">
          <div className="dashboard-section-header">
            <h3>Role Distribution</h3>
            <span className="text-sm text-muted">{data.total_users || 0} total users</span>
          </div>
          <div className="grid-3 stagger">
            {Object.entries(data.role_distribution).map(([r, count], i) => (
              <div key={r} className="card animate-fade-in-up" style={{ animationDelay: `${i * 60}ms` }}>
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-xs text-muted" style={{ textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 4 }}>
                      {r.replace('_', ' ')}
                    </div>
                    <div className="font-bold text-lg">{count}</div>
                  </div>
                  <StatusBadge status={r} />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
