from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from backend.app.database import get_db
from backend.app.models import WorkOrderModel
from backend.app.schemas import WorkOrderConfirmRequest, WorkOrderResponse
from backend.app.services.work_order_service import work_order_service

router = APIRouter()

@router.post("/confirm", response_model=WorkOrderResponse)
async def confirm_work_order(
    req: WorkOrderConfirmRequest, 
    db: AsyncSession = Depends(get_db)
):
    work_order = await work_order_service.confirm_and_create(req, db)
    return work_order

@router.get("", response_model=List[WorkOrderResponse])
async def list_work_orders(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(WorkOrderModel)
        .order_by(WorkOrderModel.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/{ticket_number}", response_model=WorkOrderResponse)
async def get_work_order(ticket_number: str, db: AsyncSession = Depends(get_db)):
    stmt = select(WorkOrderModel).where(WorkOrderModel.ticket_number == ticket_number)
    res = await db.execute(stmt)
    wo = res.scalars().first()
    if not wo:
        raise HTTPException(status_code=404, detail="工单不存在 (Work order not found)")
    return wo
