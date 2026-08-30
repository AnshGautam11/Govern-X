import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { Preload, AdaptiveDpr } from '@react-three/drei';
import SceneEnvironment from './SceneEnvironment';
import CameraController from './CameraController';
import EntryPortal from './zones/EntryPortal';
import GovernanceCity from './zones/GovernanceCity';
import AssetOrbit from './zones/AssetOrbit';
import ThreatDNALab from './zones/ThreatDNALab';
import AttackNetwork from './zones/AttackNetwork';
import DefenseWall from './zones/DefenseWall';
import AICore from './zones/AICore';
import IncidentStorm from './zones/IncidentStorm';
import RecoveryWorld from './zones/RecoveryWorld';
import FinalUniverse from './zones/FinalUniverse';

export function UniverseCanvas({
  activeZone,
  selectedNode,
  isWarping,
  onWarpComplete,
  onSelectNode,
  onSelectZone,
}) {
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <Canvas
        camera={{ position: [0, 0, 18], fov: 60, near: 0.1, far: 2500 }}
        gl={{ antialias: true, alpha: false, powerPreference: 'high-performance' }}
        style={{ background: '#030712' }}
      >
        <Suspense fallback={null}>
          <AdaptiveDpr pixelated={false} />
          <SceneEnvironment activeZone={activeZone} />
          <CameraController
            activeZone={activeZone}
            selectedNode={selectedNode}
            isWarping={isWarping}
            onWarpComplete={onWarpComplete}
          />

          {/* All 8 Continuous Spatial Zones in the Security Universe */}
          <EntryPortal isWarping={isWarping} onSelectNode={onSelectNode} />
          <GovernanceCity onSelectNode={onSelectNode} />
          <AssetOrbit onSelectNode={onSelectNode} />
          <ThreatDNALab onSelectNode={onSelectNode} />
          <AttackNetwork onSelectNode={onSelectNode} />
          <DefenseWall onSelectNode={onSelectNode} />
          <AICore onSelectNode={onSelectNode} />
          <IncidentStorm onSelectNode={onSelectNode} />
          <RecoveryWorld onSelectNode={onSelectNode} />
          <FinalUniverse onSelectZone={onSelectZone} />

          <Preload all />
        </Suspense>
      </Canvas>
    </div>
  );
}

export default UniverseCanvas;
