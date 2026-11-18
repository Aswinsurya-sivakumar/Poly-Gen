
"""
POLYGEN - WEEK 1
3D Mesh Processing and Optimization
"""

import os
import trimesh
import numpy as np


class MeshProcessor:

    def __init__(self, input_dir="generated_assets",
                 output_dir="processed_assets"):

        self.input_dir = input_dir
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

        print("PolyGen Mesh Processor Initialized")

    # ----------------------------------
    # Load 3D Model
    # ----------------------------------

    def load_model(self, filename):

        file_path = os.path.join(
            self.input_dir,
            filename
        )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Model not found: {file_path}"
            )

        mesh = trimesh.load(
            file_path,
            force="mesh",
            process=True
        )

        print("\nModel loaded successfully!")

        return mesh

    # ----------------------------------
    # Display Mesh Information
    # ----------------------------------

    def inspect_mesh(self, mesh):

        print("\n--- MESH INFORMATION ---")

        print("Vertices:", len(mesh.vertices))
        print("Faces:", len(mesh.faces))
        print("Watertight:", mesh.is_watertight)
        print("Volume:", mesh.volume)
        print("Surface Area:", mesh.area)
        print("Bounds:", mesh.bounds)

    # ----------------------------------
    # Clean Mesh
    # ----------------------------------

    def clean_mesh(self, mesh):

        print("\nCleaning mesh...")

        mesh.remove_duplicate_faces()
        mesh.remove_degenerate_faces()
        mesh.remove_unreferenced_vertices()

        mesh.fix_normals()

        print("Mesh cleaning completed!")

        return mesh

    # ----------------------------------
    # Simplify Mesh
    # ----------------------------------

    def simplify_mesh(self, mesh, target_faces=5000):

        print("\nOptimizing polygon count...")

        if len(mesh.faces) > target_faces:

            try:
                mesh = mesh.simplify_quadric_decimation(
                    face_count=target_faces
                )

                print("Mesh simplified successfully!")

            except Exception as error:

                print("Simplification unavailable:", error)
                print("Keeping original mesh.")

        else:

            print("Mesh already has fewer faces than target.")

        return mesh

    # ----------------------------------
    # Export OBJ
    # ----------------------------------

    def export_obj(self, mesh):

        output_path = os.path.join(
            self.output_dir,
            "optimized_model.obj"
        )

        mesh.export(output_path)

        print("\nOBJ exported:", output_path)

        return output_path

    # ----------------------------------
    # Export GLB
    # ----------------------------------

    def export_glb(self, mesh):

        output_path = os.path.join(
            self.output_dir,
            "optimized_model.glb"
        )

        mesh.export(output_path)

        print("GLB exported:", output_path)

        return output_path

    # ----------------------------------
    # Complete Processing Pipeline
    # ----------------------------------

    def process(self, filename):

        mesh = self.load_model(filename)

        self.inspect_mesh(mesh)

        original_faces = len(mesh.faces)

        mesh = self.clean_mesh(mesh)

        mesh = self.simplify_mesh(mesh)

        self.inspect_mesh(mesh)

        optimized_faces = len(mesh.faces)

        reduction = (
            (original_faces - optimized_faces)
            / original_faces * 100
        ) if original_faces else 0

        print("\n--- OPTIMIZATION RESULTS ---")

        print("Original Faces:", original_faces)
        print("Optimized Faces:", optimized_faces)
        print("Face Reduction:", round(reduction, 2), "%")

        obj_path = self.export_obj(mesh)

        glb_path = self.export_glb(mesh)

        print("\nMesh processing completed!")

        return obj_path, glb_path


# ======================================
# MAIN PROGRAM
# ======================================

if __name__ == "__main__":

    processor = MeshProcessor()

    processor.process("polygen_model.obj")
