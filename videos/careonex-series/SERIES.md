# CareOneX, layer by layer — an explainer series

**Status: draft plan, written before Marco's branch was pushed.** Episodes E1–E4 cover what is on
GitHub today (`nadirbt/careonex-agents`: `main`, `data-retrieval`, `feat/sonic_with_rag`,
`feat/prompt-tuning`). Marco's work (model-free update, adaptive v3 retrieval, the "latest
experiment" folders, text-to-text evaluation, the `feedback` search mode) gets its own episodes
once his branch is up, and E1/E3/E5 are revised against it.

## Who it is for, and how we know things

**Audience: a complete beginner who badly wants to understand the whole system.** No AWS, Docker,
search or speech background is assumed. Every term is explained the first time it appears, with a
picture, and the series opens with E0, which decodes the two commands Marco uses to start the app,
line by line.

**We have no access to the team's AWS account.** Everything about the live system is learned from
the code on GitHub, the team's notes (`TEAM_SETUP.md`, `NOTES-2026-10-07.md`, the Milestone 1
statement) and our own offline reruns. Every claim on screen carries a small tag saying where it
comes from:

| Tag | Meaning |
| --- | --- |
| `READ IN CODE` | we read it in the repository, at the commit named in the episode README |
| `TEAM NOTES` | the team wrote it down (setup guide, session notes, statement of work); we did not check it live |
| `MEASURED` | we ran it ourselves (offline, without AWS): see `checks/` |
| `INFERRED` | our best guess, shown with the reason; it may be wrong, and the video says what would settle it |

## Why a series, not one video

The project is built as layers that run in separate containers, and five people each work on one
or two of them with their own AI agent. One long video would mix layers that nobody needs at the
same time. Each episode here covers **one layer**: what goes in, what comes out, the decisions
inside it and why they were made, and what is still open. Watch E1 first; after that the episodes
can be watched in any order. A beginner should watch E0 first.

## Format

- 3Blue1Brown style (Manim), the house toolkit in `explainer/`.
- **No narration.** English on screen, bilingual subtitles burned in under the picture (Chinese on
  top, English below). The narration text in each `script.md` is only used for the subtitles. Its
  timing comes from a reading pace (`voice: {backend: silent, speed: …}`) instead of a voice.
- 5–9 minutes per episode. Each ends with "what is still open" and 2–3 questions to test yourself.
- Every claim is checked against the code at a named commit. The commit is printed in each
  episode's README so the video can be re-checked when the code moves.

## Fixed visual language (all episodes)

| Thing | Colour | Shape |
| --- | --- | --- |
| Our own code, one container per service | BLUE | rounded box, small "CONTAINER" tag |
| Stored data: S3 prefixes, files, chunks, passages | GREEN | box with a folded corner / prefix label `raw/`, `text/` … |
| AWS managed pieces: Bedrock models, Knowledge Base, S3 Vectors | ORANGE | box with a "BEDROCK" / "AWS" tag |
| A person: the family caller, a teammate | WHITE | person glyph |
| The caller's question, a search query | YELLOW | speech bubble / query strip |
| Failure modes, bugs, things that went wrong | RED | strike / warning tag |
| Branches by person (E1, E5+) | Nadir GOLD · Caroline PINK · Junyi PURPLE · Marco TEAL · Helen GREY | branch lines on a timeline |

## Episodes

| # | Title | Layer / containers | Source on GitHub | Status |
| --- | --- | --- | --- | --- |
| E0 | **Decoding the start-up commands**: every word, for a beginner | the laptop, AWS login, Docker, the two programs | Marco's commands + all branches | script written |
| E1 | **The big picture**: a family, a phone call, and seven containers | all; the team's branches | all branches + Milestone 1 SOW | plan; branch map waits for Marco |
| E2 | **Building the library**: from 20 public documents to 232 vectors | `data` → `ingest` → `extract` → `chunk` → `kb-sync` | `data-retrieval` | plan |
| E3 | **Finding the right passage**: embeddings, cosine similarity, filters | `retrieve` (+ Bedrock KB, S3 Vectors) | `data-retrieval`; Marco's retrieval updates | plan; revise with Marco |
| E4 | **The voice loop**: Nova 2 Sonic, barge-in and tools | `voice` | `data-retrieval`, `feat/sonic_with_rag` | plan |
| E5 | **Keeping it honest**: grounding rules, the intake, and measuring answers | prompt, tools, evaluation | `feat/sonic_with_rag`, `feat/prompt-tuning`, Marco's evaluation | plan; needs Marco |
| E6+ | **Marco's experiments** | to be decided from his branch | Marco's branch | waiting |
| E7 | **Where we are and what next** | all | all + SOW targets | plan |

### E1 · The big picture (~6 min)

1. The problem (SOW): a family fills the careonex.com form; someone must call back, explain how home
   care is paid for, and take an intake. Evening and weekend requests wait; some never get a call.
2. What the agent must do on a call: answer questions **from cited documents** (never from memory),
   take the intake one question at a time, never give medical or legal advice.
3. Two halves: **build the library** (offline, a batch pipeline) and **answer a caller** (live).
   The diagram from the team, animated piece by piece: catalog → data → ingest → extract → chunk →
   kb-sync → Knowledge Base; caller ↔ voice ↔ Nova 2 Sonic; tools → retrieve → Knowledge Base.
4. Why containers: one job each, one owner each, one prefix each; `docker compose` wires them; the
   only shared contracts are the S3 prefixes and the retrieve HTTP API.
5. Who built what: the branch map (main · data-retrieval · sonic_with_rag · prompt-tuning · Marco's
   branch), and what each branch changes relative to the one it came from.
6. Where we are vs. the Milestone 1 targets (sub-second turns, grounded answers ≥ 95 %, intake field
   accuracy ≥ 90 %): what exists, what is measured, what is not yet.

### E2 · Building the library (~8 min)

1. The catalog `ragfile_list.csv`: 20 approved public sources (NJ DMAHS, DoAS, DDS, Medicare, VA,
   one team-curated summary). Each row: program, URL, effective date, sha256.
2. `data` + `ingest`: one versioned bucket `ac215-program-kb-<account>`; each source → `raw/` +
   `.metadata.json` sidecar; skip when the sha256 is unchanged; every run writes a snapshot manifest.
   Why `ac215-` and never `careonex-` (the IAM policy is scoped by prefix).
3. `extract`: why a text form at all (raw HTML bytes change on every request; the text hash is the
   real "did the rules change?" signal); HTML main-region-first (v1 trafilatura dropped eligibility
   paragraphs; v2 stripped nav first and emptied nj.gov); PDFs via pymupdf4llm keep tables.
4. `chunk`: headings start sections, the heading path travels with every chunk ("Income limit:
   $4,855" never without "JACC"); tables never split; target 1600 / cap 2800 / merge under 200
   characters; one S3 object per chunk; the silent 1 KB sidecar limit.
5. `kb-sync`: Titan Text Embeddings v2 turns each chunk into 1024 numbers; S3 Vectors index
   (cosine); Bedrock Knowledge Base with chunking `NONE`; ingestion job. Why S3 Vectors (cents per
   month vs. ~$175 for OpenSearch Serverless) and the latency it costs.
6. Open: DoAS side-by-side table loses its column names in extraction; re-crawl schedule.

### E3 · Finding the right passage (~7 min)

1. A question becomes a vector; nearby vectors are similar meanings; cosine similarity as an angle.
2. top-k, and why it asks for 2× candidates (min 10).
3. Metadata filters: S3 Vectors only supports exact `equals`, so "Medicaid" is mapped to catalog
   labels; unknown names → no filter rather than an empty answer.
4. The latest-year policy: `figure_year` (latest year named in the text, else effective date) and
   withholding older-year figures for the same program.
5. The API contract the voice agent sees: passages with title, program, effective date, heading path.
6. Marco's retrieval changes (adaptive v3 etc.): revised once his branch is read.

### E4 · The voice loop (~8 min)

1. Speech in, speech out: Nova 2 Sonic over one bidirectional stream (16 kHz in, 24 kHz out); the
   event sequence (sessionStart, promptStart with tools, system prompt, audio chunks …).
2. Barge-in: the server stops, the client drains its playback queue.
3. The echo gate for laptop speakers: expected echo = k × what is playing; k tracked as a decaying
   peak (an average drifted to 0.03 and the assistant heard itself); ratio 1.8; hold open at onsets.
4. A tool call round trip: toolUse → `handle_tool` → contentStart / toolResult / contentEnd, keyed
   by toolUseId (Caroline's fix for overlapping calls).
5. `lookup_program_info`: caller facts folded into the query, a second age-specific lookup, dedupe,
   speakable passages (tables → one sentence per row), newest first, guidance text.
6. Intake as a state machine owned by the client (`intake_next_question` → one question) and
   `save_intake` (callback exists only after it succeeds).

### E5 · Keeping it honest (~7 min, revised with Marco)

Grounding rules in the system prompt and the tool guidance; `--expect-tool` smoke test (before it,
the test passed with zero tool calls); the intake schema with a confidence per field (Junyi's
`feat/prompt-tuning`); Marco's text-to-text evaluation with cosine similarity, and what cosine
similarity can and cannot tell you about an answer.

### E7 · Where we are and what next (~5 min)

The Milestone 1 stages 0–6 vs. what exists; the open items each branch lists; the integration
problem itself (branches that diverge: `make` vs `just`, two copies of the voice prompt); a
proposed order of work.

## Production

```
videos/careonex-series/        this plan, the shared visual kit (careonex_kit.py), the glossary
videos/careonex-e1-big-picture/ …  one video project per episode (video.yaml, script.md, scenes/, i18n/zh/)
```

Build one episode (subtitle-only, bilingual subtitles burned in):

```bash
python -m explainer.build videos/careonex-e2-library --burn      # → output/careonex-e2-library.zh-en.mp4
```
