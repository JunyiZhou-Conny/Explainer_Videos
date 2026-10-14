"""speciesOT E2 · One name, four places — Swiss scenes.

Narration and budgets come from the plan (script.json). Code on screen is Josh's real
speciesot_core.py, Tests/config.yaml and Tests/toy_config.yaml (videos/speciesot-series/
excerpts.py, real line numbers; a long line may be elided with "…", never rewritten). Error
texts are MEASURED by videos/speciesot-series/checks/error_trail.py on toy data with a
STAND-IN scgen. The diagrams here (a value token travelling four hops, dictionary drawers,
the twin drawers, the traceback read bottom-up) are this episode's own.
"""
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent.parent / "speciesot-series"
sys.path.insert(0, str(SERIES))

from manim import *  # noqa: E402,F401,F403
from speciesot_kit import *  # noqa: E402,F401,F403
from excerpts import CORE, CONFIG, TOY_CONFIG, E24_OUTPUTS, rows  # noqa: E402

CORE_PATH = "src/speciesot/speciesot_core.py"
CFG_PATH = "Tests/config.yaml"
TOY_PATH = "Tests/toy_config.yaml"
NB_PATH = "Tests/e24_replica.ipynb"
ATTR_MSG = "'scGenModel' object has no attribute 'x_dimensions'"   # stage config_setup
KEY_MSG = "'x_dimension'"                                          # stage toy_model_section


class Ep(EpisodeScene):
    episode = "E2"
    total = "07"


# ---------------------------------------------------------------- small helpers

def _nows(s):
    return "".join(s.split())


def glyphs(t, body, sub, nth=0):
    """The glyphs of Text `t` (laid out from string `body`) that spell substring `sub`."""
    i = -1
    for _ in range(nth + 1):
        i = body.find(sub, i + 1)
    a = len(_nows(body[:i]))
    return VGroup(*t[a:a + len(_nows(sub))])


def plural_s(t, body, color=RED):
    """Colour the trailing s of every `x_dimensions` in a Text built from `body`; returns them."""
    out = VGroup()
    i = body.find("x_dimensions")
    while i >= 0:
        k = len(_nows(body[:i])) + len("x_dimensions") - 1
        t[k].set_color(color)
        out.add(t[k])
        i = body.find("x_dimensions", i + 1)
    return out


def cpanel(src_rows, title, x, y, width=6.4, size=20, **kw):
    """code_panel + the geometry needed to mark rows after the panel has moved."""
    p = code_panel(src_rows, title, x, y, width, size, **kw)
    p.head_h = .4 if title else 0
    p.top0 = p.frame.get_top()[1]
    p.gut_off = p.gutter_x - p.frame.get_left()[0]
    p.w0 = p.frame.width
    return p


def rmark(p, *nums, color=RED):
    """Highlight rows by their position in the panel (robust to elided rows and moves)."""
    s = p.frame.width / p.w0
    texts = list(p.texts)
    top, x0 = p.frame.get_top()[1], p.frame.get_left()[0]
    gx = x0 + p.gut_off * s
    w = p.frame.get_right()[0] - gx - .04 * s
    out = VGroup()
    for n in nums:
        i = texts.index(p.rows[n])
        y = top - (p.head_h + .15 + p.gap / 2 + i * p.gap) * s
        band = Rectangle(width=w, height=p.gap * .98 * s, stroke_width=0, fill_color=TINT,
                         fill_opacity=1).move_to([gx + .02 * s + w / 2, y, 0])
        bar = Rectangle(width=.08 * s, height=p.gap * .98 * s, stroke_width=0, fill_color=color,
                        fill_opacity=1).move_to([gx + .04 * s, y, 0])
        out.add(VGroup(band, bar))
    out.set_z_index(1)
    return out


def tag_text(text, color=RED, size=15):
    """A provenance chip with free text (same look as the kit's source_tag)."""
    t = Text(text, font=LATIN, font_size=size, color=color, weight=BOLD)
    box = RoundedRectangle(corner_radius=.06, width=t.width + .26, height=t.height + .16,
                           stroke_color=color, stroke_width=1.5, fill_color=PAPER,
                           fill_opacity=1).move_to(t.get_center())
    return VGroup(box, t)


def token(pos, r=.1):
    return Dot(pos, radius=r, color=RED).set_z_index(8)


def hop_badge(n, x, y, r=.2, color=RED):
    c = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to([x, y, 0])
    t = Text(str(n), font=LATIN, font_size=20, color=PAPER, weight=BOLD).move_to(c)
    return VGroup(c, t).set_z_index(7)


def under(m, color=RED, buff=.06, stroke=3):
    return Line(m.get_corner(DL) + DOWN * buff, m.get_corner(DR) + DOWN * buff, color=color,
                stroke_width=stroke).set_z_index(7)


def drawer_open(d, dx=.45):
    """Slide a drawer's body out to the right (label + value travel with it)."""
    return d.animate.shift(RIGHT * dx)


# ================================================================ s01

class S01(Ep):
    def construct(self):
        self.header()
        cell = cpanel([(1, "experiment.setup()")], NB_PATH, -3.85, 1.5, width=4.9, size=22,
                      numbers=False)
        err = error_card("AttributeError", ATTR_MSG, "speciesot_core.py:253 in setup",
                         -1.25, -.85, width=10.1, size=22)
        msg = err[3][0]
        red_s = msg[-2]
        red_s.set_color(RED)
        with self.say(0) as vo:
            self.cue(vo, .03, FadeIn(cell, shift=UP * .1), run_time=.5)
            vo.wait_until("Setup crashes")
            m = rmark(cell, 1)
            cx = cell.get_x()
            tok = token([cx, cell.get_bottom()[1] - .02, 0])
            wire = Line([cx, cell.get_bottom()[1], 0], [cx, err.get_top()[1] + .02, 0],
                        color=INK, stroke_width=2)
            self.play(FadeIn(m), FadeIn(tok), run_time=.3)
            self.play(Create(wire), tok.animate.move_to(wire.get_end()), run_time=.6)
            vo.wait_until("attribute error")
            self.play(FadeOut(tok, scale=2.5), FadeIn(err, shift=UP * .12), run_time=.5)
            vo.wait_until("with an s")
            ring = Circle(radius=.2, color=RED, stroke_width=3).move_to(red_s).set_z_index(9)
            self.play(Create(ring), run_time=.45)

        line_body = CORE[253]
        fixp = cpanel([(253, line_body)], CORE_PATH, 2.8, 1.5, width=7.0, size=22)
        s253 = plural_s(fixp.row(253), line_body)[0]
        comma = fixp.row(253)[-1]
        patch = left("one-letter patch", fixp.frame.get_left()[0], .7, 20, GRAY)
        ok = mono("setup() runs ✓", 34, INK, bold=True).move_to([-2.6, -.55, 0])
        toy = left("toy data · 4 genes", -6.1, -1.55, 22, GRAY)
        st = tag_text("MEASURED · stand-in scgen").move_to([0, 0, 0])
        st.next_to(toy, RIGHT, buff=.35)
        with self.say(1) as vo:
            self.cue(vo, .02, FadeOut(ring), FadeOut(m), FadeOut(wire), FadeIn(fixp, shift=LEFT * .1),
                     run_time=.5)
            vo.wait_until("Delete the s")
            self.play(FadeIn(patch), Circumscribe(s253, color=RED, buff=.05), run_time=.5)
            self.play(FadeOut(s253, shift=UP * .25), comma.animate.shift(LEFT * ADVANCE * 22),
                      red_s.animate.set_opacity(.25), run_time=.6)
            vo.wait_until("crash disappears")
            self.play(err.animate.stretch_to_fit_height(.02).set_opacity(0), run_time=.5)
            self.remove(err)
            vo.wait_until("toy data")
            self.play(FadeIn(toy, shift=RIGHT * .1), run_time=.4)
            vo.wait_until("stand-in")
            self.play(FadeIn(st, shift=RIGHT * .1), run_time=.4)
            vo.wait_until("setup runs")
            self.play(FadeIn(ok, shift=UP * .1), run_time=.5)

        y1, y2, x0, L = .35, -.75, -1.6, 6.4
        net_lab = left("network built for", -6.1, y1 + .02, 22, INK)
        net_val = mono_left("x_dimension = 1000", -6.1, y1 - .38, 20, INK)
        dat_lab = left("toy data has", -6.1, y2 + .02, 22, INK)
        dat_val = mono_left("4 genes", -6.1, y2 - .38, 20, GRAY)
        bar1 = Rectangle(width=L, height=.42, stroke_width=0, fill_color=INK,
                         fill_opacity=1).move_to([x0 + L / 2, y1 - .18, 0])
        bar2 = Rectangle(width=max(L * 4 / 1000, .05), height=.42, stroke_width=0,
                         fill_color=INK, fill_opacity=1).move_to([x0, y2 - .18, 0], aligned_edge=LEFT)
        n1 = mono("1000", 20, INK).next_to(bar1, RIGHT, buff=.15)
        n2 = mono("4", 20, GRAY).next_to(bar2, RIGHT, buff=.15)
        neq = mono("≠", 54, RED, bold=True).move_to([x0 - .55, (y1 + y2) / 2 - .18, 0])
        verdict = at("error gone · bug stays", 0, -1.85, 34, RED, bold=True)
        with self.say(2) as vo:
            self.cue(vo, .02, FadeOut(cell), FadeOut(ok), FadeOut(toy), FadeOut(st),
                     FadeOut(patch), run_time=.4)
            self.play(FadeIn(net_lab), FadeIn(net_val), FadeIn(dat_lab), FadeIn(dat_val),
                      run_time=.4)
            vo.wait_until("one thousand genes")
            self.play(GrowFromEdge(bar1, LEFT), FadeIn(n1), run_time=.8)
            vo.wait_until("not four")
            self.play(GrowFromEdge(bar2, LEFT), FadeIn(n2), run_time=.4)
            self.play(FadeIn(neq, scale=1.4), run_time=.35)
            vo.wait_until("The error is gone")
            self.play(FadeIn(verdict, shift=UP * .1), neq.animate.set_color(INK), run_time=.5)
            vo.wait_until("follow one name")
            dots = VGroup(*[hop_badge(i + 1, 3.0 + i * .75, -1.85, r=.17) for i in range(4)])
            path = Line([3.0, -1.85, 0], [3.0 + 3 * .75, -1.85, 0], color=INK, stroke_width=2)
            self.play(verdict.animate.move_to([-2.3, -1.85, 0]), run_time=.4)
            self.play(Create(path), LaggedStart(*[FadeIn(d, scale=.6) for d in dots],
                                                lag_ratio=.25), run_time=.9)
        self.finish()


# ================================================================ s02

class S02(Ep):
    def construct(self):
        self.header()
        core = cpanel(rows(CORE, 214, 218), CORE_PATH, -2.4, .96, width=7.8, size=16)
        cfg = cpanel(rows(CONFIG, 32, 36), CFG_PATH, -3.95, -1.33, width=4.7, size=17)
        nb_rows = [(1, "%load_ext autoreload"), (2, "%autoreload 2"), (3, "…"),
                   (4, "experiment = Experiment(…)"), (5, "experiment.setup()")]
        nb = cpanel(nb_rows, NB_PATH, 4.15, -1.39, width=4.3, size=17, numbers=False)
        with self.say(0) as vo:
            vo.wait_until("three windows")
            ghosts = VGroup(*[DashedVMobject(Rectangle(width=p.frame.width, height=p.frame.height,
                                                       color=FAINT, stroke_width=2),
                                             num_dashes=40).move_to(p.frame)
                              for p in (core, cfg, nb)])
            self.play(LaggedStart(*[Create(g) for g in ghosts], lag_ratio=.2), run_time=.6)
            for p, w in zip((core, cfg, nb), ("package file", "config file", "e24_replica")):
                vo.wait_until(w)
                self.play(FadeIn(p, shift=UP * .08), run_time=.45)
            self.remove(*ghosts)

        # wire 1: core -> notebook (elbow), wire 2: config -> notebook
        y1, xe = .95, 4.15
        corners = [[core.frame.get_right()[0], y1, 0], [xe, y1, 0],
                   [xe, nb.frame.get_top()[1], 0]]
        w1_path = VMobject().set_points_as_corners(corners)
        w1 = VGroup(Line(corners[0], corners[1], color=INK, stroke_width=3),
                    Line(corners[1], corners[2], color=INK, stroke_width=3))
        w1_tip = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(.09)\
            .rotate(PI).move_to([xe, nb.frame.get_top()[1] + .08, 0])
        y2 = nb.frame.get_y()
        w2 = Line([cfg.frame.get_right()[0], y2, 0], [nb.frame.get_left()[0], y2, 0], color=INK,
                  stroke_width=3)
        w2_tip = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(.09)\
            .rotate(-PI / 2).move_to([nb.frame.get_left()[0] - .08, y2, 0])
        dash1 = VGroup(*[DashedVMobject(seg.copy().set_color(FAINT), num_dashes=n)
                         for seg, n in zip(w1, (14, 8))])
        dash2 = DashedVMobject(w2.copy().set_color(FAINT), num_dashes=16)
        pip = mono("pip install -e .", 18, INK).move_to([(core.frame.get_right()[0] + xe) / 2,
                                                         y1 + .3, 0])
        pip_e = glyphs(pip, "pip install -e .", "-e")
        frozen = VGroup(DashedVMobject(Rectangle(width=2.15, height=.5, color=GRAY,
                                                 stroke_width=2), num_dashes=24),
                        Text("frozen copy", font=LATIN, font_size=19, color=GRAY))
        frozen.move_to([pip.get_x(), .3, 0])
        frozen[1].move_to(frozen[0])
        with self.say(1) as vo:
            vo.wait_until("Two wires")
            self.play(Create(dash1), Create(dash2), run_time=.6)
            vo.wait_until("editable install")
            self.play(Create(w1), FadeIn(w1_tip), FadeOut(dash1), FadeIn(pip, shift=DOWN * .08),
                      run_time=.7)
            vo.wait_until("dash e")
            self.play(pip_e.animate.set_color(RED), Circumscribe(pip_e, color=RED, buff=.05),
                      run_time=.6)
            vo.wait_until("imports your folder")
            tok = token(corners[0])
            self.play(FadeIn(tok), run_time=.15)
            self.play(MoveAlongPath(tok, w1_path), run_time=1.0)
            vo.wait_until("not a frozen copy")
            x_out = strike(frozen[0])
            self.play(FadeIn(frozen), run_time=.35)
            self.play(Create(x_out), run_time=.3)
            vo.wait_until("And autoreload")
            m_nb = rmark(nb, 1, 2)
            self.play(FadeIn(m_nb), FadeOut(tok), run_time=.4)
            vo.wait_until("re-reads the file")
            m_core = rmark(core, 218)
            self.play(FadeIn(m_core), run_time=.35)
            tok2 = token(corners[0])
            self.play(FadeIn(tok2), run_time=.15)
            self.play(MoveAlongPath(tok2, w1_path), run_time=1.0)
            self.play(FadeOut(tok2), FadeOut(m_core), run_time=.3)

        core2 = cpanel(rows(CORE, 80, 82), CORE_PATH, -2.4, 1.24, width=7.8, size=16)
        exp_l = mono("Experiment(path)", 17, INK).move_to([w2.get_x(), y2 + .3, 0])
        safe_l = mono("yaml.safe_load", 17, RED).move_to([w2.get_x(), y2 - .3, 0])
        with self.say(2) as vo:
            vo.wait_until("config wire")
            self.play(Create(w2), FadeIn(w2_tip), FadeOut(dash2), FadeOut(m_nb),
                      pip_e.animate.set_color(INK), run_time=.6)
            vo.wait_until("Every new Experiment")
            m4 = rmark(nb, 4)
            self.play(FadeIn(m4), FadeIn(exp_l, shift=DOWN * .08), run_time=.45)
            vo.wait_until("opens config.yaml")
            self.play(ReplacementTransform(core, core2), run_time=.6)
            vo.wait_until("yaml.safe_load")
            m82 = rmark(core2, 82)
            tok3 = token(w2.get_start())
            self.play(FadeIn(m82), FadeIn(safe_l, shift=UP * .08), FadeIn(tok3), run_time=.4)
            self.play(MoveAlongPath(tok3, w2), run_time=.8)
            self.play(FadeOut(tok3), run_time=.2)

        lx, ly = [-4.1, 0, 4.1], .55
        names = ("edit a file", "rerun the cell", "read what breaks")
        steps = VGroup(*[chip(t, x, ly, INK, 26, font=LATIN) for t, x in zip(names, lx)])
        subs = VGroup(*[mono(t, 16, GRAY).move_to([x, ly - .62, 0]) for t, x in
                        zip(("core.py · config.yaml", "e24_replica.ipynb", "the traceback"), lx)])
        fwd = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=.12, color=INK,
                             stroke_width=3, tip_length=.2, max_tip_length_to_length_ratio=1)
                       for i in range(2)])
        a0 = [lx[2], ly - .95, 0]
        a1 = [lx[0], ly - .95, 0]
        back = CurvedArrow(a0, a1, angle=-TAU / 6, color=RED, stroke_width=3, tip_length=.2)
        with self.say(3) as vo:
            self.cue(vo, .01, *[FadeOut(mm) for mm in self.content()], run_time=.4)
            for i, w in enumerate(names):
                vo.wait_until(w)
                anims = [FadeIn(steps[i], shift=UP * .08), FadeIn(subs[i])]
                if i:
                    anims.append(GrowArrow(fwd[i - 1]))
                self.play(*anims, run_time=.35)
            vo.wait_until("That loop")
            self.play(Create(back), run_time=.45)
            run = VMobject().set_points_as_corners([steps[0].get_top() + UP * .14,
                                                    steps[2].get_top() + UP * .14])
            tok4 = token(run.get_start())
            self.play(FadeIn(tok4), run_time=.1)
            self.play(MoveAlongPath(tok4, run), run_time=.7)
            self.play(tok4.animate.move_to(a0), run_time=.2)
            self.play(MoveAlongPath(tok4, back), run_time=.6)
        self.finish()
