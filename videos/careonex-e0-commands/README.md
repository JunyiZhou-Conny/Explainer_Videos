# CareOneX E0 · Decoding the start-up commands

*Every word of the two command blocks that start the CareOneX voice app, for a complete beginner.*
Part of [CareOneX, layer by layer](../careonex-series/SERIES.md); watch this one first. About 9
minutes, no narrator: English on screen, bilingual subtitles (中文 above, English below) burned in.

**Watch:** `output/careonex-e0-commands.zh-en.mp4`.

**Sources:** Marco's two command blocks (team chat, 2026-10-10; the Knowledge Base ID is masked because
this repository is public); `nadirbt/careonex-agents` `data-retrieval@d96a4ad` and
`feat/sonic_with_rag@eff4a96`; `TEAM_SETUP.md`. We have no access to the team's AWS account, so every
claim carries a tag: READ IN CODE · TEAM NOTES · MEASURED · INFERRED (with the reason).

| # | Line(s) | What you learn |
| --- | --- | --- |
| 1–2 | the two blocks | two programs: retrieve (a search server, in Docker) and voice (talks to you, on the laptop) |
| 3 | `cd …` | the project folder; why we think it is Marco's copy of the team repository (inferred) |
| 4 | `$env:NAME = "value"` | environment variables: sticky notes a window gives to every program it starts |
| 5 | `AWS_PROFILE`, `aws sso login` | the team's AWS account, SSO sign-in, the AC215 permission set, 8-hour keys |
| 6 | `AWS_DEFAULT_REGION` | regions; everything is in us-east-1 |
| 7 | `$env:HOME = $HOME` | why Windows needs it for `docker compose` (inferred from docker-compose.yml) |
| 8 | `CAREONEX_KB_ID` | what a Knowledge Base is; how retrieve finds its ID; our two guesses, then Marco's branch settles it: a staging test library (read in code) |
| 9 | `docker compose up --build retrieve` | images, containers, compose, ports |
| 10 | `CAREONEX_RETRIEVE_URL`, `CAREONEX_VOICE_SEARCH_MODE` | 127.0.0.1:8080; the search mode: 0 hits on GitHub that morning (measured), then read in Marco's branch: `feedback` (default) or `baseline` |
| 11 | `uv run … python -c "…"` | uv, Python 3.12, the `mic` extra, and why `run()` is called directly (inferred) |
| 12 | — | the whole picture, a cheat sheet of every new term |

**Open questions this episode raised, and what Marco's branch (`feat/sonic_with_rag_updated@1591ed2`,
pushed the same evening) settled:**

- what `CAREONEX_VOICE_SEARCH_MODE=feedback` does: **settled** (S10, E6). Voice reads it in
  `nova_sonic/tools.py`, default `feedback`; `baseline` turns the extra search off.
- why the KB ID is set by hand: **settled** (S08, E6). It is Marco's hierarchical staging Knowledge Base
  (library C of his A/B/C chunking test); his README calls it "example staging KB".
- whether `uv run careonex-voice` fails under SSO: **still inferred**. `main()` on his branch still checks
  only for env keys or `~/.aws/credentials`, which is why calling `run()` directly makes sense (S11).
