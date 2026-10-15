# L03 QA follow-ups (from PR review bots while scenes were being built)

- S07 → S08 continuity (Bugbot, PR #6 thread on s08_uv_add.py:267): part 2 opens by reusing part 1's last
  picture; S08's recap now rebuilds S07's close (recap_window/recap_extras). Verify the two frames match in
  the whole-video pass (S07 last frame vs S08 first frames).
- S07: two unused imports (ruff F401) left by concurrent edits.
- Shared-code requests from scene agents: VersionLine label-over-start option (S04), beside() row-below
  fallback (S04), code_panel font_size + line-number gutter (S05), ConfigCard attached glyph (S05),
  readme_chip two-row variant (S05), Window.blink() invisible on PINK route + outline-pulse helper (S07),
  public hidden-part registration on Window (S07).
- S07: a short GREEN line (Window's package shelf, filled in S08) sits right of the writable layer from beat 0
  and is never explained in S07. Decide in the whole-video pass: hide it until S08, or name it.
- S08 (s08_uv_add.py ~701–702, Bugbot thread 4267126161, OPEN until fixed): FadeOut(VGroup(ov.panel, ov.rows)) —
  the wrapper isn't on the scene, the children stay in the scene via `ov`, and FadeOut's clean-up restores their
  opacity, so the README overlay snaps back before the "your turn" tag and covers the --help output. Fix: FadeOut(ov)
  (or self.remove(ov.panel, ov.rows) after the fade). Verify in the frames around the "your turn" beat.
- All scenes, all lectures: grep for FadeOut(VGroup(...)) / FadeOut of throwaway wrappers whose members stay on the
  scene through another parent; same snap-back.

## S14 (s14_secrets.py) — build agent returned before reading its preview
The build agent ended with "The preview is still rendering; I'll wait for the monitor's notice before
reading the sheets." The file is structurally complete (10/10 voiceover blocks, `explainer.check` OK at
11:16 UTC, 124.5 s, empty last frame), but nobody looked at its frames during the build. The critique stage
reviews them; at whole-video QA, give S14's contact sheets a full read regardless of the critique's verdict.
