import React, { useState, useMemo, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, AlertTriangle, ArrowUpRight, CheckCircle2, Clock3, RefreshCw, Wifi, WifiOff } from 'lucide-react';
import UniverseCanvas from './3d/UniverseCanvas';
import UniverseHUD from './hud/UniverseHUD';
import PillarCard from './PillarCard';
import TypingEffect from './TypingEffect';
import TerminalMessages from './TerminalMessages';
import { UNIVERSE_ZONES } from '../data/universeData';
import { fetchMaturityData, triggerAssessmentScan } from '../lib/api';
import './Dashboard.css';

const FUNCTIONS = [
  { key: 'Govern', title: 'Govern', name: 'GOVERN', icon: '🛡️', route: '/govern', accentColor: '#34d399' },
  { key: 'Identify', title: 'Identify', name: 'IDENTIFY', icon: '🔎', route: '/identify', accentColor: '#38bdf8' },
  { key: 'Protect', title: 'Protect', name: 'PROTECT', icon: '🔐', route: '/protect', accentColor: '#10b981' },
  { key: 'Detect', title: 'Detect', name: 'DETECT', icon: '📡', route: '/detect', accentColor: '#a78bfa' },
  { key: 'Respond', title: 'Respond', name: 'RESPOND', icon: '⚡', route: '/respond', accentColor: '#f87171' },
  { key: 'Recover', title: 'Recover', name: 'RECOVER', icon: '♻️', route: '/recover', accentColor: '#fbbf24' },
];

const toTierStatus = (tier) => {
  if (tier === 1) return 'Partial';
  if (tier === 2) return 'Risk Informed';
  if (tier === 3) return 'Repeatable';
  if (tier === 4) return 'Adaptive';
  return 'No Data';
};

const DEFAULT_OVERALL = {
  percentage: 78,
  tier: 3,
  tier_name: 'Repeatable',
  trend: 5,
  status: 'Good',
};

const DEFAULT_PILLAR_VALUES = {
  Govern: { percentage: 82, tier: 3, tier_name: 'Repeatable', trend: 4, status: 'Good' },
  Identify: { percentage: 76, tier: 3, tier_name: 'Repeatable', trend: 2, status: 'Risk informed' },
  Protect: { percentage: 88, tier: 4, tier_name: 'Adaptive', trend: 7, status: 'Adaptive' },
  Detect: { percentage: 71, tier: 3, tier_name: 'Repeatable', trend: 1, status: 'Repeatable' },
  Respond: { percentage: 68, tier: 2, tier_name: 'Risk Informed', trend: -2, status: 'Risk informed' },
  Recover: { percentage: 79, tier: 3, tier_name: 'Repeatable', trend: 3, status: 'Good' },
};

export function Dashboard() {
  const navigate = useNavigate();
  const [activeZoneId, setActiveZoneId] = useState('portal');
  const [selectedNode, setSelectedNode] = useState(null);
  const [isWarping, setIsWarping] = useState(false);
  const [isTouring, setIsTouring] = useState(false);
  const [viewMode, setViewMode] = useState('3d');
  const [assessmentState, setAssessmentState] = useState('ready');
  const [maturityData, setMaturityData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isLive, setIsLive] = useState(false);

  const activeZone = useMemo(
    () => UNIVERSE_ZONES.find((z) => z.id === activeZoneId) || UNIVERSE_ZONES[0],
    [activeZoneId]
  );

  const loadMaturityData = async () => {
    setLoading(true);
    setError('');
    try {
      const payload = await fetchMaturityData();
      setMaturityData(payload);
      setIsLive(true);
    } catch (fetchError) {
      setError(fetchError.message || 'Unable to retrieve live maturity data.');
      setIsLive(false);
      setMaturityData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMaturityData();
  }, []);

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

  const handleAssessment = async () => {
    setAssessmentState('queued');
    try {
      await triggerAssessmentScan();
      await loadMaturityData();
    } catch (scanError) {
      setError(scanError.message || 'Backend scan failed.');
      setIsLive(false);
    } finally {
      window.setTimeout(() => setAssessmentState('ready'), 1200);
    }
  };

  const overall = maturityData?.overall || DEFAULT_OVERALL;
  const pillars = maturityData?.pillars?.length ? maturityData.pillars : Object.entries(DEFAULT_PILLAR_VALUES).map(([functionName, value]) => ({
    function: functionName,
    ...value,
  }));
  const overallStatus = overall.status || toTierStatus(overall.tier);
  const attentionPillars = pillars
    .filter((pillar) => (pillar.percentage ?? 0) < 80)
    .sort((first, second) => (first.percentage ?? 0) - (second.percentage ?? 0))
    .slice(0, 3);

  return (
    <div className="dashboard-container">
      <div className="universe-canvas-wrapper">
        <UniverseCanvas
          activeZone={activeZone}
          selectedNode={selectedNode}
          isWarping={isWarping}
          onWarpComplete={handleWarpComplete}
          onSelectNode={setSelectedNode}
          onSelectZone={handleSelectZone}
        />

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

      <section className="executive-csf-section" aria-label="NIST CSF 2.0 Compliance Overview">
        <div className="dashboard-shell">
          <header className="dashboard-header">
            <div className="hero-section">
              <div className="eyebrow">Cybersecurity Governance Platform</div>
              <h1 className="dashboard-title">
                <TypingEffect text="GovernX" speed={80} />
              </h1>
              <p className="dashboard-subtitle">NIST CSF 2.0 Compliance Overview</p>
              <div className="status-line">
                <span className={`status-item ${isLive ? 'live' : 'offline'}`}>
                  {isLive ? <Wifi size={12} /> : <WifiOff size={12} />} {isLive ? 'Live API' : 'API Offline'}
                </span>
                <span className="status-separator">|</span>
                <span className="status-item">● Control Engine: {isLive ? 'Online' : 'Unavailable'}</span>
                <span className="status-separator">|</span>
                <span className="status-item">● Last Assessment: {loading ? 'Loading...' : 'Updated live'}</span>
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
              <span className="assessment-time"><Clock3 size={14} /> {loading ? 'Loading maturity data...' : 'Updated live'}</span>
              <button type="button" className="assessment-button" onClick={handleAssessment}>
                <RefreshCw size={15} className={assessmentState === 'queued' ? 'is-spinning' : ''} />
                {assessmentState === 'queued' ? 'Assessment queued' : 'Run assessment'}
              </button>
            </div>
          </div>

          {error && (
            <div className="dashboard-error" role="alert">
              <h3>BACKEND CONNECTION ERROR</h3>
              <p>{error}</p>
              <button type="button" className="retry-button" onClick={loadMaturityData}>Retry</button>
            </div>
          )}

          {!error && loading && (
            <div className="dashboard-loading" aria-live="polite">
              <div className="loading-pulse" />
              <span>Loading maturity data...</span>
            </div>
          )}

          <section className="overview-panel">
            <div className="overview-topline">
              <span className="overview-label">Executive Summary</span>
              <span className={`overview-status ${overallStatus.toLowerCase().replace(/\s+/g, '-')}`}>{overallStatus}</span>
            </div>

            <div className="overview-grid">
              <div className="score-visual">
                <div className="score-ring" style={{ '--score': `${overall.percentage ?? 0}` }}>
                  <div className="score-ring-inner">
                    <strong>{Math.round(overall.percentage ?? 0)}%</strong>
                    <span>{overall.tier_name || 'No Data'}</span>
                  </div>
                </div>
              </div>

              <div className="overview-metrics">
                <div className="overview-metric primary">
                  <span className="metric-label">Overall Compliance Score</span>
                  <strong>{Math.round(overall.percentage ?? 0)}%</strong>
                </div>
                <div className="overview-metric">
                  <span className="metric-label">Maturity Tier</span>
                  <strong>{overall.tier ? `Tier ${overall.tier}` : 'No Data'}</strong>
                </div>
                <div className="overview-metric">
                  <span className="metric-label">Tier Name</span>
                  <strong>{overall.tier_name || 'No Data'}</strong>
                </div>
                <div className="overview-metric">
                  <span className="metric-label">Trend</span>
                  <strong>{overall.trend >= 0 ? '+' : ''}{overall.trend ?? 0}%</strong>
                </div>
                <div className="overview-metric">
                  <span className="metric-label">Status</span>
                  <strong>{overall.status || 'No Data'}</strong>
                </div>
                <div className="overview-metric">
                  <span className="metric-label">API</span>
                  <strong>{isLive ? 'Live' : 'Offline'}</strong>
                </div>
              </div>
            </div>
          </section>

          <section className="dashboard-insights" aria-label="Assessment insights">
            <article className="trend-panel">
              <div className="insight-heading">
                <div>
                  <span className="overview-label">Posture trajectory</span>
                  <h2>Compliance trend</h2>
                </div>
                <span className="trend-chip"><Activity size={14} /> {overall.trend >= 0 ? '+' : ''}{overall.trend ?? 0}% vs prior scan</span>
              </div>
              <div className="trend-chart" role="img" aria-label="Current maturity score and trend compared to the last scan">
                <div className="chart-gridline gridline-top"><span>100</span></div>
                <div className="chart-gridline gridline-mid"><span>50</span></div>
                <div className="chart-gridline gridline-bottom"><span>0</span></div>
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
                <div className="chart-labels"><span>Prior</span><span>Current</span><span>Target</span></div>
              </div>
            </article>

            <article className="attention-panel">
              <div className="insight-heading">
                <div>
                  <span className="overview-label">Priority queue</span>
                  <h2>Needs attention</h2>
                </div>
                <span className="attention-count">{attentionPillars.length} pillars</span>
              </div>
              <div className="attention-list">
                {attentionPillars.length > 0 ? attentionPillars.map((pillar) => (
                  <button key={pillar.function} type="button" className="attention-item" onClick={() => handleSelectZone(pillar.function.toLowerCase())}>
                    <span className="attention-icon"><AlertTriangle size={15} /></span>
                    <span className="attention-copy"><strong>{pillar.function} maturity</strong><small>{pillar.tier_name} / {pillar.percentage ?? 0}%</small></span>
                    <span className="attention-score">{pillar.percentage ?? 0}% <ArrowUpRight size={15} /></span>
                  </button>
                )) : (
                  <div className="attention-empty">
                    <CheckCircle2 size={16} /> All pillars are tracking within acceptable maturity thresholds.
                  </div>
                )}
              </div>
              <button type="button" className="queue-link" onClick={() => handleSelectZone('respond')}><CheckCircle2 size={15} /> Review all findings</button>
            </article>
          </section>

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

          <section className="pillars-grid" aria-label="NIST CSF Pillars">
            {FUNCTIONS.map((pillarConfig) => {
              const pillar = pillars.find((item) => item.function === pillarConfig.title) || {
                function: pillarConfig.title,
                percentage: 0,
                tier: 1,
                tier_name: 'Partial',
                trend: 0,
                status: 'No Data',
              };

              return (
                <PillarCard
                  key={pillarConfig.key}
                  icon={pillarConfig.icon}
                  title={pillarConfig.title}
                  name={pillarConfig.name}
                  description={pillarConfig.title === 'Govern' ? 'Establish and monitor cybersecurity strategy, policies, roles, responsibilities, and risk oversight across the enterprise.' : `${pillarConfig.title} maturity is calculated from the live backend scoring engine.`}
                  status={pillar.status || toTierStatus(pillar.tier)}
                  compliance={Math.round(pillar.percentage ?? 0)}
                  controls={pillar.tier ? `Tier ${pillar.tier}` : 'Live'}
                  accentColor={pillarConfig.accentColor}
                  to={pillarConfig.route}
                  tier={pillar.tier}
                  tierName={pillar.tier_name}
                  trend={pillar.trend}
                  percentage={pillar.percentage}
                />
              );
            })}
          </section>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
