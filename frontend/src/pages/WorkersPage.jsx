import { useEffect, useState } from 'react';
import { listWorkers } from '../api/workers';
import DataTable from '../components/ui/DataTable';
import StatusBadge from '../components/ui/StatusBadge';
import Loader from '../components/ui/Loader';
import { Users, Search, MapPin } from 'lucide-react';

const ZONES = [
  '', 'OMR-Chennai', 'Andheri-Mumbai', 'Koramangala-Bangalore',
  'Hitech-Hyderabad', 'Connaught-Delhi', 'Salt-Lake-Kolkata',
  'Hinjewadi-Pune', 'Vaishali-Jaipur',
];

export default function WorkersPage() {
  const [workers, setWorkers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [zoneFilter, setZoneFilter] = useState('');
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchWorkers();
  }, [zoneFilter]);

  const fetchWorkers = async () => {
    setLoading(true);
    try {
      const res = await listWorkers(zoneFilter || null);
      setWorkers(res.data.workers || []);
    } catch (err) {
      console.error('Failed to fetch workers:', err);
    }
    setLoading(false);
  };

  const filtered = workers.filter((w) => {
    if (!search) return true;
    const s = search.toLowerCase();
    return (
      (w.display_name || '').toLowerCase().includes(s) ||
      (w.email || '').toLowerCase().includes(s) ||
      (w.zone || '').toLowerCase().includes(s)
    );
  });

  const columns = [
    {
      key: 'display_name',
      label: 'Name',
      render: (val, row) => (
        <div className="flex items-center gap-sm">
          <div style={{
            width: 32, height: 32, borderRadius: '50%',
            background: 'var(--primary-lighter)', color: 'var(--primary)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '0.75rem', fontWeight: 700,
          }}>
            {(val || '?').charAt(0).toUpperCase()}
          </div>
          <div>
            <div className="font-semibold">{val}</div>
            <div className="text-xs text-muted">{row.email}</div>
          </div>
        </div>
      ),
    },
    { key: 'zone', label: 'Zone', render: (val) => (
      <div className="flex items-center gap-xs">
        <MapPin size={14} className="text-muted" />
        {val}
      </div>
    )},
    { key: 'vehicle_type', label: 'Vehicle', render: (val) => {
      const icons = { bike: '🏍️', scooter: '🛵', bicycle: '🚲', auto: '🛺' };
      return <span>{icons[val] || ''} {val}</span>;
    }},
    { key: 'phone', label: 'Phone' },
    { key: 'is_active', label: 'Status', render: (val) => (
      <StatusBadge status={val !== false ? 'active' : 'expired'} />
    )},
    { key: 'created_at', label: 'Joined', render: (val) => (
      <span className="text-sm text-muted">
        {val ? new Date(val).toLocaleDateString() : '—'}
      </span>
    )},
  ];

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1>Workers</h1>
          <p className="page-subtitle">{workers.length} workers registered on the platform</p>
        </div>
      </div>

      <div className="filter-bar">
        <div className="form-group" style={{ flex: 1, maxWidth: 300 }}>
          <div style={{ position: 'relative' }}>
            <Search size={16} style={{
              position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
              color: 'var(--text-muted)',
            }} />
            <input
              className="form-input"
              style={{ paddingLeft: 36 }}
              placeholder="Search by name, email, or zone..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>
        <select
          className="form-select"
          value={zoneFilter}
          onChange={(e) => setZoneFilter(e.target.value)}
        >
          <option value="">All Zones</option>
          {ZONES.filter(Boolean).map((z) => (
            <option key={z} value={z}>{z}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <Loader message="Loading workers..." />
      ) : (
        <DataTable
          columns={columns}
          data={filtered}
          emptyMessage="No workers found"
        />
      )}
    </div>
  );
}
