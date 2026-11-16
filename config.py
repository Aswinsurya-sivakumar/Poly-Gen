
# ============================================================
# POLYGEN - WEEK 1
# TEXT TO 3D MODEL GENERATION
# Using OpenAI Shap-E
# ============================================================

import os
import torch
import numpy as np
import trimesh
import plotly.graph_objects as go

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh

from google.colab import files

# ------------------------------------------------------------
# 1. DEVICE CONFIGURATION
# ------------------------------------------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("POLYGEN TEXT-TO-3D PIPELINE")
print("---------------------------")
print("PyTorch:", torch.__version__)
print("Device:", device)

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("GPU not available. CPU generation may be slow.")

# ------------------------------------------------------------
# 2. CREATE OUTPUT DIRECTORY
# ------------------------------------------------------------

OUTPUT_DIR = "/content/polygen_output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("\nOutput directory created.")

# ------------------------------------------------------------
# 3. LOAD SHAP-E MODELS
# ------------------------------------------------------------

print("\nLoading Shap-E models...")

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

# ------------------------------------------------------------
# 4. GET TEXT PROMPT
# ------------------------------------------------------------

prompt = input(
    "\nEnter your 3D object description: "
).strip()

if not prompt:
    raise ValueError("Please enter a valid text prompt.")

print("\nYour Prompt:", prompt)

# ------------------------------------------------------------
# 5. GENERATE 3D LATENTS
# ------------------------------------------------------------

print("\nGenerating 3D model...")
print("Please wait...")

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
    use_fp16=(device.type == "cuda"),
    use_karras=True,
    karras_steps=64,
    sigma_min=1e-3,
    sigma_max=160,
    s_churn=0
)

print("\n3D generation completed!")

# ------------------------------------------------------------
# 6. DECODE LATENT INTO 3D MESH
# ------------------------------------------------------------

print("\nDecoding 3D mesh...")

mesh = decode_latent_mesh(
    xm,
    latents[0]
).tri_mesh()

vertices = np.asarray(
    mesh.verts,
    dtype=np.float32
)

faces = np.asarray(
    mesh.faces,
    dtype=np.int64
)

print("Vertices:", len(vertices))
print("Faces:", len(faces))

# ------------------------------------------------------------
# 7. SAVE MODEL AS OBJ
# ------------------------------------------------------------

obj_path = os.path.join(
    OUTPUT_DIR,
    "generated_model.obj"
)

with open(obj_path, "w") as file:
    mesh.write_obj(file)

print("\nOBJ model saved:", obj_path)

# ------------------------------------------------------------
# 8. LOAD AND INSPECT MODEL
# ------------------------------------------------------------

loaded_mesh = trimesh.load(
    obj_path,
    force="mesh",
    process=False
)

print("\nMODEL INFORMATION")
print("-----------------")
print("Vertices:", len(loaded_mesh.vertices))
print("Faces:", len(loaded_mesh.faces))
print("Watertight:", loaded_mesh.is_watertight)
print("Bounds:", loaded_mesh.bounds)
print("File size:", round(os.path.getsize(obj_path) / 1024, 2), "KB")

# ------------------------------------------------------------
# 9. VISUALIZE 3D MODEL
# ------------------------------------------------------------

print("\nDisplaying 3D model...")

fig = go.Figure(
    data=[
        go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=faces[:, 0],
            j=faces[:, 1],
            k=faces[:, 2],
            color="lightblue",
            opacity=1.0
        )
    ]
)

fig.update_layout(
    title="PolyGen - Generated 3D Model",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z",
        aspectmode="data"
    ),
    width=850,
    height=650
)

fig.show()

# ------------------------------------------------------------
# 10. DOWNLOAD GENERATED MODEL
# ------------------------------------------------------------

print("\nDownloading OBJ file...")

files.download(obj_path)

print("\nPOLYGEN PIPELINE COMPLETED SUCCESSFULLY!")
