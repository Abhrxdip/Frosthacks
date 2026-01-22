import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Text, Stars } from '@react-three/drei';
import * as THREE from 'three';
import styles from './MoodGlobe3D.module.css';

interface MoodGlobe3DProps {
  moodHistory: Array<{ date: string; mood: number; id: string; source: string }>;
}

const AnimatedGlobe: React.FC<{ moodHistory: Array<{ date: string; mood: number }> }> = ({ moodHistory }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);

  // Calculate average mood for color
  const avgMood = moodHistory.length > 0 
    ? moodHistory.reduce((sum, entry) => sum + entry.mood, 0) / moodHistory.length 
    : 5;

  // Color based on mood (red -> yellow -> green)
  let globeColor = '#44ff88'; // Green - Good
  let glowColor = '#22dd66';
  const normalized = avgMood / 10;
  if (normalized < 0.4) {
    globeColor = '#ff4444'; // Red - Poor
    glowColor = '#dd2222';
  } else if (normalized < 0.7) {
    globeColor = '#ffaa00'; // Orange - Moderate
    glowColor = '#dd8800';
  }

  // Animate rotation and pulsing
  useFrame((state) => {
    const time = state.clock.getElapsedTime();
    
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.003;
      // Subtle pulsing effect based on mood
      const pulse = Math.sin(time * 2) * 0.05;
      meshRef.current.scale.set(1 + pulse, 1 + pulse, 1 + pulse);
    }
    
    if (glowRef.current) {
      glowRef.current.rotation.y -= 0.002;
      // Glow pulsing
      const glowPulse = Math.sin(time * 3) * 0.1 + 0.9;
      glowRef.current.scale.set(1.15 * glowPulse, 1.15 * glowPulse, 1.15 * glowPulse);
    }
  });

  return (
    <>
      {/* Background stars */}
      <Stars radius={100} depth={50} count={2000} factor={4} saturation={0} fade speed={1} />
      
      {/* Outer glow sphere */}
      <Sphere ref={glowRef} args={[2.3, 32, 32]}>
        <meshBasicMaterial
          color={glowColor}
          transparent
          opacity={0.15}
          side={THREE.BackSide}
        />
      </Sphere>

      {/* Main mood globe with wireframe */}
      <Sphere ref={meshRef} args={[2, 32, 32]}>
        <meshStandardMaterial
          color={globeColor}
          roughness={0.3}
          metalness={0.7}
          emissive={globeColor}
          emissiveIntensity={0.3}
          wireframe={false}
        />
      </Sphere>

      {/* Inner core */}
      <Sphere args={[1.5, 32, 32]}>
        <meshStandardMaterial
          color={globeColor}
          transparent
          opacity={0.3}
          emissive={globeColor}
          emissiveIntensity={0.5}
        />
      </Sphere>

      {/* Mood score text */}
      <Text
        position={[0, -3.5, 0]}
        fontSize={0.6}
        color="white"
        anchorX="center"
        anchorY="middle"
        fontWeight="bold"
      >
        {avgMood.toFixed(1)}/10
      </Text>

      {/* Entry count */}
      <Text
        position={[0, 3.5, 0]}
        fontSize={0.4}
        color="#cccccc"
        anchorX="center"
        anchorY="middle"
      >
        {moodHistory.length} Mood Entries
      </Text>

      {/* Orbit controls */}
      <OrbitControls
        enableZoom={true}
        enablePan={false}
        minDistance={5}
        maxDistance={12}
        autoRotate={true}
        autoRotateSpeed={1.5}
      />

      {/* Dynamic lighting */}
      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 5, 5]} intensity={1.2} color={globeColor} />
      <pointLight position={[-5, -5, -5]} intensity={0.6} color="#4488ff" />
      <pointLight position={[0, 5, 0]} intensity={0.4} color="#ff88ff" />
    </>
  );
};

const MoodGlobe3D: React.FC<MoodGlobe3DProps> = ({ moodHistory }) => {
  return (
    <div className={styles.container}>
      <div className={styles.canvasWrapper}>
        <Canvas 
          camera={{ position: [0, 0, 8], fov: 60 }}
          gl={{ antialias: true, alpha: true }}
          dpr={[1, 2]}
        >
          <color attach="background" args={['#0a0a1a']} />
          <AnimatedGlobe moodHistory={moodHistory} />
        </Canvas>
      </div>
      <div className={styles.legend}>
        <div className={styles.legendItem}>
          <div className={styles.colorBox} style={{ background: '#44ff88' }}></div>
          <span>Good (7-10)</span>
        </div>
        <div className={styles.legendItem}>
          <div className={styles.colorBox} style={{ background: '#ffaa00' }}></div>
          <span>Moderate (4-6)</span>
        </div>
        <div className={styles.legendItem}>
          <div className={styles.colorBox} style={{ background: '#ff4444' }}></div>
          <span>Poor (1-3)</span>
        </div>
      </div>
    </div>
  );
};

export default MoodGlobe3D;
