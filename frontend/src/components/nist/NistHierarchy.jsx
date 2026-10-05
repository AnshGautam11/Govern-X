import React, { useState } from 'react';
import { CORE_HIERARCHY, GOVERN_EXAMPLE_HIERARCHY } from '../../data/nistCsfContent';
import { NistSection, Reveal } from './NistPrimitives';

/**
 * Core > Functions > Categories > Subcategories, with a worked Govern example
 * that drills down through official identifiers.
 */
export function NistHierarchy() {
  const [activeLevel, setActiveLevel] = useState(CORE_HIERARCHY[0].level);
  const active = CORE_HIERARCHY.find((item) => item.level === activeLevel) ?? CORE_HIERARCHY[0];

  return (
    <NistSection
      id="core-hierarchy"
      eyebrow="Structure"
      title="Core → Categories → Subcategories"
      lede="The CSF Core is the set of cybersecurity outcomes the Framework is built around. Those outcomes are organised hierarchically, which is what makes an organisation able to assess itself precisely rather than in broad strokes."
    >
      <div className="hierarchy-layout">
        <Reveal className="hierarchy-rail">
          <ol className="hierarchy-steps">
            {CORE_HIERARCHY.map((item, index) => {
              const isActive = item.level === activeLevel;
              return (
                <li key={item.level}>
                  <button
                    type="button"
                    className={`hierarchy-step${isActive ? ' is-active' : ''}`}
                    onClick={() => setActiveLevel(item.level)}
                    aria-pressed={isActive}
                  >
                    <span className="hierarchy-step-index">0{index + 1}</span>
                    <span className="hierarchy-step-title">{item.title}</span>
                  </button>
                </li>
              );
            })}
          </ol>
        </Reveal>

        <Reveal className="hierarchy-detail" delay={70}>
          <div className="hierarchy-detail-card">
            <span className="hierarchy-detail-level">{active.level}</span>
            <h3>{active.title}</h3>
            <p>{active.body}</p>
          </div>

          <div className="hierarchy-example">
            <span className="hierarchy-example-label">Worked example — drilling into Govern</span>
            <ol className="hierarchy-example-list">
              {GOVERN_EXAMPLE_HIERARCHY.map((item) => (
                <li key={item.code}>
                  <span className="hierarchy-example-code">{item.code}</span>
                  <span className="hierarchy-example-text">
                    <span className="hierarchy-example-level">{item.level}</span>
                    <span className="hierarchy-example-title">{item.title}</span>
                  </span>
                </li>
              ))}
            </ol>
            <p className="hierarchy-example-note">
              Identifiers shown are the official NIST CSF 2.0 codes for the Govern Function.
            </p>
          </div>
        </Reveal>
      </div>
    </NistSection>
  );
}

export default NistHierarchy;