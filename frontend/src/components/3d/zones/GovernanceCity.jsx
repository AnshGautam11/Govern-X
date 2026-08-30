import React, { useState, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { GOVERNANCE_BUILDINGS } from '../../../data/universeData';
import * as THREE from 'three';

function BuildingItem({ building, onSelect, isHovered, onHover, onUnhover }) {
  const meshRef = useRef();
  const [posX, , posZ] = building.position;
  const height = building.height;
  const posY = height / 2;

  useFrame((state, delta) => {
    if (meshRef.current) {
      const targetScale = isHovered ? 1.05 : 1.0;
      meshRef.current.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), delta * 8);
    }
  });

  return (
    <group position={[posX, 0, posZ]}>
      {/* Skyscraper Building Body */}
      <mesh
        ref={meshRef}
        position={[0, posY, 0]}
        onClick={(e) => {
          e.stopPropagation();
          onSelect({ ...building, pos: [posX, posY, posZ] });
        }}
        onPointerOver={(e) => {
          e.stopPropagation();
          onHover(building.id);
        }}
        onPointerOut={() => onUnhover()}
      >
        <boxGeometry args={[building.width, height, building.depth]} />
        <meshStandardMaterial
          color={isHovered ? building.accent : '#0a1020'}
          emissive={isHovered ? building.accent : '#111e38'}
          emissiveIntensity={isHovered ? 0.9 : 0.2}
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>

      {/* Glowing Building Edge Wireframe */}
      <mesh position={[0, posY, 0]}>
        <boxGeometry args={[building.width + 0.08, height + 0.08, building.depth + 0.08]} />
        <meshBasicMaterial
          color={building.accent}
          wireframe
          transparent
          opacity={isHovered ? 0.9 : 0.35}
        />
      </mesh>

      {/* Rooftop Beacon Spire */}
      <mesh position={[0, height + 1.2, 0]}>
        <cylinderGeometry args={[0.08, 0.2, 2.4, 8]} />
        <meshStandardMaterial
          color={building.accent}
          emissive={building.accent}
          emissiveIntensity={2.5}
        />
      </mesh>

      {/* Contextual Holographic Badge on Hover */}
      {isHovered && (
        <Html
          position={[0, height + 2.8, 0]}
          center
          distanceFactor={35}
          style={{ pointerEvents: 'none', transition: 'opacity 0.2s ease' }}
        >
          <div
            style={{
              background: 'rgba(6, 11, 24, 0.92)',
              backdropFilter: 'blur(8px)',
              border: `1px solid ${building.accent}`,
              padding: '5px 12px',
              borderRadius: '8px',
              color: '#ffffff',
              fontSize: '11px',
              whiteSpace: 'nowrap',
              fontFamily: 'Inter, system-ui, sans-serif',
              boxShadow: `0 0 16px ${building.accent}44`,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ color: building.accent, fontWeight: '800' }}>{building.code}</span>
              <span>{building.name}</span>
            </div>
            <div style={{ fontSize: '9px', color: '#94a3b8', marginTop: '2px' }}>
              Score: <strong style={{ color: building.accent }}>{building.compliance}%</strong> • {building.status}
            </div>
          </div>
        </Html>
      )}
    </group>
  );
}

export function GovernanceCity({ onSelectNode }) {
  const [hoveredBuilding, setHoveredBuilding] = useState(null);
  const roadsRef = useRef();

  useFrame((state, delta) => {
    if (roadsRef.current) {
      roadsRef.current.rotation.z += delta * 0.05;
    }
  });

  return (
    <group position={[0, 0, 0]}>
      {/* City Ground Base Platform */}
      <mesh position={[0, -0.2, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[70, 70]} />
        <meshStandardMaterial
          color="#040814"
          roughness={0.9}
          metalness={0.2}
        />
      </mesh>

      {/* Glowing City Grid Pathways / Roads */}
      <gridHelper
        args={[60, 24, '#38bdf8', '#0f172a']}
        position={[0, 0.02, 0]}
      />

      {/* Outer Road Ring Lights */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.05, 0]}>
        <ringGeometry args={[26, 26.3, 64]} />
        <meshBasicMaterial color="#34d399" transparent opacity={0.6} side={THREE.DoubleSide} />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.05, 0]}>
        <ringGeometry args={[18, 18.2, 64]} />
        <meshBasicMaterial color="#38bdf8" transparent opacity={0.5} side={THREE.DoubleSide} />
      </mesh>

      {/* Buildings */}
      {GOVERNANCE_BUILDINGS.map((building) => (
        <BuildingItem
          key={building.id}
          building={building}
          isHovered={hoveredBuilding === building.id}
          onHover={setHoveredBuilding}
          onUnhover={() => setHoveredBuilding(null)}
          onSelect={(bldg) =>
            onSelectNode?.({
              type: 'building',
              zone: 'govern',
              title: bldg.name,
              name: bldg.name,
              code: bldg.code,
              pos: bldg.pos,
              status: bldg.status,
              score: bldg.compliance,
              accent: bldg.accent,
              summary: bldg.summary,
              details: bldg.summary,
              findings: bldg.findings,
              policiesActive: bldg.policiesActive,
              reviewCadence: bldg.reviewCadence,
              route: '/govern',
              pillarName: 'GOVERN',
            })
          }
        />
      ))}
    </group>
  );
}

export default GovernanceCity;
