import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { DEFENSE_WALL_DATA } from '../../../data/universeData';
import * as THREE from 'three';

function ThreatParticleStream() {
  const threatsRef = useRef();

  // Create stream of incoming threat packets
  const threats = useMemo(() => {
    return Array.from({ length: 16 }, (_, i) => ({
      id: i,
      x: (Math.random() - 0.5) * 24,
      y: (Math.random() - 0.5) * 14,
      speed: 4 + Math.random() * 5,
      type: i % 3 === 0 ? 'BLOCKED' : i % 3 === 1 ? 'DETECTED' : 'ALLOWED',
      color: i % 3 === 0 ? '#f87171' : i % 3 === 1 ? '#fbbf24' : '#10b981',
      offset: (i / 16) * 30,
    }));
  }, []);

  useFrame((state) => {
    if (threatsRef.current) {
      threatsRef.current.children.forEach((child, idx) => {
        const item = threats[idx];
        const travelZ = ((state.clock.elapsedTime * item.speed + item.offset) % 35) - 20;

        // When packet reaches wall (z = 0)
        if (item.type === 'BLOCKED' && travelZ > 0) {
          child.position.set(item.x, item.y, -20);
        } else {
          child.position.set(item.x, item.y, travelZ);
        }
      });
    }
  });

  return (
    <group ref={threatsRef}>
      {threats.map((th) => (
        <mesh key={th.id}>
          <sphereGeometry args={[0.35, 8, 8]} />
          <meshBasicMaterial color={th.color} />
        </mesh>
      ))}
    </group>
  );
}

export function DefenseWall({ onSelectNode }) {
  const shieldRef = useRef();

  useFrame((state) => {
    if (shieldRef.current) {
      shieldRef.current.material.opacity = 0.5 + Math.sin(state.clock.elapsedTime * 2) * 0.15;
    }
  });

  return (
    <group position={[480, 0, 0]}>
      {/* Massive Hexagonal Energy Wall Shield */}
      <mesh
        ref={shieldRef}
        position={[0, 0, 0]}
        onClick={(e) => {
          e.stopPropagation();
          onSelectNode?.({
            type: 'defense_wall',
            zone: 'protect',
            title: 'Firewall Defense Matrix',
            name: 'Active Fortress Shield',
            category: 'PERIMETER DEFENSE',
            pos: [480, 0, 0],
            status: '98.4% INTEGRITY (ACTIVE FILTERING)',
            score: 88,
            accent: '#10b981',
            summary: `Active throughput: ${DEFENSE_WALL_DATA.throughputGbps} Gbps | Analyzed Today: ${DEFENSE_WALL_DATA.threatsAnalyzedToday.toLocaleString()} threats`,
            details: `Enforced Rules: ${DEFENSE_WALL_DATA.rulesEnforced} | Status: BLOCKED / DETECTED / ALLOWED realtime stream active`,
            route: '/protect',
            pillarName: 'PROTECT',
          });
        }}
      >
        <planeGeometry args={[32, 18, 16, 16]} />
        <meshStandardMaterial
          color="#10b981"
          emissive="#047857"
          emissiveIntensity={0.8}
          transparent
          opacity={0.6}
          wireframe
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Solid Inner Glow Plane */}
      <mesh position={[0, 0, -0.1]}>
        <planeGeometry args={[31.8, 17.8]} />
        <meshBasicMaterial
          color="#064e3b"
          transparent
          opacity={0.35}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Wall Perimeter Defense Towers */}
      <mesh position={[-16.5, 0, 0]}>
        <cylinderGeometry args={[0.8, 1.2, 20, 16]} />
        <meshStandardMaterial color="#0b1020" metalness={0.9} roughness={0.1} />
      </mesh>
      <mesh position={[16.5, 0, 0]}>
        <cylinderGeometry args={[0.8, 1.2, 20, 16]} />
        <meshStandardMaterial color="#0b1020" metalness={0.9} roughness={0.1} />
      </mesh>

      {/* Floating Defense HUD Banner */}
      <Html
        position={[0, 11, 0]}
        center
        distanceFactor={35}
        style={{ pointerEvents: 'none' }}
      >
        <div
          style={{
            background: 'rgba(6, 20, 18, 0.94)',
            border: '1px solid #10b981',
            padding: '6px 16px',
            borderRadius: '8px',
            color: '#ffffff',
            fontSize: '11px',
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
            textAlign: 'center',
            boxShadow: '0 0 20px rgba(16, 185, 129, 0.35)',
            fontFamily: 'Inter, system-ui, sans-serif',
          }}
        >
          <div style={{ color: '#34d399', fontWeight: 'bold', fontSize: '12px' }}>
            🛡️ FIREWALL DEFENSE SYSTEM
          </div>
          <div style={{ fontSize: '9px', color: '#a7f3d0', marginTop: '2px' }}>
            SHIELD INTEGRITY: 98.4% | THROUGHPUT: 42.8 GBPS
          </div>
        </div>
      </Html>

      {/* Live Incoming Threat Analysis Stream */}
      <ThreatParticleStream />
    </group>
  );
}

export default DefenseWall;
