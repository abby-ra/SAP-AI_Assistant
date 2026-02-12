"""
Backend startup script for SAP AI Assistant
Run this to start the FastAPI server
"""
import uvicorn
from backend.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=settings.app_port,
        reload=True,
        log_level="info"
    )
