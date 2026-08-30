import React from 'react';

export function StatusBadge({ status, tone }) {
  const normalizedTone = (tone || status || 'neutral').toLowerCase().replace(/\s+/g, '-');

  const getToneClass = () => {
    if (normalizedTone.includes('good') || normalizedTone.includes('pass') || normalizedTone.includes('opt') || normalizedTone.includes('excel')) {
      return 'badge-good';
    }
    if (normalizedTone.includes('att') || normalizedTone.includes('warn') || normalizedTone.includes('mod') || normalizedTone.includes('need')) {
      return 'badge-attention';
    }
    if (normalizedTone.includes('crit') || normalizedTone.includes('fail') || normalizedTone.includes('risk')) {
      return 'badge-critical';
    }
    return 'badge-info';
  };

  return (
    <span className={`status-badge-root ${getToneClass()}`}>
      <span className="badge-pulse-dot" />
      <span>{status}</span>
    </span>
  );
}

export default StatusBadge;

