# Review · lens 2 — newcomer pedagogy

Script at commit 1da63fa (`claude/ac215-l09-l13-batch`), read start to finish at viewing pace as
the BRIEF's target viewer: L01–L10 done (images, containers, bind mounts, Compose, networks,
published ports; from L10, service accounts, `../secrets`, ADC, Docker DNS vs `localhost`, CORS for
a container API). New to Label Studio, source/target storage, pre-signed URLs, DVC, gcsfuse, CORS on
a bucket. Read against `BRIEF.md` (V1–V7, ponder table, recap questions, outcomes),
`docs/AC215_SERIES.md` (rule 4: concept before command), `docs/STYLE_GUIDE.md` §1 (≤3 groups, one
idea per beat) and the AGENTS.md content gates. Captures opened where a beat's teaching depends on
what the terminal prints (`95:56-70`); `digest.md` checked for the token kinds (line 347) and the
console's folder placeholder (line 214).

Narration now: **4,282** words (my count matches the script's). Ceiling 4,300, so every addition
below names its cut, and the ledger at the end balances to **4,292** with every scene inside the
BRIEF's ±15 %.

## Gate checks

**Gate 1 · the hook.** S01's Monday/Friday puzzle is a real one: two folders, same names, same
count, different data, and a model that got worse. It is never paid off as asked. Part 2 freezes
photos, not labels. Nobody returns to Monday's model, and S12's payoff closes only the md5 teaser
(P1).

**Gate 2 · one animated mechanism per core idea, intuition before formalism.**

| core idea | mechanism | verdict |
| --- | --- | --- |
| one `docker run`, flag by flag | V1 peel-off | real, strong |
| who touches the bytes | V2 ticket | real; the reveal skips the alternative (P8) |
| CORS on the bucket | V3 bouncer + rule card | real |
| a label is a note | V2 step 4 envelope + thread | real; the database half is missing (P9) |
| Docker DNS vs localhost | V1 reprise + phone book | real (L10 recall) |
| gcsfuse + bind chain | V4 four stages, broken replay | real; nothing flows down the pipe (P13); the host-vs-container layer is drawn but never said (P12) |
| content addressing | V5 hash shelf | real, but plays *after* the output it explains (P3), and "fingerprint" is never defined (P2) |
| pointer in git, bytes in bucket | V6 rope, three homes | real; the "why" behind git-only-pointer is missing (P6) |
| `dvc get --rev` | V6 rope pull **before** the command | real, and the model the other scenes should follow |

**Gate 3 · ponders and recap.** 10 ponders plus 2 quick predicts, about one every 2.5 min. Audit:

| # | scene | answerable from what was shown? | answer lands? |
| --- | --- | --- | --- |
| 1 | S02 | as an L04/L10 recall, yes | the answer names "the command line container", which was never introduced (P11) |
| q | S03 | yes (the twins are said first) | yes; "task" is undefined (P19) |
| 2 | S04 | yes (`docker logs`, L2–4) | yes |
| 3 | S05 | only via the "pre-signed URLs" checkbox | partly; the relay alternative is never ruled out (P8) |
| 4 | S06 | suspect 1 yes, suspect 2 never seeded | partly (P23) |
| 5 | S07 | yes (L10 + S06's chip) | yes; it interrupts the token step (P24) |
| 6 | S08 | yes: block 3 just showed the project surviving a new container (a fair transfer) | yes |
| 7 | S11 | only if S10's silent pull-back is narrated | P12 |
| 8 | S12 | only if a fingerprint depends on bytes alone, which is never said | P2 |
| 9 | S14 | yes | yes, but it lands inside an overloaded block (P27) |
| 10 | S15 | yes (only v20/v21 seen) | yes |
| q | S16 | given away: the tools are spoken in matching order, then "In that order" | P28 |

The content recap exists (S16 block 5, V7 relit piece by piece).

**The recap against the outcomes.** Q1 tests CORS but not who fetches the bytes. Q2 is Docker DNS
(largely L10). Q3 is the pointer. Q4 is the three homes. Q5 is the warehouse, and the teardown
answers it 30 s earlier. Three outcomes are untested:
- the signed URL (who touches the bytes);
- the gcsfuse/bind chain and why the host's folder looks empty;
- why git holds only the pointer.

P29 fixes the first with no extra question. The other two belong in exercises.md.

**The part 1 → part 2 bridge.** S08 parks a good question. S09 opens without it, and S13 never says
the sentence that answers it (P6).

**Where a newcomer gets lost or bored.** S09 → the first `dvc add` in S12 runs about 7 minutes:
clone, bucket, mount theory, a failed build, a failed mount, a Linux failure and route T. In all
that time the viewer has no picture of what DVC will do with the folder. P6's preview sentence and
P3's reorder are the main fixes.

---

## Blocking

P1 · S01 → S12 → S16 · blocking · S01: "So which photos, with which labels, did that model see? And
can you get exactly those back?" (and the YELLOW caption) · The hook asks about photos *and labels*
and about getting them *back*. The video freezes photos only (labels and versions are joined only
in exercise E7, said once in S02 before the viewer knows what "halves" are). S14/S15 show the
"get back" without saying it answers the opening. S12's payoff closes the md5 teaser ("identical")
but not its question ("How can one line pin down about 600 kilobytes?"). The two folders, the
video's first picture, are never answered. A newcomer leaves believing a tag pins labels, or
feeling the opening was a bait. Fix, three small edits:
- **S12 payoff block (+6):** "So one line pins 600 kilobytes: it fingerprints the list of
  fingerprints. And an extra comparison with the instructor's tag in the class repo: identical, on
  any machine." This replaces "And the payoff: … Identical: same bytes, same fingerprint, on any
  machine." S13's "the whole trick" line then repeats it on purpose, one level deeper.
- **S12 Ponder 8 reveal, after "…because one name in the list changed." (+11):** "The opening's
  two folders were the reverse: same names, new bytes." On screen, S01's Monday/Friday cards return
  small, and their manifests differ in one PINK row.
- **S16 recap, after "…and a tag pinning the list." (+15):** "So Monday's photos come back with one
  dvc get; their labels join in exercise E7." On screen, S01's YELLOW caption returns with
  "which photos ✓ tag · which labels → E7".

P2 · S03 → S12 · blocking · S03: "One more extra, for part 2: fingerprints and sizes of the first
five photos. Remember the first one." · "Fingerprint" is the backbone of part 2, but it is never
defined. S12 uses it as known ("It fingerprinted each photo with MD5"). Ponder 8 is answerable only
if the viewer knows a fingerprint depends on the bytes alone and not the name. A viewer who guesses
"the name feeds the hash" answers "the photo's md5" and has no way to see why that is wrong. The
same property carries the hook's "same bytes, same fingerprint", Ponder 9 and recap Q3. Fix, at the
first sight of `09b` (+11): "One more extra, for part 2: each photo's fingerprint, computed from its
bytes alone. Same bytes, same string; change one byte, and it changes completely. Remember the first
one." Visual, no invented values: the five real rows of `09b` show that five different photos give
five unrelated strings, and the PINK ring lands on the first.

## Confusing

P3 · S12 · confusing · "Here is what dvc add did." (V5 after `93`'s empty add, the stand-in copy
and `95`'s pointer) · BRIEF outcome: "predict what `dvc add` writes". Series rule 4: animate the
invisible mechanism first, then type the command and let its output confirm the picture. S12 does
the opposite. The viewer types `dvc add` twice and reads `89db50de…`, `611101` and `4` before
learning what produced them, so there is nothing to predict. (S15 gets this right: the rope pull
plays, then `dvc get` runs.) Fix, a within-scene reorder; the BRIEF's S12 beat list puts V5 later,
so the coordinator should confirm. The new order:
1. `dvc remote add`;
2. V5 as a prediction ("Here is what dvc add will do. It fingerprints each photo…", +1 for the
   tense change);
3. the empty-folder trap, now readable as "the same machine, fed nothing";
4. the stand-in copy + `dvc add` + `cat`, where `nfiles: 4` and `89db50de….dir` light up as the
   prediction confirmed;
5. the cache listing;
6. the payoff.

P4 · S12 · confusing · "now the pointer file says 4 files…" / "and filed each copy under its
fingerprint" / "An extra listing of the cache shows…" · Three new terms arrive undefined:
- "pointer file" (first used in block 6);
- "copy" (a copy of what, where?);
- "the cache" (first named in block 8).

The BRIEF lists DVC pointer files as new to this viewer. Fixes:
- V5 block (+3): "and filed a copy in its cache under that fingerprint," in place of "and filed
  each copy under its fingerprint,".
- Same block (+8): "…and wrote that into the pointer file, which stands in for the folder in git."
- On screen: a GREY chip on the `.dir` box, "the .dir ending marks a folder's list". No words.

P5 · S11 → S12 · confusing · S11 ends "On your laptop, this folder stays empty." Two minutes later
S12 runs `sudo cp … cheese_dataset/` on the host, and the container sees the photos · The viewer
was just taught that the laptop's folder is a dark, empty bystander. Now the video fills that exact
folder from the laptop and it works. That contradicts the lesson, unless the viewer works out that
with no gcsfuse mount the inner bind never happened, so `-v` shows the host folder. Some will copy
the move with a working mount, where the inner bind hides whatever they put there. The caption
"where your bucket's images/ would appear" does not explain it. Fix (+12): "With no bucket mounted,
our stand-in copies four photos into the laptop folder, which the container sees through the repo
mount. Add again:" This replaces "Our stand-in copies the four photos in, and we add again:". On
screen, V4's small two-layer picture shows the inner bind GREY-dashed (absent) and the `-v` window
lit.

P6 · S08 → S09 → S13 · confusing · S08 parks: "So how do you freeze exactly which photos a model
saw? That is part 2." S09 opens with "Part 2, versioning. The lecture gives five reasons…". S13
never answers in one sentence. Four gaps:
- **The question is dropped.** Part 2 opens on a list instead, and parts may be watched separately.
- **"Why not just git?" is missing.** BRIEF outcome: "why git holds only the pointer". S13 gives
  only "because the git ignore file excludes the dataset folder", which says how, not why.
- **No preview before the setup.** The viewer gets no picture of what DVC will do before about 7
  minutes of setup and failures.
- **The answer is never said.** The `images/` folder can change; `dvc_store/` never overwrites.
  That is what freezes a version, and the visuals ("changes" vs "named by fingerprint") hint at it
  without the narration saying it.

Fix:
- **S09 block 1 (+10):** "Part 2: freezing which photos a model saw. Git alone would copy every
  photo version into every clone. Of the lecture's four approaches, we build the file-based one:
  git versions a small file of fingerprints, and a bucket holds the photos. The tool is DVC; of the
  five reasons on screen, watch save space." The five reasons stay on the card, and S14's "the
  saved space the lecture promised" still lands. On screen, a 2 s silhouette of V6 (flag → small
  card → rope → bucket), GREY, "scene 13".
- **S13 three-homes block, after "…named by its fingerprint." (+15):** "Images can change; the DVC
  store never overwrites, since new bytes get a new name." The parked YELLOW card from S08 flies in
  and gets its check mark.

P7 · S05 · confusing · "add source storage with the README's values" / "The target storage, with
the prefix cheeses labeled, fails the same way." · "Source storage" and "target storage" are Label
Studio's terms, listed as new in the BRIEF, and the narration never says what either is for.
S07's "It lands in the cheeses labeled folder" then has no visible cause. Fix:
- **Block 1 (+5):** "and add source storage, where the photos come from, with the README's values:".
- **Block 2 (+3):** "The target storage, where labels go, with the prefix cheeses labeled, fails
  the same way."

P8 · S05 · confusing · Ponder 3 ("…how can it show a private photo?") → "With a signed ticket. For
each photo, Label Studio signs a web address…" · The slide 13 redraw opening this scene links the
browser only to Label Studio, and its chip says so. A newcomer's natural answer is therefore "Label
Studio downloads the photo and passes it on". The reveal never rules that out, so the scene's title
question is half answered. Fix (+3): "With a signed ticket. Label Studio does not relay the photos;
it signs a web address with the key: permission for one photo, for a short time." On "does not
relay", a dashed relay arrow through the TEAL house is crossed out GREY. "With pre-signed URLs on"
is implied by the YELLOW checkbox still on screen.

P9 · S07 · confusing · "It lands in the cheeses labeled folder, pointing back at the photo…" ·
This answers the hook's "where does that word go" with one place. The next scene's ponder answer is
another place, the SQLite file ("The database file is still in the mounted folder… Your labels are
safe"). The viewer cannot reconcile them: are the labels in the bucket or in the database? Fix (+8):
"Label Studio saves it in its database, and target storage copies it to cheeses labeled, pointing
back at the photo, which never moved." On screen, the envelope stops at V1's GREY drawer first, then
a copy flies to the bucket. This also makes Ponder 6 more answerable. Lens 1 should confirm the
automatic export on submit, which README:184-186 implies.

P10 · S07 · confusing · "copy your access token from Account and Settings" → 401 → "this version
ships with legacy tokens switched off… then copy the legacy token" · The viewer copied a token in
block 3, and now is told to copy a *different* one, with no idea there are two kinds. `digest.md:347`
says it: what most people copy first is a JWT personal access token, and `cli.py`'s legacy `Client`
sends `Token <key>`. Fix (+4): "An extra check shows why: this version has two kinds of token, the
legacy kind is switched off, and cli.py speaks only legacy." On screen, the Account & Settings
wireframe shows two blank token rows, "personal" and "legacy", with the legacy row greyed until the
toggle flips.

P11 · S02 · confusing · Block 2: "Part 1 is the labeling station: Label Studio in a container, with
one bucket…" Ponder-1 answer: "The network lets the command line container call Label Studio by
name." · Two TEAL houses are drawn, but only one is named. The ponder's answer then leans on a
container the viewer has never heard of. Fix (+3): "Part 1 is the labeling station: Label Studio
and a small command line container, with one bucket for photos and labels."

P12 · S10 · confusing · Block 6: "…so gcsfuse only shows folders made in the console: that was the
trap. The slides say disks; they mean this bucket. And despite the slides, DVC still keeps a copy on
your disk." · Three problems:
- **Overload.** Four ideas in one block, over 5+ groups: chips, the prefix list, the camera
  pull-back, the two bind-mount labels and two notes.
- **The pull-back is silent.** The host's dark `cheese_dataset/` under two kinds of "bind mount" is
  never narrated, yet S11's Ponder 7 depends on it.
- **"Folders made in the console" sounds like magic.** The mechanism (the console writes an empty
  `images/` marker object, `digest.md:214`) is unsaid.

Fix (+7). Replace the two slide-correction sentences: S13 already carries "slide 33: no local copy ·
DVC keeps one" as a chip beside the three homes, which say "the cache on your disk", and the "disks"
note can stay a GREY chip. The new text:
- "…so gcsfuse only shows folders the console made, which leave a marker object: that was the
  trap." (in place of "…folders made in the console: that was the trap.")
- "Note the two bind mounts: dash v joins your laptop's repo to the container, and the inner one
  joins the bucket's images folder." It describes without concluding, so Ponder 7 still asks
  something.

Split the SHOW: chips + prefix list first, then the pull-back on the new sentence.

P13 · S10 · confusing · "Mount the whole bucket as a folder, with a tool called gcsfuse… DVC works
on that folder as if it were local." · From L2–4 the viewer knows bind mounts of real folders.
"Mounting a bucket" is new (the BRIEF says so), and the PINK pipe carries nothing, so the viewer
cannot tell whether the photos were downloaded, synced or streamed. Fix (+8): "Then use the data:
DVC works on that folder as if it were local, while each file is fetched from the bucket." On
screen, on "fetched", a request dot runs up the pipe and a blank tile comes back down.

P14 · S15 · confusing · Block 2 ends "Pause and work through it." Only *after* the pause do blocks
3–4 say "For your repo, replace the address and the tag" and "Your repo is private, so the notebook
needs an access token". A follow-along viewer pauses, runs the defaults against the class repo, or
pastes their private repo's URL without a token, and fails before the video says why. Fix: move the
instructions before the pause (−3).
- **Block 2:** "Open the notebook from the README and save a copy. Install DVC, run the imports, and
  sign in with your Google account. Then list your repo, fetch your tag, and count the files:
  replace the address and the tag first. Your repo is private, so put an access token in the
  address, or make it public. Pause and work through it."
- **Block 4:** "Signed in, the instructor's run shows five files in the class version 21, and a count
  of 5; your version 20 gives 4."

P15 · S13 · confusing · "Tag the commit as dataset v20…" · The BRIEF lists "git tags as dataset
versions" as new. A tag is never glossed, yet it carries the whole S13–S16 arc: the flags, the
rope, `--rev`, recap Q5. Fix (+2): "Tag the commit, a permanent name, dataset v20, and push the
branch and the tag together…".

P16 · S14 · confusing (route to lens 1) · "Check out the old pointer file with git, run dvc checkout
in the container… Both come straight from the cache on your disk." · On our machine the folder is
the host folder. With a real key, `cheese_dataset` *is* the bucket's `images/` through the bind, so
`dvc checkout` to v20 would remove `Image_5.jpg` from the bucket, and back to main would write it
back. A viewer told "from your disk" will not expect their bucket to change. Fix (0 words): a GREY
chip on the first `dvc checkout`, "with a real mount, this rewrites your bucket's images/ too", if
lens 1 confirms gcsfuse's write-through here.

## Polish

P17 · S01 · polish · Four questions in about 75 s: which photos and labels, can you get them back,
how can one line pin 600 KB, where does gouda go. Fix (0 words): one question card on screen at a
time. The gouda envelope gets its own beat after the md5 line fades. Cut "The lecture makes fun of
exactly this habit." (−8); the `lecture_ref` tag already says it.

P18 · S02 · polish · Block 2's frame holds the top row, two stations, two buckets with four
drawers, the repo with flags, Colab, the E7 bridge and the training box: 6+ groups. Fixes:
- **Frame (0 words):** the slide-6 row shrinks to a thin strip as the stations build, and the
  versioning half is drawn as outlines until S09 relights it.
- **Cut, −14:** "One, pipeline flow, draws this map with a single bucket; no README links it." Right
  after "two buckets", it makes the viewer doubt the map. Keep the chip.
- **Cut, −7:** "The lecture begins with a recall quiz, so here it is." becomes "The lecture's recall
  quiz:".

P19 · S03 · polish · Quick predict: "How many tasks should Label Studio make?" · First use of
"task". Fix (0 words): the QUICK card reads "How many tasks\n(one item to label each)\nshould Label
Studio make?".

P20 · S04 · polish · "Underneath, as stand-in calls, the server side…" · The first "stand-in" since
S03's promise, with no gloss: why not just show the screen? Fix (0 words): "Underneath, replayed as
the page's own requests: logged in, and project 1 holds the four cheeses." Also cut "Two curls get
status up and the login page." (−9); the outputs and the `extra` tag carry it.

P21 · S05 · polish · The last block stacks V2 (browser, house, vault, ticket, bouncer), the slide-7
GREY card, the broken task grid and a README card: 4+ groups under one SAY. Fix (0 words): V2 clears
before the grid; drop the slide-7 card (the narration says the same).

P22 · S06 · polish (lens 1) · A sharp newcomer knows web pages show other sites' images all the time
without CORS: why does this photo need it? If lens 1 confirms how Label Studio loads images (with a
cross-origin request, for its canvas), add a GREY chip (0 words) on V3: "Label Studio requests the
photo for its canvas → the browser checks". Otherwise, skip.

P23 · S06 · polish · Ponder 4 reveal: "One: the rule went to another bucket, because line 23 kept the
old name…" · The most visible suspect, "dash c just failed here", goes unmentioned, and suspect 2
(cached answers) was never seeded. Fix (+2): "One: the rule missed your bucket: dash c failed, or
line 23 kept the old name; dash m tells you." Add a GREY chip on S08's compose bucket-name beat:
"same trap as scene 6, suspect one".

P24 · S07 · polish · Block 3 asks the viewer to copy the token, then switches to a networking
ponder. The token is used two blocks later. Fix (0 words):
- Block 3 keeps only "The command line container calls Label Studio by name. Something to ponder:
  what if its address were localhost 8080?". It follows from S06's "a name, not localhost" chip.
- "To list labels from code, copy your access token from Account and Settings. Pause and copy it."
  opens the `-p` block (tracker D1 → D2).
- Cuts: "Forget dash k, and the error has a small typo: i required, meaning is required." (−15; keep
  `42:68-69` and the chip, unspoken, at the end of the `-t` block). "Switching to the newer client
  is an exercise." (−8; the chip says it).

P25 · S08 · polish · Block 3 carries two surprises (compose's bucket name, `depends_on`) under
5+ groups. Fixes:
- **Split (0 words):** a second block starting at "And the first call is refused".
- **Cut, −10:** "…which explains a stray line in the README's sample listing". The chip "the stray
  line, explained" stays.
- **Cut, −12:** "The images take 1.5 and 1.76 gigabytes, at the time of recording." It stays on
  screen with its chip.
- **The bridge, made concrete (+4):** "But the photos they point at can change under them: same
  name, new picture." It echoes the hook.

P26 · S12 · polish · "Now the trap:" · S10 already used "the trap" for implicit dirs, so the viewer
looks for the wrong one. Fix (0 words): "A second trap:".

P27 · S14 · polish · The Ponder 9 answer arrives in a block with six terminal beats, V5, a chip and
the counter, all under one SAY. Fix (0 words): split at "Then push:" so "2 files pushed" and the "2
pushed, not 6" counter land in their own block.

P28 · S16 · polish · Quick predict: "Match DVC, lakeFS, and Delta Lake or Iceberg." → "In that
order." · The tools are spoken in the matching order, so the answer is given away, and the SAY
repeats the card's three questions. Fix (−15):
- **The predict:** "A quick prediction: three questions, three tools. Match Delta Lake or Iceberg,
  DVC, and lakeFS."
- **The answer:** "DVC, lakeFS, then the table formats. There is no single standard; …". Chips
  shuffle on screen in the spoken order.

P29 · S16 · polish · Recap and teardown. Three problems:
- The teardown says "never delete the DVC store while any tag should still work; a tag is only a
  pointer" about 30 s before Q5 asks exactly that.
- Q1 misses the signed-URL outcome.
- "Every command in the study guide" repeats S01.

Fix:
- **Order (0 words):** recap → test yourself → teardown checklist → next. The checklist then
  confirms Q5 instead of answering it in advance.
- **Q1 card and SAY (+3):** "One: who fetches the photos, and why does that make the bucket need its
  CORS rule?"
- **Cut, −6:** "Answers are in the exercises, every command in the study guide." becomes "Answers are
  in the exercises." The footer card keeps the guide.
- **exercises.md:** route the two untested outcomes there (the host's empty folder; why not git).

P30 · all · polish · "extra" is spoken 35 times. Series rule 1 asks for it in the narration, so no
blanket change. Three low-value extras whose content stays on screen are cut to fund the fixes
above:
- S09: "An extra git log shows the starter, from October 2025." (−10)
- S11: "The README says to be inside the data-versioning folder, which you already are, then run sh
  docker-shell.sh." becomes "You are already in the data-versioning folder, so run sh
  docker-shell.sh." (−6)
- S13: "The notebook comes next in the README; we view both versions there, shortly." becomes "The
  README's notebook waits until scene 15." (−6)

S10's data-lake line is also tightened: "Add tools, like versioning, and the lecture calls it a data
lake." (−5).

---

## Word ledger

| scene | now | after | BRIEF | Δ vs BRIEF | changes |
| --- | --- | --- | --- | --- | --- |
| S01 | 219 | 211 | 220 | −4.1 % | P17 −8 |
| S02 | 256 | 238 | 250 | −4.8 % | P11 +3, P18 −14 −7 |
| S03 | 232 | 243 | 230 | +5.7 % | P2 +11 |
| S04 | 302 | 293 | 300 | −2.3 % | P20 0, −9 |
| S05 | 292 | 303 | 290 | +4.5 % | P7 +5 +3, P8 +3 |
| S06 | 300 | 302 | 290 | +4.1 % | P23 +2 |
| S07 | 299 | 288 | 310 | −7.1 % | P9 +8, P10 +4, P24 −15 −8 |
| S08 | 234 | 216 | 230 | −6.1 % | P25 −10 −12 +4 |
| S09 | 247 | 247 | 240 | +2.9 % | P6 +10, P30 −10 |
| S10 | 293 | 303 | 290 | +4.5 % | P12 +7, P13 +8, P30 −5 |
| S11 | 249 | 243 | 260 | −6.5 % | P30 −6 |
| S12 | 326 | 367 | 320 | +14.7 % | P1 +6 +11, P3 +1, P4 +3 +8, P5 +12 |
| S13 | 271 | 282 | 300 | −6.0 % | P6 +15, P15 +2, P30 −6 |
| S14 | 251 | 251 | 260 | −3.5 % | P16 0, P27 0 |
| S15 | 252 | 249 | 250 | −0.4 % | P14 −3 |
| S16 | 259 | 256 | 230 | +11.3 % | P1 +15, P28 −15, P29 +3 −6 |
| **total** | **4,282** | **4,292** | 4,270 | | net +10 |

S12 sits near its +15 % edge. If P3's reorder or the scene authors need breath there, P5's sentence
can lose "four" and "through the repo mount" goes to a chip (−5).

---

**Verdict: 2 blocking · 14 confusing · 14 polish (30 findings). Fit for scene production after the
blocking and confusing fixes, all inside the word budget (4,282 → 4,292).**
- **The blocking items:** the hook (Monday's photos, their labels, "get them back") is never
  answered; "fingerprint" is never defined, though Ponder 8, the payoff and recap Q3 stand on it.
- **The largest confusing items are structural:** S12 explains `dvc add` after its output (series
  rule 4, BRIEF "predict"); part 2 opens without the parked question or the "why not git" reason
  and never says what freezes a version; S10's pull-back is silent though Ponder 7 needs it; S12's
  stand-in fills the folder S11 just called always empty.
- **The rest are missing glosses:** source/target storage, the second container, the cache, the
  pointer file, a tag, two kinds of token. One clause each.
- **The ponders are well chosen:** 8 of 12 are fully answerable and land; the fixes above repair the
  other four.
