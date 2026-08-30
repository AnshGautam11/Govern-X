import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { ASSET_ORBIT_DATA } from '../../../data/universeData';
import * as THREE from 'three';

function OrbitingAsset({ asset, onSelect, isHovered, onHover, onUnhover }) {
  const groupRef = useRef();
  const meshRef = useRef();

  useFrame((state) => {
    if (groupRef.current) {
      const time = state.clock.elapsedTime * asset.orbitSpeed;
      const x = Math.cos(time) * asset.orbitRadius;
      const z = Math.sin(time) * asset.orbitRadius;
      const y = Math.sin(time * 1.5) * (asset.orbitRadius * asset.orbitTilt);
      groupRef.current.position.set(x, y, z);
    }
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.02;
      meshRef.current.rotation.y += 0.03;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Asset 3D Mesh */}
      <mesh
        ref={meshRef}
        onClick={(e) => {
          e.stopPropagation();
          const currentPos = groupRef.current ? [120 + groupRef.current.position.x, 20 + groupRef.current.position.y, -70 + groupRef.current.position.z] : [120, 20, -70];
          onSelect({ ...asset, pos: currentPos });
        }}
        onPointerOver={(e) => {
          e.stopPropagation();
          onHover(asset.id);
        }}
        onPointerOut={() => onUnhover()}
        scale={isHovered ? 1.4 : 1.0}
      >
        {asset.type === 'Server' && <boxGeometry args={[1.6, 1.6, 1.6]} />}
        {asset.type === 'Data Vault' && <octahedronGeometry args={[1.5, 0]} />}
        {asset.type === 'User / Identity' && <sphereGeometry args={[1.2, 16, 16]} />}
        {asset.type === 'Application' && <dodecahedronGeometry args={[1.4, 0]} />}
        {asset.type === 'Device' && <cylinderGeometry args={[1.0, 1.0, 1.6, 12]} />}

        <meshStandardMaterial
          color={asset.color}
          emissive={asset.color}
          emissiveIntensity={isHovered ? 2.5 : 0.8}
          roughness={0.2}
          metalness={0.8}
          wireframe={isHovered}
        />
      </mesh>

      {/* Pulsing Target Halo */}
      <mesh>
        <ringGeometry args={[1.8, 2.0, 24]} />
        <meshBasicMaterial color={asset.color} transparent opacity={0.6} side={THREE.DoubleSide} />
      </mesh>

      {/* Contextual Floating Tag on Hover */}
      {isHovered && (
        <Html
          position={[0, 2.2, 0]}
          center
          distanceFactor={38}
          style={{ pointerEvents: 'none', transition: 'opacity 0.2s ease' }}
        >
          <div
            style={{
              background: 'rgba(6, 11, 24, 0.92)',
              border: `1px solid ${asset.color}`,
              padding: '4px 10px',
              borderRadius: '6px',
              color: '#ffffff',
              fontSize: '10px',
              whiteSpace: 'nowrap',
              fontFamily: 'Inter, system-ui, sans-serif',
              boxShadow: `0 0 14px ${asset.color}55`,
            }}
          >
            <div style={{ fontWeight: 'bold', color: asset.color }}>{asset.name}</div>
            <div style={{ fontSize: '9px', color: '#94a3b8' }}>
              Type: {asset.type} • Status: {asset.status} ({asset.risk})
            </div>
          </div>
        </Html>
      )}
    </group>
  );
}

export function AssetOrbit({ onSelectNode }) {
  const [hoveredAsset, setHoveredAsset] = useState(null);
  const planetRef = useRef();
  const atmosphereRef = useRef();

  useFrame((state, delta) => {
    if (planetRef.current) {
      planetRef.current.rotation.y += delta * 0.08;
    }
    if (atmosphereRef.current) {
      atmosphereRef.current.rotation.y -= delta * 0.04;
    }
  });

  return (
    <group position={[120, 20, -70]}>
      {/* Central Organization Planet */}
      <mesh ref={planetRef}>
        <sphereGeometry args={[9, 32, 32]} />
        <meshStandardMaterial
          color="#0a1829"
          emissive="#0284c7"
          emissiveIntensity={0.5}
          roughness={0.4}
          metalness={0.7}
        />
      </mesh>

      {/* Cyber Continental Wireframe Crust */}
      <mesh ref={atmosphereRef}>
        <sphereGeometry args={[9.3, 24, 24]} />
        <meshBasicMaterial
          color="#38bdf8"
          wireframe
          transparent
          opacity={0.35}
        />
      </mesh>

      {/* Planet Glow Atmosphere */}
      <pointLight color="#38bdf8" intensity={4} distance={45} />

      {/* Orbital Path Rings */}
      {[18, 21, 24, 26, 29, 33].map((radius, idx) => (
        <mesh key={radius} rotation={[-Math.PI / 2 + idx * 0.08, idx * 0.05, 0]}>
          <ringGeometry args={[radius - 0.06, radius + 0.06, 64]} />
          <meshBasicMaterial color="#38bdf8" transparent opacity={0.2} side={THREE.DoubleSide} />
        </mesh>
      ))}

      {/* Orbiting Asset Nodes */}
      {ASSET_ORBIT_DATA.map((asset) => (
        <OrbitingAsset
          key={asset.id}
          asset={asset}
          isHovered={hoveredAsset === asset.id}
          onHover={setHoveredAsset}
          onUnhover={() => setHoveredAsset(null)}
          onSelect={(item) =>
            onSelectNode?.({
              type: 'asset',
              zone: 'identify',
              title: item.name,
              name: item.name,
              category: item.category,
              status: item.status,
              risk: item.risk,
              pos: item.pos,
              score: item.complianceScore,
              accent: item.color,
              summary: `${item.type} asset located at ${item.ip} operating on ${item.os}.`,
              details: `Category: ${item.category} | Workload: ${item.workload} | Last Scanned: ${item.lastScanned}`,
              route: '/identify',
              pillarName: 'IDENTIFY',
            })
          }
        />
      ))}
    </group>
  );
}

export default AssetOrbit;
