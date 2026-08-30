import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { UNIVERSE_ZONES } from '../../../data/universeData';
import * as THREE from 'three';

export function FinalUniverse({ onSelectZone }) {
  const centralNexusRef = useRef();
  const ringRef = useRef();

  useFrame((state, delta) => {
    if (centralNexusRef.current) {
      centralNexusRef.current.rotation.y += delta * 0.3;
      centralNexusRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
    }
    if (ringRef.current) {
      ringRef.current.rotation.z += delta * 0.15;
    }
  });

  return (
    <group position={[420, 20, 0]}>
      {/* Central Nexus Orb */}
      <mesh
        ref={centralNexusRef}
        onClick={(e) => {
          e.stopPropagation();
          onSelectZone?.('portal');
        }}
      >
        <icosahedronGeometry args={[12, 4]} />
        <meshStandardMaterial
          color="#38bdf8"
          emissive="#0284c7"
          emissiveIntensity={1.8}
          wireframe
        />
      </mesh>

      {/* Massive Orbiting Constellation Ring */}
      <mesh ref={ringRef} rotation={[-Math.PI / 3, 0, 0]}>
        <torusGeometry args={[80, 0.4, 16, 128]} />
        <meshStandardMaterial
          color="#818cf8"
          emissive="#6366f1"
          emissiveIntensity={2.0}
        />
      </mesh>

      {/* Pulsing Galactic Light */}
      <pointLight color="#38bdf8" intensity={8} distance={200} />

      {/* Cosmic Connected Energy Arcs Linking All Zones */}
      {UNIVERSE_ZONES.filter((z) => z.id !== 'final' && z.id !== 'portal').map((zone, idx) => {
        const [tx, ty, tz] = zone.cameraTarget;
        const relativeX = tx - 420;
        const relativeY = ty - 20;
        const relativeZ = tz;

        const points = [
          new THREE.Vector3(0, 0, 0),
          new THREE.Vector3(relativeX * 0.5, relativeY * 0.5 + 15, relativeZ * 0.5),
          new THREE.Vector3(relativeX, relativeY, relativeZ),
        ];
        const curve = new THREE.CatmullRomCurve3(points);
        const geo = new THREE.BufferGeometry().setFromPoints(curve.getPoints(30));

        return (
          <group key={idx}>
            <line geometry={geo}>
              <lineBasicMaterial color={zone.color} transparent opacity={0.5} linewidth={2} />
            </line>

            {/* Interactive Zone Marker */}
            <mesh
              position={[relativeX, relativeY, relativeZ]}
              onClick={(e) => {
                e.stopPropagation();
                onSelectZone?.(zone.id);
              }}
            >
              <sphereGeometry args={[2.8, 16, 16]} />
              <meshStandardMaterial
                color={zone.color}
                emissive={zone.color}
                emissiveIntensity={2.2}
              />
            </mesh>
          </group>
        );
      })}

      {/* Grand Title Banner */}
      <Html position={[0, 40, 0]} center distanceFactor={70} style={{ pointerEvents: 'none' }}>
        <div
          style={{
            background: 'rgba(8, 14, 30, 0.95)',
            border: '1px solid #818cf8',
            padding: '12px 28px',
            borderRadius: '12px',
            color: '#ffffff',
            boxShadow: '0 0 30px rgba(129, 140, 248, 0.5)',
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: '18px', fontWeight: '800', letterSpacing: '0.15em', color: '#c7d2fe' }}>
            ◉ GOVERNX — THE SECURITY UNIVERSE ◉
          </div>
          <div style={{ fontSize: '12px', color: '#93c5fd', marginTop: '6px', letterSpacing: '0.08em' }}>
            "YOUR SECURITY UNIVERSE, ONE INTELLIGENT VIEW."
          </div>
        </div>
      </Html>
    </group>
  );
}

export default FinalUniverse;

