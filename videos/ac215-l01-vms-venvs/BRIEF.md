# Brief · AC215 L1 — Virtual machines, virtual environments and uv

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest) and `assets/` (real captures, see `ASSETS.md`).
**Where the digest and the captures disagree, the captures win** (they are newer: a fresh uv
install on 2026-10-12 is uv 0.13.0, and on Debian 12 it downloads CPython 3.15.0, not 3.14.x).

## Audience and goal

An AC215 student: knows Python and basic ML, has done Tutorial 0 (GCP project with billing, VS
Code, git, Docker Desktop, uv on the laptop), has never set up a cloud VM or thought about where
`import` finds packages. They watch with the README of
[dlops-io/simple-translate](https://github.com/dlops-io/simple-translate) open and a VM of their
own, pausing to type each command.

After the video they can: create, SSH into and delete a Compute Engine VM; explain what
`--break-system-packages` breaks and where `sudo pip3` put the files; explain the three parts of a
venv and what activation changes; predict which Python `uv sync` will use; read `pyproject.toml`
vs `uv.lock`; read a chained traceback; and they know the README's four small errata.

## Length and parts

~30 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm). Part 1 = S01–S07
(the VM and the manual install), part 2 = S08–S15 (venvs and uv). Word budgets per scene below are
targets (±15 %).

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| the laptop / browser | GREY |
| the cloud, the VM, Google's servers | BLUE |
| the system Python and everything apt / `sudo pip` put in it (shared, OS-owned) | ORANGE |
| the venv, `.venv/`, `uv.lock`, project-owned packages | GREEN |
| uv itself (the tool) | PURPLE |
| errors, refusals, the 429, "don't do this" | RED |
| your turn, the README tracker, "look here now" | YELLOW |
| money: the cost meter, billing tags | GOLD |
| PATH and sys.path lookups (the search-light, the doors) | PINK |
| a future thing (the L2 container) | GREY, dashed |

Package chips are coloured by **where they live** (ORANGE in the system, GREEN in the venv), never
by package.

## Running example

User `student`, VM `ac215-l01` (zone us-central1-a, e2-small, Debian 12), as in the captures:
prompt `student@ac215-l01:~$`, then `student@ac215-l01:~/simple-translate$`, then
`(app) student@ac215-l01:~/simple-translate$`. The narration says once that their prompt shows
their own username. Debian 13 is shown as the alternative wherever it changes the outcome (S03:
`python3 --version`; S10: which Python uv picks).

## Visual set pieces (the 3Blue1Brown part)

- **V1 · Slicing a server (S03).** A physical server; a hypervisor slab slides on; the box splits
  into translucent slices, each grows its own OS layer (Debian 12, Ubuntu 24.04, …). One slice is
  yours (BLUE, "ac215-l01"); a browser on the left draws an SSH beam into it. A GOLD cost meter
  starts ticking beside it; in S07 "Delete" dissolves the slice and its disk and the meter stops
  (stopping alone leaves the disk and the meter keeps a slow tick).
- **V2 · sys.path shelves (S05, S08, S13).** `sys.path` as a vertical stack of shelves, real paths
  from `assets/terminal/debian12-part-a/15-syspath.txt`. `import googletrans` is a PINK search-light
  scanning top to bottom. In S05 `sudo pip3` adds jars to the ORANGE `/usr/local/lib/python3.11/
  dist-packages` shelf, which sits *above* apt's `/usr/lib/python3/dist-packages`: a same-named jar
  there is hidden (shadowing). In S08 the venv interpreter builds a different stack: the system
  dist-packages shelves slide out, a GREEN `.venv/lib/python3.15/site-packages` shelf slides in
  (real paths from `debian12-part-b/22-syspath-venv.txt`).
- **V3 · PATH doors (S09, S12).** `PATH` as a row of doors, left to right (real PATH from
  `debian12-part-b/12-python-before.txt`). A typed command name walks along and knocks; no door has
  `uv` → "command not found". `source $HOME/.local/bin/env` slides a PURPLE `~/.local/bin` door in
  at the left (the installer also added that line to your shell's startup files, which is why a
  new SSH tab works too). The doors before `source` are the real PATH minus that first entry
  (the capture had already sourced the env file). In S12 `activate` slides a
  GREEN `.venv/bin` door in at the very front; `python` walks in. `deactivate` slides it out.
- **V4 · The version number line (S10).** 3.10 … 3.16, the interval `>= 3.13` glowing GREEN. Dots
  for the interpreters uv finds: Debian 12's `3.11.2 /usr/bin/python3` lands outside (RED). A
  PURPLE download arrow drops `3.15.0 (uv-managed, 35.9 MiB)` into the interval — "the newest
  release that satisfies the constraint, at the time of recording". Then a split: on Debian 13,
  `3.13.5 /usr/bin/python3` is already inside → used, no download. `.venv/bin/python` draws a
  symlink arrow to the chosen one. A `.python-version` pin would turn the interval into one point.
- **V5 · Wish list → receipt (S11).** Two GREEN nodes (`art>=6.5`, `googletrans==4.0.2`) grow into
  the real `uv tree` (assets/terminal/debian12-part-b/17-tree.txt). Every node gets an exact version
  tag that clicks into place; the tree compresses into a scroll labelled `uv.lock`. Two students, a
  week apart, without a shared lock: their leaves get different version tags; with the scroll,
  identical.
- **V6 · What cli.py does (S02).** argv → `Namespace(text=…, src='en', dest='it')` → event loop →
  one HTTPS GET leaving the VM to `translate.googleapis.com` (BLUE) → JSON → `Output:`.
- **V7 · Nesting dolls (S01, S15).** VM ⊃ (dashed container, "L2") ⊃ venv, and the README's
  four-rung ladder (manual → uv → Docker on the laptop → Docker on a VM) with L1's two rungs lit.
- **V8 · A chained traceback (S06).** Two stacked RED boxes: the first exception (the cause) and
  the `RuntimeError` it was wrapped in, joined by "The above exception was the direct cause of the
  following exception". The eye goes to the first one.

## Scene plan

Tracker steps (ReadmeTracker), from the README bullets:
- Part A, *Installing App on VM Manually*: Create VM · SSH · apt-get update · Install git · Clone ·
  cd · Install pip · Install packages · Run it · Delete VM (10)
- Part B, *Installing App on VM using UV*: Create VM · SSH · apt-get update · Install git · Clone ·
  cd · Install uv · Reload shell · uv sync · Activate · Run it · Delete VM (12)

**S01 · Why won't pip install? (~230 words).** Cold open on the real refusal: `pip3 install
googletrans==4.0.2 art` → `error: externally-managed-environment` (real text, assets
`07-pip-refused.txt`, trimmed). "A brand-new computer, you have root, and pip says no." Then the
word "virtual" appears twice: virtual *machine*, virtual *environment* — this lecture's two ideas.
V7 ladder: the README's four ways to run the same app, each removing a kind of fragility; today
the first two. How to follow along: the README tracker (top-left), code panels with path and
lines, "▶ your turn" tags; the study guide in MLOps_Learning has every command. Tutorial 0 is the
prerequisite (GCP project with billing); no service account needed today.

**S02 · The app (~330).** What we install before how. `cli.py` in panels (assets/source/cli.py,
real line numbers): imports (5-9: two stdlib, two third-party — "these two have to come from
somewhere, and *where* is this whole lecture"), `main` (12-23), the translate call (25-39),
argparse defaults (42-70: -t "I love cheese", -s en, -d it) and `asyncio.run` (72). V6 pipeline.
Mention `raise_exception=True` (line 25): without it a failed request silently prints your input
back as the "translation" (googletrans default). Keep code on screen ≤ 12 lines at a time.

**S03 · Renting a computer: the VM (~360).** V1. Compute Engine vocabulary as the schematic create
form fills in (tag `illustration`, no Google branding): name `ac215-l01`, region us-central1 / zone
us-central1-a, machine type e2-small, boot disk Debian 12 (Debian 13 also fine), external IP on.
The README gives no settings: say these are sensible choices. GOLD tags: billed per second while
running; the disk bills while it exists. Click SSH → terminal (title `ssh · ac215-l01`). ▶ extra
checks (marked extra): `cat /etc/os-release` (real: Debian GNU/Linux 12 (bookworm)),
`python3 --version` → `Python 3.11.2` (Debian 13: `3.13.5`), `which python` → nothing:
"Debian only has python3; remember this, it comes back". Tracker 1→2.

**S04 · apt, git and the repo (~250).** ▶ `sudo apt-get update` (real Get: lines, Fetched…):
apt's catalog vs installing — update downloads the *list* of what exists; nothing is installed yet.
The README tip: `apt-get` for scripts, `apt` for humans. ▶ `sudo apt install git`: the
"Do you want to continue? [Y/n]" prompt → Y (output trimmed: "the exact list varies"). ▶
`git clone https://github.com/dlops-io/simple-translate.git`, `cd simple-translate` (prompt path
changes), `ls` (real listing). Point out: no `requirements.txt`, no `uv.lock` — just
`pyproject.toml`. Tracker 3→6.

**S05 · The system Python and PEP 668 (~400).** ▶ `sudo apt install python3-pip`; extra:
`pip3 --version` → `pip 23.0.1 from /usr/lib/python3/dist-packages/pip (python 3.11)`. Extra (the
cold open, now in context): `pip3 install googletrans==4.0.2 art` → refused; read the real message
(highlight "externally managed", "create a virtual environment"). V2: who owns which shelf; the OS
itself runs Python tools that depend on apt's jars ("a shared kitchen"). ▶ The README's command:
`sudo pip3 install --break-system-packages googletrans==4.0.2 art` → real "Successfully installed
…" (12 packages — "we asked for two") and the WARNING about running pip as root. Extra:
`python3 -c 'import googletrans; print(googletrans.__file__)'` →
`/usr/local/lib/python3.11/dist-packages/...`: the ORANGE shelf above apt's. Shadowing, said
plainly: if a pip jar and an apt jar share a name, Python takes the higher shelf, for every program
on the machine. The README tip says it is deliberate here, as a demonstration.
PONDER 1 (8 s): "A classmate's project on this VM needs httpx 0.13; yours needs httpx 0.28. Both
install system-wide like this. What happens?" Answer at the start of S06's first block or end of
S05: the last install wins, for everyone.

**S06 · Run it, and read the traceback (~330).** ▶ `python3 cli.py` (expected output: banner,
`Arguments: Namespace(text='I love cheese', file='', src='en', dest='it')`, `Input: I love cheese`,
`Output: Adoro il formaggio`; tag "expected output"); ▶ the es and fr commands (real outputs from
`assets/terminal/expected/`). Then honestly: "when we recorded this, Google refused us": the real
429 traceback (assets `10-run-default.txt`), V8: read the *first* exception — `Unexpected status
code "429"` = Google's unofficial endpoint throttling this IP; the RuntimeError on the last line is
the code's friendly wrapper (cli.py 32-37). Same wrapper hides a typo: `-d xx` → first exception
`ValueError: invalid destination language` (assets `14-badlang.txt`) under the same network-sounding
message. What to do: wait and retry, another region, or run it on your laptop — your environment
is fine if you got as far as `Input:`.

**S07 · Delete, don't stop (~160).** README: delete the VM after each walkthrough. V1 coda: Stop
ends CPU/RAM billing but the disk (and a reserved IP) keep billing; Delete with "delete boot disk"
ticked ends both. Checklist: VM instances empty, Disks empty. Optional extra (not in the README):
`gcloud compute instances list`. End of part 1: "In part 2: the same app, the clean way."

**S08 · What a virtual environment is (~300).** Back to PONDER 1: two projects, two httpx versions
— the fix is a separate toolbox per project. V2 continued: a venv is (1) `bin/python`, a symlink to
a real interpreter, (2) its own empty `site-packages`, (3) `pyvenv.cfg` with
`include-system-site-packages = false`. Same engine, different toolbox. What a venv does not
isolate: the OS, system libraries, drivers (that's for containers and VMs). We'll *see* these three
files after `uv sync` (S11/S12 show the real `.venv` listing and `pyvenv.cfg`).

**S09 · Installing uv (~280).** New VM (README step 1-6 again, fast montage with the tracker: same
commands, real outputs, "you know these now"). ▶ `curl -LsSf https://astral.sh/uv/install.sh | sh`:
the four flags in one line each, and the pipe (you are running a script from the internet: it's
the official installer; read it first if you like). Real output: "downloading uv 0.13.0 … installing
to /home/student/.local/bin … everything's installed!". ▶ extra `uv --version` → `uv: command not
found`. Why: V3 doors — the shell only knows the PATH it started with. ▶ `source
$HOME/.local/bin/env` → `uv 0.13.0`, `which uv` → `~/.local/bin/uv`. Why `source` and not `sh`: it
changes *this* shell. uv in one sentence: one fast tool that replaces venv + pip + pip-tools +
pyenv (+ pipx).

**S10 · uv sync: which Python? (~320).** `pyproject.toml` panel (all 10 lines; focus line 6
`requires-python = ">=3.13"`, lines 7-10 dependencies). PONDER 2 (8 s): "This VM has Python 3.11.
The project asks for 3.13 or newer. What will uv sync do?" ▶ `uv sync` — first three output lines
(real): "Downloading cpython-3.15.0 … (35.9MiB) / Using CPython 3.15.0 / Creating virtual
environment at: .venv". V4. A constraint is not a pin: the newest Python in range, 3.15.0 at the
time of recording; a week ago it would have been 3.14. Debian 13 branch: `Using CPython 3.13.5
interpreter at: /usr/bin/python3` (real). To make it deterministic: `uv python pin 3.13` writes
`.python-version` (extra, not in the README).

**S11 · uv sync: resolve, lock, install (~340).** The rest of the real output: "Resolved 13
packages … Installed 11 packages" and the 11 `+` lines. PONDER 3 (6 s) before revealing the
count: "pyproject.toml lists 2 dependencies. How many packages will be installed?" V5 with the
real `uv tree`. Why 11 here and 12 on Debian 13: `typing-extensions` is only needed below Python
3.15 (the lock keeps the marker; real `uv.lock` excerpt lines with `marker = "python_full_version
< '3.15'"`). ▶ extra `ls -a` → `.venv` and `uv.lock` appeared; `git status` → `uv.lock` untracked.
Erratum, kindly: the README says uv.lock pins exact versions for the next person, but the repo never
committed one, so every student's first `uv sync` resolves fresh. In your own projects: commit
`uv.lock`, and use `uv sync --locked` in CI. Re-running `uv sync` is instant ("Checked 11 packages
in 0.14ms"): idempotent.

**S12 · Activation is just PATH (~320).** Real `.venv/bin` listing: `activate` (not executable),
`python -> …/cpython-3.15…/python3.15` (the symlink from S08), no `pip`. Real `pyvenv.cfg`. ▶
`source .venv/bin/activate`: prompt becomes `(app) student@…` — note the README shows
`(simple-translate)`; uv takes the name from `name = "app"` in pyproject.toml. V3: the GREEN
`.venv/bin` door slides in front (real activate lines 97-98: `_OLD_VIRTUAL_PATH="$PATH"`,
`PATH="$VIRTUAL_ENV/bin:$PATH"`). Extra checks: `which python` → `.venv/bin/python`, `python
--version` → 3.15.0, `which pip` → nothing: uv venvs ship no pip; use `uv add <pkg>` (records it
in pyproject.toml and uv.lock). ▶ The three README runs with `python cli.py` (expected outputs).
Two ways without activating: `uv run python cli.py`, `.venv/bin/python cli.py`. Why `source`, not
`./activate`.

**S13 · Prove the isolation (~160).** Extra: `deactivate`, then `python3 -c 'import googletrans'`
→ `ModuleNotFoundError` (real): the packages exist only inside `.venv`. V2: the system
interpreter's shelves have no GREEN jar. `uv run python -c 'import googletrans, sys;
print(sys.prefix)'` → `/home/student/simple-translate/.venv` (real). PONDER 4 (6 s): "Same import,
on your part-1 VM after deactivate: does it work?" → yes, from the ORANGE `/usr/local` shelf.

**S14 · The older way: pipenv (~140).** The repo's `pipenv` branch (and the AWS track,
cheese-app-v0's api-service) use pipenv. A two-column morph: `pyproject.toml` ↔ `Pipfile`,
`uv.lock` ↔ `Pipfile.lock`, `.venv/` in the project ↔ `~/.local/share/virtualenvs/<name>-<hash>`,
`source .venv/bin/activate` ↔ `pipenv shell` (a subshell; `exit` to leave), `uv sync` ↔
`pipenv install` / `pipenv sync`. Same ideas, different names.

**S15 · Tear down, recap, what's next (~260).** ▶ Delete the VM (tracker step 12). V7: VM ⊃ venv,
and the dashed container between them solidifies as the teaser: in L2, `Dockerfile.txt` runs the
same `uv sync` inside an image (panel `Dockerfile.txt` lines 21-29; note in passing that its base
image is Python 3.12 while the project wants ≥ 3.13 — "watch what uv does there"). Recap questions
(5, on screen one at a time, answers in exercises.md): what `--break-system-packages` breaks and
where `sudo pip3` put files; the three parts of a venv; what activation changes + two ways to run
without it; why 2 dependencies became 11 packages and which file makes everyone get the same ones;
is `>=3.13` a pin, what would make the Python version deterministic. Point to the study guide and
exercises in MLOps_Learning.

## Errata to state (kindly, with the fix)

1. `uv.lock` is promised (README lines 12, 70) but not committed → commit yours; `--locked`.
2. The prompt is `(app)`, not `(simple-translate)` (README line 92) → it's `name` in pyproject.toml.
3. "`python` and `pip` resolve to the venv's binaries" (README line 92): a uv venv has no pip →
   `uv add`.
4. `requires-python = ">=3.13"` is a constraint; uv may download a newer Python than you expect.
5. `cli.py` 32-37 wraps every error, even a typo in a language code, in a message about the network.

## Things never to do on screen

No Google/GCP logos or screenshots (schematic console only, tagged `illustration`); no real
person's name; no hand-typed "output" that isn't in `assets/terminal/`; no command that differs
from the README's spelling.
