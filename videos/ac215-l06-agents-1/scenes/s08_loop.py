"""S08 · From two calls to a loop (no tracker until the teardown; lecture slides 26, then 35–41).

Beats (script.md "## S08", one voiceover block each):
0. LECTURE 26. No tracker. The V1 mini-map (bottom right) lights Dynamic Control YELLOW. The
   definition card returns, "until the task is done" underlined YELLOW; under it llm-rag's run as
   one short line (BLUE "call 1 · forced tool call" → TEAL "your code runs it" → BLUE "call 2 ·
   answer" → GREY "end"), then a GREY brace "one lap"; a README chip (README.md · line 246
   (excerpt), tag expected) "AI Agent (Cheese Expert Agent)".
1. The lecture tag, the cards and the mini-map leave (the one-lap line too: the panel and the
   ponder card fill the frame). CODE(cli.py: 474–481), 8 rows: lines 474–476 YELLOW with a GREY
   dashed ghost "no tool_config" inside line 476; line 478 GREY; line 481 GREY with the label
   "agent() ends here". PONDER (8 s) in the lower third.
2. The panel moves down, the one-lap line returns on top. Line 478 YELLOW (the 474–476 bar steps
   back to GREY: line 478 is the narrated line); a BLUE function-call
   card {name, args} drops out of "call 2" (GREY "no text"); "end" flashes with line 481; the card's
   frame turns RED, tag "never run"; a GREY dashed arrow loops from the card back to "your code
   runs it", caption "a loop would run it and ask again".
3. LECTURE 35–40. V4: the BLUE "LLM core" and the GREY "instructions" sink into the hub "decision
   maker"; two-way spokes grow to planner, tools and memory as named. Unrolled: the hub becomes the
   BLUE "model" station, the tools node the PURPLE "tools" station, the tools spoke the circular
   track (planner and memory fade).
4. The YELLOW token runs laps, the counter ticks 1 / 12, 2 / 12; the YELLOW gate "final response"
   and the caption "stop rule: a reply with no function call" appear; on turn 3 the model station
   emits a GREY "plain text" card, the gate opens and the card passes.
5. The track shrinks to the top left, PURPLE caption "inside ADK, simplified: model → tools, until
   the reply is final" + tag illustration. CODE(4-production-ready/app/runner.py: 39–48) with a GREY
   chip "ADK repo · module 4 · code only": line 40 PURPLE "the Runner streams events"; lines 45–46
   YELLOW "final response". The token runs a lap.
6. The track returns full size on the left with its counter (0 / 12), the gate along the top.
   CODE(Cheese Quiz · cell 71: 5–7) `max_turns=12` and CODE(Cheese Newsletter · cell 25: 8, GREY
   subtitle “Orchestrator Agent”) `"max_iterations": 16` write in bottom right and are boxed YELLOW
   as named; a PURPLE chip on each header row names the framework (OpenAI Agents SDK: this Runner
   is not ADK's; Microsoft Agent Framework). Replay: the token races to 12 / 12 (RED), the gate slams RED "MaxTurnsExceeded".
7. LECTURE 41. V1's anatomy (slide 41: no Task/Goal ends), the track beside it: Dynamic Control
   GREY dashed, its name grays out; the four blocks light (white outline) as named; the track flies
   into the bar, which fills PURPLE; caption "the framework writes this part".
8. TRACKER Run 3 · extra. The TEAL container terminal (8 rows) types `exit` (extra) →
   TERM(laptop/06: 42; session); the frame turns GREY (title laptop, prompt ~/AC215/llm-rag$).
   `docker ps --format 'table …'` (extra; folds) → TERM(laptop/12: 2–3) as the NAMES and PORTS
   columns (GREY tag "IMAGE not shown", as in S05): the port PINK in a PINK box, PINK tag "still up".
   `docker compose down` (extra) → TERM(laptop/13: 2–3 joined, 4, both wrapped; 5–7 with their
   times as GREY tags): the warnings turn GREY, tag "harmless"; the two "Removed" rows flash.
9. A GREEN chip "docker-volumes/: your index stays" and a PINK chip "port 8000 → free for part 2"
   write in above the terminal, then fade; ▶ your turn on a static GREY card (exit · docker compose
   down, both extra). Hold 2 s. Everything fades: an empty frame (the end of part 1).
"""

import numpy as np
from common import (
    CLOUD,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MINI_CENTER,
    NARRATION,
    P_CTR,
    TOOL,
    TURN,
    Anatomy,
    AnatomyMini,
    HubSpokes,
    LoopTrack,
    bare_prompt,
    beside,
    call_card,
    caption_extra,
    capture,
    col_box,
    definition_card,
    excerpt,
    extra_tag,
    grey_tag,
    harmless_tag,
    illustration_tag,
    leave_container,
    lref,
    lref_swap,
    note,
    one_lap_row,
    pin,
    ponder_at,
    print_build,
    readme_chip,
    session,
    src_panel,
    term,
    tracker,
    turn_card,
    type_cmd,
    under,
)
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    TAU,
    UP,
    Brace,
    Create,
    CurvedArrow,
    DashedVMobject,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Rectangle,
    ReplacementTransform,
    Rotate,
    SurroundingRectangle,
    Transform,
    VGroup,
    Write,
    linear,
    smooth,
    squish_rate_func,
    there_and_back,
)
from manim.animation.animation import prepare_animation

from explainer import style as S
from explainer.devops import box, chip, label, mono, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S08"]

# ------------------------------------------------------------------ the real sources
C06 = capture("06", "laptop")          # docker-shell.sh session: line 41 = container prompt + exit, 42 "exit"
C12 = capture("12", "laptop")          # extra: docker ps after exit
C13 = capture("13", "laptop")          # extra: docker compose down
assert C06.line(41) == P_CTR + " exit" and C06.line(42) == "exit", (C06.line(41), C06.line(42))
assert C12.cmd == "docker ps --format 'table {{.Names}}\\t{{.Image}}\\t{{.Ports}}'", C12.cmd
assert C13.cmd == "docker compose down", C13.cmd
WARN_1 = C13.join(2, 3)                # the GOOGLE_APPLICATION_CREDENTIALS warning, wrapped at 80 columns
WARN_2 = C13.line(4)
assert WARN_1.startswith("WARN[0000]") and WARN_2.startswith("WARN[0000]")
PORT = "0.0.0.0:8000->8000/tcp"

README_PHRASE = "AI Agent (Cheese Expert Agent)"
assert README_PHRASE in excerpt("README.md", 246, 246)
PONDER_Q = ("Call 2 hands the model the tools again, but no tool_config.\n"
            "Suppose Gemini answers with another function call.\n"
            "What does cli.py do?")
assert "tool_config" not in excerpt("cli.py", 474, 477)          # call 2's config: tools only
assert "max_turns=12" in excerpt("colab/cheese-quiz/cell-71.py", 6, 6)
assert '"max_iterations": 16' in excerpt("colab/cheese-newsletter/cell-25.py", 8, 8)
assert "is_final_response()" in excerpt("4-production-ready/app/runner.py", 45, 45)

RUNNER = "4-production-ready/app/runner.py"


# ------------------------------------------------------------------ helpers
def ps_columns(cap, nums=(2, 3), keep=("NAMES", "PORTS")) -> list[str]:
    """`docker ps --format 'table …'` rows cut down to the named columns (as S05 shows them), each
    column at its own width and offset: the data row is 66 characters, the house terminal 65."""
    head = cap.line(nums[0])
    names = head.split()
    starts = [head.index(n) for n in names]
    spans = dict(zip(names, zip(starts, starts[1:] + [None])))
    out = []
    for n in nums:
        s = cap.line(n)
        row = "".join(s[a:b] if b is not None else s[a:] for a, b in (spans[k] for k in keep)).rstrip()
        out.append(row)
    assert all(len(r) <= 65 for r in out), out
    return out


def span_bar(p, a: int, b: int, color: str = TURN, opacity: float = 0.18) -> Rectangle:
    """One translucent bar over file lines a..b of a src_panel (line bars of neighbouring rows
    overlap and leave darker stripes)."""
    bars = VGroup(*[p.bar(n, color, opacity) for n in range(a, b + 1)])
    r = Rectangle(width=bars.width, height=bars.height, stroke_width=0).set_fill(color, opacity)
    return r.move_to(bars)


def code_row(p, n: int, k: int = 0):
    """The k-th code row of file line n in a src_panel."""
    return p.code.code_lines[p.rows_of(n)[k]]


def ghost(pre: str, code: str, color: str = S.GREY, size: float = 20, pad_y: float = 0.05) -> VGroup:
    """A GREY dashed ghost of something absent: a serif word and a mono name in a dashed box, no
    taller than one code row (pitch 0.345) so it sits inside the row it belongs to."""
    row = VGroup(label(pre, size, color), mono(code, size, color)).arrange(RIGHT, buff=0.12)
    fr = box(row.width + 0.4, mono("|", size).height + pad_y, color, dashed=True, radius=0.08)
    fr.move_to(row)
    g = VGroup(fr, row)
    g.frame, g.row = fr, row
    return g


def dashed_curve(start, end, angle: float, color: str = S.GREY) -> VGroup:
    """A dashed curved arrow (the loop that llm-rag doesn't have)."""
    a = CurvedArrow(start, end, angle=angle, color=color, stroke_width=3, tip_length=0.2)
    tips = a.pop_tips()
    body = DashedVMobject(a, num_dashes=18, dashed_ratio=0.55).set_stroke(color, 3)
    return VGroup(body, tips)


def mixed_chip(parts, color: str, size: float = 22) -> VGroup:
    """A chip whose text mixes mono and serif: parts = [("`mono`" | "serif"), …]."""
    mobs = [mono(p[1:-1], size, INK) if p.startswith("`") else label(p, size, INK) for p in parts]
    row = VGroup(*mobs).arrange(RIGHT, buff=0.12)
    h = mono("|", size).height + 0.24
    b = box(row.width + 0.5, h, color, fill_opacity=0.16, radius=h / 2.6)
    row.move_to(b)
    g = VGroup(b, row)
    g.box, g.text = b, row
    return g


def morph_track(scene, src, dst, names=("track", "model", "tools", "token"), extra=(),
                run_time: float = 1.0):
    """The named parts of LoopTrack `src` become those of `dst` (the rest of src fades); then src
    leaves the scene and dst is on it as one piece."""
    keep = [src.parts[n] for n in names]
    rest = [m for m in src.submobjects if m not in keep]
    # the rest fades first, then the parts travel (the shrinking track crossed the fading counter)
    scene.play(*[ReplacementTransform(src.parts[n], dst.parts[n], rate_func=squish_rate_func(smooth, 0.3, 1.0))
                 for n in names],
               *[FadeOut(m, rate_func=squish_rate_func(smooth, 0.0, 0.4)) for m in rest], *extra,
               run_time=run_time)
    scene.remove(*src.get_family())
    scene.remove(*[dst.parts[n] for n in names])
    scene.add(dst)
    return dst


def tick(lt, k: int, color: str = INK, run_time: float = 0.25):
    """Animation: LoopTrack lt's counter jumps to k (its number in `color`)."""
    lt.count = k
    cnt = lt.parts["counter"]
    new = lt._counter_text(k).move_to(cnt)
    new[0].set_color(color)
    return Transform(cnt, new, run_time=run_time)


def run_lap(scene, lt, run_time: float = 1.0, color: str = INK, tick_time: float = 0.25):
    """One clockwise lap of the token, then the counter ticks (two plays: LoopTrack.lap()'s
    Succession adds a wrapper group to the scene that draws the token over the stations)."""
    scene.play(Rotate(lt.parts["token"], angle=-TAU, about_point=lt._c.get_center(), rate_func=linear),
               run_time=run_time)
    scene.play(tick(lt, lt.count + 1, color, tick_time))


def lap_to_model(lt, run_time: float = 0.5):
    """Animation: the token climbs a quarter lap, from the track's left to the model station."""
    return Rotate(lt.parts["token"], angle=-TAU / 4, about_point=lt._c.get_center(), rate_func=linear,
                  run_time=run_time)


class TheLoop(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ============================================================ 0 · one lap vs "until done"
        lr = lref("26")
        mm = AnatomyMini(center=MINI_CENTER)
        dc = definition_card()
        dc.move_to([0, 2.3, 0])
        row = one_lap_row()
        row.move_to([0, 0.9, 0])
        call1, mine, call2, end = row.steps
        brace = Brace(row, DOWN, buff=0.1, color=S.GREY)
        one = label("one lap", 22, S.GREY).next_to(brace, DOWN, buff=0.06)
        rc = readme_chip("README.md · line 246 (excerpt)", README_PHRASE, expected=True)
        rc.move_to([0, -1.0, 0])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(lr), FadeIn(dc, shift=DOWN * 0.15), FadeIn(mm), run_time=0.8)
            self.play(mm.light("control"), run_time=0.5)
            vo.wait_until("until the task is done")
            und = under(dc.until, TURN, stroke=3)
            self.play(Create(und), run_time=0.6)
            vo.wait_until("L-L-M rag's agent ran one lap")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.12) for m in row], lag_ratio=0.35),
                      run_time=2.0)
            vo.wait_until("a forced tool call")
            self.play(Indicate(call1, color=CLOUD, scale_factor=1.08), run_time=0.7)
            vo.wait_until("then an answer")
            self.play(Indicate(call2, color=CLOUD, scale_factor=1.08), run_time=0.7)
            vo.wait_until("The README calls it an agent")
            self.play(FadeIn(rc, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("by the lecture's definition")
            self.play(GrowFromCenter(brace), FadeIn(one, shift=UP * 0.1),
                      Indicate(und, color=TURN, scale_factor=1.15), run_time=0.8)
            self.play(Indicate(mm.items["control"], color=TURN, scale_factor=1.15), run_time=0.8)

        # ============================================================ 1 · call 2's config; PONDER
        p1 = src_panel("cli.py", 474, 481)
        p1.shift(UP * (3.45 - p1.get_top()[1]) - RIGHT * p1.get_center()[0])
        bars_cfg = span_bar(p1, 474, 476)
        gh = ghost("no", "tool_config").next_to(code_row(p1, 476), RIGHT, buff=0.6)
        bar478 = p1.bar(478, S.GREY, 0.25)
        bar481 = p1.bar(481, S.GREY, 0.25)
        lab481 = VGroup(mono("agent()", 22, S.GREY), label("ends here", 22, S.GREY)).arrange(RIGHT, buff=0.14)
        lab481.next_to(code_row(p1, 481), RIGHT, buff=0.6)
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in (dc, und, row, brace, one, rc, mm, lr)], run_time=0.6)
            self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(bars_cfg), FadeIn(gh, shift=LEFT * 0.1), run_time=0.6)
            self.play(FadeIn(bar478), FadeIn(bar481), FadeIn(lab481, shift=LEFT * 0.1), run_time=0.5)
        card = ponder_at(self, PONDER_Q, 8)

        # ============================================================ 2 · the call nobody runs
        anno = VGroup(p1, bars_cfg, gh, bar478, bar481, lab481)
        row.move_to([0, 3.2, 0])
        fc = call_card(rows=("{name, args}",))
        fc.next_to(call2, DOWN, buff=0.55)
        nt = note("no text", size=22).next_to(fc, RIGHT, buff=0.3)
        never = tag("never run", ERR).next_to(fc, DOWN, buff=0.2)
        with self.voiceover(SAY[2]) as vo:
            # the ponder card leaves first, then the panel slides down through its place
            self.play(FadeOut(card, rate_func=squish_rate_func(smooth, 0.0, 0.4)),
                      anno.animate(rate_func=squish_rate_func(smooth, 0.3, 1.0)).shift(DOWN * (p1.get_bottom()[1] + 3.5)),
                      FadeIn(row, rate_func=squish_rate_func(smooth, 0.6, 1.0)), run_time=0.8)
            # line 478 is the narrated line now: the config bar steps back to GREY
            self.play(bar478.animate.set_fill(TURN, 0.22), bars_cfg.animate.set_fill(S.GREY, 0.14),
                      run_time=0.4)
            self.play(FadeIn(fc, target_position=call2.get_center(), scale=0.4), run_time=0.8)
            vo.wait_until("with no text")
            self.play(FadeIn(nt, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("and the program ends")
            self.play(Indicate(end, color=INK, scale_factor=1.15), Indicate(lab481, color=INK, scale_factor=1.06),
                      run_time=0.8)
            vo.wait_until("Nothing runs that call")
            self.play(fc.frame.animate.set_stroke(ERR, 3), FadeIn(never, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a loop would run it")
            loop = dashed_curve(fc.get_left() + LEFT * 0.12, mine.get_bottom() + DOWN * 0.1, -PI / 2)
            loop_cap = label("a loop would run it and ask again", 22, S.GREY)
            loop_cap.next_to(loop, LEFT, buff=0.25).shift(DOWN * 0.35)
            self.play(Create(loop), run_time=0.9)
            self.play(FadeIn(loop_cap, shift=RIGHT * 0.1), run_time=0.5)

        # ============================================================ 3 · the hub (slides 35–40), unrolled
        hs = HubSpokes(show=("core", "sheet"))
        lt = LoopTrack(show=("track", "model", "tools"))
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in (row, fc, nt, never, loop, loop_cap, anno)], run_time=0.6)
            lr = lref("35–40")
            self.play(FadeIn(lr), FadeIn(hs), run_time=0.6)
            vo.wait_until("the core and its instructions")
            self.play(Indicate(hs.parts["core"], color=CLOUD, scale_factor=1.08),
                      Indicate(hs.parts["sheet"], color=INK, scale_factor=1.08), run_time=0.7)
            vo.wait_until("become a decision maker")
            self.play(*hs.parts_in("becomes"), run_time=0.4)
            self.wait(0.3)
            # "becomes" leaves first, then the core and the sheet sink into the hub (they crossed it)
            sink = [prepare_animation(a) for a in hs.merge()]
            for a in sink:
                a.rate_func = squish_rate_func(smooth, 0.25, 1.0)
            fade = [prepare_animation(a) for a in hs.parts_out("becomes")]
            for a in fade:
                a.rate_func = squish_rate_func(smooth, 0.0, 0.35)
            self.play(*sink, *fade, run_time=0.9)
            vo.wait_until("a planner")
            self.play(*hs.parts_in("planner", "sp_planner"), run_time=0.5)
            vo.wait_until("tools, and memory")
            self.play(*hs.parts_in("tools", "sp_tools"), run_time=0.5)
            vo.wait_until("and memory")
            self.play(*hs.parts_in("memory", "sp_memory"), run_time=0.5)
            vo.wait_until("Unroll the spoke")
            # the node's frame is filled S.BG at 1.0: Indicate on the whole node floods it YELLOW and
            # hides "tools"; pulse the label and the border instead (as S05's flash())
            self.play(Indicate(hs.parts["sp_tools"], color=TURN, scale_factor=1.1),
                      Indicate(hs.parts["tools"][1], color=TURN, scale_factor=1.06),
                      hs.parts["tools"].frame.animate(rate_func=there_and_back).set_stroke(TURN, 4.5),
                      run_time=0.6)
            pairs = {"hub": "model", "tools": "tools", "sp_tools": "track"}
            fades = [hs.parts[n] for n in ("planner", "memory", "sp_planner", "sp_memory")]
            self.play(*[ReplacementTransform(hs.parts[a], lt.parts[b]) for a, b in pairs.items()],
                      *[FadeOut(m) for m in fades], run_time=1.4)
            self.remove(*hs.get_family())
            self.remove(*[lt.parts[b] for b in pairs.values()])
            self.add(lt)

        # ============================================================ 4 · laps and the stop rule
        gate = lt.gate
        ex = lt.parts["exit"]
        stop = VGroup(label("stop rule:", 24, TURN), label("a reply with no function call", 24, INK))
        stop.arrange(RIGHT, buff=0.18).move_to([0, -2.95, 0])
        reply = lt.reply_card("plain text")
        reply.move_to(ex.get_start() + RIGHT * (reply.width / 2 + 0.12))
        before_gate = gate.lpost.get_center()[0] - reply.width / 2 - 0.2
        after_gate = gate.rpost.get_center()[0] + reply.width / 2 + 0.35
        with self.voiceover(SAY[4]) as vo:
            self.play(*lt.parts_in("token", "counter"), run_time=0.4)
            self.add(lt)                           # the token back under the stations (z-order)
            run_lap(self, lt, 0.75)                # lap 1 under "What ends the loop?"
            vo.wait_until("The stop rule")
            # lap 2 runs while the exit, the gate and "stop rule:" arrive (on the words)
            self.play(Rotate(lt.parts["token"], angle=-TAU, about_point=lt._c.get_center(), rate_func=linear),
                      *lt.parts_in("exit", "gate"), FadeIn(stop[0], shift=UP * 0.1), run_time=0.8)
            self.add(lt)
            self.play(tick(lt, 2))
            vo.wait_until("a reply with no function call")
            self.play(lap_to_model(lt), FadeIn(stop[1], shift=UP * 0.1), run_time=0.5)
            self.play(tick(lt, 3), FadeIn(reply, shift=RIGHT * 0.2), run_time=0.5)
            self.play(reply.animate.set_x(before_gate), run_time=0.8)
            vo.wait_until("is the final response")
            self.play(gate.open(run_time=0.6))
            self.play(reply.animate.set_x(after_gate), run_time=0.7)
            vo.wait_until("The model decides")
            self.play(Indicate(reply, color=INK, scale_factor=1.12), run_time=0.8)

        # ============================================================ 5 · the loop from outside: ADK's Runner
        lt5 = LoopTrack(radius=0.7, show=("track", "model", "tools", "token"))
        for n in ("counter", "exit", "gate"):          # the compact track has no counter and no gate
            lt5.remove(lt5.parts[n])
        lt5.shift(np.array([-5.3, 2.22, 0]) - lt5._c.get_center())    # clear of the panel header
        cap5 = VGroup(label("inside ADK, simplified:", 22, TOOL),
                      label("model → tools, until the reply is final", 22, TOOL))
        cap5.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        cap5.move_to([0, 2.22, 0]).align_to(np.array([-4.2, 0, 0]), LEFT)
        ill = illustration_tag().next_to(cap5[0], RIGHT, buff=0.35)
        p5 = src_panel(RUNNER, 39, 48)
        p5.shift(RIGHT * (-6.45 - p5.get_left()[0]) + UP * (-3.5 - p5.get_bottom()[1]))
        mod4 = chip("ADK repo · module 4 · code only", S.GREY, size=20)
        mod4.next_to(p5.header, RIGHT, buff=0.4)
        mod4.shift(UP * max(0.0, p5.code.get_top()[1] + 0.08 - mod4.get_bottom()[1]))   # clear of the code box
        bar40 = p5.bar(40, TOOL, 0.22)
        lab40 = VGroup(label("the Runner", 22, TOOL), label("streams events", 22, TOOL))
        lab40.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lab40.next_to(p5, RIGHT, buff=0.2).set_y(code_row(p5, 40).get_center()[1] - 0.2)
        bar45 = span_bar(p5, 45, 46)
        lab45 = VGroup(label("final", 22, TURN), label("response", 22, TURN))
        lab45.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lab45.next_to(p5, RIGHT, buff=0.2)
        lab45.set_y((code_row(p5, 45).get_center()[1] + code_row(p5, 46).get_center()[1]) / 2)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(stop), FadeOut(reply), run_time=0.4)
            morph_track(self, lt, lt5, run_time=1.0)        # the caption follows: the shrinking track crosses its place
            self.play(FadeIn(cap5, shift=RIGHT * 0.1), FadeIn(ill), run_time=0.4)
            self.play(FadeIn(p5, shift=UP * 0.15), FadeIn(mod4, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("the ADK Runner streams events")
            self.play(FadeIn(bar40), FadeIn(lab40, shift=LEFT * 0.1),
                      Indicate(p5.span(40, "self.runner.run_async("), color=TOOL, scale_factor=1.04),
                      run_time=0.7)
            vo.wait_until("this wrapper keeps")
            self.play(FadeIn(bar45), FadeIn(lab45, shift=LEFT * 0.1),
                      Indicate(p5.span(45, "event.is_final_response()"), color=TURN, scale_factor=1.04),
                      run_time=0.7)
            vo.wait_until("and the loop runs inside")
            self.play(Rotate(lt5.parts["token"], angle=-TAU, about_point=lt5._c.get_center(), rate_func=linear),
                      Indicate(cap5, color=TOOL, scale_factor=1.03), run_time=1.4)

        # ============================================================ 6 · the cap: 12 turns, then an error
        lt6 = LoopTrack(show=("track", "model", "tools", "token"))
        lt6.shift(np.array([-4.9, -0.15, 0]) - lt6._c.get_center())     # the gate runs along the top
        c71 = src_panel("colab/cheese-quiz/cell-71.py", 5, 7)
        c25 = src_panel("colab/cheese-newsletter/cell-25.py", 8, subtitle=True)   # “Orchestrator Agent”
        c25.shift(UP * (-3.5 - c25.get_bottom()[1]) + RIGHT * (6.45 - c25.get_right()[0]))
        # two different frameworks, each named on its header row (PURPLE: the loop a framework
        # runs): the quiz's Runner is the OpenAI Agents SDK's, not ADK's (cell 11 imports `agents`);
        # the newsletter's max_iterations is Microsoft Agent Framework's (cell 9, `agent_framework`)
        fw71 = chip("OpenAI Agents SDK", TOOL, size=20)
        fw25 = chip("Microsoft Agent Framework", TOOL, size=20, pad_x=0.16)
        fw25.align_to(c25.code, RIGHT)
        fw25.shift(UP * (c25.code.get_top()[1] + 0.06 - fw25.get_bottom()[1]))
        # c71 sits clear above the c25 chip (the c25 header row is one chip tall now)
        c71.shift(UP * (fw25.get_top()[1] + 0.14 - c71.get_bottom()[1]) + RIGHT * (6.45 - c71.get_right()[0]))
        fw71.align_to(c71.code, RIGHT)
        fw71.shift(UP * (c71.code.get_top()[1] + 0.06 - fw71.get_bottom()[1]))
        assert fw25.get_left()[0] - c25.header.get_right()[0] > 0.15, "c25 chip on its header"
        assert fw71.get_left()[0] - c71.header.get_right()[0] > 0.15, "c71 chip on its header"
        bx71 = SurroundingRectangle(c71.span(6, "max_turns=12"), color=TURN, buff=0.06, stroke_width=3)
        bx25 = SurroundingRectangle(c25.span(8, '"max_iterations": 16'), color=TURN, buff=0.06, stroke_width=3)
        with self.voiceover(SAY[6]) as vo:
            gone5 = [p5, mod4, bar40, lab40, bar45, lab45, cap5, ill]
            morph_track(self, lt5, lt6, extra=[FadeOut(m, rate_func=squish_rate_func(smooth, 0.0, 0.4))
                                               for m in gone5], run_time=1.0)
            self.play(*lt6.parts_in("counter", "exit", "gate"), run_time=0.4)
            self.add(lt6)
            for _ in range(2):
                run_lap(self, lt6, 0.4)
            vo.wait_until("12 turns in the Cheese Quiz Guild")
            self.play(FadeIn(c71, shift=UP * 0.15), FadeIn(fw71, shift=UP * 0.15), run_time=0.5)
            self.play(Create(bx71), run_time=0.4)
            for _ in range(2):
                run_lap(self, lt6, 0.4)
            vo.wait_until("16 iterations")
            self.play(FadeIn(c25, shift=UP * 0.15), FadeIn(fw25, shift=UP * 0.15), run_time=0.5)
            self.play(Create(bx25), run_time=0.4)
            for _ in range(2):
                run_lap(self, lt6, 0.4)
            vo.wait_until("Hitting the")           # also holds if SAY[6] gains "OpenAI" before "Agents SDK"
            while lt6.count < 11:                  # the race: 6 fast laps, the slam on "ends the run"
                run_lap(self, lt6, 0.15, tick_time=0.1)
            run_lap(self, lt6, 0.15, ERR, tick_time=0.1)
            self.play(lt6.gate.open(run_time=0.2))
            self.play(lt6.gate.slam(ERR, "MaxTurnsExceeded"))
            vo.wait_until("ends the run with an error")
            self.play(Indicate(lt6.gate.caption, color=ERR, scale_factor=1.1), run_time=0.8)

        # ============================================================ 7 · slide 41: the block a framework writes
        A = Anatomy(ends=False)
        A.move_to([-2.0, -0.3, 0])
        trk = VGroup(*[lt6.parts[n] for n in ("track", "model", "tools", "token")])
        fw = VGroup(label("the framework", 24, TOOL), label("writes this part", 24, TOOL))
        fw.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        bar = A.parts["control_dash"]
        fw.next_to(A, RIGHT, buff=0.45).set_y(bar.get_center()[1])
        with self.voiceover(SAY[7]) as vo:
            lr = lref_swap(self, lr, "41", run_time=0.4)
            self.play(FadeOut(c71), FadeOut(c25), FadeOut(fw71), FadeOut(fw25), FadeOut(bx71), FadeOut(bx25),
                      FadeOut(lt6.gate.caption),
                      *lt6.parts_out("counter", "exit", "gate"), run_time=0.5)
            self.play(trk.animate.move_to([4.95, -0.3, 0]), run_time=0.7)     # out of the anatomy's way first
            self.play(FadeIn(A, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("gray out dynamic control")
            self.play(A.names["control"].animate.set_color(S.GREY),     # grayed, still readable
                      Indicate(bar, color=S.GREY, scale_factor=1.03), run_time=0.7)
            for name, phrase in (("core", "You configure the model"), ("instructions", "instructions, tools"),
                                 ("tools", "tools and memory"), ("memory", "and memory")):
                vo.wait_until(phrase)
                self.play(A.frames[name].animate.set_stroke(INK, 4),
                          Indicate(A.names[name], color=INK, scale_factor=1.12), run_time=0.45)
            vo.wait_until("the loop is the block")
            self.play(trk.animate.scale(0.25).move_to(bar.get_center()).set_opacity(0),
                      *A.fill_control(), run_time=1.0)
            self.remove(trk, *lt6.get_family())
            self.play(FadeIn(fw, shift=LEFT * 0.15), run_time=0.6)

        # ============================================================ 8 · tear down llm-rag
        tr = tracker("Run", 3)
        t = term(P_CTR, rows=8, container=True)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(A), FadeOut(fw), FadeOut(lr), run_time=0.5)
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t, shift=UP * 0.3), run_time=0.6)
            bare_prompt(self, t)
            vo.wait_until("Type exit")
            self.play(caption_extra(tr, True), run_time=0.3)
            out = session(self, t, C06, 41, 42, type_time=0.4, out_time=0.3)
            pin(self, out[41], beside(extra_tag(), t, out[41], buff=0.4), run_time=0.3)
            self.play(*leave_container(t), run_time=0.5)
            bare_prompt(self, t)
            vo.wait_until("an extra docker ps")
            ps = type_cmd(self, t, C12.cmd, 1.2)
            pin(self, ps.rows[0], beside(extra_tag(), t, ps.rows[0], buff=0.4), run_time=0.3)
            hd, row_ch = t.print(self, ps_columns(C12), run_time=0.4)
            img = grey_tag("IMAGE not shown")          # at the right end: clear of the PINK box and tag below
            img.move_to(hd.strut).align_to(t.box, RIGHT).shift(LEFT * 0.08)
            pin(self, hd, img, run_time=0.3)
            vo.wait_until("Chroma still up")
            a = row_ch.text.index(PORT)
            pbox = col_box(row_ch, a, a + len(PORT), LOOKUP)
            self.play(substring(row_ch, PORT).animate.set_color(LOOKUP), Create(pbox), run_time=0.5)
            row_ch.add(pbox)
            up = tag("still up", LOOKUP)
            pin(self, row_ch, up.next_to(pbox, RIGHT, buff=0.12).set_y(row_ch.strut.get_center()[1]),
                run_time=0.4)
            bare_prompt(self, t)
            vo.wait_until("Then docker compose down")
            cd = type_cmd(self, t, C13.cmd, 0.6)
            pin(self, cd, beside(extra_tag(), t, cd, buff=0.4), run_time=0.3)
            warns = t.print(self, [WARN_1, WARN_2], wrap=True, run_time=0.5)
            done = print_build(self, t, [C13.line(5), C13.line(6), C13.line(7)], run_time=0.5)
            vo.wait_until("two harmless warnings")
            self.play(*[w.animate.set_color(S.GREY) for w in warns], run_time=0.4)
            pin(self, warns[-1], beside(harmless_tag(), t, warns[-1], buff=0.5), run_time=0.4)
            vo.wait_until("and it stops")
            self.play(*[Indicate(substring(r, "Removed"), color=INK, scale_factor=1.1) for r in done[1:]],
                      run_time=0.8)

        # ============================================================ 9 · what stays, what's free; ▶ your turn
        idx = mixed_chip(["`docker-volumes/`", ": your index stays"], DATA)
        prt = mixed_chip(["port 8000 → free for part 2"], LOOKUP)
        VGroup(idx, prt).arrange(RIGHT, buff=0.5).move_to([0, 1.6, 0])
        your = turn_card([("exit", "extra"), ("docker compose down", "extra")], header=None)
        your.move_to([0, 1.62, 0])                    # between the tracker (2.94) and the terminal (0.58)
        with self.voiceover(SAY[9]) as vo:
            self.play(Write(idx), run_time=0.9)
            vo.wait_until("and part 2 also needs port 8000")
            self.play(Write(prt), run_time=0.9)
            vo.wait_until("Pause and tear down")
            self.play(FadeOut(idx), FadeOut(prt), run_time=0.4)
            self.play(FadeIn(your, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("In part 2")
            # the tag's box is filled S.BG at 0.92: pulse its text and border, not the fill
            self.play(Indicate(your.tag.text, color=TURN, scale_factor=1.1),
                      your.tag.box.animate(rate_func=there_and_back).set_stroke(TURN, 3.5), run_time=0.8)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
