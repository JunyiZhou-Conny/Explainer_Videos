# L05 QA follow-ups (from PR review bots while scenes were being built)

Each item was found on a work-in-progress checkpoint; check it in the CURRENT code and on frames.

- S03 (s03_setup.py, Bugbot thread "Extra tag overlaps a full-width command"): the extra check
  `docker --version; docker compose version` fills all 65 columns of the laptop prompt row, so
  `beside(extra_tag(), t, cmd0)` cannot sit after the text and clamps over it. Put the tag on an output
  row or as a caption under the terminal.
- S04 (s04_compose.py, Bugbot thread "Build-size box uses drifting col_box"): the yellow box on
  `112.26MB` used `col_box`; e815bd3 made `col_box` measure column 0 from the glyphs (`grid_x0`).
  Check the box frames exactly `112.26MB`.
- S08 (s08_embed.py, Bugbot thread "Error row lingers on embed strip"): beat 9 types the second `--embed`
  command into the 3-row strip that beat 7 left full (two command rows + the missing-key error); the
  error stays above the new command during the ▶ hold. Clear or resize the strip first.
- S09 (s09_load.py, Bugbot thread "Prior load output remains on screen"): beat 6 types the
  recursive-split load into the still-full 13-row terminal from beat 5 without `t.clear()`; a leftover
  char-split line can sit above the new command. Those rows should hold only this command and its output.
- S11 (s11_query.py, Bugbot thread "Long cost tag overlaps prompt"): the beat-5 `cost_tag` is pinned beside
  the folded command's prompt row; the string is much longer than S08's tag, so `beside` clamps it over the
  end of `app@390fe47a277a:/app$`. Move it off that row.
- Pattern across S03/S08/S11: `beside(tag, t, row)` on a long row clamps over the text. Grep every L05 scene
  for `beside(` and check each frame.
- S13 (s13_chat.py, Bugbot thread "Line 372 highlight indexes wrong glyphs", fixed by the coordinator):
  `tc.rows[3]` is one Text of 40 glyphs, so `[0]` was the first glyph and the slice was empty. The beat-9
  highlight now slices the row itself (glyphs 23–29 = "line372", asserted). The scene's build was cut off by
  a usage limit: on resume its check stopped earlier, at the `ill`/`src` assert (line 519). Check the
  beat-9 frame once the scene builds.
- S14 (s14_semantic.py ~587–602, Bugbot thread "Strip shrink drops container frame color", found while the scene
  was still being built): beat 7 shrinks the TEAL container terminal by Transform-ing `t.box` into a dummy
  `Terminal` that keeps the default GREY laptop chrome, so the strip turns GREY while its title still says
  container. Use the house `resize()` helper (it copies the live stroke onto the dummy) or copy the stroke
  before the Transform; check the frame after beat 7.
- S11 (s11_query.py ~539–549, Bugbot thread "Cleared strip leaves typed command"): `FadeOut(t.lines)` takes the
  lines group off the terminal (Manim's Scene.remove on a submobject splits it from `t`), so the next
  `type_cmd` adds its rows as top-level objects and the later `FadeOut(t)` can leave
  `python cli.py --query --chunk_type recursive-split` on screen, in the band the your-turn card moves into.
  Check the frames after that FadeOut(t); clear the strip with the house helper (or `t.clear`) instead.
- S13 (s13_chat.py ~254–262, Bugbot thread "Tracker caption pops instead of fading"): `tracker_to` calls
  `become` and sets the live caption to opacity 0 before `play`, then fades out a `caption.copy()` that was never
  added to the scene, so the old step label vanishes in one frame instead of cross-fading. Check the frames of
  a tracker step change; add the copy to the scene before fading it (or cross-fade the live caption).
- S13 (s13_chat.py ~663–673 and ~690–691, Bugbot thread "Chat morph leaves original window", High): the
  `ReplacementTransform` runs on throwaway `shell()` wrappers around members that still belong to the
  on-scene `win` and `q`; only the wrappers swap, so `win` can stay on screen as a second chrome copy beside
  `br`, and the closing fade (`br`, `bq`) leaves `win`/`q` behind after the empty-frame hold. Check the frames
  around the morph and the scene's last frame (`explainer.check` leftovers); transform `win`/`q` themselves,
  or remove the members from them first, and fade everything at the end. (The S13 critique was paused
  mid-edit at 05:15 UTC Oct 18: check this after it resumes.)
