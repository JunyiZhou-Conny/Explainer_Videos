# L11 script review · lens 3 · follow-along completeness

Reviewed: `script.md` at `1da63fa` (branch `claude/ac215-l09-l13-batch`). Checked against
`assets/source/data-labeling/README.md` (@ `03c3e27`, which is also today's HEAD, `laptop/02`),
`assets/source/data-versioning/README.md` lines 1–425 (@ `b240b1a`, route S, the course pin), the
starter's own `data-versioning@data-versioning-ac215/README.md` (line 148 only, for the S14 beat),
today's `data-versioning@2515e5e/README.md` (the erratum beat), the starter's scripts, the Colab
cell extract `notebook-1RRQ1SlH.cells.txt`, `BRIEF.md` (trackers A–L, README checklist, teardown),
`ASSETS.md`, and line 1 plus every cited line range of the captures in `assets/terminal/`.

Summary: every README instruction in both tutorials is on screen. Every README command is typed
byte for byte as the README spells it. The only substitutions are `YOUR_BUCKET_NAME` →
`your-bucket-placeholder` (README card beside it) and the token after `-k`, which the README leaves
to you. Every extra matches its capture's line 1, and every cited TERM line range matches its
capture. README order holds, with two deviations, both narrated: Colab `dataset_v20` (J6) moves to
S15, and S05 checks both storages before it adds and syncs them. All twelve trackers match the BRIEF
(52 steps, no skip or duplicate). Both Linux fixes carry the `extra · Linux` tag and say "an extra,
for Linux". The 401 legacy-token fix is on screen (`27` → wireframe + `43` → `44`).

**Could a viewer with their own clones, pausing at each tag, finish both tutorials? Not quite.**
There are two blockers. First, S09 never leaves `~/data-labeling` before the clone. A follower's
`data-versioning` then lands inside `data-labeling`, `../secrets` points at nothing, and the errors
they get look exactly like the video's own stand-in errors, so nothing warns them (F1). Second, the
legacy-token fix has no your-turn beat, and it never shows *where* the legacy token appears once
enabled. Label Studio 1.23 shows a Personal Access Token by default, so a follower who re-runs with
that token gets the 401 again (F2).

Seven confusing items follow. The compose and v21 sections never say "pause" (F3, F4). The Colab ▶
comes before the instructions to use your own URL, your own tag and a token for a private repo (F5).
Teardown has gaps (F6). Viewers with no SSH key cannot push (F7). Nothing tells viewers which README
version the video follows; today's GitHub README and its Colab link differ (F8). The Linux `chown`
fix has no ▶ (F9). Nine polish items close the list. Seven ▶ blocks have no spoken "pause" (F10, part
of F3/F4).

## Findings

**F1 · S09 · wrong · the clone runs in `~/data-labeling`, not beside it.**
S08 ends at `student@laptop:~/data-labeling$`: `sudo ls -la docker-volumes/label-studio` (`64`) is
relative to that folder. S09's G1 block then shows `student@laptop:~$` with no `cd` on screen. A
follower who copies the screen runs README:81's clone inside `data-labeling`. That gives
`~/data-labeling/data-versioning`, nested in another git repo. Its `docker-shell.sh:6`,
`SECRETS_DIR=$(pwd)/../secrets/`, then resolves to `~/data-labeling/secrets`, which does not exist.
Docker mounts an empty folder there. Every cloud step fails with `Unable to read file
[/secrets/data-service-account.json]`, which is exactly the failure the video presents as its
expected stand-in result (`88:32`). The follower has no way to tell they went wrong. S10's tree
(`84`) would show the mismatch, but only after the clone and first push.
*Fix:* open G1 with a typed `cd ..` (no output) and the prompt changing to `student@laptop:~$`, as
S02 and S10 do. Add to the G1 SAY: "From the folder that holds data-labeling and secrets, the
data-versioning README starts with the same three cleanup commands." README:136 ("next to your
data-versioning folder") is the README's own justification. Put it on a small README card.

**F2 · S07 · wrong · the legacy-token fix is required but has no ▶, and nothing shows where the legacy token is.**
With Label Studio's defaults at 1.23.0 (`27`: `"legacy_api_tokens_enabled":false`), every follower's
README:198 fails (`42`). That makes the fix a step everyone must run before the video goes on.
Rule 2 needs a ▶ and a spoken "pause" there. The D2 · extra block (script L626–633) has neither. Its
last instruction, "then copy the legacy token", is spoken but not drawn. ASSETS (L272–277) notes that
1.23.0 shows a *Personal Access Token* (a JWT) on Account & Settings by default. D1's wireframe draws
one blank field, so the follower most likely copied the PAT. If they paste the same string again,
they get the same 401. The capture shows the 401 for a legacy-format token; the PAT case was not run,
so its exact text is unverified.
*Fix:* after the toggle beat, show the *Account & Settings* wireframe again with two labelled
sections, "Personal Access Token" and "Legacy Token". Highlight the legacy one with its value blank,
and add `▶ your turn`. Add to the SAY: "Pause: enable legacy tokens, then copy the legacy token, not
the personal one." Check the section names against the 1.23 UI before drawing them. If they cannot be
confirmed, label them "legacy token" and "personal access token" in lower case and tag
`illustration`. Optionally add a GREY chip on D1: "on 1.23 this page shows a personal access token ·
scene 7 explains".

**F3 · S14 · confusing · upload, `dvc add` and `dvc push` for v21 never say "pause", and the container restart is never mentioned.**
K1 (L999) and K2/K3 (L1011, "`▶ your turn` on each README command") carry ▶ tags, but neither SAY
says "pause". The first spoken pause in S14 is at K4's git block. The follower also left the
container in S13 to run git (`95:82`, README:312). K2's typed `sh docker-shell.sh` (`104`, the
README's own command, re-used) is not narrated. README:348 only says "Inside the container, run". The
conventions' GREY chip ("same entrypoint errors as before") describes our capture, not a follower
with a real key.
*Fix:* K1 SAY ends: "Pause and upload one or two." K2/K3 SAY opens: "Start the container again with
sh docker-shell.sh, list the folder, then dvc add and dvc push; pause and run them." That also
covers the F10 note on S12's silent re-entry (L878).

**F4 · S08 · confusing · the compose Extra has no spoken pause, and nothing returns the follower from the CLI container.**
E1 (L652–659) types `docker stop data-label-studio`, `docker ps` and the first compose run with no ▶
and no pause. E2 (L661–666) has a ▶ but its SAY has no "pause". The follower also ends S07 at the
CLI container prompt (`app@…:/app$`, L643). `docker stop` typed there gives `docker: command not
found`. README:218 says "stop all containers", which here also means "exit the CLI container".
*Fix:* open E1 with a typed `exit` at the S07 prompt (`41:112` is a real capture of it; the
container is `--rm`). Add to the SAY: "Leave the command line container with exit, stop Label
Studio, and check with docker ps; pause and do it." Then in E2: "Pause, remove it, and run the
compose script again."

**F5 · S15 · confusing · the Colab ▶ comes before what a follower needs to make the notebook work.**
The ▶ "Pause and work through it" (L1061–1069) comes before the instructions to replace the address
and the tag and the warning about the private repo (L1080–1086). The notebook as shown points at the
class repo. README:108 made your repo **private**, so Colab's `dvc get` cannot clone it without a
credential. The only fix given, "an access token in the address, or a public repo", is spoken one
block later and points to exercises. A follower who pauses at the ▶ gets a 401 from the class bucket
(`C13`) or a git authentication failure on their own repo. Neither appears on screen as theirs.
*Fix:* move the ▶ and "Pause and work through it" to the end of the `recorded` block. Show the
edited cell 13/15 form on the notebook frame:
`!dvc get https://github.com/YOUR_GITHUB_USERNAME/data-versioning cheese_dataset --force --rev dataset_v20`.
Add a GREY chip with the private-repo form,
`https://YOUR_GITHUB_USERNAME:<read-only token>@github.com/YOUR_GITHUB_USERNAME/data-versioning`,
as an `illustration` placeholder (never a real-looking token). Keep "or make it public for this
step" as the simpler route.

**F6 · S16 · confusing · teardown is incomplete in four places.**
(a) **CORS.** The `python cli.py -r` line is on the card only and is never spoken. It also cannot
run as written: S08's prune deleted `data-labeling-network` (`62:10–13`), and
`docker-shell-CLI.sh:17` joins that network without creating it (digest §6 item 7: `network
data-labeling-network not found`). (b) **The first card line, "stop and remove data-label-studio",
is stale.** S08's stop + prune already removed it (`61`, `62:9`), and S16's own `150` shows no
containers. (c) **Key.** The card gives the IAM path and the SAY says "Delete the key when you are
done". Neither says to delete `secrets/data-service-account.json` too. The card's "when the course is
done" and the SAY's "when you are done" also disagree. (d) **`docker-volumes/label-studio` on
Linux** is owned by 1001 and `docker-volumes` by root (`14`, `16`), so deleting it needs `sudo`.
Optional: the three images (~6 GB, `152`) are kept by prune, and the card never says so.
*Fix:* replace card line 1 with "containers and the labeling network: already gone (scene 8)". Spell
the CORS line as runnable: "keeping bucket 1? in data-labeling: `sh docker-shell.sh`, then
`sh docker-shell-CLI.sh`, `python cli.py -r`, `exit` · deleting the bucket removes its rule too".
Say it once: "If you keep the labeling bucket, remove its CORS rule with dash r." Use "delete the
key and its JSON in secrets when the course is done" on both card and SAY. Add "(sudo on Linux)" to
the volume line. Optional GREY line: "`docker image rm data-label-cli data-version-cli
heartexlabs/label-studio:latest` frees about 6 GB".

**F7 · S09 · confusing · a follower with no SSH key can clone but not push.**
The video teaches "no SSH route → clone over HTTPS, which the README allows" (`74`). It then types
README:122's `git remote add origin git@github.com:YOUR_GITHUB_USERNAME/data-versioning.git` and
says "Your repo now shows the 7 files on main". A follower who cloned over HTTPS because they have no
SSH key gets `Permission denied (publickey)` on `git push -u origin main`, and again on both atomic
pushes (S13, S14). The video describes success, so they have no route forward.
*Fix:* one GREY chip on G5, `illustration`, no panel: "no SSH key? use
`https://github.com/YOUR_GITHUB_USERNAME/data-versioning.git` as origin · GitHub asks for a token,
not your password". Keep the README's SSH line as the typed command.

**F8 · S09 / S10 / S15 · confusing · the viewer is never told which README version the video follows.**
The data-versioning tracker chip says "README @ b240b1a · the course pin", but there is no address. A
viewer has three README versions in front of them. GitHub's front page is today's `2515e5e`. Their
clone holds the old starter README (165 lines, with the line-148 slip). The video follows `b240b1a`.
Today's README differs where it matters. It says clone `main`, which the video covers. It adds the
"upload some pictures" sentence (today's :254), so S10's "the README never says" is true only of the
pin. Its Colab links (:350, :407) open a **different notebook**, `18KYngbv` (ASSETS L89, L103), which
is not the `1RRQ1SlH` frame S15 shows.
*Fix:* at G1, a GREY chip with the pinned address,
`github.com/dlops-io/data-versioning/blob/b240b1a/README.md`, and "the study guide links it" (check
that the short hash resolves). In S10, say "the course's README never says…". In S15, a GREY chip:
"today's README links a newer copy of this notebook · same cells · point them at your repo either
way".

**F9 · S04 · confusing · the Linux `chown` fix has no your-turn beat.**
On a Linux engine every follower's Label Studio exits within 25 s (`12`). Their `sh
docker-shell.sh` only stays up after `16`. The block (L446–451) types the fix, the README re-run and
`docker container ls`, but has no ▶ and no "pause". The caption stays `B1 · extra` while the README's
own B1/B2 commands are re-run.
*Fix:* add `▶ your turn` on the re-run, with SAY "On Linux, pause and do the same." Caption the
`chown` line `TRACKER B1 · extra · Linux` (see F18). Move the tracker back to B2 for `18`.

**F10 · S05, S09, S10, S11, S12, S13 · polish · ▶ tags whose block never says "pause".**
These are separate from F3 and F4. S05 block 2 (L485, ▶ "on the source form and on the target
form"). S09 G3 (L737, `rm -rf .git` / `git init`). S10 H1/H2 (L764, reuse the key). S13 J5 block 3
(L966, `git status` / add / commit, while the pause comes with tag/push). Two re-runs also have no
your-turn beat: S11's rebuild after the Dockerfile fix (L832, "Run it again") and S12's restart after
the `safe.directory` fix (L878).
*Fix:* S05 b2: drop the ▶ (block 4's "Pause, add both, and sync" is the checkpoint; mention the
target's own *Add Target Storage* button there). S09 G3: "Pause and run both." S10 H1: drop the ▶,
or say "Pause if you need a new key." S13 b3: drop the ▶ and let block 4's single ▶ cover git ×5.
S11: add ▶ to the rebuild, "Pause and run it again; the first build is slow." S12: "Start the
container again; now dvc init works."

**F11 · S11 · polish · the Dockerfile `sed -i` has no "our editor" chip, and it fails on macOS.**
`87`'s `sed -i '36s/google-cloud-sdk/google-cloud-cli/' Dockerfile` is GNU syntax. BSD sed on a Mac
reads `36s/…/` as the backup suffix and errors. The edits at `40` and `85` carry "our editor; use
yours", but this one does not.
*Fix:* add the same GREY chip, and show the resulting line 36 (`87:2`) large as "your new line 36".

**F12 · S14 · polish · with a real mount, the time-travel extra rewrites the bucket.**
`cheese_dataset` is the bind-mounted bucket folder `images/`. With a working gcsfuse mount, `dvc
checkout` at v20 would delete `Image_5.jpg` from the bucket (`115`: "Applying changes … M
cheese_dataset/"), and checking `main` back out would re-upload it. The SAY says "Both come straight
from the cache on your disk", which is true for the bytes but hides the side effect.
*Fix:* GREY chip on `115`: "with a real mount this rewrites images/ in your bucket · it comes back
when you check out main".

**F13 · S08 · polish · `docker-shell-compose.sh:12` calls `docker-compose`.**
Docker Desktop ships that compat command, and so did the capture engine (ASSETS L384). Linux
installs with only the compose plugin get `docker-compose: command not found` (digest gotcha 8; the
BRIEF sends it to exercises).
*Fix:* a GREY chip beside the E2 command: "docker-compose: not found? `docker compose run --rm
--service-ports data-label-cli`".

**F14 · S12 · polish · Route T followers are told "start from the starter" but not how to rejoin.**
A follower who cloned `main` has already pushed `main`'s 11 files to their GitHub repo (route T,
`142`/`143`). Restarting at S09 with a fresh `git init` makes `git push -u origin main` a
non-fast-forward rejection.
*Fix:* add to the GREY "if you cloned main" chip: "rewind to scene 9 · recreate your empty GitHub
repo first".

**F15 · S07 · polish · README:187 "Open a json file to see what the annotations look like" is not said.**
C6 is shown and narrated, but the open-a-file step is not. It is the README's own way to see the
WHITE envelope the scene animates.
*Fix:* add to the C6 SAY: "Open one to see the note." No ▶ is needed.

**F16 · S02, S03, S10 · polish · `tree` and `md5sum` are not on a Mac by default.**
Both are extras (`05`, `84`, `09b`). `09b`'s md5s set up the part-2 payoff that a follower may want
to check.
*Fix:* GREY chips: "no tree? `ls` shows the same" (S02, S10); "macOS: `md5 -r`" (S03).

**F17 · S12 · polish · the class-repo comparison cannot be reproduced from the screen.**
The strip says "cloned as class-data-versioning (extra)", but `119` is never shown, so its clone
command is missing too. Hiding the head-date output is right.
*Fix:* type `119`'s line 1 with no output panel, in the second-terminal strip before `120`.

**F18 · S04, S08, S12, S14 · polish · tracker captions.**
The conventions define caption variants, but the Linux steps are written `TRACKER B1 · extra (tag
extra · Linux)` and `TRACKER J1 · extra (tag extra · Linux)`, which leaves the caption unclear. The
extras `55` (S08, under `TRACKER F1`) and `113` (S14, no TRACKER line) have no `· extra` caption.
S05 runs the tracker B5 → B6 → B5.
*Fix:* write `TRACKER B1 · extra · Linux` and `TRACKER J1 · extra · Linux`; caption `55` as
`F1 · extra` and `113` as `K4 · extra`. S05's back-step is acceptable once F10 moves the single ▶
to block 4.

## Tracker arithmetic

| tracker | N | steps placed | result |
| --- | --- | --- | --- |
| A | 6 | A1, A2 S02 · A3–A6 S03 (+ A1/A3/A4 · extra) | ✓ |
| B | 6 | B1, B2 S04 (+ B1/B2 · extra) · B3, B4 S04 · B5, B6, B5 S05 | ✓ (back-step, F18) |
| C | 6 | C1–C4 S06 · C5, C6 S07 | ✓ |
| D | 3 | D1–D3 S07 (+ D1/D2/D3 · extra) | ✓ |
| E | 2 | E1, E2 S08 (+ E2 · extra) | ✓ |
| F | 4 | F1–F4 S08 (+ F4 · extra) | ✓ (`55` caption, F18) |
| G | 5 | G1–G5 S09 | ✓ |
| H | 3 + extra row | H1–H3 S10 · H3 · extra "upload the first photos" | ✓ |
| I | 3 + extra row | I1 S10 · I2, I3 S11 · I3 · extra "Dockerfile:36 fix" | ✓ |
| J | 6 | J1–J3 S12 · J4, J5 S13 · J6 noted S13, shown S15 | ✓ (deferral narrated) |
| K | 5 | K1–K4 S14 · K5 S15 | ✓ |
| L | 3 | L1–L3 S16 | ✓ |

The step lists in the script's Conventions match BRIEF L231–256 word for word. S01, S09's opening
and S16's monitoring and recap beats have no tracker, as the BRIEF specifies.

## Teardown (what the viewer ends with)

- **Gone:** `data-label-studio` (stop `61` + prune `62:9`); `data-labeling-network` (`62:10–13`,
  said in S08); the CLI, compose one-off and DVC containers (`--rm`).
- **Kept on purpose, said:** `docker-volumes/label-studio` (S08 ponder, S16 card); `dvc_store/` (RED
  line, card + SAY).
- **Billing, said:** bucket folders `cheeses_unlabeled/`, `cheeses_labeled/`, `images/` (card + SAY).
- **Gaps:** the CORS rule (card only, cannot be run after prune); the key's local JSON; the card's
  stale first line; `sudo` for the volume on Linux; images ~6 GB not mentioned (all F6).

## Appendix · README command checklist

Legend: ✓ present, exact and in order · ✗ gap · ▶ has a your-turn tag · "no pause" = ▶ tag but the
block's SAY never says pause.

**data-labeling README @ `03c3e27`**

| # | README line | instruction (verbatim where it is a command) | scene / tracker · SHOW | exact | ▶ | status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 14 | Cloned this repository (URL, no command) | S02 · A1 `git clone https://github.com/dlops-io/data-labeling` (= `01`) + `cd data-labeling`, README card | n/a (ours) | ▶ | ✓ |
| 2 | 18 | Docker > Preferences > Resources > 4GB | S02 · A1 README card, `erratum`, "now Settings" | n/a | – | ✓ |
| 3 | 31–40 | `secrets` folder beside `data-labeling` | S02 · A2 `cd ..`, `mkdir secrets` (chip), extra `tree -L 1 .` | n/a | ▶ | ✓ (F16) |
| 4 | 44–50 | `data-service-account`, Storage Admin, KEYS → ADD Key → JSON, rename | S03 · A3 console `illustration` | names exact | ▶ | ✓ |
| 5 | 64 | Download the unlabeled data | S03 · A4 `curl -sSLO …/v4.0/cheeses_unlabeled.zip && ls -l …` (chip) = `07` | URL exact | ▶ | ✓ |
| 6 | 65 | Extract the zip file | S03 · A4 `unzip cheeses_unlabeled.zip` (chip) = `08` | n/a | ▶ | ✓ |
| 7 | 69–72 | Bucket (REPLACE WITH YOUR BUCKET NAME) + `cheeses_unlabeled` + `cheeses_labeled` | S03 · A5 `illustration`, GOLD | names exact | ▶ | ✓ |
| 8 | 76 | Upload the images into `cheeses_unlabeled` | S03 · A6 `illustration` (21 images only) | n/a | ▶ (shared) | ✓ |
| 9 | 86 | Be inside `data-labeling` | S04 · B1 `cd data-labeling` | n/a | – | ✓ |
| 10 | 87 | `sh docker-shell.sh` | S04 · B1 = `10` | ✓ | ▶ | ✓ |
| 11 | 91 | `docker container ls` | S04 · B2 = `11` | ✓ | ▶ | ✓ |
| 12 | — | Linux fix `sudo chown -R 1001 docker-volumes/label-studio && ls -la docker-volumes` + README re-run | S04 · B1 · extra, tag `extra · Linux` = `16`, `17`, `18` | ✓ (= line 1) | **none** | ✗ F9 |
| 13 | 108–109 | Open `http://localhost:8080/`, log in | S04 · B3 `illustration` + stand-ins `23`, `24` | ✓ | ▶ | ✓ |
| 14 | 110–115 | Create Project, Image Classification, four labels, Save | S04 · B4 `illustration` + `28` | labels exact | ▶ | ✓ |
| 15 | 121–133 | Settings → Cloud Storage → Add Source Storage (fields) | S05 · B5 form `illustration` | values exact (bucket = placeholder) | – | ✓ |
| 16 | 134 | Check Connection | S05 · B5 stand-in `30` (+ extra `29`) | n/a | ▶ no pause | ✓ (F10) |
| 17 | 138–146 | Add Target Storage (fields), Check Connection | S05 · B6 `illustration` + `31` | prefix exact | ▶ no pause | ✓ (F10) |
| 18 | 135–136, 147 | Add Storage, Sync Storage; Add Target Storage | S05 · B5 block 4 (`recorded` 21 tasks, stand-in `32`) | n/a | ▶ | ✓ (order narrated) |
| 19 | 164 | Change the bucket name in `docker-shell-CLI.sh` | S06 · C1 sed (chip "our editor") = `40` | n/a | ▶ | ✓ |
| 20 | 165 | Run `docker-shell-CLI.sh` | S06 · C2 `sh docker-shell-CLI.sh` (chip) = `41` | ✓ | ▶ | ✓ |
| 21 | 167 | `python cli.py -c` | S06 · C3 `41:32` | ✓ | ▶ | ✓ |
| 22 | 168 | `python cli.py -m` | S06 · C4 `41:67` | ✓ | ▶ | ✓ |
| 23 | 174–177 | Annotate a few images | S07 · C5 `illustration` + `33` | n/a | ▶ | ✓ |
| 24 | 184–186 | View `cheeses_labeled` in the GCS browser | S07 · C6 `illustration` | n/a | – | ✓ |
| 25 | 187 | Open a json file | not said | n/a | – | ✗ F15 (polish) |
| 26 | 193–196 | Account & Settings → copy the Access Token | S07 · D1 wireframe | n/a | ▶ | ✓ (1.23 shows a PAT: F2) |
| 27 | 197 | Go to the shell in the container | S07 · D2 chip "stay in yours" | n/a | – | ✓ |
| 28 | 198 | `python cli.py -p -k` + token | S07 · D2 `python cli.py -p -k student-demo-token-not-a-secret` = `42:32` → 401 | ✓ | ▶ | ✓ |
| 29 | — | Fix: enable legacy tokens, copy the legacy token | S07 · D2 · extra, `27` + wireframe + `43` | n/a | **none** | ✗ F2 |
| 30 | 198 | re-run `-p` | S07 · D2 `44:32` | ✓ | ▶ | ✓ |
| 31 | 199 | `python cli.py -t -k` + token | S07 · D3 `44:37` | ✓ | ▶ | ✓ |
| 32 | 218 | Stop all containers | S08 · E1 (CLI container never exited) | n/a | – | ✗ F4 |
| 33 | 225 | `docker stop <container_name_or_id>` | S08 · E1 `docker stop data-label-studio` (chip) = `50` | ✓ (name filled in) | – | ✗ F4 |
| 34 | 229 | `docker ps` | S08 · E1 = `51` | ✓ | – | ✗ F4 |
| 35 | 218 | run `docker-shell-compose.sh` | S08 · E2 `sh docker-shell-compose.sh` (chip) = `52`; extra `docker rm` `53`; again `54` | ✓ | ▶ no pause | ✗ F4 (F13) |
| 36 | 243 | `docker container ls` | S08 · F1 = `60` | ✓ | ▶ | ✓ |
| 37 | 244 | Stop any container that is running | S08 · F2 `docker stop data-label-studio` = `61` | ✓ | ▶ | ✓ |
| 38 | 245 | `docker system prune` | S08 · F3 = `62` | ✓ | ▶ | ✓ |
| 39 | 246 | `docker image ls` | S08 · F4 = `63` | ✓ | ▶ | ✓ |

**data-versioning README @ `b240b1a`** (route S, the starter at `23762e4`)

| # | README line | instruction | scene / tracker · SHOW | exact | ▶ | status |
| --- | --- | --- | --- | --- | --- | --- |
| 40 | 57 | `docker container ls` | S09 · G1 = `70` (prompt `~$` with no `cd ..`) | ✓ | ▶ | ✗ F1 |
| 41 | 60 | Stop any container that is running | S09 · G1 (none running, `70`) | n/a | ▶ | ✓ |
| 42 | 65 | `docker system prune` | S09 · G1 = `71` | ✓ | ▶ | ✓ |
| 43 | 71 | `docker image ls` | S09 · G1 = `72` | ✓ | ▶ | ✓ |
| 44 | 81 | `git clone -b data-versioning-ac215 git@github.com:dlops-io/data-versioning.git` | S09 · G2, typed, no panel | ✓ | ▶ | ✓ (location: F1) |
| 45 | 84 | "Alternatively, you can clone with HTTPS" | S09 · G2 extra `git clone -b data-versioning-ac215 https://github.com/dlops-io/data-versioning.git` = `74` | ✓ (= line 1) | ▶ | ✓ |
| 46 | 89 | `cd data-versioning` | S09 · G3 | ✓ | ▶ | ✓ |
| 47 | 95 | `rm -rf .git` | S09 · G3 = `76` | ✓ | ▶ no pause | ✓ (F10) |
| 48 | 101 | `git init` | S09 · G3 = `77` | ✓ | ▶ no pause | ✓ (F10) |
| 49 | 106–110 | Private GitHub repo `data-versioning`, no README/licence/.gitignore | S09 · G4 `illustration` | ✓ | ▶ | ✓ |
| 50 | 121 | `git branch -M main` | S09 · G5 = `79` | ✓ | ▶ | ✓ |
| 51 | 122 | `git remote add origin git@github.com:YOUR_GITHUB_USERNAME/data-versioning.git` | S09 · G5 = `80` | ✓ | ▶ | ✓ (no-SSH followers: F7) |
| 52 | 123 | `git add .` | S09 · G5 = `81` | ✓ | ▶ | ✓ |
| 53 | 124 | `git commit -m "Initial commit"` | S09 · G5 = `82` | ✓ | ▶ | ✓ |
| 54 | 125 | `git push -u origin main` | S09 · G5, typed, no panel, success described | ✓ | ▶ | ✓ (F7) |
| 55 | 136–144 | `secrets` next to `data-versioning` | S10 · H1 `cd ..`, extra tree `84` | n/a | ▶ no pause | ✓ (F10, F16) |
| 56 | 150–170 | Service account + JSON key | S10 · H2 `illustration` (reuse) | names exact | ▶ (shared) | ✓ |
| 57 | 176–187 | Folders `dvc_store/`, `images/` | S10 · H3 `illustration`, GOLD | ✓ | ▶ | ✓ |
| 58 | — | (missing step) upload the first photos | S10 · H3 · extra row, "a small gap" | n/a | ▶ | ✓ (today's README has it: F8) |
| 59 | 197–205 | Edit `GCS_BUCKET_NAME`, `GCP_PROJECT`, `GCP_ZONE` | S10 · I1 sed (chip) = `85` | n/a | ▶ | ✓ |
| 60 | 215–230 | About `docker-entrypoint.sh` | S10 README card + V4 over CODE | n/a | – | ✓ |
| 61 | 237 | `cd data-versioning` | S10 · I1 typed; S11 · I2 README card "already inside" | ✓ | – | ✓ |
| 62 | 243 | `sh docker-shell.sh` | S11 · I3 = `86` (fails) | ✓ | ▶ | ✓ |
| 63 | — | Fix Dockerfile:36 (`sed -i '36s/google-cloud-sdk/google-cloud-cli/' Dockerfile && sed -n '36p' Dockerfile`) | S11 · I3 · extra = `87` | ✓ (= line 1) | ▶ | ✓ (no chip: F11) |
| 64 | 243 | `sh docker-shell.sh` again | S11 · I3 = `88` | ✓ | – | ✓ (F10) |
| 65 | 269 | `dvc init` | S12 · J1 = `90:45` (Linux refusal) | ✓ | – | ✓ |
| 66 | — | Linux fix `sudo rm -rf .dvc .dvcignore && ls -A`, `git config --global --add safe.directory /app && cat ~/.gitconfig` | S12 · J1 · extra, tag `extra · Linux` = `91`, `92` | ✓ (= line 1) | ▶ (on re-run) | ✓ |
| 67 | 269 | `dvc init` again | S12 · J1 = `93:45` | ✓ | ▶ | ✓ (silent re-entry: F10) |
| 68 | 279 | `dvc remote add -d cheese_dataset gs://YOUR_BUCKET_NAME/dvc_store` | S12 · J2 typed with `your-bucket-placeholder` = `93:63`, README card beside it | ✓ (placeholder filled) | ▶ | ✓ |
| 69 | 293 | `dvc add cheese_dataset` | S12 · J3 = `93:70` (empty) then `95:47` | ✓ | ▶ | ✓ |
| 70 | 303 | `dvc push` | S13 · J4 = `95:71` (+ extra local remote `95:77–78`) | ✓ | ▶ | ✓ |
| 71 | 306 | Inspect `dvc_store` in the bucket | S13 drawn `illustration` | n/a | – | ✓ |
| 72 | 312 | Outside the container | S13 · J5 README card + `exit` | n/a | – | ✓ |
| 73 | 315 | `git status` | S13 · J5 = `96` | ✓ | ▶ no pause | ✓ (F10) |
| 74 | 316 | `git add .` | S13 · J5 = `97` | ✓ | ▶ no pause | ✓ |
| 75 | 317 | `git commit -m "Track initial cheese dataset with DVC"` | S13 · J5 = `98` | ✓ | ▶ no pause | ✓ |
| 76 | 318 | `git tag -a dataset_v20 -m "First version of cheese dataset"` | S13 · J5 = `99` | ✓ | ▶ | ✓ |
| 77 | 319 | `git push --atomic origin main dataset_v20` | S13 · J5, typed, no panel | ✓ | ▶ | ✓ (F7) |
| 78 | 321 | Tag disclaimer | S13 `erratum` card | n/a | – | ✓ |
| 79 | 326–328 | Colab: view `dataset_v20` | S13 note → S15 · J6 | n/a | ▶ (S15) | ✓ deferral narrated (▶ order: F5) |
| 80 | 338–341 | Upload additional images to `images/` | S14 · K1 `illustration` + stand-in `103` | n/a | ▶ no pause | ✗ F3 |
| 81 | 348 | Inside the container | S14 · K2 `sh docker-shell.sh` = `104`, not narrated | ✓ | – | ✗ F3 |
| 82 | 351 | `dvc add cheese_dataset` | S14 · K2 `104:47` | ✓ | ▶ no pause | ✗ F3 |
| 83 | 357 | `dvc push` | S14 · K3 `104:64` (+ local remote `104:70`) | ✓ | ▶ no pause | ✗ F3 |
| 84 | 365 | `git status` | S14 · K4 = `105` | ✓ | ▶ | ✓ |
| 85 | 366 | `git add .` | S14 · K4 = `106` | ✓ | ▶ | ✓ |
| 86 | 367 | `git commit -m "Add images to cheese dataset"` | S14 · K4 = `107` | ✓ | ▶ | ✓ |
| 87 | 368 | `git tag -a dataset_v21 -m "Updated cheese dataset with additional images"` | S14 · K4 = `108` | ✓ | ▶ | ✓ |
| 88 | 369 | `git push --atomic origin main dataset_v21` | S14 · K4, typed, no panel | ✓ | ▶ | ✓ (F7) |
| 89 | 371–372 | Disclaimer; "do not add it again here" | S14 `erratum` beat, extra `113` + README card :372 | ✓ (starter :148 = `113` line 1) | – | ✓ (caption: F18) |
| 90 | 383–385 | Colab: view `dataset_v21` (cells 7, 9, 11, 13, 15, 17, 19, 20) | S15 · K5 notebook `illustration`, cells verbatim (`.cells.txt` lines checked) | ✓ | ▶ | ✗ F5 |
| 91 | 410 | `docker container ls` | S16 · L1 = `150` | ✓ | ▶ | ✓ |
| 92 | 413 | Stop any container that is running | none running (`150`) | n/a | ▶ | ✓ |
| 93 | 418 | `docker system prune` | S16 · L2 = `151` | ✓ | ▶ | ✓ |
| 94 | 424 | `docker image ls` | S16 · L3 = `152` | ✓ | ▶ | ✓ |

**Erratum beat · today's README @ `2515e5e`**

| # | README line | text | scene | exact | status |
| --- | --- | --- | --- | --- | --- |
| T1 | 76–82 | heading "Clone the `data-versioning-ac215` branch:" over `git clone -b main git@github.com:dlops-io/data-versioning.git` | S09 CODE window, line 81 RED | ✓ | ✓ |
| T2 | 91 | `git clone -b main https://github.com/dlops-io/data-versioning.git` | S09 second-clone strip = `131`, then `137` | ✓ (byte-exact to today's :91) | ✓ |
| T3 | — | route T refusals: `dvc init`, `dvc remote add -d cheese_dataset gs://your-bucket-placeholder/dvc_store`, `.dvc/config` | S12 strip = `145:46–55` | ✓ | ✓ (rejoin: F14) |
| T4 | 254 | "upload some pictures in the images folder" | not mentioned; S10 says "the README never says" | n/a | ✗ F8 |
| T5 | 350, 407 | Colab link → notebook `18KYngbv` | not mentioned; S15 shows `1RRQ1SlH` | n/a | ✗ F8 |

**Teardown**

| # | item | where | status |
| --- | --- | --- | --- |
| X1 | containers | S08 F2 + prune (`61`, `62:9`); `--rm` for the rest | ✓ (S16 card line stale: F6) |
| X2 | `data-labeling-network` | S08 prune `62:10–13`, said | ✓ |
| X3 | bucket CORS rule | S16 card only, not spoken, not runnable after prune | ✗ F6 |
| X4 | service-account key | S16 card IAM path + SAY | ✓ (local JSON, timing: F6) |
| X5 | buckets bill / never `dvc_store/` | S16 card + SAY, RED line | ✓ |
| X6 | `docker-volumes/label-studio` | S08 ponder + S16 card | ✓ (sudo on Linux: F6) |
| X7 | `.dvc/cache` | S16 card | ✓ |
| X8 | images (~6 GB) | not mentioned | optional (F6) |

Extras: every typed extra matches its capture's line 1 byte for byte (`02`, `03`, `05`, `06`,
`09`, `09b`, `12`–`16`, `19`–`21`, `27`, `29`, `41:102–110`, `42:67`, `53`, `54:37/39/125`, `55`,
`64`, `74`, `75`, `78`, `84`, `87`, `89`, `90:49`, `91`, `92`, `93:65/80`, `94`, `95:45/57/64/77/78`,
`101`, `102`, `103`, `104:45/57/70`, `110`–`118`, `120`–`122`, `131`, `137`, `145:51`, `C07b`, `C13`,
`C19`, `C19b`, `C20`). The stand-in API calls (`23`, `24`, `28`, `30`–`33`, `43`) are output-only
strips, as the conventions specify. Every cited TERM line range was checked against its file.

**Verdict: PASS WITH FIXES.** The checklist has 94 rows: 39 data-labeling and 55 data-versioning.
Five of them are required fixes or the missing step (rows 12, 29, 58, 63, 66), and three are README
re-runs. Every row is on screen. 13 rows are marked ✗; all are pause, ▶ or location problems, and
none is a missing or misspelled command. Every README command is byte-exact, apart from the two placeholder fills, and in README order,
apart from two narrated deviations. Trackers A–L are consistent. Two wrong items must be fixed before
scenes: S09's missing `cd ..` before the clone (F1), and S07's legacy-token fix, which has no
your-turn beat and never shows where the legacy token is (F2). The seven confusing items F3–F9 come
next.
