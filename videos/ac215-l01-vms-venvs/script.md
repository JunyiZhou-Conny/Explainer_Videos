# AC215 · Lecture 1 — Virtual machines, virtual environments and uv — narration script & visual plan (v2)

Audience: an AC215 student who knows Python and basic ML and has done Tutorial 0 (a GCP project with
billing, VS Code, git, Docker Desktop, uv on the laptop), but has never set up a cloud VM or asked
where `import` finds a package. They watch with the README of `dlops-io/simple-translate` open, a VM
of their own in a browser tab and their local clone in an editor, pausing to type every command.

Goal: after the video they can create, SSH into and delete a Compute Engine VM; explain what
`--break-system-packages` breaks and where `sudo pip3` put the files; name the three parts of a venv
and say what activation changes; predict which Python `uv sync` will use; tell `pyproject.toml`
from `uv.lock`; read a chained traceback; and they know the README's small errata.

Sources of truth: `BRIEF.md` (design), `digest.md` (tutorial digest), `assets/` (see `ASSETS.md`).
Where the digest and the captures disagree, the captures win. Nothing in a terminal panel is typed
by hand: every output line below names its capture file and line numbers.
v2 merges the four reviews in `build/review_*.md`; `build/review_merge_log.md` says what changed.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each) and become the
  subtitles. Plain spoken English: no backticks, no symbols, commands and paths described in words
  ("type sudo apt-get update", "the dot venv folder"); file names such as pyproject.toml, uv.lock,
  cli.py and pyvenv.cfg are said as words. Numbers as digits (counts that echo the terminal too:
  "installed 11"); never a "!" after a digit. Version numbers that will change are said with "at
  the time of recording".
- Every spoken sentence starts with a capital letter or a digit: `explainer.voice.split_sentences`
  splits only there, and the same split drives the TTS gaps, the subtitle cues and the one-to-one
  Chinese alignment. Never open a sentence with a command or file name; write "The command uv
  sync…", "First, curl…", "Our googletrans…". Never add 's to a word that has a lexicon entry
  unless the lexicon has the 's form too (`uv's` and `README's` do).
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer); the card is removed at the start of the next block. Four in the video.
- `TERM(folder/file: lines)`: a terminal beat. The scene types the command written just before it
  in the SHOW line (in backticks, exactly as the README spells it; extras exactly as written here),
  then prints those lines of `assets/terminal/folder/file` (line 1 of every capture is its `$ …`
  command, which is never printed; the `[exit N]` line is never printed). Inside the line list:
  `…` = print one `…` line; `+Done` = append apt's " Done" to each "Reading package lists... /
  Building dependency tree... / Reading state information..." line (ASSETS.md: lost without a
  terminal); `[Y/n] Y` = cut that line after `[Y/n]`, pause 0.6 s, type `Y`; `wrap` = fold long
  lines (`Terminal.print(..., wrap=True)`). `→ (no output)`: the prompt simply returns.
- Terminal width. Every terminal is the house `term()` (12.6 wide, 22 pt, 65 characters a row) and
  is always full width. A typed command is never cut: if prompt + command is longer than a row, it
  folds at a space onto an indented second row (toolkit: `Terminal.type` needs a `wrap=True` like
  `.print`; until then it cuts with "…", which a viewer copying the command can't use). When a
  picture needs the frame, the terminal shrinks to a 3-row strip along the bottom edge (the last
  command and its key output line). A terminal never sits half-width beside a picture. Row counts
  given below include folded rows; the line a SHOW highlights or a SAY reads must still be on
  screen at that moment.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b, header
  `path · lines a–b`; never more than 12 lines on screen at once. `PANEL(capture: lines, "header")`:
  the same look for a generated file shown from a capture (uv.lock, activate, the env file), with
  the header naming the real file and its real line numbers.
- Notes for scene authors. TERM/PANEL line numbers are *file* lines (line 1 = the `$` command), but
  `Capture.pick()` indexes the output body, so pick index = file line − 1. Lines in
  `debian12-part-a/02-git.txt`, `05-pip.txt`, `debian12-part-b/02-git.txt` and
  `debian13-part-b/02-git.txt` end in `\r` (apt progress): strip it. `25-activate-file.txt` lines
  carry grep's `97:`/`98:` prefixes: strip them and pass `first_line=97`.
- Prompts (Debian-coloured: user@host GREEN, path BLUE): `student@ac215-l01:~$`, after `cd`
  `student@ac215-l01:~/simple-translate$`, after activation
  `(app) student@ac215-l01:~/simple-translate$` (`(app)` GREEN). Terminal title `ssh · ac215-l01`.
- `TRACKER A3` / `TRACKER B9`: the `ReadmeTracker`, top-left, in every walkthrough scene, moves to
  that step. Section A = "Installing App on VM Manually", 10 steps: 1 Create VM · 2 SSH ·
  3 apt-get update · 4 Install git · 5 Clone · 6 cd · 7 Install pip · 8 Install packages ·
  9 Run it · 10 Delete VM. Section B = "Installing App on VM using UV", 12 steps: 1 Create VM ·
  2 SSH · 3 apt-get update · 4 Install git · 5 Clone · 6 cd · 7 Install uv · 8 Reload shell ·
  9 uv sync · 10 Activate · 11 Run it · 12 Delete VM. `TRACKER A2 · extra`: same step, caption
  gets " · extra" while a command the README doesn't have is on screen.
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed
  line, and the SAY says so at least the first time that command appears.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README step);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags: `illustration` (GREY) on every schematic console screen (no logos, no screenshots) and on
  every "what if" picture; `expected output` (GREY) on the `expected/` runs (part 1);
  `real capture · 2026-10-12` on the 429 run and on the part-2 runs;
  `at the time of recording` (GREY) next to uv 0.13.0 and CPython 3.15.0 when first shown.
- The cost meter is a GOLD dial whose needle sweeps, with no digits (not `CostMeter`'s `$` counter,
  which would show an invented price). It never rewinds: Delete makes it stop where it is.
- V2 layout (sys.path shelves, every use). Shelves span the full width (`Shelves(width=12.4)`; the
  terminal is the bottom strip). Path labels at 22 pt at the left. Jars are small unlabelled jar
  glyphs (≈ 0.3 wide) in their shelf's colour, right-aligned. A name tag floats above a jar only
  while the narration names it (googletrans, httpx; `pip` on apt's shelf). After S05's first
  sweep the three standard-library shelves merge into one GREY band, "standard library", and later
  scenes use short labels: `/usr/local/… (pip's)`, `/usr/lib/python3/… (apt's)`,
  `.venv/…/site-packages`.
- V3 layout (PATH doors, every use). Full width above the terminal strip; doors labelled
  `~/.local/bin`, `/usr/local/bin`, `/usr/bin`, `/bin` and one narrow GREY door `…` for the two
  games folders; gap 0.35. The walking figure starts above the first door; "command not found"
  sits under the row, not beside it.
- Spelling on screen: American. Errata are pointed out kindly, always with the fix (on-screen tag
  "erratum"; the narration says "a small mistake").
- Semantic colours (fixed for the whole video):

  | meaning | colour |
  | --- | --- |
  | the laptop / browser | GREY |
  | the cloud, the VM, Google's servers | BLUE |
  | the system Python and everything apt / `sudo pip` put in it (shared, OS-owned) | ORANGE |
  | the venv, `.venv/`, `uv.lock`, project-owned packages | GREEN |
  | uv itself (the tool) | PURPLE |
  | errors, refusals, the 429, "don't do this" | RED |
  | your turn, the README tracker, "look here now" | YELLOW |
  | money: the cost meter, billing tags | GOLD |
  | PATH and sys.path lookups (the search-light, the doors) | PINK |
  | a future thing (the L2 container) | GREY, dashed |

  Package chips/jars are coloured by **where they live** (ORANGE in the system, GREEN in the venv),
  never by package. Something that is merely absent (a file not in the repo, a version that may
  differ) is GREY dashed, not RED.
- Running example: user `student`, VM `ac215-l01` (zone us-central1-a, e2-small, Debian 12, external
  IP on), as in the captures. Debian 13 appears as the alternative where it changes the outcome
  (S03 `python3 --version`, S10 which Python uv uses, S11 the package count, S12 `python --version`).
- Length and parts: narration ≈ 4,290 words. Measured with Kokoro af_heart at speed 0.9 the voice
  speaks ≈ 151 wpm, not 174 (review_spoken #9), so ≈ 28 min of narration; typing, outputs and
  ponder timers bring it to ≈ 33 min (series range 25–35; BRIEF says ~30). Part 1 = S01–S07 (the VM
  and the manual install), part 2 = S08–S15 (venvs and uv). Each part ends on an empty frame.

---

## S01 · Why won't pip install? — `s01_hook.py` · `Hook`

SHOW: Black frame. A terminal (12.6 wide, 11 rows, title `ssh · ac215-l01`, prompt
`student@ac215-l01:~/simple-translate$`) fades in center. It types
`pip3 install googletrans==4.0.2 art` (extra; folds onto a second row) →
TERM(debian12-part-a/07-pip-refused.txt: 2–4, …, 10, …, 21; wrap) (10 rows in the 11-row terminal:
nothing scrolls). Line 2 `error: externally-managed-environment` prints RED; the rest in output grey.
SAY: Here's a brand-new computer in the cloud. It's ours, and we have root, full administrator rights. We ask pip for two Python packages, and pip says no.

SHOW: The terminal stays. A YELLOW underline sweeps under "This environment is externally managed"
(line 4), then under "create a virtual environment" (line 10). A GREY `extra` tag sits beside the
typed command.
SAY: This command isn't from the README; it's the one most of us would type first. The error says the environment is externally managed, and suggests a virtual environment. By the end of this video, every line of it will make sense.

SHOW: The terminal shrinks to the top-left corner and fades. The word "virtual" writes large in the
center, then duplicates and slides apart: left "virtual machine" (BLUE) over a small server-slice
glyph, right "virtual environment" (GREEN) over a small box of jars. The jar box then shrinks and
flies inside the server slice (V7 preview): GREEN box nested in BLUE box.
SAY: Today's lecture uses the word virtual twice. A virtual machine is a whole computer you rent and throw away. A virtual environment is a private set of Python packages for one project. And one will live inside the other.

SHOW: V7 ladder. A four-rung ladder builds from the bottom, header `README.md · lines 9–14`, each
rung a short label from the README: "1 Manual install on the VM", "2 Same VM, but with uv",
"3 Docker, on your laptop", "4 Run the Docker image on a VM". Rungs 1 (BLUE) and 2 (GREEN) light
up with a YELLOW "today" bracket; rungs 3–4 are GREY dashed with a small "L2" tag. Under rung 2, a
small GREY note: "a fresh VM of the same kind".
SAY: The tutorial, simple-translate, runs one small app four ways, each removing a kind of fragility. Today we climb the first two rungs: a manual install on a cloud VM, then a fresh VM of the same kind, with uv. Docker comes next lecture.

SHOW: A layout preview, built piece by piece as named: the ReadmeTracker appears top-left
("README › Installing App on VM Manually", 10 dots, none lit yet) with a YELLOW circle pulsing
around it; a code panel slides in at left with header `cli.py · lines 5–9` (CODE(cli.py: 5–9));
a two-line terminal at the bottom (GREY tag "preview") shows `sudo apt-get update` with a YELLOW
`▶ your turn` tag beside it, then `which python` with the GREY `extra` tag; a footer caption:
"every command: MLOps_Learning · guides/L01-vms-venvs.md".
SAY: To follow along, open the README beside this video. The tracker, top left, shows the README step. Code panels show the file and line numbers. When the yellow your-turn tag appears, pause and run the command on your own VM. A grey extra tag marks a command that isn't in the README; extras are safe, so run them too. Every command is also in the study guide, in the MLOps Learning repo.

SHOW: The preview clears. A short checklist card: "✓ Tutorial 0: a GCP project with billing"
(GREEN check), "✓ a web browser", "✗ no service account, no keys today" (GREY). Beside it a GOLD
tag "a VM costs money while it exists". Fade out.
SAY: Before you start, finish Tutorial 0, so you have a Google Cloud project with billing on. No service account or keys today; all you need is a browser.

---

## S02 · The app: cli.py — `s02_app.py` · `TheApp`

SHOW: No tracker (concept scene). CODE(cli.py: 5–9) at left. Lines 5–6 get a GREY side tag
"comes with Python"; lines 8–9 get a PINK side tag "where from?" and the words `art` and
`googletrans` turn PINK. A small GREY chip at top: "github.com/dlops-io/simple-translate · cli.py".
SAY: Before we install anything, let's see what we're installing. Open cli.py on GitHub; you'll clone it onto your VM soon. The first two imports, argparse and asyncio, come with Python. The next two, art and googletrans, don't. They have to come from somewhere. This whole lecture is about where they come from.

SHOW: The panel swaps to CODE(cli.py: 12–15) at left (6.2 wide). Line 14 highlights, and the banner
from expected/10-run-default.txt lines 4–8 draws at right; line 15 highlights, and capture line 12
(`Arguments: Namespace(text='I love cheese', file='', src='en', dest='it')`) prints full width at
20 pt under both. Then the panel swaps to CODE(cli.py: 17–23): lines 19–21 get a small GREY tag
"-f: read the text from a file", line 23 highlights, and `Input: I love cheese` (line 14) appears
under it. Thin GREY arrows link each code line to its output.
SAY: The main function prints a banner that says AC215 in ASCII art, then the parsed arguments, then the text to translate. If you pass a file with dash f, the text comes from that file instead.

SHOW: The panel swaps to CODE(cli.py: 45–51), line 49 `default="I love cheese",` highlighted; then
to CODE(cli.py: 59–70), lines 62 `default="en",` and 68 `default="it",` highlighted. V6 starts in
the top half (code panels sit in the bottom half at full width from here on): a GREY chip `argv`
with an arrow to a four-row GREY table `Namespace`: `text = 'I love cheese'` · `file = ''` ·
`src = 'en'` · `dest = 'it'`, each row lighting up as its default is highlighted in the panel.
SAY: At the bottom, argparse defines four options, and each one has a default: the text I love cheese, source language English, destination Italian. So running cli.py with no options translates I love cheese into Italian.

SHOW: CODE(cli.py: 72) alone, highlighted. V6 grows: the Namespace table feeds a circular arrow
labelled "event loop · asyncio.run(main(args))". The panel swaps to CODE(cli.py: 25–31): line 25
`async with Translator(raise_exception=True) as translator:` and line 27
`result = await translator.translate(` highlighted.
SAY: The last line starts an event loop and runs main, because googletrans version 4 is asynchronous. Inside main, a Translator sends your text off with one awaited call.

SHOW: V6 continues: a BLUE VM box (left) holds the event loop; a PINK arrow labelled "HTTPS GET"
leaves the box and reaches a BLUE cloud (right) with `translate.googleapis.com` under it (tag
"unofficial · no API key"). A small chip "JSON" travels back along a lower arrow, and the line
`Output: Adoro il formaggio` (expected/10-run-default.txt line 15, tag `expected output`) appears
under the VM box. CODE(cli.py: 39) flashes.
SAY: That call is a single HTTPS request from the VM to translate dot googleapis dot com. It's Google's unofficial translate endpoint: free, no API key, no promises. A little JSON comes back, and line 39 prints the translation.

SHOW: CODE(cli.py: 25), `raise_exception=True` boxed YELLOW. Below, two mini pipelines side by side,
tag `illustration`. Left, "library default (False)": Google's answer comes back RED "error", and
the end chip reads "Output: (your input, unchanged)" with a RED tag "looks fine, is wrong". Right,
"raise_exception=True": the RED return arrow turns into a RED exception box that rises up the
pipeline.
SAY: One detail on line 25 matters later: raise exception equals True. Without it, when Google answers with an error, googletrans hides it and hands your own input back as the translation, so nothing looks wrong. With it, a failure becomes an error you can read.

SHOW: CODE(cli.py: 32–37) alone, full width (12.7). Lines 32–37 get a RED bracket "catches every
error"; the words `from error` on line 37 underline PINK.
SAY: Lines 32 to 37 catch any error from that call and wrap it in a friendlier message about the network. Remember these lines. In a few minutes, they'll fool us.

SHOW: The full V6 picture assembles as a loop: a BLUE VM box at left holding `argv` → `Namespace` →
event loop, stacked top to bottom; a PINK "HTTPS GET" arrow to the BLUE cloud at right
(`translate.googleapis.com` under it); "JSON" back along a lower arrow; `Output:` under the VM box.
Then the two chips `art` and `googletrans` drop below the VM box and pulse PINK with "?" tags. Fade
out.
SAY: So the app is small: arguments in, one web request, one line out. What it needs is two third-party packages. Let's get a computer, and find them a home.

---

## S03 · Renting a computer: the VM — `s03_vm.py` · `RentAComputer`

SHOW: V1. A physical server (GREY rack glyph, `server()`) center. A thin slab labelled "hypervisor"
slides down onto it. The box splits into four translucent vertical slices; each grows an OS layer
on top: "Debian 12", "Ubuntu 24.04", "Debian 13", "…". One slice turns BLUE and gets the label
`ac215-l01`. Below the server, a separate row of BLUE disk blocks ("storage network"); a short line
links one of them to the BLUE slice.
SAY: A virtual machine is a slice of a real server in one of Google's data centers. Software called a hypervisor carves the machine into slices. Each slice gets virtual CPUs and memory from that server, a disk from Google's storage network, and its own operating system. One of them will be yours.

SHOW: V1 shrinks to the right third. At left, a GREY browser window (`browser_window`) with address
`console.cloud.google.com/compute/instances`, tag `illustration`, showing a schematic "VM instances"
page with a project selector at the top (GREY, "your Tutorial 0 project", pulsing YELLOW once) and
a "Create instance" button. A small GREY note: "first visit: Enable Compute Engine API".
TRACKER A1 (the tracker appears top-left).
SAY: In the console, check that your Tutorial 0 project is selected, then open Compute Engine, then VM instances. The first time, it may ask you to enable the Compute Engine API; click enable and give it a minute. Then click Create instance.

SHOW: The page becomes a schematic create form (`form_rows`), rows filling one by one:
Name `ac215-l01` · Region `us-central1` · Zone `us-central1-a` · Machine type `e2-small` ·
Boot disk `Debian GNU/Linux 12 (bookworm)` · External IPv4 `Ephemeral`. As each row fills, the
BLUE slice in V1 builds the matching part: zone → a GREY pin "us-central1-a"; machine type → a
block "CPU + memory" inside the slice; boot disk → the linked disk block below gets the label
"disk · Debian 12" (S07 greys the first block and keeps the second). A GREY footnote: "the README
gives no settings: these are sensible choices · Debian 13 works too".
SAY: The README gives no settings, so here are sensible ones. A name, like ac215-l01. A region and zone: where the machine physically lives. A machine type, which sets the CPUs and memory; e2-small is plenty. And a boot disk with Debian 12. Debian 13 works too; we'll see where it changes things.

SHOW: The External IPv4 row highlights YELLOW. In V1, PINK route lines run from the BLUE slice out
to three small chips: "Debian mirrors", "GitHub", "PyPI".
SAY: Keep the external IP address; it's on by default. Without it, and without extra network setup, this VM can't reach the internet, and every download here would hang.

SHOW: The GOLD cost meter (see Conventions: a dial, no digits) appears beside the BLUE slice and its
needle starts sweeping. Three GOLD tags slide in under it: "CPU + memory: billed per second while
running", "disk: billed while it exists" and "external IP: small hourly fee while running". On the
form, a GOLD "estimate" tag pulses on the (empty, schematic) estimate panel; no price is shown.
SAY: And now the meter starts. CPU and memory are billed by the second while the VM runs, even when it sits idle. The disk is billed for as long as it exists. The estimate is small, but the meter never stops on its own.

SHOW: "Create" is clicked; the form collapses into one instance row: a GREEN check, `ac215-l01`,
`us-central1-a`, "External IP", and an "SSH" button. The SSH button is clicked: a PINK beam shoots
from the browser into the BLUE slice; V1 and the meter shrink to a small badge at top right; a GREY
"Authorize" dialog flashes (tag `illustration`, "first time only"); then the browser window itself
transforms into the terminal (12.6 wide, 9 rows, title `ssh · ac215-l01`, prompt
`student@ac215-l01:~$`), because the SSH terminal is a browser window. The word `student` in the
prompt gets a small YELLOW tag "your username here". TRACKER A2. `▶ your turn` beside the prompt.
SAY: Click Create, wait for the green check, then click SSH. If it asks you to authorize the connection, click Authorize. A terminal opens in your browser, logged in to your new VM. Our prompt says student; yours shows your own username. Pause here, and get your VM to this point.

SHOW: TRACKER A2 · extra. It types `cat /etc/os-release` (extra) → TERM(debian12-part-a/00-os.txt:
2–5, …). The PRETTY_NAME line highlights YELLOW.
SAY: Three quick extra checks, not in the README. First, which operating system did we get? Print the os-release file: Debian 12, nicknamed bookworm.

SHOW: It types `python3 --version` (extra) → TERM(debian12-part-a/00-os.txt: 6). An ORANGE chip
"system Python" attaches to `Python 3.11.2`. At the right edge, a small GREY card titled
"Debian 13" shows TERM(debian13-part-b/00-os.txt: 6) `Python 3.13.5`.
SAY: Second, ask python3 for its version. Debian 12 ships Python 3.11.2, for the operating system itself. On Debian 13, you'd see 3.13.5. Keep both numbers in mind.

SHOW: It types `which python` (extra) → (no output; the prompt returns: capture 00-os.txt line 7
records exit status 1). A RED tag "nothing" blinks next to the empty line; a PINK caption "which:
the program a name would run · only `python3` exists here". Fade out.
SAY: Third, which python, without the 3. The which command asks which program a name would run. For python, nothing comes back: Debian has python3, but no python. Remember this for part 2.

---

## S04 · apt, git and the repo — `s04_apt_git.py` · `AptAndGit`

SHOW: TRACKER A3. Terminal (full width, prompt `student@ac215-l01:~$`). It types
`sudo apt-get update` → TERM(debian12-part-a/01-apt-update.txt: 2–9; +Done). `▶ your turn`.
Above the terminal, an ORANGE book labelled "package catalog" flips its pages; next to it a GREY
shelf "installed" stays unchanged. A GREY note: "on a Google VM: a few more lines (Google's
package sources)".
SAY: Step 3: type sudo apt-get update. Debian's package manager is apt, and sudo runs it as the administrator. Update downloads the package catalog: the list of packages that exist, and their latest versions. Nothing is installed yet. On a Google VM, you'll see a few more lines, for Google's own package sources. Pause and run it.

SHOW: The book and shelf shrink. A README tip card (GREY quote, header `README.md · line 48 (tip
after step 4)`) condenses into two chips: `apt-get` "scripts · Dockerfiles · CI" and `apt` "humans
at a terminal".
SAY: The README has a tip here: apt-get and apt do the same job. The apt-get command is the stable, scriptable one, for Dockerfiles and automated builds. The shorter apt is friendlier for typing by hand. Either is fine here.

SHOW: TRACKER A4. It types `sudo apt install git` → TERM(debian12-part-a/02-git.txt: 4–6; +Done,
…, 25–28; [Y/n] Y, …, 160–161). A GREY tag "package list varies by VM". The `Y` keystroke
flashes YELLOW. `▶ your turn`.
SAY: Step 4: sudo apt install git. This time apt really installs things. It lists what it will add and asks, do you want to continue? Type Y and press enter. The list depends on your VM; if git is already there, apt says so. Pause and run it.

SHOW: TRACKER A5. It types `git clone https://github.com/dlops-io/simple-translate.git` (folds onto
a second row) → TERM(debian12-part-a/03-clone.txt: 2). The README's clone line flashes YELLOW in a
small GREY README card ("copy it from here"). A BLUE folder glyph `simple-translate` drops into a
small "home" box at upper right.
SAY: Step 5: clone the repo. Type git clone, then the address; copy it from the README. Git copies the whole repo, with its history, into a new folder, simple-translate, in your home directory.

SHOW: TRACKER A6. It types `cd simple-translate` → (no output). The prompt for the next line becomes
`student@ac215-l01:~/simple-translate$`; the new path part flashes BLUE, and the `~` gets a small
GREY tag "~ = your home folder". `▶ your turn`.
SAY: Step 6: cd simple-translate. Watch the prompt: after the colon, it now shows the folder you're in. The wavy tilde means your home folder. Pause, and catch up to here.

SHOW: TRACKER A6 · extra. It types `ls` (extra) → TERM(debian12-part-a/04-ls.txt: 2–7).
`pyproject.toml` highlights GREEN with a tag "what the app needs"; `Dockerfile.txt` gets a GREY tag
"L2 solution file". Beside the listing, two ghost chips appear, GREY and dashed: `requirements.txt`
and `uv.lock`, captioned "not in the repo". Fade out.
SAY: One extra check: ls lists the files. There's cli.py, the README, a Dockerfile saved as a text file, two scripts for next lecture, and pyproject.toml, the list of what the app needs. Notice what's missing: no requirements file, and no lock file with exact versions. Hold on to that.

---

## S05 · The system Python and PEP 668 — `s05_system_pip.py` · `SystemPip`

SHOW: TRACKER A7. Terminal (prompt `student@ac215-l01:~/simple-translate$`). It types
`sudo apt install python3-pip` (folds onto a second row) → TERM(debian12-part-a/05-pip.txt: 4–6;
+Done, …, 54–57; [Y/n] Y, …, 603–604). GREY tag "package list varies by VM". `▶ your turn`.
SAY: Step 7: sudo apt install python3-pip. That's Debian's own packaged copy of pip, for Debian's Python. Answer Y again. Ours pulled in over a hundred packages; a real VM usually needs fewer. Pause and run it.

SHOW: TRACKER A7 · extra. It types `pip3 --version` (extra) → TERM(debian12-part-a/06-pip-version.txt:
2). The path `/usr/lib/python3/dist-packages/pip` underlines ORANGE, with a tag "apt's folder"; the
`/usr` part gets a small GREY tag "U-S-R: the system's, not your home".
SAY: An extra check: ask pip3 for its version. It's pip 23.0.1, for Python 3.11, in a folder called dist-packages under user lib. That user is spelled U-S-R: the system's files, not your home folder.

SHOW: The terminal clears and grows to 14 rows. It types `pip3 install googletrans==4.0.2 art`
(extra) → TERM(debian12-part-a/07-pip-refused.txt: 2–5, …, 10, …, 20; wrap) (14 rows), the same
text as the cold open, line 2 RED. YELLOW underlines on line 4 ("This environment is externally
managed"), line 10 ("create a virtual environment") and, in line 20, `--break-system-packages`.
SAY: Now the command from the start of the video, without sudo or any flag; it isn't in the README either. Again, pip refuses: this environment is externally managed. The hint says: install with apt, or create a virtual environment. Its last note even names a way around it.

SHOW: It types `python3 -c 'import sys; print("\n".join(sys.path))'` (extra) →
TERM(debian12-part-a/15-syspath.txt: 2–7). The six printed lines lift out of the terminal (which
shrinks to the bottom strip) and become V2 (layout: see Conventions), a full-width stack of shelves,
top to bottom: "(empty) = the current folder" (GREY), `/usr/lib/python311.zip`,
`/usr/lib/python3.11`, `/usr/lib/python3.11/lib-dynload` (GREY, bracketed "standard library"),
`/usr/local/lib/python3.11/dist-packages` (ORANGE, empty), `/usr/lib/python3/dist-packages`
(ORANGE, holding four small ORANGE jars from step 7; only `pip` carries a name tag). A PINK
search-light at the top sweeps down once. Then the three standard-library shelves merge into one
GREY band "standard library".
SAY: Why refuse? Picture how Python finds an import. This extra one-liner prints the list called sys dot path: the folders Python searches. Think of them as shelves. On every import, Python scans from the top shelf down, and takes the first match.

SHOW: The bottom ORANGE shelf glows. Small GREY gear glyphs labelled "OS tools" appear at its right
and connect to its jars with thin lines. Caption: "a shared kitchen". A small chip "PEP 668"
stamps onto the shelf's edge.
SAY: The bottom shelf belongs to apt. Debian itself runs Python tools that depend on exactly those jars, at exactly those versions. The system Python is a shared kitchen, and apt is the cook. That's what externally managed means. PEP 668 is the rule that makes pip respect it.

SHOW: TRACKER A8. The terminal grows back. It types
`sudo pip3 install --break-system-packages googletrans==4.0.2 art` (folds onto a second row) →
TERM(debian12-part-a/08-pip-break.txt: 2–5, …, 34–36; wrap). `▶ your turn`. A counter chip
"asked for 2" turns into "installed 12" (ORANGE: where they live). A GREY note: "yours may say
'Requirement already satisfied' for some". Line 36 (`WARNING: Running pip as the 'root' user …`)
gets a YELLOW bracket, and "conflicting behaviour with the system package manager" underlines.
SAY: Step 8 is the README's command: sudo pip3 install, with the flag break-system-packages. The flag overrides the guard; sudo lets pip write as administrator. Pause and run it. We asked for 2 packages and got 12; if yours says requirement already satisfied, apt already had that one. And the warning says running pip as root can clash with the system's package manager.

SHOW: Twelve small ORANGE jars fly from the terminal onto the `/usr/local/lib/python3.11/dist-packages`
shelf, which sits above apt's; a chip "12" beside them. TRACKER A8 · extra. It types
`python3 -c 'import googletrans; print(googletrans.__file__)'` (extra; folds onto a second row) →
TERM(debian12-part-a/09-where.txt: 2). The PINK search-light sweeps down and stops on a jar on the
`/usr/local` shelf; a name tag `googletrans` pops above it. The `/usr/local` label gets a GREY tag
"system-wide · every user".
SAY: Where did they go? This extra one-liner asks googletrans where it lives: in dist-packages under user local, still the system's, shared by every user. Look at the shelves: that shelf sits above the one apt owns.

SHOW: Tag `illustration` ("what if"). A dashed ORANGE jar `httpx 0.23.3 (apt's copy)` appears on the
bottom apt shelf. A PINK search-light labelled `import httpx` sweeps down and stops on pip's
`httpx 0.28.1` jar on the higher shelf (name tag pops up; a small GREY note "googletrans needs
httpx ≥ 0.27.2"). The dashed apt jar dims with a RED "hidden" tag. Caption: "shadowing · for every
program that uses the system Python".
SAY: Now suppose apt had installed an older httpx for some system tool. Our googletrans needs 0.27.2 or newer, so pip would add a second copy, on the higher shelf. Python would find that copy first and hide the one from apt, for every program that uses the system Python, not just ours. That's what the flag breaks.

SHOW: A GREY README tip card, header `README.md · line 56`, with the phrase "We use it here
deliberately as a quick demonstration" highlighted YELLOW.
SAY: To be fair, the README says it uses the flag deliberately, as a quick demonstration, and the next walkthrough does it properly.

SHOW: The shelves stay. Two GREY student glyphs appear at the shelf's side, each holding a jar
request: "classmate: httpx 0.13" and "you: httpx 0.28".
PONDER(8 s, "A classmate's project on this VM needs httpx 0.13.\nYours needs httpx 0.28.\nBoth install system-wide like this. What happens?")
SAY: Something to ponder. A classmate's project on this VM needs httpx 0.13, and yours needs httpx 0.28. Both install system-wide, like this. What happens?

SHOW: Both jars fly to the single `/usr/local` shelf slot named `httpx`: the 0.28 jar lands, then the
0.13 jar knocks it off. The other student's glyph turns RED. Caption: "one shelf · the last install
wins, for everyone". Fade out.
SAY: There's only one shelf, so there's room for only one httpx. The last install wins, for everyone, and one of the two projects breaks.

---

## S06 · Run it, and read the traceback — `s06_run.py` · `RunIt`

SHOW: TRACKER A9. Terminal (12.6 wide, 12 rows). It types `python3 cli.py` →
TERM(expected/10-run-default.txt: 2–15); tag `expected output`. The banner draws line by line,
then `Arguments: …`, `Input: I love cheese`, `Output: Adoro il formaggio` (the Output line
highlights GREEN). `▶ your turn`. A small GREY note: "red error? keep watching".
SAY: Step 9: run it. Type python3 cli.py, with the 3, since plain python doesn't exist here. You should see the banner, the arguments, your input, and the output: I love cheese, in Italian. If you get a long red error instead, don't change anything; we'll read ours together in a minute. Pause and try it.

SHOW: It types `python3 cli.py -t "Good morning. It is a good morning for cheese." -s "en" -d "es"`
(folds onto two rows) → TERM(expected/11-run-es.txt: 12–15); then
`python3 cli.py -t "Good afternoon. Would you like some cheese?" -s "en" -d "fr"` →
TERM(expected/12-run-fr.txt: 12–15). Tag `expected output` on each; the `-t`, `-s`, `-d` options get
small GREY labels "text", "source", "destination" on the first of the two. `▶ your turn` beside
the fr command, and a GREY note "copy from the README, quotes included".
SAY: Then the README's other two runs. Dash t gives the text, dash s the source language, dash d the destination. Copy them from the README, quotes included, and pause to run both. One comes back in Spanish, the other in French.

SHOW: The terminal clears and grows to 13 rows. Tag `real capture · 2026-10-12` on the terminal
frame. It types `python3 cli.py` → TERM(debian12-part-a/10-run-default.txt: 14–15, …, 24–26, …, 42;
wrap) (13 rows: nothing the next beats need scrolls away). The traceback lines print RED-tinted; the
last line (`RuntimeError: Translation request to Google Translate failed …`) highlights.
SAY: Now, honestly: when we recorded this, Google refused our requests, and the run ended in this long red traceback. Let's read it; you'll meet tracebacks like this all course long.

SHOW: V8. Lines 24 and 42 lift out of the terminal (which fades) and become two stacked RED boxes,
full width, text at 20 pt. Top box, labelled "1 · the cause": line 24 `Exception: Unexpected status
code "429" from ['translate.googleapis.com']`. Bottom box, labelled "2 · the wrapper": line 42
`RuntimeError: Translation request to Google Translate failed …` (folds into 3 rows). Between them,
line 26 "The above exception was the direct cause of the following exception:" as a PINK downward
arrow. A YELLOW eye glyph travels from the bottom box up to the top box; a GREY note "on your
screen: scroll up".
SAY: This is a chained traceback: two errors. The line between them says the first one directly caused the second. Most people read only the last line, but here that's just the wrapper. Scroll up to the first error: that's the cause.

SHOW: Zoom into box 1: "429" circled YELLOW, a chip "HTTP 429 = too many requests". Above, S02's V6
arrow replays: the PINK HTTPS GET reaches the BLUE `translate.googleapis.com` cloud, and the return
arrow comes back RED labelled "429".
SAY: The cause is status code 429: too many requests. Google's unofficial endpoint was rate-limiting our machine, as it often does with cloud machines. Nothing on the VM was broken.

SHOW: CODE(cli.py: 32–37) slides in under the boxes (full width); `from error` on line 37
underlines PINK and links to the PINK chain arrow between the boxes.
SAY: The error on the last line is the app's own wrapper, lines 32 to 37 of cli.py. It catches anything, and raises a friendlier message, chained to the original.

SHOW: TRACKER A9 · extra. The boxes shrink away; the terminal returns and types
`python3 cli.py -t hello -d xx` (extra; folds onto a second row) →
TERM(debian12-part-a/14-badlang.txt: 14–15, …, 21–23, …, 39; wrap) (13 rows with the folded command, in the same 13-row terminal). V8 updates: box 1 now
holds line 21 `ValueError: invalid destination language`; box 2 holds line 39 (the same
RuntimeError), with a RED "network?" question mark beside it. A GREY chip: "valid codes:
README.md · table at the bottom".
SAY: Why read the first error? This extra command has a typo: x x isn't a language. The first error says invalid destination language. But the last line still blames the network, because the same wrapper catches everything. A small flaw in the code, not in your setup. The valid codes are in a table at the bottom of the README.

SHOW: Three chips at right: "wait and retry", "a VM in another region", "run it on your laptop".
At left, the line `Input: I love cheese` (debian12-part-a/10-run-default.txt line 14) with a GREEN
check: "got this far → your packages work"; under it a small GREY note "can't open file 'cli.py'?
→ cd simple-translate". Fade out.
SAY: If you hit a 429, wait and retry, try another region, or run it on your laptop. If you got as far as the Input line, the imports worked; when the first error is a 429, only the network said no.

---

## S07 · Delete, don't stop — `s07_delete.py` · `DeleteVM`

SHOW: TRACKER A10. The schematic console (browser, tag `illustration`): the VM instances list with
the `ac215-l01` row ticked and two buttons above it, "Stop" and "Delete". A GREY README card,
header `README.md · line 62`: "A running VM keeps charging even when idle."
SAY: Step 10, the last one: delete the VM. As the README says, a running VM keeps charging, even when idle. So why delete it, and not just stop it?

SHOW: V1 coda at right: the BLUE slice with its "CPU + memory" block and its linked "disk · Debian
12" block (both from S03), GOLD meter sweeping. "Stop" is pressed: the CPU/memory block greys out,
the disk block stays BLUE, and the GOLD needle keeps a slow sweep, tag "disk: still billing". A
dashed GOLD chip "reserved IP: also billing" appears next to it.
SAY: Stopping ends the billing for CPU and memory, but the disk still exists, so it keeps billing, and so would a reserved IP address.

SHOW: "Delete" is pressed: a confirm dialog (tag `illustration`) "Delete ac215-l01? Its boot disk is
deleted with it", with a GREY tag "default · a setting on the boot disk". The slice and its disk
dissolve; the GOLD meter stops where it is (it doesn't rewind). `▶ your turn` beside the dialog.
SAY: Deleting removes the VM, and by default its boot disk goes with it. That's a setting on the boot disk, and it's on unless you changed it. And the meter stops. Select your instance, click Delete, and pause until it's gone.

SHOW: A checklist card: "VM instances: empty" and "Disks: empty", each ticking GREEN. Below, a GREY
laptop-terminal strip types `gcloud compute instances list`, then `gcloud compute disks list`
(extra; tag "optional · needs the gcloud CLI on your laptop"); no output is shown.
SAY: Then check two pages: VM instances and Disks should both be empty. With the gcloud tool on your laptop, two extra commands do the same: gcloud compute instances list, and gcloud compute disks list. Neither is in the README.

SHOW: A part-1 recap strip: BLUE VM slice → crowded ORANGE `/usr/local` shelf → RED tag "shared with
the whole OS". Then a closing card: "Part 2: the same app, on a fresh VM, the clean way", with a
small GREEN venv box. Everything fades to an empty frame (end of part 1).
SAY: That was the quick and dirty way. It worked, but it changed the system Python for every program on the machine. In part 2: the same app, on a fresh VM, the clean way.

---

## S08 · What a virtual environment is — `s08_venv.py` · `WhatIsAVenv`

SHOW: No tracker (concept scene). The ponder picture returns, without a timer: the single ORANGE
`/usr/local` shelf, two GREY student glyphs, "httpx 0.13" and "httpx 0.28". The shelf splits into
two separate GREEN toolboxes, one under each student, each labelled with its own project folder.
SAY: Back to our puzzle: two projects, two versions of httpx, one shared shelf. The fix is to give each project its own toolbox. That toolbox is a virtual environment.

SHOW: A GREEN folder `.venv/` opens at center. Part 1 appears: `bin/python`, with a GREEN symlink
arrow leaving the folder to a GREY box "a real Python interpreter, somewhere else". A small number
badge "1".
SAY: A virtual environment is just a folder, usually called dot venv, with three parts. First, a bin folder with a python inside. It's usually not a copy, just a link to a real interpreter somewhere else.

SHOW: Part 2 appears with badge "2": an empty GREEN shelf `lib/python3.X/site-packages/`. A GREY
note: "Debian's system Python: dist-packages · everywhere else: site-packages".
SAY: Second, its own site-packages folder, empty when uv makes it. Site-packages is the usual name; Debian calls its system ones dist-packages. This is where this project's packages go, and only this project's.

SHOW: Part 3 appears with badge "3": a small card `pyvenv.cfg` with the line
`include-system-site-packages = false` highlighted YELLOW.
SAY: Third, a small config file, pyvenv.cfg. When Python starts from the venv's bin folder, it reads this file. It says: you're in a venv, so use my site-packages, and leave the system's out.

SHOW: Tag `illustration` (a venv made from this same system python3). V2, ONE stack morphing in
place (no second stack): the S05 stack with short labels (Conventions), titled "python3 (system)".
The title transforms into ".venv/bin/python"; the GREY "standard library" band stays put, tagged
"from the real interpreter"; the two ORANGE dist-packages shelves slide out to the right and fade
(no RED push: pyvenv.cfg just leaves them off the list); an empty GREEN shelf
`.venv/lib/python3.X/site-packages` slides in from the left into their place. (The real paths for
our uv venv come later, in S12; the Debian 13 capture debian13-part-b/22-syspath-venv.txt is this
exact picture, same interpreter, minus the dist-packages shelves.)
SAY: Here's the difference on the shelves. Started from the venv, Python builds a different list. The standard library still comes from the real interpreter it links to. But both dist-packages shelves from the system are gone, and the venv's own shelf takes their place.

SHOW: An engine glyph labelled "interpreter" with two toolboxes that plug into it in turn: the ORANGE
system shelf, then the GREEN venv shelf. Caption "same engine, different toolbox". A thin RED
barrier appears between the two toolboxes.
SAY: Same engine, different toolbox. And the toolboxes don't mix: packages in the venv are invisible to the system Python, and the other way round.

SHOW: Line 10 of the S01 refusal (debian12-part-a/07-pip-refused.txt) fades in at the top:
"create a virtual environment using python3 -m venv path/to/venv.", `python3 -m venv` underlined
YELLOW. A PURPLE uv chip slides in beside it with the caption "today: uv makes it for us".
SAY: Remember pip's hint? It suggested python3 dash m venv, the classic way to make one. Today, uv makes it for us, and does a lot more.

SHOW: The GREEN venv box sits inside a dashed GREY box "container (L2)", inside the BLUE VM box.
Outside the venv but inside the VM, three RED-outlined chips: "the operating system", "system
libraries (C)", "GPU drivers".
SAY: What a venv doesn't isolate: the operating system, system libraries written in C, and drivers. Those are jobs for a whole machine, like our VM, or a container, next lecture.

SHOW: The three numbered parts shrink into a corner card "coming up: the real files, after uv sync"
(the card returns in S12 and ticks). Fade out.
SAY: After uv sync, we'll open the real folder and find all three parts.

---

## S09 · Installing uv — `s09_install_uv.py` · `InstallUv`

SHOW: TRACKER B1 (the tracker reappears with the part-2 section, 12 dots). The schematic create form
(tag `illustration`) fills its six rows at double speed with the S03 values; Create → the instance
row; the GOLD meter restarts its sweep, tag "billed per second while running". A small GREY glyph
"part-1 VM" with its ORANGE jars fades under a RED cross: "not this one"; a GREY note "name taken?
the old VM is still being deleted". TRACKER B2: SSH → a fresh terminal (prompt
`student@ac215-l01:~$`). `▶ your turn` beside the prompt.
SAY: Part 2 starts on a fresh VM, same settings, and the meter runs again. Fresh matters: this system Python never sees pip. Create it and SSH in; if the name is taken, the old VM is still being deleted, so wait a minute. Pause until your terminal is open.

SHOW: TRACKER B3 → B6, ticking as each command runs: `sudo apt-get update` →
TERM(debian12-part-b/01-apt-update.txt: 2, …, 8–9; +Done) → `sudo apt install git` →
TERM(debian12-part-b/02-git.txt: 25–28; [Y/n] Y, …, 160–161) →
`git clone https://github.com/dlops-io/simple-translate.git` → TERM(debian12-part-b/03-clone.txt: 2)
→ `cd simple-translate` (prompt becomes `student@ac215-l01:~/simple-translate$`). `▶ your turn`
after `cd`. A GREY note under the tracker: "no python3-pip this time", with a struck-through ORANGE
chip `sudo apt install python3-pip`.
SAY: Then the same four commands: apt-get update, install git, clone, and cd. Pause until your prompt ends in simple-translate.

SHOW: TRACKER B7. It types `curl -LsSf https://astral.sh/uv/install.sh | sh` (folds onto a second
row) but doesn't press enter yet. Four labels pop up under the flags: `-L` "follow redirects",
`-s` "silent", `-S` "but still show errors", `-f` "fail on HTTP errors".
SAY: Step 7 installs uv in one line. First, curl downloads a script: it follows redirects, stays quiet but shows errors, and fails on an HTTP error instead of handing an error page to the shell.

SHOW: The `| sh` part highlights PINK; a small script glyph flows along an arrow from curl into a
PURPLE `sh` glyph. A GREY note: "official installer · you can open the URL and read it first".
A second GREY note, from the README tip (`README.md · line 81`): "other ways: pip, brew · this VM
has no pip → use curl".
SAY: The vertical bar is a pipe: it hands the script straight to the shell, so you're running code from the internet: uv's official installer, which you can read first.

SHOW: The terminal grows to 12 rows. Enter is pressed → TERM(debian12-part-b/05-uv-install.txt: 2–10)
(12 rows). `▶ your turn`. Line 2's `uv 0.13.0` gets the tag `at the time of recording`; line 3
`installing to /home/student/.local/bin` highlights, and a PURPLE `uv` chip and a PURPLE `uvx` chip
drop into a folder glyph `~/.local/bin`.
SAY: Pause and run it. It installs uv, version 0.13.0 at the time of recording, and uvx, into dot local slash bin in your home folder.

SHOW: TRACKER B7 · extra. It types `uv --version` (extra) → TERM(debian12-part-b/06-uv-missing.txt:
2), printed RED, with a GREY tag "your shell may print -bash:".
SAY: Let's try uv, with an extra check. Command not found. But we just installed it.

SHOW: V3 (layout: see Conventions). The terminal shrinks to the bottom strip. Above it, full width,
PATH as a row of doors, left to right: `/usr/local/bin`, `/usr/bin`, `/bin`, `…` (debian12-part-b/
12-python-before.txt lines 4–8; the capture's first entry is held back for the next beat). A small
figure carrying the word `uv` starts above the first door and knocks on each door (PINK); each
stays shut. Under the row: RED "command not found".
SAY: When you type a command, the shell walks a list of folders called PATH, left to right, and runs the first match. None contains uv, and the shell only knows the PATH it started with.

SHOW: PANEL(debian12-part-b/05-uv-install.txt: 8–10, "uv installer · its last lines") above the
strip, line 10 `source $HOME/.local/bin/env (sh, bash, zsh)` highlighted YELLOW; beside it a GREY
README card `README.md · line 83`: "Reload your shell or run: …". TRACKER B8. In the strip it types
`source $HOME/.local/bin/env` → (no output). `▶ your turn` beside it. The panels fade;
PANEL(debian12-part-b/26-startup-files.txt: 14, "~/.local/bin/env · line 9") shows
`export PATH="$HOME/.local/bin:$PATH"`, and a PURPLE door `~/.local/bin` slides in at the far left
of the row (now matching 12-python-before.txt lines 3–8).
SAY: The installer's last lines, and step 8, give two options: reload your shell, or source the env file. A reload means a new SSH window, back in your home folder, so you'd cd into simple-translate again. Sourcing is quicker: it puts that folder first in PATH. Pause and run the source line.

SHOW: TRACKER B8 · extra. It types `uv --version` (extra) → TERM(debian12-part-b/07-uv-version.txt:
2), then `which uv` (extra) → TERM(debian12-part-b/07-uv-version.txt: 3). The `uv` figure walks in
through the PURPLE door.
SAY: Then two extra checks: uv reports its version, and which uv points into that folder.

SHOW: Two small shell bubbles. Left, "sh env": a child bubble gets the PURPLE door, then pops; the
parent's row is unchanged (RED cross). Right, "source env": the current shell's row gets the door
(GREEN check). Then PANEL(debian12-part-b/26-startup-files.txt: 4–5, "~/.profile line 29 ·
~/.bashrc line 115 · added by the installer"), tag "a new SSH session finds uv too".
SAY: Why source, and not sh? Plain sh would change a child shell that exits at once; source changes this one. The installer also made your startup files run this env file, so next time you connect, uv is found by itself.

SHOW: A PURPLE `uv` chip at center absorbs five GREY chips that fly into it: `python -m venv`,
`pip`, `pip-tools`, `pyenv`, `pipx`. Fade out.
SAY: So what is uv? One fast tool that replaces several: the venv module, pip, pip-tools for locking, pyenv for installing Pythons, and pipx.

---

## S10 · uv sync: which Python? — `s10_which_python.py` · `WhichPython`

SHOW: TRACKER B9. CODE(pyproject.toml: 1–10) at the top, full width. Line 2 `name = "app"` gets a
small GREY tag "remember this"; lines 7–10 bracket GREEN "2 dependencies"; `>=` on lines 6 and 8
gets a GREEN "range" tag and `==` on line 9 a GREEN "exact" tag; line 6
`requires-python = ">=3.13"` highlights YELLOW.
SAY: Step 9 is uv sync, and it reads pyproject.toml, so let's read it first. The name is app. Two dependencies: art, version 6.5 or newer, and googletrans, exactly 4.0.2. Greater-or-equal means a range; double equals, one version. Line 6 is a range again: Python 3.13 or newer.

SHOW: Beside the panel, a GREY chip "this VM: Python 3.11.2" (debian12-part-b/00-os.txt line 6) and
three answer chips: "fail?", "use 3.11 anyway?", "something else?".
PONDER(8 s, "This VM has Python 3.11.\nThe project asks for 3.13 or newer.\nWhat will uv sync do?")
SAY: Now predict. This VM has Python 3.11. The project asks for 3.13 or newer. What will uv sync do? Fail, use 3.11 anyway, or something else?

SHOW: The bottom terminal strip grows to 5 rows (the code panel moves up). It types `uv sync` →
TERM(debian12-part-b/08-uv-sync.txt: 2–5) (the remaining lines are held back for S11). `▶ your
turn`. `3.15.0` gets the tag `at the time of recording`; `(35.9MiB)` gets a GREY underline. A GREY
note: "no pyproject.toml found? → cd simple-translate".
SAY: Pause and run uv sync. Instead of failing, uv downloads its own Python: CPython 3.15.0, at the time of recording. Then it creates a virtual environment in dot venv. If uv can't find a pyproject.toml, cd into simple-translate first.

SHOW: V4 (the code panel fades): a number line with ticks 3.10, 3.11, … 3.16. A GREEN glow covers
3.13 and everything to its right, labelled `requires-python = ">=3.13"`. A dot labelled
`3.11.2 · /usr/bin/python3` drops onto 3.11 and turns RED, outside the glow. A GREY toggle
"Debian 12 | Debian 13" above the line shows Debian 12.
SAY: Here's what happened. Picture Python versions on a number line. The constraint lights up everything from 3.13 onward. First, uv looks for an interpreter it already has: its own downloads, then the system's. Debian's 3.11.2 lands outside the range, so it can't be used.

SHOW: A PURPLE download arrow drops a GREEN-ringed dot onto 3.15, labelled `3.15 (→ 3.15.0) ·
uv-managed · 35.9 MiB download`, "newest release in range (at the time of recording)" and
"~/.local/share/uv/python/". A GREEN folder chip `.venv/bin/python` draws a symlink arrow to the
new dot (two hops: `cpython-3.15` → `3.15.0`).
SAY: So uv downloads one. Which one? Not 3.13, but the newest release in the range, which was 3.15.0 when we recorded. It lives in uv's own folder in your home, and the venv's python links to it.

SHOW: The right end of the glow becomes an arrow running off the line, labelled "no upper limit".
A small caption strip below steps through: "before 3.15 existed → 3.14" · "today → 3.15.0" ·
"later → newer". Big caption: "a constraint is not a pin".
SAY: That's the catch: a constraint is not a pin. Before Python 3.15 came out, this same command gave people 3.14. Watch this video next year, and you may get something newer still.

SHOW: No split screen. The toggle flips to "Debian 13". The RED `3.11.2` dot slides right, relabels
as `3.13.5 · /usr/bin/python3`, and turns GREEN as it enters the glow; the PURPLE 3.15.0 dot and its
download arrow retract and fade; the `.venv/bin/python` symlink arrow swings to the 3.13.5 dot.
Below, the terminal strip shows TERM(debian13-part-b/08-uv-sync.txt: 2–3) with a GREY "Debian 13"
tag.
SAY: On Debian 13, the story changes. Its system Python, 3.13.5, is already inside the range. So uv simply uses it, with no download, and the venv's python links to the system one. Same command, different Debian, different Python.

SHOW: The toggle flips back to Debian 12. A chip (not a terminal) `uv python pin 3.13`, tags `extra`,
"not in the README" and a RED "not now · exercise B2", writes a small file chip `.python-version`
containing `3.13`; the GREEN glow shrinks from a half-line to the short 3.13 segment, labelled
`3.13.x`; a GREY note "pin 3.13.5 → one release". Fade out.
SAY: To get the same Python everywhere, pin it. The command uv python pin 3.13, not in the README, writes a small file called dot python version, and the range shrinks to the 3.13 series. Don't run it now: your next uv sync would rebuild the venv, and the rest of the video wouldn't match. It's in the exercises.

---

## S11 · uv sync: resolve, lock, install — `s11_lock.py` · `ResolveLock`

SHOW: TRACKER B9. The `uv sync` terminal from S10 returns (full width), showing
debian12-part-b/08-uv-sync.txt lines 2–5; below them a GREY curtain hides the rest. Above,
CODE(pyproject.toml: 7–10) with a GREEN "2" badge, and a small ORANGE chip "part 1: pip installed
12".
PONDER(6 s, "pyproject.toml lists 2 dependencies.\nHow many packages will be installed?")
SAY: Now the packages. A quick puzzle: pyproject.toml lists 2 dependencies, and in part 1, pip installed 12 packages for them. How many will uv install?

SHOW: The curtain lifts. Lines 6–8 print; `Installed 11 packages` highlights YELLOW and its "11" lifts
into a GREEN counter chip at left. Then lines 9–19 print (the terminal may scroll now), and each `+`
line is copied as a GREEN package chip into a column at left. These 11 chips become V5's nodes in
the next beat.
SAY: It's 11: one fewer than part 1. It resolved 13 and installed 11, each with a plus sign and an exact version. So where did the other 9 come from, and which one went missing?

SHOW: V5, above the bottom terminal strip: two GREEN nodes `art>=6.5` and `googletrans==4.0.2`
(pyproject.toml lines 8–9). TRACKER B9 · extra. In the strip it types `uv tree` (extra) →
TERM(debian12-part-b/17-tree.txt: 2–16), and the real tree grows from those lines (3–16): `app` at
the root; `googletrans` → `httpx[http2]` → `anyio` (→ `idna`), `certifi`, `httpcore` (→ `certifi`,
`h11`), `idna`, `h2` (→ `hpack`, `hyperframe`). The 11 GREEN chips from the previous beat move into
place as the nodes. The repeated `certifi` and `idna` rows don't create new nodes: each flies onto
the existing node as a second incoming edge. Counter under the graph: "11 packages".
SAY: Packages have dependencies of their own; this extra command, uv tree, draws them. Our googletrans needs httpx, an HTTP library, which needs anyio, certifi, httpcore, h2, and more. Two wishes grow into a tree.

SHOW: Each node gets an exact version tag that clicks into place (from 17-tree.txt: art v6.5,
googletrans v4.0.2, httpx v0.28.1, anyio v4.15.1, idna v3.20, certifi v2026.7.22, httpcore v1.0.9,
h11 v0.16.0, h2 v4.4.1, hpack v4.2.0, hyperframe v6.1.0). Then the whole tree rolls up into a GREEN
scroll labelled `uv.lock`. Captions: `pyproject.toml` "wish list", `uv.lock` "receipt".
SAY: Resolving means choosing one exact version for every package in the tree, versions that all fit together. Then uv writes them to a new file, uv.lock, with download addresses and checksums. The pyproject.toml file is your wish list. The uv.lock file is the receipt.

SHOW: The scroll unrolls back into the tree. The `app` root gets a GREY tag "the project itself ·
not downloaded". A hollow, dashed GREEN node `typing-extensions` hangs off `anyio`, its edge
labelled `python < 3.15`. PANEL(debian12-part-b/18-lock-head.txt: 6–13, "uv.lock · lines 5–12
(generated on your VM)") alone under the tree at 20 pt (13.2 wide); uv.lock line 11 (capture line
12: `{ name = "typing-extensions", marker = "python_full_version < '3.15'" },`) highlighted YELLOW.
Line 4 of the capture (`requires-python = ">=3.13"`) flashes as a GREY chip "one lock for every
allowed Python". Counter: "11 + app + typing-extensions = 13 resolved".
SAY: So why 13 resolved? It's 11 packages, plus the app itself, which uv doesn't download. The 13th is in uv.lock, which covers every Python the project allows, not just ours. In it, anyio needs typing extensions, but only on Python older than 3.15.

SHOW: The panel fades. The dashed node stays hollow: "11 on 3.15". Two small cards fill it in: a
mini part-1 shelf (debian12-part-a/08-pip-break.txt line 35, `typing_extensions-4.16.0` named)
"12 on 3.11", and a GREY "Debian 13" card (TERM(debian13-part-b/08-uv-sync.txt: 6, …, 18):
`Installed 12 packages` … `+ typing-extensions==4.16.0`) "12 on 3.13".
SAY: On our 3.15, it's skipped, so 11. Part 1 ran on Python 3.11, so pip installed it: 12. And on Debian 13, with Python 3.13, uv installs 12 too.

SHOW: Tag `illustration`. Two GREY student glyphs a week apart ("Monday", "next Monday"), each with
a copy of the tree. Without a shared scroll: some of the second student's leaf tags flip to GREY
dashed "newer?" chips (no version numbers invented). Then the GREEN `uv.lock` scroll is handed from
the first student to the second: every tag snaps to match, GREEN check.
SAY: Here's why the receipt matters. Two students run uv sync a week apart. Without a shared lock, each resolves fresh and may get different versions deep in the tree. With the same uv.lock, they get exactly the same packages.

SHOW: TRACKER B9 · extra. It types `ls -a` (extra) → TERM(debian12-part-b/09-ls-after.txt: 2–14);
`.venv` and `uv.lock` highlight GREEN with a "new" tag. Then `git status` (extra) →
TERM(debian12-part-b/19-git-status.txt: 2–9); `uv.lock` under "Untracked files" highlights YELLOW.
SAY: Two extra checks. First, ls dash a shows two new things: the dot venv folder, and uv.lock. And git status says uv.lock is untracked. It was made here; it didn't come with the repo.

SHOW: A GREY README card, header `README.md · line 70`: "`uv.lock` pins exact versions so the next
person gets the same setup", with a gentle YELLOW note "the repo has no uv.lock yet" and a GREY tag
"erratum". Two GREEN fix chips: "commit uv.lock" · "in CI: uv sync --locked". At "commit uv.lock",
the GREEN `uv.lock` scroll from V5 flies into a `simple-translate` folder glyph, captioned
`git add uv.lock`. At "locked flag", a GREY "CI" box runs `uv sync --locked`: a matching scroll gets
a GREEN check, a missing one a RED stop.
SAY: Now, a small mistake in the README, with an easy fix. It says uv.lock gives the next person the same versions. But the repo never committed one, so each student's first sync resolves fresh. In your own projects, commit uv.lock. In automated builds, run uv sync with the locked flag, which refuses a missing or stale lock.

SHOW: It types `uv sync` again (extra) → TERM(debian12-part-b/23-resync.txt: 2–3); `Checked 11
packages in 0.14ms` highlights GREEN. Fade out.
SAY: Last, an extra: run uv sync again. It checks the same packages, 11 here, in a fraction of a millisecond, and changes nothing: safe to re-run anytime.

---

## S12 · Activation is just PATH — `s12_activate.py` · `Activate`

SHOW: TRACKER B9 · extra. Terminal (12 rows). It types `ls -la .venv/bin` (extra) →
TERM(debian12-part-b/11-venv-bin.txt: 5, …, 13, 15–16, 18–19, 21; wrap) (12 rows; line 5 `activate`
stays on screen). Line 18 (`python -> /home/student/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/bin/python3.15`)
highlights with a GREEN badge "1 · the link"; lines 13, 15, 16, 21 (`art`, `httpx`, `idna`,
`translate`) get a GREY bracket "launchers from the packages"; a RED-struck ghost row `pip` appears
under the listing. The S08 three-part card returns top-right; part 1 ticks GREEN.
SAY: Let's open the venv, as promised. This extra command lists its bin folder: python, a link to the Python uv downloaded, and, notice, no pip.

SHOW: It types `cat .venv/pyvenv.cfg` (extra) → TERM(debian12-part-b/10-pyvenv.txt: 2–7). Line 6
`include-system-site-packages = false` gets badge "3"; line 7 `prompt = app` highlights YELLOW;
line 2 `home = …` highlights GREY with a tag "a folder". A small badge "2 · site-packages" points at
`.venv/lib/python3.15/site-packages` (from 22-syspath-venv.txt line 6). On the three-part card,
parts 3 and 2 tick GREEN.
SAY: And the config file: home is the real interpreter's folder, include system site packages is false, and the prompt is app. All three parts, as drawn.

SHOW: TRACKER B10. The terminal clears. It types `source .venv/bin/activate` → (no output). The next
prompt reads `(app) student@ac215-l01:~/simple-translate$`, `(app)` in GREEN. `▶ your turn`. A GREY
README card, header `README.md · line 92`, shows "(e.g. `(simple-translate) $`)" with a YELLOW note
"→ (app)" and a GREY tag "erratum"; CODE(pyproject.toml: 2) `name = "app"` slides in under it.
SAY: Step 10: source dot venv slash bin slash activate. Pause and run it. Your prompt now starts with app, in parentheses. The README's example says simple-translate. But uv names the prompt after the project, and pyproject.toml calls it app.

SHOW: V3 (layout: see Conventions), full width above the terminal strip: the doors `~/.local/bin`
(PURPLE), `/usr/local/bin`, `/usr/bin`, `/bin`, `…` (debian12-part-b/12-python-before.txt lines
3–8). First a replay of "before": a figure carrying `python` knocks on every door, and finds nothing
(RED "not found" under the row; the capture's `which python` printed nothing). Then
PANEL(debian12-part-b/25-activate-file.txt: 10–11, ".venv/bin/activate · lines 97–98") shows
`_OLD_VIRTUAL_PATH="$PATH"` and `PATH="$VIRTUAL_ENV/bin:$PATH"`; a GREEN door `.venv/bin` slides in
at the very front, and the `python` figure walks in through it.
SAY: What changed? Before activating, python knocked on every door in PATH and found nothing. The activate script saves your old PATH, then puts the bin folder of the venv first, so python is found at the first door.

SHOW: TRACKER B10 · extra. It types `which python` (extra) → TERM(debian12-part-b/13-activate.txt: 2);
`python --version` (extra) → TERM(debian12-part-b/13-activate.txt: 3), tag `at the time of
recording`, and a small GREY "Debian 13" chip TERM(debian13-part-b/13-activate.txt: 3)
`Python 3.13.5`; `which pip` (extra) → (no output; the capture's line 4 records exit status 1). A
RED "nothing" tag on the empty line.
SAY: Extra checks: which python points into dot venv, and python reports 3.15.0, at the time of recording; on Debian 13, 3.13.5. And which pip finds nothing.

SHOW: A GREY README card, `README.md · line 92`, phrase "`python` and `pip` resolve to the venv's
binaries" with a YELLOW note "a uv venv has no pip" and a GREY tag "erratum". Beside it, tag
`illustration` ("a machine with a system pip"): the PATH doors with the GREEN `.venv/bin` door in
front; a figure carrying `pip` walks past the GREEN door and in at the ORANGE `/usr/bin` door; a RED
chip "externally-managed-environment". Then a GREEN chip `uv add <package>` sends two arrows to file
chips `pyproject.toml` and `uv.lock`.
SAY: Another small mistake in the README: it says activation points pip into the venv, but a uv venv has no pip. On a machine with a system pip, which pip finds that one instead, and it refuses, as at the start. To add a package, use uv add, which also records it in pyproject.toml and uv.lock.

SHOW: TERM(debian12-part-b/13-activate.txt: 5–8) printed as a small card titled "after activation"
(PATH's first three entries and `VIRTUAL_ENV=/home/student/simple-translate/.venv`). A four-item
checklist builds: "`.venv/bin` first in PATH" · "VIRTUAL_ENV set" · "prompt (app)" · "a deactivate
command". A fifth item, RED-struck: "installs or loads packages". Then a second small terminal
labelled "new SSH window" opens beside the card: its prompt `student@ac215-l01:~$` has no `(app)`,
and its PATH row has no GREEN door; caption "activation: this shell only". It types
`cd simple-translate` and `source .venv/bin/activate`, and its prompt becomes
`(app) student@ac215-l01:~/simple-translate$`.
SAY: Activation also sets a variable called virtual env, changes the prompt, and adds a command called deactivate that undoes it all. It only changes where the shell looks first, and only in this shell. If your SSH window reconnects, cd into simple-translate and activate again.

SHOW: TRACKER B11. The terminal clears (prompt `(app) student@ac215-l01:~/simple-translate$`). It
types `python cli.py` → TERM(debian12-part-b/14-run-default.txt: 2–15); then
`python cli.py -t "Good morning. It is a good morning for cheese." -s "en" -d "es"` (folds) →
TERM(debian12-part-b/15-run-es.txt: 12–15); then
`python cli.py -t "Good afternoon. Would you like some cheese?" -s "en" -d "fr"` (folds) →
TERM(debian12-part-b/16-run-fr.txt: 12–15). Tag `real capture · 2026-10-12` on the terminal frame;
each `Output:` line highlights GREEN. `▶ your turn`, and a GREY note "copy from the README, quotes
included".
SAY: Step 11: the same three runs, now with plain python. Copy the long ones from the README, quotes included, and pause to run all three. This time Google answered: these are real translations. If you get a 429 again but see the Input line, your venv works.

SHOW: TRACKER B11 · extra. Two GREEN chips below the terminal, each with a GREY `extra` tag and the
tag "no activation needed": `uv run python cli.py` ("syncs if needed, then runs in the venv") and
`.venv/bin/python cli.py` ("call the venv's python by its path"). No output is shown for either.
SAY: Two extras, not in the README, that skip activation. First, uv run python cli.py syncs the venv if needed, then runs the app inside it. Or call the venv's python by its path.

SHOW: Line 5 of debian12-part-b/11-venv-bin.txt (`-rw-r--r-- … activate`) returns with a small GREY
tag "not executable" (no permission-bit lesson). Beside it, a small child-shell bubble gets a GREEN
door, then pops; the parent shell's row is unchanged: the S09 picture again. Fade out.
SAY: And why source, not just run the activate script? It isn't even executable, and run as a program, it would only change a child shell that exits at once, like the env file.

---

## S13 · Prove the isolation — `s13_isolation.py` · `Isolation`

SHOW: TRACKER B11 · extra. It types `deactivate` (extra) → (no output); the next prompt loses its
`(app)` (`student@ac215-l01:~/simple-translate$`). A GREY tag on the old prompt: "while active,
python3 → .venv too" (debian12-part-b/11-venv-bin.txt line 19, `python3 -> python`). It types
`python3 -c 'import googletrans'` (extra; folds onto a second row) →
TERM(debian12-part-b/20-isolation.txt: 2–4); `ModuleNotFoundError` in RED.
SAY: Let's prove the isolation with a few extras. Deactivate first: while the venv is active, even python3 points into it. Then ask the system's python3 to import googletrans. ModuleNotFoundError. On this VM, the packages exist only in the venv.

SHOW: V2 (short labels), above the terminal strip: the system python3 stack of this VM (GREY
"standard library" band for 3.11, two ORANGE dist-packages shelves with no googletrans jar). The
PINK search-light labelled `import googletrans` sweeps every shelf, top to bottom, and finds
nothing. To the right, the GREEN venv shelf with its `googletrans` jar sits apart, not connected to
the stack.
SAY: On the shelves: the system Python scans its own list, top to bottom. The venv's shelf isn't on that list, so the search comes up empty.

SHOW: It types `uv run python -c 'import googletrans, sys; print(sys.prefix)'` (extra; folds onto a
second row) → TERM(debian12-part-b/21-uv-run.txt: 2). The printed path
`/home/student/simple-translate/.venv` highlights GREEN; the search-light jumps to the GREEN shelf
and finds the jar.
SAY: Now the same import through uv run, printing where this Python thinks it lives. It works, and the answer is our dot venv folder.

SHOW: Faint in the background, a GREY VM glyph labelled "part-1 VM" (no shelves: they are the
answer).
PONDER(6 s, "Same import, on your part-1 VM, after deactivate.\nDoes it work?")
SAY: Now imagine you'd kept your part-1 VM. Same import, system python3, no venv. Does it work?

SHOW: The part-1 VM glyph opens into its shelves (short labels). The PINK search-light sweeps down
and stops on `googletrans` on the `/usr/local/… (pip's)` shelf (ORANGE), with the line from
debian12-part-a/09-where.txt line 2 as its label and a GREY tag "system-wide".
SAY: Yes: on that VM, sudo pip put googletrans on the system-wide user local shelf, so every program finds it. Same import, different shelves, different answer.

SHOW: The part-1 stack slides left to half width; a GREEN venv stack (three shelves: current folder,
standard library, `.venv/…/site-packages`) builds at right; its search-light runs down its own three
shelves only and never touches the ORANGE ones. Caption: "a venv ignores whatever the system Python
has". Fade out.
SAY: And it works the other way too. Even on that messy part-1 VM, a venv would ignore everything sudo pip put there, because those shelves aren't on its list. That's the whole lesson in one picture.

---

## S14 · The older way: pipenv — `s14_pipenv.py` · `Pipenv`

SHOW: No tracker. Two branch chips: `main` (GREEN) and `pipenv` (GREY), the latter with a small note
"older version of this tutorial". Beside them, two GREY repo chips that also use pipenv:
`simple-translate-aws` "AWS track" and "cheese-app-v0 · api-service (later)".
SAY: One more tool you'll meet: pipenv, an older way to do the same job. This repo's pipenv branch, an older version of this tutorial, uses it. So do the separate AWS version and, later, the cheese app's API service.

SHOW: Two columns, uv (left, GREEN/PURPLE) and pipenv (right, GREY), with a GREY tag "just read: no
pipenv on this VM". Rows morph across one at a time, as the SAY names them: `pyproject.toml` ↔
`Pipfile`; `uv.lock` ↔ `Pipfile.lock`; `.venv/` "in the project" ↔
`~/.local/share/virtualenvs/<name>-<hash>` "in your home"; `uv sync` ↔ `pipenv install` /
`pipenv sync`; `source .venv/bin/activate` ↔ `pipenv shell` (tag "a subshell · type exit to
leave").
SAY: Same ideas, different names. The pyproject.toml file becomes the Pipfile, and uv.lock becomes Pipfile.lock. The venv lives in a folder in your home instead of in the project. The command uv sync becomes pipenv install, or pipenv sync. And instead of activating, pipenv shell opens a new shell inside the venv. Type exit to leave it.

SHOW: Two chips side by side: "pipenv branch · Pipfile.lock: httpx 0.13.3" (from
`assets/source/pipenv-branch/Pipfile.lock` line 94, `"version": "==0.13.3"`) and "main · our uv
sync: httpx 0.28.1" (debian12-part-b/08-uv-sync.txt line 17, tag `at the time of recording`).
Between them, the S05 ponder picture flashes: one ORANGE shelf with a RED cross; then two GREEN
toolboxes with a GREEN check. Fade out.
SAY: And here's our puzzle again, for real. That branch's lock file pins httpx 0.13.3, while our uv sync installed 0.28.1, at the time of recording. Two versions of the same app, two versions of httpx. On one shared system Python, they couldn't live together. In two venvs, they can.

---

## S15 · Tear down, recap, and what's next — `s15_recap.py` · `Recap`

SHOW: TRACKER B12. The schematic console (tag `illustration`): `ac215-l01` ticked → Delete → the
confirm dialog "Delete ac215-l01? Its boot disk is deleted with it" (as in S07). V1: the BLUE slice
and its disk dissolve; the GOLD meter stops where it is. A checklist: "VM instances: empty" ·
"Disks: empty", ticking GREEN. `▶ your turn`.
SAY: Step 12: delete the VM, with its boot disk, then check that VM instances and Disks are both empty. Pause and do it now, before you forget.

SHOW: V7. A BLUE box "VM" containing a GREEN box "venv". Labels appear as they're said: VM "a whole
machine: wreck it, delete it"; venv "one project's Python packages". Between the two boxes, a GREY
dashed box "container · L2" fades in.
SAY: Here's where we are. The VM gave us a whole machine that we can wreck and delete. The venv keeps one project's packages away from that machine's Python. And between the two, there's room for one more layer.

SHOW: The dashed box turns solid (still GREY, tag "L2"). CODE(Dockerfile.txt: 21–29) slides in at
right: line 22 `COPY . ./` highlights, then line 24 `RUN uv sync` (GREEN), then line 29
`CMD ["-c", "source .venv/bin/activate && exec bash"]` (GREEN).
SAY: That layer is a container, and it's next lecture. The tutorial's Dockerfile already shows the idea: copy the code, run the same uv sync, and start in a shell with the venv activated. Everything you did today, baked into an image.

SHOW: CODE(Dockerfile.txt: 2) `FROM python:3.12-slim-bookworm` beside CODE(pyproject.toml: 6)
`requires-python = ">=3.13"`; between them a YELLOW "?" and the S10 number line in miniature, with
3.12 just outside the glow.
SAY: One thing to watch for next time. The Dockerfile starts from a Python 3.12 image, but the project wants 3.13 or newer. You already know what uv will do about that.

SHOW: A card titled "Test yourself", questions appearing one at a time (each stays as the next
fades in below, smaller): Q1 "What does --break-system-packages break, and where did sudo pip3 put
the files?" Beside it, its picture returns as a small thumbnail and plays one motion: pip's jars
landing above apt's.
SAY: Before you go, five questions to test yourself. One: what does the break-system-packages flag actually break, and where did sudo pip3 put the files?

SHOW: Q2 "Name the three parts of a venv." (thumbnail: the three-part venv card) Q3 "What does
activation change? Name two ways to run the app without it." (thumbnail: the GREEN door sliding to
the front of PATH)
SAY: Two: name the three parts of a virtual environment. Three: what exactly does activation change, and what are two ways to run the app without it?

SHOW: Q4 "pyproject.toml lists 2 dependencies. Why were 11 packages installed, and which file makes
everyone get the same ones?" (thumbnail: the tree rolling into the uv.lock scroll) Q5 "Is `>=3.13`
a pin? What would make the Python version deterministic?" (thumbnail: the glow shrinking to the
3.13 segment)
SAY: Four: 2 dependencies became 11 packages. Why, and which file makes everyone get the same ones? Five: is requires Python 3.13 or newer a pin, and what would make the version deterministic?

SHOW: The questions shrink to the top. Two footer cards: "Answers: exercises.md" and "Study guide +
every command: github.com/JunyiZhou-Conny/MLOps_Learning · guides/L01-vms-venvs.md". Then
everything fades to an empty frame (end of part 2).
SAY: The answers are in the exercises. Every command from today is in the study guide, in the MLOps Learning repo. Next time: containers.
