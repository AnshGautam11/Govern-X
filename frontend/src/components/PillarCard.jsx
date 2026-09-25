import React from 'react';
import { Link } from 'react-router-dom';
import TierBadge from './TierBadge';
import './PillarCard.css';

function PillarCard({
  icon,
  title,
  name,
  description,
  status,
  compliance,
  controls,
  accentColor,
  to,
  tier,
  tierName,
  trend,
  percentage,
}) {
  const hasScore = percentage != null || compliance != null;
  const score = Number.isFinite(Number(percentage ?? compliance)) ? Number(percentage ?? compliance) : null;
  const displayTier = typeof tier === 'number' ? tier : score == null ? null : Math.min(4, Math.max(1, Math.ceil(score / 25) || 1));
  const displayTierName = tierName || (displayTier == null ? 'No Data' : displayTier === 1 ? 'Partial' : displayTier === 2 ? 'Risk Informed' : displayTier === 3 ? 'Repeatable' : 'Adaptive');
  const badgeClass = status ? status.toLowerCase().replace(/\s+/g, '-') : `tier-${displayTier}`;
  const trendValue = Number.isFinite(Number(trend)) ? Number(trend) : 0;
  const trendText = `${trendValue >= 0 ? '↑' : '↓'} ${Math.abs(trendValue)}%`;

  const cardContent = (
    <article className="pillar-card" style={{ '--accent-color': accentColor }}>
      <div className="pillar-top">
        <div className="pillar-icon">{icon}</div>
        {displayTier == null ? <span className="tier-badge">No Data</span> : <TierBadge tier={displayTier} tierName={displayTierName} compact />}
      </div>

      <div className="pillar-header-block">
        <p className="pillar-kicker">{name}</p>
        <h3 className="pillar-title">{title}</h3>
      </div>

      <p className="pillar-description">{description}</p>

      <div className="compliance-section">
        <div className="compliance-header">
          <span className="compliance-label">Maturity</span>
          <span className="compliance-percent">{hasScore ? `${score.toFixed(0)}%` : 'N/A'}</span>
        </div>
        <div className="progress-bar" aria-label={`${title} maturity ${score}%`}>
          <div className="progress-fill" style={{ width: `${score == null ? 0 : Math.min(100, Math.max(0, score))}%` }} />
        </div>
      </div>

      <div className="pillar-meta">
        <span>{controls ?? 'Live'} data</span>
        <span className="pillar-trend">{trendText}</span>
      </div>

      <div className="pillar-action">
        <span className="action-text">{status || 'Live data'}</span>
        <span className="action-arrow">→</span>
      </div>
    </article>
  );

  if (!to) {
    return cardContent;
  }

  return (
    <Link to={to} className="pillar-card-link" aria-label={`View ${title} details`}>
      {cardContent}
    </Link>
  );
}

export default PillarCard;
