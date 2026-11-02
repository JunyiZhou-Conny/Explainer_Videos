"""S02 · A pipeline is a graph (V1, the tracer).
Lecture: 22, 24–30, 32–34, 40.

Beats (script.md "## S02", one voiceover block each):
 0  LECTURE 22, 34. Three WHITE task nodes (prep, train, deploy) and two PINK data edges draw in;
    at "The structure" the chip "DAG = directed acyclic graph" writes in above them.
 1  "directed" lights PINK and the arrowheads flash (producer → consumer); "acyclic" lights: a
    dotted PINK edge tries to loop from deploy back to prep, turns RED and is crossed out ("a step
    never waits on itself"). The nodes rename themselves "task", "task", "task" ("task = node");
    the edges pulse ("data dependency = edge").
 2  LECTURE 24–25. The small graph slides left (shapes shrink, text keeps its size). Right: a BLUE
    box "Vertex AI Pipelines · runs the graph" (a GREY arrow from the graph), a PURPLE chip
    "Kubeflow Pipelines · kfp" (the DSL) with an arrow into it, a GREY chip "your own Kubernetes
    cluster" struck out, and the GREY excerpt chip ml-workflow/README.md · line 212 (excerpt):
    "Agent Platform > Pipelines".
 3  LECTURE 28–29. Everything fades. CODE(ml-workflow/src/workflow/cli.py: 281–293, folded at the
    blank and comment lines): the three @dsl.component decorators lit PURPLE, the three names flash;
    the panel Transforms into lines 295–301 (wrapped), @dsl.pipeline lit PURPLE.
 4  V1. The panel moves left; the tracer canvas is on the right. A YELLOW cursor bar steps to
    line 298; `a: float = 3.0` on line 297 is ringed GREY ("pipeline input · default 3.0"); a WHITE
    node `square` drops with an empty GREEN socket labelled `.output`; GREY chip "no number yet".
 5  The cursor steps 299, 300, 301: square-2, add, square-root drop (the Y); the GREY dotted
    connections draw, the first labelled "?". At "Square is called twice" the PURPLE stamp
    "component: square" sits above both square nodes and square-2's name is ringed. GREY chip
    "the function ran once → a graph".
 6  LECTURE 29–30, 32–33, 40. The panel Transforms into lines 303–304 (304 lit PURPLE) and the
    PURPLE compiler roller presses the graph into the GREEN sheet sample-pipeline1.yaml; the panel
    Transforms into lines 311–318 (`aip.PipelineJob(` and `job.run(` lit). The panel fades; the GREY
    laptop and the BLUE Vertex zone come in, the sheet rides the PURPLE `aiplatform` arrow across;
    slide 40's chain writes along the bottom: recipe (DSL) → printed YAML → operator (SDK) →
    engine (Kubeflow) → manager (Vertex AI Pipelines).
 7  The Vertex zone grows to the frame, the sheet re-forms into the graph, a TEAL machine slides
    beside each node ("a container per task"); the two squares run YELLOW, then ✓ with 9.0 and
    16.0 in their sockets; then add 25.0, then square-root 5.0.
 8  The canvas fades. TAKEAWAY: "calling train() inside the pipeline function → creates a task
    (a node), trains nothing · nothing runs until the compiled job runs on Vertex". Empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    ArcBetweenPoints,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    ReplacementTransform,
    Transform,
    VGroup,
    Write,
)

from common import guard as _guard
from common import *  # noqa: F401,F403
from common import _arrow
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S02"]

# ------------------------------------------------------------------ the real sources
CLI = "ml-workflow/src/workflow/cli.py"
assert source_line(CLI, 281).strip() == "@dsl.component", source_line(CLI, 281)
assert source_line(CLI, 282).strip().startswith("def square(x: float)"), source_line(CLI, 282)
assert source_line(CLI, 287).strip().startswith("def add(x: float, y: float)"), source_line(CLI, 287)
assert source_line(CLI, 292).strip().startswith("def square_root(x: float)"), source_line(CLI, 292)
assert source_line(CLI, 296).strip() == "@dsl.pipeline", source_line(CLI, 296)
assert "a: float = 3.0" in source_line(CLI, 297), source_line(CLI, 297)
assert source_line(CLI, 298).strip() == "a_sq_task = square(x=a)", source_line(CLI, 298)
assert source_line(CLI, 299).strip() == "b_sq_task = square(x=b)", source_line(CLI, 299)
assert source_line(CLI, 300).strip().startswith("sum_task = add("), source_line(CLI, 300)
assert source_line(CLI, 301).strip().startswith("return square_root("), source_line(CLI, 301)
assert "compiler.Compiler().compile(sample_pipeline" in source_line(CLI, 304), source_line(CLI, 304)
assert source_line(CLI, 311).strip() == "job = aip.PipelineJob(", source_line(CLI, 311)
assert source_line(CLI, 318).strip().startswith("job.run("), source_line(CLI, 318)
README_212 = source_line("ml-workflow/README.md", 212)
AGENT = "Agent Platform > Pipelines"
assert AGENT in README_212, README_212
assert list(TOY) == ["square", "square-2", "add", "square-root"], TOY

# ------------------------------------------------------------------ layout
SAFE_L, SAFE_R = -6.45, 6.45
TOP_Y = 2.95                     # under the lecture tag (its bottom is at 3.13)


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def inside(m, l=SAFE_L, r=SAFE_R, b=-3.5, t=3.5):
    _guard(m.get_left()[0] >= l and m.get_right()[0] <= r and m.get_bottom()[1] >= b and m.get_top()[1] <= t,
           f"out of the frame: {m.get_left()[0]:.2f} {m.get_right()[0]:.2f} {m.get_bottom()[1]:.2f} "
           f"{m.get_top()[1]:.2f}")


def apart(a, b, gap=0.1, msg=""):
    """a and b do not overlap (their boxes are at least `gap` apart on one axis)."""
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    _guard(sep, f"overlap: {msg}")


def flash(mob, color: str = TURN, k: float = 1.15, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def wrapped_header(p, lines_note: str):
    """Put a panel's "· line N wrapped" header parts on a second header row ("lines_note"), so
    the header is no wider than the code (the panel must share the frame with the tracer)."""
    h = p.header
    extras = list(h.submobjects[2:])
    for m in extras:
        h.remove(m)
    row1 = VGroup(*h.submobjects)
    row2 = label(lines_note, CAPTION, S.GREY)
    row2.next_to(row1, DOWN, buff=0.06).align_to(row1, LEFT)
    h.add(row2)
    h.next_to(p.code, UP, buff=0.1).align_to(p.code, LEFT).shift(RIGHT * 0.12)
    return p


def word_chip(words, size=30):
    """'DAG = directed acyclic graph' as separate words in one GREY-outlined box. .words .frame"""
    ws = VGroup(*[label(w, size, INK) for w in words]).arrange(RIGHT, buff=0.18)
    for w in ws:
        w.align_to(ws[0], DOWN)
    fr = box(ws.width + 0.6, ws.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.9, radius=0.16)
    ws.move_to(fr)
    g = VGroup(fr, ws)
    g.frame, g.words = fr, ws
    return g


class TasksAndEdges(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0 · three tasks, two edges, "DAG"
        lr = None
        chain = Dag({"prep": (-4.0, -0.35), "train": (0.0, -0.35), "deploy": (4.0, -0.35)},
                    [("prep", "train"), ("train", "deploy")], node_kw={"outputs": ()},
                    show=("node:prep", "node:train", "node:deploy"))
        dag_chip = word_chip(["DAG", "=", "directed", "acyclic", "graph"])
        place(dag_chip, cx=0, top=2.75)
        inside(dag_chip)
        w1, w2 = chain.wire[("prep", "train")], chain.wire[("train", "deploy")]
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "22, 34")
            self.play(LaggedStart(*[FadeIn(chain.node[n], shift=DOWN * 0.3) for n in ("prep", "train", "deploy")],
                                  lag_ratio=0.35), run_time=1.2)
            self.play(*chain.parts_in("wire:prep->train", anim=lambda m: Create(m)), run_time=0.8)
            self.play(*chain.parts_in("wire:train->deploy", anim=lambda m: Create(m)), run_time=0.8)
            vo.wait_until("which step needs which")
            self.play(w1.light(), w2.light(), run_time=0.9)
            vo.wait_until("The structure")
            self.play(FadeIn(dag_chip.frame), Write(dag_chip.words), run_time=1.2)
            vo.wait_until("or DAG")
            self.play(flash(dag_chip.words[0], INK, 1.15), run_time=0.6)

        # ========================================================== 1 · directed, acyclic, task = node
        p_top = chain.node["prep"].frame.get_top()
        d_top = chain.node["deploy"].frame.get_top()
        arc = ArcBetweenPoints(d_top + LEFT * 0.2, p_top + RIGHT * 0.2 + UP * 0.04, angle=PI / 3)
        loop = DashedVMobject(arc.copy().set_stroke(EDGE, 3), num_dashes=34, dashed_ratio=0.5).set_stroke(EDGE, 3)
        end = arc.get_end()
        dv = end - arc.point_from_proportion(0.96)
        dv = dv / np.linalg.norm(dv)
        pv = np.array([-dv[1], dv[0], 0.0])
        loop_tip = Polygon(end, end - dv * 0.2 + pv * 0.11, end - dv * 0.2 - pv * 0.11, stroke_width=0) \
            .set_fill(EDGE, 1)
        peak = arc.point_from_proportion(0.5)
        cross = x_mark(0.42).move_to(peak)
        no_loop = label("a step never waits on itself", 22, ERR).move_to(peak + UP * 0.48)
        apart(no_loop, dag_chip, 0.08, "loop note vs DAG chip")
        new_titles = {}
        for n in ("prep", "train", "deploy"):
            node = chain.node[n]
            new_titles[n] = mono("task", 22, INK).move_to(node.title)
        node_lbl = label("task = node", 24, INK)
        place(node_lbl, cx=chain.node["prep"].get_center()[0], top=chain.node["prep"].get_bottom()[1] - 0.55)
        node_ptr = Line(node_lbl.get_top() + UP * 0.06, chain.node["prep"].frame.get_bottom() + DOWN * 0.06,
                        color=S.GREY, stroke_width=2)
        edge_lbl = label("data dependency = edge", 24, EDGE)
        mid = w2.path.point_from_proportion(0.5)
        place(edge_lbl, cx=mid[0], top=chain.node["deploy"].get_bottom()[1] - 0.55)
        edge_ptr = Line(edge_lbl.get_top() + UP * 0.06, mid + DOWN * 0.08, color=EDGE, stroke_width=2)
        inside(edge_lbl)
        apart(node_lbl, edge_lbl, 0.2, "node label vs edge label")
        with self.voiceover(SAY[1]) as vo:
            self.play(dag_chip.words[2].animate.set_color(EDGE), run_time=0.5)
            self.play(flash(w1.tip, EDGE, 1.8), flash(w2.tip, EDGE, 1.8), w1.light(EDGE), w2.light(EDGE),
                      run_time=0.9)
            vo.wait_until("from producer to consumer")
            self.play(w1.light(), w2.light(), run_time=0.9)
            vo.wait_until("Acyclic")
            self.play(dag_chip.words[2].animate.set_color(INK), dag_chip.words[3].animate.set_color(EDGE),
                      run_time=0.4)
            self.play(Create(loop), run_time=1.0)
            self.play(FadeIn(loop_tip), run_time=0.2)
            vo.wait_until("no step ever waits")
            self.play(loop.animate.set_stroke(ERR), loop_tip.animate.set_fill(ERR), FadeIn(cross, scale=1.4),
                      run_time=0.5)
            self.play(FadeIn(no_loop, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Tasks are the nodes")
            self.play(FadeOut(VGroup(loop, loop_tip, cross, no_loop)), dag_chip.words[3].animate.set_color(INK),
                      run_time=0.4)
            swaps = []
            for n in ("prep", "train", "deploy"):
                node = chain.node[n]
                swaps += swap_text(node, node.title, new_titles[n])
                node.title = new_titles[n]
            self.play(*swaps, run_time=0.7)
            self.play(FadeIn(node_lbl, shift=UP * 0.1), Create(node_ptr),
                      *[flash(chain.node[n].frame, INK, 1.08) for n in ("prep", "train", "deploy")], run_time=0.7)
            vo.wait_until("data dependencies are the edges")
            self.play(FadeIn(edge_lbl, shift=UP * 0.1), Create(edge_ptr), w1.light(EDGE), w2.light(EDGE),
                      run_time=0.8)
            self.play(w1.light(TURN), w2.light(TURN), run_time=0.8)

        # ========================================================== 2 · kfp describes, Vertex runs
        vx_box = box(4.6, 1.15, CLOUD, fill_opacity=0.1, radius=0.18)
        vx_t = label("Vertex AI Pipelines", 26, INK)
        vx_s = label("runs the graph", CAPTION, CLOUD)
        VGroup(vx_t, vx_s).arrange(DOWN, buff=0.06).move_to(vx_box)
        vertex = VGroup(vx_box, vx_t, vx_s)
        place(vertex, cx=3.45, cy=0.15)
        kfp = chip("Kubeflow Pipelines · kfp", TOOL, size=24)
        place(kfp, cx=3.45, cy=2.0)
        kfp_note = label("the DSL: describes the graph", CAPTION, TOOL)
        place(kfp_note, cx=3.45, top=kfp.get_bottom()[1] - 0.08)
        k_arrow = _arrow(kfp_note.get_bottom() + DOWN * 0.04, vx_box.get_top() + UP * 0.02, TOOL, 3)
        k8s = chip("your own Kubernetes cluster", S.GREY, size=22)
        place(k8s, cx=3.45, top=vx_box.get_bottom()[1] - 0.45)
        k8s_x = strike(k8s, ERR)
        ex = excerpt_chip(AGENT, "ml-workflow/README.md · line 212 (excerpt)", line=README_212)
        place(ex, right=SAFE_R, bottom=-3.35)
        small_target = (-3.1, 0.15)       # rescale 0.68: frames still hold their (unscaled) titles
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(dag_chip, node_lbl, node_ptr, edge_lbl, edge_ptr)), run_time=0.5)
            lr = lref_swap(self, lr, "24–25")
            self.play(chain.animate.rescale(0.68).move_to([*small_target, 0]), run_time=0.9)
            self.play(*[chain.node[n].title.animate.move_to(chain.node[n].frame)
                        for n in ("prep", "train", "deploy")], run_time=0.3)
            inside(chain)
            for n in ("prep", "train", "deploy"):
                _guard(chain.node[n].frame.width >= chain.node[n].title.width + 0.15, f"title {n} overflows its frame")
            g_arrow = _arrow(chain.get_right() + RIGHT * 0.1, vx_box.get_left() + LEFT * 0.05, S.GREY, 3)
            apart(chain, vertex, 0.3, "graph vs Vertex box")
            self.play(FadeIn(vertex, shift=LEFT * 0.2), Create(g_arrow), run_time=0.8)
            vo.wait_until("You describe the graph")
            self.play(FadeIn(kfp, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(kfp_note), Create(k_arrow), run_time=0.6)
            vo.wait_until("and there is no Kubernetes")
            self.play(FadeIn(k8s, shift=UP * 0.1), run_time=0.5)
            self.play(Create(k8s_x), k8s.animate.set_opacity(0.5), run_time=0.5)
            vo.wait_until("Today's console")
            inside(ex)
            apart(ex, k8s, 0.15, "excerpt vs k8s chip")
            self.play(FadeIn(ex, shift=UP * 0.15), run_time=0.6)
            self.play(flash(ex.text, INK, 1.08), run_time=0.6)

        # ========================================================== 3 · the toy pipeline's code
        pa = src_panel(CLI, [(281, 283), (286, 288), (291, 293)])
        place(pa, cx=0, cy=-0.1)
        inside(pa)
        deco_bars = VGroup(*[pa.bar(n, TOOL, 0.3) for n in (281, 286, 291)])
        pb = src_panel(CLI, 295, 301, wrap={297: ["b: float"], 300: ["add(", "y=b_sq"], 301: ["x=sum_task"]})
        wrapped_header(pb, "· lines 297, 300 and 301 wrapped")
        place(pb, cx=0, cy=-0.1)
        inside(pb)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(chain, g_arrow, vertex, kfp, kfp_note, k_arrow, k8s, k8s_x, ex)), run_time=0.6)
            lr = lref_swap(self, lr, "28–29")
            self.play(FadeIn(pa, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("Three Python functions")
            self.play(LaggedStart(*[FadeIn(b) for b in deco_bars], lag_ratio=0.4),
                      *[pa.span(n, "@dsl.component").animate.set_color(TOOL) for n in (281, 286, 291)],
                      run_time=1.0)
            vo.wait_until("square, add and square root")
            for n, name in ((282, "square"), (287, "add"), (292, "square_root")):
                self.play(flash(pa.span(n, name), TURN, 1.2), run_time=0.45)
            vo.wait_until("A fourth")
            self.play(FadeOut(deco_bars), run_time=0.3)
            self.play(ReplacementTransform(pa, pb), run_time=0.9)
            pipe_bar = pb.bar(296, TOOL, 0.3)
            self.play(FadeIn(pipe_bar), pb.span(296, "@dsl.pipeline").animate.set_color(TOOL), run_time=0.5)
            vo.wait_until("wires them together")
            self.play(flash(pb.span(296, "@dsl.pipeline"), TOOL, 1.15), run_time=0.6)

        # ========================================================== 4 · V1: a call drops a node
        tracer = Tracer()
        place(tracer, right=6.1, top=TOP_Y - 0.45)   # room for the compiler roller's sweep and label
        inside(tracer)
        pb_target = pb.copy()
        place(pb_target, left=SAFE_L, top=TOP_Y)
        apart(pb_target, tracer, 0.1, "code panel vs tracer")
        inp = pb.span(297, "a: float = 3.0")
        n_input = label("pipeline input · default 3.0", CAPTION, S.GREY)
        nonum = chip("no number yet", S.GREY, size=CAPTION)
        notes = VGroup()
        with self.voiceover(SAY[4]) as vo:
            self.play(VGroup(pb, pipe_bar).animate.shift(pb_target.get_center() - pb.get_center()), run_time=0.8)
            self.add(tracer)
            cur = pb.bar(296, TURN, 0.25)
            self.play(FadeIn(cur), run_time=0.4)
            vo.wait_until("the component calls compute nothing")
            new = pb.bar(298, TURN, 0.25)
            self.play(Transform(cur, new), run_time=0.5)
            vo.wait_until("Calling square on a")
            ring_in = ring(inp, S.GREY, buff=0.05, stroke=3)
            place(n_input, left=pb.get_left()[0] + 0.1, top=pb.get_bottom()[1] - 0.2)
            inside(n_input)
            self.play(Create(ring_in), FadeIn(n_input, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("creates a task")
            self.play(*tracer.drop("square"), run_time=0.6)
            vo.wait_until("with an empty output socket")
            self.play(*tracer.node["square"].show_labels(), flash(tracer.node["square"].sockets[0], OWN, 1.3),
                      run_time=0.7)
            vo.wait_until("No number yet")
            place(nonum, left=n_input.get_left()[0], top=n_input.get_bottom()[1] - 0.18)
            inside(nonum)
            apart(nonum, tracer, 0.1, "no-number chip vs tracer")
            self.play(FadeIn(nonum, shift=UP * 0.1), run_time=0.5)
        notes.add(n_input, nonum)

        # ========================================================== 5 · four calls, four nodes, a graph
        once = chip("the function ran once → a graph", S.GREY, size=CAPTION)
        place(once, left=n_input.get_left()[0], top=n_input.get_top()[1])
        inside(once)
        apart(once, tracer, 0.1, "once chip vs tracer")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(ring_in), run_time=0.3)
            for line_no, name in ((299, "square-2"), (300, "add"), (301, "square-root")):
                self.play(Transform(cur, pb.bar(line_no, TURN, 0.25)), run_time=0.4)
                self.play(*tracer.drop(name), run_time=0.5)
            self.play(*tracer.connect(), run_time=0.8)
            vo.wait_until("Square is called twice")
            self.play(*tracer.stamp(), flash(tracer.node["square"].title, TOOL, 1.15),
                      flash(tracer.node["square-2"].title, TOOL, 1.15), run_time=0.8)
            vo.wait_until("the second is named")
            ring2 = ring(tracer.node["square-2"].title, TOOL, buff=0.06, stroke=3)
            self.play(Create(ring2), run_time=0.5)
            vo.wait_until("The function ran once")
            self.play(FadeOut(VGroup(notes, ring2)), FadeIn(once, shift=UP * 0.1), FadeOut(cur), run_time=0.6)
            self.play(flash(tracer.node["square-root"].frame, INK, 1.06), flash(tracer.node["square"].frame, INK, 1.06),
                      flash(tracer.node["square-2"].frame, INK, 1.06), flash(tracer.node["add"].frame, INK, 1.06),
                      run_time=0.7)

        # ========================================================== 6 · compile, submit, the chain
        pc = src_panel(CLI, 303, 304, wrap={304: ["sample_pipeline", "package_path", '"sample']})
        wrapped_header(pc, "· line 304 wrapped")
        place(pc, left=SAFE_L, top=TOP_Y)
        inside(pc)
        SLIDE = 0.5                       # the tracer moves left before the press (the roller's label)
        DROP = 0.45                       # ... and down, so the roller's label clears the panel header
        _guard(pc.code.get_right()[0] + 0.1 <= tracer.get_left()[0] - SLIDE
               and pc.header.get_right()[0] + 0.1 <= tracer.parts["stamp"].get_left()[0] - SLIDE,
               "compile panel vs tracer")      # the header reaches over the tracer's empty top-left corner
        _guard(tracer.get_right()[0] - SLIDE + 0.3 + compiler_roller(1).title.width / 2 <= 6.6,
               "the compiler roller's label leaves the frame")
        _roller = compiler_roller(tracer.height + 0.3)
        _label_top = tracer.get_bottom()[1] - DROP - 0.15 + _roller.height
        _guard(_label_top + 0.05 <= pc.header.submobjects[0].get_bottom()[1], "roller label vs compile panel header")
        _guard(tracer.get_bottom()[1] - DROP - 0.15 >= -3.55, "roller bottom leaves the frame")
        pd = src_panel(CLI, 311, 318)
        place(pd, left=SAFE_L, top=TOP_Y)
        inside(pd)
        sheet = yaml_sheet("sample-pipeline1.yaml")
        place(sheet, right=SAFE_R - 0.1, cy=-1.4)
        apart(pd, sheet, 0.2, "submit panel vs sheet")
        sb = SubmitBridge(top=2.8, bottom=-1.2)
        chain_items = [("recipe (DSL)", TOOL), ("printed YAML", OWN), ("operator (SDK)", TOOL),
                       ("engine (Kubeflow)", CLOUD), ("manager (Vertex AI Pipelines)", CLOUD)]
        chips = [chip(s, c, size=CAPTION) for s, c in chain_items]
        row1 = VGroup(*chips[:3]).arrange(RIGHT, buff=0.75)
        row2 = VGroup(*chips[3:]).arrange(RIGHT, buff=0.75)
        place(row1, cx=0, top=-1.5)
        place(row2, cx=0, top=row1.get_bottom()[1] - 0.5)
        arrows = VGroup()
        for a, b in zip(chips[:2], chips[1:3]):
            arrows.add(_arrow(a.get_right(), b.get_left(), S.GREY, 3))
        mid_y = (row1.get_bottom()[1] + row2.get_top()[1]) / 2       # the bend between the two rows
        p_a = chips[2].get_bottom() + DOWN * 0.04
        p_b = np.array([p_a[0], mid_y, 0])
        p_c = np.array([chips[3].get_center()[0], mid_y, 0])
        bend = VGroup(Line(p_a, p_b, color=S.GREY, stroke_width=3), Line(p_b, p_c, color=S.GREY, stroke_width=3),
                      _arrow(p_c + UP * 0.03, chips[3].get_top() + UP * 0.02, S.GREY, 3, buff=0))
        arrows.add(bend)
        arrows.add(_arrow(chips[3].get_right(), chips[4].get_left(), S.GREY, 3))
        s40 = VGroup(*[VGroup(c, *([arrows[i]] if i < len(arrows) else [])) for i, c in enumerate(chips)])
        inside(s40)
        apart(s40, sb, 0.15, "slide 40 chain vs bridge")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(once), FadeOut(pipe_bar), run_time=0.3)
            lr = lref_swap(self, lr, "29–30, 32–33, 40")
            self.play(ReplacementTransform(pb, pc), tracer.animate.shift(LEFT * SLIDE + DOWN * DROP), run_time=0.8)
            b304 = pc.bar(304, TOOL, 0.3)
            self.play(FadeIn(b304), pc.span(304, "compiler").animate.set_color(TOOL), run_time=0.4)
            press(self, tracer, sheet)
            vo.wait_until("The Vertex AI SDK")
            self.play(FadeOut(b304), run_time=0.2)
            self.play(ReplacementTransform(pc, pd), run_time=0.8)
            b311, b318 = pd.bar(311, TURN), pd.bar(318, TURN)
            self.play(FadeIn(b311), run_time=0.4)
            vo.wait_until("submits it as a pipeline job")
            self.play(FadeIn(b318), flash(pd.span(311, "aip.PipelineJob"), TOOL, 1.1), run_time=0.6)
            vo.wait_until("Your laptop compiles")
            self.play(FadeOut(VGroup(pd, b311, b318)), run_time=0.4)
            self.play(FadeIn(sb), sheet.animate.move_to(sb.laptop_spot), run_time=0.8)
            vo.wait_until("Vertex executes")
            self.play(sb.carry(sheet, run_time=1.0))
            self.play(LaggedStart(*[FadeIn(g, shift=RIGHT * 0.15) for g in s40], lag_ratio=0.5), run_time=1.8)

        # ========================================================== 7 · on Google's machines: containers, numbers
        region = box(12.8, 6.3, CLOUD, fill_opacity=0.05, radius=0.25)
        place(region, cx=0, top=TOP_Y)
        r_cap = label("Vertex AI Pipelines · executes", CAPTION, CLOUD)
        r_cap.move_to(region.get_corner(UP + RIGHT), aligned_edge=UP + RIGHT).shift(np.array([-0.2, -0.12, 0]))
        inside(region)
        names = ["node:" + n for n in TOY] + ["wire:square->add", "wire:square-2->add", "wire:add->square-root"]
        run_g = Tracer(show=names, note=False)
        place(run_g, cx=-0.6, cy=region.get_center()[1] - 0.15)
        inside(run_g)
        machines = run_g.machines()
        m_cap = label("a container per task", CAPTION, CTR)
        place(m_cap, right=region.get_right()[0] - 0.3, bottom=region.get_bottom()[1] + 0.25)
        apart(m_cap, run_g, 0.2, "container caption vs graph")
        apart(r_cap, run_g, 0.1, "region caption vs graph")
        vfr = sb.vertex_frame.copy()
        with self.voiceover(SAY[7]) as vo:
            self.add(vfr)
            self.play(FadeOut(s40), FadeOut(sb), ReplacementTransform(vfr, region), FadeIn(r_cap),
                      FadeOut(sheet, target_position=run_g.get_center(), scale=1.6),
                      FadeIn(run_g, scale=0.4), run_time=1.0)
            vo.wait_until("does each task get a container")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in machines], lag_ratio=0.2),
                      FadeIn(m_cap), run_time=0.9)
            vo.wait_until("and do numbers appear")
            self.play(*run_g.run("square", "square-2"), run_time=0.4)
            self.play(*run_g.succeed("square", TOY_VALUES["square"]),
                      *run_g.succeed("square-2", TOY_VALUES["square-2"]), run_time=0.5)
            self.play(*run_g.run("add"), run_time=0.35)
            self.play(*run_g.succeed("add", TOY_VALUES["add"]), run_time=0.45)
            self.play(*run_g.run("square-root"), run_time=0.35)
            self.play(*run_g.succeed("square-root", TOY_VALUES["square-root"]), run_time=0.45)
            self.play(flash(run_g.node["square-root"].sockets[0], OWN, 1.3), run_time=0.6)
            self.wait(0.6)

        # ========================================================== 8 · takeaway
        card = takeaway("calling `train()` inside the pipeline function → creates a task (a node), trains nothing"
                        " · nothing runs until the compiled job runs on Vertex", width=12.6)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(region, r_cap, run_g, machines, m_cap)), FadeOut(lr), run_time=0.6)
            lr = None
            self.play(*card.write(), run_time=1.6)
            vo.wait_until("Nothing runs until")
            self.play(flash(card.rows[-1], TURN, 1.05), run_time=0.7)
        self.play(FadeOut(card), run_time=0.6)
        self.wait(0.3)
