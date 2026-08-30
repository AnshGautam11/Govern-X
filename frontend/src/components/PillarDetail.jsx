import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { getPillarBySlug } from '../data/pillarData';
import PillarPageLayout from './common/PillarPageLayout';
import GlassCard from './common/GlassCard';
import ControlCard from './common/ControlCard';
import FindingCard from './common/FindingCard';
import StatusBadge from './common/StatusBadge';

export function PillarDetail() {
  const location = useLocation();
  const slug = location.pathname.replace('/', '');
  const pillar = getPillarBySlug(slug);

  if (!pillar) {
    return (
      <div className="pillar-not-found-page">
        <div className="not-found-card">
          <h2>Pillar Not Found</h2>
          <p>The requested cybersecurity pillar does not exist.</p>
          <Link to="/" className="back-to-universe-button">← Return to Universe</Link>
        </div>
      </div>
    );
  }

  return (
    <PillarPageLayout pillar={pillar}>
      {/* Domain Specific Layouts */}
      {slug === 'govern' && (
        <div className="pillar-domain-grid">
          {/* Policy Catalog */}
          <GlassCard
            title="Strategic Policies & Standards"
            subtitle="GOVERNANCE POLICY HIERARCHY"
            accentColor={pillar.accentColor}
            badge={<StatusBadge status="92% Enforced" tone="good" />}
          >
            <div className="table-responsive">
              <table className="cyber-table">
                <thead>
                  <tr>
                    <th>Policy Standard</th>
                    <th>Owner</th>
                    <th>Version</th>
                    <th>Review</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {pillar.sections.policies.map((pol) => (
                    <tr key={pol.id}>
                      <td><strong>{pol.name}</strong></td>
                      <td>{pol.owner}</td>
                      <td><code>{pol.version}</code></td>
                      <td>{pol.reviewDate}</td>
                      <td><StatusBadge status={pol.status} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </GlassCard>

          {/* Controls Matrix */}
          <GlassCard
            title="NIST CSF 2.0 Governance Controls"
            subtitle="OVERSIGHT & ACCOUNTABILITY"
            accentColor={pillar.accentColor}
          >
            <div className="controls-grid">
              {pillar.sections.controlsList.map((ctrl) => (
                <ControlCard key={ctrl.code} {...ctrl} />
              ))}
            </div>
          </GlassCard>
        </div>
      )}

      {slug === 'identify' && (
        <div className="pillar-domain-grid">
          {/* Asset Categories */}
          <GlassCard
            title="Asset Inventory & Criticality Breakdown"
            subtitle="WORKLOAD & REPOSITORY MAP"
            accentColor={pillar.accentColor}
            badge={<StatusBadge status="142 Inventoried" tone="good" />}
          >
            <div className="table-responsive">
              <table className="cyber-table">
                <thead>
                  <tr>
                    <th>Workload Category</th>
                    <th>Active Nodes</th>
                    <th>Risk Level</th>
                    <th>Compliance</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {pillar.sections.assetCategories.map((cat, i) => (
                    <tr key={i}>
                      <td><strong>{cat.category}</strong></td>
                      <td>{cat.count} endpoints</td>
                      <td><span style={{ color: cat.risk === 'High' ? '#f87171' : cat.risk === 'Moderate' ? '#fbbf24' : '#34d399' }}>{cat.risk}</span></td>
                      <td><strong>{cat.compliance}%</strong></td>
                      <td><StatusBadge status={cat.status} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </GlassCard>

          {/* Controls Matrix */}
          <GlassCard
            title="Asset Identification Controls"
            subtitle="VISIBILITY & ATTACK SURFACE"
            accentColor={pillar.accentColor}
          >
            <div className="controls-grid">
              {pillar.sections.controlsList.map((ctrl) => (
                <ControlCard key={ctrl.code} {...ctrl} />
              ))}
            </div>
          </GlassCard>
        </div>
      )}

      {slug === 'protect' && (
        <div className="pillar-domain-grid">
          {/* Defense Layers */}
          <GlassCard
            title="Protective Safeguards & Defense Infrastructure"
            subtitle="ACCESS, ENCRYPTION & WAF"
            accentColor={pillar.accentColor}
            badge={<StatusBadge status="98.4% Shield" tone="good" />}
          >
            <div className="table-responsive">
              <table className="cyber-table">
                <thead>
                  <tr>
                    <th>Protective Layer</th>
                    <th>Throughput / Load</th>
                    <th>Filtering Efficiency</th>
                    <th>Operational Health</th>
                  </tr>
                </thead>
                <tbody>
                  {pillar.sections.defenseLayers.map((layer, i) => (
                    <tr key={i}>
                      <td><strong>{layer.name}</strong></td>
                      <td><code>{layer.throughput}</code></td>
                      <td><strong>{layer.efficiency}</strong></td>
                      <td><StatusBadge status={layer.status} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </GlassCard>

          {/* Controls Matrix */}
          <GlassCard
            title="Protective Safeguard Controls"
            subtitle="IDENTITY & ACCESS SAFEGUARDS"
            accentColor={pillar.accentColor}
          >
            <div className="controls-grid">
              {pillar.sections.controlsList.map((ctrl) => (
                <ControlCard key={ctrl.code} {...ctrl} />
              ))}
            </div>
          </GlassCard>
        </div>
      )}

      {slug === 'detect' && (
        <div className="pillar-domain-grid">
          {/* Threat Signatures */}
          <GlassCard
            title="Detected Threat Signatures & CVE Correlations"
            subtitle="CONTINUOUS THREAT SURFACE SIGNALS"
            accentColor={pillar.accentColor}
            badge={<StatusBadge status="4,820 Signatures" tone="good" />}
          >
            <div className="table-responsive">
              <table className="cyber-table">
                <thead>
                  <tr>
                    <th>Threat Name</th>
                    <th>CVE / CWE</th>
                    <th>Attack Vector</th>
                    <th>Severity</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {pillar.sections.threatSignatures.map((th, i) => (
                    <tr key={i}>
                      <td><strong>{th.threat}</strong></td>
                      <td><code>{th.cve}</code></td>
                      <td>{th.vector}</td>
                      <td><StatusBadge status={th.severity} tone={th.severity === 'Critical' ? 'critical' : 'attention'} /></td>
                      <td><StatusBadge status={th.status} tone="good" /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </GlassCard>

          {/* Controls Matrix */}
          <GlassCard
            title="Detection Controls & SIEM Integration"
            subtitle="ANOMALY MONITORING"
            accentColor={pillar.accentColor}
          >
            <div className="controls-grid">
              {pillar.sections.controlsList.map((ctrl) => (
                <ControlCard key={ctrl.code} {...ctrl} />
              ))}
            </div>
          </GlassCard>
        </div>
      )}

      {slug === 'respond' && (
        <div className="pillar-domain-grid">
          {/* Incident Timeline */}
          <GlassCard
            title="Active Incident Lifecycle Timeline"
            subtitle="ORCHESTRATION & CONTAINMENT"
            accentColor={pillar.accentColor}
            badge={<StatusBadge status="Stage: CONTAIN (78%)" tone="attention" />}
          >
            <div className="incident-timeline-list">
              {pillar.sections.incidentTimeline.map((item, idx) => (
                <div key={idx} className="timeline-row">
                  <div className="timeline-badge-col">
                    <span className="timeline-stage-tag">{item.stage}</span>
                    <span className="timeline-time">{item.time}</span>
                  </div>
                  <div className="timeline-detail-col">
                    <strong className="timeline-title">{item.title}</strong>
                    <p className="timeline-desc">{item.detail}</p>
                  </div>
                  <div className="timeline-status-col">
                    <StatusBadge status={item.status} tone={item.status.includes('Prog') ? 'attention' : item.status.includes('Comp') ? 'good' : 'neutral'} />
                  </div>
                </div>
              ))}
            </div>
          </GlassCard>

          {/* Controls Matrix */}
          <GlassCard
            title="Incident Response Controls"
            subtitle="PLAYBOOK EXECUTION"
            accentColor={pillar.accentColor}
          >
            <div className="controls-grid">
              {pillar.sections.controlsList.map((ctrl) => (
                <ControlCard key={ctrl.code} {...ctrl} />
              ))}
            </div>
          </GlassCard>
        </div>
      )}

      {slug === 'recover' && (
        <div className="pillar-domain-grid">
          {/* Restoration Catalog */}
          <GlassCard
            title="System Restoration & Resiliency Catalog"
            subtitle="BACKUP RECONSTITUTION & RTO/RPO"
            accentColor={pillar.accentColor}
            badge={<StatusBadge status="100% Backups Validated" tone="good" />}
          >
            <div className="table-responsive">
              <table className="cyber-table">
                <thead>
                  <tr>
                    <th>Critical System</th>
                    <th>Achieved RTO</th>
                    <th>Achieved RPO</th>
                    <th>Backup Mechanism</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {pillar.sections.restorationCatalog.map((sys, i) => (
                    <tr key={i}>
                      <td><strong>{sys.system}</strong></td>
                      <td><code>{sys.rto}</code></td>
                      <td><code>{sys.rpo}</code></td>
                      <td>{sys.backupType}</td>
                      <td><StatusBadge status={sys.status} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </GlassCard>

          {/* Controls Matrix */}
          <GlassCard
            title="Disaster Recovery & Continuity Controls"
            subtitle="RESILIENCE ORCHESTRATION"
            accentColor={pillar.accentColor}
          >
            <div className="controls-grid">
              {pillar.sections.controlsList.map((ctrl) => (
                <ControlCard key={ctrl.code} {...ctrl} />
              ))}
            </div>
          </GlassCard>
        </div>
      )}

      {/* Priority Findings & Action Items for Every Pillar */}
      <GlassCard
        title="Priority Findings & Actionable Remediations"
        subtitle="AUDITED FINDINGS REGISTER"
        accentColor={pillar.accentColor}
        className="findings-section-card"
      >
        <div className="findings-list">
          {pillar.findings.map((finding, idx) => (
            <FindingCard key={idx} finding={finding} index={idx} />
          ))}
        </div>
      </GlassCard>
    </PillarPageLayout>
  );
}

export default PillarDetail;
