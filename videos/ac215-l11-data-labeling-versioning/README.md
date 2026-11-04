# AC215 · Lecture 11 — Data labeling and versioning: a label is a record, a version is a fingerprint

A follow-along walkthrough of the Lecture 11 tutorials of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, *Data Labeling, Versioning and Monitoring*, each `README.md` top to bottom:

- **Part 1:** [dlops-io/data-labeling](https://github.com/dlops-io/data-labeling), branch `main` @
  [`03c3e27`](https://github.com/dlops-io/data-labeling/tree/03c3e277abeee2cdaf4c1a8149c11c9fd259577d):
  *Prerequisites*, *Setup GCP Credentials*, *Prepare Dataset*, *Run Label Studio Container*, *Setup
  Label Studio*, *Enable cross-origin resource sharing (CORS)*, *Annotate Data*, *View Annotations in
  GCS Bucket*, *View Annotations using CLI*, *Extra: Using docker-compose to run both containers* and
  *Docker Cleanup*.
- **Part 2:** [dlops-io/data-versioning](https://github.com/dlops-io/data-versioning), the README at the
  course map's pin
  [`b240b1a`](https://github.com/dlops-io/data-versioning/tree/b240b1a03e0abd1964b689ea68e35f0990a33ebc),
  run on the starter code it tells you to clone, branch `data-versioning-ac215` @ `23762e4`, with the
  one-line `Dockerfile:36` fix (`google-cloud-sdk` → `google-cloud-cli`). The README changed on lecture
  day (`main` @ `2515e5e` now says to clone `main`); the video shows what that route does, kindly, as an
  erratum.

Two folders, both called `cheese_dataset`, same file names, same count: which photos, with which labels,
did Monday's model see, and can you get exactly those back? Part 1 runs Label Studio in a container and
follows a label from a click to a JSON record in your bucket; part 2 versions the photos with DVC, so
that one md5 line pins them down and `dvc get --rev` brings them back from anywhere.

Watch it with both READMEs open, your own clones, Docker Desktop running, a Google Cloud project with
billing, your own bucket(s) and a GitHub account. **This lecture stores a few megabytes in GCS** (no
Vertex AI calls); a GOLD tag marks each place, and the video ends with the teardown checklist. The
tracker top left shows the README step; pause at every `▶ your turn` to run the command; a gray `extra`
tag marks a check that isn't in the README, and a gray "Lecture 11 · slides …" tag top right points to
the lecture slides the scene stands on.

The terminal sessions were recorded on 2026-10-23 in a fresh Docker Engine 29.8.2 standing in for a
laptop with Docker Desktop. That machine had **no Google credentials, no bucket, no browser and no SSH
route to GitHub**. Everything local ran live: Label Studio 1.23.0 in its container and its API, the
CLI container, the compose Extra, the DVC image build, `dvc init` and `dvc add`, the cache layout, the
git commits and tags; the `dataset_v20` fingerprint you compute is byte-identical to the class repo's.
Every step that needs a real credential or bucket is shown up to its honest, documented failure, and
the success you should see is tagged `recorded` with its source. Label Studio's clicks are replayed
through its API (`stand-in`: 3 tasks here, 21 for you), and the push counts come from a local stand-in
remote. The GCP console and the Label Studio, GitHub and Colab pages are schematic drawings tagged
`illustration`. The bucket on screen is the stand-in `your-bucket-placeholder`. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L11-data-labeling-versioning.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L11-data-labeling-versioning.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l11-data-labeling-versioning.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, 32:09 (1929.1 s). Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l11-data-labeling-versioning.mp4` | the same video without burned-in subtitles (1920×1080 at 60 fps, h264/AAC 48 kHz stereo, −16.1 LUFS integrated); load any `.srt` below in your player. Not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l11-data-labeling-versioning_part1.mp4` | part 1, 15:58 (958.6 s): Label Studio in Docker, signed URLs, CORS on a bucket, labels as records (S01–S08). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l11-data-labeling-versioning_part2.mp4` | part 2, 16:10 (970.5 s): DVC, a mounted bucket, content-addressed files, tags you can time-travel to (S09–S16). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l11-data-labeling-versioning.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l11-data-labeling-versioning.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l11-data-labeling-versioning.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `digest.md` | the tutorial digest: both repos, every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorials: a digest of the slide deck in our own words, with slide numbers, and which section stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (2026-10-23, a fresh Docker Engine 29.8.2 standing in for the laptop with Docker Desktop, no Google credentials); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commits |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |
| `REVIEW.md` | the review record: content gates, QA findings and fixes, the final-cut checks |

Git keeps the subtitles, the chapter files and the transcript; the MP4s are release assets.

## Chapters

Paste-ready in `output/chapters.txt` (and `chapters_part1.txt`, `chapters_part2.txt` for the parts). Part 1 (15:58) is chapters 00:00–13:57 below; part 2 (16:10) restarts at 00:00 with "A repo of your own, from the starter", its chapters at 00:00, 01:48, 03:45, 05:35, 08:16, 10:17, 12:21, 14:15.

```
00:00 Same names, different data?
01:16 Two stations, two buckets
03:14 A key, 21 photos and a bucket
04:55 A whole web app in one docker run
07:13 Who touches the bytes?
09:25 CORS: the bouncer, configured on the bucket
11:31 A label is a record; read it back by name
13:57 Both containers in one file, and a clean exit
15:58 A repo of your own, from the starter
17:47 A bucket that looks like a folder
19:44 The starter that no longer builds
21:34 Files named by their fingerprint
24:15 A pointer in git, the bytes in a bucket
26:16 One more photo: what moves?
28:19 Time travel from anywhere
30:13 Monitoring, teardown and recap
```

## What you'll learn

Ten *pause and ponder* moments and two quick predictions ask you to predict before the video shows you:
where the network, the credentials and Compose show up; how many tasks a 42-file zip makes; where to
look when a container exits; how a browser that never sees the key can show a private photo; two
suspects when the thumbnails stay broken; what `localhost` means inside the CLI container; whether
`docker system prune` deletes your labels; whether an empty folder on your laptop means the mount is
broken; which fingerprint changes on a rename; how many objects a second push uploads; whether a
silent `dvc get --quiet` worked; and which tool answers which versioning question. Five test-yourself
questions close the video.

**Part 1 · Label Studio in Docker: signed URLs, CORS on a bucket, labels as records**

1. **Same names, different data?** — two `cheese_dataset` folders and a model that got worse; the
   "final-final-v3" habit; one md5 line you will compute in part 2; where a click on "gouda" goes;
   what you need, and what bills.
2. **Two stations, two buckets** — the map that stays all lecture (slide 6 redrawn): a labeling
   station and a versioning station, each with its bucket, plus GitHub and Colab; clone both repos;
   give Docker enough memory.
3. **A key, 21 photos and a bucket** — the `data-service-account` key with the Storage Admin role;
   download and unzip the photos, drop the Mac metadata files, and make the bucket and its two folders.
4. **A whole web app in one docker run** — `docker-shell.sh`'s flags become a house on a street with a
   door and two pipes; on Linux the container exits because Docker made its data folder as root, and
   `chown -R 1001` fixes it; log in.
5. **Who touches the bytes?** — source and target storage; an honest note on this recording's missing
   key; Label Studio lists the bucket and signs a short-lived ticket, and your browser fetches the photo
   from Google itself.
6. **CORS: the bouncer, configured on the bucket** — two origins and the browser's same-origin rule;
   the README's two slips, kindly; the CLI container, `cli.py -c` sets the bucket's rule, and `curl`
   never meets a bouncer.
7. **A label is a record; read it back by name** — annotate, and a label lands as a small JSON note in
   `cheeses_labeled/`; the CLI reaches Label Studio by name, not localhost; Label Studio 1.23.0's
   legacy-token 401 and its fix.
8. **Both containers in one file, and a clean exit** — the compose Extra: the name conflict, compose's
   own bucket name on line 17, `depends_on` means started, not ready; cleanup, and the labeled project
   survives `docker system prune`.

**Part 2 · DVC: a mounted bucket, content-addressed files, tags you can time-travel to**

9. **A repo of your own, from the starter** — why not git alone; four ways to version data and the
   file-based one we build; your own private repo from the `data-versioning-ac215` starter.
10. **A bucket that looks like a folder** — a bucket stores named objects; the entrypoint's four stages:
    authenticate, mount the whole bucket with gcsfuse, bind `images/` to `cheese_dataset`, use the data;
    the `--implicit-dirs` trap.
11. **The starter that no longer builds** — `google-cloud-sdk` has no installation candidate; the
    one-line fix on `Dockerfile:36`; without a key the mount fails, and the entrypoint carries on.
12. **Files named by their fingerprint** — `dvc init` (and its Linux ownership error); MD5 per photo,
    a shelf named by the first two characters, a manifest fingerprinted in turn: `89db50de….dir`, the
    same as the instructor's tag.
13. **A pointer in git, the bytes in a bucket** — `dvc push`, the three homes of the bytes, the
    six-line pointer file in git, `dataset_v20` as an annotated tag pushed with `--atomic`.
14. **One more photo: what moves?** — add a fifth photo: four blobs already on the shelf, so the push
    uploads two objects; `dataset_v21`; a checkout experiment to watch, not to run on a real mount.
15. **Time travel from anywhere** — `dvc get --rev` walks from the tag to the bytes in Colab; the class
    bucket's 401; `--quiet` hides an unknown revision.
16. **Monitoring, teardown and recap** — three tools for three questions; monitoring, slides only; the
    whole lecture on one map; five questions; the cleanup (never delete `dvc_store` while a tag should
    still work); next, lecture 13.

## Rebuild

```bash
python -m explainer.build videos/ac215-l11-data-labeling-versioning -q l                          # fast draft
python -m explainer.build videos/ac215-l11-data-labeling-versioning --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l11-data-labeling-versioning --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l11-data-labeling-versioning --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l11-data-labeling-versioning --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes
once, then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy
from the scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the data-labeling and
data-versioning tutorials are used for study with the instructor's permission and quoted at their
pinned commits. The lecture's slides are redrawn in our own pictures, never shown. The GCP console and
the Label Studio, GitHub and Colab pages are schematic drawings (tagged `illustration`), not
screenshots; the recording used no Google credentials, and the key in the folder listings is an
obviously invalid stand-in.*
