# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Voice Realtime Assistants — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Voice Realtime Assistants"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(USE_CASE)


class TurnIn(BaseModel):
    transcript: str
    barge_in: bool = False

@app.post("/turn")
async def turn(body: TurnIn):
    if body.barge_in:
        return {"status": "interrupted", "audio_frames": []}
    text = await llm.complete(body.transcript, max_tokens=16)
    # Fake PCM-ish frame metadata
    frames = [{"seq": i, "ms": 20, "bytes": 640} for i in range(5)]
    return {"protocol": "websocket-simulated", "caption": text, "audio_frames": frames}
