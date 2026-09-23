import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import FinancialRiskDashboard from './FinancialRiskDashboard';
import * as api from '../lib/api';

const liveRisk = {
  sector: 'financial',
  p10: 10000,
  expected: 20000,
  p90: 35000,
  iterations: 10000,
  confidence_level: 0.9,
  distribution: [20, 50, 100],
  generated_at: '2026-09-23T12:00:00Z',
  data_quality: 'assumed_sample_data',
  disclaimer: 'Asset values are assumed sample inputs, not real organizational figures.',
};

function renderDashboard() {
  return render(<MemoryRouter><FinancialRiskDashboard /></MemoryRouter>);
}

describe('FinancialRiskDashboard', () => {
  it('renders the backend risk response without demo fallback data', async () => {
    vi.spyOn(api, 'fetchFinancialRisk').mockResolvedValue(liveRisk);

    renderDashboard();

    await waitFor(() => expect(screen.getByText('Total estimated financial risk')).toBeInTheDocument());
    expect(screen.getAllByText('$20.0K')).toHaveLength(2);
    expect(screen.getByText(/assumed sample inputs/i)).toBeInTheDocument();
  });

  it('shows a retryable error state when the API fails', async () => {
    vi.spyOn(api, 'fetchFinancialRisk').mockRejectedValue(new Error('API is offline'));

    renderDashboard();

    await waitFor(() => expect(screen.getByText('Financial risk unavailable')).toBeInTheDocument());
    expect(screen.getByText('API is offline')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retry request/i })).toBeInTheDocument();
  });
});