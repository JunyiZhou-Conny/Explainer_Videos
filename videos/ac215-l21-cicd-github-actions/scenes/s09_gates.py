"""S09 · Gates speak in exit codes (AC215 L21). TRACKER P5 8, STRIP Lint and Format.
Lecture: 21 · slides 22, 27 (beat 0 only). Set piece V6 ExitGates.

Beats (script.md "## S09", one voiceover block each):
0. TRACKER P5 8; the Part 2 strip moves on from `Build Container` to `Lint and Format` (YELLOW).
   LECTURE 21 · 22, 27. Two PURPLE boxes "Black" and "Flake8"; slide 22's GREY chips "coding
   standards" and "static code analysis" slide onto them. Under them a GREY line "formatter: rewrites
   · linter: reports" with a GREY dashed "L09" chip.
1. LECTURE off. README(296–301) card (299–301 light in turn), which then shrinks into the tracker's
   caption; CODE(ci.yml 59–67) takes its place. Lines 61 and 66 are too long for the frame: they are
   soft-wrapped (a GREY ↪ marks each continuation row; the text is the file's). `api/` and the two
   120 flags YELLOW; line 62 `continue-on-error: false` RED + "← blocking"; line 67 `true` GREY +
   "← advisory" (labels, not chips: a chip is taller than a code row and would cover the row above).
2. V6 ExitGates as a generic demo (gates "step 1" … "step 5"), centred: steps 1–2 hold up `0` and
   open GREEN; step 3 holds up `1` and shuts RED, the red climbs to the job badge, then the run
   badge; the gates below grey out, dashed.
3. The demo's codes go and the column morphs into run 1's lint job (Checkout, Download, Load,
   Black, Flake8), moved left; Checkout, Download, Load hold up `0`. LOG(run1/lint-and-format/04: 4, 6, 7) right (blank line
   5 dropped; line 7 soft-wrapped): line 4 RED, `Oh no! 💥 💔 💥` with the emoji drawn (star burst, broken heart); badge "exit 1". The
   Black gate holds up `1` and shuts.
4. The log gives way to STEPS(run1/lint-and-format: 2–7) (illustration): Black ✗ lights, the red
   climbs on V6 (job, run); Flake8 ⊘ lights and V6's Flake8 gate greys out, dashed. On "unless they
   ask to run always" a PINK chip `if: always()` under the list.
5. V6 steps aside (fades left: the 22 pt panel needs the full width); CODE(src/api-service/api/
   utils.py: 7–13) centred: the comma of `def power(base,exponent):`
   RED-ringed; lines 10–12 (three blank lines) shaded RED. GREY chip "the mess from L09 · kept on
   purpose for teaching".
6. V6 returns as it was; the dashed Flake8 ghost gate pulses; LOG(run1/lint-and-format/x4: 4–5) (extra; title "Lint and
   Format Check · extra: Flake8, if it had run"): `7:15 … E231` and `13:1 … E303` light. V6: the
   ghost gate holds up `1`, a GREY shunt arc carries the flow around it (continue-on-error), a small
   YELLOW warning dot on the job badge; the Black gate and the job badge pulse.
7. The log leaves; V6 moves to the centre, the line "exit code ≠ 0 → the step fails" (≠ 0 RED)
   appears under it, and the column shrinks into the line, which moves to the centre. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _gate_open  # V6's gate swing (not exported by *)

SAY = NARRATION["S09"]

# ------------------------------------------------------------------ the real sources (checked)
CI = ".github/workflows/ci.yml"
UTILS = "src/api-service/api/utils.py"
assert excerpt(CI, 59, 59).strip() == "- name: Run Black formatter check"
assert excerpt(CI, 61, 61).strip() == \
    "docker run --rm cheese-app-api:${{ github.sha }} black --check --line-length 120 api/"
assert excerpt(CI, 62, 62).strip() == "continue-on-error: false"
assert excerpt(CI, 64, 64).strip() == "- name: Run Flake8 linter"
assert excerpt(CI, 66, 66).strip() == ("docker run --rm cheese-app-api:${{ github.sha }} flake8 "
                                       "--max-line-length=120 --extend-ignore=E203,W503 api/")
assert excerpt(CI, 67, 67).strip() == "continue-on-error: true"
assert excerpt(UTILS, 7, 7) == "def power(base,exponent):"
assert [excerpt(UTILS, n, n) for n in (10, 11, 12)] == ["", "", ""]
assert excerpt(UTILS, 13, 13) == "def unused_function():"
assert "Black formatter" in readme(299) and "Flake8 linter" in readme(300)
assert "continue-on-error: true" in readme(301)

L04 = capture("run1/lint-and-format/04")
assert L04.line(4) == "would reformat /app/api/utils.py", L04.line(4)
assert L04.line(5) == "" and L04.line(6).startswith("Oh no!")
assert L04.line(7) == "1 file would be reformatted, 2 files would be left unchanged."
assert L04.exit == 1
X4 = capture("run1/lint-and-format/x4")
assert X4.line(4).startswith("api/utils.py:7:15: E231"), X4.line(4)
assert X4.line(5).startswith("api/utils.py:13:1: E303"), X4.line(5)
assert X4.exit == 1
ST = steps("run1", "lint-and-format")
assert [(s.n, s.state) for s in ST] == [(2, "success"), (3, "success"), (4, "success"), (5, "failure"),
                                         (6, "skipped")], ST
assert job_result("run1", "lint-and-format") == "failure"

GATE_NAMES = ("Checkout", "Download", "Load", "Black", "Flake8")
DEMO_NAMES = ("step 1", "step 2", "step 3", "step 4", "step 5")
RIGHT_X = 6.5               # right edge of the right-hand zone
LOG_TOP = 2.05              # Part 2 pictures stay below PIC_TOP2 (2.15)
GATES_LEFT = -6.45          # V6's left edge from beat 3 on


def top_at(m, y: float = LOG_TOP, x: float = 0.0):
    """Place m with its top edge at y, centred on x."""
    return m.move_to([x, y - m.height / 2, 0])


def right_zone(m, left: float, y: float = LOG_TOP):
    """Centre m in [left, RIGHT_X] with its top at y."""
    assert m.width <= RIGHT_X - left + 1e-6, (m.width, RIGHT_X - left)
    return top_at(m, y, (left + RIGHT_X) / 2)


def wrapped_code(path: str, a: int, b: int, folds: dict, size: float = 22) -> VGroup:
    """CODE(path: a–b) with long lines soft-wrapped, as an editor shows them: folds = {file line: [break
    after these substrings]}. Continuation rows are indented two columns deeper and marked with a GREY
    '↪' in the margin; every character is the file's. .code .header .rows{file line: [row indices]}
    .marks"""
    src_rows, rows = [], {}
    for n in range(a, b + 1):
        s = excerpt(path, n, n)
        ind = len(s) - len(s.lstrip())
        parts, rest = [], s
        for cut_after in folds.get(n, []):
            i = rest.index(cut_after) + len(cut_after)
            parts.append(rest[:i].rstrip())
            rest = rest[i:].lstrip()
        parts.append(rest)
        rows[n] = []
        for k, p_ in enumerate(parts):
            rows[n].append(len(src_rows))
            src_rows.append(p_ if k == 0 else " " * (ind + 2) + p_)
    assert "".join("".join(src_rows).split()) == "".join(excerpt(path, a, b).split())
    c = code_block("\n".join(src_rows), "yaml", size)
    head = VGroup(mono(shown_path(path), CAPTION, S.GREY), label(f"· lines {a}–{b}", CAPTION, S.GREY)) \
        .arrange(RIGHT, buff=0.14)
    head.next_to(c, UP, buff=0.1).align_to(c, LEFT).shift(RIGHT * 0.12)
    marks = VGroup()
    for n, ks in rows.items():
        for k in ks[1:]:
            ln = c.code_lines[k]
            mk = label("↪", 20, S.GREY).next_to(ln, LEFT, buff=0.18)
            marks.add(mk)
    g = VGroup(c, head, marks)
    g.code, g.header, g.rows, g.marks, g.src_rows = c, head, rows, marks, src_rows
    return g


def span(panel, n: int, sub: str):
    """Glyphs of `sub` in file line n of a wrapped_code panel (searched row by row)."""
    for k in panel.rows[n]:
        if sub in panel.src_rows[k]:
            return code_span(panel.code, k, sub)
    raise ValueError(f"{sub!r} not in line {n}")


def burst(h: float) -> VGroup:
    """💥 as a small ORANGE star burst with a YELLOW core, about one emoji tall."""
    outer = Star(n=8, outer_radius=h * 0.55, inner_radius=h * 0.26, stroke_width=0) \
        .set_fill(S.ORANGE, 1)
    core = Star(n=8, outer_radius=h * 0.3, inner_radius=h * 0.15, stroke_width=0) \
        .set_fill(S.YELLOW, 1).rotate(PI / 8)
    return VGroup(outer, core)


def broken_heart(h: float) -> VGroup:
    """💔 as a RED heart with a dark zigzag crack down its middle."""
    def pt(t):
        x = 16 * np.sin(t) ** 3
        y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
        return np.array([x, y, 0]) / 32
    heart = ParametricFunction(pt, t_range=[0, TAU], stroke_width=0).set_fill(ERR, 1)
    heart.scale_to_fit_height(h * 0.95)
    top, bot = heart.get_top()[1] - h * 0.18, heart.get_bottom()[1] + h * 0.05
    cx, dx = heart.get_center()[0], h * 0.1
    ys = np.linspace(top, bot, 5)
    crack = VMobject(stroke_color=TERM_BG, stroke_width=3).set_points_as_corners(
        [[cx + (dx if k % 2 else -dx * 0.4), y, 0] for k, y in enumerate(ys)])
    return VGroup(heart, crack)


def draw_emoji(row, chars: str):
    """Swap emo_line's GREY placeholder boxes in `row` (in the order of `chars`) for drawn glyphs, so
    'Oh no! 💥 💔 💥' does not read as missing-font tofu. Shared fix requested in common.emo_line."""
    assert len(row.emoji) == len(chars), (len(row.emoji), chars)
    new = VGroup()
    for box_, ch in zip(list(row.emoji), chars):
        h = box_.height * 1.05
        g = burst(h) if ch == "💥" else broken_heart(h)
        g.move_to(box_)
        row.remove(box_)
        row.add(g)
        new.add(g)
    row.emoji = new
    return row


class ExitCodes(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S09"] == 8, len(SAY)

        # ========================================================== 0. Black and Flake8, in the lecture's words
        tr = tracker_p5(8)
        strip = pipeline_strip("Build Container")
        ref = lref("22, 27")
        tools = VGroup()
        for name in ("Black", "Flake8"):
            fr = box(3.6, 1.15, TOOL, fill_opacity=0.12, radius=0.16)
            t = label(name, 30, TOOL).move_to(fr)
            b = VGroup(fr, t)
            b.frame, b.text = fr, t
            tools.add(b)
        tools.arrange(RIGHT, buff=1.6).move_to([0, 0.15, 0])
        chips = VGroup(grey_chip("coding standards", size=22), grey_chip("static code analysis", size=22))
        for c_, b in zip(chips, tools):
            c_.next_to(b, UP, buff=0.3)
        starts = [np.array([-6.45 + chips[0].width / 2, 1.75, 0]), np.array([6.45 - chips[1].width / 2, 1.75, 0])]
        rule = label("formatter: rewrites · linter: reports", 24, S.GREY)
        l09 = dashed_chip("L09", size=20)
        rule_g = VGroup(rule, l09).arrange(RIGHT, buff=0.3).move_to([0, -1.75, 0])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(strip, shift=RIGHT * 0.3), run_time=0.6)
            vo.wait_until("Next, lint and format")
            self.play(strip.set_current("Lint and Format"), run_time=0.6)
            self.add(strip)
            vo.wait_until("The lecture's coding standards")
            self.play(FadeIn(ref), FadeIn(tools, shift=UP * 0.15), run_time=0.6)
            ch0 = chips[0].copy().move_to(starts[0])
            self.play(FadeIn(ch0, shift=RIGHT * 0.3), run_time=0.4)
            vo.wait_until("are Black here")
            self.play(ch0.animate.move_to(chips[0]), Indicate(tools[0], color=TOOL, scale_factor=1.06), run_time=0.8)
            vo.wait_until("and its static code analysis")
            ch1 = chips[1].copy().move_to(starts[1])
            self.play(FadeIn(ch1, shift=LEFT * 0.3), run_time=0.4)
            vo.wait_until("is Flake8")
            self.play(ch1.animate.move_to(chips[1]), Indicate(tools[1], color=TOOL, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Remember lecture 9")
            self.play(FadeIn(rule_g, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("a formatter rewrites your code")
            self.play(Indicate(rule[:len("formatter:rewrites")], color=INK, scale_factor=1.05),
                      Circumscribe(tools[0], color=TOOL, buff=0.08), run_time=0.8)
            vo.wait_until("a linter only reports")
            self.play(Circumscribe(tools[1], color=TOOL, buff=0.08), run_time=0.8)

        # ========================================================== 1. the two steps in ci.yml
        card = top_at(readme_panel(296, 301))
        cp = wrapped_code(CI, 59, 67, {61: ["${{ github.sha }} black"],
                                       66: ["${{ github.sha }} flake8"]})
        assert cp.width <= 12.6, cp.width
        top_at(cp, LOG_TOP - 0.05, x=-0.25)
        blk = label("← blocking", 22, ERR).next_to(span(cp, 62, "false"), RIGHT, buff=0.35)
        adv = label("← advisory", 22, S.GREY).next_to(span(cp, 67, "true"), RIGHT, buff=0.35)
        with self.voiceover(SAY[1]) as vo:
            pic = VGroup(tools, ch0, ch1, rule_g)
            self.play(FadeOut(pic), FadeOut(ref), FadeIn(card, shift=DOWN * 0.15), run_time=0.6)
            self.remove(pic, *pic.get_family(), ref)
            hb = VGroup(hl_bar(card.rows[299], TOOL, 0.22), hl_bar(card.rows[300], TOOL, 0.22))
            self.play(FadeIn(hb), run_time=0.4)
            vo.wait_until("Both run inside the image")
            self.play(Indicate(VGroup(card.rows[299], card.rows[300]), color=TOOL, scale_factor=1.03), run_time=0.7)
            vo.wait_until("on the api folder")
            cap_copy = tr.caption.copy()
            self.play(ReplacementTransform(VGroup(card, hb), cap_copy), FadeIn(cp, shift=UP * 0.15), run_time=0.6)
            self.remove(cap_copy, card, hb)
            self.add(tr)
            apis = VGroup(span(cp, 61, "api/"), span(cp, 66, "api/"))
            self.play(apis.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(apis, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("at 120 columns")
            flags = VGroup(span(cp, 61, "--line-length 120"), span(cp, 66, "--max-line-length=120"))
            self.play(flags.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(flags, color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("The Black step says")
            s62 = span(cp, 62, "continue-on-error: false")
            b62 = hl_bar(s62, ERR, 0.2)
            self.play(FadeIn(b62), s62.animate.set_color(ERR), run_time=0.5)
            vo.wait_until("it blocks")
            self.play(FadeIn(blk, shift=LEFT * 0.2), run_time=0.4)
            vo.wait_until("The Flake8 step says true")
            s67 = span(cp, 67, "continue-on-error: true")
            b67 = hl_bar(s67, S.GREY, 0.25)
            self.play(FadeIn(b67), s67.animate.set_color(S.GREY), run_time=0.5)
            vo.wait_until("it's advisory")
            self.play(FadeIn(adv, shift=LEFT * 0.2), run_time=0.4)
            vo.wait_until("a warning that never fails the job")
            self.play(Indicate(adv, color=INK, scale_factor=1.08), run_time=0.7)

        # ========================================================== 2. V6: the rule, on a generic job
        eg = ExitGates(DEMO_NAMES).move_to([0, -0.65, 0])
        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(cp, blk, adv, b62, b67)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            self.play(FadeIn(eg, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Every command ends with an exit code")
            self.play(LaggedStart(*[Indicate(g, color=INK, scale_factor=1.12) for g in eg.gates], lag_ratio=0.15),
                      run_time=1.0)
            vo.wait_until("Zero opens the gate")
            eg.hold(self, 0, 0)
            eg.hold(self, 1, 0)
            vo.wait_until("Anything else shuts it")
            eg.hold(self, 2, 1)
            vo.wait_until("and the red climbs")
            eg.climb(self)
            eg.skip(self, [3, 4])

        # ========================================================== 3. run 1: Black says 1
        zl = GATES_LEFT + ExitGates(GATE_NAMES).width + 0.25          # the right-hand zone: [zl, RIGHT_X]
        zw = RIGHT_X - zl - 0.01
        log = run_log(L04, (4, 6, 7), colors={4: ERR}, wrap=True, max_w=zw)
        draw_emoji(log.row(6), "💥💔💥")
        demo = eg
        eg = ExitGates(GATE_NAMES).move_to([0, -0.65, 0])
        eg.shift(RIGHT * (GATES_LEFT - eg.get_left()[0]))
        with self.voiceover(SAY[3]) as vo:
            # a fresh piece, not demo.reset(): reset's badge Transform back to 'idle' collapses the
            # cross mark and shifts the badges (see the report)
            demo.drop(self, *demo.codes.values(), *demo.extras, run_time=0.3)
            self.play(ReplacementTransform(demo, eg), run_time=0.9)
            self.remove(demo)
            self.add(eg)
            # Checkout, Download, Load hold up 0 together (one by one, hold() put the log 1.5 s behind
            # "would reformat")
            zeros = [chip("0", PASS, size=22, font=MONO).next_to(eg.gates[i], RIGHT, buff=0.3) for i in range(3)]
            self.play(LaggedStart(*[FadeIn(z, shift=UP * 0.2) for z in zeros], lag_ratio=0.25), run_time=0.45)
            self.play(*[_gate_open(eg.gates[i]) for i in range(3)], run_time=0.4)
            for i, z in enumerate(zeros):
                eg.opened.add(i)
                eg.codes[i] = z
            eg.keep(self, *zeros)
            vo.wait_until("the Black step")
            right_zone(log, zl)
            self.play(FadeIn(log, shift=LEFT * 0.2), Indicate(eg.names[3], color=TOOL, scale_factor=1.15),
                      run_time=0.6)
            vo.wait_until("would reformat utils dot py")
            self.play(Indicate(log.row(4), color=ERR, scale_factor=1.05), run_time=0.7)
            vo.wait_until("One file would be reformatted")
            r7 = VGroup(*[r for r in log.rows if r is not log.row(4) and r is not log.row(6)])
            hb7 = hl_bar(r7, ERR, 0.18)
            self.play(FadeIn(hb7), run_time=0.4)
            vo.wait_until("Exit code 1")
            self.play(Circumscribe(log.badge, color=ERR, buff=0.06), run_time=0.7)
            vo.wait_until("so the gate shuts")
            eg.hold(self, 3, 1)

        # ========================================================== 4. the step list: failure, skipped
        sl = steps_list("run1", "lint-and-format", ((2, 7),))
        right_zone(sl, zl, LOG_TOP - 0.05)
        always = route_chip("if: always()", size=22).next_to(sl, DOWN, buff=0.25)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(log, hb7)), FadeIn(sl, shift=LEFT * 0.2), run_time=0.6)
            self.remove(log, hb7)
            vo.wait_until("Black, failure")
            self.play(Indicate(sl.row(5), color=ERR, scale_factor=1.05), run_time=0.6)
            eg.climb(self)
            self.play(Indicate(sl.row(7), color=ERR, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Flake8, skipped")
            self.play(Indicate(sl.row(6), color=S.GREY, scale_factor=1.05), run_time=0.6)
            eg.skip(self, [4])
            vo.wait_until("The steps below a failed step")
            self.play(Circumscribe(VGroup(eg.gates[4], eg.names[4]), color=S.GREY, buff=0.1), run_time=0.8)
            vo.wait_until("unless they ask to run always")
            self.play(FadeIn(always, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 5. the cause: L09's mess, kept on purpose
        up = code(UTILS, 7, 13)
        mess = grey_chip("the mess from L09 · kept on purpose for teaching", size=22)
        top_at(up, LOG_TOP - 0.35)
        mess.next_to(up, DOWN, buff=0.4)
        comma = code_span(up.code, 0, ",")
        cl = up.code.code_lines
        y9, y13 = cl[2].get_center()[1], cl[6].get_center()[1]
        pitch = (y9 - y13) / 4
        bg = up.code.background
        blanks = VGroup(*[Rectangle(width=bg.width - 0.12, height=pitch * 0.9, stroke_width=0)
                          .set_fill(ERR, 0.25).move_to([bg.get_center()[0], y9 - j * pitch, 0]) for j in (1, 2, 3)])
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(sl, always)), FadeOut(eg, shift=LEFT * 0.3), run_time=0.5)
            self.remove(sl, always, eg)
            self.play(FadeIn(up, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("still in the repository on purpose")
            self.play(FadeIn(mess, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("no space after the comma")
            rc = ring(comma, ERR, buff=0.1, stroke=4)
            self.play(Create(rc), comma.animate.set_color(ERR), run_time=0.6)
            self.play(Indicate(comma, color=ERR, scale_factor=1.6), run_time=0.6)
            vo.wait_until("and three blank lines")
            self.play(LaggedStart(*[FadeIn(b) for b in blanks], lag_ratio=0.35), run_time=0.9)

        # ========================================================== 6. the skipped Flake8, replayed as a ghost
        xlog = run_log(X4, (4, 5), title="Lint and Format Check · extra: Flake8, if it had run",
                       wrap=True, max_w=zw)
        right_zone(xlog, zl)
        xt = extra_tag().next_to(xlog.frame, DOWN, buff=0.15).align_to(xlog.frame, LEFT)
        ghost = eg.extras[-1] if len(eg.extras) else eg.gates[4]
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(up, mess, rc, blanks)), FadeIn(eg, shift=RIGHT * 0.3), run_time=0.6)
            self.remove(up, mess, rc, blanks)
            self.play(Indicate(VGroup(ghost, eg.names[4]), color=S.GREY, scale_factor=1.12), run_time=0.8)
            vo.wait_until("An extra run shows two warnings")
            self.play(FadeIn(xlog, shift=LEFT * 0.2), FadeIn(xt), run_time=0.6)
            vo.wait_until("on those same lines")
            spots = VGroup(substring(xlog.row(4), "utils.py:7:15"), substring(xlog.row(5), "utils.py:13:1"))
            hbs = VGroup(*[hl_bar(s_, TURN, 0.25) for s_ in spots])
            self.play(FadeIn(hbs), run_time=0.4)
            self.play(Indicate(spots, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("But even then it's advisory")
            eg.shunt(self, 4, 1)
            vo.wait_until("only Black decides the job")
            self.play(Indicate(VGroup(eg.gates[3], eg.codes[3]), color=ERR, scale_factor=1.15),
                      Circumscribe(eg.job_badge, color=ERR, buff=0.08), run_time=0.9)

        # ========================================================== 7. the whole rule
        rule2 = VGroup(label("exit code", 34, INK), label("≠ 0", 34, ERR), label("→", 34, S.GREY),
                       label("the step fails", 34, INK)).arrange(RIGHT, buff=0.25).move_to([0, -0.6, 0])
        with self.voiceover(SAY[7]) as vo:
            out_g = VGroup(xlog, xt, hbs)
            self.play(FadeOut(out_g), run_time=0.5)
            self.remove(out_g, *out_g.get_family())
            self.play(eg.animate.move_to([0, -0.4, 0]), run_time=0.7)
            vo.wait_until("a step fails when its command exits")
            under_t = rule2.copy().next_to(eg, DOWN, buff=0.25)
            if under_t.get_bottom()[1] < -3.5:
                under_t.shift(UP * (-3.5 - under_t.get_bottom()[1]))
            self.play(FadeIn(under_t, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("anything but zero")
            self.play(Indicate(under_t[1], color=ERR, scale_factor=1.2), run_time=0.7)
            vo.wait_until("It's the only thing CI listens to")
            # the column condenses into its line: it shrinks into the text, which takes the centre
            self.play(eg.animate.scale(0.15).move_to(under_t).set_opacity(0),
                      under_t.animate.move_to(rule2), run_time=0.9)
            self.remove(eg, *eg.get_family())
            self.play(Indicate(under_t, color=INK, scale_factor=1.06), run_time=0.8)

        self.wait(0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
