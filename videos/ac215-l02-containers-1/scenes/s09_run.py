"""S09 · Run it, translate, exit (README A14-A16; V2 the container; V3 the knock-out; end of part 1).

Beats (script.md "## S09", one voiceover block each):
 0  TRACKER A13 -> A14. Full terminal (13 rows): on "docker run" it types `docker run --rm -ti
    simple-translate` (folds onto 2 rows); the capture's prompt `root@93d61f44d3d7:/#` (laptop/31
    line 2) appears and pulses on "At the prompt". TRACKER A15: it types
    `python cli.py -t "Good morning" -s "en" -d "es"` (folds) -> laptop/31 lines 5-9, 13 (wrapped),
    15-16; `Output: Buen día` GREEN, it pulses on "from English to Spanish". On "Pause and run both"
    a YELLOW `▶ your turn` beside each command.
 1  The terminal shrinks to the 3-row strip (the translate command and `Output: Buen día`); the
    output line is copied up, enlarged (GREEN). Above the strip: a GREY laptop with a TEAL
    container in its screen ("the request"), a PINK route out of the laptop (the laptop pulses on
    "through your laptop's network") to a BLUE cloud `translate.googleapis.com` ("to Google"),
    carrying "Good morning"; "Buen día" rides back on a second PINK route. "If yours ends in a
    runtime error": a GREY chip "a runtime error? → Google said no · not Docker"; the cloud wiggles
    on "Google refused"; the container pulses on "Docker is fine".
 2  TRACKER A16. The picture goes; the terminal grows back (6 rows); it types `exit` at the
    container prompt (laptop/31 line 17) -> line 18; the laptop prompt returns and pulses YELLOW.
    ▶ your turn beside `exit` on "Pause and do it".
 3  The terminal shrinks to the strip. V2 above it: the TEAL stack (four thin ORANGE base slabs with
    the brace "base image", ORANGE `RUN pip install uv`, GREY `COPY . ./`, GREEN `RUN uv sync`) and
    the dashed glowing glass slab with its dot "main process". The `exit` replays: the strip's exit
    is copied to the dot; "so the container stopped": the dot goes out ("stopped"); "and dash dash
    rm": a TEAL chip `--rm` appears and the glass slab, dot and label dissolve; the stack stays, a
    GREEN check "image unchanged". TRACKER A16 · extra on "An extra check": `docker ps -a` (row tag
    `extra`) -> laptop/32 line 2 squeezed (the header only); a GREY row tag "empty"; the stack and
    the check pulse on "the image is untouched".
 4  TRACKER A16 · extra. The strip grows to 4 rows: a second run (row tag `extra`); a new glass
    slab and dot. At `root@1d1fecf6ff8f:/#` it types `echo $$` (laptop/33 line 4) -> line 5; on
    "shows that bash" the `1` flies to the dot, whose label becomes "PID 1 · bash". A `…` row with
    the GREY row tag "more checks · part 2". "The container lives": the dot and glass pulse.
    Labels right of the stack: `-i` "your keyboard → bash", `-t` "a terminal: prompt, line
    editing", each as it is said. "Then type exit": `exit` (line 29) -> line 30, the laptop prompt
    returns; the dot goes out and the slab dissolves.
 5  The picture and the strip clear. V3 card (TEAL): ENTRYPOINT `["/bin/bash"]`, CMD
    `["-c", "source … && exec bash"]`, S05's GREY labels with short arrows ("the program", then
    "its default arguments" on "the default arguments"). "What if you put words": the chip
    `docker run --rm -ti simple-translate python cli.py` at the top; `python cli.py` boxed YELLOW as
    it is said; a YELLOW "?" where the start-up line goes. PONDER (8 s): the card group slides down,
    the ponder card covers the chip (the card stays visible).
 6  A WHITE tile `python cli.py` is copied from the chip's box and knocks the CMD tile off the card;
    ENTRYPOINT pulses on "and only CMD". "So the container runs": the start-up line
    `/bin/bash python cli.py` is assembled from the two tiles and turns RED. The card and chip fade;
    the line moves up. "Bash takes python as a script name": `python` underlined, GREY "script
    name"; the door row (`/usr/local/bin` ORANGE, `…`) with GREY "venv not activated" (no venv
    door); "and finds": a PINK `python` copied from the line walks into the first door, which
    holds the ORANGE `python` program; "That's a binary": a RED stamp "a program, / not a script".
    A 4-row strip types `docker run --rm -ti simple-translate python cli.py` (row tag `extra`) ->
    laptop/36 line 2 (wrapped, RED); RED row tag "exit 126" on "exit code 126".
 7  The doors go; the card returns, wide, with ENTRYPOINT `["/bin/bash"]` and the WHITE
    `python cli.py` tile; the RED line moves under it. "replace CMD": the tile falls off, a WHITE
    tile `-c "source .venv/bin/activate && python cli.py -d fr"` slides in, and the line becomes
    `/bin/bash -c "source .venv/bin/activate && python cli.py -d fr"` in GREEN (built from the
    tiles). "as in this extra": the strip (5 rows) types `docker run --rm simple-translate -c
    "source .venv/bin/activate && python cli.py -d fr"` (folds; row tags `extra` and "no -ti ·
    nothing to type") -> laptop/37 lines 12 (wrapped), 14-15; `Output: j'adore le fromage` GREEN.
 8  CODE(docker-shell.sh: 10-15) (line 12, the commented platform build, dimmed); YELLOW bars on
    line 11 on "builds" and line 15 on "and runs"; GREY tag "not in the README · builds and runs in
    one go".
 9  TRACKER A16. Part-1 recap: the full V2 stack (brace "base image", caption
    `python:3.12-slim-bookworm`, ORANGE `RUN pip install uv`, GREY `COPY . ./`, GREEN `RUN uv sync`)
    beside the config card; a TEAL check "your image: built and run"; on "In part 2" the closing
    card "Part 2: what's inside, why it rebuilt, and shipping it to a VM". Fade to an empty frame
    (end of part 1).
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import line_bar
from explainer.scene import VoiceScene

from common import (ERR, EXIT, IMAGE, INK, LAPTOP, LAPTOP_DIR, CLOUD, MONO, NARRATION, P_LAPTOP,
                    ROUTE, RUN, STRIP_ROWS, SYSTEM, TRANSLATE, TURN, VENV, ConfigCard, Glass,
                    LayerStack, PathDoors, attach, bare_prompt, beside, box, capture, check_mark,
                    chip, code, istep, label, laptop, laptop_term, mono, mono_line, pin,
                    resize, route, row_tag, squeeze, steady, substring, tag, track, tracker_a, travel,
                    type_cmd, unpin)
from explainer.devops import cloud

SAY = NARRATION["S09"]

# ------------------------------------------------------------------ real outputs (file line numbers)
C31 = capture("31", LAPTOP_DIR)                          # laptop/31-run.txt
assert C31.cmd == RUN, C31.cmd
P31, _typed = C31.istep(2)                               # root@93d61f44d3d7:/#, the README's translate
assert _typed == TRANSLATE, C31.line(2)
OUT31 = C31.at((5, 9), 13, (15, 16))                     # banner, Arguments (wraps), Input, Output
assert OUT31[-1] == "Output: Buen día" and OUT31[5].startswith("Arguments:"), OUT31
assert C31.istep(17) == (P31, EXIT), C31.line(17)
ECHO31 = C31.at(18)                                      # ["exit"]

C32 = capture("32", LAPTOP_DIR)                          # laptop/32-ps-a.txt
PS_A = C32.cmd
assert PS_A == "docker ps -a", PS_A
PS_OUT = squeeze(C32.at(2))                              # the header only
assert len(PS_OUT) == 1 and PS_OUT[0].startswith("CONTAINER ID  IMAGE"), PS_OUT

C33 = capture("33", LAPTOP_DIR)                          # laptop/33-inside.txt
assert C33.cmd == RUN, C33.cmd
P33, _echo = C33.istep(4)
assert _echo == "echo $$" and C33.at(5) == ["1"], C33.raw[:5]
assert C33.istep(29) == (P33, EXIT), C33.line(29)
ECHO33 = C33.at(30)

C36 = capture("36", LAPTOP_DIR)                          # laptop/36-run-args.txt
RUN_ARGS = C36.cmd
assert RUN_ARGS == RUN + " python cli.py" and C36.exit == 126, (RUN_ARGS, C36.exit)
ERR36 = C36.at(2)                                        # cannot execute binary file
assert ERR36[0].endswith("cannot execute binary file"), ERR36

C37 = capture("37", LAPTOP_DIR)                          # laptop/37-run-c.txt
RUN_C = C37.cmd
assert RUN_C == 'docker run --rm simple-translate -c "source .venv/bin/activate && python cli.py -d fr"'
OUT37 = C37.at(12, 14, 15)
assert OUT37[-1] == "Output: j'adore le fromage", OUT37

# ------------------------------------------------------------------ the V3 values
ENT = '["/bin/bash"]'
CMD_IMG = '["-c", "source … && exec bash"]'               # the image's CMD, abbreviated (S08)
WORDS = "python cli.py"                                  # the words after the image name
C_STR = '-c "source .venv/bin/activate && python cli.py -d fr"'
assert RUN_C.endswith(C_STR)
LINE_BAD = "/bin/bash python cli.py"
LINE_GOOD = "/bin/bash " + C_STR
QUESTION = "docker run --rm -ti simple-translate python cli.py\nWhat command line does the container actually run?"

# ------------------------------------------------------------------ layout
STACK_X, FLOOR_Y = -2.4, -0.85        # beats 3-4: the V2 stack over the strip (4 rows: top -1.04)
CARD_X, CARD_Y = 2.0, 0.1             # beat 5: the stacked V3 card (6.0 wide), labels at its left
PONDER_Y, CARD_DROP = 1.55, 1.25      # the ponder card covers the chip; the card group drops under it
LINE_TOP = 2.3                        # beat 6: the start-up line, up top
BIG = 34                              # beat 1: the enlarged output line


# ------------------------------------------------------------------ helpers
def turn_tag() -> VGroup:
    """YELLOW '▶ your turn', the height of a terminal row."""
    return row_tag("▶ your turn", TURN)


def text_span(t, s: str, sub: str) -> VGroup:
    """Glyphs of `sub` in a Text built from string `s` (spaces have no glyphs)."""
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def steady_span(t, s: str, sub: str) -> VGroup:
    """Glyphs of `sub` in a steady() text of string `s` (its first glyph is the hidden strut)."""
    i = s.index(sub)
    a = 1 + len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def side_label(s: str, slot) -> VGroup:
    """S05's GREY label left of a card slot with a short arrow to it. .text .arrow"""
    t = label(s, 22, S.GREY)
    y = slot.get_center()[1]
    x_end = slot.get_left()[0] - 0.12
    arrow = Arrow([x_end - 0.95, y, 0], [x_end, y, 0], buff=0, color=S.GREY, stroke_width=3,
                  max_tip_length_to_length_ratio=0.3, tip_length=0.16)
    t.next_to(arrow, LEFT, buff=0.12)
    g = VGroup(t, arrow)
    g.text, g.arrow = t, arrow
    return g


def clear_with(scene, t, *anims, run_time: float = 0.4) -> None:
    """t.clear(scene), played together with other animations."""
    scene.play(FadeOut(t.lines), *anims, run_time=run_time)
    for m in list(t.lines):
        t.lines.remove(m)


def build_stack(x: float, floor_y: float, uv_h: float):
    """The finished V2 stack: four thin ORANGE base slabs (brace 'base image'), ORANGE
    `RUN pip install uv`, GREY `COPY . ./`, GREEN `RUN uv sync`. Returns (stack, slabs, brace)."""
    st = LayerStack(stack_w=3.4)
    st.floor.move_to([x, floor_y, 0])
    base = [st.make(None, SYSTEM, 0.15) for _ in range(4)]
    rest = [st.make("RUN pip install uv", SYSTEM), st.make("COPY . ./", LAPTOP),
            st.make("RUN uv sync", VENV, uv_h)]
    for s in base + rest:
        st.slabs.add(s)
    st._pending.clear()
    br = st.brace(base, "base image")
    return st, base + rest, br


def two_part(key: str, text: str) -> VGroup:
    """A flag (mono, TEAL) and what it does (GREY)."""
    return VGroup(mono(key, 24, IMAGE), label(text, 22, S.GREY)).arrange(RIGHT, buff=0.25)


def stamp(lines: list[str], color=ERR) -> VGroup:
    """A rubber stamp: RED text in a RED frame, slightly rotated."""
    t = VGroup(*[label(s, 22, color) for s in lines]).arrange(DOWN, buff=0.06)
    f = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.08,
                         stroke_color=color, stroke_width=3).set_fill(S.BG, 0.85)
    t.move_to(f)
    return VGroup(f, t).rotate(-7 * DEGREES)


# ------------------------------------------------------------------ the scene
class RunIt(VoiceScene):
    def ponder_at(self, question: str, seconds: float, center) -> VGroup:
        """pause_and_ponder's card and draining timer, placed at `center` (opaque), so the config
        card under it stays visible. Returns the card (removed at the start of the next block)."""
        card = ponder_card(question).move_to(center)
        card[0].set_fill(S.BG, 1)
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=seconds)
        return card

    def construct(self):
        assert len(SAY) == 10, f"S09 has {len(SAY)} SAY lines; this scene times 10"

        tr = tracker_a(13)
        t = laptop_term(13)

        # ========================================================== 0 · run, then translate
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.5)
            bare_prompt(self, t)
            self.play(track(tr, 14), run_time=0.5)
            self.play(Indicate(VGroup(tr.dots[13], tr.caption), color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("docker run")
            c_run = type_cmd(self, t, RUN, 2.4)
            t.set_prompt(P31)
            p_box = bare_prompt(self, t)
            vo.wait_until("At the prompt")
            self.play(track(tr, 15), Indicate(substring(p_box, P31), color=IMAGE, scale_factor=1.06),
                      run_time=0.7)
            vo.wait_until("type the README")
            c_tr = istep(self, t, C31.line(2), 1.6)
            vo.wait_until("Good morning")
            out = t.print(self, OUT31[:-1] + [(OUT31[-1], VENV)], run_time=0.8, wrap=True, lag=0.08)
            out_line = out[-1]
            vo.wait_until("from English")
            self.play(Indicate(out_line.glyphs, color=VENV, scale_factor=1.12), run_time=0.8)
            vo.wait_until("Pause and run both")
            yt_run = beside(turn_tag(), c_run.rows[1])
            yt_tr = beside(turn_tag(), c_tr.rows[1])
            self.play(FadeIn(yt_run, shift=LEFT * 0.1), FadeIn(yt_tr, shift=LEFT * 0.1), run_time=0.4)
            attach(self, c_run.rows[1], yt_run)
            attach(self, c_tr.rows[1], yt_tr)
            self.play(Wiggle(VGroup(yt_run, yt_tr), scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.7)

        # ========================================================== 1 · the request goes to Google
        big = mono_line(OUT31[-1], BIG, VENV)
        big.move_to([0, 2.3, 0])
        lap = laptop(3.0, LAPTOP).move_to([-3.4, 0.35, 0])
        lap_l = label("your laptop", 22, LAPTOP).next_to(lap, DOWN, buff=0.15)
        con = box(2.2, 0.75, IMAGE, fill_opacity=0.15).move_to(lap.screen)
        con_l = label("container", 22, IMAGE).move_to(con)
        gcl = cloud(2.6, CLOUD).move_to([3.4, 0.95, 0])
        host = mono("translate.googleapis.com", 20, CLOUD).next_to(gcl, DOWN, buff=0.15)
        req = route(con.get_right() + UP * 0.15, gcl.get_left() + RIGHT * 0.1 + DOWN * 0.05, arc=-0.35)
        ret = route(gcl.get_bottom() + LEFT * 0.75 + UP * 0.2, con.get_bottom() + RIGHT * 0.6, arc=-0.45)
        w_req = mono("Good morning", 20, ROUTE)
        w_ret = mono("Buen día", 20, ROUTE)
        oops = chip("a runtime error? → Google said no · not Docker", S.GREY, size=22)
        oops.move_to([3.15, -0.95, 0])

        with self.voiceover(SAY[1]) as vo:
            unpin(self, [(c_run.rows[1], yt_run), (c_tr.rows[1], yt_tr)], 0.3)
            resize(self, t, STRIP_ROWS, keep=[*c_tr.rows, out_line], run_time=0.7)
            self.play(TransformFromCopy(out_line.glyphs, big.glyphs), run_time=0.9)
            self.add(big)
            vo.wait_until("the request")
            self.play(FadeIn(lap), FadeIn(lap_l), FadeIn(VGroup(con, con_l), scale=0.9), run_time=0.6)
            vo.wait_until("through your laptop")
            w_req.move_to(req.get_start())
            self.play(GrowArrow(req), FadeIn(w_req), run_time=0.6)
            self.play(Indicate(lap, color=INK, scale_factor=1.04), travel(w_req, req, 1.0))
            vo.wait_until("to Google")
            self.play(FadeIn(gcl, scale=0.85), FadeIn(host), FadeOut(w_req, scale=0.6), run_time=0.6)
            w_ret.move_to(ret.get_start())
            self.play(GrowArrow(ret), FadeIn(w_ret), run_time=0.5)
            self.play(travel(w_ret, ret, 1.0))
            self.play(FadeOut(w_ret, scale=0.6), Indicate(big.glyphs, color=VENV, scale_factor=1.06), run_time=0.6)
            vo.wait_until("If yours ends")
            self.play(FadeIn(oops, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Google refused")
            self.play(Wiggle(gcl, scale_value=1.06, rotation_angle=0.03 * TAU), run_time=0.9)
            vo.wait_until("Docker is fine")
            self.play(Indicate(VGroup(con, con_l), color=IMAGE, scale_factor=1.1), run_time=0.8)

        # ========================================================== 2 · exit
        picture1 = VGroup(big, lap, lap_l, con, con_l, gcl, host, req, ret, oops)

        with self.voiceover(SAY[2]) as vo:
            resize(self, t, 6, extra=[FadeOut(picture1), track(tr, 16)], run_time=0.7)
            vo.wait_until("type exit")
            c_exit = istep(self, t, C31.line(17), 0.3)
            t.print(self, ECHO31, run_time=0.25)
            t.set_prompt(P_LAPTOP)
            p_back = bare_prompt(self, t)
            vo.wait_until("and you're back")
            self.play(Indicate(substring(p_back, P_LAPTOP), color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Pause and do it")
            yt_exit = beside(turn_tag(), c_exit)
            pin(self, c_exit, yt_exit, run_time=0.35)
            self.play(Wiggle(yt_exit, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.6)

        # ========================================================== 3 · what exit did; docker ps -a
        stack, slabs, brace = build_stack(STACK_X, FLOOR_Y, 0.62)
        glass = Glass(glass_w=3.4, process="main process").on(stack)
        rm = chip("--rm", IMAGE, size=24, font=MONO).next_to(glass, RIGHT, buff=0.55)
        unchanged = VGroup(check_mark(0.34, VENV), label("image unchanged", 24, VENV)).arrange(RIGHT, buff=0.2)
        unchanged.next_to(stack.slabs, RIGHT, buff=0.55).shift(DOWN * 0.2)
        fly = mono("exit", 22, INK)

        with self.voiceover(SAY[3]) as vo:
            unpin(self, [(c_exit, yt_exit)], 0.25)
            resize(self, t, STRIP_ROWS, keep=3, extra=[FadeIn(VGroup(*slabs, brace), shift=UP * 0.15)],
                   run_time=0.7)
            self.add(stack)
            self.play(FadeIn(glass, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("It ended")
            fly.move_to(substring(c_exit, "exit"))
            self.play(Indicate(substring(c_exit, "exit"), color=TURN, scale_factor=1.2), run_time=0.5)
            self.play(fly.animate.next_to(glass.dot, LEFT, buff=0.15).set_color(TURN), run_time=0.7)
            vo.wait_until("so the container stopped")
            self.play(glass.stop(), FadeOut(fly), run_time=0.6)
            vo.wait_until("and dash dash rm")
            self.play(FadeIn(rm, shift=LEFT * 0.15), run_time=0.4)
            self.play(glass.dissolve(), FadeOut(rm, shift=UP * 0.3), run_time=0.8)
            self.play(Create(unchanged[0]), FadeIn(unchanged[1], shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("An extra check")
            c_ps = type_cmd(self, t, PS_A, 0.6)
            self.play(track(tr, 16, extra=True), run_time=0.4)
            pin(self, c_ps, beside(row_tag("extra"), c_ps), run_time=0.25)
            ps = t.print(self, PS_OUT, run_time=0.3)[0]
            vo.wait_until("lists every container")
            self.play(Indicate(ps.glyphs, color=INK, scale_factor=1.04), run_time=0.8)
            vo.wait_until("Nothing is left")
            pin(self, ps, beside(row_tag("empty"), ps, buff=0.3), run_time=0.35)
            vo.wait_until("the image is untouched")
            self.play(Indicate(VGroup(*slabs), color=IMAGE, scale_factor=1.04),
                      Indicate(unchanged, color=VENV, scale_factor=1.1), run_time=0.9)

        # ========================================================== 4 · a second run: PID 1, -i, -t
        glass2 = Glass(glass_w=3.4, process="main process").on(stack)
        pid = steady("PID 1 · bash", 20, IMAGE).move_to(glass2.dot_label, aligned_edge=RIGHT)
        lab_i = two_part("-i", "your keyboard → bash")
        lab_t = two_part("-t", "a terminal: prompt, line editing")
        flags = VGroup(lab_i, lab_t).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        flags.next_to(stack.slabs, RIGHT, buff=0.55).set_y(1.05)

        with self.voiceover(SAY[4]) as vo:
            resize(self, t, 4, extra=[FadeOut(unchanged)], run_time=0.5)
            c_run2 = type_cmd(self, t, RUN, 1.0)
            t.set_prompt(P33)
            bare_prompt(self, t)
            x_run2 = beside(row_tag("extra"), c_run2.rows[0])
            self.play(FadeIn(glass2, shift=DOWN * 0.15), FadeIn(x_run2, shift=LEFT * 0.1), run_time=0.5)
            attach(self, c_run2.rows[0], x_run2)
            vo.wait_until("echo dollar")
            istep(self, t, C33.line(4), 0.4)
            one = t.print(self, C33.at(5), run_time=0.25)[0]
            vo.wait_until("shows that bash")
            fly1 = one.glyphs[0].copy()
            self.play(fly1.animate.move_to(pid[4]).set_color(IMAGE).scale(pid[4].height / fly1.height),
                      run_time=0.8)
            self.play(Transform(glass2.dot_label, pid), FadeOut(fly1), Flash(glass2.dot, color=IMAGE,
                      line_length=0.15, flash_radius=0.25), run_time=0.5)
            dots = t.print(self, ["…"], run_time=0.25)[0]
            pin(self, dots, beside(row_tag("more checks · part 2"), dots, buff=0.35), run_time=0.3)
            vo.wait_until("The container lives")
            self.play(Indicate(VGroup(glass2.dot, glass2.dot_label), color=IMAGE, scale_factor=1.25),
                      glass2.glow.animate.set_stroke(opacity=0.6), run_time=0.8)
            self.play(glass2.glow.animate.set_stroke(opacity=0.25), run_time=0.4)
            vo.wait_until("Dash i")
            self.play(FadeIn(lab_i, shift=RIGHT * 0.15), Indicate(glass2.dot, color=IMAGE, scale_factor=1.6),
                      run_time=0.6)
            vo.wait_until("and dash t")
            self.play(FadeIn(lab_t, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("Then type exit")
            istep(self, t, C33.line(29), 0.3)
            t.print(self, ECHO33, run_time=0.2)
            t.set_prompt(P_LAPTOP)
            bare_prompt(self, t)
            self.play(glass2.stop(), run_time=0.45)
            self.play(glass2.dissolve(), run_time=0.6)

        # ========================================================== 5 · the puzzle
        card = ConfigCard(rows=("ENTRYPOINT", "CMD"), card_w=6.0, inline=False)
        card.move_to([CARD_X, CARD_Y, 0])
        t_ent = card.place("ENTRYPOINT", card.tile(ENT))
        t_cmd = card.place("CMD", card.tile(CMD_IMG))
        lab_ent = side_label("the program", card.slots["ENTRYPOINT"])
        lab_cmd = side_label("its default arguments", card.slots["CMD"])
        q_line = steady("?", 30, TURN)
        q_line.next_to(card.frame, DOWN, buff=0.22).align_to(card.frame, LEFT).shift(RIGHT * 0.1)
        cmd_chip = chip(RUN_ARGS, S.GREY, size=22, font=MONO).move_to([0, 2.2, 0])
        words = text_span(cmd_chip.text, RUN_ARGS, WORDS)
        words_box = SurroundingRectangle(words, color=TURN, buff=0.08, stroke_width=3, corner_radius=0.05)
        group5 = VGroup(card, t_ent, t_cmd, lab_ent, lab_cmd, q_line)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(*slabs, brace, flags)), FadeOut(t, shift=DOWN * 0.2), run_time=0.6)
            self.remove(stack, t, *t.lines)
            self.play(FadeIn(VGroup(card, t_ent, t_cmd), shift=UP * 0.15), run_time=0.6)
            self.play(GrowArrow(lab_ent.arrow), FadeIn(lab_ent.text, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("the default arguments")
            self.play(GrowArrow(lab_cmd.arrow), FadeIn(lab_cmd.text, shift=RIGHT * 0.15),
                      Indicate(t_cmd, color=IMAGE, scale_factor=1.08), run_time=0.7)
            vo.wait_until("What if you put")
            self.play(FadeIn(cmd_chip, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("python cli.py")
            self.play(Create(words_box), Indicate(words, color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("What command line")
            self.play(FadeIn(q_line, scale=1.5), run_time=0.4)
            self.play(Wiggle(q_line, scale_value=1.3), run_time=0.7)

        self.play(group5.animate.shift(DOWN * CARD_DROP), run_time=0.6)
        ponder = self.ponder_at(QUESTION, 8, [0, PONDER_Y, 0])

        # ========================================================== 6 · words replace CMD: exit 126
        new_tile = card.tile(WORDS, color=INK)
        spot = card.slots["CMD"].get_left() + RIGHT * (0.08 + new_tile.width / 2)
        new_tile.move_to(spot + RIGHT * 3.2 + UP * 0.6)
        bad = steady(LINE_BAD, 22, INK, mono_font=True).move_to(q_line, aligned_edge=LEFT)
        bad_top = bad.copy().move_to([0, LINE_TOP, 0])
        py_top = steady_span(bad_top, LINE_BAD, "python")
        doors = PathDoors(["/usr/local/bin", "…"], colors={"/usr/local/bin": SYSTEM}, door_w=2.5,
                          door_h=1.6)
        d0 = doors.doors[0]
        doors.shift(np.array([-4.6 - d0.frame.get_left()[0], 1.2 - d0.frame.get_top()[1], 0]))
        no_venv = label("venv not activated", 22, S.GREY).next_to(doors.doors, RIGHT, buff=0.5)
        no_venv.set_y(d0.frame.get_center()[1])
        t2 = laptop_term(4)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(ponder), run_time=0.4)
            self.play(TransformFromCopy(words, new_tile.text), FadeIn(new_tile.frame), run_time=0.8)
            card.take(self, "CMD", run_time=0.5, extra=[new_tile.animate.move_to(spot)])
            card.tiles["CMD"] = new_tile
            vo.wait_until("and only CMD")
            self.play(Indicate(t_ent, color=IMAGE, scale_factor=1.12), Indicate(lab_ent.text, color=INK),
                      run_time=0.8)
            vo.wait_until("So the container runs")
            self.play(TransformFromCopy(steady_span(t_ent.text, ENT, "/bin/bash"), steady_span(bad, LINE_BAD, "/bin/bash")),
                      TransformFromCopy(VGroup(*new_tile.text[1:]), steady_span(bad, LINE_BAD, WORDS)),
                      FadeOut(q_line), run_time=1.0)
            self.remove(*bad)
            self.add(bad)
            self.play(bad.animate.set_color(ERR), Flash(bad.get_right() + RIGHT * 0.15, color=ERR,
                      line_length=0.18, flash_radius=0.3), run_time=0.6)
            self.play(FadeOut(VGroup(card, t_ent, new_tile, lab_ent, lab_cmd, cmd_chip, words_box)),
                      bad.animate.move_to(bad_top), run_time=0.8)
            vo.wait_until("Bash takes python")
            u_py = Line(py_top.get_corner(DL) + DOWN * 0.08, py_top.get_corner(DR) + DOWN * 0.08,
                        color=S.GREY, stroke_width=3)
            l_py = label("script name", 22, S.GREY).next_to(u_py, DOWN, buff=0.1)
            self.play(Create(u_py), FadeIn(l_py, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(doors, shift=UP * 0.15), FadeIn(no_venv), run_time=0.6)
            vo.wait_until("and finds")
            walker = mono("python", 24, ROUTE).next_to(d0.frame, UP, buff=0.15)
            self.play(TransformFromCopy(steady_span(bad, LINE_BAD, "python"), walker), run_time=0.7)
            prog = mono("python", 24, SYSTEM).move_to(d0.frame).shift(UP * 0.35)
            self.play(walker.animate.move_to(prog), d0.frame.animate.set_fill(SYSTEM, 0.3), run_time=0.6)
            self.play(Transform(walker, prog), run_time=0.4)
            vo.wait_until("in user local bin")
            self.play(Indicate(d0.label, color=SYSTEM, scale_factor=1.1), run_time=0.7)
            vo.wait_until("That's a binary")
            st = stamp(["a program,", "not a script"]).move_to(d0.frame).shift(DOWN * 0.3)
            self.play(FadeIn(st, scale=1.4), run_time=0.4)
            self.play(Indicate(st, color=ERR, scale_factor=1.06), run_time=0.5)
            self.play(FadeIn(t2), run_time=0.35)
            bare_prompt(self, t2)
            c36 = type_cmd(self, t2, RUN_ARGS, 1.3)
            pin(self, c36.rows[0], beside(row_tag("extra"), c36.rows[0]), run_time=0.25)
            vo.wait_until("cannot execute")
            err = t2.print(self, [(ERR36[0], ERR)], run_time=0.4, wrap=True)
            vo.wait_until("exit code")
            pin(self, err[-1], beside(row_tag("exit 126", ERR), err[-1]), run_time=0.4)
            self.play(Indicate(err[-1].submobjects[-1], color=ERR, scale_factor=1.3), run_time=0.6)

        # ========================================================== 7 · your own -c string
        card2 = ConfigCard(rows=("ENTRYPOINT", "CMD"), card_w=9.8, inline=False)
        card2.shift(np.array([0 - card2.frame.get_center()[0], 2.75 - card2.frame.get_top()[1], 0]))
        t_ent2 = card2.place("ENTRYPOINT", card2.tile(ENT))
        t_words2 = card2.place("CMD", card2.tile(WORDS, color=INK))
        t_c = card2.tile(C_STR, color=INK)
        t_c_spot = card2.slots["CMD"].get_left() + RIGHT * (0.08 + t_c.width / 2)
        good = card2.startup(LINE_GOOD, color=VENV, buff=0.22)
        bad_under = bad.copy().align_to(good, LEFT).set_y(good.get_center()[1])
        assert good.get_bottom()[1] > -0.5, good.get_bottom()

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(doors, no_venv, walker, st, u_py, l_py)),
                      FadeIn(VGroup(card2, t_ent2, t_words2), shift=DOWN * 0.15),
                      bad.animate.move_to(bad_under), run_time=0.8)
            vo.wait_until("replace CMD")
            t_c.move_to(t_c_spot + UP * 0.8)
            card2.take(self, "CMD", run_time=0.5, extra=[FadeIn(t_c, shift=DOWN * 0.3)])
            self.play(t_c.animate.move_to(t_c_spot), run_time=0.5)
            card2.tiles["CMD"] = t_c
            self.play(ReplacementTransform(steady_span(bad, LINE_BAD, "/bin/bash"), steady_span(good, LINE_GOOD, "/bin/bash")),
                      FadeOut(steady_span(bad, LINE_BAD, WORDS), shift=DOWN * 0.25),
                      TransformFromCopy(VGroup(*t_c.text[1:]), steady_span(good, LINE_GOOD, C_STR)),
                      run_time=0.9)
            self.remove(bad, *bad, *good)
            self.add(good)
            vo.wait_until("as in this extra")
            clear_with(self, t2, run_time=0.3)
            resize(self, t2, 5, run_time=0.4)
            bare_prompt(self, t2)
            c37 = type_cmd(self, t2, RUN_C, 1.4)
            assert len(c37.rows) == 3 and "--rm simple-translate -c" in c37.rows[1].text, [r.text for r in c37.rows]
            x37 = beside(row_tag("extra"), c37.rows[0])
            no_ti = beside(row_tag("no -ti · nothing to type"), c37.rows[1])
            self.play(FadeIn(x37, shift=LEFT * 0.1), FadeIn(no_ti, shift=LEFT * 0.1), run_time=0.3)
            attach(self, c37.rows[0], x37)
            attach(self, c37.rows[1], no_ti)
            vo.wait_until("activate, then")
            out37 = t2.print(self, OUT37[:-1] + [(OUT37[-1], VENV)], run_time=0.5, wrap=True, lag=0.1)
            self.play(Indicate(out37[-1].glyphs, color=VENV, scale_factor=1.1),
                      Indicate(good, color=VENV, scale_factor=1.04), run_time=0.7)

        # ========================================================== 8 · docker-shell.sh
        panel = code("docker-shell.sh", 10, 15, focus=[0, 1, 3, 4, 5])
        panel.move_to([0, 0.45, 0])
        bar11 = line_bar(panel.code, 1, TURN, 0.2)
        bar15 = line_bar(panel.code, 5, TURN, 0.2)
        helper = tag("not in the README · builds and runs in one go", S.GREY)
        helper.next_to(panel, DOWN, buff=0.35)

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(card2, t_ent2, t_c, good)), FadeOut(t2), run_time=0.5)
            self.remove(t2, *t2.lines)
            self.play(FadeIn(panel, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(helper, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("builds")
            self.play(FadeIn(bar11), Indicate(panel.code.code_lines[1], color=TURN, scale_factor=1.04), run_time=0.5)
            vo.wait_until("and runs")
            self.play(FadeIn(bar15), Indicate(panel.code.code_lines[5], color=TURN, scale_factor=1.04), run_time=0.5)

        # ========================================================== 9 · part-1 recap
        stack9, slabs9, brace9 = build_stack(-3.0, -0.45, 0.8)
        base_name = mono("python:3.12-slim-bookworm", 20, S.GREY).next_to(stack9.floor, DOWN, buff=0.15)
        card9 = ConfigCard(rows=("ENTRYPOINT", "CMD"), card_w=6.0, inline=False)
        card9.shift(np.array([6.3 - card9.frame.get_right()[0], 2.25 - card9.frame.get_top()[1], 0]))
        t_ent9 = card9.place("ENTRYPOINT", card9.tile(ENT))
        t_cmd9 = card9.place("CMD", card9.tile(CMD_IMG))
        done = VGroup(check_mark(0.4, IMAGE), label("your image: built and run", 28, IMAGE)).arrange(RIGHT, buff=0.25)
        done.move_to([0, -1.5, 0])
        nxt = label("Part 2: what's inside, why it rebuilt, and shipping it to a VM", 26, INK)
        nxt_box = box(nxt.width + 0.7, nxt.height + 0.5, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        nxt.move_to(nxt_box)
        closing = VGroup(nxt_box, nxt).move_to([0, -2.75, 0])

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(panel, bar11, bar15, helper)), track(tr, 16), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.4) for s in slabs9], lag_ratio=0.12),
                      FadeIn(VGroup(brace9, base_name)), FadeIn(VGroup(card9, t_ent9, t_cmd9), shift=LEFT * 0.2),
                      run_time=1.1)
            self.add(stack9)
            vo.wait_until("own image")
            self.play(Create(done[0]), FadeIn(done[1], shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(VGroup(*slabs9), color=IMAGE, scale_factor=1.03), run_time=0.6)
            vo.wait_until("In part 2")
            self.play(FadeIn(closing, shift=UP * 0.15), run_time=0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
