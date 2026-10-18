# Review record: AC215 · Lecture 2 — Containers I: one image, from laptop to VM

Produced 2026-10-13 to 2026-10-18 by Claude Code cloud sessions for Conny, on the AC215 batch draft
PR Explainer_Videos#29 (branch `claude/mlops-learning-videos-7b5use`). The final cut was stitched on
2026-10-17 (19:42–20:42 UTC) from the 1080p60 scene renders of 16:01–17:15 UTC. The episode's scenes
and `script.md` are unchanged since `5215879`, its `i18n/` and the subtitle toolkit since `0c4d0e9`
(19:38 UTC, before the stitch); later commits up to `e018fb0` touch neither this folder nor any
word L02 says. Verified facts and unclaimed reviews are kept separate.

Times are mm:ss in the full video (`output/ac215-l02-containers-1.zh-en.mp4`, 31:17.7) unless
marked "draft". The evidence for the final-cut checks is in `build/final-review/` (git-ignored,
on the producing machine): `measured.json`, `asr_summary.json`, `tags_summary.json`,
`visual_notes.txt`, `bilingual_pairs_findings.json`, plus the frames, crops and contact sheets
named below.

## Content gates (AGENTS.md)

1. **Hook**: a puzzle, not a pitch. At 00:00 a fresh VM with no code, no venv and no uv runs the app
   with one Docker command (seven layers pulled, *I love cheese* comes back in Italian). At
   00:26.9–00:36.1 the broken thing: the container's Python is 3.14.7, "yet the recipe for this image
   starts from Python 3.12. Hold that thought; we'll solve it twice today." It is solved at 11:01.5
   (our build: uv downloads the newest Python in `>=3.13`, 3.15.0 at the time of recording) and at
   27:57.0–28:21.4 (the instructor's image: built a month earlier with uv 0.12.15, so 3.14.7). ✔
2. **Intuition before formalism; an animated mechanism per core idea**. S02 builds the four nouns as
   pictures before any command is typed (01:22.7–03:16.9), and each later picture predicts output that
   a real capture then confirms:
   - image = read-only layer slabs + a config card (V2): 01:39.8, grown one Dockerfile step at a
     time in S04–S08 (05:09.9–14:34.4), rescaled to `docker history` sizes in S10;
   - container = the same slabs + a thin writable glass slab + one process; `--rm` dissolves it:
     02:09.3, and in S09 `exit` puts out PID 1 and `--rm` removes the container (15:11.5);
   - container ≠ VM, one shared kernel, Docker Desktop's hidden VM (V8): 02:43.2–03:05.9; on the
     cloud VM `dockerd` on the VM's own kernel: 27:05.6;
   - the build context as a parcel sent to the builder, with no `.dockerignore` sieve (V5 seed):
     08:30.2;
   - two Pythons in one image: number line, the `>=3.13` interval, uv's 3.15.0 dot, PATH doors (V4):
     10:39.0–11:34.3, doors at 12:55.3, the 3.14.7 coda at 28:11.4;
   - the start-up command line ENTRYPOINT + CMD (V3): 07:22.4, joined at 12:41.5, the `python cli.py`
     tile knocking CMD out and exit 126 at 16:10.6–16:24.8;
   - the layer cache as a chain with fingerprint badges and a domino wave (V5): the rule at 18:59.4,
     the changed checksum at 19:41.0, the reordered Dockerfile at 20:35.9;
   - names and the registry: two names, one ID; the push route; "already exists" (V6): 21:42.5,
     22:25.8;
   - platforms as a menu per tag, and `exec format error` (V7): 23:28.0, 24:28.8;
   - the whole route laptop → Docker Hub → VM and L1's VM-with-a-venv gaining a container (V1):
     30:07.5. ✔
3. **Ponder moments and recap**:
   - Five ponder cards with silent timers: 09:26.05 (6 s), 10:18.07, 16:02.03, 19:25.25 and 24:16.20
     (8 s each). Five is what `BRIEF.md` sets. AGENTS.md aims for one per 2 minutes, which would be
     about 16 here; this cut has 0.32 per 2 minutes, and the longest stretch without one is the
     first 9.43 minutes (00:00–09:26). Besides the ponders, the narration stops the viewer 28 times to
     run or do something ("Pause and …", "Pause now"); those are hands-on checkpoints, not ponders. ⚠
   - Recap: S16 (29:31.8, 105.9 s) summarises L1 against today (30:07.5–30:23.0), asks five
     test-yourself questions (30:23.6–31:00.5) and says what's next (31:00.8–31:15.9). Part 1 ends at
     16:49.2 with a one-line recap and a preview of part 2. ✔
4. **Written for the ear; anchored cues**: commands and paths are said in words ("dash dash rm",
   "slash dot venv"), versions have lexicon entries, changing numbers carry "at the time of
   recording"; 65 sentences show the literal form in the subtitles instead of the spoken one. There
   are 728 anchor call sites (708 `vo.wait_until`, 20 through S16's `cue()` helper; 747 anchor waits
   run with loops expanded), and the 16 final render logs have no "voiceover anchor not found". ✔
5. **Simulated-viewer QA over the full draft**: seven watchers over the whole 480p draft, per-scene
   fixers and skeptical verifiers, two finishing passes, then four checks of the final cut; findings,
   fixes and what stayed open are below. ✔
6. **Measured checks**: see *Verified (final render)*. Decode, durations, loudness, subtitle bounds and
   chapters pass; this episode has no music bed (`video.yaml` has no `music` key; the mix is narration
   only), so there is no music-balance figure. Nit: true peak is −1.0 to −1.3 dBFS against the stitcher's −1.5 dBTP target. ✔
   - Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.

## Whole-video QA (480p draft, 30:20, 2026-10-16) and the finishing passes (2026-10-17)

**Watchers (7):** a director and a newcomer for each part (part 1 = S01–S09, part 2 = S10–S16), a
Chinese/bilingual subtitle watcher, a follow-ups watcher for `QA_FOLLOWUPS.md` and an ASR watcher.
They read contact sheets with `script.md` and the `.srt` beside them and pulled exact frames for
anything unclear.

**Issues: 73, of which 0 must, 29 should and 44 nit.** By watcher (should / nit): director part 1
8 / 6, newcomer part 1 5 / 8, director part 2 5 / 10, newcomer part 2 4 / 6, subtitles 6 / 8,
ASR 1 / 6. The follow-ups watcher filed none: the S12 `path` restore and the S10 card snap-back from
`QA_FOLLOWUPS.md` were already fixed, and a snap-back detector run over all 16 scenes found 0 cases.
Apart from the two wrong labels below, every number, version, layer count and README line number
checked against the captures held.

**Musts:** none were filed, so none needed a fix.

**Shoulds (29): 27 fixed, 1 partly, 1 open.** Fixed in the scene, the narration or the subtitle
text, each checked by a verifier on freshly rendered frames:
- Wrong on screen: the solution image's second slab read `RUN pip install uv` in S09/S10; it is the
  apt + pip + uv `RUN`, now labelled `RUN apt…uv`. S13's buildx menu was titled
  `dlops/simple-translate` with two platforms, right after the video showed that image is amd64
  only; it is now `<USER NAME>/simple-translate-ac215`, and its erratum note holds about 3.5 s.
- The English `.srt` showed spoken spellings ("dash dash rm", "user local bin"), filed three times
  (the subtitle watcher noted it too):
  the toolkit now writes the English track from the literal display text. In the final `.srt` only
  the plain-prose "And the slash means you start" spells anything.
- Follow-along: S01's tracker preview drew chips no other scene uses (now the real trackers A/B/C);
  S03's Windows advice (now "an Ubuntu terminal in WSL, or Git Bash … put winpty in front of docker
  run", 03:26.2–03:36.8, and the on-screen note matches); "▶ your turn" on the wrong row in S06 and
  S07; S10 never said "type exit" (now 18:31.3); S04's inspect command and S13's `uname -m` fold broke
  mid-token or mid-command (now folded at spaces, one command per row).
- Pacing: three S03 items left the screen within about 1 s (the "every unused image" caption, the
  clone commands, the `uv.lock` ghost; now about 3 s or more); S07's `uv sync` payoff landed after the
  narration (now a 2.0 s hold); S13's two notes on "our push" were up for 1.5–2.5 s (now held, and
  the overlay is narrated: "Built on an M-series Mac, the amd64 row would say arm64",
  23:57.7).
- Continuity: S04 drew the stack and config card differently from S05–S09 (now S05's).
- Picture: S10 swapped S04's compressed base-image sizes for the unpacked ones with nothing linking
  them; S04's list now turns into the labelled note "≈ 47.6 MB compressed download / → unpacked on
  disk" (about 17:44; that it is not narrated is a nit, under Open items).
- Narration: "that one build step" was heard as "that when build step" (now "added or changed by one
  build step", 01:42.8); S07's "the same two extras" pointed at S06's `ls` (now "then two extras" with
  `ls -a`, 11:13.6).
- Subtitles: four zh line breaks (S07, S08, S09, S11) and S09's puzzle command, rewritten in
  `i18n/zh/narration/g1.yaml` / `g2.yaml`.

Partly: the S16 cost meter rewound to 12 o'clock. S16 now starts its needle where S15 would have
left it, so it never rewinds; carrying S14's badge through S15 was skipped (see Open items). Open:
`.zh.srt` splits the deploy command after `run` (see Open items).

**Nits (44):** most were fixed in the same passes, among them S02's unnarrated GPU chip (now "GPU
drivers still come from the host.", 03:13.0), the docker-shell.sh run command (now said and typed,
16:46.3), "pulls" heard as "polls" (now "pulling", 29:16.5), the narration's `docker ps -a` without
`sudo` (now "sudo docker ps dash a"), "venv's" heard as "vems" (two sentences reworded), and lexicon
entries for "rerun", "image's" and "dlops". The narration/subtitle fixer reported 20 of its items
applied, 2 partly and 5 left on purpose (all nits); the ones still open are listed below.

**Finishing passes (2026-10-17):** a plan of 17 text items, 32 scene items across 14 scenes and 21
skipped items (each with its reason), then per-scene agents with a verifier each. They added the
lecture-slide citations from `SLIDES.md`'s "do" list: 18 grey `Lecture 2 · slide(s) …` tags in 12
scenes, two short bridges (the lecture's `--entrypoint` run command, 13:31.1; the PID namespace,
15:30.0), the "namespaces" / "cgroups" chips on S02's kernel bar and its "user space" label beside
the containers, the slide-57 note at the S08 diff, S11's "one numbered step per instruction" caption,
and the "user space · Debian" / "Linux kernel" bars in the S14 and S15 VM pictures. No slide image is
shown anywhere.

## Final-cut checks (2026-10-18)

Four independent checks of the stitched 1080p60 cut, after the measurements:

- **Visual** (all 40 contact sheets of `zh-en.mp4`, one frame every 3 s, plus exact frames): one real,
  minor defect, in S06 (open, below). Everything else is a mid-animation frame that settles within
  about 1.5 s, or deliberate layout (notes on a terminal's top border at about 13:42–13:45,
  21:12–21:18, 21:48 and 22:21 cover only the border).
- **Lecture tags**: 19 appearances of the 18 tags (17 `lecture_ref` calls; S02's helper makes two
  tags, S12's tag shows twice). Nothing overlaps any tag and no tag is visible after its scene. 16
  span the picture they cite; three do not (open, below).
- **ASR round trip**: no real mispronunciation, swallowed word or late cue (details under Verified).
- **Bilingual pairs**: all 546 cues read; in each, the Chinese says what the English under it says.
  One command is split across two cues (open, below).

## Open items in this cut (left as is, with the reason)

| time | scene | item | why it was left |
| --- | --- | --- | --- |
| 08:55.1, 09:00.0 | S06 | When the narration points at a tag, `Indicate(…, color=…)` recolours the whole tag, fill included: during the 0.6 s pulse on "no .dockerignore" (08:54.8–08:55.4) the tag fills near-solid white, and during the 0.7 s pulse on "the parcel" (08:59.6–09:00.3) near-solid pink; the label is barely readable for about 0.2 s around each peak (`s06_copy.py:414`, `:423`; `frames/crop_tagflood_0533.2_0535.13.png`, `frames/crop_parcel_0540.png` vs `_0541.png`, `verify/s06/noign_fine.png`). No other scene highlights a whole tag. | Found in the final-cut check; fixing it means a scene edit and a re-render, which is the coordinator's call. |
| 18:52.3–19:00.0 | S11 | Tag "slides 36, 58–60" leaves at "For COPY" while the four-step chain stays; slide 60's all-CACHED rebuild then plays at about 19:08–19:18 with no tag. | Planned this way (the scene docstring: the lecture leaves out what invalidates a step); review-bot thread 4299714089's general point still applies here. |
| 25:32.4–25:39.9 | S14 | Tag "slide 77" leaves at "The README gives no settings" while the create-VM console stays until 25:56.3. From 25:34.9 to 25:36.9 (the console fades in at 25:36.9) the frame holds only the tracker and the tag, and the tracker's section-name pulse briefly covers the tracker's "›" separator (25:34.8–25:35.6). | Planned span; the pulse is the shared tracker pattern. Same review-bot thread. |
| 02:43.8–03:16.7 | S02 | Tag "slides 9–12, 22–24" stays about 10 s after its VM/kernel picture leaves (about 03:05.9), over beat 8's image stack, which `SLIDES.md` ties to slides 5–7, 10 and 22. | `script.md` asks for it "to the end of the scene"; it leaves with the final fade. |
| 27:27.4–29:31.8 | S15 | No cost dial during S15 while the VM still bills; S16's needle resumes ahead of S14's, so it never rewinds. | The badge's corner is used in at least five S15 beats: a redesign, not a fix. Raise on the issue if wanted. |
| 27:27.4 | S15 | `.zh.srt` splits the deploy command after `run`: `然后是部署：sudo docker run` / `--rm -ti dlops/simple-translate`. The bilingual track keeps it whole (cue 483). | Toolkit (`explainer/subtitles.py` `_cut_penalty`), a separate PR; a yaml rewrite breaks the bilingual English line. |
| 21:31.98, 21:36.47 | S12 | Bilingual cues 380/381 split `docker tag simple-translate <USER NAME>/simple-translate-ac215` in two; each pair matches and the placeholder stays whole. | A zh rewording keeps the command in one cue but splits the Chinese awkwardly; left for the coordinator. |
| 10:28.2 | S07 | "the pip step says CACHED, but COPY says DONE" describes the plain log, not the compact view. | The screen shows and highlights the plain log's `#7 DONE`, so voice and screen agree. |
| 12:03.7 | S07 | The narration doesn't say why the prompt reads `(app)`. | A GREY tag shows `pyproject.toml · line 2: name = "app"`, and the subtitles show `(app)`. |
| about 17:44 | S10 | S04's compressed download sizes are not narrated. | They now turn into the labelled note "≈ 47.6 MB compressed download / → unpacked on disk". |
| about 19:52 | S11 | The rebuild's `Downloading cpython-3.15.0-linux-x86_64-gnu` line has no Apple Silicon note (S10 has one). | Not carried into the finishing plan (nit). |
| 20:19.1–20:22.4 | S11 | The tag reads "erratum · expected while learning" while the voice says "that's expected". | Recorded decision: `BRIEF.md` erratum 7 and `script.md`'s S11 SHOW. |
| 26:14.6 | S14 | The narration's "skip ahead to the version check" gives no "answer Y". | The on-screen note says "it asks [Y/n]? answer Y / → skip to step 4: Docker version". |
| about 30:04–30:07 | S16 | `docker buildx rm multi-arch` and `docker logout` are on screen, not said. | Optional; the chips are readable for about 3.3 s. |
| about 04:45 | S03 | The simple-translate chip's flight crosses the clone URL row for about 0.3 s. | No clean route inside the frame. |
| several | all | English cue switches inside one sentence are timed by written length, so a cue can change up to about 1 s off its words. | Toolkit (`subtitles.tracks`), a separate PR. The final onset check found no cue whose audio starts more than 1 s after the cue. |
| whole cut | all | True peak −1.2 dBFS (both full cuts), −1.3 (part 1), −1.0 (part 2), above the −1.5 dBTP the stitcher's `loudnorm` asks for, by up to 0.5 dB; integrated loudness is on target. | Measured only; no clipping. A re-stitch decision for the coordinator. |
| — | docs | `script.md` (line 146) still states 4,294 words (2,348 / 1,946); the measured count is 4,398 (2,428 / 1,970). | Documentation drift only; the render is right. |

Minor timing nits the verifiers saw and left: S11's `--progress=plain` underline starts about 0.5 s
after its words (about 19:10.9); at the peak of S13's post-block pulse the gap in "built on a Mac:
linux/arm64" nearly closes for about 0.6 s (about 24:03.6); S15's pull ride starts about 0.3 s after
"from Docker Hub".

## Verified (final render)

- **Encode and decode.** All four files are H.264 High, 1920×1080, 60 fps, yuv420p, with AAC-LC
  48 kHz stereo at about 117 kb/s. A full `ffmpeg -v error … -f null -` decode of each exited 0 with
  no error lines.

  | file | duration | video frames | size | loudness | true peak | LRA |
  | --- | --- | --- | --- | --- | --- | --- |
  | `ac215-l02-containers-1.zh-en.mp4` (Bilibili) | 1877.715 s (31:17.7) | 112,662 | 88.96 MB | −16.0 LUFS | −1.2 dBFS | 2.1 LU |
  | `ac215-l02-containers-1.mp4` | 1877.715 s | 112,661 | 89.95 MB | −16.0 LUFS | −1.2 dBFS | 2.1 LU |
  | `ac215-l02-containers-1_part1.mp4` | 1018.004 s (16:58.0) | 61,077 | 46.69 MB | −16.0 LUFS | −1.3 dBFS | 2.1 LU |
  | `ac215-l02-containers-1_part2.mp4` | 859.813 s (14:19.8) | 51,584 | 43.26 MB | −16.0 LUFS | −1.0 dBFS | 2.2 LU |
- **Lengths and chapters.** The 16 scene renders sum to 1877.683 s. Part 1 + part 2 = 1877.817 s,
  +0.102 s against the full cut (video streams alone: 0.000 s). `chapters.txt` has 16 entries whose
  titles, order and start times match `video.yaml` and the stitched scene lengths;
  `chapters_part1.txt` (9) and `chapters_part2.txt` (7) match too. All 16 chapter starts show their
  scene; no black or missing scene; all 16 scene-end frames are empty (compression noise at most 3
  of 255 levels).
- **Subtitles.** `.srt` 502 cues, `.zh.srt` 460, `.zh-en.srt` 546: numbered in order, no overlaps, no
  cue under 1.000 s, at most two lines, all between 0.000 s and 1875.939 s (1.78 s before the end).
  The part files (285 / 255 / 302 and 217 / 205 / 244 cues) pass the same checks. Every bilingual cue
  is one Chinese line over one English line; 539 have Chinese characters in the Chinese line. The
  other 7: #57 (03:18.5) and #366 (20:44.3) carry the README section heading, with the Chinese
  lead-in 现在进入 README 的这一节 in the cue before; #99, #263, #288, #429, #483 are commands or
  `exec format error`. In `.zh.srt`, cue #244 (15:55) is a command. Three pairs (56/57, 230/231,
  365/366) show the whole English sentence under both Chinese halves: the tool's fallback when it
  finds no matching cut, not a swap. The winpty case reads in order (cues 61–62, 03:30.6 and 03:34.1).
- **Burned subtitles** (`zh-en.mp4`). The picture is scaled to 87 % at the top and the subtitles sit
  in the band below, so they never cover the picture. Every subtitle frame shows exactly two lines,
  Chinese above English; the widest line is 1096 px (x 411–1507). Spot-checks at 3:51, 4:09, 4:51,
  6:03, 7:51, 9:36, 10:30, 14:48, 26:09 and 27:36 show every terminal command clear of the subtitles
  (`subs_spotcheck_mosaic.png`). In the clean cut nothing reaches below y = 1040 or touches the frame
  edges.
- **Motion.** 21 still stretches of 4.0–8.4 s (freeze detection on a 480 px copy); the scene timings
  show narration and small animations in all but two, which are the ponder cards at 16:06–16:10 and
  24:18–24:22. The longest, 8.4 s at 10:07.9–10:16.3, is narrated over the "Now predict" chips.
- **ASR round trip** (substitute for a listen). `asr_video.py` with base.en on the clean cut against
  its `.srt`: 502 cues, 4,538 words recognised, 225 cues differing. Every differing cue was re-run with
  large-v3-turbo in 91 windows that include the neighbouring cues: 17 match exactly; the other 74
  differ only by ASR noise (Dockerfile → "docker file", sudo → "pseudo", digits vs words), by the 65
  intended spoken-vs-subtitle forms, or by edge bleed. base.en drop-outs at 06:49, 19:12,
  22:19–22:30, 24:24 and 28:11 were heard in full by turbo. Real problems: none. Minor notes, no fix
  needed: "stdin" heard as "Estedin" (03:34, cue 59), the "d" of "failed" / "moved" elided before
  "to" (05:00, 14:05), "Python's CLI.py" for "python cli.py" (cues 190, 192, 200, 449, 494), and
  one-syllable "venv". No cue's audio starts more than 1 s after its cue (largest gap 0.53 s, cue
  252, 14:51). The five longest silences (6.95–9.58 s) start at 09:25.78, 10:17.78, 16:01.13,
  19:24.92 and 24:15.87: the five ponder timers; the other silences over 3 s are 3.36–5.07 s.
- **Narration.** 129 SAY lines in `script.md` = 129 voice blocks rendered; 4,398 words (part 1 2,428,
  part 2 1,970); 140.5 words per minute over the runtime, 149.8 over the 1762.1 s of voice (93.8 % of
  the runtime). Kokoro `af_heart`, speed 0.9.
- **Lecture tags** (`tags_summary.json`, `tags/<id>/`): in and out times from each scene's code and
  `events.json`, offsets checked against the cut to within one frame. All are grey; singular and
  plural are right ("slide 57", "slide 77", "slide 73"); six sit off the standard top-right spot on
  purpose (S02 ×2, S05, S10, S14's second, S16's Next tag, which also clears the burned subtitles).
- **Review-bot threads on PR #29:**
  - 4293689313, verified: the S15 tag reads exactly "Intel/AMD laptop: already amd64 · Apple Silicon
    Mac: rebuild first (see Platforms)", in at 28:56.48, out at 28:59.68–29:00.08
    (`bot/s15_amd_full*.png`).
  - 4293689328, verified: in S15 beat 5 the `uv = 0.12.15` row keeps its YELLOW underline and the
    "where uv 0.12.15 came from" tag from 29:03.53 through 29:16.37 (`bot/s15_b5_uv_montage.png`).
  - 4293935086, verified: the narration text says "An extra check, sudo docker ps dash a, …"; the
    subtitles show `sudo docker ps -a` (`.srt` cue 478 at 29:33.746, `.zh-en.srt` 518, `.zh.srt` 440);
    the screen types it (`bot/s16_psa_full1776.50.png`). In audio, large-v3-turbo heard "An extra
    check, sudo docker ps-a, shows no containers left behind" in the 29:31.5–29:49.8 window (base.en:
    "pseudo-docker-ps-a"): machine evidence, not a listen.
  - 4299714089, partly verified: the three tags it names now hold (S02's "slides 30–31, 35" runs
    through the class/instance beat to 02:27.9; S02's "slides 9–12, 22–24" and S03's tag run to the end
    of their scenes, as `script.md` asks). Its general point, tags leaving before the picture they cite,
    still applies to S11's tag and S14's slide-77 tag; and S02's second tag now outlasts its VM picture
    by about 10 s. 16 of the 19 tag spans match their picture (Open items).
- **Provenance** (`ASSETS.md`). Every terminal line is a real capture of 2026-10-13: a fresh Docker
  Engine 29.8.2 on linux/amd64 standing in for the laptop, fresh `debian:12` / `debian:13` containers
  standing in for the VM. From step 3 on, the laptop builds ran on the real `python:3.12-slim-bookworm`
  rebuilt with the recording proxy's CA (`ASSETS.md`, "Capture-only base image"); the scenes crop the
  rows where that shows (its digest, three history rows, an extra `image ls` row). Code panels quote
  `dlops-io/simple-translate` at `62f821b` unchanged. The
  push without an account (`push access denied`) and Docker Hub's `toomanyrequests` are real
  captures; the successful login and pushes went to a local registry and are tagged
  `stand-in · local registry, not Docker Hub` / `watch only · don't type`; the cloud console, Docker
  Hub pages and the editor are schematic drawings tagged `illustration`. Slide citations are numbers
  only, from `SLIDES.md`.
- **No tracked media.** The MP4s are git-ignored (`videos/*/output/**/*.mp4`); subtitles, chapters
  and the transcript are tracked.

## Not claimed

- **No human listened to this cut** and no human watched it through; the listen is waived for the
  series (gate 6). The ASR round trip shows the words are recognisable; it says nothing about voice
  quality, pacing preference or how the video feels.
- **The Chinese and bilingual subtitles were reviewed by agents only** (the draft's subtitle watcher
  and the final pair check, plus `python -m explainer.i18n check`); no native speaker reviewed them.
- **The visual review is sampled**: one frame every 3 s plus targeted frames. Moments between
  samples were not all seen.
- **What the captures could not run**, so the video describes or draws it: creating, SSH-ing into and
  deleting a Compute Engine VM, and its billing (a Debian container stood in, with no systemd and
  empty package lists); a Docker Hub account, the access token, `docker login`, a successful push to
  Docker Hub and the public repository; `Mounted from library/python` on push; Docker Desktop itself
  on a Mac or Windows (the `desktop-linux` builder, the hidden VM, `aarch64` downloads); an Apple
  Silicon image failing on an amd64 VM (only the reverse case, `laptop-push/12`, was captured);
  `docker-build-push.sh`'s multi-platform push; the Windows advice (WSL, Git Bash, winpty).
- Versions, sizes and the CPython uv picks are as of 2026-10-13 and are said "at the time of
  recording"; a later viewer's numbers will differ.
- The slide numbers in the tags come from `SLIDES.md`, a digest of the instructor's PDF (not in this
  repository); they were not re-checked against the PDF in this review.
- The numbers above measure this local stitch. The release workflow re-renders and re-measures
  (`<id>.validation.json`); small differences there are possible.
