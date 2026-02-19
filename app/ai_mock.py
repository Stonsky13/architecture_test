from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Mock")


class AgentRequest(BaseModel):
    text: str


@app.post("/agent/handle")
def handle(req: AgentRequest):
    reply = f"Received: {req.text}".strip()
    return {
        "reply_text": reply if reply else "Received empty message",
        "actions": [{"type": "send_message", "status": "success"}],
    }
