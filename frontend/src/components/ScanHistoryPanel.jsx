import { useEffect, useState } from 'react';
import { fetchScanHistory } from '../lib/api';
import './ScanHistoryPanel.css';

export default function ScanHistoryPanel({ limit = 20 }) {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchScanHistory(limit);
        if (!cancelled) {
          setEntries(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError('Unable to load scan history.');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [limit]);

  if (loading) {
    return <div className="scan-history-panel scan-history-loading">Loading scan history...</div>;
  }

  if (error) {
    return <div className="scan-history-panel scan-history-error">{error}</div>;
  }

  if (entries.length === 0) {
    return <div className="scan-history-panel scan-history-empty">No scan history yet.</div>;
  }

  return (
    <div className="scan-history-panel">
      <h3 className="scan-history-title">Recent Scan History</h3>
      <table className="scan-history-table">
        <thead>
          <tr>
            <th>Check</th>
            <th>Resource</th>
            <th>Status</th>
            <th>When</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry) => (
            <tr key={entry.id} className={`scan-history-row status-${entry.status}`}>
                            <td>{entry.check_id}</td>
              <td>{entry.resource_id}</td>
              <td>{entry.status.toUpperCase()}</td>
              <td>{new Date(entry.scanned_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
