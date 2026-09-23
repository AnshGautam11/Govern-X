import React, { useEffect, useState } from 'react';
import { ArrowLeft, BarChart3, CircleDollarSign, Info, RefreshCw, ShieldAlert } from 'lucide-react';
import { Link } from 'react-router-dom';
import { fetchFinancialRisk } from '../lib/api';
import './AssessmentPages.css';

const compactMoney = (value) => {
  if (typeof value !== 'number' || !Number.isFinite(value)) return 'N/A';
  const absoluteValue = Math.abs(value);
  const unit = absoluteValue >= 1000000 ? 'M' : absoluteValue >= 1000 ? 'K' : '';
  const divisor = unit === 'M' ? 1000000 : unit === 'K' ? 1000 : 1;
  return `$${(value / divisor).toFixed(unit ? 1 : 0)}${unit}`;
};

function Metric({ label, value, detail, icon: Icon }) {
  return <article className="risk-metric"><div className="risk-metric-icon"><Icon size={18} /></div><span>{label}</span><strong>{value}</strong><small>{detail}</small></article>;
}

export default function FinancialRiskDashboard() {
  const [risk, setRisk] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [requestKey, setRequestKey] = useState(0);
  const retryAssessment = () => {
    setLoading(true);
    setRisk(null);
    setError(null);
    setRequestKey((key) => key + 1);
  };

  useEffect(() => {
    let active = true;
    fetchFinancialRisk()
      .then((payload) => {
        if (active) setRisk(payload);
      })
      .catch((requestError) => {
        if (active) setError(requestError.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, [requestKey]);

  if (loading) return <main className="assessment-page"><div className="risk-status-panel"><div className="risk-skeleton risk-skeleton-title" /><div className="risk-skeleton risk-skeleton-card" /><div className="risk-skeleton risk-skeleton-panel" /></div></main>;
  if (error) return <main className="assessment-page"><div className="risk-status-panel risk-error"><ShieldAlert size={24} /><h1>Financial risk unavailable</h1><p>{error}</p><button type="button" className="risk-retry" onClick={retryAssessment}><RefreshCw size={15} /> Retry request</button></div></main>;
  if (!risk) return <main className="assessment-page"><div className="risk-status-panel"><p>No financial risk assessment is available yet.</p><button type="button" className="risk-retry" onClick={retryAssessment}><RefreshCw size={15} /> Request assessment</button></div></main>;

  const confidence = Math.round((risk.confidence_level || 0.9) * 100);
  const distribution = Array.isArray(risk.distribution) ? risk.distribution : [];
  const distributionMax = Math.max(...distribution, 0);
  return <main className="assessment-page">
    <header className="assessment-topbar"><Link to="/" className="assessment-back"><ArrowLeft size={16} /> Universe</Link><div className="assessment-brand"><CircleDollarSign size={18} /> GOVERN-X / FINANCIAL RISK</div><Link to="/governance-assessment" className="assessment-link">Governance</Link></header>
    <div className="risk-page-shell"><div className="assessment-heading"><div><span className="assessment-kicker">Quantified exposure</span><h1>Financial Risk Dashboard</h1><p>Estimated annual cyber loss from the backend Monte Carlo assessment.</p></div><span className="data-badge">Live API</span></div>
      <div className="risk-metrics-grid"><Metric label="Total estimated financial risk" value={compactMoney(risk.expected)} detail="Expected annual loss" icon={CircleDollarSign} /><Metric label={`Value at Risk (${confidence}%)`} value={compactMoney(risk.p90)} detail="90th percentile simulated loss" icon={ShieldAlert} /><Metric label="Potential annual loss" value={compactMoney(risk.expected)} detail="Expected model impact" icon={BarChart3} /><Metric label="Simulation runs" value={risk.iterations?.toLocaleString() || 'N/A'} detail="Backend Monte Carlo iterations" icon={Info} /></div>
      <section className="risk-panel"><div className="panel-heading"><div><span className="assessment-kicker">Loss model</span><h2>Risk distribution</h2></div><span className="panel-note"><Info size={14} /> Backend-generated</span></div>{distribution.length ? <div className="distribution-chart" role="img" aria-label={`Simulated loss distribution with Value at Risk at ${confidence}% confidence`}>{distribution.map((height, index) => <span key={index} style={{ height: `${distributionMax ? Math.max((height / distributionMax) * 100, 3) : 0}%` }} className={index === Math.floor(distribution.length * 0.75) ? 'var-bar' : ''} />)}<div className="distribution-label"><b>P10 {compactMoney(risk.p10)}</b><b>VaR {confidence}% {compactMoney(risk.p90)}</b></div></div> : <p className="risk-empty">The API returned no distribution bins for this assessment.</p>}<p className="metric-explanation">VaR is the simulated loss threshold at the displayed percentile. It is not a guaranteed maximum loss.</p></section>
      <section className="risk-panel risk-unavailable"><div className="panel-heading"><div><span className="assessment-kicker">Data coverage</span><h2>Not calculated by this API</h2></div></div><p>Critical and high-risk finding counts, asset-category exposure, NIST pillar contribution, and historical trend data are unavailable from the current risk response.</p></section>
      <p className="assessment-notice" role="status">Assessment generated {risk.generated_at ? new Date(risk.generated_at).toLocaleString() : 'at an unknown time'}. {risk.disclaimer}</p>
    </div>
  </main>;
}
