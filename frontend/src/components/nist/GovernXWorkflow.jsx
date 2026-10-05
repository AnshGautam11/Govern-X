import React from 'react';
import { PROCESS_STEPS, WORKFLOW_LAYERS } from '../../data/nistCsfContent';
import { NistSection, Reveal } from './NistPrimitives';

/** The seven-step assessment cycle Govern-X runs. */
export function NistProcess() {
  return (
    <NistSection
      id="how-it-works"
      eyebrow="Method"
      title="How NIST CSF 2.0 Works"
      lede="Applying the Framework is a cycle rather than a one-off project. Each pass produces a Profile, and the Profile feeds the next pass — which is what makes the process continuous rather than periodic."
    >
      <Reveal className="process-track">
        <ol className="process-list">
          {PROCESS_STEPS.map((step) => (
            <li key={step.id} className="process-step" style={{ '--step-index': step.id }}>
              <span className="process-step-index">STEP {step.id}</span>
              <h3 className="process-step-title">{step.title}</h3>
              <p className="process-step-body">{step.body}</p>
            </li>
          ))}
        </ol>
      </Reveal>
    </NistSection>
  );
}

/** Full system diagram: organization → telemetry → Govern-X → engines → decisions. */
export function GovernXWorkflow() {
  const engines = WORKFLOW_LAYERS.filter((layer) => layer.kind === 'engine');

  return (
    <NistSection
      id="workflow"
      eyebrow="Architecture"
      title="The Govern-X Assessment Workflow"
      lede="Every assessment Govern-X runs follows the same path: collect telemetry, normalise it against the CSF Core, score it, find the gaps, and express the result in terms a decision-maker can act on."
    >
      <Reveal className="workflow-diagram">
        <div className="workflow-column">
          {WORKFLOW_LAYERS.filter((layer) => layer.kind === 'source').map((layer) => (
            <div key={layer.id} className={`workflow-node is-${layer.kind}`}>
              {layer.label}
            </div>
          ))}
        </div>

        <span className="workflow-arrow" aria-hidden="true">↓</span>

        <div className="workflow-node is-core">{WORKFLOW_LAYERS.find((l) => l.kind === 'core').label}</div>

        <span className="workflow-arrow" aria-hidden="true">↓</span>

        <div className="workflow-branches">
          {engines.map((layer) => (
            <div key={layer.id} className={`workflow-node is-${layer.kind}`}>
              {layer.label}
            </div>
          ))}
        </div>

        <span className="workflow-arrow" aria-hidden="true">↓</span>

        <div className="workflow-column">
          {WORKFLOW_LAYERS.filter((layer) => layer.kind === 'outcome').map((layer) => (
            <div key={layer.id} className={`workflow-node is-${layer.kind}`}>
              {layer.label}
            </div>
          ))}
        </div>
      </Reveal>
    </NistSection>
  );
}

export default NistProcess;