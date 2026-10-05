import React from 'react';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

const renderAppAt = (path) => {
  window.history.pushState({}, '', path);
  render(React.createElement(BrowserRouter, null, React.createElement(App)));
};

/**
 * The dashboard fires several independent fetches on mount. Wait for both the
 * maturity load and the health probe to settle so no state update lands after
 * the test environment tears down.
 */
const waitForDashboardSettled = async () => {
  await waitFor(() => {
    expect(screen.queryAllByText(/Loading maturity data/i).length).toBe(0);
  });
  await waitFor(() => {
    expect(screen.queryAllByText(/Live API|API Offline/i).length).toBeGreaterThan(0);
  });
};

describe('NIST CSF 2.0 informational page', () => {
  it('renders the hero with the framework heading and both scroll CTAs', async () => {
    renderAppAt('/nist-csf-2-0');

    await waitFor(() => {
      expect(screen.getAllByText('NIST CSF 2.0').length).toBeGreaterThan(0);
    });

    expect(
      screen.getByText(
        /Understand the framework that helps organizations manage, assess, and improve/i
      )
    ).toBeInTheDocument();

    expect(
      screen.getByRole('button', { name: /explore the framework/i })
    ).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /how govern-x helps/i })).toBeInTheDocument();
  });

  it('renders all six Functions with Govern first', async () => {
    renderAppAt('/nist-csf-2-0');

    await waitFor(() => expect(screen.getByText('The Six Functions')).toBeInTheDocument());

    const functions = ['Govern', 'Identify', 'Protect', 'Detect', 'Respond', 'Recover'];
    functions.forEach((name) => {
      expect(screen.getByRole('tab', { name: new RegExp(name, 'i') })).toBeInTheDocument();
    });
  });

  it('updates the detail panel when a different Function is selected', async () => {
    renderAppAt('/nist-csf-2-0');

    await waitFor(() => expect(screen.getByText('The Six Functions')).toBeInTheDocument());

    // The Govern summary also appears in the "What is NIST CSF 2.0?" list,
        // so scope the assertion to the Function detail panel.
        const panel = document.getElementById('fn-panel-govern');
        expect(panel).toHaveTextContent(/Establish and monitor cybersecurity risk management/i);

        fireEvent.click(screen.getByRole('tab', { name: /protect/i }));

        await waitFor(() => {
          const protectPanel = document.getElementById('fn-panel-protect');
          expect(protectPanel).toHaveTextContent(
            /Implement safeguards to manage cybersecurity risks/i
          );
        });
  });

  it('explains that Tiers are not a security score', async () => {
    renderAppAt('/nist-csf-2-0');

    await waitFor(() => expect(screen.getByText('CSF Organizational Tiers')).toBeInTheDocument());

    expect(screen.getByText(/not a security score/i)).toBeInTheDocument();
  });

  it('states that NIST CSF is not a certification', async () => {
    renderAppAt('/nist-csf-2-0');

    await waitFor(() => expect(screen.getByText('Frequently Asked Questions')).toBeInTheDocument());

    fireEvent.click(screen.getByRole('button', { name: /is nist csf 2\.0 a cybersecurity certification/i }));

    await waitFor(() => {
      expect(screen.getByText(/not a certification and not a regulatory mandate/i)).toBeInTheDocument();
    });
  });

  it('labels the example financial figure as illustrative', async () => {
    renderAppAt('/nist-csf-2-0');

    await waitFor(() => expect(screen.getByText('From Finding to Business Risk')).toBeInTheDocument());

    fireEvent.click(screen.getByRole('button', { name: /financial exposure/i }));

    await waitFor(() => expect(screen.getByText('$1.2M')).toBeInTheDocument());
    expect(screen.getByText(/not an actual financial prediction/i)).toBeInTheDocument();
  });

  it('exposes working CTAs back into the existing product', async () => {
    renderAppAt('/nist-csf-2-0');

    await waitFor(() => {
      expect(screen.getByRole('link', { name: /open govern-x dashboard/i })).toHaveAttribute(
        'href',
        '/'
      );
    });

    expect(screen.getByRole('link', { name: /explore risk assessment/i })).toHaveAttribute(
      'href',
      '/financial-risk'
    );
  });

  it('renders the footer with product, framework and disclaimer content', async () => {
    renderAppAt('/nist-csf-2-0');

    await waitFor(() => {
      expect(
        screen.getByText(/Automated NIST CSF 2.0 Compliance & Cyber Risk Quantification Engine/i)
      ).toBeInTheDocument();
    });

    expect(screen.getByText('AXLERO Innovating Solutions')).toBeInTheDocument();

        // The footer disclaimer, distinct from the FAQ answer that also mentions this.
        const footer = document.querySelector('.nist-footer');
        expect(footer).toHaveTextContent(/does not replace/i);
        expect(footer).toHaveTextContent(/qualified cybersecurity professionals/i);
  });

          it('links every NIST footer Framework entry to its Govern-X pillar page', async () => {
        renderAppAt('/nist-csf-2-0');

        await waitFor(() => expect(screen.getByText('Frequently Asked Questions')).toBeInTheDocument());

        const frameworkNav = screen.getByRole('navigation', { name: 'Framework' });
        const expected = [
          ['Govern', '/govern'],
          ['Identify', '/identify'],
          ['Protect', '/protect'],
          ['Detect', '/detect'],
          ['Respond', '/respond'],
          ['Recover', '/recover'],
        ];

        expected.forEach(([name, href]) => {
          const link = within(frameworkNav).getByRole('link', { name });
          expect(link).toHaveAttribute('href', href);
        });
          });

  it('links the new page from the dashboard navigation', async () => {
    renderAppAt('/');

    // The footer also links to this page, so scope to the command bar.
    const commandBar = document.querySelector('.dashboard-command-bar');
    await waitFor(() => {
      expect(commandBar).not.toBeNull();
      expect(
        within(commandBar).getByRole('link', { name: 'NIST CSF 2.0' })
      ).toHaveAttribute('href', '/nist-csf-2-0');
    });

      // The dashboard loads several endpoints on mount; let them settle so no
      // state update lands after the test environment tears down.
      await waitForDashboardSettled();
    });

    it('renders a dashboard footer whose CTA navigates to the NIST CSF 2.0 page', async () => {
      renderAppAt('/');

      await waitFor(() => {
        expect(
          screen.getByRole('link', { name: /explore nist csf 2\.0/i })
        ).toHaveAttribute('href', '/nist-csf-2-0');
      });

      // Footer carries the framework and product navigation plus the disclaimer.
      expect(
        screen.getByText(/Automated NIST CSF 2.0 Compliance & Cyber Risk Quantification Engine/i)
      ).toBeInTheDocument();

      const footer = document.querySelector('.dashboard-footer');
      expect(footer).toHaveTextContent(/does not replace/i);
      expect(footer.querySelector('a[href="/govern"]')).not.toBeNull();
      expect(footer.querySelector('a[href="/financial-risk"]')).not.toBeNull();

      await waitForDashboardSettled();
    });
});