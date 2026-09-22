import React, { useEffect, useState } from 'react';
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
          // API may return an array or an object containing the history.
          const history = Array.isArray(data)
            ? data
            : Array.isArray(data?.entries)
              ? data.entries
              : Array.isArray(data?.history)
                ? data.history
                : Array.isArray(data?.items)
                  ? data.items
                  : [];

          setEntries(history);
        }
      } catch (err) {
        console.error('Failed to load scan history:', err);

        if (!cancelled) {
          setError('Unable to load scan history.');
          setEntries([]);
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
    return (
      <div className="scan-history-panel scan-history-loading">
        Loading scan history...
      </div>
    );
  }

  if (error) {
    return (
      <div className="scan-history-panel scan-history-error">
        {error}
      </div>
    );
  }

  if (entries.length === 0) {
    return (
      <div className="scan-history-panel scan-history-empty">
        No scan history yet.
      </div>
    );
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
          {entries.map((entry, index) => (
            <tr
              key={entry.id ?? `${entry.check_id ?? 'scan'}-${index}`}
              className={`scan-history-row status-${entry.status ?? 'unknown'}`}
            >
              <td>{entry.check_id ?? '—'}</td>

              <td>{entry.resource_id ?? '—'}</td>

              <td>
                {(entry.status ?? 'unknown').toUpperCase()}
              </td>

              <td>
                {entry.scanned_at
                  ? new Date(entry.scanned_at).toLocaleString()
                  : '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}