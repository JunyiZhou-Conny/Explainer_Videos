# Explainer video style guide

How every video in this repo should look, sound and be built. It is written for both humans and
coding agents that implement scenes. The condensed, music-led **short** format has its own profile
(black, one glowing accent, hairlines, captions instead of narration, a beat grid):
[SHORTS.md](SHORTS.md); everything below is about the long, narrated videos.

## 1. Principles (borrowed from 3Blue1Brown)

1. **One idea per beat.** Each narration block (`with self.voiceover(...)`) shows one thing. If the
   narrator is talking about the ratio, the ratio is the brightest object on screen.
2. **Picture before formula.** Show the object, move it, *then* write the equation that describes
   what the viewer just saw. When the formula appears, highlight the part being spoken about.
3. **Semantic colour.** A concept keeps its colour for the whole video (declared at the top of the
   video's `script.md`). Never colour for decoration.
4. **Motion carries meaning.** Prefer `Transform` / `TransformMatchingTex` / `.animate` over
   fade-out-fade-in, so the viewer sees *what became what*. Use `Indicate`, `Circumscribe`,
   `Flash` to point. Use `FadeOut` to clear things that are done.
5. **Uncluttered frame.** At most ~3 visual groups at once. When the topic changes, clear the stage.
   Text is sparse: labels and short captions, never paragraphs — the narrator does the talking.
6. **Active viewing.** Use `pause_and_ponder(...)` where a viewer can genuinely work something out,
   and end with questions to test yourself (answers in the companion `exercises.md`).
7. **Mentor's map.** Each paper video places the paper in its lineage: what problem it inherited,
   what it changed, and what grew out of it (paper cards on a timeline, arrows labelled by idea).

## 2. Canvas and typography

- Frame is 14.2 × 8 Manim units (16:9). Keep content inside x ∈ [−6.6, 6.6], y ∈ [−3.6, 3.6].
- Background `style.BG` (near-black). Text font `style.FONT` (CMU Serif, matches LaTeX). Labels
  inside diagrams may use `style.FONT_SANS`.
- Sizes (font_size): titles 48–56, body 32–36, labels 24–28, smallest 20. Nothing below 20.
- A scene title, when used, sits at the top: `title.to_edge(UP, buff=0.45)`.
- Maths: `style.math(r"...")` (MathTex). Colour sub-parts with `substrings_to_isolate=[...]` /
  `set_color_by_tex`, or by indexing tex parts. Text: `style.text("...", size, color)`.

## 3. Timing with narration

```python
from manim import *
from explainer.scene import VoiceScene
from explainer import style as S
from explainer.components import *

class MyScene(VoiceScene):
    def construct(self):
        with self.voiceover("First sentence. Second sentence mentions the ratio.") as vo:
            self.play(FadeIn(thing), run_time=1.0)
            vo.wait_until("the ratio")                       # approx. time the phrase is spoken
            self.play(Indicate(ratio), run_time=vo.remaining())
```

- Every `SAY:` line of the script becomes exactly one `voiceover` block, text verbatim.
- `vo.duration` (whole clip), `vo.remaining()` (left in clip), `vo.until("phrase")` (run time ending
  when the phrase starts), `vo.wait_until("phrase")`. Phrase timing is estimated per sentence, so
  anchor to phrases near the start of sentences when precision matters.
- The block waits for the clip to end automatically; don't add long manual waits.
- Avoid dead air: something should move at least every ~4 s, except during ponder cards.
- Scenes start from an empty frame and **end with everything faded out** (`self.play(FadeOut(*self.mobjects))`)
  so scene cuts are clean.

## 4. Toolkit cheat-sheet (`explainer/`)

| helper | what it gives you |
| --- | --- |
| `style.text / math / tex / bullets` | house-font text, MathTex, Tex, bullet lists |
| `style.BLUE, ORANGE, YELLOW, GREEN, RED, PINK, PURPLE, TEAL, GOLD, GREY, WHITE` | palette |
| `person_icon(color, height)` | head-and-shoulders glyph |
| `person_grid(n, cols, color)` | n icons in a grid ("a database of people") |
| `database_rows(labels, values, color)` | stacked table rows `[box, icon, name, value]` |
| `paper_card(name, year, idea, color, highlight)` | card for a paper on a map |
| `connect(a, b, label)` | edge-to-edge arrow with optional label |
| `timeline(start, end, width, step)` | year axis with `.year_to_point(y)` |
| `chapter_card(scene, n, title)` | plays a chapter title in and out |
| `pause_and_ponder(scene, question, seconds)` | ponder card with draining timer (returns card) |
| `paper_page(png, height)` | image of a real paper page + frame |
| `laplace_pdf, gaussian_pdf` | densities for plotting |
| `highlight_box(m)` | yellow rounded box around a mobject |

## 5. Checking your work

```bash
python -m explainer.preview videos/<id>/scenes/s07_laplace.py LaplaceMechanism          # contact sheet
python -m explainer.preview videos/<id>/scenes/s07_laplace.py LaplaceMechanism --at 12,30 -q m
python -m explainer.check videos/<id>/scenes/s07_laplace.py LaplaceMechanism            # off-frame / tiny text / leftovers
python -m explainer.build videos/<id> -q l --only s07_laplace                           # re-render one scene
```

Open the contact-sheet PNG and check, frame by frame:

- [ ] nothing overlaps unintentionally; no text touches the frame edge or is clipped
- [ ] text is readable (≥ 20 pt) and not on top of busy graphics
- [ ] colours follow the semantic table
- [ ] the thing being narrated is what's visually emphasised at that moment
- [ ] no long static stretches; the scene ends on an empty frame

## 6. Manim gotchas

- `MathTex` parts: pass separate strings (`math("S(f)", "=", r"\max", ...)`) to colour/animate parts.
- `Text` measures in font points; `.scale_to_fit_width(w)` if it might overflow.
- `always_redraw` / updaters are convenient but slow; remove them (`clear_updaters()`) when done.
- `Axes.plot(f, x_range=[a, b, step])` — use a small step for the Laplace kink (`0.01`).
- `ValueTracker` + `always_redraw` is the standard way to "drag" a parameter.
- Images: `ImageMobject` can't be `Write`-n; use `FadeIn`.
- Keep scenes deterministic (seed any randomness: `np.random.default_rng(7)`).
