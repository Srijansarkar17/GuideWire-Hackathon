import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { getMyClaims, listClaims, reviewClaim } from '../api/claims';
import DataTable from '../components/ui/DataTable';
import StatusBadge from '../components/ui/StatusBadge';
import Modal from '../components/ui/Modal';
import Loader from '../components/ui/Loader';
import { CheckCircle, XCircle, Eye } from 'lucide-react';
import toast from 'react-hot-toast';

export default function ClaimsPage() {
  const { role } = useAuth();
  const isAdmin = role === 'admin' || role === 'super_admin';
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('');
  const [selectedClaim, setSelectedClaim] = useState(null);
  const [reviewModal, setReviewModal] = useState(null);

  useEffect(() => { fetchClaims(); }, [statusFilter]);

  const fetchClaims = async () => {
    setLoading(true);
    try {
      const res = isAdmin ? await listClaims(statusFilter || null) : await getMyClaims();
      setClaims(res.data.claims || []);
    } catch (err) { console.error(err); }
    setLoading(false);
  };

  const handleReview = async (claimId, action, notes) => {
    try {
      await reviewClaim(claimId, action, notes);
      toast.success(`Claim ${action}d successfully`);
      setReviewModal(null);
      fetchClaims();
    } catch (err) { toast.error(err.response?.data?.detail || 'Review failed'); }
  };

  const columns = [
    { key: 'claim_id', label: 'Claim ID', render: (v) => <span className="font-medium text-primary">{v?.slice(0,16)}</span> },
    ...(isAdmin ? [{ key: 'worker_id', label: 'Worker', render: (v) => <span className="text-sm">{v?.slice(0,12)}...</span> }] : []),
    { key: 'zone', label: 'Zone' },
    { key: 'primary_cause', label: 'Cause', render: (v) => { const i = { weather:'🌧️', traffic:'🚗', social:'📢', combined:'⚡' }; return <span>{i[v]||''} {v||'—'}</span>; } },
    { key: 'payout_amount', label: 'Payout', render: (v) => <span className="font-semibold text-accent">₹{(v||0).toLocaleString('en-IN')}</span> },
    { key: 'confidence', label: 'Confidence' },
    { key: 'fraud_check', label: 'Fraud', render: (v) => v ? <StatusBadge status={v.verdict||'clean'} /> : '—' },
    { key: 'status', label: 'Status', render: (v) => <StatusBadge status={v} /> },
    { key: '_actions', label: '', render: (_, row) => (
      <div className="flex gap-xs">
        <button className="btn btn-ghost btn-sm" onClick={(e) => { e.stopPropagation(); setSelectedClaim(row); }}><Eye size={14} /></button>
        {isAdmin && (row.status==='pending'||row.status==='flagged') && (
          <>
            <button className="btn btn-sm btn-accent" onClick={(e) => { e.stopPropagation(); setReviewModal({...row,action:'approve'}); }}><CheckCircle size={14} /></button>
            <button className="btn btn-sm btn-danger" onClick={(e) => { e.stopPropagation(); setReviewModal({...row,action:'reject'}); }}><XCircle size={14} /></button>
          </>
        )}
      </div>
    )},
  ];

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div><h1>{isAdmin ? 'All Claims' : 'My Claims'}</h1><p className="page-subtitle">{claims.length} claims total</p></div>
      </div>
      <div className="filter-bar">
        <select className="form-select" value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="flagged">Flagged</option>
          <option value="paid">Paid</option>
        </select>
      </div>
      {loading ? <Loader message="Loading claims..." /> : <DataTable columns={columns} data={claims} emptyMessage="No claims found" />}
      {selectedClaim && <ClaimDetailModal claim={selectedClaim} onClose={() => setSelectedClaim(null)} />}
      {reviewModal && <ReviewModal claim={reviewModal} onClose={() => setReviewModal(null)} onSubmit={handleReview} />}
    </div>
  );
}

function ClaimDetailModal({ claim, onClose }) {
  return (
    <Modal isOpen title="Claim Details" onClose={onClose} size="lg">
      <div className="flex flex-col gap-md">
        <div className="flex justify-between items-center">
          <span className="text-sm font-semibold text-primary">{claim.claim_id}</span>
          <StatusBadge status={claim.status} />
        </div>
        <div className="divider" />
        <h4>Disruption Scores</h4>
        {['weather','traffic','social'].map(t => (
          <div className="score-bar" key={t}>
            <span className="score-bar-label">{t}</span>
            <div className="score-bar-track"><div className={`score-bar-fill ${t}`} style={{width:`${(claim[`${t}_score`]||0)*100}%`}} /></div>
            <span className="score-bar-value">{(claim[`${t}_score`]||0).toFixed(2)}</span>
          </div>
        ))}
        <div className="divider" />
        <div className="grid-2">
          <div><div className="text-xs text-muted mb-sm">Primary Cause</div><div className="font-semibold" style={{textTransform:'capitalize'}}>{claim.primary_cause||'—'}</div></div>
          <div><div className="text-xs text-muted mb-sm">Confidence</div><div className="font-semibold">{claim.confidence}</div></div>
          <div><div className="text-xs text-muted mb-sm">Payout</div><div className="font-bold text-accent text-lg">₹{(claim.payout_amount||0).toLocaleString('en-IN')}</div></div>
          <div><div className="text-xs text-muted mb-sm">Intensity</div><div className="font-semibold">{(claim.disruption_intensity||0).toFixed(3)}</div></div>
        </div>
        {claim.fraud_check && (<>
          <div className="divider" />
          <h4>Fraud Analysis</h4>
          <div className="grid-2">
            <div><div className="text-xs text-muted mb-sm">Verdict</div><StatusBadge status={claim.fraud_check.verdict} /></div>
            <div><div className="text-xs text-muted mb-sm">Score</div><div className="font-semibold">{claim.fraud_check.fraud_score?.toFixed(2)}</div></div>
            <div><div className="text-xs text-muted mb-sm">GPS</div><div>{claim.fraud_check.gps_valid?'✅ Valid':'❌ Invalid'}</div></div>
            <div><div className="text-xs text-muted mb-sm">Servers</div><div>{claim.fraud_check.multi_server_agreement?'✅ Yes':'❌ No'}</div></div>
          </div>
          {claim.fraud_check.flags?.length > 0 && <div className="flex flex-col gap-xs">{claim.fraud_check.flags.map((f,i)=><div key={i} className="text-sm text-danger">⚠️ {f}</div>)}</div>}
        </>)}
        {claim.explanation && (<><div className="divider" /><div className="text-xs text-muted mb-sm">Explanation</div><div className="text-sm">{claim.explanation}</div></>)}
      </div>
    </Modal>
  );
}

function ReviewModal({ claim, onClose, onSubmit }) {
  const [notes, setNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const isApprove = claim.action === 'approve';
  const handleSubmit = async () => { setSubmitting(true); await onSubmit(claim.claim_id, claim.action, notes||null); setSubmitting(false); };

  return (
    <Modal isOpen title={`${isApprove?'Approve':'Reject'} Claim`} onClose={onClose}>
      <div className="flex flex-col gap-md">
        <p className="text-sm text-secondary">
          {isApprove ? `Approve claim and authorize ₹${(claim.payout_amount||0).toLocaleString('en-IN')} payout?` : 'Reject this claim?'}
        </p>
        <div className="form-group">
          <label className="form-label">Review Notes</label>
          <textarea className="form-textarea" value={notes} onChange={(e)=>setNotes(e.target.value)} placeholder="Optional notes..." />
        </div>
        <div className="flex gap-md">
          <button className="btn btn-outline" onClick={onClose}>Cancel</button>
          <button className={`btn ${isApprove?'btn-accent':'btn-danger'}`} onClick={handleSubmit} disabled={submitting} style={{flex:1}}>
            {submitting?'Processing...':isApprove?'Approve':'Reject'}
          </button>
        </div>
      </div>
    </Modal>
  );
}
