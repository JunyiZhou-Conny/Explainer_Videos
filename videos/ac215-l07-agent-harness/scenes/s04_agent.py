"""S04 · Act 1: an agent, measured (README "1 · Agent and tools", steps 1-2; the lecture's agent
recap and loop, slides 6-10, then the model/harness hand-off, slides 20-21).
Lecture: 6–10, then 20–21.

Beats (script.md "## S04", one voiceover block each):
 0  LECTURE 6–10. TRACKER Agent (section shown, no step lit yet). Slide 7 redrawn (AgentBlock) at
    centre: "Task / goal" arrows into a BLUE-outlined "Agent" box; "LLM core", "Instructions",
    "Tools" light in as named; "Memory" GREY dashed and dimmed with the GREY tag "act 4"; the bar
    "Dynamic control" and the dashed "Task completion" on "running until the task is done".
 1  The ends leave; the block shrinks (text keeps its size) into the top left. CODE(acts/
    act1_agent.py: 15–21) at 20 pt (7 lines, no wraps) under it: PURPLE tag "agent framework" beside
    `Agent(` (line 15); line 18 lights YELLOW and "Instructions" pulses; line 19 lights and "Tools"
    pulses; line 21 lights, `"response_format": AgentReply` turns YELLOW, GREY tag "structured
    reply" under the panel.
 2  LECTURE 20–21. The block leaves; the panel's code leaves, its frame reshapes and
    CODE(formaggio/agents/tools.py: 43–45) writes in (44 and 45 wrapped before "Never place" and
    before `"order_placed"`). Above it (slide 20, our drawing): the BLUE model, a PINK vertical
    seam, a GREEN gear "runtime" / "(the harness)"; caption "the model can only ask · the runtime
    runs the tool", its "·" on the seam, one baseline. A BLUE card `preview_order(items)` leaves the
    model, crosses the seam into the gear (which turns); a GREEN card "unvalidated_proposal / order
    placed: no" comes back across. `preview_order` (line 43) flashes; lines 44–45 light;
    `"order_placed": False` gets a GREEN box as the card's "order placed: no" pulses GREEN (one
    YELLOW bar over 44–45).
 3  TRACKER Agent 1. The picture leaves, its lecture tag with it. Container terminal (13 rows,
    TEAL), title-bar tags `no key` and (after the command is typed) GOLD `live · billed per token`.
    `python cli.py --act 1 --scenario standard` -> container/10 line 6 cut after "budget?" (2 rows)
    on "the ask", 8–9 on "call 1" (8 BLUE), 10 (2 rows) on "five tools" (its five tool names turn
    GREEN one by one), 11 folded after "You can find your API key at" (3 rows, RED) + 12 as 401s on
    "the call fails"; `Error code: 401` and `YOUR_OPE*******_KEY` boxed YELLOW, the YELLOW caption
    "the placeholder · replace it with your key" under the key; GREY top-band chip (in the lecture
    tag's place) "fix: README.md · lines 113–115, in this container shell" on "Fix it" (pulses on
    "three read lines"); line 13 (2 rows, GREY) with the row tag "evaluation finds it" on "The
    failed run".
 4  The terminal fades. V2 (Loop, from LoopMeter) driven by the staff's saved run (c23 lines 7–56),
    GREY tag "recorded · the staff's saved Colab run" at the top, LECTURE 20–21 back with it: the
    BLUE model, the stack (1 message, GREY: the customer's; each round adds the model's request BLUE
    and the result GREEN), the GOLD meter 1,942 with one tick, five GREEN-outlined tool paddles.
    Round 1 in steps on the narration: the request `get_catalog` crosses, the paddle lights, the
    result `products: 12 entries` comes back and goes in (stack 3, meter 3,013, a second tick).
    Round 2's request `check_stock` leaves the model and waits there.
 5  V2 dims to 20 % (Piece.dim_to; one opaque band behind the strip and the box takes the dimmed
    meter and the paddles under it whole). RECORDED(c23: 16–23) in a box (12.6 wide, 8 rows, lines
    22–23 cut at the box edge), its own recorded tag; a PINK dashed seam drawn across the box
    between lines 20 and 21 (a seam between two rows runs across them); slide 21's six-step strip
    above the box (Think → Reason → Plan | Execute → Verify → Response, PINK seam). "Plan" lights
    BLUE with line 19 `Requested tools: check_stock` BLUE; "Execute" lights GREEN with line 21 `Tool
    call 2: check_stock` GREEN. Excerpt chip README.md · line 198 "not hidden model reasoning" on
    "The trace shows" (pulses on "not hidden reasoning").
 6  The strip, box and chip leave; V2 brightens and plays rounds 2–5 fast (check_stock `ok: yes`,
    3,401; price_order `subtotal cents: 6400`, 3,554; get_pairings `bucheron: 3 entries`, 4,412;
    preview_order `status: unvalidated_proposal` / `order placed: no`, its second row ringed GREEN;
    a GOLD tick per call, six in all). Call 6: a BLUE answer card instead of a request, the paddles
    dim, the loop stops (stack 11, meter 4,540). The dimmed paddles make room for RECORDED(c23:
    52–56) (header names cell 23; line 55 BLUE). "Messages grew" pulses the stack and counter;
    "input from" pulses the meter and line 56's "4540 input tokens" turns GOLD; the GOLD total card
    "6 calls · 20,862 input + 895 output tokens · one answer" (GREY "the six calls' sums, lines
    11–56") writes in on "about 21,000"; the answer card pulses on "for one answer".
 7  TRACKER Agent 2. V2 and its lecture tag leave. Container terminal (13 rows), tags `no key` +
    GOLD live. `python cli.py --act 1 --scenario standard --show-json` (2 rows) -> container/11
    lines 8, 9 cut after "null means I have not provided that detail." (2 rows, broken at a space
    like a real terminal: a hanging indent would need a third row) on "a short note"; 10, 13–15,
    16–18 folded to `"allergies": [ "nuts" ],`, …, 27, 32 as 401s on "plus the confirmed request"
    (line 11, the customer ID, left out); the three JSON lines party_size / budget_cents / state
    turn GREEN; "null means I have not provided that detail" turns YELLOW on "where null". On
    "Pause": the terminal fades, the static GREY "your turn" card (▶): 401 fix (GREY), "with your
    key:", the two commands, "look for: …" (README.md · line 200), "no key: …" (GREY), GOLD "one
    answer ≈ six billed model calls". Hold 2 s.
 8  The card fades; LECTURE 10 arrives with the loop. Slide 10's loop rebuilt from V2's parts,
    small: the BLUE model, its stack of 11 messages, the GOLD meter at 4,540; a GREEN "tools" box, a
    GREEN dashed "tool outputs" box feeding back into the stack (the model's input); a GREY dashed
    "memory" box feeding up. The stack and the meter pulse on "The input grows". The question writes
    in RED: "How do we manage what goes into the LLM?" Everything fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    ManimColor,
    Rectangle,
    Rotate,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    Transform,
    VGroup,
    Write,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.devops import label, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ the real captures (file line numbers)
RUN = capture("container/10")
assert RUN.cmd == "python cli.py --act 1 --scenario standard", RUN.cmd
assert RUN.line(8) == "Model call 1 · Shop assistant · gpt-5.6-luna", RUN.line(8)
assert RUN.line(13).startswith("Inspect the recorded error with --list-runs and --inspect-run."), RUN.line(13)
ASK = RUN.cut(6, "budget?")                                           # 2 rows
E401 = RUN.as401(11, until="You can find your API key at")           # 3 rows, RED
STOP = RUN.as401(12, short=True)                                      # 1 row, RED

JSON_RUN = capture("container/11")
assert JSON_RUN.cmd == "python cli.py --act 1 --scenario standard --show-json", JSON_RUN.cmd
assert JSON_RUN.line(8) == "Exact customer message sent to the model:", JSON_RUN.line(8)
assert [JSON_RUN.line(n) for n in (13, 14, 15)] == ['  "party_size": 12,', '  "budget_cents": 15000,',
                                                    '  "state": "PA",']
assert JSON_RUN.line(10) == "{" and JSON_RUN.line(27) == "}"
NULL = "null means I have not provided that detail"
NOTE9 = JSON_RUN.cut(9, NULL + ".")
# line 9 as a real terminal shows it: broken at a space, the second row not indented (with the
# house hanging indent the " …" would need a third row and the panel would run to 14 rows)
_cut9 = NOTE9.index(" confirmed")
NOTE9_ROWS = [NOTE9[:_cut9], NOTE9[_cut9 + 1:]]
assert " ".join(NOTE9_ROWS) == NOTE9 and all(len(r) <= 65 for r in NOTE9_ROWS), NOTE9_ROWS
ALLERGIES = JSON_RUN.fold(16, 18, '  "allergies": [ "nuts" ],')
STOP11 = JSON_RUN.as401(32, short=True)

REC = "colab-c23-agent-harness"                                       # the staff's saved Act 1 run
_c23 = capture(f"expected/{REC}")
assert _c23.line(19) == "  Requested tools: check_stock" and _c23.line(21) == "  Tool call 2: check_stock"
assert _c23.line(55) == "  Response received; no tool calls requested."
assert _c23.line(56) == "  5.60s · 4540 input tokens · 399 output tokens"
assert len(C23) == 6 and C23[-1]["requested"] is None
TOT_IN, TOT_OUT = sum(TOKENS_IN), sum(TOKENS_OUT)
TOTAL = f"{len(C23)} calls · {TOT_IN:,} input + {TOT_OUT:,} output tokens · one answer"
assert TOTAL == "6 calls · 20,862 input + 895 output tokens · one answer", TOTAL
TOKEN_LINES = sorted(d["lines"]["tokens"] for d in C23)
SUMS = f"the six calls' sums, lines {TOKEN_LINES[0]}–{TOKEN_LINES[-1]}"
assert SUMS == "the six calls' sums, lines 11–56", SUMS

# README phrases (exact sub-strings or checked paraphrases with their line numbers)
R198 = "not hidden model reasoning"
assert R198 in source_line("README.md", 198)
assert source_line("README.md", 113).startswith("read -rsp ") and source_line("README.md", 115) == "printf '\\n'"
_r200 = source_line("README.md", 200)
assert "independent cart check" in _r200 and "distinguish a proposal from an order" in _r200, _r200
assert "Acts 1–2 have offline context preview" in source_line("README.md", 163)

# the code panels
assert source_line("acts/act1_agent.py", 15) == "    return Agent("
assert '"response_format": AgentReply' in source_line("acts/act1_agent.py", 21)
assert source_line("formaggio/agents/tools.py", 43).strip().startswith("def preview_order(")
assert '"order_placed": False' in source_line("formaggio/agents/tools.py", 45)

# ------------------------------------------------------------------ layout
T_ROWS = 13
BLOCK_K = 0.72                                   # beat 1: the agent block's shapes (text keeps 20 pt)
BLOCK_AT = np.array([-4.1, 1.75, 0])             # ... its frame's centre (under the tracker)
P1_BOTTOM = -2.8                                 # act1_agent.py panel (its code's bottom edge)
P2_BOTTOM = -2.95                                # tools.py panel
MODEL_AT = np.array([-5.3, 1.2, 0])              # beat 2's diagram (slide 20)
SEAM_X = 0.3
GEAR_AT = np.array([5.3, 1.15, 0])
REQ_Y, RES_Y = 1.5, 0.5
CARD_GAP = 0.9                                  # a card stops this far left of the gear's centre
DIM = 0.2                                        # beat 5: V2 dims to 20 %
STRIP_Y = 2.25                                   # ... slide 21's strip
BAND_LOW = -2.42                                 # ... the bottom of the opaque band behind strip and box
BOX16_TOP = 1.1                                  # ... the saved-output box's frame top
BOX16_W = 12.6                                   # ... its width (it covers the dimmed V2's middle)


# ------------------------------------------------------------------ small helpers
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


def flash(mob, color: str = TURN, k: float = 1.15):
    return Indicate(mob, color=color, scale_factor=k)


def row_tag(text: str, color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """A tag that fits inside one terminal row (the house tag is taller than a 22 pt row)."""
    t = label(text, size, color)
    h = 0.37
    b = RoundedRectangle(width=t.width + 0.36, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def box_around(mob, color: str, buff: float = 0.06, stroke: float = 3):
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=stroke, corner_radius=0.06)


def panel_bar(p, n: int, color: str = TURN, opacity: float = 0.2):
    """A translucent bar over file line n of a src_panel (all its rows)."""
    return p.bar(n, color, opacity)


def panel_bars(p, a: int, b: int, color: str = TURN, opacity: float = 0.2):
    """ONE translucent bar over file lines a..b of a src_panel (two bars would overlap in a
    brighter seam where they meet)."""
    bars = VGroup(*[panel_bar(p, n, color, opacity) for n in range(a, b + 1)])
    top, bot = bars.get_top()[1], bars.get_bottom()[1]
    one = Rectangle(width=bars.width, height=top - bot, stroke_width=0).set_fill(color, opacity)
    return one.move_to([bars.get_center()[0], (top + bot) / 2, 0])


def recolor_card(card, color: str):
    """A msg_card glyph in another colour (stroke + the same 30 % background mix as msg_card);
    opacities stay as they are (a hidden part stays hidden)."""
    card[0].set_stroke(color=color)
    card[0].set_fill(color=ManimColor(S.BG).interpolate(ManimColor(color), 0.3))
    return card


def stack_color(i: int) -> str:
    """Message i of the conversation: 0 the customer's message (GREY, as V4's user prompt), then
    per round the model's tool request (BLUE) and the tool's result (GREEN)."""
    return S.GREY if i == 0 else (CLOUD if i % 2 else HARNESS)


def hold_updaters(lm):
    """Take the counters' updaters off V2 (the message counter, the meter's number and bar) while
    it is dimmed: a DecimalNumber rebuilt every frame must not undo the dim. Returns them."""
    held = []
    for m in (lm.msgs.num, lm.meter.counter.num, lm.meter.bar):
        held.append((m, list(m.updaters)))
        m.clear_updaters()
    return held


def restore_updaters(held):
    for m, ups in held:
        for u in ups:
            m.add_updater(u)


class Loop(LoopMeter):
    """V2 with each round split into its steps (one play each), so every step can sit on its own
    narration anchor; call 6 (the answer) adds no tick: round 5 already counted call 6, whose
    input (4,540) the meter shows, so the six calls end with six ticks. The stack's cards are
    coloured by who wrote them (stack_color): the customer's message GREY, each round's request
    BLUE and its result GREEN."""

    def __init__(self, **kw):
        super().__init__(**kw)
        recolor_card(self.stack[0], stack_color(0))

    def _paddle_of(self, k: int):
        return self.paddles[C23[k]["requested"]]

    def emerge(self, scene, k: int, run_time: float = 0.4):
        """Call k+1's BLUE request card appears at the model's right edge. Returns it."""
        card = json_card([C23[k]["requested"]], CLOUD)
        card.move_to(self.model.get_right() + RIGHT * (0.2 + card.width / 2))
        scene.play(FadeIn(card, shift=RIGHT * 0.2), run_time=run_time)
        return card

    def fly(self, scene, k: int, card, run_time: float = 0.6):
        """The request crosses the lane and stops before its paddle, which lights."""
        p = self._paddle_of(k)
        target = p.frame.get_left() + LEFT * (0.25 + card.width / 2)
        scene.play(card.animate.move_to(target), p.frame.animate.set_stroke(TURN, 4),
                   p.text.animate.set_color(TURN), run_time=run_time)

    def execute(self, scene, k: int, card, run_time: float = 0.5):
        """The request goes into the paddle, then the GREEN result card comes out. Returns it."""
        p = self._paddle_of(k)
        res = json_card(RESULT_CHIPS[C23[k]["requested"]].split("; "), HARNESS)
        res.move_to(p.frame.get_left() + LEFT * (0.25 + res.width / 2))
        scene.play(FadeOut(card, shift=RIGHT * 0.3), run_time=run_time / 2)
        scene.play(FadeIn(res, shift=LEFT * 0.2), run_time=run_time / 2)
        return res

    def back(self, scene, k: int, res, run_time: float = 0.6):
        """The result travels back to the model; the paddle goes back to GREEN."""
        p = self._paddle_of(k)
        dest = self.model.get_right() + RIGHT * (0.2 + res.width / 2)
        scene.play(res.animate.move_to(dest), p.frame.animate.set_stroke(HARNESS, 3),
                   p.text.animate.set_color(INK), run_time=run_time)

    def absorb(self, scene, k: int, res, run_time: float = 0.6):
        """The result goes in: two more message cards (the model's request BLUE, the result
        GREEN), the counter and the meter move to call k+2's numbers (C23), one more GOLD tick."""
        new_cards = self._stack_cards(2, HARNESS)
        for j, c in enumerate(new_cards):
            recolor_card(c, stack_color(len(self.stack) + j))
        tick = cost_tick().next_to(self.tick_row[-1], RIGHT, buff=0.12)
        scene.play(FadeOut(res, scale=0.6), *[FadeIn(c, shift=DOWN * 0.1) for c in new_cards],
                   self.msgs.count_to(MSGS[k + 1], run_time), self.meter.set_to(TOKENS_IN[k + 1], run_time),
                   FadeIn(tick, scale=0.5), run_time=run_time)
        for c in new_cards:
            scene.remove(c)
            self.stack.add(c)
        scene.remove(tick)
        self.tick_row.add(tick)
        self.k_done = k + 1

    def fast_round(self, scene, k: int, rt: float = 1.0, card=None, hold=None):
        """One round in about rt seconds; the request's flight is short, the result card (the
        thing worth reading) stays up longest."""
        if card is None:
            card = self.emerge(scene, k, rt * 0.12)
        self.fly(scene, k, card, rt * 0.2)
        res = self.execute(scene, k, card, rt * 0.2)
        if hold is not None:
            hold(res)
        self.back(scene, k, res, rt * 0.26)
        self.absorb(scene, k, res, rt * 0.22)

    def answer6(self, scene, run_time: float = 1.4):
        """Call 6: a BLUE answer card instead of a request; the paddles dim; the loop stops."""
        card = json_card(["answer · no tool request"], CLOUD)
        card.move_to(self.model.get_right() + RIGHT * (0.2 + card.width / 2))
        scene.play(FadeIn(card, shift=RIGHT * 0.2), run_time=run_time * 0.45)
        scene.play(card.animate.shift(RIGHT * 1.6), *[p.animate.set_opacity(0.3) for p in self.paddles.values()],
                   run_time=run_time * 0.55)
        scene.remove(card)
        self.add(card)
        self.answer_card = card
        return card


def loop_diagram():
    """Beat 8: slide 10's loop from V2's own parts, small. Returns (group, parts dict)."""
    model = model_box("model", w=2.4, h=1.1, sub=MODEL_ID).move_to([-0.6, 0.85, 0])
    stack = VGroup(*[msg_card(1.2, 0.13, stack_color(i)) for i in range(MSGS[-1])])
    stack.arrange(UP, buff=0.04)
    place(stack, cx=-3.7, bottom=-0.25)
    msgs = label(f"messages: {MSGS[-1]}", CAPTION, INK).next_to(stack, UP, buff=0.15)
    meter = gold_meter("input tokens", TOKENS_IN[-1], cap=5000, w=3.0)
    meter.freeze()
    meter.move_to([-0.6, 2.3, 0])
    tools = VGroup(box(1.9, 0.75, HARNESS, fill_opacity=0.1, stroke=3), label("tools", CAPTION, INK))
    tools[1].move_to(tools[0])
    tools.move_to([3.6, 0.85, 0])
    outs_t = label("tool outputs", CAPTION, INK)
    outs = VGroup(box(outs_t.width + 0.5, 0.65, HARNESS, dashed=True, stroke=2.5), outs_t)
    outs_t.move_to(outs[0])
    outs.move_to([1.5, -0.75, 0])
    mem_t = label("memory", CAPTION, S.GREY)
    mem = VGroup(box(mem_t.width + 0.6, 0.65, S.GREY, dashed=True, stroke=2.5), mem_t)
    mem_t.move_to(mem[0])
    mem.move_to([-3.7, -1.35, 0])
    a_req = Arrow(model.get_right(), tools.get_left(), buff=0.12, color=CLOUD, stroke_width=4,
                  max_tip_length_to_length_ratio=0.12)
    a_down = Arrow(tools.get_bottom(), outs.get_right() + UP * 0.05, buff=0.1, color=HARNESS, stroke_width=4,
                   max_tip_length_to_length_ratio=0.15)
    a_in = Arrow(outs.get_left(), [stack.get_right()[0] + 0.02, stack.get_bottom()[1] + 0.3, 0], buff=0.12,
                 color=HARNESS,
                 stroke_width=4, max_tip_length_to_length_ratio=0.12)
    a_mem = Arrow(mem.get_top(), stack.get_bottom(), buff=0.1, color=S.GREY, stroke_width=4,
                  max_tip_length_to_length_ratio=0.3)
    a_stack = Arrow(stack.get_right() + UP * 0.35, model.get_left(), buff=0.12, color=S.GREY, stroke_width=4,
                    max_tip_length_to_length_ratio=0.2)
    parts = dict(model=model, stack=stack, msgs=msgs, meter=meter, tools=tools, outs=outs, mem=mem,
                 a_req=a_req, a_down=a_down, a_in=a_in, a_mem=a_mem, a_stack=a_stack)
    g = VGroup(*parts.values()).shift(RIGHT * 0.35)
    return g, parts


class AgentLoop(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0 · slide 7: the agent block
        tr = tracker("Agent")
        lr = lref("6–10")
        ab = AgentBlock(show=())
        ab.move_to([0, -0.1, 0])
        mt = ab.memory_tag("act 4")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(lr), run_time=0.5)
            ab.reveal(self, "task", "a_in", "box", run_time=0.8)
            self.wait(0.3)
            ab.reveal(self, "memory", run_time=0.4)
            self.play(FadeIn(mt, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("an agent is")
            ab.reveal(self, "core", run_time=0.4)
            self.play(flash(ab.block("core"), CLOUD), run_time=0.6)
            vo.wait_until("with instructions")
            ab.reveal(self, "instructions", run_time=0.4)
            self.play(flash(ab.block("instructions"), TURN), run_time=0.6)
            vo.wait_until("and tools")
            ab.reveal(self, "tools", run_time=0.5)
            vo.wait_until("running until")
            ab.reveal(self, "control", run_time=0.4)
            ab.reveal(self, "a_out", "done", run_time=0.5)
            self.play(flash(VGroup(ab.parts["a_out"], ab.parts["done"].text), INK, 1.1), run_time=0.6)

        # ========================================================== 1 · build_agent in code
        p1 = src_panel("acts/act1_agent.py", 15, 21, size=20)
        place(p1, cx=0)
        p1.shift(UP * (P1_BOTTOM - p1.code.get_bottom()[1]))
        agent_span = p1.span(15, "Agent(")
        row16_end = p1.span(16, "client,").get_right()[0]
        ftag = tag("agent framework", TOOL)
        place(ftag, left=max(agent_span.get_right()[0] + 0.35, row16_end + 0.35), cy=agent_span.get_center()[1])
        reply_span = p1.span(21, '"response_format": AgentReply')
        rtag = tag("structured reply", S.GREY)
        place(rtag, cx=reply_span.get_center()[0], top=p1.code.get_bottom()[1] - 0.08)
        with self.voiceover(SAY[1]) as vo:
            self.play(*ab.parts_out("task", "a_in", "a_out", "done"), FadeOut(mt), run_time=0.35)
            fc = ab.frame.get_center()
            self.play(ab.animate.rescale(BLOCK_K, about_point=fc).shift(BLOCK_AT - fc), run_time=0.6)
            mt.next_to(ab.frame, RIGHT, buff=0.15).set_y(ab.block("memory").get_center()[1])
            vo.wait_until("the function build agent")
            self.play(FadeIn(p1, shift=UP * 0.15), FadeIn(mt), run_time=0.6)
            vo.wait_until("makes one framework")
            self.play(FadeIn(ftag, shift=LEFT * 0.1), run_time=0.4)
            self.play(flash(agent_span, TOOL, 1.2), run_time=0.6)
            vo.wait_until("the shop instructions")
            bar = panel_bar(p1, 18)
            self.play(FadeIn(bar), run_time=0.3)
            self.play(flash(ab.block("instructions"), TURN, 1.15), run_time=0.7)
            vo.wait_until("five tools")
            bar19 = panel_bar(p1, 19)
            self.play(Transform(bar, bar19), run_time=0.35)
            self.play(flash(ab.block("tools"), HARNESS, 1.15), run_time=0.7)
            vo.wait_until("and a structured")
            bar21 = panel_bar(p1, 21)
            self.play(Transform(bar, bar21), reply_span.animate.set_color(TURN), run_time=0.4)
            self.play(FadeIn(rtag, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 2 · slide 20: the model can only ask
        p2 = src_panel("formaggio/agents/tools.py", 43, 45, wrap={44: ["Never place"], 45: ['"order_placed"']})
        place(p2, cx=0)
        p2.shift(UP * (P2_BOTTOM - p2.code.get_bottom()[1]))
        model = model_box("model", w=2.4, h=1.1, sub=MODEL_ID).move_to(MODEL_AT)
        seam = DashedLine([SEAM_X, 0.05, 0], [SEAM_X, 2.35, 0], color=LOOKUP, stroke_width=4, dash_length=0.1)
        gr = gear(0.45, HARNESS).move_to(GEAR_AT)
        # two rows (one row would run into the result card): "runtime" over "(the harness)"
        gr_t = VGroup(label("runtime", CAPTION, HARNESS), label("(the harness)", CAPTION, HARNESS))
        gr_t.arrange(DOWN, buff=0.06).next_to(gr, DOWN, buff=0.15)
        cap_l = label("the model can only ask", CAPTION, INK)
        cap_dot = label("·", CAPTION, LOOKUP)
        cap_r = label("the runtime runs the tool", CAPTION, INK)
        cap_dot.move_to([SEAM_X, 2.62, 0])
        cap_l.next_to(cap_dot, LEFT, buff=0.2)
        cap_r.next_to(cap_dot, RIGHT, buff=0.2).align_to(cap_l, UP)   # one baseline (cap_l has a descender)
        cap = VGroup(cap_l, cap_dot, cap_r)
        req = json_card(["preview_order(items)"], CLOUD)
        req.move_to([model.get_right()[0] + 0.15 + req.width / 2, REQ_Y, 0])
        res = json_card(["unvalidated_proposal", "order placed: no"], HARNESS)
        res.move_to([GEAR_AT[0] - CARD_GAP - res.width / 2, RES_Y, 0])
        assert req.get_right()[0] < SEAM_X - 0.1 and res.get_left()[0] > SEAM_X + 0.1
        op_box = box_around(p2.span(45, '"order_placed": False'), HARNESS)
        with self.voiceover(SAY[2]) as vo:
            lr_new = lref("20–21")
            old_bg = p1.code.background
            self.play(FadeOut(VGroup(p1.code.code_lines, p1.header, bar, ftag, rtag)), FadeOut(ab), FadeOut(mt),
                      Succession(FadeOut(lr), FadeIn(lr_new)), run_time=0.5)
            lr = lr_new
            self.play(Transform(old_bg, p2.code.background), FadeIn(model), Create(seam), FadeIn(gr), FadeIn(gr_t),
                      run_time=0.5)
            self.remove(old_bg)
            self.add(p2.code.background)
            self.play(FadeIn(p2.code.code_lines), FadeIn(p2.header), run_time=0.4)
            self.remove(p2.code.background, p2.code.code_lines, p2.header)
            self.add(p2)
            self.play(FadeIn(req, shift=RIGHT * 0.3), run_time=0.5)
            vo.wait_until("the harness runs it")
            self.play(req.animate.move_to([GEAR_AT[0] - CARD_GAP - req.width / 2, REQ_Y, 0]), FadeIn(cap), run_time=0.7)
            self.play(FadeOut(req, shift=RIGHT * 0.3, scale=0.7), Rotate(gr, angle=-PI / 2), run_time=0.7)
            vo.wait_until("And none of these")
            self.play(FadeIn(res, shift=LEFT * 0.2), run_time=0.4)
            self.play(res.animate.move_to([model.get_right()[0] + 0.15 + res.width / 2, RES_Y, 0]), run_time=0.9)
            vo.wait_until("the preview order tool")
            self.play(flash(p2.span(43, "preview_order"), TURN, 1.2), run_time=0.7)
            vo.wait_until("records an unvalidated")
            bars2 = panel_bars(p2, 44, 45)
            self.play(FadeIn(bars2), run_time=0.4)
            vo.wait_until("with order placed")
            self.play(Create(op_box), res.rows[1].animate.set_color(HARNESS), run_time=0.5)
            self.play(flash(res.rows[1], HARNESS, 1.15), run_time=0.7)

        # ========================================================== 3 · step 1: the live run, the 401
        t = term(container=True, rows=T_ROWS)
        ft = frame_tags(t, nokey_tag(), live_tag())
        nk, lv = ft[0], ft[1]
        fix = top_chip("fix: README.md · lines 113–115, in this container shell", color=S.GREY, tall=True)
        # the lecture tag leaves with slide 20's picture (it sits only over the picture it cites), so
        # the chip can move up off the frame tags into the tag's place
        fix.shift(UP * 0.15)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p2, bars2, op_box, model, seam, gr, gr_t, cap, res)), FadeOut(lr), tr.goto(1),
                      run_time=0.5)
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(nk, shift=DOWN * 0.1), run_time=0.5)
            type_cmd(self, t, RUN.cmd, 3.4)
            self.play(FadeIn(lv, shift=DOWN * 0.1), run_time=0.4)
            self.play(flash(lv.text, COST, 1.15), run_time=0.6)
            vo.wait_until("You see the ask")
            show(self, t, RUN, ASK, wrap=True, run_time=0.5)
            vo.wait_until("call 1")
            show(self, t, RUN, 8, 9, run_time=0.4)
            vo.wait_until("and five tools")
            r10 = show(self, t, RUN, 10, wrap=True, run_time=0.4)
            self.play(LaggedStart(*[wrapped_glyphs(r10, name).animate.set_color(HARNESS) for name in TOOLS_ACT1],
                                  lag_ratio=0.35), run_time=0.9)
            vo.wait_until("then the call fails")
            r11 = show(self, t, RUN, E401, STOP, wrap=True, run_time=0.6)
            e_rows = item_rows(r11, 0)
            vo.wait_until("with error 401")
            boxes = VGroup()
            for sub in ("Error code: 401", KEY_MASKED):
                row, col = wrapped_at(e_rows, sub)
                boxes.add(col_box(row, col, col + len(sub), TURN))
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.4), run_time=0.7)
            vo.wait_until("the placeholder key")
            key_row, key_col = wrapped_at(e_rows, KEY_MASKED)
            capk = label("the placeholder · replace it with your key", CAPTION, TURN)
            r3 = e_rows[-1]
            place(capk, left=boxes[1].get_left()[0], cy=r3.strut.get_center()[1])
            assert capk.get_left()[0] > r3.glyphs.get_right()[0] + 0.3 and capk.get_right()[0] < t.box.get_right()[0]
            pin(self, r3, capk, run_time=0.5)
            vo.wait_until("Fix it")
            self.play(FadeIn(fix, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("with the three read")
            self.play(flash(fix, S.GREY, 1.08), run_time=0.7)
            vo.wait_until("The failed run")
            r13 = show(self, t, RUN, (RUN.line(13), S.GREY), wrap=True, run_time=0.5)
            etag = row_tag("evaluation finds it")
            beside(etag, t, r13[-1], buff=0.45)
            pin(self, r13[-1], etag, run_time=0.4)

        # ========================================================== 4 · V2: the staff's saved run, round 1
        lm = Loop(show=())
        rtag4 = recorded_tag().move_to([0.3, 2.64, 0])
        lr = lref("20–21")                  # back with V2: the model asks, the harness runs (20); the seam (21)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(t, ft, fix, boxes)), run_time=0.5)
            lm.reveal(self, "model", "stack", "msgs", "paddles", "title", run_time=0.6, extra=(FadeIn(lr),))
            lm.reveal(self, "meter", "ticks", run_time=0.4)
            vo.wait_until("from the staff")
            self.play(FadeIn(rtag4, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("The model asks")
            card = lm.emerge(self, 0, 0.4)
            lm.fly(self, 0, card, 0.8)
            vo.wait_until("the harness runs it")
            res0 = lm.execute(self, 0, card, 0.7)
            vo.wait_until("and the result goes")
            lm.back(self, 0, res0, 0.8)
            vo.wait_until("two more messages")
            lm.absorb(self, 0, res0, 0.7)
            card1 = lm.emerge(self, 1, 0.4)

        # ========================================================== 5 · slide 21: the seam in one round
        box16 = recorded_box(REC, (16, 23), width=BOX16_W)
        box16.shift(UP * (BOX16_TOP - box16.frame.get_top()[1]) + RIGHT * (0 - box16.frame.get_center()[0]))
        rows16 = box16.rows
        # halfway between line 20's descenders and line 21's ascenders (the struts overlap, so their
        # midpoint sat on line 21's tops)
        y_seam = (rows16[4].glyphs.get_bottom()[1] + rows16[5].glyphs.get_top()[1]) / 2
        bseam = DashedLine([box16.frame.get_left()[0] - 0.25, y_seam, 0], [box16.frame.get_right()[0] + 0.25, y_seam, 0],
                           color=LOOKUP, stroke_width=4, dash_length=0.1)
        strip = SixSteps().move_to([0, STRIP_Y, 0])
        # one opaque band behind the strip and the box: the dimmed meter, ticks and all five paddles
        # go under it whole (no half-hidden paddle edges peeking out above or below the box); the
        # dimmed stack and "tools · run by the harness" stay visible below it
        backing = Rectangle(width=13.2, height=2.9 - BAND_LOW, stroke_width=0).set_fill(S.BG, 1)
        backing.move_to([0, (2.9 + BAND_LOW) / 2, 0])
        ex = excerpt_chip(R198, "README.md · line 198 (excerpt)", line=source_line("README.md", 198))
        place(ex, cx=0, top=box16.frame.get_bottom()[1] - 0.2)
        with self.voiceover(SAY[5]) as vo:
            held = hold_updaters(lm)
            lm.add(card1, rtag4)                                   # they dim with V2 (taken out again in 6)
            self.play(lm.dim_to(DIM), run_time=0.4)
            self.play(FadeIn(backing), FadeIn(strip), FadeIn(box16, shift=UP * 0.1), run_time=0.6)
            self.play(Create(bseam), run_time=0.5)
            self.play(flash(strip.seam, LOOKUP, 1.1), flash(bseam, LOOKUP, 1.05), run_time=0.7)
            vo.wait_until("The model's plan")
            self.play(strip.light("Plan"), rows16[3].glyphs.animate.set_color(CLOUD), run_time=0.5)
            self.play(flash(rows16[3].glyphs, CLOUD, 1.06), run_time=0.6)
            vo.wait_until("the harness executes")
            ex_chip = strip.chips["Execute"]               # Plan stays lit: both sides of the seam
            self.play(ex_chip.box.animate.set_fill(HARNESS, 0.4).set_stroke(HARNESS, 4),
                      rows16[5].glyphs.animate.set_color(HARNESS), run_time=0.5)
            self.play(flash(rows16[5].glyphs, HARNESS, 1.06), run_time=0.6)
            vo.wait_until("The trace shows")
            self.play(FadeIn(ex, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("not hidden reasoning")
            self.play(flash(ex.text, TURN, 1.1), run_time=0.7)

        # ========================================================== 6 · rounds 2-5, call 6, the bill
        box52 = recorded_box(REC, (52, 56), tag_=False)
        place(box52, right=6.45)
        box52.shift(UP * (-3.35 - box52.frame.get_bottom()[1]))
        rows52 = box52.rows
        total_t = label(TOTAL, 22, COST)
        total = VGroup(box(total_t.width + 0.5, total_t.height + 0.36, COST, fill=S.BG, fill_opacity=0.95,
                           stroke=2.5), total_t)
        total_t.move_to(total[0])
        total.move_to([-0.2, 1.5, 0])
        sums = label(SUMS, CAPTION, S.GREY).next_to(total, DOWN, buff=0.1)

        def ring_last(res_card):
            ring_ = box_around(res_card.rows[1], HARNESS, buff=0.05)
            self.play(Create(ring_), res_card.rows[1].animate.set_color(HARNESS), run_time=0.35)
            self.wait(0.25)
            self.remove(ring_)
            res_card.add(ring_)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(box16, bseam, strip, backing, ex)), lm.undim(), run_time=0.45)
            lm.remove(card1, rtag4)
            restore_updaters(held)
            # 0.9 s a round: "preview" is said about 2.5 s in, the answer comes on "answers"
            lm.fast_round(self, 1, 0.9, card=card1)
            for k in (2, 3):
                lm.fast_round(self, k, 0.9)
            lm.fast_round(self, 4, 0.9, hold=ring_last)
            vo.wait_until("On call 6")
            ans = lm.answer6(self, 1.2)
            self.play(*lm.parts_out("paddles", "title"), run_time=0.4)
            self.play(FadeIn(box52, shift=UP * 0.1), rows52[3].glyphs.animate.set_color(CLOUD), run_time=0.5)
            vo.wait_until("Messages grew")
            self.play(flash(lm.msgs, TURN, 1.2), flash(lm.stack, TURN, 1.08), run_time=0.8)
            vo.wait_until("input from")
            tok = substring(rows52[4], "4540 input tokens")
            self.play(flash(lm.meter, COST, 1.1), tok.animate.set_color(COST), run_time=0.8)
            vo.wait_until("about 21,000")
            self.play(FadeIn(total[0]), Write(total_t), run_time=0.9)
            self.play(FadeIn(sums, shift=UP * 0.05), run_time=0.4)
            vo.wait_until("for one answer")
            self.play(flash(ans, CLOUD, 1.08), run_time=0.7)

        # ========================================================== 7 · step 2: --show-json; your turn
        lm.freeze()
        t2 = term(container=True, rows=T_ROWS)
        ft2 = frame_tags(t2, nokey_tag(), live_tag())
        nk2, lv2 = ft2[0], ft2[1]
        card_rows_ = [
            ["401? set the key in the container:", "`read -rsp …`", "(README.md · lines 113–115)"],
            Prose("with your key:"),
            RUN.cmd,
            JSON_RUN.cmd,
            Prose("look for: the independent cart check · a proposal, not an order (README.md · line 200)"),
            ["no key: acts 1–2 have no", "`--fixture`", "(README.md · line 163)"],
            (Prose("one answer ≈ six billed model calls"), COST),
        ]
        tc = turn_card(card_rows_)
        tc.rows[0].set_color(S.GREY)
        tc.rows[5].set_color(S.GREY)
        tc.move_to([0, -0.3, 0])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(lm, rtag4, box52, total, sums)), FadeOut(lr), tr.goto(2), run_time=0.5)
            self.play(FadeIn(t2, shift=UP * 0.2), FadeIn(nk2, shift=DOWN * 0.1), run_time=0.5)
            type_cmd(self, t2, JSON_RUN.cmd, 2.2)
            self.play(FadeIn(lv2, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("a short note")
            note_rows = show(self, t2, JSON_RUN, 8, (NOTE9_ROWS[0], OUTPUT), (NOTE9_ROWS[1], OUTPUT), run_time=0.5)
            vo.wait_until("plus the confirmed")
            js = show(self, t2, JSON_RUN, 10, (13, 15), ALLERGIES, "…", 27, STOP11, run_time=0.8)
            self.play(LaggedStart(*[js[i].glyphs.animate.set_color(HARNESS) for i in (1, 2, 3)], lag_ratio=0.4),
                      run_time=0.9)
            vo.wait_until("where null")
            nl = substring(note_rows[2], NULL)
            self.play(nl.animate.set_color(TURN), run_time=0.4)
            self.play(flash(nl, TURN, 1.04), run_time=0.6)
            vo.wait_until("Pause and run")
            self.play(FadeOut(VGroup(t2, ft2)), run_time=0.4)
            self.play(FadeIn(tc, scale=0.97), run_time=0.5)
        self.wait(2)

        # ========================================================== 8 · slide 10: the loop and its question
        lr = lref("10")
        dg, dp = loop_diagram()
        q = label("How do we manage what goes into the LLM?", 28, ERR).move_to([0.2, -2.55, 0])
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(tc), run_time=0.4)
            self.play(FadeIn(VGroup(dp["model"], dp["stack"], dp["msgs"], dp["meter"])), FadeIn(lr), run_time=0.5)
            self.play(GrowArrow(dp["a_stack"]), GrowArrow(dp["a_req"]), FadeIn(dp["tools"]), run_time=0.5)
            self.play(GrowArrow(dp["a_down"]), FadeIn(dp["outs"]), GrowArrow(dp["a_in"]),
                      FadeIn(dp["mem"]), GrowArrow(dp["a_mem"]), run_time=0.6)
            self.play(flash(dp["stack"], TURN, 1.08), flash(dp["meter"], COST, 1.08), run_time=0.7)
            vo.wait_until("That's the lecture's")
            self.play(Write(q), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(VGroup(dg, q, tr, lr)), run_time=0.8)
        self.wait(0.3)
