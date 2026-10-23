# L13 script review · lens 3 · follow-along completeness

Reviewed: `script.md` at `1d1134b` (branch `claude/ac215-l09-l13-batch`). Checked against
`assets/source/model-training/README.md` (@ `b9aee1c`, the course pin and still `main`'s head on
2026-10-23, ASSETS L43–45), the repo's scripts in the same folder (`docker-shell.sh`, `Dockerfile`,
`docker-entrypoint.sh`, `package-trainer.sh`, `cli.sh`, `cli-multi-gpu.sh`, `cli.py`,
`package/setup.py`, `package/trainer/task.py`), the Colab extracts
`assets/source/colab/notebook-A-1h6xRhjI.cells.txt` and `notebook-B-1aAE5vR9.cells.txt`, `BRIEF.md`
(trackers, errata, teardown, README checklist L718–759, the coordinator's decisions table), and line 1
plus every cited line range of the captures in `assets/terminal/laptop/` and `assets/terminal/colab/`.

## Summary

Every README instruction and every notebook step is on screen. All six spelled commands are typed
byte for byte as the source spells them: `sh docker-shell.sh`, `sh package-trainer.sh`, `sh cli.sh`,
`sh cli-multi-gpu.sh`, notebook B's `!pip install -q wandb -U`, and `export WANDB_KEY=...`. The last
one has its `...` filled with the placeholder and an extra `; echo ${#WANDB_KEY}` tagged `extra`.
Every extra matches its capture's line 1. Every cited TERM and NB line range was checked against its
file, and the README card spans quote the right lines. README order holds, with two narrated
back-steps: the optional CPU step shows early in S10 and again in S13 ("in reverse"), and S05 holds
tracker B4 after B6. Both Dockerfile failures (`21` → fix 1 `22`; `23` → fix 2 `24`; `25`; `26`) and
both fixes are on screen, tagged `extra`, and said as "an extra". All eight trackers match the BRIEF
(A 6 · B 6 · C 7 · D 2 + 2 extra rows · E 3 · F 5 · G 4 · clean-up 3), with no skipped or duplicated
step.

**Could a viewer with their own clone, a GCP project and a W&B account finish the CPU path, pausing at
each tag? Yes, with two traps the script sets itself.** First, S07 tells the follower that the key
length "isn't zero" is what matters. The trainer's pinned wandb actually accepts exactly 40
characters, and the video says so only in S11, one scene after the billed `sh cli.sh`. A follower
whose key is not 40 characters long loses a paid job that fails after the data download (F1).
Second, S04's upload step says "edit cell 13, then run cells 64 and 66". Cell 13 already ran during
setup, so the old function uploads to the instructors' bucket and fails (F2).

Eight items are confusing:

- The teardown card exits the cockpit first, but its `gcloud` and `gsutil` lines need the cockpit,
  and nothing shows where `JOB_ID` comes from (F3).
- Both required Dockerfile fixes and the build re-run have no `▶ your turn` and no spoken pause (F4).
- The fix `sed`s fail on macOS sed and carry no "our editor" chip (F5).
- Part 2 opens with no "same terminal, key still exported?" check (F6).
- Notebook A's upload in S03 needs a bucket that the video creates only in S07 (F7).
- The job's gold billing tag comes after the submit pause (F8).
- S12 never says where the job's logs are (F9).
- "Raise the pin in setup.py" names no version, and no tested route exists (F10).

Seven polish items close the list, including seven `▶` blocks whose SAY never says "pause" (F11).

## Findings

**F1 · S07 / S10 / S11 · wrong (when a viewer's key is not 40 characters) · the key-length check is taught as "not zero", and the 40-character gate arrives after the billed submit.**
S07 C7 (L594–601) types `export WANDB_KEY=PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000; echo ${#WANDB_KEY}`
→ `40` and says "40 for our placeholder; what matters is that it isn't zero". S10's `▶` on `sh cli.sh`
(L758–764) submits the job. Only S11 (L849–853) says "this old wandb pin accepts exactly 40
characters, and 47 fails" (`87:14`), and that "if your key has a different length, raise the pin in
setup.py". `task.py:152–153` calls `wandb.login(key=args.wandb_key)` *after* the dataset download
(`:96–100`). A follower whose key is not 40 characters long passes every check in the video, submits
a paid job, and the job fails late. S10 itself warns that this is "the real risk" for the empty key
(L790). The follower already has the right check on screen in S07. The script just gives the wrong
criterion for it.
*Fix (respects the coordinator's "never claim a length for a real key"):* keep the S07 typed line
and capture as they are. Change the chip to "the check: not 0 · and the trainer's pinned wandb
accepts only 40 (scene 11)". End the S07 SAY: "An extra echo prints its length, 40 for our
placeholder. It must not be zero, and the trainer's pinned W and B library accepts exactly 40, so
note your number." On S10's `▶` beat, add: "Before you run it, check that your key length was 40;
if not, scene 11 shows the fix first." The video then claims nothing about real keys: it states
the pin's rule (`84:14`, `87:14`) and lets the follower compare.

**F2 · S04 · wrong · "edit the bucket and project inside cell 13, then run cells 64 and 66" uploads with the old function.**
Notebook B's bucket and project are hard-coded inside `upload_experiment` in cell 13 (NB(B: 254, 257)).
Cell 13 is the utils cell. The follower ran it during S04's B2 data cells ("cells 7–32"). Editing it
afterwards changes nothing until it runs again, so cell 66 still calls the old definition. That
definition uses `storage.Client(project="ac215-project")` and `get_bucket("cheese-app-models")`, which
fails with a permission error on the instructors' bucket. Following the SAY (L447) word for word
gives this failure. The block also has a `▶` but no "pause" (F11).
*Fix:* SAY: "To upload, edit the bucket and project inside cell 13 and run cell 13 again, then run
cells 64 and 66; pause and do it." On screen, add a GREY chip on NB(B: 254, 257): "edited? run cell
13 again".

**F3 · S15 · confusing · the teardown card exits the cockpit before the lines that need it, and `JOB_ID` has no source.**
The card's order (L1018–1024) is: `exit` the cockpit; then `gcloud ai custom-jobs cancel JOB_ID
--region=us-central1`; then `gsutil rm $GCS_BUCKET_URI/cheese-app-trainer.tar.gz`. `gcloud` and
`gsutil` are authenticated only inside the cockpit (`26:49–51`, entrypoint `:6`), and
`$GCS_BUCKET_URI` exists only there (`docker-shell.sh:8, 22`). The BRIEF says "in the cockpit, `gsutil
rm …`" (L705); the card drops "in the cockpit". `JOB_ID` is the numeric job id, not the display name
`cheese_training_job_<hex>`, and nothing shows where to find it. `40:91`, `gcloud ai custom-jobs list
--region=us-central1`, is a real typed line, and the BRIEF lists it as an extra (L250), but the
script never uses it.
*Fix:* reorder the card and label its first two lines. (1) "in the cockpit: `gcloud ai custom-jobs
list --region=us-central1` (finds the JOB_ID) · `gcloud ai custom-jobs cancel JOB_ID
--region=us-central1` · `gsutil rm $GCS_BUCKET_URI/cheese-app-trainer.tar.gz`". All three are shown,
not run, with no output panel; `40:91` is line-1-exact. (2) "or in the console: Custom jobs →
Cancel; the bucket → delete". (3) "then `exit` (`--rm` removes it) · `docker image rm …`". Add to the
SAY: "Cancel and delete from inside the cockpit, or in the console, and exit it last."

**F4 · S08 · confusing · the two required fixes and the re-run have no your-turn beat.**
Every follower's build fails today (`21`, `23`), so fix 1, the re-run, fix 2 and the third run are
steps everyone must take. That is exactly the BRIEF's "real checkpoint". The fix 1 block (L647–653)
has no `▶` and no pause. The re-run (L655–659, "Run it again") has neither. The fix 2 block
(L661–665) has neither. The third run (L667–673) has a `▶` but its SAY never says "pause". Only
the first, failing run (L641) pauses.
*Fix:* add `▶ your turn` on both fix lines and both re-runs. SAY for fix 1: "…switches the base to
bookworm, Debian 12; pause and make the same change." SAY for fix 2, after "on line 37": "Pause,
make it, and run the script again; the first full build is slow."

**F5 · S08 · confusing · fixes 1 and 2 are typed as GNU `sed -i`, which fails on macOS, and they have no "our editor" chip.**
`22:1` and `24:1` are `sed -i '2s/…/…/' Dockerfile …` and `sed -i '37s/…/…/' Dockerfile …`. BSD sed on
a Mac reads the quoted script as `-i`'s backup suffix and stops with an error. The `&& sed -n …`
check then does not run. The S08 SAY mentions Apple Silicon, so Mac followers are expected. D1's
edit (`20`) carries "our editor; use yours", but the two fixes do not. The BRIEF calls all three
`sed`s editor actions (L807).
*Fix:* add the GREY chip "our editor; use yours · macOS sed: `sed -i ''`" to both fixes. Show the
resulting lines large as the target: `22:3` "your new line 2" and `24:4` "your new line 37". `25`'s
`git diff` then confirms either route.

**F6 · S08 / S09 · confusing · part 2 starts with no check that the key is still exported in this terminal.**
Part 1 ends on the key export (S07) and a natural break, and part 2 opens with `cd model-training` and
`sh docker-shell.sh` (L620, L636). A follower who comes back in a new terminal starts a cockpit with
an empty key. The video shows that failure only in S10 (`70`), after the submit pause. S09 already
types the right check in the cockpit, `echo $GCP_PROJECT $GCS_BUCKET_URI ${#WANDB_KEY}` → `26:47`
(`… 40`), but it is an untagged extra, and the SAY only says "key came through".
*Fix:* add a GREY chip on S08 D1: "same terminal as your export · new terminal? export again first".
In S09, give that `echo` a `▶`, and add to the SAY: "Pause and check yours: if the last number is 0,
exit, export the key, and start the cockpit again." This also helps F1, because the follower sees
the length one more time before packaging.

**F7 · S03 · confusing · notebook A's upload needs a bucket that the video creates only in S07.**
A6 (L383–389) says "put your own project and bucket into cell 63, and run cell 66. Pause and run it."
`storage_client.get_bucket(GCS_BUCKET_NAME)` (cell 66) needs an existing bucket. The follower creates
one only at C6 in S07. The audience may still have an L10/L11 bucket, but nothing says to use it.
*Fix:* add a GREY chip on NB(A: 1400–1402): "your bucket: one from lecture 11, or create it now ·
scene 7 shows how". Add to the SAY: "Use one of your buckets, or create one now; scene 7 shows how."

**F8 · S10 · confusing · the job's gold billing tag comes after the submit pause.**
The `▶` on `sh cli.sh` comes at L758–764. With a real key, that submits a billed VM. The S10 GOLD
`cost_tag()` ("the job's VM bills from submission until the script exits") comes four blocks later,
at L792–796. A follower who pauses at the `▶` hears about the bill after paying it. S01's general
tag does not name this step.
*Fix:* move the GOLD tag onto the F2 `▶` beat, and open that SAY with: "A gold tag first: from
submission until the script exits, the job's machine bills your project. Now sh cli.sh; pause and
run it." Keep the V4 job-spec flight (L792) without its tag line, or end the scene on it with no SAY.

**F9 · S12 · confusing · nothing says where the job's printout is or how to tell that it ended.**
F4 (L859–863) sends the follower to Training → Custom jobs and then shows the log's shape (L865–878).
It never says that the log sits behind the job's page (its logs link opens Cloud Logging), or which
line means the job finished. The shape's last line, `Training Job Complete` (`task.py:341`), is the
only marker a follower can look for, and that is allowed, because it is the code's own print.
*Fix:* add to the F4 SAY: "Open your job and follow its logs link; wait for the line training job
complete." The console label is not verified, so tag the wireframe `illustration`, and never show a
status value (BRIEF L798–802).

**F10 · S11 · confusing · "raise the pin in setup.py" has no target version and no tested route.**
L849–853 tells a follower whose key is not 40 characters to "raise the pin in setup.py". It names no
version. It does not say to run `sh package-trainer.sh` again, which the S09 ponder implies but S11
never says. It also does not check that `task.py:22`, `from wandb.keras import WandbCallback,
WandbMetricsLogger`, still imports under a newer wandb inside `tf-cpu.2-17.py310` (unverified here;
digest L1113 flags that the import path patches `tensorflow.python.keras`). A follower who takes this
route is on their own, with a paid job at stake.
*Fix:* on the GREY card, write "raise the pin · then sh package-trainer.sh again · a tested version:
see the study guide", and have the coordinator put a verified pin, or a removal of the unused
import, in the study guide or `exercises.md`. If no version can be verified, say "the study guide has
the workaround" and do not imply a one-line fix.

**F11 · S04, S07, S08, S09, S12, S14 · polish · `▶` blocks whose SAY never says "pause", and two notebook checkpoints with no `▶`.**
Seven `▶` blocks have no spoken pause:

- S04 L447 (B5/B6, compare and upload; see F2)
- S07 L560 (C2 enable the API; C3 quota)
- S08 L673 (the third build; see F4)
- S09 L712 (E2, open `task.py`)
- S12 L888 (F5, the W&B project)
- S14 L965 (G2, open `task_multi_gpu.py`)
- S14 L993 (G4, `sh cli-multi-gpu.sh`: the most expensive optional step)

Two checkpoints have no `▶`: S04 B2 (L403–406, cells 7–32, which must run before cell 34's login) and
S03 A5 (cells 54–59, including the prediction cells 57–59, which are never mentioned).
*Fix:*

- S07: "…set a new limit and submit; pause and do both."
- S09 E2: "Pause and open it."
- S12 F5: "Pause and open your project."
- S14 G2: "Pause and open it."
- S14 G4: "Optional: pause only if your quota came through."
- S04 B2: add `▶` and "Pause and run them, through cell 32."
- S03 A5: "Run the rest of that section, to the predictions."

**F12 · S07 / S10 · polish · the taught export puts the key into shell history, which S10 then lists as an exposure.**
Typing `export WANDB_KEY=<key>` inline stores the key in the shell history. S10's answer chip says
"your shell history, if typed inline" (L779), but S07 gives no other way.
*Fix:* add an optional GREY chip at C7, tagged `extra · not captured`: "keep it out of history:
`read -rs WANDB_KEY && export WANDB_KEY` (bash, zsh)". Keep the README form as the typed line.

**F13 · S03 / S04 · polish · neither notebook's address is on screen, and notebook B gets no "save a copy, GPU" step.**
S03 says "Open notebook A from the course page". The notebooks' own "Open in Colab" badges point at
different copies (digest L1104). S04 starts at notebook B's install cell; it never tells the
follower to open B, save a copy and pick a GPU (B cell 3, NB(B: 26–31)).
*Fix:* add a GREY chip on S03 A1: "the study guide links notebooks A and B · the badges inside them
open older copies". Add to the S04 B1 SAY: "Open notebook B, save a copy, pick a GPU, and run its
first cell."

**F14 · S09 / S11 · polish · extras a follower would want to repeat are missing their command.**
(a) S11 types `80` and then `82`, `docker run --rm trainer-standin pip list`. `81`, `docker commit
trainer-standin trainer-standin >/dev/null && docker rm trainer-standin`, is never shown. Without
it, `82`–`87` fail for anyone repeating them, because there is no `trainer-standin` image. (b) S09's
chip "with your bucket: look for cheese-app-trainer.tar.gz in it" has no command, but `30:64`,
`gsutil ls $GCS_BUCKET_URI`, is captured. (c) `40:91` is needed for F3.
*Fix:* type `81`'s line 1 with no output panel between `80` and `82`. Type `30:64`'s command with no
output panel ("with your bucket it lists the tarball"). Use `40:91` on the teardown card (F3).

**F15 · S04, S07 · polish · extras without the `· extra` tracker caption or the spoken word.**
The conventions caption the tracker "· extra" while an extra is on screen. That caption is missing
for:

- the S04 stand-in strip (`C05`, `C05b`), under `TRACKER B1`
- `wandb.finish()` (L436), under B4
- `tree -L 1 .` (`05`), under C4
- the `; echo ${#WANDB_KEY}` part of `10`, under C7

S04 never says "extra" for the version check, and S07 never says it for `tree`.
*Fix:* write `TRACKER B1 · extra · local stand-in`, `TRACKER B4 · extra`, `TRACKER C4 · extra` and
`TRACKER C7 · extra`. Add "an extra tree shows it" to the C4 SAY.

**F16 · S15 · polish · smaller teardown gaps.**
(a) The card deletes the `model-trainer` key in IAM but never the local `secrets/model-trainer.json`.
(b) Notebook B uploads under a folder named after the Google account, plus `submit.txt` (cell 13,
NB(B: 269–281)), not under `experiment_<ts>/` at the root. (c) "`docker image rm …`" leaves the list
to the follower. Their extras leave `trainer-standin`, `python:3.10-slim-bookworm`, and both
`python:3.13-slim-*` bases (`91`). (d) After rotating, the Colab secret `WandB` and the exported shell
variable still hold the old key. (e) On Linux, the root-owned `trainer.tar.gz` (`31:2`) needs `sudo
rm`.
*Fix:* card line "end of term: delete the model-trainer key in IAM and its JSON in secrets · rotate
your W&B key and update the Colab secret". Change the bucket line to "experiment folders (notebook B:
under your account's folder)". Change the images line to "`docker image rm model-training-cli
trainer-standin python:3.10-slim-bookworm`". The image names come from `91`, so this is not
hand-typed output.

**F17 · S08 · polish · "your bucket and project" should say project ID and keep `gs://`.**
`docker-shell.sh:8–9` expects a `gs://` URI and a project **ID**, because the entrypoint runs `gcloud
config set project`. The capture shows both forms (`20:5–6`), but the SAY (L625) says only "bucket and
project".
*Fix:* SAY "Put your bucket, with its g s prefix, and your project ID on lines 8 and 9…", or add a
GREY chip "project ID, not its name · keep gs://".

## The W&B key step (requested judgment)

The script types capture `10`'s own line, `export
WANDB_KEY=PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000; echo ${#WANDB_KEY}`. Beside it is a README card
(`README.md · line 80`, `export WANDB_KEY=...`) with the chip "README: `...` = your key · ours: an
obvious placeholder", and the `; echo …` part is tagged `extra`.

**Served:** the README's form and the substitution are both explicit. The typed line is real, not
hand-made. The echo checks the key without printing it, which is the right habit. The ponder
(`11` → `0`) teaches that the variable belongs to one shell. S10's `70`/`71` later show the failure
and the restart.

**Not served:**

1. The criterion the echo is meant to check is wrong for this trainer: "not zero" should be "40, for
   the pinned wandb" (F1).
2. The check is never repeated where it matters, at the start of part 2 and before the submit (F6).
3. The inline form puts the key into shell history (F12).
4. The way out for a non-40-character key, "raise the pin", is untested (F10).

**Verdict:** with F1 and F6 applied, a follower is served. Without them, the step teaches a check
that passes keys the job will reject.

## Tracker arithmetic

| tracker | N | steps placed | result |
| --- | --- | --- | --- |
| A | 6 | A1, A2, A3, A4, A5, A6 (S03) | ✓ (A5 no ▶: F11) |
| B | 6 | B1, B2, B3, B4, B5, B6 (S04) · B4 held (S05) | ✓ (back-step narrated; captions F15) |
| C | 7 | C1 (+ · extra), C2, C3, C4, C5 (+ · extra), C6 (+ · extra), C7 (S07) | ✓ (C4, C7 captions F15) |
| D | 2 + 2 extra rows | D1, D2, row "fix 1 · Dockerfile:2", D2, row "fix 2 · Dockerfile:37", D2 (S08) | ✓ (no ▶ on the fixes: F4) |
| E | 3 | E1 · extra, E1, E2, E3, E3 · extra (S09) | ✓ |
| F | 5 | F1, F3 flash, F2 (+ · extra) (S10) · F2 · extra (local stand-in) (S11) · F4, F5 (S12) · F3 (+ · extra) (S13) | ✓ (F3 twice, both narrated) |
| G | 4 | G1, G2, G3, G4 (S14) | ✓ |
| clean-up | 3 | 1, 2, 3 (S15) | ✓ |

The step lists in the script's Conventions (L133–151) match BRIEF L231–244 word for word. Concept
scenes S01, S02 and S06, S11's badges beat, S14's ladder, and S15's `cli.py` beat and recap have no
tracker, as the BRIEF specifies.

## Teardown (what the viewer ends with)

- **Gone, said:** the cockpit (`--rm`, `90` empty); every CPU job ends with its script (S10's tag).
- **Shown on the card:** custom jobs RUNNING/PENDING; `gcloud ai custom-jobs cancel`; Training
  pipelines for `cli.py`; the tarball (`gsutil rm`); the experiment folders; the bucket; notebook B's
  `wandb.finish()`; disconnecting both Colab runtimes; deleting the `model-trainer` key; rotating the
  W&B key.
- **Gaps:** the card's order puts `exit` before the cockpit-only lines, and there is no `JOB_ID`
  source (F3). Also missing: the local key JSON, notebook B's account-named folder, the explicit image
  list, the Colab secret and shell variable after rotation, and `sudo` for the tarball on Linux
  (F16).
- **Nothing to undo:** the GPU quota request; the Vertex AI API (no charge while idle).

## Appendix · README and notebook checklist

Legend: ✓ present, exact and in order · ✗ gap · ▶ has a your-turn tag · "no pause" = ▶ tag but the
block's SAY never says pause.

**Notebook A** (`1h6xRhjI`, course-site order first)

| # | cell | instruction (verbatim where it is code) | scene / tracker · SHOW | exact | ▶ | status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | File → Save a copy in Drive; Runtime → Change runtime type → GPU | S03 · A1 menu `illustration` | n/a | ▶ | ✓ (address: F13) |
| 2 | 4–12 | imports, eager/replicas, `!nvidia-smi`, utils | S03 · A1 NB(A: 101, 106, 112) + outputs 115, 117, 120, 137 `recorded` | ✓ | ▶ (shared) | ✓ |
| 3 | 15–21 | download, load, view, metrics | S03 · A2 NB(A: 318), 352–353 | ✓ | ▶ | ✓ |
| 4 | 24–28 | x/y, split, `tf.data` | S03 · A3 NB(A: 432–443), 445–447 | ✓ | ▶ | ✓ |
| 5 | 31 | `create_experiment()` | S03 · A4 NB(A: 527–528) | ✓ | ▶ | ✓ |
| 6 | 33–51 | five models (build, train, save) | S03 · A4 V2 + NB(A: 242, 245, 249, 289, 307) | ✓ | ▶ | ✓ |
| 7 | 54, 56 | compare, best model | S03 · A5 NB(A: 1283–1295, 1304) | ✓ | – | ✗ F11 (polish) |
| 8 | 58–59 | predict with the best model | not said | n/a | – | ✗ F11 (polish) |
| 9 | 62 | `auth.authenticate_user()` | S03 · A6 NB(A: 1396–1397) | ✓ | ▶ | ✓ |
| 10 | 63 | `GCP_PROJECT`, `GCS_BUCKET_NAME` [REPLACE] | S03 · A6 NB(A: 1400–1402), "replace this with yours" | ✓ | ▶ | ✗ F7 (no bucket yet) |
| 11 | 66 | save data details, upload | S03 · A6 NB(A: 1437, 1439–1442) | ✓ | ▶ | ✓ |

**Notebook B** (`1aAE5vR9`)

| # | cell | instruction | scene / tracker · SHOW | exact | ▶ | status |
| --- | --- | --- | --- | --- | --- | --- |
| 12 | 3 | save a copy, GPU | not said | n/a | – | ✗ F13 (polish) |
| 13 | 5 | `!pip install -q wandb -U` | S04 · B1 NB(B: 37) + stand-in `pip install -q wandb -U` = `C05:1` | ✓ | ▶ | ✓ |
| 14 | — | (extra) `python -c 'import wandb; print(wandb.__version__)'` | S04 · B1 = `C05b:1` | ✓ (= line 1) | – | ✓ (caption, word "extra": F15) |
| 15 | 7–32 | imports, utils (cell 13), data, pipelines, `create_experiment()` | S04 · B2 one line | n/a | **none** | ✗ F11 |
| 16 | 16 | the `experiments.zip` line (optional delete) | S04 · B2 NB(B: 373–375), strike chip | ✓ | – | ✓ |
| 17 | 33–34 | secret `WandB`, notebook access; `wandb.login(key=wandb_key)` | S04 · B3 `illustration` + NB(B: 603–606), 614–615 | ✓ | ▶ | ✓ |
| 18 | 36–52 | five training cells, `wandb.init(project='cheese-app-demo')` | S04 · B4 NB(B: 697), 773, 781 | ✓ | ▶ | ✓ |
| 19 | — | (extra) `wandb.finish()` after cell 52 | S04 · B4, tag `extra`, "that one is an extra" | n/a | – | ✓ (caption F15) |
| 20 | 55–60 | compare, best, predict | S04 · B5 NB(B: 1703–1715) | ✓ | ▶ no pause | ✓ (F11) |
| 21 | 13 | edit bucket and project in `upload_experiment` | S04 · B6 NB(B: 254, 257) | ✓ | ▶ no pause | ✗ F2 (re-run cell 13) |
| 22 | 64, 66 | `auth.authenticate_user()`, `upload_experiment(data_details)` | S04 · B6 NB(B: 1819–1820) | ✓ | ▶ no pause | ✗ F2 |

**model-training README @ `b9aee1c`**

| # | README line | instruction (verbatim where it is a command) | scene / tracker · SHOW | exact | ▶ | status |
| --- | --- | --- | --- | --- | --- | --- |
| 23 | 7, 14 | Docker; GCP and W&B accounts | S01 checklist card | n/a | – | ✓ |
| 24 | 8, 16–17 | Clone (link, no command) | S07 · C1 `git clone https://github.com/dlops-io/model-training` (= `01`) + `cd model-training`, README card :17, chip | n/a (ours) | ▶ | ✓ |
| 25 | — | (extra) `git log -1 --format='%H %ci %s'`, `ls -la` | S07 · C1 · extra = `02`, `03` | ✓ (= line 1) | – | ✓ |
| 26 | 19–21 | Enable Vertex AI API | S07 · C2 `illustration` | n/a | ▶ no pause | ✓ (F11) |
| 27 | 23–44 | Quotas: filter, T4 per region, regions, EDIT QUOTAS, limit, NEXT, name, SUBMIT REQUEST; hours; may be refused | S07 · C3 `illustration` (README labels), card :43–44 | labels exact | ▶ no pause | ✓ (F11) |
| 28 | 50–58 | `secrets` beside `model-training` | S07 · C4 `cd ..`, `mkdir secrets` (chip, = `04`), extra `tree -L 1 .` (= `05`), card :55–58 | n/a | ▶ | ✓ (caption F15) |
| 29 | 60–64 | service account `model-trainer`, three roles, Manage keys → JSON → rename `model-trainer.json` | S07 · C5 `illustration`; extra `ls -la secrets` = `06` | names exact | ▶ | ✓ |
| 30 | 66–71 | bucket `cheese-app-trainer` [REPLACE WITH YOUR BUCKET NAME] | S07 · C6 `illustration`, card :71; extras `07`, `08` | ✓ | ▶ | ✓ |
| 31 | 75–79 | W&B → User settings → API keys → copy | S07 · C7 `illustration` | n/a | ▶ | ✓ |
| 32 | 80 | `export WANDB_KEY=...` | S07 · C7 `export WANDB_KEY=PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000; echo ${#WANDB_KEY}` = `10:1`, card :80 | ✓ (`...` filled, echo extra) | ▶ | ✗ F1 (criterion), F12 |
| 33 | — | (extra) `echo ${#WANDB_KEY}` in a new terminal | S07 ponder answer = `11` | ✓ | – | ✓ |
| 34 | 88–94 | bucket and project in `docker-shell.sh` | S08 · D1 `cd model-training`, `sed` = `20:1` (chip "our editor"), card :93–94 | n/a | ▶ | ✓ (F6, F17) |
| 35 | 89–112 | the listing is not the file | S08 erratum cards :100–101, :110 + CODE(docker-shell.sh: 12–24, 3) | ✓ | – | ✓ (:96 never shown ✓) |
| 36 | 114–115 | inside `model-training`: `sh docker-shell.sh` | S08 · D2 = `21` (fails at 2/14), card :114–115 | ✓ | ▶ | ✓ |
| 37 | — | (extra, fix 1) `sed -i '2s/python:3.13-slim-bullseye/python:3.13-slim-bookworm/' Dockerfile && sed -n '1,2p' Dockerfile` | S08 · D row "fix 1" = `22` | ✓ (= line 1) | **none** | ✗ F4, F5 |
| 38 | 115 | `sh docker-shell.sh` again | S08 · D2 = `23` (fails at 8/14) | ✓ | **none** | ✗ F4 |
| 39 | — | (extra, fix 2) `sed -i '37s/google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin/google-cloud-cli/' Dockerfile && sed -n '35,37p' Dockerfile` | S08 · D row "fix 2" = `24` | ✓ (= line 1) | **none** | ✗ F4, F5 |
| 40 | — | (extra) `git diff --stat; git diff Dockerfile` | S08 = `25` | ✓ (= line 1) | – | ✓ |
| 41 | 115 | `sh docker-shell.sh` third time | S08 · D2 = `26` (builds) | ✓ | ▶ no pause | ✗ F4 |
| 42 | 116 | `WANDB_KEY` passed in | S07 C7, S10 `70`/`71` | n/a | – | ✓ (part-2 check: F6) |
| 43 | — | (extra) cockpit checks `26:42–65`, `docker image ls model-training-cli` | S09 · E1 · extra = `26`, `27` | ✓ (= typed lines) | – | ✓ (F6) |
| 44 | 122–123 | review `setup.py` | S09 · E1 CODE(package/setup.py: 5–13) | ✓ | ▶ | ✓ |
| 45 | 124–125 | review `task.py` | S09 · E2 CODE(task.py: 45–54, 96–100, 152–153) | ✓ | ▶ no pause | ✓ (F11) |
| 46 | 127–129 | `sh package-trainer.sh` | S09 · E3 = `30:42`, card :128–129 | ✓ | ▶ | ✓ (`gsutil ls`: F14) |
| 47 | — | (extra) `ls -l trainer.tar.gz`, `tar tzvf trainer.tar.gz`; host check | S09 · E3 · extra = `30:53`, `30:55`, `31` | ✓ | – | ✓ |
| 48 | 133–134 | review `cli.sh` | S10 · F1 CODE(cli.sh: 5–19) | ✓ | ▶ | ✓ |
| 49 | 135–149 | required changes; accelerator and region lists | S10 card :136–142; erratum card :152–154 | ✓ | – | ✓ (region list :143–149 not quoted; no change needed on CPU) |
| 50 | 150 | `sh cli.sh` | S10 · F2 = `40:42`, card :150 | ✓ | ▶ | ✗ F1 (key gate), F8 (gold after) |
| 51 | — | (extra) `gcloud auth list`, `sh -x cli.sh`, un-exported key `70`, second cockpit `71` | S10 · F2 · extra | ✓ (= typed lines) | – | ✓ |
| 52 | 152–154 | OPTIONAL CPU: drop the accelerator; `sh cli.sh` | S10 erratum (already default), F3 flash; S13 reprise | ✓ | – | ✓ |
| 53 | 156–158 | View Jobs → Custom Jobs | S12 · F4 `illustration`, card :157–158 | n/a | ▶ | ✓ (logs: F9) |
| 54 | 160–163 | View Training Metrics → `cheese-training-vertex-ai` | S12 · F5 V2 `illustration`, card :161–163, `erratum` | ✓ | ▶ no pause | ✓ (F11) |
| 55 | 166 | review `cli-multi-gpu.sh` | S14 · G1 CODE(cli-multi-gpu.sh: 4–16) | ✓ | ▶ | ✓ |
| 56 | 167 | review `task_multi_gpu.py` | S14 · G2 CODE(task_multi_gpu.py: 286–301, 303–321, 338–343) | ✓ | ▶ no pause | ✓ (F11) |
| 57 | 168–169 | make required changes | S14 · G3 quota card | n/a | – | ✓ |
| 58 | 170 | `sh cli-multi-gpu.sh` | S14 · G4 = `50:42`, card :170 | ✓ | ▶ no pause | ✓ (F11) |

**Extras outside the README** (S11, S13, S15)

| # | command | where | exact | status |
| --- | --- | --- | --- | --- |
| 59 | `docker run --name trainer-standin -v "$PWD/trainer.tar.gz":/tmp/trainer.tar.gz python:3.10-slim-bookworm pip install /tmp/trainer.tar.gz` | S11 = `80` | ✓ (= line 1) | ✓ |
| 60 | `docker commit trainer-standin trainer-standin >/dev/null && docker rm trainer-standin` | missing | n/a | ✗ F14 |
| 61 | `docker run --rm trainer-standin pip list`; `09` loop; `… python -m trainer.task --help`; four `wandb.login` strips | S11 = `82`, `09`, `83`, `85`, `84`, `86`, `87` | ✓ (= line 1) | ✓ (not repeatable without row 60) |
| 62 | `09` loop | S13 · F3 · extra | ✓ | ✓ |
| 63 | `python cli.py`, `export GCP_REGION=us-central1`, `python cli.py` | S15 = `60:42`, `60:49`, `60:50` | ✓ | ✓ |
| 64 | `docker ps -a`, `docker image ls` | S15 · clean-up 1 = `90`, `91` | ✓ | ✓ |

**Teardown**

| # | item | where | status |
| --- | --- | --- | --- |
| X1 | cockpit | card line 1, `--rm`, `90` | ✓ (order: F3) |
| X2 | images | SAY "the images stay"; card `docker image rm …` | ✓ (explicit list: F16) |
| X3 | running/pending custom jobs | card + SAY | ✓ |
| X4 | cancel a stuck job | card, shown not run | ✗ F3 (no `JOB_ID` source, needs the cockpit) |
| X5 | Training pipelines (`cli.py`) | card | ✓ |
| X6 | tarball | card `gsutil rm`, shown not run | ✗ F3 (cockpit-only, listed after `exit`) |
| X7 | experiment folders / bucket | card + SAY | ✓ (notebook B's path: F16) |
| X8 | notebook B `wandb.finish()`; disconnect runtimes | card + SAY | ✓ |
| X9 | `model-trainer` key | card (IAM) + SAY, end of term | ✓ (local JSON: F16) |
| X10 | W&B key rotation | card + SAY | ✓ (Colab secret, shell variable: F16; history: F12) |
| X11 | GPU quota request; Vertex AI API | nothing to undo | ✓ |

**Verdict: PASS WITH FIXES.** The checklist has 64 rows: 11 notebook A, 11 notebook B, 36 README
and 6 more extras. There are also 11 teardown rows.

- **Required steps that are not in the README:** rows 37, 39 (the two Dockerfile fixes), 21 (the
  cell-13 re-run) and 19 (`wandb.finish()`).
- **Exactness and order:** every spelled README or notebook command is byte-exact, apart from the
  filled `...` in row 32. Every extra equals its capture's line 1. README order holds, apart from
  two narrated back-steps.
- **Gaps:** 14 checklist rows are marked ✗ (plus teardown rows X4 and X6). All are pause, ▶, criterion or prerequisite problems, plus one
  missing extra (row 60). No README command is missing or misspelled.
- **Must fix before scenes (2 wrong):** S07's key-length criterion and the late 40-character gate
  (F1), and S04's cell-13 edit without a re-run (F2).
- **Confusing (8):** F3–F10 come next. The most urgent are the teardown order (F3) and the missing
  your-turn beats on the two required fixes (F4).
- **Polish (7):** F11–F17.
