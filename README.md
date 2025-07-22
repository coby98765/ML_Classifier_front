# 🧠 Naive Bayes Classifier – Streamlit Frontend

This is a simple web interface built with **Streamlit** that lets users:
- Train Naive Bayes models on tabular datasets
- Classify new samples using trained models
- View prediction confidence levels
- Communicate with a **FastAPI** backend via HTTP

---

## 🚀 Features

- 📂 Upload dataset by URL and train a new model
- 🔄 Dynamically load model architecture for form generation
- 🧾 Classify inputs and get prediction results with confidence scores
- 🌀 Includes loading animations and form validation

---

## 📦 Requirements

Python 3.9+  
Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🏁 Getting Started

### 1. Set Backend URL

Set the backend API URL as an environment variable:

**Linux/Mac:**
```bash
export BACKEND_URL="http://localhost:8000"
```

**Windows CMD:**
```cmd
set BACKEND_URL=http://localhost:8000
```

**Windows PowerShell:**
```powershell
$env:BACKEND_URL="http://localhost:8000"
```

---

### 2. Run Streamlit App

```bash
streamlit run Home.py
```

---

## 🗂 Project Structure

```
front/
├── Home.py                  # Entry point (optional)
├── pages/
│   ├── 1_Train_Model.py    # Train new model from CSV URL
│   └── 2_Classify.py       # Classify new inputs using selected model
├── requirements.txt
└── README.md
```

---

## 📡 Backend API Contract

The frontend expects the FastAPI backend to implement:

- `POST /train`  
  Payload: `{ "name": "model_name", "file": "csv_url" }`  
  Response: `{ "model": "model_name", "accuracy": 95.4 }`

- `GET /models`  
  Response: `["model1", "model2", ...]`

- `GET /models/{model_name}`  
  Response: `{ "model": "model_name", "arc": { feature: [options...] } }`

- `POST /classify/{model_name}`  
  Payload: `{ feature1: value, feature2: value, ... }`  
  Response:  
  ```json
  {
    "result": "-1",
    "rate": {
      "1": 1.03,
      "-1": 98.97
    }
  }
  ```

---

## 🐳 Running with Docker

You can containerize this Streamlit app to deploy it anywhere using Docker.

### 1. Create a `Dockerfile`

```dockerfile
# Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose default Streamlit port
EXPOSE 8501

# Set environment variable for backend URL (can also be set via docker run)
ENV BACKEND_URL=http://localhost:8000

# Launch app
CMD ["streamlit", "run", "Home.py", "--server.headless=true", "--server.port=8501", "--server.enableCORS=false"]
```
---
### 2. Build the Docker image
```commandline
docker build -t bayes-front .
```

---
### 3. Run the container
```commandline
docker run -p 8501:8501 -e BACKEND_URL="http://your-backend-host:8000" bayes-front
```

---

## 🧑‍💻 Author

Built by @coby98765

Inspired by a Naive Bayes learning project

