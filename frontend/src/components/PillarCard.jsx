import React from 'react';
import { Link } from 'react-router-dom';
import './PillarCard.css';

function PillarCard({ icon, title, name, description, status, compliance, controls, accentColor, to }) {
  const badgeClass = status.toLowerCase().replace(/\s+/g, '-');

  return (
    <Link to={to} className="pillar-card-link" aria-label={`View ${title} details`}>
      <article className="pillar-card" style={{ '--accent-color': accentColor }}>
        <div className="pillar-top">
          <div className="pillar-icon">{icon}</div>
          <span className={`pillar-status-badge ${badgeClass}`}>{status}</span>
        </div>

        <div className="pillar-header-block">
          <p className="pillar-kicker">{name}</p>
          <h3 className="pillar-title">{title}</h3>
        </div>

        <p className="pillar-description">{description}</p>

        <div className="compliance-section">
          <div className="compliance-header">
            <span className="compliance-label">Compliance Score</span>
            <span className="compliance-percent">{compliance}%</span>
          </div>
          <div className="progress-bar" aria-label={`${title} compliance ${compliance}%`}>
            <div className="progress-fill" style={{ width: `${compliance}%` }} />
          </div>
        </div>

        <div className="pillar-meta">
          <span>{controls} controls</span>
          <span>Risk posture: {status}</span>
        </div>

        <div className="pillar-action">
          <span className="action-text">View Details</span>
          <span className="action-arrow">→</span>
        </div>
      </article>
    </Link>
  );
}

export default PillarCard;
