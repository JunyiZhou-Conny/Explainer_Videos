# The AC215 follow-along series

Videos for the tutorials of Harvard's AC215 (MLOps & LLMOps, Fall 2026), one per lecture, made to
be watched **with your own clone open**, pausing to run each command. The study guides, the course
map and the script that clones every tutorial repo live in
[MLOps_Learning](https://github.com/JunyiZhou-Conny/MLOps_Learning). Course materials belong to the
AC215 teaching staff (Harvard IACS); these videos are made for study with the instructor's
permission.

Everything in [STYLE_GUIDE.md](STYLE_GUIDE.md) applies. This page adds what a tutorial walkthrough
needs on top of a paper explainer.

## Folder and files

`videos/ac215-lNN-<topic>/` with the usual `video.yaml` (plus a `course:` block: lecture, Ed link,
repos with branch and commit, guide link), `script.md`, `scenes/`, `exercises.md`, `README.md`,
`output/`, and:

- `digest.md`: the verified tutorial digest (what the tutorial does, every step, code tour with
  `path:line`, gotchas, errata). The study guide in MLOps_Learning is made from it.
- `BRIEF.md`: the video's design (audience, scene beats, colours, word budget), written before the
  script.
- `ASSETS.md` + `assets/`: provenance of everything shown as real.
  - `assets/source/`: the tutorial files the code panels quote, copied unchanged at the pinned commit.
  - `assets/terminal/`: **real terminal sessions**, captured by running the README's commands in a
    fresh container or VM (`capture.sh` + `run_steps.sh` record each command's output to a file).
    Scenes print output from these files; nothing in a terminal panel is typed by hand. Where a
    capture can't be made (a cloud console, a paid service), the panel carries the tag
    `illustration` and ASSETS.md says what it is based on.

## Format rules

1. **Follow-along first.** Every command of the README section appears on screen, typed exactly as
   the README writes it, in the order the README gives. A `ReadmeTracker`
   (`explainer.devops`) is pinned top-left in every walkthrough scene: *README › section › step k
   of N*. Steps the README does not have (useful extra checks such as `which python`) are marked
   `extra` in the tracker caption and in the narration ("this one isn't in the README").
2. **"Your turn" beats.** After a command a viewer must run before the video goes on, a YELLOW
   `▶ your turn` tag appears next to it and the narration says "pause and run it". Use them at
   real checkpoints only (about one per README step), not after every line.
3. **Code panels say where they are.** `code_panel(source, path, first_line, ...)` puts
   `path · lines a–b` on top of the panel, so a viewer can find the same lines in their editor.
   Quote from `assets/source/` with the real line numbers.
4. **Concept before command.** When a command's effect is invisible (PATH lookup, sys.path, a
   lockfile, a port mapping, an image layer), animate the mechanism first, then type the command and
   show its real output confirming what the picture predicted.
5. **Real outputs, honest versions.** Long outputs show their first and last lines with a `…` line
   between. Version numbers that will change ("uv 0.13.0", "Python 3.15.0") are said with "at the
   time of recording". Errata found in the tutorial (README vs code) are pointed out kindly, with the
   fix.
6. **Costs and teardown.** Every scene that creates a billable resource shows a GOLD cost tag; the
   video ends with the teardown checklist.
7. **Length.** 25–35 minutes, cut into two parts at a natural break (`parts:` in video.yaml), each
   part ending on a clean frame. Narration ≈ 3,900–4,300 words at the house voice (Kokoro
   `af_heart`, speed 0.9 ≈ 174 words per minute); typing, output and ponder pauses add the rest.
8. **Chinese subtitles, English voice.** The series is narrated in English only. Every video
   ships English subtitles, Chinese subtitles on the English timing (`<id>.zh.srt`), bilingual
   subtitles (`<id>.zh-en.srt` / `.ass`, Chinese above, English below) and a copy with the bilingual
   subtitles burned in (`<id>.zh-en.mp4`, `python -m explainer.build videos/<id> --burn`). The
   Chinese text lives in `i18n/zh/` (glossary + sentence-aligned `narration/*.yaml`, as in
   `docs/LANGUAGES.md`); there is no Chinese voice and no Chinese on-screen text, so scenes need no
   language changes. Terminal panels and code are never translated.
9. **The lecture behind the tutorial.** Each video folder has `SLIDES.md`: a digest of the
   instructor's lecture slides in our own words, with slide numbers, and a map of which scenes
   stand on which slides (gaps, conflicts and proposals included). The slides are course material
   the student provides for study: the PDFs and slide images never enter a repository or a frame.
   When a scene teaches an idea the lecture covered, a GREY `lecture_ref(n, "a–b")` tag
   (`explainer.devops`, top right) says "Lecture n · slides a–b"; diagrams echo the lecture's
   structure and terms in the series style, and the narration may bridge in one short sentence
   ("this is the namespaces slide from lecture, at your terminal"). Where the slides and today's
   captures disagree, the captures decide what the video shows, and the video says so kindly.

## Series colours (keep across all videos)

| meaning | colour |
| --- | --- |
| your laptop, local machine | GREY |
| the cloud, a VM, a remote machine | BLUE |
| a container / image (from L2) | TEAL |
| shared, OS-owned, system-wide (system Python, apt) | ORANGE |
| project-owned, isolated (a venv, a lockfile, pinned versions) | GREEN |
| a tool you install (uv, docker, gcloud …) | PURPLE |
| an error, a failure, something to avoid | RED |
| "your turn", the README tracker, the thing to look at now | YELLOW |
| money: billing, cost tags | GOLD |
| lookups, paths, network routes | PINK |

## Production pipeline (per video)

1. Digest (research agents + adversarial verification) → `digest.md`.
2. Captures: run the tutorial in a container or VM → `assets/terminal/`, `ASSETS.md`.
3. `BRIEF.md` → `script.md` (SAY/SHOW) → review lenses: technical accuracy against the repo and
   the captures; a newcomer's pedagogy; follow-along completeness (is every README command there,
   exact, in order?); spoken flow + translatability → merge.
4. Scenes (one agent per scene, `explainer.devops` + the video's `scenes/common.py`), previews and
   `explainer.check`, an independent frame review.
5. Translate the narration for the Chinese subtitles (`i18n/zh/`: glossary, sentence-aligned
   narration, `python -m explainer.i18n check`), then render English with `--burn`; write
   `exercises.md` and `README.md`.
6. Update the course map in MLOps_Learning (`video_status` in `course/lectures.yaml`).
