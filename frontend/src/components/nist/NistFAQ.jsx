import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FAQ_ITEMS } from '../../data/nistCsfContent';
import { NIST_FUNCTIONS } from '../../data/nistCsfContent';
import { NistSection, Reveal } from './NistPrimitives';

/** Single-open accordion with full keyboard support. */
export function NistFAQ() {
  const [openId, setOpenId] = useState(FAQ_ITEMS[0].q);

  return (
    <NistSection
      id="faq"
      eyebrow="Reference"
      title="Frequently Asked Questions"
      lede="Common questions about the Framework itself, and about how Govern-X applies it."
    >
      <Reveal className="faq-list">
        {FAQ_ITEMS.map((item) => {
          const isOpen = item.q === openId;
          return (
            <div key={item.q} className={`faq-item${isOpen ? ' is-open' : ''}`}>
              <h3 className="faq-question-heading">
                <button
                  type="button"
                  className="faq-question"
                  aria-expanded={isOpen}
                  aria-controls={`faq-panel-${FAQ_ITEMS.indexOf(item)}`}
                  id={`faq-button-${FAQ_ITEMS.indexOf(item)}`}
                  onClick={() => setOpenId(isOpen ? null : item.q)}
                >
                  <span>{item.q}</span>
                  <span className="faq-toggle" aria-hidden="true">
                    {isOpen ? '−' : '+'}
                  </span>
                </button>
              </h3>
              <div
                className="faq-answer"
                id={`faq-panel-${FAQ_ITEMS.indexOf(item)}`}
                role="region"
                aria-labelledby={`faq-button-${FAQ_ITEMS.indexOf(item)}`}
                hidden={!isOpen}
              >
                <p>{item.a}</p>
              </div>
            </div>
          );
        })}
      </Reveal>
    </NistSection>
  );
}

export function NistCTA() {
  return (
    <section className="nist-cta">
      <div className="nist-container nist-cta-inner">
        <h2 className="nist-cta-title">
          Turn Cybersecurity Frameworks Into Actionable Risk Intelligence.
        </h2>
        <p className="nist-cta-text">
          Govern-X helps organizations move from static compliance assessments to continuous
          visibility, measurable maturity and business-focused cyber risk.
        </p>
        <div className="nist-cta-actions">
          <Link to="/" className="nist-btn nist-btn-primary">
            Open Govern-X Dashboard
            <span aria-hidden="true">→</span>
          </Link>
          <Link to="/financial-risk" className="nist-btn nist-btn-ghost">
            Explore Risk Assessment
            <span aria-hidden="true">→</span>
          </Link>
        </div>
      </div>
    </section>
  );
}

/** Site-wide footer; Framework links open each Function's Govern-X pillar page. */
export function NistFooter() {
  return (
    <footer className="nist-footer">
      <div className="nist-container">
        <div className="nist-footer-grid">
          <div className="nist-footer-brand">
            <span className="nist-footer-logo">GOVERN-X</span>
            <p>Automated NIST CSF 2.0 Compliance &amp; Cyber Risk Quantification Engine</p>
          </div>

          <nav className="nist-footer-column" aria-label="Product">
            <h3>Product</h3>
            <ul>
              <li><Link to="/">Dashboard</Link></li>
              <li><Link to="/financial-risk">Risk Assessment</Link></li>
              <li><Link to="/nist-csf-2-0">NIST CSF 2.0</Link></li>
              <li><Link to="/governance-assessment">Findings</Link></li>
              <li><Link to="/">Scan History</Link></li>
            </ul>
          </nav>

          <nav className="nist-footer-column" aria-label="Framework">
                      <h3>Framework</h3>
                      <ul>
                        {NIST_FUNCTIONS.map((fn) => (
                          <li key={fn.id}>
                            <Link to={`/${fn.id}`} className="nist-footer-link">
                              {fn.name}
                            </Link>
                          </li>
                        ))}
                      </ul>
                    </nav>

          <nav className="nist-footer-column" aria-label="Resources">
            <h3>Resources</h3>
            <ul>
              <li><Link to="/nist-csf-2-0">Documentation</Link></li>
              <li><Link to="/nist-csf-2-0">NIST CSF 2.0</Link></li>
              <li><Link to="/">About Govern-X</Link></li>
            </ul>
          </nav>
        </div>

        <div className="nist-footer-bottom">
          <div className="nist-footer-legal">
            <span>© 2026 Govern-X. All rights reserved.</span>
            <span className="nist-footer-motto">Built for cybersecurity governance, risk and compliance.</span>
            <span className="nist-footer-company">AXLERO Innovating Solutions</span>
          </div>
          <p className="nist-footer-disclaimer">
            Govern-X provides risk assessment and decision-support capabilities. It does not replace
            qualified cybersecurity professionals, organizational risk decisions, or official
            compliance/audit processes.
          </p>
        </div>
      </div>
    </footer>
  );
}

export default NistFAQ;