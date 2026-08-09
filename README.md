# Use Case: Voice / Realtime Assistants

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [02 — Streaming Token Delivery](../02-streaming-token-delivery.md)

## Users & problem

Users speak and hear responses with low delay. Token/text streaming alone is not enough—audio frames, barge-in, and duplex control need a bidirectional channel.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| End-to-end reply start | Hundreds of ms class (product-defined) |
| Barge-in | User interrupt stops TTS immediately |
| Protocol | WebSocket (or WebRTC) preferred over SSE |
| Jitter | Smooth audio; conceal gaps |

## Design (from parent)

```
Client mic → ASR → Agent orchestrator → LLM stream
  → TTS → audio frames on same WS
  → Barge-in cancels generation + flushes audio
```

Reuse `generation_id` lifecycle and cancel semantics from **02**; change transport to **WebSocket/WebRTC**.

## Specializations

| Concern | Voice choice |
|---------|--------------|
| Events | audio chunks + text captions + tool events |
| Backpressure | Drop/conceal audio; never stall capture path |
| Inference | Streaming LLM with low ITL; maybe speculative |
| Safety | Classifier on text + optional audio policy |

## Failure modes

- Half-duplex lock → explicit barge-in state machine.
- WS reconnect mid-utterance → resume policy or restart turn cleanly.
- Runaway speech → max utterance wall clock + cost cap.




## Design walkthrough (opens on GitHub)

![Design overview](docs/video/design-overview.gif)

Full narrated video (download): [docs/video/design-overview.mp4](docs/video/design-overview.mp4)

## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd voice-realtime-assistants
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/turn -H 'Content-Type: application/json' -d '{"transcript":"what is the weather"}' | jq
