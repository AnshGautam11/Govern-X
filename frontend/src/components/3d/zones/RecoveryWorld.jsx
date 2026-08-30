import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { RECOVERY_WORLD_DATA } from '../../../data/universeData';
import * as THREE from 'three';

export function RecoveryWorld({ onSelectNode }) {
  const crystalRef = useRef();
  const auraRef = useRef();

  useFrame((state, delta) => {
    if (crystalRef.current) {
      crystalRef.current.rotation.y += delta * 0.25;
      crystalRef.current.rotation.z = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
    }
    if (auraRef.current) {
      auraRef.current.rotation.y -= delta * 0.15;
    }
  });

  return (
    <group position={[840, 5, 10]}>
      {/* Harmonic Rebirth Base Platform */}
      <mesh position={[0, -12, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[18, 20, 2, 32]} />
        <meshStandardMaterial color="#042018" metalness={0.8} roughness={0.2} />
      </mesh>

      {/* Radiant Crystalline Core */}
      <mesh
        ref={crystalRef}
        onClick={(e) => {
          e.stopPropagation();
          onSelectNode?.({
            type: 'recovery_world',
            zone: 'recover',
            title: 'Recovery World Matrix',
            name: 'Resilient Infrastructure Lattice',
            category: 'CONTINUOUS RESILIENCE & RESTORATION',
            pos: [840, 5, 10],
            status: 'SYSTEM RESTORED (100%)',
            score: 79,
            accent: '#34d399',
            summary: `Automated Backups: ${RECOVERY_WORLD_DATA.validatedBackups} | Posture Delta: ${RECOVERY_WORLD_DATA.postureImprovementDelta}`,
            details: `RTO Achieved: ${RECOVERY_WORLD_DATA.rtoActualMinutes} | RPO Achieved: ${RECOVERY_WORLD_DATA.rpoActualSeconds} | All microservices synchronized`,
            route: '/recover',
            pillarName: 'RECOVER',
          });
        }}
      >
        <octahedronGeometry args={[5, 0]} />
        <meshStandardMaterial
          color="#34d399"
          emissive="#10b981"
          emissiveIntensity={1.8}
          roughness={0.1}
          metalness={0.9}
        />
      </mesh>

      {/* Crystalline Lattice Rebuilding Nodes */}
      {[-8, 8, -6, 6].map((x, i) => (
        <mesh key={i} position={[x, -4 + (i % 2) * 4, (i % 2 === 0 ? 6 : -6)]}>
          <boxGeometry args={[1.6, 3.2, 1.6]} />
          <meshStandardMaterial
            color="#6ee7b7"
            emissive="#34d399"
            emissiveIntensity={1.2}
            wireframe
          />
        </mesh>
      ))}

      {/* Healing Energy Rings */}
      <mesh ref={auraRef} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[14, 14.3, 48]} />
        <meshBasicMaterial color="#34d399" transparent opacity={0.65} side={THREE.DoubleSide} />
      </mesh>

      {/* Dynamic Serene Point Light */}
      <pointLight color="#34d399" intensity={5} distance={50} />

      {/* Floating Restoration Banner */}
      <Html position={[0, 14, 0]} center distanceFactor={35} style={{ pointerEvents: 'none' }}>
        <div
          style={{
            background: 'rgba(4, 24, 18, 0.94)',
            border: '1px solid #34d399',
            padding: '8px 18px',
            borderRadius: '8px',
            color: '#ffffff',
            boxShadow: '0 0 24px rgba(52, 211, 153, 0.4)',
            textAlign: 'center',
            fontFamily: 'Inter, system-ui, sans-serif',
          }}
        >
          <div style={{ color: '#6ee7b7', fontWeight: 'bold', fontSize: '12px' }}>
            🌱 RECOVERY WORLD — RESILIENCE RESTORED
          </div>
          <div style={{ color: '#a7f3d0', fontSize: '9px', marginTop: '3px' }}>
            SYSTEM RESTORED • POSTURE IMPROVING (+14%)
          </div>
        </div>
      </Html>
    </group>
  );
}

export default RecoveryWorld;
