from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.database import get_db
from backend.app.models import SessionModel, AudioFileModel
from backend.app.schemas import AudioUploadResponse
from backend.app.services.audio_service import audio_service

router = APIRouter()

@router.post("/upload", response_model=AudioUploadResponse)
async def upload_audio(
    session_id: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Verify Session
    stmt = select(SessionModel).where(SessionModel.id == session_id)
    res = await db.execute(stmt)
    session = res.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="关联会话不存在 (Session not found)")

    # Validate audio format, size, duration, energy
    audio_meta = await audio_service.validate_and_save(session_id, file)

    audio_record = AudioFileModel(
        session_id=session_id,
        original_filename=audio_meta["original_filename"],
        storage_path=audio_meta["storage_path"],
        file_size_bytes=audio_meta["file_size_bytes"],
        duration_seconds=audio_meta["duration_seconds"],
        mime_type=audio_meta["mime_type"],
        audio_hash=audio_meta["audio_hash"]
    )
    db.add(audio_record)
    session.status = "processing"
    await db.commit()
    await db.refresh(audio_record)

    return audio_record
