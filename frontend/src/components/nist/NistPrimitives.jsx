import React from 'react';
import { Link } from 'react-router-dom';
import { NIST_FUNCTIONS } from '../../data/nistCsfContent';
import { useRevealOnScroll, useScrollToSection } from './useScrollReveal';

/**
 * Section shell used by every block on the page so headings, spacing and the
 * scroll-reveal behaviour stay consistent.
 */
export function NistSection({ id, eyebrow, title, lede, children, className = '', accent }) {
  return (
    <section
      id={id}
      className={`nist-section ${className}`}
      style={accent ? { '--section-accent': accent } : undefined}
    >
      <div className="nist-container">
        {(eyebrow || title) && (
          <header className="nist-section-head">
            {eyebrow && <span className="nist-eyebrow">{eyebrow}</span>}
            {title && <h2 className="nist-section-title">{title}</h2>}
            {lede && <p className="nist-section-lede">{lede}</p>}
          </header>
        )}
        {children}
      </div>
    </section>
  );
}

/** Wraps children in a fade/slide-up reveal driven by IntersectionObserver. */
export function Reveal({ children, delay = 0, className = '' }) {
  const { ref, isVisible } = useRevealOnScroll();
  return (
    <div
      ref={ref}
      className={`nist-reveal ${isVisible ? 'is-visible' : ''} ${className}`}
      style={delay ? { transitionDelay: `${delay}ms` } : undefined}
    >
      {children}
    </div>
  );
}

export function NistHero() {
  const scrollToSection = useScrollToSection();

  return (
    <header className="nist-hero">
      <div className="nist-hero-grid" aria-hidden="true" />
      <div className="nist-hero-radar" aria-hidden="true">
        <span className="radar-sweep" />
        {NIST_FUNCTIONS.map((fn, index) => (
          <span
            key={fn.id}
            className="radar-node"
            style={{
              '--node-color': fn.color,
              '--node-index': index,
            }}
          />
        ))}
      </div>

      <div className="nist-container nist-hero-content">
        <span className="nist-eyebrow">National Institute of Standards and Technology</span>
        <h1 className="nist-hero-title">NIST CSF 2.0</h1>
        <p className="nist-hero-subtitle">
          Understand the framework that helps organizations manage, assess, and improve
          cybersecurity risk.
        </p>
        <p className="nist-hero-lede">
          NIST Cybersecurity Framework 2.0 provides a structured approach for organizations to
          understand their cybersecurity posture, prioritize risks, and continuously improve their
          security capabilities.
        </p>

        <div className="nist-hero-actions">
          <button
            type="button"
            className="nist-btn nist-btn-primary"
            onClick={() => scrollToSection('six-functions')}
          >
            Explore the Framework
            <span aria-hidden="true">↓</span>
          </button>
          <button
            type="button"
            className="nist-btn nist-btn-ghost"
            onClick={() => scrollToSection('where-govern-x-fits')}
          >
            How Govern-X Helps
            <span aria-hidden="true">↓</span>
          </button>
        </div>

        <dl className="nist-hero-facts">
          <div>
            <dt>Functions</dt>
            <dd>6</dd>
          </div>
          <div>
            <dt>Implementation Tiers</dt>
            <dd>4</dd>
          </div>
          <div>
            <dt>Focus</dt>
            <dd>Cybersecurity risk</dd>
          </div>
          <div>
            <dt>Status</dt>
            <dd>Voluntary</dd>
          </div>
        </dl>

        <p className="nist-hero-note">
          Looking for your live posture?{' '}
          <Link to="/">Open the Govern-X dashboard</Link>
        </p>
      </div>
    </header>
  );
}

export default NistSection;