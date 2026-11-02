"""S03 · task.output: the wire that makes an edge (V2, the wire).
Lecture: 28–29, 34.

Beats (script.md "## S03", one voiceover block each):
 0  LECTURE 28–29. CODE(ml-workflow/src/workflow/cli.py: 297–301) on the left, line 300 lit; the
    two `.output` sub-strings light GREEN as the SAY names x and y (each square node flashes). On the
    right the V1 graph from S02: four nodes, empty sockets, GREY dotted connections; the "?" pulses.
 1  "Not a number": square's empty socket is ringed GREY; a GREY chip "placeholder: exists after
    `square` succeeds" writes in under the panel; the dotted connection square → add turns into a
    PINK solid wire, then square-2 → add (the sockets stay empty).
 2  The code panel and the chip leave; the graph slides left; CODE(sample-pipeline1.yaml: 176–187)
    comes in on the right: 181–183 (`dependentTasks: - square - square-2`) lit PINK, 187 lit GREEN;
    it Transforms into 186–193 (187–189 and 191–193 lit GREEN, `producerTask` flashes), then into
    the window folded to 218, …, 223–230 (223–224 PINK, 228–230 GREEN) as the third wire
    add → square-root draws PINK.
 3  The YAML panel fades. Run: both squares fill YELLOW; square gets its ✓ and 9.0, only then a
    GREEN token 9.0 rides the PINK wire into add; square-2 does the same with 16.0; add fills YELLOW
    only when both tokens have arrived. A GREY chip "one argument → data + dependency" writes in.
 4  Tag `illustration`: a small card on the right: node `split` with sockets `train_uri` and
    `test_uri`, node `train`; `split.outputs["train_uri"]` writes under them and a PINK wire leaves
    only the `train_uri` socket.
 5  The graph and the split card leave (no room for the graph above two rows). Tag `illustration`, two rows. Top: `prep → train` with a
    PINK solid wire; prep ✓, a GREEN token `gs://my-bucket/runs/0427/clean.csv` (this run's path)
    leaves its socket, rides into train and settles under it; train fills YELLOW. Bottom: the same
    two nodes, no wire, train holding a GREY sticky note `"gs://my-bucket/clean.csv"`, a BLUE bucket
    with last week's GREY dashed file; prep and train fill YELLOW together.
 6  Bottom row: a RED arrow from last week's file into train, RED stamp "stale"; train ✓, outlined
    RED; then prep ✓ and its fresh GREEN clean.csv lands on the old file, one beat too late. A RED ✗
    and "no edge" where a wire would be; the sticky note flashes.
 7  The rows leave. A PINK dashed wire prep → train with `train(...).after(prep)`; prep runs, ✓
    (its socket stays empty), only then train fills YELLOW; the dashed wire flashes and a GREY
    chip "nothing rides it" writes in.
 8  The canvas clears. PONDER P1 (MCQ card, tag `illustration`, 8 s timer).
 9  Reveal: B fills YELLOW ✓, GREEN note; RED reason under A.
10  RED reasons under C and D; a RED-framed card with the kfp error message and the PURPLE chip
    `kfp 2.14.6 · read, not run` above the card.
11  The card fades. TAKEAWAY (three rows), each row flashes as the SAY reaches it; empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    MoveAlongPath,
    ReplacementTransform,
    VGroup,
    Write,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ the real sources
CLI = "ml-workflow/src/workflow/cli.py"
YAML = "ml-workflow/src/workflow/sample-pipeline1.yaml"
assert "a: float = 3.0" in source_line(CLI, 297), source_line(CLI, 297)
assert source_line(CLI, 298).strip() == "a_sq_task = square(x=a)", source_line(CLI, 298)
assert source_line(CLI, 299).strip() == "b_sq_task = square(x=b)", source_line(CLI, 299)
assert source_line(CLI, 300).strip() == "sum_task = add(x=a_sq_task.output, y=b_sq_task.output)", \
    source_line(CLI, 300)
assert source_line(CLI, 301).strip() == "return square_root(x=sum_task.output).output", source_line(CLI, 301)
assert source_line(YAML, 176).strip() == "add:", source_line(YAML, 176)
assert source_line(YAML, 181).strip() == "dependentTasks:", source_line(YAML, 181)
assert source_line(YAML, 182).strip() == "- square", source_line(YAML, 182)
assert source_line(YAML, 183).strip() == "- square-2", source_line(YAML, 183)
assert source_line(YAML, 187).strip() == "taskOutputParameter:", source_line(YAML, 187)
assert source_line(YAML, 189).strip() == "producerTask: square", source_line(YAML, 189)
assert source_line(YAML, 191).strip() == "taskOutputParameter:", source_line(YAML, 191)
assert source_line(YAML, 193).strip() == "producerTask: square-2", source_line(YAML, 193)
assert source_line(YAML, 218).strip() == "square-root:", source_line(YAML, 218)
assert source_line(YAML, 223).strip() == "dependentTasks:", source_line(YAML, 223)
assert source_line(YAML, 224).strip() == "- add", source_line(YAML, 224)
assert source_line(YAML, 230).strip() == "producerTask: add", source_line(YAML, 230)
assert TOY_VALUES["square"] == "9.0" and TOY_VALUES["square-2"] == "16.0", TOY_VALUES
assert KFP_ERROR == "The task has multiple outputs. Please reference the output by its name.", KFP_ERROR

# P1 (script.md PONDER P1; the right answer is B: index 1)
P1_Q = ('`split = split_data()` has two outputs, `train_uri` and `test_uri`. '
        '`TRAIN_URI = "gs://my-bucket/split/train.csv"`. Which call gives `train` the file '
        '**this run** produced, and makes it wait for `split`?')
P1_OPTS = ['`train(data_uri="gs://my-bucket/split/train.csv")`',
           '`train(data_uri=split.outputs["train_uri"])`',
           '`train(data_uri=TRAIN_URI).after(split)`',
           '`train(data_uri=split.output)`']
P1_ANSWER = 1
assert "outputs[" in P1_OPTS[P1_ANSWER] and ".after(" not in P1_OPTS[P1_ANSWER]

RUN_PATH = f"{BUCKET}/runs/0427/clean.csv"

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
    guard(m.get_left()[0] >= l and m.get_right()[0] <= r and m.get_bottom()[1] >= b and m.get_top()[1] <= t,
          f"out of the frame: {m.get_left()[0]:.2f} {m.get_right()[0]:.2f} {m.get_bottom()[1]:.2f} "
          f"{m.get_top()[1]:.2f}")


def apart(a, b, gap=0.1, msg=""):
    """a and b do not overlap (their boxes are at least `gap` apart on one axis)."""
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    guard(sep, f"overlap: {msg}")


def flash(mob, color: str = TURN, k: float = 1.15, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def wrapped_header(p, lines_note: str):
    """Put a panel's "· line N wrapped" header parts on a second header row, so the header is no
    wider than the code (the panel shares the frame with the graph)."""
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


def split_header(p):
    """Put a panel's header on two rows: the directory, then the file name and "· lines a–b", so
    the header is no wider than the code (the YAML panel shares the frame with the graph)."""
    path = p.source_name
    d, f = path.rsplit("/", 1)
    h = p.header
    rest = list(h.submobjects[1:])
    for m in rest:
        h.remove(m)
    row1 = mono(d + "/", CAPTION, S.GREY)
    row2 = VGroup(mono(f, CAPTION, S.GREY), *rest).arrange(RIGHT, buff=0.12)
    for m in rest:
        m.align_to(row2[0], DOWN)
    new = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    new.next_to(p.code, UP, buff=0.1).align_to(p.code, LEFT).shift(RIGHT * 0.12)
    p.remove(h)
    p.header = new
    p.add(new)
    return p


def note_chip(text: str, color: str = S.GREY, width: float = 6.0, text_color: str = INK):
    """A GREY-outlined note: serif rows with `code` mono, wrapped to `width`. .frame .rows"""
    rows = fit_rows(text, width, CAPTION, text_color)
    fr = box(rows.width + 0.4, rows.height + 0.26, color, fill=S.BG, fill_opacity=0.9, radius=0.14)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


class OutputWire(VoiceScene):
    def construct(self):
        assert len(SAY) == 12, len(SAY)

        # ========================================================== 0 · the add call passes .output twice
        lr = None
        pa = src_panel(CLI, 297, 301, wrap={297: ["b: float"], 300: ["y=b_sq"], 301: ["x=sum_task"]})
        wrapped_header(pa, "· lines 297, 300 and 301 wrapped")
        place(pa, left=SAFE_L, top=TOP_Y)
        inside(pa)
        tracer = Tracer(show=None)
        place(tracer, right=SAFE_R, top=TOP_Y - 0.25)
        inside(tracer)
        apart(pa, tracer, 0.1, "code panel vs graph")
        sq, sq2, add, root = (tracer.node[n] for n in TOY)
        b300 = pa.bar(300, TURN)
        out_x = pa.span(300, "a_sq_task.output")
        out_y = pa.span(300, "b_sq_task.output")
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "28–29")
            self.play(FadeIn(pa, shift=RIGHT * 0.2), FadeIn(tracer, shift=LEFT * 0.2), run_time=0.9)
            vo.wait_until("Look at the add call")
            self.play(FadeIn(b300), flash(add.frame, INK, 1.08), run_time=0.6)
            vo.wait_until("For x")
            self.play(out_x.animate.set_color(OWN), flash(sq.frame, OWN, 1.1), run_time=0.7)
            vo.wait_until("For y")
            self.play(out_y.animate.set_color(OWN), flash(sq2.frame, OWN, 1.1), run_time=0.7)
            vo.wait_until("So what is being passed")
            self.play(*tracer.parts_in("note"), run_time=0.4)
            self.play(flash(tracer.parts["note"], INK, 1.5), run_time=0.7)

        # ========================================================== 1 · a placeholder; plugging it in draws a wire
        ph = note_chip("placeholder: exists after `square` succeeds", width=6.0)
        place(ph, left=pa.get_left()[0] + 0.1, top=pa.get_bottom()[1] - 0.3)
        inside(ph)
        apart(ph, tracer, 0.15, "placeholder chip vs graph")
        sock_ring = ring(sq.sockets[0], S.GREY, buff=0.08, stroke=3)
        with self.voiceover(SAY[1]) as vo:
            self.play(Create(sock_ring), run_time=0.5)
            vo.wait_until("Dot output is a placeholder")
            self.play(FadeIn(ph, shift=UP * 0.1), flash(out_x, OWN, 1.1), run_time=0.7)
            vo.wait_until("exists only after")
            self.play(flash(sq.frame, TURN, 1.08), run_time=0.7)
            vo.wait_until("Plugging it in")
            self.play(FadeOut(sock_ring), *tracer.parts_out("note"), *tracer.restyle("square", "add", "data"),
                      run_time=0.7)
            self.play(*tracer.restyle("square-2", "add", "data"), run_time=0.7)
            self.play(tracer.wire[("square", "add")].light(EDGE), tracer.wire[("square-2", "add")].light(EDGE),
                      run_time=0.8)

        # ========================================================== 2 · the compiled YAML writes each wire twice
        y1 = src_panel(YAML, 176, 187)
        y2 = src_panel(YAML, 186, 193)
        y3 = src_panel(YAML, [(218, 218), (223, 230)])
        g_target = tracer.copy()
        place(g_target, left=SAFE_L + 0.05)
        for y in (y1, y2, y3):
            split_header(y)
            place(y, left=g_target.get_right()[0] + 0.25, top=TOP_Y)
            inside(y)
        for y in (y1, y2, y3):
            apart(g_target, y, 0.15, "graph vs YAML panel")
        dx = g_target.get_center()[0] - tracer.get_center()[0]
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(pa, b300, ph)), run_time=0.5)
            self.play(tracer.animate.shift(RIGHT * dx), run_time=0.7)
            self.play(FadeIn(y1, shift=LEFT * 0.3), run_time=0.6)
            vo.wait_until("add's dependent tasks")
            dep = VGroup(*[y1.bar(n, EDGE, 0.3) for n in (181, 182, 183)])
            self.play(FadeIn(dep), flash(add.frame, INK, 1.08), run_time=0.6)
            vo.wait_until("list square and square 2")
            self.play(tracer.wire[("square", "add")].light(EDGE), tracer.wire[("square-2", "add")].light(EDGE),
                      flash(y1.span(182, "square"), EDGE, 1.2), flash(y1.span(183, "square-2"), EDGE, 1.2),
                      run_time=0.8)
            vo.wait_until("and each input")
            b187 = y1.bar(187, OWN, 0.3)
            self.play(FadeIn(b187), run_time=0.4)
            self.play(FadeOut(VGroup(dep, b187)), ReplacementTransform(y1, y2), run_time=0.8)
            prod = VGroup(*[y2.bar(n, OWN, 0.3) for n in (187, 188, 189, 191, 192, 193)])
            self.play(FadeIn(prod), run_time=0.5)
            vo.wait_until("names its producer task")
            self.play(flash(y2.span(189, "square"), OWN, 1.2), flash(sq.frame, OWN, 1.08), run_time=0.6)
            self.play(flash(y2.span(193, "square-2"), OWN, 1.2), flash(sq2.frame, OWN, 1.08), run_time=0.6)
            self.play(FadeOut(prod), ReplacementTransform(y2, y3), run_time=0.8)
            third = VGroup(*[y3.bar(n, EDGE, 0.3) for n in (223, 224)], *[y3.bar(n, OWN, 0.3) for n in (228, 229, 230)])
            self.play(FadeIn(third), *tracer.restyle("add", "square-root", "data"), run_time=0.8)
            self.play(tracer.wire[("add", "square-root")].light(EDGE), run_time=0.7)

        # ========================================================== 3 · run time: 9 rides only after square succeeds
        one = note_chip("one argument → data + dependency", color=EDGE, width=5.0)
        place(one, cx=3.3, cy=0.3)
        inside(one)
        apart(one, tracer, 0.3, "one-argument chip vs graph")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(y3, third)), run_time=0.5)
            self.play(*tracer.run("square", "square-2"), run_time=0.5)
            vo.wait_until("square turns green")
            self.play(*tracer.succeed("square", TOY_VALUES["square"]), run_time=0.6)
            vo.wait_until("and only then does 9")
            t9 = tracer.send(self, "square", "add", TOY_VALUES["square"], run_time=1.0)
            self.play(*tracer.succeed("square-2", TOY_VALUES["square-2"]), run_time=0.5)
            t16 = tracer.send(self, "square-2", "add", TOY_VALUES["square-2"], run_time=1.0)
            self.play(FadeOut(t9, scale=0.6), FadeOut(t16, scale=0.6), *tracer.run("add"), run_time=0.6)
            vo.wait_until("One argument")
            self.play(FadeIn(one, shift=LEFT * 0.15), tracer.wire[("square", "add")].light(EDGE), run_time=0.8)
            vo.wait_until("both its data")
            r9 = ring(sq.values[0], OWN, buff=0.07, stroke=3)
            self.play(Create(r9), run_time=0.5)
            self.play(FadeOut(r9), run_time=0.3)
            vo.wait_until("and its dependency")
            self.play(flash(sq.ok, OWN, 1.4), tracer.wire[("square", "add")].light(EDGE), run_time=0.7)

        # ========================================================== 4 · several outputs: name the one you want
        sp = TaskNode("split", outputs=("train_uri", "test_uri"), socket_labels=True)
        tn = TaskNode("train", outputs=())
        lab0 = sp.socket_labels[0]
        tn.shift(np.array([lab0.get_right()[0] + 0.7 + tn.frame.width / 2, sp.sockets[0].get_center()[1] + 0.85, 0])
                 - tn.frame.get_center())
        sw = Wire(sp, tn, "data", start=lab0.get_right() + RIGHT * 0.12, end=tn.in_point())
        code = mono('split.outputs["train_uri"]', 22, INK)
        code[code.text.index('"train_uri"'):code.text.index('"train_uri"') + len('"train_uri"')].set_color(OWN)
        figure = VGroup(sp, sw, tn)
        code.next_to(figure, DOWN, buff=0.4).align_to(figure, LEFT)
        body = VGroup(figure, code)
        fr = box(body.width + 0.6, body.height + 1.0, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.16)
        body.move_to(fr).shift(DOWN * 0.15)
        tg = illustration_tag()
        tg.move_to(fr.get_corner(UP + RIGHT) + np.array([-0.2 - tg.width / 2, -0.12 - tg.height / 2, 0]))
        card4 = VGroup(fr, tg, body)
        place(card4, right=SAFE_R - 0.05, cy=0.2)
        inside(card4)
        apart(card4, tracer, 0.2, "split card vs graph")
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(one), run_time=0.4)
            self.play(FadeIn(VGroup(fr, tg, sp, tn), shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("you name the one you want")
            self.play(flash(lab0, OWN, 1.2), flash(sp.socket_labels[1], OWN, 1.2), run_time=0.7)
            vo.wait_until("dot outputs")
            self.play(Write(code), run_time=0.9)
            vo.wait_until("with the output's name")
            self.play(sw.draw(), flash(lab0, OWN, 1.2), run_time=0.8)
            self.play(sw.light(EDGE), run_time=0.7)

        # ========================================================== 5 · the contrast: a wire vs a hard-coded path
        wa = WirePlug("wire")
        wb = WirePlug("note")
        wa.shift(UP * (1.95 - wa.prep.frame.get_center()[1]))
        wb.shift(UP * (0.05 - wb.prep.frame.get_center()[1]))
        wa.set_x(-0.6)
        wb.set_x(-0.6)
        tag5 = illustration_tag()
        title_a = VGroup(label("with the wire:", CAPTION, S.GREY), mono("train(data_uri=prep.output)", CAPTION, EDGE)) \
            .arrange(RIGHT, buff=0.15)
        title_b = VGroup(label("hard-coded:", CAPTION, S.GREY),
                         mono(f'train(data_uri="{BUCKET}/clean.csv")', CAPTION, INK)).arrange(RIGHT, buff=0.15)
        for t in (title_a, title_b):
            t[1].align_to(t[0], DOWN)
        place(title_a, left=SAFE_L + 0.1, top=TOP_Y)
        place(tag5, left=title_a.get_right()[0] + 0.3, cy=title_a.get_center()[1])
        place(title_b, left=SAFE_L + 0.1, bottom=wb.prep.get_top()[1] + 0.25)
        tok = value_token(RUN_PATH)
        tok_end = tok.copy()
        place(tok_end, cx=wa.train.frame.get_center()[0], top=wa.train.frame.get_bottom()[1] - 0.22)
        for m in (wa, wb, title_a, title_b, tok_end, tag5):
            inside(m)
        apart(title_a, wa, 0.1, "title A vs row A")
        apart(tok_end, title_b, 0.1, "path token vs title B")
        apart(title_b, wb, 0.05, "title B vs row B")
        apart(wa, wb, 0.3, "row A vs row B")
        guard(tag5.get_right()[0] <= 2.4, "illustration tag runs into the lecture tag")
        RIDE_DY = 0.55                    # the long path rides just under the wire (never over train's name)
        tok.move_to(wa.wire_.path.get_start() + DOWN * RIDE_DY)
        ride_path = wa.wire_.path.copy().shift(DOWN * RIDE_DY)
        apart(tok, title_b, 0.05, "path token vs title B")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(tracer, card4, sw, code)), run_time=0.6)
            vo.wait_until("Now the contrast")
            self.play(FadeIn(VGroup(title_a, tag5), shift=DOWN * 0.1), FadeIn(wa), run_time=0.8)
            vo.wait_until("Often the output")
            self.play(*wa.start(), run_time=0.5)
            vo.wait_until("the file this run wrote")
            self.play(*wa.finish_prep(), run_time=0.5)
            self.play(FadeIn(tok, scale=0.8), run_time=0.4)
            vo.wait_until("With the wire")
            self.play(MoveAlongPath(tok, ride_path, run_time=1.0), wa.wire_.light(EDGE))
            self.play(tok.animate.move_to(tok_end), run_time=0.5)
            vo.wait_until("after prep succeeds")
            self.play(*wa.train.run(), flash(wa.prep.ok, OWN, 1.4), run_time=0.6)
            vo.wait_until("Hard-code a path instead")
            self.play(FadeIn(title_b, shift=DOWN * 0.1), FadeIn(wb), run_time=0.8)
            vo.wait_until("and there is no wire")
            self.play(flash(wb.parts["note"], INK, 1.1), run_time=0.6)
            vo.wait_until("train starts right away")
            self.play(*wb.start(), run_time=0.6)

        # ========================================================== 6 · the stale read
        mid = (wb.prep.sockets[0].get_right() + wb.train.frame.get_left()) / 2
        no_x = x_mark(0.34).move_to(mid)
        no_lbl = label("no edge", CAPTION, ERR).next_to(no_x, DOWN, buff=0.12)
        apart(no_lbl, title_b, 0.05, "no-edge label vs title B")
        with self.voiceover(SAY[6]) as vo:
            self.play(*wa.train.succeed(), run_time=0.4)
            vo.wait_until("The file there")
            stale = wb.stale_read()
            self.play(flash(wb.old_file, S.GREY, 1.15), run_time=0.6)
            self.play(stale[0], run_time=0.6)
            vo.wait_until("and the step succeeds")
            self.play(*stale[1:], run_time=0.6)
            self.play(*wb.finish_prep(), run_time=0.4)
            self.play(*wb.fresh_lands(), run_time=0.7)
            vo.wait_until("A guessed path")
            self.play(FadeIn(no_x, scale=1.4), FadeIn(no_lbl, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("not to the pipeline")
            self.play(flash(wb.parts["note"], ERR, 1.1), run_time=0.7)

        # ========================================================== 7 · .after(): order without data
        af = WirePlug("after")
        place(af, cx=0, cy=0.5)
        inside(af)
        nothing = note_chip("nothing rides it: the socket stays empty", width=6.0)
        place(nothing, cx=0, top=af.get_bottom()[1] - 0.4)
        inside(nothing)
        apart(nothing, af, 0.15, "nothing chip vs after row")
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(wa, wb, tok, title_a, title_b, no_x, no_lbl)), run_time=0.6)
            self.play(FadeIn(af), run_time=0.6)
            vo.wait_until("dot after adds a dashed edge")
            self.play(af.wire_.light(EDGE), flash(af.parts["after_label"], EDGE, 1.1), run_time=0.8)
            vo.wait_until("the task waits")
            self.play(*af.start(), run_time=0.5)
            vo.wait_until("to succeed")
            self.play(*af.finish_prep(), run_time=0.5)
            self.play(*af.train.run(), run_time=0.5)
            vo.wait_until("but nothing travels")
            empty = ring(af.prep.sockets[0], S.GREY, buff=0.08, stroke=3)
            self.play(af.wire_.light(EDGE), Create(empty), run_time=0.8)
            self.play(FadeIn(nothing, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 8 · PONDER P1
        with self.voiceover(SAY[8]) as vo:
            card = mcq_ponder(self, P1_Q, P1_OPTS, seconds=8, hide=(af, nothing, tag5, empty))
        guard(card.get_top()[1] <= 3.1, "MCQ card under the lecture tag")

        # ========================================================== 9 · B; A has no edge
        with self.voiceover(SAY[9]) as vo:
            self.play(*card.reveal(P1_ANSWER, "named output → this run's file + the edge"), run_time=0.8)
            vo.wait_until("A hard-codes")
            self.play(*card.reason(0, "no edge → may start at once, reads last run's file"), run_time=0.7)
            vo.wait_until("no edge")
            self.play(flash(card.options[0].text, ERR, 1.04), run_time=0.6)

        # ========================================================== 10 · C waits on an assumed path; D fails at compile
        err_lines = ("The task has multiple outputs.", "Please reference the output by its name.")
        assert " ".join(err_lines) == KFP_ERROR
        err_rows = VGroup(*[mono(s, CAPTION, INK) for s in err_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        err_fr = box(err_rows.width + 0.4, err_rows.height + 0.26, ERR, fill=S.BG, fill_opacity=0.95, radius=0.12)
        err_rows.move_to(err_fr)
        kc = kfp_chip()
        err = VGroup(VGroup(err_fr, err_rows), kc)
        kc.next_to(err[0], RIGHT, buff=0.25)
        q = card.question
        place(err, left=q.get_left()[0], cy=q.get_center()[1])
        inside(err)
        guard(err.get_right()[0] <= card.frame.get_right()[0] - 0.3, "kfp error card leaves the MCQ card")
        guard(err.get_bottom()[1] >= card.options[0].get_top()[1] + 0.05, "kfp error card vs option A")
        with self.voiceover(SAY[10]) as vo:
            self.play(*card.reason(2, "waits, but reads a path you assumed: if split writes anywhere else, "
                                      "it's stale or missing"), run_time=0.7)
            vo.wait_until("D fails")
            self.play(*card.reason(3, "two outputs → must name one"), run_time=0.6)
            self.play(q.animate.set_opacity(0), run_time=0.4)
            self.play(FadeIn(err, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("K F P refuses")
            self.play(flash(err_rows, ERR, 1.04), run_time=0.6)

        # ========================================================== 11 · takeaway
        tk = takeaway("`.output` → waits for success, gets this run's value · hard-coded or guessed path → no edge, "
                      "maybe stale · `.after()` → order, no data")
        inside(tk)
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(card), FadeOut(err), run_time=0.6)
            self.play(*tk.write(), run_time=1.6)
            vo.wait_until("If the question says")
            self.play(flash(tk.rows[0], TURN, 1.04), run_time=0.6)
            vo.wait_until("A hard-coded or guessed path")
            self.play(flash(tk.rows[1], TURN, 1.04), run_time=0.6)
            vo.wait_until("Dot after")
            self.play(flash(tk.rows[2], TURN, 1.04), run_time=0.6)
        self.play(FadeOut(tk), FadeOut(lr), run_time=0.6)
        self.wait(0.3)
