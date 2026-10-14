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
        names.add(mono(s, size).move_to([x, y + h * .18, 0]))
    for a, b in zip(boxes, boxes[1:]):
        arrows.add(Arrow(a.get_right(), b.get_left(), buff=.06, color=INK, stroke_width=2.5,
                         max_tip_length_to_length_ratio=.3))
    return boxes, names, arrows


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
            hour = chip("next hour?", -4.8, -1.62, RED, 20, font=LATIN).set_z_index(4)
            self.play(FadeIn(q, shift=UP * .1), run_time=.4)
            self.play(FadeIn(hour), run_time=.2)
            for x in (-.2, 4.35):
                self.play(hour.animate.move_to([x, -1.62, 0]), run_time=.3)
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
        habit = at("Josh's habit  →  a method · 习惯 → 方法", 0, -2.1, 28, RED, bold=True)
        with self.say(1) as vo:
            self.cue(vo, .0, FadeOut(piles, shift=UP * .2), FadeOut(q), FadeOut(hour), run_time=.5)
            vo.wait_until("planning everything")
            self.play(FadeIn(plan, shift=DOWN * .1), run_time=.4)
            vo.wait_until("first.")
            self.play(Create(strike(plan)), plan.animate.set_opacity(.45), run_time=.4)
            vo.wait_until("runs the code")
            token.move_to(nodes[0].get_top() + UP * .2)
            self.play(FadeIn(nodes[0], shift=UP * .1), FadeIn(token), run_time=.4)
            vo.wait_until("reads the first")
            self.play(GrowArrow(a12), FadeIn(nodes[1], shift=UP * .1),
                      token.animate.move_to(nodes[1].get_top() + UP * .2), run_time=.6)
            vo.wait_until("fixes only")
            self.play(GrowArrow(a23), FadeIn(nodes[2], shift=UP * .1),
                      token.animate.move_to(nodes[2].get_top() + UP * .2), run_time=.6)
            self.play(Create(back), run_time=.5)
            path = back.copy()
            self.play(MoveAlongPath(token, path), run_time=.9)
            vo.wait_until("This episode")
            self.play(FadeIn(habit, shift=UP * .1), run_time=.5)
        self.finish()
