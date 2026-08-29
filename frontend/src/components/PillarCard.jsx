import './PillarCard.css';

function PillarCard({ icon, title, description, status, compliance, accentColor }) {
  return (
    <div className="pillar-card" style={{ '--accent-color': accentColor }}>
      <div className="pillar-top">
        <div className="pillar-icon">{icon}</div>
        <span className={`pillar-status-badge ${status.toLowerCase()}`}>{status}</span>
      </div>
      
      <h3 className="pillar-title">{title}</h3>
      <p className="pillar-description">{description}</p>
      
      <div className="compliance-section">
        <div className="compliance-header">
          <span className="compliance-label">Compliance</span>
          <span className="compliance-percent">{compliance}%</span>
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${compliance}%` }}></div>
        </div>
      </div>

      <div className="pillar-action">
        <span className="action-text">View Details</span>
        <span className="action-arrow">→</span>
      </div>
    </div>
  );
}

export default PillarCard;
