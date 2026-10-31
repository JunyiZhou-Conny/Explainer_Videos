# Brief · AC215 L8 — LLM: Finetuning (follow-along: llm-finetuning)

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the tutorial digest), `SLIDES.md` (the lecture; binding next to the digest,
series rule 9) and `assets/` (real captures, see `ASSETS.md`). **Where the digest and the captures
disagree, the captures win.** They are newer (2026-10-31, 02:35–02:37 UTC; `main` still at the
pinned commit `44ef6f0`, `laptop/02`) and were made on the machines the video shows: a fresh Docker
Engine as "your laptop" (user `student`, host `laptop`, workspace `~/AC215`) and the repo's own
images, built unchanged by `sh docker-shell.sh`. There was **no service-account key and no GPU**:
every README command was typed exactly as written, in README order; every command that talks to
Google ran for real up to its first request and failed there, and those failures are kept as
instructive. What a working key prints comes from the README (tag `expected`); the Colab QLoRA run
comes from the notebook's stored outputs (an A100 run, tag `recorded`); `--prepare` also ran for
real on a small hand-written Q&A set (tag `scripted`).

| topic | digest | captures (use these) |
| --- | --- | --- |
| `--generate` without a key | errors "caught and printed per batch" | confirmed, word for word: five `Error occurred while generating content: File /secrets/llm-service-account.json was not found.`, **`[exit 0]`** (`dataset-creator/05:4-14`) |
| `--prepare` after that | `Shape: (0, 0)`, `KeyError: 'question'` (reasoned with pandas) | confirmed (`07:4-23`, exit 1, traceback at `cli.py` line 243); it has already written a 1-byte `instruct-dataset.csv` (`laptop/13`) |
| `--prepare` with data | `Shape: (N, 2)`, N ≈ 100 | on the 20 **scripted** pairs: `Shape: (19, 2)` (one duplicate question dropped), 17 train / 2 test lines (`09:4-17`, `10`) |
| `--upload`, `--train`, `--chat` without a key | 403/404 cases for a wrong bucket or endpoint | the real no-key failure for all three: `google.auth.exceptions.DefaultCredentialsError: File /secrets/llm-service-account.json was not found.` (`14:36`, `gemini-finetuner/02:69`, `03:66`); `--train` first prints google-genai's `ExperimentalWarning` (`02:4-5`); `--chat` prints the query and `Using serving location: us` before failing (`03:4-5`). Nothing reached Google |
| success output of `--upload` / `--train` | the shapes from the code's `print` lines | **not documented anywhere**: no output panel; the scene shows the command and says what to look for |
| `sh docker-shell.sh` | fails on dash | works on this laptop (BusyBox `sh`, like macOS); the dash failure is captured as an extra: `docker-shell.sh: 8: source: not found`, exit 127 (`laptop/20`) |
| the `(app)` prefix | "may not show" | it never shows: `app@6f5113cdb660:/app$` (`laptop/07:27`); a `docker exec` shell has no venv at all (`laptop/12`: `ModuleNotFoundError: No module named 'pandas'`) |
| second build | "fast" | `Building 0.0s`, every layer `CACHED` up to `uv sync` (`laptop/18`); the two folders' `Dockerfile`, `pyproject.toml`, `uv.lock` are identical (`laptop/16`) |
| image size and build time | "several minutes", not measured | `1.64GB` (`laptop/09:3`), `/.venv` 587 MB, 133 packages (`dataset-creator/02`); `Building 45.1s` here with a fast network — say "a few minutes on a laptop" |
| versions | Python 3.12.x, uv unpinned | Python 3.12.16, uv 0.13.6, google-genai 1.39.1, google-auth 2.41.1, pandas 2.3.3 (`laptop/07:24-25`, `dataset-creator/02`); Colab run: Python 3.13.15, torch 2.11.0+cu128, transformers 5.16.1, peft 0.20.0, trl 1.14.0, bitsandbytes 0.50.2 (`c08`, `c12`) |
| the chat query | "How is cheese made in Greece? Answer ‹persona› style?" | confirmed (`03:4`); the README's example still asks the older "How is cheese made?" (`readme-chat-example.txt`) |
| a T4 measurement | proposed (SLIDES.md) | **none**: no GPU here. The video has no measured T4 numbers; the 0.6 B memory figures are an estimate, labelled so |

Capture references below are `folder/file:lines` under `assets/terminal/` (`dc/` = `dataset-creator/`,
`gf/` = `gemini-finetuner/`, `cNN` = `expected/colab-cNN-….txt`, `readme-…` = `expected/readme-….txt`).

## Audience and goal

An AC215 student who has done L1–L7: uv, `pyproject.toml` and `uv.lock` (L1); containers, images,
bind mounts and `docker-shell.sh` (L2–L4); L05's RAG with the same `llm-service-account` and the same
`secrets/` folder; L06–L07's structured outputs. Knows basic ML (a loss, an optimizer, a training
loop) and has heard "LoRA" but never seen its arithmetic. They watch with `~/AC215/llm-finetuning`
open and Docker running, optionally with a GCP project with billing and the service-account key,
and the course Colab notebook open in another tab, pausing to type each command.

After the video they can:
- say what fine-tuning changes and what it doesn't: prompting and RAG change the input, fine-tuning
  changes the weights; it reliably teaches **style and habits** (the lecture's "Sure, here's…",
  the tutorial's persona openers), not facts — with the stored sky-blue answer as evidence;
- set up Track A: the service account and its two roles, the key as `secrets/llm-service-account.json`
  **next to** the clone, the three places to edit (`env.dev:6-7`, `gemini-finetuner/cli.py:10-11`,
  `:107`), a bucket of their own; run `sh docker-shell.sh` (or `bash` on Linux/WSL) in each folder
  and check the key with `ls -la /secrets`;
- explain how `dataset-creator` manufactures an **instruction dataset** with a teacher model: system
  instruction, input prompt, JSON schema, five batches; read `--generate`'s per-batch errors and know
  why the failure surfaces one command later as `KeyError: 'question'`;
- follow one Q&A pair through its shapes: CSV row → `human:/bot:` text → Gemini JSONL line → (in
  Colab) Qwen3 chat-template text → tokens; say what `--prepare` writes and why the split is 90/10;
- describe the managed tuning job: one request creates a job in `us-central1`; Google trains; the
  result is an endpoint in multi-region `us`; why `--train` prints `Tuned model info: None`, where to
  find the endpoint and what to paste into `cli.py:107`; read the README's (stale) cost table;
- explain the lecture's **memory ladder** for a 10 B model, 120 GB → ~40 GB → ~12 GB, and which
  technique removes which bar;
- explain **quantization** with absmax scaling and its round-trip error, per-block constants, NF4's 16
  quantile levels, double quantization, and "stored in 4 bits, computed in 16"; solve the 375.8 M
  puzzle;
- explain **LoRA**: `W₀ + (α/r)·B·A`, B starts at zero, the adapter runs beside the frozen layer; derive
  1,146,880 from r = 8 on `q_proj`/`v_proj` in 28 layers;
- read the notebook's training settings (gradient checkpointing, `paged_adamw_32bit`, fp16 with fp32
  adapters) and its evaluation (loss and perplexity with `disable_adapter()`), and say what a
  perplexity drop does not prove;
- name the three things you can ship (a 4.6 MB adapter, a merged FP16 model, a managed endpoint) and
  tear everything down.

## Length and parts

~30 minutes. Narration **~4,070 words** (3,900–4,300; Kokoro af_heart, speed 0.9 ≈ 174 wpm ≈ 23.4
min of speech); typing, real output, five ponders and expected/recorded cards add ~6–7 min. The
tutorial has two tracks: the README (Track A, two containers, a managed Gemini tuning job) and the
course Colab (Track B, QLoRA by hand). The lecture is the theory of Track B. Both get full weight.

The cut falls where the tutorial changes tracks — the end of the README, the start of the Colab:
- **Part 1 = S01–S09, Track A: a persona dataset and a managed tuning job** (~2,220 words, ~12.8 min
  of narration, ~16 min). It ends on "you never saw a single weight", and the promise: "in part 2 the
  weights are in your hands". Clean frame.
- **Part 2 = S10–S16, Track B: QLoRA in Colab** (~1,850 words, ~10.6 min, ~14 min): the memory bill,
  quantization, the dataset in Qwen's template, LoRA, training on a small GPU, evaluation, shipping,
  teardown and recap. It opens in the Colab tab.

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 240 | S10 MemoryBill | 250 |
| S02 ThreeDials | 220 | S11 Buckets | 290 |
| S03 KeyNextToRepo | 250 | S12 QwenInFourBits | 250 |
| S04 DatasetContainer | 260 | S13 LowRank | 290 |
| S05 Persona | 270 | S14 SmallGpu | 270 |
| S06 LateFailure | 250 | S15 DidItWork | 250 |
| S07 RowsToJsonl | 230 | S16 Recap | 250 |
| S08 TuningJob | 280 | | |
| S09 CostAndChat | 220 | | |
| **part 1** | **2,220** | **part 2** | **1,850** |

Word budgets are targets (±15 %); the total must stay inside 3,900–4,300.

## The lecture behind the tutorial (SLIDES.md)

One deck, "Lecture 8: LLM Finetuning", slides 1–73 (cite PDF page numbers, never the printed
footers). It is concept-only and covers Track B's ideas: instruction tuning, full fine-tuning's
memory bill, PEFT and LoRA, quantization and QLoRA. **Track A is not on the slides** (no Gemini,
Vertex AI / Agent Platform, Docker or endpoints); the only shared idea is the instruction dataset
(4–5). S01 says once what the GREY `lecture_ref` tag means. The two recurring pictures of part 2 come
from the deck: the **GPU-memory column** (slides 14, 37–39, 71–72: V5) and the **LoRA block diagram**
(28–30, 66–70: V7). Every lecture diagram is redrawn in the series style; no slide image, meme,
the GPT-4 cost aside (11–12), the results-table screenshot (40) or the dataset screenshot (5) appears.

| scene | slides | used for |
| --- | --- | --- |
| S01 | 7–8 | a learned opener ("Sure, here's…") — the persona is the same effect, on purpose |
| S02 | 4–8 | fine-tuning usually means instruction fine-tuning (4); task-specific fine-tuning (6); a tuned model vs plain next-word prediction (7–8) |
| S03, S04 | none | |
| S05 | 4–5 | the instruction dataset: instruction / context / output → the tutorial's question / answer |
| S06 | 5 | the card again, now as a CSV row |
| S07 | 5, then 8 | the row becomes a training line; training is still next-word prediction |
| S08 | 13–16 | one beat: the 120 GB bill becomes Google's problem |
| S09 | none | |
| S10 | 11–16, 37–39, 71–72 | the memory ladder 120 → ~40 → ~12 GB |
| S11 | 43–55, 68–69 | buckets, absmax worked example, dequantization error, NF4, stored in NF4 / computed in 16 bits |
| S12 | 68–69, then 8 | the 4-bit base in code; next-word prediction over the whole chat-template ribbon |
| S13 | 18–35 | PEFT families, low-rank counting, the LoRA equation, initialization, block diagram, parameter table |
| S14 | 13–15, 37–39, 57–72 | the ladder at 0.6 B, gradient checkpointing, paged optimizer, FP16 vs BF16, QLoRA's backward pass |
| S15 | 9–10, 36, 40 | catastrophic forgetting; "LoRA forgets less" as the adapter switch; LoRA ≈ full fine-tuning on a benchmark |
| S16 | 30, 41, 52–53, 71–72 | merge at inference; summary; the pizza (dough = NF4, cheese = paged optimizer) |

Where the slides and the tutorial disagree, the scene shows the notebook's or the library's version
and the narration says so kindly in one sentence (SLIDES.md "Conflicts"):

| # | slides | tutorial (notebook / library) | scene |
| --- | --- | --- | --- |
| 1 | QLoRA computes in **BF16**, adapters BF16 (66–70, 72) | `bnb_4bit_compute_dtype="float16"`, `fp16=True` (`cell-34.py:4`, `cell-70.py:12-13`) so T4s work; adapters cast back to **fp32** (`cell-72.py:10-14`); `c31`: "still trains in float16" | S11 (tag the dtypes as the notebook sets them), S14 (bit strips) |
| 2 | double quantization skipped (53, sticky note) | `bnb_4bit_use_double_quant=True` (`cell-18.py:10`, `cell-34.py:5`) | S11 |
| 3 | A = N(0, σ²), B = 0 (27–30) | PEFT's default draws A Kaiming-uniform; B = 0. Both start with ΔW = 0 | S13 (label A "random") |
| 4 | adapters on "each layer" (22, 41); the table treats a model as one square layer (32–35) | PEFT's Qwen3 default: `q_proj` and `v_proj` in each of 28 layers (`cell-67.py` sets no `target_modules`) | S13 |
| 5 | one absmax constant for the whole array, Int8 (45–51) | one absmax per small block, 16 NF4 levels | S11 |
| 6 | the backward pass "doesn't use" W₀ (29, 70) | W₀ gets no gradient and no update; the signal still passes through it | S14 (W₀ greys, the pulse passes through) |
| 7 | merge the update into the weights (30) | merged into a freshly loaded **FP16** base, not the 4-bit one (`cell-86.py:1-11`) | S16 |
| 8 | higher rank, better performance (25) | more capacity at more memory and time (notebook Poll 3) | S13 |

Slide slips are not copied: slide 50's 18 and 69 are **19** and **70** when rounded; slide 44 floors
where the example rounds (the scene rounds throughout); slide 23's "any matrix" is exact only at
full rank; slide 38's "100 GB optimizer state" includes the gradients (keep slide 14's 20/20/80
split). SLIDES.md's gaps adopted: the memory ladder (gap 1: S10, S14, S16), the learned opener (gap 2:
S01, S02), absmax worked (gap 3: S11), checkpointing and paging as mechanisms (gap 4: S14), the block
diagram reused three times (gap 5: S13, S14, S16), "peel off the adapter" (gap 6: S15), the table vs
the real count (gap 7: S13), BF16 vs FP16 (gap 8: S14), PEFT families (gap 9: S13), slide 40 (gap 10:
S15, one line). Not used: gap 11 (Alpaca-GPT4's provenance, unchecked), slide 10, 11–12, the memes.

Terms: the lecture's words — *instruction fine-tuning*, *instruction dataset*, *task-specific
fine-tuning*, *catastrophic forgetting*, *full-parameter fine-tuning*, *PEFT*, *update matrices* /
*adapters*, *rank r*, *scaling parameter α*, *pretrained weights W₀*, *merge*, *quantization*
("splitting a range into buckets"), *absmax*, *dequantize*, *4-bit NormalFloat (NF4)*, *gradient
checkpointing*, *paged optimizer*, *BF16*, *forward pass*, *backward pass* — and the tutorial's where
the lecture stops: *system instruction*, *response schema*, *Gemini JSONL*, *chat template*, *EOS*,
*compute dtype*, *double quantization*, `target_modules`, *trainable params*, *perplexity*,
`disable_adapter()`, *merged model*, *tuning job*, *endpoint*, *adapter size*. Qualify, don't repeat
loosely: "each layer" (each block, two projections); "A ~ N(0, σ²)" ("A random"); "BF16" (FP16 in
this notebook); "doesn't use W₀" (W₀ gets no gradient); "higher rank, better" (more capacity, more
cost); "merge into the weights" (into a 16-bit copy). `ADAPTER_SIZE_FOUR` is never called a LoRA rank
as fact ("an adapter of size four — Google's managed version of the same idea, by our reading").

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop: `~/AC215`, the clone, `secrets/`, `dataset-creator/data/` seen from the host, the laptop terminal, the browser tab | GREY |
| the cloud: Google Cloud and its three locations (`global` generation, `us-central1` tuning, multi-region `us` serving), the bucket, the tuning job and the endpoint; the Colab VM and its GPU; **everything a model writes** — the teacher's Q&A pairs, generated answers. The hand-written stand-ins sit in the same seat drawn BLUE **dashed** with the `scripted` tag | BLUE |
| the containers and images `llm-dataset-creator` and `gemini-finetuner`: `/app`, `/.venv`, the build | TEAL |
| the base image's own Python and apt packages (`python:3.12-slim-bookworm`, `build-essential curl libpq5`; only S04) | ORANGE |
| what you own: `uv.lock` and the pinned versions; **your dataset files** (`instruct-dataset.csv`, `train.jsonl`, `test.jsonl`); **the LoRA adapters A and B** (the 4.6 MB you train, save and keep) | GREEN |
| tools and libraries you install: Docker, uv, the google-genai SDK, bitsandbytes, peft, trl, transformers | PURPLE |
| errors and "avoid this": the missing-key errors, `KeyError`, `source: not found`, quantization error, out-of-memory, the ✗ on a wrong physics claim | RED |
| your turn, the trackers, "look here now"; the gradient pulse in the backward pass (the thing moving now) | YELLOW |
| money: the tuning bill, generation calls, the cost table, Colab compute units; the service-account **key glyph** (never a value) | GOLD |
| routes and lookups: bind mounts, `gs://` URIs, the three hosts, the endpoint path, the GPU ↔ CPU paging arrows | PINK |
| frozen pretrained weights **W₀** (with a snowflake): there is no laptop in part 2, so GREY here means "not yours to change"; lecture-only scale (a 10 B model, 4090 tiles), future lectures (L10) and the persona chip `‹instructor›` | GREY (W₀ solid with snowflake; lecture-only and future GREY dashed) |

dtype tags (`NF4`, `FP16`, `FP32`, `BF16`) are small neutral white labels on whatever they describe;
the deck's blue W₀ and orange adapters are not copied (here BLUE is the cloud and ORANGE is OS-owned).
Bit strips in S14 use sign / exponent / fraction in WHITE / PINK / GREEN outlines (range / precision),
not the semantic colours.

## Running example

- **Laptop:** user `student`, host `laptop`: `student@laptop:~/AC215$`, then
  `student@laptop:~/AC215/llm-finetuning/dataset-creator$` (prompt `\u@\h:\w\$`, `capture.sh:72-73`);
  S03 says once that their prompt shows their own user and machine.
- **Containers:** `app@6f5113cdb660:/app$` (dataset-creator, `laptop/07:27`) and `app@2a2550dec953:/app$`
  (gemini-finetuner, `laptop/18`); S04 says once that the part after `app@` is the container id and
  changes every run.
- **The scripted data:** `capture-only/scripted/cheese_qa_{0..4}.txt`, five files of four pairs,
  hand-written in the shape `--generate` writes, openers from the current prompt ("Good question",
  "Glad you ask", "I have slides for that" …), the last pair repeating the first question on purpose.
  Always tagged `scripted`; never called Gemini's output; said to be 20 pairs where Gemini would write
  about 100.
- **The Colab:** "Tutorial - Finetuning with QLoRA", Qwen/Qwen3-0.6B, 900 train / 100 test examples
  from the 16k file, r = 8, α = 16, 2 epochs, 450 steps; stored outputs from an A100 (say "the course
  staff's saved run, on an A100").
- **Names.** The persona is the instructor's first name. On screen every occurrence is the GREY chip
  `‹instructor›` (`expected/` files are already masked); the narration says "the instructor" or "the
  instructor's voice". `scenes/common.py` gets an `unname(text)` helper that masks the persona name
  case-insensitively in every panel line read from an unmasked file: `gf/03:4` (the query),
  `source/gemini-finetuner/cli.redacted.py:56` (`tuned_model_display_name="‹instructor›-cheese-demo-v3.1"`)
  and `:109`, `source/dataset-creator/cli.py` (every line that names the persona: `:36`, `:52`, `:70`,
  `:84`, `:90`, `:96`, `:108`, `:133`, `:137`, `:140`, `:169`), `README.md:112`, `:117-121`, `:124`, `:130`,
  `:144`, `:167`, `:171`, `:206`, `:300`, `:303`, `source/colab/cell-50.md:4-5`.
  The full name never appears (README.md:118-119, :167 and `cli.py:133`, :140 hold it: those lines are
  never quoted, even masked, beyond the opener's first words). The Hugging Face account in `c88` is `‹hf-user›`. The endpoint at `cli.py:107` is
  only ever the redacted `projects/‹instructor-project-number›/locations/us/endpoints/‹endpoint-id›`.

## Visual set pieces (the 3Blue1Brown part)

- **V1 · Three dials (S02, S15).** A model box with three dials: *prompt*, *context*, *weights*.
  Turning *prompt* (a system prompt card) or *context* (L05's retrieved chunks, PINK) changes the text
  going in; the box stays the same. Turning *weights* morphs the box itself (its grid of numbers
  shimmers). Then the sky question goes through the fine-tuned box: the answer bubble changes voice
  (an `‹instructor›` chip and "Yello…" opener appear) while its content arrow still points at "water
  molecules" with a RED ✗. Slide 8's contrast on the same stage: OPT-350m just continues "Hello my
  cheese name is cheese. / I'm not sure if you're joking or not." (`c27:11-13`). In S15 the *weights*
  dial becomes the `disable_adapter()` switch: an illustrative next-token bar chart (tag
  `illustration`) after `<|im_start|>assistant`, spread over "The", "Sure", "**" with the adapter off,
  collapsing onto "Welcome", "Yello", "Remember" with it on; the measured numbers sit beside it.
- **V2 · The stage (S03, S04, S07–S09).** Left: the GREY laptop — `~/AC215` holding `llm-finetuning/`
  and `secrets/` side by side (README.md:54-62), a GOLD key glyph in `secrets/` (empty in our capture:
  a dashed outline), `env.dev` feeding both folders. Middle: two TEAL containers built from one recipe
  (the same Dockerfile, `pyproject.toml`, `uv.lock`), PINK bind mounts `dataset-creator → /app`,
  `secrets → /secrets`; no port arrows. Right: the BLUE cloud with three pins and their hosts — `global`
  (the Gemini teacher), a bucket `gs://<your bucket>/llm-finetune-dataset-small/`, `us-central1` (the
  tuning job), `us` (the endpoint). Each Track A command lights its own PINK route: `--generate` → global;
  `--upload` → bucket; `--train` → us-central1, and the job's own arrow from the bucket (it reads your
  data itself, not through your container); `--chat` → us. In the capture every route stops at the
  container wall with a RED "no key" stamp.
- **V3 · Teacher, mould and bricks (S05, S06).** A BLUE teacher model takes two cards: the system
  instruction (persona, openers, content rules; `cli.py:36-145`) and the input prompt ("Generate 20 …",
  `:169`). Its answer pours through a mould shaped by the JSON schema (`:146-160`) and drops out as
  `{question, answer}` bricks; five batches stack (`NUM_ITERATIONS = 5`, `:170`). The no-key variant
  (S06): each batch's error is a RED spark caught in a net labelled `except Exception` (`:200-201`); the
  pile stays empty; the exit code shows a calm `0`. One command later the empty pile meets
  `output_pairs_df["question"]` and the RED `KeyError` lands — "the error was there all along; the net
  moved it". The lecture's three-part card (instruction / context / output, slide 5) fades its context
  slot to become the tutorial's two-part brick.
- **V4 · One pair, five shapes (S06, S07, S12).** One brick rides a conveyor. Station 1: a CSV row
  `question,answer` (`instruct-dataset.csv`). Station 2: `human: … \nbot: …` (`train.csv`, for older HF
  tools; Track A doesn't use it). Station 3: the Gemini JSONL line with nested `contents` / `role` /
  `parts` / `text` (real line `dc/11`, pretty `dc/12`); a 90/10 splitter sends 17 to `train.jsonl`, 2 to
  `test.jsonl`. Part 2 picks it up (S12): the Colab samples rows in exactly this format (`c53`), and
  station 4 turns it into Qwen3's chat template (`c63`): `<|im_start|>user … <|im_end|>`,
  `<|im_start|>assistant`, an empty `<think></think>`, the answer, `<|im_end|>` — bright markers on a
  ribbon. Station 5: the ribbon becomes integers, and a YELLOW highlighter sweeps every token, question
  included (loss on all tokens).
- **V5 · The memory column (S10, S14, S16).** Slide 14's stack for a 10 B model in proportion
  1 : 1 : 4 — Parameters (FP16) 20 GB, Gradients (FP16) 20 GB, Optimizer states (FP32, momentum +
  variance) 80 GB — pours into 24 GB GREY dashed GPU tiles: five of them. LoRA (37–39): gradients and
  optimizer states shrink to two small GREEN A/B blocks, the 20 GB base stays ("frozen, but it must sit in
  memory for the forward pass"): ~40 GB. QLoRA (72): the base shrinks to a 4-bit block, optimizer
  pages get PINK arrows to a CPU box: ~12 GB. The three totals line up: 120 → ~40 → ~12. In S14 the same
  column is redrawn for Qwen3-0.6B with our arithmetic, tagged `estimate`: full fine-tuning ≈ 7 GB
  before activations; the notebook's QLoRA ≈ 0.9 GB (0.22 GB 4-bit linears + 0.62 GB fp32 embeddings +
  ~18 MB adapters, their gradients and Adam states). Honest consequence, said: at 0.6 B even full
  fine-tuning would fit a 16 GB T4; the recipe is what lets the same notebook scale.
- **V6 · Buckets (S11).** (a) Slide 44: three dots (27, 55.3, 83.78) fall through a fine grid (whole
  numbers: 27, 55, 84 — rounded) and a coarse one (tens: 30, 60, 80) while a bits counter drops.
  (b) Slides 45–51: ten values 1.5 … 10.2 on a line; a scale `c = 127 / 10.2 = 12.4509` stretches them
  until 10.2 touches the 127 wall; each snaps to an integer: **19**, 29, 46, 51, **70**, 85, 98, 105, 115,
  127; dividing back gives 1.526 and 5.622 — the RED gaps are the dequantization error. (c) Per block:
  the long row of weights splits into blocks of 64, each with its own small absmax knob, so one big
  weight no longer squashes everyone's precision (Conflict 5). (d) Slides 54–55: a bell-shaped histogram;
  16 lines drop evenly spaced, then slide into NF4's quantile positions (crowded near 0, sparse in the
  tails), equal shaded areas; each weight dot snaps to its line and its label shrinks from a 32-bit
  float to a 4-bit index. (e) Double quantization: the row of knobs gets quantized too (Conflict 2).
  (f) Slides 68–69: the 4-bit block "inflates" into a 16-bit copy (tag `FP16`, Conflict 1) for one
  matrix multiply and deflates again.
- **V7 · The LoRA block diagram (S13, S14, S16).** First the counted cells (23–25): a 5×5 grid (25)
  = 5×1 × 1×5 (10) at rank 1, 20 at rank 2 — barely a saving; then the same picture at real size,
  `q_proj` as a 2048×1024 rectangle (2,097,152) beside two thin GREEN strips 2048×8 and 8×1024 (24,576).
  The equation `W₀ + ΔW = W₀ + (α/r)·B·A` lights each symbol as it is named (26); `lora_alpha=16` and
  `r=8` from `cell-67.py:2,4` pin onto α and r (α/r = 2). The diagram (28): input `x` at the bottom,
  GREY W₀ with a snowflake on the left, the GREEN A → B hourglass (width r, "A random", "B = 0") on the
  right, outputs adding into `h`. Forward pass: both branches light. Then the 28-layer tower with q and
  v lit in each block, a counter ticking to **1,146,880** (`c72`). S14: the backward pass — W₀ greys
  further, a YELLOW pulse runs down from `h`, through W₀ without changing it, into A and B (Conflict 6).
  S16: B·A slides over and fuses into a freshly loaded FP16 copy of W₀ (Conflict 7) — the merged model.
- **V8 · Memory under pressure (S14).** Slides 58–64: X → h₁ → h₂ → h₃ → ŷ as four circles with a
  memory meter. Forward: each fills (stored), meter climbs. Checkpointing: all but the checkpoint
  empty; backward: h₃ is recomputed from h₂ (a small replay arrow), meter stays low ("compute for
  memory"). Slide 65: pages of optimizer state slide from a GPU box to a CPU box along PINK arrows when
  the GPU is full and come back when needed; then the honest footnote: our ~18 MB never needs it.
  Slides 66–67: three bit strips — FP32 (1/8/23), FP16 (1/5/10), BF16 (1/8/7) — exponent = range,
  fraction = precision; the T4 has no fast BF16, so the notebook uses FP16 and keeps A and B in fp32.

## README step tracker (top-left)

Step titles ≤ 3 words. The factory in `common.py` sets the head ("README", or "Colab" for the course
notebook). Steps the README does not have are marked `extra` in the caption and the narration.

`dlops-io/llm-finetuning` `README.md` @ `44ef6f0` (the whole README is L08's) and the Colab:
- *Prerequisites* (`:31-69`), label "Prerequisites": Clone repo (`extra`; `:34` links it) · Service
  account (`:38-49`, illustration) · Secrets folder (`:50`) · Edit env.dev (`extra`) (4)
- *Generate Question Answer Dataset › Run Container* (`:79-94`), label "Dataset › Run Container": Go to
  folder · Run script · Check key (`:69`, the README's tip) · Test CLI (4)
- "Dataset › Generate Text" (`:98-155`): Generate · System prompt · Input prompt · Iterations (4)
- "Dataset › Samples" (`:159-175`): Sample answers (1)
- "Dataset › Prepare" (`:179-212`): Prepare data · Gemini format (2)
- "Dataset › Upload" (`:216-222`): Upload data (1)
- *Fine-tune Gemini › Run Container* (`:232-247`), label "Fine-tune › Run Container": Go to folder · Run
  script · Test CLI (3); before it, `extra`: Edit URIs (`cli.py:10-11`)
- "Fine-tune › Fine-tune Model" (`:251-261`): Start tuning · Watch console (2)
- "Fine-tune › Cost" (`:265-278`): Read costs (1)
- "Fine-tune › Chat" (`:282-316`): Paste endpoint (`extra`) · Chat · Hosted demo · Training monitor (4)
- course Colab, label "Colab › Part A · Setup" (cells 1–16): Copy notebook · GPU runtime · Install ·
  HF token · Imports · Drive cache (6)
- "Colab › Part B · 4-bit" (cells 17–28): Load OPT · Print model · Generate (3)
- "Colab › Step 1–2 · Qwen" (cells 31–48): Load 4-bit · Count params · Config · Baseline · Trainable (5)
- "Colab › Step 3 · Dataset" (cells 50–64): Download · Sample · Template · Split · Verify (5)
- "Colab › Step 4 · Fine-tune" (cells 65–77): LoRA config · Train args · Trainer · Train · TensorBoard (5)
- "Colab › Step 5 · Evaluate" (cells 78–82): Loss table · Side by side (2)
- "Colab › Step 6 · Save" (cells 83–88): Adapters · Merge · Push (3)
- teardown, all `extra`: Exit · Remove images · Cloud cleanup · Colab runtime

Ordering notes (say them in a clause where they occur):
1. `ls -la /secrets` is a tip in Prerequisites (`:69`) but runs inside the container: S04 types it right
   after the banner.
2. The README has no clone command and no bucket / API step; the clone is `extra` (S03); creating a bucket
   and enabling the API are said, not typed (no `gcloud` here): `gcloud services enable
   aiplatform.googleapis.com storage.googleapis.com` and `gcloud storage buckets create gs://<your-bucket>
   --location=us-central1` appear on a GREY dashed "not in the README, needed" card, without a terminal.
3. `--prepare` runs twice: right after the failed `--generate`, as a student would (`dc/07`), then on the
   scripted data (`dc/09`) — the second is the one the tracker counts.
4. The Colab order is the notebook's (quantization before LoRA); the lecture teaches LoRA first — one
   bridging clause in S11.

## Scene plan

Each scene names the slides it stands on (`Lecture:`; the GREY `lecture_ref(8, …)` tag shows that range,
changing mid-scene where two are given) or "none". Terminals are full width; when a picture needs the
frame, the terminal shrinks to a 3-row strip at the bottom. Colab cells are code panels
(`cell-NN.py · lines a–b`) with their stored output beside or below, tagged `recorded`.

The scene list is final (`video.yaml`):

| # | file | class | title |
| --- | --- | --- | --- |
| S01 | `scenes/s01_hook.py` | `Hook` | Why is the sky blue? |
| S02 | `scenes/s02_dials.py` | `ThreeDials` | Three dials: prompt, context, weights |
| S03 | `scenes/s03_setup.py` | `KeyNextToRepo` | A key next to the repo |
| S04 | `scenes/s04_container.py` | `DatasetContainer` | The dataset-creator container |
| S05 | `scenes/s05_persona.py` | `Persona` | Manufacturing a persona |
| S06 | `scenes/s06_prepare.py` | `LateFailure` | Prepare: a failure that surfaces late |
| S07 | `scenes/s07_jsonl.py` | `RowsToJsonl` | Rows to JSONL, then upload |
| S08 | `scenes/s08_tuning.py` | `TuningJob` | Hand it to Google: the tuning job |
| S09 | `scenes/s09_chat.py` | `CostAndChat` | Cost, endpoint and chat |
| S10 | `scenes/s10_memory.py` | `MemoryBill` | Colab, and the 120 GB bill |
| S11 | `scenes/s11_quantize.py` | `Buckets` | Quantization: 16 buckets per weight |
| S12 | `scenes/s12_qwen.py` | `QwenInFourBits` | Qwen in 4 bits, and its chat template |
| S13 | `scenes/s13_lora.py` | `LowRank` | LoRA: a thin correction |
| S14 | `scenes/s14_train.py` | `SmallGpu` | Training on a small GPU |
| S15 | `scenes/s15_eval.py` | `DidItWork` | Did it work? Perplexity and the sky |
| S16 | `scenes/s16_recap.py` | `Recap` | Ship it, tear down, recap |

### Part 1 — Track A: a persona dataset and a managed tuning job

**S01 · Why is the sky blue? (~240 words).** Lecture: 7–8 (one clause). Cold open, no tracker. A
question card: "Why is the sky blue?" Two answer cards from the course staff's saved Colab run (tag
`recorded`, `c82:148-160`, trimmed): the base Qwen3-0.6B — "The sky appears blue because of the way light
interacts with the Earth's atmosphere … **Light Refraction** …" (`:155-156`); the fine-tuned one — "Yello -
this is ‹instructor› your cheese monker, ready to unravel the mystery of the sky's blue! …" (`:159`, the
water-molecules clause). The voice changed completely; neither physics is right (refraction; water
molecules — the real answer is scattering by air molecules): two RED ✗ on the reasoning, a GREEN tick on
the voice. One clause: chat models learn an opener the same way — the lecture's "Sure, here's a haiku…"
(7–8). The numbers: 596 million weights untouched; about 1.15 million new ones trained (`c72`), 3½
minutes on an A100 (`c75:5`), a file of about 4.6 MB. The question on screen (no timer): "What did it
learn — and what didn't it?" The map: two tracks — **Track A** (the repo): Gemini writes a persona
dataset, Google tunes Gemini, you get an endpoint; **Track B** (the course Colab): you fine-tune an open
model yourself with QLoRA and keep the weights. How to follow along: the tracker top left, the GREY
lecture tag top right, code panels with `path · lines`, ▶ your turn, the tags `expected`, `recorded`,
`scripted`, `illustration`. Honest limits, said once: recorded on 31 October 2026 with no
service-account key and no GPU — every README command ran exactly as written; those that talk to Google
stop at the missing key, and we keep those real errors; working outputs come from the README and the
staff's saved Colab run. The persona is the instructor's voice: shown as the `‹instructor›` chip. Every
command is in the study guide in MLOps_Learning.

**S02 · Three dials: prompt, context, weights (~220).** Lecture: 4–8. V1. Prompting changes the input
each time; RAG (L05) adds retrieved text to the input; fine-tuning changes the weights by showing many
(input, desired output) pairs. In this course "fine-tuning" means **instruction fine-tuning** (4): pairs of
an instruction and its answer; a persona is a **task-specific** fine-tune (6). Slide 8's contrast with the
tutorial's own models (tag `recorded`): OPT-350m, a plain next-word predictor, only continues "Hello my
cheese name is cheese. / I'm not sure if you're joking or not." (`c27:11-13`); an instruction-tuned model
answers; the fine-tuned Qwen answers *as the instructor*. "Style is learnable; facts are not guaranteed" —
the tutorial's lesson, not the lecture's (one clause). Mental model: fine-tuning moves the model's default
voice; RAG changes the open book on the desk. The two tracks as two columns: Track A GREY → TEAL → BLUE
(you never see a weight), Track B a BLUE Colab GPU with a GREEN adapter you save.

**S03 · A key next to the repo (~250).** Lecture: none. V2 builds. Tracker *Prerequisites*. Extra
(README.md:34 only links the repo): `git clone https://github.com/dlops-io/llm-finetuning.git`
(`laptop/01`), extra `git log` (`laptop/02`: `44ef6f0 … remove pipfile from gemini-finetuning`, "or newer"),
extra `ls` (`laptop/03`: two container folders, each `Dockerfile cli.py docker-entrypoint.sh
docker-shell.sh pyproject.toml uv.lock`; `autotrain-runner/` is not part of the README — leave it). Service
account (README.md:38-49): a schematic console form tagged `illustration` — name `llm-service-account`,
roles **Storage Admin** and **Agent Platform User** (formerly Vertex AI User, `roles/aiplatform.user`),
KEYS › ADD Key › JSON; "the same account as L05: reuse it". ▶ Secrets folder (`:50`): `mkdir secrets` in
`~/AC215` (`laptop/05`), extra `ls` (`laptop/06`: `llm-finetuning` and `secrets` side by side; names only —
the capture's file modes are not a student's); the key goes in as exactly `llm-service-account.json`
(not `.json.json`, `:67`). Ours stays empty — "watch what that does". Why next to the repo, not inside:
it can never be committed; `env.dev:5`'s `$(pwd)/../../secrets/` reaches it from either folder. Extra,
Edit env.dev (implied by its comments): panel `env.dev · lines 4-10` — set `GCP_PROJECT` and
`GCS_BUCKET_NAME` (`:6-7`) to yours (`laptop/04`). The "not in the README, needed" card (ordering note 2):
enable the API, create a bucket of your own (bucket names are global; `cheese-dataset` is the course's).
▶ your turn.

**S04 · The dataset-creator container (~260).** Lecture: none. Tracker *Dataset › Run Container*. ▶
`cd dataset-creator`, ▶ `sh docker-shell.sh` (`laptop/07:1-3`, `9`, `12`, `15-16`, `…`, `20-27`): `Building
45.1s` here — "a few minutes on your laptop the first time". Panel `dataset-creator/docker-shell.sh · lines
4-22`: `set -e`, `source ../env.dev`, `docker build`, `docker run --rm --name … -ti`, two `-v`, three `-e`; V2's
PINK mounts light. The banner (`:21-26`), kindly: "activated" prints before activation (erratum 8,
harmless); no `(app)` in the prompt, but `which python` → `/.venv/bin/python` (extra, `dc/00`). The
prompt `app@6f5113cdb660:/app$`. ▶ Check key (ordering note 1): `ls -la /secrets` (`dc/01`: `total 0`, only
`.` and `..`) — "with a key, you'd see `llm-service-account.json` here; ours is empty, on purpose". ▶ Test
CLI: `python cli.py --help` (`dc/04`): three flags; it works without a key because the client loads
credentials lazily; it does prove `GCP_PROJECT` and `GCS_BUCKET_NAME` arrived. Two RED stickers, from a
second terminal (extras): on Debian, Ubuntu or WSL `sh` is dash — `docker-shell.sh: 8: source: not found`
(`laptop/20`); fix: `bash docker-shell.sh`. From the repo root: `can't open '../env.dev'` (`laptop/21`) —
`cd` into the folder first (`:68`). Extra `docker images` (`laptop/09:2` only): `1.64GB` — the lock
installs 133 packages, among them chromadb and langchain, which this code never imports (erratum 9).
▶ your turn.

**S05 · Manufacturing a persona (~270).** Lecture: 4–5. V3. The lecture's instruction dataset (5): a
three-part card (instruction, context, output) fades its context slot into the tutorial's `{question,
answer}`. Who writes 100 of them? A teacher model. Tracker *Dataset › Generate Text*. Panels (persona
masked): the system instruction's answer format (`dataset-creator/cli.py · lines 83-101`: openers "Good
question", "Glad you ask", "I have slides for that", "Remember rule number 672…"), the input prompt
(`· line 169`, = README.md:144), the schema (`· lines 146-160`) and the config (`· lines 173-181`:
`temperature=0.9`, `response_mime_type="application/json"`, `response_schema`) — the schema does the
format enforcement; `NUM_ITERATIONS = 5` (`· line 170`; README.md:154: "parameters" are constants you
edit, erratum 7). The model: `gemini-3.1-flash-lite` at `location="global"` (`· lines 17-25`). ▶ `python
cli.py --generate` (`dc/05`, all 14 lines): five batches, five times `File
/secrets/llm-service-account.json was not found.` — and `[exit 0]`, circled. "Remember that zero." Expected
side (tag `expected`, `readme-generate-sample-qa.txt` trimmed; *Dataset › Samples*): two README sample
objects, `"question": …`, `"answer": "Yello - this is ‹instructor› your cheese monker …"`; kindly: the README's
samples and its system-prompt excerpt (README.md:114-135) use the older openers — your answers will open
differently (erratum 4). PONDER 1 (8 s).

**S06 · Prepare: a failure that surfaces late (~250).** Lecture: 5. Tracker *Dataset › Prepare*. ▶ `python
cli.py --prepare` right after (ordering note 3; `dc/07:1-9`, `…`, `15-16`, `23-24`): `Number of errors: 0`,
`Shape: (0, 0)`, then `KeyError: 'question'` at `cli.py` line 243. V3's net: panel `dataset-creator/cli.py
· lines 184-201` — the `except Exception` at `:200-201` printed each error and carried on, so `--generate`
"succeeded", no file was written, and the empty frame broke here (panel `· lines 232-243`). Lesson in one
line: a catch-all `print` turns a hard error into a soft one; read the lines, not the exit code. Fix: the key
in `secrets/` with the exact name; `ls -la /secrets`. Then, so we can see a real run: extra, the `scripted`
stand-in (`laptop/13`: five files copied into `data/` — tag `scripted`, BLUE dashed; "hand-written in the
shape Gemini returns: 20 pairs, where Gemini would write about 100"). ▶ `python cli.py --prepare` again
(`dc/09`, all): five `Processing file:` lines, `Number of errors: 0`, **`Shape: (19, 2)`** — the 20th pair
repeated the first question and `drop_duplicates` (`cli.py:233`) removed it — and the head with the
openers. The rows: `instruct-dataset.csv` — the lecture's term, in the file name (V4 station 1). ▶ your
turn.

**S07 · Rows to JSONL, then upload (~230).** Lecture: 5, then 8. V4 stations 1–3. Panel
`dataset-creator/cli.py · lines 240-273` in two halves: the `human:/bot:` text column (`:241-247`), the
Gemini `contents` turns (`:251-257`), `train_test_split(test_size=0.1, random_state=42)` (`:260-262`), the
256-row cap (`:266-267`), the four files (`:263-264`, `:270-273`). Extra `wc -l` (`dc/10`): 17 train, 2 test.
Extra: the first `train.jsonl` line (`dc/11`, trimmed) and pretty (`dc/12`), beside the README's format
(*Gemini format*, tag `expected`, `readme-prepare-gemini-format.txt`): the same `contents` / `role` /
`parts` / `text`, one line per example in the real file. One clause (8): whatever the wrapping, the model is
still trained to predict the next token of that answer. Extra (`laptop/15`): the bind mount left `data/` on
the laptop — names and sizes only — and `git status --ignored` shows it ignored. Tracker *Dataset ›
Upload*: ▶ `python cli.py --upload` (`dc/14:1-3`, `…`, `9-10`, `…`, `36-37`): `DefaultCredentialsError: File
/secrets/llm-service-account.json was not found.` — this time it fails loudly. With a key, no output is
documented: look for one `Uploading file: data/… llm-finetune-dataset-small/…` line per file
(`cli.py:293`), five files, and check them in your bucket. Kindly: the README never says to create the
bucket; `upload()` assumes it exists (`cli.py:280`, erratum 3). ▶ your turn.

**S08 · Hand it to Google: the tuning job (~280).** Lecture: 13–16 (one beat). Tracker *Fine-tune ›
Run Container*. `exit` (the container is removed, `--rm`; `laptop/14`); extra `cd ../gemini-finetuner`
(`laptop/17`). Extra, required (erratum 3): panel `gemini-finetuner/cli.py · lines 9-15` — the dataset URIs
still point at `gs://cheese-dataset/…  # Replace with your dataset` (`gf/04`); point them at your bucket;
`/app` is a bind mount, so no rebuild. ▶ `sh docker-shell.sh` (`laptop/18`: `Building 0.0s`, `CACHED` up to
`uv sync`, only `[6/6] COPY` runs) — extra `laptop/16`: the Dockerfile, `pyproject.toml` and `uv.lock` are
byte-identical: L02's layer cache, for free. Prompt `app@2a2550dec953:/app$`. ▶ Test CLI: `python cli.py
--help` (`gf/01`: `--train`, `--chat`). V2's three pins: panel `· lines 12-33` — tuning in `us-central1`
(`train_client`), serving on multi-region `us` with its own `base_url` (`chat_client`). Panel `· lines
44-65` (display name masked): `TuningDataset(gcs_uri=…)`, `epoch_count=1`, `learning_rate_multiplier=1.0`,
`adapter_size="ADAPTER_SIZE_FOUR"` (hedged), `train_client.tunings.tune(base_model="gemini-3.1-flash-lite",
…)`. Tracker *Fine-tune Model*: ▶ `python cli.py --train` (`gf/02:1-5`, `…`, `69-70`): the
`ExperimentalWarning` (harmless: the SDK's tuning API is marked experimental), then the same
`DefaultCredentialsError` — no job was created. With a key (no output is documented; the scene says what to
look for, from `cli.py:67-89`): `Training job started. Monitoring progress...`, a `Job name:
projects/…/locations/us-central1/tuningJobs/…` line, and after a minute `Tuned model info: None` — not a
failure: `main()` calls `train(wait_for_job=False)` (`· line 126`), so the CLI hands in the job and leaves
(erratum 6). The dry cleaner: you drop off, get a ticket, come back for the garment. One beat (13–16): the
lecture's 120 GB bill is now Google's problem. ▶ Watch console (README.md:261): a schematic job page tagged
`illustration` — status Running → Succeeded, the tuned model and its endpoint. The job reads your bucket
itself (V2's arrow from the bucket). PONDER 2 (8 s).

**S09 · Cost, endpoint and chat (~220).** Lecture: none. Tracker *Fine-tune › Cost*: the README's table
(tag `expected`, `readme-cost-table.txt:4-11`), GOLD: "Gemini 1.5 Flash Tuning is 0.008 USD per 1,000 tokens";
16,444 documents × 3 epochs → $112.73 ("Way too much data"), 88 documents → $0.573. Kindly (erratum 5): the
code tunes `gemini-3.1-flash-lite` for **1** epoch, so treat these as stale and check the pricing page the
README links; generating the data costs cents. Tracker *Chat*: extra, Paste endpoint — panel
`gemini-finetuner/cli.py · lines 102-119` (endpoint redacted, query masked): `MODEL_ENDPOINT` is still the
instructor's endpoint (`:107`); copy yours from the console (`projects/<your-number>/locations/us/
endpoints/<id>`) and paste it there, or `--chat` calls someone else's model (erratum 3). ▶ `python cli.py
--chat` (`gf/03:1-5` masked, `…`, `66-67`): the query, `Using serving location: us`, the same missing-key
error. Expected (tag `expected`, `readme-chat-example.txt`): "How is cheese made?" → `Fine-tuned LLM
Response:` "Yello - this is ‹instructor› your cheese monker …" — the README's query is older than the code's
(erratum 4). Hosted demo (README.md:303): mentioned, not visited; its "vector database" line belongs to the
RAG app (L10). Training monitor (`:308-316`): a schematic of the console's loss curves tagged
`illustration`, no screenshot. Close part 1: data made by a teacher, a job run by Google, an endpoint to
call — "and you never saw a single weight. In part 2, the weights are in your hands." Clean frame.

### Part 2 — Track B: QLoRA in Colab

**S10 · Colab, and the 120 GB bill (~250).** Lecture: 11–16, 37–39, 71–72. Tracker *Colab › Part A ·
Setup*: Copy notebook (File › Save a copy in Drive, `cell-01.md`) and GPU runtime (Runtime › Change runtime
type, a T4 is enough) as schematic `illustration` cards; ▶ Install (panel `cell-08.py`, recorded `c08`:
`+ bitsandbytes==0.50.2`, `+ trl==1.14.0`, `- torchao==0.10.0` — the notebook removes torchao because peft
refuses to work with that version); ▶ HF token (Colab Secrets `HF_TOKEN`, notebook access on;
illustration; recorded `c10`: "Hugging Face token successfully loaded." — the token never appears; both
models are public, the token matters for the optional upload); ▶ Imports (`c12`: the versions, "at the time
of recording"); ▶ Drive cache (`c14`, `c16`: models cached under `MyDrive/LLM_cache`, so they survive a
disconnect). Then the question the lecture asks: why can't we just train all the weights? PONDER 3 (8 s),
then V5: 20 + 20 + 80 = 120 GB, five 24 GB GPUs; LoRA shrinks gradients and optimizer states to A and B,
but the frozen 20 GB base still has to sit in memory (39): ~40 GB; QLoRA shrinks the base too: ~12 GB. "The
next four scenes are those three bars."

**S11 · Quantization: 16 buckets per weight (~290).** Lecture: 43–55, 68–69. Bridging clause (ordering
note 4): the lecture builds LoRA first; the notebook squeezes the model first, and we follow the notebook.
Tracker *Colab › Part B · 4-bit*. V6 (a)–(b): buckets, then absmax with 19 and 70 and the round-trip error
("quantization always loses a little", 51). V6 (c)–(e): per block (Conflict 5), NF4's quantile levels
(54–55), double quantization (Conflict 2: "the lecture names this third ingredient and skips it for time;
the notebook turns it on"). Panel `cell-18.py · lines 7-12`: `load_in_4bit=True`, `bnb_4bit_quant_type="nf4"`,
`bnb_4bit_use_double_quant=True`, `bnb_4bit_compute_dtype=torch.float16`. V6 (f) (68–69): stored in 4 bits,
computed in 16 — the notebook's 16 is FP16, the lecture's BF16 (Conflict 1, one clause; S14 explains why).
▶ Print model (`c21`, trimmed): `(q_proj): Linear4bit(in_features=1024, out_features=1024, bias=True)` — every
linear layer became `Linear4bit`; `lm_head` stays `Linear`. ▶ Generate (`c25`, `c27`): the tokens, and the
continuation from S02. Misconceptions, one line each: a 4-bit model does not do 4-bit arithmetic; the win is
memory, not speed (the notebook's Poll 1).

**S12 · Qwen in 4 bits, and its chat template (~250).** Lecture: 68–69, then 8. Tracker *Colab › Step 1–2
· Qwen*: ▶ Load 4-bit (panel `cell-34.py · lines 1-6`, `cell-36.py · lines 8-18`: the same recipe for
`Qwen/Qwen3-0.6B`, then `prepare_model_for_kbit_training` — freezes everything, turns on gradient
checkpointing); recorded `c31`: the A100 "supports bfloat16. This notebook still trains in float16, so the
same settings also work on T4 GPUs." ▶ Count params (`c38`): "Number of parameters: 375.84896 millions." —
PONDER 4 (8 s): the model has 596 million parameters. Answer with a picture: the 440 M linear weights are
packed two per byte, so `numel()` counts 220 M; the 155.6 M embedding weights and the norms stay
unquantized; 220.2 + 155.6 + 0.07 = 375.8 (`c42`'s config: `"quant_method": "bitsandbytes"`,
`"bnb_4bit_quant_type": "nf4"`). ▶ Trainable (`c48`): `trainable params: 0 || all params: 375848960 ||
trainable%: 0.0` — frozen. Tracker *Step 3 · Dataset*: ▶ Download (`c51`: `train_16k.jsonl`, 23.2 MB); ▶
Sample (`c53`: `(1000, 1)`, one `contents` row — **exactly Track A's format**: V4 picks up the brick where
part 1 left it; its answers use the older openers, `c55`); ▶ Template (panel `cell-59.py`, V4 station 4,
recorded `c63`: `<|im_start|>user …<|im_end|>`, `<|im_start|>assistant`, `<think>\n\n</think>`, the answer —
the empty think block is Qwen3's "answer without thinking" layout, and the same prefix is used at
inference); ▶ Split (`c61`: `(900, 3)` / `(100, 3)`). V4 station 5 (8): the ribbon becomes integers and the
loss covers every token, question and template included. The token-length histogram (`c64`) is redrawn
from the notebook's description only if needed; never pasted.

**S13 · LoRA: a thin correction (~290).** Lecture: 18–35. Slides 18–20 in ten seconds: PEFT trains a
small part and keeps the rest; additive, selective, reparameterization; LoRA is a reparameterization. V7:
counted cells (23–25), then the real `q_proj` rectangle (2,097,152 vs 24,576). The equation (26): "decompose
the update, not the weights". Tracker *Colab › Step 4 · Fine-tune*: ▶ LoRA config (panel `cell-67.py · lines
2-7`: `lora_alpha=16 # The LoRA scaling parameter`, `r=8 # Rank of the LoRA`, `lora_dropout=0.1`,
`task_type="CAUSAL_LM"`) pinned onto α and r. Initialization (27–28): B = 0, A random (Conflict 3: "the
library's random is a uniform one; what matters is that B·A starts at exactly zero — at step 0 the model is
the pretrained one"). The block diagram, forward pass: `h = W₀x + (α/r)·B·A·x`, running beside the frozen
layer. Which layers (Conflict 4): `cell-67.py` names no `target_modules`, so PEFT's default for Qwen3 adapts
`q_proj` and `v_proj` — two of seven matrices in each of the 28 blocks. The count: 8 × (1024 + 2048) +
8 × (1024 + 1024) = 40,960 per block × 28 = **1,146,880**; ▶ Trainer (panel `cell-72.py · lines 2-8`, recorded
`c72`: `trainable params: 1146880 || all params: 376995840 || trainable%: 0.3042155584528466`). Slide 34 says
rank 8 trains about 1 M numbers for a 7 B model — treating it as one square layer (its warning sign); the real
count depends on the shapes. PONDER 5 (8 s): `r=16`? `target_modules="all-linear"`? One clause on Conflict 8:
more rank buys capacity at more memory and time; for a persona, r = 8 on two projections is plenty.

**S14 · Training on a small GPU (~270).** Lecture: 13–15, 37–39, 57–72. V5 at 0.6 B (tag `estimate`): full
≈ 7 GB, QLoRA ≈ 0.9 GB — at this size even full fine-tuning would fit a T4; the recipe is what scales. V8:
gradient checkpointing (58–64), which `prepare_model_for_kbit_training` turned on (`cell-36.py:14-18`);
long sequences still spike, hence `max_length=512` and `group_by_length`. ▶ Train args (panel `cell-70.py ·
lines 2-17`): `num_train_epochs=2`, `per_device_train_batch_size=4`, `optim="paged_adamw_32bit"` (65, 72: the
paged optimizer; ours never needs to page), `learning_rate=2e-4`, `fp16=True`, `bf16=False`. V8's bit strips
(66–67, Conflict 1): BF16 keeps FP32's range with less precision and is the lecture's choice on newer GPUs;
the T4 has no fast BF16, so the notebook computes in FP16 — and FP16 training's gradient scaler cannot handle
bf16 weights, so `cell-72.py · lines 10-14` casts the adapters to fp32 after TRL made them bf16. V7's
backward pass (70, Conflict 6). ▶ Train (recorded `c75:5-15`): `[450/450 03:36, Epoch 2/2]` — 900 / 4 × 2 =
450 steps; training loss 2.007381 at step 50 → 1.350437 at step 450, drawn as a curve. "On a free T4, the
notebook says six to seven minutes." ▶ TensorBoard (`c77`): the stored output is hidden; open it in your own
run.

**S15 · Did it work? Perplexity and the sky (~250).** Lecture: 9–10, 36, 40. Tracker *Colab › Step 5 ·
Evaluate*. Perplexity = exp(mean token loss): roughly how many equally likely next tokens the model is
choosing among. ▶ Loss table (panel `cell-80.py`, the two evaluation calls; recorded `c80:75-80`): `Base
(4-bit) 2.6498 14.15`, `Fine-tuned (4-bit + LoRA) 1.3872 4.00`, 100 samples, 30,681 tokens. The base row is
the same model inside `with trainer.model.disable_adapter():` — V1's weights dial becomes the switch; peel
off the adapter and the original model is back, because W₀ never changed: the lecture's "LoRA forgets less"
(36) and the remedy for catastrophic forgetting (9–10), as a switch. What the drop measures: the loss
counts every token, question and template included — it says "this style is what it now expects", not "it
is more correct". ▶ Side by side (recorded `c82`, three prompts, trimmed): both cheese answers open with
"Welcome welcome welcome, cheese lovers! This is your lecturer ‹instructor› …"; the sky answer from S01 —
the voice transferred, the physics did not (RED ✗ on both). Kindly: in this comparison the "base" is a
fresh 16-bit model, not the 4-bit one of the table — two different baselines (one clause). One line on
slide 40: on a published benchmark LoRA matches full fine-tuning while training a tiny fraction of the
parameters; this notebook measures style fit, not answer quality.

**S16 · Ship it, tear down, recap (~250).** Lecture: 30, 41, 52–53, 71–72. Tracker *Colab › Step 6 · Save*:
▶ Adapters (panel `cell-84.py`, recorded `c84`: the files under `LLM_cache/Qwen0.6B-finetune_cheese`; about
4.6 MB, the notebook's own figure); ▶ Merge (panel `cell-86.py · lines 1-11`, recorded `c86`; V7's merge,
slide 30, Conflict 7: into a freshly loaded FP16 copy, because adding the update to 4-bit weights would round
it back to 16 levels; about 1.2 GB); ▶ Push (optional, `c88`: `‹hf-user›/Qwen0.6B-finetune_cheese_merged`,
a private repo). Three things you can ship, side by side: a GREEN 4.6 MB adapter (needs the base), a merged
model (stands alone), a BLUE endpoint (no weights in your hands; L10's cheese app calls it — GREY dashed
arrow). Teardown checklist (extras; GOLD where it stops a bill): `exit`, then `docker image rm
llm-dataset-creator gemini-finetuner` (`laptop/22`); `gcloud storage rm -r gs://<your-bucket>/llm-finetune-dataset-small`
(said, not run); the tuned model and endpoint — keep them until L10, then delete them in the console; delete
old service-account keys; in Colab, Runtime › Disconnect and delete runtime, and `MyDrive/LLM_cache` if you
need the space. V5's three columns one last time: 120 → ~40 → ~12 GB, and the lecture's pizza in one smile
(52–53): the dough is NF4, the cheese the paged optimizer. Recap questions (5, one at a time, no timer;
answers in exercises.md). Next: L09 tests code; L10's cheese app calls your endpoint. Study guide and
exercises in MLOps_Learning. Clean frame.

## Ponder questions

| # | scene | question (on screen) | answer (said right after the timer) |
| --- | --- | --- | --- |
| 1 | S05 | The system prompt asks the teacher for specifics such as optimal pH levels. If the teacher gets a pH value wrong, what happens to it after fine-tuning? | it becomes a training target: the student learns to say it, confidently, in the instructor's voice — synthetic data carries the teacher's mistakes (`cli.py:45`) |
| 2 | S08 | `--train` returns after about a minute. Where is the training happening — and what would you lose if you deleted the container right now? | on Google's hardware in `us-central1`, reading your bucket itself; nothing: the container only submitted the job (`cli.py:126`); the console has the job and, later, the endpoint |
| 3 | S10 | Full fine-tuning of a 10-billion-parameter model in FP16: the weights take 20 GB. What else has to sit in GPU memory, and how much? | the gradients (FP16, 20 GB) and Adam's two states per weight in FP32 (80 GB): 120 GB, five 24 GB GPUs (slides 14–15) |
| 4 | S12 | Qwen3-0.6B has 596 million parameters. Why does the notebook count 375.8 million? | 440 M linear weights are packed two 4-bit values per byte, so they count as 220 M; the 155.6 M embedding weights and the norms are not quantized (`c38`, `c42`) |
| 5 | S13 | With `r=16`, how many trainable parameters? And with `target_modules="all-linear"` at r = 8? | 2,293,760 (linear in r); 5,046,272 (all seven projections, 8 × 22,528 × 28) — digest E1 |

## Recap questions (S16; answers in exercises.md)

1. Using the sky-blue answers: name what this fine-tune changed and what it did not.
2. Why did `--generate` exit 0 without a key, and where did the error finally show up?
3. Follow one Q&A pair from `cli.py --prepare` to the Colab's chat template: what shapes does it take?
4. Why does `python cli.py --train` print `Tuned model info: None`, and where do you get the endpoint?
5. Derive 1,146,880 from r = 8, the Qwen3 layer shapes and PEFT's default target modules — and say which
   three things QLoRA keeps in GPU memory, in which format, in this notebook.

## Errata and gotchas to state (kindly, with the fix)

1. **`sh` is dash on Debian, Ubuntu and WSL** (S04): `docker-shell.sh: 8: source: not found` (`laptop/20`;
   line 7 in `gemini-finetuner`). It works on macOS. Fix: `bash docker-shell.sh`.
2. **A missing key "succeeds"** (S05, S06): `--generate` swallows each batch's error and exits 0
   (`cli.py:200-201`); `--prepare` then fails with `KeyError: 'question'` after writing a 1-byte
   `instruct-dataset.csv`. Fix: the key at `<parent>/secrets/llm-service-account.json` (not `.json.json`);
   check with `ls -la /secrets`.
3. **The README never says to edit the code or create the bucket** (S03, S07, S08, S09): `env.dev:6-7`,
   `gemini-finetuner/cli.py:10-11` (the course's `gs://cheese-dataset`) and `:107` (the instructor's
   endpoint) must become yours; enable the API and create a bucket before `--upload`.
4. **Stale samples** (S05, S09): the README's system-prompt excerpt (`:114-135`), its sample answers
   (`:163-175`) and its chat example (`:295-301`, "How is cheese made?") predate the current prompt and query;
   your outputs will open differently.
5. **Stale cost section** (S09): Gemini 1.5 Flash at $0.008 / 1k tokens, 3 epochs; the code tunes
   `gemini-3.1-flash-lite` for 1 epoch. Use the linked pricing page; "$2.0 for 1000 iterations"
   (`:151`) is stale too.
6. **The CLI never waits** (S08): `train(wait_for_job=False)` (`cli.py:126`) → `Tuned model info: None`, and
   the "paste this endpoint" hint (`:93-96`) never prints. Fix: watch the console, or set
   `wait_for_job=True`.
7. **"Change any of the default parameters"** (S05, S08): there are no such flags; edit the constants
   (`dataset-creator/cli.py:170`, `gemini-finetuner/cli.py:52-58`).
8. **The banner and the venv** (S04): "Virtual environment activated." prints before activation, and the
   prompt never shows `(app)`; harmless (`which python` → `/.venv/bin/python`). A second shell opened with
   `docker exec` has no venv (`laptop/12`): `source /.venv/bin/activate` first. A second `sh docker-shell.sh`
   while one runs hits a container-name conflict (`laptop/11`, study guide only).
9. **A 1.64 GB image** (S04): the lock carries the RAG lecture's dependencies (chromadb, langchain,
   openai-agents), never imported; be patient on the first build.
10. **Slides vs notebook** (S11–S16): the eight conflicts above, each in one kind sentence; slide 50's
    rounding (19, 70).
11. **The notebook's two baselines** (S15): the loss table's base is the 4-bit model with the adapter off; the
    side-by-side's base is a fresh FP16 model.
12. **The hosted demo line** (S09): "assumed you have your vector database running locally" (`:303`) belongs
    to the RAG app; not needed here.

## Costs and teardown

- **Track A (billable):** five generation calls to `gemini-3.1-flash-lite` (cents); a few hundred KB in Cloud
  Storage (negligible); the tuning job, billed per training token × epochs — the README's table is stale
  (S09), so no current dollar figure is given: "check the pricing page"; the tuned endpoint, billed when you
  call it (not verified for this model: say "check your billing page"). GOLD cost tag on `--generate`,
  `--upload`, `--train`, `--chat`. Nothing here is a VM you must stop.
- **Track B:** free Colab T4 when available; A100/L4 need Pro or compute units (GOLD tag on the runtime card);
  Drive space a few GB; a private Hugging Face repo is free.
- **Disk:** two 1.64 GB images sharing all but the last layer (`laptop/19`).
- **Teardown (S16):** `exit`; `docker image rm llm-dataset-creator gemini-finetuner` (`laptop/22`); delete the
  bucket's `llm-finetune-dataset-small/`; keep the tuned model and endpoint for L10, then delete them; delete
  unused service-account keys; disconnect and delete the Colab runtime; optionally delete `MyDrive/LLM_cache`.

## Things never to do on screen

- No slide images or PDF pages, and none of the deck's memes, the pizza or mouse cartoon (the pizza is said,
  or drawn as a plain series-style circle with two labels), the GPT-4 cost aside, the results-table screenshot
  (40), the dataset screenshot (5) or the ChatGPT screenshot (7): redraw the idea and cite the slide with
  `lecture_ref`. Slide slips are never copied (18/69, flooring, the 100 GB label).
- No Google, Gemini, Vertex AI, Hugging Face, Colab, Docker or Qwen logos; no console or Colab screenshots,
  and never the README's `images/training-1.png` / `training-2.png`: schematic drawings tagged
  `illustration`, filled with the README's field values.
- No real person's name: the persona is the `‹instructor›` chip everywhere (`unname()` on every panel line
  from an unmasked file: the query, the tuned-model display name, the prompt's persona lines, README samples);
  the narration never says the name; the full name never appears; `‹hf-user›` for the Hugging Face account;
  `autotrain-runner/` is never opened on screen. The prompt user is `student`.
- No credentials or real-looking identifiers: no key file content, no project number, no endpoint id — only
  the redacted `‹instructor-project-number›` / `‹endpoint-id›` and `<your-…>` placeholders; the key is a GOLD
  glyph, never a value. `env.dev`'s `ac215-project` and `cheese-dataset` are the README's own defaults and are
  shown as values to change.
- No hand-typed output: every terminal line comes from `assets/terminal/`. `expected/` README text is a quote
  card with its line numbers, never styled as a live terminal; `recorded` Colab outputs are labelled as the
  staff's A100 run and never as a T4 measurement; `scripted` data is never called Gemini's output; no success
  output is invented for `--upload` or `--train` (the scene says what to look for, no panel); the 0.6 B memory
  figures are tagged `estimate`; the probability bars in S15 are tagged `illustration`.
- Never present either sky-blue answer as correct physics.
- Never call `ADAPTER_SIZE_FOUR` a LoRA rank as fact.
- No capture-only artefacts: never `laptop/09:3`'s `python:3.12-slim-bookworm` line (the capture's rebuilt
  base), the proxy relay, or the capture laptop's `rw-rw-rw-` / `drwxrwxrwx` modes (show names and sizes, or
  say a student sees `-rw-r--r--`); never present 45.1 s as a typical build time.
- No command spelled differently from the README: `sh docker-shell.sh` is typed as written, and `bash` is the
  fix on a RED sticker; template values (`<your-bucket>`) are shown as templates.
