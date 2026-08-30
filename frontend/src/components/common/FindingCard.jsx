import React from 'react';

export function FindingCard({ finding, index }) {
  return (
    <div className="finding-card-item">
      <div className="finding-index-circle">{String(index + 1).padStart(2, '0')}</div>
      <div className="finding-text-block">
        <p className="finding-text">{finding}</p>
        <div className="finding-meta">
          <span className="finding-action-tag">Remediation Task Active</span>
          <span className="finding-status-tag">Priority 1</span>
        </div>
      </div>
    </div>
  );
}

export default FindingCard;

