import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';
import '../../App.css';

const TITLES = {
  '/dashboard': 'Dashboard',
  '/workers': 'Workers',
  '/policies': 'Policies',
  '/claims': 'Claims',
  '/trigger-claim': 'Trigger Claim',
  '/users': 'User Management',
};

export default function AppLayout() {
  const location = useLocation();
  const title = TITLES[location.pathname] || 'Drizzle';

  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Topbar title={title} />
        <div className="page-container">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
