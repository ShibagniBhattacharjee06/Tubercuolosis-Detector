from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from src.ml_model.predict import get_result

# Define application
app = FastAPI(
    title="MEDICARE app",
    description="MEDICARE app!",
    version="0.1",
)

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    # Handle preflight OPTIONS requests directly
    if request.method == "OPTIONS":
        response = Response()
    else:
        response = await call_next(request)
    
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Standard middleware as secondary fallback
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    """Return a welcome message."""
    return {"message": "Welcome to MEDICARE app! v1.5-Bulletproof-CORS"}


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