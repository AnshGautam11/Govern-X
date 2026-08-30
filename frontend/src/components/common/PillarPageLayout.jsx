import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { pillarData } from '../../data/pillarData';
import StatusBadge from './StatusBadge';
import ComplianceGauge from './ComplianceGauge';
import Pillar3DVisualizer from './Pillar3DVisualizer';

export function PillarPageLayout({ pillar, children }) {
  const navigate = useNavigate();

  if (!pillar) return null;

  return (
    <div className="pillar-universe-page">
      {/* Background Cyber Glow Effect */}
      <div
        className="pillar-bg-glow"
        style={{
          '--glow-color': pillar.accentColor,
        }}
      />

      <div className="pillar-page-shell">
        {/* Top Universe Breadcrumb & Return Action */}
        <header className="pillar-page-top-bar">
          <div className="pillar-brand-group">
            <Link to="/" className="pillar-universe-link">
              <span className="brand-dot">◉</span>
              <span className="brand-name">GovernX</span>
              <span className="brand-sub">Security Universe</span>
            </Link>
            <span className="breadcrumb-separator">/</span>
            <span className="current-pillar-crumb" style={{ color: pillar.accentColor }}>
              {pillar.name} ({pillar.code})
            </span>
          </div>

          <Link to="/" className="back-to-universe-button" aria-label="Return to 3D Universe">
            <span className="back-arrow">←</span>
            <span>Return to Universe</span>
          </Link>
        </header>

        {/* Six Pillar Navigation Switcher Bar */}
        <nav className="pillar-nav-switcher" aria-label="NIST CSF Pillars Switcher">
          {pillarData.map((item) => {
            const isActive = item.slug === pillar.slug;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => navigate(item.route)}
                className={`pillar-switcher-tab ${isActive ? 'is-active' : ''}`}
                style={{
                  '--pillar-accent': item.accentColor,
                }}
                aria-label={`Switch to ${item.title} pillar`}
              >
                <span className="switcher-icon">{item.icon}</span>
                <div className="switcher-text-block">
                  <span className="switcher-name">{item.name}</span>
                  <span className="switcher-score">{item.score}%</span>
                </div>
              </button>
            );
          })}
        </nav>

        {/* Hero Section */}
        <section className="pillar-hero-banner" style={{ borderColor: `${pillar.accentColor}33` }}>
          <div className="hero-left-content">
            <div className="hero-eyebrow-row">
              <span className="hero-kicker-tag" style={{ color: pillar.accentColor, borderColor: `${pillar.accentColor}44` }}>
                NIST CSF 2.0 • {pillar.code}
              </span>
              <span className="hero-theme-tag">Spatial Zone: {pillar.themeName}</span>
              <StatusBadge status={pillar.status} tone={pillar.badgeTone} />
            </div>

            <h1 className="pillar-hero-title">
              <span className="pillar-icon-large">{pillar.icon}</span> {pillar.title}
            </h1>
            <p className="pillar-hero-desc">{pillar.detail || pillar.description}</p>

            {/* Quick Metrics Strip */}
            {pillar.metrics && (
              <div className="pillar-metrics-strip">
                {pillar.metrics.map((m, idx) => (
                  <div key={idx} className="metric-chip">
                    <span className="metric-chip-label">{m.label}</span>
                    <strong className="metric-chip-value" style={{ color: pillar.accentColor }}>{m.value}</strong>
                    <span className="metric-chip-sub">{m.sub}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="hero-right-gauge">
            <ComplianceGauge
              score={pillar.score}
              accentColor={pillar.accentColor}
              size={130}
              label="Compliance"
            />
            <div className="gauge-summary-text">
              <strong>{pillar.controls} Assessed</strong>
              <span>{pillar.requirements} Requirements</span>
            </div>
          </div>
        </section>

        {/* Interactive 3D Zone Mini-Visualizer */}
        <section className="pillar-visualizer-section">
          <Pillar3DVisualizer pillarSlug={pillar.slug} />
        </section>

        {/* Domain-Specific Content Sections */}
        <main className="pillar-content-body">
          {children}
        </main>
      </div>
    </div>
  );
}

export default PillarPageLayout;

