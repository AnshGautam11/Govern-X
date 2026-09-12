const API_BASE_URL = (import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      Accept: 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let errorMessage = 'Unable to load security data.';

    try {
      const payload = await response.json();
      errorMessage = payload.detail || payload.error || payload.message || errorMessage;
    } catch {
      // Ignore JSON parsing errors and fall back to the generic message.
    }

    throw new Error(errorMessage);
  }

  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('application/json')) {
    return null;
  }

  const text = await response.text();
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export async function fetchHealthStatus() {
  return apiRequest('/health');
}

export async function fetchMaturityData() {
  return apiRequest('/dashboard/maturity');
}

export async function triggerAssessmentScan() {
  return apiRequest('/scan/aws', { method: 'POST' });
}

export async function fetchScanResults() {
  const payload = await apiRequest('/scan/aws');
  return payload?.results ?? [];
}

export { API_BASE_URL };

export async function fetchScanHistory(limit = 50) {
  const payload = await apiRequest(`/scan/history?limit=${limit}`);
  return payload?.entries ?? [];
}
