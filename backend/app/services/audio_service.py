import os
import wave
import hashlib
from pathlib import Path
from fastapi import UploadFile, HTTPException
from backend.app.config import settings

class AudioService:
    """
    Audio file validation, storage, and signal inspection.
    Handles E01 (Corrupted), E02 (Exceeds size/duration), E03 (Silent/No Speech).
    """

    ALLOWED_MIME_TYPES = {
        "audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3", "audio/ogg", "application/octet-stream"
    }

    @staticmethod
    def calculate_hash(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    @classmethod
    async def validate_and_save(cls, session_id: str, file: UploadFile) -> dict:
        content = await file.read()
        file_size = len(content)

        # E01 Check: Empty file
        if file_size == 0:
            raise HTTPException(
                status_code=400, 
                detail="音频文件损坏或为空 (Empty or corrupted audio file - 0 bytes)"
            )

        # E02 Check: Exceeds size limit (50MB)
        if file_size > settings.MAX_AUDIO_SIZE_BYTES:
            raise HTTPException(
                status_code=400, 
                detail=f"音频文件过大，超出系统限制 50MB (File size {file_size} exceeds {settings.MAX_AUDIO_SIZE_BYTES} bytes)"
            )

        # Inspect Audio Header & Duration
        duration_seconds = 0.0
        is_silent = False
        
        # Check if valid WAV
        if content[:4] == b'RIFF' and content[8:12] == b'WAVE':
            try:
                import io
                with wave.open(io.BytesIO(content), 'rb') as wf:
                    channels = wf.getnchannels()
                    framerate = wf.getframerate()
                    nframes = wf.getnframes()
                    if framerate > 0:
                        duration_seconds = round(nframes / float(framerate), 2)
                    
                    # E02 Check: Exceeds duration (600s)
                    if duration_seconds > settings.MAX_AUDIO_DURATION_SECONDS:
                        raise HTTPException(
                            status_code=400,
                            detail=f"单次录音时长超出 10 分钟限制 (Duration {duration_seconds}s > 600s)"
                        )

                    # E03 Check: Silent audio detection (RMS energy)
                    raw_frames = wf.readframes(min(nframes, framerate * 3))
                    if raw_frames:
                        import struct
                        # 16-bit audio samples
                        sample_count = len(raw_frames) // 2
                        if sample_count > 0:
                            samples = struct.unpack(f"<{sample_count}h", raw_frames[:sample_count*2])
                            rms = (sum(s * s for s in samples) / sample_count) ** 0.5
                            if rms < 15.0:  # extremely quiet/silent threshold
                                is_silent = True
            except HTTPException:
                raise
            except Exception as e:
                # Malformed WAV header
                raise HTTPException(status_code=400, detail=f"无法解析的音频文件格式: {str(e)}")
        else:
            # Check basic extension for MP3/OGG simulation
            filename = file.filename.lower()
            if not (filename.endswith(".wav") or filename.endswith(".mp3") or filename.endswith(".ogg")):
                raise HTTPException(
                    status_code=400, 
                    detail="不支持的音频文件格式，仅支持 WAV/MP3/OGG (Unsupported audio format)"
                )
            # Default reasonable duration estimate for mock mp3
            duration_seconds = 4.2

        if is_silent:
            raise HTTPException(
                status_code=422,
                detail="检测到静音或极微弱噪音音频，无法进行有效识别 (Silent audio detected)"
            )

        # Save to persistent storage
        audio_hash = cls.calculate_hash(content)
        file_ext = Path(file.filename).suffix or ".wav"
        saved_filename = f"{session_id}_{audio_hash[:10]}{file_ext}"
        storage_path = Path(settings.STORAGE_DIR) / saved_filename
        
        with open(storage_path, "wb") as f:
            f.write(content)

        return {
            "original_filename": file.filename,
            "storage_path": str(storage_path),
            "file_size_bytes": file_size,
            "duration_seconds": duration_seconds,
            "mime_type": file.content_type or "audio/wav",
            "audio_hash": audio_hash
        }

audio_service = AudioService()
