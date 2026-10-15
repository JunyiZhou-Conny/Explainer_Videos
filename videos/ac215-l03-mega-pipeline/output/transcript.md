# AC215 · Lecture 3 — Containers II: five containers, one bucket (follow-along: mega-pipeline)

## 00:00 — Five containers, one bucket
A voice recording goes in on the left. Five programs, each in its own container, turn it into a podcast in English and in French, without ever sending each other a message. So how do they cooperate, and who pays?
Since last lecture, four things change: you write the Dockerfile, and you build five images, not one. A bind mount opens a window into your laptop, and the containers reach Google Cloud through a shared bucket and a service account key.
Open the mega-pipeline README beside this video. The tracker, top left, shows the README step; code panels show file and line numbers. Pause at the yellow your-turn tag; a gray extra tag marks a command not in the README.
You'll need Tutorial 0, for Docker Desktop and uv, the course key from Canvas, and your group name. Every command is also in the study guide, in the MLOps Learning repo.
One honest limit: we recorded without a course key, so wherever the code talks to Google, you'll see the command and what to look for, not its output.
We recorded on a Debian 12 laptop with Docker Engine 29, at the time of recording. On a Mac or Windows, the prompt differs and Docker Desktop runs the containers; the commands are the same.

## 01:19 — The bucket is the message bus
In production, services call each other's APIs. This tutorial simplifies: each component writes its output to shared storage, where the next one reads it.
That storage is one Google Cloud Storage bucket, drawn as a cabinet of drawers. The first stage, A, turns recordings from input audios into transcripts in text prompts. Then B turns each transcript into a longer podcast script, in text paragraphs.
From there the path splits. C turns the script into English speech, stored in the drawer named text audios. D translates it into French, in text translated, and E speaks the French, in output audios.
Nothing triggers anything: you run each component yourself, in this order.
A bucket has no real folders: a name like text prompts, slash, group-01, slash, input dash something dot t x t is one single object name.
Here's A's upload code: prefix, group name, file name, and only files starting with input. B downloads with the same pattern: that naming contract is the whole wiring.
The group name keeps teams apart, and its default has no guard: a component you forgot to edit writes into the default group's drawer, maybe over someone else's work. Set it before every run.
Each stage that succeeds lights up your row on a live leaderboard. Every call and every byte is billed to the course's project, not yours.
Which two stages could run at the same time, and which one has to wait?
C and D both read only B's text paragraphs, so they could run side by side. E reads what D writes, so it waits for D.

## 03:12 — Clone: five folders, no Dockerfile
The README's first command: clone the repo. Type git clone and the address, copied from the README, and pause to run it.
Then cd mega-pipeline. An extra check, not in the README, lists the files and shows the commit: five component folders, on the main branch, at the commit this video uses.
Another extra lists all five folders. Each has a README, its own cli.py, and a secrets folder, and not one has a Dockerfile: the README says you write all five yourself.
Two differences to remember. The generate text folder already has its own pyproject.toml and a main dot py file, but no dot gitignore file. And synthesis audio has a bonus script.
Now the first component. The tracker switches to the transcribe audio README, whose step 1 is cd transcribe audio. Pause, and catch up to here.
Open cli.py in your editor. The first imports come with Python, but the two Google Cloud modules and ffmpeg don't. Part 2 shows where they come from.
Next come four settings: the bucket's name, the two drawers this stage uses, and on line 21 the group name, which you'll change soon.
At the bottom, main runs up to three verbs, always in this order: download, transcribe, upload.

## 04:35 — The key, and uv init
Step 2 is the key: a file from Canvas called mega-pipeline dot json. It lets your code act as the course's service account, a robot Google account, so guard it like a credit card.
Pause, download it, and put it in this folder's secrets folder, with a copy in each of the other four.
The name must be exact. If your browser saved it with a 1 in parentheses, rename it.
A small mistake: the component READMEs link to an older Canvas file, so use the main README's link.
Step 3 uses uv. After Tutorial 0, uv dash dash version prints a version, so skip ahead to uv init. This recording laptop had no uv: command not found.
Otherwise, use the README's installer: on macOS or Linux, this curl line, which installed uv 0.13.0 at the time of recording. On Windows, the PowerShell line; on any system, pip install uv.
Then restart your terminal, as the installer says, cd back into transcribe audio, and uv answers.
Now the step itself: uv init dash dash bare. It writes just one file, pyproject.toml, for a project named transcribe dash audio. Pause and run it.
An extra look inside: a name, a version, an empty list of dependencies, and the minimum Python version, 3.11.
That 3.11 comes from this laptop's Python, 3.11.2. In the image, uv sync needs a Python in this range, and 3.12 is in it, so all is well.
Your number depends on your laptop. If yours says 3.13 or newer, the image's 3.12 falls outside, so edit it to 3.12. That fix isn't in the README; generate text shows why.

## 06:31 — Write the Dockerfile, line by line
Step 4 is the heart of this lecture: there's no Dockerfile here, so you write it yourself, piece by piece.
Line 1 starts from the official Python 3.12 image on Debian 12. The README names it in its text, not in a code block.
Line 3 declares a build argument, a variable that exists only during the build: the Debian packages build essential and ffmpeg. The Python package ffmpeg dash python just runs the ffmpeg program.
Lines 5 to 10 set six environment variables. As in lecture 2, they only write on the config card: no layers. The first four: apt never asks questions, text is Unicode, Python prints at once, and uv copies files instead of linking them.
Line 9 matters most: it tells uv to build the venv in slash home, slash app, slash dot venv, outside slash app. Soon, this line saves us.
Line 10 tells Google's libraries where the key is: secrets, slash, mega-pipeline dot json, a relative path.
Lines 12 to 21 are one RUN instruction, chained with double ampersands, so they make one layer. It updates Debian, installs our packages, and deletes apt's package lists in that same layer, so they cost nothing.
Then it upgrades pip and installs uv with it. Unlike Debian's system Python in lecture 1, this Python belongs to the image, so pip may install into it.
Last, it creates a user called app, user ID 1000, who owns slash app: as the README says, running as root is a security risk.
Lines 23 and 24 switch to that user and make slash app the working folder. Line 26 copies everything in this folder into the image; hold on to that word, everything.
Line 27 runs uv sync to build the venv from pyproject.toml, and lines 29 and 30 start bash with the venv activated, as in lecture 2.
The main README's appendix has a sample Dockerfile, but its build argument has curl instead of ffmpeg: don't paste it into transcribe audio.
Pause now and write it: a file named Dockerfile, with no extension. Type the FROM line, then copy the README's six code blocks below it, in order.

## 09:01 — Build: five steps, one fat layer
First, an extra check: your Dockerfile, named exactly that, sits next to pyproject.toml.
Step 5 builds the image. A small gap: the README names it, transcribe audio, but gives no command. Here it is: docker build, dash t and the name, then a dot for this folder, the build context.
Pause and run it. Your terminal shows a compact live view; here are the full log's landmarks. Build step 2 is our big RUN: apt installs 237 packages, a 205 megabyte download, then pip installs uv, all in 46.9 seconds.
Build steps 3 and 4 set the working folder and copy our files. Build step 5 runs uv sync with the image's own Python 3.12, creates the venv, and resolves 1 package: the project itself, with no dependencies yet.
It ends by naming the image, with a warning about line 10: Docker flags any variable whose name sounds secret. The value is just a path, so it's harmless, and you'll see it every build.
An extra check, docker images, says 1.35 gigabytes on this machine. By far the biggest layer is that one RUN, 842 megabytes of compilers, ffmpeg and their libraries, while the copied folder is tiny.
And if you skipped uv init, build step 5 fails, because there's no pyproject.toml to sync.
Ponder this. You change only the group name in cli.py and build again: which of the five build steps run again?
Build steps 4 and 5. The copied folder changed, so the copy runs again, and so does every step after it; build steps 1 to 3 come from the cache. We'll see it in part 2.

## 11:03 — Run: a window into your laptop
Step 6 runs the image, so first, a picture. The copied files sit in slash app; the venv sits outside it, in slash home. As in lecture 2, a container adds a thin writable layer, thrown away on exit by dash dash r m.
Dash v mounts the current folder, pwd, onto slash app: it covers the copied files, so slash app is now your folder.
So edits in VS Code show up inside at once. Anything written under slash app goes straight into your laptop's folder and stays; anything else lands on the throwaway layer.
Ponder this. In lecture 2, the venv sat next to the code. If it sat in slash app here, what would the container find there with this mount?
It would find your laptop's folder, with no venv in it, so activation would fail. That's what line 9, uv project environment, prevents.
Type docker run, dash dash r m, dash t i, dash v with the mount, and the image name. Copy it from the README, quotes included, and pause to run it.
On Windows, run these commands in Git BASH, keep the quotes around pwd, and if docker run says the input device is not a T-T-Y, put winpty in front.
The prompt changes: you're user app, in slash app, and after the at sign comes the container's ID, new on every run.
No venv name shows in the prompt, yet the venv is active: two extra checks find python in slash home, version 3.12.
Two more extras: listing the folder shows your laptop's files, and the key variable from line 10 is set.
Last extra: ask cli.py for its help. Module not found, no module named google: the packages aren't installed yet.
The container runs and sees your folder, but Python can't find Google. In part 2, we add the packages, and find out why they vanish.

## 13:11 — uv add: what lands where
Welcome back. We're inside the transcribe audio container, and Python can't find Google's packages yet.
Step 7: the README lists three packages to add, so type all three in one uv add command. Pause and run it.
Three packages asked for, and 26 installed. As in lecture 1, each package brings its own dependencies, and uv resolves the whole tree.
But where did everything land? The list, pyproject.toml, and the receipt, uv.lock, sit in slash app, so they're written to your laptop. The 26 packages went into the venv in slash home, on the container's throwaway layer.
Two extra checks. The pyproject.toml now lists the three packages, each with a lower bound, and a new uv.lock of about 138 kilobytes sits next to cli.py, owned by user app.
Another extra: the venv variable says slash home, slash app, slash dot venv, outside the window.
Two asides. The package is ffmpeg dash python; plain ffmpeg is another project. And on a Linux laptop whose folder isn't owned by user ID 1000, uv add fails with permission denied: the chown command on screen fixes it.
The README adds: when you exit, rebuild the image. We'll do that at the end, and see why.
Step 8: set your group name. On your laptop, in VS Code, open cli.py and change line 21 to your team's name; ours is group-01. Pause and make the change.
Inside, an extra grep already shows the new line: the window works both ways. Use the same name in all five cli.py files, or the stages won't find each other's work.
Step 9: python cli.py dash dash help. This time it works, and it matches the README's block line for line. Pause, and get to this point.

## 15:16 — Who is calling? The key and ADC
Step 10 downloads the recordings: python cli.py dash dash download, or dash d for short. Our machine had no key, so here's what a missing key looks like.
It printed the arguments and the word download, then a traceback. The last line says default credentials error: the file secrets, slash, mega-pipeline dot json was not found.
Read it as in lecture 1. Our code, line 36, built a storage client; the client asked Google's auth library for credentials, and that library looked for a missing file.
Here's the chain when it works. Your code never passes the key: the client asks Google's auth library who it is. That search is called application default credentials, or ADC, and its first stop is the variable from line 10.
That variable is a signpost: secrets, slash, mega-pipeline dot json, starting from the current folder, slash app. Through the window, it leads to the key on your laptop.
From the key, the library makes a short-lived access token, and every request to Google carries it.
Google then checks twice, as the README says. Authentication asks who is calling, and the key says it's the course's service account; authorization asks whether it may do this, and IAM roles open the bucket.
This error has three usual causes. The key isn't in this component's secrets folder, you changed directory away from slash app, or you ran docker run from the wrong laptop folder.
One extra check: even this failed run created two folders on your laptop, input audios, and text prompts with your group inside. The code makes them before it builds the client.
With your key, look for the word download, one object name per recording, and the audio files appearing in input audios on your laptop. Pause, check your key is in secrets, and run it.

## 17:23 — Transcribe and upload
Step 11 transcribes. For each recording, ffmpeg first converts the MP3 into FLAC, and that's why ffmpeg is in the build argument.
The audio bytes travel inside the request. The long-running recognize call hands back an operation at once, like a ticket stub. Its result call then waits up to 90 seconds for the transcript.
Long audio comes back in pieces, so lines 84 to 91 join every piece; that was the latest commit's fix.
Type python cli.py dash dash transcribe, or dash t. Look for transcribing and a file name, ffmpeg's log, the response, and the transcript. If it says no such file, ffmpeg, add ffmpeg to line 3, exit and rebuild.
Then open the new text file under text prompts, group-01, on your laptop. If it says None, Speech-to-Text returned nothing: delete it and transcribe again, because finished files are skipped.
Step 12: python cli.py dash dash upload, or dash u. It uploads only files starting with input, under the same name in the bucket: look for uploading, then text prompts, your group, and the file.
Your transcript drops into your group's drawer, and the transcribe cell lights up on the leaderboard, which is how the README says to check. Pause and run all three steps, with your key.
An extra tip: the flags combine, so dash d, dash t, dash u runs all three, in order. Each call is billed to the course project.

## 19:00 — Exit, and bake it in
Step 13: exit, and rebuild. Type exit, and the container is removed with its throwaway layer, and the 26 packages go with it.
Back on the laptop, an extra check: the pyproject.toml with three dependencies, the lock file, and the two new folders all survived, because they were in the window.
Git status shows only cli.py as changed; we'll see why the rest is invisible at the end.
Now the trap, as an extra. Start a new container from the image you built earlier, and ask for help again. It's module not found again: the packages lived only in the old container.
The README's fix: exit, and rebuild the image with the same docker build command. Pause and run it.
The ponder's answer, for real: build steps 2 and 3 are cached, while build step 4 copies the changed folder and build step 5, uv sync, runs again. The build took under ten seconds.
The full log shows what uv sync did this time: the copy brought in the lock file, and uv installed the same 26 packages, into the image.
Two more extras. The image grew to 1.48 gigabytes, and docker history lists one row per instruction: card-only lines show zero bytes. The uv sync layer now holds 105 megabytes, the packages plus uv's download cache.
And a fresh container now imports all three packages with no uv add at all: they're baked in.
One more thing: because the copy comes before uv sync, any edit, even the group name, knocks over uv sync, like lecture 2's dominoes. Later tutorials copy pyproject.toml and uv.lock first.

## 20:50 — generate_text: same recipe, two surprises
Component B, generate text, follows the same recipe; we'll go faster. Steps 1 and 2: cd into its folder, and copy the key into its secrets folder.
An extra look: this folder already has its own pyproject.toml, listing both packages and requiring Python 3.14 or newer. Leave that until step 13.
Surprise one: uv init fails: the project is already initialized. The README still says to run it, a small mistake: skip step 3, and ignore the leftover main dot py.
Step 4: the same Dockerfile, except line 3 drops ffmpeg, since this component never touches audio. Copy yours and change that line.
Step 5 builds it, and the big RUN step runs again, because the package list it installs changed. Pause and run it.
Ponder this. The image has Python 3.12; this pyproject.toml asks for 3.14 or newer. Which Python will the venv use?
The live view hides it; the full log shows it: uv downloaded its own Python, 3.15.0 at the time of recording, and built the venv on it.
The image's 3.12 falls outside the interval, so uv fetched the newest Python in range, as in lecture 2.
Step 6 runs it, and an extra check confirms Python 3.15.0, from uv's folder, not the image's.
Step 7's uv add finds nothing new, since both packages are listed; it only writes the lock file.
Steps 8 and 9: set the group name, here on line 19, and check the help, which matches the README. Pause and catch up.
Steps 10 to 12: download, generate, upload. The generate step sends each transcript to Gemini 2.5 Flash Lite on Vertex AI. Google retires that model on October 20, 2026; after that, start the container with a current model in the Gemini model variable.
Look for your prompt, generated text and a long podcast script, then the upload. Pause and run all three.
Step 13, exit and rebuild, brings the fix: lower the minimum Python version to 3.12. Git status lists the Dockerfile too: this folder has no dot gitignore.
Pause and rebuild: uv sync now uses the image's Python 3.12, as does the next container. Exit it. Better still, fix this before your first build.

## 23:40 — Synthesize, translate, synthesize
Speed round: C, D and E. For C, synthesis audio E-N, cd in, copy the key, and run uv init. If it stamps 3.13 or newer, change it to 3.12, here and in D and E.
Write the same Dockerfile as B's. A small slip, here and in E: the README's text says to keep ffmpeg, but its code block, which is right, leaves it out.
Build it: build step 2 is cached and the build takes 0.6 seconds: C's Dockerfile matches B's up to there, so Docker reuses B's big layer.
Run it, and add storage and text to speech: 24 packages.
Set the group name on line 18, then check the help. Without a key, even help fails: line 22 builds the Text-to-Speech client as soon as the script starts, before reading any flags. Pause and catch up.
The request carries the text and an address in the bucket, line 78. Google's long audio service writes the speech straight there, never through your container.
C just holds a ticket stub for up to 300 seconds, then prints that the audio will be saved: so C has no upload step.
So in C, pause to run download and synthesis, then exit and rebuild.
D, translate text, races through the same setup: cd, key, uv init, the same Dockerfile, a build.
Then run it, add storage and translate, and set the group name on line 18. Like C, even help needs the key. Pause and catch up.
Translation has no ticket stub: the French comes straight back, is printed and saved under text translated, so D needs an upload.
Pause to run download, translate and upload, then exit and rebuild.
E, synthesis audio, is C again, group name on line 18 too. One harmless slip: its help text says transcribe audio file to text, pasted from A's code. Pause and catch up.
Pause, and run download and synthesis with your key.
An optional bonus in E speaks the French with ElevenLabs, in the instructor's voice. It uses your own ElevenLabs key and quota: a key file in secrets, your group name in the bonus script too, and uv add requests.
Then run its three commands. Without the key file, even download fails: the script reads that file as soon as it starts.
Pause to exit and rebuild E. With all five done, your group's drawers fill, and your leaderboard row lights up.

## 26:26 — Keep the key out of the image
One last question about the key. It's git-ignored, so it never reaches GitHub. But you build the image and push it to Docker Hub: is the key inside?
Let's test it, with an 82 byte stand-in for the real key. These extra Git commands show it's ignored, by line 3 of dot gitignore.
Now rebuild, and list the secrets folder inside the image itself, with no mount. There it is: mega-pipeline dot json, inside the image. Your real key is in every image you built today, because step 2 came before step 5.
Docker doesn't read dot gitignore. Remember lecture 2's parcel: the build context is the whole folder, key included, and the copy line unpacks all of it. The README's secrets note covers Git only.
The fix, which lecture 2 recommended, is an extra here: a file named dot dockerignore, with one line, secrets slash. All five images copied the key, so pause and add it in all five folders.
Rebuild, and list again: cannot access, no such file or directory. The key stayed out of the image.
And the run still works, because the mount brings your secrets folder in when the container starts.
The README's optional last section pushes the image to Docker Hub: create an access token there, then log in, tag and push. Only push an image built with that dot dockerignore.
Log in with just your user name and paste the token at the prompt; after dash p it stays in your shell history. If you ever pushed an image with the key, delete it and tell the staff.
Where the course is heading: last year's solution kept the secrets folder outside the repo and mounted it at slash secrets at run time. No key ever enters the image.

## 28:28 — Clean up, recap, and what's next
Time to clean up. In the cloud there's nothing to delete: you created no machine, bucket or account.
Locally, cd dot dot back up to the repo. An extra command lists the five images: transcribe audio at 1.48 gigabytes, the other four at about 845 megabytes each.
To keep your work, check Git. An extra git status shows your edited cli.py files and the files in generate text, but the other four folders hide their Dockerfiles and project files.
In your own repo, add those Dockerfiles and project files with git add dash f, but not the data folders, and never stop ignoring secrets.
Then pause and remove the five images with docker image rm, another extra. Older builds stay behind untagged, each holding your key, so docker image prune removes those too.
Five questions to test yourself. One: which drawer does D, translate text, read, and who wrote it? Two: why doesn't the mount hide the packages, and what breaks without uv project environment?
Three: after uv add in a throwaway container, what survives, and what makes it permanent? Four: which variable points to the key, and why only from slash app? Five: how can an image hold a git-ignored key, and the fix?
Answers are in the exercises; every command is in the study guide. Next lecture: your own bucket and service account, the key outside the repo, and a script that builds and runs each container.
