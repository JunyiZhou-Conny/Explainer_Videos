# L02 QA follow-ups (from PR review bots while scenes were being built)

- S12 (s12_push.py ~645–646, 672–674, 707–710; Bugbot thread 4267479737, OPEN): unparking the push picture restores
  `st`, `hub` and the parcels but not `path` (removed with `body` in beat 6), so later parcels move along an invisible
  route (denied-push return, stand-in upload). Restore `path` with the rest; check those beats' frames.
- S10 (s10_inside.py ~352–361, 609–610; Bugbot thread 4267479746, OPEN): FadeIn(card9.everything()) leaves the wrapper
  on the scene as the card's parent; `park` FadeOuts a NEW everything() group, so the card snaps back over the
  terminal. Beat 5: FadeOut of a throwaway wrapper around `cap` without self.remove(cap). Fix: fade/remove the object
  actually on the scene; check the frames after park and after beat 5.
- All L02 scenes: sweep for the FadeOut-wrapper snap-back pattern (see SKILL.md pitfalls).

## How to judge the FadeOut "snap-back" findings above (tested 2026-10-15, Manim 0.22)
`FadeOut(wrapper)` takes every member off the scene, even members that are children of a panel on the scene,
then restores their opacity. A member snaps back only if it is still a child of a parent that is later added
or animated again (`self.add(panel)`, `panel.animate…`, a Transform of the panel). So for each finding: check
whether the faded members stay in a parent that comes back later. If they do, fix it (remove them from the
parent, or fade the parent); if not, the finding does not reproduce. Bugbot's PR #29 finding on L02 S12
`scroll()` did not reproduce: the rows leave `t.lines` right after the fade.
