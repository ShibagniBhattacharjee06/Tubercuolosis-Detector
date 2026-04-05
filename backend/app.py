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

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    """Return a welcome message."""
    return {"message": "Welcome to MEDICARE app! v1.4-Diagnostic-Live"}


@app.get("/api/v1/predict")
async def predict_get():
    """Diagnostic GET endpoint to test connectivity."""
    return {"message": "Prediction endpoint is REACHABLE via GET. Use POST for actual predictions."}


@app.post("/api/v1/predict")
async def predict(file: UploadFile = File(...)):
    return get_result(image_file=file, is_api=True)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)