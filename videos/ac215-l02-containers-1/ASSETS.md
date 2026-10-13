# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

## `source/` — the tutorial's own files

From [dlops-io/simple-translate](https://github.com/dlops-io/simple-translate) at commit
`62f821bfe09fc1c2ecb0f14354b1f205777c0efa` (main, 2026-09-08; still the head of `main` on
2026-10-13), copied unchanged with `git show <commit>:<path>` so the code panels quote the exact
lines a viewer sees in their own clone. Course material by the AC215 teaching staff (Harvard IACS),
used for study with the instructor's permission.

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | the two sections: *Developing App using Containers* (lines 106-191: the five Dockerfile steps at 132-165, build 170-174, run 176-184, push 186-191) and *Running App on VM using Docker* (203-220); the four-step ladder (9-16); the clone command (50) |
| `Dockerfile.txt` | the solution Dockerfile (29 lines, no newline at the end) |
| `cli.py` | the app: banner/arguments/input (12-23), the translate call and its `RuntimeError` (25-39), the defaults `I love cheese` / `en` / `it` (49, 62, 68) |
| `pyproject.toml` | `requires-python = ">=3.13"` (6), the two dependencies (7-10) |
| `docker-shell.sh` | build + run helper (11, 15) and the commented-out `--platform=linux/amd64` build (12) |
| `docker-build-push.sh` | the multi-arch buildx push (`DOCKER_USERNAME="dlops"` at 11, builder 15-23, push 27) |
| `dot-gitignore.txt` | the repo's `.gitignore`, renamed so that git does not treat it as this folder's ignore file (its line 3, `Dockerfile`, would hide files here) |
| `pipenv-branch/Dockerfile`, `pipenv-branch/docker-shell.sh` | the older Pipenv variant, branch `pipenv` at `3a354d81f787a064aea3ab061359c9a1e223e4d5` (2026-08-28), for comparison only (`FROM python:3.11-slim-buster`, `--platform=linux/amd64` active) |

There is no Colab notebook for this lecture.

## `terminal/` — real terminal sessions

Captured on **2026-10-13** (01:43-02:00 UTC) by `terminal/capture.sh`, which starts a fresh
disposable environment per walkthrough and runs `terminal/run_steps.sh` inside it. Each README
command runs exactly as written, in README order, and its output goes to its own file: the file
starts with the command (`$ ...`), then the output, then its exit status (`[exit N]`). Steps that
are not in the README are marked *extra* below and in `run_steps.sh`.

Two kinds of file:

- **`step` files**: the command runs without a terminal, like in a script. Docker then prints its
  plain progress (BuildKit's `#1 … DONE` log, one line per pull/push event).
- **`istep` files**: the command runs in a real pseudo-terminal (`ptyrun.py`, 80×24; the build views
  100×60), and the lines a person would type at the prompt (`python cli.py …`, `exit`) are typed
  into it when the prompt appears. The file holds what the terminal shows at the end: prompts,
  echoed input, output, Docker's progress redrawn the way a terminal redraws it. Colours are
  dropped. For `docker run -ti` the exit status is the container's (bash's last command). In
  `laptop/19` and `laptop/22` the tab characters of `ls` were expanded to the terminal's 8-column
  tab stops after capture; `ptyrun.py` now does this itself.

| folder | environment | README section |
| --- | --- | --- |
| `laptop/` | a fresh, empty Docker engine standing in for Docker Desktop: `docker:29.8.2-dind` (Docker client and engine 29.8.2, buildx v0.37.2, containerd image store, builder `default`, linux/amd64), user `student` in the `docker` group, git 2.54.0 | *Developing App using Containers*, from `docker container ls` to `docker tag` |
| `laptop-push/` | a second fresh engine, same setup, for the push part | *Pushing Docker Image to Docker Hub* + extras |
| `vm-debian12/` | a fresh `debian:12` container standing in for the Compute Engine VM, with the baseline a GCP Debian image has (`python3`, `sudo`, `curl`, a user `student` with passwordless sudo) | *Running App on VM using Docker* (docker.io 20.10.24) |
| `vm-debian13/` | the same on `debian:13` (the README names no VM image) | *Running App on VM using Docker* (docker.io 26.1.5) |
| `expected/` | README text for the steps that cannot run here (see below) | console + Docker Hub account steps |

### `laptop/` — README "Developing App using Containers" (README.md:106-191)

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt` | extra | date, `Linux x86_64`, Docker 29.8.2, buildx v0.37.2, git 2.54.0 |
| `01-container-ls.txt` | `docker container ls` (115) | only the header row: nothing is running, so "Stop any container that is running" (116) has nothing to stop |
| `02-system-prune.txt` | `docker system prune` (117) | the four-item `WARNING! This will remove:` list, `[y/N] y` typed, `Total reclaimed space: 0B` |
| `03-image-ls.txt` | `docker image ls` (118) | empty table; Docker 29's columns `IMAGE  ID  DISK USAGE  CONTENT SIZE  EXTRA` |
| `04-clone.txt` | "Clone or download" (125); the command is README.md:50 | `Cloning into 'simple-translate'...` |
| `05-ls.txt` | extra | `.git .gitignore .vscode Dockerfile.txt README.md cli.py docker-build-push.sh docker-shell.sh pyproject.toml`: no `Dockerfile`, no `uv.lock` |
| `06-git-log.txt` | extra | `62f821b Handle translation exceptions with detailed error messages` |
| `07-build-no-dockerfile.txt` | extra: the build before the file exists | `ERROR: failed to build: failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory`, exit 1 |
| `08-dockerfile-v1.txt` | Step 1 (132-137) | `cat Dockerfile`: the README's block (lines 135-136) |
| `09-build-v1.txt` | build after Step 1 (174) | first build: `[1/1] FROM …python:3.12-slim-bookworm@sha256:34386ef0…`, the four base layers downloaded (3.34, 15.97, 28.25 MB, 249 B) while `unpacking`, `naming to docker.io/library/simple-translate:latest` |
| `10-config-v1.txt` | extra | `Entrypoint=null Cmd=["python3"] WorkingDir=""`: the base image's CMD, no WORKDIR |
| `11-run-v1.txt` | run after Step 1 (180) | the Python REPL: `Python 3.12.15 (main, Oct  6 2026, 02:02:31) [GCC 12.2.0] on linux`, `>>> exit()` |
| `12-git-status.txt` | extra | `nothing to commit, working tree clean` although `Dockerfile` exists (`.gitignore` line 3) |
| `13-dockerfile-v2.txt` | Step 2 (139-143) | + `ENTRYPOINT ["/bin/bash"]` |
| `14-build-v2.txt` | build | `CACHED` FROM, config-only change |
| `15-config-v2.txt` | extra | `Entrypoint=["/bin/bash"] Cmd=null`: setting ENTRYPOINT cleared the inherited CMD |
| `16-run-v2.txt` | run | a bare bash prompt `root@f72851da4a58:/#`, `exit` |
| `17-dockerfile-v3.txt` | Step 3 (145-152) | + `RUN pip install uv`, `COPY . ./` |
| `18-build-v3.txt` | build | `pip install uv` → `uv-0.13.0` (17.9 MB), the root-user pip warning, `[notice] A new release of pip is available: 25.0.1 -> 26.2.1`, `COPY . ./` |
| `19-run-v3.txt` | run | `ls` in `/` mixes the repo files (`Dockerfile`, `cli.py`, …) with `bin etc usr …`; `python cli.py` → `File "//cli.py", line 8` … `ModuleNotFoundError: No module named 'art'`; exit 1 |
| `20-dockerfile-v4.txt` | Step 4 (154-158) | + `RUN uv sync` |
| `21-build-v4.txt` | build | `[2/4] RUN pip install uv` `CACHED`, but `[3/4] COPY . ./` runs again (the edited `Dockerfile` is in the build context); `uv sync`: `Downloading cpython-3.15.0-linux-x86_64-gnu (download) (35.9MiB)`, `Using CPython 3.15.0`, `Creating virtual environment at: /.venv`, `Resolved 13 packages`, `Installed 11 packages` with versions |
| `22-run-v4.txt` | run (+ extra typed checks) | `ls -a` shows `.venv` and `uv.lock` (and `.git`, `.dockerenv`); `python cli.py` still fails (system 3.12); `.venv/bin/python --version` → `Python 3.15.0`; `source .venv/bin/activate && python cli.py` → banner, `Output: Adoro il formaggio`, then the `(app)` prompt prefix |
| `23-dockerfile-v5.txt` | Step 5 (160-165) | the full five-step Dockerfile |
| `24-build-v5.txt` | build | again `COPY . ./` + `uv sync` + CPython download, although only a `CMD` line was appended |
| `25-config-v5.txt` | extra | `Entrypoint=["/bin/bash"] Cmd=["-c","source .venv/bin/activate && exec bash"]` |
| `26-run-v5.txt` | run (+ extra typed checks) | prompt `root@…:/#` without `(app)`; `which python` → `/.venv/bin/python`; `Python 3.15.0`; `VIRTUAL_ENV` = `/.venv` |
| `27-diff-solution.txt` | "Solution Dockerfile: `Dockerfile.txt`" (167-168), extra | a unified diff (BusyBox `diff`): the three `ENV` lines, the `RUN set -ex; apt-get …` block, ENTRYPOINT moved down |
| `28-cp-solution.txt` | extra | `cp Dockerfile.txt Dockerfile` (the README only names the file) |
| `29-build.txt` | Build Docker Image (170-174) | typed in a terminal: the compact view `[+] Building 28.1s (9/9) FINISHED  docker:default` with `[2/4] RUN set -ex; …` 13.3 s, `[3/4] COPY . ./`, `[4/4] RUN uv sync` 4.9 s, exporting, `naming to docker.io/library/simple-translate:latest` |
| `30-image-ls.txt` | extra | `simple-translate:latest  73e9ab822b0b  518MB  144MB` (and the capture-only base, see below) |
| `31-run.txt` | Run Docker Container (176-184): `docker run --rm -ti simple-translate`, `python cli.py -t "Good morning" -s "en" -d "es"`, `exit` | banner, `Arguments: Namespace(text='Good morning', file='', src='en', dest='es')`, `Input: Good morning`, `Output: Buen día`, `exit` |
| `32-ps-a.txt` | extra | empty: `--rm` removed the container |
| `33-inside.txt` | extra | `pwd` → `/`; `echo $$` → `1` (bash is PID 1); `which python`; `Python 3.15.0` vs `/usr/local/bin/python --version` → `Python 3.12.15`; `ls /root/.local/share/uv/python`; `.venv/pyvenv.cfg` (`uv = 0.13.0`, `version_info = 3.15`, `prompt = app`); `ls -a /` |
| `34-history.txt` | extra | `docker history`: `uv sync` 125MB, `COPY . ./` 250kB, `RUN set -ex; apt-get …` 97.5MB, the `ENV`/`ENTRYPOINT`/`CMD` rows at 0B, the base image's rows (`PYTHON_VERSION=3.12.15`, `debian.sh … bookworm` 85.3MB); three capture-only rows, see below |
| `35-platform.txt` | extra | `x86_64`, `linux/amd64` |
| `36-run-args.txt` | extra | `docker run --rm -ti simple-translate python cli.py` → `/usr/local/bin/python: /usr/local/bin/python: cannot execute binary file`, exit 126 |
| `37-run-c.txt` | extra | `docker run --rm simple-translate -c "source .venv/bin/activate && python cli.py -d fr"` → `Output: j'adore le fromage` |
| `38-rebuild-same.txt` | extra | rebuild with no change, `--progress=plain`: every step `CACHED` |
| `39-edit-cli.txt` | extra | `git diff`: default text `I love cheese` → `I love brie` (cli.py:49) |
| `40-rebuild-edited.txt` | extra | `[2/4]` `CACHED`, `[3/4] COPY . ./` and `[4/4] RUN uv sync` run again, CPython downloaded again |
| `41-rebuild-restored.txt` | extra | after `git checkout cli.py` the cache does **not** come back: `COPY . ./` and `uv sync` run again, because `git` rewrote `.git/index`, which `COPY . ./` copies too |
| `42-docker-shell.txt` | extra (`sh docker-shell.sh`, not in the README) | cached compact build, then the container prompt, `exit` |
| `43-tag.txt` | Tag the Docker Image (190), `<USER NAME>` = `student` | no output, exit 0 |
| `44-image-ls-tagged.txt` | extra | `simple-translate:latest` and `student/simple-translate-ac215:latest`: the same ID `b5c531a6b555` |
| `capture-only/` | not part of the tutorial | `base.Dockerfile` + `base-build.txt`: the capture-only base image, see below |

### `laptop-push/` — README "Pushing Docker Image to Docker Hub" (README.md:186-191)

A second fresh engine (the first session's registry extras hit Docker Hub's rate limit, see
below). Before the steps, capture-only: the base image was loaded from the recording machine
(`docker save | docker load`, the same `sha256:34386ef0…` digest as `laptop/09`), the repo cloned,
`cp Dockerfile.txt Dockerfile` and the README's build run once (`capture-only/build.txt`, a plain
log of the solution build: `+ apt-get update`, `0 upgraded`, `Successfully installed pip-26.2.1`,
`uv-0.13.0`, `Using CPython 3.15.0`, `Installed 11 packages`). Image IDs therefore differ from
`laptop/`.

| file | README step | what it shows |
| --- | --- | --- |
| `01-tag.txt` | Tag the Docker Image (190) | no output, exit 0 |
| `02-image-ls.txt` | extra | two names, one ID |
| `03-push-no-login.txt` | Push to Docker Hub (191), **without** the login (no account here) | in a terminal: `The push refers to repository [docker.io/student/simple-translate-ac215]`, layers `Waiting`, then `push access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed`, exit 1. The real error a student gets when not logged in or pushing to someone else's namespace |
| `04-registry.txt` | extra | starts a throwaway local registry (`registry:3`, with a password file) as a stand-in for Docker Hub |
| `05-login-local.txt` | Login (189), same form, against the local registry with a placeholder password | `WARNING! Using --password via the CLI is insecure. Use --password-stdin.`, the unencrypted-credentials warning, `Login Succeeded` |
| `06-tag-local.txt` | Tag (190), local registry name | exit 0 |
| `07-push-local.txt` | Push (191), local registry | every layer `Pushed`, `latest: digest: sha256:2c302ec4… size: 856` (in a terminal) |
| `08-push-local-again.txt` | extra | the same push again: `Layer already exists` / `Already exists`, same digest |
| `09-imagetools-local.txt` | extra | what was pushed: an OCI image index with `linux/amd64` + an `unknown/unknown` attestation manifest |
| `10-imagetools-dlops.txt` | extra | `dlops/simple-translate:latest` is a single `application/vnd.docker.distribution.manifest.v2+json` (digest `sha256:2454010b…`): not a multi-platform index |
| `11-imagetools-python.txt` | extra | the base `python:3.12-slim-bookworm` is an index: `linux/amd64`, `linux/arm/v7`, `linux/arm64/v8`, `linux/386`, `linux/ppc64le`, each with an attestation manifest; `3.12.15-slim-bookworm`, created 2026-10-06 |
| `12-arm64-on-amd64.txt` | extra | `docker run --rm --platform linux/arm64 debian:12 uname -m` on this amd64 machine: pulls the arm64 image, then `exec /usr/bin/uname: exec format error`, exit 255. The same failure as an Apple Silicon image on a default (amd64) GCP VM, the other way round |
| `13-logout-local.txt` | extra | `Removing login credentials for localhost:5000` |
| `capture-only/` | not part of the tutorial | `base.Dockerfile`, `base-build.txt`, `build.txt` (see above), `hub-retries.txt` |

### `vm-debian12/` and `vm-debian13/` — README "Running App on VM using Docker" (README.md:203-220)

Same files in both folders.

| file | README step | what it shows |
| --- | --- | --- |
| `00-os.txt` | extra | `Debian GNU/Linux 12 (bookworm)` / `13 (trixie)`, `x86_64`, no `docker` yet |
| `01-apt-install-docker.txt` | `sudo apt install docker.io` (210), exactly as written | **fails**: `E: Unable to locate package docker.io` (Debian 13: `Error: …`), exit 100: the package lists are empty and the README has no `apt-get update` here |
| `02-apt-update.txt` | extra: `sudo apt-get update` (the README uses it at line 44, not here) | `Get:1 … InRelease` … `Reading package lists...` |
| `03-apt-install-docker.txt` | `sudo apt install docker.io` again | Debian 12: `1 upgraded, 92 newly installed`, `Need to get 107 MB`, `docker.io (20.10.24+dfsg1-1+deb12u1+b6)`, `Created symlink …docker.service`. Debian 13 (apt 3 layout): `Upgrading: 1, Installing: 91`, `Download size: 118 MB`, `docker.io (26.1.5+dfsg1-9+deb13u1)` |
| `04-docker-version.txt` | `sudo docker --version` (213) | `Docker version 20.10.24+dfsg1, build 297e128` / `Docker version 26.1.5+dfsg1, build a72d7cd` |
| `05-docker-no-sudo.txt` | extra: why the README uses `sudo` | `permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock`, exit 1 |
| `06-docker-run.txt` | `sudo docker run --rm -ti dlops/simple-translate` (215), then `python cli.py` (218) typed at the prompt, then extra `python --version`, `exit` | `Unable to find image 'dlops/simple-translate:latest' locally`, `latest: Pulling from dlops/simple-translate`, seven `Pull complete`, `Digest: sha256:2454010b…`, `Status: Downloaded newer image …`; `root@…:/# python cli.py` → banner, `Arguments: Namespace(text='I love cheese', file='', src='en', dest='it')`, `Input: I love cheese`, `Output: Adoro il formaggio`; `Python 3.14.7` |
| `07-images.txt` | extra | `dlops/simple-translate  latest  8a968f7e6f7a  3 weeks ago  347MB` (this Docker's classic image store) |
| `08-platform.txt` | extra | `x86_64`, `linux/amd64 created 2026-09-16T21:28:58…-04:00` |
| `09-history.txt` | extra | the published image's layers: `uv sync` 114MB, `COPY . ./` 209kB, `RUN set -ex; apt-get …` 108MB, base `PYTHON_VERSION=3.12.14` (sizes as Docker 20.10/26 count them) |
| `10-image-files.txt` | extra | inside the published image: `1266 cli.py` with `async with Translator() as translator:` (the older `cli.py`, without `raise_exception=True`); `.venv/bin/python -> …/cpython-3.14-linux-x86_64-gnu/bin/python3.14`; `pyvenv.cfg` with `uv = 0.12.15` |
| `11-ps-a.txt` | extra | empty: `--rm` |
| `vm-debian13/06-docker-run-rate-limited.txt` | the same README command, an earlier attempt | `docker: Error response from daemon: toomanyrequests: You have reached your unauthenticated pull rate limit.`, exit 125. Kept because it is a real failure a class sharing one network address can hit (the fix is `docker login`, or waiting): see "Docker Hub's rate limit" below |
| `capture-only/hub-retries.txt` | not part of the tutorial | how many attempts of `06` hit the rate limit before one got through |

### `expected/` — what cannot run here

| file | source | used for |
| --- | --- | --- |
| `vm-console.txt` | README.md:207-208 and 220, verbatim | *Create a VM Instance*, *SSH into your newly created instance*, *Delete your VM*: console clicks, no GCP account here. Scenes draw a schematic console tagged `illustration`; the README gives no machine type, zone or image, so the drawing shows none as "required" |
| `dockerhub-push.txt` | README.md:188-191, verbatim | *Sign up in Docker Hub and create an Access Token*, `docker login -u <USER NAME> -p <ACCESS TOKEN>` and the push to your own Docker Hub repository need an account and a token. The README documents no output. Scenes type the README's commands and show the real messages of `laptop-push/03` (push without login) and `laptop-push/05-09` (local-registry stand-in), tagged so |

## Differences from a real laptop / VM, and how scenes handle them

- **A Linux engine, not Docker Desktop on a Mac.** The "laptop" is Docker Engine 29.8.2 on
  linux/amd64. On Docker Desktop the builder is called `desktop-linux` (build logs say
  `building with "desktop-linux" instance`, the compact view's right column says
  `docker:desktop-linux` instead of `docker:default`) and Desktop adds a `View build details:` link
  after each build. On Apple Silicon the image is `linux/arm64` and uv downloads an `aarch64`
  CPython. Scenes say "on an Intel/AMD machine" where the platform shows.
- **Capture-only base image (laptop builds from Step 3 on).** The recording sandbox reaches the
  internet only through a TLS-intercepting proxy, so `pip`, `uv` and `apt-get` inside a build need
  its CA. Instead of editing the README's Dockerfiles, `run_steps.sh` (`capture_only_base`) rebuilt
  `python:3.12-slim-bookworm` (the real one, `sha256:34386ef0…`) with the CA added, apt sources
  switched to `https://`, and `ENV SSL_CERT_FILE`, and tagged it under the same name
  (`capture-only/base.Dockerfile`, `base-build.txt`). Builds 09 and 14 used the real base. Effects:
  the `FROM` lines from `laptop/18` on show the digest `sha256:4fb3e77d…` (yours:
  `sha256:34386ef0…`, as in `laptop/09`); `laptop/34-history.txt` has three extra rows
  (`COPY capture-ca.crt …`, `RUN cat …`, `ENV SSL_CERT_FILE=…`, about 0.7 MB) between the base and
  the tutorial's rows; `docker image ls` (`laptop/30`, `44`, `laptop-push/02`) lists a
  `python:3.12-slim-bookworm` row that a student's list may not have; the solution build's apt
  lines say `https://deb.debian.org` (`laptop-push/capture-only/build.txt`; a student's say
  `http://`). Scenes crop those rows or show the published image's history (`vm-*/09`) instead.
- **Proxy settings.** The laptop engine got the proxy through the Docker client's
  `~/.docker/config.json` `proxies` setting (the same setting Docker Desktop has under
  Settings › Resources › Proxies), which passes `HTTPS_PROXY` into builds and containers without
  changing any command. `proxy_relay.py` only makes the sandbox proxy reachable from Docker's
  network. Nothing of this shows in the outputs. The translation calls themselves needed no CA.
- **Interactive steps.** A person types at the prompt; here `ptyrun.py` typed the same lines
  (see the istep note above). The build steps 09-24 ran without a terminal, so their files are
  BuildKit's plain log; on screen you get the compact view of `laptop/29`. Scenes use the plain
  log to explain the steps and say "add `--progress=plain` to see this".
- **"Create a file called Dockerfile".** The capture wrote each README block into `Dockerfile` with
  `sed -n` from the README's own lines (135-136, 142, 148-151, 157, 163-164) instead of an
  editor; `cat Dockerfile` shows each version.
- **The VM is a container.** No systemd: apt's postinst prints `invoke-rc.d: could not determine
  current runlevel` / `policy-rc.d denied execution of start.` where a VM starts the service, and
  `run_steps.sh` starts `dockerd` by hand after step 03 (the container is privileged only for
  that). The container started with empty package lists, which is why `01` fails; a fresh Compute
  Engine image may ship package lists from its build date, so on a VM the README's command may
  work, or fail the same way, or fail with `404 Not Found` on stale lists. Scenes show the failure
  as "if you see this, run `sudo apt-get update` first". The package list is longer than on a GCP
  image, which already has some of these packages; scenes show its first and last lines.
- **Docker Hub's rate limit.** Docker Hub allows 100 anonymous pulls per hour per IP address, and
  the sandbox's few egress addresses are shared, so pulls often failed with `429 Too Many
  Requests` / `toomanyrequests`. The first laptop session's registry and platform extras failed
  that way (dropped; redone in `laptop-push/`); in later runs `run_steps.sh` (`hub_retry`) re-runs a
  pulling step until it gets through and logs the failed attempts in `capture-only/hub-retries.txt`.
  Every kept file is one complete run.
- **No apt `Done`, no colours.** As in L1, apt without a terminal leaves out ` Done` after its
  progress lines and `yes |` answers its prompt (Debian 12 shows `Do you want to continue? [Y/n]`
  followed directly by the next line; Debian 13's apt 3 shows `Continue? [Y/n] y`). Scenes show
  the README's command and the `Y` answer.

## Versions at the time of recording (2026-10-13)

| what | version |
| --- | --- |
| Docker (laptop stand-in) | client + engine 29.8.2, buildx v0.37.2, containerd image store |
| base image | `python:3.12-slim-bookworm` @ `sha256:34386ef0…` = Python 3.12.15 (built 2026-10-06), pip 25.0.1 |
| `pip install uv` | uv 0.13.0 |
| `uv sync` (fresh build) | CPython 3.15.0 (35.9 MiB download); anyio 4.15.1, art 6.5, certifi 2026.7.22, googletrans 4.0.2, h11 0.16.0, h2 4.4.1, hpack 4.2.0, httpcore 1.0.9, httpx 0.28.1, hyperframe 6.1.0, idna 3.20 |
| solution image | `simple-translate:latest` 518MB disk / 144MB content (Docker 29) |
| published image | `dlops/simple-translate:latest` @ `sha256:2454010b…`, linux/amd64 only, created 2026-09-16; CPython 3.14.7, uv 0.12.15, base Python 3.12.14, older `cli.py` (1266 bytes) |
| Debian 12 `docker.io` | 20.10.24+dfsg1-1+deb12u1+b6 (`Docker version 20.10.24+dfsg1, build 297e128`) |
| Debian 13 `docker.io` | 26.1.5+dfsg1-9+deb13u1 (`Docker version 26.1.5+dfsg1, build a72d7cd`) |

Versions that will change for a later viewer (uv, the CPython uv picks, the base image's Python
patch release, package versions, Docker) are said with "at the time of recording".

## Re-running the captures

```
bash assets/terminal/capture.sh laptop
bash assets/terminal/capture.sh laptop-push
bash assets/terminal/capture.sh vm debian:12 vm-debian12
bash assets/terminal/capture.sh vm debian:13 vm-debian13
```

Needs Docker with privileged containers. Behind an HTTPS-only proxy on `127.0.0.1` (the recording
sandbox), export `HTTPS_PROXY` and `CA_BUNDLE` (a PEM file with the proxy's CA) first; without
them the capture-only parts (relay, base image with the CA, rate-limit retries) are skipped.
`laptop-push` loads `python:3.12-slim-bookworm` from the machine's own Docker when it has it, and
pulls it otherwise.
`docker rm -f l02-relay` removes the relay afterwards.
