"""S15 · Branch protection: from report to gate (AC215 L21). TRACKER P6 1–6 (the optional README
Part 6, README.md:369–397). Lecture: 21 · slides 5–6 (beat 0 only). Set pieces V1 ServerDoor (beat
0), V3 TriggerLanes (beat 3). No pipeline strip: S15's SHOW names none (Part 6 is not a pipeline
stage), and the frame needs the room.

Beats (script.md "## S15", one voiceover block each):
0. TRACKER P5 8 cross-fades into TRACKER P6 1. LECTURE 21 · 5–6. S02's door returns as
   "GitHub.com": the GREY 'post-receive' bell with the BLUE 'Actions' badge inside, the door in its
   left wall. On "post-receive bell" a GREEN commit dot goes through the door, the bell rings and
   the Actions badge sparks. On "the gate that refuses" the GREEN 'branch protection' gate docks in
   front of the door; on "with required status checks" (GREY chip under it) a second dot comes,
   the gate lights GREEN and shuts, the dot turns RED and bounces back.
1. LECTURE off. README(373–379) card left (rows light as they are said). Right, a schematic
   Settings → Branches page (BLUE frame, tag `illustration`): BLUE "Add rule" button, field
   "Branch name pattern" `main`, two checkboxes ticked on their phrases. A GREY note under the
   README card: "today's page may say / “classic branch protection rule” / or offer rulesets".
2. TRACKER P6 2. The README card folds to its line 378 (the ids); the note leaves. A check picker
   under the checkboxes: four rows with the job names (GREEN ticks), two pulsed on their phrases.
   Line 378 is struck GREY with "erratum · names, not ids" and "listed after a recent run" under
   it; GOLD cost_tag("private repo: paid plan · public: free") and GREY "GitHub Pro: Student
   Developer Pack".
3. TRACKER P6 3. Card and page leave. README(383–396) as a GREY code card (tag "shown, not run"),
   line 385 `git checkout -b feature/test-protection` YELLOW. S04's lanes return small under it
   (main, feature/test-protection): a dot pushed to the feature lane gives no spark; the PR arrow
   into main gives one.
4. TRACKER P6 4. The lanes leave, the card folds to line 388. An 8-row `laptop` terminal types
   `echo "def broken(): assert False" >> tests/unit/test_utils.py` → TERM(laptop/51: no output).
   TRACKER P6 4 · extra: `docker build -t cheese-app-api:local .` (extra) → TERM(laptop/52: 2, …,
   61), `docker run --rm cheese-app-api:local pytest tests/unit/ -v` (extra) → TERM(laptop/53:
   15, …, 29): `collected 11 items`, `11 passed` YELLOW; GREY `erratum` chip beside the card's
   line 388. On "because pytest only collects" the terminal shrinks to a 3-row strip and
   CODE(pytest.ini: 6–8) takes the middle; line 8 `python_functions = test_*` YELLOW on "start
   with test".
5. The pytest.ini panel leaves; the terminal grows back. GREY chip "test file restored" (laptop/54,
   not typed); it types `echo "def test_broken(): assert False" >> tests/unit/test_utils.py`
   (extra) → TERM(laptop/55: no output); the chip becomes "rebuilt" (laptop/56, not printed);
   `docker run --rm cheese-app-api:local pytest tests/unit/ -v` → TERM(laptop/57: 28, 37–38):
   `test_broken FAILED`, `1 failed, 11 passed` RED. On the card, `def broken` is struck GREY and
   `def test_broken` written above it (GREEN), "commit the corrected line".
6. TRACKER P6 5. The terminal leaves; the card becomes README lines 391–393 (shown, not run), each
   line lit on its phrase. TRACKER P6 6: the card moves to the top and a schematic PR row takes the
   frame (tag `illustration`): "Unit Tests ✗ · required" and a GREY locked "Merge pull request"
   button; GREY chip "fork: set base repository to <you>/cheese-app-ci-cd"; `▶ your turn`. The PR
   row fades; a 3-row strip terminal types `git checkout -- tests/unit/test_utils.py && git status
   --short` (extra) → TERM(laptop/58: no output). Fade; empty frame.

Deviations from SHOW: the README(383–396) card cannot share the frame at 20 pt with an 8-row
terminal, so from beat 4 on it folds to the line being discussed (388), then to 391–393 (beat 6),
by Transform; the struck line and its correction stay with it. In beat 2 the README card folds to
its line 378 so the picker's slip, the cost tag and the Pro chip fit beside the page. The pytest
summary rows of 53 and 57 are shown without their '=' padding and 57:28 with its space run
squeezed (the words are the capture's; S10 does the same). No pipeline strip (see above).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S15"]

# ------------------------------------------------------------------ the real sources (checked)
README_SRC = source_text("README.md").split("\n")
assert README_SRC[369 - 1] == "## Part 6: Branch Protection (Optional)", README_SRC[368]
assert README_SRC[378 - 1].startswith("   - Select: `lint-and-format`"), README_SRC[377]
assert README_SRC[385 - 1] == "git checkout -b feature/test-protection", README_SRC[384]
assert README_SRC[388 - 1] == 'echo "def broken(): assert False" >> tests/unit/test_utils.py'
assert README_SRC[391 - 1: 393] == ["git add .", 'git commit -m "Intentionally break tests"',
                                    "git push origin feature/test-protection"], README_SRC[390:393]
INI = source_text("pytest.ini").split("\n")
assert INI[8 - 1] == "python_functions = test_*", INI[7]

C51, C52, C53 = capture("laptop/51"), capture("laptop/52"), capture("laptop/53")
C55, C57, C58 = capture("laptop/55"), capture("laptop/57"), capture("laptop/58")
assert C51.cmd == README_SRC[388 - 1] and C51.exit == 0 and not C51.lines
assert C52.cmd == "docker build -t cheese-app-api:local ." and C52.exit == 0
assert C52.line(2) == '#0 building with "default" instance using docker driver' and C52.line(61) == "#16 DONE 0.1s"
assert C53.cmd == "docker run --rm cheese-app-api:local pytest tests/unit/ -v" and C53.exit == 0
assert C53.line(15) == "collecting ... collected 11 items", C53.line(15)
assert C55.cmd == 'echo "def test_broken(): assert False" >> tests/unit/test_utils.py' and not C55.lines
assert C57.cmd == C53.cmd and C57.exit == 1
assert C58.cmd == "git checkout -- tests/unit/test_utils.py && git status --short" and not C58.lines
assert capture("laptop/54").exit == 0 and capture("laptop/56").exit == 0


def summary(s: str) -> str:
    """A pytest summary row without its '=' padding (S10 and L09 do the same)."""
    assert s.startswith("=") and s.endswith("="), s
    return s.strip("= ")


L53_15, L53_29 = C53.line(15), summary(C53.line(29))
assert L53_29 == "11 passed in 0.03s", L53_29
L57_28 = squeeze_spaces(C57.line(28))
L57_37, L57_38 = C57.line(37), summary(C57.line(38))
assert L57_28 == "tests/unit/test_utils.py::test_broken FAILED  [100%]", L57_28
assert L57_37 == "FAILED tests/unit/test_utils.py::test_broken - assert False", L57_37
assert L57_38 == "1 failed, 11 passed in 0.05s", L57_38
JOB_ROWS = ["Lint and Format Check", "Unit Tests", "Integration Tests", "System Tests"]
assert [JOB_NAME[j] for j in ("lint-and-format", "unit-tests", "integration-tests", "system-tests")] == JOB_ROWS

# ------------------------------------------------------------------ layout
TOP = 2.75                       # pictures stay below PIC_TOP (no strip in this scene)
LEFT_X = -6.5
CARD_SIZE = 20


def readme_code(nums, size: float = CARD_SIZE, colors: dict | None = None, gaps: dict | None = None,
                where: str | None = None) -> VGroup:
    """README lines `nums` (inside its ```bash fence) as a GREY code card: header 'README.md · lines
    a–b', the raw lines in mono (comments GREY, commands WHITE, ❌ drawn). gaps={file line: extra
    space above that row}. .frame .head .rows{file line: mono_line}"""
    colors, gaps = colors or {}, gaps or {}
    pitch = line_pitch(size)
    rows, body, y = {}, VGroup(), 0.0
    for n in nums:
        s = README_SRC[n - 1]
        col = colors.get(n, S.GREY if s.startswith("#") else INK)
        r = emo_line(s, size, col)
        y -= gaps.get(n, 0.0)
        r.shift(-r.strut.get_corner(UL) + UP * y)
        y -= pitch
        rows[n] = r
        body.add(r)
    if gaps.get(nums[0]):
        body.add(Rectangle(width=0.01, height=gaps[nums[0]], stroke_width=0, fill_opacity=0)
                 .move_to(body[0].get_corner(UL), aligned_edge=DOWN))   # room above the first row
    a, b = nums[0], nums[-1]
    where = where or (f"line {a}" if a == b else f"lines {a}–{b}")
    head = VGroup(mono("README.md", CAPTION, S.GREY), label(f"· {where}", CAPTION, S.GREY)).arrange(RIGHT, buff=0.12)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    frame = box(inner.width + 0.6, inner.height + 0.42, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    g = VGroup(frame, inner)
    g.frame, g.head, g.rows = frame, head, rows
    return g


def at_top_left(m, top: float = TOP, left: float = LEFT_X):
    return m.shift(np.array([left - m.get_left()[0], top - m.get_top()[1], 0]))


def note_box(lines, size: float = 20, color=S.GREY) -> VGroup:
    """A GREY rounded note of a few short lines (a chip too long for one row)."""
    t = VGroup(*[label(s, size, INK if i == 1 else color) for i, s in enumerate(lines)])
    t.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.36, corner_radius=0.14,
                          stroke_color=color, stroke_width=2).set_fill(S.BG, 0.95)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def lock_glyph(h: float = 0.3, color=S.GREY) -> VGroup:
    body = RoundedRectangle(width=h * 0.9, height=h * 0.65, corner_radius=0.03, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.3)
    shackle = Arc(radius=h * 0.28, start_angle=0, angle=PI, color=color, stroke_width=2.5)
    shackle.next_to(body, UP, buff=0)
    return VGroup(body, shackle)


def extra_pin(scene, t: Terminal, ln):
    """PLAYS: the GREY 'extra' row tag beside a typed row, or on the title bar when the row is too long."""
    tg = beside(extra_row(), ln)
    if tg.get_right()[0] > 6.45:
        tg = on_bar(t, extra_row())
        scene.play(FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
        return tg
    pin(scene, ln, tg)
    return None


def pr_arrow(scene, tl: TriggerLanes, src: str, dst: str = "main"):
    """TriggerLanes.pr(fire=False) with the label left of the arc, between the two lanes (as S04)."""
    a = tl.dots[src][-1].get_center() + UP * 0.12
    b = np.array([tl.lx1 - 0.3, tl.lanes[dst].line.get_center()[1], 0]) + DOWN * 0.12
    ar = route(a, b, arc=-0.6, dashed=True)
    y = tl.lanes[dst].line.get_center()[1] - tl.pitch * 0.5
    pts = route(a, b, arc=-0.6).get_points()
    p = min(pts, key=lambda q: abs(q[1] - y))
    t = label(f"PR → {dst}", 20, ROUTE)
    t.move_to([p[0] - 0.25 - t.width / 2, y, 0])
    scene.play(Create(ar), FadeIn(t), run_time=0.6)
    tl.pr_arrow, tl.pr_label, tl.pr_dst, tl.pr_a, tl.pr_b = ar, t, dst, a, b
    tl.keep(scene, ar, t)
    return ar, t


class ProtectMain(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S15"] == 7, len(SAY)

        # ========================================================== 0. the bell and the gate
        tr5 = tracker_p5(8)
        tr = tracker_p6(1)
        ref = lref("5–6")
        sd = ServerDoor(name="GitHub.com", box_w=5.0, box_h=3.0)
        for m in (sd.gate, sd.gate.text):
            sd.remove(m)
        act = github_chip("Actions").next_to(sd.bell, UP, buff=0.12)
        sd.add(act)
        sd.shift(np.array([0.9 - sd.server.get_center()[0], 0.0 - sd.server.get_center()[1], 0]))
        prot = gate_glyph(0.9, 0.6, S.GREY).move_to(sd.door.get_left() + LEFT * 0.42)
        prot_t = label("branch protection", 20, PASS).next_to(prot, UP, buff=0.12)
        prot_t.shift(LEFT * max(0, prot_t.get_right()[0] - (sd.door.get_left()[0] - 0.12)))
        req = grey_chip("required status checks").next_to(prot, DOWN, buff=0.3)
        req.shift(LEFT * max(0, req.get_right()[0] - (sd.door.get_left()[0] - 0.12)))
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr5, shift=RIGHT * 0.2), run_time=0.4)
            swap_tracker(self, tr5, tr)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.05), run_time=0.5)
            vo.wait_until("it's the lecture's gate")
            self.play(FadeIn(ref), FadeIn(sd, shift=LEFT * 0.3), run_time=0.7)
            vo.wait_until("A push-triggered run")
            d1 = dot(PASS).move_to(sd.start)
            self.play(FadeIn(d1), run_time=0.2)
            self.play(d1.animate.move_to(sd.door), run_time=0.6)
            self.play(d1.animate.move_to(sd.landing), run_time=0.4)
            vo.wait_until("is the post-receive bell")
            sp = spark().move_to(act)
            self.play(FadeIn(sp, scale=0.5), Indicate(act, color=ROUTE, scale_factor=1.1), run_time=0.35)
            self.play(FadeOut(sp, scale=1.4), run_time=0.25)
            self.remove(sp)
            sd.ring(self)
            self.play(Indicate(sd.bell_text, color=INK, scale_factor=1.1), run_time=0.5)
            vo.wait_until("the gate that refuses")
            self.play(FadeIn(prot, shift=RIGHT * 0.3), FadeIn(prot_t), run_time=0.6)
            self.play(prot.bar.animate.set_color(PASS), prot.posts.animate.set_color(PASS),
                      Indicate(prot_t, color=PASS, scale_factor=1.08), run_time=0.6)
            vo.wait_until("with required status checks")
            self.play(FadeIn(req, shift=UP * 0.15), run_time=0.4)
            d2 = dot(PASS).move_to(sd.start)
            self.play(FadeIn(d2), run_time=0.2)
            self.play(d2.animate.move_to(prot.get_left() + LEFT * 0.15), run_time=0.5)
            self.play(Indicate(prot, color=PASS, scale_factor=1.12), d2.animate.set_color(ERR), run_time=0.5)
            self.play(d2.animate.move_to(sd.start), run_time=0.5)
            sd.keep(self, d1, d2, prot, prot_t, req)

        # ========================================================== 1. Settings → Branches
        card = readme_panel(373, 379, card_w=5.4, size=20)
        at_top_left(card)
        page = gh_page("Settings → Branches", page_w=7.2, page_h=5.85)
        page.shift(np.array([6.5 - page.get_right()[0], TOP - page.get_top()[1], 0]))
        add_rule = github_chip("Add rule").move_to(page.crumb).align_to(page.frame, RIGHT).shift(LEFT * 0.3)
        bx = page.body.get_left()[0]
        field = field_row("Branch name pattern", "main", value_color=OWN, field_w=3.0)
        field.move_to([bx + field.width / 2, page.crumb.get_bottom()[1] - 0.5 - field.height / 2, 0])
        cb1 = checkbox_row("Require a pull request before merging")
        cb2 = checkbox_row("Require status checks to pass before merging")
        cbs = VGroup(cb1, cb2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        cbs.next_to(field, DOWN, buff=0.4).align_to(field, LEFT)
        for cb in (cb1, cb2):
            cb.remove(cb.tick)
        ill = illustration_tag().next_to(page.frame.get_corner(DR), UL, buff=0.15)
        ill.shift(DOWN * (ill.get_bottom()[1] - page.frame.get_bottom()[1] - 0.15))
        today = note_box(["today's page may say", "“classic branch protection rule”", "or offer rulesets"])
        today.next_to(card, DOWN, buff=0.3).align_to(card, LEFT)
        rows = card.rows
        with self.voiceover(SAY[1]) as vo:
            gone = VGroup(sd)
            self.play(FadeOut(gone, shift=LEFT * 0.4), FadeOut(ref), run_time=0.5)
            self.remove(gone, *gone.get_family(), ref)
            self.play(FadeIn(card, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Go to Settings")
            self.play(FadeIn(VGroup(page, ill), shift=LEFT * 0.2), Indicate(rows[373], color=TURN, scale_factor=1.04),
                      run_time=0.6)
            vo.wait_until("and add a rule for main")
            self.play(FadeIn(add_rule, scale=0.8), run_time=0.4)
            self.play(Indicate(add_rule, color=GITHUB, scale_factor=1.1), FadeIn(field, shift=DOWN * 0.15),
                      run_time=0.6)
            self.play(Indicate(rows[374], color=TURN, scale_factor=1.04), Indicate(field.value, color=OWN, scale_factor=1.2),
                      run_time=0.6)
            vo.wait_until("Tick the boxes")
            self.play(FadeIn(cbs, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("Require a pull request before merging")
            self.play(Create(cb1.tick), Indicate(rows[376], color=TURN, scale_factor=1.04), run_time=0.6)
            vo.wait_until("and Require status checks to pass")
            self.play(Create(cb2.tick), Indicate(rows[377], color=TURN, scale_factor=1.04), run_time=0.6)
            cb1.add(cb1.tick)
            cb2.add(cb2.tick)
            vo.wait_until("Today's page may call it")
            self.play(FadeIn(today, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("or offer rulesets instead")
            self.play(Indicate(today.text[2], color=INK, scale_factor=1.08), run_time=0.6)

        # ========================================================== 2. pick the checks (a slip)
        card2 = readme_panel(373, 379, lines=[378], card_w=5.4, size=20)
        at_top_left(card2)
        r378 = card2.rows[378]
        r378_parts = r378 if isinstance(r378, VGroup) else VGroup(r378)
        strikes = VGroup(*[strike(p, S.GREY, 3) for p in r378_parts])
        err = erratum_tag("erratum · names, not ids").next_to(card2, DOWN, buff=0.3).align_to(card2, LEFT)
        after = grey_chip("listed after a recent run").next_to(err, DOWN, buff=0.2).align_to(card2, LEFT)
        cost = cost_tag("private repo: paid plan · public: free").next_to(after, DOWN, buff=0.45).align_to(card2, LEFT)
        pro = grey_chip("GitHub Pro: Student Developer Pack").next_to(cost, DOWN, buff=0.2).align_to(card2, LEFT)
        pick_h = label("Status checks that are required", 20, S.GREY)
        pick_h.next_to(cbs, DOWN, buff=0.45).align_to(cbs, LEFT)
        picks = VGroup()
        for nm in JOB_ROWS:
            r = VGroup(check_mark(0.22, PASS, stroke=3.5), label(nm, 20, INK)).arrange(RIGHT, buff=0.2)
            picks.add(r)
        picks.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(pick_h, DOWN, buff=0.25).align_to(pick_h, LEFT)
        picks.shift(RIGHT * 0.3)
        with self.voiceover(SAY[2]) as vo:
            self.play(track(tr, 2), FadeOut(today), run_time=0.5)
            self.remove(today)
            self.play(Transform(card.frame, card2.frame), Transform(card.head, card2.head),
                      FadeOut(VGroup(*[v for k, v in rows.items() if k != 378])),
                      ReplacementTransform(rows[378], r378), run_time=0.8)
            self.remove(card, *card.get_family())
            self.add(card2)
            vo.wait_until("Then pick the checks")
            self.play(FadeIn(pick_h, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("A small slip")
            self.play(LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.3), FadeIn(err, shift=UP * 0.15),
                      run_time=0.7)
            vo.wait_until("the picker lists jobs by their names")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in picks], lag_ratio=0.25), run_time=0.9)
            vo.wait_until("like Lint and Format Check")
            self.play(Indicate(picks[0][1], color=PASS, scale_factor=1.08), run_time=0.6)
            vo.wait_until("and Unit Tests")
            self.play(Indicate(picks[1][1], color=PASS, scale_factor=1.08), run_time=0.6)
            vo.wait_until("not the README's IDs")
            self.play(Indicate(r378, color=S.GREY, scale_factor=1.04), flash_tag_anim(err), run_time=0.6)
            vo.wait_until("They appear only after a recent run")
            self.play(FadeIn(after, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("On a private repository")
            self.play(FadeIn(cost, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(pro, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("needs a paid plan")
            flash_tag(self, cost)

        # ========================================================== 3. a branch, then the PR
        full = readme_code([n for n in range(384, 397) if README_SRC[n - 1].strip()], where="lines 383–396")
        at_top_left(full)
        shown = shown_tag().next_to(full.frame.get_corner(UR), DL, buff=0.12)
        r385 = full.rows[385]
        bar385 = hl_bar(r385, TURN, 0.22)
        tl = TriggerLanes(lanes=("main", "feature/test-protection"), lane_w=10.4, pitch=1.0, meter=False)
        dx = -6.4 - tl.get_left()[0]
        dy = -3.45 - tl.get_bottom()[1]
        tl.shift(np.array([dx, dy, 0]))
        tl.lx0 += dx
        tl.lx1 += dx
        nothing = grey_chip("no run").next_to(tl.runners["feature/test-protection"], RIGHT, buff=0.3)
        with self.voiceover(SAY[3]) as vo:
            left = VGroup(card2, strikes, err, after, cost, pro, page, ill, add_rule, field, cbs, pick_h, picks)
            self.play(track(tr, 3), FadeOut(left, shift=DOWN * 0.2), run_time=0.6)
            self.remove(left, *left.get_family())
            self.play(FadeIn(full, shift=DOWN * 0.15), FadeIn(shown), run_time=0.6)
            vo.wait_until("git checkout, dash b")
            self.add_foreground_mobject(r385)
            self.play(FadeIn(bar385), r385.animate.set_color(TURN), run_time=0.5)
            self.remove_foreground_mobject(r385)
            vo.wait_until("Pushing that branch starts nothing")
            self.play(FadeIn(tl, shift=UP * 0.2), run_time=0.5)
            tl.push(self, "feature/test-protection")
            self.play(Indicate(tl.runners["feature/test-protection"], color=S.GREY, scale_factor=1.15),
                      FadeIn(nothing, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("the run starts when you open the pull request")
            pr_arrow(self, tl, "feature/test-protection", "main")
            tl.pr_fire(self)

        # ========================================================== 4. def broken: still 11 passed
        cmp4 = readme_code([388], gaps={388: 0.42})
        at_top_left(cmp4)
        t = laptop_term(8)
        bar_tags = []
        err388 = erratum_tag().next_to(cmp4.frame, RIGHT, buff=0.3)
        with self.voiceover(SAY[4]) as vo:
            others = VGroup(*[v for k, v in full.rows.items() if k != 388], bar385, shown)
            self.play(track(tr, 4), FadeOut(VGroup(tl, nothing), shift=DOWN * 0.2), FadeOut(others),
                      Transform(full.frame, cmp4.frame), Transform(full.head, cmp4.head),
                      full.rows[388].animate.move_to(cmp4.rows[388]), run_time=0.8)
            self.remove(full, tl, nothing, *full.get_family(), *tl.get_family(), *others.get_family())
            self.add(cmp4)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.4)
            type_capture(self, t, C51, type_time=1.6)
            self.play(Indicate(substring(cmp4.rows[388], "def broken"), color=TURN, scale_factor=1.1), run_time=0.5)
            bare_prompt(self, t)
            self.play(track(tr, 4, True), run_time=0.4)
            ln = type_capture(self, t, C52, type_time=0.9)[0]
            bar_tags.append(extra_pin(self, t, ln))
            out(self, t, [C52.line(2), "…", C52.line(61)], run_time=0.5)
            vo.wait_until("An extra run in the image")
            ln = type_capture(self, t, C53, type_time=1.2)[0]
            bar_tags.append(extra_pin(self, t, ln))
            o = out(self, t, [L53_15, "…", (L53_29, TURN)], run_time=0.5)
            vo.wait_until("still says 11 passed")
            self.play(Indicate(o[-1], color=TURN, scale_factor=1.08), Indicate(o[0], color=TURN, scale_factor=1.05),
                      FadeIn(err388, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("because pytest only collects")
            resize(self, t, 3)
            ini = code("pytest.ini", 6, 8)
            ini.move_to([0, (cmp4.get_bottom()[1] + strip_top()) / 2, 0])
            self.play(FadeIn(ini, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("start with test")
            bar8 = line_bar(ini.code, 2, TURN, 0.25)
            self.play(FadeIn(bar8), Indicate(code_span(ini.code, 2, "test_*"), color=TURN, scale_factor=1.15),
                      run_time=0.7)

        # ========================================================== 5. test_broken: 1 failed
        r388 = cmp4.rows[388]
        old = substring(r388, "def broken")
        fix = mono("def test_broken", CARD_SIZE, PASS)
        fix.next_to(old, UP, buff=0.12).align_to(old, LEFT)
        st_old = strike(old, S.GREY, 3)
        commit_c = grey_chip("commit the corrected line").move_to(cmp4.head)
        commit_c.shift(RIGHT * (cmp4.frame.get_right()[0] - 0.2 - commit_c.get_right()[0]))
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(ini, bar8), shift=DOWN * 0.2), run_time=0.4)
            self.remove(ini, bar8)
            resize(self, t, 8, run_time=0.6)
            restored = grey_chip("test file restored")
            under_term(t, restored, buff=0.1)
            self.play(FadeIn(restored, shift=DOWN * 0.1), run_time=0.3)
            ln = type_capture(self, t, C55, type_time=1.2)[-1]
            bar_tags.append(extra_pin(self, t, ln))
            bare_prompt(self, t)
            rebuilt = grey_chip("rebuilt").move_to(restored).align_to(restored, RIGHT)
            self.play(ReplacementTransform(restored, rebuilt), run_time=0.3)
            vo.wait_until("Now 1 failed")
            type_capture(self, t, C57, type_time=0.9)
            o = out(self, t, [(L57_28, ERR), L57_37, (L57_38, ERR)], run_time=0.5)
            self.play(Indicate(o[-1], color=ERR, scale_factor=1.08), run_time=0.6)
            vo.wait_until("That's the one")
            self.play(Create(st_old), FadeIn(fix, shift=DOWN * 0.1), run_time=0.6)
            self.play(FadeIn(commit_c, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("with protection on")
            self.play(Indicate(substring(o[0], "FAILED"), color=ERR, scale_factor=1.15), run_time=0.6)
            vo.wait_until("the merge button stays locked")
            self.play(Circumscribe(o[-1], color=ERR, buff=0.06), run_time=0.8)

        # ========================================================== 6. push, PR, locked merge
        c6 = readme_code([391, 392, 393])
        c6.move_to([LEFT_X + c6.width / 2, 0.6, 0])
        shown6 = shown_tag().next_to(c6.frame, RIGHT, buff=0.3).align_to(c6.frame, UP)
        c6_top = c6.copy()
        at_top_left(c6_top)
        bars6 = {n: hl_bar(c6.rows[n], TURN, 0.22) for n in (391, 392, 393)}
        prp = gh_page("Pull request · feature/test-protection → main", page_w=8.2, page_h=2.55)
        prp.shift(np.array([LEFT_X - prp.get_left()[0], c6_top.get_bottom()[1] - 0.35 - prp.get_top()[1], 0]))
        chk = VGroup(state_mark("failure", 0.32), label("Unit Tests", 22, INK),
                     grey_chip("required")).arrange(RIGHT, buff=0.25)
        chk.move_to(prp.body).align_to(prp.body, LEFT).shift(UP * 0.3)
        mtxt = label("Merge pull request", 20, S.GREY)
        lk = lock_glyph(0.3)
        mg = VGroup(lk, mtxt).arrange(RIGHT, buff=0.2)
        mbtn = RoundedRectangle(width=mg.width + 0.5, height=0.5, corner_radius=0.1, stroke_color=S.GREY,
                                stroke_width=2).set_fill(S.GREY_DARK, 0.4)
        mg.move_to(mbtn)
        merge = VGroup(mbtn, mg).next_to(chk, DOWN, buff=0.3).align_to(chk, LEFT)
        VGroup(chk, merge).move_to(prp.body).align_to(prp.body, LEFT)
        assert merge.get_bottom()[1] > prp.frame.get_bottom()[1] + 0.12, merge.get_bottom()
        ill6 = illustration_tag().next_to(prp.frame, RIGHT, buff=0.3).align_to(prp.frame, UP)
        turn = your_turn().next_to(ill6, DOWN, buff=0.3).align_to(ill6, LEFT)
        fork = grey_chip("fork: set base repository to <you>/cheese-app-ci-cd")
        fork.next_to(prp.frame, DOWN, buff=0.25).align_to(prp.frame, LEFT)
        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(t, err388, commit_c, rebuilt, *[x for x in bar_tags if x is not None])
            self.play(track(tr, 5), FadeOut(gone, shift=DOWN * 0.3), run_time=0.6)
            self.remove(gone, *gone.get_family())
            frag = VGroup(cmp4, st_old, fix)
            self.play(ReplacementTransform(frag, c6), FadeIn(shown6), run_time=0.7)
            for n, cue in ((391, "git add dot"), (392, "git commit, dash m"), (393, "and git push origin")):
                vo.wait_until(cue)
                self.add(bars6[n], c6.rows[n])
                self.play(FadeIn(bars6[n]), Indicate(c6.rows[n], color=TURN, scale_factor=1.04), run_time=0.6)
            vo.wait_until("Open the pull request on GitHub")
            self.play(track(tr, 6), FadeOut(VGroup(*bars6.values())), FadeOut(shown6),
                      c6.animate.move_to(c6_top), run_time=0.6)
            self.remove(*bars6.values(), shown6)
            self.play(FadeIn(VGroup(prp, chk, merge), shift=UP * 0.2), FadeIn(ill6), run_time=0.6)
            vo.wait_until("the merge stays locked")
            self.play(Indicate(chk, color=ERR, scale_factor=1.06), run_time=0.6)
            self.play(Wiggle(lk, scale_value=1.3), Indicate(mtxt, color=S.GREY, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Pause and try it on yours")
            self.play(FadeIn(turn, shift=LEFT * 0.15), FadeIn(fork, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, turn)
            vo.wait_until("Here, git checkout puts the test file back")
            pr_all = VGroup(prp, chk, merge, ill6, turn, fork)
            self.play(FadeOut(pr_all, shift=DOWN * 0.2), run_time=0.5)
            self.remove(pr_all, *pr_all.get_family())
            t3 = laptop_term(3)
            self.play(FadeIn(t3, shift=UP * 0.2), run_time=0.4)
            ln = type_capture(self, t3, C58, type_time=1.4)[-1]
            t3_tag = extra_pin(self, t3, ln)
            bare_prompt(self, t3)

        everything = VGroup(t3, c6, tr, *([t3_tag] if t3_tag is not None else []))
        self.play(FadeOut(everything), run_time=0.6)
        self.remove(everything, *everything.get_family())
        self.wait(0.3)


def flash_tag_anim(tg, color=None):
    """ANIM: the words of a tag flash (its filled box stays put, so the word stays readable)."""
    return Indicate(tg.text, color=color or tg.text.get_color(), scale_factor=1.12)

