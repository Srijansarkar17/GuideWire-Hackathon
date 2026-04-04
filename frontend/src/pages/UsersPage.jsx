import { useEffect, useState } from 'react';
import { listUsers } from '../api/auth';
import DataTable from '../components/ui/DataTable';
import StatusBadge from '../components/ui/StatusBadge';
import Loader from '../components/ui/Loader';

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roleFilter, setRoleFilter] = useState('');

  useEffect(() => { fetchUsers(); }, [roleFilter]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await listUsers(roleFilter || null);
      setUsers(res.data.users || []);
    } catch (err) { console.error(err); }
    setLoading(false);
  };

  const columns = [
    { key: 'display_name', label: 'Name', render: (v) => <span className="font-semibold">{v||'—'}</span> },
    { key: 'email', label: 'Email' },
    { key: 'role', label: 'Role', render: (v) => <StatusBadge status={v} /> },
    { key: 'is_active', label: 'Active', render: (v) => v !== false ? '✅' : '❌' },
    { key: 'created_at', label: 'Created', render: (v) => <span className="text-sm text-muted">{v ? new Date(v).toLocaleDateString() : '—'}</span> },
  ];

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div><h1>User Management</h1><p className="page-subtitle">{users.length} users</p></div>
      </div>
      <div className="filter-bar">
        <select className="form-select" value={roleFilter} onChange={(e) => setRoleFilter(e.target.value)}>
          <option value="">All Roles</option>
          <option value="worker">Worker</option>
          <option value="admin">Admin</option>
          <option value="super_admin">Super Admin</option>
        </select>
      </div>
      {loading ? <Loader /> : <DataTable columns={columns} data={users} emptyMessage="No users found" />}
    </div>
  );
}
