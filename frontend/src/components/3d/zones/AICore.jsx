import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { AI_CORE_METRICS } from '../../../data/universeData';

export function AICore({ onSelectNode }) {
  const coreRef = useRef();
  const ring1Ref = useRef();
  const ring2Ref = useRef();
  const ring3Ref = useRef();

  useFrame((state, delta) => {
    if (coreRef.current) {
      coreRef.current.rotation.y += delta * 0.4;
      coreRef.current.rotation.x += delta * 0.2;
      const pulse = Math.sin(state.clock.elapsedTime * 3) * 0.08 + 1;
      coreRef.current.scale.set(pulse, pulse, pulse);
    }
    if (ring1Ref.current) {
      ring1Ref.current.rotation.x += delta * 0.6;
      ring1Ref.current.rotation.y += delta * 0.3;
    }
    if (ring2Ref.current) {
      ring2Ref.current.rotation.y -= delta * 0.8;
      ring2Ref.current.rotation.z += delta * 0.4;
    }
    if (ring3Ref.current) {
      ring3Ref.current.rotation.z += delta * 0.5;
      ring3Ref.current.rotation.x -= delta * 0.3;
    }
  });

  return (
    <group position={[600, 35, -15]}>
      {/* Central Pulsing Geodesic AI Core */}
      <mesh
        ref={coreRef}
        onClick={(e) => {
          e.stopPropagation();
          onSelectNode?.({
            type: 'ai_core',
            zone: 'govern',
            title: 'GovernX AI Posture Core',
            name: 'Neural Intelligence Engine',
            category: 'AUTONOMOUS REASONING',
            pos: [600, 35, -15],
            status: 'CONTINUOUS TELEMETRY SYNTHESIS',
            score: 96,
            accent: '#38bdf8',
            summary: 'Cross-universe neural engine evaluating compliance drift, asset vulnerability correlation, and automated remediation playbooks.',
            details: 'Model: Deep CSF-2.0 Cognitive Model | Accuracy: 96.8% | Active Policies: 34 Autonomous Rules Enforced',
            route: '/govern',
            pillarName: 'AI ENGINE',
          });
        }}
      >
        <icosahedronGeometry args={[5, 3]} />
        <meshStandardMaterial
          color="#0284c7"
          emissive="#38bdf8"
          emissiveIntensity={1.4}
          wireframe
        />
      </mesh>

      {/* Inner Glowing AI Nucleus */}
      <mesh>
        <sphereGeometry args={[3.2, 24, 24]} />
        <meshBasicMaterial color="#38bdf8" transparent opacity={0.6} />
      </mesh>

      {/* Gyroscopic Concentric Orbiting Rings */}
      <mesh ref={ring1Ref}>
        <torusGeometry args={[8.5, 0.12, 16, 64]} />
        <meshStandardMaterial color="#38bdf8" emissive="#38bdf8" emissiveIntensity={2.0} />
      </mesh>

      <mesh ref={ring2Ref}>
        <torusGeometry args={[11, 0.1, 16, 64]} />
        <meshStandardMaterial color="#818cf8" emissive="#6366f1" emissiveIntensity={1.8} />
      </mesh>

      <mesh ref={ring3Ref}>
        <torusGeometry args={[13.5, 0.08, 16, 64]} />
        <meshStandardMaterial color="#34d399" emissive="#10b981" emissiveIntensity={1.5} />
      </mesh>

      {/* Dynamic AI Energy Lighting */}
      <pointLight color="#38bdf8" intensity={6} distance={60} />

      {/* Floating AI Telemetry Cards */}
      <Html position={[0, 16, 0]} center distanceFactor={40} style={{ pointerEvents: 'none' }}>
        <div
          style={{
            background: 'rgba(6, 14, 32, 0.94)',
            border: '1px solid #38bdf8',
            padding: '8px 16px',
            borderRadius: '10px',
            color: '#ffffff',
            boxShadow: '0 0 24px rgba(56, 189, 248, 0.4)',
            textAlign: 'center',
            fontFamily: 'Inter, system-ui, sans-serif',
          }}
        >
          <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#38bdf8', letterSpacing: '0.1em' }}>
            🧠 AI CORE — NEURAL SECURITY MATRIX
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '6px', marginTop: '6px' }}>
            {AI_CORE_METRICS.map((m, idx) => (
              <div key={idx} style={{ fontSize: '9px', background: 'rgba(56, 189, 248, 0.1)', padding: '3px 6px', borderRadius: '4px' }}>
                <span style={{ color: '#94a3b8' }}>{m.label}: </span>
                <strong style={{ color: '#38bdf8' }}>{m.value}</strong>
              </div>
            ))}
          </div>
        </div>
      </Html>
    </group>
  );
}

export default AICore;
