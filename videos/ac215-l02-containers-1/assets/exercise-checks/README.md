# Exercise checks · ac215-l02-containers-1 (2026-10-13, 19:38–19:58 UTC)

What was run to verify `exercises.md`, beyond the captures in `assets/terminal/`, which the answers
cite directly (`laptop/NN`, `laptop-push/NN`, `vm-debian12/NN`). Raw logs are in
`assets/exercise-checks/logs/`.

## Setup (disposable; nothing from the repo ran on the host)

- Docker Engine 29.8.2 on the session machine (containerd image store, builder `default`, BuildKit
  v0.33.1, linux/amd64). Every image and container was named `l02ex*`. Containers ran with `--rm`,
  except the named ones B2/C7 needed, which were removed afterwards.
- Work clone: `git clone` of the read-only `dlops/simple-translate` clone, checked out at
  `62f821b` (`git log --oneline -1` → `62f821b Handle translation exceptions with detailed error messages`).
- Proxy CA: the sandbox's TLS-intercepting proxy needs its CA inside builds. The check-only base
  `l02ex/base:3.12` is `python:3.12-slim-bookworm` (`sha256:34386ef0…`, the same as `laptop/09`)
  plus the CA, https apt sources and `ENV SSL_CERT_FILE` (`exercises_checks/check-base.Dockerfile`,
  the recipe from `assets/terminal/laptop/capture-only/base.Dockerfile`). Builds used it through a
  named build context, `--build-context python:3.12-slim-bookworm=docker-image://l02ex/base:3.12`
  (`exercises_checks/bld.sh`), so the Dockerfiles kept their `FROM python:3.12-slim-bookworm` line.
  Side effect: BuildKit lists `FROM` as a context, not a step, so the logs number the steps
  `[1/4] RUN …`, `[2/4] COPY …` instead of a student's `[2/4] RUN …`, `[3/4] COPY …`. The same for
  3.13: `l02ex/base:3.13`.
- Proxy for builds: `--network host --build-arg HTTPS_PROXY=… --build-arg https_proxy=…`
  (proxy build args are not part of the cache key).

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| baseline | `cp Dockerfile.txt Dockerfile`, build → `l02ex-st` | same steps as `laptop/29`: uv 0.13.0, `Downloading cpython-3.15.0-linux-x86_64-gnu (download) (35.9MiB)`, `Installed 11 packages`; `docker history`: `uv sync` 125MB, `RUN set -ex…` 97.5MB, `COPY` 262kB; `docker image ls` 518MB |
| Q3, B1.1 | `docker run --rm --network host l02ex-st -c 'ls -l .venv/bin/python; …; du -sh /root/.local/share/uv/python /.venv'` | `.venv/bin/python -> /root/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/bin/python3.15`; `112M` uv's Python folder, `6.9M` `/.venv`. (`python --version` here said 3.12.15 because `-c` bypasses CMD's activation, which is C2) |
| B1.2 | `ENV UV_PYTHON_DOWNLOADS=never` added after `FROM` (`py-never.log`) | the apt/pip `RUN` reran (not `CACHED`); `uv sync`: `error: No interpreter found for Python >=3.13 in managed installations or search path` + `hint: A managed Python download is available for Python >=3.13, but Python downloads are set to 'never'`; `exit code: 2`; no image `l02ex-never` created |
| B1.3 | `FROM python:3.13-slim-bookworm` (pulled 2026-10-13, Python 3.13.16) (`py-313.log`) | `Using CPython 3.13.16 interpreter at: /usr/local/bin/python3`, no download, `Installed 12 packages` (+ `typing-extensions==4.16.0`; `uv.lock` marker: anyio needs it for `python_full_version < '3.15'`); `uv sync` layer 8.19MB; image 348MB vs 518MB; `.venv/bin/python -> /usr/local/bin/python3`; both `python --version` → 3.13.16 |
| B2 | via `assets/terminal/ptyrun.py` (a pty, lines typed at the prompt): `docker run --rm -ti l02ex-st` → `echo "Le fromage est bon" > /note.txt`, `exit`; second `--rm` run → `cat /note.txt`; `docker run -ti --name l02ex-note …`, `docker ps -a`, `docker start -ai l02ex-note`, `docker diff` | `cat: /note.txt: No such file or directory`; `l02ex-note   Exited (0)`; after `start -ai` the same prompt ID `82a118d25278` and `Le fromage est bon`; `docker diff`: `C /root`, `A /root/.bash_history`, `A /note.txt` |
| Q4, B3 | the cache-friendly Dockerfile + `.dockerignore` (`Dockerfile.cache-friendly`, `dot-dockerignore.txt`), six builds (`cache-1…6`) | 1: apt/pip `RUN` `CACHED` (built before), `COPY pyproject.toml README.md ./`, `uv sync` (download), `COPY . ./` run; `transferring context: 19.99kB` (67.72kB with `.git` in the baseline). 2: all `CACHED`. 3 (`I love brie`): only `COPY . ./` ran. 4 (`git checkout -q cli.py`): all `CACHED`. 5 (comment appended to `Dockerfile`): all `CACHED`. 6 (empty line in `README.md`): `COPY pyproject.toml README.md ./`, `uv sync`, `COPY . ./` ran |
| B3.6 | `COPY pyproject.toml ./` without `README.md` (`cache-7-no-readme.log`) | `uv sync` succeeds: `Resolved 13 packages`, `Installed 11 packages` (no `[build-system]` in `pyproject.toml`) |
| Q4 | `docker run --rm -ti --network host l02ex-cache` (pty): `which python`, `ls -a /`; `-c "source .venv/bin/activate && python cli.py -d fr"` | `/.venv/bin/python`; no `.git`, no `Dockerfile` in `/` (`.dockerignore` itself is copied); `Output: j'adore le fromage` |
| B3.6, D2 | `uv lock` in a container (`--entrypoint uv l02ex-st lock`, the clone mounted), then `COPY pyproject.toml uv.lock ./` + `RUN uv sync --locked`; then `"rich"` added to `pyproject.toml` by hand (`lock-1`, `lock-2`) | the locked build works (`Resolved 13 packages`, `Installed 11 packages`); after the hand edit: ``error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.``, build fails |
| B4 | (a) `docker run --rm l02ex-st`; (c) `printf 'which python\necho $VIRTUAL_ENV\n' \| docker run --rm -i l02ex-st`; (b) `docker run --rm -t --name l02ex-tonly l02ex-st` in a pty, `echo typed-but-lost` typed (`run-flags.log`) | (a) no output, exit 0, 0.4 s; (c) `/.venv/bin/python`, `/.venv`, no prompt; (b) a prompt, the typed line echoed by the local terminal, no output; `docker ps` showed `l02ex-tonly Up 2 minutes` until `docker stop` |
| Q2 | `docker run --rm --entrypoint /.venv/bin/python l02ex-st cli.py -h`; `-c ".venv/bin/python cli.py -h"` | both print `usage: cli.py [-h] [-t TEXT] [-f FILE] [-s SRC] [-d DEST]`, exit 0 |
| C2 | `docker run --rm l02ex-st -c "python cli.py"` | `File "//cli.py", line 8` … `ModuleNotFoundError: No module named 'art'`, exit 1 |
| B5 | `docker tag l02ex-st l02ex-student/simple-translate-ac215`, `docker image ls`, `docker rmi l02ex-student/simple-translate-ac215` | same ID `a3140e74c5bb` on both rows; `Untagged: l02ex-student/simple-translate-ac215:latest`; `l02ex-st` still there |
| B5, C3 | `docker push l02ex-pushtest` (a `FROM scratch` image, no login) | `The push refers to repository [docker.io/library/l02ex-pushtest]`, then `push access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed`, exit 1 (nothing uploaded) |
| C1 | `docker build -t l02ex-nodot -f Dockerfile` (in the clone); the same with the dot from `/tmp` | `ERROR: docker: 'docker buildx build' requires 1 argument` + usage, exit 1; `ERROR: failed to build: failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory` |
| C4 | a local registry (`mirror.gcr.io/library/registry:3` on `127.0.0.1:5052`); `docker build --platform linux/arm64` of a `FROM scratch` image, push, `docker buildx imagetools inspect`, `docker rmi`, `docker run --rm localhost:5052/student/armonly` | index: `Platform: linux/arm64` + `Platform: unknown/unknown`; run: `docker: Error response from daemon: no matching manifest for linux/amd64/v4 in the manifest list entries: no match for platform in manifest: not found`, exit 125 |
| C5 | `docker buildx create --driver-opt network=host --name l02ex-multi` (without `--use`, so the shared default stayed current), `BUILDX_BUILDER=l02ex-multi docker build -t l02ex-g2 …`, then with `--load`; `docker buildx rm l02ex-multi` | `WARNING: No output specified with docker-container driver. Build result will only remain in the build cache. To push result image into registry use --push or to load image into docker use --load`; no `l02ex-g2` in `docker image ls`; builder container `buildx_buildkit_l02ex-multi0`; with `--load` the image appears; `buildx rm` removes the container |
| C6 | `debian:12`, privileged: `apt-get update`, `apt-get install docker.io sudo`, `useradd student`, `dockerd`, then `su - student -c "docker ps"`, `docker ps` (root), `usermod -aG docker student`, `su - student -c "id -nG; docker ps"` (`vm-docker-group.log`) | `Docker version 20.10.24+dfsg1, build 297e128`; `srw-rw---- 1 root docker … /var/run/docker.sock`; before: `permission denied while trying to connect to the Docker daemon socket …`, after usermod + new login: `student docker` and the empty `docker ps` table |
| C7 | `docker run -d --rm --name l02ex-shell -ti l02ex-st`, then the same in a pty | `docker: Error response from daemon: Conflict. The container name "/l02ex-shell" is already in use by container "…". You have to remove (or rename) that container to be able to reuse that name.`, exit 125 |
| D3 | `COPY token.txt` then `RUN rm /token.txt` on the check base; `docker save`, search the layer tars | `ls /token.txt` fails in the container; the file (`not-a-real-secret`) is still in the `COPY` layer |
| D3 | `docker run --rm --network host dlops/simple-translate -c 'ls -d /.git …; ls /.git; wc -l /.git/logs/HEAD'` | `/.git` (with `logs`, `objects`, `cursor` …), `/.vscode`, `/Dockerfile.txt`; `logs/HEAD` has 4 entries, each with an e-mail address (not printed here) |

Not run (cited from the captures or the repo instead): `docker build --platform=linux/amd64` on a
Mac and a real buildx multi-platform push (no arm64 machine, no emulator, no Docker Hub account);
`docker login` / `docker push` to Docker Hub; whether a read-only Docker Hub token produces the
same `insufficient_scope` denial (C3, cause 3); Docker 20.10's exact wording of `no matching
manifest` on a VM (C4: checked on Docker 29 only); `docker system prune -a` (D4: not run on the
shared host). Docker Hub's repository and token defaults couldn't be checked without an account.

## Incident, and cleanup

- The C6 check ran its nested `dockerd` in a privileged container with `--network host` and
  `--bridge=none --iptables=false`. With the bridge disabled, dockerd deletes an existing
  `docker0`, and in the host's network namespace that was the host's default bridge (gone since
  about 19:49 UTC). From then on, `docker run` without `--network host` fails with
  `adding interface veth… to bridge docker0 failed: Device does not exist`. Builds and
  `--network host` runs still work, and the later checks used only those. Recreating the bridge by
  hand was refused by the session's permission policy. Restarting the host `dockerd` brings it
  back, but it stops running containers, so that's left to the coordinator (reported in the
  return). Lesson for future checks: run nested daemons on Docker's own network, as
  `assets/terminal/capture.sh` does, never with `--network host`.
- Removed afterwards: the containers (all `--rm`, plus `l02ex-note`, `l02ex-shell`, `l02ex-tonly`),
  the throwaway builder `l02ex-multi` and the local registry container. **Not yet removed**: the
  images `l02ex-st`, `l02ex-cache`, `l02ex-cache-noreadme`, `l02ex-py313`, `l02ex-locked`,
  `l02ex/base:3.12`, `l02ex/base:3.13`, and the pulls made for these checks
  (`python:3.13-slim-bookworm`, `mirror.gcr.io/library/registry:3`). From 19:54 UTC a second agent
  was working on the same task, in the same scratch folder (`scratchpad/l02ex/`) and with the same
  `l02ex*` names (it built `l02ex-py313never` and rebuilt `l02ex-leak`, and drafted
  `README.draft.md`). Deleting the shared names would have broken its checks, so `docker rmi` of
  the `l02ex*` images is left to whoever finishes last. The build cache of these builds was left in
  place (no shared prune).
