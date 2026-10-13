# First episode verification

Output: `outputs/skills-ecosystem/skills-ecosystem.mp4`, reviewed 2026-10-12.

## Verified

- Encoded video: H.264, 1920×1080, 30 fps; target 9,000 frames / 300 s. Container duration 300.019667 s, including AAC timing. AAC audio present.
- All twelve scenes rendered successfully from the bilingual script. All 25 narration clips match their script text and finish within their assigned scene boundaries; none was clipped to force the target duration.
- Audio was synthesized locally with Kokoro `af_heart`, speed 0.95, and normalized. Measured mean volume is -19.6 dB. No external speech-service account was needed. Audio presence/energy and timing are verified; no human listening review is claimed.
- 70 bilingual caption cues are ordered, non-overlapping and inside the movie runtime. Font-measured maximum line widths are 1462 px Chinese and 1385 px English, within the 1740 px caption area. English/Chinese tracks and styled ASS are included.
- Thirty-six encoded-video frames, three across each scene, were visually inspected. Headings, Chinese labels, paths, counts, diagrams and the caption band are readable and not cut off in those checks. Different reveal states are present. Review frames and six contact sheets are retained in the output's `review/` folder.
- The content distinguishes the pre-install baseline, file provenance versus installer identity, caches versus active discovery, and instructions versus connected tools. The completed preset catalog and defaults match the narration.
- The installed skill was found by Codex's live registry and Cursor's local catalog. A separate Claude Code invocation applied the saved settings and NASA-punk guidance to a new-topic brief. This is stronger evidence than file placement alone; it is not a render test of every style in every agent.

## Practical limits

This first episode uses a restrained Swiss editorial layout and staged diagrams. It is not a recreation of the creator's continuous spatial wall or a tested sample of the other six presets. Voice pronunciation, pacing preference and subjective visual quality remain open to user review. Captions use measured sentence timing, with estimated subdivisions inside longer sentences; they are not word-level forced alignment.

Reference review used chronological visual evidence across the full runtimes, including dense on-screen dialogue extraction for the making-of. No continuous soundtrack-listening claim is made. Original reference media and game assets are not included in this new video.

## Public checkout integration, 2026-10-12

The public package removes personal metadata paths, uses the existing root toolkit instead
of a vendored copy, and registers downloaded fonts within the scene process. A narrated
S01 sample rendered successfully in this checkout (22.215 s, 1080p30, five bilingual cues);
a representative encoded frame was inspected for layout and captions. A dedicated Python
3.12 environment was installed and verified on macOS arm64. Linux setup is documented but
not freshly tested. These checks do not establish a new full-episode or listening review.

The original full MP4 passed another complete FFmpeg decode during release preparation.
Release file hash and metadata are in `catalog/release-media.json` at the repository root.

## Engine convergence, 2026-10-13

The episode route now runs on explainer/episode.py (shared subtitles/burn/voice/music
toolkit; tools/render_episode.py is a shim). Verified in this checkout: the pre-music
build reproduces the released master's numbers exactly (300.019667 s, −19.6 dB, 70 cues;
delivery sidecars re-committed from that build, so their script_sha256 matches the
committed script.json — checked by tools/check_incubator.py). A scored build (music now
on by default) validates at 300.074 s, 70 cues, mix −16.19 LUFS / peak −1.14 dBTP, score
coverage 0.93; the swiss pixel style-check passes on sampled frames. scenes.py now imports
the shared swiss components (explainer/styles/swiss.py); a sample re-render after the
refactor reproduced s01 (22.200 s, 5 cues). The released incubator-2026-10-12 master is
unchanged; the scored cut is a new capability, not a replacement, and no human listening
review of the score is claimed yet.
