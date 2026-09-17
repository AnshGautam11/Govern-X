import { useMemo, useState } from 'react';
import './FindingsExplorer.css';

const FUNCTIONS = ['ALL FUNCTIONS', 'Govern', 'Identify', 'Protect', 'Detect', 'Respond', 'Recover'];
const SEVERITIES = ['ALL', 'critical', 'high', 'medium', 'low'];

export default function FindingsExplorer({ findings }) {
  const [severity, setSeverity] = useState('ALL');
  const [functionName, setFunctionName] = useState('ALL FUNCTIONS');
  const [status, setStatus] = useState('ALL');
  const [expanded, setExpanded] = useState(null);

  const filteredFindings = useMemo(() => findings.filter((finding) => (
    (severity === 'ALL' || finding.severity === severity)
    && (functionName === 'ALL FUNCTIONS' || finding.mapping?.csf_function === functionName)
    && (status === 'ALL' || finding.status === status)
  )), [findings, functionName, severity, status]);

  return (
    <section className="findings-explorer" aria-label="Security findings explorer">
      <div className="findings-heading">
        <div><span className="overview-label">Evidence register</span><h2>Security findings</h2></div>
        <span className="attention-count">{filteredFindings.length} shown / {findings.length} mapped</span>
      </div>
      <div className="findings-filters">
        <label>Severity<select value={severity} onChange={(event) => setSeverity(event.target.value)}>{SEVERITIES.map((value) => <option key={value}>{value}</option>)}</select></label>
        <label>NIST function<select value={functionName} onChange={(event) => setFunctionName(event.target.value)}>{FUNCTIONS.map((value) => <option key={value}>{value}</option>)}</select></label>
        <label>Status<select value={status} onChange={(event) => setStatus(event.target.value)}><option>ALL</option><option value="pass">pass</option><option value="fail">fail</option><option value="error">error</option></select></label>
      </div>
      <div className="findings-list">
        {filteredFindings.map((finding, index) => {
          const isOpen = expanded === index;
          return (
            <article className={`finding-row ${finding.status}`} key={`${finding.check_id}-${finding.resource_id}-${index}`}>
              <button type="button" className="finding-summary" onClick={() => setExpanded(isOpen ? null : index)} aria-expanded={isOpen}>
                <span><strong>{finding.title}</strong><small>{finding.resource_id}</small></span>
                <span className="finding-tags"><b>{finding.severity?.toUpperCase()}</b><em>{finding.status?.toUpperCase()}</em><i>{isOpen ? '−' : '+'}</i></span>
              </button>
              {isOpen && <div className="finding-detail"><p>{finding.detail}</p><dl><div><dt>NIST function</dt><dd>{finding.mapping?.csf_function || 'Unmapped'}</dd></div><div><dt>Category</dt><dd>{finding.mapping?.csf_subcategory || 'Unavailable'}</dd></div><div><dt>Control</dt><dd>{finding.check_id}</dd></div><div><dt>Recommendation</dt><dd>{finding.mapping?.justification || 'Review the failed control and apply the AWS security baseline.'}</dd></div></dl></div>}
            </article>
          );
        })}
        {filteredFindings.length === 0 && <p className="findings-empty">NO SECURITY FINDINGS DETECTED</p>}
      </div>
    </section>
  );
}
