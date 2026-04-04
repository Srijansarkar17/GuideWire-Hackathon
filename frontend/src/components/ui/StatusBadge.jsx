export default function StatusBadge({ status, size = 'default' }) {
  const normalized = (status || '').toLowerCase().replace(/\s+/g, '_');

  const sizeClass = size === 'sm' ? 'badge badge-sm' : 'badge';

  return (
    <span className={`${sizeClass} badge-${normalized}`}>
      <span className="badge-dot" style={{
        width: 6,
        height: 6,
        borderRadius: '50%',
        background: 'currentColor',
        opacity: 0.6,
      }} />
      {status}
    </span>
  );
}
