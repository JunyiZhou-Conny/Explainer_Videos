# L11 script v1 (1da63fa) — review lens 1: technical accuracy

Scope: every SAY/SHOW claim in `script.md` checked against `assets/terminal/laptop/*.txt`,
`assets/terminal/colab/*.txt`, `assets/source/**`, `ASSETS.md`, `digest.md` (§1–§3, §6, §10 errata
and open questions), `SLIDES.md`, and the tools' behaviour (DVC content addressing and checkout,
`.dvc` pointer fields, gcsfuse / `mount --bind` and mount propagation, CORS, Label Studio storage and
tokens, Docker networking and bind mounts). Line numbers are file lines (capture line 1 = the `$`
command); `script.md:N` points at the quoted line.

**Verified clean (no finding):** every TERM range and every highlighted capture line, checked file
by file: 00:4–6; 01:2; 02:2; 03:2–19 (9/10/11/14–16/17); 05:2–6; 06:2–5; 07:2; 08:2–9, 44–45;
09:2–4, 11, 23–29; 09b:2–12 (md5s 2–6); 10:2–3, 70–72; 11–18 (incl. 12:3 `Exited (1) 25 seconds
ago`, 13:5/8/12, 14:6, 15:2, 16:5, 18:3); 19:10–13, 16, 20–21 (8–9 cropped); 20:2; 21:2; 23:2;
24:2–7; 27:2; 28:6; 29:2–4; 30:3; 31:3; 32:2–5; 33:2–4; 40:2–3; 41:3, 26–31, 33–34, 65–66, 68–69,
100–101, 109, 111; 42:33, 36–38, 43, 66, 68–69; 43:2; 44:33–36, 38–42; 50–53; 54:28–30, 38, 40–41,
123–124, 126–130; 55; 60–64; 70–72; 74; 75; 77:2, 15; 78:2–9; 79–82; 84:2–3, 18–26; 85:2–7;
86:2, 1075–1081, 1125; 87:2; 88:2–3, 27–32, 39, 41–42, 45–52, 66; 89:2–4; 90:27–28, 41–42, 46,
50–52; 91; 92:2–6; 93:46, 48, 52, 64, 66–69, 71–75, 81–86, 107; 94:2–8; 95:46–63, 65–70, 72–74,
77–82; 96:2–18 (5–7, 12, 13–14, 18); 97–99; 101; 102; 103:5–9; 104:46–63, 65–67, 71–74; 105–108;
110:7–15; 111; 112; 113:2; 114:2; 115:49, 51; 116; 117:49, 51; 118:2, 4, 6; 120:2–7, 10; 121:2;
122:4–5; 131:2; 137:2–12; 145:47, 49–50, 52–55; 150; 151:2–9, 20; 152:2–5; colab C07b:2, C13:5,
C19, C20:2–4, C19b:2. All crop rules (33–38/40 of the DVC re-entries, 34–39/41 of 145, 19:8–9,
63/72:5–6, 152:6–7) match the files, and the only inline `[exit N]` lines are 20:2 and 27:2, as the
conventions say. Every CODE range and highlighted line: data-labeling `docker-shell.sh` 5–9, 12–24
(6, 9, 12, 14–17, 19–20), `docker-shell-CLI.sh` 15–25 (17, 19, 23, 24), `cli.py` 22–34 (23, 26–33,
34), 35–38, 40, 47–72, 75–83 (79), 123, `docker-compose.yml` 13–18 (17), 19–20; starter
`docker-shell.sh` 5–10, 17–27 (18–23), `docker-entrypoint.sh` 8–13 (11), `Dockerfile` 36,
`.gitignore` 3; `data-versioning@2515e5e/README.md` 76–82 (78, 81). Every README card line: data-
labeling 14, 18, 37–40, 44–50, 62–65, 67–72, 76, 91–97/95, 110–115, 121–134, 138–146, 151, 153,
157, 165, 174–177, 184–187, 193–196, 204, 218–229; data-versioning @ b240b1a 81, 84, 104,
106–110, 121–125, 140–144, 148–170, 174–187, 201–205, 215–230, 234–238, 256–260, 279, 312, 321,
324–328, 336–341, 338, 372, 383; starter README 148. Notebook extract lines 47, 276–283, 292,
302–303, 310–314, 328–329, 331, 352–353, 355, 361–362, 370.
Numbers: 3,720,496 B ≈ "3.7 MB"; 21 + 21 files (42); ≈ 3.8 MB for the 21 images (digest §2,
3,767,117 B); 611,101 B ≈ "600 kB"; `89db50de….dir`/611101/4 and `6b342844….dir`/712574/5; md5
aisles `5b`/`ba`/`91`/`5b`/`89`; 5 then 2 files pushed; 6 files in the v20 commit; 7 files in the
starter; tags v20/v21/v30 only; uid 1001; +25 s; 1.5 / 1.76 / 2.73 GB; versions 1.23.0 / 1.23.2,
Python 3.12.15 / 3.11.17, uv 0.13.5, dvc 3.63.0 / 3.67.1, Docker 29.8.2, Compose v5.6.0, git
2.54.0. Causal claims verified: Docker auto-creating the missing bind source as root vs a uid-1001
image (13/14/15); `-d`, user-defined network DNS, `-p` publish, `localhost` inside a container
(41:109/111); ADC failing at `storage.Client()` because the variable points at a missing file
(41:39–66); pre-signed URLs and the browser fetching straight from `storage.googleapis.com` (digest
§3.2); `maxAgeSeconds` only caching preflights; CORS ignored by curl and not access control;
`docker stop` keeping the name (52:30); compose's own bucket copy (54:38) and `depends_on` not
waiting (54:41–124); prune keeping bind-mounted folders (64); the entrypoint's unconditional
"mounted" echo and missing `set -e` (88:41, 45); both mounts invisible on the host (mount
propagation, 89); libgit2's ownership refusal and the `safe.directory` fix via the
`~/.gitconfig → /etc/gitconfig` mount (90, 92, 93); `dvc add` on an empty folder (93:82–84); the
`.dir` manifest of sorted `{md5, relpath}` (digest §3.5) and the rename ponder answer; route T's
refusals (145); `--atomic`; the 401 at the manifest in the rope's order (C13:5); `--quiet` hiding
the error (C19/C20/C19b). Honest framing: S05's card, every `recorded` card (S05, S06, S15), every
`extra · stand-in` / `extra · local remote` tag on 23–33, 43, 94, 95, 103, 104, and the no-panel
`git push` / SSH clone beats match ASSETS.md. No real e-mail, user name or person's name is
rendered (`student@example.com`, `YOUR_GITHUB_USERNAME`, `<course instructor>` throughout).

---

## Findings

### Wrong

**A1 · S12 · wrong** · SHOW (`script.md:926–934`): the second-terminal strip types
`diff <(git -C class-data-versioning show dataset_v20:cheese_dataset.dvc) <(git -C data-versioning show dataset_v20:cheese_dataset.dvc) && echo identical`
→ `TERM(laptop/121: 2)`; SAY (`:935`) "Identical: same bytes, same fingerprint, on any machine."
· Evidence: the right-hand side reads **our** tag `dataset_v20`, which does not exist until S13
types `git tag -a dataset_v20 …` (`99-git-tag.txt:1`, `script.md:976`). The capture ran in that
order (`121` after `99`–`102`; ASSETS.md:194, 203–204). At the S12 moment a viewer typing the
command gets `fatal: invalid object name 'dataset_v20'` and `diff` sees an empty stream, so the
panel shows a success that cannot happen where it is placed. (The placement comes from BRIEF.md:199
and :546.)
· Fix: keep `120: 2–7` in S12 (the class card sliding in beside our `95:58–63` card, "same 32
characters", no command typed on our side), and move the `121` diff into S13 right after
`git show dataset_v20:cheese_dataset.dvc` → `TERM(laptop/102: 2–7)`, where S01's PINK line lands.
SAY S12: "And the payoff: the instructor's tag in the class repo holds the same fingerprint,
character for character." SAY S13 (after "the tag pins these six lines"): "An extra diff against
the instructor's tag: identical, same bytes, same fingerprint, on any machine." Note the BRIEF
placement in the reply to the coordinator.

**A2 · S14 · wrong** · "One extra experiment: time travel without the cloud. Check out the old
pointer file with git, run dvc checkout in the container, and the folder holds four photos again.
Back to main, and five. Both come straight from the cache on your disk." (`script.md:1047`; SHOW
`:1039–1046`, no stand-in tag)
· Evidence: on a student's machine `/app/cheese_dataset` **is** the bucket's `images/` folder
(`data-versioning@data-versioning-ac215/docker-entrypoint.sh:13`; SLIDES.md:198–199, slide 32:
"every read and write actually lands in the bucket"). `dvc checkout` makes the workspace match the
pointer: here it removed `Image_5.jpg` (`115-dvc-checkout-v20.txt:49–51`) and wrote it back
(`117:48–51`). Through gcsfuse that is a delete of `images/Image_5.jpg` in the bucket and a
re-upload on the way back; a viewer who stops at v20 has silently removed photos from `images/`.
The captured run only worked "without the cloud" because the folder was the unmounted stand-in
(`94`, `103`; ASSETS.md:320–324), yet the beat carries no `stand-in` tag.
· Fix: SAY "One extra experiment, on our stand-in folder: check out the old pointer file with git,
run dvc checkout in the container, and the folder holds four photos again. Back to main, and five,
both from the cache on disk. With a real mount, this folder is your bucket's images folder, so
checkout deletes and rewrites photos there; to look at an old version, use dvc get, next." SHOW:
tag `extra · stand-in` on `114`–`117`, plus a GREY chip "real mount: checkout writes to images/ in
the bucket".

**A3 · S06 · wrong** · Ponder answer, SAY "One: the rule went to another bucket, because line 23
kept the old name; dash m tells you." (`script.md:586`; SHOW `:582–583`, "the rule card flying to a
second, GREY bucket")
· Evidence: line 23's old value is the instructor's `cheese-app-data-demo`
(`data-labeling/docker-shell-CLI.sh:23`), in another project; bucket names are global (S03).
`set_cors_configuration()` calls `storage_client.get_bucket(bucket_name)` before patching
(`cli.py:25`), so with an unedited name `-c` stops with an error (no access to, or no such,
bucket) and patches nothing: no rule "goes to another bucket". The silent-wrong-bucket case needs
a name of a bucket the key *can* write, e.g. a typo naming your part-2 bucket. Digest §6 #10
carries the same shortcut.
· Fix: SAY "One: the rule went to a different bucket of yours than the one Label Studio reads,
because line 23 names it; dash m shows which bucket got the rule." SHOW: the rule card flies to
the viewer's *other* BLUE bucket; chip "an untouched README name fails outright: not your bucket".

**A4 · S04, S06, S08, S10 · wrong (masking rule)** · CODE panels render the course's project id
`ac215-project`: `data-labeling/docker-shell.sh:22` inside the 12–24 window (`script.md:416`),
`docker-shell-CLI.sh:21` inside 15–25 (`:555`), `docker-compose.yml:15` inside 13–18 (`:669`),
and starter `docker-shell.sh:8` inside 5–10 with lines 7–9 highlighted RED (`:782–785`).
· Evidence: the brief's rule allows no project id other than `your-gcp-project`; the conventions'
**Personal data** list (`script.md:115–117`) masks the e-mail but not these four lines. The
README's own placeholder for this value is `YOUR_GCP_PROJECT_ID` (`data-versioning/README.md:203`).
· Fix: add to the Personal-data convention: "`data-labeling/docker-shell.sh:22`,
`docker-shell-CLI.sh:21`, `docker-compose.yml:15` and starter `docker-shell.sh:8` render
`GCP_PROJECT` as `YOUR_GCP_PROJECT_ID` (the README's placeholder)". S10's RED → GREEN edit still
reads correctly (`YOUR_GCP_PROJECT_ID` → `your-gcp-project`, `85:5`).

### Misleading

**A5 · S07 · misleading** · "Now the README command: python cli.py dash p, dash k, and your token.
Pause and run it. On Label Studio 1.23.0 it fails with a 401: legacy token authentication has been
disabled for this organization." (`script.md:624`)
· Evidence: that message is what the capture's fixed **legacy** token got (`42:43`; the token is
the capture-only stand-in, ASSETS.md:303–308). The token Account & Settings shows by default in
1.23.0 is a JWT Personal Access Token, which the legacy client sends as `Token <JWT>`; that case
was not run and its message is undocumented (ASSETS.md:272–277; digest §6 #11, :347). A viewer who
pauses and runs it is told to expect a message they will probably not see.
· Fix: "Pause and run it. On Label Studio 1.23.0 it fails with a 401. Ours says legacy token
authentication has been disabled for this organization; the token the page shows by default is a
newer kind that this client cannot use either." (No panel for the JWT case.)

**A6 · S15 · misleading** · "Signed in, the notebook shows five files in the class version 21,
and a count of 5." (`script.md:1086`)
· Evidence: those outputs are the instructor's run (`notebook-1RRQ1SlH.cells.txt:304–318, 331,
355`; ASSETS.md:290–297). A student signed in with their own account most likely cannot read the
class bucket (digest §6 #13b: "expect a 403"; §10 open question). Also, cell 13's `dvc list -R`
lists the class repo's default branch (`:303`), not tag `dataset_v21`; it shows five files because
`main`'s pointer equals v21's `3280f8f9….dir` (`data-versioning/cheese_dataset.dvc:2`, `120:10`).
· Fix: "In the instructor's signed-in run, the notebook lists five files on the class repo, the
same set as its version 21, and counts 5. Your account probably cannot read the class bucket, so
use your repo: replace the address and the tag; your version 20 gives 4."

**A7 · S06 · misleading** · "Your browser hands a cross-origin answer to the page only if it
carries a header allowing this origin, and Google adds that header only if the bucket has its own
CORS rule." (`script.md:536`)
· Evidence: a plain `<img>` displays cross-origin images without any CORS header; the rule bites
only when page code reads the response in CORS mode, which is how Label Studio loads the images
(digest §3.3: "When page JavaScript fetches a cross-origin resource **in CORS mode**"). Stated
unconditionally, the scene's core sentence predicts that every website's CDN images would break.
· Fix: "When the page's own code fetches it, as Label Studio does, your browser hands a
cross-origin answer to the page only if it carries a header allowing this origin; …" (+5 words).

**A8 · S10 / S11 · misleading** · V4 binds stage 1 **Authenticate** to entrypoint line 8 "and the
GREEN key sliding into gcsfuse's `--key-file`" (`script.md:791`); SAY S11 "Authentication cannot
find the key file, so the bucket never mounts." (`:839`)
· Evidence: line 8 authenticates only the `gcloud` CLI; gcsfuse reads the key itself through its
own `--key-file` on line 10, and DVC uses ADC (digest §3.7/:224). The two failures are independent:
`88:32` (gcloud) and `88:39` (gcsfuse, "failed to detect credentials: open /secrets/…"). With the
key in place but line 8 removed, the mount would still work. The "so" teaches a dependency that
does not exist.
· Fix: SAY "gcloud cannot find the key file, and neither can gcsfuse, so the bucket never mounts."
SHOW: stage 1 is the key file feeding line 10's `--key-file`; line 8 gets a small GREY side note
"gcloud's own login · not used by gcsfuse or DVC".

### Polish

**A9 · S04 · polish** · "a box offering version 1.23.2, because the image tag is latest; this video
ran 1.23.0" (`script.md:458`)
· Evidence: the box appears because the image's 1.23.0 is older than PyPI's 1.23.2 (`19:11`;
`26:2` `"current_version_is_outdated": true`). The unpinned `latest` tag explains why *your*
version may differ, not the box.
· Fix: "a box offering version 1.23.2, newer than the image; the tag is latest, so yours may
differ. This video ran 1.23.0, at the time of recording."

**A10 · S04 · polish** · "Two curls get status up and the login page." (`script.md:458`)
· Evidence: `21:2` is `302 -> http://localhost:8080/user/login/`, a redirect; the page itself is
`22`, which the scene does not show.
· Fix: "Two curls get status up and a redirect to the login page."

**A11 · S05 · polish** · "The target storage, with the prefix cheeses labeled, fails the same way."
(`script.md:492`)
· Evidence: `31:3` is a generic `"Error validating storage connection"`, not the source form's
`"File /secrets/data-service-account.json was not found."` (`30:3`). Same cause, different text
on screen.
· Fix: "The target storage, with the prefix cheeses labeled, fails too, with a vaguer message."

**A12 · S06 · polish** · "Apple Silicon says aarch64 where this machine says x86." (`script.md:553`)
· Evidence: the highlighted line is `41:27` `Architecture: x86_64`; same question as L10's A11.
· Fix: "… where this machine says x86_64" with a lexicon entry, or keep "x86" (not false).

**A13 · S07 · polish** · SHOW `curl -s -b /tmp/ls.cookies http://localhost:8080/api/jwt/settings`
(extra), typed at the laptop prompt (`script.md:626–627`; conventions `:91`).
· Evidence: the cookie file is the capture's scripted login (`23:1`); a viewer has no
`/tmp/ls.cookies` and would get the 401 of `25:2–3`. Every other call that rides on that login is
an output-only `extra · stand-in` strip.
· Fix: show `27` like the other stand-ins (output only, headed `GET /api/jwt/settings · stand-in`,
tag `extra · stand-in`), or add a GREY chip "uses our scripted login · yours: Organization → API
Tokens Settings".

**A14 · S07 · polish** · "Connection refused: inside a container, localhost is that container"
(`script.md:618`)
· Evidence: the panel says `curl: (7) Failed to connect to localhost port 8080 after 0 ms:
Couldn't connect to server` (`41:109`); "connection refused" is the underlying errno, not on
screen. Correct, but the subtitle and the panel disagree.
· Fix: "It cannot connect: inside a container, localhost is that container, and nothing listens
there."

**A15 · S07 · polish** · "Then dash t with your token: 3 tasks in our stand-in, 21 for you, one
labeled, as gouda." (`script.md:641`)
· Evidence: `44:41` "Number of labeled tasks: 1" is ours; the viewer labeled "a few" (`:596`).
· Fix: "… 3 tasks in our stand-in, 21 for you; ours has one labeled, as gouda."

**A16 · S08 · polish** · "An extra echo prints the class bucket name" (`script.md:677`)
· Evidence: `54:38` is `cheese-app-data-demo`, the README's part-1 bucket; the conventions reserve
"the class bucket" for `cheese-app-data-versioning` (`script.md:217–219`), and S12/S15 use it that
way.
· Fix: "An extra echo prints the README's bucket name".

**A17 · S08 · polish** · SHOW "`docker system prune` → TERM(laptop/62: …), lines 10 and 13
(`data-labeling-network`) YELLOW" (`script.md:682–683`)
· Evidence: `62:10` is the deleted container's id; only `62:13` is the network.
· Fix: "line 13 (`data-labeling-network`) YELLOW; line 10 (the stopped container) GREY".

**A18 · S13 · polish** · "the cache on your disk where hashing happens" (`script.md:964`; V6 label
`:962`)
· Evidence: `dvc add` computes the md5s while reading the workspace (through the mount); the cache
is where it then stores the copies (digest §3.5).
· Fix: "the cache on your disk, filled by dvc add" (label "your disk · copies made by dvc add").

**A19 · S01, S13 · polish** · GOLD tags "storage: a few MB, cents" (`script.md:291`) and "a second
copy of the photos now bills · cents" / SAY "still cents" (`:960–964`).
· Evidence: digest §2: the whole lecture's storage is "a fraction of a cent per month"; S03
already says so (`:400–402`).
· Fix: "a fraction of a cent a month" in all three places.

**A20 · S02 · polish** · "Part 2 is the versioning station: one DVC container, a second bucket"
(`script.md:316`)
· Evidence: the README only asks for "your bucket" with two folders (`data-versioning/README.md:178–184`),
and S10's own chip says "a new bucket, or part 1's" (`script.md:774`).
· Fix: "… one DVC container, a bucket with two folders, your own GitHub repo …" (or drop S10's "or
part 1's" chip if two buckets is a brief decision).

**A21 · S02 · polish** · SHOW "the two trees matching row for row" (`script.md:348`)
· Evidence: `05:2–6` adds `.`, a blank line and `3 directories, 0 files`; README:37–40 has two rows.
· Fix: "matching folder for folder".

### Writer-facing notes (no change required)

- `dvc push` in `95:74` / `104:67` fails with `unexpected error - b/your-bucket-placeholder/o`, not
  an explicit credentials message; "fails without credentials" (`script.md:957`) is the correct
  diagnosis (cf. `93:89–106`), so keep it.
- S12's "so git refuses" (`:872`): the refusal text is libgit2's (DVC's git library) applying
  git's ownership rule; "git" is an acceptable simplification.
- S14's "gcsfuse caches listings" chip is digest §6 #18's claim; the TTLs are unverified (digest
  §10), so keep the wording vague, as it is.

---

**Verdict: 4 wrong · 4 misleading · 13 polish. No capture line, code line, README line or number
citation is wrong. Fit for scenes after A1–A4 are applied (A1 also needs the BRIEF placement
noted), preferably with A5–A8; the fixes are roughly word-neutral (A2 +25 words, A7 +5, A6 +12;
A9/A11/A14 are shorter).**
