
import { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";

// AI-generated 3D model
function GeneratedModel() {
  const { scene } = useGLTF("/models/polygen_model.glb");

  return <primitive object={scene} />;
}

// PolyGen 3D Model Viewer
function ModelViewer() {
  return (
    <div
      style={{
        width: "100%",
        height: "550px",
        background: "#e8eef5",
        borderRadius: "12px",
        overflow: "hidden",
      }}
    >
      <Canvas
        camera={{
          position: [4, 2.8, 5],
          fov: 45,
          near: 0.1,
          far: 1000,
        }}
        shadows
      >
        {/* Lighting */}
        <ambientLight intensity={1.5} />

        <hemisphereLight
          args={["#ffffff", "#b0b0b0", 1.2]}
        />

        <directionalLight
          position={[5, 8, 5]}
          intensity={2.5}
          castShadow
        />

        {/* Ground grid */}
        <gridHelper
          args={[10, 20, "#888888", "#cccccc"]}
          position={[0, -0.02, 0]}
        />

        {/* Generated GLB model */}
        <Suspense fallback={null}>
          <GeneratedModel />
        </Suspense>

        {/* Mouse controls */}
        <OrbitControls
          makeDefault
          enableRotate
          enableZoom
          enablePan
          enableDamping
          dampingFactor={0.05}
          minDistance={2}
          maxDistance={20}
          target={[0, 1, 0]}
        />
      </Canvas>
    </div>
  );
}

useGLTF.preload("/models/polygen_model.glb");

export default ModelViewer;
