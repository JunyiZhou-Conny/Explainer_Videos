# Review record: Why is a git branch almost free?

Produced 2026-10-13 through the episode lifecycle (issue #12, PR #13), by a Claude Code
cloud session. Verified facts and unclaimed reviews are kept separate.

## Content gates (AGENTS.md)

1. **Hook** — s01 opens on a puzzle (a branch created faster than the sentence announcing
   it, against a half-gigabyte repo), not a value proposition. ✔
2. **Intuition before formalism; animated mechanism** — the pointer model is shown moving
   before any definition: s03 builds the commit graph node by node; s04 animates the commit
   (new node → parent arrow → the `idea` tag sliding, `main` provably still); s06 animates
   the two-parent merge. ✔
3. **Ponder moments and recap** — two ponder cards (s01 ~0:23, s04 ~1:47, with the rest of
   the frame dimmed) ≈ one per 90 s; s07 recaps the three ideas and ends with a
   do-it-yourself (`.git/refs/heads/<your-branch>`). ✔
4. **Written for the ear; anchored cues** — numbers spoken in words ("forty-one bytes"),
   ".git" spoken as "dot git", no SHA read aloud; 14 `wait_until` word anchors drive the
   key reveals (Kokoro sentence marks; the full build fails on missing anchors). ✔
5. **Simulated-viewer QA over the full draft** — findings below, all fixed and re-rendered. ✔
6. **Measured checks** — see Verified; **human review: Conny's listening sign-off
   (2026-10-14, in the production session, after watching the delivered full cut)**: ✔

   > 听过了，发音和配乐都可以，合并吧

## Whole-video QA (first full render, 2026-10-13)

Reviewed 14 encoded frames across all seven scenes, as the target viewer:

- [s02 ~0:40][layout] PROBLEM: the ref-file card overlapped the `.git/refs/heads` tree
  ("heads/" clipped). FIX: card moved right and narrowed; SHA width-capped; annotations
  re-seated. 
- [s03 ~1:14][layout] PROBLEM: the `idea` tag flew in on top of the third snapshot card.
  FIX: the tag now points up from below the node, where the frame is empty.
- [s04 ~0:10 of scene][readability] PROBLEM (sample round): the `idea` pointer's arrow
  crossed the `main` box while both pointed at the same commit. FIX: `branch_tag` gained a
  horizontal offset; the initial tag approaches diagonally.
- [s01/s04 ponder][focus] PROBLEM (sample round): underlying diagrams poked out around the
  ponder card. FIX: the rest of the frame dims to 15 % while a ponder is up.
- [s06 ~2:30][caption band] PROBLEM: the below-node `idea` tag entered the reserved caption
  band (the pixel check's 3 % tolerance let it through). FIX: the merge diagram lifted; the
  tag now bottoms out above the band.
- Positive checks: s05's HEAD transfer reads clearly; s06's real `cat-file` card is legible
  at phone size; captions nowhere collide with diagrams; every scene boundary cuts clean.

## Verified (final render)

- 180.000 s exactly, 1920×1080 @30 fps H.264 + AAC; 38 bilingual cues ordered and inside
  the runtime; validation sidecar committed as `delivery/` after the final build.
- Composed score mixed under narration: voice ≈ −16.1 LUFS, music ≈ −22 LUFS in gaps /
  ≈ −32 under speech, true peak ≤ −1.1 dBTP, score coverage ≥ 0.96.
- Swiss pixel style-check passed (background dominance, caption band clear) on sampled
  frames of the clean render.
- Evidence provenance in SOURCES.md: the 41-byte ref file, its exact bytes, and the
  two-parent `git cat-file` output are real, from this repository.

## Not claimed

- The Chinese caption translation was self-reviewed only; no independent translation pass.
- Conny's sign-off covers pronunciation and music on a full listen; no second human
  reviewer has watched the cut.
