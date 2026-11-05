# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

**The one thing to know about this lecture's captures:** L14 deploys to Google Cloud, and the
recording sandbox has **no GCP project, no Google account and no credentials** (see the skill's
environment rules). Everything that runs on the student's own machine is captured live: the clone,
Part 2.1's `docker run` of the public image (pulled fresh, digest checked), the web app's page and
JSON routes, Part 3.3's `uv sync --frozen` + `uv run … serve`, the image's `batch` command, the
helper's dry run and the lifecycle scripts' plans, and Part 1's handler run locally by the same
functions-framework version Cloud Run's build installs. Every gcloud box is captured up to its
**honest first error** (an invalid placeholder project ID, then "no active account"), and every
console step is an `illustration` drawn from the README's own field values. What the cloud then
shows (the function's URL answering, the deployed service, speech, the job's files) is tagged
`recorded` and quoted from the README and its GIF captions (`expected/`). No output was invented.

## Which commit

**Pinned: `main` @ `46cc62fd8b1ac94ce733571a834b46002d8dd8c4`** (2026-10-22 09:26:24 −0400, "Point
student setup instructions to the main repository").

- The course tutorials page links the repo's default branch, unpinned. On 2026-11-04
  `git ls-remote https://github.com/dlops-io/serverless-deployment.git` gave `HEAD` =
  `refs/heads/main` = `46cc62f`, and every capture's `02-git-log.txt` shows the fresh clone at that
  commit: this is the README a student reaches today. The published exam edition
  `videos/ac215-l14-exam/` quotes the same commit.
- The batch `units.json` and the course map (`MLOps_Learning/course/lectures.yaml`) still name
  `4eaf3433a3430f51306e67247287a124d0c35710` (2025-10-20, "updates"). Its README is the old ~150-line
  version (Python 3.10, `functions-framework==3.*`, the `dlops/simple-translate-http` image); the
  28 commits of 2026-10-21/22 replaced it with the 1,079-line four-part tutorial. The course
  page's two anchors (`#running-app-as-cloud-function`, `#running-app-in-cloud-run`) exist only in
  the old README. `source/at-4eaf343/README.md` keeps that version for the "what changed" note and
  for checking `SLIDES.md` (written against it); nothing is run from it.
- Other branches: `codex/four-part-tutorial` @ `fadf1b9` (the rewrite; `46cc62f` is its tip plus
  one README line), `pipenv` @ `fb0cb7f` (2024 code). Not used.

## `source/` — the tutorial's own files

From [dlops-io/serverless-deployment](https://github.com/dlops-io/serverless-deployment) at
`46cc62f`, copied unchanged with `git show 46cc62f:<path>`, the repo's relative paths preserved.
Course material by the AC215 teaching staff (Harvard IACS), used for study with the instructor's
permission. The `images/` folder (console GIFs/PNGs) is **not** copied: console screenshots never
enter a frame or the repository.

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | the whole tutorial (1,079 lines): the four-part table (12-17), Before you begin + worksheet (26-60), Terminal setup (66-89), Part 1 (91-233: console steps 97-152, query string 154-173, recorded result 180-184, gcloud box 194-205, More detail 210-233), Part 2 (235-353: `docker run` 244-255, console 270-296, gcloud box 320-325), Part 3 (355-578: identity 364-428, attach + env vars 430-502, local ADC + uv 504-578), Part 4 (580-1016: buckets 593-675, job identity 677-729, job command + eleven argument chips 731-824, execute + files 826-907, overrides 909-967, helper 969-1016), clean-up (1018-1028), troubleshooting table (1033-1053), image digest (1066-1070) |
| `tutorial/function/main.py`, `requirements.txt` | Part 1's handler `hello_http` (7-12: `request.args.get` with defaults, keyword `src=`/`dest=` call) and its two pins (`functions-framework==3.10.2`, `googletrans==4.0.0rc1`) |
| `tutorial/app/Dockerfile`, `.dockerignore` | the image of Parts 2-4: `python:3.12-slim-bookworm`, `ENV … PORT=8080`, deps-then-code layers, user `app`, `EXPOSE 8080`, `CMD ["python", "-m", "translation_demo", "serve"]`, no ENTRYPOINT (1-12) |
| `tutorial/app/translation_demo/__main__.py` | one image, two startup commands: `serve` → `os.execvp("gunicorn", … 0.0.0.0:$PORT, 1 worker × 4 threads)` (22-26); `batch` options (14-20), `--plan` (42-49), read → validate → translate → speak → save (51-62), "A failing job must exit unsuccessfully" (58-61) |
| `tutorial/app/translation_demo/web.py` | `GET /` with `speech_enabled` (13-15), JSON input (17-25), `POST /api/translate` 400/502/200 (27-38), `POST /api/speech` 400/503/502/WAV (40-54) |
| `tutorial/app/translation_demo/translation.py` | nine languages (3-13), limits (16-24), lazy googletrans import (27-34) |
| `tutorial/app/translation_demo/speech.py` | `ENABLE_SPEECH` (34-35), env defaults (83-86), the Agent Platform URL (91-92), ADC with quota project (102-105), error mapping (108-119) |
| `tutorial/app/translation_demo/storage.py` | `gs://` parsing (10-16), size-checked read (23-30), unique attempt prefix, create-only uploads, manifest last (33-56) |
| `tutorial/app/translation_demo/templates/index.html` | the page: "Play audio · enable in part 3" (51), the JSON POSTs (76-80, 95-97) |
| `tutorial/app/pyproject.toml`, `requirements.lock`, `uv.lock` | the pins (flask 3.1.3, google-auth 2.62.0, google-cloud-storage 3.17.1, googletrans 4.0.0rc1, gunicorn 26.2.0, httpx 0.13.3, requests 2.34.2) |
| `tutorial/app/README.md` | the application guide: local dev + offline checks (7-32), ADC and impersonation (34-200), "One image, two startup commands" (202-223), the public image + digest (225-242) |
| `tutorial/app/examples/passage.txt`, `tutorial/app/tests/*.py` | Part 4's four-line passage; the 17 offline contract tests |
| `tutorial/run_job.py` | Part 4.6's helper: plain-name check (35-39), run id + URIs (47-50), the three gcloud commands (56-65), "Downloaded results" only after a complete manifest (66-72) |
| `tutorial/spin_up.py`, `tear_down.py`, `lifecycle/`, `tests/` | the optional scripted practice stack (`docs/lifecycle.md`) and its 25 offline tests |
| `tutorial/gif_steps.json` | the captions of the README's console GIFs: the source of the `recorded` lines in `terminal/expected/` |
| `tutorial/label_gifs.py` | (the GIF-labelling script; context only) |
| `docs/lifecycle.md` | the optional setup/cleanup guide: plan by default, `--apply` to change the cloud (1-60, 149-210) |
| `main.py`, `cli.py`, `Dockerfile`, `docker-entrypoint.sh`, `docker-shell.sh`, `pyproject.toml`, `.gitignore` | the 2025 files still at the repo root, unchanged since `4eaf343`, which the new README never mentions (mention once, do not teach) |
| `at-4eaf343/README.md` | the old README at `4eaf343` (see "Which commit") |

There is no Colab notebook for this lecture.

## `terminal/` — real terminal sessions

Captured **2026-11-04 09:24–09:35 UTC** by `terminal/capture.sh`, which runs
`terminal/run_steps.sh` inside fresh disposable containers, one segment at a time. Each README
command runs exactly as written, in README order, and its output goes to its own file: the file
starts with the command (`$ ...`), then the output, then its exit status (`[exit N]`). Steps that
are not in the README are marked *extra* below and in `run_steps.sh`.

Two kinds of file, as in L10/L11: **`step` files** (no terminal, plain output) and **`istep`
files** (a real pseudo-terminal via `ptyrun.py`, 100×40: servers run in the foreground, a second
shell fetches the evidence while they run, then Ctrl-C is typed as the `^C` byte; this copy of
`ptyrun.py` adds `--expect file:PATH`, a cue file the second shell creates when it is done, because
gunicorn logs no access lines a regex could wait for). The `istep` files are `10`, `20`
(laptop), `11`, `22`, `24`-`28` (dev).

| folder | environment | source it follows |
| --- | --- | --- |
| `laptop/` | a fresh, empty Docker engine standing in for the student's machine with Docker: `docker:29.8.2-dind` (client + engine 29.8.2, linux/amd64), Alpine, user `student` in the `docker` group, git 2.54.0, curl, python3 (for `ptyrun.py`) | README "Before you begin" step 4, Terminal setup, **Part 2.1**; extras on the image (ports, process, digest, config) and its `batch` command (Part 4's job, run locally) |
| `dev/` | `python:3.12-slim-bookworm` (Debian 12, Python 3.12.15, git 2.39.5) + curl, user `student`; uv **0.13.7** from its installer | **Part 3.3** (`cd tutorial/app`, `uv sync --frozen`, `uv run … serve`), the app guide's offline checks; Part 1's handler under functions-framework (extra stand-in) |
| `gcloud/` | `gcr.io/google.com/cloudsdktool/google-cloud-cli:slim` (Debian 13, **Google Cloud SDK 592.0.0**, core 2026.10.30) + Debian's python3 3.13.5 / `python-is-python3`, user `student`, **no account signed in** | the Terminal setup, the gcloud boxes (Part 1 deploy, Part 4.5 upload), **Part 4.6** helper, `docs/lifecycle.md` plans |
| `expected/` | — | `recorded` / `illustration` text for what only the cloud shows (below) |

### `laptop/` — the README's local steps, then the image's two commands

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt` | extra | date, Docker 29.8.2, git 2.54.0, an empty image list |
| `01-clone.txt` | Before you begin, step 4 (README:38-39 "Clone or download the repository"; the README spells no command, this is the usual `git clone`) | `Cloning into 'serverless-deployment'...` |
| `02-git-log.txt` | extra | `46cc62fd8b1a… 2026-10-22 09:26:24 -0400 Point student setup instructions to the main repository` |
| `03-ls.txt`, `04-ls-tutorial.txt` | extra | the repo root (2025 files + `tutorial/`, `docs/`, `images/`); `tutorial/`, `function/`, `app/`, `translation_demo/` |
| `05-terminal-setup.txt` | Terminal setup (README:75-81) | the seven `export` lines verbatim + `echo` of `WEB_EMAIL`, `JOB_EMAIL`, `IMAGE` → `translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com` etc. (`YOUR_PROJECT_ID` stays the README's placeholder). `gcloud auth login` (README:74) is in "not captured" |
| `10-docker-run.txt` | **Part 2.1 step 1** (README:246-249), verbatim | on an engine that never saw the image: `Unable to find image … locally`, 11 layers, `Digest: sha256:c17b6db09f74…dbe72e` (= README:1069), then gunicorn: `Starting gunicorn 26.2.0`, `Listening at: http://0.0.0.0:8080 (1)`, `Using worker: gthread`, `Booting worker with pid: 7`, `Control socket listening at /home/app/.gunicorn/gunicorn.ctl`; `^C` → `Handling signal: int`, `Worker exiting`, `Shutting down: Master`, exit 0 (Part 2.1 step 4, "Stop the local container with Ctrl+C") |
| `11-curl-home.txt` | extra (step 2, "Open http://localhost:8086") | `HTTP/1.1 200 OK`, `Server: gunicorn`, `<title>Translate · AC215</title>`, the disabled button `Play audio · enable in part 3` (step 4) |
| `12-docker-ps.txt` | extra | `0.0.0.0:8086->8080/tcp`, command `"python -m translati…"` |
| `13-docker-top.txt` | extra | the container's processes are **gunicorn** (master + worker), not `python -m translation_demo`: `os.execvp` replaced it. The USER column says `student` because `docker top` prints host user names: the image's `app` is UID 1000, which is `student` on this laptop |
| `14-curl-8080.txt` | extra | `curl: (7) Failed to connect to localhost:8080`: the laptop's port is 8086 (digest gotcha 5) |
| `15-image-digest.txt` | extra | `cgumb/ac215-translation-demo@sha256:c17b6db0…dbe72e`, the digest README:1069 and `tutorial/app/README.md:228-229` publish |
| `16-image-config.txt` | extra | `linux/amd64`, `User: app`, `WorkingDir: /app`, `ExposedPorts: map[8080/tcp:{}]`, **`Entrypoint: []`**, **`Cmd: [python -m translation_demo serve]`**, `PYTHON_VERSION=3.12.15`, `PORT=8080` |
| `17-docker-ps-after.txt` | extra | `--rm` removed the container; the image stays (260 MB on disk, 62 MB content) |
| `20-docker-run.txt` | **Part 2.1** again, verbatim (image already present: no pull lines) | the same gunicorn start and Ctrl-C shutdown, while the requests below ran |
| `21-translate-fr.txt` | extra (step 3, what **Translate** sends: `index.html:76-80`) | `POST /api/translate` `{"text": "Good afternoon everyone", "src": "en", "dest": "fr"}` → `{"dest":"fr","src":"en","text":"Bonjour à tous"}` `[HTTP 200]` (raw JSON, as the browser receives it) |
| `22-translate-zh.txt` | extra | the same to `zh-cn`, pretty-printed: `"text": "大家下午好"` |
| `23-translate-passage.txt` | extra | Part 4's `passage.txt` through the web app → its French translation ("La pluie du soir est passée. …") |
| `24-speech-disabled.txt` | extra (step 4, Play audio disabled) | `POST /api/speech` → `{"error":"Speech is disabled. Enable it for part 3 after configuring Agent Platform access."}` `[HTTP 503]` |
| `25-bad-language.txt` | extra | `dest: "xx"` → `{"error":"Choose a supported destination language."}` `[HTTP 400]` |
| `26-query-string.txt` | extra | Part 1's query string sent to this app (`GET /api/translate?text=…`) → `405` "The method is not allowed": the web app takes JSON POSTs (`tutorial/app/README.md:16-18`: "The browser sends a JSON POST here; part 1 used URL query parameters") |
| `30`-`36-port-*.txt` | extra (digest exercise E1) | `-e PORT=9090 -p 8086:8080`: `curl: (56) Recv failure: Connection reset by peer`; the log says `Listening at: http://0.0.0.0:9090`; with `-p 8086:9090` the page answers |
| `40-passage.txt` | extra (Part 4.1's input) | the four-line passage, 131 characters |
| `41-batch-plan.txt` | extra (`tutorial/app/README.md:210-217`, "For a job, override its command", with the public image for the local build `translation-demo:dev`) | `"status": "plan_only"`, `"input_characters": 131`, the five steps, `"implemented": true`, exit 0 |
| `42-batch-no-speech.txt` | extra | the real batch without `ENABLE_SPEECH`: `Batch failed: Speech is disabled. …`, **exit 1** (the job's truthful exit status, `__main__.py:58-61`) |
| `43-batch-no-identity.txt` | extra | with the job's three variables but no Google identity: `Batch failed: Google credentials are unavailable. Configure local ADC or attach an authorized runtime service account.`, exit 1 |
| `44-one-chip.txt` | extra (README:750-753, "Do not paste the whole block into one argument field") | the whole argument list as one argv element after `python`: `Error while finding module specification for ' translation_demo batch --input-uri …' (ModuleNotFoundError: No module named ' translation_demo batch --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage')`, exit 1 |
| `45-args-without-command.txt` | extra (Docker's analogue of arguments with no command: arguments replace `CMD`, and the image has no ENTRYPOINT) | `exec: "-m": executable file not found in $PATH`, exit 127 |
| `46-bad-uri.txt`, `47-batch-help.txt` | extra | a URI without `gs://` → `error: Use a gs://bucket/object-or-prefix URI.` (exit 2); `batch --help` |
| `48-docker-images.txt` | extra | nothing left running |

### `dev/` — Part 3.3 on a developer machine, and Part 1's handler locally

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt`, `01-clone.txt`, `02-git-log.txt` | extra / Before you begin step 4 | Debian 12, Python 3.12.15, git 2.39.5, no `uv` yet; clone at `46cc62f` |
| `03-uv-install.txt`, `04-uv-version.txt` | extra (README:556 "With uv installed"; uv's documented installer) | `downloading uv 0.13.7`; `uv 0.13.7` |
| `10-cd-uv-sync.txt` | **Part 3.3** (README:559-560), verbatim | `Using CPython 3.12.15`, `Creating virtual environment at: .venv`, builds `googletrans==4.0.0rc1`, `Installed 41 packages`, the full `+` list (flask 3.1.3, google-auth 2.62.0, gunicorn 26.2.0, httpx 0.13.3, …) |
| `11-uv-run-serve.txt` | **Part 3.3** (README:561-563), verbatim (`$PROJECT_ID` = the README placeholder from the Terminal setup) | gunicorn `Listening at: http://0.0.0.0:8086`, then `^C` and a clean shutdown |
| `12-curl-home.txt` | extra (README:566 "Open http://localhost:8086") | with `ENABLE_SPEECH=true` the button reads **`Play audio`** (title "Translate some text first"), no longer "enable in part 3" |
| `13-translate.txt` | extra | `Bonjour à tous`, `[HTTP 200]` |
| `14-speech-no-adc.txt` | extra (README:566 "translate, and play audio") | no ADC here (the impersonated login of README:547-548 needs a Google account): `{"error":"Google credentials are unavailable. Configure local ADC or attach an authorized runtime service account."}` `[HTTP 503]`: the app's own message for a missing identity (`speech.py:108-109`) |
| `15-unittest.txt` | extra (`tutorial/app/README.md:23`) | 17 tests, `OK` |
| `16-batch-plan.txt` | extra (`tutorial/app/README.md:24-26`) | the same plan JSON as `laptop/41` |
| `17-uv-tree.txt` | extra | the six direct dependencies |
| `18-cd-back.txt` | README:567 "Run `cd ../..`" | back at the repo root |
| `20-function-files.txt` | extra | `tutorial/function/main.py` and `requirements.txt` as the console's two files |
| `21-function-venv.txt` | extra (what the function build installs, README:212-216) | a venv with the two requirements: functions-framework 3.10.2, googletrans 4.0.0rc1, Flask 3.1.3, gunicorn 26.2.0, httpx 0.13.3 (pip 25.0.1 notes a newer pip). This file is the second run in the same container (the venv existed; the output is the same as the first) |
| `22-functions-framework.txt` | extra stand-in for Part 1's deployed function: `functions-framework --target hello_http` in `tutorial/function/`, port 8080 (the `PORT` default) | it prints nothing while serving (its gunicorn log level is `error`), then `^C` |
| `23-curl-default.txt` | Part 1.3 step 2 (README:158-159), against the stand-in | no arguments → `Bienvenido a AC215` `[HTTP 200]`, the same text the console rehearsal recorded |
| `24-curl-readme.txt` | **Part 1's gcloud box, the `curl --get` part** (README:202-204), verbatim, with `FUNCTION_URL=http://localhost:8080` in place of the `gcloud run services describe` lookup (README:200-201, needs a project) | `Bonjour à tous` (= README:183) |
| `25-curl-query-fr.txt` | Part 1.3 step 3 (README:163), the query string | `Bonjour à tous` |
| `26-curl-el.txt`, `27-curl-hi.txt`, `28-curl-zh.txt` | Part 1.3 step 4 (README:166-167) | `Καλησπέρα σε όλους`, `सबको दोपहर की नमस्ते`, `大家下午好` |
| `29-wrong-target.txt` | extra (digest gotcha 1 / exercise E4) | `--target translate` → `MissingTargetException: File /home/student/serverless-deployment/tutorial/function/main.py is expected to contain a function named 'translate'. Found: 'hello_http' instead`, exit 1 (on Cloud Run the path is the build's `/workspace/main.py`) |
| `provider-timeout/22, 23, 28` | the first run of the same segment, kept on purpose | the unofficial translation endpoint timed out on one request: the server log shows `ERROR in app: Exception on / [GET]` … `httpcore._exceptions.ReadTimeout: The read operation timed out` (traceback through `main.py:12`), and that client got `500 Internal Server Error: The server encountered an internal error …`. This is README:228-231 and 1039 ("Text translation fails → Service logs and external translation provider availability") happening for real; a re-run a minute later succeeded (the files above) |

### `gcloud/` — the gcloud boxes and the helper, with no account

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt`, `01-clone.txt`, `02-git-log.txt` | extra / Before you begin step 4 | Google Cloud SDK 592.0.0 (core 2026.10.30, bundled Python 3.14.9), Python 3.13.5 at `/usr/bin/python`; clone at `46cc62f` |
| `03-auth-list.txt` | extra (what `gcloud auth login`, README:74, would change) | `No credentialed accounts.` |
| `04-terminal-setup.txt` | Terminal setup (README:75-81) | the exports, verbatim; `gcloud config list` shows no account and no project |
| `05-function-deploy.txt` | **Part 1 gcloud box** (README:195-198), verbatim, with the placeholder left unreplaced | `ERROR: (gcloud) The project property must be set to a valid project ID, not the project name [YOUR_PROJECT_ID]`, exit 1: what a student sees who forgets "replacing the project ID" (README:70) |
| `06-help-run-deploy.txt`, `07-help-jobs-create.txt`, `08-help-jobs-execute.txt` | extra | this gcloud's own help for every README flag: `--function` ("If a value is provided, that value is used as the entrypoint"), `--base-image`, `--source` (buildpacks unless a Dockerfile is present), `--concurrency`, `--min/max-instances` (set on each new Revision); jobs `--command` ("Entrypoint for the container image"), `--args` ("If not specified and no '--command' is provided, the container image's default Cmd is used"), `--tasks`, `--max-retries`, `--task-timeout`; execute `--args` ("an execution will be created with the input values. Otherwise, the existing arguments of the job are used"), `--wait` |
| `09-upload.txt` | **Part 4.5 steps 1-2** (README:924-933), verbatim | the bucket exports + `gcloud storage cp ./passage.txt …` → the same invalid-project error |
| `10-helper.txt` | **Part 4.6** (README:975-978), verbatim | the helper prints its first command (`$ gcloud storage cp … gs://YOUR_INPUT_BUCKET/run-20261104-093…-<12 hex>/passage.txt …`), gcloud fails, `Helper stopped: gcloud failed with exit status 1. Later steps were not run.` exit 1 |
| `11-helper-dry-run.txt` | extra (README:1000 `--dry-run`) | all three commands: upload to `run-<UTC timestamp>-<12 hex>/passage.txt`, `gcloud run jobs execute translation-audio … --args=-m,translation_demo,batch,--input-uri,…,--output-uri,…/ --wait --quiet`, `Cloud outputs: gs://YOUR_OUTPUT_BUCKET/run-…/`, the recursive download; exit 0 |
| `12-helper-help.txt`, `13-helper-gs-prefix.txt`, `14-ls-results.txt` | extra (README:1000-1002) | `--help`; `--input-bucket=gs://…` → `input-bucket must be a plain name, without slashes or commas` (exit 2); the dry runs wrote nothing (no `results/`) |
| `15-spin-up-plan.txt`, `16-tear-down-plan.txt` | `docs/lifecycle.md` commands, verbatim (`--project=YOUR_PROJECT_ID`) | `Stopped: Invalid project: YOUR_PROJECT_ID`: the scripts validate the placeholder too |
| `17-helper-tests.txt` | `docs/lifecycle.md` (`python -m unittest discover -s tutorial/tests -v`) | 25 tests, `OK` |
| `18-function-deploy-signin.txt` | extra: the Part 1 box again with `PROJECT_ID=your-project-id` (a lowercase stand-in in valid project-ID format, still a placeholder) | one step further: `ERROR: (gcloud.run.deploy) You do not currently have an active account selected. Please run: $ gcloud auth login` |
| `19-helper-signin.txt` | extra: Part 4.6 verbatim with the same stand-in | the helper's first upload stops at the same sign-in error; `Helper stopped …` |
| `20-spin-up-plan.txt` | extra: `docs/lifecycle.md`'s plan with the stand-in | the whole setup plan (APIs, three service accounts, role bindings, two buckets with `--soft-delete-duration=7d`, the function, the web service and the job **by digest** `cgumb/ac215-translation-demo@sha256:c17b6db0…`), `Setup plan only; nothing created.` |
| `21-tear-down-plan.txt`, `22-ls-after.txt` | extra | tear-down needs the manifest that only `--apply` writes: `Stopped: [Errno 2] No such file or directory: 'local-state/lecture14-demo.json'`; nothing was written locally |

### capture-only (not part of the tutorial)

- **The recording proxy.** The sandbox reaches the internet only through a TLS-intercepting HTTPS
  proxy on the host's loopback. `proxy_relay.py` (container `l14-relay`) forwards it onto Docker's
  bridge; the laptop's Docker client config (`~/.docker/config.json` "proxies") passes it to the
  containers the tutorial starts. A student's machine needs none of this.
- **`laptop/capture-only/image-with-ca.Dockerfile`** (+ `-build.txt`): after `10-docker-run.txt` had
  pulled and run the **untouched** public image (its digest in `15-image-digest.txt`), the image was
  rebuilt with the proxy's CA appended to a bundle and `SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE` pointing
  at it (user back to `app`), and **re-tagged under the same name**, so the README's `docker run`
  stays verbatim and googletrans's HTTPS call can pass the proxy. Files `20`-`48` ran on that
  re-tag (local image ID `f50c08e71be0` in `48-docker-images.txt` instead of `c17b6db09f74`);
  everything else in it is byte-identical to the public image.
- **`dev/capture-only/dev-standin.Dockerfile`**, **`gcloud/capture-only/gcloud-standin.Dockerfile`**
  (+ build logs): the two stand-in machines (CA, https apt sources, git/curl or python3, a user
  `student`).
- **`ptyrun.py`** (from L10/L11, plus `--expect file:PATH`) and the readiness probes in
  `run_steps.sh` (`wait_http`; `wait_tcp` for the function, whose every `GET /` calls the provider)
  send no request a file shows.
- `gcloud/` copies `tutorial/app/examples/passage.txt` to `./passage.txt` before step 09: README
  4.5 step 2 says "Save a new short UTF-8 passage as `passage.txt`" without a command.

## What cannot run here, and how the video shows it

No GCP project, Google account, credentials, browser sign-in or billing exist in the sandbox.

| README step | why not | how the video shows it |
| --- | --- | --- |
| Terminal setup: `gcloud auth login` (README:74) | browser sign-in to a Google account | command typed; `gcloud/03-auth-list.txt` for "before"; narration says what the sign-in does (CLI identity, not ADC, README:86-87) |
| Before you begin 1-3: project selector, billing, region (README:28-37) | console | `illustration` (schematic, never a screenshot), the README's values: project **ID** vs display name, `northamerica-northeast2` (Toronto), speech `us-central1` |
| Part 1.1-1.2: Write a function → `translate-function`, Python 3.12, Allow public access, Create; paste `main.py` + `requirements.txt`, entry point `hello_http`, Save and redeploy (README:97-152) | console + Cloud Build | `illustration` with those field values; the two files from `source/tutorial/function/`; what the build then runs: `dev/20-22` (functions-framework 3.10.2 serving `hello_http`) |
| Part 1.3: the service URL, `?text=…&src=en&dest=fr`, `el`/`hi`/`zh-cn`, Logs → 200 (README:154-169) | needs the deployed function | the same handler's real answers from the local stand-in (`dev/23-28`, tagged "local stand-in"); the cloud results tagged `recorded` from `expected/part1-function-recorded.txt` (Bienvenido a AC215; Bonjour à tous; Greek; GET 200) |
| Part 1 gcloud box: `gcloud run deploy translate-function …`, `FUNCTION_URL=$(gcloud run services describe …)` (README:195-201) | project + account | `gcloud/05` (placeholder error) and `gcloud/18` (sign-in error) — instructive, see surprises; the `curl --get` line itself ran against the stand-in (`dev/24`) |
| Part 2.2: Deploy container, the image URL, `translation-demo`, public, request-based, min 0 / max 2, port 8080, 512 MiB, 1 CPU, timeout 120, concurrency 4, Create, URL, Revision History, Logs (README:270-296) + gcloud box (README:321-324) | console / project | `illustration` with those values; the command typed with no output panel; cloud results `recorded` (`expected/part2-service-recorded.txt`); the same image's behaviour is the real `laptop/10-26` |
| Part 3.1: enable Agent Platform API, create `translation-demo-runtime` with Agent Platform User + Service Usage Consumer (README:364-380) + gcloud box (README:412-419) | IAM | `illustration`; commands typed, no output panel; `expected/part3-speech-recorded.txt` ("Enabled, No keys") |
| Part 3.2: attach the account, three env vars, View diff & redeploy, Play audio (README:430-462) + gcloud box (README:489-492) | IAM + Gemini TTS | `illustration`; `recorded` playback captions; the failure side is real: `laptop/24` (speech disabled, 503), `dev/14` (no identity, 503) |
| Part 3.3: Token Creator grant, `gcloud services enable iamcredentials…`, `gcloud auth application-default login --impersonate-service-account=…`, `set-quota-project` (README:519-548) | Google account + IAM | commands typed, no output panel; the rest of 3.3 (`uv sync --frozen`, `uv run … serve`) is captured (`dev/10-18`) |
| Part 4.1: two buckets (wizard values), `run-001/passage.txt` upload, the `gs://` URI (README:593-621) + gcloud box (README:661-672) | Cloud Storage | `illustration` with the wizard values; the passage is real (`laptop/40`); the gcloud upload's first error is real (`gcloud/09`) |
| Part 4.2: `translation-audio-job`, project roles, Object Viewer on input, Object Creator on output (README:677-690) + gcloud box (README:711-721) | IAM | `illustration`; commands typed, no output panel |
| Part 4.3: Create job, image, `translation-audio`, 1 task, command `python`, the eleven argument chips, env vars, timeout 5 min, 0 retries, service account, Create (README:737-785) + gcloud box (README:816-821) | Cloud Run jobs | `illustration` of the form (chips one per value); the same argv run for real with the image (`laptop/41-47`: plan, honest failures, the one-chip and no-command mistakes); `gcloud/07` for what `--command`/`--args` mean |
| Part 4.4: Execute, History, task logs, output folder with `translated.txt`, `speech.wav`, `manifest.json` (README:828-848) + gcloud box (README:872-876) | job execution | `recorded` from `expected/part4-job-recorded.txt` (`translation-audio-hq9f5`, `run-001/de2f41…/`); the log JSON as an `illustration` from code (`expected/part4-task-log-shape.txt`, placeholders) |
| Part 4.5: `export INPUT_BUCKET…`, `gcloud storage cp`, `gcloud run jobs execute … --args=…es… --wait`, download (README:924-950) | project + account | `gcloud/09` (upload's first error); execute/download typed with no output panel; the GIF's "successful Spanish job execution" `recorded` |
| Part 4.6: the helper (README:975-978) | project + account | `gcloud/10`/`19` (verbatim, stops at sign-in), `gcloud/11` (`--dry-run`: the three commands it would run), `recorded`: "Downloaded results" only after a complete manifest (README:992-993) |
| Clean up (README:1020-1028) | console | checklist `illustration`; `gcloud/20` shows the scripted stack's resource list (what a clean-up has to cover) |

`expected/` (each file's first line says exactly where it comes from):

| file | tag | source |
| --- | --- | --- |
| `part1-function-recorded.txt` | recorded | README.md:180-184; `tutorial/gif_steps.json` (function-deploy-test.gif captions 6-13) |
| `part2-service-recorded.txt` | recorded | README.md:291-296, 314-315; gif_steps.json (container-setup.gif captions 11-18) |
| `part3-speech-recorded.txt` | recorded | README.md:380, 453-462; gif_steps.json (identity-create, identity-impersonation, identity-speech-settings, web-translation-speech); the rehearsal's own project ID in one caption replaced by `<your project ID>` |
| `part4-job-recorded.txt` | recorded | README.md:830-842, 850-852, 859-860, 963-964, 991-993; gif_steps.json (job-execution-results, terminal-job-steps, terminal-job-helper) |
| `part4-task-log-shape.txt` | illustration | the keys and order of `storage.py:48-56` as printed by `__main__.py:62`, placeholders in angle brackets: not an output |

The README's console GIFs themselves are screenshots and never appear; the gcloud boxes' success
outputs are documented nowhere in the repo as text, so those commands appear without an output panel.

## Surprises (README vs reality, 2026-11-04)

1. **The placeholder is rejected before the sign-in.** Every gcloud command with
   `PROJECT_ID=YOUR_PROJECT_ID` stops at `The project property must be set to a valid project ID,
   not the project name [YOUR_PROJECT_ID]` (`gcloud/05`, `09`, `10`), and so do the lifecycle scripts
   (`Stopped: Invalid project`, `gcloud/15-16`) — although `docs/lifecycle.md` itself shows
   `--project=YOUR_PROJECT_ID`. Only with a real (here: valid-format stand-in) ID does gcloud ask for
   `gcloud auth login` (`gcloud/18`).
2. **The translation provider is flaky, for real.** One of seven function requests timed out at the
   unofficial endpoint → HTTP 500 with a `ReadTimeout` traceback in the server log
   (`dev/provider-timeout/`); a re-run succeeded. README:228-231 warns exactly this ("inspect logs
   rather than treating a completed build as proof that translation worked").
3. **The one-chip error is longer than the digest's.** Python reports `Error while finding module
   specification for ' translation_demo batch …' (ModuleNotFoundError: No module named
   ' translation_demo batch --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage')`: the module name
   is cut at the first dot (`passage.txt`), with a leading space (`laptop/44`). Digest gotcha 11's
   `No module named  translation_demo batch …` is the gist, not the text.
4. **Arguments without the command** (Docker's analogue): `exec: "-m": executable file not found in
   $PATH`, exit 127 (`laptop/45`): the container never starts, as the digest's exercise E2 predicted.
5. **gunicorn 26.2.0 prints a fifth start-up line**, `Control socket listening at
   /home/app/.gunicorn/gunicorn.ctl` (`laptop/10`, `dev/11`), and its access log is off: the
   terminal shows nothing per request.
6. **functions-framework is silent while it serves** (gunicorn log level `error`): no "Listening"
   line (`dev/22`). The cloud function's logs come from Cloud Run, not from the framework.
7. **`docker top` names the image's `app` user `student`** (`laptop/13`): UID 1000 on both sides.
8. **The README's flags all exist in gcloud 592.0.0** (`gcloud/06-08`); `--function` takes the entry
   point, and `jobs execute --args` replaces the job's arguments for that execution only, as
   README:954-956 says.
9. **uv** prints no warnings with `UV_SYSTEM_CERTS` (capture-only); 0.13.7 deprecates the older
   `UV_NATIVE_TLS` name. Not a student issue (no proxy CA on a laptop).
10. Everything else matched the README: the pull's digest equals README:1069; port 8086 → 8080;
    "Play audio · enable in part 3" until `ENABLE_SPEECH=true`; `Bonjour à tous`; Ctrl-C stops the
    container cleanly.

### `SLIDES.md` conflicts, re-checked against the captures

- Conflict 2 (a function "has no container"): `dev/21-22` show what the build installs and runs:
  functions-framework 3.10.2 → Flask + gunicorn, serving `hello_http` on port 8080.
- Conflict 3 (the slide's positional `translate(text,src,dest)`): the deployed handler passes
  `src=`/`dest=` by name (`dev/20`), and it returns the README's results (`dev/23-28`).
- Conflict 5 (what you hand over): `main.py`, `requirements.txt`, entry point — `dev/29` is what a
  wrong entry point does. (`SLIDES.md` quotes `4eaf343` for runtime "Python 3.10" and
  `functions-framework==3.*`; at `46cc62f` it is Python 3.12 and `==3.10.2`: the captures follow
  `46cc62f`.)

## Versions (at the time of recording, 2026-11-04)

Docker client/engine 29.8.2 (dind); image `cgumb/ac215-translation-demo:lecture14-agent-platform-20261022`
= `sha256:c17b6db09f7402febb582bf327920ec9ca4eee113f5ddefa38e9da5619dbe72e` (linux/amd64, Python
3.12.15, gunicorn 26.2.0); uv 0.13.7, 41 locked packages (flask 3.1.3, google-auth 2.62.0,
google-cloud-storage 3.17.1, googletrans 4.0.0rc1, httpx 0.13.3, requests 2.34.2); functions-framework
3.10.2; Google Cloud SDK 592.0.0; git 2.54.0 (laptop) / 2.39.5 (dev); Python 3.12.15 (dev), 3.13.5
(gcloud machine).

## Re-running the captures

```bash
export HTTPS_PROXY=...   CA_BUNDLE=...   # only behind a recording proxy
bash assets/terminal/capture.sh laptop setup
bash assets/terminal/capture.sh laptop pre run1 ca run2 port job
bash assets/terminal/capture.sh laptop teardown
bash assets/terminal/capture.sh dev pre local function
bash assets/terminal/capture.sh dev teardown
bash assets/terminal/capture.sh gcloud run
docker rm -f l14-relay
```

Without a proxy, `laptop ca` is skipped and the public image runs untouched. Timestamps, the
helper's run ids, PIDs and layer ids differ on every run; translations come from an external
provider and can differ or fail (surprise 2).
