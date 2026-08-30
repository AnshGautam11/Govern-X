import React from 'react';
import StatusBadge from './StatusBadge';

export function ControlCard({ code, title, status, evidence }) {
  return (
    <div className="control-card-item">
      <div className="control-card-top">
        <span className="control-card-code">{code}</span>
        <StatusBadge status={status} />
      </div>
      <h4 className="control-card-title">{title}</h4>
      {evidence && (
        <div className="control-card-evidence">
          <span className="evidence-label">Audited Evidence:</span>
          <span className="evidence-value">{evidence}</span>
        </div>
      )}
    </div>
  );
}

export default ControlCard;

