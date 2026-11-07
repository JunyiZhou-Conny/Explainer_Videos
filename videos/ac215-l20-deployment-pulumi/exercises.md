# Exercises · AC215 L20 — Deployment: by hand, then Pulumi to a single VM

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real: the captures of
2026-11-05 (`assets/terminal/`: `vm/…` is a fresh Debian 12 machine standing in for your VM, with
Docker 29.9.3 from the README's `get-docker.sh`; `laptop/…` a fresh Docker 29.8.2 engine standing in
for your laptop, with the deployment toolbox built from `src/deployment/`; provenance in
[`ASSETS.md`](ASSETS.md)), and the extra checks run for these exercises, listed with their scripts
and logs in [`assets/exercise-checks/`](assets/exercise-checks/README.md). The repository is
`dlops-io/cheese-app-v3` at `3ecef56` (`main`); `README:NN` means its README's line NN, and code
references are `path:line` under `src/`. Nothing here used a Google account, a Docker Hub login or a
key: whatever only the cloud can show is worked out from the code and the captured first error, and
the answer says so. The Pulumi checks ran on Pulumi's local file backend with two small stand-in
projects, not with the tutorial's programs (those stop at their first Google call, `laptop/b43`).
Versions are those at the time of recording; yours may be newer. The checks publish host port 18080
where your VM uses 80. Wherever an answer shows a project ID or an `sa_…` user, put your own.

---

## Part A · The five questions from the end of the video

**Q1. Trace `http://<instance_ip>/api-service/status`: which gate, which container, which location
block, and which character makes the API see `/status`?**

<details><summary>Answer</summary>

1. **The gate.** The request arrives on TCP port 80. The firewall rule `allow-http`
   (`deployment/deploy_single_vm/create_instance.py:51-62`) allows port 80 from `0.0.0.0/0` to VMs
   with the network tag `http-server`, and the VM carries that tag (`:134`). (On the part 1 VM the
   console's *Allow HTTP traffic* tick added the same tag.) Nothing opens 3000, 9000 or 8000.
2. **The container.** Host port 80 belongs to the `nginx` container (`setup_webserver.py:71-102`,
   ports 80 and 443). The frontend, the API and the vector DB publish 3000, 9000 and 8000 on the VM,
   behind the closed fence.
3. **The location block.** `location ^~ /api-service/ {` (`deployment/nginx-conf/nginx/nginx.conf:35`):
   a prefix match, and `^~` means no regex location is consulted once it matches. Everything else
   falls through to `location /` (`:47`) and the frontend on 3000.
4. **The character.** The final `/` of `proxy_pass http://api-service:9000/;` (`:37`). A `proxy_pass`
   with a URI part replaces the matched prefix `/api-service/` with that URI, `/`, so the API receives
   `/status`. `api-service` is resolved by Docker's DNS on the app's network (`appnetwork` on the
   Pulumi VM, `cheese-app-network` on yours from part 1).

The v3 API is started without `ROOT_PATH` and without `--root-path` on the Pulumi VM
(`setup_containers.py:219-225`, `api-service/docker-entrypoint.sh:19`), so its routes are mounted at
the top (`api/service.py:13, 50`) and `/status` answers `{"version":"3.0"}` (`:34-36`). Checked with
stand-ins: nginx with the repo's `nginx.conf` hands `/api-service/status` to the API as `/status`;
the same routing code answers `GET /status -> 200 {"version":"3.0"}` and
`GET /api-service/status -> 404` ([`nginx.log`](assets/exercise-checks/logs/nginx.log),
[`fastapi.log`](assets/exercise-checks/logs/fastapi.log)). The footer's API version comes from this
call (`frontend-react/src/services/DataService.js:64`, through `NEXT_PUBLIC_BASE_API_URL=/api-service`).
On the part 1 VM the same trip ends in a 404 (`vm/49`): the public `dlops/…` image predates `/status`
(C10).
</details>

**Q2. What three things does `pulumi up` compare, what does `--refresh` change, and what does `-y`
skip?**

<details><summary>Answer</summary>

- **Desired state**: what your program declares when Pulumi runs it now.
- **State**: what Pulumi recorded after its last run, kept in the backend (your GCS state bucket,
  `gs://<project>-pulumi-state-bucket`, `docker-shell.sh:17`, `docker-entrypoint.sh:23`).
- **Reality**: what actually exists in the cloud and on the VM.

The plan is the difference between desired state and **state**. Reality only enters if you ask:
**`--refresh`** first reads every resource through its provider and updates the state to match, and
then diffs. Without it, a container someone removed by hand still looks present: in the stand-in,
after `docker rm -f`, `pulumi preview` said `3 unchanged` and `pulumi preview --refresh` said
`+ 1 to create` ([`pulumi.log`](assets/exercise-checks/logs/pulumi.log), "B7"). Refresh only helps
for resources a provider can read: a `remote.Command` is not re-checked (Q4).

**`-y`** answers yes to "Do you want to perform this update?". The preview is still computed and
printed, but nobody looks at it before it is applied. In a non-interactive shell, `pulumi up`
without it refuses: `error: --yes or --skip-preview or --preview-only must be passed in to proceed
when running in non-interactive mode` (`pulumi.log`, "B5"). `pulumi preview` stops before anything
changes. So: check the plan with `preview` (or answer the prompt yourself) whenever you changed
something, and keep `-y` for runs you have already reviewed.
</details>

**Q3. Name the two service accounts, where each key sits (laptop, VM), and what each may do.**

<details><summary>Answer</summary>

| | `deployment` → `deployment.json` | `gcp-service` → `gcp-service.json` |
| --- | --- | --- |
| roles (README) | Compute Admin, Compute OS Login, Artifact Registry Administrator, Kubernetes Engine Admin, Service Account User, Storage Admin (README:241-246) | Storage Object Viewer, Vertex AI Administrator, Artifact Registry Reader (README:253-255) |
| on the laptop | `secrets/deployment.json`, next to your clone, mounted into the toolbox as `/secrets` (`docker-shell.sh:9, 16, 37`) | `secrets/gcp-service.json`, same folder |
| used by | the toolbox: `gcloud auth activate-service-account` (`docker-entrypoint.sh:10`), the state bucket, Pulumi's Google provider, the image push (credential helper, `docker_config.json`), SSH through OS Login with `ssh-key-deployment` | the app: uploaded by Pulumi to `/srv/secrets/gcp-service.json` on the VM (`setup_containers.py:44-63`) and mounted into the loader and `api-service` (`:180-188`, `:220-236`), for Vertex AI (Gemini, embeddings). On the part 1 VM you pasted it into `secrets/gcp-service.json` (README:74) |
| may | create and delete VMs, disks, networks, buckets and registries, log in to VMs | read stored objects and images, call Vertex AI; it cannot create a VM, a disk or a bucket |

The **VM** should only hold the narrow key: a compromised VM with the deployment key could create
or delete anything in the project (P5 in the video). Two footnotes from the code: the VM's
*attached* identity is whatever `security:gcp_service_account_email` says, and the README sets it to
`deployment@…` (README:355, `create_instance.py:135-145`); no key file is copied for it, and its
token is limited by the scopes listed there (read-only storage, logging, monitoring, tracing,
service control). And Pulumi's Docker provider pulls the images with the toolbox's credentials,
that is as `deployment` (`setup_containers.py:92-96`). D4 tries the narrow account.

The third key, `ssh-key-deployment`, is not a service-account key: its private half stays in
`secrets/` (`-rw-------`, `laptop/b11`), its public half goes into the deployment account's OS
Login profile (README:302).
</details>

**Q4. Which of slide 19's six steps can Pulumi inspect afterwards, and which does it only remember
running? Why must those scripts be safe to run twice?**

<details><summary>Answer</summary>

| step | file | how it is managed | after the run |
| --- | --- | --- | --- |
| 1 Setup | `docker-shell.sh` | not Pulumi at all (a shell script and the toolbox) | — |
| 2 Images | `deploy_images/__main__.py` | `docker_build.Image` resources (provider: docker-build) | a resource with an ID and outputs (tag, digest) |
| 3 VM | `create_instance.py` | `gcp.compute.Network`, three `Firewall`s, a `Disk`, an `Instance` | **inspectable**: `--refresh` reads them from the Compute Engine API |
| 4 Provision | `provision_instance.py` | nine `remote.Command`s over SSH | **only remembered**: Pulumi stores the script and its output, not what it changed |
| 5 Containers | `setup_containers.py` | `docker.Network`, four `docker.Container`s through Docker over SSH, plus four `remote.Command`/`CopyToRemote` (secrets, folders) | the containers and network are **inspectable**; the commands only remembered |
| 6 Web server | `setup_webserver.py` | the `nginx` `docker.Container`, plus `remote.Command`/`CopyToRemote` for the config and the restart | the container inspectable; the commands only remembered |

Checked with the stand-ins: a container removed by hand is found by `--refresh` and re-created; a
file that a `remote.Command` created and someone deleted is not noticed (`3 unchanged`), and
`destroy` leaves it there, because these commands have no `delete` script ([`pulumi.log`](assets/exercise-checks/logs/pulumi.log),
"B7" and "Q5").

**Safe to run twice**: Pulumi cannot look at what a script did, so it may run it again whenever it
re-creates that resource: when the script text or a trigger changes (the nginx steps use the
config's checksum as a trigger, `setup_webserver.py:45, 53, 66, 111`), when a run stopped halfway
and you `up` again, or after you change what the commands depend on (check the plan for `+-` on
them). The data disk is its own resource and outlives a replaced VM. So every script is written to
be idempotent: `blkid … || mkfs.ext4 …` formats only a disk with no filesystem
(`provision_instance.py:29`), `grep -q … || … tee -a /etc/fstab` adds the mount once (`:50-52`),
`mkdir -p`, `groupadd docker || true`. Checked on an image file: the guarded line run twice keeps the
data (`ext4`, the file is still there); the plain `mkfs.ext4` run a second time, without a terminal,
reformats without asking and the file is gone ([`disk.log`](assets/exercise-checks/logs/disk.log)).
</details>

**Q5. What survives `pulumi destroy` in `deploy_single_vm`, and how do you clean it up?**

<details><summary>Answer</summary>

`pulumi destroy --stack dev --refresh -y` in `deploy_single_vm` (README:389, which doesn't say
which folder) deletes the stack's resources in reverse order: the containers over SSH, the VM, the
data disk `cheese-app-demo-disk`, the three firewalls and the network. The `remote.Command`s are
dropped from the state without running anything. What survives:

| what | why | clean up |
| --- | --- | --- |
| the images in Artifact Registry | another stack, and `retain_on_delete=True` (`deploy_images/__main__.py:31, 51, 70`): even `destroy` in `deploy_images` only forgets them | `gcloud artifacts repositories delete cheese-app-repository --location=us` |
| the repository `cheese-app-repository` | made by your extra `gcloud artifacts repositories create` line, not by Pulumi | the same command |
| both stacks' history and config | "The resources in the stack have been deleted, but the history and configuration associated with the stack are still maintained." (`laptop/b45`; the same in `pulumi.log`, "Q5") | `pulumi stack rm dev` in each project, if you are done for good |
| the state bucket `gs://<project>-pulumi-state-bucket` | created by the toolbox's entrypoint (`docker-entrypoint.sh:15-20`) | `gcloud storage rm -r gs://<project>-pulumi-state-bucket`, **last**, once no stack holds anything |
| the part 1 VM and its boot disk | the README never deletes it | VM instances → delete, with its boot disk |
| your Docker Hub images | pushed by `docker-hub.sh` | free; delete them on Docker Hub if you like |
| the service accounts, their keys, the OS Login key, the enabled APIs | made by hand | when the course ends: delete the keys (IAM → Service accounts → Keys) |
| on the laptop | the toolbox image (2.61 GB, `laptop/b36b`), the `multi-arch` builder of `docker-hub.sh` (`laptop/a03`), `src/deployment/pulumi-plugins/` | `docker image rm`, `docker buildx rm multi-arch`, `docker buildx use default` |

The gcloud lines were not run here (no account); check that **VM instances**, **Disks** and
**Artifact Registry** are empty in the console afterwards.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Follow the slash.** On your part 1 VM (nginx in front, the public images), predict which
container answers and which path it receives for: `/`, `/status`, `/api-service/`,
`/api-service/status`, `/api-service/podcasts/?limit=3`, `/api-servicex/status`, and `/api-service`
without the final slash. Then delete the last `/` of line 37 (`proxy_pass http://api-service:9000;`),
restart nginx, and predict again.

<details><summary>Answer</summary>

With the repo's file (stand-ins that print what they receive, [`nginx.log`](assets/exercise-checks/logs/nginx.log)):

| request | answered by | path it receives |
| --- | --- | --- |
| `/`, `/status` | frontend | `/`, `/status` (only `/api-service/…` goes to the API) |
| `/api-service/` | api-service | `/` (`{"message":"Welcome to AC215"}` on your VM, `vm/49`) |
| `/api-service/status` | api-service | `/status` (404 with the public image, `{"version":"3.0"}` with v3 code: Q1) |
| `/api-service/podcasts/?limit=3` | api-service | `/podcasts/?limit=3` (the query string travels along) |
| `/api-servicex/status` | frontend | `/api-servicex/status`: the prefix is `/api-service/`, with its slash |
| `/api-service` | nginx itself | `301` to `/api-service/` (nginx's rule for a prefix location ending in `/`) |

Without the final slash, `proxy_pass` has no URI part, so nginx passes the path unchanged: the API
stand-in receives `/api-service/status` and `/api-service/`. The v3 API, started without
`ROOT_PATH`, then answers 404 for `/api-service/status` (`fastapi.log`). That is the job `ROOT_PATH`
does in Kubernetes (L22): there the ingress keeps the prefix, and the app is mounted under it.
</details>

**B2. Save the access log.** The README writes `nginx.conf` with one `echo '…'` (README:156-213).
Write it instead with a quoted heredoc: `cat > conf/nginx/nginx.conf <<'EOF'`, the same text, `EOF`.
Predict the difference between the two files, whether `nginx -t` accepts each, and what one
access-log line looks like with each.

<details><summary>Answer</summary>

The echo version is 58 lines and its `log_format` is mangled: `log_format  main   - []  `, two
blank lines and a `;` (`vm/45`). The quotes inside the text close and reopen the outer quote, so the
shell expanded `$remote_addr`, `$request`, `$status`… as empty shell variables. The heredoc version
(57 lines) keeps all three `log_format` lines; with `<<'EOF'` quoted, the shell expands nothing. Both
pass `nginx -t` (routing never used the format), but the access lines differ: `-[]` with the echo
file (`vm/51`), and with the heredoc
`<client ip> - - [06/Nov/2026:01:00:21 +0000] "GET /api-service/status HTTP/1.1" 200 64 "-" "curl/8.5.0" "-"`
([`nginx.log`](assets/exercise-checks/logs/nginx.log), "B2"). The heredoc file equals the repository's
`src/deployment/nginx-conf/nginx/nginx.conf` except for blank lines and one shortened comment: on the
VM you could also copy that file over with `scp`, which is what Pulumi does (`setup_webserver.py:48-55`).
</details>

**B3. Stop, don't restart.** On your part 1 VM, stop only the frontend
(`sudo docker stop frontend`) and leave nginx alone. Predict what `/` and `/api-service/` return. Then
`sudo docker restart nginx` and predict again. How do you bring the site back?

<details><summary>Answer</summary>

While nginx keeps running, it still has the frontend's address from when it started: `/` fails with
an error page (`504` in the check, after nginx gave up waiting), but `/api-service/status` is still
forwarded to the API. After the restart nginx resolves both names again, `frontend` is not on the
network any more, and it refuses to start: `Exited (1)`,
`nginx: [emerg] host not found in upstream "frontend" in /etc/nginx/nginx.conf:48`, and now nothing
answers on port 80, the API's path included (`vm/58`; the same with stand-ins in `nginx.log`, "B3").
That is the video's opening puzzle. Fix: `sudo docker start frontend`, then `sudo docker start nginx`
(`vm/59`: `http://localhost/ -> 200`). Order matters: the names must resolve when nginx starts.
</details>

**B4. Format twice.** In any Debian or Ubuntu container (no privileges needed), make a 64 MB image
file and run the format line of `provision_instance.py:29` against it twice, with a file written in
between (`debugfs -w -R 'write history.txt history.txt' disk.img`). Predict what each run prints and
whether the file survives. Then run plain `mkfs.ext4 disk.img < /dev/null` once more.

```bash
truncate -s 64M disk.img
blkid -o value -s TYPE disk.img || mkfs.ext4 -q disk.img     # run this line twice
```

<details><summary>Answer</summary>

First run: `blkid` finds no filesystem and exits non-zero, so `mkfs.ext4` formats; nothing is
printed (with `-q`). Second run: `blkid` prints `ext4` and exits 0, so `||` skips the format, and
`debugfs -R 'cat history.txt' disk.img` still prints the file. Plain `mkfs.ext4` with no terminal
reformats without asking, and the file is gone: `history.txt: File not found by ext2_lookup`
([`disk.log`](assets/exercise-checks/logs/disk.log)). Over Pulumi's SSH session there is no terminal
either, so the guard is the only thing standing between a re-run and your chat history and model on
`/mnt/disk-1`.
</details>

**B5. Run it again.** In `deploy_images`, after a successful `pulumi up --stack dev --refresh -y`,
predict the plan of `pulumi preview --stack dev --refresh` with no change to any file. Then predict
what `pulumi up --stack dev` (without `-y`) does in a script, and what `pulumi stack init dev` says
the second time you enter the toolbox.

<details><summary>Answer</summary>

Not "no changes": the three images change, because `timestamp_tag` is `datetime.now()`
(`deploy_images/__main__.py:13`) and the tag is an input of each image (`:25`). Every `up` builds and
pushes three new tags, so the registry grows (GOLD: storage costs), and the VM stack then gets new
image tags. The stand-in, which keeps the same timestamp tag and export name, shows the shape:
second run `+-1 to replace` with the output going from `…:20261106010441` to `…:20261106010445`
([`pulumi.log`](assets/exercise-checks/logs/pulumi.log), "B5"; the real program's plan line for a
`docker_build.Image` was not captured: your preview shows the exact symbol). D2 fixes it.

Without `-y` in a non-interactive script: `error: --yes or --skip-preview or --preview-only must be
passed in to proceed when running in non-interactive mode` (exit 2). In a terminal it shows the plan
and asks. The second `pulumi stack init dev`: `error: stack 'organization/<project>/dev' already
exists` (the state is in your bucket, not in the container); use `pulumi stack select dev`.
</details>

**B6. Images first, then the VM.** After B5's new images, predict the plan in `deploy_single_vm`.
Which resources change, and why?

<details><summary>Answer</summary>

The VM program reads the images stack's outputs through
`pulumi.StackReference("organization/deploy-images/dev")` (`setup_containers.py:27-31`), and each
app container's `image` is the first tag (`:112`, `:172`, `:210`). New tags mean new inputs for
`frontend`, the `vector-db-loader` and `api-service`, and a container cannot change its image in
place: Pulumi replaces those three (the loader runs again and reloads the collection). The VM, disk,
firewalls, `vector-db` (`chromadb/chroma:latest`, `:134`) and `nginx` (`nginx:stable`) don't change,
and the provisioning commands don't run again because none of their inputs changed. The stand-in
shows the mechanism: the reference's output changes and its container is `+-1 to replace`
(`[diff: ~labels]`, its tag travels as a label), while the `remote.Command` stays unchanged
([`pulumi.log`](assets/exercise-checks/logs/pulumi.log), "B6"). Not run with the real programs.
</details>

**B7. Drift.** On the Pulumi VM, someone runs `sudo docker rm -f nginx`. Predict the plan of
`pulumi preview --stack dev` and of `pulumi preview --stack dev --refresh`. Then someone deletes
`/conf/nginx/nginx.conf` instead: what does `--refresh` find?

<details><summary>Answer</summary>

Without `--refresh`, Pulumi compares the program with its state, which still lists the container:
no changes, and the site stays down. With `--refresh`, the Docker provider reads the VM's Docker,
finds no `nginx`, drops it from the state, and the plan is `+ create` for `deploy-nginx-container`;
`up --refresh -y` brings it back. The stand-in: `3 unchanged` without, `+ 1 to create` with, and the
container re-created ([`pulumi.log`](assets/exercise-checks/logs/pulumi.log), "B7").

The deleted config file is invisible: it was placed by `upload-nginx-conf` and `move-nginx-conf`,
which are commands (`setup_webserver.py:48-68`). Their inputs didn't change (the checksum is computed
from your laptop's copy), so the plan is empty (the stand-in: `3 unchanged` after its file was
deleted). nginx keeps running with the file it opened, until a restart. To force a new upload, change
the file (new checksum) or replace the step: `pulumi up --stack dev --refresh -y
--replace <urn of upload-nginx-conf>` (the URN from `pulumi stack --show-urns`; not run here). Lesson:
don't fix a Pulumi-managed machine by hand; change the code and `up`.
</details>

**B8. Your values, not the README's.** In the toolbox, run the README's four `deploy_single_vm`
config lines exactly as printed (README:352-355), then `pulumi config`. Predict the output, and what
`git status` on your laptop shows afterwards.

<details><summary>Answer</summary>

`gcp:project ac215-project`, `security:gcp_service_account_email deployment@ac215-project.iam.gserviceaccount.com`
and the README's own `sa_…` number (`laptop/b42`): the README's project and the README author's OS
Login user, which your deployment account cannot use. Run the three `config set` lines again with
your project ID, your `sa_…` username from `gcloud compute os-login ssh-keys add` (README:302-316)
and `deployment@<your project>.iam.gserviceaccount.com`. The same goes for `deploy_images`
(README:333). The values are written into `Pulumi.dev.yaml`, a committed file (`b33` shows it), in
the folder the toolbox mounts as `/app` (`docker-shell.sh:36`): `git status` on the laptop lists
`src/deployment/deploy_images/Pulumi.dev.yaml` and `src/deployment/deploy_single_vm/Pulumi.dev.yaml`
as modified (worked out from the mount; inside the toolbox `/app` is not a git repository, `b46`).
Commit them on your own branch or stash them before pulling course updates. They hold no secret
(the passphrase is empty, `Dockerfile:51`).
</details>

---

## Part C · Debugging

**C1. Two angle-bracket errors.** `docker login -u <USER NAME> -p <ACCESS TOKEN>` says
`bash: -c: line 1: syntax error near unexpected token 'newline'` (`laptop/a01`), and
`gcloud compute project-info add-metadata --project <YOUR GCP_PROJECT> --metadata enable-oslogin=TRUE`
says `bash: line 1: YOUR: No such file or directory` (`laptop/b08`). Same cause?

<details><summary>Answer</summary>

Yes. `<` and `>` are redirections to the shell: `<YOUR` asks it to read a file called `YOUR`, and
`<ACCESS TOKEN>` ends in a `>` with nothing after it. The placeholders are meant to be replaced
entirely, brackets included: `docker login -u yourname` (better: `echo "$TOKEN" | docker login -u
yourname --password-stdin`, which keeps the token out of your shell history) and `--project
your-project-id`.
</details>

**C2. `sh docker-shell.sh` fails, then runs anyway.** The build stops at `[ 2/16] RUN apt-get update &&
apt-get install -y curl …` with 22 `E: Failed to fetch …debian-security… 404 Not Found` errors, then the
script prints `Unable to find image 'cheese-app-deployment:latest' locally` and `pull access denied`
(`laptop/b02`). Why both, and what is the fix?

<details><summary>Answer</summary>

`src/deployment/Dockerfile:4` is `FROM python:3.13-slim-bullseye`, Debian 11. Its security updates
moved to `archive.debian.org` after its long-term support ended, so the index still on
`deb.debian.org` points at packages that are gone: 404 (ASSETS.md, breakage 1). The script then runs
`docker run` regardless, because `set -e` is commented out (`docker-shell.sh:4`): there is no image,
so Docker tries Docker Hub for `cheese-app-deployment:latest` and is refused. Read the **first**
error. Fix 1: `FROM python:3.13-slim-bookworm` (Debian 12, `laptop/b02a`), then run it again (C3).
</details>

**C3. After fix 1.** The build now passes steps 2–7 and stops at step 8:
`Package google-cloud-sdk is not available … However the following packages replace it:
google-cloud-cli` and `E: Package 'google-cloud-sdk' has no installation candidate` (`laptop/b02b`).

<details><summary>Answer</summary>

Google's apt repository no longer carries the old transitional package names (`Dockerfile:29-30`);
apt itself names the replacement. Fix 2: install `google-cloud-cli google-cloud-cli-gke-gcloud-auth-plugin`.
The two one-line edits together are the diff in `laptop/b02c`; with both, the toolbox builds
(`[+] Building 91.9s (21/21) FINISHED`, `laptop/b02d`). This one would also fail on bullseye once
the first problem was fixed another way.
</details>

**C4. Pulumi wants a browser.** In `deploy_images`, `pulumi stack init dev` prints `Connect to Pulumi
Cloud for state storage …` and `Press <ENTER> to log in with your browser` (`laptop/b14`), and
`pulumi config set …` says `error: PULUMI_ACCESS_TOKEN must be set for login during non-interactive
CLI sessions` (`laptop/b15`). What went wrong, and where do you look?

<details><summary>Answer</summary>

Pulumi isn't logged in to your state bucket, so it falls back to its own cloud service. The login
happens in the toolbox's entrypoint, scroll up to it: `docker-entrypoint.sh:10-23` activates
`/secrets/deployment.json`, creates the bucket if needed and runs `pulumi login gs://…`. In `b02d`
the first lamp is already red (`invalid_grant: Invalid grant: account not found`: the recording's key
belongs to no account), so the bucket and the login fail after it. Check `gcloud auth list` (yours
must list `deployment@<project>.iam.gserviceaccount.com` as active; `b06` says
`No credentialed accounts.`), the file name `secrets/deployment.json`, that `secrets/` sits next to the
clone (`docker-shell.sh:9`, three folders up from `src/deployment`), and `GCP_PROJECT` in
`docker-shell.sh:13`. Then leave and run `sh docker-shell.sh` again. Don't press Enter for Pulumi
Cloud, and don't use `pulumi login --local` (the video's recording workaround): your state belongs in
the bucket, where the other stack and your next session find it.
</details>

**C5. "The container name is already in use."** You run the README's interactive `api-service` command
(README:133-144) and get `docker: Error response from daemon: Conflict. The container name
"/api-service" is already in use …` (`vm/38`, exit 125).

<details><summary>Answer</summary>

The detached `api-service` from README:118-127 is still running, and container names are unique on a
Docker host. The interactive variant is an alternative, not an extra step: `sudo docker rm -f
api-service`, run the interactive one (`vm/40`: a shell `app@<id>:/app$`, because `DEV=1`), `exit`,
then start the detached one again (`vm/41`). nginx and the frontend find the API by this name, so the
detached one must be back before the site works.
</details>

**C6. nginx won't stay up.** After a VM reboot (or a `docker restart nginx`), `sudo docker container ls
-a` shows `nginx Exited (1)` or restarting, and its log says
`nginx: [emerg] host not found in upstream "api-service" in /etc/nginx/nginx.conf:37`.

<details><summary>Answer</summary>

nginx resolves every `proxy_pass` host when it loads its config and refuses to start if one doesn't
resolve; Docker's DNS only answers for containers that are running on that network. Here the API
container isn't (line 37 is the API's `proxy_pass`; `:48` would be the frontend). Reproduced with
stand-ins: the same message for each name ([`nginx.log`](assets/exercise-checks/logs/nginx.log),
"C6"). Find out why the API is down (`sudo docker container logs api-service`: at import it needs the
vector DB, `api/utils/llm_rag_utils.py:57`, and its key), start it, then start nginx. On the Pulumi VM
the frontend has no restart policy (`setup_containers.py:110-129`), so after a reboot it is the
frontend that is missing (D3).
</details>

**C7. The exported SSH command doesn't work.** `pulumi stack output ssh_command` gives
`ssh sa_…@<instance_ip>`, and running it says `Permission denied (publickey).`

<details><summary>Answer</summary>

The export leaves out the key (`deploy_single_vm/__main__.py:34`), and ssh only tries its default
keys (`~/.ssh/id_*`); the key in your OS Login profile is `secrets/ssh-key-deployment`. Add
`-i /secrets/ssh-key-deployment` in the toolbox (or the path to your `secrets/` folder on the
laptop). Reproduced against a test SSH server: without `-i`,
`student@127.0.0.1: Permission denied (publickey).` (exit 255); with it, `logged in`
([`pulumi.log`](assets/exercise-checks/logs/pulumi.log), "C7"). Or use the console's SSH button.
</details>

**C8. `unknown stack`.** `pulumi preview --stack dev --refresh` in `deploy_single_vm` fails with
`Preview failed: unknown stack "organization/deploy-images/dev"`.

<details><summary>Answer</summary>

The VM program reads the image tags from that stack (`setup_containers.py:27`), and it doesn't exist
in the backend you are logged in to: `deploy_images` has not been run (or not as stack `dev`, or you
are logged in somewhere else, C4). Run `pulumi stack init dev` and `pulumi up --stack dev --refresh -y`
in `deploy_images` first, and don't rename its project or stack. The stand-in, run in the wrong order,
gives exactly `error: Preview failed: unknown stack "organization/l20ex-images/dev"`
([`pulumi.log`](assets/exercise-checks/logs/pulumi.log), "C8"). (On the README's GCS backend the
message for this case was not captured.)
</details>

**C9. A safer key?** A classmate put a passphrase on `ssh-key-deployment` "for safety". The VM is
created, then the first provisioning step fails.

<details><summary>Answer</summary>

Pulumi connects with the key itself (`create_instance.py:8-14, 157-161`) and has no way to type a
passphrase. With an encrypted key the command provider stops at once: `error: ssh: this private key
is passphrase protected` (reproduced with a `remote.Command`,
[`pulumi.log`](assets/exercise-checks/logs/pulumi.log), "C9"). Make a new key with an empty
passphrase (press Enter twice at `ssh-keygen -f ssh-key-deployment`, README:296), upload its `.pub`
again (README:302) and `up`. The protection is the file's place and mode: `secrets/`, outside the
repo, `-rw-------` (`laptop/b11`), never committed.
</details>

**C10. `/status` says 404 on the part 1 VM.** `curl -s -i http://localhost:9000/status` on your manual
VM answers `HTTP/1.1 404 Not Found` (`vm/34`), though `api/service.py:34-36` in your clone has the
route.

<details><summary>Answer</summary>

Part 1 runs the public `dlops/cheese-app-api-service` image, not your clone: that image's
`api/service.py` has no `/status` and no `ROOT_PATH` mount (`vm/36`), so it is older than the code you
read. `/` (`{"message":"Welcome to AC215"}`, `vm/33`) and `/docs` (`vm/35`) are the checks that work
there. Build and push your own images (`docker-hub.sh` with your Docker Hub name) and use
`<you>/cheese-app-…` in the VM commands, and `/status` answers `{"version":"3.0"}`. Part 2 builds from
your clone, so the Pulumi VM has it.
</details>

**C11. The push is refused.** `pulumi up` in `deploy_images` builds the frontend (`npm ci`, `next
build`), then fails: `failed to fetch anonymous token: … 403 Forbidden` (`laptop/b35b`). Another
student gets `name unknown: Repository "cheese-app-repository" not found`. What does each mean?

<details><summary>Answer</summary>

`anonymous token … 403`: Docker had no credentials for `us-docker.pkg.dev`, so it asked anonymously
and was refused. In the recording the gcloud credential helper had no account (C4); for you, check
`gcloud auth list` and that the entrypoint ran `gcloud auth configure-docker us-docker.pkg.dev`
(`docker-entrypoint.sh:13`, `b02d`: `Adding credentials for: us-docker.pkg.dev`). `Repository … not
found` (the digest's gotcha 1, not reproduced here): the push is authorised, but nothing ever creates
`cheese-app-repository` (`deploy_images/__main__.py:14-15`; `artifactregistry` is imported on `:4` and
never used, and no README step creates it). Create it once in the toolbox: `gcloud artifacts
repositories create cheese-app-repository --repository-format=docker --location=us` (`us` matches the
host `us-docker.pkg.dev`).
</details>

**C12. The vector data isn't on the disk.** On the part 1 VM, `ls -la docker-volumes/chromadb` is empty
although the loader inserted 14,356 chunks (`vm/28`).

<details><summary>Answer</summary>

The README mounts the folder at `/chroma/chroma` (README:95), the data path of older Chroma images.
The server image today (Chroma 1.0.0 at the time of recording, `vm/24`) logs `persist_path: "/data"`
(`vm/25`), and `vm/28` shows `/data/chroma.sqlite3` (36 MB) inside the container and nothing in the
mounted folder. So the chunks live in the container's writable layer: they survive restarts, but not
`docker rm` (P1 in the video). Fix: `-v ./docker-volumes/chromadb:/data`, then the stop, rm and run
lines again and the loader. `setup_containers.py:150-155` has the same slip on the Pulumi VM
(`/mnt/disk-1/chromadb` → `/chroma/chroma`). It matters little here, because every deployment runs
the loader again.
</details>

---

## Part D · Think

**D1. One public door.** On the Pulumi VM, `vector-db` publishes 8000 and `api-service` 9000, and
neither is reachable from your laptop. Why is that enough, and what would go wrong if you added a
firewall rule for 8000 and 9000 "to make debugging easier"?

<details><summary>Answer</summary>

`-p` (or `ports=`) opens a door on the VM; the firewall decides which doors the internet can reach,
and `create_instance.py:51-89` opens only 80 and 443 (tagged VMs) and 22 (every VM); on your part 1
VM the console's two ticks did the same with tags. (Docker's port mappings do face the VM's network,
so the firewall is what keeps them private: not checked here against GCP, only read from the code.)
Opening 8000 would put the vector database, with no login at all, on the internet: anyone could read,
add or delete the collection. Opening 9000 bypasses nginx: the API would be reachable at a second
address, the frontend's calls would not change, and every route, including the paid Vertex AI
chats, could be called directly. Debug from inside instead: SSH and `curl localhost:9000/status`, or
an SSH tunnel (`ssh -i … -L 9000:localhost:9000 sa_…@<instance_ip>`).
</details>

**D2. A tag that only changes with the code.** Why does `deploy_images` rebuild on every run, and how
would you make a run with no code change a no-op? What do you lose?

<details><summary>Answer</summary>

The tag is the current second (`deploy_images/__main__.py:13`), so it differs on every run (B5).
Derive it from the code instead: the commit (`git rev-parse --short HEAD`) or a hash of the build
context, passed in as stack config (inside the toolbox `/app` is only `src/deployment`, without
`.git`, `laptop/b46`, so compute it on the laptop: `pulumi config set image_tag $(git rev-parse --short
HEAD)`). Then no change means the same tag, no plan, and no container replacement in the VM stack.
The stand-in with a fixed tag: `2 unchanged` ([`pulumi.log`](assets/exercise-checks/logs/pulumi.log),
"D2"). What you lose: a rebuild after a base-image update (same code, same tag) no longer reaches the
VM unless you also change the tag; the image's digest (`ref` export, `:34`) is the exact pin if you
need one. And uncommitted changes would ship under the last commit's tag.
</details>

**D3. Reboot.** You SSH into the Pulumi VM and run `sudo reboot`. A minute later, which URLs work?
Change one line of the code so that the answer is "all of them".

<details><summary>Answer</summary>

The disk comes back from `/etc/fstab` (`provision_instance.py:50-54`), Docker starts on boot
(`systemctl enable docker`, `:150`), and containers with `restart="always"` come back: `vector-db`
(`setup_containers.py:136`), `api-service` (`:212`) and `nginx` (`setup_webserver.py:75`). The
frontend has no restart policy (`setup_containers.py:110-129`), so it stays stopped, its name doesn't
resolve, and nginx refuses to start and keeps retrying: neither `/` nor `/api-service/status`
answers, though the API itself runs (`curl localhost:9000/status` on the VM works). That is the
video's opening puzzle again (B3, C6). Fix: add `restart="always"` to `deploy_frontend` and `up`; the
plan shows the frontend replaced or updated (Pulumi decides; check the plan). Worked out from the code
and B3's checks; no VM was rebooted here. (A guest reboot keeps the ephemeral IP; a stop and start
may not.)
</details>

**D4. Try the narrow key.** The video suggests running the VM as `gcp-service` instead of
`deployment`. What do you change, what will Pulumi do with a running VM, and does anything in this
repo need the VM to be `deployment`?

<details><summary>Answer</summary>

`pulumi config set security:gcp_service_account_email gcp-service@<your project>.iam.gserviceaccount.com`
in `deploy_single_vm` (README:355 sets `deployment@…`). Attaching it is allowed because
`deployment` has Service Account User (README:245). On a VM that already exists the plan is an
update of `cheese-app-demo`, and the Google provider refuses to change the service account of a
running VM unless the instance allows stopping for the update (`allow_stopping_for_update=True` in
`gcp.compute.Instance(...)`; per the provider's documentation, not checked here); then it stops,
changes and starts the VM, and the ephemeral IP may change, which ripples into every SSH connection.
Easier: set it before the first `up`, or `destroy` and `up` again.

As far as the code shows, nothing on the VM needs `deployment`: the image pulls use the toolbox's
credentials (`setup_containers.py:92-96`), the containers use `gcp-service.json` from `/srv/secrets`,
and the VM's own token is only limited by its scopes (`create_instance.py:137-144`). Not tested end to
end here. It is the lecture's rule (slides 25–26): the machine that runs the app holds only what
running needs.
</details>

**D5. When is `-y` dangerous?** `create_instance.py:100-103` looks up the newest Ubuntu 22.04 image on
every run, and the README always deploys with `up … -y`. What could a routine `up` do a month from now?

<details><summary>Answer</summary>

When Canonical publishes a newer image, the lookup returns a new `self_link`, the instance's boot
image input changes, and the boot image can't be changed in place: the plan would most likely show
`+-` **replace** for `cheese-app-demo` (inferred from the code and the provider's schema, as in the
digest's gotcha 20; not reproduced). A replaced VM means a new boot disk, a new ephemeral IP, the
provisioning and the containers again; the data disk survives as its own resource (and B4's guard
keeps it from being reformatted). With `-y`, nobody reads that plan. Run `pulumi preview --stack dev
--refresh` first and look for `+-` on the instance, or pin the image (a fixed image name instead of
`family=`) or tell Pulumi to ignore that field (`ignore_changes` in `ResourceOptions`).
</details>

**D6. One VM.** List three ways this deployment goes down that Cloud Run (L14) or Kubernetes (L22)
would survive, and one thing the single VM does better.

<details><summary>Answer</summary>

Down: the VM itself (a host failure, a reboot with the frontend's missing restart policy, D3, a
replacement, D5); a container crash that `restart` can't fix (nginx waiting for a name, C6); a traffic
spike, because one `n2d-standard-2` has fixed CPU and memory and nothing adds a second copy; and every
deploy replaces containers in place, so there is a short outage each time (B6). Cloud Run starts and
replaces instances for you and scales from zero; Kubernetes (L22, with this toolbox and the same images
stack) keeps several replicas behind a load balancer, restarts them, and rolls updates. The single VM
does better on simplicity and cost predictability: one machine, about two dollars a day plus disks and
the address, everything visible with `docker container ls`, and a persistent disk for state without
any extra service. That is why it is the right first step, and why the lecture ends on "single point
of failure".
</details>
