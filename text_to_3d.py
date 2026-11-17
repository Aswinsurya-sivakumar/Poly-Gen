
"""
POLYGEN - WEEK 1
Text-to-3D Asset Generation
Using Shap-E
"""

import os
import torch
import trimesh
import numpy as np

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh


class PolyGen:

    def __init__(self, output_dir="generated_assets"):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

        print("Initializing PolyGen...")
        print("Device:", self.device)

        self.load_models()

    # ----------------------------------
    # Load AI Models
    # ----------------------------------

    def load_models(self):

        print("Loading Shap-E models...")

        self.transmitter = load_model(
            "transmitter",
            device=self.device
        )

        self.model = load_model(
            "text300M",
            device=self.device
        )

        self.diffusion = diffusion_from_config(
            load_config("diffusion")
        )

        print("Models loaded successfully!")

    # ----------------------------------
    # Generate 3D Latents
    # ----------------------------------

    def generate_3d(self, prompt):

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        print("\nGenerating 3D model...")
        print("Prompt:", prompt)

        latents = sample_latents(
            batch_size=1,
            model=self.model,
            diffusion=self.diffusion,
            guidance_scale=15.0,
            model_kwargs={
                "texts": [prompt]
            },
            progress=True,
            clip_denoised=True,
            use_fp16=self.device.type == "cuda",
            use_karras=True,
            karras_steps=64,
            sigma_min=1e-3,
            sigma_max=160,
            s_churn=0
        )

        print("Generation completed!")

        return latents[0]

    # ----------------------------------
    # Convert Latent to Mesh
    # ----------------------------------

    def create_mesh(self, latent):

        print("Creating 3D mesh...")

        mesh_data = decode_latent_mesh(
            self.transmitter,
            latent
        )

        mesh = mesh_data.tri_mesh()

        return mesh

    # ----------------------------------
    # Validate Mesh
    # ----------------------------------

    def validate_mesh(self, mesh):

        print("\nChecking generated mesh...")

        vertices = np.asarray(mesh.verts)
        faces = np.asarray(mesh.faces)

        print("Vertices:", len(vertices))
        print("Faces:", len(faces))

        if len(vertices) == 0 or len(faces) == 0:
            raise ValueError("Generated mesh is empty")

        return True

    # ----------------------------------
    # Export OBJ
    # ----------------------------------

    def export_obj(self, mesh, filename):

        path = os.path.join(
            self.output_dir,
            filename + ".obj"
        )

        with open(path, "w") as file:
            mesh.write_obj(file)

        print("OBJ saved:", path)

        return path

    # ----------------------------------
    # Export GLB
    # ----------------------------------

    def export_glb(self, obj_path, filename):

        mesh = trimesh.load(
            obj_path,
            force="mesh"
        )

        glb_path = os.path.join(
            self.output_dir,
            filename + ".glb"
        )

        mesh.export(glb_path)

        print("GLB saved:", glb_path)

        return glb_path

    # ----------------------------------
    # Complete Pipeline
    # ----------------------------------

    def run(self, prompt):

        latent = self.generate_3d(prompt)

        mesh = self.create_mesh(latent)

        self.validate_mesh(mesh)

        obj_path = self.export_obj(
            mesh,
            "polygen_model"
        )

        glb_path = self.export_glb(
            obj_path,
            "polygen_model"
        )

        print("\n--------------------------")
        print("POLYGEN COMPLETED")
        print("--------------------------")

        print("OBJ:", obj_path)
        print("GLB:", glb_path)

        return obj_path, glb_path


# ======================================
# MAIN PROGRAM
# ======================================

if __name__ == "__main__":

    polygen = PolyGen()

    user_prompt = input(
        "\nDescribe your 3D object: "
    )

    polygen.run(user_prompt)