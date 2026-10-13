# Exercises · AC215 L3 — Containers II: five containers, one bucket

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real captures from
2026-10-13 (`assets/terminal/`), or were checked the same day in throwaway containers built from the
README's Dockerfile (Docker Engine 29.8.2, uv 0.13.0, Python 3.12.15 in the image). Versions on your
laptop may be newer. Parts B and C run **without** the course key, except where an item says "with
your key".

---

## Part A · The five questions from the end of the video

**Q1. Which prefix does `translate_text` read, and which stage wrote it?**

<details><summary>Answer</summary>

D reads `text_paragraphs/<group_name>/input-*.txt`: its download lists the bucket with
`match_glob=f"{text_paragraphs}/{group_name}/input-*.txt"` (`translate_text/cli.py:37`). B,
`generate_text`, wrote those objects: its upload takes every `text_paragraphs/<group>/input-*.txt` on
your laptop and uploads it under the same name (`generate_text/cli.py:97-104`). C reads the same
drawer (`synthesis_audio_en/cli.py:39`), which is why C and D can run side by side, while E reads
`text_translated/`, which D writes (`synthesis_audio/cli.py:38`). The object name (prefix, group,
`input-…` file name) is the whole contract. If D's `group_name` differs from B's, D's download
matches nothing: no error, just empty folders and nothing to translate.
</details>

**Q2. Why doesn't the mount hide the packages? What breaks without `UV_PROJECT_ENVIRONMENT`?**

<details><summary>Answer</summary>

`-v "$(pwd):/app"` covers only `/app`. Dockerfile line 9, `ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv`,
makes `uv sync` build the venv outside it (the build log says
`Creating virtual environment at: /home/app/.venv`; inside the container `echo $VIRTUAL_ENV` prints
`/home/app/.venv`, `transcribe_audio/10-venv-where.txt`). Your laptop's folder hides the copied code,
not the packages.

Without line 9, uv uses its default, `.venv` in the project folder, i.e. `/app/.venv` (checked: the
build step says `Creating virtual environment at: .venv`). Then:
- With the README's `CMD` unchanged, the container stops at once, with or without the mount:
  `/bin/bash: line 1: /home/app/.venv/bin/activate: No such file or directory`, exit status 1.
- If you also point `CMD` at `/app/.venv` (lecture 2's layout), it works without the mount, but with
  the mount your laptop's folder covers `/app` and its `.venv`, and you get the same
  `No such file or directory` (both checked). If your laptop folder had a `.venv` of its own, the
  container would see that one: a venv made for your laptop's OS, useless in Linux.
</details>

**Q3. After `uv add` in a `--rm` container: what survives, what is lost, what makes it permanent?**

<details><summary>Answer</summary>

Survives: everything written under `/app`, because `/app` is your laptop's folder. That's
`pyproject.toml` with its three new dependencies, the new `uv.lock` (138,445 bytes), and the
`input_audios/` and `text_prompts/` folders (`laptop/14-host-after-uv-add.txt`).

Lost: the 26 packages. uv installed them into `/home/app/.venv`, on the container's writable layer,
and `--rm` deletes that layer on `exit`. A new container from the same image fails again with
`ModuleNotFoundError: No module named 'google'` (`transcribe_audio/11-g10-new-container.txt`). Without
`--rm` they would sit in that one stopped container, never in the image (checked).

Permanent: rebuild with `docker build -t transcribe_audio .`. `COPY` brings in the new
`pyproject.toml` and `uv.lock`, and `uv sync` installs from them: `Resolved 27 packages`,
`Installed 26 packages` (`laptop/15-rebuild.plain.txt` lines 33 and 39). A fresh container then
prints `imports ok` with no `uv add` (`transcribe_audio/12-after-rebuild.txt`).
</details>

**Q4. Which variable tells the libraries where the key is, and why only from `/app`?**

<details><summary>Answer</summary>

`GOOGLE_APPLICATION_CREDENTIALS`, set by Dockerfile line 10 to `secrets/mega-pipeline.json`. Your
code never passes the key: `storage.Client()` asks `google.auth.default()` for credentials
(Application Default Credentials, ADC), and its first stop is this variable. The value is a
**relative** path, and google-auth checks it with `os.path.exists(filename)`
(`google/auth/_default.py:177` in google-auth 2.62.0), so it is resolved from the current directory.
`WORKDIR /app` starts the shell in `/app`, where `secrets/` is your component folder's `secrets/`
through the mount. Anywhere else, it points at nothing. Checked with a stand-in file in
`translate_text`: from `/app` the library found it (and rejected it as not a real key,
`does not have a valid type`); after `cd /tmp` it said `File secrets/mega-pipeline.json was not found.`
Stay in `/app`, or use an absolute path, as last year's solution does
(`GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json`, `docker-shell.sh:10`).
</details>

**Q5. How can an image contain a git-ignored key? The fix?**

<details><summary>Answer</summary>

`.gitignore` is read by Git only (`transcribe_audio/.gitignore:3`, `/secrets`). `docker build … .`
sends the whole folder as the build context, and `COPY --chown=app:app . ./` (Dockerfile line 26)
copies all of it, `secrets/` included. With no mount,
`docker run --rm --entrypoint ls transcribe_audio -la /app/secrets` lists `mega-pipeline.json`
(`laptop/22-g1-key-in-image.txt`). The build's `SecretsUsedInArgOrEnv` warning is about something
else: it only flags the *name* of the variable on line 10.

Fix: Docker reads `.dockerignore`. Put one line, `secrets/`, in a `.dockerignore` in each of the five
component folders and rebuild. The same `ls` then says
`ls: cannot access '/app/secrets': No such file or directory` (`laptop/25-g1-key-not-in-image.txt`),
and the app still finds the key, because the mount brings `secrets/` in at run time. Then remove the
older builds (B5), never push an image built before the fix, and if you did push one, delete it and
tell the staff.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Three notes, three places.** In the `transcribe_audio` folder, start the container with the
README's `docker run --rm -ti -v "$(pwd):/app" transcribe_audio` and type:

```bash
touch /app/note-app.txt /tmp/note-tmp.txt /home/app/note-home.txt
exit
```

Predict which notes you'll find (a) on your laptop, with `ls`, and (b) in a **new** container, with
`ls /tmp /home/app`. Then check.

<details><summary>Answer</summary>

(a) Only `note-app.txt`: `/app` is your laptop's folder, and `git status --short` now shows
`?? note-app.txt`. (b) Neither of the other two. They were on the container's throwaway layer, like
the packages from `uv add`, which live in `/home/app` too. A new container may show a
`/tmp/uv-….lock` file: that one comes from the image's own build. Delete `note-app.txt` when you're
done.
</details>

**B2. Who asked for `requests`?** Inside the container, after the step-7 `uv add`, run
`uv tree --depth 1`, then `uv tree --invert --package requests`. Predict how many direct dependencies
the first prints, and why E's bonus `uv add requests` installs nothing.

<details><summary>Answer</summary>

Three: `ffmpeg-python`, `google-cloud-speech`, `google-cloud-storage`
(`transcribe_audio/09-uv-tree.txt`); the other 23 of the 26 came along with them. The inverted tree
shows `requests v2.34.2` pulled in by `google-api-core` and by `google-cloud-storage` itself
(checked). E also uses `google-cloud-storage`, so `requests` is already installed there: `uv add
requests` prints `Resolved 25 packages` and `Checked 24 packages`
(`synthesis_audio/04-bonus-uv-add-requests.txt`), and only writes `"requests>=2.34.2"` into
`pyproject.toml`. Adding it is still right: `cli_11.py` imports `requests` itself, and shouldn't
depend on another package happening to need it.
</details>

**B3. Copy the lock first.** After the step-13 rebuild, replace Dockerfile lines 26–27 with:

```dockerfile
COPY --chown=app:app pyproject.toml uv.lock ./
RUN uv sync
COPY --chown=app:app . ./
```

Build once. Then change only `group_name` in `cli.py` and build again. Predict which build steps say
`CACHED`. Then predict what this Dockerfile does in a folder that has no `uv.lock` yet.

<details><summary>Answer</summary>

The build now has six steps. After the edit, `[2/6]` (apt), `[3/6]` (`WORKDIR`), `[4/6]` (`COPY
pyproject.toml uv.lock`) and `[5/6]` (`RUN uv sync`) are all `CACHED`. Only `[6/6] COPY . ./` runs
(checked). A `COPY` step's cache key is the content of the files it copies, and your edit only
touched a file the last `COPY` copies. `uv sync` now runs again only when `pyproject.toml` or
`uv.lock` changes, which is exactly when it should. (It works without the code because a
`uv init --bare` project has no build system: uv installs only its dependencies.) In a folder without
`uv.lock` (before step 7) the build stops at once:
`failed to compute cache key: … "/uv.lock": not found` (checked). That's why the README's order is
simpler for a first Dockerfile, and why later tutorials use this one.
</details>

**B4. A smaller `uv sync` layer.** After the step-13 rebuild, `docker history transcribe_audio`
shows the `uv sync` layer at 105 MB (`laptop/17-history.txt`). In a container, run
`du -sh /home/app/.venv /home/app/.cache/uv`. Predict the two sizes. Then change line 27 to
`RUN uv sync --no-cache`, rebuild, and compare `docker history` and `docker images`.

<details><summary>Answer</summary>

About half each: `50M` for the venv and `51M` for uv's download cache in `/home/app/.cache/uv`
(checked). With `--no-cache` the layer drops to 52.4 MB, and the image from 1.48 GB to 1.42 GB
in our check (same Docker Engine 29.8.2 as the recording). The cache speeds up the *next* uv
command on the same machine; in a finished image it mostly takes up space. (Your sizes can differ
a little with newer package versions and Docker Desktop's way of counting.)
</details>

**B5. Old builds and the key.** Every image you built before adding `.dockerignore` contained your
key. After the fix and the rebuild, is the old one gone? Run
`docker info | grep -iE "storage driver|driver-type"` and `docker images --filter dangling=true`,
and predict what each shows.

<details><summary>Answer</summary>

It depends on Docker's image store, which `docker info` names:
- **Classic store** (`Storage Driver: overlay2`): the previous build stays behind as an
  `<untagged>` image, and `docker run --rm --entrypoint ls <its ID> /app/secrets` still lists
  `mega-pipeline.json`. `docker image prune -f` deletes it.
- **containerd image store** (`driver-type: io.containerd.snapshotter.v1`, as on the Docker Engine 29
  used for the recording): rebuilding under the same name replaces the image, and no untagged copy
  is listed. But the old `COPY` layer, key included, stays in the **build cache**: delete
  `.dockerignore` and build again, and that `COPY` step says `CACHED`. `docker builder prune -f`
  removes it.

Both checked in a throwaway Docker daemon, with a stand-in key. Run both prune commands either way.
</details>

---

## Part C · Debugging

**C1. A one-shot run.** You want to run a step from your laptop without the interactive shell:
`docker run --rm -v "$(pwd):/app" transcribe_audio python cli.py -d`. It prints
`/usr/local/bin/python: /usr/local/bin/python: cannot execute binary file` and the exit status is
126 (`laptop/18-g16-entrypoint.txt`). Why, and what works?

<details><summary>Answer</summary>

The image's `ENTRYPOINT` is `["/bin/bash"]` (Dockerfile line 29). Words after the image name replace
`CMD`, so the container runs `/bin/bash python cli.py -d`. Bash takes its first argument as a script
to read. It finds `python` on `PATH` (the image's `/usr/local/bin/python`, since nothing activated
the venv) and refuses to run a binary as a script: 126. The error comes before any Python runs, so
it doesn't need the key. These work (checked with `--help` instead of `-d`):

```bash
docker run --rm -v "$(pwd):/app" transcribe_audio -c "source /home/app/.venv/bin/activate && python cli.py -d"
docker run --rm -v "$(pwd):/app" --entrypoint /home/app/.venv/bin/python transcribe_audio cli.py -d
```

`-c "uv run python cli.py -d"` works too. But `-c "python cli.py -d"` alone fails with
`ModuleNotFoundError: No module named 'google'`: without activation, `python` is the image's own,
which has none of the packages.
</details>

**C2. "But my key is right there."** In the `translate_text` container, with the key in `secrets/`,
a teammate types `cd /tmp && python /app/cli.py --help` and gets
`google.auth.exceptions.DefaultCredentialsError: File secrets/mega-pipeline.json was not found.`
Why does `--help` touch credentials at all, and why "not found"?

<details><summary>Answer</summary>

1. `translate_text/cli.py:20` creates `translate.Client()` at import, before argparse sees `--help`,
   and its constructor calls `google.auth.default()` (`google/cloud/client/__init__.py`, line 218 in
   `translate_text/03-help.txt`). C and E do the same at `cli.py:22` and `:21`. A builds its clients
   inside `download()`, `transcribe()` and `upload()`, and B's Gemini client (`generate_text/cli.py:23`)
   doesn't look for credentials when it's created, so their `--help` works without a key
   (`transcribe_audio/05-help.txt`, `generate_text/04-help.txt`).
2. `secrets/mega-pipeline.json` is relative: from `/tmp` it means `/tmp/secrets/…`. Checked with a
   stand-in file: from `/app` it was found; from `/tmp` it was not; from `/tmp` with
   `GOOGLE_APPLICATION_CREDENTIALS=/app/secrets/mega-pipeline.json` it was found again.

Fix: `cd /app`. (Starting the container from the repo root instead of the component folder fails
even earlier: `python: can't open file '/app/cli.py'`.)
</details>

**C3. `AttributeError: module 'ffmpeg' has no attribute 'input'`.** With your key in place,
`python cli.py -t` stops at `cli.py` line 67 with this error, although `import ffmpeg` worked. What
happened?

<details><summary>Answer</summary>

The wrong PyPI project. `uv add ffmpeg`, or `uv add python-ffmpeg`, installs a different package
that is also imported as `ffmpeg` but has no `input()` (both checked: the same `AttributeError`).
`cli.py` needs `ffmpeg-python` (`transcribe_audio/README.md:108`). Fix inside the container:
`uv remove ffmpeg` (or `python-ffmpeg`), `uv add ffmpeg-python`, then exit and rebuild. You can
reproduce it without a key: `python -c "import ffmpeg; ffmpeg.input('x')"`.
</details>

**C4. `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`** at `ffmpeg.run(stream)`,
`cli.py` line 69, with your key, although `ffmpeg-python` is installed. Why?

<details><summary>Answer</summary>

`ffmpeg-python` only builds a command line and starts the `ffmpeg` *program* with `subprocess`. The
program comes from Debian, through line 3's build argument. The usual cause is a line 3 without
`ffmpeg`, e.g. pasted from the appendix's sample (`ARG DEBIAN_PACKAGES="build-essential curl"`,
`README.md:179`) or from B's Dockerfile. Checked in an image built with `build-essential` only:
`which ffmpeg` prints nothing, and `ffmpeg.run` raises exactly this error from `subprocess.Popen`.
Fix: `ARG DEBIAN_PACKAGES="build-essential ffmpeg"`, exit, rebuild. The big `RUN` step runs again,
because the package list it installs changed.
</details>

**C5. "Transcribe does nothing."** With your key, one transcript in
`text_prompts/<group>/` says just `None`. You run `python cli.py -t` again: it prints `Args: …` and
`transcribe`, and nothing more. Why, and what now? (From the code: the call needs the key.)

<details><summary>Answer</summary>

When Speech-to-Text returns no results, `cli.py` writes the placeholder it started with,
`text = "None"` (lines 80, 84, 95–96). A re-run skips every recording whose `.txt` already exists
(lines 61–62), so the `None` file counts as done, and `--upload` would send it on to B. Delete that
`.txt` on your laptop, run `-t` again, and `cat` the result before `-u`.
</details>

---

## Part D · Think

**D1. Make it Spanish.** You want a Spanish podcast instead of a French one. Which lines change,
what must you delete for the new language to actually be produced, and do you need to rebuild?

<details><summary>Answer</summary>

- D: `translate_text/cli.py:61`, `target_language="fr"` → `"es"`.
- E: `synthesis_audio/cli.py:47-48`, `language_code = "fr-FR"` → `"es-ES"` and a Spanish voice name
  (the voice list is linked in those lines' comments).

No rebuild: only code changes, and the mount brings it in; no new packages. Deletions:
- D skips any paragraph whose translation already exists locally (`translate_text/cli.py:52-53`):
  delete `text_translated/<group>/*.txt` on your laptop, then `-t` and `-u`. The upload uses the
  same object names, so the Spanish replaces the French in the bucket.
- E's `--download` wipes its local `text_translated/` and fetches the Spanish
  (`synthesis_audio/cli.py:33-40`), but `--synthesis` skips every recording whose audio object
  already exists in the bucket (`blob.exists()`, line 68). The French audio under
  `output_audios/<group>/` has to be deleted first (whether the course key may delete objects is up
  to the staff). The local check at line 56 never triggers, because E never saves audio locally.
</details>

**D2. A recording called `podcast.mp3`.** Someone adds `input_audios/podcast.mp3` (no `input-`
prefix) to the bucket. Trace how far it gets through the pipeline.

<details><summary>Answer</summary>

1. A's `--download` takes every object under `input_audios/` (`transcribe_audio/cli.py:39-43`), so
   it's downloaded.
2. `--transcribe` processes every file in the folder and writes
   `text_prompts/<group>/podcast.txt` (`:54-59`).
3. `--upload` only takes `input-*.txt` (`:108`), so it's never uploaded, and B's download would
   ignore it anyway (`generate_text/cli.py:42`).

It stops after A's local output, with no error anywhere. File names are part of the interface.
</details>

**D3. From a Mac to a VM.** A teammate builds `generate_text` on an Apple Silicon Mac and pushes it
to Docker Hub. You pull it on an amd64 Linux VM and run it. What happens, and how should it have
been built?

<details><summary>Answer</summary>

`docker build` makes an image for the machine it runs on: `linux/arm64` on Apple Silicon
(`python:3.12-slim-bookworm` exists for both). An amd64 machine without emulation can't run arm64
programs: forcing an arm64 image on our amd64 check machine gave
`exec /bin/uname: exec format error`. Build for both platforms instead, as last year's solution does
in its `prod` mode (`docker-shell.sh:62-70`):
`docker buildx build --platform linux/amd64,linux/arm64 -t <USER NAME>/generate_text --push .`
And push only images built with the `.dockerignore` fix.
</details>

**D4. A bucket instead of APIs.** The README says production services call each other's APIs, and
this tutorial uses a shared bucket instead (`README.md:61-67`). What does the bucket give you, and
what does it cost?

<details><summary>Answer</summary>

Gains: the stages don't need to be running at the same time, or even on the same day; every
intermediate result is a file you can open, check and redo (D2, C5); teams share one pipeline,
separated by prefixes; and the leaderboard can read the same storage. Costs: nothing triggers the
next stage (you run each by hand); mistakes are silent (a wrong name or group just matches nothing,
Q1 and D2); two runs with the same group overwrite each other; and every stage needs credentials for
the bucket, here one shared key. With APIs, a call answers at once and can return an error, but every
service must be up and reachable.
</details>

**D5. Three ways to hand a container the key.** Compare: (a) the README as written (the key in each
component's `secrets/`, copied into the image), (b) the same with `.dockerignore`, (c) last year's
solution (one `secrets/` folder outside the repo, mounted at `/secrets`, with an absolute
`GOOGLE_APPLICATION_CREDENTIALS`, `docker-shell.sh:9-10`, `:96-99`). For each: is the key in the
image? Could Git pick it up? Does it still work after `cd /tmp`? How many copies are on your laptop?

<details><summary>Answer</summary>

| | in the image? | Git | after `cd /tmp` | copies |
| --- | --- | --- | --- | --- |
| (a) | yes, in every image | ignored (`/secrets` in four component `.gitignore` files, `secrets/` at the root for `generate_text`) | no (relative path) | five |
| (b) | no | ignored | no | five |
| (c) | no | outside the repo: nothing to ignore | yes (`/secrets/mega-pipeline.json`) | one |

(c) is where the course goes next: the key never enters the repo or an image, and one copy serves
every component.
</details>
