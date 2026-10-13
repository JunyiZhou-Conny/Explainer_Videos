# CareOneX E4 · The voice loop — script draft (v0, not rendered)

**Draft.** Based on `data-retrieval@d96a4ad` + `feat/sonic_with_rag@eff4a96` (services/voice), now
checked against Marco's `feat/sonic_with_rag_updated@1591ed2`. Changes there that E4 must show:
`CAREONEX_VOICE_SEARCH_MODE` (default `feedback`, `baseline` rolls back; E6 explains the search);
one retrieval per lookup (the age-specific second query is gone); blank or malformed results are
never presented as evidence; the callback number is saved only after a digit readback and an
explicit "yes" (`nova_sonic/intake_confirmation.py`).

## S01 · One stream, both directions — `NovaSonic`

SHOW: Caller → mic chunks (16 kHz, 512 frames ≈ 32 ms) → `audioInput` events → Nova 2 Sonic
(`amazon.nova-2-sonic-v1:0`, Bedrock `InvokeModelWithBidirectionalStream`) → `audioOutput` (24 kHz) →
speaker. Both directions at once on one open stream.
SAY: The voice container keeps one stream open to Nova 2 Sonic for the whole call. Microphone audio goes up in small chunks, about 32 milliseconds each. Spoken reply audio comes back down on the same stream, at the same time.

SHOW: The opening sequence as cards: sessionStart (endpointing sensitivity) → promptStart (voice
"matthew", the three tools) → system prompt (SYSTEM text) → audio contentStart → audio chunks …
SAY: Before the caller says anything, the client sends a short script of events: start the session, declare the voice and the three tools, and send the system prompt, the long list of rules the model must follow.

## S02 · Barge-in — `BargeIn`

SHOW: Nova is speaking (queue of audio chunks); the caller starts talking; Nova stops on the server
and sends `{ "interrupted" : true }`; the client drains its queue.
SAY: Callers interrupt. Nova notices on the server and stops generating, but audio it already sent is still queued on the laptop. So the client empties its playback queue the moment it sees the interrupted signal.

## S03 · The echo gate — `EchoGate`

SHOW: Laptop speakers: the reply leaks into the mic and looks like the caller speaking. The gate:
expected echo = k × loudest output in the last 0.3 s; forward mic audio only if louder than 1.8 ×
that (and above RMS 250); once open, hold for 10 chunks. k learned as a slowly decaying peak (an
average drifted down to 0.03 and the assistant heard itself again).
SAY: (to write)

## S04 · A tool call, round trip — `ToolCall`

SHOW: Nova emits `toolUse` (name, toolUseId, JSON input) → `handle_tool` runs in the background →
three events back: contentStart (TOOL) → toolResult → contentEnd; records keyed by toolUseId
(Caroline's fix: overlapping calls once stored results on the wrong call).
SAY: (to write)

## S05 · lookup_program_info — `Lookup`

SHOW: The input (query, program, county, age, situation) → county validation (21 NJ counties; "New
Jersey" dropped) → query enriched with caller facts → POST /retrieve top_k 5 with `search_mode`
(`feedback` by default on Marco's branch) → dedupe → speakable passages (Markdown removed; tables →
one sentence per row) → newest first → guidance text appended. Before/after strip: on
`feat/sonic_with_rag` an age also triggered a second, age-specific query (top_k 3); Marco's branch
removed it ("every age-bearing lookup silently doubled the number of Bedrock queries").
SAY: (to write)

## S06 · The intake as a state machine — `Intake`

SHOW: intake_next_question: the model reports what it knows; the client returns the ONE next
question in a fixed order (relationship → age → county → help → hours → timeline → payer → name →
phone); save_intake writes JSON; a callback exists only after it succeeds.
SAY: (to write)

## S07 · What is open — `OpenVoice`

SHOW: Caroline's open items (2026-10-07 notes): length and format still model-dependent; "**" in
transcripts; county not validated in intake tools; README credentials section out of date. Plus:
the persona harness from the SOW does not exist yet; no telephony yet (laptop mic only).
SAY: (to write)
