
import { Suspense, useMemo } from "react";
import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader.js";
import * as THREE from "three";

// Load the generated car model
function CarModel() {
  const obj = useLoader(
    OBJLoader,
    "/models/generated_car.obj"
  );

  const car = useMemo(() => {
    const cloned = obj.clone(true);

    // Find original model dimensions
    const box = new THREE.Box3().setFromObject(cloned);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());

    // Center the model
    cloned.position.sub(center);

    // Normalize model size
    const maxDimension = Math.max(
      size.x,
      size.y,
      size.z
    );

    if (maxDimension > 0) {
      cloned.scale.setScalar(3 / maxDimension);
    }

    return cloned;
  }, [obj]);

  return (
    <group rotation={[0, 0, Math.PI]}>
      <primitive object={car} />
    </group>
  );
}

// Complete 3D viewer
function ModelViewer() {
  return (
    <div
      style={{
        width: "100%",
        height: "550px",
        background: "#e8eef5",
        borderRadius: "10px",
        overflow: "hidden"
      }}
    >
      <Canvas
        camera={{
          position: [4, 3, 5],
          fov: 50,
          near: 0.1,
          far: 1000
        }}
      >
        {/* Lighting */}
        <ambientLight intensity={1.5} />

        <directionalLight
          position={[5, 8, 5]}
          intensity={2}
        />

        {/* Ground reference */}
        <gridHelper args={[10, 10]} />

        {/* AI-generated car */}
        <Suspense fallback={null}>
          <CarModel />
        </Suspense>

        {/* Mouse controls */}
        <OrbitControls
          enableRotate
          enableZoom
          enablePan
          makeDefault
        />
      </Canvas>
    </div>
  );
}

export default ModelViewer;
