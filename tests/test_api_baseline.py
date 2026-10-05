import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
import io
import wave
import struct

from backend.app.main import app
from backend.app.database import engine, Base

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

def make_test_wav(duration_s=1.0, is_silent=False):
    buf = io.BytesIO()
    sample_rate = 16000
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        n = int(sample_rate * duration_s)
        samples = []
        for i in range(n):
            if is_silent:
                val = 0
            else:
                val = int(10000 * (1 if (i // 100) % 2 == 0 else -1))
            samples.append(val)
        raw = struct.pack(f"<{n}h", *samples)
        wf.writeframes(raw)
    buf.seek(0)
    return buf.read()

@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/api/v1/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_session_lifecycle_and_audio():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Create Session
        res = await ac.post("/api/v1/sessions", json={
            "customer_name": "张伟",
            "customer_phone": "13812345678",
            "channel": "web_upload"
        })
        assert res.status_code == 200
        session_data = res.json()
        session_id = session_data["id"]
        assert session_data["customer_phone_masked"] == "138****5678"
        assert session_data["customer_name_masked"] == "张*"

        # 2. Upload Corrupted/Empty Audio (E01)
        res = await ac.post("/api/v1/audio/upload", data={"session_id": session_id}, files={"file": ("empty.wav", b"", "audio/wav")})
        assert res.status_code == 400

        # 3. Upload Silent Audio (E03)
        silent_wav = make_test_wav(duration_s=1.0, is_silent=True)
        res = await ac.post("/api/v1/audio/upload", data={"session_id": session_id}, files={"file": ("silent.wav", silent_wav, "audio/wav")})
        assert res.status_code == 422

        # 4. Upload Valid Audio
        valid_wav = make_test_wav(duration_s=2.5, is_silent=False)
        res = await ac.post("/api/v1/audio/upload", data={"session_id": session_id}, files={"file": ("clean_01.wav", valid_wav, "audio/wav")})
        assert res.status_code == 200
        audio_id = res.json()["id"]

        # 5. Process ASR Transcription
        res = await ac.post(f"/api/v1/transcriptions/process/{audio_id}")
        assert res.status_code == 200
        trans_data = res.json()
        assert "masked_text" in trans_data
        trans_id = trans_data["id"]

        # 6. Manual Revision of Transcription
        res = await ac.put(f"/api/v1/transcriptions/{trans_id}/edit", json={
            "edited_text": "你好我上周五买的降噪耳机订单号是ORD-20261001-8848，右耳充不进电申请换货。"
        })
        assert res.status_code == 200
        assert res.json()["is_manually_edited"] is True

        # 7. Run Agent Analysis & Tracing
        res = await ac.post("/api/v1/agent/run", json={"session_id": session_id})
        assert res.status_code == 200
        agent_data = res.json()
        assert agent_data["intent"] in ["REPAIR", "RETURN"]
        assert len(agent_data["traces"]) >= 3

        # 8. Human-in-the-loop Confirm Work Order
        res = await ac.post("/api/v1/work-orders/confirm", json={
            "session_id": session_id,
            "order_id": "ORD-20261001-8848",
            "ticket_type": "REPAIR",
            "reason": "右耳充不进电",
            "solution_proposal": "符合15天换新政策，顺丰免费寄修换新",
            "idempotency_key": "IDEM-TEST-001",
            "confirmed_by": "Agent-001"
        })
        assert res.status_code == 200
        wo_data = res.json()
        assert wo_data["status"] == "CONFIRMED"
        ticket_number = wo_data["ticket_number"]

        # 9. Test Idempotency (E07 Scenario)
        res_dup = await ac.post("/api/v1/work-orders/confirm", json={
            "session_id": session_id,
            "order_id": "ORD-20261001-8848",
            "ticket_type": "REPAIR",
            "solution_proposal": "符合15天换新政策",
            "idempotency_key": "IDEM-TEST-001"
        })
        assert res_dup.status_code == 200
        assert res_dup.json()["ticket_number"] == ticket_number  # Exactly same ticket!

        # 10. n8n Status Callback
        res_cb = await ac.post("/api/v1/webhook/n8n/callback", json={
            "ticket_number": ticket_number,
            "status": "callback_succeeded",
            "channel": "email"
        })
        assert res_cb.status_code == 200
        assert res_cb.json()["updated_status"] == "SYNCED_N8N"
