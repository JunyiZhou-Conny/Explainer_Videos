# Exercises · AC215 L1 — virtual machines, virtual environments and uv

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real captures from
2026-10-12 (`assets/terminal/`); versions on your VM may be newer.

---

## Part A · The five questions from the end of the video

**Q1. What does `--break-system-packages` actually break, and where did `sudo pip3` put the files?**

<details><summary>Answer</summary>

On Debian 12/13 and Ubuntu 24.04 the system Python is *externally managed* (PEP 668): apt owns
its packages in `/usr/lib/python3/dist-packages`, and the OS's own Python tools depend on those
exact versions. pip refuses to touch that interpreter; the flag overrides the refusal. With `sudo`,
pip installed into `/usr/local/lib/python3.11/dist-packages` (the video's
`python3 -c 'import googletrans; print(googletrans.__file__)'` printed
`/usr/local/lib/python3.11/dist-packages/googletrans/__init__.py`). That folder comes **before**
apt's on `sys.path`, so a pip-installed package with the same name as an apt one hides apt's copy,
for every program on the machine. What breaks is the guarantee that the OS's Python tools see the
versions apt tested them with.
</details>

**Q2. Name the three parts of a virtual environment.**

<details><summary>Answer</summary>

1. `bin/python`, a symlink to a real interpreter (on the Debian 12 VM:
   `python -> /home/student/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/bin/python3.15`).
2. Its own `lib/python3.X/site-packages/`, empty at first.
3. `pyvenv.cfg`, with `include-system-site-packages = false`: when Python starts from the venv's
   `bin/`, it reads this file and builds a `sys.path` with the venv's site-packages instead of the
   system's dist-packages.
</details>

**Q3. What exactly does activation change? Name two ways to run the app without it.**

<details><summary>Answer</summary>

`source .venv/bin/activate` saves the old `PATH` and puts `.venv/bin` first
(`PATH="$VIRTUAL_ENV/bin:$PATH"`, lines 97–98 of the generated script), exports `VIRTUAL_ENV`,
prefixes the prompt with `(app)` and defines `deactivate`. It installs and loads nothing; it only
changes where the shell looks first. Without activating: `uv run python cli.py`, or
`.venv/bin/python cli.py`.
</details>

**Q4. `pyproject.toml` lists 2 dependencies. Why were 11 packages installed, and which file makes
everyone get the same ones?**

<details><summary>Answer</summary>

Dependencies have dependencies: `googletrans==4.0.2` needs `httpx[http2]`, which needs `anyio`,
`certifi`, `httpcore` (→ `h11`), `idna` and `h2` (→ `hpack`, `hyperframe`); with `art`, that's 11.
`uv sync` resolved 13 entries: the 11, `typing-extensions` (needed only on Python < 3.15, so skipped
on 3.15 and installed on Debian 13's 3.13: 12 packages there) and the project itself. The file that
freezes the exact versions is **`uv.lock`**. The tutorial repo doesn't commit one, so commit yours
and use `uv sync --locked` in automated builds.
</details>

**Q5. Is `requires-python = ">=3.13"` a pin? What would make the Python version deterministic?**

<details><summary>Answer</summary>

No, it's a constraint with no upper limit. uv uses an interpreter it already has if one fits
(Debian 13's system `3.13.5`), otherwise it downloads the newest release in range (CPython 3.15.0 on
2026-10-12; earlier the same command gave 3.14). `uv python pin 3.13` writes `.python-version`, and
every `uv sync` then uses 3.13.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Which shelf?** On your part-1 VM (the manual install), predict what this prints, then run it:

```bash
python3 -c "import googletrans, sys; print(googletrans.__file__); print(sys.prefix)"
```

Then do the same with `.venv/bin/python` on your part-2 VM.

<details><summary>Answer</summary>

System Python: `/usr/local/lib/python3.11/dist-packages/googletrans/__init__.py` and `/usr`.
Venv Python: `/home/<you>/simple-translate/.venv/lib/python3.15/site-packages/googletrans/__init__.py`
(or `python3.13` on Debian 13) and `/home/<you>/simple-translate/.venv`. Same import, different
shelf, because each interpreter builds its own `sys.path`.
</details>

**B2. Which Python will uv pick?** On a fresh VM, before `uv sync`, run `python3 --version` and
`uv python list --only-installed`. Predict what `uv sync` will use. Run it, then
`cat .venv/pyvenv.cfg`. Then run `uv python pin 3.13` and `uv sync` again.

<details><summary>Answer</summary>

Debian 12 (3.11.2, outside `>=3.13`): uv downloads the newest release in range, and `pyvenv.cfg`'s
`home` points under `~/.local/share/uv/python/`. Debian 13 (3.13.5): uv uses `/usr/bin/python3`
(`home = /usr/bin`). After the pin, `.python-version` contains `3.13`; on Debian 12, `uv sync`
downloads a 3.13.x and rebuilds `.venv` with it. Pinning `3.11` fails, because 3.11 doesn't satisfy
`requires-python`.
</details>

**B3. Make it reproducible.** In your own fork (or a copy), commit `uv.lock`. Then add `"rich"` to
`dependencies` **by hand** (not with `uv add`) and run `uv sync --locked`. Predict the outcome, then
fix it.

<details><summary>Answer</summary>

uv sees that the lock no longer matches `pyproject.toml` and refuses: the lockfile needs to be
updated, but `--locked` was given. Fix: `uv lock` (or `uv sync` without the flag), then commit both
files. This is why later course Dockerfiles copy `uv.lock` and run `uv sync --frozen`.
</details>

**B4. Read from a file.** Create `msg.txt` with two French sentences, then run
`python cli.py -f msg.txt -s auto -d en`. Predict the `Arguments:` and `Input:` lines.

<details><summary>Answer</summary>

`Arguments: Namespace(text='I love cheese', file='msg.txt', src='auto', dest='en')`: `-t` keeps
its default, but `cli.py` lines 19–21 replace the text with the file's contents, so `Input:` shows
your French. A wrong path raises `FileNotFoundError` before any network call, and it isn't wrapped,
because the file is read outside the `try`.
</details>

---

## Part C · Debugging

**C1. "It says the network is down, but it isn't."** `python cli.py -t hello -d xx` ends with
`RuntimeError: Translation request to Google Translate failed (the server's network/IP may be
rate-limited or blocked by Google's unofficial translate endpoint).` Is the network the problem?

<details><summary>Answer</summary>

No. The first exception in the chained traceback is `ValueError: invalid destination language`,
raised by googletrans before any request. `cli.py` lines 32–37 catch every exception and re-raise
one network-flavoured message. Read the **first** exception: it's the cause. (A real network
problem looks like `Exception: Unexpected status code "429" from ['translate.googleapis.com']`.)
</details>

**C2. `pip` inside the venv.** With `(app)` active on your part-2 VM, `pip install rich` gives
`pip: command not found`. On your part-1 VM, inside a venv you made the same way, it gives
`error: externally-managed-environment`. Explain both, and add `rich` properly.

<details><summary>Answer</summary>

A uv-created venv has no `pip` (look at `ls .venv/bin`), so the shell keeps walking `PATH`. The
fresh part-2 VM never installed `python3-pip`, so there's nothing to find. On the part-1 VM it finds
the system `pip`, which belongs to the externally managed system Python. The right way is
`uv add rich`: it updates `pyproject.toml` and `uv.lock` and installs into `.venv`.
</details>

**C3. Activation mechanics.** A classmate runs `./.venv/bin/activate` and gets `Permission denied`.
They try `bash .venv/bin/activate`: no error, but `which python` still prints nothing. Why?

<details><summary>Answer</summary>

`activate` isn't executable (`-rw-r--r--`), and `bash file` runs it in a child shell that changes
its own `PATH` and exits. Activation has to happen in your current shell: `source .venv/bin/activate`.
</details>

**C4. `uv: command not found` right after installing uv.** Why, and what are two fixes?

<details><summary>Answer</summary>

The installer put `uv` in `~/.local/bin`, but your current shell's `PATH` was set before that
folder was added. Either `source $HOME/.local/bin/env` (it prepends `~/.local/bin`), or open a new
SSH tab: the installer appended `. "$HOME/.local/bin/env"` to `~/.profile` and `~/.bashrc`.
</details>

---

## Part D · Think

**D1. Pick the right isolation.** For each case, is a venv enough, or do you need a VM/container?
(a) two projects need different `pandas` versions; (b) your code needs the `libpq` C library and a
particular CUDA driver; (c) a teammate on macOS must reproduce your exact Linux setup; (d) you want
to try risky `sudo apt` changes without endangering your laptop.

<details><summary>Answer</summary>

(a) A venv per project. (b) A venv only isolates Python packages. System libraries and drivers
need a container image (L2) or a VM image. (c) A venv plus `uv.lock` makes the Python packages
identical, but not the OS; a container gives the same Linux userland. (d) A VM: disposable, delete
it when done.
</details>

**D2. Stop or delete?** You stop your VM on Friday and come back two weeks later. What did you pay
for in between, and what would delete have changed?

<details><summary>Answer</summary>

A stopped VM doesn't bill CPU and memory, but its boot disk still exists and bills per GB-month,
and so would a reserved static IP. Deleting it with "Delete boot disk" ticked (the default) removes
both. Then check that **VM instances** and **Disks** are empty.
</details>
