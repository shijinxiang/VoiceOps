import time
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from backend.app.models import WorkOrderModel, WorkflowTaskModel, SessionModel
from backend.app.schemas import WorkOrderConfirmRequest
from backend.app.services.n8n_service import n8n_service
from backend.app.config import settings

import uuid

class WorkOrderService:
    """
    Work Order Lifecycle & Human-in-the-loop (HITL) Service.
    Enforces idempotency, state transitions, and audit records.
    """

    @staticmethod
    def generate_ticket_number() -> str:
        timestamp_str = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        suffix = uuid.uuid4().hex[:6].upper()
        return f"WO-{timestamp_str}-{suffix}"

    async def confirm_and_create(
        self, 
        req: WorkOrderConfirmRequest, 
        db: AsyncSession
    ) -> WorkOrderModel:
        # 1. Idempotency Check (E07 Scenario)
        if req.idempotency_key:
            stmt = select(WorkOrderModel).where(WorkOrderModel.idempotency_key == req.idempotency_key)
            result = await db.execute(stmt)
            existing = result.scalars().first()
            if existing:
                # Return existing work order without duplicate creation
                return existing

        # 2. Verify Session exists
        session_stmt = select(SessionModel).where(SessionModel.id == req.session_id)
        session_res = await db.execute(session_stmt)
        session = session_res.scalars().first()
        if not session:
            raise HTTPException(status_code=404, detail="关联会话不存在 (Session not found)")

        # 3. Create Confirmed Work Order
        ticket_number = self.generate_ticket_number()
        work_order = WorkOrderModel(
            ticket_number=ticket_number,
            session_id=req.session_id,
            order_id=req.order_id,
            ticket_type=req.ticket_type,
            status="CONFIRMED",
            reason=req.reason,
            solution_proposal=req.solution_proposal,
            policy_citation=req.policy_citation,
            idempotency_key=req.idempotency_key,
            confirmed_by=req.confirmed_by,
            confirmed_at=datetime.utcnow()
        )
        db.add(work_order)
        await db.flush()

        # Update Session status
        session.status = "completed"

        # 4. Trigger n8n Automation Webhook
        notify_payload = {
            "ticket_number": ticket_number,
            "session_id": req.session_id,
            "order_id": req.order_id,
            "ticket_type": req.ticket_type,
            "solution_proposal": req.solution_proposal,
            "confirmed_by": req.confirmed_by
        }
        n8n_result = await n8n_service.trigger_notification(notify_payload)

        # 5. Record Workflow Task
        task = WorkflowTaskModel(
            work_order_id=work_order.id,
            webhook_url=settings.N8N_WEBHOOK_URL,
            request_payload=notify_payload,
            response_payload=n8n_result,
            status=n8n_result.get("status", "callback_succeeded")
        )
        db.add(task)
        await db.commit()
        await db.refresh(work_order)

        return work_order

work_order_service = WorkOrderService()
