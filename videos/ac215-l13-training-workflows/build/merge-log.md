# Merge log · script.md review merge (reviews of commit 1d1134b)

Merged by the merge agent on branch `claude/ac215-l09-l13-batch`. Precedence:
accuracy > follow-along > pedagogy > flow/style. Coordinator decisions applied as given: A1–A7
applied; F1 approved (S07 states that the pinned wandb 0.15.11 accepts exactly 40 characters, a
fact about the pin from `84:14` and `87:14`, and the follower checks again in S09 and before S10's
billed submit); F2 treated as must-fix; P1 (the serverless trip told once, V4 step 4 back as a drawn,
not recorded, picture) and P2 (the hook's verdict, with the frozen MobileNet's 67.24 % vs 68.97 %)
approved; the two claims handed to lens 1 resolved as below; no "notebook A's" anywhere in SAY or
SHOW. `explainer/lexicon.yaml` untouched (the flow block is already in 09e7e2f).

The two claims handed to lens 1:
- **S14 "copied"** → **"is not mirrored"**. No source in the episode says "copied": digest.md:242
  and :748 say variables created in the scope "become mirrored variables". SAY: "…a model built
  outside is not mirrored." BRIEF V7 synced.
- **S11 "can read buckets in the same project by default"** → **kept**. digest.md:102 says the job
  "runs as Google's Vertex AI service agent in your project, which can read buckets in the same
  project", and :218 names the Custom Code Service Agent (unless `--service-account` is passed).
  Spoken: "By default the job runs as it, and it can open buckets in the same project."

Structure. Scene list and part cut unchanged. Inside scenes:
- S04: the last block is split in two: B5 (table, epochs, frozen-MobileNet evidence) and B6
  (upload). The ponder now shows two `model.fit` calls first.
- S06: block 4 tells the whole trip once.
- S10: the GOLD tag and V4 step 3's flight move from the last block to the submit beat. The final
  block is gone.
- S11: badges 1 and 3, then the ponder, then badge 2 as the answer. The drawn V4 step 4 comes before
  the stand-in.
- S14: ladder → V7 → G1 → G2 → ponder → caveats → G3/GOLD/G4.
- S15: the teardown card puts the cockpit-only lines before `exit`. `tracker_cleanup` is reordered
  to jobs & bucket · cockpit & images · notebooks & keys.

There are still eleven ponders and one quick predict.

After the merge, all re-run on the final file:
- **README/notebook commands.** Every typed command of v1 is still typed, byte for byte. A scan of
  every `` `cmd` → `` in SHOW gives 58 → 59: the one addition is `81`'s line 1, and nothing was
  removed. The first occurrences stay in README order: `!pip install -q wandb -U` (S04), `export
  WANDB_KEY=…` (S07), `sh docker-shell.sh` (S08), `sh package-trainer.sh` (S09), `sh cli.sh` (S10),
  `sh cli-multi-gpu.sh` (S14). Two command texts appear on cards, shown and not run:
  - `gcloud ai custom-jobs list --region=us-central1`, the typed part of `40:91`;
  - `gsutil ls $GCS_BUCKET_URI`, the typed part of `30:64`.
- **Citations.** Every `TERM(laptop|colab/NN: …)` resolves to exactly one capture, with every line
  inside the file. That covers 40 capture ids, including the new `81: 2`, `84: …, 14` and `80: …, 70
  wrap`. Every `CODE(path: a–b)` exists, with `b` inside the file. Every `NB(A|B: …)` is in range.
  New ones checked by content:
  - `NB(B: 940–945)`: cell 42's `model.fit`, no callback line;
  - `NB(A: 1285, 1292)` and `NB(B: 1704, 1711)`: the frozen rows, 67.24 % and 68.97 %;
  - `NB(A: 1412–1419)`: `data_details`;
  - `NB(B: 26–31)`: cell 3, save a copy and GPU.
- **README.** README card spans are unchanged, and none covers line 96.
- **Sentences.** Every SAY sentence (`split_sentences`) starts with a capital or a digit. No SAY line
  has backticks, parentheses, `!`, `%`, `&`, `/` or `#`.
- **Splice trap.** A regex over all 223 lexicon keys finds no "a"/"A" directly before a key except
  the guarded "a 403". No "'s" follows a key except `README's`. No "notebook A's" appears in SAY or
  SHOW.
- **TTS.** Every new or changed SAY sentence was phonemized with `KokoroBackend.phonemize` and the
  current lexicon. No mid-sentence stop appears. 67.24, the one new decimal, reads clean
  mid-sentence. Fixed by rewrite:
  - "the opening's answer" was read as "open-ING's"; it is now "So the verdict: …";
  - "pip reads" broke the homograph rule; it is now "pip uses".

  "closed" (S07 ponder) is unchanged from v1; the flow review confirmed it is fine.
- **People and prices.** No real name, e-mail, W&B user or team. The only new "@" is the service
  agent pattern `service-…@gcp-sa-aiplatform-cc`. No prices, no "cents".

## Review 1 · accuracy (A1–A21): 18 applied, 3 adapted, 0 skipped

- **A1 applied** (coordinator). S09 SAY: "TensorFlow and scikit-learn are not declared: they are
  assumed to come from the image Google provides, and scene 11 shows the tarball lacks them.
  Requests only arrives because wandb needs it." The ORANGE layer reads "TensorFlow ·
  scikit-learn", with a GREY chip "requests: via wandb". The script's and BRIEF's colour tables, V4,
  errata 12 and BRIEF S09 are synced.
- **A2 applied** (coordinator; merged with F8). The tag reads "the job's VM bills while it is up:
  from provisioning until the script exits · see the Vertex AI pricing page". SAY: "A gold tag
  first: once the job's machine is provisioned, your project pays until the script exits." This
  also takes V29's "bill" → "pays".
- **A3 applied** (coordinator). S09: "…scene 11 shows the tarball lacks them". S11: "The trainer
  counts on the prebuilt image for those, which we did not pull to check." The word "did", not
  "could", follows ASSETS.md:288–290 ("not checked (too big to pull)"). The chips read "expected in
  tf-cpu.2-17 · not verified here" (S09, S11).
- **A4 applied** (coordinator). SHOW: metrics ✗ "execution_time is in config · no metric logged".
  SAY: "Metrics, none: the execution time goes into the config." The F5 block now says "its config,
  including the execution time". BRIEF S12 and ponder 9 are synced.
- **A5 applied** (coordinator). SAY: "On our Linux engine it belongs to root, because the container
  wrote it; on Docker Desktop, to you. Git ignores it either way." The chip reads "Linux engine ·
  Docker Desktop: your user". This is shorter than the proposed wording, to fit the budget.
- **A6 applied** (coordinator). SAY: "Our 40 character placeholder passes the offline length check,
  and nothing more." `86:4` is now YELLOW, not GREEN, with the chip "length check only · offline ·
  nothing asked W&B".
- **A7 applied** (coordinator, first option). `TERM(laptop/80: 2, …, 68, 70 wrap)`: line 70 folds
  into six rows, so `cheese-app-trainer-0.0.1` and `wandb-0.15.11` are on screen. The scene-author
  notes are updated in the script and the BRIEF.
- **A8 applied.** The `09` strip in S11 is plain `extra`. The Conventions tag list says why.
- **A9 applied** (merged with V43a). "…and on Vertex that comes after the data download, on billed
  machine time."
- **A10 applied.** The badge reads "Vertex AI Custom Code Service Agent ·
  service-…@gcp-sa-aiplatform-cc". The spoken name stays "your project's Vertex AI service agent".
- **A11 applied.** S14 SAY: "Here it fails like cli.sh, with no active account." S13's honest line
  uses the same wording (P20).
- **A12 adapted.** The chip reads "screenshots and a diagram · redrawn in this video". The spoken
  list is gone: P5 cut the sentence to "Two extras show the course pin and the repo's files."
- **A13 applied.** "Cell 55 builds the second table from the opening."
- **A14 adapted.** The window stays at `task.py: 27–30`, and the chip now names both dead flags:
  "--model-dir and --lr: parsed, never used". This matches BRIEF erratum 7.
- **A15 applied.** "…in the worker pool: values from lines 12–13, used on line 26".
- **A16 applied.** S05's tags use SLIDES.md:40 wording: "Initialize wandb run" · "Add a callback to
  monitor model" · "Let wandb know to finish the run". S14's tags use SLIDES.md:46: "Create
  distribution Strategy" · "Adjust dataset batch size" · "Create & Compile model in strategy scope".
  The SAY keeps its paraphrase.
- **A17 applied.** "with the instructors' project id and bucket name".
- **A18 applied.** The tag reads "weights of 10–104 MB per model (the table's model_size), plus a
  .keras copy of each". SAY: "…those files now sit in your bucket, 10 to 104 megabytes of weights
  per model, plus a copy." BRIEF S03 and costs are synced.
- **A19 applied.** `TERM(laptop/84: …, 14)`; line 3 is never printed (Conventions note).
- **A20 applied.** The "fresh cockpit" chip moved to the `sh package-trainer.sh` prompt.
- **A21 adapted.** The chip reads "system charts and run metadata · not the image tag (cli.sh)". The
  SAY stays as "system charts, while the image tag sits in cli.sh". It is not wrong, the reviewer
  marks the metadata as uncaptured wandb default behaviour, and the fuller sentence cost +6.

## Review 3 · follow-along (F1–F17): 11 applied, 6 adapted, 0 skipped

- **F1 applied** (coordinator; must-fix).
  - S07 SAY: "An extra echo prints its length, 40 for our placeholder. It must not be zero, and the
    trainer's pinned wandb accepts exactly 40." The chip reads "the check: not 0 · and the
    trainer's pinned wandb 0.15.11 accepts only 40 (scene 11: `84:14`, `87:14`)".
  - S09 (with F6): "Pause and check yours: the last number must be 40, not 0."
  - S10, before the submit: "Check that your key length is 40; if not, watch scene 11 before you
    submit."
  - The Conventions "What may not" line now says the 40 rule is about the pin. The BRIEF decisions
    table row "W&B key length" is updated to match.
- **F2 applied** (must-fix). B6 is now its own block: "To upload, edit the bucket and project inside
  cell 13 and run cell 13 again, then run cells 64 and 66; pause and do it." It has the chip
  "edited? run cell 13 again".
- **F3 applied.** The card order is now:
  1. In the cockpit: `gcloud ai custom-jobs list --region=us-central1` (finds the JOB_ID) · cancel ·
     nothing RUNNING/PENDING · Training pipelines.
  2. `gsutil rm …` · the folders · the bucket.
  3. Or in the console.
  4. Then `exit`, with `90`/`91`.
  5. Notebooks.
  6. Keys.

  SAY: "From inside the cockpit, or in the console, make sure no custom job is running or pending.
  Remove the tarball and experiment folders too. Then exit; an extra docker ps shows nothing left."
  `tracker_cleanup` is reordered. BRIEF teardown is synced.
- **F4 applied.** ▶ now sits on fix 1, the re-run, fix 2 and the third run. The spoken lines are:
  - "…bookworm, Debian 12; pause and make it."
  - "Pause and run it again."
  - "…on line 37; pause and make it."
  - "Pause and run it a third time: it builds…"
- **F5 applied.** Both fixes, and the D1 edit, carry the chip "our editor; use yours · macOS sed:
  sed -i ''". `22:3` and `24:4` are shown large as "your new line 2" and "your new line 37".
- **F6 adapted.**
  - S08 D1 has the chip "same terminal as your export · new terminal? export again first".
  - In S09 the cockpit `echo` gets ▶, the `40` is YELLOW, and the chip reads "0? exit · export
    WANDB_KEY=… · sh docker-shell.sh".
  - The SAY is shorter than proposed ("Pause and check yours: the last number must be 40, not 0.").
    The fix lives on the chip, for budget.
- **F7 adapted.** The chip reads "your bucket: one from lecture 11, or create it now · scene 7 shows
  how". SAY: "Any bucket of yours works; scene 7 creates one." That is 9 words, not 12.
- **F8 applied** (with A2). The GOLD tag and V4 step 3's flight open the submit beat. The old last
  block of S10 is removed.
- **F9 applied.** "Open your job and follow its logs link; wait for the line training job complete."
  The job page wireframe has a "logs" link, as an `illustration`; the console labels were not
  captured. No status value is shown.
- **F10 adapted.** No wandb version could be verified, so the video does not imply a one-line fix.
  The card reads "a different length? raise the pin, then sh package-trainer.sh again · a tested
  route: see the study guide". SAY: "If yours differs, the study guide has a workaround." This
  merges V16's split. **The study guide must carry it** (see the coordinator list).
- **F11 applied** (one adapted spot). New pause beats:
  - S03 A5: "pause and run through the predictions" (▶ and the chip "cells 54–59").
  - S04 B2: ▶ and "then pause and run them".
  - S07: "Pause and do both."
  - S08: the third run (F4).
  - S09 E2: "pause and open it".
  - S12 F5: "Pause and open your project."
  - S14 G2: "pause and open it".
  - S14 G4: "If your quota came through, pause and run sh cli-multi-gpu.sh." This is the adapted
    form, after the GOLD tag.

  S04 B5 has no ▶ of its own. Its chip "run cells 55–60 too · pause at the next step" hands it to
  B6's pause.
- **F12 applied.** S07 has an optional chip, tagged `extra · not captured`: "keep it out of your
  shell history: `read -rs WANDB_KEY && export WANDB_KEY` (bash, zsh)".
- **F13 adapted.** The S03 chip reads "the study guide links notebooks A and B · the badges inside
  them open older copies". The S04 chip, not spoken, reads "open notebook B · save a copy · GPU
  runtime (cell 3, NB(B: 26–31))". The proposed S04 sentence was not spoken, for budget.
- **F14 adapted.**
  - (a) `81` is typed between `80` and `82`. It prints `trainer-standin` (`81:2`), so it is shown
    as TERM, not "no output".
  - (b) `30:64` is not typed: its output here is the placeholder's 404, and typing it with no panel
    would misstate it. The command sits on the chip "with your bucket: `gsutil ls $GCS_BUCKET_URI`
    lists cheese-app-trainer.tar.gz".
  - (c) `40:91` is on the teardown card (F3).
- **F15 adapted.**
  - All four tracker captions are written: `B1 · extra · local stand-in`, `B4 · extra`, `C4 ·
    extra`, `C7 · extra`.
  - S04 now says "An extra check in our signed-out stand-in shows 0.31.0…", merged with V26.
  - S07's "an extra tree shows it" was not spoken, for budget; the caption carries it.
- **F16 applied.** The card adds:
  - the key's JSON in secrets;
  - notebook B's folder "under your account's folder" (`nbB:269-281`);
  - the explicit `docker image rm model-training-cli python:3.13-slim-bookworm
    python:3.13-slim-bullseye` (and the extras' `trainer-standin python:3.10-slim-bookworm`), with
    names from `91`;
  - "update the Colab secret `WandB` · the old export lives on in that terminal: open a new one";
  - "Linux: `sudo rm trainer.tar.gz`".
- **F17 applied.** Chip: "project ID, not its name · keep gs://".

## Review 2 · pedagogy (P1–P24): 19 applied, 5 adapted, 0 skipped

- **P1 applied** (coordinator).
  - S06 block 4: "Step two packs that file into a tarball, one compressed archive, and uploads it to
    a bucket. Step three runs from what the lecture calls the Model Trainer CLI Container, our
    cockpit on your laptop: it asks Vertex AI for a job. Vertex AI then starts a machine, CPU only
    or with one T4. It loads Google's prebuilt TensorFlow image, installs your tarball, runs your
    trainer with your flags, and deletes the machine." This also covers V35. On screen, V4 step 4
    plays as a miniature tagged "plan · drawn".
  - S06 block 5: "And the image is Google's, not yours."
  - S10: "Then it points at your tarball in the bucket and the module to run". Line 10 gets a PINK
    arrow.
  - S11: the real V4 step 4 is drawn once (tag "what Vertex does · drawn, not recorded", no output
    panels). `--args` splits into argv on S09's flag lines, then the dashed stand-in replaces the
    VM. SAY: "On Vertex, the job's first step installs your tarball into Google's image. We can't
    run Vertex here, so we rerun that step…"
  - BRIEF V4, S06 and S11 are synced.
- **P2 adapted** (coordinator). "notebook A's" is forbidden, and "opening's" is mis-stressed.
  - S03: "…and the winner in notebook A leads by two photos."
  - S04 B5: "Now the frozen MobileNet, with the same settings and epochs: 67.24 in notebook A, 68.97
    here. Two photos apart by chance alone: the size of the winning margin." Both frozen rows ring
    YELLOW, and S03's ruler returns.
  - S04: the dashboard sentence is cut; the slide-16 chip stays.
  - S12: "The folder from notebook A has no commit, no split and no notes either. So the verdict:
    these tables cannot crown a recipe. Seed the split, match the epochs, keep the code version,
    then compare. Exercise 1 adds a small callback." The proposal's "misses the same three" was
    made precise because the folder does keep image sizes and the label map (`NB(A: 1412–1419)`).
  - On screen, S01's card returns with "can't tell · yet", and the chip reads "exercise 3: seed the
    split" (digest exercise 3).
- **P3 adapted.** "Part 2 ships the trainer: build the cockpit, pack the code, send one job." V1's
    repo lane flashes in three stages. "It starts in the repo." was cut for budget; `cd
    model-training` is on screen.
- **P4 applied.** NB(B: 710–716) sits beside NB(B: 940–945), unhighlighted. SAY: "But only the two
  block run shows curves. Compare its model fit call with another cell's." The answer: "A callback:
  code that model fit calls after every epoch. …"
- **P5 adapted.** "Then request GPU quota, an allowance per region. Filter for custom model training,
  pick T4 GPUs, include us-central1, where cli.sh runs, set a new limit and submit. Pause and do
  both." On screen, `us-central1` is YELLOW with the chip "cli.sh's region · line 14". This is
  funded by the proposed C1 cut (−11) and "Approval may take hours or be refused; cli.sh runs on CPU
  without it."
- **P6 applied.** S10: "The worker pool spec is the job's machine order: machine type, one replica,
  meaning one machine, image and module." This is merged with V46's split. In S14, "only to count
  GPUs", and V7 defines "replica".
- **P7 applied** (coordinator, "not mirrored"). The S14 order is now ladder → V7 → G1 → G2 → ponder
  → caveats → G3/G4. V7: "Here is the idea. Each GPU holds an identical copy of the model, called a
  replica. A global batch of 64, one step's worth, splits into two halves of 32. … Variables created
  inside the scope are mirrored, one synced copy per GPU; a model built outside is not mirrored."
  The gloss "one step's worth" replaces "what both GPUs take in one step" (−4). G2 SAY: "These are
  the lecture's three changes." plus one sentence per call-out (V19). BRIEF V7 and S14 are synced.
- **P8 applied.** Block 2 now reads "…The middle lanyard is still empty." The answer is the
  proposal's text, with badge 2 drawn only then. BRIEF V5, S11 and ponder 8 are synced.
- **P9 applied.** "It is the label pip uses to install the tarball." The proposal had "reads", which
  the homograph rule forbids. Also "…so once installed, python dash m trainer dot task works."
- **P10 applied.** S04 chip: "system charts = the machine's CPU · GPU · memory over time". S12 chip:
  "system charts · CPU · GPU · memory".
- **P11 adapted.** "Then the fine-tuned MobileNet leaves Colab." This is +1, not +4, and avoids
  "notebook A's". The chip reads "train_base True = fine-tuned · False = frozen".
- **P12 applied.** Only the ▶ tag is previewed. SAY: "A yellow tag means pause and run it, and the
  study guide has every command."
- **P13 applied.** The timing stays on the GREY chip.
- **P14 applied** (with V14). "The script's set dash e, exit on error, then stops it before docker
  run."
- **P15 applied.** V4 step 3's card assembles over the `cli.sh` review and flies at the submit (F8).
- **P16 applied.** "Exit, export, and start again; first exit any old cockpit, which holds the name."
  The chip reads "fixed name: model-training-cli".
- **P17 applied.** YELLOW chip "class 0: brie in A · gruyere in B", checked against `nbA:352` and
  `nbB:409`. The S03 pin returns.
- **P18 applied.** "Now the reverse of the README's optional CPU step…"
- **P19 applied.** "…with CUDA, the GPU libraries."
- **P20 adapted.** "An extra check shows Google still serves both GPU images, at the time of
  recording." The honest line follows A11: "Here the GPU block would fail the same way as in scene
  10, with no active account, so there is nothing new to show, and nothing we fake." The sizes are
  on screen only.
- **P21 applied.** The recap is now content sentences, and the SHOW relights one group per sentence.
- **P22 applied.** "Answers are in the exercises." Routing goes to the coordinator (below).
- **P23 applied.**
- **P24 applied.** All five cuts: S02, S08, S09 ×2 (versions now on screen only), S12.

## Review 4 · flow (V1–V46): 31 applied, 11 adapted, 4 skipped

- **V1–V12 applied** through the coordinator's lexicon block (09e7e2f); no text change. V4's S12
  sentence no longer exists (P2).
- **V13 applied** (re-anchored on "named sources", 0 words). **V14 applied** (with P14).
- **V15 adapted.** "The call run save with the word test uploads files matching test; it does not
  save the run." This is +1, not +2.
- **V16 applied** ("which key format W and B gives out today").
- **V17 applied** ("shows").
- **V18 adapted.** Superseded by P21's short sentences.
- **V19 applied**, via P7's G2.
- **V20 applied**, in V7's SAY.
- **V21 adapted.** Superseded by P23.
- **V22 applied.**
- **V23 applied**, via the P1 and P6 splits.
- **V24 adapted.** Superseded by P20.
- **V25 applied.**
- **V26 adapted.** Split as proposed, with F15's "An extra check in our signed-out stand-in shows
  0.31.0…".
- **V27 adapted.** Superseded by P24.
- **V28 applied** (lexicon). **V29 applied**: S01 says "cost money"; S10's line became A2's "your
  project pays".
- **V30 skipped**, as moot: P2 cut the "say cheese" sentence.
- **V31 applied.** **V32 adapted**: "936 to train, 104 to validate, 116 to test" (0 words) and
  "…is 104, the validation set". **V33 applied.** **V34 applied.** **V35 applied** (via P1).
- **V36 skipped.** Superseded by P16.
- **V37 applied** ("rerun").
- **V38 adapted.** "To put it kindly, not with this code."
- **V39 skipped**, for budget (+2). **V40 skipped**, for budget (+4).
- **V41 adapted.** S08 uses "because". S10 uses "because" without the +3 split.
- **V42 applied.**
- **V43 adapted.** The first half is applied with A9. The second half ("and the error says") is
  skipped for budget (+4).
- **V44 applied.** **V45 applied.**
- **V46 adapted.**
  - Applied: S03.7.2, S08.2.1, S08.3.2, S10.4.3 (P6), S10.7.2, S05.7.2 (P13 form), S04.2.1 (F11
    rewrite), S11.6.1 (A3), S12.4.1, S14.2.2, S14.6.2.
  - Done with 0-word splits: S05.5.1 and S15.1.2.
  - Skipped for budget: S01.4.1 (+4) and S07.4.1 (+1).

## Word-budget trims (each removes a spoken restatement of something still on screen)

The mandated fixes took the draft to about 4,426. The review-proposed cuts (P2, P5, P12, P13, P20,
P22, P23, P24) and the cuts below bring it to 4,292. No cut removes a README command, a tag, a
`recorded` source or a fix above. Cuts that remove a spoken fact still shown on screen:

- **S01:** "a line we will look at together, because your W and B key is inside it" → "That
  command carries your W and B key." (the strip with the RED key).
- **S02:**
  - "and the milestone accepts an equivalent" (chip);
  - "tracking, and one serverless training run that is logged and reproducible" (the Milestone 3
    chip).
- **S03:**
  - spoken "TensorFlow 2.19.0" (recorded output);
  - "to the opening question" (SHOW "the hook's first answer");
  - "the repo trainer copies the same lines" → "copied into the repo trainer";
  - "Finally, upload." (tracker A6).
- **S04:**
  - "Next, the key." (tracker B3);
  - "and prints a link to the run" (banner `nbB:781`);
  - "Check the epochs: … so it is" shortened.
- **S07:**
  - the C1 list (P5);
  - "an extra listing shows ours" (caption `C5 · extra`);
  - "the Colab lane is lit" (V1);
  - "so this is for later" → "without it".
- **S08:**
  - "with any editor; we use sed" (chip);
  - "It starts in the repo." (`cd` on screen);
  - "two mounts…, four environment variables, and no port" → "mounts your code and secrets"
    (CODE window and chips);
  - the spoken Python 3.13.17 / uv 0.13.5 (tags);
  - "The prompt is root, and its ID changes every run." (chip).
- **S09:**
  - "Its image takes 2.59 gigabytes." (tag);
  - "With yours, look for cheese-app-trainer.tar.gz in your bucket." (the `gsutil ls` chip);
  - "with each file size inside" (the `tar tzvf` listing).
- **S10:**
  - "Its accelerator list may also be out of date." (chip);
  - "nothing here shows that" (the "no panel" chip);
  - "Check the Vertex AI pricing page." (tag text).
- **S11:** F10's sentence shortened.
- **S12:** "1,156 photos, then 936, 104 and 116" (the log shape).
- **S13:** the three sizes (P20).
- **S14:**
  - "Everything else was already done; only the launch script changed." (slide-30 line);
  - "what both GPUs take in one step" → "one step's worth".
- **S15:**
  - "Lecture 15 picks this route up." (chip and Next card);
  - "and the images stay on disk" (card and `91`).

## BRIEF.md changes (sync only where the merge changed structure)

- **Decisions table, "W&B key length".** "the check that matters is not 0" now reads "not 0, and 40
  for the trainer's pinned wandb 0.15.11, a fact about the pin". This follows the F1 approval.
- **Colours.** The ORANGE row: TensorFlow and scikit-learn are expected and not verified; requests
  arrives with wandb (A1, A3).
- **V4.** Its scenes: S06's trip told once with a step-4 miniature; S10's card assembly; S11's step
  4 drawn, then the stand-in. Its ORANGE layer is corrected (A1, A3).
- **V5.** The S11 badge order and the Custom Code Service Agent label (P8, A10).
- **V7.** Played before the code; "not mirrored" (P7, coordinator).
- **Trackers.** `tracker_cleanup`'s new order, and `81` (F3, F14).
- **S01:** only the ▶ tag is previewed (P12).
- **S03:** the "notebook A's" rule, the bucket chip, the predictions ▶, the A18 GOLD wording.
- **S04:** the two-`model.fit` ponder setup and the callback gloss (P4); the frozen-MobileNet
  evidence; the upload as its own block with the cell-13 re-run (P2, F2); slide 16 as a chip.
- **S06:** the trip told once (P1).
- **S07:** quota per region and `us-central1` (P5); the 40-character pin wording and the `read -rs`
  chip (F1, F12).
- **S08:** the part-2 purpose sentence; ▶ on the fixes and re-runs; the macOS `sed` chip (P3, F4,
  F5).
- **S09:** the ▶ key check; A1/A3; `setup.py`'s purpose; the Linux owner (F6, P9, A5).
- **S10:** the GOLD tag and key check before the submit; the spec card's assembly; the worker pool
  gloss (A2, F8, F1, P15, P6).
- **S11:** the badge order; the drawn step 4; "not verified"; length check only; the study guide
  workaround (P8, P1, A3, A6, F10).
- **S12:** the logs link (F9); metrics none (A4); the hook verdict (P2).
- **S13:** the short honest line; sizes not spoken (P20, A11).
- **S14:** the new order (P7).
- **S15:** the recap as content sentences (P21).
- **Ponder table:** rows 2, 8 and 9.
- **Errata:** 8 and 12.
- **Costs:** S03 (A18) and S10 (tag before the submit).
- **Teardown checklist:** rewritten in the new order with F16's items.
- **Notes for authors:** `80` with `wrap`, and `84` from line 14.

The word-budget table is unchanged (the targets). The merged counts are in the script.

## For the coordinator

1. **Git.** `build/` is gitignored (`.gitignore:2`), so this file needs `git add -f`.
   `build/review-flow.md` is not tracked yet either; only the other three reviews are.
2. **Study guide (F10).** S11 now says "If yours differs, the study guide has a workaround". The
   card says "raise the pin, then sh package-trainer.sh again · a tested route: see the study
   guide". `MLOps_Learning · guides/L13-training-workflows.md` must carry a verified route. That is
   either a newer `wandb` pin checked inside `tf-cpu.2-17.py310` together with `task.py:22`'s `from
   wandb.keras import …`, or removing that unused import. If neither can be verified, change the
   sentence before scenes.
3. **Lexicon (optional).** `67.24` (S04) is new. It phonemizes clean mid-sentence today. A
   robustness key beside `68.97` is needed only if an edit moves it to a sentence end.
4. **Tight margins.**
   - The total is 4,292 of 4,300.
   - S02 is 190 (floor 187).
   - S03 is 317 (cap 322).
   - S04 is 325 (cap 333).
   - S07 is 321 (cap 333).
   - S15 is 298 (cap 310).

   Any later addition must name its cut in the same scene.
5. **exercises.md routing** (P22): see the report.
6. **Unverifiable from here.**
   - The console's job-page "logs" link label: drawn as an `illustration`.
   - Whether `tf-cpu.2-17.py310` holds scikit-learn and requests (not pulled).
   - Today's W&B key format.

## Final word counts (`python -m explainer.script`, after merge)

| scene | words | BRIEF | ±15 % band |
| --- | --- | --- | --- |
| S01 | 205 | 220 | 187–253 ✓ |
| S02 | 190 | 220 | 187–253 ✓ |
| S03 | 317 | 280 | 238–322 ✓ |
| S04 | 325 | 290 | 247–333 ✓ |
| S05 | 242 | 240 | 204–276 ✓ |
| S06 | 259 | 250 | 213–287 ✓ |
| S07 | 321 | 290 | 247–333 ✓ |
| S08 | 333 | 340 | 289–391 ✓ |
| S09 | 311 | 300 | 255–345 ✓ |
| S10 | 339 | 310 | 264–356 ✓ |
| S11 | 318 | 300 | 255–345 ✓ |
| S12 | 297 | 290 | 247–333 ✓ |
| S13 | 205 | 230 | 196–264 ✓ |
| S14 | 332 | 300 | 255–345 ✓ |
| S15 | 298 | 270 | 230–310 ✓ |

**Total: 4,292 words** (required 3,900–4,300). Part 1 (S01–S07) has 1,859 words and part 2
(S08–S15) has 2,433. The Conventions length table is updated to match.
