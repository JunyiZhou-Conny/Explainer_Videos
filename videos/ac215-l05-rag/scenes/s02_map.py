"""S02 · Two lanes, one database (concept scene: no README tracker). Lecture: A12–A16, B5–B6.

Beats (script.md "## S02", one voiceover block each):
0. LECTURE A12–A14. Our redrawing of A12 in five boxes, built as named: a GREY user glyph; a PINK
   arrow "question" into a PURPLE cluster of three gears "RAG code"; a PINK arrow up to a TEAL
   cylinder "vector database" and a GREEN arrow "retrieved texts" back down; a GREEN elbow arrow
   "full prompt" into a BLUE "LLM" box; a BLUE arrow "response" back to the user. A thin RED
   dotted line between cylinder and LLM gets a RED cross: "never talk".
1. LECTURE A16. The gears open up: two faint lane bands grow out of them, the arrows go, and the
   user, the cylinder and the LLM move to their places in V1 (RagMap). Top lane as named: GREEN
   pages "knowledge base" -> PURPLE ruler "chunking" -> a BLUE "embedding model" box (top half
   only, so far) -> GREEN vectors -> the TEAL cylinder. Bottom lane: a PINK question arrow runs
   straight at the cylinder, as on A12; then the BLUE box slides down between, cutting it, the
   question passes through the box's lower half (a PINK highlight) and leaves as a PINK query
   vector; a chip at the cylinder: "the database gets numbers, not words".
2. LECTURE B5–B6. The bottom lane goes on (cylinder -> GREEN prompt card -> BLUE LLM -> answer,
   a BLUE arrow back to the user) while "the pipeline slide" is named; then B5's three dashed
   regions fade in one at a time as named: Indexing (the whole top lane), Retrieval (the lower
   half of the embedding box, the query vector, the cylinder, the arrow into the prompt card; a
   YELLOW flash runs along that arrow into the pulsing prompt card, "brings the context"),
   Augmentation & Generation (the LLM only).
3. The regions dim to outlines (tabs and lecture tag leave). The README's two step titles
   (README.md lines 5 and 9) label the lanes; five YELLOW flag chips (README.md lines 17–21 as
   text, no emoji) drop under their boxes as named, each box pulsing as its chip lands.
4. The top lane pulses once, slowly ("once · offline · slow" under it); the bottom lane pulses
   quickly three times ("every question"). The shared BLUE box gets a YELLOW edge and a rule card
   writes above it: "same model · same 256 numbers · both lanes" / "chunks before, questions
   later". A small RED "what if" inset right of the top lane's end (tag illustration): a
   different BLUE box, "another model", feeds a sketch of the space in which its question vector
   points away from the GREEN chunk vectors, into an empty region; RED cross.
5. V1's second layer: TEAL "CLI container" around the ruler ("no network needed"); BLUE dashed
   "Google" outlines around the embedding model and the LLM, a GOLD tag "pay per use · your key"
   and a GREY note "no VM, no bucket: nothing keeps running"; TEAL "Chroma container" around the
   cylinder, a PINK route down to a GREY folder "on your laptop".
6. Everything but the CLI container frame fades; the frame grows to the centre and five GREY
   command lines appear inside it, one per flag. Fade out to an empty frame.
"""

import numpy as np
from common import (
    CLOUD,
    CTR,
    DATA,
    ERR,
    INK,
    LAPTOP,
    LOOKUP,
    NARRATION,
    TOOL,
    TURN,
    RagMap,
    _set_op,
    cost_tag,
    cylinder,
    gears_glyph,
    grey_tag,
    illustration_tag,
    lref,
    model_box,
    note,
    person,
    sans,
    vec_glyph,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Circle,
    Create,
    DashedLine,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromPoint,
    LaggedStart,
    Line,
    RoundedRectangle,
    Rotate,
    ShowPassingFlash,
    Succession,
    Text,
    Transform,
    VGroup,
    VMobject,
    Write,
    there_and_back,
)

from explainer import style as S
from explainer.devops import box, cross_mark, mono, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S02"]

YT, YB, X = RagMap.YT, RagMap.YB, RagMap.X
FLAGS = ["--chunk", "--embed", "--load", "--query", "--chat"]


# ------------------------------------------------------------------ small helpers
def arrow(a, b, color, stroke: float = 4, tip: float = 0.18) -> Arrow:
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color,
                 stroke_width=stroke, max_tip_length_to_length_ratio=0.3, tip_length=tip)


def elbow(points, color, stroke: float = 4) -> VGroup:
    """A polyline whose last segment is an arrow (draw it with Create(..., lag_ratio=1))."""
    pts = [np.array(p, dtype=float) for p in points]
    line = VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners(pts[:-1])
    return VGroup(line, arrow(pts[-2], pts[-1], color, stroke))


def pulse(m, color: str = TURN, k: float = 1.1):
    """A there-and-back emphasis: the strokes take `color`, the shape grows a little."""
    return m.animate(rate_func=there_and_back).scale(k).set_stroke(color)


def shown_copy(part):
    """A free copy of a hidden RagMap part at full opacity (the target of a morph)."""
    c = part.copy()
    _set_op(c)
    return c


def draw(g):
    """Draw a location part: its frames and routes are drawn, its tags and labels fade in."""
    def has_text(s):
        return any(isinstance(f, Text) for f in s.get_family())

    return AnimationGroup(*[FadeIn(s) if getattr(s, "keep_size", False) or has_text(s) else Create(s)
                            for s in g.submobjects])


def card(rows, color: str = S.GREY, pad: float = 0.22) -> VGroup:
    """Rows of text in an opaque rounded card with a `color` border. .frame .rows"""
    rows = VGroup(*rows).arrange(DOWN, buff=0.1)
    fr = RoundedRectangle(width=rows.width + 2 * pad + 0.1, height=rows.height + 2 * pad,
                          corner_radius=0.14, stroke_color=color, stroke_width=2.5).set_fill(S.BG, 0.95)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


# ------------------------------------------------------------------ the scene
class TwoLanes(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0. A12 in five boxes
        lr = lref("A12–A14")
        u_pos = np.array([-5.0, YB, 0])
        g_pos = np.array([-0.8, YB, 0])
        c_pos = np.array([-0.8, 1.55, 0])
        l_pos = np.array([4.2, 1.55, 0])

        user = person(LAPTOP, 0.7).move_to(u_pos)
        u_lab = sans("user", 20, S.GREY).move_to(u_pos + DOWN * 0.74)
        gears = gears_glyph(TOOL, 0.36).move_to(g_pos)
        g_lab = sans("RAG code", 20, TOOL).next_to(gears, DOWN, buff=0.16)
        q_arr = arrow(user.get_right() + RIGHT * 0.1, [gears.get_left()[0] - 0.12, YB, 0], LOOKUP)
        q_lab = sans("question", 20, LOOKUP).next_to(q_arr, UP, buff=0.12)
        cyl = cylinder(0.95, 1.1).move_to(c_pos)
        c_lab = sans("vector database", 20, S.GREY).next_to(cyl, UP, buff=0.14)
        y_lo, y_hi = gears.get_top()[1] + 0.08, cyl.get_bottom()[1] - 0.06
        up = arrow([g_pos[0] - 0.25, y_lo, 0], [g_pos[0] - 0.25, y_hi, 0], LOOKUP)
        down = arrow([g_pos[0] + 0.25, y_hi, 0], [g_pos[0] + 0.25, y_lo, 0], DATA)
        rt_lab = sans("retrieved texts", 20, DATA).next_to(down, RIGHT, buff=0.2)
        llm = model_box("LLM", 1.3, 0.9).move_to(l_pos)
        lb = llm.frame.get_bottom()[1]
        full = elbow([[gears.get_right()[0] + 0.1, YB, 0], [l_pos[0] - 0.3, YB, 0],
                      [l_pos[0] - 0.3, lb - 0.04, 0]], DATA)
        fp_lab = sans("full prompt", 20, DATA).move_to([(gears.get_right()[0] + l_pos[0]) / 2, YB + 0.3, 0])
        y_back = -2.5
        resp = elbow([[l_pos[0] + 0.3, lb - 0.04, 0], [l_pos[0] + 0.3, y_back, 0],
                      [u_pos[0], y_back, 0], [u_pos[0], u_lab.get_bottom()[1] - 0.06, 0]], CLOUD)
        r_lab = sans("response", 20, CLOUD).move_to([1.4, y_back + 0.28, 0])
        x0, x1 = cyl.get_right()[0] + 0.12, llm.frame.get_left()[0] - 0.12
        never = DashedLine([x0, c_pos[1], 0], [x1, c_pos[1], 0], color=ERR, stroke_width=2.5,
                           dash_length=0.06, dashed_ratio=0.45)
        xm = (x0 + x1) / 2
        cross = cross_mark(0.34, ERR).move_to([xm, c_pos[1], 0])
        n_lab = sans("never talk", 20, ERR).move_to([xm, c_pos[1] + 0.42, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(lr), FadeIn(user, shift=RIGHT * 0.2), FadeIn(u_lab), run_time=0.7)
            vo.wait_until("The user's question")
            self.play(GrowArrow(q_arr), FadeIn(q_lab), run_time=0.7)
            self.play(FadeIn(gears, scale=0.6), FadeIn(g_lab), run_time=0.6)
            self.play(Rotate(gears[0], 1.2), Rotate(gears[1], -1.6), Rotate(gears[2], -1.6), run_time=0.8)
            vo.wait_until("which asks a vector database")
            self.play(GrowArrow(up), run_time=0.5)
            self.play(FadeIn(cyl, shift=DOWN * 0.15), FadeIn(c_lab), run_time=0.6)
            self.play(GrowArrow(down), FadeIn(rt_lab, shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("The code joins")
            self.play(Rotate(gears[0], 1.2), Rotate(gears[1], -1.6), Rotate(gears[2], -1.6), run_time=0.7)
            self.play(Create(full, lag_ratio=1), FadeIn(fp_lab), run_time=1.1)
            self.play(FadeIn(llm, scale=0.8), run_time=0.5)
            vo.wait_until("and the model's response")
            self.play(Create(resp, lag_ratio=1), FadeIn(r_lab), run_time=1.4)
            vo.wait_until("The database never talks")
            self.play(Create(never), run_time=0.6)
            self.play(Create(cross), FadeIn(n_lab, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 1. V1 grows out of the gears
        m = RagMap(show=())
        # clearances the shared layout leaves at zero (a request for common.py is in the report)
        m.parts["lab_query"].shift(UP * 0.08)           # off the Retrieval region's bottom edge
        m.parts["loc_google"][2].shift(DOWN * 0.13)     # "Google · Vertex AI" off the embedding box
        m.parts["loc_google"][3].shift(UP * 0.12)       # "Google" off the LLM box's top edge
        m.parts["loc_chroma"][1].shift(UP * 0.08)       # "Chroma container" off the cylinder's lid
        bands =VGroup(*[RoundedRectangle(width=12.9, height=1.3, corner_radius=0.3, stroke_width=0)
                         .set_fill(S.GREY, 0.07).move_to([0, y, 0]) for y in (YT, YB)])
        bands.set_z_index(-2)
        morph = {"user": user, "lab_user": u_lab, "database": cyl, "lab_database": c_lab, "llm": llm}
        targets = {k: shown_copy(m.parts[k]) for k in morph}
        a12_rest = VGroup(q_arr, q_lab, up, down, rt_lab, full, fp_lab, resp, r_lab, never, cross, n_lab)
        em = m.parts["embedding"]
        half = box(em.width, 1.55, CLOUD, fill_opacity=0.12, radius=0.14, stroke=3)
        half.move_to(em.get_top(), aligned_edge=UP)
        em_l, em_r = em.get_left()[0], em.get_right()[0]
        db = m.parts["database"]
        straight = arrow(m.parts["a_question"].get_start(), [db.get_left()[0] - 0.08, YB, 0], LOOKUP)
        hl = RoundedRectangle(width=em.width - 0.12, height=em.height / 2 - 0.1, corner_radius=0.1,
                              stroke_width=0).set_fill(LOOKUP, 0.35)
        hl.move_to(em.get_bottom() + UP * em.height / 4)          # the box's lower half
        flash = Line([em_l, YB, 0], [em_r, YB, 0], color=LOOKUP, stroke_width=8)
        nums = card([sans("the database gets", 20, INK), sans("numbers, not words", 20, LOOKUP)], LOOKUP)
        nums.move_to([X["database"] + 0.25, -2.45, 0])
        nums_link = Line([X["database"], nums.get_top()[1], 0], [X["database"], db.get_bottom()[1] - 0.08, 0],
                         color=LOOKUP,
                         stroke_width=2.5)

        with self.voiceover(SAY[1]) as vo:
            self.add(m)
            lr16 = lref("A16")
            self.play(Succession(FadeOut(lr), FadeIn(lr16)), FadeOut(a12_rest), FadeOut(gears, scale=2.4),
                      FadeOut(g_lab),
                      *[GrowFromPoint(b, gears.get_center()) for b in bands],
                      *[Transform(morph[k], targets[k]) for k in morph], run_time=1.4)
            for k in morph:
                self.remove(morph[k])
                m.parts_in(k)                       # the real part takes the copy's place
            lr = lr16
            vo.wait_until("On top, books are cut")
            self.play(*m.parts_in("books", "lab_books"), run_time=0.5)
            self.play(*m.parts_in("a_books", anim=GrowArrow), run_time=0.4)
            self.play(*m.parts_in("chunking", "lab_chunking"), run_time=0.5)
            vo.wait_until("an embedding model turns")
            self.play(*m.parts_in("a_chunks", anim=GrowArrow), run_time=0.4)
            self.play(FadeIn(half), *m.parts_in("lab_embedding"), run_time=0.6)
            self.play(*m.parts_in("a_embed", anim=GrowArrow), run_time=0.4)
            self.play(*m.parts_in("vectors", "lab_vectors"), run_time=0.5)
            vo.wait_until("and the vectors go")
            self.play(*m.parts_in("a_vectors", anim=GrowArrow), run_time=0.5)
            self.play(pulse(db, DATA, 1.05), run_time=0.6)
            vo.wait_until("Below, the question")
            self.play(GrowArrow(straight), *m.parts_in("lab_question"), run_time=0.6)
            self.wait(0.45)                         # the A12 arrow, straight at the cylinder
            full_em = shown_copy(em)
            q_short = shown_copy(m.parts["a_question"])
            self.play(Transform(half, full_em), Transform(straight, q_short), run_time=0.8)
            self.remove(half, straight)
            m.parts_in("embedding", "a_question")
            self.play(FadeIn(hl), run_time=0.3)
            self.play(ShowPassingFlash(flash, time_width=0.6), FadeOut(hl), run_time=0.6)
            vo.wait_until("and only its vector")
            self.play(*m.parts_in("a_query", anim=GrowArrow), run_time=0.4)
            self.play(*m.parts_in("query", anim=lambda q: GrowFromPoint(q, np.array([em_r, YB, 0]))),
                      *m.parts_in("lab_query"), run_time=0.5)
            self.play(*m.parts_in("a_qdb", anim=GrowArrow), run_time=0.4)
            self.play(FadeIn(nums, shift=UP * 0.1), Create(nums_link), run_time=0.6)

        # ========================================================== 2. B5's three phases
        back_y = -2.65
        ans = m.parts["answer"]
        u_lab_m = m.parts["lab_user"]
        ret = elbow([[X["answer"], ans.get_bottom()[1] - 0.02, 0], [X["answer"], back_y, 0],
                     [X["user"], back_y, 0], [X["user"], u_lab_m.get_bottom()[1] - 0.06, 0]], CLOUD)

        with self.voiceover(SAY[2]) as vo:
            lr5 = lref("B5–B6")
            self.play(Succession(FadeOut(lr), FadeIn(lr5)), FadeOut(nums), FadeOut(nums_link), run_time=0.6)
            lr = lr5
            self.play(LaggedStart(*m.parts_in("a_context", anim=GrowArrow), *m.parts_in("prompt"),
                                  *m.parts_in("a_prompt", anim=GrowArrow), *m.parts_in("a_answer", anim=GrowArrow),
                                  *m.parts_in("answer"), lag_ratio=0.6), run_time=1.8)
            self.play(Create(ret, lag_ratio=1), run_time=0.9)
            vo.wait_until("Indexing is the whole")
            self.play(FadeOut(bands), *m.parts_in("reg_indexing", "tab_indexing"), run_time=0.7)
            vo.wait_until("Retrieval brings the context")
            self.play(*m.parts_in("reg_retrieval", "tab_retrieval"), run_time=0.7)
            ac = m.parts["a_context"]                   # "brings the context to the prompt"
            self.play(ShowPassingFlash(Line(ac.get_start(), ac.get_end()).set_stroke(TURN, 8), time_width=0.6),
                      pulse(m.parts["prompt"], TURN, 1.06), run_time=0.8)
            vo.wait_until("and the model does")
            self.play(*m.parts_in("reg_generation", "tab_generation"), run_time=0.7)

        # ========================================================== 3. the README's steps and flags
        src = note("README.md · lines 17–21").move_to([-4.9, -0.3, 0])
        flag_box = [("flag_chunk", "chunking"), ("flag_embed", "embedding"), ("flag_load", "database"),
                    ("flag_query", "query"), ("flag_chat", "llm")]

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(lr), FadeOut(ret), *m.parts_out(*RagMap.TABS),
                      *[m.parts[r].animate.set_stroke(opacity=0.3) for r in RagMap.REGIONS], run_time=0.7)
            self.play(*m.parts_in("lane1", anim=lambda c: FadeIn(c, shift=DOWN * 0.2)), run_time=0.7)
            self.wait(0.6)
            self.play(*m.parts_in("lane2", anim=lambda c: FadeIn(c, shift=UP * 0.2)), run_time=0.7)
            vo.wait_until("and gives each box")
            self.play(FadeIn(src), run_time=0.5)
            for i, (fl, bx) in enumerate(flag_box):
                if i == 0:
                    vo.wait_until("chunk, embed and load")
                if i == 3:
                    vo.wait_until("query and chat below")
                self.play(*m.parts_in(fl, anim=lambda c: FadeIn(c, shift=DOWN * 0.2)),
                          pulse(m.parts[bx]), run_time=0.55)

        # ========================================================== 4. two rules
        once = grey_tag("once · offline · slow").move_to([-4.6, YT - 0.88, 0])
        every = grey_tag("every question").move_to([-3.75, YB - 0.52, 0])
        rule = card([sans("same model · same 256 numbers · both lanes", 22, INK),
                     sans("chunks before, questions later", 20, S.GREY)], TURN)
        rule.move_to([-1.75, 2.76, 0])                 # clear of the top labels (y ≤ 2.05)
        # the "what if" inset, right of the top lane's end: another model puts the question where
        # no chunk is
        wf = box(3.45, 2.45, ERR, dashed=True, stroke=3).move_to([4.825, 1.72, 0])
        wt = tag("what if", ERR).move_to(wf.get_corner(UP + LEFT) + RIGHT * 0.75)
        wi = illustration_tag().move_to(wf.get_corner(DOWN + LEFT) + RIGHT * 1.0)
        other = model_box("another\nmodel", 1.0, 0.7).move_to([3.86, 1.72, 0])
        ring_ = Circle(radius=0.74)
        space = DashedVMobject(ring_, num_dashes=30, dashed_ratio=0.5).set_stroke(S.GREY, 2)
        space.move_to([5.72, 1.72, 0])
        o = space.get_center()
        feed = arrow(other.get_right() + RIGHT * 0.06, space.get_left() + LEFT * 0.06, LOOKUP)
        chunks = vec_glyph(3, DATA, 0.6, spread=34, base=128, stroke=4)
        chunks.shift(o - chunks[1].get_start())
        c_lab = sans("chunks", 20, DATA).move_to(o + np.array([-0.66, 0.98, 0]))
        d = np.array([np.cos(np.radians(-38)), np.sin(np.radians(-38)), 0])
        q_off = arrow(o, o + 0.6 * d, LOOKUP, stroke=4, tip=0.16)
        x_off = cross_mark(0.22, ERR).move_to(o + 0.84 * d)
        q_lab = sans("question", 20, LOOKUP).move_to(o + np.array([0.08, -0.98, 0]))
        o_dot = Dot(o, radius=0.04, color=S.GREY)
        inset = VGroup(wf, wt, wi, other, feed, space, o_dot, chunks, c_lab, q_off, q_lab, x_off)

        with self.voiceover(SAY[4]) as vo:
            self.play(*m.parts_out("lane1", "lane2", *RagMap.FLAGS, *RagMap.REGIONS), FadeOut(src), run_time=0.7)
            vo.wait_until("The top lane runs once")
            self.play(FadeIn(once, shift=RIGHT * 0.15), run_time=0.4)
            self.play(m.pulse_lane("top", TURN, run_time=2.4))
            vo.wait_until("The bottom lane runs")
            self.play(FadeIn(every, shift=RIGHT * 0.15), run_time=0.4)
            for _ in range(3):
                self.play(m.pulse_lane("bottom", TURN, run_time=0.65))
            vo.wait_until("And both lanes must")
            self.play(m.light("embedding"), FadeIn(rule.frame), Write(rule.rows[0]), run_time=1.1)
            self.play(FadeIn(rule.rows[1], shift=UP * 0.08), run_time=0.6)
            vo.wait_until("or the question and the chunks")
            self.play(Create(wf), FadeIn(wt), FadeIn(wi), FadeIn(other), run_time=0.6)
            self.play(Create(space), FadeIn(o_dot), FadeIn(chunks), FadeIn(c_lab), run_time=0.6)
            self.play(GrowArrow(feed), run_time=0.35)
            self.play(GrowArrow(q_off), FadeIn(q_lab), run_time=0.5)
            self.play(Create(x_off), run_time=0.4)

        # ========================================================== 5. where each box runs
        no_net = grey_tag("no network needed").move_to([X["chunking"], 2.82, 0])
        pay = cost_tag("pay per use · your key").move_to([X["embedding"], -2.56, 0])
        no_vm = note("no VM, no bucket: nothing keeps running").move_to([X["embedding"], -3.12, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(once, every, rule, inset)), m.unlight("embedding"),
                      *m.parts_out(*RagMap.LABELS), run_time=0.7)
            vo.wait_until("The chunker runs")
            self.play(*m.parts_in("loc_cli", anim=draw), run_time=0.8)
            self.play(FadeIn(no_net, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Both models run")
            self.play(*m.parts_in("loc_google", anim=draw), run_time=0.9)
            vo.wait_until("you pay for")
            self.play(FadeIn(pay, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and nothing keeps")
            self.play(FadeIn(no_vm), run_time=0.5)
            vo.wait_until("The database runs")
            self.play(*m.parts_in("loc_chroma", anim=draw), run_time=0.8)
            vo.wait_until("with its files")
            self.play(*m.parts_in("loc_disk", anim=draw), run_time=0.7)

        # ========================================================== 6. one python cli.py command per step
        cf = m.parts["loc_cli"].copy()
        big = box(7.0, 3.7, CTR, dashed=True, stroke=3).move_to([0, -0.2, 0])
        big_t = tag("CLI container", CTR).move_to(big.get_top())
        lines = VGroup(*[mono(f"python cli.py {f} …", 24, S.GREY, t2c={f"{f} …": INK})
                         for f in FLAGS]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        lines.move_to(big).shift(DOWN * 0.1)

        with self.voiceover(SAY[6]) as vo:
            self.add(cf)
            self.play(FadeOut(m), FadeOut(VGroup(no_net, pay, no_vm)), run_time=0.6)
            self.play(Transform(cf, VGroup(big, big_t)), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in lines], lag_ratio=0.35), run_time=1.5)
            vo.wait_until("inside that first container")
            self.play(cf[0].animate(rate_func=there_and_back).set_stroke(TURN, 5), run_time=0.9)
            vo.wait_until("let's get it running")
            self.play(FadeOut(cf), FadeOut(lines), run_time=0.8)
