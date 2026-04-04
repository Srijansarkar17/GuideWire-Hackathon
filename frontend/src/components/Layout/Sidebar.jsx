import { NavLink } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  LayoutDashboard,
  Users,
  Shield,
  FileText,
  AlertTriangle,
  Zap,
  CloudRain,
  LogOut,
  Menu,
  X,
} from 'lucide-react';
import { useState } from 'react';

const NAV_ITEMS = {
  worker: [
    { to: '/dashboard', label: 'Dashboard', icon: <LayoutDashboard size={18} /> },
    { to: '/policies', label: 'My Policies', icon: <Shield size={18} /> },
    { to: '/claims', label: 'My Claims', icon: <FileText size={18} /> },
    { to: '/trigger-claim', label: 'Trigger Claim', icon: <Zap size={18} /> },
  ],
  admin: [
    { to: '/dashboard', label: 'Dashboard', icon: <LayoutDashboard size={18} /> },
    { to: '/workers', label: 'Workers', icon: <Users size={18} /> },
    { to: '/policies', label: 'All Policies', icon: <Shield size={18} /> },
    { to: '/claims', label: 'All Claims', icon: <FileText size={18} /> },
  ],
  super_admin: [
    { to: '/dashboard', label: 'Dashboard', icon: <LayoutDashboard size={18} /> },
    { to: '/workers', label: 'Workers', icon: <Users size={18} /> },
    { to: '/policies', label: 'All Policies', icon: <Shield size={18} /> },
    { to: '/claims', label: 'All Claims', icon: <FileText size={18} /> },
    { to: '/users', label: 'User Management', icon: <AlertTriangle size={18} /> },
  ],
};

export default function Sidebar() {
  const { user, role, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const items = NAV_ITEMS[role] || NAV_ITEMS.worker;

  const initials = user?.display_name
    ? user.display_name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    : '??';

  return (
    <>
      {/* Mobile menu button */}
      <button
        className="mobile-menu-btn"
        onClick={() => setMobileOpen(!mobileOpen)}
        style={{
          position: 'fixed',
          top: 16,
          left: 16,
          zIndex: 60,
          background: 'var(--bg-card)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius)',
          padding: 8,
          display: 'none',
        }}
      >
        {mobileOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Overlay for mobile */}
      {mobileOpen && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.3)',
            zIndex: 45,
            display: 'none',
          }}
          className="mobile-overlay"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside className={`sidebar ${mobileOpen ? 'open' : ''}`}>
        <NavLink to="/dashboard" className="sidebar-logo" onClick={() => setMobileOpen(false)}>
          <div className="sidebar-logo-icon">
            <CloudRain size={20} />
          </div>
          <div className="sidebar-logo-text">
            Dri<span>zzle</span>
          </div>
        </NavLink>

        <nav className="sidebar-nav">
          <div className="sidebar-section">
            <div className="sidebar-section-title">Navigation</div>
            {items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
                onClick={() => setMobileOpen(false)}
              >
                {item.icon}
                <span>{item.label}</span>
              </NavLink>
            ))}
          </div>
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="sidebar-avatar">{initials}</div>
            <div className="sidebar-user-info">
              <div className="sidebar-user-name">{user?.display_name || 'User'}</div>
              <div className="sidebar-user-role">{(role || '').replace('_', ' ')}</div>
            </div>
            <button
              className="btn btn-ghost btn-icon"
              onClick={logout}
              title="Sign Out"
              style={{ marginLeft: 'auto' }}
            >
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
