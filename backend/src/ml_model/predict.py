import os
import io
import gc
from PIL import Image
import numpy as np
import onnxruntime
import datetime
import base64
from pathlib import Path

# Application paths
BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = "tuberModel.onnx"
MODEL_PATH = os.path.join(BASE_DIR, FILE_NAME)

# Global session for lazy loading
_ort_session = None

def get_session():
    """Lazily load the ONNX session with memory optimizations."""
    global _ort_session
    if _ort_session is None:
        try:
            # Set session options for low memory
            options = onnxruntime.SessionOptions()
            options.intra_op_num_threads = 1
            options.inter_op_num_threads = 1
            options.execution_mode = onnxruntime.ExecutionMode.ORT_SEQUENTIAL
            
            _ort_session = onnxruntime.InferenceSession(
                MODEL_PATH, 
                options,
                providers=['CPUExecutionProvider']
            )
        except Exception as e:
            print(f"Error loading ONNX model: {e}")
            _ort_session = None
    return _ort_session

# Label mapping
class_names = ['normal', 'tuberculosis']

def transform_image(image_bytes):
    """Memory-efficient image transformation."""
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    
    # Resize shorter side to 255
    w, h = image.size
    if w < h:
        new_w, new_h = 255, int(255 * h / w)
    else:
        new_w, new_h = int(255 * w / h), 255
    image = image.resize((new_w, new_h), Image.BILINEAR)
    
    # Center Crop 224x224
    w, h = image.size
    left, top = (w - 224) / 2, (h - 224) / 2
    image = image.crop((left, top, left + 224, top + 224))
    
    # ToTensor & Normalize
    img_array = np.array(image).astype(np.float32) / 255.0
    img_array = img_array.transpose((2, 0, 1))
    
    mean = np.array([0.485, 0.456, 0.406]).reshape(3, 1, 1)
    std = np.array([0.229, 0.224, 0.225]).reshape(3, 1, 1)
    img_array = (img_array - mean) / std
    
    # Cleanup raw image object immediately
    image.close()
    
    return np.expand_dims(img_array, axis=0)

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def get_prediction(image_bytes):
    session = get_session()
    if session is None:
        return "Error", 0.0
    
    img = transform_image(image_bytes=image_bytes)
    ort_inputs = {session.get_inputs()[0].name: img}
    ort_outs = session.run(None, ort_inputs)

    # Cleanup image array early
    del img

    img_out = sigmoid(ort_outs[0])
    predicted_idx = np.argmax(img_out[0])
    confidence = round(float(img_out[0][predicted_idx]) * 100, 2)
    
    return class_names[predicted_idx], confidence

def get_result(image_bytes, is_api=False):
    start_time = datetime.datetime.now()
    
    class_name, confidence = get_prediction(image_bytes)
    
    image_data = None
    if not is_api:
        encoded_string = base64.b64encode(image_bytes)
        image_data = f'data:image/jpeg;base64,{encoded_string.decode("utf-8")}'
    
    # CALCULATE TIME
    execution_time = f'{round((datetime.datetime.now() - start_time).total_seconds() * 1000)} ms'
    
    # FINAL MEMORY CLEANUP
    gc.collect()

    result = {
        "inference_time": execution_time,
        "predictions": {
            "class_name": class_name,
            "confidence": confidence
        }
    }
    if not is_api and image_data:
        result["image_data"] = image_data
        
    return result
