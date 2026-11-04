# AC215 · Lecture 10 — Connecting to the cloud: one key, three containers, one browser

A follow-along walkthrough of the Lecture 10 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, *Connecting to the Cloud: Networking, Authentication & Storage*:
[dlops-io/cheese-app-v0](https://github.com/dlops-io/cheese-app-v0), branch `main` @
[`cb6fb94`](https://github.com/dlops-io/cheese-app-v0/tree/cb6fb94576aa37bb0b94a8745e5e94e6a504f4bb)
(2026-10-08), its `README.md` top to bottom: *Prerequisites* (the GCP service account and the
Docker network), *Build the Vector DB*, *Run API Service Container*, *Run Frontend Container*, the
five app pages (*Text Chunking*, *Vector DB UI*, *Chat*, *Cheese Expert Agent*, the fine-tuned
cheese model) and the API endpoints. A cheese chatbot built from three containers (ChromaDB with its
loader, a FastAPI server, a Next.js frontend) that calls Vertex AI with a service-account key: who
checks that it is really you, and how does a web page find a database inside a container? The
*Optional: LLM RAG Tutorial* is lecture 5 material and is not followed here.

Panels also quote, for context only and never run: the standalone `dlops-io/llm-rag` (`e17a39f`),
`dlops-io/llm-finetuning` (`44ef6f0`), `dlops-io/mega-pipeline` (`c6bbc9b`), `dlops-io/port_toy`
(`d190c71`), and next lecture's `dlops-io/data-labeling` (`03c3e27`) and `dlops-io/data-versioning`
(`b240b1a`).

Watch it with the README open, your own clone of cheese-app-v0, Docker Desktop running, and a
Google Cloud project with billing. **This lecture bills**: the embedding build and every chat and
agent question make real Vertex AI calls against your project; a GOLD tag marks each one, and the
video ends with the teardown (containers, network, and stale service-account keys). The tracker top
left shows the README stage; pause at every `▶ your turn` to run the command; a gray `extra` tag
marks a check that isn't in the README, and a gray "Lecture 10 · slides …" tag top right points to
the lecture slides the scene stands on.

The terminal sessions were recorded on 2026-10-19/20 in a fresh Docker Engine 29.8.2 standing in
for a laptop with Docker Desktop. That machine had **no Google credentials**, so every step that
needs a real key is shown up to its honest, documented failure
(`DefaultCredentialsError: File /secrets/llm-service-account.json was not found.`), and the success
you should see is tagged `recorded` with its source; no chat, agent or tuned-model answer text is
shown, because nothing documents it. The GCP console and the browser pages are schematic drawings
tagged `illustration`. The project ID on screen is the stand-in `your-gcp-project`. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command, and the
answers to the five test-yourself questions (§8, Q1–Q5):
[MLOps_Learning · guides/L10-cloud-connect-cheese-app-v0.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L10-cloud-connect-cheese-app-v0.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l10-cloud-connect.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, 30:50 (1850.6 s). Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l10-cloud-connect.mp4` | the same video without burned-in subtitles (1920×1080 at 60 fps, h264/AAC 48 kHz stereo, −16.1 LUFS integrated); load any `.srt` below in your player. Not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l10-cloud-connect_part1.mp4` | part 1, 17:46 (1066.8 s): service accounts, ADC and IAM, from a JSON key to a bearer token (S01–S09). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l10-cloud-connect_part2.mp4` | part 2, 13:03 (784.0 s): ports, Docker DNS, CORS, and what survives (S10–S15). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l10-cloud-connect.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l10-cloud-connect.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l10-cloud-connect.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `digest.md` | the tutorial digest: the repo, every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the slide deck in our own words, with slide numbers, and which chapter stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (2026-10-19/20, a fresh Docker Engine 29.8.2 standing in for the laptop with Docker Desktop, no Google credentials); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commits |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |
| `REVIEW.md` | the review record: content gates, QA findings and fixes, the final-cut checks |

Git keeps the subtitles, the chapter files and the transcript; the MP4s are release assets.

## Chapters

Paste-ready in `output/chapters.txt` (and `chapters_part1.txt`, `chapters_part2.txt` for the parts). Part 1 (17:46) is chapters 00:00–15:25 below; part 2 (13:03) restarts at 00:00 with "A name is not localhost", its chapters at 00:00, 02:06, 04:36, 07:24, 09:12, 11:10.

```
00:00 Three phone calls, one question
01:26 One laptop, three containers, one cloud
03:05 An identity for code
04:59 Two filesystems, one folder
07:09 A network, a compose file, a running Chroma
08:56 Chunks for free, embeddings need a key
11:15 ADC: from key file to bearer token
13:19 IAM: may this identity do this, here?
15:25 Run the API, and survive line 14
17:46 A name is not localhost
19:52 One server, two addresses
22:22 The browser is the integrator
25:10 The agent, and a model that isn't yours
26:59 What survives: volumes now, buckets next
28:57 Tear down, recap, and what's next
```

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: what `/secrets`
holds when the key is saved inside the repo, which part of a request decides whose IAM is checked,
what the API would need to reach the database by name, which of the browser's three calls fails
when the frontend moves to port 3300 (and whether `curl` cares), and whether `docker compose down`
deletes your embeddings. Five test-yourself questions close the video (answers in the study guide,
§8 Q1–Q5).

**Part 1 · service accounts, ADC and IAM: from a JSON key to a bearer token**

1. **Three phone calls, one question** — one chat answer is three calls from your browser; three
   riddles (`-p 3200:3000`, `localhost:9000`, `llm-rag-chromadb`); what you need, and what bills.
2. **One laptop, three containers, one cloud** — the map that stays all lecture; clone the repo
   (the README gives no address) and check the commit.
3. **An identity for code** — a service account versus an API key or OAuth; create
   `llm-service-account`, grant its two roles, download a JSON key, and treat it like a password.
4. **Two filesystems, one folder** — `../../secrets` climbs out of the repo; the `-v` mount to
   `/secrets` and the variable that points there; the `.gitignore` gap and Docker's silent empty
   folder.
5. **A network, a compose file, a running Chroma** — the idempotent inspect-or-create network
   command, your project ID in the script, `sh docker-shell.sh`, and an honest note on this
   recording's missing key.
6. **Chunks for free, embeddings need a key** — chunking runs (11 books; 8,248 and 14,228 chunks at
   the time of recording); the embed step dies at authentication without a key; a 403 for a
   disabled API; the book-title slip.
7. **ADC: from key file to bearer token** — ADC's three places in order; the signed JWT, Google's
   token desk and a one-hour bearer token; ADC caught failing on an empty `/secrets`.
8. **IAM: may this identity do this, here?** — the (identity, role, resource) grid; a 401 versus a
   403 and the three causes of a 403; enabling the Vertex AI API.
9. **Run the API, and survive line 14** — `api-service/docker-shell.sh` dies on an existing network;
   fix line 14; `uvicorn_server`, a 500 with an empty `/secrets`, and the recorded 200 of 256
   numbers.

**Part 2 · ports, Docker DNS, CORS, and what survives**

10. **A name is not localhost** — each container has its own localhost; Docker DNS on a shared
    network; the API cannot find the database by name until `docker network connect`.
11. **One server, two addresses** — the frontend's `npm install` and `npm run dev`; `-p 3200:3000`
    as a tunnel; the three bands of port numbers; `0.0.0.0` twice, and doors that face your Wi-Fi.
12. **The browser is the integrator** — the five pages; one chat question as three cross-origin
    calls; origins, preflights and Chroma's guest list; CORS is enforced by the browser and ignored
    by `curl`; an unprotected AI endpoint on your laptop.
13. **The agent, and a model that isn't yours** — the agent's tool pick and loop; the fine-tuned
    endpoint that points into someone else's project, so expect a 403 or a not-found error.
14. **What survives: volumes now, buckets next** — stop the containers, `docker compose down`, and
    find the database file still on disk; storage buckets as the cloud version, and four rules.
15. **Tear down, recap, and what's next** — remove the network, delete stale keys; the whole
    lecture on one map; find the layer of an error; five questions; next, lecture 11.

## Rebuild

```bash
python -m explainer.build videos/ac215-l10-cloud-connect -q l                          # fast draft
python -m explainer.build videos/ac215-l10-cloud-connect --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l10-cloud-connect --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l10-cloud-connect --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l10-cloud-connect --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes
once, then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy
from the scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the cheese-app-v0 tutorial is
used for study with the instructor's permission, and the context repos are quoted at their pinned
commits. The lecture's slides are redrawn in our own pictures, never shown. The GCP console and the
browser pages are schematic drawings (tagged `illustration`), not screenshots; the recording used
no Google credentials, and the key in the folder listings is an obviously invalid stand-in.*
