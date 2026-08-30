import React from 'react';
import { useNavigate } from 'react-router-dom';
import ZoneNavigation from './ZoneNavigation';
import TelemetryDrawer from './TelemetryDrawer';
import PortalIntroOverlay from './PortalIntroOverlay';
import UniverseMinimap from './UniverseMinimap';
import { overallScore, pillarData } from '../../data/pillarData';
import './UniverseHUD.css';

export function UniverseHUD({
  activeZone,
  onSelectZone,
  selectedNode,
  onCloseDrawer,
  isWarping,
  onEnterSystem,
  isTouring,
  onToggleTour,
  viewMode,
  onToggleViewMode,
}) {
  const navigate = useNavigate();
  const isPortalIntro = activeZone?.id === 'portal';

  return (
    <div className="universe-hud-root">
      {/* Top Futuristic Navigation Bar */}
      <header className="hud-top-bar">
        {/* Left: Brand Identity */}
        <div className="hud-brand-block">
          <div className="hud-logo-icon">◉</div>
          <div>
            <h1 className="hud-brand-title">GovernX</h1>
            <span className="hud-brand-tag">The Security Universe</span>
          </div>
        </div>

        {/* Center: Quick Pillar Access Bar */}
        <div className="hud-pillar-shortcuts">
          {pillarData.map((p) => (
            <button
              key={p.id}
              type="button"
              className="hud-pillar-btn"
              onClick={() => navigate(p.route)}
              style={{ '--p-color': p.accentColor }}
              title={`View ${p.title} (${p.score}%)`}
              aria-label={`View ${p.title} details`}
            >
              <span className="hud-pillar-icon">{p.icon}</span>
              <span className="hud-pillar-name">{p.name}</span>
              <span className="hud-pillar-score">{p.score}%</span>
            </button>
          ))}
        </div>

        {/* Right: Score Gauge & View Switcher */}
        <div className="hud-right-actions">
          <div className="hud-score-chip">
            <div className="hud-score-value">{overallScore.score}%</div>
            <div className="hud-score-label">NIST CSF 2.0</div>
          </div>

          <button
            type="button"
            className="hud-mode-toggle-btn"
            onClick={onToggleViewMode}
            title="Toggle between 3D Spatial Universe and 2D Executive Matrix"
          >
            {viewMode === '3d' ? '📊 CSF MATRIX' : '🌌 3D UNIVERSE'}
          </button>
        </div>
      </header>

      {/* Spatial Radar Minimap (Desktop) */}
      {!isPortalIntro && (
        <aside className="hud-minimap-container">
          <UniverseMinimap activeZone={activeZone} onSelectZone={onSelectZone} />
        </aside>
      )}

      {/* Bottom Zone Navigation Timeline */}
      {!isPortalIntro && (
        <footer className="hud-bottom-nav">
          <ZoneNavigation
            activeZone={activeZone}
            onSelectZone={onSelectZone}
            isTouring={isTouring}
            onToggleTour={onToggleTour}
          />
        </footer>
      )}

      {/* Intro Portal Overlay with ENTER SYSTEM Trigger */}
      <PortalIntroOverlay
        isVisible={isPortalIntro}
        isWarping={isWarping}
        onEnterSystem={onEnterSystem}
      />

      {/* Interactive Object Telemetry Detail Drawer */}
      <TelemetryDrawer
        selectedNode={selectedNode}
        onClose={onCloseDrawer}
      />
    </div>
  );
}

export default UniverseHUD;
