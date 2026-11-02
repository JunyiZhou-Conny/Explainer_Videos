"""S08 · The system test and the silent skip (README Part 3 Option 2, tracker C6 -> C8).

Beats (script.md, ## S08; one voiceover block each):
0. TRACKER C6; `Lecture 9 · slides 94–97` (top right, whole scene). Title card: slide 94's question
   "can anything but our code make it fail?" over the GREEN dashed border. Then a GREY chip over the
   terminal: the README repeats the build (line 190, `laptop/part3-opt2-01`: all CACHED). Full
   terminal: `docker run -d --name api-server -p 9000:9000 -e DEV=1 cheese-app-api:local`
   (README:193, folds) -> part3-opt2-02: 2 (the container ID, ringed TEAL). `▶ your turn`.
1. TRACKER C6 · extra: `until curl -sf …/health; do sleep 1; done; echo` (extra) -> part3-opt2-03: 2;
   GREY note "CI waits too · ci.yml:150–154"; `docker ps` (extra) -> part3-opt2-04: 2–3 (columns
   STATUS, PORTS, NAMES).
2. TRACKER C7: `docker run --rm --network host cheese-app-api:local pytest tests/system/ -v`
   (README:196) -> part3-opt2-05: 13–17, 19 (`5 passed` GREEN). The terminal shrinks to a strip
   holding the command and its summary; above it the V2 wire picture: a TEAL test container (five
   BLUE dots, pytest) and the TEAL api-server container (`server :9000`) joined by the PINK
   `--network host` wire; the request token crosses, `{"distance": 5.0}` comes back. `▶ your turn`.
3. The five dots pass (BLUE, GREEN checks), the wire flashes. PONDER (8 s).
4. TRACKER C8: the dots go idle in a row above a full terminal: `docker stop api-server && docker
   rm api-server` (README:199) -> part3-opt2-06: 2–3. `▶ your turn`.
5. TRACKER C8 · extra: the same system command (extra) -> part3-opt2-07: 13–17, 19–24 (wrap).
   `1 passed, 4 skipped` GREEN with a YELLOW "still green" tag; the four dots turn GREY dashed "s";
   the four SKIPPED rows are ringed.
6. CODE(test_system_api.py: 15–25): is_api_running, line 24's skipif YELLOW, a YELLOW clock chip
   "evaluated once · at collection"; a smoke detector whose battery slides out, GREY zzz,
   "silent ≠ no fire".
7. The border picture: 22 dots inside the hermetic border (11 GREEN unit, 11 TEAL: 10 integration +
   test_api_structure, ringed), 4 BLUE system dots outside, GREY dashed; a dashed "marker" chip
   (part 2). A GREY dashed CI card: CODE(ci.yml: 150–154), `curl -f … || exit 1` RED-outlined,
   "CI fails loudly · lecture 21". Both fade; the gate table's system row fills outside the
   turnstile, GREY dashed. Fade out.

Deviations (reported to the coordinator):
- CODE(test_system_api.py) shows 15–25, not 11–25 (15 lines; a panel takes <= 12). Line 24 is 86
  characters (the frame takes 72 at 20 pt): it is cut at the frame edge with the house "…" (common
  `cut`), after `reason="API not running at`; the narrated `skipif(not is_api_running()` stays whole.
- docker ps (part3-opt2-04) is 122 characters wide even squeezed; it shows the columns STATUS, PORTS,
  NAMES (`cols`), which carry what the narration names ("shows the server up").
- The script puts the wire picture "beside the terminal"; a full terminal and a picture never share
  the frame, so the terminal first shrinks to a strip (command + `5 passed`) and the picture stands
  above it. The dots row above the 10-row terminal in beats 4–5 is a one-row legend, not a picture.
- Border dots: SCENE-NOTES' kinds colouring (11 GREEN unit + 11 TEAL), not "21 GREEN": the 10
  integration tests run in-process (TEAL, as S03 taught); the 22nd TEAL dot is ringed.
- pytest's summary lines are shown without their '=' padding (as S03/S07 do); long PASSED/SKIPPED
  test-id rows break as S07's soft() does; the -ra SKIPPED rows wrap at the terminal edge.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer import style as S

from common import (ERR, FUTURE, IMAGE, INK, NARRATION, P_LAPTOP, PASS, ROUTE, SKIP,
                    SYSTEM_TEST, TURN, UNIT, INTEG, GateTable, HermeticBorder, RequestToken, RESPONSE,
                    TestDots, attach, beside, capture, check_mark, chip, code, code_panel, code_span,
                    cols, excerpt, extra_row, hl_bar, label, line_bar, lref, mono,
                    cut, note, outline_box, pause_and_ponder, pin, readme, resize, ring, row_tag, shown_path,
                    substring, term, tool_chip, track, tracker, turn_row, type_cmd, unpin)

SAY = NARRATION["S08"]
SYS = "cheese-app-ci-cd/tests/system/test_system_api.py"
CI = "cheese-app-ci-cd/.github/workflows/ci.yml"
C0, C1 = 15, 25                     # test_system_api.py window (line 24 cut at the frame edge)


def summary(cap, n: int) -> str:
    """A pytest summary line without its '=' padding (as S03/S07 show them)."""
    s = cap.line(n)
    assert s.startswith("=") and s.endswith("="), s
    return s.strip("= ")


def soft(lines: list[str], n: int) -> list[str]:
    """pytest's long rows broken at the last space that fits (S07): 'PASSED' never splits; a test
    id longer than a row breaks at the edge, as a terminal wraps it."""
    out = []
    for s in lines:
        while len(s) > n:
            k = s.rfind(" ", 0, n + 1)
            if k > 0:
                out.append(s[:k])
                s = s[k + 1:]
            else:
                out.append(s[:n])
                s = s[n:]
        out.append(s)
    return out


def rows_of(line) -> list:
    return list(line.rows) if hasattr(line, "rows") else [line]


def find_in(line, sub: str) -> list:
    """The glyphs of `sub` in a typed command, as one group per row: a fold may split `sub`
    between rows, so each word is found on its own row then. Flash the pieces with flash()."""
    for r in rows_of(line):
        if sub in r.text:
            return [substring(r, sub)]
    parts, rows = [], rows_of(line)
    for w in sub.split():
        hit = [r for r in rows if w in r.text]
        if not hit:
            raise KeyError(sub)
        parts.append(substring(hit[0], w))
    return parts


def flash(pieces, color, scale: float = 1.12, run_time: float = 0.8):
    """One Indicate per piece (each scales about its own centre, never the group's), together."""
    return AnimationGroup(*[Indicate(p, color=color, scale_factor=scale) for p in pieces], run_time=run_time)


def tag_on(scene, line, mk, anim=None):
    """Pin a row tag (mk()) beside a typed command: its last row, or its first row when the last
    is too long to leave room. Returns (row, tag) for unpin()."""
    rs = rows_of(line)
    row = rs[-1]
    t = beside(mk(), row)
    if t.get_right()[0] > 6.55:
        row = rs[0]
        t = beside(mk(), row)
    assert t.get_right()[0] <= 6.55, line
    if anim is not None:
        pin(scene, row, t, anim=AnimationGroup(FadeIn(t, shift=LEFT * 0.1), anim))
    else:
        pin(scene, row, t)
    return row, t


def container(title: str, box_w: float, box_h: float, mono_title: bool = False) -> VGroup:
    """A TEAL container box with its name at the top inside. .frame .title"""
    f = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.16, stroke_color=IMAGE,
                         stroke_width=3).set_fill(IMAGE, 0.07)
    t = (mono if mono_title else label)(title, 22, IMAGE)
    t.next_to(f.get_top(), DOWN, buff=0.25)
    g = VGroup(f, t)
    g.frame, g.title = f, t
    return g


def clock(r: float = 0.17, color=TURN) -> VGroup:
    face = Circle(radius=r, stroke_color=color, stroke_width=3)
    h1 = Line(ORIGIN, UP * r * 0.65, color=color, stroke_width=3)
    h2 = Line(ORIGIN, RIGHT * r * 0.5, color=color, stroke_width=3)
    return VGroup(face, h1, h2)


def smoke_detector() -> VGroup:
    """A ceiling smoke detector seen from below, its battery in the slot. .body .led .battery .slot"""
    body = Circle(radius=0.62, stroke_color=S.GREY, stroke_width=3).set_fill(S.GREY_DARKER, 1)
    inner = Circle(radius=0.36, stroke_color=S.GREY, stroke_width=2)
    vents = VGroup(*[Line(LEFT * 0.2, RIGHT * 0.2, color=S.GREY, stroke_width=2).shift(UP * dy)
                     for dy in (-0.12, 0, 0.12)])
    led = Dot(radius=0.05, color=S.GREY_DARK).move_to(body.get_center() + np.array([0.45, 0.2, 0]))
    slot = DashedVMobject(Rectangle(width=0.62, height=0.26), num_dashes=14, dashed_ratio=0.5)
    slot.set_stroke(S.GREY, 2).next_to(inner, DOWN, buff=0.04)
    cell = RoundedRectangle(width=0.56, height=0.22, corner_radius=0.04, stroke_color=S.GREY,
                            stroke_width=2).set_fill(S.GREY, 0.35)
    nub = Rectangle(width=0.05, height=0.1, stroke_width=0).set_fill(S.GREY, 1).next_to(cell, RIGHT, buff=0)
    battery = VGroup(cell, nub).move_to(slot)
    g = VGroup(body, inner, vents, led, slot, battery)
    g.body, g.led, g.battery, g.slot = body, led, battery, slot
    return g


class SilentSkip(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)
        build, run, wait = capture("part3-opt2-01"), capture("part3-opt2-02"), capture("part3-opt2-03")
        ps, sysc, stop = capture("part3-opt2-04"), capture("part3-opt2-05"), capture("part3-opt2-06")
        nosrv = capture("part3-opt2-07")
        for c, n in ((build, 190), (run, 193), (sysc, 196), (stop, 199), (nosrv, 196)):
            assert c.cmd == readme(n), (c.cmd, readme(n))
        assert any(s == "#6 CACHED" for s in build.lines)

        # ========================================================== 0. the question, a live server
        tr = tracker("C", 6)
        ref = lref("94–97")
        q = label("can anything but our code make it fail?", 36, INK)
        border = HermeticBorder(q.width + 1.6, 2.2)
        border.move_to([0, 0.2, 0])
        q.move_to(border.frame).shift(DOWN * 0.1)

        t = term(P_LAPTOP, rows=10)
        b1 = label("the README repeats the build first (line 190):", 20, S.GREY)
        b2 = VGroup(mono(build.cmd, 20, INK), label("· already built, all CACHED", 20, S.GREY))
        b2.arrange(RIGHT, buff=0.15)
        bt = VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        bf = RoundedRectangle(width=bt.width + 0.5, height=bt.height + 0.32, corner_radius=0.12,
                              stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.1)
        bt.move_to(bf)
        bchip = VGroup(bf, bt).move_to([0, (t.box.get_top()[1] + 2.85) / 2, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.7)
            self.play(Indicate(tr.dots[5], color=TURN, scale_factor=1.6), run_time=0.5)
            self.play(Create(border.frame), FadeIn(border.text), run_time=0.8)
            vo.wait_until("the lecture's question")
            self.play(FadeIn(q, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("but our code")
            self.play(Indicate(border.frame, color=UNIT, scale_factor=1.03), run_time=0.8)
            vo.wait_until("make it fail?")
            self.play(Indicate(q, color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Start a live server")
            self.play(FadeOut(VGroup(border, q), shift=UP * 0.3), run_time=0.5)
            self.remove(border, q)
            self.play(FadeIn(t), FadeIn(bchip, shift=DOWN * 0.15), run_time=0.6)
            r_ln = type_cmd(self, t, run.cmd, type_time=1.3)
            for anchor, sub in (("detached", "-d"), ("named api-server", "--name api-server"),
                                ("on port 9000", "-p 9000:9000"), ("with DEV equals 1", "-e DEV=1")):
                vo.wait_until(anchor)
                self.play(flash(find_in(r_ln, sub), TURN, 1.12, run_time=0.5))
            vo.wait_until("All you get back")
            cid = t.print(self, run.at(2), run_time=0.4)[0]
            cring = ring(cid.glyphs, IMAGE, buff=0.06)
            self.play(Create(cring), run_time=0.5)
            attach(self, cid, cring)
            vo.wait_until("Pause and run it")
            r_row, r_tag = tag_on(self, r_ln, turn_row)
            self.play(Indicate(r_tag, color=TURN, scale_factor=1.15), run_time=0.6)

        # ========================================================== 1. wait for it (extras)
        ci_note = note("CI waits too · ci.yml:150–154", S.GREY, 22).move_to(bchip)

        with self.voiceover(SAY[1]) as vo:
            unpin(self, r_row, r_tag)
            vo.wait_until("runs the tests immediately")
            self.play(Indicate(bchip, color=S.GREY, scale_factor=1.03), run_time=0.6)
            vo.wait_until("We add one extra first")
            self.play(FadeOut(bchip), run_time=0.4)
            self.remove(bchip)
            w_ln = type_cmd(self, t, wait.cmd, type_time=1.2)
            w_row, w_tag = tag_on(self, w_ln, extra_row, anim=track(tr, extra=True))
            vo.wait_until("until it answers")
            ok = t.print(self, wait.at(2), run_time=0.4)[0]
            self.play(substring(ok, "healthy").animate.set_color(PASS), run_time=0.5)
            vo.wait_until("CI waits too")
            self.play(FadeIn(ci_note, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("you will see why soon")
            self.play(Indicate(ci_note, color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("A second extra")
            unpin(self, w_row, w_tag)
            p_ln = type_cmd(self, t, ps.cmd, type_time=0.4)
            p_row, p_tag = tag_on(self, p_ln, extra_row)
            table = t.print(self, cols(ps.at(2, 3), ["STATUS", "PORTS", "NAMES"]), run_time=0.5)
            vo.wait_until("shows the server up")
            up = substring(table[1], "Up 1 second")
            self.play(up.animate.set_color(PASS), Indicate(substring(table[1], "api-server"), color=IMAGE,
                                                           scale_factor=1.12), run_time=0.8)

        # ========================================================== 2. the system tests, over the wire
        with self.voiceover(SAY[2]) as vo:
            unpin(self, p_row, p_tag, FadeOut(ci_note))
            self.remove(ci_note)
            resize(self, t, 13, extra=[track(tr, 7, extra=False)])
            s_ln = type_cmd(self, t, sysc.cmd, type_time=1.2)
            for anchor, sub in (("docker run with network host", "--network host"),
                                ("pytest tests slash system", "pytest tests/system/")):
                vo.wait_until(anchor)
                self.play(flash(find_in(s_ln, sub), TURN, 1.08, run_time=0.5))
            t.print(self, soft(sysc.at((13, 17)), t.max_chars), run_time=0.7, lag=0.08)
            s_sum = t.print(self, [(summary(sysc, 19), PASS)], run_time=0.3)[0]
            vo.wait_until("5 passed")
            self.play(Indicate(substring(s_sum, "5 passed"), color=PASS, scale_factor=1.2), run_time=0.6)

            # the strip keeps the command and its verdict; the wire picture stands above it
            resize(self, t, 3, keep=[*rows_of(s_ln), s_sum])
            left = container("test container", 3.1, 3.2).move_to([-4.85, 0.85, 0])
            right = container("api-server", 2.9, 3.2, mono_title=True).move_to([4.95, 0.85, 0])
            dots = TestDots(5, SYSTEM_TEST).move_to(left.frame).shift(DOWN * 0.15)
            pyt = tool_chip("pytest").next_to(dots, DOWN, buff=0.35)
            srv = chip("server :9000", SYSTEM_TEST, size=20).move_to(right.frame)
            wy = left.frame.get_center()[1] + 0.1
            wire = Line([left.frame.get_right()[0], wy, 0], [right.frame.get_left()[0], wy, 0],
                        color=ROUTE, stroke_width=5)
            wlab = mono("--network host", 20, S.GREY).next_to(wire, DOWN, buff=0.3)
            self.play(FadeIn(VGroup(left, right, dots, pyt, srv)), Create(wire), FadeIn(wlab), run_time=0.8)
            tok = RequestToken()
            tok.move_to(wire.get_start() + RIGHT * (tok.pill.width / 2 + 0.05) + UP * 0.55)
            vo.wait_until("really crossed the wire")
            self.play(FadeIn(tok, scale=0.8), run_time=0.3)
            self.play(tok.animate.move_to(wire.get_end() + LEFT * (tok.pill.width / 2 + 0.05) + UP * 0.55),
                      ShowPassingFlash(wire.copy().set_stroke(INK, 9), time_width=0.6), run_time=1.1)
            back = RequestToken(RESPONSE)
            back.move_to(wire.get_end() + LEFT * (back.pill.width / 2 + 0.05) + UP * 0.55)
            self.play(Indicate(srv, color=SYSTEM_TEST, scale_factor=1.1), FadeTransform(tok, back), run_time=0.6)
            self.play(back.animate.move_to(wire.get_start() + RIGHT * (back.pill.width / 2 + 0.05) + UP * 0.55),
                      run_time=1.0)
            vo.wait_until("Pause and run it")
            s_row, s_tag = tag_on(self, s_ln, turn_row)
            self.play(Indicate(s_tag, color=TURN, scale_factor=1.15), run_time=0.6)

        # ========================================================== 3. ponder: no server
        checks = VGroup(*[check_mark(0.24, PASS).next_to(d, UP, buff=0.1) for d in dots.dots])

        with self.voiceover(SAY[3]) as vo:
            unpin(self, s_row, s_tag)
            self.play(FadeOut(back), dots.to(range(5), "pass", run_time=0.8), run_time=0.8)
            self.remove(back)
            self.play(LaggedStart(*[Create(c) for c in checks], lag_ratio=0.15),
                      ShowPassingFlash(wire.copy().set_stroke(INK, 9), time_width=0.6), run_time=0.8)
            vo.wait_until("with no server running")
            self.play(Indicate(srv, color=SYSTEM_TEST, scale_factor=1.12), run_time=0.8)
            vo.wait_until("What exactly does pytest print?")
            self.play(Indicate(s_sum, color=PASS, scale_factor=1.06), run_time=0.8)
        ponder = pause_and_ponder(self, "The same system-test command,\nbut the server is not running.\n"
                                        "Fail, error, or something else?", seconds=8)

        # ========================================================== 4. clean up = the experiment
        dlab = note("tests/system/ · 5 tests", S.GREY, 22)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(ponder), run_time=0.5)
            self.remove(ponder)
            rest = VGroup(left, right, pyt, srv, wire, wlab, checks)
            self.play(FadeOut(rest), track(tr, 8), run_time=0.6)
            self.remove(rest)
            # two plays: dots.to() Transforms toward targets built where the dots stand now
            self.play(dots.to(range(5), "idle", run_time=0.5), run_time=0.5)
            resize(self, t, 10, keep=0, extra=[dots.animate.move_to([-1.6, 1.97, 0])])
            dlab.next_to(dots, RIGHT, buff=0.4)
            self.play(FadeIn(dlab, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("stop and remove the server")
            x_ln = type_cmd(self, t, stop.cmd, type_time=1.0)
            t.print(self, stop.at(2, 3), run_time=0.4)
            vo.wait_until("Pause and do it")
            x_row, x_tag = tag_on(self, x_ln, turn_row)
            self.play(Indicate(x_tag, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("doubles as our experiment")
            self.play(flash([*dots.dots, dlab], S.GREY, 1.1))

        # ========================================================== 5. the answer: still green
        with self.voiceover(SAY[5]) as vo:
            unpin(self, x_row, x_tag)
            n_ln = type_cmd(self, t, nosrv.cmd, type_time=1.0)
            n_row, n_tag = tag_on(self, n_ln, extra_row, anim=track(tr, extra=True))
            t.print(self, soft(nosrv.at((13, 17)), t.max_chars), run_time=0.7, lag=0.08)
            self.wait(0.4)
            t.print(self, [summary(nosrv, 19)], run_time=0.3)
            skipped = t.print(self, nosrv.at((20, 23)), wrap=True, run_time=0.6, lag=0.08)
            n_sum = t.print(self, [(summary(nosrv, 24), PASS)], run_time=0.3)[0]
            vo.wait_until("1 passed, 4 skipped")
            self.play(Indicate(substring(n_sum, "1 passed, 4 skipped"), color=PASS, scale_factor=1.12),
                      dots.to(4, "pass", run_time=0.5), run_time=0.8)
            vo.wait_until("the headline is still green")
            g_tag = beside(row_tag("still green", TURN), n_sum)
            pin(self, n_sum, g_tag)
            self.play(Indicate(g_tag, color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("Four gray dots")
            self.play(dots.to(range(4), "skip", run_time=1.0), run_time=1.0)
            vo.wait_until("not failures")
            self.play(flash(dots.dots[:4], SKIP, 1.25, run_time=0.7))
            vo.wait_until("Only the summary")
            sk_ring = ring(skipped, TURN, buff=0.06)
            self.play(Create(sk_ring), run_time=0.6)
            attach(self, skipped[0], sk_ring)
            vo.wait_until("tells the truth")
            words = [substring(r, "SKIPPED") for r in skipped if "SKIPPED" in r.text]
            self.play(flash(words, TURN, 1.15))
            vo.wait_until("API not running")
            apis = [substring(r, "API not running") for r in skipped if "API not running" in r.text]
            self.play(flash(apis, TURN, 1.1))

        # ========================================================== 6. why: evaluated at collection
        src = excerpt(SYS, C0, C1).split("\n")
        k24 = 24 - C0
        assert src[k24].startswith("@pytest.mark.skipif(not is_api_running(), ")
        # line 24 is 86 characters, the panel takes 72 at 20 pt: the house cut at the frame edge
        src[k24] = cut(src[k24], 'reason="API not running at')
        assert len(src[k24]) <= 72, len(src[k24])
        panel = code_panel("\n".join(src), shown_path(SYS), C0, "python", font_size=20)
        code_span(panel.code, k24, "…").set_color(S.GREY)   # pygments paints the cut's "…" as an error (pink)
        panel.move_to([0, 2.72 - panel.height / 2, 0])
        fn_bar = VGroup(*[line_bar(panel.code, k, SYSTEM_TEST, 0.14) for k in range(0, 7)])
        get_span = code_span(panel.code, 18 - C0, "requests.get")
        sk_bar = line_bar(panel.code, k24, TURN, 0.22)
        cls_span = code_span(panel.code, k24 + 1, "class TestAPIEndpoints")

        clk = clock()
        ctext = label("evaluated once · at collection", 22, TURN)
        crow = VGroup(clk, ctext).arrange(RIGHT, buff=0.2)
        cf = RoundedRectangle(width=crow.width + 0.5, height=crow.height + 0.3, corner_radius=0.14,
                              stroke_color=TURN, stroke_width=2.5).set_fill(S.BG, 0.95)
        crow.move_to(cf)
        cchip = VGroup(cf, crow)
        low = (panel.get_bottom()[1] - 3.5) / 2
        cchip.move_to([-6.4 + cchip.width / 2, low, 0])
        det = smoke_detector().move_to([2.4, low - 0.05, 0])
        zzz = label("z z z", 24, S.GREY).next_to(det, UR, buff=0.0).shift(LEFT * 0.1 + DOWN * 0.15)
        silent = note("silent ≠ no fire", S.GREY, 24).next_to(det, RIGHT, buff=0.9)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(t, sk_ring, g_tag, n_tag, dots, dlab)), track(tr, extra=False), run_time=0.6)
            self.remove(t, sk_ring, g_tag, n_tag, dots, dlab)
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("probes the server once")
            self.play(FadeIn(fn_bar), run_time=0.5)
            self.play(Indicate(get_span, color=SYSTEM_TEST, scale_factor=1.1), run_time=0.7)
            vo.wait_until("when pytest collects the module")
            self.play(FadeOut(fn_bar), FadeIn(sk_bar), run_time=0.5)
            self.play(FadeIn(cchip, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("marks the whole class")
            self.play(Indicate(cls_span, color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("a second late is too late")
            self.play(Rotate(clk[1], angle=-2 * PI, about_point=clk[0].get_center()),
                      Indicate(ctext, color=TURN, scale_factor=1.06), run_time=1.0)
            vo.wait_until("A smoke detector")
            self.play(FadeIn(det, scale=0.9), run_time=0.6)
            vo.wait_until("battery removed")
            self.play(det.battery.animate.shift(DOWN * 0.1 + RIGHT * 1.05).rotate(-0.3), run_time=0.8)
            vo.wait_until("will never beep")
            self.play(FadeIn(zzz, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("not the same as no fire")
            self.play(FadeIn(silent, shift=LEFT * 0.15), run_time=0.6)

        # ========================================================== 7. outside the border; CI; the table
        inside = TestDots(22, [UNIT] * 11 + [INTEG] * 11, cols=11, state="pass")
        inside.move_to([-3.0, 1.7, 0])
        hb = HermeticBorder.around(inside, buff=0.32)
        extra_dot = inside.dots[21]
        ed_ring = Circle(radius=0.3, stroke_color=INK, stroke_width=3).move_to(extra_dot)
        in_lab = note("22 inside · 11 unit, 11 run in-process", S.GREY, 22).next_to(hb, DOWN, buff=0.22)
        ed_lab = note("1 from tests/system/ · no server", INTEG, 22).next_to(hb, DOWN, buff=0.22)
        outside = TestDots(4, SYSTEM_TEST, state="skip").move_to([3.6, inside.get_center()[1], 0])
        out_lab = note("4 need a live server", S.GREY, 22).next_to(outside, DOWN, buff=0.4)
        out_lab.align_to(in_lab, DOWN)
        m_t = VGroup(label("a marker the run", 20, FUTURE), label("must select · part 2", 20, FUTURE))
        m_t.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        m_box = outline_box(m_t.width + 0.5, m_t.height + 0.35, FUTURE)
        m_t.move_to(m_box)
        marker = VGroup(m_box, m_t)
        marker.box, marker.text = m_box, m_t

        cip = code(CI, 150, 154)
        curl = code_span(cip.code, 154 - 150, "curl -f http://localhost:9000/ || exit 1")
        cap = note("CI fails loudly · lecture 21", S.GREY, 22)
        cap.next_to(cip, DOWN, buff=0.22).align_to(cip, LEFT)
        inner = VGroup(cip, cap)
        cframe = outline_box(inner.width + 0.6, inner.height + 0.5, FUTURE)
        cframe.move_to(inner)
        card = VGroup(cframe, inner)
        card.move_to([-6.4 + card.width / 2, -3.45 + card.height / 2, 0])
        marker.move_to([(card.get_right()[0] + 6.4) / 2, (out_lab.get_bottom()[1] - 3.45) / 2, 0])
        assert marker.get_left()[0] > card.get_right()[0] + 0.2 and marker.get_right()[0] < 6.5
        curl_bar = hl_bar(curl, S.GREY, 0.3)          # built after the card is placed
        red = ring(curl, ERR, buff=0.08, stroke=4)

        gt = GateTable(keys=("tests", "system"), filled=("tests",))
        gt.move_to([0, 0.2, 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(panel, sk_bar, cchip, det, zzz, silent)), run_time=0.6)
            self.remove(panel, sk_bar, cchip, det, zzz, silent)
            self.play(Create(hb.frame), FadeIn(hb.text), run_time=0.8)
            vo.wait_until("22 tests live inside")
            self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in inside.dots], lag_ratio=0.04), run_time=1.0)
            self.add(inside)
            vo.wait_until("the 21 from last scene")
            self.play(flash(inside.dots[:21], INK, 1.2), FadeIn(in_lab), run_time=0.8)
            vo.wait_until("plus the one system folder test")
            self.play(Create(ed_ring), FadeOut(in_lab), FadeIn(ed_lab), run_time=0.7)
            vo.wait_until("These 4 stand outside")
            self.play(LaggedStart(*[FadeIn(d, shift=LEFT * 0.3) for d in outside.dots], lag_ratio=0.15),
                      FadeIn(out_lab), run_time=0.8)
            self.add(outside)
            self.play(flash(outside.dots, SKIP, 1.25, run_time=0.6))
            vo.wait_until("The honest remedy")
            self.play(Create(marker.box.frame), FadeIn(marker.text), run_time=0.7)
            vo.wait_until("the guest lecture shows it")
            self.play(Indicate(marker, color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("CI's version is loud")
            self.play(Create(cframe.frame), FadeIn(inner, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("it curls the server first")
            self.play(FadeIn(curl_bar), run_time=0.5)
            vo.wait_until("if the server is down")
            self.play(Create(red), curl.animate.set_color(ERR), run_time=0.7)
            vo.wait_until("the whole job fails")
            self.play(Indicate(red, color=ERR, scale_factor=1.06), run_time=0.7)
            vo.wait_until("The system row enters")
            pic = VGroup(hb, inside, ed_ring, ed_lab, outside, out_lab, marker, card, curl_bar, red)
            self.play(FadeOut(pic), run_time=0.6)
            self.remove(pic)
            self.play(FadeIn(gt, shift=LEFT * 0.6), run_time=0.8)
            gt.fill(self, "system")
            vo.wait_until("not on every commit")
            gt.settle(self, "system")
            self.play(Indicate(gt.icon, color=S.GREY, scale_factor=1.3), run_time=0.6)
            vo.wait_until("not hermetic")
            self.play(Indicate(gt.rows["system"].cells[3], color=INK, scale_factor=1.12), run_time=0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
