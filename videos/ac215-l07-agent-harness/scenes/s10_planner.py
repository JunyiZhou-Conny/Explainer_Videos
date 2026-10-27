"""S10 · Act 4: a planner with five drawers (README "3 · Harness › Act 4", step 1, and one extra).
Lecture: 8, 13–16, then 22.

Beats (script.md "## S10", one voiceover block each):
 0  The event chip README.md · line 460 (excerpt) "40 guests in NY" arrives mid-frame (it flashes
    on "a 40-guest event") and moves top left on "The lecture splits". Then LECTURE 8, 13–16 comes
    in with slides 13/16's two memory chips on the left, "short-term memory" and "long-term memory"
    (GREY dashed, tag `concept · lecture only`), and V6's empty cabinet frame on the right (tag
    `illustration`). On "saved memory" the long-term chip slides into the GREEN drawer "Memory ·
    customer_memory.sqlite", on "and history" the short-term chip into "History · the
    conversation"; on "plus tasks", "approvals" and "and the audit" the drawers Tasks, Approval and
    Audit slide in between. On "five kinds of state" a GREEN brace with those words. No key yet.
 1  The checkpoint chip README.md · line 522 "Which of these can authorize an action?" (top band).
    A GREY hand tries Tasks, History, Memory and Audit with a turn: each stays shut and turns GREY.
    On "Only one" a YELLOW key comes down into the Approval drawer's keyhole; on "the approval
    drawer" it turns and the drawer opens.
 2  TRACKER Act4 1. The chips, brace, key and hand leave; the cabinet closes, its words fade and it
    shrinks to a glyph in the top band, right. The container terminal (13 rows, TEAL, title-bar tag
    `no key`) types `python cli.py --act 4` (GOLD `live · billed per token` beside it) ->
    container/40 lines 2–4, 5 (its blank line), 6–8 wrapped, 9 as 401s. On "the harness prints"
    line 4 turns GREEN (the mask stays GREY) with the GREEN tag "loaded by the host · before any
    model call" on the blank row under it; the nine tool names of line 8 light GREEN as the SAY
    names them. On "No tool writes memory" a GREY dashed ghost chip "a memory-write tool", struck
    through RED, appears beside them; the terminal shrinks to the strip (the command, line 4, the
    tools' last row with the ghost chip) while the cabinet grows back above it, its words return
    (tag `illustration`), and a BLUE hand reaches for the Memory drawer and finds no handle ("the
    model: no memory tool").
 3  The cabinet and hand leave. Above the strip QUOTE(README.md: 460) (`expected`), its brief rows
    underlined YELLOW on "1,000 grams each" and its stock row on "The shop has only"; beside it a
    stock bar for Époisses: on "and 1,200 of" a 1,200 g outline, on "The shop has only" 900 g GREEN,
    on "300 short" the missing 300 g RED dashed "300 g short". On "A finished task"
    QUOTE(README.md: 471) with its two sentences "A completed task is not an approval." and "Shop
    stock does not establish vendor availability.", underlined in turn.
 4  The cards, bar and strip leave. CODE(formaggio/agents/planner_tools.py: 72–75); under it a
    GREEN `save_vendor_email` card. On "approval mode always require" a YELLOW box round
    `approval_mode="always_require"`; on "so the framework pauses" a padlock closes on the card
    and the PURPLE tag "the framework pauses" appears. On "Act 3 paused" a mini rail (tag
    `illustration`) freezes amber at "manager review" ("act 3: a workflow pauses"); on "this
    pauses one tool" the tool card freezes amber ("act 4: one tool pauses").
 5  TRACKER Act4 1 · extra. The container terminal (12 rows, TEAL, title-bar tag `scripted`) types
    `python cli.py --act 4 --fixture --email-decision approve` (it folds; `--email-decision
    approve` in a YELLOW outline with the YELLOW tag `TEST decision` and the GREY tag `extra`) ->
    container/42 lines 51–53, 55–60. On "the vendor address" line 52 PINK; on "and a body written
    by code" the GREY tag "written by code, not the model" beside line 55 and line 57 YELLOW; on
    "nut allergy included" line 58 GREEN. On "Then:" it prints lines 62 and 65 wrapped ("status:
    saved" and "email transmitted: no" turn GREEN as the SAY names them), and on "and the file
    path" lines 83, 91 wrapped and 92 (the path PINK).
 6  Line 62 gets YELLOW underlines; on "the README predicts it" the top-band chip README.md · line
    837 (excerpt) "a misleading approval-identity warning on successful resumes"; on "and it's
    harmless" the GREY tag `harmless` beside it; on "Trust the authoritative block" lines 83 and
    92 turn GREEN. On "Pause and run step 1" the terminal leaves (the caption drops " · extra");
    LECTURE 22 with the V1 mini-map: Tools YELLOW, its GREEN cell gains a bar, caption "Tools ←
    approval on save". The caption, map and tag leave; the static "your turn" card (with your
    key: the live command, "type approve or decline when asked"; the extra fixture command, GREEN
    "no key: offline · free"; GOLD "live · billed per token"). Hold 2 s, then fade to an empty
    frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Brace,
    Circumscribe,
    Create,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    Mobject,
    Rectangle,
    RoundedRectangle,
    Rotate,
    Succession,
    SurroundingRectangle,
    VGroup,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.devops import MONO, box, label, mono, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S10"]

# ------------------------------------------------------------------ the real captures (file line numbers)
C40 = capture("container/40")
C42 = capture("container/42")
assert C40.cmd == "python cli.py --act 4", C40.cmd
assert C42.cmd == "python cli.py --act 4 --fixture --email-decision approve", C42.cmd
assert len(P_CTR) + 1 + len(C40.cmd) <= 65                 # the live command fits its row
assert len(P_CTR) + 1 + len(C42.cmd) > 65                  # the fixture command folds
MEM4 = C40.line(4)
assert MEM4 == f"Memory for {MASK1}: French cheeses; funky cheeses", MEM4
MEM_A, MEM_B = "Memory for ", ": French cheeses; funky cheeses"
assert C40.line(5) == ""
assert C40.line(8).startswith("  Available tools: ")
assert PLANNER_TOOLS == ("assess_event", "read_vendor_document", "draft_vendor_email", "save_vendor_email",
                         "todos_add", "todos_complete", "todos_remove", "todos_get_remaining", "todos_get_all")
assert "memory" not in " ".join(PLANNER_TOOLS)              # no memory-write tool
TOOL_BEATS = (("assess the event", PLANNER_TOOLS[:1]), ("read the vendor document", PLANNER_TOOLS[1:2]),
              ("draft and save", PLANNER_TOOLS[2:4]), ("and the to-do tools", PLANNER_TOOLS[4:]))
assert C42.line(51).startswith("MOCK EMAIL REVIEW — ticket ")
assert C42.line(52) == f"To: {VENDOR}"
assert C42.line(57) == "- Époisses: 300 g additional"
assert C42.line(58) == "Destination: NY. Confirmed allergy constraints: nuts."
assert C42.line(55) == "Hello," and C42.line(60) == "Thank you."
assert C42.line(62).startswith("Ignored an approval response with id ")
assert "approval occurrence identity" in C42.line(62)
SAVED, SENT = "status: saved", "email transmitted: no"
assert SAVED in C42.line(65) and C42.line(65).endswith(SENT)
assert C42.line(83).startswith("--- HARNESS SAVED — run ")
HTML_PATH = C42.line(91).split("HTML file: ", 1)[1]
assert HTML_PATH.startswith("/app/outputs/") and HTML_PATH.endswith(".html")
assert C42.line(92) == "No order placed; no email transmitted."

# ------------------------------------------------------------------ sources (exact sub-strings, checked)
R460 = source_line("README.md", 460)
EVENT = "40 guests in NY"
assert EVENT in R460
Q460 = ["The event brief specifies 1,000 g Comté, 1,000 g Mimolette, and 1,200 g Époisses for 40 guests in NY.",
        "The cheese quote is $177.80.",
        "Shop Époisses stock is 900 g, leaving a 300 g shortfall."]
assert " ".join(Q460) == R460, R460
NEED_G, STOCK_G = 1200, 900                     # README.md line 460 (and container/42 line 90: "300 g short")
assert f"{NEED_G:,} g Époisses" in R460 and f"stock is {STOCK_G} g" in R460 and f"{NEED_G - STOCK_G} g shortfall" in R460
Q471 = ["A completed task is not an approval.", "Shop stock does not establish vendor availability."]
assert all(q in source_line("README.md", 471) for q in Q471)
R522 = "Which of these can authorize an action?"
assert source_line("README.md", 522).endswith(R522) and source_line("README.md", 522).startswith("**Checkpoint:**")
PT = "formaggio/agents/planner_tools.py"
APPROVAL72 = 'approval_mode="always_require"'
assert source_line(PT, 72).strip() == f"@tool({APPROVAL72})"
assert source_line(PT, 73).strip().startswith("def save_vendor_email(")
R837 = "a misleading approval-identity warning on successful resumes"
assert R837 in source_line("README.md", 837)
FIX_CMD = C42.cmd

# ------------------------------------------------------------------ layout
SAFE = 6.45
CAB_C = np.array([2.25, -0.45, 0])     # the cabinet (beats 0-1): x -1.25..5.75, y -2.5..1.6
CHIP_X = -4.3                          # the lecture's memory chips, left
BAND_K = 0.2                           # the cabinet as a glyph in the top band (beat 2), over a 13-row terminal
BAND_RIGHT = 5.1                       # (clear of the `no key` tag on the title bar under it)
CAB2_C = np.array([-2.9, STRIP_TOP + 0.08 + 2.05, 0])   # the cabinet back above the strip (frame 7.0 x 4.1)
FREEZE_X = 3.3                         # beat 4: the two freezes at x = -3.3 and +3.3


# ------------------------------------------------------------------ small helpers (S09's idioms)
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


def flash(mob, color: str = TURN, k: float = 1.1):
    """Indicate on a chip's or tag's TEXT (its .text), never on a filled backing."""
    txt = getattr(mob, "text", None)
    return Indicate(txt if isinstance(txt, Mobject) else mob, color=color, scale_factor=k)


def apart(a, b, gap: float = 0.06):
    """Assert that the bounding boxes of a and b are at least `gap` apart (no overlap)."""
    ok = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
          or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    assert ok, (a.get_corner(DOWN + LEFT), a.get_corner(UP + RIGHT), b.get_corner(DOWN + LEFT), b.get_corner(UP + RIGHT))


def inside(m, x0: float = -6.55, x1: float = 6.55, y0: float = -3.55, y1: float = 3.55):
    assert m.get_left()[0] >= x0 and m.get_right()[0] <= x1 and m.get_bottom()[1] >= y0 and m.get_top()[1] <= y1, \
        (m.get_corner(DOWN + LEFT), m.get_corner(UP + RIGHT))


def bar_y(t, rows: int) -> float:
    """The title bar's centre y of the house terminal `t` at `rows` rows (bottom edge fixed)."""
    return strip_top(rows) - t.bar_h / 2


def fit(scene, t, rows: int, keep=None, tags=(), run_time: float = 0.8, extra=()):
    """resize(), with the title-bar tags riding along on the bar (S08/S09's idiom); `extra`
    animations play with the frame's move."""
    y = bar_y(t, rows)
    title, t.title = t.title, None
    try:
        resize(scene, t, rows, keep=keep, run_time=run_time,
               extra=[title.animate.set_y(y), *[m.animate.set_y(y) for m in tags], *extra])
    finally:
        t.title = title


def slim_tag(s: str, color: str = S.GREY) -> VGroup:
    """A tag whose box fits inside one terminal row pitch (0.40): it sits on a blank output row
    without touching the rows above and below. .box .text"""
    t = label(s, CAPTION, color)
    b = RoundedRectangle(width=t.width + 0.36, height=t.height + 0.1, corner_radius=(t.height + 0.1) / 2,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return keep_size(g)


def ghost_chip(s: str) -> VGroup:
    """A GREY dashed chip for something that does not exist (a memory-write tool), one row tall.
    Strike it through with strike(g.text, ERR) once it is placed. .box .text"""
    t = label(s, CAPTION, S.GREY)
    h = 0.34
    b = box(t.width + 0.4, h, S.GREY, dashed=True, radius=h / 2, stroke=2)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return keep_size(g)


def drawer_rows(cab: Cabinet) -> dict:
    """The text row (title · detail) of every drawer (Cabinet builds VGroup(face, tint, row, …))."""
    out = {}
    for k, g in cab.dr.items():
        row = g.submobjects[2]
        assert g.title in row.submobjects and g.detail in row.submobjects
        out[k] = row
    return out


def shut_grey(cab: Cabinet, name: str) -> list:
    """Animations: a drawer that stays shut turns GREY (face, tint, words, handle)."""
    g = cab.drawer(name)
    anims = [g.face.animate.set_stroke(S.GREY), g[1].animate.set_fill(S.GREY, 0.08),       # g[1]: the tint
             g.title.animate.set_color(S.GREY), g.detail.animate.set_color(S.GREY)]
    if g.handle is not None:
        anims.append(g.handle.animate.set_fill(S.GREY, 0.9))
    return anims


def regreen(cab: Cabinet, names) -> list:
    """Animations: the drawers' shapes back to GREEN (their words are about to fade)."""
    anims = []
    for n in names:
        g = cab.drawer(n)
        anims += [g.face.animate.set_stroke(HARNESS), g[1].animate.set_fill(HARNESS, 0.1)]
        if g.handle is not None:
            anims.append(g.handle.animate.set_fill(HARNESS, 0.9))
    return anims


def pin_all(scene, row, mobs, anims, run_time: float = 0.4):
    """Play `anims`, then make `mobs` part of the terminal row (they scroll and fade with it), as
    pin() does for one tag. Only outlines, lines and tags placed clear of the row's text."""
    for m in mobs:
        assert not covers_text(m, row), m
    scene.play(*anims, run_time=run_time)
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def recolor(glyphs, color: str):
    return glyphs.animate.set_color(color)


def tool_card(text: str = "save_vendor_email") -> VGroup:
    """Beat 4: the GREEN tool card (mono name left, room for the padlock right). .frame .tint
    .text .lock_spot"""
    t = mono(text, CAPTION + 2, INK)
    w, h = t.width + 1.3, 0.8
    fr = box(w, h, HARNESS, fill=S.BG, fill_opacity=1.0, stroke=3)
    tint = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_width=0).set_fill(HARNESS, 0.12)
    t.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, tint, t)
    g.frame, g.tint, g.text = fr, tint, t
    g.lock_spot = lambda: np.array([fr.get_right()[0] - 0.42, fr.get_center()[1], 0])
    return g


class StockBar(VGroup):
    """Beat 3 (illustration of README.md line 460): Époisses needs 1,200 g; the shop has 900 g; 300 g
    short. A GREY outline (the need), a GREEN bar (shop stock), a RED dashed segment (short).
    Parts: name, need (label), outline, bar, have (label), gap, short (label)."""

    def __init__(self, w: float = 3.7):
        super().__init__()
        h = 0.44
        self.outline = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=INK,
                                        stroke_width=2.5).set_fill(opacity=0)
        k = STOCK_G / NEED_G
        self.bar = Rectangle(width=w * k - 0.06, height=h - 0.1, stroke_width=0).set_fill(HARNESS, 0.75)
        self.bar.move_to(self.outline.get_left() + RIGHT * (0.04 + self.bar.width / 2))
        gw = w * (1 - k)
        self.gap = box(gw - 0.06, h - 0.1, ERR, dashed=True, stroke=2.5, radius=0.05)
        self.gap.move_to(self.outline.get_right() + LEFT * (0.04 + (gw - 0.06) / 2))
        self.name = label("Époisses", CAPTION, INK).next_to(self.outline, UP, buff=0.14).align_to(self.outline, LEFT)
        self.need = label(f"{NEED_G:,} g needed", CAPTION, INK).next_to(self.outline, UP, buff=0.14).align_to(self.outline, RIGHT)
        self.have = label(f"{STOCK_G} g in stock", CAPTION, HARNESS).next_to(self.outline, DOWN, buff=0.14).align_to(self.outline, LEFT)
        self.short = label(f"{NEED_G - STOCK_G} g short", CAPTION, ERR).next_to(self.outline, DOWN, buff=0.14).align_to(self.outline, RIGHT)
        self.need.align_to(self.name, DOWN)
        self.short.align_to(self.have, UP)
        assert self.have.get_right()[0] + 0.2 < self.short.get_left()[0]
        assert self.name.get_right()[0] + 0.2 < self.need.get_left()[0]
        self.add(self.outline, self.bar, self.gap, self.name, self.need, self.have, self.short)


# ------------------------------------------------------------------ the scene
class FiveDrawers(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · two memory chips -> five drawers
        lr = lref("8, 13–16")
        ev = readme_chip("README.md · line 460 (excerpt)", EVENT)
        place(ev, left=-SAFE, cy=3.27)
        apart(ev, lr, 0.3)
        ev_home = ev.get_center()
        cab = Cabinet(only=())
        cab.shift(CAB_C - cab.frame.get_center())
        ill = illustration_tag()
        place(ill, right=cab.frame.get_right()[0], top=cab.frame.get_bottom()[1] - 0.12)
        st_chip = concept_box("short-term memory")
        lt_chip = concept_box("long-term memory")
        for c_, k in ((st_chip, "history"), (lt_chip, "memory")):
            place(c_, cx=CHIP_X, cy=cab.drawer(k).face.get_center()[1])
        ctag = concept_tag()
        place(ctag, cx=CHIP_X, bottom=st_chip.get_top()[1] + 0.2)
        brace = Brace(cab.frame, LEFT, buff=0.12, color=HARNESS)
        five = label("five kinds of state", CAPTION + 2, HARNESS)
        place(five, right=brace.get_left()[0] - 0.15, cy=cab.frame.get_center()[1])
        for m in (ev, cab, ill, st_chip, lt_chip, ctag, brace, five):
            inside(m)
        apart(ctag, ev, 0.3)
        apart(st_chip, cab.frame, 0.5)
        apart(five, ctag, 0.1)
        drows = drawer_rows(cab)

        def into(chip_, name):
            """The lecture's chip slides right into its drawer (fading as it arrives) while the
            drawer fades in under it."""
            tgt = drows[name].get_center()
            return [FadeOut(chip_, target_position=tgt, scale=0.9),
                    *cab.parts_in(name, anim=lambda m: FadeIn(m, shift=RIGHT * 0.5))]

        def slide_in(name):
            return cab.parts_in(name, anim=lambda m: FadeIn(m, shift=LEFT * 0.6))

        ev.move_to([0, 0.5, 0])                          # it opens the scene in the middle
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ev, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("a 40-guest event")
            self.play(flash(ev.phrase, TURN, 1.06), run_time=0.7)
            vo.wait_until("The lecture splits")
            self.play(ev.animate.move_to(ev_home), run_time=0.6)
            self.play(FadeIn(lr), FadeIn(ctag, shift=DOWN * 0.1),       # the lecture tag comes with its picture
                      LaggedStart(FadeIn(st_chip), FadeIn(lt_chip), lag_ratio=0.4), run_time=0.8)
            self.play(FadeIn(cab), FadeIn(ill), run_time=0.6)
            vo.wait_until("here that's saved memory")
            self.play(*into(lt_chip, "memory"), run_time=0.9)
            vo.wait_until("and history")
            self.play(*into(st_chip, "history"), run_time=0.8)
            vo.wait_until("plus tasks")
            self.play(*slide_in("tasks"), FadeOut(ctag), run_time=0.5)
            vo.wait_until("approvals")
            self.play(*slide_in("approval"), run_time=0.45)
            vo.wait_until("and the audit")
            self.play(*slide_in("audit"), run_time=0.45)
            vo.wait_until("five kinds of state")
            self.play(GrowFromEdge(brace, RIGHT), FadeIn(five, shift=RIGHT * 0.15), run_time=0.6)

        # ========================================================== 1 · which drawer can authorize an action?
        c522 = top_chip(R522, where="README.md · line 522")
        apart(c522, ev, 0.05)
        apart(c522, cab.frame, 0.3)
        apart(c522, lr, 0.05)
        hnd = hand(S.GREY, h=0.5)
        grip = DOWN * 0.1                 # the palm on the handle, the fingers above it

        def at_handle(name):
            return cab.handle_point(name) + grip

        hnd.move_to(at_handle("tasks"))
        key = key_glyph(0.3, TURN).rotate(-PI / 2)          # shaft down, the bow on top
        kh = cab.keyhole()
        key.shift(kh.get_center() - key.get_bottom())
        apart(key, drows["memory"], 0.1)
        trials = ("tasks", "history", "memory", "audit")
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(c522, shift=DOWN * 0.1), FadeIn(hnd, shift=LEFT * 0.2), run_time=0.45)
            for i, name in enumerate(trials):
                if i:
                    self.play(hnd.animate.move_to(at_handle(name)), run_time=0.22)
                self.play(Succession(Rotate(hnd, -0.45, about_point=hnd.palm.get_center()),
                                     Rotate(hnd, 0.45, about_point=hnd.palm.get_center())),
                          cab.try_open(name, run_time=0.42), run_time=0.42)
                self.play(*shut_grey(cab, name), run_time=0.2)
            vo.wait_until("Only one")
            self.play(FadeOut(hnd, shift=RIGHT * 0.2), FadeIn(key, shift=DOWN * 0.3), run_time=0.4)
            vo.wait_until("the approval drawer")
            self.play(key.animate.stretch(0.25, 0), run_time=0.25)
            self.play(key.animate.stretch(4.0, 0), run_time=0.25)
            self.play(cab.open("approval"), key.animate.shift(RIGHT * 0.7), run_time=0.55)

        # ========================================================== 2 · step 1: act 4, memory first, no memory tool
        tr = tracker("Act4", 1)
        t = term(container=True, rows=13)
        ft = frame_tags(t, nokey_tag())
        band_c = np.array([BAND_RIGHT - cab.frame.width * BAND_K / 2, 3.51 - cab.frame.height * BAND_K / 2, 0])
        offs = {k: drows[k].get_center() - g.face.get_center() for k, g in cab.dr.items()}
        mdl = label("the model: no memory tool", CAPTION, S.GREY, t2c={"the model": CLOUD})
        bhand = hand(CLOUD, h=0.5)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(c522, ev, brace, five)), FadeOut(lr), FadeOut(key), FadeOut(ill),
                      FadeIn(tr, shift=DOWN * 0.25), run_time=0.5)
            self.play(cab.close("approval"), *regreen(cab, trials), run_time=0.4)
            self.play(FadeOut(VGroup(*drows.values())), run_time=0.3)
            for k, g in cab.dr.items():               # out of the drawers: they must not snap back
                g.remove(drows[k])
                g.title.set_color(HARNESS)
                g.detail.set_color(INK)
            self.play(cab.animate.scale(BAND_K).move_to(band_c), run_time=0.6)
            inside(cab)
            assert cab.frame.get_bottom()[1] > t.box.get_top()[1] + 0.08, (cab.frame.get_bottom(), t.box.get_top())
            assert cab.frame.get_left()[0] > tr.get_right()[0] + 0.3
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(ft, shift=DOWN * 0.1), run_time=0.4)
            cmd = type_cmd(self, t, C40.cmd, 0.7)
            lt = beside(live_tag(), t, cmd, buff=0.35)
            pin(self, cmd, lt, run_time=0.3)
            out = show(self, t, C40, (2, 4), 5, (6, 8), C40.as401(9, short=True), wrap=True, run_time=0.6)
            assert len(t.lines) == 13, len(t.lines)
            r4 = item_rows(out, 2)
            blank = item_rows(out, 3)[0]
            r8 = item_rows(out, 6)
            vo.wait_until("the harness prints")
            host = slim_tag("loaded by the host · before any model call", HARNESS)
            place(host, left=grid_x0(r4[0]), cy=blank.strut.get_center()[1])
            self.play(recolor(wrapped_glyphs(r4, MEM_A), HARNESS), recolor(wrapped_glyphs(r4, MEM_B), HARNESS),
                      run_time=0.4)
            pin(self, blank, host, run_time=0.4)
            for anchor, names in TOOL_BEATS:
                vo.wait_until(anchor)
                self.play(LaggedStart(*[recolor(wrapped_glyphs(r8, n), HARNESS) for n in names], lag_ratio=0.35),
                          run_time=0.3 + 0.12 * len(names))
            vo.wait_until("No tool writes memory")
            gh = ghost_chip("a memory-write tool")
            beside(gh, t, r8[-1], buff=0.45)
            gx = strike(gh.text, ERR, 3.5)                 # drawn where the chip now is
            pin_all(self, r8[-1], [gh, gx], [LaggedStart(FadeIn(gh, shift=LEFT * 0.1), Create(gx), lag_ratio=0.55)],
                    run_time=0.55)
            # the terminal shrinks to the strip while the cabinet grows back above it
            fit(self, t, 3, keep=[cmd, r4[0], r8[-1]], tags=list(ft), run_time=0.8,
                extra=[cab.animate.scale(1 / BAND_K).move_to(CAB2_C)])
            for k, g in cab.dr.items():
                drows[k].move_to(g.face.get_center() + offs[k])
            rows_back = VGroup(*drows.values())
            place(ill, left=cab.frame.get_right()[0] + 0.25, top=cab.frame.get_top()[1])
            mem_spot = cab.handle_point("memory")
            bhand.move_to(mem_spot + RIGHT * 0.55 + DOWN * 0.1)
            place(mdl, left=cab.frame.get_right()[0] + 0.3, cy=mem_spot[1])
            for m in (cab, ill, bhand, mdl):
                inside(m)
            assert cab.frame.get_bottom()[1] > STRIP_TOP + 0.04 and cab.frame.get_top()[1] < tr.get_bottom()[1] - 0.05
            apart(ill, mdl, 0.15)
            apart(rows_back, bhand, 0.1)
            self.play(FadeIn(rows_back), FadeIn(ill), FadeIn(bhand, shift=LEFT * 0.25), run_time=0.4)
            self.remove(rows_back)
            for k, g in cab.dr.items():
                g.add(drows[k])
            self.play(bhand.animate.shift(LEFT * 0.55), run_time=0.3)
            self.play(Succession(Rotate(bhand, -0.4, about_point=bhand.palm.get_center()),
                                 Rotate(bhand, 0.4, about_point=bhand.palm.get_center())),
                      FadeIn(mdl, shift=LEFT * 0.1), run_time=0.5)

        # ========================================================== 3 · what to look for, with a key
        q460 = quote_card(460, lines=Q460, wrap=62)
        place(q460, left=-SAFE, top=2.82)
        q471 = quote_card(471, lines=Q471, wrap=62)
        place(q471, left=-SAFE, top=q460.get_bottom()[1] - 0.22)
        assert q471.get_bottom()[1] > STRIP_TOP + 0.12, (q471.get_bottom(), STRIP_TOP)
        assert q460.get_top()[1] < tr.get_bottom()[1] - 0.05
        sb = StockBar()
        place(sb, right=SAFE, cy=q460.frame.get_center()[1])
        apart(sb, q460, 0.3)
        inside(sb)
        rows460 = q460.rows
        assert len(rows460) == 4, [r.text for r in rows460]
        u_brief = VGroup(*[under(r, TURN, 3) for r in rows460[:2]])
        u_stock = under(rows460[3], TURN, 3)
        u471 = [under(r, TURN, 3) for r in q471.rows]
        with self.voiceover(SAY[3]) as vo:
            self.wait(0.8)                                # the hand's moment, held into this block
            self.play(FadeOut(VGroup(cab, ill, bhand, mdl)), run_time=0.4)
            self.play(FadeIn(q460, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("1,000 grams each")
            self.play(Create(u_brief), run_time=0.6)
            vo.wait_until("and 1,200 of")
            self.play(FadeIn(VGroup(sb.outline, sb.name, sb.need)), run_time=0.5)
            vo.wait_until("The shop has only")
            self.play(Create(u_stock), GrowFromEdge(sb.bar, LEFT), FadeIn(sb.have, shift=UP * 0.05), run_time=0.8)
            vo.wait_until("300 short")
            self.play(Create(sb.gap), FadeIn(sb.short, shift=UP * 0.05), run_time=0.6)
            vo.wait_until("A finished task")
            self.play(FadeIn(q471, shift=UP * 0.1), run_time=0.5)
            self.play(Create(u471[0]), run_time=0.4)
            vo.wait_until("and shop stock")
            self.play(Create(u471[1]), run_time=0.4)

        # ========================================================== 4 · approval mode: one tool pauses
        p72 = src_panel(PT, 72, 75, wrap=True)
        place(p72, cx=0, top=2.82)
        assert p72.get_top()[1] < tr.get_bottom()[1] - 0.05
        b72 = SurroundingRectangle(p72.span(72, APPROVAL72), color=TURN, buff=0.05, stroke_width=3,
                                   corner_radius=0.04)
        rl = Rail(mini=True)
        rl.scale(0.7)
        place(rl, cx=-FREEZE_X, top=-0.75)
        tok = cart_token(scale=0.6)
        tok.move_to(rl.spot("pairings"))
        lab_rev = label(RAIL_SHORT["review"], CAPTION, INK).next_to(rl.station("review").frame, DOWN, buff=0.1)
        card = tool_card()
        place(card, cx=FREEZE_X, cy=rl.get_center()[1])
        lock = padlock(0.5, S.GREY)
        lock.move_to(card.lock_spot())
        assert lock.get_left()[0] > card.text.get_right()[0] + 0.1
        lift = UP * lock.body.height * 0.35
        lock.shackle.shift(lift)                  # open: it clicks shut on the card
        cap3 = label("act 3: a workflow pauses", CAPTION, INK)
        cap4 = label("act 4: one tool pauses", CAPTION, INK)
        place(cap3, cx=-FREEZE_X, top=lab_rev.get_bottom()[1] - 0.18)
        place(cap4, cx=FREEZE_X, cy=cap3.get_center()[1])
        fw = tag("the framework pauses", TOOL)
        place(fw, cx=0, cy=(p72.get_bottom()[1] + rl.get_top()[1]) / 2)
        ill4 = illustration_tag()
        place(ill4, left=-SAFE, cy=fw.get_center()[1])
        for m in (p72, rl, card, cap3, cap4, fw, ill4, lab_rev):
            inside(m)
        apart(fw, p72, 0.08)
        apart(fw, rl, 0.08)
        apart(fw, card, 0.08)
        apart(ill4, fw, 0.3)
        apart(ill4, rl, 0.08)
        apart(rl, card, 0.4)
        apart(cap3, cap4, 0.4)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(q460, q471, u_brief, u_stock, *u471, sb)), FadeOut(VGroup(t, ft)), run_time=0.5)
            self.play(FadeIn(p72, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(card, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("approval mode always require")
            self.play(Create(b72), run_time=0.45)
            vo.wait_until("so the framework pauses")
            self.play(FadeIn(lock, shift=DOWN * 0.25), run_time=0.35)
            self.play(lock.shackle.animate.shift(-lift), FadeIn(fw, scale=0.95), run_time=0.35)
            vo.wait_until("Act 3 paused")
            self.play(FadeIn(rl), FadeIn(tok), FadeIn(lab_rev), FadeIn(ill4), run_time=0.45)
            self.play(*rl.freeze("review"), FadeIn(cap3, shift=UP * 0.05), run_time=0.5)
            vo.wait_until("this pauses one tool")
            self.play(card.frame.animate.set_stroke(AMBER, 4), card.tint.animate.set_fill(AMBER, 0.2),
                      FadeIn(cap4, shift=UP * 0.05), run_time=0.5)

        # ========================================================== 5 · the scripted extra: what approve prints
        t5 = term(container=True, rows=12)
        ft5 = frame_tags(t5, scripted_tag())
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(p72, b72, card, lock, rl, tok, lab_rev, cap3, cap4, fw, ill4)), run_time=0.5)
            self.play(caption_extra(tr, True), FadeIn(t5, shift=UP * 0.2), FadeIn(ft5, shift=DOWN * 0.1), run_time=0.5)
            cmd5 = type_cmd(self, t5, FIX_CMD, 1.0)
            # the command starts under the prompt (type_cmd: it fits a row of its own), so the
            # tags sit on the prompt row: `extra` after the prompt, TEST decision over the flag
            r_p, r_dec = cmd5.rows[0], cmd5.rows[-1]
            assert r_p.text.strip() == P_CTR and r_dec.text.strip() == FIX_CMD, (r_p.text, r_dec.text)
            dec = substring(r_dec, "--email-decision approve")
            ol = SurroundingRectangle(dec, color=TURN, buff=0.05, stroke_width=2.5, corner_radius=0.05)
            pin(self, r_dec, ol, anim=Create(ol), run_time=0.3)
            et = beside(extra_tag(), t5, r_p, buff=0.35)
            tt = test_tag()
            tt.move_to([0, r_p.strut.get_center()[1], 0]).align_to(ol, RIGHT)
            assert tt.get_left()[0] > et.get_right()[0] + 0.3 and tt.get_right()[0] < t5.box.get_right()[0] - 0.12
            pin(self, r_p, et, run_time=0.3)
            pin(self, r_p, tt, run_time=0.3)
            o5 = show(self, t5, C42, (51, 53), (55, 60), run_time=0.6)
            r52, r55, r57, r58 = o5[1], o5[3], o5[5], o5[6]
            vo.wait_until("the vendor address")
            self.play(recolor(r52.glyphs, LOOKUP), run_time=0.4)
            vo.wait_until("and a body written by code")
            wc = slim_tag("written by code, not the model")
            beside(wc, t5, r55, buff=0.4)
            pin(self, r55, wc, run_time=0.4)
            self.play(recolor(r57.glyphs, TURN), run_time=0.4)
            vo.wait_until("nut allergy included")
            self.play(recolor(r58.glyphs, HARNESS), run_time=0.4)
            self.play(Indicate(substring(r58, "nuts."), color=HARNESS, scale_factor=1.15), run_time=0.5)
            vo.wait_until("Then:")                        # the output scrolls on in two steps
            o6 = show(self, t5, C42, 62, 65, wrap=True, run_time=0.5)
            r62, r65 = item_rows(o6, 0), item_rows(o6, 1)
            vo.wait_until("status saved")
            self.play(recolor(wrapped_glyphs(r65, SAVED), HARNESS), run_time=0.4)
            vo.wait_until("email transmitted no")
            self.play(recolor(wrapped_glyphs(r65, SENT), HARNESS), run_time=0.4)
            vo.wait_until("and the file path")
            o7 = show(self, t5, C42, 83, 91, 92, wrap=True, run_time=0.4)
            r83, r91, r92 = (item_rows(o7, k) for k in range(3))
            assert len(t5.lines) == 12 and t5.lines[0] is r62[0], [ln.text for ln in t5.lines]
            self.play(recolor(wrapped_glyphs(r91, HTML_PATH), LOOKUP), run_time=0.5)

        # ========================================================== 6 · the harmless warning; the map; your turn
        c837 = top_chip(R837, where="README.md · line 837 (excerpt)")
        assert c837.get_bottom()[1] > t5.box.get_top()[1] + 0.05 and c837.get_top()[1] < tr.get_bottom()[1] - 0.02
        u62 = [under(r.glyphs, TURN, 3) for r in r62]
        hm = harmless_tag()
        beside(hm, t5, r62[-1], buff=0.4)
        lr22 = lref("22")
        mm = BoundaryMini(upto=3)
        tc = turn_card([Prose("with your key:"), C40.cmd, (Prose("type approve or decline when asked"), S.GREY),
                        (FIX_CMD, "extra"), (Prose("no key: offline · free"), HARNESS),
                        (Prose("live · billed per token"), COST)])
        place(tc, cx=0, cy=-0.3)
        inside(tc)
        assert tc.get_top()[1] < tr.get_bottom()[1] - 0.1
        with self.voiceover(SAY[6]) as vo:
            self.play(LaggedStart(*[Create(u) for u in u62], lag_ratio=0.25), run_time=0.7)
            for r, u in zip(r62, u62):                   # the underlines belong to their rows
                self.remove(u)
                r.add(u)
            vo.wait_until("the README predicts it")
            self.play(FadeIn(c837, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("and it's harmless")
            pin(self, r62[-1], hm, run_time=0.4)
            vo.wait_until("Trust the authoritative block")
            self.play(recolor(r83[0].glyphs, HARNESS), run_time=0.4)
            self.play(recolor(r92[0].glyphs, HARNESS), Circumscribe(VGroup(r83[0], r92[0]), color=HARNESS,
                                                                     fade_out=True, stroke_width=3), run_time=0.7)
            vo.wait_until("Pause and run step 1")
            self.play(FadeOut(VGroup(t5, ft5)), FadeOut(c837), caption_extra(tr, False), run_time=0.5)
            self.play(FadeIn(mm), FadeIn(lr22), run_time=0.5)
            self.play(mm.light("tools"), run_time=0.3)
            cap_t = mm.caption("Tools ← approval on save")
            self.play(mm.add_bar("tools"), FadeIn(cap_t, shift=LEFT * 0.1), run_time=0.5)
        self.wait(1.6)
        self.play(FadeOut(cap_t), run_time=0.3)
        self.play(FadeOut(mm), FadeOut(lr22), run_time=0.4)
        self.play(FadeIn(tc, scale=0.97), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tc, tr)), run_time=0.8)
        self.wait(0.3)
