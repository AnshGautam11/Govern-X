import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export function PortalIntroOverlay({ isVisible, isWarping, onEnterSystem }) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          className="portal-intro-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0, scale: 1.1, filter: 'blur(10px)' }}
          transition={{ duration: 0.8 }}
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '3rem 1.5rem',
            pointerEvents: 'none',
            zIndex: 30,
            background: 'radial-gradient(circle at center, rgba(5, 9, 20, 0.4) 0%, rgba(5, 9, 20, 0.85) 100%)',
          }}
        >
          {/* Header Title */}
          <motion.div
            initial={{ y: -30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.6 }}
            style={{ textAlign: 'center' }}
          >
            <div
              style={{
                display: 'inline-block',
                padding: '4px 14px',
                borderRadius: '999px',
                border: '1px solid rgba(56, 189, 248, 0.4)',
                background: 'rgba(15, 23, 42, 0.8)',
                color: '#38bdf8',
                fontSize: '0.75rem',
                letterSpacing: '0.18em',
                textTransform: 'uppercase',
                marginBottom: '0.8rem',
              }}
            >
              Enterprise Cybersecurity Control Center
            </div>
            <h1
              style={{
                fontSize: 'clamp(2.4rem, 6vw, 4.8rem)',
                fontWeight: 900,
                letterSpacing: '0.12em',
                margin: 0,
                background: 'linear-gradient(135deg, #ffffff 0%, #38bdf8 45%, #7bf1a8 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                textTransform: 'uppercase',
                textShadow: '0 0 40px rgba(56, 189, 248, 0.3)',
              }}
            >
              GovernX
            </h1>
            <p
              style={{
                color: '#94a3b8',
                fontSize: 'clamp(1rem, 2vw, 1.4rem)',
                letterSpacing: '0.2em',
                textTransform: 'uppercase',
                marginTop: '0.4rem',
              }}
            >
              The Security Universe
            </p>
          </motion.div>

          {/* Central Call-to-Action */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.6 }}
            style={{ pointerEvents: 'auto', textAlign: 'center' }}
          >
            <button
              type="button"
              disabled={isWarping}
              onClick={onEnterSystem}
              className="enter-system-btn"
              style={{
                position: 'relative',
                padding: '1.1rem 2.8rem',
                fontSize: '1.1rem',
                fontWeight: '800',
                letterSpacing: '0.16em',
                textTransform: 'uppercase',
                color: '#ffffff',
                background: isWarping
                  ? 'linear-gradient(135deg, #0284c7 0%, #10b981 100%)'
                  : 'linear-gradient(135deg, rgba(2, 132, 199, 0.8) 0%, rgba(16, 185, 129, 0.8) 100%)',
                border: '1px solid rgba(56, 189, 248, 0.6)',
                borderRadius: '999px',
                cursor: isWarping ? 'wait' : 'pointer',
                boxShadow: '0 0 30px rgba(56, 189, 248, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3)',
                transition: 'all 0.3s ease',
              }}
            >
              {isWarping ? 'WARPING INTO UNIVERSE...' : 'ENTER SYSTEM →'}
            </button>
            <div style={{ marginTop: '0.8rem', color: '#64748b', fontSize: '0.75rem', letterSpacing: '0.1em' }}>
              ◉ CYBER GATE ARMED • NIST CSF 2.0 PROTOCOLS LOADED
            </div>
          </motion.div>

          {/* Bottom Security Matrix Topline */}
          <motion.div
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.6 }}
            style={{
              display: 'flex',
              gap: '1.5rem',
              color: '#94a3b8',
              fontSize: '0.75rem',
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
            }}
          >
            <span>● 8 Interactive Zones</span>
            <span>● Live NIST CSF 2.0 Telemetry</span>
            <span>● Continuous Defense Matrix</span>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default PortalIntroOverlay;

