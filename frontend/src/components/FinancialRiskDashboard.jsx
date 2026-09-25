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

  const confidence = 90;
  const distribution = Array.isArray(risk.distribution) ? risk.distribution : [];
  const distributionMax = Math.max(...distribution, 0);
  return <main className="assessment-page">
    <header className="assessment-topbar"><Link to="/" className="assessment-back"><ArrowLeft size={16} /> Universe</Link><div className="assessment-brand"><CircleDollarSign size={18} /> GOVERN-X / FINANCIAL RISK</div><Link to="/governance-assessment" className="assessment-link">Governance</Link></header>
    <div className="risk-page-shell"><div className="assessment-heading"><div><span className="assessment-kicker">Quantified exposure</span><h1>Financial Risk Dashboard</h1><p>Risk is calculated only when current scan findings can be matched to configured asset inputs.</p></div><span className="data-badge">Live API</span></div>
      {risk.status === 'calculated' ? <>
        <div className="risk-metrics-grid"><Metric label="Expected annual loss" value={compactMoney(risk.expected_loss)} detail="Based on latest scan" icon={CircleDollarSign} /><Metric label={`Value at Risk (${confidence}%)`} value={compactMoney(risk.p90)} detail="90th percentile" icon={ShieldAlert} /><Metric label="Open findings" value={risk.open_findings} detail={`${risk.assets_considered} inventoried assets`} icon={BarChart3} /><Metric label="Simulation runs" value={risk.iterations?.toLocaleString() || 'N/A'} detail="No simulation needed for zero-loss state" icon={Info} /></div>
        <section className="risk-panel"><div className="panel-heading"><div><span className="assessment-kicker">Loss model</span><h2>Risk distribution</h2></div><span className="panel-note"><Info size={14} /> Current scan</span></div>{distribution.length ? <div className="distribution-chart" role="img" aria-label={`Current-scan loss distribution: P50 ${compactMoney(risk.p50)}, P90 ${compactMoney(risk.p90)}, P95 ${compactMoney(risk.p95)}, P99 ${compactMoney(risk.p99)}`}>{distribution.map((height, index) => <span key={index} style={{ height: `${distributionMax ? Math.max((height / distributionMax) * 100, 3) : 0}%` }} className={index === Math.floor(distribution.length * 0.75) ? 'var-bar' : ''} />)}<div className="distribution-label"><b>P50 {compactMoney(risk.p50)}</b><b>P90 {compactMoney(risk.p90)}</b><b>P95 {compactMoney(risk.p95)}</b><b>P99 {compactMoney(risk.p99)}</b></div></div> : <p className="risk-empty">No loss distribution: the latest scan contains no failed controls.</p>}</section>
      </> : <section className="risk-panel risk-unavailable"><div className="panel-heading"><div><span className="assessment-kicker">Data coverage</span><h2>Financial risk unavailable</h2></div></div><p>{risk.reason || 'Required asset valuation, exposure, and occurrence data are not available for the current findings.'}</p><p>{risk.open_findings} failed controls cannot currently be associated with {risk.assets_considered} inventoried assets.</p></section>}
      <p className="assessment-notice" role="status">Latest scan: {risk.generated_at ? new Date(risk.generated_at).toLocaleString() : 'No scan recorded'}. Data quality: {risk.data_quality}.</p>
    </div>
  </main>;
}
