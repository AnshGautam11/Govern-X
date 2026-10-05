import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  COMPARISON,
  GOVERN_X_CAPABILITIES,
  GOVERN_X_FLOW,
  RISK_STORY,
} from '../../data/nistCsfContent';
import { NistSection, Reveal } from './NistPrimitives';

/** Telemetry → Govern-X → NIST mapping → risk → executive decision support. */
export function GovernXRole() {
  return (
    <NistSection
      id="where-govern-x-fits"
      eyebrow="Govern-X"
      title="Where Govern-X Fits"
      lede="Govern-X operationalizes the NIST CSF 2.0 approach by connecting cybersecurity telemetry, organizational context, compliance controls and financial risk into a unified assessment workflow."
    >
      <Reveal className="governx-flow" >
        <ol className="governx-flow-track">
          {GOVERN_X_FLOW.map((node, index) => (
            <li
              key={node.id}
              className={`governx-flow-node is-${node.kind}`}
              style={{ '--flow-index': index }}
            >
              <span className="governx-flow-label">{node.label}</span>
            </li>
          ))}
        </ol>
      </Reveal>

      <Reveal className="governx-capabilities" delay={70}>
        <h3 className="governx-subheading">Govern-X Capabilities</h3>
        <div className="governx-capability-grid">
          {GOVERN_X_CAPABILITIES.map((capability) => (
            <article key={capability.id} className="governx-capability">
              <h4>{capability.title}</h4>
              <p>{capability.body}</p>
            </article>
          ))}
        </div>
      </Reveal>
    </NistSection>
  );
}

/** From a single technical finding through to a financial exposure figure. */
export function GovernXExample() {
  const [activeStage, setActiveStage] = useState(RISK_STORY.stages[0].id);
  const stage = RISK_STORY.stages.find((item) => item.id === activeStage) ?? RISK_STORY.stages[0];

  return (
    <NistSection
      id="govern-x-example"
      eyebrow="Worked Example"
      title="From Finding to Business Risk"
      lede="A single technical control failure is rarely actionable on its own. Govern-X traces it through mapping, risk, maturity and financial consequence so the same finding can be discussed by both a security engineer and a board member."
    >
      <Reveal className="example-finding">
        <span className="example-finding-label">Finding</span>
        <blockquote>{RISK_STORY.finding}</blockquote>
      </Reveal>

      <div className="example-layout">
        <Reveal className="example-track">
          <ol className="example-track-list">
            {RISK_STORY.stages.map((item, index) => (
              <li key={item.id}>
                <button
                  type="button"
                  className={`example-stage${item.id === activeStage ? ' is-active' : ''}`}
                  onClick={() => setActiveStage(item.id)}
                  aria-pressed={item.id === activeStage}
                >
                  <span className="example-stage-index">0{index + 1}</span>
                  <span className="example-stage-label">{item.label}</span>
                </button>
              </li>
            ))}
          </ol>
        </Reveal>

        <Reveal className="example-detail" delay={70}>
          <div className="example-detail-card">
            <h3>{stage.label}</h3>
            <p>{stage.body}</p>

            {stage.id === 'financial' && (
              <div className="example-var">
                <span className="example-var-label">Potential Value at Risk</span>
                <strong className="example-var-value">{RISK_STORY.valueAtRisk}</strong>
                <span className="example-var-disclaimer">{RISK_STORY.disclaimer}</span>
              </div>
            )}
          </div>

          <Link to="/" className="nist-btn nist-btn-primary example-cta">
            View in Govern-X Dashboard
            <span aria-hidden="true">→</span>
          </Link>
        </Reveal>
      </div>
    </NistSection>
  );
}

/** Traditional manual process vs the Govern-X automated workflow. */
export function GovernXComparison() {
  return (
    <NistSection
      id="why-different"
      eyebrow="Differentiation"
      title="Why Govern-X Is Different"
      lede="Most organisations assess against a framework manually, on a schedule, using evidence that has already gone stale. Govern-X keeps the assessment current and connected to business risk."
    >
      <Reveal className="comparison-grid">
        <article className="comparison-column comparison-traditional">
          <h3>{COMPARISON.traditional.title}</h3>
          <ul>
            {COMPARISON.traditional.items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article className="comparison-column comparison-governx">
          <h3>{COMPARISON.governX.title}</h3>
          <ul>
            {COMPARISON.governX.items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      </Reveal>
    </NistSection>
  );
}

export default GovernXRole;