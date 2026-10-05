from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime
from backend.app.database import get_db
from backend.app.models import SessionModel, AudioFileModel, TranscriptionModel, WorkOrderModel, AgentTraceModel
from backend.app.schemas import SessionCreate, SessionResponse
from backend.app.services.masking_service import masking_service

router = APIRouter()

@router.post("", response_model=SessionResponse)
async def create_session(req: SessionCreate, db: AsyncSession = Depends(get_db)):
    code_suffix = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    session = SessionModel(
        session_code=f"SESS-{code_suffix}",
        customer_name_masked=masking_service.mask_name(req.customer_name or ""),
        customer_phone_masked=masking_service.mask_phone(req.customer_phone or ""),
        channel=req.channel,
        status="created"
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

@router.get("", response_model=List[SessionResponse])
async def list_sessions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(SessionModel).order_by(SessionModel.created_at.desc()).offset(offset).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/{session_id}")
async def get_session_detail(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(SessionModel)
        .options(
            selectinload(SessionModel.audio_files),
            selectinload(SessionModel.transcriptions),
            selectinload(SessionModel.work_orders),
            selectinload(SessionModel.traces)
        )
        .where(SessionModel.id == session_id)
    )
    res = await db.execute(stmt)
    session = res.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在 (Session not found)")

    return {
        "id": session.id,
        "session_code": session.session_code,
        "customer_name_masked": session.customer_name_masked,
        "customer_phone_masked": session.customer_phone_masked,
        "channel": session.channel,
        "status": session.status,
        "created_at": session.created_at,
        "audio_files": session.audio_files,
        "transcriptions": session.transcriptions,
        "work_orders": session.work_orders,
        "traces": sorted(session.traces, key=lambda t: t.step_index)
    }
