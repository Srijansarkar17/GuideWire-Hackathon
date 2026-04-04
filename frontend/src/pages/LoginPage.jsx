import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, useSearchParams, useLocation } from 'react-router-dom';
import { registerWorker } from '../api/workers';
import { bootstrapSuperAdmin } from '../api/auth';
import { CloudRain, AlertCircle, Shield } from 'lucide-react';

export default function LoginPage() {
  const {
    loginWithGoogle,
    loginWithEmail,
    error,
    setError,
    isAuthenticated,
    hasProfile,
    refreshProfile,
    localRegister,
  } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const staffDocsOpen =
    location.pathname === '/login/admin' || searchParams.get('staff') === '1';

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [isLocalRegistering, setIsLocalRegistering] = useState(false);

  const [regName, setRegName] = useState('');
  const [regPhone, setRegPhone] = useState('');
  const [regZone, setRegZone] = useState('OMR-Chennai');
  const [regVehicle, setRegVehicle] = useState('bike');

  /** After Firebase auth, choose worker onboarding vs staff (admin) profile */
  const [accountType, setAccountType] = useState('worker');
  const [bootstrapSecret, setBootstrapSecret] = useState('');

  useEffect(() => {
    if (isAuthenticated && hasProfile) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, hasProfile, navigate]);

  if (isAuthenticated && hasProfile) {
    return null;
  }

  const handleLocalRegisterSubmit = (e) => {
    e.preventDefault();
    localRegister({
      display_name: regName,
      email: email,
      phone: regPhone,
      zone: regZone,
      vehicle_type: regVehicle,
    });
    navigate('/dashboard');
  };

  const handleGoogleLogin = async () => {
    setSubmitting(true);
    try {
      await loginWithGoogle();
    } catch {
      // Error already set in context
    }
    setSubmitting(false);
  };

  const handleEmailLogin = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await loginWithEmail(email, password);
    } catch {
      // Error already set in context
    }
    setSubmitting(false);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await registerWorker({
        display_name: regName,
        phone: regPhone,
        zone: regZone,
        vehicle_type: regVehicle,
      });
      window.location.reload();
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
    setSubmitting(false);
  };

  const handleBootstrapSuperAdmin = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await bootstrapSuperAdmin(bootstrapSecret.trim());
      await refreshProfile();
      navigate('/dashboard', { replace: true });
    } catch (err) {
      const d = err.response?.data?.detail;
      setError(typeof d === 'string' ? d : Array.isArray(d) ? d[0]?.msg : 'Bootstrap failed');
    }
    setSubmitting(false);
  };

  if (isLocalRegistering) {
    return (
      <div className="login-wrapper">
        <div className="login-card" style={{ maxWidth: 440 }}>
          <div className="login-logo">
            <div className="login-logo-icon">
              <CloudRain size={28} />
            </div>
            <h1>Register</h1>
            <p>Register</p>
          </div>
          <form onSubmit={handleLocalRegisterSubmit} className="flex flex-col gap-md">
            <div className="form-group">
              <label className="form-label">Full Name</label>
              <input
                className="form-input"
                type="text"
                value={regName}
                onChange={(e) => setRegName(e.target.value)}
                placeholder="Rahul Kumar"
                required
                minLength={2}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input
                className="form-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="worker@example.com"
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Zone</label>
              <select className="form-select" value={regZone} onChange={(e) => setRegZone(e.target.value)}>
                <option value="OMR-Chennai">OMR-Chennai</option>
                <option value="Andheri-Mumbai">Andheri-Mumbai</option>
                <option value="Koramangala-Bangalore">Koramangala-Bangalore</option>
                <option value="Hitech-Hyderabad">Hitech-Hyderabad</option>
                <option value="Connaught-Delhi">Connaught-Delhi</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Vehicle Type</label>
              <select className="form-select" value={regVehicle} onChange={(e) => setRegVehicle(e.target.value)}>
                <option value="bike">Bike</option>
                <option value="scooter">Scooter</option>
                <option value="bicycle">Bicycle</option>
                <option value="auto">Auto</option>
              </select>
            </div>
            <div className="flex gap-sm mt-sm">
              <button type="submit" className="btn btn-primary btn-lg flex-1">
                Register
              </button>
              <button type="button" className="btn btn-outline btn-lg" onClick={() => setIsLocalRegistering(false)}>
                Back
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  // Firebase user present but no Firestore users/{uid} profile yet
  if (isAuthenticated && !hasProfile) {
    return (
      <div className="login-wrapper">
        <div className="login-card" style={{ maxWidth: 440 }}>
          <div className="login-logo">
            <div className="login-logo-icon">
              <CloudRain size={28} />
            </div>
            <h1>Complete your account</h1>
            <p>Choose how this login should be registered in Drizzle.</p>
          </div>

          <div className="flex gap-sm mb-md" style={{ flexWrap: 'wrap' }}>
            <button
              type="button"
              className={`btn btn-sm ${accountType === 'worker' ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => {
                setAccountType('worker');
                setError(null);
              }}
            >
              Delivery worker
            </button>
            <button
              type="button"
              className={`btn btn-sm flex items-center gap-xs ${accountType === 'staff' ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => {
                setAccountType('staff');
                setError(null);
              }}
            >
              <Shield size={16} />
              Admin / staff
            </button>
          </div>

          {error && (
            <div className="login-error">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          {accountType === 'worker' ? (
            <form onSubmit={handleRegister} className="flex flex-col gap-md">
              <p className="text-sm text-muted" style={{ marginTop: 0 }}>
                Creates your worker profile so you can receive policies and file claims.
              </p>
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input
                  className="form-input"
                  type="text"
                  value={regName}
                  onChange={(e) => setRegName(e.target.value)}
                  placeholder="Rahul Kumar"
                  required
                  minLength={2}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Phone Number</label>
                <input
                  className="form-input"
                  type="text"
                  value={regPhone}
                  onChange={(e) => setRegPhone(e.target.value)}
                  placeholder="+919876543210"
                  required
                  minLength={10}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Zone</label>
                <select
                  className="form-select"
                  value={regZone}
                  onChange={(e) => setRegZone(e.target.value)}
                >
                  <option value="OMR-Chennai">OMR-Chennai</option>
                  <option value="Andheri-Mumbai">Andheri-Mumbai</option>
                  <option value="Koramangala-Bangalore">Koramangala-Bangalore</option>
                  <option value="Hitech-Hyderabad">Hitech-Hyderabad</option>
                  <option value="Connaught-Delhi">Connaught-Delhi</option>
                  <option value="Salt-Lake-Kolkata">Salt-Lake-Kolkata</option>
                  <option value="Hinjewadi-Pune">Hinjewadi-Pune</option>
                  <option value="Vaishali-Jaipur">Vaishali-Jaipur</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Vehicle Type</label>
                <select
                  className="form-select"
                  value={regVehicle}
                  onChange={(e) => setRegVehicle(e.target.value)}
                >
                  <option value="bike">Bike</option>
                  <option value="scooter">Scooter</option>
                  <option value="bicycle">Bicycle</option>
                  <option value="auto">Auto</option>
                </select>
              </div>
              <button
                type="submit"
                className="btn btn-primary btn-lg w-full mt-sm"
                disabled={submitting}
              >
                {submitting ? 'Registering...' : 'Register as worker'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleBootstrapSuperAdmin} className="flex flex-col gap-md">
              <p className="text-sm text-muted" style={{ marginTop: 0, lineHeight: 1.55 }}>
                <strong>Same sign-in as workers</strong> (Google or email). Staff accounts are stored
                in Firestore with role <code>admin</code> or <code>super_admin</code> — not via the
                worker form above.
              </p>
              <p className="text-sm text-muted" style={{ lineHeight: 1.55 }}>
                <strong>Option A — First super admin (once):</strong> set{' '}
                <code>DRIZZLE_BOOTSTRAP_SECRET</code> in the backend <code>.env</code>, restart
                Uvicorn, then enter that secret here.
              </p>
              <p className="text-sm text-muted" style={{ lineHeight: 1.55 }}>
                <strong>Option B:</strong> run{' '}
                <code style={{ fontSize: '0.75rem' }}>
                  python -m backend.scripts.seed_admin --uid &lt;UID&gt; --email &lt;E&gt; --role
                  admin
                </code>{' '}
                after you know your Firebase UID (Authentication tab in Firebase Console).
              </p>
              <div className="form-group">
                <label className="form-label">Bootstrap secret (Option A only)</label>
                <input
                  className="form-input"
                  type="password"
                  autoComplete="off"
                  value={bootstrapSecret}
                  onChange={(e) => setBootstrapSecret(e.target.value)}
                  placeholder="Matches DRIZZLE_BOOTSTRAP_SECRET on the server"
                />
              </div>
              <button
                type="submit"
                className="btn btn-primary btn-lg w-full"
                disabled={submitting || !bootstrapSecret.trim()}
              >
                {submitting ? 'Creating profile...' : 'Create first super admin profile'}
              </button>
            </form>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="login-wrapper">
      <div className="login-card">
        <div className="login-logo">
          <div className="login-logo-icon">
            <CloudRain size={28} />
          </div>
          <h1>Welcome to Drizzle</h1>
          <p>Parametric insurance for gig workers</p>
        </div>

        {error && (
          <div className="login-error">
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        <button className="btn-google" onClick={handleGoogleLogin} disabled={submitting}>
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          {submitting ? 'Signing in...' : 'Sign in with Google'}
        </button>

        <div className="login-divider">or</div>

        <form onSubmit={handleEmailLogin} className="flex flex-col gap-md">
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              className="form-input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              className="form-input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
          <button type="submit" className="btn btn-primary btn-lg w-full" disabled={submitting}>
            {submitting ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <details
          className="mt-md"
          open={staffDocsOpen}
          style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}
        >
          <summary className="cursor-pointer font-semibold" style={{ cursor: 'pointer' }}>
            Administrators &amp; policies / claims
          </summary>
          <div style={{ marginTop: '0.75rem', lineHeight: 1.6 }}>
            <p style={{ marginBottom: '0.75rem' }}>
              <strong>Admin sign-in</strong> uses this same page (Google or email). There is no
              separate URL for passwords. Your account needs a Firestore <code>users</code> record
              with role <code>admin</code> or <code>super_admin</code>.
            </p>
            <p style={{ marginBottom: '0.75rem' }}>
              <strong>Workers:</strong> sign in → register as worker → an admin creates a{' '}
              <strong>policy</strong> for you (Policies → Create) → you open{' '}
              <strong>Trigger claim</strong> when you have an <em>active</em> policy.
            </p>
            <p style={{ marginBottom: 0 }}>
              <strong>Admins:</strong> <strong>Policies</strong> lists and creates coverage for
              workers. <strong>Claims</strong> lists events; workers submit from Trigger claim.
              First super admin: after first Google/email sign-in, use the <strong>Admin / staff</strong>{' '}
              tab if bootstrap is configured, or run <code>seed_admin.py</code>.
            </p>
          </div>
        </details>

        <div className="login-divider">or</div>
        <button type="button" className="btn btn-outline btn-lg w-full" onClick={() => setIsLocalRegistering(true)}>
          Register
        </button>

        <p className="register-toggle text-sm text-muted" style={{ marginBottom: 0, marginTop: '2rem' }}>
          New worker? Sign in above, then complete the worker registration form.
        </p>
      </div>
    </div>
  );
}
