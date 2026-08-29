import './Dashboard.css';
import PillarCard from './PillarCard';
import TypingEffect from './TypingEffect';
import TerminalMessages from './TerminalMessages';

function Dashboard() {
  const pillars = [
    {
      id: 1,
      icon: '⚙️',
      title: 'Govern',
      description: 'Establish and monitor cybersecurity strategy, policies, roles, and responsibilities.',
      status: 'Active',
      compliance: 92,
      accentColor: '#00ff41'
    },
    {
      id: 2,
      icon: '🔎',
      title: 'Identify',
      description: 'Understand cybersecurity risks, assets, systems, and organizational context.',
      status: 'Compliant',
      compliance: 85,
      accentColor: '#00d4ff'
    },
    {
      id: 3,
      icon: '🔐',
      title: 'Protect',
      description: 'Implement safeguards to ensure delivery of critical services.',
      status: 'Compliant',
      compliance: 88,
      accentColor: '#26d946'
    },
    {
      id: 4,
      icon: '⚠️',
      title: 'Detect',
      description: 'Identify and analyze possible cybersecurity attacks and compromises.',
      status: 'Review',
      compliance: 72,
      accentColor: '#b366ff'
    },
    {
      id: 5,
      icon: '⚡',
      title: 'Respond',
      description: 'Take action regarding detected cybersecurity incidents.',
      status: 'Partial',
      compliance: 68,
      accentColor: '#ff9500'
    },
    {
      id: 6,
      icon: '🔄',
      title: 'Recover',
      description: 'Restore affected assets and operations after a cybersecurity incident.',
      status: 'Partial',
      compliance: 65,
      accentColor: '#ff3b30'
    }
  ];

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="hero-section">
          <h1 className="dashboard-title">
            <TypingEffect text="GOVERNX" speed={80} />
          </h1>
          <p className="dashboard-subtitle">
            Automated NIST CSF 2.0 Compliance Engine
          </p>
          
          <div className="status-line">
            <span className="status-item">● SYSTEM STATUS: SECURE</span>
            <span className="status-separator">|</span>
            <span className="status-item">● COMPLIANCE ENGINE: ONLINE</span>
            <span className="status-separator">|</span>
            <span className="status-item">● LAST SCAN: 2 MINUTES AGO</span>
          </div>
        </div>

        <TerminalMessages />
      </div>

      <div className="compliance-overview">
        <div className="metric">
          <div className="metric-value">78%</div>
          <div className="metric-label">Overall Compliance</div>
        </div>
        <div className="metric">
          <div className="metric-value">124</div>
          <div className="metric-label">Controls Assessed</div>
        </div>
        <div className="metric">
          <div className="metric-value">97</div>
          <div className="metric-label">Controls Compliant</div>
        </div>
        <div className="metric">
          <div className="metric-value">27</div>
          <div className="metric-label">Open Findings</div>
        </div>
      </div>
      
      <div className="pillars-grid">
        {pillars.map((pillar) => (
          <PillarCard
            key={pillar.id}
            icon={pillar.icon}
            title={pillar.title}
            description={pillar.description}
            status={pillar.status}
            compliance={pillar.compliance}
            accentColor={pillar.accentColor}
          />
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
