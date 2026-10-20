"""S04 · A menu of two tools (llm-rag › Agents; lecture slides 8–14, then 39).

Beats (script.md "## S04", one voiceover block each):
0. LECTURE 8–14, no tracker yet. V3's first half (MenuColumn): L05's strip (slide 8) writes left
   to right, question → Retrieval → LLM → Response; two BLUE LLM boxes open slide 13's column and
   the six GREY dashed technique boxes (slides 9–12, our words) fly in from Retrieval as named.
1. "agentic RAG" (GREY) beside the first LLM, which gets the YELLOW label "chooses"; a YELLOW ring
   hops down the menu.
2. TRACKER Agents (no step lit). The column shrinks to llm-rag's two GREEN menu cards, "retrieval
   decision" stays behind dashed; the V1 mini-map comes in bottom right, Tools lit YELLOW. L05's
   strip gives way to the README chip `README.md · line 244 (excerpt)` "let the LLM decide how to
   retrieve" (tag `expected`); each card is ringed as the SAY names it.
3. The mini-map, the lecture tag and the column leave; the first card moves to where its
   declaration starts and fades into CODE(agent_tools.py: 9–19) (line 12 wrapped; every panel
   of the scene gets the full 12.9 width, so the notes on its lines sit inside it): line 10 GREEN + note "← the name the model writes back"; line 11 GREEN +
   note "↑ the model's documentation, with the parameter descriptions" (line 18 GREEN too;
   both bars pulse with the note at "the only documentation"); lines 13–15 bracketed, tag "JSON schema". Notes on code lines are plain text (a framed tag is taller
   than a code row).
4. Panel changes are scrolls (morph_panel: the frame resizes, rows that stay Transform, the
   others drift up and fade or rise into place). CODE(19–30), line 19 carried over: the nine
   names (line 28 masked) get a GREEN bracket "enum: only these 9"; the nine name rows fold into
   one "… 9 names …" row, the bracket and its tag with them; scroll to CODE(31–37): line 33
   (wrapped) YELLOW, its "a a" underlined with the GREY tag "erratum · typo in the source";
   line 36 GREEN.
5. CODE(41–49) (lines 41 and 47 wrapped): `collection, embed_func` underlined TEAL, each flashed
   as named, "your code supplies these"; `author, search_content` underlined GREEN "from the
   model", then line 47's `n_results=10, where={"author": author}` PINK; "and the search text"
   flashes line 43's `search_content` PINK. After the SAY the panel moves to CODE(78–81) at the
   bottom, note "one Tool, two declarations" (about 2 s without voice).
6. LECTURE 39. A GREY heading "a tool-using agent must", then three GREY dashed duty chips (slide
   39, our words) write in as named (CODE 78–81 stays at the bottom); the first two
   attach to a BLUE pen "the model writes", the third gets a GREY tag "call 2"; a TEAL gear "your
   code runs" turns beside the pen.
7. Two columns: the nine enum names (GREEN, masked) and the 11 book titles (GREY, cut out of the
   load step's `Processing file:` lines, capture order, long titles cut with "…"); no lines.
   PONDER 8 s: the lists collapse into a GREEN stack "9 author names" and a GREY stack of eleven
   book glyphs "11 books", the two GREEN menu cards above them; the card in the lower third.
8. The lists expand again for the answer, the books now in the enum's order (cli.py:61-71 maps book
   to author) and the two orphans at the bottom. The extra card "count the chunks per author" (one
   row, top right) and the 3-row container strip print TERM(cli-container/34: 15, 26–28; line 28
   folded before "author = None", so the word stays whole). Each part is marked as the SAY names
   it: the links and the cottage cheese book, row 27 at "178 chunks", its tag, the Woman's
   Institute book, row 28 at "1,505 chunks", its tag. GREEN lines join nine books to nine
   names; Cottage Cheese Recipe Book gets the GREY tag "author not in the list · 178 chunks", the
   Woman's Institute book a RED-edged tag "author = None · 1,505 chunks · lecture 5's file-name
   slip" (in the empty author slots, left of each book).
9. The strip and the card leave; the GREEN card get_book_by_search_content comes in under the lists
   and two PINK arrows reach the two orphans, "still reachable". Then V3's stage builds as named:
   Google's cloud with Gemini · location global, the laptop with the two TEAL containers, the
   dashed boundary "HTTPS".
10. The lock goes on the cylinder; one ghost run (tag `illustration`): the PINK question and the
   two GREEN menu names go into the model ("call 1", a GOLD tick), a BLUE {name, args} card comes
   back across the boundary, the TEAL gear turns, a PINK arrow dips into the cylinder, ten GREEN
   chunk cards wrap into one TEAL {"content": …} card, a fresh question, the BLUE card and the TEAL
   card go in together ("call 2", a GOLD tick) and a BLUE answer comes back. The trip shrinks into
   the call strip under the tracker, the mini-map returns with Tools lit; everything fades: empty
   frame.
"""

import re

import numpy as np
from common import (
    CLOUD,
    CTR,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MINI_CENTER,
    NARRATION,
    TURN,
    AnatomyMini,
    CallStrip,
    MenuColumn,
    TrustStage,
    answer_bars,
    capture,
    concept_box,
    cost_tick,
    erratum_tag,
    excerpt,
    extra_card,
    gear,
    illustration_tag,
    json_card,
    lref,
    menu_card,
    mtext,
    note,
    pencil,
    ponder_at,
    readme_chip,
    ring,
    seal,
    src_panel,
    switch_section,
    term,
    under,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    TAU,
    UP,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    Rotate,
    RoundedRectangle,
    Transform,
    VGroup,
    VMobject,
    there_and_back,
)

from explainer import style as S
from explainer.devops import box, chip, label, line_bar, mono, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S04"]
AT = "agent_tools.py"
PONDER_Q = ("Nine author names, eleven books.\n"
            "At least how many books can get_book_by_author never reach?\n"
            "Can the agent still get to them?")

# ------------------------------------------------------------------ the real sources
README_244 = excerpt("README.md", 244, 244)
README_PHRASE = "let the LLM decide how to retrieve"
assert README_PHRASE in README_244, README_244

ENUM = [re.search(r'"(.+)"', s).group(1) for s in excerpt(AT, 20, 28).split("\n")]   # masked
assert len(ENUM) == 9 and ENUM[-1] == "‹instructor›", ENUM

LOAD = capture("20", "cli-container")                  # the load step's Processing file lines
BOOK_LINES = (9, 23, 36, 52, 65, 77, 89, 101, 116, 129, 142)
BOOKS = []
for _n in BOOK_LINES:
    _m = re.fullmatch(r"Processing file: outputs/embeddings-char-split-(.+)\.jsonl", LOAD.line(_n))
    assert _m, (_n, LOAD.line(_n))
    BOOKS.append(_m.group(1))
assert len(BOOKS) == 11

# cli.py:61-71 maps each book's file name to its metadata (the author the enum must match)
AUTHOR_OF = {}
for _s in excerpt("cli.py", 61, 71).split("\n"):
    _m = re.match(r'\s*"(.+)": \{"author": "(.+)", "year"', _s)
    assert _m, _s
    AUTHOR_OF[_m.group(1)] = _m.group(2)
MATCHED = [next(b for b in BOOKS if AUTHOR_OF.get(b) == a) for a in ENUM]     # book of enum name i
ORPHANS = [b for b in BOOKS if b not in MATCHED]
COTTAGE, WOMANS = "Cottage Cheese Recipe Book", "Womans Institute Library of Cookery"
assert sorted(ORPHANS) == [COTTAGE, WOMANS], ORPHANS

AUTH = capture("34", "cli-container")                  # the extra check: chunks per author
OUT_15, OUT_26, OUT_27, OUT_28 = (AUTH.line(n) for n in (15, 26, 27, 28))
assert OUT_15 == "chunks in char-split-collection: 8248"
assert "'Cottage Cheese Recipe Book': 178 chunks" in OUT_27
assert OUT_28.endswith("'Womans Institute Library of Cookery': 1505 chunks, author = None")
N_COTTAGE = int(re.search(r"(\d+) chunks", OUT_27).group(1))     # 178
N_WOMANS = int(re.search(r"(\d+) chunks", OUT_28).group(1))      # 1505
# line 28 is longer than a row: fold it at the word before "author" (a plain wrap splits "None")
_k = OUT_28.index(" author = None")
OUT_28_ROWS = [OUT_28[:_k], "    " + OUT_28[_k + 1:]]

# ------------------------------------------------------------------ layout
PANEL_L, PANEL_TOP = -6.45, 2.75
NAME_X, BOOK_X = -6.3, 1.0             # left edges of the two columns
BOOK_W = 5.35                          # the widest book title (longer ones are cut with "…")
LANE = 2.42                            # the ghost run's lane, above the stage


def lag_play(scene, anims, owner=None, lag_ratio=0.3, run_time=1.0, extra=()):
    """Play a LaggedStart, then take its wrapper group off the scene: `owner` (the group that holds
    the animated members) is added back whole; without an owner the wrapper is simply removed."""
    g = LaggedStart(*anims, lag_ratio=lag_ratio)
    scene.play(g, *extra, run_time=run_time)
    if owner is not None:
        scene.add(owner)
    elif g.group in scene.mobjects:
        scene.remove(g.group)


def widen(p, w=12.9):
    """Give a code panel's background the full width (text unchanged), so every panel of the
    scene has the same frame and the notes on its lines sit inside it."""
    bg = p.code.background
    new = RoundedRectangle(width=w, height=bg.height, corner_radius=0.15, stroke_color=S.GREY_DARK,
                           stroke_width=2).set_fill(bg.get_fill_color(), bg.get_fill_opacity())
    new.align_to(bg, LEFT).align_to(bg, UP)
    bg.become(new)
    return p


def at_top_left(p):
    widen(p)
    return p.align_to([PANEL_L, 0, 0], LEFT).align_to([0, PANEL_TOP, 0], UP)


def morph_panel(scene, old, new, pairs=(), drift=0.45, run_time=0.8, extra=()):
    """old -> new (two src_panels of the same file): the background resizes in place, paired rows
    Transform into their new places (pairs: (old row indices, new row indices[, extra targets])),
    every other old row drifts up and fades while every other new row rises into place: a scroll
    down the file, or a fold. The headers swap in place. Leaves `new` on the scene as one group."""
    oc, nc = old.code.code_lines, new.code.code_lines
    used_o, used_n, anims, wrappers = set(), set(), [], []
    anims.append(ReplacementTransform(old.code.background, new.code.background))
    anims += [FadeOut(old.header), FadeIn(new.header)]
    for pair in pairs:
        o, n = pair[0], pair[1]
        more = list(pair[2]) if len(pair) > 2 else []
        used_o.update(o)
        used_n.update(n)
        dst = VGroup(*[nc[i] for i in n], *more)
        wrappers.append(dst)
        anims.append(ReplacementTransform(VGroup(*[oc[i] for i in o]), dst))
    anims += [FadeOut(r, shift=UP * drift) for i, r in enumerate(oc) if i not in used_o]
    anims += [FadeIn(r, shift=UP * drift) for i, r in enumerate(nc) if i not in used_n]
    tops = list(scene.mobjects)
    above = tops[tops.index(old) + 1:] if old in tops else []    # drawn over the old panel
    scene.play(*anims, *extra, run_time=run_time)
    scene.remove(old, new, *wrappers)
    scene.add(new)
    still = [m for m in above if m in scene.mobjects]
    if still:                                # e.g. a bracket and its tag: keep them over the panel
        scene.bring_to_front(*still)
    for w in wrappers:                       # extra targets (e.g. the "9 names" note) stay up
        for m in w.submobjects:
            if m not in new.get_family():
                scene.add(m)


def gtag(s, color=DATA, size=20, text_color=None):
    """A small tag in `color` (opaque, text in the tag's colour)."""
    return tag(s, color, size=size, text_color=text_color)


def rbracket(mobs, x, color=DATA, pad=0.05):
    """A ']' bracket at x spanning `mobs` vertically. Not added."""
    g = VGroup(*mobs)
    top, bot = g.get_top()[1] + pad, g.get_bottom()[1] - pad
    ln = VMobject(stroke_color=color, stroke_width=3)
    ln.set_points_as_corners([[x - 0.1, top, 0], [x, top, 0], [x, bot, 0], [x - 0.1, bot, 0]])
    return ln


def line_note(s, color=DATA, size=20, arrow="←"):
    """A note on a code line: an arrow and serif text in `color`, no frame (it fits between rows)."""
    return label(f"{arrow} {s}", size, color)


def two_line_note(a, b, color=DATA, size=20, arrow="↑"):
    rows = VGroup(label(f"{arrow} {a}", size, color), label(b, size, color))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    rows[1].shift(RIGHT * (label(f"{arrow} ", size).width))
    return rows


def short_title(t, max_w=BOOK_W, size=20):
    """The title as shown in the column: cut at a word with a GREY '…' when wider than max_w."""
    if label(t, size).width <= max_w:
        return t
    words = t.split(" ")
    while words and label(" ".join(words) + " …", size).width > max_w:
        words.pop()
    return " ".join(words).rstrip(",") + " …"


def book_row(t, size=20):
    s = short_title(t)
    return label(s, size, S.GREY, t2c={"…": S.GREY_DARK} if s.endswith("…") else None)


def name_row(a, size=20):
    return mtext(a, size, DATA, font=S.FONT)


def place_col(rows, x, ys):
    for r, y in zip(rows, ys):
        r.move_to([x + r.width / 2, y, 0])
    return rows


def slab(color, w=1.15, h=0.1):
    return RoundedRectangle(width=w, height=h, corner_radius=0.04, stroke_color=color,
                            stroke_width=2).set_fill(color, 0.35)


def book_glyph(w=1.15, h=0.12):
    """A book lying flat: a GREY slab with a darker spine."""
    b = RoundedRectangle(width=w, height=h, corner_radius=0.03, stroke_color=S.GREY,
                         stroke_width=2).set_fill(S.GREY, 0.25)
    sp = Line(b.get_left() + RIGHT * 0.12 + UP * h / 2, b.get_left() + RIGHT * 0.12 + DOWN * h / 2,
              color=S.GREY, stroke_width=2)
    return VGroup(b, sp)


def mini_call_card():
    """V3's BLUE function-call card, compact: {name, args} and the small seal."""
    g = json_card(["{name, args}"], CLOUD)
    s = seal(0.15, CLOUD).move_to(g.frame.get_corner(UP + RIGHT) + np.array([-0.04, -0.04, 0]))
    g.add(s)
    return g


def answer_card():
    bars = answer_bars(3, w=1.4, color=CLOUD)
    fr = box(bars.width + 0.5, bars.height + 0.36, CLOUD, fill=S.BG, fill_opacity=0.95, radius=0.12)
    bars.move_to(fr)
    tint = RoundedRectangle(width=fr.width, height=fr.height, corner_radius=0.12, stroke_width=0) \
        .set_fill(CLOUD, 0.1).move_to(fr)
    return VGroup(fr, tint, bars)


class ToolMenu(VoiceScene):
    def construct(self):
        assert len(SAY) == 11, len(SAY)

        # ============================================================ 0 · L05's line, the recap's menu
        mc = MenuColumn(show=())                 # its own strip stays hidden: cp stands in
        self.add(mc)
        cp = MenuColumn(show=("strip",)).parts["strip"]
        boxes, arrows = cp.boxes, cp[1]
        with self.voiceover(SAY[0]) as vo:
            ref = lref("8–14")
            self.play(FadeIn(ref), run_time=0.6)
            vo.wait_until("a straight line")
            self.add(cp)
            lag_play(self, [FadeIn(boxes[0], shift=RIGHT * 0.2), GrowArrow(arrows[0]),
                            FadeIn(boxes[1], shift=RIGHT * 0.2), GrowArrow(arrows[1]),
                            FadeIn(boxes[2], shift=RIGHT * 0.2), GrowArrow(arrows[2]),
                            FadeIn(boxes[3], shift=RIGHT * 0.2)], owner=cp, lag_ratio=0.55, run_time=3.0)
            vo.wait_until("The lecture's recap")
            self.play(Indicate(boxes[1], color=TURN, scale_factor=1.1), run_time=0.7)
            self.play(*mc.parts_in("llm_top", "llm_bot"), run_time=0.6)
            vo.wait_until("steps around the search")
            lag_play(self, [mc.fly_in(0), mc.fly_in(1)], owner=mc, lag_ratio=0.5, run_time=0.9)
            vo.wait_until("whether to retrieve")
            self.play(mc.fly_in(2), run_time=0.5)
            vo.wait_until("grading")
            self.play(mc.fly_in(3), run_time=0.45)
            vo.wait_until("rewriting")
            self.play(mc.fly_in(4), run_time=0.45)
            vo.wait_until("and web search")
            self.play(mc.fly_in(5), run_time=0.45)

        # ============================================================ 1 · a model in front of the menu
        with self.voiceover(SAY[1]) as vo:
            mc.reveal(self, "agentic", run_time=0.5)
            vo.wait_until("puts a model in front")
            self.play(Indicate(mc.parts["llm_top"], color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("and lets it choose")
            hop = ring(mc.parts["box0"], TURN, buff=0.05)
            self.play(*mc.parts_in("chooses"), Create(hop), run_time=0.5)
            for k in (3, 5):
                self.play(hop.animate.move_to(mc.parts[f"box{k}"]), run_time=0.35)

        # ============================================================ 2 · llm-rag: a menu of two
        mm = AnatomyMini(center=MINI_CENTER)
        rc = readme_chip("README.md · line 244 (excerpt)", README_PHRASE, expected=True)
        rc.move_to([0, cp.get_center()[1], 0])
        with self.voiceover(SAY[2]) as vo:
            tr = switch_section(self, None, "Agents", None)
            self.play(*mc.to_menu(), FadeOut(hop), run_time=1.0)
            self.play(FadeIn(mm), run_time=0.5)
            self.play(mm.light("tools"), run_time=0.5)
            vo.wait_until("Its README says")
            self.play(FadeOut(cp), FadeIn(rc, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("Search one author's book")
            r0 = ring(mc.parts["menu0"], TURN, buff=0.06)
            self.play(Create(r0), run_time=0.5)
            vo.wait_until("or search all books")
            r1 = ring(mc.parts["menu1"], TURN, buff=0.06)
            self.play(ReplacementTransform(r0, r1), run_time=0.5)

        # ============================================================ 3 · the first menu item
        p1 = at_top_left(src_panel(AT, 9, 19, wrap={12: ["OpenAPI"]}))
        c1 = p1.code.code_lines
        with self.voiceover(SAY[3]) as vo:
            m0 = mc.parts["menu0"].copy()
            self.add(m0)
            # the first card leaves the menu and lands where its declaration will start
            self.play(FadeOut(mc), FadeOut(rc), FadeOut(ref), FadeOut(mm), FadeOut(r1),
                      m0.animate.align_to(c1[0], LEFT).align_to(c1[0], UP).shift(LEFT * 0.1),
                      run_time=0.7)
            self.play(FadeIn(p1, shift=UP * 0.1), FadeOut(m0), run_time=0.6)
            vo.wait_until("a name, which")
            b10 = p1.bar(10, DATA)
            tA = line_note("the name the model writes back").next_to(c1[1], RIGHT, buff=0.35)
            self.play(FadeIn(b10), FadeIn(tA, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("and a description")
            b11 = p1.bar(11, DATA)
            tB = two_line_note("the model's documentation,", "with the parameter descriptions")
            tB.move_to([0, (c1[3].get_center()[1] + c1[4].get_center()[1]) / 2, 0])
            tB.align_to([c1[3].get_right()[0] + 0.45, 0, 0], LEFT)
            self.play(FadeIn(b11), FadeIn(tB, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("with the parameter descriptions")
            b18 = p1.bar(18, DATA)
            self.play(FadeIn(b18), Indicate(tB[1], color=DATA, scale_factor=1.05), run_time=0.7)
            vo.wait_until("the only documentation")
            # the two description bars brighten and settle back as the narration names them
            self.play(Indicate(tB[0], color=DATA, scale_factor=1.06),
                      VGroup(b11, b18).animate(rate_func=there_and_back).set_fill(opacity=0.42),
                      run_time=0.8)
            vo.wait_until("Parameters come as")
            rows = [c1[k] for k in (5, 6, 7)]
            bx = max(r.get_right()[0] for r in rows) + 0.3
            br = rbracket(rows, bx)
            tC = gtag("JSON schema").next_to(br, RIGHT, buff=0.15)
            self.play(Create(br), FadeIn(tC, shift=LEFT * 0.1), run_time=0.6)

        # ============================================================ 4 · enum, coaching, required
        p2 = at_top_left(src_panel(AT, 19, 30))
        c2 = p2.code.code_lines
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(b10, b11, b18, tA, tB, br, tC)), run_time=0.3)
            morph_panel(self, p1, p2, pairs=[(p1.rows_of(19), p2.rows_of(19))], run_time=0.8)
            vo.wait_until("9 names in an enum")
            names = [c2[k] for k in range(1, 10)]
            bx = max(r.get_right()[0] for r in names) + 0.25
            br2 = rbracket(names, bx)
            tE = gtag("enum: only these 9").next_to(br2, RIGHT, buff=0.15)
            self.play(Create(br2), FadeIn(tE, shift=LEFT * 0.1), run_time=0.6)
            self.wait(0.15)
            # the nine name rows fold into one row; the bracket and its tag fold with them
            p2f = at_top_left(src_panel(AT, [19, 29, 30]))
            gap = p2f.code.code_lines[1]
            nine = mono("9 names …", 22, S.GREY).next_to(gap, RIGHT, buff=0.18)
            nine.align_to(gap, DOWN)
            names_rows = [k for n in range(20, 29) for k in p2.rows_of(n)]
            fold = [(p2.rows_of(n), p2f.rows_of(n)) for n in (19, 29, 30)]
            fold.append((names_rows, [1], [nine]))
            br2f = rbracket([gap, nine], nine.get_right()[0] + 0.25)
            morph_panel(self, p2, p2f, pairs=fold, run_time=0.7,
                        extra=[Transform(br2, br2f), tE.animate.next_to(br2f, RIGHT, buff=0.15)])
            vo.wait_until("The search text's description")
            self.wait(0.4)
            p3 = at_top_left(src_panel(AT, 31, 37, wrap=True))
            morph_panel(self, p2f, p3, run_time=0.7,
                        extra=[FadeOut(VGroup(nine, br2, tE), shift=UP * 0.45)])
            vo.wait_until("even coaches the model")
            b33 = p3.bar(33, TURN)
            self.play(FadeIn(b33), run_time=0.5)
            vo.wait_until("a sentence or two")
            aa = p3.span(33, "a a")
            u_aa = under(aa, S.GREY, 3)
            tErr = erratum_tag("typo in the source")
            row7 = p3.code.code_lines[p3.rows_of(34)[0]]
            row8 = p3.code.code_lines[p3.rows_of(35)[0]]
            tErr.move_to([aa.get_center()[0] + tErr.width / 2 - 0.3,
                          (row7.get_center()[1] + row8.get_center()[1]) / 2, 0])
            self.play(Create(u_aa), FadeIn(tErr, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("And both fields are required")
            b36 = p3.bar(36, DATA)
            self.play(FadeIn(b36), run_time=0.4)
            self.play(Indicate(p3.span(36, '["author", "search_content"]'), color=DATA, scale_factor=1.06),
                      run_time=0.6)

        # ============================================================ 5 · the real function
        p4 = at_top_left(src_panel(AT, 41, 49, wrap={41: ["collection"], 47: ["n_results"]}))
        c4 = p4.code.code_lines
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(b33, u_aa, tErr, b36)), run_time=0.3)
            morph_panel(self, p3, p4, run_time=0.8)
            vo.wait_until("Two more arguments")
            code_args = p4.span(41, "collection, embed_func")
            u_code = under(code_args, CTR, 4)
            self.play(Create(u_code), run_time=0.5)
            vo.wait_until("the collection and")
            self.play(Indicate(p4.span(41, "collection"), color=CTR, scale_factor=1.12), run_time=0.6)
            vo.wait_until("an embedding function")
            self.play(Indicate(p4.span(41, "embed_func"), color=CTR, scale_factor=1.12), run_time=0.6)
            vo.wait_until("your code supplies them")
            tCode = line_note("your code supplies these", CTR).next_to(c4[1], RIGHT, buff=0.35)
            self.play(FadeIn(tCode, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("The model controls only")
            model_args = p4.span(41, "author, search_content")
            u_model = under(model_args, DATA, 4)
            tModel = line_note("from the model").next_to(c4[0], RIGHT, buff=0.35)
            self.play(Create(u_model), FadeIn(tModel, shift=LEFT * 0.15), run_time=0.6)
            b47 = line_bar(p4.code, p4.rows_of(47)[1], LOOKUP, 0.22)    # where={"author": author}
            self.play(FadeIn(b47), run_time=0.5)
            vo.wait_until("and the search text")
            self.play(Indicate(p4.span(43, "search_content"), color=LOOKUP, scale_factor=1.12),
                      run_time=0.6)
        p5 = widen(src_panel(AT, 78, 81, wrap={80: ["get_book_by_search_content_func"]}))
        p5.align_to([PANEL_L, 0, 0], LEFT).align_to([0, -3.45, 0], DOWN)
        c5 = p5.code.code_lines
        tTool = line_note("one Tool, two declarations").next_to(c5[3], RIGHT, buff=0.35)
        b80 = p5.bar(80, DATA)
        self.play(FadeOut(VGroup(u_code, tCode, u_model, tModel, b47)), run_time=0.3)
        morph_panel(self, p4, p5, run_time=0.9)
        self.play(FadeIn(b80), FadeIn(tTool, shift=LEFT * 0.15), run_time=0.6)
        self.wait(0.3)

        # ============================================================ 6 · slide 39's three duties
        duties = VGroup(concept_box("pick the tool"), concept_box("format its inputs"),
                        concept_box("interpret its outputs")).arrange(RIGHT, buff=0.9)
        duties.move_to([0, 1.95, 0])
        pen = pencil(0.75, CLOUD)
        pen_l = label("the model writes", 22, CLOUD)
        pen_g = VGroup(pen, pen_l).arrange(RIGHT, buff=0.25)
        pen_g.move_to([(duties[0].get_center()[0] + duties[1].get_center()[0]) / 2 - 0.4, 0.35, 0])
        links = VGroup(*[Line(d.get_bottom() + DOWN * 0.05, pen.get_top() + UP * 0.08, color=CLOUD,
                              stroke_width=3) for d in duties[:2]])
        call2 = gtag("call 2", S.GREY).next_to(duties[2], DOWN, buff=0.25)
        gr = gear(0.3, CTR)
        gr_l = label("your code runs", 22, CTR)
        gr_g = VGroup(gr, gr_l).arrange(RIGHT, buff=0.25).next_to(pen_g, RIGHT, buff=1.0)
        with self.voiceover(SAY[6]) as vo:
            ref = lref("39")
            self.play(FadeIn(ref), run_time=0.5)
            vo.wait_until("a tool-using agent")
            must = note("a tool-using agent must", size=22).move_to([0, 2.65, 0])
            self.play(FadeIn(must, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("pick the right tool")
            self.play(FadeIn(duties[0], shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("format its inputs")
            self.play(FadeIn(duties[1], shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("and interpret its outputs")
            self.play(FadeIn(duties[2], shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("Here the model picks")
            self.play(FadeIn(pen_g, shift=UP * 0.15), run_time=0.5)
            self.play(Create(links), FadeIn(call2, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("your code runs the tool")
            self.play(FadeIn(gr_g, shift=LEFT * 0.15), run_time=0.5)
            self.play(Rotate(gr, angle=-TAU / 2), run_time=1.2)

        # ============================================================ 7 · eleven books, nine names
        ys7 = [2.12 - k * 0.37 for k in range(11)]
        names7 = place_col(VGroup(*[name_row(a) for a in ENUM]), NAME_X, ys7[:9])
        books7 = place_col(VGroup(*[book_row(b) for b in BOOKS]), BOOK_X, ys7)
        h_names = label("9 names in the enum", 22, DATA)
        h_names.move_to([NAME_X + h_names.width / 2, 2.62, 0])
        h_books = label("11 books in the collection", 22, S.GREY)
        h_books.move_to([BOOK_X + h_books.width / 2, 2.62, 0])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(p5, b80, tTool, must, duties, pen_g, links, call2, gr_g)), FadeOut(ref),
                      run_time=0.6)
            self.play(FadeIn(h_books), FadeIn(books7, shift=LEFT * 0.15, lag_ratio=0.12), run_time=1.3)
            vo.wait_until("beside the 9 names")
            self.play(FadeIn(h_names), FadeIn(names7, shift=RIGHT * 0.15, lag_ratio=0.12), run_time=1.2)

        # ---------------------------------------------------------- PONDER: the lists collapse to counts
        n_stack = VGroup(*[slab(DATA) for _ in range(9)]).arrange(UP, buff=0.05)
        b_stack = VGroup(*[book_glyph() for _ in range(11)]).arrange(UP, buff=0.04)
        for k, g in enumerate(b_stack):
            g.shift(RIGHT * 0.05 * ((k * 7) % 3 - 1))
        n_lab = label("9 author names", 22, DATA)
        b_lab = label("11 books", 22, S.GREY)
        n_grp = VGroup(n_stack, n_lab).arrange(RIGHT, buff=0.35)
        b_grp = VGroup(b_stack, b_lab).arrange(RIGHT, buff=0.35)
        n_grp.move_to([-3.0, 0.35, 0])
        b_grp.move_to([3.0, 0.35, 0])
        b_stack.align_to(n_stack, DOWN)
        b_lab.move_to([b_lab.get_center()[0], b_stack.get_center()[1], 0])
        n_lab.move_to([n_lab.get_center()[0], n_stack.get_center()[1], 0])
        menus = VGroup(*[menu_card(s) for s in MenuColumn.MENU]).arrange(DOWN, buff=0.14)
        menus.move_to([0, 2.15, 0])
        self.play(*[ReplacementTransform(n, s) for n, s in zip(names7, n_stack)],
                  *[ReplacementTransform(b, s) for b, s in zip(books7, b_stack)],
                  ReplacementTransform(h_names, n_lab), ReplacementTransform(h_books, b_lab),
                  FadeIn(menus, shift=DOWN * 0.15), run_time=1.0)
        card = ponder_at(self, PONDER_Q, 8)

        # ============================================================ 8 · two books
        ys8 = [2.5 - k * 0.33 for k in range(9)] + [-0.6, -1.1]
        order = MATCHED + [WOMANS, COTTAGE]            # the orphans in the empty author slots
        names8 = place_col(VGroup(*[name_row(a) for a in ENUM]), NAME_X, ys8[:9])
        books8 = place_col(VGroup(*[book_row(b) for b in order]), BOOK_X, ys8)
        by_title = {b: books8[order.index(b)] for b in BOOKS}
        links8 = VGroup(*[Line(n.get_right() + RIGHT * 0.15, books8[k].get_left() + LEFT * 0.15,
                               color=DATA, stroke_width=2.5) for k, n in enumerate(names8)])
        xc = extra_card("count the chunks per author")
        xc.header.next_to(xc.frame, LEFT, buff=0.25)
        xc.move_to([6.45 - xc.width / 2, 3.58 - xc.height / 2, 0])
        t = term(rows=3, container=True)
        w_book, c_book = by_title[WOMANS], by_title[COTTAGE]
        t_cot = gtag(f"author not in the list · {N_COTTAGE:,} chunks", S.GREY)
        t_cot.move_to([w_book.get_left()[0] - 0.25 - t_cot.width / 2, c_book.get_center()[1], 0])
        t_wom = gtag(f"author = None · {N_WOMANS:,} chunks · lecture 5's file-name slip", ERR, text_color=INK)
        t_wom.move_to([w_book.get_left()[0] - 0.25 - t_wom.width / 2, w_book.get_center()[1], 0])
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(card), FadeOut(menus), FadeOut(n_lab), FadeOut(b_lab),
                      *[ReplacementTransform(s, n) for s, n in zip(n_stack, names8)],
                      *[ReplacementTransform(s, by_title[b]) for s, b in zip(b_stack, BOOKS)],
                      FadeIn(xc, shift=DOWN * 0.15), FadeIn(t, shift=UP * 0.3), run_time=1.0)
            t.print(self, [OUT_15, OUT_26, OUT_27], run_time=0.5)
            out28 = t.print(self, OUT_28_ROWS, run_time=0.4)
            vo.wait_until("The cottage cheese")
            lag_play(self, [Create(ln) for ln in links8], owner=links8, lag_ratio=0.15, run_time=1.1,
                     extra=[c_book.animate.set_color(INK)])
            vo.wait_until("178 chunks")
            row27 = t.find("Cottage")
            u27 = under(substring(row27, f"'{COTTAGE}': {N_COTTAGE} chunks"), S.GREY, 3)
            self.play(Create(u27), run_time=0.4)
            vo.wait_until("has an author who")
            self.play(FadeIn(t_cot, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("The Woman's Institute")
            self.play(w_book.animate.set_color(INK), run_time=0.4)
            vo.wait_until("1,505 chunks")
            u28 = VGroup(*[under(substring(r, r.text.strip()), ERR, 3) for r in out28])
            self.play(Create(u28), run_time=0.5)
            vo.wait_until("has no author at all")
            self.play(FadeIn(t_wom, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("a file name slip")
            self.play(Indicate(t_wom.text, color=ERR, scale_factor=1.04), run_time=0.7)

        # ============================================================ 9 · still reachable; the stage
        m1 = menu_card(MenuColumn.MENU[1])
        m1.move_to([6.45 - m1.width / 2, -2.45, 0])
        reach = label("still reachable", 22, LOOKUP).next_to(m1, LEFT, buff=0.35)
        a_w = GrowArrow(_arrow_up(m1, w_book.get_right()[0] + 0.15, w_book.get_bottom()[1] + 0.02))
        a_c = GrowArrow(_arrow_up(m1, c_book.get_center()[0], c_book.get_bottom()[1] + 0.02))
        st = TrustStage(show=())
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(t), FadeOut(xc), FadeOut(u27), FadeOut(u28), run_time=0.5)
            self.play(FadeIn(m1, shift=UP * 0.15), run_time=0.5)
            self.play(a_w, a_c, FadeIn(reach), run_time=0.7)
            vo.wait_until("Now the stage")
            lists = VGroup(names8, books8, links8, t_cot, t_wom, m1, reach, a_w.mobject, a_c.mobject)
            self.play(FadeOut(lists), run_time=0.6)
            self.add(st)
            vo.wait_until("Gemini in Google's cloud")
            st.reveal(self, "cloud", "model", run_time=0.7)
            vo.wait_until("two containers")
            st.reveal(self, "laptop", run_time=0.4)
            st.reveal(self, "cli", "chroma", run_time=0.6)
            vo.wait_until("and a boundary between")
            st.reveal(self, "boundary", "https", run_time=0.6, anim=lambda m: FadeIn(m, shift=DOWN * 0.1))

        # ============================================================ 10 · only a menu crosses; one ghost run
        model_c = st.parts["model"].frame.get_center()
        q1 = chip("question", LOOKUP, size=20)
        mn = VGroup(*[menu_card(s.split("(")[0]) for s in MenuColumn.MENU]).arrange(DOWN, buff=0.1,
                                                                                    aligned_edge=LEFT)
        call1 = VGroup(q1, mn).arrange(RIGHT, buff=0.3)
        call1.move_to([2.4, 2.72, 0])
        itag = illustration_tag().move_to([-4.3, -1.95, 0])
        lab = label("call 1", 22, S.GREY).move_to([-1.6, 3.25, 0])
        tick1 = cost_tick().next_to(lab, RIGHT, buff=0.15)
        cc = mini_call_card()
        cc.move_to(model_c)
        cc_spot = np.array([0.3, LANE, 0])

        def absorb(m):
            return m.animate.move_to(model_c).scale(0.15).set_opacity(0)

        with self.voiceover(SAY[10]) as vo:
            st.reveal(self, "lock", run_time=0.5, extra=[FadeIn(itag)])
            self.play(FadeIn(call1, shift=UP * 0.2), FadeIn(lab), FadeIn(tick1), run_time=0.6)
            vo.wait_until("only a menu")
            lag_play(self, [absorb(m) for m in (mn[0], mn[1], q1)], lag_ratio=0.15, run_time=0.9)
            self.remove(call1, q1, *mn)
            vo.wait_until("Call 1 returns")
            self.play(*st.light("model"), run_time=0.3)
            self.play(FadeIn(cc, scale=0.4), *st.unlight("model"), run_time=0.4)
            self.play(cc.animate.move_to(cc_spot), run_time=0.9)
            vo.wait_until("a function name")
            self.play(Indicate(cc[2], color=CLOUD, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Your code runs it")
            dip = st.dip()
            chunks = st.chunk_cards(10)
            tc = json_card(['{"content": …}'], CTR)
            tc.next_to(cc, RIGHT, buff=0.18)
            st.reveal(self, "gear", run_time=0.3)
            self.play(Rotate(st.parts["gear"], angle=-TAU / 3), GrowArrow(dip),
                      FadeIn(chunks, scale=0.6, lag_ratio=0.08), run_time=0.75)
            self.play(ReplacementTransform(chunks, tc), FadeOut(dip), run_time=0.5)
            vo.wait_until("call 2 sends back")
            q2 = chip("question", LOOKUP, size=20).next_to(tc, RIGHT, buff=0.18)   # clear of HTTPS
            lab2 = label("call 2", 22, S.GREY).move_to(lab)
            tick2 = cost_tick().next_to(lab2, RIGHT, buff=0.15)
            self.play(FadeIn(q2, shift=DOWN * 0.1), ReplacementTransform(lab, lab2),
                      ReplacementTransform(tick1, tick2), run_time=0.4)
            lag_play(self, [absorb(m) for m in (q2, cc, tc)], lag_ratio=0.12, run_time=0.9)
            self.remove(q2, cc, tc)
            ans = answer_card().move_to(model_c)
            self.play(FadeIn(ans, scale=0.4), run_time=0.35)
            self.play(ans.animate.move_to(cc_spot), run_time=0.8)

        cs = CallStrip()
        trip = VGroup(st, ans, lab2, tick2, itag)
        # the trip shrinks toward the call strip, which takes over as it vanishes
        lag_play(self, [FadeOut(trip, target_position=cs.get_center(), scale=0.25),
                        FadeIn(cs, scale=0.85)], owner=cs, lag_ratio=0.6, run_time=1.2)
        mm2 = AnatomyMini(center=MINI_CENTER)
        self.play(FadeIn(mm2), run_time=0.5)
        self.play(mm2.light("tools"), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(tr), FadeOut(cs), FadeOut(mm2), run_time=0.8)
        self.wait(0.3)


def _arrow_up(card, x, y_end):
    """A PINK arrow from the top of `card` straight up to (x, y_end). Not added."""
    from manim import Arrow
    return Arrow([x, card.get_top()[1] + 0.02, 0], [x, y_end, 0], buff=0.04, color=LOOKUP, stroke_width=4,
                 tip_length=0.18, max_tip_length_to_length_ratio=0.3)
