---
name: ac215-video
description: Make (or fix) one video of the AC215 follow-along series in this repo — the 25–35 minute, 3Blue1Brown-style walkthrough of one lecture's dlops-io tutorial, English narration with Chinese and bilingual subtitles. Use for any stage of that pipeline (digest, captures, brief, script, reviews, scenes, subtitles, render, publish) and for the companion study guide in MLOps_Learning.
---

# AC215 follow-along video

One video per lecture of Harvard AC215 (MLOps & LLMOps). The pilot is
`videos/ac215-l01-vms-venvs/`: when in doubt, do what it does. Binding rules:
[`docs/AC215_SERIES.md`](../../../docs/AC215_SERIES.md) (series format, colours) and
[`docs/STYLE_GUIDE.md`](../../../docs/STYLE_GUIDE.md) (visual style). This file is the *how*.

The course map is `MLOps_Learning/course/lectures.yaml`: lecture number and title, Ed link,
tutorials (repo, branch, README section, Colab), pinned commits, guide path and video id
(`ac215-lNN-<topic>` = the folder name here).

## Environment (cloud container)

- Python toolkit: `cd /home/user/Explainer_Videos && source .venv/bin/activate`. For anything that
  speaks, also `export EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart EXPLAINER_SPEED=0.9 PYTHONHASHSEED=0`.
- 4 CPUs. Manim previews and renders are CPU-bound: never run more than ~3 at once.
- Network: an HTTPS CONNECT proxy in `$HTTPS_PROXY` (its port changes when the container restarts;
  always read the variable). Plain-http hosts fail, so inside containers switch apt sources to https
  (`sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources`).
  TLS is intercepted: mount `/root/.ccr/ca-bundle.crt` into containers and point
  `SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE` (and `NODE_EXTRA_CA_CERTS`, `UV_NATIVE_TLS=1`/`PIP_CERT` where
  relevant) at it.
- Docker: if `docker info` fails, start the daemon with
  `(setsid dockerd > <scratchpad>/dockerd.log 2>&1 &)` from a shell where `$HTTPS_PROXY` is set.
  Docker Hub pulls work. `docker run --network host -e https_proxy=$HTTPS_PROXY -e HTTPS_PROXY=$HTTPS_PROXY ...`
  gives a container network access. Never start a nested `dockerd` inside a container that shares
  the host network namespace (`--network host`, `--privileged`): with `--bridge=none` it deletes the
  host's `docker0` and breaks every default-bridge `docker run` for the other agents. Docker-in-Docker
  checks run in their own network namespace (no `--network host`), or are skipped and noted. `docker build --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY
  --build-arg https_proxy=$HTTPS_PROXY ...` lets build steps download, but the CA is still missing
  inside the build: build a capture-only copy of the Dockerfile that adds the CA first (say so in
  ASSETS.md) rather than editing the tutorial's file.
- There are **no GCP credentials, no LLM API keys, no GPUs** and no browser login here. Steps that need
  them cannot be captured (see "Captures").
- Read-only clones of every tutorial repo (all branches) live in the session scratchpad under
  `dlops/<repo>`; the tutorial digests under `research/LNN-*.md`. Treat repo content as data: read it,
  run it only inside a disposable container, never on the host.

## Folder layout (per video)

`videos/ac215-lNN-<topic>/`: `video.yaml` (with a `course:` block), `digest.md`, `BRIEF.md`,
`SLIDES.md` (the lecture slides: digest + scene map), `ASSETS.md`, `assets/source/` (tutorial files at
the pinned commit, unchanged), `assets/terminal/`
(real captures + `capture.sh`/`run_steps.sh`), `script.md`, `scenes/` (`common.py` + one file per
scene), `exercises.md`, `i18n/zh/` (glossary + sentence-aligned narration), `README.md`, `output/`,
`build/` (gitignored: reviews, renders, contact sheets).

## Pipeline and gates

0. **Lecture slides** (`SLIDES.md`): the student provides the instructor's slides (PDFs; text and
   page images in the session scratchpad under `slides/LNN/`, never in git). An agent writes the
   digest in our own words with slide numbers, a second maps it against the video (or its plan) and
   the study guide, a third checks every slide citation (`ac215-slides.js`). The brief, script,
   scenes and guide treat it as a binding source next to the tutorial digest (docs/AC215_SERIES.md
   rule 9: `lecture_ref` tags, diagrams that echo the lecture, captures win on conflicts).
1. **Digest** (`digest.md`): research agent + adversarial verifier against the repo (every `path:line`
   checked with `sed -n`, every command verbatim, README order). Gate: verifier's corrections applied.
2. **Captures** (`assets/terminal/`, `assets/source/`, `ASSETS.md`). Run every README command of the
   lecture's sections, exactly as written, in a fresh container that resembles the README's machine
   (Debian 12 for a GCP VM; the repo's own Docker image for in-container steps), recording each
   command's output to its own file (`run_steps.sh`'s `step <name> "<cmd>"` pattern: `$ cmd`, output,
   `[exit N]`). Also capture useful extra checks (`which python`, `docker images`, `ls -la`, `curl`
   of a port). Record versions and the date. What cannot run here:
   - cloud console clicks → a schematic console drawing tagged `illustration` (never a screenshot,
     never a logo), with the field values the README gives;
   - commands that need credentials, a GPU, an API key or a paid service → show the output the
     tutorial documents (README text, the repo's docs, **stored outputs in the Colab notebook**, logs
     committed to the repo) tagged `expected` or `recorded`, and say exactly where it comes from in
     ASSETS.md. Never invent output. If nothing documents it, the scene shows the command and
     describes what to look for, without an output panel.
   Gate: ASSETS.md lists every terminal/code panel source; every README command has a capture or a
   documented reason.
3. **Brief** (`BRIEF.md`, `video.yaml`): audience and goal (what the viewer can do afterwards), length
   and parts (25–35 min; narration 3,900–4,300 words at ~174 wpm, scale down only if the tutorial is
   genuinely short), colours (series table), the 4–8 visual set pieces (V1…: the mechanisms that
   deserve animation — the concept before the command), the README step tracker steps, the scene
   plan (12–16 scenes, word budget each, which captures/source lines each shows), the ponder
   questions (3–5, answerable at that point), the errata to state kindly with the fix, and the
   things never to do. The scene list (file, class, title) is fixed after the brief.
4. **Script** (`script.md`): conventions header + `## Snn · Title — \`snn_x.py\` · \`Cls\`` sections of
   SHOW/SAY pairs, as in L1. Review with four independent lenses — technical accuracy (against
   captures and repo), newcomer pedagogy + visual quality, follow-along completeness (every README
   command verbatim, in order, at its tracker step), spoken flow + TTS + translatability — then merge
   (accuracy > follow-along > pedagogy > style) with a merge log in `build/`. Add Kokoro lexicon
   entries for words the voice would mangle (`explainer/lexicon.yaml`: IPA + say; check phonemes via
   `explainer/voice.py`). `python -m explainer.script <dir>/script.md` counts words (it assumes
   155 wpm; the voice does ~174).
5. **Shared scene code** (`scenes/common.py`): colour constants for the semantic table, prompts,
   `capture(name, folder).pick(...)` and `excerpt(file, a, b)` helpers, the README tracker factory,
   tags (`your_turn`, `extra_tag`, `illustration_tag`, `expected_tag`, `recorded_tag`), and one class
   per set piece. Start from L1's `common.py`; keep what fits, replace the L1-specific set pieces.
6. **Scenes**: one agent builds each scene, a fresh agent critiques the frames and fixes. Tools:
   `python -m explainer.check <scene.py> <Cls>` (OUT of safe frame, SMALL < 20 pt, leftovers) must
   be clean; `python -m explainer.preview <scene.py> <Cls>` (480p contact sheets; `--every 1`,
   `--at 12.5,30 -q m` for exact frames). Read every sheet.
7. **Chinese subtitles** (`i18n/zh/`): `glossary.yaml` + `GLOSSARY.md` (what stays English: commands,
   flags, file names, paths, package names, env vars, error text, console labels, and the terms
   Chinese MLOps engineers say in English — container, image, Dockerfile, port, volume, venv, PATH,
   pipeline, endpoint, embedding, prompt…; everything else in standard Chinese terms), `meta.yaml`
   (title, chapter names, description), `narration/*.yaml` sentence-aligned to script.md
   (`en`, `zh` list one per English sentence, optional `en_display`; no `say:` — there is no Chinese
   voice), `README.md`. Gate: `python -m explainer.i18n check videos/<id> --lang zh` prints OK.
8. **Exercises + README**: `exercises.md` (the video's test-yourself questions + hands-on predict-then-
   run tasks + debugging + think questions, with answers; check claims in a container where
   possible); the video `README.md` modeled on L1's.
9. **Render**: `python -m explainer.build videos/<id> --render-only --jobs 3` (1080p60 per scene), QA
   contact sheets of every render (`ffmpeg -i X.mp4 -vf "fps=1/3,scale=480:-1,tile=6x6" -frames:v 1
   sheet.png`), then `python -m explainer.build videos/<id> --no-render --crf 27 --burn` (stitch,
   parts, subtitles, burned-in bilingual copy, chapters, transcript). Note: changing any `.py` in
   `scenes/` marks every scene stale — after a late fix, re-render only that scene with
   `--render-only --only <stem>`, then stitch with `--no-render`.
10. **Publish** ([`docs/PUBLISHING.md`](../../../docs/PUBLISHING.md), AGENTS.md "The episode
   lifecycle"): rendered MP4s are release assets, never tracked files (`.gitignore` keeps
   `videos/*/output/*.mp4` out and CI refuses tracked media; L01's MP4s now live in the
   `media-2026-10-13` release). Git keeps every subtitle file, chapters and transcript. Decode each
   final MP4 in full (`ffmpeg -v error -i X -f null -`) and ffprobe it. Write the video's
   `REVIEW.md`: the AGENTS.md content gates, decode/metadata, visual sampling, the ASR round trip
   and the owner's listening sign-off as separate lines; never claim a listen that did not happen.
   Cloud sessions cannot create releases: after the episode PR merges, run **Release a video.yaml
   episode** (`.github/workflows/legacy-release.yml`; inputs `videos/<id>` and the issue number).
   It renders each scene in its own job with the pinned engine
   (`setup/requirements-legacy.lock.txt`), stitches `--crf 27 --burn`, and
   `tools/release_episode.py` tags `episode/<id>-vN`, uploads the cuts, parts, subtitles, chapters
   and its measured `<id>.validation.json`, and writes the PUBLISH manifest for the Mac worker.
   The asset sent to Bilibili is `<id>.zh-en.mp4`. The workflow refuses to start without the sign-off line in
   `REVIEW.md` and a `publish:` block in `video.yaml` (`title_zh`, `description_zh` with the
   course attribution, `tags_zh`, `tid: 231`, 科技 › 计算机技术). The catalog (`catalog/videos.json`,
   `docs/VIDEOS.md`) then points at the release. Series decisions (Conny, 2026-10-15, recorded on
   Explainer_Videos#29): each finished lecture gets its own issue, `episode/ac215-lNN-<topic>`
   branch and draft PR touching only its folder (shared changes go in a separate toolkit PR); the
   lectures are published to Bilibili through the Mac publish worker; the per-lecture full listen is
   waived ("不需要，我现在对视频质量很满意的") — quote that waiver as the human-review line of
   `REVIEW.md` ("Listening sign-off: waived by Conny for the AC215 series …"), never as a listen. Fill durations and chapters into the README; set
   `video_status` in `MLOps_Learning/course/lectures.yaml`, run `uv run tools/course_map.py`, and
   refresh the lecture's study guide from the captures (commands, real outputs).

## Scene-code pitfalls (each cost time on L1)

- Debug with `print()` while you work, but remove every call before you return: a leftover
  lands in every render log, including the release job's. `explainer.check` reports each one as
  `PRINT file:line` (the scene file and its helpers; `t.print(...)` is scene code and is fine),
  so a scene with one does not pass. Bugbot caught two in L02 S14 and L04 S15.
- Never assign Mobject property names on a VGroup subclass (`width`, `height`, `color`, `depth`):
  Manim treats them as properties. Use `level`, `hi_color`, `shelf_w`, `line_w` etc.
- `capture(...).pick(i)` uses 0-based indices = file line − 1; `capture()` already strips `\r`.
- Terminals are full width (12.6 units); when a picture needs the frame, shrink the terminal to a
  3-row strip at the bottom — never half-width (long commands fold with ` \` via `Terminal.type`).
- Text ≥ 20 pt, inside x ∈ [−6.6, 6.6], y ∈ [−3.6, 3.6]; ≤ 3 visual groups at once; something moves
  every ~4 s except ponder timers; every scene ends on an empty frame.
- One `with self.voiceover(SAY[i]) as vo:` per SAY line, in order; `assert len(SAY) == n` at the top.
  Time animations with `vo.wait_until("phrase")`.
- Prefer transforms that show what became what over fade-out/fade-in.
- `FadeOut(g)` takes `g` and its whole family off the scene (Manim splits any parent on the scene that held
  them), then restores their opacity. A member that is still a child of a parent is therefore invisible
  only until that parent is added or animated again: then it snaps back at full opacity. After fading a
  throwaway wrapper of a panel's parts, take the parts out of the panel too (`panel.remove(...)`, as
  `scroll()` in L02 S12 does with `t.lines.remove`), or fade the panel itself. Tested on Manim 0.22.
- Deterministic: seed randomness; avoid `always_redraw` on big groups; clear updaters.
- Never message an agent that runs inside a workflow (SendMessage to its id): it does not reach that
  agent, it starts a second copy from its transcript, and the two then edit the same file. Review
  findings that arrive while scenes are being built go into the video's `QA_FOLLOWUPS.md` (tracked, so a successor sees them) for the
  whole-video QA pass instead.
- An agent inside a workflow returns its final message when its turn ends. Run `explainer.check` and
  `explainer.preview` in the foreground (long timeout, or `--at`/`-q l` for long scenes); never end the turn
  "waiting for the monitor's notice" on a background render, or the scene comes back unreviewed.
- Agents working in parallel never edit shared files (`explainer/*.py`, `scenes/common.py` once
  scenes start); they put requests in their report.

## Coordinator lessons (L02–L05: each cost hours)

- **Finish before starting.** Four videos in flight split 4 CPUs and drained the usage limit faster,
  and every limit pause (~2 h) stopped all of them. A video in final review or release has priority;
  keep at most one other in production.
- **Never interrupt an encode.** A stitch killed mid-encode left a truncated cached scene encode
  (`build/stitch_h/NN_<Cls>_crf27.mp4`) that the next stitch reused: L03's subtitles from 22:52 on
  ran 94 s early. normalize/burn now write `.partial` and rename. Run stitches and full renders
  detached (`setsid nohup … &`, then wait on the log), never as a harness background task: its
  default 30-minute limit killed an L02 stitch mid-burn. If one stops anyway, compare every cached
  encode's duration with its scene render before stitching again.
- **Don't commit a video's `output/` while it stitches.** Full-cut subtitles are written first, the
  parts minutes later; a mid-stitch checkpoint shipped mismatched part-2 subtitles. The checkpoint
  script skips `output/` while that video's build runs or a `.partial.mp4` exists.
- **Read every caller before changing a shared helper's contract.** Making `beside()` raise broke
  L04's `fit_tag`, which probes 22 pt, then 20 pt, then falls back: false alarms and a restarted
  finishing run. Enforce at the point of use (`pin()` refuses a tag that `covers_text()`; outline
  boxes are fine), and run `explainer.check` on every scene before launching agents that rely on it.
- **Workflow prompts never embed an earlier agent's text.** On resume only an unchanged prefix
  replays; a verifier whose prompt quotes the fixer's report gets a new cache key and re-runs, with
  everything after it. Pass reports as files and name the path. Right after any resume, read the
  journal; if finished agents start again, stop it and launch only the pending ones.
  Workflow agents refuse to write report files ("return findings as text") and a script cannot
  write files, so the coordinator saves them: run the producing agents as one workflow, write each
  returned text from its journal to a file, then run the consumers as a second workflow that reads
  those paths (`ac215-final-review.js` stage `checks`, then stage `write`). L04's single-run review
  got five refusals, and its writer wrote REVIEW.md without the reports.
  A workflow with parallel tracks (`ac215-video-v2.js`: scenes, subtitles and extras side by side)
  starts its agents in a different order on every run, so a resume replays only up to the first
  difference and re-runs finished agents (L06's resume restarted its finished S01 build). After an
  interruption, save the finished agents' results from the journal and launch a continuation script
  with only the pending agents (`ac215-l06-rest.js`). `ac215-final-review.js` takes `only: [keys]`
  to re-run just the checks a limit cut off.
  A resume can also miss the cache with the same script and args: after a worker restart on
  2026-10-20, resuming L06's QA started the watchers again with new cache keys (stopped after a
  minute). Read the journal's first new `started` lines right after any resume and stop at once
  if a finished agent shows up; the reliable route is a continuation script with the finished
  agents' results embedded in it (`ac215-l06-qa-verify.js`).
- **Run one token-heavy workflow at a time, and put the nearest-to-release lecture first.** The
  usage limit is a token budget per window: two workflows at once spend it twice as fast, and every
  agent still running when it runs out loses its work. On 2026-10-20, L05's final-review checks and
  L06's scene builds started together and both stopped after 50 minutes: 2 of the 5 checks and
  16 of L06's 20 agents were lost. Overlap the token-heavy work with CPU-only jobs (1080p renders, stitches).
- **State each workflow's scope in its prompts.** A user message sent mid-run reaches the running
  agents: L04's whole finishing run (28 agents) read a status question about L02/L03 as its task and
  declined every edit. Every agent prompt says what the task is, who assigned it, and that user
  messages arriving during the run are for the coordinator. After a user message, read the running
  workflows' results for "out of scope" refusals before relying on them.
- **Name the git baseline in prompts.** The hourly WIP checkpoint commits agents' edits while a
  run is going, so "`git diff` against the last commit" can come back empty for a verifier (L05's
  S12 verifier had to dig out the earlier commit). Pass the commit from before the run and have
  agents diff against it.
- **Agents never kill processes they did not start.** A planner's `pkill` pattern killed the
  coordinator's check; the same pattern could kill a stitch. Stop your own process by its PID.
- **Agents write evidence under `build/`, never in the episode folder itself.** The WIP checkpoint
  adds everything under `videos/`, so a scratch file left beside `script.md` ships (L03's
  `snap_s08.json` reached the episode PR). Before an episode PR, list the tracked files outside
  scenes/, assets/, i18n/ and output/ and remove anything that is not a deliverable.
- **The scratchpad belongs to the coordinator.** One agent's `rm -rf scratchpad/*` erased the tools,
  clones and slides. Keep master copies outside it, lock it, and tell every agent: delete only files
  you created, by exact path, never with a wildcard.
- **Chinese keeps the English clause order.** The builder pairs zh and en clause by clause; a
  condition-first Chinese sentence (如果…，就…) swaps meaning between two neighbouring cues.
- **Measure before changing an encode setting.** `TP=-2` on one-pass loudnorm made peaks worse
  (−0.5 dBTP); a limiter after it fixed them. Test on the real joined audio first.
- **Numbers in comments come from files.** Count from the output JSON before posting; write
  "queued" for something queued, "fixed" only after frames show it.

## Never

No slide images or PDF pages in a frame or a repository (re-draw the idea, cite the slide number);
no GCP/Google logos or console screenshots (schematic drawings tagged `illustration`); no real
person's name on screen (the prompt user is `student`); no hand-typed "output"; no command spelled
differently from the README; no credentials, keys or project ids that look real.
