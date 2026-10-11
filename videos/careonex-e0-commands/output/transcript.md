# CareOneX E0 · Decoding the start-up commands: every word, for a beginner

## 00:00 — Two walls of text
Marco sent the team these two blocks of commands. They start the CareOneX voice app on his laptop. If they look like a wall of noise, that is normal.
By the end of this video, every line will mean something. Each one turns out to be a small lesson about how the whole system fits together.
One warning first. We cannot log into the team's AWS account. So everything here is learned from the code on GitHub and the team's notes. Each claim carries a tag, and when we are guessing, the tag says INFERRED, with our reason.

## 00:46 — Two terminals, two programs
The two blocks start two programs. Terminal 1 starts retrieve, a small search server. Terminal 2 starts voice, the program you actually talk to.
Voice listens to your microphone and plays the reply. When it needs a fact, it asks retrieve, on the same laptop. Both programs also talk to Amazon's cloud, AWS, where the AI models and the document library live.
A terminal is a window where you type commands instead of clicking. Marco is on Windows, using PowerShell. We can tell from the way his lines are written.

## 01:29 — cd: the project folder
Line 1 is cd, short for change directory. It moves the terminal into the project folder. Every later command looks for its files relative to this folder.
The folder is Marco's own copy of the team's code, with his newest changes in it. We infer that, because the next commands expect exactly the folders of the team repository.

## 01:57 — Sticky notes: environment variables
Most of the other lines look like this: dollar sign, env, colon, a name, equals, a value. Each one sets an environment variable.
Think of environment variables as sticky notes on the terminal window. Every program started from that window can read them. The CareOneX code reads its settings this way, so nothing about Marco's laptop is written into the code.
The notes belong to one window only. That is why both blocks set the same AWS lines again.

## 02:35 — Who are you? AWS profile and SSO login
An AWS account is the team's own fenced-off corner of Amazon's cloud. Everything CareOneX uses lives inside it, and it has one bill. The team's notes show a budget of 30 dollars a month for the AI models.
Nobody shares a password. Each teammate signs in through a single sign-on portal, called SSO, with their own email and a second factor. After signing in, everyone gets the same set of permissions, named AC215. It covers the AI models, the course's own storage, and the knowledge base, and nothing in the company's production systems.
A profile is a named entry in a settings file on the laptop. "careonex-team" says: log in through that portal, into the team account, with the AC215 permissions. The command aws sso login opens a browser, you approve, and the laptop receives temporary keys that last 8 hours.
The CareOneX code finds those temporary keys through the profile name. When they expire, the voice program stops with a one-line message telling you to log in again.

## 03:54 — Where in the world: the region
AWS runs data centers in many regions around the world. Each region is its own copy of the cloud. The team's models and storage are all in us-east-1, in Northern Virginia, so every program must be told to go there.

## 04:13 — The strange one: $env:HOME = $HOME
Now the strangest line: set HOME to HOME. It looks like it does nothing. It fixes a Windows problem.
The retrieve program will run inside a container, a sealed box. To use your login, the box needs your keys folder. The team's Docker file finds that folder through a variable named HOME.
On a Mac, HOME is always set. On Windows it is not, so the box would look for keys in an empty path and fail to log in. The line copies PowerShell's own home folder into the HOME sticky note. Only terminal 1 needs it, because only terminal 1 uses Docker.

## 05:02 — Which library? CAREONEX_KB_ID
A Knowledge Base is an Amazon service that stores the team's documents as small searchable passages, and searches them on request. Every knowledge base has an ID, a short code like this one.
The retrieve code looks for this sticky note first. If it is missing, it reads the ID from a file in the team's storage, written there by the container that built the library.
Why set it by hand? We had guessed two reasons: to save one read from storage, or to point retrieve at a different knowledge base. Marco's branch, pushed later that day, settles it. This ID is one of three test libraries he built to compare ways of cutting the documents. Without this line, retrieve would use the main library. Episode 6 explains his test.

## 06:03 — Boxes: docker compose up --build retrieve
Docker packs a program with everything it needs into an image, like a frozen lunch box. A container is that box, running. It runs the same on Marco's laptop, on yours, and on a server.
Docker compose reads the team's file that describes all the containers. The word up starts one. The option build first rebuilds its image, so Marco's newest code is inside. And retrieve picks just the search server.
Inside the box, retrieve becomes a small web server. It listens on port 8080, a numbered door. The Docker file connects that door to the same door on the laptop, so other programs can knock.

## 06:53 — Terminal 2: where to ask, and how
In terminal 2, the first new note tells voice where retrieve is. 127.0.0.1 always means this same computer, and 8080 is the door retrieve opened. Without this note, the voice app answers that the knowledge base is unavailable.
The next note picks how voice searches. When we first looked, it was nowhere in the code on GitHub. Marco's branch, pushed later that day, explains it. Feedback runs a first search, may add one more, and merges the results. Baseline runs one search only. Feedback is also the default when the note is missing. Episode 6 shows what it does.

## 07:39 — The long last line: uv run
The last line is the longest. Let's take it apart.
uv is a tool that sets up the exact Python and libraries a project needs, then runs a command inside that setup. Python 3.12 is the oldest version Amazon's streaming library accepts. And the directory option says: use the voice project.
extra mic adds the microphone library. It is optional on purpose: a container has no microphone or speakers, so the voice program runs directly on the laptop instead.
Finally, the quoted part is a tiny Python program that starts the voice session. The team's instructions use a shorter command, but that one first checks for a kind of saved key file that an SSO login may never create. Calling the session directly skips that check. That is our inference; it fits the code exactly.

## 08:43 — The whole picture
Put together, it looks like this. Both programs use your 8-hour login. You speak, voice streams it to Nova 2 Sonic, Nova asks for a fact, voice asks retrieve, retrieve searches the knowledge base, and Nova speaks the answer.
Here is every new word from this video on one card. Pause here if you want to keep it.
Next, the big picture: what CareOneX is for, and who on the team built which part.
