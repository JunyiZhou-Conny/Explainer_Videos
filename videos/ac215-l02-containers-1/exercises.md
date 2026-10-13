# Exercises · AC215 L2 — Containers I: one image, from laptop to VM

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real captures from
2026-10-13 (`assets/terminal/`), or were checked the same day in throwaway containers built from the
README's Dockerfile (Docker Engine 29.8.2, uv 0.13.0, Python 3.12.15 in the base image; what was run
is listed in [`assets/exercise-checks/README.md`](assets/exercise-checks/README.md)). Image IDs, container IDs and versions on your laptop will
differ. Commands marked *(extra)* aren't in the README.

---

## Part A · The five questions from the end of the video

**Q1. What is the difference between an image and a container, and what does `--rm` delete?**

<details><summary>Answer</summary>

An **image** is a stack of read-only layers plus a small config. Each `RUN` or `COPY` adds a layer
(`docker history simple-translate`: `RUN uv sync` 125MB, `COPY . ./` 250kB, the apt/pip `RUN`
97.5MB, then the base image's own rows). `ENV`, `ENTRYPOINT` and `CMD` only write on the config:
their rows are `0B` (`laptop/34`). `docker run` makes a **container**: the same layers, shared, not
copied, plus a thin writable layer on top and one main process. For our image that process is bash:
`echo $$` prints `1` (`laptop/33`). Think of the image as a class and each container as an instance;
that's why the README's "Build the docker container" (`README.md:173`) is a slip: building makes an
image.

When the main process ends (you type `exit`), the container **stops**. It still exists, writable
layer and all, until something removes it. `--rm` removes it as soon as it stops: the container,
with its writable layer and every file you created inside it. The image is untouched. After the
README's run, `docker ps -a` lists nothing (`laptop/32`), and `simple-translate` is still in
`docker image ls`. B2 shows the difference.
</details>

**Q2. What command line does our container run at start-up, and what happens with
`docker run --rm -ti simple-translate python cli.py`?**

<details><summary>Answer</summary>

ENTRYPOINT + CMD, joined: `/bin/bash -c "source .venv/bin/activate && exec bash"`. The extra
`docker image inspect` shows both halves:
`Entrypoint=["/bin/bash"] Cmd=["-c","source .venv/bin/activate && exec bash"]` (`laptop/25`). The
first bash sources the activate script, which puts `/.venv/bin` first in `PATH`, then `exec bash`
replaces it with an interactive bash that keeps that `PATH` and gives you the prompt.

Words after the image name replace **CMD only**, so the container runs `/bin/bash python cli.py`.
Bash takes `python` as the name of a script file. There's none in `/`, so it searches `PATH`, where
nothing has activated the venv. It finds the base image's `/usr/local/bin/python`, a program, not
a script, and refuses:
`/usr/local/bin/python: /usr/local/bin/python: cannot execute binary file`, exit 126 (`laptop/36`).
Two forms that work:

```bash
docker run --rm simple-translate -c "source .venv/bin/activate && python cli.py -d fr"   # laptop/37: Output: j'adore le fromage
docker run --rm --entrypoint /.venv/bin/python simple-translate cli.py -d fr             # replaces bash itself
```
</details>

**Q3. The Dockerfile says `python:3.12`. Why does `python --version` print 3.15 (or 3.14), and
what does `/usr/local/bin/python` print?**

<details><summary>Answer</summary>

`pyproject.toml` line 6 asks for `requires-python = ">=3.13"`, and the base image's 3.12 doesn't
qualify (`Dockerfile.txt` line 2). So during the build, `uv sync` downloads its own Python: the
newest stable release in the range that uv knows. With uv 0.13.0 on 2026-10-13 that was CPython
3.15.0 (`Downloading cpython-3.15.0-linux-x86_64-gnu (download) (35.9MiB)`, `laptop/21`). The
instructor's `dlops/simple-translate` was built on 2026-09-16 with uv 0.12.15, which picked 3.14.7
(`vm-debian12/08`, `10`). The venv's `python` is a link into uv's folder
(`.venv/bin/python -> /root/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/bin/python3.15`),
and CMD activated the venv, so `python` finds that one first.

`/usr/local/bin/python --version` prints the base image's own Python: `Python 3.12.15`
(`laptop/33`; 3.12.14 in the instructor's image). That Python only ran `pip install uv`. The image
carries two Pythons. Most of the 125MB `uv sync` layer is the second one: 112M under
`/root/.local/share/uv/python`, against 6.9M for `/.venv` itself. To keep one Python, start from
`python:3.13-slim-bookworm`, or make `requires-python` something the image already meets (B1).
</details>

**Q4. You edit one line of `cli.py`. Which build steps re-run, and how would you reorder the
Dockerfile so `uv sync` stays cached?**

<details><summary>Answer</summary>

A step is reused when its parent step and its instruction are unchanged and, for `COPY`, the copied
files have the same checksum. Editing `cli.py` changes what `COPY . ./` copies, so `[3/4] COPY . ./`
runs again, and so does every step after it: `[4/4] RUN uv sync`, Python download included. `FROM`
reuses the base, and `[2/4] RUN set -ex; apt-get update …` says `CACHED` (`laptop/40`). Undoing
the edit with `git checkout` doesn't bring the cache back: git rewrote `.git/index`, which is in
the build context too (`laptop/41`).

The fix: copy only what `uv sync` needs, run it, then copy the rest, and keep `.git`, a local
`.venv` and the Dockerfile out of the context. This is the full Dockerfile from the video, a
pattern for your own projects, not the course solution:

```dockerfile
# Use the official Debian-hosted Python image
FROM python:3.12-slim-bookworm

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Python wants UTF-8 locale
ENV LANG=C.UTF-8

# Tell Python to disable buffering so we don't lose any logs.
ENV PYTHONUNBUFFERED=1

# Ensure we have an up to date baseline, install dependencies and uv
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    pip install --no-cache-dir --upgrade pip && \
    pip install uv

# Copy only the files uv sync needs, then install the packages
COPY pyproject.toml README.md ./
RUN uv sync

# Copy the rest of the source code
COPY . ./

# Entry point
ENTRYPOINT ["/bin/bash"]
# Get into the uv virtual environment shell
CMD ["-c", "source .venv/bin/activate && exec bash"]
```

and next to it a file `.dockerignore`:

```
.git
.venv
secrets/
Dockerfile
```

Checked on 2026-10-13: after editing `cli.py`, only the last `COPY . ./` ran; the apt/pip `RUN`,
`COPY pyproject.toml README.md ./` and `RUN uv sync` said `CACHED`. The Dockerfile still builds
although it's listed in `.dockerignore`: Docker reads it separately, and `COPY` no longer copies
it. B3 walks through the rebuilds.
</details>

**Q5. Name two ways to make an image built on Apple Silicon run on a default GCP VM.**

<details><summary>Answer</summary>

Every program in an image is machine code for one kind of CPU. A plain `docker build` on an
M-series Mac makes `linux/arm64` programs. A default (E2) VM is `amd64` and has no emulator, so it
can't run them.

1. **Build for the VM's platform**:
   `docker build -t simple-translate --platform=linux/amd64 -f Dockerfile .` (it's the
   commented-out line 12 of `docker-shell.sh`). On the Mac it runs emulated: slower, but it works.
   Then `docker tag` and `docker push` again, as in the README.
2. **Push both platforms with buildx**: `docker-build-push.sh` creates a buildx builder (line 23)
   and runs `docker buildx build --platform linux/amd64,linux/arm64 --push …` (line 27). That
   pushes one tag that points at a menu of two images. Put your username on line 11
   (`DOCKER_USERNAME="dlops"`) and `simple-translate-ac215` on line 7, run `docker login` first,
   then `bash docker-build-push.sh` (the file isn't executable). Afterwards run
   `docker buildx use default` (`desktop-linux` on Docker Desktop) so plain builds land on your
   laptop again (C5).

Check before you deploy: `docker buildx imagetools inspect <USER NAME>/simple-translate-ac215`
must list `Platform: linux/amd64`. A third way changes the VM, not the image: an Arm machine series
(such as C4A) runs arm64 images directly.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Two Pythons, then one.** Start `docker run --rm -ti simple-translate` and predict what these
print, then run them *(extra)*: `python --version`, `/usr/local/bin/python --version`,
`ls -l .venv/bin/python`. Then copy the solution Dockerfile to a new file and add one line right
after `FROM`:

```bash
cp Dockerfile.txt Dockerfile.never        # then add, as line 3:  ENV UV_PYTHON_DOWNLOADS=never
docker build -t st-never -f Dockerfile.never .
```

Predict which steps run and how the build ends. Last, change that file's `FROM` line to
`python:3.13-slim-bookworm` (keep the `ENV`), build it as `st-313`, and predict `python --version`
inside and the size in `docker image ls`.

<details><summary>Answer</summary>

1. `Python 3.15.0`, `Python 3.12.15`, and a link
   `.venv/bin/python -> /root/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/bin/python3.15`
   (Q3).
2. The new `ENV` sits right under `FROM`, so every step after it runs again, the apt/pip `RUN`
   included: the first step that changes reruns, along with everything below it. Then `uv sync`
   fails, because it may not download a Python and the image has none in range:

   ```
   error: No interpreter found for Python >=3.13 in managed installations or search path
   hint: A managed Python download is available for Python >=3.13, but Python downloads are set to 'never'
   ```

   The build stops (`exit code: 2`), and `st-never` isn't created. That's the point of the
   setting: a mismatch fails loudly instead of quietly adding 112M of Python.
3. With the 3.13 base, `uv sync` finds the image's own Python and downloads nothing:
   `Using CPython 3.13.16 interpreter at: /usr/local/bin/python3` (3.13.16 at the time of checking).
   It installs 12 packages, one more than before: `typing-extensions`, which `anyio` needs only
   below Python 3.15. `python --version` and `/usr/local/bin/python --version` now agree, and
   `.venv/bin/python -> /usr/local/bin/python3`. The `uv sync` layer drops from 125MB to about 8MB,
   and the image from 518MB to about 350MB on disk.
</details>

**B2. Where did my file go?** Start the container, write a file, leave, and start it again:

```bash
docker run --rm -ti simple-translate
echo "Le fromage est bon" > /note.txt     # at the container's prompt
exit
docker run --rm -ti simple-translate      # then: cat /note.txt
```

Predict the result. Now repeat with `docker run -ti --name cheese simple-translate` (no `--rm`),
write the note, `exit`, and predict what `docker ps -a` shows. Can you get the note back?

<details><summary>Answer</summary>

With `--rm`, `cat: /note.txt: No such file or directory`: the first container and its writable
layer were deleted on exit, and the second one starts fresh from the unchanged image. Without
`--rm`, `docker ps -a` lists `cheese` as `Exited (0)`: stopped, not gone. `docker start -ai cheese`
starts that same container again (same ID in the prompt), with the same start-up command, and
`cat /note.txt` prints `Le fromage est bon`. `docker diff cheese` *(extra)* lists what its writable
layer holds: `A /note.txt` (and bash's history). Clean up with `docker rm cheese`. The image never
changed; only one container's top layer did.
</details>

**B3. Rebuild without the wait.** Replace your `Dockerfile` with the one from Q4 and create its
`.dockerignore` (your solution is still in `Dockerfile.txt`). Predict, for each build below, which
steps say `CACHED`. Use `docker build --progress=plain -t simple-translate -f Dockerfile .` to see
every step.

1. the first build with the new file;
2. the same build again, nothing changed;
3. after changing `"I love cheese"` to `"I love brie"` on line 49 of `cli.py`;
4. after `git checkout -q cli.py`;
5. after adding a comment line at the end of the `Dockerfile`;
6. after adding an empty line to `README.md`.

<details><summary>Answer</summary>

1. The apt/pip `RUN` is `CACHED` if you built the solution before (same base, same instruction:
   the comments don't count). `COPY pyproject.toml README.md ./`, `RUN uv sync` (with the 35.9MiB
   download) and `COPY . ./` run. The context shrinks too: `transferring context: 19.99kB` in our
   check, without `.git`.
2. Everything `CACHED`.
3. Only the last `COPY . ./` runs; `uv sync` stays `CACHED`.
4. Everything `CACHED`: the files are back, and `.git/index` is no longer in the context (compare
   `laptop/41`).
5. Everything `CACHED`: the Dockerfile is ignored, so editing it no longer changes what `COPY`
   copies. That's what made every "Build + Run" in part 1 rerun `uv sync`.
6. `COPY pyproject.toml README.md ./` runs, and so do `uv sync` and the last `COPY`. The README is
   there because `pyproject.toml` names it (`readme = "README.md"`, line 5). Here `uv sync` works
   without it (checked: the project has no build system, so uv doesn't build it), so
   `COPY pyproject.toml ./` alone would keep README edits away from `uv sync`. Once you commit a
   `uv.lock`, copy it in the same line and use `RUN uv sync --locked`. A dependency added to
   `pyproject.toml` without `uv lock` then stops the build:
   ``error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.``
</details>

**B4. What `-t` and `-i` each do.** Predict, then run:
(a) `docker run --rm simple-translate`;
(b) `docker run --rm -t simple-translate`, then type `echo hi`;
(c) `echo 'which python' | docker run --rm -i simple-translate`.

<details><summary>Answer</summary>

(a) No output, and you're back at your laptop prompt in under a second (exit 0). Bash got no
terminal and no input, read end-of-input at once, and exited, and `--rm` removed the container.
(b) A prompt appears (`-t` gave bash a terminal), but your keystrokes never reach it: nothing runs,
and the container stays `Up`. Stop it from a second terminal with `docker stop <container id>`.
(c) `/.venv/bin/python`: `-i` connects your input, so piped or typed commands run in the activated
venv. But with no terminal, bash shows no prompt and no line editing. `-ti` gives you both, which
is why the README uses it.
</details>

**B5. Two names, one image.** After the README's `docker tag simple-translate
<USER NAME>/simple-translate-ac215`, run `docker image ls` *(extra)*. Predict what
`docker rmi <USER NAME>/simple-translate-ac215` *(extra)* deletes. Then predict where
`docker push simple-translate` would go.

<details><summary>Answer</summary>

`docker image ls` shows two rows with the same ID (`b5c531a6b555` in `laptop/44`): a tag is a
second name, not a copy. `docker rmi` on one name prints
`Untagged: <USER NAME>/simple-translate-ac215:latest` and removes only that name. The image stays
under `simple-translate`, same ID. Tag it again before you push. A name without an account belongs
to `library`, the official images' namespace. So `docker push simple-translate` prints
`The push refers to repository [docker.io/library/simple-translate]` and ends in
`push access denied, repository does not exist or may require authorization` (checked with a
throwaway name). Only `<USER NAME>/…` names go to your account.
</details>

---

## Part C · Debugging

**C1. Two ways the build won't start.** (a) `docker build -t simple-translate -f Dockerfile` prints
`ERROR: docker: 'docker buildx build' requires 1 argument`. (b) A classmate's build says
`ERROR: failed to build: failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory`.
What went wrong in each?

<details><summary>Answer</summary>

(a) The final `.` is missing: the build context is the one argument `docker build` requires (the
`-f` file is only the recipe). (b) Docker looks for `Dockerfile` in the context folder and doesn't
find it. Either the terminal isn't in `simple-translate` (`README.md:172`; check with `pwd`, `ls`),
or the file is named something else: it must be exactly `Dockerfile`, capital D, no extension.
`Dockerfile.txt` is the solution, not the recipe the command reads. The video got this message by
building before writing the file (`laptop/07`).
</details>

**C2. "I replaced CMD and now `art` is missing."** To translate in one go, someone runs
`docker run --rm simple-translate -c "python cli.py"` and gets
`ModuleNotFoundError: No module named 'art'`. The image works with `-ti`. Why?

<details><summary>Answer</summary>

Their `-c` string replaced the whole CMD, including `source .venv/bin/activate`. Nothing activated
the venv, so `python` found the base image's `/usr/local/bin/python` (3.12), which has none of the
packages: the same failure as in Step 4 (`laptop/22`). Put the activation back into the string,
`-c "source .venv/bin/activate && python cli.py"` (`laptop/37`), or call the venv's Python by its
path: `-c ".venv/bin/python cli.py"`.
</details>

**C3. `push access denied`.** `docker push student/simple-translate-ac215` ends with
`push access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed`
(`laptop-push/03`). Name three causes.

<details><summary>Answer</summary>

1. You're not logged in (that's how the recording got it: no Docker Hub account). Run
   `docker login -u <USER NAME>` and paste the token when it asks.
2. The name doesn't start with **your** username: a typo, the README's `student` from the video,
   a name without an account (`library`, B5), or `docker-build-push.sh` still saying
   `DOCKER_USERNAME="dlops"` (line 11).
3. The token can't write: create one with read and write access.
</details>

**C4. The VM won't run your image.** You built on an M-series Mac with the README's command, tagged
and pushed. On the VM, `sudo docker run --rm -ti <USER NAME>/simple-translate-ac215` fails with
`no matching manifest for linux/amd64 in the manifest list entries`, while
`sudo docker run --rm -ti dlops/simple-translate` works. Explain, and find the evidence.

<details><summary>Answer</summary>

Your tag points at a menu with one real row, `linux/arm64`, plus an attestation (how the image was
built): `docker buildx imagetools inspect <USER NAME>/simple-translate-ac215` shows
`Platform: linux/arm64` and `Platform: unknown/unknown`. The VM asks for amd64, and the menu has no
such row. In our check, a pushed arm64-only image gave Docker 29 on amd64
`no matching manifest for linux/amd64/v4 in the manifest list entries: no match for platform in manifest: not found`
(the CPU variant depends on the machine). An image pushed as a single manifest pulls instead and
then fails with `exec format error`, the failure the video shows the other way round
(`laptop-push/12`). `dlops/simple-translate` runs because it's a single `linux/amd64` image
(`laptop-push/10`, `vm-debian12/08`). The fix is Q5.
</details>

**C5. "My changes don't show up any more."** After running `docker-build-push.sh`, the README's
`docker build -t simple-translate -f Dockerfile .` ends with
`WARNING: No output specified with docker-container driver. Build result will only remain in the build cache. To push result image into registry use --push or to load image into docker use --load`,
and `docker run --rm -ti simple-translate` still runs the old image. Why?

<details><summary>Answer</summary>

Line 23 of the script, `docker buildx create … --use --name multi-arch`, made a new builder your
current one. It runs in its own container (`buildx_buildkit_multi-arch0`) and keeps its results to
itself, so nothing new lands in `docker image ls`. `docker buildx ls` marks the current builder
with `*`. Switch back with `docker buildx use default` (`desktop-linux` on Docker Desktop), or add
`--load` to that one build. Checked on 2026-10-13 with a throwaway builder: without `--load`, the
same warning and no image; with it, the image appears.
</details>

**C6. `permission denied` on the VM.** On the VM, `docker ps` without `sudo` prints
`permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: …`
(`vm-debian12/05`). Why does the README write `sudo`, and what's the alternative?

<details><summary>Answer</summary>

The Docker CLI talks to the background service through the socket `/var/run/docker.sock`, owned by
`root` and the group `docker` (`srw-rw---- 1 root docker`). Your user is in neither, so the README
uses `sudo`. The alternative is `sudo usermod -aG docker $USER`, then close the SSH window and
connect again: a shell keeps the groups it started with. Checked in a Debian 12 stand-in: after
the change and a new login, `id -nG` listed `docker` and `docker ps` worked without `sudo`. Being
in that group is as powerful as root on that machine, which is fine on a throwaway course VM.
</details>

**C7. A name already in use.** You run `sh docker-shell.sh` *(extra)* in a second terminal while
the first one's container is still open. It fails with
`docker: Error response from daemon: Conflict. The container name "/simple-translate" is already in use by container "…". You have to remove (or rename) that container to be able to reuse that name.`
(exit 125). Why does the README's own run command never do this?

<details><summary>Answer</summary>

`docker-shell.sh` line 15 runs `docker run --rm --name $IMAGE_NAME -ti $IMAGE_NAME`: every
container it starts is called `simple-translate`, and two containers can't share a name. The
README's `docker run --rm -ti simple-translate` gives no `--name`, so Docker invents a new name
each time. Type `exit` in the other terminal, or find it with `docker ps -a` and remove it with
`docker rm -f simple-translate`.
</details>

---

## Part D · Think

**D1. Container or VM?** For each case, would a container do, or do you need a VM? (a) Two apps on
one server need different versions of a system library. (b) Software that needs a different kernel
or operating system, such as a Windows program or a custom kernel module. (c) Your Linux image needs
a GPU. (d) You run Linux containers on a Mac.

<details><summary>Answer</summary>

(a) Containers: each image carries its own system files and libraries, which a venv couldn't
isolate in L1. (b) A VM: containers are isolated processes that share the host's Linux kernel.
(c) A container can use it, but the GPU driver stays the host's: the machine needs the driver, and
the container needs access to the device. (d) Both: Docker Desktop runs your containers inside a
small, hidden Linux VM, because macOS has no Linux kernel to share.
</details>

**D2. Same Dockerfile, a month apart.** The instructor's image and yours came from the same
Dockerfile, yet one runs Python 3.14.7 with uv 0.12.15 and the other 3.15.0 with uv 0.13.0. List
what you would pin so that a rebuild next month gives the same image, and say how you would make
the VM run exactly the image you tested.

<details><summary>Answer</summary>

- The base image, by digest:
  `FROM python:3.12-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258`
  (the multi-platform index the README's tag pointed at on 2026-10-13, `laptop/09`). A tag like
  `3.12-slim-bookworm` moves with every patch release.
- uv itself: `pip install uv==0.13.0`, not `pip install uv`.
- The Python: a base image that meets `requires-python`, or a pinned version (`uv python pin`, L1),
  and `ENV UV_PYTHON_DOWNLOADS=never` so a mismatch fails (B1).
- The packages: commit a `uv.lock` (the repo has none) and build with `uv sync --locked` (B3).
- `apt-get upgrade -y` still takes whatever Debian ships that day.

Even then, a rebuild is a new image. To run exactly the one you tested, deploy the image, not the
recipe: push it once and run it by its digest (`<USER NAME>/simple-translate-ac215@sha256:…`, the
`digest:` line of your push), or with a version tag you never reuse. `latest` is just a name that
moves.
</details>

**D3. Before you push to a public repository.** A new Docker Hub repository is public. What could
your image tell a stranger, and what doesn't fix it?

<details><summary>Answer</summary>

Everything `COPY . ./` copied. That includes `.git`, your whole commit history with author names
and e-mail addresses: the published `dlops/simple-translate` contains `/.git` with its `logs/`.
It also includes `.vscode`, and any key or `secrets/` folder in the project, a real risk from L3
on. `docker history` shows every `RUN` line, and `docker image inspect` every `ENV` value, so a
secret in either is public too.

What doesn't fix it: deleting the file in a later step. A file that `COPY` added and a later
`RUN rm` deleted is gone from the running container but still sits in the earlier layer, and
anyone who pulls the image can extract it (checked with a dummy token file and `docker save`).
Adding a `.dockerignore` now doesn't change images you already pushed. Keep secrets out of the
build context (`.dockerignore`), rebuild, push again, and delete or make private any repository
that leaked.
</details>

**D4. What's still running after the lecture?** List everything this lecture may have left
behind, and what each one costs.

<details><summary>Answer</summary>

- **The VM** bills per second while it runs, and its boot disk bills while it exists. Delete it
  with its disk, then check that *VM instances* and *Disks* are empty (`README.md:220`).
- **Your Docker Hub repository** is free but public until you delete it or make it private (D3).
- **Your laptop's disk**: the image is 518MB as Docker 29 counts it, plus the build cache and the
  base image. `docker system prune -a` removes stopped containers, unused networks, every image no
  container uses, and the build cache; images download again when you next need them.
- **The `multi-arch` builder**, if you ran `docker-build-push.sh`: a running container
  (`buildx_buildkit_multi-arch0`) with its own cache. Remove it with `docker buildx rm multi-arch`,
  then `docker buildx use default`.
- **Containers**: none, if every run used `--rm`. Check with `docker ps -a` on the laptop and
  `sudo docker ps -a` on the VM before you delete it (`laptop/32`, `vm-debian12/11`).
- Optionally, `docker logout`.
</details>
