import React, { useEffect, useState } from 'react';
import { ArrowLeft, BarChart3, CircleDollarSign, Database, Info, ShieldAlert } from 'lucide-react';
import { Link } from 'react-router-dom';
import { fetchFinancialRisk } from '../lib/api';
import { mockFinancialRisk } from '../data/mockFinancialRisk';
import './AssessmentPages.css';

const money = (value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(value || 0);
const compactMoney = (value) => `₹${((value || 0) / 1000000).toFixed(1)}M`;

function Metric({ label, value, detail, icon: Icon }) {
  return <article className="risk-metric"><div className="risk-metric-icon"><Icon size={18} /></div><span>{label}</span><strong>{value}</strong><small>{detail}</small></article>;
}

export default function FinancialRiskDashboard() {
  const [risk, setRisk] = useState(null);
  const [usingMock, setUsingMock] = useState(false);
  const [status, setStatus] = useState('Loading financial risk assessment...');

  useEffect(() => {
    fetchFinancialRisk().then((payload) => {
      if (!payload || typeof payload !== 'object') throw new Error('Empty response');
      setRisk(payload);
      setStatus('Live financial risk service connected.');
    }).catch(() => {
      setRisk(mockFinancialRisk);
      setUsingMock(true);
      setStatus('Financial risk API unavailable. Showing clearly labelled demo data.');
    });
  }, []);

  if (!risk) return <main className="assessment-page"><div className="assessment-loading">{status}</div></main>;
  const confidence = Math.round((risk.confidenceLevel || 0.95) * 100);
  return <main className="assessment-page">
    <header className="assessment-topbar"><Link to="/" className="assessment-back"><ArrowLeft size={16} /> Universe</Link><div className="assessment-brand"><CircleDollarSign size={18} /> GOVERN-X / FINANCIAL RISK</div><Link to="/governance-assessment" className="assessment-link">Governance</Link></header>
    <div className="risk-page-shell"><div className="assessment-heading"><div><span className="assessment-kicker">Quantified exposure</span><h1>Financial Risk Dashboard</h1><p>Estimated cyber loss exposure from the organization&apos;s assessed assets and risk model.</p></div><span className={`data-badge ${usingMock ? 'demo' : ''}`}>{usingMock ? 'Demo fallback' : 'Live API'}</span></div>
      <div className="risk-metrics-grid"><Metric label="Value at Risk" value={compactMoney(risk.valueAtRisk)} detail={`${confidence}% confidence threshold`} icon={ShieldAlert} /><Metric label="Expected annual loss" value={compactMoney(risk.expectedLoss)} detail="Estimated average model impact" icon={BarChart3} /><Metric label="Maximum simulated loss" value={compactMoney(risk.maxLoss)} detail="Upper simulated exposure" icon={CircleDollarSign} /><Metric label="Total asset value" value={compactMoney(risk.totalAssetValue)} detail={`${risk.assetsAtRisk || 0} assets at risk`} icon={Database} /></div>
      <section className="risk-panel"><div className="panel-heading"><div><span className="assessment-kicker">Loss model</span><h2>Loss distribution</h2></div><span className="panel-note"><Info size={14} /> Backend-generated distribution</span></div><div className="distribution-chart" role="img" aria-label={`Loss distribution with Value at Risk at ${confidence}% confidence`}>{(risk.distribution || []).map((height, index) => <span key={index} style={{ height: `${height}%` }} className={index === Math.floor((risk.distribution.length || 1) * 0.7) ? 'var-bar' : ''} />)}<div className="distribution-label"><b>Expected loss</b><b>VaR {confidence}%</b></div></div><p className="metric-explanation">VaR is an estimated loss threshold that the selected model could reach or exceed at the displayed confidence level. It is not a guaranteed maximum loss.</p></section>
      <section className="risk-panel"><div className="panel-heading"><div><span className="assessment-kicker">Exposure allocation</span><h2>Financial risk breakdown</h2></div></div><div className="risk-table-wrap"><table className="risk-table"><thead><tr><th>Asset category</th><th>Asset value</th><th>Exposure</th><th>Estimated risk</th></tr></thead><tbody>{(risk.breakdown || []).map((item) => <tr key={item.category}><td><strong>{item.category}</strong></td><td>{money(item.value)}</td><td>{item.exposure}%</td><td>{money(item.risk)}</td></tr>)}</tbody></table></div></section>
      <p className="assessment-notice" role="status">{status} {usingMock && 'These values are synthetic and should not be treated as board-ready estimates.'}</p>
    </div>
  </main>;
}
