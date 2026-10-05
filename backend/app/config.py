from pydantic_settings import BaseSettings
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "VoiceOps"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite+aiosqlite:///{BASE_DIR}/voiceops.db"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Storage
    STORAGE_DIR: str = os.getenv("STORAGE_DIR", str(BASE_DIR / "storage"))
    
    # n8n Webhook configuration
    N8N_WEBHOOK_URL: str = os.getenv(
        "N8N_WEBHOOK_URL", 
        "http://localhost:5678/webhook/voiceops-workorder"
    )
    MOCK_NOTIFICATION_WEBHOOK: bool = True
    
    # RAG parameters
    RAG_SIMILARITY_THRESHOLD: float = 0.55
    RAG_TOP_K: int = 3
    
    # Hardware & Latency Budgets
    MAX_AUDIO_SIZE_BYTES: int = 50 * 1024 * 1024  # 50MB
    MAX_AUDIO_DURATION_SECONDS: float = 600.0     # 10 minutes
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
Path(settings.STORAGE_DIR).mkdir(parents=True, exist_ok=True)
