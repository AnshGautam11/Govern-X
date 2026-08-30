import React, { useRef, useState, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { THREAT_DNA_NODES } from '../../../data/universeData';
import * as THREE from 'three';

export function ThreatDNALab({ onSelectNode }) {
  const [hoveredNode, setHoveredNode] = useState(null);
  const helixGroupRef = useRef();

  // Generate double-helix geometry
  const { strandA, strandB, rungs } = useMemo(() => {
    const pointsA = [];
    const pointsB = [];
    const ladderRungs = [];
    const totalSteps = 40;
    const height = 36;
    const radius = 4.5;
    const turns = 2.5;

    for (let i = 0; i <= totalSteps; i++) {
      const t = (i / totalSteps) * Math.PI * 2 * turns;
      const y = (i / totalSteps) * height - height / 2;
      const xA = Math.cos(t) * radius;
      const zA = Math.sin(t) * radius;
      const xB = Math.cos(t + Math.PI) * radius;
      const zB = Math.sin(t + Math.PI) * radius;

      pointsA.push(new THREE.Vector3(xA, y, zA));
      pointsB.push(new THREE.Vector3(xB, y, zB));

      if (i % 2 === 0) {
        ladderRungs.push({
          start: new THREE.Vector3(xA, y, zA),
          end: new THREE.Vector3(xB, y, zB),
          mid: new THREE.Vector3((xA + xB) / 2, y, (zA + zB) / 2),
        });
      }
    }

    return { strandA: pointsA, strandB: pointsB, rungs: ladderRungs };
  }, []);

  useFrame((state, delta) => {
    if (helixGroupRef.current) {
      helixGroupRef.current.rotation.y += delta * 0.35;
      helixGroupRef.current.position.y = -20 + Math.sin(state.clock.elapsedTime * 0.8) * 1.2;
    }
  });

  return (
    <group position={[240, -20, 10]}>
      {/* Laboratory Base Pedestal and Holographic Rings */}
      <mesh position={[0, -22, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[14, 16, 2, 32]} />
        <meshStandardMaterial color="#0b1020" metalness={0.9} roughness={0.2} />
      </mesh>

      <mesh position={[0, -20.8, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[12, 12.3, 48]} />
        <meshBasicMaterial color="#a78bfa" transparent opacity={0.7} side={THREE.DoubleSide} />
      </mesh>

      {/* Rotating DNA Helix */}
      <group ref={helixGroupRef}>
        {/* Connecting Hydrogen Rungs */}
        {rungs.map((rung, idx) => {
          const length = rung.start.distanceTo(rung.end);
          return (
            <mesh key={idx} position={rung.mid}>
              <boxGeometry args={[length, 0.15, 0.15]} />
              <meshBasicMaterial color="#7c3aed" transparent opacity={0.6} />
            </mesh>
          );
        })}

        {/* Interactive Threat/Vulnerability/Risk Nodes along Helix */}
        {THREAT_DNA_NODES.map((node) => {
          const stepIndex = Math.min(node.helixIndex * 6 + 4, strandA.length - 1);
          const isStrandA = node.helixIndex % 2 === 0;
          const pos = isStrandA ? strandA[stepIndex] : strandB[stepIndex];
          const isHovered = hoveredNode === node.id;

          return (
            <group key={node.id} position={[pos.x, pos.y, pos.z]}>
              <mesh
                scale={isHovered ? 1.4 : 1.0}
                onClick={(e) => {
                  e.stopPropagation();
                  onSelectNode?.({
                    type: 'threat_dna',
                    zone: 'detect',
                    title: node.name,
                    name: node.name,
                    category: node.kind,
                    severity: node.severity,
                    cve: node.cve,
                    pos: [240 + pos.x, -20 + pos.y, 10 + pos.z],
                    status: node.status,
                    accent: node.accent,
                    score: node.severity === 'Critical' ? 45 : node.severity === 'High' ? 65 : 82,
                    summary: `Linked ${node.kind}: ${node.vulnerability}`,
                    details: `Impact: ${node.impact} | CVE: ${node.cve} | Risk: ${node.riskLevel}`,
                    route: '/detect',
                    pillarName: 'DETECT',
                  });
                }}
                onPointerOver={(e) => {
                  e.stopPropagation();
                  setHoveredNode(node.id);
                }}
                onPointerOut={() => setHoveredNode(null)}
              >
                <sphereGeometry args={[0.9, 20, 20]} />
                <meshStandardMaterial
                  color={node.accent}
                  emissive={node.accent}
                  emissiveIntensity={isHovered ? 3.0 : 1.2}
                  roughness={0.1}
                  metalness={0.8}
                />
              </mesh>

              {/* Glowing Halo */}
              <mesh>
                <ringGeometry args={[1.2, 1.35, 16]} />
                <meshBasicMaterial color={node.accent} transparent opacity={0.7} side={THREE.DoubleSide} />
              </mesh>

              {/* Contextual Node Tooltip on Hover */}
              {isHovered && (
                <Html
                  position={[0, 1.4, 0]}
                  center
                  distanceFactor={32}
                  style={{ pointerEvents: 'none', transition: 'opacity 0.2s ease' }}
                >
                  <div
                    style={{
                      background: 'rgba(6, 11, 24, 0.94)',
                      border: `1px solid ${node.accent}`,
                      padding: '4px 10px',
                      borderRadius: '6px',
                      color: '#ffffff',
                      fontSize: '10px',
                      whiteSpace: 'nowrap',
                      fontFamily: 'Inter, system-ui, sans-serif',
                      boxShadow: `0 0 14px ${node.accent}55`,
                    }}
                  >
                    <div style={{ fontWeight: 'bold', color: node.accent }}>[{node.kind}] {node.name}</div>
                    <div style={{ fontSize: '9px', color: '#94a3b8', marginTop: '2px' }}>
                      Severity: {node.severity} • {node.cve}
                    </div>
                  </div>
                </Html>
              )}
            </group>
          );
        })}
      </group>
    </group>
  );
}

export default ThreatDNALab;
