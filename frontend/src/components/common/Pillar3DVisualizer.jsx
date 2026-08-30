import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, AdaptiveDpr } from '@react-three/drei';
import GovernanceCity from '../3d/zones/GovernanceCity';
import AssetOrbit from '../3d/zones/AssetOrbit';
import DefenseWall from '../3d/zones/DefenseWall';
import ThreatDNALab from '../3d/zones/ThreatDNALab';
import AttackNetwork from '../3d/zones/AttackNetwork';
import RecoveryWorld from '../3d/zones/RecoveryWorld';

export function Pillar3DVisualizer({ pillarSlug }) {
  const getZoneComponent = () => {
    switch (pillarSlug) {
      case 'govern':
        return (
          <group position={[0, -2, 0]}>
            <GovernanceCity />
          </group>
        );
      case 'identify':
        return (
          <group position={[-120, -20, 70]}>
            <AssetOrbit />
          </group>
        );
      case 'protect':
        return (
          <group position={[-480, 0, 0]}>
            <DefenseWall />
          </group>
        );
      case 'detect':
        return (
          <group position={[-240, 20, -10]}>
            <ThreatDNALab />
          </group>
        );
      case 'respond':
        return (
          <group position={[-360, -15, 55]}>
            <AttackNetwork />
          </group>
        );
      case 'recover':
        return (
          <group position={[-840, -5, -10]}>
            <RecoveryWorld />
          </group>
        );
      default:
        return <GovernanceCity />;
    }
  };

  const getCameraPosition = () => {
    switch (pillarSlug) {
      case 'govern':
        return [0, 22, 42];
      case 'identify':
        return [0, 20, 48];
      case 'protect':
        return [0, 5, 42];
      case 'detect':
        return [0, 0, 36];
      case 'respond':
        return [0, 18, 38];
      case 'recover':
        return [0, 12, 34];
      default:
        return [0, 20, 40];
    }
  };

  return (
    <div className="pillar-3d-visualizer-container">
      <Canvas
        camera={{ position: getCameraPosition(), fov: 50 }}
        gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
      >
        <Suspense fallback={null}>
          <AdaptiveDpr pixelated={false} />
          <ambientLight intensity={0.6} color="#0f172a" />
          <directionalLight position={[30, 40, 20]} intensity={1.5} color="#38bdf8" />
          <pointLight position={[0, 10, 0]} intensity={2.5} distance={60} color="#38bdf8" />

          {getZoneComponent()}

          <OrbitControls
            enableDamping
            dampingFactor={0.06}
            enablePan={false}
            minDistance={15}
            maxDistance={90}
            maxPolarAngle={Math.PI / 2 + 0.1}
          />
        </Suspense>
      </Canvas>
      <div className="visualizer-hint">
        <span>◉ Interactive 3D Spatial Zone • Drag to rotate / Scroll to zoom</span>
      </div>
    </div>
  );
}

export default Pillar3DVisualizer;

