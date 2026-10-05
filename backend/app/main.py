from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.app.config import settings
from backend.app.database import engine, Base
from backend.app.api.api_sessions import router as sessions_router
from backend.app.api.api_audio import router as audio_router
from backend.app.api.api_transcriptions import router as transcriptions_router
from backend.app.api.api_agent import router as agent_router
from backend.app.api.api_orders import router as orders_router
from backend.app.api.api_work_orders import router as work_orders_router
from backend.app.api.api_webhook import router as webhook_router
from backend.app.api.api_health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="企业语音售后智能平台 (VoiceOps Enterprise After-Sales Audio Intelligence Platform)",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers under /api/v1
prefix = settings.API_V1_PREFIX
app.include_router(health_router, prefix=f"{prefix}/health", tags=["Health"])
app.include_router(sessions_router, prefix=f"{prefix}/sessions", tags=["Sessions"])
app.include_router(audio_router, prefix=f"{prefix}/audio", tags=["Audio"])
app.include_router(transcriptions_router, prefix=f"{prefix}/transcriptions", tags=["Transcriptions"])
app.include_router(agent_router, prefix=f"{prefix}/agent", tags=["Agent"])
app.include_router(orders_router, prefix=f"{prefix}/orders", tags=["Orders"])
app.include_router(work_orders_router, prefix=f"{prefix}/work-orders", tags=["Work Orders"])
app.include_router(webhook_router, prefix=f"{prefix}/webhook/n8n", tags=["n8n Webhook"])

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "docs_url": "/docs",
        "health_check": f"{prefix}/health"
    }
