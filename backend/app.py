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
    return {"message": "Welcome to MEDICARE app! v2.3-Final-Fix"}

@app.post("/api/v1/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read file asynchronously
        image_bytes = await file.read()
        
        if len(image_bytes) == 0:
            return JSONResponse(
                status_code=400,
                content={"error": "Empty file uploaded", "server_version": "v2.3"}
            )
            
        print(f"DEBUG: Processing image of size {len(image_bytes)} bytes")
        result = get_result(image_bytes=image_bytes, is_api=True)
        print("DEBUG: Prediction successful")
        return result
        
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print(f"CRITICAL: Prediction error [{error_type}]: {error_msg}")
        traceback.print_exc()
        
        return JSONResponse(
            status_code=500,
            content={
                "error": error_msg,
                "type": error_type,
                "server_version": "v2.3",
                "details": "Model inference failed. Ensure input image format is correct."
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