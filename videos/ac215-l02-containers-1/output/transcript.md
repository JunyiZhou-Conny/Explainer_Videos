# AC215 · Lecture 2 — Containers I: one image, from laptop to VM (follow-along: simple-translate)

## 00:00 — One command on a fresh VM
Here's a fresh virtual machine in the cloud: no copy of our code, no virtual environment, no uv. It has only Docker, and we type one command. Just watch; you'll run it yourself at the end.
Docker downloads an image, in seven layers, and starts a shell inside it. There we run the app, and its default text, I love cheese, comes back in Italian.
One extra check, not in the README: which Python is this? It's 3.14.7. Yet the recipe for this image starts from Python 3.12. Hold that thought; we'll solve it twice today.
That's where today's tutorial, simple-translate, ends. Last lecture we climbed its first two rungs: a manual install on a VM, then uv. Today, the other two: package the app as a Docker image on your laptop, push it to Docker Hub, and run it on a VM.
To follow along, open the README beside this video. Three trackers, top left, show where we are: on the laptop, on Docker Hub, on the VM. When the yellow your-turn tag appears, pause and run the command; a gray extra tag marks a check that isn't in the README.
You need Docker Desktop running, a free Docker Hub account, and your Google Cloud project for the VM at the end. No service account or keys today.

## 01:22 — Image, layer, container, registry
First, four words for the whole lecture. In lecture 1, every new VM needed the same setup, on an operating system that had to cooperate. A Docker image packs it all into one thing you can copy: system files, Python, the packages and the code.
An image is a stack of read-only layers. Each layer holds the files that one build step added or changed. Beside it sits a small config card: settings like environment variables, and which program to start.
The recipe is a Dockerfile, read one instruction at a time. Instructions that change files, like RUN and COPY, add a layer. Others, like CMD, only write on the card.
Run an image and you get a container: the same layers, shared, plus a thin writable layer on top, and one main process. When that process ends, the container stops, and dash dash rm deletes it, writable layer and all. The image never changes.
Think of the image as a class, and each container as an instance. One small slip in the README: it says build the docker container. Building makes an image; running makes a container.
A registry, like Docker Hub, stores images by name, on shelves. A tag is a name that points at one image, such as latest.
And a container is not a small VM. A VM boots its own kernel, the core of the operating system. Containers are isolated processes that share one Linux kernel.
On a Mac or Windows laptop, Docker Desktop provides that kernel with a small, hidden Linux VM. On a cloud VM, Docker runs right on the VM's own Linux.
What a venv couldn't isolate in lecture 1, the system's files and libraries, is now inside the box.

## 03:13 — A clean slate, and the clone
Now the README section Developing App using Containers. Open a terminal on your laptop. On a Mac your prompt looks different; on Windows, use Git Bash.
First, docker container ls lists running containers. Here it shows only the header, so nothing is running. If yours can't connect to the Docker daemon, start Docker Desktop and try again. Pause and run it.
Next, stop any running container. There's nothing to stop here; if you have one, docker stop with its ID does it.
Then docker system prune. It lists what it will remove and asks; type y. Nothing to reclaim here; yours may delete the stopped hello-world container from Tutorial 0. Pause and run it.
Look at the third item: dangling images, the ones without a name. Despite the README's heading, named images survive. With dash a, prune would remove every unused image.
Then docker image ls lists your images. The list is empty here; yours may still show hello-world: it has a name, so it survived. Your columns may differ: this is Docker 29, at the time of recording.
Now the code. As the README notes, a clone on last lecture's VM doesn't help: Docker Desktop runs on your laptop. Clone it here, then cd into simple-translate. Pause and run both.
An extra check, not in the README: ls dash a. There's the solution, Dockerfile.txt, but no file called just Dockerfile, and no uv.lock.
Run the README's build command now, as an extra: failed to read dockerfile. The README wants you to write it, in five steps.

## 04:56 — Dockerfile step 1: FROM
Next, inside the simple-translate folder, create a file called Dockerfile: capital D, no extension. The README fills it in five steps, with a build and a run after each. Pause and create the file.
Dockerfile step 1 is one instruction: FROM python, 3.12, slim bookworm. That's the official Python image, on a slim Debian 12 called bookworm. Paste it in, save, and check with cat, an extra.
Now the build command. Dash t names the image simple-translate; dash f picks the recipe. And the final dot is the build context: this folder, which Docker sends to the builder. Step 3 shows why that matters.
Pause and run the build. Your terminal shows a compact view. Here you see the full log; to get it, add dash dash progress equals plain. On Docker Desktop, the builder is called desktop linux, not default.
Docker fetches the base image, four layers, under 50 megabytes compressed, and saves the result as simple-translate, tagged latest. Those four layers are the bottom of our stack.
What will it do when it starts? An extra docker image inspect reads the config card: no entrypoint, and the command python3, inherited from the base image. So we predict a Python prompt.
Now the run command: docker run, dash dash rm, dash t i, simple-translate. Dash dash rm cleans up afterwards; dash t i lets you type into it. Pause and run it. There's the Python prompt, 3.12.15 at the time of recording. Type exit with parentheses to leave.
One surprise: an extra git status says nothing to commit, though we just made a file. The gitignore file here lists Dockerfile on line 3, so git hides yours. To commit it anyway, use git add dash f.

## 06:52 — Step 2: ENTRYPOINT
Step 2 adds one line: ENTRYPOINT, slash bin slash bash. Put it under the FROM line, and save.
Pause and build again. The FROM step says CACHED: nothing is downloaded, and no layer is added. ENTRYPOINT only writes on the config card.
Think of ENTRYPOINT as the program to start, and CMD as its default arguments. The entrypoint is now bash, and the command slot still says python3. So will the container start bash, running python3?
This extra inspect says no: the entrypoint is bash, and the command is now null. Setting an entrypoint resets the command you inherited from the base image. So bash starts on its own.
Pause and run it: a bare prompt. Read it left to right. You're root, the administrator, inside the container. After the at sign comes the container's ID, which changes every run, so yours will differ.
And the slash means you start in the top folder of the image, because this image sets no working directory. Type exit to leave.

## 07:58 — Step 3: install uv, copy the code
Step 3 adds two instructions. RUN pip install uv uses the pip of the base image to install uv. And the COPY line copies this folder, dot, into the image's top folder, dot slash. Add both at the end, and save.
Here's why the final dot matters. Docker packs the whole folder into one parcel, the build context, and sends it to the builder. Every file goes in, the hidden git folder and your Dockerfile too; a file called dot dockerignore could leave some out, but this repo has none. The COPY line unpacks it all into the image's top folder.
Pause and build. The log confirms it: there's no dockerignore file, so nothing is filtered out, and the whole context, 63 kilobytes here, travels to the builder.
Then pip installs uv, version 0.13.0 at the time of recording, and COPY runs: two new layers. Pip also warns about running as root. In lecture 1 that warning mattered; here, the image itself is the isolation.
Something to ponder: uv is installed, and the code is in the image. Will python cli.py run?
No. Pause and run it, then look around with ls, an extra: our files sit right next to the system's own folders.
Then python cli.py, another extra: ModuleNotFoundError, no module named art. We installed the installer, not the packages. Type exit.

## 09:40 — Step 4: uv sync, and two Pythons
Step 4 adds RUN uv sync; add it at the end, and save. Like on last lecture's VM, it reads pyproject.toml and installs the packages into a venv.
Now predict. This image's Python is 3.12, and line 6 of pyproject.toml asks for 3.13 or newer. What will uv sync do during the build?
Pause and build. First, notice: the pip step says CACHED, but COPY says DONE: it ran again, although we only added a line. Keep that question for part 2.
Now the answer. As on the Debian 12 VM in lecture 1, uv downloads its own Python: CPython 3.15.0, at the time of recording. Then it creates a venv at slash dot venv, and installs 11 packages.
On the number line, the requirement covers 3.13 and newer. The base image's 3.12 falls outside, so uv downloads the newest stable Python it knows in the range, and the venv's python links to it.
Pause and run it, then try the same two extras. Now the listing shows dot venv, and a new uv.lock. But python cli.py fails exactly as before. Why?
Remember lecture 1: activation is just PATH. Nothing has activated the venv, so the word python first finds the Python in user local bin, from the base image. That's 3.12, and it has none of our packages.
Activating the venv would put its bin folder in front, and python would find 3.15.0. Two extra checks confirm it: the venv's own python reports 3.15.0, and after sourcing the activate script, python cli.py works. The prompt now shows app in parentheses. Type exit to get back to your laptop.
So this image carries two Pythons: 3.12 from the base, which only installed uv, and 3.15 for the app. That's half of the opening puzzle, and a small mismatch in the tutorial. In your own projects, start from a Python 3.13 image, or make requires-python match the image.

## 12:09 — Step 5: CMD, the solution, the build
Step 5 adds the last instruction, CMD. It holds dash c and one quoted command: source the activate script, then exec bash. Add it at the end, and save.
On the card, the entrypoint and the command join into one command line: bash, dash c, then that string. On its own, bash dash c runs the string and exits.
Here the string first sources the activate script, which puts the venv's bin folder first in PATH. Then exec bash swaps this bash for an interactive one that keeps the new PATH and gives you a prompt.
Pause and build. Again COPY and uv sync run, and Python downloads again, for one added line. Part 2 explains why.
Pause and run it. No app in parentheses this time; is the venv active? These extra checks say yes: which python points into dot venv, it's 3.15.0, and the virtual env variable is set. The fresh bash set its own prompt. Then type exit, back to your laptop.
The README then points to a solution, Dockerfile.txt. An extra diff shows what it adds; if yours prints less-than and greater-than signs, add dash u. First, three ENV lines: no questions from apt, a UTF-8 locale, and unbuffered logs.
Second, one bigger RUN: update and upgrade the Debian packages, clean up, upgrade pip, and install uv. And ENTRYPOINT moved to the end: the order of ENTRYPOINT and CMD doesn't matter.
The README only names the file. So here's the quickest way, an extra command: copy it over yours with cp. Pause and do that.
Now the README's Build Docker Image section: from the simple-translate folder, the same build. Pause and run it. This compact view is what you'll see: four steps, the apt and pip step the slowest.

## 14:06 — Run it, translate, exit
Now the README's Run Docker Container step: docker run, dash dash rm, dash t i, simple-translate. At the prompt, type the README's translation: Good morning, from English to Spanish. Pause and run both.
Good morning comes back in Spanish: the request went from the container, through your laptop's network, to Google. If yours ends in a runtime error, Google refused the request: try later; Docker is fine.
To leave, type exit, and you're back on your laptop. Pause and do it.
What did exit do? It ended the container's process, so the container stopped, and dash dash rm deleted it. An extra check, docker ps dash a, lists every container, even stopped ones. Nothing is left; the image is untouched.
In a second run, an extra check, echo dollar dollar, shows that bash is process number 1. The container lives as long as that process. Dash i connects your keyboard, and dash t gives it a terminal. Then type exit.
Now a puzzle. Remember, CMD only holds the default arguments. What if you put words right after the image name: docker run, simple-translate, python cli.py? What command line does the container run?
Words after the image name replace CMD, and only CMD. So the container runs bash, python cli.py. Bash takes python as a script name, and finds the Python program in user local bin. That's a binary, so bash refuses: cannot execute binary file, exit code 126.
To run it in one go, replace CMD with your own dash c string, as in this extra: activate, then translate to French.
A repo helper, docker-shell.sh, builds and runs in one go.
You've built and run your own image. In part 2: what's inside it, why it keeps rebuilding, and how to ship it to a VM.

## 16:19 — What's inside the image
Part 2 opens the image we built; this scene and the next are extras. First, docker image ls: 518 megabytes on disk, and 144 megabytes of content, at the time of recording. Content is the compressed layers that travel to a registry; disk adds the unpacked copy.
Then docker history lists the layers, newest first. Read it bottom-up, and it's the Dockerfile top-down: the apt and pip step at 97.5 megabytes, our code at 250 kilobytes, and uv sync at 125 megabytes. The ENV, ENTRYPOINT and CMD rows are zero bytes: config only.
Below them sit the base image's own rows: Debian bookworm at the bottom, the PATH that puts user local bin first, and Python 3.12.15.
To look yourself, start a container again; these are from our second run in part 1. There, python is 3.15.0, while the base Python is still 3.12.15. Most of that 125 megabyte layer is this second Python, in uv's own folder.
Now list the top folder. Beside the system folders sit the hidden git folder, the editor's VS Code folder, the README and your Dockerfile. The COPY line copied the whole build context, your git history included.
That's a gap in the tutorial: there's no dockerignore file. In your own projects, add one listing dot git, dot venv and your secrets folder. It matters most once the image is public, and that's soon.

## 18:05 — The layer cache
So why did COPY and uv sync rerun when we only added a line? Docker caches every build step. A step is reused when its parent step and its instruction are unchanged. For COPY, the checksum of the copied files must match too. The first step that changes runs again, and so does every step after it.
Rebuild with nothing changed, adding the extra flag for the full log. FROM reuses the base, and the three steps after it all say CACHED: nothing runs.
Now predict. You change one word in cli.py and rebuild. Which of the four steps run again?
Try it, as an extra: on line 49, change I love cheese to I love brie. The git diff shows the change; the build context now has a different checksum.
Rebuild. FROM and the apt and pip step are reused. But the checksum of the copied files changed, so COPY runs, and uv sync after it, Python download and all.
Now undo the edit with git checkout. Same files, so the cache comes back? No: COPY and uv sync run again. Git rewrote its own index file, inside the hidden git folder, and that folder is in the build context too.
That answers the question from part 1. Your Dockerfile sits in the build context too, so every edit to it changed that checksum. While you follow the README step by step, that's expected.
In your own projects, put the slow steps first: copy only the files uv sync needs, run it, then copy the rest. A dockerignore keeps the git folder, any local venv and the Dockerfile out. Now an edit to cli.py reruns only the last COPY.

## 20:00 — Tag and push
Now the README section Pushing Docker Image to Docker Hub. First, sign up and create an access token, with read and write access, not the default. Copy it right away: it's shown only once, and it works like a password. Pause and make yours.
Next, log in: docker login, dash u with your user name, dash p with your token. We have no account, so we couldn't run it.
So some steps use a stand-in, a small registry on our own machine: just watch those. Logging in to it warns that a password on the command line is insecure.
That's a small slip in the README: with dash p, your token stays in your shell history. Instead, type docker login, dash u, and your user name, then paste the token when it asks. Pause and log in.
Then tag the image: docker tag, simple-translate, then your user name, slash simple-translate-ac215. Pause and run it with your own name. An extra image ls shows two names, one ID: a second name, not a copy.
Read the long name in four parts: the registry, docker dot I-O, the default; your account; the repository; and the tag, latest. Names without an account, like our first, fall under library.
Then push: docker push, with the same name. Pause and run it. Yours should upload each layer and end with a digest line. Without an account, Docker Hub refused ours: push access denied. If you see it, log in, and check your token can write and the name starts with your user name.
On the stand-in, the push goes through, ending with a digest: a fingerprint of the whole image.
Push again: every layer already exists, and only missing layers travel. On Docker Hub, even the base layers may say mounted from library python: it already has them.
And remember: a new Docker Hub repository is public by default. Anyone can pull it, git folder and all.

## 22:04 — Platforms: arm64 vs amd64
One more check before the VM; this scene is all extras. Our machine is Intel or AMD, and the image says linux slash amd64. On an Apple Silicon Mac, you'd see arm64.
Why does that matter? Every program in an image, bash, Python, uv, is machine code for one kind of CPU: amd64 for Intel and AMD, arm64 for Apple Silicon. A container's programs run directly on the CPU, so unless an emulator steps in, the CPU must speak the image's language. Docker Desktop has one built in; a plain Linux VM doesn't.
A tag can point at a menu, one image per platform. This python tag lists five platforms: amd64, two kinds of arm, and two rarer ones. Docker pulls the row that matches your machine.
The instructor's image, dlops slash simple-translate, is no menu: one image, amd64 only.
Our stand-in push is a small menu: amd64, plus an attestation, a record of how the image was built.
Now ponder. You built on an M-series Mac and pushed. Your VM is an ordinary Intel or AMD machine. Will your image run there?
No. Here's the same failure the other way around, on our machine, which has no emulator: exec format error. Docker Desktop would just run it, emulated. A Mac-built image on a default VM fails like this, or with no matching manifest.
Two fixes, neither in the README. One: build for the VM's platform, with the flag dash dash platform equals linux slash amd64. It's the commented-out line 12 of docker-shell.sh. On a Mac, it runs emulated: slower, but it works. Then tag and push again, as before.
Two: docker-build-push.sh uses buildx, Docker's multi-platform builder, to build both and push one menu.
Put your user name on line 11, and simple-translate-ac215 on line 7, the README's name. Log in first, then run it with bash. Afterwards, switch back with docker buildx use default, or desktop linux on Docker Desktop.

## 24:39 — A VM with only Docker
The last README section: Running App on VM using Docker. First, create a VM, as in lecture 1. The README gives no settings. An ordinary E2 machine with Debian 12 or 13 will do; E2 machines are amd64. The meter starts: the VM bills by the second while it runs, its disk while it exists.
Next, SSH in. Pause now: create your VM, and wait until its SSH terminal is open.
Then install Docker: sudo apt install docker dot I-O. Pause and run it. In our stand-in, a fresh Debian with empty package lists, it fails: unable to locate package. If yours installed, skip ahead to the version check.
A small gap in the README: this section skips sudo apt-get update, used in lecture 1. Without it, the package lists may be empty, as here, or out of date, with Not Found errors. Run the update first, an extra, and pause after it.
Now the install works: 92 new packages, a 107 megabyte download, on Debian 12; 91 packages and 118 megabytes on Debian 13. Answer Y. Pause and run it.
Then sudo docker dash dash version. This is Debian's own Docker package: 20.10.24 on Debian 12, 26.1.5 on Debian 13, at the time of recording. Older than the laptop's, but plenty.
Here Docker runs right on the VM's Linux kernel; there's no hidden VM, unlike Docker Desktop on a Mac.
And why sudo? Without it, this extra docker ps is refused: permission denied on the Docker socket, the door to Docker's background service. Only root and the docker group may open it.

## 26:35 — One-command deploy
Then the deploy: sudo docker run, dash dash rm, dash t i, dlops slash simple-translate. Pause and run it. The image isn't on this VM yet, so Docker pulls it from Docker Hub, seven layers, then starts a container.
Now run the app with python cli.py and its defaults: I love cheese comes back in Italian. Pause and run it. No clone, no pip, no uv on this VM: just Docker and one image.
And the opening question: why 3.14.7, when the recipe says 3.12? The same reason as in our build. This image was built on September 16 with uv 0.12.15, and the newest stable Python that uv knew in the range was 3.14.7. Our build today got 3.15.0.
Same Dockerfile, a month apart, two Pythons. Nothing in the recipe is pinned: pip installs the latest uv, the Python range is open, and the repo has no uv.lock, so each build writes its own. An image freezes all that: ship the image, not the recipe.
Type exit. One more small mismatch: the README promises to pull the image you pushed, but this command runs the instructor's. Your image is your user name, slash simple-translate-ac215. Run it with the same command, once it's built for amd64.
Also, an extra check shows the published image lags the repo: its cli.py is the older one, without raise exception equals True. If Google refuses a request, that version quietly prints your input back. That's not a Docker problem.
And if the pull itself fails with too many requests: Docker Hub limits anonymous pulls per network address, which a classroom can hit. Wait a while, or log in first, with sudo docker login.

## 28:36 — Tear down, recap, and what's next
Before you go, clean up. An extra check, docker ps dash a, shows no containers left behind, thanks to dash dash rm.
Last README step: delete the VM, with its boot disk, then check that VM instances and Disks are both empty. Pause and do it now.
Two optional chores. Your Docker Hub repository stays public until you delete it or make it private. And to reclaim the space your images take on the laptop, run docker system prune dash a.
Lecture 1 gave us a VM with a venv inside. Today a container slid in between: the venv now lives in an image, at slash dot venv. You built it on your laptop, pushed it to a registry, and ran it on a VM with one command.
Five questions to test yourself. One: what's the difference between an image and a container, and what does dash dash rm delete? Two: what does our container run at startup, and what happens if you add python cli.py after the image name?
Three: the Dockerfile says Python 3.12, so why does python report 3.15, or 3.14? Four: you edit one line of cli.py; which steps rerun, and how would you reorder the Dockerfile? Five: name two ways to make a Mac-built image run on a default VM.
The answers are in the exercises, and every command is in the study guide. Next time, Containers 2: five containers working together, a working directory, a non-root user, and your laptop's folder mounted inside a container.
