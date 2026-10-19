# AC215 · Lecture 6 — LLM: Agents I: function calling by hand, ADK, MCP, many agents, the harness

A follow-along walkthrough of the Lecture 6 tutorials of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**:

- [dlops-io/llm-rag](https://github.com/dlops-io/llm-rag), branch `main` @
  [`e17a39f`](https://github.com/dlops-io/llm-rag/tree/e17a39f35bc07b440f573def480adaf4703f8b91), section
  *Agents*, with the three lecture 5 steps it stands on: *Prerequisites*, *Run LLM RAG Container* and
  *Load Embeddings into Vector Database*;
- [dlops-io/llm-agent-google-adk](https://github.com/dlops-io/llm-agent-google-adk), branch `main` @
  [`f89faa7`](https://github.com/dlops-io/llm-agent-google-adk/tree/f89faa79de744f6a046e30dff24b3b6f1d73720b),
  the whole README (*Getting Started*, *Running Agents*), with modules `1-baseline` and `3-mcp-tools`
  run and code from modules 4 and 5;
- three Colab notebooks: [Cheese Quiz](https://colab.research.google.com/drive/14UKW-Z7kFPuCwVqyUFcLxeA1KF70fwfm?usp=sharing),
  [Travel Planner](https://colab.research.google.com/drive/1I_jJEHJsVkGxNoSC1c4wEoVF2QL6vCVY?usp=sharing)
  and [Cheese Newsletter · Harness](https://colab.research.google.com/drive/1nnHrJ4Si3tpgUQl6HqlcwxKymV1-ecPv?usp=sharing)
  (notebooks have no commit: the copies the video quotes, downloaded on October 17, 2026, are in
  `assets/source/colab/`).

An agent is a model, given instructions and tools, that runs on its own until the task is done. The
video climbs toward that in three steps. By hand: llm-rag's `--agent` gives Gemini 3.1 Flash-Lite a menu
of two hand-written function declarations and forces it to pick one; your Python runs the search against
lecture 5's Chroma collection, and a second call writes the answer. With a framework: Google's Agent
Development Kit (ADK) runs the loop, keeps a session's state, and plugs in tools over MCP. With a
harness: two notebooks where Python, not the model, decides what counts as approved and what counts as
done. Two other commits of llm-rag are quoted for comparison, not followed:
[`68e0bde`](https://github.com/dlops-io/llm-rag/tree/68e0bdecba017b506c7646d710b1fbf1bc6b31fc) (the staff's
committed embeddings, which the video loads for real) and
[`96d5fd7`](https://github.com/dlops-io/llm-rag/tree/96d5fd78d24607e20ae84d5339ed62abaadff17d) (the
instructor's book before commit `85bba32` rewrote it; the staff's recorded run quotes this old text).

Watch it with three things open: your `~/AC215/llm-rag` clone with lecture 5's collection on disk (or
the time to load it again), a fresh clone of `llm-agent-google-adk`, and a Colab copy of the Cheese
Quiz. You need Docker with Compose, uv and Node.js, and three keys: lecture 5's service-account key, a
Google AI Studio key, and an OpenAI key with billing on. The tracker top left shows the README (or
notebook) step; pause at every `▶ your turn` to run the command; a gray `extra` tag marks a check that
isn't in the README, and a gray "Lecture 6 · slides …" tag top right points to the lecture slides the
scene stands on. The video was recorded on October 18, 2026 **without keys**: Docker, Chroma, uv, the
ADK web server and two MCP servers ran for real (Docker Engine 29.8.2, Compose v5.6.0, uv 0.13.1, ADK
2.12.0, Node.js 24); every model call stopped before sending, or was refused; model answers are the
teaching staff's saved outputs, tagged `recorded`. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L06-agents-1.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L06-agents-1.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l06-agents-1.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l06-agents-1.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l06-agents-1_part1.mp4` | part 1, DURATION_P1: what an agent is, and function calling by hand with llm-rag (S01–S08). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l06-agents-1_part2.mp4` | part 2, DURATION_P2: frameworks own the loop — ADK, MCP, many agents and the harness (S09–S16). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l06-agents-1.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l06-agents-1.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l06-agents-1.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, eleven hands-on predict-then-run tasks (steer the tool choice, let the model skip retrieval, turn the two calls into a capped loop, watch the whiteboard, fix the router two ways, module 4 as a web API, module 2 with LiteLLM, the MCP filter, approving your own travel plan, the newsletter's URL rule as a check, sessions out of git), eight debugging and six think questions, with answers |
| `assets/exercise-checks/` | what was run to check `exercises.md`, in throwaway containers with the tutorials' own lockfile, versions and notebook cells, with every log; stand-ins for the model where a reply was needed |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the instructor's slides in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from: the llm-rag laptop and its container (a fresh Docker Engine 29.8.2, the staff's committed vectors loaded for real), a Debian 12 laptop with no Python for the ADK repo, the Cheese Quiz's remote MCP server, all on October 18, 2026, without keys; and in `expected/` the staff's recorded `out.txt` and the notebooks' saved outputs. Provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commits (llm-rag, the old book at `96d5fd7`, the ADK repo), and the notebooks' cells |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s are release assets.

## Chapters

CHAPTERS

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: nine author names in the
menu against eleven books, and which books the agent can never reach by author; what `cli.py` does if
call 2 answers with another function call; which Python `uv sync` uses on a laptop with no Python at
all; which handler runs when the classifier answers "Simple" with a capital S; and why the travel
planner's model can't approve its own plan. Five test-yourself questions close the video (answers in
`exercises.md`).

**Part 1 · what an agent is, and function calling by hand (llm-rag)**

1. **Who searched your database?** — the staff's recorded run, where a function and its arguments print
   before the answer: ten passages from one book, filtered by author, although Gemini runs in Google's
   data center, where localhost means nothing; the lecture's Paris trip (plan five days, replan when it
   rains): a model drafts, RAG fetches, neither acts — live systems, tools that act, autonomy; the three
   steps of the video (by hand, with a framework, with a harness); what you need, and what a recording
   without keys shows.
2. **Who holds the steering wheel?** — the Cheese Quiz: a copy in Drive, the OpenAI key in Colab's
   Secrets, an install cell that is unpinned and hides its errors; one question three ways with the same
   GPT-4o: one call in under 3 seconds; a reasoning workflow whose Python orders 11 calls (39 seconds, a
   token total that is only an estimate); an agent with instructions and OpenAI's hosted web search, two
   searches and a stop on its own after 13 seconds ("Tools used: 1" counts tools configured, not calls);
   the lecture's definition and five blocks, dynamic control as the steering wheel; an agent isn't a
   smarter model.
3. **Everything the model knows is in the envelope** — LLMs are stateless; every call is a fresh
   envelope; seven steps change only the inputs (a system prompt, retrieved documents, earlier turns, a
   profile from past sessions, a tool's output, an output schema) and the top pick changes with them;
   memory is paper you put back in the envelope, every call; the lecture's instructions and memory
   blocks; spot the slip: step 2 swaps the system and user roles; step 6 pastes in a tool's output — but
   how does a model ask for a tool?
4. **A menu of two tools** — lecture 5's straight-line RAG and the lecture's smarter retrieval; agentic
   RAG, a model choosing from a menu; llm-rag's two function declarations, written by hand: a name the
   model writes back, a description that is the only documentation it sees, JSON-schema parameters, an
   enum of 9 authors, both fields required; two more arguments of the real function (the collection, the
   embedding function) that the model never controls; the lecture's three duties of a tool user; nine
   names, eleven books: two books no author search can reach (178 chunks, and 1,505 that lost their
   author to lecture 5's file-name slip), both still reachable by the all-books search; the stage —
   Gemini in Google's cloud, two containers on your laptop — and the trip: call 1 returns an order, your
   code runs it, call 2 sends back the result.
5. **Back in the container: the agent needs an index** — a fresh start (clone, the key in `secrets/`
   beside the repo), `cd llm-rag`, your Project ID in `docker-shell.sh`, `sh docker-shell.sh` (a
   harmless pull message, a 40-second build, Python 3.12.15 and uv 0.13.1); `docker ps` and port 8000;
   step 1 of the Agents section on a fresh clone: the collection does not exist (line 429, before any
   call to Gemini); keep lecture 5's database (rebuilt if you chunked before September 22, 2026) or
   chunk, embed and load again; the staff's committed embeddings standing in for the embed step; the
   load: 11 books, 8,248 chunks, 24 from the instructor's story.
6. **Call 1: the model writes the call** — the user's turn; three settings: temperature 0, the menu as
   tools, and a tool config with mode any, which becomes `ANY`: the model must answer with a function
   call, so it chooses which search, never whether (the lecture's Self-RAG decides whether); the request
   as built, not sent: the question, both declarations with the enum, mode ANY, temperature 0, and no
   system instruction (defined, never sent, as in lecture 5); step 1 with the collection loaded stops at
   the first model call for want of a key; the staff's recorded call: four words of search text where
   the description asked for a sentence or two, an ID and a thought signature; the SDK ran nothing; what
   to look for with your key, and what each failure means.
7. **Call 2: your code ran it, the model answers** — the dispatcher matches the name, runs the real
   function with the model's arguments and wraps the result; the staff's recorded call through the
   tutorial's own dispatcher against this collection (a stored chunk's vector standing in for the
   embedding): 10 passages of today's story, one string of 3,509 characters; call 2 sends the question,
   the model's own turn unchanged with its thought signature, and your function responses, with the
   tools but no tool config; the staff's answer and its tokens (247 and 1,269); who searched your
   database and who chose the book; two model calls and one embedding call per question; a book rewritten
   by the commit that added the recorded output: an index answers from what was loaded; `response.text`;
   the course's hosted Cheese Agent Tool.
8. **From two calls to a loop** — llm-rag's agent runs one lap, the smallest piece of an agent; the
   lecture's hub unrolled into a loop; the stop rule, a reply with no function call; ADK's Runner
   streaming events while the loop runs inside the library; the caps (12 turns in the Cheese Quiz Guild,
   16 iterations in the newsletter, `MaxTurnsExceeded`); dynamic control, the block the lecture grays out
   because a framework writes it; teardown: `exit` leaves Chroma on port 8000, `docker compose down`, the
   index stays on disk.

**Part 2 · frameworks own the loop — ADK, MCP, many agents and the harness**

9. **ADK: clone, configure, and a sync that fails** — no Docker this time; the clone, and a `cd` to a
   folder that doesn't exist; six module folders and no lock file; `cp .env.example .env`, a key from
   Google AI Studio, and a current model in the model line (the lecture's first design decision; the
   code's fallback is shut down, Gemini 2.5 Flash limited to earlier users); only the nearest `.env` is
   loaded; the project file's open-ended versions; with no Python on the laptop uv downloads CPython
   3.15.0, and `onnxruntime` has wheels only up to 3.14; `uv python pin 3.13`; a 1.6 GB environment
   (plus about 3 GB of CUDA packages on a Linux PC); ADK 2.12.0.
10. **adk web and the folder names** — `uv run adk web` from the repository root; the telemetry question
    the README doesn't mention (Enter means yes; `adk telemetry disable`); port 8000 and the dev UI; seven
    entries in the dropdown; agent names must be Python identifiers, so `1-baseline` is refused, and an
    older ADK refuses it too; the fix: rename the folders; the root `.env` and `baseline.agent` in the
    log; the quick start's file argument and the module READMEs' missing `web`; the port clash with
    llm-rag's Chroma (`docker compose down`, or `--port 8080`).
11. **Runner, session, state: the shared whiteboard** — baseline's three LLM agents in the lecture's
    blocks (model, instruction, output key; no tools); a sequential agent; the agent tree the UI loads,
    with the model from your root `.env`; a new session with an empty state; output keys write into the
    state, placeholders read from it, and the agents never call each other; a parallel agent; a pipeline
    without tools guesses its prices; the README's "memory" is session state for one session, not the
    lecture's memory; what the placeholder key does (API key not valid); what to look for with your key,
    and the session file in the agent's folder.
12. **Tools you didn't write: MCP** — the lecture's three families of tools (data, action,
    orchestration); one agent wired to ten services, ten custom integrations; MCP as a shared protocol:
    a host with clients and a server per service; three plugs: the filesystem server over stdio, a child
    process started with `npx`, whose 14 tools `tool_filter` cuts to three; the Cheese Quiz's remote
    server by URL, passed as MCP servers, not tools (a browser's plain request gets 406; initialize, list
    tools, call); the notebook's own FastMCP server in a thread on port 8001; your client process does
    the talking: MCP gives the model no network access.
13. **Many agents: who plans the order?** — the lecture's deep-research tree; three answers: the code
    (a sequential agent, an assembly line); the model (the Guild's orchestrator calling specialists
    turned into tools; "at most 2 review rounds" is a rule in prose, and only a cap of 12 turns is
    enforced; the saved run's three errors, and a quiz anyway); Python reading the model's label (a
    custom agent whose plain `if` statements pick a handler from a classifier's word); an exact
    comparison, and two fixes; handoffs, for lecture 7.
14. **The harness: only a human says yes** — the Travel Planner rehearses the lecture's trip: a pinned
    Agents SDK, a mock catalog that books nothing; the saved run's four turns; the gate: a finalize call
    only proposes, and the code stores the plan as pending; approval lives in a separate function that
    runs on the human's message before the agent; Python builds the budget, 2,690 of 6,000 dollars, and
    the notebook's own test checks it; what the user sees comes from checked state: a hard guardrail
    raises, a soft one warns; the lecture's success criteria and guardrails, kept in code on the action
    tool.
15. **The harness: success is a receipt** — the Cheese Newsletter with Microsoft's Agent Framework,
    pinned; the `USERS` cell (you and a friend; email is preview only); an orchestrator with three tools,
    16 iterations, one tool call at a time; the saved run's four editor calls, because validation errors
    go back as the tool's result; Python ignores the orchestrator's words and checks for a receipt and a
    file on disk; a rule left in the prompt (no embedded URLs) slips: a note is not a check; the
    lecture's Self-RAG and Corrective RAG: don't trust, check.
16. **Tear down, recap, and what's next** — Ctrl+C; `git status`: the renamed folders and your pin,
    `.env`, `.venv` and `uv.lock` ignored, the sessions in `.adk/` not; delete the 1.6 GB environment
    when you're done; disconnect and delete each Colab runtime; three keys, and where each belongs; the
    lecture's anatomy filled with today's code; the lecture's formula plus two pieces: a loop the
    framework runs, and checks your code enforces; five test-yourself questions; next lecture, Agents II:
    the harness.

The tutorials' small mistakes are pointed out kindly, with the fix. In llm-rag: the Agents section
doesn't say it needs lecture 5's collection (load it first); the system instruction is defined but
never sent, as in lecture 5; the README says the command "displays the LLM's response", but line 478
prints the whole response object (print `response.text`); the committed `out.txt` answers from the
instructor's book before the same commit rewrote it (an index is a snapshot: rebuild it when the
books change); and a doubled "a a" in the search text's description. In the ADK repo: `cd google-adk-tutorial` (the folder is
`llm-agent-google-adk`); no lock file, and the README's `uv sync` fails whenever uv picks CPython 3.15,
because `onnxruntime` has no wheel for it (`uv python pin 3.13`); module folder names that aren't Python
identifiers, which today's ADK refuses and a version pin doesn't fix (rename them); retired model
defaults, `gemini-2.0-flash` in the code and `gemini-2.5-flash` in `.env.example` (set `GEMINI_MODEL` to
a current model in the root `.env`, and skip the module READMEs' Setup steps, since only the nearest
`.env` is loaded); ADK 2.12's telemetry question, where Enter means yes (`adk telemetry disable`);
`QUICKSTART.md` passing a file to `adk web`, and the module READMEs' `uv run adk` without `web`; the
README's "memory", which is session state; and sessions saved in each agent's `.adk/` folder, which the
`.gitignore` doesn't cover (add `.adk/`). In the notebooks: the Cheese Quiz installs unpinned packages
and hides the output (rerun without the redirect if imports fail); "Tools used: 1" counts configured
tools and "Total tokens: 701" is an estimate; step 2 of *Managing LLM Inputs* swaps the system and user
roles (swap them back before comparing); the FastMCP cell's comment says port 8000 where the code uses
8001; and the Newsletter's "no embedded URLs" rule is never checked by code (exercises B10 makes it a
check).

## Rebuild

```bash
python -m explainer.build videos/ac215-l06-agents-1 -q l                          # fast draft
python -m explainer.build videos/ac215-l06-agents-1 --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l06-agents-1 --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l06-agents-1 --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l06-agents-1 --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes once,
then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy from the
scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); this video is made for study with
the instructor's permission. The lecture's slides are redrawn in our own pictures, never shown. The
Google Cloud console, Google AI Studio, Colab, the ADK dev UI and the course's hosted Cheese Agent Tool
are schematic drawings (tagged `illustration`), not screenshots; no real key was used or shown, and the
instructor's name is hidden on screen.*
