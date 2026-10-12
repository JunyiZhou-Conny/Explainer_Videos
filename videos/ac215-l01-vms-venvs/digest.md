# L01 · Virtual Environments and Virtual Machines — tutorial digest

- **Ed lesson:** https://edstem.org/us/courses/97373/lessons/166027/ (course site: `tutorials_demo.md:16-27`; lecture date Sep 3 per `_modules/week-01.md:5-7`)
- **Repo used (primary):** `dlops-io/simple-translate`, branch `main`, commit `62f821bfe09fc1c2ecb0f14354b1f205777c0efa`, committed 2026-09-08 13:58:15 -0400 ("Handle translation exceptions with detailed error messages")
- **Repo used (comparison only):** `dlops-io/simple-translate`, branch `pipenv` (a tag named `pipenv` points at the same commit), commit `3a354d81f787a064aea3ab061359c9a1e223e4d5`, committed 2026-08-28 08:13:27 -0400. It is a separate root commit with no history shared with `main` (`git merge-base` finds nothing).
- **README sections this lecture covers** (in `main`'s `README.md`):
  - `## 🛠️ Installing App on VM Manually`: `README.md:38-64`, GitHub anchor `#️-installing-app-on-vm-manually`, which the course site URL-encodes as `#%EF%B8%8F-installing-app-on-vm-manually` (`tutorials_demo.md:21`)
  - `## ⚡ Installing App on VM using UV`: `README.md:68-101`, anchor `#-installing-app-on-vm-using-uv` (`tutorials_demo.md:26`)
  - Context only: `README.md:1-34` (overview, prerequisites, contents). Sections 3-4 (Docker, `README.md:106-220`) belong to L02.
- **Colab notebooks used:** none. The `colab/` folder has no L01 notebook.
- **Not used:** `simple-translate-aws` (the AWS track; it isn't cloned and is out of scope).
- **Context repos cited in §7 only:** `llm-rag` main `e17a39f35bc07b440f573def480adaf4703f8b91` (2026-10-07), `mega-pipeline` main `c6bbc9ba88984e1234b68ccf5cdf7c00f7e9accc` (2026-09-27), `cheese-app-v0` main `cb6fb94576aa37bb0b94a8745e5e94e6a504f4bb` (2026-10-08).
- **How I checked uv's behaviour:** I copied `pyproject.toml` into a sandbox and ran uv 0.11.32 against the copy on 2026-10-12, using `uv lock`/`uv sync --no-build`, `--managed-python`, `--python 3.11/3.12`, `--locked` and `uv python pin`. I executed no repository script, Dockerfile or `cli.py`. The package versions below come from that sandbox, so yours will differ (§3.5 explains why).

---

## 1. What you build

You rent a Linux computer in Google Cloud (a Compute Engine **VM**), SSH into it from the browser, clone a 72-line Python command-line app (`cli.py`), and get it running two ways. **Walkthrough A** is the "quick and dirty" way: you `sudo pip3 install` the two dependencies, `googletrans` and `art`, straight into the operating system's own Python, and you have to pass `--break-system-packages` to get past Debian/Ubuntu's PEP 668 guard. **Walkthrough B** is the clean way: you install `uv`, and `uv sync` reads `pyproject.toml`, finds or downloads a Python ≥ 3.13, creates a project-local **virtual environment** in `.venv/`, resolves the full dependency tree into `uv.lock`, and installs those exact versions into `.venv`. You activate the venv and run the same commands. The app sends your text to Google's *unofficial* translate endpoint over HTTPS and prints an ASCII-art banner, the parsed arguments, the input and the translation. There are no containers, open ports, volumes, service accounts or secrets in this lecture. When you finish you **delete the VM**.

```
 YOUR LAPTOP                                GOOGLE CLOUD  (your project, one zone e.g. us-central1-a)
 +---------------------------+              +---------------------------------------------------------------+
 | Browser                   |  HTTPS       |  Compute Engine VM  (e2-*, Debian/Ubuntu boot disk)           |
 |  console.cloud.google.com |------------->|  vCPU + RAM (billed while RUNNING), boot disk (billed while   |
 |  /compute/instances       |  "SSH" btn   |  it EXISTS), ephemeral external IPv4                          |
 |  [Create] [SSH] [Delete]  |=============>|                                                               |
 +---------------------------+  (tcp/22,    |  /home/<you>/simple-translate/      <- git clone              |
                                 in-browser |     cli.py   pyproject.toml   README.md   Dockerfile.txt ...  |
                                 terminal)  |     uv.lock   (created by uv sync - NOT in the repo)          |
                                            |     .venv/    (created by uv sync)                            |
                                            |                                                               |
                                            |  Walkthrough A (manual)          Walkthrough B (uv)            |
                                            |  $ python3 cli.py ...           (app) $ python cli.py ...     |
                                            |        |                                |                     |
                                            |        v                                v                     |
                                            |  /usr/bin/python3 (OS Python)    .venv/bin/python -> some     |
                                            |  + /usr/local/lib/python3.X/      CPython >= 3.13 (system or  |
                                            |    dist-packages  <- sudo pip3    ~/.local/share/uv/python/)  |
                                            |    (shared with the whole OS)     + .venv/lib/python3.X/      |
                                            |                                     site-packages <- uv sync  |
                                            +-------------------------------+-------------------------------+
                                                                            | outbound HTTPS only; no inbound
                                                                            | ports are opened by this tutorial
      +------------------+------------------+---------------------+---------+---------------+-----------------------------+
      v                  v                  v                     v                         v                             v
 deb.debian.org     github.com         pypi.org +              astral.sh/uv/install.sh   python-build-standalone     translate.googleapis.com
 (apt-get update,   (git clone          files.pythonhosted.org (uv + uvx binaries ->     (managed CPython download,  /translate_a/single?client=gtx
  git, python3-pip)  dlops-io/          (googletrans, art,      ~/.local/bin)             only if no Python >= 3.13   (unofficial, no API key;
                     simple-translate)   httpx, h2, ...)                                  is installed)               may rate-limit cloud IPs)

 Call chain for one translation:
   shell -> python cli.py -t "..." -s en -d es
         -> argparse Namespace -> asyncio.run(main(args))           (cli.py:72, :12)
         -> googletrans.Translator(raise_exception=True)            (cli.py:25)  [httpx.AsyncClient, HTTP/2]
         -> GET https://translate.googleapis.com/translate_a/single (googletrans urls.py:7, constants.py:3)
         <- JSON -> result.text -> print("Output:", ...)            (cli.py:39)
```

---

## 2. Prerequisites and costs

**Accounts**
- A Google Cloud project with **billing enabled**, set up in "Tutorial 0 - Setup & Installs" (`README.md:20-21`, https://github.com/dlops-io/ac215-setup; that repo wasn't available to me).
- No GitHub login is needed because the repo is public and cloned over HTTPS (`README.md:50`).
- No Docker Hub account is needed until L02.

**Local installs**
- For L01 you need only a web browser: everything runs on the VM through the console's in-browser SSH (`README.md:42-43`).
- Optional: the `gcloud` CLI, if you'd rather drive the VM from your terminal (the commands are below; they aren't in the README).

**GCP APIs**
- **Compute Engine API** (`compute.googleapis.com`). The console asks you to enable it the first time you open *VM instances*. From the CLI: `gcloud services enable compute.googleapis.com`. Nothing else is needed.

**Service accounts / keys / secrets / env vars**
- **None.** The README says so: "You don't need GCP credentials (a service account) for this tutorial - that comes in a later one." (`README.md:23`).
- `cli.py` reads no environment variables. `grep -n "os.environ\|getenv" cli.py` finds nothing.
- Console-created VMs get the Compute Engine default service account attached, but this code never uses it.

**Where the code expects things (paths)**

| Thing | Where | Set by |
|---|---|---|
| Repo checkout | `~/simple-translate` (your SSH user's home) | `git clone` + `cd simple-translate` (`README.md:50-51`, `:76-77`) |
| Working directory when you run the app | repo root (you run `python cli.py`; it has no other path assumptions; `-f FILE` is resolved relative to the cwd, `cli.py:19-21`) | you |
| Walkthrough A packages | `/usr/local/lib/python3.X/dist-packages/` (Debian's location for `sudo pip`) | `sudo pip3 install ...` (`README.md:53`) |
| `uv` / `uvx` binaries | `~/.local/bin/` | uv installer (`README.md:78`); `source $HOME/.local/bin/env` puts that directory on `PATH` (`README.md:83`) |
| Project definition | `./pyproject.toml` (`uv sync` searches the current directory and its parents) | repo |
| Lockfile | `./uv.lock`, **written on your VM by the first `uv sync`**; the repo has none | `uv sync` |
| Virtual environment | `./.venv/`, which contains its own `.gitignore` holding `*` so git ignores it | `uv sync` |
| uv-managed Python (only if needed) | `~/.local/share/uv/python/` | `uv sync` (automatic download) |
| uv download cache | `~/.cache/uv/` | uv |

**Billable resources and how to shut them down**
- **VM vCPU/RAM:** billed per second while the VM is *running*, including when it sits idle. Rough on-demand list prices in us-central1, from memory, so check the estimate panel on the console's create page: e2-micro ≈ $0.008/h, e2-small ≈ $0.017/h, e2-medium ≈ $0.034/h. A one-hour lab costs a few cents. e2-micro in us-west1/us-central1/us-east1 falls under GCP's always-free tier (one instance per month, standard persistent disk).
- **Boot disk (persistent disk):** billed per GB-month for as long as the disk *exists*, even while the VM is stopped (the console default is about 10 GB).
- **External IPv4 address:** billed per hour while assigned (around $0.005/h).
- **Network egress:** negligible here (a few MB).
- **Shut-down procedure:** the README says to delete the VM after *each* walkthrough (`README.md:62`, `:98`): "Go to VM instances, select your instance, and click Delete." Leave "Delete boot disk when instance is deleted" ticked (it is by default) or the disk stays behind. Then check:
  - *Compute Engine → VM instances* is empty
  - *Compute Engine → Disks* has no orphaned disk
  - CLI alternatives (not in the README): `gcloud compute instances list` and `gcloud compute instances delete <name> --zone <zone>`
- **Stopping isn't deleting:** a *stopped* VM still pays for its disk (and for a static IP, if you reserved one).
- **Optional `gcloud` equivalents** (my suggestion, not from the README):
  ```bash
  gcloud compute instances create ac215-l01 --zone=us-central1-a --machine-type=e2-small \
      --image-family=debian-12 --image-project=debian-cloud
  gcloud compute ssh ac215-l01 --zone=us-central1-a
  gcloud compute instances delete ac215-l01 --zone=us-central1-a
  ```

---

## 3. Concepts this tutorial teaches

Concepts marked **[ANIMATE]** most deserve a 3Blue1Brown-style animated explanation.

### 3.1 Virtual machine (VM) **[ANIMATE]**
- **Explanation.** A VM is a complete computer made of software:
  - virtual CPUs, RAM, a virtual disk and a network card, carved out of a physical server by a **hypervisor**
  - its own operating system kernel on top (Debian, Ubuntu)
  - in GCP a VM is a *Compute Engine instance*, defined by a **machine type** (vCPU/RAM, e.g. e2-small), a **zone** (where it physically lives), a **boot disk image** (which OS it starts with) and a **network interface** (internal IP, optionally an external IP)

  You get root via `sudo`, and you pay by the second.
- **Mental model.** It's a disposable rented Linux box: it starts empty, you set it up, and you throw it away. Whatever you do inside can't hurt your laptop or anyone else's VM.
- **Analogy.** A hotel room in a big building. The building (physical server) and the front desk (hypervisor) are shared, but your room has its own lock, furniture and bathroom (kernel, disk, OS), and checkout (Delete) wipes it.
- **Common misconception.** "Stopping the VM stops all charges." Stopping only ends the CPU/RAM billing; the disk keeps billing until you delete it.
  A second one is "a VM is basically a container." A VM boots its own kernel; containers (L02) share the host's kernel.
- **Animation idea.** A big physical server box. A thin "hypervisor" slab slides in on top, then the box splits into 3-4 translucent slices, each sprouting its own OS layer ("Debian 12", "Ubuntu 24.04"…). One slice is highlighted as *your* VM; a browser window off to the side draws an SSH beam into it. At the end, a "Delete" stamp makes the slice dissolve and a cost meter stops ticking.

### 3.2 The system Python and PEP 668 ("externally managed")
- **Explanation.**
  - Debian/Ubuntu ship a Python (`/usr/bin/python3`) that **the OS itself** relies on, and `apt` owns its packages in `/usr/lib/python3/dist-packages`.
  - Since PEP 668, the distribution drops a marker file `EXTERNALLY-MANAGED` next to the stdlib, and pip ≥ 23 refuses to install into that interpreter.
  - `--break-system-packages` overrides the refusal.
  - Run with `sudo`, pip writes into `/usr/local/lib/python3.X/dist-packages`, which comes *before* apt's directory on `sys.path`, so a pip-installed `idna` or `certifi` can silently shadow the apt copy that some system tool depends on. `README.md:55-56` explains this.
- **Mental model.** The system Python is a shared kitchen: the OS cooks in it, and if you rearrange the spice rack, the OS's recipes may break.
- **Analogy.** The landlord's fuse box: you *can* rewire it ("break system packages"), but it's not your building.
- **Common misconception.** "`--break-system-packages` only affects this project." It changes the interpreter every user and every system script on the machine shares.

### 3.3 Virtual environment (venv) **[ANIMATE]**
- **Explanation.** A venv is just a directory with these parts:
  1. `bin/python`: a **symlink** to a real interpreter. In the sandbox, `.venv/bin/python -> /usr/bin/python3`, or `-> ~/.local/share/uv/python/cpython-3.14…/bin/python3.14` when uv downloaded one.
  2. Its own empty `lib/python3.X/site-packages/`.
  3. `pyvenv.cfg`, which tells the interpreter "you are a venv; use *my* site-packages", with `include-system-site-packages = false`.

  When Python starts from `.venv/bin/python`, it builds `sys.path` with the venv's site-packages instead of the system one. Packages installed in the venv are invisible to the OS Python, and vice versa.
- **Mental model.** Same engine, different toolbox: the interpreter is shared, the installed packages aren't.
- **Analogy.** A project-specific backpack. You don't empty the household toolbox into it; you pack exactly what this job needs.
- **Common misconception.** "A venv contains its own copy of Python." Usually it's a symlink (verified in the sandbox).
  A second one is "a venv isolates everything." It isolates *Python packages* only: not system libraries (e.g. `libpq`), not the OS, not GPU drivers. That's what containers and VMs are for.
- **Animation idea.** Draw `sys.path` as a vertical list of shelves. For `/usr/bin/python3` the shelves are `/usr/lib/python3.11`, `/usr/local/lib/python3.11/dist-packages`, `/usr/lib/python3/dist-packages`. Then switch to `.venv/bin/python`: the last two shelves slide out and a fresh `.venv/lib/python3.14/site-packages` shelf slides in. `import googletrans` is a little search-light that scans the shelves from top to bottom.

### 3.4 Activation is just `PATH` (and a prompt) **[ANIMATE]**
- **Explanation.** `source .venv/bin/activate` runs a shell script *in your current shell*. It:
  - saves the old `PATH`, then prepends the venv's `bin` (generated `activate:97-99`: `PATH="$VIRTUAL_ENV/bin:$PATH"`)
  - exports `VIRTUAL_ENV`
  - sets `VIRTUAL_ENV_PROMPT` to the venv's prompt name. For this repo that's `app`, taken from `pyproject.toml:2`.
  - prefixes `PS1` so the prompt reads `(app) $`
  - defines `deactivate`

  Nothing else changes. You can skip activation entirely: `.venv/bin/python cli.py` or `uv run python cli.py` give the same result.
- **Mental model.** When you type `python`, the shell walks `PATH` from left to right and runs the first match. Activation puts `.venv/bin` at the front of the line.
- **Analogy.** Changing which drawer you grab a screwdriver from first. The screwdrivers themselves don't move.
- **Common misconception.** "Activation installs or loads packages." It doesn't; it only changes lookup order.
  Another is "`./.venv/bin/activate` works too." The file isn't executable (`-rw-r--r--` in the sandbox), and even run with `bash`, it would modify a *child* shell that exits immediately. That's why the README says `source` (`README.md:92`).
- **Animation idea.** `PATH` as a row of doors: `/usr/local/bin | /usr/bin | /bin`. The word `python` walks along and knocks. On Debian, no door has a `python` (only `python3`), so the result is "command not found". Run `source activate` and a new door `.venv/bin` slides in at the far left, and `python` enters it. `deactivate` slides it back out.

### 3.5 Declared vs resolved dependencies; the lockfile **[ANIMATE]**
- **Explanation.**
  - `pyproject.toml` states **intent**: "I need `art>=6.5` and `googletrans==4.0.2`" (`pyproject.toml:7-10`).
  - Those two direct dependencies drag in **transitive** ones (`httpx[http2]` → `httpcore`, `h2`, `hpack`, `hyperframe`, `anyio`, `idna`, `certifi`, `h11`, `typing-extensions`).
  - The **resolver** picks one concrete version for each and writes the result, with sha256 hashes and download URLs, to **`uv.lock`**.
  - On 2026-10-12, 2 declared dependencies resolved to **13 lock entries**: 12 packages plus the project itself, recorded as `source = { virtual = "." }`.
  - Anyone who runs `uv sync` *with that lockfile* gets byte-identical packages. `uv sync --locked` refuses to proceed if the lock is missing or stale; `--frozen` installs the lock as-is without checking it.
- **Mental model.** `pyproject.toml` is the shopping list ("some milk"); `uv.lock` is the receipt ("Brand X, 1 L, batch #…").
- **Analogy.** A recipe ("a cup of flour") vs a photo of the exact bags used.
- **Common misconception.** "Pinning `googletrans==4.0.2` makes the install reproducible." The *transitive* dependencies (httpx, certifi…) still float; only the lockfile freezes them.
  This repo also **doesn't commit a `uv.lock`** (`git ls-files` has none, `git log --all -- uv.lock` is empty), even though `README.md:70` says it "pins exact versions so the next person gets the same setup". Every student's first `uv sync` creates a fresh lock from whatever is newest on PyPI that day.
- **Animation idea.** Start with two nodes, `art` and `googletrans`. `googletrans` sprouts `httpx[http2]`, which sprouts `anyio`, `certifi`, `httpcore`, `idna`, `h2`, and so on until the tree from `uv tree` (§5) is fully drawn. Then every node gets a version tag that "clicks" into place, and the whole tree compresses into a single scroll labelled `uv.lock`. Show two students: without the scroll, their trees differ in leaf versions; with it, the trees are identical.

### 3.6 Python version: constraint vs pin **[ANIMATE]**
- **Explanation.**
  - `requires-python = ">=3.13"` (`pyproject.toml:6`) is a **constraint**, not a pin.
  - uv first looks for a compatible interpreter it already has: its own managed installs, then the system's.
  - If none is found, it **downloads** a standalone CPython build into `~/.local/share/uv/python/`. In the sandbox, with only managed Pythons allowed, uv 0.11.32 downloaded **CPython 3.14.6**, the newest stable release matching `>=3.13`, not 3.13.
  - A real pin is a `.python-version` file written by `uv python pin 3.X`. This repo has none.
  - Which Python you end up with therefore depends on the VM image:
    - Debian 12 ships 3.11, so uv downloads 3.14.x
    - Ubuntu 24.04 ships 3.12, so uv downloads 3.14.x
    - an image whose `python3` is ≥ 3.13 is used directly
- **Mental model.** A number line of Python versions with a shaded interval `[3.13, ∞)`. uv walks the interpreters it can find and keeps the first one inside the interval. If none qualifies, it fetches the newest stable release in the interval.
- **Analogy.** "Any flight that lands after 13:00." Without a specific booking (the pin), you get whatever the system finds.
- **Common misconception.** "uv uses the Python that came with the VM." Only when it satisfies `requires-python`. Otherwise uv quietly downloads another one, about 34 MB in the sandbox.
  Another is "requires-python is ignored." Force an older interpreter and uv errors out:
  `error: The requested interpreter resolved to Python 3.11.17, which is incompatible with the project's Python requirement: `>=3.13` (from `project.requires-python`)` (sandbox output).
- **Animation idea.** A horizontal number line (3.10 … 3.15) with the interval `>=3.13` glowing. Dots appear for the interpreters found on a Debian 12 VM: `3.11 /usr/bin/python3`, outside the interval, turns red. A download arrow drops a new dot `3.14.x (managed)` into the interval, and `.venv/bin/python` draws a symlink arrow to it.

### 3.7 uv as one tool instead of five (and how pipenv differs)
- **Explanation.** `uv` (Astral, written in Rust) replaces:
  - `python -m venv` (create a venv)
  - `pip` (install)
  - `pip-tools` / `pipenv lock` (resolve and lock)
  - `pyenv` (install Pythons)
  - `pipx` (tools)

  It keeps a global cache (`~/.cache/uv`) and hard-links or copies wheels from it, which is why re-syncs take milliseconds. A **uv venv has no `pip` inside it**: the sandbox `.venv/bin` has `python`, `python3`, `python3.13`, `activate*` and package scripts, but no `pip`. To add packages you use `uv add <pkg>`, which edits `pyproject.toml`, re-locks and syncs, or `uv pip install`.

  The **`pipenv` branch** shows the older way:

  | | uv (`main`) | pipenv (`pipenv` branch) |
  |---|---|---|
  | Project file | `pyproject.toml` | `Pipfile` |
  | Lockfile | `uv.lock` | `Pipfile.lock` (committed, with sha256 hashes) |
  | Python version | `requires-python` (constraint); uv can download Pythons itself | `[requires] python_version = "3.11"` (`origin/pipenv:Pipfile:12-13`); relies on the system or pyenv |
  | Where the venv lives | `.venv` in the project | `~/.local/share/virtualenvs/<name>-<hash>` by default |
  | Getting into it | `source .venv/bin/activate` modifies the current shell | `pipenv shell` spawns a *subshell*; you `exit` to leave |
  | Install command | `uv sync` | `pipenv install` (VM, `origin/pipenv:README.md:30`) or `pipenv sync` (Docker, `origin/pipenv:Dockerfile:20`) |
- **Mental model.** uv is a single fast binary that owns the whole "which Python + which packages" problem.
- **Common misconception.** "`pip install` inside an activated uv venv installs into the venv." `pip` isn't in the venv. You get the system `pip`, which then hits PEP 668, or "command not found" on a VM where `python3-pip` was never installed.

### 3.8 Why both: layers of isolation
- **Explanation.** Each layer isolates one kind of thing:
  - A **VM** isolates *hardware and OS*: a whole machine you can wreck and delete.
  - A **venv** isolates *Python packages* within one OS: two projects on the same VM can need different `httpx` versions.
  - **Containers** (L02) isolate a *filesystem + process tree* that shares the host kernel, and ship the venv along with the OS libraries.

  In this course you'll nest all three: a VM runs Docker, and the container runs a uv venv. `Dockerfile.txt:24` runs `uv sync` *inside* an image.
- **Mental model.** Russian dolls: VM ⊃ (container ⊃) venv.
- **Common misconception.** "If I use a VM I don't need a venv" (or the reverse). They solve different problems. A VM gives you a clean machine, and a venv keeps you from polluting the machine's Python so it stays clean.

---

## 4. Step-by-step walkthrough

Steps follow the README order. Commands in code spans are verbatim from the README unless marked *(extra)*.

### Part 0: before you start

**Step 0. Project, billing, Compute Engine API.**
- **Action:** in the console, pick your AC215 project and open *Compute Engine → VM instances* (https://console.cloud.google.com/compute/instances). Click *Enable* if it asks to enable the Compute Engine API.
- **Under the hood:** this turns on `compute.googleapis.com` for the project; it can take a minute.
- **Checkpoint:** the VM instances page loads with a "Create instance" button.
- **If it fails:** "Billing account required" means you need to link billing (or the course credit) to the project.

### Part A: 🛠️ Installing App on VM Manually (`README.md:38-64`)

**Step 1. Create a VM** (`README.md:42`: "Create a VM Instance from [GCP](https://console.cloud.google.com/compute/instances)").
- **Action:** *Create instance*. The README gives no settings. Sensible choices:
  - a name, e.g. `ac215-l01`
  - region us-central1, any zone
  - machine type e2-small (e2-micro also works)
  - boot disk: the default Debian image
  - **keep an external IPv4** (the default)
- **Under the hood:** GCP allocates a slice of a host, copies the image onto a new persistent disk, boots it, and runs the guest agent, which sets up users and SSH keys.
- **Checkpoint:** a green check next to the instance and an External IP shown.
- **If it fails:**
  - "Quota exceeded": pick another region or a smaller machine type
  - "Compute Engine API has not been used": go back to Step 0

**Step 2. SSH in** (`README.md:43`).
- **Action:** click **SSH** in the instance row.
- **Under the hood:** the browser SSH client pushes a temporary key (via OS Login or instance metadata) and opens a terminal as a Linux user derived from your Google account. Your home is `/home/<you>`.
- **Checkpoint:** a prompt like `<you>@ac215-l01:~$`.
- *(extra, recommended)* Look around: `cat /etc/os-release`, `python3 --version`, `which python` (on Debian this prints nothing: there's no `python` command).
- **If it fails:**
  - "Connection via Cloud Identity-Aware Proxy failed" or a timeout usually means a firewall rule for tcp:22 is missing in a non-default VPC. The default VPC has `default-allow-ssh`.

**Step 3. Update package lists** (`README.md:44`): `sudo apt-get update`
- **Under the hood:** downloads fresh package indexes from the Debian mirrors. Nothing is upgraded yet.
- `README.md:47-48` explains `apt-get` (scriptable) vs `apt` (interactive).
- **Checkpoint:** ends with "Reading package lists... Done".
- **If it fails / hangs:** the VM has no outbound internet. Check that it has an external IP (or Cloud NAT).

**Step 4. Install Git** (`README.md:45`): `sudo apt install git`
- **Checkpoint:** answer `Y` at "Do you want to continue? [Y/n]" (add `-y` to skip the prompt); `git --version` then prints a version. (Some images already have git; apt then says "git is already the newest version".)

**Step 5. Clone and enter the repo** (`README.md:50-51`): `git clone https://github.com/dlops-io/simple-translate.git` then `cd simple-translate`
- **Checkpoint:** `ls` shows `Dockerfile.txt  README.md  cli.py  docker-build-push.sh  docker-shell.sh  pyproject.toml` (`ls -a` also shows `.gitignore .vscode .git`). *(extra)* `git log -1 --oneline` shows `62f821b Handle translation exceptions with detailed error messages`, or a newer commit if the repo has changed since.
- Note: **no `uv.lock`, no `.python-version`, no `requirements.txt`.**

**Step 6. Install pip for the system Python** (`README.md:52`): `sudo apt install python3-pip`
- **Under the hood:** apt installs Debian's pip package (plus `python3-setuptools`, `python3-wheel`, and so on) for `/usr/bin/python3`.
- **Checkpoint:** `pip3 --version` prints something like `pip 23.x from /usr/lib/python3/dist-packages/pip (python 3.11)` on Debian 12.
- *(extra, highly instructive)* Try the install **without** the flag first: `pip3 install googletrans==4.0.2 art`. You should get `error: externally-managed-environment`, followed by the text of `/usr/lib/python3.X/EXTERNALLY-MANAGED`. On Ubuntu 24.04 that text begins: "To install Python packages system-wide, try apt install python3-xyz, where xyz is the package you are trying to install. If you wish to install a non-Debian-packaged Python package, create a virtual environment using python3 -m venv path/to/venv. …" (read from the marker file on an Ubuntu 24.04 system).

**Step 7. Install the app's packages into the OS Python** (`README.md:53`): `sudo pip3 install --break-system-packages googletrans==4.0.2 art`
- **Under the hood:**
  - pip runs as root, skips the PEP 668 check (`README.md:55-56`), and resolves `googletrans==4.0.2` → `httpx[http2]>=0.27.2` plus its tree, and `art` (unpinned here, so the latest).
  - It installs everything into `/usr/local/lib/python3.X/dist-packages`, which every user and every system script on this VM shares.
- **Checkpoint:**
  - "Successfully installed anyio-… art-… certifi-… googletrans-4.0.2 h11-… h2-… hpack-… httpcore-… httpx-… hyperframe-… idna-…" (exact list and versions vary), plus a **WARNING about running pip as the 'root' user**.
  - *(extra)* `python3 -c "import googletrans; print(googletrans.__file__)"` shows `/usr/local/lib/python3.11/dist-packages/googletrans/__init__.py` (Debian 12).
- **If it fails:**
  - `no such option: --break-system-packages`: your image has pip < 23.0.1 (e.g. Ubuntu 22.04's pip 22.0.2). That image also has no PEP 668 marker, so drop the flag.
  - Without `sudo`, pip prints "Defaulting to user installation because normal site-packages is not writeable" and installs to `~/.local/lib/python3.X/site-packages`. That still works for your user. The README's previous revision used no `sudo` (commit `e3bd74e` added it).

**Step 8. Run the app** (`README.md:58-61`):
```
python3 cli.py
python3 cli.py -t "Good morning. It is a good morning for cheese." -s "en" -d "es"
python3 cli.py -t "Good afternoon. Would you like some cheese?" -s "en" -d "fr"
```
- **Under the hood:**
  - argparse builds the `Namespace` (`cli.py:42-70`)
  - `asyncio.run` starts the event loop (`cli.py:72`)
  - `main` prints the banner, the args and the input (`cli.py:13-23`)
  - `Translator(raise_exception=True)` opens an `httpx.AsyncClient` and sends one HTTPS GET to `translate.googleapis.com` (`cli.py:25-31`)
  - the result text is printed (`cli.py:39`)
- **Checkpoint (first command)** — the banner and arguments were verified by running the same `art`/`argparse` calls in the sandbox:
  ```
      _      ____  ____   _  ____
     / \    / ___||___ \ / || ___|
    / _ \  | |      __) || ||___ \
   / ___ \ | |___  / __/ | | ___) |
  /_/   \_\ \____||_____||_||____/

  Arguments: Namespace(text='I love cheese', file='', src='en', dest='it')

  Input: I love cheese
  Output: <Italian translation, e.g. "Amo il formaggio">
  ```
  The translated wording comes from Google and wasn't verified here.
- **If it fails:**
  - `RuntimeError: Translation request to Google Translate failed (the server's network/IP may be rate-limited or blocked by Google's unofficial translate endpoint).` **Scroll up to the first exception** in the chained traceback ("The above exception was the direct cause of…"):
    - `Exception: Unexpected status code "429" …` (or another non-200 code): Google is throttling the VM's IP. Wait and retry, try another region, or run it on your laptop.
    - `ValueError: invalid destination language`: you mistyped a code (see §6).
  - `ModuleNotFoundError: No module named 'googletrans'`: Step 7 didn't install for this interpreter.

**Step 9. Delete the VM** (`README.md:62`). Or *(extra)* keep it for Part B. Reusing it is instructive, because it shows the venv ignoring the polluted system Python. Remember to delete it at the end.

### Part B: ⚡ Installing App on VM using UV (`README.md:68-101`)

**Steps 10-14. New VM, SSH, `sudo apt-get update`, `sudo apt install git`, `git clone …` + `cd simple-translate`** (`README.md:72-77`). These are identical to Steps 1-5. Note that Part B never installs `python3-pip`; uv doesn't need it.

**Step 15. Install uv** (`README.md:78`): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Under the hood:**
  - `curl -L` follows redirects, `-s` is silent, `-S` still shows errors, `-f` fails on HTTP errors.
  - The downloaded shell script detects your CPU and OS, downloads the `uv` and `uvx` binaries into `~/.local/bin`, writes `~/.local/bin/env`, and adds a line that sources it to your shell profile.
  - Alternatives are in `README.md:80-81`.
- **Checkpoint:** output ending roughly with "installing to /home/<you>/.local/bin … everything's installed!" and a hint to restart the shell or run `source $HOME/.local/bin/env`. The exact wording is the installer's.
- **If it fails:**
  - `curl: command not found` (rare on GCP images): `sudo apt-get install -y curl`
  - TLS or connection errors: check outbound internet

**Step 16. Put uv on PATH** (`README.md:83`): `source $HOME/.local/bin/env`
- **Under the hood:** the script prepends `$HOME/.local/bin` to `PATH` if it isn't there already. Its key line is `export PATH="$HOME/.local/bin:$PATH"` (line 9 of the installer-generated `~/.local/bin/env`).
- **Checkpoint:** `uv --version` prints `uv 0.x.y`; `which uv` gives `/home/<you>/.local/bin/uv`.
- **If it fails:** `uv: command not found` means you skipped this step or ran it as `sh ~/.local/bin/env`, which only changes a child shell. Open a new SSH tab or `source` it.

**Step 17. Create the environment** (`README.md:84`): `uv sync`
- **Under the hood** (`README.md:86-87` gives the README's version):
  1. Finds `pyproject.toml` in the current directory (`pyproject.toml:1-10`).
  2. Picks an interpreter satisfying `requires-python = ">=3.13"` (`pyproject.toml:6`). On a Debian 12 / Ubuntu 24.04 VM nothing qualifies, so uv **downloads a managed CPython**: the newest stable release ≥ 3.13, which was 3.14.6 with uv 0.11.32.
  3. Creates `.venv/`, whose prompt name comes from `name = "app"` at `pyproject.toml:2`.
  4. **Resolves** the dependency tree and **writes `uv.lock`**, because the repo has none.
  5. Installs 12 packages into `.venv`. The project itself is a "virtual" (non-installed) project because `pyproject.toml` has no `[build-system]`.
- **Checkpoint** (sandbox output; versions will differ for you):
  ```
  Downloading cpython-3.14.6-linux-x86_64-gnu (download) (34.3MiB)
   Downloaded cpython-3.14.6-linux-x86_64-gnu (download)
  Using CPython 3.14.6
  Creating virtual environment at: .venv
  Resolved 13 packages in …
  Installed 12 packages in …
   + anyio==4.15.1
   + art==6.5
   + certifi==2026.7.22
   + googletrans==4.0.2
   + h11==0.16.0
   + h2==4.4.1
   + hpack==4.2.0
   + httpcore==1.0.9
   + httpx==0.28.1
   + hyperframe==6.1.0
   + idna==3.20
   + typing-extensions==4.16.0
  ```
  (If the VM already has Python ≥ 3.13 you'll see `Using CPython 3.13.x interpreter at: /usr/bin/python3` instead of the download lines.)
  - `ls -a` now shows `.venv` and `uv.lock`
  - `cat .venv/pyvenv.cfg` contains `include-system-site-packages = false` and `prompt = app`
  - `git status` shows `uv.lock` as untracked; `.venv` stays hidden thanks to `.venv/.gitignore`
- **If it fails:**
  - `error: No \`pyproject.toml\` found in current directory or any parent directory`: you're not in `simple-translate/`.
  - `error: No interpreter found for Python >=3.13 in managed installations` with the hint "…Python downloads are set to 'never'": Python downloads are disabled (e.g. `UV_PYTHON_DOWNLOADS=never`). Unset that variable, or install a 3.13+ Python yourself.
  - Network errors: check egress to pypi.org and GitHub (the Python builds are fetched from python-build-standalone releases).

**Step 18. Activate** (`README.md:89`): `source .venv/bin/activate`
- **Under the hood:** see §3.4 and `README.md:91-92`.
- **Checkpoint:**
  - The prompt becomes **`(app) <you>@ac215-l01:~/simple-translate$`**. The README's example `(simple-translate) $` is wrong for this repo (§10).
  - `which python` gives `/home/<you>/simple-translate/.venv/bin/python`
  - `python --version` gives `Python 3.14.x` (or 3.13.x)
  - `which pip` prints **nothing**, because uv venvs have no pip
- **If it fails:** `bash: .venv/bin/activate: No such file or directory` means Step 17 didn't finish or you're in the wrong directory.

**Step 19. Run the app** (`README.md:94-97`):
```
python cli.py
python cli.py -t "Good morning. It is a good morning for cheese." -s "en" -d "es"
python cli.py -t "Good afternoon. Would you like some cheese?" -s "en" -d "fr"
```
- **Checkpoint:** the same output as Step 8.
- **If it fails:**
  - `python: command not found`: the venv isn't active (Debian has no `python`). Re-run Step 18, or use `uv run python cli.py`, which needs no activation.
  - Translation errors: as in Step 8.

**Step 20 (extra). Prove the isolation.**
- `deactivate`, then `python3 -c "import googletrans"`. On a *fresh* Part B VM this raises `ModuleNotFoundError`, because the packages exist only in `.venv`. On a reused Part A VM it succeeds from `/usr/local/lib/...`.
- `uv run python -c "import googletrans, sys; print(sys.prefix)"` prints the `.venv` path.

**Step 21. Delete the VM** (`README.md:98`) and confirm the instance and its disk are gone (§2).

### Part C (optional, read-only comparison): the `pipenv` branch

**Step 22.** On your laptop clone (or on the VM):
- `git show origin/pipenv:Pipfile` and `git show origin/pipenv:README.md | sed -n 22,35p` *(extra)*
- The pipenv README's VM walkthrough is (`origin/pipenv:README.md:29-31`): `sudo apt install pipenv`, `pipenv install`, `pipenv shell`.
- **Caveat:** that README's clone command (`origin/pipenv:README.md:27`) clones the **default branch (`main`)**, which has no `Pipfile`. To try it for real you'd first need `git switch pipenv` *(extra)*.
- I didn't verify that the old `googletrans==4.0.0rc1` stack (`origin/pipenv:Pipfile:9`; it locks `httpx==0.13.3`) still works.

---

## 5. Code tour

```
simple-translate/  (main @ 62f821b)
├── cli.py                 # the app: argparse -> asyncio -> googletrans -> print   (L01 core)
├── pyproject.toml         # project metadata, requires-python, 2 direct deps        (L01 core: read by uv sync)
├── README.md              # 4 walkthroughs; L01 = lines 38-101
├── Dockerfile.txt         # solution Dockerfile for L02 (uv sync inside python:3.12-slim-bookworm)
├── docker-shell.sh        # L02: build + run the image locally
├── docker-build-push.sh   # L02: multi-arch buildx build + push to dlops/simple-translate
├── .gitignore             # ignores .DS_Store, Dockerfile (student-made), /.idea/
└── .vscode/settings.json  # VS Code: Black as Python formatter
  (no uv.lock, no .python-version: both get created / are absent on your machine)

simple-translate/  (pipenv @ 3a354d8, comparison only)
├── Pipfile, Pipfile.lock  # pipenv equivalents of pyproject.toml / uv.lock (python 3.11, googletrans 4.0.0rc1)
├── cli.py                 # older synchronous version of the app
├── Dockerfile             # python:3.11-slim-buster + pipenv sync + "pipenv shell"
├── docker-shell.sh, tip.txt (sample text file for -f), README.md, .gitignore, .vscode/
```

**`pyproject.toml:1-10`**
```toml
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
- **L1:** `[project]` is the standard PEP 621 table that every modern Python tool reads.
- **L2:** `name = "app"` becomes the venv prompt (`(app)`) and the root of `uv tree`. Lines 2 and 4 are `uv init` boilerplate.
- **L6:** a *floor*, not a pin. It was changed from `">=3.12,<3.13"` to `">=3.13"` in commit `2827e2a` (2026-09-02); see §6 and §10.
- **L8:** `art>=6.5` allows any newer art.
- **L9:** `googletrans==4.0.2` is an exact pin, but only for this one package.
- There's no `[build-system]` table, so uv treats this as a *virtual project*: it installs the dependencies but not the project itself.

**`cli.py:5-9`** (imports)
```python
import argparse
import asyncio

from art import text2art
from googletrans import Translator
```
- `argparse` and `asyncio` are stdlib.
- `art` and `googletrans` are the only third-party imports, and they must come from *some* site-packages. Which one depends on the interpreter: system (Part A) or `.venv` (Part B).

**`cli.py:12-23`** (start of `main`)
```python
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
- `async def` is needed because googletrans 4.x is an asyncio library.
- `text2art("AC215")` draws the banner. Printing `args` shows the whole parsed `Namespace`, which is a useful debugging habit.
- `-f/--file` overrides `-t`. The path is relative to your *current directory*.

**`cli.py:25-39`** (the network call)
```python
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
- **L25:** `async with` closes the underlying `httpx.AsyncClient` on exit (googletrans `client.py:105-109`). `raise_exception=True` is crucial: the library default is `False` (googletrans `constants.py:461`), and with `False` a failed HTTP call silently returns the input text as the "translation" (`client.py:136-144`, excerpt below).
- **L27:** `await` performs one HTTPS GET.
- **L32-37:** catch *anything* and re-raise a friendlier `RuntimeError`, chained with `from error`. That also swallows non-network errors such as `ValueError("invalid destination language")`; see §6.
- **L39:** `result.text` is the translated string.

**`cli.py:65-72`** (CLI defaults and the event loop)
```python
    parser.add_argument(
        "-d",
        "--dest",
        default="it",
        help="Destination language",
    )

    asyncio.run(main(parser.parse_args()))
```
- The defaults (`-t "I love cheese"`, `-s en`, `-d it`; see `cli.py:45-70`) are why a bare `python cli.py` translates to Italian.
- `asyncio.run` creates an event loop, runs `main` to completion and closes the loop.
- `python cli.py --help` lists all four options.

**googletrans 4.0.2 (third-party, installed into `.venv/lib/python3.X/site-packages/googletrans/`), `client.py:130-144`**
```python
        if r.status_code == 200:
            data = utils.format_json(r.text)
            if not isinstance(data, list):
                data = [data]  # Convert dict to list to match return type
            return data, r

        if self.raise_exception:
            raise Exception(
                'Unexpected status code "{}" from {}'.format(
                    r.status_code, self.service_urls
                )
            )

        DUMMY_DATA[0][0][0] = text
        return DUMMY_DATA, r
```
- This is why commit `62f821b` added `raise_exception=True` to `cli.py:25`. Without it, a 429/403 from Google produces `Output: <your original text>` and no error.
- The request goes to `https://{host}/translate_a/single` (`urls.py:7`) with host `translate.googleapis.com` (`constants.py:3`). That's an unofficial, keyless endpoint, *not* the paid Cloud Translation API.

**googletrans 4.0.2 `client.py:263-269`** (language validation, which runs *before* any network call)
```python
        if dest not in LANGUAGES:
            if dest in SPECIAL_CASES:
                dest = SPECIAL_CASES[dest]
            elif dest in LANGCODES:
                dest = LANGCODES[dest]
            else:
                raise ValueError("invalid destination language")
```
- Lines 252-253 first lowercase the code and cut it at `_`, so `zh-CN` from the README table (`README.md:238`) becomes `zh-cn`, which is valid.
- An unknown code raises `ValueError`, which `cli.py:32` then wraps in the misleading "network/IP" `RuntimeError`.

**Generated by `uv sync`, not in the repo: `.venv/pyvenv.cfg`** (sandbox, system 3.13 interpreter)
```
home = /usr/bin
implementation = CPython
uv = 0.11.32
version_info = 3.13.16
include-system-site-packages = false
prompt = app
```
- `home` is where the real interpreter lives; `.venv/bin/python` is a symlink to `/usr/bin/python3`.
- `include-system-site-packages = false` is the isolation switch.
- `prompt = app` comes from `pyproject.toml:2`.

**Generated, not in the repo: `uv tree`** (sandbox, 2026-10-12)
```
app v0.1.0
├── art v6.5
└── googletrans v4.0.2
    └── httpx[http2] v0.28.1
        ├── anyio v4.15.1
        │   ├── idna v3.20
        │   └── typing-extensions v4.16.0
        ├── certifi v2026.7.22
        ├── httpcore v1.0.9
        │   ├── certifi v2026.7.22
        │   └── h11 v0.16.0
        ├── idna v3.20
        └── h2 v4.4.1 (extra: http2)
            ├── hpack v4.2.0
            └── hyperframe v6.1.0
```
2 declared dependencies became 12 installed packages. Everything below `googletrans` floats unless a `uv.lock` is shared.

**`origin/pipenv:Pipfile:8-13`** (the pipenv equivalent)
```toml
[packages]
googletrans = "==4.0.0rc1"
art = "*"

[requires]
python_version = "3.11"
```
- Same idea, different file: `[packages]` corresponds to `dependencies`, and `[requires] python_version` is an *exact minor* requirement (3.11) where uv uses a range.
- The committed `Pipfile.lock` pins 14 packages with sha256 hashes, e.g. `httpx==0.13.3` and `art==6.2`.

**`origin/pipenv:cli.py:4-11`** (the old synchronous API)
```python
import argparse
from googletrans import Translator
from art import text2art

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

translator = Translator()
```
- googletrans 4.0.0rc1 was synchronous: `translator.translate(...)` at `origin/pipenv:cli.py:30`, with no `await`.
- Moving to 4.0.2 forced the async rewrite on `main` (commit `e3bd74e`).
- Line 9 creates a parser that is never used; it's shadowed at line 38.

**`Dockerfile.txt:21-29`** (L02 preview: the same `uv sync`, inside an image)
```dockerfile
# Copy the source code
COPY . ./

RUN uv sync

# Entry point
ENTRYPOINT ["/bin/bash"]
# Get into the uv virtual environment shell
CMD ["-c", "source .venv/bin/activate && exec bash"]
```
- This is exactly Part B, baked into a container: `uv sync` builds the venv at build time.
- The container's default command `source`s the activate script, the same Step 18, so you land in an activated shell.

---

## 6. Gotchas and common errors

1. **`error: externally-managed-environment` from `pip3 install`.**
   - **Cause:** PEP 668. The Debian/Ubuntu system Python carries an `EXTERNALLY-MANAGED` marker.
   - **Fix:** in Part A, add `--break-system-packages` exactly as `README.md:53` does; or better, use a venv (Part B).

2. **`no such option: --break-system-packages`.**
   - **Cause:** an old image with pip < 23.0.1, e.g. Ubuntu 22.04 (pip 22.0.2) or Debian 11. Those images have no PEP 668 marker either.
   - **Fix:** drop the flag, or choose a Debian 12 / Ubuntu 24.04 image.

3. **`bash: python: command not found`.**
   - **Cause:** Debian/Ubuntu provide only `python3`, which is why Part A uses `python3` (`README.md:59-61`). In Part B, `python` exists only once the venv is active.
   - **Fix:** `source .venv/bin/activate` (`README.md:89`), or `uv run python cli.py`, or `.venv/bin/python cli.py`.

4. **`uv: command not found` right after installing.**
   - **Cause:** the installer put uv in `~/.local/bin`, which isn't on `PATH` in the current shell.
   - **Fix:** `source $HOME/.local/bin/env` (`README.md:83`), or open a new SSH tab.

5. **`uv sync` downloads ~34 MB of "cpython-3.14.x".**
   - **Cause:** `pyproject.toml:6` requires `>=3.13`. Debian 12 ships 3.11 and Ubuntu 24.04 ships 3.12, so uv fetches the newest stable release in range. That's 3.14.x, not 3.13 (sandbox, uv 0.11.32).
   - **Effect:** it isn't an error, but you're no longer running the OS Python, and two VMs with different images can end up on different interpreters.
   - **Fix (if you want determinism):** `uv python pin 3.13`, which writes `.python-version`. With the current `requires-python`, pinning 3.11 or 3.12 errors out: `error: The requested Python version \`3.11\` is incompatible with the project \`requires-python\` value of \`>=3.13\`.` (sandbox).

6. **`error: The requested interpreter resolved to Python 3.12.3, which is incompatible with the project's Python requirement: \`>=3.13\` (from \`project.requires-python\`)`.**
   - **Cause:** you forced an old interpreter (`uv sync --python 3.12`, or `UV_PYTHON=3.12`).
   - **Fix:** drop the override, or relax `requires-python` if you really need an older interpreter.

7. **`error: No interpreter found for Python >=3.13 in managed installations` plus the hint "…Python downloads are set to 'never'".**
   - **Cause:** downloads are disabled, e.g. by `UV_PYTHON_DOWNLOADS=never` or a corporate config.
   - **Fix:** allow downloads, or install Python 3.13+ yourself.

8. **The README promises a lockfile, but the repo has none.**
   - **Symptom:** two students (or the same student a week later) get different `httpx`/`certifi` versions, and `uv.lock` shows up as an untracked file.
   - **Cause:** `uv.lock` was never committed (`git log --all -- uv.lock` is empty), contradicting `README.md:12` and `README.md:70`.
   - **Fix:** in your own repo, commit `uv.lock` and use `uv sync --locked` in CI/Docker. `llm-rag/Dockerfile:42-45` shows the pattern the course uses later: copy `pyproject.toml uv.lock*`, then `RUN uv sync --frozen`.

9. **The prompt shows `(app)`, not `(simple-translate)`.**
   - **Cause:** uv names the venv prompt after `[project].name` (`pyproject.toml:2`), as `.venv/pyvenv.cfg` `prompt = app` and generated `activate:101-102` show. `README.md:92` shows `(simple-translate) $`.
   - **Fix:** none needed. It's cosmetic; rename the project in `pyproject.toml` if it bothers you.

10. **`pip install X` "doesn't work" inside an activated uv venv.**
    - **Symptom:** `pip: command not found` (fresh Part B VM), or an `externally-managed-environment` error (reused Part A VM, where `/usr/bin/pip` is the system pip).
    - **Cause:** uv venvs ship no `pip` (sandbox `.venv/bin` has none), contrary to `README.md:92`, which says activation makes "`python` and `pip` resolve to the venv's binaries".
    - **Fix:** `uv add X` (updates `pyproject.toml` and `uv.lock`) or `uv pip install X` (venv only, not recorded).

11. **`./.venv/bin/activate` → `Permission denied`, or `bash .venv/bin/activate` "does nothing".**
    - **Cause:** the activate script isn't executable (`-rw-r--r--`), and running it in a child shell can't change your current shell.
    - **Fix:** `source .venv/bin/activate` (`README.md:92` explains why).

12. **Misleading network error for a typo in a language code.**
    - **Symptom:** `python cli.py -d xx` ends with `RuntimeError: Translation request to Google Translate failed (the server's network/IP may be rate-limited or blocked …)`.
    - **Cause:** googletrans raises `ValueError("invalid destination language")` *before* any network call (googletrans `client.py:263-269`), and `cli.py:32-37` catches every `Exception` and rewraps it.
    - **Fix:** read the first exception in the chained traceback, and use codes from the table at `README.md:225-288`. Case doesn't matter, and `zh-CN`/`zh-TW` work.

13. **Real rate-limiting / blocking from Google.**
    - **Symptom:** the same `RuntimeError`, but the cause is `Exception: Unexpected status code "<code>" from ['translate.googleapis.com']`.
    - **Cause:** the app uses an unofficial, keyless endpoint (googletrans `constants.py:3`, `urls.py:7`). Cloud-provider IPs are a common target for throttling, and commit `62f821b`'s message and `cli.py:34-36` anticipate exactly this.
    - **Fix:** retry later, use a different region/VM, or run it on your laptop. The production-grade alternative is the official Cloud Translation API with credentials, which a later lecture's service-account work would enable. I didn't test it from a GCP IP.

14. **apt/git/curl hang or time out.**
    - **Cause:** the VM was created without an external IP (and has no Cloud NAT), so it has no outbound internet.
    - **Fix:** edit the VM's network interface to add an ephemeral external IP, or recreate the VM with the default networking.

15. **Surprise bills.**
    - **Cause:** you forgot to delete the VM; or you stopped it instead of deleting it (the disk still bills); or you unticked "delete boot disk" on deletion.
    - **Fix:** follow `README.md:62` and `:98`, then check *VM instances* and *Disks* (§2).

16. **Wrong directory.**
    - **Symptom:** `error: No \`pyproject.toml\` found in current directory or any parent directory` (sandbox message).
    - **Fix:** `cd ~/simple-translate`.

17. **Moved or renamed the project folder after `uv sync`.**
    - **Cause:** the generated `activate` hard-codes the absolute venv path (`VIRTUAL_ENV='…/.venv'`, line 81 of the sandbox `activate`).
    - **Fix:** `rm -rf .venv && uv sync`. Venvs aren't relocatable; treat them as disposable build output.

18. **The pipenv branch doesn't work as documented.**
    - **Symptoms:**
      - `pipenv install` creates an empty Pipfile, because the branch README's `git clone` (`origin/pipenv:README.md:27`) checks out `main`, which has no Pipfile
      - pipenv may complain about Python 3.11 vs your system Python (`origin/pipenv:Pipfile:13`)
      - building its Dockerfile fails at `apt-get update`
    - **Cause:** that Dockerfile's base image is Debian 10 *buster* (`origin/pipenv:Dockerfile:2`, `python:3.11-slim-buster`), which is end-of-life and whose apt repositories have been moved to the archive. I expect the failure but didn't test it.
    - **Fix:** `git switch pipenv` before `pipenv install`; treat the branch as a reading exercise.

19. **(Applies from L02 on) The Python version in `Dockerfile.txt` disagrees with `pyproject.toml`.**
    - **Cause:** `Dockerfile.txt:2` and `README.md:133-136` use `python:3.12-slim-bookworm`, but `pyproject.toml:6` needs ≥ 3.13.
    - **Effect:** `RUN uv sync` (`Dockerfile.txt:24`) skips the image's 3.12 and downloads a separate CPython (3.14.x today) at build time. That makes a bigger image whose base Python goes unused.
    - **Fix:** use a `python:3.13-slim` base or change `requires-python`.
    - **Platform:** the uv binaries and managed Pythons exist for both x86_64 and aarch64, so an Arm VM (t2a/c4a) works too. Apple Silicon issues (amd64 vs arm64 images) only appear in L02 (see the commented `--platform=linux/amd64` at `docker-shell.sh:12`).

---

## 7. Where this sits in the course

- **Before:**
  - **Tutorial 0 - Setup & Installs** (`README.md:20-21`) gives you the GCP account and project, VS Code, Git, Docker Desktop and uv on your laptop.
  - Lecture 1 is the first lecture with a tutorial (`tutorials_demo.md:16-27`); the course README lists "Virtual Environments and Virtual Machines" as the third theme, after the MLOps intro and LLM topics.
- **What L01 adds:**
  - Two isolation primitives, the VM (a disposable machine) and the venv (disposable package sets).
  - The vocabulary everything else uses: `pyproject.toml`, `uv sync`, `uv.lock`, `.venv`, `requires-python`, activation.
  - The habit of tearing down cloud resources.
- **Next (L02 Containers I, same repo, `tutorials_demo.md:31-42`):**
  - Walkthroughs 3-4 of this README (`README.md:106-220`) put the *same* `uv sync` inside a Docker image (`Dockerfile.txt:24`), run it locally (`docker-shell.sh:11-15`), and push it to Docker Hub.
  - Then you run the image on a fresh VM that has only Docker (`README.md:207-218`, `sudo docker run --rm -ti dlops/simple-translate`). The image `dlops/simple-translate` is built and pushed multi-arch by `docker-build-push.sh:11` and `:27`.
- **Later:**
  - **L03 mega-pipeline** has you author a `pyproject.toml` yourself with `uv init --bare` (`mega-pipeline/generate_text/README.md:22`) and `uv add` (`:104`). Its `generate_text/pyproject.toml:4` already requires `>=3.14`.
  - **cheese-app/llm-rag** uses the production pattern this repo lacks: a committed `uv.lock`, `UV_PROJECT_ENVIRONMENT=/.venv`, `UV_LINK_MODE=copy` and `uv sync --frozen` (`llm-rag/Dockerfile:17-18`, `:42-45`).
  - pipenv also survives in `cheese-app-v0/api-service` (`Pipfile`, `Dockerfile:44` `RUN pipenv sync`), so the comparison in Part C pays off.
- **Milestone 2** requires "Virtual Environment Setup" ("Create virtual machines/environments to support containers", `milestone2.md:39-41`) and "`pyproject.toml` (using `uv`) for each container" (`milestone2.md:78`).
- **Branch diff (`pipenv` → `main`, unrelated roots):** `git diff --stat origin/pipenv main` reports 11 files changed, 265 insertions, 247 deletions.

  | File | Change | Lines |
  |---|---|---|
  | `.gitignore` | +2 | |
  | `Dockerfile` | removed | −26 |
  | `Dockerfile.txt` | new | +29 |
  | `Pipfile` | removed | −13 |
  | `Pipfile.lock` | removed | −128 |
  | `README.md` | rewritten | ±186 |
  | `cli.py` | rewritten | ±81 |
  | `docker-build-push.sh` | new | +29 |
  | `docker-shell.sh` | changed | ±4 |
  | `pyproject.toml` | new | +10 |
  | `tip.txt` | removed | −4 |

  Meaningful changes:
  1. pipenv/Pipfile replaced by uv/pyproject (the lockfile was dropped along the way)
  2. googletrans 4.0.0rc1 (sync) → 4.0.2 (async), so `cli.py` now uses `asyncio.run` and `async with Translator(raise_exception=True)`
  3. Python 3.11 → ≥3.13 for the app (the Dockerfile still says 3.12)
  4. Debian buster → bookworm base image
  5. Docker build defaults to the native architecture (`docker-shell.sh:11`; the amd64 line at `:12` is commented out), plus a new multi-arch push script
  6. the README gained a narrative ("four ways, each removing a class of fragility", `README.md:9-16`) and tips on `apt` vs `apt-get`, PEP 668, `uv sync` and `activate`

  On `main` itself, history was reset on 2026-08-28 (`5a6849d`); since then `e3bd74e` made `cli.py` async and added `sudo`, `476aec1` bumped googletrans in the README, `2827e2a` bumped `requires-python`/googletrans in `pyproject.toml`, and `62f821b` added the `raise_exception`/`RuntimeError` wrapping.

---

## 8. Video plan (suggestion)

**Hook question:** "On a brand-new cloud computer, `pip install` refuses to install a package. *Your* computer, *your* root password — why would it say no? And why does the fix involve the word 'virtual' twice?"

**Target length:** ~20 minutes (~3,100 spoken words at 155 wpm). Viewers should pause at each "▶ do it" marker and run the command on their own VM, with the local clone open in VS Code for reading `cli.py` and `pyproject.toml`.

**Chapters**

1. **Two kinds of "virtual"** (1.5 min)
   - *Idea:* VMs virtualize the machine; venvs virtualize the Python package set. Different problems, used together.
   - *Visual:* the word "virtual" splits into two labels; two nested boxes appear (a large box "VM" holding a small box "venv"), with a dashed future box "container" fading in between them.
   - *On screen:* `README.md:9-16` (the four-step ladder).

2. **Renting a computer** (2.5 min)
   - *Idea:* a VM is a slice of a physical server with its own OS; you pay while it runs and while its disk exists.
   - *Visual:* the server box gets a hypervisor slab and splits into slices (§3.1 animation); a cost meter ticks beside your slice.
   - *On screen:* the console *Create instance* form (machine type, zone, boot disk, external IP), the SSH button, then ▶ `cat /etc/os-release`, `python3 --version`, `which python` (no output).

3. **The quick-and-dirty install** (3 min)
   - *Idea:* the OS owns its Python; PEP 668 is a guard rail; `--break-system-packages` and `sudo` put packages into a shared, OS-wide location.
   - *Visual:* a "kitchen" labelled `/usr/lib/python3/dist-packages (apt)` with a second shelf `/usr/local/lib/.../dist-packages (sudo pip)` sliding in *above* it, shadowing two jars (`idna`, `certifi`).
   - *On screen:* ▶ `sudo apt-get update`, `sudo apt install git`, `git clone …`, `sudo apt install python3-pip`, the failing `pip3 install googletrans==4.0.2 art`, then `sudo pip3 install --break-system-packages googletrans==4.0.2 art` (`README.md:44-53`), then `python3 -c "import googletrans; print(googletrans.__file__)"`.
   - **Pause-and-ponder #1:** "Your classmate's project needs `httpx 0.13` and yours needs `httpx 0.28`, on the same VM. With only this install method, what happens?" (Answer later: the last install wins for *everyone*, which motivates the venv.)

4. **What `cli.py` actually does** (2.5 min)
   - *Idea:* argparse → asyncio → one HTTPS GET to an unofficial endpoint → print; plus why `raise_exception=True` matters.
   - *Visual:* a pipeline of boxes: `argv` → `Namespace(text=…, file='', src='en', dest='it')` → event loop circle → an arrow leaving the VM to `translate.googleapis.com` → a JSON blob → "Output:". Then replay it with a red 429 on the return arrow: first with the old code (the output is just the input echoed back), then with `raise_exception=True` (a red exception propagates up and wraps into a `RuntimeError`).
   - *On screen:* `cli.py:12-39`, googletrans `client.py:130-144`, ▶ the three `python3 cli.py …` commands (`README.md:59-61`).

5. **A private toolbox: what a venv really is** (2.5 min)
   - *Idea:* a venv is a symlinked interpreter, an empty site-packages and a `pyvenv.cfg` switch.
   - *Visual:* the `sys.path` shelves animation (§3.3); a symlink arrow from `.venv/bin/python` to the real interpreter.
   - *On screen:* `ls -la .venv/bin`, `cat .venv/pyvenv.cfg`.

6. **uv sync: from wish list to receipt** (3 min)
   - *Idea:* `pyproject.toml` declares, the resolver expands the tree, and `uv.lock` freezes it. Also: this repo has no lockfile.
   - *Visual:* the dependency-tree growth → version tags → scroll animation (§3.5); two students' trees diverging without the scroll.
   - *On screen:* ▶ `curl -LsSf https://astral.sh/uv/install.sh | sh`, `source $HOME/.local/bin/env`, `uv sync` (`README.md:78-84`), then `uv tree`, `head -40 uv.lock`, `git status`.
   - **Pause-and-ponder #2 (before `uv sync`):** "`pyproject.toml` says `requires-python = ">=3.13"`; this VM has Python 3.11. Predict what `uv sync` will do: fail, use 3.11, or something else?" (Then reveal the number-line animation (§3.6) and the download of 3.14.x.)

7. **Activation is just PATH** (2 min)
   - *Idea:* `source activate` puts `.venv/bin` first in `PATH` and changes the prompt; nothing else.
   - *Visual:* the row-of-doors animation (§3.4); the prompt gains `(app)`, with a note that the README says `(simple-translate)`.
   - *On screen:* ▶ `source .venv/bin/activate`, `which python`, `echo $PATH | tr ':' '\n' | head -3`, `which pip` (nothing), the three `python cli.py …` runs (`README.md:95-97`), `deactivate`, `uv run python cli.py`.
   - **Pause-and-ponder #3:** "After `deactivate`, will `python3 -c 'import googletrans'` work on the Part B VM? And on the Part A VM?" (Fresh Part B VM: no, because the packages live only in `.venv`. Part A VM: yes, from `/usr/local`.)

8. **The old way: pipenv** (1.5 min)
   - *Idea:* the same concepts under different names (Pipfile/Pipfile.lock, a venv outside the project, `pipenv shell` as a subshell).
   - *Visual:* a two-column morph in which `pyproject.toml` ↔ `Pipfile`, `uv.lock` ↔ `Pipfile.lock` and `.venv/` ↔ `~/.local/share/virtualenvs/…` slide across and swap labels.
   - *On screen:* `git show origin/pipenv:Pipfile`, `origin/pipenv:README.md:29-31`.

9. **Tear it down, and what's next** (1.5 min)
   - *Idea:* delete, don't stop; and the next step is to freeze OS + Python + venv together into a container.
   - *Visual:* the cost meter stops only when "Delete" dissolves both the VM *and* its disk; then the dashed "container" box from chapter 1 solidifies around the venv.
   - *On screen:* the console Delete dialog, *Disks* page, `gcloud compute instances list`, a preview of `Dockerfile.txt:21-29`.

**Recap questions (end of video)**
1. What does `--break-system-packages` actually break, and where did `sudo pip3` put the files?
2. Name the three things inside `.venv` that make it a virtual environment.
3. What exactly changes in your shell when you `source .venv/bin/activate`? Name two ways to run the app without activating.
4. `pyproject.toml` lists two dependencies; why did 12 packages get installed, and which file would make every student get the same 12 versions?
5. Is `requires-python = ">=3.13"` a pin? What would make the Python version deterministic?
6. Which GCP resources keep billing after you *stop* a VM?

---

## 9. Exercises

**E1. Where do packages live? (hands-on, predict-then-run)**
- On your Part A VM, *predict* what `python3 -c "import googletrans, sys; print(googletrans.__file__); print(sys.prefix)"` prints. Then do the same with `.venv/bin/python` on your Part B VM.
- *Worked answer:*
  - The system interpreter prints `/usr/local/lib/python3.11/dist-packages/googletrans/__init__.py` (on Debian 12; the minor version follows the image) and `sys.prefix = /usr`.
  - The venv interpreter prints `…/simple-translate/.venv/lib/python3.14/site-packages/googletrans/__init__.py` (or `python3.13`) and `sys.prefix = …/simple-translate/.venv`.
  - Same import statement, different shelf, because each interpreter builds its own `sys.path`. In a venv, `include-system-site-packages = false` keeps the system shelves out.

**E2. Which Python will uv pick? (hands-on, predict-then-run)**
- On a fresh Debian 12 VM, before `uv sync`, run `python3 --version` and `uv python list --only-installed`. Predict the interpreter `uv sync` will use. Then run it and check `cat .venv/pyvenv.cfg`.
- Next, make it use exactly 3.13: `uv python pin 3.13` followed by `uv sync`.
- *Worked answer:*
  - The system has 3.11, which falls outside `>=3.13`, so uv downloads the newest stable release in range: 3.14.x with uv 0.11.32 (`Downloading cpython-3.14.6-…`). `pyvenv.cfg` shows `version_info = 3.14.x` and a `home` under `~/.local/share/uv/python/`.
  - `uv python pin 3.13` writes `.python-version` containing `3.13`. The next `uv sync` downloads CPython 3.13.x (none is installed) and recreates `.venv` with it.
  - Pinning `3.11` fails with `error: The requested Python version \`3.11\` is incompatible with the project \`requires-python\` value of \`>=3.13\`.` To use 3.11 you must first relax `requires-python`. In the sandbox, `>=3.11` plus `uv python pin 3.11` gave "Using CPython 3.11.17 interpreter at: /usr/bin/python3.11".

**E3. "It says the network is down, but it isn't" (debugging)**
- `python cli.py -t "hello" -d xx` fails with `RuntimeError: Translation request to Google Translate failed (the server's network/IP may be rate-limited or blocked by Google's unofficial translate endpoint).` Is the network the problem?
- *Worked answer:*
  - No. Scroll up: the first traceback ends with `ValueError: invalid destination language`, raised by googletrans' validation (`client.py:263-269`) *before* any HTTP request. `cli.py:32-37` catches **every** `Exception` and rewraps it with a network-flavoured message.
  - Fix the code (`-d es`). For a better program, catch `ValueError` separately, or validate against `googletrans.LANGUAGES` before calling the API.
  - Lesson: in a chained traceback, the *first* exception is the cause.

**E4. `pip install` inside the venv (debugging)**
- With `(app)` active on your Part B VM, you run `pip install rich` and get `bash: pip: command not found`. On your reused Part A VM, the same command gives `error: externally-managed-environment`. Explain both, and add `rich` properly.
- *Worked answer:*
  - uv-created venvs contain no pip (`ls .venv/bin`), so `PATH` lookup falls through to the system. The fresh Part B VM has no system pip at all (Part B never ran `apt install python3-pip`). On the Part A VM, `/usr/bin/pip` exists but belongs to the system Python, which is PEP 668-protected.
  - The proper way is `uv add rich`. It adds `"rich>=…"` to `pyproject.toml`, updates `uv.lock` and installs into `.venv`. `uv pip install rich` would install into the venv *without* recording it, so the next person wouldn't get it.

**E5. Make it reproducible (hands-on)**
- After `uv sync`, commit the generated `uv.lock` in your own fork or your `MLOps_Learning` repo. Then add `"rich"` to `dependencies` by hand in `pyproject.toml` (don't use `uv add`) and run `uv sync --locked`. Predict the outcome, then fix it.
- *Worked answer:*
  - uv notices the lockfile no longer matches `pyproject.toml` and refuses:
    ```
    error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.

    hint: To update the lockfile, run `uv lock`.
    ```
    (sandbox output; it resolved 17 packages before refusing)
  - Fix it with `uv lock` (or `uv sync` without `--locked`), then commit both files.
  - Without any `uv.lock`, `uv sync --locked` fails with `error: Unable to find lockfile at \`uv.lock\`, but \`--locked\` was provided. To create a lockfile, run \`uv lock\` or \`uv sync\` without the flag.`
  - This is why the course's later Dockerfiles copy `uv.lock*` and use `uv sync --frozen` (`llm-rag/Dockerfile:42-45`).

**E6. Activation mechanics (debugging + conceptual)**
- A classmate runs `./.venv/bin/activate` and gets `Permission denied`. They try `bash .venv/bin/activate`: no error, but `which python` still prints nothing. Why? Give two ways to run the app *without* activating.
- *Worked answer:*
  - `activate` isn't executable (`-rw-r--r--`). With `bash`, it runs in a child process that modifies *its own* `PATH` and exits, leaving your shell unchanged. Activation must happen in the current shell, which is what `source` does (`README.md:92`).
  - Ways to skip activation: `.venv/bin/python cli.py` (calls the venv interpreter directly), or `uv run python cli.py` (uv syncs if needed, then runs inside the venv).

**E7. Files from disk (hands-on)**
- Create `msg.txt` containing two sentences in French, then run `python cli.py -f msg.txt -s auto -d en`. Predict what "Arguments:" and "Input:" print.
- *Worked answer:*
  - `Arguments: Namespace(text='I love cheese', file='msg.txt', src='auto', dest='en')`. `-t` keeps its default, but `cli.py:19-21` replaces `text` with the file's contents, so `Input:` shows your French text.
  - `src='auto'` is accepted, because googletrans skips source validation for `auto` (`client.py:255`).
  - A wrong path gives `FileNotFoundError` *before* the network call. Unlike E3 it isn't rewrapped: the file read at `cli.py:19-21` happens outside the `try`.

**E8. Pick the right isolation (conceptual)**
- For each case, say whether a venv is enough or you need a VM/container:
  - (a) two projects need different `pandas` versions
  - (b) your code needs the `libpq` C library and a specific CUDA driver
  - (c) a teammate on macOS must reproduce your exact Linux setup
  - (d) you want to experiment with `sudo apt` changes without risking your laptop
- *Worked answer:*
  - (a) A venv per project is enough.
  - (b) A venv only isolates Python packages; system libraries and drivers need a container image (L02) or a VM image.
  - (c) A venv plus `uv.lock` gets the Python packages identical, but the OS differs. A container gives them the same Linux userland.
  - (d) A VM, which is disposable: delete it when done.

---

## 10. Errata and open questions

**Errata (wrong, outdated, ambiguous or inconsistent)**

1. **The promised lockfile doesn't exist.**
   - The claim: `README.md:12` says "pinned in a lock file, so the next person gets the exact same versions", and `README.md:70` says "`uv.lock` pins exact versions so the next person gets the same setup".
   - The evidence: there's no `uv.lock` in the tree (`git ls-files`), and `git log --all -- uv.lock` is empty, so every `uv sync` on a fresh clone resolves anew. `README.md:87` hedges with "and `uv.lock` if present".
2. **Wrong prompt example.** `README.md:92` shows `(simple-translate) $`. With `name = "app"` (`pyproject.toml:2`), uv's venv prompt is `(app)`: the sandbox shows `prompt = app` in `pyvenv.cfg` and `VIRTUAL_ENV_PROMPT="app"` in `activate:102`.
3. **No pip in a uv venv.** `README.md:92` says activation makes "`python` and `pip` resolve to the venv's binaries". uv venvs contain no `pip` (sandbox `.venv/bin` listing).
4. **Miscount in the activate tip.** `README.md:92` says "Four things … so you can later run `deactivate` to undo all three". The count is internally inconsistent; this is cosmetic.
5. **Python version mismatch between app and Dockerfile.** `pyproject.toml:6` (`>=3.13`, changed in `2827e2a` on 2026-09-02 from `">=3.12,<3.13"`) disagrees with `Dockerfile.txt:2` and `README.md:133-136` (`python:3.12-slim-bookworm`, "Python 3.12 image"). This hits in L02, where uv will download another interpreter inside the image.
6. **"Pinned" isn't a pin.** `requires-python = ">=3.13"` isn't a version pin, and there's no `.python-version`. The README never says that `uv sync` may download a Python, which it will on Debian 12 / Ubuntu 24.04 images (3.14.x with uv 0.11.32). That makes "the next person gets the same setup" (`README.md:70`) doubly untrue: neither the packages nor the interpreter are fixed.
7. **Misleading error message.** `cli.py:32-37` wraps *every* exception, including `ValueError("invalid destination language")` from googletrans' validation (`client.py:263-269`), in a message blaming the network or IP.
8. **Probably broken Contents links.** `README.md:31-32` use `#installing-app-on-vm-manually` and `#installing-app-on-vm-using-uv`. The course site uses the emoji-derived anchors `#%EF%B8%8F-installing-app-on-vm-manually` and `#-installing-app-on-vm-using-uv` (`tutorials_demo.md:21`, `:26`). I couldn't confirm the rendering offline.
9. **The VM spec is underspecified.** `README.md:42` and `:72` give no machine type, zone, image or networking guidance. The outcome depends on the image: whether `--break-system-packages` exists (pip ≥ 23.0.1), and whether uv downloads a Python.
10. **Part A and Part B can get different `art` versions.** `README.md:53` installs `art` unpinned in Part A, while `pyproject.toml:8` says `art>=6.5`. The difference is small.
11. **The `pipenv` branch is stale as a runnable tutorial.**
    - Its README clones the default branch (`origin/pipenv:README.md:8`, `:27`), so the `Pipfile` isn't present unless you switch branches.
    - Its Docker base `python:3.11-slim-buster` (`origin/pipenv:Dockerfile:2`) is Debian 10, which is EOL.
    - It tags images as `…-e115` (`origin/pipenv:README.md:91`), a leftover from another course.
    - The AWS track still uses pipenv (`tutorials_demo.md:24-27`).
12. **Boilerplate metadata.** `pyproject.toml:4` (`description = "Add your description here"`) and `name = "app"` are `uv init` boilerplate. That's harmless, but it's why the prompt reads `(app)`.

**Open questions (couldn't be determined from the sources)**
- What the Ed lesson (slides, lecture notes) adds or changes relative to the README. I had no access to Ed content.
- Contents of Tutorial 0 (`dlops-io/ac215-setup`), which wasn't cloned: which uv version students install, and whether `gcloud` is part of the setup.
- Which boot image the GCP console defaults to when students do the lab (Debian 12 vs 13). That decides whether uv uses the system Python or downloads one.
- Whether `translate.googleapis.com` currently rate-limits or blocks GCP egress IPs. Commit `62f821b` and `cli.py:34-36` suggest it has happened, but I didn't test from a VM. I also didn't verify the exact translated output strings.
- Whether instructors intend a new VM per walkthrough (as written, `README.md:72`) or reuse of one VM. Reuse is cheaper and demonstrates the isolation better.
- Whether the pipenv branch (`googletrans==4.0.0rc1`, `httpx==0.13.3`) still runs at all today. Not tested.
