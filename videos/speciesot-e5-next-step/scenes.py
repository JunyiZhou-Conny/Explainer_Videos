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
N_NOTEBOOKS = 83            # .ipynb files in the speciesOT repo at 109bf12 (no checkpoints)
STAGES = ["setup", "train", "predict", "evaluate"]
STAGE_X = [-4.65, -1.55, 1.55, 4.65]

# m1_modern.yaml (speciesOT repo at 109bf12), the lines shown on screen, verbatim
SPEC = {
    1: "experiment_tag: hvg_pearson_residuals_m1_v08_ood",
    4: "data_file: datasets/speciesot-human-mouse-hvg/hvg_pearson_residuals_m1_v08.h5ad",
    25: "holdout_cell_types:",
    26: "- CL:0000875",
    28: "datasplit_strategy: toggle_ood",
    29: "mode: ood",
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
        names.add(mono(s, size).move_to([x, y + h * .18, 0]).set_z_index(2))
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
        f_path = mono("speciesot_core.py", 16, GRAY).move_to([-4.8, -1.2, 0])
        f_lab = at("345 lines", -4.8, -1.62, 26, INK, bold=True)
        grid = tiles(-.2, .47)
        g_path = mono("speciesOT repo · *.ipynb", 16, GRAY).move_to([-.2, -1.2, 0])
        g_lab = at("83 notebooks", -.2, -1.62, 26, INK, bold=True)
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
            hour = chip("next hour?", -4.8, .47, RED, 22, font=LATIN).set_z_index(4)
            self.play(FadeIn(q, shift=UP * .1), today.animate.set_color(GRAY), run_time=.4)
            self.play(FadeIn(hour, scale=.8), run_time=.2)
            for x in (-.2, 4.35):
                self.play(hour.animate.move_to([x, .47, 0]), run_time=.3)
        piles = VGroup(frame, shape, f_path, f_lab, grid, g_path, g_lab, axis, ticks, ends, bar,
                       today, t_path, t_lab)

        plan = chip("plan everything first", 0, 1.45, GRAY, 24, font=LATIN)
        nodes = [chip(t, x, .05, INK, 24, font=LATIN) for t, x in
                 (("run the code", -4.3), ("read the first break", 0), ("fix only that", 4.3))]
        a12 = arrow(nodes[0].get_right(), nodes[1].get_left(), INK)
        a23 = arrow(nodes[1].get_right(), nodes[2].get_left(), INK)
        back = CurvedArrow(nodes[2].get_bottom() + DOWN * .08, nodes[0].get_bottom() + DOWN * .08,
                           angle=-PI / 4, color=INK, stroke_width=2.5)
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
                      token.animate.move_to(nodes[2].get_top() + UP * .2), run_time=.6)
            self.play(Create(back), run_time=.5)
            self.play(MoveAlongPath(token, back.copy()), Transform(nodes[2], paint(nodes[2].copy(), INK)), run_time=.9)
            self.play(token.animate.move_to(nodes[0].get_top() + UP * .2),
                      Transform(nodes[0], paint(nodes[0].copy(), RED)), run_time=.3)
            vo.wait_until("This episode")
            self.play(FadeIn(habit, shift=UP * .1), run_time=.5)
        self.finish()


# ---------------------------------------------------------------- s02

class S02(Ep):
    def construct(self):
        self.header()
        y0, ty = .55, .2
        boxes, names, arrows = stage_row(y0, h=1.1)
        who = chip("IdentityModel", -4.95, 1.68, RED, 21)
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
            self.cue(vo, .0, FadeOut(ok), FadeIn(skel, shift=UP * .1), run_time=.5)
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
            sc.move_to([2.45, -.62 - k * .42, 0])
        toy = at("computed on toy data", 2.45, -1.5, 17, GRAY)
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
            self.play(*[TransformFromCopy(boxes[3], sc) for sc in scores], FadeIn(toy),
                      run_time=.6)
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
            self.play(*[TransformFromCopy(boxes[3], v) for v in vals], FadeIn(later), run_time=.6)
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


def trail_card(i, y=.93, w=2.9):
    stage, etype, _, ln, frag, _ = TRAIL[i]
    x = STAGE_X[i]
    frame = Rectangle(width=w, height=.97, stroke_color=INK, stroke_width=2, fill_color=PAPER,
                      fill_opacity=1).move_to([x, y, 0])
    bar = Rectangle(width=w, height=.07, stroke_width=0, fill_color=RED,
                    fill_opacity=1).move_to([x, frame.get_top()[1] - .035, 0])
    lx = x - w / 2 + .18
    g = VGroup(frame, bar, mono_line(etype, lx, y + .2, 19, RED, bold=True),
               mono_line(frag, lx, y - .07, 16), mono_line(f"line {ln}", lx, y - .32, 16, GRAY))
    g.set_z_index(3)
    return g


def message_line(i, y=.12, x=-6.2):
    _, etype, msg, *_ = TRAIL[i]
    a = mono_line(etype + ":", x, y, 17, RED, bold=True)
    b = mono_line(msg, x + ADVANCE * 17 * (len(etype) + 2), y, 17)
    return VGroup(a, b)


def trail_panel(i, top=-.12):
    return panel_at(TRAIL[i][5], CORE_PATH, -1.95, top, 8.6, 17)


class S03(Ep):
    def construct(self):
        self.header()
        ty = 1.86
        track = line(-6.2, ty, 6.2, ty, INK, 2)
        stops = VGroup(*[line(x, ty - .1, x, ty + .1, INK, 2) for x in STAGE_X])
        labels = VGroup(*[mono_line(s, x - ADVANCE * 18 * len(s) / 2, 1.6, 18, GRAY)
                          for x, s in zip(STAGE_X, STAGES)])
        add = VGroup(chip("IdentityModel", -1.6, .75, GRAY, 20), chip("+ scGenModel", 1.6, .75, RED, 20))
        with self.say(0) as vo:
            self.cue(vo, .02, Create(track), FadeIn(stops), FadeIn(labels), run_time=.5)
            vo.wait_until("add scGen")
            self.play(FadeIn(add[0]), FadeIn(add[1], shift=LEFT * .2), run_time=.4)
            vo.wait_until("Pause")
            card = ponder("加上 scGen 继续跑：哪个阶段最先坏？",
                          "Add scGen and keep running: which stage breaks first?", y=-.95)
            self.play(self.dim_rest(), run_time=.4)
            self.play(FadeIn(card, shift=UP * .1), run_time=.4)
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
            self.cue(vo, .0, FadeOut(card), FadeOut(add),
                     *[m.animate.set_opacity(1) for m in (track, stops, labels)], run_time=.4)
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
            return cards[i].animate.move_to([STAGE_X[i], .93, 0])

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
                          label("one name, four places", 18, GRAY)).arrange(DOWN, aligned_edge=LEFT,
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
            msg4, panel4 = message_line(3), trail_panel(3)
            self.play(slide(3), numbered[2].animate.set_color(INK), numbered[3].animate.set_color(RED),
                      FadeOut(m3), FadeOut(n1), FadeOut(n2), ReplacementTransform(msg3, msg4),
                      FadeOut(panel3), FadeIn(panel4), run_time=.8)
            mx, hx, top = 3.7, 4.9, -.35
            mouse = VGroup(*[Dot([mx, top - k * .155, 0], radius=.055, color=INK) for k in range(5)])
            human = VGroup(*[Dot([hx, top - k * .155, 0], radius=.055, color=INK) for k in range(7)])
            ml = label("5 mouse", 17, GRAY).next_to(mouse, LEFT, buff=.15)
            hl = label("7 human", 17, GRAY).next_to(human, RIGHT, buff=.15)
            vo.wait_until("different cell counts")
            self.play(FadeIn(mouse), FadeIn(human), FadeIn(ml), FadeIn(hl), run_time=.5)
            vo.wait_until("line them up")
            pairs = VGroup(*[line(mx + .07, top - k * .155, hx - .07, top - k * .155, FAINT, 1.5)
                             for k in range(5)])
            self.play(LaggedStart(*[Create(p) for p in pairs], lag_ratio=.15),
                      human[5:].animate.set_color(RED), run_time=.6)
            vo.wait_until("at line 313")
            m = highlight(self, panel4, 313, run_time=.35)
        rows_y = [-.62, -1.07, -1.52, -1.97]
        board = Rectangle(width=8.5, height=2.65, stroke_color=INK, stroke_width=2).move_to(
            [-1.95, -1.08, 0])
        head = left("TO-DO · 待办", -5.95, -.1, 22, INK, bold=True)
        todo = []
        for k, (stage, etype, _, ln, *_r) in enumerate(TRAIL):
            box = Square(.26, stroke_color=INK, stroke_width=2).move_to([-5.8, rows_y[k], 0])
            num = mono(str(k + 1), 20, RED, bold=True).move_to([-5.3, rows_y[k], 0])
            txt = mono_left(f"{stage:<9}{etype:<15}line {ln}", -4.9, rows_y[k], 19)
            todo.append(VGroup(box, num, txt))
        given = VGroup(label("program order", 24, RED, bold=True),
                       label("顺序由程序给出", 18, GRAY)).arrange(DOWN, aligned_edge=LEFT, buff=.1)
        given.move_to([2.7 + given.width / 2, -.62, 0])
        with self.say(4) as vo:
            self.cue(vo, .0, FadeOut(m), FadeOut(panel4), FadeOut(msg4), FadeOut(mouse),
                     FadeOut(human), FadeOut(ml), FadeOut(hl), FadeOut(pairs),
                     numbered[3].animate.set_color(INK), run_time=.4)
            self.play(Create(board), FadeIn(head), run_time=.4)
            self.play(LaggedStart(*[ReplacementTransform(cards[k], todo[k]) for k in range(4)],
                                  lag_ratio=.3), run_time=1.6)
            vo.wait_until("You don't")
            self.play(LaggedStart(*[Indicate(t[1], color=RED, scale_factor=1.4) for t in todo],
                                  lag_ratio=.2), run_time=1.0)
            vo.wait_until("The program")
            self.play(FadeIn(given, shift=LEFT * .1), run_time=.5)
        self.finish()
