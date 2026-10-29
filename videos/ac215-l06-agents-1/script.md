# AC215 · Lecture 6 — LLM: Agents I (follow-along: llm-rag Agents, llm-agent-google-adk, three Colab notebooks) — narration script & visual plan (v2)

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
numbers. v2 merges the four review lenses (`build/review_*.md`); `build/review_merge_log.md` says what
changed and why, finding by finding.

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
  as in BRIEF.md. The card sits in the lower third (y ≈ −2.2) so the picture above stays visible: use
  L05's `ponder_at` (`ac215-l05-rag/scenes/common.py`; copy it into `common.py`), which lifts the card's
  bottom to −3.55 so a 3-line card stays inside the safe frame (`pause_and_ponder` centers it). A 3-row
  terminal strip fades out while the card is up, so its edge doesn't peek out under it. The picture
  during the timer never shows the answer. S12's "Do you see
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
  returns. `a–b folded to X`: print the one row X in place of lines a–b; X is made only of those lines' own
  text, with a GREY `…` for what it leaves out (long JSON bodies, so every highlight fits in 13 rows).
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
  model. A `▶` card names the notebook's own section and cell titles ("every cell, from Install Packages to
  Download"), never cell numbers: Colab shows none.
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
  SAY (`self.wait(2)`) before anything moves or fades. House rule for the `▶` beat (it stacks up otherwise):
  lecture and concept chips fade before the card enters, no new picture arrives with it, and the scene's
  GOLD cost goes in as the card's last line.
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
  hosted search, and the GOLD key glyph for each of the three keys (never their content). No scene number
  ever appears on screen (viewers see chapter titles): a forward reference says "call 2", "later",
  "trip planner", "newsletter", "teardown".
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
  S04–S07, Dynamic Control in S08). It shows only on beats with no code panel and no terminal taller than
  the 3-row strip (the end of S04, the start of S08, S11), and never flickers on and off within a beat.
  **The call strip** (from the end of S04 to S07): a one-line GREY strip under the tracker, "call 1 → your
  code → call 2", whose current step lights YELLOW (S06: call 1; S07: your code, then call 2); in S06–S07 it
  does the orienting the mini-map did. V1 does not copy the slide's colours.
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
- Length and parts: narration 4,307 words (`python -m explainer.script`, after fix round 1; v2 after the
  review merge had 4,291, v1 4,292; BRIEF.md: 3,900–4,300, plan ~4,250). Part 1 = S01–S08 (what an agent
  is, and function calling by hand) 2,157 words; part 2 = S09–S16 (frameworks own the loop) 2,150 words.
  Per scene (BRIEF.md budget ±15 %):

  | scene | S01 | S02 | S03 | S04 | S05 | S06 | S07 | S08 | S09 | S10 | S11 | S12 | S13 | S14 | S15 | S16 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | budget | 260 | 280 | 200 | 290 | 250 | 280 | 300 | 270 | 360 | 300 | 270 | 280 | 240 | 260 | 200 | 210 |
  | words | 260 | 275 | 201 | 311 | 263 | 262 | 310 | 275 | 362 | 289 | 270 | 296 | 221 | 261 | 213 | 238 |

  `explainer.script` assumes 155 wpm and BRIEF.md 174; the spoken review synthesized 66 sentences and
  measured af_heart at 0.9 at 148.5 wpm (L04/L05: 144–151), so 4,307 words ≈ 29.0 min of voice plus ≈ 1
  min of sentence gaps and, with typing, outputs, five ponders and the `▶` holds, ≈ 35 min: the top of the
  series range. Later changes trim rather than add. Run `python -m explainer.script
  videos/ac215-l06-agents-1/script.md --synth` when the CPUs are free and put the measured total here.
  Part 1 ends on the teardown of S08 (empty frame); part 2 opens on a fresh laptop picture in S09. Each part ends on an empty frame.
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
  - Lexicon (`explainer/lexicon.yaml`, block `# AC215 L06`, added at the review merge): **ADK** (letters,
    `ˌeɪdˌiːkˈeɪ`; phrase-initial, or before a version, it phonemized as the word `ˈædk`), **enum**
    (`ˈiːnʌm`; the voice said `ɪnˈʌm`), **Colab** (`kˈoʊlæb`; the voice said `kˈɑːlæb`), **CUDA**
    (`kˈuːdə`; the voice said `kjˈuːdə`), **Havarti** (`həvˈɑːɹɾi`; heard as "have already"), the versions
    **1.6**, **2.12**, **2.12.0**, **1.27.5**, **3.10** (read in groups, "two point twelve point zero"; "1.6"
    and "2.12.0" also broke their sentences) and **406** ("four oh six"). No other video's narration uses
    these words. Checked and fine without an entry: MCP, FastMCP, npx, GPT-4o, L-L-M rag, O-N-N-X, Gemini
    3.1 Flash-Lite, Mara, Anja, OpenAI, AI Studio, localhost, transhumance and Self-RAG (existing entries),
    PyTorch, JSON, dot env, 8001, 1,505, 3,509, 2,690. Keep the SAY spellings exactly as written.
  - i18n stage: `en_display` candidates (spoken form → literal): L-L-M rag → `llm-rag`, L-L-M agent google
    ADK → `llm-agent-google-adk`, dot env → `.env`, dot env dot example → `.env.example`, dash dash agent →
    `--agent`, mode any → `mode="any"`, mode ANY / the enum value ANY → `"mode": "ANY"` / `ANY`, O-N-N-X
    runtime → `onnxruntime`, MCP underscore tools → `mcp_tools`, response dot text → `response.text`, get
    book by author → `get_book_by_author`, cd L-L-M rag → `cd llm-rag`, cd google ADK tutorial → `cd
    google-adk-tutorial`, cd L-L-M agent google ADK → `cd llm-agent-google-adk`, python cli.py, dash dash
    agent, chunk type char split → `python cli.py --agent --chunk_type char-split` (and dash dash load →
    `--load`), uv run ADK web → `uv run adk web`, uv run ADK dash dash version → `uv run adk --version`, dash
    dash port 8080 → `--port 8080`, uv run ADK telemetry disable → `uv run adk telemetry disable`, GCP project →
    `GCP_PROJECT`, docker volumes folder → `docker-volumes/`, Google API key equals → `GOOGLE_API_KEY=`, dot
    ADK folder → `.adk/`, tool config → `tool_config`, default credentials error → `DefaultCredentialsError`,
    1 baseline → `1-baseline`, baseline dot agent → `baseline.agent`, output key → `output_key`, MCP
    servers, not tools → `mcp_servers`, not `tools`, needs confirmation → `needs_confirmation`, apply
    confirmation → `apply_confirmation`, send email → `send_email`, the users cell → the `USERS` cell,
    control C → `Ctrl+C`, MLOps Learning repo → `MLOps_Learning` repo.
  - Emoji in captured lines (`c21` line 3, the `c25` strip, `cell-57.py` lines 4 and 11) don't render: the
    house mono font drops them silently. Leave such lines out; where one is needed (`cell-57.py` line 11, the
    port erratum), print it without its emoji and have ASSETS.md say so.
  - One `Gate` class in `common.py` (a bar, a label, open and slam animations) serves S08's "final
    response" and `MaxTurnsExceeded` gates, S14's turnstile and S15's SUCCESS door: one idea, one look. "The
    human" is `person_icon` (`explainer/components.py`); the pen, gear and calculator are labelled chips.
  - S11's "history" line: with ADK's default `include_contents`, each `LlmAgent` in the sequence also gets
    the earlier agents' replies, as "[agent] said: …" context (`_present_other_agent_message`,
    `google/adk/flows/llm_flows/context/_fencing.py:255-295` in the google-adk 2.12.0 wheel, read at the
    review merge; `1-baseline/agent.py` sets no `include_contents`). It is drawn, tagged `illustration`.

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
SAY: Here's a question for a cheese expert: describe where cheese making is important in the instructor's book. In the staff's recorded run, these two lines print before the answer: a function called get book by author, and its arguments.

SHOW: From the panel's second line a PINK arrow runs down into the TEAL cylinder; ten GREEN chunk cards
rise out of it, each with the same small GREY label "one book". Then a RED dashed line leaves the BLUE
Gemini chip toward `localhost:8000` and stops at the cloud's edge, where a GREY chip reads "localhost =
this machine". Two YELLOW questions write in, center: "Who searched your database?" and "Who chose the
book?" They shrink into a small YELLOW card top right that stays until the scene ends (S07 answers it).
SAY: Ten passages came back, all from one book, filtered by author. But Gemini runs in Google's data center, where localhost means nothing. So who searched your database, and who chose the book?

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
Google ADK" (a PURPLE uv glyph and a BLUE chip, caption "uv · the Gemini API"); "with a harness · two
Colab notebooks" (a BLUE notebook frame with a GREEN check inside, caption "OpenAI"). A small GREY chip
along the left edge, spanning both parts: "ideas along the way: the Cheese Quiz notebook". Small markers at
the right edge: "part 1" beside band 1, "part 2" beside bands 2–3.
SAY: Today we climb toward that in three steps. By hand, with L-L-M rag's agent; with a framework, Google's Agent Development Kit; and with a harness, in Colab notebooks.

SHOW: A layout preview in three steps, each clearing the last, as named: (1) the tracker top left, its
head cycling "llm-rag", "ADK", "Colab", with a YELLOW circle pulsing around it; (2) a GREY
`lecture_ref(6, "51–53")` sample top right; (3) a 3-row terminal strip (tag `preview`) with
`python cli.py --agent --chunk_type char-split` and a YELLOW `▶ your turn` tag. Then a row of GREY tags
writes in along the bottom: `recorded` · `expected` · `illustration` · `extra` · `stand-in` · `no key` ·
`built, not sent`.
SAY: The tracker, top left, shows the step; the gray tag, top right, names the lecture slides. Pause at each yellow your-turn tag, and run the command.

SHOW: The preview clears. A checklist card "You need" writes in row by row as named: "lecture 5's
char-split collection (or the load step)", a GOLD key "service-account key · lecture 5", "Docker", "uv",
"Node.js", a GOLD key "Google AI Studio key", a GOLD key "OpenAI key · billing on", and a GREY row (not
spoken) "three Colab notebooks · links in the study guide".
SAY: You'll need the database and key from lecture 5, Docker, uv, Node, and two more keys: one from Google AI Studio, one from OpenAI, with billing on.

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
SAY: First the ideas, in the Cheese Quiz. Save a copy in Drive, then add your OpenAI key in the Secrets panel, under the name shown, with notebook access on.

SHOW: TRACKER CQ-Pre 3. CODE(colab/cheese-quiz/cell-10.py: 3) (header `Cheese Quiz · cell 10 · line 3`,
subtitle "Install Packages"): `fastmcp openai-agents` gets a GREY tag "unpinned"; `> /dev/null 2>&1`
underlines YELLOW with a tag "hides every error · erratum: rerun without it if imports fail". TRACKER
CQ-Pre 4: RECORDED(expected/colab-cheese-quiz-c13-download.txt: 5–6, 9–10), with a YELLOW caption "look
for both To: lines · missing? rerun Download". `▶ your turn` on a static GREY card "Prerequisites: save a
copy · Secrets: OPENAI_API_KEY, notebook access on · run Install Packages, Imports, Set Up OpenAI Key,
Download". Hold 2 s.
SAY: The install cell installs two packages, unpinned, and hides all output: if imports fail later, rerun it without that redirect. Then download the quiz files, and pause to run the setup.

SHOW: TRACKER CQ-Agent 1. V1 lane 1 as a compact row (≤ 1.1 units tall) in the top third: a PINK question
chip "best cheese for a grilled cheese sandwich?" → a BLUE `gpt-4o` chip → a GREY answer card; a GOLD
counter "1 call · 2.81 s" (RECORDED(expected/colab-cheese-quiz-c21-base-llm.txt: 30), tag `recorded`). No
code panel: each lane is one row, so the three fit the frame together (the study guide quotes
`cell-20.py: 8–17`).
SAY: Now the notebook asks one question three ways, with the same model each time: what's the best cheese for a grilled cheese sandwich? Lane 1, the base LLM: one call to GPT-4o, one answer, in under 3 seconds.

SHOW: LECTURE 16–18. TRACKER CQ-Agent 2. Lane 2 under lane 1: four GREY stations in one row, plain-word
labels, "analyze" → "decompose" → "answer + verify" (badge "×4") → "synthesize". A token runs the row;
each station pings the same BLUE `gpt-4o` with a GOLD tick; the counter ticks 1 → 11 calls, then "39.34 s"
(RECORDED(expected/colab-cheese-quiz-c25-reasoning-llm.txt: 101), tag `recorded`). A GREY diamond at the
row's start: "your Python decides the order". A chip "701 tokens" (c25: 101) with a GREY `erratum` tag "an
estimate: +100 per sub-question (cell 24 · line 116)".
SAY: Lane 2, the reasoning LLM: Python methods run in a fixed order. Analyze, split into 4 sub-questions, answer and verify each, then combine. That's 11 calls and 39 seconds, and its token total is only an estimate.

SHOW: Slide 18's four technique names (our words, GREY dashed, ≥ 20 pt) write in above the stations they
name: "problem decomposition" over decompose, "verification loop" over answer + verify, "summary
generation" over synthesize, "sequential processing" along the arrows; the diamond pulses. Captions: GREY
"reasoning workflow: many calls, ordered by your code" and a GREY dashed chip "a reasoning model thinks
inside one call · more with Gemini, later".
SAY: The lecture calls a multi-call system like this a reasoning engine. Here your Python orders the calls, so it's a reasoning workflow, not a reasoning model.

SHOW: TRACKER CQ-Agent 3. The lecture tag leaves. Lane 3 under lane 2: the diamond slides *into* the BLUE
`gpt-4o` chip; a GREY "instructions" sheet clips onto it; an excerpt chip `tools=[web_tool],` (header
`Cheese Quiz · cell 30 · line 34 (excerpt)`) hands it a BLUE `web_search` chip tagged "hosted by OpenAI"
(GOLD tick). The model reaches for it twice, the two search texts of
RECORDED(expected/colab-cheese-quiz-c31-simple-agent.txt: 23, 28) flying out as small PINK chips, then
stops: "13.29 s" (c31: 100). An excerpt chip `Tools used: 1` (c31: 99) with a GREY `erratum` tag "tools
configured (cell 30 · line 71), not calls".
SAY: Lane 3, the agent: the same model, plus instructions and a web search tool that OpenAI hosts. Its answer reports two searches, and it stopped on its own after 13 seconds. It also reports one tool used, but that counts tools configured, not calls.

SHOW: LECTURE 25–27. Lane 3 becomes V1, the anatomy, part by part, full size: its BLUE `gpt-4o` chip moves
into one rounded agent box as "LLM core"; its instructions sheet becomes GREY-outlined "Instructions"; its
`web_search` chip becomes GREY-outlined "Tools"; the diamond inside the model stretches into the wide
dashed "Dynamic Control" bar; an empty GREY-outlined "Memory" appears (nothing in lane 3 remembers). A GREY
chip "Task / Goal" → the agent box → a GREY chip "Task completion". Lanes 1–2 shrink to a thumbnail under
the tracker. Above it the lecture's
definition writes in (slide 26, our words): "an LLM, given instructions and tools, that runs on its own
until the task is done". The Dynamic Control bar turns YELLOW, caption "who decides the next step".
SAY: The lecture defines an agent as an LLM, given instructions and tools, that runs on its own until the task is done. Of its five blocks, one decides the next step: dynamic control, the steering wheel.

SHOW: The thumbnail's BLUE `gpt-4o` chips and the anatomy's LLM core highlight YELLOW together; a GREY card
"agent = a smarter model" gets a RED strike. The anatomy shrinks into the bottom-right corner: the
mini-map. Then `▶ your turn` on a static GREY card "LLM to Agent: every cell, from "Define the LLM model and
question" to the Agent", its last line GOLD "paid per call". Hold 2 s.
SAY: So an agent isn't a smarter model: the model was the same in all three lanes. What changed is who steers, and the tools. Every call is paid; pause, and run the three lanes.

---

## S03 · Everything the model knows is in the envelope — `s03_envelope.py` · `Envelope`

Lecture: 41.

SHOW: TRACKER CQ-Inputs 1. The mini-map hides. An excerpt chip (header `Cheese Quiz · cell 35 · line 1
(excerpt)`): "LLMs are stateless functions." V2: an envelope slides to the BLUE `gpt-4o` chip, which
opens it, answers, and the envelope crumples away; a fresh empty envelope arrives. Caption "every call: a
fresh envelope".
SAY: Next section: managing the model's inputs. LLMs are stateless functions. Every call is a fresh envelope, and the model knows only what's inside.

SHOW: LECTURE 41. V2, one tracker step at a time (TRACKER CQ-Inputs 1 → 7): the envelope holds what that
step's cell actually sends, each sheet labelled in slide 41's words: "user prompt", "system prompt",
"contexts: retrieved documents", "user sessions: earlier turns", "user preferences: a profile from past
sessions", "contexts: tool outputs", "output schema". The sheet a step adds glows as it slides in; sheets it
drops slide out: step 4 drops the documents, step 5 keeps 2 of the 4 earlier turns, step 6 drops the turns
(`cell-40.py: 42–45`, `cell-41.py: 18–25`, `cell-42.py: 49–54`, `cell-43.py: 56–59`, `cell-44.py: 29–41`).
As each step lands, the answer card beside the envelope Transforms to that step's pick.
SAY: The notebook keeps the model and question fixed, and changes the inputs each step. A system prompt, retrieved documents, earlier turns, a profile from past sessions, a tool's output, an output schema.

SHOW: The seven picks lay out in a column right of the envelope (RECORDED excerpts, tag `recorded`), each
joined by a thin line to the step that produced it, each lighting as the SAY names it: `Cheddar` (c38: 10)
· `American Cheese` (c39: 10) · `American Cheese` (c40: 10) · "mild cheddar and mozzarella" (c41: 8) ·
`Havarti` (c42: 8) · "Whole Foods Mild Cheddar" (c43: 8) · `"top_recommendation": "Whole Foods Mild
Cheddar",` (c44: 10, wrapped).
SAY: Watch the top pick change: cheddar, American, then mild cheeses for kids, then Havarti. Then a mild cheddar from Whole Foods, and finally the same pick as strict JSON.

SHOW: TRACKER CQ-Inputs 4. CODE(colab/cheese-quiz/cell-41.py: 18–22) (header `Cheese Quiz · cell 41 · lines
18–22`, subtitle "Step 4: Adding Short-term Memory", 9 rows): lines 20–22, the earlier turns, highlight GREY
one by one and fly into the envelope as sheets; then it Transforms into CODE(colab/cheese-quiz/cell-41.py:
22–25) (8 rows), and line 23 flies in. Caption "memory = paper you put back, every call".
SAY: Step 4 shows what memory really is. The earlier turns aren't remembered: the code sends them again, every time. Memory is paper you put back in the envelope.

SHOW: The sheets regroup under two GREY headers in slide 41's words: "Instructions: system & user
prompts · contexts · output schema" and "Memory: user sessions · user preferences". A GREY dashed chip
"Lecture 7: context engineering".
SAY: The lecture groups these sheets into two building blocks: instructions and memory. Next lecture names the craft: context engineering.

SHOW: TRACKER CQ-Inputs 2. A YELLOW card "Spot it" (no timer). CODE(colab/cheese-quiz/cell-39.py: 16–21)
(header `Cheese Quiz · cell 39 · lines 16–21`, subtitle "Step 2: Prompt Engineering"); lines 19–20
highlight. After the SAY, 4 s with the code on screen (`self.wait(4)`), while the "Spot it" card's
underline draws across the 4 s.
SAY: Now look closely at the code of step 2. Can you spot the slip?

SHOW: In V2, the "system prompt" and "user prompt" sheets flip so that each carries the other's role label;
both flash RED.
SAY: The system prompt goes in with the role user, and the question with the role system.

SHOW: An `erratum` tag; the two labels swap back (GREEN check), caption "swap the roles, then compare ·
steps 3–7 are right". Under the code panel a GREEN fix chip of two rows, `{"role": "system", "content":
system_prompt},` / `{"role": "user", "content": user_prompt}` (header "cell 39 · lines 19–20 · your edit"),
GREY tag "your step 2 answer will differ from the saved one". `▶ your turn` on a static GREY card
"Managing LLM Inputs: swap the roles in step 2 · run steps 1–7", its last line GOLD "paid per call". Hold 2 s.
SAY: Swap those two roles before comparing; from step 3 on, they're right. Pause, and run the seven steps.

SHOW: The "tool outputs" sheet glows YELLOW in the envelope, with a GREY tag "simulated · pasted in by the
code (cell 43 · line 6)"; a GREY "?" chip appears beside it: "how does a model ask for a tool?" A GREY chip:
"keep the Cheese Quiz open · its Tools, MCP section comes after ADK". The envelope fades.
SAY: And notice step 6: the code pasted a tool's output into the envelope. But how does a model ask for a tool?

---

## S04 · A menu of two tools — `s04_menu.py` · `ToolMenu`

Lecture: 8–14, then 39.

SHOW: LECTURE 8–14. No tracker yet. V3's first half: L05's strip (slide 8) writes left to right: PINK
"question" → GREEN "Retrieval" → BLUE "LLM" → GREY "Response". Then six GREY dashed boxes (slides 9–12,
our words) fly in one after another as named and stack into a column between two BLUE LLM boxes (slide
13): "pre-retrieval", "post-retrieval", "retrieval decision", "document grading", "query rewrite", "web
search".
SAY: In lecture 5, RAG was a straight line: question, retrieval, model, response. The lecture's recap makes retrieval smarter: steps around the search, whether to retrieve at all, grading, rewriting, and web search.

SHOW: The first BLUE LLM box gets a YELLOW label "chooses"; a GREY caption "agentic RAG".
SAY: Agentic RAG puts a model in front of that menu, and lets it choose.

SHOW: TRACKER Agents (llm-rag · Agents, no step lit). The column shrinks to two GREEN menu cards,
`get_book_by_author(author, search_content)` and `get_book_by_search_content(search_content)`;
"retrieval decision" stays behind as a GREY dashed card (S06 crosses it out). A README chip (header
`README.md · line 244 (excerpt)`, tag `expected`): "let the LLM decide how to retrieve".
SAY: L-L-M rag's agents section is agentic RAG with a menu of two. Its README says: let the L-L-M decide how to retrieve. Search one author's book, or search all books.

SHOW: The mini-map hides. CODE(agent_tools.py: 9–19) (header `agent_tools.py · lines 9–19`): line 10
`name="get_book_by_author",` highlights, a GREEN tag "the name the model writes back"; line 11 the
description, tag "the model's documentation, with the parameter descriptions"; lines 13–15 `parameters={
"type": "object", "properties": {`, tag "JSON schema".
SAY: Here's the first menu item, written by hand: a name, which the model will write back, and a description; with the parameter descriptions, the only documentation the model sees. Parameters come as a JSON schema.

SHOW: The panel Transforms to CODE(agent_tools.py: 19–30) (line 28 through `unname`): the nine names get a
GREEN bracket "enum: only these 9"; then it folds the names to one `… 9 names …` row and Transforms to
CODE(agent_tools.py: 31–37): line 33 wraps and highlights YELLOW, its "a a" gets a GREY `erratum` tag
"typo in the source"; line 36 `"required": ["author", "search_content"],` highlights GREEN.
SAY: The author must be one of 9 names in an enum. The search text's description even coaches the model: expand the search term to a sentence or two. And both fields are required.

SHOW: CODE(agent_tools.py: 41–49) (header `agent_tools.py · lines 41–49`): on line 41, `author,
search_content` underline GREEN "from the model", `collection, embed_func` underline TEAL "your code
supplies these"; line 47 `n_results=10, where={"author": author}` highlights PINK. Then it Transforms to
CODE(agent_tools.py: 78–81): "one Tool, two declarations".
SAY: Now the real function. Two more arguments, the collection and an embedding function, aren't in the schema: your code supplies them. The model controls only the author and the search text.

SHOW: LECTURE 39. Three GREY dashed duty chips (slide 39, our words): "pick the tool", "format its
inputs", "interpret its outputs". The first two attach to a BLUE pen glyph "the model writes"; the third
gets a small GREY tag "call 2". A TEAL gear "your code runs" sits beside the pen.
SAY: The lecture says a tool-using agent must pick the right tool, format its inputs, and interpret its outputs. Here the model picks and formats only by writing; your code runs the tool.

SHOW: Two columns: left, the nine enum names (masked) in GREEN; right, the 11 book titles in GREY, cut out
of the `Processing file: outputs/embeddings-char-split-<title>.jsonl` lines of
`cli-container/20-load-char-split.txt` (lines 9, 23, 36, 52, 65, 77, 89, 101, 116, 129, 142: titles
only). No lines connect them (the picture never shows the answer). When the ponder card arrives (lower
third), the two lists collapse into counts above it: the nine names into a GREEN stack "9 author names",
the eleven titles into a GREY stack of eleven book glyphs "11 books"; the two GREEN menu cards sit small
above them. After the timer the lists expand again for the answer.
SAY: Here are the 11 books in the collection, beside the 9 names in the enum.
PONDER(8 s, "Nine author names, eleven books.\nAt least how many books can get_book_by_author never reach?\nCan the agent still get to them?")

SHOW: An extra card: "count the chunks per author" (container prompt `app@abcf218747d0:/app$`); a
terminal strip prints TERM(cli-container/34-x-authors.txt: 15, 26–28). In the two columns, GREEN lines
connect nine books to the nine names; *Cottage Cheese Recipe Book* stays unconnected with a GREY tag
"author not in the list · 178 chunks"; *Womans Institute Library of Cookery* gets a RED-edged tag "author
= None · 1,505 chunks · lecture 5's file-name slip".
SAY: Two books. The cottage cheese recipe book, 178 chunks, has an author who isn't on the list. The Woman's Institute book, 1,505 chunks, has no author at all: a file name slip in lecture 5.

SHOW: Both unconnected books get a PINK arrow to `get_book_by_search_content` "still reachable". Then V3's
stage builds full width: left, the BLUE Google cloud with a BLUE chip "Gemini · location global"; center,
a dashed vertical trust boundary labelled PINK "HTTPS"; right, the GREY laptop holding two TEAL containers,
the CLI container (`cli.py`, `agent_tools.py`) and the Chroma container (cylinder
"char-split-collection · book · author · year").
SAY: Both stay reachable by the search across all books. Now the stage: Gemini in Google's cloud, two containers on your laptop, and a boundary between.

SHOW: The two GREEN menu cards slide across the boundary into the cloud; the cylinder stays put, a GREY
lock glyph on it. Then one ghost run on the stage (tag `illustration`), each step labelled as the SAY names
it: a PINK question card and the menu go up ("call 1"); a BLUE card `{name, args}` comes back across the
boundary; inside the CLI container a TEAL gear turns, a PINK arrow dips into the cylinder, ten small GREEN
cards come out and wrap into one TEAL card; the question, the BLUE card and the TEAL card go up together
("call 2"); a BLUE answer card comes back. The trip shrinks to the call strip under the tracker, "call 1 →
your code → call 2" (the next scenes light it step by step). The mini-map returns, Tools lit YELLOW.
SAY: The model never gets your database, only a menu. Call 1 returns an order: a function name and arguments. Your code runs it; call 2 sends back the result.

---

## S05 · Back in the container: the agent needs an index — `s05_container.py` · `BackInTheContainer`

Lecture: none.

SHOW: TRACKER Prereq 1. Terminal (full width, 8 rows, title `laptop`, prompt `student@laptop:~/AC215$`).
A GREY caption "fresh start only · README.md · line 48 links the repo". It types
`git clone https://github.com/dlops-io/llm-rag.git` → TERM(laptop/01-clone.txt: 2); then `mkdir secrets; ls`
(extra) → TERM(laptop/02-x-mkdir-secrets.txt: 2) (`llm-rag  secrets`); a GOLD key chip
"llm-service-account.json → secrets/ · beside llm-rag, never inside (lecture 5 · README.md · lines 62–69)".
SAY: Lecture 5 ended on one command; today we run it. Starting fresh? Clone L-L-M rag, and put the service account key in a secrets folder beside it; otherwise, go to your folder.

SHOW: TRACKER Run 1. It types `cd llm-rag` → (no output); the prompt becomes
`student@laptop:~/AC215/llm-rag$`. TRACKER Run 2: PANEL(laptop/05-x-edit-gcp-project.txt: 10–11,
"docker-shell.sh · line 7 · your edit"), line 10 RED `-`, line 11 GREEN `+`; `your-project-id` gets a YELLOW
tag "your own project ID". `▶ your turn` on a static GREY card "fresh start: git clone
https://github.com/dlops-io/llm-rag.git · mkdir secrets (key inside) · then: cd llm-rag · set GCP_PROJECT in
docker-shell.sh". Hold 2 s.
SAY: Step 1: cd L-L-M rag. Step 2: edit docker-shell.sh, and set GCP project to your own project ID; we used a placeholder. Pause, and do both.

SHOW: TRACKER Run 3. Terminal (13 rows). It types `sh docker-shell.sh` → TERM(laptop/06-docker-shell.txt:
2–5, 6, 7–9 joined, 10–11, …, 32–34; session; wrap). Lines 6–9 print RED, then turn GREY with the tag
"harmless · its wording depends on your Docker setup"; line 11 `Building 40.5s` gets the tag
`at the time of recording`.
SAY: Step 3: sh docker-shell.sh. Compose starts Chroma first. The pull message after it looks like an error but is harmless: there's no such image online, so Compose builds it.

SHOW: TERM(laptop/06-docker-shell.txt: 35–40; session); lines 38–39 get the tag `at the time of
recording`. Then line 41's prompt appears alone, cut before `exit` (`app@abcf218747d0:/app$`); the frame
turns TEAL, title `container · llm-rag-cli`; `abcf218747d0` gets a GREY tag "container ID · your numbers
will differ". At "pause, and get to this prompt" the terminal shrinks to a 3-row strip (the uv 0.13.1 row,
`Activating virtual environment...`, the prompt with its ID underline and tag), and `▶ your turn` comes on a
static GREY card above it: `sh docker-shell.sh` "until the app@…:/app$ prompt". Hold 2 s.
SAY: After about 40 seconds of building, the banner prints. Python 3.12.15 and uv 0.13.1, at the time of recording. After the at sign comes the container's ID, new every run; pause, and get to this prompt.

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
skip ahead", with a GREY note "chunked before September 22, 2026? git pull, then chunk → embed → load · the
book changed (explained soon)"; right "no database? · `python cli.py --chunk --chunk_type char-split` ·
`python cli.py --embed --chunk_type char-split` · then the load step" (README text, tag `expected`,
`README.md · lines 103, 129`; the embed step needs your key).
SAY: The agent needs the index from lecture 5. Kept that database? It's in the docker volumes folder; if you chunked before September 22, pull and rebuild it. Otherwise, chunk, embed and load again.

SHOW: On the right path, the "embed" arrow gets a GOLD key; a GREY card slides over it:
PANEL(laptop/08-x-copy-staff-embeddings.txt: 2–3, "outputs/embeddings-char-split-* · copied from commit
68e0bde") (`11` files, `31M total`), tag `recorded · the staff's vectors`.
SAY: We had no key, so the staff's committed embeddings stood in for the embed step.

SHOW: TRACKER Load 1. The container terminal grows (13 rows). It types `python cli.py --load --chunk_type
char-split` → TERM(cli-container/20-load-char-split.txt: 2–8, …, 142, 152–153; wrap). A README chip in the
top band (header `README.md · line 152`, tag `expected`): "recursive-split too · the agent uses char-split".
A GREY chip "8,248 chunks in 11 books · 24 from the instructor's story" (from `cli-container/34` line 15 and
line 143 of `20`). TRACKER Load 1 · extra: it types `python cli.py --get --chunk_type char-split` (extra) →
TERM(cli-container/21-x-get.txt: 6 cut after `'1021665fac86c5a5-0',`) with a `…`. `▶ your turn` on a static
GREY card "python cli.py --load --chunk_type char-split (or keep yours) · python cli.py --get --chunk_type
char-split". Hold 2 s.
SAY: Then the load step: python cli.py, dash dash load, chunk type char split. 11 books, 8,248 chunks; the instructor's story is just 24 of them. An extra get command confirms the collection answers; pause, and load yours.

---

## S06 · Call 1: the model writes the call — `s06_call1.py` · `CallOne`

Lecture: 35, then 10–13.

SHOW: TRACKER Agents 1. The call strip lights "call 1". CODE(cli.py: 431–437) (header `cli.py · lines
431–437`; line 435 through `unname`): `Content(role="user", parts=[Part(text=…)])`, the question PINK. Then
it Transforms into CODE(cli.py: 441–452) (header `cli.py · lines 441–452`).
SAY: After the collection lookup, the agent function builds the user's turn: the question, with the role user. Then comes the first call to Gemini.

SHOW: LECTURE 35. Line 445 `temperature=0,` highlights, with a GREY dashed chip (slide 35, our words) "LLM
core: model · parameters · response format"; line 446 `tools=[agent_tools.cheese_expert_tool],` highlights
GREEN "the menu"; lines 447–451 highlight YELLOW, `mode="any"` boxed.
SAY: Three settings: temperature zero, the menu as tools, and a tool config with mode any. The lecture lists temperature as a design choice. Zero keeps the tool choice nearly repeatable.

SHOW: A terminal strip at the TEAL container prompt. It types
`python -c 'from google.genai import types; print(repr(types.FunctionCallingConfig(mode="any")))'`
(extra; folds) → TERM(cli-container/32-x-mode-any.txt: 2–4). `ANY` highlights YELLOW; caption "the model
must answer with a function call".
SAY: An extra one-liner shows what mode any becomes: the enum value ANY. The model must answer with a function call.

SHOW: LECTURE 10–13. V3's column returns small with its GREY dashed "retrieval decision" card; beside it
a GREY dashed Self-RAG box "Retrieve?" with yes/no branches (tag `concept · lecture only`). A RED line
crosses out "retrieval decision"; caption "chooses which search · never whether". A GREY chip "exercise:
delete tool_config, then greet it".
SAY: In the lecture, a good agent may decide not to search at all; Self-RAG starts with that decision. Ours can't: on call 1, mode any forces a tool call. It chooses which search, never whether.

SHOW: The lecture tag leaves. V2: an envelope opens onto the real request. An extra card: "runs agent()
unchanged · prints the request instead of sending it"; then a full-width terminal at the container prompt
prints (≤ 12 rows, so every highlight is on screen at once) TERM(cli-container/31-x-call1-request.txt: 20;
wrap, 21–31 folded to `{ "contents": [ { "parts": [ { "text": "Describe where cheese making … book?" } ],
"role": "user" } ],` (wrap), 32–41 folded to `"tools": [ { "functionDeclarations": [ { … "name":
"get_book_by_author", …`, 42–52 folded to `"enum": [ … 9 names … ],`, 53–85 folded to `… "name":
"get_book_by_search_content" … ],`, 86–90 folded to `"toolConfig": { "functionCallingConfig": { "mode":
"ANY" } },`, 91–93 folded to `"generationConfig": { "temperature": 0.0 }`, 95), tag `built, not sent`. On
line 20, `locations/global` and `gemini-3.1-flash-lite` highlight BLUE; `"mode": "ANY"` and `"temperature":
0.0` YELLOW; line 95 GREY.
SAY: What does Gemini actually receive? An extra script runs the same code, but prints the request instead of sending it. One envelope: the question, both declarations with the enum, mode ANY and temperature zero.

SHOW: A GREY dashed ghost card "systemInstruction" slides next to the body with a tag `erratum` "defined
at cli.py lines 40–58 · never sent (as in lecture 5)".
SAY: And no system instruction: as in lecture 5, cli.py defines one and never sends it.

SHOW: TRACKER Agents 1. Terminal (full width, TEAL). It types `python cli.py --agent --chunk_type
char-split` → TERM(cli-container/30-agent.txt: 2–3, 8–10, 16–17, …, 71; wrap), tag `real run · no key`;
lines 8–10 (masked) get a GREEN tag "the lookup passed"; line 71 RED. A GREY "with your key, look for"
card: "`LLM Response:` with a function_call · cli.py line 454".
SAY: Now step 1 again, with the collection loaded. The lookup passes and the question prints, but the first model call needs your key: default credentials error, file not found.

SHOW: The terminal clears. V3's stage returns in the upper half (last seen at the end of the menu scene);
in the lower half PANEL(expected/out-txt-agent-run.txt: 15 cut after "LLM Response:" + ` …`, 21–29; 29 cut
to `thought_signature=b'\x01\x8f=k_…',`) (header `out.txt · lines 14–28 (excerpt)`, 11 rows, line 23
masked, tag `recorded · the staff's run, September 22, 2026`). V3: the BLUE model's speech bubble becomes a
BLUE JSON card `{name: get_book_by_author, args: {author, search_content}}` with a small BLUE seal "thought
signature".
SAY: Here's what the staff saw. The model's whole answer is a function call: get book by author, with the instructor as author, and the search text, cheese making importance location.

SHOW: `'cheese making importance location'` highlights; a GREY tag "4 words · the description asked for a
sentence or two" (excerpt chip of `agent_tools.py · line 33`). The `id='call_1212960'` line and the seal
pulse.
SAY: Four words, though the description asked for a sentence or two. There's also an ID, and a thought signature; we'll meet it again.

SHOW: PANEL(expected/out-txt-agent-run.txt: 52, "out.txt · line 51"):
`automatic_function_calling_history=[]` highlights GREY "the SDK ran nothing"; under the panel, at "it only has
declarations", a GREY caption "it runs functions itself only when you pass Python functions · here: declarations
only". The BLUE card waits at the
trust boundary, unopened; caption "Gemini wrote arguments · nothing has run yet". Then `▶ your turn` on a
static GREY card (short lines, two columns): top "with your key: python cli.py --agent --chunk_type
char-split"; left "look for, in order:" `LLM Response:` with a function_call (cli.py line 454) ·
`Function calls:` (line 458) · `Function:` and `Calling function with args:` (agent_tools.py lines 87, 89)
· `Response:` 10 passages from today's story (line 101) · a second `LLM Response:` about today's book
(cli.py line 478); right "if it fails with your key:" DefaultCredentialsError → is
llm-service-account.json in secrets/, beside llm-rag? · 403 PERMISSION_DENIED → the service account's
roles (README.md · lines 56–58) and the Vertex AI API · KeyError: 'GCP_PROJECT' → start with sh
docker-shell.sh; last line GOLD "2 Gemini calls + 1 embedding call per run · paid". Hold 2 s.
SAY: The SDK ran nothing; it only has declarations. So far, one paid call. Pause here, and run step 1 with your key.

---

## S07 · Call 2: your code ran it, the model answers — `s07_call2.py` · `CallTwo`

Lecture: 39.

SHOW: The call strip lights "your code". Under it an excerpt chip `function_responses =
agent_tools.execute_function_calls(` (header `cli.py · line 459 (excerpt)`), caption "hand the calls to the
dispatcher", stays while CODE(agent_tools.py: 84–94) (line 88 `if function_call.name ==
"get_book_by_author":` YELLOW "match the name") Transforms into CODE(agent_tools.py: 95–100, 103–107) folded
(header `agent_tools.py · lines 95–107 (folded)`, 12 rows; 95–100 GREEN "call the real function", 103–107
TEAL "wrap the result"). No mini-map in this scene: the call strip orients.
SAY: Back in your Python, a dispatcher matches each call's name, runs the real function with the model's arguments, and wraps the result as a function response.

SHOW: An extra card: "feed the model's call from the staff's run through agent_tools.execute_function_calls,
against this collection", with a PINK tag `stand-in` "a stored chunk's vector replaces Google's
embedding". The TEAL container terminal prints TERM(cli-container/33-x-dispatch-recorded-call.txt: 36,
37–44 folded to `Function calls: [FunctionCall( … name='get_book_by_author' )]`, 45, 48; wrap) (author
masked).
SAY: Without a key, an extra script feeds the staff's recorded call through the tutorial's own dispatcher, against our collection.

SHOW: Line 36 `stand-in embed_func: returns the stored vector of chunk 8440accaceb0ce96-6 (Tolminc Cheese)`
highlights PINK, tag `stand-in`.
SAY: One stand-in: without Google we can't embed the search text, so a stored chunk's vector stands in, and the 10 chunks may differ from a real query's.

SHOW: TERM(cli-container/33-x-dispatch-recorded-call.txt: 51–57, …, 135; wrap). V3 runs above a strip:
on the TEAL side the BLUE card's arguments split; PINK `search_content` → a dashed vector glyph
(`stand-in`) → `collection.query(…, n_results=10, where={"author": …})` → ten GREEN chunk cards from
today's story (first words from lines 51, 57, 59: "is ready?” Mara asked", "Anja smiled", "Over the
following hours") → they merge into one GREEN string strip → a TEAL card `{"content": …}` labelled "3,509
characters" (line 135) staples onto the BLUE call card. The cylinder never moves toward the cloud.
SAY: Out come 10 passages from today's story, about Mara and Anja. Joined into one string of 3,509 characters, they're stapled to the call as its response.

SHOW: CODE(cli.py: 464–477) (header `cli.py · lines 464–477`, 12 rows: lines 470–472 shown as one row
`Content(parts=function_responses),`): line 468 GREY "the question", line 469 BLUE "the model's own turn,
unchanged", the `function_responses` row TEAL "your function responses"; line 475 `tools=` GREEN; a GREY
dashed ghost beside line 474 "no tool_config → mode back to automatic". The call strip lights "call 2".
As the SAY names them, the three rows fly out as sheets into a fresh V2 envelope: GREY "the question", BLUE
"the model's turn" with its seal, TEAL "your function responses"; the GREEN menu card clips on; a GREY
dashed ghost where the tool config was.
SAY: Call 2 sends three things: the question, the model's own turn, unchanged, and your function responses. The tools go along again, but no tool config: the mode is back to automatic.

SHOW: LECTURE 39: the duty chip "interpret its outputs" lights. V2's second envelope opens: a full-width
terminal prints (13 rows, so lines 151, 167 and 231 are on screen together)
TERM(cli-container/33-x-dispatch-recorded-call.txt: 137 (no wrap: cut at the row), 138–147 folded to
`{ "contents": [ { … "role": "user" },`, 148–150 folded to `{ "parts": [ {`, 151 cut to
`"thoughtSignature": "AY89a186…",`, 152–159 folded to `"functionCall": { … "name": "get_book_by_author" }`,
160–163 folded to `} ], "role": "model" },`, 164–166 folded to `{ "parts": [ {`, 167, 168, 170 cut after
`Mara asked.` + `…` (the file has `"content": "is ready?\u201d Mara asked.`: print the escape as it is), …, 231,
233), tag `built, not sent`. Line 151 `"thoughtSignature":` boxed BLUE; the BLUE seal from V3 lands on it.
Line 167 `"functionResponse"` TEAL; line 231 `"generationConfig": {}` GREY.
SAY: Inside, the model's turn carries its thought signature: Gemini's thinking models sign their turn, and want it back exactly as sent. Resending the turn unchanged keeps the seal.

SHOW: Our request stays unsent: the `built, not sent` terminal fades in place and V3's compact stage returns. A
GREY dashed envelope, the staff's recorded call 2 (tag `recorded · the staff's call 2, September 22, 2026` under
the stage), crosses into the cloud, and a BLUE prose card comes back; while the stage leaves it unfolds into
PANEL(expected/out-txt-agent-run.txt: 99, 105 cut after "Alpine region,", 111 cut after "limestone caves",
112 cut after "(the seasonal movement of livestock)") (header `out.txt · lines 98–111 (excerpt)`, masked,
tag `recorded · the staff's run · old book`); "transhumance" highlights YELLOW. Two GOLD chips: "247 tokens"
(`out.txt` line 49, file line 50) and "1,269 tokens" (`out.txt` line 135, file line 136), with a GREY note
under them "printed as `total_token_count` · out.txt · lines 49, 135".
SAY: The staff's answer? An Alpine valley, its caves, and transhumance, the seasonal movement of livestock. The two calls used 247 and 1,269 tokens.

SHOW: The hook's YELLOW card returns, center: "Who searched your database?" → GREEN "your Python, on your
laptop"; "Who chose the book?" → BLUE "Gemini wrote the call". A GOLD tag "2 Gemini calls + 1 embedding
call per question" (the embedding: `agent_tools.py · line 43` → `cli.py · lines 75–84`).
SAY: So, who searched your database? Gemini wrote the call and chose the book; your Python ran it, on your laptop. That's two model calls and one embedding call per question, all paid.

SHOW: TRACKER Agents 1 · extra. The lecture tag and the call strip leave. An extra card "count four of the answer's
words in out.txt, today's book, and the book before 85bba32" over a second terminal (title `laptop · second
terminal`, 20 pt so the table's 70 columns fit) → TERM(laptop/10-x-old-words.txt: 2–5); the "book today 0" column
highlights RED. The card leaves and the terminal grows to 13 rows (the table stays). It types
`git show --stat --format='%h %ad %s' --date=short 85bba32; head -4 'input-datasets/books/Tolminc Cheese.txt'`
(extra; folds) → TERM(laptop/09-x-book-changed.txt: 2 cut after "2026-09-22", 4–6, `…` for 7–8 (the author line
is never shown), 9). The commit and both files underline YELLOW, with a GREY "← today's book" beside line 9. At
"The staff's index" the "book before 85bba32" column highlights GREEN.
SAY: But today's book never says transhumance, nor three other words from this run: the commit that added this output also rewrote the book. The staff's index was built from the old text.

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
SAY: Step 2 links to the course's hosted Cheese Agent Tool, up at the time of recording; try it in Chrome.

---

## S08 · From two calls to a loop — `s08_loop.py` · `TheLoop`

Lecture: 26, then 35–41.

SHOW: LECTURE 26. No tracker. The mini-map shows, Dynamic Control lit YELLOW. The definition card from
S02 returns, "…until the task is done" underlined. Beside it, llm-rag's run as one short line: BLUE "call
1 · forced tool call" → TEAL "your code runs it" → BLUE "call 2 · answer" → GREY "end". A README chip
(header `README.md · line 246 (excerpt)`, tag `expected`) "AI Agent (Cheese Expert Agent)".
SAY: The lecture's agent runs until the task is done. L-L-M rag's agent ran one lap: a forced tool call, then an answer. The README calls it an agent; by the lecture's definition, it's the smallest piece of one.

SHOW: CODE(cli.py: 474–481) (header `cli.py · lines 474–481`, 8 rows): lines 474–476 highlight with a GREY
dashed ghost "no tool_config"; line 478 GREY; line 481 `def main(args=None):` GREY, label "agent() ends
here". The ponder card sits in the lower third.
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
SAY: The lecture draws the agent as a hub: the core and its instructions become a decision maker, with spokes to a planner, tools, and memory. Unroll the spoke to the tools into a loop.

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
SAY: Before part 2, tear down. Type exit; an extra docker ps then shows Chroma still up, on port 8000. Then docker compose down: two harmless warnings, and it stops.

SHOW: A PINK chip "port 8000 → free for part 2" and a GREEN chip "docker-volumes/: your index stays" write
in, then fade; `▶ your turn` on a static GREY card "exit · docker compose down". Hold 2 s. Then everything
fades to an empty frame (end of part 1).
SAY: Your index stays on disk, and part 2 also needs port 8000. Pause and tear down. In part 2, a framework runs this loop for us.

---

## S09 · ADK: clone, configure, and a sync that fails — `s09_adk_setup.py` · `AdkSetup`

Lecture: 35 (the model-line beat only).

SHOW: A new picture: the GREY laptop with a GREY dashed "no Docker this time" chip, a PURPLE uv glyph and
an empty `.venv` box; across a dashed boundary, a BLUE chip "Gemini API", reached with a GOLD key "AI
Studio key". Below it a terminal (full width, title `laptop`, prompt `student@laptop:~/AC215$`) fades in,
with a GREY caption "a new terminal · the folder that holds your clones · not inside llm-rag".
SAY: Part 2: frameworks own the loop. No Docker this time: Google's Agent Development Kit runs in a uv environment on your laptop. Open a new terminal where you keep your clones.

SHOW: TRACKER Start 1. A README chip (header `README.md · line 77`, tag `expected`): `git clone
<repository-url>`. It types `git clone https://github.com/dlops-io/llm-agent-google-adk.git` →
TERM(adk-laptop/01-clone.txt: 2); a GREY caption "the README's placeholder, filled in". TRACKER Start 2:
it types `cd google-adk-tutorial` → TERM(adk-laptop/02-cd-as-written.txt: 2), RED, tag `erratum`.
SAY: Step 1: clone; the README writes a placeholder for the address. The next line says cd google ADK tutorial, but no such folder exists.

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
SAY: Next, copy dot env dot example to dot env. An extra grep shows a placeholder Google API key, and the model, Gemini 2.5 Flash.

SHOW: TRACKER Start 4, then Start 5. The terminal shrinks to a strip. A GREY browser frame (tag
`illustration`) "Google AI Studio · API keys" with a button "Create API key"; a GOLD key glyph comes out
(never its content). A GREY file card (header `.env · your copy · git-ignored`) shows `GOOGLE_API_KEY=`
and the GOLD key glyph slots in after `=`. A GREY note "README: the key's source is the next step;
paste it here".
SAY: Then create a key in Google AI Studio, and paste it into dot env, after Google API key equals.

SHOW: LECTURE 35 (this beat only; it leaves with the next). On the `.env` card, the `GEMINI_MODEL=` line
highlights YELLOW; `gemini-2.5-flash` slides out and `gemini-3.1-flash-lite` slides in, GREEN, tag "your
edit · the model llm-rag uses (cli.py · line 27)".
SAY: Also change the model line. Choosing the LLM core is the lecture's first design decision, and here it's one line: a current model, like Gemini 3.1 Flash-Lite.

SHOW: Two GREY chips under the card: "the code's fallback: gemini-2.0-flash (`1-baseline/agent.py · line
12`) · shut down" and "gemini-2.5-flash · limited to earlier users", tag "Google's model pages, checked
October 18, 2026"; an `erratum` tag on both. A GREY dashed card: "module READMEs' Setup steps (uv sync,
cp .env.example .env): skip them · the root sync and the root .env cover every module · only the nearest
.env is loaded". The chips and the card fade; `▶ your turn` on a static GREY card "git clone
https://github.com/dlops-io/llm-agent-google-adk.git · cd llm-agent-google-adk · cp .env.example .env ·
GOOGLE_API_KEY=<your key> · GEMINI_MODEL=gemini-3.1-flash-lite", its last line a GOLD key glyph "the key
stays in the git-ignored .env". Hold 2 s.
SAY: Google lists the code's fallback, Gemini 2.0 Flash, as shut down, and limits 2.5 Flash to earlier users. Keep everything in this root file: only the nearest dot env is loaded. Pause, and set up yours.

SHOW: CODE(llm-agent-google-adk/pyproject.toml: 8–19) (header `pyproject.toml · lines 8–19`): line 8
`requires-python = ">=3.10"` GREEN; line 10 `"google-adk>=1.8.0",` YELLOW "no upper bound"; lines 18–19
`chromadb`, `sentence-transformers` GREY "→ onnxruntime, PyTorch".
SAY: The project file wants Python 3.10 or newer and ADK 1.8 or newer, with no upper bound. It also lists Chroma and sentence transformers.

SHOW: V5: L01's number line `3.10 … 3.16` slides in above the strip; the interval `>=3.10` glows GREEN to
the right edge; no ORANGE dot anywhere; a GREY chip "no python3 on PATH" (excerpt of
`adk-laptop/00-x-env.txt` line 9). The ponder card sits in the lower third; the 3-row strip fades out
while it is up.
SAY: One more fact: this laptop has no Python at all.
PONDER(6 s, "This laptop has no Python at all.\nThe project asks for 3.10 or newer.\nWhich Python will uv sync use?")

SHOW: TRACKER Start 6. The terminal grows (12 rows). It types `uv sync` → TERM(adk-laptop/07-uv-sync.txt:
2–4). On the number line a PURPLE download arrow drops `CPython 3.15.0` at the newest end (tag `at the
time of recording`).
SAY: Then install: uv sync. As in lecture 1, with no Python around, uv downloads the newest: CPython 3.15.0, at the time of recording.

SHOW: TERM(adk-laptop/07-uv-sync.txt: 5–7 joined, 9–11 joined; wrap), RED. V5: a shelf of wheels for
`onnxruntime 1.31.0` (a GREY arrow from `chromadb`, `pyproject.toml · line 18`) shows tags `cp311 cp312
cp313 cp313t cp314 cp314t`; the 3.15 slot is empty and turns RED.
SAY: It resolves 189 packages, then fails. O-N-N-X runtime, which Chroma pulls in, has wheels only up to Python 3.14.

SHOW: An `erratum` tag on the tracker's step 6: "fails whenever uv picks 3.15"; a GREY note "uv tries the
Pythons it downloaded before the system's (as in lecture 1): a uv-managed 3.15 wins over a system 3.12".
TRACKER Start 6 ·
extra: it types `uv python pin 3.13` (extra) → TERM(adk-laptop/09-x-python-pin.txt: 2), tag `fix · not in
the README`. V5: the interval collapses to the point 3.13; the `cp313` wheel clicks in, GREEN; a GREEN
file card `.python-version` "3.13" drops into the repo.
SAY: So this step fails whenever uv picks 3.15: on a fresh laptop, or where uv already has 3.15, even beside an older Python. The fix, with an extra command: uv python pin 3.13.

SHOW: TRACKER Start 6. It types `uv sync` → TERM(adk-laptop/12-uv-sync.txt: 2–4, …, 38, …, 89, …, 155)
(never lines 5–7 or 140); `google-adk==2.12.0` and `onnxruntime==1.31.0` highlight GREEN. A GREY chip
"about 1.6 GB (`du -sh`, extra) · on a Linux PC about 3 GB more of CUDA packages · a Mac: none"
(from `adk-laptop/14` line 12 and `10`).
SAY: Then uv sync again: CPython 3.13 this time, and it installs, ADK 2.12.0 included. PyTorch makes it big: about 1.6 gigabytes, plus about 3 gigabytes for CUDA on a Linux PC.

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
a 0.6 s pause the terminal types `n` (as the capture did), and a GREY chip appears: "`uv run adk
telemetry disable` · change it later".
SAY: The text says telemetry is off by default, but the capital Y means pressing enter answers yes. Answer as you like; change it later with this command: uv run ADK telemetry disable.

SHOW: TERM(adk-laptop/15-adk-web.txt: 34–38, 41); line 41 `Uvicorn running on http://127.0.0.1:8000` PINK.
TRACKER RunAg 2: the terminal shrinks to a strip; a GREY browser frame (tag `illustration`) opens at
`localhost:8000`, and its address bar changes to `localhost:8000/dev-ui/`. One strip at a time, as in the
container scene: a second strip (title `laptop · second terminal`) slides over the server strip, types `curl
-s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' http://localhost:8000/` (extra; folds) →
TERM(adk-laptop/16-x-dev-ui.txt: 2), and slides away again.
SAY: Then the server starts, on port 8000. Step 2: open localhost 8000 in your browser; an extra curl shows the redirect to the dev UI.

SHOW: In the browser, a schematic agent dropdown opens listing the seven entries of
TERM(adk-laptop/17-x-list-apps.txt: 2) (the strip shows the extra `curl -s http://localhost:8000/list-apps;
echo` and its line). The cursor picks `1-baseline`; a RED banner in the page shows the `detail` text of
TERM(adk-laptop/18-x-select-1-baseline.txt: 2; wrap); then the second-terminal strip gives way to the server
strip, which shows `15` lines 44–45 joined (`… "GET /dev/apps/1-baseline/build_graph HTTP/1.1" 404 Not
Found`).
SAY: The agent dropdown lists 7 entries, nested ones included. Pick 1 baseline, as its README says, and the page refuses: agent names must be valid Python identifiers.

SHOW: Why, as a picture (tag `illustration`): a GREY folder `1-baseline/` holding `agent.py`; a PURPLE
arrow labelled `adk web` → a GREY chip `app name = "1-baseline"` → a check "Python identifier? letters,
digits, underscores · no leading digit"; the leading `1` and the `-` flash RED. A GREY tag "ADK 2.12 checks
when it loads the agent · 1.27.5 checks later, in App(name=…)". No `import` line: the loader itself accepts
the folder (1.27.5 lists it); the name check refuses it (`18` line 2, `24` lines 131–134).
SAY: Why? Each folder name becomes the app's name, and an identifier holds only letters, digits and underscores, never starting with a digit. The name 1 baseline breaks both rules.

SHOW: A RED dashed frame `what if · just watch`, one strip at a time: it types `uv add
"google-adk>=1.8.0,<1.28"` (extra) → TERM(adk-laptop/21-x-uv-add-pin.txt: 7–8); the browser's dropdown
shows the four folders of `adk-laptop/25-x-list-apps-pinned.txt` line 2 (GREEN; drawn in the page, no
strip); the strip shows TERM(adk-laptop/24-x-adk-web-pinned.txt: 131, 132–134 joined cut after
"underscores."; wrap) RED. It types `git checkout pyproject.toml; uv sync --upgrade-package google-adk`
(extra) → TERM(adk-laptop/27-x-undo-pin.txt: 8–9). The frame closes; caption "back in your terminal".
SAY: An older version, 1.27.5, lists only the four folders. But picking one still fails, as an invalid app name. So a version pin doesn't help; we undid ours.

SHOW: TRACKER RunAg 1 · extra. In the viewer's terminal, still running the first server: Ctrl+C →
TERM(adk-laptop/15-adk-web.txt: 46, 49–51); the prompt `student@laptop:~/AC215/llm-agent-google-adk$`
returns. Then it types `mv 1-baseline baseline; mv 3-mcp-tools mcp_tools; mv 5-custom-agent custom_agent;
ls` (extra; folds) → TERM(adk-laptop/28-x-rename.txt: 2–12); `baseline`, `custom_agent`, `mcp_tools`
highlight GREEN; tag `fix · not in the README`.
SAY: What works is renaming, which isn't in the README either. Stop the server with control C, then drop each leading number, and turn hyphens into underscores.

SHOW: It types `uv run adk web` → TERM(adk-laptop/29-x-adk-web-renamed.txt: 36–37 joined, 38–39 joined,
40; wrap); in the first line `…/llm-agent-google-adk/.env` highlights PINK "the root .env". The browser's
dropdown now lists the entries of TERM(adk-laptop/30-x-list-apps-renamed.txt: 2) (extra strip `curl -s
http://localhost:8000/list-apps; echo`) after the page reloads; `baseline` is picked, GREEN. A GREY chip
under the list: "this video: baseline, mcp_tools · custom_agent as code · 2, 4, 6: exercises.md".
SAY: Start the web server again, and pick baseline. The log says it loaded the dot env at the repository root, and found the root agent in baseline dot agent.

SHOW: A GREY chip "git status: 3 folders deleted, 3 new · fine for your copy (teardown)". Two `erratum`
chips write in: (a) a README chip (header `QUICKSTART.md · line 24`, tag `expected`) `uv run adk web
1-baseline/agent.py` → the line of TERM(adk-laptop/19-x-quickstart-file.txt: 5) RED; (b) a README chip
(header `2-litellm/README.md · line 74`, tag `expected`) `uv run adk` →
TERM(adk-laptop/20-x-adk-without-web.txt: 2) "prints help · starts nothing".
SAY: Two more slips: the quick start passes a file where a folder is expected, and the module READMEs drop the word web, so it only prints help.

SHOW: A RED dashed frame `what if · just watch`, captioned "llm-rag's Chroma still on port 8000":
TERM(adk-laptop/36-x-port-8000-busy.txt: 21; wrap) RED; then it types `uv run adk web --port 8080`
(extra) → TERM(adk-laptop/37-x-adk-web-port-8080.txt: 34). Back in the viewer's terminal, `▶ your turn`
on a static GREY card "Ctrl+C · mv 1-baseline baseline; mv 3-mcp-tools mcp_tools; mv 5-custom-agent
custom_agent; ls · uv run adk web · reload localhost:8000 · pick baseline". Hold 2 s.
SAY: And if L-L-M rag's Chroma still holds port 8000, they clash; the web server stopped: address already in use. Run docker compose down first, or add dash dash port 8080. Pause, and get the dev UI open on baseline.

---

## S11 · Runner, session, state: the shared whiteboard — `s11_state.py` · `SharedState`

Lecture: 40–41 (and 20–22).

SHOW: TRACKER Base 1. CODE(llm-agent-google-adk/1-baseline/agent.py: 14–19) (header `1-baseline/agent.py ·
lines 14–19`, subtitle "your copy: baseline/agent.py"), then Transform to lines 21–26. LECTURE 40–41: the
mini-map grows to the right third and labels the constructor's arguments with slide 41's blocks:
`model=` → LLM core (BLUE), `instruction=` → Instructions, `tools=` → a GREY dashed "none here",
`output_key=` → Memory "within one session".
SAY: Baseline holds three LLM agents, each with a model, an instruction, and an output key. In the lecture's blocks: the LLM core, the instructions, and no tools at all.

SHOW: CODE(llm-agent-google-adk/1-baseline/agent.py: 35–39) (header `1-baseline/agent.py · lines 35–39`;
the summarizer itself appears in V6): `SequentialAgent(…)` highlights PURPLE, and the mini-map's Dynamic
Control fills PURPLE "Runner + SequentialAgent". Then an extra card: "ask the server for the agent tree the
UI loads", and a full-width terminal (title `laptop · second terminal`, prompt
`student@laptop:~/AC215/llm-agent-google-adk$`; adk web keeps the first) prints
TERM(adk-laptop/31-x-select-baseline.txt: 2–5; each line cut after its instruction's first sentence);
`model gemini-2.5-flash` is boxed YELLOW in the three agent rows, with a YELLOW tag above the terminal, "from your
root .env · yours: the model you set", and a GREY tag beside the tree's last row, "the capture kept .env.example's
2.5-flash". The YELLOW tag's border flares at "check yours".
SAY: A sequential agent runs them in order: validator, planner, summarizer. An extra request shows the tree the UI loads, with the model from your root dot env; check yours.

SHOW: TRACKER Base 1 · extra. In the second terminal it types `curl -s -X POST
http://localhost:8000/apps/baseline/users/student/sessions; echo` (extra; folds) →
TERM(adk-laptop/32-x-new-session.txt: 2; wrap); `"state":{}` and `"events":[]` highlight GREEN; the id gets
`your numbers will differ`. V6 starts above a strip: a GREEN whiteboard with three empty cells
`itinerary_validation`, `travel_plan`, `trip_summary`, and an empty events column beside it.
SAY: Another extra request creates a session: an empty state, and no events yet. Think of the state as a shared whiteboard.

SHOW: V6, captioned throughout "what ADK does once you add your key · no model output was recorded", tag
`illustration`. A PURPLE Runner takes a GREY message card (the request of `adk-laptop/33` line 1: "2 adults,
Boston to Montreal, Oct 30 - Nov 2, 1500 dollars, train preferred"); `ItineraryValidator` (a BLUE model chip
and its instruction card) answers, and its reply (a blank GREEN card, no text) flies into cell 1 along a
label `output_key`; an event block stacks in the column. `TravelPlanner`'s instruction card shows `Using
{itinerary_validation}, …` with a PINK hole; cell 1's card flies into the hole before its BLUE chip lights;
its reply fills cell 2.
SAY: Once you add your key, the Runner does this. The validator's reply goes into the state, under its output key; before the planner runs, its instruction's placeholder is filled from that cell.

SHOW: `TripSummarizer` reads `{travel_plan}` the same way and fills cell 3; three event blocks stand in
the column, labelled "the Events tab". Between the agents, a GREY crossed-out arrow "no calls between
agents"; a thin GREY line runs from the events column into each instruction card, labelled "history" (each
agent also sees the earlier agents' replies; see the note for scene authors). A GREY dashed coda (tag
`concept · module README only`): `ParallelAgent` fills three cells at once on three branch lines.
SAY: The summarizer reads the plan the same way. The agents never call each other: the session carries the data, in its state and its history of events. A parallel agent fills its cells at once.

SHOW: LECTURE 20–22. The lecture's Paris request card (from S01) appears beside the pipeline; its "live
systems" and "tools that act" chips find nothing to attach to: `tools=` stays a GREY dashed "none".
Caption "costs: the model's own estimates".
SAY: The lecture's planner needs live systems; this pipeline has no tools, so its prices are the model's guesses. A later notebook gets prices from tools and sums from Python.

SHOW: LECTURE 40–41. A README chip (header `README.md · line 140 (excerpt)`, tag `expected`): "Memory:
Structured state tied to a session_id"; beside it a GREEN box "session state · one session" (the
whiteboard with its three cells); then a second, empty board slides in labelled "new session" while the
first dims: nothing carries over. A GREY dashed box "memory across sessions · the lecture's sense · not in
today's runs" holds a small copy of the Cheese Quiz's "profile from past sessions" sheet, tagged "typed
into the notebook (cell 42)".
SAY: The ADK README calls this memory. The code calls it session state, and it lasts one session; the lecture's memory remembers you next time, which none of today's runs does.

SHOW: An extra card: "send a trip request with the placeholder key (POST /run)" →
TERM(adk-laptop/33-x-send-placeholder-key.txt: 2) `Internal Server Error`; the server strip shows
TERM(adk-laptop/29-x-adk-web-renamed.txt: 357–363 joined, cut after "Please pass a valid API key.";
wrap) RED; tag `real run · placeholder key`.
SAY: Without a real key, a trip request gets an internal server error. The server log says why: API key not valid. The placeholder reached Google, and was refused.

SHOW: A GREY "with your key, look for" card, items writing in as named: "three replies, in order", "State
tab: itinerary_validation · travel_plan · trip_summary". PANEL(adk-laptop/29-x-adk-web-renamed.txt: 41–42
joined, "adk web log") with `baseline/.adk/session.db` highlighted PINK "a file in the agent's folder".
Then `▶ your turn` on a static GREY card "pick baseline · send a trip request, e.g. "2 adults, Boston to
Montreal, Oct 30 - Nov 2, 1500 dollars, train preferred"", its last line GOLD "3 Gemini calls per request ·
free tier has limits". Hold 2 s.
SAY: With your key, look for three replies in order, and three new entries in the State tab; the session is a file in the agent's folder. Each request is three model calls: pause, and plan a trip.

---

## S12 · Tools you didn't write: MCP — `s12_mcp.py` · `McpPlugs`

Lecture: 51–53.

SHOW: LECTURE 51. No tracker. Three bins write in (slide 51, our words): "data · fetch", "action · change
something", "orchestration · hand work to an agent". Tool chips drop in as named: `get_book_by_author`,
`web_search`, `read_file` → data; `finalize_itinerary`, `send_email` → action (GREY tags "trip planner",
"newsletter"); `research_facts`, `researcher_agent` → orchestration.
SAY: The lecture sorts tools into three families. Data tools fetch, like our book searches; action tools change something, like finalizing a trip or sending email; orchestration tools hand work to another agent.

SHOW: LECTURE 52. One agent box with four tool pills; ten GREY wires fan out to ten service boxes in a
right-hand column, labels ≥ 20 pt (our redrawing of slide 52's protocol labels, no brands): "email ·
SMTP/IMAP", "calendar · CalDAV", "search · REST", "database · SQL/NoSQL", "an API · REST", "files · File
I/O", "drive · Drive API", "maps · Maps API", "chat · chat API", "messages · messaging API". A GREY caption
"Do you see a problem?". In the 5 s of silence after the SAY (`self.wait(5)`, no timer), a small GREY block
"custom code" grows on each wire, one after another, and a counter "10 integrations" ticks up.
SAY: Now wire one agent to ten services, each with its own protocol. The lecture asks: do you see a problem?

SHOW: LECTURE 53. Morph: the agent box becomes "MCP host" with small "client" ports; the ten wires merge
into one PINK trunk labelled "same protocol" (never a box); an "MCP server" adapter clicks onto each
service.
SAY: Every tool becomes a custom integration. MCP, the Model Context Protocol, makes it one pattern: a host with clients, and an MCP server for each service.

SHOW: The trunk splits into three separate PINK plugs, each its own connection: "stdio · a child
process", "HTTPS · a remote URL", "HTTP · a thread on :8001". Caption "one protocol · one connection per
server". The lecture tag stays.
SAY: The lecture's MCP box is a shared protocol, not a program you run. In code, each server is its own plug, and the tutorial has three.

SHOW: TRACKER Mcp 1. A README card (header `3-mcp-tools/README.md · lines 56–63`, tag `expected`), not
typed: `brew install node` (macOS) · `sudo apt install nodejs npm` (Ubuntu) · "Windows: nodejs.org"; a GREY
chip under it "Ubuntu 22.04's apt Node is v12: too old for MCP servers · use nodejs.org (recorded with
v24.22.0)". A terminal strip (title `laptop · second terminal`; adk web keeps the first): it types `node
--version; npx --version` (extra) → TERM(adk-laptop/34-x-node.txt: 2–3), tag `at the time of recording`.
SAY: Plug 1 is in the ADK module on MCP. Install Node.

SHOW: The README card and the strip leave. CODE(llm-agent-google-adk/3-mcp-tools/agent.py: 20–29) in the
left two thirds (header `3-mcp-tools/agent.py · lines 20–29`, subtitle "your copy: mcp_tools/agent.py"):
lines 23–24 PURPLE, line 28 `tool_filter` YELLOW. In the right third, the picture: a PINK stdio pipe from a
PURPLE ADK process into a PURPLE `npx … server-filesystem` child process on the GREY laptop.
SAY: The agent's toolset starts a filesystem server with npx, as a child process, talking over standard input and output.

SHOW: An extra card: "ask the agent's own toolset for its tools · no model involved" (second terminal) →
TERM(adk-laptop/35-x-mcp-toolset.txt: 21, 30, 31 cut after "14 [" + `…]`, 32–37). V7: 14 GREY tool chips
fall onto a sieve labelled `tool_filter`; `list_directory`, `read_file`, `search_files` pass GREEN,
`write_file` and `edit_file` bounce off. TRACKER Mcp 2: a GREY "with your key:" card "pick mcp_tools · ask:
List files in this directory → a list_directory call in the Events tab, and the five entries below (`35`
lines 33–37), plus `[DIR] .adk` (the session folder: picking the agent creates it, `29` line 42)".
SAY: An extra script asks that toolset for its tools, with no model involved. The server offers 14, including write and edit, and the filter lets three through. With your key, ask the agent to list files.

SHOW: TRACKER CQ-Tools 1, then CQ-Tools 2. A BLUE Colab frame.
RECORDED(expected/colab-cheese-quiz-c50-tools-called.txt: 3–6) small (tool name masked), caption "step 1: a
Python function with @function_tool (cell 48)". A GREY chip "Colab disconnected? rerun Prerequisites first".
Then CODE(colab/cheese-quiz/cell-54.py: 2, 10–13, 17, 26–27) folded (header `Cheese Quiz · cell 54 · lines
2–27 (folded)`, ≤ 12 rows, URL masked to `https://‹instructor›-fun-facts.dlops.io/mcp`):
`MCPServerStreamableHttp(` and `params={"url": …}` PINK; line 27 `mcp_servers=mcp_servers,` YELLOW "not
tools=". The picture: a PINK HTTPS line from the BLUE Colab VM to a BLUE remote server box.
SAY: Plug 2 is back in the Cheese Quiz. After a first tool written as a plain function, the notebook connects to a remote MCP server by URL, passed as MCP servers, not tools.

SHOW: The HTTPS line from the Colab VM to the remote server box stays up. One extra card lists the four
requests once ("an extra check · in the study guide": a browser's plain GET, initialize, tools/list,
tools/call). A strip (second terminal) prints only the browser's GET: TERM(mcp-remote/01-x-browser-get.txt:
2, 10; wrap) `HTTP/2 406` and "…Client must accept text/event-stream", RED. Then three small envelopes
travel the line, each returning with one excerpt chip: "initialize" → `"protocolVersion":"2025-06-18"` (`02`
line 3, with `"version":"1.16.0"`); "tools/list" → `"name":"‹instructor›_fun_fact_mcp"` (`03` line 3);
"tools/call" → the `"fact"` text of `04` line 3 as in the file, tag `your numbers will differ` "a new fact
each call".
SAY: Extra curl commands talk to that server. A browser's plain request gets 406: the server is up, but speaks MCP, not web pages. Then initialize, list tools, call: one tool, one cheese fact per call.

SHOW: TRACKER CQ-Tools 3, subtitle "Build your own MCP Server (Optional)". CODE(colab/cheese-quiz/cell-57.py:
2, 5–6, 11, 14) folded (header `Cheese Quiz · cell 57 · lines 2–14 (folded)`, 8 rows, names masked; line 11
without its emoji, see the note for scene authors): line 14 `port=8001` GREEN; line 11 with an `erratum`
chip "the comment says port 8000"; RECORDED(expected/colab-cheese-quiz-c57-fastmcp-server.txt: 3)
`…127.0.0.1:8000/mcp` as a one-line chip under it, GREY tag "saved from an older version of the cell". Then
the panel leaves and RECORDED(expected/colab-cheese-quiz-c59-local-mcp.txt: 3–10) prints beside the
picture: `"POST /mcp HTTP/1.1" 200 OK` lines interleaved with `‹instructor› Fun Fact Tool Called`; a PURPLE
FastMCP thread on `127.0.0.1:8001` inside the BLUE Colab VM.
SAY: Plug 3 is optional: the notebook runs its own FastMCP server, in a thread, on port 8001. A small slip: the comment above says 8000, and so does an older saved output.

SHOW: The three plugs side by side; in each, the BLUE model chip only emits a BLUE call card, while a
PURPLE client process does all the talking along the PINK lines. Then `▶ your turn` on a static GREY card:
"no Node? `brew install node` · or nodejs.org" · `node --version; npx --version` (extra) · "dev UI: pick
mcp_tools, ask "List files in this directory" · with your key" · "Cheese Quiz › Tools, MCP: every cell (Build
your own MCP Server is optional)" · GREY "first run times out? warm the npx cache once:" · `npx -y
@modelcontextprotocol/server-filesystem .` "Ctrl+C, then retry" (digest G12) · last line GOLD "OpenAI calls ·
paid". No GREY "your turn" header. Hold 2 s.
SAY: Notice who does the talking: your client process. MCP gives the model no network access; it still only writes calls. Pause, and run the MCP cells.

---

## S13 · Many agents: who plans the order? — `s13_many.py` · `ManyAgents`

Lecture: 44–49 (and 38).

SHOW: LECTURE 44–49. A GREY dashed tree (our redrawing, tag `concept · lecture example`): "lead agent" →
"planner" → three parallel "web search" agents → "synthesis" → "report". Beside it, two tutorial trees with
plain-word nodes ≥ 20 pt: the Guild, a BLUE "orchestrator" over GREEN chips "facts", "write", "review",
"vegan"; the Newsletter, a BLUE "orchestrator" over "researcher", "editor", "send_email".
SAY: In the lecture, deep research is a tree of agents: a lead agent, a planner, parallel web searchers, and a synthesis into a report. The tutorial builds trees like it: the Cheese Quiz Guild, and the newsletter.

SHOW: LECTURE 38. The three trees fade. A YELLOW question "Who plans the order?" writes in at the top, three
empty slots in a row under it: "the code", "the model", "Python reading the model's label". Slot 1 opens
alone: CODE(llm-agent-google-adk/1-baseline/agent.py: 35–39) (header `1-baseline/agent.py · lines 35–39`,
subtitle "your copy: baseline/agent.py") and an assembly line of three GREY stations; then it shrinks into
its slot as a small assembly-line icon before slot 2 opens (the same for slots 2 and 3).
SAY: The lecture's planner raises the question that sorts them: who plans the order? First answer: the code. The sequential agent is an assembly line, its order fixed in Python.

SHOW: TRACKER CQ-Guild 1, then CQ-Guild 2. Slot 2: CODE(colab/cheese-quiz/cell-68.py: 1–8) (header
`Cheese Quiz · cell 68 · lines 1–8`): `.as_tool(` highlights on each line; a whole agent shrinks into one
tool chip, which drops into a small GREY "orchestration" bin, redrawn from the MCP scene.
SAY: Second answer: the model. In the Guild, each specialist becomes a tool: a whole agent behind one function. An orchestrator decides which to call.

SHOW: CODE(colab/cheese-quiz/cell-70.py: 4–5, 9–11) folded (header `Cheese Quiz · cell 70 · lines 4–11
(folded)`, 8 rows): "Follow the assembly line strictly" and "(Make at most 2 total review rounds.)"
highlight YELLOW with a GREY tag "a rule in prose · no code enforces it". A chip
CODE(colab/cheese-quiz/cell-71.py: 6) `orchestrator, prompt, max_turns=12` GREEN.
SAY: Its instructions say: follow the assembly line strictly, at most 2 review rounds. That's a rule in prose; no code enforces it, except a cap of 12 turns.

SHOW: TRACKER CQ-Guild 3. RECORDED(expected/colab-cheese-quiz-c75-guild-star-wars.txt: 3–5, 7, 13) (the
display line as a GREY label "a quiz widget", then the first question's text): three RED
`ERROR:openai.agents:Error getting response` lines, then a GREY tag "a quiz anyway". The Guild tree returns
small: three RED "?" marks flash on its hops, with a GREY tag "which calls failed: not in the log"; GOLD
ticks on every hop. They fade; `▶ your turn` on a static GREY card "Cheese Quiz Guild: every cell, from
Some Utils to Example 2", its last line GOLD "hosted web search · paid". Hold 2 s.
SAY: The staff's saved run logged three errors getting a response, and still produced a quiz; the log doesn't say which calls failed. Every hop adds cost, time, and a way to fail; pause, and run the Guild.

SHOW: Slot 3: CODE(llm-agent-google-adk/5-custom-agent/conditional_agent.py: 85, 89, 94, 99) folded (header
`5-custom-agent/conditional_agent.py · lines 85–99 (folded)`, subtitle "your copy:
custom_agent/conditional_agent.py", 8 rows, font 20 so it fits above the card): line 85 `complexity =
ctx.session.state.get("query_complexity", "simple")` PINK; lines 89, 94, 99 YELLOW, each with a GREY label
at its right: "→ simple handler", "→ complex handler", "→ clarification handler". A small GREY chip
"classifier: output_key="query_complexity" (line 171)" and a GREY chip "code only · running it:
exercises.md". The ponder card sits in the lower third.
SAY: Third answer: Python, reading the model's label. In this custom agent, a classifier writes one word into the state, and plain if statements pick the handler.
PONDER(6 s, "The classifier answers \"Simple\", with a capital S.\nWhich handler runs?")

SHOW: Line 89 `if complexity == "simple":` gets a RED cross against "Simple"; line 94 a RED cross; line 99
`else:  # ambiguous` lights → "clarification handler". A GREEN fix chip `complexity.strip().lower()` ·
"or a structured output (exercises)".
SAY: The else branch: clarification. The comparison is exact; lowercase the label first, or ask for structured output. The exercises try both.

SHOW: A GREY dashed chip "handoffs" (tag `concept · lecture only`) slides into the small orchestration bin,
with a GREY note "lecture 7 · slides". Fade out.
SAY: The lecture also lists handoffs among the orchestration tools. These tutorials use agents as tools; lecture 7 sketches handoffs.

---

## S14 · The harness: only a human says yes — `s14_approval.py` · `ApprovalGate`

Lecture: 20–22, then 36–37.

SHOW: TRACKER TP 1 → 3. A BLUE Colab frame (title "Travel Planner", tag `illustration`).
CODE(colab/travel-planner/cell-08.py: 2) `%pip install -q "openai-agents==0.3.2"` GREEN "pinned". LECTURE
20–22: the Paris request card (from the hook) shrinks into a small GREY box "mock catalog" reading "3
cities · 6 hotels · prices in cents · 5 search tools + finalize" (from `cell-12.py: 6–18`, `cell-14.py`,
`cell-21.py: 28–34`; no code chips). A GREY excerpt chip of
RECORDED(expected/colab-travel-planner-c27-turn4-yes.txt: 5) "Nothing has been booked."
SAY: The Travel Planner notebook rehearses the lecture's trip. Copy it, add your key, and install its pinned agents package. Paris shrinks to a mock catalog: 3 cities, 6 hotels, 5 search tools and a finalize tool, booking nothing.

SHOW: TRACKER TP 4 → 6. Three compact turn cards (tag `recorded · the staff's last saved run`): Turn 1
RECORDED(expected/colab-travel-planner-c24-turn1.txt: 3, 4 cut after "Los Angeles?"); Turn 2 the five
`[tool]` lines of RECORDED(expected/colab-travel-planner-c25-turn2.txt: 3, 31, 59, 73, 87) counted 1–5,
then line 109 `Kind: options`; Turn 3 RECORDED(expected/colab-travel-planner-c26-turn3.txt: 3–5).
SAY: In the staff's saved run, turn 1 asks which California city. Turn 2 runs five searches and offers options. In turn 3 the user picks, the model calls finalize, and the reply shows the exact plan and asks for a yes.

SHOW: V8: a GREEN plan card (RECORDED(c26: 6–19), the exact proposal JSON, small) walks toward a door marked
FINAL; a turnstile stops it and stamps it YELLOW `PENDING`. CODE(colab/travel-planner/cell-15.py: 36–42)
(header `Travel Planner · cell 15 · lines 36–42`, subtitle "Finalize Plan Tool", 8 rows; the comment above
it would state the ponder's answer): lines 36–42 highlight. The BLUE model pushes the card again in the same
turn: the same stamp.
SAY: That's the gate. A finalize call from the model can only propose: if the plan isn't the approved one, the code stores it as pending, and returns needs confirmation.

SHOW: CODE(colab/travel-planner/cell-18.py: 55, 59–61) folded (header `Travel Planner · cell 18 · lines
55–61 (folded)`, subtitle "Business Logic", ≤ 8 rows; the docstring on line 56 would state the answer):
`prompt` on line 55 PINK; line 61 GREEN "pending → approved". The turnstile shrinks to the top right,
PENDING showing. A GREY `person_icon` "the human". The ponder card sits in the lower third.
SAY: Approval lives in a separate function, apply confirmation: only an explicit yes copies pending to approved.
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
SAY: Turn 4: the human types yes. The stamp flips to approved, finalize runs, and Python builds the budget line by line: 2,690 of the 6,000 dollars. The notebook's own test checks Python's number.

SHOW: CODE(colab/travel-planner/cell-18.py: 129–135) (header `Travel Planner · cell 18 · lines 129–135`,
11 rows): lines 129–131 RED "hard guardrail: raise"; lines 133–135 YELLOW "soft guardrail: warn".
SAY: What the user sees comes from checked state, not the model's prose. An itinerary that skipped the check raises an error, a hard guardrail; a dollar amount in the model's prose only prints a warning, a soft one.

SHOW: LECTURE 36–37. Two GREY cards (slides 36–37, our words): a prompt card "instructions" with a sticky
note "success criteria" (slide 36), and a "decision maker" card with a sticky note "guardrails" (slide 37);
each note gets GREEN copies in code: "approval gate", "Python's budget", "checked render", the gate sitting
on the action tool `finalize_itinerary`. The cards fade. TRACKER TP 8; `▶ your turn` on a static GREY card
"Travel Planner: every cell in order, Install OpenAI Agents SDK to Turn 4 · the last cell, Start an
interactive conversation, is optional: type exit to leave", its last line GOLD "OpenAI calls · every
turn". Hold 2 s.
SAY: The lecture puts success criteria in the instructions, and guardrails in the decision maker. This notebook keeps both in code the model can't talk its way past, on the action tool. Every turn is paid; pause, and run the four turns.

---

## S15 · The harness: success is a receipt — `s15_receipt.py` · `Receipt`

Lecture: 36–37 (and 10–12).

SHOW: TRACKER NL 1 → 3. A BLUE Colab frame (title "Cheese Newsletter · Harness", tag `illustration`). With
the menu path, a GREY two-line caption under the cell-8 chip, "first open it: course site · Lecture 6 · Tutorial
3, / or the Cheese Newsletter link in the study guide", until "In the users cell". A small chip
CODE(colab/cheese-newsletter/cell-08.py: 3) `"agent-framework-core==1.18.0" \` "pinned".
CODE(colab/cheese-newsletter/cell-16.redacted.py: 6–12) (header `Cheese Newsletter · cell 16 · lines
6–12`): lines 8–9 `<reader1>`, `<reader2>` YELLOW "you and a friend"; lines 10–11 GREY "commented out";
line 6's "Email is preview-only" GREEN.
SAY: The last notebook writes a cheese newsletter per reader, with Microsoft's Agent Framework, pinned. In the users cell, put in yourself and a friend, and keep two entries. Email is preview only; nothing is sent.

SHOW: TRACKER NL 4. CODE(colab/cheese-newsletter/cell-25.py: 5, 8, 12–16, 25) folded (header `Cheese
Newsletter · cell 25 · lines 5–25 (folded)`, subtitle "Orchestrator Agent", 11 rows): line 5 `gpt-5.6-luna`
BLUE; line 8
`"max_iterations": 16` PURPLE; lines 13–15, the three tools, GREEN; line 25
`"allow_multiple_tool_calls": False` "one at a time".
SAY: The orchestrator gets three tools: a researcher with web search, an editor, and send email. At most 16 iterations, one tool call at a time.

SHOW: TRACKER NL 5. RECORDED(expected/colab-cheese-newsletter-c27-run-demo.txt: 4–11) (readers as in the
file): the four `[tool] editor_agent` lines get a YELLOW bracket "×4"; line 10 `send_email`; line 11
`Saved HTML: … (8005 bytes). No email sent.`. A chip CODE(colab/cheese-newsletter/cell-16.redacted.py:
114–116) "every draft is validated · errors go back as the tool's result". Then line 30 `Created 4 mock
emails. No email was sent.` with a GREY tag "saved run: 4 readers · today's list: 2".
SAY: In the staff's saved run, the first city took four editor calls; the code validates every draft and hands any errors back as the tool's result. Then send email wrote the HTML to a file. That run had four readers; today's list makes two.

SHOW: LECTURE 36–37. V8: a newsletter draft card and the BLUE orchestrator's speech bubble "done!"; a door
marked SUCCESS stays shut. CODE(colab/cheese-newsletter/cell-18.py: 118–120, 123–124) folded (header `Cheese
Newsletter · cell 18 · lines 118–124 (folded)`, subtitle "Business Logic", 9 rows): line 119 `if
context.receipt is None:` → RED "no receipt → error"; line 123 `if not Path(receipt["path"]).is_file():` →
RED "file missing → error"; line 120's `{reply}` GREY "the model's words appear only inside the error". A
GREEN receipt token with a file path drops into a slot; the file exists; the door opens.
SAY: Now the harness. When the orchestrator stops, Python ignores its words and checks two things: is there a receipt from send email, and is that file on disk? If not, the run fails; success is a receipt, not a claim.

SHOW: TRACKER NL 6. CODE(colab/cheese-newsletter/cell-22.py: 16) (header `Cheese Newsletter · cell 22 ·
line 16`, subtitle "Editor Agent") becomes a GREY sticky note on the prompt; it drifts through the gate
unchecked. RECORDED(expected/colab-cheese-newsletter-c30-preview-1.txt: 26 cut to `…Promotion URL:
https://…`), the URL RED, tag `erratum` "a rule that matters belongs in validate_newsletter". Caption "a
note is not a check".
SAY: Compare a rule that lives only in the prompt. The editor is told: no embedded URLs. The saved preview has one anyway, because no code checks for it; a note is not a check.

SHOW: LECTURE 10–12. Two GREY dashed boxes (tag `concept · lecture only`): "Self-RAG: relevant? supported?
useful?" and "Corrective RAG: grade the documents", caption "don't trust: check". A GREY dashed chip
"Lecture 7: the harness". They fade; `▶ your turn` on a static GREY card "Newsletter: every cell in order ·
edit USERS (keep 2: the second preview shows reader 2) · Run Demo · the two previews", its last line GOLD
"web search · billed per call". Hold 2 s.
SAY: The lecture's Self-RAG and Corrective RAG grade their retrieval for the same reason: don't trust, check. Next lecture calls this outer layer the harness. Web search is billed per call; pause, and run the demo.

---

## S16 · Tear down, recap, and what's next — `s16_recap.py` · `Recap`

Lecture: 41 (and 32–33).

SHOW: TRACKER RunAg 1 · extra. The ADK terminal (strip), running the restarted server: Ctrl+C →
TERM(adk-laptop/29-x-adk-web-renamed.txt: 364, 367–369) `ADK Web Server shutting down...`. It types `git
status --short; git status --short --ignored | grep '^!!'` (extra; folds) →
TERM(adk-laptop/39-x-git-status.txt: 2, …, 16–21, …, 24) in a 12-row terminal: `?? .python-version` GREEN "your
pin"; `!! .env`, `!! .venv/`, `!! uv.lock` GREY "ignored"; the second `…` (the two `__pycache__/` rows) turns GREY
with the ignored rows under one GREY bracket.
SAY: Tear down: control C stops the web server. An extra git status shows the renamed folders and your Python pin; dot env, the virtual environment and the lock file are ignored.

SHOW: A RED-outlined ghost folder `baseline/.adk/` "sessions · not in .gitignore" (from the log line
`29` lines 41–42); a GREY chip "add .adk/ to your ignore file (exercises)"; a GREY two-row chip "`.venv` · 1.6 GB ·
delete when done / on a Linux PC: about 3 GB more (CUDA)".
SAY: The sessions in the agent's dot ADK folder aren't ignored, so don't commit them, and delete the 1.6 gigabyte virtual environment when you're done.

SHOW: A BLUE Colab frame with Runtime › Disconnect and delete runtime (tag `illustration`), ticked three
times: "Cheese Quiz", "Travel Planner", "Newsletter". Three GOLD key glyphs in a row: "service account · in
secrets/ beside llm-rag", "AI Studio key · root .env", "OpenAI key · Colab Secrets only"; each gets a GREY
"delete or cap when the course ends". A GREY chip "llm-rag: stopped in part 1"; a GOLD chip "tried
6-rag/1-vertex-rag-engine? its corpus is billable · exercises.md deletes it".
SAY: In each notebook, disconnect and delete the runtime. Keep the service account key beside L-L-M rag, never inside, and delete or cap the other two keys when the course ends.

SHOW: LECTURE 41. The anatomy (V1) full size, each block filling with two or three of the tutorial's
objects as the SAY names it (GREY code chips, ≥ 20 pt, so they fit): LLM core `gemini-3.1-flash-lite`,
`gpt-4o`; Instructions `instruction=`, `output_type`; Tools `FunctionDeclaration`, `MCPToolset`,
`.as_tool`; Memory "message history", "session state · one session".
SAY: Here's the lecture's anatomy, filled with today's code. Gemini and OpenAI models as the core; prompts and output types as instructions; tools by hand, decorated, or over MCP; history and session state as memory.

SHOW: Dynamic Control fills PURPLE with `Runner`, `max_turns=12`, and a TEAL chip "llm-rag: two calls by
hand". LECTURE 32–33: the lecture's formula writes in under it (our words):
"agent ≈ LLM + reasoning + instructions + tools"; two GREEN chips append: "+ a loop the framework runs",
"+ checks your code enforces".
SAY: Dynamic control is the framework's loop, or two calls by hand. The lecture's formula, LLM plus reasoning, instructions and tools, gains two pieces: a loop the framework runs, and checks that your own code enforces.

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
