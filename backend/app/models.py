from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey, JSON, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from backend.app.database import Base

def gen_uuid():
    return str(uuid.uuid4())

class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    session_code = Column(String(64), unique=True, index=True)
    customer_name_masked = Column(String(64), nullable=True)
    customer_phone_masked = Column(String(32), nullable=True)
    channel = Column(String(32), default="web_upload")
    status = Column(String(32), default="created")  # created, processing, pending_confirmation, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    audio_files = relationship("AudioFileModel", back_populates="session", cascade="all, delete-orphan")
    transcriptions = relationship("TranscriptionModel", back_populates="session", cascade="all, delete-orphan")
    work_orders = relationship("WorkOrderModel", back_populates="session", cascade="all, delete-orphan")
    traces = relationship("AgentTraceModel", back_populates="session", cascade="all, delete-orphan")


class AudioFileModel(Base):
    __tablename__ = "audio_files"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    original_filename = Column(String(255), nullable=False)
    storage_path = Column(String(512), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    duration_seconds = Column(Float, default=0.0)
    mime_type = Column(String(64), default="audio/wav")
    audio_hash = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("SessionModel", back_populates="audio_files")


class TranscriptionModel(Base):
    __tablename__ = "transcriptions"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    raw_text = Column(Text, nullable=True)
    masked_text = Column(Text, nullable=False)
    is_manually_edited = Column(Boolean, default=False)
    edited_text = Column(Text, nullable=True)
    status = Column(String(32), default="pending")  # pending, running, succeeded, failed
    asr_model = Column(String(64), default="Paraformer-large-zh")
    processing_time_ms = Column(Integer, default=0)
    cer_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    session = relationship("SessionModel", back_populates="transcriptions")


class OrderModel(Base):
    __tablename__ = "orders"

    order_id = Column(String(64), primary_key=True)
    customer_name = Column(String(64), nullable=False)
    customer_phone = Column(String(32), nullable=False)
    product_name = Column(String(128), nullable=False)
    order_amount = Column(Numeric(10, 2), default=0.0)
    purchase_date = Column(DateTime, nullable=False)
    delivery_date = Column(DateTime, nullable=True)
    shipping_company = Column(String(64), nullable=True)
    tracking_number = Column(String(64), nullable=True)
    shipping_status = Column(String(32), default="delivering")
    warranty_expire_date = Column(DateTime, nullable=True)


class WorkOrderModel(Base):
    __tablename__ = "work_orders"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    ticket_number = Column(String(64), unique=True, index=True)
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    order_id = Column(String(64), nullable=True)
    ticket_type = Column(String(32), nullable=False)  # RETURN, REPAIR, LOGISTICS_EXPEDITE, LOGISTICS_RESEND, etc.
    status = Column(String(32), default="DRAFT")      # DRAFT, PENDING_CONFIRMATION, CONFIRMED, SYNCED_N8N, REJECTED
    reason = Column(Text, nullable=True)
    solution_proposal = Column(Text, nullable=False)
    policy_citation = Column(JSON, default=list)
    idempotency_key = Column(String(64), unique=True, index=True, nullable=True)
    confirmed_by = Column(String(64), nullable=True)
    confirmed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    session = relationship("SessionModel", back_populates="work_orders")
    workflow_tasks = relationship("WorkflowTaskModel", back_populates="work_order", cascade="all, delete-orphan")


class AgentTraceModel(Base):
    __tablename__ = "agent_traces"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    step_index = Column(Integer, default=1)
    action_type = Column(String(64), nullable=False)
    input_payload = Column(JSON, default=dict)
    output_payload = Column(JSON, default=dict)
    latency_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("SessionModel", back_populates="traces")


class WorkflowTaskModel(Base):
    __tablename__ = "workflow_tasks"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    work_order_id = Column(String(36), ForeignKey("work_orders.id"), nullable=False)
    webhook_url = Column(String(512), nullable=False)
    request_payload = Column(JSON, default=dict)
    response_payload = Column(JSON, default=dict)
    retry_count = Column(Integer, default=0)
    status = Column(String(32), default="pending")  # pending, dispatched, callback_succeeded, failed
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    work_order = relationship("WorkOrderModel", back_populates="workflow_tasks")


class KnowledgeChunkModel(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    policy_code = Column(String(32), index=True)
    category = Column(String(32), index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    embedding_vector = Column(JSON, nullable=True)  # Stored as JSON list of floats for portable sqlite / pgvector
    created_at = Column(DateTime, default=datetime.utcnow)
