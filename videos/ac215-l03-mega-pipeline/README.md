# AC215 · Lecture 3 — Containers II: five containers, one bucket

A follow-along walkthrough of the Lecture 3 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**: [dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline) (`main` @
[`c6bbc9b`](https://github.com/dlops-io/mega-pipeline/tree/c6bbc9ba88984e1234b68ccf5cdf7c00f7e9accc)),
the whole main README (*Clone this Repository*, *Connecting the Pipeline Components*, *GCS Bucket
Details*, *GCP Credentials File*, *Time to Build — The Five Components*, *Quick Reference*,
*Appendix*) and the five component READMEs it sends you to: `transcribe_audio`, `generate_text`,
`synthesis_audio_en`, `translate_text`, `synthesis_audio`. One panel quotes last year's `solution`
branch ([`8083187`](https://github.com/dlops-io/mega-pipeline/tree/8083187ec0e022ba34440892689145ff703a34e0),
`transcribe_audio/docker-shell.sh`) as where the course goes next; it is not followed.

Watch it with the mega-pipeline README and the `transcribe_audio` README open, your own clone,
Docker Desktop and uv from Tutorial 0, the course key from Canvas and your team's group name. The
tracker top left shows the README step; pause at every `▶ your turn` to run the command; a gray
`extra` tag marks a check that isn't in the README. The video was recorded **without the course
key**: wherever the code calls Google, it shows the command and what to look for, not the output.
Series format: [`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L03-containers-2-mega-pipeline.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L03-containers-2-mega-pipeline.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l03-mega-pipeline.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. The only video file committed |
| `output/ac215-l03-mega-pipeline.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Not committed: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l03-mega-pipeline_part1.mp4` | part 1, DURATION_P1: the pipeline, and your first Dockerfile (S01–S07). Not committed: rebuilt with `--no-render` |
| `output/ac215-l03-mega-pipeline_part2.mp4` | part 2, DURATION_P2: packages, the key, and all five components (S08–S15). Not committed: rebuilt with `--no-render` |
| `output/ac215-l03-mega-pipeline.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l03-mega-pipeline.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l03-mega-pipeline.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, hands-on predict-then-run tasks, debugging, and think questions, with answers |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (a fresh Debian 12 "laptop" and Docker Engine 29.8.2, 2026-10-13, no course key); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commit (and four files from the `solution` branch) |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

## Chapters

CHAPTERS

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: which two stages
could run at the same time, which build steps run again after you change only the group name, what
a venv at `/app/.venv` would find under the mount, which Python the venv gets when the image has 3.12
and `pyproject.toml` asks for 3.14 or newer, and whether a git-ignored key ends up in the image you
push. Five test-yourself questions close the video (answers in `exercises.md`).

**Part 1 · the pipeline, and your first Dockerfile**

1. **Five containers, one bucket** — five programs, each in its own container, turn a recording
   into an English and a French podcast without messaging each other; what changes since lecture 2
   (you write the Dockerfile, five images, a bind mount, a shared bucket and a service-account key).
2. **The bucket is the message bus** — each stage reads one bucket prefix and writes the next;
   object names like `text_prompts/group-01/input-….txt` (no real folders) are the whole wiring;
   the group name keeps teams apart and has no guard; the leaderboard; every call is billed to the
   course's project.
3. **Clone: five folders, no Dockerfile** — `git clone`, five component folders each with a README,
   `cli.py` and `secrets/` but no Dockerfile; `generate_text`'s own `pyproject.toml` and `main.py`;
   a first look at `transcribe_audio/cli.py`: imports, settings, and the three verbs download,
   transcribe, upload.
4. **The key, and uv init** — the course's service-account key from Canvas into each `secrets/`
   folder, under its exact name; installing uv if needed; `uv init --bare`, and why its
   `requires-python` depends on your laptop's Python.
5. **Write the Dockerfile, line by line** — the base image, a build argument with `ffmpeg`, six
   environment variables (`UV_PROJECT_ENVIRONMENT` and `GOOGLE_APPLICATION_CREDENTIALS` among them),
   one chained `RUN` layer that installs packages and uv and creates the user `app`, `COPY` of
   *everything*, `uv sync`, the start command; why not to paste the appendix's sample.
6. **Build: five steps, one fat layer** — `docker build -t transcribe_audio .` and the build context;
   the full log's landmarks (237 apt packages, uv sync with the image's Python 3.12); the harmless
   secrets warning; an 842 MB layer in a 1.35 GB image; what a missing `pyproject.toml` does.
7. **Run: a window into your laptop** — the container's throwaway layer; `-v "$(pwd):/app"` covers
   `/app` with your folder, so the venv lives in `/home/app`; the Windows notes (Git BASH, quotes,
   `winpty`); inside: user `app`, the venv active without a prompt prefix, and
   `No module named 'google'`.

**Part 2 · packages, the key, and all five components**

8. **uv add: what lands where** — three packages become 26; `pyproject.toml` and `uv.lock` are
   written to your laptop, the packages to the venv on the throwaway layer; `ffmpeg-python` vs
   `ffmpeg`; permission errors on Linux; the group name, edited on the laptop and seen inside;
   `--help` matching the README.
9. **Who is calling? The key and ADC** — `--download` without a key and how to read its
   `DefaultCredentialsError`; Application Default Credentials and the relative path in
   `GOOGLE_APPLICATION_CREDENTIALS`; authentication and authorization; the three usual causes; what
   to look for with your key.
10. **Transcribe and upload** — ffmpeg turns MP3 into FLAC; a long-running Speech-to-Text call (a
    ticket stub, up to 90 s); long transcripts joined; a transcript that says `None`; only `input-`
    files are uploaded; the leaderboard; `-d -t -u` in one go.
11. **Exit, and bake it in** — `exit` takes the packages with it; what survived on the laptop; the
    trap (a new container from the old image); the rebuild (build steps 2–3 cached, COPY and
    `uv sync` again, 26 packages baked in, 1.48 GB); `docker history`; why any edit re-runs
    `uv sync`.
12. **generate_text: same recipe, two surprises** — `uv init` fails (skip it); the Dockerfile
    without ffmpeg; `requires-python = ">=3.14"` makes uv download its own Python (3.15.0 at the
    time of recording), fixed with `>=3.12`; Gemini 2.5 Flash Lite on Vertex AI, which Google
    retires on October 20, 2026, and the `GEMINI_MODEL` variable for a current model.
13. **Synthesize, translate, synthesize** — C, D and E at speed: C reuses B's big layer (a 0.6 s
    build); even `--help` needs the key in C, D and E; Text-to-Speech writes straight into the
    bucket (no upload), Translation answers at once (D uploads); the optional ElevenLabs bonus.
14. **Keep the key out of the image** — a git-ignored stand-in key ends up in every image, because
    Docker doesn't read `.gitignore`; the fix, a `.dockerignore` with `secrets/`; the mount still
    brings the key at run time; the optional Docker Hub push, done safely; last year's solution
    (secrets outside the repo, mounted at `/secrets`).
15. **Clean up, recap, and what's next** — nothing to delete in the cloud; the five images;
    `git status` and `git add -f` for your git-ignored work (never `secrets/`);
    `docker image rm` and `docker image prune`; five test-yourself questions; lecture 4.

The README's small mistakes are pointed out kindly, with the fix: the component READMEs link an
older Canvas file for the key (use the main README's); the build command is never given
(`docker build -t <component> .`, from the component folder); the appendix's sample Dockerfile has
`curl` instead of `ffmpeg`; `uv init --bare` writes your laptop's Python into `requires-python`
(above 3.12, lower it to `>=3.12`); in `generate_text` the project is already initialized, with
`>=3.14`, so skip `uv init` and lower it there too; C's and E's READMEs say to keep `ffmpeg`, but
their code blocks, which leave it out, are right; E's `--help` says "Transcribe audio file to
text", pasted from A; the secrets note covers Git only, while `COPY . ./` puts the key in every
image (add `.dockerignore`); and four folders git-ignore your Dockerfile, `pyproject.toml` and
`uv.lock` (`git add -f` them in your own repo, keep `secrets/` ignored).

## Rebuild

```bash
python -m explainer.build videos/ac215-l03-mega-pipeline -q l                          # fast draft
python -m explainer.build videos/ac215-l03-mega-pipeline --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l03-mega-pipeline --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l03-mega-pipeline --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l03-mega-pipeline --lang zh                # Chinese text aligned with the English
```

The clean video and the two part cuts are not in Git: after a fresh clone, render the scenes once,
then the `--no-render` line rebuilds them (and the burned-in copy) from the scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); this video is made for study
with the instructor's permission. The bucket, the leaderboard and the Canvas download are schematic
drawings (tagged `illustration`), not screenshots; no course key was used or shown.*
