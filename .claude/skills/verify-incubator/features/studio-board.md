# Studio progress board and library

Conny follows production on the Studio site, not in chat. The board (`index.html`) shows how many
episodes are in production, queued, paused or waiting on him, what he must do next (for example the
publish-worker command to copy), a per-series course map, and a card with a stage bar per
episode in production. The library (`library.html`) lists every released video with its
Bilibili status and download link. Both pages read only `data/status.json` and
`data/library.json`, which `tools/studio_status.py` builds from the episode issues and the catalog.

## Sub-features

- `board-stats` shows five stat tiles: 制作中, 排队, 暂停, 等你处理, 已上 B 站.
- `board-attention` shows the 需要你处理 section with each waiting episode's next action.
- `board-map` shows the 课程地图 course map, one square per lecture, coloured by state.
- `board-cards` shows one card per episode in production, with a stage bar labelled `当前阶段：…，约 N%`.
- `board-fresh` shows 数据更新于 <time>, the age of the data.
- `library-list` lists the videos, with the totals line `N 个视频 · M 个已上 B 站 · 共 …`.

## How to get to it (user POV)

- Open the deployed GitHub Pages site (rebuilt by `.github/workflows/pages.yml` on every issue label or comment).
- Choose `制作进度` or `视频库` in the top navigation.
- Build it locally: `python3 tools/studio_status.py --out site/data`, then serve `site/`.

## Driving it with control.py

Preconditions:

- `$C studio-up --run $RUN` printed `READY http://127.0.0.1:<port>/ (pid …, N episodes on the board)`.
- `$C doctor --run $RUN` reports `studio server is this run's` as `OK`.

- **Board and library.** Run the journey. Run `$C browse --run $RUN --name board .claude/skills/verify-incubator/features/steps/board.json`.
  Every step prints `ok` and the exit code is `0`. It checks the `制作进度` heading, the `数据更新于` freshness line,
  at least five `a.stat` tiles, the `课程地图` section, at least one stage bar, then follows the `视频库` link and checks
  the `视频库` heading, the `个视频` totals and at least one `article.vid`.
- **Proof.** Look at the artifacts. Open `evidence/board-board.png` and `evidence/board-library.png`. Compare the stat
  tiles in `board-board.aria.txt` (e.g. `link "5 制作中"`) with the counts that `evidence/studio-build.stdout` printed
  (`status: N episodes (K in flight)…`), and with `evidence/studio-status.json`.
- **Data change.** When the change is to `tools/studio_status.py`, also rebuild from the saved payloads and compare. Run
  `$C cli --run $RUN --name rebuild -- python3 tools/studio_status.py --snapshot outputs/verify/$RUN/evidence/studio-snapshot.json --out outputs/verify/$RUN/work/rebuild --now <generated_at from studio-status.json>`.
  Exit code `0`. `rebuild/status.json` differs from `evidence/studio-status.json` only where the change intends.

## Gotchas

- Live mode reads today's issues. Counts and cards change between runs, so assert structure, not numbers.
  For a before/after comparison, build both sides from one `--snapshot`.
- The live build calls the GitHub REST API, about 100 requests. The cloud container's proxy authenticates them.
  Elsewhere, set `GH_TOKEN`, or use `--snapshot`. `--offline` gives an empty board (library only), so the
  board journey fails there by design.
- The 复制 buttons write to the clipboard, which headless Chromium does not grant. Assert the command text
  in the ARIA snapshot (`code: python3 tools/publish_worker.py --repo … --upload`) instead of clicking.
- Card links go to github.com. Do not follow them in a proof.
