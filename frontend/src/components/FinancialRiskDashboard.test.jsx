import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import FinancialRiskDashboard from './FinancialRiskDashboard';
import * as api from '../lib/api';

const liveRisk = {
  status: 'calculated',
  expected_loss: 20000,
  p50: 18000,
  p90: 35000,
  p95: 42000,
  p99: 50000,
  iterations: 10000,
  distribution: [20, 50, 100],
  generated_at: '2026-09-23T12:00:00Z',
  data_quality: 'current_scan_risk_inputs',
  open_findings: 2,
  assets_considered: 3,
};

const unavailableRisk = {
  status: 'unavailable',
  expected_loss: null,
  p50: null,
  p90: null,
  p95: null,
  p99: null,
  iterations: 0,
  distribution: [],
  generated_at: '2026-09-23T12:00:00Z',
  data_quality: 'missing_asset_risk_parameters',
  open_findings: 2,
  assets_considered: 3,
  reason: 'Asset exposure and occurrence parameters are missing.',
};

function renderDashboard() {
  return render(<MemoryRouter><FinancialRiskDashboard /></MemoryRouter>);
}

describe('FinancialRiskDashboard', () => {
  it('renders the backend risk response percentiles without demo fallback data', async () => {
    vi.spyOn(api, 'fetchFinancialRisk').mockResolvedValue(liveRisk);

    renderDashboard();

    await waitFor(() => expect(screen.getByText('Expected annual loss')).toBeInTheDocument());
    expect(screen.getByText('$20.0K')).toBeInTheDocument();
    expect(screen.getByRole('img', { name: /P99 \$50\.0K/i })).toBeInTheDocument();
    expect(screen.getByText(/Data quality: current_scan_risk_inputs/i)).toBeInTheDocument();
  });

  it('states that financial risk is unavailable when risk inputs cannot be joined', async () => {
    vi.spyOn(api, 'fetchFinancialRisk').mockResolvedValue(unavailableRisk);

    renderDashboard();

    await waitFor(() => expect(screen.getByText('Financial risk unavailable')).toBeInTheDocument());
    expect(screen.getByText(/Asset exposure and occurrence parameters are missing/i)).toBeInTheDocument();
    expect(screen.queryByText('$20.0K')).not.toBeInTheDocument();
  });

  it('shows a retryable error state when the API fails', async () => {
    vi.spyOn(api, 'fetchFinancialRisk').mockRejectedValue(new Error('API is offline'));

    renderDashboard();

    await waitFor(() => expect(screen.getByText('Financial risk unavailable')).toBeInTheDocument());
    expect(screen.getByText('API is offline')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retry request/i })).toBeInTheDocument();
  });
});