# Exercise checks · ac215-l06-agents-1 (2026-10-19, 10:18–10:58 UTC)

What was run to verify `exercises.md`, beyond the captures in `assets/terminal/`, which the answers cite
directly (`laptop/NN`, `cli-container/NN`, `adk-laptop/NN`, `mcp-remote/NN`, `expected/…`). Logs and the
check scripts are in [`logs/`](logs/). Every log starts with its command (`$ …`) and ends with `[exit N]`;
the instructor's name is written `<instructor>` in all of them.

There was no Google Cloud project, no AI Studio key and no OpenAI key. Wherever an exercise depends on a
model's reply, the check replaced the model with a **stand-in**: a reply written by hand
(`(stand-in reply …)`, scripted function calls, or labels like `Simple`) that drives the tutorial's own,
unchanged code down one path. Stand-in replies are never model output; the tables say which checks use
one. Model calls that would have left the machine were stopped before sending, or failed for want of a
key or of internet.

## Setup (disposable; nothing from the repos ran on the host)

- Docker Engine 29.8.2 on the session machine (its daemon was started for these checks). Every container,
  image, network and volume was named `l06ex*`; work copies lived inside named volumes, never in this
  folder.
- **llm-rag** (`rag-setup.sh`): the repo's files at `e17a39f` (the pinned commit, `git archive` of the
  read-only clone) plus the staff's 11 `embeddings-char-split-*.jsonl` files from `68e0bde` (as the video's
  `laptop/08` copies them), in the volume `l06ex-rag-work`; a `/.venv` made by `uv sync --frozen` of the
  repo's own `uv.lock` with uv 0.13.1 on `python:3.12-slim-bookworm` (the Dockerfile's base): Python
  3.12.15, 123 packages, chromadb 1.1.0, google-genai 1.39.1 (the capture's versions). The Chroma server
  is the image the captures pulled as `latest`, `chromadb/chroma@sha256:1e0b73a1…` (`chroma 1.4.4`), on a
  private network `l06ex-net` under the alias `llm-rag-chromadb`, so the unchanged `cli.py` finds it by
  name. The collection was loaded with the README's own command (`setup-load-char-split.log`: 11 files,
  `Finished inserting 24 items into collection 'char-split-collection'` for the story, 8,248 in all).
  `rrun.sh` runs a command the way the student types it at the container's prompt: the work copy on
  `/app`, `/.venv` activated, `GCP_PROJECT=your-project-id`, the key path set and `/secrets` empty, no
  internet. Two differences from `sh docker-shell.sh`: the venv sits in a volume instead of the image
  (the image's apt layer was not built), and the commands run as root, not as `app`. `mkcopy.sh` makes a
  patched copy (`b2`, `b3`, `c2`) of the work copy and logs its diff.
- **llm-agent-google-adk** (`adk-laptop.Dockerfile`, `adk-setup.sh`): a check laptop on
  `python:3.12-slim-bookworm` (so it has a system Python 3.12.15, used by C3), with the sandbox proxy's
  CA, git, curl, uv 0.13.1 and Node.js v24.22.0 / npm 11.19.1 (the capture's versions), user `student`.
  In the volume `l06ex-adk-home`: `git clone` at `f89faa7`, the README's `cp .env.example .env` with the
  video's edit `GEMINI_MODEL=gemini-3.1-flash-lite` (the key stays the placeholder), the video's fix
  `uv python pin 3.13` (CPython 3.13.16), and a `.venv` with the exact versions of the capture's
  `uv sync` (`adk-laptop/12`) minus PyTorch and the packages only it and sentence-transformers need
  (`adk-packages.txt`: 137 of 148; about 1 GB less disk; `adk web` never imports them). From then on
  `uv run` ran with `UV_NO_SYNC=1`, so it would not add PyTorch back. `setup-rename.log`: the video's
  rename (`mv 1-baseline baseline; mv 3-mcp-tools mcp_tools; mv 5-custom-agent custom_agent`).
  `arun.sh` runs a command as `student` in the repo root, with no network unless `NET=host` (npm and PyPI
  downloads; the check laptop's `~/.npmrc` carries the proxy and CA, as in the capture). `web.sh` starts
  and stops `uv run adk web` for a check.
- **Stand-ins.** `standin.py` (llm-rag): replaces `llm_client.models.generate_content` with scripted
  replies and the query embedding with the stored vector of one chunk; prints each model call's contents
  and tool config. `adk_standin.py` (ADK): a `BaseLlm` subclass whose replies are written by hand; it
  prints the system instruction and contents ADK would send, and any response schema.
- **Colab notebooks** (`colab-setup.sh`): three venvs on `python:3.12-slim-bookworm`, each with exactly
  what its notebook's install cell installs: `openai-agents==0.3.2` (Travel Planner cell 8);
  `agent-framework-core==1.18.0`, `agent-framework-openai==1.14.3`, `opentelemetry-api==1.42.1`
  (Newsletter cell 8); `fastmcp openai-agents`, unpinned, as Cheese Quiz cell 10 does (fastmcp 4.1.1,
  openai-agents 0.24.0 that day). `notebook.py` executes chosen cells from `assets/source/colab/` (the
  Newsletter's `USERS` cell is the redacted copy) into one namespace, as a runtime would; `crun.sh` runs a
  check with no network, so no OpenAI call could happen.

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| Q1, Q2 | captures `cli-container/31`, `32`, `33`; google-genai 1.39.1's `FunctionCallingConfigMode` docs (`q2-function-calling-modes.log`) | `ANY` = "constrained to always predicting function calls only" (`types.py:500-501`), `AUTO` = "model decides…" (`:498-499`), `VALIDATED` (`:504-505`) |
| Q3 | `grep` of the installed libraries (`q3-caps-a.log`, `-b`, `-c`) | openai-agents 0.3.2 and 0.24.0: `DEFAULT_MAX_TURNS = 10`, `MaxTurnsExceeded` (0.3.2 `run.py:538`); agent-framework-core 1.18.0: `DEFAULT_MAX_ITERATIONS = 40` (`_tools.py:102`), "Phase 3: the iteration budget is exhausted, so request one final response with tools disabled" (`:3734`); google-adk 2.12.0: `_DEFAULT_MAX_LLM_CALLS = 500` (`run_config.py:38`), `is_final_response()` (`events/event.py:286-308`) |
| Q4, B4, C4 | `q4_whiteboard.py`: `baseline/agent.py`'s `root_agent`, unchanged, each `LlmAgent`'s model swapped for the stand-in, through ADK's `InMemoryRunner`; a second session; the planner alone (`q4-a-whiteboard.log`) | instructions arrive with `{itinerary_validation}` / `{travel_plan}` filled from state; the summarizer's contents also hold "[ItineraryValidator] said" and "[TravelPlanner] said" blocks; state has the three keys, 4 events; new session `{}`, 0 events; planner alone → `` KeyError: "Context variable not found: `itinerary_validation` in agent 'TravelPlanner'." `` |
| C4 | `c4_optional_key.py`: the planner alone with `{itinerary_validation?}` (`c4-optional-placeholder.log`) | the instruction goes out as "Using , design a realistic…" |
| Q5, B9 | `b9_travel_gate.py`: Travel Planner cells 9, 12, 14, 15, 18, 20, 21 executed; `finalize_plan`, `apply_confirmation`, `check_itinerary` called directly; `run_turn` with stand-in agents (`b9-travel-gate.log`); B9's cell exactly as printed (`b9_snippet.py`, `b9-b-snippet.log`) | two calls in one turn: `needs_confirmation` both; after "yes": `within_budget`, 2,690.0, remaining 3,310.0; approve: `Yes!`, `yes please`, `y`, `Confirm.`, `yes, confirm`; not: `Yes, please.`, `OK`, `sure`, `Yes go ahead`; 15:00 flight 2,790.0; `SFO-GATE` + pets → `ValueError: Hotel does not meet…`; without pets 2,410.0 and `needs_confirmation`; an "itinerary" without finalize → retry, then `RuntimeError: The agent returned an itinerary without a successful same-turn check.`; money in prose → `[warning]`; `SQLiteSession(…, db_path=':memory:')` |
| Q5, B10 | `b10_newsletter.py`: Newsletter cells 9, 16 (redacted), 18, 20 executed; `generate_newsletter` with three stand-in orchestrators; `validate_newsletter` with the five added lines; `Settings` (`b10-newsletter.log`) | "says done" → `RuntimeError: No successful tool receipt. Orchestrator response: Newsletter sent successfully!`; "sends" → `Saved HTML: … (3014 bytes). No email sent.`; "file gone" → `RuntimeError: The mock email receipt points to a file that does not exist.`; URL draft: `ready` as committed, `error` + no receipt with the check; recipient `<email>` → `ValueError: Use a single email-shaped preview recipient…` |
| B1, D5 | `b1_two_tools.py`: the dispatcher with hand-written calls and a stand-in query vector (a stored chunk about rennet) (`b1-two-tools.log`) | by author `George E. Newell`: 10 of 10 from *Hand-book on cheese making*; all books: 6 + 4 from *The Book of Cheese*; both 3,509 characters; `Milk Industry Foundation`: 10 results; the Woman's Institute author: 0 results, its chunks' metadata `{'book': 'Womans Institute Library of Cookery'}` |
| B2 | copy `b2` (`b2.patch.py`, `b2-a-diff.log`); `request_call1.py` prints call 1's request and stops (`b2-b-request-no-tool-config.log`); `b2_text_reply.py` with a stand-in text reply (`b2-c-text-reply.log`) | top-level keys `contents`, `tools`, `generationConfig` (no `toolConfig`); `Function calls: []`, `Function calls did not result in any responses...`, 1 model call |
| B3 | copy `b3` with the loop (`b3.patch.py`, `b3-a-diff.log`); `b3_loop.py` in three scenarios (`b3-b-loop-*.log`) | contents roles per call `[user]`, `[user, model, user]`, 5 contents; `Answer:` after 3 calls; never-stops: 5 calls, `Gave up after 5 steps`; the real SDK builds request 3 (`functionCall` / `functionResponse` parts), not sent |
| B5 | `b5.patch.py` writes `conditional_agent_lower.py` and `conditional_agent_schema.py` beside the original (`b5-a-patch.log`); `b5_router.py` runs each module's own `main()` (its three test queries, Runner and `ConditionalAgent`) with stand-in models (`b5-b` … `b5-f`); `uv run --project ..` vs `uv sync --dry-run` in the module folder (`b5-g-which-venv.log`) | committed: `simple`/`complex`/`ambiguous` route right, `Simple` and `complex\n` → `ClarificationHandler`; `.strip().lower()`: right; `output_schema`: the class sent as response schema, `application/json`, routes right; `{"complexity": "Simple"}` → `ValidationError` (literal_error); `--project ..` → the root `.venv`; in-folder sync "Would install 276 packages" |
| B6, C5 | `b6_module4.sh`: `uv run --project .. uvicorn app.main:app --port 8080` and the README's requests, no internet (`b6-a-module4-api.log`); `b6_sessions.py`: `AgentRunner.run` twice with a stand-in (`b6-b-two-requests.log`); `c5_error_event.py`: the runner's events (`c5-error-event.log`) | `/health` `{"status":"healthy"}`; `/docs` 200; `/chat` 500, log: the model error, then `AttributeError: 'NoneType' object has no attribute 'parts'` at `app/runner.py:46`; wrong field 422; second request sends only its own message; 2 sessions, 2 users; the final event: `content=None error_code='ClientConnectorDNSError'` |
| B7 | `b7.patch.py` copies `2-litellm` to `litellm_agent` (with `LiteLlm(model="openai/gpt-5.6-luna")`) and to `litellm` (`b7-a-patch.log`); `b7_litellm.py`: `LLMRegistry.resolve`, `AgentLoader`, a first message without `OPENAI_API_KEY` (`b7-b-load.log`) | `gpt-4` → `google.adk.integrations.openai._openai_llm.OpenAILlm`; `openai/…` → `LiteLlm`; `2-litellm` → `Invalid agent name`; `litellm` → `No root_agent found for 'litellm'`; `litellm_agent` loads; first message → `Missing credentials …` (no request sent); the copies were deleted afterwards |
| B8 | `b8_mcp.py`: the module's own `MCPToolset` (npx, stdio), committed filter and a copy with `read_text_file` added (`b8-a-mcp-filter.log`); a filter naming a missing tool (`b8_missing_name.py`, `b8-b-missing-name.log`) | 3 → 4 tools; `read_file`: "DEPRECATED: Use read_text_file instead."; `search_files` `agent` → "No matches found", `**/*agent*` → 2 paths; `../.env` → "Access denied - path outside allowed directories"; missing name → no error, two tools |
| B11 | `b11_adk_git.sh`: `adk web`, one session through `POST /apps/baseline/users/student/sessions`, `git add --all --dry-run` before and after `.adk/` in `.gitignore` (undone after) (`b11-adk-sessions-git.log`) | "Creating local session service at …/baseline/.adk/session.db"; `add 'baseline/.adk/session.db'`; then `.gitignore:73:.adk/` and no longer listed |
| C1 | `c_module_env.sh`: `adk web`, the agent tree from `/dev/apps/baseline/build_graph` with only the root `.env`, then after `cp .env.example .env` in `baseline/` (removed after) (`c1-module-env.log`); `c1_mcp_env.py`: `list_directory` and `read_file` on a module `.env` in `mcp_tools/` (removed after) (`c1-b-mcp-module-env.log`) | root: `Loaded .env file for baseline at …/.env`, `model gemini-3.1-flash-lite` ×3, earlier sessions still listed after a restart; module: `… at …/baseline/.env`, `model gemini-2.0-flash` ×3; the module `.env` listed and read in full |
| C2 | copy `c2` with `print(response.text)` (`c2.patch.py`, `c2-a-diff.log`); `c2_second_call.py`: the staff's recorded call 1 (`out.txt:20-28`) then a stand-in function call as reply 2 (`c2-b-second-call.log`) | "Warning: there are non-text parts in the response: ['function_call'] …", then `None`; 2 model calls |
| C3 | `c3_python_pick.sh` in a throwaway home on the check laptop, fresh clone (`c3-python-pick.log`) | without a uv-managed Python: `Using CPython 3.12.15 interpreter at: /usr/local/bin/python3`; after `uv python install 3.15`: `Using CPython 3.15.0`, `error: Distribution onnxruntime==1.31.0 … can't be installed …` |
| C6 | `c6_fastmcp_rerun.py`: Cheese Quiz cells 11, 48, 57 in one process; a FastMCP client calls the tool; cell 57 edited and run again (`c6-fastmcp-rerun.log`) | second run prints `Server thread alive: True`, then `[Errno 98] … address already in use`; 3 s later the thread is dead; the client still gets a random fact from the old function |
| C7 | `vertexai.preview.rag` import and `setup_corpus.py` without the project variable (`m6-c-vertex-rag-import.log`); the menu with `GOOGLE_CLOUD_PROJECT=your-project-id`, option 5 twice, `y` then `yes` (`m6-d-delete-corpus-menu.log`) | google-cloud-aiplatform 2.5.0, a deprecation warning; `Error: GOOGLE_CLOUD_PROJECT environment variable not set.`; `y` → `Cancelled.`; `yes` → `rag.delete_corpus` → `DefaultCredentialsError` |
| C8 | `m6_chroma.py` against the Chroma server (`m6-a-heartbeats.log`); `docker exec` into it (`m6-b-chroma-image.log`); `docker image inspect` (`m6-e-chroma-image-config.log`); the image started with the module compose file's environment and volume path, one record added (`m6-f-module-compose-settings.log`) | v1 heartbeat 410 "The v1 API is deprecated", v2 200; no `curl` in the image; `chroma 1.4.4`; no declared volume, entrypoint `chroma run /config.yaml`; data in `/data`, `/chroma/chroma` empty |
| D3 | the installed google-adk's memory package and the tutorial repo (`d3-adk-memory.log`) | `memory/`: in-memory, SQLite, Vertex AI Memory Bank and RAG memory services; `load_memory_tool.py`, `preload_memory_tool.py`; `git grep` in the repo: no match |
| D4 | `Agent.as_tool` in openai-agents 0.24.0 (`d4-as-tool.log`) | `max_turns: int \| None = None` (`agent.py:617`) → `DEFAULT_MAX_TURNS` (`:755`) |
| D6 | `git show 14f2a14:src/vector-db/agent_tools.py` of `cheese-app-v2` (lecture 18) against llm-rag's (`d6-cheese-app-v2.log`) | identical |
| teardown | `adk telemetry --help`, `adk telemetry disable` (`d-telemetry.log`) | commands `disable`, `enable`, `status`; writes `~/.adk/config.json` `{"telemetry": false}` |

## Not run (and why)

- **Every model reply.** No key: which tool Gemini picks (B1), its greeting (B2), real loop laps (B3),
  the baseline's three replies (B4), the router's handlers (B5), module 4's answers (B6), an OpenAI answer
  through LiteLLM (B7), MCP calls chosen by a model (B8), the notebooks end to end (B9, B10, C6). Stand-ins
  drove the code instead; the answers name what a model would add.
- **Google Cloud.** Creating or deleting a Vertex AI RAG corpus and the RAG Engine tier (C7): the delete
  path was followed up to the credentials check; the billing advice comes from Google's documentation
  (RAG Engine deployment modes and Spanner mode pages, "last updated 2026-10-15", read on 2026-10-19).
- **PyTorch.** Not installed in the ADK check venv, so `6-rag/2-custom-chromadb-rag`'s ingestion and agent
  (sentence-transformers) were not run (C8 checked the server side only). Module 4's Docker variant was not
  built (B6's note on `GEMINI_MODEL` follows from `app/agent.py:12` and the Dockerfile).
- **Code shown but not executed:** C5's wrapper fix (the attributes it reads were checked in
  `c5-error-event.log`), D4's ways of enforcing the review limit.
- llm-rag ran as root in a container without the image's apt layer (see Setup); `cli.py` behaves the same.

## Cleanup

Removed afterwards, by name: the container `l06ex-chroma` (and `l06ex-m6`, removed inside its check), the
network `l06ex-net`, the volumes `l06ex-rag-work`, `l06ex-rag-venv`, `l06ex-chroma-data`, `l06ex-adk-home`,
`l06ex-colab` (and `l06ex-m6-chroma`), the image `l06ex/adk-laptop`, and the two build-context files in the
session scratchpad. Inside `l06ex-adk-home`, the extra files the checks made (`litellm/`, `litellm_agent/`,
the router copies, the module `.env` files) were deleted file by file before the git check, so
`b11-adk-sessions-git.log` lists only what a student's folder would hold. The Docker daemon (its log is
in the session scratchpad) and the build cache were left in place: other work may use them.
