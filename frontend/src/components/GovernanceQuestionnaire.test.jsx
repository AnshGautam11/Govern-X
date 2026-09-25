import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import GovernanceQuestionnaire from './GovernanceQuestionnaire';
import * as api from '../lib/api';

const questions = [
  { id: 'risk_owner_assigned', category: 'Govern', question: 'Risk owner assigned?', type: 'yes_no', required: true, weight: 1 },
  { id: 'security_policy_reviewed', category: 'Govern', question: 'Policy reviewed?', type: 'yes_no', required: true, weight: 1 },
];

function renderQuestionnaire() {
  return render(<MemoryRouter><GovernanceQuestionnaire /></MemoryRouter>);
}

describe('GovernanceQuestionnaire', () => {
  it('loads questions and saved answers from the backend and submits active question keys', async () => {
    vi.spyOn(api, 'fetchGovernanceQuestions').mockResolvedValue(questions);
    vi.spyOn(api, 'fetchGovernanceResponses').mockResolvedValue({ responses: [] });
    vi.spyOn(api, 'fetchGovernanceScore').mockResolvedValue({ completion_percentage: 0, score: 0, answered: 0, total: 2, by_function: { GOVERN: 0 } });
    const submit = vi.spyOn(api, 'submitGovernanceAssessment').mockResolvedValue({ status: 'submitted' });

    renderQuestionnaire();

    expect(await screen.findByText('Risk owner assigned?')).toBeInTheDocument();
    fireEvent.click(screen.getByLabelText('Yes'));
    fireEvent.click(screen.getByRole('button', { name: /save & continue/i }));
    fireEvent.click(await screen.findByLabelText('No'));
    api.fetchGovernanceScore.mockResolvedValue({ completion_percentage: 100, score: 50, answered: 2, total: 2, by_function: { GOVERN: 50 } });
    fireEvent.click(screen.getByRole('button', { name: /submit assessment/i }));

    await waitFor(() => expect(submit).toHaveBeenCalledWith({
      risk_owner_assigned: true,
      security_policy_reviewed: false,
    }));
    expect(await screen.findByText('50%')).toBeInTheDocument();
  });
});