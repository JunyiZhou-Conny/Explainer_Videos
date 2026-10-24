# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

**The one thing to know about this lecture's captures:** the recording sandbox has **no GCP
credentials, no bucket, no browser and no SSH route to GitHub** (see the skill's environment
rules). Everything local is captured live: both clones, the dataset zip, Label Studio in its
container (start, port, login, its HTTP API, a project, tasks, one annotation), the CLI container,
`cli.py -p` / `-t` against the live server, the compose "Extra", the DVC image build, the
entrypoint, `dvc init` / `remote add` / `add`, the git commits and tags, a local time travel, and
the Colab notebook's `dvc` cells in a signed-out stand-in. Every step that needs a real Google
credential or bucket (`cli.py -c` / `-m`, Label Studio's *Check Connection*, the gcsfuse mount,
`dvc push`, Colab's `dvc get`) is captured up to its **honest, documented failure**, and what a
student sees on success is listed under "What cannot run here" with its source. No output was
invented.

**Read this before the brief: the README moved after the digest.** The digest pins
`data-versioning` at `b240b1a` (the course map's pin; README says *clone the
`data-versioning-ac215` starter*). On 2026-10-13, the day of the lecture, a teaching assistant
pushed seven commits; today's head `2515e5e` tells students to **clone `main`** instead, links a
**new Colab notebook**, and adds an HTTPS section. Cloning `main` brings the instructor's `.dvc/`
and `cheese_dataset.dvc` along, so `dvc init` and `dvc remote add` refuse, and `dvc push` targets
the **class bucket** (`145-docker-shell-dvc.txt`). Both routes are captured: route **S** (starter,
the pin, digest Part B; full walk) and route **T** (today's README, up to the divergence). The
brief must pick one and say so; route S + the one-line Dockerfile fix is the one that works.

## `source/` — the tutorials' own files

Copied unchanged with `git show <commit>:<path>`, relative paths preserved, except the two Colab
extracts (see below). Course material by the AC215 teaching staff (Harvard IACS), used for study
with the instructor's permission.

**Personal data in the snapshots (scenes must mask it):** `data-labeling/docker-shell.sh:19`,
`data-labeling/docker-compose.yml:31` and `data-labeling/README.md:109, 204, 206` contain the
instructor's e-mail address; `data-versioning@2515e5e/README.md:136` contains a teaching
assistant's GitHub user name. Scenes quoting those lines show `student@example.com` /
`YOUR_GITHUB_USERNAME` instead and say nothing about the original.

### `source/data-labeling/`

[dlops-io/data-labeling](https://github.com/dlops-io/data-labeling) at
`03c3e277abeee2cdaf4c1a8149c11c9fd259577d` (main, 2025-10-20; still the head of `main` on
2026-10-23, verified in `terminal/laptop/02-git-log.txt`). Digest pin, unchanged.

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | Part A, 246 lines: secrets folder (31-40), SA console steps (42-50), env var note (52-56), download (62-65), bucket (67-76), `sh docker-shell.sh` (82-97, the sample `docker container ls` with the stray compose line 95), login + project (102-115), storage forms (117-147), CORS text (149-168; the reverse-DNS erratum at 153), annotate (172-187), token + `cli.py -p/-t` (189-199), the `'amanita'` sample (204-206), compose "Extra" (214-229), cleanup (239-246) |
| `docker-shell.sh` | network (6), `rm -f` (9), the `docker run -d` with `-p 8080:8080`, both `-v`, the login env vars, `GOOGLE_APPLICATION_CREDENTIALS` (12-24) |
| `docker-shell-CLI.sh` | build (7), `docker run --rm -ti` on `data-labeling-network`, `../data-labeling:/app`, `GCS_BUCKET_NAME` to edit (23), `LABEL_STUDIO_URL=http://data-label-studio:8080` (24) |
| `docker-shell-compose.sh`, `docker-compose.yml` | the compose "Extra": `docker-compose run --rm --service-ports` (12); `external: true` network (2-5), the second hard-coded bucket (17), `depends_on` (19-20), the volume (27), login env (31-32) |
| `cli.py` | `storage.Client()` + the CORS rule + `bucket.patch()` (22-41), metadata (44-72), the legacy `Client(...)` (79, 95), `projects[0]` (99), `get_labeled_tasks()` (105), the "-k argument i required" typo (123) |
| `Dockerfile`, `docker-entrypoint.sh`, `pyproject.toml`, `uv.lock`, `.gitignore` | python:3.12-slim + uv + user `app`; the banner; pins google-cloud-storage 3.4.1, label-studio-sdk 2.0.12, pandas 2.3.3; `/docker-volumes` ignored |

### `source/data-versioning/` — README and finished state at the pin

[dlops-io/data-versioning](https://github.com/dlops-io/data-versioning) `main` at
`b240b1a03e0abd1964b689ea68e35f0990a33ebc` (2026-09-19; the digest's and course map's pin; **no
longer the head**, see `source/data-versioning@2515e5e/`).

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | Part B as the digest reads it (first copy, 1-425): cleanup (52-72), clone the **ac215** branch over SSH (76-84), `cd` / `rm -rf .git` / `git init` (86-101), new repo + first push (106-126), secrets + SA (134-170), bucket folders (174-187), `docker-shell.sh` values (195-205), `cd data-versioning` + `sh docker-shell.sh` (232-243), `dvc init` (269), `dvc remote add` (279, 285), `dvc add` (293), `dvc push` (303), git v20 (315-319), the tag disclaimer (321), Colab (324-328), v21 (332-372), cleanup (403-425); the duplicated copy from 425 on |
| `.dvc/config`, `.dvc/.gitignore`, `.dvcignore`, `cheese_dataset.dvc` | the instructor's finished state: remote `gs://cheese-app-data-versioning/dvc_store`; the v21/v30 pointer `3280f8f9….dir`, 785481 B, 5 files |
| `Dockerfile` | the gcsfuse-bionic `http://` repo (33), `google-cloud-cli` (36), root user (52) |
| `docker-entrypoint.sh` | `echo $GCS_BUCKET_NAME` (7), gcloud (9), gcsfuse (11), the unconditional "mounted" echo (12), `mount --bind` (14) |
| `docker-shell.sh`, `pyproject.toml`, `uv.lock`, `.gitignore` | bucket/project/zone to edit (7-9), the privileged `docker run` (17-27); dvc 3.63.0, dvc-gs 3.0.2, gcsfs 2025.9.0, google-cloud-storage 3.4.1 |

### `source/data-versioning@data-versioning-ac215/` — the starter

Branch `data-versioning-ac215` at `23762e49ae890af40757c93356fae6cf2e526db2` (2025-10-20;
verified in `terminal/laptop/75-git-log.txt`). `README.md` (the older starter README), `.gitignore`
(`/cheese_dataset` at 3), `Dockerfile` (**`google-cloud-sdk` at 36**, the line that fails today),
`docker-entrypoint.sh` (one line shorter than main's: gcloud at 8, gcsfuse at 10, `mount --bind`
at 13), `docker-shell.sh` and `pyproject.toml` (identical to main's). Its `uv.lock` is
byte-identical to `source/data-versioning/uv.lock` and is not duplicated.

### `source/data-versioning@2515e5e/` — the README as it reads today

`main` at `2515e5efb82073b565e9a21016dd5295d44c9d2c` (2026-10-13 12:19 -0400, "Change clone branch
from 'data-versioning-ac215' to 'main'"), the head on 2026-10-23 (`terminal/laptop/134-git-log.txt`).
Only the two files that differ from the pin are snapshotted (`git diff --stat b240b1a 2515e5e`:
`README.md` 445 lines changed, `docker-entrypoint.sh` 8):

- `README.md` (450 lines): the heading still says "Clone the `data-versioning-ac215` branch" (78)
  over `git clone -b main …` (81); new HTTPS section (86-100) with **two** `cd data-versioning`
  (97, 105); `git remote set-url origin https://github.com/<a TA's user>/…` **before** any remote
  exists (133-138); the "upload some pictures" sentence (254); a **new Colab link**
  `18KYngbvVQGYu_1LK61M7xh6XI1_KskXL` (350, 407); the duplicate copy removed except a stray
  `# 🧀 Data Versioning with DVC` glued to the last fence (449).
- `docker-entrypoint.sh`: `mkdir -p /mnt/gcs_data` (10, was `/mnt/gcs_bucket`), a two-line comment
  about bind mounts (15-16), `mount --bind` now at 18.

### `source/colab/` — extracts of the two notebooks (edited, see notes)

Downloaded 2026-10-23 from Google Drive; the `.ipynb` files are **not** in the repo (their
metadata carries names of the people who ran them). Each extract holds the cell sources and stored
outputs only, ANSI colours dropped:

| file | notebook | notes |
| --- | --- | --- |
| `notebook-1RRQ1SlH.cells.txt` | `1RRQ1SlHq5lKK76R8LoQdi5LjCnND3jTq`, linked from README @ b240b1a (the digest's notebook) | stored outputs = **`recorded`** source for Colab: `pip install` (dvc 3.63.0, dvc-gs 3.0.2), `dvc list -R` (5 `cheese_dataset/…` files incl. the Gruyère `.webp`), `dvc get --rev dataset_v21` progress, `Number of items: 5`, and the stale `Number of items: 3` after the `dataset_v25` cell. Edited: the instructor's name in cell 0 reads `<course instructor>`. |
| `notebook-18KYngbv.cells.txt` | `18KYngbvVQGYu_1LK61M7xh6XI1_KskXL`, linked from README @ 2515e5e | same cells pointed at a TA's own repo, `--rev dataset_v20` / `dataset_v21`; stored outputs `Number of items: 13` (v20) and `9` (v21) from the TA's own run; cell 17 now says to add **or delete** photos. Edited: the TA's GitHub user reads `YOUR_GITHUB_USERNAME`, the instructor's name `<course instructor>`. |

## `terminal/` — real terminal sessions

Captured **2026-10-23 11:42–12:06 UTC** in one clean run (`capture.sh laptop setup` → all
segments → `capture.sh colab run`) by `terminal/capture.sh`, which runs `terminal/run_steps.sh`
inside fresh disposable containers. Each README command runs exactly as written, in README order,
and its output goes to its own file: the file starts with the command (`$ ...`), then the output,
then its exit status (`[exit N]`; single-line outputs carry it inline). Steps that are not in the
README are marked *extra* below and in `run_steps.sh`.

Two kinds of file, as in L10: **`step` files** (no terminal, plain output; colours dropped) and
**`istep` files** (a real pseudo-terminal via `ptyrun.py`, 110×50; the lines a person would type at
the container prompt are typed when the prompt appears; progress bars appear redrawn, colours are
dropped). An `istep` file's `[exit N]` is the status of the shell's last command before `exit`.

| folder | environment | source it follows |
| --- | --- | --- |
| `laptop/` | a fresh, empty Docker engine standing in for the student's machine with Docker Desktop: `docker:29.8.2-dind` (client + engine 29.8.2, Compose v5.6.0 plugin + `docker-compose` compat command, linux/amd64), user `student` in the `docker` group with sudo, git 2.54.0 (identity `student <student@example.com>`), curl, tree, unzip, ssh | `data-labeling/README.md` top to bottom (Part A, files 00-64), then `data-versioning/README.md` @ b240b1a (route S, 70-122), then today's README @ 2515e5e (route T, 130-145), then cleanup (150-152) |
| `colab/` | a `python:3.12-slim-bookworm` container + git, root in `/content` like a Colab runtime, **not signed in** (`capture-only/colab-standin.Dockerfile`) | the notebook @ b240b1a's code cells 7, 13, 15, 17, 19, 20 as shell commands |

### `laptop/` — Part A, `data-labeling` README top to bottom

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt` | extra | date, `Linux x86_64`, Docker 29.8.2, Compose v5.6.0, git 2.54.0 |
| `01-clone.txt` | Prerequisites, README:14 | `git clone https://github.com/dlops-io/data-labeling` |
| `02-git-log.txt` | extra | HEAD = `03c3e277…` 2025-10-20 = the digest pin |
| `03-ls.txt` | extra | the repo's top level (three PNG figures, three shell scripts, `cli.py`, `uv.lock` …) |
| `04-mkdir-secrets.txt` | README:31-40 (the README shows the tree, not a command) | `mkdir secrets` next to the repo |
| `05-tree.txt`, `06-ls-secrets.txt` | README:37-40 tree / step A2 checkpoint (extra) | `data-labeling` beside `secrets`; `secrets/data-service-account.json` — the **placeholder** key (below) |
| `07-download-zip.txt` | "Download data", README:64 (a browser download; `curl -LO` of the same URL) | `cheeses_unlabeled.zip`, 3,720,496 bytes |
| `08-unzip.txt` | "Extract the zip file", README:65 | each image **and** its `__MACOSX/…/._Image_*` twin |
| `09-ls-images.txt` | extra (digest A3 checkpoint, gotcha #22) | 21 images (incl. `Image_3.png`) + 21 resource forks |
| `09b-md5-images.txt` | extra (digest §3.5) | md5 + size of `Image_1-5.jpg`: `5b53853e…`, `ba044df2…`, `91f482c4…`, `5b85cf7e…`, `54081d12…` — the fingerprints DVC computes later |
| `10-docker-shell.txt` | "Run `docker-shell.sh`", README:87 | pulls `heartexlabs/label-studio:latest`, prints the container id, exit 0 |
| `11-docker-container-ls.txt` | README:91 | the README's checkpoint line: `heartexlabs/label-studio:latest … Up Less than a second   0.0.0.0:8080->8080/tcp   data-label-studio` |
| `12-docker-container-ls-a.txt` | extra | 25 s later: **`Exited (1)`** |
| `13-docker-logs.txt` | extra (digest A6 checkpoint) | **digest gotcha #12, live:** `ERROR: Data directory is not writable: /label-studio/data`, `UID = 1001`, the directory owned by root, and Label Studio's own fix text |
| `14-ls-volume.txt`, `15-ls-uid.txt` | extra (gotcha #12's checks) | Docker created `docker-volumes/label-studio` as **root**; the image runs as `uid=1001 gid=0(root)` |
| `16-fix-volume-perms.txt` | extra (gotcha #12's fix; Linux only) | `sudo chown -R 1001 docker-volumes/label-studio` |
| `17-docker-shell-again.txt`, `18-docker-container-ls.txt` | README:87 / :91 again | the script removes the exited container, starts a new one: **Up**, `0.0.0.0:8080->8080/tcp` |
| `19-docker-logs.txt` | extra | first-start log: `Initializing database..`, Django 5.2.17, `Starting development server at http://0.0.0.0:8080/`, an "Update available 1.23.0 → 1.23.2" box, `GET /health 200` |
| `20-curl-health.txt` … `22-curl-login-page.txt` | extra (README:108 "go to http://localhost:8080/") | `{"status": "UP"}`; `/` → `302 -> /user/login/`; the login page `200 text/html`, `<title>Label Studio</title>` |
| `23-login.txt`, `24-whoami.txt` | README:109 login, done with curl (CSRF form post) | `302 -> http://localhost:8080/` = logged in; `/api/current-user/whoami` → `student@example.com` (the capture-only stand-in, below) |
| `25-api-no-token.txt` | extra | `/api/projects` without credentials → `401 Authentication credentials were not provided.` |
| `26-api-version.txt` | extra (digest §5 open question) | `/api/version` answers **without a token**: `"release": "1.23.0"`, Community edition |
| `27-jwt-settings.txt` | extra (digest gotcha #11) | the organization's token settings as the UI reads them: `{"api_tokens_enabled":true,"legacy_api_tokens_enabled":false}` — **legacy tokens are OFF by default** |
| `28-create-project.txt` | "Create Annotation Project", README:110-115 (stand-in for the clicks: the UI's own API call with the Image Classification config and the four cheeses) | project `1` "Cheese labels", the label config echoed back, `HTTP 201` |
| `29-ls-secrets-in-container.txt` | extra (digest A8 "If it fails") | `/secrets` inside Label Studio is empty |
| `30-check-source-storage.txt` | "Configure Cloud Storage" → *Check Connection*, README:121-134 (the form's validate call with the README's values) | **honest failure:** `400 … "File /secrets/data-service-account.json was not found."` |
| `31-check-target-storage.txt` | *Add Target Storage* → *Check Connection*, README:138-146 | **honest failure:** `400 … "Error validating storage connection"` |
| `32-import-tasks.txt` | stand-in for *Sync Storage* (README:136; no bucket here) | three tasks with the `gs://…/cheeses_unlabeled/Image_N.jpg` URIs a sync creates: `"task_count":3`, `HTTP 201` |
| `33-annotate.txt` | stand-in for clicking **gouda** + *Submit* (README:174-177) | the annotation JSON Label Studio 1.23.0 stores: `result → value → choices: ["gouda"]`, `from_name "choice"`, `to_name "image"`, `created_username " student@example.com, 1"`, `HTTP 201` |
| `40-edit-bucket.txt` | "Change the bucket name in docker-shell-CLI.sh", README:164 (sed is the editor) | line 23 now `GCS_BUCKET_NAME="your-bucket-placeholder"` |
| `41-docker-shell-CLI.txt` | README:165-168: `sh docker-shell-CLI.sh`, then `python cli.py -c` and `python cli.py -m` typed inside; extras `ls -la /secrets`, `echo $GCS_BUCKET_NAME $LABEL_STUDIO_URL`, two curls | uv build (python 3.12.15, uv 0.13.5), the `app@…:/app$` prompt; **`-c` and `-m` both fail honestly** at `storage.Client()`: `google.auth.exceptions.DefaultCredentialsError: File /secrets/data-service-account.json was not found.` (after printing `set_cors_configuration()` / `view_bucket_metadata()`); **digest §3.4 live:** `localhost:8080` → `curl: (7) … Couldn't connect to server`, `data-label-studio:8080/health` → `{"status": "UP"}` |
| `42-cli-projects-401.txt` | README:198 `python cli.py -p -k <token>`; extras `cli.py -t` and `cli.py -p -k` | **digest gotcha #11, live:** `401` — `"Authentication token no longer valid: legacy token authentication has been disabled for this organization"` (the SDK's own error block + traceback ending `401 Client Error: Unauthorized for url: …/api/projects?page_size=10000000`); the typo `-k argument i required for API access to LABEL Studio`; argparse's `expected one argument` |
| `43-enable-legacy-tokens.txt` | extra (gotcha #11's first fix: *Organization → API Tokens Settings*, done with the UI's own call) | `{"api_tokens_enabled":true,"legacy_api_tokens_enabled":true}` |
| `44-cli-projects-tasks.txt` | README:198-199 again: `-p` and `-t` | `-p`: `get_projects`, `[<label_studio_sdk._legacy.project.Project object at 0x…>]`, `1 Cheese labels`, the object repr; `-t`: `Number of tasks: 3`, `Number of labeled tasks: 1`, one `Annotations: [{'id': 1, 'result': [{… 'choices': ['gouda']}], …}]` line — the shape of README:204 with a cheese instead of `'amanita'` |
| `50-docker-stop.txt`, `51-docker-ps.txt` | "Extra" note, README:224-229 | `docker stop data-label-studio`; nothing running |
| `52-docker-shell-compose.txt` | README:218 `docker-shell-compose.sh` (run as `sh …`) | `docker-compose` works (Compose v2 compat command), the obsolete-`version` WARN, then **digest gotcha #6, live:** `Conflict. The container name "/data-label-studio" is already in use` — `docker stop` left it behind; exit 1 |
| `53-docker-rm.txt` | extra (gotcha #6's fix) | `docker rm data-label-studio` |
| `54-docker-shell-compose-run.txt` | README:218 again; typed inside: extras `echo $GCS_BUCKET_NAME`, `python cli.py -p -k …`, a wait loop, `-p` again | compose creates `data-label-studio`, the one-off `data-labeling-data-label-cli-run-…` (README:95's stray line explained); **errata #9 live:** `GCS_BUCKET_NAME` is `cheese-app-data-demo` (compose's own copy, not the edited script); **`depends_on` does not wait:** the first `cli.py -p` → `ConnectionRefusedError … Max retries exceeded with url: /api/version`; after the loop `{"status": "UP"}`, `-p` lists `1 Cheese labels` — **the project survived** (same `docker-volumes` folder) |
| `55-docker-ps.txt` | extra | `data-label-studio` still Up after the CLI shell exits |
| `60-…` – `63-…` | "Docker Cleanup", README:243-246 | `docker container ls`; `docker stop data-label-studio`; `docker system prune` (the `[y/N] y` prompt, the deleted container and **`data-labeling-network`**); `docker image ls` (`data-label-cli` 1.76 GB, `heartexlabs/label-studio` 1.5 GB) |
| `64-volume-survives.txt` | extra | `docker-volumes/label-studio/label_studio.sqlite3` is still there (owned by 1001, hence sudo) |

### `laptop/` — Part B, route S: README @ b240b1a + the `data-versioning-ac215` starter

| file | README step | what it shows |
| --- | --- | --- |
| `70-…` – `72-…` | README:52-72 | `docker container ls`, `docker system prune` (y), `docker image ls` |
| `73-clone-ssh.txt` | README:81 | `ssh: connect to host github.com port 22: Operation timed out` — **the sandbox has no SSH route** (a student without a key on GitHub gets a different SSH error; nothing in the sources documents its text, so no panel should claim one) |
| `74-clone-https.txt` | README:84's HTTPS alternative, same branch | `git clone -b data-versioning-ac215 https://github.com/dlops-io/data-versioning.git` |
| `75-git-log.txt` | extra | `23762e49…` 2025-10-20 = the digest's starter pin |
| `76-rm-git.txt`, `77-git-init.txt` | README:95, 101 | git 2.54's `hint: Using 'master' as the name for the initial branch…` block, `Initialized empty Git repository` |
| `78-ls-A.txt` | extra (digest B2 checkpoint) | 7 files + `.git`; **no `.dvc/`** |
| `79-…` – `83-…` | README:121-125 | `git branch -M main`, `remote add` (README's literal placeholder URL), `git add .`, `[main (root-commit) …] Initial commit  7 files changed`, `git push -u origin main` → the same SSH timeout (no GitHub repo/route here) |
| `84-tree.txt` | README:136-144 folder structure (extra) | `data-labeling`, `data-versioning`, `secrets/data-service-account.json` side by side (placeholder key) |
| `85-edit-docker-shell.txt` | README:195-205 (sed is the editor) | lines 7-9: `your-bucket-placeholder`, `your-gcp-project`, `us-central1-a` |
| `86-docker-shell-starter-fails.txt` | README:243 `sh docker-shell.sh`, unmodified starter | **digest gotcha #1, live, word for word:** `Package google-cloud-sdk is not available, but is referred to by another package. … However the following packages replace it: google-cloud-cli` / `E: Package 'google-cloud-sdk' has no installation candidate`, `ERROR: failed to build`, exit 1 |
| `87-fix-dockerfile.txt` | extra (gotcha #1's fix = main's `ebf09c8`) | line 36 → `google-cloud-cli` |
| `88-docker-shell.txt` | README:243 again; extras typed inside: `ls -la cheese_dataset`, `which dvc`, `dvc --version`, `gcsfuse --version`, `gcloud --version`, `ls /mnt/gcs_data` | build (gcsfuse + google-cloud-cli + uv sync), `Container is running!!!`, `Python 3.11.17`, then the entrypoint's three **honest failures**: `ERROR: (gcloud.auth.activate-service-account) Unable to read file [/secrets/data-service-account.json]` (digest §6 #3 verbatim), gcsfuse 3.13.0's JSON log ending `failed to detect credentials: open /secrets/data-service-account.json: no such file or directory`, the **unconditional** `GCS bucket mounted at /mnt/gcs_data` (errata #10 live), `mount: /app/cheese_dataset: special device /mnt/gcs_data/images does not exist.` (digest §6 #2 verbatim); the root prompt anyway (no `set -e`); `cheese_dataset` empty; `/.venv/bin/dvc`, `3.63.0` |
| `89-host-cheese-dataset.txt` | extra (digest §3.7) | on the host the folder exists, empty, **owned by root** |
| `90-dvc-init-ownership.txt` | README:269 `dvc init` | **Linux-engine finding (digest §10 open question, answered):** `ERROR: unexpected error - /app/.git/: repository path '/app' is not owned by current user`; `ls -A` shows a half-made `.dvc/` + `.dvcignore` |
| `91-clean-partial-init.txt`, `92-safe-directory.txt` | extra (the fix) | `sudo rm -rf .dvc .dvcignore`; `git config --global --add safe.directory /app` — `~/.gitconfig` is what `docker-shell.sh:23` mounts as the container's `/etc/gitconfig` |
| `93-dvc-v20.txt` | README:269, 279, 293, 303 inside one container session; extras `cat .dvc/config`, `cat cheese_dataset.dvc`, an ADC check | `Initialized DVC repository.` + the analytics box + "What's next?"; `Setting 'cheese_dataset' as a default remote.`; the config; `dvc add` on the **empty** folder (the failed mount) → `md5: d751713988987e9331980363e24189ce.dir`, `size: 0`, `nfiles: 0` — gotcha "never `dvc add` an empty folder", live; `dvc push` → honest failure (`failed to transfer … - https://storage.googleapis.com/upload/storage/v1/b/your-bucket-placeholder/o`, `1 files failed to upload`); the ADC check → `DefaultCredentialsError: File /secrets/data-service-account.json was not found.` |
| `94-standin-images.txt` | **capture-only stand-in** for "upload images to `images/`" | `Image_1.jpg`…`Image_4.jpg` from the zip copied into `cheese_dataset/` (sudo: the folder is root's) |
| `95-dvc-add-push-v20.txt` | README:293, 303 again on the four photos; extras `cat`, `find .dvc/cache`, a local stand-in remote | `md5: 89db50de27acfd6822faabc3da39b0a8.dir`, `size: 611101`, `nfiles: 4` — **the class's `dataset_v20`, reproduced live** (see 121); the cache: `5b/53853e…`, `5b/85cf7e…`, `89/db50de….dir`, `91/f482c4…`, `ba/044df2…` (+ the empty `d7/5171….dir` from 93); `dvc push` → honest failure; `dvc push -r standin` → **`5 files pushed`** (4 photos + the manifest; the digest's unverified "I expect 5", confirmed) |
| `96-git-status.txt` | README:315 | digest B11 checkpoint, exactly: `.dvc/.gitignore`, `.dvc/config`, `.dvcignore` **staged** by `dvc init`; `.dvc/config` modified again (remote add); `cheese_dataset.dvc` untracked (plus our `Dockerfile`/`docker-shell.sh` edits) |
| `97-…` – `100-…` | README:316-319 | `git add .`; the commit (`create mode … cheese_dataset.dvc`); the annotated tag; `git push --atomic origin main dataset_v20` → SSH timeout |
| `101-git-log.txt`, `102-git-show-v20.txt` | extra | `(HEAD -> main, tag: dataset_v20)`; the six-line pointer the tag pins |
| `103-standin-new-image.txt` | **capture-only stand-in** for "Upload a few additional images" (README:338) | `Image_5.jpg` added |
| `104-dvc-add-push-v21.txt` | README:351, 357; extra `dvc push -r standin` | `md5: 6b3428441b34d1c1217aa55e963f7716.dir`, `712574`, `5`; `dvc push` honest failure; `dvc push -r standin` → **`2 files pushed`** — the new photo + the new manifest (the ponder answer of digest §8 ch. 8, live) |
| `105-…` – `109-…` | README:365-369 | `git status` shows only `modified: cheese_dataset.dvc`; commit; tag v21; push → SSH timeout |
| `110-git-diff.txt` | extra (digest B13 checkpoint) | the pointer's three changed lines: md5, size 611101 → 712574, nfiles 4 → 5 |
| `111-…`, `112-…` | extra | two tags on two commits; `git tag -n` with both messages |
| `113-remote-add-again.txt` | extra (what README:372 warns about; the old starter README repeats it) | `error: remote origin already exists.` |
| `114-…` – `117-…` | extra (time travel without Colab) | `git checkout dataset_v20 -- cheese_dataset.dvc` + `dvc checkout` → 4 photos; back to `main` + `dvc checkout` → 5 photos (from the local cache) |
| `118-ls-remote-tags.txt` | extra (digest §6 #13c) | the class repo has exactly `dataset_v20`, `v21`, `v30` (annotated; peeled to `299bcab`, `6de43d1`, `8a1d9b0`) — no `v25` |
| `119-…`, `120-class-v20-v21.txt` | extra | the class repo's head is now `2515e5e…`; its `dataset_v20` pointer `89db50de….dir/611101/4` and `dataset_v21` pointer `3280f8f9….dir/785481/5` |
| `121-compare-v20.txt` | extra | our `dataset_v20` pointer and the class's are **identical** |
| `122-class-bucket-anonymous.txt` | extra (digest §6 #13b) | `401 Anonymous caller does not have storage.objects.list access …cheese-app-data-versioning` |

### `laptop/` — Part B, route T: the README as it reads today (@ 2515e5e)

In `~/today/` (its own `secrets/`, empty), so the two clones do not collide.

| file | README step (today) | what it shows |
| --- | --- | --- |
| `130-clone-ssh-main.txt`, `131-clone-https-main.txt` | README:81, :91 | SSH timeout (sandbox); the HTTPS clone of **`main`** |
| `132-cd.txt`, `133-cd-again.txt` | README:97, :105 | the first `cd data-versioning` works; the second, as written, fails: `cd: data-versioning: No such file or directory` |
| `134-git-log.txt` | extra | `2515e5e…` 2026-10-13 |
| `135-…`, `136-…`, `137-ls-A.txt` | README:111, 117; extra | `.dvc/`, `.dvcignore`, `cheese_dataset.dvc` **came with the clone** |
| `138-remote-set-url.txt` | README:136 (a TA's user name replaced, below) | `error: No such remote 'origin'` — `set-url` before any `remote add` |
| `139-…` – `143-…` | README:143-147 | the same five commands; the first commit now carries the instructor's DVC files (11 files); push → SSH timeout |
| `144-edit-docker-shell.txt` | README:219-235 | same three values |
| `145-docker-shell-dvc.txt` | README:267, 293, 303, 317, 327 + extras `cat .dvc/config`, `cat cheese_dataset.dvc` | build passes (main's Dockerfile); the entrypoint now echoes the bucket name; same three entrypoint failures; **`dvc init` → `ERROR: failed to initiate DVC - '.dvc' exists. Use `-f` to force.`**; **`dvc remote add` → `ERROR: configuration error - config file error: remote 'cheese_dataset' already exists. Use `-f\|--force` to overwrite it.`**; the config still says `url = gs://cheese-app-data-versioning/dvc_store`; the pointer is the instructor's `3280f8f9….dir`; `dvc add` overwrites it; **`dvc push` goes to the class bucket** → `Anonymous caller does not have storage.objects.get access … cheese-app-data-versioning …` |
| `150-…` – `152-…` | "Docker Cleanup" (README:403-425 @ pin; 427-449 today) | `docker container ls`, `docker system prune` (y), `docker image ls` (`data-version-cli` 2.73 GB …) |
| `capture-only/` | not part of the tutorial | the two base-image re-tags (Dockerfiles + build logs), the placeholder key and its move log, the login stand-in diff |

### `colab/` — the notebook's cells, signed out

| file | notebook cell (@ b240b1a's notebook) | what it shows |
| --- | --- | --- |
| `C00-env.txt` | extra | Python 3.12.15, git 2.39.5 |
| `C07-pip-install.txt`, `C07b-dvc-version.txt` | cell 7 `!pip install dvc dvc-gs` | today pip resolves **dvc 3.67.1, dvc-gs 3.1.0, gcsfs 2026.10.1** (the notebook's stored run: 3.63.0 / 3.0.2) |
| `C13-dvc-list.txt` | cell 13 | honest failure without sign-in: `Could not determine bucket type … Your default credentials were not found`, then `401 Anonymous caller does not have storage.objects.get access … dvc_store/files/md5/32/80f8f9629451704dca3f792534e1f5.dir` — DVC fetches the **`.dir` manifest** to expand the folder; exit 255 |
| `C15-dvc-get-v21.txt` | cell 15 | the same 401 on the same manifest |
| `C17-count.txt` | cell 17 (run with `python -c`) | `FileNotFoundError: … 'cheese_dataset'` |
| `C19-dvc-get-v25-quiet.txt` | cell 19 | **prints nothing**, exit 1 — `--quiet` hides the error (digest gotcha #13c, live) |
| `C20-count.txt` | cell 20 | `FileNotFoundError` — the failure surfaces one cell later |
| `C19b-dvc-get-v25-loud.txt` | extra (cell 19 without `--quiet`) | `ERROR: failed to get 'cheese_dataset' from 'https://github.com/dlops-io/data-versioning' - unknown Git revision 'dataset_v25'` |

## What cannot run here, and what was recorded instead

- **The GCP console** (service account + key, data-labeling README:42-50, data-versioning README
  @ b240b1a:148-170; bucket and folders, README:67-76 / :174-187; uploading the 21 images,
  README:76; uploading to `images/`; viewing `cheeses_labeled/` and opening a JSON, README:182-187;
  browsing `dvc_store/`). Browser clicks: scenes draw a schematic console tagged `illustration`
  (never a screenshot or logo) with the README's field values: SA **`data-service-account`**, role
  **Cloud Storage → Storage Admin**, *KEYS → ADD Key → JSON*, saved as
  `secrets/data-service-account.json`; buckets `cheese-app-data-demo` (folders `cheeses_unlabeled`,
  `cheeses_labeled`) and `cheese-app-data-versioning` (folders `dvc_store`, `images`), each
  "REPLACE WITH YOUR BUCKET NAME". The key's fields are drawn from digest §2; never render a
  plausible private key. What `dvc_store/` contains after a push is drawn from the **live local
  cache layout** in `95` (same `files/md5/<2>/<30>` paths; the remote mirrors the cache).
- **The Label Studio UI** (login page, project wizard, *Labeling Setup* template, the storage
  forms, the task grid with thumbnails, the labeling screen, *Account & Settings*, *Organization →
  API Tokens Settings*). **No screenshots of the product.** Scenes draw it schematically, tagged
  `illustration`, with the README's labels and values (README:110-147, 174-177, 193-199). The
  server side of each click is captured live (`20`-`33`, `43`): what the browser would get back.
  The thumbnails' CORS failure and the fix are browser behaviour: draw them (digest §3.2-§3.3)
  without an output panel; a browser's console message is not captured anywhere.
- **`python cli.py -c` / `-m` success** (README:167-168). Captured to the honest failure (`41`).
  The success output is `recorded` from the code's own prints, `cli.py:19` (`set_cors_configuration()`),
  `:40` (`Set CORS policies for bucket <name> is [{'origin': ['*'], 'method': ['GET'],
  'responseHeader': ['Content-Type', 'Access-Control-Allow-Origin'], 'maxAgeSeconds': 3600}]` —
  the dict comes from `:26-33`) and `:47-72` (`view_bucket_metadata()`, the `ID:`…`Labels:` lines;
  only `Cors:` is load-bearing). Do not invent the other metadata values (location, creation time…);
  show them as `…`.
- **Storage *Check Connection* / *Sync Storage* success, "21 tasks", annotations written to
  `cheeses_labeled/`.** No bucket. The README states the outcomes (README:134-136, 174, 186), the
  digest gives the count (21, from the zip, `09`). The tasks/annotation captured here (`32`, `33`,
  `44`) are **API stand-ins** for those clicks, with the same `gs://` URI shape a sync creates
  (digest A12) — tag them so (e.g. `extra · stand-in`), and do not present `Number of tasks: 3` as
  what the README run gives (it gives 21). The exact object name Label Studio writes to
  `cheeses_labeled/` is not documented anywhere available; draw "one JSON object per annotation"
  without a file name.
- **The token as copied from *Account & Settings*.** The capture uses a fixed stand-in token
  (below). Label Studio 1.23.0 shows a Personal Access Token (a JWT) by default; its exact UI text
  was not captured. What *is* captured: with the defaults, `cli.py`'s legacy client gets the 401 in
  `42` for a legacy token; after enabling legacy tokens it works (`44`). The JWT case (digest
  gotcha #11, sending `Token eyJ…`) was not run, so as not to print a real-looking token: describe
  it, no output panel.
- **gcsfuse mount success, `ls cheese_dataset` showing the bucket's images, the empty host view
  next to a full container view** (digest §3.7, E6). Not possible without a bucket. Captured: the
  failure chain (`88`), the empty folders (`88`, `89`). Draw the two-view picture as `illustration`.
- **`dvc push` success to `gs://…/dvc_store`** (README:303, :357). Captured to its honest failure
  (`93`, `95`, `104`). What a student would see: the summary line comes from the **live push to a
  local stand-in remote** with the same data (`5 files pushed`, then `2 files pushed`) — tag those
  panels `extra · local remote`, never as the GCS push. The `gs://` push's own progress text is not
  captured; DVC prints the same `N files pushed` summary for any remote (dvc 3.63.0), which is all a
  panel should show.
- **`git push` to GitHub** (README:125, 319, 369). No GitHub repo, no SSH route: captured to the
  sandbox's SSH timeout (`83`, `100`, `109`). That error is the sandbox's, not a student's: scenes
  show the command and describe success (branch + tag on GitHub, *Tags* list) without an output panel.
- **Colab** (README:324-328, :381-385). The stand-in runs the notebook's cells signed out (cell 11
  `auth.authenticate_user()` needs a browser), so everything stops at the class bucket's 401
  (`C13`, `C15`). Success output is `recorded` from the notebook's stored outputs
  (`source/colab/notebook-1RRQ1SlH.cells.txt`, cells 7, 13, 15, 17: the five-file `dvc list`, the
  5-file download, `Number of items: 5`), from the instructor's 2025-10-28/29 run of the **class**
  repo. For a viewer's own repo: `Number of items: 4` for v20 follows from the live `95`
  (`nfiles: 4`) — fine as narration, not as a captured panel. The new notebook's `13` / `9` are a
  TA's own dataset, not reproducible; do not show them as expected values.

## Capture-only deviations (the recording sandbox vs a student's machine)

None of the tutorial's commands were changed; the environment around them was:

- **Login stand-in (privacy).** `data-labeling/docker-shell.sh:19` and `docker-compose.yml:31` were
  edited in the capture clone so the Label Studio account is **`student@example.com`** instead of
  the instructor's real address, and a line `LABEL_STUDIO_USER_TOKEN="student-demo-token-not-a-secret"`
  was added after the password line in both (so `-k` takes an obviously fake, fixed token instead
  of a random real-looking one). The password stays the README's `awesome` (a tutorial default, not
  a personal secret). Diff: `laptop/capture-only/login-standin.diff` (the original address masked).
  Effect: `24`, `33`, `44` show `student@example.com`; README:204 shows the instructor's address in
  the same place.
- **Placeholder names.** Bucket **`your-bucket-placeholder`** (checked not to exist on 2026-10-23;
  an earlier trial with `your-bucket-name` hit somebody's real bucket and was discarded), project
  **`your-gcp-project`**, GitHub user **`YOUR_GITHUB_USERNAME`** (the README's own placeholder; in
  route T it also replaces a TA's real user name in README:136's `set-url` line).
- **The placeholder key.** `secrets/data-service-account.json` in `05`/`06`/`84` is an obviously
  invalid stand-in (`project_id: "your-gcp-project"`, zeroed ids,
  `PLACEHOLDER-THIS-IS-NOT-A-REAL-KEY` — `laptop/capture-only/placeholder-key.json`; 422 B, a real
  key is ~2.3 KB). It is moved out before every cloud step (`capture-only/placeholder-key-moves.txt`),
  so they fail with the *documented* missing-file errors rather than an undocumented parse error.
- **Stand-in data for the bucket's `images/` folder** (`94`, `103`): with no gcsfuse mount, the
  photos are copied into the (unmounted) `cheese_dataset/` folder with `sudo cp`. Everything DVC
  then does to them is real. Choice of photos: `Image_1-4.jpg` (the class's v20, digest §3.5) and
  `Image_5.jpg` (any fifth photo; the class's v21 added a Gruyère `.webp` that is not in the zip,
  so our v21 hash `6b342844….dir` differs from the class's `3280f8f9….dir` — expected).
- **A local DVC remote** `standin` at `/app/.dvc/tmp/standin-remote`, added with `--local` (written
  to the git-ignored `.dvc/config.local`, so the committed `.dvc/config` and every `git status` are
  unaffected), only to show what a push uploads.
- **sudo** for the student (a Linux user would have it): used for the gotcha #12 fix (`16`), the
  root-owned folders (`64`, `91`, `94`, `103`).
- **Proxy relay, Docker client proxies, base images.** The sandbox reaches the internet only
  through a TLS-intercepting HTTPS proxy on the host's loopback that refuses plain http.
  `proxy_relay.py` (container `l11-relay`) forwards the bridge gateway to it; the laptop engine and
  its containers get it through `~/.docker/config.json`'s `proxies` (Docker Desktop: *Settings ›
  Resources › Proxies*). Docker injects those into every container, which is why gcsfuse's log in
  `88`/`90`/`93`/… has three `Added environment https_proxy: …` / `no_proxy` lines, and why
  Label Studio's update check reached PyPI in `19`: **scenes crop those three lines.**
  `python:3.12-slim-bookworm` (data-labeling's base) and `python:3.11-slim-bookworm`
  (data-versioning's) were rebuilt with the proxy's CA, https Debian sources, the CA env vars, and
  an apt hook that turns the Dockerfile's `http://packages.cloud.google.com` gcsfuse line into https
  before each `apt-get update`, then re-tagged under the same names
  (`laptop/capture-only/python3.1{1,2}-base.Dockerfile` + build logs). A student's build pulls the
  base layers and fetches gcsfuse over plain http.
- **SSH.** `GIT_SSH_COMMAND="ssh -o ConnectTimeout=15 -o BatchMode=yes"` bounds the SSH attempts;
  the `Operation timed out` lines are the sandbox's (port 22 is closed), not a student's.
- **The Colab stand-in** is a container, not Colab: cell commands without `!`, cells 17/20 as
  `python -c`, no `auth.authenticate_user()`, today's pip resolution (`colab/capture-only/`).
- **`umask 022`** is set in `run_steps.sh` (docker exec would default to 0000), so modes in `ls -la`
  look like a normal shell's.
- The laptop baseline (bash, git identity, curl, tree, unzip, ssh, sudo, python3 for `ptyrun.py`)
  is not part of the tutorial. `hub_retry` (Docker Hub 429s) retried twice
  (`capture-only/hub-retries.txt`: the python:3.11 base re-tag and `10-docker-shell`, 30 s each);
  the files keep the attempts that got through.

## Differences and findings vs the digest, found while running

**New (not in the digest):**

1. **The README changed after the digest** (2026-10-13, `2515e5e`): clone `main` instead of the
   starter → `dvc init` and `dvc remote add` refuse, the remote stays the **class bucket**, and the
   first push targets it (`137`, `145`); a doubled `cd data-versioning` (`133`); `git remote
   set-url` before `remote add` (`138`); a new Colab notebook pointed at a TA's own repo. The course
   map still pins `b240b1a`.
2. **Label Studio 1.23.0 disables legacy API tokens by default** (`27`), so README:198-199 fail
   with `401 … legacy token authentication has been disabled for this organization` (`42`) until
   an admin enables legacy tokens (`43`, `44`). The digest's gotcha #11 guessed at the token type;
   this is the concrete default and message. `/api/version` needs no token (`26`): the 401 comes from
   `/api/projects`, the first `get_projects()` call, as the digest predicted.
3. **On a Linux engine, `dvc init` inside the root container fails** on the bind-mounted repo:
   `repository path '/app' is not owned by current user` (`90`), leaving a half-made `.dvc/`. Fix:
   `git config --global --add safe.directory /app` on the host (picked up through the
   `~/.gitconfig` mount). Docker Desktop on macOS was not tested here; the instructor's in-container
   commit suggests it does not hit this.
4. **Label Studio's own data-permission check** prints the gotcha #12 diagnosis and a fix
   (`rm -rf … mkdir -p … sudo chown :0 mydata`) — the container exits 1 seconds after
   `docker container ls` showed it Up (`11`→`12`). The digest's `chown -R 1001` works (`16`-`18`).
5. **Compose `depends_on` race, live** (`54`): the CLI shell opens before Label Studio listens.
6. **`dvc add` on the empty, unmounted folder succeeds silently** with `nfiles: 0`
   (`d751713988987e9331980363e24189ce.dir`, `93`): the "never version nothing" trap is real.
7. **gcsfuse is 3.13.0 now** (digest: 3.12.1 on 2026-10-01) and logs JSON; its error ends
   `failed to detect credentials: open /secrets/data-service-account.json: no such file or directory`.
8. **Colab's `pip install dvc dvc-gs` today gives dvc 3.67.1 / dvc-gs 3.1.0**, not the 3.63.0 the
   container pins and the notebook's stored run shows.
9. Compose's `version` attribute warning appears on every compose run (digest gotcha #8's harmless
   warning, live); `docker-compose` exists as a compat command in this engine, so gotcha #8's
   "command not found" did not occur here.

**Digest confirmed live:** gotcha #1 (word for word, `86`), #2 and #3 (verbatim, `88`), #6 (`52`),
#12 (`13`), #13b (401 anonymous, `C13`, `122`), #13c (`--quiet` hides the error, `C19`/`C20`;
`unknown Git revision 'dataset_v25'`, `C19b`); errata #9 (compose's own bucket name, `54`), #10
(unconditional "mounted", `88`), #11 (`-k argument i required`, `42`); the B11 `git status`
checkpoint exactly (`96`); `dvc push` "N files pushed" = images + 1 (`95`: 5) and "2 objects, not 6"
for v21 (`104`); the v20 hash `89db50de….dir` / 611101 / 4 (`95`, identical to the class tag, `121`);
the class tags v20/v21/v30 only (`118`); §3.4's two addresses (`41`); the 21 + 21 files of the zip
(`09`).

**Digest details to correct:** the sample `-p` output prints `Project object at 0x…` reprs, not
dicts (`44`); the `docker container ls` checkpoint in A6 is momentary on Linux (`12`); the digest
pins `b240b1a` as "main" — it is no longer the head (item 1 above).

## Versions at the time of recording (2026-10-23)

| what | version |
| --- | --- |
| laptop Docker (stand-in for Docker Desktop) | client + engine 29.8.2, Compose v5.6.0, linux/amd64 |
| laptop git | 2.54.0 |
| Label Studio | `heartexlabs/label-studio:latest` → **1.23.0** (Community; backend commit `df96d79`), Django 5.2.17, image digest `sha256:afcc516a2277…` at pull time (**unpinned tag**; PyPI already had 1.23.2) |
| data-label-cli image | python:3.12-slim-bookworm → Python 3.12.15, uv 0.13.5; uv.lock: label-studio-sdk 2.0.12, google-cloud-storage 3.4.1, pandas 2.3.3 |
| data-version-cli image | python:3.11-slim-bookworm → Python 3.11.17, uv 0.13.5, **gcsfuse 3.13.0**, Google Cloud SDK 590.0.0 (`google-cloud-cli`); uv.lock: dvc 3.63.0, dvc-gs 3.0.2, gcsfs 2025.9.0 |
| Colab stand-in | Python 3.12.15, git 2.39.5; `pip install dvc dvc-gs` → dvc 3.67.1, dvc-gs 3.1.0, gcsfs 2026.10.1 |

Things that vary between runs and must be said with "at the time of recording" or cropped:
container ids in prompts and lists, commit hashes of *our* commits (`git log`), image ids and
sizes, build timings, created/up times, request ids in Label Studio's JSON errors, timestamps,
gcsfuse's mount-id and log timestamps, Label Studio's "update available" box, the unpinned
`label-studio:latest`, gcsfuse and google-cloud-cli versions (apt, unpinned), Colab's pip
resolution. The md5 values, sizes and file counts are deterministic for these photos.

## Re-running the captures

```
export HTTPS_PROXY=http://127.0.0.1:<port>  CA_BUNDLE=<proxy CA bundle>   # sandbox only
bash assets/terminal/capture.sh laptop setup
bash assets/terminal/capture.sh laptop pre ls1 ls2 cli cmp aclean
bash assets/terminal/capture.sh laptop b-pre b-build b-v20 b-git20 b-v21 b-git21 b-up
bash assets/terminal/capture.sh laptop t-repo t-dvc bclean
bash assets/terminal/capture.sh laptop teardown
bash assets/terminal/capture.sh colab run
docker rm -f l11-relay
```

Needs Docker with privileged containers. The laptop container persists between segment calls, so
a long capture can run in parts; a re-run of a segment overwrites only that segment's files, but
segments are not idempotent (clones, edits, the project in Label Studio): for a clean re-capture,
`teardown` + `setup` and run them all in order. Order matters (`ls1` → `ls2` → `cli` → `cmp`;
`b-build` leaves the image `b-v20` uses; `b-pre`'s prune runs before the first DVC build). The
full run takes about 35 minutes (two image pulls/builds). Without `HTTPS_PROXY`/`CA_BUNDLE` the
capture-only parts (relay, CA, base re-tags, hub retries) are skipped.

## Gate

Every command of both READMEs has a capture above, exactly as written, in README order: Part A's
`sh docker-shell.sh`, `docker container ls`, `sh docker-shell-CLI.sh` with `python cli.py -c`,
`-m`, `-p -k`, `-t -k`, `docker-shell-compose.sh`, `docker stop`/`docker ps`, and the cleanup
commands; Part B's cleanup, clone (SSH and HTTPS), `cd`/`rm -rf .git`/`git init`, the five
first-push commands, `cd data-versioning` + `sh docker-shell.sh`, `dvc init`, `dvc remote add`,
`dvc add`, `dvc push`, both rounds of `git status`/`add`/`commit`/`tag`/`push --atomic`, and the
cleanup — for the pinned README (route S) and, where it differs, today's (route T); the Colab
notebook's code cells. README steps without a live success have a documented reason and source:
the GCP console (browser → `illustration`, README field values), the Label Studio UI (browser →
`illustration`; its server side captured), the GCS-dependent outputs (honest failures captured;
success from the code's prints, the README, the notebook's stored outputs, or the labelled local
stand-ins), `git push` (no GitHub route), the uploads to the bucket (labelled stand-ins). No output
was invented. Capture-only logs live under `laptop/capture-only/` and `colab/capture-only/`.
