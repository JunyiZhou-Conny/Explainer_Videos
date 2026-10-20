# AC215 · Lecture 5 — Introduction to RAG (follow-along: llm-rag) — narration script & visual plan (v2)

Audience: an AC215 student who has done L1–L4 (VMs and uv; a given Dockerfile and Docker Hub; the
mega-pipeline with a service-account key, `docker-shell.sh` and the `../secrets` mount; port_toy's
container networks, name lookup, published ports and Compose). They know Python and basic ML and
have used an LLM, but have never built a retrieval system or used a vector database. They watch
with their clone of `dlops-io/llm-rag` open in `~/AC215/llm-rag` (beside `~/AC215/secrets`), pausing
to type every command.

Goal: after the video they can say what RAG is (retrieve, then generate; the model is unchanged)
and why the lecture rejects pasting every book into the prompt and fine-tuning for this job; draw
the two lanes that share one embedding model and one database and put each `cli.py` flag in its
lane; set up the folders, the service account, the key, the Vertex AI API and `GCP_PROJECT`; start
the two-container app with `sh docker-shell.sh` and read `docker-compose.yml` as a picture
(network by name, a published port, three bind mounts), recognizing the harmless first-run "not
found", the run-container's real name and the two ways the start goes wrong; run both chunkers,
predict the char-split count and explain recursive-split's hidden overlap; explain an embedding as a
direction, cosine similarity versus Chroma's cosine distance, the 256 numbers and why query and
chunks share one model; load a collection and say what a record holds, why load always rebuilds,
what an index is for and where the database lives; read a query whose filters act before ranking;
explain the chat prompt and its missing system instruction; explain semantic chunking and why it
needs the API at `--chunk`; name the lecture's other levers; tear down and know why an index goes
stale.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `SLIDES.md` (the
lecture: decks A and B, binding next to the digest, docs/AC215_SERIES.md rule 9), `assets/` (see
`ASSETS.md`). Where the digest and the captures disagree, the captures win (BRIEF.md's table); where
the slides and the captures disagree, the captures decide what is shown and the SAY says so kindly.
Nothing in a terminal panel is typed by hand: every output line below names its capture file and
line numbers. v1 was written from BRIEF.md; v2 merges the four review lenses (accuracy,
follow-along, pedagogy, spoken flow; `build/review_merge_log.md`).

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–5 short
  sentences, at most about 60 words) and become the subtitles. Plain spoken English: no backticks,
  no symbols; commands, flags and paths are on screen and said in words ("dash dash chunk", "chunk
  type char split", "slash app", "the docker volumes folder"). File names with a lexicon entry
  (cli.py, docker-shell.sh, docker-compose.yml, pyproject.toml, uv.lock) are said as words. The repo
  and container names are said "L-L-M rag", "L-L-M rag CLI", "L-L-M rag chroma D-B"; the key file
  "L-L-M service account dot JSON". A command is never the bare subject of a sentence: "the docker
  ps command shows", "an extra command called get", "the load step". Numbers as digits ("10
  results", "11 files"); only S01's story beats say "eleven books" and "ten pages". Never a "!"
  after a digit. Versions that will change are said with "at the time of recording" (Docker 29.8.2,
  Compose 5.6.0, Python 3.12.15, uv 0.13.1, the Chroma server). Dates in American order ("October
  16, 2026"). IDs: write `ID` / `IDs` (espeak reads ID as I-D; `IDs` has a lexicon entry), never
  `I-Ds`.
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the split drives the TTS gaps, the subtitle cues and the Chinese alignment).
  No sentence opens with a command or a lower-case file name. No `'s` on a word with a lexicon entry
  and none after a digit. Never put "a" right before a word with a lexicon entry (the entry splits
  the sentence and "a" becomes the letter A: "a zip download", never "a ZIP"). A lone letter is
  never a sentence subject (Kokoro reads "A" as "uh"): the personality game says "the first
  candidate". No sentence opens with "Ours". "dash a" ends its phrase. Sentences stay under 30
  words. Spelling American on screen and in the SAY ("gray", "neighbors", "visualizer"; the colour
  constants stay GREY etc.).
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, a silent ponder timer of n seconds; the card is
  removed at the start of the next block, whose SAY gives the answer. Five in the video (S06, S07,
  S08, S12, S14), as in BRIEF.md. The card sits in the lower third (y ≈ −2.2) so the picture above
  it stays visible: build it with `ponder_card(...)` and place it yourself, as
  `ac215-l02-containers-1/scenes/s09_run.py` does (`pause_and_ponder` centers it). The picture
  during the timer never shows the answer.
- `LECTURE A16–A19` (or `B5`, `A63`): from that SAY block on, the GREY `lecture_ref(5, "A16–A19")`
  tag (`explainer.devops`) sits top right: "Lecture 5 · slides A16–A19". A = the main deck
  ("Introduction to RAG"), B = the supplement ("Advanced RAG"); S01 explains the tag once, with an
  on-screen caption for A and B. The tag changes
  or leaves when the SHOW says; a scene with `Lecture: none` never shows it. The slides themselves are
  never shown: every lecture picture below is our own redrawing in the series colours. At most one
  short spoken bridge to the lecture per scene.
- `TERM(folder/file: lines)`: a terminal beat. The scene types the command written just before it in
  the SHOW line (in backticks, exactly as the README spells it; extras exactly as captured), then
  prints those lines of `assets/terminal/folder/file`. Line 1 of every capture is its `$ …` command
  and is never printed; the `[exit N]` line is never printed. In the line list: `…` = print one `…`
  line; `wrap` = fold long lines (`Terminal.print(..., wrap=True)`); without `wrap`, a line longer
  than a row is cut with `…`; `N cut after "x"` = print line N only up to and including x.
  `session` = a capture whose lines include prompts (`laptop/07`, `23`, `gotchas/01`): a listed line
  that starts with a prompt is not printed as output; the scene sets that prompt and types the
  command after it. `→ (no output)`: the prompt simply returns.
- Captures whose `$` line joins commands with `;` are typed as one line exactly as captured (all
  are extras; long ones fold onto two rows), except `laptop/15` (two `docker inspect` commands, typed one after the
  other, each folding onto two rows).
- Multi-line extras (`python - <<'EOF' … EOF` in `recorded-embeddings/06`, `07`, `08`, `09`) are
  never typed. They appear as a GREY card "an extra Python check · in the study guide" holding the
  one-line purpose the SHOW gives, and the output prints in a terminal from the listed lines. Their
  code is never on screen (two of them name a book's author in variable names and labels). (The
  study-guide refresh must add these four checks; see the merge log.)
- BuildKit live-view rows (`laptop/07` lines 10–35) are 79 characters, so they print cut at 65
  without their time: the row's last field (`line.split()[-1]`, e.g. `81.5s`) becomes a small GREY
  tag at the row's end. The line lists never include `[internal]` rows, `[1/6] FROM`, `resolve`, or
  `=> =>` sub-lines, except line 21 `transferring context: 112.26MB`. BuildKit's `[k/6]` steps are
  *build step k* in the SAY and get a TEAL badge; *step k* alone is always the README tracker's step.
- Wide tables. `docker ps` / `docker ps -a` (`laptop/08`, `20`; 126–169 characters) print as a
  *column view*: each line keeps only its PORTS and NAMES fields (the capture's own text, sliced,
  not retyped), header "docker ps · PORTS and NAMES". `docker images` (`laptop/14`, `26`) keeps IMAGE
  and DISK USAGE, header "docker images · IMAGE and DISK USAGE". `ls -la` rows longer than a row are
  cut with `…` (the owner and size stay visible).
- Terminal renders wrap at 80 columns: a line that ends mid-word and continues on the next is one
  output line. Join such pairs before printing (`laptop/07` 7–8, `21` 2–3, `25` 2–3, `gotchas/01` 2–3 and
  its traceback pairs). `laptop/05` line 6 is cut instead (see "Names on screen"). Line numbers here still name the file's own lines.
- Terminal width. Every terminal is the house `term()` (12.6 wide, 22 pt, 65 characters a row),
  always full width, at most 13 rows. A typed command is never cut: it folds at a space onto an
  indented second row ending in ` \` (`Terminal.type`). When a picture needs the frame, the
  terminal shrinks to a 3-row strip along the bottom edge (the last command and its key output
  line). Never half width; a second panel goes above the strip, never beside a full-width terminal.
- Terminal titles: `laptop`; `laptop · second terminal` for checks while the container runs (it
  first shows `student@laptop:~$` with a GREY caption "new terminal: cd here first", then
  `student@laptop:~/AC215/llm-rag$`); `container · llm-rag-cli` inside the CLI container, whose frame
  turns TEAL. After `exit`, the same terminal's frame turns GREY and its title becomes `laptop`.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b; the header is
  the path as in the viewer's clone (`cli.py · lines 183–194`); last year's file carries its branch
  (`pipenv · cli.py · lines 62–64`), the old book its commit (`96d5fd7 · Tolminc Cheese.txt · line
  102 (excerpt)`). Never more than 12 lines on screen. A line longer than 65 characters is shown
  *wrapped*: broken at spaces, continuation rows indented and marked with a GREY ↪, header suffix
  `· line N wrapped`. An *excerpt chip* quotes an exact sub-string of one line, headed
  `path · line N (excerpt)`. A *code strip* is a 3-row code panel along the bottom edge, showing
  one excerpt at a time and Transforming into the next while its header updates (S04). `PANEL(capture:
  lines, "header")`: the same look for lines from `assets/terminal/` (a diff, a recorded line); a
  header names the command or file, never a capture folder.
- README cards. While a terminal of 10 or more rows is up, a README card is a one-line chip in the
  top band, right of the tracker: `README.md · line N` + the quoted phrase, at most 40 characters.
  A multi-line README card appears only above a 3-row strip, or with no terminal.
- "With your key, look for" cards (Google calls that could not be recorded) and "if it fails (with
  your key)" cards: a GREY caption card, one short line per item, each citing the `cli.py` line that
  prints or writes it; items write in when the SAY names them (`vo.wait_until`). Never styled as
  terminal output, never in a terminal frame, never with invented values.
- `TRACKER Run 3` = the `ReadmeTracker`, top-left in every walkthrough scene, moves to that section
  and step; `TRACKER Run 3 · extra`: same step, the caption gets " · extra" while a command the
  README doesn't have is on screen; `TRACKER Account 1→6` = the dots tick one per console screen.
  Caption "README › section › step k of N". `README.md` of `dlops-io/llm-rag` @ `e17a39f`:
  - `Prereq` = "Prerequisites" (`:45-48`), 2: 1 Docker installed · 2 Clone repo.
  - `Account` = "Service Account" (`:52-69`), 6: 1 Open console · 2 Create account · 3 Grant roles ·
    4 Keys tab · 5 Add JSON key · 6 Rename, save.
  - `Run` = "Run Container" (`:75-85`), 3: 1 cd llm-rag · 2 Set GCP_PROJECT · 3 Run script.
  - `Chunk` = "Chunk" (`:91-116`), 3: 1 Visualizer · 2 Char split · 3 Recursive split.
  - `Embed` = "Embed" (`:122-138`), 2: 1 Embed char · 2 Embed recursive.
  - `Load` = "Load" (`:144-165`), 3: 1 Load char · 2 Load recursive · 3 Chroma UI.
  - `Query` = "Query" (`:171-186`), 2: 1 Query char · 2 Query recursive.
  - `Chat` = "Chat" (`:192-214`), 3: 1 Chat char · 2 Chat recursive · 3 Chat tool.
  - `Semantic` = "Semantic Chunking" (`:220-236`), 1: 1 Semantic run.
  - `Agents` = "Agents (L06)" (`:242-271`), 1: 1 Run agent (preview only, S16).
  Ordering (said in a clause where it happens, BRIEF.md "Ordering notes"): the visualizer link comes
  first (S06); `--load` appears first as captured before there were embeddings, then on the staff's
  vectors (S09); the restart (S10) is not in the README; "Chroma UI" and "Chat tool" are links, drawn
  as browser windows; *Agents* is L06's, a preview.
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed line,
  and the SAY says so ("an extra check", "not in the README") at least the first time. The clone
  command, which the README implies but doesn't print, gets a GREY caption citing `README.md · line
  48` instead.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README step);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses. A `▶` never sits on a
  frame that can't be read when paused: when the checkpoint's commands have scrolled away or a
  picture replaced them, the `▶` sits on a static GREY "your turn" card listing them exactly as typed.
  Every `▶` beat holds its frame for 2 s of silence after its SAY (`self.wait(2)`) before anything
  moves or fades.
- "What if" demos (S05's two traps) run inside a RED dashed frame titled `what if · just watch`, so
  they never look like the viewer's own terminal; the scene then returns to the viewer's terminal
  with a GREY caption "back in your container".
- Tags (GREY unless stated): `extra`; `illustration` on every schematic (the console, the web tools
  in a browser frame, "what if" pictures); `our illustration` on pictures that look like data but
  are not measurements (the embedding space — a 2-D drawing of a sphere, a circle and a dashed
  equator ellipse, with arrows as 2-D projections; `VoiceScene` is not a `ThreeDScene` — and its
  clusters, the HNSW graph, the seismograph's curve, the dot cloud of S12); `at the time of
  recording` next to the first Docker/Compose, Python and uv versions and the Chroma versions; `real
  run · no key` on the runs that fail for lack of a key (`cli-container/20`, `40`, `60`); `recorded ·
  the staff's vectors (68e0bde)` on every panel computed from the staff's committed embeddings
  (`recorded-embeddings/01`–`09`); `stand-in query · a stored story chunk's vector` on
  `recorded-embeddings/09`; `lecture example` on numbers taken from the slides (0.57, 0.77, 0.43,
  0.93; 0.986/0.976/0.886; 0.89/0.85/0.68, 0.8; the RRF table; the Chester question); `concept · not
  in the tutorial's code` (GREY dashed) throughout S15; `preview · L06` on the agent command;
  `erratum` on every tutorial slip (the SAY says "a small slip", always with the fix); `fix · not in
  the repo` on V7's plugged cable; `your numbers will differ` on container ids, UUIDs and heartbeat
  values; GOLD cost tags ("your project pays · per use") on each Google call and on the key (Vertex
  AI bills the text sent and returned; we count calls, we never say the bill is per call).
- The key is always a GOLD key glyph labelled `llm-service-account.json`; its content is never
  drawn. The course's project id appears only inside the diff line the viewer must edit
  (`laptop/06` line 10), never in a caption, label or SAY. The placeholder is `your-project-id`.
- The bind mount is one folder seen from two sides: nothing travels along a PINK mount route; a file
  that appears on one side blinks on both sides at once, and the route only pulses.
- Names on screen. No real person's name in captions, labels or narration; the Tolminc story is "the
  instructor's short story"; books are named by title, never by author. Never show these lines:
  `Tolminc Cheese.txt:1`, `cli.py:61-71`, `:435`, `README.md:263`, `semantic_splitter.py:102-105`,
  `cli-container/10:36`, `13:36`, `15:3`, `recorded-embeddings/01:145`, `02:156`, `07:12-21`,
  `08:6` and `08:12` (a label with an author's name), `05` and `70` past the ids list of line 6,
  `expected/out-txt-agent-run.txt` except lines 65 and 74. `laptop/05` line 6 is cut after
  `origin/HEAD)` (a GitHub user name follows); line 7 is never printed. Commit chips show the hash
  and our own words only, never a commit's author or merge message.
- Semantic colours (series table applied, BRIEF.md):

  | meaning | colour |
  | --- | --- |
  | your laptop: `~/AC215`, the `llm-rag/` and `secrets/` folders, `outputs/` and `docker-volumes/chromadb/` as folders on your disk; the browser and the course's web tools; the published host door `:8000` | GREY |
  | Google Cloud: your project, IAM and the service account, the Vertex AI API; the tall **embedding model** box shared by both lanes (`gemini-embedding-001`) and the **LLM** box (`gemini-3.1-flash-lite`); the LLM's answer; Docker Hub | BLUE |
  | containers and images: the CLI container (`llm-rag-cli`), the Chroma container (`chromadb/chroma:latest`), the vector-database cylinder inside it, the `llm-rag-network` rail, container-side ports | TEAL |
  | system parts inside the image: the Debian base, the apt layer, the image's Python 3.12.15 | ORANGE |
  | project-owned data and recipe: book pages once cut, chunk cards, document vectors, records, the two collections; `Dockerfile`, `pyproject.toml`, `uv.lock`, `docker-compose.yml`, `/.venv` | GREEN |
  | tools: docker, Compose, git, uv, `docker-shell.sh`; the chunkers as tools — a ruler (char-split), scissors (recursive-split), a seismograph (semantic-split) | PURPLE |
  | errors and "avoid this": `DefaultCredentialsError`, exit 127, the first-run "not found" (RED, then grayed "harmless"), the unplugged system-instruction cable, Gutenberg license chunks, stale chunks, the "what if" frames | RED |
  | your turn, the README tracker, "look here now", the top-K cut line, the semantic threshold line | YELLOW |
  | money: every call to Vertex AI (embedding batches, the chat call), the key glyph | GOLD |
  | lookups and routes: the question and its query vector, similarity arcs and the search beam, filter masks' edges, the name lookup `llm-rag-chromadb → 172.19.0.2`, the three bind-mount routes, the `8000:8000` arrow, `GOOGLE_APPLICATION_CREDENTIALS` as a signpost | PINK |
  | a future thing (L06 agents, L08 fine-tuning) and the lecture's concepts with no code here (S15) | GREY, dashed |

  Chunk cards and document vectors are GREEN whatever book they come from; a book is shown by a
  label or a position, never by a colour. A filter dims what it removes to GREY at low opacity. The
  system instruction is a GREY dashed ghost card.
- Visual set pieces V1–V8 are specified in BRIEF.md ("Visual set pieces"); SHOW lines say which one,
  its state, and what moves. V1's mini-map (from S06 on): a glyph-only copy of the two lanes,
  ≈ 3.2 × 1.4, bottom right above the safe-frame edge, its active box lit YELLOW; it hides whenever a
  terminal taller than the 3-row strip, or a code panel of more than 5 lines, is on screen.
- Running example (BRIEF.md): user `student`, host `laptop`, workspace `~/AC215`:
  `student@laptop:~/AC215$`, then `student@laptop:~/AC215/llm-rag$`; the G1 demo in
  `student@laptop:~/AC215-zip$` and `student@laptop:~/AC215-zip/llm-rag-main$`. Container prompts:
  `app@92c5bfd26089:/app$` (first session, `laptop/07`), `app@390fe47a277a:/app$` (after the restart,
  `laptop/23`), `app@2af936bbf5b9:/app$` (the G5 demo, `gotchas/01`). `GCP_PROJECT="your-project-id"`.
  The question `How is tolminc cheese made?` (`cli.py:318`); chat's copy has two question marks
  (`cli.py:372`). The knowledge base: 11 books, ten from Project Gutenberg and the instructor's short
  story `Tolminc Cheese.txt` (7,808 characters). The stand-in query chunk `8440accaceb0ce96-6`.
- Length and parts: narration 4,339 words (`python -m explainer.script`, v2; v1 4,262; BRIEF.md:
  3,900–4,300, plan ~4,240). Part 1 = S01–S09 (build the index) 2,534 words; part 2 = S10–S16 (ask
  the index) 1,805 words. Per scene (BRIEF.md budget ±15 %):

  | scene | S01 | S02 | S03 | S04 | S05 | S06 | S07 | S08 | S09 | S10 | S11 | S12 | S13 | S14 | S15 | S16 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | budget | 220 | 260 | 270 | 290 | 240 | 280 | 220 | 330 | 300 | 190 | 290 | 290 | 280 | 270 | 210 | 300 |
  | words | 248 | 251 | 285 | 298 | 270 | 272 | 191 | 396 | 323 | 196 | 262 | 268 | 285 | 270 | 190 | 334 |

  S08 sits at the top of its band: it carries the first paid call's recovery card (follow-along
  must-fix). `explainer.script` assumes 155 wpm; the series docs assume ~174, but a sample of this
  script measured 144–151 wpm with af_heart at 0.9 (L04: 146 over the whole script, gaps included),
  so expect ≈ 29.5–31 min of voice; typing, outputs and five ponder timers bring the video to
  ≈ 33–34 min: do not grow the script. After the merge, run `python -m explainer.script
  videos/ac215-l05-rag/script.md --synth` when the CPUs are free (it fills the TTS cache for the
  render) and put the measured total here. Part 1 ends on "the index is built"; part 2 opens in
  S10 with a re-orientation and a fresh `sh docker-shell.sh`. Each part ends on an empty frame.
- Notes for scene authors.
  - `Capture.pick()` indexes the output body: pick index = file line − 1.
  - `cli-container/` files ran through `docker exec` and have no prompt: draw `app@92c5bfd26089:/app$`
    in part 1 (S05–S09) and `app@390fe47a277a:/app$` in part 2 (S10–S14), and type the `$` command
    there. The part-2 runs (`cli-container/40`, `60`, `recorded-embeddings/05`, `07`–`09`) were
    captured in the first session, before the restart; their outputs do not depend on the session
    (the same loaded collection answers after the restart, `cli-container/70`), so the part-2 prompt
    keeps the story continuous. Container ids carry `your numbers will differ`.
    `recorded-embeddings/` files ran in the container too (draw the part's prompt), except `03` and
    `04` (a `curl` to localhost and an `ls`), which are on the laptop; `00` is never typed.
  - `laptop/07` (session): line 45 is the prompt with `exit` typed after it; S04 stops at the prompt,
    S10 types `exit` and prints line 46. `laptop/23` likewise: S10 stops at line 13's prompt, S16
    types `exit` and prints line 14.
  - `expected/*.txt`: line 1 is a `#` source header (never printed).
  - V3's ribbon is a row of word blocks: one thin GREEN rectangle per word of `Tolminc Cheese.txt`,
    its width proportional to its characters, no text (about 1,000 characters span the frame, so the
    350-character ruler window is ≈ 4.4 units and the 20-character band ≈ 0.25). Real text appears
    only in zoom callouts of at most 60 characters. Block positions are computed on the whole file,
    but the first two lines (the author line) stay off-screen left, so the first cut lands where
    `cli-container/12` says. V8's sentence tiles are numbered blocks showing their first three words
    at ≥ 20 pt; one tile zooms to its full sentence once. (Text below 20 pt fails `explainer.check`.)
  - Lexicon (added at review, `explainer/lexicon.yaml`, `# AC215 L05`): RAG, Self-RAG, Tolminc,
    transhumance, 0.13.1, 3.1, 0.16, 0.31, 0.42, 0.67, 0.75, 0.8, and the list "0.57, 0.77, 0.43,
    0.93" as one entry (S11; a bare `0.43` would re-voice a finished CareOneX episode). Keep those
    spellings exactly in the SAY lines. Not needed: Chroma (never add it: four SAY lines say
    "Chroma's"), Vertex, Gemini, Gutenberg, SQLite, H-N-S-W, Mara, 0.369, 0.402 (read fine).
  - i18n stage: `build/review_spoken.md` §16 lists the `en_display` lines (spoken form → literal:
    L-L-M rag → `llm-rag`, slash app → `/app`, the docker volumes folder → `docker-volumes/`, the word
    load → `load()`, documents, item zero → `documents[0]`, contains → `$contains`, …) and the
    glossary pins (lane → 通道, ruler → 尺子, seismograph → 地震仪, "a small slip" → one fixed
    phrase, `Step 1` / `Step 2` kept in English, …). Apply them in `i18n/zh/`.
  - Never shown (BRIEF.md "Things never to do"): slide images, memes, README figures; Google logos or
    console screenshots; the Docker-in-Docker laptop, `proxy_relay.py`, `mirror.gcr.io`, the CA
    variables, the rebuilt base's `[1/6] FROM …@sha256:60c8fd1…`, apt's `https://deb.debian.org`
    lines, the `docker exec` that typed the container commands, the `git ls-tree … git show` copy
    command of `recorded-embeddings/00`; invented `Embedding values:`, `Results:`, `INPUT_PROMPT:`
    or `LLM Response:` values; `out.txt` as the output of any L05 command; `docker compose run --rm
    llm-rag-cli` as a way to start.

---

## S01 · A model that never read the book — `s01_hook.py` · `Hook`

Lecture: A6–A11.

SHOW: Black frame, no tracker. A GREY chat box (`browser_window` frame, tag `illustration`) fades
in center; the question `How is tolminc cheese made?` types into its input field (the README's
sample question, `cli.py:318`), a cursor blinks, and a BLUE "LLM" box above it begins to answer: a
row of gray placeholder bars streams out (no words).
SAY: Here's the question this tutorial asks a language model: how is Tolminc cheese made? Tolminc is a real Alpine cheese, but the answer we want lives in one particular text.

SHOW: The chat box shrinks to the upper left. A shelf of eleven GREEN book spines slides in along
the bottom; ten carry a small GREY label "Project Gutenberg", the eleventh glows YELLOW. It opens
into CODE(input-datasets/books/Tolminc Cheese.txt: 3–4) (header `Tolminc Cheese.txt · lines 3–4`),
line 4 *A fictional tale inspired by Alpine cheesemaking* underlined YELLOW. A GREY chip "11 books ·
input-datasets/books". Then the BLUE LLM box gets a small GREY calendar glyph "trained before this
story", and its gray answer bars turn RED-edged. On the last sentence a large YELLOW "?" hangs in
the gap between the glowing book and the LLM box, and stays (S13 comes back to it).
SAY: The knowledge base is eleven books: ten old cheese books from Project Gutenberg, and the instructor's short story, a fictional tale. A model trained before that story existed has never read it, so it answers from somewhere else. How do we make it answer from this story, without retraining it?

SHOW: LECTURE A6–A7. The shelf slides away; the "?" shrinks to the top corner. Four chips write in a
row: "stale training data", "no specialized knowledge", "hallucination", "no sources". A YELLOW
bracket closes over the first two, labelled "RAG fixes these"; the other two stay dim.
SAY: The lecture lists four weaknesses: stale training data, no specialized knowledge, hallucination, and no sources. RAG, retrieval augmented generation, goes after the first two.

SHOW: LECTURE A8–A10. The chips shrink to the top. Three roads run from a pile of GREEN books (left)
to the BLUE LLM box (right), drawn one at a time as named. Road 1: every page pours into the prompt,
which overflows; a RED cross and the word "garbage". Road 2: GREY dashed, a slow clock glyph, a tag
"fine-tuning · lecture 8". Road 3: the lecture tag leaves; a small librarian glyph picks ten pages
(GREEN cards) from the pile and hands them over; a YELLOW tag "open-book exam · our image".
SAY: Paste all eleven books into the prompt, and you get garbage. Fine-tune the model, and it's slow; that's lecture 8. Or let a librarian hand it the ten most relevant pages: an open-book exam. That's RAG.

SHOW: LECTURE A11. The roads fade. A crowded GREY sketch of boxes and arrows fills the frame,
blurred (our redrawing of "a map of RAG techniques", no labels legible). Four YELLOW questions write
in over it, each with a short arrow into the blur: "What is an embedding?", "a vector database?",
"a query?", "the context?".
SAY: The lecture's map of RAG techniques is crowded, but it starts from four questions. What is an embedding, a vector database, a query, the context? This video answers all four.

SHOW: The map clears. A layout preview in three steps, each clearing the last, as named: (1) the
ReadmeTracker top-left ("README › Run Container", 3 dots) with a YELLOW circle pulsing around it;
(2) the GREY tag "Lecture 5 · slides A16–A19" top right, with a small GREY caption under it "A =
main deck · B = supplement"; (3) a 3-row terminal strip at the bottom (GREY tag "preview"): `sh
docker-shell.sh` with a YELLOW `▶ your turn` tag, then `docker ps` with the GREY `extra` tag. Then a
footer caption "every command: MLOps_Learning · guides/L05-rag.md". (`illustration` and `recorded`
are explained where they first appear.)
SAY: Open the README beside this video. Top left, the tracker shows its step; top right, the gray tag points to the lecture slides. When the yellow your-turn tag appears, pause and run the command; extra commands aren't in the README.

SHOW: The preview clears. A card "Recorded October 16, 2026" with three rows writing in as named:
"Docker, chunking, Chroma: real runs" (GREEN check), "embeddings: the staff's recorded vectors"
(tag `recorded`), "Google calls: the command, the real no-key error, what to look for" (GREY key
glyph crossed out). Under it a GREY chip "Linux laptop · Docker Engine 29.8.2 · Compose v5.6.0"
(from `laptop/00` lines 3–5) with the tag `at the time of recording`. Fade out.
SAY: We recorded without a Google key. Docker, chunking and the database ran for real; the embeddings are the staff's recorded vectors. Where the code calls Google, you see the command, the real error, and what to look for.

---

## S02 · Two lanes, one database — `s02_map.py` · `TwoLanes`

Lecture: A12–A16, B5–B6.

SHOW: LECTURE A12–A14. No tracker (concept scene). Four boxes build left to right as named: a GREY
user glyph; a PINK arrow "question" into a PURPLE cluster of three gears labelled "RAG code"; from
it a PINK arrow up to a TEAL cylinder "vector database" and a GREEN arrow "retrieved texts" back
down; from the gears a GREEN elbow arrow "full prompt" into a BLUE box "LLM"; a BLUE arrow "response"
back to the user. A thin RED dotted line between cylinder and LLM gets a RED cross: "never talk".
SAY: Here's RAG in four boxes. The user's question goes to the RAG code, which asks a vector database for related texts. The code joins question and texts into one full prompt, and the model's response goes back. The database never talks to the model.

SHOW: LECTURE A16. The gears open up and V1 grows out of them, full width. Top lane, left to right:
a stack of GREEN book pages "knowledge base" → a PURPLE ruler glyph "chunking" → a tall BLUE box
"embedding model" spanning both lanes → GREEN vector glyphs → a TEAL cylinder "vector database"
spanning both lanes. Bottom lane: the PINK question arrow first runs straight at the cylinder, as on
A12; then the tall BLUE box slides in between, the question passes through its lower half (a PINK
highlight) and leaves as a PINK query vector, and a chip appears at the cylinder: "the database
gets numbers, not words". The bottom lane goes on: the cylinder → a GREEN prompt card "prompt +
query + context" → the BLUE LLM box → a BLUE arrow back to the user.
SAY: Open the RAG box and you get two lanes. On top, books are cut into chunks, an embedding model turns each chunk into a vector, and the vectors go into the database. Below, the question goes through the same model, and only its vector reaches the database.

SHOW: LECTURE B5–B6. Three dashed regions fade in one at a time as named, as B5 draws them:
"Indexing" around the whole top lane; "Retrieval" around the lower half of the embedding box, the
query vector, the cylinder and the arrow into the prompt card; "Augmentation & Generation" around
the LLM only. No numbered circles.
SAY: This is the pipeline slide from lecture, with three phases. Indexing is the whole top lane. Retrieval brings the context to the prompt, and the model does augmentation and generation.

SHOW: The regions dim to outlines. Two GREY lane labels: `README.md · line 5` "Step 1: Chunk ->
Embed -> Load" over the top lane, and `README.md · line 9` on two rows, "Step 2: Query -> Embed ->
Retrieve" / "-> LLM -> Generate Answer", under the bottom lane. Then five YELLOW flag chips (the
README's steps, `README.md · lines 17–21`, as text, no emoji) drop under their boxes one at a time as
named, each box pulsing as its chip lands: "Chunk `--chunk`", "Embed `--embed`", "Load `--load`" |
"Query `--query`", "Chat `--chat`".
SAY: The README calls the two lanes step 1 and step 2, and gives each box one flag of cli.py: chunk, embed and load on top, query and chat below.

SHOW: The top lane pulses once slowly with a GREY tag "once · offline · slow"; the bottom lane
pulses quickly three times, "every question". Then the shared BLUE box glows YELLOW-edged and a rule
card writes above it: "same model · same kind of vector · both lanes" and, under it, "chunks before,
questions later". A small RED "what if" inset (tag `illustration`): a second, different BLUE box in
the bottom lane makes the query vector point off into an empty region, RED cross.
SAY: Two rules. The top lane runs once, offline, and it's slow. The bottom lane runs for every question. And both lanes must use the same embedding model, or the question and the chunks don't live in the same space.

SHOW: V1's second layer: three location frames draw around the boxes as named. A TEAL frame "CLI
container" around the chunking ruler (a GREY chip "no network needed"). A BLUE cloud "Google · Vertex
AI" around both the embedding model and the LLM, with a GOLD tag "pay per use · your key" and a GREY
note "no VM, no bucket: nothing keeps running". A second TEAL frame "Chroma container" around the
cylinder, with a PINK route down to a GREY folder "on your laptop".
SAY: Where does each box run? The chunker runs in your own container. Both models run at Google: you pay for the text you send, with your key, and nothing keeps running there. The database runs in a second container, with its files on your laptop.

SHOW: Everything but the TEAL "CLI container" frame fades. It grows to center and five GREY command
lines appear inside it, one per flag: `python cli.py --chunk …`, `--embed …`, `--load …`,
`--query …`, `--chat …`. Fade out.
SAY: Every step is one python cli.py command, inside that first container. So first, let's get it running.

---

## S03 · Your key, your folders, your project — `s03_setup.py` · `KeyAndProject`

Lecture: none.

SHOW: TRACKER Prereq 1 · extra. Terminal (full width, 10 rows, title `laptop`, prompt
`student@laptop:~/AC215$`). It types `docker --version; docker compose version` (extra) →
TERM(laptop/01-x-docker-check.txt: 2–3). `29.8.2` and `v5.6.0` get the tag `at the time of
recording`; the space in `docker compose` flashes YELLOW. A GREY note under the terminal: "Mac:
zsh, prompt ends in % · Windows: WSL or Git Bash".
SAY: Prerequisites first: Docker. This extra check prints its versions; the script needs docker compose, with a space. On a Mac your prompt looks different; on Windows, use WSL or Git Bash.

SHOW: TRACKER Prereq 2. A one-line README chip in the top band: `README.md · line 48` "Cloned this
repository" (the clone command itself is not printed there). It types `git clone
https://github.com/dlops-io/llm-rag.git` → TERM(laptop/02-clone.txt: 2). TRACKER Prereq 2 · extra.
It types `mkdir secrets; ls` (extra) → TERM(laptop/03-x-mkdir-secrets.txt: 2). The terminal shrinks
to the 3-row strip. Above it, left: a static GREY card with `▶ your turn`, "in your course folder
(~/AC215)": `git clone https://github.com/dlops-io/llm-rag.git` · `mkdir secrets; ls` (extra).
Right: two GREY folders `llm-rag/` and `secrets/` side by side under a GREY `~/AC215` bracket, with a
small README card `README.md · lines 66–69` (the `|-llm-rag` / `|-secrets` layout); the name
`llm-rag` underlines YELLOW with a tag "exactly this name".
SAY: The README links the repo but doesn't print the clone command, so here it is. Then, as an extra, make a secrets folder beside the clone, and keep the clone's name exactly L-L-M rag. Pause and do both, in your course folder.

SHOW: TRACKER Account 1→6. The strip and the card leave; the folders stay small at right. A
schematic console in a GREY browser frame (tag `illustration`, no logo), each screen replacing the
last as named: "IAM & Admin › Service accounts" → "Create service account": name
`llm-service-account` → "Grant access": two role chips "Storage Admin" and "Gemini Enterprise Agent
Platform User" (with a small GREY note "Vertex AI User in older projects") → the account's "KEYS"
tab → "Add key › Create new key › JSON", with a GREY chip "key creation blocked by an org policy?
use a personal project, not one under the university's organization". A GOLD key glyph drops out of
the browser into the GREY `secrets/` folder and its label changes to `llm-service-account.json`.
SAY: Now the service account, in the Google Cloud console. Create one called L-L-M service account, and grant it two roles: Storage Admin, and Gemini Enterprise Agent Platform User. Open its keys tab, add a JSON key, and save it in secrets as L-L-M service account dot JSON.

SHOW: A GOLD tag on the key: "this file spends your project's money". CODE(.gitignore: 1–5) slides in
at right (header `.gitignore · lines 1–5`); a GREY dashed ghost line "secrets" under line 5 with a
GREY tag "not here". The two folders pulse: the key sits *beside* the repo. Then L04's three gates
in miniature, three small BLUE gates in a row labelled "who?" (the GOLD key), "may?" (a role chip),
"switched on?" (an API switch, still off).
SAY: That key spends your project's money; the git ignore file has no secrets line, so it's safe only beside the repo. Remember the three gates from lecture 4: the key says who you are, the role what you may do, and the API must be switched on.

SHOW: The `erratum` tag goes on the "Storage Admin" chip only: it dims to GREY with a note "no
storage call in this code", and the Agent Platform chip gets a GREEN tick "needed". Then the third gate: a schematic "APIs & Services › Vertex AI API ·
aiplatform.googleapis.com › Enable" screen (tag `illustration`), TRACKER Account 6 · extra; the
switch flips and the third gate opens with a white tick. Under it a RED chip, dimmed, "without it:
SERVICE_DISABLED on the first embed, after 5 retries". Then the console leaves and `▶ your turn`
sits on a static GREY card "your turn · in the console" (tag `illustration`), all 6 TRACKER Account
dots lit, one row per step: "IAM & Admin › Service accounts › Create: llm-service-account" · "roles:
Gemini Enterprise Agent Platform User (Vertex AI User) · Storage Admin" · "KEYS › Add key › Create
new key › JSON" · "rename it llm-service-account.json, into secrets/ beside llm-rag/" · "APIs &
Services › Vertex AI API › Enable (extra)"; under the rows a GREY look-for line "check: ls secrets →
llm-service-account.json".
SAY: Two small slips. Nothing here uses Cloud Storage, so the Agent Platform role is what matters. And the README never says to enable the Vertex AI API; without it, the first embedding call fails with service disabled, after 5 retries. Pause and do it all now: account, roles, key, and API.

SHOW: TRACKER Run 1. Terminal back (full width, 9 rows). It types `cd llm-rag` → (no output); the
next prompt is `student@laptop:~/AC215/llm-rag$`, the new path part flashing GREY. TRACKER Run 1 ·
extra. It types `ls -a; git log --oneline -1` (extra) → TERM(laptop/05-x-ls.txt: 2–5, 6 cut after
"origin/HEAD)"; wrap). `docker-shell.sh`, `docker-compose.yml` and `cli.py` highlight GREEN one by
one; `e17a39f` gets a GREY tag "the commit this video was recorded on".
SAY: Step 1 of the next section: cd L-L-M rag. An extra look shows the scripts, the compose file, cli.py, and the commit this video was recorded on.

SHOW: TRACKER Run 2. A GREY pencil glyph edits a file card `docker-shell.sh` (caption "in your
editor"), then it types `git diff docker-shell.sh` (extra) → TERM(laptop/06-x-edit-gcp-project.txt:
6–13). Line 10 (`-`) prints RED-tinted, line 11 (`+`, `your-project-id`) GREEN; a YELLOW tag on
`your-project-id`: "your Project ID · not the name"; line 12 gets a GREY tag "leave this: a path
inside the container". `▶ your turn`. A small GREY note: "skip it → calls go to the course's
project → permission error".
SAY: Step 2: in your editor, set GCP project on line 7 to your own Project ID, the ID, not the name. Leave line 8 alone. Skip this, and your calls go to the course's project and fail. Pause and edit.

---

## S04 · One script, two containers — `s04_compose.py` · `TwoContainers`

Lecture: none.

SHOW: TRACKER Run 3. A small recap strip at the top, glyph-only: two TEAL boxes on a rail (L04) and
a GOLD key through a PINK route into a TEAL box (L03); both slide together into one empty GREY
laptop outline, center, captioned "today: both at once". Inside it, two GREY folders `llm-rag/` and
`secrets/` side by side.
SAY: Lecture 4 put two containers on one network; lecture 3 brought a key in through a mount. Today: both at once, with one command.

SHOW: The laptop picture moves to the upper half. A PANEL: line 11 of `laptop/06` without its leading
`+` (header `docker-shell.sh · line 7 · after your edit`), then CODE(docker-shell.sh: 8–12) below it
(header `docker-shell.sh · lines 8–12`). The three `export` lines highlight in turn; three PINK value
chips lift off them (`your-project-id`, `/secrets/llm-service-account.json`, `llm-rag-cli`); line 12
`docker compose run --rm $IMAGE_NAME` highlights YELLOW.
SAY: The script, docker-shell.sh, exports three values: your project, the key's path inside the container, and the image name. Then it calls docker compose run, with dash dash r m, for that one service.

SHOW: The script panels leave. V2 owns the top ≈ 4.3 units; the compose file arrives as a code
strip along the bottom edge, one excerpt at a time, each building V2 as it highlights:
CODE(docker-compose.yml: 1–3) lays the TEAL rail `llm-rag-network`; it Transforms into
CODE(docker-compose.yml: 6–8), which puts a TEAL box "CLI container" on the rail, with a GREEN recipe
chip "build: .".
SAY: The compose file draws the whole picture: one network, by name, and the CLI service on it, with an image built from this folder if missing.

SHOW: The strip Transforms on: CODE(docker-compose.yml: 10–12) draws two PINK mount routes from the
laptop folders (`../llm-rag → /app`, `../secrets → /secrets`); CODE(docker-compose.yml: 13–15) (line
14 as an excerpt chip if it needs wrapping) opens two empty `$` slots on the box, and the PINK chips
from the script drop into them; CODE(docker-compose.yml: 16–17) draws a dashed arrow "depends on" to
an empty TEAL outline on the rail.
SAY: Two mounts put the repo onto slash app and secrets onto slash secrets. Two slots take the script's values, and the service depends on Chroma.

SHOW: The strip goes on the same way: CODE(docker-compose.yml: 18–20) fills the TEAL outline,
"Chroma container", image chip `chromadb/chroma:latest` (pulled from a BLUE "Docker Hub" shelf), name
tag `llm-rag-chromadb`; CODE(docker-compose.yml: 21–22) draws a PINK `8000:8000` arrow through a GREY
street door on the laptop's edge; CODE(docker-compose.yml: 23–24) a third PINK route
`./docker-volumes/chromadb → /data`; line 26 as an excerpt chip gets a GREY tag "lets the course's
web tools in · Load, step 3".
SAY: The Chroma service runs the database from Docker Hub, under a fixed name. It publishes port 8000 to your laptop, keeps its data in the docker volumes folder, and lets the course's web tools in.

SHOW: The strip leaves. CODE(Dockerfile: 18) and CODE(Dockerfile: 45) as two excerpt chips. Inside
the CLI box, a GREEN box `/.venv` sits *outside* `/app`; the PINK `/app` route pulses and a GREY
sheet "your repo" covers `/app` only, leaving `/.venv` visible. A tiny loop: a pencil edits `cli.py`
on the laptop side, the file blinks on both sides, "no rebuild".
SAY: From the Dockerfile: the virtual environment lives in slash dot venv, outside slash app, so the code mount can't hide it. Edit cli.py on your laptop and rerun; no rebuild.

SHOW: The picture shrinks to the top. Terminal (full width, 12 rows, title `laptop`, prompt
`student@laptop:~/AC215/llm-rag$`). It types `sh docker-shell.sh` → TERM(laptop/07-docker-shell.txt:
2–5; session). In the shrunk picture, as lines 3–5 print: the Chroma image arrives from the BLUE
Docker Hub shelf, the rail is laid, and the Chroma box fills in. A GREY chip beside the pull line:
"first build also pulls python:3.12-slim-bookworm (~48 MB)". (No `▶` here: the checkpoint is the
prompt, at the end of the scene.)
SAY: Step 3: sh docker-shell.sh. Compose pulls Chroma's image, creates the network, and creates the Chroma container first.

SHOW: TERM(laptop/07-docker-shell.txt: 6–8; session) (7–8 joined, wrap). Lines 7–8 print RED; a
small BLUE Docker Hub shelf in the picture shows an empty slot labelled `llm-rag-cli`. Then the RED
lines fade to GREY with a tag "harmless".
SAY: Then this, which looks like an error but isn't. Compose first asks Docker Hub for an image called L-L-M rag CLI, finds none, and builds it instead.

SHOW: TERM(laptop/07-docker-shell.txt: 9–10, 21, 22, 25, 26, …, 36; session) (BuildKit rows cut at 65,
times as GREY tags). Line 10's `81.5s` tag highlights; `[2/6]`, `[5/6]`, `[6/6]` get TEAL badges
"build step 2", "5", "6"; line 21 `112.26MB` highlights YELLOW. Then the terminal shrinks to the
3-row strip. Above it, a GREEN parcel "build context" opens: a big GREY block "`.git` · 103 MB" (from
`laptop/05b` line 2), a tiny GREEN block "chroma.sqlite3" (`laptop/14b`) and a small sliver "the
rest"; one chip `erratum · no .dockerignore → exercises` and a GREY caption "the mounts hide both at
run time".
SAY: The build took 81 seconds here. Its context was 112 megabytes. Most of it is git history, which still holds an old copy of the staff's database. With no docker ignore file, the image keeps it.

SHOW: The terminal grows back. TERM(laptop/07-docker-shell.txt: 37–44; session). Line 38's container
name `llm-rag-llm-rag-cli-run-90678535ddef` underlines GREY (S05 comes back to it); lines 42–43 get
the tag `at the time of recording`; line 40 `x86_64` gets a GREY note "Apple Silicon: aarch64 · both
native". Line 41 "…activated." and line 44 "Activating virtual environment..." get a small GREY
bracket and an `erratum` tag "says it before it does · cosmetic".
SAY: Then the banner: Python 3.12.15 and uv 0.13.1, at the time of recording. It says activated before it activates: cosmetic.

SHOW: The prompt of line 45 appears alone (session: `app@92c5bfd26089:/app$`, nothing typed); the
terminal's frame turns TEAL and its title becomes `container · llm-rag-cli`. `92c5bfd26089` gets a
GREY tag "container id · your numbers will differ". In the picture, the CLI box lights. `▶ your
turn`.
SAY: You're at the container's prompt. The part after the at sign is the container's ID; it changes every run. Pause, and get to this prompt.

---

## S05 · Names, mounts, and two traps — `s05_lookaround.py` · `NamesAndMounts`

Lecture: none.

SHOW: TRACKER Run 3 · extra. A second terminal (full width, 8 rows, title `laptop · second terminal`):
it first shows `student@laptop:~$` with the GREY caption "new terminal: cd here first", then the
prompt `student@laptop:~/AC215/llm-rag$`. It types `docker ps` (extra) →
TERM(laptop/08-x-docker-ps.txt: 2–4) as the column view "docker ps · PORTS and NAMES".
`0.0.0.0:8000->8000/tcp` highlights PINK; `llm-rag-chromadb` and
`llm-rag-llm-rag-cli-run-90678535ddef` highlight YELLOW. A chip `docker-compose.yml · line 9`
`container_name: llm-rag-cli` appears above with an `erratum` tag "not used by compose run".
SAY: Check the picture with extras: open a second laptop terminal and cd into L-L-M rag. The docker ps command shows Chroma with port 8000 published. But the CLI container isn't called L-L-M rag CLI: compose run ignores that name.

SHOW: It types the two commands of `laptop/15-x-mounts.txt`'s `$` line one after the other (extra;
each folds onto two rows); the container name inside them underlines YELLOW with a GREY tag "yours
differs · copy it from docker ps" → TERM(laptop/15-x-mounts.txt: 2–3, 5). Above the terminal, V2's
three PINK routes pulse as their lines print.
SAY: And docker inspect, with the name from docker ps, lists the mounts. The repo is on slash app, secrets on slash secrets, and the docker volumes folder on Chroma's slash data.

SHOW: Back in the container terminal (TEAL frame, prompt `app@92c5bfd26089:/app$`, 9 rows). It types
`echo GCP_PROJECT=$GCP_PROJECT; echo GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS; ls -la /secrets`
(extra; folds onto two rows) → TERM(cli-container/01-x-env.txt: 2–6). `your-project-id` highlights
YELLOW; the path on line 3 becomes a PINK signpost pointing at an empty `/secrets` box; a GOLD
dashed key outline sits where yours would be, tag "yours: the key file".
SAY: Inside the container, your Project ID and the key's path arrived. Our secrets folder is empty, with no key; yours should list the JSON file.

SHOW: It types `getent hosts llm-rag-chromadb; curl -s http://llm-rag-chromadb:8000/api/v2/heartbeat; echo`
(extra; folds) → TERM(cli-container/04-x-chroma-by-name.txt: 2–3). Above, a PINK phone-book card on
the rail: `llm-rag-chromadb → 172.19.0.2`. Then the second terminal: it types
`curl http://localhost:8000/api/v2/heartbeat` (extra) → TERM(laptop/10-x-heartbeat.txt: 2); the
PINK `8000:8000` arrow and the GREY street door pulse. Heartbeat numbers get `your numbers will differ`.
SAY: The CLI finds Chroma by name, through the network's phone book. From your laptop, the heartbeat comes through localhost port 8000, the published door for you and your browser.

SHOW: Second terminal: it types `ls -la docker-volumes/chromadb` (extra) →
TERM(laptop/13-x-docker-volumes.txt: 2–5). `root root` highlights; the GREY folder in the picture
gets a small lock glyph "root's · Linux: sudo to delete"; a small GREY tag on the folder "made by
Docker: the mount's source".
SAY: Docker already created Chroma's data folder on your laptop, owned by root, with the database file in it. On Linux, deleting it later will need sudo.

SHOW: Trap 1, inside a RED dashed frame titled `what if · just watch` (small GREY note "recorded
after teardown"). The picture's `$` slots empty out. A RED tag "the wrong way" sits beside the typed
line. In the frame, a fresh laptop terminal (12 rows) types `docker compose run --rm llm-rag-cli`
(extra) → TERM(gotchas/01-x-g5-compose-run-direct.txt: 2–4, …; session) (2–3 joined); at the prompt
`app@2af936bbf5b9:/app$` it types `python cli.py --chunk --chunk_type char-split` →
TERM(gotchas/01-x-g5-compose-run-direct.txt: 17–19, …, 55; wrap). Line 55's `File  was not found.`:
a YELLOW box around the two spaces, tag "an empty file name"; a chip `cli.py · line 35`
`llm_client = genai.Client(` "runs at startup". The CLI box's two slots blink RED, empty.
SAY: Now two traps, hit on purpose. Trap one: typing the compose command yourself. Both variables come out blank, and even chunking dies at startup, where cli.py creates its Google client, looking for a key file with no name. Always start through the script.

SHOW: Trap 2, in the same RED dashed frame. A laptop terminal (prompt `student@laptop:~/AC215-zip$`,
9 rows). It types `git clone https://github.com/dlops-io/llm-rag.git llm-rag-main; mkdir secrets; ls`
(extra) → TERM(gotchas/03-x-g1-clone-as-main.txt: 2–4); a GREY tag "what a zip download unpacks".
Then the prompt becomes `student@laptop:~/AC215-zip/llm-rag-main$` with a GREY caption "after cd
llm-rag-main" (not typed: not captured as its own step), and it types `sh docker-shell.sh` →
TERM(gotchas/04-x-g1-docker-shell.txt: 2–7), line 7 RED. Then `ls -la ..; ls -la ../llm-rag` (extra)
→ TERM(gotchas/05-x-g1-stray-folder.txt: 2, 5–6, 8–10). Above, the PINK route `../llm-rag → /app`
reaches for a folder that isn't there; a GREY dashed folder `llm-rag` (root) pops into existence,
empty, and slides over `/app`, hiding the code. Fix card: "keep the name llm-rag (or mount .:/app) ·
delete the stray folder (sudo on Linux)".
SAY: Trap two: a clone with another name, like the folder a zip download gives you. The compose file mounts a folder named L-L-M rag, so Docker creates an empty one, owned by root, over your code. Keep the name, and delete the stray folder.

SHOW: The RED frame leaves; the TEAL `app@92c5bfd26089:/app$` terminal returns as a 3-row strip with
a GREY caption "back in your container". Above it, a small card, three version chips in a row from
`laptop/11` line 2, `11b` line 2 and the image digest's tag (BRIEF.md: Docker Hub `latest` =
`1.5.9`): "tag 1.5.9 · chroma 1.4.4 · API "1.0.0"", tag `at the time of recording`, and a GREY note
"team tip: pin a tag in docker-compose.yml · line 19". Then `▶ your turn` on a static GREY card in
two groups: "container": `echo GCP_PROJECT=$GCP_PROJECT; echo
GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS; ls -la /secrets` (folded), with a GOLD
note "yours: llm-service-account.json listed"; "second terminal, in llm-rag": `docker ps` · `curl
http://localhost:8000/api/v2/heartbeat` · `ls -la docker-volumes/chromadb`. Hold 2 s, then fade out.
SAY: One last oddity: the image tag called latest, and three version numbers that don't match; a team should pin a tag. Pause and try these checks; your key in slash secrets matters most.

---

## S06 · Cutting the books: a ruler — `s06_charsplit.py` · `CharSplit`

Lecture: A19–A22, B14–B15.

SHOW: LECTURE A19–A22. TRACKER Chunk 1. V1's mini-map appears bottom right, "chunking" lit. Center
(tag `illustration`): inside a GREEN book, three small topic arrows (curd · pasture · grandfather)
Transform into one averaged arrow; three PINK questions, one per topic, all land on it and fetch
the whole book: the prompt card overflows, RED. Then the book splits into GREEN cards, each with its
own arrow; one question lands next to one card, and only that card slides into the prompt card. A
GREY chip "a chunk = what you retrieve = what you paste".
SAY: Indexing starts with chunking. One vector for a whole book averages its topics, so every question fetches the whole book. Sending 11 books each time is slow, costly, and gives garbage. A chunk is small enough to find, and to paste.

SHOW: A GREY browser frame (tag `illustration`), address `ac215-llm-rag.dlops.io/chunkviz`, a
schematic page: a paragraph of word blocks with colored bands and two sliders "chunk size",
"overlap" (no screenshot); while the SAY runs the sliders move and the bands re-flow. A README chip
`README.md · line 95` "check out this visualization" and a GREY note "use Chrome".
SAY: Step 1 is a link: the README's chunk visualizer. Open it in Chrome and play with the sliders; here's the idea it shows.

SHOW: V3. The Tolminc story as a GREEN ribbon of word blocks (see notes: no text; ≈ 1,000 characters
span the frame). A PURPLE ruler window, 350 characters wide (≈ 4.4 units), lands on its start;
CODE(cli.py: 184–189) slides in below (header `cli.py · lines 184–189 · line 189 wrapped`, 7 rows;
the mini-map hides), lines 185–186 highlight with the ruler; then `separator=''` on line 189 boxes
YELLOW. The ruler steps forward 330 characters; a 20-character band (≈ 0.25 units) glows in both
windows. A counter starts "chunks: 1, 2…" and stops at 2.
SAY: Character splitting is a ruler. Lines 185 and 186 set windows of 350 characters, overlapping by 20. The separator is empty, so it counts characters, not words, stepping 330 at a time.

SHOW: The code panel leaves. The ribbon zooms out to the whole story, a GREY bar "7,808 characters";
the ruler and the 20-character band sit at its left end. The ponder card sits in the lower third.
PONDER(8 s, "The story is 7,808 characters long.\nWindows of 350 characters overlap by 20.\nHow many chunks?")
SAY: The instructor's story is 7,808 characters long. Windows of 350 that overlap by 20: how many chunks?

SHOW: The ruler slides along the bar in steps, the counter ticking fast to 24; a small equation
writes in: "1 + ⌈(7,808 − 350) / 330⌉ = 24".
SAY: The first window takes 350 characters, and each one after it adds 330 new ones. 7,458 more characters need 23 more windows: 24 chunks.

SHOW: TRACKER Chunk 2. Terminal (full width, 13 rows, TEAL frame, prompt `app@92c5bfd26089:/app$`;
the mini-map hides). It types `python cli.py --chunk --chunk_type char-split` →
TERM(cli-container/10-chunk-char-split.txt: 2–7, …, 32–34) (no `wrap`: lines 2 and 5 are cut with `…`,
so the command, `11`, `24` and the `▶` fit in 13 rows). Line 4's `11` and line 33's `24` highlight
YELLOW; line 5 gets a GREY tag "your book order may differ". `▶ your turn`. A GREY chip "no Google
call in char-split's branch", and beside the `▶` a GREY chip "Linux · PermissionError … 'outputs'?
on the laptop: mkdir outputs && chmod a+w outputs".
SAY: Step 2: python cli.py, dash dash chunk, chunk type char split. It reads 11 books and prints each book's chunk count; the story gets 24. No key needed: this branch never calls Google. Pause and run it.

SHOW: TRACKER Chunk 2 · extra. It types `wc -l outputs/chunks-char-split-*.jsonl` (extra) →
TERM(cli-container/11-x-wc-char-split.txt: 2–13) (long names cut with `…`); line 11 `24` and line 13
`8248 total` highlight.
SAY: An extra line count of the chunk files: 24 for the story, and 8,248 in total.

SHOW: LECTURE B14–B15. TRACKER Chunk 2 · extra. It types the one-liner of `cli-container/12-x-overlap-char-split.txt` (extra;
folds onto three rows) → TERM(cli-container/12-x-overlap-char-split.txt: 2–4). The terminal shrinks to
the 3-row strip; above it V3 zooms on the seam as a text callout: `…intended to ac` |
`s she intended to accomplish…`, the shared 20 characters glowing in both; `ac` and the lone `s`
underline YELLOW. At the side, small: the lecture's example, GREY cards "…artificial intelli" |
"gence…" sitting end to end, no band (tag `lecture example`).
SAY: An extra look at the seam. Chunk 0 stops two letters into the word accomplish. Chunk 1 backs up 20 characters, to the last letter of things, so accomplish is whole again. The lecture's pieces sit end to end, with no overlap.

SHOW: TRACKER Chunk 2 · extra. Second laptop terminal (strip). It types `ls -la outputs | head -5` (extra) →
TERM(laptop/16-x-outputs-on-laptop.txt: 2–6); `student student` highlights; a GREY chip
`.gitignore · line 4` `/outputs`. Then back to `cli-container/10` as a PANEL (lines 8–9, header
"python cli.py --chunk … · the first book's table"): row 0 `The Project Gutenberg eBook of …`
highlights RED; a RED tag `erratum` "header and license, chunked like the rest · see part 2".
SAY: The chunk files land in outputs, on your laptop, and git ignores them. Row 0 of a Gutenberg book is the Project Gutenberg header: these books start with a header and end with a license, both chunked like the rest.

---

## S07 · Recursive split and its hidden overlap — `s07_recursive.py` · `RecursiveSplit`

Lecture: B16–B19.

SHOW: TRACKER Chunk 3. CODE(cli.py: 196–205) (header `cli.py · lines 196–205`; the mini-map hides
while it is up); line 197 `chunk_size = 350` highlights; lines 199–200 get a GREY dashed ghost
argument `chunk_overlap = ?` beside them.
SAY: Recursive splitting gets only a chunk size, the same 350. No overlap is given.

SHOW: LECTURE B16–B19. The panel leaves; mini-map, "chunking" lit. V3's scissors. The same
word-block ribbon, with paragraph gaps as wider spaces and line breaks as row ends; four PURPLE
separator chips in order `\n\n`, `\n`, `" "`, `""`. The scissors hunt along the ribbon: they first
try the blank line between paragraphs (chip 1 lights), then a line break, then a space; every cut
lands between blocks. Small, at the side: the lecture's mock paper, sections marked, with a ruler
running one section's heading into the next (RED) beside one-chunk-per-section (GREEN) (tag
`illustration`).
SAY: It works like scissors that look for the best gap. First a blank line between paragraphs, then a line break, then a space, and only as a last resort, a single character. So every cut falls between words.

SHOW: Terminal (full width, 13 rows, TEAL). It types `python cli.py --chunk --chunk_type recursive-split`
→ TERM(cli-container/13-chunk-recursive-split.txt: 2–4, …, 32–33) (no `wrap`); then (TRACKER Chunk 3 ·
extra) `wc -l outputs/chunks-recursive-split-*.jsonl` (extra) →
TERM(cli-container/14-x-wc-recursive-split.txt: 11, 13). 2 + 6 + 2 + 2 + 1 = 13 rows: the README
command stays on screen. `35` and `14228 total` highlight. `▶ your turn` beside the README command.
SAY: Step 3: the same command with chunk type recursive split. The story now makes 35 chunks, and an extra line count gives 14,228 in total. Pause and run it.

SHOW: The terminal shrinks to a strip. Two GREEN bars above it: "char-split 8,248" and
"recursive-split 14,228", both labelled "chunk size 350". The ponder card sits in the lower third,
above the strip.
PONDER(8 s, "Same chunk size, 350.\nWhy 14,228 chunks instead of 8,248?")
SAY: Same chunk size, 350. So why 14,228 chunks instead of 8,248?

SHOW: TRACKER Chunk 3 · extra. It types the one-liner of `cli-container/15-x-recursive-chunks.txt`
(extra; folds) → TERM(cli-container/15-x-recursive-chunks.txt: 8–16; wrap) (the terminal grows to 12
rows; the bars go). `## Chapter One: The First Slice` on line 8 and again on line 12 highlight
YELLOW, joined by a PINK bracket "repeated". A chip: "library default: chunk_overlap = 200" with an
`erratum` tag "the README says overlapping, not how much".
SAY: Look at the first chunks. Chunk 1 starts again with Chapter One, repeating the end of chunk 0. The splitter's library default is an overlap of up to 200 characters, which the README never mentions. Cutting at boundaries also makes chunks shorter.

SHOW: The terminal shrinks to the strip. V3's ribbon returns with recursive chunks drawn as cards,
wide overlap bands shaded; each band gets a small GOLD coin glyph "embedded, stored, paid for".
A GREY chip "want another value? set chunk_overlap".
SAY: Overlap is insurance against cutting an idea in half. But every repeated character is embedded, stored, and paid for. If you want a different value, set chunk overlap yourself.

SHOW: The lecture's mock paper from beat 2 grows: three section-shaped chunks (title, abstract,
methods) in GREEN. Two arrows from the strip's command: "recursive: paragraphs" (part way) and
"semantic chunking · part 2" (all the way, GREY dashed). V1 mini-map: "chunking" gets a GREEN tick.
Fade out.
SAY: The lecture's point is that ideal chunks follow the document's own structure. Recursive splitting goes part of the way, using paragraphs. Semantic chunking, in part 2, goes further.

---

## S08 · Meaning as direction: embeddings — `s08_embed.py` · `Embeddings`

Lecture: A24–A28, A40–A47, B59–B60.

SHOW: LECTURE A24–A28. TRACKER Embed (no step lit yet). Mini-map, "embedding model" lit. V4: chunk
cards fly through the BLUE embedding box into a 2-D drawing of a sphere (a circle and a dashed
equator ellipse) and each becomes a GREEN arrow from the origin, drawn as a 2-D projection; arrows
of cards about milk and curd cluster together, arrows of license-text cards sit elsewhere (tag `our
illustration`, caption "a sketch of 3-D; each real vector has 256 numbers"). A GREY chip "one vector
per chunk · a sentence embedding, not a word embedding".
SAY: Next, the embedding model. It turns each chunk into one vector, a list of numbers, so similar meanings point in similar directions: in this sketch, curd near curd, license text elsewhere.

SHOW: LECTURE A40–A43. Only the instructor's column of the lecture's table writes in (five rows:
extroversion, emotional stability, agreeableness, conscientiousness, imagination; tag `lecture
example`), then becomes an arrow; the three candidates appear directly as arrows in a 2-D sketch
(tag `sketch · not to scale`, angles and lengths exaggerated: the first candidate at 10° and short,
the second at 25° and 1.4× longer, the third at 45°). A YELLOW angle arc between the instructor's
arrow and each candidate's. A small podium: "cosine: A 0.986 · B 0.976 · C 0.886"; the first
candidate's medal card gets a GREEN tick. A GREY caption "lecture game: who is most like the instructor?"
comes in on "which of three candidates" and leaves before the measures table.
SAY: The personality game from lecture makes this concrete: which of three candidates is most like the instructor? Five scores make each person a five-number vector. Cosine similarity compares only the angle, and picks the first candidate.

SHOW: LECTURE A44–A47. A second podium: "dot product: B 81.2 · A 80.2" (tag "computed from the
lecture's table · not on the slides", SLIDES.md A40–A43); the second candidate's longer arrow
pulses, and the first and second medal cards swap places (a Transform) as the SAY reaches "would
pick the second candidate". A small three-row table: cosine (angle), Euclidean (distance), dot
product (angle and length).
SAY: The dot product also counts length, and would pick the second candidate, whose arrow is longer. So a measure is a choice; for text, cosine is the usual one.

SHOW: CODE(cli.py: 22–27) (header `cli.py · lines 22–27`); lines 24–26 highlight. A long BLUE bar of
3,072 cells (GREY labels "the model's full output" and "length 1") is cut after its first 256
cells, which turn GREEN: "output_dimensionality = 256"; the 256-cell arrow shrinks to ≈ 0.4 of a
dashed unit circle.
SAY: The tutorial's model, Gemini embedding 001, natively returns 3,072 numbers. The code asks for the first 256. The model is trained to make that prefix useful alone.

SHOW: CODE(cli.py: 96–106) (the mini-map hides). A stack of GREEN chunk cards goes to the BLUE box in
batches of 100 (chip `cli.py · lines 252–253`, `batch_size=100`), a GOLD tick per batch. A GREY chip
`cli.py · lines 108–119` "on an API error: retry after 5, 10, 20, 40, 80 s · then give up" (no RED
animation).
SAY: Chunks go to the model in batches of 100. On an API error, it retries up to 5 times, doubling the wait from 5 seconds.

SHOW: LECTURE B59–B60. The panel leaves. V1 full width (the mini-map grows into it): the shared BLUE
box lights from the top lane ("chunks · now"), then from the bottom lane ("questions · later").
Chip `cli.py · lines 75–84` `generate_query_embedding` "same model, same 256".
SAY: Your question will use this same model, later. Chunks now, questions later: one model.

SHOW: TRACKER Embed 1. V1 shrinks back to the mini-map. Terminal (full width, 12 rows, TEAL). It types
`python cli.py --embed --chunk_type char-split` → TERM(cli-container/20-embed-char-split.txt: 2–6, …,
21–22, …, 73; wrap) with the tag `real run · no key`. Line 73 prints RED. A GOLD tag on the command:
"first Google call · your project pays".
SAY: Step 1: python cli.py, dash dash embed, chunk type char split. It's the first call to Google. On our machine it reads the first book, then stops at the missing key file. On yours, it runs.

SHOW: The terminal shrinks to the strip. A GREY "with your key, look for" card, items writing in as
named: "Processing file: outputs/chunks-char-split-… · per book" (`cli.py:240`); "a 5-second pause"
(`:256`); "a second table with an embedding column" (`:259-260`); "embeddings-char-split-*.jsonl beside
the chunks" (`:262-264`).
SAY: With your key, look for each book's file, a 5-second pause, a table with an embedding column, and new embeddings files beside the chunks.

SHOW: A second GREY card above the strip, "if it fails (with your key)", rows writing in as named:
"File /secrets/llm-service-account.json was not found → not in ../secrets under that name · check:
ls -la /secrets in the container"; "API error (code: 403) … Retrying in 5 seconds (attempt 1/5) →
the message names the cause · gives up after 5 tries, ~2.5 min (`cli.py · lines 117–118`)";
"PERMISSION_DENIED → fix GCP_PROJECT in docker-shell.sh, or the role in IAM (console) · then exit
and sh docker-shell.sh again"; "SERVICE_DISABLED → enable the Vertex AI API, wait a minute, rerun".
SAY: If yours fails, or keeps retrying, read the error. Key file not found: check its name in secrets. Permission denied: fix the Project ID or the role, then exit and start the script again. Service disabled: switch on the API.

SHOW: TRACKER Embed 2. The cards leave. It types `python cli.py --embed --chunk_type recursive-split`
(no output panel). `▶ your turn` on a GREY card listing both embed commands, with a GREY row "each
run sleeps 5 s per book (cli.py · line 256)". A GOLD tag: "≈ 89 calls (char-split) · ≈ 148 calls
(recursive-split) · cents, by our estimate · check the current price list".
SAY: Step 2 does the same for recursive split. Pause and run both, with your key: about 89 and 148 calls, a few cents by our estimate. Check the current price list.

SHOW: A card (tag `recorded · the staff's vectors (68e0bde)`): a GREY commit chip `68e0bde` "the staff
committed their outputs/" → a RED strike chip `d9ced19` "reverted · merged in e17a39f" → a GREY note
"still in every clone's history"; a small GREY chip `58dd602` "their database removed too"; under it
`22 files · 82 MB` (from `recorded-embeddings/00` lines 2–3) and a GREEN check "their 22 chunk files
= ours, byte for byte". The command that copied them is not shown. A GREY row along the card's foot:
"no key yet? the study guide shows how to copy these into outputs/".
SAY: The video goes on with the staff's own outputs, once committed and still in every clone's history. Their chunk files match ours byte for byte, so their vectors are what this command makes.

SHOW: TRACKER Embed 2 · extra. A GREY card "an extra Python check · Tolminc's vectors: count, first
five, lengths" (code not shown); terminal (strip, 4 rows) → TERM(recorded-embeddings/06-x-vector-norms.txt:
9–11) with the tag `recorded · the staff's vectors (68e0bde)`. Above, V4's arrows: each GREEN arrow
gets a ruler mark at about 0.4 of a dashed unit circle.
SAY: An extra check on the story's vectors. 24 rows of 256 numbers. Their lengths run from 0.369 to 0.402, not 1.

SHOW: The dashed unit circle and the short arrows stay; one arrow is stretched to length 1 and back.
A GREY chip `"hnsw:space": "cosine"` (`cli.py:288`) with a GREY note "the measure, set at load
(next scene)". The ponder card sits in the lower
third.
PONDER(8 s, "Our database will compare by cosine (set when we load).\nThese vectors are shorter than 1, and not all the same length.\nDoes that change which chunks count as nearest?")
SAY: When we load them, the database will compare by cosine, and these arrows are shorter than 1. Does that change which chunks count as nearest?

SHOW: The stretched arrow keeps its angle arc unchanged (YELLOW "cosine: same"). Then a GREY "what if"
inset (tag `illustration`): with straight-line distance, the stretched arrow's distance to the
query changes, RED.
SAY: No: cosine only sees the angle. With straight-line distance, Chroma's default, or a dot product, length would leak into the ranking: the game's lesson.

---

## S09 · Load: records, an index, a folder on your disk — `s09_load.py` · `LoadChroma`

Lecture: A30–A38.

SHOW: LECTURE A30–A31. TRACKER Load (no step lit yet). Mini-map, "vector database" lit. A GREY table
glyph with a SQL chip `WHERE price BETWEEN 10 AND 50` (GREEN tick); then a PINK question "chunks that
mean something like this" bounces off it (RED cross), and lands in the TEAL cylinder.
SAY: An ordinary database answers precise questions, like a price between 10 and 50, but it can't find rows whose meaning is like a question. A vector database can.

SHOW: V5. GREEN arrows drop into rows with four cells as named: id `1021665fac86c5a5-0`, document
(chunk text, blurred), metadata `{book, author, year}`, embedding. CODE(cli.py: 127–130) (header
`cli.py · lines 127–130`) highlights with the id cell, then Transforms into CODE(cli.py: 132–138) as
the metadata cell lights. Rows stack into a GREEN collection labelled `char-split-collection` (chip
`cli.py · line 277` `f"{method}-collection"`).
SAY: Each chunk becomes a record: an ID, the text, metadata with book, author and year, and the vector. The ID hashes the book's name plus the row number, so it's stable.

SHOW: CODE(cli.py: 280–290) (the mini-map hides); line 282 `delete_collection` highlights RED as the
collection empties, lines 287–288 GREEN as it is recreated with the chip `{"hnsw:space": "cosine"}`.
SAY: Records go into a collection, one per chunk type. The load step deletes it and creates it again, with cosine as its measure: every load is a full rebuild.

SHOW: LECTURE A32–A38. A small GREY strip of the lecture's four stages (Indexing → Vector Database →
Querying → Post Processing), "Indexing" lit. A PINK pointer walks down a column of ~30 rows while a
counter ticks to "8,248" ("slow"). Then the rows lift into a layered graph (tag `our illustration of
HNSW`): a sparse top layer, denser layers below; the pointer hops down in four steps to a neighbor.
SAY: Comparing a question with every vector is slow at scale. So the database builds an index, in these slides' sense: a layered graph called H-N-S-W, where a search hops down in a few steps.

SHOW: TRACKER Load 1. Terminal (full width, 10 rows, TEAL). It types
`python cli.py --load --chunk_type char-split` → TERM(cli-container/30-load-char-split.txt: 2–8; wrap)
with a GREY caption "first run · before any embeddings existed". Line 5 `did not exist. Creating new.`
and line 8 `Number of files to process: 0` highlight YELLOW; a GREY note "0 here = your embed step
didn't finish".
SAY: Step 1: python cli.py, dash dash load, chunk type char split. On our first run there were no embeddings yet: it made an empty collection and found 0 files. If you see 0, your embed step didn't finish.

SHOW: The terminal clears; tag `recorded · the staff's vectors (68e0bde)`. The same command again →
TERM(recorded-embeddings/01-load-char-split.txt: 2–12, 19–22, …, 152–153; wrap) (13 rows; the first
rows scroll). Line 5 `Deleted existing collection` highlights; line 11–12's `embedding` column
highlights GREEN; lines 19–22 tick the inserted counter. Above the terminal, a GREEN counter adds
up the books to "8,248".
SAY: On the staff's recorded vectors, the same command deletes that empty collection and reads 11 files with an embedding column. It inserts 8,248 records, in batches of 500.

SHOW: TRACKER Load 2. It types `python cli.py --load --chunk_type recursive-split` →
TERM(recorded-embeddings/02-load-recursive-split.txt: 2–8, …, 163–164; wrap). A second GREEN
collection `recursive-split-collection` stacks beside the first: "14,228". The terminal shrinks to
the strip; `▶ your turn` on a GREY card listing both load commands and a third row "(link)
ac215-llm-rag.dlops.io/chromaui · in Chrome · step 3, below".
SAY: Step 2 loads recursive split, 14,228 records. Pause and run both loads.

SHOW: TRACKER Load 2 · extra. Second laptop terminal (strip): it types the `curl … | grep …` line of
`recorded-embeddings/03` (extra; folds) → TERM(recorded-embeddings/03-x-collection-names.txt: 2–5),
`"dimension":256` highlighted, beside a GREY ghost of `laptop/17b` line 3 `"dimension":null` (tag
"before the first insert").
SAY: An extra check: both collections now have dimension 256, fixed by the first insert.

SHOW: The strip clears. A GREY card "an extra Python check · one metadata dict per book" →
TERM(recorded-embeddings/07-x-metadata-per-book.txt: 11, …, 22) (tag `recorded`); line 22 RED,
`erratum`. CODE(cli.py: 178) excerpt chip `filename.split(".")[0]` with the Woman's Institute file
name cut at its first dot; fix chip "os.path.splitext(filename)[0] · delete outputs/*Womans Institute
Library of Cookery.jsonl · then chunk, embed, load".
SAY: And one book has no author or year: a small slip cuts its file name at the first dot. Split off only the extension, delete that book's old files in outputs, then chunk, embed and load again.

SHOW: Second laptop terminal (8 rows): it types `ls -la docker-volumes/chromadb; du -sh docker-volumes/chromadb`
(extra; folds) → TERM(recorded-embeddings/04-x-docker-volumes.txt: 2–8) (UUID rows cut with `…`).
`59781120` and `82M` highlight; the two UUID folders get GREEN labels "index · one per collection"
(tag `your numbers will differ`; nothing captured maps a UUID to a collection). Above, V5 zooms out:
the cylinder inside the TEAL Chroma box pours through the PINK `/data` route into the GREY folder. A
README chip `README.md · line 160` "persistent".
SAY: The docker volumes folder on your laptop now holds a 60-megabyte SQLite file and two index folders, one per collection, owned by root. The README calls it persistent.

SHOW: TRACKER Load 3. A GREY browser frame (tag `illustration`), address
`ac215-llm-rag.dlops.io/chromaui`, a schematic collection list (no screenshot); a PINK arrow from the
page through the GREY door `:8000` to the Chroma box. Beside it, two short strips: `laptop/12` line 5
`access-control-allow-origin: https://ac215-llm-rag.dlops.io` (GREEN) and a GREY ghost "no such line
for another site, e.g. `Origin: https://example.com`" (from `laptop/12b`), headed by the whole command
on two rows, `curl -si -H 'Origin: https://ac215-llm-rag.dlops.io' \` / `    http://localhost:8000/api/v2/heartbeat`
(extra). A
GREY note on the browser frame: "if Chrome asks to reach your local network, allow it".
SAY: Step 3 is a link to the course's Chroma UI. Opened in Chrome, it reads your local database through port 8000; Chroma's settings let the course's site in.

SHOW: The full V1 returns; its top lane glows end to end, GREEN ticks on chunk, embed, load. A
caption "part 1: the index is built". Fade to an empty frame (end of part 1).
SAY: The top lane is done: the index is built. In part 2, we ask it questions.

---

## S10 · Exit, and the index survives — `s10_persist.py` · `IndexSurvives`

Lecture: none.

SHOW: Part 2 opens. V1 full width as S09 left it: the top lane GREEN with ticks on chunk, embed and
load, the bottom lane GREY with the caption "part 2". The TEAL cylinder grows and Transforms into
V2's Chroma box on the rail, its PINK `/data` route reaching the GREY `docker-volumes/chromadb/`
folder, with the CLI box beside it; a YELLOW "?" over the folder. V2 then shrinks to the top.
SAY: In part 1, we built the index: chunk, embed, load. Part 2 puts it to work. But first, a test: does the index survive closing the laptop?

SHOW: TRACKER Run 3 · extra. Container terminal (strip, TEAL, prompt `app@92c5bfd26089:/app$`): it
types `exit` (extra) → TERM(laptop/07-docker-shell.txt: 46). The CLI box dissolves (`--rm`). The same
terminal's frame turns GREY, title `laptop`, prompt `student@laptop:~/AC215/llm-rag$`, and it grows
to 6 rows. It types `docker ps -a` (extra) → TERM(laptop/20-x-ps-after-exit.txt: 2–3) as the column
view; the Chroma row highlights YELLOW, "Up 2 minutes", and the PINK `8000` door stays lit.
SAY: Leaving isn't in the README. Type exit, and on the laptop, list every container with docker ps dash a. The CLI container is gone, removed on exit, but Chroma is still up, and port 8000 is still taken.

SHOW: It types `docker compose down` (extra) → TERM(laptop/21-x-compose-down.txt: 2–7) (2–3 joined).
Lines 2–4 print RED, then fade to GREY "harmless: the values live only in docker-shell.sh"; lines
6–7 remove the Chroma box and the rail from the picture.
SAY: To stop it, run docker compose down from the repo folder. Two warnings say the variables aren't set. They're harmless: only the script sets them, and the down command needs neither. Then Chroma and the network are removed.

SHOW: The terminal clears and grows to 13 rows. It types `docker ps -a; docker network ls; ls -la
docker-volumes/chromadb` (extra) → TERM(laptop/22-x-after-down.txt: 2–12) (UUID rows cut with `…`);
the empty container table and the `chroma.sqlite3` row highlight; a GREY note beside the network
rows "no llm-rag-network". In the picture only the GREY folder remains, glowing.
SAY: Nothing is running now. But the docker volumes folder on your disk still holds the database file and both index folders, and your chunk files in outputs are untouched.

SHOW: TRACKER Run 3. The terminal clears (13 rows). It types `sh docker-shell.sh` →
TERM(laptop/23-x-docker-shell-again.txt: 2–12; session), then the prompt `app@390fe47a277a:/app$`
(TEAL frame): the command, the output and the new prompt are all on screen. `[+] run 2/2`
highlights; a GREY chip "no pull · no build: the image exists". New TEAL boxes land over the same
GREY folder. A GREY note: "after a git pull that changes pyproject.toml or the Dockerfile: docker
compose build". `▶ your turn`.
SAY: Back another day: sh docker-shell.sh again. No pull, no build: the image exists. After a git pull that changes the dependencies or the Dockerfile, run docker compose build first. Pause and restart.

SHOW: TRACKER Run 3 · extra. Second laptop terminal (strip): the `curl … | grep …` line (extra) →
TERM(laptop/24-x-collection-names-after-restart.txt: 2–5), both `"dimension":256`. Then the
container: `python cli.py --get --chunk_type char-split` (extra; GREY note "not in the README · S12")
→ TERM(cli-container/70-x-get-after-restart.txt: 6 cut after the ids list's `]`; wrap); above it a
PANEL of `recorded-embeddings/05` line 6 cut the same way, header "the same command before exit".
The first and last id of each list get GREEN ticks, and a chip "10 of 10 match".
SAY: Two extra checks: both collections are back, with dimension 256, and an extra command called get returns the same 10 record IDs. The container was disposable; the data never lived in it.

---

## S11 · Asking the database: rank and cut — `s11_query.py` · `NearestNeighbours`

Lecture: A39, A48–A53.

SHOW: LECTURE A39. TRACKER Query (no step lit yet). V1's bottom lane lights: the PINK question `How
is tolminc cheese made?` passes through the lower half of the BLUE embedding box and comes out as a
PINK query vector among the GREEN vectors (V4's sphere drawing, tag `our illustration`); a PINK
search beam sweeps to its nearest arrows.
SAY: Now the bottom lane. The question goes through the same embedding model and becomes a query vector, in the same space as the chunks. Querying means finding its nearest neighbors.

SHOW: LECTURE A48–A53. V6, first half: a column of stored vectors (GREEN bars) and the PINK query
vector; similarity scores write in one by one beside four rows: 0.57, 0.77, 0.43, 0.93 (tag `lecture
example`). The column re-sorts by score; a YELLOW line cuts it under the top rows, "top K".
SAY: The lecture scores every stored vector against the query. 0.57, 0.77, 0.43, 0.93. Sort by score, and keep the top K, with K fixed in advance. This code uses 10.

SHOW: The flip: each score becomes 1 − score (0.07, 0.23, 0.43, 0.57) and the arrow labelled "better"
beside the column turns upside down; header changes from "similarity (lecture)" to "cosine distance
(Chroma)"; a small GREY scale under it: "similarity −1 … 1 → distance 2 … 0 · 0 = same direction".
SAY: One difference: the lecture ranks by similarity, where higher is better. Chroma reports cosine distance, one minus the similarity, where smaller is closer. Same order, opposite direction.

SHOW: The YELLOW K-line stays; rows below it dim. A GREY note "no distance threshold in this code":
even when every row is far away, ten rows sit above the line (fewer only if fewer chunks are
available).
SAY: And a query returns K results whenever K chunks are available, relevant or not. Nothing in this code sets a distance threshold.

SHOW: CODE(cli.py: 316–323) (header `cli.py · lines 316–323`; the mini-map hides); line 318 (the
question), line 319 (`generate_query_embedding`, with a BLUE glyph of the shared box) and line 323
(`get_collection`) highlight in turn.
SAY: In the code, the query function sets the question, turns it into a vector with the same Google model, and opens the chunk type's collection.

SHOW: TRACKER Query 1. Terminal (full width, 11 rows, TEAL). It types
`python cli.py --query --chunk_type char-split` with a GOLD tag "one embedding call per question ·
your project pays" → TERM(cli-container/40-query-char-split.txt: 2–3, …, 9–13, …, 64; wrap) with the
tag `real run · no key`. Line 3 `load()` gets a YELLOW box and an `erratum` tag "a copy-paste label ·
cli.py · line 310"; line 64 RED. Above (strip mode after the print), a small picture: the TEAL
cylinder blinks once (connected, `cli.py · line 313`), then stays idle, captioned "connected · no
search ran"; the PINK question stops at the BLUE box, RED cross.
SAY: Step 1: python cli.py, dash dash query, chunk type char split. A small slip first: it prints the word load, a label copied from the load code. Then it connects to Chroma, but stops at the key while embedding the question, before it searches.

SHOW: The PINK question card, made of words, slides at the TEAL cylinder and bumps off a slot shaped
like an arrow; chip "Chroma takes vectors, not words". It returns to the BLUE box, which would turn
it into a PINK arrow that fits the slot; the GOLD key is missing, so the box stays dark, RED cross. A
GREY chip "only the same model makes a vector in the same space".
SAY: The question must become a vector before the database can compare it, and only the same Google model makes one in the same space.

SHOW: TRACKER Query 2. It types `python cli.py --query --chunk_type recursive-split` (no output panel).
`▶ your turn` on a GREY card listing both query commands, with the GOLD tag "one embedding call per
question". The terminal shrinks; a GREY "with your key, look for" card writes in: "Embedding values:
… 256 numbers" (`cli.py:320`); "Query: How is tolminc cheese made?" (`:360`); "Results: a dict of
lists of lists" (`:361`), with four GREY empty slots "ids · distances · metadatas · documents", each
holding one inner list (no values).
SAY: Step 2 runs it on recursive split. With your key, look for 256 embedding values, the query, and the results. The results are lists of lists: one list per query, holding IDs, distances, metadata and documents. Pause and run both.

SHOW: A chip `cli.py · line 386 · in chat()` `results["documents"][0]` with `[0]` highlighted YELLOW
and pointing at the first inner list. A GREY note "no results were recorded: next, we ask the
loaded database directly". Fade out.
SAY: That's why chat, later, reads documents, item zero. No results were recorded, so next we ask the loaded database directly.

---

## S12 · Filters come first — `s12_filters.py` · `FiltersFirst`

Lecture: A54–A55.

SHOW: TRACKER Query 2 · extra. CODE(cli.py: 352–361) (header `cli.py · lines 352–361`); line 356
`n_results=10`, line 357 `where={"book": "The Complete Book of Cheese"}` and line 358
`where_document={"$contains": search_string}` (with line 353 `search_string = "Italian"`) highlight
in turn, line 357 and 358 with PINK edges.
SAY: Here's the query the code sends: 10 results and two filters. The metadata filter keeps one book, The Complete Book of Cheese. The document filter keeps chunks that contain Italian.

SHOW: V6, second half: a cloud of about 1,000 small GREEN dots for the char-split collection, caption
"1 dot ≈ 8 chunks" (tag `our illustration` for the layout); the PINK question sits among a cluster of
dots labelled "Tolminc story". The ponder card sits in the lower third, the cloud above it.
PONDER(8 s, "The question is about Tolminc.\nThe query keeps one book, and only chunks containing 'Italian'.\nWhat will the ten results be about?")
SAY: The question is about Tolminc. What will the 10 results be about?

SHOW: A GREY card "an extra Python check · counts with the query's filters · code: study guide,
Step 9" (tag `recorded`); the
mask animates on the dots with each count: "8,248" (`recorded-embeddings/08` line 11) → the book
filter dims all but "1,355" (also `cli-container/11` line 8, the book's chunk file) → `$contains
"Italian"` dims all but "64" (`08` line 13), shown as 64 separate brighter dots → a YELLOW counter
"mentioning Tolminc: 0" (`08` line 14). A strip prints TERM(recorded-embeddings/08-x-filter-counts.txt:
13–15). The Tolminc cluster is fully dimmed.
SAY: An extra check counts them in the loaded collection. Of 8,248 chunks, the book filter keeps 1,355. The word Italian keeps 64. How many mention Tolminc? None.

SHOW: Tag `stand-in query · a stored story chunk's vector`. A GREY card "an extra Python check ·
code: study guide, Step 9"; terminal (11 rows) → TERM(recorded-embeddings/09-x-query-by-chunk-vector.txt:
16–28; wrap). `0.0000` gets a GREY tag "itself"; `0.1627` highlights. Above (after the print, strip
mode), the PINK beam from the stand-in point reaches its ten nearest, all inside the Tolminc
cluster.
SAY: Now a search. The real question needs Google to become a vector, so we use a stand-in: the stored vector of one story chunk. Without filters, its 10 nearest are all from the story, at distances from 0, the chunk itself, up to 0.16.

SHOW: TERM(recorded-embeddings/09-x-query-by-chunk-vector.txt: 29–39) (the terminal clears first).
`0.2833` and `0.3123` highlight. In the picture the mask returns: the beam has to stretch past the
dimmed cluster to the far, lit survivors, all labelled "The Complete Book of Cheese".
SAY: With the code's filters, all 10 results come from The Complete Book of Cheese. Their distances run from 0.28 to 0.31. The filters act first, and top K fills its 10 places with whatever survives, however far.

SHOW: LECTURE A54–A55. The lecture's four-stage strip (Indexing → Vector Database → Querying → Post
Processing), with a box "metadata filter" sitting in Post Processing: the ten story results pass
through it and all ten are struck out, leaving an empty list (RED "nothing left"). Then the box
slides left to *before* Querying, and a GREY caption reads "Chroma: filter, then rank · 10 results,
wrong cheese".
SAY: The lecture puts metadata filtering after ranking: here, that would drop all 10 story chunks and return nothing. Chroma filters first, so you get 10 results, about the wrong cheese.

SHOW: CODE(cli.py: 325–331) (header `cli.py · lines 325–331`), the `#` marks highlighted GREY, tag
`erratum`; a README chip `README.md · line 186` "Apply various types of filters". A GREY chip
"uncomment lines 326–331 · variant 4 still prints after it · needs your key · no rebuild: the code is
mounted". A small chip `$contains` = "keyword filter (case-sensitive) · not keyword ranking (S15)".
SAY: A small slip: the README promises various filters, but only variant 4 runs; variants 1 to 3 are commented out. Uncomment the first, with no filter, and every chunk competes. And contains is a keyword filter, not a keyword ranking.

SHOW: TRACKER Query 2 · extra. Terminal (TEAL, 9 rows): it types `python cli.py --get --chunk_type char-split`
(extra; GREY note "not in the README · cli.py · lines 402–418") → TERM(recorded-embeddings/05-x-get.txt:
2–3, 6 cut after the ids list's `]`, a GREY " …" after it; wrap) with the tag `recorded`; a GREY note "no distances: no
ranking". The terminal shrinks to the strip as the ten returned ids become ten cards in the
cylinder, labelled as `recorded-embeddings/05`'s documents are: "-0 to -2 Gutenberg header" (RED),
"-3 to -5 title page, contents" (GREY), "-6 to -9 chapter one begins" (GREEN). Last, the GREEN fix card:
"the fix: keep only the text between the `*** START OF` and `*** END OF` lines · then chunk, embed,
load again". The documents of `05` line 6 are
never printed (names of the book's producers and author).
SAY: The get command from the restart check uses the same book filter, but no question, so no distances. Its 10 records start with the Gutenberg header, then the title page and contents. That header, and each book's closing license, are indexed like any text: strip them before chunking.

---

## S13 · Chat: the prompt is the whole trick — `s13_chat.py` · `FinalPrompt`

Lecture: A57–A62, B78.

SHOW: LECTURE A57–A59. TRACKER Chat (no step lit yet). Mini-map, the prompt card and the LLM lit.
V7: three blocks write in, stacked: "system prompt · how to behave" (GREY), "query · the user's
input" (PINK), "context · retrieved text" (GREEN), with a brace "final prompt".
SAY: Now generation. The lecture's final prompt has three parts: a system prompt that says how to behave, the user's query, and the context retrieved from the database.

SHOW: CODE(cli.py: 379–386) (header `cli.py · lines 379–386`; the mini-map hides); lines 380–383
highlight, with a GREY chip "no filter this time"; `n_results=10` YELLOW. Ten GREEN chunk cards drop
out of the cylinder.
SAY: In chat, the code queries again, this time with no filter, for 10 results.

SHOW: CODE(cli.py: 388–391) (header `cli.py · lines 388–391`): the PINK question card and the ten
GREEN cards stack into one prompt card in that shape (question, then the chunks joined by newlines);
a small ORANGE chip on line 390 "needs Python 3.12" (not narrated). The panel Transforms into
CODE(cli.py: 394–396) as the prompt card flows into the BLUE LLM box (`gemini-3.1-flash-lite`, chip
`cli.py · line 27`); an answer shape (gray bars, no words) comes out, with thin arrows back to the
cards it should draw from.
SAY: Then it builds the input prompt: the question, followed by the 10 chunks, joined by newlines. The prompt goes to Gemini 3.1 Flash Lite.

SHOW: The system-prompt block from the first beat becomes a GREY dashed ghost card labelled
`SYSTEM_INSTRUCTION` with CODE(cli.py: 40–41) inside it (line 41 wrapped; header `cli.py · lines
40–41 · line 41 wrapped`), then CODE(cli.py: 47) (wrapped) under it. Its cable hangs loose beside
the BLUE box, RED, unplugged; lines 394–396 flash again: `contents=INPUT_PROMPT`, no `config`. A
README chip `README.md · line 21` "grounded in your documents" appears as "never sent" is said.
SAY: So where's the system prompt? Line 40 defines one: answer only from the chunks, and say so when they don't contain enough. But look at the call. It's never sent.

SHOW: Tag `erratum`. The cable plugs in, GREEN, with a fix chip on two rows,
`config=types.GenerateContentConfig(` / `  system_instruction=SYSTEM_INSTRUCTION)`, tagged `fix · not
in the repo`. Beside it CODE(pipenv-branch/cli.py: 62–64) (header `pipenv · cli.py · lines 62–64`),
tag "pipenv branch (March 2025) sent it".
SAY: A small slip, with a one-line fix: pass it in a config argument. The older pipenv branch did send it. Without it, the README's promise of grounded answers rests on the chunks alone.

SHOW: LECTURE A61–A62. The BLUE LLM box with a GREY padlock "weights unchanged"; the TEAL cylinder
empties (dashed "delete the collection") and the answer's arrows to the cards fade away.
SAY: And notice what didn't change: the model itself. No weights moved. Delete the collection, and the knowledge is gone.

SHOW: TRACKER Chat 1 → Chat 2. Terminal (strip, TEAL). It types
`python cli.py --chat --chunk_type char-split`, then `python cli.py --chat --chunk_type recursive-split`
(no output panels). A GREY note "no key: both stop at cli.py · line 373, embedding the question".
A GOLD tag "per question: one embedding call + one Gemini call". (The `▶` comes on the step-3
card, which lists both commands.)
SAY: Steps 1 and 2: python cli.py, dash dash chat, for char split and for recursive split. Without a key, both stop embedding the question. Each question costs one embedding call and one Gemini call.

SHOW: A GREY "with your key, look for" card, items writing in as named: "chat()" (`cli.py:365`);
"Query: How is tolminc cheese made??" (`:374`), the two question marks boxed with an `erratum` tag
"harmless · the README shows one"; "Embedding values: … 256 numbers" (`:375`); "Results:" (`:384`);
"10" (`:386`); "INPUT_PROMPT: …your chunks…" (`:393`); "LLM Response: …" (`:399`).
SAY: With your key, look for the query, printed with two question marks, a harmless slip, and its 256 embedding values. Then the results, the number 10, the input prompt with your chunks, and the model's response.

SHOW: S01's chat box returns, with `How is tolminc cheese made?`, its RED-edged answer bars and the
YELLOW "?". The bars draw thin arrows to GREEN chunk cards and turn GREEN where they do (tag
`illustration`: a shape, not an answer); the "?" resolves. Then a grounding test card, two columns.
Left, GREEN: "from your chunks: Mara · her grandfather · the curd" (from the story: `Tolminc
Cheese.txt` lines 8, 10, 102; chip line 4 *A fictional tale*). Right, RED: "not in your chunks:
real-world rules for Tolminc" (a GREY note: only 3 char-split chunks contain the word "Tolminc",
`recorded-embeddings/08` line 15). A GREY note "compare the char-split and recursive-split answers".
LECTURE B78 as the grounding test card comes in; its heading reads "a grounding test · the lecture's
IsSUP check, done by eye"; the tag leaves with the card.
SAY: Remember the opening question? The story is fiction, so an answer about Mara, her grandfather and the curd came from your chunks. Real-world rules for Tolminc came from the model's memory. Compare both chunk types.

SHOW: TRACKER Chat 3. A GREY browser frame (tag `illustration`), address
`ac215-llm-rag.dlops.io/chat`, a schematic chat page (no screenshot), with a GREY note "use Chrome".
Pause card: `▶ your turn` listing the two chat commands and the link, plus two GREY rows "your own
question: cli.py · line 372 · no rebuild" and "404 NOT_FOUND for the model? change GENERATIVE_MODEL,
cli.py · line 27". Hold 2 s, then fade out.
SAY: Step 3 is a link to the course's chat tool, in Chrome. Pause: run both chat commands with your key, then try the tool. For your own question, change line 372 of cli.py.

---

## S14 · Semantic chunking: cut where meaning shifts — `s14_semantic.py` · `SemanticSplit`

Lecture: B13–B34.

SHOW: LECTURE B19–B33. TRACKER Semantic (no step lit yet). Mini-map, "chunking" lit. Small,
at the upper left: the lecture's walk (tag `lecture example`): six numbered sentence tiles, an
anchor arrow under tile 1; "0.89" joins tiles 1–2; the anchor moves to tile 3, "0.85" and "0.68"
appear, a threshold line "0.8"; tiles 1–3 become chunk 1. The walk then shrinks into three GREEN
ticks, "split at . ? ! · one neighbor each side · cosine", and clears.
SAY: Back to chunking, with the lecture's best answer: cut where the meaning changes. On the slides, an anchor walks through the sentences and joins neighbors while their similarity stays above 0.8.

SHOW: V8, full width: a row of numbered sentence tiles from the story, each showing its first three
words (`The first thing…`; one tile zooms to its full sentence once), split by the regex chip
`semantic_splitter.py · line 118` `(?<=[.?!])\s+`. A ±1 bracket slides from tile to tile; each
three-tile window drops through the BLUE embedding box (a GOLD tick per batch of 50, chip
`semantic_splitter.py · line 206`) and becomes an arrow.
SAY: The code uses the same ingredients with a different rule. Every sentence gets a window, itself and one neighbor on each side, and each window is embedded.

SHOW: Consecutive arrows pair up; the angle between each pair rises as a PINK spike over the gap
between their tiles, building the curve from left to right (tag `our illustration`).
SAY: Then it measures the distance between each window and the next, and plots it over the text, like a seismograph.

SHOW: CODE(semantic_splitter.py: 91–96) (header `semantic_splitter.py · lines 91–96`), line 92
`"percentile": 95` highlights; a YELLOW line rises to the 95th percentile of the curve. Then
CODE(semantic_splitter.py: 239–243): the spikes above the line turn into cuts, and the tiles fall
apart into chunks of very different lengths.
SAY: Next, it draws a line at the 95th percentile, and cuts at every spike above it. So the biggest 5 percent of gaps become chunk boundaries.

SHOW: Two small cards: "char-split · --chunk · no key: ✓" (GREEN) and "semantic-split · --chunk · no
key: ?" (YELLOW). The ponder card sits in the lower third.
PONDER(8 s, "char-split ran the chunk step without a key.\nCan semantic-split?")
SAY: Char split ran the chunk step without a key. Can semantic split?

SHOW: The "?" turns into a RED cross; the window bracket and the BLUE box flash: "every window is
embedded before a single cut". Then CODE(cli.py: 207–215) (header `cli.py · lines 207–215`); line 210
`embedding_function=generate_text_embeddings` highlights, with a BLUE glyph of the shared embedding
box and a GOLD tag "a Google call".
SAY: No. To find where the meaning shifts, it has to embed every sentence window first. Look at the function handed to the chunker: generate text embeddings, the same one the embed step uses.

SHOW: TRACKER Semantic 1. Terminal (full width, 12 rows, TEAL). It types
`python cli.py --chunk --embed --load --chunk_type semantic-split` (folds onto two rows) →
TERM(cli-container/60-semantic-split.txt: 2–5, …, 11, 14, 17, 20, 23, …, 75; wrap) with the tag
`real run · no key`. The five `File …` frames highlight in a PINK chain (cli.py 212 → splitter 275 →
229 → 206 → cli.py 98); line 75 RED. A GREY chip "nothing saved" (`cli-container/61` line 2: `0`).
SAY: The README's command runs all three steps with chunk type semantic split. On our machine it fails inside the chunk step, on the first book, before a single chunk is saved.

SHOW: The terminal shrinks to the strip. GOLD tags write in: "≈ 528 embedding calls just to chunk
the corpus" · "≈ 90 more to embed the chunks" · "10–20 min" (tag "our estimate"). A GREY tip card, two rows:
"try one book first: move the others out of input-datasets/books" / "then put them back and run the
command again". A GREY
"with your key, look for" card, three rows: "per book: Number of chunks: … (cli.py · line 215), far
fewer than char-split" · "embed(): Processing file: outputs/chunks-semantic-split-… (line 240)" ·
"load(): Finished inserting … into collection 'semantic-split-collection' (line 161)". Under it a
GREY note: "429 retries are normal · stopped after 5? wait, then rerun: it starts over"; it also
sits as a GREY row on the ▶ card in the next beat.
SAY: With your key, budget for it: by our estimate, about 528 embedding calls to chunk the corpus, about 90 more to embed the chunks, and 10 to 20 minutes. Try one book first, then put the others back and run it again. Look for a chunk count per book, and finally, finished inserting into the semantic split collection.

SHOW: The cards leave. Seven GREEN bars of very different lengths (tag `our illustration`, no numbers); a GREY note "a
single-topic book still gets its top 5 % cut". `▶ your turn` on a GREY card with the README command,
"with your key", and a second row "(extra, after the load finishes) python cli.py --chat
--chunk_type semantic-split". Hold 2 s, then fade out.
SAY: The chunks come out very uneven, and even a single-topic book gets cut at its biggest gaps. Afterwards, an extra: chat works the same way. Pause and try it, with your key.

---

## S15 · Beyond naïve RAG: what the lecture adds — `s15_advanced.py` · `BeyondNaive`

Lecture: B6–B10, B35–B65.

SHOW: LECTURE B6–B10. No tracker. Tag `concept · not in the tutorial's code` (GREY dashed) top left
for the whole scene. A strip: "Indexing" → "Retrieval" (tall) → "Augmentation & Generation"; a
GREY dashed column "Pre-Retrieval" slides in before Retrieval, then "Post-Retrieval" after
it. A small seismograph glyph (S14) lights GREEN inside Pre-Retrieval: "the one lever this tutorial
implements".
SAY: The lecture goes further. Its frame adds a pre-retrieval stage and a post-retrieval stage. Semantic chunking sits in pre-retrieval: the one advanced lever this tutorial implements. Here are three more, as ideas only.

SHOW: LECTURE B36–B39. In Pre-Retrieval, GREY dashed: a long, cluttered question card shrinks into
"Where do dolphins live?" (GREEN tick); then a short vague card balloons into a long rewrite with RED
highlights "invented".
SAY: Also before retrieval: query rewriting. A model turns a cluttered question into a clean one, like where do dolphins live. But hand it a vague question, and the rewrite can invent details.

SHOW: LECTURE B42–B48. In Retrieval, GREY dashed: a PINK query card on top, "Chester went to the bank
of the river in the morning" (tag `lecture example`). Below it three paragraph cards "Chester … bank"
(riverbank early; bank, borrow money; swimming, riverbank). Two ranked lists side by side, "keyword ·
BM25" (2, 1, 3) and "vectors" (1, 3, 2). A small GREY chip: "rare words weigh most · only 3
char-split chunks contain Tolminc" (`recorded-embeddings/08` line 15).
SAY: In retrieval: hybrid search. Keywords pin down names and rare words; vectors catch meaning. Take the question: Chester went to the bank of the river in the morning. The two rank three paragraphs differently.

SHOW: The formula writes in, `w / (k + rank)`, with a GREY note "k: a constant, here 0 · not top-K ·
w = 0.5". Each list item sends 0.5 / rank to a fused bar per paragraph (tag `lecture example`):
0.75, 0.67, 0.42; the near paraphrase rises to the top. A GREY chip "tutorial: $contains only
filters".
SAY: Reciprocal rank fusion gives each paragraph one half divided by its rank, in each list, and adds them up. The near paraphrase wins with 0.75, ahead of 0.67 and 0.42.

SHOW: LECTURE B51–B65. In Post-Retrieval, GREY dashed: a column of 25 rows (top K = 25) with five
YELLOW "truly relevant" rows scattered; a chip "bi-encoder: vectors made before the question · like
our 8,248". A slower GREY diamond "cross-encoder" reads each (question, chunk) pair and reorders the
column: the YELLOW rows rise to the top. Caption "fast + accurate: strong together".
SAY: After retrieval: re-ranking. A fast retriever, whose vectors were made before the question existed, returns 25 candidates with the right ones scattered. A slower model reads each question and chunk together and reorders them.

SHOW: The three ideas shrink into a row of three GREY dashed chips (query rewriting · hybrid search + rank
fusion · re-ranking); a `cli.py` file glyph beside them with
a GREY "not here". A small GREY note under S12's filter box: "our query: remove the filter". Fade out.
SAY: None of these is in cli.py. They're what you reach for when naive retrieval brings back the wrong chunks; our filtered query only needed its filter removed.

---

## S16 · Tear down, a stale index, recap — `s16_recap.py` · `Recap`

Lecture: B68–B76, A63.

SHOW: No lecture tag yet. TRACKER Run 3 · extra. Container terminal (strip, TEAL, prompt
`app@390fe47a277a:/app$`): it types `exit` (extra) → TERM(laptop/23-x-docker-shell-again.txt: 14;
session); the frame turns GREY, prompt `student@laptop:~/AC215/llm-rag$`. It types `docker compose down` (extra) →
TERM(laptop/25-x-compose-down-final.txt: 2–7) (2–3 joined; the WARN lines GREY "harmless"). Above,
V2: the CLI box, then the Chroma box and the rail dissolve; the GREY folder stays.
SAY: Time to tear down. Type exit, then docker compose down from the repo folder: the same harmless warnings, then Chroma and the network are gone.

SHOW: It types `docker images` (extra) → TERM(laptop/26-x-images.txt: 2–5) as the column view;
`2.11GB` and `826MB` highlight; the base image's row gets a GREY tag "already inside the 2.11 GB".
A GREY chip "need the space? docker image rm llm-rag-cli chromadb/chroma:latest".
SAY: The images stay: 2.11 gigabytes for the CLI image, its Python base included, and 826 megabytes for Chroma.

SHOW: It types `git status; git status --short --ignored` (extra) → TERM(laptop/27-x-git-status.txt:
8, 11–14). ` M docker-shell.sh` highlights GREY ("your edit"); `!! docker-volumes/` and `!! outputs/`
GREEN ("ignored · stays on your disk"); the chip becomes "only to delete the index
later (Linux, root-owned): sudo rm -rf docker-volumes".
SAY: Now git status shows only your edit to docker-shell.sh. The outputs and docker volumes folders are ignored, and stay on your disk.

SHOW: The GOLD key glyph in `secrets/` beside the repo. A RED "what if" inset (tag `illustration`):
the key inside `llm-rag/` is not ignored, and a `COPY . ./` arrow packs it into an image layer, RED
cross. A GOLD tag "nothing runs in Google Cloud · you paid only for what you sent". Then the inset
clears and `▶ your turn` sits on a static GREY card "tear down", each row getting a GREEN tick as
named: `exit` (in the container) · `docker compose down` (laptop, in ~/AC215/llm-rag) · optional
`docker image rm llm-rag-cli chromadb/chroma:latest` · "keep docker-volumes/ and outputs/: your
index" · "course over: IAM › Service accounts › KEYS › delete"; a GOLD row "nothing to delete in
Google Cloud". Hold 2 s.
SAY: Nothing keeps running in Google Cloud; you paid only for what you sent. Keep the key beside the repo: inside it, git wouldn't ignore the key, and the image would copy it. Delete it when the course ends. Pause and tear down now, so port 8000 is free next time.

SHOW: The stale index. A PANEL of `expected/out-txt-agent-run.txt` line 74 cut after "economic life"
(header `out.txt · line 73 (excerpt)`, tag `recorded · the staff's agent run, September 22, 2026`),
"transhumance" highlighted. Beside it
CODE(tolminc-before-85bba32/input-datasets/books/Tolminc Cheese.txt: 102) as an excerpt chip `…known as transhumance, shaped not just the economic life…`
(header `96d5fd7 · Tolminc Cheese.txt · line 102 (excerpt)`), and today's file with a GREY chip
"line 4: A fictional tale…", a RED tag "not in today's book". A TEAL cylinder holding RED-edged
"stale" cards; an arrow "books changed → chunk, embed, load again".
SAY: One last lesson, from the staff's recorded run of next lecture's agent. It retrieved text about transhumance from an older Tolminc book, replaced that same day. The database answers from what was loaded: when the books change, rebuild the index.

SHOW: TRACKER Agents 1. A static GREY card "next lecture · inside the container:" with
`python cli.py --agent --chunk_type char-split` (tag `preview · L06`; not typed into a terminal, no
output). A PANEL of `expected/out-txt-agent-run.txt` line 65 (header `out.txt · line 64`, tag
`recorded`) `Function: get_book_by_author`, with a GREY note "must call a tool: which one is its
choice" (`cli.py · line 449`, `mode="any"`). LECTURE B68–B76: a GREY dashed "Retrieve?" diamond with
Yes/No branches (tag `concept`), caption "a related idea, further: whether to retrieve".
On "Our chat opens the book" the Yes branch flashes YELLOW with a GREY note "our chat: every
question"; on "and checks nothing" a GREY note "our chat: no check" by "check what it found".
SAY: Next lecture runs this command with an agent. In the staff's run, the model chose which retrieval tool to call. The lecture's Self-RAG goes further: the model decides whether to retrieve at all, then checks what it found. Our chat opens the book for every question, and checks nothing.

SHOW: LECTURE A63. The blurred map from S01 returns; its four YELLOW questions light up one by one,
each with a tiny thumbnail of the picture that answered it (glyph-only: V4's arrows, V5's cylinder,
V6's beam, V7's prompt card).
SAY: And the four questions? An embedding is a direction for meaning. A vector database stores records, with an index to search them. A query finds the question's nearest neighbors. The context is the chunks you paste into the prompt.

SHOW: No lecture tag. A card "Test yourself", questions appearing one at a time (each stays as the
next fades in below, smaller). Behind Q1, V1 small, both lanes with all five flags ticked: the
pipeline the viewer built. Q1 "Which cli.py flags belong to each lane, and what must both lanes
share?" Q2 "Why does the CLI reach the database at llm-rag-chromadb:8000, and who uses the published
port 8000?"
SAY: Five questions to test yourself. One: which flags belong to each lane, and what must both lanes share? Two: why does the CLI reach the database by name, and who uses port 8000?

SHOW: Q3 "What does chunk_overlap buy and cost, and why did recursive-split make 14,228 chunks?" Q4
"Why did the README's --query return no Tolminc text?" Q5 "What is the tutorial's prompt missing
compared with the lecture's final prompt, and what is the one-line fix?"
SAY: Three: what does overlap buy and cost? And why did the recursive splitter make more chunks? Four: why did the README's query return no Tolminc text? Five: what is the prompt missing, and what's the fix?

SHOW: The questions shrink to the top. Two footer cards: "Answers: study guide §8 (exercises.md)" and "Study guide +
every command: github.com/JunyiZhou-Conny/MLOps_Learning · guides/L05-rag.md". Then everything fades
to an empty frame (end of part 2).
SAY: The answers are in the exercises, and every command is in the study guide, in the MLOps Learning repo. Next time: agents.
