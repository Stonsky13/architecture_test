from __future__ import annotations
import os
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from app.tasks import process_webhook

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
app = FastAPI(title="Webhook PoC")


@app.post("/webhook/telegram")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid secret")
    payload = await request.json()
    task = process_webhook.delay(payload)
    return JSONResponse({"ok": True, "task_id": task.id}, status_code=200)
