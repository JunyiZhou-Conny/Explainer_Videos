"""S01 · A model that never read the book (cold open of AC215 L5). Lecture: A6–A11.

Beats (script.md "## S01", one voiceover block each):
0. Black frame, no tracker. A GREY chat box (browser frame, tag `illustration`) fades in centre,
   a cursor blinking in its empty field; the BLUE "LLM" box drops in above it as "a language model"
   is said. The README's sample question `How is tolminc cheese made?` (cli.py:318, PINK, with a
   GREY note "the README's sample question") types into the field, the cursor blinks, and the LLM
   box begins to answer: four gray placeholder bars stream out (no words).
1. The chat box shrinks to the upper left (the LLM box moves to the upper right). A shelf of eleven
   GREEN spines slides in along the bottom; ten carry a GREY "Project Gutenberg" label, the
   eleventh (thin: a short story) glows YELLOW and opens into CODE(Tolminc Cheese.txt: 3–4),
   line 4 underlined YELLOW. A GREY chip "11 books · input-datasets/books". The LLM box gets a GREY
   calendar glyph and "trained before this story"; the gray answer bars turn RED-edged. On the last
   sentence the panel folds back into its book and a large YELLOW "?" hangs in the gap between the
   glowing book and the LLM box (it stays, small, top left, until the map of beat 4).
2. LECTURE A6–A7. The shelf slides away (the chat box and the LLM box go with it); the "?" shrinks
   to the top-left corner. Four chips write in a row as named: "stale training data", "no
   specialized knowledge", "hallucination", "no sources". A YELLOW bracket closes over the first
   two, labelled "RAG fixes these"; the other two dim.
3. LECTURE A8–A10. The chips shrink to the top. Three roads run from a pile of GREEN books (left)
   to the BLUE LLM box (right), drawn one at a time as named. Road 1: every page pours into the
   prompt, which overflows; a RED cross and "garbage". Road 2: GREY dashed, a slow clock glyph, a
   tag "fine-tuning · lecture 8". Road 3 (the lecture tag stays; beat 4 hands it over to A11): a
   librarian glyph picks ten pages (GREEN cards) from the pile and hands them over; a YELLOW tag
   "open-book exam · our image";
   "That's RAG" lights road 3.
4. LECTURE A11. The roads fade. A crowded GREY sketch of boxes and arrows fills the frame, blurred
   (our redrawing of the lecture's map of RAG techniques, no labels; tag "illustration · our
   redrawing"); it dims, and four YELLOW questions write in over it, each with a short arrow into
   the blur: "What is an embedding?", "a vector database?", "a query?", "the context?".
5. A GREY file row `llm-rag/README.md` "beside this video" turns into the ReadmeTracker. Layout
   preview in three steps, each clearing the last: the tracker ("README › Run Container", 3 dots),
   a YELLOW pointer on its step while the lit dot pulses (the tracker sits at the safe-frame corner,
   so a ring around it would touch its text); the pointer swings to the GREY tag "Lecture 5 · slides
   A16–A19" with the caption "A = main deck · B = supplement"; a 3-row terminal strip (GREY tag
   "preview"):
   `sh docker-shell.sh` + ▶ your turn, then `docker ps` + extra. Then the caption "every command:
   MLOps_Learning · guides/L05-rag.md".
6. A card "Recorded October 16, 2026": "Docker, chunking, Chroma: real runs" (GREEN check),
   "embeddings: the staff's recorded vectors" (tag recorded), "Google calls: the command, the real
   no-key error, what to look for" (GREY key glyph crossed out); under it a GREY chip "Linux laptop ·
   Docker Engine 29.8.2 · Compose v5.6.0" (laptop/00 lines 3–5) with "at the time of recording".
   The three parts of the Google row light YELLOW as named. Everything fades to an empty frame.
"""

import numpy as np
from common import (
    CLOUD,
    DATA,
    ERR,
    INK,
    LAPTOP,
    LOOKUP,
    NARRATION,
    P_REPO,
    QUESTION,
    STORY_PATH,
    TURN,
    beside,
    calendar_glyph,
    capture,
    chunk_card,
    clock_glyph,
    excerpt,
    extra_tag,
    file_row,
    grey_tag,
    illustration_tag,
    key_glyph,
    lref,
    model_box,
    note,
    person,
    pin,
    recorded_tag,
    recording_tag,
    source_text,
    src_panel,
    term,
    tracker,
    type_cmd,
    under,
    your_turn,
)
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    ArcBetweenPoints,
    Arrow,
    Circle,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    FadeTransform,
    Group,
    GrowArrow,
    GrowFromEdge,
    GrowFromPoint,
    Indicate,
    LaggedStart,
    Line,
    ManimColor,
    Rectangle,
    Rotate,
    RoundedRectangle,
    ShowIncreasingSubsets,
    ShowPassingFlash,
    Succession,
    Transform,
    VGroup,
    VMobject,
    Write,
    linear,
    there_and_back,
)

from explainer import style as S
from explainer.devops import (
    TERM_BG,
    box,
    browser_window,
    check_mark,
    chip,
    cross_mark,
    label,
    mono,
    tag,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources
ENV = capture("00", "laptop")                       # 00-x-env.txt (extra): date and versions
assert ENV.line(2).startswith("2026-10-16"), ENV.line(2)
assert ENV.line(3) == "Linux x86_64", ENV.line(3)
assert "engine 29.8.2" in ENV.line(4), ENV.line(4)
assert ENV.line(5) == "Docker Compose version v5.6.0", ENV.line(5)
RUN = capture("07", "laptop")                       # 07-docker-shell.txt: the README's command
assert RUN.cmd == "sh docker-shell.sh", RUN.cmd
PS = capture("08", "laptop")                        # 08-x-docker-ps.txt (extra)
assert PS.cmd == "docker ps", PS.cmd
assert "How is tolminc cheese made?" in source_text("cli.py").split("\n")[317], "cli.py:318"
LINE4 = excerpt(STORY_PATH, 4, 4)
assert LINE4 == "*A fictional tale inspired by Alpine cheesemaking*", LINE4

GUIDE = "MLOps_Learning · guides/L05-rag.md"
WEAK = ["stale training data", "no specialized knowledge", "hallucination", "no sources"]
QUESTIONS = ["What is an embedding?", "a vector database?", "a query?", "the context?"]
ROWS6 = ["Docker, chunking, Chroma: real runs", "embeddings: the staff's recorded vectors",
         "Google calls: the command, the real no-key error, what to look for"]


# ------------------------------------------------------------------ small helpers
def clear_stage(scene, *anims, run_time: float = 0.6):
    """Fade out everything on screen (together with `anims`), then drop it from the scene."""
    old = list(scene.mobjects)
    if old:
        scene.play(FadeOut(Group(*old)), *anims, run_time=run_time)
        scene.remove(*old)
    elif anims:
        scene.play(*anims, run_time=run_time)


def mix(color, k: float) -> ManimColor:
    """An opaque colour k of the way from the background to `color`."""
    return ManimColor(S.BG).interpolate(ManimColor(color), k)


def pulse(m, color: str = TURN, k: float = 1.08):
    """A there-and-back emphasis for shapes: strokes take `color`, the shape grows a little."""
    return m.animate(rate_func=there_and_back).scale(k).set_stroke(color)


def chat_box(url: str, width: float, height: float, size: float) -> VGroup:
    """A schematic chat page (common.chat_window with a bigger address font, so the scene can
    shrink it to 80 % and keep 20 pt): .frame .address .field .answer"""
    w = browser_window(url, width=width, height=height, size=size)
    c = w.content
    field = RoundedRectangle(width=c.width - 0.6, height=0.62, corner_radius=0.14,
                             stroke_color=S.GREY, stroke_width=2).set_fill(TERM_BG, 1)
    field.move_to(c.get_bottom() + UP * 0.5)
    ans = Rectangle(width=c.width - 0.6, height=c.height - 1.25, stroke_width=0, fill_opacity=0)
    ans.next_to(field, UP, buff=0.18)
    w.add(field, ans)
    w.field, w.answer = field, ans
    return w


def stream_bars(width: float, n: int = 4, h: float = 0.14) -> VGroup:
    """The LLM's answer: n gray placeholder bars (no words), the last one shorter."""
    ws = [1.0, 0.9, 0.96, 0.55][:n]
    bars = VGroup(*[RoundedRectangle(width=width * k, height=h, corner_radius=h / 2, stroke_width=0)
                    .set_fill(S.GREY, 0.8) for k in ws])
    return bars.arrange(DOWN, aligned_edge=LEFT, buff=h * 1.05)


def spine(w: float, h: float, words=None) -> VGroup:
    """A GREEN book spine standing on y=0 (bottom edge), two bands; `words` (lines) written up the
    spine in GREY. .frame .words"""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color=DATA,
                          stroke_width=2.5).set_fill(mix(DATA, 0.14), 1)
    bands = VGroup(*[Line(LEFT * w * 0.36, RIGHT * w * 0.36, color=DATA, stroke_width=2,
                          stroke_opacity=0.7).move_to(fr.get_center() + UP * y)
                     for y in (h / 2 - 0.13, -h / 2 + 0.13)])
    g = VGroup(fr, bands)
    g.frame, g.words = fr, None
    if words:
        t = VGroup(*[label(s, 20, S.GREY) for s in words]).arrange(DOWN, buff=0.04)
        t.rotate(PI / 2).move_to(fr)
        g.add(t)
        g.words = t
    g.shift(UP * h / 2)
    return g


def glow_of(m, color: str = TURN) -> VGroup:
    """A soft glow around a shape: wide translucent strokes."""
    return VGroup(*[m.copy().set_fill(opacity=0).set_stroke(color, w, opacity=o)
                    for w, o in ((22, 0.08), (13, 0.14), (7, 0.25))])


def arc_road(a, b, sag: float, color: str = S.GREY, stroke: float = 4) -> VMobject:
    """An arc from a to b bulging by `sag` (positive: up)."""
    chord = np.linalg.norm(np.array(b) - np.array(a))
    r = (chord ** 2 / 4 + sag ** 2) / (2 * abs(sag))
    ang = 2 * np.arcsin(chord / (2 * r))
    return ArcBetweenPoints(np.array(a), np.array(b), angle=-ang if sag > 0 else ang,
                            stroke_color=color, stroke_width=stroke)


def book_pile() -> VGroup:
    """A pile of GREEN books (lying flat), 1.6 wide."""
    books = VGroup()
    specs = [(1.5, 0.0), (1.35, 0.08), (1.55, -0.05), (1.3, 0.1), (1.45, -0.02)]
    for k, (w, dx) in enumerate(specs):
        b = RoundedRectangle(width=w, height=0.24, corner_radius=0.05, stroke_color=DATA,
                             stroke_width=2.5).set_fill(mix(DATA, 0.18), 1)
        b.move_to([dx, k * 0.27, 0])
        books.add(b)
    return books


def blur_map() -> VGroup:
    """Our blurred redrawing of a crowded map of RAG techniques: GREY boxes, nodes and arrows in a
    soft halo, scribbles instead of labels (nothing legible). Seeded."""
    rng = np.random.default_rng(11)
    halo, core = VGroup(), VGroup()

    def soft(m, fill: float = 0.05):
        m.set_fill(S.GREY, fill)
        for w, o in ((18, 0.05), (9, 0.08)):                     # the blur: wide faint strokes
            halo.add(m.copy().set_fill(opacity=0).set_stroke(S.GREY, w, opacity=o))
        ghost = m.copy().set_fill(opacity=0).set_stroke(S.GREY, 1.6, opacity=0.22)
        halo.add(ghost.shift(np.array([0.04, -0.03, 0])))          # a double image
        c = m.set_stroke(S.GREY, 1.6, opacity=0.42)
        core.add(c)
        return c

    def scribble(cx, cy, w):
        for k in range(rng.integers(1, 3)):
            ln = Line([cx - w * 0.35, cy + 0.07 - k * 0.14, 0],
                      [cx - w * 0.35 + w * rng.uniform(0.35, 0.7), cy + 0.07 - k * 0.14, 0])
            soft(ln.set_stroke(width=3))

    # the centre row: question, two hops, three stores, documents, a funnel, a brain, the answer
    xs = [-5.6, -4.6, -4.0, -2.7, -1.2, 0.2, 1.6, 3.0, 4.4, 5.6]
    nodes = []
    q = soft(RoundedRectangle(width=0.9, height=0.45, corner_radius=0.1).move_to([xs[0], 0, 0]))
    scribble(xs[0], 0, 0.9)
    nodes.append(q)
    for x in xs[1:3]:
        nodes.append(soft(Circle(radius=0.2).move_to([x, 0, 0])))
    stores = VGroup(*[soft(RoundedRectangle(width=0.8, height=0.36, corner_radius=0.16)
                           .move_to([xs[3], y, 0])) for y in (0.55, 0, -0.55)])
    nodes.append(stores)
    for x in xs[4:9]:
        b = soft(RoundedRectangle(width=0.85, height=0.55, corner_radius=0.12).move_to([x, 0, 0]))
        scribble(x, 0, 0.85)
        nodes.append(b)
    nodes.append(soft(RoundedRectangle(width=0.8, height=0.45, corner_radius=0.1).move_to([xs[9], 0, 0])))
    for a, b in zip(nodes[:-1], nodes[1:]):
        p0, p1 = a.get_right() + RIGHT * 0.05, b.get_left() + LEFT * 0.05
        if p1[0] - p0[0] > 0.15:
            soft(Arrow(p0, p1, buff=0, stroke_width=2.5, tip_length=0.12))
    # six regions around the row, each crowded with small labelled-looking boxes
    regions = [(-4.3, 1.75), (-0.2, 1.85), (3.9, 1.75), (-4.1, -1.8), (0.1, -1.85), (4.0, -1.8)]
    for cx, cy in regions:
        w, h = rng.uniform(3.4, 3.9), rng.uniform(1.3, 1.6)
        soft(RoundedRectangle(width=w, height=h, corner_radius=0.18).move_to([cx, cy, 0]), 0.03)
        cols = 3
        for i in range(rng.integers(4, 7)):
            bx = cx - w / 2 + 0.25 + (i % cols + 0.5) * (w - 0.5) / cols + rng.uniform(-0.1, 0.1)
            by = cy + (0.3 if i < cols else -0.3) + rng.uniform(-0.08, 0.08)
            bw = (w - 0.5) / cols - 0.15
            soft(RoundedRectangle(width=bw, height=0.42, corner_radius=0.08).move_to([bx, by, 0]))
            scribble(bx, by, bw)
        # one or two arrows from the region to the row
        for k in range(rng.integers(1, 3)):
            x0 = cx + rng.uniform(-1.2, 1.2)
            y0 = cy - np.sign(cy) * h / 2
            y1 = np.sign(cy) * 0.45
            soft(Arrow([x0, y0, 0], [x0 + rng.uniform(-0.6, 0.6), y1, 0], buff=0.05, stroke_width=2.5,
                       tip_length=0.12))
    g = VGroup(halo, core)
    g.nodes = nodes
    return g


# ------------------------------------------------------------------ the scene
class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0. the question
        win = chat_box("a chat with an LLM", 7.0, 3.0, 25).move_to([0, -0.6, 0])
        q = mono(QUESTION, 25, LOOKUP)
        q.move_to(win.field).align_to(win.field, LEFT).shift(RIGHT * 0.22)
        cur = Rectangle(width=0.04, height=0.36, stroke_width=0).set_fill(INK, 1)
        cur.move_to(q.get_left() + RIGHT * 0.02)              # waiting in the empty field
        bars = stream_bars(win.answer.width - 0.2).move_to(win.answer).align_to(win.answer, LEFT) \
            .shift(RIGHT * 0.1)
        llm = model_box("LLM", 1.7, 1.0, size=26).move_to([0, 2.6, 0])
        feed = Arrow(llm.get_bottom(), win.frame.get_top(), buff=0.08, color=CLOUD, stroke_width=5,
                     max_tip_length_to_length_ratio=0.25)
        ill = illustration_tag().next_to(win.frame, UP, buff=0.12).align_to(win.frame, RIGHT)
        sample = note("the README's sample question").next_to(win.frame, DOWN, buff=0.2)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(win), FadeIn(ill), run_time=0.8)
            self.add(cur)
            for _ in range(2):
                self.play(cur.animate.set_opacity(0), run_time=0.2)
                self.play(cur.animate.set_opacity(1), run_time=0.2)
            vo.wait_until("asks a language model")
            self.play(FadeIn(llm, shift=DOWN * 0.3), run_time=0.6)
            vo.wait_until("how is Tolminc")
            self.remove(cur)
            self.play(ShowIncreasingSubsets(q, rate_func=linear), run_time=1.3)
            cur.next_to(q, RIGHT, buff=0.07)
            self.add(cur)
            self.play(FadeIn(sample, shift=UP * 0.1), run_time=0.4)
            for _ in range(2):
                self.play(cur.animate.set_opacity(0), run_time=0.2)
                self.play(cur.animate.set_opacity(1), run_time=0.2)
            vo.wait_until("Tolminc is a real")
            self.play(Indicate(llm.frame, color=CLOUD, scale_factor=1.08), GrowArrow(feed), run_time=0.7)
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.9,
                                  rate_func=linear), run_time=3.6)
            vo.wait_until("lives in one particular")
            self.play(FadeOut(cur), run_time=0.4)
        self.remove(cur)

        # ========================================================== 1. eleven books, one story
        chat = VGroup(win, q, bars)
        k = 0.8
        c_end = np.array([-6.45 + win.frame.width * k / 2, 3.45 - win.frame.height * k / 2, 0])
        c_now = win.frame.get_center()
        llm_to = np.array([4.75, 2.85, 0])
        # the shelf: ten Gutenberg spines and the thin eleventh (the short story)
        heights = [1.85, 1.7, 1.95, 1.78, 1.9, 1.65, 1.88, 1.75, 1.92, 1.8]
        books = VGroup(*[spine(0.7, h, ("Project", "Gutenberg")) for h in heights])
        story = spine(0.4, 1.55)
        row = VGroup(*books, story).arrange(RIGHT, buff=0.07, aligned_edge=DOWN)
        row.shift(np.array([-6.3 - row.get_left()[0], -3.27 - row.get_bottom()[1], 0]))
        board = Line([-6.45, -3.3, 0], [row.get_right()[0] + 0.15, -3.3, 0], color=LAPTOP, stroke_width=5)
        words = VGroup(*[b.words for b in books])
        shelf = VGroup(board, row)
        glow = glow_of(story.frame)
        kb = VGroup(label("11 books", 22, INK), mono("input-datasets/books", 20, S.GREY)) \
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        kb_box = box(kb.width + 0.5, kb.height + 0.36, S.GREY, fill_opacity=0.1, radius=0.14).move_to(kb)
        kb_chip = VGroup(kb_box, kb)
        kb_chip.move_to([(board.get_right()[0] + 6.5) / 2 + 0.05, -2.45, 0])
        assert kb_chip.get_left()[0] > board.get_right()[0] + 0.1, kb_chip.get_left()
        panel = src_panel(STORY_PATH, 3, 4).move_to([0, 0.05, 0])
        ul = under(panel.span(4, LINE4), TURN)
        cal = calendar_glyph(0.5).next_to(llm_to + LEFT * llm.width / 2, LEFT, buff=0.3)
        before = note("trained before this story")
        before.move_to([llm_to[0] - 0.35, llm_to[1] - llm.height / 2 - 0.35, 0])
        qmark = label("?", 96, TURN)

        with self.voiceover(SAY[1]) as vo:
            self.play(chat.animate.scale(k, about_point=c_now).shift(c_end - c_now),
                      llm.animate.move_to(llm_to),
                      ill.animate.next_to(np.array([c_end[0] + win.frame.width * k / 2, 3.45, 0]),
                                          RIGHT, buff=0.25).shift(DOWN * 0.2),
                      FadeOut(feed), FadeOut(sample), run_time=0.9)
            self.remove(feed, sample)
            for b in books:
                b.remove(b.words)
            self.play(FadeIn(shelf, shift=RIGHT * 1.2), run_time=0.9)
            vo.wait_until("eleven books")
            self.play(FadeIn(kb_chip, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("ten old cheese books")
            self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.1) for w in words], lag_ratio=0.12),
                      run_time=1.2)
            vo.wait_until("and the instructor's")
            self.play(FadeIn(glow), story.frame.animate.set_stroke(TURN, 3.5), run_time=0.5)
            self.play(GrowFromPoint(panel, story.get_top()), run_time=0.8)
            vo.wait_until("a fictional tale")
            self.play(Create(ul), run_time=0.5)
            vo.wait_until("A model trained before")
            self.play(FadeIn(cal, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("has never read it")
            self.play(FadeIn(before, shift=UP * 0.1), Indicate(cal, color=S.GREY, scale_factor=1.2),
                      run_time=0.7)
            vo.wait_until("so it answers from")
            self.play(bars.animate.set_stroke(ERR, 1.6, opacity=1), run_time=0.7)
            gap_a = story.get_top() + UP * 0.2
            gap_b = before.get_bottom() + DOWN * 0.15
            qmark.move_to((gap_a + gap_b) / 2)
            vo.wait_until("How do we make it")
            self.play(FadeOut(VGroup(panel, ul), target_position=story.get_top(), scale=0.1), run_time=0.5)
            self.remove(panel, ul)
            self.play(Write(qmark), run_time=0.6)
            self.play(qmark.animate(rate_func=there_and_back).scale(1.25), run_time=0.7)

        # ========================================================== 2. four weaknesses
        lr = lref("A6–A7")
        chips = VGroup(*[chip(s, ERR, size=24) for s in WEAK]).arrange(RIGHT, buff=0.3).move_to([0, 0.1, 0])
        assert chips.width < 13.0, chips.width
        x0, x1 = chips[0].get_left()[0], chips[1].get_right()[0]
        yb = chips.get_top()[1] + 0.12
        brk = VMobject(stroke_color=TURN, stroke_width=4).set_points_as_corners(
            [[x0, yb, 0], [x0, yb + 0.22, 0], [x1, yb + 0.22, 0], [x1, yb, 0]])
        fixes = label("RAG fixes these", 24, TURN).next_to(brk, UP, buff=0.12)
        q_corner = np.array([-6.2, 3.1, 0])
        anchors = ["stale training data", "no specialized knowledge", "hallucination", "and no sources"]

        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(chat, llm, cal, before, ill, kb_chip)
            self.play(FadeOut(VGroup(shelf, glow, words), shift=LEFT * 2.5), FadeOut(gone),
                      qmark.animate.scale(0.45).move_to(q_corner), FadeIn(lr), run_time=0.9)
            self.remove(shelf, glow, words, gone)
            for c, a in zip(chips, anchors):
                vo.wait_until(a)
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("RAG, retrieval")
            self.play(Create(brk), Write(fixes), run_time=0.8)
            vo.wait_until("goes after the first two")
            self.play(chips[2:].animate.set_opacity(0.3), pulse(VGroup(chips[0].box, chips[1].box), TURN, 1.05),
                      run_time=0.8)

        # ========================================================== 3. three roads
        top_grp = VGroup(chips, brk, fixes)
        ks = 20 / 24
        pile = book_pile().move_to([-5.3, -0.5, 0])
        pile_l = note("11 books").next_to(pile, DOWN, buff=0.18)
        llm3 = model_box("LLM", 1.5, 1.0, size=24).move_to([5.3, -0.5, 0])
        a_pt, b_pt = np.array([-4.35, -0.5, 0]), np.array([4.45, -0.5, 0])
        road1 = arc_road(a_pt, b_pt, 2.0)
        road2 = DashedLine(a_pt, b_pt, color=S.GREY, stroke_width=4, dash_length=0.16)
        road3 = arc_road(a_pt, b_pt, -2.0)
        apex1, apex3 = road1.point_from_proportion(0.5), road3.point_from_proportion(0.5)
        prompt = box(2.3, 0.8, DATA, fill=mix(DATA, 0.08), fill_opacity=1, radius=0.12).move_to(apex1)
        prompt_l = note("prompt", INK).next_to(prompt, DOWN, buff=0.12)
        rng = np.random.default_rng(3)
        pages, spots = VGroup(), []
        pc = prompt.get_center()
        for i in range(14):                      # first the prompt fills up, two neat rows of pages
            spots.append((pc + np.array([(i % 7 - 3) * 0.3, 0.17 - (i // 7) * 0.34, 0]), 0.0))
        for i in range(12):                      # then it overflows: pages pile over the top edge
            x = rng.uniform(-1.05, 1.05)
            spots.append((pc + np.array([x, rng.uniform(0.42, 0.6), 0]), rng.uniform(-0.45, 0.45)))
        spots += [(pc + np.array([-1.32, -0.12, 0]), 0.6), (pc + np.array([1.34, -0.2, 0]), -0.5)]
        for _ in spots:
            p = Rectangle(width=0.24, height=0.3, stroke_color=DATA, stroke_width=2) \
                .set_fill(mix(DATA, 0.4), 1).move_to(pile.get_top() + DOWN * 0.1).set_opacity(0)
            pages.add(p)
        cross = cross_mark(0.42, ERR, stroke=6).move_to(road1.point_from_proportion(0.75))
        garbage = label("garbage", 26, ERR).next_to(cross, RIGHT, buff=0.2).shift(UP * 0.12)
        clock_bg = Circle(radius=0.36, stroke_width=0).set_fill(S.BG, 1)
        clock = clock_glyph(0.34, S.GREY).move_to([0, -0.5, 0])
        clock_bg.move_to(clock)
        ft = grey_tag("fine-tuning · lecture 8").next_to(clock, DOWN, buff=0.22)
        lib = person(S.GREY, 0.7).move_to(apex3 + UP * 0.42)
        fan_at = lib.get_right() + RIGHT * 0.45 + DOWN * 0.05
        cards, fan, dest = VGroup(), [], []
        for i in range(10):
            c = chunk_card(0.42, 0.28).move_to(pile.get_top() + DOWN * 0.1).set_opacity(0)
            cards.add(c)
            fan.append(fan_at + np.array([0.035 * i, 0.025 * i, 0]))
            # under the LLM box: two neat rows of five, so the ten pages can be counted
            dest.append(llm3.get_bottom() + np.array([(i % 5 - 2) * 0.41, -0.27 - (i // 5) * 0.29, 0]))
        exam = tag("open-book exam · our image", TURN).move_to([2.3, -3.12, 0])

        with self.voiceover(SAY[3]) as vo:
            tgt = top_grp.copy().scale(ks)
            tgt.move_to([-0.25, 3.48 - tgt.height / 2, 0])
            lr_new = lref("A8–A10")
            # the tag swaps in turn (old out, then new in): faded at once, the two texts overlapped
            self.play(Succession(FadeOut(lr), FadeIn(lr_new)), top_grp.animate.scale(ks).move_to(tgt),
                      FadeIn(pile), FadeIn(pile_l), FadeIn(llm3), run_time=0.8)
            self.remove(lr)
            lr = lr_new
            self.play(Create(road1), FadeIn(prompt), FadeIn(prompt_l), run_time=0.5)
            self.add(pages)
            self.play(LaggedStart(*[p.animate(path_arc=-1.0).move_to(s).rotate(r).set_opacity(1)
                                    for p, (s, r) in zip(pages, spots)], lag_ratio=0.1), run_time=1.3)
            vo.wait_until("and you get garbage")
            self.play(prompt.animate.set_stroke(ERR), road1.animate.set_stroke(ERR, opacity=0.6),
                      Create(cross), FadeIn(garbage, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("Fine-tune the model")
            self.play(Create(road2), FadeIn(clock_bg), FadeIn(clock), run_time=0.6)
            self.play(Rotate(clock[1], angle=-2 * PI, about_point=clock[0].get_center(), rate_func=linear),
                      run_time=1.8)
            vo.wait_until("that's lecture 8")
            self.play(FadeIn(ft, shift=UP * 0.1),
                      Rotate(clock[1], angle=-PI, about_point=clock[0].get_center(), rate_func=linear),
                      run_time=0.9)
            vo.wait_until("Or let a librarian")
            # the A8–A10 tag stays while road 3 (A10: RAG) is drawn; beat 4's clear_stage takes it
            # out before the A11 tag fades in
            self.play(Create(road3), run_time=0.6)
            self.play(FadeIn(lib, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("hand it the ten")
            self.add(cards)
            self.play(LaggedStart(*[c.animate(path_arc=0.8).move_to(f).set_opacity(1)
                                    for c, f in zip(cards, fan)], lag_ratio=0.1), run_time=0.9)
            self.wait(0.3)
            self.play(LaggedStart(*[c.animate(path_arc=0.5).scale(0.85).move_to(d)
                                    for c, d in zip(cards, dest)], lag_ratio=0.06), run_time=0.9)
            vo.wait_until("an open-book exam")
            self.play(FadeIn(exam, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("That's RAG")
            flash = road3.copy().set_stroke(TURN, 7)
            self.play(road3.animate.set_stroke(TURN), ShowPassingFlash(flash, time_width=0.5),
                      pulse(llm3.frame, TURN, 1.06), run_time=0.9)

        # ========================================================== 4. the lecture's map, four questions
        mp = blur_map()
        assert mp.get_left()[0] > -6.6 and mp.get_right()[0] < 6.6 and mp.get_top()[1] < 3.1, mp.get_top()
        ill4 = illustration_tag("our redrawing").move_to([0, 0, 0])
        ill4.move_to([6.5 - ill4.width / 2, -3.32, 0])
        nd = mp.nodes
        targets = [nd[1].get_top() + UP * 0.08, nd[3].get_top() + UP * 0.08,
                   nd[0].get_bottom() + DOWN * 0.08, nd[4].get_bottom() + DOWN * 0.08]
        spots4 = [(-4.3, 1.98), (0.0, 1.98), (-4.9, -1.98), (0.45, -1.98)]
        qs, arrows = VGroup(), VGroup()
        for s, (x, y), t_pt in zip(QUESTIONS, spots4, targets):
            c = chip(s, TURN, size=26, text_color=TURN, fill_opacity=0.0)
            c.box.set_fill(S.BG, 0.95)
            c.move_to([x, y, 0])
            qs.add(c)
            start = c.get_bottom() if y > 0 else c.get_top()
            start = start + (UP if y < 0 else DOWN) * 0.05
            arrows.add(Arrow(start, t_pt, buff=0.04, color=TURN, stroke_width=5,
                             max_tip_length_to_length_ratio=0.3))
        lr = lref("A11")

        with self.voiceover(SAY[4]) as vo:
            clear_stage(self, run_time=0.6)
            self.play(FadeIn(lr), FadeIn(mp, lag_ratio=0.02), FadeIn(ill4), run_time=1.3)
            vo.wait_until("but it starts from")
            self.play(mp.animate.fade(0.5), run_time=0.6)
            for i, a in enumerate(["What is an embedding", "a vector database", "a query", "the context"]):
                vo.wait_until(a)
                self.play(FadeIn(qs[i], scale=0.9), GrowArrow(arrows[i]), run_time=0.5)
            vo.wait_until("This video answers")
            self.play(LaggedStart(*[q_.animate(rate_func=there_and_back).scale(1.1) for q_ in qs],
                                  lag_ratio=0.2), run_time=1.2)

        # ========================================================== 5. how to follow along
        tr = tracker("Run", 3)
        readme = VGroup(file_row("llm-rag/README.md", size=26), note("beside this video", size=24))
        readme.arrange(DOWN, buff=0.25).move_to([0, 0.4, 0])
        # a YELLOW pointer (the tracker sits at the safe-frame corner: no room for a ring around it);
        # it swings from the tracker's step to the lecture tag
        lr5 = lref("A16–A19")
        decks = note("A = main deck · B = supplement").next_to(lr5, DOWN, buff=0.15).align_to(lr5, RIGHT)
        aim = tr.caption.get_bottom() + DOWN * 0.17
        ptr = Arrow(aim + np.array([2.1, -1.35, 0]), aim, buff=0, color=TURN, stroke_width=6,
                    max_tip_length_to_length_ratio=0.18)
        aim_r = lr5.get_left() + LEFT * 0.1
        ptr_r = Arrow(aim_r + np.array([-2.5, -0.8, 0]), aim_r, buff=0, color=TURN, stroke_width=6,
                      max_tip_length_to_length_ratio=0.18)
        t5 = term(P_REPO, rows=3)
        prev = grey_tag("preview").next_to(t5.box, UP, buff=0.12).align_to(t5.box, RIGHT).shift(LEFT * 0.2)
        foot = VGroup(label("every command:", 24, S.GREY), mono(GUIDE, 22, S.GREY)).arrange(RIGHT, buff=0.25)
        foot.move_to([0, t5.box.get_top()[1] + 0.95, 0])

        with self.voiceover(SAY[5]) as vo:
            clear_stage(self, run_time=0.7)
            self.play(FadeIn(readme, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Top left, the tracker")
            self.play(FadeTransform(readme, tr), run_time=0.7)
            self.remove(readme)
            self.play(GrowArrow(ptr), run_time=0.5)
            lit = tr.dots[tr.k - 1]
            for _ in range(2):
                self.play(lit.animate(rate_func=there_and_back).scale(1.4),
                          ptr.animate(rate_func=there_and_back).shift((aim - ptr.get_start()) * 0.06),
                          run_time=0.5)
            vo.wait_until("top right, the gray tag")
            self.play(FadeOut(tr), Transform(ptr, ptr_r), FadeIn(lr5), run_time=0.6)
            self.remove(tr)
            self.play(FadeIn(decks, shift=DOWN * 0.1), run_time=0.5)
            self.play(lr5.box.animate(rate_func=there_and_back).set_stroke(TURN, 5), run_time=0.8)
            vo.wait_until("When the yellow")
            self.play(FadeOut(VGroup(lr5, decks, ptr)), FadeIn(t5), FadeIn(prev), run_time=0.5)
            self.remove(lr5, decks, ptr)
            ln = type_cmd(self, t5, RUN.cmd, type_time=0.8)
            yt = pin(self, ln, beside(your_turn(), t5, ln))
            vo.wait_until("pause and run")
            self.play(pulse(yt.box, TURN, 1.15), run_time=0.7)
            vo.wait_until("extra commands")
            ln2 = type_cmd(self, t5, PS.cmd, type_time=0.5)
            pin(self, ln2, beside(extra_tag(), t5, ln2))
        self.play(FadeIn(foot, shift=UP * 0.15), run_time=0.5)
        self.wait(1.5)

        # ========================================================== 6. what was recorded, and how
        head = label("Recorded October 16, 2026", 28, INK)
        rows = VGroup(*[label(s, 24, INK) for s in ROWS6]).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        body = VGroup(head, rows).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        rows.shift(RIGHT * 1.05)                               # a column for the icons
        card = box(body.width + 0.9, body.height + 0.8, S.GREY, fill_opacity=0.04).move_to(body)
        VGroup(card, body).move_to([0, 0.75, 0])
        assert card.get_left()[0] > -6.6 and card.get_right()[0] < 6.6, card.width
        icon_x = rows.get_left()[0] - 0.6
        tick = check_mark(0.36, DATA).move_to([icon_x, rows[0].get_center()[1], 0])
        rec = recorded_tag().next_to(rows[1], RIGHT, buff=0.3)
        assert rec.get_right()[0] < card.get_right()[0] - 0.1, rec.get_right()
        kg = key_glyph(0.36, S.GREY)
        kg.move_to([icon_x, rows[2].get_center()[1], 0])
        assert kg.get_right()[0] < rows[2].get_left()[0] - 0.15, kg.get_right()
        kx = cross_mark(0.46, S.GREY, stroke=5).move_to(kg)
        env = chip("Linux laptop · Docker Engine 29.8.2 · Compose v5.6.0", S.GREY, size=22)
        at_rec = recording_tag()
        envg = VGroup(env, at_rec).arrange(RIGHT, buff=0.3).next_to(card, DOWN, buff=0.45)
        whole = VGroup(card, body, tick, rec, kg, kx, envg)
        whole.shift(UP * (0.15 - whole.get_center()[1]))           # card and chip centred together
        assert len(rows[2]) == len("".join(ROWS6[2].split())), "one glyph per non-space character"

        def part(i: int, sub: str) -> VGroup:
            """The glyphs of `sub` in row i (Text glyphs skip spaces)."""
            s = ROWS6[i]
            a = len("".join(s[:s.index(sub)].split()))
            return VGroup(*rows[i].submobjects[a:a + len("".join(sub.split()))])

        looks = [part(2, s) for s in ("the command", "the real no-key error", "what to look for")]

        with self.voiceover(SAY[6]) as vo:
            clear_stage(self, run_time=0.5)
            self.play(FadeIn(card), FadeIn(head, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(env, shift=UP * 0.15), FadeIn(at_rec, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("Docker, chunking")
            self.play(Create(tick), FadeIn(rows[0], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("the embeddings are")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), FadeIn(rec, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Where the code calls")
            self.play(FadeIn(kg), Create(kx), FadeIn(rows[2], shift=RIGHT * 0.15), run_time=0.7)
            for lk, a in zip(looks, ["you see the command", "the real error", "and what to look for"]):
                vo.wait_until(a)
                self.play(Indicate(lk, color=TURN, scale_factor=1.06), run_time=0.7)

        clear_stage(self, run_time=0.8)
