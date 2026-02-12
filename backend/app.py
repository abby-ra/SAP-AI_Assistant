from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.config import settings
from backend.services.model_service import run_model_test
import os

app = FastAPI(title="SAP Enterprise AI Assistant", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from frontend directory
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
def serve_frontend():
    """Serve the frontend HTML"""
    frontend_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Frontend not found"}


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "environment": settings.app_env}


@app.get("/api/model-test")
def model_test() -> dict:
    return run_model_test()


@app.post("/api/analyze")
def analyze(request: dict) -> dict:
    """Analyze a business query using AI"""
    query = request.get("query", "").strip()
    
    if not query:
        return {
            "status": "error",
            "analysis": "Please provide a query to analyze.",
            "query": ""
        }
    
    from backend.services.model_service import analyze_business_query
    return analyze_business_query(query)
