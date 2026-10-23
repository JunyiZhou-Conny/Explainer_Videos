# AC215 · Lecture 11 — Data labeling and versioning: where does a label go, and what is a version? — narration script & visual plan (v1)

Audience: an AC215 student who has done L1–L10 (a GCP project, images, containers, bind mounts,
Compose, networks and published ports; from L10 service accounts, the `../secrets` convention,
ADC, Docker DNS vs `localhost`, and CORS when a browser calls a container API). New to them: a
labeling tool as a containerized web app, source/target storage and pre-signed URLs, CORS **on a
bucket**, annotations as records, FUSE-mounted buckets, content-addressed storage, DVC pointer
files and git tags as dataset versions. They watch with their own clones of
`dlops-io/data-labeling` and (part 2) their own repo made from `dlops-io/data-versioning`'s
starter branch open, a GCP project with billing, their own bucket(s) and a GitHub account, pausing
to run every command. This lecture stores a few MB in GCS (GOLD tags, teardown checklist at the
end) and calls no paid model.

Goal: after the video they can run Label Studio with one `docker run` and read each flag of
`docker-shell.sh` as a door, a street, a pipe or a sticky note (and fix the Linux-only data-folder
crash); explain who touches the photo bytes (Label Studio lists and signs with the key, the
browser downloads straight from GCS with a short-lived signed URL) and why that makes the *bucket*
need a CORS rule (enforced by the browser, set on the bucket, ignored by `curl`); say what a label
is on disk (one JSON record pointing at an unmoved photo) and list labels from a second container
by Docker DNS name, including the Label Studio 1.23 legacy-token 401 and its fix; clone the
starter into a repo of their own, fix its one broken Dockerfile line, and explain the gcsfuse +
`mount --bind` chain (and why the host's `cheese_dataset/` looks empty); predict what `dvc add`
writes (per-file md5s on a two-character shelf, a `.dir` manifest, a six-line pointer) and get the
same 32 characters as the instructor's `dataset_v20` from the same four photos; say where the bytes
sit (bucket `images/`, `.dvc/cache`, `dvc_store/`), why git holds only the pointer, why a second
version uploads two objects, and what `dvc get --rev <tag>` walks; and shut everything down
without destroying the one thing their tags depend on (`dvc_store/`).

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `SLIDES.md`
(lecture-slide digest), `assets/` (see `ASSETS.md`). Where the digest or the slides and the
captures disagree, the captures win. Nothing in a terminal panel is typed by hand: every output
line below names its capture file and line numbers.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each) and become the
  subtitles. Plain spoken English: no backticks, no symbols, no parentheses; commands and paths are
  said in words ("sh docker-shell.sh", "dash p, 8080 colon 8080", "slash secrets", "localhost
  8080") while the exact spelling is on screen. Underscored names are said as words ("cheese
  dataset", "cheeses unlabeled", "DVC store"); tags as "dataset v20". File, tool and service names
  are written as they are and said by lexicon entries (`explainer/lexicon.yaml`; existing and used
  here: "8080", cli.py, docker-shell.sh, docker-compose.yml, Colab, ADC, "401" and its guard "a
  401", "README's", READMEs). Words this script needs that have no entry yet are listed in
  **Lexicon candidates** at the end; this script does not edit the lexicon. The lexicon splice turns
  an "a" directly before an entry into the letter name, so no SAY line puts a bare "a" before an
  entry or a candidate ("one JSON key", "its own CORS rule", "the DVC store", never "a CORS
  rule"); "a 401" is the one guarded form. No `'s` after a word with an entry or a candidate,
  except `README's`. Numbers as digits; never a "!" after a digit. Versions are said with "at the
  time of recording" (Label Studio 1.23.0 and the offered 1.23.2, DVC 3.63.0, Colab's DVC 3.67.1,
  the image sizes); the md5s, sizes and file counts are deterministic for these photos and are said
  plainly ("same bytes, same fingerprint"). HTTP status codes are digits ("a 401", "status 400" is
  never spoken; S05 says "fails").
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the Chinese alignment). No
  sentence opens with a lowercase command, flag, tool or file name ("Then dash p…", "Here, git
  status shows…", "The command dvc get…"). No homographs: never "read", "live", "lives", "close",
  "lead", "tear" (so "shutdown list", not "teardown"), "minute", "content", "record" as a noun (a
  label is "a small JSON note" in SAY, "record" only on screen). The main clause comes first so the
  Chinese subtitles keep English clause order.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer); the card is removed at the start of the next block. Ten in the video (BRIEF,
  coordinator decision: no more): S02, S05, S06, S11, S12, S14 (8 s) and S04, S07, S08, S15 (6 s).
  `QUICK(4 s, "question")` is the same call with 4 s, for the BRIEF's two quick predicts (S03,
  S16); the card says "quick predict" instead of "ponder".
- `TERM(laptop/NN: lines)`: a terminal beat. `laptop/NN` is the one file
  `assets/terminal/laptop/NN-*.txt` (`colab/CNN` likewise under `assets/terminal/colab/`). The
  scene types the command written just before it in the SHOW line (in backticks, exactly as the
  README spells it; extras exactly as the capture's line 1 spells them), then prints those lines.
  Line 1 of every capture is its `$ …` command and is never printed; the `[exit N]` line is never
  printed, and a trailing inline `[exit N]` is stripped (`20:2`, `27:2`). Inside the line list:
  - `…` = print one `…` line;
  - `wrap` = fold long lines (`Terminal.print(..., wrap=True)`): tracebacks, Label Studio's JSON
    errors, the gcsfuse error, the class bucket's 401s;
  - `from "…"` = print that long line from the quoted phrase on, after a `…` (`88:39`, `C13:5`);
  - `squeeze` = a table re-aligned with two-space gutters, an empty trailing column dropped;
  - `[y/N] y` = cut that line after the bracket, pause 0.6 s, type the answer;
  - `→ (no output)`: the prompt simply returns (the capture holds only `[exit 0]`).
- Typed lines at a container prompt. The `istep` captures (`41`, `42`, `44`, `54`, `88`, `90`,
  `93`, `95`, `104`, `115`, `117`, `145`) hold the prompt and the typed line together
  (`app@5bf8945fb887:/app$ python cli.py -c`, `root@d5bf95465b66:/app# dvc init`). The scene sets
  the terminal's prompt to the capture's own and types the rest of that line; the line numbers in a
  TERM after such a command are its output lines. The capture opened a fresh container for most
  steps, so the id changes between them; the `exit` lines that ended a capture are not typed unless
  the SHOW says so, and a GREY chip at the second container prompt of a scene says "our capture: a
  fresh container for each step · stay in yours". S06 says once that the id changes every run.
- Re-entering the DVC container (`93`, `95`, `104`, `115`, `117`): the scene types
  `sh docker-shell.sh` (the README's command, re-used) and prints only `27–28, …, 41–42`
  (`Running container`, `Container is running!!!`, `…`, the "mounted" line and the mount error), a
  GREY chip "same entrypoint errors as before".
- Crops (BRIEF, ASSETS "Capture-only deviations"): never print the three `Added environment …`
  lines and the gcsfuse JSON `INFO` lines of any DVC-container start (lines 33–38 and 40 of `88`,
  `90`, `93`, `95`, `104`, `115`, `117`; 34–39 and 41 of `145`); `19`'s PyPI lines 8–9; the base
  image pull rows of `10` (first and last only); the build-step rows of `41`, `42`, `44`, `52`,
  `54`, `88`, `93`… (first and last only, or none); the base-image rows of `63`/`72`/`152` (lines
  5–6 of `63`/`72`, 6–7 of `152`); `119` (the class repo's head date) is never shown. Image ids and
  our commit hashes carry "yours will differ"; nobody reads them aloud. The placeholder key's size
  (`06`, 422 B) is never highlighted, and its content is never shown.
- Terminal size: the house `term()` (12.6 wide, 22 pt, 65 characters a row, full width). A typed
  command is never cut: it folds at a space onto an indented row; the long one-liners (`07`, `09`,
  `09b`, the `sed` edits, the `tree -I`, the class-repo comparisons) are shown small in a strip and
  fold. When a picture needs the frame, the terminal shrinks to a 3-row strip along the bottom edge;
  a full terminal and a picture never share the frame.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b, header
  `path · lines a–b`; never more than 12 lines on screen at once (a longer span is a 12-line window
  that scrolls). Folders: `data-labeling/` (@ `03c3e27`), `data-versioning/` (README @ `b240b1a`,
  the course pin), `data-versioning@data-versioning-ac215/` (the starter, header prefix
  "starter ·"), `data-versioning@2515e5e/` (today's README, header prefix "README today ·"). A
  "README card" is a GREY quote of README text with the header `README.md · line n` (data-labeling
  or data-versioning named in the header when ambiguous). **Personal data:** quoted lines
  `data-labeling/docker-shell.sh:19`, `docker-compose.yml:31`, `README.md:109, 204, 206` render
  `student@example.com`; today's README:136 is never quoted; nothing is said about the originals.
- `TRACKER A3`: the `ReadmeTracker`, top-left, in every walkthrough scene, moves to that step.
  `TRACKER A3 · extra`: same step, caption gets " · extra" while a command the README doesn't have
  is on screen (variants `extra · Linux`, `extra · stand-in`, `extra · local remote`). Twelve
  trackers (BRIEF), titled with the README section headings; data-labeling README @ `03c3e27`,
  data-versioning README @ `b240b1a`:
  - A = "data-labeling › Setup" (`README.md:11-76`), 6 steps: 1 Clone · 2 secrets folder ·
    3 Service account + key · 4 Download & extract · 5 Bucket + two folders · 6 Upload the 21 images.
  - B = "data-labeling › Run & set up Label Studio" (`:78-147`), 6 steps: 1 sh docker-shell.sh ·
    2 docker container ls · 3 Log in · 4 Create project · 5 Source storage · 6 Target storage.
  - C = "data-labeling › CORS & annotate" (`:149-187`), 6 steps: 1 Edit bucket name ·
    2 sh docker-shell-CLI.sh · 3 python cli.py -c · 4 python cli.py -m · 5 Annotate · 6 View in GCS.
  - D = "data-labeling › View Annotations using CLI" (`:189-207`), 3 steps: 1 Copy the token ·
    2 cli.py -p -k · 3 cli.py -t -k.
  - E = "data-labeling › Extra: docker-compose" (`:214-229`), 2 steps: 1 Stop (docker stop /
    docker ps) · 2 docker-shell-compose.sh.
  - F = "data-labeling › Docker Cleanup" (`:239-246`), 4 steps: 1 docker container ls · 2 stop ·
    3 docker system prune · 4 docker image ls.
  - G = "data-versioning › Prepare Docker and Create Your Repository" (`:48-126`), 5 steps:
    1 Clean Docker · 2 Clone the starter · 3 cd / rm -rf .git / git init · 4 New private repo ·
    5 First push.
  - H = "data-versioning › Set Up GCP Storage and Credentials" (`:130-187`), 3 steps: 1 secrets
    folder · 2 Service account · 3 Bucket folders — plus an `extra` row "upload the first photos".
  - I = "data-versioning › Start the DVC Container" (`:191-243`), 3 steps: 1 Edit docker-shell.sh ·
    2 cd data-versioning · 3 sh docker-shell.sh — plus an `extra` row "Dockerfile:36 fix".
  - J = "data-versioning › Create and View Dataset Versions" (`:250-328`), 6 steps: 1 dvc init ·
    2 dvc remote add · 3 dvc add · 4 dvc push · 5 git ×5 · 6 Colab dataset_v20.
  - K = "data-versioning › Updated Dataset Version: dataset_v21" (`:332-385`), 5 steps: 1 Upload
    images · 2 dvc add · 3 dvc push · 4 git ×5 · 5 Colab dataset_v21.
  - L = "data-versioning › Docker Cleanup" (`:403-425`), 3 steps: 1 docker container ls ·
    2 docker system prune · 3 docker image ls.
  S01, S09's opening, S16's monitoring beat and S16's recap have no tracker.
- `(extra)` after a command: not in the README. A small GREY tag `extra` (or a variant) sits beside
  the typed line, and the SAY says "extra" the first time each kind appears. Commands the README
  describes without spelling (download, extract, `mkdir secrets`, the `sed` edits, `docker stop`
  with the container's name, `sh docker-shell-CLI.sh` for README:165's "Run `docker-shell-CLI.sh`",
  `sh docker-shell-compose.sh` for README:218) carry a GREY chip saying so ("the README shows a
  tree, not a command", "our editor; use yours", "the README names the script"); the README's own
  words stand beside them on a README card.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README step);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every console step, Label Studio screen, GitHub form,
  notebook frame, the hook's two folders and its invented `final-final` file names, the working
  two-view of S11 and the drawn `dvc_store/`; `recorded · <source>` on every success a student sees
  that this machine could not produce (the 21 synced tasks, `README.md:136` + `09`; the CORS print,
  `cli.py:40` + `:26–33`; the metadata print, `cli.py:47–72`; the notebook's cells 13/15/17);
  `extra · stand-in` on Label Studio's clicks replayed as its own API calls (`23`, `24`, `28`, `30`,
  `31`, `32`, `33`, `43`) and the photo copies (`94`, `103`); `extra · local remote` on
  `dvc push -r standin` (`95`, `104`); `at the time of recording` beside every version and image
  size when first shown; `erratum` on every README/repo slip (the narration says "a small slip" or
  "a small gap", never "erratum"); the GOLD `cost_tag()` at S01 (checklist), S03 (bucket 1 + 21
  photos), S10 (`images/`) and S13 (`dvc_store/`), and on S16's checklist card. There are no
  `expected` panels in this episode.
- The honest framing (BRIEF, coordinator decision): S03 says in one line that the key in the
  listing is a stand-in, explained later; S05's third block, at the first cloud failure, says in
  full that this machine has no Google account, no bucket, no browser and no SSH route to GitHub,
  and that the key is an obviously invalid stand-in moved out before every cloud step. From then on
  every cloud failure is taught as the missing-key lesson, every success carries `recorded` + its
  source, and nothing apologises again. `git push` and the SSH clone are typed with **no output
  panel** (the timeouts in `73`, `83`, `100`, `109` are the sandbox's); success is described.
- Stand-in numbers are never README numbers: `"task_count":3` / `Number of tasks: 3` always carry
  "ours: 3 · yours: 21"; our v21 manifest `6b342844….dir` differs from the class's `3280f8f9….dir`
  (a different fifth photo) and is never compared as "should match"; only v20 matches (`121`),
  called "the instructor's tag in the class repo", with no date.
- `lecture_ref(11, "a–b")` (GREY, top right): one per scene as assigned in the BRIEF, spans from
  SLIDES.md §5. Lecture diagrams are redrawn in series style; no slide images, product or console
  screenshots, cartoons, memes or the slide-24 screenshot (S01 types our own invented names).
- Spelling on screen and in the subtitles: American ("gray").
- Semantic colours (BRIEF, fixed for the whole video):

  | meaning | colour |
  | --- | --- |
  | your laptop: host shell, host filesystem, the browser's home, the host's (empty) `cheese_dataset/`, `.dvc/cache` | GREY |
  | the cloud: both buckets, `storage.googleapis.com`, `dvc_store/`, the Colab runtime, the signed-URL ticket | BLUE |
  | containers and images: `data-label-studio`, `data-label-cli`, `data-version-cli`, the compose one-off | TEAL |
  | system-wide / root-owned / host-level power: root-owned folders, uid 1001 vs root, git's ownership check, apt packages, `--privileged` / `/dev/fuse` | ORANGE |
  | project-owned, protected: the `secrets/` key, `.dvc/config`, `cheese_dataset.dvc`, tags as dataset names | GREEN |
  | tools: docker, compose, git, dvc, gcsfuse, gcloud, uv, the Label Studio SDK | PURPLE |
  | errors and refusals: 400/401, `Exited (1)`, the failed build, the entrypoint's failure chain, route T's refusals, the empty-folder version | RED |
  | your turn, the README tracker, the current step | YELLOW |
  | money: GCS storage, the second copy in `dvc_store/`, what keeps billing after shutdown | GOLD |
  | lookups, paths, routes: the Docker street + Docker DNS, the mount pipes, md5 → `files/md5/xx/…` shelf paths, the tag → pointer → manifest → blob rope | PINK |
  | future / elsewhere / lecture-only: L13 training, lakeFS / Delta / Iceberg, monitoring, the class repo's bucket | GREY, dashed |

  Episode-local semantics: two buckets, always two BLUE shapes (`cheese-app-data-demo` for
  labeling, the versioning bucket for DVC). The signed URL is a BLUE ticket with a wax seal and an
  unlabeled hourglass (no expiry value anywhere). An annotation is a WHITE envelope whose label word
  is the only text inside. md5 strings are PINK (addresses); the pointer file and tags are GREEN.
  The `cheese_dataset/` folder seen from the host is GREY and dark; seen from inside the container
  through the mount it is PINK-piped to BLUE. The CORS bouncer stands at the browser's door, facing
  the page; the rule card sits on the bucket.
- Running example. The laptop: user `student`, terminal title `laptop`, prompts from the captures:
  `student@laptop:~$`, `student@laptop:~/data-labeling$`, `student@laptop:~/data-versioning$`; the
  route-T strip is titled `laptop · second clone in ~/today` with prompts `student@laptop:~/today$`
  and `student@laptop:~/today/data-versioning$`. A fresh Docker 29.8.2 engine (Compose v5.6.0,
  git 2.54.0, `x86_64`) stands in for Docker Desktop. Inside containers: `app@<id>:/app$`
  (data-label-cli) and `root@<id>:/app#` (data-version-cli, root). The Colab stand-in strip is
  titled `colab stand-in · signed out`, prompt `$` (its captures have no prompt). Placeholders
  everywhere: login `student@example.com` / `awesome`, bucket `your-bucket-placeholder`, project
  `your-gcp-project`, GitHub user `YOUR_GITHUB_USERNAME`, token `student-demo-token-not-a-secret`
  (GREY chip "obviously fake"). The class bucket `cheese-app-data-versioning` appears only in quoted
  README/config lines and RED class-repo beats; the narration says "the instructor", "the class
  repo", "the class bucket".
- V7, the running map (`PipelineMap`, BRIEF): built in S02 and kept as persistent state; each scene
  lights its piece (secrets drawer S02, bucket 1 S03, the Label Studio house S04, the CLI house S06,
  the labeled drawer S07, compose S08, the repo + flags S09/S13/S14, bucket 2 S10, Colab S15); S08
  ends part 1 with the labeling half lit; S16 adds the GREY-dashed monitoring watchtower, shows it
  complete, then unlit.
- Length and parts: narration **4,282** words (`python -m explainer.script`, which counts SAY
  words; its minute figure assumes 155 wpm and is ignored). At Kokoro af_heart speed 0.9 (≈174 wpm)
  that is ≈24.6 min of narration, ≈29–31 min with typing, outputs and ponder timers. Part 1 =
  S01–S08 (labeling; ends on `docker system prune` with the labeled project still on disk), part 2
  = S09–S16 (versioning). Each part ends on an empty frame. Per scene (BRIEF target in brackets):

  | scene | words (BRIEF) | scene | words (BRIEF) |
  | --- | --- | --- | --- |
  | S01 Hook | 219 (220) | S09 YourOwnRepo | 247 (240) |
  | S02 TwoStations | 256 (250) | S10 BucketAsFolder | 293 (290) |
  | S03 KeyAndPhotos | 232 (230) | S11 StarterFix | 249 (260) |
  | S04 StudioInABox | 302 (300) | S12 Fingerprints | 326 (320) |
  | S05 WhoTouchesBytes | 292 (290) | S13 PointerAndBytes | 271 (300) |
  | S06 CorsOnTheBucket | 300 (290) | S14 SecondVersion | 251 (260) |
  | S07 LabelsAndTokens | 299 (310) | S15 TimeTravel | 252 (250) |
  | S08 ComposeAndClean | 234 (230) | S16 Recap | 259 (230) |
  | **part 1** | **2,134** (2,120) | **part 2** | **2,148** (2,150) |

  Every scene is within the BRIEF's ±15 %. Re-run the counter after any review edit.

Notes for scene authors
- TERM line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the
  output body, so pick index = file line − 1.
- Shared code (`scenes/common.py`, started from L10's): tracker factories `tracker_a` … `tracker_l`
  with the step lists above; prompts `P_LAPTOP` (+ `~/data-labeling`, `~/data-versioning`,
  `~/today` variants), container prompts from each capture; tags `extra_tag` (and its three
  variants), `illustration_tag`, `recorded_tag`, `your_turn`, `cost_tag` (GOLD), `erratum_tag`.
  Set pieces: `StationMap` (V1), `SignedTicket` (V2), `OriginGate` (V3), `FuseMount` (V4),
  `HashShelf` (V5), `TagRope` (V6), `PipelineMap` (V7). Never reuse a scene class name for a helper.
- `86` is 1,126 lines: print only 1075–1081 and line 1125 cut after `failed to solve:` with `…`.
- `54:126` holds `{"status": "UP"}`, the prompt and the next typed command on one line: print the
  JSON, then let the prompt and typing continue on the same row, as the capture shows.
- Never: a real-looking key, token or JWT (`eyJ…`); the placeholder key's content; the
  instructor's e-mail or a TA's user name; any expiry time, task count, object name, file size or
  accuracy number that no source gives; Label Studio, console or Colab screenshots; a GCS push, a
  `cli.py -c` success, a gcsfuse mount, a GitHub push or a Colab download presented as live;
  labeled data drawn as photos sorted into class folders; "Label Studio copies the images"; CORS
  called access control; the host's `cheese_dataset/` drawn holding photos; "DVC stores diffs";
  deleting `dvc_store/` as cleanup; `89`'s root ownership as the mount's success state; the
  capture-only lines read aloud.

---

## S01 · Same names, different data? — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. Two GREY folder cards slide in side by side, `cheese_dataset ·
Monday` and `cheese_dataset · Friday` (tag `illustration`: invented names), each listing
`Image_1.jpg` … `Image_4.jpg` with a GREY chip "4 files". Between them a GREY model card with a
RED down arrow and a "?" (no accuracy numbers anywhere). On "can you get exactly those back", a
YELLOW caption settles at the top: "which photos, with which labels, did Monday's model see?"
SAY: Two folders, both called cheese dataset, with the same file names and the same count. On Monday you trained a model on one of them. On Friday the model got worse, and nobody touched the code. So which photos, with which labels, did that model see? And can you get exactly those back?

SHOW: Slide 24's idea redrawn (GREY tag `lecture_ref(11, "20, 24")` top right from here to the end
of the scene): a GREY terminal strip (tag `illustration`, our own invented names) whose `ls` fills
row by row: `cheese-final.zip`, `cheese-final-v2.zip`, `cheese-final-final-v3.zip`,
`cheese-final-final-v3-USE-THIS.zip`, … until the rows overflow the strip and scroll; a RED "?"
stamps on the last row.
SAY: Most of us answer with file names: final, final version 2, final final version 3, until nobody knows which one is final. The lecture makes fun of exactly this habit.

SHOW: Clear to a dark frame. One PINK line types alone, centred: `md5: 89db50de27acfd6822faabc3da39b0a8.dir`
(the string of `laptop/95`, line 59), with a GREY chip "same bytes, same fingerprint". On "where
does that word actually go", a WHITE envelope with the single word `gouda` floats in beside it
under a GREY "?".
SAY: Here is a better answer: one short line. In part 2 you will compute this exact string on your own laptop from 4 cheese photos, and it will match the instructor's tag in the class repo, character for character. How can one line pin down about 600 kilobytes of photos? And before that, when someone clicks gouda, where does that word actually go?

SHOW: A checklist card: "✓ Docker Desktop running", "✓ a GCP project with billing + your own
bucket" (GOLD `cost_tag()` beside it: "storage: a few MB, cents"), "✓ a GitHub account". Layout
preview: `tracker_a(1)` appears top-left with a YELLOW ring; the ring flicks through the twelve
tracker titles A–L. A 2-row strip terminal (GREY tag "preview", prompt `student@laptop:~$`) shows a
YELLOW `▶ your turn` row tag, then a GREY `extra` row tag, then a GREY `recorded` chip (one after
the other, never stacked). Fade out.
SAY: To follow along you need Docker Desktop, a Google Cloud project with billing and your own bucket, and a GitHub account. This lecture stores a few megabytes in the cloud, and gold tags mark where. The tracker in the top left follows both READMEs. A yellow your-turn tag means pause and run it; a gray extra tag marks a check that is not in the README. Every command is in the study guide.

---

## S02 · Two stations, two buckets — `s02_map.py` · `TwoStations`

SHOW: No tracker yet. GREY tag `lecture_ref(11, "4–6, 8–12")` top right, whole scene. V7's top row
(slide 6 redrawn): a GREY dotted box "Unlabeled" with six blank tiles → a long arrow under a RED
"How do we do this?" → a box "Labeled" with four rows `brie`, `gouda`, `parmigiano`, `gruyere` →
a GREY-dashed box "training · L13". On "graded against", a GREY one-line card (slide 4): "labels =
ground truth · labeled mistakes → the next version".
SAY: First, the map. The lecture draws unlabeled cheese photos, then labeled ones, then training, and the arrow in between asks how. Labels are the ground truth a model learns from and is graded against, and its labeled mistakes become the next dataset version.

SHOW: Below the top row, the two stations build as the code builds them: the labeling station (a
GREY laptop outline; two hollow TEAL houses on a PINK street) ↔ BLUE bucket 1
`cheese-app-data-demo` with drawers `cheeses_unlabeled/` and `cheeses_labeled/`; the versioning
station (a hollow TEAL `data-version-cli`) ↔ BLUE bucket 2 (`images/`, `dvc_store/`) and a GREY
"your private GitHub repo" with two GREEN flag stubs; a BLUE Colab box "view versions". A
GREY-dashed bridge between `cheeses_labeled/` and `images/`, caption "not connected in the code ·
exercise E7". The training box stays GREY dashed.
SAY: Underneath, the two stations this lecture builds. Part 1 is the labeling station: Label Studio in a container, with one bucket for photos and labels. Part 2 is the versioning station: one DVC container, a second bucket, your own GitHub repo, and Colab to view versions. The code does not connect the halves yet; exercise E7 does.

SHOW: Slide 8's recall quiz as three GREY chips floating over the map: "Docker network", "cloud
credentials", "Docker Compose".
PONDER(8 s, "Docker network, cloud credentials,\nDocker Compose: where will each\none show up today?")
SAY: The lecture begins with a recall quiz, so here it is. Docker network, cloud credentials, Docker Compose: where will each one show up today?

SHOW: The answer (slides 10–12): each chip flies to its spot on V7. "Docker network" → the PINK
street between the two TEAL houses, labelled `data-labeling-network`, an arrow from the right
house to the left one by name; "cloud credentials" → a GREEN `secrets/` drawer with the label
`GOOGLE_APPLICATION_CREDENTIALS`, GREEN pipes into every TEAL house; "Docker Compose" → a
GREY-dashed blanket over both houses, "the README's Extra".
SAY: The network lets the command line container call Label Studio by name. The credentials are one key file, mounted into every container. And Compose is the README's extra section, which starts both containers together.

SHOW: TRACKER A1 (tracker A appears: "README › data-labeling › Setup", 6 dots). Full-width laptop
terminal (title `laptop`, prompt `student@laptop:~$`). A README card (`README.md · line 14`). It
types `git clone https://github.com/dlops-io/data-labeling` → TERM(laptop/01: 2); `▶ your turn`.
Then `cd data-labeling` → (no output); prompt `student@laptop:~/data-labeling$`. A GREY chip on the
terminal title, not spoken: "Docker 29.8.2 · Compose v5.6.0 · git 2.54.0 · at the time of
recording" (laptop/00, lines 4–6). A small README card (`README.md · line 18`), "Docker>Preferences>Resources
… > 4GB", tag `erratum`, chip "now: Settings › Resources".
SAY: Time to type. Clone the data-labeling repo and move into it; pause and run it. Give Docker more than 4 gigabytes of memory, as the README asks; the setting is now under Settings, Resources.

SHOW: TRACKER A1 · extra. It types `git log -1 --format='%H %ci'` (extra) → TERM(laptop/02: 2);
`03c3e277…` and `2025-10-20` highlight. Then `ls -la` (extra) → TERM(laptop/03: 2–19); the three
shell scripts (lines 14–16) and `cli.py` (line 10) highlight, then the three PNGs (9, 11, 17);
`pipeline-flow.png` (17) gets a GREY chip "a version of this map, one bucket · no README links it".
SAY: An extra git log shows this video's commit, from October 2025, and an extra listing shows three shell scripts, cli.py, and three pictures. One, pipeline flow, draws this map with a single bucket; no README links it.

SHOW: TRACKER A2. It types `cd ..` → (no output); prompt `student@laptop:~$`. Then `mkdir secrets`
(GREY chip "the README shows a tree, not a command") → TERM(laptop/04: → (no output)); then
`tree -L 1 .` (extra) → TERM(laptop/05: 2–6) beside a README card (`README.md · lines 37–40`), the
two trees matching row for row. `▶ your turn`. On V7 a GREEN `secrets/` drawer settles beside the
labeling station, outside every repo. Fade out.
SAY: Next, the secrets folder, beside the repo and never inside it; it serves both repos today. Pause and make it; an extra tree view matches the README.

---

## S03 · A key, 21 photos and a bucket — `s03_photos.py` · `KeyAndPhotos`

SHOW: TRACKER A3. GREY tag `lecture_ref(11, "5–6, 11")` top right, whole scene. A schematic
console (tag `illustration`; no screenshot, no logo) with README.md lines 44–50's values, step by
step: "IAM & Admin → Service accounts" → "Create service account · data-service-account" →
"Grant this service account access to project: Cloud Storage → Storage Admin" → tab "KEYS" →
"ADD Key (Create New Key)" → "JSON"; a file icon drops into `secrets/` and is renamed
`data-service-account.json`. On "every bucket in the project", a GREY chip under the role:
"project-wide · this tutorial needs object read/write + storage.buckets.update (for CORS)".
`▶ your turn`.
SAY: Now the key. In the console, create a service account named data-service-account with the Storage Admin role, then one JSON key, saved in your secrets folder as data-service-account dot json. This role is broader than needed: it covers every bucket in the project. Pause and create yours.

SHOW: TRACKER A3 · extra. Terminal, prompt `student@laptop:~$`. It types `ls -la secrets` (extra)
→ TERM(laptop/06: 2–5); the file name highlighted (not its size); a GREY tag `stand-in` on line 5
with the caption "explained in scene 5".
SAY: An extra listing shows the key in place. This one is a stand-in, and the reason comes in scene 5.

SHOW: TRACKER A4. A README card (`README.md · lines 62–65`): "Download the unlabeled data from
here · Extract the zip file". It types
`curl -sSLO https://github.com/dlops-io/datasets/releases/download/v4.0/cheeses_unlabeled.zip && ls -l cheeses_unlabeled.zip`
(GREY chip "the README's link, with curl"; folds) → TERM(laptop/07: 2), `3720496` highlighted. Then
`unzip cheeses_unlabeled.zip` (GREY chip "the README says extract") → TERM(laptop/08: 2–9, …,
44–45); each `__MACOSX/cheeses_unlabeled/._Image_*` row flashes GREY under its image row.
`▶ your turn`.
SAY: Download the unlabeled photos from the README link, about 3.7 megabytes; we use curl, and a browser works too. Then extract the zip. Pause and do both. Notice that every image comes with a twin in a hidden Mac folder.

SHOW: The two folders side by side, unlabeled counts hidden.
QUICK(4 s, "The zip held 42 files.\nHow many tasks should\nLabel Studio make?")
SAY: A quick prediction: the zip held 42 files. How many tasks should Label Studio make?

SHOW: TRACKER A4 · extra. It types
`ls cheeses_unlabeled; ls cheeses_unlabeled | wc -l; ls -a __MACOSX/cheeses_unlabeled | head -5; ls -A __MACOSX/cheeses_unlabeled | wc -l`
(extra; folds) → TERM(laptop/09: 2–4, …, 11, …, 23–29); line 23 `21` and line 29 `21` YELLOW,
line 11 `Image_3.png` YELLOW. The 21 twins drop into a RED bin "don't upload". A tiny GREY funnel
(slides 16–18 redrawn) sorts tiles into "keep" and "discard".
SAY: 21. An extra count shows 21 images, one a PNG, plus 21 Mac metadata files: upload only the images, or you get 21 broken tasks. The lecture calls this curation, dropping junk before it becomes a task.

SHOW: TRACKER A4 · extra. It types the `md5sum … ; wc -c …` line (extra; folds, small) →
TERM(laptop/09b: 2–12); line 2's `5b53853e667c8a76121fdc475996c895` gets a PINK ring and a pin
"part 2".
SAY: One more extra, for part 2: fingerprints and sizes of the first five photos. Remember the first one.

SHOW: TRACKER A5. Console `illustration` (README.md lines 67–72): "Create bucket ·
`your-bucket-placeholder`" with the README's "(REPLACE WITH YOUR BUCKET NAME)" and "Keep the
defaults" → folders `cheeses_unlabeled/` and `cheeses_labeled/`. TRACKER A6 (README.md line 76):
21 blank image tiles fly into `cheeses_unlabeled/` (no photos drawn). On V7, BLUE bucket 1 lights.
GOLD `cost_tag()`: "storage starts here · ≈ 3.8 MB · a fraction of a cent a month · check the
pricing page" (digest §2 estimate). `▶ your turn`. Fade out.
SAY: Then create your bucket with a name of your own, since names are global, and keep the defaults. Add two folders, cheeses unlabeled and cheeses labeled, and upload the 21 images into the first. Pause and set it up. A gold tag: storage starts here, about 3.8 megabytes, a fraction of a cent a month.

---

## S04 · A whole web app in one docker run — `s04_studio.py` · `StudioInABox`

SHOW: TRACKER B1 (tracker B appears: "README › data-labeling › Run & set up Label Studio", 6
dots). GREY tag `lecture_ref(11, "7, 13–14")` top right, whole scene. Slide 7's why as one GREY
line: "a labeling tool in your own container · no outside labeling service sees your data".
CODE(data-labeling/docker-shell.sh: 5–9): line 6 (`docker network inspect … || docker network
create data-labeling-network`) YELLOW, a small GREY sticky note "inspect … || create · L10's
shape"; line 9 (`docker rm -f data-label-studio 2>/dev/null || true`) GREY.
SAY: The README runs Label Studio from a ready-made image, in your own container, so no outside labeling service sees your photos. Its script creates the network only if missing, as last lecture, and removes any old container of that name.

SHOW: V1 builds over CODE(data-labeling/docker-shell.sh: 12–24) (a 12-line window that scrolls one
line at the end; line 19 renders `student@example.com`). Each line peels off and becomes a part:
line 12 `-d` slides the TEAL `data-label-studio` house into the background and the prompt returns;
line 14 `--network data-labeling-network` lays a PINK street under it; line 15 `-p 8080:8080` cuts
a GREY door in the laptop wall, chip "publish the port"; line 16 `-v …/docker-volumes/label-studio:/label-studio/data`
is a GREY pipe to a drawer "database" (slide 13, callout 1); line 17 `-v "$(pwd)/../secrets:/secrets"`
a GREEN pipe; lines 18–23 `-e` stick on as notes (login, key path; callout 2). The lecture's label
"Label Studio Container" appears once in GREY above the house, then morphs into `data-label-studio`.
SAY: Then one docker run, flag by flag. The flag dash d runs it in the background, the network flag puts it on a private street, and dash p, 8080 colon 8080, publishes the port: a door in your laptop wall. Two dash v flags mount a database folder and your secrets; the dash e lines set the login and key path.

SHOW: TRACKER B1. Terminal, prompt `student@laptop:~/data-labeling$`. It types `sh docker-shell.sh`
→ TERM(laptop/10: 2–3, …, 70–72); line 72 (the container id) gets a GREY chip "yours will
differ". `▶ your turn`. TRACKER B2: `docker container ls` → TERM(laptop/11: 2–3; squeeze);
`Up Less than a second` and `0.0.0.0:8080->8080/tcp` GREEN, beside a README card
(`README.md · lines 91–97`, its line 95 dimmed for now). `▶ your turn`.
SAY: Pause and run sh docker-shell.sh; it pulls the image and prints a container ID. Then the README's check, docker container ls: up, port 8080 published.

SHOW: TRACKER B2 · extra. A GREY "+25 s" clock chip. It types `docker container ls -a` (extra) →
TERM(laptop/12: 2–3; squeeze); `Exited (1) 25 seconds ago` RED. The V1 house tips over.
PONDER(6 s, "It said Up.\nNow it says Exited (1).\nWhere do you look first?")
SAY: But look again 25 seconds later, with an extra dash a: exited. Something to ponder: where do you look first?

SHOW: TRACKER B2 · extra. It types `docker logs data-label-studio 2>&1 | tail -n 40` (extra) →
TERM(laptop/13: 4–12); line 5 RED, line 8 `UID        = 1001` and line 12 (owner `root`) YELLOW.
V1's drawer flashes ORANGE. Then `ls -la docker-volumes docker-volumes/label-studio` (extra) →
TERM(laptop/14: 2–6), line 6's `root` ORANGE; `docker run --rm --entrypoint id heartexlabs/label-studio:latest`
(extra; folds) → TERM(laptop/15: 2), `uid=1001` YELLOW.
SAY: The logs. Label Studio explains itself: its data folder is not writable. It runs as user 1001, but Docker created the missing folder as root. Two extra checks confirm both halves.

SHOW: TRACKER B1 · extra (tag `extra · Linux`). It types
`sudo chown -R 1001 docker-volumes/label-studio && ls -la docker-volumes` (folds) →
TERM(laptop/16: 2–5), line 5's `1001` GREEN; the drawer turns GREY. Then `sh docker-shell.sh` →
TERM(laptop/17: 2–3) and `docker container ls` → TERM(laptop/18: 2–3; squeeze), `Up About a
minute` GREEN; the house stands.
SAY: The fix is an extra, for Linux; Docker Desktop for Mac normally avoids this. Give the folder to user 1001 with sudo chown, run the script again, and now it stays up.

SHOW: TRACKER B2 · extra. It types `docker logs data-label-studio 2>&1 | grep -v '^\s*$' | tail -n 25`
(extra) → TERM(laptop/19: 10–13, 16, 20–21) (lines 8–9 never printed); the update box (10–13)
YELLOW with `at the time of recording`. Then `curl -s http://localhost:8080/health` (extra) →
TERM(laptop/20: 2); `curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' http://localhost:8080/`
(extra; folds) → TERM(laptop/21: 2).
SAY: Extra checks: the logs show the server starting and a box offering version 1.23.2, because the image tag is latest; this video ran 1.23.0, at the time of recording. Two curls get status up and the login page.

SHOW: TRACKER B3. A schematic login page (`illustration`) at `http://localhost:8080/`, fields
`student@example.com` / `awesome`; CODE(data-labeling/docker-shell.sh: 19–20) small beside it
(line 19 renders `student@example.com`). Its server side, tag `extra · stand-in`, in a strip:
TERM(laptop/23: 2), then TERM(laptop/24: 2–7) with `"email": "student@example.com"` highlighted.
TRACKER B4: a wizard `illustration` (README.md lines 110–115): Create Project → name → skip Data
Import → Labeling Setup → "Computer Vision > Image Classification" → choices `brie`, `gouda`,
`gruyere`, `parmigiano` → Save. Server side, `extra · stand-in`: TERM(laptop/28: 6; wrap, cut after
the label config), `"id":1,"title":"Cheese labels"` and the four `<Choice value=…/>` highlighted.
`▶ your turn` on each step. Fade out.
SAY: Open localhost 8080 and log in with the username and password from lines 19 and 20 of your script. Create a project with the image classification template, with the choices brie, gouda, gruyere and parmigiano. Pause and do it. Underneath, as stand-in calls, the server side: logged in, and project 1 holds the four cheeses.

---

## S05 · Who touches the bytes? — `s05_storage.py` · `WhoTouchesBytes`

SHOW: TRACKER B5. GREY tag `lecture_ref(11, "6–7, 13")` top right, whole scene. Slide 13 redrawn
small in GREY (two containers, the bucket, the browser linked only to Label Studio), chip "the
slide links the browser only to Label Studio". Then a form `illustration` with README.md lines
121–134's values: Storage Type `Google Cloud Storage`, Storage Title `Cheese Images`, Bucket Name
`your-bucket-placeholder`, Bucket Prefix `cheeses_unlabeled`, Import Method `Files - …`,
☑ "Treat every bucket object as a source file" (GREY chip "may be missing in newer versions ·
carry on"), ☑ "Use pre-signed URLs" (YELLOW), credentials and project ID empty (chip "empty = the
key the container already has").
SAY: Back in the project, open settings, cloud storage, and add source storage with the README's values: Google Cloud Storage, your bucket, the prefix cheeses unlabeled, and pre-signed URLs on. If a checkbox is missing, carry on. Leave the credentials empty: that means the key the container already has.

SHOW: The form's *Check Connection* button, then its own API call in a strip, tag
`extra · stand-in`: TERM(laptop/30: 3; wrap), `"File /secrets/data-service-account.json was not
found."` RED. Laptop prompt `student@laptop:~/data-labeling$`: `docker exec data-label-studio ls -la /secrets`
(extra) → TERM(laptop/29: 2–4): empty. TRACKER B6: the target form (`illustration`, README.md
lines 138–146: prefix `cheeses_labeled`), its *Check Connection*, `extra · stand-in` →
TERM(laptop/31: 3; wrap), `"Error validating storage connection"` RED. `▶ your turn` on the source
form and on the target form.
SAY: Then click Check Connection. Here it fails: file not found. An extra listing shows why: slash secrets inside Label Studio is empty. The target storage, with the prefix cheeses labeled, fails the same way.

SHOW: The honest card (GREY), its three lines building on their sentences: "This recording machine
has no Google account, no bucket, no browser and no SSH route to GitHub." · "The key in the folder
listings is an obviously invalid stand-in, moved out before every cloud step." · "Each cloud step
shows the failure a misplaced key gives." On "tagged recorded", three GREY chips settle under it:
`recorded · source named`, `extra · stand-in`, `extra · local remote`.
SAY: One honest note about this recording. This machine has no Google account, no bucket, no browser, and no SSH route to GitHub. The key in the folder listings is an obviously invalid stand-in, moved out before every cloud step. So each cloud step here fails exactly the way a misplaced key fails, the most common mistake in this lecture. Every success you should expect is tagged recorded, with its source, and clicks and uploads are replayed locally, tagged stand-in.

SHOW: TRACKER B5. With a real key: *Add Storage*, then *Sync Storage*: 21 task cards fan out from
the BLUE bucket (tag `recorded · README.md:136 + the 21 images of laptop/09`). Our stand-in, tag
`extra · stand-in`: TERM(laptop/32: 2–5; wrap); the three
`gs://your-bucket-placeholder/cheeses_unlabeled/Image_N.jpg` URIs highlighted, `"task_count":3`
YELLOW with a chip "ours: 3 · yours: 21". `▶ your turn`.
SAY: With a real key, add both storages and click sync: one task per photo, 21 for you. Our stand-in imports 3 tasks with the same kind of addresses. Pause, add both, and sync.

SHOW: V2 steps 1–2a: the GREY browser on the laptop floor, the TEAL Label Studio house holding the
GREEN key, the BLUE vault `cheese-app-data-demo` with drawers `cheeses_unlabeled/` and
`cheeses_labeled/`. (1) Label Studio reaches the vault with the key, lists names, task cards fan
out. (2a) The browser raises a hand at card 1. Nothing else moves.
PONDER(8 s, "Label Studio holds the key;\nyour browser never sees it.\nHow can it show a private photo?")
SAY: So who touches the photos? Label Studio holds the key and lists the bucket; your browser asks for task 1. Something to ponder: your browser never sees the key, so how can it show a private photo?

SHOW: The answer, V2 steps 2–3: Label Studio stamps a BLUE ticket (the photo's URL, a wax seal
"signed with the key", an hourglass with no value) and slides it across; the key stays behind,
GREEN, in the house. The browser walks the ticket to the vault's own door,
`https://storage.googleapis.com`; the vault checks the seal and hands back the photo, which
bounces off a GREY bouncer at the browser's door (V3 teaser). A GREY card, slide 7's "private"
made precise: "no outside labeling company sees your data · the photos stay in your bucket · your
browser fetches them straight from Google". Cliff-hanger: a task grid with broken thumbnails
(`illustration`) beside a README card (`README.md · line 151`). Fade out.
SAY: With a signed ticket. For each photo, Label Studio signs a web address with the key: permission for one photo, for a short time. Your browser carries that ticket straight to Google, and the key stays in the container. So private means no outside labeling company sees your data. Then the thumbnails break, and the README warns you: it is CORS.

---

## S06 · CORS: the bouncer, configured on the bucket — `s06_cors.py` · `CorsOnTheBucket`

SHOW: TRACKER C1 (tracker C appears: "README › data-labeling › CORS & annotate", 6 dots), no
lecture_ref yet (CORS is tutorial-only; a GREY chip says so). V3: two islands labelled with their
origins, `http://localhost:8080` (the page) and `https://storage.googleapis.com` (the photo);
scheme · host · port chips light where they differ. The GREY bouncer stands at the browser's door,
facing the page. A response package arrives with no `Access-Control-Allow-Origin` label → RED X;
the tile stays broken. A rule card slot on the BLUE bucket, empty. A GREY chip: "L10: the Chroma
bouncer · now on a bucket".
SAY: The page comes from localhost 8080, the photo from Google's storage address: a different origin. Your browser hands a cross-origin answer to the page only if it carries a header allowing this origin, and Google adds that header only if the bucket has its own CORS rule. Same bouncer as last lecture, now on a bucket.

SHOW: A kind card, tag `erratum`: README card (`README.md · lines 153, 157`), "reverse DNS lookup"
struck through in GREY → "the browser's same-origin rule + a response header"; "must be done
programmatically" → GREY chip "no CORS editor in the console · `gcloud storage buckets update
--cors-file` also works".
SAY: A small slip: the README blames a reverse DNS lookup, but the cause is that same-origin rule. And though the console has no CORS editor, the gcloud tool can set the rule too.

SHOW: TRACKER C1. CODE(data-labeling/docker-shell-CLI.sh: 23) small, `cheese-app-data-demo` RED. A
strip types the edit (GREY chip "our editor; use yours"; the `sed` of TERM laptop/40's line 1;
folds) → TERM(laptop/40: 2–3), `your-bucket-placeholder` GREEN. `▶ your turn`. TRACKER C2: README
card (`README.md · line 165`, "Run `docker-shell-CLI.sh`", GREY chip "the README names the
script"). It types `sh docker-shell-CLI.sh` → TERM(laptop/41: 3, …, 26–31); `Python 3.12.15` and
`uv 0.13.5` (lines 29–30) with `at the time of recording`; line 27 `Architecture: x86_64` with a
chip "aarch64 on Apple Silicon". The prompt becomes the capture's `app@5bf8945fb887:/app$`. On V7,
the second TEAL house appears on the street. `▶ your turn`.
SAY: The README sets the rule from a second container. Put your bucket name on line 23 of docker-shell-CLI.sh, then run it with sh; the ID in the prompt changes every run, and Apple Silicon says aarch64 where this machine says x86. Pause and do both.

SHOW: CODE(data-labeling/docker-shell-CLI.sh: 15–25): line 17 `--network data-labeling-network`
PINK (V1: the CLI house moves onto the same street); line 19 `-v "$(pwd)/../data-labeling:/app"`
YELLOW, chip "mounted by folder name · keep it data-labeling"; line 24
`-e LABEL_STUDIO_URL="http://data-label-studio:8080"` YELLOW, chip "a name, not localhost ·
scene 7".
SAY: This container joins the same street, mounts the repo by its folder name, so keep that name, and calls Label Studio by name, not localhost.

SHOW: TRACKER C3. At `app@5bf8945fb887:/app$` it types `python cli.py -c` → TERM(laptop/41: 33–34,
…, 65–66; wrap), line 66 RED. `▶ your turn`. TRACKER C4: `python cli.py -m` → TERM(laptop/41:
68–69, …, 100–101; wrap), line 101 RED. `▶ your turn`. CODE(data-labeling/cli.py: 22–34): line 23
`storage_client = storage.Client()` YELLOW, chip "no key path · ADC, as in L10"; lines 26–33 (the
rule) GREEN, line 34 `bucket.patch()` YELLOW.
SAY: Inside, run python cli.py dash c, then dash m; pause and run them. Here both stop at the storage client: file not found, since ADC looks for the key. The code builds one rule, any origin, GET only, max age one hour, and patches the bucket.

SHOW: A GREY card, tag `recorded · cli.py:40 + :26–33`: `set_cors_configuration()` / `Set CORS
policies for bucket <your bucket> is [{'origin': ['*'], 'method': ['GET'], 'responseHeader':
['Content-Type', 'Access-Control-Allow-Origin'], 'maxAgeSeconds': 3600}]`. A second card, tag
`recorded · cli.py:47–72`: `view_bucket_metadata()`, `ID: …`, `Name: …`, `…`, `Cors: […]` YELLOW,
`…`. V3: the rule card sticks onto the BLUE bucket; the next package carries
`Access-Control-Allow-Origin: *` and is waved in; the tile fills (`illustration`, no photo). A GREY tag `maxAgeSeconds: 3600`
clips onto an `OPTIONS` knock drawn dashed, caption "preflights only · a plain GET has none".
SAY: With a real key, dash c prints the rule and dash m the bucket settings. Now the header arrives and the thumbnails load. The max age only caches preflight checks, which a plain image request never makes.

SHOW: The broken grid again (`illustration`).
PONDER(8 s, "You ran cli.py -c and refreshed:\nstill broken thumbnails.\nTwo suspects?")
SAY: Something to ponder. You ran dash c and refreshed, and the thumbnails are still broken. Name two suspects.

SHOW: The answer. Suspect 1: CODE(data-labeling/docker-shell-CLI.sh: 23) with the old name, the
rule card flying to a second, GREY bucket; chip "check with python cli.py -m". Suspect 2: a
refresh arrow, chip "hard refresh · or a private window". The `curl` figure again with a GREY chip
"CORS is not access control · no signed URL → still refused". GREY tag `lecture_ref(11, "13")`
top right for this block (the CLI container of slide 13). Fade out.
SAY: One: the rule went to another bucket, because line 23 kept the old name; dash m tells you. Two: your browser reused cached answers; hard refresh. And curl never met a bouncer: CORS is a browser rule, not access control.

---

## S07 · A label is a record; read it back by name — `s07_labels.py` · `LabelsAndTokens`

SHOW: TRACKER C5. GREY tag `lecture_ref(11, "4, 6, 10, 13")` top right, whole scene. A
labeling-screen wireframe (`illustration`, README.md lines 174–177): one image frame (no photo),
four choices; the cursor clicks `gouda`, then Submit. Its server side, tag `extra · stand-in`:
TERM(laptop/33: 2–4; wrap), `"choices": ["gouda"]` and `HTTP 201` highlighted. `▶ your turn`.
SAY: Back in Label Studio, click a task, pick a cheese, and submit; repeat for a few. Pause and label some. Here is what one click becomes, as a stand-in call: a small JSON document whose result says choices, gouda.

SHOW: V2 step 4: a WHITE envelope with `gouda` flies from Label Studio into `cheeses_labeled/`, a
thin thread tying it back to its photo in `cheeses_unlabeled/`, which never moved. Slide 6's
sorted "Labeled" rows (from V7) morph into a stack of envelopes; GREY chip "the slide draws what
labels mean". TRACKER C6: console `illustration` (README.md lines 184–187): `cheeses_labeled/`
holding "some json files", one per annotation, no object names drawn.
SAY: It lands in the cheeses labeled folder, pointing back at the photo, which never moved. The slide sorts photos into rows, but on disk a label is a small JSON note, and a labeled dataset is photos plus notes. In the console, that folder shows one JSON file per annotation.

SHOW: TRACKER D1 (tracker D appears: "README › data-labeling › View Annotations using CLI", 3
dots). An *Account & Settings* wireframe (`illustration`, README.md lines 193–196), the token
field drawn blank. `▶ your turn`. V1 reprise: the CLI house on the street, an arrow labelled
`localhost:8080` hovering over it.
PONDER(6 s, "Inside the CLI container,\nwhat if LABEL_STUDIO_URL were\nhttp://localhost:8080?")
SAY: To list labels from code, copy your access token from Account and Settings. Pause and copy it. The command line container calls Label Studio by name. Something to ponder: what if its address were localhost 8080?

SHOW: TRACKER D1 · extra. The same CLI session as S06, prompt `app@5bf8945fb887:/app$`:
`curl -sS http://localhost:8080/health` (extra) → TERM(laptop/41: 109), RED;
`curl -s http://data-label-studio:8080/health; echo` (extra) → TERM(laptop/41: 111), GREEN. V1:
the CLI's own `localhost` arrow curls back into its own empty house: refused; the name arrow runs
down the PINK street to Label Studio, a PINK "phone book · Docker DNS" lit; the browser's
`localhost:8080` arrow comes in through the laptop door.
SAY: Connection refused: inside a container, localhost is that container, and nothing listens there. Two extra curls prove it, and the name works, because the Docker network keeps a phone book of container names.

SHOW: TRACKER D2. At `app@eb57c56e6715:/app$` (GREY chip "our capture: a fresh container for each
step · stay in yours"), it types `python cli.py -p -k student-demo-token-not-a-secret` (GREY chip
on the token: "obviously fake") → TERM(laptop/42: 33, 36–38, 43, …, 66; wrap); lines 37 and 43
RED. `▶ your turn`.
SAY: Now the README command: python cli.py dash p, dash k, and your token. Pause and run it. On Label Studio 1.23.0 it fails with a 401: legacy token authentication has been disabled for this organization.

SHOW: TRACKER D2 · extra. Laptop strip: `curl -s -b /tmp/ls.cookies http://localhost:8080/api/jwt/settings`
(extra) → TERM(laptop/27: 2), `"legacy_api_tokens_enabled":false` RED. CODE(data-labeling/cli.py:
75–83): line 79 `label_studio_client = Client(url=LABEL_STUDIO_URL, api_key=api_key)` YELLOW, chip
"the legacy client". The fix on screen: an *Organization → API Tokens Settings* wireframe
(`illustration`) with a "legacy tokens" toggle switching ON; its server side, `extra · stand-in` →
TERM(laptop/43: 2), `"legacy_api_tokens_enabled":true` GREEN. A GREY chip: "other fix: the SDK's
LabelStudio client · exercise".
SAY: An extra check shows why: this version ships with legacy tokens switched off, and cli.py uses the legacy client. The fix is on screen: organization, API token settings, enable legacy tokens, then copy the legacy token. Switching to the newer client is an exercise.

SHOW: TRACKER D2. At `app@e9e15714ac9b:/app$`: the same command → TERM(laptop/44: 33–36), `1 Cheese
labels` GREEN, chip on line 34 "object reprs, not dicts". `▶ your turn`. TRACKER D3:
`python cli.py -t -k student-demo-token-not-a-secret` → TERM(laptop/44: 38–42; wrap);
`Number of tasks: 3` with a chip "ours: 3 · yours: 21", `['gouda']` YELLOW. `▶ your turn`. A README
card (`README.md · line 204`, rendered with `student@example.com`), `'amanita'` GREY, tag
`erratum`, chip "a mushroom from an older course app · same shape".
SAY: Run dash p again, and it lists project 1, cheese labels. Then dash t with your token: 3 tasks in our stand-in, 21 for you, one labeled, as gouda. Pause and run both. The README's sample says amanita, a mushroom from an older course app; same shape.

SHOW: TRACKER D3 · extra. At `app@eb57c56e6715:/app$`: `python cli.py -t` (extra: "forgot -k") →
TERM(laptop/42: 68–69); `i required` GREY, tag `erratum`, chip "cli.py:123 · is required". Fade
out.
SAY: Forget dash k, and the error has a small typo: i required, meaning is required.

---

## S08 · Both containers in one file, and a clean exit — `s08_compose.py` · `ComposeAndClean`

SHOW: TRACKER E1 (tracker E appears: "README › data-labeling › Extra: docker-compose", 2 dots).
GREY tag `lecture_ref(11, "12")` top right, whole scene. A README card (`README.md · lines
218–229`). Laptop prompt `student@laptop:~/data-labeling$`. It types `docker stop data-label-studio`
(GREY chip "README: docker stop <container_name_or_id>") → TERM(laptop/50: 2); `docker ps` →
TERM(laptop/51: 2; squeeze), empty. TRACKER E2: `sh docker-shell-compose.sh` (GREY chip "the
README names the script") → TERM(laptop/52: 26, …, 30; wrap); line 26 GREY "harmless", line 30
RED. On V7 a ghost of the stopped house still holds its name tag.
SAY: The README's extra runs both containers from one compose file. Stop Label Studio, check with docker ps, then run sh docker-shell-compose.sh. Here it stops on a name conflict: docker stop leaves the container behind, still holding its name.

SHOW: TRACKER E2 · extra. `docker rm data-label-studio` (extra) → TERM(laptop/53: 2); the ghost
vanishes. Then `sh docker-shell-compose.sh` → TERM(laptop/54: 28–30); V1's compose overlay drapes
one file over both houses; lines 29–30 `Container data-labeling-data-label-cli-run-ca04106a92f5 …`
YELLOW beside the README card (`README.md · line 95` now lit), chip "the stray line, explained".
`▶ your turn`.
SAY: An extra docker rm frees the name, and the second run works. Then Compose creates Label Studio plus a one-off command line container, which explains a stray line in the README's sample listing.

SHOW: TRACKER E2 · extra. At `app@ce215fc4f7a5:/app$`: `echo $GCS_BUCKET_NAME` (extra) →
TERM(laptop/54: 38), `cheese-app-data-demo` RED; CODE(data-labeling/docker-compose.yml: 13–18),
line 17 RED, tag `erratum`, chip "edit this one too". Then
`python cli.py -p -k student-demo-token-not-a-secret` (extra) → TERM(laptop/54: 40–41, …, 123–124;
wrap), RED; CODE(data-labeling/docker-compose.yml: 19–20) beside it: `depends_on` becomes an order
arrow with a stopwatch reading "started", not "ready". Then
`until curl -s http://data-label-studio:8080/health; do sleep 2; done` (extra; folds) →
TERM(laptop/54: 126–130) (line 126 prints `{"status": "UP"}`, then the prompt and the typed
command continue on the same row); `1 Cheese labels` GREEN; the V1 drawer pulses: "same folder".
SAY: Two real surprises. An extra echo prints the class bucket name: compose keeps its own copy, on line 17 of docker-compose.yml, so edit it too. And the first call is refused: depends on starts Label Studio first, but does not wait until it listens. After an extra wait loop, project 1 is back, because the same folder is mounted.

SHOW: TRACKER F1 (tracker F appears: "README › data-labeling › Docker Cleanup", 4 dots). After the
capture's `exit` (54: 131): `docker ps` (extra) → TERM(laptop/55: 2–3; squeeze), "still Up". Then
`docker container ls` → TERM(laptop/60: 2–3; squeeze); TRACKER F2: `docker stop data-label-studio`
→ TERM(laptop/61: 2); TRACKER F3: `docker system prune` → TERM(laptop/62: 2–8 [y/N] y, 9–13, …, 24),
lines 10 and 13 (`data-labeling-network`) YELLOW; TRACKER F4: `docker image ls` →
TERM(laptop/63: 2–4; squeeze), `1.76GB` and `1.5GB` with `at the time of recording`. On V7 the
houses and the street disappear; the drawer stays. `▶ your turn`.
SAY: Label Studio keeps running after you leave. Then the README's cleanup: list, stop, prune, and list the images; pause and run them. The prune also removed the network, so next time run docker-shell.sh first. The images take 1.5 and 1.76 gigabytes, at the time of recording.

SHOW: The empty lot where the house stood; only the GREY drawer remains, dimmed.
PONDER(6 s, "After docker system prune,\nis your labeled project gone?")
SAY: Something to ponder: after docker system prune, is your labeled project gone?

SHOW: TRACKER F4 · extra. `sudo ls -la docker-volumes/label-studio` (extra) → TERM(laptop/64: 2–9),
`label_studio.sqlite3` GREEN, owner `1001` with a chip "hence sudo". Part-1 close on V7: the
labeling half lit, both BLUE buckets on, the versioning half dark; a YELLOW parked card under it:
"your labels are safe · the photos they point at can change · how do you freeze which photos a
model saw?". Fade to an empty frame (end of part 1).
SAY: No. The database file is still in the mounted folder, and prune never touches folders you mount. Your labels are safe. But the photos they point at can change under them. So how do you freeze exactly which photos a model saw? That is part 2.

---

## S09 · A repo of your own, from the starter — `s09_repo.py` · `YourOwnRepo`

SHOW: No tracker (concept beat). GREY tag `lecture_ref(11, "20, 23, 26")` top right, whole scene.
The hook's overflowing `final-final` strip returns (`illustration`). Slide 20's five reasons as a
card: track changes · roll back · audit · collaborate · save space (the last one YELLOW, "scene
14"). Slide 23's four approaches as four rows: full snapshots · table-based (logs, snapshots) ·
object store (its own history) · file-based (hashes + metadata, git keeps the history); the last
row lights GREEN with a PURPLE chip "DVC · today".
SAY: Part 2, versioning. The lecture gives five reasons to version data: track changes, roll back, audit, work together, and save space. Of its four approaches, we build the file-based one: fingerprints plus a little metadata, with git keeping the history. The tool is DVC.

SHOW: TRACKER G1 (tracker G appears: "README › data-versioning › Prepare Docker and Create Your
Repository", 5 dots). A GREY chip under the tracker: "README @ b240b1a · the course pin". Laptop
prompt `student@laptop:~$`. It types `docker container ls` → TERM(laptop/70: 2; squeeze);
`docker system prune` → TERM(laptop/71: 2–8 [y/N] y, 9); `docker image ls` → TERM(laptop/72: 2–4;
squeeze). `▶ your turn`.
SAY: The data-versioning README starts with the same three cleanup commands. Pause and run them.

SHOW: TRACKER G2. It types `git clone -b data-versioning-ac215 git@github.com:dlops-io/data-versioning.git`
(README.md line 81; folds); no output panel, a GREY chip "this machine has no SSH route to GitHub".
A README card (`README.md · line 84`): "Alternatively, you can clone with HTTPS." It types
`git clone -b data-versioning-ac215 https://github.com/dlops-io/data-versioning.git` (extra: the
README's HTTPS alternative; folds) → TERM(laptop/74: 2). `▶ your turn`. TRACKER G3: `cd data-versioning`
→ (no output); prompt `student@laptop:~/data-versioning$`. `git log -1 --format='%H %ci'` (extra)
→ TERM(laptop/75: 2), `23762e49…` and `2025-10-20` highlighted.
SAY: Then clone the starter branch the README names. Its SSH command needs your key on GitHub; this machine has no SSH route, so the same branch comes over HTTPS, which the README allows. Pause, clone it, and move in. An extra git log shows the starter, from October 2025.

SHOW: A kind card, tag `erratum`: CODE(data-versioning@2515e5e/README.md: 76–82), header "README
today · 2515e5e", line 78 "Clone the `data-versioning-ac215` branch:" over line 81
`git clone -b main git@github.com:dlops-io/data-versioning.git` RED. A small second terminal strip,
title `laptop · second clone in ~/today`, prompt `student@laptop:~/today$`: it types
`git clone -b main https://github.com/dlops-io/data-versioning.git` (extra; folds) →
TERM(laptop/131: 2); prompt `student@laptop:~/today/data-versioning$`; `ls -A` (extra) →
TERM(laptop/137: 2–12), `.dvc`, `.dvcignore` and `cheese_dataset.dvc` RED, chip "came with the
clone". The strip closes; the first terminal returns.
SAY: One note: on the day of the lecture the README changed, and it now says to clone main. That branch brings the instructor's finished DVC files along, as an extra second clone shows; we will see where that bites. This video follows the course's pinned README: the starter branch, plus one fix.

SHOW: TRACKER G3. Prompt `student@laptop:~/data-versioning$`. A README card (`README.md · line
104`, "Why remove `.git`?"). It types `rm -rf .git` → TERM(laptop/76: → (no output)); `git init` →
TERM(laptop/77: 2, …, 15), `master` in line 2 YELLOW. `ls -A` (extra) → TERM(laptop/78: 2–9), a
GREY chip "no .dvc/ · no class tags". `▶ your turn`.
SAY: Remove the old git history, so the code is no longer tied to the class repo, and start fresh with git init. Its hint mentions master, which is why the branch gets renamed next. An extra listing shows 7 files and no DVC folder.

SHOW: TRACKER G4. A GitHub new-repository form (`illustration`, README.md lines 106–110): name
`data-versioning`, ● Private, ☐ README ☐ .gitignore ☐ license. `▶ your turn`. TRACKER G5
(README.md lines 121–125): it types `git branch -M main` → TERM(laptop/79: → (no output));
`git remote add origin git@github.com:YOUR_GITHUB_USERNAME/data-versioning.git` (folds) →
TERM(laptop/80: → (no output)); `git add .` → TERM(laptop/81: → (no output));
`git commit -m "Initial commit"` → TERM(laptop/82: 2–3) (our hash with "yours will differ");
`git push -u origin main` — typed, no output panel; a GREY card "on your machine: your repo on
GitHub shows these 7 files on main". On V7 the GREY repo box lights. `▶ your turn`. Fade out.
SAY: On GitHub, create an empty private repo called data-versioning, with no README, license or gitignore. Then the five commands: rename the branch, add your repo as origin, add, commit, and push. Pause and run them. Your repo now shows the 7 files on main.

---

## S10 · A bucket that looks like a folder — `s10_bucket.py` · `BucketAsFolder`

SHOW: No tracker for this block. GREY tag `lecture_ref(11, "21, 27–34")` top right, whole scene.
Slide 21's two cards redrawn: "Bucket · objects with names + metadata" → "+ tools" → "Data lake ·
the same bucket, plus tools"; of the five tool ticks, "return to earlier versions" lights. Then a
bucket's object list: `images/Image_1.jpg`, `images/Image_2.jpg`, `dvc_store/files/…`; the
"folders" melt into PINK shared prefixes.
SAY: A bucket stores named objects, nothing else. The lecture calls a bucket plus tools a data lake, and versioning is one of those tools. Its folders are only shared name prefixes, which sets a trap.

SHOW: TRACKER H1 (tracker H appears: "README › data-versioning › Set Up GCP Storage and
Credentials", 3 dots + an `extra` row). It types `cd ..` → (no output); prompt
`student@laptop:~$`. `tree -L 2 -I 'cheeses_unlabeled|__MACOSX|ls-api|*.zip' .` (extra; folds) →
TERM(laptop/84: 2–3, …, 18–26); `data-versioning` and `secrets/data-service-account.json`
highlighted, beside a README card (`README.md · lines 140–144`). TRACKER H2: the S03 console
(`illustration`), short: the same `data-service-account`, Storage Admin, JSON key (README.md lines
148–170). `▶ your turn`.
SAY: The secrets folder from part 1 already sits beside this repo, and the README wants the same service account and key: reuse both, as an extra tree view shows.

SHOW: TRACKER H3. Console `illustration` (README.md lines 174–187): bucket `your-bucket-placeholder`
(GREY chip "a new bucket, or part 1's") → "Create folder" `dvc_store/` and `images/`; on V7 the
second BLUE bucket lights. TRACKER H3 · extra (the `extra` row "upload the first photos"): four
blank tiles `Image_1.jpg` … `Image_4.jpg` fly into `images/` (`illustration`). A kind card, tag
`erratum`: README card (`README.md · line 338`), "Upload a few additional images", caption "but no
step uploads the first ones". GOLD `cost_tag()`: "images/: a few hundred kB". `▶ your turn`.
SAY: In your bucket, create two folders in the console: DVC store and images. A small gap: the README never says to put the first photos into images, yet later it says to add more. So upload Image 1 to Image 4 from the zip. Pause and do it; a gold tag, a few hundred kilobytes.

SHOW: TRACKER I1 (tracker I appears: "README › data-versioning › Start the DVC Container", 3
dots + an `extra` row). It types `cd data-versioning` → (no output). CODE(data-versioning@data-versioning-ac215/docker-shell.sh:
5–10), header "starter · docker-shell.sh", lines 7–9 RED, beside a README card (`README.md · lines
201–205`). A strip types the edit (GREY chip "our editor; use yours"; the `sed` of TERM laptop/85's
line 1; folds) → TERM(laptop/85: 2–7), lines 4–6 GREEN. A GREY chip over lines 5–6: "passed in ·
read by nothing" (tag `erratum`). `▶ your turn`.
SAY: In docker-shell.sh, replace the bucket, project and zone with yours. Only the bucket name is ever used; the other two are passed in and ignored. Pause and edit it.

SHOW: A README card (`README.md · lines 215–230`, "About docker-entrypoint.sh"). V4 built stage by
stage over CODE(data-versioning@data-versioning-ac215/docker-entrypoint.sh: 8–13), four boxes
darkening left to right (slides 29–32): **Authenticate** (line 8 and the GREEN key sliding into
gcsfuse's `--key-file`); **Bucket Mounting** (line 10: a PINK `gcsfuse` pipe from the whole BLUE
bucket, `images/` *and* `dvc_store/`, to `/mnt/gcs_data`); **Connecting the Application** (line 13:
a short PINK `mount --bind` pipe from `/mnt/gcs_data/images` to `/app/cheese_dataset`); **Using
the Data** (a PURPLE `dvc` chip sits on the last folder).
SAY: At start, the entrypoint runs the four stages the lecture draws. Authenticate with the key. Mount the whole bucket as a folder, with a tool called gcsfuse. Bind its images folder to the path the app expects, cheese dataset. Then use the data: DVC works on that folder as if it were local.

SHOW: Slide 34's chips over line 10: `gcsfuse` · `--key-file=$GOOGLE_APPLICATION_CREDENTIALS` ·
`$GCS_BUCKET_NAME` · `/mnt/gcs_data` (a GREY chip "two hyphens, full variable name"), and a dashed
fifth chip `--implicit-dirs`, "not passed here" RED: the prefix list from the first block returns,
and only the console-made `images/` shows as a folder. The camera pulls back: the container inside
the GREY laptop; the `/app` window (Docker `-v`) shows the repo on both sides, but the host's
`cheese_dataset/` is dark; two labels, "bind mount · host → container (-v)" and "bind mount ·
inside the container (mount --bind)". GREY notes: "slides: disks → here: a bucket" and "slide 33:
no local copy → DVC keeps one in .dvc/cache (scene 13)".
SAY: The lecture takes the mount line apart: tool, key file, bucket, mount point. One flag is not passed, implicit dirs, so gcsfuse only shows folders made in the console: that was the trap. The slides say disks; they mean this bucket. And despite the slides, DVC still keeps a copy on your disk.

SHOW: CODE(data-versioning@data-versioning-ac215/docker-shell.sh: 17–27): lines 18–20
`--privileged`, `--cap-add SYS_ADMIN`, `--device /dev/fuse` ORANGE; line 21 `-v "$BASE_DIR":/app`
GREY; line 22 `-v "$SECRETS_DIR":/secrets` GREEN; line 23 `-v ~/.gitconfig:/etc/gitconfig` YELLOW,
chip "configure git first, or Docker creates a directory here". Fade out.
SAY: Mounting needs the fuse device and mount rights, hence privileged and the extra capability. The script also mounts your repo, secrets and git config; set up git before the first run, or Docker creates a folder in its place.

---

## S11 · The starter that no longer builds — `s11_build.py` · `StarterFix`

SHOW: TRACKER I2. GREY tag `lecture_ref(11, "26, 29–32")` top right, whole scene. A README card
(`README.md · lines 234–238`): "Make sure you are inside the `data-versioning` folder: `cd
data-versioning`", GREY chip "already inside since scene 9 · this line is for a new terminal".
TRACKER I3: prompt `student@laptop:~/data-versioning$`; it types `sh docker-shell.sh` →
TERM(laptop/86: 2, …, 1075–1081, …, 1125; wrap) (line 1125 cut after `failed to solve:` with `…`);
lines 1075 and 1078–1079 YELLOW, 1081 RED. `▶ your turn`.
SAY: The README says to be inside the data-versioning folder, which you already are, then run sh docker-shell.sh. Pause and run it. On the starter branch, the build dies: package google-cloud-sdk has no installation candidate. The message even names the replacement, google-cloud-cli.

SHOW: A kind card, tag `erratum`: CODE(data-versioning@data-versioning-ac215/Dockerfile: 36),
header "starter · Dockerfile", `google-cloud-sdk` RED; caption "Google renamed the apt package ·
main fixed line 36 in ebf09c8 · the starter branch never got it". TRACKER I3 · extra: a strip types
the fix (tag `extra`; folds) → TERM(laptop/87: 2), `google-cloud-cli` GREEN. `▶ your turn`.
SAY: A small slip, and not your fault: Google renamed the package, the main branch fixed line 36, and the starter never got the fix. Make the same one-word change, as an extra. Pause and edit it.

SHOW: TRACKER I3. It types `sh docker-shell.sh` → TERM(laptop/88: 2–3, …, 27–31); line 3 gets a
GREY chip "slow the first time · at the time of recording", line 30 `Python 3.11.17` with `at the
time of recording`. Then V4 replays broken, one stage per line printed: TERM(laptop/88: 32; wrap) —
stage 1 RED, no key; TERM(laptop/88: 39; from "failed to detect credentials") — stage 2's pipe
never connects; TERM(laptop/88: 41) — a YELLOW sign over the door, "GCS bucket mounted", beside
CODE(data-versioning@data-versioning-ac215/docker-entrypoint.sh: 11) with a chip "printed no matter
what"; TERM(laptop/88: 42) — stage 3 RED. Lines 33–38 and 40 are never printed.
SAY: Run it again. The first build is slow; it installs gcsfuse and the cloud tools. Then the entrypoint runs, and every stage fails the way a missing key fails. Authentication cannot find the key file, so the bucket never mounts. Yet the next line says bucket mounted, because the script prints it no matter what. Then the bind mount fails: special device does not exist.

SHOW: TRACKER I3 · extra. The prompt appears anyway: `root@9a9e6dff5c15:/app#` (TERM(laptop/88: 45)
prompt), chip "no set -e". It types `ls -la cheese_dataset` (extra) → TERM(laptop/88: 46–48), empty,
RED; `which dvc` (extra) → TERM(laptop/88: 50); `dvc --version` (extra) → TERM(laptop/88: 52),
`3.63.0` with "pinned by uv.lock · at the time of recording". A YELLOW rule card parks in the
corner: "`ls cheese_dataset` before `dvc add`".
SAY: And still you get a root prompt, because the entrypoint does not stop at errors. Extra checks: the cheese dataset folder is empty, and DVC 3.63.0 is installed, pinned by the lock file. So the rule for today: list the folder before you add it.

SHOW: The two-view picture with a real key (`illustration`): inside the TEAL container,
`cheese_dataset/` shows four blank image tiles, PINK-piped to the BLUE bucket; on the GREY laptop,
the same folder is dark and empty.
PONDER(8 s, "Inside, ls cheese_dataset lists\nfour photos; on your laptop it's empty.\nIs the mount broken?")
SAY: With a real key, the folder inside lists your four photos. Something to ponder: on your laptop, the same folder is empty. Is the mount broken?

SHOW: The answer: V4's pipes glow inside the container outline only, with a GREY label "the
container's own mounts". The capture's `exit` (88: 66); on the host, prompt
`student@laptop:~/data-versioning$`: `ls -la cheese_dataset` (extra) → TERM(laptop/89: 2–4), the
folder empty, `root` ORANGE, chip "made by the entrypoint's mkdir -p, through /app". A GREY chip:
"here the mount failed · with a real key, this view is the same". Fade out.
SAY: No. Both mounts exist only inside the container. Your laptop sees the empty folder the entrypoint made through the repo mount; an extra listing shows it, owned by root. On your laptop, this folder stays empty.

---

## S12 · Files named by their fingerprint — `s12_fingerprints.py` · `Fingerprints`

SHOW: TRACKER J1 (tracker J appears: "README › data-versioning › Create and View Dataset
Versions", 6 dots). GREY tag `lecture_ref(11, "20, 23, 25")` top right, whole scene. At
`root@60401905a530:/app#` (GREY chip "our capture: a fresh container for each step · stay in
yours"; re-entry as in the conventions: TERM(laptop/90: 27–28, …, 41–42)), it types `dvc init` →
TERM(laptop/90: 46), RED; `ls -A` (extra) → TERM(laptop/90: 50–51), `.dvc` and `.dvcignore` RED,
chip "half-made". An ORANGE picture: a "root" badge inside the container, a "student" badge on the
repo folder on disk, git's ownership check between them, RED.
SAY: Inside the container, run dvc init. On Linux it may stop: the repository path is not owned by the current user. You are root inside, the repo is yours on disk, so git refuses, leaving a half-made folder.

SHOW: TRACKER J1 · extra (tag `extra · Linux`). The capture's `exit` (90: 52); on the host:
`sudo rm -rf .dvc .dvcignore && ls -A` → TERM(laptop/91: 2–10);
`git config --global --add safe.directory /app && cat ~/.gitconfig` (folds) → TERM(laptop/92:
2–6), lines 5–6 GREEN; an arrow `~/.gitconfig` → `/etc/gitconfig` (starter docker-shell.sh line
23). Then `sh docker-shell.sh` → TERM(laptop/93: 27–28, …, 41–42); at `root@d5bf95465b66:/app#`
`dvc init` → TERM(laptop/93: 46, 48, 52) (the analytics box cut to its line 52, GREY chip "opt out:
dvc config core.analytics false"). `▶ your turn`.
SAY: The fix is an extra, for Linux: on your laptop, remove the half-made files and mark slash app as a safe directory in your git config, which the container mounts. Then dvc init works. Pause and run it.

SHOW: Route T, kindly: the second strip returns, title `laptop · second clone in ~/today`, a GREY
chip "if you cloned main". At `root@15ddd4810362:/app#`: `dvc init` → TERM(laptop/145: 47), RED;
`dvc remote add -d cheese_dataset gs://your-bucket-placeholder/dvc_store` → TERM(laptop/145:
49–50; wrap), line 50 RED; `cat .dvc/config` (extra) → TERM(laptop/145: 52–55), line 55
`url = gs://cheese-app-data-versioning/dvc_store` RED, chip "the class bucket". The strip closes.
SAY: If you cloned main, it stops here: DVC is already set up, the remote is refused, and the config still points at the class bucket. Start from the starter, as we did.

SHOW: TRACKER J2. Back at `root@d5bf95465b66:/app#`. A README card (`README.md · line 279`):
`dvc remote add -d cheese_dataset gs://YOUR_BUCKET_NAME/dvc_store`. It types
`dvc remote add -d cheese_dataset gs://your-bucket-placeholder/dvc_store` (YOUR_BUCKET_NAME
replaced; folds) → TERM(laptop/93: 64); `cat .dvc/config` (extra) → TERM(laptop/93: 66–69), GREEN.
On V7 a PINK line runs from the DVC house to `dvc_store/`. `▶ your turn`.
SAY: Then point DVC at the DVC store folder in your bucket, as its default remote. Pause and add it.

SHOW: TRACKER J3. It types `dvc add cheese_dataset` → TERM(laptop/93: 71, 73, 75); `cat cheese_dataset.dvc`
(extra) → TERM(laptop/93: 81–86), lines 82–84 (`d751713988987e9331980363e24189ce.dir`, `size: 0`,
`nfiles: 0`) RED. The YELLOW rule card from S11 flashes.
SAY: Now the trap: the mount failed, so the folder is empty, and dvc add happily versions nothing, zero files. This is why you list first.

SHOW: TRACKER J3 · extra (tag `extra · stand-in`). The capture's `exit` (93: 107); on the host:
`sudo cp ../cheeses_unlabeled/Image_1.jpg ../cheeses_unlabeled/Image_2.jpg ../cheeses_unlabeled/Image_3.jpg ../cheeses_unlabeled/Image_4.jpg cheese_dataset/ && ls -la cheese_dataset`
(folds, small) → TERM(laptop/94: 2–8), caption "where your bucket's images/ would appear". Then
`sh docker-shell.sh` → TERM(laptop/95: 27–28, …, 41–42); at `root@1d462befbcdd:/app#`:
`ls cheese_dataset` (extra) → TERM(laptop/95: 46); `dvc add cheese_dataset` → TERM(laptop/95: 48,
50, 52); `cat cheese_dataset.dvc` (extra) → TERM(laptop/95: 58–63), lines 59–61 YELLOW. `▶ your
turn`.
SAY: Our stand-in copies the four photos in, and we add again: now the pointer file says 4 files, 611,101 bytes, and one fingerprint for the folder. Pause and add yours.

SHOW: V5 in full: four tiles labelled `Image_1.jpg` … `Image_4.jpg` (no photos drawn) drop into a
hash machine; each comes out as its real PINK md5 from TERM(laptop/09b: 2–5) (`5b53853e…`,
`ba044df2…`, `91f482c4…`, `5b85cf7e…`; the first one carries S03's PINK pin) and slides onto a shelf
aisle named by its first two characters: `5b/`, `ba/`, `91/`, and `5b/` again (two tiles share an
aisle; chip "a path, not a meaning"). A manifest card gathers the four `{md5, relpath}` pairs,
sorted, is hashed itself → `89db50de….dir` on aisle `89/`, and shrinks into the six-line GREEN
`cheese_dataset.dvc` (the lines of `95:58–63`). Chips: GREY "fingerprint · slide 25", PINK "md5 ·
DVC".
SAY: Here is what dvc add did. It fingerprinted each photo with MD5, the values from part 1, and filed each copy under its fingerprint, the first 2 characters naming the shelf. Then it fingerprinted a manifest, the list of fingerprints and names, and wrote that into the pointer file.

SHOW: TRACKER J3 · extra. It types `find .dvc/cache -type f | sort` (extra) → TERM(laptop/95:
65–70) under the drawing; each line lights its aisle; line 70 (`d7/51713988987e9331980363e24189ce.dir`)
GREY, chip "the empty version".
SAY: An extra listing of the cache shows those shelves, plus one more: the empty version from before.

SHOW: TRACKER J3 · extra. On the host (the capture's `exit`, 95: 82), a GREY chip "the class repo,
cloned as class-data-versioning (extra)". It types
`git -C class-data-versioning show dataset_v20:cheese_dataset.dvc; echo ---; git -C class-data-versioning show dataset_v21:cheese_dataset.dvc`
(extra; folds, small) → TERM(laptop/120: 2–7) (the v21 half, lines 8–14, not printed here); the
class card slides in beside ours. Then
`diff <(git -C class-data-versioning show dataset_v20:cheese_dataset.dvc) <(git -C data-versioning show dataset_v20:cheese_dataset.dvc) && echo identical`
(extra; folds, small) → TERM(laptop/121: 2), GREEN; the two cards merge into one. S01's PINK line
flies in and lands on it.
SAY: And the payoff: an extra comparison with the instructor's tag in the class repo. Identical: same bytes, same fingerprint, on any machine.

SHOW: The manifest card alone, `Image_2.jpg` highlighted.
PONDER(8 s, "Rename Image_2.jpg → brie_2.jpg,\ndvc add again. Which changes: the photo's\nmd5, the .dir md5, size, nfiles?")
SAY: Something to ponder. You rename Image 2 to brie 2, and add again. Which changes: the photo fingerprint, the manifest fingerprint, the size, or the file count?

SHOW: The answer: on the manifest card one `relpath` rewrites to `brie_2.jpg`; the `.dir` fingerprint
rerolls (shown as `????????….dir`, no invented value); the blob on aisle `ba/`, `size` and `nfiles`
stay GREEN. A misconception chip: "DVC stores whole files, not diffs · one changed pixel = a new
md5, a new blob". Fade out.
SAY: Only the manifest fingerprint, because one name in the list changed. And DVC stores whole files, not differences; one changed pixel means a new fingerprint and a new copy.

---

## S13 · A pointer in git, the bytes in a bucket — `s13_pointer.py` · `PointerAndBytes`

SHOW: TRACKER J4. GREY tag `lecture_ref(11, "22–23, 25, 33")` top right, whole scene. At
`root@1d462befbcdd:/app#` (the same session as S12's last panel; on screen the capture continues):
`dvc push` → TERM(laptop/95: 72–74), line 74 RED. `▶ your turn`. Tag `extra · local remote`:
`dvc remote add --local standin /app/.dvc/tmp/standin-remote` → TERM(laptop/95: → (no output),
the prompt of line 78 returns); `dvc push -r standin` → TERM(laptop/95: 79–81), `5 files pushed`
YELLOW; chip "4 photos + 1 manifest · any remote prints this summary".
SAY: Next, dvc push. Pause and run it. Here it fails without credentials. To show what a push uploads, an extra push goes to a local stand-in remote: 5 files pushed, the four photos and the manifest. A real bucket prints the same summary.

SHOW: `dvc_store/` drawn (`illustration`, drawn from the cache layout of `95:65–69`) as the cache's
mirror: `files/md5/5b/…`, `ba/…`, `91/…`, `5b/…`, `89/….dir`. GOLD `cost_tag()`: "a second copy
of the photos now bills · cents". V6's three-homes panel: `images/` (BLUE, "the folder you upload
to · changes"), `.dvc/cache` (GREY, "your disk · where hashing happens"), `dvc_store/` (BLUE,
"named by fingerprint"). Conflict 9 chip, GREY: "slide 33: no local copy · DVC keeps one".
SAY: In your bucket, the DVC store now mirrors the cache: same shelves, same names. A gold tag: that is a second copy of the photos, still cents. So the bytes now sit in three places: the images folder you upload to, the cache on your disk where hashing happens, and the DVC store, where every file is named by its fingerprint.

SHOW: TRACKER J5. A README card (`README.md · line 312`): "Run these commands **outside the
container**". The capture's `exit` (95: 82); prompt `student@laptop:~/data-versioning$`. It types
`git status` → TERM(laptop/96: 2–18); lines 5–7 (staged by `dvc init`) GREEN, line 12 (`.dvc/config`
modified by `remote add`) YELLOW, lines 13–14 GREY ("our two edits"), line 18 `cheese_dataset.dvc`
YELLOW. `git add .` → TERM(laptop/97: → (no output)); `git commit -m "Track initial cheese dataset with DVC"`
→ TERM(laptop/98: 2–7), chip "6 small text files · no photos"; CODE(data-versioning@data-versioning-ac215/.gitignore:
3) small, `/cheese_dataset` GREEN, and a GREY chip ".dvc/cache: ignored by .dvc/.gitignore".
`▶ your turn`.
SAY: Now git, outside the container. Here, git status shows the DVC files that dvc init already staged, the new pointer file, and your two edits. Add and commit: 6 small text files and no photos, because the git ignore file excludes the dataset folder.

SHOW: It types `git tag -a dataset_v20 -m "First version of cheese dataset"` → TERM(laptop/99: →
(no output)); `git push --atomic origin main dataset_v20` — typed, no output panel; a GREY card "on
your machine: branch and tag arrive together, or neither · the tag appears under Tags on GitHub".
`▶ your turn`. Extras: `git log --oneline --decorate` → TERM(laptop/101: 2–3), `tag: dataset_v20`
GREEN, chip "our hashes · yours differ"; `git show dataset_v20:cheese_dataset.dvc` →
TERM(laptop/102: 2–7). V6: a horizontal git timeline with two beads (Initial commit, the v20
commit); a GREEN flag `dataset_v20` plants on the second; zoom into the bead: the six-line card; a
PINK rope runs from it down into the BLUE `dvc_store/` to the `.dir` box, which fans out to four
blob boxes. A GREY line (slide 25, one level deeper): "git keeps the fingerprint of the list of
fingerprints".
SAY: Tag the commit as dataset v20, and push the branch and the tag together; atomic means both arrive, or neither. Pause and run them. An extra log shows the tag on your commit, and the tag pins these six lines. That is the whole trick: git keeps the fingerprint of a list of fingerprints, and a rope leads from the tag to the bytes in your bucket.

SHOW: A kind card, tag `erratum`: README card (`README.md · line 321`), "this tag is taken", chip
"only in a fork · after rm -rf .git and git init, no tags exist". Then the README's own table
(README.md lines 256–260): Git · code and small DVC metadata files / DVC · large dataset files /
GCS · where DVC stores dataset versions. TRACKER J6: a GREY note "Colab: view dataset_v20 → scene
15 views both versions" (README.md lines 324–328). Fade out.
SAY: The README warns that this tag may be taken; that applies only to a fork, and your fresh repo has no tags. Its table sums it up: git holds code and small DVC files, DVC tracks the dataset, the bucket stores the versions. The notebook comes next in the README; we view both versions there, shortly.

---

## S14 · One more photo: what moves? — `s14_v21.py` · `SecondVersion`

SHOW: TRACKER K1 (tracker K appears: "README › data-versioning › Updated Dataset Version:
dataset_v21", 5 dots). GREY tag `lecture_ref(11, "20")` top right, whole scene. Console
`illustration` (README.md lines 336–341): a fifth blank tile flies into `images/`. The copy, tag
`extra · stand-in`: `sudo cp ../cheeses_unlabeled/Image_5.jpg cheese_dataset/ && ls -la cheese_dataset`
(folds) → TERM(laptop/103: 5–9), line 9 `Image_5.jpg` YELLOW. A GREY chip: "gcsfuse caches listings
· wait a little · ls first". `▶ your turn`.
SAY: Now a second version. Upload a few more photos to the images folder; our stand-in copies in one, Image 5. With a real bucket, the mount can take a little while to notice, so list before you add.

SHOW: V5's shelf with four filled aisles and the `89/` manifest; a fifth tile waits outside.
PONDER(8 s, "Four photos already in dvc_store.\nYou add one. How many objects\nwill dvc push upload?")
SAY: Something to ponder. Four photos are already in the DVC store, and you add one. How many objects will dvc push upload?

SHOW: TRACKER K2. `sh docker-shell.sh` → TERM(laptop/104: 27–28, …, 41–42); at
`root@c7959d5d7f9d:/app#`: `ls cheese_dataset` (extra) → TERM(laptop/104: 46); `dvc add cheese_dataset`
→ TERM(laptop/104: 48, 50, 52); `cat cheese_dataset.dvc` (extra) → TERM(laptop/104: 58–63), lines
59–61 YELLOW; a GREY chip "the class v21: 3280f8f9….dir · a different fifth photo" (laptop/120,
line 10). TRACKER K3: `dvc push` → TERM(laptop/104: 65–67), line 67 RED; tag `extra · local
remote`: `dvc push -r standin` → TERM(laptop/104: 71–73), `2 files pushed` YELLOW. V5: `Image_5.jpg`
→ `54081d12…` (laptop/09b, line 6) onto a new aisle `54/`; the four old tiles light "already on
the shelf"; a new manifest `6b342844….dir` on aisle `6b/`; a counter "2 pushed, not 6". `▶ your
turn` on each README command.
SAY: Two: the new photo and a new manifest. Adding again gives 5 files, 712,574 bytes, and a new manifest fingerprint. The class version 21 has a different one, because its fifth photo was another image. Then push: here the local stand-in shows 2 files pushed, because the four old photos are already on the shelf. That is the saved space the lecture promised.

SHOW: TRACKER K4. The capture's `exit` (104: 74); prompt `student@laptop:~/data-versioning$`. It
types `git status` → TERM(laptop/105: 2–6), line 6 `modified:   cheese_dataset.dvc` YELLOW;
`git add .` → TERM(laptop/106: → (no output)); `git commit -m "Add images to cheese dataset"` →
TERM(laptop/107: 2–3); `git tag -a dataset_v21 -m "Updated cheese dataset with additional images"`
→ TERM(laptop/108: → (no output)); `git push --atomic origin main dataset_v21` — typed, no output
panel. `▶ your turn`. Extras: `git diff HEAD~1 -- cheese_dataset.dvc` → TERM(laptop/110: 7–15),
lines 8–13 YELLOW; `git log --oneline --decorate` → TERM(laptop/111: 2–4); `git tag -n` →
TERM(laptop/112: 2–3). V6: a third bead and a second GREEN flag `dataset_v21`; its rope fans out to
five blobs, four of them shared with v20's rope.
SAY: Back on your laptop, the five git commands again: status shows only the pointer file changed; then add, commit, tag dataset v21, and push. Pause and run them. An extra diff shows the whole change in three lines: the fingerprint, the size and the count. Two flags now sit on two commits, and their ropes share four photos.

SHOW: A kind card, RED, tag `erratum`: README card "starter · README.md · line 148" (`Add a remote
origin git remote add origin git@github.com:YOUR_GITHUB_USERNAME/data-versioning.git`). It types
`git remote add origin git@github.com:YOUR_GITHUB_USERNAME/data-versioning.git` (extra; folds) →
TERM(laptop/113: 2), RED; a README card (`README.md · line 372`): "Do not add it again here."
SAY: The starter branch keeps an older README that adds the remote again at this point. That fails: remote origin already exists. The pinned README says not to.

SHOW: TRACKER K4 · extra. Time travel without the cloud: `git checkout dataset_v20 -- cheese_dataset.dvc && git status --short`
(extra; folds) → TERM(laptop/114: 2); `sh docker-shell.sh` → TERM(laptop/115: 27–28, …, 41–42); at
`root@cae2b394b48b:/app#` `dvc checkout` (extra) → TERM(laptop/115: 49), `ls cheese_dataset`
(extra) → TERM(laptop/115: 51), four names GREEN; exit; `git checkout main -- cheese_dataset.dvc && git status --short`
(extra) → TERM(laptop/116: → (no output)); `sh docker-shell.sh` → TERM(laptop/117: 27–28, …,
41–42); at `root@b505a5708abb:/app#` `dvc checkout` → TERM(laptop/117: 49), `ls cheese_dataset` →
TERM(laptop/117: 51), five names GREEN. On V6 a GREY cursor hops from flag to flag; the blobs come
from the GREY `.dvc/cache`, not the bucket. Fade out.
SAY: One extra experiment: time travel without the cloud. Check out the old pointer file with git, run dvc checkout in the container, and the folder holds four photos again. Back to main, and five. Both come straight from the cache on your disk.

---

## S15 · Time travel from anywhere — `s15_colab.py` · `TimeTravel`

SHOW: TRACKER J6, then K5 on "both versions" (tracker J returns to step 6 with a GREY chip "from
scene 13", then tracker K to step 5). GREY tag `lecture_ref(11, "22, 26")` top right, whole scene.
Slide 22's term card: "time travel · reaching an earlier version · only while its files are kept".
V6's rope pull, `dvc get <repo> cheese_dataset --rev <tag>`: the BLUE Colab box clones the repo at
the tag → reads *that commit's* `.dvc/config` (a chip: "which bucket") → fetches the `.dir`
manifest → then the blobs; four blank tiles materialize in Colab.
SAY: Now, time travel from anywhere: the lecture's phrase for reaching an earlier version, which works only while its files are kept. The command dvc get, with a tag, walks the rope: it clones the repo at that tag, reads that commit's config to find the bucket, fetches the manifest, then the photos.

SHOW: The notebook (`illustration`: a notebook frame, no screenshot; README.md lines 326 and 383,
"Open the Colab Notebook"; slide 26 links the same one). Cells verbatim from
`source/colab/notebook-1RRQ1SlH.cells.txt`: cell 7 `!pip install dvc dvc-gs` (line 47); cell 9's
imports (lines 276–283), chip "keep it: it imports auth"; cell 11 `auth.authenticate_user()`
(line 292); cell 13 `!dvc list -R https://github.com/dlops-io/data-versioning.git` (line 303,
with its comment "Replace github url with your url"); cell 15 `!rm -rf cheese_dataset` /
`!dvc get https://github.com/dlops-io/data-versioning cheese_dataset --force --rev dataset_v21`
(lines 328–329); cell 17 the count (lines 352–353). `▶ your turn`.
SAY: Open the notebook from the README and save a copy. Install DVC, run the imports, and sign in with your Google account. Then list a repo, fetch a version, and count the files. Pause and work through it.

SHOW: Strip `colab stand-in · signed out`, tag `extra`: `dvc --version` → TERM(colab/C07b: 2),
`3.67.1` with chips "today's pip · the notebook ran 3.63.0" and `at the time of recording`.
`dvc list -R https://github.com/dlops-io/data-versioning.git` → TERM(colab/C13: 5; wrap, from
"Anonymous caller"), RED, the tail `…/dvc_store/files/md5/32/80f8f9629451704dca3f792534e1f5.dir' …, 401`
with the `.dir` YELLOW; on V6 the rope stops at the manifest box. Extra, laptop strip:
`curl -s -w '\nHTTP %{http_code}\n' 'https://storage.googleapis.com/storage/v1/b/cheese-app-data-versioning/o?prefix=dvc_store/'`
(folds, small) → TERM(laptop/122: 4–5; wrap), RED.
SAY: Our stand-in is not signed in, and pip gives it a newer DVC, 3.67.1, at the time of recording. Listing the class repo fails with a 401, and look where: at the manifest, because DVC fetches the list first, in the rope's order. The class bucket refuses anonymous callers.

SHOW: A GREY card, tag `recorded · notebook cells 13, 15, 17 · the instructor's run of the class
repo`: cell 13's stored listing (`notebook-1RRQ1SlH.cells.txt` lines 310–314: the five
`cheese_dataset/…` files, the long `.webp` name folded); cell 15's `Downloading cheese_dataset:
0% 0/5` (line 331); cell 17's `Number of items: 5` (line 355). A chip: "your repo: your URL, your
tag · your v20 gives 4". A small GREY chip: "private repo → a token in the URL, or make it public
(exercises)".
SAY: Signed in, the notebook shows five files in the class version 21, and a count of 5. For your repo, replace the address and the tag; your version 20 gives 4. Your repo is private, so the notebook needs an access token in the address, or a public repo.

SHOW: Cell 19 (lines 361–362): `!rm -rf cheese_dataset` /
`!dvc get https://github.com/dlops-io/data-versioning cheese_dataset --force --quiet --rev dataset_v25`;
in the stand-in strip → TERM(colab/C19: → (no output)).
PONDER(6 s, "Cell 19 — dvc get … --quiet\n--rev dataset_v25 — prints nothing.\nDid it work?")
SAY: Something to ponder. Cell 19 asks quietly for dataset v25, and prints nothing. Did it work?

SHOW: The answer: cell 20 → TERM(colab/C20: 2–4), RED; without `--quiet`,
`dvc get https://github.com/dlops-io/data-versioning cheese_dataset --force --rev dataset_v25`
(extra; folds) → TERM(colab/C19b: 2; wrap), `unknown Git revision 'dataset_v25'` RED. Extra, laptop
strip: `git ls-remote --tags https://github.com/dlops-io/data-versioning` → TERM(laptop/118: 2, 4,
6), the three tag names highlighted. V6: a flag that was never planted, its rope ending in air. A
kind card, tag `erratum`: "cell 20's stored `Number of items: 3` (line 370) is left over from an
older run · --quiet hides errors too". Fade out.
SAY: No. The next cell fails: no such folder. Without the quiet flag, the error appears: unknown Git revision. The class repo only has tags v20, v21 and v30. The stored count of 3 under the next cell is left over from an older run; quiet hides errors too.

---

## S16 · Monitoring, teardown and recap — `s16_recap.py` · `Recap`

SHOW: No tracker. GREY tag `lecture_ref(11, "25, 35–36, 38–40")` top right, whole scene. Slide 36
redrawn as three question cards: "Which images trained this model?" · "Can I test new images
before everyone uses them?" · "What did this table hold before the change?"; three tool chips
below, unmatched: DVC · lakeFS · Delta Lake / Iceberg (GREY dashed).
QUICK(4 s, "Which images trained this model? · Can I test\nnew images first? · What did this table hold?\nWhich tool answers each?")
SAY: A quick prediction: which images trained this model? Can I test new images before everyone uses them? What did this table hold before the change? Match DVC, lakeFS, and Delta Lake or Iceberg.

SHOW: The chips land in order: DVC ("uses git") · lakeFS ("its own history") · Delta Lake /
Iceberg ("table versions"). Slide 35's line, GREY: "no single standard". A GREY chip: "Milestone 2
accepts a light tool like this one".
SAY: In that order. There is no single standard; your project milestone accepts a light tool like this.

SHOW: Monitoring, slides only: a GREY-dashed watchtower rises over V7, chip "this lecture has no
monitoring tutorial". Slide 38's five reasons as GREY chips (quality · freshness · drift: "suddenly
far more photos of one cheese" · cost · the broken step); slide 39's three approaches in one line
(rules · anomaly detection · lineage + metadata); slide 40's tools as plain text, no logos. A
YELLOW line: "versioning: what changed · monitoring: that something changed".
SAY: The lecture ends with monitoring, slides only: watch quality, freshness, drift, cost and broken steps, with rules, anomaly detection or lineage. Versioning tells you what changed; monitoring tells you that something changed.

SHOW: TRACKER L1 (tracker L appears: "README › data-versioning › Docker Cleanup", 3 dots). Laptop
prompt `student@laptop:~/data-versioning$`. `docker container ls` → TERM(laptop/150: 2; squeeze);
TRACKER L2: `docker system prune` → TERM(laptop/151: 2–8 [y/N] y, 9, …, 20); TRACKER L3:
`docker image ls` → TERM(laptop/152: 2–5; squeeze), `data-version-cli` `2.73GB` with `at the time of
recording`. `▶ your turn`. Then the shutdown checklist card (GOLD frame), one line per sentence:
"stop and remove `data-label-studio`" · "optional: `python cli.py -r` removes the CORS rule
(cli.py:35–38)" · "`docker-volumes/label-studio`: delete only when done with the project" ·
"buckets bill until deleted: `cheeses_unlabeled/`, `cheeses_labeled/`, `images/`" · RED-outlined:
"never `dvc_store/` while a tag should still work" · "`.dvc/cache`: safe to delete once pushed" ·
"delete the key when the course is done (IAM › Service accounts › Keys)".
SAY: Cleanup is the README's three commands; pause and run them. Then shut down: stop and remove Label Studio. Buckets bill until deleted, but never delete the DVC store while any tag should still work; a tag is only a pointer. Delete the key when you are done.

SHOW: The recap on V7, complete: pieces relight one by one as each is named: the TEAL Label Studio
house with its door and drawer (V1); the BLUE ticket (V2); the bouncer and the rule card on the
bucket (V3); the WHITE envelope with its thread; the FUSE pipes (V4); the hash shelf (V5); the
flags and the rope (V6). Then everything unlit.
SAY: The whole lecture on one map: Label Studio in a container, signed tickets, a bouncer the bucket configures, labels as small notes, a mounted bucket feeding DVC, photos filed by fingerprint, and a tag pinning the list.

SHOW: A card "Test yourself". One question at a time (≥ 24 pt, ≤ 3 lines), each with a thumbnail of
its picture; earlier ones collapse into a label list at left. Q1 "Why does the bucket need a CORS
rule when it is your browser that complains, and why does curl never notice?" (the bouncer) · Q2
"cli.py reaches Label Studio at data-label-studio:8080, you at localhost:8080. Why can't they
swap?" (two arrows) · Q3 "What is inside cheese_dataset.dvc, and which field changes if you rename
one photo?" (the manifest card) · Q4 "After dvc add and dvc push, name the three places the photo
bytes sit." (three homes) · Q5 "You delete gs://…/dvc_store but keep GitHub and its tags. What does
dvc get --rev dataset_v20 do now?" (the rope in air). Labels: "CORS" · "two addresses" · "the
pointer" · "three homes" · "the warehouse".
SAY: 5 questions to test yourself. One: why does the bucket need its CORS rule, when curl never notices? Two: why can the command line container and your browser not swap addresses? Three: what is in the pointer file, and what changes on a rename? Four: where do the bytes sit after a push? Five: without the DVC store, what does dvc get do?

SHOW: The label list stays at left. Footer cards: "Answers: exercises.md" and "Study guide + every
command: MLOps_Learning · guides/L11-data-labeling-versioning.md". A "Next" card, GREY dashed:
"L13 · trains on the labeled cheeses from a prepared zip · swap that download for dvc get --rev to
make a run reproducible". Everything fades to an empty frame (end of part 2).
SAY: Answers are in the exercises, every command in the study guide. In lecture 13 you train from a prepared zip; fetching a tagged version instead makes such a run reproducible.

---

## Lexicon candidates

Words the SAY lines contain that `explainer/lexicon.yaml` has no entry for and Kokoro af_heart may
misread. **Not added**: the lexicon stage checks each with `explainer/voice.py` (phonemes) and adds
only the ones it gets wrong, each with `ipa` + `say`. The SAY lines already avoid a bare "a" and a
`'s` directly before every word below, so no "a X" guard is needed unless the reviewer adds one.
Nothing in the md5 / hash family is spoken: every hash fragment (`89db50de…`, `5b53853e…`,
`d7/…`, `6b342844…`, `3280f8f9…`, `54081d12…`, the commit and container ids) is on screen only.

| word as written in SAY | scenes | intended reading | why it is a candidate |
| --- | --- | --- | --- |
| DVC | S02, S09–S16 | "D V C" | acronym; may be read as a word |
| dvc (in `dvc init`, `dvc add`, `dvc push`, `dvc get`, `dvc checkout`) | S12–S16 | "D V C" | lowercase command name; entries are case-sensitive, so it needs its own |
| gcsfuse | S10, S11 | "G C S fuse" | invented tool name |
| CORS | S05, S06, S16 | "kors" (one syllable) | L10 used it without an entry; confirm it is not spelled out |
| MD5 | S12 | "M D 5" | letter-digit acronym |
| JSON | S03, S07 | "jay-son" | check it is not spelled out |
| docker-shell-CLI.sh | S06 | "docker shell C L I dot S H" | variant of the existing `docker-shell.sh` entry |
| docker-shell-compose.sh | S08 | "docker shell compose dot S H" | same |
| google-cloud-sdk | S11 | "google cloud S D K" | package name |
| google-cloud-cli | S11 | "google cloud C L I" | package name |
| 1.23.0 | S04, S07 | "one point twenty-three point zero" | new `a.b.c` version |
| 1.23.2 | S04 | "one point twenty-three point two" | new `a.b.c` version |
| 3.63.0 | S11 | "three point sixty-three point zero" | new `a.b.c` version |
| 3.67.1 | S15 | "three point sixty-seven point one" | new `a.b.c` version |
| 1.5, 1.76, 3.7, 3.8 | S03, S08 | "one point five", "one point seven six", "three point seven", "three point eight" | two-part numbers (L09 added several such) |
| 1001 | S04 | "ten oh one" | a user id; default reading would be "one thousand one" |
| v20, v21, v25, v30 | S13, S14, S15 | "vee twenty", … | tag names |
| aarch64 | S06 | "A arch sixty-four" | architecture name (L10 said it with no entry; confirm) |
| x86 | S06 | "x eighty-six" | architecture name (L10 likewise) |
| sudo | S04 | "soo-doo" | Unix command |
| chown | S04 | "C H own" | Unix command |
| GET | S06 | "get" | HTTP method in capitals; may be spelled out |
| dirs (in "implicit dirs") | S10 | "durs" | abbreviation of directories |
| lakeFS | S16 | "lake F S" | product name, mixed case |
| gruyere | S04 | "groo-YAIR" | cheese name |
| parmigiano | S04 | "par-mee-JAH-no" | cheese name |
| gouda | S01, S04, S07 | "GOO-da" (or "GOW-da"; pick one) | cheese name, two common readings |
| amanita | S07 | "am-uh-NYE-tuh" | mushroom name |
| E7 | S02 | "E 7" | exercise label |
| PNG | S03 | "P N G" | acronym; probably fine |
