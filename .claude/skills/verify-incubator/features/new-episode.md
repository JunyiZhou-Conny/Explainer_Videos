# Scaffold a new episode

A user starts an episode with one command. It creates `videos/<slug>/` with the saved production
defaults (`episode.json`), a storyboard skeleton and a frozen snapshot of the chosen style preset.
The command refuses to touch a slug that already exists.

## Sub-features

- `scaffold-defaults` writes `episode.json` from `skill-library/conny-explainer-video/defaults.json`
  (today: preset `3b1b`, 300 s, 1920×1080 at 30 fps, English `af_heart` at 0.95).
- `scaffold-preset` honours `--preset`, `--minutes` and `--narration-language` overrides.
- `scaffold-snapshot` copies the preset to `style.md` and records its sha256 as `style_sha256`.
- `scaffold-refuse` exits non-zero without writing when the slug exists.

## How to get to it (user POV)

- Run `python3 skill-library/conny-explainer-video/scripts/new_episode.py <slug> --topic "<topic>" [--preset <name>] --workspace .`.
- Ask an agent to start an episode. The skill runs the same command.

## Driving it with control.py

Preconditions:

- Baseline preconditions in `README.md` hold.
- No `videos/verify-$RUN*` folder exists (doctor's last line says `clean`).

- **Scaffold.** Create a verification episode. Run
  `$C cli --run $RUN --name scaffold -- python3 skill-library/conny-explainer-video/scripts/new_episode.py verify-$RUN --topic "Why is a git branch almost free?" --workspace .`.
  Exit code `0`. Stdout is `Brief created. Author script.json and matching scenes.py, then render a sample.`
- **Read it back.** Inspect what was written. Run
  `$C cli --run $RUN --name scaffold-read -- python3 -c "import json,hashlib,sys; d='videos/verify-$RUN/'; e=json.load(open(d+'episode.json')); print(sorted(__import__('os').listdir(d)), e['preset'], e['duration_seconds'], e['video'], e['narration'], hashlib.sha256(open(d+e['style_snapshot'],'rb').read()).hexdigest()==e['style_sha256'])"`.
  Stdout lists `['episode.json', 'storyboard.md', 'style.md']`, the defaults' preset and duration, and ends with `True`.
- **Override.** Scaffold with flags. Run
  `$C cli --run $RUN --name scaffold-swiss -- python3 skill-library/conny-explainer-video/scripts/new_episode.py verify-$RUN-swiss --topic "x" --preset swiss --minutes 3 --workspace .`.
  Exit code `0`. `videos/verify-$RUN-swiss/episode.json` has `"preset": "swiss"` and `"duration_seconds": 180.0`,
  and its `style.md` equals `skill-library/conny-explainer-video/presets/swiss.md`.
- **Refuse.** Repeat **Scaffold** with `--name scaffold-again`. Exit code `2`. Stderr ends with
  `Episode already exists; inspect it before editing: …/videos/verify-$RUN`, and the files from
  **Read it back** are byte-identical.

## Gotchas

- This journey writes into the real `videos/` folder, because that is what the command does. The
  slug must start with `verify-$RUN` so that cleanup removes it. Never commit a `videos/verify-*` folder.
- The scaffold has no `script.json` or `scenes.py`, so it cannot be rendered. "Brief created" is the
  whole proof.
- `tools/check_incubator.py` hashes every `videos/*/episode.json` style snapshot. Run it only after cleanup.
