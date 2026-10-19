# Brief · AC215 L6 — LLM: Agents I (follow-along: llm-rag Agents, llm-agent-google-adk, three Colab notebooks)

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the tutorial digest), `SLIDES.md` (the lecture; binding next to the digest,
series rule 9) and `assets/` (real captures, see `ASSETS.md`). **Where the digest and the captures
disagree, the captures win.** They are newer (2026-10-18, 22:58–23:33 UTC; both repos' `main` still
at the pinned commits `e17a39f` and `f89faa7`) and were made on the machines the video shows: a
Linux laptop with Docker for llm-rag, a fresh Debian 12 laptop with uv and Node.js (and no Python)
for ADK. Neither had a Google or OpenAI key.

| topic | digest | captures (use these) |
| --- | --- | --- |
| ADK `uv sync` as the README writes it | works; resolves google-adk 2.12.0 (checked with `uv lock` on a Python 3.12 image) | **fails on a fresh laptop**: `Using CPython 3.15.0`, `Resolved 189 packages`, then `onnxruntime==1.31.0` has no `cp315` wheel, exit 2 (`adk-laptop/07`). Fix: `uv python pin 3.13` (`09`), `uv sync` again (`12`) |
| the `1-baseline` folder name (G1) | pin `google-adk>=1.8.0,<1.28` (→ 1.27.5), or symlinks | the pin is **not** enough: 1.27.5 lists the four folders (`25`) but `adk web` refuses the app when you pick it: `Invalid app name '1-baseline': must be a valid identifier…` (`24:131-132`, `26`). Symlinks failed too (ASSETS, not kept). **Renaming works**: `mv 1-baseline baseline` etc. with today's ADK 2.12.0 (`28`–`31`) |
| ADK 2.12's error text | `Invalid agent name: '1-baseline'. Agent names must be valid Python identifiers (letters, digits, and underscores only).` | `… must be valid Python identifiers or paths separated by dots (letters, digits, underscores, and dots).` (`18`) |
| the agent dropdown | exactly four folders | ADK 2.12 lists **seven** (`4-production-ready.app`, `6-rag.1-vertex-rag-engine`, … `17`); four only under 1.27.5 (`25`) |
| first `adk web` | starts the server | ADK 2.12 first asks `Enable telemetry? [Y/n]` (Enter means yes, although the text says it is off by default), then starts (`15:1-13`) |
| the placeholder key | — | `adk web` starts and loads agents with it; the first message is refused by Google: `400 INVALID_ARGUMENT … API key not valid` (`29:357-358`), the browser gets `Internal Server Error` (`33`) |
| which `.env` | the nearest one, override | confirmed: `Loaded .env file for baseline at …/llm-agent-google-adk/.env` (`29:36-37`) — the root file, because no module `.env` was copied |
| sessions on disk | — | `baseline/.adk/session.db` (`29:41-42`); the repo's `.gitignore` does not cover `.adk/` (`39`) |
| MCP filesystem server | 3 of 14 tools; four files + `__pycache__` | confirmed (`35:30-37`) |
| remote MCP server | 406 to a browser, `initialize` / `tools/list` work | confirmed, plus a real `tools/call` (`mcp-remote/01`–`04`; the fact changes every run: use the file's text, not ASSETS's) |
| port 8000 | `adk web` vs Chroma: Errno 98 | confirmed, exit 3; `--port 8080` starts (`36:21`, `37:34`) |
| `--agent` on a fresh clone | NotFound at `get_collection` | confirmed: `chromadb.errors.NotFoundError: Collection [char-split-collection] does not exist`, before any Gemini call (`cli-container/10`) |
| `--agent` with the collection, no key | `DefaultCredentialsError` at the first `generate_content` | confirmed at `cli.py:441`, after `user_prompt_content` is printed (`30`) |
| the two requests | read from the code | **built by google-genai 1.39.1 and printed, never sent**: call 1 has `"toolConfig": {"functionCallingConfig": {"mode": "ANY"}}`, `"temperature": 0.0`, no `systemInstruction` (`31`); call 2 has three contents (user, the model's turn with `thoughtSignature`, a `functionResponse` with no role), `tools` again, **no** `toolConfig`, `"generationConfig": {}` (`33:137-233`) |
| the Compose pull message | `failed to resolve reference … not found` (L05) | this laptop's classic image store prints `pull access denied for llm-rag-cli …` (`laptop/06:6-9`); both harmless, a student with Docker Desktop sees L05's wording |
| the container | `llm-rag-llm-rag-cli-run-<id>` | `llm-rag-llm-rag-cli-run-61b50b7d6730`, prompt `app@abcf218747d0:/app$` (`laptop/06:34`, `:41`) |
| the workspace | `~/Desktop/AC215` | `~/AC215` (both laptops); say "wherever you keep your clones" |
| `uv sync` after the pin | 189 / 218 packages | a student sees `Resolved 189 packages` and plain `torch==2.14.1` (plus ~3 GB of CUDA packages on a Linux PC, `10`); the capture's `Resolved 171` and `torch==2.14.1+cpu` come from a capture-only CPU index (`11`): never show those two lines |

## Audience and goal

An AC215 student who has done L1–L5: uv, `pyproject.toml` and `uv.lock` (L1); containers,
`docker-shell.sh` and a mounted service-account key (L2–L4); L05's RAG pipeline in `llm-rag` (chunk
→ embed → load into `char-split-collection`, query, chat). They read Python comfortably (including
`async`/`await` at a reading level) and have used a chat assistant, but have never written a tool for
an LLM, used an agent framework or heard of MCP. They watch with three things open: their
`~/AC215/llm-rag` clone (with L05's collection still on disk), a fresh clone of
[dlops-io/llm-agent-google-adk](https://github.com/dlops-io/llm-agent-google-adk), and a Colab copy of
the Cheese Quiz; they pause to type each command.

After the video they can:
- say what separates a plain LLM call, a reasoning *workflow* and an agent (who decides the next
  step), and name the lecture's five blocks of an agent — LLM core, instructions, dynamic control,
  tools, memory — and which one nobody writes by hand;
- explain that each model call is a fresh, stateless request that carries all its context, and spot
  a swapped `system`/`user` role;
- read a function declaration (name, description, JSON-schema parameters, `enum`, `required`) and
  explain function calling: the model *writes* `{name, args}`, their code *makes* the call, and a
  second request carries the question, the model's own turn (thought signature intact) and the
  function response; say what `mode="any"` forces and what it takes away;
- run llm-rag's `--agent` on top of L05's collection, read its trace, and explain why the staff's
  recorded answer talks about a book that no longer exists;
- explain the agent loop and its stop rule (a reply with no function call), the turn caps frameworks
  add, and why llm-rag's "agent" runs exactly one lap;
- set up the ADK repo: the real folder name, the key and a current model in the root `.env`, the
  failing `uv sync` and `uv python pin 3.13`, `uv run adk web` (telemetry question, port 8000), and
  folder names that ADK accepts;
- explain ADK's Runner, session, state and events, `output_key` and `{key}`, and the difference
  between session state and the lecture's memory;
- explain MCP — one protocol, one connection per server, over stdio or HTTP — and `tool_filter`; sort
  tools into the lecture's data, action and orchestration families;
- compare three ways to compose agents by who plans the order (code, an orchestrator model, Python
  reading a model's label);
- explain the harness ideas in the last two notebooks — Python-owned arithmetic, an approval gate only
  a later human turn opens, success as a receipt for a file on disk — and why a rule written in the
  prompt is not a check;
- tear down: `exit` + `docker compose down` (port 8000), Ctrl+C, delete the Colab runtimes, look after
  three keys.

## Length and parts

~30 minutes. Narration **~4,250 words** (3,900–4,300; Kokoro af_heart, speed 0.9 ≈ 174 wpm ≈ 24.5
min of speech); typing, real output, five ponders and recorded notebook outputs add ~6 min. The
tutorial is long — one README section that stands on L05, a whole second repo, three notebooks — so
the video follows **every command** of llm-rag's *Agents* section and of the ADK root README, and uses
each notebook for the one idea it teaches best, with its saved outputs. ADK modules 2, 4 (beyond one
code panel) and 6, the Travel Planner's interactive chat and the Guild's schemas go to exercises.md.

The cut falls where the hand-written agent is torn down and the frameworks begin:
- **Part 1 = S01–S08, what an agent is, and function calling by hand** (~2,130 words, ~12.2 min of
  narration, ~15.5 min): the hook, the three lanes and the anatomy (Cheese Quiz), the envelope,
  llm-rag's tool menu, its two calls run against L05's index, the loop. It ends with `exit` and
  `docker compose down` — "part 2's web server wants port 8000 too" — on a clean frame.
- **Part 2 = S09–S16, frameworks own the loop** (~2,120 words, ~12.2 min, ~15 min): ADK setup and its
  three traps, state, MCP, many agents, the two harness notebooks, teardown and recap. It opens on a
  fresh laptop terminal and a new repo.

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 260 | S09 AdkSetup | 360 |
| S02 SteeringWheel | 280 | S10 AdkWeb | 300 |
| S03 Envelope | 200 | S11 SharedState | 270 |
| S04 ToolMenu | 290 | S12 McpPlugs | 280 |
| S05 BackInTheContainer | 250 | S13 ManyAgents | 240 |
| S06 CallOne | 280 | S14 ApprovalGate | 260 |
| S07 CallTwo | 300 | S15 Receipt | 200 |
| S08 TheLoop | 270 | S16 Recap | 210 |
| **part 1** | **2,130** | **part 2** | **2,120** |

Word budgets are targets (±15 %); the total must stay inside 3,900–4,300.

## The lecture behind the tutorial (SLIDES.md)

One deck, "Lecture 6: LLM: Agents I", slides 1–56 (the PDF page is the footer). It has **no code**:
it teaches with box diagrams and annotated screenshots of a chat product. The video redraws its master
picture, **slide 27's agent anatomy**, as the running map (V1) and lights one block per chapter. Its
RAG recap ladder (8–14) becomes S04's menu, its "how an agent works" hub (35–41) S08's loop, its tool
slides (51–53) S12, its research example (44–49) S13's tree, and its travel planner (20–22) S01's
motivation and S14's opening. S01 says once what the GREY `lecture_ref` tag means ("Lecture 6 ·
slides 20–22"). Where the slides and the captures disagree, the captures decide what the scene shows
and the narration says so kindly in one sentence:

| # | slides | tutorial / captures | scene |
| --- | --- | --- | --- |
| 1 | an agent runs until the task is done (26), cycling through planner, tools and memory (37–40) | llm-rag's `--agent` makes two calls and stops: the README calls it an agent, by the lecture's definition it is one lap; call 2 has no tool config, so a second tool request would only be printed (`cli.py:441`, `:465`, `:478`; `cli-container/31`, `33`) | S08 |
| 2 | the agent decides *whether* to retrieve (Self RAG 10–11, the menu's "Retrieval Decision" 13, the assistant that skips search for a stable topic 33) | `mode="any"` forces a call: `"mode": "ANY"` in the real request (`31:86-90`); it chooses *which* search, never whether | S06 |
| 3 | memory persists across sessions (40–41) | the ADK README calls per-session state "Memory" (`README.md:140`); in ADK's code it is session state; none of today's runs keeps memory across sessions | S11 |
| 4 | one "MCP" box between the host and every server (53) | one connection per server: an `npx` child process over stdio (`adk-laptop/35`), a remote server over HTTP with its own session id (`mcp-remote/`), a FastMCP thread on `:8001` (Cheese Quiz cell 57) | S12 |
| 5 | the planner books a Paris trip and replans for weather and delays through live systems (20–22) | the Travel Planner plans Seattle → San Francisco from a mock catalog and books nothing (`colab-travel-planner-c27-turn4-yes.txt:9`); ADK's `1-baseline` is three tool-less `LlmAgent`s (`adk-laptop/31`) | S11, S14 |
| 6 | "reasoning" names a multi-call engine (16–18) and the model's own thinking (31–33) | the Cheese Quiz's `ReasoningLLM` is 11 calls ordered by Python (`c25`); Gemini's thinking lives inside one call, its `thoughtSignature` sent back unchanged (`33:151`) | S02, S07 |
| 7 | success criteria and guardrails live in the instructions and the decision maker (36–37) | the last two notebooks enforce them in code: an approval gate, Python's arithmetic, a receipt; a rule left in the prompt slipped (the "no URLs" rule vs the saved preview) | S14, S15 |

SLIDES.md's gaps, adopted: the anatomy as the running map (gap 1: S02, S08, S11, S16); agentic RAG
and the choice not to retrieve (gap 2: S04, S06); why agents (gap 3: S01, S14); the three tool
families (gap 4: S12, S14); the LLM core as a design decision (gap 5: `temperature=0` in S06, the
model line in `.env` in S09); who plans the order (gap 6: S13); the research tree and the formula (gap
7: S13, S16); check, don't trust (gap 8: S15, one clause).

Terms: use the lecture's words (*agent*, *LLM core*, *instructions*, *dynamic control* / *decision
maker*, *planner*, *tools*, *memory*, *building blocks*, *agentic RAG*, *retrieval decision*,
*function calling*, *data / action / orchestration tools*, *MCP host, client, server*, *sub-agent*,
*deep research*) and add the tutorial's where the lecture stops (*function declaration*, *function
call*, *function response*, *forced tool call*, *agent loop*, *stop rule*, *turn cap*, *Runner*,
*session*, *state*, `output_key`, *transport*, `tool_filter`, *agents as tools*, *workflow agent*,
*harness*, *approval gate*, *receipt*). Qualify, never repeat loosely: "agents invoke tools" → the
model asks, your code runs; "memory" → cross-session memory or per-session state; "reasoning" → a
workflow of calls or the model's own thinking; the "MCP" box → one protocol, one connection per
server; "agent" for `--agent` → one tool call, no loop. Slide slips are not copied (39 "interest",
51 "can invoked", 52 "Toolt 4", 36 "Guideline"); the deck's "Reasoning Engine" names two different
things — say which.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop: `~/AC215`, the two clones, the laptop terminal, the browser and the ADK dev UI as a page on it, `.env` as a file; the user's turn ("the human types yes") | GREY |
| the cloud: every **model** (the LLM core: `gemini-3.1-flash-lite` on Vertex AI, the Gemini API behind the AI Studio key, OpenAI's `gpt-4o` / `gpt-5.6-luna`), anything the model writes (the function-call card, the answer, the orchestrator's "done!"), OpenAI's hosted `web_search`, the remote MCP server, the Colab VM's frame, the hosted Cheese Agent Tool | BLUE |
| containers: `llm-rag-cli` (where `cli.py` and `agent_tools.py` run — the dispatcher, the two calls), `llm-rag-chromadb` and its collection cylinder; the function-response card llm-rag's code builds | TEAL |
| a Python that was already on the machine (V5: none on our laptop; a Mac's old system Python would sit outside `>=3.10`) | ORANGE |
| project-owned and pinned: the function declarations (the menu: names, descriptions, `enum`), chunk cards and records (as in L05), session-state cells, `.python-version`, `pyproject.toml`'s lines, everything the harness *checked* (the approved proposal, Python's budget report, the receipt) | GREEN |
| tools you install and the loops they run: docker / Compose, uv (and the CPython it downloads), Node.js / `npx` and the filesystem MCP server package, ADK (`adk`, `Runner`, `SequentialAgent`), the OpenAI Agents SDK (`Runner.run`), Microsoft Agent Framework, FastMCP; the dynamic-control block once a framework fills it | PURPLE |
| errors and "avoid this": every traceback's last line, `NotFoundError`, `DefaultCredentialsError`, the missing `cp315` wheel, `Invalid agent name`, Errno 98, 406 to a browser, `MaxTurnsExceeded`, a rejected turnstile, the swapped roles, a rule that slipped | RED |
| your turn, the trackers, "look here now", the anatomy block in focus, the PENDING stamp | YELLOW |
| money: every model call and hosted search (GOLD tick per call), and the three keys — the service-account key (L05), the AI Studio key, the OpenAI key — always a GOLD key glyph, never their content | GOLD |
| routes and lookups: the user's question and `search_content`, the query vector, the trust-boundary crossing, MCP transports (the stdio pipe, HTTPS), `localhost:8000` / `:8080` / `:8001`, the `{key}` placeholder holes, "the nearest `.env`" | PINK |
| lecture concepts with no code here (Self RAG, Corrective RAG, handoffs, the research tree, `ParallelAgent`), and the future (L07's harness) | GREY, dashed |

The colour of a card says **who wrote it**: the model's function call is BLUE, the response your
code builds is TEAL (llm-rag) or GREEN (a harness check). That is the video's thesis in one rule.
In Colab both the model and your code live in Google's cloud, so the notebook scenes draw the Colab
VM as a BLUE frame and let the **dashed trust boundary**, not the colour, separate your code from the
model. The anatomy (V1) does not copy the slide's colours (its red and green would read as "error"
and "project-owned"): the LLM core is BLUE, the other four blocks are outlined in GREY until filled,
the block in focus turns YELLOW, and dynamic control is dashed (slide 41 greys it out) until a
framework fills it in PURPLE.

## Running example

- **llm-rag laptop:** user `student`, host `laptop`: `student@laptop:~/AC215$`, then
  `student@laptop:~/AC215/llm-rag$`; the container prompt `app@abcf218747d0:/app$` (`laptop/06:41`);
  say once that the part after `app@` is the container id and changes every run.
- **ADK laptop:** `student@laptop:~/AC215$`, then `student@laptop:~/AC215/llm-agent-google-adk$`.
  The browser: `http://localhost:8000/dev-ui/` (`adk-laptop/16`).
- **Colab:** schematic notebook frames (tagged `illustration`) with the notebook's own section titles;
  outputs come from `expected/colab-*` (tagged `recorded`, "the staff's last saved run").
- **The question:** `"Describe where cheese making is important in ‹instructor›'s book?"`
  (`cli.py:435`); the narration says "the instructor's book".
- **The instructor's name is never on screen or in the narration.** `scenes/common.py` gets one helper
  (e.g. `unname(text)`) that every panel line goes through: it replaces `Pavlos Protopapas`,
  `Protopapas`, `Pavlos` and `pavlos` with a GREY chip `‹instructor›` (so `‹instructor›_fun_fact_mcp`,
  `https://‹instructor›-fun-facts.dlops.io/mcp`, `"‹instructor› Cheese MCP"`). S01 says it once: "on
  screen we hide the instructor's name; your terminal shows it". The captured files stay unchanged.
  The staff readers of the Newsletter are already `<reader1>`… / `<email>` in `assets/`.
- **Other names:** Mara and Anja are characters in the instructor's short story (fine). Public-domain
  authors appear only inside the `enum` panels (`agent_tools.py:19-29`, `31:42-52`) and the per-author
  table (`34:16-25`), never in captions or narration; otherwise books are named by title.
- **Placeholders:** `GCP_PROJECT="your-project-id"` (`laptop/05:11`; the course's `ac215-project`
  appears only in the diff line the viewer must edit, `:10`); `GOOGLE_API_KEY=your_google_ai_api_key_here`
  (`adk-laptop/06:2`); the OpenAI key is the Secrets panel's name `OPENAI_API_KEY`, never a value.
- **Long outputs:** first and last lines with a `…` line; tracebacks: the first `/app/…` frame that
  matters and the last line. Long JSON request bodies fold with `…` lines; the key being discussed is
  highlighted. Long extra commands (the `python - <<'EOF'` check scripts `31`, `33`, `34`, `35`; the
  long `curl` lines of `mcp-remote/`) are collapsed to their first line plus a caption saying what the
  script does ("prints the request instead of sending it"); the full scripts are in `assets/` and the
  study guide.
- **Versions** are "at the time of recording": Docker Engine 29.8.2, Compose v5.6.0, Python 3.12.15,
  uv 0.13.1, chromadb 1.1.0, google-genai 1.39.1 (container); CPython 3.15.0 then 3.13.16,
  google-adk 2.12.0, Node.js v24.22.0, npm 11.19.1 (ADK laptop); the remote server 1.16.0, protocol
  `2025-06-18`; the notebooks' saved runs (Cheese Quiz 2026-09-23, Newsletter 2026-09-20).

## Visual set pieces (the 3Blue1Brown part)

- **V1 · Three lanes, then the anatomy (S02; running map in S04–S08, S11, S16).** One question, "the
  best cheese for a grilled cheese sandwich", the same BLUE `gpt-4o` in three lanes. Lane 1
  (`BaseLLM`): PINK question → BLUE model → answer; a counter "1 call · 2.81 s" (`c21:30`). Lane 2
  (`ReasoningLLM`): a conveyor of GREY code boxes named after the methods (`analyze_query`,
  `decompose_problem`, `answer_sub_question` / `verify_response` ×4, `synthesize_final_response`), each
  pinging the same model; the counter ticks to **11 calls · 39.34 s** (`c25`); the decision diamond is
  GREY — your Python decides; slide 18's technique names (problem decomposition, sequential
  processing, a verification loop, summary generation) float small over the boxes it uses. Lane 3
  (`SimpleAgent`): the diamond is inside the BLUE model; it reaches into a toolbox, takes `web_search`
  (BLUE, hosted) twice, returns, stops; "13.29 s" (`c31`). Then the lanes fold into slide 27's
  anatomy: Task / Goal → the agent box (LLM core BLUE; Instructions; a wide Dynamic Control bar; Tools;
  Memory) → Task completion. Dynamic control lights YELLOW: "this is the steering wheel". A small copy
  sits bottom right from S04 to S08, the block in focus lit (tools S04–S07, dynamic control S08); S11
  labels it with ADK's constructor; S16 fills every block with the tutorial's objects.
- **V2 · The envelope (S03; reused S06, S07).** "LLMs are stateless functions" (Cheese Quiz cell 35):
  every call is a fresh envelope. Seven sheets slide in, one per step, labelled with slide 41's words:
  the user prompt, a system prompt, retrieved documents, prior turns, a profile from past sessions,
  tool outputs, an output schema. Beside it an answer card shows the **top pick**, which changes as the
  sheets arrive — Cheddar (`c38:10`), mild cheddar and mozzarella for the kids (`c41:8`), Havarti
  (`c42:8`), Whole Foods Mild Cheddar (`c43:8`), then a JSON `top_recommendation` (`c44:10`). At step 2
  two sheets carry each other's role label (RED flip, cell 39 lines 19-20). In S06 the envelope opens
  onto the real call-1 body (`31`); in S07 a second envelope holds three contents (`33`).
- **V3 · The model writes the call, your code makes it (S04 build; S06–S07 run).** First the menu:
  L05's strip (slide 8: question → Retrieval → LLM → Response); slides 9–12's boxes (Pre-Retrieval,
  Post-Retrieval, Retrieval Decision, Document Eval, Query Rewrite, Web Search) fly into slide 13's
  column between two LLMs (GREY dashed: concepts); the column shrinks to llm-rag's two GREEN menu cards,
  `get_book_by_author(author, search_content)` and `get_book_by_search_content(search_content)`, with
  "Retrieval Decision" left as a dashed card (crossed out in S06 when `mode="any"` appears). Then the
  stage: BLUE Google cloud (Gemini, location `global`) | a dashed trust boundary labelled "HTTPS" | the
  GREY laptop holding the TEAL CLI container (`cli.py`, `agent_tools.py`) and the TEAL Chroma container
  (the collection; metadata `book`, `author`, `year`). The model's speech bubble becomes a BLUE JSON
  card `{name, args}` with a small BLUE seal (the thought signature); it crosses the boundary; the
  dispatcher's two `if function_call.name == …` branches (`agent_tools.py:88`, `:111`) route it; PINK
  `search_content` → an embedding → `collection.query(…, n_results=10, where={"author": …})` → ten GREEN
  chunk cards → joined into one string → a TEAL `{"content": …}` card stapled to the call; the bundle
  crosses back with the seal intact; prose comes out. Slide 39's three duties caption the trip: pick
  the tool (the name), format its inputs (the arguments), interpret the output (call 2). The model
  never touches the cylinder.
- **V4 · The loop and its stop rule (S08).** Slides 35–40's hub: the LLM core and the prompt
  "become" a decision maker, with two-way spokes to planner, tools and memory. The tools spoke unrolls
  into a circular track: model → tools → model. A token runs laps; a counter ticks against a cap
  (`max_turns=12`, Cheese Quiz cell 71). When the model emits text with no function call, a gate opens:
  a final response. Replay: the counter hits 12/12 and a RED `MaxTurnsExceeded` gate slams. llm-rag's
  run is drawn as one fixed lap with no gate: after call 2 the program simply ends. Slide 41's greyed
  dynamic-control block fills PURPLE: "the framework writes this part".
- **V5 · Which Python, which wheel (S09).** L01's number line returns: 3.10 … 3.16 with
  `requires-python = ">=3.10"` glowing GREEN. No ORANGE dot: this laptop has no Python (`00:9`). A
  PURPLE download arrow drops `CPython 3.15.0` at the newest end. `onnxruntime 1.31.0` arrives (via
  `chromadb`, `pyproject.toml:18`) as a shelf of wheels tagged `cp311 cp312 cp313 cp313t cp314 cp314t`
  (`07:9-11`); the 3.15 slot is empty → RED. `uv python pin 3.13` collapses the interval to one point;
  the `cp313` wheel clicks in → GREEN; a `.python-version` file appears.
- **V6 · The shared whiteboard (S11).** A GREEN session board with three empty cells
  (`itinerary_validation`, `travel_plan`, `trip_summary`, from `adk-laptop/31`); `state: {}`,
  `events: []` (`32`). A PURPLE Runner takes a message; `ItineraryValidator` (BLUE model chip +
  instruction card) writes cell 1 through `output_key`; `TravelPlanner`'s instruction
  `Using {itinerary_validation}, …` has a PINK hole, and cell 1's text flies into it *before* the call;
  it writes cell 2; `TripSummarizer` reads `{travel_plan}` and writes cell 3. Events stack in a column
  beside the board (what `adk web`'s Events tab lists). The agents never talk to each other; the board
  carries the data. A dashed coda: `ParallelAgent` writes three cells at once on three branches. The
  board is a file: `baseline/.adk/session.db`. Caption throughout: "what ADK does once you add your
  key — no model output was recorded".
- **V7 · One protocol, one plug per server (S12).** Slide 51's three families as three bins (data,
  action, orchestration); the tutorial's tool chips drop into them. Slide 52: an agent with four tool
  pills and ten grey wires, each to a service with its own protocol label ("Do you see a problem?").
  Morph to slide 53: an MCP host with clients, the wires merge into one PINK trunk labelled **"same
  protocol"** (never a box), and an MCP-server adapter clicks onto each service. Zoom to the
  tutorial's three real plugs, each its own connection: (a) a PINK stdio pipe into a PURPLE `npx …
  server-filesystem` child process on the GREY laptop — 14 tool chips fall onto a sieve labelled
  `tool_filter` and three pass (`35`); (b) a PINK HTTPS line to the BLUE remote server, three small
  envelopes `initialize`, `tools/list`, `tools/call` going back and forth, while a browser's plain GET
  bounces off with RED 406 (`mcp-remote/01`–`04`); (c) a PURPLE FastMCP thread on `127.0.0.1:8001`
  inside the BLUE Colab VM (cell 57, `c59`). The model still only writes calls; the client process
  does the talking.
- **V8 · Turnstile and receipt (S14, S15).** A GREEN plan card (the exact proposal JSON, `c26:6-19`)
  walks toward a door marked FINAL; a turnstile stops it and stamps it YELLOW `PENDING`
  (`needs_confirmation`); the model pushes it again in the same turn — same stamp. Next turn a GREY
  human hand types "yes"; `apply_confirmation` copies pending → approved; the stamp flips GREEN
  `APPROVED`; the turnstile turns; a calculator (Python) builds the budget line by line, 880 + 1,000 +
  600 + 150 + 60 = **2,690** (`c27:26-32`), and only that report reaches the user. S15: a newsletter
  draft and the BLUE orchestrator shouting "done!"; the door stays shut until a GREEN receipt token
  with a file path drops into a slot and the file exists. A sticky note on the prompt, "no embedded
  URLs", drifts through the gate unchecked and a URL shows up in the preview (RED): a note is not a
  check.

## README step tracker (top-left)

Step titles ≤ 3 words. The tracker names its source in the header (the `common.py` factory swaps
`ReadmeTracker`'s "README" head for "llm-rag", "ADK" or "Colab"). Steps the README does not have are
marked `extra` in the caption and in the narration ("this one isn't in the README").

`dlops-io/llm-rag` `README.md` @ `e17a39f` (L06's section is *Agents*; three L05 sections it stands on
appear in S05 for a viewer starting fresh):
- *Prerequisites* (`:45-48`, L05), label "llm-rag · Prerequisites": Clone repo (1; the README links
  the repo, the command is not printed)
- *Run LLM RAG Container* (`:75-85`, L05), label "llm-rag · Run Container": cd llm-rag · Set
  GCP_PROJECT · Run script (3)
- *Load Embeddings into Vector Database* (`:144-153`, L05), label "llm-rag · Load (L05)": Load
  char-split (1)
- *Agents* (`:242-271`), label "llm-rag · Agents": Run agent · Agent tool (2)

`dlops-io/llm-agent-google-adk` `README.md` @ `f89faa7` (the whole README is L06's):
- *Getting Started* (`:72-107`), label "ADK · Getting Started": Clone repo · cd folder · Copy .env ·
  Add API key · AI Studio key · uv sync (6, in README order: step 3 says where the key comes from, so
  S09 creates the key while on step 4 and says so)
- *Running Agents* (`:109-119`), label "ADK · Running Agents": adk web · Open UI (2)
- module READMEs, for orientation (label "ADK · <module>"): *1-baseline* (`1-baseline/README.md:76-92`):
  Pick baseline (1); *3-mcp-tools* (`3-mcp-tools/README.md:53-94`): Install Node · Ask agent (2);
  *5-custom-agent*: code panel only, no tracker steps (its scripts need a key and build a second venv;
  exercises.md)

Colab notebooks (label "Colab · <notebook> › <section>", sections = the notebooks' own headings):
- *Cheese Quiz*: Prerequisites (cells 9–13): Copy notebook · Add key · Install · Download (4) · LLM to
  Agent (15–31): Base LLM · Reasoning LLM · Agent (3) · Managing LLM Inputs (33–44): Basic prompt ·
  Prompt engineering · RAG documents · Short-term memory · Long-term memory · Tool outputs ·
  Structured output (7) · Tools, MCP (45–59): Fun-fact tool · Remote MCP · Own MCP (3) · Cheese Quiz
  Guild (60–77): Guild members · Orchestrator · Run guild (3)
- *Travel Planner*: Copy, add key · Install · Define tools · Turn 1 · Turn 2 · Turn 3 · Turn 4 · Chat
  loop (8; cells 1, 10 / 8 / 11–21 / 24 / 25 / 26 / 27 / 28–29)
- *Cheese Newsletter*: Copy, add key · Install · Edit USERS · Define agents · Run demo · View outputs
  (6; cells 1, 10 / 8 / 16 / 18–25 / 27 / 30–31)

Ordering notes (say them in a clause where they occur):
1. The course site orders the tutorials Cheese Quiz → llm-rag → ADK → Travel Planner → Newsletter.
   The video interleaves the Cheese Quiz with the repos by idea (its own section order is kept:
   S02–S03, S12, S13); the tracker always says which notebook section is on screen.
2. `python cli.py --agent --chunk_type char-split` runs three times: on a fresh clone (S05, it fails
   before Gemini: no collection), after the load (S06, it fails at the key), and as the staff's
   recorded run (S06–S07, tagged `recorded`).
3. The fixes that are not in the README are extras: `uv python pin 3.13` (S09), the folder rename and
   the rejected pin (S10), `--port 8080` (S10).

## Scene plan

Each scene names the slides it stands on (`Lecture:`; the GREY `lecture_ref` tag shows that range,
and changes mid-scene where two ranges are given) or "none". Terminals are full width; when a picture
needs the frame, the terminal shrinks to a 3-row strip at the bottom.

The scene list is final (`video.yaml`):

| # | file | class | title |
| --- | --- | --- | --- |
| S01 | `scenes/s01_hook.py` | `Hook` | Who searched your database? |
| S02 | `scenes/s02_steering.py` | `SteeringWheel` | Who holds the steering wheel? |
| S03 | `scenes/s03_envelope.py` | `Envelope` | Everything the model knows is in the envelope |
| S04 | `scenes/s04_menu.py` | `ToolMenu` | A menu of two tools |
| S05 | `scenes/s05_container.py` | `BackInTheContainer` | Back in the container: the agent needs an index |
| S06 | `scenes/s06_call1.py` | `CallOne` | Call 1: the model writes the call |
| S07 | `scenes/s07_call2.py` | `CallTwo` | Call 2: your code ran it, the model answers |
| S08 | `scenes/s08_loop.py` | `TheLoop` | From two calls to a loop |
| S09 | `scenes/s09_adk_setup.py` | `AdkSetup` | ADK: clone, configure, and a sync that fails |
| S10 | `scenes/s10_adk_web.py` | `AdkWeb` | adk web and the folder names |
| S11 | `scenes/s11_state.py` | `SharedState` | Runner, session, state: the shared whiteboard |
| S12 | `scenes/s12_mcp.py` | `McpPlugs` | Tools you didn't write: MCP |
| S13 | `scenes/s13_many.py` | `ManyAgents` | Many agents: who plans the order? |
| S14 | `scenes/s14_approval.py` | `ApprovalGate` | The harness: only a human says yes |
| S15 | `scenes/s15_receipt.py` | `Receipt` | The harness: success is a receipt |
| S16 | `scenes/s16_recap.py` | `Recap` | Tear down, recap, and what's next |

### Part 1 — what an agent is, and function calling by hand

**S01 · Who searched your database? (~260 words).** Lecture: 20–22. Cold open on the staff's recorded
run (tagged `recorded`): the question card `Describe where cheese making is important in ‹instructor›'s
book?` on the left; at the bottom the GREY laptop with the TEAL Chroma container at `localhost:8000`;
far right, in Google's BLUE cloud, Gemini. Two real lines appear between them:
`Function: get_book_by_author` and `Calling function with args: ‹instructor› , cheese making
importance location` (`expected/out-txt-agent-run.txt:65`, `:68`). "Ten passages from exactly one
book, chosen by its author. But Gemini can't see your laptop — `localhost` means nothing in Google's
data centre. So who searched your database, and who decided which book?" (answered in S04–S07). Then
the lecture's reason for agents (20–22), redrawn: a trip request card (five days in Paris, a budget,
replan if it rains or a flight is late); "can an LLM or RAG alone do this?"; two verdicts (an LLM
drafts but can't act; RAG fetches and summarises); three missing pieces as chips — live systems,
tools that act, autonomy. Today's three levels as three bands: **by hand** (llm-rag `--agent`, Docker,
Gemini on Vertex AI), **with a framework** (Google ADK, uv, the Gemini API), **with a harness** (three
Colab notebooks, OpenAI). How to follow along: the tracker top left (llm-rag, ADK or Colab), the GREY
`lecture_ref` top right, code panels with `path · lines`, ▶ your turn, and the tags `recorded`,
`expected`, `illustration`, `extra`, `stand-in`, `no key`, `built, not sent`. You need L05's
collection, Docker, uv, Node.js, an AI Studio key and an OpenAI key with billing. Honest limit, said
once: recorded on 18 October 2026 without Google or OpenAI keys — Docker, Chroma, uv, ADK's web server
and an MCP server ran for real; every model call either stops before it is sent or is refused; model
answers are the teaching staff's saved outputs. "On screen we hide the instructor's name; your
terminal shows it." Every command is in the study guide in MLOps_Learning.

**S02 · Who holds the steering wheel? (~280).** Lecture: 16–18, then 25–27. Tracker *Colab · Cheese
Quiz › Prerequisites*: Copy notebook (File › Save a copy in Drive, illustration); Add key (the Secrets
panel: name `OPENAI_API_KEY`, Notebook access on — illustration; GOLD key; panel `cell-12 · lines 3-4`,
`userdata.get('OPENAI_API_KEY')`); Install (panel `cell-10 · line 3`: unpinned, and `> /dev/null 2>&1`
hides every error — if the next cell's imports fail, rerun it without the redirect); Download
(`c13:5`, `:9`: `quiz-schema.json` 2.10k, `quiz-ui.html` 10.8k). Tracker *LLM to Agent*, V1: the same
question three ways, the same `gpt-4o` each time (`c21:6`, `c25:4`, `c31:4`). Lane 1, `BaseLLM`
(panel `cell-20 · lines 8-17`; `c21:3`, `:30`: one call, `Tokens: 293, Time: 2.81s`). Lane 2,
`ReasoningLLM` (panel `cell-24 · lines 98-119`; `c25:8-29` scrolls eleven `Making single API call...`
lines; tail `Sub-questions explored: 4`, `Total tokens: 701, Time: 39.34s`; one clause: the 701 is an
estimate, line 116 adds 100 per sub-question). Slides 16–18 call this a reasoning engine of many
calls; here **your Python** orders them, so it is a reasoning *workflow*, not a reasoning model
(Conflict 6). Lane 3, `SimpleAgent` (panel `cell-30 · lines 13-16, 30-35`; `c31:7`, the two searches
it chose `:23`, `:28`; tail `Tools used: 1`, `Time: 13.29s` — one clause: that counts tools
*configured*, line 71, not calls). The lecture's definition (26, in our words: an LLM with instructions
and tools that runs on its own until the task is done) and the anatomy grows out of the lanes (27);
dynamic control turns YELLOW — "who decides the next step". Misconception, said plainly: an agent is
not a smarter model; the model was the same in all three lanes; the loop and the tools changed. GOLD:
every lane is paid per call. ▶ your turn: run the cells through the agent.

**S03 · Everything the model knows is in the envelope (~200).** Lecture: 41. Tracker *Colab · Cheese
Quiz › Managing LLM Inputs*, steps 1–7. Cell 35's line: LLMs are stateless functions. V2 with the
seven sheets and the moving top pick (real lines `c38:10` … `c44:10`). Step 4 re-sends the earlier
turns (panel `cell-41 · lines 18-25`): memory is paper you put back in the envelope every time. Slide
41 lists these sheets as parts of the instructions (system and user prompts, contexts, output schema)
and of memory (user sessions, preferences); the next lecture names the craft — context engineering.
Spot-it beat (no timer): panel `cell-39 · lines 16-21` — the system prompt goes in with role `user`,
the question with role `system`. Erratum, kindly: step 2 tests a scrambled conversation; swap the two
roles before comparing; step 3 onward has them right. Bridge: step 6 put a tool's output in the
envelope; "next: how the model asks for a tool in the first place". ▶ your turn.

**S04 · A menu of two tools (~290).** Lecture: 8–14, then 39. V3's first half: L05's strip, the
technique boxes flying into slide 13's column, the column shrinking to llm-rag's two GREEN cards. The
README's own line (`README.md:244`): "let the LLM decide how to retrieve" — agentic RAG with a menu of
two. Panel `agent_tools.py · lines 9-38` (the enum's nine entries, lines 20-28, shown once and then
folded; line 28 masked): the name the model will write; the description, the only documentation
the model ever sees (line 33 even coaches it: "Expand the search term to a a sentence or two" — typo
in the source); the parameters as JSON schema; the `enum`, so the model can only pick a listed author;
`required`. Panel `· lines 41-49`: the real function — `collection` and `embed_func` are not in the
schema: your code injects them; the model controls only `author` and `search_content`. Panel `· lines
79-81`: one `Tool` holds both declarations. Slide 39: the agent must pick the right tool, format its
inputs, interpret its outputs — here the model picks and formats by *writing*; your code runs. The
eleven books (the `Processing file` lines of `cli-container/20`: 9, 23, …, 142, titles only) beside
the nine enum names. PONDER 1 (8 s): "Nine names in the enum, eleven books in the collection. Which
books can the agent never reach by author — and is it for the same reason?" Answer with extra
`cli-container/34` (lines 15, 26-28): *Cottage Cheese Recipe Book*, 178 chunks — its author is simply
not in the list; the *Woman's Institute* book, 1,505 chunks — it has no author at all (L05's erratum:
the file name was cut at its first dot). Both stay reachable through the search across all books. V3's
stage closes the scene: "the model never gets your database; it gets a menu".

**S05 · Back in the container: the agent needs an index (~250).** Lecture: none. "L05 ended on one command; today we run it."
Tracker *llm-rag · Prerequisites* only for a fresh start (`laptop/01`). *Run Container*: ▶ `cd
llm-rag` (`03`); ▶ set `GCP_PROJECT` (`05:10-11`, the placeholder diff — "type your own Project ID");
▶ `sh docker-shell.sh` (`06`, trimmed 1-5, 6-9, 10-11, `…`, 32-41): Chroma first, the harmless pull
message (its wording depends on your Docker setup; Compose then builds), `Building 40.5s`, the banner,
`app@abcf218747d0:/app$`. Extra `docker ps` (`07`): the CLI container's run name and
`llm-rag-chromadb` on `0.0.0.0:8000->8000/tcp` — "remember port 8000 for part 2". Tracker *Agents*
step 1: ▶ `python cli.py --agent --chunk_type char-split` on a fresh clone (`cli-container/10`: 1-3,
9-10, 25): `NotFoundError: Collection [char-split-collection] does not exist`, from line 429, before
any call to Gemini (panel `cli.py · lines 425-429`). The agent stands on L05's index. If you kept L05's
database, it is still in `docker-volumes/chromadb` and you skip ahead (if you loaded before 22
September, reload: the book changed — S07). Without it: L05's chunk → embed → load. We have no key, so
as in L05 the staff's committed embeddings stand in for `--embed` (card from `laptop/08`: commit
`68e0bde`, 11 files, 31 MB, tagged `recorded`). Tracker *Load (L05)*: ▶ `python cli.py --load
--chunk_type char-split` (`20`: 1-8, `…`, 142, 153): 8,248 chunks in eleven books, 24 of them the
instructor's story. Extra `python cli.py --get --chunk_type char-split` (`21:6`, ids only): the
collection answers. ▶ your turn.

**S06 · Call 1: the model writes the call (~280).** Lecture: 10–13, then 35. Mini-map: the tools block
lit. Panel `cli.py · lines 432-453` (line 435 masked): the user turn; `generate_content` with
`temperature=0` (slide 35: sampling is a design choice — here, the same tool choice every run), the
menu as `tools=`, and `tool_config` with `mode="any"`. Extra `cli-container/32`: the lower-case string
becomes `FunctionCallingConfigMode.ANY` — the model must answer with a function call. Conflict 2,
kindly: in the lecture a good agent may decide not to search at all (Self RAG's first box, slide 10;
the assistant that answered a stable question without searching, slide 33); ours can't — the
"Retrieval Decision" card is crossed out: it chooses *which* search, never *whether* (exercise: delete
`tool_config` and greet it). V2: the envelope opens on the real request, extra `cli-container/31`
(tagged `built, not sent`; the script collapsed to its first line + "prints the request instead of
sending it"): line 20 (`POST …/projects/your-project-id/locations/global/…/gemini-3.1-flash-lite:generateContent`),
22-31 (contents: the user turn), 34-41 and 51-53 folded (the two `functionDeclarations`, the enum),
86-93 (`"mode": "ANY"`, `"temperature": 0.0`), 95 (`-- stopped here: nothing was sent to Vertex AI
--`). One clause: no `systemInstruction` — L05's unsent instruction is missing here too. Tracker
*Agents* step 1 again: ▶ `python cli.py --agent --chunk_type char-split` (`30`, tagged `no key`: 1-3,
8-10, 16-17, `…`, 71): the lookup passed; the first model call needs your key —
`DefaultCredentialsError: File /secrets/llm-service-account.json was not found.` With your key you see
`LLM Response:` next. What it looked like for the staff (`expected/out-txt-agent-run.txt`, tagged
`recorded`: 15, 17-28, 34; line 29's `thought_signature` shown as `b'\x01\x8f=k_…'`): the model's whole
answer is a function call — name `get_book_by_author`, `author` = `‹instructor›`, `search_content`
`'cheese making importance location'` (four words, though the description asked for a sentence or
two), an id, a thought signature. V3: the speech bubble becomes the BLUE card. One clause on
`automatic_function_calling_history=[]` (`:52`): the SDK ran nothing; it can't, it only has
declarations. "Gemini wrote arguments. Nothing has run yet." GOLD: one Gemini call. ▶ your turn (with
your key).

**S07 · Call 2: your code ran it, the model answers (~300).** Lecture: 39. Panel `cli.py · lines
456-460` (pick out the function calls, hand them to the dispatcher) and `agent_tools.py · lines
84-110` (match the name, print, call the real function, wrap the result with
`Part.from_function_response(name=…, response={"content": …})`). Extra `cli-container/33`, tagged
`stand-in` and said: "the model's call from the staff's run, through the tutorial's own dispatcher,
against *our* collection; Google would turn the search text into a vector, we can't, so a stored
chunk's vector stands in — which ten chunks come back is not what the real query returns" (lines 36,
37-45, 48 masked, 51-57 — Mara, Anja, the next step — `…`, 135: `function_responses: 1 part,
name='get_book_by_author', response keys=['content'], 3509 characters`). V3: ten GREEN cards, one
string, a TEAL `{"content": …}` card stapled to the call. Panel `cli.py · lines 464-477`: call 2 sends
three things — the question, **the model's own turn unchanged** (line 469), your responses — and
`tools` again with no `tool_config`: the mode is back to automatic. V2's second envelope from `33`
(tagged `built, not sent`): 137, 139-147, 148-163 (the `thoughtSignature` seal, the `functionCall`),
164-175 (the `functionResponse`, content folded), `…`, 231 (`"generationConfig": {}`), 233. Gemini's
thinking models sign their turn, and the API wants it back exactly as sent: re-sending the model's
turn verbatim keeps the seal on (digest Excerpt 4). The staff's answer (`expected/…` 99, 105, 111-112,
tagged `recorded`, masked; tokens 247 and 1,269 at `:50`, `:136`): the Soča Valley, transhumance… The
twist (extras `laptop/09:1-6`, `laptop/10:2-5`): those words appear in `out.txt` and in the book
*before* commit `85bba32`, and **zero times** in today's book — the run was recorded against an index
built from the old text. Your run, on today's book, draws on chunks like the ones above: Mara, the
curd, the wheels. An index answers from what was loaded (L05). Erratum, kindly: the README says it
"Displays the LLM's response" (`readme-agents-this-will.txt:7`); `cli.py:478` prints the whole
response object — `print(response.text)` shows just the answer. Tracker *Agents* step 2: the hosted
Cheese Agent Tool (`README.md:268`; browser, illustration; extra `laptop/11`: `200 text/html`; "use
Chrome"). Answer to the hook: Gemini wrote the call; your Python searched your database. GOLD: two
Gemini calls per question.

**S08 · From two calls to a loop (~270).** Lecture: 26, then 35–41. Mini-map: dynamic control lit.
V4's hub (35–40). The lecture's agent runs until the task is done; llm-rag's ran one lap: a forced
call, then an answer. Conflict 1, kindly: "the README calls it an agent; by the lecture's definition
it's the smallest piece of one". PONDER 2 (8 s): "Call 2 hands the model the tools again but no
`tool_config`. Suppose Gemini answers with *another* function call. What does `cli.py` do?" Answer:
line 478 prints a response whose only part is a function call, with no text, and the program ends;
nothing runs it. A loop would run it and ask again. V4's track: the stop rule (a reply with no
function call is a final response) and the cap. In code the caller sees it from outside: panel
`4-production-ready/app/runner.py · lines 39-48` (ADK's Runner streams events; this wrapper keeps the
one where `event.is_final_response()`); the loop inside the library is drawn, not quoted (caption
"inside ADK, simplified: repeat model → tools until the reply is final"). The caps: panel Cheese Quiz
`cell-71 · lines 5-7` (`max_turns=12`) and Newsletter `cell-25 · line 8` (`"max_iterations": 16`) —
the RED gate. Slide 41 greys out dynamic control: you configure the model, the instructions, the tools,
the memory; the loop is the block the framework writes (PURPLE). Part 1 teardown, all extras: ▶ `exit`
(`laptop/06:41-42`); `docker ps` (`12`): the CLI container is gone (`--rm`) but `llm-rag-chromadb` is
still up on port 8000; `docker compose down` (`13`, the two WARN lines are harmless). "Part 2's web
server wants port 8000 too." Close part 1: "in part 2, a framework runs this loop for us". Clean
frame.

### Part 2 — frameworks own the loop

**S09 · ADK: clone, configure, and a sync that fails (~360).** Lecture: none. A new picture: the GREY
laptop with no Docker, PURPLE uv, and a BLUE Gemini API reached with an AI Studio key (GOLD).
Tracker *ADK · Getting Started*: ▶ `git clone https://github.com/dlops-io/llm-agent-google-adk.git`
(`adk-laptop/01`; the README writes `<repository-url>`). ▶ `cd google-adk-tutorial` (`02`: `No such
file or directory`) — erratum, kindly: the folder is named after the repo — ▶ `cd
llm-agent-google-adk` (`03`). Extra `ls -a` (`04`): six module folders, `pyproject.toml`, and no
`uv.lock` — the repo ignores it (`.gitignore:34`), so every student resolves versions fresh (unlike
llm-rag). ▶ `cp .env.example .env` (`05`); extra (`06`): the placeholder key and
`GEMINI_MODEL=gemini-2.5-flash`. Add API key / AI Studio key: Create API key (illustration, GOLD key
glyph) → paste it into `GOOGLE_API_KEY` in this root `.env` (git-ignored). The model line is the
lecture's first design decision (slide 35) in one line: set a current model, e.g.
`gemini-3.1-flash-lite`, the one llm-rag uses — Google lists `gemini-2.0-flash` (the code's fallback
when the line is missing, `1-baseline/agent.py:12`) as shut down and limits `gemini-2.5-flash` to
earlier users (digest G2, checked 18 October). Keep everything in the root `.env`: don't copy a
module's `.env.example` — ADK reads only the nearest `.env` (S10 shows which one it loaded). Panel
`pyproject.toml · lines 8-20`: `requires-python = ">=3.10"`, `google-adk>=1.8.0` with no upper bound,
and `chromadb` plus `sentence-transformers` (they pull in PyTorch). PONDER 3 (6 s): "This laptop has
no Python at all (`00:9`). The project asks for 3.10 or newer. Which Python will `uv sync` use?"
(L01). ▶ `uv sync` (`07`, all of it): `Using CPython 3.15.0` — the newest, at the time of recording —
`Resolved 189 packages`, then the RED error and hint: `onnxruntime` 1.31.0 has wheels only up to
`cp314`. V5. Erratum, kindly: the README's step 4 fails on a fresh machine today; a laptop where uv
finds a Python 3.10–3.14 first may get through (reasoned from L01's capture, not captured here), but
pin anyway so every laptop builds the same environment. The fix, not in the README: extra ▶ `uv python
pin 3.13` (`09`), then ▶ `uv sync` again (`12`, trimmed: 1-4, 6-7, `…`, 38 `google-adk==2.12.0`, 89
`onnxruntime==1.31.0`, `…`, 156; never line 5 or 140). Said: PyTorch makes this big — about 1.6 GB
(`14:12`), and on a Linux PC about 3 GB more of CUDA packages (`10`); a Mac gets none. Extra `uv run
adk --version` (`13`): `adk, version 2.12.0`, at the time of recording. ▶ your turn.

**S10 · adk web and the folder names (~300).** Lecture: none. Tracker *ADK · Running Agents*: ▶ `uv
run adk web` from the repository root (`15`): first a question (lines 1-13) — kindly: the text says
telemetry is off by default, but `[Y/n]` means Enter answers yes; answer as you like (`adk telemetry
disable` changes it later); then the banner (34-41: `Uvicorn running on http://127.0.0.1:8000`). Open
UI (`README.md:119`): a browser (illustration) at `localhost:8000` lands on `/dev-ui/` (extra `16`).
The agent dropdown, drawn with the real list (extra `17`): seven entries. Pick `1-baseline` → RED
(extra `18`: `Invalid agent name: '1-baseline'. Agent names must be valid Python identifiers…`; the
server log `15:44`). Why, as a picture: `adk web` imports `<folder>.agent` and reads `root_agent`, and
a Python module name can't start with a digit or contain a hyphen — `import 1-baseline.agent` is a
syntax error; newer ADK checks the name first. One beat on what doesn't work (extras `21:1`, `:7-8`;
`25`; `24:131-132`): an older ADK (1.27.5) lists the folder but still refuses it as an app name; undo
(`27`). The fix, not in the README: extra ▶ `mv 1-baseline baseline; mv 3-mcp-tools mcp_tools; mv
5-custom-agent custom_agent; ls` (`28`), ▶ `uv run adk web` again (`29`, lines 36-40: `Loaded .env file
for baseline at …/llm-agent-google-adk/.env` — the root `.env`; `Found root_agent in baseline.agent`;
`build_graph … 200 OK`), extra `30`: `baseline`, `custom_agent`, `mcp_tools`. Git now sees deleted and
new folders (`39`): fine for your copy. One clause each: QUICKSTART's `uv run adk web
1-baseline/agent.py` → `Directory '1-baseline/agent.py' is a file.` (`19`: `adk web` takes a folder);
the module READMEs' `uv run adk` without `web` only prints help (`20`). If llm-rag's Chroma still holds
port 8000: extra `36` (line 21, RED `[Errno 98] … address already in use`, exit 3) → `uv run adk web
--port 8080` (`37:34`), or `docker compose down` as in S08. ▶ your turn.

**S11 · Runner, session, state: the shared whiteboard (~270).** Lecture: 40–41 (and 20–22). Tracker
*ADK · 1-baseline*: Pick baseline. Panels `1-baseline/agent.py · lines 14-26` and `· lines 28-39`
("your copy is now `baseline/agent.py`"). Mini-map labels the constructor with slide 41's blocks:
`model=` → LLM core; `instruction=` → instructions; `tools=` → none here; `output_key` → memory, within
one session; the Runner → dynamic control (PURPLE). Extra `adk-laptop/31`: the tree the UI loads —
`TravelPlannerPipeline` over `ItineraryValidator`, `TravelPlanner`, `TripSummarizer`, their output keys
and `model gemini-2.5-flash` (from the root `.env`: set yours, S09). Extra `32`: a new session,
`"state":{}`, `"events":[]`. V6. Conflict 5, kindly: the lecture's planner calls live systems; this
pipeline has no tools at all, so its prices are the model's guesses (the harness notebook, S14, fixes
exactly that). Conflict 3, kindly: the README calls this "Memory" (`README.md:140`); ADK's code calls
it session state; the lecture's memory lasts across sessions, and none of today's runs keeps that kind.
Without a key: a trip request sent (extra `33`: `Internal Server Error`; the reason in `29:357-358`,
RED `400 INVALID_ARGUMENT … API key not valid`) — the placeholder reached Google and was refused. What
to look for with your key (a caption, not output): three replies in order; the State tab gains
`itinerary_validation`, `travel_plan`, `trip_summary`. The session is a file in the agent's folder
(`29:41-42`, `baseline/.adk/session.db`). GOLD: three Gemini calls per request. ▶ your turn.

**S12 · Tools you didn't write: MCP (~280).** Lecture: 51–53. V7 opens with slide 51's three families
and the tutorial's tools sorted into them; then 52 ("Do you see a problem?", a 5-second beat, not a
ponder) → 53, the trunk labelled "same protocol"; Conflict 4, kindly: "the lecture's MCP box is the
shared protocol, not a program you run — in code each server is its own plug". Plug 1, tracker *ADK ·
3-mcp-tools*: Install Node (`3-mcp-tools/README.md:53-64`; extra `34`: `v24.22.0`, `11.19.1`). Panel
`3-mcp-tools/agent.py · lines 20-29`: ADK starts `npx -y @modelcontextprotocol/server-filesystem
<folder>` as a child process and talks over its stdin and stdout; `tool_filter` lets three tools
through. Extra `35` (no model involved; the script collapsed; the `UserWarning` and `npm notice` lines
cut): 21 (`Secure MCP Filesystem Server running on stdio`), 30 (`tools the agent sees: ['list_directory',
'read_file', 'search_files']`), 31 folded (`tools the server offers: 14 […]`: `write_file`,
`edit_file` … filtered out), 32-37 (`list_directory`: four files and `__pycache__`). Ask agent (`:88-92`):
with your key, ask "List files in this directory" and look for a `list_directory` call in the events.
Plug 2, tracker *Colab · Cheese Quiz › Tools, MCP*: panel `cell-54 · lines 2-27` folded to 2, 10-18,
26-27 (`MCPServerStreamableHttp(params={"url": …})`, passed as `mcp_servers=`, not `tools=`; URL
masked). Extras `mcp-remote/01` (lines 2, 10: `HTTP/2 406`, "Client must accept text/event-stream" —
what a browser gets: the server is up, it speaks MCP, not web pages), `02` (`initialize`: protocol
`2025-06-18`, server version 1.16.0), `03` (`tools/list`: one tool), `04` (`tools/call`: a fact; it
changes every run). Plug 3: panel `cell-57 · lines 2-9, 14`: your own FastMCP server in a thread on
`127.0.0.1:8001`; erratum, kindly: the comment above it says port 8000 (line 11), and so does the saved
output of an older version (`c57`). Recorded `c59:3-10`: `"POST /mcp HTTP/1.1" 200 OK` interleaved with
`‹instructor› Fun Fact Tool Called`. Misconception, said plainly: MCP doesn't give the model network
access — your client process connects; the model still only writes calls. GOLD: OpenAI calls in the
notebook. ▶ your turn.

**S13 · Many agents: who plans the order? (~240).** Lecture: 44–49 (and 38). The lecture's research
example as a GREY dashed tree (lead agent → planner → parallel web searchers → synthesis → report),
next to the tutorial's two trees: the Cheese Quiz Guild and the Newsletter. Slide 38's planner asks
the question that sorts them: **who plans the order?** Three diagrams morph. (1) Code:
`SequentialAgent` (`1-baseline/agent.py · lines 35-39`, recap) — an assembly line. (2) The model:
tracker *Colab · Cheese Quiz › Cheese Quiz Guild*; panel `cell-68 · lines 1-8` (`.as_tool(...)`: a
whole agent becomes one tool — the orchestration family), `cell-70 · lines 3-11` (the orchestrator's
instructions: "Follow the assembly line strictly", "at most 2 total review rounds" — a rule in prose
that no code enforces), `cell-71 · lines 5-7` (`max_turns=12`). Recorded `c75:2-5`: three `ERROR:openai.agents:Error
getting response` lines — and then a quiz anyway (`:7-12`): the orchestrator worked around failed
calls; every hop adds cost, time and a way to fail. (3) Python reading the model's label: panel
`5-custom-agent/conditional_agent.py · lines 84-102` (a custom agent: a classifier writes
`query_complexity` through `output_key`, plain `if` statements route). PONDER 4 (6 s): "The classifier
answers `Simple`, with a capital S. Which handler runs?" Answer: the `else` branch — clarification;
the comparison is exact; fix with `.strip().lower()` or a structured output (exercises). One clause:
slide 51 also lists handoffs; these tutorials use agents as tools; L07 shows the other pattern.

**S14 · The harness: only a human says yes (~260).** Lecture: 20–22, then 36–37. Tracker *Colab ·
Travel Planner*: Copy, add key; Install (panel `cell-08`: this notebook pins `openai-agents==0.3.2`);
Define tools. Slide 20's Paris trip shrinks to the notebook's mock catalog — three cities, six hotels,
prices in cents (`cell-12`), five search tools and a finalize tool (`cell-14`, `cell-21`); it books
nothing (`c27:9`, Conflict 5). Recorded turns, compact: Turn 1 (`c24:3-4`: `Kind: clarification` —
San Francisco or Los Angeles?), Turn 2 (`c25:3`, the five `[tool]` lines counted, `Kind: options`),
Turn 3 (`c26:3-19`: `[tool] finalize_plan…`, `Kind: clarification`, the exact JSON proposal). V8's
turnstile with panels `cell-15 · lines 33-42` (the gate: a model's call can only *propose*) and
`cell-18 · lines 55-65` (`apply_confirmation`: only the human's next message, a literal yes, approves).
PONDER 5 (8 s): "In turn 3 the model got `needs_confirmation`. Why can't it just call
`finalize_itinerary` again to approve its own plan?" Answer: approval comes only from
`apply_confirmation`, which runs on the human's text *before* the agent; inside turn 3 nothing has
been approved. Turn 4, "yes" (`c27:3-5`, `:25-34`): `Kind: itinerary`, a budget report "computed by
Python"; V8's calculator, 2,690 of 6,000; the notebook's own test asserts Python's number (`cell-27 ·
line 6`). What the user sees is rendered from checked state (panel `cell-18 · lines 122-135`: an
unchecked itinerary raises; money in the model's prose only warns — a hard and a soft guardrail).
Conflict 7: the lecture puts success criteria and guardrails in the instructions (36–37); this
notebook keeps a copy in code the model can't talk its way past — and the gate sits on the action
tool (slide 51). GOLD: OpenAI calls per turn. ▶ your turn.

**S15 · The harness: success is a receipt (~200).** Lecture: 36–37 (and 10–12). Tracker *Colab ·
Cheese Newsletter*: Copy, add key; Install (`c08`, pinned framework); Edit USERS (panel
`cell-16.redacted · lines 6-12`: replace the readers with yourself and a friend; keep two — cell 31
shows the second; e-mail is preview-only); Define agents (panel `cell-25 · lines 5-16, 25`: model
`gpt-5.6-luna`, `max_iterations` 16, three tools — `researcher_agent`, `editor_agent`, `send_email` —
one call at a time); Run demo. Recorded `c27:3-11` (the first reader's city: the editor runs four
times — the validator's errors come back as tool results — then `send_email`, `Saved HTML: … No email
sent.`), `:30` (`Created 4 mock emails…` — the saved run had four readers; today's list makes two).
V8's receipt slot with panel `cell-18 · lines 117-125`: no receipt → error; a receipt whose file is
missing → error; the model's reply appears only inside the error message. A note vs a check (E15):
panel `cell-22 · line 16` ("no … embedded URLs") vs the saved preview `c30:26` (trimmed to
`…Promotion URL: https://…`): nothing checks for URLs, so one slipped through. The lecture's Self RAG
and Corrective RAG (10–12) check retrieval for the same reason: don't trust, check (our link). Bridge:
the next lecture calls this the **harness**. GOLD: web search is billed per call. ▶ your turn.

**S16 · Tear down, recap, and what's next (~210).** Lecture: 41 (and 32–33). Teardown: Ctrl+C in `adk
web` (`15:46-56`, `ADK Web Server shutting down...`); extra `git status` (`39`): the renamed folders,
`.python-version`; `.env`, `.venv/` and `uv.lock` are ignored — the sessions in `baseline/.adk/` are
not covered by the repo's `.gitignore`, so don't commit them; `.venv` is 1.6 GB, delete the folder when
you're done. Colab: Runtime › Disconnect and delete runtime, in each notebook (illustration). Three GOLD
keys: the service-account key stays in `secrets/` beside `llm-rag`; delete the AI Studio key and the
OpenAI key (or cap their spending) when the course ends. (llm-rag was shut down in S08.) Recap: V1's
anatomy filled with the tutorial's objects — LLM core: `gemini-3.1-flash-lite`, `gpt-4o`,
`gpt-5.6-luna`; instructions: `instruction=`, `instructions=`, the system prompt, `output_type`; tools:
`FunctionDeclaration`, `@function_tool`, `@tool`, `MCPToolset`, `.as_tool`; memory: the message
history, session state (within one session); dynamic control: ADK's Runner, `Runner.run` with
`max_turns`, `max_iterations` — and llm-rag's two hand-written calls. The lecture's formula (32–33),
LLM + reasoning + instructions + tools, gets the tutorial's two additions: a loop the framework runs,
and checks your code enforces. Recap questions (5, on screen one at a time, answers in exercises.md):
(1) in function calling, who runs the function, and what travels back to the model in call 2? (2) what
does `mode="any"` change, and why only on call 1? (3) what ends an agent loop, what cap do frameworks
add, and which lecture block is that? (4) how does `TripSummarizer` get the travel plan without a
message from `TravelPlanner`? (5) in the last two notebooks, what decides that a run succeeded, and
why not the model's final text? Next: L07, Agents II — the harness becomes the topic. Study guide and
exercises in MLOps_Learning. Clean frame.

## Ponder questions (summary)

| # | scene | question | answer (said right after the timer) |
| --- | --- | --- | --- |
| 1 | S04 | nine enum names, eleven books: which books can the agent never reach by author, and is it for the same reason? | *Cottage Cheese Recipe Book* (178 chunks: its author isn't listed) and the *Woman's Institute* book (1,505 chunks: no author at all, L05's dot erratum); both reachable by the all-books search (`cli-container/34`) |
| 2 | S08 | call 2 passes `tools` but no `tool_config`; if Gemini asks for another tool, what does `cli.py` do? | prints a response whose only part is a function call and ends; nothing runs it (`cli.py:478`; `33:231`); a loop would run it and ask again |
| 3 | S09 | no Python on the laptop, `requires-python >=3.10`: which Python will `uv sync` use? | the newest it can download, CPython 3.15.0 at the time of recording (`07:2`) — and `onnxruntime` has no wheel for it |
| 4 | S13 | the classifier answers `Simple` (capital S): which handler runs? | the `else` branch, clarification: the comparison is exact (`conditional_agent.py:89-102`) |
| 5 | S14 | in turn 3 the model got `needs_confirmation`: why can't it call `finalize_itinerary` again to approve its own plan? | approval comes only from `apply_confirmation`, which runs on the human's next message before the agent (cell 18:55-65; cell 15:33-42) |

## Errata to state (kindly, with the fix)

1. **`cd google-adk-tutorial`** (ADK `README.md:78`; real `adk-laptop/02`) → `cd llm-agent-google-adk` (S09).
2. **The ADK `uv sync` fails on a fresh laptop** (`README.md:100`; real `07`): uv takes CPython 3.15.0,
   `onnxruntime` has no `cp315` wheel; the repo has no lockfile (`.gitignore:34`) → `uv python pin 3.13`,
   then `uv sync` (S09).
3. **The module folders' names** (`1-baseline`, `3-mcp-tools`, `5-custom-agent`) are not Python
   identifiers, so today's ADK refuses them in `adk web` (real `18`); pinning ADK below 1.28 does not
   help (real `24`, `26`) → rename the folders (`28`–`31`) (S10).
4. **Retired model defaults**: the code falls back to `gemini-2.0-flash` (`1-baseline/agent.py:12`, and
   seven more places), `.env.example:21` says `gemini-2.5-flash` → set `GEMINI_MODEL` to a current model
   (`gemini-3.1-flash-lite`) in the root `.env`, and don't copy module `.env.example` files (S09).
5. **ADK 2.12's telemetry question**: not in the README; Enter means yes although the text says "off
   by default" → answer deliberately; `adk telemetry disable` (S10).
6. **QUICKSTART and module READMEs**: `uv run adk web 1-baseline/agent.py` (real `19`) and `uv run adk`
   without `web` (real `20`) → `uv run adk web` from the root, pick in the UI (S10, one clause each).
7. **"Memory" in the ADK README** (`README.md:140`) is per-session state; ADK's memory is a separate,
   cross-session service (S11).
8. **llm-rag's Agents section doesn't say it needs L05's collection** (real `cli-container/10`) → load
   it first (S05).
9. **"Displays the LLM's response"** (`README.md:266`) — `cli.py:478` prints the whole response object
   → `print(response.text)` (S07).
10. **`out.txt` and the README's flow picture come from the old book** (real `laptop/09`, `10`) → your
    answer will be about today's story; an index is a snapshot (S07).
11. **No system instruction in the agent's calls either** (`cli.py:40-58`; real `31`: no
    `systemInstruction`) — L05's erratum, one clause (S06).
12. **Cheese Quiz step 2 swaps the roles** (cell 39 lines 19-20) → swap them back (S03).
13. **"Tools used: 1" and "Total tokens: 701"** (cells 30:71, 24:116) count configured tools and an
    estimate (S02, one clause).
14. **Cheese Quiz cell 57 says port 8000; the code uses 8001** (line 11 vs 14; saved output `c57`) (S12).
15. **The Newsletter's "no embedded URLs" rule is never checked** (cell 22:16 vs `c30:26`) → a rule that
    matters belongs in `validate_newsletter` (S15).
16. **Cheese Quiz cell 10 installs unpinned packages and hides the output** → rerun without the
    redirect if imports fail; pin what worked (S02, one clause).
17. **ADK saves sessions in `<agent>/.adk/`, which `.gitignore` doesn't cover** (real `29:41-42`, `39`)
    → don't commit them; add `.adk/` to your ignore file (S16).

Slides vs captures (not tutorial errata; said kindly where they occur): `--agent` is one lap (S08), it
always retrieves (S06), "memory" (S11), one connection per MCP server (S12), the travel planner is a
rehearsal (S11, S14), two kinds of "reasoning" (S02), checks live in code (S14, S15).

## Costs and teardown

- **Paid per call, nothing left running in a cloud:** llm-rag's `--agent` makes two Gemini calls on
  Vertex AI (the staff's run: 247 + 1,269 tokens, `expected/…:50`, `:136`) — negligible; embeddings only
  if you rebuild the collection (L05). ADK's pipeline makes three Gemini API calls per request; the free
  tier may cover the exercises (check your quota page). The notebooks use OpenAI: dozens of calls for the
  Cheese Quiz, hosted web search billed per call (Cheese Quiz agent, Guild, Newsletter researcher) —
  the digest's estimate is cents to a few dollars for everything; the narration says "check the current
  price list". GOLD tags in S02, S06, S07, S11, S12, S14, S15. Nothing was billed in the recording: there
  were no keys.
- **Three keys** (S16): the service-account key (L05) beside the repo, never in it; the AI Studio key in
  the git-ignored root `.env`; the OpenAI key only in Colab's Secrets panel, never pasted into a cell.
  Delete or cap them when the course ends.
- **Local teardown:** llm-rag in S08 (`exit` leaves Chroma on port 8000; `docker compose down` stops it,
  the index stays in `docker-volumes/`). ADK in S16 (Ctrl+C; `.venv` 1.6 GB; `.adk/` sessions; the renamed
  folders). Colab: delete each runtime.
- **Optional, not in the video:** ADK's `6-rag/1-vertex-rag-engine` creates a billable Vertex AI RAG
  corpus — exercises.md says how to delete it.

## README commands checklist (for the follow-along review)

| README command | where | scene (capture) |
| --- | --- | --- |
| llm-rag: repo link → `git clone https://github.com/dlops-io/llm-rag.git` (L05) | `README.md:48` | S05 (`laptop/01`, fresh start only) |
| "inside the `llm-rag` folder" → `cd llm-rag` (L05) | `:79` | S05 (`laptop/03`) |
| update `GCP_PROJECT` in `docker-shell.sh` (L05) | `:80` | S05 (`laptop/05`) |
| `sh docker-shell.sh` (L05) | `:84` | S05 (`laptop/06`) |
| `python cli.py --load --chunk_type char-split` (L05) | `:151` | S05 (`cli-container/20`) |
| `python cli.py --agent --chunk_type char-split` | `:258` | S05 (`10`), S06 (`30`, no key; `expected/out-txt-agent-run.txt`) |
| Cheese Agent Tool (link) | `:268` | S07 (illustration; `laptop/11`) |
| ADK: `git clone <repository-url>` | `README.md:77` | S09 (`adk-laptop/01`, URL filled in) |
| `cd google-adk-tutorial` | `:78` | S09 (`02`, fails; `03` with the real name) |
| `cp .env.example .env` | `:84` | S09 (`05`; `06`) |
| "Edit .env and add your GOOGLE_API_KEY" | `:85` | S09 (illustration; placeholder `06`) |
| Google AI Studio → Create API key | `:90-94` | S09 (illustration) |
| `uv sync` (from the repository root) | `:100` | S09 (`07` fails; `12` after the pin) |
| `uv run adk web` | `:116` | S10 (`15`; `29` after the rename) |
| open http://localhost:8000, select an agent | `:119` | S10 (illustration; `16`, `17`, `18`, `30`) |
| module 1: select `1-baseline` in the UI | `1-baseline/README.md:76-92` | S11 (`31`, `32`, `33`) |
| module 3: install Node.js; ask "List files in this directory" | `3-mcp-tools/README.md:53-64`, `:88-92` | S12 (`34`; `35`; caption) |

## Things never to do on screen

Series rules:
- No slide images, no PDF pages, no README figures (`images/llm-rag-flow-3.png`, `demo.gif`): redraw the
  idea and cite the slide with `lecture_ref`. No screenshots of the chat product on slides 28–33 and
  42–49; if a chat is needed, a generic chat mock-up tagged `illustration`.
- No Google, GCP, Colab, OpenAI, Microsoft or Node logos and no screenshots of AI Studio, Colab, the ADK
  dev UI or `ac215-llm-rag.dlops.io`: schematic drawings tagged `illustration`, filled with captured data
  only (`adk-laptop/17`, `30`, `31`, `32`, the error texts).
- No real person's name in captions, labels or narration, and the instructor's name nowhere on screen
  (the `‹instructor›` mask, Running example). The prompt user is `student`; the Newsletter's readers are
  `<reader1>`…; public-domain authors only inside the enum panels and the per-author table.
- No hand-typed output: every terminal and notebook line comes from `assets/terminal/`; `expected/`
  README text is shown as README text, never styled as output; "what to look for" is a caption.
- No command spelled differently from the README. Substitutions are said: the clone URL for
  `<repository-url>`, the real folder name after the failed `cd`, the placeholder project id.
- No credentials or real-looking ids: `your-project-id`, `your_google_ai_api_key_here`, the Secrets
  panel's name; never a key's content. `ac215-project` only inside the diff line the viewer edits.

Lecture-specific:
- Never say Gemini "queried your database" or "ran the function": the model writes the call, your code
  makes it.
- Never call llm-rag's `--agent` an agent loop.
- Never present a model call as having succeeded on our machine: no invented `LLM Response:`, answers,
  ADK events, State-tab values, MCP replies from a model, or notebook outputs. The staff's `out.txt` and
  the notebooks' saved outputs are always tagged `recorded`; `out.txt` is always said to come from the old
  book.
- Never present `cli-container/31` or `33` as sent: they carry `built, not sent`; never present `33`'s
  ten chunks as what the real query returns: `stand-in`, said aloud.
- Never present the `google-adk<1.28` pin as a fix (it is shown once as tried and refused), and never
  show the symlink attempts.
- Never show the capture's plumbing: the capture-only uv config (`adk-laptop/11`), `Resolved 171
  packages` or `torch==2.14.1+cpu` (`12:5`, `:140`), the Docker-in-Docker laptop, `proxy_relay.py`,
  `~/.npmrc`, CA variables, the rebuilt base image, `docker exec`, the `/tmp/mcp-headers` plumbing of
  the curl lines (collapse them).
- Never present module 2 (`2-litellm`) as working, or module 4/6 as run: code panels only.
- Never state prices as verified; never claim a step was billed.
- Never show the notebook's original reader list (the course staff's names and addresses): only
  `cell-16.redacted.py`, and never a Colab cell copied from anywhere but `assets/source/colab/`.

## Left for exercises.md (not in the video)

The digest's Exercises 1–8 (steer the tool choice by editing the question at `cli.py:435`; delete
`tool_config` and greet the agent; the folder-name error and its fix — now the rename, not the pin; the
port that won't let go; the `Simple` router and a structured-output fix; why a receipt; make `2-litellm`
use LiteLLM with a provider-prefixed model; turn llm-rag's two calls into a capped loop). Also: run
`4-production-ready` with `uvicorn` and `curl /chat`; `5-custom-agent`'s two scripts from the root venv
(`uv run --project ..`); the Travel Planner's interactive chat (fresh session each time, in-memory
`SQLiteSession`); the Guild's unused `mozzarella_tool` and the `fact_cache` it can't write; ADK's
`ParallelAgent` and `LoopAgent` from the module READMEs; `6-rag/2-custom-chromadb-rag` (its v1
heartbeat and its own port 8000); deleting the Vertex AI RAG corpus of `6-rag/1-vertex-rag-engine`;
adding `.adk/` to `.gitignore`; MCP's `read_file` vs `read_text_file`; telemetry on and off.
