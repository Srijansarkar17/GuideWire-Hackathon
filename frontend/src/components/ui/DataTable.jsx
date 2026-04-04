import { PackageOpen } from 'lucide-react';

export default function DataTable({ columns, data, emptyMessage = 'No data found', onRowClick }) {
  if (!data || data.length === 0) {
    return (
      <div className="empty-state">
        <PackageOpen size={48} />
        <h3>{emptyMessage}</h3>
        <p className="text-sm text-muted">Results will appear here once data is available.</p>
      </div>
    );
  }

  return (
    <div className="table-container">
      <table className="table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key} style={col.width ? { width: col.width } : {}}>
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr
              key={row.id || row.uid || row.policy_id || row.claim_id || i}
              onClick={() => onRowClick?.(row)}
              style={onRowClick ? { cursor: 'pointer' } : {}}
            >
              {columns.map((col) => (
                <td key={col.key}>
                  {col.render ? col.render(row[col.key], row) : row[col.key] || '—'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
