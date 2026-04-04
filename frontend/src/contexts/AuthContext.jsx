import { createContext, useContext, useState, useEffect } from 'react';
import {
  onAuthStateChanged,
  signInWithPopup,
  signInWithEmailAndPassword,
  GoogleAuthProvider,
  signOut as firebaseSignOut,
} from 'firebase/auth';
import { auth } from '../firebase';
import { getMe } from '../api/auth';

const AuthContext = createContext(null);

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}

export function AuthProvider({ children }) {
  const [firebaseUser, setFirebaseUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Listen for Firebase auth state
  useEffect(() => {
    // Check if local user exists FIRST
    const localUserStr = localStorage.getItem('drizzle_local_user');
    if (localUserStr) {
      try {
        const localUser = JSON.parse(localUserStr);
        setProfile(localUser);
        setFirebaseUser({ isLocal: true, uid: localUser.uid });
        setLoading(false);
        return;
      } catch (e) {
        console.warn('Failed to parse local user', e);
        localStorage.removeItem('drizzle_local_user');
      }
    }

    // Timeout fallback — if Firebase never fires onAuthStateChanged, stop loading
    const timeout = setTimeout(() => {
      setLoading(false);
    }, 3000);

    let unsub;
    try {
      unsub = onAuthStateChanged(auth, async (fbUser) => {
        clearTimeout(timeout);
        setFirebaseUser(fbUser);
        if (fbUser) {
          try {
            const res = await getMe();
            setProfile(res.data);
            setError(null);
          } catch (err) {
            // User is authenticated in Firebase but has no backend / Firestore profile yet
            // (401/403/404) — normal for new users who must complete registration
            setProfile(null);
            const s = err.response?.status;
            if (s !== 401 && s !== 403 && s !== 404) {
              console.warn('Failed to fetch profile:', err);
            }
          }
        } else {
          setProfile(null);
        }
        setLoading(false);
      });
    } catch (err) {
      console.warn('Firebase auth init error:', err);
      clearTimeout(timeout);
      setLoading(false);
    }

    return () => {
      clearTimeout(timeout);
      if (unsub) unsub();
    };
  }, []);

  const loginWithGoogle = async () => {
    setError(null);
    try {
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(auth, provider);
      // Profile will be fetched by the onAuthStateChanged listener
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const loginWithEmail = async (email, password) => {
    setError(null);
    try {
      const result = await signInWithEmailAndPassword(auth, email, password);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const logout = async () => {
    if (firebaseUser?.isLocal) {
      localStorage.removeItem('drizzle_local_user');
      setProfile(null);
      setFirebaseUser(null);
      return;
    }
    await firebaseSignOut(auth);
    setProfile(null);
    setFirebaseUser(null);
  };

  const localRegister = (userData) => {
    const localUser = {
      uid: 'usr_' + Date.now(),
      email: userData.email || 'worker@example.com',
      display_name: userData.display_name,
      role: 'worker', 
      zone: userData.zone,
      vehicle_type: userData.vehicle_type,
      phone: userData.phone || '0000000000',
      is_local: true
    };
    localStorage.setItem('drizzle_local_user', JSON.stringify(localUser));
    setProfile(localUser);
    setFirebaseUser({ isLocal: true, uid: localUser.uid });
    setError(null);
  };

  const refreshProfile = async () => {
    if (firebaseUser?.isLocal) return;
    try {
      const res = await getMe();
      setProfile(res.data);
    } catch {
      // Ignore
    }
  };

  const value = {
    firebaseUser,
    user: profile,
    role: profile?.role || null,
    loading,
    error,
    isAuthenticated: !!firebaseUser,
    hasProfile: !!profile,
    loginWithGoogle,
    loginWithEmail,
    logout,
    refreshProfile,
    setError,
    localRegister,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
