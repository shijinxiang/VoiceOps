from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from backend.app.database import get_db
from backend.app.models import SessionModel, AudioFileModel, TranscriptionModel
from backend.app.schemas import TranscriptionResponse, TranscriptionEditRequest
from backend.app.services.asr_service import asr_service
from backend.app.services.masking_service import masking_service

router = APIRouter()

@router.post("/process/{audio_id}", response_model=TranscriptionResponse)
async def process_transcription(audio_id: str, db: AsyncSession = Depends(get_db)):
    # Retrieve audio
    stmt = select(AudioFileModel).where(AudioFileModel.id == audio_id)
    res = await db.execute(stmt)
    audio = res.scalars().first()
    if not audio:
        raise HTTPException(status_code=404, detail="音频文件不存在 (Audio record not found)")

    # Call ASR pipeline
    asr_res = await asr_service.transcribe(audio.storage_path, audio.original_filename)

    record = TranscriptionModel(
        session_id=audio.session_id,
        raw_text=asr_res["raw_text"],
        masked_text=asr_res["masked_text"],
        status="succeeded",
        asr_model=asr_res["asr_model"],
        processing_time_ms=asr_res["processing_time_ms"]
    )
    db.add(record)

    # Update session status
    sess_stmt = select(SessionModel).where(SessionModel.id == audio.session_id)
    sess_res = await db.execute(sess_stmt)
    session = sess_res.scalars().first()
    if session:
        session.status = "transcribed"

    await db.commit()
    await db.refresh(record)
    return record


@router.put("/{transcription_id}/edit", response_model=TranscriptionResponse)
async def edit_transcription(
    transcription_id: str, 
    req: TranscriptionEditRequest, 
    db: AsyncSession = Depends(get_db)
):
    stmt = select(TranscriptionModel).where(TranscriptionModel.id == transcription_id)
    res = await db.execute(stmt)
    record = res.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail="转写记录不存在 (Transcription not found)")

    # Save manual edit with masking
    record.is_manually_edited = True
    record.edited_text = req.edited_text
    record.masked_text = masking_service.mask_text(req.edited_text)
    record.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(record)
    return record
