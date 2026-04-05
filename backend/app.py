from typing import Dict
from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.responses import JSONResponse

from src.ml_model.predict import get_result

from fastapi.middleware.cors import CORSMiddleware
import traceback

# Define application
app = FastAPI(
    title="MEDICARE app",
    description="MEDICARE app!",
    version="0.1",
)

# Standard CORS Middleware for better compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    """Return a welcome message."""
    return {"message": "Welcome to MEDICARE app! v2.1-Standardized"}

@app.post("/api/v1/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read file asynchronously (efficient for larger images)
        image_bytes = await file.read()
        
        # Guard: Check if file is empty
        if len(image_bytes) == 0:
            return JSONResponse(
                status_code=400,
                content={"error": "Empty file uploaded"}
            )
            
        result = get_result(image_bytes=image_bytes, is_api=True)
        return result
        
    except Exception as e:
        print(f"Prediction error: {e}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "details": "Check server logs for full traceback.",
                "type": type(e).__name__
            }
        )

@app.get("/api/v1/predict")
async def predict_get():
    return {"message": "Prediction endpoint is REACHABLE via GET."}

@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)