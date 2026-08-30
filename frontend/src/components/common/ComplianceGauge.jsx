import React from 'react';

export function ComplianceGauge({ score, accentColor = '#38bdf8', size = 110, label = 'Score' }) {
  const strokeWidth = 8;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="compliance-gauge-root" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="gauge-svg">
        {/* Track Background */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(30, 41, 59, 0.6)"
          strokeWidth={strokeWidth}
        />
        {/* Progress Arc */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={accentColor}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{
            transformOrigin: 'center',
            transform: 'rotate(-90deg)',
            transition: 'stroke-dashoffset 1s ease',
            filter: `drop-shadow(0 0 6px ${accentColor}88)`,
          }}
        />
      </svg>
      <div className="gauge-content">
        <strong style={{ color: '#ffffff' }}>{score}%</strong>
        <span style={{ color: accentColor }}>{label}</span>
      </div>
    </div>
  );
}

export default ComplianceGauge;

