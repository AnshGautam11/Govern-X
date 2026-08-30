import React from 'react';

export function GlassCard({
  children,
  title,
  subtitle,
  badge,
  action,
  accentColor = '#38bdf8',
  className = '',
  style = {},
}) {
  return (
    <article
      className={`glass-card-root ${className}`}
      style={{
        '--card-accent': accentColor,
        ...style,
      }}
    >
      {(title || subtitle || badge || action) && (
        <div className="glass-card-header">
          <div>
            {subtitle && <span className="glass-card-subtitle">{subtitle}</span>}
            {title && <h3 className="glass-card-title">{title}</h3>}
          </div>
          <div className="glass-card-header-actions">
            {badge && <span>{badge}</span>}
            {action && <div>{action}</div>}
          </div>
        </div>
      )}
      <div className="glass-card-body">{children}</div>
    </article>
  );
}

export default GlassCard;

