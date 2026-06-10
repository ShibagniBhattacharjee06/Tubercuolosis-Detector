# 🫁 Tuberculosis Detector

An AI-powered Tuberculosis Detection System that analyzes Chest X-Ray images using Deep Learning to assist in the early identification of Tuberculosis (TB). This project is one of the core diagnostic modules within the **Medicare Healthcare Platform**, a unified ecosystem that integrates multiple AI-powered healthcare services into a single application.

## 🌐 Live Demo

### Tuberculosis Detection Module
🔗 https://tubercuolosis-detector.vercel.app

### Medicare Main Platform
🔗 https://medicare-beryl.vercel.app

---

# 📖 About The Project

Tuberculosis remains one of the world's most prevalent infectious diseases, particularly affecting developing and resource-constrained regions where access to radiologists and healthcare specialists may be limited.

The Tuberculosis Detector leverages Deep Learning and Medical Image Analysis to automatically examine Chest X-Ray images and identify signs of Tuberculosis with high accuracy.

Developed as a specialized AI service within the Medicare ecosystem, this module can function independently or seamlessly integrate with the Medicare platform, enabling users to access multiple healthcare diagnostic tools from a centralized dashboard.

The goal is to support healthcare professionals with faster preliminary screening and improve healthcare accessibility through AI-assisted diagnosis.

---

# 🏥 Medicare Ecosystem

This project is part of the larger **Medicare Healthcare Platform**, where multiple independently deployed AI services work together to provide comprehensive healthcare assistance.

### Medicare Modules

- 🫁 Tuberculosis Detection System
- 🦴 Fracture Detection System
- 🧠 Brain Tumor Detection System
- 🩺 AI Skin Disease Assistant
- 🤖 AI Doctor Assistant
- 👩‍⚕️ ASHA Worker Management Portal

Each module is developed, trained, deployed, and maintained independently while remaining connected through the Medicare platform.

```text
                     Medicare Platform
                 (medicare-beryl.vercel.app)

                              │
     ┌────────────┬────────────┬────────────┬────────────┐
     │            │            │            │            │
 Tuberculosis  Fracture    Brain Tumor    Skin AI    AI Doctor
   Service      Service      Service      Service      Service

         │
         ▼

tubercuolosis-detector.vercel.app
```

---

# 🎯 Problem Statement

Tuberculosis diagnosis often requires expert radiological examination and can be time-consuming, especially in healthcare systems facing resource constraints.

This project aims to:

- Assist in early Tuberculosis screening
- Reduce diagnostic delays
- Improve healthcare accessibility
- Support healthcare professionals with AI-assisted analysis
- Provide rapid Chest X-Ray interpretation

The system serves as a diagnostic support tool and is not intended to replace professional medical evaluation.

---

# 🚀 Features

## Automated Chest X-Ray Analysis

Users can upload Chest X-Ray images directly through the web interface for instant analysis.

---

## Binary Disease Classification

The model classifies X-Ray scans into:

- Tuberculosis
- Normal

---

## Confidence Score Generation

Every prediction is accompanied by a confidence score, allowing users and healthcare professionals to assess prediction reliability.

---

## Real-Time Inference

The system performs rapid image analysis and generates results within seconds.

---

## User-Friendly Dashboard

Provides:

- X-Ray Preview
- Prediction Result
- Confidence Score
- Simple Healthcare Interface

---

## Medicare Integration

The module operates both:

- As an independent application
- As a fully integrated Medicare diagnostic service

---

# 🏗️ System Architecture

```text
                     User Uploads
                   Chest X-Ray Image
                            │
                            ▼
                   Image Preprocessing
                            │
                            ▼
                    Image Normalization
                            │
                            ▼
                    DenseNet-121 Model
                            │
                            ▼
                    Feature Extraction
                            │
                            ▼
                   Binary Classification
                            │
                            ▼
                   Confidence Calculation
                            │
                            ▼
                     Prediction Output
```

---

# 🧠 AI Model Architecture

The Tuberculosis Detection System utilizes **DenseNet-121**, a powerful Convolutional Neural Network architecture known for efficient feature propagation and strong performance in medical image classification tasks.

### Why DenseNet-121?

- Efficient feature reuse
- Reduced parameter count
- Strong medical imaging performance
- Better gradient flow
- High classification accuracy

The model is trained on Chest X-Ray datasets containing both normal and tuberculosis-positive cases.

---

# 🔄 Model Workflow

### Step 1: Image Upload

The user uploads a Chest X-Ray image.

### Step 2: Preprocessing

The image is resized, normalized, and prepared for model inference.

### Step 3: Feature Extraction

DenseNet-121 extracts complex pulmonary features from the image.

### Step 4: Prediction

The model determines whether the scan indicates Tuberculosis or Normal conditions.

### Step 5: Confidence Generation

A confidence score is calculated for the prediction.

### Step 6: Result Display

The final result is displayed through the user interface.

---

# 🛠️ Technology Stack

## Frontend

- React.js
- Vite
- Tailwind CSS

## Backend

- Python
- Flask

## Artificial Intelligence

- TensorFlow
- Keras
- DenseNet-121
- OpenCV
- NumPy
- Pandas

## Deployment

- Vercel
- Render

---

# 📊 Performance Highlights

The model demonstrates strong performance across evaluation metrics.

### Achievements

- Accuracy: ~98%
- High Precision
- High Recall
- Strong F1-Score
- Low False Negative Rate
- Fast Inference Speed

The model is optimized to minimize missed Tuberculosis cases, making recall a particularly important evaluation metric.

---

# 💡 Key Engineering Highlights

### Modular AI Service

Developed as an independent microservice that can be updated without affecting other Medicare modules.

### Scalable Integration

Connected to the Medicare platform through API-based communication.

### Cloud Deployment

Supports real-time predictions through cloud-hosted infrastructure.

### Maintainable Architecture

Follows a modular design for future expansion and enhancements.

---

# 🔮 Future Enhancements

- Explainable AI using Grad-CAM
- Heatmap Visualization of Infected Regions
- Multi-Disease Chest X-Ray Detection
- Mobile Application Integration
- Offline Inference Support
- Electronic Health Record Integration
- Clinical Decision Support Features

---

# 📌 Project Links

## Tuberculosis Detection System

### Live Demo
🔗 https://tubercuolosis-detector.vercel.app

### GitHub Repository
🔗 [Add Repository Link]

---

## Medicare Healthcare Platform

### Live Demo
🔗 https://medicare-beryl.vercel.app

### GitHub Repository
🔗 [Add Medicare Repository Link]

---

# ⚠️ Disclaimer

This project is intended for educational, research, and healthcare assistance purposes only. The predictions generated by the model should not be considered a replacement for professional medical diagnosis, clinical judgment, or treatment recommendations.

---

# 👨‍💻 Developer

**Shibagni Bhattacharjee**

B.Tech Computer Science Engineering  
University of Engineering & Management, Jaipur

⭐ If you found this project useful, consider giving the repository a star.
