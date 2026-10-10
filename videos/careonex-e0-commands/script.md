# CareOneX E0 · Decoding the start-up commands — script & visual plan (v1)

Series: *CareOneX, layer by layer* (`videos/careonex-series/SERIES.md`). Watch first.

Audience: a complete beginner who wants to understand everything. No AWS, Docker, networking or
Python-packaging knowledge assumed. Goal: after E0 the viewer can read Marco's two start-up commands
and say what every line does, why it is there, and which piece of the system it touches.

**No narrator.** SAY lines are the subtitles (Chinese above, English below), shown at a reading pace
of ~2.2 words/s. Short sentences, one idea each.

**Sources.** The two command blocks Marco posted in the team chat (2026-10-10, 16:08), copied exactly.
The code on GitHub (`nadirbt/careonex-agents`: `data-retrieval@d96a4ad`, `feat/sonic_with_rag@eff4a96`),
`TEAM_SETUP.md` on `data-retrieval`. Marco's own code was not on GitHub yet when this was written;
it arrived the same evening as `feat/sonic_with_rag_updated@1591ed2`, and S08 and S10 now use it to
settle the two guesses they had made.
The Knowledge Base id in his command is shown masked (`UYC7······`): this repository is public, and the
team's own docs keep account identifiers out of it.

**Source tags** (every claim on screen carries one): `READ IN CODE` · `TEAM NOTES` · `MEASURED` ·
`INFERRED` (with the reason). Colours: tags GREY, INFERRED PURPLE so guesses stand out.

Conventions: `SHOW:` what is on screen during the following `SAY:`. Semantic colours: our code =
BLUE · stored data = GREEN · AWS = ORANGE · the person / laptop = WHITE · a request or a setting
being explained = YELLOW · problems = RED.

---

## S01 · Two walls of text — `s01_hook.py` · `Hook`

SHOW: The two command blocks, exactly as Marco posted them, side by side in two terminal windows
labelled "terminal 1" and "terminal 2". The KB id is masked.
SAY: Marco sent the team these two blocks of commands. They start the CareOneX voice app on his laptop. If they look like a wall of noise, that is normal.

SHOW: Each line gets a small number badge 1–14 (empty lines skipped), lit one after another.
SAY: By the end of this video, every line will mean something. Each one turns out to be a small lesson about how the whole system fits together.

SHOW: A card "How we know": four tags with their meaning: READ IN CODE · TEAM NOTES · MEASURED ·
INFERRED. A padlock on an "AWS account" cloud: "we cannot log in".
SAY: One warning first. We cannot log into the team's AWS account. So everything here is learned from the code on GitHub and the team's notes. Each claim carries a tag, and when we are guessing, the tag says INFERRED, with our reason.

---

## S02 · Two terminals, two programs — `s02_two.py` · `TwoPrograms`

SHOW: A laptop (WHITE outline). Inside it two windows: terminal 1 → a BLUE box "retrieve"
(container, "search server"); terminal 2 → a BLUE box "voice" ("talks to you"). Outside the laptop,
an ORANGE cloud "AWS · us-east-1". Tag READ IN CODE.
SAY: The two blocks start two programs. Terminal 1 starts retrieve, a small search server. Terminal 2 starts voice, the program you actually talk to.

SHOW: A microphone and a speaker attach to voice. An arrow voice → retrieve labelled
"127.0.0.1:8080". Arrows from both programs to the AWS cloud: voice → "Nova 2 Sonic", retrieve →
"Knowledge Base".
SAY: Voice listens to your microphone and plays the reply. When it needs a fact, it asks retrieve, on the same laptop. Both programs also talk to Amazon's cloud, AWS, where the AI models and the document library live.

SHOW: A terminal window, a cursor blinking; "a terminal = a window where you type commands".
Underneath: "PowerShell (Windows)", the terminal Marco uses. Tag INFERRED: "`$env:` and the
`C:\Users\…` path are PowerShell syntax".
SAY: A terminal is a window where you type commands instead of clicking. Marco is on Windows, using PowerShell. We can tell from the way his lines are written.

---

## S03 · Line 1: cd — `s03_cd.py` · `ChangeDir`

SHOW: Line 1 lit: `cd "C:\Users\Marco\Desktop\CareOneX_Requester_Live_Voice_App"`. A folder tree
opens: Desktop → CareOneX_Requester_Live_Voice_App → services/ (data, extract, chunk, kb-sync,
retrieve, voice) + docker-compose.yml.
SAY: Line 1 is cd, short for change directory. It moves the terminal into the project folder. Every later command looks for its files relative to this folder.

SHOW: Tag INFERRED next to the folder name: "the folder holds Marco's copy of the team repository,
careonex-agents, with his own changes. The name is his; the layout (services/, docker-compose.yml)
is what the later commands need."
SAY: The folder is Marco's own copy of the team's code, with his newest changes in it. We infer that, because the next commands expect exactly the folders of the team repository.

---

## S04 · Sticky notes: environment variables — `s04_env.py` · `EnvVars`

SHOW: Line `$env:AWS_PROFILE = "careonex-team"` lit. The terminal grows a row of sticky notes
(YELLOW): AWS_PROFILE = careonex-team, AWS_DEFAULT_REGION = us-east-1, …
SAY: Most of the other lines look like this: dollar sign, env, colon, a name, equals, a value. Each one sets an environment variable.

SHOW: A program box launched from the terminal reads the sticky notes (arrows from notes into the
program). Code snippet from config.py: `os.environ.get("CAREONEX_RETRIEVE_URL", "")`. Tag READ IN CODE.
SAY: Think of environment variables as sticky notes on the terminal window. Every program started from that window can read them. The CareOneX code reads its settings this way, so nothing about Marco's laptop is written into the code.

SHOW: Terminal 2 has its own, separate set of notes; the notes of terminal 1 do not cross over.
SAY: The notes belong to one window only. That is why both blocks set the same AWS lines again.

---

## S05 · Who are you? AWS profile and SSO login — `s05_login.py` · `Login`

SHOW: The ORANGE cloud becomes "the team's AWS account": a fenced area inside AWS. Inside: Bedrock
models, S3 buckets, the Knowledge Base. A budget meter: "$30 / month on Bedrock, alerts at 50 %,
80 %, 100 %". Tag TEAM NOTES (TEAM_SETUP.md).
SAY: An AWS account is the team's own fenced-off corner of Amazon's cloud. Everything CareOneX uses lives inside it, and it has one bill. The team's notes show a budget of 30 dollars a month for the AI models.

SHOW: Five people (Nadir GOLD as owner; Caroline, Helen, Junyi, Marco) → a portal → each gets
"AC215" permissions. A card lists what AC215 allows: talk to Nova 2 Sonic and Titan · read and write
ac215-* buckets and vector buckets · manage knowledge bases · nothing on careonex-*. Tag TEAM NOTES.
SAY: Nobody shares a password. Each teammate signs in through a single sign-on portal, called SSO, with their own email and a second factor. After signing in, everyone gets the same set of permissions, named AC215. It covers the AI models, the course's own storage, and the knowledge base, and nothing in the company's production systems.

SHOW: Line `$env:AWS_PROFILE = "careonex-team"`, then line `aws sso login --profile careonex-team`.
The one-time setup from TEAM_SETUP.md, `aws configure sso` (session "careonex", start URL <portal>,
account <team account>, role AC215, region us-east-1, profile name careonex-team), writing a profile
block into `~/.aws/config` (tag TEAM NOTES). A browser pops up "Approve"; a key icon with "8 hours"
drops into `~/.aws/sso/cache`.
SAY: A profile is a named entry in a settings file on the laptop. "careonex-team" says: log in through that portal, into the team account, with the AC215 permissions. The command aws sso login opens a browser, you approve, and the laptop receives temporary keys that last 8 hours.

SHOW: Code from session.py: `_load_sso_credentials()` reading the profile with botocore, and the
message "Run: aws sso login --profile careonex-team and start again." Tag READ IN CODE.
SAY: The CareOneX code finds those temporary keys through the profile name. When they expire, the voice program stops with a one-line message telling you to log in again.

---

## S06 · Where in the world: the region — `s06_region.py` · `Region`

SHOW: A world map with dots for AWS regions; us-east-1 (Northern Virginia) lit. Line
`$env:AWS_DEFAULT_REGION = "us-east-1"` lit. Tag READ IN CODE: "every service defaults to
us-east-1"; TEAM NOTES: "Nova 2 Sonic is enabled for the team in us-east-1".
SAY: AWS runs data centers in many regions around the world. Each region is its own copy of the cloud. The team's models and storage are all in us-east-1, in Northern Virginia, so every program must be told to go there.

---

## S07 · The strange one: $env:HOME = $HOME — `s07_home.py` · `Home`

SHOW: Line `$env:HOME = $HOME` lit, with a question mark.
SAY: Now the strangest line: set HOME to HOME. It looks like it does nothing. It fixes a Windows problem.

SHOW: docker-compose.yml excerpt: `- ${HOME}/.aws:/home/app/.aws` (tag READ IN CODE). A tunnel from
the laptop folder `C:\Users\Marco\.aws` (with the 8-hour key) into the container's
`/home/app/.aws`.
SAY: The retrieve program will run inside a container, a sealed box. To use your login, the box needs your keys folder. The team's Docker file finds that folder through a variable named HOME.

SHOW: Two columns: Mac/Linux: HOME is an environment variable ✓. Windows PowerShell: `$HOME` exists
only inside PowerShell; HOME as an environment variable: empty → the tunnel points at "/.aws"
(RED). The line copies one into the other. Tag INFERRED: "from how PowerShell and Docker Compose
handle variables; terminal 2 does not need it because it does not use Docker". Small note: "the
team's setup guide is written for macOS (Homebrew); Windows needs this extra line" (TEAM NOTES).
SAY: On a Mac, HOME is always set. On Windows it is not, so the box would look for keys in an empty path and fail to log in. The line copies PowerShell's own home folder into the HOME sticky note. Only terminal 1 needs it, because only terminal 1 uses Docker.

---

## S08 · Which library? CAREONEX_KB_ID — `s08_kbid.py` · `KnowledgeBaseId`

SHOW: Line `$env:CAREONEX_KB_ID = "UYC7······"` lit. An ORANGE box "Bedrock Knowledge Base" with an
ID badge. Inside it: GREEN chunks → vectors (as in E2). Tag READ IN CODE.
SAY: A Knowledge Base is an Amazon service that stores the team's documents as small searchable passages, and searches them on request. Every knowledge base has an ID, a short code like this one.

SHOW: retrieve's config.py: `env = os.environ.get("CAREONEX_KB_ID"); if env: return env` → else
read `config/knowledge-base.json` from the S3 bucket. Two arrows into retrieve: the sticky note
(lit) and the bucket file (dimmed). Tag READ IN CODE.
SAY: The retrieve code looks for this sticky note first. If it is missing, it reads the ID from a file in the team's storage, written there by the container that built the library.

SHOW: The two guesses we made before Marco's code was public (INFERRED, PURPLE): "skip one read from
storage" · "point at a different knowledge base, e.g. one built for Marco's experiments". Then the
answer from his branch `feat/sonic_with_rag_updated` (READ IN CODE): his README line
`$env:CAREONEX_KB_ID = "UYC7······"  # example staging KB`; the second guess gets a ✓, the first fades.
"library C: one of three test libraries for comparing chunkers (E6)". Without the line: retrieve
reads `config/knowledge-base.json` → the main library.
SAY: Why set it by hand? We had guessed two reasons: to save one read from storage, or to point retrieve at a different knowledge base. Marco's branch, pushed later that day, settles it. This ID is one of three test libraries he built to compare ways of cutting the documents. Without this line, retrieve would use the main library. Episode 6 explains his test.

---

## S09 · Boxes: docker compose up --build retrieve — `s09_docker.py` · `Docker`

SHOW: An "image" = a frozen box: Python 3.12 + the retrieve code + its libraries (from retrieve's
Dockerfile). A "container" = a running copy of the image. Tag READ IN CODE (Dockerfile).
SAY: Docker packs a program with everything it needs into an image, like a frozen lunch box. A container is that box, running. It runs the same on Marco's laptop, on yours, and on a server.

SHOW: Line `docker compose up --build retrieve` with each word underlined in turn: compose → reads
docker-compose.yml (7 services listed, retrieve lit); up → start; --build → rebuild the image first
(a hammer); retrieve → only this service.
SAY: Docker compose reads the team's file that describes all the containers. The word up starts one. The option build first rebuilds its image, so Marco's newest code is inside. And retrieve picks just the search server.

SHOW: The running retrieve container: "FastAPI app", two doors: GET /health and POST /retrieve, on
port 8080; a pipe from container port 8080 to laptop port 8080 (`ports: "8080:8080"`). Tag READ IN
CODE.
SAY: Inside the box, retrieve becomes a small web server. It listens on port 8080, a numbered door. The Docker file connects that door to the same door on the laptop, so other programs can knock.

---

## S10 · Terminal 2: where to ask, and how — `s10_voice_env.py` · `VoiceSettings`

SHOW: Line `$env:CAREONEX_RETRIEVE_URL = "http://127.0.0.1:8080"`. 127.0.0.1 → "this computer"
(a laptop pointing at itself); :8080 → the door from S09. Code: if the URL is empty, the tool answers
"knowledge base unavailable". Tag READ IN CODE.
SAY: In terminal 2, the first new note tells voice where retrieve is. 127.0.0.1 always means this same computer, and 8080 is the door retrieve opened. Without this note, the voice app answers that the knowledge base is unavailable.

SHOW: Line `$env:CAREONEX_VOICE_SEARCH_MODE = "feedback"`. First: the search of the four branches that
were on GitHub that morning: 0 results (MEASURED). Then Marco's branch (READ IN CODE), tools.py:
`mode = os.environ.get("CAREONEX_VOICE_SEARCH_MODE", "feedback")`; two values: `feedback` = a first
search, maybe one extra search, merged (E6) · `baseline` = one search only, the rollback switch.
Our earlier guess ("a switch that chooses how voice searches") gets a ✓.
SAY: The next note picks how voice searches. When we first looked, it was nowhere in the code on GitHub. Marco's branch, pushed later that day, explains it. Feedback runs a first search, may add one more, and merges the results. Baseline runs one search only. Feedback is also the default when the note is missing. Episode 6 shows what it does.

---

## S11 · The long last line: uv run — `s11_uv.py` · `UvRun`

SHOW: The last line, split into its parts, each lit in turn: `uv run` · `--python 3.12` ·
`--extra mic` · `--directory services/voice` · `python -c "…"`.
SAY: The last line is the longest. Let's take it apart.

SHOW: uv → a tool that builds the right Python setup for a project and runs a command in it.
--python 3.12 → Amazon's streaming library needs at least 3.12 (tag READ IN CODE: pyproject
`requires-python >=3.12`). --directory services/voice → use the voice project's settings and
libraries.
SAY: uv is a tool that sets up the exact Python and libraries a project needs, then runs a command inside that setup. Python 3.12 is the oldest version Amazon's streaming library accepts. And the directory option says: use the voice project.

SHOW: --extra mic → also install PyAudio, the microphone library (pyproject: optional `mic` extra).
A container with a crossed-out microphone: "PyAudio is not in the image on purpose". Tag READ IN CODE.
SAY: extra mic adds the microphone library. It is optional on purpose: a container has no microphone or speakers, so the voice program runs directly on the laptop instead.

SHOW: `python -c "import asyncio; from nova_sonic.__main__ import run; asyncio.run(run())"` →
"run this tiny program: start the voice session". Next to it the README's shorter way, `uv run
careonex-voice`, which goes through `main()`; main()'s check highlighted: no keys in sticky notes and
no `~/.aws/credentials` file → stop. Tag INFERRED: "calling run() directly skips that check, which
expects long-lived keys; with SSO there may be no credentials file".
SAY: Finally, the quoted part is a tiny Python program that starts the voice session. The team's instructions use a shorter command, but that one first checks for a kind of saved key file that an SSO login may never create. Calling the session directly skips that check. That is our inference; it fits the code exactly.

---

## S12 · The whole picture — `s12_picture.py` · `WholePicture`

SHOW: The laptop with both programs, the AWS account with Nova 2 Sonic, Titan, the Knowledge Base,
S3 Vectors and the bucket; the keys from the SSO login flowing to both programs. Then one spoken
question animates through: mic → voice → Nova 2 Sonic → tool request → voice → retrieve (8080) →
Knowledge Base → passages back → Nova → speaker.
SAY: Put together, it looks like this. Both programs use your 8-hour login. You speak, voice streams it to Nova 2 Sonic, Nova asks for a fact, voice asks retrieve, retrieve searches the knowledge base, and Nova speaks the answer.

SHOW: A cheat-sheet card with every term from this video and one line each.
SAY: Here is every new word from this video on one card. Pause here if you want to keep it.

SHOW: The series map: E1 the big picture, E2 the library, E3 search, E4 the voice loop, E5 checking
answers, then Marco's experiments.
SAY: Next, the big picture: what CareOneX is for, and who on the team built which part.
