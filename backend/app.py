from typing import Dict

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.ml_model.predict import get_result

# Define application
app = FastAPI(
    title="MEDICARE app",
    description="MEDICARE app!",
    version="0.1",
)

origins = [
    "*",
    "https://tubercuolosis-detector.vercel.app",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    """Return a welcome message."""
    return {"message": "Welcome to MEDICARE app!"}


@app.post("/api/v1/predict")
async def predict(file: UploadFile = File(...)):
    return get_result(image_file=file, is_api=True)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)