import React from 'react';
import { Link } from 'react-router-dom';
import { pillarData } from '../../data/pillarData';
import './DashboardFooter.css';

/**
 * Site footer for the main dashboard.
 *
 * Uses the same restrained enterprise treatment as the NIST CSF 2.0 page so
 * both read as one product, and surfaces the NIST Framework page as the
 * primary call to action.
 */
export function DashboardFooter() {
  return (
    <footer className="dashboard-footer" aria-label="Site footer">
      <div className="dashboard-footer-cta">
        <div className="dashboard-footer-cta-copy">
          <span className="dashboard-footer-cta-eyebrow">Framework Reference</span>
          <h2 className="dashboard-footer-cta-title">Turn Cybersecurity Frameworks Into Actionable Risk Intelligence.</h2>
          <p className="dashboard-footer-cta-text">
            Understand how the six NIST CSF 2.0 Functions, Profiles and Implementation Tiers map
            onto the posture Govern-X measures on this dashboard.
          </p>
        </div>
        <Link to="/nist-csf-2-0" className="dashboard-footer-cta-button">
          <span className="dashboard-footer-cta-button-label">Explore NIST CSF 2.0</span>
          <span className="dashboard-footer-cta-button-arrow" aria-hidden="true">→</span>
        </Link>
      </div>

      <div className="dashboard-footer-grid">
        <div className="dashboard-footer-brand">
          <span className="dashboard-footer-logo">GOVERN-X</span>
          <p>Automated NIST CSF 2.0 Compliance &amp; Cyber Risk Quantification Engine</p>
        </div>

        <nav className="dashboard-footer-column" aria-label="Product">
          <h3>Product</h3>
          <ul>
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/nist-csf-2-0">NIST CSF 2.0</Link></li>
            <li><Link to="/financial-risk">Risk Assessment</Link></li>
            <li><Link to="/governance-assessment">Governance Assessment</Link></li>
          </ul>
        </nav>

        <nav className="dashboard-footer-column" aria-label="Framework">
          <h3>Framework</h3>
          <ul>
            {pillarData.map((pillar) => (
              <li key={pillar.id}>
                <Link to={pillar.route}>{pillar.name}</Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>

      <div className="dashboard-footer-bottom">
        <div className="dashboard-footer-legal">
          <span>© 2026 Govern-X. All rights reserved.</span>
          <span className="dashboard-footer-motto">Built for cybersecurity governance, risk and compliance.</span>
          <span className="dashboard-footer-company">AXLERO Innovating Solutions</span>
        </div>
        <p className="dashboard-footer-disclaimer">
          Govern-X provides risk assessment and decision-support capabilities. It does not replace
          qualified cybersecurity professionals, organizational risk decisions, or official
          compliance/audit processes.
        </p>
      </div>
    </footer>
  );
}

export default DashboardFooter;