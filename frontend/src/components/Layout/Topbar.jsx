import { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { LogOut } from 'lucide-react';
import StatusBadge from '../ui/StatusBadge';

export default function Topbar({ title }) {
  const { user, role, logout } = useAuth();
  const [health, setHealth] = useState(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('http://localhost:8000/health');
        const data = await res.json();
        setHealth(data);
      } catch {
        setHealth({ status: 'error' });
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="topbar">
      <div className="topbar-left">
        <h2 className="topbar-title">{title || 'Dashboard'}</h2>
      </div>
      <div className="topbar-right">
        {health && (
          <div className="topbar-health">
            <div className={`topbar-health-dot ${health.status === 'ok' ? '' : 'offline'}`} />
            <span>API {health.status === 'ok' ? 'Online' : 'Offline'}</span>
          </div>
        )}
        {role && <StatusBadge status={role} />}
        <button className="topbar-btn-logout" onClick={logout}>
          <LogOut size={14} />
          Sign Out
        </button>
      </div>
    </div>
  );
}
