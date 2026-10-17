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
