# Design: Voice Realtime Assistants

**Project:** `voice-realtime-assistants`  
**Parent system design:** [02 — Streaming Token Delivery](../02-streaming-token-delivery.md)

## 1. What this POC demonstrates

Simulates duplex voice turn with barge-in and audio frame metadata (WS semantics over HTTP POC).

## 2. Architecture (POC)

```text
POST /turn → optional barge_in interrupt → caption + fake audio frames
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Barge-in state | User interrupt must stop TTS immediately. | `barge_in` short-circuit. |
| Caption + audio frames | Voice UIs need both text and timed media. | Frame list with ms/bytes. |
| Protocol note | Production uses WebSocket/WebRTC, not SSE. | `protocol=websocket-simulated`. |

## 4. Key endpoints

`GET /health`, `POST /turn`

## 5. Tradeoffs / POC limits

No real audio codec path — frames are metadata only.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

> **Watch on YouTube:** [Voice Realtime Assistants — System Design #Shorts](https://youtu.be/a9h2PFHSUrs)
>
> Direct link: **https://youtu.be/a9h2PFHSUrs**

Also available in-repo:
- GIF preview: [`video/design-overview.gif`](./video/design-overview.gif)
- MP4 download: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Narration script: [`video/narration.txt`](./video/narration.txt)

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

