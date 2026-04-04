import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { getMyPolicies, listPolicies, createPolicy, calculatePremium } from '../api/policies';
import { listWorkers } from '../api/workers';
import DataTable from '../components/ui/DataTable';
import StatusBadge from '../components/ui/StatusBadge';
import Modal from '../components/ui/Modal';
import Loader from '../components/ui/Loader';
import { Shield, Plus, Calculator } from 'lucide-react';
import toast from 'react-hot-toast';

const ZONES = [
  'OMR-Chennai', 'Andheri-Mumbai', 'Koramangala-Bangalore',
  'Hitech-Hyderabad', 'Connaught-Delhi', 'Salt-Lake-Kolkata',
  'Hinjewadi-Pune', 'Vaishali-Jaipur',
];

export default function PoliciesPage() {
  const { role } = useAuth();
  const isAdmin = role === 'admin' || role === 'super_admin';

  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    fetchPolicies();
  }, [statusFilter]);

  const fetchPolicies = async () => {
    setLoading(true);
    try {
      const res = isAdmin
        ? await listPolicies(statusFilter || null)
        : await getMyPolicies();
      setPolicies(res.data.policies || []);
    } catch (err) {
      console.error('Failed to fetch policies:', err);
    }
    setLoading(false);
  };

  const columns = [
    {
      key: 'policy_id',
      label: 'Policy ID',
      render: (val) => <span className="font-medium text-primary">{val?.slice(0, 16)}</span>,
    },
    ...(isAdmin ? [{
      key: 'worker_id',
      label: 'Worker',
      render: (val) => <span className="text-sm">{val?.slice(0, 12)}...</span>,
    }] : []),
    { key: 'zone', label: 'Zone' },
    {
      key: 'coverage_type',
      label: 'Coverage',
      render: (val) => <span style={{ textTransform: 'capitalize' }}>{val}</span>,
    },
    {
      key: 'coverage_days',
      label: 'Days',
      render: (val) => <span className="font-medium">{val}</span>,
    },
    {
      key: 'sum_insured',
      label: 'Sum Insured',
      render: (val) => <span className="font-semibold">₹{val?.toLocaleString('en-IN')}</span>,
    },
    {
      key: 'premium',
      label: 'Premium',
      render: (val) => <span className="font-semibold text-primary">₹{val?.toLocaleString('en-IN')}</span>,
    },
    {
      key: 'status',
      label: 'Status',
      render: (val) => <StatusBadge status={val} />,
    },
    {
      key: 'created_at',
      label: 'Created',
      render: (val) => (
        <span className="text-sm text-muted">
          {val ? new Date(val).toLocaleDateString() : '—'}
        </span>
      ),
    },
  ];

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1>{isAdmin ? 'All Policies' : 'My Policies'}</h1>
          <p className="page-subtitle">{policies.length} policies total</p>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={() => setShowCreate(true)}>
            <Plus size={16} />
            Create Policy
          </button>
        )}
      </div>

      <div className="filter-bar">
        <select
          className="form-select"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="expired">Expired</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>

      {loading ? (
        <Loader message="Loading policies..." />
      ) : (
        <DataTable
          columns={columns}
          data={policies}
          emptyMessage="No policies found"
        />
      )}

      {showCreate && (
        <CreatePolicyModal
          onClose={() => setShowCreate(false)}
          onCreated={() => {
            setShowCreate(false);
            fetchPolicies();
          }}
        />
      )}
    </div>
  );
}

function CreatePolicyModal({ onClose, onCreated }) {
  const [workerId, setWorkerId] = useState('');
  const [zone, setZone] = useState('OMR-Chennai');
  const [coverageType, setCoverageType] = useState('comprehensive');
  const [coverageDays, setCoverageDays] = useState(30);
  const [sumInsured, setSumInsured] = useState(30000);
  const [submitting, setSubmitting] = useState(false);
  const [preview, setPreview] = useState(null);
  const [workers, setWorkers] = useState([]);

  useEffect(() => {
    listWorkers()
      .then((res) => setWorkers(res.data.workers || []))
      .catch(() => {});
  }, []);

  const handlePreview = async () => {
    try {
      const res = await calculatePremium({
        worker_id: workerId,
        zone,
        coverage_type: coverageType,
        coverage_days: coverageDays,
        sum_insured: sumInsured,
      });
      setPreview(res.data);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Preview failed');
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await createPolicy({
        worker_id: workerId,
        zone,
        coverage_type: coverageType,
        coverage_days: coverageDays,
        sum_insured: sumInsured,
      });
      toast.success('Policy created successfully!');
      onCreated();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to create policy');
    }
    setSubmitting(false);
  };

  return (
    <Modal isOpen title="Create New Policy" onClose={onClose} size="lg">
      <form onSubmit={handleCreate} className="flex flex-col gap-md">
        <div className="form-group">
          <label className="form-label">Worker</label>
          <select
            className="form-select"
            value={workerId}
            onChange={(e) => setWorkerId(e.target.value)}
            required
          >
            <option value="">Select a worker...</option>
            {workers.map((w) => (
              <option key={w.uid} value={w.uid}>
                {w.display_name} — {w.zone} ({w.email})
              </option>
            ))}
          </select>
        </div>

        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Zone</label>
            <select className="form-select" value={zone} onChange={(e) => setZone(e.target.value)}>
              {ZONES.map((z) => <option key={z} value={z}>{z}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Coverage Type</label>
            <select className="form-select" value={coverageType} onChange={(e) => setCoverageType(e.target.value)}>
              <option value="comprehensive">Comprehensive</option>
              <option value="weather">Weather Only</option>
              <option value="traffic">Traffic Only</option>
              <option value="social">Social Only</option>
            </select>
          </div>
        </div>

        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Coverage Days</label>
            <input
              className="form-input"
              type="number"
              min={1}
              max={365}
              value={coverageDays}
              onChange={(e) => setCoverageDays(Number(e.target.value))}
            />
          </div>
          <div className="form-group">
            <label className="form-label">Sum Insured (₹)</label>
            <input
              className="form-input"
              type="number"
              min={1000}
              max={500000}
              value={sumInsured}
              onChange={(e) => setSumInsured(Number(e.target.value))}
            />
          </div>
        </div>

        {preview && (
          <div className="card" style={{ background: 'var(--primary-lighter)', border: 'none' }}>
            <h4 className="mb-sm text-primary">Premium Preview</h4>
            <div className="flex justify-between text-sm mb-sm">
              <span>Premium</span>
              <span className="font-bold">₹{preview.premium?.toLocaleString('en-IN')}</span>
            </div>
            <div className="flex justify-between text-sm mb-sm">
              <span>Daily Rate</span>
              <span className="font-semibold">₹{preview.daily_rate?.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Risk Score</span>
              <span className="font-semibold">{preview.risk_score?.toFixed(3)}</span>
            </div>
          </div>
        )}

        <div className="flex gap-md" style={{ marginTop: 8 }}>
          <button
            type="button"
            className="btn btn-outline"
            onClick={handlePreview}
            disabled={!workerId}
          >
            <Calculator size={16} />
            Preview Premium
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={submitting || !workerId}
            style={{ flex: 1 }}
          >
            {submitting ? 'Creating...' : 'Create Policy'}
          </button>
        </div>
      </form>
    </Modal>
  );
}
