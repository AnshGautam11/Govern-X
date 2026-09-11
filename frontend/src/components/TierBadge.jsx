import React from 'react';
import './TierBadge.css';

const TIER_LABELS = {
  1: 'Partial',
  2: 'Risk Informed',
  3: 'Repeatable',
  4: 'Adaptive',
};

function TierBadge({ tier, label, tierName, compact = false }) {
  const numericTier = Number.isFinite(Number(tier)) ? Number(tier) : 1;
  const normalizedTier = Math.min(4, Math.max(1, numericTier));
  const displayLabel = label || tierName || TIER_LABELS[normalizedTier] || 'Partial';

  return (
    <span
      className={`tier-badge tier-${normalizedTier} ${compact ? 'compact' : ''}`}
      aria-label={`Tier ${normalizedTier}: ${displayLabel}`}
      title={`Tier ${normalizedTier}: ${displayLabel}`}
    >
      <span className="tier-badge__label">Tier {normalizedTier}</span>
      <span className="tier-badge__name">{displayLabel}</span>
    </span>
  );
}

export default TierBadge;
