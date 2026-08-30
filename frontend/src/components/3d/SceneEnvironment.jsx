import React, { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export function SceneEnvironment({ activeZone }) {
  const starsRef = useRef();
  const dustRef = useRef();

  // Procedural Starfield
  const [starPositions, starColors] = useMemo(() => {
    const count = 1200;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const palette = [
      new THREE.Color('#38bdf8'),
      new THREE.Color('#818cf8'),
      new THREE.Color('#34d399'),
      new THREE.Color('#f43f5e'),
      new THREE.Color('#ffffff'),
    ];

    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      // Spread across the vast universe
      positions[i3] = (Math.random() - 0.5) * 1600 + 400;
      positions[i3 + 1] = (Math.random() - 0.5) * 800;
      positions[i3 + 2] = (Math.random() - 0.5) * 1200;

      const color = palette[Math.floor(Math.random() * palette.length)];
      colors[i3] = color.r;
      colors[i3 + 1] = color.g;
      colors[i3 + 2] = color.b;
    }
    return [positions, colors];
  }, []);

  // Cyber Floating Dust
  const dustPositions = useMemo(() => {
    const count = 400;
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      positions[i3] = (Math.random() - 0.5) * 1000 + 400;
      positions[i3 + 1] = (Math.random() - 0.5) * 300;
      positions[i3 + 2] = (Math.random() - 0.5) * 600;
    }
    return positions;
  }, []);

  useFrame((state, delta) => {
    if (starsRef.current) {
      starsRef.current.rotation.y += delta * 0.015;
    }
    if (dustRef.current) {
      dustRef.current.rotation.x += delta * 0.008;
      dustRef.current.rotation.y += delta * 0.012;
    }
  });

  return (
    <group>
      {/* Ambient and directional cybersecurity lighting */}
      <ambientLight intensity={0.45} color="#0f172a" />
      <directionalLight position={[100, 150, 80]} intensity={1.2} color="#93c5fd" />
      <directionalLight position={[-100, -50, -80]} intensity={0.6} color="#06b6d4" />
      <pointLight
        position={activeZone?.cameraTarget || [0, 0, 0]}
        intensity={2.5}
        distance={120}
        color={activeZone?.color || '#38bdf8'}
      />

      {/* Deep Space Stars */}
      <points ref={starsRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={starPositions.length / 3}
            array={starPositions}
            itemSize={3}
          />
          <bufferAttribute
            attach="attributes-color"
            count={starColors.length / 3}
            array={starColors}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={1.8}
          vertexColors
          transparent
          opacity={0.85}
          sizeAttenuation
          blending={THREE.AdditiveBlending}
        />
      </points>

      {/* Cyber Space Dust */}
      <points ref={dustRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={dustPositions.length / 3}
            array={dustPositions}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={2.2}
          color="#38bdf8"
          transparent
          opacity={0.4}
          sizeAttenuation
          blending={THREE.AdditiveBlending}
        />
      </points>

      {/* Infinite Cyber Grid Base */}
      <gridHelper
        args={[2000, 100, '#1e293b', '#0f172a']}
        position={[420, -40, 0]}
      />
    </group>
  );
}

export default SceneEnvironment;

