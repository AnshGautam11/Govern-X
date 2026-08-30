import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { INCIDENT_STORM_DATA } from '../../../data/universeData';
import * as THREE from 'three';

export function IncidentStorm({ onSelectNode }) {
  const stormCloudRef = useRef();
  const lightningRef = useRef();

  // Procedural dark storm cloud particles
  const stormParticles = useMemo(() => {
    const count = 350;
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2;
      const r = Math.random() * 22 + 4;
      pos[i * 3] = Math.cos(theta) * r;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 14;
      pos[i * 3 + 2] = Math.sin(theta) * r;
    }
    return pos;
  }, []);

  useFrame((state, delta) => {
    if (stormCloudRef.current) {
      stormCloudRef.current.rotation.y += delta * 0.45;
    }
    if (lightningRef.current) {
      lightningRef.current.intensity = Math.random() > 0.92 ? 8 : 1.2;
    }
  });

  return (
    <group position={[720, -30, -70]}>
      {/* Dynamic Lightning Flash */}
      <pointLight ref={lightningRef} color="#fb923c" distance={60} />

      {/* Swirling Dark Incident Vortex */}
      <points ref={stormCloudRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={stormParticles.length / 3}
            array={stormParticles}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={1.6}
          color="#ea580c"
          transparent
          opacity={0.65}
          blending={THREE.AdditiveBlending}
        />
      </points>

      {/* Core Anomaly Entity */}
      <mesh
        onClick={(e) => {
          e.stopPropagation();
          onSelectNode?.({
            type: 'incident_storm',
            zone: 'respond',
            title: 'Incident Storm Lifecycle',
            name: 'Active Anomaly Protocol',
            category: 'INCIDENT RESPONSE ORCHESTRATION',
            pos: [720, -30, -70],
            status: 'CONTAINMENT IN PROGRESS (78%)',
            score: 68,
            accent: '#fb923c',
            summary: `${INCIDENT_STORM_DATA[0].title}. Stage: ${INCIDENT_STORM_DATA[0].stage}`,
            details: `Origin: ${INCIDENT_STORM_DATA[0].origin} | Remediation: ${INCIDENT_STORM_DATA[0].remediation}`,
            route: '/respond',
            pillarName: 'RESPOND',
          });
        }}
      >
        <octahedronGeometry args={[4, 1]} />
        <meshStandardMaterial
          color="#c2410c"
          emissive="#ea580c"
          emissiveIntensity={2.2}
          wireframe
        />
      </mesh>

      {/* Floating Incident Lifecycle HUD */}
      <Html position={[0, 12, 0]} center distanceFactor={35} style={{ pointerEvents: 'none' }}>
        <div
          style={{
            background: 'rgba(20, 10, 5, 0.94)',
            border: '1px solid #ea580c',
            padding: '8px 16px',
            borderRadius: '8px',
            color: '#ffffff',
            boxShadow: '0 0 20px rgba(234, 88, 12, 0.4)',
            textAlign: 'center',
            fontFamily: 'Inter, system-ui, sans-serif',
          }}
        >
          <div style={{ color: '#fb923c', fontWeight: 'bold', fontSize: '11px' }}>
            ⚡ INCIDENT STORM ORCHESTRATION
          </div>
          <div style={{ display: 'flex', gap: '8px', marginTop: '6px', fontSize: '9px' }}>
            <span style={{ color: '#34d399' }}>DETECT ✓</span> →
            <span style={{ color: '#34d399' }}>RESPOND ✓</span> →
            <span style={{ color: '#fb923c', fontWeight: 'bold' }}>CONTAIN (78%)</span> →
            <span style={{ color: '#94a3b8' }}>RECOVER</span>
          </div>
        </div>
      </Html>
    </group>
  );
}

export default IncidentStorm;
