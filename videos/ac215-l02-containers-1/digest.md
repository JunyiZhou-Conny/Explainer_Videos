# L02 · Containers I — tutorial digest

- **Ed lesson:** https://edstem.org/us/courses/97373/lessons/166028/ (course-site map: `src/2026-AC215/tutorials_demo.md:31-42`; lecture date Sep 8 per `_modules/week-02.md:5-7`)
- **Repo used:** `dlops-io/simple-translate`
  - branch `main`, commit `62f821bfe09fc1c2ecb0f14354b1f205777c0efa`, committed 2026-09-08 13:58:15 -0400 ("Handle translation exceptions with detailed error messages")
  - other branch in the repo, **not** used by L02: `origin/pipenv` @ `3a354d81f787a064aea3ab061359c9a1e223e4d5` (2026-08-28; a tag `pipenv` points at the same commit). It is an older Pipenv / Python 3.11 variant whose README names the image `simple-translate-e115` (`origin/pipenv:README.md:91-92,114`). It shares no history with `main`.
- **README sections covered:**
  - [🐳 Developing App using Containers](https://github.com/dlops-io/simple-translate?tab=readme-ov-file#-developing-app-using-containers): `README.md:106-191` (Dockerfile, build, run, push to Docker Hub)
  - [☁️ Running App on VM using Docker](https://github.com/dlops-io/simple-translate?tab=readme-ov-file#%EF%B8%8F-running-app-on-vm-using-docker): `README.md:203-220`
- **Colab notebooks:** none for this lecture.
- **Context repos read for sections 7 and 10:** `dlops-io/mega-pipeline` `main` @ `c6bbc9ba88984e1234b68ccf5cdf7c00f7e9accc` (2026-09-27, the L03 tutorial); `port_toy` `main` @ `d190c71` (2026-09-20, L04); `ml-workflow` `main` @ `972ffbb` (2025-10-23) and `cheese-app-v4` `main` @ `033f187` (2025-12-02) for the later multi-arch push scripts.
- **Published image pulled and inspected (2026-10-13):** `docker.io/dlops/simple-translate:latest`, manifest digest `sha256:2454010bcf64b211d81805c38ae3dfc7842bff6fed558bb3bb6dc7659a63f916`. It is a single `linux/amd64` manifest (`application/vnd.docker.distribution.manifest.v2+json`, not a multi-arch index), config `sha256:8a968f7e6f7a0387bd9993abf30518d30d45ec7440e18a70669f8bf2b8bfa5b2`, created 2026-09-16T21:28:58-04:00. Its `docker history` matches `Dockerfile.txt` instruction for instruction. I opened it only in disposable containers (`--network none`, `--entrypoint /bin/bash`) to read files. See Concept 8 and Errata E1, E5.
- **Method (verification, 2026-10-13):** every `path:line` below was checked with `sed -n` against `62f821b`. I built `Dockerfile.txt` and each of the README's five Dockerfile versions in a sandbox: Docker Engine 29.8.2, containerd image store, BuildKit v0.33.1, linux/amd64. The builds used a **capture-only** addition, not part of the tutorial: the sandbox's TLS-proxy CA and https apt sources. I ran the results in disposable containers. Outputs marked *observed* come from those runs. Outputs marked *expected* were not run here: anything on macOS / Apple Silicon, `docker login`/`push`, and the GCP VM.
- **AWS variant** (`simple-translate-aws`) was not examined.

---

## 1. What you build

You take the small command-line translator `cli.py` and package it as a Docker **image**. The image holds a Debian 12 userland (files, not a kernel), the base image's Python 3.12, `uv`, a second CPython that uv downloads because `pyproject.toml` asks for ≥3.13 (3.15.0 at the time of recording, see Concept 8), the app's virtual environment and the source code. You build it on your laptop, run it as a throw-away **container**, give it a Docker Hub name and push it to the **registry**. Then you create a fresh Google Compute Engine VM that has nothing installed except Docker. There you pull an image and run the same app with one `docker run`: no `git clone`, no `pip`, no `uv` on the VM. The README's command pulls the instructor's `dlops/simple-translate`, not the image you pushed (Errata E4). This is Steps 3 and 4 of the README's four-step ladder (`README.md:9-16`). Steps 1 and 2 (manual install, then `uv` on a VM) were Lecture 1. The app has no web server, so no ports are published and no volumes are mounted. The only network traffic is the build-time downloads and the runtime HTTPS call to Google's unofficial translate endpoint.

```
 YOUR LAPTOP  (macOS; Apple Silicon = arm64, Intel = amd64)
 +-----------------------------------------------------------------------+
 |  ~/.../simple-translate/   (git clone)                                 |
 |    Dockerfile  (you write it; solution = Dockerfile.txt)               |
 |    cli.py   pyproject.toml   docker-shell.sh   docker-build-push.sh    |
 |       |                                                                |
 |       |  docker build -t simple-translate -f Dockerfile .              |
 |       |  (the "." = build context, sent to BuildKit)                   |
 |       v                                                                |
 |  +-- Docker Desktop: a hidden Linux VM --------------------------+     |
 |  |  dockerd + BuildKit                                           |     |
 |  |  local image store:  simple-translate:latest                  |     |
 |  |     (4 base layers from python:3.12-slim-bookworm + 3 yours)  |     |
 |  |       | docker run --rm -ti simple-translate                  |     |
 |  |       v                                                       |     |
 |  |  [container]  /bin/bash -c "source .venv/bin/activate         |     |
 |  |               && exec bash"                                   |     |
 |  |     root@<id>:/# python cli.py -t ... -s en -d es  ------------+-----+--> HTTPS translate.googleapis.com
 |  +---------------------------------------------------------------+     |     (googletrans, unofficial endpoint)
 +-------------------------------|---------------------------------------+
                                 | docker login / docker tag / docker push
                                 | (only layers the registry lacks are uploaded)
                                 v
                 +----------------------------------------+
                 |  Docker Hub  (registry, docker.io)     |
                 |   <USER NAME>/simple-translate-ac215   |  <- your image (arm64 if built
                 |   dlops/simple-translate:latest        |     plainly on an M-series Mac!)
                 |      (instructor's; linux/amd64 only)  |
                 +-------------------|--------------------+
                                     | docker pull (implicit in docker run)
                                     v
 GOOGLE CLOUD PROJECT -> Compute Engine VM (Debian; x86_64 = amd64 by default)
 +-----------------------------------------------------------------------+
 |  sudo apt install docker.io        -> dockerd                          |
 |  sudo docker run --rm -ti dlops/simple-translate                       |
 |     [container] root@<id>:/# python cli.py  ---------------------------+--> HTTPS translate.googleapis.com
 +-----------------------------------------------------------------------+
   No ports (-p), no volumes (-v), no service account, no secrets.
```

---

## 2. Prerequisites and costs

**Accounts**
- A **GCP account and project with billing enabled**, from Tutorial 0 (`README.md:20-21`). You need the **Compute Engine API**; the console asks you to enable it the first time you open *VM instances*. No other GCP API is used.
- A **Docker Hub account** plus a **Personal Access Token**, used as the password for `docker login` (`README.md:188-189`).
- No service account and no JSON key: "You don't need GCP credentials (a service account) for this tutorial" (`README.md:23`).

**Local installs** (from Tutorial 0, `README.md:110-111`)
- Docker Desktop, running (check: `docker run hello-world`), plus VS Code and Git. `uv` is not needed on the laptop, because the image installs its own.
- Check your CPU architecture now with `uname -m`. `arm64` means Apple Silicon (read Gotcha G1 before pushing); `x86_64` means Intel.

**Secrets, files and environment variables the code expects**
- `cli.py` reads **no** environment variables and **no** secrets files.
- `Dockerfile.txt` sets three build/runtime env vars: `DEBIAN_FRONTEND=noninteractive`, `LANG=C.UTF-8` and `PYTHONUNBUFFERED=1` (`Dockerfile.txt:5,8,11`).
- Your Docker Hub token is stored by `docker login` through the credential helper configured in `~/.docker/config.json` (on Docker Desktop for Mac, the macOS keychain). Do **not** put it in the repo.
- The only file the tooling insists on is **`Dockerfile`** in the repo root. Both helper scripts call `-f Dockerfile` (`docker-shell.sh:11`, `docker-build-push.sh:27`), but the repo ships only `Dockerfile.txt`, and `.gitignore:3` ignores `Dockerfile`, so you must create it.

**Network**
- The build downloads the base image from Docker Hub, package lists from the Debian mirrors, a newer `pip` and `uv` from PyPI, a **standalone CPython** (because of `requires-python = ">=3.13"`, see Concept 8), and the app's wheels from PyPI. uv 0.13.0 fetches the CPython (a python-build-standalone build) from `releases.astral.sh`, Astral's mirror of the project's GitHub releases (*observed* with `uv python list --show-urls`).
- At runtime the app calls `https://translate.googleapis.com/translate_a/single`. This is googletrans 4.0.2's default host, per `googletrans/constants.py:3` and `googletrans/urls.py:7` in the wheel.

**Billable resources and shutdown**

| Resource | Billed while | How to stop it |
|---|---|---|
| Compute Engine VM (any E2 type is enough; e2-small/e2-medium cost a few US cents per hour at list price, and the create page shows an estimate) | running | **Delete** the VM: `README.md:220` ("Go to VM instances, select your instance, and click Delete"). Stopping alone keeps the disk billed. |
| Boot persistent disk (default 10 GB) | it exists, **even while the VM is stopped** | deleted with the VM by default ("Delete boot disk when instance is deleted") |
| Ephemeral external IPv4 | VM running | released when the VM is deleted |
| Docker Hub repo | free (public by default) | optional: delete the repo on hub.docker.com |
| Laptop disk (images, build cache, buildx builder container) | n/a | `docker system prune -a`, `docker buildx rm multi-arch` (if you ran `docker-build-push.sh`) |

If you prefer the CLI (my addition, not in the README): `gcloud compute instances delete <VM_NAME> --zone=<ZONE>`.

---

## 3. Concepts this tutorial teaches

Concepts marked ★ are the ones that most deserve an **animated** explanation.

### C1 ★ Image, layer, container, registry (and tag)
- **Explanation.**
  - An **image** is a read-only, content-addressed stack of filesystem **layers** plus a small JSON config (env vars, entrypoint, default command, architecture).
  - Each `RUN`/`COPY` instruction in a Dockerfile produces one layer, a tarball of the files it changed. `ENV`/`ENTRYPOINT`/`CMD` only edit the config.
  - A **container** is a running (or stopped) instance: the image's layers stacked read-only, plus one thin **writable layer** on top, plus a process.
  - A **registry** (Docker Hub) stores layers and manifests under **repository** names. A **tag** (`:latest`) is a movable pointer to one manifest, or to an index of per-platform manifests (C7).
- **Mental model.** The image is a *class*; containers are *instances*. The registry is *PyPI for images*. A tag is a *git branch name*: it points at a content hash and can be moved.
- **Analogy.** An image is a frozen meal in its sealed tray: layers are the ingredients stacked in the order they were added. A container is that meal heated on a plate. You can add salt, which only touches the plate, and when you throw the plate away (`--rm`) the tray in the freezer is unchanged.
- **Misconception.** "`docker build` builds a container." The README itself says "Build the docker container" (`README.md:173`), but build produces an **image**. Run produces a container. A second misconception: "my changes inside the container are saved". They live only in that container's writable layer and vanish with `--rm`.
- **Concrete numbers** (*observed* with `docker history dlops/simple-translate`, unpacked sizes in decimal MB). The published image has 7 layers, 146 MB compressed.
  - 4 layers come from `python:3.12-slim-bookworm`: 85.3 + 10.4 + 45.0 + 0.02 ≈ 141 MB.
  - The 3 added by `Dockerfile.txt` are 111 MB (apt/pip/uv), 0.5 MB (`COPY . ./`) and 127 MB (`uv sync`).
  - The `ENV`, `ENTRYPOINT` and `CMD` lines are listed with 0 B.
  - A fresh amd64 build on 2026-10-13 gave 97.5 MB, 0.26 MB and 125 MB, on a 149.5 MB base (Python 3.12.15).
- **Animation.** Translucent slabs drop onto a stack, each labelled with its Dockerfile line. A glass lid labelled "config" snaps on top. The stack is cloned into a "container" with a thin glowing slab above it. `exit` + `--rm` makes only the glowing slab dissolve. Separately, slabs fly to a shelf labelled "Docker Hub" and a sticky note `:latest` attaches to the stack.

### C2 Dockerfile, build context and working directory
- **Explanation.** A Dockerfile is a recipe executed top to bottom by BuildKit:
  - `FROM` picks the starting image.
  - `ENV` sets environment variables in the image config.
  - `RUN` executes a shell command in a temporary container and snapshots the result as a layer.
  - `COPY . ./` copies files from the **build context**: the directory you pass as the last argument of `docker build`, here `.`.
  - `ENTRYPOINT`/`CMD` record what runs when a container starts.
  - With no `WORKDIR`, relative paths resolve against `/`. The python base image sets none (its config has no `WorkingDir`), so `COPY . ./` drops `cli.py` at **`/cli.py`** and `uv sync` creates **`/.venv`**. The published image's `activate` script confirms this with `VIRTUAL_ENV='/.venv'`.
- **Mental model.** `docker build` = "ship a tarball of `.` to a builder, replay the recipe, and snapshot after each step".
- **Analogy.** A lab protocol: the context is the box of reagents you hand to the technician, who can use nothing outside that box.
- **Misconception.** "`COPY` copies only what my app needs." It copies *everything* in the context that is not excluded by a `.dockerignore`, and this repo has none.
  - The published image contains the author's whole `.git/` directory, because of `Dockerfile.txt:22`. Its HEAD is `2827e2a`. It includes an editor's search index under `.git/cursor/crepe/…` and a reflog with the commit authors' names and e-mails.
  - A fresh build also copies your own `Dockerfile` (*observed*: `ls /` lists `Dockerfile` next to `Dockerfile.txt`).

### C3 ★ Layer cache and instruction order
- **Explanation.** BuildKit caches each step, keyed on the parent layer plus the instruction (plus, for `COPY`, a checksum of the copied files). If a step's key matches, it is reused (`CACHED`). The first changed step **and every step after it** are rebuilt. In `Dockerfile.txt`, `COPY . ./` (line 22) comes *before* `RUN uv sync` (line 24). Editing any file in the folder therefore invalidates the copy, which forces `uv sync` to run again. That includes `README.md` and even the `Dockerfile` itself, which sits in the context. The re-run downloads the CPython again (35.9 MiB compressed, ~100 MB unpacked; Concept 8) plus all the wheels. *Observed:* when the README's Step 5 adds only the `CMD` line at the end, the rebuild re-runs both `COPY . ./` and `RUN uv sync`, because the edited `Dockerfile` is one of the files `COPY . ./` copies.
- **Mental model.** A row of dominoes: a change knocks over its own domino and everything to its right, never anything to its left. Put rarely-changing steps on the left: copy `pyproject.toml`/`uv.lock` first, run `uv sync`, then copy the code.
- **Analogy.** Re-doing a recipe from the step where you changed an ingredient. Changing the garnish should not make you re-bake the cake.
- **Misconception.** "Docker caches per file, so changing `cli.py` only re-copies `cli.py`." It re-runs every later instruction.
- **Animation.** A horizontal chain of step boxes, each with a hash fingerprint. Edit `cli.py`: the `COPY` box's fingerprint changes colour, and a red wave flows right through `RUN uv sync` while the boxes on the left glow green ("CACHED"). Then swap the order: the wave now stops at a tiny "COPY cli.py" box.

### C4 ★ ENTRYPOINT + CMD = the container's command line
- **Explanation.** At start-up Docker runs `ENTRYPOINT` followed by `CMD` as one argv. Here that is `["/bin/bash"] + ["-c", "source .venv/bin/activate && exec bash"]`, i.e. `/bin/bash -c "source .venv/bin/activate && exec bash"` (`Dockerfile.txt:27,29`). `source` loads the venv, which exports `PATH=/.venv/bin:...` and `VIRTUAL_ENV`. Then `exec bash` *replaces* that shell with an interactive bash that inherits those variables, so `python` means the venv's Python. Anything you type after the image name in `docker run IMAGE ...` **replaces CMD only**. `--entrypoint` replaces the entrypoint and also clears the image's CMD. Also, setting `ENTRYPOINT` resets any `CMD` inherited from the base image. That is why README Step 2 (`README.md:139-143`) turns "start a Python REPL" (the base image's `CMD ["python3"]`) into "start bash".
- **Mental model.** ENTRYPOINT is the *verb*, CMD the *default arguments*. `docker run` arguments are *replacement arguments*.
- **Analogy.** A coffee machine: ENTRYPOINT is "brew", CMD is the default "medium latte" button. Typing your own order replaces the latte, not the act of brewing.
- **Misconception.** "`docker run --rm -ti simple-translate python cli.py` runs my script." It actually runs `/bin/bash python cli.py`.
  - Bash reads its first argument as the name of a *shell script*.
  - There is no `python` file in `/`, so bash searches `PATH` and finds the binary `/usr/local/bin/python`. The venv was never activated, so this is the base image's Python.
  - Bash refuses to read a binary as a script. *Observed:* `/usr/local/bin/python: /usr/local/bin/python: cannot execute binary file`, exit code 126.
- **Animation.** Two puzzle tiles, `["/bin/bash"]` and `["-c", "source … && exec bash"]`, slide together into one command line. A third tile, `python cli.py`, slides in from `docker run` and *knocks out* the CMD tile, leaving the malformed `/bin/bash python cli.py`, which flashes red.

### C5 Container lifecycle and the `docker run` flags used
- **Explanation.**
  - `-i` keeps STDIN open and attached, so your keystrokes reach bash.
  - `-t` allocates a pseudo-terminal, giving you a prompt, line editing and colours.
  - `--rm` deletes the container (its writable layer) when its main process exits.
  - `--name simple-translate` (only in `docker-shell.sh:15`) gives it a fixed name, which must be unique among existing containers.
  - The container lives exactly as long as its PID 1, here the `exec`-ed bash, so typing `exit` stops it (`README.md:184`).
  - `docker container ls` lists running containers. `docker system prune` removes stopped containers, unused networks, dangling images and unused build cache (`README.md:115-118`).
- **Mental model.** A container is a process with its own filesystem view. When the process dies, the container stops.
- **Analogy.** A hotel room: `--rm` is "housekeeping wipes the room at checkout". Without it the room (a stopped container) stays booked and keeps its mess.
- **Misconception.** "Stopping a container deletes it." Without `--rm`, stopped containers pile up; `docker ps -a` shows them.

### C6 Containers vs VMs (and why a Mac needs a hidden VM)
- **Explanation.** A VM virtualises hardware and boots its own kernel. A container is an isolated *process* that shares the host's Linux kernel, using namespaces and cgroups. Linux images need a Linux kernel, so on macOS Docker Desktop runs a lightweight Linux VM, and your containers run *inside* it. On the GCP VM, Docker runs directly on the VM's Debian kernel. In Step 4 you stack both ideas: a container inside a cloud VM.
- **Mental model.** VM = a separate house. Container = a separate apartment in a shared building: separate doors and furniture, but shared plumbing (the kernel).
- **Misconception.** "A container includes an OS kernel." It includes OS *userland files* (Debian's `/bin`, `/usr`, apt …) but not a kernel. That is also why CPU architecture still matters (C7).

### C7 ★ CPU architecture and multi-platform images
- **Explanation.** Every binary in an image (bash, CPython, uv) is compiled for one CPU instruction set: `linux/amd64` (Intel/AMD, GCP's default E2 VMs) or `linux/arm64` (Apple Silicon, GCP T2A/C4A). A plain `docker build` on an M-series Mac produces an **arm64** image. A registry tag can point to a **manifest list / image index**, a menu of per-platform manifests. `docker pull` picks the entry matching the host.
  - The base `python:3.12-slim-bookworm` index lists amd64, arm/v7, arm64/v8, 386 and ppc64le (plus attestation entries).
  - Your plain push lists only arm64, so an amd64 VM either fails to pull it or pulls it and fails to execute it (Gotcha G1). Which of the two depends on your Docker's image store:
    - The containerd image store (the default for fresh installs of recent Docker versions) exports even a plain `docker build` as an index: your one platform plus an attestation manifest. *Observed* in the amd64 build log: `exporting attestation manifest`, then `exporting manifest list`.
    - The classic store pushes a single manifest.
  - Fixes in the repo, neither mentioned in the README:
    - build for amd64 with `docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .` (commented out at `docker-shell.sh:12`);
    - build and push both platforms with `docker buildx build --platform linux/amd64,linux/arm64 --push ...` (`docker-build-push.sh:27`). This uses QEMU/Rosetta emulation for the foreign platform, which is slower.
- **Mental model.** An image tag is a restaurant menu. The VM orders "amd64". If the menu only lists "arm64", there is nothing to serve.
- **Analogy.** A DVD region code: same movie, same disc format, but the player refuses the wrong region.
- **Misconception.** "Containers are portable everywhere." They are portable across *Linux hosts of the same CPU architecture*; across architectures you need a multi-arch image or emulation.
- **Animation.** Two chips, labelled ARM and x86, each with its own "alphabet" of instructions. An image built on the ARM chip carries ARM glyphs. Shipped to an x86 VM, the glyphs do not match and the screen shows `exec format error`. Then buildx forks the build into two lanes (one through a QEMU "translator" box), both stacks fly to Docker Hub, and an index card listing both platforms appears. The x86 VM picks its row.

### C8 ★ Who actually provides Python inside this image?
- **Explanation.** The base image ships CPython **3.12** (`FROM python:3.12-slim-bookworm`, `Dockerfile.txt:2`), but `pyproject.toml:6` says `requires-python = ">=3.13"` (changed from `">=3.12,<3.13"` in commit `2827e2a`, 2026-09-02). When `RUN uv sync` (`Dockerfile.txt:24`) finds no compatible interpreter, uv **downloads a standalone CPython** into `/root/.local/share/uv/python/` and builds `/.venv` on it. The base image's 3.12 is then used only to run `pip install uv`. Evidence from the published image (*observed*):
  - `.venv/bin/python -> /root/.local/share/uv/python/cpython-3.14-linux-x86_64-gnu/bin/python3.14`
  - the directory `cpython-3.14.7-linux-x86_64-gnu/`: 98 MiB of files (107 MiB on disk) out of the 127 MB `uv sync` layer
  - `pyvenv.cfg` with `version_info = 3.14` and `uv = 0.12.15`
  - a freshly generated `/uv.lock` with `requires-python = ">=3.13"` and 13 `[[package]]` entries: the project `app` plus 12 dependencies (anyio, art 6.5, certifi, googletrans 4.0.2, h11, h2, hpack, httpcore, httpx 0.28.1, hyperframe, idna, typing-extensions)
  - A fresh build on 2026-10-13 (*observed*) behaved the same way, with newer versions:
    - `pip install uv` installed uv 0.13.0;
    - `uv sync` printed `Downloading cpython-3.15.0-linux-x86_64-gnu (download) (35.9MiB)`, `Using CPython 3.15.0`, `Creating virtual environment at: /.venv` and `Installed 11 packages` (typing-extensions is only needed below Python 3.15);
    - in the container, `python --version` printed `Python 3.15.0`, while `/usr/local/bin/python --version` printed `Python 3.12.15`.
- **Mental model.** The `FROM` line is a *suggestion* about Python. The project file plus the package manager decide which Python actually runs.
- **Misconception.** "The README says Python 3.12 (`README.md:133`), so the app runs on 3.12."
  - Inside the container, `python --version` printed **3.15.0** in a fresh build on 2026-10-13 (*observed*). It prints 3.14.7 in the instructor's image.
  - The version depends on the uv release that the build installed: uv picks the newest CPython it knows that satisfies `>=3.13`.
- **Animation.** A slab labelled "Python 3.12 (base)" sits in the stack. `uv sync` reads `>=3.13` from pyproject, the 3.12 slab greys out with a ✗, and a fat new 3.15 slab (~100 MB; 3.14 in the instructor's image) is pulled down from a cloud labelled "python-build-standalone" and wired to `.venv`.

---

## 4. Step-by-step walkthrough

Work in a terminal on your **laptop** for steps 1-11b, in the browser (Cloud console) for step 12, and on the **VM** for steps 13-17. README line numbers refer to `README.md` at commit `62f821b`.

### Phase A: Build and run locally

**Step 1. Make sure Docker is up and clean** (`README.md:110-118`)
```
docker container ls
docker system prune
docker image ls
```
- **Under the hood:** `container ls` (the same as `docker ps`) lists *running* containers. For any you see, use `docker stop <CONTAINER ID>` ("Stop any container that is running", `README.md:116`). `system prune` asks for confirmation (`[y/N]`), then deletes stopped containers, unused networks, **dangling** (untagged) images and unused build cache. Tagged-but-unused images survive unless you add `-a`.
- **Checkpoint:** `docker container ls` prints only the header row. `docker image ls` prints a (possibly empty) table of images.
- **If it fails:** `Cannot connect to the Docker daemon at unix:///…/docker.sock. Is the docker daemon running?` means Docker Desktop is not started. Open it and wait for "Engine running".
- **Extra check (not a step of this section):** the README's note (`README.md:110-111`) points back to Tutorial 0's `docker run hello-world`. Run it if you are unsure that Docker works.

**Step 2. Clone the repo on your laptop** (`README.md:120-125`)
- The README says "Clone or download from [here]". The command (from `README.md:50`) is:
```
git clone https://github.com/dlops-io/simple-translate.git
cd simple-translate
```
- e.g. inside your course folder (`~/Desktop/AC215`). The note at `README.md:122-123` matters: a clone you made on the L01 VM does not help, because Docker Desktop runs on your laptop.
- **Checkpoint:** `ls` shows `Dockerfile.txt README.md cli.py docker-build-push.sh docker-shell.sh pyproject.toml`. There is no `Dockerfile` and no `uv.lock`.

**Step 3. Create `Dockerfile`, version 1: base image only** (`README.md:127-137`)
```
# Use the official Debian-hosted Python image
FROM python:3.12-slim-bookworm
```
- Create the file in VS Code (not TextEdit, which can silently add `.rtf`/`.txt`). The README asks you to "Do a Build + Run after each step" (`README.md:130`), using the commands from `README.md:174` and `README.md:180`:
```
docker build -t simple-translate -f Dockerfile .
docker run --rm -ti simple-translate
```
- **Under the hood:** `-t simple-translate` names the result `docker.io/library/simple-translate:latest` (the build log ends with "naming to …"). `-f Dockerfile` is the default name, so it is redundant but explicit. `.` is the build context.
- **Observed:** a **Python 3.12 REPL**: `Python 3.12.15 (main, Oct  6 2026, 02:02:31) [GCC 12.2.0] on linux`, then `>>>`. The patch version depends on when your base image was pulled. The REPL appears because the image inherits the base config `CMD ["python3"]`. Leave with `exit()` or Ctrl-D.

**Step 4. Version 2: add the entrypoint** (`README.md:139-143`)
```
ENTRYPOINT ["/bin/bash"]
```
- Rebuild and re-run with the same two commands.
- **Observed:** a bash prompt like `root@e8c2e6d6e51d:/#`. The hostname is the container ID, the user is root and the directory is `/`. Setting `ENTRYPOINT` cleared the inherited `CMD ["python3"]`, so bash starts with no arguments (Concept 4).

**Step 5. Version 3: install uv and copy the code** (`README.md:145-152`)
```
# Install uv
RUN pip install uv
# Copy the source code
COPY . ./
```
- **Under the hood:** `RUN` executes in a temporary container and snapshots the change as a layer. pip may print a harmless "Running pip as the 'root' user…" warning. `COPY . ./` copies the whole context (including `.git/` and `Dockerfile` itself) into `/`.
- **Checkpoint inside the container (*observed*):** `ls` in `/` shows `Dockerfile  Dockerfile.txt  README.md  cli.py  docker-build-push.sh  docker-shell.sh  pyproject.toml` mixed in with `bin etc usr …`.
- **Pause-and-ponder:** `python cli.py` fails (*observed*): a traceback through `File "//cli.py", line 8, in <module>` ending in `ModuleNotFoundError: No module named 'art'`. The system Python 3.12 has no project dependencies yet.

**Step 6. Version 4: create the venv** (`README.md:154-158`)
```
RUN uv sync
```
- Build with `--progress=plain` to see uv's log: `docker build --progress=plain -t simple-translate -f Dockerfile .`
- **Under the hood:** uv reads `pyproject.toml` (`pyproject.toml:6-10`). It finds no interpreter `>=3.13` on the image and downloads a standalone CPython: 3.15.0 in a fresh build on 2026-10-13 (*observed*), 3.14.7 in the published image. It then creates `/.venv`, resolves and writes `/uv.lock` (there is no lock in the repo, so versions float) and installs 11 packages (12 on Python 3.14).
- Because your `Dockerfile` is inside the build context, this rebuild re-runs `COPY . ./` even though you only appended a line. The same happens at Step 7 (G21).
- **Checkpoint inside the container:**
  - `ls -a /` now shows `.venv` and `uv.lock`.
  - `python cli.py` *still* fails with the same `ModuleNotFoundError` (*observed*), because `python` is `/usr/local/bin/python` (3.12).
  - `source .venv/bin/activate && python cli.py` works.
  - `.venv/bin/python --version` → `Python 3.15.0` (*observed*, 2026-10-13).

**Step 7. Version 5: auto-activate the venv** (`README.md:160-165`)
```
# Get into the uv virtual environment shell
CMD ["-c", "source .venv/bin/activate && exec bash"]
```
- **Observed:** you land at `root@<id>:/#`.
  - The `(app)` prefix is missing. `activate` does export `PS1="(app) "`, but the interactive bash started by `exec bash` reads Debian's `/etc/bash.bashrc`, which sets `PS1` again (`/etc/bash.bashrc:21` in the image).
  - The venv **is** active (*observed*): `which python` → `/.venv/bin/python`, `echo $VIRTUAL_ENV` → `/.venv`, `python --version` → `Python 3.15.0`, `pwd` → `/`.

**Step 8. Compare with the solution** (`README.md:167-168`)
- Your file (assembled from `README.md:134-164`) is a subset of `Dockerfile.txt`. The solution adds:
  - the three `ENV` lines (`Dockerfile.txt:4-11`);
  - one `RUN set -ex; …` that does `apt-get update && apt-get upgrade -y && apt-get clean`, upgrades pip and then runs your `pip install uv` (`Dockerfile.txt:14-19`), so the solution has one `RUN` layer where yours has two;
  - `ENTRYPOINT` moved to the end (`Dockerfile.txt:27`). Order does not matter for ENTRYPOINT/CMD.
- Shortcut: `cp Dockerfile.txt Dockerfile`.

**Step 9. Build the final image** (`README.md:170-174`)
```
docker build -t simple-translate -f Dockerfile .
```
- **Checkpoint:** `docker image ls` lists `simple-translate` with the tag `latest`. The size columns depend on your Docker version:
  - With the containerd image store (Docker 29), a fresh amd64 build showed `DISK USAGE 517MB`, `CONTENT SIZE 144MB` (*observed*). Disk usage counts the compressed layers (~144 MB) plus their unpacked copy (~373 MB).
  - The classic store's single `SIZE` column shows the unpacked size, roughly 370–380 MB.
  - An arm64 build on a Mac differs a little.
- Check its platform: `docker image inspect simple-translate --format '{{.Os}}/{{.Architecture}}'` → `linux/arm64` on Apple Silicon, `linux/amd64` on Intel.

**Step 10. Run it and translate** (`README.md:176-184`)
```
docker run --rm -ti simple-translate
python cli.py -t "Good morning" -s "en" -d "es"
exit
```
- **Observed output** (fresh build, sandbox network, 2026-10-13):
  - two blank lines and a large ASCII-art "AC215" banner (`cli.py:13-14`)
  - `Arguments: Namespace(text='Good morning', file='', src='en', dest='es')` (`cli.py:15`)
  - `Input: Good morning` (`cli.py:23`)
  - `Output: Buen día` (`cli.py:39`; Google's wording can change)
- `exit` ends bash (PID 1), the container stops, and `--rm` deletes it.
- **Equivalent helper (not mentioned in the README):** `sh docker-shell.sh` does build + run in one go (`docker-shell.sh:11,15`), adding `--name simple-translate`.
- **If it fails:**
  - A `RuntimeError: Translation request to Google Translate failed (…rate-limited or blocked…)` comes from `cli.py:32-37`. It means the request to the unofficial Google endpoint failed: refused, rate-limited, or no network at all. With `--network none` the traceback ends in exactly this line (*observed*). Retry later or on another network; your Docker setup is fine.

### Phase B: Push to Docker Hub

**Step 11. Log in, tag, push** (`README.md:186-191`)
- Create an access token ("Sign up in Docker Hub and create an [Access Token]", `README.md:188`), then:
```
docker login -u <USER NAME> -p <ACCESS TOKEN>
docker tag simple-translate <USER NAME>/simple-translate-ac215
docker push <USER NAME>/simple-translate-ac215
```
- **Under the hood:**
  - `docker login` stores the credential; prefer `docker login -u <USER NAME>` and paste the token at the prompt (Gotcha G13).
  - `docker tag` adds a second **name** pointing at the *same* image ID: no copy, no rebuild. The name expands to `docker.io/<USER NAME>/simple-translate-ac215:latest`.
  - `docker push` uploads only layers the registry does not have. *Expected* (not run here, no credentials): the base layers may show `Mounted from library/python`, a cross-repository mount with no upload, while your 3 layers show `Pushed`. A `latest: digest: sha256:… size: …` line ends it. The exact lines differ between the classic and containerd image stores.
- **Checkpoint:** the repo appears (public) under your account on hub.docker.com.
- **If it fails:**
  - `denied: requested access to the resource is denied` → you are not logged in, or the prefix is not *your* username.
  - Uppercase letters in the name. `docker build -t` says `invalid tag "…": repository name must be lowercase`, and `docker run` says `invalid reference format: repository name (…) must be lowercase` (both *observed*). Docker Hub names are lowercase, so use lowercase.

**Step 11b. (Apple Silicon only; NOT in the README) Publish an image the VM can run**
- Before you deploy your own image to a default x86 VM, push an amd64 or multi-arch build. Either:
```
docker build -t simple-translate --platform=linux/amd64 -f Dockerfile .
docker tag simple-translate <USER NAME>/simple-translate-ac215
docker push <USER NAME>/simple-translate-ac215
```
  (the build line is the variant commented out at `docker-shell.sh:12`), or log in (Step 11), edit `DOCKER_USERNAME="dlops"` (`docker-build-push.sh:11`) and `IMAGE_NAME` (`docker-build-push.sh:7`, e.g. to `simple-translate-ac215`), and run `bash docker-build-push.sh` (it is not executable, see G4). It builds both `linux/amd64` and `linux/arm64` and pushes them (`docker-build-push.sh:23-27`).
- **Afterwards:** run `docker buildx use default` (or `desktop-linux`; see `docker buildx ls`) so later plain `docker build`s load into your local image store again (G2).
- **Verify:** `docker buildx imagetools inspect <USER NAME>/simple-translate-ac215` lists `Platform: linux/amd64` (and `linux/arm64`).

### Phase C: Run on a VM with Docker

**Step 12. Create a VM and SSH in** (`README.md:207-208`)
- "Create a VM Instance from GCP", then "SSH into your newly created instance". The README does not specify a machine type. A default **E2 (x86/amd64)** machine with a Debian image works with the instructor's image. Avoid T2A/C4A (Arm) unless your image is multi-arch.
- Optional CLI equivalent (my addition, not in the README):
```
gcloud compute instances create simple-translate-vm --zone=us-central1-a --machine-type=e2-small --image-family=debian-12 --image-project=debian-cloud
gcloud compute ssh simple-translate-vm --zone=us-central1-a
```
- **Checkpoint:** `uname -m` → `x86_64`.

**Step 13. Install Docker on the VM** (`README.md:209-210`)
```
sudo apt install docker.io
```
- **Under the hood:** this installs Debian's packaged Docker engine (dockerd, containerd, runc) and starts the service. Answer `Y` at the prompt.
- The README omits the `sudo apt-get update` it used in walkthroughs 1-2 (`README.md:44,74`). Run `sudo apt-get update` first if you get `E: Unable to locate package docker.io`, or 404 errors from stale package lists. In a fresh Debian container with empty lists, `apt-get install -y docker.io` exits with code 100 (*observed*).
- Package candidates on 2026-10-13 (*observed* with `apt-cache policy docker.io` in Debian containers): Debian 12 `20.10.24+dfsg1-1+deb12u1+b6`, Debian 13 `26.1.5+dfsg1-9+deb13u1`.

**Step 14. Verify** (`README.md:212-213`)
```
sudo docker --version
```
- **Expected:** `Docker version 20.10.24+dfsg1, build …` on Debian 12, or `Docker version 26.1.5+dfsg1, …` on Debian 13. The version depends on the Debian release of your VM image (see the package candidates above).

**Step 15. Pull and run the image** (`README.md:214-215`)
```
sudo docker run --rm -ti dlops/simple-translate
```
- **Under the hood:** the image is not local, so Docker prints `Unable to find image 'dlops/simple-translate:latest' locally`, pulls the 7 layers (~146 MB compressed), then starts `/bin/bash -c "source .venv/bin/activate && exec bash"`.
- `sudo` is needed because your user is not in the `docker` group. Note this is the **instructor's** image; to deploy *yours*, run `sudo docker run --rm -ti <USER NAME>/simple-translate-ac215` (requires Step 11b if you built on Apple Silicon).
- **Checkpoint:** a `root@<id>:/#` prompt.

**Step 16. Run the CLI** (`README.md:217-218`)
```
python cli.py
```
- **Observed** (the published image, run in the sandbox on 2026-10-13): the banner, `Arguments: Namespace(text='I love cheese', file='', src='en', dest='it')`, `Input: I love cheese` and `Output: Adoro il formaggio`. The defaults are `cli.py:49` (`"I love cheese"`), `cli.py:62` (`"en"`) and `cli.py:68` (`"it"`). The image's older `cli.py` has the same defaults.
- **Caveat:** the published `dlops/simple-translate` image contains an *older* `cli.py`: 1266 bytes, the `e3bd74e` version (the image's `.git` HEAD is `2827e2a`), with `Translator()` and the default `raise_exception=False`.
  - If Google answers with a non-200 status (for example, it rate-limits the VM's IP), the app prints `Output: I love cheese` **untranslated, with no error**: googletrans returns its dummy data containing your input (`googletrans/client.py:136-144` in the 4.0.2 wheel).
  - A connection failure still raises an exception. See G15.

**Step 17. Leave and clean up** (`README.md:220`)
- `exit` the container, then **delete the VM**: console → VM instances → select → Delete, or `gcloud compute instances delete simple-translate-vm --zone=us-central1-a`.
- **Checkpoint:** the instance list is empty and *Disks* shows no leftover boot disk.

---

## 5. Code tour

```
simple-translate/            (main @ 62f821b)
├── README.md               tutorial; L02 = lines 106-191 (containers) and 203-220 (VM + Docker)
├── Dockerfile.txt          solution Dockerfile (mode 100755); copy to "Dockerfile" (which is git-ignored)
├── docker-shell.sh         dev helper: docker build + docker run --rm --name … -ti  (executable)
├── docker-build-push.sh    buildx multi-arch (amd64+arm64) build & push to dlops/…  (NOT executable)
├── cli.py                  the app: argparse → async googletrans call → print
├── pyproject.toml          uv project "app": art, googletrans==4.0.2; requires-python >=3.13
├── .gitignore              ignores .DS_Store, Dockerfile, /.idea/
└── .vscode/settings.json   Black formatter (irrelevant to Docker)
(no uv.lock, no .dockerignore, no .python-version)
```

**Excerpt 1: base image and environment.** `Dockerfile.txt:1-11`
```
# Use the official Debian-hosted Python image
FROM python:3.12-slim-bookworm

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Python wants UTF-8 locale
ENV LANG=C.UTF-8

# Tell Python to disable buffering so we don't lose any logs.
ENV PYTHONUNBUFFERED=1
```
- `FROM` (line 2): a multi-arch official image (Debian 12 "bookworm", slim variant, CPython 3.12). Docker picks the variant matching the build platform.
- `DEBIAN_FRONTEND` (line 5) stops apt/debconf from waiting for keyboard input during the build. Because it is `ENV`, not `ARG`, it also persists into running containers.
- `LANG` (line 8) is already set by the base image (its config `Env` contains `LANG=C.UTF-8`), so this line is redundant but harmless.
- `PYTHONUNBUFFERED` (line 11) makes `print` output appear immediately, which matters later for `docker logs`.

**Excerpt 2: OS update, uv, code, venv.** `Dockerfile.txt:13-24`
```
# Ensure we have an up to date baseline, install dependencies and
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    pip install --no-cache-dir --upgrade pip && \
    pip install uv

# Copy the source code
COPY . ./

RUN uv sync
```
- One `RUN` = one layer. `set -ex` stops the build on the first error and echoes each command into the build log.
- `apt-get upgrade -y` patches OS packages. `apt-get clean` empties the `.deb` cache but **not** `/var/lib/apt/lists`: ~19 MB stay in both the published and a fresh image (*observed*). L03's Dockerfile adds `rm -rf /var/lib/apt/lists/*`.
- The second `pip install uv` lacks `--no-cache-dir`, which leaves ~18-20 MB of pip cache in `/root/.cache/pip`. The `uv` binary itself is ~49.5 MB (*observed*).
- `COPY . ./` (line 22) copies the whole build context into `/` (no `WORKDIR`).
- `RUN uv sync` (line 24) creates `/.venv` and `/uv.lock`, and, because of `pyproject.toml:6`, downloads a standalone CPython ≥3.13 (Concept 8).
- Order matters: any file change re-runs line 24 (Concept 3).

**Excerpt 3: start-up command.** `Dockerfile.txt:26-29`
```
# Entry point
ENTRYPOINT ["/bin/bash"]
# Get into the uv virtual environment shell
CMD ["-c", "source .venv/bin/activate && exec bash"]
```
- Both use exec (JSON) form, so Docker runs the argv directly without wrapping it in `/bin/sh -c`.
- The combined command is `/bin/bash -c "source .venv/bin/activate && exec bash"`. `source` is a bash builtin that Debian's `/bin/sh` (dash) lacks (*observed*: `/bin/sh: 1: source: not found`; dash only has `.`), so the command must run under bash.
- `.venv` is relative to the working directory `/`.
- `exec bash` replaces the `-c` shell, so the interactive shell becomes PID 1 (*observed*: `echo $$` prints `1`) and `exit` ends the container.

**Excerpt 4: the project definition.** `pyproject.toml:1-10`
```
[project]
name = "app"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "art>=6.5",
    "googletrans==4.0.2",
]
```
- `name = "app"` (line 2) becomes the venv prompt name (`prompt = app` in the image's `pyvenv.cfg`).
- `requires-python` (line 6) conflicts with the 3.12 base image and triggers the CPython download.
- Dependencies (lines 7-10): `art` is a floor only (`>=6.5`); `googletrans` is pinned. googletrans pulls in `httpx[http2]>=0.27.2`.
- No `[build-system]` table, so uv treats this as a non-package project and installs only its dependencies.

**Excerpt 5: the app's main flow.** `cli.py:12-23`
```
async def main(args):
    print("\n")
    print(text2art("AC215"))
    print("\nArguments:", args)

    text = args.text

    if args.file:
        with open(args.file, encoding="utf-8") as file:
            text = file.read()

    print("\nInput:", text)
```
- `main` is `async` because googletrans 4.x exposes an async API.
- `text2art` prints the banner, which is a quick visual proof that `art` imported, i.e. that the venv is active.
- `-f/--file` (lines 19-21) reads a file **inside the container's filesystem**. A file on your laptop is invisible unless you copy it into the image or mount it (L03's `-v`).

**Excerpt 6: the network call.** `cli.py:25-39`
```
    async with Translator(raise_exception=True) as translator:
        try:
            result = await translator.translate(
                text,
                src=args.src,
                dest=args.dest,
            )
        except Exception as error:
            raise RuntimeError(
                "Translation request to Google Translate failed "
                "(the server's network/IP may be rate-limited or blocked "
                "by Google's unofficial translate endpoint)."
            ) from error

    print("Output:", result.text)
```
- `async with` closes the underlying httpx client on exit.
- `raise_exception=True` (added in `62f821b` on 2026-09-08, the day of L02) turns a non-200 reply into an exception. Without it, a non-200 reply makes googletrans silently return your input text as the "translation" (`googletrans/client.py:136-144`).
- The `RuntimeError` message tells you it is a network/IP problem, not a Docker problem.

**Excerpt 7: CLI defaults and entry.** `cli.py:59-72`
```
    parser.add_argument(
        "-s",
        "--src",
        default="en",
        help="Source language",
    )
    parser.add_argument(
        "-d",
        "--dest",
        default="it",
        help="Destination language",
    )

    asyncio.run(main(parser.parse_args()))
```
- The source language defaults to English and the destination to Italian. Codes come from the table at `README.md:225-288`.
- `asyncio.run` starts the event loop that runs `main`.

**Excerpt 8: the local dev helper.** `docker-shell.sh:6-15`
```
# Define some environment variables
export IMAGE_NAME="simple-translate"
export BASE_DIR=$(pwd)

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .
#docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti $IMAGE_NAME
```
- Build (line 11), then run (line 15): the same as `README.md:174` + `README.md:180`, plus `--name`.
- Line 12 is the commented-out **amd64** build for Apple Silicon users. Compare `origin/pipenv:docker-shell.sh`, where this line was the *active* one.
- `BASE_DIR` (line 8) is unused here; it is a leftover of the course's script template, which uses it for `-v` mounts later.

**Excerpt 9: the multi-arch publisher.** `docker-build-push.sh:15-27`
```
# Check if multi-arch builder exists and remove it if it does
if docker buildx inspect multi-arch >/dev/null 2>&1; then
    echo "Removing existing multi-arch builder..."
    docker buildx rm multi-arch
fi

# Setup multi architecture build
echo "Creating new multi-arch builder..."
docker buildx create --driver-opt network=host --use --name multi-arch

# Push
echo "Pushing multi-arch image to registry..."
docker buildx build --platform linux/amd64,linux/arm64 --push -t $DOCKER_USERNAME/$IMAGE_NAME -f Dockerfile .
```
- Lines 16-19 make the script re-runnable by deleting any old `multi-arch` builder.
- Line 23 creates a builder that runs BuildKit in its own container (the `docker-container` driver, started on first use), which can build several platforms at once. `--driver-opt network=host` gives that container the host's network. `--use` makes it the **current** builder for later commands, including plain `docker build` (G2).
- Line 27 builds amd64 and arm64 (one natively, one emulated) and `--push`es one tag that points at an index of both. The result is *not* loaded into your local image list.
- `DOCKER_USERNAME="dlops"` (line 11) must be changed to your username.

**Excerpt 10: why your Dockerfile does not show up in git.** `.gitignore:1-4`
```
# misc
.DS_Store
Dockerfile
/.idea/
```
- Line 3 hides the `Dockerfile` you write, presumably so students' attempts never collide with the repo. As a side effect, `git status` will not show it and it will not be committed to your own GitHub unless you `git add -f Dockerfile`.

**Excerpt 11: the push recipe.** `README.md:186-191`
```
### 📤 Pushing Docker Image to Docker Hub

* Sign up in Docker Hub and create an [Access Token](https://hub.docker.com/settings/security)
* Login to the Hub: `docker login -u <USER NAME> -p <ACCESS TOKEN>`
* Tag the Docker Image: `docker tag simple-translate <USER NAME>/simple-translate-ac215`
* Push to Docker Hub: `docker push <USER NAME>/simple-translate-ac215`
```
- Tag = rename-by-pointer.
- Push = upload missing layers + manifest.
- Nothing here sets a platform, so what you push is whatever your laptop built.

---

## 6. Gotchas and common errors

| # | Symptom | Cause | Fix |
|---|---|---|---|
| G1 | On the GCP VM, `docker run <you>/simple-translate-ac215` fails with `no matching manifest for linux/amd64 in the manifest list entries`, or pulls with `WARNING: The requested image's platform (linux/arm64/v8) does not match the detected host platform …` and then dies with `exec /bin/bash: exec format error` (*expected*; not run here) | A plain `docker build` (`README.md:174`) on an Apple Silicon Mac makes an **arm64** image; default GCP VMs are **amd64**. The README never mentions `--platform`. The first message appears when your push is an index (containerd image store: image + attestation), the second when it is a single manifest (classic store). | Build with `--platform=linux/amd64` (`docker-shell.sh:12`), or push multi-arch with `docker-build-push.sh:27`, or create an Arm (T2A/C4A) VM. Verify with `docker buildx imagetools inspect <image>`. |
| G2 | After running `docker-build-push.sh`, a normal `docker build -t simple-translate …` prints `WARNING: No output specified with docker-container driver. Build result will only remain in the build cache. To push result image into registry use --push or to load image into docker use --load` (*observed* with a `docker-container` builder), and `docker run simple-translate` runs an **old** image (or none) | `docker buildx create … --use` (`docker-build-push.sh:23`) switched your current builder to a `docker-container` builder whose results are not loaded into the local image store (*observed*: nothing new in `docker image ls`) | `docker buildx use default` (Docker Desktop: usually `desktop-linux`; check `docker buildx ls`), or add `--load` |
| G3 | `docker-build-push.sh` fails at the push with an authorization error (*expected* wording along the lines of `push access denied, repository does not exist or may require authorization … insufficient_scope`) | `DOCKER_USERNAME="dlops"` is hard-coded (`docker-build-push.sh:11`). You cannot push to the instructor's namespace. | Set it to your Docker Hub username, and log in first |
| G4 | `./docker-build-push.sh` → `permission denied` | The file is mode 100644, not executable (`git ls-files -s`); `docker-shell.sh` is 100755 | `bash docker-build-push.sh` or `chmod +x docker-build-push.sh` |
| G5 | `docker build … -f Dockerfile .` or `sh docker-shell.sh` → `ERROR: failed to build: failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory` (*observed*, Docker 29; older versions print it without `failed to build:`) | The repo ships only `Dockerfile.txt`; you are expected to write `Dockerfile` (`README.md:128`). Or you ran the command outside the repo folder. | `cp Dockerfile.txt Dockerfile` or write it; `cd` into `simple-translate` (`README.md:172`) |
| G6 | Your `Dockerfile` is missing from `git status` / your GitHub fork | `.gitignore:3` ignores `Dockerfile` | `git add -f Dockerfile`, or remove that line in your own copy |
| G7 | Inside the container `python --version` says 3.15.0 (fresh build, 2026-10-13) or 3.14.7 (instructor's image) although the README says 3.12. The build log shows `Downloading cpython-…`, and the `uv sync` layer is ~100 MB bigger than the venv alone. | `pyproject.toml:6` (`>=3.13`) vs `Dockerfile.txt:2` (3.12): uv downloads a standalone Python (Concept 8; *observed* in both images) | Align them: `FROM python:3.13-slim-bookworm`, or `requires-python = ">=3.12"`. Optionally set `ENV UV_PYTHON_DOWNLOADS=never` so a mismatch fails loudly (*observed*: `error: No interpreter found for Python >=3.13 in managed installations or search path`). |
| G8 | Two builds a week apart contain different package/Python/uv versions | No `uv.lock` in the repo (`git log --all -- uv.lock` is empty); `art>=6.5` and all transitive dependencies float; `pip install uv` is unpinned. *Observed:* the published image (2026-09-16) has uv 0.12.15 + CPython 3.14.7; a fresh build on 2026-10-13 got uv 0.13.0 + CPython 3.15.0 and `idna` 3.20 instead of 3.19. | Commit a `uv.lock` (`uv lock` locally) and use `uv sync --frozen`; pin uv (`pip install uv==<version>`) |
| G9 | Editing `cli.py` (or even `README.md`) makes every rebuild re-run `uv sync` and re-download Python | `COPY . ./` precedes `RUN uv sync` (`Dockerfile.txt:22-24`) | Copy `pyproject.toml` (and `uv.lock`) first, `RUN uv sync`, then `COPY` the code (sketch tested in Exercise E2) |
| G10 | Big image; your `.git` (with your commit history, names and e-mails), a laptop `.venv`, or (in later tutorials) `secrets/` end up inside a **public** Docker Hub image | No `.dockerignore`; `COPY . ./` copies the whole context. The published image contains `.git/` including an editor index under `.git/cursor/`. A copied laptop `.venv` is replaced by `uv sync` with `warning: Ignoring existing virtual environment linked to non-existent Python interpreter` (*observed* with a macOS-style `.venv`), so it only wastes time. | Add a `.dockerignore` with `.git`, `.venv`, `secrets/`, `__pycache__`, `.DS_Store` |
| G11 | `docker run --rm -ti simple-translate python cli.py` → `/usr/local/bin/python: /usr/local/bin/python: cannot execute binary file`, exit 126 (*observed*) | Arguments after the image name replace **CMD**; the command becomes `/bin/bash python cli.py` (`Dockerfile.txt:27,29`). Bash looks for a *script* called `python`, finds the binary on `PATH` and refuses to read it (Concept 4). | `docker run --rm simple-translate -c "source .venv/bin/activate && python cli.py -t 'Good morning' -s en -d es"`, or `docker run --rm --entrypoint /.venv/bin/python simple-translate cli.py -d fr` |
| G12 | `sh docker-shell.sh` → `docker: Error response from daemon: Conflict. The container name "/simple-translate" is already in use by container "<id>". You have to remove (or rename) that container to be able to reuse that name.` (*observed* form) | `--name $IMAGE_NAME` (`docker-shell.sh:15`) while another container (e.g. in a second terminal) still has that name | `docker ps -a`, then exit the other one or `docker rm -f simple-translate` |
| G13 | `WARNING! Using --password via the CLI is insecure. Use --password-stdin.` (*observed*) | `README.md:189` passes the token with `-p`; it lands in your shell history | `docker login -u <USER NAME>` and paste the token at the prompt, or `echo "$TOKEN" \| docker login -u <USER NAME> --password-stdin` |
| G14 | On the VM: `permission denied while trying to connect to the Docker daemon socket` | Your VM user is not in the `docker` group | Use `sudo` as the README does (`README.md:213,215`), or `sudo usermod -aG docker $USER` and reconnect |
| G15 | `Output:` equals `Input:` on the VM (no translation, no error), or `RuntimeError: Translation request to Google Translate failed …` | The request to Google's unofficial endpoint failed. The published `dlops/simple-translate` has the old `cli.py` with `raise_exception=False`, so on a non-200 reply (rate-limit, block) googletrans returns your text as dummy data (`googletrans/client.py:136-144`). The repo's `cli.py:25-37` raises instead. | Not a Docker bug: retry later or from another network. Build from the current repo to get the explicit error. |
| G16 | `E: Unable to locate package docker.io` (empty lists) or `404 Not Found` fetch errors (stale lists) on a fresh VM | `README.md:210` skips `apt-get update` | `sudo apt-get update && sudo apt install docker.io` |
| G17 | `docker system prune` did not free much space | Without `-a` it removes only *dangling* images and unused cache (`README.md:113,117`) | `docker system prune -a` (removes all unused images; they re-download next time) |
| G18 | You edit `cli.py` on the laptop and the running container does not see it | The code was **copied** into the image at build time; there is no bind mount | Rebuild, or wait for L03's `-v "$(pwd):/app"` pattern |
| G19 | `Cannot connect to the Docker daemon at unix:///…/docker.sock` on the laptop | Docker Desktop is not running | Start it (`README.md:110-111`) |
| G20 | You get charged after the lab | The VM, or its boot disk if you only stopped it, is still alive | Delete the VM (`README.md:220`) and check *Disks* |
| G21 | Every "Build + Run after each step" (`README.md:130`) from Step 4 on re-runs `uv sync` and re-downloads Python, even when you only appended a line | Your `Dockerfile` is inside the build context, so `COPY . ./` copies it; any edit to it changes the copy's checksum and invalidates `COPY` and everything after it (*observed*: adding only the Step 5 `CMD` line re-ran `COPY . ./` and `RUN uv sync`) | Expected while you learn. In real projects, a `.dockerignore` listing `Dockerfile` (it is still used for the build) plus the G9 order avoids it |
| G22 | You see a prompt but typing does nothing, and Ctrl-C only prints a new prompt | `docker run -t` without `-i`: a terminal but no attached stdin (*observed*: the container stays `Up`) | Use `-ti` as the README does; stop the stuck one with `docker stop <id>` from another terminal |

---

## 7. Where this sits in the course

**Before: L01, Virtual Environments and Virtual Machines** (`tutorials_demo.md:16-27`). It used the *same repo* (Steps 1 and 2, `README.md:38-101`):
- Manual install with `sudo pip3 install --break-system-packages …` on a VM.
- Then `uv sync` + `source .venv/bin/activate` on a VM.
- You learned venvs, `pyproject.toml` and VMs. The pain point: every new VM needs `apt`, `git clone`, `uv` and `uv sync` again, and works only if the OS cooperates.

**This lecture adds:**
- an **image** that contains the OS userland, Python, the venv and the code;
- a **registry** to ship it;
- a **one-command deploy** on a VM that has only Docker.

Files newly in play in L02: `Dockerfile.txt` (→ your `Dockerfile`), `docker-shell.sh` and `docker-build-push.sh`. `cli.py` and `pyproject.toml` are reused unchanged.

**Repo history relevant to L02:**
```
62f821b 2026-09-08  cli.py: raise_exception=True + RuntimeError wrapper; .gitignore: add /.idea/
2827e2a 2026-09-02  pyproject.toml: requires-python ">=3.12,<3.13" -> ">=3.13"; googletrans 4.0.0rc1 -> 4.0.2
476aec1 2026-09-02  README: googletrans==4.0.2 in step 1, reworded PEP 668 tip
e3bd74e 2026-09-02  cli.py rewritten async (googletrans 4.x API); README sudo pip3
5a6849d 2026-08-28  initial uv-based version
```
`git diff --stat main origin/pipenv` (the older Pipenv variant, for orientation):
```
 .gitignore           |   2 -
 Dockerfile           |  26 +++++++
 Dockerfile.txt       |  29 --------
 Pipfile              |  13 ++++
 Pipfile.lock         | 128 +++++++++++++++++++++++++++++++++++
 README.md            | 186 +++++++++++++--------------------------------------
 cli.py               |  81 ++++++++--------------
 docker-build-push.sh |  29 --------
 docker-shell.sh      |   4 +-
 pyproject.toml       |  10 ---
 tip.txt              |   4 ++
 11 files changed, 247 insertions(+), 265 deletions(-)
```
Meaningful differences in the pipenv variant:
- `FROM python:3.11-slim-buster`, `ADD . /`, `RUN pipenv sync`, `CMD ["-c", "pipenv shell"]`.
- `docker-shell.sh` builds with `--platform=linux/amd64` *active*.
- A committed lock file (`Pipfile.lock`), which main lacks.

**Next: L03, Containers II (mega-pipeline)** (`tutorials_demo.md:46-52`). Same Dockerfile skeleton, grown up (per `mega-pipeline/transcribe_audio/README.md:36-102`):

| simple-translate (L02) | mega-pipeline component (L03) |
|---|---|
| no `WORKDIR` → app in `/` | `WORKDIR /app` (line 77) |
| runs as root | non-root `USER app`, `COPY --chown=app:app` (lines 76, 82) |
| venv in `/.venv` | `ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv` (line 54) |
| no credentials | `ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json` (line 55) plus a service-account key |
| code baked in; rebuild to change | bind mount `docker run --rm -ti -v "$(pwd):/app" transcribe_audio` (line 99) |
| apt lists left in the image (Errata E11) | `rm -rf /var/lib/apt/lists/*` in the same `RUN` (line 64) |
| one container | five containers communicating through a GCS bucket |

**L04** adds the flexible workflow and `docker compose` with ports and networks (`port_toy`). The **multi-arch push** pattern from `docker-build-push.sh` returns almost verbatim in later lectures, e.g. `ml-workflow/src/data-collector/docker-shell-push.sh:25-33` and `cheese-app-v4/src/data-collector/docker-shell-push.sh:25-33`. `ml-workflow/README.md:137` has an explicit "If you are on M1/2 Macs" `--platform=linux/amd64/v2` line. Mastering Concepts 3, 4 and 7 now pays off all semester.

---

## 8. Video plan (suggestion)

**Hook question:** *"A container is supposed to run the same everywhere. So why can an image built on your Mac refuse to start on a Google VM, and why is the 'Python 3.12' image actually running Python 3.15?"*

**Target length:** 25–35 minutes, per the series rules. That is ~3,900–4,300 narrated words at the house voice's ~174 wpm (about 23–25 minutes), plus typing, output and ponder pauses. The terminal is on screen roughly half the time. The chapter times below are rough.

**Chapters**

1. **"Same code, different machine"** (0:00-2:00)
   - **Idea:** L01's VM + uv still depends on the host. Containers ship the environment itself.
   - **Visual:** three machines (Mac, VM, friend's laptop), each with a different Python version bubble. The app box only fits one. Then a shipping container swallows app + Python + OS userland and fits on all three.
   - **On screen:** `README.md:9-16` (the four-step ladder).

2. **Four nouns: image, layer, container, registry** (2:00-5:00)
   - **Idea:** an image is a frozen stack of layers; a container is a live instance with a writable top; a registry is a shelf of stacks; a tag is a sticky note.
   - **Visual:** the slab-stack animation (C1). Layer sizes from the published image's `docker history` appear as slab heights: ~141 MB base, then 111, 0.5 and 127 MB.
   - **On screen:** `docker container ls`, `docker system prune`, `docker image ls` (`README.md:115-118`).

3. **Writing the Dockerfile in five moves** (5:00-9:30)
   - **Idea:** each instruction adds a layer or edits the config; build + run after each step to *see* what changed.
   - **Visual:** the Dockerfile on the left grows line by line; the matching slab drops on the right. A terminal shows the result: REPL `>>>` → bash `root@…:/#` → `ls /` reveals `cli.py` → `ModuleNotFoundError: No module named 'art'` → working venv.
   - **On screen:** `README.md:132-165`, `docker build -t simple-translate -f Dockerfile .`, `docker run --rm -ti simple-translate`.
   - **Pause-and-ponder #1 (after adding only `ENTRYPOINT ["/bin/bash"]`):** "The base image's default command was `python3`. Will the container now run `/bin/bash python3`?" Answer: no. Setting ENTRYPOINT resets the inherited CMD, so you get a plain bash prompt.

4. **ENTRYPOINT + CMD: one sentence, two halves** (9:30-12:00)
   - **Idea:** the container's command line is ENTRYPOINT ++ CMD; `docker run` arguments replace CMD.
   - **Visual:** the puzzle-tile animation (C4), then the failure `/bin/bash python cli.py` lights up red.
   - **On screen:** `Dockerfile.txt:26-29`; demo `docker run --rm simple-translate -c "source .venv/bin/activate && python cli.py -d fr"`.

5. **Who provides Python?** (12:00-14:30)
   - **Idea:** `requires-python` beats `FROM`; uv downloads its own interpreter.
   - **Visual:** the 3.12 slab greys out; a ~100 MB 3.15 slab descends (C8).
   - **On screen:** `pyproject.toml:6`, `Dockerfile.txt:2`, a `--progress=plain` build log, and in the container `python --version`, `which python`, `ls /root/.local/share/uv/python`.
   - **Pause-and-ponder #2 (before running `python --version`):** "The FROM line says 3.12 and pyproject says >=3.13. What will print?" Answer: 3.15.0 at the time of recording (the newest CPython that uv 0.13.0 knew; the instructor's image has 3.14.7). The 3.12 is only used to install uv.

6. **Cache and context** (14:30-17:00)
   - **Idea:** a change re-runs its step and everything after it; the context is everything in `.`.
   - **Visual:** the domino/fingerprint chain (C3). Then a "context" box being shipped to the builder, with `.git/` and `.venv/` sneaking in; a `.dockerignore` sieve filters them out.
   - **On screen:** edit the default `-t` text at `cli.py:49`, rebuild with `--progress=plain`, and point at `CACHED` vs re-run lines. Then the reordered Dockerfile from Exercise E2 (marked "improvement, not course solution"). Also show that the README's own "Build + Run after each step" re-runs `uv sync` once the `Dockerfile` changes (G21).

7. **`docker run` flags and the container lifecycle** (17:00-19:00)
   - **Idea:** `-i` (stdin), `-t` (terminal), `--rm` (auto-delete), `--name`; PID 1 lives, so the container lives.
   - **Visual:** a pipe icon for `-i`, a monitor icon for `-t`, a trash can for `--rm`. `exit` makes the writable slab dissolve.
   - **On screen:** `docker run --rm -ti simple-translate`; `python cli.py -t "Good morning" -s "en" -d "es"`; `exit`; `docker ps -a` with and without `--rm` (extra); `sh docker-shell.sh` (extra, not in the README).

8. **Naming and shipping: tag and push** (19:00-21:00)
   - **Idea:** a tag is a pointer; pushing uploads only missing, content-addressed layers.
   - **Visual:** two sticky notes (`simple-translate`, `<you>/simple-translate-ac215`) point at one image ID. Slabs fly to Docker Hub; the four base slabs "teleport" ("Mounted from library/python") while your three upload.
   - **On screen:** `README.md:188-191`, with `docker login -u <USER NAME>` (interactive) instead of `-p`.

9. **Platforms: why your Mac image breaks on the VM** (21:00-24:00)
   - **Idea:** binaries are CPU-specific; a tag can point to a menu (index) of platforms; buildx cooks for both.
   - **Visual:** the chip/alphabet animation, then the buildx two-lane fork and the index card (C7).
   - **On screen:** `uname -m`, `docker image inspect simple-translate --format '{{.Os}}/{{.Architecture}}'`, `docker-shell.sh:12`, `docker-build-push.sh:11-27`, `docker buildx imagetools inspect <you>/simple-translate-ac215`, `docker buildx use default`.
   - **Pause-and-ponder #3 (before deploying):** "You built on an M-series Mac and pushed. The VM is e2-small. Will `sudo docker run <you>/simple-translate-ac215` work?" Answer: no (arm64 vs amd64). Also: "Why does `dlops/simple-translate` work there?" Because it was published as linux/amd64.

10. **Deploy on the VM, then delete it** (24:00-26:00)
    - **Idea:** a VM with only Docker becomes a deploy target in three commands; always clean up.
    - **Visual:** a cloud VM box gets a Docker whale, a stack drops in from Docker Hub, and the translation flies out to `translate.googleapis.com`. Then the VM fades with a "$" icon crossed out.
    - **On screen:** `sudo apt-get update` (extra, not in this README section), `sudo apt install docker.io`, `sudo docker --version`, `sudo docker run --rm -ti dlops/simple-translate`, `python cli.py`, then Delete VM (`README.md:207-220`). Mention the silent-untranslated-output caveat (G15).

**Recap questions** (end card)
1. What is the difference between `docker build` and `docker run`, and which one creates a layer?
2. In `Dockerfile.txt`, why does changing `README.md` cause `uv sync` to re-run, and how would you prevent it?
3. What exact command does the container run at start-up, and what happens to it if you type `docker run … simple-translate ls`?
4. Why does `python --version` inside the container not print 3.12?
5. Name two ways to make an image built on Apple Silicon run on a default GCP VM.
6. Which GCP resources keep billing after you `exit` the container, and how do you stop them?

---

## 9. Exercises

**E1. Predict the Python (hands-on).**
- Build the solution image. Before running anything, predict the output of `python --version` and `/usr/local/bin/python --version` inside the container. Then add `ENV UV_PYTHON_DOWNLOADS=never` right after the `FROM` line, rebuild, and predict what happens.
- *Answer:*
  - `python` resolves to `/.venv/bin/python`, a uv-managed CPython ≥3.13: `Python 3.15.0` in a fresh build on 2026-10-13 (*observed*), 3.14.7 in the published image. `/usr/local/bin/python` is the base image's 3.12.x (`Python 3.12.15`, *observed*).
  - With downloads disabled, `RUN uv sync` *fails*, because uv cannot find an interpreter satisfying `>=3.13` (`pyproject.toml:6`) on a 3.12 image. *Observed* message: `error: No interpreter found for Python >=3.13 in managed installations or search path`, followed by `hint: A managed Python download is available for Python >=3.13, but Python downloads are set to 'never'`.
  - Fix with `FROM python:3.13-slim-bookworm`, or `requires-python = ">=3.12"` in pyproject. The image then shrinks by roughly 100 MB because the download disappears.

**E2. Cache detective (hands-on).**
- Build with `docker build --progress=plain -t simple-translate -f Dockerfile .` twice in a row, then change the default text in `cli.py:49` to `"I love brie"` and build again. Which steps say `CACHED` each time?
- *Answer:*
  - The second build caches everything.
  - After the edit, `FROM`, the three `ENV`s and the apt/pip `RUN` (`Dockerfile.txt:14-19`) are cached. `COPY . ./` (line 22) and `RUN uv sync` (line 24) re-run, including the CPython download, because the COPY checksum changed and every later step depends on it.
  - Improvement (*tested* on 2026-10-13: after editing `cli.py`, only the last `COPY` re-ran and everything above it was `CACHED`; add a `uv.lock` before you switch to `uv sync --frozen`):
```
WORKDIR /app
COPY pyproject.toml README.md ./
RUN uv sync
COPY cli.py ./
```
  - Now editing `cli.py` re-runs only the last `COPY`. Keep the README's `ENTRYPOINT`/`CMD`: `CMD`'s relative `.venv` path then resolves to `/app/.venv`, which is correct because `WORKDIR` is `/app` (*observed*: `which python` → `/app/.venv/bin/python`).

**E3. "My command is ignored" (debugging).**
- `docker run --rm -ti simple-translate python cli.py -d fr` prints `/usr/local/bin/python: /usr/local/bin/python: cannot execute binary file` (*observed*). Why? Give two working one-liners.
- *Answer:*
  - Arguments after the image replace CMD, giving `/bin/bash python cli.py -d fr` (`Dockerfile.txt:27,29`). Bash treats `python` as the name of a shell script. It is not in `/`, so bash finds `/usr/local/bin/python` on `PATH` (the venv is not active) and refuses to read a binary as a script (exit 126).
  - Working versions:
    - (a) `docker run --rm simple-translate -c "source .venv/bin/activate && python cli.py -d fr"`
    - (b) `docker run --rm --entrypoint /.venv/bin/python simple-translate cli.py -d fr`. This works because `--entrypoint` replaces bash (and clears the image's CMD), and the working directory `/` contains `cli.py`.

**E4. The VM refuses your image (debugging).**
- On an e2-small VM, `sudo docker run --rm -ti student/simple-translate-ac215` fails with `no matching manifest for linux/amd64 in the manifest list entries`, yet `sudo docker run --rm -ti dlops/simple-translate` works. The student built on a MacBook Air M2 with `README.md:174` and pushed with `README.md:190-191`. Explain and fix.
- *Answer:*
  - The pushed image only contains `linux/arm64` (an index with one platform plus an attestation, as the containerd image store exports it). The VM is amd64, and Docker can find no amd64 entry under the tag.
  - `dlops/simple-translate:latest` is a single linux/amd64 image (manifest checked 2026-10-13, built 2026-09-16), so it runs.
  - Fix: `docker build -t simple-translate --platform=linux/amd64 -f Dockerfile .` then tag + push. Or set `DOCKER_USERNAME`/`IMAGE_NAME` in `docker-build-push.sh:7,11` and run `bash docker-build-push.sh` for amd64+arm64. Check with `docker buildx imagetools inspect student/simple-translate-ac215`.
  - Then run `docker buildx use default` so local builds load again (G2).

**E5. Where did my file go? (conceptual + hands-on).**
- Inside the container, run `echo "Le fromage est bon" > /note.txt` and `exit`. Run the container again: is `/note.txt` there? Now repeat without `--rm`. How do you get back to that container?
- *Answer:*
  - With `--rm` the container and its writable layer are deleted on exit. The new container starts fresh from the image, so there is no note.
  - Without `--rm`, the old container still exists (stopped): `docker ps -a` shows it as `Exited (0)`. `docker start -ai <container id>` restarts it with the same start-up command and re-attaches, and `cat /note.txt` prints the note (*observed*).
  - The image never changed; only a container's top layer did.

**E6. Translate a file from your laptop (hands-on, previews L03).**
- Create `notes.txt` on the laptop with an English sentence. Why does `python cli.py -f notes.txt -s en -d fr` inside `docker run --rm -ti simple-translate` fail? Make it work without rebuilding.
- *Answer:*
  - The container's filesystem is the image plus a writable layer. Your laptop's `notes.txt` is not in it, unless it was in the folder at build time, in which case you would see the *old* copy at `/notes.txt`. `cli.py:19-21` opens the path inside the container.
  - Mount it: `docker run --rm -ti -v "$(pwd)/notes.txt:/data/notes.txt" simple-translate`, then `python cli.py -f /data/notes.txt -s en -d fr`. L03 generalises this to `-v "$(pwd):/app"`.

**E7. Predict `-i` vs `-t` (conceptual).**
- What happens with (a) `docker run --rm simple-translate`, (b) `docker run --rm -t simple-translate`, (c) `docker run --rm -i simple-translate`?
- *Answer:*
  - (a) No stdin and no TTY: bash reads EOF immediately, exits 0, and the container is gone in under a second with no output (*observed*).
  - (b) A TTY but no stdin: you get a prompt, but your keystrokes are not forwarded. Bash waits forever, Ctrl-C only makes it print a new prompt, and the container stays `Up` until you `docker stop` it from another terminal (*observed*).
  - (c) stdin but no TTY: no prompt or line editing, but typed commands still run in the activated venv (*observed*: `which python` → `/.venv/bin/python`). Ctrl-D (end of input) ends it.
  - `-ti` gives the interactive shell the README expects.

**E8. The silent non-translation (debugging).**
- On the VM, `dlops/simple-translate` prints `Input: I love cheese` and `Output: I love cheese`. On your laptop, your own build of the current repo prints a `RuntimeError: Translation request to Google Translate failed …`. Same app?
- *Answer:*
  - Almost. The published image was built from an older working copy (its `.git` HEAD is `2827e2a`) whose `cli.py` uses `Translator()`, i.e. `raise_exception=False`. The `cli.py` in the image is 1266 bytes, the pre-`62f821b` version.
  - When Google returns a non-200 status, googletrans 4.0.2 returns dummy data containing the original text (`googletrans/client.py:136-144`).
  - The current repo passes `raise_exception=True` and wraps the failure in a clear `RuntimeError` (`cli.py:25-37`).
  - Both mean "the endpoint refused this request", not a Docker problem. (In the sandbox on 2026-10-13 both images translated normally: `Output: Adoro il formaggio`.) Lesson: a tag on Docker Hub can lag the git repo, so pin and inspect what you deploy.

---

## 10. Errata and open questions

**Errata (with evidence)**
- **E1. Python version mismatch.** `README.md:133` and `Dockerfile.txt:2` use the Python 3.12 image, but `pyproject.toml:6` requires `>=3.13`, a change introduced in commit `2827e2a` (old value `">=3.12,<3.13"`).
  - `uv sync` therefore downloads a standalone CPython. The published `dlops/simple-translate` image runs **CPython 3.14.7** from `/root/.local/share/uv/python/cpython-3.14.7-linux-x86_64-gnu/` (98 MiB of files in the 127 MB `uv sync` layer). A fresh build on 2026-10-13 got **CPython 3.15.0** (uv 0.13.0).
  - The README never mentions this.
- **E2. No lock file.** `README.md:12`, `README.md:70` and `README.md:87` describe `uv.lock` pinning exact versions, but the repo has no `uv.lock` and never had one (`git log --all -- uv.lock` is empty). Builds resolve fresh each time; `art>=6.5` and the uv version (`pip install uv`, `Dockerfile.txt:19`) float.
- **E3. Platforms never covered.** The README never mentions CPU platforms or the two helper scripts (`grep -n 'platform\|amd64\|arm64\|docker-shell\|docker-build-push' README.md` finds nothing). The only platform handling is the commented line `docker-shell.sh:12` and the unreferenced `docker-build-push.sh`.
- **E4. Step 4 deploys the wrong image.** `README.md:14` ("Pull what you just pushed") and `README.md:205` ("pull the image you pushed in step 3") promise your own image. But `README.md:215` runs the instructor's `dlops/simple-translate`, not the student's `<USER NAME>/simple-translate-ac215` from `README.md:190-191`. The names also disagree with `docker-build-push.sh:7` (`IMAGE_NAME="simple-translate"`).
- **E5. The published image is not multi-arch and lags the repo.** `docker-build-push.sh` claims to push a multi-arch `dlops/simple-translate`, but `dlops/simple-translate:latest` is a **single linux/amd64 manifest** (created 2026-09-16). It would not run natively on an Arm VM. It also contains the pre-`62f821b` `cli.py` (1266 bytes, no `raise_exception=True`; the image's `.git` HEAD is `2827e2a`), even though it was built eight days after that commit.
- **E6. Broken in-page links.** The README "Contents" links (`README.md:31-34`) use anchors like `#developing-app-using-containers`. GitHub generates `#-developing-app-using-containers` for the emoji heading (the course site itself links that form, `tutorials_demo.md:36`), so the in-page links are likely broken. The same applies to the other three emoji headings.
- **E7. Image vs container terminology.** "copy source code into the container" (`README.md:146`) and "Build the docker container" (`README.md:173`) should both say *image*.
- **E8. Prune wording.** "clear up an unused images" (`README.md:113`): `docker system prune` (`README.md:117`) removes only *dangling* images unless you pass `-a`.
- **E9. Insecure login.** `docker login -u <USER NAME> -p <ACCESS TOKEN>` (`README.md:189`) passes the secret on the command line; Docker itself warns against this.
- **E10. Missing apt update.** `README.md:210` installs `docker.io` without the `sudo apt-get update` used earlier (`README.md:44`, `README.md:74`).
- **E11. Dockerfile hygiene.** In `Dockerfile.txt`:
  - the comment at line 13 is truncated ("install dependencies and");
  - line 17 `apt-get clean` leaves `/var/lib/apt/lists` (~19 MB, *observed*);
  - line 19 `pip install uv` leaves ~18-20 MB of pip cache (*observed*);
  - `uv sync` leaves ~7 MB of uv cache under `/root/.cache/uv` (*observed*);
  - `ENV LANG=C.UTF-8` (line 8) duplicates the base image;
  - there is no `WORKDIR`, so the app lives in `/` (published image: `VIRTUAL_ENV='/.venv'`);
  - there is no `.dockerignore`, so `.git/` and the `Dockerfile` itself are copied (`Dockerfile.txt:22`; see G10, G21).
- **E12. Wrong prompt example (L01 section, low priority).** `README.md:92` suggests the prompt becomes `(simple-translate) $`. uv names the prompt after the project, `app` (`pyproject.toml:2`; the published image's `pyvenv.cfg` has `prompt = app`). Inside the container even that prefix is overwritten by Debian's `/etc/bash.bashrc` `PS1`.
- **E13. Placeholder metadata (cosmetic).** `pyproject.toml:2-4`: `name = "app"`, `description = "Add your description here"`.

**Open questions / could not determine**
- The Ed lesson (`lessons/166028`) and the lecture slides were not accessible (the site links them as `/not-yet/`, `_modules/week-02.md:7`). They may already cover the Apple Silicon `--platform` issue that the README omits.
- Which CPython a fresh build picks depends on the uv version installed at build time: 3.14.7 with uv 0.12.15 (published image, 2026-09-16), 3.15.0 with uv 0.13.0 (my build, 2026-10-13). A student who builds later may get a newer one.
- Whether Google's unofficial translate endpoint currently blocks GCP VM IPs. The 2026-09-08 commit message and the error text in `cli.py:33-37` suggest it happened in class. From the sandbox on 2026-10-13 it translated normally.
- The current Docker Hub token page URL: `README.md:188` links `https://hub.docker.com/settings/security`. Both that and `app.docker.com/settings/personal-access-tokens` redirect to login, so I could not confirm which is current.
- The default GCP VM image (Debian 12 vs 13) decides which `docker.io` version Step 13 installs; the README does not specify an image or machine type.
- Outputs marked *expected* (macOS / Apple Silicon behaviour, `docker login`/`push`, the VM's `docker --version` and pull) were not run here. The exact wording of Docker/BuildKit messages varies between Docker versions and between the classic and containerd image stores. My observations come from Docker Engine 29.8.2 on linux/amd64, not Docker Desktop.
- Whether a GCP Debian image ships with populated or stale apt lists, which decides whether Step 13 works without `apt-get update`.
- The AWS variant (`simple-translate-aws`, `tutorials_demo.md:37,42`) was not examined.
