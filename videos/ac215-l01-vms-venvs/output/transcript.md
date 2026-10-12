# AC215 · Lecture 1 — Virtual machines, virtual environments and uv (follow-along: simple-translate)

## 00:00 — Why won't pip install?
Here's a brand-new computer in the cloud. It's ours, and we have root, full administrator rights. We ask pip for two Python packages, and pip says no.
This command isn't from the README; it's the one most of us would type first. The error says the environment is externally managed, and suggests a virtual environment. By the end of this video, every line of it will make sense.
Today's lecture uses the word virtual twice. A virtual machine is a whole computer you rent and throw away. A virtual environment is a private set of Python packages for one project. And one will live inside the other.
The tutorial, simple-translate, runs one small app four ways, each removing a kind of fragility. Today we climb the first two rungs: a manual install on a cloud VM, then a fresh VM of the same kind, with uv. Docker comes next lecture.
To follow along, open the README beside this video. The tracker, top left, shows the README step. Code panels show the file and line numbers. When the yellow your-turn tag appears, pause and run the command on your own VM. A grey extra tag marks a command that isn't in the README; extras are safe, so run them too. Every command is also in the study guide, in the MLOps Learning repo.
Before you start, finish Tutorial 0, so you have a Google Cloud project with billing on. No service account or keys today; all you need is a browser.

## 01:34 — The app: cli.py
Before we install anything, let's see what we're installing. Open cli.py on GitHub; you'll clone it onto your VM soon. The first two imports, argparse and asyncio, come with Python. The next two, art and googletrans, don't. They have to come from somewhere. This whole lecture is about where they come from.
The main function prints a banner that says AC215 in ASCII art, then the parsed arguments, then the text to translate. If you pass a file with dash f, the text comes from that file instead.
At the bottom, argparse defines four options, and each one has a default: the text I love cheese, source language English, destination Italian. So running cli.py with no options translates I love cheese into Italian.
The last line starts an event loop and runs main, because googletrans version 4 is asynchronous. Inside main, a Translator sends your text off with one awaited call.
That call is a single HTTPS request from the VM to translate dot googleapis dot com. It's Google's unofficial translate endpoint: free, no API key, no promises. A little JSON comes back, and line 39 prints the translation.
One detail on line 25 matters later: raise exception equals True. Without it, when Google answers with an error, googletrans hides it and hands your own input back as the translation, so nothing looks wrong. With it, a failure becomes an error you can read.
Lines 32 to 37 catch any error from that call and wrap it in a friendlier message about the network. Remember these lines. In a few minutes, they'll fool us.
So the app is small: arguments in, one web request, one line out. What it needs is two third-party packages. Let's get a computer, and find them a home.

## 03:34 — Renting a computer: the VM
A virtual machine is a slice of a real server in one of Google's data centers. Software called a hypervisor carves the machine into slices. Each slice gets virtual CPUs and memory from that server, a disk from Google's storage network, and its own operating system. One of them will be yours.
In the console, check that your Tutorial 0 project is selected, then open Compute Engine, then VM instances. The first time, it may ask you to enable the Compute Engine API; click enable and give it a minute. Then click Create instance.
The README gives no settings, so here are sensible ones. A name, like ac215-l01. A region and zone: where the machine physically lives. A machine type, which sets the CPUs and memory; e2-small is plenty. And a boot disk with Debian 12. Debian 13 works too; we'll see where it changes things.
Keep the external IP address; it's on by default. Without it, and without extra network setup, this VM can't reach the internet, and every download here would hang.
And now the meter starts. CPU and memory are billed by the second while the VM runs, even when it sits idle. The disk is billed for as long as it exists. The estimate is small, but the meter never stops on its own.
Click Create, wait for the green check, then click SSH. If it asks you to authorize the connection, click Authorize. A terminal opens in your browser, logged in to your new VM. Our prompt says student; yours shows your own username. Pause here, and get your VM to this point.
Three quick extra checks, not in the README. First, which operating system did we get? Print the os-release file: Debian 12, nicknamed bookworm.
Second, ask python3 for its version. Debian 12 ships Python 3.11.2, for the operating system itself. On Debian 13, you'd see 3.13.5. Keep both numbers in mind.
Third, which python, without the 3. The which command asks which program a name would run. For python, nothing comes back: Debian has python3, but no python. Remember this for part 2.

## 05:57 — apt, git and the repo
Step 3: type sudo apt-get update. Debian's package manager is apt, and sudo runs it as the administrator. Update downloads the package catalog: the list of packages that exist, and their latest versions. Nothing is installed yet. On a Google VM, you'll see a few more lines, for Google's own package sources. Pause and run it.
The README has a tip here: apt-get and apt do the same job. The apt-get command is the stable, scriptable one, for Dockerfiles and automated builds. The shorter apt is friendlier for typing by hand. Either is fine here.
Step 4: sudo apt install git. This time apt really installs things. It lists what it will add and asks, do you want to continue? Type Y and press enter. The list depends on your VM; if git is already there, apt says so. Pause and run it.
Step 5: clone the repo. Type git clone, then the address; copy it from the README. Git copies the whole repo, with its history, into a new folder, simple-translate, in your home directory.
Step 6: cd simple-translate. Watch the prompt: after the colon, it now shows the folder you're in. The wavy tilde means your home folder. Pause, and catch up to here.
One extra check: ls lists the files. There's cli.py, the README, a Dockerfile saved as a text file, two scripts for next lecture, and pyproject.toml, the list of what the app needs. Notice what's missing: no requirements file, and no lock file with exact versions. Hold on to that.

## 07:39 — The system Python and PEP 668
Step 7: sudo apt install python3-pip. That's Debian's own packaged copy of pip, for Debian's Python. Answer Y again. Ours pulled in over a hundred packages; a real VM usually needs fewer. Pause and run it.
An extra check: ask pip3 for its version. It's pip 23.0.1, for Python 3.11, in a folder called dist-packages under user lib. That user is spelled U-S-R: the system's files, not your home folder.
Now the command from the start of the video, without sudo or any flag; it isn't in the README either. Again, pip refuses: this environment is externally managed. The hint says: install with apt, or create a virtual environment. Its last note even names a way around it.
Why refuse? Picture how Python finds an import. This extra one-liner prints the list called sys dot path: the folders Python searches. Think of them as shelves. On every import, Python scans from the top shelf down, and takes the first match.
The bottom shelf belongs to apt. Debian itself runs Python tools that depend on exactly those jars, at exactly those versions. The system Python is a shared kitchen, and apt is the cook. That's what externally managed means. PEP 668 is the rule that makes pip respect it.
Step 8 is the README's command: sudo pip3 install, with the flag break-system-packages. The flag overrides the guard; sudo lets pip write as administrator. Pause and run it. We asked for 2 packages and got 12; if yours says requirement already satisfied, apt already had that one. And the warning says running pip as root can clash with the system's package manager.
Where did they go? This extra one-liner asks googletrans where it lives: in dist-packages under user local, still the system's, shared by every user. Look at the shelves: that shelf sits above the one apt owns.
Now suppose apt had installed an older httpx for some system tool. Our googletrans needs 0.27.2 or newer, so pip would add a second copy, on the higher shelf. Python would find that copy first and hide the one from apt, for every program that uses the system Python, not just ours. That's what the flag breaks.
To be fair, the README says it uses the flag deliberately, as a quick demonstration, and the next walkthrough does it properly.
Something to ponder. A classmate's project on this VM needs httpx 0.13, and yours needs httpx 0.28. Both install system-wide, like this. What happens?
There's only one shelf, so there's room for only one httpx. The last install wins, for everyone, and one of the two projects breaks.

## 10:53 — Run it, and read the traceback
Step 9: run it. Type python3 cli.py, with the 3, since plain python doesn't exist here. You should see the banner, the arguments, your input, and the output: I love cheese, in Italian. If you get a long red error instead, don't change anything; we'll read ours together in a minute. Pause and try it.
Then the README's other two runs. Dash t gives the text, dash s the source language, dash d the destination. Copy them from the README, quotes included, and pause to run both. One comes back in Spanish, the other in French.
Now, honestly: when we recorded this, Google refused our requests, and the run ended in this long red traceback. Let's read it; you'll meet tracebacks like this all course long.
This is a chained traceback: two errors. The line between them says the first one directly caused the second. Most people read only the last line, but here that's just the wrapper. Scroll up to the first error: that's the cause.
The cause is status code 429: too many requests. Google's unofficial endpoint was rate-limiting our machine, as it often does with cloud machines. Nothing on the VM was broken.
The error on the last line is the app's own wrapper, lines 32 to 37 of cli.py. It catches anything, and raises a friendlier message, chained to the original.
Why read the first error? This extra command has a typo: x x isn't a language. The first error says invalid destination language. But the last line still blames the network, because the same wrapper catches everything. A small flaw in the code, not in your setup. The valid codes are in a table at the bottom of the README.
If you hit a 429, wait and retry, try another region, or run it on your laptop. If you got as far as the Input line, the imports worked; when the first error is a 429, only the network said no.

## 12:58 — Delete, don't stop
Step 10, the last one: delete the VM. As the README says, a running VM keeps charging, even when idle. So why delete it, and not just stop it?
Stopping ends the billing for CPU and memory, but the disk still exists, so it keeps billing, and so would a reserved IP address.
Deleting removes the VM, and by default its boot disk goes with it. That's a setting on the boot disk, and it's on unless you changed it. And the meter stops. Select your instance, click Delete, and pause until it's gone.
Then check two pages: VM instances and Disks should both be empty. With the gcloud tool on your laptop, two extra commands do the same: gcloud compute instances list, and gcloud compute disks list. Neither is in the README.
That was the quick and dirty way. It worked, but it changed the system Python for every program on the machine. In part 2: the same app, on a fresh VM, the clean way.

## 14:01 — What a virtual environment is
Back to our puzzle: two projects, two versions of httpx, one shared shelf. The fix is to give each project its own toolbox. That toolbox is a virtual environment.
A virtual environment is just a folder, usually called dot venv, with three parts. First, a bin folder with a python inside. It's usually not a copy, just a link to a real interpreter somewhere else.
Second, its own site-packages folder, empty when uv makes it. Site-packages is the usual name; Debian calls its system ones dist-packages. This is where this project's packages go, and only this project's.
Third, a small config file, pyvenv.cfg. When Python starts from the venv's bin folder, it reads this file. It says: you're in a venv, so use my site-packages, and leave the system's out.
Here's the difference on the shelves. Started from the venv, Python builds a different list. The standard library still comes from the real interpreter it links to. But both dist-packages shelves from the system are gone, and the venv's own shelf takes their place.
Same engine, different toolbox. And the toolboxes don't mix: packages in the venv are invisible to the system Python, and the other way round.
Remember pip's hint? It suggested python3 dash m venv, the classic way to make one. Today, uv makes it for us, and does a lot more.
What a venv doesn't isolate: the operating system, system libraries written in C, and drivers. Those are jobs for a whole machine, like our VM, or a container, next lecture.
After uv sync, we'll open the real folder and find all three parts.

## 15:48 — Installing uv
Part 2 starts on a fresh VM, same settings, and the meter runs again. Fresh matters: this system Python never sees pip. Create it and SSH in; if the name is taken, the old VM is still being deleted, so wait a minute. Pause until your terminal is open.
Then the same four commands: apt-get update, install git, clone, and cd. Pause until your prompt ends in simple-translate.
Step 7 installs uv in one line. First, curl downloads a script: it follows redirects, stays quiet but shows errors, and fails on an HTTP error instead of handing an error page to the shell.
The vertical bar is a pipe: it hands the script straight to the shell, so you're running code from the internet: uv's official installer, which you can read first.
Pause and run it. It installs uv, version 0.13.0 at the time of recording, and uvx, into dot local slash bin in your home folder.
Let's try uv, with an extra check. Command not found. But we just installed it.
When you type a command, the shell walks a list of folders called PATH, left to right, and runs the first match. None contains uv, and the shell only knows the PATH it started with.
The installer's last lines, and step 8, give two options: reload your shell, or source the env file. A reload means a new SSH window, back in your home folder, so you'd cd into simple-translate again. Sourcing is quicker: it puts that folder first in PATH. Pause and run the source line.
Then two extra checks: uv reports its version, and which uv points into that folder.
Why source, and not sh? Plain sh would change a child shell that exits at once; source changes this one. The installer also made your startup files run this env file, so next time you connect, uv is found by itself.
So what is uv? One fast tool that replaces several: the venv module, pip, pip-tools for locking, pyenv for installing Pythons, and pipx.

## 18:03 — uv sync: which Python?
Step 9 is uv sync, and it reads pyproject.toml, so let's read it first. The name is app. Two dependencies: art, version 6.5 or newer, and googletrans, exactly 4.0.2. Greater-or-equal means a range; double equals, one version. Line 6 is a range again: Python 3.13 or newer.
Now predict. This VM has Python 3.11. The project asks for 3.13 or newer. What will uv sync do? Fail, use 3.11 anyway, or something else?
Pause and run uv sync. Instead of failing, uv downloads its own Python: CPython 3.15.0, at the time of recording. Then it creates a virtual environment in dot venv. If uv can't find a pyproject.toml, cd into simple-translate first.
Here's what happened. Picture Python versions on a number line. The constraint lights up everything from 3.13 onward. First, uv looks for an interpreter it already has: its own downloads, then the system's. Debian's 3.11.2 lands outside the range, so it can't be used.
So uv downloads one. Which one? Not 3.13, but the newest release in the range, which was 3.15.0 when we recorded. It lives in uv's own folder in your home, and the venv's python links to it.
That's the catch: a constraint is not a pin. Before Python 3.15 came out, this same command gave people 3.14. Watch this video next year, and you may get something newer still.
On Debian 13, the story changes. Its system Python, 3.13.5, is already inside the range. So uv simply uses it, with no download, and the venv's python links to the system one. Same command, different Debian, different Python.
To get the same Python everywhere, pin it. The command uv python pin 3.13, not in the README, writes a small file called dot python version, and the range shrinks to the 3.13 series. Don't run it now: your next uv sync would rebuild the venv, and the rest of the video wouldn't match. It's in the exercises.

## 20:37 — uv sync: resolve, lock, install
Now the packages. A quick puzzle: pyproject.toml lists 2 dependencies, and in part 1, pip installed 12 packages for them. How many will uv install?
It's 11: one fewer than part 1. It resolved 13 and installed 11, each with a plus sign and an exact version. So where did the other 9 come from, and which one went missing?
Packages have dependencies of their own; this extra command, uv tree, draws them. Our googletrans needs httpx, an HTTP library, which needs anyio, certifi, httpcore, h2, and more. Two wishes grow into a tree.
Resolving means choosing one exact version for every package in the tree, versions that all fit together. Then uv writes them to a new file, uv.lock, with download addresses and checksums. The pyproject.toml file is your wish list. The uv.lock file is the receipt.
So why 13 resolved? It's 11 packages, plus the app itself, which uv doesn't download. The 13th is in uv.lock, which covers every Python the project allows, not just ours. In it, anyio needs typing extensions, but only on Python older than 3.15.
On our 3.15, it's skipped, so 11. Part 1 ran on Python 3.11, so pip installed it: 12. And on Debian 13, with Python 3.13, uv installs 12 too.
Here's why the receipt matters. Two students run uv sync a week apart. Without a shared lock, each resolves fresh and may get different versions deep in the tree. With the same uv.lock, they get exactly the same packages.
Two extra checks. First, ls dash a shows two new things: the dot venv folder, and uv.lock. And git status says uv.lock is untracked. It was made here; it didn't come with the repo.
Now, a small mistake in the README, with an easy fix. It says uv.lock gives the next person the same versions. But the repo never committed one, so each student's first sync resolves fresh. In your own projects, commit uv.lock. In automated builds, run uv sync with the locked flag, which refuses a missing or stale lock.
Last, an extra: run uv sync again. It checks the same packages, 11 here, in a fraction of a millisecond, and changes nothing: safe to re-run anytime.

## 23:23 — Activation is just PATH
Let's open the venv, as promised. This extra command lists its bin folder: python, a link to the Python uv downloaded, and, notice, no pip.
And the config file: home is the real interpreter's folder, include system site packages is false, and the prompt is app. All three parts, as drawn.
Step 10: source dot venv slash bin slash activate. Pause and run it. Your prompt now starts with app, in parentheses. The README's example says simple-translate. But uv names the prompt after the project, and pyproject.toml calls it app.
What changed? Before activating, python knocked on every door in PATH and found nothing. The activate script saves your old PATH, then puts the bin folder of the venv first, so python is found at the first door.
Extra checks: which python points into dot venv, and python reports 3.15.0, at the time of recording; on Debian 13, 3.13.5. And which pip finds nothing.
Another small mistake in the README: it says activation points pip into the venv, but a uv venv has no pip. On a machine with a system pip, which pip finds that one instead, and it refuses, as at the start. To add a package, use uv add, which also records it in pyproject.toml and uv.lock.
Activation also sets a variable called virtual env, changes the prompt, and adds a command called deactivate that undoes it all. It only changes where the shell looks first, and only in this shell. If your SSH window reconnects, cd into simple-translate and activate again.
Step 11: the same three runs, now with plain python. Copy the long ones from the README, quotes included, and pause to run all three. This time Google answered: these are real translations. If you get a 429 again but see the Input line, your venv works.
Two extras, not in the README, that skip activation. First, uv run python cli.py syncs the venv if needed, then runs the app inside it. Or call the venv's python by its path.
And why source, not just run the activate script? It isn't even executable, and run as a program, it would only change a child shell that exits at once, like the env file.

## 25:55 — Prove the isolation
Let's prove the isolation with a few extras. Deactivate first: while the venv is active, even python3 points into it. Then ask the system's python3 to import googletrans. ModuleNotFoundError. On this VM, the packages exist only in the venv.
On the shelves: the system Python scans its own list, top to bottom. The venv's shelf isn't on that list, so the search comes up empty.
Now the same import through uv run, printing where this Python thinks it lives. It works, and the answer is our dot venv folder.
Now imagine you'd kept your part-1 VM. Same import, system python3, no venv. Does it work?
Yes: on that VM, sudo pip put googletrans on the system-wide user local shelf, so every program finds it. Same import, different shelves, different answer.
And it works the other way too. Even on that messy part-1 VM, a venv would ignore everything sudo pip put there, because those shelves aren't on its list. That's the whole lesson in one picture.

## 27:10 — The older way: pipenv
One more tool you'll meet: pipenv, an older way to do the same job. This repo's pipenv branch, an older version of this tutorial, uses it. So do the separate AWS version and, later, the cheese app's API service.
Same ideas, different names. The pyproject.toml file becomes the Pipfile, and uv.lock becomes Pipfile.lock. The venv lives in a folder in your home instead of in the project. The command uv sync becomes pipenv install, or pipenv sync. And instead of activating, pipenv shell opens a new shell inside the venv. Type exit to leave it.
And here's our puzzle again, for real. That branch's lock file pins httpx 0.13.3, while our uv sync installed 0.28.1, at the time of recording. Two versions of the same app, two versions of httpx. On one shared system Python, they couldn't live together. In two venvs, they can.

## 28:16 — Tear down, recap, and what's next
Step 12: delete the VM, with its boot disk, then check that VM instances and Disks are both empty. Pause and do it now, before you forget.
Here's where we are. The VM gave us a whole machine that we can wreck and delete. The venv keeps one project's packages away from that machine's Python. And between the two, there's room for one more layer.
That layer is a container, and it's next lecture. The tutorial's Dockerfile already shows the idea: copy the code, run the same uv sync, and start in a shell with the venv activated. Everything you did today, baked into an image.
One thing to watch for next time. The Dockerfile starts from a Python 3.12 image, but the project wants 3.13 or newer. You already know what uv will do about that.
Before you go, five questions to test yourself. One: what does the break-system-packages flag actually break, and where did sudo pip3 put the files?
Two: name the three parts of a virtual environment. Three: what exactly does activation change, and what are two ways to run the app without it?
Four: 2 dependencies became 11 packages. Why, and which file makes everyone get the same ones? Five: is requires Python 3.13 or newer a pin, and what would make the version deterministic?
The answers are in the exercises. Every command from today is in the study guide, in the MLOps Learning repo. Next time: containers.
