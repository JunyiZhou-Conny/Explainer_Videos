"""S13 · The local conundrum: --no-verify (AC215 L21). TRACKER P5 8 · extra, STRIP Lint and Format.
Lecture: 21 · slides 29–31 (beats 0–6), 21 · slide 11 (beat 11). Set pieces V1 HookChain, V4 JobGraph.

Beats (script.md "## S13", one voiceover block each):
0. TRACKER P5 8 · extra; the Part 2 strip with `Lint and Format` current. LECTURE 21 · 29–31. A GREY
   title chip "The local conundrum"; under it V1 (GREY laptop frame, three gates; a GREEN commit dot
   passes them) and a BLUE server "GitHub" holding a `Check Code` box, joined by a YELLOW arc
   "why twice?".
1. The picture leaves; a 10-row `laptop` terminal types line 1 of `laptop/40` (extra; folds onto
   four rows, GREY `extra` beside the last) → TERM(laptop/40: 10–11): line 10 RED, line 11 GREEN
   with its squeezed text YELLOW-highlighted. The tracker caption flashes on "extras".
2. `git add .` → (no output); `git commit -m "quick fix"` → TERM(laptop/42: 9–11, 13) (line 9
   `…Failed` RED, dot leader shortened to fit; line 13 `reformatted …service.py` YELLOW). The
   terminal shrinks to a 3-row strip; V1 small in the middle: the commit dot stops RED at Black.
3. V1 leaves. `git status --short` → TERM(laptop/43: 2) `MM src/api-service/api/service.py`; the
   two M's fly up to two file icons: "staged: messy" (RED, the squeezed line) and "working copy:
   reformatted" (GREEN, the spaced line).
4. The icons leave; the terminal grows to 5 rows: `git commit --no-verify -m "quick fix"` (extra;
   folds; `--no-verify` RED) → TERM(laptop/44: 2–3); it shrinks to a 3-row strip and V1 comes
   back: a RED bypass arc swings over all three gates and the dot rides it; RED `--no-verify` chip.
5. The BLUE server returns on the right; `git push` → TERM(laptop/45: 3); the dot flies into the
   server. V1 and the strip leave; the server becomes GRAPH(run3) (short labels, compact), which
   colors from `runner/run3/results.txt`: lint ✗ RED, the tests ✓, summary ✓, run badge ✗; LOG(
   run3/lint-and-format/04: 4, 6–7) along the bottom (line 4 RED; badge "exit 1").
6. The log becomes LOG(run3/lint-and-format/x4: 4–6) (title "Lint and Format Check · extra:
   Flake8, if it had run", GREY `extra` tag); its three rows flash RED. The graph turns back into
   the BLUE server, whose `Check Code` box flashes RED with a RED chip "caught".
7. LECTURE off. Server and log leave. A 5-row terminal: `git status --short` → TERM(laptop/48: 2);
   `git restore src/api-service/api/service.py && git status --short` (folds) → (no output). Above
   it a GREY code card headed "pushed it too?" (RED ✗ "main") with the four commands, tag "shown,
   not run".
8. Two columns from `.pre-commit-config.yaml:12–44`: "local hooks" (GREY) lists the nine hook ids;
   "CI" (BLUE): `black` and `flake8` get GREEN ticks and chips "api/ only · ci.yml:61" / ":66";
   the seven hygiene rows get GREY dashed "not in CI" one by one as they are named. A GREY
   `erratum` chip: "the slides: CI repeats the checks · this CI: two of them".
9. The erratum chip goes; two version chips: GREY "pre-commit: Black 24.1.1 (pinned)" and TEAL
   "image: black 26.10.1 (newest)" with a GREEN "=" between them and the tag "at the time of
   recording"; the "=" wobbles into a GREY dashed "≠ some day".
10. Table and chips clear. A GREY key-file icon sits on a GREY laptop; it rides a RED `--no-verify`
   arc into a BLUE "GitHub" box where GRAPH(run3)'s six nodes wait GREY (tag `illustration`); the
   nodes pulse in turn on the question. PONDER(8 s).
11. The card leaves. The key passes all six nodes untouched (each flashes GREY) and stays RED on
   GitHub. LECTURE 21 · 11. A GREY chat-card fragment (`#build-alerts`, tag `illustration`):
   "Failed step:" `Run python3 -m pre-commit run --all-files`; a GREEN dashed new step slides in
   under the lint job: `pre-commit run --all-files`. A RED chip "rotate the key: it's already on
   GitHub". Fade; empty frame.

Deviations from SHOW: beat 4 starts from the 3-row strip of beat 3, so the terminal first grows to
5 rows (the folded command and its two output rows), then shrinks back to the strip. V1 sits left of
centre in beats 4–5 (not in the middle) so the server can stand to its right for the push. In beat
5 the graph is drawn at its compact size straight away (short labels, badge above Build, tag on
the right): a names-sized graph does not fit above the 12.6-wide log at >= 20 pt, so there is no
shrink. In beats 6–7 the graph turns back into the server (for "caught") and then leaves with the
log, instead of shrinking. Beat 8 lists the real hook ids (`end-of-file-fixer`,
`check-added-large-files`, `check-merge-conflict`, `black`, `flake8`) rather than shortened names.
Line 5 of `run3/.../04` (blank) is dropped, per the conventions.
"""

import re

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S13"]

# ------------------------------------------------------------------ the real sources (checked)
C40 = capture("laptop/40")
C41 = capture("laptop/41")
C42 = capture("laptop/42")
C43 = capture("laptop/43")
C44 = capture("laptop/44")
C45 = capture("laptop/45")
C48 = capture("laptop/48")
C49 = capture("laptop/49")
assert C40.cmd_lines[0].startswith("sed -i 's/z = power(x, 2) + power(y, 2)/z=power(x,2)+power(y,2)/'"), C40.cmd_lines
assert C40.line(10) == "-    z = power(x, 2) + power(y, 2)", C40.line(10)
assert C40.line(11) == "+    z=power(x,2)+power(y,2)", C40.line(11)
assert C41.cmd_lines == ["git add ."]
assert C42.cmd_lines == ['git commit -m "quick fix"'] and C42.exit == 1
assert C42.line(9).startswith("Format Python code with Black") and C42.line(9).endswith("Failed"), C42.line(9)
assert C42.line(10) == "- hook id: black" and C42.line(11) == "- files were modified by this hook"
assert C42.line(13) == "reformatted src/api-service/api/service.py", C42.line(13)
assert C43.cmd_lines == ["git status --short"] and C43.line(2) == "MM src/api-service/api/service.py"
assert C44.cmd_lines == ['git commit --no-verify -m "quick fix"'], C44.cmd_lines
assert C44.line(2) == "[main 2892b1b] quick fix", C44.line(2)
assert C45.cmd_lines == ["git push"] and C45.line(3).strip() == "2289d89..2892b1b  main -> main", C45.line(3)
assert C48.cmd_lines == ["git status --short"] and C48.line(2) == " M src/api-service/api/service.py"
assert C49.cmd_lines == ["git restore src/api-service/api/service.py && git status --short"]
assert C49.exit == 0 and len(C49.lines) == 0, C49.lines
RUN3 = results("run3")
assert RUN3["lint-and-format"] == "failure" and all(RUN3[j] == "success" for j in JOB_IDS
                                                     if j != "lint-and-format"), RUN3
L04 = capture("run3/lint-and-format/04")
assert L04.line(4) == "would reformat /app/api/service.py" and L04.line(5) == "", L04.line(4)
assert L04.line(7) == "1 file would be reformatted, 2 files would be left unchanged.", L04.line(7)
X4 = capture("run3/lint-and-format/x4")
assert [s.split(" ")[0:2] for s in X4.at((4, 6))] == [["api/service.py:43:6:", "E225"],
                                                    ["api/service.py:43:14:", "E231"],
                                                    ["api/service.py:43:25:", "E231"]], X4.at((4, 6))
assert X4.cmd_lines[0].split(" ")[3] == "flake8" or "flake8" in X4.cmd_lines[0]
CFG = source_text(".pre-commit-config.yaml").split("\n")
HOOK_IDS = tuple(re.match(r"\s*- id: (\S+)", CFG[n - 1]).group(1) for n in (12, 14, 16, 18, 21, 23, 25, 32, 41))
assert HOOK_IDS[:7] == HYGIENE and HOOK_IDS[7:] == ("black", "flake8"), HOOK_IDS
CI = source_text(".github/workflows/ci.yml").split("\n")
assert "black --check --line-length 120 api/" in CI[61 - 1], CI[60]
assert "flake8 --max-line-length=120 --extend-ignore=E203,W503 api/" in CI[66 - 1], CI[65]
assert "rev: 24.1.1" in CFG[30 - 1] and VERSIONS["black (hook)"] == "24.1.1"
assert VERSIONS["black (image)"] == "26.10.1"

# ------------------------------------------------------------------ layout
TOP = 2.05                       # Part 2 pictures stay below PIC_TOP2 (2.15)
COLS = 65                        # the house terminal at 22 pt
CHAIN_L = np.array([-2.75, 0.45, 0])     # V1 left of centre (server on the right)
CHAIN_C = np.array([0.0, 0.45, 0])       # V1 in the middle (over a 3-row strip)
SERVER_C = np.array([4.75, 0.45, 0])
PONDER_Q = "A teammate commits a private key file\nwith --no-verify and pushes to main.\nWhich job of this pipeline catches it?"

_HOOK = re.compile(r"^(.*?[^.])(\.{3,})((?:\(no files to check\))?(?:Passed|Failed|Skipped))$")


def hook_row(s: str, n: int = COLS) -> str:
    """A pre-commit row with its dot leader shortened to fit `n` columns (words unchanged)."""
    m = _HOOK.match(s)
    if not m:
        return s
    name, _, tail = m.groups()
    dots = n - len(name) - len(tail)
    assert dots >= 3, s
    return name + "." * dots + tail


def server_box(box_w: float = 3.2, box_h: float = 1.9) -> VGroup:
    """The BLUE 'GitHub' server of slides 29–31 with its 'Check Code' box. .frame .title .check"""
    fr = box(box_w, box_h, GITHUB, fill_opacity=0.08, radius=0.2)
    tt = label("GitHub", 22, GITHUB).next_to(fr.get_corner(UL), DR, buff=0.18)
    t = label("Check Code", 20, INK)
    cf = RoundedRectangle(width=t.width + 0.36, height=0.62, corner_radius=0.1, stroke_color=INK,
                          stroke_width=2.5).set_fill(PANEL, 1)
    t.move_to(cf)
    ck = VGroup(cf, t)
    ck.frame, ck.text = cf, t
    ck.move_to(fr).shift(DOWN * 0.22)
    g = VGroup(fr, tt, ck)
    g.frame, g.title, g.check = fr, tt, ck
    return g


def bar_extra(t: Terminal, line) -> VGroup:
    """The row tag 'extra' beside a typed command's last row (it always fits here)."""
    tg = beside(extra_row(), line, buff=0.4)
    assert tg.get_right()[0] <= t.box.get_right()[0] - 0.12, tg.get_right()
    return tg


def clear_lines(scene, t: Terminal, run_time: float = 0.4):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    for m in gone:
        t.lines.remove(m)
    if gone:
        scene.play(FadeOut(VGroup(*gone)), run_time=run_time)
        scene.remove(*gone)


def compact_graph(states=None) -> JobGraph:
    """GRAPH(run3), compact: short labels, the run badge above Build, the tag right of Summary."""
    g = JobGraph(states=states, labels="short", size=20, pitch=0.55, col_gap=0.6)
    g.badge.next_to(g.nodes["build"], LEFT, buff=0.3)
    g.tag.next_to(g.nodes["lint-and-format"], RIGHT, buff=0.3)
    summ = g.nodes["test-summary"]
    assert g.tag.get_top()[1] < summ.get_bottom()[1] - 0.1, (g.tag.get_top(), summ.get_bottom())
    g.shift(-g.get_center()[0] * RIGHT)
    assert g.width < 12.9, g.width
    return g


def file_card(title: str, code_line: str, color) -> VGroup:
    """A file icon with its caption and the line it holds. .icon .cap .code"""
    ic = file_glyph(0.8, color)
    cap = label(title, 22, color)
    cl = mono(code_line, 20, INK)
    g = VGroup(ic, cap, cl).arrange(DOWN, buff=0.18)
    g.icon, g.cap, g.code = ic, cap, cl
    return g


def not_in_ci() -> VGroup:
    """A GREY dashed 'not in CI' chip sized for a 0.42 table row. .box .text"""
    t = label("not in CI", 20, S.GREY)
    ob = outline_box(t.width + 0.34, 0.36, S.GREY, solid=False, radius=0.18)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def code_card(head: str, lines, size: float = 20) -> VGroup:
    """A GREY card: a label header, then mono command rows. .frame .head .rows"""
    hd = label(head, 22, S.GREY)
    rows = VGroup(*[mono_line(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    body = VGroup(hd, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    fr = box(body.width + 0.6, body.height + 0.36, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.head, g.rows = fr, hd, rows
    return g


class NoVerify(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S13"] == 12, len(SAY)

        # ========================================================== 0. slide 29: why run them twice?
        tr = tracker_p5(8, True)
        strip = pipeline_strip("Lint and Format")
        ref = lref("29–31")
        title = grey_chip("The local conundrum", size=24).move_to([0, 1.65, 0])
        hc = HookChain(size=20).move_to(CHAIN_L + DOWN * 0.45)
        sv = server_box().move_to(SERVER_C + DOWN * 0.45)
        why_a = ArcBetween(hc.frame.get_right() + RIGHT * 0.1 + UP * 0.25,
                           sv.frame.get_left() + LEFT * 0.1 + UP * 0.25, -PI / 3, TURN, 3)
        why = label("why twice?", 22, TURN).next_to(why_a, UP, buff=0.12)
        assert why.get_right()[0] < sv.frame.get_left()[0] and hc.get_left()[0] > -6.6, hc.get_left()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(strip, shift=RIGHT * 0.3), run_time=0.6)
            self.play(FadeIn(ref), FadeIn(title, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("If the hooks already ran")
            self.play(FadeIn(hc, shift=UP * 0.15), run_time=0.5)
            d0 = hc.commit(self)
            hc.pass_through(self, d0, step=0.25)
            vo.wait_until("why run the same checks again")
            self.play(FadeIn(sv, shift=LEFT * 0.2), run_time=0.5)
            self.play(Create(why_a), FadeIn(why, shift=DOWN * 0.1), run_time=0.6)
            self.play(Circumscribe(sv.check, color=TURN, buff=0.06), Indicate(sv.check.text, color=TURN),
                      Indicate(hc.gates, color=TURN, scale_factor=1.03), run_time=0.9)

        # ========================================================== 1. extras: squeeze one line
        t = laptop_term(10)
        assert t.box.get_top()[1] < TOP, t.box.get_top()
        with self.voiceover(SAY[1]) as vo:
            gone = VGroup(title, hc, d0, sv, why_a, why)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("These steps are extras")
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("A quick edit")
            (sed,) = type_capture(self, t, C40, type_time=1.6)
            pin(self, sed, bar_extra(t, sed))
            vo.wait_until("and git diff shows it")
            minus, plus = out(self, t, [(C40.line(10), ERR), (C40.line(11), PASS)])
            hl = hl_bar(substring(plus, "z=power(x,2)+power(y,2)"), TURN, opacity=0.35)
            self.play(FadeIn(hl), Indicate(substring(plus, "z=power(x,2)+power(y,2)"), color=TURN,
                                           scale_factor=1.06), run_time=0.7)
            self.remove(hl)
            plus.add_to_back(hl)
            self.add(plus)

        # ========================================================== 2. the hook stops the commit
        hc2 = HookChain(size=20).move_to(CHAIN_C)
        assert hc2.get_top()[1] < TOP and hc2.get_bottom()[1] > STRIP_TOP + 0.1, (hc2.get_top(), hc2.get_bottom())
        with self.voiceover(SAY[2]) as vo:
            clear_lines(self, t, run_time=0.3)
            vo.wait_until("Git add dot")
            type_capture(self, t, C41, type_time=0.4)
            bare_prompt(self, t)
            vo.wait_until("then git commit")
            type_capture(self, t, C42, type_time=0.7)
            vo.wait_until("The Black hook fails")
            r9, r10, r11 = out(self, t, [(hook_row(C42.line(9)), ERR), C42.line(10), C42.line(11)])
            self.play(Indicate(substring(r9, "Failed"), color=ERR, scale_factor=1.25), run_time=0.5)
            vo.wait_until("and reformats the file")
            (r13,) = out(self, t, [(C42.line(13), TURN)])
            vo.wait_until("so the hook stopped the commit")
            resize(self, t, 3, keep=[r9, r11, r13], run_time=0.6)
            self.play(FadeIn(hc2, shift=UP * 0.15), run_time=0.4)
            d2 = hc2.commit(self)
            hc2.pass_through(self, d2, stop=1, step=0.25)

        # ========================================================== 3. git status --short: MM
        staged = file_card("staged: messy", "z=power(x,2)+power(y,2)", ERR).move_to([-3.2, 0.55, 0])
        work = file_card("working copy: reformatted", "z = power(x, 2) + power(y, 2)", PASS).move_to([3.2, 0.55, 0])
        assert staged.get_top()[1] < TOP and staged.get_bottom()[1] > STRIP_TOP + 0.1, staged.get_bottom()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(hc2, d2)), run_time=0.4)
            self.remove(hc2, d2, *hc2.get_family())
            vo.wait_until("Git status, short")
            type_capture(self, t, C43, type_time=0.5)
            (mm,) = out(self, t, [C43.line(2)])
            vo.wait_until("shows M twice")
            mm2 = substring(mm, "MM")
            self.play(Indicate(mm2, color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("Black fixed your working copy")
            a2 = mm2[1].copy()
            self.add(a2)
            self.play(FadeIn(work, shift=UP * 0.2), mm2[1].animate.set_color(PASS),
                      a2.animate.move_to(work.icon.get_left() + LEFT * 0.35).set_color(PASS), run_time=0.8)
            vo.wait_until("but the staged copy")
            a1 = mm2[0].copy()
            self.add(a1)
            self.play(FadeIn(staged, shift=UP * 0.2), mm2[0].animate.set_color(ERR),
                      a1.animate.move_to(staged.icon.get_left() + LEFT * 0.35).set_color(ERR), run_time=0.8)
            self.play(Indicate(staged.code, color=ERR, scale_factor=1.06), run_time=0.6)

        # ========================================================== 4. slide 30: --no-verify
        hc4 = HookChain(size=20).move_to(CHAIN_L)
        assert hc4.get_left()[0] > -6.6, hc4.get_left()
        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(staged, work, a1, a2)
            self.play(FadeOut(gone), run_time=0.4)
            self.remove(gone, *gone.get_family())
            resize(self, t, 5, run_time=0.5)
            vo.wait_until("Now the lecture's command")
            self.play(Indicate(ref, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("git commit, no verify")
            (nv,) = type_capture(self, t, C44, type_time=1.0)
            nv_flag = substring(nv.rows[0], "--no-verify")
            self.play(nv_flag.animate.set_color(ERR), run_time=0.4)
            pin(self, nv, bar_extra(t, nv))
            vo.wait_until("No hook ran")
            r_main, r_one = out(self, t, [C44.line(2), C44.line(3)])
            vo.wait_until("and the commit exists")
            self.play(Indicate(substring(r_main, "[main 2892b1b] quick fix"), color=INK, scale_factor=1.06),
                      run_time=0.5)
            resize(self, t, 3, run_time=0.5)
            vo.wait_until("no verify skips every pre-commit check")
            self.play(FadeIn(hc4, shift=UP * 0.15), run_time=0.4)
            d4 = hc4.commit(self, color=PASS)
            arc = hc4.bypass(self, d4, run_time=1.0)
            nvc = err_chip("--no-verify", mono_font=True)
            nvc.move_to(hc4.frame.get_corner(DR) + np.array([-0.2 - nvc.width / 2, 0.2 + nvc.height / 2, 0]))
            assert nvc.get_top()[1] < hc4.gates.get_bottom()[1] or nvc.get_left()[0] > hc4.gates.get_right()[0] + 0.2, \
                (nvc.get_corner(UL), hc4.gates.get_corner(DR))
            self.play(FadeIn(nvc, shift=DOWN * 0.1), d4.animate.set_color(ERR), run_time=0.4)
            hc4.keep(self, nvc)

        # ========================================================== 5. push: run 3
        sv5 = server_box().move_to(SERVER_C)
        g5 = compact_graph(None)
        lg = run_log(L04, (4, 6, 7), colors={4: ERR})
        lg.move_to([0, -3.5 + lg.height / 2, 0])
        g5.move_to([0, (TOP + lg.get_top()[1] + 0.35) / 2, 0])
        assert lg.get_top()[1] < g5.get_bottom()[1] - 0.15, (lg.get_top(), g5.get_bottom())
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeIn(sv5, shift=LEFT * 0.2), run_time=0.4)
            vo.wait_until("Push it")
            (pl,) = type_capture(self, t, C45, type_time=0.4)
            (pushed,) = out(self, t, [C45.line(3)])
            hc4.push(self, d4, sv5.frame.get_left() + RIGHT * 0.5 + DOWN * 0.25, arc=-0.4, run_time=0.7)
            vo.wait_until("Run 3")
            self.play(FadeOut(VGroup(hc4, d4, t)), run_time=0.4)
            self.remove(hc4, d4, t, *hc4.get_family(), *t.get_family())
            self.play(ReplacementTransform(sv5, g5), run_time=0.8)
            vo.wait_until("lint and format, red")
            g5.reveal(self, RUN3, order=["build", "lint-and-format"], per=0.35, badge=False)
            vo.wait_until("on service dot py")
            self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(lg.row(4), color=ERR, scale_factor=1.05), run_time=0.6)
            vo.wait_until("The tests and the summary all pass")
            g5.reveal(self, RUN3, order=["unit-tests", "integration-tests", "system-tests", "test-summary"],
                      per=0.3, running=True, badge=True)

        # ========================================================== 6. what Flake8 would have said
        lg6 = run_log(X4, ((4, 6),), title="Lint and Format Check · extra: Flake8, if it had run",
                      colors={4: ERR, 5: ERR, 6: ERR})
        lg6.move_to([0, -3.5 + lg6.height / 2, 0])
        xt = extra_tag().next_to(lg6.frame, UP, buff=0.1).align_to(lg6.frame, LEFT)
        sv6 = server_box().move_to([0, 0.95, 0])
        caught = err_chip("caught", size=22).next_to(sv6.check, RIGHT, buff=0.35)
        caught.shift(RIGHT * max(0, sv6.frame.get_right()[0] + 0.25 - caught.get_left()[0]))
        assert sv6.get_bottom()[1] > xt.get_top()[1] + 0.1, (sv6.get_bottom(), xt.get_top())
        with self.voiceover(SAY[6]) as vo:
            self.play(ReplacementTransform(lg, lg6), run_time=0.8)
            self.play(FadeIn(xt, shift=DOWN * 0.1), run_time=0.3)
            vo.wait_until("three times")
            self.play(LaggedStart(*[Indicate(substring(lg6.row(n), code_), color=ERR, scale_factor=1.25)
                                    for n, code_ in ((4, "E225"), (5, "E231"), (6, "E231"))], lag_ratio=0.35),
                      run_time=1.2)
            vo.wait_until("CI caught what no verify let through")
            self.play(ReplacementTransform(g5, sv6), run_time=0.8)
            red_ck = sv6.check.copy()
            red_ck[0].set_stroke(ERR)
            red_ck[1].set_color(ERR)
            self.play(Transform(sv6.check, red_ck), Circumscribe(sv6.check, color=ERR, buff=0.06),
                      FadeIn(caught, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("slide 31")
            self.play(Indicate(ref, color=TURN, scale_factor=1.06), Indicate(caught, color=ERR, scale_factor=1.1),
                      run_time=0.7)

        # ========================================================== 7. clean up the experiment
        t7 = laptop_term(5)
        card = code_card("pushed it too?", ["pre-commit run --all-files", "git add .",
                                            'git commit -m "Format service.py"', "git push"])
        red = VGroup(state_mark("failure", 0.3), mono("main", 22, OWN)).arrange(RIGHT, buff=0.15)
        red.next_to(card.head, RIGHT, buff=0.35)
        card.add(red)
        card.move_to([-1.2, (TOP + t7.box.get_top()[1]) / 2, 0])
        shown = shown_tag().next_to(card, RIGHT, buff=0.3).align_to(card, UP)
        assert card.get_top()[1] < TOP and card.get_bottom()[1] > t7.box.get_top()[1] + 0.1, card.get_bottom()
        with self.voiceover(SAY[7]) as vo:
            gone = VGroup(sv6, caught, lg6, xt)
            self.play(FadeOut(gone), FadeOut(ref), run_time=0.5)
            self.remove(gone, ref, *gone.get_family())
            self.play(FadeIn(t7, shift=UP * 0.2), run_time=0.4)
            type_capture(self, t7, C48, type_time=0.5)
            (m8,) = out(self, t7, [C48.line(2)])
            self.play(Indicate(substring(m8, "M"), color=PASS, scale_factor=1.4), run_time=0.5)
            vo.wait_until("git restore puts the file back")
            type_capture(self, t7, C49, type_time=1.0)
            bare_prompt(self, t7)
            vo.wait_until("If you pushed it too")
            self.play(FadeIn(card, shift=DOWN * 0.15), FadeIn(shown, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("your main is now red")
            self.play(Indicate(red, color=ERR, scale_factor=1.15), run_time=0.6)
            vo.wait_until("run pre-commit run, all files")
            self.play(Indicate(card.rows[0], color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("then add, commit and push")
            self.play(LaggedStart(*[Indicate(r, color=TURN, scale_factor=1.05) for r in card.rows[1:]],
                                  lag_ratio=0.35), run_time=1.2)

        # ========================================================== 8. what CI repeats, and what not
        pitch = 0.42
        hdr_y, row0 = 1.85, 1.32
        lx, rx = -5.9, 0.6
        lh = VGroup(label("local hooks", 24, LAPTOP), mono(".pre-commit-config.yaml", 20, S.GREY)).arrange(RIGHT, buff=0.3)
        lh.move_to([lx + lh.width / 2, hdr_y, 0])
        rh = label("CI", 24, GITHUB).move_to([rx, hdr_y, 0]).align_to(np.array([rx, 0, 0]), LEFT)
        names = VGroup(*[mono(h, 22, INK).move_to([0, row0 - i * pitch, 0]).align_to(np.array([lx, 0, 0]), LEFT)
                         for i, h in enumerate(HOOK_IDS)])
        rule = Line([lx, hdr_y - 0.3, 0], [6.2, hdr_y - 0.3, 0], color=S.GREY_DARK, stroke_width=2)
        ticks = VGroup()
        for i, n in ((7, 61), (8, 66)):
            mk = check_mark(0.3, PASS)
            ch = row_tag([(f"api/ only · ci.yml:{n}", "mono")], PASS)
            row = VGroup(mk, ch).arrange(RIGHT, buff=0.25).move_to([0, names[i].get_center()[1], 0])
            row.align_to(np.array([rx, 0, 0]), LEFT)
            ticks.add(row)
        nots = VGroup(*[not_in_ci().move_to([0, names[i].get_center()[1], 0])
                        .align_to(np.array([rx, 0, 0]), LEFT) for i in range(7)])
        err8 = VGroup(erratum_tag(), grey_chip("the slides: CI repeats the checks · this CI: two of them"))
        err8.arrange(RIGHT, buff=0.25).move_to([0, -2.72, 0])
        assert names[-1].get_bottom()[1] > err8.get_top()[1] + 0.15, names[-1].get_bottom()
        table = VGroup(lh, rh, rule, names)
        spoken = ("trailing whitespace", "end of file", "YAML", "large files", "JSON", "merge markers",
                  "and private keys")
        with self.voiceover(SAY[8]) as vo:
            gone = VGroup(t7, card, shown)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            self.play(FadeIn(lh, shift=RIGHT * 0.2), FadeIn(rh, shift=LEFT * 0.2), Create(rule), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.15) for n in names], lag_ratio=0.12), run_time=1.2)
            vo.wait_until("But CI repeats only Black and Flake8")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in ticks], lag_ratio=0.4),
                      names[7].animate.set_color(PASS), names[8].animate.set_color(PASS), run_time=0.8)
            vo.wait_until("and only on the api folder")
            self.play(LaggedStart(*[Indicate(r[1], color=PASS, scale_factor=1.08) for r in ticks], lag_ratio=0.3),
                      FadeIn(err8, shift=UP * 0.15), run_time=0.9)
            vo.wait_until("The seven hygiene hooks never run in CI")
            self.play(Indicate(VGroup(*names[:7]), color=S.GREY, scale_factor=1.03), run_time=0.6)
            for i, w in enumerate(spoken):
                vo.wait_until(w)
                self.play(FadeIn(nots[i], shift=LEFT * 0.15), names[i].animate.set_color(S.GREY), run_time=0.3)
            self.play(Indicate(names[6], color=ERR, scale_factor=1.08), run_time=0.5)

        # ========================================================== 9. pinned Black vs the image's Black
        v1 = grey_chip(f"pre-commit: Black {VERSIONS['black (hook)']} (pinned)", size=20)
        v2 = image_chip(f"image: black {VERSIONS['black (image)']} (newest)", size=20)
        eq = label("=", 36, PASS)
        vrow = VGroup(v1, eq, v2).arrange(RIGHT, buff=0.85).move_to([0, -2.72, 0])
        ne = dashed_chip("≠ some day", S.GREY, size=22).move_to(eq)
        assert ne.width < 0.85 * 2 + eq.width + 0.5 - 0.3, ne.width
        assert vrow.width + 0.5 < 13.2, vrow.width
        rec = recording_tag().move_to([0, -3.3, 0])
        assert vrow.get_top()[1] < names[-1].get_bottom()[1] - 0.1 and rec.get_top()[1] < vrow.get_bottom()[1], \
            (vrow.get_top(), rec.get_top())
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(err8), table.animate.fade(0.55), nots.animate.fade(0.55),
                      ticks.animate.fade(0.55), run_time=0.5)
            self.remove(err8, *err8.get_family())
            vo.wait_until("the hooks pin an older Black")
            self.play(FadeIn(v1, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("than the image installs")
            self.play(FadeIn(v2, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("At the time of recording they agreed")
            self.play(FadeIn(eq, scale=0.6), FadeIn(rec, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("but they can drift apart")
            self.play(Wiggle(eq, scale_value=1.3, rotation_angle=0.08 * TAU), run_time=0.8)
            self.play(ReplacementTransform(eq, ne), v1.animate.shift(LEFT * 0.25), v2.animate.shift(RIGHT * 0.25),
                      run_time=0.6)

        # ========================================================== 10. ponder: a key with --no-verify
        lap = laptop_icon(1.6).move_to([-5.3, 0.0, 0])
        key = key_file(0.6).next_to(lap, UP, buff=0.1)
        g10 = JobGraph(states=None, labels="short", size=20, pitch=0.58, col_gap=0.6, badge=False,
                       tag_text=None)
        gh = box(g10.width + 0.7, g10.height + 1.75, GITHUB, fill_opacity=0.06, radius=0.2)
        gh_t = label("GitHub", 22, GITHUB).next_to(gh.get_corner(UL), DR, buff=0.18)
        gil = illustration_tag().next_to(gh.get_corner(UR), DL, buff=0.12)
        g10.move_to(gh).shift(UP * 0.05)
        hub = VGroup(gh, gh_t, gil, g10)
        hub.move_to([6.45 - hub.width / 2, TOP - hub.height / 2, 0])
        assert hub.get_left()[0] > lap.get_right()[0] + 1.6, (hub.get_left(), lap.get_right())
        land = g10.nodes["build"].get_top() + UP * 0.45
        kpath = ArcBetweenPointsNoTip(key.get_center(), land, -PI / 5, ERR, 4)
        nv10 = err_chip("--no-verify", mono_font=True).next_to(kpath, DOWN, buff=0.12)
        nv10.move_to([(lap.get_right()[0] + gh.get_left()[0]) / 2, nv10.get_center()[1], 0])
        assert kpath.get_top()[1] < TOP and nv10.get_right()[0] < gh.get_left()[0] - 0.1, (kpath.get_top(), nv10.get_right())
        with self.voiceover(SAY[10]) as vo:
            gone = VGroup(table, nots, ticks, v1, v2, ne, rec)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            vo.wait_until("A teammate commits")
            self.play(FadeIn(lap, shift=UP * 0.15), FadeIn(hub, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("a private key file")
            self.play(FadeIn(key, shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("with no verify")
            self.play(Create(kpath), FadeIn(nv10), run_time=0.6)
            vo.wait_until("and pushes to main")
            self.play(MoveAlongPath(key, kpath), run_time=1.0)
            vo.wait_until("Which job of this pipeline")
            order = ["build", "lint-and-format", "unit-tests", "integration-tests", "system-tests", "test-summary"]
            self.play(LaggedStart(*[g10.pulse(j, INK) for j in order], lag_ratio=0.3), run_time=1.8)
        card10 = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 11. none: add the step, rotate the key
        ref11 = lref("11")
        chat = chat_window(rows=[label("Failed step:", 20, ERR),
                                 mono("Run python3 -m", 20, INK), mono("pre-commit run --all-files", 20, INK)],
                           win_w=4.9, win_h=1.95)
        chat.move_to([-6.45 + chat.width / 2, 0.65, 0])
        ctag = illustration_tag().next_to(chat, DOWN, buff=0.15).align_to(chat, LEFT)
        lint = g10.nodes["lint-and-format"]
        step = dashed_chip("pre-commit run --all-files", PASS, size=20, mono_font=True)
        step.next_to(lint, DOWN, buff=0.22).align_to(lint, LEFT)
        rot = err_chip("rotate the key: it's already on GitHub", size=22).move_to([0, -3.05, 0])
        assert step.get_bottom()[1] > hub.get_bottom()[1] + 0.05 and step.get_right()[0] < gh.get_right()[0] - 0.1, \
            (step.get_bottom(), step.get_right())
        assert chat.get_right()[0] < hub.get_left()[0] - 0.15, (chat.get_right(), hub.get_left())
        assert rot.get_top()[1] < min(hub.get_bottom()[1], ctag.get_bottom()[1]) - 0.1, rot.get_top()
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(card10), run_time=0.4)
            self.remove(card10)
            vo.wait_until("None")
            for j in ("build", "unit-tests", "integration-tests", "system-tests", "lint-and-format", "test-summary"):
                nd = g10.nodes[j]
                self.play(key.animate.move_to(nd.get_top() + UP * 0.36), run_time=0.22)
                self.play(g10.pulse(j, S.GREY), run_time=0.22)
            vo.wait_until("Detect private key is a local hook only")
            self.play(FadeOut(VGroup(kpath, nv10)), run_time=0.4)
            self.remove(kpath, nv10)
            self.play(Indicate(lap, color=S.GREY, scale_factor=1.1), key.animate.set_color(ERR), run_time=0.6)
            vo.wait_until("The fix is one CI step")
            self.play(FadeOut(lap), run_time=0.3)
            self.remove(lap)
            self.play(FadeIn(step, shift=UP * 0.3), Circumscribe(lint, color=PASS, buff=0.06), run_time=0.7)
            vo.wait_until("the very step that fails")
            self.play(FadeIn(ref11), FadeIn(chat, shift=RIGHT * 0.2), FadeIn(ctag), run_time=0.6)
            self.play(Indicate(chat.rows[2], color=TURN, scale_factor=1.06),
                      Indicate(step.text, color=PASS, scale_factor=1.06), run_time=0.8)
            vo.wait_until("And rotate that key")
            self.play(FadeIn(rot, shift=UP * 0.15), Indicate(key, color=ERR, scale_factor=1.3), run_time=0.6)
        self.play(FadeOut(VGroup(hub, key, step, chat, ctag, rot, ref11, tr, strip)), run_time=0.8)
        self.wait(0.3)
