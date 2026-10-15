"""speciesOT E5 · What next? Follow the errors — Swiss scenes.

Narration and budgets come from the plan (script.json). Josh's code on screen comes only from
videos/speciesot-series/excerpts.py (real line numbers; a long line may be elided with "…",
never rewritten). Repo facts come from the speciesOT repo at 109bf12 (specs/m1_modern.yaml,
speciesOT/baseline/analysis/v08_scorecard_dual.csv, cellot/.../extended_metrics.py); measured
facts from videos/speciesot-series/checks/error_trail.json. Our own sketches carry EXAMPLE, our
recommendations (SOLID mapping, card order) carry INFERRED.

This episode's diagrams: three piles (file shape, 83 notebook tiles, a Feb→Oct strip), a habit
loop, four stage boxes with a walking token, an error track that becomes a to-do board, gene
axes as bars, one table splitting into four files, a scorecard ladder with 80-cell sampling,
SOLID letters pointing into the file's shape, and the Monday loop.
"""
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent.parent / "speciesot-series"
sys.path.insert(0, str(SERIES))

from manim import *  # noqa: E402,F401,F403
from speciesot_kit import *  # noqa: E402,F401,F403
from excerpts import CORE, E24_OUTPUTS, LINE_KINDS, LINE_LENGTHS, rows  # noqa: E402

CORE_PATH = "src/speciesot/speciesot_core.py"
SPEC_PATH = "speciesOT · specs/m1_modern.yaml"
CARD_PATH = "speciesOT · speciesOT/baseline/analysis/v08_scorecard_dual.csv"
METRICS_PATH = "speciesOT · cellot/cellot_gpu/scripts/extended_metrics.py"
CSV5 = "m1 v08 scGen,0.927,0.1737,…,0.5542,…"   # v08_scorecard_dual.csv line 5, columns elided
N_NOTEBOOKS = 83            # .ipynb files in the speciesOT repo at 109bf12 (no checkpoints)
STAGES = ["setup", "train", "predict", "evaluate"]
STAGE_X = [-4.65, -1.55, 1.55, 4.65]

# m1_modern.yaml (speciesOT repo at 109bf12), the lines shown on screen, verbatim
SPEC = {
    1: "experiment_tag: hvg_pearson_residuals_m1_v08_ood",
    22: "condition_column: condition",
    23: "source: mouse",
    24: "target: human",
    4: "data_file: datasets/speciesot-human-mouse-hvg/hvg_pearson_residuals_m1_v08.h5ad",
    27: "holdout_species: null",
    25: "holdout_cell_types:",
    26: "- CL:0000875",
    28: "datasplit_strategy: toggle_ood",
    29: "mode: ood",
    30: "test_size: 0.2",
    31: "random_state: 0",
    32: "datasplit_stratify: condition",
    33: "scgen_hidden_units:",
    34: "- 256",
    35: "- 256",
}
# extended_metrics.py 154-157 and 166 (speciesOT repo at 109bf12), verbatim
METRICS = {
    154: "    def _r2_means(A, B):",
    155: "        a, b = np.asarray(A).mean(0), np.asarray(B).mean(0)",
    156: "        r = np.corrcoef(a, b)[0, 1]",
    157: "        return float(r * r)",
    166: "    r2_identity = _r2_means(control, treated) if control is not None else np.nan",
}


class Ep(EpisodeScene):
    episode = "E5"
    total = "07"


# ---------------------------------------------------------------- small parts

def tick(x, y, s=.16, color=INK, stroke=4):
    """A drawn check mark (no glyph dependence)."""
    return VMobject(color=color, stroke_width=stroke).set_points_as_corners(
        [[x - s, y, 0], [x - s * .35, y - s * .6, 0], [x + s, y + s * .7, 0]])


def cross(x, y, s=.14, color=RED, stroke=4):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=stroke),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=stroke))


def tiles(cx, cy, n=N_NOTEBOOKS, cols=12, w=.24, h=.3, gap=.08, color=GRAY):
    """n small notebook tiles (a sheet with a header strip), row by row."""
    g = VGroup()
    rows_ = -(-n // cols)
    width = cols * w + (cols - 1) * gap
    height = rows_ * h + (rows_ - 1) * gap
    for k in range(n):
        r, c = divmod(k, cols)
        x = cx - width / 2 + w / 2 + c * (w + gap)
        y = cy + height / 2 - h / 2 - r * (h + gap)
        sheet = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5,
                          fill_color=PAPER, fill_opacity=1).move_to([x, y, 0])
        strip = Rectangle(width=w, height=h * .22, stroke_width=0, fill_color=color,
                          fill_opacity=1).move_to([x, y + h / 2 - h * .11, 0])
        g.add(VGroup(sheet, strip))
    return g


def file_shape(x0, top, bottom, width=2.6, xscale=.016):
    """The real shape of speciesot_core.py: one hairline per line, length ~ characters."""
    n = len(LINE_LENGTHS)
    dy = (top - bottom) / n
    g = VGroup()
    for i, (ln, kind) in enumerate(zip(LINE_LENGTHS, LINE_KINDS)):
        if ln == 0:
            continue
        y = top - (i + .5) * dy
        g.add(Line([x0, y, 0], [x0 + min(ln * xscale, width - .25), y, 0], stroke_width=1.4,
                   color=FAINT if kind == "c" else GRAY))
    frame = Rectangle(width=width, height=top - bottom + .16, stroke_color=INK, stroke_width=2)\
        .move_to([x0 + width / 2 - .1, (top + bottom) / 2, 0])
    return frame, g


def stage_row(y, w=2.5, h=1.0, size=24, stroke=2.5):
    boxes, names, arrows = VGroup(), VGroup(), VGroup()
    for x, s in zip(STAGE_X, STAGES):
        boxes.add(Rectangle(width=w, height=h, stroke_color=INK, stroke_width=stroke,
                            fill_color=PAPER, fill_opacity=1).move_to([x, y, 0]))
        names.add(mono_line(s, x - ADVANCE * size * len(s) / 2, y + h * .18, size).set_z_index(2))
    for a, b in zip(boxes, boxes[1:]):
        arrows.add(Arrow(a.get_right(), b.get_left(), buff=.06, color=INK, stroke_width=2.5,
                         max_tip_length_to_length_ratio=.3))
    return boxes, names, arrows


def mono_line(s, x, y, size=20, color=INK, bold=False):
    """Monospace text whose first cell starts at x, on a stable baseline (strut glyph)."""
    t = Text("|" + s, font=MONO, font_size=size, color=color, weight=BOLD if bold else "NORMAL")
    t.strut = t[0]
    return place_line(t, x, y, size)


def panel_at(rows_, title, x, top, width, size):
    """A code panel whose top edge sits at `top` (built in place, so its marks line up)."""
    probe = code_panel(rows_, title, x, 0, width=width, size=size)
    return code_panel(rows_, title, x, top - probe.frame.height / 2, width=width, size=size)


def pill(text, x, y, color=INK, size=20, font=MONO, pad=.22):
    """A chip whose text sits on a stable baseline, so neighbouring chips share one height."""
    t = Text("|" + text, font=font, font_size=size, color=color)
    strut = t[0]
    t.shift([0, y - strut.get_center()[1], 0])
    t.remove(strut)
    t.shift([x - t.get_center()[0], 0, 0])
    box = RoundedRectangle(corner_radius=.06, width=t.width + 2 * pad, height=strut.height + .22,
                           stroke_color=color, stroke_width=2, fill_color=PAPER,
                           fill_opacity=1).move_to([x, y, 0])
    return VGroup(box, t)


def glyphs(text_mob, full, sub):
    """The glyphs of `sub` inside a Text built from `full` (Text drops spaces)."""
    f, t = full.replace(" ", ""), sub.replace(" ", "")
    i = f.index(t)
    return VGroup(*text_mob[i:i + len(t)])


def fly(src_point, target):
    """A copy of `target` that starts at src_point (for ReplacementTransform into target)."""
    return target.copy().move_to(src_point).set_opacity(0)


def paint(ch, color):
    """Recolour a chip's outline and text (not its paper fill)."""
    ch[0].set_stroke(color=color)
    ch[1].set_color(color)
    return ch


def tagline(kind, text, x, y, size=19, color=GRAY):
    """A provenance chip followed by a short gray note, left-aligned at x."""
    st = source_tag(kind)
    st.move_to([x + st.width / 2, y, 0])
    note = left(text, st.get_right()[0] + .18, y, size, color)
    return VGroup(st, note)


# ---------------------------------------------------------------- s01

class S01(Ep):
    def construct(self):
        self.header()
        frame, shape = file_shape(-6.0, 1.7, -.75)
        f_path = mono("speciesot_core.py", 16, GRAY).move_to([-4.5, -1.2, 0])
        # 346 = editor line count (wc -l says 345: the last line has no newline)
        f_lab = VGroup(label("346 lines", 26, INK, bold=True), source_tag("READ IN CODE"))\
            .arrange(RIGHT, buff=.2).move_to([-4.5, -1.62, 0])
        grid = tiles(-.2, .47)
        g_path = mono("speciesOT repo · *.ipynb", 16, GRAY).move_to([-.2, -1.2, 0])
        g_lab = VGroup(label("83 notebooks", 26, INK, bold=True), source_tag("READ IN CODE"))\
            .arrange(RIGHT, buff=.2).move_to([-.2, -1.62, 0])
        ax_y, x_feb, x_oct = .47, 2.75, 5.95
        months = ["Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
        mx = [x_feb + i * (x_oct - x_feb) / 8 for i in range(9)]
        axis = line(x_feb - .1, ax_y, x_oct + .1, ax_y, INK, 2)
        ticks = VGroup(*[line(x, ax_y - .1, x, ax_y + .1, GRAY, 2) for x in mx])
        ends = VGroup(at("Feb", x_feb, ax_y - .42, 18, GRAY), at("Oct", x_oct, ax_y - .42, 18, GRAY))
        bar = Rectangle(width=x_oct - x_feb, height=.34, stroke_width=0, fill_color=INK,
                        fill_opacity=1).move_to([(x_feb + x_oct) / 2, ax_y + .42, 0])
        today = at("today", x_oct, ax_y + .95, 18, RED)
        t_path = mono("logs · scorecards", 16, GRAY).move_to([4.35, -1.2, 0])
        t_lab = at("results since Feb", 4.35, -1.62, 26, INK, bold=True)
        q = at("Where does the next hour go?", 0, -2.18, 30, RED, bold=True)

        with self.say(0) as vo:
            vo.wait_until("three hundred")
            self.play(FadeIn(frame), FadeIn(f_path), FadeIn(f_lab, shift=UP * .1), run_time=.4)
            self.play(LaggedStart(*[Create(l) for l in shape], lag_ratio=.004), run_time=1.1)
            vo.wait_until("eighty-three")
            self.play(LaggedStart(*[FadeIn(t, scale=.6) for t in grid], lag_ratio=.03),
                      FadeIn(g_path), FadeIn(g_lab, shift=UP * .1), run_time=1.2)
            vo.wait_until("results going back")
            self.play(Create(axis), FadeIn(ticks), FadeIn(ends), FadeIn(today),
                      FadeIn(t_path), FadeIn(t_lab, shift=UP * .1), run_time=.4)
            self.play(GrowFromEdge(bar, RIGHT), run_time=1.0)
            vo.wait_until("Where does")
            hour = pill("next hour?", -4.8, .47, RED, 22, font=LATIN).set_z_index(4)
            self.play(FadeIn(q, shift=UP * .1), today.animate.set_color(GRAY), run_time=.4)
            self.play(FadeIn(hour, scale=.8), run_time=.2)
            for x in (-.2, 4.35):
                self.play(hour.animate.move_to([x, .47, 0]), run_time=.3)
        piles = VGroup(frame, shape, f_path, f_lab, grid, g_path, g_lab, axis, ticks, ends, bar,
                       today, t_path, t_lab)

        plan = pill("plan everything first", 0, 1.45, GRAY, 24, font=LATIN)
        nodes = [pill(t, x, .05, INK, 24, font=LATIN) for t, x in
                 (("run the code", -4.3), ("read the first break", 0), ("fix only that", 4.3))]
        a12 = arrow(nodes[0].get_right(), nodes[1].get_left(), INK)
        a23 = arrow(nodes[1].get_right(), nodes[2].get_left(), INK)
        back = CurvedArrow(nodes[2].get_bottom() + DOWN * .08, nodes[0].get_bottom() + DOWN * .08,
                           angle=-PI / 4, color=INK, stroke_width=2.5, tip_length=.2)
        token = Dot(radius=.1, color=RED).set_z_index(5)
        habit = VGroup(at("Josh's habit  →  a method", 0, -1.78, 30, RED, bold=True),
                       at("习惯 → 方法", 0, -2.25, 22, GRAY))
        with self.say(1) as vo:
            self.cue(vo, .0, FadeOut(piles, shift=UP * .2), FadeOut(q), FadeOut(hour), run_time=.5)
            vo.wait_until("planning everything")
            self.play(FadeIn(plan, shift=DOWN * .1), run_time=.4)
            vo.wait_until("first.")
            self.play(Create(strike(plan)), plan.animate.set_opacity(.45), run_time=.4)
            vo.wait_until("runs the code")
            token.move_to(nodes[0].get_top() + UP * .2)
            paint(nodes[0], RED)
            self.play(FadeIn(nodes[0], shift=UP * .1), FadeIn(token), run_time=.4)
            vo.wait_until("reads the first")
            paint(nodes[1], RED)
            self.play(GrowArrow(a12), FadeIn(nodes[1], shift=UP * .1), Transform(nodes[0], paint(nodes[0].copy(), INK)),
                      token.animate.move_to(nodes[1].get_top() + UP * .2), run_time=.6)
            vo.wait_until("fixes only")
            paint(nodes[2], RED)
            self.play(GrowArrow(a23), FadeIn(nodes[2], shift=UP * .1), Transform(nodes[1], paint(nodes[1].copy(), INK)),
                      token.animate.move_to(nodes[2].get_bottom() + DOWN * .08), run_time=.5)
            self.play(Create(back), MoveAlongPath(token, back.copy()),
                      Transform(nodes[2], paint(nodes[2].copy(), INK)),
                      Transform(nodes[0], paint(nodes[0].copy(), RED)), run_time=.8)
            vo.wait_until("This episode")
            self.play(FadeIn(habit, shift=UP * .1), run_time=.5)
        self.finish()


# ---------------------------------------------------------------- s02

class S02(Ep):
    def construct(self):
        self.header()
        y0, ty = .55, .2
        boxes, names, arrows = stage_row(y0, h=1.1)
        who = pill("IdentityModel", -4.95, 1.68, RED, 21)
        who_note = left("only · on toy data", who.get_right()[0] + .2, 1.68, 20, GRAY)
        meas = tagline("MEASURED", "identity_end_to_end", 2.35, 1.68, 18)
        token = Dot([-6.1, ty, 0], radius=.11, color=RED).set_z_index(5)
        ticks = [tick(x + .82, ty, .15).set_z_index(2) for x in STAGE_X]
        ok = at("no errors · 没有报错", 0, -.6, 28, INK, bold=True)
        with self.say(0) as vo:
            vo.wait_until("identity model")
            self.play(FadeIn(who, shift=RIGHT * .1), run_time=.4)
            vo.wait_until("whole pipeline")
            self.play(LaggedStart(*[FadeIn(VGroup(b, n), shift=UP * .1) for b, n in
                                    zip(boxes, names)], lag_ratio=.2),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.3), run_time=.9)
            vo.wait_until("toy data")
            self.play(FadeIn(who_note), FadeIn(token), run_time=.3)
            for i, w in enumerate(["setup,", "train,", "predict,", "evaluate."]):
                vo.wait_until(w)
                self.play(token.animate.move_to([STAGE_X[i], ty, 0]), run_time=.3)
                self.play(Create(ticks[i]), run_time=.15)
            vo.wait_until("No errors")
            self.play(token.animate.move_to([6.1, ty, 0]), FadeIn(ok, shift=UP * .1), FadeIn(meas),
                      run_time=.4)
        span = VGroup(line(-5.9, -.18, 5.9, -.18, INK, 2), line(-5.9, -.3, -5.9, -.06, INK, 2),
                      line(5.9, -.3, 5.9, -.06, INK, 2))
        skel = VGroup(at("walking skeleton", 0, -.72, 32, RED, bold=True),
                      at("会走路的骨架", 0, -1.2, 22, GRAY))
        with self.say(1) as vo:
            self.cue(vo, .0, FadeOut(ok), FadeIn(skel, shift=UP * .1),
                     Transform(who, paint(who.copy(), INK)), run_time=.5)
            vo.wait_until("end to end")
            self.play(Create(span), run_time=.5)
            vo.wait_until("most are thin")
            self.play(boxes.animate.set_stroke(color=GRAY, width=1.2), FadeOut(span), run_time=.6)
            vo.wait_until("thicken one bone")
            self.play(boxes[3].animate.set_stroke(color=RED, width=7), run_time=.6)
            vo.wait_until("keeps walking")
            token.move_to([-6.1, ty, 0])
            self.play(MoveAlongPath(token, Line([-6.1, ty, 0], [6.1, ty, 0])),
                      LaggedStart(*[Indicate(t, color=RED, scale_factor=1.3) for t in ticks],
                                  lag_ratio=.25), run_time=1.2, rate_func=linear)
            self.play(FadeOut(token), run_time=.2)
        ex = boxes[3].get_bottom()[0]
        out = Arrow([ex, -.02, 0], [ex, -.85, 0], buff=0, color=RED, stroke_width=3,
                    max_tip_length_to_length_ratio=.25)
        none = mono("returned None", 22, RED).move_to([ex, -1.12, 0])
        scores = VGroup(mono("R2   0.103", 20), mono("MMD  0.326", 20))
        for k, sc in enumerate(scores):
            sc.move_to([1.6, -.62 - k * .42, 0])
        toy = at("computed on toy data", 1.6, -1.5, 17, GRAY)
        # card 1: evaluate returns a table, models × metrics
        cx0, cx1, cy0, cy1 = -6.2, 1.6, -2.42, -.55
        frame = Rectangle(width=cx1 - cx0, height=cy1 - cy0, stroke_color=INK, stroke_width=2,
                          fill_color=PAPER, fill_opacity=1).move_to([(cx0 + cx1) / 2,
                                                                     (cy0 + cy1) / 2, 0])
        c_head = left("CARD 1", cx0 + .22, cy1 - .3, 20, RED, bold=True)
        c_title = left("return a table: models × metrics", cx0 + 1.35, cy1 - .3, 22, INK, bold=True)
        c_tag = source_tag("INFERRED").move_to([cx1 - .72, cy1 - .3, 0])
        cols_x, rows_y = [-2.75, -.55], [-1.62, -2.05]
        heads = VGroup(*[mono(t, 17, GRAY).move_to([x, -1.2, 0]) for t, x in
                         zip(("R2Evaluation", "MMDEvaluation"), cols_x)])
        rnames = VGroup(*[mono_left(t, cx0 + .25, y, 18) for t, y in
                          zip(("IdentityModel", "scGenModel"), rows_y)])
        cells = VGroup(*[Rectangle(width=1.95, height=.38, stroke_color=FAINT, stroke_width=1.5)
                         .move_to([x, y, 0]) for y in rows_y for x in cols_x])
        later = VGroup(*[mono("…", 18, GRAY).move_to([x, rows_y[1], 0]) for x in cols_x])
        with self.say(2) as vo:
            self.cue(vo, .0, FadeOut(skel), run_time=.3)
            vo.wait_until("evaluate returned")
            self.play(GrowArrow(out), run_time=.4)
            vo.wait_until("nothing")
            self.play(FadeIn(none, shift=DOWN * .1), run_time=.35)
            vo.wait_until("The scores")
            self.play(*[ReplacementTransform(fly(boxes[3].get_center(), sc), sc) for sc in scores],
                      FadeIn(toy), run_time=.6)
            vo.wait_until("dropped")
            self.play(scores.animate.shift(DOWN * .9).set_opacity(0), FadeOut(toy), run_time=.6)
            vo.wait_until("So the first")
            self.play(FadeIn(frame), FadeIn(c_head), FadeIn(c_title, shift=RIGHT * .1),
                      FadeIn(c_tag), run_time=.5)
            vo.wait_until("as a table")
            self.play(FadeIn(heads), FadeIn(rnames), Create(cells), run_time=.6)
            vo.wait_until("models by metrics")
            vals = VGroup(*[mono(t, 20, RED).move_to([x, rows_y[0], 0]) for t, x in
                            zip(("0.103", "0.326"), cols_x)])
            toy2 = left("toy data", .62, rows_y[0], 17, GRAY)
            self.play(*[ReplacementTransform(fly(boxes[3].get_center(), v), v) for v in vals],
                      FadeIn(later), FadeIn(toy2), run_time=.6)
        self.finish()


# ---------------------------------------------------------------- s03

# The measured trail (checks/error_trail.json): stage, type, message (verbatim), line, the
# verbatim fragment shown on the small card, and the excerpt rows that raised it.
TRAIL = [
    ("setup", "AttributeError", "'scGenModel' object has no attribute 'x_dimensions'", 253,
     "…'x_dimensions'", rows(CORE, 252, 254)),
    ("train", "TypeError",
     "scGenModel.train() missing 1 required positional argument: 'training_data'", 133,
     "…'training_data'", rows(CORE, 131, 133) + [(None, "    …"), (261, CORE[261])]),
    ("predict", "NameError", "name '_dense' is not defined", 288, "name '_dense' …",
     [(261, CORE[261]), (262, CORE[262]), (None, "        …"), (287, CORE[287]),
      (288, CORE[288])]),
    ("evaluate", "ValueError", "operands could not be broadcast together with shapes (5,4) (7,4)",
     313, "…(5,4) (7,4)", rows(CORE, 311, 313)),
]


def trail_card(i, y=.98, w=2.9):
    stage, etype, _, ln, frag, _ = TRAIL[i]
    x = STAGE_X[i]
    frame = Rectangle(width=w, height=.9, stroke_color=INK, stroke_width=2, fill_color=PAPER,
                      fill_opacity=1).move_to([x, y, 0])
    bar = Rectangle(width=w, height=.07, stroke_width=0, fill_color=RED,
                    fill_opacity=1).move_to([x, frame.get_top()[1] - .035, 0])
    lx = x - w / 2 + .18
    g = VGroup(frame, bar, mono_line(etype, lx, y + .2, 19, RED, bold=True),
               mono_line(frag, lx, y - .05, 16), mono_line(f"line {ln}", lx, y - .29, 16, GRAY))
    g.set_z_index(3)
    return g


def message_line(i, y=.05, x=-6.2):
    _, etype, msg, *_ = TRAIL[i]
    a = mono_line(etype + ":", x, y, 17, RED, bold=True)
    b = mono_line(msg, x + ADVANCE * 17 * (len(etype) + 2), y, 17)
    return VGroup(a, b)


def trail_panel(i, top=-.2):
    return panel_at(TRAIL[i][5], CORE_PATH, -1.95, top, 8.6, 17)


class S03(Ep):
    def construct(self):
        self.header()
        ty = 1.86
        track = line(-6.2, ty, 6.2, ty, INK, 2)
        stops = VGroup(*[line(x, ty - .1, x, ty + .1, INK, 2) for x in STAGE_X])
        labels = VGroup(*[mono_line(s, x - ADVANCE * 18 * len(s) / 2, 1.6, 18, GRAY)
                          for x, s in zip(STAGE_X, STAGES)])
        add = VGroup(pill("IdentityModel", -1.6, .75, GRAY, 20), pill("+ scGenModel", 1.6, .75, RED, 20))
        with self.say(0) as vo:
            self.cue(vo, .02, Create(track), FadeIn(stops), FadeIn(labels), run_time=.5)
            vo.wait_until("add scGen")
            self.play(FadeIn(add[0]), FadeIn(add[1], shift=LEFT * .2), run_time=.4)
            vo.wait_until("Pause")
            card = ponder("加上 scGen 继续跑：哪个阶段最先坏？",
                          "Add scGen and keep running: which stage breaks first?", y=-.95)
            self.play(self.veil(), run_time=.4)
            self.play(FadeIn(card, shift=UP * .1), run_time=.4)
        self.hold(0)
        big = VGroup(source_tag("MEASURED"),
                     label("toy data · stand-in scgen · smallest patch per stage", 22, GRAY))
        big.arrange(RIGHT, buff=.25).move_to([0, -.55, 0])
        token = Dot([-6.2, ty, 0], radius=.1, color=RED).set_z_index(5)
        xs = [cross(x, ty, .11).set_z_index(4) for x in STAGE_X]
        dock = VGroup(source_tag("MEASURED"), label("toy data · stand-in scgen", 17, GRAY),
                      label("smallest patch per stage", 17, GRAY))
        for m, y in zip(dock, (-1.62, -1.98, -2.3)):
            m.move_to([2.7 + m.width / 2, y, 0])
        numbered = VGroup(*[mono_line(f"{k + 1} · {s}", x - ADVANCE * 18 * (len(s) + 4) / 2, 1.6,
                                      18) for k, (x, s) in enumerate(zip(STAGE_X, STAGES))])
        with self.say(1) as vo:
            self.cue(vo, .0, FadeOut(card), FadeOut(add), self.unveil(), run_time=.4)
            vo.wait_until("toy data")
            self.play(FadeIn(big, shift=UP * .1), run_time=.5)
            vo.wait_until("patching only")
            self.add(token)
            for k, x in enumerate(STAGE_X):
                self.play(token.animate.move_to([x, ty, 0]), run_time=.32)
                self.play(Create(xs[k]), run_time=.18)
                self.play(xs[k].animate.set_color(GRAY), run_time=.18)
            self.play(token.animate.move_to([6.2, ty, 0]), run_time=.25)
            self.remove(token)
            vo.wait_until("Here's the trail")
            self.play(*[x_.animate.set_color(RED) for x_ in xs],
                      ReplacementTransform(labels, numbered), ReplacementTransform(big, dock),
                      run_time=.7)

        cards = [trail_card(i) for i in range(4)]
        for c in cards:
            c.shift(RIGHT * (8.3 - c.get_x()))

        def slide(i):
            return cards[i].animate.move_to([STAGE_X[i], .98, 0])

        with self.say(2) as vo:
            self.cue(vo, .0, slide(0), numbered[0].animate.set_color(RED), run_time=.8)
            msg = message_line(0)
            vo.wait_until("attribute error")
            self.play(FadeIn(msg, shift=UP * .08), run_time=.4)
            panel = trail_panel(0)
            vo.wait_until("x_dimensions")
            self.play(FadeIn(panel), run_time=.4)
            vo.wait_until("line 253")
            m = highlight(self, panel, 253, run_time=.35)
            note = VGroup(label("→ episode 2", 22, INK, bold=True),
                          label("one name, five places", 18, GRAY)).arrange(DOWN, aligned_edge=LEFT,
                                                                            buff=.12)
            note.move_to([2.7 + note.width / 2, -.55, 0])
            vo.wait_until("That was")
            self.play(FadeIn(note, shift=LEFT * .1), run_time=.4)
            vo.wait_until("Train:")
            msg2, panel2 = message_line(1), trail_panel(1)
            self.play(slide(1), numbered[0].animate.set_color(INK), numbered[1].animate.set_color(RED),
                      FadeOut(m), FadeOut(note), ReplacementTransform(msg, msg2),
                      FadeOut(panel), FadeIn(panel2), run_time=.8)
            vo.wait_until("missing its training")
            m = highlight(self, panel2, 261, run_time=.35)
            n1 = label("needs training_data", 18, INK).move_to([2.7, -.4, 0], aligned_edge=LEFT)
            self.play(FadeIn(n1), run_time=.3)
            vo.wait_until("because line 133")
            m2 = panel2.mark(133)
            n2 = label("line 133 passes nothing", 18, RED).move_to([2.7, -.8, 0], aligned_edge=LEFT)
            self.play(ReplacementTransform(m, m2), FadeIn(n2), run_time=.4)
        with self.say(3) as vo:
            msg3, panel3 = message_line(2), trail_panel(2)
            self.cue(vo, .0, slide(2), numbered[1].animate.set_color(INK),
                     numbered[2].animate.set_color(RED), FadeOut(m2), FadeOut(n1), FadeOut(n2),
                     ReplacementTransform(msg2, msg3), FadeOut(panel2), FadeIn(panel3), run_time=.8)
            vo.wait_until("line 288")
            m = highlight(self, panel3, 288, run_time=.35)
            vo.wait_until("a helper")
            m2 = panel3.mark(262)
            n1 = label("_dense lives inside train", 18, INK).move_to([2.7, -.4, 0], aligned_edge=LEFT)
            self.play(ReplacementTransform(m, m2), FadeIn(n1), run_time=.4)
            vo.wait_until("can't see")
            m3 = panel3.mark(288)
            n2 = label("predict can't see it", 18, RED).move_to([2.7, -.8, 0], aligned_edge=LEFT)
            self.play(ReplacementTransform(m2, m3), FadeIn(n2), run_time=.4)
            vo.wait_until("Evaluate:")
            msg4, panel4 = message_line(3, y=-.3), trail_panel(3, top=-.55)
            run4 = VGroup(left("identity run ·", STAGE_X[3] - 1.4, .3, 17, GRAY),
                          left("5 mouse vs 7 human cells", STAGE_X[3] - 1.4, .07, 17, GRAY))
            self.play(slide(3), numbered[2].animate.set_color(INK), numbered[3].animate.set_color(RED),
                      FadeOut(m3), FadeOut(n1), FadeOut(n2), ReplacementTransform(msg3, msg4),
                      FadeOut(panel3), FadeIn(panel4), run_time=.8)
            self.play(FadeIn(run4), run_time=.3)
            x0d, my, hy, dx = 2.95, -.8, -1.2, .27
            mouse = VGroup(*[Dot([x0d + k * dx, my, 0], radius=.055, color=INK) for k in range(5)])
            human = VGroup(*[Dot([x0d + k * dx, hy, 0], radius=.055, color=INK) for k in range(7)])
            ml = label("5 mouse", 17, GRAY).next_to(mouse, RIGHT, buff=.2)
            hl = label("7 human", 17, GRAY).next_to(human, RIGHT, buff=.2)
            vo.wait_until("different cell counts")
            self.play(FadeIn(mouse), FadeIn(human), FadeIn(ml), FadeIn(hl), run_time=.5)
            vo.wait_until("line them up")
            pairs = VGroup(*[line(x0d + k * dx, my - .07, x0d + k * dx, hy + .07, GRAY, 2)
                             for k in range(5)])
            self.play(LaggedStart(*[Create(p) for p in pairs], lag_ratio=.15),
                      human[5:].animate.set_color(RED), run_time=.6)
            vo.wait_until("at line 313")
            m = highlight(self, panel4, 313, run_time=.35)
        rows_y = [-.5, -.92, -1.34, -1.88]
        board = Rectangle(width=8.8, height=2.67, stroke_color=INK, stroke_width=2).move_to(
            [-1.8, -1.085, 0])
        head = left("TO-DO · 待办", -5.95, -.08, 22, INK, bold=True)
        sep = DashedLine([-6.05, -1.62, 0], [2.45, -1.62, 0], color=GRAY, dash_length=.08)
        todo = []
        for k, (stage, etype, _, ln, *_r) in enumerate(TRAIL):
            box = Square(.26, stroke_color=INK, stroke_width=2).move_to([-5.62, rows_y[k], 0])
            num = mono(str(k + 1), 20, RED, bold=True).move_to([-5.18, rows_y[k], 0])
            txt = mono_left(f"{stage:<9}{etype:<14} line {ln}", -4.85, rows_y[k], 19)
            todo.append(VGroup(box, num, txt))
        # scGen's path: the three stops it hits, in program order
        path = VGroup(Line([-5.98, rows_y[0], 0], [-5.98, rows_y[2] + .06, 0], color=RED,
                           stroke_width=4),
                      *[Dot([-5.98, y, 0], radius=.06, color=RED) for y in rows_y[:3]],
                      Triangle(color=RED, fill_color=RED, fill_opacity=1, stroke_width=0)
                      .scale(.07).rotate(PI).move_to([-5.98, rows_y[2] - .02, 0]))
        p_lab = VGroup(label("scGen's path", 22, RED, bold=True),
                       mono("253 → 133 → 288", 19, RED)).arrange(DOWN, aligned_edge=LEFT, buff=.1)
        p_lab.move_to([2.75 + p_lab.width / 2, -.62, 0])
        idn = left("identity run · fixed by R² of means (E5 · s05)", -4.85, -2.2, 17, GRAY)
        choose = left("you choose which path first", 2.75, -1.2, 19, INK)
        with self.say(4) as vo:
            self.cue(vo, .0, FadeOut(m), FadeOut(panel4), FadeOut(msg4), FadeOut(mouse),
                     FadeOut(human), FadeOut(ml), FadeOut(hl), FadeOut(pairs),
                     FadeOut(run4),
                     numbered[3].animate.set_color(INK), run_time=.4)
            self.play(Create(board), FadeIn(head), Create(sep), run_time=.4)
            self.play(LaggedStart(*[ReplacementTransform(cards[k], todo[k]) for k in range(4)],
                                  lag_ratio=.3), run_time=1.4)
            vo.wait_until("Along scGen's path")
            self.play(Create(path), FadeIn(p_lab, shift=LEFT * .1), run_time=.6)
            vo.wait_until("hands you the order")
            self.play(LaggedStart(*[Indicate(t[1], color=RED, scale_factor=1.4) for t in todo[:3]],
                                  lag_ratio=.2), run_time=.8)
            vo.wait_until("You only choose")
            self.play(FadeIn(idn, shift=UP * .05), FadeIn(choose, shift=LEFT * .1), run_time=.5)
        self.finish()



# ---------------------------------------------------------------- s04

GENES = [  # (row label, genes, evidence shown under the bar, READ IN NOTEBOOK)
    ("mouse train", 18024, "Tests/e24_replica.ipynb   'x_dimensions': 18024"),
    ("human train", 61759, "Tests/e24_replica.ipynb   n_obs × n_vars = 58931 × 61759"),
    ("test files", 1000, "e22_batch_correction.ipynb   n_obs=251, n_vars=1000"),
]
# the notebook text on screen must stay verbatim (Josh's e24_replica.ipynb outputs, cells 3 and 6)
assert "'x_dimensions': 18024" in E24_OUTPUTS[3]
assert "n_obs × n_vars = 58931 × 61759" in E24_OUTPUTS[6]
SLOTS = [("train · mouse", "source_training_data_path"), ("train · human", "target_training_data_path"),
         ("test · mouse", "source_test_data_path"), ("test · human", "target_test_data_path")]


class S04(Ep):
    def construct(self):
        self.header()
        x0, scale, rows_y = -3.6, 9.4 / 61759, [1.6, .72, -.16]
        names, bars, vals, evid = VGroup(), VGroup(), VGroup(), VGroup()
        for (name, n, ev), y in zip(GENES, rows_y):
            names.add(left(name, -6.2, y, 22, INK))
            bars.add(Rectangle(width=n * scale, height=.3, stroke_width=0, fill_color=INK,
                               fill_opacity=1).move_to([x0 + n * scale / 2, y, 0]))
            evid.add(mono_left(ev, x0, y - .33, 16, GRAY))
        vals.add(mono(f"{GENES[0][1]:,} genes", 20).next_to(bars[0], RIGHT, buff=.15))
        vals.add(mono(f"{GENES[1][1]:,} genes", 20, PAPER).move_to(bars[1]).align_to(bars[1], RIGHT)
                 .shift(LEFT * .12).set_z_index(2))
        vals.add(mono(f"{GENES[2][1]:,} genes", 20, RED).next_to(bars[2], RIGHT, buff=.15))
        tag = tagline("READ IN NOTEBOOK", "recorded outputs", -6.2, -.95, 17)
        with self.say(0) as vo:
            vo.wait_until("Josh's notebook")
            self.play(FadeIn(tag), run_time=.4)
            for k, w in enumerate(["mouse training", "human one", "The test files"]):
                vo.wait_until(w)
                self.play(FadeIn(names[k]), GrowFromEdge(bars[k], LEFT), FadeIn(evid[k]),
                          run_time=.8 if k == 1 else .5)
                self.play(FadeIn(vals[k]), run_time=.3)
        # L1: one network input (Josh's line 104 sets x_dimensions from the mouse file)
        cut = x0 + GENES[0][1] * scale
        gate = DashedLine([cut, 1.95, 0], [cut, -.45, 0], color=RED, dash_length=.08)
        gate_lab = left("one network input", cut + .12, 1.95, 18, RED)
        gate_why = left("sized by the mouse file (core line 104)", cut + .15, rows_y[0], 17, GRAY)
        over = Rectangle(width=x0 + GENES[1][1] * scale - cut, height=.3, stroke_width=0,
                         fill_color=RED, fill_opacity=1).move_to([(cut + x0 + 9.4) / 2, rows_y[1], 0])
        t_end = x0 + GENES[2][1] * scale
        short = DashedVMobject(Rectangle(width=cut - t_end, height=.3, color=RED, stroke_width=2.5),
                               num_dashes=36).move_to([(cut + t_end) / 2, rows_y[2], 0])
        shared_w = GENES[2][1] * scale          # the shared 1,000 genes, at the same scale
        shared = VGroup(*[Rectangle(width=shared_w, height=.3, stroke_width=0, fill_color=RED,
                                    fill_opacity=1).move_to([x0 + shared_w / 2, y, 0])
                          for y in rows_y]).set_z_index(2)
        axis_lab = VGroup(label("one gene axis: the shared 1,000", 24, RED, bold=True),
                          label("orthologous HVGs · 同一个基因轴", 18, GRAY))\
            .arrange(DOWN, aligned_edge=LEFT, buff=.08).move_to([x0 + shared_w + .35, .72, 0],
                                                                aligned_edge=LEFT)
        data_cls = VGroup(pill("TrainingData", -4.75, -1.75, INK, 20), pill("TestData", -2.0, -1.75, INK, 20))
        cls_note = mono_left(f"{CORE_PATH}  20–33", -6.2, -2.3, 16, GRAY)
        slot = DashedVMobject(Rectangle(width=3.9, height=.62, color=RED), num_dashes=48)\
            .move_to([1.55, -1.75, 0])
        slot_lab = at("gene alignment · 对齐基因", 1.55, -1.75, 18, RED)
        inf = source_tag("INFERRED").move_to([3.8, -1.75, 0], aligned_edge=LEFT)
        with self.say(1) as vo:
            self.cue(vo, .0, FadeOut(evid), FadeOut(tag), FadeOut(vals), Create(gate), FadeIn(gate_lab),
                     FadeIn(gate_why), run_time=.5)
            self.add(over)
            self.play(FadeIn(over), Create(short), run_time=.5)
            vo.wait_until("share one gene axis")
            self.play(FadeIn(shared), FadeOut(over), FadeOut(short), FadeOut(gate), FadeOut(gate_lab),
                      FadeOut(gate_why), run_time=.5)
            self.play(*[b.animate.stretch_to_fit_width(shared_w).align_to([x0, 0, 0], LEFT) for b in bars],
                      run_time=.8)
            self.play(FadeIn(axis_lab, shift=LEFT * .1), run_time=.4)
            vo.wait_until("Lining up genes")
            self.play(FadeIn(data_cls, shift=UP * .1), FadeIn(cls_note), run_time=.5)
            vo.wait_until("next to the data")
            self.play(Create(slot), FadeIn(slot_lab), FadeIn(inf), run_time=.6)
        # L2: the M1 v08 file is one table + a split recipe; the data classes take four files
        tx0, tx1, ty0, ty1 = -6.2, -4.0, -1.55, 1.45
        table = Rectangle(width=tx1 - tx0, height=ty1 - ty0, stroke_color=INK, stroke_width=2,
                          fill_color=PAPER, fill_opacity=1).move_to([(tx0 + tx1) / 2, (ty0 + ty1) / 2, 0])
        hatch = VGroup(*[line(tx0, y, tx1, y, FAINT, 1) for y in np.linspace(ty0 + .2, ty1 - .2, 14)])
        dims = VGroup(left("~8,054 cells ×", tx0, -1.88, 20, INK))
        dims.add(left("1,000 genes", dims[0].get_right()[0] + .12, -1.88, 20, INK))
        fname = mono_left("hvg_pearson_residuals_m1_v08.h5ad", tx0, 1.85, 16, GRAY)
        t_tag = source_tag("READ IN CODE").move_to([fname.get_right()[0] + .2, 1.85, 0],
                                                   aligned_edge=LEFT)
        recipe = panel_at([(n, SPEC[n]) for n in (23, 24, 25, 26)] + [(None, "…")] +
                          [(n, SPEC[n]) for n in (28, 29, 30, 31)], SPEC_PATH, -.95, 1.6, 5.4, 16)
        slots = VGroup()
        for k, (a, b) in enumerate(SLOTS):
            y = 1.3 - k * .86
            box = Rectangle(width=4.2, height=.72, stroke_color=INK, stroke_width=2).move_to([4.15, y, 0])
            slots.add(VGroup(box, left(a, 2.22, y + .14, 19, INK, bold=True),
                             mono_left(b, 2.22, y - .17, 16, GRAY)))
        s_head = left("TrainingData · TestData: four paths", 2.05, 1.95, 17, GRAY)
        mid = (ty0 + ty1) / 2
        bands = VGroup(*[Rectangle(width=tx1 - tx0, height=.32, stroke_width=0, fill_color=RED,
                                   fill_opacity=.85).move_to([(tx0 + tx1) / 2, y, 0])
                         for y in (mid + .45, ty0 + .45)])
        divider = DashedLine([tx0, mid, 0], [tx1, mid, 0], color=INK, dash_length=.1)
        sp_lab = VGroup(at("mouse", (tx0 + tx1) / 2, ty1 - .3, 18, GRAY), at("human", (tx0 + tx1) / 2, mid - .3, 18, GRAY))
        card2 = VGroup(left("CARD 2", -6.2, -2.3, 20, RED, bold=True),
                       left("split the table into four files", -5.1, -2.3, 20, INK, bold=True))
        c_tag = source_tag("INFERRED").next_to(card2, RIGHT, buff=.25)
        done = tick(-.17, -1.75, .15, RED)
        done_lab = at("done in M1 v08", 1.55, -2.27, 18, RED, bold=True)
        with self.say(2) as vo:
            vo.wait_until("already done")
            self.play(Create(done), FadeIn(done_lab, shift=UP * .05), run_time=.4)
            vo.wait_until("The M1")
            self.play(FadeOut(data_cls), FadeOut(cls_note), FadeOut(slot), FadeOut(slot_lab),
                      FadeOut(inf), FadeOut(done), FadeOut(done_lab), FadeOut(names), FadeOut(axis_lab),
                      FadeOut(shared), ReplacementTransform(bars, VGroup(table, hatch)), run_time=.7)
            self.play(FadeIn(dims), FadeIn(fname), FadeIn(t_tag), run_time=.4)
            vo.wait_until("a thousand genes")
            top_edge = line(tx0, ty1, tx1, ty1, RED, 5)
            self.play(Create(top_edge), dims[1].animate.set_color(RED), run_time=.5)
            vo.wait_until("split recipe")
            self.play(FadeIn(recipe, shift=UP * .1), FadeOut(top_edge), dims[1].animate.set_color(INK),
                      run_time=.5)
            vo.wait_until("four files")
            self.play(FadeIn(s_head), LaggedStart(*[FadeIn(sl, shift=LEFT * .1) for sl in slots],
                                                  lag_ratio=.2), run_time=.9)
            vo.wait_until("So the real card")
            m = highlight(self, recipe, 23, 24, run_time=.3)
            self.play(Create(divider), FadeIn(sp_lab), run_time=.5)
            m2 = recipe.mark(25, 26, 28, 30)
            self.play(ReplacementTransform(m, m2), FadeIn(bands), run_time=.5)
            vo.wait_until("training and test")
            parts = [Rectangle(width=tx1 - tx0, height=.5, stroke_width=0, fill_color=c,
                               fill_opacity=1).set_z_index(4)
                     .move_to([(tx0 + tx1) / 2, y, 0])
                     for c, y in ((INK, ty1 - .7), (INK, mid - .7), (RED, mid + .45), (RED, ty0 + .45))]
            self.add(*parts)
            self.play(*[pc.animate.stretch_to_fit_width(.4).stretch_to_fit_height(.42)
                        .move_to([5.97, slots[k][0].get_y(), 0]) for k, pc in enumerate(parts)],
                      run_time=1.0)
            vo.wait_until("mouse and human")
            self.play(FadeOut(m2), FadeIn(card2), FadeIn(c_tag), run_time=.4)
        self.finish()


# ---------------------------------------------------------------- s05

CSV4 = "m1 v08 IMPACT,0.9188,0.1035,…,0.5542,…"  # v08_scorecard_dual.csv line 4, columns elided
CLUSTER_RUN = "cluster: cellot_gpu/results/hvg_pearson_residuals_m1_v08_ood/scgen/"


def scorecard(rows_):
    """The scorecard panel (header line 1 plus the given rows), top at y = 2.0."""
    return panel_at([(1, "model,R2,MMD,…,r2_identity,…")] + rows_, CARD_PATH, -2.1, 2.0, 8.2, 17)


class S05(Ep):
    def construct(self):
        self.header()
        grid = tiles(0, .82, h=.28)
        with self.say(0) as vo:
            self.cue(vo, .0, LaggedStart(*[FadeIn(t, scale=.6) for t in grid], lag_ratio=.01),
                     run_time=.7)
            card = ponder("八十三个 notebook，先复现哪一个？为什么？",
                          "83 notebooks: which would you replicate first, and why?", y=-1.35)
            self.play(self.veil(), run_time=.3)
            self.play(FadeIn(card, shift=UP * .1), run_time=.4)
        self.hold(0)
        self.remove(*grid)
        self.add(grid)                      # one mobject from here on (no stray wrapper groups)
        # L1: not a notebook: a spec and a scorecard row
        g_strike = Line(grid.get_corner(DL) + LEFT * .1, grid.get_corner(UR) + RIGHT * .1, color=RED,
                        stroke_width=5)
        answer = VGroup(label("not a notebook", 28, GRAY), label("→  a spec + a scorecard row", 28, RED,
                                                                 bold=True)).arrange(RIGHT, buff=.3)
        answer.move_to([0, -.55, 0])
        quote = VGroup(label("“model-version comparisons are made on the v08 OOD cuts”", 21, INK),
                       tagline("READ IN CODE", "speciesOT · AGENTS.md, line 41 (the frozen benchmark)",
                               0, 0, 17))
        quote.arrange(DOWN, buff=.15).move_to([0, -1.35, 0])
        m1 = VGroup(label("M1 v08 · OOD", 30, RED, bold=True),
                    label("holdout CL:0000875 · non-classical monocytes", 21, GRAY))
        m1.arrange(RIGHT, buff=.35).move_to([0, -2.17, 0])
        spec_rows = [(1, "experiment_tag: …_m1_v08_ood"),
                     (4, "data_file: …/hvg_pearson_residuals_m1_v08.h5ad")] + \
                    [(n, SPEC[n]) for n in (25, 26, 28, 31, 32, 33, 34, 35)]
        spec = panel_at(spec_rows, SPEC_PATH, -2.75, 1.95, 7.0, 16)
        core_rows = rows(CORE, 162, 166) + [(None, "…"), (212, CORE[212])]
        core = panel_at(core_rows, CORE_PATH, 3.6, 1.95 - 5 * spec.gap, 5.3, 16)
        pasted = VGroup(label("pasted · 粘贴", 22, RED, bold=True),
                        label("same settings, as comments", 18, GRAY)).arrange(DOWN, aligned_edge=LEFT,
                                                                              buff=.1)
        pasted.move_to([.95, 1.5, 0], aligned_edge=LEFT)
        with self.say(1) as vo:
            self.cue(vo, .0, FadeOut(card), self.unveil(), run_time=.35)
            self.play(Create(g_strike), grid.animate.set_opacity(.3), FadeIn(answer[0]), run_time=.5)
            self.play(FadeIn(answer[1], shift=LEFT * .1), run_time=.4)
            vo.wait_until("frozen benchmark")
            self.play(FadeIn(quote, shift=UP * .1), run_time=.5)
            vo.wait_until("M1, version eight")
            self.play(FadeIn(m1[0], shift=UP * .1), run_time=.4)
            vo.wait_until("holding out")
            self.play(FadeIn(m1[1]), run_time=.4)
            vo.wait_until("Its spec")
            self.play(FadeOut(grid), FadeOut(g_strike), FadeOut(quote), FadeOut(m1), FadeOut(answer),
                      FadeIn(spec, shift=UP * .1), run_time=.7)
            vo.wait_until("pasted its model")
            self.play(FadeIn(core, shift=LEFT * .1), FadeIn(pasted), run_time=.5)
            ms = highlight(self, spec, 31, 32, 33, 34, 35, run_time=.3)
            mc = highlight(self, core, 162, 163, 164, 165, 166, run_time=.3)
            vo.wait_until("a little above")
            mk = highlight(self, core, 212, run_time=.35)
        # L2 phase A: the scorecard row, its notebook, the first golden number, same on every row
        csv2 = scorecard([(5, CSV5)])
        csv3 = scorecard([(4, CSV4), (5, CSV5)])
        written = VGroup(label("written by", 17, GRAY),
                         mono("speciesOT/baseline/analysis/22_v08_results.ipynb", 16, GRAY),
                         label("(cell 3)", 17, GRAY)).arrange(RIGHT, buff=.14)
        written.move_to([-6.2 + written.width / 2, .17, 0])
        nb_path = source_tag("READ IN NOTEBOOK")
        nb_path.move_to([-6.2 + nb_path.width / 2, -.2, 0])
        gold = mono("0.5542", 64, RED, bold=True).move_to([4.35, 1.5, 0])
        gold_lab = VGroup(label("identity · R² of means", 20, INK),
                          label("均值 R²", 18, GRAY)).arrange(DOWN, buff=.06).move_to([4.35, .68, 0])
        ident = VGroup(label("r2_identity identical", 20, RED, bold=True),
                       label("→ it describes the data", 20, INK)).arrange(DOWN, aligned_edge=LEFT, buff=.1)
        ident.move_to([2.6 + ident.width / 2, -.05, 0])
        # phase B: how it is computed; what control and treated are
        metr = panel_at([(n, METRICS[n]) for n in (154, 155, 156, 157)] +
                        [(None, "    …"), (166, "    r2_identity = _r2_means(control, treated) if …")],
                        METRICS_PATH, -2.0, 2.0, 8.4, 16)
        ctl = left("control = mouse test cells: what IdentityModel returns (line 159)", -6.2, -.62, 18,
                   INK)
        trt = left("treated = human test cells", -6.2, -.95, 18, INK)
        checks = ["same file", "same split", "R² of means"]
        cl = VGroup()
        for k, c in enumerate(checks):
            y = .05 - k * .5
            cl.add(VGroup(Square(.3, stroke_color=INK, stroke_width=2).move_to([2.85, y, 0]),
                          left(c, 3.2, y, 21, INK)))
        cticks = [tick(2.87, .05 - k * .5, .13, RED) for k in range(3)]
        result = VGroup(label("→ reproduce 0.5542", 22, RED, bold=True),
                        label("almost exactly · 几乎精确", 18, GRAY)).arrange(DOWN, aligned_edge=LEFT,
                                                                           buff=.08)
        result.move_to([2.7, -1.6, 0], aligned_edge=LEFT)
        # phase C: means, not cells, also removes the line-313 crash
        c313 = trail_card(3, y=-1.85, w=2.8).move_to([-4.75, -1.85, 0])
        no313 = VGroup(label("means, not cells", 22, RED, bold=True),
                       label("→ no line-313 crash", 22, RED, bold=True)).arrange(DOWN, aligned_edge=LEFT,
                                                                                 buff=.08)
        no313.move_to([-2.65, -1.85, 0], aligned_edge=LEFT)
        with self.say(2) as vo:
            self.cue(vo, .0, FadeOut(spec), FadeOut(core), FadeOut(pasted), FadeOut(ms), FadeOut(mc),
                     FadeOut(mk), run_time=.4)
            self.play(FadeIn(csv2, shift=DOWN * .1), run_time=.5)
            vo.wait_until("written by")
            self.play(FadeIn(written), FadeIn(nb_path), run_time=.4)
            vo.wait_until("The identity")
            m5 = highlight(self, csv2, 5, run_time=.3)
            self.play(TransformFromCopy(glyphs(csv2.row(5), CSV5, "0.5542"), gold), FadeIn(gold_lab),
                      run_time=.8)
            vo.wait_until("same on every")
            self.play(FadeOut(m5), ReplacementTransform(csv2, csv3), run_time=.6)
            boxes = VGroup(*[SurroundingRectangle(glyphs(csv3.row(n), t, "0.5542"), color=RED, buff=.05,
                                                  stroke_width=2.5) for n, t in ((4, CSV4), (5, CSV5))])
            self.play(Create(boxes), FadeIn(ident[0], shift=LEFT * .1), run_time=.5)
            vo.wait_until("describes the data")
            self.play(FadeIn(ident[1], shift=LEFT * .1), run_time=.4)
            vo.wait_until("mouse test cells")
            self.play(FadeOut(csv3), FadeOut(boxes), FadeOut(written), FadeOut(nb_path),
                      FadeIn(metr, shift=UP * .1), run_time=.5)
            mm = highlight(self, metr, 166, run_time=.25)
            self.play(FadeIn(ctl, shift=UP * .05), run_time=.35)
            vo.wait_until("against human")
            self.play(FadeIn(trt, shift=UP * .05), run_time=.35)
            vo.wait_until("No training")
            self.play(Indicate(metr.row(166), color=RED, scale_factor=1.03), run_time=.5)
            vo.wait_until("no sampling")
            mm2 = metr.mark(155)
            self.play(ReplacementTransform(mm, mm2), run_time=.3)
            vo.wait_until("so once")
            self.play(FadeOut(ident), FadeIn(cl), run_time=.4)
            for k, w in enumerate(["same file", "split,", "computes R squared"]):
                vo.wait_until(w)
                self.play(Create(cticks[k]), run_time=.25)
            vo.wait_until("reproduce it")
            self.play(FadeIn(result, shift=RIGHT * .1), run_time=.4)
            vo.wait_until("Comparing means")
            self.play(FadeIn(c313, shift=UP * .1), Indicate(metr.row(155), color=RED, scale_factor=1.03),
                      run_time=.6)
            vo.wait_until("removes the crash")
            st313 = strike(c313, RED, 5)
            link = Arrow(c313.get_right(), no313.get_left(), buff=.1, color=RED, stroke_width=3,
                         max_tip_length_to_length_ratio=.3)
            self.play(Create(st313), GrowArrow(link), FadeIn(no313, shift=LEFT * .1), run_time=.6)
        # L3: scGen's number, where its run lives, 80-cell sampling, and what not to trace
        csv3b = scorecard([(4, CSV4), (5, CSV5)])
        steps = VGroup()
        for k, (x0, h) in enumerate(((-6.2, .5), (-4.25, 1.0), (-2.3, 1.5))):
            steps.add(Rectangle(width=1.85, height=h, stroke_width=0, fill_color=INK if k < 2 else RED,
                                fill_opacity=1).move_to([x0 + .925, -2.35 + h / 2, 0]))
        s_txt = VGroup(at("data", -5.275, -2.1, 20, PAPER, bold=True),
                       at("identity", -3.325, -2.05, 20, PAPER, bold=True),
                       mono("0.5542", 19, PAPER).move_to([-3.325, -1.62, 0]),
                       at("scGen", -1.375, -1.75, 20, PAPER, bold=True),
                       mono("0.927", 19, PAPER).move_to([-1.375, -1.3, 0])).set_z_index(3)
        s_cap = VGroup(at("file + split", -5.275, -1.62, 17, GRAY),
                       VGroup(at("≈ exact", -3.325, -.9, 17, GRAY),
                              at("(no training)", -3.325, -1.14, 17, GRAY)),
                       at("± tolerance", -1.375, -.62, 17, RED))
        run_chip = pill(CLUSTER_RUN, 0, .08, INK, 16)
        run_tag = source_tag("READ IN NOTEBOOK")
        VGroup(run_chip, run_tag).arrange(RIGHT, buff=.2).move_to([0, .08, 0]).align_to([-6.2, 0, 0], LEFT)
        run_src = left("22_v08_results.ipynb · cell 1 (MODELS)", -6.2, -.3, 17, GRAY)
        adapter = VGroup(label("your adapter wraps that model", 20, INK, bold=True), source_tag("INFERRED"))\
            .arrange(RIGHT, buff=.2)
        adapter.move_to([.25 + adapter.width / 2, -.55, 0])
        rng = np.random.default_rng(5)
        pts = np.clip(rng.normal(0, 1, size=(200, 2)), -2, 2) * [.45, .32] + [1.5, -1.62]
        dots = VGroup(*[Dot([x, y, 0], radius=.03, color=GRAY) for x, y in pts])
        nl_y, nl0, nl1 = -1.3, 3.3, 6.1
        center = (nl0 + nl1) / 2
        nline = VGroup(line(nl0, nl_y, nl1, nl_y, INK, 2),
                       mono("0.927", 18, INK).move_to([center, nl_y - .35, 0]),
                       at("mean of 80-cell samples", center, -1.98, 17, GRAY))
        ex_tag = source_tag("EXAMPLE").move_to([center, -2.3, 0])
        trace = VGroup(label("only your adapter's calls (E4)", 21, INK, bold=True),
                       label("your scorecard is the check", 21, INK)).arrange(DOWN, aligned_edge=LEFT, buff=.14)
        t_frame = Rectangle(width=5.75, height=1.25, stroke_color=INK, stroke_width=2, fill_color=PAPER,
                            fill_opacity=1).move_to([3.3, -1.7, 0])
        trace.move_to([t_frame.get_left()[0] + .25 + trace.width / 2, -1.7, 0])
        t_tag = source_tag("INFERRED").move_to([t_frame.get_right()[0] - .72, -1.32, 0])
        t_head = left("don't trace all of cellot", t_frame.get_left()[0], -.98 - .02, 18, GRAY)
        with self.say(3) as vo:
            self.cue(vo, .0, FadeOut(metr), FadeOut(mm2), FadeOut(ctl), FadeOut(trt), FadeOut(cl),
                     *[FadeOut(t) for t in cticks], FadeOut(result), FadeOut(c313), FadeOut(st313),
                     FadeOut(link), FadeOut(no313), FadeIn(csv3b), run_time=.45)
            self.play(GrowFromEdge(steps[0], DOWN), GrowFromEdge(steps[1], DOWN), FadeIn(s_txt[:3]),
                      FadeIn(s_cap[:2]), run_time=.5)
            vo.wait_until("zero point nine")
            m5 = highlight(self, csv3b, 5, run_time=.25)
            self.play(GrowFromEdge(steps[2], DOWN), FadeIn(s_txt[3]),
                      TransformFromCopy(glyphs(csv3b.row(5), CSV5, "0.927"), s_txt[4]), run_time=.8)
            vo.wait_until("on the cluster")
            self.play(FadeIn(run_chip, shift=UP * .05), FadeIn(run_tag), FadeIn(run_src), run_time=.5)
            vo.wait_until("To aim for it")
            self.play(FadeIn(adapter, shift=RIGHT * .1), run_time=.5)
            vo.wait_until("It averages")
            self.play(FadeIn(dots), Create(nline[0]), FadeIn(nline[1:]), FadeIn(ex_tag), run_time=.5)
            marks = VGroup()
            for off in (-.32, .22, .05):
                pick = rng.choice(200, 80, replace=False)
                sub = VGroup(*[dots[i] for i in pick])
                mk = line(center + off, nl_y - .14, center + off, nl_y + .14, GRAY, 3)
                self.play(sub.animate.set_color(RED), run_time=.35)
                self.play(sub.animate.set_color(GRAY), Create(mk), run_time=.3)
                marks.add(mk)
            mean = Triangle(color=RED, fill_color=RED, fill_opacity=1).scale(.1).rotate(PI)\
                .move_to([center, nl_y + .3, 0])
            self.play(FadeIn(mean, shift=DOWN * .1), run_time=.3)
            vo.wait_until("aim within")
            band = Rectangle(width=1.3, height=.42, stroke_width=0, fill_color=RED, fill_opacity=.18)\
                .move_to([center, nl_y, 0])
            self.play(FadeIn(band), FadeIn(s_cap[2]), run_time=.5)
            vo.wait_until("And you don't need")
            self.play(*[FadeOut(x) for x in (dots, nline, ex_tag, marks, mean, band)], run_time=.4)
            self.play(FadeIn(t_frame), FadeIn(trace[0]), FadeIn(t_tag), FadeIn(t_head), run_time=.5)
            vo.wait_until("Your own scorecard")
            self.play(FadeIn(trace[1].set_color(RED)), Indicate(csv3b.row(5), color=RED, scale_factor=1.02),
                      run_time=.6)
        self.finish()


# ---------------------------------------------------------------- s06

PRINCIPLES = [("S", "Single responsibility", "单一职责"), ("O", "Open–closed", "开闭原则"),
              ("L", "Liskov substitution", "里氏替换"), ("I", "Interface segregation", "接口隔离"),
              ("D", "Dependency inversion", "依赖倒置")]
SPOTS = {"S": [(20, 33)], "O": [(107, 115)], "L": [(43, 43), (133, 133), (155, 155)],
         "I": [(54, 57)], "D": [(248, 248)]}       # where each letter points (INFERRED mapping)


def barcode(x0=-6.0, x1=6.0, base=-2.3, hscale=.0095, hmax=1.7):
    """speciesot_core.py on its side: one hairline per line, height ~ characters."""
    n = len(LINE_LENGTHS)
    dx = (x1 - x0) / n
    g = VGroup(*[Line([x0 + (i + .5) * dx, base, 0], [x0 + (i + .5) * dx, base + min(ln * hscale, hmax), 0],
                      stroke_width=1.6, color=FAINT if k == "c" else GRAY)
                 for i, (ln, k) in enumerate(zip(LINE_LENGTHS, LINE_KINDS)) if ln])
    g.x_of = lambda line_no: x0 + (line_no - .5) * dx
    g.dx = dx
    return g


class S06(Ep):
    def construct(self):
        self.header()
        ly = 1.72
        letters = VGroup(*[at(c, -5.95 + k * .6, ly, 40, INK, bold=True)
                           for k, (c, *_r) in enumerate(PRINCIPLES)])
        tag = source_tag("INFERRED").move_to([5.6, ly, 0])
        names = []
        for c, en, zh in PRINCIPLES:
            a = left(en, -3.0, ly, 26, INK, bold=True)
            names.append(VGroup(a, left(zh, a.get_right()[0] + .25, ly, 20, GRAY)))

        def focus(k, *extra, run_time=.5):
            anims = [letters[j].animate.set_color(RED if j == k else GRAY) for j in range(5)]
            return self.play(*anims, *extra, run_time=run_time)

        # L0: a compass, not a checklist; each letter points at a spot in the file
        comp_c = (-2.6, -.55)
        dial = Circle(radius=.95, color=INK, stroke_width=2.5).move_to([*comp_c, 0])
        needle = VGroup(Polygon([0, .85, 0], [-.11, 0, 0], [.11, 0, 0], color=RED, fill_color=RED,
                                fill_opacity=1, stroke_width=0),
                        Polygon([0, -.85, 0], [-.11, 0, 0], [.11, 0, 0], color=INK, fill_color=PAPER,
                                fill_opacity=1, stroke_width=2)).move_to([*comp_c, 0])
        comp_lab = at("a compass: when something hurts", comp_c[0], -1.85, 20, INK)
        boxes = VGroup(*[VGroup(Square(.32, stroke_color=GRAY, stroke_width=2).move_to([2.0, .3 - k * .45, 0]),
                                left(c, 2.35, .3 - k * .45, 20, GRAY, bold=True))
                         for k, (c, *_r) in enumerate(PRINCIPLES)])
        no_check = at("not a day-one checklist", 2.6, -2.05, 20, GRAY)
        code = barcode()
        bands, drops, srcs = VGroup(), VGroup(), []
        for k, (c, *_r) in enumerate(PRINCIPLES):
            for a, b in SPOTS[c]:
                srcs.append(letters[k])
                xc = (code.x_of(a) + code.x_of(b)) / 2
                bands.add(Rectangle(width=max(code.dx * (b - a + 1), .07), height=1.85, stroke_width=0,
                                    fill_color=RED, fill_opacity=.22).move_to([xc, -2.3 + .925, 0]))
                drops.add(at(c, xc, -.2, 26, RED, bold=True))
        f_lab = mono_left(CORE_PATH, -6.0, .25, 16, GRAY)
        with self.say(0) as vo:
            self.cue(vo, .02, LaggedStart(*[FadeIn(l, shift=DOWN * .1) for l in letters], lag_ratio=.15),
                     FadeIn(tag), run_time=.8)
            vo.wait_until("compass")
            self.play(Create(dial), FadeIn(needle), FadeIn(comp_lab), run_time=.5)
            self.play(Rotate(needle, -PI / 3, about_point=[*comp_c, 0]), run_time=.4)
            self.play(Rotate(needle, PI / 3 + PI / 8, about_point=[*comp_c, 0]), run_time=.4)
            vo.wait_until("not a checklist")
            self.play(FadeIn(boxes), FadeIn(no_check), run_time=.4)
            st = strike(boxes, RED, 4)
            self.play(Create(st), run_time=.3)
            vo.wait_until("Each letter")
            self.play(*[FadeOut(m) for m in (dial, needle, comp_lab, boxes, no_check, st)],
                      FadeIn(f_lab), LaggedStart(*[Create(l) for l in code], lag_ratio=.002),
                      run_time=.9)
            self.play(*[TransformFromCopy(s_, d) for s_, d in zip(srcs, drops)], FadeIn(bands),
                      run_time=.8)
        # L1: S — the data classes only load data; O — add a class, not an if
        s_panel = panel_at([(20, CORE[20]), (24, CORE[24]), (25, CORE[25]), (None, ""), (27, CORE[27]),
                            (32, CORE[32]), (33, CORE[33])], CORE_PATH, -.95, 1.25, 10.5, 17)
        slots = VGroup()
        for k, t in enumerate(("gene alignment", "split the M1 table")):
            r = DashedVMobject(Rectangle(width=3.3, height=.6, color=RED), num_dashes=40)\
                .move_to([-4.5 + k * 3.6, -2.0, 0])
            slots.add(VGroup(r, at(t, r.get_x(), -2.0, 19, RED)))
        beside = left("beside them", 1.0, -2.0, 19, GRAY)
        o_panel = panel_at([(107, CORE[107]), (108, CORE[108]), (None, ""), (112, CORE[112]),
                            (None, "        …"),
                            (115, "            self.models.append(scGenModel(self.experiment_spec[…]))")],
                           CORE_PATH, -1.45, 1.25, 9.5, 16)
        ghost = DashedVMobject(RoundedRectangle(corner_radius=.06, width=2.4, height=.55, color=GRAY),
                               num_dashes=30).move_to([4.95, .65, 0])
        ghost_t = mono("CellOTModel", 19, GRAY).move_to(ghost)
        add_cls = VGroup(left("+ a new class", 4.15, .05, 19, INK), tick(3.85, .05, .12, INK))
        no_if = VGroup(left("not another if", 4.15, -.4, 19, RED), cross(3.85, -.4, .1, RED))
        reg = code_panel([(None, 'MODELS = {"IdentityModel": IdentityModel, …}')],
                         "our sketch · not in the repo", -2.9, -1.75, width=6.6, size=16, numbers=False)
        reg_tag = source_tag("EXAMPLE").move_to([1.1, -1.75, 0])
        reg_note = left("CellOT = one new entry", 2.0, -1.75, 19, GRAY)
        with self.say(1) as vo:
            self.cue(vo, .0, FadeOut(code), FadeOut(bands), FadeOut(drops), FadeOut(f_lab),
                     FadeIn(names[0]), run_time=.4)
            focus(0, FadeIn(s_panel, shift=UP * .1))
            vo.wait_until("only load data")
            m = highlight(self, s_panel, 24, 25, 32, 33, run_time=.35)
            vo.wait_until("gene alignment")
            self.play(LaggedStart(*[Create(sl) for sl in slots], lag_ratio=.3), run_time=.7)
            self.play(FadeIn(beside), run_time=.3)
            vo.wait_until("Open-closed")
            self.play(FadeOut(s_panel), FadeOut(m), FadeOut(slots), FadeOut(beside),
                      ReplacementTransform(names[0], names[1]), run_time=.4)
            focus(1, FadeIn(o_panel, shift=UP * .1), run_time=.4)
            vo.wait_until("adding CellOT")
            self.play(Create(ghost), FadeIn(ghost_t), run_time=.4)
            self.play(FadeIn(add_cls), run_time=.3)
            vo.wait_until("chain of ifs")
            m = highlight(self, o_panel, 107, 112, run_time=.3)
            self.play(FadeIn(no_if), run_time=.3)
            vo.wait_until("A dictionary")
            self.play(FadeIn(reg, shift=UP * .1), FadeIn(reg_tag), run_time=.5)
            self.play(FadeIn(reg_note), ghost_t.animate.set_color(INK), run_time=.4)
        # L2: L — every model keeps the contract's promise
        l_rows = [(43, CORE[43]), (None, "    …"), (133, CORE[133]), (None, "    …"), (155, CORE[155]),
                  (None, "    …"), (261, CORE[261])]
        l_panel = panel_at(l_rows, CORE_PATH, -2.5, 1.25, 7.4, 17)
        notes = {43: ("contract: needs training_data", INK), 133: ("Experiment calls train()", INK),
                 155: ("IdentityModel: takes none", INK),
                 261: ("scGenModel keeps it → breaks", RED)}
        ann = {n: left(t, 1.55, l_panel.row_y(n), 18, c) for n, (t, c) in notes.items()}
        follow = Arrow([1.4, l_panel.row_y(155), 0], [1.4, l_panel.row_y(133), 0], buff=.05, color=RED,
                       stroke_width=3, max_tip_length_to_length_ratio=.25)
        lesson = VGroup(label("Python checks names, not inputs", 24, RED, bold=True),
                        label("only a test can catch this · 只有测试能抓到", 19, GRAY))\
            .arrange(DOWN, aligned_edge=LEFT, buff=.1).move_to([-6.2, -2.0, 0], aligned_edge=LEFT)
        with self.say(2) as vo:
            self.cue(vo, .0, FadeOut(o_panel), FadeOut(m), FadeOut(ghost), FadeOut(ghost_t), FadeOut(add_cls),
                     FadeOut(no_if), FadeOut(reg), FadeOut(reg_tag), FadeOut(reg_note),
                     ReplacementTransform(names[1], names[2]), run_time=.4)
            focus(2, FadeIn(l_panel, shift=UP * .1))
            vo.wait_until("The contract's train")
            m = highlight(self, l_panel, 43, run_time=.3)
            self.play(FadeIn(ann[43]), run_time=.3)
            vo.wait_until("IdentityModel's takes")
            m2 = l_panel.mark(155)
            self.play(ReplacementTransform(m, m2), FadeIn(ann[155]), run_time=.4)
            vo.wait_until("Line 133")
            m3 = l_panel.mark(133)
            self.play(ReplacementTransform(m2, m3), FadeIn(ann[133]), GrowArrow(follow), run_time=.5)
            vo.wait_until("so scGen")
            m4 = l_panel.mark(261)
            self.play(ReplacementTransform(m3, m4), FadeIn(ann[261]), run_time=.4)
            vo.wait_until("Python checks")
            self.play(FadeIn(lesson, shift=UP * .1), run_time=.5)
        # L3: I — one method; D — Experiment talks to the contract; only scGenModel imports scgen
        i_panel = panel_at(rows(CORE, 54, 57), CORE_PATH, -1.0, 1.25, 10.4, 17)
        one = at("one method", 5.25, .35, 22, RED, bold=True)
        dy = .35
        e_p = pill("Experiment", -4.85, dy, INK, 20)
        a_p = pill("AbstractModel", -1.15, dy, INK, 20)
        s_p = pill("scGenModel", 2.2, dy, INK, 20)
        g_p = pill("scgen", 5.0, dy, GRAY, 20)
        a1 = arrow(e_p.get_right(), a_p.get_left(), INK)
        a2 = arrow(s_p.get_left(), a_p.get_right(), INK)
        a3 = arrow(s_p.get_right(), g_p.get_left(), GRAY)
        a1_l = at("model.train() …", (e_p.get_right()[0] + a_p.get_left()[0]) / 2, dy - .42, 17, GRAY)
        a3_l = at("import · line 248", (s_p.get_right()[0] + g_p.get_left()[0]) / 2, dy - .42, 17, GRAY)
        never = DashedVMobject(ArcBetweenPoints(e_p.get_top() + UP * .05, g_p.get_top() + UP * .05,
                                                angle=-PI / 6, color=RED, stroke_width=3), num_dashes=40)
        no = cross(.07, never.get_top()[1], .13, RED, 5)
        no_l = at("never imports scgen", .07, never.get_top()[1] - .3, 19, RED, bold=True)
        imp = panel_at([(247, CORE[247]), (248, CORE[248])], CORE_PATH, 2.1, -.4, 6.6, 18)
        only = VGroup(label("the only import scgen that runs", 20, RED, bold=True),
                      label("(lines 14 and 233 are comments)", 17, GRAY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=.08)
        only.move_to([imp.frame.get_left()[0] + only.width / 2, -2.07, 0])
        with self.say(3) as vo:
            self.cue(vo, .0, FadeOut(l_panel), FadeOut(m4), *[FadeOut(a) for a in ann.values()],
                     FadeOut(follow), FadeOut(lesson), ReplacementTransform(names[2], names[3]), run_time=.4)
            focus(3, FadeIn(i_panel, shift=UP * .1))
            vo.wait_until("one method")
            m = highlight(self, i_panel, 56, run_time=.3)
            self.play(FadeIn(one), run_time=.3)
            vo.wait_until("Dependency inversion")
            self.play(ReplacementTransform(names[3], names[4]), FadeOut(one), FadeOut(m), FadeOut(i_panel),
                      run_time=.4)
            focus(4, FadeIn(e_p), FadeIn(a_p), FadeIn(s_p), FadeIn(g_p), run_time=.4)
            vo.wait_until("talks to the contract")
            self.play(GrowArrow(a1), FadeIn(a1_l), GrowArrow(a2), run_time=.5)
            self.play(GrowArrow(a3), FadeIn(a3_l), run_time=.3)
            vo.wait_until("never imports")
            self.play(Create(never), run_time=.4)
            self.play(Create(no), FadeIn(no_l), run_time=.3)
            vo.wait_until("only scGenModel")
            self.play(FadeIn(imp, shift=UP * .1), run_time=.4)
            highlight(self, imp, 248, run_time=.3)
            vo.wait_until("line 248")
            self.play(FadeIn(only, shift=UP * .05), run_time=.35)
        # L4: refactor when the third model arrives
        rng = np.random.default_rng(3)
        messy = VGroup(*[line(-6.0 + rng.uniform(0, .6), .95 - k * .2, -6.0 + rng.uniform(1.2, 3.0),
                              .95 - k * .2, GRAY, 3) for k in range(7)])
        tidy = VGroup(*[line(-6.0 + (.3 if k % 3 else 0), .95 - k * .2, -6.0 + (2.2 if k % 3 else 2.6),
                             .95 - k * .2, INK, 3) for k in range(7)])
        same = VGroup(arrow([-2.9, .35, 0], [-2.1, .35, 0], INK), mono("0.5542", 22, INK).move_to([-1.3, .35, 0]),
                      at("same result", -1.3, -.05, 17, GRAY))
        r_lab = VGroup(label("refactoring", 24, INK, bold=True), label("reshape, same behaviour · 重构", 18, GRAY))\
            .arrange(DOWN, aligned_edge=LEFT, buff=.08).move_to([.6, .7, 0], aligned_edge=LEFT)
        m_y = -1.65
        line_t = line(-6.0, m_y, 5.5, m_y, FAINT, 2)
        mods = [pill("IdentityModel", -4.4, m_y, INK, 19), pill("scGenModel", -1.0, m_y, INK, 19)]
        third = DashedVMobject(RoundedRectangle(corner_radius=.06, width=2.4, height=.55, color=RED),
                               num_dashes=30).move_to([2.6, m_y, 0])
        third_t = at("3rd model", 2.6, m_y, 19, RED)
        here = at("refactor here", 2.6, m_y + .62, 20, RED, bold=True)
        with self.say(4) as vo:
            self.cue(vo, .0, *[FadeOut(x) for x in (e_p, a_p, s_p, g_p, a1, a2, a3, a1_l, a3_l,
                                                   never, no, no_l, names[4], imp, only)],
                     *[l.animate.set_color(GRAY) for l in letters], run_time=.4)
            self.play(FadeIn(messy), FadeIn(same[1]), FadeIn(same[0]), FadeIn(r_lab), run_time=.4)
            vo.wait_until("reshaping")
            self.play(Transform(messy, tidy), Indicate(same[1], color=RED, scale_factor=1.1),
                      FadeIn(same[2]), run_time=1.0)
            vo.wait_until("can wait")
            self.play(Create(line_t), FadeIn(mods[0]), FadeIn(mods[1]), run_time=.4)
            vo.wait_until("third model")
            self.play(Create(third), FadeIn(third_t, shift=LEFT * .2), run_time=.4)
            self.play(FadeIn(here, shift=DOWN * .1), run_time=.3)
        self.finish()


# ---------------------------------------------------------------- s07

LOOP = [("write the call as a test", (-3.4, 1.3)), ("run it", (3.4, 1.3)),
        ("read the last line", (4.72, -.4)), ("smallest change", (3.4, -2.05)),
        ("pass → commit", (-3.4, -2.05)), ("next card", (-4.95, -.4))]
CARDS = [("evaluate → table", "models × metrics"), ("split M1 v08", "four files"),
         ("identity = 0.554", "R² of means"), ("scGen ≈ 0.927", "walk its error trail")]


class S07(Ep):
    def construct(self):
        self.header()
        nodes = [pill(t, x, y, INK, 22, font=LATIN) for t, (x, y) in LOOP]
        edges = [Arrow(nodes[k].get_center(), nodes[(k + 1) % 6].get_center(), buff=0, color=INK,
                       stroke_width=2.5, max_tip_length_to_length_ratio=.06) for k in range(6)]
        for k, e in enumerate(edges):      # trim each edge to the boxes it joins
            a, b = nodes[k], nodes[(k + 1) % 6]
            d = b.get_center() - a.get_center()
            u = d / np.linalg.norm(d)
            pa = a.get_center() + u * min(a.width / 2 / max(abs(u[0]), 1e-3), a.height / 2 / max(abs(u[1]), 1e-3))
            pb = b.get_center() - u * min(b.width / 2 / max(abs(u[0]), 1e-3), b.height / 2 / max(abs(u[1]), 1e-3))
            edges[k] = Arrow(pa + u * .08, pb - u * .08, buff=0, color=INK, stroke_width=2.5,
                             tip_length=.18, max_tip_length_to_length_ratio=.3)
        token = Dot(radius=.1, color=RED).set_z_index(5)
        term = terminal(["$ pytest", "…", "NameError: name '_dense' is not defined"], 0, -.35, width=6.2,
                        size=17)
        term_tag = source_tag("EXAMPLE").move_to([2.45, .55, 0])
        last_bar = Rectangle(width=6.0, height=.32, stroke_width=0, fill_color=RED, fill_opacity=.35)\
            .move_to([0, term.lines[2].get_y(), 0]).set_z_index(1)
        passed = mono("1 passed", 17, PAPER).move_to(term.lines[2], aligned_edge=LEFT).set_z_index(2)

        def go(k, *extra, run_time=.5):
            """Advance the loop from node k-1 to node k (k >= 1)."""
            prev = k - 1
            self.play(GrowArrow(edges[prev]), FadeIn(nodes[k], shift=UP * .05),
                      Transform(nodes[prev], paint(nodes[prev].copy(), INK)),
                      token.animate.move_to(nodes[k].get_top() + UP * .18), *extra, run_time=run_time)

        with self.say(0) as vo:
            vo.wait_until("Write the call")
            paint(nodes[0], RED)
            token.move_to(nodes[0].get_top() + UP * .18)
            self.play(FadeIn(nodes[0], shift=UP * .05), FadeIn(token), run_time=.5)
            vo.wait_until("Run it")
            paint(nodes[1], RED)
            go(1, FadeIn(term[0]), FadeIn(term.lines[0]), FadeIn(term_tag))
            vo.wait_until("Read the last line")
            paint(nodes[2], RED)
            go(2, FadeIn(term.lines[1]), FadeIn(term.lines[2]))
            self.play(FadeIn(last_bar), run_time=.3)
        with self.say(1) as vo:
            paint(nodes[3], RED)
            self.cue(vo, .0)
            go(3)
            vo.wait_until("gets past")
            self.play(FadeOut(last_bar), FadeOut(term.lines[2]), FadeIn(passed), run_time=.5)
            vo.wait_until("When the test")
            paint(nodes[4], RED)
            go(4)
            vo.wait_until("pick up")
            paint(nodes[5], RED)
            go(5, run_time=.4)
            self.play(GrowArrow(edges[5]), Transform(nodes[5], paint(nodes[5].copy(), INK)),
                      Transform(nodes[0], paint(nodes[0].copy(), RED)),
                      token.animate.move_to(nodes[0].get_top() + UP * .18), run_time=.5)
        loop = VGroup(*nodes, *edges, token, term[0], term.lines[0], term.lines[1], passed, term_tag)
        # L2: the four cards, in order
        cy, cw, ch = .95, 2.9, 1.55
        cards = []
        for k, (title, sub) in enumerate(CARDS):
            x = STAGE_X[k]
            fr = Rectangle(width=cw, height=ch, stroke_color=INK, stroke_width=2, fill_color=PAPER,
                           fill_opacity=1).move_to([x, cy, 0])
            cards.append(VGroup(fr, left(f"CARD {k + 1}", x - cw / 2 + .18, cy + .5, 18, RED, bold=True),
                                left(title, x - cw / 2 + .18, cy + .02, 23, INK, cw - .36, bold=True),
                                left(sub, x - cw / 2 + .18, cy - .45, 18, GRAY)))
        order = tagline("INFERRED", "card order: our recommendation", -6.2, -.2, 17)
        my = -1.35
        # card 1: a 2×2 table fills; card 2: one block splits in four; card 3: a number counts up;
        # card 4: the four trail stops turn from ✗ to ✓
        t1 = VGroup(*[Square(.36, stroke_color=INK, stroke_width=2).move_to([STAGE_X[0] - .2 + i * .4,
                                                                             my + .2 - j * .4, 0])
                      for j in range(2) for i in range(2)])
        t1f = VGroup(*[Square(.3, stroke_width=0, fill_color=INK, fill_opacity=1).move_to(q) for q in t1])
        block = Rectangle(width=.9, height=.7, stroke_width=0, fill_color=INK, fill_opacity=1)\
            .move_to([STAGE_X[1], my, 0])
        quads = VGroup(*[Rectangle(width=.42, height=.32, stroke_width=0, fill_color=INK if j == 0 else RED,
                                   fill_opacity=1).move_to([STAGE_X[1] - .3 + i * .6, my + .25 - j * .5, 0])
                         for j in range(2) for i in range(2)])
        val = ValueTracker(0)
        num = always_redraw(lambda: mono(f"{val.get_value():.3f}", 30, INK, bold=True)
                            .move_to([STAGE_X[2], my, 0]))
        num_end = mono("0.554", 30, RED, bold=True).move_to([STAGE_X[2], my, 0])
        stops4 = [cross(STAGE_X[3] - .75 + i * .5, my + .1, .1, RED) for i in range(4)]
        oks4 = [tick(STAGE_X[3] - .75 + i * .5, my + .1, .11, INK) for i in range(4)]
        near = mono("≈ 0.927", 20, RED).move_to([STAGE_X[3], my - .45, 0])
        with self.say(2) as vo:
            self.cue(vo, .0, FadeOut(loop, shift=UP * .2), run_time=.4)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * .1) for c in cards], lag_ratio=.15),
                      FadeIn(order), run_time=.7)
            vo.wait_until("Make evaluate")
            self.play(cards[0][0].animate.set_stroke(RED, 4), Create(t1), run_time=.4)
            self.play(LaggedStart(*[FadeIn(f) for f in t1f], lag_ratio=.2), run_time=.6)
            vo.wait_until("Split the M1")
            self.play(cards[0][0].animate.set_stroke(INK, 2), cards[1][0].animate.set_stroke(RED, 4),
                      FadeIn(block), run_time=.4)
            self.play(ReplacementTransform(block, quads), run_time=.6)
            vo.wait_until("Run identity")
            self.play(cards[1][0].animate.set_stroke(INK, 2), cards[2][0].animate.set_stroke(RED, 4),
                      FadeIn(num), run_time=.4)
            vo.wait_until("gives zero point")
            self.play(val.animate.set_value(.554), run_time=1.0, rate_func=smooth)
            self.remove(num)
            self.add(num_end)
            vo.wait_until("Then walk")
            self.play(cards[2][0].animate.set_stroke(INK, 2), cards[3][0].animate.set_stroke(RED, 4),
                      num_end.animate.set_color(INK), *[FadeIn(s_) for s_ in stops4], run_time=.4)
            for s_, o in zip(stops4, oks4):
                self.play(ReplacementTransform(s_, o), run_time=.3)
            vo.wait_until("lands near")
            self.play(FadeIn(near, shift=UP * .1), run_time=.4)
        board = VGroup(*cards, order, t1, t1f, quads, num_end, *oks4, near)
        # L3: recap
        rows_y = [1.15, .45, -.25, -.95]
        icons = VGroup(
            VGroup(*[VGroup(Square(.26, stroke_color=INK, stroke_width=2).move_to([-5.7 + i * .34, rows_y[0], 0]),
                            tick(-5.7 + i * .34, rows_y[0], .07, INK, 3)) for i in range(4)]),
            VGroup(*[mono(str(i + 1), 20, RED, bold=True).move_to([-5.7 + i * .34, rows_y[1], 0])
                     for i in range(4)]),
            mono("0.554", 22, RED, bold=True).move_to([-5.2, rows_y[2], 0]),
            VGroup(Circle(radius=.22, color=INK, stroke_width=2).move_to([-5.2, rows_y[3], 0]),
                   Polygon([-5.2, rows_y[3] + .18, 0], [-5.25, rows_y[3], 0], [-5.15, rows_y[3], 0],
                           color=RED, fill_color=RED, fill_opacity=1, stroke_width=0)))
        texts = VGroup(*[left(t, -4.3, y, 26, INK) for t, y in zip(
            ["the skeleton already walks", "the errors give the order",
             "first golden number: identity 0.554", "SOLID is for when something hurts"], rows_y)])
        recap = left("RECAP · 回顾", -6.2, 1.8, 18, GRAY, bold=True)
        motto = VGroup(label("Momentum beats a perfect plan.", 32, RED, bold=True),
                       label("动起来，比完美的计划更重要", 20, GRAY)).arrange(DOWN, aligned_edge=LEFT, buff=.12)
        motto.move_to([-6.2, -1.98, 0], aligned_edge=LEFT)
        with self.say(3) as vo:
            self.cue(vo, .0, FadeOut(board, shift=UP * .2), FadeIn(recap), run_time=.4)
            for k, w in enumerate(["The skeleton", "the errors give", "the first golden", "and SOLID"]):
                vo.wait_until(w)
                self.play(FadeIn(icons[k], shift=RIGHT * .1), FadeIn(texts[k], shift=RIGHT * .1),
                          run_time=.45)
            vo.wait_until("Momentum")
            self.play(FadeIn(motto, shift=UP * .1), run_time=.5)
        self.finish()
