import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

const renderAppAt = (path) => {
  window.history.pushState({}, '', path);
  render(React.createElement(BrowserRouter, null, React.createElement(App)));
};

describe('GovernX 3D Security Universe & NIST CSF Navigation', () => {
  it('renders the 3D Security Universe dashboard and all six pillar links', async () => {
    renderAppAt('/');

    await waitFor(() => {
      const titles = screen.getAllByText(/GovernX/i);
      expect(titles.length).toBeGreaterThan(0);
    });

    expect(screen.getAllByText(/The Security Universe/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/NIST CSF 2.0 Compliance Overview/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Overall Compliance Score/i).length).toBeGreaterThan(0);

    expect(screen.getByRole('link', { name: /view govern details/i })).toHaveAttribute('href', '/govern');
    expect(screen.getByRole('link', { name: /view identify details/i })).toHaveAttribute('href', '/identify');
    expect(screen.getByRole('link', { name: /view protect details/i })).toHaveAttribute('href', '/protect');
    expect(screen.getByRole('link', { name: /view detect details/i })).toHaveAttribute('href', '/detect');
    expect(screen.getByRole('link', { name: /view respond details/i })).toHaveAttribute('href', '/respond');
    expect(screen.getByRole('link', { name: /view recover details/i })).toHaveAttribute('href', '/recover');
  });

  it('renders interactive 3D security universe nodes that route to pillar pages', async () => {
    renderAppAt('/');

    const zoneButtons = await screen.findAllByRole('button', { name: /open governance city zone/i });
    expect(zoneButtons.length).toBeGreaterThan(0);

    fireEvent.click(zoneButtons[0]);
    await waitFor(() => expect(screen.getByText('Govern')).toBeInTheDocument());
    expect(screen.getByText(/governance, accountability, and policy oversight/i)).toBeInTheDocument();
  });

  it('renders the govern pillar detail page, policies, and placeholder score', async () => {
    renderAppAt('/govern');

    await waitFor(() => expect(screen.getByText('Govern')).toBeInTheDocument());
    expect(screen.getAllByText(/82%|82\/100/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Strategic Policies & Standards/i)).toBeInTheDocument();
    expect(screen.getByText(/Information Security Management Standard/i)).toBeInTheDocument();
  });

  it('renders the protect pillar detail page and defense safeguards', async () => {
    renderAppAt('/protect');

    await waitFor(() => expect(screen.getByText('Protect')).toBeInTheDocument());
    expect(screen.getAllByText(/88%|88\/100/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Protective Safeguards & Defense Infrastructure/i)).toBeInTheDocument();
  });

  it('supports Enter System warp button on the 3D portal', async () => {
    renderAppAt('/');

    const enterBtn = screen.getByRole('button', { name: /enter system/i });
    expect(enterBtn).toBeInTheDocument();

    fireEvent.click(enterBtn);
    expect(enterBtn).toHaveTextContent(/WARPING/i);
  });

  it('renders all six pillar detail routes correctly with rich domain cards', async () => {
    const pillars = [
      { path: '/identify', name: 'Identify', score: '76%', domainText: 'Asset Inventory & Criticality Breakdown' },
      { path: '/detect', name: 'Detect', score: '71%', domainText: 'Detected Threat Signatures & CVE Correlations' },
      { path: '/respond', name: 'Respond', score: '68%', domainText: 'Active Incident Lifecycle Timeline' },
      { path: '/recover', name: 'Recover', score: '79%', domainText: 'System Restoration & Resiliency Catalog' },
    ];

    for (const p of pillars) {
      renderAppAt(p.path);
      await waitFor(() => expect(screen.getByText(p.name)).toBeInTheDocument());
      expect(screen.getAllByText(new RegExp(p.score)).length).toBeGreaterThan(0);
      expect(screen.getByText(p.domainText)).toBeInTheDocument();
    }
  });

  it('supports seamless pillar-to-pillar navigation on detail pages', async () => {
    renderAppAt('/govern');

    await waitFor(() => expect(screen.getByText('Govern')).toBeInTheDocument());

    const switchBtn = screen.getByRole('button', { name: /switch to identify pillar/i });
    expect(switchBtn).toBeInTheDocument();

    fireEvent.click(switchBtn);
    await waitFor(() => expect(screen.getByText('Identify')).toBeInTheDocument());
    expect(screen.getByText(/Asset Inventory & Criticality Breakdown/i)).toBeInTheDocument();
  });
});
