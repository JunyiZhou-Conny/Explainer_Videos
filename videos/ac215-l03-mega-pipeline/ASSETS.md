# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

## `source/` — the tutorial's own files

From [dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline), branch `main`, commit
`c6bbc9ba88984e1234b68ccf5cdf7c00f7e9accc` (2026-09-27, still the head of `main` on 2026-10-13),
copied unchanged with `git show <commit>:<path>` (each file checked against its git blob hash), at
the repo's own relative paths so that a code panel's `path · lines a–b` matches a viewer's clone:

- `README.md` (the main README: overview, bucket prefixes `:74-80`, credentials `:90-106`, the five
  tasks `:110-124`, quick reference `:128-165`, sample Dockerfile `:175-225`, Windows notes
  `:227-236`), `.gitignore`;
- for each component `transcribe_audio/`, `generate_text/`, `synthesis_audio_en/`, `translate_text/`,
  `synthesis_audio/`: its `README.md` and `cli.py`, and its `.gitignore` (there is none in
  `generate_text/`); plus `generate_text/pyproject.toml` (the committed `requires-python = ">=3.14"`),
  `generate_text/main.py` and the bonus `synthesis_audio/cli_11.py`.

`source/solution-branch/transcribe_audio/` holds `docker-shell.sh`, `Dockerfile`, `pyproject.toml` and
`README.md` from the `solution` branch, commit `8083187ec0e022ba34440892689145ff703a34e0`
(2025-09-22), for the "where the course goes next" panel (secrets mounted at `/secrets` at run time,
`docker-shell.sh:95-100`). The two PNGs of the repo are not copied: the bucket image is a console
screenshot and must be redrawn as a schematic (`illustration`).

Course material by the AC215 teaching staff (Harvard IACS), used for study with the instructor's
permission.

## `terminal/` — real terminal sessions

Captured on **2026-10-13** (01:42–01:51 UTC) by `terminal/capture.sh`, which builds two
capture-only images and then runs `terminal/run_steps.sh` part by part (`a a2 b c d e final`). Each
file starts with the command (`$ ...`), then its output, then its exit status (`[exit N]`); ANSI
colour codes are removed. Every README command of the tutorial is run in README order, exactly as
written, except for the additions listed under "Differences" below.

**"Your laptop"** is two things working on the same folder:

- **the laptop's shell** (git, uv, ls, cat): a fresh `debian:12` container per command (image
  `l03-capture/laptop:debian12`: Debian 12 with git 2.39.5, curl and Debian's python3 3.11.2, user
  `student`, uid 1000), started with `bash -l` like a new terminal, the home folder bind-mounted so
  the clone and uv persist between commands;
- **the laptop's Docker**: Docker Engine 29.8.2 (client and server, API 1.56, linux/amd64,
  containerd v2.3.6, runc 1.5.1, buildx v0.37.1, BuildKit "default" builder with the docker driver)
  on the capture machine, run from the same folder, so `"$(pwd)"` is that folder.

Inside the containers: the five images built from the README's Dockerfile on
`python:3.12-slim-bookworm` (Python 3.12.15, Debian 12.15, image digest
`sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258`), with pip upgraded from
25.0.1 to 26.2.1 and **uv 0.13.0** installed by the Dockerfile's `pip install uv`. The laptop's uv is
also 0.13.0 (installed by the README's own installer). Versions marked below are "at the time of
recording".

| folder | what |
| --- | --- |
| `laptop/` | everything typed in the laptop's terminal: clone, uv install, `uv init --bare`, every `docker build` / `docker images` / `docker run` typed on the host, extra checks and gotcha demos (numbered 00–26 for A, 30s B, 40s C, 50s D, 60s E, 70s wrap-up) |
| `transcribe_audio/` … `synthesis_audio/` | commands typed at each container's prompt (`app@<id>:/app$`): `uv add`, `cat pyproject.toml`, `python cli.py …` |
| `expected/` | README text for the `--help` output of C, D and E, which can't run here (see below); each file's first line says where it comes from |
| `files/` | the Dockerfile each component's README has a student write (`<component>.Dockerfile`), and each `pyproject.toml` as `uv add` left it on the laptop (`<component>.pyproject.toml`) |

### `laptop/` — the laptop's terminal

| file | README step | what it shows |
| --- | --- | --- |
| `00-laptop.txt` | extra | the laptop shell: Debian 12, Python 3.11.2, git 2.39.5, the date (2026-10-13 01:42 UTC) |
| `01-docker-version.txt` | extra | Docker client and engine 29.8.2 |
| `02-base-image.txt` | extra | `docker pull python:3.12-slim-bookworm` (already up to date on this machine) and its Python 3.12.15 |
| `03-clone.txt` | README.md:33 | `git clone https://github.com/dlops-io/mega-pipeline.git` |
| `04-ls.txt` | README.md:34 + extra | after `cd mega-pipeline`: `ls`, the commit (`c6bbc9b`), branch `main` |
| `05-ls-components.txt` | extra | `ls -a` of the five folders: `README.md cli.py secrets` (+ `.gitignore`), no Dockerfile anywhere; `generate_text/` already has `pyproject.toml` and `main.py` and no `.gitignore`; `synthesis_audio/` has `cli_11.py` |
| `06-uv-missing.txt` | extra (A README:26 "Don't have uv installed?") | `uv --version` → `uv: command not found` on a laptop without uv |
| `07-uv-install.txt` | transcribe_audio/README.md:29 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` → uv 0.13.0 into `~/.local/bin` |
| `08-uv-version.txt` | README:34 "restart your terminal" | `uv --version` in a new terminal → `uv 0.13.0` |
| `09-uv-init.txt` | transcribe_audio/README.md:22 | `uv init --bare` → ``Initialized project `transcribe-audio` `` |
| `10-cat-pyproject.txt` | extra | the scaffold: `requires-python = ">=3.11"` (the laptop's Python 3.11), `dependencies = []` |
| `11-ls-before-build.txt` | README:40-90 (Dockerfile written) + extra | `ls -a` with the new `Dockerfile` and `pyproject.toml`; `git status` → `working tree clean` (both are in `transcribe_audio/.gitignore`) |
| `12-build.txt` | transcribe_audio/README.md:95 (command: digest §4 step 5) | the **first** build, full plain log (1,393 lines): `[2/5]` apt installs 237 packages for `build-essential ffmpeg` (205 MB download, 46.9 s), pip 25.0.1 → 26.2.1, uv 0.13.0, ten harmless `update-alternatives: warning` lines; `[5/5] RUN uv sync` → `Using CPython 3.12.15 interpreter at: /usr/local/bin/python3`, `Resolved 1 package`; the `SecretsUsedInArgOrEnv` build warning (line 10) |
| `13-images.txt` | extra | `docker images transcribe_audio` → 1.35 GB on disk (357 MB content) before any package is baked in |
| `14-host-after-uv-add.txt` | transcribe_audio/README.md:110 | back on the laptop after the in-container `uv add`: `pyproject.toml` lists the three packages, `uv.lock` (138,445 bytes) exists, `input_audios/` and `text_prompts/` appeared, `git status --short` shows only ` M cli.py` |
| `15-rebuild.txt` | README:110 "re-build the image" | the rebuild as the terminal shows it (live progress view, 80 columns): `CACHED [2/5]`, `CACHED [3/5]`, `[4/5] COPY`, `[5/5] RUN uv sync 2.9s`, `Building 9.9s` |
| `15-rebuild.plain.txt` | same build | its full log: `uv sync` now installs the 26 locked packages |
| `16-images-after.txt` | extra | 1.48 GB (388 MB content) with the packages |
| `17-history.txt` | extra | `docker history transcribe_audio`: one row per Dockerfile line; the apt `RUN` layer is 842 MB, `uv sync` 105 MB, `COPY` 180 kB. The four rows `ENV SSL_CERT_FILE…`, `RUN … sed …`, `COPY ca-bundle.crt …` (×2) come from the capture-only base, not from the tutorial |
| `18-g16-entrypoint.txt` | extra, gotcha G16 | `docker run --rm -v "$(pwd):/app" transcribe_audio python cli.py -d` → `/usr/local/bin/python: … cannot execute binary file`, exit 126 |
| `19-g16-fix.txt` | extra, G16 fix | `… transcribe_audio -c "source /home/app/.venv/bin/activate && python cli.py --help"` → the usage text |
| `20-g1-git-ignores-key.txt` | extra, G1 | with a **placeholder** `secrets/mega-pipeline.json` (see below): Git ignores it (`transcribe_audio/.gitignore:3:/secrets`) |
| `21-g1-rebuild-with-key.txt` | extra, G1 | rebuild (plain log) with the placeholder in the folder |
| `22-g1-key-in-image.txt` | extra, G1 | `docker run --rm --entrypoint ls transcribe_audio -la /app/secrets` → `mega-pipeline.json` is inside the image |
| `23-g1-dockerignore.txt` | extra, G1 fix | a `.dockerignore` containing `secrets/` |
| `24-g1-rebuild-dockerignore.txt` | extra, G1 fix | rebuild with it |
| `25-g1-key-not-in-image.txt` | extra, G1 fix | `ls: cannot access '/app/secrets': No such file or directory` |
| `26-g21-no-pyproject.txt` | extra, G21 | the README's build in a copy of the folder without `pyproject.toml` → ``error: No `pyproject.toml` found in current directory or any parent directory`` at `[5/5] RUN uv sync`, exit 1 |
| `30-b-ls.txt` | generate_text/README.md:13 + extra | `ls -a` and the committed `pyproject.toml` (`requires-python = ">=3.14"`, both packages already listed) |
| `31-b-uv-init.txt` | generate_text/README.md:22 | `uv init --bare` → ``error: Project is already initialized in `/home/student/mega-pipeline/generate_text` (`pyproject.toml` file exists)``, exit 2 |
| `32-b-build.txt` / `.plain.txt` | generate_text/README.md:95 | first build with `ARG DEBIAN_PACKAGES="build-essential"` (46 apt packages, 73.8 MB, `[2/5]` 22.8 s, `Building 54.0s`); the plain log shows `uv sync` **downloading CPython 3.15.0** (`Downloading cpython-3.15.0-linux-x86_64-gnu (download) (35.9MiB)`, `Using CPython 3.15.0`) because of `>=3.14`, then installing 34 packages (google-genai 2.30.0) |
| `33-b-rebuild.txt` / `.plain.txt` | README:110 | rebuild after `uv add`: apt layer cached, CPython 3.15.0 downloaded again |
| `34-b-fix-requires-python.txt` | extra, the G3 fix | `requires-python = ">=3.12"`; `git status --short .` → ` M pyproject.toml`, `?? Dockerfile`, `?? uv.lock` (no `.gitignore` in this folder) |
| `35-b-rebuild-312.txt` / `.plain.txt` | extra, the G3 fix | `Using CPython 3.12.15 interpreter at: /usr/local/bin/python3`, 35 packages re-resolved |
| `40-c-uv-init.txt` | synthesis_audio_en/README.md:22 + extra | ``Initialized project `synthesis-audio-en` `` and the scaffold (`>=3.11`) |
| `41-c-build.txt` / `.plain.txt` | synthesis_audio_en/README.md:95 | first build: `CACHED [2/5]` — B's apt layer is reused, because the Dockerfile text up to that line is identical; `Building 0.6s` |
| `42-c-rebuild.txt` / `.plain.txt` | README:104-110 | rebuild after `uv add` (24 packages) |
| `50-d-uv-init.txt`, `51-d-build.*`, `52-d-rebuild.*` | translate_text/README.md:22, :95, :104-110 | the same for D (`translate-text`; 25 packages incl. google-cloud-translate 3.28.0) |
| `60-e-uv-init.txt`, `61-e-build.*`, `62-e-rebuild.*` | synthesis_audio/README.md:22, :95, :104-110, :146 | the same for E (`synthesis-audio`; 24 packages, then `requests` added) |
| `70-images-all.txt` | extra | all five images: transcribe_audio 1.48 GB, the other four 842–846 MB each |
| `71-git-status.txt` | extra | `git status` at the repo root after all five: only `generate_text/` (no `.gitignore`) and the edited `transcribe_audio/cli.py` show; the other folders' Dockerfiles, `pyproject.toml` and `uv.lock` are invisible to Git (erratum E12) |
| `72-cleanup.txt` | extra (teardown, not in the README) | `docker image rm transcribe_audio generate_text synthesis_audio_en translate_text synthesis_audio` |

### Inside the containers

| file | README step | what it shows |
| --- | --- | --- |
| `transcribe_audio/01-docker-run-tty.txt` | transcribe_audio/README.md:99 | the README's exact `docker run --rm -ti -v "$(pwd):/app" transcribe_audio` in a real terminal, before `uv add`: the prompt `app@5b4d4981ec25:/app$` (no `(transcribe-audio)` prefix, G19), `which python` → `/home/app/.venv/bin/python`, Python 3.12.15, `ls -a` of the mounted folder, `echo $GOOGLE_APPLICATION_CREDENTIALS` → `secrets/mega-pipeline.json`, `python cli.py --help` → `ModuleNotFoundError: No module named 'google'` (packages not added yet), `exit` (exit status 1 = that last command's) |
| `transcribe_audio/02-uv-add.txt` | transcribe_audio/README.md:105-110 | `uv add google-cloud-storage google-cloud-speech ffmpeg-python` → `Resolved 27 packages`, 26 installed (google-cloud-speech 2.41.0, google-cloud-storage 3.17.0, ffmpeg-python 0.2.0, grpcio 1.84.0, protobuf 7.36.2 …) |
| `transcribe_audio/03-cat-pyproject.txt`, `04-ls.txt` | extra | the three dependencies with lower bounds; `uv.lock` (138,445 bytes) next to `cli.py`, all owned by `app` |
| `transcribe_audio/05-help.txt` | transcribe_audio/README.md:117 | `python cli.py --help` — identical, line for line, to the README's block (`:118-126`) |
| `transcribe_audio/06-group-name.txt` | transcribe_audio/README.md:114 | the container sees the laptop's edit: `21:group_name = "group-01" …` |
| `transcribe_audio/07-download.txt` | README.md:134 / transcribe_audio/README.md:131 | `python cli.py --download` **without the Canvas key**: `Args: Namespace(download=True, transcribe=False, upload=False)` and `download` print (as they would with a key), then `google.auth.exceptions.DefaultCredentialsError: File secrets/mega-pipeline.json was not found.` (kept because it is instructive: this is what a missing or misplaced key looks like, G5) |
| `transcribe_audio/08-ls-after-download.txt` | extra | `input_audios/` and `text_prompts/group-01/` were created (empty) before the failure |
| `transcribe_audio/09-uv-tree.txt`, `10-venv-where.txt` | extra | `uv tree --depth 1`; the venv is `/home/app/.venv`, outside the mount, with the new packages in it |
| `transcribe_audio/11-g10-new-container.txt` | extra, G10 | a **new** container from the image built before `uv add`: `ModuleNotFoundError` again — the packages lived in the old container |
| `transcribe_audio/12-after-rebuild.txt` | extra | after `15-rebuild`: `imports ok` with no `uv add`, uv 0.13.0, Python 3.12.15 |
| `transcribe_audio/13-g7-root-owned.txt` | extra, G7 | the folder owned by root (a Linux host or VM where you work as root): `uid=1000(app)`, `uv add requests` → ``error: failed to create file `/app/pyproject.toml`: Permission denied (os error 13)`` |
| `generate_text/01-python-version.txt` | extra, G3 | after the README's build: the venv's Python is **3.15.0**, `/home/app/.local/share/uv/python/cpython-3.15.0-linux-x86_64-gnu/bin/python3.15`, not the image's 3.12 |
| `generate_text/02-uv-add.txt` | generate_text/README.md:104-106 | `uv add google-cloud-storage google-genai` → `Resolved 35 packages`, `Checked 34 packages`: nothing new (the committed `pyproject.toml` already had both); it only writes `uv.lock` to the laptop |
| `generate_text/03-cat-pyproject.txt` | extra | `pyproject.toml` unchanged by `uv add` |
| `generate_text/04-help.txt` | generate_text/README.md:115 | identical to the README's block (`:116-124`); works without the key (the Gemini client loads credentials lazily) |
| `generate_text/05-python-version-312.txt`, `06-help-312.txt` | extra, G3 fix | after `35-b-rebuild-312`: Python 3.12.15 from `/usr/local/bin/python3.12`, same help |
| `synthesis_audio_en/01-uv-add.txt`, `02-cat-pyproject.txt` | synthesis_audio_en/README.md:104-106 | `uv add google-cloud-storage google-cloud-texttospeech` (25 resolved, 24 installed; google-cloud-texttospeech 2.38.0) |
| `synthesis_audio_en/03-help.txt` | synthesis_audio_en/README.md:115 | **without the key** `--help` fails at import (`cli.py` line 22 builds `TextToSpeechLongAudioSynthesizeClient()`): `DefaultCredentialsError: File secrets/mega-pipeline.json was not found.` Kept because it is instructive (G5: in C, D and E even `--help` needs the key). The README's output is in `expected/` |
| `translate_text/01-uv-add.txt`, `02-cat-pyproject.txt`, `03-help.txt` | translate_text/README.md:104-106, :115 | the same for D (`translate.Client()` at `cli.py` line 20) |
| `synthesis_audio/01-uv-add.txt` … `03-help.txt` | synthesis_audio/README.md:104-106, :115 | the same for E (`cli.py` line 21) |
| `synthesis_audio/04-bonus-uv-add-requests.txt` | synthesis_audio/README.md:146 | `uv add requests` → `Checked 24 packages`: `requests` was already installed (a google-cloud-storage dependency); `files/synthesis_audio.pyproject.toml` shows it added as `"requests>=2.34.2"` |
| `synthesis_audio/05-bonus-cli11-download.txt` | synthesis_audio/README.md:151 | `python cli_11.py --download` without an ElevenLabs key file → `FileNotFoundError: … 'secrets/11lab_api_key.txt'` at line 33 (the key is read at import). Kept to show that the bonus needs the key file before any flag works |

### Differences from a student's laptop, and how the scenes handle them

- **The `FROM` line.** Builds here need the capture proxy's CA certificate and https apt sources,
  which the tutorial's Dockerfile can't provide. So the folder's `Dockerfile` has line 1
  `FROM l03-capture/python:3.12-slim-bookworm`: `python:3.12-slim-bookworm` plus the CA bundle, https
  apt sources and `SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE`/`PIP_CERT` (defined in `capture.sh`). Every
  other line is the README's (`files/<component>.Dockerfile` is the version a student writes: the
  component README's code blocks in order, with the `FROM` line from its prose at `:41`; same line
  count, so the warning's "(line 10)" and the `Dockerfile:27` error excerpt match). Visible effects:
  the `load metadata for …` and `[1/5] FROM …` lines name the capture base and show `CACHED`/no pull
  (a student's first build pulls `docker.io/library/python:3.12-slim-bookworm`); apt's `Get:` lines say
  `https://deb.debian.org` (a student sees `http://`); `transferring dockerfile: 840B`/`833B` is a few
  bytes more than a student's; `17-history.txt` has four extra base rows. Scenes show the README's
  `FROM` line and skip or cut those lines (`…`).
- **`--network host`** is added to every `docker build` here (the proxy listens on 127.0.0.1), and a
  `DOCKER_CONFIG` "proxies" entry passes the proxy variables to builds and containers. The step files
  show the command as run; scenes type the README's command. Note the component READMEs never spell
  the build command (`transcribe_audio/README.md:95` only says to name the image `transcribe_audio`);
  `docker build -t transcribe_audio .` is the digest's (§4 step 5, erratum E13).
- **In-container commands** (all files in the component folders except `01-docker-run-tty.txt`) were
  typed into one container per list, started like the README's `docker run --rm -ti -v "$(pwd):/app"
  <image>` but with `-i` instead of `-ti` (no terminal; the commands arrive on stdin) and with
  `--network host`. The image's own `CMD` activates the venv, so the environment is the README's.
  Without a terminal there is no prompt in these files and uv prints no progress bars; scenes draw the
  prompt `app@<id>:/app$` as in `01-docker-run-tty.txt`.
- **The group-name edit** (`group-01`, the README's example) was made on the laptop before the
  container of `02-…10-` started, not while it ran (a piped session can't pause for an editor). The
  bind mount makes the two equivalent; `06-group-name.txt` shows the container seeing it.
- **Two capture passes for A.** `laptop/00–13` and `transcribe_audio/01` are from the first pass. In
  that pass the in-container commands were split over two containers by mistake, so `uv add` and
  `--download` ran in different containers; those files were discarded. For the second pass
  (`run_steps.sh` part `a2`: `laptop/14–26`, `transcribe_audio/02–13`) the folder was reset to its
  state after step 13 (the `uv init --bare` scaffold, no `uv.lock`, `cli.py` unchanged) and the image
  rebuilt from the cache (not recorded). Image ids therefore differ between `13-images.txt` and the
  later files; nothing else does. A fresh run of `capture.sh` does both parts in one go.
- **The laptop is Linux.** The folder belongs to uid 1000, which is also `app`'s uid in the image, so
  the container can write to the mount, as Docker Desktop arranges on macOS and Windows.
  `13-g7-root-owned.txt` shows what happens when the uids don't match.
- **Which Python `uv init --bare` finds.** This laptop has Debian 12's Python 3.11.2, so the scaffold
  says `>=3.11` and the image's 3.12 satisfies it. A laptop whose Python (or uv-managed Python) is
  3.13 or newer gets `>=3.13`…, and then its build downloads a separate CPython exactly as
  `generate_text`'s committed `>=3.14` does here (`32-b-build.plain.txt`, G3). Narration: "your
  `requires-python` depends on your laptop; check it".
- **Live view vs. plain log.** Builds 15 and 32–62 were run in a real terminal (80×40 pseudo-terminal,
  `tty_session.py`, rendered with the `pyte` terminal emulator 0.8.2): `NN-….txt` is what the terminal
  shows when the build ends. `NN-….plain.txt` is the same build's step-by-step log, replayed with
  `docker buildx history logs <ref>`; a replay lacks the live log's first line (`#0 building with
  "default" instance using docker driver`) and the closing warning summary. `12-build.txt` and the G1
  and G21 builds are live plain logs (run without a terminal). `transcribe_audio/01-docker-run-tty.txt`
  was rendered by removing ANSI sequences (pyte was not installed yet; the session has no cursor
  movement, so the result is the same).
- **The placeholder key (G1 only).** No real key exists here. For `20–25` a file
  `secrets/mega-pipeline.json` containing `{"placeholder": "stands in for the Canvas key in this
  capture; not a credential"}` (82 bytes) stood where the Canvas key goes, and was deleted after `25`.
  Every other capture ran with no key at all.
- **Image sizes** are this machine's (containerd image store: "disk usage" and "content size");
  Docker Desktop shows one size per image. Versions (uv 0.13.0, pip 26.2.1, Python 3.12.15, CPython
  3.15.0, the package versions) were the newest on 2026-10-13: the narration says "at the time of
  recording".

## `expected/` — what the README documents (not captures)

| file | source | used for |
| --- | --- | --- |
| `synthesis_audio_en-help.txt` | `synthesis_audio_en/README.md:115-123` | C's `python cli.py --help` with the key in place |
| `translate_text-help.txt` | `translate_text/README.md:115-124` | D's `python cli.py --help` with the key in place |
| `synthesis_audio-help.txt` | `synthesis_audio/README.md:115-123` | E's `python cli.py --help`; note the code's description (`synthesis_audio/cli.py:105`) is "Transcribe audio file to text", so a real run prints that line instead of the README's "Synthesis audio from text" (erratum E6) |

Each starts with a `#` header line naming its source; the command line is marked `$`. Scenes tag
these panels `expected` (`expected_tag`). The A and B `--help` outputs were captured for real and match
their README blocks exactly.

## Not captured, and how the video shows them

| README step | why | on screen |
| --- | --- | --- |
| Download `mega-pipeline.json` from Canvas into each `secrets/` (README.md:97-99, component READMEs `:16-17`) | needs a HarvardKey login; the key is a credential | a schematic of the file going into each `secrets/` folder, tagged `illustration`; no file content is ever shown |
| `python cli.py --download / --transcribe / --upload` (A), `--download / --generate / --upload` (B), `--download / --synthesis` (C, E), `--download / --translate / --upload` (D) — README.md:134-164 and each component's "Testing your code locally" | need the shared GCP key (Cloud Storage, Speech-to-Text, Vertex AI Gemini, Text-to-Speech, Translation, all billed to the course project) | the command, typed exactly; no output panel (nothing in the repo documents these outputs: no Colab, no logs); the narration says what to look for (digest §4 steps 10–19, from the code). The only real output is A's `--download` without a key (`transcribe_audio/07-download.txt`), shown as "what a missing key looks like". C/D/E `--help`: `expected/` |
| The leaderboard at `http://ac215-mega-pipeline.dlops.io/` (README.md:54) | a live web page fed by the shared bucket | a schematic leaderboard tagged `illustration` (no screenshot) |
| The bucket and its prefixes (README.md:74-82, `mega-pipeline-bucket.png`) | console screenshot; no access | a schematic drawer/prefix drawing tagged `illustration`, labels from README.md:74-80 |
| `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` and `pip install uv` (component READMEs `:32`, `:34`) | Windows / the alternative installer; the laptop used the curl installer | command only |
| `winpty docker run --rm -ti -v "$(pwd)":/app generate_text` (README.md:235) | needs Windows + Git BASH | command only |
| `docker login -u <USER NAME> -p <ACCESS TOKEN>`, `docker tag …`, `docker push …` (component READMEs `:136-140` / `:160-162`) | needs a Docker Hub account and token; pushing an image that contains the key would publish it (G1) | commands only, with the G1 warning (`laptop/22-g1-key-in-image.txt`) |
| `python cli_11.py --synthesis / --upload` (synthesis_audio/README.md:152-153) | needs an ElevenLabs API key | command only; `synthesis_audio/05-bonus-cli11-download.txt` shows the missing-key-file error |
| The appendix's sample Dockerfile (README.md:175-225) | not built as-is; the component README's version was built | quoted from `source/README.md` with its differences (`set -ex`, the man-page loop, `ARG DEBIAN_PACKAGES="build-essential curl"`, which lacks ffmpeg) |

## Re-running

`PYTHON=<a python with pyte> bash assets/terminal/capture.sh <empty work dir>` (behind the proxy, also
`export CA_BUNDLE=/root/.ccr/ca-bundle.crt`; parts can be run one at a time, `setup` first). It
writes into `assets/terminal/` and removes the five images at the end (`final`); the capture-only
images `l03-capture/python:3.12-slim-bookworm` and `l03-capture/laptop:debian12` stay until removed
by hand. Re-running on a machine whose build cache already has the apt layer turns `12-build.txt`'s
`[2/5]` into `CACHED`.
