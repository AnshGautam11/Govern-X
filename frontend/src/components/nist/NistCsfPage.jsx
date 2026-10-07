import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { CSF_2_CHANGES, CSF_EVOLUTION, NIST_FUNCTIONS, WHY_NIST } from '../../data/nistCsfContent';
import { NistHero, NistSection, Reveal } from './NistPrimitives';
import NistFunctions from './NistFunctions';
import NistHierarchy from './NistHierarchy';
import NistProfiles, { NistTiers } from './NistProfiles';
import GovernXRole, { GovernXComparison, GovernXExample } from './GovernXRole';
import NistProcess, { GovernXWorkflow } from './GovernXWorkflow';
import NistFAQ, { NistCTA, NistFooter } from './NistFAQ';
import './NistCsfPage.css';

const WHAT_IS_FLOW = [
  'Organization',
  'Cybersecurity Risk',
  'NIST CSF 2.0',
  'Assess → Prioritize → Improve',
  'Stronger Cybersecurity Posture',
];

/** Navigational header shared by the page so it never traps the user. */
function NistTopBar() {
  const navigate = useNavigate();
  return (
    <div className="nist-topbar">
      <div className="nist-container nist-topbar-inner">
        <Link to="/" className="nist-topbar-brand">
          <span className="nist-topbar-mark" aria-hidden="true">◉</span>
          <span>Govern-X</span>
        </Link>
        <nav className="nist-topbar-nav" aria-label="Page sections">
          <button type="button" onClick={() => document.getElementById('six-functions')?.scrollIntoView({ behavior: 'smooth' })}>
            Functions
          </button>
          <button type="button" onClick={() => document.getElementById('core-hierarchy')?.scrollIntoView({ behavior: 'smooth' })}>
            Core
          </button>
          <button type="button" onClick={() => document.getElementById('tiers')?.scrollIntoView({ behavior: 'smooth' })}>
            Tiers
          </button>
          <button type="button" onClick={() => document.getElementById('faq')?.scrollIntoView({ behavior: 'smooth' })}>
            FAQ
          </button>
        </nav>
        <button type="button" className="nist-topbar-exit" onClick={() => navigate('/')}>
          Back to Dashboard
        </button>
      </div>
    </div>
  );
}

function WhatIsCsf() {
  return (
    <NistSection
      id="what-is-csf"
      eyebrow="Overview"
      title="What is NIST CSF 2.0?"
      lede="NIST Cybersecurity Framework 2.0 is a cybersecurity risk management framework developed by the National Institute of Standards and Technology. It gives organisations a common structure for understanding and managing cybersecurity risk, so posture can be assessed, compared and improved on a shared basis."
    >
      <div className="whatis-layout">
        <Reveal className="whatis-capabilities">
          <p className="whatis-intro">
            It provides organizations with a common structure to:
          </p>
          <ul className="whatis-list">
            {NIST_FUNCTIONS.map((fn) => (
              <li key={fn.id} style={{ '--fn-color': fn.color }}>
                <span className="whatis-list-code">{fn.code}</span>
                <span>
                  <strong>{fn.name}</strong> — {fn.summary}
                </span>
              </li>
            ))}
          </ul>
        </Reveal>

        <Reveal className="whatis-flow" delay={70}>
          <ol className="flow-rail">
            {WHAT_IS_FLOW.map((step, index) => (
              <li key={step} className={index === WHAT_IS_FLOW.length - 1 ? 'is-final' : ''}>
                {step}
              </li>
            ))}
          </ol>
        </Reveal>
      </div>
    </NistSection>
  );
}

function WhyNist() {
  return (
    <NistSection
      id="why-nist"
      eyebrow="Rationale"
      title="Why NIST CSF 2.0?"
      lede="Organisations adopt the Framework because a structured, shared method produces better risk decisions than ad-hoc security metrics alone."
    >
      <div className="why-grid">
        {WHY_NIST.map((item, index) => (
          <Reveal key={item.id} delay={index * 60} className="why-card-wrap">
            <article className="why-card" tabIndex={0}>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
            </article>
          </Reveal>
        ))}
      </div>
    </NistSection>
  );
}

function WhatChanged() {
  return (
    <NistSection
      id="what-changed"
      eyebrow="Evolution"
      title="What’s New in NIST CSF 2.0?"
      lede="CSF 2.0 is an evolution of the original Framework, not a replacement of everything that came before. The six-function structure, the Core and the tiered characteristics of risk management all carry forward."
    >
      <div className="changes-grid">
        {CSF_2_CHANGES.map((change, index) => (
          <Reveal key={change.id} delay={index * 60} className="changes-card-wrap">
            <article className="changes-card">
              <span className="changes-index">{change.index}</span>
              <h3>{change.title}</h3>
              <span className="changes-emphasis">{change.emphasis}</span>
              <p>{change.body}</p>
            </article>
          </Reveal>
        ))}
      </div>

      <Reveal className="evolution">
        <h3 className="evolution-title">CSF 1.1 → CSF 2.0</h3>
        <div className="evolution-table-wrap">
          <table className="evolution-table">
            <thead>
              <tr>
                <th scope="col">Aspect</th>
                <th scope="col">{CSF_EVOLUTION.from}</th>
                <th scope="col">{CSF_EVOLUTION.to}</th>
              </tr>
            </thead>
            <tbody>
              {CSF_EVOLUTION.rows.map((row) => (
                <tr key={row.aspect}>
                  <th scope="row">{row.aspect}</th>
                  <td>{row.v1}</td>
                  <td>{row.v2}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="evolution-note">{CSF_EVOLUTION.note}</p>
      </Reveal>
    </NistSection>
  );
}

export function NistCsfPage() {
  return (
    <div className="nist-page">
      <NistTopBar />
      <NistHero />
      <main className="nist-main">
        <WhatIsCsf />
        <WhyNist />
        <WhatChanged />
        <NistFunctions />
        <NistHierarchy />
        <NistProfiles />
        <NistTiers />
        <NistProcess />
        <GovernXRole />
        <GovernXWorkflow />
        <GovernXExample />
        <GovernXComparison />
        <NistFAQ />
      </main>
      <NistCTA />
      <NistFooter />
    </div>
  );
}

export default NistCsfPage;