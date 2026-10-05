from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Sessions
class SessionCreate(BaseModel):
    customer_phone: Optional[str] = None
    customer_name: Optional[str] = None
    channel: str = "web_upload"

class SessionResponse(BaseModel):
    id: str
    session_code: str
    customer_name_masked: Optional[str] = None
    customer_phone_masked: Optional[str] = None
    channel: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Audio Upload
class AudioUploadResponse(BaseModel):
    id: str
    session_id: str
    original_filename: str
    file_size_bytes: int
    duration_seconds: float
    mime_type: str
    audio_hash: Optional[str]

# Transcriptions
class TranscriptionEditRequest(BaseModel):
    edited_text: str
    revision_note: Optional[str] = None

class TranscriptionResponse(BaseModel):
    id: str
    session_id: str
    masked_text: str
    is_manually_edited: bool
    edited_text: Optional[str] = None
    status: str
    asr_model: str
    processing_time_ms: int
    cer_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Orders
class OrderResponse(BaseModel):
    order_id: str
    customer_name: str
    customer_phone: str
    product_name: str
    order_amount: float
    purchase_date: datetime
    delivery_date: Optional[datetime] = None
    shipping_company: Optional[str] = None
    tracking_number: Optional[str] = None
    shipping_status: str
    warranty_expire_date: Optional[datetime] = None

    class Config:
        from_attributes = True

# Work Orders
class WorkOrderConfirmRequest(BaseModel):
    session_id: str
    order_id: Optional[str] = None
    ticket_type: str
    reason: Optional[str] = None
    solution_proposal: str
    policy_citation: List[Dict[str, Any]] = []
    idempotency_key: str
    confirmed_by: str = "Agent-001"

class WorkOrderResponse(BaseModel):
    id: str
    ticket_number: str
    session_id: str
    order_id: Optional[str] = None
    ticket_type: str
    status: str
    reason: Optional[str] = None
    solution_proposal: str
    policy_citation: List[Dict[str, Any]]
    idempotency_key: Optional[str] = None
    confirmed_by: Optional[str] = None
    confirmed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Agent Traces
class AgentTraceResponse(BaseModel):
    id: str
    session_id: str
    step_index: int
    action_type: str
    input_payload: Dict[str, Any]
    output_payload: Dict[str, Any]
    latency_ms: int
    created_at: datetime

    class Config:
        from_attributes = True

# n8n Webhook Callback
class N8nCallbackRequest(BaseModel):
    ticket_number: str
    status: str  # callback_succeeded, failed
    channel: str = "email"
    response_payload: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
