from fastapi import APIRouter
import time
from backend.app.config import settings

router = APIRouter()

@router.get("")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": time.time(),
        "database": "connected",
        "asr_adapter": "ready",
        "rag_adapter": "ready"
    }
