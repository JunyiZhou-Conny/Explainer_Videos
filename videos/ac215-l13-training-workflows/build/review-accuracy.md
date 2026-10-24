# L13 script v1 (1d1134b) — review lens 1: technical accuracy

Scope: every SAY/SHOW claim in `script.md` checked against `assets/terminal/laptop/*.txt`,
`assets/terminal/colab/*.txt`, `assets/source/model-training/**` (README, Dockerfile, the five shell
scripts, `cli.py`, `setup.py`, `task.py`, `task_multi_gpu.py`), `assets/source/model-training-history/*.diff`,
the two notebook extracts, `ASSETS.md`, `digest.md` (§2, §3, §7, §9 and §10 errata and open
questions), `SLIDES.md`, and the tools' behaviour (Vertex AI custom jobs, worker-pool specs and
prebuilt containers, the Custom Code Service Agent vs the submitting key, gsutil, sdist tarball +
`find_packages`, `tf.distribute.MirroredStrategy` global batch / all-reduce / scope, `wandb.login` /
`init(config=…)` / module-attribute `wandb.config` / `run.save`, Colab secrets). Line numbers are file
lines (capture line 1 = the `$` command); `script.md:N` points at the quoted line.

**Verified clean (no finding):** every TERM range and highlighted line: laptop 00:4–5; 01:2; 02:2;
03:7–23 (`.sh` rows 9/11/16/17/19, `cli.py` 10, `package` 18, PNGs 12–15/21/23); 04; 05:2–6;
06:2–5 (415 B never highlighted); 07:5, 15; 08:5, 17; 09:2–7 (4.31 / 8.93 / 7.61 GB); 10:2 (`40`);
11:2 (`0`); 20:2–6 (5–6); 21:23, 65–70, 166, 181–188 (22 distinct `Err:` packages, step 2/14,
`Dockerfile:18`); 22:2–3; 23:330, 344–348, 356, 372–378 (step 8, `Dockerfile:36`/37); 24:2–4;
25:2–4, 11–12, 20–21; 26:3, 19, 32, 34–41, 43–45, 47, 49–52, 54, 61, 64, 66–69 (314.2 s ≈ 5 min;
28–31 never printed); 27:2–3 (2.59GB); 30:43–52, 54 (4016), 56–63 (10253); 31:2–5 (`root`,
`.gitignore:4`); 40:43–44, 47, 58, 64–66, 69, 75–77; 50:43–44; 60:43, 47–48, 51–52, 119;
70:34–41, 43, 45; 71:34; 80:2, 68; 82:2–3, 7, 19, 26; 83:2, 7–9; 84:14; 85:2; 86:4; 87:14;
90:2; 91:2–7; colab C05:2, 4–5; C05b:2 (0.31.0); C38:2–9, 16–17; C38b:3–4, 16–17. Crops match the
files (`[IP: …]` tails, ProxyError lines 84:2/86:2/86:5/87:2, container ids, the job hex, BuildKit
sha lines, image IDs). Every CODE range and highlight: `Dockerfile` 1–2; `docker-shell.sh` 3, 12–24
(14, 17, 18–19, 20–23); `docker-entrypoint.sh` 13–19; `package-trainer.sh` 1–4; `cli.sh` 5–19, 21–37,
9–14, 30–37, 31; `cli-multi-gpu.sh` 4–16 (6, 8, 10, 11–12, 16); `cli.py` 7; `setup.py` 5–13 (5, 11);
`task.py` 45–54 (52), 60, 96–100, 152–153, 312–322, 326–331, 335–338 and the log-shape gutter lines
57, 61, 67, 94, 102, 107, 122, 148–150, 263, 269, 274, 308, 314, 321, 333, 336, 341;
`task_multi_gpu.py` 275, 286–301 (287–289, 293), 303–321, 324–334, 338–343; `88f3374.diff` 30–36
(34); commit times 10:34:01 → 11:25:19 = 51 min. README cards 17, 25–39, 43–44, 55–58, 62, 71, 80,
93–94, 100–101, 110, 114–115, 128–129, 136–142, 150, 152–154, 157–158, 161–163, 170 (line 96 is never
shown or quoted). Notebook lines A 101/106/112 → 115/117/120, 137, 318, 352–353, 432–447 (436, 439),
527–528, 242/245/249/289/307, 1272, 1280, 1283–1295, 1304, 1396–1402, 1437–1442; B 37, 254/257,
373–375, 409–410, 502–504, 603–606, 614–615, 696–705, 710–716, 732, 773, 781–782, 1009–1021, 1629,
1703–1715, 1819–1820. Numbers: 1,156 / 936 / 104 / 116 (ceil splits); 68.97 / 67.24 / 62.93 and
epochs 15 vs 10; 0.86 points = 100/116, "two photos" = 80 vs 78; 25 epochs and 0.72436 / 0.45192
in the 2_block history; 0.22.2 vs 0.31.0; 510 MB (digest: 509,683,967 B); 4 KB tarball; eight tar
entries; 22 packages; Python 3.13.17, uv 0.13.5, SDK 590.0.0, aiplatform 1.120.0, Docker 29.8.2, git
2.54.0; 40 / 2 / 47 characters; global batch 64, 15 steps = 14 × 64 + 40, 32 per GPU; n1-standard-4,
n1-standard-32 + 2 × T4. Causal claims verified: `set -e` in `docker-shell.sh` skipping `docker run`
and its absence in the entrypoint; the bullseye-security 404s vs archive.debian.org (ASSETS:18–26,
250–255); `google-cloud-sdk` → `google-cloud-cli`; x86_64 under `--platform=linux/amd64`; root
prompt (user `app` never switched to); `find_packages` + `__init__.py`; the `/app` bind mount making
"re-package, don't rebuild" true; `package-trainer.sh:4`'s fixed object name; `sh -x` showing the
GPU image overridden at `cli.sh:31` and the key in `--args`; exported variables not surviving a new
shell; the empty key → `api_key not configured (no-tty)` after the download (`task.py:96` before
`:153`); `"16"` → `yours was 2`; `cli.py` needing `GCP_REGION` and sending no key; the name
`Conflict`; `wandb.config = {...}` rebinding the module name (C38/C38b, digest §3.2);
`wandb.run.save("test")` as a file-glob upload; callback-only curves in notebook B (E15) and the
shared `mobilenetv2_train_base` display name; the string sort (E22); the unseeded split (E4);
`os.listdir` label order (E19, A 352 vs B 409); no `model.save` (E6); the stray `None`; slide 23's
`epochs=25`; the two-images-same-name double submit; `tf-cpu` + T4 → `GPU Available:  []`, GPU
billed (digest §3.6); MirroredStrategy's three edits, `num_workers` = replicas, variables mirrored
inside the scope; L14 Cloud Run / L15 saving the model and reusing the SDK route (digest §7, B16).
Honest framing: every failure shown is the captured one; no `JOB_STATE_SUCCEEDED`, "submitted",
`gsutil cp` success or GPU success line appears; every `recorded`, `extra · local stand-in`,
`illustration` and `stand-in` tag sits on the right panel (with the A8 exception). No price
anywhere. No real person's name, e-mail, W&B user or team (`<W&B user>`, `<team>` throughout); the
instructors' `ac215-project` / `cheese-app-trainer` / `cheese-app-models` appear only in quoted
README/notebook lines and `08`, each with "replace this with yours" (coordinator decision), never as
ours; the CODE windows on `docker-shell.sh` (3, 12–24) avoid lines 8–9.

---

## Findings

### Wrong

**A1 · S09 (and S11) · wrong** · "TensorFlow, scikit-learn and requests are not declared: they are
assumed to come from the image Google provides, and scene 11 tests that." (`script.md:706`; SHOW
`:702–703` ORANGE layer "TensorFlow · scikit-learn · requests — assumed from Google's image")
· Evidence: `requests` arrives with the tarball, as a dependency of `wandb==0.15.11`:
`80-standin-pip-install.txt:69–70` ("Installing collected packages: … requests …",
`requests-2.34.2`) and `82-standin-pip-list.txt:19`. S11 itself then says "pip list shows wandb,
requests and their helpers" (`script.md:838`), contradicting S09. The digest's E12 (and BRIEF:88,
:449) predate the capture; the captures win.
· Fix: SAY "TensorFlow and scikit-learn are not declared at all: they are assumed to come from the
image Google provides. Requests is not declared either; it only arrives because wandb needs it."
ORANGE layer: "TensorFlow · scikit-learn — assumed from Google's image", plus a GREY chip "requests:
via wandb". (See A3 for "scene 11 tests that".)

**A2 · S10 · wrong** · GOLD `cost_tag()` "the job's VM bills from submission until the script exits"
(`script.md:794`) and SAY "from submission until the script exits, the job's machine bills your
project" (`:796`)
· Evidence: `digest.md:120` and `BRIEF.md:698` both say "from provisioning until the script exits"
(BRIEF:492 has the slip the script copied). A custom job waits in QUEUED/PENDING before its VM is
provisioned (digest §3.4 job states); that wait is not machine time.
· Fix: tag "the job's VM bills while it is up: from provisioning until the script exits · see the
Vertex AI pricing page"; SAY "A gold tag: once its machine is provisioned, until the script exits,
the job bills your project. Check the Vertex AI pricing page."

### Misleading

**A3 · S09, S11 · misleading** · S09 "…and scene 11 tests that" (`script.md:706`, chip "scene 11
tests it" `:704`); S11 "but no TensorFlow and no scikit-learn: those come from the prebuilt image
Google still serves" (`:838`)
· Evidence: scene 11 shows only that the tarball does *not* bring them (`82`, `83:9`); nothing pulls
or inspects Google's image (`09` reads manifests only). ASSETS.md:288–290: "Whether they still
contain scikit-learn, requests or a working `wandb==0.15.11` import was not checked"; digest §10
lists it as open. TensorFlow is implied by the image name; scikit-learn is not verified.
· Fix: S09 "…and scene 11 shows the tarball does not bring them." S11 "…no TensorFlow and no
scikit-learn: the trainer counts on the prebuilt image for those, which we could not pull to
check." Chip under the ORANGE slot: "expected in tf-cpu.2-17 · not verified here".

**A4 · S12 · misleading** · "Metrics, only the execution time." (`script.md:900`; SHOW `:896`
"metrics ◐ ('only execution_time')")
· Evidence: `execution_time` is written with `wandb.config.update` (`task.py:336`), so it lands in
the run's **config**, not its metrics; there is no `wandb.log` and no callback (`task.py:326–331`),
so the run logs zero metric series. SLIDES.md:186 keeps the qualifier "(stored in config)"; digest
E1 lists it separately from metrics. The ledger already shows it as a config chip
(`execution_time ← :336`, `script.md:886`), so the answer contradicts the row.
· Fix: SHOW "metrics ✗ ('execution_time is in config · no metric logged')"; SAY "Metrics, none:
the execution time goes into the config."

**A5 · S09 · misleading** · "On the host it belongs to root, because the container wrote it"
(`script.md:728`; SHOW `:727` `root` YELLOW)
· Evidence: true on the recording's Linux engine (`31:2`). ASSETS.md:267–269: "On a Mac the owner
column differs. Do not make it load-bearing." Docker Desktop's file sharing on macOS (and Windows)
presents files written through a bind mount as owned by the host user.
· Fix: SAY "On our Linux engine it belongs to root, because the container wrote it; on Docker
Desktop you'll see your own user. Either way git ignores it." Chip on `root`: "Linux engine · on a
Mac: your user".

**A6 · S11 · misleading** · "Our 40 character placeholder passes." (`script.md:847`; SHOW `:845–846`
`TERM(laptop/86: 4)` GREEN)
· Evidence: the container runs with `--network none` (`86:1`); `wandb.login(key=…)` in 0.15.11 only
checks the length and writes `~/.netrc` (`86:3–4`; `84:12–13` shows the check is the local
`apikey.write_key`). Nothing asked W&B whether the key is valid; an obviously fake key would be
refused when `wandb.init` reaches api.wandb.ai. GREEN + "passes" reads as a working login.
· Fix: SAY "Our 40 character placeholder passes the length check; nothing here asks W and B whether
it is real." Chip on 86:4: "length check only · offline"; colour it YELLOW or GREY, not GREEN.

**A7 · S11 · misleading** · SHOW "`TERM(laptop/80: 2, …, 68, 70 cut)`; `cheese-app-trainer-0.0.1` and
`wandb-0.15.11` YELLOW" (`script.md:827–828`; also the scene-author note `:257`)
· Evidence: `80:70` is 339 characters; `cheese-app-trainer-0.0.1` starts at column 123 and
`wandb-0.15.11` at 327. `cut` prints only the first 65 (`script.md:82`, `:106`), which ends at
"…PyYAML-6.0.3", so neither highlighted package is on screen while the SAY names both.
· Fix: `70 wrap` (6 rows in the small strip), or keep `70 cut` and move the two highlights to the
next panel's `82:7` and `82:26` (already printed), saying so in the SHOW line; update `:257`.

### Polish

**A8 · S11 · polish** · `for i in tf-cpu.2-17.py310 …` → `TERM(laptop/09: 2–3)` shown while the
tracker reads `extra · local stand-in` (`script.md:823`, `:832–834`)
· Evidence: `09` is a live `docker manifest inspect` of Google's real images, not a stand-in
(ASSETS.md:125); the stand-in tag list (`script.md:167–169`) covers `80`–`87` only.
· Fix: tag that strip plain `extra` (as S13 does for the same capture, `:916`).

**A9 · S11 · polish** · "…and on Vertex that comes after the paid data download." (`script.md:847`)
· Evidence: the download is a free GitHub release (`task.py:96–100`); what costs is the VM's time
while it downloads (digest §2 "a job that fails late, for example after the 305 MB dataset
download").
· Fix: "…and on Vertex that comes after the data download, on billed machine time."

**A10 · S11 · polish** · "your project's Vertex AI service agent" (`script.md:809`, `:813`)
· Evidence: a project has two Vertex agents; the one that runs custom-training code by default is the
**Vertex AI Custom Code Service Agent** (`service-<project-number>@gcp-sa-aiplatform-cc.iam.gserviceaccount.com`,
digest §3.5). A student searching IAM for "Vertex AI Service Agent" finds the other one, which is the
wrong identity to grant in the 403 case (`:821`).
· Fix: badge text "Vertex AI Custom Code Service Agent · service-…@gcp-sa-aiplatform-cc" (spoken
wording can stay "your project's Vertex AI service agent").

**A11 · S14 · polish** · "here it fails at the same login, with no fake success" (`script.md:993`)
· Evidence: `50:44` is gcloud's "You do not currently have an active account selected"; "login" right
after S11's W&B login beats invites the wrong reading.
· Fix: "here it fails the same way as cli.sh, with no active account, and we show no fake success."

**A12 · S07 · polish** · "…and six console pictures this video redraws" (`script.md:552`; chip
"console screenshots" `:551`)
· Evidence: of the six PNGs (`03:12–15, 21, 23`) four are console quota pages;
`serverless-training.png` is the README's architecture diagram (README:4) and `wandb-api-key.png` a
W&B page (ASSETS.md:46–48).
· Fix: SAY "six pictures, screenshots and a diagram, that this video redraws"; chip "screenshots and
a diagram · redrawn in this video".

**A13 · S04 · polish** · "Cells 55 to 60 build the second table from the opening." (`script.md:447`)
· Evidence: the table is cell 55 alone (`NB(B: 1677–1715)`); cell 57 picks the best model and 59–60
run predictions (cell headers at B 1677, 1720, 1729, 1755).
· Fix: "Cell 55 builds the second table from the opening."

**A14 · S15 · polish** · SHOW "`CODE(package/trainer/task.py: 27–30)` small, '--model-dir: parsed,
never used'" (`script.md:1009`)
· Evidence: `--model-dir` is lines 27–29; line 30 is `--lr`, which is also ignored
(`learning_rate = 0.001` hard-coded at `task.py:274`; digest E5).
· Fix: `CODE(task.py: 27–29)`, or keep 27–30 with the chip "--model-dir and --lr: parsed, never
used".

**A15 · S13 · polish** · "`accelerator-type=NVIDIA_TESLA_T4,accelerator-count=1` in the worker pool,
from line 26" (`script.md:909`)
· Evidence: `cli.sh:26` holds `accelerator-type=$ACCELERATOR_TYPE,accelerator-count=$ACCELERATOR_COUNT`;
the values are set at `cli.sh:12–13` (digest §3.6), and S13 shows `CODE(cli.sh: 9–14)` just before.
· Fix: "…from lines 12–13, used on line 26".

**A16 · S05, S14 · polish** · "three lines slide in with the lecture's call-outs: BLUE 'start the
run' … GREEN 'watch the model' … RED 'finish the run'" (`script.md:455–457`) and "each tagged with
the lecture's call-out: BLUE 'create the strategy' … GREEN 'scale the batch' … RED 'build and
compile inside the scope'" (`:961–962`)
· Evidence: the slides say "Initialize wandb run" / "Add a callback to monitor model" / "Let wandb
know to finish the run" (SLIDES.md:40) and "Create distribution Strategy" / "Adjust dataset batch
size" / "Create & Compile model in strategy scope" (SLIDES.md:46).
· Fix: put the slides' wording on the tags (the SAY can keep its paraphrase), or call them "our
labels for the lecture's call-outs".

**A17 · S03 · polish** · SHOW "NB(A: 1400–1402) with the two instructors' names" (`script.md:384`)
· Evidence: those lines hold the instructors' project id and bucket name (`GCP_PROJECT =
"ac215-project"`, `GCS_BUCKET_NAME = "cheese-app-models"`), not people's names; the extract's people
are masked in cell 0. "Names" invites a scene author to look for a person.
· Fix: "with the instructors' project id and bucket name".

**A18 · S03 · polish** · GOLD "model files of 10–104 MB each (the table's model_size)"
(`script.md:387`); SAY "those model files now sit in your bucket, 10 to 104 megabytes each"
(`:389`)
· Evidence: `model_size` is the size of the `.weights.h5` file only (`NB(A: 252–254, 286,
1277–1278)`); each model also writes a `.keras` copy (`NB(A: 242)`) plus small JSONs, so a model
puts roughly twice that in the bucket.
· Fix: tag "weights of 10–104 MB per model, plus a .keras copy of each"; SAY "…those model files now
sit in your bucket, weights of 10 to 104 megabytes per model, plus a copy of each."

**A19 · S11 · polish** · `… wandb.login(key='16')"` → `TERM(laptop/84: 3, …, 14)` (`script.md:844`)
· Evidence: `84:3` is "wandb: W&B API key is configured. Use `wandb login --relogin` to force
relogin", printed *before* the length check fails (`84:12–14`). On screen it reads as a success
line inside a failure.
· Fix: print `84: 14` only (with `…` before it), or keep 3 GREY with a chip "printed before the
check".

**A20 · S09 · polish** · GREY chip "our capture: a fresh cockpit for this step · stay in yours"
placed at `ls -l trainer.tar.gz` (`script.md:723–725`)
· Evidence: the new cockpit starts at `30:42` with `sh package-trainer.sh`, which the scene types
first (`:716`); the conventions put the chip at the first prompt of a new segment (`:91–94`), as S10
(`:759`) and S14 (`:988`) do.
· Fix: move the chip to the `sh package-trainer.sh` prompt.

**A21 · S12 · polish** · "The environment only partly: system charts, while the image tag sits in
cli.sh." (`script.md:900`; SHOW `:895–896`)
· Evidence: besides system charts, a wandb run stores its own metadata (Python version, OS, host
hardware) and by default the installed-package list in the run's files; it does not store the image
tag (`cli.sh:31`). The ◐ verdict is right; the reason undersells what W&B keeps. (Not captured here;
wandb's default behaviour, check a real run's Files tab.)
· Fix: chip "system charts and run metadata · not the image tag (cli.sh)"; SAY "The environment only
partly: W and B notes the machine and Python, while the image tag sits in cli.sh."

### Writer-facing notes (no change required)

- S07's "the README's name returns 401, it belongs to someone else" (`:592`): the 401 text itself says
  "(or it may not exist)" (`08:5`); the inference rests on `07` returning 404 for a missing bucket to
  the same anonymous caller. Correct as stated; keep `07` and `08` side by side so the contrast carries
  it.
- S14's "the two are averaged across a link called all-reduce" (`:973`): Keras scales each replica's
  loss and all-reduces with a sum, which is the same as averaging; digest §3.7 says "summed/averaged".
  Fine for this audience.
- S08's "about 5 minutes here" (`:673`): steps 2–7 were cached from the second attempt (`26:13–18`),
  as they will be for a student who followed the same sequence. Correct.
- S01's "same five models" (`:284`): the hyperparameters also differ beyond the MobileNet epochs
  (notebook A's `2_block` ran 1 epoch, B's 25: `NB(A: 1293)`, `NB(B: 1713)`). Not an error; usable as
  a second "not like for like" pointer if S04 wants one.
- S04's experiments zip "you never use" (`:406`): true with the default `LOAD_PREV_TRAINED = False`
  (`NB(B: 596)`); digest E16 shows the flag would load 3-class mushroom models anyway.

---

**Verdict: 2 wrong · 5 misleading · 14 polish (A1–A21). No TERM file,
line range or crop is wrong, no CODE/README/notebook citation is wrong (A14 and A15 are window/line
precision), no number lacks a source, no price, no real name/user/team, README:96 never shown, and no
success is shown where only a failure was captured. Fit for scenes after A1 and A2 (one requests
claim, one billing start) and A3–A7 are applied; the fixes are near word-neutral (A1 +10 words,
A5 +9, A6 +6, A3 +6; A4 is shorter).**
