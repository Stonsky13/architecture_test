from __future__ import annotations

import json
import logging
import os
import httpx
from celery import shared_task

AI_URL = os.getenv("AI_URL", "http://localhost:8001/agent/handle")
logger = logging.getLogger("worker")
logging.basicConfig(level=logging.INFO)


def extract_text(payload: dict) -> str:
    msg = payload.get("message") or {}
    return str(msg.get("text") or "")


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def process_webhook(self, payload: dict) -> dict:
    logger.info("Received webhook payload: %s", json.dumps(payload, ensure_ascii=False))
    text = extract_text(payload)
    req = {"text": text}

    try:
        with httpx.Client(timeout=10) as client:
            r = client.post(AI_URL, json=req)
            r.raise_for_status()
            result = r.json()
    except (httpx.HTTPError, TimeoutError) as e:
        logger.exception("AI call failed, retrying: %s", e)
        raise self.retry(exc=e)

    logger.info("AI result: %s", json.dumps(result, ensure_ascii=False))
    return result
