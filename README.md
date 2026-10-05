# CloudWelcome - FastAPI & Python Demo Application

An interactive, modern full-stack web application built with **FastAPI**, **Python 3.11+**, and vanilla HTML5/CSS/JavaScript designed to welcome users with personalized greetings, visitor analytics, dynamic micro-interactions (confetti and glassmorphism UI), and Azure deployment readiness.

---

## 🌟 Key Features

- **Personalized Greeting Engine**: Generates customized welcome notes based on user name, role/title, and tone style (Warm & Friendly, Professional, Futuristic AI, Playful).
- **Modern Responsive Frontend**:
  - Dark mode aesthetic with glassmorphic cards, radiant purple/cyan gradient glow, and smooth animations.
  - Interactive greeting form with instant visual card presentation.
  - Celebration confetti effect with pure HTML5 Canvas (zero external bloated dependencies).
  - Quick action to copy personalized greetings.
- **Visitor Telemetry & Community Lounge**:
  - Live visitor feed showing recent check-ins and avatars.
  - Metrics tracking total visitors and server uptime.
- **Production & Cloud Ready**:
  - `GET /api/health` probe endpoint for Azure liveness/readiness probes.
  - Auto-generated interactive Swagger UI documentation at `/docs` and ReDoc at `/redoc`.
  - Docker containerization (`Dockerfile` and `.dockerignore`) optimized for **Azure App Service** and **Azure Container Apps**.

---

## 📁 Project Architecture

```text
Azure Deployement/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI endpoints, static files, and business logic
│   ├── models.py          # Pydantic data schemas
│   └── static/            # Static assets
│       ├── index.html     # Semantic, accessible HTML5 dashboard
│       ├── css/
│       │   └── style.css  # Modern responsive styles & animations
│       └── js/
│           └── app.js     # Client-side API integration & confetti
├── tests/
│   └── test_app.py        # Automated test suite (Pytest + TestClient)
├── Dockerfile             # Production multi-stage Docker build
├── .dockerignore
├── .gitignore
├── requirements.txt       # Dependencies (fastapi, uvicorn, pydantic)
├── run.py                 # Convenience local runner
└── README.md              # Documentation
```

---

## 🚀 Getting Started Locally

### 1. Prerequisites
- Python 3.10 or higher installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
You can run using the convenience script:
```bash
python run.py
```
Or directly with Uvicorn:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 4. Access the Application
- **Frontend Welcome Dashboard**: Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Health Check Endpoint**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## 🧪 Running Automated Tests

Run the test suite using pytest:
```bash
python -m pytest tests/test_app.py -v
```

---

## ☁️ Azure Deployment Guide

### Option A: Azure Container Apps (Recommended)

1. **Build and push the Docker image to Azure Container Registry (ACR)**:
   ```bash
   az acr build --registry <your-acr-name> --image welcome-portal:latest .
   ```

2. **Deploy to Azure Container Apps**:
   ```bash
   az containerapp create \
     --name welcome-app \
     --resource-group <your-resource-group> \
     --environment <your-environment-name> \
     --image <your-acr-name>.azurecr.io/welcome-portal:latest \
     --target-port 8000 \
     --ingress external \
     --query properties.configuration.ingress.fqdn
   ```

### Option B: Azure App Service (Linux Web App)

1. **Direct Zip/Code Deployment**:
   - Set the startup command in Azure Portal under **Configuration -> General Settings**:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port 8000
     ```
   - Deploy code via Azure CLI or VS Code Azure Tools extension:
     ```bash
     az webapp up --name <unique-app-name> --resource-group <your-rg> --runtime "PYTHON:3.11"
     ```

2. **Health Probe Configuration**:
   - Path: `/api/health`
   - Port: `8000`

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the frontend single-page web application |
| `GET` | `/api/welcome` | Returns platform greeting metadata and visitor count |
| `POST` | `/api/welcome` | Generates personalized greeting and adds visitor to log |
| `GET` | `/api/visitors` | Lists recent visitor history |
| `GET` | `/api/health` | Health probe returning uptime, status, and environment |
| `GET` | `/docs` | OpenAPI / Swagger interactive documentation |
