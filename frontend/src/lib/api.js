export const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

async function apiRequest(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: { Accept: 'application/json', ...(options.headers || {}) },
      ...options,
    });
  } catch {
    throw new Error('Unable to communicate with the Govern-X API. Check the backend status and API URL.');
  }

  if (!response.ok) {
    let detail = '';
    try {
      const payload = await response.json();
      detail = payload.detail || payload.error || payload.message || '';
    } catch {
      // Keep the user-facing message stable when an upstream error is not JSON.
    }
    throw new Error(detail || `Govern-X API request failed (${response.status}).`);
  }

  if (!(response.headers.get('content-type') || '').includes('application/json')) return null;
  return response.json();
}

export const fetchHealthStatus = () => apiRequest('/health');
export const fetchMaturityData = () => apiRequest('/dashboard/maturity');
export const triggerAssessmentScan = () => apiRequest('/scan/aws', { method: 'POST' });
export const fetchScanHistory = (limit = 20) => apiRequest(`/scan/history?limit=${limit}`);
export const fetchGovernanceQuestions = () => apiRequest('/governance/questions');
export const submitGovernanceAssessment = (answers) => apiRequest('/governance/assessment', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ answers }),
});
export const fetchFinancialRisk = (sector = 'financial') => apiRequest('/risk/assess', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ sector }),
}).then((payload) => {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    throw new Error('The financial risk API returned an invalid response.');
  }
  return payload;
});

export function normalizeScanResponse(payload) {
  const results = payload?.results || [];
  const findings = (payload?.findings || []).map((finding) => ({
    ...finding.result,
    mapping: finding.mapping,
    title: finding.result?.check_id?.replace(/^check_/, '').replaceAll('_', ' ') || 'Security check',
  }));
  const scores = payload?.scores || payload?.pillar_scores || {};
  const categories = ['Govern', 'Identify', 'Protect', 'Detect', 'Respond', 'Recover'].reduce((all, name) => {
    all[name] = findings.filter((finding) => finding.mapping?.csf_function === name);
    return all;
  }, {});

  return {
    summary: {
      totalChecks: results.length,
      passed: results.filter((result) => result.status === 'pass').length,
      failed: results.filter((result) => result.status === 'fail').length,
      errors: results.filter((result) => result.status === 'error').length,
      complianceScore: payload?.overall_score ?? payload?.overall?.score ?? null,
      maturityScore: payload?.overall_score ?? payload?.overall?.score ?? null,
      tier: payload?.overall_tier ?? null,
      tierName: payload?.tier_name || payload?.overall?.tier || 'No Data',
    },
    findings,
    results,
    categories,
    scores,
    assets: [],
    scanMetadata: { timestamp: payload?.timestamp, environment: payload?.environment || null },
    raw: payload,
  };
}

export function normalizeMaturityResponse(payload) {
  const pillars = payload?.pillars || [];
  const overall = payload?.overall || {};
  return {
    summary: {
      totalChecks: null,
      passed: null,
      failed: null,
      errors: null,
      complianceScore: overall.percentage ?? null,
      maturityScore: overall.percentage ?? null,
      tier: overall.tier ?? null,
      tierName: overall.tier_name || 'No Data',
    },
    findings: [],
    results: [],
    categories: {},
    scores: Object.fromEntries(pillars.map((pillar) => [pillar.function, { score: pillar.percentage, tier: pillar.tier }])),
    assets: [],
    scanMetadata: { timestamp: null, environment: payload?.environment || null },
    raw: payload,
  };
}
