import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
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
