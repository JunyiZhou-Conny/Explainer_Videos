# L04 QA follow-ups (from PR review bots while scenes were being built)

- S11 (s11_start.py, Bugbot thread on line 268, OPEN until checked on frames): the processor's default-value
  underlines on YAML line 13 crossed the capitals on line 14. `base_under` now builds `d_lines` (line 622).
  Verify in the frames of that beat that every underline sits under its own line and clear of line 14.
- S16 (s16_recap.py, Bugbot, resolved): the shared-layers bracket now sits right of the image rows
  (`x = max(glyph right) + 0.25`). Check in the recap frames that the brace and its label
  `shared layers · ≈ 200 MB in all` stay right of the names and inside the frame.
- S15 (s15_compose.py, Bugbot, does not reproduce): `swap_panel` hides the incoming panel from t = 0
  (AnimationGroup begins every part at once). Nothing to do unless a contact sheet shows two panels at once.
- L04/L05 `col_box` now measures column 0 from the glyphs (`grid_x0`, e815bd3): boxes in S13 and S15
  moved right by about 0.6 cell. Check that each box frames exactly its characters.
- S03 (s03_code.py SKIP_TO, Bugbot thread "Skip timestamp misses the next chapter"): the finishing pass lengthens
  S03 (copy-out warning before the pause), so the "cloned fresh? skip to …" chip must be recomputed from the
  re-voiced scene durations. After the 1080p stitch, check the chip text equals S04's start in output/chapters.txt.
