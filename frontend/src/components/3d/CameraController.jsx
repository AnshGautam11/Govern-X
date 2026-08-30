import React, { useEffect, useRef } from 'react';
import { useThree, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import gsap from 'gsap';
import * as THREE from 'three';

export function CameraController({
  activeZone,
  selectedNode,
  isWarping,
  onWarpComplete,
  enableOrbit = true,
}) {
  const { camera } = useThree();
  const controlsRef = useRef();
  const targetLookAt = useRef(new THREE.Vector3(0, 0, 0));
  const currentLookAt = useRef(new THREE.Vector3(0, 0, 0));
  const isTransitioning = useRef(false);

  // Animate Camera Position and Target on Active Zone or Selected Node Change
  useEffect(() => {
    if (!activeZone) return;

    let px, py, pz, tx, ty, tz;

    if (selectedNode && selectedNode.pos) {
      // Focus directly near the selected 3D node
      [tx, ty, tz] = selectedNode.pos;
      px = tx + 8;
      py = ty + 6;
      pz = tz + 12;
    } else {
      [px, py, pz] = activeZone.cameraPosition || [0, 0, 20];
      [tx, ty, tz] = activeZone.cameraTarget || [0, 0, 0];
    }

    isTransitioning.current = true;
    targetLookAt.current.set(tx, ty, tz);

    const duration = isWarping ? 2.4 : 1.6;
    const ease = isWarping ? 'power4.inOut' : 'power3.inOut';

    const tl = gsap.timeline({
      onComplete: () => {
        isTransitioning.current = false;
        if (controlsRef.current) {
          controlsRef.current.target.copy(targetLookAt.current);
          controlsRef.current.update();
        }
      },
    });

    tl.to(
      camera.position,
      {
        x: px,
        y: py,
        z: pz,
        duration,
        ease,
      },
      0
    );

    tl.to(
      currentLookAt.current,
      {
        x: tx,
        y: ty,
        z: tz,
        duration,
        ease,
      },
      0
    );

    if (activeZone.fov) {
      tl.to(
        camera,
        {
          fov: activeZone.fov,
          duration: 1.6,
          ease: 'power2.out',
          onUpdate: () => camera.updateProjectionMatrix(),
        },
        0
      );
    }
  }, [activeZone, selectedNode, isWarping, camera]);

  // Handle Enter System Warp Transition
  useEffect(() => {
    if (isWarping) {
      const tl = gsap.timeline({
        onComplete: () => {
          if (onWarpComplete) onWarpComplete();
        },
      });

      tl.to(camera.position, {
        z: -10,
        y: 2,
        duration: 1.6,
        ease: 'expo.in',
      });
    }
  }, [isWarping, camera, onWarpComplete]);

  // Continuously update camera lookAt when transitioning
  useFrame(() => {
    if (isTransitioning.current) {
      camera.lookAt(currentLookAt.current);
    }
  });

  return (
    <OrbitControls
      ref={controlsRef}
      enableDamping
      dampingFactor={0.06}
      enablePan={false}
      minDistance={6}
      maxDistance={800}
      maxPolarAngle={Math.PI / 2 + 0.15}
      enabled={enableOrbit && !isWarping}
    />
  );
}

export default CameraController;
