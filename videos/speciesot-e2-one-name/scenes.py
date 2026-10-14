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


def lag(scene, *anims, lag_ratio=.2, run_time=1.0, extra=()):
    """LaggedStart that leaves the scene's mobject tree alone.

    By default Scene.play adds a wrapper Group of the animated mobjects; Scene.add then
    restructures the scene, splitting each parent card (e.g. a drawer) into loose parts, and
    removing that wrapper afterwards takes the children off screen. Here the wrapper is an
    empty holder (nothing to restructure), removed after the play; animated mobjects that are
    not yet on screen are added as themselves. `extra` animations play alongside."""
    fam = scene.get_mobject_family_members()
    for a in anims:
        if not a.is_introducer() and a.mobject not in fam:
            scene.add(a.mobject)
    holder = VGroup()
    scene.play(*extra, LaggedStart(*anims, lag_ratio=lag_ratio, group=holder),
               run_time=run_time)
    scene.remove(holder)


def tb_block(lines, x, y, width, size=19, color="#D9D5CB"):
    """A terminal panel whose lines keep their leading spaces (traceback indentation)."""
    gap = size * .0185
    h = len(lines) * gap + .36
    box = Rectangle(width=width, height=h, stroke_width=0, fill_color=INK,
                    fill_opacity=1).move_to([x, y, 0])
    top, x0 = box.get_top()[1], box.get_left()[0] + .25
    texts = VGroup(*[place_line(code_line(l, size, color), x0, top - .18 - gap / 2 - i * gap, size)
                     for i, l in enumerate(lines)])
    g = VGroup(box, texts)
    g.box, g.lines, g.gap = box, texts, gap
    return g


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
            self.play(Create(path), run_time=.3)
            lag(self, *[FadeIn(d, scale=.6) for d in dots], lag_ratio=.25, run_time=.6)
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
            lag(self, *[Create(g) for g in ghosts], lag_ratio=.2, run_time=.6)
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


# ================================================================ s03

def value_token(text="50", size=20):
    t = Text(text, font=MONO, font_size=size, color=PAPER, weight=BOLD)
    box = RoundedRectangle(corner_radius=.08, width=t.width + .26, height=t.height + .2,
                           stroke_width=0, fill_color=RED, fill_opacity=1).move_to(t)
    return VGroup(box, t).set_z_index(8)


def hop_ring(n, frame, r=.2):
    """Hop number in a red ring, just left of a station's top-left corner."""
    x, y = frame.get_left()[0] - .32, frame.get_top()[1] - .22
    c = Circle(radius=r, color=RED, stroke_width=3, fill_color=PAPER, fill_opacity=1)\
        .move_to([x, y, 0])
    t = Text(str(n), font=LATIN, font_size=22, color=RED, weight=BOLD).move_to(c)
    return VGroup(c, t).set_z_index(7)


def link(a, b):
    return Arrow(a, b, buff=.1, color=GRAY, stroke_width=2, tip_length=.16,
                 max_tip_length_to_length_ratio=1)


class S03(Ep):
    def construct(self):
        self.header()
        full = cpanel(rows(CONFIG, 30, 40), CFG_PATH, -3.25, -.05, width=5.1, size=18)
        one = left("one value", .6, 1.35, 24, GRAY)
        zv = mono_left("z_dimension = 50", .6, .75, 34, INK)
        latent = left("the latent size · 潜空间大小", .6, .15, 22, GRAY)
        tok = value_token()
        with self.say(0) as vo:
            self.cue(vo, .03, FadeIn(one), run_time=.35)
            vo.wait_until("z_dimension, fifty")
            self.play(FadeIn(zv, shift=UP * .1), FadeIn(latent), run_time=.5)
            vo.wait_until("Hop one")
            b1 = hop_ring(1, full.frame)
            self.play(FadeIn(full, shift=RIGHT * .1), FadeIn(b1), run_time=.5)
            m38 = rmark(full, 38)
            tok.move_to(glyphs(full.row(38), CONFIG[38], "50"))
            self.play(FadeIn(m38), FadeIn(tok, scale=1.3), run_time=.4)
            vo.wait_until("under models")
            m30 = rmark(full, 30)
            self.play(FadeIn(m30), run_time=.35)
            vo.wait_until("under scGenModel")
            m32 = rmark(full, 32)
            self.play(FadeIn(m32), run_time=.35)

        # station 1 (compact), station 2 (drawers in a dict frame)
        st1 = cpanel([(38, CONFIG[38])], CFG_PATH, -3.95, 1.45, width=3.6, size=20)
        s1_38 = rmark(st1, 38)
        b1s = hop_ring(1, st1.frame)
        dx, dw = -3.8, 3.9
        dframe = Rectangle(width=dw, height=2.37, stroke_color=INK, stroke_width=2,
                           fill_color=PAPER, fill_opacity=1).move_to([dx, .55 - 2.37 / 2, 0])
        dtitle = mono("spec['models']['scGenModel']", 15, GRAY)
        dtitle.move_to([dframe.get_left()[0] + .15 + dtitle.width / 2, .35, 0])
        drule = line(dframe.get_left()[0], .15, dframe.get_right()[0], .15, FAINT, 1.5)
        specs = [("use_all_genes", "True"), ("x_dimension", "1000"), ("z_dimension", "50")]
        drawers = VGroup(*[drawer(k, v, dx, -.2 - i * .6, width=3.6, size=18)
                           for i, (k, v) in enumerate(specs)])
        dct = VGroup(dframe, dtitle, drule)
        zdr = drawers[2]
        zdr[3].set_opacity(0)                      # the value arrives with the token
        b2 = hop_ring(2, dframe)
        exact = left("open by its exact label", dframe.get_left()[0], -2.15, 18, RED)
        with self.say(1) as vo:
            self.cue(vo, .01, FadeOut(one), FadeOut(zv), FadeOut(latent), FadeOut(m30),
                     FadeOut(m32), ReplacementTransform(full, st1), ReplacementTransform(m38, s1_38),
                     ReplacementTransform(b1, b1s),
                     tok.animate.move_to(glyphs(st1.row(38), CONFIG[38], "50")), run_time=.7)
            vo.wait_until("safe load")
            l12 = link([-5.1, st1.frame.get_bottom()[1] + .02, 0], [-5.1, .57, 0])
            sl = mono("yaml.safe_load", 16, GRAY).next_to(l12, RIGHT, buff=.15)
            self.play(Create(l12), FadeIn(sl), FadeIn(dct), FadeIn(b2), run_time=.5)
            lag(self, *[FadeIn(d, shift=DOWN * .1) for d in drawers], lag_ratio=.2,
                run_time=.7)
            vo.wait_until("labelled drawers")
            lag(self, *[Indicate(d[2], color=INK, scale_factor=1.12) for d in drawers],
                lag_ratio=.15, run_time=.8)
            vo.wait_until("exact label")
            self.play(tok.animate.move_to(zdr[3]), zdr[2].animate.set_color(RED), run_time=.6)
            self.play(FadeIn(exact), run_time=.3)

        st3 = cpanel([(221, CORE[221])], CORE_PATH, 2.425, 1.45, width=7.75, size=18)
        b3 = hop_ring(3, st3.frame)
        obj = obj_card("scGenModel", ["lr = 0.001", "x_dimension = 1000", "z_dimension = 50"],
                       x=.75, y=-1.2, width=3.6, size=19, row_gap=.38)
        for r in obj.rows[:2]:
            r.set_color(GRAY)
        zrow = obj.rows[2]
        zrow.set_opacity(0)
        b4 = hop_ring(4, obj[0])
        with self.say(2) as vo:
            vo.wait_until("Hop three")
            self.play(FadeIn(st3, shift=LEFT * .1), FadeIn(b3), FadeOut(exact),
                      zdr[2].animate.set_color(INK), run_time=.5)
            vo.wait_until("hands the scGenModel")
            l23 = link(dframe.get_corner(UR), st3.frame.get_corner(DL) + RIGHT * .3)
            self.play(Create(l23), Indicate(dtitle, color=RED, scale_factor=1.06), run_time=.7)
            vo.wait_until("init opens")
            m221 = rmark(st3, 221)
            self.play(FadeIn(m221), run_time=.35)
            vo.wait_until("labelled z_dimension")
            key = glyphs(st3.row(221), CORE[221], "self.config['z_dimension']")
            zdr.generate_target()
            zdr.target.shift(RIGHT * .35)
            zdr.target[2].set_color(RED)
            self.play(MoveToTarget(zdr), run_time=.4)
            self.play(tok.animate.move_to(key).scale(.5).set_opacity(0),
                      key.animate.set_color(RED), run_time=.7)
            self.remove(tok)
            vo.wait_until("Hop four")
            zdr.generate_target()
            zdr.target.shift(LEFT * .35)
            zdr.target[2].set_color(INK)
            self.play(FadeIn(obj, shift=UP * .1), FadeIn(b4), MoveToTarget(zdr), run_time=.5)
            vo.wait_until("as self.z_dimension")
            attr0 = glyphs(st3.row(221), CORE[221], "self.z_dimension")
            tok = value_token().move_to(attr0)
            l34 = link(st3.frame.get_bottom() + LEFT * 2.5, obj[0].get_top() + RIGHT * .2)
            self.play(FadeIn(tok), key.animate.set_color(INK), run_time=.25)
            self.play(Create(l34), tok.animate.move_to(zrow.get_right() + LEFT * .22),
                      run_time=.7)
            self.play(zrow.animate.set_opacity(1), FadeOut(tok, scale=.6), run_time=.35)

        st3b = cpanel([(221, CORE[221]), (None, "        …"), (254, CORE[254])], CORE_PATH,
                      2.425, 1.14, width=7.75, size=18)
        m221b = rmark(st3b, 221)
        net = chip("network", 4.65, -1.0, INK, 22, font=LATIN)
        same = at("same spelling × 4", 4.65, -2.0, 28, RED, bold=True)
        with self.say(3) as vo:
            self.cue(vo, .01, ReplacementTransform(st3, st3b), ReplacementTransform(m221, m221b),
                     FadeOut(l34), FadeOut(l23), run_time=.6)
            vo.wait_until("line 254")
            m254 = rmark(st3b, 254)
            attr = glyphs(st3b.row(254), CORE[254], "self.z_dimension")
            self.play(ReplacementTransform(m221b, m254), run_time=.35)
            tok = value_token().move_to(zrow.get_right() + LEFT * .22)
            self.play(FadeIn(tok), run_time=.2)
            self.play(tok.animate.move_to(attr).scale(.5).set_opacity(0),
                      attr.animate.set_color(RED), run_time=.7)
            self.remove(tok)
            vo.wait_until("build the network")
            l5 = link(st3b.frame.get_bottom() + RIGHT * 2.2, net.get_top())
            tok = value_token().move_to(attr)
            self.play(Create(l5), FadeIn(net), FadeIn(tok), run_time=.4)
            self.play(tok.animate.move_to(net), attr.animate.set_color(INK), run_time=.5)
            self.play(FadeOut(tok, scale=.5), net[0].animate.set_stroke(RED), run_time=.3)
            vo.wait_until("Four hops")
            marks = VGroup(
                under(glyphs(st1.row(38), CONFIG[38], "z_dimension")),
                under(zdr[2]),
                under(glyphs(st3b.row(221), CORE[221], "z_dimension", 1)),
                under(glyphs(st3b.row(221), CORE[221], "z_dimension", 0)),
                under(glyphs(zrow, "z_dimension = 50", "z_dimension")),
                under(glyphs(st3b.row(254), CORE[254], "z_dimension", 1)))
            self.play(net[0].animate.set_stroke(INK), run_time=.2)
            lag(self, *[Create(u) for u in marks], lag_ratio=.18, run_time=.9)
            self.play(FadeIn(same, shift=UP * .1), run_time=.4)
            vo.wait_until("jumping between files")
            tabs = [p.tab for p in (st1, st3b)]
            self.play(*[Indicate(t, color=RED, scale_factor=1.1) for t in tabs], run_time=.7)
        self.finish()


# ================================================================ s04

def empty_drawer(label_, x, y, width=3.4, size=20, color=GRAY):
    body = DashedVMobject(Rectangle(width=width, height=.56, color=color, stroke_width=2),
                          num_dashes=36).move_to([x, y, 0])
    lab = mono(f"'{label_}'", size, color)
    lab.move_to([x - width / 2 + .16 + lab.width / 2, y, 0])
    q = mono("?", size, color).move_to([x + width / 2 - .3, y, 0])
    return VGroup(body, lab, q)


def probe(text, size=18):
    """A lookup in flight: the key being asked for, in a red outline."""
    return chip(text, 0, 0, RED, size).set_z_index(8)


class S04(Ep):
    def construct(self):
        self.header()
        cx = [-3.2, 3.2]
        divider = line(0, 1.8, 0, -2.3, FAINT, 1.5)
        heads = VGroup(mono("config['key']", 26, INK).move_to([cx[0], 1.6, 0]),
                       mono("self.name", 26, INK).move_to([cx[1], 1.6, 0]))
        kinds = VGroup(at("dictionary lookup · 查抽屉", cx[0], 1.1, 19, GRAY),
                       at("attribute lookup · 问对象", cx[1], 1.1, 19, GRAY))
        dl = VGroup(drawer("lr", "0.001", cx[0], .45, width=3.4, size=19),
                    drawer("z_dimension", "50", cx[0], -.15, width=3.4, size=19))
        slot = empty_drawer("key", cx[0], -.75, width=3.4, size=19)
        ob = obj_card("scGenModel", ["lr = 0.001", "z_dimension = 50"], x=cx[1], y=-.05,
                      width=3.4, size=19, row_gap=.38)
        errs = VGroup(chip("KeyError", cx[0], -1.65, GRAY, 24),
                      chip("AttributeError", cx[1], -1.65, GRAY, 24))
        whys = VGroup(at("missing drawer · 少了抽屉", cx[0], -2.28, 18, GRAY),
                      at("missing fact · 少了事实", cx[1], -2.28, 18, GRAY))
        ex_tag = tag_at("EXAMPLE", 5.65, 1.85)
        with self.say(0) as vo:
            self.cue(vo, .02, Create(divider), FadeIn(heads[0], shift=DOWN * .08),
                     FadeIn(heads[1], shift=DOWN * .08), FadeIn(kinds), FadeIn(ex_tag),
                     run_time=.6)
            self.play(FadeIn(dl), FadeIn(ob), run_time=.4)
            vo.wait_until("each one fails")
            lag(self, FadeIn(errs[0]), FadeIn(errs[1]), lag_ratio=.3, run_time=.6)
            vo.wait_until("Opening a drawer")
            pr = probe("'key'").move_to(heads[0].get_right() + RIGHT * .7)
            self.play(FadeIn(pr, scale=.8), FadeIn(slot), run_time=.4)
            self.play(pr.animate.move_to([cx[0] + 2.35, -.75, 0]), run_time=.7)
            vo.wait_until("raises a key error")
            self.play(slot[0].animate.set_color(RED), errs[0][0].animate.set_stroke(RED),
                      errs[0][1].animate.set_color(RED), FadeIn(whys[0]), FadeOut(pr),
                      run_time=.45)

        toy = cpanel(rows(TOY_CONFIG, 14, 19), TOY_PATH, -3.75, .72, width=5.1, size=18)
        toy_s = plural_s(toy.row(19), TOY_CONFIG[19])
        with self.say(1) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()], FadeIn(toy, shift=UP * .1),
                     run_time=.6)
            vo.wait_until("spells it")
            m19 = rmark(toy, 19)
            self.play(FadeIn(m19), Circumscribe(toy_s, color=RED, buff=.05), run_time=.6)
            vo.wait_until("Will init")
            card = ponder("init 会抛出 KeyError，还是 AttributeError？",
                          "Will __init__ raise a KeyError or an AttributeError?", y=-1.2)
            self.play(self.veil(), run_time=.4)
            self.play(FadeIn(card, shift=UP * .1), run_time=.5)
        self.hold(1)

        dspec = [("random_state", "0"), ("hidden_units", "[256, 256]"), ("lr", "0.001"),
                 ("use_all_genes", "True"), ("x_dimensions", "1000")]
        dx = -4.25
        dstack = VGroup(*[drawer(k, v, dx, 1.35 - i * .6, width=4.0, size=17)
                          for i, (k, v) in enumerate(dspec)])
        ds_s = plural_s(dstack[4][2], "'x_dimensions'")
        miss = empty_drawer("x_dimension", dx, 1.35 - 5 * .6 - .12, width=4.0, size=17)
        dhead = mono("toy_config['models']['scGenModel']", 15, GRAY).move_to([dx, 1.85, 0])
        p220 = cpanel([(220, CORE[220])], CORE_PATH, 2.8, 1.5, width=7.0, size=16)
        answer = mono("KeyError", 40, RED, bold=True).move_to([3.3, -.5, 0])
        kerr = error_card("KeyError", KEY_MSG, "speciesot_core.py:220 in __init__", 3.3, -.8,
                          width=6.0, size=22)
        kerr[2].set_z_index(6)
        with self.say(2) as vo:
            self.cue(vo, .01, FadeOut(card), self.unveil(), run_time=.4)
            self.play(FadeIn(answer, scale=1.2), run_time=.4)
            vo.wait_until("Build scGenModel")
            self.play(FadeOut(m19), ReplacementTransform(toy, dstack), FadeIn(dhead),
                      run_time=.8)
            vo.wait_until("line 220")
            m220 = rmark(p220, 220)
            self.play(FadeIn(p220, shift=LEFT * .1), run_time=.4)
            self.play(FadeIn(m220), run_time=.3)
            key = glyphs(p220.row(220), CORE[220], "'x_dimension'")
            pr = probe("'x_dimension'", 17).move_to(key)
            self.play(FadeIn(pr), run_time=.25)
            self.play(pr.animate.move_to([dx + 2.0 + pr.width / 2 + .15, dstack[0].get_y(), 0]),
                      run_time=.5)
            lag(self, *[Indicate(d[2], color=INK, scale_factor=1.08) for d in dstack],
                lag_ratio=.15, run_time=.8,
                extra=[pr.animate.move_to([dx + 2.0 + pr.width / 2 + .15, dstack[4].get_y(), 0])])
            self.play(Circumscribe(ds_s, color=RED, buff=.04), run_time=.4)
            self.play(ReplacementTransform(answer, kerr[2]), FadeIn(VGroup(*kerr[:2], *kerr[3:])),
                      run_time=.5)
            vo.wait_until("The drawer it asked")
            self.play(FadeIn(miss), pr.animate.move_to([dx + 2.0 + pr.width / 2 + .15,
                                                        miss.get_y(), 0]), run_time=.5)
            self.play(miss[0].animate.set_color(RED), miss[1].animate.set_color(RED),
                      run_time=.3)

        attrs = ["random_state = 0", "lr = 0.001", "use_all_genes = True", "x_dimension = 1000",
                 "z_dimension = 50"]
        obj = obj_card("scGenModel", attrs, x=-4.55, y=.55, width=3.5, size=18, row_gap=.38)
        xrow = obj.rows[3]
        p253 = cpanel(rows(CORE, 252, 253), CORE_PATH, 3.17, 1.36, width=6.26, size=18)
        s253 = plural_s(p253.row(253), CORE[253])
        aerr = error_card("AttributeError", ATTR_MSG, "speciesot_core.py:253 in setup", 1.95,
                          -1.42, width=8.6, size=19, tag=None)
        plural_s(aerr[3][0], ATTR_MSG)
        atag = tag_text("MEASURED · stand-in scgen")
        atag.move_to([aerr[0].get_right()[0] - atag.width / 2 - .14,
                      aerr[0].get_top()[1] - .34, 0]).set_z_index(6)
        with self.say(3) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()], run_time=.4)
            self.play(FadeIn(obj, shift=RIGHT * .1), FadeIn(p253, shift=LEFT * .1), run_time=.5)
            vo.wait_until("never received")
            noslot = VGroup(DashedVMobject(Rectangle(width=obj[0].width, height=.5, color=GRAY,
                                                     stroke_width=2), num_dashes=40),
                            mono("x_dimensions = ?", 18, GRAY))
            noslot.move_to([obj.get_x(), obj.get_bottom()[1] - .4, 0])
            noslot[1].move_to([obj[0].get_left()[0] + .22 + noslot[1].width / 2, noslot.get_y(), 0])
            plural_s(noslot[1], "x_dimensions = ?")
            self.play(Create(noslot[0]), FadeIn(noslot[1]), run_time=.5)
            pr = probe("x_dimensions", 17).move_to([1.2, -.2, 0])
            pr[1].set_color(INK)
            plural_s(pr[1], "x_dimensions")
            vo.wait_until("line 253")
            m253 = rmark(p253, 253)
            attr = glyphs(p253.row(253), CORE[253], "self.x_dimensions")
            self.play(FadeIn(m253), run_time=.3)
            pr.move_to(attr)
            self.play(FadeIn(pr), run_time=.2)
            self.play(pr.animate.next_to(xrow, RIGHT, buff=.45), run_time=.6)
            vo.wait_until("init only ever wrote")
            self.play(Indicate(xrow, color=RED, scale_factor=1.08), run_time=.5)
            self.play(FadeIn(aerr, shift=UP * .1), FadeIn(atag, shift=UP * .1), run_time=.45)

        tb = ["Traceback (most recent call last):",
              "  …",
              "  File \".../speciesot_core.py\", line 119, in setup",
              "    model.setup()",
              "  File \".../speciesot_core.py\", line 253, in setup",
              "    x_dimension= self.x_dimensions,",
              "AttributeError: 'scGenModel' object has no attribute 'x_dimensions'.",
              "Did you mean: 'x_dimension'?"]
        term = tb_block(tb, -.75, .3, width=11.1, size=19)
        lines = term.lines
        g = term.gap
        tx = term.box.get_right()[0]
        ly_ = [term.box.get_top()[1] - .18 - g / 2 - i * g for i in range(len(tb))]
        what = bracket(tx + .18, ly_[6] + g / 2 - .03, ly_[7] - g / 2, "WHAT", RED, 22)
        where = bracket(tx + .18, ly_[4] + g / 2, ly_[5] - g / 2 + .03, "WHERE", RED, 22)
        ttag = tag_text("MEASURED frames · stand-in scgen · message text from Python 3.12")
        ttag.move_to([term.box.get_left()[0] + ttag.width / 2, term.box.get_bottom()[1] - .3, 0])
        cursor = Triangle(fill_color=RED, fill_opacity=1, stroke_width=0).scale(.11)\
            .rotate(-PI / 2).set_z_index(8)
        with self.say(4) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()], run_time=.35)
            self.play(FadeIn(term, shift=UP * .1), FadeIn(ttag), run_time=.5)
            vo.wait_until("start at the bottom")
            cursor.move_to([term.box.get_left()[0] - .2, ly_[7], 0])
            self.play(FadeIn(cursor, shift=RIGHT * .1), run_time=.3)
            vo.wait_until("The last line says")
            self.play(cursor.animate.move_to([cursor.get_x(), ly_[6], 0]),
                      lines[6].animate.set_color(PAPER), Create(what[0]), FadeIn(what[1]),
                      run_time=.5)
            vo.wait_until("did you mean")
            self.play(cursor.animate.move_to([cursor.get_x(), ly_[7], 0]),
                      lines[7].animate.set_color(RED), run_time=.45)
            vo.wait_until("Just above it")
            self.play(cursor.animate.move_to([cursor.get_x(), ly_[4], 0]),
                      lines[7].animate.set_color(PAPER), lines[4].animate.set_color(PAPER),
                      lines[5].animate.set_color(PAPER), run_time=.5)
            vo.wait_until("says where")
            self.play(Create(where[0]), FadeIn(where[1]), what[0].animate.set_color(INK),
                      what[1].animate.set_color(INK), run_time=.45)

        ly = [.95, -.85]
        xs = [-.4, 2.6]
        lane_lab = VGroup(
            VGroup(left("stand-in scgen", -6.1, ly[0] + .2, 22, INK, bold=True),
                   left("what we measured", -6.1, ly[0] - .22, 18, GRAY)),
            VGroup(left("on the cluster", -6.1, ly[1] + .2, 22, INK, bold=True),
                   left("scvi-tools scgen 2.1.0", -6.1, ly[1] - .22, 18, GRAY)))
        rails = VGroup(*[line(-2.4, y, 4.2, y, FAINT, 2) for y in ly])
        stops = VGroup(*[VGroup(*[chip(f"line {n}", x, y, INK, 19) for n, x in zip((252, 253), xs)])
                         for y in ly])
        res_a = mono("AttributeError", 18, RED).next_to(stops[0][1], DOWN, buff=.18)
        mark_a = mono("✓", 22, INK).next_to(stops[0][0], UP, buff=.12)
        res_b = left("no VAEArith in 2.1.0", -2.2, ly[1] - .62, 18, RED)
        e4 = chip("episode 4", 5.25, ly[1], RED, 20, font=LATIN)
        tags = VGroup(source_tag("MEASURED").move_to([5.25, ly[0], 0]),
                      source_tag("INFERRED").move_to([5.25, ly[1] - .62, 0]))
        with self.say(5) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()], run_time=.35)
            self.play(FadeIn(lane_lab[0]), Create(rails[0]), FadeIn(stops[0]), FadeIn(tags[0]),
                      run_time=.5)
            t1 = token([-2.4, ly[0], 0])
            self.play(FadeIn(t1), run_time=.15)
            self.play(t1.animate.move_to(stops[0][0].get_left() + LEFT * .2), run_time=.4)
            self.play(t1.animate.move_to(stops[0][1].get_left() + LEFT * .2), FadeIn(mark_a),
                      run_time=.5)
            self.play(FadeIn(res_a), stops[0][1][0].animate.set_stroke(RED), run_time=.35)
            vo.wait_until("On the cluster")
            self.play(FadeIn(lane_lab[1]), Create(rails[1]), FadeIn(stops[1]), run_time=.5)
            t2 = token([-2.4, ly[1], 0])
            self.play(FadeIn(t2), run_time=.15)
            self.play(t2.animate.move_to(stops[1][0].get_left() + LEFT * .2), run_time=.45)
            self.play(stops[1][0][0].animate.set_stroke(RED), FadeIn(res_b), FadeIn(tags[1]),
                      run_time=.4)
            vo.wait_until("Episode four")
            arr = arrow(stops[1][0].get_right(), e4.get_left(), RED)
            self.play(GrowArrow(arr), FadeIn(e4), FadeOut(stops[1][1]), run_time=.5)
        self.finish()


# ================================================================ s05

def dict_frame(title, x_left, top, width, height, size=15):
    frame = Rectangle(width=width, height=height, stroke_color=INK, stroke_width=2,
                      fill_color=PAPER, fill_opacity=1)
    frame.move_to([x_left + width / 2, top - height / 2, 0])
    t = mono(title, size, GRAY)
    t.move_to([x_left + .15 + t.width / 2, top - .2, 0])
    rule = line(x_left, top - .4, x_left + width, top - .4, FAINT, 1.5)
    g = VGroup(frame, t, rule)
    g.frame, g.title = frame, t
    return g


class S05(Ep):
    def construct(self):
        self.header()
        p = cpanel(rows(CORE, 97, 104), CORE_PATH, 0, .58, width=12.5, size=16)
        typed = chip("x_dimension: 1000", -3.4, -1.85, GRAY, 20)
        real = chip("source_adata.shape[1]", 2.9, -1.85, INK, 20)
        typed_l = left("typed by hand · config.yaml:37", typed.get_left()[0], -1.32, 17, GRAY)
        real_l = left("read from the data", real.get_left()[0], -1.32, 17, GRAY)
        repl = arrow(real.get_left(), typed.get_right(), RED)
        with self.say(0) as vo:
            self.cue(vo, .02, FadeIn(p, shift=UP * .1), run_time=.5)
            vo.wait_until("When use_all_genes")
            m = rmark(p, 101)
            self.play(FadeIn(m), run_time=.4)
            vo.wait_until("typed gene count")
            self.play(FadeIn(typed), FadeIn(typed_l), run_time=.4)
            vo.wait_until("read from the data")
            self.play(FadeIn(real), FadeIn(real_l), run_time=.4)
            self.play(GrowArrow(repl), run_time=.5)
            vo.wait_until("Line 104")
            m2 = rmark(p, 104)
            self.play(ReplacementTransform(m, m2), run_time=.4)

        p104 = cpanel([(104, CORE[104])], CORE_PATH, -1.0, 1.55, width=10.6, size=16)
        s104 = plural_s(p104.row(104), CORE[104])[0]
        m104 = rmark(p104, 104)
        dfr = dict_frame("model_config   (toy data, 4 genes)", -6.3, .55, 4.6, 1.75)
        dsing = drawer("x_dimension", "1000", -4.0, -.12, width=4.3, size=19)
        dplur = drawer("x_dimensions", "4", -4.0, -.74, width=4.3, size=19)
        plural_s(dplur[2], "'x_dimensions'")
        dsing.set_z_index(1)
        dplur.set_z_index(1)
        lab1 = left("singular · typed by hand", -1.3, -.12, 18, GRAY)
        lab2 = left("with an s · the real count", -1.3, -.74, 18, GRAY)
        with self.say(1) as vo:
            self.cue(vo, .01, FadeOut(m2), FadeOut(repl), FadeOut(typed_l), FadeOut(real_l),
                     ReplacementTransform(p, p104), run_time=.6)
            self.play(FadeIn(m104), run_time=.3)
            vo.wait_until("x_dimensions, with an s")
            s104.set_color(RED)
            self.play(Circumscribe(s104, color=RED, buff=.05), run_time=.6)
            vo.wait_until("two drawers")
            self.play(FadeIn(dfr), ReplacementTransform(typed, dsing), run_time=.6)
            vo.wait_until("x_dimension, singular")
            self.play(FadeIn(lab1, shift=RIGHT * .1), Indicate(dsing[2], color=INK), run_time=.5)
            vo.wait_until("and x_dimensions")
            key = glyphs(p104.row(104), CORE[104], '"x_dimensions"')
            self.play(ReplacementTransform(real, dplur), FadeIn(lab2, shift=RIGHT * .1),
                      Indicate(key, color=RED), run_time=.8)
            snap = tag_text("MEASURED · stand-in scgen")
            snap.move_to([-6.3 + snap.width / 2, -1.5, 0])
            self.play(FadeIn(snap), run_time=.3)

        p220 = cpanel([(220, CORE[220])], CORE_PATH, -2.8, 1.55, width=7.0, size=16)
        m220 = rmark(p220, 220)
        out_rows = [(i + 1, t) for i, t in enumerate(E24_OUTPUTS[3].split("\n"))]
        nb = cpanel(out_rows, NB_PATH + " · Out", 4.05, -.53, width=4.5, size=17, numbers=False)
        plural_s(nb.row(5), out_rows[4][1])
        nb_tag = source_tag("READ IN NOTEBOOK").move_to([4.05, -1.92, 0])
        nb_note = at("real mouse training file, older config", 4.05, -2.3, 16, GRAY)
        nobody = left("nobody reads this drawer", -1.3, -.74, 18, RED)
        with self.say(2) as vo:
            self.cue(vo, .01, FadeOut(m104), ReplacementTransform(p104, p220), run_time=.6)
            self.play(FadeIn(m220), run_time=.3)
            key = glyphs(p220.row(220), CORE[220], "'x_dimension'")
            ask = arrow(key.get_bottom() + DOWN * .05, dsing.get_corner(UR) + RIGHT * .25, RED)
            self.play(GrowArrow(ask), run_time=.45)
            dsing.generate_target()
            dsing.target.shift(RIGHT * .3)
            dsing.target[2].set_color(RED)
            self.play(MoveToTarget(dsing), run_time=.4)
            vo.wait_until("nobody reads")
            self.play(dplur.animate.set_opacity(.35), ReplacementTransform(lab2, nobody),
                      run_time=.6)
            vo.wait_until("Josh's notebook")
            self.play(FadeIn(nb, shift=LEFT * .1), FadeIn(nb_tag), FadeIn(nb_note), run_time=.5)
            vo.wait_until("eighteen thousand")
            m5 = rmark(nb, 5)
            self.play(FadeIn(m5), run_time=.4)
            link_ = DashedLine(nb.frame.get_left() + DOWN * .72, dplur.get_corner(DR) + RIGHT * .05,
                               color=GRAY, stroke_width=2)
            vo.wait_until("nothing reads it")
            self.play(Create(link_), run_time=.5)

        with self.say(3) as vo:
            card = ponder("基因数该手写进配置，还是永远从数据里来？",
                          "Typed into the config, or always read from the data?", y=-1.1)
            self.cue(vo, .05, self.veil(), run_time=.5)
            self.play(FadeIn(card, shift=UP * .1), run_time=.5)
        self.hold(3)
        self.finish()


# ================================================================ s06

def rule_card(n, title, x, y, w=6.2, h=2.05):
    frame = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=2, fill_color=PAPER,
                      fill_opacity=1).move_to([x, y, 0])
    L, T = frame.get_left()[0], frame.get_top()[1]
    ring = Circle(radius=.2, color=RED, stroke_width=3).move_to([L + .4, T - .38, 0])
    num = Text(str(n), font=LATIN, font_size=20, color=RED, weight=BOLD).move_to(ring)
    t = left(title, L + .75, T - .38, 24, INK, bold=True)
    g = VGroup(frame, ring, num, t)
    g.L, g.T = L, T
    return g


class S06(Ep):
    def construct(self):
        self.header()
        xs, ys = [-3.2, 3.2], [1.0, -1.35]
        slots = VGroup(*[DashedVMobject(Rectangle(width=6.2, height=2.05, color=FAINT,
                                                  stroke_width=2), num_dashes=60)
                         .move_to([xs[i % 2], ys[i // 2], 0]) for i in range(4)])
        with self.say(0) as vo:
            self.cue(vo, .05, run_time=.1)
            lag(self, *[Create(sl) for sl in slots], lag_ratio=.2, run_time=.9)

        c1 = rule_card(1, "one spelling", xs[0], ys[0])
        L, T = c1.L, c1.T
        r1 = [("config.yaml", CONFIG[37].strip()), ("__init__", "self.config['x_dimension']"),
              ("attribute", "self.x_dimension")]
        rows1 = VGroup()
        for i, (k, code) in enumerate(r1):
            yy = T - .88 - i * .36
            rows1.add(VGroup(left(k, L + .35, yy, 17, GRAY), mono_left(code, L + 1.95, yy, 17)))
        unders1 = VGroup(*[under(glyphs(r[1], code, "x_dimension"), buff=.04, stroke=2.5)
                           for r, (_, code) in zip(rows1, r1)])
        c2 = rule_card(2, "derived values are derived", xs[1], ys[0])
        L2, T2 = c2.L, c2.T
        ex2 = mono_left("x_dimension = data.shape[1]", L2 + .35, T2 - .9, 17)
        tag2 = source_tag("EXAMPLE")
        tag2.move_to([L2 + 6.2 - .15 - tag2.width / 2, T2 - 2.05 + .3, 0])
        cells = VGroup(*[Square(.18, stroke_color=INK, stroke_width=1.5).move_to(
            [L2 + .55 + c * .22, T2 - 1.4 - r * .21, 0]) for r in range(3) for c in range(4)])
        top_line = line(L2 + .46, T2 - 1.21, L2 + 1.30, T2 - 1.21, INK, 2)
        glab = left("data: 3 cells × 4 genes", L2 + 1.6, T2 - 1.6, 17, GRAY)
        with self.say(1) as vo:
            vo.wait_until("One:")
            self.play(FadeIn(c1), FadeOut(slots[0]), run_time=.45)
            lag(self, *[FadeIn(r, shift=RIGHT * .08) for r in rows1], lag_ratio=.25, run_time=.7)
            vo.wait_until("exactly one name")
            lag(self, *[Create(u) for u in unders1], lag_ratio=.25, run_time=.8)
            vo.wait_until("Two:")
            self.play(FadeIn(c2), FadeOut(slots[1]), FadeIn(ex2), FadeIn(tag2),
                      *[u.animate.set_color(INK) for u in unders1], run_time=.45)
            vo.wait_until("the data can tell you")
            self.play(FadeIn(cells), Create(top_line), FadeIn(glab), run_time=.5)
            four = mono("4", 20, RED, bold=True).move_to(top_line.get_center() + UP * .16)
            self.play(FadeIn(four, scale=1.3), run_time=.3)
            target = ex2.get_right() + RIGHT * .5
            arrow4 = mono("→", 18, GRAY).move_to(ex2.get_right() + RIGHT * .22)
            self.play(four.animate.move_to(target), FadeIn(arrow4), run_time=.6)

        c3 = rule_card(3, "fail early", xs[0], ys[1])
        L3, T3 = c3.L, c3.T
        ex3 = mono_left("KeyError inside __init__", L3 + .35, T3 - .9, 17)
        tl = line(L3 + .4, T3 - 1.5, L3 + 5.8, T3 - 1.5, INK, 2)
        ta, tb_ = L3 + .9, L3 + 5.0
        ticks = VGroup(line(ta, T3 - 1.4, ta, T3 - 1.6, INK, 2), line(tb_, T3 - 1.4, tb_, T3 - 1.6,
                                                                    INK, 2))
        tla = mono("__init__", 16, INK).move_to([ta, T3 - 1.82, 0])
        tlb = left("1 h into training", tb_ - .9, T3 - 1.82, 17, GRAY)
        xa = mono("✗", 30, RED, bold=True).move_to([ta, T3 - 1.18, 0])
        xb = mono("✗", 30, FAINT, bold=True).move_to([tb_, T3 - 1.18, 0])
        with self.say(2) as vo:
            vo.wait_until("Three:")
            self.play(FadeIn(c3), FadeOut(slots[2]), FadeIn(ex3), four.animate.set_color(INK),
                      run_time=.45)
            vo.wait_until("the moment the object")
            self.play(Create(tl), FadeIn(ticks), FadeIn(tla), FadeIn(tlb), run_time=.6)
            tok = token([L3 + .4, T3 - 1.5, 0], r=.08)
            self.play(FadeIn(tok), run_time=.15)
            self.play(tok.animate.move_to([ta, T3 - 1.5, 0]), run_time=.4)
            vo.wait_until("explodes inside init")
            self.play(FadeIn(xa, scale=1.6), FadeOut(tok), run_time=.4)
            vo.wait_until("not an hour")
            self.play(FadeIn(xb), run_time=.3)
            self.play(Create(strike(xb, GRAY, 3)), run_time=.3)

        c4 = rule_card(4, "search after a rename", xs[1], ys[1])
        L4, T4 = c4.L, c4.T
        cmd = 'grep -rn "x_dimensions" .'
        ex4 = mono_left(cmd, L4 + .35, T4 - .9, 17)
        plural_s(ex4, cmd)
        tag4 = source_tag("EXAMPLE")
        tag4.move_to([L4 + 6.2 - .15 - tag4.width / 2, T4 - .38, 0])
        files = ["src/speciesot/*.py", "Tests/*.yaml", "Tests/*.ipynb"]
        frows = VGroup(*[mono_left(f, L4 + .35, T4 - 1.28 - i * .29, 16, GRAY)
                         for i, f in enumerate(files)])
        rerun = chip("↻ rerun smallest example", 0, 0, INK, 16, font=LATIN)
        rerun.move_to([L4 + 6.2 - .2 - rerun.width / 2, T4 - 1.72, 0])
        with self.say(3) as vo:
            vo.wait_until("Four:")
            self.play(FadeIn(c4), FadeOut(slots[3]), FadeIn(ex4), FadeIn(tag4),
                      xa.animate.set_color(INK), run_time=.45)
            vo.wait_until("search the whole")
            scan = line(L4 + .3, T4 - 1.1, L4 + .3, T4 - 1.98, RED, 3)
            self.play(FadeIn(frows), FadeIn(scan), run_time=.3)
            self.play(scan.animate.shift(RIGHT * 4.0), run_time=.7)
            vo.wait_until("YAML files included")
            self.play(FadeOut(scan), frows[1].animate.set_color(RED), run_time=.4)
            vo.wait_until("Then rerun")
            self.play(FadeIn(rerun, shift=LEFT * .1), frows[1].animate.set_color(INK),
                      run_time=.4)

        tp = cpanel([(n, TOY_CONFIG[n]) for n in (1, 7, 12, 21)], TOY_PATH, -4.5, .62,
                    width=3.6, size=17)
        gap_box = VGroup(DashedVMobject(Rectangle(width=2.15, height=.5, color=RED,
                                                  stroke_width=2), num_dashes=26),
                         mono("experiment:", 17, RED))
        gap_box.move_to([-1.45, 1.15, 0])
        gap_box[1].move_to(gap_box[0])
        gap_note = at("missing", -1.45, .7, 17, RED)
        kerr = error_card("KeyError", "'experiment'", "speciesot_core.py:86 in setup", -3.35,
                          -1.38, width=5.9, size=20)
        t1 = left("trap 1 · toy config drifted", -6.3, 1.82, 22, INK, bold=True)
        t2 = left("trap 2 · YAML None", .4, 1.82, 22, INK, bold=True)
        div = line(0, 1.95, 0, -2.4, FAINT, 1.5)
        ra = mono_left(CONFIG[31].strip(), .4, 1.05, 19)
        ra_src = left("config.yaml:31", .4, .68, 16, GRAY)
        rb = mono_left("Other: null", .4, .05, 19)
        a1 = arrow([3.55, 1.05, 0], [4.45, 1.05, 0], INK)
        a2 = arrow([3.55, .05, 0], [4.45, .05, 0], INK)
        va = chip("'None'", 5.35, 1.05, RED, 19)
        vb = chip("None", 5.35, .05, INK, 19)
        la = at("a str", 5.35, .55, 16, RED)
        lb = at("empty", 5.35, -.45, 16, GRAY)
        meas = mono_left("{'IdentityModel': 'None', 'Other': None}", .4, -1.15, 17)
        msrc = left("yaml.safe_load of these two lines", .4, -1.62, 17, GRAY)
        mtag = source_tag("MEASURED").move_to([5.55, -1.62, 0])
        with self.say(4) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()], run_time=.35)
            self.play(FadeIn(t1), FadeIn(t2), Create(div), run_time=.35)
            vo.wait_until("toy config has drifted")
            self.play(FadeIn(tp, shift=UP * .1), run_time=.4)
            vo.wait_until("no experiment section")
            self.play(Create(gap_box[0]), FadeIn(gap_box[1]), FadeIn(gap_note), run_time=.45)
            vo.wait_until("line 86")
            self.play(FadeIn(kerr, shift=UP * .1), run_time=.45)
            vo.wait_until("None is just")
            self.play(FadeIn(ra), FadeIn(ra_src), GrowArrow(a1), run_time=.4)
            vo.wait_until("a string")
            self.play(FadeIn(va, shift=RIGHT * .1), FadeIn(la), run_time=.35)
            vo.wait_until("spells an empty value")
            self.play(FadeIn(rb), GrowArrow(a2), FadeIn(vb, shift=RIGHT * .1), FadeIn(lb),
                      run_time=.4)
            self.play(FadeIn(meas), FadeIn(msrc), FadeIn(mtag), run_time=.4)
        self.finish()


# ================================================================ s07

class S07(Ep):
    def construct(self):
        self.header()
        hx = [-4.65, -1.55, 1.55, 4.65]
        hy = 1.45
        names = ["a YAML line", "a dictionary drawer", "init", "an attribute"]
        codes = ["z_dimension: 50", "['z_dimension']", "self.config[…]", "self.z_dimension"]
        boxes = VGroup(*[RoundedRectangle(corner_radius=.06, width=2.75, height=.95,
                                          stroke_color=INK, stroke_width=2, fill_color=PAPER,
                                          fill_opacity=1).move_to([x, hy, 0]) for x in hx])
        caps = VGroup(*[at(n, x, hy + .2, 19, GRAY) for n, x in zip(names, hx)])
        cods = VGroup(*[mono(c, 17, INK).move_to([x, hy - .2, 0]) for c, x in zip(codes, hx)])
        badges = VGroup(*[hop_badge(i + 1, x - 1.375, hy + .475, r=.17)
                          for i, x in enumerate(hx)])
        links = VGroup(*[Arrow([hx[i] + 1.4, hy, 0], [hx[i + 1] - 1.4, hy, 0], buff=0,
                               color=GRAY, stroke_width=2, tip_length=.14,
                               max_tip_length_to_length_ratio=1) for i in range(3)])
        same = at("same spelling at every hop", 0, .62, 22, RED, bold=True)
        with self.say(0) as vo:
            vo.wait_until("four hops")
            self.play(FadeIn(boxes), FadeIn(badges), Create(links), run_time=.5)
            for i, w in enumerate(("a YAML line", "a dictionary drawer", "init,",
                                   "an attribute")):
                vo.wait_until(w)
                self.play(FadeIn(caps[i]), FadeIn(cods[i], shift=UP * .06), run_time=.35)
            tok = token([hx[0] - 1.1, hy - .2, 0], r=.08)
            vo.wait_until("Every hop")
            path = VMobject().set_points_as_corners([[hx[0] - 1.1, hy - .52, 0],
                                                     [hx[3] + 1.1, hy - .52, 0]])
            self.play(FadeIn(tok), run_time=.1)
            tok.move_to(path.get_start())
            self.play(MoveAlongPath(tok, path), FadeIn(same), run_time=1.0)
            self.play(FadeOut(tok), run_time=.2)

        cx = [-3.2, 3.2]
        k_chip = chip("KeyError", cx[0], -.25, INK, 24)
        a_chip = chip("AttributeError", cx[1], -.25, INK, 24)
        k_txt = at("a drawer is missing · 少了抽屉", cx[0], -.85, 20, GRAY)
        a_txt = at("the object never got the fact · 少了事实", cx[1], -.85, 20, GRAY)
        quiet = VGroup(left("a quiet bug can hide behind a fixed crash", -6.1, -1.7, 24, RED,
                            bold=True),
                       mono_left("x_dimension = 1000  ≠  4 genes", 1.95, -1.7, 19, INK))
        quiet[1].move_to([6.3 - quiet[1].width / 2, -1.7, 0])
        with self.say(1) as vo:
            self.cue(vo, .02, same.animate.set_color(INK), run_time=.3)
            vo.wait_until("A key error")
            self.play(FadeIn(k_chip, shift=UP * .08), run_time=.35)
            vo.wait_until("a drawer is missing")
            self.play(FadeIn(k_txt), k_chip[0].animate.set_stroke(RED), k_chip[1].animate.set_color(RED),
                      run_time=.4)
            vo.wait_until("An attribute error")
            self.play(FadeIn(a_chip, shift=UP * .08), k_chip[0].animate.set_stroke(INK),
                      k_chip[1].animate.set_color(INK), run_time=.35)
            vo.wait_until("never got the fact")
            self.play(FadeIn(a_txt), a_chip[0].animate.set_stroke(RED),
                      a_chip[1].animate.set_color(RED), run_time=.4)
            vo.wait_until("And a quiet bug")
            self.play(FadeIn(quiet[0], shift=RIGHT * .1), a_chip[0].animate.set_stroke(INK),
                      a_chip[1].animate.set_color(INK), run_time=.45)
            self.play(FadeIn(quiet[1]), run_time=.35)

        title = left("exercise · 练习", -6.3, 1.75, 26, INK, bold=True)
        places = [(CFG_PATH + ":37", CONFIG[37].strip()), (TOY_PATH + ":19", TOY_CONFIG[19].strip()),
                  ("speciesot_core.py:104", 'model_config["x_dimensions"] = …'),
                  ("speciesot_core.py:220", CORE[220].strip()),
                  ("speciesot_core.py:253", CORE[253].strip())]
        rows_ = VGroup()
        boxes2 = VGroup()
        for i, (where, code) in enumerate(places):
            yy = 1.12 - i * .5
            b = Square(.26, stroke_color=INK, stroke_width=2).move_to([-6.05, yy, 0])
            w = mono_left(where, -5.7, yy, 17, GRAY)
            c = mono_left(code, -1.25, yy, 18, INK)
            plural_s(c, code)
            boxes2.add(b)
            rows_.add(VGroup(b, w, c))
        rerun = chip("then rerun e24_replica.ipynb", -2.55, -1.55, INK, 20, font=LATIN)
        e5 = VGroup(left("which data should the number come from?", 1.0, -1.55, 20, GRAY),
                    chip("episode 5", 5.4, -1.55, RED, 19, font=LATIN))
        e5[0].move_to([e5[1].get_left()[0] - .25 - e5[0].width / 2, -2.15, 0])
        e5[1].move_to([5.4, -2.15, 0])
        with self.say(2) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()], run_time=.4)
            self.play(FadeIn(title), run_time=.3)
            vo.wait_until("both spellings")
            lag(self, *[FadeIn(r, shift=RIGHT * .08) for r in rows_], lag_ratio=.15,
                run_time=.9)
            vo.wait_until("Pick one")
            pick = VGroup(chip("x_dimension", 2.75, 1.75, INK, 20),
                          chip("x_dimensions", 5.15, 1.75, INK, 20))
            plural_s(pick[1][1], "x_dimensions")
            orr = at("or", 3.95, 1.75, 19, GRAY)
            plab = left("pick one:", .2, 1.75, 19, GRAY)
            self.play(FadeIn(pick), FadeIn(orr), FadeIn(plab), run_time=.4)
            vo.wait_until("both YAML files")
            self.play(*[Indicate(rows_[i][1], color=RED, scale_factor=1.06) for i in (0, 1)],
                      run_time=.6)
            for i, n in zip((2, 3, 4), ("104", "220", "253")):
                vo.wait_until(n)
                self.play(Indicate(rows_[i][1], color=RED, scale_factor=1.06), run_time=.4)
            vo.wait_until("Then rerun")
            self.play(FadeIn(rerun, shift=UP * .08), run_time=.4)
            vo.wait_until("episode five")
            self.play(FadeIn(e5), run_time=.4)
        self.finish()
