
from pathlib import Path

import trimesh


def generate_mesh():
    # Create the output directory
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    # Create a basic 3D box
    mesh = trimesh.creation.box(
        extents=[1.0, 1.0, 1.0]
    )

    # Save the mesh as an OBJ file
    output_path = output_dir / "sample_model.obj"
    mesh.export(output_path)

    print("3D mesh generated successfully!")
    print(f"Saved to: {output_path.resolve()}")
    print(f"Vertices: {len(mesh.vertices)}")
    print(f"Faces: {len(mesh.faces)}")


if __name__ == "__main__":
    generate_mesh()
