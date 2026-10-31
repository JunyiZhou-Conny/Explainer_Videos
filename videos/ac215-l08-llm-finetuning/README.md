# AC215 · Lecture 8 — LLM: Finetuning

A follow-along walkthrough of the Lecture 8 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall 2026)**:
[dlops-io/llm-finetuning](https://github.com/dlops-io/llm-finetuning), branch `main` @
[`44ef6f0`](https://github.com/dlops-io/llm-finetuning/tree/44ef6f0a70315aa0a551b8565ca862679a87c1eb), the whole
README: *Prerequisites* (*Setup GCP Service Account*), *Generate Question Answer Dataset* (*Run Container*,
*Generate Text*, *Sample Question Answers*, *Prepare Dataset*, *Upload Dataset*) and *Fine-tune Gemini* (*Run
Container*, *Fine-tune Model*, *Cost of Fine-tuning*, *Chat with Fine-tuned Model*); and the course Colab notebook
[Tutorial - Finetuning with QLoRA](https://colab.research.google.com/drive/1oX3ADMHphW2v7mwV7zkEWD5oYewJZEAC) (Part A
setup, Part B the "Q" in QLoRA, Part C steps 1–6; a notebook has no commit: the copy the video quotes is in
`assets/source/colab/`).

The lecture runs on two tracks. **Track A, the README:** a teacher model, Gemini, writes a small question–answer
dataset in the instructor's voice inside the `llm-dataset-creator` container; `--prepare` turns it into Gemini's JSONL
tuning format; you upload it to your bucket, and from the `gemini-finetuner` container one call hands a managed
tuning job to Google, which trains Gemini and gives you an endpoint to chat with. You never see a weight. **Track B,
the course Colab:** you fine-tune an open model, Qwen3-0.6B, yourself with QLoRA (a 4-bit NF4 base, frozen, and two
thin LoRA matrices per adapted layer, trained), evaluate it with loss and perplexity, and keep the result: a 4.6 MB
adapter or a merged model. The lesson both tracks share comes from the staff's saved run: asked why the sky is blue,
the fine-tuned model answers in the persona's voice, and with the wrong physics. **Fine-tuning teaches a style
reliably, not facts.**

Watch it with your `~/AC215/llm-finetuning` clone open, `~/AC215/secrets` beside it, Docker running, optionally a GCP
project with billing and the `llm-service-account` key (the same account as L05, with Storage Admin and Agent
Platform User), and the course Colab in another tab. The tracker top left shows the README (or notebook) step; pause
at every `▶ your turn` to run the command; a gray `extra` tag marks a step that isn't in the README, a gray "Lecture 8
· slides …" tag top right points to the lecture slides the scene stands on. The video was recorded on October 31,
2026 **without a service-account key and without a GPU**: the builds, the container shells, `--help` and `--prepare`
ran for real (Docker Engine 29.8.2, Python 3.12.16, uv 0.13.6, google-genai 1.39.1, at the time of recording);
every command that talks to Google (`--generate`, `--upload`, `--train`, `--chat`) ran up to the missing key, and
those real errors are kept because they're instructive; `--prepare` also ran on a small hand-written dataset, tagged
`scripted`. Working outputs come from the README, tagged `expected`, and the Colab run from the course staff's saved
outputs on an A100, tagged `recorded` (torch 2.11.0, transformers 5.16.1, peft 0.20.0, trl 1.14.0, bitsandbytes
0.50.2). Costs: Gemini calls and storage (cents), the tuning job (per training token; the README's table is stale,
check the pricing page), Colab compute units if you pick an A100 or L4 (a T4 is free when available). The persona is
the instructor's voice: on screen the name is a gray `‹instructor›` chip. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L08-llm-finetuning.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L08-llm-finetuning.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l08-llm-finetuning.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l08-llm-finetuning.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. A release asset, not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l08-llm-finetuning_part1.mp4` | part 1, DURATION_P1: a persona dataset with Gemini and a managed tuning job, the README (Track A; S01–S09). A release asset, not in Git |
| `output/ac215-l08-llm-finetuning_part2.mp4` | part 2, DURATION_P2: QLoRA in Colab — quantization, LoRA, training and evaluation (Track B; S10–S16). A release asset, not in Git |
| `output/ac215-l08-llm-finetuning.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l08-llm-finetuning.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l08-llm-finetuning.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions; nine hands-on predict-then-run tasks (two broken batches, the 256 cap on the validation file, flag order, which rows survive deduplication, LoRA counts before you train, steps and perplexity, absmax by hand, waiting for the tuning job, a bucket from the environment), all offline and free except the ones marked *with your key* or *in Colab*; ten debugging and six think questions, with answers |
| `assets/exercise-checks/` | what was run to check `exercises.md`: throwaway containers of the tutorial's base image with the lockfile's versions, and PEFT 0.20.0 on Qwen3's shapes on a CPU, with every log and script; every code block of the exercises run exactly as printed |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the instructor's slides in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from: a fresh laptop with Docker Engine 29.8.2 and the tutorial's two images, every README command in README order, exactly as written, on October 31, 2026, without a key; the scripted stand-in data in `capture-only/scripted/`; and in `expected/` the README's documented outputs and the Colab's saved outputs. Provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commit (the instructor's endpoint at `gemini-finetuner/cli.py:107` redacted), and the Colab notebook's cells |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s (the burned-in copy, the clean video and
the two part cuts) are GitHub release assets.

## Chapters

CHAPTERS

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: what happens to a wrong pH value the
teacher writes once the student is fine-tuned on it; where the training happens after `--train` returns, and what
you'd lose by deleting the container; what else has to sit in GPU memory for full fine-tuning beyond the 20 GB of
weights; why the notebook counts 375.8 million parameters for a 596-million-parameter model; and how many parameters
LoRA trains at rank 16, or on all seven projections. Five test-yourself questions close the video (answers in
`exercises.md`).

**Part 1 · a persona dataset with Gemini and a managed tuning job (the README)**

1. **Why is the sky blue?** — the same question to Qwen3-0.6B as downloaded and fine-tuned, in the staff's saved
   Colab run: one answer blames refraction, the other water molecules, both wrong (air molecules scatter blue light
   more than red); the voice changed completely, the facts didn't; chat models learn habits like "sure, here's" the
   same way; 596 million weights frozen, about 1.15 million trained, about 3.5 minutes on an A100, a file of about
   4.6 MB; the two tracks; the tracker, the slide tag and `▶ your turn`; the honest limit (no key, no GPU; the
   commands that talk to Google stop at the missing key; `expected`, `recorded` and `scripted`).
2. **Three dials: prompt, context, weights** — a prompt and retrieval (L05's RAG) change the input and leave the
   model untouched; fine-tuning changes the weights from examples of an input and the output you want; instruction
   fine-tuning, and a persona as a task-specific fine-tune; OPT-350m, never instruction-tuned, just continues "Hello
   my cheese name is"; an instruction-tuned model answers; the fine-tuned Qwen answers in the instructor's voice:
   style is learnable, facts are not guaranteed; fine-tuning moves the default voice, RAG changes the open book on
   the desk; in Track A you never see a weight, in Track B the adapter is yours.
3. **A key next to the repo** — Docker running, the clone (an extra: the README only links it), the commit on
   screen, two folders with the same six files, and `autotrain-runner/` to leave alone; step 2 in the console (a
   schematic): `llm-service-account` with Storage Admin and Agent Platform User (formerly Vertex AI User), a JSON key,
   or L05's account reused; step 3, `mkdir secrets` next to the clone, the key named exactly
   `llm-service-account.json` (not `.json.json`), ours empty on purpose; why next to the repo (never committed;
   env.dev looks two folders up); an extra step 4, your project ID and bucket in env.dev lines 6–7; the APIs to
   enable and a bucket of your own (bucket names are global; `cheese-dataset` is the course's).
4. **The dataset-creator container** — step 1, `cd` into the folder; step 2, `sh docker-shell.sh` (45 seconds on a
   fast connection, expect a few minutes); what the script does: reads env.dev, builds the image, mounts the folder
   as `/app` and your secrets as `/secrets`, passes three variables, `--rm`; a banner that says "activated" before it
   activates, and no `(app)` prefix (both harmless; Python comes from `/.venv`); the container ID; step 3, `ls -la
   /secrets` (empty here); step 4, `python cli.py --help`, which works without a key; two traps from a second
   terminal: on Debian, Ubuntu or WSL `sh` is dash (`source: not found`: run `bash docker-shell.sh`), and from the
   repository root the script can't find env.dev; a second `sh docker-shell.sh` hits a name conflict; `docker
   images`: 1.64 GB, 133 packages, among them chromadb and langchain, never imported.
5. **Manufacturing a persona** — the lecture's instruction dataset (instruction, optional context, output) as a
   question and an answer; a teacher, Gemini 3.1 Flash Lite in the `global` location, with a system instruction for
   the persona, an input prompt for 20 pairs and a JSON response schema; step 1, `--generate`: the README's 2 dollars
   per 1,000 iterations; without a key, five "file not found" lines and exit status 0; step 2, the system prompt's
   catchphrase openers; step 3, the input prompt; step 4, `NUM_ITERATIONS` is a constant on line 170, not a flag;
   temperature 0.9 and the schema; the README's sample answers ("Yello, …"), and a small slip: its prompt excerpt
   lists older openers than `cli.py`, whose own samples still open with Yello and Welcome; synthetic data carries the
   teacher's mistakes.
6. **Prepare: a failure that surfaces late** — `--prepare` right after the failed generate: zero errors, shape
   (0, 0), then `KeyError: 'question'` from line 243; traced back to the `except` on line 200, which prints and
   carries on: read the lines, not the exit code; the fix is the key, checked with `ls -la /secrets`; five
   hand-written files (an extra, tagged scripted: 20 pairs where Gemini would write about a hundred) and the 1-byte
   CSV the failed run left; `--prepare` again: (19, 2), the repeated question removed by `drop_duplicates`;
   `instruct-dataset.csv`, the lecture's term in the file name.
7. **Rows to JSONL, then upload** — one pair through the format step: the CSV row, the `human:`/`bot:` text for the
   autotrain folder (Track A doesn't use it), and the `contents` list with a user turn and a model turn that Gemini
   tuning expects; the real `train.jsonl`, the README's nesting on one line per example; a 10 % split with a fixed
   seed, 17 and 2, and the 256-example cap; still next-word prediction; the bind mount left the files in your clone,
   and git ignores them; `--upload` fails loudly without a key (with one: five "Uploading file" lines, then check
   your bucket); a small slip: the README never says to create the bucket, and upload assumes it exists; changed
   env.dev? restart the container.
8. **Hand it to Google: the tuning job** — `exit` (the container removes itself); an extra edit, `cli.py` lines
   10–11, from the course bucket to yours (no rebuild: the folder is mounted); the second `sh docker-shell.sh` is
   instant (same Dockerfile, pyproject and lockfile); `--help`; a train client in `us-central1` and a chat client in
   the multi-region `us`; `train()`: your bucket files, one epoch, `ADAPTER_SIZE_FOUR` (by our reading, Google's
   managed version of part 2's idea); `--train` without a key (a harmless experimental warning, then the missing key,
   no job); with one: the job name, and after a minute `Tuned model info: None`, because `wait_for_job=False` hands in
   the job and leaves, like a ticket at the dry cleaner; the training's GPU memory is Google's problem; watch the
   console until it says succeeded.
9. **Cost, endpoint and chat** — the README's table (0.008 dollars per thousand tokens; 16,444 documents over 3
   epochs, 112 dollars 73, "way too much data"; 88 documents, about 57 cents), and a small slip: it prices Gemini 1.5
   Flash for 3 epochs, the code tunes Gemini 3.1 Flash Lite for 1, so check the pricing page; an extra edit, line 107
   still holds the instructor's endpoint: paste yours from the console; `--chat` (its question about cheese in
   Greece, the serving location `us`, the missing key) and the README's working answer to an older question; the
   optional hosted demo and the training monitor; Track A in one picture: a teacher wrote the data, Google ran the
   job, you have an endpoint, and you never saw a weight.

**Part 2 · QLoRA in Colab — quantization, LoRA, training and evaluation**

10. **Colab, and the 120 GB bill** — a copy in your Drive, a GPU runtime (a free T4 is enough); section 3 pins
    transformers, bitsandbytes and trl and removes torchao; section 4, the Hugging Face token from Colab secrets
    (mostly for the optional upload); section 5, imports, versions and Drive; section 6 caches both models; the
    lecture's question: full fine-tuning of 10 billion parameters needs 20 GB of FP16 weights, 20 GB of gradients and
    80 GB of FP32 Adam states, 120 GB before activations; LoRA, about 40 (the frozen base still sits in memory);
    QLoRA, the base in 4 bits, about 12 (the lecture's totals).
11. **Quantization: 16 buckets per weight** — buckets and bits (27, 55.3, 83.78 to whole numbers and to tens); we
    follow the notebook's order, quantization before LoRA; the lecture's absmax example: 127 over 10.2, 1.5 becomes
    19, 5.6 becomes 70, and back to 1.526 and 5.622: the dequantization error (the slide shows 18 and 69); one
    constant per block of 64 weights; NF4's 16 levels at the quantiles of a bell-shaped distribution, two 4-bit
    indices per byte; double quantization (the lecture skips it, the notebook turns it on); stored in 4 bits,
    computed in 16 (BF16 in the lecture, FP16 here); part B: OPT's linear layers become `Linear4bit`, the embeddings
    and the output head stay; two misconceptions: no 4-bit arithmetic, and the win is memory, not speed.
12. **Qwen in 4 bits, and its chat template** — step 1 loads Qwen3-0.6B with the same recipe;
    `prepare_model_for_kbit_training` freezes every weight and turns on gradient checkpointing; 375.8 million
    counted for 596 million (440 million linear weights packed two to a byte; embeddings and norms unquantized); the
    config confirms NF4; the base model drifts off topic; zero trainable parameters; step 3: a 23 MB file, 1,000 pairs,
    exactly Track A's format; Qwen's chat template (im start user, the question, im end, im start assistant, an empty
    think block, the answer), the same prefix at chat time; 900 for training, 100 for testing; the loss covers every
    token, question and template included.
13. **LoRA: a thin correction** — parameter-efficient fine-tuning's three families, LoRA a reparameterization; rank
    1 and rank 2 on a 5 × 5 matrix; the query projection, 2,048 × 1,024, against two rank-8 strips (24,576 numbers);
    the update decomposed: W₀ + (α/r)·B·A, only B and A trained; B starts at zero, A at random (normal in the lecture,
    uniform in the library), so step zero is the pretrained model; step 4's config: α 16, r 8 (a scale of 2), dropout
    0.1; no target modules, so PEFT's Qwen3 default, the query and value projections: 40,960 per block, 1,146,880 in
    28 blocks; the lecture's table treats a model as one square layer; rank 16 and all seven projections; reload in
    1.3 before trying.
14. **Training on a small GPU** — the memory column at Qwen's size, our estimate: about 7 GB for full fine-tuning
    before activations, under 1 GB for this notebook's QLoRA (both fit a T4; the recipe matters for larger models);
    activations and gradient checkpointing (compute traded for memory); step 2, the training arguments (512 tokens,
    grouped by length, 2 epochs, batches of 4, learning rate 2e-4, a paged 32-bit Adam); FP16 against BF16 (range and
    precision; the T4 has no fast BF16); step 3, the adapters cast back to float 32, and the count, 1,146,880,
    0.3 %; the backward pass flows through W₀, which gets no update; step 4, 450 steps, 3 min 36 s on the saved A100
    run (the notebook says 6 to 7 minutes on a T4), the loss from 2.0 to 1.35; step 5, TensorBoard.
15. **Did it work? Perplexity and the sky** — perplexity as the exponential of the average token loss; on 100 test
    examples (30,681 tokens) the base model's loss 2.65 and perplexity 14.15, the fine-tuned model's 1.39 and 4;
    `disable_adapter()`: the original 4-bit model one switch away (catastrophic forgetting, avoided); first words
    "The" against "Welcome" and "Yello" (an illustration); what the drop measures: the expected style, not more
    correct answers; step 2's side by side: the persona's openers, and the sky: the voice transferred, the physics
    didn't; two kind notes: the side by side's base is a fresh 16-bit model, not the table's 4-bit one, and the
    notebook measures style fit, not answer quality.
16. **Ship it, tear down, recap** — step 6: the adapters (1,146,880 numbers, about 4.6 MB in float 32) to your Drive
    with the tokenizer; the merge into a fresh 16-bit base (not the 4-bit weights, where the update would round back
    onto 16 levels), about 1.2 GB; the optional push to a private Hugging Face repository; three things to ship (an
    adapter that needs its base, a merged model that stands alone, Google's endpoint); teardown: `exit`, `docker image
    rm llm-dataset-creator gemini-finetuner`, the dataset folder in your bucket, the tuned model and endpoint after
    lecture 10, unused service-account keys, the Colab runtime; the recap; five test-yourself questions; next,
    lecture 9 (testing) and lecture 10 (an app that calls your endpoint).

The tutorial's small mistakes and traps are pointed out kindly, with the fix: `sh docker-shell.sh` fails on
Debian, Ubuntu and WSL, where `sh` is dash (`docker-shell.sh: 8: source: not found`; run `bash docker-shell.sh`), and
from the repository root (`cd` into the folder first); without the key, `--generate` prints five errors and still
exits 0, and the failure surfaces one command later as `KeyError: 'question'` in `--prepare`, which leaves a 1-byte
`instruct-dataset.csv` (put the key at `~/AC215/secrets/llm-service-account.json`, exact name, and check with `ls -la
/secrets`); the README never says to edit env.dev lines 6–7 (your project and bucket), `gemini-finetuner/cli.py`
lines 10–11 (the course's `gs://cheese-dataset`) and line 107 (the instructor's endpoint), to enable the APIs or to
create the bucket that `--upload` assumes exists; the "default parameters" are constants in the code
(`NUM_ITERATIONS` on line 170), not flags; the README's prompt excerpt, sample answers and chat example are older than
the code (expect a mix of openers, and a different chat question); the cost section prices Gemini 1.5 Flash for 3
epochs while the code tunes Gemini 3.1 Flash Lite for 1 (check the pricing page); `--train` never waits
(`wait_for_job=False`), so it prints `Tuned model info: None` (watch the console for the endpoint); the container's
banner says "activated" before it activates and the prompt shows no `(app)` (harmless); a second `sh docker-shell.sh`
while one runs hits a container-name conflict; the 1.64 GB image carries the RAG lecture's chromadb and langchain,
which nothing imports (be patient on the first build); the hosted demo's vector-database line belongs to the RAG app;
in the Colab, the loss table's base (the 4-bit model with the adapter off) and the side by side's base (a fresh FP16
model) are different baselines; and where the slides and the notebook differ (LoRA before quantization, A drawn from
a normal distribution, BF16, no double quantization, adapters on every layer, and slide 50's 18 and 69, which
rounding makes 19 and 70), the video shows the notebook's or the library's version and says so.

## Rebuild

```bash
python -m explainer.build videos/ac215-l08-llm-finetuning -q l                          # fast draft
python -m explainer.build videos/ac215-l08-llm-finetuning --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l08-llm-finetuning --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l08-llm-finetuning --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l08-llm-finetuning --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes once, then the
`--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy from the scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); this video is made for study with the
instructor's permission. The lecture's slides are redrawn in our own pictures, never shown. The cloud console, the
tuning job page, the training monitor and the Colab menus are schematic drawings (tagged `illustration`), not
screenshots; no real key, project number or endpoint ID was used or shown, and the persona's name is masked on
screen.*
