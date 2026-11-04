# Exercises · AC215 L14 — Serverless deployment: a function, a service and a job on Cloud Run

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real: the captures of
2026-11-04 (`assets/terminal/`: `laptop/…` is a fresh Docker 29.8.2 engine standing in for your
laptop, `dev/…` a Debian 12 shell with Python 3.12.15 and uv 0.13.7, `gcloud/…` Google Cloud SDK
592.0.0 with **no account signed in**), and the extra checks run for these exercises, listed with
their logs in [`assets/exercise-checks/`](assets/exercise-checks/README.md). The README is
`dlops-io/serverless-deployment` at `46cc62f`; `README:NN` means its line NN. Nothing here
touched a Google project: whatever only the cloud can show is quoted from the README's own
recording (`expected/…`, *recorded*) or worked out from the code, and the answer says which.
Versions are those at the time of recording; yours may be newer. Where a check publishes host
port 18086, the README's port is 8086: use 8086.

---

## Part A · The five questions from the end of the video

**Q1. Place Parts 1 and 2 on the lecture's 2×2: what do you hand over, and who builds the image
in each case?**

<details><summary>Answer</summary>

Both sit in the bottom (serverless) row; they differ in the column.

- **Part 1, "a file · serverless":** you hand over `main.py`, `requirements.txt` and the entry
  point `hello_http` (README:124-152). **Cloud Build** builds the image: it installs the
  requirements once, at build time, configures the Functions Framework and publishes an image to
  Artifact Registry (README:212-216; the gcloud box says `--source=tutorial/function
  --base-image=python312`, README:195-198, and gcloud's help says a source deploy uses Google
  Cloud buildpacks unless a Dockerfile is present, `gcloud/06`). Inside, functions-framework runs
  a Flask app under gunicorn: the same two pins install functions-framework 3.10.2, Flask 3.1.3
  and gunicorn 26.2.0 on a laptop (`dev/21`). So the file cell has a container inside, and that
  image is what clean-up step 4 removes.
- **Parts 2–4, "a container · serverless":** you hand over a finished image,
  `cgumb/ac215-translation-demo:lecture14-agent-platform-20261022`, built by the tutorial's
  authors from `tutorial/app/Dockerfile`. Cloud Run builds nothing: "We supplied an already-built
  image, so this deployment did not need to build our source" (README:314-315).

The top row (a rented machine) is Lectures 1 and 2.
</details>

**Q2. Which two settings make the meter run while nobody is using the app, and what does min
instances buy you?**

<details><summary>Answer</summary>

**Minimum number of instances ≥ 1** (an instance is kept running and billed while idle) and
**instance-based billing** (each instance is billed for its whole lifetime, not only while it
serves requests). The README's service uses **Request-based** billing and **minimum 0**
(README:281-283, `--min-instances=0`), so compute bills only while requests are being served. That
is the condition under which the lecture's "pay only when your code runs" holds; the build, the
stored function image, the buckets and each speech call bill separately.

A minimum instance buys **warmth, not capacity**: a request that arrives after a quiet spell
need not wait for a cold start ("Minimum-instance settings can keep capacity warm when that
matters", README:223-224). It does not raise how many requests can be served at once; that is
max instances × concurrency (D1).
</details>

**Q3. Who may call it, and who it runs as: which setting answers each, and why is no key file
needed?**

<details><summary>Answer</summary>

- **Who may call it:** the service's **Authentication → Allow public access** (README:281); the
  gcloud boxes spell it `--no-invoker-iam-check` (README:198, 323). It only admits callers: it
  gives the app no right to call anything.
- **Who it runs as:** the **Security** tab's **Service account**, `translation-demo-runtime`
  (README:437-439; `--service-account="$WEB_EMAIL"`, README:491). Until you attach one, the service
  normally runs as the project's default compute account. The account's roles decide what the
  running app may call: **Agent Platform User** (call the model) and **Service Usage Consumer**
  (the app names your project as quota project, `speech.py:102-105`).
- **No key file:** Cloud Run hands the running instance short-lived tokens for the attached account,
  and the app's `google.auth.default(…)` (Application Default Credentials, `speech.py:102`) finds
  them by itself. "You do not need to create or download a key" (README:380); the README's
  recording shows the account "Enabled, No keys" (`expected/part3-speech-recorded.txt:2`). On your
  laptop the same line finds the ADC file that the impersonated login of section 3.3 wrote
  (README:547-548), again without a private key.

Attaching the account is a third, separate right: **your** Service Account User on it
(README:432-434).
</details>

**Q4. Why does the job set a command and eleven separate arguments, and what happens with
neither?**

<details><summary>Answer</summary>

The image has two start-up slots: an **empty entrypoint** and the command
`python -m translation_demo serve` (`laptop/16`: `Entrypoint: []`, `Cmd: [python -m
translation_demo serve]`). **Container command** `python` fills the empty entrypoint slot (gcloud's
help: `--command` is the "Entrypoint for the container image", `gcloud/07`). **Container
arguments** replace the default command, and each chip is one item of the argument list, with no
shell to split a line (README:750-753). Together the process becomes
`python -m translation_demo batch --input-uri gs://…/passage.txt --src en --dest fr --output-uri gs://…/run-001/`:
the `batch` program, which reads, translates, speaks, saves and exits (`__main__.py:51-62`).

With **neither**, the job runs the image default, `serve`: gunicorn starts listening and never
exits, so the task runs into its 5-minute timeout and fails (README:1044, "Job starts a server
instead of finishing"). Checked with Docker: the default container was still running 15 s later,
`Listening at: http://0.0.0.0:8080` (exercise check C3 d). The other mistakes are in C3.
</details>

**Q5. Name the lecture's three downsides of serverless (slide 16), and what this tutorial gives
you for each.**

<details><summary>Answer</summary>

- **Cold starts** → **min instances ≥ 1** keeps an instance warm, for money (Q2). The README adds
  that a cold start starts an instance of your app, not necessarily a new machine, and that no
  fixed idle time predicts it (README:218-224).
- **Limited control and debugging** → three places to look: the **build and start-up logs** (a
  wrong entry point, C1), the **service logs** (the translation provider's timeout, C10; speech
  errors, C5–C6), and the **job's logs and `manifest.json`** (a job's success is the manifest saying
  `complete`, not the green check alone). The README's troubleshooting table (README:1035-1046)
  maps each symptom to its check.
- **Vendor lock-in** → the parts you wrote ran on a plain laptop: the function under the open-source
  Functions Framework (`dev/22`–`28`), the image under Docker (`laptop/10`–`48`). The Google-specific
  parts are the console set-up, IAM (the service accounts and roles) and Cloud Build.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Who chooses the port?** With Docker running, predict what `curl` says, then run:

```bash
docker run -d --name port-demo --rm -e PORT=9090 -p 8086:8080 \
  cgumb/ac215-translation-demo:lecture14-agent-platform-20261022
curl -sS http://localhost:8086/
docker logs port-demo 2>&1 | grep Listening
docker stop port-demo
```

Then fix it without removing `-e PORT=9090`.

<details><summary>Answer</summary>

`curl: (56) Recv failure: Connection reset by peer`, and the log says `Listening at:
http://0.0.0.0:9090 (1)` (`laptop/31`, `32`; the same in the exercise check B1). `serve` binds
gunicorn to `0.0.0.0:$PORT` (`__main__.py:23-24`), so the app moved to 9090, while Docker still
pipes the laptop's 8086 to the container's 8080, where nothing listens. Fix: `-p 8086:9090`; then
`curl -s http://localhost:8086/ | grep -o '<title>.*</title>'` prints `<title>Translate ·
AC215</title>` (`laptop/35`). The right-hand number must be where the app listens. Cloud Run does
the same in reverse: it sets `PORT` (8080 in the service's container settings, README:284-285) and
connects to it.
</details>

**B2. Tag or digest?** Run the README's `docker run` once (it pulls the image), then:

```bash
docker image inspect --format '{{index .RepoDigests 0}}' \
  cgumb/ac215-translation-demo:lecture14-agent-platform-20261022
docker images --digests cgumb/ac215-translation-demo
```

Compare with README:1069. Which reference would you deploy if you had to reproduce the deployment
next May?

<details><summary>Answer</summary>

The pull reports `Digest: sha256:c17b6db09f7402febb582bf327920ec9ca4eee113f5ddefa38e9da5619dbe72e`
(`laptop/10:16`), and `RepoDigests` gives
`cgumb/ac215-translation-demo@sha256:c17b6db0…dbe72e` (`laptop/15:2`): the digest README:1069
publishes. The tag `lecture14-agent-platform-20261022` is a movable label: whoever owns the
repository can push a new image under it. The digest is a fingerprint of the bytes and cannot point
anywhere else. To reproduce, deploy `cgumb/ac215-translation-demo@sha256:c17b6db0…` (the lifecycle
scripts do, `gcloud/20`); the console steps paste the tag (README:276-278, 741-743), and the revision
records the digest it resolved. (Our re-run for these exercises was refused by Docker Hub with
`429 Too Many Requests`; the captures above are from the recording.)
</details>

**B3. One image, a different program.** The job and the web service run the same image. Predict
the output, then run the job's own arguments with `--plan` added (no API call, no upload):

```bash
docker run --rm cgumb/ac215-translation-demo:lecture14-agent-platform-20261022 \
  python -m translation_demo batch --plan \
  --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage.txt --src en --dest fr \
  --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/
```

Why is `input_characters` empty? Try `--text-file examples/passage.txt` in place of `--input-uri`.

<details><summary>Answer</summary>

A JSON plan, exit 0: `"status": "plan_only"`, `"input_characters": null`, the two URIs, `en` →
`fr`, five steps ("Read the passage", "Translate the complete passage", "Synthesize speech with
Agent Platform", "Save text, audio, and completion manifest to a unique attempt prefix", "Exit")
and `"implemented": true` (exercise check B3). No gunicorn: the arguments replaced the image's
`serve` command. A remote plan deliberately does not download its input or look for credentials
(`__main__.py:36-37`), so it cannot count characters; with the image's own copy of the passage it
reports `"input_characters": 131` (exercise check, last C4 step; `laptop/41`). The app guide's
offline version is `uv run python -m translation_demo batch --plan --text-file examples/passage.txt
…` in `tutorial/app` (`dev/16`).
</details>

**B4. An override that forgets a flag.** Section 4.5 executes the saved French job with
`--args=…,--src,en,--dest,es,…`. Suppose you leave out `--dest,es`. Predict the language, then check
with a plan:

```bash
docker run --rm cgumb/ac215-translation-demo:lecture14-agent-platform-20261022 \
  python -m translation_demo batch --plan \
  --input-uri gs://YOUR_INPUT_BUCKET/run-002/passage.txt --src en \
  --output-uri gs://YOUR_OUTPUT_BUCKET/run-002/ | grep language
```

<details><summary>Answer</summary>

`"destination_language": "fr"` (exercise check B4). Not because the saved job says French: an
override replaces the **whole** argument list for that execution (README:953-956; gcloud's help,
"an execution will be created with the input values", `gcloud/08`), so nothing is merged from the
saved job. A flag you leave out falls back to the **program's** default, `--dest` = `fr`
(`__main__.py:18`). The saved job happens to say `fr` too, so this mistake is invisible here: leave
out `--src` and the program uses its default `en`, whatever the job says. Spell every argument in
every override (the helper does: B7).
</details>

**B5. Which values switch speech on?** Predict which of these make the page's button read
**Play audio** instead of "Play audio · enable in part 3": `ENABLE_SPEECH` unset, `true`, `True`,
`yes`, `on`. Run the image with `-e ENABLE_SPEECH=<value> -p 8086:8080`, then
`curl -s http://localhost:8086/ | grep speech-button`.

<details><summary>Answer</summary>

`true`, `True` and `yes` enable it; unset and `on` don't (exercise check B5). `enabled()` lower-cases
the value and accepts only `1`, `true` or `yes` (`speech.py:34-35`). The page renders the flag when
it loads (`web.py:13-15`), so after changing the variable on Cloud Run you need the new revision
**and** a page reload (README:1040). Enabled means only that the button may try: the speech call
still needs the project variable and an identity (C5, C6).
</details>

**B6. What reaches the handler?** Part 1's handler reads three query parameters with defaults
(`tutorial/function/main.py:9-11`). Predict `text`, `src` and `dest` for each URL:
(a) no query string; (b) `?text=Good+afternoon&dest=el`; (c) `?text=Tom%20%26%20Jerry&dest=fr`;
(d) `?text=Tom & Jerry&dest=fr`; (e) `?Dest=fr&text=Hi`.

<details><summary>Answer</summary>

Checked with Flask's test client on the real `main.py` under functions-framework 3.10.2, googletrans
replaced by a stand-in that echoes its arguments (exercise check B6):

| URL | text | src | dest |
| --- | --- | --- | --- |
| (a) none | `Welcome to AC215` | `en` | `es` |
| (b) `+` | `Good afternoon` | `en` | `el` |
| (c) `%26` | `Tom & Jerry` | `en` | `fr` |
| (d) raw `&` | `Tom ` | `en` | `fr` |
| (e) `Dest` | `Hi` | `en` | `es` |

`%20` and `+` both decode to a space; `%26` is an encoded `&`. A raw `&` ends the pair, so (d)
translates `Tom ` and the rest becomes a key nobody reads. Keys are case-sensitive, so `Dest` is
ignored and the default Spanish comes back. This is why the README's gcloud box uses
`curl --get --data-urlencode` (README:202-204): curl encodes each value for you (`dev/24` answered
`Bonjour à tous`). The real function's answers are in `dev/23`–`28` and `expected/part1-function-recorded.txt`.
</details>

**B7. The helper's plan.** In the repository root, with your exports set, run the helper with
`--dry-run` (README:1000):

```bash
python tutorial/run_job.py ./passage.txt \
  --project="$PROJECT_ID" --region="$REGION" --job="$JOB_NAME" \
  --input-bucket="$INPUT_BUCKET" --output-bucket="$OUTPUT_BUCKET" \
  --src=en --dest=fr --download-dir=./results --dry-run
```

Predict: how many commands, what folder name, and what is written to your disk? Then add
`--no-download`.

<details><summary>Answer</summary>

Three `$ gcloud …` lines and `Cloud outputs: gs://…/run-<UTC date>-<UTC time>-<12 hex>/`
(`gcloud/11`; exercise check B7): an upload to `gs://INPUT/run-…/passage.txt`, `gcloud run jobs
execute … --args=-m,translation_demo,batch,--input-uri,…,--src,en,--dest,fr,--output-uri,…/
--wait --quiet`, and a recursive download into `./results`. The run id is a UTC timestamp plus 12
random hex characters (`run_job.py:47`), so every submission gets a fresh prefix in both buckets.
A dry run executes nothing and writes nothing (`gcloud/14`). With `--no-download`, two commands:
the download is skipped and results stay in Storage. For real, it stops at the first failing
command, and prints `Downloaded results` only after it finds a `manifest.json` with `"status":
"complete"` next to both files (`run_job.py:66-72`).
</details>

---

## Part C · Debugging

**C1. "Revision not ready."** A classmate pasted the tutorial's `main.py` and requirements, typed
`translate` as the **Function entry point**, and selected **Save and redeploy**. The build installed
the requirements, but the revision never becomes ready. What do the logs say, and what is the fix?

<details><summary>Answer</summary>

`MissingTargetException: File /workspace/main.py is expected to contain a function named
'translate'. Found: 'hello_http' instead`. The requirements are fine; when the new revision starts,
functions-framework looks up the entry point by name. Locally: `dev/29` (`…/tutorial/function/main.py
is expected to contain …`), and the exercise check C1; on Cloud Run the file is the build's
`/workspace/main.py`, and you read it in the build and start-up logs, the first of the three places to
look (README:1038). Fix the field to `hello_http` (README:150-151: "the Python function the serving
framework should call, not the filename or service name"), or rename the `def`.
</details>

**C2. "It worked in Lecture 1."** A classmate copies `googletrans==4.0.2` from the Lecture 1 project
into the function's requirements. The build succeeds; every request returns 500, and the log ends
with `AttributeError: 'coroutine' object has no attribute 'text'`. Why?

<details><summary>Answer</summary>

googletrans 4.0.2's `Translator.translate` is a coroutine function (asynchronous): calling it
without `await` returns a coroutine object, and `.text` on that raises exactly this error (exercise
check C2: `coroutine function: True`, `AttributeError: 'coroutine' object has no attribute 'text'`).
The handler is synchronous (`main.py:12`). The pinned `googletrans==4.0.0rc1`
(`requirements.txt:2`) has a synchronous `translate(self, text: str, dest='en', src='auto')`. Keep
the pin. The same signature explains the keyword call: passed by position, the second argument is
`dest`, so a slide-style `translate(text, src, dest)` swaps source and destination; the handler passes
`src=` and `dest=` by name.
</details>

**C3. Four job set-ups.** Each classmate created the job from the same image. Say what each task
runs and how its execution ends: (a) Container command `python`, no arguments; (b) the eleven
arguments, no command; (c) command `python`, all eleven values pasted into **one** argument chip;
(d) neither changed.

<details><summary>Answer</summary>

Reproduced with Docker on the same image (exercise check C3; Docker's analogue, not Cloud Run's
text):

- **(a)** `python` with no script and no terminal reads its program from an empty standard input and
  exits **0** at once: no output, no files. Under Docker: `exit status: 0`. On Cloud Run this would
  likely be a *succeeded* execution with an empty output prefix (not checked there), which is why
  success means a `manifest.json`, not a green check.
- **(b)** The arguments replace the image's command and the entrypoint is empty, so the first
  argument, `-m`, becomes the program: `exec: "-m": executable file not found in $PATH`, exit 127
  (`laptop/45`). The container never starts.
- **(c)** One argv element after `python`: `-m` takes the rest of that element as one module name,
  cut at the first dot: `No module named ' translation_demo batch --input-uri
  gs://YOUR_INPUT_BUCKET/run-001/passage'`, exit 1 (`laptop/44`; README:750-753, "Do not paste the
  whole block into one argument field").
- **(d)** The image default, `serve`: gunicorn listens and never exits; the task fails at its
  5-minute timeout (README:1044; the local container was still running after 15 s).

Only command `python` plus eleven separate chips runs `batch`.
</details>

**C4. The execution fails in a second.** The job's last argument is `gs://YOUR_OUTPUT_BUCKET` (no
`/run-001/`), and the task log ends with `error: …` and exit status 2. What does the log say? What
about `--dest xx`, an input URI without `gs://`, or a 6,000-character passage?

<details><summary>Answer</summary>

`batch` checks its arguments before any cloud call and exits through `argparse` (exit 2)
(`__main__.py:32-40`). Exercise check C4, with the plan flag:

- output URI with no prefix: `error: A bucket and an object path or output prefix are required.`
  (`storage.py:10-16`);
- `--dest xx`: `error: Choose a supported destination language.` (nine codes, `translation.py:3-13`);
- no `gs://`: `error: Use a gs://bucket/object-or-prefix URI.` (`laptop/46`);
- too long: `error: Use at most 5,000 characters for this demo.` A file given by `--input-uri` is
  only read during the real run: a Storage object over 20,000 bytes fails then with `Batch failed: Use
  an input text file no larger than 20,000 bytes for this demo.` and exit 1 (`storage.py:23-28`, from
  the code).
</details>

**C5. Play audio is on, but says 503.** After section 3.2 the button reads **Play audio**, but
playing gives `Set GOOGLE_CLOUD_PROJECT to the project authorized for Agent Platform.` What was
missed? And what does the same request say when all three variables are set but the service has no
usable identity?

<details><summary>Answer</summary>

Only `ENABLE_SPEECH=true` was added; the second variable, `GOOGLE_CLOUD_PROJECT`, is missing
(README:444-448 lists all three). With all three set and no identity: `Google credentials are
unavailable. Configure local ADC or attach an authorized runtime service account.` Both are HTTP 503
(exercise check C5; `dev/14` for the second). The app maps configuration problems to 503
(`web.py:50-51`) and checks in this order: flag (`Speech is disabled …`, `laptop/24`), text, size,
language, project, then credentials (`speech.py:74-109`). Read the message before changing
permissions (README:457-458).
</details>

**C6. Works with `uv run`, not in Docker.** On your laptop, after the impersonated
`gcloud auth application-default login`, `uv run python -m translation_demo serve` speaks. You build
the image and run it with the same three variables, and Play audio says `Google credentials are
unavailable …`. Why, and what is the fix?

<details><summary>Answer</summary>

Your ADC file lives on the laptop (`~/.config/gcloud/application_default_credentials.json`), and
"Your host's credentials are **not automatically inside a container**" (`tutorial/app/README.md:168-170`).
Inside the container, `google.auth.default()` finds nothing: the same 503 (exercise check C5, a
container with no identity). Fix, for local development only: mount that one file read-only and
point `GOOGLE_APPLICATION_CREDENTIALS` at it, as `tutorial/app/README.md:171-182` shows (with
`--user "$(id -u):$(id -g)"` so the container user can read it; rootless Docker may need `--user
0:0`, lines 186-188). Never copy it into the image or Git (README:551-552). On Cloud Run you attach
the service account instead.
</details>

**C7. Translate works, Play audio says 400.** A classmate pastes a long passage into the web app.
Translate works; Play audio answers 400. What is the likely message, and why not 503?

<details><summary>Answer</summary>

`Use at most 4,000 UTF-8 bytes for this short speech demo.` (`speech.py:79-80`). Translation allows
up to 5,000 characters (`translation.py:19-20`), but speech counts **bytes** of the translated text,
and accented or non-Latin letters take 2–3 bytes each: 2,001 × `é` is only 2,001 characters but 4,002
bytes, and the check answers `400` (exercise check C7). It is 400 because the request itself is the
problem (`web.py:48-49`), not the deployment's configuration. A made-up `dest` also gives 400
(`Choose a supported destination language.`). Shorten the text.
</details>

**C8. The helper refuses.** Three classmates run the helper: one passes
`--input-bucket=gs://my-input`, one `--dest=es,de`, and one runs it on a laptop where gcloud isn't
installed. What does each see?

<details><summary>Answer</summary>

- `run_job.py: error: input-bucket must be a plain name, without slashes or commas` (exit 2;
  `gcloud/13`). It wants the bucket **name** (README:1002); it builds the `gs://` URIs itself.
- `run_job.py: error: dest must be a plain name, without slashes or commas`: commas separate gcloud's
  `--args` values, so a comma would smuggle in an extra argument (`run_job.py:35-39`).
- `$ gcloud storage cp …` is printed, then `Helper stopped: [Errno 2] No such file or directory:
  'gcloud'`, exit 1, nothing downloaded (exercise check C8). The helper needs Python and a signed-in
  gcloud (README:1006-1008). With gcloud but no sign-in it stops at the first command too
  (`gcloud/19`), and a gcloud failure prints `Helper stopped: gcloud failed with exit status 1. Later
  steps were not run.` (`gcloud/10`).
</details>

**C9. Two gcloud errors in a row.** You paste Part 1's gcloud box right after the Terminal setup and
get `The project property must be set to a valid project ID, not the project name
[YOUR_PROJECT_ID]`. You fix that and get `You do not currently have an active account selected.`
What did you skip each time?

<details><summary>Answer</summary>

First: the placeholder. `export PROJECT_ID=YOUR_PROJECT_ID` must hold your real project **ID**, not
the display name (README:70, 75; `gcloud/05`); gcloud rejects the placeholder before it checks any
sign-in. Second: `gcloud auth login` (README:74); `gcloud/18` shows the error once the ID has a valid
format. Note that `gcloud auth login` signs in the gcloud tool only; the app's local identity is the
separate `gcloud auth application-default login` of section 3.3 (README:86-87).
</details>

**C10. A green build and a 500.** The function deployed fine. Most queries answer; one returns `500
Internal Server Error`, and the service log shows a traceback through `main.py", line 12, in
hello_http` ending in `httpcore._exceptions.ReadTimeout: The read operation timed out`. Is the
deployment broken?

<details><summary>Answer</summary>

No. Line 12 calls googletrans, which wraps an **unofficial** outside translation endpoint that can be
slow, rate-limit or change. That request timed out and the handler has no error handling, so the
framework answered 500. It happened during our recording (`dev/provider-timeout/28`, `22`), and the
same request a minute later answered `大家下午好` (`dev/28`). The README warns: "inspect logs rather
than treating a completed build as proof that translation worked" (README:228-231; table row
README:1039). Retry; for anything real, use a supported translation API. (The web app maps the same
failure to `502` "The translation provider could not complete the request.", `web.py:33-37`.)
</details>

**C11. "Agent Platform access denied."** After section 3.2, Play audio shows `Agent Platform access
denied. Check the caller identity, enabled API, inference permissions, and quota project.` What do
you check, in which order?

<details><summary>Answer</summary>

Worked out from the code and the README (no project here): the app raises this message when Agent
Platform answers 401 or 403 (`speech.py:112-113`), and the browser gets 503. Check (1) **which
account the revision runs as** (Security tab: `translation-demo-runtime`, not the default compute
account; a new revision after the change); (2) that account's **Agent Platform User** and **Service
Usage Consumer** roles: the app sends your project as quota project (`speech.py:104`), so the second
is needed too; (3) the **Agent Platform API** is enabled in that project; (4) `GOOGLE_CLOUD_PROJECT`
is the project with those grants. A wrong `GOOGLE_CLOUD_LOCATION` gives a different message, `The
speech model was not found …` (404, `speech.py:114-115`). README:457-458 and 1041.
</details>

---

## Part D · Think

**D1. Concurrency and the ceiling.** The web service (concurrency 4, max instances 2) gets 3
translations per second, each taking 2 s (the provider is slow). How many requests are in flight, how
many instances run, and what happens when traffic doubles? What would you change?

<details><summary>Answer</summary>

Little's law: in flight = arrival rate × time in system = 3 × 2 = **6**, so ⌈6 / 4⌉ = **2
instances**, already the maximum. At 6 per second, 12 are in flight but there are only 2 × 4 = **8
slots**: the rest wait, and some can be refused (Cloud Run's documentation describes a 429 when no
instance is available; not checked here). Raise **max instances**, or raise **concurrency together
with gunicorn's threads** (4 threads, `__main__.py:25`, which is why the README sets concurrency
4). Raising **min instances** does not help: warmth, not capacity (Q2).
</details>

**D2. Create without reading.** The job account has only **Storage Object Creator** on the output
bucket. Why can it write three files, and why can it neither overwrite an earlier result nor list the
folder? Who reads the results?

<details><summary>Answer</summary>

`save_artifacts` only creates new objects: a fresh `uuid4().hex` folder per attempt
(`storage.py:37-38`) and every upload with `if_generation_match=0` ("only if no object exists",
lines 46 and 54-55). Creating needs `storage.objects.create`, which Object Creator has. Overwriting
would need delete and listing `storage.objects.list`; Object Creator grants neither (README:686-688;
Google's role definition, not checked live). So a re-execution lands beside the first attempt instead
of over it, and a bug cannot erase earlier output. **You** read the results with your own identity
(README:692-694); the job never needs to.
</details>

**D3. Three principals.** For each, name the principal, the role and the resource: (a) a teammate who
should deploy the job with its account attached; (b) the job itself; (c) you, testing speech locally
as the web service's account.

<details><summary>Answer</summary>

- (a) the teammate's **user** — **Service Account User** on `translation-audio-job` (plus rights to
  create Cloud Run jobs); to run it with overrides, `run.jobs.runWithOverrides` (Cloud Run Jobs
  Executor With Overrides, README:724-727).
- (b) `serviceAccount:translation-audio-job@YOUR_PROJECT_ID.iam.gserviceaccount.com` — **Agent
  Platform User** and **Service Usage Consumer** on the project; **Storage Object Viewer** on the
  input bucket; **Storage Object Creator** on the output bucket (README:711-721).
- (c) your **user** — **Service Account Token Creator** on `translation-demo-runtime`, with the IAM
  Service Account Credentials API enabled (README:519-525, 541-545).

None implies another: the job's Storage roles give you nothing, and your Token Creator gives the job
nothing.
</details>

**D4. Function, service or job?** For your Cheese App milestone (deploy your model or API with Cloud
Functions or Cloud Run), which would you choose for (a) a small webhook that reformats one JSON
request; (b) the API server your frontend calls; (c) a nightly re-embedding of 10,000 documents?

<details><summary>Answer</summary>

(a) A **Cloud Run function**: one handler, a few dependencies, a URL; Google builds the image. (b) A
**Cloud Run service** from your own image: several routes, your Dockerfile and lockfile, a container
you can run on your laptop first, with min/max instances and concurrency tuned to its threads. (c) A
**Cloud Run job**: finite work with no one waiting, input and output in Cloud Storage, its own
service account, a timeout, retries 0 at first, success proven by a manifest; split it over several
tasks only once one task is too slow (README:902-903 calls chunking and parallel tasks extensions).
The heavy model itself would sit behind an endpoint (Lecture 15), with the deployed code around it
(README:7-10).
</details>

**D5. A pattern that misses.** `tutorial/app/.dockerignore` lists `__pycache__` and `*.pyc`. Does
that keep `translation_demo/__pycache__/` out of the image? What pattern would?

<details><summary>Answer</summary>

No. `.dockerignore` patterns match from the root of the build context, so `__pycache__` excludes only
a top-level `__pycache__/`, and `*.pyc` only top-level `.pyc` files. The digest found six
`translation_demo/__pycache__/*.cpython-312.pyc` files in the public image's code layer (digest
erratum 5; not re-checked here, because our local build's source had no caches). Harmless, since they
match the sources, but `**/__pycache__` and `**/*.pyc` are what was meant.
</details>

**D6. What still bills?** You deleted `translate-function`, `translation-demo` and
`translation-audio`. Name four things that can still cost money, and how to check each.

<details><summary>Answer</summary>

1. The **function's image** in Artifact Registry, which stays after the service is gone (clean-up step
   4, README:1027-1028). 2. **Buckets and their objects**, including **soft-deleted** ones, which stay
   recoverable and billable during the retention period (`docs/lifecycle.md:176-177`). 3. The
   **build's source archives and logs** in Google's managed build storage (`docs/lifecycle.md:205-210`).
4. Anything you left with **min instances ≥ 1** or **instance-based billing** in another service. Check
   Artifact Registry, Cloud Storage (and its soft-deleted objects), and the Cloud Run services list.
   Don't delete the shared public image, which others use (README:1027-1028); and the two service
   accounts cost nothing, but delete them once detached (README:1023-1025).
</details>
