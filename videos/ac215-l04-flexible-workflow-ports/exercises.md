# Exercises · AC215 L4 — Containers II-b: build or pull, ports and Compose

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real captures from
2026-10-14 (`assets/terminal/`), or were checked the same day on a throwaway "laptop" like the
recording's: Docker Engine 29.8.2, Compose v5.6.0, buildx v0.37.2, the tutorials' own Dockerfiles
(`build/exercises_checks.md` lists every command). Versions, container IDs and ephemeral ports on
your laptop will differ. There was no Google account: nothing below needs your key, except where an
item says "with your key".

---

## Part A · The five questions from the end of the video

**Q1. Which files define a mega-pipeline image? What does `run` use when there's no local image?**

<details><summary>Answer</summary>

The recipe is three committed files in each component folder:
- `Dockerfile`: the base image `python:3.14-slim-bookworm`, the apt packages, the user `app`, then
  `COPY --chown=app:app . ./` and `RUN uv sync` (lines 39 and 41).
- `pyproject.toml`: the dependencies.
- `uv.lock`: their exact versions, which `uv sync` installs.

`docker-shell.sh` builds from the component folder (`docker build -t $IMAGE_NAME -f Dockerfile .`,
line 75), so everything else in that folder is copied in too (Q3). Not everything is pinned: the base
image tag, `apt-get upgrade` and `pip install uv` take whatever is current on the day you build
(Python 3.14.8 and uv 0.13.0 at the time of recording).

`run` (lines 79–96) first asks `docker image inspect mega-pipeline-<component>`:
- If a local image of that name exists, it's used, however old: `Using local image...`
  (`mega-laptop/18-a-run-local.txt`).
- If not, it runs `$DOCKER_USERNAME/$IMAGE_NAME`, i.e. `dlops/mega-pipeline-transcribe-audio`, tag
  `latest`. `docker run` pulls it the first time and reuses that copy afterwards.

That Docker Hub image was created on 2025-02-18 from the `pipenv-flexible-workflow` branch: Python
3.8.17, it starts `pipenv shell`, and it runs as root (`mega-laptop/72-run-registry.txt`,
`74-x-registry-image.txt`). Your folder is mounted over its `/app`: your code in their environment.
`transcribe_audio`'s `--help` still works; `generate_text` fails with
`ImportError: cannot import name 'genai' from 'google' (unknown location)`
(`76-run-registry-b.txt`); and pipenv leaves a root-owned `Pipfile` in your folder
(`73-x-host-after-registry.txt`). So build locally (no argument, or `dev`), and use `run` only for
images your team pushed from this branch under its own `DOCKER_USERNAME`.
</details>

**Q2. Which three gates must a call to your bucket pass, and where does each one fail?**

<details><summary>Answer</summary>

1. **Who are you?** The key. Google's libraries find it through
   `GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json` (`docker-shell.sh:10`, `:95`) and
   turn it into a short-lived token. This gate fails **inside your container**, before any request
   leaves: `google.auth.exceptions.DefaultCredentialsError: File /secrets/mega-pipeline.json was not
   found.` (`mega-transcribe_audio/09-download.txt`).
   - In `transcribe_audio` and `generate_text` it shows up at `--download`.
   - In `synthesis_audio_en`, `translate_text` and `synthesis_audio` even `--help` fails, because they
     build their Google client at import (`synthesis_audio_en/cli.py:23`, `translate_text/cli.py:22`,
     `synthesis_audio/cli.py:22`).
   - Usual causes: no key in the `secrets/` folder beside the repo, another file name, or the script
     run from another folder (`$(pwd)/../../secrets/`, `docker-shell.sh:9`).
2. **What may you do?** The service account's IAM roles on your project: Storage Admin for all five
   components, Agent Platform User for `generate_text`, Cloud Speech Client for `transcribe_audio`,
   Cloud Translation API User for `translate_text`. Text-to-Speech has no role (`README.md:178-185`).
   This gate fails **at Google**: the request leaves with a valid token and comes back as a 403
   permission error. The same happens when a `cli.py` still names the course's project or bucket, as
   `generate_text` and `translate_text` ship: your account has no role there.
3. **Is the API switched on?** The five services of `gcloud services enable` (`README.md:193-198`).
   Also fails **at Google**, with a 403 whose message says the API is disabled or has not been used
   in your project.

Role and API changes can take a few minutes to apply. Gates 2 and 3 were not reproduced here (no
Google account); with your key, read the last line of the traceback for "permission" or "disabled".
</details>

**Q3. How does a git-ignored key end up in an image? The fix?**

<details><summary>Answer</summary>

`.gitignore` is read by Git only (`transcribe_audio/.gitignore:3`, `/secrets`). Docker reads
`.dockerignore`, and no branch of the repo has one (checked: all eight branches). `docker build … .`
sends the component folder as the build context, and `COPY --chown=app:app . ./` (Dockerfile line 39)
copies all of it.

In a lecture 3 clone switched to this branch, the old key is still at
`transcribe_audio/secrets/mega-pipeline.json`, as the README says: "Your `secrets/` folder and any
downloaded audio stay put" (`README.md:50`). So `./docker-shell.sh dev` bakes it in, and
`docker run --rm --entrypoint ls mega-pipeline-transcribe-audio -la /app /app/secrets` lists
`mega-pipeline.json` (`mega-l03-laptop/13-x-key-in-image.txt`, a stand-in file). `prod` would push
that layer to Docker Hub, where a new repository is public.

The fix:
1. Delete every `secrets/` folder **inside** a component. The key belongs in `secrets/` beside the
   repo: outside the build context, it reaches the container only through the `-v` mount, at run time.
2. Add a `.dockerignore` containing `secrets/` to each component folder. Checked with a stand-in key:
   after it, `ls /app/secrets` in the new image says `No such file or directory`.
3. Remove images built before the fix (`docker image rm`, and `docker builder prune` for the build
   cache: lecture 3's exercise B5).
4. If an image with a key was ever pushed, delete that key (IAM & Admin › Service accounts › Keys).
   Deleting the image is not enough.

`README.md:203` ("the canonical way to make that mistake impossible") holds for Git, not for images.
</details>

**Q4. In `-p 127.0.0.1:8095:9100`: which number does the browser use, which does `gateway.py` bind,
and what does `127.0.0.1` restrict?**

<details><summary>Answer</summary>

The order is IP address : host port : container port (`README.md:224-230`).
- **8095** is for the browser: `http://localhost:8095` worked, and `localhost:8090` was refused
  (`port-laptop/32-send-8095.txt`, `33-curl-8090-gone.txt`).
- **9100** is what `gateway.py` binds: `port = int(os.environ.get("PORT", "9100"))` and
  `HTTPServer(("", port), Gateway)` (`gateway.py:51-52`). The README never sets the gateway's `PORT`,
  so it's the default, on every address of its own container (`""`). Moving the street door didn't
  touch the room.
- **127.0.0.1** restricts the laptop side: Docker accepts connections for 8095 only on the laptop's
  loopback address, so only programs on your laptop can connect. Without it, `-p 8091:9100` shows
  `0.0.0.0:8091->9100/tcp` in `docker ps`: every address of your laptop, so other machines on your
  network may connect (`21-x-ps-all-addresses.txt`).

It restricts nothing inside the container: the gateway must still listen on all of its own addresses
(C2). And the container never learns 8095: its banner still says `open http://localhost:8090`
(`gateway.py:53`, `34-logs-gateway-8095.txt`).
</details>

**Q5. Inside the gateway, what is `localhost`, and which name reaches the processor?**

<details><summary>Answer</summary>

`localhost` is the gateway container itself: each container has its own network stack, with its own
loopback and its own ports. `docker exec gateway curl --max-time 3 http://localhost:9200/health` fails
with `curl: (7) Failed to connect to localhost port 9200` (`port-laptop/25-exec-localhost.txt`), while
on 9100, the gateway's own port, `localhost` returns the page (`26-x-exec-localhost-9100.txt`).

The processor is reached by its container name, **`processor`**, on port 9200:
`docker exec gateway curl http://processor:9200/health` prints `ok` (`24-exec-processor.txt`). It works
because both containers are on the user-defined network `toynet`: the gateway's `/etc/resolv.conf`
says `nameserver 127.0.0.11`, Docker's built-in DNS, which answers `processor` with the processor's
address on `toynet` (`172.19.0.2` in our run; `28-network-inspect.txt`, `29-x-dns.txt`). The gateway
takes the name from `-e PROCESSOR_HOST=processor` (`gateway.py:13`). Under Compose the same name works
(`51-compose-exec.txt`). On Docker's default `bridge` network, names don't resolve at all (C1).
</details>

---

## Part B · Hands-on (predict, then run)

**B1. `EXPOSE` is not publish.** In your port_toy clone, add the line `EXPOSE 9200` to
`processor/Dockerfile`, right after `WORKDIR /app`. Rebuild with
`docker build -t toy-processor ./processor` and start both containers as in Step 1 (remove old ones
first). Predict (a) the processor's `PORTS` cell in `docker ps`, (b) whether
`curl --max-time 3 http://localhost:9200/health` now works from your laptop. (c) Then re-create the
processor with `-P` (capital P) added to its `docker run`, and look again.

<details><summary>Answer</summary>

(a) `9200/tcp`: a declared port with no arrow and no host side, the "declared" case of
`README.md:211`. (b) Still `curl: (7) Failed to connect to localhost:9200 after 1 ms: Could not
connect to server` (checked). `EXPOSE` only writes a note into the image
(`docker image inspect --format '{{json .Config.ExposedPorts}}' toy-processor` prints
`{"9200/tcp":{}}`); it "documents a container port. It does not publish it." (`README.md:545`).
(c) `-P` publishes every exposed port to a random free host port, on all addresses: our check got
`0.0.0.0:32768->9200/tcp` (`docker port processor` tells you which), and
`curl http://localhost:32768/health` printed `ok`. Only `-p`, `-P` and Compose's `ports:` open a
door on your laptop. Undo: `git checkout processor/Dockerfile`, rebuild, re-create the processor.
</details>

**B2. Two rooms with the same number.** Re-create the processor with `-e PORT=9100`, and the gateway
with `-e PROCESSOR_PORT=9100` (keep `-p 127.0.0.1:8090:9100`). Does either one fail with "port is
already allocated"? What does the page show?

<details><summary>Answer</summary>

Both start: `processor listening on port 9100 (internal only)` and
`gateway listening on port 9100  →  open http://localhost:8090`. The page works and its port card
says `processor listening on port 9100` (our reply: `"listen_port": 9100`, checked). Each container
has its own set of ports, so two rooms can share a number. Only a door on the laptop can be "already
allocated" (`README.md:357-363`; `port-laptop/18-x-all-addresses-taken.txt`). Put both back on 9200
afterwards.
</details>

**B3. Step 3, in Compose.** With the app running from `docker compose up -d`, change only the
processor's `PORT: "9200"` to `"9300"` in `docker-compose.yml` (line 31) and run
`docker compose up -d`. Predict which containers Compose recreates and whether a message goes
through. Then change the gateway's `PROCESSOR_PORT` (line 21) to `"9300"` and run
`docker compose up -d` again.

<details><summary>Answer</summary>

First `up -d`: `Container gateway Running`, then `Container processor Recreate`, `Recreated`,
`Started`. Compose compares each service's settings with its running container and recreates only the
one that changed. The message fails exactly as Step 3 did by hand: our check's request (curl standing
in for the page) got `curl: (52) Empty reply from server`, the page doesn't change, and
`docker compose logs gateway` ends with `ConnectionRefusedError: [Errno 111] Connection refused`.

Second `up -d`: `Container processor Running`, `Container gateway Recreate … Started`. The message
works, with `"listen_port": 9300`. That `up -d` took about 11 seconds: the old gateway takes 10 to
stop (B4). No image was rebuilt: both are configuration. Undo with `git checkout docker-compose.yml`
and `docker compose up -d`.
</details>

**B4. Make Ctrl+C fast.** With the app running, `time docker compose down` takes about 20 seconds
(the capture: `Removed 10.2s` for each container, `64-compose-down-running.txt`). Add the line
`init: true` to both services (under each `container_name:`, same indentation), run
`docker compose up -d`, then `time docker compose down` again. Predict. Then try
`stop_signal: SIGINT` instead of `init: true`, and run `docker compose stop` and
`docker compose ps -a` before `down`.

<details><summary>Answer</summary>

Without the change: 21.1 s in our check. Each `CMD ["python", "-u", …]` makes Python the container's
first process, PID 1. Python installs no handler for SIGTERM, and Linux applies no default action to
a signal sent to PID 1, so the polite stop is ignored. Docker waits its 10-second stop timeout, then
kills (exit 137 = 128 + 9), the gateway first, then the processor.

- `init: true`: 0.96 s. Docker's small init process is now PID 1 (`docker top gateway` shows
  `/sbin/docker-init -- python -u gateway.py` and, under it, `python -u gateway.py`). It passes
  SIGTERM on to Python, which is no longer PID 1 and stops at once: `Exited (143)` (128 + 15,
  SIGTERM).
- `stop_signal: SIGINT`: 0.96 s, `Exited (130)`. Python turns SIGINT into `KeyboardInterrupt`, the
  same as Ctrl+C in a terminal; the gateway's log ends with `KeyboardInterrupt`.

By hand, `docker run --init …` does the same as `init: true`. A third way is in the code: install a
SIGTERM handler. Undo with `git checkout docker-compose.yml`.
</details>

**B5. A package that never reached the image.** In `transcribe_audio`, start the container
(`./docker-shell.sh`), then inside: `uv add rich`, `python -c "import rich"`, `exit`. Now run
`./docker-shell.sh run` and `python -c "import rich"` again. Predict both imports, and what
`git status` shows on your laptop. Then `exit`, run `./docker-shell.sh dev`, and predict which
build steps run.

<details><summary>Answer</summary>

1. Inside the first container the import works: uv installed `rich` (plus `markdown-it-py`, `mdurl`,
   `pygments`) into `/home/app/.venv`. Through the `/app` window, your laptop's `git status` shows
   ` M pyproject.toml` and ` M uv.lock` (`"rich>=15.0.0"` added, the version at the time of checking).
2. `exit` deletes the container (`--rm`), and the venv copy with `rich` in it.
3. `run` says `Using local image...`: the image built *before* `uv add`. So
   `ModuleNotFoundError: No module named 'rich'` (checked).
4. `dev`: build steps 2 and 3 `CACHED`; step 4, `COPY`, and step 5, `uv sync`, run again because
   `pyproject.toml` and `uv.lock` changed (`Resolved 31 packages`, `Installed 30 packages`). After
   that, `run` imports `rich`.

That's the README's order (`transcribe_audio/README.md:89`): `uv add` inside the container, commit
both files, then `dev`. Teammates get the package when they pull your commit and build, or when they
pull an image you pushed. Undo: `git checkout pyproject.toml uv.lock`, then `./docker-shell.sh dev`.
</details>

**B6. Get your lecture 3 work back.** After the branch switch of Get the Code, your clone holds two
stashes (`git stash list`). Predict what (a) `git stash pop` and (b) `git stash apply stash@{1}` do
on `flexible-workflow`. Then find two safe ways to recover your old group name and your lecture 3
`generate_text/Dockerfile`.

<details><summary>Answer</summary>

The stash is last in, first out: `stash@{0}` is the `git stash -u` one, holding the two untracked
`generate_text` files; `stash@{1}` holds your `cli.py` edit (`mega-l03-laptop/10-x-after.txt`).
Checked on the same lecture 3 state:

(a) `git stash pop` refuses: `generate_text/Dockerfile already exists, no checkout`, the same for
`uv.lock`, then `error: could not restore untracked files from stash`. Nothing changes, and "The stash
entry is kept in case you need it again." The branch has its own tracked files at those paths.

(b) `CONFLICT (content): Merge conflict in transcribe_audio/cli.py`: the branch rewrote the lines
around `group_name`. Back out with `git checkout HEAD -- transcribe_audio/cli.py`.

Two safe ways:
- **Read, don't apply.** `git stash show -p stash@{1}` shows your old `group_name` line; type it into
  the branch's `cli.py`. `git show 'stash@{0}^3:generate_text/Dockerfile'` prints a stashed untracked
  file (the stash's third parent holds the untracked files).
- **Go back.** From a clean working tree, `git checkout main`, then `git stash pop` twice: your
  lecture 3 state returns (checked). Not all of it, though: `transcribe_audio`'s lecture 3
  `Dockerfile`, `pyproject.toml` and `uv.lock` are gone. They were ignored, so `-u` didn't stash
  them; the switch replaced them with the branch's files, and the way back deleted those. That
  folder ends with only `.gitignore`, `README.md`, `cli.py` and `secrets/`, the old key still
  inside. Copy files out *before* you switch.

When you're done: `git stash drop` for each stash, or `git stash clear`.
</details>

**B7. What `prod` leaves behind.** Run only the builder line of `prod`, which pushes nothing:
`docker buildx create --driver-opt network=host --use --name multi-arch` (`docker-shell.sh:62`).
Predict (a) what `docker buildx ls` marks with `*`, (b) which builder the next
`./docker-shell.sh dev` builds with. Then clean up.

<details><summary>Answer</summary>

(a) `multi-arch*`, driver `docker-container`: `--use` made it the current builder, and the script
never switches back.

(b) On our Docker Engine 29.8.2 with buildx v0.37.2, still the default one. The plain build log of
`./docker-shell.sh dev` begins `#0 building with "default" instance using docker driver` (in a
terminal, the `[+] Building …` line ends with `docker:default`), and the image is updated as usual.
The current builder is used by `docker buildx build` commands like `prod`'s line 66. A
`docker buildx build -t <name> .` without `--push` or `--load` printed
`WARNING: No output specified with docker-container driver. Build result will only remain in the
build cache.`, and the local image stayed unchanged (checked with a one-file image). The first build
also starts a container, `buildx_buildkit_multi-arch0`, from the image `moby/buildkit:buildx-stable-1`.

Clean up: `docker buildx rm multi-arch` removes that container and switches back to `default*`
(checked); `docker buildx use default` only switches back. `docker image rm
moby/buildkit:buildx-stable-1` frees the image. If you're on another Docker version, check yours the
same way: `docker buildx ls`, and the first line of a plain build log.
</details>

---

## Part C · Debugging

**C1. "The page does nothing."** You started the processor without `--network`:
`docker run -d --name processor -e PORT=9200 toy-processor`, and the gateway exactly as in Step 1.
The page doesn't update, and `docker logs gateway` ends with
`socket.gaierror: [Errno -2] Name or service not known` (`port-laptop/73-x-ex3-logs.txt`). Why, and
what are two fixes?

<details><summary>Answer</summary>

The processor is on Docker's default `bridge` network, not on `toynet`, so `toynet`'s DNS doesn't know
the name `processor`. The lookup fails before any port is tried: from the gateway,
`curl: (6) Could not resolve host: processor` (`71-x-ex3-resolve.txt`). Compare Step 3's
`Connection refused`, where the name resolved and nobody listened (cheat sheet `README.md:551-552`).
The page has no error handling, so you only see it in the gateway's log (the captured request got
`Empty reply from server`, `72-x-ex3-send.txt`).

Fixes (both checked):
- `docker network connect toynet processor`: the running container joins `toynet` too (`docker
  inspect` then lists `bridge toynet`), and `curl http://processor:9200/health` from the gateway
  prints `ok` at once.
- Or `docker rm -f processor` and start it again with `--network toynet`, as the README does.

The default `bridge` network has no name lookup between containers at all: with *both* containers
started without `--network`, the gateway still can't resolve `processor` (its `/etc/resolv.conf`
holds ordinary DNS servers, not `127.0.0.11`), although the processor's IP address works. That's why
the README creates `toynet`.
</details>

**C2. A "safer" bind address.** A teammate changes `gateway.py:52` to
`server = HTTPServer(("127.0.0.1", port), Gateway)` "so it's only local", rebuilds `toy-gateway` and
starts it as in Step 1. `docker logs gateway` shows the usual banner, and `docker ps` the usual
`127.0.0.1:8090->9100/tcp`, but the browser gets an error. Explain.

<details><summary>Answer</summary>

Published traffic arrives at the container's network interface, its address on `toynet`, not at the
container's own loopback. A server bound to `127.0.0.1` *inside* the container accepts only
connections from inside that same container. Checked:
- From the laptop: `curl: (56) Recv failure: Connection reset by peer` (your browser's wording may
  differ).
- From the processor, `curl http://gateway:9100`: `Failed to connect to gateway port 9100 … Could not
  connect to server`.
- From inside the gateway, `curl http://localhost:9100` still returns the page.

Restrict on the **host** side, with `-p 127.0.0.1:8090:9100`, as the README does, and keep `""` (all
addresses) inside the container (Q4).
</details>

**C3. A name already in use.** With `transcribe_audio`'s container open in one terminal (and
`--download` already run in it), you run `./docker-shell.sh` in a second terminal. It builds, then:
`docker: Error response from daemon: Conflict. The container name "/mega-pipeline-transcribe-audio" is
already in use …`, exit status 125 (`mega-laptop/15-a-x-g9-second-shell.txt`). Why did it build again,
why the conflict, and how do you get a second shell into the same container?

<details><summary>Answer</summary>

It built again because the folder changed: `--download` had created `input_audios/` and
`text_prompts/`. Git ignores them, Docker doesn't, so `[4/5] COPY` and `[5/5] RUN uv sync` ran
again (in the capture's log they are not `CACHED`). Those folders are now in the image too: list
them in your `.dockerignore` along with `secrets/`.

The conflict: `docker run --rm --name $IMAGE_NAME` (`docker-shell.sh:92`) gives every container of a
component the same name, and the first one is still running.

A second shell: `docker exec -it mega-pipeline-transcribe-audio bash` gets you in as `app`, in `/app`,
but **without** the venv: `which python` prints `/usr/local/bin/python`, and
`import google.cloud.storage` fails with `ModuleNotFoundError: No module named 'google'` (checked).
The image activates the venv only in its start command (Dockerfile line 46), so repeat that command:

```bash
docker exec -it mega-pipeline-transcribe-audio bash -c "source /home/app/.venv/bin/activate && exec bash"
```

Or use `uv run python cli.py …` in the plain `exec` shell (checked: both print the help text). To
end the first container from outside, `docker rm -f mega-pipeline-transcribe-audio`.
</details>

**C4. Compose refuses to start.** You skip Step 3's clean-up and run `docker compose up -d`. It
prints `WARN … a network with name toynet exists but was not created by compose.`, then
`Conflict. The container name "/processor" is already in use by container …`, exit status 1
(`port-laptop/68-x-g11-compose-up.txt`). Why? And what happens if only the network is left over?

<details><summary>Answer</summary>

The compose file pins the names it creates: `container_name: gateway` and `container_name: processor`
(`docker-compose.yml:13`, `:28`) and `name: toynet` (`:39`). Docker allows one container per name,
and your by-hand containers still hold those two. Fix: `docker rm -f gateway processor` and
`docker network rm toynet` (README Step 3, "Clean up before Compose"), then `docker compose up -d`.

Without the pins, Compose would prefix its project name, the folder's: with `container_name:` and
`name: toynet` deleted, our check got `port_toy-gateway-1`, `port_toy-processor-1` and the network
`port_toy_toynet` (with no `networks:` keys at all, it would be `port_toy_default`,
`README.md:473`).

With only the network left over, Compose v5.6.0 prints the same warning and then uses it: both
containers start (`69b-x-g11-compose-up-net.txt`). But `docker compose down` then leaves `toynet`
behind, because Compose didn't create it; `docker network rm toynet` removes it
(`69c-x-g11-cleanup.txt`).
</details>

**C5. "My change to the processor doesn't show."** With the app running under Compose, you change
`processor.py` line 30 to `"upper": text.lower(),` and run `docker compose up -d`. Compose answers
`Container gateway Running`, `Container processor Running`, and the page still shows capitals.
`docker compose restart processor` doesn't help either. Why? And why would an edit to
`gateway/index.html` show at once?

<details><summary>Answer</summary>

`processor.py` reaches the container only through `COPY . .` (`processor/Dockerfile:4`): the image
holds the old copy. `up -d` saw no change in the compose file and no new image, so it left both
containers running; `restart` restarts the same image (both checked). Rebuild:
`docker compose up -d --build` (`README.md:497-501`). Its log shows `[gateway 4/4] COPY . .`
`CACHED` and `[processor 4/4] COPY . .` built, then `Container processor Recreate`, while the gateway
stays `Running`; the reply is now `hello from the laptop` (checked).

The gateway's folder is mounted (`volumes: - ./gateway:/app`, `docker-compose.yml:17-18`), and
`gateway.py:20` reads `index.html` on every page load, so an edit shows on the next reload, with no
rebuild (checked: a changed `<title>` came back from `curl` at once). An edit to `gateway.py` itself
is also visible through the mount, but Python read it when it started: it needs
`docker compose restart gateway`, still no rebuild (checked with the banner text).
</details>

**C6. `PermissionError` on a Linux VM.** You run the mega-pipeline on a Linux machine where your
user's `id -u` isn't 1000. `python cli.py --download` stops with
`PermissionError: [Errno 13] Permission denied: 'input_audios'`, raised from `makedirs()`
(`transcribe_audio/cli.py:28`). Why? (It never gets as far as the key.)

<details><summary>Answer</summary>

The container runs as `app`, uid 1000 (Dockerfile lines 30 and 35). A bind mount keeps the host's
ownership, so `/app` is your folder, owned by your uid with mode `drwxr-xr-x`: uid 1000 may read it
but not create `input_audios/` in it. Checked as a user with uid 1001; `uv add` failed there too:
``error: failed to create file `/app/pyproject.toml`: Permission denied (os error 13)``. Docker
Desktop on macOS and Windows handles file ownership in mounts for you, so this mostly hits Linux VMs.

Fixes:
- Work as a user whose uid is 1000 (`id -u`), or make the component folder writable for uid 1000.
- Or add `--user "$(id -u):$(id -g)"` to the `docker run` in `docker-shell.sh`. Checked: `--download`
  then creates the folders, owned by you, and stops at the missing key, as it should. But `uv add`
  fails: ``error: Failed to initialize cache at `/.cache/uv` `` (a uid the image doesn't know has no
  home folder), and the venv in `/home/app` belongs to `app` anyway. Fine for running the steps, not
  for changing packages.
</details>

---

## Part D · Think

**D1. Make `run` safe.** `run` pulled a February 2025 image for a branch written in September 2026.
What would you change in your team's workflow so that `./docker-shell.sh run` gives everyone the image
of the code they have?

<details><summary>Answer</summary>

The problem is the tag: `dlops/mega-pipeline-<component>:latest` is a signpost to whatever was pushed
last under that name, by whoever, from whatever branch. Nothing ties it to your commit. Some fixes:
- **Your own account.** Set `DOCKER_USERNAME` (`docker-shell.sh:13`) to your team's, so `run` never
  falls back to `dlops`.
- **Push from this branch.** Push with `prod`, after the `.dockerignore` fix (Q3).
- **A tag that names the code.** For example, tag with the commit as well as `latest`
  (`-t $DOCKER_USERNAME/$IMAGE_NAME:$(git rev-parse --short HEAD)`) and run that tag.
- **Refresh on purpose.** `docker run` pulls a tag only when it's missing: a second
  `docker run hello-world` printed no pull lines (checked), so `run` keeps reusing a cached
  `dlops/…:latest` until you pull again or remove it. `docker pull <user>/<image>` (or
  `docker run --pull=always`) asks the registry again.
- **The other direction.** `run` prefers *any* local `mega-pipeline-<component>` image, so a stale
  local build hides a fresh push: `docker image rm` it first.

And while the Dockerfile, `pyproject.toml` or `uv.lock` change every week, building locally (`dev`,
or no argument) is the safe default: it's the "early in development" mode of `README.md:71`.
</details>

**D2. Rebuild or not?** For each change, do you need to rebuild an image? (a) `group_name` in a
`cli.py`; (b) a new package with `uv add`; (c) `-e GEMINI_MODEL=gemini-2.5-flash \` added to
`generate_text/docker-shell.sh`; (d) a new key in `secrets/`; (e) the processor's `PORT` in Step 3;
(f) `processor.py` under Compose; (g) `gateway/index.html` under Compose; (h) a package added to
`ARG DEBIAN_PACKAGES`.

<details><summary>Answer</summary>

| change | rebuild? | why |
| --- | --- | --- |
| (a) `group_name` | no | the mount shows the edit at once, even in a running container (`mega-synthesis_audio_en/02-help.txt`) |
| (b) `uv add` | yes, `dev` | the packages live in the image's `/home/app/.venv`; the container's copy dies with it (B5) |
| (c) `-e GEMINI_MODEL` | no | set at `docker run`; inside, `echo $GEMINI_MODEL` prints `gemini-2.5-flash`, and the image's own environment has no such variable (checked). `cli.py:73` reads it each time `--generate` runs |
| (d) the key | never | it's mounted at `/secrets` and must never be in an image (Q3) |
| (e) `PORT` | no | configuration (`README.md:404-409`) |
| (f) `processor.py` | yes, `up -d --build` | copied in by `COPY . .` (C5) |
| (g) `index.html` | no | mounted and read on every page load (C5) |
| (h) `DEBIAN_PACKAGES` | yes | and it's the slow one: build step 2 runs again |

One catch for (a) and (c): the default mode rebuilds on every start anyway, and `docker-shell.sh` and
`cli.py` sit in the folder that `COPY . ./` copies. Editing either makes build steps 4 and 5 run again
(checked for (c)). It's quick, but it isn't "nothing".
</details>

**D3. Compose for part 1.** Write a `docker-compose.yml` for `transcribe_audio` that does what
`./docker-shell.sh` does when it runs the container: the same image, the two mounts and the
environment variable. How do you get the interactive shell from it?

<details><summary>Answer</summary>

Saved in `transcribe_audio/` (checked with `docker compose config` and runs):

```yaml
services:
  transcribe:
    build: .
    image: mega-pipeline-transcribe-audio
    volumes:
      - ./:/app
      - ../../secrets/:/secrets
    environment:
      GOOGLE_APPLICATION_CREDENTIALS: /secrets/mega-pipeline.json
    stdin_open: true
    tty: true
```

`docker compose run --rm transcribe` opens the image's start command: the shell with the venv
active, `/app` and `/secrets` mounted. If the image is missing, Compose first tries to pull it
(`failed to resolve reference "docker.io/library/mega-pipeline-transcribe-audio:latest" … not found`,
harmless) and then builds it (checked). Our check printed `app`,
`/home/app/.venv/bin/python`, `/secrets/mega-pipeline.json`, and `--download` stopped at the missing
key, as with the script. Relative paths count from the file's folder, like the script's `$(pwd)`;
`image:` gives the built image the script's name, so `./docker-shell.sh run` finds it too.

What it doesn't do: `--name` (Compose names each run `transcribe_audio-transcribe-run-<id>`, so two
shells don't conflict), the `dev`/`run` choice (`docker compose build` builds, `run` uses what's
there) and `prod`. Compose also made a network, `transcribe_audio_default`, which
`docker compose down` removes. Lecture 5 uses this kind of file: a CLI container and a database
container on one Compose network, with the same `../secrets` mount.
</details>

**D4. What's still there after the lecture?** List what this lecture may have left on your laptop and
in the cloud, and what each costs.

<details><summary>Answer</summary>

On your laptop (disk space only):
- the five component images: transcribe 1.48 GB, the others 821–836 MB (`mega-laptop/70-x-images.txt`);
- any `dlops/mega-pipeline-*` you pulled with `run`: 1.17 GB and 1.02 GB (`78-x-images-all.txt`);
- the base images (`python:3.14-slim-bookworm` 195 MB, `python:3.14-slim` 179 MB) and `hello-world`
  with its exited container (`port-laptop/46-x-after-cleanup.txt`: `docker ps -a`, then `docker rm`);
- port_toy's four images, `toy-*` and `port_toy-*`, 198 MB each but sharing layers (about 200 MB in
  all, `66-x-images-remain.txt`);
- if you tried B7 or `prod`: the `multi-arch` builder's container (`docker buildx rm multi-arch`) and
  `moby/buildkit:buildx-stable-1`;
- root-owned `Pipfile`s from `run` (`73-x-host-after-registry.txt`): your folder is yours, so `rm
  Pipfile` works (answer `y` if it asks about a write-protected file);
- your stashes in the lecture 3 clone (B6), and the key in `secrets/` beside the repo.

In the cloud:
- the bucket bills storage until you delete it, when the course no longer needs it;
- the key works until you delete it (IAM & Admin › Service accounts › Keys): delete it when you're
  done, at once if it ever left your laptop;
- the APIs bill per use, not for being enabled; the service account itself costs nothing;
- any Docker Hub repository you pushed to with `prod` is public unless you changed it.

`docker image rm <name>` (or `docker image prune` for untagged ones) frees the space; port_toy itself
never cost anything.
</details>
