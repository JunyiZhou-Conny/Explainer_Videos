# Review record: AC215 · Lecture 2 — Containers I: one image, from laptop to VM

Produced 2026-10-13 to 2026-10-18 by Claude Code cloud sessions for Conny, on the AC215 batch draft
PR Explainer_Videos#29 (branch `claude/mlops-learning-videos-7b5use`). The final cut was first
stitched on 2026-10-17 (19:42–20:42 UTC) from the 1080p60 scene renders of 16:01–17:15 UTC and
checked (*Final-cut checks*). A fix round then changed four scenes (S02, S06, S11, S14), re-rendered
them at 1080p60 on 2026-10-18 (04:09–04:39 UTC) and re-stitched the cut on 2026-10-18 from those
four renders and the twelve unchanged stitched segments of 2026-10-17. That stitch run (the
re-stitch) wrote the deliverables at 05:20–06:09 UTC; it reused the four new scene segments that an
earlier run of the same stitch (started 04:44 UTC) had normalized at 04:46–04:52 UTC, and it was
rechecked (*Fix round and recheck*). Two stitcher commits then changed the final audio encode, and
the same stitch (`--no-render --crf 27 --burn`) wrote the deliverables again at 09:34–10:22 UTC from
the same sixteen scene segments; only the final audio encode differs. This final stitch is the cut
this record describes and measures. Its frames were not checked again: the frames cited here are of
the re-stitch (the four changed scenes), which used the same sixteen scene segments, or of the
2026-10-17 stitch (the whole cut); the ASR round trip ran on the 2026-10-17 stitch, with the same
narration. The fix round's commits are:
- the four scene files and their SHOW lines in `script.md`: `661cc16`, `e4ab95c`, `85fb162` and
  `8a61f62`. No SAY line changed.
- one Chinese sentence in `i18n/zh/narration/g2.yaml`: `8a61f62`.
- a sample-peak limiter after `loudnorm` in the stitcher (`explainer/build.py`): `5a02ba1`.
- the stitcher's final audio encode (`explainer/build.py`): no AAC noise substitution, `8a092e4`;
  the limit lowered from 0.79 to 0.71 and AAC at 192k instead of 128k, `5833542`.
- the regenerated subtitles: `48068d7` for the full cut and `bdfead6` for part 2.

Apart from these, the scenes and `script.md` are unchanged since `5215879`, and `i18n/` and the
subtitle toolkit since `0c4d0e9`. The toolkit's only other change since then is two
`explainer/lexicon.yaml` entries for "port toy" (`e018fb0`), a phrase L02 never says. Later commits
up to `855cbd7` touch neither this folder nor `explainer/`; from there to `86fb60c`, this folder
changed only in `REVIEW.md` and `QA_FOLLOWUPS.md` (`bf99362`, `7312ec1`) and `explainer/` only in
`8a092e4` and `5833542`. Verified facts and unclaimed reviews are kept separate.

Times are mm:ss in the full video (`output/ac215-l02-containers-1.zh-en.mp4`, 31:17.7) unless
marked "draft". The evidence for the final-cut checks is in `build/final-review/` (git-ignored,
on the producing machine): `measured.json`, `asr_summary.json`, `tags_summary.json`,
`visual_notes.txt`, `bilingual_pairs_findings.json`, plus the frames, crops and contact sheets
named below. The evidence for the recheck of the re-stitched cut is in `build/recheck/` (also
git-ignored, on the same machine):
- `measured.json`, `s12_tag_burned_extent.json`, `frames/` and `logs/`;
- `scenes/`: frames `f_MMmSS.sss.png` of the clean cut, with `_tr` top-right crops and `_zoom` 2×
  zooms, plus `tag_spans.json`, `scene_offsets.json`, `end_frames_luma.json`, `s06/pill_luma.json`,
  `s14/gap_fill.json`, `subs/` and `sheets/`;
- `review/`: two S02 frames taken for this record;
- `adv/`: an adversarial re-check of this record: its own `ebur128` / `loudnorm` / audio-MD5 logs
  and probes (`adv/logs/`), stitch-segment and render probes (`adv/segments.json`), subtitle checks
  (`adv/subs_check.json`) and frames of both cuts (`adv/frames/`).

The evidence for the re-measure of the final stitch is in `build/remeasure/` (also git-ignored, on
the same machine): `measured.json`, `subs_chapters.json`, the raw logs in `logs/`, and the scripts
that wrote them (`run.sh`, `subs_chapters.py`, `assemble.py`). An adversarial verifier's own
re-measure of it is in `build/remeasure/verify/` (`verify_summary.json`, `logs/` and its scripts).

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
   run with loops expanded). The 16 final render logs have no "voiceover anchor not found"; four of
   them, S02, S06, S11 and S14, are from the fix round's re-renders of 2026-10-18. The fix round
   added and removed no `vo.wait_until` call in those four files. ✔
5. **Simulated-viewer QA over the full draft**: seven watchers over the whole 480p draft, per-scene
   fixers and skeptical verifiers, two finishing passes, then four checks of the final cut. A fix
   round on four scenes followed, with a fixer and a verifier each, and then a recheck of the
   re-stitched cut. Findings, fixes and what stayed open are below. ✔
6. **Measured checks**: see *Verified (final render)*, measured on the final stitch (09:34–10:22
   UTC). Decode, durations, loudness, true peak, subtitle bounds and chapters pass. This episode has
   no music bed (`video.yaml` has no `music` key; the mix is narration only), so there is no
   music-balance figure. True peak is now −2.34 dBTP (both full cuts and part 1) and −2.81 dBTP
   (part 2), 0.84–1.31 dB under the stitcher's −1.5 dBTP target, at −16.07 to −16.10 LUFS. The
   limiter after `loudnorm` (`5a02ba1`) first met the target, at −1.53 / −1.63 on the re-stitch; the
   audio encode change (`8a092e4`, `5833542`) gave the margin. The 2026-10-17 stitch read −1.0 to
   −1.3. ✔
   - Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   - The ASR round trip was run on the previous stitch (2026-10-17), not on the re-stitch or the
     final stitch. The narration is the same: no SAY line changed, and the 129 voice blocks have the
     same per-scene durations (1762.133 s in all). The re-stitch changed only the four scenes listed
     and added the limiter; the final stitch changed only the final audio encode.

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

## Final-cut checks (2026-10-18, previous stitch)

Four independent checks of the first stitched 1080p60 cut (2026-10-17), after the measurements:

- **Visual** (all 40 contact sheets of `zh-en.mp4`, one frame every 3 s, plus exact frames): one real,
  minor defect, in S06 (fixed in the fix round, below). Everything else is a mid-animation frame
  that settles within about 1.5 s, or deliberate layout (notes on a terminal's top border at about
  13:42–13:45, 21:12–21:18, 21:48 and 22:21 cover only the border).
- **Lecture tags**: 19 appearances of the 18 tags (17 `lecture_ref` calls; S02's helper makes two
  tags, S12's tag shows twice). Nothing overlaps any tag and no tag is visible after its scene. 16
  span the picture they cite; three did not (fixed in the fix round, below).
- **ASR round trip**: no real mispronunciation, swallowed word or late cue (details under Verified).
- **Bilingual pairs**: all 546 cues read; in each, the Chinese says what the English under it says.
  One command was split across two cues (fixed in the fix round, below).

## Fix round and recheck of the re-stitched cut (2026-10-18)

Each changed scene had a fixer and a skeptical verifier working on 720p preview frames. Their
reports are kept outside this repository. The S06 and S14 verifiers each made one more change:
S06's pill outline now scales with its text, and S14's `ac215-l02` box fades in only in the last
30 % of the dial's move, from the left, so the dial no longer crosses it. The S02 and S11 verifiers
changed nothing. The four scenes were then re-rendered at 1080p60 and the cut re-stitched. Two
agents rechecked the re-stitched cut, and an adversarial verifier then re-measured the audio,
the probes and the subtitles and re-extracted frames for each fixed item below
(`build/recheck/adv/`); it did not re-run the full decode or re-read the sheets:
- **Scene recheck** (`build/recheck/scenes/`): frames of the clean cut at times taken from each
  scene's `events.json` plus the scene's start. For the four scenes, contact sheets of
  `zh-en.mp4` at one frame every 2 s, with the time burned in; all 16 sheets were read.
- **Measurement recheck** (`build/recheck/measured.json`).
- **Re-measure of the final stitch** after the audio encode change (`build/remeasure/`): see
  *Audio encode* below the table.

Every item below is fixed on the re-stitched cut. Frame paths are under `build/recheck/`.

| time | scene | what changed, as measured on the re-stitched cut | evidence |
| --- | --- | --- | --- |
| 08:54.8–08:55.4, 08:59.6–09:00.3 | S06 | The two `Indicate` pulses no longer flood the tags with colour (`s06_copy.py` lines 414 and 424). Only the text pulses, and the pill outline scales with it. The "no .dockerignore" pulse runs 08:54.833–08:55.433 (peak 08:55.133): its text turns white. "The parcel" pulse runs 08:59.633–09:00.333 (peak 08:59.983) and stays pink. The fill stays dark: mean brightness inside the pill is 55.6 at the peak against 34.1 before (the rise is the white text), and 33.5 against 31.9 for the parcel. A flooded pill would read near 200. The grown pills stay clear of "▶ your turn". | `scenes/s06/f_08m54.700` … `f_08m55.550` and `f_08m59.550` … `f_09m00.450`, each with `_zoom`; `scenes/s06/pill_luma.json` |
| 18:59.4–19:18.9 | S11 | The all-CACHED rebuild now has a tag. A new GREY `Lecture 2 · slide 60` (standard top right) fades in with the rebuild terminal at 19:08.800–19:09.150. It leaves as the terminal shrinks to the strip, at 19:18.150–19:18.850, just after "Now predict" (19:17.900). It sits about 45 px above the step badges and overlaps nothing. `slides 36, 58–60` still leaves at "For COPY" (18:59.433–19:00.033), as planned: the COPY checksum rule that follows is not in the lecture. `SLIDES.md` gives slide 60 as the all-cached rebuild. | `scenes/s11/f_18m59.300`, `f_18m59.750`, `f_19m00.150`, `f_19m08.600`, `f_19m08.980`, `f_19m09.300`, `f_19m13.000` (and `_tr`), `f_19m17.850`, `f_19m18.500`, `f_19m18.950` |
| 25:32.4–25:57.3 | S14 | **Slide-77 tag:** it now stays until the create-VM console becomes the SSH terminal. It comes in at 25:32.417 and is still on at 25:39.3 and 25:40.0 (the old exit was at ≈25:39.4). It is fully on at 25:56.40, faint at 25:56.60 and gone at 25:56.80. **Near-empty frame:** closed. The console now fades in during the section-name pulse, 25:34.850–25:35.650. The frame holds only the tracker and the tag for about 0.5 s (≈25:34.6–25:35.2), while the title lands in the tracker; the old gap was 25:34.9–25:36.9. **Badge:** the `ac215-l02` box appears from about 25:57.03, left of the cost dial, and the dial never crosses it (checked 25:56.95–25:57.30). | `scenes/s14/f_25m39.300`, `f_25m40.000`, `f_25m56.400`, `f_25m56.600_tr`, `f_25m56.800_tr`; `f_25m34.000` to `f_25m35.900` and `scenes/s14/gap_fill.json`; `f_25m56.950_tr`, `f_25m56.990` to `f_25m57.300` (each with `_zoom`) |
| 03:05.9–03:16.7 | S02 | Tag `slides 9–12, 22–24` now fades out with its VM/kernel picture, 03:05.917–03:06.517. A new `Lecture 2 · slides 5–7, 10, 22` fades in with beat 8's image stack at 03:06.517–03:07.517, in the old tag's spot under "registry". It leaves with the final fade, 03:15.900–03:16.700. `SLIDES.md` ties beat 8 to slides 5–7, 10 and 22. The two tags never show together and the new one overlaps nothing. `script.md`'s S02 SHOW lines now give these spans. | `scenes/s02/f_03m05.700`, `f_03m06.200`, `f_03m06.530`, `f_03m07.000`, `f_03m07.600`, `f_03m13.500`, `f_03m15.800` (and `_tr`), `f_03m16.300` |
| 21:31.98–21:39.81 | S12 | The bilingual English line now holds `docker tag simple-translate <USER NAME>/simple-translate-ac215` whole: the zh in `i18n/zh/narration/g2.yaml` was reworded. In `.zh-en.srt`, cue 380 (21:31.983–21:34.500) reads 然后给 image 打 tag：在 docker tag 后面先写 / "Then tag the image:". Cue 381 (21:34.500–21:39.812) reads simple-translate 再写你的用户名/simple-translate-ac215 over the whole command, and the `.ass` matches. In `.zh.srt`, cues 319/320 run 21:31.983–21:33.483 (1.500 s) and 21:33.483–21:39.812. The English `.srt` (cue 355) was already whole and is unchanged. Part 2 has the same wording: `.zh-en.srt` cues 78/79, `.ass` lines 92/93 and `.zh.srt` cues 64/65, all at 04:34.033–04:41.862. Every part-2 cue (217 / 205 / 244 / 244) equals the full cut's minus 1017.950 s, in both text and timing; in the `.ass`, which rounds to the centisecond, two end times differ by 0.01 s (the cues starting 18:31.28 and 22:23.54). The burned copy shows two lines here: 897 px of Chinese and 706 px of English. | `scenes/subs/zhen_1293.20.png`, `scenes/subs/zhen_1297.50.png`, `frames/zh-en_t1293.0.png`, `frames/zh-en_t1297.0.png`, `s12_tag_burned_extent.json`, `scenes/subs/part2_vs_full.json`; commits `48068d7` and `bdfead6` |
| whole cut | all | True peak is −2.34 dBTP (full cut, Bilibili copy, part 1) and −2.81 (part 2) on the final stitch, after the audio encode change below. The limiter (`5a02ba1`) first met the stitcher's −1.5 dBTP target on the re-stitch, at −1.53 and −1.63; the 2026-10-17 stitch read −1.0 to −1.3. Integrated loudness is −16.07 to −16.10 LUFS. | `build/remeasure/measured.json` (`loudness.loudnorm_measure_2dp`), `build/remeasure/logs/*.ebur128.log`, `build/remeasure/logs/*.loudnorm_measure.log`; the re-stitch's figures: `build/recheck/measured.json`, `build/recheck/logs/` |
| — | docs | `script.md` (line 146) now gives the measured word count: 4,398 words (2,428 / 1,970), changed in `8a61f62`. | `script.md:146` |

Checked across the four scenes:
- All four end on an empty frame (luma 14–16; `scenes/end_frames_luma.json`), and no lecture tag
  shows at any scene end.
- In the burned copy, the subtitles sit in the band under the picture and never cover a tag or a
  command (`scenes/subs/zhen_*.png`).
- The sheets for S06, S11 and S14 start 2 s after the scene does (an ffmpeg rounding effect); S02's
  start at 01:22.700.

Chapters did not move: the 16 re-stitched scene lengths equal the previous ones to the millisecond
(`scenes/scene_offsets.json`).

**Audio encode, after the recheck (final stitch, 09:34–10:22 UTC).** The re-stitch met the −1.5 dBTP
target by only 0.03–0.13 dB. The encoded file's true peak overshoots the sample-peak limit: with AAC
at 128k, by about 1.1 dB on L03's full cut (−0.9 dBTP at limit 0.79, i.e. −2.05 dBFS) and by
0.42–0.52 dB on this re-stitch. AAC noise substitution put a +0.9 dBTP spike into L03 part 2 that showed only when decoding from the
start. `8a092e4` turns noise substitution off (`-aac_pns 0`); `5833542` lowers the limit from 0.79
to 0.71 and encodes at 192k instead of 128k. The cut was stitched again with `--no-render --crf 27
--burn` from the same sixteen segments (all dated 04:52 UTC or earlier); the 16 tracked subtitle,
chapter and transcript files it rewrote are byte-identical to HEAD. Re-measured
(`build/remeasure/measured.json`): true peak −2.34 dBTP (full cut, Bilibili copy, part 1) and
−2.81 (part 2), 0.84–1.31 dB under the target; −16.07 to −16.10 LUFS; LRA 2.1–2.2 LU; AAC 178–179
kb/s; 103.39 / 104.38 / 54.52 / 49.87 MB. Durations, frame counts and video bitrates are as before.

## Open items in this cut (left as is, with the reason)

| time | scene | item | why it was left |
| --- | --- | --- | --- |
| 25:34.8–25:35.6 | S14 | The tracker's section-name pulse briefly touches the tracker's "›" separator, around 25:35.1 (`build/recheck/scenes/s14/f_25m35.100.png`). The rest of this row, the slide-77 span and the near-empty frame, was fixed in the fix round. | The shared tracker pattern. |
| 21:31.98–21:39.81 | S12 | The bilingual Chinese line breaks after 先写: cue 380 ends 在 docker tag 后面先写 and cue 381 starts simple-translate 再写你的用户名/…, so cue 380's Chinese already starts on the command while its English line is only "Then tag the image:". | The trade-off of keeping the English command whole in one cue, which the fix round chose. |
| 27:27.4–29:31.8 | S15 | No cost dial during S15 while the VM still bills; S16's needle resumes ahead of S14's, so it never rewinds. | The badge's corner is used in at least five S15 beats: a redesign, not a fix. Raise on the issue if wanted. |
| 27:27.4 | S15 | `.zh.srt` splits the deploy command after `run`: `然后是部署：sudo docker run` / `--rm -ti dlops/simple-translate`. The bilingual track keeps it whole (cue 483). | Toolkit (`explainer/subtitles.py` `_cut_penalty`), a separate PR; a yaml rewrite breaks the bilingual English line. |
| 10:28.2 | S07 | "the pip step says CACHED, but COPY says DONE" describes the plain log, not the compact view. | The screen shows and highlights the plain log's `#7 DONE`, so voice and screen agree. |
| 12:03.7 | S07 | The narration doesn't say why the prompt reads `(app)`. | A GREY tag shows `pyproject.toml · line 2: name = "app"`, and the subtitles show `(app)`. |
| about 17:44 | S10 | S04's compressed download sizes are not narrated. | They now turn into the labelled note "≈ 47.6 MB compressed download / → unpacked on disk". |
| about 19:52 | S11 | The rebuild's `Downloading cpython-3.15.0-linux-x86_64-gnu` line has no Apple Silicon note (S10 has one). | Not carried into the finishing plan (nit). |
| 20:19.1–20:22.4 | S11 | The tag reads "erratum · expected while learning" while the voice says "that's expected". | Recorded decision: `BRIEF.md` erratum 7 and `script.md`'s S11 SHOW. |
| 26:14.6 | S14 | The narration's "skip ahead to the version check" gives no "answer Y". | The on-screen note says "it asks [Y/n]? answer Y / → skip to step 4: Docker version". |
| about 30:04–30:07 | S16 | `docker buildx rm multi-arch` and `docker logout` are on screen, not said. | Optional; the chips are readable for about 3.3 s. |
| about 04:45 | S03 | The simple-translate chip's flight crosses the clone URL row for about 0.3 s. | No clean route inside the frame. |
| several | all | English cue switches inside one sentence are timed by written length, so a cue can change up to about 1 s off its words. | Toolkit (`subtitles.tracks`), a separate PR. The final onset check found no cue whose audio starts more than 1 s after the cue. |

Minor timing nits the verifiers saw and left:
- S11's `--progress=plain` underline starts about 0.5 s after its words (about 19:10.9).
- At the peak of S13's post-block pulse, the gap in "built on a Mac: linux/arm64" nearly closes for
  about 0.6 s (about 24:03.6).
- S15's pull ride starts about 0.3 s after "from Docker Hub".

The fix round's fixers and verifiers saw two more on 720p preview frames. Both are older than the
fix round, and the adversarial re-check confirmed both on the re-stitched 1080p60 cut:
- S06's "RUN pip install uv" row passes over the terminal's "laptop" title bar as a smear of letters
  while it turns into the layer slab (the `TransformFromCopy` runs 09:16.733–09:17.433; the smear
  shows at about 09:16.9–09:17.2, over the title bar and then the `python:3.12-slim-bookworm`
  label; `build/recheck/adv/frames/s06/clean_09m16.900.png` to `clean_09m17.200.png`). This is the
  intended transform, caught mid-morph.
- S14's terminal title-bar line fades in at its final width and reaches past the right edge of the
  growing box, at low opacity, for about 0.3 s (about 25:56.8–25:57.1;
  `build/recheck/adv/frames/s14/clean_25m56.800.png` to `clean_25m57.100.png`).

## Verified (final render)

Measured on the final stitch (`build/remeasure/measured.json`, 2026-10-18 10:26–10:50 UTC, one
ffmpeg job at a time; raw logs in `build/remeasure/logs/`, subtitle and chapter checks in
`build/remeasure/subs_chapters.json`). The MP4s were written at 09:38:09 (clean), 10:19:55 (zh-en),
10:21:32 (part 1) and 10:22:50 (part 2) UTC, and their timestamps did not change while they were
measured. The independent re-measure in `build/recheck/adv/logs/` was of the re-stitch, whose
figures it confirmed. An adversarial verifier then re-measured all four final files on its own,
10:56–11:05 UTC, one ffmpeg job at a time (`build/remeasure/verify/`: probes, packet counts,
`ebur128`, `loudnorm`, a 4× soxr-oversampled peak with its location, audio MD5). Sizes, bitrates,
packet counts, loudness, true peak, LRA and audio MD5s agree with `build/remeasure/` (the figures
below); it did not re-run the full decode. Items marked "previous stitch" come
from the 2026-10-17 stitch (`build/final-review/`) and were not re-run; items marked "re-stitch"
come from the 05:20 stitch (`build/recheck/`), which used the same scene segments as the final one.

- **Encode and decode.** All four files are H.264 High, 1920×1080, 60 fps, yuv420p, with AAC-LC
  48 kHz stereo at 178–179 kb/s (the re-stitch had 117–118 kb/s at 128k). A full `ffmpeg -v error …
  -f null -` decode of each exited 0 with no error lines, and the frame counts read during decoding
  match the file headers. Overall bitrates are 440.5 / 444.7 / 428.4 / 464.1 kb/s, in the order of
  the table; the video bitrates, 250.4 / 254.6 / 237.7 / 274.6 kb/s, and the audio packet counts
  equal the re-stitch's.

  | file | duration | video frames | size | loudness | true peak | LRA |
  | --- | --- | --- | --- | --- | --- | --- |
  | `ac215-l02-containers-1.zh-en.mp4` (Bilibili) | 1877.715 s (31:17.7) | 112,662 | 103.39 MB | −16.1 LUFS (−16.08) | −2.3 dBTP (−2.34) | 2.1 LU |
  | `ac215-l02-containers-1.mp4` | 1877.715 s | 112,661 | 104.38 MB | −16.1 LUFS (−16.08) | −2.3 dBTP (−2.34) | 2.1 LU |
  | `ac215-l02-containers-1_part1.mp4` | 1018.004 s (16:58.0) | 61,077 | 54.52 MB | −16.1 LUFS (−16.10) | −2.3 dBTP (−2.34) | 2.1 LU |
  | `ac215-l02-containers-1_part2.mp4` | 859.813 s (14:19.8) | 51,584 | 49.87 MB | −16.0 LUFS (−16.07) | −2.8 dBTP (−2.81) | 2.2 LU |

  Loudness, true peak and LRA come from `ebur128=peak=true`. The two-decimal figures in brackets
  come from `loudnorm` run in measure-only mode. The true-peak target of −1.5 dBTP is met on every
  file, by 0.84–1.31 dB; the re-stitch read −1.53, −1.53, −1.53 and −1.63 (0.03–0.13 dB under), and
  the previous stitch −1.2, −1.2, −1.3 and −1.0. In every file both channels peak at the same level
  (to 0.1 dB; 4× oversampled, left / right −2.340 / −2.343 dB in the full cuts and part 1,
  −2.813 / −2.813 in part 2). In that oversampled decode from the start, the highest peak falls at
  04:11.8 (251.81 s) in both full cuts and part 1, and part 2's at 06:45.6 of the part (405.58 s,
  23:43.5 in the full cut). The full cuts' one-decimal loudness reads −16.1 where the re-stitch's
  read −16.0 because `ebur128`'s own integrated value sits on the rounding edge: −16.055 unrounded
  on the final stitch (part 2: −16.040), while `loudnorm` reads −16.08 on both stitches. The audio
  packets of `zh-en.mp4` are identical to the clean cut's (same MD5); every file's audio MD5 is new, as
  expected from the new encode.
- **Lengths and chapters.** The 16 scene renders sum to 1877.683 s and 112,661 frames. The four
  re-rendered scenes (S02, S06, S11, S14) keep their lengths to the millisecond, and each stitched
  scene's frame count equals its render's. The other twelve are stitched from the same normalized
  segments as before (written 2026-10-17). Part 1 + part 2 = 1877.817 s, +0.102 s against the full
  cut; counting video streams alone, the difference is 0.000 s and the parts' frames add up to
  112,661. `chapters.txt` has 16 entries whose titles, order and start times match `video.yaml` and
  the stitched scene lengths; its content is unchanged since `0c4d0e9`. `chapters_part1.txt` (9)
  and `chapters_part2.txt` (7) match too.
  - Previous stitch: all 16 chapter starts show their scene, no scene is black or missing, and all
    16 scene-end frames are empty (compression noise at most 3 of 255 levels).
  - Re-stitch: the four re-rendered scenes' end frames read luma 14–16
    (`build/recheck/scenes/end_frames_luma.json`).
- **Subtitles.** `.srt` 502 cues, `.zh.srt` 460, `.zh-en.srt` 546: numbered in order, no overlaps, no
  cue under 1.000 s, at most two lines, all between 0.000 s and 1875.939 s (1.78 s before the end).
  The part files (285 / 255 / 302 and 217 / 205 / 244 cues) pass the same checks; part 1's shortest
  cue is 1.003 s. Each part's cues match the full cut's for that stretch exactly. The fix round
  changed only bilingual cues 380/381 and `.zh.srt` cues 319/320, plus the same cues in part 2 (see
  the fix-round table); the English `.srt` is unchanged since `0c4d0e9`. Every bilingual cue
  is one Chinese line over one English line; 539 have Chinese characters in the Chinese line. The
  other 7: #57 (03:18.5) and #366 (20:44.3) carry the README section heading, with the Chinese
  lead-in 现在进入 README 的这一节 in the cue before; #99, #263, #288, #429, #483 are commands or
  `exec format error`. In `.zh.srt`, cue #244 (15:55) is a command. Three pairs (56/57, 230/231,
  365/366) show the whole English sentence under both Chinese halves: the tool's fallback when it
  finds no matching cut, not a swap. The winpty case reads in order (cues 61–62, 03:30.6 and 03:34.1).
- **Burned subtitles** (`zh-en.mp4`). The picture is scaled to 87 % at the top and the subtitles sit
  in the band below, so they never cover the picture. Previous stitch:
  - every subtitle frame shows exactly two lines, Chinese above English, and the widest line is
    1096 px (x 411–1507);
  - spot-checks at 3:51, 4:09, 4:51, 6:03, 7:51, 9:36, 10:30, 14:48, 26:09 and 27:36 show every
    terminal command clear of the subtitles (`subs_spotcheck_mosaic.png`);
  - in the clean cut nothing reaches below y = 1040 or touches the frame edges.

  Re-stitch:
  - S12's cue 381 shows two lines, 897 px and 706 px (`build/recheck/s12_tag_burned_extent.json`);
  - the four changed scenes' 2 s sheets show the subtitles only in the band under the picture;
  - the parts are clean cuts: nothing above level 21 below y = 1040
    (`build/recheck/frames/ac215-l02-containers-1_part1_t200.png`, `_part2_t277.png`).
- **Motion** (previous stitch). 21 still stretches of 4.0–8.4 s (freeze detection on a 480 px copy);
  the scene timings show narration and small animations in all but two, which are the ponder cards
  at 16:06–16:10 and 24:18–24:22. The longest, 8.4 s at 10:07.9–10:16.3, is narrated over the "Now
  predict" chips.
- **ASR round trip** (substitute for a listen; previous stitch). It was run on the 2026-10-17
  stitch and not re-run on the re-stitch or the final stitch. The narration is the same: no SAY line
  changed in the fix round (`script.md` changed only SHOW lines and the word count), and the 129
  voice blocks have the same per-scene durations, 1762.133 s in all. The re-stitch changed only the
  four scenes listed and added the limiter after `loudnorm`; the final stitch changed only the final
  audio encode (limit 0.71, AAC at 192k, no noise substitution). `asr_video.py` with base.en on the
  clean cut against its `.srt`: 502 cues, 4,538 words recognised, 225 cues differing. Every differing cue was re-run with
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
- **Lecture tags**: 21 appearances of 20 tags. There are 18 `lecture_ref` call sites; S02's helper
  makes three tags and S12's tag shows twice.
  - Sources: `build/final-review/` (`tags_summary.json`, `tags/<id>/`) and, for the four
    re-rendered scenes, `build/recheck/scenes/tag_spans.json`.
  - In and out times come from each scene's code and `events.json`. Previous stitch: offsets
    checked against the cut to within one frame. Re-stitch: the S02, S11 and S14 tags checked on
    frames of the clean cut.
  - All are grey, and singular and plural are right ("slide 57", "slide 60", "slide 73", "slide
    77"). Seven sit off the standard top-right spot on purpose: S02 ×3, S05, S10, S14's second, and
    S16's Next tag, which also clears the burned subtitles.
  - The three spans that did not match their picture are fixed (fix-round table). S02's first tag,
    whose code the fix round did not touch, still holds through the class/instance beat: it fades
    out with the class/instance captions at 02:27.200–02:27.900 (`events.json`); it is on at
    02:27.3 and gone by 02:28.0 (`build/recheck/review/s02_first_tag_t147.3.png`, `_t148.6.png`;
    `build/recheck/adv/frames/s02/clean_02m27.300.png` to `clean_02m28.000.png`).
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
  - 4299714089 (thread PRRT_kwDOU7eKAs6tZHA3), verified on the re-stitched cut:
    - The three tags it names hold. S02's "slides 30–31, 35" runs through the class/instance beat
      (`build/recheck/review/s02_first_tag_t147.3.png`, `_t148.6.png`). S03's tag runs to the end
      of its scene; S03 is unchanged.
    - S02's "slides 9–12, 22–24" now runs through the Docker Desktop beat and leaves with its
      VM/kernel picture at 03:05.917–03:06.517 instead of outlasting it by about 10 s. `script.md`
      now gives that span.
    - The thread's general point, tags leaving before the picture they cite, is closed. S11's
      all-CACHED rebuild now has its own slide-60 tag, and S14's slide-77 tag spans the console.
    - Evidence: the S02, S11 and S14 rows of the fix-round table.
  - 4305798900, verified: the part-2 `.zh-en.srt`, `.zh-en.ass` and `.zh.srt` (commit `bdfead6`)
    carry the same `docker tag` wording as the full cut, at part-2 cues 78/79 (`.ass` lines 92/93,
    `.zh.srt` 64/65). Every part-2 cue equals the full cut's minus 1017.950 s, in both text and
    timing, up to the `.ass` file's centisecond rounding (two end times 0.01 s apart)
    (`build/recheck/scenes/subs/part2_vs_full.json`, `build/recheck/adv/subs_check.json`).
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
  quality, pacing preference or how the video feels. It ran on the previous stitch and was not
  re-run on the re-stitch, whose audio passes through the new limiter, or on the final stitch, whose
  audio is limited at 0.71 and encoded at 192k without noise substitution.
- **The final stitch was only re-measured.** Its decode, probes, loudness, true peak, subtitles and
  chapters were checked (`build/remeasure/`), and its probes, loudness and true peak again
  independently (`build/remeasure/verify/`); none of its frames were looked at. Every frame cited in
  this record is of the re-stitch or the 2026-10-17 stitch; the re-stitch used the same sixteen
  scene segments. The final stitch's durations, frame counts and video bitrates equal the
  re-stitch's, but no video-packet checksum of the re-stitch was kept, so the picture was not
  compared byte for byte.
- **The re-stitch was checked only where it changed.** The four changed scenes were re-read at one
  frame every 2 s plus exact frames, and every file was re-measured. The other twelve scenes were
  not looked at again; their stitched segments are the same files as in the previous stitch. These
  checks were not re-run on the re-stitch: the motion (freeze) check, the burned-subtitle
  spot-checks, the widest-line measure and the bilingual pair reading (only the S12 cues were
  re-read).
- **The fix round's fixers and verifiers worked on 720p preview renders.** Their reports and frames
  are not in this repository. The frames cited for the fix round are of the re-stitched 1080p60
  cut.
- **The Chinese and bilingual subtitles were reviewed by agents only** (the draft's subtitle watcher
  and the final pair check, plus `python -m explainer.i18n check`); no native speaker reviewed them.
- **The visual review is sampled**: one frame every 3 s plus targeted frames on the previous stitch,
  and one every 2 s for the four changed scenes on the re-stitch. Moments between samples were not
  all seen.
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
