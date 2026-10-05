from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from backend.app.database import get_db
from backend.app.models import WorkOrderModel, WorkflowTaskModel
from backend.app.schemas import N8nCallbackRequest

router = APIRouter()

@router.post("/callback")
async def n8n_callback(req: N8nCallbackRequest, db: AsyncSession = Depends(get_db)):
    """
    Receives notification callback from n8n automation workflow.
    """
    stmt = select(WorkOrderModel).where(WorkOrderModel.ticket_number == req.ticket_number)
    res = await db.execute(stmt)
    wo = res.scalars().first()
    if not wo:
        raise HTTPException(status_code=404, detail="工单未找到")

    # Update WorkOrder status
    if req.status == "callback_succeeded":
        wo.status = "SYNCED_N8N"
    else:
        wo.status = "NOTIFICATION_FAILED"
    wo.updated_at = datetime.utcnow()

    # Update Task record
    task_stmt = select(WorkflowTaskModel).where(WorkflowTaskModel.work_order_id == wo.id)
    task_res = await db.execute(task_stmt)
    task = task_res.scalars().first()
    if task:
        task.status = req.status
        task.response_payload = req.response_payload or {}
        task.last_error = req.error_message
        task.updated_at = datetime.utcnow()

    await db.commit()
    return {"status": "ok", "ticket_number": req.ticket_number, "updated_status": wo.status}
