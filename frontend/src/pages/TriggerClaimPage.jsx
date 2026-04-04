import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { getMyPolicies } from '../api/policies';
import { triggerClaim } from '../api/claims';
import Loader from '../components/ui/Loader';
import StatusBadge from '../components/ui/StatusBadge';
import { Zap, MapPin, Search, Activity, Navigation } from 'lucide-react';
import toast from 'react-hot-toast';
import { motion, AnimatePresence } from 'framer-motion';

export default function TriggerClaimPage() {
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPolicy, setSelectedPolicy] = useState('');
  const [lat, setLat] = useState('');
  const [lon, setLon] = useState('');
  const [notes, setNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  // Search logic
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    const fetchPolicies = async () => {
      try {
        const res = await getMyPolicies();
        const active = (res.data.policies || []).filter(p => p.status === 'active');
        setPolicies(active);
      } catch (err) { console.error(err); }
      setLoading(false);
    };
    fetchPolicies();
  }, []);

  const handleSearchLocation = async () => {
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    setSearchResults([]);
    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(searchQuery)}&countrycodes=in&format=json&limit=5`);
      const data = await response.json();
      if (data.length === 0) {
        toast.error('No locations found in India for this query');
      } else {
        setSearchResults(data);
      }
    } catch (err) {
      toast.error('Failed to search location');
      console.error(err);
    }
    setIsSearching(false);
  };

  const selectLocation = (result) => {
    setLat(parseFloat(result.lat).toFixed(4));
    setLon(parseFloat(result.lon).toFixed(4));
    setSearchResults([]);
    setSearchQuery(result.display_name); // show picked name
    toast.success('Location set automatically');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setResult(null);
    try {
      const res = await triggerClaim({
        policy_id: selectedPolicy,
        lat: parseFloat(lat),
        lon: parseFloat(lon),
        notes: notes || undefined,
      });
      setResult(res.data);
      toast.success('Claim processed successfully!');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to trigger claim');
    }
    setSubmitting(false);
  };

  if (loading) return <Loader message="Loading policies..." />;

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5, staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 15 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <motion.div 
      variants={containerVariants} 
      initial="hidden" 
      animate="visible" 
      style={{ maxWidth: 760, margin: '0 auto', paddingBottom: '40px' }}
    >
      <motion.div variants={itemVariants} className="page-header" style={{ marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', background: 'linear-gradient(135deg, var(--primary), var(--primary-dark))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Trigger a Claim
          </h1>
          <p className="page-subtitle" style={{ fontSize: '1rem', marginTop: '4px' }}>Real-time disruption analysis powered by AI.</p>
        </div>
      </motion.div>

      {policies.length === 0 ? (
        <motion.div variants={itemVariants} className="card empty-state">
          <Activity size={48} color="var(--text-muted)" />
          <h3 style={{ marginTop: '1rem' }}>No Active Policies</h3>
          <p className="text-sm text-muted">You need an active policy to trigger a claim. Please acquire coverage first.</p>
        </motion.div>
      ) : (
        <motion.div variants={itemVariants} className="card" style={{ padding: '2rem', border: '1px solid var(--border)', borderRadius: '24px', boxShadow: '0 10px 30px -10px rgba(0,0,0,0.05)' }}>
          <form onSubmit={handleSubmit} className="flex flex-col gap-lg">
            <div className="form-group">
              <label className="form-label" style={{ fontWeight: 700, color: 'var(--text)' }}>1. Select Your Coverage</label>
              <select 
                className="form-select" 
                value={selectedPolicy} 
                onChange={(e) => setSelectedPolicy(e.target.value)} 
                required
                style={{ height: '52px', fontSize: '1rem', backgroundColor: '#F8FAFC' }}
              >
                <option value="">Choosing coverage...</option>
                {policies.map(p => (
                  <option key={p.policy_id} value={p.policy_id}>
                    {p.policy_id?.slice(0,16)} — {p.zone} ({p.coverage_type}) — ₹{p.sum_insured?.toLocaleString('en-IN')}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="form-label" style={{ fontWeight: 700, color: 'var(--text)', marginBottom: '12px', display: 'block' }}>2. Search Incident Location</label>
              
              {/* Location Search Bar */}
              <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
                <input 
                  type="text" 
                  className="form-input" 
                  style={{ backgroundColor: '#F8FAFC', flex: 1 }} 
                  placeholder="e.g. Bandra Mumbai, Anna Nagar Chennai..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleSearchLocation(); } }}
                />
                <button 
                  type="button" 
                  className="btn btn-outline" 
                  onClick={handleSearchLocation} 
                  disabled={isSearching}
                  style={{ borderRadius: '12px', flexShrink: 0 }}
                >
                  {isSearching ? <Loader size={16} /> : <Search size={18} />} {isSearching ? '' : 'Search Area'}
                </button>
              </div>

              {/* Search Results Dropdown-like UI */}
              {searchResults.length > 0 && (
                <div style={{ background: '#fff', border: '1px solid var(--border)', borderRadius: '12px', marginBottom: '16px', overflow: 'hidden', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
                  {searchResults.map((res, i) => (
                    <div 
                      key={res.place_id} 
                      onClick={() => selectLocation(res)}
                      style={{ 
                        padding: '12px 16px', 
                        cursor: 'pointer', 
                        borderBottom: i < searchResults.length - 1 ? '1px solid var(--border)' : 'none',
                        transition: 'background 0.2s',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.background = '#F8FAFC'}
                      onMouseLeave={(e) => e.currentTarget.style.background = '#fff'}
                    >
                      <Navigation size={16} color="var(--primary)" style={{ flexShrink: 0 }} />
                      <div className="text-sm" style={{ flex: 1 }}>{res.display_name}</div>
                    </div>
                  ))}
                </div>
              )}

              <div className="grid-2">
                <div className="form-group">
                  <label className="text-xs text-muted mb-xs block">Latitude</label>
                  <input className="form-input" type="number" step="0.0001" value={lat} onChange={(e) => setLat(e.target.value)} placeholder="Lat: e.g. 13.0827" required style={{ backgroundColor: '#F8FAFC' }} />
                </div>
                <div className="form-group">
                  <label className="text-xs text-muted mb-xs block">Longitude</label>
                  <input className="form-input" type="number" step="0.0001" value={lon} onChange={(e) => setLon(e.target.value)} placeholder="Lon: e.g. 80.2707" required style={{ backgroundColor: '#F8FAFC' }} />
                </div>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" style={{ fontWeight: 700, color: 'var(--text)' }}>3. Incident Description (Optional)</label>
              <textarea className="form-textarea" value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Provide any details about the disruption..." style={{ backgroundColor: '#F8FAFC', borderRadius: '16px' }} />
            </div>

            <motion.button 
              whileHover={{ scale: 1.02 }} 
              whileTap={{ scale: 0.98 }}
              type="submit" 
              className="btn btn-primary btn-lg w-full" 
              disabled={submitting || !selectedPolicy}
              style={{ padding: '16px', borderRadius: '16px', fontSize: '1.1rem', marginTop: '1rem', background: submitting ? 'var(--text-muted)' : 'linear-gradient(135deg, var(--primary), var(--primary-light))' }}
            >
              {submitting ? <Loader message="Analyzing Signals..." style={{ color: 'white' }} /> : <span style={{ display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}><Zap size={20} /> Trigger Analysis</span>}
            </motion.button>
          </form>
        </motion.div>
      )}

      {/* Result Section */}
      <AnimatePresence>
        {result && (
          <motion.div 
            initial={{ opacity: 0, height: 0, scale: 0.95 }}
            animate={{ opacity: 1, height: 'auto', scale: 1 }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="card mt-xl"
            style={{ overflow: 'hidden', padding: 0, border: '2px solid var(--primary-lighter)', borderRadius: '24px', boxShadow: '0 20px 40px -15px rgba(37, 99, 235, 0.15)' }}
          >
            <div style={{ background: 'var(--primary-lighter)', padding: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3 style={{ color: 'var(--primary-dark)', fontSize: '1.25rem', marginBottom: '4px' }}>Analysis Complete</h3>
                <div className="text-sm text-primary">ID: {result.claim_id}</div>
              </div>
              <StatusBadge status={result.status} />
            </div>

            <div style={{ padding: '2rem' }}>
              <div className="grid-2 mb-lg" style={{ gap: '2rem' }}>
                <div>
                  <div className="text-sm text-muted mb-xs">Primary Cause Found</div>
                  <div className="font-bold text-lg" style={{ textTransform: 'capitalize' }}>
                    {result.primary_cause === 'weather' ? '🌧️ ' : result.primary_cause === 'traffic' ? '🚗 ' : result.primary_cause === 'social' ? '📢 ' : '⚡ '}{result.primary_cause || '—'}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-muted mb-xs">Confidence Score</div>
                  <div className="font-bold text-lg">{result.confidence || 'HIGH'}</div>
                </div>
              </div>

              <div style={{ background: '#F8FAFC', padding: '1.5rem', borderRadius: '16px', marginBottom: '2rem' }}>
                <h4 className="mb-md" style={{ fontSize: '1rem', color: 'var(--text)' }}>Signal Diagnostics</h4>
                {['weather','traffic','social'].map(t => (
                  <div className="score-bar" key={t} style={{ marginBottom: '16px' }}>
                    <span className="score-bar-label" style={{ textTransform: 'capitalize', width: '70px', fontSize: '0.8125rem' }}>{t}</span>
                    <div className="score-bar-track" style={{ height: '10px', borderRadius: '6px' }}>
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${(result[`${t}_score`]||0)*100}%` }}
                        transition={{ duration: 1.2, ease: "easeOut", delay: 0.2 }}
                        className={`score-bar-fill ${t}`} 
                        style={{ height: '10px', borderRadius: '6px' }}
                      />
                    </div>
                    <span className="score-bar-value" style={{ fontSize: '0.8125rem', fontWeight: 800 }}>{(result[`${t}_score`]||0).toFixed(2)}</span>
                  </div>
                ))}
              </div>

              <div className="flex justify-between items-center" style={{ padding: '1rem 0', borderTop: '1px dashed var(--border)', borderBottom: '1px dashed var(--border)' }}>
                <div>
                  <div className="text-sm text-muted">Authorized Payout</div>
                  <div className="font-bold" style={{ fontSize: '2rem', color: 'var(--accent)', lineHeight: 1 }}>₹{(result.payout_amount||0).toLocaleString('en-IN')}</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div className="text-sm text-muted mb-xs">Fraud Verification</div>
                  {result.fraud_check && <StatusBadge status={result.fraud_check.verdict||'clean'} />}
                </div>
              </div>

              {result.explanation && (
                <div className="mt-md" style={{ padding: '1rem', background: 'var(--info-lighter)', borderRadius: '12px' }}>
                  <div className="text-xs font-bold text-info mb-xs" style={{ textTransform: 'uppercase' }}>Automated Verdict</div>
                  <div className="text-sm" style={{ color: 'var(--text-secondary)' }}>{result.explanation}</div>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
