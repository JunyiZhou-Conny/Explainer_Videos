"""S02 · Who holds the steering wheel? (Colab · Cheese Quiz: Prerequisites, then LLM to Agent).
Lecture: 16–18, then 25–27.

Beats (script.md "## S02", one voiceover block each):
 0  TRACKER CQ-Pre 1. The BLUE Colab frame "Cheese Quiz" (illustration); the menu path File › Save a
    copy in Drive, its second chip YELLOW; beside it a GREY caption where the original notebook is
    (course site · Lecture 6 · Tutorial 1, or the study guide's link; it stays through beat 0).
    TRACKER CQ-Pre 2: the schematic Secrets panel slides in (a
    key icon; one row: Notebook access toggle, Name OPENAI_API_KEY, Value ••••••; a GOLD key beside
    it). Under it CODE(colab/cheese-quiz/cell-12.py: 3–4) "Set Up OpenAI Key"; the name and
    userdata.get('OPENAI_API_KEY') light YELLOW together; the toggle switches on.
 1  TRACKER CQ-Pre 3. CODE(cell-10.py: 3) "Install Packages": GREY tag "unpinned" under fastmcp
    openai-agents; a YELLOW underline under > /dev/null 2>&1 and the tag "hides every error ·
    erratum: …". TRACKER CQ-Pre 4: RECORDED(c13: 5–6, …, 9–10), the two To: rows YELLOW, caption
    "look for both To: lines · missing? rerun Download". ▶ your turn card. Hold 2 s.
 2  TRACKER CQ-Agent 1. The frame goes. The PINK question chip; three lane names; the BLUE gpt-4o.
    Lane 1 (≤ 1.1 tall, top): question → gpt-4o → GREY answer card; a GOLD tick and "1 call ·
    2.81 s" (c21: 30), recorded.
 3  LECTURE 16–18. TRACKER CQ-Agent 2. Lane 1 dims. Lane 2: the same gpt-4o slides down; a GREY
    diamond "your Python decides the order"; four GREY stations analyze → decompose → answer +
    verify (×4) → synthesize; a YELLOW token runs the row, each station pings gpt-4o (an arc, a GOLD
    tick); the counter ticks 1 → 11 calls, then "39.34 s" (c25: 101), recorded; "701 tokens" with
    the erratum "an estimate: +100 per sub-question (cell 24 · line 116)".
 4  Slide 18's technique names (GREY dashed) over the stations they name (two tiers, leaders);
    "sequential processing" lights the arrows; the diamond pulses; GREY caption "reasoning workflow:
    …" and a GREY dashed chip "a reasoning model thinks inside one call · more with Gemini, later".
 5  TRACKER CQ-Agent 3. The lecture tag and lane 2's notes leave; lanes 2–3 slide up, lane 2 dims.
    Lane 3: lane 2's gpt-4o flashes and the same gpt-4o fades in on lane 3, lane 2's diamond slides
    into it; a GREY instructions note clips on; the excerpt chip tools=[web_tool], (cell 30 · line
    34) flashes and a BLUE web_search fades in under the model,
    "hosted by OpenAI"; two reaches (GOLD ticks), the two search texts (c31: 23, 28) grow in PINK;
    the answer and "13.29 s" (c31: 100); the excerpt Tools used: 1 (c31: 99) + erratum "tools
    configured (cell 30 · line 71), not calls".
 6  LECTURE 25–27. Lanes 1–2 shrink to a thumbnail under the tracker; lane 3 becomes V1 (Anatomy)
    part by part: gpt-4o → LLM core (the note fades), Instructions fades in, web_search → Tools,
    the question → Task / Goal, the answer → Task completion; the definition (slide 26, our words) above; an empty
    Memory; the diamond stretches into the dashed Dynamic Control bar, which lights YELLOW: a
    steering wheel and "who decides the next step".
 7  "agent = a smarter model" gets a RED strike; the thumbnail's gpt-4o chips and the LLM core light
    YELLOW together; then control and tools light; the anatomy shrinks into the mini-map (bottom
    right). ▶ your turn card "LLM to Agent: every cell …", last line GOLD "paid per call". Hold 2 s.
    Empty frame.
"""

import re

import numpy as np
from manim import *  # noqa: F401,F403

from common import *  # noqa: F401,F403
from explainer.scene import VoiceScene

SAY = NARRATION["S02"]
assert len(SAY) == 8

# ------------------------------------------------------------------ sources (file lines)
CELL12, CELL10 = "colab/cheese-quiz/cell-12.py", "colab/cheese-quiz/cell-10.py"
assert excerpt(CELL12, 4, 4) == "api_key = userdata.get('OPENAI_API_KEY')"
assert "fastmcp openai-agents > /dev/null 2>&1" in excerpt(CELL10, 3, 3)
TOOLS_LINE = excerpt("colab/cheese-quiz/cell-30.py", 34, 34)
assert TOOLS_LINE.strip() == "tools=[web_tool],"
assert '"tools": self.agent.tools' in excerpt("colab/cheese-quiz/cell-30.py", 71, 71)
assert "total_tokens += 100" in excerpt("colab/cheese-quiz/cell-24.py", 116, 116)

C13 = capture("expected/colab-cheese-quiz-c13-download.txt")
DL_OUT = C13.at(5, 6, "…", 9, 10)
assert DL_OUT[0] == "To: /content/quiz-schema.json" and DL_OUT[3] == "To: /content/quiz-ui.html"
DL_W = 5.6                                   # wide enough for both To: rows (the 100% rows are cut)
assert int((DL_W - 0.6) / cell_width(20)) >= max(len(DL_OUT[0]), len(DL_OUT[3]))

C21 = capture("expected/colab-cheese-quiz-c21-base-llm.txt")
C25 = capture("expected/colab-cheese-quiz-c25-reasoning-llm.txt")
C31 = capture("expected/colab-cheese-quiz-c31-simple-agent.txt")
assert C21.line(6).endswith(MODEL_CQ) and C25.line(4).endswith(MODEL_CQ) and C31.line(4).endswith(MODEL_CQ)
T1 = re.fullmatch(r"Tokens: \d+, Time: ([\d.]+)s", C21.line(30)).group(1) + " s"           # 2.81 s
_m25 = re.fullmatch(r"Total tokens: (\d+), Time: ([\d.]+)s", C25.line(101))
TOK2, T2 = f"{_m25.group(1)} tokens", _m25.group(2) + " s"                                   # 701, 39.34 s
assert C25.line(100) == "Sub-questions explored: 4"
assert sum("Making single API call" in C25.line(n, strip_emoji=True) for n in range(9, 30)) == COUNTS["reasoning_calls"] == 11
SEARCHES = [re.search(r'"(.+)"', C31.line(n)).group(1) for n in (23, 28)]
assert C31.line(23).startswith("### Search 1:") and C31.line(28).startswith("### Search 2:")
TOOLS_USED = C31.line(99)
assert TOOLS_USED == "Tools used: 1"
T3 = re.fullmatch(r"Time: ([\d.]+)s", C31.line(100)).group(1) + " s"                        # 13.29 s

OUT_HALF = squish_rate_func(smooth, 0.0, 0.45)   # a swap in one play: the old text leaves first,
IN_HALF = squish_rate_func(smooth, 0.55, 1.0)    # then the new one comes in (same run_time)

# ------------------------------------------------------------------ layout
NAME_X = -6.45                  # lane names, left column
ROW_X0 = -4.55                  # lane contents start
COUNT_R = 4.75                  # right edge of each lane's GOLD counter
Y1, Y2 = 2.3, 0.4               # lane rows; lane 2 slides up by LIFT when lane 3 starts
LIFT = 0.95
Y3_PRE, Y3 = -2.85, -0.35       # lane 3's name waits low (lane 2's notes go between), its row
SUB = -0.8                      # lane 2's sub-row (diamond caption, ticks, counter) below its stations
                                # (low enough that the ×4 badge clears the counter's digits)
X2 = ROW_X0 + 0.2               # lane 2's row starts a little further right (its longer name)
FR_TOP = 2.55                   # the Colab frame's top edge (its tab clears the tracker)
X0 = -6.15                      # left edge of the notebook content inside the frame


def arr(a, b, color=S.GREY, stroke=3):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=stroke, tip_length=0.14,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=20)


def lines_chip(rows, color, size=20, text_color=INK, fill=0.12, pad_x=0.22, pad_y=0.12):
    """A chip of one or more serif rows. .box .text"""
    t = VGroup(*[label(r, size, text_color) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    b = box(t.width + 2 * pad_x, max(0.5, t.height + 2 * pad_y), color, fill_opacity=fill,
            radius=0.14)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def halves(text):
    """Two rows of about equal length, split at a space."""
    words = text.split(" ")
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
    return [" ".join(words[:best]), " ".join(words[best:])]


def station(text):
    return lines_chip([text], S.GREY, size=20, fill=0.06, pad_x=0.15)


def tech(rows):
    """One of slide 18's technique names (a lecture concept): a GREY dashed box, two rows, 20 pt."""
    t = VGroup(*[label(r, 20, INK) for r in rows]).arrange(DOWN, buff=0.06)
    h = t.height + 0.22
    b = box(t.width + 0.3, h, S.GREY, dashed=True, radius=0.14)
    bg = RoundedRectangle(width=b.width, height=h, corner_radius=0.14, stroke_width=0).set_fill(S.BG, 0.9)
    t.move_to(b)
    g = VGroup(bg, b, t)
    g.box, g.text = b, t
    return g


def lane_name(n, name):
    return VGroup(label(f"lane {n}", 20, S.GREY), label(name, 20, S.GREY)) \
        .arrange(DOWN, aligned_edge=LEFT, buff=0.06)


def answer_card():
    b = box(1.0, 0.5, S.GREY, fill_opacity=0.08, radius=0.1)
    bars = answer_bars(3, w=0.7, h=0.07).move_to(b)
    g = VGroup(b, bars)
    g.box = b
    return g


def toggle():
    pill = RoundedRectangle(width=0.66, height=0.32, corner_radius=0.16, stroke_color=S.GREY,
                            stroke_width=2).set_fill(S.GREY_DARK, 0.8)
    knob = Circle(radius=0.11, stroke_width=0).set_fill(S.GREY, 1).move_to(pill.get_left() + RIGHT * 0.17)
    g = VGroup(pill, knob)
    g.pill, g.knob = pill, knob
    return g


def secrets_panel():
    """Colab's Secrets side panel, schematic: a key icon and "Secrets", column heads, one row.
    .name .value .toggle .row_y .frame"""
    head = VGroup(key_outline(0.24, S.GREY), label("Secrets", 22, INK)).arrange(RIGHT, buff=0.22)
    heads = [label(s, 20, S.GREY) for s in ("Notebook access", "Name", "Value")]
    tg = toggle()
    name = mono("OPENAI_API_KEY", 22, INK)
    val = mono("••••••", 22, INK)
    x = [0.0, heads[0].width + 0.45]
    x.append(x[1] + name.width + 0.45)
    yh, yr = -0.62, -1.1
    for k, (hd, cell) in enumerate(zip(heads, (tg, name, val))):
        hd.move_to([x[k], yh, 0], aligned_edge=LEFT)
        cell.move_to([x[k], yr, 0], aligned_edge=LEFT)
    head.move_to([0, 0, 0], aligned_edge=LEFT)
    rule = Line([0, -0.35, 0], [x[2] + val.width, -0.35, 0], color=S.GREY_DARK, stroke_width=2)
    body = VGroup(head, rule, *heads, tg, name, val)
    fr = RoundedRectangle(width=body.width + 0.7, height=body.height + 0.5, corner_radius=0.14,
                          stroke_color=S.GREY_DARK, stroke_width=2).set_fill(PANEL, 1).move_to(body)
    g = VGroup(fr, body)
    g.frame, g.name, g.value, g.toggle, g.row_y = fr, name, val, tg, yr
    return g


def wheel(r=0.2, color=TURN):
    """A steering wheel (three spokes; not the six-spoke Python wheel of V5)."""
    rim = Circle(radius=r, stroke_color=color, stroke_width=3.5)
    hub = Circle(radius=r * 0.24, stroke_color=color, stroke_width=2.5).set_fill(color, 0.6)
    spokes = VGroup(*[Line(ORIGIN, r * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=3)
                      for a in (PI / 2 + PI, PI / 6, 5 * PI / 6)])
    return VGroup(rim, spokes, hub)


def dimmed(group, k):
    """Transform: every member of `group` to k of its own first-seen opacity (k=1 restores)."""
    target = group.copy()
    for src, dst in zip(group.get_family(), target.get_family()):
        if isinstance(src, VMobject):
            if not hasattr(src, "_s02_op"):
                src._s02_op = (src.get_fill_opacity(), src.get_stroke_opacity())
            f, s = src._s02_op
            dst.set_fill(opacity=f * k, family=False)
            dst.set_stroke(opacity=s * k, family=False)
    return Transform(group, target)


def lifted(group, k, dy):
    """Transform: `group` shifted up by dy and dimmed to k (lanes 2-3 make room for lane 3)."""
    t = dimmed(group, k)
    t.target_mobject.shift(UP * dy)
    return t


def place_counter(cc, final_text, y, size=24):
    """Put a CallCounter so that its final text (with the time) ends at COUNT_R."""
    w = label(final_text, size, COST).width
    cc.move_to([COUNT_R - w + cc.width / 2, y, 0])
    return cc


def coin_row(n, right, y, pitch=0.21):
    coins = VGroup(*[cost_tick(0.085) for _ in range(n)])
    for k, c in enumerate(coins):
        c.move_to([right - (n - 1 - k) * pitch, y, 0])
    return coins


def your_card(rows, header=None):
    """turn_card's look for rows that mix serif and mono (card_rows + the YELLOW ▶ tag; no GREY
    "your turn" header above it: the tag already says so, and beat 1 needs the room)."""
    c = card_rows(rows, header=header, buff=0.13)
    # a taller frame (0.14 more at the top), so the ▶ tag straddling the edge clears the first row
    fr = c.frame
    tall = box(fr.width, fr.height + 0.14, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    tall.move_to(fr).align_to(fr, DOWN)
    c.remove(fr)
    c.add_to_back(tall)
    c.frame = tall
    tg = your_turn().move_to(c.frame.get_corner(UP + RIGHT)).shift(LEFT * 1.0)
    c.add(tg)
    c.tag = tg
    return c


class SteeringWheel(VoiceScene):
    def construct(self):
        # ============================================================ 0 · copy, key
        with self.voiceover(SAY[0]) as vo:
            tr = tracker("CQ-Pre", 1)
            cf = colab_frame("Cheese Quiz", top=FR_TOP)
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(cf), run_time=1.0)
            mp = menu_path(["File", "Save a copy in Drive"])
            mp.move_to([X0, 1.85, 0], aligned_edge=LEFT)
            # where the original notebook is: the course site (Lecture 6 · Tutorial 1, Colab link,
            # tutorials_demo.md:85-88) and the study guide's Cheese Quiz checklist link the same
            # Colab. Ed itself was never opened, so it is not named.
            where = VGroup(label("first open it: course site · Lecture 6 · Tutorial 1,", 20, S.GREY),
                           label("or the Cheese Quiz link in the study guide", 20, S.GREY)) \
                .arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            where.next_to(mp, RIGHT, buff=0.55).set_y(mp.get_y())
            assert where.get_right()[0] < cf.tag.get_right()[0]
            assert where.get_top()[1] < cf.tag.get_bottom()[1] - 0.1
            vo.wait_until("in the Cheese Quiz")
            self.play(FadeIn(mp, shift=DOWN * 0.1), FadeIn(where, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Save a copy")
            self.play(mp.light(1), run_time=0.6)

            sec = secrets_panel()
            sec.move_to([X0, 0.0, 0], aligned_edge=LEFT).align_to(mp, LEFT)
            sec.shift(UP * (1.25 - sec.get_top()[1]))
            assert where.get_bottom()[1] > sec.get_top()[1] + 0.12
            gk = key_glyph(0.32).next_to(sec.frame, RIGHT, buff=0.3)
            gk.set_y(sec.name.get_y())
            vo.wait_until("then add your OpenAI key")
            self.play(tr.goto(2), FadeIn(sec, shift=RIGHT * 0.5), run_time=0.8)
            self.play(FadeIn(gk, scale=1.5), run_time=0.5)

            p12 = src_panel(CELL12, 3, 4, subtitle=True)
            p12.move_to([X0, 0, 0], aligned_edge=LEFT)
            p12.shift(UP * (sec.frame.get_bottom()[1] - 0.55 - p12.get_top()[1]))
            vo.wait_until("under the name shown")
            self.play(FadeIn(p12, shift=UP * 0.15), run_time=0.6)
            sp = p12.span(4, "userdata.get('OPENAI_API_KEY')")
            hl_code = box(sp.width + 0.2, sp.height + 0.2, TURN, fill_opacity=0.1, radius=0.08).move_to(sp)
            hl_name = box(sec.name.width + 0.2, sec.name.height + 0.24, TURN, fill_opacity=0.1,
                          radius=0.08).move_to(sec.name)
            self.play(Create(hl_name), Create(hl_code), run_time=0.7)
            vo.wait_until("with notebook access on")
            tg = sec.toggle
            self.play(tg.knob.animate.move_to(tg.pill.get_right() + LEFT * 0.17).set_fill(INK, 1),
                      tg.pill.animate.set_fill(TURN, 0.55).set_stroke(TURN, 2.5), run_time=0.6)

        # ============================================================ 1 · install, download
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(mp), FadeOut(where), FadeOut(sec), FadeOut(gk), FadeOut(p12),
                      FadeOut(hl_name), FadeOut(hl_code), tr.goto(3), run_time=0.6)
            p10 = src_panel(CELL10, 3, subtitle=True)
            p10.move_to([X0, 0, 0], aligned_edge=LEFT)
            p10.shift(UP * (cf.title.get_bottom()[1] - 0.2 - p10.get_top()[1]))   # clear of the tab
            self.play(FadeIn(p10, shift=UP * 0.15), run_time=0.6)
            pk = p10.span(3, "fastmcp openai-agents")
            rd = p10.span(3, "> /dev/null 2>&1")
            y_tags = p10.get_bottom()[1] - 0.12
            unp = grey_tag("unpinned")
            unp.move_to([pk.get_x(), y_tags - unp.height / 2, 0])
            vo.wait_until("installs two packages")
            pk_ul = under(pk, S.GREY, stroke=3)
            self.play(Create(pk_ul), FadeIn(unp, shift=UP * 0.1), run_time=0.6)
            ul = under(rd, TURN)
            vo.wait_until("and hides all output")
            self.play(Create(ul), run_time=0.5)
            hide = lines_chip(["hides every error · erratum:", "rerun without it if imports fail"],
                              S.GREY, size=20, text_color=S.GREY, fill=0.0)
            hide.box.set_fill(S.BG, 0.92)
            hide.move_to([0, y_tags - hide.height / 2, 0]).align_to(rd, RIGHT).shift(RIGHT * 0.3)
            vo.wait_until("if imports fail later")
            self.play(FadeIn(hide, shift=UP * 0.1), run_time=0.6)

            ob = output_box(DL_OUT, header="Cheese Quiz · cell 13 · output", width=DL_W)
            ob.move_to([X0, 0, 0], aligned_edge=LEFT)
            sv = saved_run_tag().next_to(ob.header, RIGHT, buff=0.25)
            VGroup(ob, sv).shift(UP * (hide.box.get_bottom()[1] - 0.2 - VGroup(ob, sv).get_top()[1]))
            to_bars = VGroup(*[Rectangle(width=ob.rows[i].width + 0.16, height=0.34, stroke_width=0)
                               .set_fill(TURN, 0.18).move_to(ob.rows[i]) for i in (0, 3)])
            look = label("look for both To: lines · missing? rerun Download", 20, TURN)
            look.next_to(ob.frame, DOWN, buff=0.12).align_to(ob.frame, LEFT)
            assert look.get_bottom()[1] > cf.frame.get_bottom()[1] + 0.12
            vo.wait_until("Then download the quiz files")
            self.play(tr.goto(4), FadeIn(ob, shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(to_bars), FadeIn(sv), FadeIn(look, shift=UP * 0.1), run_time=0.6)

            card = your_card([
                "Prerequisites: save a copy",
                VGroup(label("Secrets:", 20, INK), mono("OPENAI_API_KEY", 20, INK)).arrange(RIGHT, buff=0.14),
                "with notebook access on",
                "run Install Packages, Imports,",
                "Set Up OpenAI Key, Download",
            ])
            card.move_to([0, 0, 0])
            card.shift(np.array([6.3 - card.frame.get_right()[0], -3.36 - card.frame.get_bottom()[1], 0]))
            assert card.frame.get_top()[1] < sv.get_bottom()[1] - 0.12
            assert card.frame.get_left()[0] > max(ob.frame.get_right()[0], look.get_right()[0]) + 0.2
            vo.wait_until("and pause to run the setup")
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
        self.wait(2)

        # ============================================================ 2 · lane 1
        with self.voiceover(SAY[2]) as vo:
            tr2 = tracker("CQ-Agent", 1)
            setup = [cf, p10, pk_ul, unp, ul, hide, ob, to_bars, sv, look, card]
            # the old tracker lifts away, then the new one drops in (at once, both read mid-swap)
            self.play(FadeOut(tr, shift=UP * 0.25, rate_func=OUT_HALF),
                      FadeIn(tr2, shift=DOWN * 0.25, rate_func=IN_HALF),
                      *[FadeOut(m) for m in setup], run_time=0.8)
            tr = tr2
            q1 = lines_chip(["best cheese for a grilled", "cheese sandwich?"], LOOKUP, size=20)
            q1.move_to([ROW_X0 + q1.width / 2, Y1, 0])
            vo.wait_until("asks one question")
            self.play(FadeIn(q1, shift=RIGHT * 0.3), run_time=0.6)
            n1, n2, n3 = (lane_name(1, "base LLM"), lane_name(2, "reasoning LLM"), lane_name(3, "agent"))
            for n, y in ((n1, Y1), (n2, Y2), (n3, Y3_PRE)):
                n.move_to([NAME_X + n.width / 2, y, 0])
            vo.wait_until("three ways")
            self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.2) for n in (n1, n2, n3)], lag_ratio=0.3),
                      run_time=0.9)
            m1 = model_chip(MODEL_CQ, 22)
            m1.move_to([q1.get_right()[0] + 0.45 + m1.width / 2, Y1, 0])
            vo.wait_until("with the same model")
            self.play(FadeIn(m1, scale=1.2), run_time=0.6)
            vo.wait_until("what's the best cheese")
            self.play(Indicate(q1, scale_factor=1.05, color=LOOKUP), run_time=0.9)

            vo.wait_until("Lane 1")
            self.play(n1.animate.set_color(INK), run_time=0.4)
            a1 = arr(q1.get_right(), m1.get_left(), LOOKUP)
            ans1 = answer_card().move_to([m1.get_right()[0] + 0.45 + 0.5, Y1, 0])
            a1b = arr(m1.get_right(), ans1.get_left(), CLOUD)
            cc1 = CallCounter(1)
            place_counter(cc1, f"1 call · {T1}", Y1)
            coins1 = coin_row(1, cc1.get_left()[0] - 0.2, Y1)
            rec1 = recorded_tag().move_to([6.45, Y1, 0], aligned_edge=RIGHT)
            vo.wait_until("one call to")
            dot = Dot(q1.get_right(), radius=0.08, color=LOOKUP)
            self.play(GrowArrow(a1), run_time=0.4)
            self.play(MoveAlongPath(dot, Line(q1.get_right(), m1.get_left())), run_time=0.5)
            self.remove(dot)
            self.play(Indicate(m1, scale_factor=1.08, color=CLOUD), FadeIn(coins1, scale=1.6),
                      FadeIn(cc1), run_time=0.6)
            vo.wait_until("one answer")
            self.play(GrowArrow(a1b), FadeIn(ans1, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("in under 3 seconds")
            self.play(cc1.with_time(T1), FadeIn(rec1), run_time=0.6)
            lane1 = VGroup(n1, q1, a1, m1, a1b, ans1, coins1, cc1, rec1)

        # ============================================================ 3 · lane 2
        with self.voiceover(SAY[3]) as vo:
            lr = lref("16–18")
            self.play(tr.goto(2), FadeIn(lr), dimmed(lane1, 0.4), n2.animate.set_color(INK), run_time=0.7)
            d2 = diamond(w=0.7).move_to([X2 + 0.35, Y2, 0])
            sts = [station(s) for s in ("analyze", "decompose", "answer + verify", "synthesize")]
            x = d2.get_right()[0] + 0.4
            for s in sts:
                s.move_to([x + s.width / 2, Y2, 0])
                x = s.get_right()[0] + 0.4
            bt = label("×4", 20, INK)
            badge = VGroup(RoundedRectangle(width=bt.width + 0.22, height=0.36, corner_radius=0.14,
                                            stroke_color=S.GREY, stroke_width=2).set_fill(S.BG, 1), bt)
            bt.move_to(badge[0])
            badge.move_to(sts[2].get_corner(DOWN + RIGHT) + np.array([0.1, -0.1, 0]))   # clear of the descenders
            arrows2 = VGroup(*[arr(a.get_right(), b.get_left())
                               for a, b in zip([d2] + sts[:-1], sts)])
            m2 = model_chip(MODEL_CQ, 22).move_to(m1)
            m2_at = np.array([sts[-1].get_right()[0] + 0.45 + m2.width / 2, Y2, 0])
            dcap = label("your Python decides the order", 20, S.GREY)
            dcap.move_to([X2 + dcap.width / 2, Y2 + SUB, 0])
            vo.wait_until("Python methods")
            self.play(FadeIn(d2, scale=0.6), FadeIn(dcap, shift=UP * 0.1),
                      m2.animate.move_to(m2_at), run_time=0.9)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(s, shift=RIGHT * 0.15))
                                    for a, s in zip(arrows2, sts)], lag_ratio=0.35),
                      FadeIn(badge), run_time=1.3)

            cc2 = CallCounter(1)
            place_counter(cc2, f"11 calls · {T2}", Y2 + SUB)
            coins2 = coin_row(11, cc2.get_left()[0] - 0.2, Y2 + SUB)
            rec2 = recorded_tag().move_to([6.45, Y2 + SUB, 0], aligned_edge=RIGHT)
            tok = Dot(radius=0.08, color=TURN).move_to(d2.get_top() + UP * 0.12)

            def ping(i_station, k, run_time, first=False):
                s = sts[i_station]
                a, b = s.get_top() + UP * 0.05, m2.get_top() + UP * 0.05
                arc = ArcBetweenPoints(a, b, angle=-PI / 3.2 if i_station < 3 else -PI / 2.2)
                arc.set_stroke(CLOUD, 4)
                anims = [ShowPassingFlash(arc, time_width=0.6), FadeIn(coins2[k - 1], scale=1.8)]
                anims.append(FadeIn(cc2) if first else cc2.count_to(k, run_time))
                self.play(*anims, run_time=run_time)

            vo.wait_until("Analyze")
            self.play(FadeIn(tok), tok.animate.move_to(sts[0].get_top() + UP * 0.12), run_time=0.35)
            ping(0, 1, 0.45, first=True)
            vo.wait_until("split into 4 sub-questions")
            self.play(tok.animate.move_to(sts[1].get_top() + UP * 0.12), run_time=0.3)
            ping(1, 2, 0.4)
            vo.wait_until("answer and verify each")
            self.play(tok.animate.move_to(sts[2].get_top() + UP * 0.12), run_time=0.3)
            for k in range(3, 11):
                ping(2, k, 0.22)
            vo.wait_until("then combine")
            self.play(tok.animate.move_to(sts[3].get_top() + UP * 0.12), run_time=0.3)
            ping(3, 11, 0.45)
            self.play(FadeOut(tok), run_time=0.3)
            vo.wait_until("That's 11 calls")
            self.play(Indicate(cc2, scale_factor=1.15, color=COST), run_time=0.7)
            vo.wait_until("and 39 seconds")
            self.play(cc2.with_time(T2), FadeIn(rec2), run_time=0.6)
            tokc = chip(TOK2, S.GREY, size=22)
            tokc.move_to([X2 + tokc.width / 2, Y2 + SUB - 0.62, 0])
            est = erratum_tag("an estimate: +100 per sub-question (cell 24 · line 116)")
            est.move_to([6.45 - est.width / 2, tokc.get_y(), 0])
            tokc.next_to(est, LEFT, buff=0.15)
            vo.wait_until("token total")
            self.play(FadeIn(tokc, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(est, shift=LEFT * 0.1), run_time=0.5)
            lane2 = VGroup(n2, d2, *sts, badge, arrows2, m2, dcap, coins2, cc2, rec2)

        # ============================================================ 4 · reasoning workflow
        with self.voiceover(SAY[4]) as vo:
            y_t = sts[0].get_top()[1] + 0.12
            t_seq = tech(["sequential", "processing"])
            t_dec = tech(["problem", "decomposition"])
            t_ver = tech(["verification", "loop"])
            t_sum = tech(["summary", "generation"])
            t_seq.move_to([(d2.get_right()[0] + sts[0].get_left()[0]) / 2, y_t + t_seq.height / 2, 0])
            for t, st in ((t_dec, sts[1]), (t_ver, sts[2]), (t_sum, sts[3])):
                t.move_to([st.get_x(), y_t + t.height / 2, 0])
            techs = VGroup(t_seq, t_dec, t_ver, t_sum)
            vo.wait_until("a multi-call system")
            self.play(LaggedStart(AnimationGroup(FadeIn(t_seq, shift=DOWN * 0.1),
                                                 Indicate(arrows2, scale_factor=1.0, color=INK)),
                                  FadeIn(t_dec, shift=DOWN * 0.1), FadeIn(t_ver, shift=DOWN * 0.1),
                                  FadeIn(t_sum, shift=DOWN * 0.1), lag_ratio=0.5), run_time=2.6)
            vo.wait_until("Here your Python")
            self.play(Indicate(d2, scale_factor=1.35, color=INK), Indicate(dcap, scale_factor=1.05, color=INK),
                      run_time=1.0)
            wf = label("reasoning workflow: many calls, ordered by your code", 22, S.GREY)
            wf.move_to([0.4, Y2 + SUB - 1.15, 0])
            rm = concept_box("a reasoning model thinks inside one call · more with Gemini, later")
            rm.move_to([0.4, Y2 + SUB - 1.72, 0])
            vo.wait_until("so it's a reasoning workflow")
            self.play(FadeIn(wf, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("not a reasoning model")
            self.play(FadeIn(rm, shift=UP * 0.1), run_time=0.6)
        self.wait(1.0)

        # ============================================================ 5 · lane 3
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(lr), FadeOut(techs), FadeOut(tokc), FadeOut(est),
                      FadeOut(wf), FadeOut(rm), run_time=0.5)
            y3 = Y3
            self.play(tr.goto(3), lifted(lane2, 0.4, LIFT), n3.animate.shift(UP * (Y3 - Y3_PRE)).set_color(INK),
                      run_time=0.8)
            q3 = chip("?", LOOKUP, size=22)
            q3.move_to([ROW_X0 - 0.2, y3, 0])
            note = sticky_note("instructions")
            m3 = model_chip(MODEL_CQ, 22).move_to(m2)
            # the wide chip (a slot for the diamond on the right)
            w_box = box(m3.text.width + 1.25, m3.box.height, CLOUD, fill_opacity=0.16,
                        radius=m3.box.height / 2.6)
            m3_x = q3.get_right()[0] + 0.45 + note.width - 0.12 + w_box.width / 2
            w_box.move_to([m3_x, y3, 0])
            w_txt = m3.text.copy().move_to(w_box.get_left() + RIGHT * (0.3 + m3.text.width / 2))
            note.move_to([w_box.get_left()[0] - note.width / 2 + 0.12, y3 + 0.1, 0])
            vo.wait_until("the same model")
            # lane 2's model flashes in place and the same model fades in on lane 3 (flying down,
            # the chip crossed "synthesize" and the "11 calls" counter)
            m3.move_to([m3_x, y3, 0])
            self.play(FadeIn(q3), Indicate(m2, color=CLOUD, scale_factor=1.08),
                      FadeIn(m3, rate_func=squish_rate_func(smooth, 0.3, 1.0)), run_time=0.8)
            d3 = diamond(w=0.42).move_to(d2)
            self.play(Transform(m3.box, w_box), Transform(m3.text, w_txt), run_time=0.4)
            self.play(d3.animate.move_to(w_box.get_right() + LEFT * 0.42), run_time=0.8)
            vo.wait_until("plus instructions")
            a3 = arr(q3.get_right(), note.get_left(), LOOKUP)
            self.bring_to_back(note)
            self.play(FadeIn(note, shift=RIGHT * 0.3), GrowArrow(a3), run_time=0.6)

            ex_tools = excerpt_chip("tools=[web_tool],", "Cheese Quiz · cell 30 · line 34 (excerpt)",
                                    line=TOOLS_LINE)
            ex_tools.move_to([NAME_X + ex_tools.width / 2, 0, 0])
            ex_tools.shift(UP * (-3.5 - ex_tools.get_bottom()[1]))
            w3 = chip("web_search", CLOUD, size=22, font=MONO)
            w3_at = np.array([w_box.get_x(), y3 - 0.95, 0])
            w3.move_to(w3_at)
            host = grey_tag("hosted by OpenAI")
            host.move_to([w3_at[0] + w3.width / 2 + 0.2 + host.width / 2, w3_at[1], 0])
            vo.wait_until("and a web search tool")
            self.play(FadeIn(ex_tools, shift=UP * 0.1), run_time=0.5)
            # the excerpt flashes in place, web_search fades in under the model (a flying copy
            # crossed the excerpt's header and scrambled its letters)
            self.play(Indicate(ex_tools.chip.text, color=CLOUD, scale_factor=1.08),
                      ex_tools.chip.box.animate(rate_func=there_and_back).set_stroke(CLOUD, 4),
                      FadeIn(w3, rate_func=squish_rate_func(smooth, 0.3, 1.0)), run_time=0.8)
            vo.wait_until("that OpenAI hosts")
            self.play(FadeIn(host, shift=LEFT * 0.1), run_time=0.5)

            t3 = label(T3, 24, COST)
            t3.move_to([COUNT_R - t3.width / 2, y3, 0])
            coins3 = coin_row(2, host.get_right()[0] + 0.25 + 0.21, w3_at[1])
            rec3 = recorded_tag().move_to([6.45, y3, 0], aligned_edge=RIGHT)
            sch = []
            x = ROW_X0
            for s in SEARCHES:
                c = lines_chip(halves(f"“{s}”"), LOOKUP, size=20, fill=0.1)
                c.move_to([x + c.width / 2, y3 - 1.75, 0])
                x = c.get_right()[0] + 0.3
                sch.append(c)
            down = Arrow(m3.box.get_bottom(), w3.get_top(), buff=0.03, color=CLOUD, stroke_width=3,
                         tip_length=0.12, max_tip_length_to_length_ratio=0.5).shift(LEFT * 0.25)
            back = Arrow(w3.get_top(), m3.box.get_bottom(), buff=0.03, color=CLOUD, stroke_width=3,
                         tip_length=0.12, max_tip_length_to_length_ratio=0.5).shift(RIGHT * 0.25)
            vo.wait_until("Its answer reports two searches")
            for k in range(2):
                # each search text grows in its own place (flying out of web_search, the cards
                # crossed its name and each other)
                start = sch[k].copy().scale(0.3).move_to(sch[k])
                self.play(GrowArrow(down), run_time=0.35)
                self.play(ReplacementTransform(start, sch[k]), FadeIn(coins3[k], scale=1.8),
                          GrowArrow(back), run_time=0.6)
                self.play(FadeOut(down), FadeOut(back), run_time=0.25)
            ans3 = answer_card().move_to([w_box.get_right()[0] + 0.5 + 0.5, y3, 0])
            a3b = arr(w_box.get_right(), ans3.get_left(), CLOUD)
            vo.wait_until("and it stopped on its own")
            self.play(GrowArrow(a3b), FadeIn(ans3, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("after 13 seconds")
            self.play(FadeIn(t3, shift=LEFT * 0.1), FadeIn(rec3), run_time=0.6)

            ex_used = excerpt_chip(TOOLS_USED, "Cheese Quiz · cell 31 · saved output")
            ex_used.move_to(ex_tools, aligned_edge=DOWN + LEFT)
            cfg = erratum_tag("tools configured (cell 30 · line 71), not calls")
            cfg.next_to(ex_used.chip, RIGHT, buff=0.25)
            vo.wait_until("It also reports one tool used")
            self.play(FadeOut(ex_tools, shift=DOWN * 0.1, rate_func=OUT_HALF),
                      FadeIn(ex_used, shift=UP * 0.1, rate_func=IN_HALF), run_time=0.6)
            vo.wait_until("tools configured")
            self.play(FadeIn(cfg, shift=LEFT * 0.1), run_time=0.6)

        # ============================================================ 6 · the anatomy
        with self.voiceover(SAY[6]) as vo:
            lr = lref("25–27")
            A = Anatomy()
            A.move_to([0, -1.4, 0])
            A.parts["box"].set_fill(opacity=0)
            # the thumbnail of lanes 1-2, under the tracker
            th_q = box(0.42, 0.24, LOOKUP, fill_opacity=0.2, radius=0.06)
            th_m1 = model_chip(MODEL_CQ, 20)
            th_a = box(0.42, 0.24, S.GREY, fill_opacity=0.1, radius=0.06)
            row1 = VGroup(label("1", 20, S.GREY), th_q, th_m1, th_a).arrange(RIGHT, buff=0.18)
            th_d = diamond(w=0.3)
            th_s = [box(0.3, 0.2, S.GREY, fill_opacity=0.06, radius=0.04) for _ in range(4)]
            th_m2 = model_chip(MODEL_CQ, 20)
            row2 = VGroup(label("2", 20, S.GREY), th_d, *th_s, th_m2).arrange(RIGHT, buff=0.12)
            th_m2.shift(RIGHT * 0.06)
            rows = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            th_fr = RoundedRectangle(width=rows.width + 0.4, height=rows.height + 0.3, corner_radius=0.12,
                                     stroke_color=S.GREY_DARK, stroke_width=2).move_to(rows)
            thumb = VGroup(th_fr, rows)
            thumb.move_to([TRACK_LEFT + thumb.width / 2, 2.75 - thumb.height / 2, 0])
            rows[0][1:].align_to(rows[1][1], LEFT)
            gone = [n1, a1, a1b, coins1, cc1, rec1, n2, arrows2, badge, dcap, coins2, cc2, rec2,
                    n3, a3, coins3, t3, rec3, host, ex_used, cfg, *sch]
            self.play(FadeIn(lr),
                      *[FadeOut(m) for m in gone],
                      ReplacementTransform(q1, th_q), ReplacementTransform(m1, th_m1),
                      ReplacementTransform(ans1, th_a), ReplacementTransform(d2, th_d),
                      *[ReplacementTransform(s, t) for s, t in zip(sts, th_s)],
                      ReplacementTransform(m2, th_m2), FadeIn(th_fr), FadeIn(row1[0]), FadeIn(row2[0]),
                      run_time=1.2)

            dc = definition_card()
            dc.move_to([th_fr.get_right()[0] + 0.35 + dc.width / 2, 0, 0])
            dc.shift(UP * (2.6 - dc.get_top()[1]))
            vo.wait_until("defines an agent")
            self.play(FadeIn(dc.frame), Write(dc.rows[0]), run_time=1.0)
            vo.wait_until("an LLM")
            # the diamond rides along inside the LLM core (it was inside the model in lane 3) until
            # it stretches into the Dynamic Control bar; lane 3's question and answer step out to
            # the ends, where Task / Goal and Task completion will form (the answer card sat
            # where the Instructions block now is)
            core_fr = A.frames["core"]
            d3_at = np.array([core_fr.get_right()[0] - 0.45, core_fr.get_y(), 0])
            self.play(FadeIn(A.parts["box"]), FadeIn(A.parts["head"]),
                      ReplacementTransform(m3, A.parts["core"]),
                      # the note leaves before the growing core reaches it (it covered the note)
                      FadeOut(note, rate_func=squish_rate_func(smooth, 0.0, 0.35)),
                      d3.animate.scale(1.2).move_to(d3_at), FadeOut(a3b),
                      q3.animate.move_to(A.parts["task"]), ans3.animate.move_to(A.parts["done"]),
                      run_time=0.8)
            self.bring_to_front(d3)                  # above the core's tinted fill
            vo.wait_until("given instructions")
            # the Instructions block fades in where it stays (the note's arc crossed the "Agent" head)
            self.play(FadeIn(A.parts["instructions"], scale=0.9), run_time=0.8)
            vo.wait_until("and tools")
            self.play(ReplacementTransform(w3, A.parts["tools"]), run_time=0.7)
            vo.wait_until("that runs on its own")
            self.play(Write(dc.rows[1]), ReplacementTransform(q3, A.parts["task"]),
                      GrowArrow(A.parts["a_in"]), run_time=0.8)
            vo.wait_until("until the task is done")
            und = under(dc.until, TURN, stroke=3)
            self.play(Create(und), GrowArrow(A.parts["a_out"]), ReplacementTransform(ans3, A.parts["done"]),
                      run_time=0.8)

            vo.wait_until("Of its five blocks")
            self.play(FadeIn(A.parts["memory"], shift=UP * 0.1), run_time=0.5)
            blocks = [A.frames[n] for n in ("core", "instructions", "tools", "memory")]
            self.play(LaggedStart(*[Indicate(b, scale_factor=1.04, color=INK) for b in blocks[:2]],
                                  Indicate(d3, scale_factor=1.3, color=INK),
                                  *[Indicate(b, scale_factor=1.04, color=INK) for b in blocks[2:]],
                                  lag_ratio=0.3), run_time=1.1)
            vo.wait_until("one decides the next step")
            self.play(ReplacementTransform(d3, A.parts["control_dash"]), FadeIn(A.names["control"]),
                      run_time=0.9)
            bar, nm = A.parts["control_dash"], A.names["control"]
            wh = wheel().move_to([bar.get_left()[0] + 0.42, bar.get_y(), 0])
            nm_to = nm.copy().next_to(wh, RIGHT, buff=0.22)
            who = label("who decides the next step", 22, TURN)
            if nm_to.get_right()[0] + 0.35 + who.width > bar.get_right()[0] - 0.12:
                who = label("who decides the next step", 20, TURN)
            who.next_to(nm_to, RIGHT, buff=0.35)
            assert who.get_right()[0] < bar.get_right()[0] - 0.1
            vo.wait_until("dynamic control")
            # the caption comes in once the name has slid past its place (they crossed)
            self.play(nm.animate.move_to(nm_to), FadeIn(wh, scale=0.5),
                      FadeIn(who, shift=LEFT * 0.1, rate_func=squish_rate_func(smooth, 0.65, 1.0)),
                      run_time=0.5)
            self.play(A.light("control"), run_time=0.4)
            vo.wait_until("the steering wheel")
            self.play(Rotate(wh, -PI / 5), run_time=0.45)
            self.play(Rotate(wh, PI / 5), run_time=0.45)

        # ============================================================ 7 · same model, your turn
        with self.voiceover(SAY[7]) as vo:
            smart = card_rows(["agent = a smarter model"])
            smart.move_to(dc.frame)
            self.play(FadeOut(dc, rate_func=OUT_HALF), FadeOut(und, rate_func=OUT_HALF),
                      FadeIn(smart, rate_func=IN_HALF), run_time=0.6)
            vo.wait_until("isn't a smarter model")
            st_line = strike(smart.rows[0], stroke=3)
            self.play(Create(st_line), run_time=0.5)
            th_chips = [th_m1, th_m2]
            vo.wait_until("the model was the same")
            self.play(A.light("core"), wh.animate.set_color(S.GREY), who.animate.set_color(S.GREY),
                      *[c.box.animate.set_stroke(TURN, 4) for c in th_chips],
                      *[c.text.animate.set_color(TURN) for c in th_chips], run_time=0.7)
            vo.wait_until("What changed is who steers")
            self.play(A.light("control"), wh.animate.set_color(TURN), who.animate.set_color(TURN),
                      *[c.box.animate.set_stroke(CLOUD, 2.5) for c in th_chips],
                      *[c.text.animate.set_color(INK) for c in th_chips], run_time=0.6)
            vo.wait_until("and the tools")
            self.play(A.frames["tools"].animate.set_stroke(TURN, 4), A.names["tools"].animate.set_color(TURN),
                      run_time=0.5)

            # the anatomy shrinks into the mini-map
            mm = AnatomyMini()
            glyphs = A.glyph_only()
            texts = [m for m in A.get_family() if isinstance(m, Text)] + [who]
            self.play(*[FadeOut(t) for t in texts], FadeOut(lr), FadeOut(smart), FadeOut(st_line), run_time=0.4)
            self.remove(*A.get_family(), wh)
            wh2 = wh.copy()
            self.add(glyphs, wh2)
            shrink = VGroup(glyphs, wh2)
            k = mm.frame.width / A.width
            self.play(shrink.animate.scale(k).move_to(mm.get_center()), run_time=0.8)
            self.play(FadeOut(shrink), FadeIn(mm), run_time=0.4)

            card = your_card(["LLM to Agent: every cell, from", "“Define the LLM model and question”",
                              "to the Agent", ("paid per call", COST)])
            card.move_to([-0.3, -0.45, 0])
            vo.wait_until("Every call is paid")
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
