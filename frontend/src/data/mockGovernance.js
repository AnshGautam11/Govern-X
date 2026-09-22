export const mockGovernanceQuestions = [
  { id: 'GV-01', category: 'Govern', question: 'Is cybersecurity governance formally defined?', type: 'yes_no', required: true, weight: 5 },
  { id: 'GV-02', category: 'Govern', question: 'Is there an assigned security leadership role?', type: 'single_select', options: ['Yes', 'Partially', 'No'], required: true, weight: 5 },
  { id: 'GV-03', category: 'Govern', question: 'Are cybersecurity responsibilities documented across the organization?', type: 'yes_no', required: true, weight: 4 },
  { id: 'GV-04', category: 'Govern', question: 'How often are security policies reviewed?', type: 'single_select', options: ['Quarterly', 'Annually', 'Ad hoc', 'Never'], required: true, weight: 4 },
  { id: 'GV-05', category: 'Govern', question: 'Is cybersecurity risk reported to senior management?', type: 'yes_no', required: true, weight: 5 },
  { id: 'GV-06', category: 'Govern', question: 'Rate the maturity of the documented risk management process.', type: 'rating', options: ['Initial', 'Developing', 'Repeatable', 'Adaptive'], required: true, weight: 5 },
  { id: 'GV-07', category: 'Govern', question: 'Are security roles and responsibilities clearly assigned?', type: 'yes_no', required: true, weight: 4 },
  { id: 'GV-08', category: 'Govern', question: 'How are third-party cybersecurity risks governed?', type: 'single_select', options: ['Formal program', 'Tracked informally', 'Not governed'], required: true, weight: 4 },
  { id: 'GV-09', category: 'Govern', question: 'Are security policies reviewed on a defined schedule?', type: 'yes_no', required: true, weight: 3 },
  { id: 'GV-10', category: 'Govern', question: 'Add context or evidence for this assessment item.', type: 'text', required: false, weight: 1 },
];

export const mockGovernanceScore = {
  score: 78,
  answered: 10,
  total: 10,
  tier: 3,
  tierName: 'Repeatable',
};
