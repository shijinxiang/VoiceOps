import time
import httpx
from typing import Dict, Any, Optional
from backend.app.config import settings

class N8nService:
    """
    n8n Workflow Integration & Notification Service.
    Supports asynchronous webhook dispatch, retry mechanism, and mock callbacks.
    """

    async def trigger_notification(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatches work order notification to n8n webhook.
        """
        webhook_url = settings.N8N_WEBHOOK_URL
        max_retries = 3
        backoff_sec = 0.5

        if settings.MOCK_NOTIFICATION_WEBHOOK:
            # High-fidelity mock dispatch for standalone demonstration
            return {
                "status": "callback_succeeded",
                "webhook_url": webhook_url,
                "dispatch_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "channel": "email_and_feishu",
                "message": f"Successfully notified customer and inventory center for ticket {payload.get('ticket_number')}"
            }

        async with httpx.AsyncClient(timeout=5.0) as client:
            for attempt in range(1, max_retries + 1):
                try:
                    resp = await client.post(webhook_url, json=payload)
                    if resp.status_code == 200:
                        return {
                            "status": "callback_succeeded",
                            "webhook_url": webhook_url,
                            "response": resp.json() if resp.headers.get("content-type") == "application/json" else resp.text
                        }
                    else:
                        if attempt == max_retries:
                            return {
                                "status": "failed",
                                "last_error": f"n8n returned HTTP {resp.status_code}",
                                "retry_count": attempt
                            }
                except Exception as e:
                    if attempt == max_retries:
                        return {
                            "status": "failed",
                            "last_error": str(e),
                            "retry_count": attempt
                        }
                    time.sleep(backoff_sec * attempt)

n8n_service = N8nService()
