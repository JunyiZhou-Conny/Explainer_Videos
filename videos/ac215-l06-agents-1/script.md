# AC215 · Lecture 6 — LLM: Agents I (follow-along: llm-rag Agents, llm-agent-google-adk, three Colab notebooks) — narration script & visual plan (v1)

Audience: an AC215 student who has done L1–L5: uv, `pyproject.toml` and `uv.lock` (L1); containers,
`docker-shell.sh` and a mounted service-account key (L2–L4); L05's RAG pipeline in `llm-rag` (chunk →
embed → load into `char-split-collection`, query, chat). They read Python comfortably (`async`/`await` at
a reading level) and have used a chat assistant, but have never written a tool for an LLM, used an agent
framework or heard of MCP. They watch with three things open: their `~/AC215/llm-rag` clone (with L05's
collection on disk), a fresh clone of `dlops-io/llm-agent-google-adk`, and a Colab copy of the Cheese
Quiz; they pause to type each command.

Goal: after the video they can say what separates a plain LLM call, a reasoning workflow and an agent
(who decides the next step) and name the lecture's five blocks of an agent, and which one nobody writes
by hand; explain that every model call is a fresh, stateless envelope, and spot a swapped `system`/`user`
role; read a function declaration (name, description, JSON-schema parameters, `enum`, `required`) and
explain function calling (the model writes `{name, args}`, their code makes the call, call 2 carries the
question, the model's own turn with its thought signature, and the function response), and what
`mode="any"` forces and takes away; run llm-rag's `--agent` on L05's collection and explain why the
staff's recorded answer talks about a book that no longer exists; explain the agent loop, its stop rule
and turn caps, and why llm-rag's agent runs one lap; set up the ADK repo (the real folder name, the key
and a current model in the root `.env`, the failing `uv sync` and `uv python pin 3.13`, `uv run adk web`,
the telemetry question, folder names ADK accepts); explain Runner, session, state and events, `output_key`
and `{key}`, and session state versus the lecture's memory; explain MCP (one protocol, one connection per
server, stdio or HTTP) and `tool_filter`, and sort tools into data, action and orchestration; compare three
ways to compose agents by who plans the order; explain the harness ideas of the last two notebooks
(Python-owned arithmetic, an approval gate only a later human turn opens, success as a receipt for a file
on disk) and why a rule written in the prompt is not a check; tear down.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `SLIDES.md` (the lecture,
binding next to the digest, docs/AC215_SERIES.md rule 9), `assets/` (see `ASSETS.md`). Where the digest
and the captures disagree, the captures win (BRIEF.md's table); where the slides and the captures
disagree, the captures decide what is shown and the SAY says so kindly, in one sentence. Nothing in a
terminal or notebook-output panel is typed by hand: every output line below names its file and line
numbers. v1 is written from BRIEF.md; the four review lenses come next (`build/review_*.md`).

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at most
  about 60 words, sentences under 30 words) and become the subtitles. Plain spoken English: no backticks,
  no symbols; commands, flags and paths are on screen and said in words ("dash dash agent", "chunk type
  char split", "dot env", "uv python pin 3.13"). The repo names are said "L-L-M rag" and "L-L-M agent
  google ADK"; ADK is "ADK" (letters) or "the Agent Development Kit"; MCP is "MCP"; ONNX Runtime is
  "O-N-N-X runtime"; the model names "Gemini 3.1 Flash-Lite", "Gemini 2.5 Flash", "GPT-4o". A command is
  never the bare subject of a sentence ("an extra ls shows", "the load step"). Numbers as digits ("10
  passages", "11 books"); never a "!" after a digit. Versions that will change are said with "at the time
  of recording" (Python 3.12.15, uv 0.13.1, CPython 3.15.0, ADK 2.12.0, Node 24). Dates in American order
  ("October 18, 2026").
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences` splits
  only there; the split drives the TTS gaps, the subtitle cues and the Chinese alignment). No sentence
  opens with a command, a lower-case file name or the word ADK (the voice reads a sentence-initial ADK as
  a word: see "Lexicon" below). No `'s` on a word with a lexicon entry, none after a digit; never "a"
  right before a word with a lexicon entry ("the project file", never "a pyproject.toml"). Spelling
  American on screen and in the SAY ("gray", "analyze"; the colour constants stay GREY etc.).
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, a silent ponder timer of n seconds; the card is removed
  at the start of the next block, whose SAY gives the answer. Five in the video (S04, S08, S09, S13, S14),
  as in BRIEF.md. The card sits in the lower third (y ≈ −2.2) so the picture above stays visible: build it
  with `ponder_card(...)` and place it yourself, as `ac215-l02-containers-1/scenes/s09_run.py` does
  (`pause_and_ponder` centers it). The picture during the timer never shows the answer. S12's "Do you see
  a problem?" is a 5-second silent beat (`self.wait(5)` after the SAY), not a ponder.
- `Lecture: 20–22.` under a scene header lists the slides the scene stands on; `Lecture: none.` means the
  tag never appears in that scene. `LECTURE 20–22` in a SHOW line: from that SAY block on, the GREY
  `lecture_ref(6, "20–22")` tag (`explainer.devops`) sits top right ("Lecture 6 · slides 20–22"), until a
  SHOW changes it or says it leaves. S01 explains the tag once. The slides themselves are never shown:
  every lecture picture below is our own redrawing in the series colours, with the slide's structure and
  terms. At most one short spoken bridge to the lecture per scene, beyond the slide-based beats the brief
  asks for.
- `TERM(folder/file: lines)`: a terminal beat. The scene types the command written just before it in the
  SHOW line (in backticks, exactly as the README spells it; extras exactly as captured), then prints those
  lines of `assets/terminal/folder/file`. Line 1 of every capture is its `$ …` command and is never
  printed; the `[exit N]` line is never printed. In the line list: `…` = print one `…` line; `wrap` = fold
  long lines (`Terminal.print(..., wrap=True)`); without `wrap`, a line longer than a row is cut with `…`;
  `N cut after "x"` = print line N only up to and including x; `a–b joined` = the capture wrapped one
  output line at 80 columns over lines a–b: join them, then print (with `wrap` if needed); `session` = a
  capture whose lines include prompts (`laptop/06`): a listed line that starts with a prompt is not
  printed as output; the scene sets that prompt and types after it. `→ (no output)`: the prompt simply
  returns.
- Extra scripts and long plumbing commands are never typed. `cli-container/31`, `33`, `34`,
  `adk-laptop/35` (multi-line `python - <<'EOF'` blocks), `adk-laptop/31`, `33` (long `curl | python`
  lines), `laptop/10` (a shell loop) and the four `mcp-remote/` curls (with their `/tmp/mcp-headers`
  plumbing) appear as a GREY *extra card*: the tag `extra`, the words "an extra check · in the study
  guide" and the one-line purpose the SHOW gives in quotes; then their output prints in a terminal from
  the listed lines. Their code is never on screen.
- Terminal width. Every terminal is the house `term()` (12.6 wide, 22 pt, 65 characters a row), always
  full width, at most 13 rows. A typed command is never cut: it folds at a space onto an indented second
  row ending in ` \` (`Terminal.type`). When a picture needs the frame, the terminal shrinks to a 3-row
  strip along the bottom edge (the last command and its key output line). Never half width; a second panel
  goes above the strip, never beside a full-width terminal.
- Terminal titles and prompts. llm-rag laptop: title `laptop`, prompt `student@laptop:~/AC215$`, after
  `cd` `student@laptop:~/AC215/llm-rag$`; `laptop · second terminal` for checks while the container runs
  (its prompt is `student@laptop:~/AC215/llm-rag$`). Inside the CLI container the frame turns TEAL, title
  `container · llm-rag-cli`, prompt `app@abcf218747d0:/app$` (`laptop/06` line 41); after `exit` the frame
  turns GREY again. ADK laptop (part 2): title `laptop`, prompt `student@laptop:~/AC215$`, after `cd`
  `student@laptop:~/AC215/llm-agent-google-adk$`; `laptop · second terminal` for the extra `curl` checks
  while `adk web` runs.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b, header the path as
  in the viewer's clone (`agent_tools.py · lines 9–19`, `1-baseline/agent.py · lines 14–19`); after the
  S10 rename a GREY subtitle says "your copy: baseline/agent.py". Never more than 12 lines on screen; a
  longer range is shown in windows of ≤ 12 lines that Transform into each other, or *folded* (only the
  listed lines, a GREY `…` row between gaps, header suffix `(folded)`). A line longer than 65 characters
  is shown wrapped (continuation rows indented, marked with a GREY ↪). An *excerpt chip* quotes an exact
  sub-string of one line, headed `path · line N (excerpt)`. `PANEL(file: lines, "header")`: the same look
  for lines from `assets/terminal/` (a diff, a recorded line); the header names the real file or command,
  never a capture folder.
- Colab. Every notebook scene draws a BLUE rounded frame (the Colab VM is Google's cloud) titled with the
  notebook's name, tag `illustration`; menus and the Secrets panel are schematic (no logos, no
  screenshots). Notebook code: `CODE(colab/<notebook>/cell-NN.py: a–b)`, header `<Notebook> · cell NN ·
  lines a–b` (NN = the cell's 0-based index in the `.ipynb`, as the digest and `assets/source/colab/`
  number it; Colab shows no numbers, so the cell's `# @title` or first comment, when it has one, appears
  as a GREY subtitle). Saved notebook outputs: `RECORDED(expected/colab-…: lines)`, an output box under
  the cell (never a terminal frame), tag `recorded · the staff's last saved run`; marker lines
  (`[stdout]`, `[display: …]`, `[stderr]`) are never printed, except where a SHOW quotes one as a label.
  In the notebook scenes the dashed trust boundary, not the colour, separates the student's code from the
  model.
- The staff's `--agent` run: `PANEL(expected/out-txt-agent-run.txt: lines)`, header `out.txt · lines …`
  (out.txt's own line = file line − 1), tag `recorded · the staff's run, September 22, 2026`. It is never
  styled as the viewer's terminal. From S07 on it also carries "old book".
- README cards. While a terminal of 10 or more rows is up, a README card is a one-line chip in the top
  band, right of the tracker: `README.md · line N` + the quoted phrase (≤ 40 characters), tag `expected`
  when it is README text. A multi-line README card appears only above a 3-row strip, or with no terminal.
  `expected/` README text is shown as README text, never as output.
- "With your key, look for" cards (model calls that could not be recorded): a GREY caption card, one short
  line per item, each citing the code line that prints or writes it; items write in when the SAY names
  them. Never styled as terminal output, never with invented values.
- Trackers. `TRACKER Run 3` = the README tracker (`ReadmeTracker` via the `common.py` factory), top left
  in every walkthrough scene, moves to that section and step; `TRACKER Run 3 · extra`: same step, the
  caption gets " · extra" while a command the README doesn't have is on screen. Caption "<source> ›
  section › step k of N", the head naming its source (llm-rag, ADK or Colab). Step titles ≤ 3 words:
  - `dlops-io/llm-rag` `README.md` @ `e17a39f`:
    `Prereq` = "llm-rag · Prerequisites" (`:45-48`, L05), 1: 1 Clone repo ·
    `Run` = "llm-rag · Run Container" (`:75-85`, L05), 3: 1 cd llm-rag · 2 Set GCP_PROJECT · 3 Run script ·
    `Load` = "llm-rag · Load (L05)" (`:144-153`), 1: 1 Load char-split ·
    `Agents` = "llm-rag · Agents" (`:242-271`), 2: 1 Run agent · 2 Agent tool.
  - `dlops-io/llm-agent-google-adk` `README.md` @ `f89faa7`:
    `Start` = "ADK · Getting Started" (`:72-107`), 6: 1 Clone repo · 2 cd folder · 3 Copy .env · 4 Add
    API key · 5 AI Studio key · 6 uv sync ·
    `RunAg` = "ADK · Running Agents" (`:109-119`), 2: 1 adk web · 2 Open UI ·
    `Base` = "ADK · 1-baseline" (`1-baseline/README.md:76-92`), 1: 1 Pick baseline ·
    `Mcp` = "ADK · 3-mcp-tools" (`3-mcp-tools/README.md:53-94`), 2: 1 Install Node · 2 Ask agent.
    (`5-custom-agent` has code panels only, no tracker steps.)
  - Colab, head "Colab · <notebook> › <section>":
    `CQ-Pre` = Cheese Quiz › Prerequisites, 4: 1 Copy notebook · 2 Add key · 3 Install · 4 Download ·
    `CQ-Agent` = Cheese Quiz › LLM to Agent, 3: 1 Base LLM · 2 Reasoning LLM · 3 Agent ·
    `CQ-Inputs` = Cheese Quiz › Managing LLM Inputs, 7: 1 Basic prompt · 2 Prompt engineering · 3 RAG
    documents · 4 Short-term memory · 5 Long-term memory · 6 Tool outputs · 7 Structured output ·
    `CQ-Tools` = Cheese Quiz › Tools, MCP, 3: 1 Fun-fact tool · 2 Remote MCP · 3 Own MCP ·
    `CQ-Guild` = Cheese Quiz › Cheese Quiz Guild, 3: 1 Guild members · 2 Orchestrator · 3 Run guild ·
    `TP` = Travel Planner, 8: 1 Copy, add key · 2 Install · 3 Define tools · 4 Turn 1 · 5 Turn 2 · 6 Turn 3 ·
    7 Turn 4 · 8 Chat loop ·
    `NL` = Cheese Newsletter, 6: 1 Copy, add key · 2 Install · 3 Edit USERS · 4 Define agents · 5 Run demo ·
    6 View outputs.
  Ordering (said in a clause where it happens, BRIEF.md "Ordering notes"): the course site orders the
  tutorials Cheese Quiz → llm-rag → ADK → Travel Planner → Newsletter, and the video interleaves the Cheese
  Quiz by idea while keeping its own section order (S02–S03, S12, S13); `python cli.py --agent
  --chunk_type char-split` runs three times (S05 fresh clone, S06 no key, S06–S07 the staff's recorded
  run); the fixes not in the README are extras (`uv python pin 3.13` S09; the rename, the rejected pin and
  `--port 8080` S10).
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed line, and
  the SAY says so ("an extra check", "not in the README") at least the first time. The two clone commands,
  which the READMEs imply or write as a placeholder, get a GREY caption citing the README line instead.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README step); the SAY
  of that block says "pause". A `▶` never sits on a frame that can't be read when paused: when the
  checkpoint's commands have scrolled away or a picture replaced them, the `▶` sits on a static GREY "your
  turn" card listing them exactly as typed. Every `▶` beat holds its frame for 2 s of silence after its
  SAY (`self.wait(2)`) before anything moves or fades.
- "What if" demos (S10's pinned older ADK and the port clash) run inside a RED dashed frame titled `what
  if · just watch`, so they never look like the viewer's own terminal; the scene then returns to the
  viewer's terminal with a GREY caption "back in your terminal".
- Tags (GREY unless stated): `extra`; `illustration` on every schematic (Colab, AI Studio, the ADK dev UI,
  the hosted Cheese Agent Tool, V6's whiteboard run, the "inside ADK" loop); `recorded` on everything the
  teaching staff saved (`out.txt`, the notebooks' outputs; never on our own runs); `expected` on README
  text; `stand-in` (PINK) on `cli-container/33`'s ten chunks; `real run · no key` on `cli-container/30`,
  `real run · placeholder key` on `adk-laptop/29`/`33`; `built, not sent` on the two request bodies
  (`cli-container/31`, `33`); `at the time of recording` next to versions; `erratum` on every tutorial slip
  (the SAY says "a small slip" where it helps, always with the fix); `fix · not in the README` on
  `uv python pin 3.13` and the rename; `your numbers will differ` on container ids, session ids and the MCP
  fact; `concept · lecture only` (GREY dashed) on lecture ideas with no code here (Self-RAG, Corrective RAG,
  handoffs, the research tree, `ParallelAgent`); GOLD cost tags ("paid · per call") on every model call and
  hosted search, and the GOLD key glyph for each of the three keys (never their content).
- Semantic colours (BRIEF.md, series table applied):

  | meaning | colour |
  | --- | --- |
  | your laptop: `~/AC215`, the two clones, the laptop terminal, the browser and the ADK dev UI as a page on it, `.env` as a file; the user's turn ("the human types yes") | GREY |
  | the cloud: every model (the LLM core: `gemini-3.1-flash-lite` on Vertex AI, the Gemini API behind the AI Studio key, `gpt-4o`, `gpt-5.6-luna`), anything the model writes (the function-call card, the answer, the orchestrator's "done!"), OpenAI's hosted `web_search`, the remote MCP server, the Colab VM's frame, the hosted Cheese Agent Tool | BLUE |
  | containers: `llm-rag-cli` (where `cli.py` and `agent_tools.py` run — the dispatcher, the two calls), `llm-rag-chromadb` and its collection cylinder; the function-response card llm-rag's code builds | TEAL |
  | a Python that was already on the machine (V5: none on our laptop) | ORANGE |
  | project-owned and pinned: the function declarations (the menu cards: names, descriptions, `enum`), chunk cards, session-state cells, `.python-version`, `pyproject.toml`'s lines, everything the harness checked (the approved proposal, Python's budget report, the receipt) | GREEN |
  | tools you install and the loops they run: docker / Compose, uv (and the CPython it downloads), Node.js / `npx` and the filesystem MCP server, ADK (`adk`, `Runner`, `SequentialAgent`), the OpenAI Agents SDK (`Runner.run`), Microsoft Agent Framework, FastMCP; the dynamic-control block once a framework fills it | PURPLE |
  | errors and "avoid this": every traceback's last line, `NotFoundError`, `DefaultCredentialsError`, the missing `cp315` wheel, `Invalid agent name`, Errno 98, 406 to a browser, `MaxTurnsExceeded`, the swapped roles, a rule that slipped | RED |
  | your turn, the trackers, "look here now", the anatomy block in focus, the PENDING stamp | YELLOW |
  | money: every model call and hosted search (a GOLD tick per call), the three keys (GOLD key glyphs) | GOLD |
  | routes and lookups: the user's question and `search_content`, the query vector, the trust-boundary crossing, MCP transports (the stdio pipe, HTTPS), `localhost:8000` / `:8080` / `:8001`, the `{key}` placeholder holes, "the nearest `.env`" | PINK |
  | lecture concepts with no code here (Self-RAG, Corrective RAG, handoffs, the research tree, `ParallelAgent`), and the future (L07's harness) | GREY, dashed |

  The colour of a card says who wrote it: the model's function call is BLUE, the response llm-rag's code
  builds is TEAL, a harness check is GREEN. Something merely absent (a lock file not in the repo, a tool
  list that is empty, the missing system instruction) is a GREY dashed ghost, not RED.
- Visual set pieces V1–V8 are specified in BRIEF.md ("Visual set pieces"); SHOW lines say which one, its
  state, and what moves. V1's mini-map (from the end of S02 to S08, and in S11): a glyph-only copy of the
  anatomy, ≈ 3.2 × 1.6, bottom right above the safe-frame edge; LLM core BLUE, the other four blocks GREY
  outlines, Dynamic Control dashed until S08 fills it PURPLE; the block in focus lit YELLOW (Tools in
  S04–S07, Dynamic Control in S08). It hides whenever a terminal taller than the 3-row strip, or a code
  panel of more than 5 lines, is on screen. V1 does not copy the slide's colours.
- Running example (BRIEF.md): user `student`, host `laptop`, workspace `~/AC215` (the narration says
  "wherever you keep your clones" where it matters). The question `Describe where cheese making is
  important in ‹instructor›'s book?` (`cli.py:435`); the narration says "the instructor's book". The
  Cheese Quiz question "What's the best cheese for a grilled cheese sandwich?" (cell 37). The browser:
  `http://localhost:8000/dev-ui/` (`adk-laptop/16`).
- Names on screen. Every panel line goes through `scenes/common.py`'s `unname(text)`, which replaces
  `Pavlos Protopapas`, `Protopapas`, `Pavlos` and `pavlos` with a GREY chip `‹instructor›` (so
  `‹instructor›_fun_fact_mcp`, `https://‹instructor›-fun-facts.dlops.io/mcp`, `"‹instructor› Cheese MCP"`).
  The captured files stay unchanged. Mara and Anja (characters in the instructor's story) are fine.
  Public-domain authors appear only inside the enum panels (`agent_tools.py:19-29`) and never in captions
  or narration; books are named by title. The Newsletter's readers are `<reader1>`… / `<email>`; only
  `colab/cheese-newsletter/cell-16.redacted.py` is ever quoted for the `USERS` cell. Never shown:
  `laptop/04` (a GitHub user name), `laptop/09` line 2 past `2026-09-22` (the commit subject) and line 7
  (the book's author line), `cli-container/34` lines 16–25, any Colab cell 00 (the course header), the
  instructor's name anywhere, a key's content, a real project id (`ac215-project` appears only in the diff
  line `laptop/05` line 10 that the viewer edits).
- Never shown (BRIEF.md "Things never to do"): slide images, README figures (`images/llm-rag-flow-3.png`,
  `demo.gif`), Google/Colab/OpenAI/Microsoft/Node logos or screenshots; the capture's plumbing
  (`adk-laptop/11`, `Resolved 171 packages`, `torch==2.14.1+cpu`, the Docker-in-Docker laptop,
  `proxy_relay.py`, `~/.npmrc`, CA variables, `docker exec`, `/tmp/mcp-headers`); the symlink attempts;
  the `google-adk<1.28` pin as a fix; invented `LLM Response:` values, ADK events, State-tab values, model
  replies or notebook outputs; `cli-container/31` or `33` as sent; `33`'s ten chunks as what the real query
  returns.
- Length and parts: narration 4,292 words (`python -m explainer.script`, v1; BRIEF.md: 3,900–4,300,
  plan ~4,250). Part 1 = S01–S08 (what an agent is, and function calling by hand) 2,127 words; part 2 =
  S09–S16 (frameworks own the loop) 2,165 words. Per scene (BRIEF.md budget ±15 %):

  | scene | S01 | S02 | S03 | S04 | S05 | S06 | S07 | S08 | S09 | S10 | S11 | S12 | S13 | S14 | S15 | S16 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | budget | 260 | 280 | 200 | 290 | 250 | 280 | 300 | 270 | 360 | 300 | 270 | 280 | 240 | 260 | 200 | 210 |
  | words | 256 | 272 | 199 | 291 | 259 | 272 | 304 | 274 | 362 | 303 | 268 | 292 | 230 | 261 | 210 | 239 |

  `explainer.script` assumes 155 wpm and BRIEF.md 174; L04/L05 measured 144–151 wpm for af_heart at 0.9,
  which would make ≈ 28.5–30 min of voice and, with typing, outputs, five ponders and the `▶` holds,
  ≈ 34–35 min: at the top of the series range, so the review lenses should not grow the script (trim
  rather than add). After the merge, run `python -m explainer.script videos/ac215-l06-agents-1/script.md
  --synth` when the CPUs are free and put the measured total here. Part 1 ends on the teardown of S08
  (empty frame); part 2 opens on a fresh laptop picture in S09. Each part ends on an empty frame.
- Notes for scene authors.
  - `Capture.pick()` indexes the output body: pick index = file line − 1. `expected/*.txt` line 1 is a `#`
    source header (never printed).
  - `cli-container/` files ran through `docker exec` and have no prompt: draw `app@abcf218747d0:/app$` and
    type the `$` command there (or show the extra card). `laptop/06` (session): line 41 is the container
    prompt with `exit` typed after it; S05 stops at that prompt (cut before `exit`), S08 types `exit` and
    prints line 42.
  - Captures wrapped at 80 columns (join before printing): `laptop/06` 7–9, `laptop/13` 2–3,
    `adk-laptop/07` 5–7 and 9–11, `15` 2–3, 5–8, 10–11, 44–45, `24` 132–134, `29` 36–37, 38–39, 41–42,
    357–363. `adk-laptop/36` and `cli-container/` files are not wrapped (fold them with `wrap`).
  - `adk-laptop/12`: print only the lines the SHOW lists; lines 5–7 and 140 carry the capture-only CPU
    index's numbers (`Resolved 171`, `148 packages`, `+cpu`) and are never printed.
  - Lexicon (to add at review, `explainer/lexicon.yaml`, `# AC215 L06`): **ADK** (letters, `ˌeɪdˌiːkˈeɪ`;
    a phrase-initial "ADK web" phonemizes as `ˈædk`), **enum** (`ˈiːnʌm`; the voice says `ɪnˈʌm`),
    **Colab** (`kˈoʊlæb`; the voice says `kˈɑːlæb`). Checked and fine without an entry: MCP, FastMCP, npx,
    GPT-4o, L-L-M rag, O-N-N-X, Gemini 3.1 Flash-Lite, Havarti, Mara, Anja, OpenAI, AI Studio, localhost,
    transhumance and Self-RAG (existing entries), PyTorch, CUDA, JSON, dot env, 8001, 1,505, 3,509, 2,690.
    Keep the SAY spellings exactly as written.
  - i18n stage: `en_display` candidates (spoken form → literal): L-L-M rag → `llm-rag`, L-L-M agent google
    ADK → `llm-agent-google-adk`, dot env → `.env`, dash dash agent → `--agent`, mode any → `mode="any"`,
    O-N-N-X runtime → `onnxruntime`, MCP underscore tools → `mcp_tools`, custom underscore agent →
    `custom_agent`, response dot text → `response.text`.

---

## S01 · Who searched your database? — `s01_hook.py` · `Hook`

Lecture: 20–22.

SHOW: Black frame, no tracker. Left: a GREY question card types in
`Describe where cheese making is important in ‹instructor›'s book?` (from
`expected/out-txt-agent-run.txt` line 9, through `unname`), tag `recorded · the staff's run`. Bottom
center: the GREY laptop outline holding the TEAL Chroma container (a cylinder, label `llm-rag-chromadb ·
localhost:8000`). Far right: a BLUE cloud "Google Cloud" with a BLUE chip "Gemini". Between them,
PANEL(expected/out-txt-agent-run.txt: 65, 68) (header `out.txt · lines 64, 67`; line 68 reads
`Calling function with args: ‹instructor› , cheese making importance location`) types in line by line.
SAY: Here's a question for a cheese expert: describe where cheese making is important in the instructor's book. In the staff's recorded run, two lines print before any answer: a function called get book by author, and its arguments.

SHOW: From the panel's second line a PINK arrow runs down into the TEAL cylinder; ten GREEN chunk cards
rise out of it, each with the same small GREY label "one book". Then a RED dashed line leaves the BLUE
Gemini chip toward `localhost:8000` and stops at the cloud's edge, where a GREY chip reads "localhost =
this machine". Two YELLOW questions write in, center: "Who searched your database?" and "Who chose the
book?" They shrink into a small YELLOW card top right that stays until the scene ends (S07 answers it).
SAY: Ten passages came back, all from one book, chosen by its author. But Gemini runs in Google's data center, where localhost means nothing. So who searched your database, and who chose the book?

SHOW: LECTURE 20–22 (the tag appears top right; for this beat only a small GREY caption under it reads
"the lecture slides this stands on"). The picture shrinks away. A GREY request card writes in (our words,
slide 20): "5 days in Paris · flights and hotels within budget · activities you'd enjoy · replan if it
rains or a flight is late". Below it, "Can an LLM or RAG alone do this?" and two verdict chips: BLUE
"LLM: drafts a plan, can't act as things change" and TEAL-outlined "RAG: fetches and summarizes".
SAY: The lecture asks a bigger version: plan five days in Paris, and replan if it rains or a flight is late. A model can draft a plan, and RAG can fetch facts, but neither can act.

SHOW: Three GREY dashed chips slide in under the verdicts as named (slide 22): "live systems", "tools
that act", "autonomy".
SAY: What's missing: live systems, tools that act, and the autonomy to decide.

SHOW: The lecture tag leaves. Three horizontal bands write in, top to bottom: "by hand · llm-rag --agent"
(a TEAL container glyph and a BLUE chip, caption "Docker · Gemini on Vertex AI"); "with a framework ·
Google ADK" (a PURPLE uv glyph and a BLUE chip, caption "uv · the Gemini API"); "with a harness · three
Colab notebooks" (a BLUE notebook frame with a GREEN check inside, caption "OpenAI"). Small markers at
the right edge: "part 1" beside band 1, "part 2" beside bands 2–3.
SAY: Today we climb toward that in three steps. By hand, with L-L-M rag's agent; with a framework, Google's Agent Development Kit; and with a harness, in three Colab notebooks.

SHOW: A layout preview in three steps, each clearing the last, as named: (1) the tracker top left, its
head cycling "llm-rag", "ADK", "Colab", with a YELLOW circle pulsing around it; (2) a GREY
`lecture_ref(6, "51–53")` sample top right; (3) a 3-row terminal strip (tag `preview`) with
`python cli.py --agent --chunk_type char-split` and a YELLOW `▶ your turn` tag. Then a row of GREY tags
writes in along the bottom: `recorded` · `expected` · `illustration` · `extra` · `stand-in` · `no key` ·
`built, not sent`.
SAY: The tracker, top left, shows the step; the gray tag, top right, the lecture slides. Pause at each yellow your-turn tag, and run the command.

SHOW: The preview clears. A checklist card "You need" writes in row by row as named: "lecture 5's
char-split collection (or the load step)", "Docker", "uv", "Node.js", a GOLD key "Google AI Studio key",
a GOLD key "OpenAI key · billing on".
SAY: You'll need lecture 5's database, Docker, uv, Node, and two keys: one from Google AI Studio, and one from OpenAI, with billing on.

SHOW: A card "Recorded October 18, 2026 · no Google or OpenAI keys" with three rows writing in as named:
GREEN check "real runs: Docker, Chroma, uv, the ADK web server, two MCP servers"; a GREY crossed-out key
"model calls: stopped before sending, or refused"; tag `recorded` "model answers: the teaching staff's
saved outputs".
SAY: We recorded on October 18, 2026, without keys. Docker, Chroma, uv, the ADK web server and two MCP servers ran for real; every model call stopped unsent, or was refused. Model answers are the staff's saved outputs.

SHOW: A GREY chip `‹instructor›` with the caption "the instructor's name, hidden on screen". A footer
card "every command: MLOps_Learning · guides/L06-agents-1.md". Fade to an empty frame.
SAY: On screen we hide the instructor's name; your terminal shows it. Every command is in the study guide, in the MLOps Learning repo.

---

## S02 · Who holds the steering wheel? — `s02_steering.py` · `SteeringWheel`

Lecture: 16–18, then 25–27.

SHOW: TRACKER CQ-Pre 1. A BLUE Colab frame (title "Cheese Quiz", tag `illustration`) with a schematic
menu path File › Save a copy in Drive, highlighted YELLOW. TRACKER CQ-Pre 2: a schematic Secrets side
panel slides in: a key icon, one row Name `OPENAI_API_KEY` · Value `••••••` · Notebook access toggle ON;
a GOLD key glyph beside the row. Under it CODE(colab/cheese-quiz/cell-12.py: 3–4) (header `Cheese Quiz ·
cell 12 · lines 3–4`, subtitle "Set Up OpenAI Key"), `userdata.get('OPENAI_API_KEY')` highlighted.
SAY: Part 1 starts in Colab, with the Cheese Quiz. Save a copy in Drive, then add your OpenAI key in the Secrets panel, under the name shown, with notebook access on.

SHOW: TRACKER CQ-Pre 3. CODE(colab/cheese-quiz/cell-10.py: 3) (header `Cheese Quiz · cell 10 · line 3`,
subtitle "Install Packages"): `fastmcp openai-agents` gets a GREY tag "unpinned"; `> /dev/null 2>&1`
underlines YELLOW with a tag "hides every error · erratum: rerun without it if imports fail". TRACKER
CQ-Pre 4: RECORDED(expected/colab-cheese-quiz-c13-download.txt: 5–6, 9–10). `▶ your turn` on a static
GREY card "Prerequisites: save a copy · Secrets: OPENAI_API_KEY · Install · Download". Hold 2 s.
SAY: The install cell installs two packages, unpinned, and hides all output: if imports fail later, rerun it without that redirect. Then download the quiz files, and pause to run the setup.

SHOW: TRACKER CQ-Agent 1. V1 lane 1 in the top third: a PINK question chip "What's the best cheese for a
grilled cheese sandwich?" → a BLUE model chip `gpt-4o` → a GREY answer card; a counter "1 call · 2.81 s"
(RECORDED(expected/colab-cheese-quiz-c21-base-llm.txt: 3, 30) in a small output box). In the lower half
CODE(colab/cheese-quiz/cell-20.py: 8–17) (header `Cheese Quiz · cell 20 · lines 8–17`, subtitle "Define
BaseLLM"), line 14 `messages=[{"role": "user", "content": user_prompt}],` highlighted.
SAY: Now the notebook asks one question three ways, with the same model each time: what's the best cheese for a grilled cheese sandwich? Lane 1, the base LLM: one call to GPT-4o, one answer, in under 3 seconds.

SHOW: LECTURE 16–18. TRACKER CQ-Agent 2. Lane 2 builds under lane 1: a conveyor of GREY code boxes named
`analyze_query`, `decompose_problem`, then `answer_sub_question` / `verify_response` four times, then
`synthesize_final_response`; each pings the same BLUE `gpt-4o` chip with a GOLD tick. Small GREY dashed
labels from slide 18 float in above the boxes they describe: "problem decomposition", "sequential
processing", "verification loop", "summary generation". A GREY decision diamond on the conveyor: "your
Python decides". RECORDED(expected/colab-cheese-quiz-c25-reasoning-llm.txt: 8–29) scrolls through a
strip (eleven `🧠 BaseLLM: Making single API call...` lines, each ticking a counter), then (c25: 100–101)
`Sub-questions explored: 4` / `Total tokens: 701, Time: 39.34s`. Beside it
CODE(colab/cheese-quiz/cell-24.py: 98–119) folded to 99, 102, 108–110, 116, 119 (header `Cheese Quiz ·
cell 24 · lines 98–119 (folded)`); line 116 `total_tokens += 100  # Approximate token usage` gets a
GREY `erratum` tag "an estimate: +100 per sub-question".
SAY: Lane 2, the reasoning LLM: Python methods run in a fixed order. Analyze, split into 4 sub-questions, answer and verify each, then combine. That's 11 calls and 39 seconds, and its token total is only an estimate.

SHOW: A small GREY dashed stack of four layers (slide 16's reasoning engine, our redrawing, labels
unreadably small) slides beside lane 2 and merges into the conveyor; the GREY diamond pulses. Two
captions: GREY "reasoning workflow: many calls, ordered by your code" and a GREY dashed chip "the model's
own thinking: inside one call · S07".
SAY: The lecture calls a multi-call system like this a reasoning engine. Here your Python orders the calls, so it's a reasoning workflow, not a reasoning model.

SHOW: TRACKER CQ-Agent 3. The lecture tag leaves. Lane 3 builds under lane 2: the decision diamond now sits *inside* the BLUE
`gpt-4o` chip; the model reaches into a GREY toolbox, takes a BLUE `web_search` chip (hosted, GOLD tick),
twice — the two search texts of RECORDED(expected/colab-cheese-quiz-c31-simple-agent.txt: 23, 28) fly
out as small PINK chips — returns, and stops; "13.29 s". CODE(colab/cheese-quiz/cell-30.py: 13–16, 30–35)
(header `Cheese Quiz · cell 30 · lines 13–35 (folded)`, subtitle "Define SimpleAgent"), `tools=[web_tool]`
highlighted. RECORDED(c31: 99–100); line 99 `Tools used: 1` gets a GREY `erratum` tag "tools configured
(cell 30 · line 71), not calls".
SAY: Lane 3, the agent: the same model, plus instructions and a web search tool. Its answer reports two searches, and it stopped on its own after 13 seconds. Its last line, tools used 1, counts tools configured, not calls.

SHOW: LECTURE 25–27. The three lanes fold into V1, the anatomy, full size: a GREY chip "Task / Goal" →
one rounded agent box holding a BLUE "LLM core", GREY-outlined "Instructions", a wide dashed bar "Dynamic
Control", GREY-outlined "Tools" and "Memory" → a GREY chip "Task completion". Above it the lecture's
definition writes in (slide 26, our words): "an LLM, given instructions and tools, that runs on its own
until the task is done". The Dynamic Control bar turns YELLOW, caption "who decides the next step".
SAY: The lecture defines an agent as an LLM, given instructions and tools, that runs on its own until the task is done. Of its five blocks, one decides the next step: dynamic control, the steering wheel.

SHOW: The three lanes return small at left, the identical BLUE `gpt-4o` chip in each highlighted YELLOW;
a GREY card "agent = a smarter model" gets a RED strike. GOLD tags per lane: "1 call", "11 calls",
"calls + hosted searches". `▶ your turn` on a static GREY card "LLM to Agent: Base LLM · Reasoning LLM ·
Agent (cells 18–31)". Hold 2 s. Then the anatomy shrinks into the bottom-right corner: the mini-map.
SAY: So an agent isn't a smarter model: the model was the same in all three lanes. What changed is who steers, and the tools. Every call is paid; pause, and run through the agent.

---

## S03 · Everything the model knows is in the envelope — `s03_envelope.py` · `Envelope`

Lecture: 41.

SHOW: TRACKER CQ-Inputs 1. The mini-map hides. An excerpt chip (header `Cheese Quiz · cell 35 · line 1
(excerpt)`): "LLMs are stateless functions." V2: an envelope slides to the BLUE `gpt-4o` chip, which
opens it, answers, and the envelope crumples away; a fresh empty envelope arrives. Caption "every call: a
fresh envelope".
SAY: Next section: managing the model's inputs. It opens plainly: LLMs are stateless functions. Every call is a fresh envelope, and the model knows only what's inside.

SHOW: LECTURE 41. V2: seven sheets slide into the envelope, one per tracker step (TRACKER CQ-Inputs 1 → 7),
each labelled in slide 41's words: "user prompt", "system prompt", "contexts: retrieved documents",
"user sessions: earlier turns", "user preferences: a profile from past sessions", "contexts: tool
outputs", "output schema".
SAY: The notebook keeps the model and question fixed, and adds one sheet per step. A system prompt, retrieved documents, earlier turns, a profile from past sessions, a tool's output, an output schema.

SHOW: Beside the envelope an answer card shows the top pick, changing as the sheets replay quickly
(RECORDED excerpts, tag `recorded`): `Cheddar` (c38: 10) → `American Cheese` (c39: 10) → `American
Cheese` (c40: 10) → "mild cheddar and mozzarella" (c41: 8) → `Havarti` (c42: 8) → "Whole Foods Mild
Cheddar" (c43: 8) → `"top_recommendation": "Whole Foods Mild Cheddar",` (c44: 10).
SAY: Watch the top pick change: cheddar, then American, mild cheeses for the kids, Havarti, a mild cheddar from Whole Foods, and finally the same pick as strict JSON.

SHOW: TRACKER CQ-Inputs 4. CODE(colab/cheese-quiz/cell-41.py: 18–25) (header `Cheese Quiz · cell 41 ·
lines 18–25`, subtitle "Step 4: Adding Short-term Memory"): lines 20–23, the earlier turns, highlight
GREY one by one and fly into the envelope as sheets. Caption "memory = paper you put back, every call".
SAY: Step 4 shows what memory really is. The earlier turns aren't remembered: the code sends them again, every time. Memory is paper you put back in the envelope.

SHOW: The sheets regroup under two GREY headers in slide 41's words: "Instructions: system & user
prompts · contexts · output schema" and "Memory: user sessions · user preferences". A GREY dashed chip
"Lecture 7: context engineering".
SAY: The lecture files these sheets under two building blocks, instructions and memory. Next lecture names the craft: context engineering.

SHOW: TRACKER CQ-Inputs 2. A YELLOW card "Spot it" (no timer). CODE(colab/cheese-quiz/cell-39.py: 16–21)
(header `Cheese Quiz · cell 39 · lines 16–21`, subtitle "Step 2: Prompt Engineering"); lines 19–20
highlight. In V2, the "system prompt" and "user prompt" sheets flip so that each carries the other's role
label; both flash RED.
SAY: Now look closely at step 2's code. Can you spot the slip? The system prompt goes in with the role user, and the question with the role system.

SHOW: An `erratum` tag; the two labels swap back (GREEN check), caption "swap the roles, then compare ·
steps 3–7 are right". `▶ your turn` on a static GREY card "Managing LLM Inputs: steps 1–7". Hold 2 s.
SAY: Swap those two roles before comparing; from step 3 on, they're right. Pause, and run the seven steps.

SHOW: The "tool outputs" sheet glows YELLOW in the envelope; a GREY "?" chip appears beside it: "how does
a model ask for a tool?" The envelope fades.
SAY: And notice step 6: a tool's output went into the envelope. But how does a model ask for a tool?

---

## S04 · A menu of two tools — `s04_menu.py` · `ToolMenu`

Lecture: 8–14, then 39.

SHOW: LECTURE 8–14. No tracker yet. V3's first half: L05's strip (slide 8) writes left to right: PINK
"question" → GREEN "Retrieval" → BLUE "LLM" → GREY "Response". Then six GREY dashed boxes (slides 9–12,
our words) fly in one after another as named and stack into a column between two BLUE LLM boxes (slide
13): "pre-retrieval", "post-retrieval", "retrieval decision", "document grading", "query rewrite", "web
search".
SAY: Lecture 5's RAG was a straight line: question, retrieval, model, response. The lecture's recap adds smarter retrieval: steps before and after the search, deciding whether to retrieve, grading results, rewriting the query, searching the web.

SHOW: The first BLUE LLM box gets a YELLOW label "chooses"; a GREY caption "agentic RAG".
SAY: Agentic RAG puts a model in front of that menu, and lets it choose.

SHOW: TRACKER Agents (llm-rag · Agents, no step lit). The column shrinks to two GREEN menu cards,
`get_book_by_author(author, search_content)` and `get_book_by_search_content(search_content)`;
"retrieval decision" stays behind as a GREY dashed card (S06 crosses it out). A README chip (header
`README.md · line 244 (excerpt)`, tag `expected`): "let the LLM decide how to retrieve".
SAY: L-L-M rag's agents section is agentic RAG with a menu of two. Its README says: let the L-L-M decide how to retrieve. Search one author's book, or search all books.

SHOW: The mini-map hides. CODE(agent_tools.py: 9–19) (header `agent_tools.py · lines 9–19`): line 10
`name="get_book_by_author",` highlights, a GREEN tag "the name the model writes back"; line 11 the
description, tag "the only documentation the model sees"; lines 13–15 `parameters={ "type": "object",
"properties": {`, tag "JSON schema".
SAY: Here's the first menu item, written by hand: a name, which the model will write back, and a description, the only documentation the model ever sees. Parameters come as a JSON schema.

SHOW: The panel Transforms to CODE(agent_tools.py: 19–30) (line 28 through `unname`): the nine names get a
GREEN bracket "enum: only these 9"; then it folds the names to one `… 9 names …` row and Transforms to
CODE(agent_tools.py: 31–37): line 33 wraps and highlights YELLOW, its "a a" gets a GREY `erratum` tag
"typo in the source"; line 36 `"required": ["author", "search_content"],` highlights GREEN.
SAY: The author must be one of 9 names in an enum, and both fields are required. The search text's description even coaches the model: expand the search term to a sentence or two.

SHOW: CODE(agent_tools.py: 41–49) (header `agent_tools.py · lines 41–49`): on line 41, `author,
search_content` underline GREEN "from the model", `collection, embed_func` underline TEAL "your code
supplies these"; line 47 `n_results=10, where={"author": author}` highlights PINK. Then it Transforms to
CODE(agent_tools.py: 78–81): "one Tool, two declarations".
SAY: Now the real function. It takes two more arguments, the collection and an embedding function, that aren't in the schema: your code supplies them. The model controls only the author and the search text.

SHOW: LECTURE 39. Three GREY dashed duty chips (slide 39, our words): "pick the tool", "format its
inputs", "interpret its outputs". The first two attach to a BLUE pen glyph "the model writes"; the third
gets a small GREY tag "call 2 · S07". A TEAL gear "your code runs" sits beside the pen.
SAY: The lecture says a tool-using agent must pick the right tool, format its inputs, and interpret its outputs. Here the model picks and formats only by writing; your code runs.

SHOW: Two columns: left, the nine enum names (masked) in GREEN; right, the 11 book titles in GREY, cut out
of the `Processing file: outputs/embeddings-char-split-<title>.jsonl` lines of
`cli-container/20-load-char-split.txt` (lines 9, 23, 36, 52, 65, 77, 89, 101, 116, 129, 142: titles
only). No lines connect them (the picture never shows the answer). The ponder card sits in the lower
third.
SAY: Here are the 11 books in the collection, beside the 9 names in the enum.
PONDER(8 s, "Nine names in the enum, eleven books in the collection.\nWhich books can the agent never reach by author?\nIs it for the same reason?")

SHOW: An extra card: "count the chunks per author" (container prompt `app@abcf218747d0:/app$`); a
terminal strip prints TERM(cli-container/34-x-authors.txt: 15, 26–28). In the two columns, GREEN lines
connect nine books to the nine names; *Cottage Cheese Recipe Book* stays unconnected with a GREY tag
"author not in the list · 178 chunks"; *Womans Institute Library of Cookery* gets a RED-edged tag "author
= None · 1,505 chunks · lecture 5's file-name slip".
SAY: Two books. The cottage cheese recipe book, 178 chunks, has an author who isn't on the list. The Woman's Institute book, 1,505 chunks, has no author at all: lecture 5's file name slip.

SHOW: Both unconnected books get a PINK arrow to `get_book_by_search_content` "still reachable". Then V3's
stage builds full width: left, the BLUE Google cloud with a BLUE chip "Gemini · location global"; center,
a dashed vertical trust boundary labelled PINK "HTTPS"; right, the GREY laptop holding two TEAL containers,
the CLI container (`cli.py`, `agent_tools.py`) and the Chroma container (cylinder
"char-split-collection · book · author · year").
SAY: Both stay reachable by the search across all books. Now the stage: Gemini in Google's cloud, two containers on your laptop, and a boundary between.

SHOW: The two GREEN menu cards slide across the boundary into the cloud; the cylinder stays put, and a
GREY lock glyph sits on it. The mini-map returns, Tools block lit YELLOW.
SAY: The model never gets your database. It gets a menu.

---

## S05 · Back in the container: the agent needs an index — `s05_container.py` · `BackInTheContainer`

Lecture: none.

SHOW: TRACKER Prereq 1. Terminal (full width, 8 rows, title `laptop`, prompt `student@laptop:~/AC215$`).
A GREY caption "fresh start only · README.md · line 48 links the repo" and a GOLD key chip "also: the service-account key in secrets/ (lecture 5 · README.md · lines 52–69)". It types
`git clone https://github.com/dlops-io/llm-rag.git` → TERM(laptop/01-clone.txt: 2).
SAY: Lecture 5 ended on one command; today we run it. Starting fresh? Clone L-L-M rag, and set up the service account key as in lecture 5; otherwise, go to your folder.

SHOW: TRACKER Run 1. It types `cd llm-rag` → (no output); the prompt becomes
`student@laptop:~/AC215/llm-rag$`. TRACKER Run 2: PANEL(laptop/05-x-edit-gcp-project.txt: 10–11, "docker-shell.sh · line 7 · your edit"),
line 10 RED `-`, line 11 GREEN `+`; `your-project-id` gets a YELLOW tag "your own project ID". `▶ your
turn` on a static GREY card "cd llm-rag · set GCP_PROJECT in docker-shell.sh". Hold 2 s.
SAY: Step 1: cd L-L-M rag. Step 2: in docker-shell.sh, set GCP project to your own project ID; we used a placeholder. Pause, and do both.

SHOW: TRACKER Run 3. Terminal (13 rows). It types `sh docker-shell.sh` → TERM(laptop/06-docker-shell.txt:
2–5, 6, 7–9 joined, 10–11, …, 32–34; session; wrap). Lines 6–9 print RED, then turn GREY with the tag
"harmless · its wording depends on your Docker setup"; line 11 `Building 40.5s` gets the tag
`at the time of recording`.
SAY: Step 3: sh docker-shell.sh. Compose starts Chroma first. The pull message after it looks like an error but is harmless: there's no such image online, so Compose builds it.

SHOW: TERM(laptop/06-docker-shell.txt: 35–40; session); lines 38–39 get the tag `at the time of
recording`. Then line 41's prompt appears alone, cut before `exit` (`app@abcf218747d0:/app$`); the frame
turns TEAL, title `container · llm-rag-cli`; `abcf218747d0` gets a GREY tag "container ID · your numbers
will differ". `▶ your turn` beside the prompt. Hold 2 s.
SAY: After about 40 seconds of building, the banner: Python 3.12.15 and uv 0.13.1, at the time of recording. After app at comes the container's ID, new every run; pause, and get to this prompt.

SHOW: TRACKER Run 3 · extra. A second terminal slides over (title `laptop · second terminal`, prompt
`student@laptop:~/AC215/llm-rag$`). It types `docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'`
(extra; folds onto two rows) → TERM(laptop/07-x-docker-ps.txt: 2–4). `0.0.0.0:8000->8000/tcp` highlights
PINK with a tag "port 8000 · remember for part 2". The second terminal slides away.
SAY: An extra check from a second terminal: docker ps. Chroma publishes port 8000; remember that port for part 2.

SHOW: Back in the TEAL container terminal. TRACKER Agents 1. It types
`python cli.py --agent --chunk_type char-split` → TERM(cli-container/10-agent-no-collection.txt: 2–3,
9–10, …, 25; wrap), tag `real run · fresh clone`; line 25 RED. The terminal shrinks to a strip; above it
CODE(cli.py: 427–429) (header `cli.py · lines 427–429`), line 429 RED.
SAY: Now the agents section, step 1: python cli.py, dash dash agent, chunk type char split. On a fresh clone it fails at once: the collection does not exist. That's line 429, before any call to Gemini.

SHOW: A GREY two-way card above the strip: left "kept lecture 5's database? · docker-volumes/chromadb ·
skip ahead", with a GREY note "loaded before September 22, 2026? reload: the book changed · S07"; right
"no database? · chunk → embed → load (lecture 5)".
SAY: The agent stands on lecture 5's index. If you kept that database, it's in the docker volumes folder, but reload it if you loaded before September 22. Otherwise, chunk, embed and load again.

SHOW: On the right path, the "embed" arrow gets a GOLD key; a GREY card slides over it:
PANEL(laptop/08-x-copy-staff-embeddings.txt: 2–3, "outputs/embeddings-char-split-* · copied from commit 68e0bde")
(`11` files, `31M total`), tag `recorded · the staff's vectors`.
SAY: We had no key, so the staff's committed embeddings stood in for the embed step.

SHOW: TRACKER Load 1. The container terminal grows (13 rows). It types
`python cli.py --load --chunk_type char-split` → TERM(cli-container/20-load-char-split.txt: 2–8, …, 142,
152–153; wrap). A GREY chip "8,248 chunks in 11 books · 24 from the instructor's story" (from
`cli-container/34` line 15 and line 143 of `20`). TRACKER Load 1 · extra: it types
`python cli.py --get --chunk_type char-split` (extra) → TERM(cli-container/21-x-get.txt: 6 cut after
`'1021665fac86c5a5-0',`) with a `…`. `▶ your turn` on a static GREY card "python cli.py --load
--chunk_type char-split (or keep yours) · python cli.py --get --chunk_type char-split". Hold 2 s.
SAY: Then the load step: python cli.py, dash dash load, chunk type char split. 11 books, 8,248 chunks; the instructor's story is just 24 of them. An extra get command confirms the collection answers; pause, and load yours.

---

## S06 · Call 1: the model writes the call — `s06_call1.py` · `CallOne`

Lecture: 35, then 10–13.

SHOW: TRACKER Agents 1. The mini-map shows, Tools lit. CODE(cli.py: 431–437) (header `cli.py · lines
431–437`; line 435 through `unname`): `Content(role="user", parts=[Part(text=…)])`, the question PINK. Then
it Transforms into CODE(cli.py: 441–453) (header `cli.py · lines 441–453`); the mini-map hides.
SAY: After the collection lookup, the agent function builds the user's turn: the question, with the role user. Then comes the first call to Gemini.

SHOW: LECTURE 35. Line 445 `temperature=0,` highlights, with a GREY dashed chip (slide 35, our words) "LLM
core: model · sampling · response format"; line 446 `tools=[agent_tools.cheese_expert_tool],` highlights
GREEN "the menu"; lines 447–451 highlight YELLOW, `mode="any"` boxed.
SAY: Three settings: temperature zero, the menu as tools, and a tool config with mode any. Sampling is one of the lecture's design choices; zero keeps the tool choice repeatable.

SHOW: A terminal strip at the TEAL container prompt. It types
`python -c 'from google.genai import types; print(repr(types.FunctionCallingConfig(mode="any")))'`
(extra; folds) → TERM(cli-container/32-x-mode-any.txt: 2–4). `ANY` highlights YELLOW; caption "the model
must answer with a function call".
SAY: An extra one-liner shows what any becomes: the enum value ANY. The model must answer with a function call; plain text isn't allowed.

SHOW: LECTURE 10–13. V3's column returns small with its GREY dashed "retrieval decision" card; beside it
a GREY dashed Self-RAG box "Retrieve?" with yes/no branches (tag `concept · lecture only`). A RED line
crosses out "retrieval decision"; caption "chooses which search · never whether". A GREY chip "exercise:
delete tool_config, then greet it".
SAY: In the lecture, a good agent may decide not to search at all; Self-RAG starts with that decision. Ours can't: mode any forces a tool call every time. It chooses which search, never whether.

SHOW: The lecture tag leaves. V2: an envelope opens onto the real request. An extra card: "runs agent() unchanged · prints the
request instead of sending it"; then a full-width terminal at the container prompt prints
TERM(cli-container/31-x-call1-request.txt: 20; wrap, 21–31, 32–34, 35–41 folded to one row `{
"description": "Get the book chunks filtered by author name", "name": "get_book_by_author", … }`, 42–52
folded to `"enum": [ … 9 names … ],` 53–85 folded to `… get_book_by_search_content …`, 86–93, 95), tag
`built, not sent`. On line 20, `locations/global` and `gemini-3.1-flash-lite` highlight BLUE; line 88
`"mode": "ANY"` and line 92 `"temperature": 0.0` YELLOW; line 95 GREY.
SAY: What does Gemini actually receive? An extra script runs the same code, but prints the request instead of sending it. One envelope: the question, both declarations with the enum, mode ANY, temperature zero.

SHOW: A GREY dashed ghost card "systemInstruction" slides next to the body with a tag `erratum` "defined
at cli.py lines 40–58 · never sent (as in lecture 5)".
SAY: And no system instruction: like lecture 5's chat, the agent defines one and never sends it.

SHOW: TRACKER Agents 1. Terminal (full width, TEAL). It types `python cli.py --agent --chunk_type
char-split` → TERM(cli-container/30-agent.txt: 2–3, 8–10, 16–17, …, 71; wrap), tag `real run · no key`;
lines 8–10 (masked) get a GREEN tag "the lookup passed"; line 71 RED. A GREY "with your key, look for"
card: "`LLM Response:` with a function_call · cli.py line 454".
SAY: Now step 1 again, with the collection loaded. The lookup passes and the question prints, but the first model call needs your key: default credentials error, file not found.

SHOW: PANEL(expected/out-txt-agent-run.txt: 15, 17–28, 34) (header `out.txt · lines 14–33 (excerpt)`,
line 23 masked, tag `recorded · the staff's run, September 22, 2026`); line 29 appears as
`thought_signature=b'\x01\x8f=k_…',`. V3: the BLUE model's speech bubble becomes a BLUE JSON card
`{name: get_book_by_author, args: {author, search_content}}` with a small BLUE seal "thought signature".
SAY: Here's what the staff saw. The model's whole answer is a function call: get book by author, with the instructor as author, and the search text, cheese making importance location.

SHOW: `'cheese making importance location'` highlights; a GREY tag "4 words · the description asked for a
sentence or two" (excerpt chip of `agent_tools.py · line 33`). The `id='call_1212960'` line and the seal
pulse.
SAY: Four words, though the description asked for a sentence or two. There's also an ID, and a thought signature; we'll meet it again.

SHOW: PANEL(expected/out-txt-agent-run.txt: 52, "out.txt · line 51"):
`automatic_function_calling_history=[]` highlights GREY "the SDK ran nothing". The BLUE card waits at the
trust boundary, unopened; caption "Gemini wrote arguments · nothing has run yet". A GOLD tag "1 Gemini
call · paid". `▶ your turn` on a static GREY card "with your key: python cli.py --agent --chunk_type
char-split". Hold 2 s.
SAY: The SDK ran nothing either; it has declarations, not your functions. Gemini wrote arguments, and nothing has run yet: one paid call. Pause here, and run step 1 with your key.

---

## S07 · Call 2: your code ran it, the model answers — `s07_call2.py` · `CallTwo`

Lecture: 39.

SHOW: The mini-map shows, Tools lit. CODE(cli.py: 456–460) (header `cli.py · lines 456–460`): line 457
highlights "pick out the function calls", lines 459–460 "hand them to the dispatcher". It Transforms into
CODE(agent_tools.py: 84–94) (line 88 `if function_call.name == "get_book_by_author":` YELLOW), then
CODE(agent_tools.py: 95–110) (lines 95–100 GREEN "call the real function", lines 103–110 TEAL "wrap the
result"); the mini-map hides while the panel is up.
SAY: Back in your Python, a dispatcher matches each call's name, runs the real function with the model's arguments, and wraps the result as a function response.

SHOW: An extra card: "feed the model's call from the staff's run through agent_tools.execute_function_calls,
against this collection", with a PINK tag `stand-in` "a stored chunk's vector replaces Google's
embedding". The TEAL container terminal prints TERM(cli-container/33-x-dispatch-recorded-call.txt: 36,
37–44 folded to `Function calls: [FunctionCall( … name='get_book_by_author' )]`, 45, 48; wrap) (author
masked).
SAY: This part runs without a key: an extra script feeds the staff's recorded call through the tutorial's own dispatcher, against our collection.

SHOW: Line 36 `stand-in embed_func: returns the stored vector of chunk 8440accaceb0ce96-6 (Tolminc Cheese)`
highlights PINK, tag `stand-in`.
SAY: One stand-in: without Google we can't embed the search text, so a stored chunk's vector stands in, and the 10 chunks differ from a real query's.

SHOW: TERM(cli-container/33-x-dispatch-recorded-call.txt: 51–57, …, 135; wrap). V3 runs above a strip:
on the TEAL side the BLUE card's arguments split; PINK `search_content` → a dashed vector glyph
(`stand-in`) → `collection.query(…, n_results=10, where={"author": …})` → ten GREEN chunk cards from
today's story (first words from lines 51, 57, 59: "is ready?” Mara asked", "Anja smiled", "Over the
following hours") → they merge into one GREEN string strip → a TEAL card `{"content": …}` labelled "3,509
characters" (line 135) staples onto the BLUE call card. The cylinder never moves toward the cloud.
SAY: Out come 10 passages from today's story: Mara, Anja, the next step. Joined into one string of 3,509 characters, they're stapled to the call as its response.

SHOW: CODE(cli.py: 464–477) (header `cli.py · lines 464–477`, 12 rows: lines 470–472 shown as one row
`Content(parts=function_responses),`): line 468 GREY "the question", line 469 BLUE "the model's own turn,
unchanged", the `function_responses` row TEAL "your function responses"; line 475 `tools=` GREEN; a GREY
dashed ghost beside line 474 "no tool_config → mode back to automatic".
SAY: Call 2 sends three things: the question, the model's own turn, unchanged, and your function responses. The tools go along again, but no tool config: the mode is back to automatic.

SHOW: LECTURE 39: the duty chip "interpret its outputs" lights. V2's second envelope opens: a full-width
terminal prints TERM(cli-container/33-x-dispatch-recorded-call.txt: 137; wrap, 138–147 folded to `{
"contents": [ { … "role": "user" },`, 148–163, 164–169, 170 cut after `"content": "is ready?” Mara
asked.` + `…"`, 171–175, …, 231–233), tag `built, not sent`. Line 151 `"thoughtSignature":` boxed BLUE,
its value cut to `"AY89a186…",`; the BLUE seal from V3 lands on it. Line 167 `"functionResponse"` TEAL;
line 231 `"generationConfig": {}` GREY.
SAY: Inside, the model's turn carries its thought signature: Gemini's thinking models sign their turn, and want it back exactly as sent. Resending the turn unchanged keeps the seal.

SHOW: PANEL(expected/out-txt-agent-run.txt: 99, 105 cut after "Alpine region,", 111 cut after "cattle
rearing", 112 cut after "(the seasonal movement of livestock)") (header `out.txt · lines 98–111
(excerpt)`, masked, tag `recorded · the staff's run · old book`); "transhumance" highlights YELLOW. Two
GOLD chips: "247 tokens" (`out.txt` line 49, file line 50) and "1,269 tokens" (`out.txt` line 135, file line 136).
SAY: The staff's answer? An Alpine valley, its caves, and transhumance, the seasonal movement of livestock. The two calls used 247 and 1,269 tokens.

SHOW: TRACKER Agents 1 · extra. The lecture tag leaves. A strip (title `laptop · second terminal`): it types
`git show --stat --format='%h %ad %s' --date=short 85bba32; head -4 'input-datasets/books/Tolminc Cheese.txt'`
(extra; folds) → TERM(laptop/09-x-book-changed.txt: 2 cut after "2026-09-22", 4–6). Then an extra card:
"count four of the answer's words in out.txt, today's book, and the book before 85bba32" →
TERM(laptop/10-x-old-words.txt: 2–5); the "book today 0" column highlights RED, the "before 85bba32"
column GREEN.
SAY: But today's book has none of those words: the commit that added this output also rewrote the book. The staff's index was built from the old text.

SHOW: The TEAL cylinder: its cards for the old book turn GREY dashed "old book", today's 24 GREEN cards
slide in. Caption "an index answers from what was loaded · lecture 5".
SAY: Your run on today's book draws on passages like these: Mara, the curd, the wheels. An index answers from what was loaded.

SHOW: An `erratum` README chip (header `README.md · line 266`, tag `expected`): "Displays the LLM's
response"; beside it CODE(cli.py: 478) and a GREEN fix chip `print(response.text)` "just the answer".
SAY: One small slip: the README promises the response, but line 478 prints the whole response object. Print response dot text for just the answer.

SHOW: TRACKER Agents 2. A GREY browser frame (tag `illustration`) at `ac215-llm-rag.dlops.io/agent` with
an empty chat box; a README chip (header `README.md · line 271`, tag `expected`) "Use Chrome browser for
best performance". A strip: it types
`curl -s -o /dev/null -w '%{http_code} %{content_type}\n' https://ac215-llm-rag.dlops.io/agent` (extra;
folds) → TERM(laptop/11-x-hosted-agent.txt: 2), tag `at the time of recording`.
SAY: Step 2 links to the course's hosted Cheese Agent Tool, which was up at the time of recording; the README suggests Chrome.

SHOW: The hook's YELLOW card returns, center: "Who searched your database?" → GREEN "your Python, on your
laptop"; "Who chose the book?" → BLUE "Gemini wrote the call". A GOLD tag "2 Gemini calls per question".
SAY: So, who searched your database? Gemini wrote the call and chose the book; your Python ran it, on your laptop. That's two paid calls per question.

---

## S08 · From two calls to a loop — `s08_loop.py` · `TheLoop`

Lecture: 26, then 35–41.

SHOW: LECTURE 26. No tracker. The mini-map shows, Dynamic Control lit YELLOW. The definition card from
S02 returns, "…until the task is done" underlined. Beside it, llm-rag's run as one short line: BLUE "call
1 · forced tool call" → TEAL "your code runs it" → BLUE "call 2 · answer" → GREY "end". A README chip
(header `README.md · line 246 (excerpt)`, tag `expected`) "AI Agent (Cheese Expert Agent)".
SAY: The lecture's agent runs until the task is done. L-L-M rag's agent ran one lap: a forced tool call, then an answer. The README calls it an agent; by the lecture's definition, it's the smallest piece of one.

SHOW: CODE(cli.py: 474–478) (header `cli.py · lines 474–478`): lines 474–476 highlight with a GREY dashed
ghost "no tool_config"; line 478 GREY. The ponder card sits in the lower third.
SAY: Here's a question about that one lap.
PONDER(8 s, "Call 2 hands the model the tools again, but no tool_config.\nSuppose Gemini answers with another function call.\nWhat does cli.py do?")

SHOW: Line 478 highlights; a BLUE function-call card with no text drops out of the "call 2" box, and the
line ends at "end" with the card unopened (RED outline, "never run"). A GREY dashed arrow loops from the
card back to "your code runs it": caption "a loop would run it and ask again".
SAY: It prints a response whose only part is a function call, with no text, and the program ends. Nothing runs that call; a loop would run it, and ask again.

SHOW: LECTURE 35–40. V4: the BLUE "LLM core" and a GREY "instructions" sheet merge into a hub labelled
"decision maker"; two-way spokes grow to three GREY-outlined nodes "planner", "tools", "memory". Then the
tools spoke unrolls into a circular track: a BLUE station "model" → a PURPLE station "tools" → back to
"model".
SAY: The lecture draws the agent as a hub: the core and its instructions become a decision maker, with spokes to a planner, tools, and memory. Unroll the tools spoke into a loop.

SHOW: A token runs laps on the track; each lap a counter ticks "1/12", "2/12", "3/12". On lap 3 the model
station emits a GREY text card with no function call; a YELLOW gate opens: "final response". Caption
"stop rule: a reply with no function call".
SAY: What ends the loop? The stop rule: a reply with no function call is the final response. The model decides it's done by answering in plain text.

SHOW: CODE(llm-agent-google-adk/4-production-ready/app/runner.py: 39–48) (header
`4-production-ready/app/runner.py · lines 39–48`, a GREY chip "ADK repo · module 4 · code only"): line 40
`async for event in self.runner.run_async(` PURPLE "the Runner streams events"; line 45
`if event.is_final_response():` YELLOW. The track sits above it, labelled PURPLE "inside ADK, simplified:
model → tools, until the reply is final", tag `illustration`.
SAY: In code you see the loop from outside: the ADK Runner streams events, this wrapper keeps the final response, and the loop runs inside the library.

SHOW: Two code chips: CODE(colab/cheese-quiz/cell-71.py: 5–7) (header `Cheese Quiz · cell 71 · lines
5–7`) `max_turns=12` and CODE(colab/cheese-newsletter/cell-25.py: 8) (header `Cheese Newsletter · cell 25
· line 8`) `"max_iterations": 16`. Replay on the track: the counter hits 12/12 and a RED gate
`MaxTurnsExceeded` slams down.
SAY: You also cap it, in case it never stops: 12 turns in the Cheese Quiz Guild, 16 iterations in the newsletter. Hitting the Agents SDK cap ends the run with an error.

SHOW: LECTURE 41. The anatomy (V1) full size: the four configurable blocks light GREY one by one as named
("LLM core", "instructions", "tools", "memory"); Dynamic Control is GREY dashed (slide 41 grays it out);
then it fills PURPLE, caption "the framework writes this part".
SAY: The lecture's building blocks gray out dynamic control. You configure the model, instructions, tools and memory; the loop is the block a framework writes for you.

SHOW: TRACKER Run 3 · extra. The TEAL container terminal returns (8 rows): it types `exit` (extra) →
TERM(laptop/06-docker-shell.txt: 42; session); the frame turns GREY, title `laptop`, prompt
`student@laptop:~/AC215/llm-rag$`. It types `docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'`
(extra; folds) → TERM(laptop/12-x-ps-after-exit.txt: 2–3); the row `llm-rag-chromadb … 0.0.0.0:8000->8000/tcp`
highlights PINK "still up". It types `docker compose down` (extra) → TERM(laptop/13-x-compose-down.txt:
2–3 joined, 4–7); lines 2–4 GREY "harmless".
SAY: Before part 2, tear down. After exit, an extra docker ps shows Chroma still up, on port 8000. Then docker compose down: two harmless warnings, and it stops.

SHOW: `▶ your turn` on a static GREY card "exit · docker compose down". Hold 2 s. A PINK chip "port 8000 →
free for part 2"; a GREEN chip "docker-volumes/: your index stays". Then everything fades to an empty frame
(end of part 1).
SAY: Your index stays on disk, and part 2's web server wants port 8000 too. Pause and tear down. In part 2, a framework runs this loop for us.

---

## S09 · ADK: clone, configure, and a sync that fails — `s09_adk_setup.py` · `AdkSetup`

Lecture: 35 (the model-line beat only).

SHOW: A new picture: the GREY laptop with a GREY dashed "no Docker this time" chip, a PURPLE uv glyph and
an empty `.venv` box; across a dashed boundary, a BLUE chip "Gemini API", reached with a GOLD key "AI
Studio key". Below it a terminal (full width, title `laptop`, prompt `student@laptop:~/AC215$`) fades in.
SAY: Part 2: frameworks own the loop. No Docker this time: Google's Agent Development Kit runs in a uv environment on your laptop, and calls Gemini with an AI Studio key.

SHOW: TRACKER Start 1. A README chip (header `README.md · line 77`, tag `expected`): `git clone
<repository-url>`. It types `git clone https://github.com/dlops-io/llm-agent-google-adk.git` →
TERM(adk-laptop/01-clone.txt: 2); a GREY caption "the README's placeholder, filled in". TRACKER Start 2:
it types `cd google-adk-tutorial` → TERM(adk-laptop/02-cd-as-written.txt: 2), RED, tag `erratum`.
SAY: Step 1: clone; the README writes a placeholder for the address. Step 2 says cd google ADK tutorial, but no such folder exists.

SHOW: It types `cd llm-agent-google-adk` → (no output); the prompt becomes
`student@laptop:~/AC215/llm-agent-google-adk$`; the folder name flashes GREEN "named after the repo".
SAY: A small slip: the folder is named after the repo. Type cd L-L-M agent google ADK instead.

SHOW: TRACKER Start 2 · extra. It types `ls -a` (extra) → TERM(adk-laptop/04-x-ls.txt: 2–4). The six
module folders `1-baseline` … `6-rag` highlight GREY, `pyproject.toml` GREEN; a GREY dashed ghost chip
`uv.lock` "git-ignored · .gitignore line 34".
SAY: An extra ls shows six numbered module folders, but no lock file: the repo ignores it, so everyone resolves fresh versions.

SHOW: TRACKER Start 3. It types `cp .env.example .env` → (no output). TRACKER Start 3 · extra: it types
`grep -v '^#' .env | grep .` (extra) → TERM(adk-laptop/06-x-env-file.txt: 2–5). Line 2
`GOOGLE_API_KEY=your_google_ai_api_key_here` GREY "placeholder"; line 4 `GEMINI_MODEL=gemini-2.5-flash`
YELLOW.
SAY: Step 3: copy dot env dot example to dot env. An extra grep shows a placeholder Google API key, and the model, Gemini 2.5 Flash.

SHOW: TRACKER Start 4, then Start 5. The terminal shrinks to a strip. A GREY browser frame (tag
`illustration`) "Google AI Studio · API keys" with a button "Create API key"; a GOLD key glyph comes out
(never its content). A GREY file card (header `.env · your copy · git-ignored`) shows `GOOGLE_API_KEY=`
and the GOLD key glyph slots in after `=`. A GREY note "README: the key's source is the next step;
paste it here".
SAY: Step 4: create a key in Google AI Studio and paste it into dot env, after Google API key equals.

SHOW: LECTURE 35 (this beat only; it leaves with the next). On the `.env` card, the `GEMINI_MODEL=` line highlights YELLOW; `gemini-2.5-flash` slides out and
`gemini-3.1-flash-lite` slides in, GREEN, tag "your edit · the model llm-rag uses (cli.py · line 27)".
SAY: Also change the model line. Choosing the LLM core is the lecture's first design decision, and here it's one line: a current model, like Gemini 3.1 Flash-Lite.

SHOW: Two GREY chips under the card: "the code's fallback: gemini-2.0-flash (`1-baseline/agent.py · line
12`) · shut down" and "gemini-2.5-flash · limited to earlier users", tag "Google's model pages, checked
October 18, 2026"; an `erratum` tag on both. A GREY dashed card: "module .env.example files · don't copy
them: only the nearest .env is loaded". `▶ your turn` on a static GREY card "cp .env.example .env ·
GOOGLE_API_KEY=<your key> · GEMINI_MODEL=gemini-3.1-flash-lite". Hold 2 s.
SAY: Google lists the code's fallback, Gemini 2.0 Flash, as shut down, and limits 2.5 Flash to earlier users. Keep everything in this root file: only the nearest dot env is loaded. Pause, and set up yours.

SHOW: CODE(llm-agent-google-adk/pyproject.toml: 8–19) (header `pyproject.toml · lines 8–19`): line 8
`requires-python = ">=3.10"` GREEN; line 10 `"google-adk>=1.8.0",` YELLOW "no upper bound"; lines 18–19
`chromadb`, `sentence-transformers` GREY "→ onnxruntime, PyTorch".
SAY: The project file asks for Python 3.10 or newer, and ADK 1.8 or newer, with no upper bound, plus Chroma and sentence transformers.

SHOW: V5: L01's number line `3.10 … 3.16` slides in above the strip; the interval `>=3.10` glows GREEN to
the right edge; no ORANGE dot anywhere; a GREY chip "no python3 on PATH" (excerpt of
`adk-laptop/00-x-env.txt` line 9). The ponder card sits in the lower third.
SAY: One more fact: this laptop has no Python at all.
PONDER(6 s, "This laptop has no Python at all.\nThe project asks for 3.10 or newer.\nWhich Python will uv sync use?")

SHOW: TRACKER Start 6. The terminal grows (12 rows). It types `uv sync` → TERM(adk-laptop/07-uv-sync.txt:
2–4). On the number line a PURPLE download arrow drops `CPython 3.15.0` at the newest end (tag `at the
time of recording`).
SAY: Step 6: uv sync. As in lecture 1, with no Python around, uv downloads the newest: CPython 3.15.0, at the time of recording.

SHOW: TERM(adk-laptop/07-uv-sync.txt: 5–7 joined, 9–11 joined; wrap), RED. V5: a shelf of wheels for
`onnxruntime 1.31.0` (a GREY arrow from `chromadb`, `pyproject.toml · line 18`) shows tags `cp311 cp312
cp313 cp313t cp314 cp314t`; the 3.15 slot is empty and turns RED.
SAY: It resolves 189 packages, then fails. O-N-N-X runtime, which Chroma pulls in, has wheels only up to Python 3.14.

SHOW: An `erratum` tag on the tracker's step 6: "fails on a fresh laptop today"; a GREY dashed note "a
laptop where uv finds Python 3.10–3.14 first may get through · reasoned, not captured". TRACKER Start 6 ·
extra: it types `uv python pin 3.13` (extra) → TERM(adk-laptop/09-x-python-pin.txt: 2), tag `fix · not in
the README`. V5: the interval collapses to the point 3.13; the `cp313` wheel clicks in, GREEN; a GREEN
file card `.python-version` "3.13" drops into the repo.
SAY: So step 6 fails on a fresh laptop today; one with an older Python may get through. Pin anyway, so every laptop builds the same environment, with an extra command: uv python pin 3.13.

SHOW: TRACKER Start 6. It types `uv sync` → TERM(adk-laptop/12-uv-sync.txt: 2–4, …, 38, …, 89, …, 155)
(never lines 5–7 or 140); `google-adk==2.12.0` and `onnxruntime==1.31.0` highlight GREEN. A GREY chip
"about 1.6 GB (`uv pip list`, extra) · on a Linux PC about 3 GB more of CUDA packages · a Mac: none"
(from `adk-laptop/14` line 12 and `10`).
SAY: Then uv sync again: CPython 3.13 this time, and it installs, ADK 2.12.0 included. PyTorch makes it big: about 1.6 gigabytes, plus about 3 of CUDA packages on a Linux PC.

SHOW: TRACKER Start 6 · extra. It types `uv run adk --version` (extra) →
TERM(adk-laptop/13-x-adk-version.txt: 2), tag `at the time of recording`. `▶ your turn` on a static GREY
card "cd llm-agent-google-adk · cp .env.example .env · key + GEMINI_MODEL in .env · uv python pin 3.13 ·
uv sync". Hold 2 s.
SAY: An extra check, uv run ADK dash dash version, says 2.12.0, at the time of recording. Pause, and get your sync to succeed.

---

## S10 · adk web and the folder names — `s10_adk_web.py` · `AdkWeb`

Lecture: none.

SHOW: TRACKER RunAg 1. Terminal (full width, 12 rows), prompt `student@laptop:~/AC215/llm-agent-google-adk$`.
It types `uv run adk web` → TERM(adk-laptop/15-adk-web.txt: 2–3 joined, 10–11 joined, 13 cut after
"[Y/n]:"; wrap). A tag `erratum` "not in the README".
SAY: Running agents, step 1, from the repository root: uv run ADK web. First, version 2.12 asks a question the README doesn't mention: may Google collect usage data?

SHOW: "This is OFF by default." underlines GREY; `[Y/n]` is boxed YELLOW with a tag "Enter = yes". After
a 0.6 s pause the terminal types `n` (as the capture did), and a GREY chip appears: "`adk telemetry
disable` · change it later".
SAY: The text says telemetry is off by default, but the capital Y means pressing enter answers yes. Answer as you like; the telemetry disable command changes it later.

SHOW: TERM(adk-laptop/15-adk-web.txt: 34–38, 41); line 41 `Uvicorn running on http://127.0.0.1:8000`
PINK. TRACKER RunAg 2: the terminal shrinks to a strip; a GREY browser frame (tag `illustration`) opens
at `localhost:8000`, and its address bar changes to `localhost:8000/dev-ui/`. A second strip (title
`laptop · second terminal`): it types `curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n'
http://localhost:8000/` (extra; folds) → TERM(adk-laptop/16-x-dev-ui.txt: 2).
SAY: Then the server starts, on port 8000. Step 2: open localhost 8000 in your browser; an extra curl shows the redirect to the dev UI.

SHOW: In the browser, a schematic agent dropdown opens listing the seven entries of
TERM(adk-laptop/17-x-list-apps.txt: 2) (the strip shows the extra `curl -s http://localhost:8000/list-apps; echo`
and its line). The cursor picks `1-baseline`; a RED banner in the page shows the `detail` text of
TERM(adk-laptop/18-x-select-1-baseline.txt: 2; wrap); the server strip shows `15` lines 44–45 joined
(`… "GET /dev/apps/1-baseline/build_graph HTTP/1.1" 404 Not Found`).
SAY: The agent dropdown lists 7 entries, nested ones included. Pick 1 baseline, as its README says, and the page refuses: agent names must be valid Python identifiers.

SHOW: Why, as a picture (tag `illustration`): a GREY folder `1-baseline/` holding `agent.py`; a PURPLE
arrow labelled `adk web` turns it into the Python line `import 1-baseline.agent` → `root_agent`; the `1`
and the `-` flash RED, with a RED chip "SyntaxError · a module name can't start with a digit or hold a
hyphen". A GREY tag "ADK 2.12 checks the name first".
SAY: Why? The web server imports each folder as a Python module, folder dot agent, and reads its root agent. A module name can't start with a digit or contain a hyphen, so newer versions check the name first.

SHOW: A RED dashed frame `what if · just watch`: it types `uv add "google-adk>=1.8.0,<1.28"` (extra) →
TERM(adk-laptop/21-x-uv-add-pin.txt: 7–8); a strip shows TERM(adk-laptop/25-x-list-apps-pinned.txt: 2)
(four folders, GREEN), then TERM(adk-laptop/24-x-adk-web-pinned.txt: 131, 132–134 joined cut after
"underscores."; wrap) RED. It types `git checkout pyproject.toml; uv sync --upgrade-package google-adk`
(extra) → TERM(adk-laptop/27-x-undo-pin.txt: 8–9). The frame closes; caption "back in your terminal".
SAY: An older version, 1.27.5, lists only the four folders, but picking one still fails, as an invalid app name. So a version pin doesn't help; undo it.

SHOW: TRACKER RunAg 1 · extra. In the viewer's terminal, it types
`mv 1-baseline baseline; mv 3-mcp-tools mcp_tools; mv 5-custom-agent custom_agent; ls` (extra; folds) →
TERM(adk-laptop/28-x-rename.txt: 2–12); `baseline`, `custom_agent`, `mcp_tools` highlight GREEN; tag
`fix · not in the README`.
SAY: What works is renaming, which isn't in the README either: 1 baseline becomes baseline, 3 MCP tools becomes MCP underscore tools, and 5 custom agent becomes custom underscore agent.

SHOW: It types `uv run adk web` → TERM(adk-laptop/29-x-adk-web-renamed.txt: 36–37 joined, 38–39 joined,
40; wrap); in the first line `…/llm-agent-google-adk/.env` highlights PINK "the root .env". The browser's
dropdown now lists the entries of TERM(adk-laptop/30-x-list-apps-renamed.txt: 2) (extra strip `curl -s
http://localhost:8000/list-apps; echo`); `baseline` is picked, GREEN.
SAY: Start the web server again, and pick baseline. The log says it loaded the dot env file at the repository root, and found the root agent in baseline dot agent.

SHOW: A GREY chip "git status: 3 folders deleted, 3 new · fine for your copy (S16)". Two `erratum` chips
write in: (a) a README chip (header `QUICKSTART.md · line 24`, tag `expected`) `uv run adk web
1-baseline/agent.py` → the line of TERM(adk-laptop/19-x-quickstart-file.txt: 5) RED; (b) a README chip
(header `2-litellm/README.md · line 74`, tag `expected`) `uv run adk` → TERM(adk-laptop/20-x-adk-without-web.txt: 2)
"prints help · starts nothing".
SAY: Git now sees deleted and new folders, which is fine. Two more slips: the quick start passes a file where a folder is expected, and the module READMEs drop the word web, so it only prints help.

SHOW: A RED dashed frame `what if · just watch`, captioned "llm-rag's Chroma still on port 8000":
TERM(adk-laptop/36-x-port-8000-busy.txt: 21; wrap) RED; then it types `uv run adk web --port 8080`
(extra) → TERM(adk-laptop/37-x-adk-web-port-8080.txt: 34). Back in the viewer's terminal, `▶ your turn`
on a static GREY card "rename the three folders · uv run adk web · localhost:8000 · pick baseline". Hold
2 s.
SAY: And if L-L-M rag's Chroma still holds port 8000, the server stops: address already in use. Run docker compose down, or add dash dash port 8080. Pause, and get the dev UI open on baseline.

---

## S11 · Runner, session, state: the shared whiteboard — `s11_state.py` · `SharedState`

Lecture: 40–41 (and 20–22).

SHOW: TRACKER Base 1. CODE(llm-agent-google-adk/1-baseline/agent.py: 14–19) (header `1-baseline/agent.py ·
lines 14–19`, subtitle "your copy: baseline/agent.py"), then Transform to lines 21–26. LECTURE 40–41: the
mini-map grows to the right third and labels the constructor's arguments with slide 41's blocks:
`model=` → LLM core (BLUE), `instruction=` → Instructions, `tools=` → a GREY dashed "none here",
`output_key=` → Memory "within one session".
SAY: You picked three LLM agents, each with a model, an instruction, and an output key. In the lecture's blocks: the LLM core, the instructions, and no tools at all.

SHOW: CODE(llm-agent-google-adk/1-baseline/agent.py: 28–39) (header `1-baseline/agent.py · lines 28–39`); lines 35–39
`SequentialAgent(…)` highlight PURPLE, and the mini-map's Dynamic Control fills PURPLE "Runner +
SequentialAgent". Then an extra card: "ask the server for the agent tree the UI loads", and a full-width
terminal prints TERM(adk-laptop/31-x-select-baseline.txt: 2–5; each line cut after its instruction's
first sentence); `model gemini-2.5-flash` highlights YELLOW "from your root .env · set yours (S09)".
SAY: A sequential agent runs them in order: validator, planner, summarizer. An extra request shows the tree the UI loads, with the model from your root dot env; set yours.

SHOW: TRACKER Base 1 · extra. It types `curl -s -X POST http://localhost:8000/apps/baseline/users/student/sessions; echo`
(extra; folds) → TERM(adk-laptop/32-x-new-session.txt: 2; wrap); `"state":{}` and `"events":[]` highlight
GREEN; the id gets `your numbers will differ`. V6 starts above a strip: a GREEN whiteboard with three
empty cells `itinerary_validation`, `travel_plan`, `trip_summary`, and an empty events column beside it.
SAY: Another extra request creates a session: an empty state, and no events yet. Think of the state as a shared whiteboard.

SHOW: V6, captioned throughout "what ADK does once you add your key · no model output was recorded", tag
`illustration`. A PURPLE Runner takes a GREY message card; `ItineraryValidator` (a BLUE model chip and its
instruction card) answers, and its reply (a blank GREEN card, no text) flies into cell 1 along a label
`output_key`; an event block stacks in the column. `TravelPlanner`'s instruction card shows
`Using {itinerary_validation}, …` with a PINK hole; cell 1's card flies into the hole before its BLUE chip
lights; its reply fills cell 2.
SAY: Once you add your key, the Runner does this. The validator's reply goes into the state, under its output key; before the planner runs, its instruction's placeholder is filled from that cell.

SHOW: `TripSummarizer` reads `{travel_plan}` the same way and fills cell 3; three event blocks stand in
the column, labelled "the Events tab". Between the agents, a GREY crossed-out arrow "no messages". A GREY
dashed coda (tag `concept · module README only`): `ParallelAgent` fills three cells at once on three
branch lines.
SAY: The summarizer reads the plan the same way. The agents never message each other: the whiteboard carries the data, and every step is an event. A parallel agent would fill its cells at once, on separate branches.

SHOW: LECTURE 20–22. The lecture's Paris request card (from S01) appears beside the pipeline; its "live
systems" and "tools that act" chips find nothing to attach to: `tools=` stays a GREY dashed "none".
Caption "costs: the model's own estimates".
SAY: The lecture's planner calls live systems; this pipeline has no tools, so its prices are the model's guesses. A later notebook fixes exactly that.

SHOW: LECTURE 40–41. A README chip (header `README.md · line 140 (excerpt)`, tag `expected`): "Memory:
Structured state tied to a session_id"; beside it a GREEN box "session state · one session" (the
whiteboard) and a GREY dashed box "memory across sessions · the lecture's sense · not in today's runs".
SAY: The ADK README calls this state memory. The code calls it session state, and it lasts one session; the lecture's memory remembers you next time, which none of today's runs does.

SHOW: An extra card: "send a trip request with the placeholder key (POST /run)" →
TERM(adk-laptop/33-x-send-placeholder-key.txt: 2) `Internal Server Error`; the server strip shows
TERM(adk-laptop/29-x-adk-web-renamed.txt: 357–363 joined, cut after "Please pass a valid API key.";
wrap) RED; tag `real run · placeholder key`.
SAY: Without a real key, a trip request gets an internal server error. The server log says why: API key not valid. The placeholder reached Google, and was refused.

SHOW: A GREY "with your key, look for" card, items writing in as named: "three replies, in order", "State
tab: itinerary_validation · travel_plan · trip_summary". PANEL(adk-laptop/29-x-adk-web-renamed.txt: 41–42
joined, "adk web log") with `baseline/.adk/session.db` highlighted PINK "a file in the agent's folder". A
GOLD tag "3 Gemini calls per request". `▶ your turn` on a static GREY card "pick baseline · send a trip
request". Hold 2 s.
SAY: With your key, look for three replies in order, and three new keys in the State tab; the session is a file in the agent's folder. Each request is three paid calls: pause, and plan a trip.

---

## S12 · Tools you didn't write: MCP — `s12_mcp.py` · `McpPlugs`

Lecture: 51–53.

SHOW: LECTURE 51. No tracker. Three bins write in (slide 51, our words): "data · fetch", "action · change
something", "orchestration · hand work to an agent". Tool chips drop in as named: `get_book_by_author`,
`web_search`, `read_file` → data; `finalize_itinerary`, `send_email` → action (GREY tags "S14", "S15");
`research_facts`, `researcher_agent` → orchestration.
SAY: The lecture sorts tools into three families. Data tools fetch, like our book searches; action tools change something, like finalizing a trip or sending email; orchestration tools hand work to another agent.

SHOW: LECTURE 52. One agent box with four tool pills; ten GREY wires fan out to ten service boxes, each
with its own protocol label (our redrawing: "email · SMTP", "calendar · CalDAV", "database · SQL", "drive
· API", …). A GREY caption "Do you see a problem?". After the SAY, 5 s of silence (`self.wait(5)`), no
timer.
SAY: Now wire one agent to ten services, each with its own protocol. The lecture asks: do you see a problem?

SHOW: LECTURE 53. Morph: the agent box becomes "MCP host" with small "client" ports; the ten wires merge
into one PINK trunk labelled "same protocol" (never a box); an "MCP server" adapter clicks onto each
service.
SAY: Every tool becomes a custom integration. MCP, the Model Context Protocol, makes it one pattern: a host with clients, and an MCP server for each service.

SHOW: The trunk splits into three separate PINK plugs, each its own connection: "stdio · a child
process", "HTTPS · a remote URL", "HTTP · a thread on :8001". Caption "one protocol · one connection per
server". The lecture tag stays.
SAY: That MCP box is a shared protocol, not a program you run. In code, each server is its own plug, and the tutorial has three.

SHOW: TRACKER Mcp 1. A README card (header `3-mcp-tools/README.md · lines 56–63`, tag `expected`), not
typed: `brew install node` (macOS) · `sudo apt install nodejs npm` (Ubuntu) · "Windows: nodejs.org". A
terminal strip (ADK laptop): it types `node --version; npx --version` (extra) →
TERM(adk-laptop/34-x-node.txt: 2–3), tag `at the time of recording`. Then
CODE(llm-agent-google-adk/3-mcp-tools/agent.py: 20–29) (header `3-mcp-tools/agent.py · lines 20–29`,
subtitle "your copy: mcp_tools/agent.py"): lines 23–24 PURPLE, line 28 `tool_filter` YELLOW. The picture:
a PINK stdio pipe from a PURPLE ADK process into a PURPLE `npx … server-filesystem` child process on the
GREY laptop.
SAY: Plug 1 is in the ADK module on MCP. Install Node, and the agent's toolset starts a filesystem server with npx, as a child process, talking over standard input and output.

SHOW: An extra card: "ask the agent's own toolset for its tools · no model involved" →
TERM(adk-laptop/35-x-mcp-toolset.txt: 21, 30, 31 cut after "14 [" + `…]`, 32–37). V7: 14 GREY tool chips
fall onto a sieve labelled `tool_filter`; `list_directory`, `read_file`, `search_files` pass GREEN,
`write_file` and `edit_file` bounce off. TRACKER Mcp 2: a GREY "with your key, ask:" card "List files in
this directory → look for a list_directory call in the events".
SAY: An extra script asks that toolset for its tools, no model involved: the server offers 14, including write and edit, and the filter lets three through. With your key, ask the agent to list files.

SHOW: TRACKER CQ-Tools 1, then CQ-Tools 2. A BLUE Colab frame. RECORDED(expected/colab-cheese-quiz-c50-tools-called.txt:
3–6) small (tool name masked), caption "step 1: a Python function with @function_tool (cell 48)". Then
CODE(colab/cheese-quiz/cell-54.py: 2, 10–18, 26–27) (header `Cheese Quiz · cell 54 · lines 2–27
(folded)`, URL masked to `https://‹instructor›-fun-facts.dlops.io/mcp`): `MCPServerStreamableHttp(` and
`params={"url": …}` PINK; line 27 `mcp_servers=mcp_servers,` YELLOW "not tools=". The picture: a PINK
HTTPS line from the BLUE Colab VM to a BLUE remote server box.
SAY: Plug 2 is in the Cheese Quiz. After a first tool written as a plain function, the notebook connects to a remote MCP server by URL, passed as MCP servers, not tools.

SHOW: Four extra cards in a row, each followed by its output in a terminal strip (from the ADK laptop):
"a browser's plain GET" → TERM(mcp-remote/01-x-browser-get.txt: 2, 10; wrap) `HTTP/2 406` and
"…Client must accept text/event-stream" RED; "initialize" → excerpt chips of `02` line 3
`"protocolVersion":"2025-06-18"` and `"serverInfo":{"name":"‹instructor› Cheese MCP","version":"1.16.0"}`;
"tools/list" → an excerpt chip of `03` line 3 `"name":"‹instructor›_fun_fact_mcp"`; "tools/call" →
excerpt chips of `04` line 3, the `"structuredContent":{"fact":…}` text as in the file, and
`"isError":false`, tag `your numbers will differ` "a new fact each call". A small envelope travels the
HTTPS line for each.
SAY: Extra curl commands talk to that server. A browser's plain request gets 406: the server is up, but speaks MCP, not web pages. Then initialize, list tools, call: one tool, one cheese fact per call.

SHOW: TRACKER CQ-Tools 3. CODE(colab/cheese-quiz/cell-57.py: 2–9, 14) (header `Cheese Quiz · cell 57 ·
lines 2–14 (folded)`, names masked): line 14 `port=8001` GREEN; an `erratum` chip on line 11 "the
comment says port 8000"; beside it RECORDED(expected/colab-cheese-quiz-c57-fastmcp-server.txt: 3)
`…127.0.0.1:8000/mcp`, GREY tag "saved from an older version of the cell". Then
RECORDED(expected/colab-cheese-quiz-c59-local-mcp.txt: 3–10): `"POST /mcp HTTP/1.1" 200 OK` lines
interleaved with `‹instructor› Fun Fact Tool Called`. The picture: a PURPLE FastMCP thread on
`127.0.0.1:8001` inside the BLUE Colab VM.
SAY: Plug 3: the notebook runs its own FastMCP server, in a thread, on port 8001. A small slip: the comment above says 8000, and so does an older saved output.

SHOW: The three plugs side by side; in each, the BLUE model chip only emits a BLUE call card, while a
PURPLE client process does all the talking along the PINK lines. A GOLD tag "OpenAI calls · paid".
`▶ your turn` on a static GREY card "node --version · Cheese Quiz: Tools, MCP (cells 45–59)". Hold 2 s.
SAY: Notice who does the talking: your client process. MCP gives the model no network access; it still only writes calls. Pause, and run the MCP cells.

---

## S13 · Many agents: who plans the order? — `s13_many.py` · `ManyAgents`

Lecture: 44–49 (and 38).

SHOW: LECTURE 44–49. A GREY dashed tree (our redrawing, tag `concept · lecture example`): "lead agent" →
"planner" → three parallel "web search" agents → "synthesis" → "report". Beside it, two tutorial trees in
the series colours: the Cheese Quiz Guild (a BLUE orchestrator over the specialists' tool chips
`research_facts`, `vegan_specialist`, `write_quiz`, `review_quiz`, `format_quiz_json`) and the Cheese
Newsletter (an orchestrator over `researcher_agent`, `editor_agent`, `send_email`).
SAY: The lecture's deep research example is a tree of agents: a lead agent, a planner, parallel web searchers, and a synthesis into a report. The tutorial builds trees like it: the Cheese Quiz Guild, and the newsletter.

SHOW: LECTURE 38. A YELLOW question writes in over all three: "Who plans the order?" Three empty slots
below it: "the code", "the model", "Python reading the model's label". Slot 1 fills:
CODE(llm-agent-google-adk/1-baseline/agent.py: 35–39) (header `1-baseline/agent.py · lines 35–39`) and an
assembly line of three GREY stations.
SAY: The lecture's planner raises the question that sorts them: who plans the order? First answer: the code. The sequential agent you just ran is an assembly line, its order fixed in Python.

SHOW: TRACKER CQ-Guild 1, then CQ-Guild 2. Slot 2: CODE(colab/cheese-quiz/cell-68.py: 1–8) (header
`Cheese Quiz · cell 68 · lines 1–8`): `.as_tool(` highlights on each line; a whole agent shrinks into one
tool chip, which drops into S12's "orchestration" bin.
SAY: Second answer: the model. In the Guild, each specialist, from the fact finder to the critic, becomes a tool: a whole agent behind one function. An orchestrator decides which to call.

SHOW: CODE(colab/cheese-quiz/cell-70.py: 3–11) (header `Cheese Quiz · cell 70 · lines 3–11`): "Follow the
assembly line strictly" and "(Make at most 2 total review rounds.)" highlight YELLOW with a GREY tag "a
rule in prose · no code enforces it". A chip CODE(colab/cheese-quiz/cell-71.py: 6) `orchestrator, prompt,
max_turns=12` GREEN.
SAY: Its instructions say: follow the assembly line strictly, at most 2 review rounds. That's a rule in prose; no code enforces it, except a cap of 12 turns.

SHOW: TRACKER CQ-Guild 3. RECORDED(expected/colab-cheese-quiz-c75-guild-star-wars.txt: 3–5, 7, 13) (the
display line as a GREY label "a quiz widget", then the first question's text): three RED
`ERROR:openai.agents:Error getting response` lines, then a GREY tag "a quiz anyway". In the Guild tree,
three hops flash RED and the orchestrator routes around them; GOLD ticks on every hop, a GOLD tag "hosted web search · paid". `▶ your turn` on a static GREY card "Cheese Quiz Guild: cells 60–77". Hold 2 s.
SAY: The staff's saved run logged three errors getting a response, and still produced a quiz: the orchestrator worked around failed calls. Every hop adds cost, time, and a way to fail; pause, and run the Guild.

SHOW: Slot 3: CODE(llm-agent-google-adk/5-custom-agent/conditional_agent.py: 84–94), then 94–102 (header
`5-custom-agent/conditional_agent.py · lines 84–102`, ≤ 12 lines at a time); line 85
`complexity = ctx.session.state.get("query_complexity", "simple")` PINK; lines 89, 94, 99, the three
branches, YELLOW. A small GREY chip "classifier: output_key="query_complexity" (line 171)". The ponder
card sits in the lower third.
SAY: Third answer: Python, reading the model's label. In this custom agent, a classifier writes one word into the state, and plain if statements pick the handler.
PONDER(6 s, "The classifier answers \"Simple\", with a capital S.\nWhich handler runs?")

SHOW: Line 89 `if complexity == "simple":` gets a RED cross against "Simple"; line 94 a RED cross; line 99
`else:  # ambiguous` lights → "clarification handler". A GREEN fix chip `complexity.strip().lower()` ·
"or a structured output (exercises)".
SAY: The else branch: clarification. The comparison is exact; lowercase the label first, or ask for structured output. The exercises try both.

SHOW: A GREY dashed chip "handoffs" (tag `concept · lecture only`) slides into S12's orchestration bin,
with a GREY note "lecture 7". Fade out.
SAY: The lecture also lists handoffs among the orchestration tools. These tutorials use agents as tools; lecture 7 shows handoffs.

---

## S14 · The harness: only a human says yes — `s14_approval.py` · `ApprovalGate`

Lecture: 20–22, then 36–37.

SHOW: TRACKER TP 1 → 3. A BLUE Colab frame (title "Travel Planner", tag `illustration`).
CODE(colab/travel-planner/cell-08.py: 2) `%pip install -q "openai-agents==0.3.2"` GREEN "pinned". LECTURE
20–22: the Paris request card (from S01) shrinks into a small GREY box "mock catalog": "3 cities · 6
hotels · prices in cents" (a folded chip of CODE(colab/travel-planner/cell-12.py: 6–18)) and "5 search
tools + finalize" (CODE(colab/travel-planner/cell-21.py: 28–34)). A GREY chip: excerpt of
RECORDED(expected/colab-travel-planner-c27-turn4-yes.txt: 5) "Nothing has been booked."
SAY: The Travel Planner notebook rehearses the lecture's trip. Copy it, add your key, and install its pinned agents package. Paris shrinks to a mock catalog: 3 cities, 6 hotels, 5 search tools and a finalize tool, booking nothing.

SHOW: TRACKER TP 4 → 6. Three compact turn cards (tag `recorded · the staff's last saved run`): Turn 1
RECORDED(expected/colab-travel-planner-c24-turn1.txt: 3, 4 cut after "Los Angeles?"); Turn 2 the five
`[tool]` lines of RECORDED(expected/colab-travel-planner-c25-turn2.txt: 3, 31, 59, 73, 87) counted 1–5,
then line 109 `Kind: options`; Turn 3 RECORDED(expected/colab-travel-planner-c26-turn3.txt: 3–5).
SAY: In the staff's saved run, turn 1 asks which California city. Turn 2 runs five searches and offers options. In turn 3 the user picks, the model calls finalize, and the reply asks: here's the exact plan; reply yes to approve.

SHOW: V8: a GREEN plan card (RECORDED(c26: 6–19), the exact proposal JSON, small) walks toward a door
marked FINAL; a turnstile stops it and stamps it YELLOW `PENDING`. CODE(colab/travel-planner/cell-15.py:
33–42) (header `Travel Planner · cell 15 · lines 33–42`, subtitle "Finalize Plan Tool"): lines 36–42
highlight. The BLUE model pushes the card again in the same turn: the same stamp.
SAY: That's the gate. A finalize call from the model can only propose: if the plan isn't the approved one, the code stores it as pending, and returns needs confirmation.

SHOW: CODE(colab/travel-planner/cell-18.py: 55–65) (header `Travel Planner · cell 18 · lines 55–65`,
subtitle "Business Logic"): lines 59–61 highlight. A GREY hand glyph "the human's next message". The
ponder card sits in the lower third.
SAY: Approval lives in a separate function, apply confirmation. It reads the human's next message, and only an explicit yes copies pending to approved.
PONDER(8 s, "In turn 3 the model got needs_confirmation.\nWhy can't it just call finalize_itinerary again\nto approve its own plan?")

SHOW: CODE(colab/travel-planner/cell-18.py: 105–109) (header `Travel Planner · cell 18 · lines 105–109`):
line 106 `apply_confirmation(prompt, context)` before line 109 `reply = await invoke_agent(…)`, a GREY
arrow "runs first". On the turnstile the PENDING stamp stays on every push.
SAY: Because apply confirmation runs on the human's message, before the agent starts. Inside turn 3, nothing is approved, so every retry gets the same stamp.

SHOW: TRACKER TP 7. A GREY human hand types "yes" (CODE(colab/travel-planner/cell-27.py: 2)); the stamp
flips GREEN `APPROVED`; the turnstile turns; a calculator glyph builds the budget line by line from
RECORDED(expected/colab-travel-planner-c27-turn4-yes.txt: 25–34): 880 + 1,000 + 600 + 150 + 60 = 2,690 of
6,000; `"total_usd": 2690.0` GREEN. A chip CODE(colab/travel-planner/cell-27.py: 6) "the notebook's own
test".
SAY: Turn 4: the human types yes. The stamp flips to approved, finalize runs, and Python builds the budget line by line: 2,690 dollars out of 6,000. The notebook's own test checks Python's number.

SHOW: CODE(colab/travel-planner/cell-18.py: 122–135) folded to 122–123, 126, 128–131, 133–135 (header
`Travel Planner · cell 18 · lines 122–135 (folded)`): lines 129–131 RED "hard guardrail: raise"; lines
133–135 YELLOW "soft guardrail: warn".
SAY: What you see is rendered from checked state. An itinerary that skipped the check raises an error, a hard guardrail; a dollar amount in the model's prose only prints a warning, a soft one.

SHOW: LECTURE 36–37. Two GREY sticky notes on a prompt card (slides 36–37, our words): "success
criteria", "guardrails"; each gets a GREEN copy in code: "approval gate", "Python's budget", "checked
render". From S12's bins, `finalize_itinerary` lights in "action". TRACKER TP 8: a GREY chip "chat loop ·
exercises". A GOLD tag "OpenAI calls · every turn". `▶ your turn` on a static GREY card "Travel Planner:
install · define tools · turns 1–4". Hold 2 s.
SAY: The lecture puts success criteria and guardrails in the instructions. This notebook keeps a copy in code the model can't talk its way past, on the action tool. Every turn is paid; pause, and run the four turns.

---

## S15 · The harness: success is a receipt — `s15_receipt.py` · `Receipt`

Lecture: 36–37 (and 10–12).

SHOW: TRACKER NL 1 → 3. A BLUE Colab frame (title "Cheese Newsletter · Harness", tag `illustration`). A
small chip CODE(colab/cheese-newsletter/cell-08.py: 3) `"agent-framework-core==1.18.0" \` "pinned".
CODE(colab/cheese-newsletter/cell-16.redacted.py: 6–12) (header `Cheese Newsletter · cell 16 · lines
6–12`): lines 8–9 `<reader1>`, `<reader2>` YELLOW "you and a friend"; lines 10–11 GREY "commented out";
line 6's "Email is preview-only" GREEN.
SAY: The last notebook writes a cheese newsletter per reader, with Microsoft's Agent Framework, pinned. In the users cell, put in yourself and a friend, and keep two entries. Email is preview only; nothing is sent.

SHOW: TRACKER NL 4. CODE(colab/cheese-newsletter/cell-25.py: 5–16, 25) (header `Cheese Newsletter ·
cell 25 · lines 5–25 (folded)`, subtitle "Orchestrator Agent"): line 5 `gpt-5.6-luna` BLUE; line 8
`"max_iterations": 16` PURPLE; lines 13–15, the three tools, GREEN; line 25
`"allow_multiple_tool_calls": False` "one at a time".
SAY: The orchestrator gets three tools: a researcher with web search, an editor, and send email. At most 16 iterations, one tool call at a time.

SHOW: TRACKER NL 5. RECORDED(expected/colab-cheese-newsletter-c27-run-demo.txt: 4–11) (readers as in the
file): the four `[tool] editor_agent` lines get a YELLOW bracket "×4"; line 10 `send_email`; line 11
`Saved HTML: … (8005 bytes). No email sent.`. A chip CODE(colab/cheese-newsletter/cell-16.redacted.py:
114–116) "every draft is validated · errors go back as the tool's result". Then line 30 `Created 4 mock
emails. No email was sent.` with a GREY tag "saved run: 4 readers · today's list: 2".
SAY: In the staff's saved run, the first city took four editor calls: the code validates each draft and returns any errors as the tool's result. Then send email saved the HTML. That run had four readers; today's list makes two.

SHOW: LECTURE 36–37. V8: a newsletter draft card and the BLUE orchestrator's speech bubble "done!"; a door marked
SUCCESS stays shut. CODE(colab/cheese-newsletter/cell-18.py: 117–125) (header `Cheese Newsletter · cell 18
· lines 117–125`, subtitle "Business Logic"): line 119 `if context.receipt is None:` → RED "no receipt →
error"; line 123 `if not Path(receipt["path"]).is_file():` → RED "file missing → error"; line 120's
`{reply}` GREY "the model's words appear only inside the error". A GREEN receipt token with a file path
drops into a slot; the file exists; the door opens.
SAY: Now the harness. When the orchestrator stops, Python ignores what it says and checks two things: is there a receipt from send email, and is that file on disk? If not, the run fails; success is a receipt, not a claim.

SHOW: TRACKER NL 6. CODE(colab/cheese-newsletter/cell-22.py: 16) (header `Cheese Newsletter · cell 22 ·
line 16`, subtitle "Editor Agent") becomes a GREY sticky note on the prompt; it drifts through the gate
unchecked. RECORDED(expected/colab-cheese-newsletter-c30-preview-1.txt: 26 cut to `…Promotion URL:
https://…`), the URL RED, tag `erratum` "a rule that matters belongs in validate_newsletter". Caption "a
note is not a check".
SAY: Compare a rule that lives only in the prompt. The editor is told: no embedded URLs. The saved preview has one anyway, because no code checks for it; a note is not a check.

SHOW: LECTURE 10–12. Two GREY dashed boxes (tag `concept · lecture only`): "Self-RAG: relevant? supported?
useful?" and "Corrective RAG: grade the documents", caption "don't trust: check". A GREY dashed chip
"Lecture 7: the harness". A GOLD tag "web search · billed per call". `▶ your turn` on a static GREY card
"Newsletter: edit USERS · run the demo · view the previews". Hold 2 s.
SAY: The lecture's Self-RAG and Corrective RAG grade their retrieval for the same reason: don't trust, check. Next lecture calls this outer layer the harness. Web search is billed per call; pause, and run the demo.

---

## S16 · Tear down, recap, and what's next — `s16_recap.py` · `Recap`

Lecture: 41 (and 32–33).

SHOW: TRACKER RunAg 1 · extra. The ADK terminal (strip): Ctrl+C → TERM(adk-laptop/15-adk-web.txt: 49–51)
`ADK Web Server shutting down...`. It types `git status --short; git status --short --ignored | grep '^!!'`
(extra; folds) → TERM(adk-laptop/39-x-git-status.txt: 2, …, 16–21, 24) in a 12-row terminal: `?? .python-version`
GREEN "your pin"; `!! .env`, `!! .venv/`, `!! uv.lock` GREY "ignored".
SAY: Time to tear down: control C stops the web server. An extra git status shows the renamed folders and your Python pin; dot env, the virtual environment and the lock file are ignored.

SHOW: A RED-outlined ghost folder `baseline/.adk/` "sessions · not in .gitignore" (from the log line
`29` lines 41–42); a GREY chip "add .adk/ to your ignore file (exercises)"; a GREY chip ".venv · 1.6 GB".
SAY: The sessions in the agent's dot ADK folder aren't ignored, so don't commit them, and delete the 1.6 gigabyte virtual environment when you're done.

SHOW: A BLUE Colab frame with Runtime › Disconnect and delete runtime (tag `illustration`), ticked three
times: "Cheese Quiz", "Travel Planner", "Newsletter". Three GOLD key glyphs in a row: "service account ·
in secrets/ beside llm-rag", "AI Studio key · root .env", "OpenAI key · Colab Secrets only"; each gets a
GREY "delete or cap when the course ends". A GREY chip "llm-rag: stopped in part 1".
SAY: In each notebook, disconnect and delete the runtime. Keep the service account key beside L-L-M rag, never inside it, and delete or cap the other two keys when the course ends.

SHOW: LECTURE 41. The anatomy (V1) full size, each block filling with the tutorial's objects as named
(GREY code chips): LLM core `gemini-3.1-flash-lite`, `gpt-4o`, `gpt-5.6-luna`; Instructions
`instruction=`, `instructions=`, "the system prompt", `output_type`; Tools `FunctionDeclaration`,
`@function_tool`, `@tool`, `MCPToolset`, `.as_tool`; Memory "message history", "session state · one
session".
SAY: Here's the lecture's anatomy, filled with today's code. Gemini and OpenAI models as the core; prompts and output types as instructions; tools by hand, decorated, or over MCP; history and session state as memory.

SHOW: Dynamic Control fills PURPLE with `Runner`, `Runner.run(max_turns=12)`, `max_iterations`, and a TEAL
chip "llm-rag: two calls by hand". LECTURE 32–33: the lecture's formula writes in under it (our words):
"agent ≈ LLM + reasoning + instructions + tools"; two GREEN chips append: "+ a loop the framework runs",
"+ checks your code enforces".
SAY: Dynamic control is the framework's loop, or two calls by hand. The lecture's formula, LLM plus reasoning, instructions and tools, gains two pieces: a loop the framework runs, and checks your code enforces.

SHOW: The lecture tag leaves. A card "Test yourself", questions appearing one at a time (each stays as the
next fades in below, smaller): Q1 "In function calling, who runs the function, and what travels back to
the model in call 2?" Q2 "What does mode="any" change, and why only on call 1?"
SAY: Test yourself. One: who runs the function, and what goes back in call 2? Two: what does mode any change, and why only on call 1?

SHOW: Q3 "What ends an agent loop, what cap do frameworks add, and which lecture block is that?" Q4 "How
does TripSummarizer get the travel plan without a message from TravelPlanner?"
SAY: Three: what ends an agent loop, what cap do frameworks add, and which block is that? Four: how does the summarizer get the plan without a message?

SHOW: Q5 "In the last two notebooks, what decides that a run succeeded, and why not the model's final
text?" Then the questions shrink to the top; footer cards "Answers: exercises.md", "Study guide + every
command: github.com/JunyiZhou-Conny/MLOps_Learning · guides/L06-agents-1.md" and a GREY dashed chip
"Lecture 7 · Agents II: the harness". Everything fades to an empty frame (end of part 2).
SAY: Five: what decides that a harness run succeeded, and why not the model's word? Answers and every command are in the exercises and the study guide. Next lecture: the harness itself.
