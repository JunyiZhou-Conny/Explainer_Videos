# Brief · AC215 L11 — Data labeling and versioning: where does a label live, and what is a version?

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest), `SLIDES.md` (the lecture-slide digest and scene
map) and `assets/` (real captures, see `ASSETS.md`). **Where the digest or the slides and the
captures disagree, the captures win.** They are newer (2026-10-23 11:42–12:06 UTC) and were made by
running both READMEs' commands as written, in README order — up to the honest, documented failure
wherever a real Google credential, a bucket, GitHub over SSH or a browser would be needed (this
sandbox has none):

| topic | digest / slides | captures (use these) |
| --- | --- | --- |
| which data-versioning README | digest pins `b240b1a` ("clone the `data-versioning-ac215` starter") | the README **moved on lecture day** (`2515e5e`, 2026-10-13): it now says clone `main`. **Decision (taken, not re-opened): teach route S** — README @ `b240b1a` + the starter + the one-line Dockerfile fix, fully captured (`laptop/70`–`122`). Route T's real refusals are a short, kind erratum beat (`131`, `137`, `145`) |
| the starter's build | digest gotcha #1 predicted the apt failure | **live, word for word** (`86`: `E: Package 'google-cloud-sdk' has no installation candidate`); fix `87`; clean build `88` |
| Label Studio API token | digest gotcha #11 guessed "JWT vs legacy" | concrete: Label Studio **1.23.0 ships with legacy tokens OFF** (`27`); `cli.py -p` → `401 … legacy token authentication has been disabled for this organization` (`42`); enabling them (`43`) makes `-p`/`-t` work (`44`). The video shows this fix on screen |
| Label Studio on Linux | digest gotcha #12 ("PermissionError", uid assumed) | live: `Up` (`11`) then `Exited (1)` 25 s later (`12`), Label Studio's own diagnosis (`13`), uid **1001** confirmed (`15`), `chown -R 1001` fixes it (`16`–`18`). An `extra · Linux` step |
| `dvc init` on Linux | digest §10 open question | live: `repository path '/app' is not owned by current user` (`90`), half-made `.dvc/`; fix `git config --global --add safe.directory /app` (`92`). An `extra · Linux` step |
| `N files pushed` | digest: "I expect 5, unverified" | **5** for v20 and **2** for v21 — but only to a **local stand-in remote** (`95`, `104`; tag `extra · local remote`). The GCS push fails honestly (`93`, `95`, `104`) |
| the v20 fingerprint | digest §3.5 reproduced offline | **live**: `89db50de27acfd6822faabc3da39b0a8.dir`, 611101, 4 (`95`), byte-identical to the class repo's `dataset_v20` pointer (`120`, `121`) — the hook's payoff |
| `-p` output shape | digest: dicts | `Project object at 0x…` reprs (`44`) |
| `docker container ls` checkpoint | digest A6: "Up" | momentary on Linux (`11` → `12`) |
| compose "Extra" | digest gotchas #6, #9; `depends_on` "does not wait" | all three live: name conflict (`52`), compose's own bucket name `cheese-app-data-demo` (`54:37-38`), `ConnectionRefusedError` before Label Studio listens (`54:39-124`), then the project **survived** (`54:126-130`) |
| Colab | digest: stored outputs from the instructor's run | the stand-in (signed out) stops at the class bucket's 401 on the `.dir` manifest (`C13`, `C15`); `--quiet` hides `unknown Git revision 'dataset_v25'` (`C19`/`C19b`/`C20`); success is `recorded` from the notebook's stored outputs |
| monitoring | digest §10: "no tutorial" | slides 38–40 cover it conceptually; still no tutorial → **a slides-only beat** (S16) |
| length | digest §8: ≈30 min, ~4,600 words at 155 wpm | series voice ~174 wpm: plan **~4,270 words ≈ 24.5 min narration**, ~29–31 min with typing, output and ponders |

## Audience and goal

An AC215 student who has done L1–L10: they have a GCP project (L1), know images, containers, bind
mounts, Compose, networks and published ports (L2–L4), and — from L10 — service accounts, the
`../secrets` convention, ADC, Docker DNS vs `localhost`, and CORS when a browser calls a container
API. New to them: a labeling tool as a containerized web app, source/target storage and pre-signed
URLs, CORS **on a bucket**, annotations as records, FUSE-mounted buckets, content-addressed storage,
DVC pointers and git tags as dataset versions. They watch with their own clones of
[dlops-io/data-labeling](https://github.com/dlops-io/data-labeling) and
[dlops-io/data-versioning](https://github.com/dlops-io/data-versioning) open, pausing to run each
command. **This lecture stores data in GCS** (a few MB: cents, not dollars) and calls no paid model:
GOLD tags mark where storage starts and doubles, and the video ends on the teardown checklist.

After the video they can:
- run Label Studio with one `docker run`, and read every flag of `docker-shell.sh` as a mount, a
  door, a street or a sticky note (and fix the Linux-only data-folder crash);
- explain who touches the photo bytes: Label Studio lists and signs with the key, the **browser**
  downloads straight from GCS with a short-lived signed URL — and why that makes the *bucket* need
  a CORS rule (enforced by the browser, set on the bucket, ignored by `curl`);
- say what a label is on disk (one JSON record pointing at an unmoved photo), and read labels back
  through the API from a second container by its Docker DNS name — including fixing Label Studio
  1.23's legacy-token 401;
- clone the starter into a repo of their own, fix its one broken Dockerfile line, and explain the
  gcsfuse + `mount --bind` chain (and why the host's `cheese_dataset/` looks empty);
- predict what `dvc add` writes: per-file md5s on a two-character shelf, a `.dir` manifest, a
  six-line pointer — and get the *same* 32 characters as the class's `dataset_v20` from the same
  four photos;
- say where the bytes live (bucket `images/`, `.dvc/cache`, `dvc_store/`), why git holds only the
  pointer, why a second version uploads two objects, and what `dvc get --rev <tag>` walks;
- tear everything down without destroying the one thing their tags depend on (`dvc_store/`).

## Length and parts

~29–31 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm); the plan below
totals **~4,270**. Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S08** (~2,120 words, ~15 min): **labeling** — the hook, the two-station map, the
  key, the photos and the bucket, Label Studio in a box, who touches the bytes (signed URLs), CORS on
  the bucket, labels as records read back by name and token, the compose Extra and cleanup.
- **Part 2 = S09–S16** (~2,150 words, ~15 min): **versioning** — your own repo from the starter,
  the bucket as a folder, the starter's broken line and the entrypoint chain, fingerprints, the
  pointer and the bytes, the second version, time travel from Colab, then monitoring (slides only),
  teardown and recap.

The cut is the lecture's own seam (slide 19's agenda: Labeling | Versioning). Part 1 ends on
**`docker system prune` with the labeled project still on disk** (`64`) and the left half of the
map lit, with one question parked for part 2: "your labels are safe — but the photos they point at
can change under them. How do you freeze *which* photos a model saw?" Part 2 answers it.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop: host shell, host filesystem, the browser's home, the host's (empty) `cheese_dataset/`, `.dvc/cache` on your disk | GREY |
| the cloud: both buckets, `storage.googleapis.com`, `dvc_store/`, the Colab runtime, the signed-URL ticket | BLUE |
| containers and images: `data-label-studio`, `data-label-cli`, `data-version-cli`, the compose one-off | TEAL |
| system-wide / root-owned / host-level power: root-owned folders (uid 1001 vs root; the dubious-ownership check), apt packages (`google-cloud-sdk` → `google-cloud-cli`), `--privileged` / `/dev/fuse` | ORANGE |
| project-owned, protected: the `secrets/` key, the git-tracked DVC files (`.dvc/config`, `cheese_dataset.dvc`), tags as dataset names | GREEN |
| tools: docker, compose, git, dvc, gcsfuse, gcloud, uv, the Label Studio SDK | PURPLE |
| errors and refusals: 400/401, `Exited (1)`, the failed build, the entrypoint's failure chain, route T's refusals, the empty-folder version | RED |
| your turn, the README tracker, the current step | YELLOW |
| money: GCS storage (photos, second copy in `dvc_store/`), what teardown keeps billing | GOLD |
| lookups, paths, routes: the Docker network street + Docker DNS, the mount pipes (gcsfuse, `mount --bind`, `-v`), md5 → `files/md5/xx/…` shelf paths, the tag → pointer → manifest → blob rope | PINK |
| future / elsewhere / lecture-only: L13 training, lakeFS / Delta / Iceberg, monitoring tools, the class repo's bucket | GREY, dashed |

Episode-local semantics (keep consistent): **two buckets, always two BLUE shapes** (`cheese-app-
data-demo` for labeling, the versioning bucket for DVC — SLIDES proposal, so Conflict 1 never needs
explaining twice). The **signed URL is a BLUE ticket with a wax seal and an unlabeled hourglass**
(no expiry value is documented — never print one). An **annotation is a WHITE envelope** (neutral
data) whose label word is the only text inside. **md5 strings are PINK** (they are addresses);
the **pointer file and tags are GREEN** (they are what your repo owns). The `cheese_dataset/`
folder seen from the host is GREY and dark; seen from inside the container through the mount it is
PINK-piped to BLUE.

## Running example

- **The laptop** (a fresh `docker:29.8.2-dind` engine standing in for Docker Desktop,
  linux/amd64): user `student`, home `/home/student` with `data-labeling/`, `data-versioning/`,
  `secrets/` and the extracted `cheeses_unlabeled/` side by side (`84`); terminal title `laptop`,
  prompts `student@laptop:~$`, `…:~/data-labeling$`, `…:~/data-versioning$`. Say once:
  "Architecture: x86_64 here; aarch64 on Apple Silicon — no flags needed" (digest gotcha 21).
- **Inside containers**: `app@<id>:/app$` (data-label-cli; ids change every run, say once),
  `root@<id>:/app#` (data-version-cli — it runs as root, which matters on Linux).
- **The sandbox, honestly** (said once, in S05, then never apologised for): this recording machine
  has no Google credentials, no bucket, no browser and no SSH route to GitHub. The key in the folder
  shots is an obviously invalid stand-in (`06`, 422 B) moved out before every cloud step, so each
  cloud step shows **the exact missing-key failure a student with a misplaced key gets** (L10's
  lesson, again). Successes are `recorded` with a named source; uploads to a bucket are copied in
  locally and tagged `extra · stand-in`; what a push uploads is shown against a local remote tagged
  `extra · local remote`; Label Studio's clicks are its own API calls tagged `extra · stand-in`.
- **Placeholders, everywhere**: login `student@example.com` / `awesome` (the README's password is a
  tutorial default; the address on screen is always the placeholder — quoted lines of
  `docker-shell.sh:19`, `docker-compose.yml:31`, `README.md:109/204/206` show it too, and nothing is
  said about the original); bucket `your-bucket-placeholder`; project `your-gcp-project`; GitHub
  user `YOUR_GITHUB_USERNAME` (the README's own placeholder); token
  `student-demo-token-not-a-secret` (obviously fake, `42`/`44`). **Project id** (series convention,
  as L10 BRIEF:110-113): ours is always `your-gcp-project` (`85`); the README's `ac215-project`
  appears only inside quoted source lines (CODE windows quote it verbatim, never masked) and RED
  story beats — never as ours. The class bucket
  `cheese-app-data-versioning` appears only in quoted README/config lines and RED class-repo beats.
- **Versions**, all "at the time of recording": Docker 29.8.2 / Compose v5.6.0, git 2.54.0; Label
  Studio **1.23.0** from an **unpinned** `heartexlabs/label-studio:latest` (its log says 1.23.2 is
  available, `19`), Django 5.2.17; data-label-cli: Python 3.12.15, uv 0.13.5, label-studio-sdk
  2.0.12, google-cloud-storage 3.4.1; data-version-cli: Python 3.11.17, dvc **3.63.0** (pinned by
  `uv.lock`), gcsfuse **3.13.0** and Google Cloud SDK 590.0.0 (apt, unpinned); Colab's
  `pip install dvc dvc-gs` today gives dvc **3.67.1** (`C07b`). Image sizes 1.5 GB / 1.76 GB /
  2.73 GB (`152`). The md5s, sizes and file counts are deterministic for these photos — say "same
  bytes, same hash" instead of "at the time of recording" for those.
- **Crops** (capture-only artefacts, ASSETS "Capture-only deviations"): the three `Added environment
  https_proxy / GOOGLE_APPLICATION_CREDENTIALS / no_proxy` lines and the gcsfuse JSON INFO lines in
  every DVC-container start (`88`/`90`/`93`/`95`/`104`/`115`/`117`/`145`: lines 33–38, 40); the
  PyPI lines in `19` (8–9); the base-image pull rows; image ids and our commit hashes ("yours will
  differ"). The gcsfuse error line (`88:39`, long) is folded and shown from "failed to detect
  credentials" on.

## Visual set pieces (the 3Blue1Brown part)

Class names in `scenes/common.py`; none collides with a scene class (`video.yaml`).

- **V1 · `StationMap` — slide 13, assembled flag by flag (S04 build, S07 Docker DNS, S08 compose).**
  A TEAL `data-label-studio` house inside the GREY laptop. The `docker run` of
  `docker-shell.sh:12-24` peels off one line at a time and each flag *becomes* a part: `-d` slides
  the house into the background and hands the prompt back; `--network` lays a PINK street under it;
  `-p 8080:8080` cuts a door in the laptop wall; `-v …/docker-volumes/label-studio` is a GREY pipe
  to a drawer (the SQLite file — slide 13's callout 1); `-v ../secrets` a GREEN pipe (the key); the
  `-e` lines stick on as notes (login, key path — callout 2). On Linux the drawer flashes ORANGE:
  root-owned, the house runs as uid 1001, the house falls over (`12`/`13`); `chown` turns it GREY
  and the house stands (`16`–`18`). In S07 a second TEAL house (`data-label-cli`) moves onto the
  same street; two arrows reach Label Studio — the browser through the door (`localhost:8080`), the
  CLI by name down the street (`data-label-studio:8080`, Docker DNS as the street's phone book) —
  and the CLI's own `localhost` arrow curls back into its own empty house: refused (`41:108-111`).
  In S08 one compose file drapes over both houses; `depends_on` is an order arrow with a stopwatch
  that reads "started", not "ready" (`54`).
- **V2 · `SignedTicket` — who touches the bytes (S05, S06 payoff, S07 finale).** Three actors: the
  browser (GREY, on the laptop floor), Label Studio (TEAL), the BLUE vault `cheese-app-data-demo`
  with two drawers, `cheeses_unlabeled/` and `cheeses_labeled/`. (1) *Sync*: Label Studio reaches
  the vault holding the GREEN key, reads 21 names, and 21 task cards fan out. (2) The browser asks
  for card 1; Label Studio stamps a BLUE ticket — the URL, a wax seal (a signature made with the
  key), an hourglass (short-lived) — and slides it across; **the key stays behind**. (3) The browser
  walks the ticket to the vault's own door; the vault checks the seal and hands back the photo …
  which bounces off the bouncer (V3, cliff-hanger). (4, S07) A click on "gouda": a WHITE envelope
  `result → value → choices: ["gouda"]` flies from Label Studio into `cheeses_labeled/`, a thin
  thread tying it back to the photo, which never moved (slide 6's "Labeled" rows morph into this
  stack of envelopes — Conflict 2).
- **V3 · `OriginGate` — CORS, configured on the bucket (S06).** Two islands labelled with their
  origins, `http://localhost:8080` (the page) and `https://storage.googleapis.com` (the photo);
  scheme + host + port chips show they differ. The bouncer stands at the *browser's* door, facing
  the page. A response package arrives with no `Access-Control-Allow-Origin` label → RED X, the
  tile stays broken. `cli.py -c` sticks a rule card onto the bucket (CODE `cli.py:26-33`'s values:
  origin `*`, method `GET`, max age 3600); the next package carries `Access-Control-Allow-Origin: *`
  and is waved in; the tile fills (schematic, no photo). A `curl` figure strolls past (no browser,
  no bouncer). The max-age tag clips onto an OPTIONS knock that this simple GET never makes.
  Callback line: L10's Chroma bouncer, now on a bucket.
- **V4 · `FuseMount` — a bucket that looks like a folder (S10 build, S11 failure replay, S13).**
  Slides 29–32's four stages as four boxes darkening left to right, each lighting one piece of the
  entrypoint: **Authenticate** (the GREEN key into gcsfuse — `--key-file` on line 10; line 8 is
  gcloud's own login, used by neither gcsfuse nor DVC, so it gets only a GREY side note);
  **Bucket Mounting** (a
  PINK `gcsfuse` pipe from the BLUE bucket — the *whole* bucket, `images/` *and* `dvc_store/` — to
  `/mnt/gcs_data`); **Connecting the Application** (a short PINK `mount --bind` pipe from
  `/mnt/gcs_data/images` to `/app/cheese_dataset`); **Using the Data** (PURPLE dvc sits on the last
  folder). Slide 34's chips over the starter's real line (`docker-entrypoint.sh:10`): `gcsfuse` ·
  `--key-file=$GOOGLE_APPLICATION_CREDENTIALS` · `$GCS_BUCKET_NAME` · `/mnt/gcs_data` (two hyphens,
  full variable name — Conflict 10), plus a dashed fifth chip `--implicit-dirs`, "not passed here".
  Camera pulls back: the container inside the GREY laptop; the `/app` window (Docker `-v`) shows the
  repo on both sides — but the host's `cheese_dataset/` is dark (mount namespace): "bind mount" at
  two layers, labelled. S11 replays it broken: stage 1 finds no key, stage 2's pipe never connects,
  stage 3 says "special device does not exist" — and a sign over the door still reads "GCS bucket
  mounted" (the unconditional echo).
- **V5 · `HashShelf` — files named by their fingerprint (S12, S14 reprise, Ponder 8).** Played in
  S12 **as a prediction, before any `dvc add` output** (concept before command; the manifest's
  `.dir` box reads `????????….dir` and the pointer card's fields stay blank until `95:59-61`
  confirms them). Four tiles
  labelled `Image_1.jpg` … `Image_4.jpg` (no photos drawn) drop into a hash machine; each comes out
  as its real PINK md5 (`09b`): `5b53853e…`, `ba044df2…`, `91f482c4…`, `5b85cf7e…`, and slides onto
  a shelf aisle named by its first two characters — `5b/`, `ba/`, `91/`, and `5b/` again (two photos
  share an aisle: it is a path, not a meaning). A manifest card gathers the four `{md5, relpath}`
  pairs, sorted, is hashed itself → `89db50de….dir` on aisle `89/`, and shrinks into the six-line
  GREEN `cheese_dataset.dvc` (`95:57-63`). The real cache listing (`95:64-70`) types in under the
  drawing, including the GREY `d7/5171….dir` — the empty "nothing" version from the failed mount.
  Then the class repo's `dataset_v20` card (`120`) slides in beside ours: the same 32 characters.
  The `121` diff that proves them identical needs our own tag, so it runs in S13, right after `git
  tag` / `git show` (`99`–`102`). S14: `Image_5`
  → `54081d12…` on aisle `54/`; the four old labels light "already on the shelf"; a new manifest
  `6b342844….dir`; the push counter reads 2 (`104`, local remote). Ponder 8: a rename rewrites one
  `relpath` on the manifest card; no photo moves.
- **V6 · `TagRope` — pointer in git, bytes in the bucket (S13, S14, S15).** A horizontal git
  timeline with commit beads (Initial commit, the v20 commit, the v21 commit — `101`/`111`, hashes
  "yours will differ"); GREEN flags `dataset_v20`, `dataset_v21` planted on them. Zoom into a bead:
  the six-line pointer card; a PINK rope runs from it down into the BLUE warehouse `dvc_store/` to
  the `.dir` box, which fans out to four blob boxes; v21's rope fans to five, four of them shared.
  The **three homes of the bytes** panel (Conflict 9): `images/` (BLUE, the mutable workspace you
  upload to), `.dvc/cache` (GREY, your disk — copies made by `dvc add`), `dvc_store/` (BLUE,
  immutable, named by content; never overwritten — this is what freezes a version). S15: `dvc get --rev dataset_v20` pulls the rope — the Colab box clones the repo
  at the tag, reads *that commit's* `.dvc/config` (which bucket!), fetches the manifest first, then
  the blobs; four photos materialize. Failure replays: rope into the class bucket → 401 at the
  manifest (`C13`); a flag that was never planted (`dataset_v25`) → nothing to pull (`C19b`); a burnt
  warehouse → the rope ends in air (recap Q5).
- **V7 · `PipelineMap` — the running map (built S02, part-1 end S08, reopened S09, complete S16).**
  Slide 6 redrawn on top (Unlabeled → the red "How do we do this?" arrow → Labeled → a GREY-dashed
  "training · L13" box), and below it the two stations as the code builds them: the labeling
  station (two TEAL houses on a PINK street in the GREY laptop) ↔ BLUE bucket 1
  (`cheeses_unlabeled/`, `cheeses_labeled/`); the versioning station (TEAL `data-version-cli`) ↔ BLUE
  bucket 2 (`images/`, `dvc_store/`) and your private GitHub repo (GREY, GREEN tag flags); Colab
  (BLUE) as "view versions". A GREY-dashed bridge between `cheeses_labeled/` and `images/` labelled
  "not connected in the code — exercise E7". Each scene lights its piece; S16 adds a GREY-dashed
  monitoring watchtower over the whole thing, then unlights everything for teardown.

## README step tracker (ReadmeTracker, top-left)

Twelve trackers, titled with the README section headings so "step k of N" matches what the viewer
scrolls past. data-labeling README = `README.md` @ `03c3e27`; data-versioning README = `README.md`
@ `b240b1a` (first copy, lines 1–425).

- **A · data-labeling › Setup** (`README.md:11-76`), 6 steps: Clone · secrets folder · Service
  account + key · Download & extract · Bucket + two folders · Upload the 21 images
- **B · data-labeling › Run & set up Label Studio** (`:78-147`), 6 steps: `sh docker-shell.sh` ·
  `docker container ls` · Log in · Create project · Source storage · Target storage
- **C · data-labeling › CORS & annotate** (`:149-187`), 6 steps: Edit bucket name ·
  `sh docker-shell-CLI.sh` · `python cli.py -c` · `python cli.py -m` · Annotate · View in GCS
- **D · data-labeling › View Annotations using CLI** (`:189-207`), 3 steps: Copy the token ·
  `cli.py -p -k` · `cli.py -t -k`
- **E · data-labeling › Extra: docker-compose** (`:214-229`), 2 steps: Stop (`docker stop` /
  `docker ps`) · `sh docker-shell-compose.sh`
- **F · data-labeling › Docker Cleanup** (`:239-246`), 4 steps: `docker container ls` · stop ·
  `docker system prune` · `docker image ls`
- **G · data-versioning › Prepare Docker and Create Your Repository** (`:48-126`), 5 steps: Clean
  Docker (3 commands) · Clone the starter · `cd` / `rm -rf .git` / `git init` · New private repo
  (GitHub) · First push (5 commands)
- **H · data-versioning › Set Up GCP Storage and Credentials** (`:130-187`), 3 steps: secrets
  folder · Service account · Bucket folders `dvc_store/` + `images/` — and the **missing step**
  (upload the first photos to `images/`) as an `extra` row
- **I · data-versioning › Start the DVC Container** (`:191-243`), 3 steps: Edit `docker-shell.sh`
  values · `cd data-versioning` · `sh docker-shell.sh` — the Dockerfile:36 fix as an `extra` row
- **J · data-versioning › Create and View Dataset Versions** (`:250-328`), 6 steps: `dvc init` ·
  `dvc remote add` · `dvc add` · `dvc push` · git status/add/commit/tag/push · Colab `dataset_v20`
- **K · data-versioning › Updated Dataset Version: dataset_v21** (`:332-385`), 5 steps: Upload
  images · `dvc add` · `dvc push` · git ×5 · Colab `dataset_v21`
- **L · data-versioning › Docker Cleanup** (`:403-425`), 3 steps: `docker container ls` ·
  `docker system prune` · `docker image ls`

Steps the READMEs do not have are marked `extra` in the tracker caption and the narration ("this
one isn't in the README"): `git log`, `ls`, `tree`, `md5sum`, `docker container ls -a`, `docker
logs`, the uid check, **`chown -R 1001` (`extra · Linux`)**, the curl checks, the in-container `ls`
/ `echo` / curl lines, **enabling legacy tokens** (`43`, the on-screen fix), `docker rm` before
compose, the wait loop, the volume check, the HTTPS form of the clone (README:84 names it, gives no
command), **the Dockerfile fix** (`87`), `ls cheese_dataset` / `which dvc` / versions,
**`safe.directory` (`extra · Linux`)**, the stand-in copies (`extra · stand-in`), the local remote
(`extra · local remote`), `cat`/`find .dvc/cache`, `git log`/`show`/`diff`/`tag -n`, the local
`dvc checkout` time travel, the class-repo comparisons. S01 and S09's opening are concept beats
with no tracker; S16's monitoring beat has none.

## Scene plan

Notation: `laptop/NN` = `assets/terminal/laptop/NN-*.txt`, `colab/CNN` likewise; line numbers are
file lines (line 1 is the `$` command and is never printed; `[exit N]` is never printed). ▶ =
README command with a `your turn` tag at real checkpoints. CODE(file: a-b) quotes `assets/source/`
at the pin (`data-labeling/`, `data-versioning/` = README @ `b240b1a`,
`data-versioning@data-versioning-ac215/` = the starter, `data-versioning@2515e5e/` = today's README).
`lecture_ref(11, "a–b")` per AC215_SERIES rule 9; spans from SLIDES.md §5.

### Part 1 · Labeling

**S01 · Same names, different data? (~220 words) — `s01_hook.py` · `Hook`.** Cold open, no
tracker; `lecture_ref(11, "20, 24")` on the closing beat. The puzzle, as a picture: two folders side
by side, `cheese_dataset · Monday` and `cheese_dataset · Friday`, each holding `Image_1.jpg …
Image_4.jpg` — same names, same count. Between them, a model card with a down arrow and a "?" (no
invented accuracy numbers: "your model got worse; nobody touched the code"). The question on
screen: *which photos — with which labels — did Monday's model see, and can you get exactly those
back?* The habit everyone has, slide 24 redrawn with **our own invented names** (never the slide's
screenshot): an `ls` that fills with `cheese-final.zip`, `cheese-final-v2.zip`,
`cheese-final-final-v3.zip` … until it overflows — "and which one is final?" Then the teaser line,
alone on a dark frame, PINK: `md5: 89db50de27acfd6822faabc3da39b0a8.dir`. "In about twenty
minutes you will compute this exact string on your own laptop — the same thirty-two characters the
instructor's repo has, from the same four photos. How can one short line pin down six hundred
kilobytes of cheese? And before that: when someone clicks *gouda*, where does that word actually
live?" How to follow along: two repos, Docker Desktop, a GCP project with billing and your own
bucket (GOLD: storage, a fraction of a cent a month), a GitHub account; twelve trackers, `▶ your turn`, the study guide
has every command.

**S02 · Two stations, two buckets (~250) — `s02_map.py` · `TwoStations`.** Tracker A1→A2;
`lecture_ref(11, "4–6, 8–12")`. V7 built: slide 6 redrawn — Unlabeled → "How do we do this?" →
Labeled → Colab — then the stations underneath *as the code builds them*: labeling station ↔
bucket 1, versioning station ↔ bucket 2 + GitHub, Colab as "view versions", training GREY-dashed
"L13" (Conflict 1, said once: "slide 6 shows where this is heading; this lecture builds two
stations, and the code doesn't connect them yet — exercise E7"). Slide 4 in one line: labels are
the ground truth a model is graded against; labeled mistakes become the next dataset version — the
loop that makes this one lecture. **PONDER 1 (8 s)** — slide 8's recall quiz: "Docker network,
cloud credentials, Docker Compose: where will each one show up today?" Answer (slides 10–12, each
chip flying to its spot on the map): the network carries the CLI's calls to Label Studio by name;
the credentials are `../secrets` + `GOOGLE_APPLICATION_CREDENTIALS`, mounted into every container;
Compose is the README's Extra. ▶ clone (README:14) → `laptop/01`; extra `02` (HEAD `03c3e277…`,
2025-10-20 — the course pin); extra `03` (three shell scripts, `cli.py`, three PNG figures — "one
of them, `pipeline-flow.png`, is the map you just saw; no README points to it"). ▶ the `secrets`
folder **next to** the repo (README:31-40) → `04`, `05` (`data-labeling` beside `secrets`). One
line: the same `secrets/` will serve both repos (digest §2's layout) — never inside either.

**S03 · A key, 21 photos and a bucket (~230) — `s03_photos.py` · `KeyAndPhotos`.** Tracker
A3→A6; `lecture_ref(11, "5–6, 11")`. ▶ Service account (README:42-50) as a schematic console
`illustration` (never a screenshot or logo): `data-service-account`, role **Cloud Storage → Storage
Admin**, KEYS → ADD Key → JSON, saved as `secrets/data-service-account.json`. "Same badge as L10,
a storage role this time." Extra `06`: the file is there — tagged `stand-in` (422 B; the narration
promises to explain in S05). One line, kindly: Storage Admin is project-wide; this tutorial needs
object read/write plus `storage.buckets.update` for the CORS patch (digest gotcha 20). ▶ download
(README:64) → `07` (`cheeses_unlabeled.zip`, 3,720,496 bytes; "a browser download works the same —
this is the same URL with curl"); ▶ extract (README:65) → `08` (every image *and* its
`__MACOSX/…/._Image_*` twin). **Quick predict (4 s)**: "the zip held 42 files. How many tasks should
Label Studio make?" → extra `09`: **21** images (incl. `Image_3.png`) + 21 resource forks — upload
only the images, or you get 21 broken tasks (gotcha 22; slide 15–18's curation in one sentence:
throw out junk before it becomes a task). Extra `09b`, planted for part 2: five md5s and sizes —
"hold on to `5b53853e…`; it comes back." ▶ bucket + `cheeses_unlabeled/` + `cheeses_labeled/`
(README:67-72) and ▶ upload the 21 images (README:76) as console `illustration`, bucket named
`your-bucket-placeholder` ("REPLACE WITH YOUR BUCKET NAME" — bucket names are global, slide 34).
GOLD: storage starts here — about 3.8 MB, a fraction of a cent a month (digest §2 estimate; "check
the pricing page"). The first BLUE bucket appears on V7.

**S04 · A whole web app in one docker run (~300) — `s04_studio.py` · `StudioInABox`.** Tracker
B1→B4; `lecture_ref(11, "7, 13–14")`. Slide 7's why in one sentence: a labeling tool, run in your
own container, so no outside labeling service sees your data. V1 in full over
CODE(data-labeling/docker-shell.sh: 6-24) (line 19 shows `student@example.com`): line 6's
`inspect || create` network (L10's idempotent shape), line 9's `rm -f`, then the flag peel-off;
"publish the port" (Conflict 5), the repo's container names, the lecture's "Label Studio Container"
named once. ▶ `sh docker-shell.sh` (README:87) → `10` (crop the pull rows to first/last; the
container id); ▶ `docker container ls` (README:91) → `11`: `Up Less than a second
0.0.0.0:8080->8080/tcp data-label-studio` — the README's checkpoint, met. Extra `12`, 25 s later:
**`Exited (1)`**. **PONDER 2 (6 s)**: "It said Up. Now it says Exited (1). Where do you look first?"
→ extra `13`, `docker logs`: `ERROR: Data directory is not writable: /label-studio/data`, `UID =
1001`, owner `root` — Label Studio's own diagnosis. V1's drawer turns ORANGE: Docker created
`docker-volumes/label-studio` as root (`14`), the image runs as uid 1001 (`15`). The fix,
`extra · Linux` → `16` (`sudo chown -R 1001 docker-volumes/label-studio`); "on Docker Desktop for
Mac this normally doesn't happen". ▶ again → `17`, `18`: Up, and stays up. Extra `19` (crop lines
8–9): `Initializing database..`, `Starting development server at http://0.0.0.0:8080/`, the
"Update available 1.23.0 → 1.23.2" box (the `latest` tag moves — at the time of recording). Extras
`20`–`22`: `{"status": "UP"}`, `302 -> /user/login/`, `<title>Label Studio</title>`. ▶ Log in
(README:108-109) and ▶ Create Project (README:110-115): a schematic login + wizard `illustration`
(Image Classification template, choices `brie`, `gouda`, `gruyere`, `parmigiano`); their server
side, `extra · stand-in`: `23` (`302 -> /`), `24` (`"email": "student@example.com"`), `28` (project
`1` "Cheese labels", the four `<Choice>`s echoed back). "Log in with the username and password
your script sets on lines 19–20."

**S05 · Who touches the bytes? (~290) — `s05_storage.py` · `WhoTouchesBytes`.** Tracker B5→B6;
`lecture_ref(11, "6–7, 13")`. Slide 13 redrawn: "the slide connects the browser only to Label
Studio — yet the photos never pass through it" (Conflict 4). ▶ Source storage (README:121-136) as
a form `illustration` with the README's values: `Google Cloud Storage`, `Cheese Images`, bucket
`your-bucket-placeholder`, prefix `cheeses_unlabeled`, Import Method `Files - …`, *Treat every
bucket object as a source file* (may no longer appear — digest §10, "if you don't see it, carry
on"), **Use pre-signed URLs** on, credentials and project fields empty — "empty means: use the key
the container already has". ▶ Target storage (README:138-147), prefix `cheeses_labeled`. Here the
sandbox framing, said once and plainly (Running example). Extra `29`: `/secrets` inside Label
Studio is empty; the form's *Check Connection*, its own API call (`extra · stand-in`) → `30`:
**`400 … "File /secrets/data-service-account.json was not found."`**; target → `31`: `400 …
"Error validating storage connection"` — "exactly what a misplaced key gives you". *Sync Storage*
with a real key: 21 task cards (`recorded`: README:136 + the 21 images of `09`). Our stand-in
imports three tasks with the same `gs://…/cheeses_unlabeled/Image_N.jpg` URIs a sync creates → `32`
(`"task_count":3` — "you will see 21"). Then V2 steps 1–3: list → task cards → the sealed BLUE
ticket → the browser at the vault's door. **PONDER 3 (8 s)**: "Label Studio holds the key; your
browser never sees it. How can the browser show a *private* photo?" Answer: a pre-signed URL — a
permission for one object, for a short time, signed with the key; the browser carries the ticket,
not the key. Slide 7's "private" made precise (Conflict 3): no outside labeling company sees your
data, but the photos live in your bucket and your browser fetches them straight from Google.
Cliff-hanger: the task grid with broken thumbnails (`illustration`) — README:151 says you'll see a
CORS error here, and you will.

**S06 · CORS: the bouncer, configured on the bucket (~290) — `s06_cors.py` · `CorsOnTheBucket`.**
Tracker C1→C4; `lecture_ref(11, "13")` on the CLI container (CORS itself is tutorial-only, said
so). V3 in full: two origins, the bouncer at the browser's door, the unlabeled package bounced.
Kindly (erratum 6): README:153 blames "reverse DNS lookup" — CORS is the browser's same-origin
rule, satisfied by a response header the *bucket* must send; and :157's "must be programmatic" —
the console has no CORS editor, but `gcloud storage buckets update --cors-file` also works (said,
not run). ▶ Edit the bucket name (README:164) → `40` (`docker-shell-CLI.sh:23` now
`your-bucket-placeholder`; sed is our editor, you use yours). ▶ `sh docker-shell-CLI.sh`
(README:165 says "Run `docker-shell-CLI.sh`") → `41:1-31` (crop the build to first/last rows;
`Container is running!!!`, Python 3.12.15, uv 0.13.5, `app@…:/app$`). CODE(data-labeling/
docker-shell-CLI.sh: 15-25): same street, the repo mounted at `/app` *by its folder name* (gotcha 9
in one line), `LABEL_STUDIO_URL` is a name, not localhost (pays off in S07). ▶ `python cli.py -c`
(README:167) → `41:32-66` (first and last lines: `set_cors_configuration()` … `DefaultCredentialsError:
File /secrets/data-service-account.json was not found.`); ▶ `python cli.py -m` (README:168) →
`41:67-101`, same ending. CODE(data-labeling/cli.py: 22-41): `storage.Client()` with no key path
(ADC — L10's chain), the rule dict, `bucket.patch()`. With a real key — `recorded` (the print at
`cli.py:40`, dict from `:26-33`): `Set CORS policies for bucket <your bucket> is [{'origin': ['*'],
'method': ['GET'], 'responseHeader': [...], 'maxAgeSeconds': 3600}]`; `-m` prints the bucket's
metadata, of which only `Cors:` matters (other values shown as `…`, never invented). The rule
card sticks; V3's next package is waved in; the tile fills (`illustration`). The max-age myth in
one line: it caches *preflights*; plain image GETs have none — if thumbnails stay broken, hard-
refresh. **PONDER 4 (8 s)**: "You ran `cli.py -c`, refreshed — still broken thumbnails. Two
suspects?" Answer: the rule missed your bucket — `-c` failed (an unedited line 23 names the
README's bucket, which is not yours, so `get_bucket` fails outright, `cli.py:25`) or line 23 names
another bucket of yours (check with `-m`) — or the browser reused cached responses without the
header (hard refresh / private window). `curl` would
have fetched the photo all along: CORS is not access control.

**S07 · A label is a record; read it back by name (~310) — `s07_labels.py` · `LabelsAndTokens`.**
Tracker C5→C6, then D1→D3; `lecture_ref(11, "4, 6, 10, 13")`. ▶ Annotate (README:174-177): a
labeling-screen wireframe `illustration` (one image frame, four choices); click **gouda**, Submit →
the server side, `extra · stand-in` → `33`: `{"result": [{"from_name": "choice", "to_name": "image",
"type": "choices", "value": {"choices": ["gouda"]}}]}`, `HTTP 201`. V2 step 4: the WHITE envelope
into `cheeses_labeled/`, its thread back to the unmoved photo; slide 6's sorted rows morph into a
stack of envelopes (Conflict 2: "the slide draws what labels mean; on disk a label is a small
record that points at the photo"). Where the click goes, in order (script v2): Label Studio saves
the annotation in its database (V1's drawer — which is why Ponder 6's answer holds), and the
target storage writes a copy to `cheeses_labeled/` on submit (digest A12, README:184-186; not
captured here). ▶ View in GCS (README:184-186) — `illustration`: "some json files", one per
submitted annotation — **no object name drawn** (not documented); "open one" (README:187) shows the
envelope's shape (`33`). A labeled
dataset = photos ⨝ records; nothing sorted into `brie/`, `gouda/` folders. ▶ The token
(README:193-196): an *Account & Settings* wireframe with the token field drawn blank. V1 reprise —
the CLI house joins the street. **PONDER 5 (6 s)**: "Inside the CLI container, what if
`LABEL_STUDIO_URL` were `http://localhost:8080`?" → extra `41:106-111`, live: `localhost:8080` →
`curl: (7) … Couldn't connect to server`; `data-label-studio:8080/health` → `{"status": "UP"}` —
inside a container, localhost is *that* container; on a shared street, names resolve (slide 10).
▶ `python cli.py -p -k <token>` (README:198) → `42:32-66` (crop the traceback middle): `Response
status code: 401` … **`"Authentication token no longer valid: legacy token authentication has been
disabled for this organization"`**. Why, live: extra `27` — `"legacy_api_tokens_enabled":false`:
Label Studio 1.23.0 turns legacy tokens off by default, and `cli.py` uses the legacy `Client`
(CODE data-labeling/cli.py: 76-88); `27` rides on our scripted login, so it is an output-only
`extra · stand-in` strip, not a typed command. Two kinds of token: the page shows a personal access
token (a JWT) by default, which the legacy client cannot use either (not captured; no panel).
**The on-screen fix**, its own ▶ with a spoken pause: *Organization → API Tokens Settings →
enable legacy tokens* (`illustration`) and its server side, `extra · stand-in` → `43`
(`"legacy_api_tokens_enabled":true`); then the *Account & Settings* wireframe again with two rows,
lower-case "personal access token" and "legacy token" (`illustration`; the 1.23 labels were not
captured), the legacy one lit: copy the legacy token, not the personal one. (The other fix, switching to the
SDK's `LabelStudio` client, is one line here and an exercise.) ▶ again → `44:32-36`: `get_projects`,
`[<…Project object at 0x…>]`, `1 Cheese labels`; ▶ `python cli.py -t -k <token>` (README:199) →
`44:37-42`: `Number of tasks: 3` (stand-in — "yours: 21"), `Number of labeled tasks: 1`, the
`Annotations:` line with `['gouda']`. Kindly: README:204's sample says `'amanita'` — a mushroom from
the course's older app; same shape. Typo, one line: forget `-k` and argparse says `-k argument i
required` (`42:67-69`).

**S08 · Both containers in one file, and a clean exit (~230) — `s08_compose.py` ·
`ComposeAndClean`.** Tracker E1→E2, F1→F4; `lecture_ref(11, "12")`. First `exit` the CLI
container (typed at S07's last prompt, `42:73-74`; README:218's "stop all containers"). ▶ `docker stop
data-label-studio` (README:225) → `50`; ▶ `docker ps` (README:229) → `51` (empty). ▶ `sh
docker-shell-compose.sh` (README:218) → `52`: the harmless `version is obsolete` WARN, then
**`Conflict. The container name "/data-label-studio" is already in use`** — `docker stop` left the
stopped container holding the name (gotcha 6). Extra `53`: `docker rm data-label-studio`. ▶ again →
`54` (crop): compose creates `data-label-studio` and the one-off
`data-labeling-data-label-cli-run-…` — README:95's stray line explained. V1 compose overlay.
Two live surprises, kindly: extra `54:37-38` — `echo $GCS_BUCKET_NAME` prints
**`cheese-app-data-demo`**: compose has its own copy (`docker-compose.yml:17`; erratum 9 — edit it
too); extra `54:39-124` (first/last lines) — the first `cli.py -p` dies with
`ConnectionRefusedError … /api/version`: `depends_on` starts Label Studio first but doesn't wait
until it *listens*; the wait loop → `{"status": "UP"}` → `1 Cheese labels` (`54:125-130`) — **the
project survived** a whole new container, because the same folder is mounted. Extra `55`: Label
Studio still up after the shell exits. ▶ Cleanup (README:243-246): `60`, `61`, `62` (`docker system
prune`: the stopped container **and** `data-labeling-network` deleted — re-run `docker-shell.sh`
before the CLI script next time, gotcha 7), `63` (images 1.5 GB / 1.76 GB — at the time of
recording). **PONDER 6 (6 s)**: "After `docker system prune`, is your labeled project gone?" →
extra `64`: `label_studio.sqlite3` still in `docker-volumes/label-studio` (owned by 1001 — hence
sudo) — prune never touches bind-mounted folders. Part-1 close on V7: the labeling half lit, the
two buckets BLUE; the parked question (Length and parts).

### Part 2 · Versioning

**S09 · A repo of your own, from the starter (~240) — `s09_repo.py` · `YourOwnRepo`.** Opening
concept beat (no tracker), then Tracker G1→G5; `lecture_ref(11, "20, 23, 26")`. Opens on S08's
parked question ("freeze which photos a model saw"), then why not git alone (every clone would
carry every photo version), slide 23's four approaches in one line each, and the one we build:
*file-based* — git versions a small file of fingerprints, a bucket holds the photos (DVC), with a
2 s silhouette of V6; slide 20's five reasons as a quick card (**save space** lit, paid off in
S14). ▶ `cd ..` first (S08 ended in `~/data-labeling`; README:136 wants the clone beside
`secrets/`), then Clean Docker (README:57/65/71) → `70`–`72` (fast; the same three commands as S08).
A GREY chip gives the pinned README's address (`b240b1a`). ▶ Clone the starter
(README:81, SSH): command shown, **no output panel** — "this recording machine has no SSH route to
GitHub; the README's tip says HTTPS works too" → extra `74` (the same branch over HTTPS); extra `75`
(`23762e49…`, 2025-10-20). The erratum beat, kindly, with today's README on screen
(CODE data-versioning@2515e5e/README.md: 76-82 — heading "Clone the `data-versioning-ac215`
branch" over `git clone -b main …`): "the README changed on lecture day and now says `main`. Cloning
`main` brings the instructor's finished DVC files along — extra `137`: `.dvc`, `.dvcignore`,
`cheese_dataset.dvc` came with the clone — and we'll see exactly where that bites. This video
follows the course's pinned README: the starter branch, plus one fix." ▶ `cd data-versioning`
(README:89), ▶ `rm -rf .git` (README:95) → `76`, ▶ `git init` (README:101) → `77` (show the first
hint line and `Initialized empty Git repository`; the `master` hint is why `git branch -M main`
comes next). Extra `78`: seven files, **no `.dvc/`** — a clean start, and no class tags. ▶ New
private repo on GitHub (README:106-110) — `illustration`, no README/licence/.gitignore. ▶ the five
first-push commands (README:121-125) → `79`–`82` (`[main (root-commit) …] Initial commit`, 7 files);
`git push -u origin main` → command shown, success described ("your repo shows seven files on
`main`"), **no panel** (the sandbox's SSH timeout is not a student's error).

**S10 · A bucket that looks like a folder (~290) — `s10_bucket.py` · `BucketAsFolder`.** Tracker
H1→H3, I1; `lecture_ref(11, "21, 27–34")`. Slide 21's two cards: a bucket stores named objects with
metadata — nothing else; a data lake is the same bucket plus tools, and versioning is one of them.
"Folders" are name prefixes (GCS is flat) — which sets up a trap. V4 built stage by stage over
CODE(data-versioning@data-versioning-ac215/docker-entrypoint.sh: 8-13), slide 34's chips over line
10, the dashed `--implicit-dirs` chip ("not passed here — so create `images/` as a folder in the
console"). "The lecture says *disks*; it means the bucket" (Conflict 8). Slide 33's why — one
central dataset, ordinary file paths, no download — and its honest qualifier (Conflict 9): DVC
will still keep its own copy on your disk; S13 shows where. ▶ secrets (README:134-144): reuse part
1's → extra `84` (`data-labeling`, `data-versioning`, `secrets/data-service-account.json` side by
side). ▶ service account (README:148-170): the same `data-service-account` (`illustration`, short).
▶ bucket folders (README:174-187) `dvc_store/` + `images/` (`illustration`) — the second BLUE bucket
on V7 (a new bucket or part 1's both work). Erratum 3, kindly: the README never says to put the
**first** photos into `images/`, yet later says "upload a few *additional* images" — `extra` row:
upload `Image_1`–`Image_4` from the zip (that is what the class's v20 is — S12 proves it). ▶ edit
`docker-shell.sh` (README:197-205) → `85` (lines 7–9: `your-bucket-placeholder`,
`your-gcp-project`, `us-central1-a`; only the bucket name is read by anything — erratum 16, one
line). CODE(data-versioning@data-versioning-ac215/docker-shell.sh: 17-27): `--privileged
--cap-add SYS_ADMIN --device /dev/fuse` in ORANGE — FUSE needs a device and mount rights; the
repo mounted at `/app`, `../secrets`, and `~/.gitconfig` as `/etc/gitconfig` (gotcha 4: configure
git first, or Docker creates a *directory* there). GOLD: `images/` is a few hundred kB.

**S11 · The starter that no longer builds (~260) — `s11_build.py` · `StarterFix`.** Tracker
I2→I3; `lecture_ref(11, "26, 29–32")`. ▶ `cd data-versioning` (README:237), ▶ `sh docker-shell.sh`
(README:243) → `86` (crop to its last lines, 1074–1081 and the final `ERROR: failed to build`):
**`Package google-cloud-sdk is not available … However the following packages replace it:
google-cloud-cli` / `E: Package 'google-cloud-sdk' has no installation candidate`**. Kindly
(erratum 2): Google renamed the apt package; `main` fixed line 36, the starter branch never got the
fix. The fix, `extra` → `87` (line 36 now `google-cloud-cli`, exactly main's `ebf09c8`) — CODE
(data-versioning@data-versioning-ac215/Dockerfile: 36) before, `87` after. ▶ again → `88`: the
build (gcsfuse + google-cloud-cli + uv, slow first time, say once), `Container is running!!!`,
`Python 3.11.17`, and then the entrypoint's honest chain, V4 replayed broken: `ERROR:
(gcloud.auth.activate-service-account) Unable to read file [/secrets/data-service-account.json]`
(`88:32`); gcsfuse's `… failed to detect credentials: open /secrets/data-service-account.json: no
such file or directory` (`88:39`, folded, from "failed to detect" on); **`GCS bucket mounted at
/mnt/gcs_data`** (`88:41`) — printed *unconditionally* (erratum 12: the sign that lies); `mount:
/app/cheese_dataset: special device /mnt/gcs_data/images does not exist.` (`88:42`); and the root
prompt anyway — the entrypoint has no `set -e`. Extras `88:45-52`: `cheese_dataset` empty, `which
dvc` → `/.venv/bin/dvc`, `3.63.0`. The rule: **always `ls cheese_dataset` before `dvc add`.** With a
real key — `illustration` of the working two-view: inside, four images; on the host, nothing.
**PONDER 7 (8 s)**: "With a working key, `ls cheese_dataset` inside the container lists your four
photos — and on your laptop, the same folder is empty. Is the mount broken?" Answer: no — the FUSE
and bind mounts live in the container's mount namespace; the host sees only the empty folder the
entrypoint's `mkdir -p` made through `/app` (extra `89`: it exists, empty, **owned by root**).

**S12 · Files named by their fingerprint (~320) — `s12_fingerprints.py` · `Fingerprints`.**
Tracker J1→J3; `lecture_ref(11, "20, 23, 25")`. Beat order (script v2; concept before command,
coordinator-approved review P3):
1. ▶ `dvc init` (README:269): on a Linux engine → `90:45-51`: `ERROR: unexpected error -
   /app/.git/: repository path '/app' is not owned by current user` and a half-made `.dvc/` — git's
   ownership check (root in the container, `student` on disk; ORANGE).
2. The fix, `extra · Linux` → `91` (remove the half-made files), `92` (`git config --global --add
   safe.directory /app` — on the *host*: the container reads it through the `~/.gitconfig` mount).
   ▶ start the container again, `dvc init` → `93:45-48` (`Initialized DVC repository.`; crop the
   analytics box to one line — opt-out `dvc config core.analytics false`).
3. **Route T, kindly** — if you cloned `main`, this is where it stops: `145:46-55`: `ERROR: failed
   to initiate DVC - '.dvc' exists`; `remote add` → `remote 'cheese_dataset' already exists`; and
   `.dvc/config` still says `gs://cheese-app-data-versioning/dvc_store` — the class bucket, where
   your push would go (S13). Fix: the starter route, as here (chip: rewind to S09, recreate your
   empty GitHub repo first).
4. ▶ `dvc remote add -d cheese_dataset gs://YOUR_BUCKET_NAME/dvc_store` (README:279; ours with
   `your-bucket-placeholder`) → `93:63-69` (`Setting 'cheese_dataset' as a default remote.`, the
   four-line config).
5. **V5 as a prediction, before any `dvc add` output**: the hash machine with `09b`'s real md5s,
   copies filed in `.dvc/cache` on two-character aisles, the manifest hashed to a `????????….dir`
   box, only that fingerprint written into a blank six-line pointer card that "stands in for the
   folder in git". "Fingerprint" is the lecture's word (slide 25); md5 is DVC's.
6. ▶ `dvc add cheese_dataset` (README:293) — first on what the failed mount left → `93:70-86`:
   `md5: d751713988987e9331980363e24189ce.dir`, `size: 0`, **`nfiles: 0`** — "a second trap": the
   same machine, fed nothing (RED; the S11 rule card flashes).
7. The photos, `extra · stand-in` → `94` (Image_1–4 copied into the laptop folder, which the
   container sees through the repo mount because no bucket is mounted; caption "where your
   bucket's images/ would appear") and ▶ again → `95:45-63`: **`md5:
   89db50de27acfd6822faabc3da39b0a8.dir`, `size: 611101`, `nfiles: 4`** — the prediction
   confirmed (the blank fields fill).
8. Extra `95:64-70` — the real cache listing (the GREY `d7/…` leftover too).
9. The hook pays off: "one line pins 600 kB: it fingerprints the list of fingerprints", and extra
   `120` — the class repo's `dataset_v20` pointer beside ours, the same 32 characters. (The `121`
   diff needs our own tag and runs in S13.)
10. **PONDER 8 (8 s)**: "You rename `Image_2.jpg` to `brie_2.jpg` and run `dvc add` again. Which
    change: the photo's md5, the `.dir` md5, `size`, `nfiles`?" Answer: only the `.dir` md5 — the
    manifest's `relpath` changed; the blob, the size and the count did not (exercise E1 has the
    full check). The hook's two folders were the reverse: same names, new bytes. Misconception, one
    line: DVC stores whole files, not diffs — change one pixel and the photo gets a new md5 and a
    new blob.

**S13 · A pointer in git, the bytes in a bucket (~300) — `s13_pointer.py` · `PointerAndBytes`.**
Tracker J4→J5; `lecture_ref(11, "22–23, 25, 33")`. ▶ `dvc push` (README:303) → `95:71-76`: the
honest failure (`ERROR: unexpected error - b/your-bucket-placeholder/o` — no credentials). What a
push uploads, against a local remote, `extra · local remote` → `95:77-81`: **`5 files pushed`** —
four photos + the manifest ("the same summary line any remote prints"). `dvc_store/` drawn
(`illustration`) as the cache's mirror: `files/md5/5b/…`, `ba/…`, `91/…`, `89/….dir` — same paths
(ASSETS: drawn from the live cache layout). GOLD: a second copy of the photos now bills (still a fraction of a cent a month).
V6: the three homes of the bytes (Conflict 9 resolved), then the rope. Said once: `images/` can
change; `dvc_store/` never overwrites, since new bytes get a new name — the answer to S08's parked
question (its card gets a check mark). ▶ On the host, outside the
container (README:312) — ▶ `git status` (README:315) → `96`: `dvc init` already **staged** three
files, `remote add` modified `.dvc/config` again, `cheese_dataset.dvc` untracked (and our
`Dockerfile` / `docker-shell.sh` edits); ▶ `git add .` (`97`), ▶ commit (`98`: `create mode …
cheese_dataset.dvc` — six text files, **no photos**: `/cheese_dataset` is git-ignored,
CODE(data-versioning@data-versioning-ac215/.gitignore: 3), the cache by `.dvc/.gitignore`), ▶ `git
tag -a dataset_v20 -m …` (`99`), ▶ `git push --atomic origin main dataset_v20` (README:319) —
command shown, success described (branch and tag together or neither; the tag on GitHub's *Tags*
list), **no panel**. Extras `101` (`(HEAD -> main, tag: dataset_v20)`), `102` (`git show
dataset_v20:cheese_dataset.dvc` — the six lines the flag pins). The flag plants on V6's bead.
Then, in the second-terminal strip, extra `121`: `diff` of the class repo's `dataset_v20` pointer
against ours → `identical` — same bytes, same hash, on any machine (moved here from S12: it needs
our tag; S01's PINK line lands on it).
Kindly (erratum 8): README:321's "this tag is taken" is true only if you forked — after `rm -rf
.git` and `git init` your repo has no tags at all. Slide 25's line one level deeper (Conflict 7):
git keeps the fingerprint of the *list* of fingerprints. The README's own table (README:256-260):
Git = code and small DVC files, DVC = the dataset, GCS = where versions live.

**S14 · One more photo: what moves? (~260) — `s14_v21.py` · `SecondVersion`.** Tracker K1→K4;
`lecture_ref(11, "20")`. ▶ Upload more photos to `images/` (README:336-341) — `illustration`; the
copy, `extra · stand-in` → `103` (`Image_5.jpg`). One line: gcsfuse caches listings — give it about
a minute, `ls` before `dvc add` (gotcha 18). **PONDER 9 (8 s)**: "Four photos are already in
`dvc_store`. You add one. How many objects will `dvc push` upload?" ▶ `dvc add cheese_dataset`
(README:351) → `104:45-63`: `6b3428441b34d1c1217aa55e963f7716.dir`, `712574`, `5` (ours differs
from the class's v21 — their fifth photo was a Gruyère web image not in the zip; ours is
`Image_5.jpg`). ▶ `dvc push` (README:357) → `104:64-69` (honest failure); `extra · local remote` →
`104:70-73`: **`2 files pushed`** — the new photo and the new manifest; V5's four old aisles light
"already on the shelf" (slide 20's *Efficiency*, with numbers). ▶ git ×5 (README:365-369):
`105` (only `cheese_dataset.dvc` modified), `106`, `107` (1 file, 3 lines), `108`, push shown,
no panel. Extra `110`: the diff — md5, `size` 611101 → 712574, `nfiles` 4 → 5; extras `111`
(two flags on two beads), `112` (`git tag -n`). RED, kindly: the old starter README (line 148)
tells you to add the remote again here — extra `113`: `error: remote origin already exists.`
(README:372's note says don't). Time travel without the cloud, extras `114`–`117`, tagged
`extra · stand-in` (the folder is our unmounted stand-in): `git checkout dataset_v20 --
cheese_dataset.dvc`, then `dvc checkout` inside the container → four photos; back to `main` → five
— from the local cache. **Honest warning, said:** with a real mount `cheese_dataset/` *is* the
bucket's `images/`, so `dvc checkout` deletes and rewrites photos there (v20 removes
`Image_5.jpg`, `main` writes it back); a GREY chip says so. Pauses: K1 (upload), K2 (restart, `ls`,
`dvc add`) and K3 (`dvc push`) each have their own ▶ and spoken pause; the ponder answer and the
push land in separate blocks.

**S15 · Time travel from anywhere (~250) — `s15_colab.py` · `TimeTravel`.** Tracker J6, K5;
`lecture_ref(11, "22, 26")`. Slide 22's term, "time travel", and its condition: an old version can
be read only while its files are kept. V6's rope pull, `dvc get <repo> cheese_dataset --rev <tag>`:
clone at the tag → that commit's `.dvc/config` → the `.dir` manifest → the blobs. ▶ The notebook
(README:326, :383; slide 26 links the same one): cells shown as a notebook-frame `illustration` with
their code verbatim — `!pip install dvc dvc-gs` (cell 7), the imports (cell 9: keep it — it imports
`auth`), `auth.authenticate_user()` (cell 11), `dvc list -R` (13), `dvc get … --rev dataset_v21`
(15), the count (17). In our signed-out stand-in container, `extra` → `C07b` (`3.67.1` — today's
pip, not the notebook's 3.63.0), `C13`/`C15` (crop): the class bucket answers **401 on the `.dir`
manifest** (`…/dvc_store/files/md5/32/80f8f9….dir`) — DVC fetches the manifest first, exactly the
rope's order; extra `122` — anonymous listing of the class bucket is refused. What success looks
like — `recorded`, the notebook's stored outputs (`source/colab/notebook-1RRQ1SlH.cells.txt`, cells
13/15/17, the instructor's run of the **class** repo): five `cheese_dataset/…` files, a five-file
download, `Number of items: 5` — said as "the instructor's signed-in run" (cell 13 lists the class
repo's `main`, the same five files as its v21); a viewer's own account probably cannot access the
class bucket. For *your* repo: replace the URL and the tag (the edited cell 15 shown with
`YOUR_GITHUB_USERNAME` and `--rev dataset_v20`); your v20 gives four (narration only — follows from
`95`). Your repo is private (README:108): Colab's anonymous clone needs a read-only token URL (a
`<read-only token>` placeholder chip) or a public repo (gotcha 13a, one line). **The notebook's ▶
comes after these instructions**, at the end of the `recorded` block, not on the first notebook
frame. A GREY chip: today's README links a newer copy (`18KYngbv`, same cells, a TA's repo).
**PONDER 10 (6 s)**: "Cell 19
— `dvc get … --quiet --rev dataset_v25` — prints nothing. Did it work?" → `C19` (nothing, exit 1),
`C20` (`FileNotFoundError: … 'cheese_dataset'` — one cell later), `C19b` without `--quiet`:
**`unknown Git revision 'dataset_v25'`**; extra `118`: the class repo has only `dataset_v20`,
`v21`, `v30`. Kindly (errata 14): the stored `Number of items: 3` under cell 20 is left over from a
2024 run; and `--quiet` hides errors too.

**S16 · Monitoring, teardown and recap (~230) — `s16_recap.py` · `Recap`.** Tracker L1→L3;
`lecture_ref(11, "25, 35–36, 38–40")`. Beat order (script v2): quick predict → monitoring → recap
on V7 → Test yourself → README cleanup + teardown checklist → footer / Next (the checklist confirms
recap Q5 instead of answering it in advance). The recap closes the hook: "Monday's photos come back
with one `dvc get`; their labels join in exercise E7". Slide 36 redrawn as a **quick predict (4 s)**,
tools spoken in shuffled order so the answer is not given away: three questions, three tools — "which images trained this model?" (DVC, uses git), "can I test new images
before everyone uses them?" (lakeFS, its own history), "what did this table hold before the
change?" (Delta Lake / Iceberg, table versions); slide 35's "no single standard". One line for the
project: Milestone 2 accepts a light tool like this one. **Monitoring — slides only**, GREY dashed,
said plainly ("this lecture has no monitoring tutorial"): slide 38's five reasons (quality,
freshness, drift — "suddenly far more photos of one cheese", cost, the broken step), slide 39's
three approaches (rules, anomaly detection, lineage + metadata) in one line; hook callback:
*versioning tells you what changed; monitoring tells you that something changed.* No tool logos
(names as text only, slide 40). ▶ Cleanup (README:410/418/424) → `150`, `151` (prune), `152` (2.73
GB `data-version-cli` — at the time of recording). Teardown checklist (GOLD), below. V7 complete,
then unlit. "Test yourself", five questions one at a time with a thumbnail of their picture
(answers in exercises.md) — see Recap questions. Footer cards: exercises.md and the study guide
(`MLOps_Learning · guides/L11-data-labeling-versioning.md`). Next, GREY dashed: L13 trains on the
labeled cheeses from a prepared zip — swapping that download for `dvc get --rev` is how you'd make
a run reproducible.

## Word budget

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 220 | S09 YourOwnRepo | 240 |
| S02 TwoStations | 250 | S10 BucketAsFolder | 290 |
| S03 KeyAndPhotos | 230 | S11 StarterFix | 260 |
| S04 StudioInABox | 300 | S12 Fingerprints | 320 |
| S05 WhoTouchesBytes | 290 | S13 PointerAndBytes | 300 |
| S06 CorsOnTheBucket | 290 | S14 SecondVersion | 260 |
| S07 LabelsAndTokens | 310 | S15 TimeTravel | 250 |
| S08 ComposeAndClean | 230 | S16 Recap | 230 |
| **part 1** | **2,120** | **part 2** | **2,150** |

Total ≈ **4,270** words ≈ 24.5 min of narration; typing, outputs and ponder timers bring it to
~29–31 min.

## Ponder questions (summary)

Ten timed ponders and two quick predicts — about one every 2.5 minutes (AGENTS content gate 3).
Each is answerable from the picture or capture shown just before it.

| # | scene | question (as on the card) | answer (said right after the timer) |
| --- | --- | --- | --- |
| 1 | S02 (8 s) | "Docker network, cloud credentials,\nDocker Compose: where will each\none show up today?" | Network: the CLI reaches Label Studio by name on `data-labeling-network`; credentials: `../secrets` + `GOOGLE_APPLICATION_CREDENTIALS` in every container; Compose: the README's Extra (slides 8–12) |
| q | S03 (4 s) | "The zip held 42 files.\nHow many tasks should\nLabel Studio make?" | 21 — the other 21 are `__MACOSX` resource forks; don't upload them (`09`, gotcha 22) |
| 2 | S04 (6 s) | "It said Up.\nNow it says Exited (1).\nWhere do you look first?" | `docker logs data-label-studio` — Label Studio explains itself: data dir not writable, uid 1001 vs root (`13`) |
| 3 | S05 (8 s) | "Label Studio holds the key;\nyour browser never sees it.\nHow can it show a private photo?" | A pre-signed URL: one object, short-lived, signed with the key; the browser carries the ticket, not the key (digest §3.2) |
| 4 | S06 (8 s) | "You ran `cli.py -c` and refreshed:\nstill broken thumbnails.\nTwo suspects?" | The rule missed your bucket: `-c` failed (an untouched README name is not your bucket, so `get_bucket` fails outright, `cli.py:25`), or line 23 names another bucket of yours — check `-m`; or cached responses without the header (hard refresh); `curl` never cared (digest gotcha 10) |
| 5 | S07 (6 s) | "Inside the CLI container,\nwhat if `LABEL_STUDIO_URL` were\n`http://localhost:8080`?" | It cannot connect (`curl: (7) … Couldn't connect to server`) — localhost is the CLI container itself; the name works on the shared network (`41:106-111`, live) |
| 6 | S08 (6 s) | "After `docker system prune`,\nis your labeled project gone?" | No — `label_studio.sqlite3` lives in the bind-mounted `docker-volumes/label-studio` (`64`); prune removed the container and the network (`62`) |
| 7 | S11 (8 s) | "Inside, `ls cheese_dataset` lists\nfour photos; on your laptop it's empty.\nIs the mount broken?" | No — the FUSE and bind mounts exist only in the container's mount namespace; the host sees the empty folder `mkdir -p` made (`89`, digest §3.7) |
| 8 | S12 (8 s) | "Rename `Image_2.jpg` → `brie_2.jpg`,\n`dvc add` again. Which change: the photo's\nmd5, the `.dir` md5, size, nfiles?" | Only the `.dir` md5 (the manifest's relpath); blob, size and count unchanged (digest §3.5, E1) |
| 9 | S14 (8 s) | "Four photos already in `dvc_store`.\nYou add one. How many objects\nwill `dvc push` upload?" | Two: the new photo and the new manifest (`104`: `2 files pushed`, local remote) |
| 10 | S15 (6 s) | "Cell 19 — `dvc get … --quiet\n--rev dataset_v25` — prints nothing.\nDid it work?" | No: `--quiet` hid `unknown Git revision 'dataset_v25'` (`C19b`); the failure surfaces in cell 20 (`C20`) |
| q | S16 (4 s) | "Which images trained this model? · Can I test\nnew images first? · What did this table hold?\nWhich tool answers each?" | DVC · lakeFS · Delta Lake / Iceberg (slides 25, 36) |

## Recap questions (S16 "Test yourself"; answers in exercises.md)

1. Who fetches the photos, and why does that make the *bucket* need a CORS rule — and why does
   `curl` never notice? (Spoken: "who fetches the photos, and why does the bucket need its CORS
   rule?"; it also tests the signed-URL outcome.)
2. `cli.py` reaches Label Studio at `data-label-studio:8080`, you at `localhost:8080`. Why can't
   they swap?
3. What exactly is inside `cheese_dataset.dvc`, and which field changes if you rename one photo?
4. After `dvc add` and `dvc push`, name the three places the photo bytes live.
5. You delete `gs://…/dvc_store` but keep GitHub and its tags. What does `dvc get --rev dataset_v20`
   do now?

(Digest recap Q4 — "why `--privileged` with `/dev/fuse`?" — and SLIDES' additions go to
exercises.md.)

## Errata and version drift to state (kindly, with the fix)

1. **Today's README says clone `main`** (`2515e5e`, pushed on lecture day; README:78 heading still
   names the starter over `git clone -b main`). `main` carries the instructor's `.dvc/` and
   `cheese_dataset.dvc` (`137`), so `dvc init` and `dvc remote add` refuse and `.dvc/config` keeps
   the **class bucket** — the push goes there and is refused (`145`). Also a doubled `cd` (`133`) and
   `remote set-url` before any remote (`138`) — exercises only. Fix: the course's pinned README —
   the `data-versioning-ac215` starter + erratum 2 (S09 named, S12 the refusals).
2. **The starter no longer builds** (`86`, word for word): `google-cloud-sdk` → `google-cloud-cli`
   on `Dockerfile:36`, exactly main's `ebf09c8` (`87`) (S11).
3. **Label Studio 1.23.0 disables legacy API tokens by default** (`27`); `cli.py`'s legacy client
   gets `401 … legacy token authentication has been disabled` (`42`). Fix on screen: Organization →
   API Tokens Settings → enable legacy tokens (`43` → `44`); or switch to the `LabelStudio` client
   (exercise) (S07).
4. **Linux only: Label Studio's data folder** (`12`–`13`): Docker creates it as root, the image runs
   as uid 1001. Fix `sudo chown -R 1001 docker-volumes/label-studio` (`16`), `extra · Linux` (S04).
5. **Linux only: `dvc init` and git's ownership check** (`90`): fix `git config --global --add
   safe.directory /app` on the host (`92`), `extra · Linux` (S12). Docker Desktop on macOS not
   tested here — say "if you see this".
6. **README:153's CORS explanation** ("reverse DNS lookup") is not how CORS works — it's the
   browser's same-origin rule and a response header; :157's "must be programmatic" — `gcloud
   storage buckets update --cors-file` also works (S06).
7. **Missing step: the first photos** — README:180-187 never says to upload any to `images/`, yet
   :338 says "additional" (S10 `extra` row; S12 shows what an empty folder gets you).
8. **The tag disclaimer** (README:321, :371) only applies to forks; after `rm -rf .git` + `git
   init` no tag is taken (S13).
9. **Compose has its own bucket name** (`docker-compose.yml:17`; `54:37-38` prints
   `cheese-app-data-demo`) — edit it too (S08).
10. **`docker stop` leaves the container** → compose's name conflict (`52`); fix `docker rm` (`53`)
    (S08). **`depends_on` doesn't wait** (`54`): wait for `/health` (S08).
11. **The unconditional "GCS bucket mounted"** (`88:41`, entrypoint line 11 on the starter) and no
    `set -e`: check `ls cheese_dataset` before `dvc add` (S11).
12. **Small README/code slips**: the `'amanita'` sample (README:204), the stray compose line in the
    sample `docker container ls` (README:95), "Pipfiles" (README:162), the `-k argument i required`
    typo (`cli.py:123`, `42`), "Docker>Preferences" (README:18 — now Settings) — one line each,
    where they appear (S04, S07, S08).
13. **The old starter README repeats `git remote add origin`** for v21 (line 148) → `error: remote
    origin already exists.` (`113`); the pinned README:372 says don't (S14).
14. **Colab**: `dataset_v25` doesn't exist and `--quiet` hides the error (`C19`/`C19b`/`C20`); cell
    20's stored "3" is a stale 2024 output; the defaults point at the class repo and bucket, which
    you cannot read (`C13`, `122`); a private repo needs a token URL; today's pip gives dvc 3.67.1
    (`C07b`) (S15).
15. **Slides vs code, one kind line each** (SLIDES conflicts): labels flow to Colab training (1, S02),
    labeled photos sorted into rows (2, S07), "nothing uploaded externally" (3, S05), slide 13's
    missing traffic lines (4, S05/S07), names (5, S04), `gcs://` → `gs://` (6, only if the curation
    path appears), git records the manifest's fingerprint (7, S13), "disks" (8, S10), "no local copy"
    (9, S10/S13), the em-dash `—key-file` chip (10, S10).
16. **Unused env vars**: `GCP_PROJECT` / `GCP_ZONE` are passed everywhere and read by nothing
    (S10, one line).
17. **Version drift, "at the time of recording"**: every number in the Running-example list; the
    unpinned `label-studio:latest` (its form fields may differ from the README — "if a field is
    missing, carry on"); gcsfuse and gcloud from apt, unpinned.

## Costs and teardown

This lecture **stores data in GCS** and calls no paid API. GOLD tags exactly where storage starts:
- **S03**: bucket 1 + the 21 photos (~3.8 MB; "a fraction of a cent a month — check the pricing
  page"; digest §2 estimate, never an exact amount).
- **S10**: bucket 2's `images/` (a few hundred kB).
- **S13**: `dvc push` stores a second copy in `dvc_store/`; S14 adds only what changed.
Label Studio, the CLI containers and DVC run locally, free.

Teardown, captured: `docker stop` / `docker rm` / compose (`50`–`53`), `docker system prune` (`62`:
container **and** network; `151`), image list (`63`, `152`). The checklist card (S16):
- containers and the labeling network: already gone (S08's stop + prune; `--rm` cleans the others);
- keeping bucket 1? remove its CORS rule with `python cli.py -r` (`cli.py:35-38`), spelled runnable
  after the prune: in `data-labeling`, `sh docker-shell.sh`, then `sh docker-shell-CLI.sh`,
  `python cli.py -r`, `exit` (the CLI script joins the network but does not create it); deleting
  the bucket removes its rule too — said once;
- delete `docker-volumes/label-studio` only if you no longer need the project (it survives prune —
  `64`; `sudo` on Linux, owned by 1001);
- buckets bill until deleted: `cheeses_unlabeled/`, `cheeses_labeled/`, `images/` when you're done
  — but **never `dvc_store/` while any tag should still work** (a tag is a pointer; the warehouse is
  the coat room — recap Q5);
- `.dvc/cache` can be deleted safely once pushed (`dvc pull` restores it);
- delete the service-account key **and** its JSON in `secrets/` when the course is done (IAM →
  Service accounts → Keys; card and narration say the same);
- optional GREY line: `docker image rm data-label-cli data-version-cli
  heartexlabs/label-studio:latest` frees about 6 GB (prune keeps images).

## README commands checklist (for the follow-along review)

Every README instruction, verbatim, in README order.

**data-labeling README @ `03c3e27`**

| README instruction | README line | scene |
| --- | --- | --- |
| Clone the repo (prerequisite) | 14 | S02 (`01`) |
| Docker memory > 4 GB (now *Settings → Resources*) | 18 | S02 (one line) |
| `secrets` folder next to `data-labeling` | 31-40 | S02 (`04`, `05`) |
| Console: `data-service-account`, Storage Admin, JSON key → `secrets/data-service-account.json` | 42-50 | S03 (`illustration`; `06` stand-in) |
| Download `cheeses_unlabeled.zip`; extract | 64-65 | S03 (`07`, `08`) |
| Bucket + `cheeses_unlabeled` + `cheeses_labeled` | 67-72 | S03 (`illustration`) |
| Upload the images to `cheeses_unlabeled` | 74-76 | S03 (`illustration`) |
| `sh docker-shell.sh` | 87 | S04 (`10`, `17`) |
| `docker container ls` | 91 | S04 (`11`, `18`) |
| Open `http://localhost:8080/`, log in | 108-109 | S04 (`illustration`; `20`–`24` server side) |
| Create Project, Image Classification, four labels | 110-115 | S04 (`illustration`; `28` stand-in) |
| Settings → Cloud Storage → Add Source Storage (fields), Check Connection, Add, Sync | 121-136 | S05 (`illustration`; `29`–`30`, `32` stand-in) |
| Add Target Storage (fields), Check Connection, Add | 138-147 | S05 (`illustration`; `31`) |
| Change the bucket name in `docker-shell-CLI.sh` | 164 | S06 (`40`) |
| Run `docker-shell-CLI.sh` | 165 | S06 (`41`, typed as `sh docker-shell-CLI.sh`) |
| `python cli.py -c` | 167 | S06 (`41`; success `recorded`) |
| `python cli.py -m` | 168 | S06 (`41`; success `recorded`) |
| Annotate a few images | 174-177 | S07 (`illustration`; `33` stand-in) |
| View `cheeses_labeled` in the GCS browser | 184-186 | S07 (`illustration`) |
| User Profile → Account & Settings → copy the Access Token | 193-196 | S07 (`illustration`; legacy-token fix `27`, `43`) |
| `python cli.py -p -k` + token | 198 | S07 (`42` 401, `44` after the fix) |
| `python cli.py -t -k` + token | 199 | S07 (`44`) |
| Stop all containers; run `docker-shell-compose.sh` | 218 | S08 (`50`, `52`–`54`) |
| `docker stop <container_name_or_id>` / `docker ps` | 225, 229 | S08 (`50`, `51`) |
| Docker Cleanup: `docker container ls`, stop, `docker system prune`, `docker image ls` | 243-246 | S08 (`60`–`63`) |

**data-versioning README @ `b240b1a`** (route S; starter `23762e4`)

| README instruction | README line | scene |
| --- | --- | --- |
| `docker container ls` / stop / `docker system prune` / `docker image ls` | 57-71 | S09 (`70`–`72`) |
| `git clone -b data-versioning-ac215 git@github.com:dlops-io/data-versioning.git` | 81 | S09 (command; HTTPS alternative `74`, README:84) |
| `cd data-versioning` | 89 | S09 |
| `rm -rf .git` | 95 | S09 (`76`) |
| `git init` | 101 | S09 (`77`) |
| Create a private, empty GitHub repo `data-versioning` | 106-110 | S09 (`illustration`) |
| `git branch -M main` · `git remote add origin git@github.com:YOUR_GITHUB_USERNAME/data-versioning.git` · `git add .` · `git commit -m "Initial commit"` · `git push -u origin main` | 121-125 | S09 (`79`–`82`; push: no panel) |
| `secrets` folder; service account + key | 134-170 | S10 (`84`; `illustration`) |
| Bucket folders `dvc_store/`, `images/` (+ the missing first upload) | 174-187 | S10 (`illustration`; `extra` row) |
| Edit `GCS_BUCKET_NAME`, `GCP_PROJECT`, `GCP_ZONE` in `docker-shell.sh` | 197-205 | S10 (`85`) |
| About `docker-entrypoint.sh` | 215-230 | S10 (CODE, V4) |
| `cd data-versioning` · `sh docker-shell.sh` | 237, 243 | S11 (`86`; fix `87`; `88`) |
| `dvc init` | 269 | S12 (`90`; Linux fix `91`–`92`; `93`) |
| `dvc remote add -d cheese_dataset gs://YOUR_BUCKET_NAME/dvc_store` | 279 | S12 (`93`) |
| `dvc add cheese_dataset` | 293 | S12 (`93` empty, `95`) |
| `dvc push` | 303 | S13 (`95`; `extra · local remote`) |
| `git status` · `git add .` · `git commit -m "Track initial cheese dataset with DVC"` · `git tag -a dataset_v20 -m "First version of cheese dataset"` · `git push --atomic origin main dataset_v20` | 315-319 | S13 (`96`–`99`; push: no panel) |
| Colab: view `dataset_v20` | 326-328 | S15 (`illustration`; `C07b`, `C13`, `C15`; `recorded`) |
| Upload additional images to `images/` | 338-341 | S14 (`illustration`; `103` stand-in) |
| `dvc add cheese_dataset` · `dvc push` | 351, 357 | S14 (`104`) |
| `git status` · `git add .` · `git commit -m "Add images to cheese dataset"` · `git tag -a dataset_v21 -m "Updated cheese dataset with additional images"` · `git push --atomic origin main dataset_v21` | 365-369 | S14 (`105`–`108`; push: no panel) |
| Colab: view `dataset_v21` (cells 13, 15, 17, 19, 20) | 383-385 | S15 (`C19`, `C19b`, `C20`; `recorded`) |
| Docker Cleanup: `docker container ls`, `docker system prune`, `docker image ls` | 410-424 | S16 (`150`–`152`) |

## Notes for script and scene authors

- Shared code (`scenes/common.py`, started from L10's): tracker factories `tracker_a` … `tracker_l`
  with the step lists above; prompts `P_LAPTOP` (+ `~/data-labeling`, `~/data-versioning`
  variants), `P_CLI` (`app@<id>:/app$`), `P_DVC` (`root@<id>:/app#`) — container prompts come from
  each capture; tags `extra_tag` (with variants `extra · Linux`, `extra · stand-in`,
  `extra · local remote`), `illustration_tag`, `recorded_tag`, `your_turn`, the GOLD `cost_tag`.
  Set-piece classes: `StationMap` (V1), `SignedTicket` (V2), `OriginGate` (V3), `FuseMount` (V4),
  `HashShelf` (V5), `TagRope` (V6), `PipelineMap` (V7, persistent state across scenes). **Never
  reuse a scene class name** (`video.yaml`) for a helper.
- **The sandbox framing is load-bearing**: once, in S05; afterwards every failure is the lesson,
  every success is `recorded` + source, every stand-in is tagged. Never imply a failure surprised
  us; never show the placeholder key's content.
- **Stand-in numbers are not README numbers**: `"task_count":3` / `Number of tasks: 3` are our
  three imported tasks — the narration says "yours: 21" each time. Our v21 hash `6b342844…` differs
  from the class's `3280f8f9…` (different fifth photo) — say so in S14, never compare them as
  "should match". Only v20 matches (`121`).
- **Personal data**: quoted lines `docker-shell.sh:19`, `docker-compose.yml:31`, README:109/204/206
  render `student@example.com`; today's README:136 renders `YOUR_GITHUB_USERNAME`; Colab extracts
  already read `<course instructor>` / `YOUR_GITHUB_USERNAME`. Narration says "the instructor".
  Commit metadata, tagger names and the notebook's run dates are never shown.
- `istep` captures (`41`, `42`, `44`, `54`, `88`, `90`, `93`, `95`, `104`, `115`, `117`, `145`)
  hold whole sessions: pick line ranges per typed command (ranges above). Tracebacks: first line,
  `…`, last two lines. Long lines (`88:39`, `145:75`, `C13`) fold with `wrap` or are cropped from
  the meaningful phrase on.
- `86` is 1,126 lines: show only the apt verdict (1074–1081) and the final `ERROR: failed to
  build` line.
- `git push` (`83`, `100`, `109`) and the SSH clone (`73`): command typed, **no output panel** — the
  timeouts are the sandbox's.
- The `recorded` CORS line: built from `cli.py:40`'s f-string and `:26-33`'s dict, with the bucket
  shown as `<your bucket>`; the metadata lines of `-m` other than `Cors:` are `…`.
- Redraw every lecture diagram in series style; never slide images, the README PNGs, product
  screenshots (SuperAnnotate, Label Studio, the GCS console), cartoons, memes or the "final-final"
  screenshot (type our own invented names). One `lecture_ref` per scene as assigned.
- Chinese glossary heads-up: Label Studio, task, annotation, source / target storage, pre-signed
  URL, CORS, origin, preflight, bucket, prefix, mount, bind mount, FUSE, gcsfuse, DVC, remote,
  cache, manifest, md5, hash, pointer file, tag, annotated tag, commit, Colab, token, legacy token
  stay English; 标注 (labeling/annotation as an activity), 版本管理, 指纹 (fingerprint, the lecture's
  word) per the `i18n` glossary conventions when that stage comes.

## Things never to do on screen

Series rules:
- No slide images, console or product screenshots, Google/GCP or tool logos, memes or cartoons:
  redraw the idea, cite slides via `lecture_ref`; the console, Label Studio and Colab are schematic
  `illustration`s with README field values and **no invented numbers** (no task counts, expiry
  times, object names, file sizes or accuracy figures that no source gives).
- No real person's name, e-mail or GitHub user on screen (placeholders above); no hand-typed
  output: every terminal line comes from `assets/terminal/`; `recorded` panels name their source
  (`cli.py:40`/`:26-33`, README:136, the notebook's cells 13/15/17); stand-in and local-remote
  panels are tagged so.
- No command spelled differently from the README (the `sed` edits in `40`/`85`/`87` are editor
  actions, marked `extra` / "update the file"; the HTTPS clone `74` is the README:84 alternative,
  marked `extra`).

Lecture-specific:
- Never show the placeholder key's content or any plausible key, token or JWT (`eyJ…`): the token
  field is drawn blank; the demo token is the obviously fake `student-demo-token-not-a-secret`.
- Never present `Number of tasks: 3`, our v21 hash, or `5 files pushed` / `2 files pushed` as what
  the README run prints to GCS without the stand-in / local-remote tag.
- Never claim a GCS push, a `cli.py -c` success, a gcsfuse mount, a GitHub push or a Colab download
  happened live.
- Never draw the labeled data as photos sorted into class folders, never say Label Studio copies
  the images, never call CORS access control, never say the host's `cheese_dataset/` holds the
  photos, never say DVC stores diffs, and never tell viewers to delete `dvc_store/` as cleanup.
- Never show `89`'s root ownership as the mount's success state (in our capture the mount failed;
  the working two-view is `illustration`).
- Never read the capture-only lines aloud (proxy env lines, PyPI fetch, gcsfuse INFO JSON, image
  ids, our commit hashes as "the" hashes).

## Left for exercises.md (not in the video)

Digest E2 (`cli.py -r`, watch thumbnails break, `curl` still works), E3 (the JWT case and the
`LabelStudio` client fix), E4 in full, E5 (delete a photo → v22; delete `dvc_store` → dangling
tags), E6 (the two-view check with a real key), E7 (connect the halves: annotations → `images/<label>/`
→ a tag that pins images *and* labels); route T in full (the doubled `cd` `133`, `set-url` before a
remote `138`, the 11-file first commit `142`); gotcha 4 (`~/.gitconfig` becoming a directory),
gotcha 5 (port 8080 taken, `-p 8081:8080`), gotcha 8 (`docker compose` vs `docker-compose`),
gotcha 13a's token URL in full, gotcha 18 (gcsfuse caching) details, gotcha 20 (bucket-level role
instead of Storage Admin); the old starter README's other slips (`git init` twice, no `branch -M`);
the new notebook `18KYngbv` (a TA's own repo — its counts 13/9 are not reproducible); slide 22's
concept table and slides 15–18 beyond one sentence; digest recap Q1–Q6 not used in S16, SLIDES'
added recap questions (Git vs no Git; three reasons beyond rollback; renaming as versioning; where
DVC keeps a local copy).
