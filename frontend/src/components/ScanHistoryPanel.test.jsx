import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import ScanHistoryPanel from './ScanHistoryPanel';
import * as api from '../lib/api';

describe('ScanHistoryPanel', () => {
  it('does not crash when fetchScanHistory returns {entries: [...]} shape', async () => {
    vi.spyOn(api, 'fetchScanHistory').mockResolvedValue({
      entries: [
        { id: 1, check_id: 's3_public_access_block', resource_id: 'bucket-a', status: 'pass', scanned_at: '2026-09-21T00:00:00Z' },
      ],
    });

    render(<ScanHistoryPanel limit={20} />);

    await waitFor(() => {
      expect(screen.getByText('s3_public_access_block')).toBeInTheDocument();
    });
  });

  it('shows empty state when entries is missing entirely', async () => {
    vi.spyOn(api, 'fetchScanHistory').mockResolvedValue({});

    render(<ScanHistoryPanel limit={20} />);

    await waitFor(() => {
      expect(screen.getByText(/no scan history/i)).toBeInTheDocument();
    });
  });
});
