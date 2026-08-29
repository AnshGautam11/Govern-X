import React from 'react';
import { Link } from 'react-router-dom';
import './PillarCard.css';

function PillarCard({ icon, title, description, status, compliance, accentColor, to }) {
  return React.createElement(
    Link,
    {
      to,
      className: 'pillar-card-link',
      'aria-label': `View ${title} details`,
    },
    React.createElement(
      'article',
      {
        className: 'pillar-card',
        style: { '--accent-color': accentColor },
      },
      React.createElement(
        'div',
        { className: 'pillar-top' },
        React.createElement('div', { className: 'pillar-icon' }, icon),
        React.createElement('span', { className: `pillar-status-badge ${status.toLowerCase()}` }, status)
      ),
      React.createElement('h3', { className: 'pillar-title' }, title),
      React.createElement('p', { className: 'pillar-description' }, description),
      React.createElement(
        'div',
        { className: 'compliance-section' },
        React.createElement(
          'div',
          { className: 'compliance-header' },
          React.createElement('span', { className: 'compliance-label' }, 'Score'),
          React.createElement('span', { className: 'compliance-percent' }, `${compliance}/100`)
        ),
        React.createElement(
          'div',
          { className: 'progress-bar' },
          React.createElement('div', { className: 'progress-fill', style: { width: `${compliance}%` } })
        )
      ),
      React.createElement(
        'div',
        { className: 'pillar-action' },
        React.createElement('span', { className: 'action-text' }, 'View Details'),
        React.createElement('span', { className: 'action-arrow' }, '→')
      )
    )
  );
}

export default PillarCard;
