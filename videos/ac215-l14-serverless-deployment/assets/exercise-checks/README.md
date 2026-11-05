# Exercise checks · ac215-l14-serverless-deployment (2026-11-04, 10:53–11:00 UTC)

What was run to verify [`exercises.md`](../../exercises.md), beyond the captures in `assets/terminal/`, which the
answers cite directly (`laptop/NN`, `dev/NN`, `gcloud/NN`, `expected/…`; provenance in
[`ASSETS.md`](../../ASSETS.md)). Logs and the check scripts are in [`logs/`](logs/). Every step in a log starts with
its command (`$ …`) and ends with `[exit N]`, as in `assets/terminal/run_steps.sh`. Where a step pipes into `grep`
or `tail`, `[exit N]` is the last command's status; steps that matter print the real status themselves
(`exit status: N`).

There was **no Google account, no GCP project and no credentials**, as in the captures. Nothing here created a cloud
resource or called a Google API: every check ran offline (`--network none`), except the image build and the pip
installs, which only downloaded packages. The translation provider was never called: B6 replaces googletrans with an
echo stand-in. No log contains a person's name, a key, a real project ID or a bucket name; the placeholders are the
README's (`YOUR_INPUT_BUCKET`, `YOUR_OUTPUT_BUCKET`) and the valid-format stand-in `your-project-id`.

## Setup (disposable; nothing from the repo ran on the host)

- Docker Engine 29.8.2 on the session machine; the repo's files are the copies in `assets/source/` (unchanged at
  `46cc62f`), mounted read-only.
- **The public image could not be pulled that day.** [`setup.sh`](logs/setup.sh) ([`setup.log`](logs/setup.log)):
  Docker Hub answered `429 Too Many Requests` to the pull by tag and by digest. So the image checks ran on a **local
  build of the same source**: [`image-local.Dockerfile`](logs/image-local.Dockerfile) is `tutorial/app/Dockerfile`
  line for line, plus three check-only lines that trust the session proxy's CA (pip needs it to reach PyPI); the
  build context was `tutorial/app/` at `46cc62f`
  ([`image-local-build.log`](logs/image-local-build.log): the same `requirements.lock` pins, Python 3.12.15,
  gunicorn 26.2.0). Its config matches the public image's (`laptop/16`): linux/amd64, user `app`, no entrypoint,
  `Cmd ["python","-m","translation_demo","serve"]`. **Difference:** its digest is not `c17b6db0…`, and its source
  tree has no `__pycache__` folders, so the `.dockerignore` note (exercises D5) could not be re-checked; the
  public image's own behaviour is in the captures `laptop/10`–`48`. The image `l14ex/translation-demo:local` was
  removed afterwards.
- [`function-run.sh`](logs/function-run.sh) runs [`function.sh`](logs/function.sh) in `python:3.12-slim-bookworm`
  (Python 3.12.15) with `tutorial/function/` mounted at `/fn`; network only for pip (through the session proxy).
- [`helper-run.sh`](logs/helper-run.sh) runs [`helper.sh`](logs/helper.sh) in `python:3.12-slim-bookworm` with
  `--network none` and `tutorial/` mounted at `/repo/tutorial`. No gcloud is installed in it.
- [`lib.sh`](logs/lib.sh): the `step` function. [`image.sh`](logs/image.sh) runs from the host's Docker CLI; it
  publishes host port **18086** where the README uses 8086, so it could not collide with anything else on the
  machine.

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| B1 | `image.sh` "B1": `-e PORT=9090 -p 18086:8080`, `curl`, `docker logs`; then `-p 18086:9090` ([`image.log`](logs/image.log)) | `curl: (56) Recv failure: Connection reset by peer` (exit 56); `Listening at: http://0.0.0.0:9090 (1)`; with the pipe at 9090, `<title>Translate · AC215</title>`. Same as the captures `laptop/30`–`36` (public image, port 8086) |
| B2 | `setup.sh`: pulls by tag and by digest ([`setup.log`](logs/setup.log)) | **not re-run**: `429 Too Many Requests` from Docker Hub. The answer uses `laptop/10:16` and `laptop/15:2` (the digest the fresh pull reported equals README:1069) |
| B3 | `image.sh` "B3": `batch --plan` with the job's own arguments; "C4" last step: `--text-file examples/passage.txt` | `"status": "plan_only"`, `"input_characters": null` for `--input-uri`, the five steps, `"implemented": true`, exit 0; `"input_characters": 131` for the file |
| B4 | `image.sh` "B4": the run-002 override without `--dest`; `helper.sh` step 2 | `"destination_language": "fr"`; the helper's `--args` ends `…,--src,en,--dest,fr,…` when `--dest` is left out |
| B5 | `image.sh` "C5-C7, B5": the page's speech button for `ENABLE_SPEECH` unset, `true`, `True`, `yes`, `on` | unset and `on`: `Play audio · enable in part 3` (disabled, "Enable speech with Agent Platform credentials in part 3"); `true`, `True`, `yes`: `Play audio` (title "Translate some text first") |
| B6 | `function.sh` last step: `functions_framework.create_app(target="hello_http", source="/fn/main.py")` with googletrans replaced by an echo stand-in; Flask's test client ([`function.log`](logs/function.log)) | `GET /` → `text='Welcome to AC215' src='en' dest='es'`; `%20` and `+` arrive as spaces; `%26` as `&`; a raw `&` cuts the text to `'Tom '`; `Dest=fr` is ignored (`dest='es'`) |
| B7 | `helper.sh` steps 1, 3 ([`helper.log`](logs/helper.log)) | three `$ gcloud …` lines and `Cloud outputs: …` with `run-20261104-105856-<12 hex>`; with `--no-download`, two commands; nothing written |
| C1 | `function.sh` step 2: `functions-framework --target translate` in `tutorial/function` | `functions_framework.exceptions.MissingTargetException: File /fn/main.py is expected to contain a function named 'translate'. Found: 'hello_http' instead` (the capture `dev/29` shows the same with the repo path) |
| C2 | `function.sh` steps 1, 3, 4: the two pins; `inspect.signature`; googletrans 4.0.2 in a second venv | functions-framework 3.10.2, googletrans 4.0.0rc1, Flask 3.1.3, gunicorn 26.2.0, httpx 0.13.3; 4.0.0rc1: `translate(self, text: str, dest='en', src='auto')`, not a coroutine function; 4.0.2 (its module still reports `__version__` 3.4.0): a coroutine function, the call returns a `coroutine`, and `.text` raises `AttributeError: 'coroutine' object has no attribute 'text'` |
| C3, Q4 | `image.sh` "C3": (a) command `python`, no arguments; (b) arguments, no command; (c) the eleven values in one argument; (d) neither, checked after 15 s | (a) no output, `exit status: 0`; (b) `exec: "-m": executable file not found in $PATH`, `exit status: 127`; (c) `ModuleNotFoundError: No module named ' translation_demo batch --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage'`, `exit status: 1`; (d) `running after 15 s: true`, `Listening at: http://0.0.0.0:8080 (1)` |
| C4 | `image.sh` "C4": `--dest xx`; `--output-uri gs://YOUR_OUTPUT_BUCKET`; `--input-uri` without `gs://`; a 5,001-character passage | `error: Choose a supported destination language.` (`exit status: 2`); `error: A bucket and an object path or output prefix are required.`; `error: Use a gs://bucket/object-or-prefix URI.`; `error: Use at most 5,000 characters for this demo.` |
| C5, C6 | `image.sh` "C5-C7": `POST /api/speech` sent from inside the container, speech on | without `GOOGLE_CLOUD_PROJECT`: `503 {"error":"Set GOOGLE_CLOUD_PROJECT to the project authorized for Agent Platform."}`; all three variables, no identity: `503 {"error":"Google credentials are unavailable. Configure local ADC or attach an authorized runtime service account."}` |
| C7 | same | 2,001 × `é` (4,002 UTF-8 bytes): `400 {"error":"Use at most 4,000 UTF-8 bytes for this short speech demo."}`; `dest: "xx"`: `400 {"error":"Choose a supported destination language."}` |
| C8 | `helper.sh` steps 4–8 | `--input-bucket=gs://…`: `error: input-bucket must be a plain name, without slashes or commas`; `--dest=es,de`: `error: dest must be a plain name, …`; 5,001 characters: `error: Use a nonempty UTF-8 passage of at most 5,000 characters and 20,000 bytes`; with no gcloud on `PATH`: `$ gcloud storage cp …`, then `Helper stopped: [Errno 2] No such file or directory: 'gcloud'`, `exit status: 1`, no `results/` |

## Not run (and why)

- **Everything that needs a Google account or project**: deploying the function, the service and the job, IAM
  grants, buckets, speech, executions, downloads. Their answers cite the README, the code at `46cc62f`, the gcloud
  help captured in `gcloud/06`–`08`, and the README's recording (`expected/`, tagged `recorded`), and say so. The
  no-account failures are the captures `gcloud/05`, `09`, `10`, `18`, `19`.
- **Cloud Run's own messages and limits**: what Cloud Run prints when a job's first argument becomes the program
  (C3 b shows Docker's analogue), whether a job with command `python` and no arguments also exits 0 there (C3 a ran
  under Docker, whose stdin was empty), the status code a refused request gets when every instance is busy (D1), and
  console labels. Answers say "Docker's analogue" or "per Cloud Run's documentation, not checked here".
- **B2 (tag vs digest)**: Docker Hub's 429; the captures `laptop/10` and `laptop/15` answer it.
- **The offline test suites**: captured in `dev/15` (17 tests, `OK`) and `gcloud/17` (25 tests, `OK`); not repeated.

## Cleanup

Every check container ran with `--rm` or was stopped and removed by name (the last step of `image.log` counts 0
containers named `l14ex-…`). The local image `l14ex/translation-demo:local` and the build context in the session
scratchpad were deleted afterwards; the base image `python:3.12-slim-bookworm` was already on the machine and was
kept. Nothing was written outside the containers, the scratchpad and this folder.
