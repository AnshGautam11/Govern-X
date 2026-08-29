import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { getPillarBySlug } from '../data/pillarData';

function PillarDetail() {
  const { pillarSlug } = useParams();
  const pillar = getPillarBySlug(pillarSlug);

  if (!pillar) {
    return React.createElement(
      'div',
      { className: 'pillar-detail-page' },
      React.createElement(
        'div',
        { className: 'pillar-detail-shell' },
        React.createElement('h2', { className: 'pillar-detail-title' }, 'Pillar not found'),
        React.createElement(
          Link,
          { to: '/', className: 'back-to-dashboard' },
          '← Back to Dashboard'
        )
      )
    );
  }

  return React.createElement(
    'div',
    { className: 'pillar-detail-page' },
    React.createElement(
      'div',
      { className: 'pillar-detail-shell', style: { borderColor: pillar.accentColor } },
      React.createElement(
        'div',
        { className: 'pillar-detail-header' },
        React.createElement('div', null, React.createElement('h1', { className: 'pillar-detail-title' }, pillar.title)),
        React.createElement('div', { className: 'pillar-detail-score' }, `${pillar.score}/100`)
      ),
      React.createElement('p', { className: 'pillar-detail-description' }, pillar.detail),
      React.createElement(
        'div',
        { className: 'pillar-detail-progress' },
        React.createElement(
          'div',
          { className: 'pillar-detail-progress-bar' },
          React.createElement('div', {
            className: 'pillar-detail-progress-fill',
            style: {
              width: `${pillar.score}%`,
              background: `linear-gradient(90deg, ${pillar.accentColor} 0%, #00d4ff 100%)`,
            },
          })
        )
      ),
      React.createElement(
        'div',
        { className: 'compliance-section', style: { marginBottom: '2rem' } },
        React.createElement(
          'div',
          { className: 'compliance-header' },
          React.createElement('span', { className: 'compliance-label' }, 'Pillar Score'),
          React.createElement(
            'span',
            { className: 'compliance-percent', style: { color: pillar.accentColor } },
            `${pillar.score}/100`
          )
        ),
        React.createElement(
          'div',
          { className: 'progress-bar' },
          React.createElement('div', {
            className: 'progress-fill',
            style: {
              width: `${pillar.score}%`,
              background: `linear-gradient(90deg, ${pillar.accentColor} 0%, rgba(0, 255, 65, 0.6) 100%)`,
            },
          })
        )
      ),
      React.createElement(
        Link,
        { to: '/', className: 'back-to-dashboard' },
        '← Back to Dashboard'
      )
    )
  );
}

export default PillarDetail;
