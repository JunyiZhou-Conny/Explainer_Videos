"""S03 · Everything the model knows is in the envelope (Colab · Cheese Quiz › Managing LLM Inputs).
Lecture: 41.

Beats (script.md "## S03", one voiceover block each):
0. TRACKER CQ-Inputs 1. An excerpt chip (header `Cheese Quiz · cell 35 · line 1 (excerpt)`): "LLMs
   are stateless functions." V2: a small envelope slides to the BLUE `gpt-4o` chip, which opens it
   and answers (BLUE answer bars); the envelope crumples away and a fresh empty envelope arrives,
   caption "every call: a fresh envelope". (S02 ends on an empty frame, so there is no mini-map
   to hide.)
1. LECTURE 41. One tracker step at a time (1 → 7): each step's sheet slides in glowing YELLOW, in
   slide 41's words (user prompt · system prompt · contexts: retrieved documents · user sessions:
   earlier turns · user preferences: a profile from past sessions · contexts: tool outputs ·
   output schema); step 4 drops the documents, step 5 keeps 2 of the 4 turns, step 6 drops the
   turns. The BLUE "top pick" card beside the envelope Transforms to each step's pick (recorded).
2. The pick card opens into a column of the seven picks (c38:10 … c44:10, wrapped), each joined
   by a thin line to its step badge; a YELLOW ring lights each pick as it is named. Tag
   "recorded · the staff's last saved run".
3. TRACKER CQ-Inputs 4. CODE(cell-41.py: 18–22) at the bottom, a fresh 3-slot envelope above it
   holding the system prompt; lines 20, 21, 22 highlight GREY and fly in as sheets onto one pile;
   the panel Transforms into CODE(cell-41.py: 22–25), line 23 flies onto the pile and line 24 (the
   question) into the last slot. Caption "memory = paper you put back, every call".
4. The sheets regroup into two GREY-framed blocks under slide 41's headers: "Instructions: system
   & user prompts · contexts · output schema" (five sheets) and "Memory: user sessions · user
   preferences" (the pile becomes "user sessions: earlier turns"). A GREY dashed chip "Lecture 7:
   context engineering".
5. The lecture tag leaves. TRACKER CQ-Inputs 2. CODE(cell-39.py: 16–21) top left, a YELLOW
   "Spot it" card beside it (no timer); lines 19–20 get YELLOW bars. After the SAY, 4 s with the
   code on screen while the card's underline draws.
6. A step-2 envelope (system prompt / user prompt, each with its role label) below the code:
   the two role labels trade places and both sheets turn RED; the role values in lines 19–20 are
   ringed RED.
7. `erratum` tag on the code panel; the labels trade back (GREEN check); under the code panel a
   GREEN fix chip (header "cell 39 · lines 19–20 · your edit") and the GREY tag "your step 2
   answer will differ from the saved one"; caption "swap the roles, then compare · steps 3–7 are
   right". The envelope gives way to the static GREY ▶ your turn card "Managing LLM Inputs: swap
   the roles in step 2 · run steps 1–7", last line GOLD "paid per call". Hold 2 s.
8. TRACKER CQ-Inputs 6. Step 6's envelope (user prompt, system prompt, profile, tool outputs);
   the tool-outputs sheet glows YELLOW with the GREY tag "simulated · pasted in by the code (cell
   43 · line 6)"; a GREY "?" chip "how does a model ask for a tool?"; a GREY chip "keep the Cheese
   Quiz open · its Tools, MCP section comes after ADK". Everything fades: empty frame.
"""

import re

import numpy as np
from common import (
    CLOUD,
    COST,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MONO,
    NARRATION,
    TURN,
    Prose,
    _with_header,
    answer_bars,
    capture,
    card_rows,
    concept_box,
    erratum_tag,
    excerpt,
    excerpt_chip,
    grey_tag,
    lref,
    model_chip,
    mtext,
    note,
    ring,
    saved_run_tag,
    src_panel,
    switch_section,
    turn_card,
)
from common import Envelope as EnvelopePiece
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    FadeTransform,
    LaggedStart,
    Line,
    ManimColor,
    ReplacementTransform,
    Transform,
    UpdateFromAlphaFunc,
    VGroup,
    Write,
    interpolate_color,
    linear,
    rush_into,
)

from explainer import style as S
from explainer.devops import box, check_mark, chip, label, step_badge
from explainer.scene import VoiceScene

SAY = NARRATION["S03"]
CQ = "colab/cheese-quiz"

# ------------------------------------------------------------------ the real sources
_C35 = excerpt(f"{CQ}/cell-35.md", 1, 1)
STATELESS = "LLMs are stateless functions."
assert _C35.startswith(STATELESS), _C35


def _pick(cell: int, n: int, sub: str) -> str:
    """An exact sub-string of the staff's saved output (expected/colab-cheese-quiz-cNN-*.txt)."""
    line = capture(f"colab-cheese-quiz-c{cell}", "expected").line(n)
    assert sub in line, (cell, n, line)
    return sub


PICKS = [[_pick(38, 10, "Cheddar")], [_pick(39, 10, "American Cheese")],
         [_pick(40, 10, "American Cheese")], [_pick(41, 8, "mild cheddar and mozzarella")],
         [_pick(42, 8, "Havarti")], [_pick(43, 8, "Whole Foods Mild Cheddar")]]
_L44 = capture("colab-cheese-quiz-c44", "expected").line(10).strip()
assert _L44 == '"top_recommendation": "Whole Foods Mild Cheddar",', _L44
_cut = _L44.index(" ")
PICKS.append([_L44[:_cut], "↪ " + _L44[_cut + 1:]])        # c44 line 10, wrapped (house ↪)

# what each step's cell sends (the sheets): checked against the cells
_C38, _C39, _C40 = (f"{CQ}/cell-{n}.py" for n in (38, 39, 40))
_C41, _C42, _C43, _C44 = (f"{CQ}/cell-{n}.py" for n in (41, 42, 43, 44))
assert excerpt(_C38, 9, 9).strip() == '{"role": "user", "content": user_prompt}'
assert "CHEESE_KNOWLEDGE_BASE" in excerpt(_C40, 37, 37)                      # step 3: documents
assert excerpt(_C41, 18, 25).count('"role": "assistant"') == 2               # step 4: 4 turns
assert excerpt(_C42, 49, 54).count('"role": "assistant"') == 1               # step 5: 2 turns
assert "{memory_context}" in excerpt(_C42, 45, 45)                           # step 5: the profile
assert "tool_outputs" in excerpt(_C43, 50, 50) and "assistant" not in excerpt(_C43, 56, 59)
assert '"json_schema"' in excerpt(_C44, 35, 35)                              # step 7: the schema
assert excerpt(f"{CQ}/cell-43.py", 6, 6).startswith("# Simulated tool functions")

TURNS = []                                       # cell 41 lines 20-23: the earlier turns
for _i, _n in enumerate(range(20, 24), start=1):
    _role = re.search(r'"role": "(\w+)"', excerpt(_C41, _n, _n)).group(1)
    TURNS.append((_n, f"turn {_i} · {_role}"))
assert [t for _, t in TURNS] == ["turn 1 · user", "turn 2 · assistant", "turn 3 · user",
                                  "turn 4 · assistant"]
assert '"role": "system"' in excerpt(_C41, 19, 19)
assert excerpt(_C41, 24, 24).strip() == '{"role": "user", "content": user_prompt}'

_L19, _L20 = excerpt(_C39, 19, 19).strip(), excerpt(_C39, 20, 20).strip()
assert _L19 == '{"role": "user", "content": system_prompt},', _L19
assert _L20 == '{"role": "system", "content": user_prompt}', _L20
FIX = [_L19.replace('"user"', '"system"'), _L20.replace('"system"', '"user"')]
assert FIX == ['{"role": "system", "content": system_prompt},', '{"role": "user", "content": user_prompt}']

# slide 41's words on the sheets (script.md S03)
W_USER, W_SYS = "user prompt", "system prompt"
W_DOCS, W_TURNS = "contexts: retrieved documents", "user sessions: earlier turns"
W_PROF, W_TOOLS = "user preferences: a profile from past sessions", "contexts: tool outputs"
W_SCHEMA = "output schema"

# ------------------------------------------------------------------ layout
ENV_C = np.array([-3.25, 0.0, 0])          # the main envelope (6.4 wide, 5 slots: y -1.67..1.67)
CHIP_C = np.array([3.4, 1.2, 0])           # the gpt-4o chip
CARD_C = np.array([3.4, -0.55, 0])         # the top-pick card
COL_X = 0.55                               # the picks column: badge x; chips start at COL_X + 0.7


def place(env, center):
    """Put the envelope's body (not its bounding box, which holds the hidden open flap) at center."""
    env.shift(np.array(center) - env.parts["body"].get_center())
    return env


def sheet_of(env, text, hue=S.GREY):
    """A sheet for `env` remembering its colour (.hue) for glow on / off."""
    s = env.sheet(text, hue)
    s.hue = hue
    return s


def glow(s):
    s.frame.set_stroke(TURN, 4)
    return s


def unglow(s):
    """The glow fades back to the sheet's colour. Stroke only (an .animate copy of the frame would
    pin its points and fight a restack that moves the sheet in the same play)."""
    c0, c1 = ManimColor(TURN), ManimColor(s.hue)
    return UpdateFromAlphaFunc(s.frame, lambda m, a: m.set_stroke(interpolate_color(c0, c1, a),
                                                                   4 - 2 * a))


def pick_text(rows, center):
    """The pick (mono, 20 pt), one or two rows (a GREY ↪ on the continuation)."""
    lines = VGroup(*[S.text(r, 20, INK, font=MONO, t2c={"↪": S.GREY}) for r in rows])
    lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(center)
    return lines


def pick_frame():
    """The BLUE top-pick card (frame + GREY header); the text is a separate mobject."""
    fr = box(5.6, 1.5, CLOUD, fill=S.BG, fill_opacity=0.95, radius=0.14).move_to(CARD_C)
    head = note("top pick").move_to(fr.get_top() + DOWN * 0.24)
    g = VGroup(fr, head)
    g.frame = fr
    return g


def role_label(role: str):
    lbl = VGroup(note("role"), S.text(f'"{role}"', 20, INK, font=MONO)).arrange(RIGHT, buff=0.12)
    return lbl


def to_spot(lbl, sheet):
    """Where a role label sits on `sheet`: right-aligned, 0.15 from the edge."""
    x = sheet.frame.get_right()[0] - 0.15 - lbl.width / 2
    return np.array([x, sheet.frame.get_center()[1], 0])


class Envelope(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ============================================================ 0 · a fresh envelope
        with self.voiceover(SAY[0]) as vo:
            tr = switch_section(self, None, "CQ-Inputs", 1)
            gpt = model_chip("gpt-4o").move_to(CHIP_C)
            env1 = place(EnvelopePiece(width=2.6, slots=1), [-3.25, 0.2, 0])
            q1 = sheet_of(env1, W_USER, LOOKUP)
            q1.move_to(env1.slot_point(0))
            env1.sheet_group.add(q1)
            env1.sheets.append(q1)
            self.play(FadeIn(gpt), FadeIn(env1, shift=RIGHT * 0.4), run_time=0.8)
            vo.wait_until("LLMs are stateless")
            ec = excerpt_chip(STATELESS, "Cheese Quiz · cell 35 · line 1 (excerpt)", line=_C35)
            ec.move_to([0, 0, 0]).align_to([-6.4, 0, 0], LEFT).align_to([0, 2.72, 0], UP)
            self.play(FadeIn(ec, shift=DOWN * 0.15), run_time=0.6)
            self.play(env1.animate.shift([1.0, CHIP_C[1], 0] - env1.parts["body"].get_center()),
                      run_time=1.0)
            vo.wait_until("Every call is a fresh envelope")
            bars = answer_bars(3, w=1.9, color=CLOUD).move_to(CARD_C + UP * 0.5)
            down = Arrow(gpt.get_bottom(), bars.get_top(), buff=0.12, color=S.GREY, stroke_width=3,
                         tip_length=0.16, max_tip_length_to_length_ratio=0.3)
            self.play(*env1.open(), run_time=0.4)
            self.play(Create(down), FadeIn(bars, shift=DOWN * 0.15), run_time=0.6)
            self.play(env1.animate(rate_func=rush_into).scale(0.08).rotate(PI * 0.7).set_opacity(0),
                      run_time=0.6)
            self.remove(env1)
            env = place(EnvelopePiece(width=6.4, slots=5), ENV_C)
            cap1 = note("every call: a fresh envelope").next_to(env.parts["body"], DOWN, buff=0.3)
            self.play(FadeIn(env, shift=RIGHT * 0.6), FadeIn(cap1), FadeOut(bars), FadeOut(down),
                      run_time=0.8)
            vo.wait_until("and the model knows only")
            self.play(env.parts["body"].animate.set_stroke(TURN, 4), run_time=0.4)
            self.play(env.parts["body"].animate.set_stroke(S.GREY, 3), run_time=0.5)

        # ============================================================ 1 · seven steps, seven inputs
        with self.voiceover(SAY[1]) as vo:
            ref = lref("41")
            a_in = Arrow([ENV_C[0] + 3.3, CHIP_C[1], 0], gpt.get_left(), buff=0.1, color=S.GREY,
                         stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.3)
            card = pick_frame()
            a_out = Arrow(gpt.get_bottom(), card.frame.get_top(), buff=0.1, color=S.GREY,
                          stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.3)
            rec = saved_run_tag().next_to(card, DOWN, buff=0.25)
            ptxt = pick_text(PICKS[0], card.frame.get_center() + DOWN * 0.16)
            s_user = glow(sheet_of(env, W_USER, LOOKUP))
            env.add_sheet(self, s_user, start=env.slot_point(0) + LEFT * 1.2, run_time=0.7,
                          extra=[FadeOut(ec), FadeIn(ref), Create(a_in)])
            self.play(Create(a_out), FadeIn(card), FadeIn(ptxt), FadeIn(rec), run_time=0.7)
            vo.wait_until("keeps the model and question fixed")
            rings = VGroup(ring(gpt, TURN), ring(s_user.frame, TURN, buff=0.05))
            self.play(Create(rings), unglow(s_user), run_time=0.6)
            vo.wait_until("and changes the inputs")
            self.play(FadeOut(rings), run_time=0.4)
            last = None

            def step(k, sheet=None, drop=None, extra=()):
                """Tracker to step k: `drop` slides out, `sheet` slides in glowing, the pick changes."""
                nonlocal ptxt, last
                new = pick_text(PICKS[k - 1], card.frame.get_center() + DOWN * 0.16)
                anims = [tr.goto(k), ReplacementTransform(ptxt, new), *extra]
                if last is not None:
                    anims.append(unglow(last))
                ptxt = new
                if drop is not None:
                    env.remove_sheet(self, drop, shift=LEFT * 1.0, run_time=0.5, extra=anims)
                    anims = []
                if sheet is not None:
                    glow(sheet)
                    tgt = env.slot_point(len(env.sheets))
                    env.add_sheet(self, sheet, start=tgt + LEFT * 1.2, run_time=0.6, extra=anims)
                    last = sheet

            vo.wait_until("A system prompt")
            s_sys = sheet_of(env, W_SYS)
            step(2, s_sys)
            vo.wait_until("retrieved documents")
            s_docs = sheet_of(env, W_DOCS)
            step(3, s_docs)
            vo.wait_until("earlier turns")
            s_turns = sheet_of(env, W_TURNS)
            n4 = note("4 turns")
            n4.move_to(s_turns.frame.get_right() + LEFT * (0.2 + n4.width / 2))
            s_turns.add(n4)
            step(4, s_turns, drop=s_docs)
            vo.wait_until("a profile from past sessions")
            s_prof = sheet_of(env, W_PROF)
            n2 = note("2 turns").move_to(n4, aligned_edge=RIGHT)
            step(5, s_prof, extra=[Transform(n4, n2)])           # n4 stays the sheet's member
            vo.wait_until("a tool's output")
            s_tools = sheet_of(env, W_TOOLS)
            step(6, s_tools, drop=s_turns)
            vo.wait_until("an output schema")
            s_schema = sheet_of(env, W_SCHEMA)
            step(7, s_schema)

        # ============================================================ 2 · the seven picks
        with self.voiceover(SAY[2]) as vo:
            rows = []
            y = 2.45
            for k, pk in enumerate(PICKS, start=1):
                t = pick_text(pk, [0, 0, 0])
                fr = box(t.width + 0.44, t.height + 0.26, CLOUD, fill=S.BG, fill_opacity=0.0,
                         radius=0.12)
                x0 = COL_X + 0.7
                fr.move_to([x0 + fr.width / 2, y - fr.height / 2, 0])
                t.move_to(fr)
                bd = step_badge(k, S.GREY, size=20, radius=0.2).move_to([COL_X, fr.get_center()[1], 0])
                ln = Line(bd.get_right(), fr.get_left(), color=S.GREY_DARK, stroke_width=2)
                rows.append(VGroup(bd, ln, fr, t))
                y -= fr.height + 0.13
            col_tag = saved_run_tag().next_to(VGroup(*rows), DOWN, buff=0.3).align_to(rows[0], LEFT)
            # the card's JSON pick becomes row 7's text; the rest of the column fades in
            self.play(FadeOut(gpt), FadeOut(a_in), FadeOut(a_out), FadeOut(card), FadeOut(rec),
                      unglow(s_schema), ReplacementTransform(ptxt, rows[6][3]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r[:3] if k == 6 else r, shift=LEFT * 0.2)
                                    for k, r in enumerate(rows)], lag_ratio=0.12),
                      FadeIn(col_tag), run_time=1.0)
            hl = None
            for k, phrase in ((0, "cheddar, American"), (1, "American, then"),
                              (3, "then mild cheeses for kids"), (4, "then Havarti"),
                              (5, "Then a mild cheddar"), (6, "and finally the same pick")):
                vo.wait_until(phrase)
                tgt = VGroup(rows[k][0], rows[k][2])
                if k == 1:
                    tgt = VGroup(rows[1][0], rows[1][2], rows[2][0], rows[2][2])
                new = ring(tgt, TURN, buff=0.08, stroke=3)
                if hl is None:
                    self.play(Create(new), run_time=0.5)
                else:
                    self.play(ReplacementTransform(hl, new), run_time=0.5)
                hl = new
            self.wait(0.6)
            self.play(FadeOut(hl), run_time=0.4)

        # ============================================================ 3 · memory is paper you put back
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(env), FadeOut(cap1), *[FadeOut(r) for r in rows], FadeOut(col_tag),
                      tr.goto(4), run_time=0.7)
            p41a = src_panel(_C41, 18, 22, wrap=True)
            _with_header(p41a, "Cheese Quiz · cell 41 · lines 18–22",
                         subtitle="Step 4: Adding Short-term Memory")
            p41a.align_to([-6.45, 0, 0], LEFT).align_to([0, -3.56, 0], DOWN)
            env4 = EnvelopePiece(width=4.4, slots=3, pitch=0.46, margin=0.32)
            place(env4, [6.45 - 2.2, 2.72 - env4.env_h / 2, 0])
            s4_sys = sheet_of(env4, W_SYS)
            s4_sys.move_to(env4.slot_point(0))
            env4.sheet_group.add(s4_sys)
            env4.sheets.append(s4_sys)
            self.play(FadeIn(p41a, shift=UP * 0.3), FadeIn(env4, shift=DOWN * 0.2), run_time=0.8)
            pile = []

            def fly(panel, n, text, slot, offset=0):
                """Line n gets a GREY bar; a sheet flies from it into `slot` of the envelope."""
                bar = panel.bar(n, S.GREY, 0.3)
                self.play(FadeIn(bar), run_time=0.2)
                sh = sheet_of(env4, text, LOOKUP if text == W_USER else S.GREY)
                sh.move_to(env4.slot_point(slot) + np.array([0.06 * offset, 0.02 * offset, 0]))
                self.play(FadeTransform(bar.copy(), sh), run_time=0.45)
                self.remove(sh)
                env4.sheet_group.add(sh)
                return bar, sh

            vo.wait_until("The earlier turns")
            bars4 = []
            for i, (n, text) in enumerate(TURNS[:3]):
                b, sh = fly(p41a, n, text, 1, i)
                bars4.append(b)
                pile.append(sh)
                if i == 0:
                    env4.sheets.append(sh)
            p41b = src_panel(_C41, 22, 25, wrap=True)
            _with_header(p41b, "Cheese Quiz · cell 41 · lines 22–25",
                         subtitle="Step 4: Adding Short-term Memory")
            p41b.align_to(p41a, LEFT).align_to(p41a, DOWN)
            self.play(*[FadeOut(b) for b in bars4], ReplacementTransform(p41a, p41b), run_time=0.6)
            vo.wait_until("the code sends them again")
            b23, sh = fly(p41b, TURNS[3][0], TURNS[3][1], 1, 3)
            pile.append(sh)
            vo.wait_until("every time")
            b24, s4_user = fly(p41b, 24, W_USER, 2)
            env4.sheets.append(s4_user)
            vo.wait_until("Memory is paper")
            cap4 = note("memory = paper you put back, every call", size=24, color=INK)
            cap4.move_to([0, 1.65, 0]).align_to([-6.4, 0, 0], LEFT)
            self.play(Write(cap4), run_time=0.9)
            pile_ring = ring(VGroup(*pile), TURN, buff=0.06)
            self.play(Create(pile_ring), run_time=0.5)

        # ============================================================ 4 · two building blocks
        with self.voiceover(SAY[4]) as vo:
            lw, rw = EnvelopePiece(width=5.1), EnvelopePiece(width=6.4)   # sheet factories
            left = [sheet_of(lw, W_SYS), sheet_of(lw, W_USER, LOOKUP), sheet_of(lw, W_DOCS),
                    sheet_of(lw, W_TOOLS), sheet_of(lw, W_SCHEMA)]
            right = [sheet_of(rw, W_TURNS), sheet_of(rw, W_PROF)]
            h_l = VGroup(label("Instructions", 24, S.GREY), note("system & user prompts ·"),
                         note("contexts · output schema"))
            h_l.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            h_r = VGroup(label("Memory", 24, S.GREY), note("user sessions · user preferences"))
            h_r.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            col_l = VGroup(h_l, VGroup(*left).arrange(DOWN, buff=0.1)).arrange(DOWN, aligned_edge=LEFT,
                                                                               buff=0.25)
            col_r = VGroup(h_r, VGroup(*right).arrange(DOWN, buff=0.1)).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.25)
            fr_l = box(col_l.width + 0.5, col_l.height + 0.45, S.GREY, fill=S.BG, fill_opacity=0.0,
                       radius=0.16)
            fr_r = box(col_r.width + 0.5, col_r.height + 0.45, S.GREY, fill=S.BG, fill_opacity=0.0,
                       radius=0.16)
            fr_l.move_to([-6.45 + fr_l.width / 2, 2.6 - fr_l.height / 2, 0])
            fr_r.move_to([6.45 - fr_r.width / 2, 2.6 - fr_r.height / 2, 0])
            col_l.move_to(fr_l)
            col_r.move_to(fr_r).align_to(fr_r, UP).shift(DOWN * 0.225)
            for s in list(env4.sheet_group):                # the sheets leave the envelope
                env4.sheet_group.remove(s)
                self.add(s)
            self.play(FadeOut(p41b), FadeOut(b23), FadeOut(b24), FadeOut(cap4), FadeOut(pile_ring),
                      FadeOut(env4),
                      ReplacementTransform(s4_sys, left[0]), ReplacementTransform(s4_user, left[1]),
                      ReplacementTransform(VGroup(*pile), right[0]),
                      *[FadeIn(s, shift=DOWN * 0.15) for s in (left[2], left[3], left[4], right[1])],
                      run_time=1.4)
            vo.wait_until("instructions and memory")
            self.play(Create(fr_l), FadeIn(h_l), run_time=0.6)
            vo.wait_until("and memory")
            self.play(Create(fr_r), FadeIn(h_r), run_time=0.6)
            vo.wait_until("Next lecture")
            l7 = concept_box("Lecture 7: context engineering").move_to([fr_r.get_center()[0], -0.6, 0])
            self.play(FadeIn(l7, shift=UP * 0.15), run_time=0.6)

        # ============================================================ 5 · spot it
        blocks = VGroup(fr_l, fr_r, h_l, h_r, *left, *right, l7)
        with self.voiceover(SAY[5]) as vo:
            p39 = src_panel(_C39, 16, 21, subtitle=True)
            p39.align_to([-6.45, 0, 0], LEFT).align_to([0, 2.7, 0], UP)
            self.play(FadeOut(blocks), FadeOut(ref), tr.goto(2), run_time=0.7)
            self.play(FadeIn(p39, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("Can you spot")
            spot_t = label("Spot it", 30, TURN)
            spot_s = label("the slip in step 2", 22, INK)
            spot_rows = VGroup(spot_t, spot_s).arrange(DOWN, buff=0.45)
            spot_fr = box(2.75, spot_rows.height + 0.7, TURN, fill=S.BG, fill_opacity=0.95, radius=0.16)
            spot = VGroup(spot_fr, spot_rows)
            spot_rows.move_to(spot_fr)
            spot.move_to([6.45 - 1.375, p39.code.get_center()[1], 0])
            uline = Line(spot_fr.get_left() + RIGHT * 0.3, spot_fr.get_right() + LEFT * 0.3,
                         color=TURN, stroke_width=4)
            uline.move_to([spot_fr.get_center()[0], (spot_t.get_bottom()[1] + spot_s.get_top()[1]) / 2, 0])
            ybars = VGroup(p39.bar(19, TURN, 0.2), p39.bar(20, TURN, 0.2))
            self.play(FadeIn(spot, scale=0.95), FadeIn(ybars), run_time=0.6)
        self.play(Create(uline), run_time=4.0, rate_func=linear)

        # ============================================================ 6 · the swapped roles
        with self.voiceover(SAY[6]) as vo:
            env2 = EnvelopePiece(width=4.8, slots=2)
            place(env2, [6.43 - 2.4, -3.56 + env2.env_h / 2, 0])
            s2_sys = sheet_of(env2, W_SYS)
            s2_user = sheet_of(env2, W_USER, LOOKUP)
            for i, s in enumerate((s2_sys, s2_user)):
                s.move_to(env2.slot_point(i))
                env2.sheet_group.add(s)
                env2.sheets.append(s)
            r_sys, r_user = role_label("system"), role_label("user")
            r_sys.move_to(to_spot(r_sys, s2_sys))
            r_user.move_to(to_spot(r_user, s2_user))
            self.play(FadeOut(spot), FadeOut(uline), FadeIn(env2, shift=UP * 0.2), FadeIn(r_sys),
                      FadeIn(r_user), run_time=0.7)
            vo.wait_until("goes in with the role user")
            rbars = VGroup(p39.bar(19, ERR, 0.2), p39.bar(20, ERR, 0.2))
            red_rings = VGroup(ring(p39.span(19, '"user"'), ERR, buff=0.05),
                               ring(p39.span(20, '"system"'), ERR, buff=0.05))
            self.play(r_sys.animate(path_arc=-PI * 0.6).move_to(to_spot(r_sys, s2_user)),
                      r_user.animate(path_arc=-PI * 0.6).move_to(to_spot(r_user, s2_sys)),
                      run_time=0.9)
            vo.wait_until("and the question with the role system")
            self.play(s2_sys.frame.animate.set_stroke(ERR, 4), s2_user.frame.animate.set_stroke(ERR, 4),
                      ReplacementTransform(ybars, rbars), Create(red_rings), run_time=0.6)

        # ============================================================ 7 · the fix, your turn
        with self.voiceover(SAY[7]) as vo:
            err = erratum_tag().next_to(p39.header, RIGHT, buff=0.35)
            ok = check_mark(0.34, S.GREEN)
            ok.move_to([to_spot(r_sys, s2_sys)[0], env2.parts["body"].get_top()[1] + 0.3, 0])
            self.play(FadeIn(err),
                      r_sys.animate(path_arc=PI * 0.6).move_to(to_spot(r_sys, s2_sys)),
                      r_user.animate(path_arc=PI * 0.6).move_to(to_spot(r_user, s2_user)),
                      run_time=0.9)
            self.play(s2_sys.frame.animate.set_stroke(S.GREY, 2), s2_user.frame.animate.set_stroke(LOOKUP, 2),
                      FadeOut(red_rings), FadeOut(rbars), Create(ok), run_time=0.6)
            fix = card_rows([f"`{FIX[0]}`", f"`{FIX[1]}`"], header="cell 39 · lines 19–20 · your edit",
                            frame_color=DATA)
            fix.align_to([-6.45, 0, 0], LEFT).align_to([0, p39.get_bottom()[1] - 0.25, 0], UP)
            differs = grey_tag("your step 2 answer will differ from the saved one")
            differs.next_to(fix, DOWN, buff=0.25).align_to(fix, LEFT)
            self.play(FadeIn(fix, shift=UP * 0.15), FadeIn(differs), run_time=0.7)
            vo.wait_until("from step 3 on")
            cap7 = note("swap the roles, then compare · steps 3–7 are right")
            cap7.next_to(differs, DOWN, buff=0.3).align_to(fix, LEFT)
            self.play(FadeIn(cap7), run_time=0.5)
            vo.wait_until("Pause")
            card7 = turn_card([Prose("Managing LLM Inputs:"), Prose("swap the roles in step 2"),
                               Prose("run steps 1–7"), (Prose("paid per call"), COST)], width=4.3)
            card7.shift([6.43 - card7.frame.get_right()[0], -3.5 - card7.frame.get_bottom()[1], 0])
            self.play(FadeOut(env2), FadeOut(r_sys), FadeOut(r_user), FadeOut(ok), run_time=0.4)
            self.play(FadeIn(card7, shift=UP * 0.15), run_time=0.6)
        self.wait(2)

        # ============================================================ 8 · step 6 pasted a tool's output
        with self.voiceover(SAY[8]) as vo:
            env6 = place(EnvelopePiece(width=6.4, slots=4), [-2.95, 0.75, 0])
            s6 = [sheet_of(env6, W_USER, LOOKUP), sheet_of(env6, W_SYS), sheet_of(env6, W_PROF),
                  sheet_of(env6, W_TOOLS)]
            for i, s in enumerate(s6):
                s.move_to(env6.slot_point(i))
                env6.sheet_group.add(s)
                env6.sheets.append(s)
            self.play(FadeOut(VGroup(p39, err, fix, differs, cap7, card7)), tr.goto(6), run_time=0.6)
            self.play(FadeIn(env6, shift=RIGHT * 0.5), run_time=0.7)
            vo.wait_until("the code pasted")
            sim = grey_tag("simulated · pasted in by the code (cell 43 · line 6)")
            sim.next_to(env6.parts["body"], DOWN, buff=0.3).align_to(s6[3].frame, LEFT)
            self.play(s6[3].frame.animate.set_stroke(TURN, 4), FadeIn(sim, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("But how does a model")
            ask = chip("?   how does a model ask for a tool?", S.GREY, size=22)
            ask.next_to(s6[3].frame, RIGHT, buff=0.75)
            sim_ln = Line(s6[3].frame.get_right() + RIGHT * 0.05, ask.get_left(), color=S.GREY,
                          stroke_width=2)
            keep = chip("keep the Cheese Quiz open · its Tools, MCP section comes after ADK", S.GREY,
                        size=20)
            keep.move_to([0, -2.55, 0])
            self.play(Create(sim_ln), FadeIn(ask, shift=LEFT * 0.15), run_time=0.6)
            self.play(FadeIn(keep), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(VGroup(env6, sim, sim_ln, ask, keep, tr)), run_time=0.8)
