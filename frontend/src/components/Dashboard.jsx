import React from 'react';
import './Dashboard.css';
import PillarCard from './PillarCard';
import TypingEffect from './TypingEffect';
import TerminalMessages from './TerminalMessages';
import { overallScore, pillarData } from '../data/pillarData';

function Dashboard() {
  const pillars = pillarData;

  return React.createElement(
    'div',
    { className: 'dashboard' },
    React.createElement(
      'div',
      { className: 'dashboard-header' },
      React.createElement(
        'div',
        { className: 'hero-section' },
        React.createElement(
          'h1',
          { className: 'dashboard-title' },
          React.createElement(TypingEffect, { text: 'GOVERNX', speed: 80 })
        ),
        React.createElement(
          'p',
          { className: 'dashboard-subtitle' },
          'Automated NIST CSF 2.0 Compliance Engine'
        ),
        React.createElement(
          'div',
          { className: 'status-line' },
          React.createElement('span', { className: 'status-item' }, '● SYSTEM STATUS: SECURE'),
          React.createElement('span', { className: 'status-separator' }, '|'),
          React.createElement('span', { className: 'status-item' }, '● COMPLIANCE ENGINE: ONLINE'),
          React.createElement('span', { className: 'status-separator' }, '|'),
          React.createElement('span', { className: 'status-item' }, '● LAST SCAN: 2 MINUTES AGO')
        )
      ),
      React.createElement(TerminalMessages)
    ),
    React.createElement(
      'div',
      { className: 'compliance-overview' },
      React.createElement(
        'div',
        { className: 'metric' },
        React.createElement('div', { className: 'metric-value' }, `${overallScore.score}/100`),
        React.createElement('div', { className: 'metric-label' }, 'Overall Score')
      ),
      React.createElement(
        'div',
        { className: 'metric' },
        React.createElement('div', { className: 'metric-value' }, '124'),
        React.createElement('div', { className: 'metric-label' }, 'Controls Assessed')
      ),
      React.createElement(
        'div',
        { className: 'metric' },
        React.createElement('div', { className: 'metric-value' }, '97'),
        React.createElement('div', { className: 'metric-label' }, 'Controls Compliant')
      ),
      React.createElement(
        'div',
        { className: 'metric' },
        React.createElement('div', { className: 'metric-value' }, '27'),
        React.createElement('div', { className: 'metric-label' }, 'Open Findings')
      )
    ),
    React.createElement(
      'div',
      { className: 'pillars-grid' },
      ...pillars.map((pillar) =>
        React.createElement(PillarCard, {
          key: pillar.id,
          icon: pillar.icon,
          title: pillar.title,
          description: pillar.description,
          status: pillar.status,
          compliance: pillar.score,
          accentColor: pillar.accentColor,
          to: `/pillar/${pillar.slug}`,
        })
      )
    )
  );
}

export default Dashboard;
