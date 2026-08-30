import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export function EntryPortal({ isWarping, onSelectNode }) {
  const outerRingRef = useRef();
  const innerRingRef = useRef();
  const coreRef = useRef();
  const particlesRef = useRef();

  // Orbital glyph/energy particles around portal
  const particlePositions = useMemo(() => {
    const count = 180;
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2;
      const radius = 5.2 + Math.random() * 2.4;
      pos[i * 3] = Math.cos(angle) * radius;
      pos[i * 3 + 1] = Math.sin(angle) * radius;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 2;
    }
    return pos;
  }, []);

  useFrame((state, delta) => {
    const speedMultiplier = isWarping ? 8.0 : 1.0;
    if (outerRingRef.current) {
      outerRingRef.current.rotation.z += delta * 0.4 * speedMultiplier;
      outerRingRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.6) * 0.1;
    }
    if (innerRingRef.current) {
      innerRingRef.current.rotation.z -= delta * 0.7 * speedMultiplier;
      innerRingRef.current.rotation.y = Math.cos(state.clock.elapsedTime * 0.8) * 0.15;
    }
    if (coreRef.current) {
      const pulse = Math.sin(state.clock.elapsedTime * (isWarping ? 12 : 3)) * 0.08 + 1;
      coreRef.current.scale.set(pulse, pulse, pulse);
    }
    if (particlesRef.current) {
      particlesRef.current.rotation.z += delta * 0.25 * speedMultiplier;
    }
  });

  return (
    <group position={[0, 0, 0]}>
      {/* Outer Hexagonal Shield Ring */}
      <mesh ref={outerRingRef}>
        <torusGeometry args={[6.2, 0.14, 16, 64]} />
        <meshStandardMaterial
          color="#38bdf8"
          emissive="#0284c7"
          emissiveIntensity={isWarping ? 4.0 : 1.5}
          roughness={0.2}
          metalness={0.8}
        />
      </mesh>

      {/* Segmented Middle Ring */}
      <mesh ref={innerRingRef}>
        <torusGeometry args={[4.8, 0.18, 16, 48]} />
        <meshStandardMaterial
          color="#7bf1a8"
          emissive="#10b981"
          emissiveIntensity={isWarping ? 5.0 : 2.0}
          wireframe
        />
      </mesh>

      {/* Central Cyber Portal Core */}
      <mesh
        ref={coreRef}
        onClick={() => onSelectNode?.({ type: 'portal', name: 'Cyber Gate', status: 'Active' })}
      >
        <circleGeometry args={[3.8, 48]} />
        <meshBasicMaterial
          color={isWarping ? '#ffffff' : '#0369a1'}
          transparent
          opacity={0.7}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Glowing Energy Aura */}
      <pointLight
        color="#38bdf8"
        intensity={isWarping ? 12 : 4}
        distance={25}
      />

      {/* Swirling Data Particles */}
      <points ref={particlesRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={particlePositions.length / 3}
            array={particlePositions}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={0.18}
          color="#7dd3fc"
          transparent
          opacity={0.85}
          blending={THREE.AdditiveBlending}
        />
      </points>

      {/* Portal Gate Base Arch Pillars */}
      <mesh position={[-7.5, -2, 0]}>
        <cylinderGeometry args={[0.3, 0.4, 8, 16]} />
        <meshStandardMaterial color="#1e293b" metalness={0.9} roughness={0.1} />
      </mesh>
      <mesh position={[7.5, -2, 0]}>
        <cylinderGeometry args={[0.3, 0.4, 8, 16]} />
        <meshStandardMaterial color="#1e293b" metalness={0.9} roughness={0.1} />
      </mesh>
    </group>
  );
}

export default EntryPortal;

