"""speciesOT E1 · Four verbs and a contract — Swiss scenes.

Narration and budgets come from the plan (script.json). Code on screen is Josh's real
speciesot_core.py (videos/speciesot-series/excerpts.py, real line numbers; a long line may be
elided with "…", never rewritten). The visual vocabulary is the series kit; the diagrams here
(file-shape minimap, an object filling up line by line, contract slots, the conductor's lists,
two answers to one call) are this episode's own.
"""
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent.parent / "speciesot-series"
sys.path.insert(0, str(SERIES))

from manim import *  # noqa: E402,F401,F403
from speciesot_kit import *  # noqa: E402,F401,F403
from excerpts import CORE, CONFIG, LINE_KINDS, LINE_LENGTHS, rows  # noqa: E402

CORE_PATH = "src/speciesot/speciesot_core.py"
JOBS = [  # (job, zh, first line, last line, classes)
    ("data", "数据", 20, 33, "TrainingData · TestData"),
    ("contract", "契约", 35, 57, "AbstractModel · AbstractEvaluation"),
    ("conductor", "指挥", 67, 146, "Experiment"),
    ("model", "模型", 151, 294, "IdentityModel · scGenModel"),
    ("metric", "指标", 300, 335, "R2Evaluation · MMDEvaluation"),
]


class Ep(EpisodeScene):
    episode = "E1"
    total = "06"


def minimap(x0, top, bottom, width=3.2):
    """The real shape of speciesot_core.py: one hairline per line, length ~ characters."""
    n = len(LINE_LENGTHS)
    dy = (top - bottom) / n
    xscale = .024
    g = VGroup()
    for i, (ln, kind) in enumerate(zip(LINE_LENGTHS, LINE_KINDS)):
        if ln == 0:
            continue
        y = top - (i + .5) * dy
        g.add(Line([x0, y, 0], [x0 + min(ln * xscale, width - .2), y, 0], stroke_width=1.6,
                   color=FAINT if kind == "c" else GRAY))
    frame = Rectangle(width=width, height=top - bottom + .16, stroke_color=INK, stroke_width=2)\
        .move_to([x0 + width / 2 - .1, (top + bottom) / 2, 0])
    g.dy, g.top = dy, top
    return frame, g


def line_y(m, n):
    return m.top - (n - .5) * m.dy


class S01(Ep):
    def construct(self):
        self.header()
        nb = code_panel([(None, l) for l in [
            "experiment = Experiment(experiment_spec_path)",
            "experiment.setup()", "experiment.train()",
            "experiment.predict()", "experiment.evaluate()"]],
            "e24_src_example.ipynb", -2.4, .3, width=7.6, size=22, numbers=False)
        keys = list(nb.rows)
        with self.say(0) as vo:
            self.cue(vo, .05, FadeIn(nb, shift=UP * .1), run_time=.6)
            mark = None
            for i, word in enumerate(["set up", "train,", "predict,", "evaluate"]):
                vo.wait_until(word)
                new = nb.mark(keys[i + 1])
                self.play(FadeIn(new) if mark is None else ReplacementTransform(mark, new),
                          run_time=.3)
                mark = new
            self.play(FadeOut(mark), run_time=.3)
        frame_map, m = minimap(-.1, 1.85, -2.3)
        with self.say(1) as vo:
            self.cue(vo, .05, nb.animate.scale(.74).move_to([-3.4, .9, 0]), run_time=.7)
            path = mono(CORE_PATH, 16, GRAY).move_to([1.5, 2.06, 0])
            vo.wait_until("speciesot_core.py")
            self.play(FadeIn(frame_map), FadeIn(path), run_time=.4)
            self.play(LaggedStart(*[Create(l) for l in m], lag_ratio=.004), run_time=1.8)
            count = at("345 lines", -3.4, -.5, 32, INK, bold=True)
            vo.wait_until("three hundred")
            self.play(FadeIn(count, shift=UP * .1), run_time=.5)
            q = at("which lines matter?", -3.4, -1.15, 26, RED)
            vo.wait_until("Which lines")
            self.play(FadeIn(q), run_time=.5)
        with self.say(2) as vo:
            self.cue(vo, .05, FadeOut(q), run_time=.3)
            words = ["Data,", "contract,", "conductor,", "model,", "metric."]
            prev = None
            for (job, zh, a, b, _), w in zip(JOBS, words):
                br = bracket(3.3, line_y(m, a), line_y(m, b), "", RED, 22)
                lab = left(f"{job} · {zh}", 3.55, (line_y(m, a) + line_y(m, b)) / 2, 22, RED,
                           bold=True)
                vo.wait_until(w)
                anims = [Create(br), FadeIn(lab, shift=LEFT * .08)]
                if prev is not None:
                    anims += [prev[0].animate.set_color(INK), prev[1].animate.set_color(INK)]
                self.play(*anims, run_time=.4)
                prev = (br, lab)
            self.play(prev[0].animate.set_color(INK), prev[1].animate.set_color(INK), run_time=.3)
            hint = at("every line does one of five jobs", -3.4, -1.15, 24, RED)
            self.play(FadeIn(hint), run_time=.5)
        self.finish()


class S02(Ep):
    def construct(self):
        self.header()
        blueprint = class_card("class scGenModel", ["__init__(config)", "setup()",
                                                    "train(training_data)",
                                                    "predict(test_data)"],
                               -3.6, .45, width=4.6)
        bp_lab = left("blueprint · 蓝图", -5.9, 1.78, 22, GRAY)
        ghost = DashedVMobject(Rectangle(width=3.9, height=2.2, color=GRAY), num_dashes=50)\
            .move_to([3.2, .45, 0])
        none = at("no object yet", 3.2, .45, 24, GRAY)
        with self.say(0) as vo:
            vo.wait_until("class.")
            self.play(FadeIn(blueprint, shift=UP * .1), FadeIn(bp_lab), run_time=.6)
            vo.wait_until("isn't the thing")
            self.play(Create(ghost), FadeIn(none), run_time=.6)
        call = code_panel([(115, CORE[115])], CORE_PATH, 0, -1.75, width=12.6, size=18)
        obj = obj_card("scGenModel", [], x=3.2, y=.75, width=3.9)
        with self.say(1) as vo:
            self.cue(vo, .05, FadeIn(call, shift=UP * .1), run_time=.5)
            vo.wait_until("Line 115")
            hl = highlight(self, call, 115)
            arr = arrow(blueprint.get_right() + RIGHT * .05, obj.get_left() + LEFT * .05)
            self.play(Create(arr), FadeOut(none), FadeOut(ghost), FadeIn(obj), run_time=.8)
            note = at("scGenModel(config)  →  a new object", 3.2, -.25, 22, RED)
            self.play(FadeIn(note), run_time=.4)
        init = code_panel(rows(CORE, 214, 225), CORE_PATH, -2.0, -.2, width=8.6, size=19)
        facts = ["config = {…}", "random_state = 0", "hidden_units = [256, 256]", "lr = 0.001",
                 "use_all_genes = True", "x_dimension = 1000", "z_dimension = 50",
                 "alpha = 0.5", "dropout_rate = 0.2", "model_path = '…/scGen'",
                 "network = None"]
        full = obj_card("scGenModel", facts, x=4.45, y=-.2, width=3.6, size=16, row_gap=.3)
        with self.say(2) as vo:
            self.cue(vo, .02, FadeOut(call), FadeOut(hl), FadeOut(blueprint), FadeOut(bp_lab),
                     FadeOut(arr), FadeOut(note), FadeIn(init),
                     ReplacementTransform(obj, VGroup(*full[:4])), run_time=.7)
            vo.wait_until("init method")
            m = highlight(self, init, 214, run_time=.3)
            per = max(.25, (vo.remaining() - .6) / len(facts))
            for i, n in enumerate(range(215, 226)):
                new = init.mark(n)
                self.play(ReplacementTransform(m, new), FadeIn(full.rows[i], shift=LEFT * .15),
                          run_time=min(.45, per))
                m = new
                if per > .45:
                    self.wait(per - .45)
            self.play(FadeOut(m), run_time=.3)
        twin_facts = list(facts)
        twin_facts[3] = "lr = 0.01"
        twin = obj_card("scGenModel", twin_facts, x=3.2, y=-.4, width=3.6, size=16, row_gap=.3)
        with self.say(3) as vo:
            m = highlight(self, init, 218, run_time=.3)
            ring = SurroundingRectangle(full.rows[3], color=RED, stroke_width=2.5, buff=.06)
            vo.wait_until("self.lr")
            self.play(Create(ring), full.rows[3].animate.set_color(RED), run_time=.5)
            vo.wait_until("Build two models")
            self.play(FadeOut(m), FadeOut(init), FadeOut(ring),
                      VGroup(*full[:4], full.rows).animate.move_to([-3.2, -.4, 0]), run_time=.6)
            twin.rows[3].set_color(RED)
            self.play(FadeIn(twin, shift=LEFT * .2), run_time=.6)
            s1 = at("self = this object", -3.2, 1.85, 22, RED)
            s2 = at("self = this object", 3.2, 1.85, 22, RED)
            self.play(FadeIn(s1), FadeIn(s2), run_time=.4)
        self.finish()


class S03(Ep):
    def construct(self):
        self.header()
        abstract = code_panel(rows(CORE, 35, 48), CORE_PATH, -1.6, -.25, width=9.3, size=19)
        with self.say(0) as vo:
            self.cue(vo, .05, FadeIn(abstract, shift=UP * .1), run_time=.6)
            vo.wait_until("marked abstract")
            m1 = highlight(self, abstract, 37, 42, 46, run_time=.4)
            vo.wait_until("raises an error")
            m2 = abstract.mark(40, 44, 48)
            self.play(ReplacementTransform(m1, m2), run_time=.4)
        contract = class_card("AbstractModel", ["setup()", "train(training_data)",
                                                "predict(test_data)"],
                              3.35, .9, width=5.2, abstract=True)
        slots = VGroup(*[DashedVMobject(Rectangle(width=1.35, height=.3, color=RED),
                                        num_dashes=14)
                         .move_to([contract.get_right()[0] - .85, t.get_y(), 0])
                         for t in contract.methods])
        clab = left("contract · 契约", .85, 2.0, 22, RED, bold=True)
        blank = left("blank · 空白", contract.get_right()[0] - 1.45, -.35, 18, RED)
        with self.say(1) as vo:
            self.cue(vo, .03, FadeOut(m2), abstract.animate.scale(.56).move_to([-3.6, -.25, 0]),
                     run_time=.6)
            self.play(FadeIn(contract, shift=LEFT * .1), FadeIn(clab), run_time=.5)
            vo.wait_until("set up, train")
            self.play(LaggedStart(*[Indicate(t, color=RED, scale_factor=1.05)
                                    for t in contract.methods], lag_ratio=.3), run_time=1.0)
            vo.wait_until("doesn't fill")
            self.play(Create(slots), FadeIn(blank), run_time=.6)
        with self.say(2) as vo:
            card = ponder("直接造一个 AbstractModel，会怎样？",
                          "What happens if you call AbstractModel() directly?", y=-.9)
            self.cue(vo, .1, self.dim_rest(), run_time=.5)
            self.play(FadeIn(card, shift=UP * .1), run_time=.5)
        err = error_card("TypeError", ["Can't instantiate abstract class AbstractModel",
                                       "without an implementation for abstract methods",
                                       "'predict', 'setup', 'train'"],
                         ">>> AbstractModel()      (Python 3.12)", 0, -1.05, width=9.2, size=20)
        with self.say(3) as vo:
            self.cue(vo, .02, FadeOut(card), *[mm.animate.set_opacity(1) for mm in
                                               (abstract, contract, slots, clab, blank)],
                     run_time=.4)
            vo.wait_until("We ran it")
            self.play(FadeIn(err, shift=UP * .1), run_time=.6)
        ident = class_card("IdentityModel", ["setup():  pass", "train():  pass",
                                             "predict():  return mouse"],
                           -3.3, -1.45, width=4.9, parent="AbstractModel")
        scg = class_card("scGenModel", ["setup():  build network", "train():  learn δ",
                                        "predict():  shift mouse"],
                         3.3, -1.45, width=4.9, parent="AbstractModel")
        with self.say(4) as vo:
            self.cue(vo, .02, FadeOut(err), FadeOut(abstract), FadeOut(blank),
                     VGroup(contract, slots).animate.move_to([0, 1.1, 0]),
                     clab.animate.move_to([-3.95, 1.5, 0]), run_time=.7)
            self.play(FadeIn(ident, shift=UP * .1), FadeIn(scg, shift=UP * .1), run_time=.6)
            bottom = contract.get_bottom()[1]
            up1 = Arrow(ident.get_top(), [-1.2, bottom, 0], buff=.08, color=INK, stroke_width=2.5,
                        max_tip_length_to_length_ratio=.15)
            up2 = Arrow(scg.get_top(), [1.2, bottom, 0], buff=.08, color=INK, stroke_width=2.5,
                        max_tip_length_to_length_ratio=.15)
            vo.wait_until("name in brackets")
            self.play(ident[2].animate.set_color(RED), scg[2].animate.set_color(RED),
                      FadeOut(slots), run_time=.5)
            vo.wait_until("inheritance")
            inh = at("inheritance · 继承", 0, -.3, 24, RED, bold=True)
            self.play(GrowArrow(up1), GrowArrow(up2), FadeIn(inh), run_time=.7)
        note = code_panel(rows(CORE, 19, 20), CORE_PATH, 0, -.35, width=8.0, size=20)
        with self.say(5) as vo:
            self.cue(vo, .03, FadeOut(inh), FadeOut(up1), FadeOut(up2),
                     VGroup(ident, scg).animate.set_opacity(.2), run_time=.4)
            self.play(FadeIn(note, shift=UP * .1), run_time=.5)
            vo.wait_until("nothing to sign")
            nothing = at("abc.ABC + no abstract methods = nothing to sign", 0, -1.4, 22, GRAY)
            self.play(FadeIn(nothing), run_time=.4)
            vo.wait_until("line 19")
            highlight(self, note, 19, run_time=.4)
        self.finish()


class S04(Ep):
    def construct(self):
        self.header()
        cond = chip("Experiment", 0, 1.45, RED, 26)
        clab = at("conductor · 指挥", 0, .85, 20, GRAY)
        parts = VGroup(*[chip(t, x, -.3, GRAY, 20, font=LATIN) for t, x in
                         (("reads the config", -4.2), ("builds the pieces", 0),
                          ("cues each one", 4.2))])
        with self.say(0) as vo:
            self.cue(vo, .05, FadeIn(cond, shift=DOWN * .1), FadeIn(clab), run_time=.6)
            for p, w in zip(parts, ["reads the config", "builds the pieces", "tells each"]):
                vo.wait_until(w)
                self.play(FadeIn(p, shift=UP * .1), run_time=.35)
        yml = code_panel(rows(CONFIG, 30, 45), "Tests/config.yaml", -3.6, -.35, width=5.4,
                         size=18)
        models = VGroup(chip("IdentityModel", 1.0, .35, INK, 20),
                        chip("scGenModel", 3.75, .35, INK, 20))
        evals = VGroup(chip("R2Evaluation", 1.0, -1.05, INK, 20),
                       chip("MMDEvaluation", 3.75, -1.05, INK, 20))
        mlab = left("self.models", -.45, .95, 20, GRAY)
        elab = left("self.evaluations", -.45, -.45, 20, GRAY)
        with self.say(1) as vo:
            self.cue(vo, .02, FadeOut(parts), FadeOut(clab),
                     cond.animate.scale(.8).move_to([2.4, 1.6, 0]), FadeIn(yml), run_time=.6)
            vo.wait_until("models, from")
            m = highlight(self, yml, 31, 32, run_time=.35)
            self.play(FadeIn(mlab), TransformFromCopy(yml.row(31), models[0]),
                      TransformFromCopy(yml.row(32), models[1]), run_time=.8)
            vo.wait_until("evaluations, from")
            m2 = yml.mark(44, 45)
            self.play(ReplacementTransform(m, m2), run_time=.3)
            self.play(FadeIn(elab), TransformFromCopy(yml.row(44), evals[0]),
                      TransformFromCopy(yml.row(45), evals[1]), run_time=.8)
        preds = VGroup(*[cloud(14, x, -2.0, .13, GRAY, seed=i, radius=.03)
                         for i, x in enumerate((1.0, 3.75))])
        plab = left("self.predictions", -.45, -1.6, 20, GRAY)
        with self.say(2) as vo:
            tok = Dot([models[0].get_left()[0] - .3, .35, 0], radius=.09, color=RED)
            self.cue(vo, .05, FadeOut(m2), FadeIn(tok), run_time=.3)
            for chp in models:
                self.play(tok.animate.move_to(chp.get_bottom() + DOWN * .18), run_time=.4)
                self.play(Indicate(chp, color=RED, scale_factor=1.06), run_time=.4)
            vo.wait_until("Predict collects")
            self.play(FadeOut(tok), FadeIn(plab), *[FadeIn(p, shift=DOWN * .2) for p in preds],
                      run_time=.7)
        gx, gy = [2.4, 5.0], [.35, -.55]
        grid = VGroup()
        with self.say(3) as vo:
            self.cue(vo, .02, FadeOut(yml), FadeOut(mlab), FadeOut(elab), FadeOut(plab),
                     FadeOut(preds),
                     models[0].animate.move_to([-.5, gy[0], 0]),
                     models[1].animate.move_to([-.5, gy[1], 0]),
                     evals[0].animate.move_to([gx[0], 1.15, 0]),
                     evals[1].animate.move_to([gx[1], 1.15, 0]), run_time=.8)
            for i in range(2):
                for j in range(2):
                    box = Rectangle(width=1.8, height=.72, stroke_color=INK, stroke_width=2)\
                        .move_to([gx[j], gy[i], 0])
                    grid.add(VGroup(box, mono("x.xxx", 22, GRAY).move_to(box.get_center())))
            vo.wait_until("times two")
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=.25), run_time=1.0)
            four = at("2 × 2 = 4 numbers", 2.5, -1.35, 26, RED, bold=True)
            self.play(FadeIn(four), run_time=.4)
        table = VGroup(models, evals, grid, cond)
        ev = code_panel(rows(CORE, 141, 145), CORE_PATH, -.6, -1.3, width=10.6, size=19)
        with self.say(4) as vo:
            self.cue(vo, .03, FadeOut(four), table.animate.scale(.72).move_to([2.6, 1.25, 0]),
                     run_time=.6)
            self.play(FadeIn(ev, shift=UP * .1), run_time=.4)
            vo.wait_until("Line 145")
            highlight(self, ev, 145, run_time=.35)
            self.play(*[c[1].animate.set_opacity(0).shift(DOWN * .25) for c in grid.submobjects],
                      run_time=.7)
            dropped = left("returns None · 结果没有保存", -6.1, 1.3, 22, RED)
            st = source_tag("MEASURED").next_to(dropped, DOWN, buff=.15, aligned_edge=LEFT)
            self.play(FadeIn(dropped), FadeIn(st), run_time=.4)
        self.finish()


class S05(Ep):
    def construct(self):
        self.header()
        pred = code_panel(rows(CORE, 135, 138), CORE_PATH, 0, .6, width=12.4, size=20)
        with self.say(0) as vo:
            self.cue(vo, .03, FadeIn(pred), run_time=.5)
            vo.wait_until("Line 137")
            m = highlight(self, pred, 137, run_time=.35)
            q = at("which model? — it never asks · 它从不过问是哪个模型", 0, -1.0, 26, RED)
            self.play(FadeIn(q), run_time=.4)
        call = mono("137  p = model.predict(self.test_data)", 18, INK).move_to([0, 1.75, 0])
        lane_y = [.35, -1.3]
        mouse_x, box_x, out_x = -4.6, -1.3, 2.0
        mouse = [cloud(26, mouse_x, y, .22, GRAY, seed=3, radius=.04) for y in lane_y]
        mlabel = at("mouse test cells", mouse_x, 1.0, 17, GRAY)
        human = DashedVMobject(Circle(radius=.6, color=RED), num_dashes=24).move_to([4.8, -.45, 0])
        hlabel = at("human (truth)", 4.8, .35, 17, RED)
        with self.say(1) as vo:
            self.cue(vo, .02, FadeOut(q), FadeOut(m), ReplacementTransform(pred, call),
                     run_time=.5)
            ib = chip("IdentityModel", box_x, lane_y[0], INK, 20)
            a1 = arrow([mouse_x + .55, lane_y[0], 0], ib.get_left(), INK)
            self.play(FadeIn(mouse[0]), FadeIn(mlabel), Create(a1), FadeIn(ib), run_time=.6)
            vo.wait_until("unchanged")
            out1 = mouse[0].copy()
            a2 = arrow(ib.get_right(), [out_x - .55, lane_y[0], 0], INK)
            self.play(Create(a2), out1.animate.move_to([out_x, lane_y[0], 0]), run_time=.9)
            same = at("the same cells back", out_x, lane_y[0] + .6, 17, GRAY)
            self.play(FadeIn(same), FadeIn(human), FadeIn(hlabel), run_time=.4)
            vo.wait_until("baseline")
            base = at("do-nothing baseline · 基线", out_x, lane_y[0] - .62, 18, INK, bold=True)
            self.play(FadeIn(base), run_time=.4)
        with self.say(2) as vo:
            sb = chip("scGenModel", box_x, lane_y[1], RED, 20)
            b1 = arrow([mouse_x + .55, lane_y[1], 0], sb.get_left(), INK)
            self.cue(vo, .03, FadeIn(mouse[1]), Create(b1), FadeIn(sb), run_time=.6)
            out2 = mouse[1].copy()
            b2 = arrow(sb.get_right(), [out_x - .55, lane_y[1], 0], RED)
            vo.wait_until("toward human")
            self.play(Create(b2), out2.animate.move_to([out_x + 1.35, lane_y[1] + .45, 0])
                      .set_color(RED), run_time=1.0)
            planned = at("planned — episode 4", out_x + .9, lane_y[1] - .65, 17, GRAY)
            self.play(FadeIn(planned), run_time=.3)
            vo.wait_until("polymorphism")
            poly = at("one call, different answers · 多态 polymorphism", 0, -2.2, 24, RED,
                      bold=True)
            self.play(FadeIn(poly), run_time=.5)
        with self.say(3) as vo:
            card = ponder("加入 CellOT 时，Experiment 里哪些行应该改？",
                          "Adding CellOT: which lines of Experiment should change?", y=-.6)
            self.cue(vo, .1, self.dim_rest(), run_time=.5)
            self.play(FadeIn(card, shift=UP * .1), run_time=.5)
        chain = code_panel([(107, CORE[107]), (108, CORE[108]), (None, ""),
                            (112, CORE[112]), (None, "        …"),
                            (115, "            self.models.append(scGenModel(self.experiment_spec[…]))")],
                           CORE_PATH, -1.5, -.6, width=9.4, size=19)
        ideal = at("ideally: none · 理想情况：一行都不用改", 0, 1.2, 30, INK, bold=True)
        with self.say(4) as vo:
            self.cue(vo, .02, *[FadeOut(mm) for mm in self.content()], run_time=.4)
            vo.wait_until("Ideally")
            self.play(FadeIn(ideal), run_time=.5)
            vo.wait_until("Today")
            self.play(ideal.animate.scale(.75).move_to([0, 1.78, 0]), FadeIn(chain), run_time=.6)
            vo.wait_until("chain of if")
            highlight(self, chain, 107, 112, run_time=.4)
            ghost = chip("CellOTModel ?", 4.75, -.6, GRAY, 20)
            e5 = at("→ episode 5", 4.75, -1.25, 18, RED)
            self.play(FadeIn(ghost), FadeIn(e5), run_time=.5)
        self.finish()


class S06(Ep):
    def construct(self):
        self.header()
        cards = VGroup(
            card("class → object", "init writes facts · self = this one", -4.2, 1.0, 3.95, 1.6,
                 accent=True),
            card("abstract = contract", "names methods · fill every blank", 0, 1.0, 3.95, 1.6),
            card("Experiment", "conducts models + metrics", 4.2, 1.0, 3.95, 1.6),
        )
        for i in range(3):
            with self.say(i) as vo:
                self.cue(vo, .05, FadeIn(cards[i], shift=UP * .1), run_time=.5)
        table = VGroup()
        for i, (job, zh, a, b, classes) in enumerate(JOBS):
            y = -.45 - i * .42
            table.add(VGroup(left(f"{job} · {zh}", -6.1, y, 22, INK, bold=True),
                             mono_left(classes, -3.3, y, 19, INK),
                             mono_left(f"lines {a}–{b}", 3.3, y, 19, GRAY)))
        path = mono_left(CORE_PATH, -6.1, .02, 17, GRAY)
        with self.say(3) as vo:
            self.cue(vo, .02, cards.animate.scale(.85).shift(UP * .3), run_time=.4)
            self.play(FadeIn(path), LaggedStart(*[FadeIn(r, shift=RIGHT * .1) for r in table],
                                                lag_ratio=.25), run_time=1.6)
            vo.wait_until("companion notes")
            self.play(*[r[0].animate.set_color(RED) for r in table], run_time=.5)
        self.finish()
