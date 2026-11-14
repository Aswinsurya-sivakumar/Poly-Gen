import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import trimesh

from IPython.display import display

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh

# Set device
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("PolyGen - Text to 3D Generation")
print("--------------------------------")

print("PyTorch Version:", torch.__version__)
print("Device:", device)

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("Warning: GPU not available. Enable T4 GPU in Colab.")

PROJECT_DIR = "/content/PolyGen"

OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
MODEL_DIR = os.path.join(PROJECT_DIR, "models")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

print("Project folders created successfully!")

print("Loading Shap-E models...")

xm = load_model(
    "transmitter",
    device=device
)

model = load_model(
    "text300M",
    device=device
)

diffusion = diffusion_from_config(
    load_config("diffusion")
)

print("Models loaded successfully!")

def generate_3d_model(prompt, filename):

    print("\nGenerating 3D model...")
    print("Prompt:", prompt)

    latents = sample_latents(
        batch_size=1,
        model=model,
        diffusion=diffusion,
        guidance_scale=15.0,
        model_kwargs={
            "texts": [prompt]
        },
        progress=True,
        clip_denoised=True,
        use_fp16=torch.cuda.is_available(),
        use_karras=True,
        karras_steps=64,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0
    )

    # Convert latent representation into 3D mesh
    mesh = decode_latent_mesh(
        xm,
        latents[0]
    ).tri_mesh()

    # Save OBJ file
    output_path = os.path.join(
        OUTPUT_DIR,
        filename + ".obj"
    )

    with open(output_path, "w") as file:
        mesh.write_obj(file)

    print("3D model generated successfully!")
    print("Saved at:", output_path)

    return output_path

    prompt = "A futuristic sports car"

model_path = generate_3d_model(
    prompt,
    "sports_car"
)