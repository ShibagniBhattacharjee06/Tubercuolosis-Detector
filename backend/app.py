from typing import Dict
from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.responses import JSONResponse

from src.ml_model.predict import get_result

# Define application
app = FastAPI(
    title="MEDICARE app",
    description="MEDICARE app!",
    version="0.1",
)

@app.get("/")
def index():
    """Return a welcome message."""
    return {"message": "Welcome to MEDICARE app! v2.0-UltraLean-Final"}

@app.options("/api/v1/predict")
async def predict_options():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )

@app.post("/api/v1/predict")
async def predict(file: UploadFile = File(...)):
    result = get_result(image_file=file, is_api=True)
    return JSONResponse(
        content=result,
        headers={"Access-Control-Allow-Origin": "*"}
    )

@app.get("/api/v1/predict")
async def predict_get():
    return JSONResponse(
        content={"message": "Prediction endpoint is REACHABLE via GET."},
        headers={"Access-Control-Allow-Origin": "*"}
    )

@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)