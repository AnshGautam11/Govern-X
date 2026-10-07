import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { NIST_FUNCTIONS } from '../../data/nistCsfContent';
import { NistSection, Reveal } from './NistPrimitives';

/**
 * The six Functions laid out as a system diagram. Selecting a node reveals
 * its purpose, activities, outcome and how Govern-X supports it.
 * Falls back to a vertical card list on narrow viewports via CSS.
 */
export function NistFunctions() {
  const [activeId, setActiveId] = useState(NIST_FUNCTIONS[0].id);
  const active = NIST_FUNCTIONS.find((fn) => fn.id === activeId) ?? NIST_FUNCTIONS[0];

  return (
    <NistSection
      id="six-functions"
      eyebrow="The Core"
      title="The Six Functions"
      lede="NIST CSF 2.0 organises every cybersecurity outcome around six Functions. Together they cover how an organisation governs, understands, safeguards, detects, responds and recovers — though they are not a strict linear process and may be applied in the order that fits a given context."
    >
      <div className="functions-layout">
        <Reveal className="functions-visual">
          <div className="functions-orbit" role="tablist" aria-label="NIST CSF 2.0 Functions">
            {NIST_FUNCTIONS.map((fn) => {
              const isActive = fn.id === activeId;
              return (
                <button
                  key={fn.id}
                  type="button"
                  role="tab"
                  id={`fn-tab-${fn.id}`}
                  aria-selected={isActive}
                  aria-controls={`fn-panel-${fn.id}`}
                  className={`function-node node-${fn.id}${isActive ? ' is-active' : ''}`}
                  style={{ '--fn-color': fn.color }}
                  onClick={() => setActiveId(fn.id)}
                >
                  <span className="function-node-code">{fn.code}</span>
                  <span className="function-node-name">{fn.name}</span>
                </button>
              );
            })}
          </div>
          <p className="functions-flow-note">
            Commonly read as <strong>GOVERN → IDENTIFY → PROTECT → DETECT → RESPOND → RECOVER</strong>,
            but the Functions interact rather than run as a mandatory sequence.
          </p>
        </Reveal>

        <Reveal className="functions-detail" delay={80}>
          <div
            className="function-detail-card"
            style={{ '--fn-color': active.color }}
            role="tabpanel"
            id={`fn-panel-${active.id}`}
            aria-labelledby={`fn-tab-${active.id}`}
            tabIndex={0}
          >
            <span className="function-detail-code">{active.code}</span>
            <h3 className="function-detail-title">{active.name}</h3>
            <p className="function-detail-summary">{active.summary}</p>
            <p className="function-detail-purpose">{active.purpose}</p>

            <div className="function-detail-block">
              <h4>Example security activities</h4>
              <ul>
                {active.activities.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="function-detail-block">
              <h4>Example organizational outcome</h4>
              <p>{active.outcome}</p>
            </div>

            <div className="function-detail-block is-governx">
              <h4>How Govern-X supports this Function</h4>
              <p>{active.governX}</p>
            </div>

            <Link to={`/${active.id}`} className="function-detail-link">
              Open {active.name} in Govern-X
              <span aria-hidden="true">→</span>
            </Link>
          </div>
        </Reveal>
      </div>
    </NistSection>
  );
}

export default NistFunctions;