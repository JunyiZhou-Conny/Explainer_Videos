# AC215 · Lecture 1 — Virtual machines, virtual environments and uv

A follow-along walkthrough of the Lecture 1 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**: [dlops-io/simple-translate](https://github.com/dlops-io/simple-translate) (`main` @
[`62f821b`](https://github.com/dlops-io/simple-translate/tree/62f821bfe09fc1c2ecb0f14354b1f205777c0efa)),
sections *Installing App on VM Manually* and *Installing App on VM using UV*. Watch it with the
README open and a VM of your own, and pause at every `▶ your turn` to run the command. Series
format: [`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L01-vms-venvs.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L01-vms-venvs.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l01-vms-venvs.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, 29:52, 85 MB |
| `output/ac215-l01-vms-venvs.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player |
| `output/ac215-l01-vms-venvs_part1.mp4` | part 1, 14:01: a cloud VM and the quick-and-dirty install (S01–S07) |
| `output/ac215-l01-vms-venvs_part2.mp4` | part 2, 15:51: virtual environments with uv (S08–S15) |
| `output/ac215-l01-vms-venvs.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l01-vms-venvs.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l01-vms-venvs.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, hands-on predict-then-run tasks, debugging, and a few think questions, with answers |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (fresh Debian 12 and 13 containers, 2026-10-12); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commit |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

## Chapters

Paste-ready in `output/chapters.txt` (and `chapters_part1.txt`, `chapters_part2.txt` for the parts).

```
00:00 Why won't pip install?
01:34 The app: cli.py
03:34 Renting a computer: the VM
05:57 apt, git and the repo
07:39 The system Python and PEP 668
10:53 Run it, and read the traceback
12:58 Delete, don't stop
14:01 What a virtual environment is
15:48 Installing uv
18:03 uv sync: which Python?
20:37 uv sync: resolve, lock, install
23:23 Activation is just PATH
25:55 Prove the isolation
27:10 The older way: pipenv
28:16 Tear down, recap, and what's next
```

## What you'll learn

Four *pause and ponder* moments ask you to predict before the video shows you: two projects that
need different httpx versions on one machine, which Python `uv sync` will use on a VM that has
3.11, how many packages two dependencies turn into, and whether the import still works after
`deactivate`. Five test-yourself questions close the video (answers in `exercises.md`).

**Part 1 · a cloud VM and the quick-and-dirty install**

1. **Why won't pip install?** The `externally-managed-environment` error, line by line, and the
   two kinds of "virtual" this lecture is about.
2. **The app** — `cli.py`: argparse options and their defaults, googletrans 4's asynchronous
   call (one HTTPS request to Google's unofficial endpoint), and the lines that will fool us later.
3. **Renting a computer** — a Compute Engine VM: region, machine type, boot disk, what it costs
   while it runs; SSH in.
4. **apt, git and the repo** — `apt-get update` vs `apt install`, cloning the repo, and what's
   in it (and what isn't: no lock file).
5. **The system Python and PEP 668** — `sys.path` as shelves, why apt owns the system Python,
   what `--break-system-packages` breaks, and where `sudo pip3` put the files.
6. **Run it, and read the traceback** — the README's three runs; a chained traceback (a 429
   from Google wrapped in the app's own network message): find the first error, not the last.
7. **Delete, don't stop** — a stopped VM still bills its disk.

**Part 2 · virtual environments with uv**

8. **What a virtual environment is** — three parts: a link to an interpreter, its own
   `site-packages`, and an `activate` script.
9. **Installing uv** — `curl … | sh`, `~/.local/bin`, "command not found" and PATH, `source`
   vs `sh`, and what uv replaces.
10. **`uv sync`: which Python?** — `requires-python = ">=3.13"` is a constraint, not a pin; uv
    downloads a Python when the VM's is too old.
11. **`uv sync`: resolve, lock, install** — 2 dependencies become 11 packages; `pyproject.toml`
    vs `uv.lock`, and `--locked`.
12. **Activation is just PATH** — the prompt, `which python`, no `pip` in a uv venv, and two
    ways to run the app without activating.
13. **Prove the isolation** — the same import from the system Python, through `uv run`, and on
    the part-1 VM.
14. **The older way: pipenv** — `Pipfile` / `Pipfile.lock` on the tutorial's `pipenv` branch, side
    by side with uv.
15. **Tear down, recap, and what's next** — delete the VM and its disk; containers in Lecture 2.

The README's small mistakes are pointed out kindly, with the fix: `uv.lock` is promised but not
committed (commit yours, use `uv sync --locked`); the prompt says `(app)`, not
`(simple-translate)` (it comes from `name` in `pyproject.toml`); a uv venv has no `pip` (use
`uv add`); and `cli.py` reports every error, even a mistyped language code, as a network problem.

## Rebuild

```bash
python -m explainer.build videos/ac215-l01-vms-venvs -q l                 # fast draft
python -m explainer.build videos/ac215-l01-vms-venvs --crf 27 --burn      # 1080p60 + subtitles + burned-in copy
python -m explainer.build videos/ac215-l01-vms-venvs --subs-only          # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l01-vms-venvs --lang zh       # Chinese text aligned with the English
```

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); this video is made for study
with the instructor's permission. The cloud console shown is a schematic drawing (tagged
`illustration`), not a screenshot.*
