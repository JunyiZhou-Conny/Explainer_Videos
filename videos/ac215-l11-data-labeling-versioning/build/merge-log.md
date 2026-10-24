# Merge log · script.md review merge (reviews of commit 1da63fa)

Merged by the merge agent on branch `claude/ac215-l09-l13-batch`. Precedence:
accuracy > follow-along > pedagogy > flow/style. Coordinator decisions applied as given: A4
skipped (the series' project-id convention is now written into the script's Conventions block);
P3's reorder approved; A1 approved (`121` moved to S13, `120` kept in S12); A2 = P16 = F12
applied with an honest warning and a `stand-in` tag; P9 verified against the sources (below);
F1 and F2 treated as must-fix.

The scene list and the part cut are unchanged. Nothing moved between scenes except `121` (S12 →
S13, A1). Inside scenes: S12 reordered (V5 as a prediction before any `dvc add` output); S16
reordered (recap → test yourself → cleanup/teardown → next); S07 reordered (token copy moves to
the `-p` block, P24); S09's opening reordered (parked question first, P6); blocks split in S01, S08,
S10, S13, S14. Ten PONDER cards and two QUICK predicts, as before.

After the merge (all re-run on the final file):
- **README commands**: every README command of both tutorials is still typed on screen byte for
  byte, and the first occurrences are in README order (a scan over the SHOW lines for the 39
  commands of the follow-along checklist, data-labeling then data-versioning, then the notebook
  cells). The only new typed lines are `cd ..` (S09, F1), `exit` (S08, F4, the capture's own
  `42:73`) and the moved `121` diff.
- **Citations**: every `TERM(laptop|colab/NN: …)` resolves to exactly one capture file and every
  cited line is inside it; every `CODE(path: a–b)` exists under `assets/source/` with `b` inside the
  file. New citations spot-checked by content: `41:66`, `42:73–74`, `85:5`, `95:58–63`, `120:2–7`,
  `121:2`, `114:1`, `115:49–51`, data-labeling `README.md:147`, data-versioning `README.md:136`.
- **Sentences**: every SAY sentence (`explainer.voice.split_sentences`) starts with a capital or a
  digit. No SAY line has backticks, parentheses or "!".
- **Splice trap**: a regex over all 182 keys of `explainer/lexicon.yaml` (including the new L11
  block) finds no "a"/"A" directly before a key except the guarded "a 401" (S07, S15). No `'s`
  after a key except `README's`.
- **Homographs**: one new one caught and fixed: A6's "cannot read the class bucket" → "cannot
  access". No "read/live/lives/close/lead/tear/minute/content/record(s)" remain.
- **People**: no real name, e-mail or user name. Only `student@example.com`, `student@laptop`,
  `YOUR_GITHUB_USERNAME`, `<read-only token>` and the course placeholders appear.
- `explainer/lexicon.yaml` untouched (the flow review's block was already applied by the
  coordinator); the script's Lexicon section now records each candidate's status.

## Review 1 · accuracy (A1–A21): 15 applied, 4 adapted, 2 skipped

- **A1 applied** (coordinator) — S12 keeps `120:2–7`: the class card slides in beside ours
  (`95:58–63`), no command typed on our side. SAY: "And the instructor's tag in the class repo holds
  the same fingerprint, character for character." The `121` diff moves to its own S13 block, right
  after `git show` (`102`), in the second-terminal strip at `~`. SAY: "An extra diff against the
  instructor's tag: identical, same bytes, same fingerprint, on any machine." BRIEF V5 (:199) and
  S12/S13 (:546) synced.
- **A2 applied** (coordinator; = P16 = F12) — S14 tagged `extra · stand-in` on `114`–`117`, with a GREY
  chip "real mount: dvc checkout writes to images/ in your bucket · v20 deletes Image_5.jpg there ·
  main writes it back". SAY: "One extra experiment, on our stand-in folder: … With a real mount,
  this folder is your bucket's images folder, so checkout deletes and rewrites photos there." The
  "use dvc get, next" pointer was dropped for budget, because S15 follows immediately.
- **A3 applied** (merged with P23) — "One: the rule missed your bucket. Dash c failed, or line 23
  names another bucket of yours; dash m shows which bucket got it." SHOW: `41:66` flashes; the rule
  card flies to the viewer's other BLUE bucket; chip "an untouched README name fails outright: not
  your bucket". BRIEF S06 and ponder table synced. (digest §6 #10 still has the shortcut; the
  digest is outside this merge.)
- **A4 skipped** (coordinator) — the series convention (L10 BRIEF:110–113) quotes source lines
  verbatim. The Conventions block now says: ours is always `your-gcp-project`; `ac215-project`
  appears only inside quoted source lines (the four CODE windows are named) and RED story beats,
  never highlighted, never spoken, never masked. BRIEF's Running example has the same rule.
- **A5 adapted** (merged with P10 and F2) — "On Label Studio 1.23.0 it fails with a 401; ours says
  legacy token authentication has been disabled for this organization." The "newer kind" half moved
  to the next block, where P10's two-kinds explanation lands: "The page shows a newer personal token
  by default, the legacy kind is switched off, and cli.py speaks only legacy." No panel for the
  personal-token case.
- **A6 applied** — "The instructor's signed-in run lists five files on the class repo, the same set
  as its version 21, and counts 5. Your account probably cannot access the class bucket, so use your
  repo: …". "Read" became "access" (homograph); the chip on cell 13 says "the class repo's main · the
  same five files as its v21".
- **A7 applied** (merged with V15) — "When the page's own code fetches the photo, as Label Studio
  does, your browser hands the answer over only if it carries a header that allows this origin.
  Google adds that header only if the bucket has its own CORS rule." The P22 chip uses the same
  fact.
- **A8 applied** — S10 V4: stage 1 is the key file feeding line 10's `--key-file`; line 8 gets a GREY
  side note "gcloud's own login · not used by gcsfuse or DVC". S11 SAY: "The gcloud tool cannot find
  the key file, and neither can gcsfuse, so the bucket never mounts." ("The gcloud tool" keeps the
  capital start.) S11's broken replay was re-labelled to match. BRIEF V4 synced.
- **A9 adapted** (merged with V4) — "Extra checks: the logs show a box offering version 1.23.2,
  newer than this image, which ran 1.23.0 at the time of recording. The tag is latest, so yours may
  differ."
- **A10 adapted** — the "two curls" sentence is cut (P20). The redirect is on screen (`21:2`), so no
  wrong claim remains.
- **A11 applied** — "The target storage, where labels go, with the prefix cheeses labeled, fails
  too, with a vaguer message."
- **A12 skipped** — "x86" kept, as in L10 (A11 there). Saying `x86_64` would need a lexicon entry.
- **A13 applied** — `27` is now an output-only strip headed `GET /api/jwt/settings · stand-in`,
  tagged `extra · stand-in` ("it rides on our scripted login"). The Conventions list of stand-in
  calls now includes `27`, and the "`27` is typed" sentence is gone.
- **A14 applied** — "It cannot connect: inside a container, localhost is that container, and nothing
  listens there." BRIEF ponder 5 answer synced.
- **A15 applied** — "3 tasks in our stand-in, 21 for you; ours has one labeled, as gouda."
- **A16 applied** — "An extra echo prints the README's bucket name".
- **A17 applied** — `62`: line 13 YELLOW, line 10 GREY ("the stopped container").
- **A18 applied** — SAY "the cache on your disk, filled by dvc add"; V6 label "your disk · copies
  made by dvc add"; BRIEF V6 synced.
- **A19 applied** — S01 checklist tag and S13 tag + SAY: "a fraction of a cent a month" (S13 SAY:
  "still a fraction of a cent a month"). The Conventions cost-tag line now forbids "cents"; BRIEF
  S01/S13 GOLD lines synced.
- **A20 adapted** — SAY: "one DVC container, a bucket with two folders, your own GitHub repo".
  V7 keeps its two BLUE shapes (a BRIEF episode-local rule), with a GREY chip "a new bucket or part
  1's, scene 10" matching S10's chip.
- **A21 applied** — "matching folder for folder".

## Review 3 · follow-along (F1–F18): 17 applied, 1 adapted, 0 skipped

- **F1 applied** (must-fix) — S09 G1 opens at `student@laptop:~/data-labeling$` with a typed `cd ..`
  (no output), prompt `student@laptop:~$`, beside a README card `README.md · line 136` ("next to your
  `data-versioning` folder"). SAY: "First, move up one folder, so the new clone sits beside
  data-labeling and secrets."
- **F2 applied** (must-fix) — S07 has a new fix block. The *Organization → API Tokens Settings*
  toggle and `43` come first. Then the *Account & Settings* wireframe returns with two rows,
  lower-case "personal access token" and "legacy token" (`illustration`; the 1.23 labels were not
  captured). The legacy row is lit with a blank value, followed by `▶ your turn`. SAY: "The fix: in
  organization, API token settings, enable legacy tokens. Then copy the legacy token, not the
  personal one. Pause and do both." The block before it draws the same two rows (legacy greyed),
  for P10.
- **F3 applied** — K1: "Pause and upload one or two." K2 (its own block, P27): "Start the container
  again, list the folder, and add it; pause and run them." The SHOW marks the re-entry "the README's
  command, re-used". K3: "Then dvc push; pause and run it."
- **F4 applied** — S08 E1 types `exit` at S07's last prompt (`42:73` → `42:74`). SAY: "Leave the
  command line container with exit, stop Label Studio, and check with docker ps; pause and do it."
  E1 gets a ▶. E2: "pause, remove it, and run the compose script again."
- **F5 applied** — S15's ▶ moved to the end of the `recorded` block, after the instructions. The
  notebook frame shows the edited cell 15 (`YOUR_GITHUB_USERNAME`, `--rev dataset_v20`), plus a
  GREY `illustration` chip with the private-repo form
  `https://YOUR_GITHUB_USERNAME:<read-only token>@github.com/YOUR_GITHUB_USERNAME/data-versioning`
  "· or make it public for this step".
- **F6 applied** — card line 1 is now "containers and the labeling network: already gone (scene 8)".
  The CORS line is spelled out runnable after the prune (`sh docker-shell.sh`, `sh
  docker-shell-CLI.sh`, `python cli.py -r`, `exit`; "deleting the bucket removes its rule too") and
  is spoken once: "If you keep the labeling bucket, remove its CORS rule with dash r." The volume
  line gains "(sudo on Linux)". Card and SAY now agree on the key: "Delete the key and its JSON file
  when the course is done." The optional GREY `docker image rm …` line (about 6 GB) is on the card.
  The spoken "already gone" sentence was cut for budget; the card carries it. BRIEF teardown synced.
- **F7 applied** — a GREY chip (not spoken) on `git remote add origin …`: "no SSH key? use
  https://github.com/YOUR_GITHUB_USERNAME/data-versioning.git as origin · GitHub asks for a token,
  not your password".
- **F8 applied** — the G1 chip gives `github.com/dlops-io/data-versioning/blob/b240b1a/README.md` and
  "the study guide links it". (The short hash resolves on raw.githubusercontent.com: HTTP 200. The
  github.com blob page could not be checked from this sandbox: the proxy returned 403.) S10 says
  "the course's README never says…", and its erratum caption adds "today's README (2515e5e) adds that
  sentence". S15 gets a chip: "today's README links a newer copy of this notebook (18KYngbv) · same
  cells, pointed at a TA's repo". This wording follows ASSETS.md:103.
- **F9 applied** — `TRACKER B1 · extra · Linux` on `chown`. The tracker returns to B1 for the
  re-run and to B2 for `18`, and the re-run gets `▶ your turn`. SAY: "On Linux, pause and do the
  same."
- **F10 applied** — S05: the block-2 ▶ was dropped, and block 4's single ▶ covers both forms (the
  *Add Target Storage* button flashes there). S09 G3: "Pause and run both." S10 H1/H2: the ▶ was
  dropped ("nothing new to run if part 1's key is in place"). S13 block 3: the ▶ was dropped, and
  the tag/push block's ▶ covers all five git commands. S11 rebuild: ▶ plus "Pause and run it again."
  S12 restart: "Start the container again, and dvc init works."
- **F11 applied** — the Dockerfile `sed` gets "our editor; use yours · this sed -i is GNU syntax".
  `87:2` is shown large as "your new line 36".
- **F12 applied** — via A2.
- **F13 applied** — a GREY chip beside E2: "docker-compose: not found? docker compose run --rm
  --service-ports data-label-cli".
- **F14 applied** — the route-T chip adds "rewind to scene 9 · recreate your empty GitHub repo
  first".
- **F15 applied** — "Open one to see the note." The SHOW opens one file to the envelope's shape
  (`33`), with no object name.
- **F16 applied** — chips "no tree? ls shows the same" (S02, S10) and "macOS: md5 -r" (S03).
- **F17 adapted** — `119`'s line 1 is not typed: it also prints the class repo's head commit and
  date, and the conventions never show those. Instead, the S12 strip's GREY chip spells the clone
  command `git clone -q https://github.com/dlops-io/data-versioning class-data-versioning`, the first
  half of `119:1`.
- **F18 applied** — the captions are written in full: `TRACKER B1 · extra · Linux`, `TRACKER J1 ·
  extra · Linux`, `TRACKER J3 · extra · stand-in`, `TRACKER F1 · extra` on `55`, `TRACKER K4 · extra`
  on `113`, `TRACKER K4 · extra · stand-in` on `114`–`117`. The Conventions tracker line now says
  variants are written in full.

## Review 2 · pedagogy (P1–P30): 24 applied, 6 adapted, 0 skipped

- **P1 applied** (blocking) — S12 payoff: "So one line pins 600 kilobytes: it fingerprints the list
  of fingerprints." (A1's wording follows.) Ponder-8 reveal: "The opening's two folders were the
  reverse: same names, new bytes." S01's cards return with manifests that differ in one PINK row (no
  invented values). S16 recap: "So Monday's photos come back with one dvc get; their labels join in
  exercise E7." S01's caption returns with "which photos ✓ tag · which labels → E7".
- **P2 applied** (blocking) — S03: "One more extra, for part 2: each photo's fingerprint, computed from
  its bytes alone. Same bytes, same string; change one byte, and it changes completely. Remember the
  first one." The five real `09b` rows pulse as five unrelated strings.
- **P3 applied** (coordinator) — S12 order: init → Linux fix → route T → remote add → **V5 as a
  prediction** ("Here is what dvc add will do with photos…"; the `.dir` box reads `????????….dir`
  and the pointer card is blank) → the empty add ("a second trap") → stand-in copy + add + `cat`,
  where the blank fields fill (`95:59–61`) → cache listing → payoff → ponder. BRIEF S12 beat list
  rewritten.
- **P4 applied** — "It files a copy in its cache under that fingerprint…" and "…writes that
  fingerprint into the pointer file, which stands in for the folder in git." A GREY chip on the
  `.dir` box: "the .dir ending marks a folder's list".
- **P5 applied** — "With no bucket mounted, our stand-in copies four photos into the laptop folder,
  which the container sees through the repo mount, and we add again." It includes V4's small
  two-layer picture, with the inner bind dashed.
- **P6 adapted** — S09 opens on the parked card: "Part 2: freezing which photos a model saw. Git alone
  would copy every photo version into every clone. Of the lecture's four approaches, we build the
  file-based one: git versions a small file of fingerprints, and a bucket holds the photos. The tool
  is DVC." It shows a 2 s V6 silhouette. "Of the five reasons on screen, watch save space" was cut
  for budget; the card keeps "save space" YELLOW "scene 14". S13 adds "The images folder can
  change; the DVC store never overwrites, because new bytes get a new name." The parked card gets
  its check mark there.
- **P7 applied** — "add source storage, where the photos come from" and "The target storage, where
  labels go, …".
- **P8 applied** — "Label Studio does not relay the photos; it signs a web address with the key…" A
  dashed relay arrow is crossed out.
- **P9 applied, verified** — digest A12 (`digest.md:332`) says: "on submit, Label Studio writes one
  object per annotation to the target prefix". Line :334 adds that annotations made before the
  target storage was added need *Sync*. README:184–186 expects "json files corresponding to the
  images … that have been annotated", and ASSETS.md:265–270 says the bucket side was not captured
  (no bucket). Our order adds the target storage (S05) before annotating (S07), so the claim holds.
  The claim is kept, worded: "Label Studio saves it in its database, and the target storage writes
  a copy to cheeses labeled, pointing back at the photo, which never moved." On screen, the envelope
  stops at V1's database drawer, then a copy flies to the bucket. A GREY chip reads "on submit, via
  target storage · README.md:184–186 · not captured here". Label Studio's own source is not in
  `assets/`, so the export-on-submit mechanism rests on the digest and the README.
- **P10 adapted** — merged with A5/F2 (two-row token wireframe; "this version has two kinds of
  token…").
- **P11 applied** — "Label Studio and a small command line container"; the second house is
  captioned.
- **P12 applied** — "…so gcsfuse only shows folders the console made, which leave a marker object.
  That was the trap." (digest :214). The two slide-correction sentences became chips (not spoken).
  The SHOW is split, and the pull-back gets its own sentence: "Note the two bind mounts: dash v
  joins your laptop's repo to the container, and the inner one joins the bucket's images folder."
- **P13 applied** — "…as if it were local, while each file is fetched from the bucket." On
  "fetched", a request dot runs up the pipe.
- **P14 adapted** — superseded by F5's order (the instructions come after the `recorded` block,
  then the ▶). Block 2 no longer says "pause".
- **P15 adapted** — "Tag the commit as dataset v20, a permanent name, and push…" (word order; the
  flag plants on "a permanent name").
- **P16 applied** — = A2.
- **P17 applied** — one question large at a time; the gouda envelope has its own beat; "The lecture
  makes fun of exactly this habit." was cut.
- **P18 applied** — the slide-6 row shrinks; the versioning half is drawn as outlines until S09; the
  pipeline-flow sentence was cut (its chip stays, unspoken); the quiz line is now "Now, the
  lecture's recall quiz."
- **P19 applied** — QUICK card "How many tasks (one item to label each) should Label Studio make?"
- **P20 adapted** — the curls sentence was cut. The server-side line was merged with V36:
  "Underneath, our stand-in calls replay the page's requests: we are logged in, and project 1 holds
  the four cheeses."
- **P21 applied** — V2 clears before the grid; the slide-7 card was dropped.
- **P22 applied** — a chip (confirmed by A7): "Label Studio's page fetches the photo in CORS mode →
  the browser checks · a plain image tag would not".
- **P23 adapted** — merged into A3 ("dash c failed, or line 23 names another bucket of yours").
  Seeding suspect 2 earlier was not added (budget). The S08 chip "same trap as scene 6" was not
  added: compose's untouched README name fails outright, which is not the silent case.
- **P24 applied** — the ponder block keeps only the by-name line and the question. The token copy
  opens the `-p` block (tracker D appears there). "Forget dash k…" is unspoken, folded into the end
  of the `-t` block (`42:68–69` + chip). "Switching to the newer client is an exercise." is a chip.
- **P25 applied** — the compose block split at "And the first call is refused". The stray-line
  clause and the image-size sentence were cut (chips stay). The bridge became "…can change under
  them: same name, new picture."
- **P26 applied** — "A second trap: …".
- **P27 applied** — S14 split: the ponder answer + `dvc add` block, then the push block.
- **P28 applied** — "A quick prediction: three questions, three tools. Match Delta Lake or Iceberg,
  DVC, and lakeFS." / "DVC, lakeFS, then the table formats." The chips are shuffled on screen.
- **P29 applied** — S16 order: recap → test yourself → cleanup + teardown → next. Q1 reads "One: who
  fetches the photos, and why does the bucket need its CORS rule?" (3 words shorter than proposed);
  the card also keeps "Why does curl never notice?". The footer SAY is now "Answers are in the
  exercises." BRIEF recap Q1 and S16 order synced. Not done here: routing the two untested
  outcomes into exercises.md (see the coordinator list).
- **P30 applied** — S09's git-log sentence was cut. S11: "You are already in the data-versioning
  folder, so run sh docker-shell.sh." S13's notebook sentence was cut entirely (the GREY note says
  it). S10: "Add tools, like versioning, and the lecture calls it a data lake."

## Review 4 · flow (V1–V53): 42 applied, 7 adapted, 4 skipped

- **V1 applied** — "…and writes that fingerprint into the pointer file" (now in the V5 prediction
  block).
- **V2 applied** — sentence split (the lexicon entry was added by the coordinator).
- **V3 applied** (coordinator lexicon; no script change).
- **V4 applied** — split, merged with A9 (lexicon entries by the coordinator).
- **V5, V6, V7 applied** (coordinator lexicon; no script change).
- **V8 applied** — "…which leave a marker object. That was the trap." (the `implicit dirs` entry
  was added by the coordinator; the two words stay adjacent).
- **V9 applied** — "The README's extra section runs…"
- **V10 applied** — "the depends on setting starts Label Studio first…"
- **V11 skipped** — superseded: P18 cut the sentence.
- **V12 applied** — via A19, "still a fraction of a cent a month".
- **V13 applied** — "You give Image 2 the new name brie 2, and add again."
- **V14 adapted** — the review's alternative: the S15 SHOW re-anchors K5 on "from anywhere" (0 words).
- **V15 applied** — with A7.
- **V16 adapted** — split into two sentences (+3 words, not +8): "…the images folder you upload to,
  and the cache on your disk, filled by dvc add. The third is the DVC store, …"
- **V17 applied** — the recap became four short sentences, the review's text, plus P1's closing
  line.
- **V18, V19, V20 applied** (coordinator lexicon: "1001", gouda, parmigiano).
- **V21 adapted** — "load the libraries" in place of "run the imports" (0 words, no noun "imports").
- **V22 applied** — split.
- **V23 applied** — split.
- **V24 adapted** — split into "…walks the rope. It clones the repo at that tag, reads that commit's
  config to find the bucket, then fetches the manifest, then the photos." (two sentences, not
  three).
- **V25 applied** — split. The later "which the container mounts" clause was cut for budget; the
  `~/.gitconfig → /etc/gitconfig` arrow stays.
- **V26 applied** — split.
- **V27 applied** — split.
- **V28 applied** — split (the `data-service-account` entry was added by the coordinator).
- **V29 applied** — split.
- **V30 applied** — "…on a shelf named by the first 2 characters." (inside the P3 prediction block).
- **V31 adapted** — split; the byte count is no longer spoken (cut for budget; line 60 stays
  highlighted).
- **V32 applied** — all four splits. In S10, "your repo, secrets and git config" (not "your" ×3).
- **V33 applied**.
- **V34 applied**.
- **V35 adapted** — "only if it is missing" applied; "as in the last lecture" was cut for budget (the
  sticky note says "L10's shape").
- **V36 adapted** — merged with P20.
- **V37 applied**.
- **V38 applied** — "because ADC looks for the key".
- **V39 applied**.
- **V40 applied** — "after you exit the command line container".
- **V41 skipped** — the clause ("where that bites") was cut for budget; route T in S12 shows it.
- **V42 applied** — "Git's hint mentions master".
- **V43 applied** — "git ignore file".
- **V44 applied** — "into the images folder".
- **V45 applied** — "Image 1 through Image 4".
- **V46 applied** — "the privileged flag".
- **V47 applied** — "makes a version with zero files".
- **V48 skipped** — after P27's split, "a different one" sits in the sentence right after "a new
  manifest fingerprint", so the referent is adjacent. The longer form would cost 2 words in S14.
- **V49 applied** — "the quiet flag hides errors too".
- **V50 applied** — "Buckets cost money until you delete them".
- **V51 applied** — "the format is the same" (the mushroom gloss is now only on the chip).
- **V52 applied** — "why can't…".
- **V53 skipped** — a series decision (the `October 2025` key is not in the lexicon); the
  Conventions block says so.

## Word-budget trims (logged per the merge rules)

The mandated fixes added about 270 words to a 4,282-word draft. The largest additions were P6,
P1, P2, F2/A5/P10, A2, A1, F5/A6, F6, P3/P4/P5, P9, F3 and F4. Before trimming, the draft stood at
4,554. The additions were paid for with the review-proposed cuts (P17, P18, P20, P24, P25, P28,
P29, P30, P12's slide sentences) and with polish-level cuts of my own. Each cut removes either a
spoken restatement of something still on screen, or a connective. None removes a README command,
a tag, a `recorded` source or a fix above. Cuts that remove a spoken fact still shown on screen:

- S03: "about 3.7 megabytes" (`07:2` highlighted); "about 3.8 megabytes" (the GOLD tag says ≈ 3.8
  MB); the stand-in sentence was shortened to "a stand-in, explained in scene 5".
- S04: "and prints a container ID" (chip "yours will differ"); "Two extra checks confirm both
  halves." (`14`, `15` on screen); "as in the last lecture" (sticky note).
- S05: "So private means no outside labeling company sees your data." S04 already says "no outside
  labeling service sees your photos", and P21 dropped the slide-7 card. **This narrows the BRIEF's
  Conflict 3** (see the coordinator list).
- S06: "Same bouncer as last lecture, now on a bucket." (chip "L10: the Chroma bouncer · now on a
  bucket"); "the gcloud tool can set the rule too" (erratum chip).
- S07: "Two extra curls prove it" (two panels); "a mushroom from an older course app" (chip).
- S08: "Two real surprises."; "Your labels are safe." (the YELLOW parked card).
- S09: "of the five reasons on screen, watch save space" (card); "we will see where that causes
  trouble" (S12 shows it); "An extra listing shows 7 files and no DVC folder." (chip; the last
  block still says "the 7 files on main").
- S10: "a gold tag, a few hundred kilobytes" (GOLD tag); "the other two are passed in and ignored"
  (chip "passed in · read by nothing"); "a tool called".
- S11: "it installs gcsfuse and the cloud tools"; "On your laptop, this folder stays empty." (`89` +
  chip).
- S12: "the values from part 1" (S03's PINK pin); "611,101 bytes" (`95:60` YELLOW); "which the
  container mounts" (arrow); "This is why you list first." (the S11 rule card flashes); "An extra
  listing of"; route T's "still" and "as we did".
- S13: "same shelves, same names" (drawn mirror); "A real bucket prints the same summary." (chip "any
  remote prints this summary"); "The README's notebook waits until scene 15." (GREY note).
- S14: "712,574 bytes" (`104:60` YELLOW); "the fingerprint, the size and the count" (diff lines
  YELLOW); "Two flags now sit on two commits, and their ropes share four photos." (the V6 picture).
- S15: "The class bucket refuses anonymous callers." (`122` RED strip); "under the next cell"
  (erratum card).
- S16: "with rules, anomaly detection or lineage" (one line on screen); "Containers and the network
  are already gone." (card line 1).

## BRIEF.md changes (sync only where the merge changed structure)

- Running example: the project-id rule (A4's coordinator decision), mirroring L10 BRIEF:110–113.
- V4: stage 1 = the key into line 10's `--key-file`; line 8 is a side note (A8).
- V5 (:199): played as a prediction before `dvc add`'s output (P3); `120` beside ours in S12; the
  `121` diff runs in S13 (A1).
- V6: `.dvc/cache` = "copies made by dvc add" (A18); `dvc_store/` never overwritten (P6).
- S01 / S13 GOLD wording: "a fraction of a cent a month" (A19).
- S06: ponder 4 answer (A3).
- S07: database first, then target storage on submit (P9); `27` as a stand-in strip (A13); two
  kinds of token and the legacy-token ▶ beat (F2/P10/A5); "open one" (F15).
- S08: `exit` first (F4).
- S09: the opening reordered around the parked question and "why not git alone" (P6); `cd ..`
  first (F1); the pinned-README chip (F8).
- S12 (:546): a numbered beat list in the new order (P3, A1, P1, P5, P26, F14).
- S13: the `121` diff after `102` (A1); the "never overwrites" line answering S08's question (P6).
- S14: time travel tagged `extra · stand-in` with the honest warning (A2); the three ▶/pause
  blocks (F3, P27).
- S15: A6's wording; the ▶ after the instructions (F5); the edited cell 15 and the private-repo
  chip; the 18KYngbv chip (F8).
- S16: the new beat order and the hook closure (P29, P1); shuffled tools (P28).
- Ponder table rows 4 (A3) and 5 (A14); recap Q1 (P29); the teardown checklist (F6).

## For the coordinator

1. **Git**: `build/` is gitignored (`.gitignore:2`), so this file needs `git add -f`, as the four
   reviews had. The batch WIP commit `977aecf` already holds `script.md` in its final v2 state
   (`git diff HEAD` shows only `BRIEF.md` modified).
2. **exercises.md** (P29): route the two outcomes the recap does not test — why the host's
   `cheese_dataset/` looks empty, and why git holds only the pointer.
3. **S05 "private"** (Conflict 3): the sentence was cut for budget. S04's "no outside labeling
   service sees your photos" plus the V2 picture now carry it. Restoring the sentence costs +10 in
   S05 (298 → 308, still in band) and would need a matching cut elsewhere to stay under 4,300.
4. **Unverifiable from here**: the 1.23 *Account & Settings* labels (drawn lower-case, tagged
   `illustration`); Label Studio's export-on-submit (digest + README, not captured); the github.com
   blob URL with the short hash (the raw URL resolves).
5. **Series decisions left open**: V53 (`October 2025` lexicon key) and A12 (`x86_64` spoken).
6. **digest.md §6 #10** still has A3's "rule goes to another bucket" shortcut (outside this merge).
7. **Tight margins**: total 4,286/4,300; S12 354/368 and S16 260/264 sit near the top of their
   bands, so any later addition there must name its cut in the same scene.

## Final word counts (`python -m explainer.script`, after merge)

| scene | words | BRIEF | ±15 % band |
| --- | --- | --- | --- |
| S01 | 210 | 220 | 187–253 ✓ |
| S02 | 238 | 250 | 213–287 ✓ |
| S03 | 234 | 230 | 196–264 ✓ |
| S04 | 293 | 300 | 255–345 ✓ |
| S05 | 298 | 290 | 247–333 ✓ |
| S06 | 292 | 290 | 247–333 ✓ |
| S07 | 303 | 310 | 264–356 ✓ |
| S08 | 233 | 230 | 196–264 ✓ |
| S09 | 243 | 240 | 204–276 ✓ |
| S10 | 288 | 290 | 247–333 ✓ |
| S11 | 237 | 260 | 221–299 ✓ |
| S12 | 354 | 320 | 272–368 ✓ |
| S13 | 284 | 300 | 255–345 ✓ |
| S14 | 263 | 260 | 221–299 ✓ |
| S15 | 256 | 250 | 213–287 ✓ |
| S16 | 260 | 230 | 196–264 ✓ |

**Total: 4,286 words** (required 3,900–4,300). Part 1 (S01–S08) = 2,101; part 2 (S09–S16) =
2,185. The Conventions length table was updated to match.
