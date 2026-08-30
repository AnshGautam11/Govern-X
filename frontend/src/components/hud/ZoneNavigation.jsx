import React, { useEffect } from 'react';
import { UNIVERSE_ZONES } from '../../data/universeData';

export function ZoneNavigation({
  activeZone,
  onSelectZone,
  isTouring,
  onToggleTour,
}) {
  const currentIndex = UNIVERSE_ZONES.findIndex((z) => z.id === activeZone?.id);

  const handlePrev = () => {
    const prevIndex = (currentIndex - 1 + UNIVERSE_ZONES.length) % UNIVERSE_ZONES.length;
    onSelectZone(UNIVERSE_ZONES[prevIndex].id);
  };

  const handleNext = () => {
    const nextIndex = (currentIndex + 1) % UNIVERSE_ZONES.length;
    onSelectZone(UNIVERSE_ZONES[nextIndex].id);
  };

  // Tour mode timer
  useEffect(() => {
    if (!isTouring) return;
    const interval = setInterval(() => {
      const nextIdx = (currentIndex + 1) % UNIVERSE_ZONES.length;
      onSelectZone(UNIVERSE_ZONES[nextIdx].id);
    }, 6500);
    return () => clearInterval(interval);
  }, [isTouring, currentIndex, onSelectZone]);

  return (
    <div className="zone-navigation-container">
      {/* Top Quick Zone Switcher Strip */}
      <div className="zone-pill-strip">
        {UNIVERSE_ZONES.map((zone) => {
          const isActive = zone.id === activeZone?.id;
          return (
            <button
              key={zone.id}
              type="button"
              onClick={() => onSelectZone(zone.id)}
              className={`zone-pill-item ${isActive ? 'is-active' : ''}`}
              style={{
                '--zone-color': zone.color,
              }}
              title={zone.name}
              aria-label={`Open ${zone.name} zone`}
            >
              <span className="zone-pill-number">{zone.zoneNumber}</span>
              <span className="zone-pill-label">{zone.name}</span>
            </button>
          );
        })}
      </div>

      {/* Main Zone Navigation Controller Bar */}
      <div className="zone-nav-bar">
        <div className="zone-meta-block">
          <div className="zone-tag">
            <span className="zone-tag-num">ZONE {activeZone?.zoneNumber || '00'}</span>
            {activeZone?.pillarName && (
              <span className="zone-pillar-badge" style={{ color: activeZone.color, borderColor: `${activeZone.color}44` }}>
                {activeZone.pillarName}
              </span>
            )}
          </div>
          <div className="zone-title-row">
            <h3 className="zone-current-name" style={{ color: activeZone?.color || '#38bdf8' }}>
              {activeZone?.name}
            </h3>
            <span className="zone-subtitle">{activeZone?.subtitle}</span>
          </div>
        </div>

        {/* Controls */}
        <div className="zone-control-buttons">
          <button
            type="button"
            className="zone-nav-btn"
            onClick={handlePrev}
            title="Previous Zone"
            aria-label="Previous Zone"
          >
            ← PREV
          </button>

          <button
            type="button"
            className={`zone-tour-btn ${isTouring ? 'is-touring' : ''}`}
            onClick={onToggleTour}
            title="Toggle Automated Universe Cinematic Tour"
            aria-label="Toggle Auto Tour"
          >
            {isTouring ? '⏸ PAUSE TOUR' : '▶ AUTO TOUR'}
          </button>

          <button
            type="button"
            className="zone-nav-btn"
            onClick={handleNext}
            title="Next Zone"
            aria-label="Next Zone"
          >
            NEXT →
          </button>
        </div>
      </div>
    </div>
  );
}

export default ZoneNavigation;

