# AC215 · Lecture 8 — LLM: Finetuning (follow-along: llm-finetuning) — narration script & visual plan (v2: four reviews merged, `build/review_merge_log.md`)

Audience: an AC215 student who has done L1–L7: uv, `pyproject.toml` and `uv.lock` (L1); containers, images, bind
mounts and `docker-shell.sh` (L2–L4); L05's RAG with the same `llm-service-account` and the same `secrets/` folder;
L06–L07's structured outputs. They know basic ML (a loss, an optimizer, a training loop), have heard "LoRA" but never
seen its arithmetic, and have never fine-tuned an LLM. They watch with `~/AC215/llm-finetuning` open and Docker
running, optionally with a GCP project with billing and the service-account key, and the course Colab "Tutorial -
Finetuning with QLoRA" in another tab, pausing to type each command.

Goal (BRIEF.md "Audience and goal"): after the video they can say what fine-tuning changes and what it doesn't
(prompting and RAG change the input, fine-tuning changes the weights; it reliably teaches style and habits, not
facts, with the stored sky-blue answers as evidence); set up Track A (the service account and its two roles, the key
as `secrets/llm-service-account.json` next to the clone, the three places to edit, a bucket of their own, `sh
docker-shell.sh` or `bash` in each folder, `ls -la /secrets`); explain how `dataset-creator` manufactures an
instruction dataset with a teacher model and why a missing key surfaces one command later as `KeyError: 'question'`;
follow one Q&A pair from CSV row to Gemini JSONL to Qwen3's chat template to tokens; describe the managed tuning job
(`us-central1` → endpoint in `us`, `Tuned model info: None`, where the endpoint comes from) and read the stale cost
table; explain the memory ladder 120 → ~40 → ~12 GB, quantization (absmax, per-block constants, NF4, double
quantization, stored in 4 bits / computed in 16), LoRA (`W₀ + (α/r)·B·A`, B = 0, 1,146,880 from r = 8 on
`q_proj`/`v_proj` × 28), the notebook's training settings and evaluation (loss, perplexity, `disable_adapter()`, what
a perplexity drop does not prove); name the three things they can ship; and tear everything down.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest; not yet fact-checked at the time of
this draft), `SLIDES.md` (the lecture, binding next to the digest, docs/AC215_SERIES.md rule 9), `assets/` (see
`ASSETS.md`). Where the digest and the captures disagree, the captures win (BRIEF.md's table); where the slides and
the tutorial disagree, the scene shows the notebook's or the library's version and the SAY says so kindly, in one
sentence (BRIEF.md "Conflicts" 1–8). Nothing in a terminal panel or recorded-output box is typed by hand: every
output line below names its file and line numbers.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at most about 60
  words; the recap list may run a little longer) and become the subtitles. Plain spoken English: no backticks, no
  symbols; commands, flags and paths are on screen and said in words ("python cli.py dash dash generate", "the
  secrets folder", "slash app"). File names such as cli.py, env.dev, docker-shell.sh, instruct-dataset.csv,
  train.jsonl and llm-service-account.json are said as words. Numbers as digits ("19 by 2", "1,146,880"); money in
  words ("112 dollars 73"); never a "!" after a digit. Versions that will change are said with "at the time of
  recording". The date is said in American order ("October 31, 2026"). The model names are said "Gemini 3.1 Flash
  Lite", "Qwen3 0.6B", "OPT 350m".
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences` splits only there;
  the split drives the TTS gaps, the subtitle cues and the one-to-one Chinese alignment). No sentence opens with a
  command or a lower-case file name. No `'s` after a digit or on a word with a lexicon entry unless the lexicon has
  the `'s` form (`README's` does). Spelling American on screen and in the SAY ("gray"; the colour constants stay GREY).
- Names. The persona is the instructor's first name. The SAY says "the instructor" or "the instructor's voice" and
  never a name. On screen every occurrence is the GRAY chip `‹instructor›`: `scenes/common.py`'s `unname(text)` masks
  the name case-insensitively in every panel line read from an unmasked file (`gemini-finetuner/03` line 4, the
  query; `cli.redacted.py:56` and `:109`; `dataset-creator/cli.py:84`, `:90`, `:96`; `README.md` lines; `cell-50.md`).
  `expected/` files are already masked. The full name never appears: `README.md:118-119`, `:167` and
  `dataset-creator/cli.py:133`, `:140` are never quoted. The Hugging Face account is `‹hf-user›` (already masked in
  `c88`). The endpoint at `gemini-finetuner/cli.py:107` is only ever the redacted
  `projects/‹instructor-project-number›/locations/us/endpoints/‹endpoint-id›`. The key is a GOLD key glyph, never a
  value.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, a silent ponder timer of n seconds (`pause_and_ponder`); the card
  sits in the lower third, a 3-row terminal strip fades while it is up, and the picture during the timer never shows
  the answer. The card is removed at the start of the next block, whose SAY gives the answer. Five in the video
  (S05, S08, S10, S12, S13; BRIEF.md "Ponder questions").
- `Lecture: 7–8.` under a scene header lists the slides the scene stands on; `Lecture: none.` means the tag never
  appears. `LECTURE 7–8` in a SHOW line: from that SAY block on, the GRAY `lecture_ref(8, "7–8")` tag
  (`explainer.devops`) sits top right ("Lecture 8 · slides 7–8"), until a SHOW changes it or says it leaves. S01
  explains the tag once. The slides are never shown: every lecture picture is our own redrawing in the series colours,
  with the slide's structure and terms; no slide image, meme, pizza cartoon, screenshot (5, 7, 40) or the GPT-4 cost
  aside (11–12). Slide slips are never copied (slide 50's 18 and 69 are drawn as 19 and 70; slide 44 is rounded, not
  floored; slide 38's "100 GB" is drawn as slide 14's 20 + 80).
- `TERM(folder/file: lines)`: a terminal beat. The scene types the command written just before it in the SHOW line
  (in backticks, exactly as the README spells it; extras exactly as captured), then prints those lines of
  `assets/terminal/folder/file`. Line 1 of every capture is its `$ …` command and is never printed; the `[exit N]`
  line is never printed (where the exit status matters, a GRAY caption says it, e.g. "exit status 0"). In the line
  list: `…` = print one GRAY `…` line; `wrap` = fold long lines (`Terminal.print(..., wrap=True)`); without `wrap`, a
  line longer than a row is cut with `…`; `N cut after "x"` = print line N only up to and including x, then ` …`;
  `→ (no output)`: the prompt simply returns. `names+sizes` = print only the size and name columns of those `ls -la`
  lines, joined by two spaces (a column cut, never new text): the capture laptop's `rw-rw-rw-` / `drwxrwxrwx` modes
  are capture artefacts and never appear. BuildKit lines (`laptop/07`, `laptop/18`) are padded with runs of spaces
  before the timing: collapse each run to two spaces (whitespace only).
- `cd` commands with no output (`cd llm-finetuning`, `cd ..`, `cd llm-finetuning/dataset-creator`) have no capture
  file because they print nothing: the scene types them and the prompt changes (`→ (no output)`). They are the
  README's "make sure you are inside the … folder" (README.md:83, :236) or extras where marked.
- Terminal width. Every terminal is the house `term()` (12.6 wide, 22 pt, 65 characters a row), always full width,
  at most 13 rows. A typed command is never cut: it folds at a space onto an indented second row ending in ` \`
  (`Terminal.type`). When a picture needs the frame, the terminal shrinks to a 3-row strip along the bottom edge (the
  last command and its key output line); never half width; a second panel goes above the strip, never beside a
  full-width terminal.
- Terminal titles and prompts. Laptop: title `laptop`, prompt `student@laptop:~/AC215$`, then
  `student@laptop:~/AC215/llm-finetuning$` and `student@laptop:~/AC215/llm-finetuning/dataset-creator$` (S03 says once
  that their prompt shows their own user and machine). Second laptop terminal (S04, S06, S07 extras): title `laptop ·
  second terminal`, prompt `student@laptop:~/AC215/llm-finetuning/dataset-creator$`. The containers: the frame turns
  TEAL, title `container · llm-dataset-creator`, prompt `app@6f5113cdb660:/app$` (`laptop/07` line 27), and title
  `container · gemini-finetuner`, prompt `app@2a2550dec953:/app$` (`laptop/18` line 27); S04 says once that the part
  after `app@` is the container id (GRAY tag `your id will differ`). `dataset-creator/` and `gemini-finetuner/`
  captures ran at those prompts: draw the prompt and type the `$` command after it. `laptop/07` and `laptop/18` line 27
  is the container prompt with `exit` typed after it: S04 and S08 stop at the prompt (cut before ` exit`); S08 and S16
  type `exit` and print line 28.
- Extra cards. Extras whose command is long plumbing are never typed: `laptop/02` (git log), `dataset-creator/00`
  (whoami …), `laptop/16` (the three diffs) appear as a GRAY *extra card*: the tag `extra`, "an extra check · in the
  study guide" and the one-line purpose the SHOW gives in quotes; then their output prints from the listed lines.
  Every other extra is typed as captured.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b, header `path · lines a–b`;
  never more than 12 rows on screen; a longer range is shown in windows of ≤ 12 lines that Transform into each other,
  or *folded* (only the listed lines, a GRAY `…` row between gaps, header suffix `(folded)`). Lines longer than 65
  characters wrap (continuation rows indented, a GRAY ↪). An *excerpt chip* quotes an exact sub-string of one line,
  headed `path · line N (excerpt)`. `gemini-finetuner/cli.redacted.py` is labelled `gemini-finetuner/cli.py` (same
  line numbers, line 107 redacted). Every line goes through `unname()`.
- Colab. Part 2 scenes draw a BLUE rounded frame (the Colab VM is Google's cloud) titled "QLoRA notebook · Colab", tag
  `illustration`; menus, the runtime dialog and the Secrets panel are schematic (no logos, no screenshots). Notebook
  code: `CODE(colab/cell-NN.py: a–b)`, header `QLoRA notebook · <section> · cell NN · lines a–b`: the section is the notebook's own heading number (`3`,
  `1.3`, `4.2` …), which the viewer can find in Colab (Colab shows no cell numbers); NN = the cell's 0-based index, as
  in `assets/source/colab/`, for authors. Source chips follow the same form ("QLoRA notebook · 5.2 · cell 82"). The
  SAY names notebook places by the notebook's numbers ("section 3", "2.2", "step 4"), never by our cell indices.
- `RECORDED(expected/colab-cNN-…: lines)`: the staff's saved Colab outputs (an A100 run), printed in an output box
  (never a terminal frame) with the tag `recorded · the staff's saved Colab run (A100)`. Line 1 of each `expected/`
  file is a `#` source header and is never printed; the `$ …` lines that follow are the cell's code, never printed as
  output. Same `…`, `wrap` and `cut after` rules as TERM. Emoji in `c80` and `c82` (`📊 📝 🔵 🟢 ✅ ✓`) are stripped
  (`strip_emoji=True`, L06 helper); `🔵 Base Model:` lines print GRAY, `🟢 Fine-Tuned Model:` lines GREEN-outlined.
- `QUOTE(expected/readme-…: lines)`: README text about what a working run prints, as a GRAY quote card headed with
  its README lines (from the file's `#` header, e.g. `README.md · lines 295–301`), tag `expected`, never styled as a
  live terminal.
- Trackers. `TRACKER DsRun 2` = the `ReadmeTracker` (via the `common.py` factory), top left in every walkthrough
  scene, moves to that section and step; `TRACKER DsRun 2 · extra`: same step, the caption gets " · extra" while a
  command the README doesn't have is on screen. Caption "<head> › section › step k of N"; head "README", or "Colab"
  for the course notebook. Step titles ≤ 3 words (BRIEF.md "README step tracker"):
  - `Prereq` = Prerequisites (`README.md:31-69`), 4: 1 Clone repo (extra) · 2 Service account · 3 Secrets folder ·
    4 Edit env.dev (extra).
  - `DsRun` = Dataset › Run Container (`:79-94`), 4: 1 Go to folder · 2 Run script · 3 Check key · 4 Test CLI.
  - `DsGen` = Dataset › Generate Text (`:98-155`), 4: 1 Generate · 2 System prompt · 3 Input prompt · 4 Iterations.
  - `DsSamples` = Dataset › Samples (`:159-175`), 1: 1 Sample answers.
  - `DsPrep` = Dataset › Prepare (`:179-212`), 2: 1 Prepare data · 2 Gemini format.
  - `DsUp` = Dataset › Upload (`:216-222`), 1: 1 Upload data.
  - `FtRun` = Fine-tune › Run Container (`:232-247`), 3: 1 Go to folder · 2 Run script · 3 Test CLI. Edit URIs
    (`cli.py:10-11`) is `TRACKER FtRun 1 · extra`, between steps 1 and 2.
  - `FtModel` = Fine-tune › Fine-tune Model (`:251-261`), 2: 1 Start tuning · 2 Watch console.
  - `FtCost` = Fine-tune › Cost (`:265-278`), 1: 1 Read costs.
  - `FtChat` = Fine-tune › Chat (`:282-316`), 4: 1 Paste endpoint (extra) · 2 Chat · 3 Hosted demo · 4 Training
    monitor.
  - `ColabA` = Colab › Part A · Setup (cells 1–16), 6: 1 Copy notebook · 2 GPU runtime · 3 §3 Install · 4 §4 HF
    token · 5 §5 Imports, Drive · 6 §6 Download. (Steps 3–6 are the notebook's sections 3–6; steps 1–2 are the
    copy and runtime instructions above them, said "first" and "then", never "step 1/2", which would collide with
    the notebook's "1. Intro", "2. Learning Objectives".)
  - `ColabB` = Colab › Part B · 4-bit (cells 17–28), 3: 1 Load OPT · 2 §1 Verify · 3 §2 Generate.
  - `Qwen` = Colab › Step 1–2 · Qwen (cells 31–48), 5: 1 1.3 Load · 2 2.1 Params · 3 2.2 Config · 4 2.3 Baseline ·
    5 2.4 Trainable.
  - `Data` = Colab › Step 3 · Dataset (cells 50–64), 5: 1 3.1 Download · 2 3.2 Sample · 3 3.5 Template · 4 3.6 Split ·
    5 3.7 Verify.
  - `Tune` = Colab › Step 4 · Fine-tune (cells 65–77), 5: 1 4.1 LoRA config · 2 4.2 Train args · 3 4.3 Trainer ·
    4 4.4 Train · 5 4.5 TensorBoard.
  - `Eval` = Colab › Step 5 · Evaluate (cells 78–82), 2: 1 5.1 Loss table · 2 5.2 Side by side.
  - `Save` = Colab › Step 6 · Save (cells 83–88), 3: 1 6.1 Adapters · 2 6.2 Merge · 3 6.3 Push.
  - `Down` = Teardown · extra, 4: 1 Exit · 2 Remove images · 3 Cloud cleanup · 4 Colab runtime (every step `extra`).
  The SAY's "step k" is the tracker's step within the section on screen. Ordering (said in a clause where it
  happens; BRIEF.md "Ordering notes"): the clone is extra (S03); `ls -la /secrets` is the README's Prerequisites tip
  but runs inside the container, right after the banner (S04, as DsRun 3); enabling the API and creating a bucket are
  said on a card, not typed (S03); `--generate` is typed at DsGen 1 in README order and the README's explanations
  (system prompt, input prompt, iterations) follow it as steps 2–4 (S05); `--prepare` runs twice, right after the
  failed `--generate` and then on the scripted data, and the tracker counts the second (S06); the notebook's order is
  quantization before LoRA, said in S11; the LoRA count is derived in S13 and confirmed by the trainer cell at Tune 3
  in S14 (notebook order: config → arguments → trainer).
- `(extra)` after a command: not in the README or the notebook. A small GRAY tag `extra` sits beside the typed line,
  and the SAY says so ("an extra", "not in the README") the first time in each scene.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint; the SAY of that block says "pause". When the
  checkpoint's commands have scrolled away or a picture replaced them, the `▶` sits on a static GRAY "your turn" card
  listing them exactly as typed. Every `▶` beat holds its frame for 2 s of silence after its SAY (`self.wait(2)`)
  before anything moves. The scene's GOLD cost goes in as the card's last line where something is billed ("free" in
  GREEN when nothing is).
- Tags (GRAY unless stated): `extra`; `illustration` on every schematic (console forms, the job page, the training
  monitor, Colab menus, the probability bars in S15, the dry-cleaner ticket); `recorded · the staff's saved Colab run
  (A100)` on notebook outputs (never presented as a T4 measurement); `expected` on README text about working output;
  `scripted` on the hand-written stand-in data and everything printed from it (its seat drawn BLUE dashed: real
  program output on hand-written data, never "Gemini's output"); `no key` on every terminal that runs a command
  reaching Google (`--generate`, `--upload`, `--train`, `--chat`); GOLD `billed` on those four commands; `estimate` on
  our own 0.6 B memory figures (S14); `at the time of recording` next to versions; `erratum` on every tutorial slip
  (the SAY says "a small slip" where it helps, always with the fix); `your id will differ` on container ids;
  `concept · lecture only` (GRAY dashed) on lecture-only scale (the 10 B model, the 24 GB tiles). No scene number
  ever appears on screen: forward references say "part 2", "the training chapter", "teardown".
- Semantic colours (BRIEF.md "Colours", series table applied):

  | meaning | colour |
  | --- | --- |
  | your laptop: `~/AC215`, the clone, `secrets/`, `dataset-creator/data/` seen from the host, the laptop terminal, the browser tab | GREY |
  | the cloud: Google Cloud and its three locations (`global` generation, `us-central1` tuning, multi-region `us` serving), the bucket, the tuning job, the endpoint; the Colab VM and its GPU; **everything a model writes** (the teacher's Q&A pairs, generated answers). The hand-written stand-ins sit in the same seat, BLUE **dashed**, tag `scripted` | BLUE |
  | the containers and images `llm-dataset-creator` and `gemini-finetuner`: `/app`, `/.venv`, the build | TEAL |
  | the base image's own Python and apt packages (`python:3.12-slim-bookworm`; only S04) | ORANGE |
  | what you own: `uv.lock` and pinned versions; **your dataset files** (`instruct-dataset.csv`, `train.jsonl`, `test.jsonl`); **the LoRA adapters A and B** (the 4.6 MB you train, save and keep) | GREEN |
  | tools and libraries you install: Docker, uv, the google-genai SDK, bitsandbytes, peft, trl, transformers | PURPLE |
  | errors and "avoid this": the missing-key errors, `KeyError`, `source: not found`, quantization error, out-of-memory, the ✗ on a wrong physics claim | RED |
  | your turn, the trackers, "look here now"; the gradient pulse in the backward pass | YELLOW |
  | money: generation calls, the tuning bill, the cost table, Colab compute units; the service-account key glyph (never a value) | GOLD |
  | routes and lookups: bind mounts, `gs://` URIs, the three hosts, the endpoint path, GPU ↔ CPU paging arrows | PINK |
  | frozen pretrained weights **W₀** (solid, with a snowflake; in part 2 GREY means "not yours to change"); lecture-only scale and future lectures (L10) GREY dashed; the persona chip `‹instructor›` | GREY |

  dtype tags (`NF4`, `FP16`, `FP32`, `BF16`) are small neutral white labels on whatever they describe; the deck's blue
  W₀ and orange adapters are not copied. Bit strips (S14) outline sign / exponent / fraction in WHITE / PINK / GREEN
  (range / precision), not the semantic colours. Something merely absent (the empty `secrets/`, an output nobody
  documented) is GREY dashed, not RED.
- Visual set pieces V1–V8 are specified in BRIEF.md ("Visual set pieces"); SHOW lines say which one, its state and
  what moves. Reused objects: **the stage** (V2: GREY laptop left, two TEAL containers middle, BLUE cloud with three
  pins right; S03, S04, S07–S09), **the conveyor** (V4: S06, S07, S12), **the memory column** (V5: S10, S14, S16),
  **the LoRA block** (V7: S13, S14, S16).
- Running example: user `student`, host `laptop`, workspace `~/AC215`; containers `app@6f5113cdb660:/app$` and
  `app@2a2550dec953:/app$`. The scripted data: `capture-only/scripted/cheese_qa_{0..4}.txt`, five files of four pairs,
  hand-written in the shape `--generate` writes, openers from the current prompt, the last pair repeating the first
  question on purpose; always tagged `scripted`, said to be 20 pairs where Gemini would write about 100. The Colab:
  Qwen/Qwen3-0.6B, 900 train / 100 test examples sampled from the 16k file, r = 8, α = 16, 2 epochs, 450 steps;
  stored outputs from an A100 ("the course staff's saved run, on an A100").
- Length and parts: narration 4,294 words (`python -m explainer.script`, v2; BRIEF.md: 3,900–4,300, plan ~4,070;
  every scene inside its budget ±15 %; part 1 2,357, part 2 1,937). At the measured 144–151 wpm of af_heart at 0.9
  (L04–L07) that is ≈ 28–29.5 min of voice; typing, outputs, five 8-s ponders and the `▶` holds bring it to ≈ 33–34 min.
  Any later change must trim, not add. Part 1 = S01–S09 (Track A: a persona dataset and a
  managed tuning job), part 2 = S10–S16 (Track B: QLoRA in Colab). Part 1 ends on S09's empty frame after "In part 2,
  the weights are in your hands."; part 2 opens on the Colab frame. Each part ends on an empty frame.

  | scene | S01 | S02 | S03 | S04 | S05 | S06 | S07 | S08 | S09 | S10 | S11 | S12 | S13 | S14 | S15 | S16 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | budget | 240 | 220 | 250 | 260 | 270 | 250 | 230 | 280 | 220 | 250 | 290 | 250 | 290 | 270 | 250 | 250 |
  | words | 255 | 204 | 265 | 279 | 307 | 247 | 252 | 312 | 236 | 233 | 316 | 238 | 316 | 303 | 253 | 278 |

- Notes for scene authors.
  - `Capture.pick()` indexes the output body: pick index = file line − 1. `expected/*.txt` line 1 is a `#` source
    header; `colab-*` files then carry the cell's code as `$ …` / two-space-indented lines before the output.
  - `laptop/09` line 4 (the capture's rebuilt `python:3.12-slim-bookworm`) is never printed; print lines 2–3 only.
    Never present 45.1 s as typical. Never print `laptop/07.plain.txt` or `18.plain.txt` (proxy and CA lines).
  - `gemini-finetuner/02` line 4 and `03` lines are long: line 4 wraps (2 rows). `03` line 4 goes through `unname()`.
  - `dataset-creator/09` lines 12–17 are pandas' head table, 100+ characters wide: print each cut at 65 characters
    (the question column and the first words of the answer), GRAY `…` at the cut.
  - `c63` line 3 is one long `Column([...])` repr: S12 draws it as the ribbon (V4 station 4) from its own text: the
    markers `<|im_start|>user`, the question, `<|im_end|>`, `<|im_start|>assistant`, `<think>\n\n</think>`, the
    answer's first words (masked), with `\n` shown as GRAY ↵ glyphs; nothing added.
  - V5 numbers: 10 B model: 20 / 20 / 80 GB (slide 14), tiles of 24 GB; LoRA ≈ 40, QLoRA ≈ 12 (slides 39, 72). Qwen3
    0.6 B (tag `estimate`, our arithmetic): full ≈ 7 GB (596 M × (2 + 2 + 8) bytes); QLoRA ≈ 0.9 GB (0.22 GB packed
    4-bit linears + 0.62 GB fp32 embeddings + ≈ 18 MB adapters with their gradients and Adam states).
  - V6 numbers: slide 44 dots 27, 55.3, 83.78 → 27, 55, 84 (whole numbers) and 30, 60, 80 (tens); slides 45–51:
    X = 1.5, 2.3, 3.7, 4.1, 5.6, 6.8, 7.9, 8.4, 9.2, 10.2; c = 127 / 10.2 = 12.4509; Int8 = 19, 29, 46, 51, 70, 85, 98,
    105, 115, 127; 19 / 12.4509 = 1.526, 70 / 12.4509 = 5.622. Blocks of 64 weights (bitsandbytes' NF4 block size).
  - V7 numbers: `q_proj` 2048 × 1024 = 2,097,152 vs A 8 × 1024 + B 2048 × 8 = 24,576; `v_proj` 1024 × 1024, LoRA
    16,384; per block 40,960; × 28 = 1,146,880 (`c42`: hidden 1,024, 16 heads of 128, 8 key-value heads, 28 layers).
    PONDER 5: r = 16 → 2,293,760; all seven projections at r = 8 → 8 × 22,528 × 28 = 5,046,272.
  - Lexicon (added at the review merge, block `# AC215 L08` in `explainer/lexicon.yaml`): LoRA, QLoRA, Qwen, Qwen's,
    Qwen3, us-central1, JSONL, Teardown, env.dev, instruct-dataset.csv, train.jsonl, llm-service-account.json, torchao,
    absmax, dequantization, reparameterization, "dash la", "im start", "im end", the matrix-A phrases ("B and A", "B
    times A", "A at random", "draws A"), "a reparameterization", "a Colab GPU", and every decimal the SAY speaks
    (the phonemizer otherwise reads "375.8" as a sentence end); decimals or words a finished video also says are
    L08-only phrases ("pyproject and lockfile", "from 1.5", "1.5 becomes", "5.6 becomes", "from 2.0", "a dropout of
    0.1", "torch 2.11"). Checked, no entry: NF4, BF16, FP16, PEFT, bitsandbytes, trl, A100, T4, OPT, Yello, monker,
    US (the location), Colab (has one), Gemini, README's, Dockerfile, lockfile, docker ps. 44ef6f0 is never said.
    Any new SAY text: no `'s` on Qwen3, no decimal without an entry, no article "a" right before a lexicon word.
  - i18n `en_display` candidates (spoken → literal): python cli.py dash dash generate / prepare / upload / train /
    chat / help → `python cli.py --generate` …; sh docker-shell.sh; bash docker-shell.sh; ls dash la slash secrets →
    `ls -la /secrets`; slash app → `/app`; slash secrets → `/secrets`; slash dot venv → `/.venv`; dash dash rm →
    `--rm`; docker ps dash a → `docker ps -a`; docker image rm; key error, question → `KeyError: 'question'`; tuned
    model info, none → `Tuned model info: None`; wait for job set to false → `wait_for_job=False`; disable adapter →
    `disable_adapter()`; prepare model for k-bit training → `prepare_model_for_kbit_training`; drop duplicates →
    `drop_duplicates`; train test split → `train_test_split`; Linear4bit; NUM_ITERATIONS; target modules →
    `target_modules`; im start / im end → `<|im_start|>` / `<|im_end|>`; W naught → W₀; alpha over r → α/r;
    MLOps Learning → `MLOps_Learning`; money: 112 dollars 73 → $112.73, 0.008 dollars → $0.008.

---

## S01 · Why is the sky blue? — `s01_hook.py` · `Hook`

Lecture: 7–8.

SHOW: Cold open, no tracker. Black frame. A YELLOW-outlined question card writes in top center: "Why is the sky
blue?" Below it two empty answer-card outlines slide in side by side: left GRAY "Qwen3-0.6B · as downloaded", right
"Qwen3-0.6B · fine-tuned" with a small GREEN adapter glyph on its corner; tag `recorded · the staff's saved Colab run
(A100)` under both. A GRAY source chip "QLoRA notebook · 5.2 · cell 82".
SAY: Why is the sky blue? We asked two versions of the same small language model. Both answers come from the course staff's saved Colab run.

SHOW: The cards fill. Left: RECORDED(expected/colab-c82-base-vs-finetuned.txt: 155 cut after "atmosphere.", 156 cut
after "(refracts)") (wrap, 4 rows). Right: RECORDED(expected/colab-c82-base-vs-finetuned.txt: 159 cut after "sky's
blue!") then a GRAY `…` and the exact sub-string "The blue color of the sky is due to the scattering of light by the
water molecules in the atmosphere." (wrap, 5 rows). On "cheesy greeting" the opener "Yello - this is ‹instructor›
your cheese monker" lights YELLOW; the `‹instructor›` chip is GRAY.
SAY: The original answers like a textbook. The fine-tuned one opens with a cheesy greeting in the instructor's voice, and then explains.

SHOW: A RED ✗ lands on "**Light Refraction**" in the left card, a second RED ✗ on "water molecules" in the right card;
a GREEN tick lands on the right card's opener, caption "voice: learned". Below both, a GRAY chip "the real reason:
air molecules scatter blue light more than red (Rayleigh scattering)".
SAY: Now check the physics. One blames refraction, the other water molecules. Both are wrong: air molecules scatter blue light more than red. The voice changed completely; the facts did not get better.

SHOW: LECTURE 7–8. The cards shrink to the top. Center: a GRAY redrawn chat bubble (our drawing, no screenshot) whose
first line "Sure, here's…" lights YELLOW, caption "a habit a chat model learned". On "This one" the bubble fades (it
returns in the next chapter) and the numbers write in ONE row (one visual group) as the SAY names them: a GREY
snowflake slab "596 M weights · frozen" with, beside it, a hair-thin GREEN strip "≈ 1.15 M new · trained" (the
contrast in widths is the point); then two small chips: BLUE "3 min 36 s · A100" and GREEN file glyph "≈ 4.6 MB"
(source chip "QLoRA notebook · 6.1"). The recorded lines (`c72` line 23, `c75` line 5) are not printed here; S14
shows them.
SAY: Chat models learn their habits the same way; the lecture shows one that starts with the words, sure, here's. This one kept 596 million weights frozen and trained 1.15 million new ones. It took about 3 and a half minutes on an A100, and fits in a file of about 4.6 megabytes.

SHOW: The chips fade. A YELLOW question writes across the middle (no timer): "What did it learn — and what didn't
it?" It moves up; the map builds in two columns. Left, "Track A · the README": GREY laptop → TEAL container → BLUE
cloud, labels "Gemini writes a persona dataset", "Google tunes Gemini", "you get an endpoint". Right, "Track B · the
course Colab": a BLUE GPU box with a GREEN adapter, labels "you fine-tune an open model with QLoRA", "you keep the
weights".
SAY: So what did it learn, and what didn't it? Two tracks answer that. In track A, the README, Gemini writes a persona dataset and Google tunes Gemini for you. In track B, the course Colab, you fine-tune an open model yourself and keep the weights.

SHOW: The map clears. A layout preview builds piece by piece as named: the ReadmeTracker top left ("README ›
Prerequisites", 4 dots, none lit) with a YELLOW circle pulsing around it; a GRAY specimen lecture tag "Lecture 8 ·
slides N" top right pulses once; a 2-row terminal strip (GRAY tag "preview") with a YELLOW `▶ your turn` tag, drawn
dim. Under it, the tag row, each tag writing in as a small chip: `expected`, `recorded`, `scripted`, `illustration`.
SAY: The tracker, top left, shows the step; the gray tag, top right, shows the lecture slides. When a tag says your turn, pause and run the command.

SHOW: The preview clears. An honest-limit card; its rows write in as the SAY reaches them: GREEN "ran for real:
every README command, exactly as written"; RED "commands that talk to Google: up to the missing key (kept, they are
instructive)"; BLUE "working outputs: `expected` = the README · `recorded` = the staff's saved Colab run";
BLUE dashed "`scripted` = a small hand-written dataset"; a GRAY chip "recorded October 31, 2026 · no key · no GPU";
a GRAY persona chip `‹instructor›` with "the persona: the instructor's voice". Footer: "every command: MLOps_Learning ·
guides/L08-llm-finetuning.md". Everything fades to an empty frame.
SAY: One honest limit: we recorded this on October 31, 2026, with no service account key and no GPU. Every README command ran exactly as written; the ones that talk to Google stop at the missing key, and we keep those real errors. Working outputs come from the README and the saved Colab run.

---

## S02 · Three dials: prompt, context, weights — `s02_dials.py` · `ThreeDials`

Lecture: 4–8.

SHOW: V1. A model box center (a grid of small numbers inside, BLUE outline) with three dials on its front, labelled
"prompt", "context", "weights". An input arrow enters from the left, an output arrow leaves right. On "prompt", the
first dial turns: a GRAY system-prompt card slides onto the input arrow; the box does not change. On "retrieval", the
second dial turns: three PINK chunk cards (L05's retrieved chunks, chip "L05 · RAG") stack onto the input arrow; the box
still does not change. On "untouched", both input cards flash and the box's grid stays still.
SAY: There are three ways to change what a model says. A prompt changes the input every time you ask. Retrieval, the RAG app from lecture 5, adds looked-up text to the input. Both leave the model itself untouched.

SHOW: LECTURE 4–6. The third dial turns: the box's grid of numbers shimmers and changes, the box itself morphs. Into it
flows a stack of small cards, each "(input, desired output)". A GRAY lecture term chip "instruction fine-tuning"
writes beside the stack (slide 4), then "task-specific fine-tuning" under it, with the persona chip `‹instructor›` (slide
6).
SAY: Fine-tuning turns the third dial: it changes the weights, by showing the model many examples of an input and the output you want. In this course that usually means instruction fine-tuning: pairs of an instruction and its answer. A persona is a task-specific fine-tune.

SHOW: LECTURE 7–8. The stage splits in three rows (slide 8's contrast, our drawing). Row 1, a GRAY box "OPT-350m ·
plain next-word predictor": input "Hello my cheese name is" → RECORDED(expected/colab-c27-opt-generate.txt: 11–12)
in its output bubble, tag `recorded`. Row 2 an outline "instruction-tuned model" with S01's redrawn GRAY chat bubble
"Sure, here's…" (our drawing, caption "a habit a chat model learned"). Row 3 "fine-tuned Qwen" with a bubble opening `Yello - this is ‹instructor›…` (from `c82` line
159, the same excerpt as S01).
SAY: Compare a model that was never instruction-tuned. The notebook gives OPT 350m the words, hello, my cheese name is. It simply keeps going: my cheese name is cheese, I'm not sure if you're joking or not.

SHOW: Row 2 lights: its bubble answers. Row 3 lights: its bubble answers in the persona's voice; the RED ✗ from S01
("water molecules") returns small on row 3's content. A YELLOW banner writes under the rows: "style is learnable ·
facts are not guaranteed" with a GRAY caption "what the saved run shows".
SAY: An instruction-tuned model answers instead of continuing, often with a habit like, sure, here's. Our fine-tuned Qwen answers the way the instructor would. That's the lesson of the saved run: style is learnable; facts are not guaranteed.

SHOW: The rows clear. Two pictures side by side: left, a GRAY desk with an open book of PINK chunks ("RAG: the open
book on the desk"); right, the model's voice box with its dial on "weights" ("fine-tuning: the default voice"). Then
both shrink, and S01's two-track map fades back in small at the bottom (the same object, not a rebuild); only two
captions update as named: Track A gains a GRAY crossed-out eye "you never see a weight", Track B a save glyph "yours
to keep". Everything fades to an empty frame.
SAY: A useful mental model: fine-tuning moves the model's default voice; RAG changes the open book on its desk. In track A, Google trains the model and you never see a weight. In track B, you train a small adapter on a Colab GPU, and it is yours to save.

---

## S03 · A key next to the repo — `s03_setup.py` · `KeyNextToRepo`

Lecture: none.

SHOW: TRACKER Prereq 1 · extra. A full-width terminal, title `laptop`, prompt `student@laptop:~/AC215$`. It types
`git clone https://github.com/dlops-io/llm-finetuning.git` (extra) → TERM(laptop/01-x-clone.txt: 2). A GRAY chip
"README.md · line 34 only links the repository". GRAY caption "your prompt shows your own user and machine". Before
the clone, an extra card "is Docker running" (README.md:33 "Have Docker installed") → TERM(laptop/00-x-env.txt: 4)
with the tag `at the time of recording`.
SAY: Start in your workspace, the AC215 folder, with Docker installed and running. The README only links the repository, so cloning it is an extra step. Your prompt shows your own user name and machine.

SHOW: It types `cd llm-finetuning` (extra) → (no output). An extra card "which commit am I on" →
TERM(laptop/02-x-git-log.txt: 2 cut after "44ef6f0", 3) with a GRAY tag "or newer". Then it types
`ls -a; ls -a dataset-creator gemini-finetuner` (extra) → TERM(laptop/03-x-ls.txt: 6–11, 12, 15–20 folded to
"Dockerfile  cli.py  docker-entrypoint.sh  docker-shell.sh  pyproject.toml  uv.lock", 22, 25–30 folded the same
way) (10 rows). Line 7 `autotrain-runner` prints dim GRAY with a GRAY tag "not part of the README".
SAY: Recorded at the commit on screen; yours may be newer. Inside are two folders, dataset-creator and gemini-finetuner, each with the same six files. The autotrain folder is not part of the README, so leave it alone.

SHOW: TRACKER Prereq 2. The terminal shrinks to a 3-row strip. Above it, a schematic console form (tag
`illustration`, no logos): "Create service account", name field `llm-service-account`; a roles box where two chips drop
in: "Storage Admin" and "Agent Platform User" with a GRAY sub-label "formerly Vertex AI User · roles/aiplatform.user";
then a "KEYS" tab and a button "ADD KEY › Create new key › JSON"; a GOLD key glyph drops out of the form into a GRAY
"Downloads" folder. A GRAY chip "the same account as L05: reuse it" fades in last.
SAY: Step 2 happens in the cloud console. Create a service account called llm-service-account with two roles: Storage Admin, and Agent Platform User, formerly Vertex AI User. Under keys, add a JSON key, which downloads to your laptop. If you kept the account from lecture 5, reuse it.

SHOW: TRACKER Prereq 3. The form fades; the strip grows back to a full terminal. It types `cd ..` (extra) → (no
output), prompt `student@laptop:~/AC215$`; types `mkdir secrets` (`README.md:50`) → TERM(laptop/05-x-mkdir-secrets.txt)
→ (no output); types `ls -la; ls -la secrets` (extra) → TERM(laptop/06-x-ls-workspace.txt: 2, 5–6, 7–8) (folder
names `llm-finetuning` and `secrets` lit GREY). A GRAY chip "move the key in · name it exactly llm-service-account.json";
a RED erratum-style warning chip "not llm-service-account.json.json (hidden extensions · README.md:67)". Under
`secrets`, a GREY dashed key outline "ours: empty".
SAY: Step 3: make a folder called secrets next to the repository, not inside it. Move the key in and name it exactly llm-service-account.json; with hidden file extensions it can end up as dot json dot json. Ours stays empty on purpose. Watch what that does.

SHOW: V2 begins: the terminal shrinks to a strip; the GREY laptop box `~/AC215` draws on the left with two folder
glyphs side by side, `llm-finetuning/` and `secrets/` (GREY dashed key outline inside), as in `README.md:54-62`. A
RED "git" arrow from the clone tries to reach `secrets/` and bounces off the clone's edge ("never committed"). An
excerpt chip `env.dev · line 5 (excerpt)`: `SECRETS_DIR=$(pwd)/../../secrets/`; a PINK path walks from
`dataset-creator/` up two folders to `~/AC215/secrets/`, then the same from `gemini-finetuner/`.
SAY: Why next to the repository? A key outside the clone can never be committed by accident. The env.dev file looks two folders up from wherever the script runs, so both container folders reach the same key.

SHOW: TRACKER Prereq 4 · extra. CODE(env.dev: 4–10) above the strip (7 lines); lines 6 and 7 light YELLOW, their
values `"ac215-project"` and `"cheese-dataset"` get GRAY tags "the README's defaults · change to yours". Line 9 gets
a GRAY tag "its comment says change too · not passed to either container · optional". An extra tag
on the panel header ("implied by its comments"). The strip shows TERM(laptop/04-x-env-dev.txt) typed as `cat env.dev`
(extra), its last line visible.
SAY: An extra step 4, implied by the file's own comments: in env.dev, set your own project ID and bucket name on lines 6 and 7. The scripts pass both into the containers.

SHOW: The panel fades. A GREY dashed card "not in the README, needed" with two lines (shown, never typed, no terminal):
`gcloud services enable aiplatform.googleapis.com storage.googleapis.com` and `gcloud storage buckets create
gs://<your-bucket> --location=us-central1`; `<your-bucket>` is a YELLOW template chip; GRAY caption "bucket names are
global · cheese-dataset is the course's". Then the GRAY "your turn" card with a YELLOW `▶ your turn` tag lists:
`git clone https://github.com/dlops-io/llm-finetuning.git` (extra) · service account + JSON key · `mkdir secrets` ·
`mv ~/Downloads/<downloaded-key>.json secrets/llm-service-account.json` (a template line, YELLOW template chips, shown,
never run) · env.dev lines 6–7 · API + bucket; last line GOLD "a bucket: storage
billing, cents". 2 s hold. Everything fades to an empty frame.
SAY: The README also assumes the Agent Platform and Storage APIs are enabled, and a bucket of your own. Bucket names are global, and cheese-dataset belongs to the course. Pause here and finish all four steps.

---

## S04 · The dataset-creator container — `s04_container.py` · `DatasetContainer`

Lecture: none.

SHOW: TRACKER DsRun 1. Full-width terminal `laptop`, prompt `student@laptop:~/AC215$`. It types
`cd llm-finetuning/dataset-creator` → (no output); the prompt becomes `student@laptop:~/AC215/llm-finetuning/dataset-creator$`.
TRACKER DsRun 2: it types `sh docker-shell.sh` with a YELLOW `▶ your turn` tag →
TERM(laptop/07-docker-shell-dataset-creator.txt: 3, 9, 12, 15–16, …, 20) (BuildKit spaces collapsed); `45.1s` on
line 3 gets a GRAY tag "fast network · expect a few minutes". A small GRAY chip under the typed line: "`source: not
found`? → `bash docker-shell.sh` (shown in a minute)".
SAY: Step 1 of the dataset section: go into the dataset-creator folder. Step 2: sh docker-shell.sh. The first build installs everything. Here it took 45 seconds on a fast connection; expect a few minutes. If you see source, not found, the fix is coming.

SHOW: The terminal shrinks to a 3-row strip. Above it, the code first: CODE(dataset-creator/docker-shell.sh: 8–22)
folded to lines 8, 13, 16–22 (9 lines + 2 gap rows = 11 rows; lines 4 `set -e` and 10 are not narrated). As the SAY
names each line, it lights and its picture is *pulled out of it* (a Transform, so the viewer sees what became what):
line 8 → a GRAY arrow from an `env.dev` glyph; line 13 shrinks into a TEAL image box `llm-dataset-creator`; line 16
into a TEAL container box; lines 17 and 18 into V2's two PINK mount arrows `dataset-creator → /app` and `secrets →
/secrets` (GREY dashed key outline still empty); lines 19–21 into three small chips `GOOGLE_APPLICATION_CREDENTIALS`,
`GCP_PROJECT`, `GCS_BUCKET_NAME`. On "Three variables" the code panel fades and the pulled-out picture moves to the
centre (image → container, mounts, chips); `--rm` becomes a GRAY tag "removed on exit" on the container box. Never
more than code + picture + strip on screen. No port arrows.
SAY: What did the script do? It reads env.dev, builds the image, and runs it with two folders mounted: this folder becomes slash app, and your secrets folder becomes slash secrets. Three variables carry the key's path, your project and your bucket. The dash dash rm flag removes the container when you exit.

SHOW: The panel fades; the terminal grows back (frame turns TEAL, title `container · llm-dataset-creator`) and prints
TERM(laptop/07-docker-shell-dataset-creator.txt: 21–26, 27 cut before " exit"). Line 23 "Virtual environment
activated." gets a GRAY `erratum` tag "printed before line 26"; the prompt's missing `(app)` gets a GRAY note "no
(app) prefix". An extra card "which Python, which settings" → TERM(dataset-creator/00-x-whoami.txt: 5, 9–11)
(`/.venv/bin/python` lit GREEN). The prompt `app@6f5113cdb660` gets the GRAY tag `your id will differ`.
SAY: Read the banner kindly: it says activated before the activation line runs, and the prompt never shows an app prefix. Both are harmless; an extra check shows Python comes from slash dot venv, and your settings arrived. The part after app and the at sign is the container ID; yours will differ.

SHOW: TRACKER DsRun 3. GRAY chip "README.md · line 69 · a Prerequisites tip, run inside the container". It types
`ls -la /secrets` with a YELLOW `▶ your turn` tag → TERM(dataset-creator/01-ls-secrets.txt: 2–4). A GREY dashed
ghost row appears under it: "with a key: llm-service-account.json" (dashed, clearly not output).
SAY: Step 3 is the README's tip: ls dash la slash secrets, inside the container. With a key, you'd see llm-service-account.json here. Ours shows only the folder itself, on purpose.

SHOW: TRACKER DsRun 4. It types `python cli.py --help` with a YELLOW `▶ your turn` tag →
TERM(dataset-creator/04-help.txt: 2–10). The three flags light in turn. GRAY caption "no key needed yet: the clients
look for credentials on their first call". 2 s hold.
SAY: Step 4: python cli.py dash dash help. Three flags: generate, prepare and upload. It works without a key, because the code only looks for credentials when it first calls Google. Pause, and get to this prompt.

SHOW: A second terminal slides in over the first (title `laptop · second terminal`, prompt
`student@laptop:~/AC215/llm-finetuning/dataset-creator$`), GRAY tag `extra`. It types `dash docker-shell.sh` →
TERM(laptop/20-x-dash.txt: 2) in RED, a RED sticker "Debian · Ubuntu · WSL: sh is dash" and a GREEN fix chip
`bash docker-shell.sh`; a GRAY note "macOS: sh works". Then `cd ..` → (no output) and
`sh dataset-creator/docker-shell.sh` → TERM(laptop/21-x-wrong-folder.txt: 2; wrap) in RED, sticker "run it from
inside the folder", fix chip "cd into the folder first · README.md:68"; then `cd dataset-creator` → (no output). A
RED chip, no terminal: "a second `sh docker-shell.sh` while one runs → Conflict: the name is already in use
(`laptop/11` lines 21–24) · use the laptop shell, or `exit` first".
SAY: Two traps, shown as extras from a second terminal. On Debian, Ubuntu or WSL, sh is dash, which has no source command: run bash docker-shell.sh instead. And from the repository root, the script cannot find env.dev: cd into the folder first.

SHOW: The second terminal types `docker images` (extra) → TERM(laptop/09-x-docker-images.txt: 2–3); `1.64GB` lights
YELLOW. Beside it, a TEAL image block stacks an ORANGE base slab (`python:3.12-slim-bookworm`), a thin TEAL `/app` layer
and a thick GREEN `/.venv` slab "133 packages · 587 MB" (from `dataset-creator/02`, as a chip); inside the slab two
GRAY dashed chips "chromadb", "langchain" with a GRAY `erratum` tag "never imported here". The second terminal slides
away; the first, at the container prompt, stays. Everything fades to an empty frame.
SAY: One more extra: docker images reports 1.64 gigabytes. The lockfile installs 133 packages, among them the RAG lecture's chromadb and langchain, which this code never imports.

---

## S05 · Manufacturing a persona — `s05_persona.py` · `Persona`

Lecture: 4–5.

SHOW: LECTURE 4–5. No terminal. A three-part card (our redrawing of slide 5): "instruction", "context (optional)",
"output". On "drops the context", the context slot fades and the card folds into a GREEN-outlined brick with two
fields `question` and `answer` (V3's brick). A stack of empty brick outlines grows behind it with a counter "≈ 100".
SAY: The lecture's instruction dataset has three parts per example: an instruction, optional context, and the output you want. The tutorial drops the context: each example is a question and an answer. Who writes a hundred of them? Another model, a teacher.

SHOW: V3. A BLUE teacher-model box "gemini-3.1-flash-lite · global" (excerpt chips `dataset-creator/cli.py · line 18
(excerpt)`: `GCP_LOCATION = "global"`, `line 19 (excerpt)`: `GENERATIVE_MODEL = "gemini-3.1-flash-lite"`). Two cards slide
into it as named: GRAY "system instruction · the persona" (`cli.py · lines 36–144`) and GRAY "input prompt · 20 pairs"
(`line 169`). Out of its right side, the answer pours through a PINK-outlined mould labelled "response schema" (`lines
146–160`) and drops out as BLUE bricks `{question, answer}`, 20 at a time; five batches stack, a counter "batch 0 … 4".
A GOLD tag `billed · cents` on the teacher.
SAY: Here the teacher is Gemini 3.1 Flash Lite, called in the global location. It gets a system instruction describing the persona, an input prompt asking for 20 pairs, and a JSON schema that fixes the answer's shape: question and answer objects.

SHOW: The V3 picture shrinks to a strip along the top (teacher box + one row of five empty brick slots, height ≤ 1.2).
TRACKER DsGen 1. Full-width TEAL terminal at the container prompt `app@6f5113cdb660:/app$`, GRAY tag `no key`, at
most 9 rows: it types `python cli.py --generate` with a GOLD `billed` tag → TERM(dataset-creator/05-generate.txt: 4–9,
…, 12–13) (9 rows; "Error occurred …" lines cut at 65 characters, RED). As each RED line prints, one brick slot in the
strip goes dark; the GRAY `…` row darkens the fourth (batch 3), so the five slots go dark one per batch. A GOLD chip
"≈ $2 / 1,000 iterations · README.md:151". A GRAY caption "exit status 0" appears and a YELLOW circle draws around it.
SAY: Step 1: python cli.py dash dash generate. With a key, it costs cents: the README estimates 2 dollars per 1,000 iterations. Without one, every batch prints the same line: the key file was not found. And yet the exit status is zero, which means success. Remember that zero.

SHOW: TRACKER DsGen 2. The terminal shrinks to a 3-row strip (its last line and the circled "exit status 0").
Above it CODE(dataset-creator/cli.py: 83–102) folded to lines 83–90, 96, 102 (10 lines + 2 gap rows = 12, persona
masked by `unname()`); the five openers on lines 85–89 light one by one ("Good question", "Glad you ask", "I have slides for
that", "I knew you will ask this…", "Remember rule number 672…").
SAY: Step 2 explains the system prompt, which lives in cli.py. It tells the teacher to open each answer with one of the instructor's catchphrases, such as good question, or glad you ask. And it asks for technical, passionate answers.

SHOW: TRACKER DsGen 3, then DsGen 4. An excerpt chip `dataset-creator/cli.py · line 169 (excerpt)`: "Generate 20
diverse, informative, and engaging question-answer pairs about cheese …" with a GRAY note "= README.md · line 144".
Then CODE(dataset-creator/cli.py: 170–181) (12 lines): line 170 `NUM_ITERATIONS = 5` lights YELLOW with an `erratum`
tag "a constant you edit · README.md:106 says "default parameters""; line 174 `temperature=0.9` lights; lines 179–180
`response_mime_type="application/json"`, `response_schema=response_schema` light PINK and the mould from V3 pulses.
SAY: Step 3 is the input prompt, asking for 20 diverse pairs. Step 4: the number of iterations is a constant on line 170, not a flag; edit it for a bigger dataset. Temperature 0.9 adds variety, and the response schema makes Gemini return JSON in that shape.

SHOW: TRACKER DsSamples 1. The panel fades. QUOTE(expected/readme-generate-sample-qa.txt: 4–5, 6 cut after "‹instructor›,",
8, 9–10 cut after "cheese monker,", 11) headed `README.md · lines 163–175`, tag `expected`; the two answer openers light
BLUE. A GRAY `erratum` chip under it: "README.md:114–135 lists older openers than cli.py:83–101 · cli.py's own
sample answers (lines 127–141) still open with Yello / Welcome" (line numbers only; lines 133 and 140 carry the full
name and are never quoted).
SAY: With a key, the files would hold answers like the README's samples: Yello, this is the instructor, your cheese monker. A small slip: the README's prompt excerpt lists older openers than cli.py, but cli.py's own samples still open with Yello and Welcome. Expect a mix.

SHOW: The quote card fades. An excerpt chip `dataset-creator/cli.py · line 45 (excerpt)`: "Include specific data such
as optimal pH levels, aging temperatures, and humidity percentages". The strip fades for the ponder card.
SAY: One question before we move on. The prompt asks the teacher for specifics, such as optimal pH levels.
PONDER(8 s, "If the teacher gets a pH value wrong, what happens to it after fine-tuning?")

SHOW: The ponder card leaves. A BLUE brick with a RED-outlined number "pH ✗" travels from the teacher into a GREEN
dataset stack, then into a GREY student-model box that now says the same number in a speech bubble, with the
`‹instructor›` chip. Caption: "synthetic data carries the teacher's mistakes". Everything fades to an empty frame.
SAY: It becomes a training target. The student learns to say it, confidently, in the instructor's voice. Synthetic data carries the teacher's mistakes, so check what the teacher wrote.

---

## S06 · Prepare: a failure that surfaces late — `s06_prepare.py` · `LateFailure`

Lecture: 5.

SHOW: TRACKER DsPrep 1. Full-width TEAL terminal at `app@6f5113cdb660:/app$`. GRAY chip "right after the failed
generate, as a student would". It types `python cli.py --prepare` → TERM(dataset-creator/07-prepare-no-data.txt:
2–6, …, 15–17, …, 23) (11 rows); line 6 `Shape: (0, 0)` lights YELLOW; line 15 (`line 243, in prepare`) and line 23
`KeyError: 'question'` print RED.
SAY: Now step 1 of the prepare section, as a student would type it right after that run: python cli.py dash dash prepare. Zero errors, a shape of zero by zero, and then a crash: key error, question, from line 243 of cli.py.

SHOW: The terminal shrinks to a 3-row strip (the KeyError). Above it V3's net: CODE(dataset-creator/cli.py: 184–201)
folded to 184–186, 188, 196–201 (10 rows). Five RED sparks (one per batch) fly out of line 188's call and fall into
a net drawn under lines 200–201, labelled `except Exception`; each spark becomes a printed line; the brick pile beside
it stays empty; a calm GRAY "exit 0".
SAY: Trace it back. In generate, each batch runs inside a try block, and the except on line 200 catches any exception, prints it, and carries on. So no file was written, and the command still exited with zero.

SHOW: The net panel's code fades, leaving only V3's net glyph (the empty brick pile, the `except Exception` label)
small at the left edge. CODE(dataset-creator/cli.py: 232–243) folded to 232–233, 235, 241–243 (6 lines + 2 gap rows)
full width, beside the net glyph (code panels are never side by side: both run past 65 characters). An empty GRAY
table "0 rows · 0 columns" slides out of the empty pile into line 232's `output_pairs_df`; on line 243
`output_pairs_df["question"]` lights and a RED `KeyError` stamp lands. A GRAY arrow runs from the net glyph to the
stamp: "the error was there all along · the net moved it". Caption YELLOW: "read the lines, not the exit code".
SAY: Prepare found no files, built an empty table, and failed the first time it read the question column. The error was there all along; the catch-all only moved it one command later. Read the lines, not the exit code.

SHOW: The panels fade. A GREEN fix card: "key → `~/AC215/secrets/llm-service-account.json` (exact name)" and
"check: `ls -la /secrets`". The GREY dashed key outline in V2's `secrets/` glyph turns into a solid GOLD key glyph (an
illustration: tag `illustration`).
SAY: The fix is the key itself: put it in the secrets folder with the exact name, and check with ls dash la slash secrets.

SHOW: TRACKER DsPrep 1 · extra. The second laptop terminal slides in (title `laptop · second terminal`), GRAY tag
`extra`, BLUE dashed tag `scripted`. It types `cp ~/scripted/cheese_qa_*.txt data/; ls -la data` →
TERM(laptop/13-x-scripted-data.txt: 2, 5–10 names+sizes); the five `cheese_qa_` files print inside a BLUE dashed
outline; line 10's `1 … instruct-dataset.csv` lights RED-outlined with a GRAY note "left by the failed run".
A GRAY card beside: "hand-written in the shape Gemini returns · 20 pairs (Gemini: ≈ 100)" and a GRAY chip "not in
the repo · with a key, generate writes these files for you".
SAY: So we can watch a real run, an extra: five hand-written files, tagged scripted, in exactly the shape Gemini returns. They hold 20 pairs, where Gemini would write about a hundred; your generate writes its own. Note the 1-byte CSV the failed run left behind.

SHOW: The second terminal slides away. In the container terminal it types `python cli.py --prepare` again →
TERM(dataset-creator/09-prepare.txt: 4–9, 11, 13–17) (12 rows: the five "Processing file" lines, "Number of
errors: 0", `Shape: (19, 2)` and the five rows; lines 13–17 cut at 65 characters), tag `scripted`. Line 11
`Shape: (19, 2)` lights YELLOW. An excerpt chip `dataset-creator/cli.py · line 233 (excerpt)`:
`output_pairs_df.drop_duplicates(subset=["question"], inplace=True)`; a small animation: 20 bricks, the last
(BLUE dashed) matches the first's question and drops out → 19. The openers in lines 13–17 light BLUE.
SAY: Now prepare again. Five files processed, zero errors, and a shape of 19 by 2. The last scripted pair repeats the first question on purpose, and drop duplicates on line 233 removed it. Every answer opens with a catchphrase.

SHOW: V4 station 1 appears: one brick lands on a conveyor as a GREEN CSV-row card `question,answer`, file chip
`instruct-dataset.csv` (GREEN); the word "instruct" lights, with a GRAY lecture chip "instruction dataset · slide 5".
Then the GRAY "your turn" card with a YELLOW `▶ your turn` tag: `python cli.py --generate` · `python cli.py --prepare`;
last line GOLD "generate: billed · cents" and GREEN "prepare: free". 2 s hold. Everything fades to an empty frame.
SAY: The rows are saved as instruct-dataset.csv: the lecture's term, in the file name. Pause, and run generate and prepare yourself.

---

## S07 · Rows to JSONL, then upload — `s07_jsonl.py` · `RowsToJsonl`

Lecture: 5, then 8.

SHOW: LECTURE 5. TRACKER DsPrep 2. V4 conveyor across the middle, station 1 (the CSV row) on the left. Above it
CODE(dataset-creator/cli.py: 240–247) (8 lines); line 242 and 245 light. Station 2 builds: the brick becomes a text card
from PANEL(dataset-creator/13-x-csv-head.txt: 3, 4 cut after "large wheels.", "header" `train.csv`), lines starting
`human:` and `bot:`; a GRAY tag "for autotrain-runner · track A doesn't use it" and the card dims.
SAY: Step 2 of prepare is about format. Follow one pair. It starts as a CSV row. Lines 241 to 247 glue it into one text with human and bot labels, the text column the repository's autotrain folder reads. Track A doesn't use that one.

SHOW: The code window Transforms into CODE(dataset-creator/cli.py: 251–257) (7 lines). Station 3 builds: the brick
unfolds into nested boxes: `contents` → two turns, `role: user` / `role: model`, each `parts` → `text`; the question
drops into the user turn, the answer into the model turn.
SAY: Lines 251 to 257 build what Gemini tuning expects: a list called contents, with a user turn and a model turn, each holding parts and text.

SHOW: TRACKER DsPrep 2 · extra. The code fades. PANEL(dataset-creator/12-x-jsonl-pretty.txt: 3–8, 13–16 folded,
"header" `head -1 data/train.jsonl | python -m json.tool`) full width (10 lines + 1 gap row = 11 rows, text cut at 65
characters), tags `scripted`, `extra`; the keys `contents` (l.3), `role` (l.5, 13), `parts` (l.6, 14), `text` (l.8,
16) light. Then it Transforms in place into QUOTE(expected/readme-prepare-gemini-format.txt: 4–9, 14–17 folded the
same way) headed `README.md · lines 191–212`, tag `expected`: the four keys stay lit and do not move
(TransformMatchingStrings), only the values change; caption "same nesting". Then the quote collapses into the single
line PANEL(dataset-creator/11-x-train-jsonl-head.txt: 2 cut after "Gruyere?"}]},", "header" `head -c 400
data/train.jsonl`) across the middle: the newlines visibly disappear, caption "one example per line".
SAY: An extra look at the real train.jsonl: the same nesting as the README's example, but each example on a single line. That's the L in JSONL: JSON lines.

SHOW: CODE(dataset-creator/cli.py: 259–273) folded to 260–264, 267, 270–273 (10 lines + 2 gap rows = 12). V4's
splitter: 19 bricks enter, a GRAY seed chip "random_state=42", 17 go to a GREEN `train.jsonl`, 2 to a GREEN
`test.jsonl`; on line 267 a GRAY cap "≤ 256 · per the comment on line 266". The second laptop terminal (extra) types
`ls -la data; wc -l data/*.jsonl data/*.csv` → TERM(dataset-creator/10-x-ls-data-after.txt: 10–14 names+sizes, 15–17)
as a 3-row strip that scrolls; `2 data/test.jsonl` and `17 data/train.jsonl` light.
SAY: Then train test split holds out 10 percent with a fixed seed: 17 examples for training, 2 for validation. The code's comment says Gemini accepts at most 256 validation examples, hence the cap.

SHOW: LECTURE 8. The JSONL line's model turn lights; under it a row of token boxes for the answer's first words
("Glad", "you", "ask", …) with a YELLOW arrow sliding one box at a time: "predict the next token".
SAY: Whatever the wrapping, training is still next-word prediction, now on the instructor's answers.

SHOW: The second laptop terminal (title `laptop · second terminal`, extra) types `ls -la data; git -C .. status --short
--ignored` → TERM(laptop/15-x-data-on-host.txt: 5–14 names+sizes, 15); the files light GREY (seen from the laptop), line
15 `!! dataset-creator/data/` lights GREEN with a GRAY note "ignored · .gitignore lines 8–9". V2's PINK mount arrow
`dataset-creator → /app` pulses.
SAY: An extra from the laptop side: the bind mount left these files in your clone. Git status shows the data folder as ignored, so it stays out of your commits.

SHOW: TRACKER DsUp 1. The container terminal returns full width (GRAY tag `no key`). It types `python cli.py --upload`
with a GOLD `billed` tag → TERM(dataset-creator/14-upload.txt: 2–3, …, 9–10, …, 36; wrap) (line 36 RED, 2 rows). Then
the terminal shrinks to a strip; V2's PINK route from the container to the BLUE bucket pin `gs://<your-bucket>/
llm-finetune-dataset-small/` stops at the container wall with a RED "no key" stamp. A GREY dashed "what to look for"
card (no output panel): excerpt chip `dataset-creator/cli.py · line 293 (excerpt)`: `print("Uploading file:", data_file,
destination_blob_name)`, "× 5 files · then check your bucket"; a RED chip "403? → your bucket in env.dev · both roles ·
API enabled".
SAY: Next section, upload: python cli.py dash dash upload. This time it fails loudly, with a default credentials error: file not found. With a key, no output is documented. Look for one line per file starting with uploading file, five in all, then find them in your bucket.

SHOW: An `erratum` card: excerpt chip `dataset-creator/cli.py · line 280 (excerpt)`: `bucket = storage_client.bucket(
GCS_BUCKET_NAME)` with a GRAY note "assumes the bucket exists"; GREEN fix "create it first (the card in Prerequisites)";
a GRAY chip "changed env.dev? `exit`, then `sh docker-shell.sh` again: it is read at start (`docker-shell.sh` lines 8,
19–21)". Then the GRAY "your turn" card with a YELLOW `▶ your turn` tag: `python cli.py --upload`; last line GOLD "storage:
cents". 2 s hold. Everything fades to an empty frame (the container stays open for the next chapter).
SAY: A small slip: the README never says to create that bucket, and upload assumes it exists. Make it first. If you just changed env.dev, restart the container. Then pause and upload.

---

## S08 · Hand it to Google: the tuning job — `s08_tuning.py` · `TuningJob`

Lecture: 13–16.

SHOW: TRACKER FtRun 1. Full-width TEAL terminal at `app@6f5113cdb660:/app$`. It types `exit` →
TERM(laptop/07-docker-shell-dataset-creator.txt: 28); the frame turns GRAY (`laptop`). It types `docker ps -a`
(extra) → TERM(laptop/14-x-ps-after-exit.txt: 2) (only the header). Then `cd ../gemini-finetuner && pwd && ls`
(extra form of "go to the folder", README.md:236) → TERM(laptop/17-x-cd-gemini-finetuner.txt: 2–8); the prompt
becomes `student@laptop:~/AC215/llm-finetuning/gemini-finetuner$`.
SAY: On to the fine-tune section. Type exit; the container removes itself, and an extra docker ps dash a shows nothing left. Step 1: go to the gemini-finetuner folder.

SHOW: TRACKER FtRun 1 · extra. The terminal shrinks to a strip; it types `grep -n 'gs://' cli.py` (extra) →
TERM(gemini-finetuner/04-x-dataset-uris.txt: 2–3; wrap). Above it CODE(gemini-finetuner/cli.py: 9–15) (7 lines);
`gs://cheese-dataset` on lines 10–11 lights YELLOW with `erratum` tag "the course's bucket · # Replace with your
dataset"; a YELLOW template chip `gs://<your-bucket>/llm-finetune-dataset-small/…` slides over each. V2's PINK mount
`gemini-finetuner → /app` pulses: "files in the folder: live inside · no rebuild" (env.dev is different: read at start).
SAY: An extra edit the README leaves out: lines 10 and 11 still point at the course bucket, cheese-dataset. Point them at your own. The folder is mounted into the container, so there's no need to rebuild.

SHOW: TRACKER FtRun 2. Full terminal again. It types `sh docker-shell.sh` with a YELLOW `▶ your turn` tag →
TERM(laptop/18-docker-shell-gemini-finetuner.txt: 3, 12–16, …, 21, 27 cut before " exit") (BuildKit spaces
collapsed); each `CACHED` word lights GREEN, `Building 0.0s` lights. The frame turns TEAL, title `container ·
gemini-finetuner`. An extra card "are the two folders built the same way?" → TERM(laptop/16-x-diff-folders.txt: 2–4)
as a chip row over the strip.
SAY: Step 2: sh docker-shell.sh again. It's instant: every layer up to uv sync is cached, because both folders share the same Dockerfile, pyproject and lockfile, as an extra diff shows.

SHOW: TRACKER FtRun 3. It types `python cli.py --help` → TERM(gemini-finetuner/01-help.txt: 2–9). Then the terminal
shrinks to a strip; above it CODE(gemini-finetuner/cli.py: 12–33) folded to 12–15, 19–23, 26–32 (16 rows → two
windows: 12–15 + 19–23, then 26–32). V2's cloud draws its three pins: `global` (dim, "the teacher"), `us-central1`
lights as `train_client` is named, `us` lights as `chat_client` is named with its `base_url` excerpt
`https://aiplatform.us.rep.googleapis.com` as a PINK route.
SAY: Step 3: python cli.py dash dash help shows two flags, train and chat. The train client creates tuning jobs in us-central1. The chat client calls the tuned model in the multi-region location US, at its own address.

SHOW: CODE(gemini-finetuner/cli.py: 44–62) folded to 44, 48–49, 52–55, 61–62 (9 lines + 3 gap rows = 12; line 56,
the display name, and lines 63–65 are not shown). As named: lines 48–49 light PINK (the two `gs://` datasets); line 53
`epoch_count=1`; line 54; line 55 `adapter_size="ADAPTER_SIZE_FOUR"` gets a GRAY hedge chip "by our reading: Google's
managed small-adapter idea · see part 2"; lines 61–62 `train_client.tunings.tune(base_model=…` light YELLOW.
SAY: The train function wraps your bucket files as tuning datasets, and asks for one epoch and an adapter of size four. By our reading, that's Google's managed version of the idea you'll build in part 2. One call starts the job.

SHOW: TRACKER FtModel 1. Full TEAL terminal, GRAY tag `no key`. It types `python cli.py --train` with a GOLD `billed`
tag → TERM(gemini-finetuner/02-train.txt: 2–5, …, 69; wrap) (line 4 GRAY-dim with a tag "harmless", line 69 RED).
V2's route from the container toward `us-central1` stops at the wall with a RED "no key" stamp.
SAY: Step 1 of the fine-tune model section: python cli.py dash dash train. The experimental warning is harmless. Then the missing key: no job was created.

SHOW: The terminal shrinks to a strip. A GREY dashed "what to look for" card (no output panel, nothing documented):
three excerpt chips in order, `gemini-finetuner/cli.py · line 67 (excerpt)` "Training job started. Monitoring
progress...", `line 68 (excerpt)` `Job name: {tuning_job.name}` with a GRAY note "…/locations/us-central1/tuningJobs/…",
`line 89 (excerpt)` `Tuned model info: {tuning_job.tuned_model}` with a GRAY note "→ None after a minute"; a RED chip
"403? → your bucket in cli.py lines 10–11 · both roles · API enabled". Then CODE(gemini-finetuner/cli.py: 125–126)
(2 lines), `wait_for_job=False` YELLOW, GRAY note (no `erratum`: a design choice) "waits 60 s, then leaves · never
waits for the job to finish" (`cli.py` lines 71–72). A small dry-cleaner glyph (tag `illustration`): a garment goes
over a counter, a ticket comes back. Then the GRAY "your turn" card with a YELLOW `▶ your turn` tag:
"`gemini-finetuner/cli.py` lines 10–11 → your bucket · `sh docker-shell.sh` · `python cli.py --train`"; last line GOLD
"tuning: billed per training token · the README's table comes next". 2 s hold.
SAY: With a key, look for training job started, a job name in us-central1, and after a minute, tuned model info, none. Main calls train with wait for job set to false, so the command hands in the job and leaves, like a ticket at the dry cleaner. Read the cost table next, then pause and start your job.

SHOW: LECTURE 13–16. A GREY dashed miniature of the memory column (V5 preview, `concept · lecture only`) labelled "GPU
memory · part 2" (no number yet) slides from the laptop side across to the BLUE `us-central1` pin and settles there.
TRACKER FtModel 2. A schematic job page (tag `illustration`, no logos): status chip Running → Succeeded, rows "tuned
model", "endpoint: projects/…/locations/us/endpoints/…" (GRAY placeholders); a GRAY chip "Agent Platform › Tuning ·
console.cloud.google.com/agent-platform/tuning/managed (README.md:261)". V2's PINK arrow runs from the bucket straight
into the job, bypassing the container.
SAY: Training needs far more GPU memory than a laptop has; here that's Google's problem. Step 2: watch the job in the console until it says succeeded, with a tuned model and an endpoint.

SHOW: The job page shrinks; the strip fades. The ponder card enters.
SAY: A question to pause on.
PONDER(8 s, "--train returns after about a minute. Where is the training happening, and what would you lose if you deleted the container right now?")

SHOW: The ponder card leaves. The TEAL container box fades out entirely (`--rm`); the BLUE job at `us-central1` keeps
running with the bucket arrow; the console page with the job stays. Caption "the container only submitted the job".
Everything fades to an empty frame.
SAY: On Google's hardware in us-central1, reading your bucket directly. Deleting the container loses nothing: it only submitted the job.

---

## S09 · Cost, endpoint and chat — `s09_chat.py` · `CostAndChat`

Lecture: none.

SHOW: TRACKER FtCost 1. QUOTE(expected/readme-cost-table.txt: 4–11) headed `README.md · lines 269–276`, tag
`expected`, GOLD outline; the two cost cells `$112.73` and `$0.573` light GOLD as named; "*** Way too much data for this
fine tuning!" lights.
SAY: Step 1 of the cost section: the README's table. At 0.008 dollars per thousand tokens, 16,444 documents over 3 epochs come to 112 dollars 73; the table calls that way too much data. 88 documents cost about 57 cents.

SHOW: An `erratum` tag on the table: "Gemini 1.5 Flash · 3 epochs" (in the table) vs "code: gemini-3.1-flash-lite ·
epoch_count=1" (excerpt chips `gemini-finetuner/cli.py · line 15 (excerpt)` and `line 53 (excerpt)`). The table
greys; a GOLD chip "check the pricing page the README links · README.md:278"; a small GOLD chip "generating the data:
cents".
SAY: A small slip: the table prices Gemini 1.5 Flash for 3 epochs, while the code tunes Gemini 3.1 Flash Lite for 1. Treat these numbers as stale and check the pricing page the README links.

SHOW: TRACKER FtChat 1 (extra). CODE(gemini-finetuner/cli.py: 102–119) folded to 102–107, 109–110, 113–117 (13 rows →
two windows: 102–107, then 109–117 folded) through `unname()`. Line 107 lights YELLOW: `MODEL_ENDPOINT =
"projects/‹instructor-project-number›/locations/us/endpoints/‹endpoint-id›"` with `erratum` tag "the instructor's
endpoint"; a YELLOW template chip `projects/<your-number>/locations/us/endpoints/<id>` slides over it from the
console page (illustration) of S08. GRAY tag `extra`.
SAY: Before you chat, one more extra edit. Line 107 still holds the instructor's endpoint. Copy yours from the console: a path ending in locations, US, endpoints and an ID. Paste it there; otherwise chat points at the instructor's endpoint, which your key can't reach.

SHOW: TRACKER FtChat 2. Full TEAL terminal at `app@2a2550dec953:/app$`, GRAY tag `no key`. It types `python cli.py
--chat` with a GOLD `billed` tag and a YELLOW `▶ your turn` tag → TERM(gemini-finetuner/03-chat.txt: 2–5, …, 66;
wrap) (line 4 through `unname()`: `query:  How is cheese made in Greece? Answer ‹instructor› style?`; line 5 `Using
serving location: us` lights PINK; line 66 RED). V2's route toward the `us` pin stops at the wall, RED "no key".
SAY: Step 2: python cli.py dash dash chat. It prints its question, how is cheese made in Greece, answered the instructor's way. Then it prints the serving location, US, and the same missing key. Pause and run it once your endpoint is in.

SHOW: The terminal shrinks to a strip. QUOTE(expected/readme-chat-example.txt: 10–14; wrap, line 14 cut after "heart
of cheesemaking!") headed `README.md · lines 295–301`, tag `expected`; the opener lights BLUE, the persona chip GRAY.
A GRAY `erratum` chip "the README's query is older than the code's".
SAY: The README shows a working endpoint's answer to an older question: the same Yello opener. Your answer will differ.

SHOW: TRACKER FtChat 3, then FtChat 4. A GRAY chip "hosted demo · `ac215-llm-rag.dlops.io/finetunechat` · use Chrome ·
README.md:303–306 · optional" with a GRAY note "its vector-database line belongs to the RAG app (L10)" (GREY dashed).
Then a schematic training-monitor panel (tag `illustration`, no screenshot, never `images/training-1.png`): two
falling GRAY loss curves "training", "validation" on unlabeled axes, and beside them a second GRAY schematic label
"data distribution" (README.md:308–316).
SAY: Step 3, the hosted demo, is optional. Step 4: the console's training monitor shows your job's loss curves and its data distribution.

SHOW: V2 full stage one last time: GREY laptop with `secrets/` and the clone, two TEAL containers, BLUE cloud with the
teacher at `global`, the bucket, the job at `us-central1`, the endpoint at `us`; the four routes light in order
(generate, upload, train, chat). Then a GRAY curtain slides over the model inside the cloud: a crossed-out eye "you
never saw a weight". A GREEN adapter glyph glints in the dark on the right, caption "part 2". Everything fades to an
empty frame (end of part 1).
SAY: That's track A: a teacher wrote the data, Google ran the job, and you have an endpoint to call. And you never saw a single weight. In part 2, the weights are in your hands.

---

## S10 · Colab, and the 120 GB bill — `s10_memory.py` · `MemoryBill`

Lecture: 11–16, 37–39, 71–72.

SHOW: Part 2 opens on the BLUE Colab frame "QLoRA notebook · Colab" (tag `illustration`). TRACKER ColabA 1: a
schematic File menu, "Save a copy in Drive" lights YELLOW (from `cell-01.md`), GRAY note "the original is view-only".
TRACKER ColabA 2: a schematic "Change runtime type" dialog, "T4 GPU" selected; GOLD chip "A100 · L4: Pro or compute
units".
SAY: Part 2 happens in the course Colab, Tutorial, Finetuning with QLoRA. First: File, Save a copy in Drive; the original is view-only. Then: Runtime, Change runtime type, and pick a GPU. A free T4 is enough.

SHOW: TRACKER ColabA 3. CODE(colab/cell-08.py: 1–7) (7 lines, wrap); lines 3–4 and 7 light. Below it
RECORDED(expected/colab-c08-install.txt: 13, 18, 21): `+ bitsandbytes==0.50.2`, `+ trl==1.14.0` GREEN, `- torchao==0.10.0`
GRAY; tag `at the time of recording`.
SAY: Section 3 pins transformers, bitsandbytes and trl, and removes torchao, which, the notebook notes, makes peft refuse to add LoRA layers.

SHOW: One slot below the tracker; each step *replaces* the previous one in it (at most one output on screen at a
time). TRACKER ColabA 4: a schematic Secrets panel (illustration): a row `HF_TOKEN`, value a row of GRAY dots,
"notebook access" switch on; RECORDED(expected/colab-c10-hf-token.txt: 13); a GRAY chip "SecretNotFoundError? name it
HF_TOKEN · turn notebook access on". TRACKER ColabA 5: the panel Transforms into RECORDED(expected/colab-c12-
versions.txt: 32; wrap), tag `at the time of recording`, then RECORDED(expected/colab-c14-drive-mount.txt: 6). TRACKER
ColabA 6: RECORDED(expected/colab-c16-hf-download.txt: 7–8 cut after "models--Qwen--Qwen3-0.6B"), whose path
Transforms into a GREY Drive folder glyph `MyDrive/LLM_cache` with two model boxes inside. Then the GRAY "your turn"
card with a YELLOW `▶ your turn` tag: "Save a copy · T4 runtime · HF_TOKEN secret · run Part A, sections 3 to 6"; last
line GREEN "T4: free (when available)" and GOLD "A100 / L4: compute units". 2 s hold.
SAY: Section 4 reads your Hugging Face token from Colab secrets; both models are public, so it matters mostly for the optional upload. Section 5 imports the libraries, prints the versions, at the time of recording torch 2.11 and transformers 5.16, and mounts your Drive. Section 6 caches both models there. Pause and run part A.

SHOW: LECTURE 11–16. The Colab frame shrinks to a corner. A GREY dashed model block "10 B parameters" (`concept ·
lecture only`) pours into a column: a first slab "Parameters · FP16 · 20 GB". The ponder setup: the column stops.
SAY: Now the lecture's question. Why not simply train all the weights? Take a model with 10 billion parameters in 16-bit floats: the weights alone take 20 gigabytes.
PONDER(8 s, "Full fine-tuning: what else has to sit in GPU memory, and how much?") (a GRAY hint line on the card: "hint:
the optimizer is Adam, kept in 32-bit")

SHOW: The ponder card leaves. V5: two more slabs stack in proportion 1 : 1 : 4: "Gradients · FP16 · 20 GB", "Optimizer
states · FP32 · momentum + variance · 80 GB"; a total "120 GB" writes beside. Five GREY dashed 24 GB GPU tiles line up
and the column pours into them, filling all five.
SAY: The gradients, one per weight, take another 20 gigabytes. And the Adam optimizer keeps two running averages per weight in 32-bit floats: 80 gigabytes. That's 120 in total, the memory of five GPUs with 24 gigabytes each, before any activations.

SHOW: LECTURE 37–39, then LECTURE 71–72. The column copies twice to the right. Second column: gradients and optimizer
slabs shrink to two small GREEN blocks "A", "B"; the 20 GB parameters slab stays GREY with a snowflake ("frozen, but
needed for the forward pass"); total "≈ 40 GB" with a GRAY tag "the lecture's total". Third column: the parameters
slab shrinks to a thin GREY "4-bit" block (tag `NF4`); a small GRAY optimizer-page block gets a PINK arrow to a "CPU"
box; total "≈ 12 GB", GRAY tag "the lecture's total". (The slabs are not drawn to add up to the two totals: the
lecture gives totals only.) The three totals line up under the columns: 120 → ≈ 40 → ≈ 12, labels "full", "LoRA",
"QLoRA". Everything fades to an empty frame.
SAY: LoRA trains only small adapters, so gradients and optimizer states nearly vanish, but the frozen base still sits in memory for the forward pass. The lecture puts that at about 40 gigabytes. QLoRA stores the base in 4 bits, and the lecture's total drops to about 12. The next chapters are those three bars.

---

## S11 · Quantization: 16 buckets per weight — `s11_quantize.py` · `Buckets`

Lecture: 43–55, 68–69.

SHOW: No tracker yet (it appears at (e), when the notebook's first cell of part B slides in). LECTURE 43–44. The QLoRA
bar from S10 (≈ 12 GB) sits small at the top left with its 4-bit block lit. V6 (a): a number line 0–100 with three
BLUE dots 27, 55.3, 83.78. On the second sentence a GRAY two-line bridge chip writes: "lecture: LoRA first ·
notebook: quantization first → we follow the notebook".
SAY: Quantization means splitting a range into buckets and storing only which bucket a number fell into. The lecture builds LoRA first; we follow the notebook, which quantizes first.

SHOW: V6 (a): a fine grid of whole-number buckets drops onto the line: the dots snap to 27, 55, 84; then a coarse grid
of tens: 30, 60, 80; a bits counter beside the line reads "7 bits" on the whole-number grid (101 buckets) and drops to
"4 bits" on the tens grid (11 buckets).
SAY: Round 27, 55.3 and 83.78 to whole numbers: 27, 55 and 84. Round to tens: 30, 60 and 80. Fewer buckets need fewer bits, and lose more detail.

SHOW: LECTURE 45–51. V6 (b): ten BLUE values on a line, 1.5 … 10.2. A scale label `c = 127 / 10.2 = 12.451` writes (rounded; the slide truncates);
the line stretches until 10.2 touches a wall at 127; each value snaps to an integer tick and its label changes: 1.5 →
**19**, 2.3 → 29, … 5.6 → **70**, … 10.2 → 127 (19 and 70 lit YELLOW).
SAY: The lecture's worked example uses absmax. Ten values from 1.5 to 10.2 are multiplied by 127 over the largest, so 10.2 lands exactly on 127. Then each value rounds to an integer: 1.5 becomes 19, and 5.6 becomes 70.

SHOW: Dividing back: the ticks shrink to the original line, 19 lands at 1.526, 70 at 5.622; small RED gaps between
1.5 and 1.526 and between 5.6 and 5.622 glow, label "dequantization error". A GRAY `erratum` chip "slide 50 shows 18
and 69 · rounding gives 19 and 70".
SAY: Divide back, and 19 becomes 1.526, 70 becomes 5.622. Those small red gaps are the dequantization error: quantization always loses a little. The slide shows 18 and 69; rounding gives 19 and 70.

SHOW: V6 (c): a long row of weight dots; one large dot far right stretches a single absmax knob and squashes every
other dot onto a few ticks (RED). Then the row splits into blocks of 64, each with its own small knob; the dots spread
over their ticks again. GRAY caption "one constant per block of 64 · the lecture uses one per array".
SAY: One constant for a whole matrix is risky: one large weight squashes everyone else's precision. So bitsandbytes keeps one absmax constant per small block of 64 weights.

SHOW: LECTURE 54–55. V6 (d): a bell-shaped histogram of weights; 16 vertical lines drop evenly spaced, then slide
into NF4's quantile positions, crowded near 0, sparse in the tails; the 16 areas between them shade alternately,
"equal share" on two of them. Each weight dot snaps to its nearest line; one dot's label shrinks from a 32-bit float
"0.0371…" to a 4-bit index "1011". Then two neighbouring 4-bit indices slide together into one byte box `1011 0110`,
caption "two weights per byte".
SAY: Four bits give 16 levels. Weights are bell-shaped, so 4-bit NormalFloat, NF4, puts them at quantiles: dense near zero, sparse in the tails. Each weight is stored as a 4-bit index; two of them fit in one byte.

SHOW: V6 (e): the row of block knobs from (c) lines up and gets quantized too: each knob snaps to a coarser tick,
caption "double quantization". TRACKER ColabB 1. CODE(colab/cell-18.py: 7–12) (6 lines, header `QLoRA notebook ·
Part B · cell 18 · lines 7–12`) slides in; line 10 `bnb_4bit_use_double_quant=True` lights YELLOW, a GRAY chip "the
lecture skips it · the notebook turns it on";
line 9 `"nf4"` and line 8 `load_in_4bit=True` light.
SAY: Those block constants add up, so double quantization quantizes them as well. The lecture skips it; the notebook turns it on, right here, beside NF4.

SHOW: LECTURE 68–69. V6 (f): a GREY 4-bit block (tag `NF4`) inflates into a 16-bit copy (tag `FP16`), meets an input
vector in a matrix multiply, and deflates back; line 11 `bnb_4bit_compute_dtype=torch.float16` lights. A GRAY chip
"lecture: BF16 · notebook: FP16 (the training chapter explains)".
SAY: Stored in 4 bits, computed in 16: for each matrix multiply, the layer's weights are expanded to a 16-bit copy, used, then dropped. The lecture computes in BF16; this notebook in FP16, as the training chapter explains.

SHOW: TRACKER ColabB 2. RECORDED(expected/colab-c21-opt-350m-4bit-model.txt: 3, 6, 10–11, 13–16, 20–21, …, 27) (12
rows); every `Linear4bit` lights GREY; line 6 `(embed_tokens): Embedding(...)` lights white with a GRAY note "not
4-bit", and `(lm_head): Linear(...)` with a GRAY note "stays 16-bit". TRACKER ColabB 3: RECORDED(expected/colab-c25-
tokenize.txt: 4) then RECORDED(expected/colab-c27-opt-generate.txt: 11–12) (the continuation from the three dials
chapter). Then the GRAY "your turn" card with a YELLOW `▶ your turn` tag: "run Part B, sections 1 and 2"; last line
GREEN "T4: free (when available)". 2 s hold.
SAY: Section 1 of part B prints the small OPT model: every linear layer is now Linear4bit, while the embeddings and the output head stay as they were. Section 2 tokenizes and generates the continuation we met earlier. Pause, and run part B.

SHOW: Two RED-crossed misconception chips write in: "4-bit model = 4-bit arithmetic ✗" → GREEN "computed in 16 bits";
"quantization = speed ✗" → GREEN "the win is memory". Everything fades to an empty frame.
SAY: Two misconceptions to drop: a 4-bit model does not do 4-bit arithmetic, and the win is memory, not speed.

---

## S12 · Qwen in 4 bits, and its chat template — `s12_qwen.py` · `QwenInFourBits`

Lecture: 68–69, then 8.

SHOW: LECTURE 68–69. TRACKER Qwen 1. CODE(colab/cell-34.py: 1–6) (6 lines) beside "= the same recipe" pointing at a
mini copy of S11's `cell-18` lines 8–11; then it Transforms into CODE(colab/cell-36.py: 8–18) folded to 8–13, 18 (7
rows); line 18 `prepare_model_for_kbit_training` lights; two chips write under it: GREY snowflake "freezes every
weight", YELLOW "gradient checkpointing: on" with a GRAY note "the training chapter shows it". (`c31`, the BF16
check, is shown in the training chapter's FP16 beat instead.)
SAY: Step 1 loads the real student, Qwen3 0.6B, with the same 4-bit recipe. Then prepare model for k-bit training freezes every weight and turns on gradient checkpointing, a memory trick the training chapter shows.

SHOW: TRACKER Qwen 2. RECORDED(expected/colab-c38-num-params.txt: 5); `375.84896` lights YELLOW. Beside it a GRAY chip
"Qwen3-0.6B: 596 M parameters". The panel stays; the ponder card enters.
SAY: Section 2.1 counts the parameters: 375.8 million. But Qwen3 0.6B has 596 million.
PONDER(8 s, "Qwen3-0.6B has 596 million parameters. Why does the notebook count 375.8 million?")

SHOW: The ponder card leaves. A bar of 596 M splits: GREY "linear weights · 440 M" packs into "220 M" (pairs of 4-bit
values fold into single bytes, two per box); GREY solid "embeddings · 155.6 M" with a small WHITE tag "not 4-bit"
stays (GREY: frozen pretrained weights, against the GREY *packed* slab); a sliver
"norms · 0.07 M". The sum writes: 220.2 + 155.6 + 0.07 = 375.8. TRACKER Qwen 3: RECORDED(expected/colab-c42-qwen-config.txt:
58, 63–64, 71) as a 4-row chip ("quantization_config", `"bnb_4bit_quant_type": "nf4"`, `"bnb_4bit_use_double_quant":
true`, `"quant_method": "bitsandbytes"`).
SAY: The 440 million weights in linear layers are packed two 4-bit values to a byte, so they count as 220 million. The 155.6 million embedding weights and the norms are not quantized. Add them up: 375.8 million. The configuration, in 2.2, confirms NF4.

SHOW: TRACKER Qwen 4: RECORDED(expected/colab-c45-baseline-generate.txt: 8; wrap) with a GRAY note "drifts off topic".
TRACKER Qwen 5: RECORDED(expected/colab-c48-trainable-before.txt: 5); `trainable params: 0` lights, a GREY snowflake
on the model glyph.
SAY: In 2.3 the base model continues a sentence, and it drifts off topic. And 2.4 counts trainable parameters: zero. Everything is frozen.

SHOW: TRACKER Data 1, then Data 2. RECORDED(expected/colab-c51-gdown-dataset.txt: 5–6); RECORDED(expected/colab-c53-
sample-1000.txt: 7, 8 cut after "Italy influence the production of its cheeses?'}]}"). V4's conveyor returns from
part 1: the JSONL brick from S07 slides in from the left and lands on the `contents` row, matching key for key; caption
"exactly track A's format". A GRAY note "the staff's 16k file: Remember / Hi everyone / Welcome / Yello openers
(3.3 · cell 55)" (`expected/colab-c55-extract-qa.txt` lines 25–29). A GRAY chip by the c51 line: "Too many users …?
retry later, or use your own train.jsonl from part 1 (same format)".
SAY: The notebook's step 3 prepares the data. It downloads a 23 megabyte file and samples 1,000 pairs. Look at a row: contents, a user turn, a model turn. It's exactly the format of track A: the brick from part 1 arrives here.

SHOW: TRACKER Data 3. CODE(colab/cell-59.py: 10–15) (6 lines); line 13 `apply_chat_template` lights. V4 station 4: the
brick unrolls into a ribbon drawn from RECORDED(expected/colab-c63-one-example.txt: 3): bright markers
`<|im_start|>user`, the question, `<|im_end|>`, `<|im_start|>assistant`, `<think>` ↵↵ `</think>`, the answer's first
words (masked), and `<|im_end|>` from the template (GRAY tag "EOS · already there, so the trainer's Adding EOS step
adds nothing"). The empty think block glows; GRAY note "answer without thinking · the same prefix at inference".
SAY: Section 3.5 lets the tokenizer write Qwen's chat template: im start user, the question, im end, im start assistant, an empty think block, and the answer. The empty think block is how Qwen3 answers without thinking, and chat uses the same prefix later.

SHOW: LECTURE 8. TRACKER Data 4: RECORDED(expected/colab-c61-train-test-split.txt: 11–12). TRACKER Data 5: the ribbon
from c63 again. V4 station 5: the ribbon becomes a row of integer boxes; a YELLOW highlighter sweeps every box, question
and markers included, caption "loss on every token". Then the GRAY "your turn" card with a YELLOW `▶ your turn` tag:
"run Part C, Steps 1, 2 and 3 (1.1 to 3.7)"; last line GREEN "T4: free (when available)". 2 s hold. Everything fades
to an empty frame.
SAY: Section 3.6 splits 900 for training and 100 for testing, and 3.7 checks one example. Then the ribbon becomes integers, and the loss covers every token, question and template included. It's still next-word prediction. Pause, and run steps 1 to 3.

---

## S13 · LoRA: a thin correction — `s13_lora.py` · `LowRank`

Lecture: 18–35.

SHOW: LECTURE 18–20. A GREY model block with a snowflake. Three GRAY family cards fan out under "parameter-efficient
fine-tuning": "additive · add small new parts", "selective · train a chosen few", "reparameterization · train a
compact form of the update"; LoRA's card lights GREEN in the third.
SAY: Parameter-efficient fine-tuning trains a small part and freezes the rest. The lecture sorts the methods into three families: additive, selective and reparameterization. LoRA is a reparameterization.

SHOW: LECTURE 23–25. V7's counted cells: a 5 × 5 grid with a counter "25"; a 5 × 1 column and a 1 × 5 row slide out
and multiply back into a 5 × 5 grid, counter "10 · rank 1"; a second column-and-row pair joins, counter "20 · rank 2";
GRAY caption "barely a saving".
SAY: Start small. A 5 by 5 matrix has 25 numbers. A 5 by 1 column times a 1 by 5 row also makes a 5 by 5 matrix, from only 10 numbers. That's rank 1; rank 2 needs 20. At this size it's barely a saving.

SHOW: The grid grows into a large GREY rectangle labelled `q_proj · 2048 × 1024`, counter "2,097,152". Beside it two
GREEN strips, "B · 2048 × 8" and "A · 8 × 1024", drawn at true scale (hairlines); a YELLOW magnifier circle then pulls
each out to a readable width with the GRAY caption "width 8 · magnified"; counter "24,576"; the ratio writes "≈ 1.2 %".
SAY: At real size it's different. Qwen's query projection is a 2,048 by 1,024 matrix: over 2 million numbers. A rank 8 pair of strips, 2,048 by 8 and 8 by 1,024, holds 24,576.

SHOW: LECTURE 26. The equation writes and each symbol lights as named: `W₀ + ΔW = W₀ + (α/r)·B·A`; W₀ GREY with a
snowflake, B and A GREEN. GRAY caption "decompose the update, not the weights".
SAY: So LoRA decomposes the update, not the weights. The new layer is the frozen W naught, plus alpha over r, times B times A. Only B and A are trained.

SHOW: LECTURE 27–30. V7's block diagram (picture before the config): input `x` at the bottom; left, GREY W₀ with a
snowflake; right, the GREEN A → B hourglass (narrow waist "r"), A labelled "random", B labelled "= 0"; both outputs add
into `h` at the top: `h = W₀x + (α/r)·B·A·x`, with the label "α/r" on the right branch. A GRAY chip "lecture: A ~ N(0,
σ²) · PEFT: uniform · both: B·A = 0 at step 0". Forward pass: both branches light from `x` up to `h`; the right branch
adds exactly zero.
SAY: B starts at zero and A at random. The lecture draws A from a normal distribution; the library uses a uniform one. What matters is that B times A starts at exactly zero, so at step zero the model is the pretrained one. Both branches' outputs add.

SHOW: TRACKER Tune 1. CODE(colab/cell-67.py: 2–7) (6 lines, header `QLoRA notebook · 4.1 · cell 67 · lines 2–7`) with
a YELLOW `▶ your turn` tag beside the diagram; `lora_alpha=16` flies a copy onto α and `r=8` onto r in the α/r label
*on the diagram's right branch* (the waist now reads "r = 8"); "α / r = 2" writes; line 3 `lora_dropout=0.1` and
line 6 `task_type="CAUSAL_LM"` light briefly.
SAY: Now the notebook's step 4, the LoRA config: alpha 16 and rank 8, so the update is scaled by 2, plus a dropout of 0.1 for regularization. Pause and run it.

SHOW: The block shrinks into a 28-layer tower; in each block, seven small matrix glyphs, `q_proj` and `v_proj` lit GREEN.
Under one block, one GRAY chip row with each glyph's in + out sizes (source chip `c42`: hidden 1,024, 16 × 128 query,
8 × 128 key-value, intermediate 3,072): "q 1024+2048 · k 1024+1024 · v 1024+1024 · o 2048+1024 · gate 1024+3072 · up
1024+3072 · down 3072+1024", q and v lit GREEN; it stays visible through the ponder. GRAY chip "4.1 names no
target_modules → PEFT's Qwen3 default: q_proj, v_proj". The arithmetic writes:
8 × (1024 + 2048) + 8 × (1024 + 1024) = 40,960 per block; a counter ticks up the tower × 28 to **1,146,880**. A GRAY
`erratum`-style chip "lecture: adapters on each layer · here: two projections per block".
SAY: Which layers? The config names no target modules. So for Qwen3, the PEFT library's default adapts the query and value projections: two of the seven matrices in each of the 28 blocks. That's 40,960 per block, 1,146,880 in all.

SHOW: LECTURE 32–35. A GRAY dashed square "7 B weights as one square · 83,666 × 83,666" beside the tower, arithmetic
under it "rank 1: 2 × 83,666 ≈ 167 K" (the table's first cell), GRAY chip "the lecture's table · one square matrix
(slide 35's own warning)"; the tower and its shape row stay lit. Then the ponder card enters.
SAY: The lecture's table treats a whole model as one square layer; the real count depends on these shapes. Now, try it yourself.
PONDER(8 s, "With r=16, how many trainable parameters? And with target_modules=\"all-linear\" at r = 8?")

SHOW: The ponder card leaves. The counter doubles to 2,293,760 ("linear in r"); then all seven matrices in each block
light, the counter runs to 5,046,272 (8 × 22,528 × 28). A GRAY chip "more rank: more capacity · more memory and time"
and a GRAY chip "trying it? re-run 1.3 (reload the model) before 4.1–4.3". Everything fades to an empty frame.
SAY: Rank 16 doubles it, to 2,293,760. All seven projections at rank 8 give 5,046,272. More rank buys capacity at more memory and time; for a persona, rank 8 on two projections is plenty. To try it, reload the model in 1.3 first.

---

## S14 · Training on a small GPU — `s14_train.py` · `SmallGpu`

Lecture: 13–15, 37–39, 57–72.

SHOW: LECTURE 13–15, 37–39. V5 redrawn for Qwen3-0.6B, tag `estimate` (our arithmetic): left column "full fine-tuning
≈ 7 GB · before activations"; right column "QLoRA in this notebook ≈ 0.9 GB": a thin GREY "4-bit linears 0.22 GB", a
GREY solid "embeddings 0.62 GB" with a small WHITE `FP32` tag, a hairline GREEN "adapters + gradients + Adam ≈ 18 MB".
A GRAY dashed "T4 · 16 GB" outline behind both: both fit; on "fit a T4" both columns pulse inside the T4 outline. On
"scales", S10's GREY dashed 10 B column slides in on the right and overflows the T4 outline far above the frame edge
(top clipped by a GRAY "↑ 120 GB" arrow, `concept · lecture only`).
SAY: Back to the memory column, at Qwen's size, by our own estimate. Full fine-tuning would need about 7 gigabytes before activations; this notebook's QLoRA, under 1. At 0.6 billion parameters, even full fine-tuning would fit a T4. The recipe matters because the same notebook scales to models that wouldn't.

SHOW: LECTURE 57–64. V8: four circles X → h₁ → h₂ → h₃ → ŷ with a memory meter. Forward: each circle fills (stored),
the meter climbs. Checkpointing: all but the checkpoint (h₂) empty, the meter drops; backward: h₃ is recomputed from h₂
(a small replay arrow), the meter stays low; caption "compute for memory". GRAY chip "on since 1.3 (cell 36)".
SAY: The rest of the memory goes to activations, the values each layer computes on the way forward, kept for the backward pass. Gradient checkpointing keeps only a few and recomputes the rest when needed: compute traded for memory.

SHOW: TRACKER Tune 2. CODE(colab/cell-70.py: 2–17) folded to 3, 5–7, 10, 12–13, 15 (8 rows) with a YELLOW `▶ your
turn` tag. Line 3 `max_length=512` and line 15 `group_by_length` light first; then lines 5–6, line 10
`learning_rate=2e-4`, line 7 `optim="paged_adamw_32bit"`. LECTURE 65: V8's paging: pages of optimizer state slide from a
GPU box to a CPU box along PINK arrows when the GPU fills, and back; GRAY footnote "our ≈ 18 MB never needs it".
SAY: Step 2, the training arguments. Sequences are capped at 512 tokens and grouped by length: 2 epochs, batches of 4, and a learning rate of 2 times 10 to the minus 4. The optimizer is a paged 32-bit Adam. Paging moves optimizer state to CPU memory when the GPU fills up. Ours never needs to.

SHOW: LECTURE 66–67. Lines 12–13 `fp16=True`, `bf16=False` light. V8's bit strips: FP32 1 / 8 / 23, FP16 1 / 5 / 10,
BF16 1 / 8 / 7 (sign WHITE, exponent PINK "range", fraction GREEN "precision"); BF16's exponent box matches FP32's.
A GRAY chip "T4: no fast BF16 → FP16 here (lecture: BF16 for QLoRA)"; under it RECORDED(expected/colab-c31-gpu-bf16-
check.txt: 9; wrap) (the saved A100 run supports BF16, yet the notebook keeps FP16 so the same settings run on a T4).
SAY: Then fp16 on and bf16 off. BF16 keeps the range of float 32 with less precision, and the lecture uses it for QLoRA. The T4 has no fast BF16, so this notebook computes in FP16.

SHOW: TRACKER Tune 3. CODE(colab/cell-72.py: 10–14) (5 lines); A and B in the LoRA block flip their dtype tags from
`BF16` to `FP32`. RECORDED(expected/colab-c72-sfttrainer-trainable.txt: 23; wrap); `1146880` lights YELLOW and the S13
counter "1,146,880" flashes beside it: ✓.
SAY: Step 3 builds the trainer. The trainer turns the adapters into BF16, which FP16 training cannot unscale, so this cell casts them back to float 32. And the count confirms our arithmetic: 1,146,880 trainable parameters, 0.3 percent.

SHOW: LECTURE 29, 70. V7's block diagram returns: W₀ greys further; a YELLOW pulse runs down from `h`, passes through
W₀ without changing it (W₀ stays GREY, a snowflake flashes), and reaches B and A, which update (their grids shimmer).
A GRAY chip "lecture: gradients flow only through the adapters · precisely: through W₀ too, but W₀ gets no gradient".
SAY: In the backward pass, the gradient flows down through W naught, and only B and A are updated. W naught is used on the way down; it just gets no gradient and no update.

SHOW: TRACKER Tune 4. RECORDED(expected/colab-c75-train.txt: 5–15) (11 rows); `[450/450 03:36, Epoch 2/2]` lights;
then the output Transforms into a falling curve (each loss value flies to its point, 2.007381 → 1.350437 over steps
50–450), leaving only the curve, the `[450/450 03:36, Epoch 2/2]` line and a GRAY arithmetic chip "900 / 4 × 2 = 450".
No excerpt chip (the SAY gives the T4 time). TRACKER Tune 5: RECORDED(expected/colab-c77-tensorboard.txt: 4) GRAY,
"open it in your own run", replaces the arithmetic chip on the last sentence. YELLOW `▶ your turn`. Everything fades
to an empty frame.
SAY: Step 4, train: 900 examples in batches of 4 for 2 epochs is 450 steps, 3 minutes and 36 seconds on the saved A100 run. The notebook says 6 to 7 minutes on a T4. The loss falls from 2.0 to 1.35. Step 5, TensorBoard, shows these curves in your own run. Pause and train.

---

## S15 · Did it work? Perplexity and the sky — `s15_eval.py` · `DidItWork`

Lecture: 9–10, 36, 40.

SHOW: TRACKER Eval 1. A formula card: "perplexity = exp(mean token loss)"; beside it, a fan of equally likely
next-token boxes shrinks from 14 to 4 as an illustration (tag `illustration`).
SAY: Did it work? Step 1 measures it. Perplexity is the exponential of the average token loss: roughly how many equally likely next tokens the model is choosing among.

SHOW: CODE(colab/cell-80.py: 53–55) (3 lines); line 54 `with trainer.model.disable_adapter():` lights. Then
RECORDED(expected/colab-c80-eval-loss-perplexity.txt: 75–80): `Base (4-bit) 2.6498 14.15` GRAY, `Fine-tuned (4-bit +
LoRA) 1.3872 4.00` GREEN.
SAY: On 100 test examples, 30,681 tokens, the base model has a loss of 2.65 and a perplexity of 14.15. The fine-tuned model: 1.39, and a perplexity of 4.

SHOW: LECTURE 36, then 9–10. V1's weights dial returns, now a switch labelled `disable_adapter()`; flipping it slides the
GREEN A/B block out of V7's mini block diagram, W₀ (snowflake) untouched; flipping back slides it in. A GRAY lecture
chip "catastrophic forgetting · LoRA forgets less".
SAY: The base row is the same model inside disable adapter. Switch the adapter off and the original model, in 4 bits, is back, because W naught never changed. That's the lecture's point about catastrophic forgetting, losing old skills while learning new ones: with LoRA, the old model is one switch away.

SHOW: An illustrative first-word bar chart (tag `illustration`, no numbers on its axis) after the empty think block
(the prompt uses `enable_thinking=False`, `cell-82.py` lines 19–27): adapter off, one tall bar "The" plus two
unlabeled GRAY bars; adapter on, they collapse onto "Welcome", "Yello". A GRAY chip "saved run: base answers start
"The" · fine-tuned: "Welcome" / "Yello" (5.2)". The measured loss table from c80 sits small beside it.
SAY: In the saved run, every base answer starts with the word the. The fine-tuned ones start with welcome or Yello, the openers of its training data. Those bars are an illustration; the measured numbers sit beside them.

SHOW: The ribbon from S12 with the YELLOW highlighter over every token, questions and markers included; a GRAY card
"what the drop says: this style is what it now expects" and a RED-outlined card "what it does not say: the answers are
more correct".
SAY: What does the drop measure? The loss counts every token, questions and template included. It says this style is what the model now expects, not that its answers are more correct.

SHOW: TRACKER Eval 2. RECORDED(expected/colab-c82-base-vs-finetuned.txt: 119, 131 cut after "cheese lovers! This is
your lecturer ‹instructor›", 138 cut after "piccante'", 146 cut after "‹instructor›") (wrap, 8 rows); both fine-tuned
openers light BLUE. Then the sky pair from S01 returns: RECORDED(…: 148, 156 cut after "(refracts)", 159 cut after "sky's
blue!"), the two RED ✗ and the GREEN tick on the voice. Then the GRAY "your turn" card with a YELLOW `▶ your turn`
tag: "run Step 5 (5.1, 5.2)"; last line GREEN "T4: free (when available)". 2 s hold.
SAY: Step 2 compares answers. Both cheese answers now open with welcome welcome welcome, cheese lovers, in the instructor's voice. And the sky: the voice transferred, the physics did not. Pause, and run step 5.

SHOW: LECTURE 40. Two GRAY chips: "loss table: the 4-bit model, adapter off" and "side by side: a fresh 16-bit
model" with a GRAY note "two different baselines". Then a GRAY redrawn bar pair "LoRA ≈ full fine-tuning on a
published benchmark" (no screenshot, no numbers) beside a GREEN chip "this notebook: style fit, not answer quality".
Everything fades to an empty frame.
SAY: Two kind notes. In this comparison the base is a fresh 16-bit model, not the 4-bit one from the table, so the baselines differ. And the lecture shows LoRA matching full fine-tuning on a published benchmark; this notebook measures style fit, not answer quality.

---

## S16 · Ship it, tear down, recap — `s16_recap.py` · `Recap`

Lecture: 30, 41, 52–53, 71–72.

SHOW: TRACKER Save 1. CODE(colab/cell-84.py: 1–5) (5 lines) with a YELLOW `▶ your turn` tag;
RECORDED(expected/colab-c84-save-adapters.txt: 8–10; wrap) (the folder `LLM_cache/Qwen0.6B-finetune_cheese`); V7's GREEN
A/B block drops into a GREY Drive folder as a GREEN file "≈ 4.6 MB · float 32" (source chip "QLoRA notebook · 6.1").
SAY: The notebook's step 6 saves your work. First the adapters: 1,146,880 numbers, about 4.6 megabytes in float 32, saved to your Drive with the tokenizer.

SHOW: LECTURE 30. TRACKER Save 2. CODE(colab/cell-86.py: 1–11) folded to 1–5, 9, 11 (7 rows); line 4 `dtype=torch.float16`
lights. V7 merge: a fresh GREY W₀ (tag `FP16`) loads; B·A slides over and fuses into it; the snowflake melts, the block
turns into one "merged model · ≈ 1.2 GB" (GREEN outline). A GRAY chip "not into the 4-bit weights: the update would
round back onto 16 levels". RECORDED(expected/colab-c86-merge-and-save.txt: 26 cut after "_merged"). A GRAY chip
"torchao ImportError here? run the install cell, restart the session".
SAY: Then the merge. The notebook loads a fresh 16-bit copy of the base and adds B times A into it. Not into the 4-bit weights: there, the update would round back onto 16 levels. The merged model is about 1.2 gigabytes.

SHOW: TRACKER Save 3. RECORDED(expected/colab-c88-push-to-hub.txt: 31) (`‹hf-user›` GRAY chip), tag "optional · private
repo · token with write role". Then three cards side by side: GREEN "adapter · 4.6 MB · needs its base", GREEN-outlined
"merged model · stands alone", BLUE "endpoint (track A) · no weights in your hands" with a GREY dashed arrow to "L10 ·
cheese app".
SAY: Step 3 can push the merged model to a private Hugging Face repository. So you can ship three things: an adapter that needs its base, a merged model that stands alone, or Google's endpoint, with no weights in your hands.

SHOW: TRACKER Down 1. Full TEAL terminal at `app@2a2550dec953:/app$` types `exit` → TERM(laptop/18-docker-shell-gemini-
finetuner.txt: 28); the frame turns GRAY. It types `cd ..` → (no output). TRACKER Down 2: `docker image rm
llm-dataset-creator gemini-finetuner` → TERM(laptop/22-x-image-rm.txt: 2–5 cut after 20 hex characters). Then the
terminal shrinks; a teardown checklist writes, items ticking as named: TRACKER Down 3, GOLD "bucket:
`gcloud storage rm -r gs://<your-bucket>/llm-finetune-dataset-small` (shown, not run here)"; GOLD "tuned model + endpoint:
keep for L10, then delete in the console"; GOLD key glyph "delete unused service-account keys"; TRACKER Down 4, GOLD
"Colab: Runtime › Disconnect and delete runtime"; GRAY "optional: MyDrive/LLM_cache"; GRAY `extra` "optional: `docker
image rm python:3.12-slim-bookworm` (if no other lecture uses it; `laptop/19` line 5, shown, not run here)". Then the
GRAY "your turn" card with a YELLOW `▶ your turn` tag: `exit` · `docker image rm llm-dataset-creator gemini-finetuner`
· bucket folder · service-account keys · Colab runtime; last line GOLD "after this: nothing billed except what you
keep for L10". 2 s hold.
SAY: Teardown. Exit the container and remove both images with docker image rm. Delete the dataset folder in your bucket. Keep the tuned model and endpoint for lecture 10, then delete them. Delete unused service account keys, and disconnect and delete the Colab runtime. Pause, and tear down.

SHOW: LECTURE 71–72. A content recap built from the set pieces, each shrinking in from its own chapter as named: V1's
three dials (the weights dial turned); V3/V4's teacher → brick → JSONL ribbon; V5's three columns 120 → ≈ 40 → ≈ 12
GB (GRAY tag "the lecture's totals" on 40 and 12) with V7's thin GREEN A/B strips beside the frozen GREY W₀. Under
the QLoRA column, a small plain series-style circle (no cartoon, LECTURE 52–53, unspoken) with two labels "dough ·
NF4" and "cheese · paged optimizer", caption "the lecture's QLoRA pizza".
SAY: Here's where we are. Prompts and retrieval change the input; fine-tuning changes the weights, and here it taught a voice, not facts. In track A, a teacher wrote the data and Google tuned the model. In track B, QLoRA froze a 4-bit base and trained two thin matrices: 120, then 40, then 12 gigabytes.

SHOW: Recap questions, one at a time, YELLOW numbers, no timer (answers in exercises.md): 1 "What did this fine-tune
change, and what not? (the sky)"; 2 "Why did --generate exit 0 without a key?"; 3 "Which shapes does one pair take
on its way to the chat template?"; 4 "Why does --train print Tuned model info: None?"; 5 "Where does 1,146,880 come
from, and what does QLoRA keep in GPU memory here?"
SAY: Five questions to test yourself. What did this fine-tune change, and what not? Why did generate exit zero without a key? Which shapes does one pair take on its way to the template? Why does train print tuned model info, none? And where does 1,146,880 come from?

SHOW: Two GREY dashed cards "next: L09 · testing code" and "L10 · the cheese app calls your endpoint"; footer "study
guide and exercises: MLOps_Learning · guides/L08-llm-finetuning.md". Everything fades to an empty frame.
SAY: Next, lecture 9 tests code, and in lecture 10 an app calls your endpoint. The study guide and the exercises are in MLOps Learning.
