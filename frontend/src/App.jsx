import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useAuth, AuthProvider } from './contexts/AuthContext';
import { FullPageLoader } from './components/ui/Loader';
import AppLayout from './components/Layout/AppLayout';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import WorkersPage from './pages/WorkersPage';
import PoliciesPage from './pages/PoliciesPage';
import ClaimsPage from './pages/ClaimsPage';
import TriggerClaimPage from './pages/TriggerClaimPage';
import UsersPage from './pages/UsersPage';
import './App.css';

function ProtectedRoute({ children, allowedRoles }) {
  const { isAuthenticated, hasProfile, loading, role } = useAuth();
  if (loading) return <FullPageLoader />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (!hasProfile) return <Navigate to="/login" replace />;
  if (allowedRoles && !allowedRoles.includes(role)) return <Navigate to="/dashboard" replace />;
  return children;
}

function AppRoutes() {
  const { loading } = useAuth();
  if (loading) return <FullPageLoader />;

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/login/admin" element={<LoginPage />} />
      <Route path="/" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="policies" element={<PoliciesPage />} />
        <Route path="claims" element={<ClaimsPage />} />
        <Route path="trigger-claim" element={<ProtectedRoute allowedRoles={['worker']}><TriggerClaimPage /></ProtectedRoute>} />
        <Route path="workers" element={<ProtectedRoute allowedRoles={['admin','super_admin']}><WorkersPage /></ProtectedRoute>} />
        <Route path="users" element={<ProtectedRoute allowedRoles={['super_admin']}><UsersPage /></ProtectedRoute>} />
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
        <Toaster position="top-right" toastOptions={{
          duration: 4000,
          style: { background: '#fff', color: '#0F172A', borderRadius: '12px', boxShadow: '0 10px 25px -5px rgba(15,23,42,0.1)', fontSize: '0.875rem', fontFamily: 'Inter, sans-serif' },
          success: { iconTheme: { primary: '#10B981', secondary: '#fff' } },
          error: { iconTheme: { primary: '#EF4444', secondary: '#fff' } },
        }} />
      </AuthProvider>
    </BrowserRouter>
  );
}
