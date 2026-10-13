# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

## `source/` — the tutorial's own files

`cli.py`, `pyproject.toml`, `Dockerfile.txt` and `README.md` from
[dlops-io/simple-translate](https://github.com/dlops-io/simple-translate) at commit
`62f821bfe09fc1c2ecb0f14354b1f205777c0efa` (main, 2026-09-08), copied unchanged so the code panels
quote the exact lines a viewer sees in their own clone. Course material by the AC215 teaching
staff (Harvard IACS), used for study with the instructor's permission.

`source/pipenv-branch/Pipfile` and `Pipfile.lock` come from the same repo's `pipenv` branch at
commit `3a354d81f787a064aea3ab061359c9a1e223e4d5` (S14 quotes its pinned `httpx` version).

## `terminal/` — real terminal sessions

Captured on 2026-10-12 by `terminal/capture.sh`: a fresh `debian:12` (or `debian:13`) container
per walkthrough, given the baseline a Compute Engine Debian image already has (`python3`, `sudo`,
`curl`, a user with passwordless sudo, called `student`), then `terminal/run_steps.sh` runs the
README's commands one by one and saves each one's output. Each file starts with the command
(`$ ...`) and ends with its exit status (`[exit N]`).

| folder | what |
| --- | --- |
| `debian12-part-a/` | walkthrough 1, *Installing App on VM Manually*, Debian 12 (Python 3.11.2, pip 23.0.1) |
| `debian12-part-b/` | walkthrough 2, *Installing App on VM using UV*, Debian 12 (uv 0.13.0 downloads CPython 3.15.0) |
| `debian13-part-b/` | walkthrough 2 on Debian 13 (uv uses the system CPython 3.13.5) |
| `expected/` | the three `cli.py` runs as they look when Google answers (see below) |

Differences from a real Compute Engine VM, and how the scenes handle them:

- **Package lists.** A container starts from a smaller base than a GCP image, so
  `apt install git` / `python3-pip` pull in more packages here than on a VM. Scenes show the start
  and the end of those outputs, with a `…` line in between; the narration says the exact list
  varies.
- **Interactive apt.** The capture pipes `yes` into `apt install` (no terminal). Scenes show the
  README's command, `sudo apt install git`, and the `Do you want to continue? [Y/n]` prompt answered
  with `Y`, as on a VM. Without a terminal apt also leaves out the ` Done` it prints at the end of
  its progress lines (`Reading package lists... Done`); scenes put it back.
- **`26-startup-files.txt`** (part B) was captured in a second run of the same image, after the
  uv installer: the lines it appended to `~/.profile` and `~/.bashrc`, and `~/.local/bin/env`.
- **The translation itself.** Google's unofficial endpoint answered the part-A runs
  (`debian12-part-a/10-12`, system Python, captured first) with HTTP 429 ("too many requests"),
  and S06 teaches that real failure. A few minutes later the part-B runs from the venv
  (`debian12-part-b/14-16`, `debian13-part-b/14-16`) succeeded, and those are real outputs:
  "I love cheese" → *Adoro il formaggio*; "Good morning. It is a good morning for cheese." →
  *Buen día. Es un buen día para el queso.*; "Good afternoon. Would you like some cheese?" →
  *Bon après-midi. Veux-tu du fromage ?*. `expected/` is the part-A output up to `Input:` plus the
  `Output:` line those runs would have printed (the same translations, `cli.py:39`); the video tags
  those runs "expected output".
- **Versions move.** uv 0.13.0 and CPython 3.15.0 were the newest on 2026-10-12; the narration says
  "at the time of recording" wherever a version number would change for a later viewer.
