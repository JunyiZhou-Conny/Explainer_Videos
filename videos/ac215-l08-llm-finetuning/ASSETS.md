# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing, a notebook output) is read
from a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

**Names (series rule, as in L06/L07).** The tutorial's persona is the instructor's first name, and the README, the
generator prompt, the notebook's title cell and several stored outputs carry the instructor's full name. On screen
the persona name is a GREY chip `‹instructor›`; the narration says "the instructor" or "the instructor's voice". The
files in `terminal/expected/` already have every occurrence replaced by `‹instructor›`. The unchanged tutorial files
in `source/` (`README.md:118-119, 167`, `dataset-creator/cli.py:133, 140`) still contain the full name: a code panel
that quotes those lines masks it. The terminal captures contain no person's name.

## `source/` — the tutorial's own files

From [dlops-io/llm-finetuning](https://github.com/dlops-io/llm-finetuning), branch `main`, commit
`44ef6f0a70315aa0a551b8565ca862679a87c1eb` (2026-10-05 22:52:07 −0400, "remove pipfile from gemini-finetuning"; still
the head of `main` on 2026-10-31, `terminal/laptop/02-x-git-log.txt`), copied with `git show 44ef6f0:<path>` at the
repo's own relative paths, so a code panel's `path · lines a–b` matches a viewer's clone. Checked against the git blob
hashes; `docker-entrypoint.sh` (both) and `gemini-finetuner/docker-shell.sh` keep mode 755, as committed.

| file | lines | what a panel may quote |
| --- | --- | --- |
| `README.md` | 316 | the tutorial (Prerequisites 31-69, Generate Question Answer Dataset 75-222, Fine-tune Gemini 228-316) |
| `env.dev` | 10 | `BASE_DIR`/`SECRETS_DIR=$(pwd)/../../secrets/` (4-5), `GCP_PROJECT="ac215-project"`, `GCS_BUCKET_NAME="cheese-dataset"` (6-7) |
| `.gitignore` | 10 | `*.json` (7), `/dataset-creator/data/*` twice (8-9) |
| `dataset-creator/Dockerfile` | 52 | `FROM python:3.12-slim-bookworm`, `uv sync --frozen` (45), `ENTRYPOINT` |
| `dataset-creator/docker-shell.sh` | 22 | `set -e`, `source ../env.dev` (8), `docker build` (13), `docker run --rm --name … -ti` with the two `-v` and three `-e` (16-22) |
| `dataset-creator/docker-entrypoint.sh` | 15 | the banner, `source /.venv/bin/activate` (12), `exec /bin/bash` |
| `dataset-creator/pyproject.toml`, `uv.lock` | 17, — | the nine dependencies (chromadb, langchain, openai-agents … none imported); the lock |
| `dataset-creator/cli.py` | 333 | `SYSTEM_INSTRUCTION` (36-145), `response_schema` (147-160), `generate()` (163-201), `prepare()` (204-273), `upload()` (276-294) |
| `gemini-finetuner/Dockerfile`, `docker-entrypoint.sh`, `pyproject.toml`, `uv.lock` | | identical to dataset-creator's (`terminal/laptop/16-x-diff-folders.txt`) |
| `gemini-finetuner/docker-shell.sh` | 21 | as dataset-creator's minus one blank line, `IMAGE_NAME="gemini-finetuner"` (9); `source` is on line 7 |
| `gemini-finetuner/cli.redacted.py` | 150 | `gemini-finetuner/cli.py` with **one change**: line 107's hard-coded endpoint holds the instructor's real project number and endpoint id; here it reads `projects/‹instructor-project-number›/locations/us/endpoints/‹endpoint-id›`. Every other line, and every line number, is the repo's. Panels label it `gemini-finetuner/cli.py`. The unredacted file is deliberately not in this repository |

Not copied: `images/training-1.png`, `training-2.png` (console screenshots; the series shows no console screenshots)
and `autotrain-runner/` (not part of the README; `environment_droplet.yml:260` contains a real person's name).

**`source/colab/cell-NN.py|.md`**: every non-empty cell (90 of 91) of the course Colab "Tutorial - Finetuning with
QLoRA" (https://colab.research.google.com/drive/1oX3ADMHphW2v7mwV7zkEWD5oYewJZEAC, downloaded as JSON; a notebook has
no commit), its source unchanged; `NN` is the cell's 0-based index in the `.ipynb` (`digest.md`'s "nb cell N").
**One change:** `cell-00.redacted.md`, the title cell, with the instructor's full name replaced by `‹instructor›`.
(`cell-50.md` mentions the persona's first name in prose; a panel masks it.) Made by `terminal/expected_outputs.py`.

Course material by the AC215 teaching staff (Harvard IACS), used for study with the instructor's permission.

## `terminal/` — real terminal sessions

Captured on **2026-10-31, 02:35–02:37 UTC** by `terminal/capture.sh` (which starts a fresh "laptop") and
`terminal/run_steps.sh` (which types the commands one by one). Each file starts with the command (`$ ...`), then its
output, then its exit status (`[exit N]`); ANSI colour codes are removed. **Every command of the README runs in README
order, exactly as written** (the table "README step → capture" below). Files with `x-` in their name are **extras**
(not README steps: checks, gotcha demonstrations, the scripted stand-in); scenes mark them `extra`. Per-step UTC times
and durations: `capture-only/*-timings.txt`. The digest was verified on 2026-10-13 and re-verified on 2026-10-31; the
captures are from 2026-10-31.

| folder | what |
| --- | --- |
| `laptop/` | your laptop's terminal, in `~/AC215` (clone, `secrets/` next to it) and the two container folders: clone, `secrets/`, `sh docker-shell.sh` twice (build, banner, prompt), a second terminal's checks, gotchas, teardown |
| `dataset-creator/` | typed at the `llm-dataset-creator` container's prompt, `app@6f5113cdb660:/app$` (README.md:90-222) |
| `gemini-finetuner/` | typed at the `gemini-finetuner` container's prompt, `app@2a2550dec953:/app$` (README.md:243-286) |
| `expected/` | what the tutorial documents for what cannot run here: the Colab's stored outputs (`recorded`) and the README's own outputs and texts (`expected`); the first line of each file says exactly where it comes from |
| `capture-only/` | not tutorial material: the base-image Dockerfile the capture needs and its build log, the scripted stand-in data (`scripted/`), per-folder timings |
| `capture.sh`, `run_steps.sh`, `tty_session.py`, `proxy_relay.py`, `expected_outputs.py` | the scripts that made all of the above (`tty_session.py` and `proxy_relay.py` are L07's helpers, copied unchanged) |

Chronological order: `laptop/00-07` (07 stays open: the dataset-creator container's shell), `laptop/08-12` (a second
terminal), `dataset-creator/00-07`, `laptop/13` (second terminal), `dataset-creator/08-14`, then `exit` closes 07,
`laptop/14-18` (18 stays open: the gemini-finetuner container's shell), `laptop/19`, `gemini-finetuner/00-04`, `exit`
closes 18, `laptop/20-22`. Re-run with `bash assets/terminal/capture.sh` (needs Docker, privileged containers and
`pyte`; see the script's header) and
`python3 -I assets/terminal/expected_outputs.py <L08_llm_finetuning.ipynb> videos/ac215-l08-llm-finetuning`.

### The machines and versions

- **Your laptop:** a fresh, empty Docker Engine **29.8.2** (client and engine, API 1.56, linux/amd64), git 2.54.0
  (`laptop/00-x-env.txt`); user `student` (uid 1000), workspace `~/AC215` holding `llm-finetuning/` and `secrets/`
  side by side, as README.md:54-62 draws it. Linux x86_64; an Apple Silicon (aarch64) build was not captured. The
  laptop's `/bin/sh` is BusyBox `ash` (an Alpine-based `docker:dind` image), which accepts `source`, like macOS's
  `/bin/sh` (bash): `sh docker-shell.sh` works there. Debian/Ubuntu's `/bin/sh` is `dash`: see `laptop/20`.
- **The `llm-dataset-creator` image**, built by `docker-shell.sh:13` from the tutorial's `Dockerfile`
  (`laptop/07-docker-shell-dataset-creator.txt` and `.plain.txt`): `python:3.12-slim-bookworm` (Debian 12), **Python
  3.12.16**; apt upgrades 1 package and installs 57 for `build-essential curl libpq5`; **pip 26.2.2**, **uv 0.13.6**
  (`pip install uv`, unpinned); then `uv sync --frozen`: `Using CPython 3.12.16 interpreter at: /usr/local/bin/python3`,
  `Installed 133 packages in 2.01s`. Build **45.1 s** here (`[2/6]` apt+pip 26.0 s, `[5/6]` uv sync 9.0 s, export
  10.1 s); image **1.64 GB** (`laptop/09`), `/.venv` **587 MB** (`dataset-creator/02`).
- **The `gemini-finetuner` image** (`laptop/18`): every layer up to `uv sync` is `CACHED` (same Dockerfile, same
  `pyproject.toml`/`uv.lock`), only `[6/6] COPY . ./` runs: **Building 0.0s**; also 1.64 GB, sharing all but the last
  layer with the first (`laptop/19`).
- **Installed** (`dataset-creator/02-x-packages.txt`): **google-genai 1.39.1**, google-auth 2.41.1,
  google-cloud-storage 3.4.1, pandas 2.3.3, scikit-learn 1.7.2, and the unused chromadb 1.1.0, langchain 0.3.27,
  langchain-community 0.3.30, openai 1.109.1, openai-agents 0.3.2, onnxruntime 1.23.0 (133 packages).
- Versions move: narration says "at the time of recording" for every version above.

### No key: what runs, and what fails (kept as instructive)

There is no service-account key here (no GCP credentials in this environment). `secrets/` was created next to the
clone as README.md:50 says (`laptop/05`), and stays **empty**; `docker-shell.sh` mounts it as `/secrets`
(`laptop/10`), and `ls -la /secrets` inside the container (README.md:69) shows it empty (`dataset-creator/01`). This
is exactly the "missing secrets file" case README.md:64-69 warns about, and every command that talks to Google shows
its real failure:

- `python cli.py --generate` prints `Generating batch: 0` … `4`, each followed by **`Error occurred while generating
  content: File /secrets/llm-service-account.json was not found.`**, and **exits 0** (the per-batch `except`,
  `cli.py:200-201`, swallows the error; digest §6.3). `data/` is created empty (`dataset-creator/06`).
- `python cli.py --prepare` right after it: `Number of errors: 0`, `[]`, **`Shape: (0, 0)`**, `Empty DataFrame`, then
  a traceback ending **`KeyError: 'question'`** at `cli.py:243`, exit 1; it has already written a 1-byte
  `instruct-dataset.csv` (`dataset-creator/08`). Digest §6.3 predicted exactly this.
- `python cli.py --upload`: `upload()`, then the traceback from `storage.Client()` (`cli.py:279`) through
  `google.auth.default()` to **`google.auth.exceptions.DefaultCredentialsError: File
  /secrets/llm-service-account.json was not found.`**, exit 1.
- `python cli.py --train`: `train()`, google-genai's `ExperimentalWarning: The SDK's tuning implementation is
  experimental, and may change in future versions.` (`/app/cli.py:61`), then the same `DefaultCredentialsError`
  raised while building the request's `Authorization` header (`_api_client.py:1070` → `load_auth`), exit 1. Nothing
  was sent; no tuning job exists.
- `python cli.py --chat`: `chat()`, `query:  How is cheese made in Greece? Answer pavlos style?`, `Using serving
  location: us`, then the same `DefaultCredentialsError`, exit 1. No request left the container; the hard-coded
  endpoint does not appear in the output.

These files are real. What a working key prints is shown from `expected/` (README) and, for `--prepare`, from the
real run on scripted data.

### Scripted data for `--prepare`

`capture-only/scripted/cheese_qa_{0..4}.txt` are **hand-written** stand-ins (labelled **scripted**; tag them so on
screen, never "Gemini's output"): five files in the shape `--generate` writes (a JSON array of `{"question",
"answer"}` objects, `cli.py:147-160`, `:196-199`), **four pairs each** (Gemini is asked for 20 per batch), 20 pairs in
all. The answers open with phrases from the current prompt's opener list (`cli.py:83-101`: "Good question", "Glad you
ask", "I have slides for that", "I knew you will ask this, I have slides coming", "Remember rule number 672…") and
name nobody. The last pair repeats the first question on purpose, to show `drop_duplicates` (`cli.py:233`).
`laptop/13` copies them into the bind-mounted `data/` from the laptop. The `--prepare` run on them is real:
`Shape: (19, 2)`, the head, then `train.jsonl` (17 lines) and `test.jsonl` (2 lines): `train_test_split(test_size=0.1,
random_state=42)` on 19 rows (`dataset-creator/09-10`).

### `laptop/` — your laptop's terminal

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-env.txt` | extra | date, `x86_64`, Docker 29.8.2, git 2.54.0, `student`, uid 1000, `~/AC215` |
| `01-x-clone.txt` | extra (README.md:34 links the repo; no clone command) | `git clone https://github.com/dlops-io/llm-finetuning.git` → `Cloning into 'llm-finetuning'...` |
| `02-x-git-log.txt` | extra | `44ef6f0 …`, `2026-10-05 22:52:07 -0400 remove pipfile from gemini-finetuning` = the pin; branches `main`, `pipenv` |
| `03-x-ls.txt` | extra | `.gitignore README.md autotrain-runner dataset-creator env.dev gemini-finetuner images`; each container folder: `Dockerfile cli.py docker-entrypoint.sh docker-shell.sh pyproject.toml uv.lock` (no `data/`: deleted in `6e4c3f7`) |
| `04-x-env-dev.txt` | extra (digest Step 1) | `cat env.dev`: the ten lines, the three "CHANGE TO YOUR …" comments |
| `05-x-mkdir-secrets.txt` | **README.md:50** (no command given) | `mkdir secrets` in `~/AC215`, next to the clone |
| `06-x-ls-workspace.txt` | extra (README.md:54-62 layout) | `llm-finetuning` and `secrets` side by side; `secrets` empty (the key cannot be made here) |
| `07-docker-shell-dataset-creator.txt` (+ `.plain.txt`) | **README.md:87** (in `dataset-creator`, README.md:83) | `sh docker-shell.sh` in an 80×40 terminal: BuildKit's `[+] Building 45.1s (11/11) FINISHED` (the six steps, `[2/6] RUN set -ex; …` 26.0 s, `[5/6] RUN uv sync --frozen` 9.0 s), the banner (`Container is running!!!`, `Architecture: x86_64`, `Environment ready! Virtual environment activated.`, `Python version: Python 3.12.16`, `UV version: uv 0.13.6 (x86_64-unknown-linux-gnu)`, `Activating virtual environment...`), the prompt **`app@6f5113cdb660:/app$`** (no `(app)` prefix: digest Step 4), and `exit` at the end of the session. `.plain.txt` = the build's step log (622 lines: apt, pip, the 133 `+ package==version` of `uv sync`) |
| `08-x-docker-ps.txt` | extra | the container `llm-dataset-creator`, `PORTS` empty |
| `09-x-docker-images.txt` | extra | `llm-dataset-creator:latest` **1.64GB**; the `python:3.12-slim-bookworm` line (124MB) is the capture's rebuilt base (see below) |
| `10-x-mounts.txt` | extra | `…/AC215/llm-finetuning/dataset-creator -> /app`, `…/AC215/secrets -> /secrets`; `GCP_PROJECT=ac215-project`, `GCS_BUCKET_NAME=cheese-dataset`, `GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json`; `ports: {}  user: app  workdir: /app` |
| `11-x-docker-shell-again.txt` | extra (digest §6.11) | a second `sh docker-shell.sh` while the first runs: the build, all `CACHED`, `Building 0.0s`, then **`docker: Error response from daemon: Conflict. The container name "/llm-dataset-creator" is already in use by container "6f5113cd…"`** (the 80-column terminal wraps it; scenes join the lines), exit 125 |
| `12-x-exec-no-venv.txt` | extra (digest §6.11) | `docker exec llm-dataset-creator bash -c 'which python; python -c "import pandas"'` → `/usr/local/bin/python`, `ModuleNotFoundError: No module named 'pandas'`: a `docker exec` shell skips the entrypoint, so the venv is not active |
| `13-x-scripted-data.txt` | extra (**scripted**) | `cp ~/scripted/cheese_qa_*.txt data/; ls -la data`: the five scripted files beside the 1-byte `instruct-dataset.csv` left by the failed `--prepare` |
| `14-x-ps-after-exit.txt` | extra | after `exit` in 07: `docker ps -a` is empty (`--rm`) |
| `15-x-data-on-host.txt` | extra | the bind mount left `data/` on the laptop: the five inputs, `instruct-dataset.csv` 5988 B, `train.csv`, `test.csv`, `train.jsonl` 6868 B, `test.jsonl` 774 B; `git status --ignored`: `!! dataset-creator/data/` |
| `16-x-diff-folders.txt` | extra (digest Step 9) | `uv.lock: identical`, `pyproject.toml: identical`, `Dockerfile: identical`; the two `docker-shell.sh` differ by one blank line (6) and `IMAGE_NAME` (10/9) |
| `17-x-cd-gemini-finetuner.txt` | extra (README.md:236 "Make sure you are inside the gemini-finetuner folder") | `cd ../gemini-finetuner && pwd && ls` |
| `18-docker-shell-gemini-finetuner.txt` (+ `.plain.txt`) | **README.md:240** | `sh docker-shell.sh` in `gemini-finetuner`: `[+] Building 0.0s (11/11) FINISHED`, `CACHED [2/6]` … `CACHED [5/6] RUN uv sync --frozen`, `[6/6] COPY --chown=app:app . ./`, the same banner, prompt **`app@2a2550dec953:/app$`**, `exit` |
| `19-x-docker-images.txt` | extra | `gemini-finetuner:latest` 1.64GB beside `llm-dataset-creator:latest` 1.64GB (shared layers) |
| `20-x-dash.txt` | extra (digest §6.1, E3: `/bin/sh` on Debian/Ubuntu/WSL is dash) | `dash docker-shell.sh` → **`docker-shell.sh: 8: source: not found`**, exit 127: what `sh docker-shell.sh` prints on those systems. Fix: `bash docker-shell.sh` |
| `21-x-wrong-folder.txt` | extra (digest §6.2, README.md:68) | `sh dataset-creator/docker-shell.sh` from the repo root → `dataset-creator/docker-shell.sh: source: line 8: can't open '../env.dev': No such file or directory`, exit 2 (BusyBox's wording; bash says `line 8: ../env.dev: No such file or directory`) |
| `22-x-image-rm.txt` | extra (teardown) | `docker image rm llm-dataset-creator gemini-finetuner` → `Untagged:`/`Deleted:` for both |

### `dataset-creator/` — typed at the `llm-dataset-creator` container's prompt

While the session of `laptop/07` was open, each command ran in that container as user `app` in `/app`, after
activating `/.venv` exactly as `docker-entrypoint.sh:12` does (`docker exec` from a second terminal, stderr joined to
stdout; the output is what the session's terminal shows). The prompt to draw is `app@6f5113cdb660:/app$`.

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-whoami.txt` | extra | `app`, uid 1000, `/app`, `/.venv/bin/python`, Python 3.12.16, uv 0.13.6, `VIRTUAL_ENV=/.venv`, `GCP_PROJECT=ac215-project`, `GCS_BUCKET_NAME=cheese-dataset`, `GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json` |
| `01-ls-secrets.txt` | **README.md:69** (tip) | `ls -la /secrets`: `total 0`, only `.` and `..`: **no key** |
| `02-x-packages.txt` | extra | the versions above, `packages in /.venv: 133`, `587M /.venv` |
| `03-x-ls-app.txt` | extra | `/app` = the bind-mounted folder (six files, owned by `app` = uid 1000 = the laptop's `student`) |
| `04-help.txt` | **README.md:93** | `usage: cli.py [-h] [--generate] [--prepare] [--upload]`, `CLI`, the four options; works without a key |
| `05-generate.txt` | **README.md:103** | the five batches, each `Error occurred while generating content: File /secrets/llm-service-account.json was not found.`, **exit 0** |
| `06-x-ls-data.txt` | extra | `data/` exists and is empty |
| `07-prepare-no-data.txt` | **README.md:184** (run right after 05, as a student would) | `Shape: (0, 0)`, `Empty DataFrame`, traceback, `KeyError: 'question'`, exit 1 |
| `08-x-ls-data-scripted.txt` | extra (**scripted**) | the five scripted files in `data/` and the first 400 bytes of `cheese_qa_0.txt` |
| `09-prepare.txt` | **README.md:184** (on the **scripted** data) | `Processing file: data/cheese_qa_0.txt` … `_4.txt`, `Number of errors: 0`, `[]`, **`Shape: (19, 2)`**, the 5-row head (`question`, `answer`) |
| `10-x-ls-data-after.txt` | extra | the five outputs; `wc -l`: `test.jsonl` 2, `train.jsonl` 17, `instruct-dataset.csv` 20 lines (multi-line answers in CSV quoting would show more; these have none) |
| `11-x-train-jsonl-head.txt` | extra | `{"contents":[{"role":"user","parts":[{"text":"What makes Comte different from Gruyere?"}]},{"role":"model","parts":[{"text":"Glad you ask! …` (one line per example) |
| `12-x-jsonl-pretty.txt` | extra (compare README.md:191-212) | the same first line through `python -m json.tool`: the README's `contents` / `role` / `parts` / `text` nesting |
| `13-x-csv-head.txt` | extra | `train.csv`: `text`, `"human: … \nbot: …"`; `instruct-dataset.csv`: `question,answer` |
| `14-upload.txt` | **README.md:221** | `upload()`, traceback from `storage.Client()`, `DefaultCredentialsError: File /secrets/llm-service-account.json was not found.`, exit 1 |

### `gemini-finetuner/` — typed at the `gemini-finetuner` container's prompt

Same method, during the session of `laptop/18`; prompt `app@2a2550dec953:/app$`.

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-whoami.txt` | extra | `app`, `/app`, `/.venv/bin/python`, Python 3.12.16, `GCP_PROJECT=ac215-project`, `/secrets` empty |
| `01-help.txt` | **README.md:246** | `usage: cli.py [-h] [--train] [--chat]`, `--train     Train model`, `--chat      Chat with model` |
| `02-train.txt` | **README.md:256** | `CLI Arguments: Namespace(train=True, chat=False)`, `train()`, the `ExperimentalWarning`, `DefaultCredentialsError`, exit 1 |
| `03-chat.txt` | **README.md:285** | `chat()`, `query:  How is cheese made in Greece? Answer pavlos style?`, `Using serving location: us`, `DefaultCredentialsError`, exit 1 (mask the persona's first name in the query line on screen) |
| `04-x-dataset-uris.txt` | extra (digest Step 3, E1) | `grep -n 'gs://' cli.py` → lines 10-11, both `gs://cheese-dataset/llm-finetune-dataset-small/…  # Replace with your dataset` |

### README step → capture

| README | command | capture |
| --- | --- | --- |
| 38-49 | (GCP Console: service account, roles, JSON key) | not captured: console clicks, no GCP account → schematic drawing tagged `illustration` (field values: `llm-service-account`, Storage Admin, Agent Platform User = `roles/aiplatform.user`, KEYS → ADD Key → JSON) |
| 50 | (create `secrets/` next to the repo, put the key in it) | `laptop/05`, `06` (folder only; no key exists here) |
| 87 | `sh docker-shell.sh` | `laptop/07` |
| 93 | `python cli.py --help` | `dataset-creator/04` |
| 69 | `ls -la /secrets` | `dataset-creator/01`, `gemini-finetuner/00` |
| 103 | `python cli.py --generate` | `dataset-creator/05` (real failure, no key); success: `expected/readme-generate-sample-qa.txt` |
| 154 | `NUM_ITERATIONS = 5` (an edit, not a command) | `source/dataset-creator/cli.py:170` |
| 184 | `python cli.py --prepare` | `dataset-creator/07` (after the failed generate), `09` (scripted data, real run); format: `expected/readme-prepare-gemini-format.txt` |
| 221 | `python cli.py --upload` | `dataset-creator/14` (real failure, no key); success output: not documented by the README |
| 240 | `sh docker-shell.sh` | `laptop/18` |
| 246 | `python cli.py --help` | `gemini-finetuner/01` |
| 256 | `python cli.py --train` | `gemini-finetuner/02` (real failure, no key); success output: not documented by the README |
| 261, 308-316 | (Agent Platform → Tuning console: job status, Training Monitor, Data distribution) | not captured: console → schematic drawing tagged `illustration`; the README's screenshots are not shown |
| 265-278 | (Cost of Fine-tuning, nothing to run) | `expected/readme-cost-table.txt` |
| 285 | `python cli.py --chat` | `gemini-finetuner/03` (real failure, no key); success: `expected/readme-chat-example.txt` |
| 303-306 | (hosted demo `ac215-llm-rag.dlops.io/finetunechat`) | not visited; at most mentioned |

### `expected/` — what the tutorial documents (not produced here)

Made by `terminal/expected_outputs.py` from `source/README.md` and the Colab JSON. The first line of each file says
where it comes from; names are masked (`‹instructor›`; the uploader's Hugging Face account → `‹hf-user›`). Masking
changes the width of a few pandas display rows (`colab-c55`); that is the only effect.

**`expected` — the README's own outputs and texts** (tag `expected`):

| file | source | shows |
| --- | --- | --- |
| `readme-generate-sample-qa.txt` | README.md:163-175 | two sample `--generate` objects (pasta filata; Parmigiano-Reggiano) with the **old** openers ("Welcome welcome welcome, cheese lovers! …", "Yello - this is ‹instructor› your cheese monker …"), each cut with `...` |
| `readme-prepare-gemini-format.txt` | README.md:191-212 | the Gemini tuning format, pretty-printed (one line per example in the real files: `dataset-creator/11-12`) |
| `readme-system-prompt-excerpt.txt` | README.md:114-135 | the README's excerpt of the system prompt (older than `cli.py:83-101`: digest E4) |
| `readme-input-prompt.txt` | README.md:143-145 | the input prompt (word for word `cli.py:169`) |
| `readme-cost-table.txt` | README.md:267-278 | "Gemini 1.5 Flash Tuning is 0.008 USD per 1,000 tokens", the two-row table (3 epochs; $112.73 for 16,444 documents "Way too much data", $0.573 for 88), the pricing link. Stale: the code tunes `gemini-3.1-flash-lite` for 1 epoch (digest E6) |
| `readme-chat-example.txt` | README.md:288-301 | "How is cheese made?" → `Fine-tuned LLM Response:` "Yello - this is ‹instructor› your cheese monker, …" (the README's query is older than `cli.py:109`'s) |

Not documented anywhere, so **no output panel** (the scene shows the command and says what to look for, from the
code's `print` lines): a successful `--generate` run's own lines (`Generating batch: 0` … `4` with no error),
`--upload`'s `Uploading file: …` lines (`cli.py:293`), `--train`'s `Training job started. Monitoring progress...` /
`Job name: …` / `Tuned model info: None` (`gemini-finetuner/cli.py:67-97`), the tuning job's duration and actual
cost.

**`recorded` — the Colab's stored outputs** (tag `recorded`): the course notebook "Tutorial - Finetuning with QLoRA"
as downloaded, run by its authors on an **A100** (`metadata.colab.gpuType`); Python 3.13.15, torch 2.11.0+cu128,
transformers 5.16.1, peft 0.20.0, trl 1.14.0, bitsandbytes 0.50.2 (`colab-c08`, `c12`). Each file: the cell's source
after `$ `, then its stored output; HTML outputs (the training table, the side-by-side cards) as text, progress
widgets as their stored start state.

| file | nb cell | shows |
| --- | --- | --- |
| `colab-c08-install.txt` | 8 | `Using Python 3.13.15 environment at: /usr`, `+ bitsandbytes==0.50.2`, `+ trl==1.14.0`, `- torchao==0.10.0` |
| `colab-c10-hf-token.txt` | 10 | `Hugging Face token successfully loaded.` (the token itself never appears) |
| `colab-c12-versions.txt` | 12 | `torch 2.11.0+cu128 \| transformers 5.16.1 \| peft 0.20.0 \| trl 1.14.0 \| bitsandbytes 0.50.2` |
| `colab-c14-drive-mount.txt`, `c16-hf-download.txt` | 14, 16 | `Mounted at /content/drive`; the two snapshot paths under `/content/drive/MyDrive/LLM_cache/` |
| `colab-c21-opt-350m-4bit-model.txt` | 21 | `print(model)` of OPT-350m: `Linear4bit` everywhere, `lm_head` stays `Linear` |
| `colab-c25-tokenize.txt`, `c27-opt-generate.txt` | 25, 27 | `input_ids tensor([[    2, 31414,   127,  7134,   766,    16]] …`; "Hello my cheese name is cheese. / I'm not sure if you're joking or not. …" |
| `colab-c31-gpu-bf16-check.txt` | 31 | "Your GPU supports bfloat16. This notebook still trains in float16, …" (A100 branch; the T4 branch was not recorded) |
| `colab-c36-load-qwen-4bit.txt` | 36 | the download/loading widgets (`config.json`, tokenizer files, `Loading weights: … 0/311`) |
| `colab-c38-num-params.txt` | 38 | `Number of parameters: 375.84896 millions.` |
| `colab-c42-qwen-config.txt` | 42 | `Qwen3Config {…}` with `"quant_method": "bitsandbytes"`, `"bnb_4bit_quant_type": "nf4"`, `"bnb_4bit_use_double_quant": true`, `"tie_word_embeddings": true` |
| `colab-c45-baseline-generate.txt` | 45 | "what is your name ? I'm trying to get the correct answers …" (the stored output does not start with the prompt: digest E17) |
| `colab-c48-trainable-before.txt` | 48 | `trainable params: 0 \|\| all params: 375848960 \|\| trainable%: 0.0` |
| `colab-c51-gdown-dataset.txt` | 51 | `To: /content/train_16k.jsonl`, `100% 23.2M/23.2M` |
| `colab-c53-sample-1000.txt` | 53 | `(1000, 1)`, one row's `contents` (Gemini format, as Track A writes it) |
| `colab-c55-extract-qa.txt` | 55 | the question/answer frame head (old openers: "Yello - this is ‹instructor› your cheese monker", "Welcome students, this is ‹instructor› …") |
| `colab-c59-chat-template-map.txt`, `c61-train-test-split.txt` | 59, 61 | `Map: … 0/1000`; `(900, 3)` / `(100, 3)` |
| `colab-c63-one-example.txt` | 63 | one training text in Qwen3's chat template: `<\|im_start\|>user …<\|im_end\|>`, `<\|im_start\|>assistant`, an empty `<think>\n\n</think>` block, the answer |
| `colab-c64-token-histogram.txt` | 64 | the histogram is an image (`[image: <Figure …>]`); redraw it, never paste it |
| `colab-c72-sfttrainer-trainable.txt` | 72 | the dataset-preparation widgets, `trainable params: 1146880 \|\| all params: 376995840 \|\| trainable%: 0.3042155584528466` |
| `colab-c75-train.txt` | 75 | the PAD/BOS/EOS notice, **`[450/450 03:36, Epoch 2/2]`**, the loss table (50: 2.007381 … 450: 1.350437), `TrainOutput(global_step=450, training_loss=1.4964344957139757, … 'train_runtime': 217.4211 …)` |
| `colab-c77-tensorboard.txt` | 77 | "Output hidden; open in https://colab.research.google.com to view." (no stored TensorBoard) |
| `colab-c80-eval-loss-perplexity.txt` | 80 | `Samples evaluated: 100`, `Total tokens: 30,681`; **Base (4-bit) 2.6498 / 14.15; Fine-tuned (4-bit + LoRA) 1.3872 / 4.00** |
| `colab-c82-base-vs-finetuned.txt` | 82 | three prompts (fresh vs aged cheese; Gorgonzola dolce vs piccante; "Why is the sky blue?"), base vs fine-tuned answers, cut at 100 new tokens. Both "sky" answers explain it wrongly (refraction; water molecules): the fine-tuned model learned the voice, not physics. Do not present either as correct |
| `colab-c84-save-adapters.txt`, `c86-merge-and-save.txt` | 84, 86 | the saved tokenizer file paths under `LLM_cache/Qwen0.6B-finetune_cheese` and `…_merged` |
| `colab-c88-push-to-hub.txt` | 88 | `✓ Detected Hugging Face username: ‹hf-user›`, `Model successfully uploaded to https://huggingface.co/‹hf-user›/Qwen0.6B-finetune_cheese_merged` (a real person's account in the original: always masked) |

### Not captured here, and how the video shows it

- **The GCP Console** (service account and key, README.md:38-49; the Agent Platform tuning page, README.md:261,
  308-316): no GCP account. Schematic drawings tagged `illustration`, with the README's field values; the README's two
  console screenshots are not shown.
- **Live Gemini generation** (`--generate` with a key), **upload**, **the tuning job** (`--train`), its **run time and
  cost**, and **the chat with a tuned endpoint** (`--chat`): need GCP credentials and a billed project. The real
  no-key failures are captured; the success side comes from `expected/readme-*` (tag `expected`) and, for the data
  path, the real `--prepare` on scripted data. No live tuned-model answer exists in this repository; the only
  documented one is the README's (older query).
- **The Colab QLoRA run**: needs a GPU (none here). Shown from the stored outputs (`expected/colab-*`, tag
  `recorded`). SLIDES.md proposes a T4 re-run with a measured peak memory; that could not be done here, so the video
  has no measured T4 numbers.
- **The hosted demo** (README.md:303): not visited.
- **Apple Silicon**: not captured (digest §6.9: every locked package has an aarch64 wheel).

### Differences from a real laptop, and how the scenes handle them

- **Base image.** `python:3.12-slim-bookworm` was pulled into the laptop's own engine and rebuilt under the same name
  with the recording proxy's CA and https apt sources (`capture-only/base-python-3.12-slim-bookworm.Dockerfile`, build
  log beside it), so the tutorial's Dockerfiles built unchanged. On a real laptop that line in `docker images` is the
  official image (about 120-130 MB, a different ID).
- **Proxy relay.** The laptop's git, engine and containers reached the internet through `proxy_relay.py` (container
  `l08-relay`); nothing about it shows in the captures except through `docker info`, which was not captured.
- **File modes.** Files the container wrote through the capture's `docker exec` show `-rw-rw-rw-` and `data/` shows
  `drwxrwxrwx` (`dataset-creator/08`, `10`; `laptop/13`, `15`): the capture laptop's sessions ran with umask 000 (the
  directories its setup created show the same, `laptop/06`). With the usual umask 022 a student sees `-rw-r--r--` and
  `drwxr-xr-x`. Scenes that show these listings either show the files' names and sizes only or note this.
- **Linux uid 1000.** The laptop's user is uid 1000, like the container's `app`, so the bind-mounted `data/` was
  writable. On a Linux host with another uid, `--generate` may fail with `PermissionError … 'data'` (digest §6.6; not
  reproduced here).
- **`sh`.** BusyBox `ash` on this laptop (accepts `source`, like macOS); `laptop/20` shows dash, the `/bin/sh` of
  Debian/Ubuntu/WSL.
- **Timing.** The first build took 45.1 s on this machine with a fast network; on a laptop with Docker Desktop expect
  several minutes (the lock pulls chromadb, onnxruntime and langchain, which the code never imports).

### Surprises (README vs reality)

1. **`--generate` "succeeds" without a key** (exit 0, five swallowed errors), and the failure surfaces one command
   later as `KeyError: 'question'` in `--prepare`, after it has written a 1-byte `instruct-dataset.csv`
   (`dataset-creator/05`, `07`, `08`).
2. **`sh docker-shell.sh` fails on Debian/Ubuntu/WSL** (`docker-shell.sh: 8: source: not found`, `laptop/20`); it works
   on macOS and on this BusyBox laptop. `bash docker-shell.sh` works everywhere.
3. **The second image builds in 0.0 s**: the two folders' `Dockerfile`, `pyproject.toml` and `uv.lock` are identical,
   so every layer but the last is cached (`laptop/16`, `18`).
4. **The `(app)` venv prefix never shows** in the container prompt, although the venv is active (`which python` →
   `/.venv/bin/python`); a `docker exec` shell, by contrast, has no venv (`laptop/12`).
5. **The README's sample outputs use the old openers and an older chat query** ("How is cheese made?" vs the code's
   "How is cheese made in Greece? Answer pavlos style?", `gemini-finetuner/03`).
6. **`--train` prints an `ExperimentalWarning`** from google-genai 1.39.1 before anything else (`gemini-finetuner/02`).
7. **The dataset URIs and the endpoint still point at the course's resources** (`gemini-finetuner/04`;
   `cli.redacted.py:107`): a student must edit `cli.py:10-11` and `:107` (digest E1).
8. **The image is 1.64 GB** for a CLI that imports four libraries; `/.venv` holds 133 packages (587 MB).
