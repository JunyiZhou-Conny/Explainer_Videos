# AC215 · Lecture 4 — Containers II-b: build or pull, ports and Compose (follow-along: mega-pipeline flexible-workflow, port_toy)

## 00:00 — Build or pull? Whose localhost?
A command from this lecture's README, on a laptop that never built this image: with no local image, it pulls one from Docker Hub. Inside, Python says 3.8.17, and the Gemini library won't import.
Yet this repo's Dockerfile says Python 3.14. This image was built in February 2025, with Python 3.8. Where did it come from?
A second surprise, from the other tutorial: a server listening on port 9200. The laptop can't reach it; another container, asking by name, gets a reply: ok.
Two puzzles. Part 1: where did that image come from, and should you build or pull? Part 2: whose localhost is it?
The tracker shows the README step, code panels show file and line numbers. Pause at the yellow your-turn tag; gray extra tags mark commands the README doesn't have.
Every command is also in the study guide. Part 1 needs Tutorial 0 and a Google Cloud project with billing; part 2 needs only Docker.
We recorded on Linux, with Docker Engine 29.8.2 at the time of recording. On a Mac or in Git BASH, the prompt and a few messages differ; the commands and ports don't.
One honest limit: we had no Google account. Wherever the code calls Google, you'll see the command, the real error a missing key gives, and what to look for.

## 01:30 — Same pipeline, built like a team
In lecture 3, the course handed you a shared bucket and one shared key, copied into every component folder. This branch is the same pipeline, built the way a real team would build it.
Your team owns its bucket. You create your own service account, and keep its one key outside the repo.
You no longer write the Dockerfile: it's committed, together with pyproject.toml and uv.lock. And each component has one script, docker-shell.sh, that holds the long docker build and docker run commands.
The five stages haven't changed, and they still never call each other: each writes to the bucket, and the next reads from it. Containers that talk directly come in part 2.
A team can get an image two ways. Early in a project, everyone builds it from the recipe in Git. Later, one person publishes finished images to Docker Hub, and everyone else pulls.
Look closely at the tag. It's a signpost to one particular image, built on some day, from some version of the recipe. Nothing promises it matches the commit you have.
One script decides which of the two you get; we'll read it line by line. First, the code.

## 02:43 — Get the code: clone, or switch branches
Starting fresh? From your workspace folder, clone the repo with this branch checked out: git clone, dash dash branch flexible-workflow. Then cd into mega-pipeline. Pause and run both.
Two extra checks: git branch shows flexible-workflow at the pinned commit, and transcribe audio holds its Dockerfile, the script, pyproject.toml and uv.lock, which you wrote in lecture 3.
Already have your clone from lecture 3? It's on main; if you cloned fresh, skip to the next chapter. Step 1: cd into it. Two extra checks show its state.
Three piles. Your edited cli.py is tracked. Your two new files in generate text are untracked. In transcribe audio, the Dockerfile, pyproject.toml, uv.lock and the key are ignored.
Step 2, git fetch origin. Here it prints nothing: a clone already has every branch, and nothing had changed upstream. Yours may list updates.
Step 3, git checkout flexible-workflow, and Git refuses, for two reasons.
Your edits to cli.py would be overwritten, and two untracked files sit where the branch has files of its own. Nothing changed.
The README's note covers the first reason: git stash puts your edits away, and the first wall falls. On a retry, the untracked files still block it.
A small gap: the note covers only edited files. An extra git stash dash u stashes untracked files too, and the checkout works. The other option, git checkout dash dash dot, discards your edits and leaves untracked files alone.
Step 5, git branch: star, flexible-workflow. Pause and switch your own clone.
Extra checks show your ignored lecture 3 Dockerfile, pyproject.toml and uv.lock were replaced by the branch's, without a word: copy them out first if you want them.
The old key still sits inside transcribe audio; your secrets stay put, as the README says. Every build there copies it into the image, so delete each component's secrets folder now. Your edits wait in the stash.

## 04:59 — Your bucket and your three values
Before you run, the README's folder layout: your key lives in a secrets folder beside the repo, never inside it. Go up one level, to your workspace, and create that folder.
Step 2: every cli.py sets three values near the top: your project ID, your bucket, and your group name.
An extra grep shows what ships: three files are blank, but generate text and translate text already hold the course's project and bucket, and the instructor's group name.
A small slip: the README says an assert stops you if you forget, but it only rejects an empty value. Those two files would send your calls to the course's project and bucket, where they fail with permission errors.
Set all three, in all five files. An extra git diff shows our placeholders, your-project-id, your-team-bucket and group-01; type your own. In translate text, also change the target language from Spanish to French. Pause and edit them.
Step 3, your bucket: the components read and write these prefixes, and every output lands under your group's name.
Another small gap: the README never says how to create the bucket, and its sample upload is named test dot mp3. Create the bucket in the console.
Then upload a short recording into a folder named input audios, as input, dash, something, dot mp3. The transcript keeps that name, and upload only sends names starting with input.

## 06:36 — Three gates: account, role, API
Your bucket only lets in callers who prove who they are and have permission. For code, that identity is a service account, with one JSON key.
Google's libraries turn that key into a short-lived token, and every call to Google's API doors must pass three gates.
Gate 1 asks who you are: without the key, the call fails inside your container. Gate 2 asks what you may do: the account needs a role. Gate 3 asks if the API is switched on.
In the console, create a service account, for example mega-pipeline-sa. Grant it four roles: Storage Admin for every component, Agent Platform User for Gemini, Cloud Speech Client, and Cloud Translation API User.
Text-to-Speech needs no role. A small slip: the generate text README still says Vertex AI User, which finds nothing now.
Download a JSON key; it arrives with a long generated name. Rename it mega-pipeline.json, in the secrets folder beside the repo. Whoever holds it can spend your project's money: never commit or paste it.
Next, enable the APIs, in the console or with gcloud. Typed exactly as written, the set project command fails: the shell reads the placeholder's angle brackets as redirections. Type your own project ID, without brackets.
Then the gcloud services enable command switches on all five. Our laptop had no Google account, so gcloud says no active account: that's the login step from Tutorial 0. Logged in, it enables them, and calls bill your project.
Ponder this. Your key is in place and every API is enabled, but you forgot the Agent Platform User role. Where does generate text fail: inside your container, or at Google?
At Google, as a permission error. The key proved who you are; the role decides what you may do. New roles and APIs can take minutes to apply. Pause, and set up your account, key and APIs.

## 08:54 — docker-shell.sh: one script, two windows
Every component runs through its docker-shell.sh; let's read it once. Line 7 names the image, and the container too. Lines 8 and 9 build paths from pwd, the folder you're in.
So run it from the component folder. Line 10 is the key's path inside the container; line 13 names the Docker Hub account, dlops.
The case statement turns your first word into a mode. No word: build, then run. Dev only builds, run only runs, and prod builds for two processor types and pushes.
We'll use the default for all five, then come back to the other three.
Running opens two windows into your laptop. Dash v puts the component folder at slash app, and the secrets folder beside the repo at slash secrets. Dash e sets an environment variable: a signpost to the key for Google's libraries.
As in lecture 3, the venv lives outside slash app, so the window can't hide it. The key is never copied: slash secrets shows it only while the container runs.
Now cd into transcribe audio and run docker-shell.sh, no argument. Two steps take nearly all the time: build step 2, the system packages, and writing out the image; a first build also pulls the base image. Pause and run it.
The full log shows why uv sync is quick: the image's Python, 3.14.8 at the time of recording, already satisfies 3.14 or newer, so uv downloads none.
You're inside, as user app, in slash app; after the at sign comes the container ID, new every run. The first check, help, matches the README.
Three extra checks inside: python comes from the venv, the signpost points to slash secrets, and slash secrets is empty here. In a second terminal, opened in the same folder, an extra docker inspect lists both mounts.
Step 5, chmod plus x, is harmless: an extra ls shows it's already executable. Step 6, on Windows: use Git BASH, and put winpty in front if Docker says the input device is not a T-T-Y.

## 11:11 — Five components, five honest errors
Back in the container, the Quick Reference. The download step prints its arguments, then stops: default credentials error, file slash secrets slash mega-pipeline.json was not found.
That's gate 1, failing inside the container. Usual causes: no key in the secrets folder, another file name, or the script run from the wrong folder.
Both transcribe and upload stop the same way. With your key, look for the transcript, then a text file under text prompts, slash group-01, locally and in the bucket.
Speech-to-Text bills per audio minute, and this branch keeps only a long recording's first chunk: use a short clip. Pause and run it: the next component reads its output.
Next: exit, cd into generate text, and run the script. Without ffmpeg, its system layer differs: a fresh build, about 50 seconds. Help matches the README.
The download fails the same way. The generate step prints only its arguments and the word generate, then exits with status 0. Did it call Gemini?
No. The download had failed, so the loop had no prompts to work on. Exit status 0 doesn't prove it did anything.
The upload needs the key too. The generate text README adds one step: a variable picks the Gemini model. Gemini bills per token.
Next, synthesis audio E-N builds in 8 seconds, its system layer cached. We left its cli.py unedited on purpose: help stops at the assert; here, the guard works.
Edit it on the laptop: the window shows it at once. Now help fails at line 23, which builds the Google client on import: even help needs the key.
With your key, you'd see the README's help. There's no upload step: Text-to-Speech writes the audio straight into your bucket.
In translate text: an 8-second build, help failing at import, then download, translate and upload.
In synthesis audio, the same: download, then synthesis. Pause, and run all five with your key, checking the bucket after each.
Two small slips. The translation targeted Spanish, but the final voice is French: that's why you switched it. And the optional ElevenLabs bonus reads its key from inside slash app: point it at slash secrets.

## 13:51 — dev, run, and a stale image
Exit, and cd back into transcribe audio. Step 2 of How to Run, docker-shell.sh dev, only builds: no container starts. Here, all was cached; after any change in the folder, the copy and uv sync steps run again.
What is dev for? Adding a package: uv add, inside the container, updates pyproject.toml and uv.lock through the window; then dev bakes it into the image.
Step 3, run, skips the build: using local image, because one exists. Pause and try dev and run yourself.
A small inaccuracy: the README's overview says run pulls from the registry. In fact, any local image of that name wins, however old; otherwise it runs the Docker Hub image, pulled only the first time.
Ponder this. A teammate has never built this image, and types docker-shell.sh run. Which Python do they get?
This extra command deletes our local image, so we become that teammate.
Local image not found, so it pulls the dlops image from Docker Hub. Then, a surprise: creating a Pipfile. That's pipenv, this course's tool before uv.
The prompt says root. Python is 3.8.17, in an environment pipenv made. Help still works here, in the older wording of Python 3.8. Then type exit.
An extra inspect opens the box: created on February 18, 2025, with Python 3.8.17, starting pipenv shell, as root.
Its build matches an older branch, pipenv flexible workflow, not your recipe. Your folder slides over its slash app: your code, their environment. For generate text, that's the import error from the start: the first puzzle, solved.
It also left a Pipfile in your folder, owned by root. If you tried this, delete it and run dev to get your own image back.
So build locally, with no argument or dev, and use run only for images your team pushed from this branch, under your own Docker Hub account.

## 16:24 — prod, a stowaway key, and clean-up
Step 4, prod, publishes. It recreates a builder named multi-arch, a build engine for several processor types. Dash dash use makes it current, and the script never switches back: docker buildx use default does.
Then one buildx build makes amd64 and arm64 images and pushes both under one tag: as in lecture 2, an Apple-silicon Mac pulls one, a cloud VM the other.
Before prod, log in with an access token; dash p leaves it in your shell history. Set the Docker username in the script to your own. Don't run prod yet: first, check what it would publish.
Here's why. In the switched lecture 3 clone, the old key still sits in transcribe audio. Build there with dev, and an extra command lists the new image's slash app: the key is inside.
The copy line takes the whole folder. The gitignore keeps secrets out of Git, not out of images, and no branch has a dockerignore. Prod would push your key to Docker Hub.
So the README's promise holds for Git, not for images. Delete any secrets folder inside a component, add a dockerignore listing secrets, and if a key was ever pushed, delete that key. Pause and check yours.
Clean-up for part 1. Exit each container; dash dash r m deletes it. The transcribe image alone is 1.48 gigabytes: remove all five with docker image rm, plus any dlops images you pulled.
In the cloud, the bucket bills a little storage until you delete it, when the course is over; the key works until you delete it in the console. In part 2: containers that talk to each other directly.

## 18:14 — Two little computers, one network
In part 1, containers only left files in a bucket. Port toy makes two containers talk directly, and needs only Docker: a gateway serves a web page and forwards your text to a processor, which turns it into capitals.
Think of each container as its own little computer, with its own localhost and its own full set of ports. Two containers can both use port 9100 without any clash.
A network you create joins them like a small home network, with a phone book that turns container names into addresses. Docker's default network has none.
Prerequisites: docker run hello-world checks that Docker is running. It pulls a tiny image and prints hello from Docker.
Step 1 sets the app up by hand. From your workspace folder, clone the code: the README says clone or download but prints no command. Then cd into port toy. Pause and run them.
Two extra checks: the files match the README's tree, a gateway and a processor, and git log shows the commit this video pins.
Next, docker network create toynet. Docker prints the new network's ID: that's the rail both containers will plug into.
From the README's handy commands, docker network ls lists it, beside Docker's three built-in networks. Pause, and create yours.

## 19:37 — Build, start, read the logs
Next, build two images. The two Dockerfiles are almost identical: a slim Python 3.14 image, plus curl from apt. Each copies its code and runs it with dash u, so prints reach the logs at once.
The processor builds first, and its apt layer takes a few seconds. Your first build also pulls the Python base image.
Then the gateway: Docker reuses the processor's apt layer from the cache, because the two files match up to the copy line. It's done in under a second.
Then start the processor on toynet, with PORT set to 9200, and no dash p. It listens on 9200 inside its own box, but nothing on your laptop leads to it.
Then start the gateway. Dash p publishes a port: it opens a street door on your laptop that leads to a room inside the container. The order is IP address, host port, container port: 127.0.0.1, meaning this laptop only, then door 8090, then room 9100.
The two dash e flags tell the gateway where to call: the name processor, port 9200. Lines 13 and 14 of its code read them; the values in quotes there are only defaults.
Now check docker logs for each. The processor listens on 9200, internal only; the gateway listens on 9100. Pause and start both.

## 21:10 — Send a message: ports on the wire
To finish step 1, open localhost 8090 in your browser, type a message, and click Send. The reply comes back in capitals, with three port numbers: where the gateway sent from, where the processor listened, and where it saw the message arrive from.
We recorded without a browser, so curl sent the same request the page sends; this is the reply it got.
The processor listened on 9200, the destination. But every connection has two ends, so the gateway's side needs a port too. Its operating system picked a temporary one, 55620, and stapled it to the packet.
The processor saw the same number arrive, because nothing rewrites it inside the network. Line 38 of the gateway reads its own port; line 32 of the processor reads the sender's.
Send again, and the number changes: a new connection, a new temporary port. Yours will differ.
One more detail: the page's diagram shows 8090 by reading its own address bar. The container can't know which door on your laptop you gave it. Pause, send a message, and leave both running.

## 22:23 — Who can reach whom
Step 2 checks the ports. Docker ps shows the gateway's mapping, host side first: 127.0.0.1, port 8090, to 9100. The processor's PORTS column is empty: listening, but not published.
An extra docker ps with three columns matches the README's sample.
What does the 127.0.0.1 do? This extra run leaves it out, asking for door 8090 on every address. Docker refuses, port is already allocated: our gateway holds 8090. The container was still created, so remove it.
With door 8091 it works, and the mapping shows 0.0.0.0: every address, so other machines on your network could connect. Remove it. That's why the README writes 127.0.0.1: this laptop only.
From the laptop, curl on 8090 returns the gateway's page. Curl on 9200 can't connect: your laptop has no door to it, unless something else of yours uses 9200.
From inside the gateway, docker exec runs curl, asking for the name processor, on port 9200. The answer: ok.
Ponder this. The same command with localhost instead of processor. What answers?
Nothing. Inside the gateway, localhost is the gateway itself, and nothing there listens on 9200. That's the second puzzle: each container has its own localhost. An extra check: on 9100, its own port, localhost returns the page.
So how did the name work? From the handy commands, docker network inspect shows an address for each container, on toynet's own subnet.
Each container asks Docker's built-in phone book, at 127.0.0.11, which turns names into those addresses. Addresses can change when a container restarts; names stay.
Another handy command, docker exec dash i t gateway sh, opens a shell inside; its hostname is the container ID. One aside: the processor image has curl too, though the README implies it doesn't. Pause, and test from both sides.

## 24:58 — Change the ports
Step 3 changes the ports. First the street door: remove the gateway, and start it again on 127.0.0.1, port 8095. The room inside stays 9100.
The page works on 8095. Two extra checks: 8090 no longer connects, and docker ps shows the new mapping. Pause and move your gateway's door.
Why do this? Another app on your laptop might already hold 8090. Doors on the laptop must be unique; rooms inside containers never collide.
A small slip: the gateway's log still says open localhost 8090. That text is hard-coded in line 53. Trust docker ps and the page instead.
Next, the processor's port: remove it, and start it with PORT set to 9300. The README says: send a message, and it should fail.
It does, but quietly. The page has no error handling, so nothing on it changes; the captured request got only curl's error, empty reply from server.
An extra docker logs on the gateway shows why: it found the processor by name, but the connection was refused: nobody listens on 9200 anymore. A wrong name fails differently: see the exercises.
Ponder this. Which one setting fixes it, and does any image need rebuilding?
The gateway's processor port. Remove the gateway and start it with 9300, back on 8090, and the message goes through. No image was rebuilt: it's only configuration. Pause and fix yours.
The two settings must agree: the processor's PORT and the gateway's processor port.
Finally, clean up before Compose: remove both containers, then the network. An extra check shows only hello-world's old container left. Skip this, and Compose hits a name conflict. Pause and clean up.

## 27:07 — Compose: the same app, declared
Step 4: Docker Compose. The README shows an excerpt; open the whole docker-compose.yml. Almost every flag you typed by hand has a home in it.
Dash dash name becomes container name, and the build command becomes build. Dash p becomes ports, dash e becomes environment, and the network is named at the bottom of the file.
Two keys are new: the volumes key mounts the gateway's folder into slash app, and the depends on key starts the processor first. All of step 1 collapses into one command: docker compose up.
Run it. Compose builds both images, all from the cache, and names them after the folder and the service: port toy, dash gateway.
Then it creates the network and both containers, and prints both banners, each line prefixed with its service. Pause and run it.
Open the page: it works. In a second terminal, cd into port toy first: Compose reads the file in the current folder. There, docker compose ps shows the same mapping.
An extra network ls shows that Compose made toynet, and compose exec reaches the processor by name: ok.
The README's table pairs each by-hand command with its Compose version. In the first terminal, your requests now show in the log.
The README stops the app at the end of step 4; we stop it now, in the foreground: press Control C. Compose says it's stopping gracefully, but it takes about 20 seconds.
Python, each container's first process, ignores the polite stop signal unless it's written to catch it. So Docker waits 10 seconds per container, then kills it.
Exit code 137 means killed. Docker compose ps dash a: both containers exited, but they're still there.
Docker compose down removes the containers and the network, and nothing is left in ps dash a. Control C stops; down removes. Pause, and run the whole cycle.

## 29:20 — Edit, apply, tear down, recap
Back to the README's order: up dash d starts the app in the background and returns your prompt.
Two handy commands. Compose logs dash f follows the gateway's log; Control C stops only the following. Compose exec gateway sh opens a shell, where the environment shows processor and 9200.
Step 3: repeat the port experiments in the file. Change 8090 to 8095 and run up dash d: Compose recreates only the gateway.
The page answers on 8095; change it back and apply again.
Changed code that's copied into an image needs dash dash build. We added a comment to the processor's code: only the copy layer is new, and only the processor is recreated.
The gateway's folder is mounted, and it rereads its page on each load: edits show on the next reload, without a rebuild.
To finish, docker compose down; nothing is left in ps dash a. The images remain, sharing about 200 megabytes; remove them to free space. Port toy costs nothing. Pause and shut it down.
To test yourself. One: which files define a mega-pipeline image, and what does run use when there's no local image?
Two: which three gates must a call to your bucket pass, and where does each one fail? Three: how does a git-ignored key end up in an image, and what's the fix?
Four: dash p 127.0.0.1, 8095, 9100. Which number does the browser use, which does the gateway bind, and what does 127.0.0.1 restrict? Five: inside the gateway, what is localhost, and which name reaches the processor?
Next lecture, a command-line container calls a database container by name on a Compose network, with the same secrets mount: parts 1 and 2 together. Answers are in the exercises.
