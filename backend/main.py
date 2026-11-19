
from fastapi import FastAPI

app = FastAPI(
    title="PolyGen API",
    description="Generative Text-to-3D Asset Pipeline",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "project": "PolyGen",
        "message": "PolyGen backend is running successfully!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "PolyGen Backend"
    }
