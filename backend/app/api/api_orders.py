from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.app.services.order_service import order_service
from backend.app.schemas import OrderResponse

router = APIRouter()

@router.get("/lookup", response_model=OrderResponse)
async def lookup_order(order_id: str = Query(..., description="订单号")):
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在 (Order does not exist)")
    return order

@router.get("", response_model=List[OrderResponse])
async def list_orders():
    return order_service.list_all()
