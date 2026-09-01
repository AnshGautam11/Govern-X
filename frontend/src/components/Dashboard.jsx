import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, AlertTriangle, ArrowUpRight, CheckCircle2, Clock3, RefreshCw } from 'lucide-react';
import UniverseCanvas from './3d/UniverseCanvas';
import UniverseHUD from './hud/UniverseHUD';
import PillarCard from './PillarCard';
import TypingEffect from './TypingEffect';
import TerminalMessages from './TerminalMessages';
import { overallScore, pillarData } from '../data/pillarData';
import { UNIVERSE_ZONES } from '../data/universeData';
import './Dashboard.css';

export function Dashboard() {
  const navigate = useNavigate();
  const [activeZoneId, setActiveZoneId] = useState('portal');
  const [selectedNode, setSelectedNode] = useState(null);
  const [isWarping, setIsWarping] = useState(false);
  const [isTouring, setIsTouring] = useState(false);
  const [viewMode, setViewMode] = useState('3d'); // '3d' | 'matrix'
  const [assessmentState, setAssessmentState] = useState('ready');

  const activeZone = useMemo(
    () => UNIVERSE_ZONES.find((z) => z.id === activeZoneId) || UNIVERSE_ZONES[0],
    [activeZoneId]
  );

  const handleSelectZone = (zoneId) => {
    setActiveZoneId(zoneId);
    setSelectedNode(null);
    const targetZone = UNIVERSE_ZONES.find((z) => z.id === zoneId);
    if (targetZone?.route && targetZone.route !== '/') {
      navigate(targetZone.route);
    }
  };

  const handleEnterSystem = () => {
    setIsWarping(true);
  };

  const handleWarpComplete = () => {
    setIsWarping(false);
    setActiveZoneId('govern');
  };

  const handleAssessment = () => {
    setAssessmentState('queued');
    window.setTimeout(() => setAssessmentState('ready'), 2400);
  };

  const attentionPillars = pillarData
    .filter((pillar) => pillar.status !== 'Excellent')
    .sort((first, second) => first.score - second.score)
    .slice(0, 3);

  return (
    <div className="dashboard-container">
      {/* 3D Security Universe Spatial Canvas */}
      <div className="universe-canvas-wrapper">
        <UniverseCanvas
          activeZone={activeZone}
          selectedNode={selectedNode}
          isWarping={isWarping}
          onWarpComplete={handleWarpComplete}
          onSelectNode={setSelectedNode}
          onSelectZone={handleSelectZone}
        />

        {/* Futuristic Glassmorphic HUD */}
        <UniverseHUD
          activeZone={activeZone}
          onSelectZone={handleSelectZone}
          selectedNode={selectedNode}
          onCloseDrawer={() => setSelectedNode(null)}
          isWarping={isWarping}
          onEnterSystem={handleEnterSystem}
          isTouring={isTouring}
          onToggleTour={() => setIsTouring((prev) => !prev)}
          viewMode={viewMode}
          onToggleViewMode={() => setViewMode((prev) => (prev === '3d' ? 'matrix' : '3d'))}
        />
      </div>

      {/* Accessible NIST CSF 2.0 Compliance Matrix & Executive Dashboard View */}
      <section
        className="executive-csf-section"
        aria-label="NIST CSF 2.0 Compliance Overview"
      >
        <div className="dashboard-shell">
          <header className="dashboard-header">
            <div className="hero-section">
              <div className="eyebrow">Cybersecurity Governance Platform</div>
              <h1 className="dashboard-title">
                <TypingEffect text="GovernX" speed={80} />
              </h1>
              <p className="dashboard-subtitle">NIST CSF 2.0 Compliance Overview</p>
              <div className="status-line">
                <span className="status-item">● System Status: Secure</span>
                <span className="status-separator">|</span>
                <span className="status-item">● Control Engine: Online</span>
                <span className="status-separator">|</span>
                <span className="status-item">● Last Assessment: {overallScore.lastAssessment}</span>
              </div>
            </div>
            <TerminalMessages />
          </header>

          <div className="dashboard-command-bar" aria-label="Dashboard actions">
            <div className="command-context">
              <span className="command-pulse" aria-hidden="true" />
              <div>
                <span className="command-label">Live assessment workspace</span>
                <strong>Production posture / AWS organization</strong>
              </div>
            </div>
            <div className="command-actions">
              <span className="assessment-time"><Clock3 size={14} /> Updated {overallScore.lastAssessment}</span>
              <button type="button" className="assessment-button" onClick={handleAssessment}>
                <RefreshCw size={15} className={assessmentState === 'queued' ? 'is-spinning' : ''} />
                {assessmentState === 'queued' ? 'Assessment queued' : 'Run assessment'}
              </button>
            </div>
          </div>

          <section className="overview-panel">
            <div className="overview-topline">
              <span className="overview-label">Executive Summary</span>
              <span className={`overview-status ${overallScore.statusTone}`}>{overallScore.status}</span>
            </div>

            <div className="overview-grid">
              <div className="score-visual">
                <div className="score-ring" style={{ '--score': `${overallScore.score}` }}>
                  <div className="score-ring-inner">
                    <strong>{overallScore.score}%</strong>
                    <span>Secure</span>
                  </div>
                </div>
              </div>

              <div className="overview-metrics">
                <div className="overview-metric primary">
                  <span className="metric-label">Overall Compliance Score</span>
                  <strong>{overallScore.score}%</strong>
                </div>
                <div className="overview-metric">
                  <span className="metric-label">Security Posture</span>
                  <strong>{overallScore.securityPosture}</strong>
                </div>
                <div className="overview-metric">
                  <span className="metric-label">Controls Assessed</span>
                  <strong>{overallScore.controlsAssessed}</strong>
                </div>
                <div className="overview-metric">
                  <span className="metric-label">Controls Passed</span>
                  <strong>{overallScore.controlsPassed}</strong>
                </div>
                <div className="overview-metric">
                  <span className="metric-label">Require Attention</span>
                  <strong>{overallScore.controlsAttention}</strong>
                </div>
                <div className="overview-metric">
                  <span className="metric-label">Last Assessment</span>
                  <strong>{overallScore.lastAssessment}</strong>
                </div>
              </div>
            </div>
          </section>

          <section className="dashboard-insights" aria-label="Assessment insights">
            <article className="trend-panel">
              <div className="insight-heading">
                <div>
                  <span className="overview-label">Posture trajectory</span>
                  <h2>Compliance is trending upward</h2>
                </div>
                <span className="trend-chip"><Activity size={14} /> +6.2% / 90 days</span>
              </div>
              <div className="trend-chart" role="img" aria-label="Compliance score increased from 71 percent to 78 percent over the last 90 days">
                <div className="chart-gridline gridline-top"><span>80</span></div>
                <div className="chart-gridline gridline-mid"><span>75</span></div>
                <div className="chart-gridline gridline-bottom"><span>70</span></div>
                <svg viewBox="0 0 620 180" preserveAspectRatio="none" aria-hidden="true">
                  <defs>
                    <linearGradient id="trend-fill" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.28" />
                      <stop offset="100%" stopColor="#38bdf8" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                  <path className="trend-area" d="M0 142 C75 136 98 118 158 126 S248 112 306 96 S397 101 458 67 S540 75 620 42 L620 180 L0 180 Z" />
                  <path className="trend-line" d="M0 142 C75 136 98 118 158 126 S248 112 306 96 S397 101 458 67 S540 75 620 42" />
                  <circle cx="620" cy="42" r="5" className="trend-point" />
                </svg>
                <div className="chart-labels"><span>Jun 03</span><span>Jun 24</span><span>Jul 15</span><span>Aug 05</span><span>Sep 01</span></div>
              </div>
            </article>

            <article className="attention-panel">
              <div className="insight-heading">
                <div>
                  <span className="overview-label">Priority queue</span>
                  <h2>Needs attention</h2>
                </div>
                <span className="attention-count">{overallScore.controlsAttention} controls</span>
              </div>
              <div className="attention-list">
                {attentionPillars.map((pillar) => (
                  <button key={pillar.id} type="button" className="attention-item" onClick={() => handleSelectZone(pillar.slug)}>
                    <span className="attention-icon"><AlertTriangle size={15} /></span>
                    <span className="attention-copy"><strong>{pillar.title} controls</strong><small>{pillar.status} posture / {pillar.controls} controls</small></span>
                    <span className="attention-score">{pillar.score}% <ArrowUpRight size={15} /></span>
                  </button>
                ))}
              </div>
              <button type="button" className="queue-link" onClick={() => handleSelectZone('respond')}><CheckCircle2 size={15} /> Review all findings</button>
            </article>
          </section>

          {/* Universe Fast Jump Links */}
          <div className="universe-fast-jump-strip">
            {UNIVERSE_ZONES.map((zone) => (
              <button
                key={zone.id}
                type="button"
                className="zone-node-button"
                aria-label={`Open ${zone.name} zone`}
                onClick={() => handleSelectZone(zone.id)}
              >
                {zone.name}
              </button>
            ))}
          </div>

          {/* Six Pillar Cards Grid */}
          <section className="pillars-grid" aria-label="NIST CSF Pillars">
            {pillarData.map((pillar) => (
              <PillarCard
                key={pillar.id}
                icon={pillar.icon}
                title={pillar.title}
                name={pillar.name}
                description={pillar.description}
                status={pillar.status}
                compliance={pillar.score}
                controls={pillar.controls}
                accentColor={pillar.accentColor}
                to={pillar.route}
              />
            ))}
          </section>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
