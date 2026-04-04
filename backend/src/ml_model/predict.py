import os
import io
from PIL import Image
import numpy as np
import onnxruntime
import datetime
import base64
from pathlib import Path
# model

BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = "tuberModel.onnx"
MODEL_PATH = os.path.join(BASE_DIR, FILE_NAME)

# Use CPU provider for maximum compatibility on lightweight environments
try:
    # Explicitly set providers to avoid warnings or failures on some CPU-only environments
    ort_session = onnxruntime.InferenceSession(
        MODEL_PATH, 
        providers=['CPUExecutionProvider']
    )
except Exception as e:
    print(f"Error loading ONNX model: {e}")
    ort_session = None


# classes
class_names = ['normal', 'tuberculosis']


def transform_image(image_bytes):
    """
    Replicates torchvision transforms:
    - Resize(255)
    - CenterCrop(224)
    - ToTensor() (0-1 range, [C, H, W])
    - Normalize(mean, std)
    """
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    
    # Resize shorter side to 255
    w, h = image.size
    if w < h:
        new_w = 255
        new_h = int(255 * h / w)
    else:
        new_h = 255
        new_w = int(255 * w / h)
    image = image.resize((new_w, new_h), Image.BILINEAR)
    
    # Center Crop 224x224
    w, h = image.size
    left = (w - 224) / 2
    top = (h - 224) / 2
    right = (w + 224) / 2
    bottom = (h + 224) / 2
    image = image.crop((left, top, right, bottom))
    
    # ToTensor: Scale to [0, 1] and transpose to [C, H, W]
    img_array = np.array(image).astype(np.float32) / 255.0
    img_array = img_array.transpose((2, 0, 1))
    
    # Normalize with ImageNet stats
    mean = np.array([0.485, 0.456, 0.406]).reshape(3, 1, 1)
    std = np.array([0.229, 0.224, 0.225]).reshape(3, 1, 1)
    img_array = (img_array - mean) / std
    
    # Add batch dimension [1, C, H, W]
    return np.expand_dims(img_array, axis=0)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def get_prediction(image_bytes):
    if ort_session is None:
        return "Error", 0.0
    
    img = transform_image(image_bytes=image_bytes)
    ort_inputs = {ort_session.get_inputs()[0].name: img}
    ort_outs = ort_session.run(None, ort_inputs)

    img_out = sigmoid(ort_outs[0])
    predicted_idx = np.argmax(img_out[0])
    confidence = round(float(img_out[0][predicted_idx]) * 100, 2)
    return class_names[predicted_idx], confidence


def get_result(image_file, is_api=False):
    start_time = datetime.datetime.now()
    image_bytes = image_file.file.read()
    class_name, confidence = get_prediction(image_bytes)
    if not is_api:
        encoded_string = base64.b64encode(image_bytes)
        bs64 = encoded_string.decode('utf-8')
        image_data = f'data:image/jpeg;base64,{bs64}'
    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = f'{round(time_diff.total_seconds() * 1000)} ms'
    result = {
        "inference_time": execution_time,
        "predictions": {
            "class_name": class_name,
            "confidence": confidence
        }
    }
    if not is_api:
        result["image_data"] = image_data
    return result
