from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any
from backend.app.database import get_db
from backend.app.models import SessionModel, TranscriptionModel, AgentTraceModel, WorkOrderModel
from backend.app.services.agent_service import agent_service
from backend.app.services.masking_service import masking_service

router = APIRouter()

@router.post("/run")
async def run_agent_analysis(
    payload: Dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_db)
):
    session_id = payload.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="缺少 session_id 参数")

    # Get latest transcription
    stmt = (
        select(TranscriptionModel)
        .where(TranscriptionModel.session_id == session_id)
        .order_by(TranscriptionModel.created_at.desc())
    )
    res = await db.execute(stmt)
    transcription = res.scalars().first()
    if not transcription:
        raise HTTPException(status_code=400, detail="该会话尚无转写内容，无法进行分析 (No transcription found)")

    # Use edited text if available, otherwise masked text
    text_to_process = transcription.edited_text or transcription.masked_text

    # Run Agent reasoning
    result = await agent_service.analyze_and_draft(text_to_process, session_id)

    # Persist traces to database
    for trace_item in result["traces"]:
        trace_record = AgentTraceModel(
            session_id=session_id,
            step_index=trace_item["step_index"],
            action_type=trace_item["action_type"],
            input_payload=masking_service.sanitize_for_audit_log(trace_item["input_payload"]),
            output_payload=masking_service.sanitize_for_audit_log(trace_item["output_payload"]),
            latency_ms=trace_item["latency_ms"]
        )
        db.add(trace_record)

    # Update session status
    sess_stmt = select(SessionModel).where(SessionModel.id == session_id)
    sess_res = await db.execute(sess_stmt)
    session = sess_res.scalars().first()
    if session:
        session.status = "pending_confirmation" if result["requires_human_confirm"] else "analyzed"

    await db.commit()
    return result
