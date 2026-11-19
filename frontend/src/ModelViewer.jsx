
import { Suspense } from "react";
import { Canvas, useLoader } from "@react-three/fiber";
import { Center, OrbitControls } from "@react-three/drei";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader.js";

function Model() {
  // Load the generated OBJ model
  const model = useLoader(
    OBJLoader,
    "/models/sample_model.obj"
  );

  return (
    <Center>
      <primitive object={model.clone()} scale={1.5} />
    </Center>
  );
}

export default function ModelViewer() {
  return (
    <div style={{ width: "100%", height: "500px" }}>
      <Canvas camera={{ position: [3, 3, 5], fov: 50 }}>
        <color
          attach="background"
          args={["#e8eef5"]}
        />

        {/* Lighting */}
        <ambientLight intensity={1.5} />

        <directionalLight
          position={[5, 5, 5]}
          intensity={2}
        />

        {/* Load the 3D model */}
        <Suspense fallback={null}>
          <Model />
        </Suspense>

        {/* Camera controls */}
        <OrbitControls
          enableZoom={true}
          enablePan={true}
          enableRotate={true}
        />

        {/* Ground grid */}
        <gridHelper args={[10, 10]} />
      </Canvas>
    </div>
  );
}
