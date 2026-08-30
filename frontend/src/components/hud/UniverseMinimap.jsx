import React from 'react';
import { UNIVERSE_ZONES } from '../../data/universeData';

export function UniverseMinimap({ activeZone, onSelectZone }) {
  return (
    <div className="universe-minimap">
      <div className="minimap-header">
        <span className="minimap-dot" />
        <span className="minimap-title">SPATIAL RADAR</span>
      </div>
      <div className="minimap-radar-circle">
        <div className="radar-sweep" />
        {UNIVERSE_ZONES.map((zone) => {
          const isActive = zone.id === activeZone?.id;
          // Calculate relative normalized 2D projection
          const [tx, , tz] = zone.cameraTarget;
          const leftPercent = 50 + (tx - 420) / 10;
          const topPercent = 50 + tz / 2.5;

          return (
            <button
              key={zone.id}
              type="button"
              onClick={() => onSelectZone(zone.id)}
              className={`minimap-node ${isActive ? 'is-active' : ''}`}
              style={{
                left: `${Math.max(10, Math.min(90, leftPercent))}%`,
                top: `${Math.max(10, Math.min(90, topPercent))}%`,
                '--zone-color': zone.color,
              }}
              title={`Jump to ${zone.name}`}
            />
          );
        })}
      </div>
    </div>
  );
}

export default UniverseMinimap;

