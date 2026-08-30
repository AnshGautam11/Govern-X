import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export function TelemetryDrawer({ selectedNode, onClose }) {
  const navigate = useNavigate();

  if (!selectedNode) return null;

  return (
    <AnimatePresence>
      <motion.div
        className="telemetry-drawer-backdrop"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
        style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(5, 9, 20, 0.4)',
          backdropFilter: 'blur(4px)',
          zIndex: 45,
        }}
      >
        <motion.aside
          className="telemetry-drawer"
          initial={{ x: '100%', opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: '100%', opacity: 0 }}
          transition={{ type: 'spring', damping: 25, stiffness: 220 }}
          onClick={(e) => e.stopPropagation()}
          style={{
            position: 'absolute',
            top: 0,
            right: 0,
            bottom: 0,
            width: 'min(440px, 92vw)',
            background: 'linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(9, 14, 26, 0.98) 100%)',
            borderLeft: `1px solid ${selectedNode.accent || 'rgba(56, 189, 248, 0.3)'}`,
            boxShadow: `-12px 0 40px rgba(3, 7, 18, 0.6), 0 0 20px ${selectedNode.accent || '#38bdf8'}33`,
            padding: '2rem 1.6rem',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            overflowY: 'auto',
          }}
        >
          {/* Top Bar */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span
                  style={{
                    display: 'inline-block',
                    width: '8px',
                    height: '8px',
                    borderRadius: '50%',
                    background: selectedNode.accent || '#38bdf8',
                    boxShadow: `0 0 10px ${selectedNode.accent || '#38bdf8'}`,
                  }}
                />
                <span
                  style={{
                    fontSize: '0.72rem',
                    letterSpacing: '0.14em',
                    textTransform: 'uppercase',
                    color: selectedNode.accent || '#38bdf8',
                    fontWeight: 700,
                  }}
                >
                  {selectedNode.category || selectedNode.type?.toUpperCase() || 'TELEMETRY'}
                </span>
              </div>
              <button
                type="button"
                onClick={onClose}
                style={{
                  background: 'rgba(255, 255, 255, 0.06)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  color: '#94a3b8',
                  borderRadius: '8px',
                  width: '32px',
                  height: '32px',
                  display: 'grid',
                  placeItems: 'center',
                  cursor: 'pointer',
                  fontSize: '14px',
                }}
              >
                ✕
              </button>
            </div>

            <h2 style={{ fontSize: '1.4rem', color: '#f8fafc', margin: '0 0 0.8rem', lineHeight: 1.3 }}>
              {selectedNode.title || selectedNode.name}
            </h2>

            {/* Score / Status Strip */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: selectedNode.score ? '1fr 1fr' : '1fr',
                gap: '0.8rem',
                margin: '1.2rem 0',
              }}
            >
              {selectedNode.score !== undefined && (
                <div
                  style={{
                    padding: '0.8rem',
                    borderRadius: '12px',
                    background: 'rgba(30, 41, 59, 0.6)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                  }}
                >
                  <div style={{ fontSize: '0.68rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                    Compliance Score
                  </div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 800, color: selectedNode.accent || '#38bdf8', marginTop: '2px' }}>
                    {selectedNode.score}%
                  </div>
                </div>
              )}

              <div
                style={{
                  padding: '0.8rem',
                  borderRadius: '12px',
                  background: 'rgba(30, 41, 59, 0.6)',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                }}
              >
                <div style={{ fontSize: '0.68rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                  Operational Status
                </div>
                <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f8fafc', marginTop: '4px' }}>
                  {selectedNode.status || 'Active'}
                </div>
              </div>
            </div>

            {/* Summary */}
            <div style={{ margin: '1.2rem 0' }}>
              <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '0.4rem' }}>
                Operational Summary
              </div>
              <p style={{ color: '#cbd5e1', fontSize: '0.92rem', lineHeight: 1.6 }}>
                {selectedNode.summary || selectedNode.details}
              </p>
            </div>

            {/* Findings if present */}
            {selectedNode.findings && selectedNode.findings.length > 0 && (
              <div style={{ margin: '1.2rem 0' }}>
                <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '0.6rem' }}>
                  Control Findings & Review
                </div>
                <ul style={{ margin: 0, paddingLeft: '1.2rem', color: '#cbd5e1', fontSize: '0.88rem', lineHeight: 1.6 }}>
                  {selectedNode.findings.map((f, i) => (
                    <li key={i} style={{ marginBottom: '0.4rem' }}>{f}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Bottom Actions */}
          <div style={{ marginTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
            {selectedNode.route && (
              <button
                type="button"
                onClick={() => navigate(selectedNode.route)}
                style={{
                  width: '100%',
                  padding: '0.9rem',
                  borderRadius: '10px',
                  background: `linear-gradient(135deg, ${selectedNode.accent || '#38bdf8'}33, rgba(15, 23, 42, 0.8))`,
                  border: `1px solid ${selectedNode.accent || '#38bdf8'}`,
                  color: '#ffffff',
                  fontWeight: 700,
                  fontSize: '0.9rem',
                  letterSpacing: '0.08em',
                  textTransform: 'uppercase',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  boxShadow: `0 0 16px ${selectedNode.accent || '#38bdf8'}44`,
                }}
              >
                <span>Open {selectedNode.pillarName || 'Pillar'} CSF View</span>
                <span>→</span>
              </button>
            )}

            <button
              type="button"
              onClick={onClose}
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '10px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                color: '#94a3b8',
                fontWeight: 600,
                fontSize: '0.85rem',
                cursor: 'pointer',
              }}
            >
              Close Telemetry Panel
            </button>
          </div>
        </motion.aside>
      </motion.div>
    </AnimatePresence>
  );
}

export default TelemetryDrawer;

