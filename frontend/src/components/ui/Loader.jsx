import { CloudRain } from 'lucide-react';

export default function Loader({ message = 'Loading...' }) {
  return (
    <div className="loader-wrapper">
      <div className="loader-content">
        <div className="loader-icon">
          <CloudRain size={32} />
        </div>
        <p className="loader-text">{message}</p>
      </div>
      <style>{`
        .loader-wrapper {
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 300px;
          width: 100%;
        }
        .loader-content {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 12px;
        }
        .loader-icon {
          color: var(--primary);
          animation: spin 1.5s linear infinite;
        }
        .loader-text {
          color: var(--text-muted);
          font-size: 0.875rem;
          font-weight: 500;
        }
      `}</style>
    </div>
  );
}

export function InlineLoader() {
  return (
    <span className="inline-loader" style={{
      display: 'inline-block',
      width: 16,
      height: 16,
      border: '2px solid var(--border)',
      borderTopColor: 'var(--primary)',
      borderRadius: '50%',
      animation: 'spin 0.8s linear infinite',
    }} />
  );
}

export function FullPageLoader({ message = 'Loading Drizzle...' }) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      background: 'var(--bg)',
    }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{
          width: 64,
          height: 64,
          background: 'linear-gradient(135deg, var(--primary), var(--primary-light))',
          borderRadius: 16,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 16px',
          animation: 'spin 2s linear infinite',
        }}>
          <CloudRain size={32} color="#fff" />
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>{message}</p>
      </div>
    </div>
  );
}
