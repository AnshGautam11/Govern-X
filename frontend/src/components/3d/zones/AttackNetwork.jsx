import React, { useRef, useState, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { ATTACK_NETWORK_DATA } from '../../../data/universeData';
import * as THREE from 'three';

function NetworkEdge({ edge, nodesMap }) {
  const fromNode = nodesMap[edge.from];
  const toNode = nodesMap[edge.to];
  const packetRef = useRef();

  const startVec = new THREE.Vector3(...fromNode.pos);
  const endVec = new THREE.Vector3(...toNode.pos);
  const edgeColor = edge.isAttack ? '#f87171' : '#10b981';

  useFrame((state) => {
    if (packetRef.current) {
      const t = (state.clock.elapsedTime * edge.flowRate) % 1;
      const currentPos = new THREE.Vector3().lerpVectors(startVec, endVec, t);
      packetRef.current.position.copy(currentPos);
    }
  });

  return (
    <group>
      {/* Animated Traveling Packet */}
      <mesh ref={packetRef}>
        <sphereGeometry args={[0.35, 12, 12]} />
        <meshBasicMaterial color={edgeColor} />
      </mesh>
    </group>
  );
}

export function AttackNetwork({ onSelectNode }) {
  const [hoveredNode, setHoveredNode] = useState(null);

  // Map nodes by ID
  const nodesMap = useMemo(() => {
    const map = {};
    ATTACK_NETWORK_DATA.nodes.forEach((node) => {
      map[node.id] = node;
    });
    return map;
  }, []);

  return (
    <group position={[360, 15, -55]}>
      {/* Cyber Base Matrix Grid */}
      <gridHelper args={[50, 16, '#f87171', '#0f172a']} position={[0, -12, 0]} />

      {/* Network Edge Lines */}
      {ATTACK_NETWORK_DATA.edges.map((edge, idx) => {
        const from = nodesMap[edge.from];
        const to = nodesMap[edge.to];
        const color = edge.isAttack ? '#f87171' : '#10b981';

        const points = [new THREE.Vector3(...from.pos), new THREE.Vector3(...to.pos)];
        const lineGeo = new THREE.BufferGeometry().setFromPoints(points);

        return (
          <group key={idx}>
            <line geometry={lineGeo}>
              <lineBasicMaterial color={color} transparent opacity={0.65} linewidth={2} />
            </line>
            <NetworkEdge edge={edge} nodesMap={nodesMap} />
          </group>
        );
      })}

      {/* Network Nodes */}
      {ATTACK_NETWORK_DATA.nodes.map((node) => {
        const isHovered = hoveredNode === node.id;
        const isAttacked = node.status === 'under_attack';
        const nodeColor = isAttacked ? '#f87171' : node.color;

        return (
          <group key={node.id} position={node.pos}>
            <mesh
              scale={isHovered ? 1.4 : 1.0}
              onClick={(e) => {
                e.stopPropagation();
                onSelectNode?.({
                  type: 'network_node',
                  zone: 'respond',
                  title: node.label,
                  name: node.label,
                  category: node.type.toUpperCase(),
                  pos: [360 + node.pos[0], 15 + node.pos[1], -55 + node.pos[2]],
                  status: isAttacked ? 'ACTIVE ATTACK MITIGATION' : 'PROTECTED & MONITORED',
                  score: isAttacked ? 58 : 94,
                  accent: nodeColor,
                  summary: `Topology Node: ${node.label} (${node.type}). Status: ${node.status}`,
                  details: `Position: [${node.pos.join(', ')}] | Active Defense Shield: ${isAttacked ? 'Intercepting' : 'Normal'}`,
                  route: '/respond',
                  pillarName: 'RESPOND',
                });
              }}
              onPointerOver={(e) => {
                e.stopPropagation();
                setHoveredNode(node.id);
              }}
              onPointerOut={() => setHoveredNode(null)}
            >
              <dodecahedronGeometry args={[1.1, 0]} />
              <meshStandardMaterial
                color={nodeColor}
                emissive={nodeColor}
                emissiveIntensity={isAttacked ? 3.0 : isHovered ? 2.5 : 1.0}
                roughness={0.2}
                metalness={0.8}
              />
            </mesh>

            {/* Pulsing Warning / Defense Halo */}
            <mesh>
              <ringGeometry args={[1.5, 1.7, 16]} />
              <meshBasicMaterial
                color={nodeColor}
                transparent
                opacity={isAttacked ? 0.9 : 0.4}
                side={THREE.DoubleSide}
              />
            </mesh>

            {/* Contextual Label on Hover */}
            {isHovered && (
              <Html
                position={[0, 1.8, 0]}
                center
                distanceFactor={35}
                style={{ pointerEvents: 'none', transition: 'opacity 0.2s ease' }}
              >
                <div
                  style={{
                    background: 'rgba(6, 11, 24, 0.94)',
                    border: `1px solid ${nodeColor}`,
                    padding: '4px 10px',
                    borderRadius: '6px',
                    color: '#ffffff',
                    fontSize: '10px',
                    whiteSpace: 'nowrap',
                    fontFamily: 'Inter, system-ui, sans-serif',
                    boxShadow: `0 0 14px ${nodeColor}66`,
                  }}
                >
                  <span style={{ color: nodeColor, fontWeight: 'bold' }}>{node.label}</span>
                  <div style={{ fontSize: '8px', color: isAttacked ? '#f87171' : '#34d399', marginTop: '2px' }}>
                    {isAttacked ? '🚨 THREAT INTERCEPTION' : 'SECURE PATH'}
                  </div>
                </div>
              </Html>
            )}
          </group>
        );
      })}
    </group>
  );
}

export default AttackNetwork;
