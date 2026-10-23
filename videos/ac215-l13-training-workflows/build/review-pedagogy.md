# Review · lens 2 — newcomer pedagogy

Script at commit 1d1134b (`claude/ac215-l09-l13-batch`), read start to finish at viewing pace as
the BRIEF's target viewer. This viewer has done L01–L11: a GCP project with billing, images,
containers, bind mounts and `docker-shell.sh` scripts, training and fine-tuning in Colab (L8),
service accounts and JSON keys in `../secrets`, buckets, and a DVC-versioned dataset. They are new
to experiment tracking, W&B, packaging a notebook, Vertex AI custom jobs and prebuilt containers,
the identity that runs a job, GPU quotas and multi-GPU training.

Read against `BRIEF.md` (V1–V7, the ponder table, recap questions, outcomes),
`docs/AC215_SERIES.md` (rule 4: concept before command), `docs/STYLE_GUIDE.md` §1 (≤3 groups, one
idea per beat, picture before formula) and the AGENTS.md content gates. Notebook extracts were
opened where a beat's teaching depends on what the notebooks printed:
- `nbA:1283-1295` and `nbB:1703-1715`, the two tables;
- `nbB:710-716` vs `:940-945`, two `model.fit` calls;
- `nbA:352` vs `nbB:409`, the label orders.

Code checked: `cli.sh`, `task.py:40-68`, `task_multi_gpu.py:286-343`.

Narration now: **4,239** words (`python -m explainer.script`, which agrees with the script). The
ceiling is 4,300, so every addition below names its cut. The ledger at the end balances to
**4,276**, with every scene inside the BRIEF's ±15 %.

## Gate checks

**Gate 1 · the hook.** S01 is a real puzzle. Two tables come from the same pipeline, the same
1,156 photos and the same five models, and they crown different MobileNets at the same 68.97 %. The
narration points at the `epochs` column without explaining it. The payoff exists, but in pieces:
- S03: the unseeded split, and a two-photo margin;
- S04: 10 vs 15 epochs, "not a fair comparison";
- S12: "exactly why tables A and B could not be compared".

The question as asked, "which recipe is better?", never gets a verdict. The strongest evidence is
sitting in the two tables and is never used: the frozen MobileNet, same settings and same 15 epochs,
scores 67.24 % in A and 68.97 % in B. That is two photos of pure run-to-run noise, exactly A's
winning margin. S03's "notebook A wins by two photos" also reads as "notebook A beat notebook B"
(P2).

**Gate 2 · one animated mechanism per core idea, intuition before formalism.**

| core idea | mechanism | verdict |
| --- | --- | --- |
| a home-made tracker | V2 folder → five files → table | real, strong |
| an unseeded test set | S03 tile strip reshuffles, "1 photo = 0.86 points" | real, strong (the best beat of part 1) |
| runs on a shared axis, curves need a callback | V2 slots + PURPLE pipe | real. The ponder before it asks for something never shown (P4) |
| `wandb.config = {…}` goes nowhere | V3 sticky label peels onto a loose dict | real, strong; predict → picture → proof |
| serverless = rent the machine | S06 tile + GOLD meter, V4 step 1 | real. The full trip is never assembled (P1) |
| packaging | V4 step 2 box, tar, gzip | real. What `setup.py` is *for* is unsaid (P9) |
| submitting | V4 step 3 spec card | real, but it flies at the end of S10, after the command (P15) |
| **the job's first minute on Vertex** | BRIEF V4 step 4 (Google's VM, image, `pip install`, `python -m trainer.task` with argv) | **missing**: only the laptop stand-in plays (P1) |
| submitter vs runner | V5 badges | real. The ponder's answer is shown before it is asked (P8) |
| GPU = three switches | V6 | real, strong |
| data-parallel training | V7 split, all-reduce, mirrored update | real, but plays *after* the code it explains (P7) |
| the model never comes back | V4 step 5 ghost | real |

**Gate 3 · ponders and recap.** There are 11 ponders and 1 quick predict, about one every
2.5 minutes. Audit:

| # | scene | answerable from what was shown? | answer lands? |
| --- | --- | --- | --- |
| 1 | S03 | yes: both `test_size=test_percent` are on the panel | yes |
| 2 | S04 | **no**: only `wandb.init` was on screen, so "callback" is a guess (P4) | yes, but "callback" is unglossed (P4) |
| 3 | S05 | as a predict, yes (it expects a wrong guess) | yes, strongly (V3 + `C38`) |
| q | S06 | yes, from "the image is Google's" | yes |
| 4 | S07 | yes (shell basics, L2–4) | yes |
| 5 | S08 | yes (FROM, from L2) | yes |
| 6 | S09 | yes (S08's `/app` mount + S06 "Google's image") | yes |
| 7 | S10 | guessable; the job page was never shown | yes |
| 8 | S11 | **given away**: block 2 names the service agent as "runs the job" | it repeats block 2 (P8) |
| 9 | S12 | yes, but "system charts" was never explained, though "environment: partly" rests on it (P10) | yes; it lands inside a dense block |
| 10 | S13 | yes (V6 just played) | yes |
| 11 | S14 | yes (global batch 64 just drawn) | yes |

The content recap exists (S15, V1 relit), but it is a list of picture labels: "three badges,
three switches". A newcomer replays names, not ideas (P21).

**The recap against the outcomes.**
- Tested: Q1 is outcome 1, the record's gaps. Q2 is outcome 3, the trip, but the video never says
  it in one place (P1). Q3 is the config half of outcome 2. Q4 covers outcomes 5–6 (identity, the
  key). Q5 is the mirrored half of outcome 7. The GPU switches are ponder 10, and the missing model
  is S15's beat, both as the BRIEF says.
- Untested: callback → curves, the cockpit only submits, and an un-exported key failing *after*
  the download. Route them to exercises.md (P22).

**The part 1 → part 2 bridge.** S07 closes well: what is lit, and the teaser "today it won't
build". S08 then opens with "Part 2 starts in the repo" and goes straight to `sed`. Part 2 has no
sentence of purpose, and its main noun, "cockpit", was never defined in part 1 either (P1, P3).

**Where a newcomer gets lost or bored.**
- **Lost: S06 → S11.** The pieces of the serverless trip are scattered over five scenes: flags in
  S06, the tarball in S09, `--python-package-uris` and `--args` in S10, `pip install` in S11's
  stand-in. Nobody ever says the chain "Vertex starts a VM with Google's image, installs your
  tarball, runs `python -m trainer.task` with your flags, deletes the VM". Recap Q2 asks for exactly
  that chain (P1).
- **Lost: S10.** "Worker pool spec" and "replica count" arrive unglossed. "Replica" then means
  something else in S14 (P6).
- **Lost: S14.** The code's three edits come before the picture that explains them (P7).
- **Bored: S04.** Seven blocks, about 4 asides each worth a chip, not a sentence: the 510 MB
  zip, the two same-named runs, `wandb.finish`, the slide-16 screenshot. The fixes trim them (P2,
  P23).
- **Bored: S13.** Three image sizes and a second "nothing to show" apology. The S07 note already
  carries the sandbox framing (P20).

---

## Blocking

P1 · S06 → S10 → S11 · blocking.
- **Quotes:**
  - S06: "Step two packs that file and uploads it to a bucket. Step three runs from what the lecture
    calls the Model Trainer CLI Container, on your laptop, which asks Vertex AI for a job. Each job
    runs in its own container…"
  - S10: "points at your package and module".
  - S11: "We can't run Vertex here, so we replay the job's first step on the laptop".
- **Issue:** BRIEF outcome 3 is one chain: a tarball goes to a bucket, Vertex starts a VM with
  Google's prebuilt TensorFlow container, `pip install`s the tarball, runs `python -m trainer.task`
  with flags, and deletes the VM. The video never says it in one place.
  - The BRIEF's V4 step 4, the real job on Google's VM, is never drawn. S11 plays only the laptop
    stand-in, so a viewer can come away thinking the job runs in a plain `python:3.10` container.
  - "Your package" in S10 has no visible referent: the viewer must infer that it is the tarball's
    `gs://` path.
  - Three nouns the whole of part 2 stands on are never glossed: "cockpit" (first spoken in S06's
    quick-predict answer, with no link to "Model Trainer CLI Container"), "tarball" and "prebuilt".
  - Recap Q2 asks for this chain.
- **Fix, three edits:**
  - **S06 block 4 (+18):** "Step two packs that file into a tarball, one compressed archive, and
    uploads it to a bucket. Step three runs from what the lecture calls the Model Trainer CLI
    Container, our cockpit on your laptop: it asks Vertex AI for a job. Vertex AI then starts a
    machine, CPU only or with one T4. It loads Google's prebuilt TensorFlow image, installs your
    tarball, runs your trainer with your flags, and deletes the machine." On screen, one job tile
    plays V4 step 4 in miniature, in step with the clauses.
  - **S06 block 5 (−6):** "And the image is Google's, not yours." This replaces "And the image that
    runs the job belongs to Google, not to you.", which the new block 4 already says.
  - **S10 block 1 (+6):** "points at your tarball in the bucket and the module to run," in place
    of "points at your package and module,". Line 10 (`PYTHON_PACKAGE_URI=$GCS_BUCKET_URI/…`)
    lights.
  - **S11 stand-in block (+10):** "On Vertex, the job's first step installs your tarball into
    Google's image. We can't run Vertex here, so we replay that step on the laptop, tagged as a
    stand-in." Before the dashed stand-in container, the real V4 step 4 plays once, GREY tag
    "what Vertex does · drawn, not recorded", no output panels: the VM, the ORANGE image, the
    tarball unwrapping, `pip install`, then `python -m trainer.task --model_name=mobilenetv2
    --train_base --epochs=2 --batch_size=32 --wandb_key=…`. The `--args` string from S10 splits at
    its commas into argv tokens that land on S09's `task.py` flag lines. The dashed stand-in then
    replaces the BLUE VM, which makes the swap visible.

P2 · S01 → S03 → S04 → S12 · blocking.
- **Quotes:**
  - S01: "So which recipe is better, fine-tuning or freezing? … Hold that question."
  - S03: "and notebook A wins by two photos".
  - S12: "That is exactly why tables A and B could not be compared".
- **Issue:** gate 1 asks for the hook to be paid off. The pieces exist, but the question as asked
  never gets an answer, and S12's line is about the *repo* run, which the viewer must transfer to
  the notebooks alone. "Notebook A wins by two photos" sounds like A beat B. The cleanest evidence
  is unused: the frozen MobileNet, same settings (lr 0.001, batch 32, SGD, 15 epochs) in both
  tables, scores **67.24 % in A and 68.97 % in B** (`nbA:1283-1295`, `nbB:1703-1715`). Same
  recipe, two photos apart, the exact size of A's winning margin. A newcomer can leave believing
  fine-tuning won (A) or that W&B fixes it.
- **Fix, three edits:**
  - **S03 hook block (+2):** "One photo is worth 0.86 points, and notebook A's winner leads by just
    two photos." This replaces "…and notebook A wins by two photos."
  - **S04 last block, split into two blocks (+25 −12):**
    - Block 1 keeps the table and epochs sentences, then adds: "Now the frozen MobileNet: same
      settings and epochs, 67.24 in A, 68.97 here. Two photos apart by chance alone: the size of
      the winning margin." On screen, both frozen rows ring YELLOW, with the chip "same settings ·
      15 epochs · 2 photos apart". 67.24 goes to the lexicon candidates beside 68.97.
    - Block 2 is upload only: "To upload, edit the bucket and project inside cell 13, then run
      cells 64 and 66."
    - Cut "The lecture's dashboard comes from an earlier project; yours will say cheese." (−12).
      The slide-16 chip stays on screen.
  - **S12 last block (+16):** "Notebook A's folder misses the same three. So the opening's answer:
    these tables cannot crown a recipe. Seed the split, match the epochs, keep the code version,
    then compare. Exercise 1 adds a small callback." This replaces "That is exactly why tables A and
    B could not be compared, and exercise 1 adds a small callback." On screen, S01's YELLOW question
    card returns small, and its "?" resolves to "can't tell · yet". The chip "exercise 3: seed the
    split" sits beside "exercise 1".

## Confusing

P3 · S07 → S08 · confusing.
- **Quote:** S08 block 1: "Part 2 starts in the repo. Put your bucket and project on lines 8
  and 9…"
- **Issue:** parts may be watched separately. Part 2 opens on `sed` with no sentence of what part 2
  does, and leans on "cockpit", a nickname given once, in passing.
- **Fix (+13):** "Part 2 ships the trainer: build the cockpit, pack the code, send one job. It
  starts in the repo." This replaces "Part 2 starts in the repo." On screen, V1's repo lane flashes
  in the three spoken stages (cockpit → bucket → job tile), then dims.

P4 · S04 · confusing.
- **Quote:** "But the stored history shows curves only for the two block run. Something to ponder:
  what do the other four lack?" → "A callback."
- **Issue:** only `wandb.init(project=…)` was on screen. The viewer has never seen a `model.fit`
  call in notebook B, so "a callback" can only be guessed, and gate 3 wants ponders answerable from
  what was shown. "Callback" is also unglossed: the three-line pattern that names it comes a scene
  later, in S05.
- **Fix:**
  - **Before the ponder, on screen (+4):** NB(B: 710–716) beside NB(B: 940–945). These are the
    `2_block` cell's `model.fit` and the next cell's, identical but for line 715, and neither is
    highlighted. New SAY: "But only the two block run shows curves. Compare its model fit call with
    another cell's. Something to ponder: what do the other four lack?" Line 715 lights only in the
    answer.
  - **The answer (+5):** "A callback: code that model fit calls after every epoch. Only the two
    block cell passes the W and B callback, so only its loss and accuracy arrive, epoch by epoch."

P5 · S07 · confusing.
- **Quote:** "Then request GPU quota: filter for custom model training, pick T4 GPUs per region,
  choose regions, set a new limit and submit."
- **Issue:** "quota" is never said to be a per-region allowance, though S13's third switch ("quota
  … in this region") and S14's "32 virtual CPUs" depend on it. A follow-along viewer may also
  request a region `cli.sh` doesn't use: line 14 is `us-central1`, and its own comment says to
  match it.
- **Fix (+10):** "Then request GPU quota, your GPU allowance per region: filter for custom model
  training, pick T4 GPUs per region, choose regions including us-central1, where cli.sh runs, set a
  new limit and submit."
- **Funded in-scene (−11), since S07 sits at +14.5 %:** "Two extras show the course pin and the
  repo's files." This replaces "Two extras show the course pin, then five shell scripts, cli.py,
  the package folder and six console pictures this video redraws." The YELLOW rows and the chip
  "console screenshots · redrawn in this video" carry the list.

P6 · S10 → S14 · confusing.
- **Quotes:**
  - S10: "the worker pool spec with machine, replica count, image and module".
  - S14: "multiplies the batch size by the number of replicas, here GPUs, not machines".
- **Issue:** "worker pool spec" and "replica count" arrive with no gloss, and S13 reuses the first
  ("one T4 in the worker pool spec"). Then "replica" changes meaning. In `cli.sh`
  `replica-count=1` is machines; in S14 a replica is a model copy on one GPU (and S03 already
  showed `Number of replicas: 1`). A newcomer will conflate them, and S14's chip alone cannot undo
  that.
- **Fix:**
  - **S10 (+7):** "Then the full command: the worker pool spec, the job's machine order: machine
    type, one replica, meaning one machine, image and module; then the arguments, ending with your W
    and B key in plain text."
  - **S14:** the replica gloss lands in V7 (P7: "…an identical copy of the model, called a
    replica").
  - **S14 opening (0):** "but only to count GPUs" in place of "but only to count replicas", so the
    word's first S14 use is the defined one.

P7 · S14 · confusing.
- **Quote:** block 3 "It makes the three changes of the lecture: it creates the mirrored strategy,
  multiplies the batch size…, and builds and compiles the model inside the scope", then block 4,
  V7: "Here is what that buys."
- **Issue:** series rule 4 and the style guide's picture before formula. The viewer reads
  `global_batch_size = args.batch_size * num_workers` and `with strategy.scope():` before seeing
  why a batch is split or what a mirrored variable is. Three more terms are thin:
  - "global batch" is used without a gloss;
  - "mirrored" is explained only by its name;
  - "a model built outside stays single" never says what goes wrong.
- **Fix: reorder.** Ladder → V7 → G1 `cli-multi-gpu.sh` → G2 `task_multi_gpu.py` → ponder 11 →
  caveats → G3/G4. The README order of G1 → G2 is kept; V7 moves ahead of both.
  - **V7 SAY (+9 +6):** "Here is the idea. Each GPU holds an identical copy of the model, called a
    replica. A global batch of 64, what both GPUs take in one step, splits into two halves of 32;
    … Variables created inside the scope are mirrored, one synced copy per GPU; a model built
    outside is not copied."
    - Lens 1 should confirm the last clause for TF 2.14 / Keras with `MirroredStrategy`. Otherwise
      use "a model built outside is not mirrored" (same count).
  - **G2 SAY (−5):** "Then review the multi-GPU trainer: the picture, as the lecture's three
    changes. It creates the mirrored strategy, multiplies the batch size by the number of replicas,
    and builds and compiles the model inside the scope of the strategy. Model fit is unchanged." The
    chip "num_workers counts GPU replicas here, not machines" stays.

P8 · S11 · confusing.
- **Quote:** block 2: "The second badge belongs to Google: your project's Vertex AI service
  agent, which runs the job by default." Then Ponder 8: "…your key file never left your laptop.
  How?"
- **Issue:** the ponder's answer is spoken 20 s before the ponder, so the timer asks the viewer to
  repeat a sentence. "Service agent" is never set against what the viewer knows from L10, a
  service account: is it one, and whose?
- **Fix: reorder.** Badges 1 and 3 first, the middle lanyard empty with a GREY "?", then the
  ponder; badge 2 is the answer.
  - **Block 2 (−12):** "The third is your W and B key, for a different building altogether,
    carried by hand inside the job's arguments. The middle lanyard is still empty."
  - **Answer (+15):** "The second badge: your project's Vertex AI service agent, a service account
    Google manages. By default the job runs as it, and it can open buckets in the same project. Your
    key only proved who submitted. If a job ever gets a 403 on your bucket, that is the identity to
    grant access."

P9 · S09 · confusing.
- **Quote:** "Review setup.py; pause and open it. The only declared dependency is wandb… so python
  dash m trainer dot task works."
- **Issue:** the BRIEF lists "turning a notebook into a pip-installable package" as new. The
  script never says what `setup.py` is for (pip reads it when installing the tarball), or *where*
  `python -m trainer.task` works (on the job, after the install, from any folder). Without that,
  S11's `pip install /tmp/trainer.tar.gz` is a new idea, not a confirmation.
- **Fix (+10 +2):**
  - "Review setup.py; pause and open it. It is the label pip reads to install the tarball. The only
    declared dependency is wandb, pinned to 0.15.11."
  - "…so once installed, python dash m trainer dot task works."

P10 · S04 → S12 · confusing (0 words).
- **Quote:** S04: "Without one, wandb init gives you system charts, never your curves." S12 Ponder 9
  answer: "The environment only partly: system charts…"
- **Issue:** "system charts" is never said to be the machine's CPU, GPU and memory, so the ponder
  answer "environment: partly" reads as arbitrary.
- **Fix (0 words):** a GREY chip on the S04 line, "system charts = CPU · GPU · memory over time",
  repeated small on S12's "system charts" chip.

## Polish

P11 · S01 · polish.
- **Quote:** "Then the winner leaves Colab."
- **Issue:** it says "the winner" one sentence after asking whether there is one. The
  `train_base_True` = fine-tuned link, which S10's `--train_base` and S12's run name need, is never
  made.
- **Fix (+4):** "Then notebook A's pick, the fine-tuned MobileNet, leaves Colab." On screen
  (0 words), a GREY chip under the tables: "train_base True = fine-tuned · False = frozen".

P12 · S01 · polish.
- **Quote:** the last block, with the checklist, a GOLD tag, the seven tracker titles, four tag
  kinds in sequence and the two words.
- **Issue:** 5+ groups in the cold open.
- **Fix:**
  - **On screen (0 words):** show only the `▶ your turn` tag; the other tags explain themselves on
    first use.
  - **SAY (−4):** "A yellow tag means pause and run it, and the study guide has every command." This
    replaces "Seven trackers follow along, a yellow tag means…"

P13 · S05 · polish.
- **Quote:** "…removed the callback, 51 minutes after the image moved to a newer TensorFlow, without
  saying why."
- **Issue:** this is trivia, and it invites a guess the video doesn't make.
- **Fix (−10):** "…removed the callback, without saying why." The GREY chip keeps the timing.

P14 · S08 · polish.
- **Quote:** "The script's set dash e then skips docker run."
- **Issue:** the line is used twice (S08 blocks 3 and 6), and L2–4 viewers may not know `set -e`.
- **Fix (+3):** "The script's set dash e, stop on error, then skips docker run."

P15 · S10 · polish (0 words).
- **Issue:** V4 step 3, the spec card flying to Vertex, plays in the last block, after `sh cli.sh`
  and `sh -x`. Rule 4 wants the picture first.
- **Fix:** play the card's assembly over block 1's `cli.sh` review, one chip per spoken item, so
  `sh -x`'s trace confirms it. The last block keeps only the tile, the GOLD meter and the tag.

P16 · S10 · polish (0 words).
- **Quote:** "exit any old cockpit first, or the name conflicts".
- **Issue:** "the name" has no antecedent; the fixed `--name model-training-cli` was GREY in S08 and
  never said.
- **Fix:** "Exit, export, and start again; first exit any old cockpit, which holds the name." (14 →
  14). The chip on `71:34` reads "fixed name: model-training-cli".

P17 · S12 · polish (0 words).
- **Quote:** "The labels line has no fixed order, as the two notebooks show, and no label map is saved."
- **Issue:** a newcomer can't see why this matters. S03's "remember their order" pin is paid off
  silently.
- **Fix:** a YELLOW chip on the two `Labels:` lines, "class 0: brie in A · gruyere in B"
  (`nbA:352`, `nbB:409`). S03's pin icon returns beside it.

P18 · S13 · polish.
- **Quote:** "Back to the optional step, in reverse: what would it take to train on a GPU?"
- **Issue:** "the optional step" was last mentioned three scenes ago, as a flashing tracker caption.
- **Fix (+2):** "Now the reverse of the README's optional CPU step: what would it take to train on a
  GPU?"

P19 · S13 · polish.
- **Quote:** "The image: TensorFlow built for GPUs, with CUDA."
- **Issue:** the image switch carries ponder 10's answer ("no CUDA"), and CUDA is never glossed.
- **Fix (+3):** "…with CUDA, the GPU libraries."

P20 · S13 · polish.
- **Quotes:**
  - "An extra check shows the prebuilt images are still served, at the time of recording: the CPU
    image at 4.31 gigabytes compressed, and two GPU images at 8.93 and 7.61."
  - "This recording has no GPU quota and no account, and the GPU block runs the same create command
    that failed in scene 10. So there is nothing new to show, and nothing we would fake."
- **Issue:** three sizes the viewer cannot use, and a second sandbox apology. The BRIEF's framing
  is "once, in S07, then never apologised for", and the honest line can stay much shorter.
- **Fix (−15 −11):**
  - "An extra check shows Google still serves both GPU images, at the time of recording." The sizes
    stay on screen.
  - "Here the GPU block would fail at the same login as scene 10, so there is nothing new to show,
    and nothing we fake."

  S13 ends at 201, inside its −15 % floor (196).

P21 · S15 · polish.
- **Quote:** "The whole lecture on one map: a folder of runs, runs on a shared axis, config passed to
  wandb init, a tarball that travels while your image stays home, a key inside one command, three
  badges, three switches, and two GPUs in step."
- **Issue:** gate 3 asks for a *content* recap. This is a list of picture names. "Three badges" and
  "three switches" recall nothing unless the viewer already remembers.
- **Fix (+12):** "The whole lecture on one map. A run is only as useful as what it keeps. Curves
  need a callback; config goes into wandb init. Only the tarball travels, into Google's image, run
  as the service agent, your key in its arguments. One GPU needs three switches; two GPUs split the
  batch and average gradients." It is the same relight order, with one sentence per lit group.

P22 · S15 · polish.
- **Quote:** "Answers are in the exercises, every command in the study guide."
- **Issue:** this repeats S01 and the footer card. Three outcomes go untested, as noted in the gate
  check.
- **Fix:**
  - **SAY (−6):** "Answers are in the exercises."
  - **exercises.md (0 words):** one question each for callback → curves (digest exercise 1 already
    does it), "which machine never imports TensorFlow", and "the key was never exported: when does
    the job fail, and what has it cost?" (digest exercise 2).

P23 · S04 · polish.
- **Quote:** "Two more things: both MobileNet runs show the same name, so tell them apart by run ID,
  and no cell finishes the last run, so add wandb finish after cell 52; that one is an extra."
- **Issue:** a two-item aside in the middle of the scene's densest stretch.
- **Fix (−8):** "Both MobileNet runs share one name, so tell them apart by run ID. No cell finishes
  the last run, so add wandb finish after cell 52, an extra."

P24 · several scenes · polish: cuts that fund the fixes above. Each cut removes a sentence whose
content stays on screen.
- **S02 (−5):** "…baseline models is today: early, before the better models." becomes "…baseline
  models is today."
- **S08 (−8):** "Google renamed its apt package, and nothing here needs the Kubernetes plugin
  either." becomes "Google renamed its apt package." The chip "no Kubernetes plugin needed here"
  stays.
- **S09 (−12):** "…and gcloud, gsutil and uv are here, with Cloud SDK 590.0.0 and the Vertex AI
  library 1.120.0, at the time of recording." becomes "…and gcloud, gsutil and uv are here,
  versions on screen." The `at the time of recording` tags stay beside `590.0.0` and `1.120.0`.
  Series rule 5 is met on screen, as L11's review did for its extras.
- **S09 (−6):** "Tar lists eight entries, gsutil prints a new, harmless notice, and the upload
  fails:" becomes "Tar lists eight entries, and the upload fails:". The "new notice · harmless"
  chip stays.
- **S12 (−14):** cut "The README says you'll see the new job, ready to be provisioned to run." The
  README card (`README.md · lines 157–158`) is on screen.

---

## Word ledger

| scene | now | after | BRIEF | Δ vs BRIEF | changes |
| --- | --- | --- | --- | --- | --- |
| S01 | 218 | 218 | 220 | −0.9 % | P11 +4, P12 −4 |
| S02 | 211 | 206 | 220 | −6.4 % | P24 −5 |
| S03 | 304 | 306 | 280 | +9.3 % | P2 +2 |
| S04 | 305 | 319 | 290 | +10.0 % | P2 +25 −12, P4 +4 +5, P10 0, P23 −8 |
| S05 | 252 | 242 | 240 | +0.8 % | P13 −10 |
| S06 | 246 | 258 | 250 | +3.2 % | P1 +18 −6 |
| S07 | 332 | 331 | 290 | +14.1 % | P5 +10 −11 |
| S08 | 342 | 350 | 340 | +2.9 % | P3 +13, P14 +3, P24 −8 |
| S09 | 307 | 301 | 300 | +0.3 % | P9 +10 +2, P24 −12 −6 |
| S10 | 323 | 336 | 310 | +8.4 % | P1 +6, P6 +7, P15 0, P16 0 |
| S11 | 292 | 305 | 300 | +1.7 % | P1 +10, P8 −12 +15 |
| S12 | 267 | 269 | 290 | −7.2 % | P2 +16, P10 0, P17 0, P24 −14 |
| S13 | 222 | 201 | 230 | −12.6 % | P18 +2, P19 +3, P20 −15 −11 |
| S14 | 326 | 336 | 300 | +12.0 % | P6 0, P7 +9 +6 −5 |
| S15 | 292 | 298 | 270 | +10.4 % | P21 +12, P22 −6 |
| **total** | **4,239** | **4,276** | 4,130 | | net +37 |

Parts after the fixes: part 1 (S01–S07) 1,880, part 2 (S08–S15) 2,396. S07 stays at its +15 %
edge, as now. Any further S07 addition needs its own cut (candidate: "an extra listing shows ours",
−5). If the coordinator wants more air, P20's honest line can go to a card only (−24).

---

**Verdict: 2 blocking · 8 confusing · 14 polish (24 findings). The script is fit for scene
production after the blocking and confusing fixes, all inside the word budget (4,239 → 4,276).**
- **Blocking:**
  - The lecture's central mechanism, the serverless trip, is never told end to end, and its real
    picture (V4 step 4 on Google's VM) is replaced by the stand-in. Recap Q2 and outcome 3 stand
    on it.
  - The hook's question never gets a verdict, and the tables already hold the decisive evidence:
    the frozen MobileNet, same settings, two photos apart.
- **The confusing items are mostly order and glosses:**
  - two ponders that are unanswerable (2) or given away (8);
  - V7 after its code;
  - no purpose sentence at the part-2 seam;
  - missing one-clause glosses for quota (with the region trap), worker pool and the two meanings
    of replica, service agent, `setup.py`'s job, and system charts.
- **What works:** the hook is a genuine puzzle. V3 (the config label) and the S03 seed beat are
  the best teaching in the script. V6's three switches and ponders 1, 3, 5, 6, 10 and 11 are
  well-built, and the honest sandbox framing is clear and stated once in S07.
