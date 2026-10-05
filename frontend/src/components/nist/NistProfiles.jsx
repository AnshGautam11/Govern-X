import React, { useState } from 'react';
import { IMPLEMENTATION_TIERS, PROFILES_STAGES, TIER_CAVEAT } from '../../data/nistCsfContent';
import { NistSection, Reveal } from './NistPrimitives';

/** Current Profile → Gap Analysis → Target Profile → Improvement. */
export function NistProfiles() {
  return (
    <NistSection
      id="profiles"
      eyebrow="Assessment"
      title="CSF Profiles"
      lede="An Organizational Profile captures the cybersecurity outcomes an organisation has achieved. Profiles are what turn the Framework from a reference document into a usable assessment method, because they give you a concrete current state to compare against a concrete target."
    >
      <div className="profiles-track">
        {PROFILES_STAGES.map((stage, index) => (
          <Reveal key={stage.id} delay={index * 70} className="profiles-stage-wrap">
            <article className="profiles-stage">
              <span className="profiles-stage-index">0{index + 1}</span>
              <h3 className="profiles-stage-label">{stage.label}</h3>
              <p className="profiles-stage-question">{stage.question}</p>
              <p className="profiles-stage-body">{stage.body}</p>
            </article>
            {index < PROFILES_STAGES.length - 1 && (
              <span className="profiles-connector" aria-hidden="true">
                ↓
              </span>
            )}
          </Reveal>
        ))}
      </div>

      <Reveal className="profiles-note">
        <p>
          Profiles let an organisation prioritise improvements against business need and risk,
          rather than against whichever control happens to be easiest to evidence.
        </p>
      </Reveal>
    </NistSection>
  );
}

/** The four Implementation Tiers as an interactive progression. */
export function NistTiers() {
  const [activeTier, setActiveTier] = useState(1);
  const tier = IMPLEMENTATION_TIERS.find((item) => item.tier === activeTier) ?? IMPLEMENTATION_TIERS[0];

  return (
    <NistSection
      id="tiers"
      eyebrow="Maturity"
      title="CSF Organizational Tiers"
      lede="Implementation Tiers describe how rigorously an organisation governs and manages cybersecurity risk. They describe the maturity of the management system itself, progressing from reactive practice to continuous adaptation."
    >
      <div className="tiers-layout">
        <Reveal className="tiers-visual">
          <div className="tiers-ladder">
            {IMPLEMENTATION_TIERS.map((item) => {
              const isActive = item.tier === activeTier;
              return (
                <button
                  key={item.tier}
                  type="button"
                  className={`tier-step${isActive ? ' is-active' : ''}`}
                  style={{ '--tier-color': item.color, '--tier-fill': `${item.tier * 25}%` }}
                  onClick={() => setActiveTier(item.tier)}
                  aria-pressed={isActive}
                >
                  <span className="tier-step-bar" aria-hidden="true" />
                  <span className="tier-step-tier">TIER {item.tier}</span>
                  <span className="tier-step-name">{item.name}</span>
                </button>
              );
            })}
          </div>
          <div className="tiers-meter">
            <div
              className="tiers-meter-fill"
              style={{ '--tier-color': tier.color, width: `${tier.tier * 25}%` }}
            />
          </div>
          <p className="tiers-meter-label">
            Selected: Tier {tier.tier} — {tier.name}
          </p>
        </Reveal>

        <Reveal className="tiers-detail" delay={70}>
          <div className="tiers-detail-card" style={{ '--tier-color': tier.color }}>
            <span className="tiers-detail-tier">TIER {tier.tier}</span>
            <h3>{tier.name}</h3>
            <p>{tier.body}</p>
          </div>
          <p className="tiers-caveat">{TIER_CAVEAT}</p>
        </Reveal>
      </div>
    </NistSection>
  );
}

export default NistProfiles;