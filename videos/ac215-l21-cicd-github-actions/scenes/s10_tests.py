"""S10 · Three test jobs, three altitudes (AC215 L21). TRACKER P5 8, STRIP Test.
Lecture: 21 · slide 27 (beat 0 only). Set pieces: V6 on the step rows (beat 3), V7 SystemTestRig
(beats 6-8), L09's trapdoor (beat 10).

Beats (script.md "## S10", one voiceover block each):
0. TRACKER P5 8; the Part 2 strip moves on to `Test` (YELLOW). LECTURE 21 · 27. The Test box grows
   down into three boxes `Unit Tests` (GREEN edge), `Integration Tests` (TEAL), `System Tests` (BLUE),
   stacked like altitudes, the unit box lowest; a GREY "closer to the real thing" arrow beside them.
1. LECTURE off. The three boxes shrink into a small altitude ladder right of the strip (stays for the
   whole scene); `Unit Tests` YELLOW. README(303–308) card (306 lit), which shrinks into the tracker's
   caption; CODE(ci.yml 88–95) (20 pt; lines 90 and 94 soft-wrapped, GREY ↪ marks) with line 90
   YELLOW; then LOG(run1/unit-tests/04: 15, …, 29, crop7) takes its place: `collected 11 items`,
   `11 passed` GREEN.
2. LOG(run1/unit-tests/05: 3, …, 75, 77) (wrap): line 3 GREY, line 75 `INTERNALERROR> PermissionError …`
   RED, line 77 `11 passed` GREEN; badge "exit 3".
3. STEPS(run1/unit-tests: 2–8): job result ✓ lights; a GREY `continue-on-error: true` chip (ci.yml 95)
   rides in onto the coverage row and becomes its note "(continue-on-error: the job stays green)";
   the row holds up `3` and a GREY shunt arc jumps past it. On "Then the upload" the list folds to
   rows 5–8 (room for the log below); a PINK `if: always()` chip (ci.yml 102) rides in onto the
   upload row, a PINK "always" bridge reaches it; LOG(run1/unit-tests/06: 2) `0` under the list and a
   GREY card beside it: "on GitHub: a warning · No files were found … coverage/ · expected, not captured".
4. The README card (307–308) comes back from the tracker with a GREY `erratum` tag. Extra
   LOG(run1/unit-tests/x3: 3, 7) (padding squeezed): line 3 `drwxr-xr-x … root root … .` ORANGE,
   line 7 `uid=1000(app) …` TEAL; a drawing: the runner's `coverage/` folder owned by root (ORANGE),
   mounted into a TEAL container where the user "app" bounces off it (RED ✗); GREY chip
   "fix: exercises.md"; the folder gets a GREEN "writable first" outline.
5. `Integration Tests` YELLOW. README(310–314) (313 lit) → tracker; CODE(tests/integration/
   test_api.py: 7–11) line 11 YELLOW; a TEAL container holding "test client" and "app", a PINK
   arrow staying inside, "one Python process"; "no server · no port"; LOG(run1/integration-tests/04:
   15, …, 28): `10 passed, 1 warning` GREEN.
6. `System Tests` YELLOW. README(316–323) → tracker. V7 SystemTestRig (one BLUE runner, bottom);
   CODE(ci.yml 146–148) above it, line 148 YELLOW; the TEAL `api-server` container comes up
   (`-d`, then `-p 9000:9000` → the ORANGE door 9000; the `-e DEV=1` chip moves into the container);
   "exit 0" from LOG 04 on the line. Extra LOG(run1/system-tests/x3: 2–3, PORTS and NAMES columns)
   with `0.0.0.0:9000->9000/tcp` PINK.
7. CODE(ci.yml 150–154): `sleep 10` → the hourglass empties; line 154 → the PINK `curl -f` arrow
   knocks on the door, ✓; LOG(run1/system-tests/05: 4, 8) line 8 GREEN; the next gate (a GREY gate
   where the tests will run) opens GREEN.
8. CODE(ci.yml 156–158) (line 158 soft-wrapped): a second TEAL container `tests` with its own
   bubble; `--network host` dissolves the bubble, the PINK `localhost:9000` arrow reaches the door;
   README chip "Network Modes" lands there; LOG(run1/system-tests/06: 15, …, 23): `5 passed` GREEN.
9. The rig goes. CODE(ci.yml 160–169), lines 161 and 166 `if: always()` PINK; LOG(run1/system-tests/
   07: 3, 9, 10–15, addresses cropped): `Running in DEV mode`, `Application startup complete.`,
   then the six requests arrive one by one (PINK dots), labelled GREY "curl", "skipif probe",
   "tests"; LOG(08: 3–4) `api-server` twice while a TEAL `api-server` chip fades; the code panel
   returns and the README chip "Conditional Execution" lands on the two `always` lines.
10. Centre: L09's trapdoor (`skipif`, dashed hatch, dashed "L09" chip): a GREY test drops through
   quietly, the hatch is drawn shut; beside it the `curl -f` gate glows and shuts RED with
   "exit 1". GREY caption "in CI: a missing server fails loudly". Fade; empty frame.

pytest's '=====' padding around a summary line is stripped for the panels (as L09 S03/S07 did);
the words are the capture's.
"""

import copy

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.components import person_icon
from explainer.devops import folder_glyph
from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S10"]

# ------------------------------------------------------------------ the real sources (checked)
CI = ".github/workflows/ci.yml"
TAPI = "tests/integration/test_api.py"
assert excerpt(CI, 88, 88).strip() == "- name: Run unit tests"
assert excerpt(CI, 90, 90).strip() == \
    "docker run --rm cheese-app-api:${{ github.sha }} pytest tests/unit/ -v --tb=short"
assert excerpt(CI, 92, 92).strip() == "- name: Generate coverage report"
assert excerpt(CI, 95, 95).strip() == "continue-on-error: true"
assert excerpt(CI, 97, 97).strip() == "- name: Upload coverage report"
assert excerpt(CI, 101, 101).strip() == "path: coverage/"
assert excerpt(CI, 102, 102).strip() == "if: always()"
assert excerpt(CI, 148, 148).strip() == \
    "docker run -d --name api-server -p 9000:9000 -e DEV=1 cheese-app-api:${{ github.sha }}"
assert excerpt(CI, 153, 153).strip() == "sleep 10"
assert excerpt(CI, 154, 154).strip() == "curl -f http://localhost:9000/ || exit 1"
assert excerpt(CI, 158, 158).strip() == \
    "docker run --rm --network host cheese-app-api:${{ github.sha }} pytest tests/system/ -v --tb=short"
assert excerpt(CI, 161, 161).strip() == "if: always()" and excerpt(CI, 166, 166).strip() == "if: always()"
assert excerpt(CI, 163, 163).strip() == "docker logs api-server"
assert excerpt(TAPI, 11, 11) == "client = TestClient(app)"
assert excerpt(TAPI, 8, 8) == "from fastapi.testclient import TestClient"
assert "Runs unit tests in isolation" in readme(306)
assert "terminal, XML, and HTML" in readme(307) and "Uploads coverage report" in readme(308)
assert "TestClient" in readme(313)
assert "--network host" in readme(321)
assert readme(338).startswith("**Conditional Execution**") and readme(342).startswith("**Network Modes**")


def summary(s: str) -> str:
    """A pytest summary line without its '=' padding (L09 S03 / S07 do the same)."""
    assert s.startswith("=") and s.endswith("="), s
    return s.strip("= ")


def retext(name: str, edits: dict):
    """The capture with some FILE lines passed through a function (padding only: the words stay)."""
    c = capture(name)
    c2 = copy.copy(c)
    raw = list(c.raw)
    for n, f in edits.items():
        raw[n - 1] = f(raw[n - 1])
    c2.raw = raw
    return c2


U04 = retext("run1/unit-tests/04", {29: summary})
assert U04.line(15) == "collecting ... collected 11 items" and U04.line(29).startswith("11 passed")
assert U04.exit == 0
U05 = retext("run1/unit-tests/05", {77: summary})
assert U05.line(3).startswith("Executing command: pytest tests/unit/ --cov=api")
assert U05.line(75) == "INTERNALERROR> PermissionError: [Errno 13] Permission denied: 'coverage/style_cb_4667309f.css'"
assert U05.line(77).startswith("11 passed") and U05.exit == 3
U06 = capture("run1/unit-tests/06")
assert U06.line(2) == "0" and U06.exit == 0
UX3 = retext("run1/unit-tests/x3", {3: squeeze_spaces})
assert UX3.line(3).startswith("drwxr-xr-x") and " root  root " in UX3.line(3) and UX3.line(3).endswith(" .")
assert UX3.line(7) == "uid=1000(app) gid=1000(app) groups=1000(app)"
ST = steps("run1", "unit-tests")
assert [(s.n, s.state) for s in ST] == [(2, "success"), (3, "success"), (4, "success"), (5, "success"),
                                         (6, "failure"), (7, "success")], ST
assert job_result("run1", "unit-tests") == "success"
I04 = retext("run1/integration-tests/04", {28: summary})
assert I04.line(15) == "collecting ... collected 10 items" and I04.line(28).startswith("10 passed, 1 warning")
S04 = capture("run1/system-tests/04")
assert S04.exit == 0
SX3 = capture("run1/system-tests/x3")
PS = cols(SX3.at(2, 3), ["PORTS", "NAMES"])
assert PS[1].startswith("0.0.0.0:9000->9000/tcp") and PS[1].endswith("api-server"), PS


SX3c = copy.copy(SX3)          # x3's table, only the PORTS and NAMES columns (cols(), as act -l is shown)
SX3c.raw = [SX3.raw[0], PS[0], PS[1]]
S05 = capture("run1/system-tests/05")
assert S05.line(4) == "Waiting for server to start..."
assert S05.line(8) == '{"message":"Welcome to the Cheese App CI/CD Tutorial!"}', S05.line(8)
S06 = retext("run1/system-tests/06", {23: summary})
assert S06.line(15) == "collecting ... collected 5 items" and S06.line(23).startswith("5 passed")
S07 = capture("run1/system-tests/07")
assert S07.line(3) == "Running in DEV mode" and S07.line(9).endswith("Application startup complete.")
assert '"GET / HTTP/1.1" 200 OK' in S07.line(10) and '"GET /health' in S07.line(11)
assert "x=3&y=4" in S07.line(15)
S08 = capture("run1/system-tests/08")
assert S08.at((3, 4)) == ["api-server", "api-server"]

LOG_TOP = 2.05               # Part 2 pictures stay below PIC_TOP2 (2.15)
LEFT_X = -6.45
LIST_X = -5.45               # step lists: room on their left for the shunt arc and the 'always' bridge
BAND_BOTTOM = -0.55          # system beats: panels above, the rig below
RIG_H = 2.9
RIG_C = np.array([0.0, -3.55 + RIG_H / 2, 0])

LEVELS = (("Unit Tests", PASS), ("Integration Tests", IMAGE), ("System Tests", GITHUB))


def top_at(m, y: float = LOG_TOP, x: float | None = None, left: float | None = None):
    """Place m with its top edge at y, centred on x or with its left edge at `left`."""
    if left is not None:
        x = left + m.width / 2
    return m.move_to([0.0 if x is None else x, y - m.height / 2, 0])


def wrapped_code(path: str, a: int, b: int, folds: dict, size: float = 20) -> VGroup:
    """CODE(path: a–b) with long lines soft-wrapped, as an editor shows them (S09's helper): folds =
    {file line: [break after these substrings]}. Continuation rows are indented two columns deeper
    and marked with a GREY '↪'; every character is the file's. .code .header .rows .src_rows"""
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
            marks.add(label("↪", 20, S.GREY).next_to(c.code_lines[k], LEFT, buff=0.18))
    g = VGroup(c, head, marks)
    g.code, g.header, g.rows, g.src_rows = c, head, rows, src_rows
    return g


def span(panel, n: int, sub: str):
    """Glyphs of `sub` in file line n of a wrapped_code panel (searched row by row)."""
    for k in panel.rows[n]:
        if sub in panel.src_rows[k]:
            return code_span(panel.code, k, sub)
    raise ValueError(f"{sub!r} not in line {n}")


def row_bar(panel, n: int, color, opacity: float = 0.22):
    """A translucent bar over every row of file line n of a wrapped_code panel."""
    return VGroup(*[line_bar(panel.code, k, color, opacity) for k in panel.rows[n]])


def level_box(name: str, edge, box_w: float, box_h: float, size: float, lit: bool = False) -> VGroup:
    fr = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.1, stroke_color=edge, stroke_width=3)
    fr.set_fill(TURN if lit else S.BG, 0.3 if lit else 1)
    t = label(name, size, INK).move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def ladder(lit: int | None = None) -> VGroup:
    """The three test jobs as a small staircase right of the strip (unit lowest)."""
    g = VGroup()
    for i, (name, edge) in enumerate(LEVELS):
        b = level_box(name, edge, 2.4, 0.36, 20, lit == i)
        b.move_to([4.8 + 0.25 * i, 2.38 + 0.42 * i, 0])
        g.add(b)
    return g


def light_level(lad: VGroup, k: int):
    """ANIM: level k fills YELLOW, the others go dark (whole boxes: the text stays on top)."""
    tgt = ladder(k)
    return AnimationGroup(*[Transform(lad[i], tgt[i]) for i in range(3)])


class CompactRig(SystemTestRig):
    """V7 in a 2.9-tall runner: server_up puts the '-e DEV=1' chip inside the api-server container
    (under its name), where the shared layout's chip below the box would leave the runner."""

    def server_up(self, scene):
        c = self.runner.get_center()
        sv = self._container("api-server").move_to(c + np.array([-self.rig_w * 0.3, -0.35, 0]))
        sv.text.shift(UP * 0.25)
        dev = grey_chip("-e DEV=1", mono_font=True).move_to(sv.frame.get_center() + DOWN * 0.27)
        door = door_glyph("9000", SHARED, 0.8).move_to(sv.frame.get_right() + RIGHT * 0.3)
        door.shift(DOWN * (door.frame.get_center()[1] - sv.get_center()[1]))
        scene.play(FadeIn(sv, scale=0.9), run_time=0.5)
        scene.play(FadeIn(door, shift=LEFT * 0.2), run_time=0.4)
        self.server, self.door, self.dev = sv, door, dev
        self.keep(scene, sv, door)

    def env_in(self, scene):
        """The '-e DEV=1' chip drops into the container."""
        scene.play(FadeIn(self.dev, shift=DOWN * 0.3), run_time=0.5)
        self.keep(scene, self.dev)


class TestJobs(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S10"] == 11, len(SAY)

        # ========================================================== 0. one test box, three altitudes
        tr = tracker_p5(8)
        strip = pipeline_strip("Lint and Format")
        ref = lref("27")
        big = VGroup()
        for i, (name, edge) in enumerate(LEVELS):
            b = level_box(name, edge, 3.7, 0.9, 26)
            b.move_to([-2.9 + 3.3 * i, -2.3 + 1.35 * i, 0])
            big.add(b)
        ground = DashedLine([-5.4, -2.95, 0], [5.4, -2.95, 0], dash_length=0.12, color=S.GREY_DARK)
        alt = Arrow([-5.9, -2.8, 0], [-5.9, 0.9, 0], buff=0, color=S.GREY, stroke_width=3, tip_length=0.2)
        alt_t = label("closer to the real thing", 22, S.GREY).next_to(alt, UP, buff=0.15).align_to(alt, LEFT)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(strip, shift=RIGHT * 0.3), run_time=0.6)
            vo.wait_until("Now the tests")
            self.play(strip.set_current("Test"), run_time=0.6)
            self.add(strip)
            vo.wait_until("The lecture's one test box")
            self.play(FadeIn(ref), Indicate(strip.boxes[3], color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("is three jobs here")
            self.play(LaggedStart(*[AnimationGroup(TransformFromCopy(strip.boxes[3].frame, big[i].frame),
                                                   FadeIn(big[i].text, run_time=0.9)) for i in range(3)],
                                  lag_ratio=0.25), run_time=1.4)
            self.remove(*big)
            self.add(big)
            vo.wait_until("side by side")
            self.play(Create(ground), LaggedStart(*[Indicate(b.text, color=INK, scale_factor=1.08) for b in big],
                                                  lag_ratio=0.2), run_time=0.9)
            vo.wait_until("each at a different altitude")
            self.play(GrowArrow(alt), FadeIn(alt_t, shift=UP * 0.15), run_time=0.8)
            self.play(LaggedStart(*[Circumscribe(b, color=b.frame.get_stroke_color(), buff=0.08) for b in big],
                                  lag_ratio=0.3), run_time=1.2)

        # ========================================================== 1. unit tests: one function at a time
        lad = ladder()
        card = top_at(readme_panel(303, 308), left=LEFT_X)
        cp = wrapped_code(CI, 88, 95, {90: ["${{ github.sha }}"],
                                       94: ["-v", "/app/coverage", "tests/unit/", "--cov-report=xml"]})
        assert cp.width <= 12.6 and cp.height <= LOG_TOP + 3.55, (cp.width, cp.height)
        top_at(cp, LOG_TOP, left=LEFT_X)
        log4 = top_at(run_log(U04, (15, "…", 29), colors={29: PASS}), left=LEFT_X)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(ref), FadeOut(VGroup(ground, alt, alt_t)),
                      *[ReplacementTransform(big[i], lad[i]) for i in range(3)], run_time=0.9)
            self.add(lad)
            self.play(light_level(lad, 0), FadeIn(card, shift=DOWN * 0.15), run_time=0.6)
            self.add(lad)
            vo.wait_until("one function at a time")
            hb = hl_bar(card.rows[306], PASS, 0.22)
            self.play(FadeIn(hb), Indicate(card.rows[306], color=INK, scale_factor=1.03), run_time=0.7)
            vo.wait_until("with no outside dependencies")
            cap_copy = tr.caption.copy()
            self.play(ReplacementTransform(VGroup(card, hb), cap_copy), FadeIn(cp, shift=UP * 0.15), run_time=0.7)
            self.remove(cap_copy, card, hb)
            self.add(tr)
            b90 = row_bar(cp, 90, TURN, 0.22)
            self.play(FadeIn(b90), span(cp, 90, "tests/unit/").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("The log collects 11 tests")
            self.play(FadeOut(VGroup(cp, b90), shift=UP * 0.15), FadeIn(log4, shift=UP * 0.15), run_time=0.6)
            self.remove(cp, b90)
            self.play(Indicate(log4.row(15), color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("and 11 pass")
            self.play(Indicate(log4.row(29), color=PASS, scale_factor=1.1), run_time=0.7)

        # ========================================================== 2. the coverage run: 11 pass, exit 3
        log5 = top_at(run_log(U05, (3, "…", 75, 77), colors={3: S.GREY, 75: ERR, 77: PASS}, wrap=True),
                      left=LEFT_X)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(log4, shift=LEFT * 0.2), FadeIn(log5, shift=LEFT * 0.2), run_time=0.6)
            self.remove(log4)
            vo.wait_until("Then the coverage step runs them again")
            self.play(Indicate(log5.heading, color=INK, scale_factor=1.04), run_time=0.7)
            vo.wait_until("and all 11 pass again")
            self.play(Indicate(log5.row(77), color=PASS, scale_factor=1.1), run_time=0.7)
            vo.wait_until("But pytest hits an internal error")
            r75 = VGroup(*[r for r in log5.rows if log5.rows.submobjects.index(r) >=
                           log5.rows.submobjects.index(log5.row(75)) and r is not log5.row(77)])
            hb75 = hl_bar(r75, ERR, 0.2)
            self.play(FadeIn(hb75), run_time=0.4)
            vo.wait_until("permission denied")
            pd = substring(log5.row(75), "PermissionError")
            self.play(Indicate(pd, color=ERR, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Exit code 3")
            self.play(Circumscribe(log5.badge, color=ERR, buff=0.06), run_time=0.7)

        # ========================================================== 3. green anyway: the shunt and the always bridge
        sl = top_at(steps_list("run1", "unit-tests", ((2, 8),)), y=LOG_TOP + 0.05, left=LIST_X)
        sl2 = top_at(steps_list("run1", "unit-tests", ((5, 8),)), y=LOG_TOP + 0.05, left=LIST_X)
        note = sl.notes[6]
        sl.row(6).remove(note)
        c95 = grey_chip("continue-on-error: true", size=20, mono_font=True)
        c95.move_to([6.4 - c95.width / 2, -3.2, 0])
        c102 = route_chip("if: always()", size=20)
        log6 = run_log(U06, (2,))
        warn = VGroup(
            VGroup(warning_sign(0.32, TURN), label("on GitHub: a warning", 20, INK)).arrange(RIGHT, buff=0.15),
            mono("No files were found", 20, S.GREY), mono("… coverage/", 20, S.GREY),
            expected_tag("not captured"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        warn_fr = box(warn.width + 0.5, warn.height + 0.4, S.GREY, fill=S.BG, fill_opacity=1)
        warn_card = VGroup(warn_fr, warn)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(log5, hb75)), FadeIn(sl, shift=LEFT * 0.2), run_time=0.6)
            self.remove(log5, hb75)
            vo.wait_until("Yet the job is green")
            self.play(Indicate(sl.row(8), color=PASS, scale_factor=1.08), run_time=0.7)
            vo.wait_until("The step says continue on error")
            self.play(FadeIn(c95, shift=LEFT * 0.3), run_time=0.4)
            self.play(c95.animate.move_to(note), run_time=0.7)
            self.play(ReplacementTransform(c95, note), run_time=0.5)
            self.remove(note)
            sl.row(6).add(note)
            self.add(sl)
            vo.wait_until("so the failure is shunted aside")
            c3 = sl.code_chip(6, 3)
            arc = sl.shunt_arc(6)
            self.play(FadeIn(c3, scale=1.3), run_time=0.4)
            self.play(Create(arc), Indicate(sl.row(6).mark, color=ERR, scale_factor=1.3), run_time=0.8)
            vo.wait_until("Then the upload")
            dy = sl2.row(6).get_center()[1] - sl.row(6).get_center()[1]
            self.play(ReplacementTransform(sl, sl2), c3.animate.shift(UP * dy), arc.animate.shift(UP * dy),
                      run_time=0.8)
            self.add(sl2)
            vo.wait_until("marked if always")
            c102.next_to(sl2.row(7), RIGHT, buff=0.35)
            start = c102.copy().move_to([6.4 - c102.width / 2, c102.get_center()[1], 0])
            self.play(FadeIn(start, shift=LEFT * 0.3), run_time=0.3)
            self.play(ReplacementTransform(start, c102), run_time=0.6)
            br = sl2.bridge(6, 7)
            self.play(Create(br[0]), FadeIn(br[1]), run_time=0.6)
            vo.wait_until("finds no files")
            log6.next_to(sl2, DOWN, buff=0.08).align_to(sl2, LEFT)
            assert log6.get_bottom()[1] >= -3.6, log6.get_bottom()
            self.play(FadeIn(log6, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(log6.row(2), color=TURN, scale_factor=1.5), run_time=0.6)
            vo.wait_until("on GitHub, a yellow warning says so")
            warn_card.next_to(log6, RIGHT, buff=0.25).align_to(log6, UP)
            assert warn_card.get_right()[0] <= 6.55, warn_card.get_right()
            self.play(FadeIn(warn_card, shift=LEFT * 0.2), run_time=0.5)
            self.play(Indicate(warn[0][0], color=TURN, scale_factor=1.3), run_time=0.6)

        # ========================================================== 4. the README's small gap: root owns coverage/
        card4 = top_at(readme_panel(303, 308, lines=[307, 308]), left=LEFT_X)
        err = erratum_tag().next_to(card4, RIGHT, buff=0.25).align_to(card4, UP).shift(DOWN * 0.1)
        x3 = run_log(UX3, (3, 7), title="Unit Tests · extra: who owns coverage/", size=20, max_w=8.7,
                     colors={3: SHARED, 7: IMAGE})
        top_at(x3, -0.05, left=LEFT_X)
        xt = extra_tag().next_to(x3.frame, DOWN, buff=0.12).align_to(x3.frame, LEFT)
        fix = grey_chip("fix: exercises.md", size=22).next_to(xt, RIGHT, buff=0.4)
        # the drawing: the runner's folder, mounted into the container
        dx = x3.get_right()[0] + 0.3
        cx = (dx + 6.45) / 2
        ctn = box(6.45 - dx, 1.75, IMAGE, fill_opacity=0.1, radius=0.12)
        ctn.move_to([cx, -2.5, 0])
        ctn_t = label("test container", 20, IMAGE).next_to(ctn.get_corner(UL), DR, buff=0.12)
        user = person_icon(IMAGE, 0.42)
        user_t = label("app", 20, IMAGE)
        user_g = VGroup(user, user_t).arrange(RIGHT, buff=0.12).move_to(ctn.get_center() + DOWN * 0.25)
        fold = folder_glyph(0.5, SHARED)
        fold_t = mono("coverage/", 20, SHARED)
        own_t = label("owner: root", 20, SHARED)
        fold_g = VGroup(fold, VGroup(fold_t, own_t).arrange(DOWN, aligned_edge=LEFT, buff=0.06)) \
            .arrange(RIGHT, buff=0.2).move_to([cx, -0.6, 0])
        mount = DashedLine(fold.get_bottom() + DOWN * 0.05, ctn.get_top(), dash_length=0.08, color=S.GREY)
        mount_t = mono("-v", 20, S.GREY).next_to(mount, LEFT, buff=0.1)
        x_mark = cross_mark(0.3, ERR).next_to(fold, LEFT, buff=0.2)
        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(sl2, c3, arc, c102, br, log6, warn_card)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            cap_copy = tr.caption.copy()
            self.add(cap_copy)
            self.play(ReplacementTransform(cap_copy, card4), run_time=0.7)
            self.remove(cap_copy)
            self.add(card4, tr)
            vo.wait_until("it promises terminal")
            hb7 = hl_bar(card4.rows[307], S.GREY, 0.3)
            self.play(FadeIn(hb7), FadeIn(err, shift=LEFT * 0.2), run_time=0.5)
            self.play(Circumscribe(err, color=INK, buff=0.06), run_time=0.6)
            vo.wait_until("Docker creates the missing coverage folder")
            self.play(FadeIn(x3, shift=UP * 0.15), FadeIn(xt), FadeIn(ctn), FadeIn(ctn_t), run_time=0.6)
            self.play(FadeIn(fold_g, shift=DOWN * 0.15), Create(mount), FadeIn(mount_t), run_time=0.6)
            vo.wait_until("as root")
            self.play(Indicate(x3.row(3), color=SHARED, scale_factor=1.05), Indicate(own_t, color=SHARED),
                      run_time=0.8)
            vo.wait_until("and the container's user, app")
            self.play(FadeIn(user_g, scale=0.9), Indicate(x3.row(7), color=IMAGE, scale_factor=1.05), run_time=0.7)
            vo.wait_until("can't write into it")
            self.play(bounce(user_g, fold.get_bottom() + DOWN * 0.45, run_time=1.0))
            self.play(FadeIn(x_mark, scale=1.4), Indicate(fold, color=ERR), run_time=0.5)
            vo.wait_until("Create the folder writable first")
            ok_ring = ring(fold, PASS, buff=0.1, dashed=True)
            ok_t = label("writable first", 20, PASS).next_to(fold_g, UP, buff=0.3)
            self.play(FadeOut(x_mark), Create(ok_ring), FadeIn(ok_t, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("the exercises have the fix")
            self.play(FadeIn(fix, shift=LEFT * 0.2), run_time=0.5)
            self.play(Circumscribe(fix, color=INK, buff=0.06), run_time=0.6)

        # ========================================================== 5. integration: the test client, in-process
        card5 = top_at(readme_panel(310, 314), left=LEFT_X)
        tp = top_at(code(TAPI, 7, 11, font_size=20), left=LEFT_X)
        ctn5 = box(4.4, 1.8, IMAGE, fill_opacity=0.08, radius=0.14)
        ctn5.move_to([4.25, 1.1, 0])
        ctn5_t = label("one Python process", 20, IMAGE).next_to(ctn5.get_corner(UL), DR, buff=0.12)
        client = level_box("test client", TOOL, 1.7, 0.75, 22)
        app_b = level_box("app", INK, 1.2, 0.75, 22)
        VGroup(client, app_b).arrange(RIGHT, buff=0.9).move_to(ctn5.get_center() + DOWN * 0.25)
        call = route(client.get_right(), app_b.get_left(), arc=-0.6)
        noport = label("no server · no port", 22, S.GREY).next_to(ctn5, DOWN, buff=0.2)
        log_i = run_log(I04, (15, "…", 28), colors={28: PASS})
        log_i.move_to([LEFT_X + log_i.width / 2, -3.55 + log_i.height / 2, 0])
        assert log_i.get_top()[1] < tp.get_bottom()[1] - 0.05 and log_i.get_top()[1] < noport.get_bottom()[1], \
            (log_i.get_top(), tp.get_bottom(), noport.get_bottom())
        with self.voiceover(SAY[5]) as vo:
            gone = VGroup(card4, hb7, err, x3, xt, fix, ctn, ctn_t, user_g, fold_g, mount, mount_t, ok_ring, ok_t)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            self.play(light_level(lad, 1), FadeIn(card5, shift=DOWN * 0.15), run_time=0.6)
            self.add(lad)
            vo.wait_until("use the FastAPI test client")
            hb13 = hl_bar(card5.rows[313], IMAGE, 0.22)
            self.play(FadeIn(hb13), run_time=0.4)
            cap_copy = tr.caption.copy()
            self.play(ReplacementTransform(VGroup(card5, hb13), cap_copy), FadeIn(tp, shift=UP * 0.15), run_time=0.7)
            self.remove(cap_copy, card5, hb13)
            self.add(tr)
            b11 = line_bar(tp.code, 4, TURN, 0.22)
            self.play(FadeIn(b11), code_span(tp.code, 4, "TestClient(app)").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("the app is called inside the same Python process")
            self.play(FadeIn(ctn5), FadeIn(ctn5_t), FadeIn(client, shift=RIGHT * 0.2), FadeIn(app_b, shift=LEFT * 0.2),
                      run_time=0.6)
            self.play(GrowArrow(call), run_time=0.6)
            pdot = Dot(radius=0.08, color=ROUTE).move_to(call.get_start())
            self.play(MoveAlongPath(pdot, call), run_time=0.8)
            self.play(FadeOut(pdot), Circumscribe(app_b, color=ROUTE, buff=0.08), run_time=0.5)
            self.remove(pdot)
            vo.wait_until("No server, no port")
            self.play(FadeIn(noport, shift=UP * 0.15), FadeIn(log_i, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("10 passed")
            self.play(Indicate(log_i.row(28), color=PASS, scale_factor=1.1), run_time=0.7)

        # ========================================================== 6. system tests: the real server, port 9000
        card6 = top_at(readme_panel(316, 323), left=LEFT_X)
        rig = CompactRig(rig_w=10.0, rig_h=RIG_H).move_to(RIG_C)
        c1 = wrapped_code(CI, 146, 148, {148: ["-e DEV=1"]})
        top_at(c1, LOG_TOP, left=LEFT_X)
        assert c1.get_bottom()[1] > rig.get_top()[1] + 0.05, (c1.get_bottom(), rig.get_top())
        e0_t = label("this step:", 20, S.GREY)
        e0 = exit_badge(0)
        VGroup(e0_t, e0).arrange(RIGHT, buff=0.15).next_to(c1.header, RIGHT, buff=0.5)
        x3s = run_log(SX3c, (2, 3), title="System Tests · extra: docker ps", colors={2: S.GREY})
        top_at(x3s, LOG_TOP, left=LEFT_X)
        x3s_t = extra_tag().next_to(x3s.frame, RIGHT, buff=0.25).align_to(x3s.frame, UP)
        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(tp, b11, ctn5, ctn5_t, client, app_b, call, noport, log_i)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            self.play(light_level(lad, 2), FadeIn(card6, shift=DOWN * 0.15), run_time=0.6)
            self.add(lad)
            vo.wait_until("need the real thing")
            hb19 = hl_bar(card6.rows[319], GITHUB, 0.22)
            self.play(FadeIn(hb19), Indicate(card6.rows[319], color=INK, scale_factor=1.03), run_time=0.6)
            vo.wait_until("One container starts the server")
            cap_copy = tr.caption.copy()
            self.play(ReplacementTransform(VGroup(card6, hb19), cap_copy), FadeIn(c1, shift=UP * 0.15),
                      FadeIn(rig), run_time=0.7)
            self.remove(cap_copy, card6, hb19)
            self.add(tr)
            b148 = row_bar(c1, 148, TURN, 0.22)
            self.play(FadeIn(b148), run_time=0.3)
            rig.server_up(self)
            vo.wait_until("in the background")
            self.play(span(c1, 148, "-d").animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(span(c1, 148, "-d"), color=TURN, scale_factor=1.4), run_time=0.5)
            vo.wait_until("and publishes port 9000")
            p9 = span(c1, 148, "-p 9000:9000")
            self.play(p9.animate.set_color(SHARED), run_time=0.3)
            self.play(Indicate(p9, color=SHARED, scale_factor=1.12), Indicate(rig.door, color=SHARED), run_time=0.7)
            rig.env_in(self)
            self.play(FadeIn(e0), FadeIn(e0_t), run_time=0.4)
            vo.wait_until("An extra command, docker ps")
            self.play(FadeOut(VGroup(c1, b148, e0, e0_t), shift=UP * 0.15), FadeIn(x3s, shift=UP * 0.15),
                      FadeIn(x3s_t), run_time=0.6)
            self.remove(c1, b148, e0, e0_t)
            vo.wait_until("shows it running")
            self.play(Indicate(substring(x3s.row(3), "api-server"), color=IMAGE, scale_factor=1.12),
                      Indicate(rig.server, color=IMAGE, scale_factor=1.04), run_time=0.8)
            vo.wait_until("with 9000 mapped")
            port = substring(x3s.row(3), "0.0.0.0:9000->9000/tcp")
            self.play(port.animate.set_color(ROUTE), run_time=0.4)
            self.play(Indicate(port, color=ROUTE, scale_factor=1.1), Indicate(rig.door, color=SHARED), run_time=0.7)

        # ========================================================== 7. sleep 10, then curl -f knocks
        c2 = top_at(code(CI, 150, 154, font_size=20), LOG_TOP, left=LEFT_X)
        assert c2.get_bottom()[1] > rig.get_top()[1] + 0.05, c2.get_bottom()
        log05 = top_at(run_log(S05, (4, 8), colors={8: PASS}), LOG_TOP, left=LEFT_X)
        assert log05.get_bottom()[1] > rig.get_top()[1] + 0.02, log05.get_bottom()
        gate = gate_glyph(0.7, 0.8).move_to(rig.runner.get_center() + np.array([3.0, -0.35, 0]))
        gate_t = label("next step", 20, S.GREY).next_to(gate, DOWN, buff=0.12)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(x3s, x3s_t), shift=UP * 0.15), FadeIn(c2, shift=UP * 0.15),
                      FadeIn(gate), FadeIn(gate_t), run_time=0.6)
            self.remove(x3s, x3s_t)
            vo.wait_until("the job waits 10 seconds")
            b153 = line_bar(c2.code, 3, TURN, 0.22)
            self.play(FadeIn(b153), run_time=0.3)
            rig.wait(self, 1.6)
            vo.wait_until("and curl, dash f, knocks")
            b154 = line_bar(c2.code, 4, ROUTE, 0.22)
            rig.drop(self, rig.hour, run_time=0.3)
            self.play(FadeOut(b153), FadeIn(b154), code_span(c2.code, 4, "curl -f").animate.set_color(ROUTE),
                      run_time=0.4)
            vo.wait_until("on localhost 9000")
            rig.knock(self, ok=True)
            vo.wait_until("Only when the welcome message comes back")
            self.play(FadeOut(VGroup(c2, b154), shift=UP * 0.15), FadeIn(log05, shift=UP * 0.15), run_time=0.6)
            self.remove(c2, b154)
            self.play(Indicate(log05.row(8), color=PASS, scale_factor=1.05), run_time=0.7)
            vo.wait_until("does the next gate open")
            self.play(Transform(gate.bar, gate.bar.copy().rotate(PI / 2.4, about_point=gate.bar.get_start())
                                .set_color(PASS)), gate.posts.animate.set_color(PASS), run_time=0.6)

        # ========================================================== 8. the tests' container, on the host network
        c3p = wrapped_code(CI, 156, 158, {158: ["--network host", "${{ github.sha }}"]})
        top_at(c3p, LOG_TOP, left=LEFT_X)
        assert c3p.get_bottom()[1] > rig.get_top()[1] + 0.02, c3p.get_bottom()
        log06 = top_at(run_log(S06, (15, "…", 23), colors={23: PASS}, heading=False), LOG_TOP, left=LEFT_X)
        assert log06.get_bottom()[1] > rig.get_top()[1] + 0.02, log06.get_bottom()
        nm = grey_chip("Network Modes", size=20)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(log05, shift=UP * 0.15), FadeIn(c3p, shift=UP * 0.15),
                      FadeOut(VGroup(gate, gate_t)), run_time=0.6)
            self.remove(log05, gate, gate_t)
            vo.wait_until("A second container runs the tests")
            b158 = row_bar(c3p, 158, TURN, 0.2)
            self.play(FadeIn(b158), run_time=0.3)
            rig.tests_up(self)
            vo.wait_until("with network host")
            nh = span(c3p, 158, "--network host")
            self.play(nh.animate.set_color(ROUTE), run_time=0.3)
            self.play(Indicate(nh, color=ROUTE, scale_factor=1.12), run_time=0.5)
            rig.host_net(self)
            vo.wait_until("it shares the runner's network")
            nm.move_to(rig.tests.get_center() + DOWN * 0.95)
            if nm.get_bottom()[1] < rig.runner.get_bottom()[1] + 0.05:
                nm.shift(UP * (rig.runner.get_bottom()[1] + 0.05 - nm.get_bottom()[1]))
            nm_start = nm.copy().move_to([6.3 - nm.width / 2, LOG_TOP - 0.3, 0])
            self.play(FadeIn(nm_start, shift=LEFT * 0.2), run_time=0.3)
            self.play(ReplacementTransform(nm_start, nm), Indicate(rig.runner, color=GITHUB, scale_factor=1.01),
                      run_time=0.8)
            vo.wait_until("so localhost 9000 reaches the server")
            self.play(Indicate(rig.net, color=ROUTE, scale_factor=1.05), Indicate(rig.door, color=SHARED),
                      run_time=0.8)
            self.play(FadeOut(VGroup(c3p, b158), shift=UP * 0.15), FadeIn(log06, shift=UP * 0.15), run_time=0.5)
            self.remove(c3p, b158)
            vo.wait_until("5 passed")
            self.play(Indicate(log06.row(23), color=PASS, scale_factor=1.1), run_time=0.7)

        # ========================================================== 9. if: always(): the server log, then cleanup
        c4 = top_at(code(CI, 160, 169), LOG_TOP, x=-1.2)
        a161 = line_bar(c4.code, 1, ROUTE, 0.25)
        a166 = line_bar(c4.code, 6, ROUTE, 0.25)
        log07 = top_at(run_log(S07, (3, 9, (10, 15))), LOG_TOP, left=LEFT_X)
        assert log07.get_bottom()[1] > -3.55, log07.get_bottom()
        arrive = [log07.row(n) for n in range(10, 16)]
        saved = [r.copy() for r in arrive]
        for r in arrive:
            r.set_opacity(0)
        whos = {10: "curl", 11: "skipif probe", 12: "tests"}
        who_t = {n: label(s, 20, S.GREY).next_to(log07.row(n), RIGHT, buff=0.4) for n, s in whos.items()}
        tick = Line(log07.row(12).get_corner(UL) + LEFT * 0.14 + UP * 0.02,
                    log07.row(15).get_corner(DL) + LEFT * 0.14 + DOWN * 0.02, color=S.GREY, stroke_width=3)
        log08 = top_at(run_log(S08, ((3, 4),)), LOG_TOP, left=LEFT_X)
        srv = image_chip("api-server", size=22).next_to(log08, RIGHT, buff=0.6)
        ce = grey_chip("Conditional Execution", size=22)
        ce.move_to([c4.get_right()[0] + 0.4 + ce.width / 2, (a161.get_center()[1] + a166.get_center()[1]) / 2, 0])
        assert ce.get_right()[0] <= 6.5, ce.get_right()
        ce_arrows = VGroup(arrow(ce.get_left(), a161.get_right() + LEFT * 0.05, color=ROUTE),
                           arrow(ce.get_left(), a166.get_right() + LEFT * 0.05, color=ROUTE))
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(rig, log06, nm)), run_time=0.5)
            self.remove(rig, log06, nm, *rig.get_family())
            self.play(FadeIn(c4, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Two steps marked if always")
            self.play(FadeIn(a161), FadeIn(a166), code_span(c4.code, 1, "if: always()").animate.set_color(ROUTE),
                      code_span(c4.code, 6, "if: always()").animate.set_color(ROUTE), run_time=0.6)
            vo.wait_until("even after a failure")
            self.play(Indicate(VGroup(code_span(c4.code, 1, "if: always()"), code_span(c4.code, 6, "if: always()")),
                               color=ROUTE, scale_factor=1.1), run_time=0.7)
            vo.wait_until("show the server log")
            self.play(FadeOut(VGroup(c4, a161, a166), shift=UP * 0.15), FadeIn(log07, shift=UP * 0.15), run_time=0.6)
            self.remove(c4, a161, a166)
            vo.wait_until("where every test request arrives")
            for n, r, s in zip(range(10, 16), arrive, saved):
                d = Dot(radius=0.08, color=ROUTE).move_to([log07.frame.get_right()[0] - 0.25, r.get_center()[1], 0])
                anims = [Transform(r, s)]
                if n in who_t:
                    anims.append(FadeIn(who_t[n], shift=LEFT * 0.1))
                if n == 12:
                    anims.append(Create(tick))
                self.play(FadeIn(d, scale=1.5), run_time=0.12)
                self.play(d.animate.move_to([r.get_left()[0] - 0.14, r.get_center()[1], 0]), *anims, run_time=0.38)
                self.play(FadeOut(d), run_time=0.08)
                self.remove(d)
            vo.wait_until("then stop and remove the container")
            hold = VGroup(log07, *who_t.values(), tick)
            self.play(FadeOut(hold, shift=UP * 0.15), FadeIn(log08, shift=UP * 0.15), FadeIn(srv), run_time=0.6)
            self.remove(hold, *hold.get_family())
            self.play(Indicate(log08.rows, color=IMAGE, scale_factor=1.06), run_time=0.5)
            self.play(srv.animate.set_opacity(0.15), run_time=0.6)
            vo.wait_until("That's the README's conditional execution")
            self.play(FadeOut(VGroup(log08, srv), shift=UP * 0.15), FadeIn(VGroup(c4, a161, a166), shift=UP * 0.15),
                      run_time=0.6)
            self.remove(log08, srv)
            ce_start = ce.copy().move_to([6.3 - ce.width / 2, -3.0, 0])
            self.play(FadeIn(ce_start, shift=LEFT * 0.2), run_time=0.3)
            self.play(ReplacementTransform(ce_start, ce), run_time=0.6)
            self.play(LaggedStart(*[GrowArrow(a) for a in ce_arrows], lag_ratio=0.3), run_time=0.7)

        # ========================================================== 10. L09's quiet skip vs CI's loud gate
        td = CompactRig().trapdoor().scale(1.6)
        td.move_to([-2.8, 0.3, 0])
        l09 = dashed_chip("L09", size=22).next_to(td, LEFT, buff=0.5)
        td_t = label("skips quietly", 24, S.GREY).next_to(td, DOWN, buff=1.1)
        tdot = Dot(radius=0.14, color=S.GREY).move_to(td[0].get_top() + UP * 1.0)
        cg = gate_glyph(1.3, 1.5, ROUTE).move_to([2.6, 0.3, 0])
        cg_t = mono("curl -f", 26, ROUTE).next_to(cg, UP, buff=0.25)
        e1 = exit_badge(1, size=22).next_to(cg, RIGHT, buff=0.4)
        capt = label("in CI: a missing server fails loudly", 28, S.GREY).move_to([0, -2.2, 0])
        with self.voiceover(SAY[10]) as vo:
            gone = VGroup(c4, a161, a166, ce, ce_arrows)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            vo.wait_until("In lecture 9")
            self.play(FadeIn(td), FadeIn(l09), run_time=0.6)
            vo.wait_until("a missing server made these tests skip quietly")
            self.play(FadeIn(tdot), run_time=0.3)
            hinge = td[1].get_center()
            self.play(Rotate(td[0], -PI / 3, about_point=hinge), run_time=0.4)
            self.play(tdot.animate.shift(DOWN * 1.4).set_opacity(0), run_time=0.8)
            self.remove(tdot)
            self.play(Rotate(td[0], PI / 3, about_point=hinge), FadeIn(td_t, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Here the curl gate")
            self.play(FadeIn(cg), FadeIn(cg_t), run_time=0.5)
            self.play(Indicate(VGroup(cg, cg_t), color=ROUTE, scale_factor=1.1), run_time=0.7)
            vo.wait_until("makes it fail loudly instead")
            self.play(cg.bar.animate.set_color(ERR), cg.posts.animate.set_color(ERR), FadeIn(e1, shift=LEFT * 0.2),
                      run_time=0.5)
            self.play(FadeIn(capt, shift=UP * 0.15), Circumscribe(e1, color=ERR, buff=0.06), run_time=0.7)

        self.wait(0.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
