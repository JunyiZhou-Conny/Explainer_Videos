"""S06 · Push to a repo of your own (AC215 L21, part 1). Tracker P5 4 → 6 (README Part 5 · "Push to
GitHub", README.md:344–348). No lecture tag (script.md has no LECTURE line in S06).

Beats (script.md "## S06", one voiceover block each):
0. TRACKER P5 4 · extra. Full-width `laptop` terminal at `student@laptop:~$`. A GREY card above it:
   "L09 folder in the way? …" (git reset --hard b8458ff drops L09's commit), flashed on "that one has
   the Black fix committed"; on "would come out green" a GREEN dashed chip "your L09 folder: first
   run green" beside it. `git clone https://github.com/dlops-io/cheese-app-ci-cd.git` (extra,
   folds) → laptop/02:2; `cd cheese-app-ci-cd` (no output) → the prompt changes, its path flashes
   YELLOW; `git status` (extra) → laptop/14:2–5, line 5 GREEN. `▶ your turn` on the clone's first row,
   held ~2 s (the viewer's first command).
1. GREY chip "your prompt shows your own user" over the terminal, the user@host of the prompt
   flashes. `git ls-remote …` (extra, folds) → laptop/01:3 crop7, GREEN; `git log -3 --format='%h %ci
   %s'` (extra) → laptop/03:2–4, lines 2–3 YELLOW; GREY chips "undid it" beside line 2 (b8458ff) and "planted it · → part 2" beside
   line 3 (c3b227f planted math.sqrt(2 * z), b8458ff reverted it: digest.md:781).
2. TRACKER P5 4. The terminal clears to 6 rows; README(344–348) card top right ("Push to GitHub"
   and its three commands; each row flashes as typed). `git add .` → the prompt returns. TRACKER P5
   5. `git commit -m "Add CI pipeline"` → laptop/11:2–5, line 5 RED, an "exit 1" badge beside it.
3. The terminal shrinks to a 3-row strip. GREY `erratum` tag under the card, line 347 ringed GREY:
   "erratum · already committed in a clone or fork". Left: the clone's history (1a5e363 → c3b227f →
   b8458ff), a GREEN `.github/workflows/ci.yml` chip settles on b8458ff, "already there".
4. TRACKER P5 6 · extra. Card, tag and history go (the card into the tracker's caption); the
   terminal grows to 6 rows: `git remote -v` (extra) → laptop/13:2–3, both `dlops-io/cheese-app-ci-cd`
   ORANGE. The terminal shrinks to a strip; a GREY laptop, a PINK push arrow to an ORANGE box
   "dlops-io/cheese-app-ci-cd · the course's"; a dot bounces back and a RED stamp "permission
   denied" lands (no terminal output for it).
5. The strip and the laptop leave; the ORANGE box slides aside (top left). Two BLUE boxes: "fork it
   on GitHub" (a GREY "fork" arrow from the ORANGE box; chip "Actions tab → enable workflows") and
   "new empty repo" (chips "empty: no README · no license · no .gitignore", "HTTPS + token? it needs
   the workflow scope"). Under both, a GREY code card `git remote set-url origin \\ <YOUR_REPO_URL>`
   (tag "shown, not run"), `<you>` YELLOW on "your own address"; YELLOW `▶ your turn` beside it and
   the GREY chip "asked to sign in? a personal access token or gh auth login · never your password",
   held ~4.5 s after the narration (it is not spoken).
6. The two BLUE boxes merge into one BLUE "your repository" box, top right; the rest leaves. The
   terminal returns (7 rows, ~/cheese-app-ci-cd): `git init --bare -b main …` (extra, folds) →
   laptop/20:2 wrap; `git remote set-url origin /home/student/…` (extra, folds) → no output. GREY
   chip on the box: "stand-in for your GitHub repository".
7. TRACKER P5 6. `git push` → laptop/22:2–3 (line 2 GREY, line 3 GREEN); GREY chip over the
   terminal "on GitHub: more lines first, same last line". The terminal shrinks to a strip; a GREY
   laptop, a PINK arrow and a dot fly into "your repository", a PINK spark with the chip "event · run
   1", a TEAL `cheese-app-api:b8458ff…` chip forms under it. `▶ your turn` beside `git push`.
8. The drawing clears (the strip stays; its your-turn tag leaves with the card in); a BLUE "your fork" box comes in, the
   laptop's dashed GREY push arrow reaches it, chip "Everything up-to-date · no run". On "To get run 1
   anyway" a GREY code card `git commit --allow-empty -m "Trigger CI"` / `git push` (tag "not in
   README · shown, not run"; exercise-checks C3), YELLOW `▶ your turn` on "then git push"; on "Or
   wait" a dashed GREY arrow to the dashed chip "or wait: first run in part 2". After
   the narration, fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ the real sources (checked)
C01, C02, C03 = capture("01"), capture("02"), capture("03")
C10, C11, C13, C14 = capture("10"), capture("11"), capture("13"), capture("14")
C20, C21, C22 = capture("20"), capture("21"), capture("22")
assert C02.cmd == "git clone https://github.com/dlops-io/cheese-app-ci-cd.git" == f"git clone {COURSE_URL}"
assert C02.at(2) == ["Cloning into 'cheese-app-ci-cd'..."]
assert C14.cmd == "git status" and C14.line(5) == "nothing to commit, working tree clean"
assert C01.cmd == f"git ls-remote {COURSE_URL}"
LS_MAIN = crop(C01.line(3))
assert LS_MAIN.startswith("b8458ff…") and LS_MAIN.endswith("refs/heads/main"), LS_MAIN
assert C03.cmd == "git log -3 --format='%h %ci %s'"
assert C03.line(2).startswith("b8458ff") and C03.line(2).endswith("demo class 1")
assert C03.line(3).startswith("c3b227f") and C03.line(3).endswith("demo class 1")
assert C10.cmd == "git add ." == readme(346) and C10.lines == []
assert C11.cmd == 'git commit -m "Add CI pipeline"' == readme(347) and C11.exit == 1
assert C11.line(5) == "nothing to commit, working tree clean"
assert C13.cmd == "git remote -v" and all(COURSE_REPO in C13.line(n) for n in (2, 3))
assert C20.cmd == "git init --bare -b main /home/student/github-standin/student/cheese-app-ci-cd.git"
assert C20.line(2).startswith("Initialized empty Git repository in /home/student/github-standin/")
assert C21.cmd == "git remote set-url origin /home/student/github-standin/student/cheese-app-ci-cd.git"
assert C21.lines == []
assert C22.cmd == "git push" == readme(348)
assert C22.line(3) == " * [new branch]      main -> main", C22.line(3)
assert readme_lines(344, 344)[0][1] == "Push to GitHub"
SET_URL = ("git remote set-url origin \\", "    " + YOUR_REPO_URL)
# the fork route's empty commit (SAY[8]; verified in assets/exercise-checks row C3, not in the README)
EMPTY_COMMIT = ('git commit --allow-empty -m "Trigger CI"', "git push")

ART_Y = 0.55          # the drawings' row over a 3-row strip (y in [-1.3, 2.8])


# ------------------------------------------------------------------ local helpers
def bar_tag(scene, t: Terminal, tg):
    """PLAYS: a row-sized tag on the terminal's title bar (replacing the one there)."""
    old = getattr(t, "bar_tag", None)
    on_bar(t, tg)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
        scene.remove(old)
    else:
        scene.play(FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    t.add(tg)
    t.bar_tag = tg
    return tg


def clear_bar(scene, t: Terminal, *extra):
    """PLAYS: the title-bar tag (if any) leaves."""
    old = getattr(t, "bar_tag", None)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), *extra, run_time=0.3)
        scene.remove(old)
        t.bar_tag = None
    elif extra:
        scene.play(*extra, run_time=0.3)


def mark_extra(scene, t: Terminal, line):
    """PLAYS: the row tag 'extra' beside a typed command (its last row), or on the title bar when
    the row leaves no room. Returns the tag."""
    tg = beside(extra_row(), line, buff=0.4)
    if tg.get_right()[0] <= t.box.get_right()[0] - 0.12:
        clear_bar(scene, t)
        pin(scene, line, tg)
        return tg
    return bar_tag(scene, t, extra_row())


def clear_lines(scene, t: Terminal, *extra, run_time: float = 0.4):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(VGroup(*gone)), *extra, run_time=run_time)
    scene.remove(*gone)


def note_card(rows, color=S.GREY, size: float = 20) -> VGroup:
    """A GREY card of short label rows (strings, or (string, colour, 'mono'|'label'))."""
    items = []
    for r in rows:
        if isinstance(r, str):
            items.append(label(r, size, INK))
        else:
            s, col, kind = r
            items.append(mono_line(s, size, col) if kind == "mono" else label(s, size, col))
    body = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    fr = box(body.width + 0.5, body.height + 0.36, color, fill=S.GREY_DARKER, fill_opacity=1)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.body = fr, body
    return g


def repo_box(top: str, sub: str | None, color, mono_top: bool = True, box_w: float | None = None) -> VGroup:
    """A rounded repository box: a name (mono) and a GREY sub-line. .frame .text"""
    t1 = mono(top, 22, color) if mono_top else label(top, 24, color)
    rows = VGroup(t1) if sub is None else VGroup(t1, label(sub, 20, S.GREY)).arrange(DOWN, buff=0.1)
    fr = box(box_w or rows.width + 0.6, rows.height + 0.4, color, fill_opacity=0.12, radius=0.18)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.text = fr, rows
    return g


def stamp(text: str) -> VGroup:
    """A RED rubber stamp (outlined, slightly tilted)."""
    t = label(text, 26, ERR)
    b = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.3, corner_radius=0.08,
                         stroke_color=ERR, stroke_width=4).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t).rotate(8 * DEGREES)
    g.box, g.text = b, t
    return g


class PushIt(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S06"] == 9, len(SAY)

        # ========================================================== 0. a fresh clone
        tr = tracker_p5(4, True)
        t = term(P_HOME, rows=9)
        l09 = note_card(["L09 folder in the way? Clone into another folder,",
                         ("or in it: git reset --hard b8458ff", INK, "mono"),
                         ("(drops L09's commit)", S.GREY, "label")])
        l09.next_to(t.box, UP, buff=0.25).align_to(t.box, RIGHT)
        past = dashed_chip("your L09 folder: first run green", color=PASS).next_to(l09, LEFT, buff=0.35)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(t, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("Start from a fresh clone")
            self.play(FadeIn(l09, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("that one has the Black fix committed")
            self.play(Circumscribe(l09.body[1], color=TURN, buff=0.08), run_time=0.9)
            vo.wait_until("and your first run would come out green")
            self.play(FadeIn(past, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(past.text, color=PASS, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Clone, change into the folder")
            ln = type_capture(self, t, C02, type_time=1.0)[0]
            mark_extra(self, t, ln)
            out(self, t, C02.at(2), run_time=0.4)
            vo.wait_until("change into the folder")
            type_cmd(self, t, "cd cheese-app-ci-cd", type_time=0.5)
            cd_prompt(self, t, P_LAPTOP)
            vo.wait_until("and git status")
            st_ln = type_capture(self, t, C14, type_time=0.4)[0]
            mark_extra(self, t, st_ln)
            rows = out(self, t, [C14.line(2), C14.line(3), (C14.line(5), PASS)], run_time=0.5)
            vo.wait_until("says the tree is clean")
            self.play(Indicate(rows[-1], color=PASS, scale_factor=1.04), run_time=0.7)
            # the clone is the viewer's first command: mark it and hold it before it scrolls away
            head_row = ln.rows[0] if hasattr(ln, "rows") else ln      # 'git clone \\' (folded): room there
            cl_turn = beside(turn_row(), head_row, buff=0.4)
            pin(self, head_row, cl_turn)
            flash_tag(self, cl_turn)
            self.wait(1.8)

        # ========================================================== 1. two extra checks
        own = grey_chip("your prompt shows your own user").next_to(t.box, UP, buff=0.25).align_to(t.box, LEFT)
        user = substring(st_ln, "student@laptop")
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(l09), FadeOut(past), FadeIn(own, shift=DOWN * 0.15), run_time=0.5)
            self.remove(l09, past)
            self.play(Indicate(user, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Two extra checks first")
            self.play(FadeOut(own), run_time=0.3)
            self.remove(own)
            ls = type_capture(self, t, C01, type_time=1.0)[0]
            mark_extra(self, t, ls)
            vo.wait_until("the pinned commit is still the head")
            head = out(self, t, [(LS_MAIN, PASS)], run_time=0.4)[0]
            self.play(Indicate(substring(head, "b8458ff…"), color=PASS, scale_factor=1.12), run_time=0.6)
            vo.wait_until("and the last two commits")
            lg = type_capture(self, t, C03, type_time=0.7)[0]
            mark_extra(self, t, lg)
            logs = out(self, t, [(C03.line(2), TURN), (C03.line(3), TURN), C03.line(4)], run_time=0.5)
            self.play(Indicate(VGroup(substring(logs[0], "demo class 1"), substring(logs[1], "demo class 1")),
                               color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("The second undid a bug")
            # newest first: b8458ff (row 0) undid the bug that c3b227f (row 1) planted (digest.md:781)
            undid = beside(row_tag("undid it"), logs[0], buff=0.4)
            planted = beside(row_tag("planted it · → part 2"), logs[1], buff=0.4)
            assert planted.get_right()[0] <= t.box.get_right()[0] - 0.12, planted.get_right()
            self.play(Circumscribe(logs[0], color=TURN, buff=0.06), run_time=0.8)
            pin(self, logs[0], undid, anim=FadeIn(undid, shift=LEFT * 0.1))
            pin(self, logs[1], planted, anim=FadeIn(planted, shift=LEFT * 0.1))
            self.play(Indicate(substring(logs[1], C03.line(3)[:7]), color=TURN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("we'll run it later")
            flash_tag(self, planted)

        # ========================================================== 2. the README's block
        card = readme_panel(344, 348)
        card.align_to(np.array([6.3, 0, 0]), RIGHT).align_to(np.array([0, 2.7, 0]), UP)
        with self.voiceover(SAY[2]) as vo:
            clear_bar(self, t)
            clear_lines(self, t, track(tr, 4, False))
            resize(self, t, 6, run_time=0.6)
            vo.wait_until("Now the README block")
            self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.6)
            self.play(Indicate(card.rows[344], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Git add dot")
            self.play(Indicate(card.rows[346], color=TURN, scale_factor=1.1), run_time=0.5)
            type_capture(self, t, C10, type_time=0.4)
            vo.wait_until("no output")
            bare_prompt(self, t)
            vo.wait_until("Then git commit")
            self.play(track(tr, 5), Indicate(card.rows[347], color=TURN, scale_factor=1.06), run_time=0.6)
            type_capture(self, t, C11, type_time=0.9)
            vo.wait_until("And Git answers")
            res = out(self, t, [C11.line(2), C11.line(3), (C11.line(5), ERR)], run_time=0.5)
            nothing = res[-1]
            badge = beside(exit_badge(1), nothing, buff=0.4)
            pin(self, nothing, badge)
            self.play(Indicate(nothing, color=ERR, scale_factor=1.04), run_time=0.6)

        # ========================================================== 3. a small slip
        err = erratum_tag("erratum · already committed in a clone or fork")
        err.next_to(card, DOWN, buff=0.25).align_to(card, RIGHT)
        ptr = ring(card.rows[347], S.GREY, buff=0.06)
        names = [C03.line(n)[:7] for n in (4, 3, 2)]          # oldest → newest
        dots = VGroup(*[dot(S.GREY, 0.12) for _ in names]).arrange(RIGHT, buff=1.35)
        links = VGroup(*[Line(a.get_right(), b.get_left(), color=S.GREY, stroke_width=3)
                         for a, b in zip(dots[:-1], dots[1:])])
        ids = VGroup(*[mono(n, 20, S.GREY).next_to(d, DOWN, buff=0.18) for n, d in zip(names, dots)])
        cap = label("your clone's history", 20, S.GREY)
        hist = VGroup(links, dots, ids)
        hist.move_to([-3.4, ART_Y - 0.15, 0])
        cap.next_to(hist, DOWN, buff=0.25)
        ci = ok_chip(".github/workflows/ci.yml", mono_font=True).next_to(dots[-1], UP, buff=0.8)
        ci.align_to(dots[-1], RIGHT).shift(RIGHT * 0.6)
        there = label("already there", 20, PASS).next_to(ci, UP, buff=0.12).align_to(ci, RIGHT)
        dx = dots[-1].get_center()[0]
        drop = arrow(np.array([dx, ci.get_bottom()[1] - 0.04, 0]), np.array([dx, dots[-1].get_top()[1] + 0.06, 0]),
                     color=PASS, stroke=2.5)
        with self.voiceover(SAY[3]) as vo:
            resize(self, t, 3, keep=[nothing], run_time=0.6)
            self.add(t)
            vo.wait_until("A small slip")
            self.play(FadeIn(err, shift=UP * 0.15), Create(ptr), run_time=0.5)
            flash_tag(self, err)
            vo.wait_until("in a clone or a fork")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.3),
                      Create(links), FadeIn(ids), FadeIn(cap), run_time=0.9)
            vo.wait_until("the pipeline is already committed")
            self.play(FadeIn(ci, shift=DOWN * 0.3), run_time=0.5)
            self.play(GrowArrow(drop), dots[-1].animate.set_color(PASS), FadeIn(there, shift=UP * 0.1),
                      run_time=0.6)
            vo.wait_until("so there is nothing to add")
            self.play(Indicate(nothing, color=ERR, scale_factor=1.04), Indicate(ci, color=PASS, scale_factor=1.06),
                      run_time=0.8)

        # ========================================================== 4. origin is the course's
        laptop_g = laptop_icon(1.5).move_to([-4.6, ART_Y, 0])
        course = repo_box(COURSE_REPO, "the course's", SHARED).move_to([2.6, ART_Y, 0])
        push_ar = route(laptop_g.get_right() + RIGHT * 0.1, course.get_left() + LEFT * 0.1)
        no = stamp("permission denied").next_to(course, DOWN, buff=0.1).shift(RIGHT * 0.4)
        with self.voiceover(SAY[4]) as vo:
            cap_copy = tr.caption.copy()
            hist_all = VGroup(hist, cap, ci, there, drop)
            self.play(ReplacementTransform(VGroup(card, err, ptr), cap_copy), FadeOut(hist_all),
                      track(tr, 6, True), run_time=0.7)
            self.remove(cap_copy, card, err, ptr, hist_all)
            self.add(tr)
            clear_lines(self, t, run_time=0.3)
            resize(self, t, 6, run_time=0.5)
            vo.wait_until("git remote, dash v")
            rm = type_capture(self, t, C13, type_time=0.5)[0]
            mark_extra(self, t, rm)
            rem = out(self, t, [C13.line(2), C13.line(3)], run_time=0.4)
            vo.wait_until("Origin is still the course's")
            spans = VGroup(*[substring(r, COURSE_REPO) for r in rem])
            self.play(spans.animate.set_color(SHARED), run_time=0.4)
            self.play(Indicate(spans, color=SHARED, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and you can't write to it")
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(laptop_g, shift=RIGHT * 0.2), FadeIn(course, shift=LEFT * 0.2), run_time=0.5)
            self.play(GrowArrow(push_ar), run_time=0.6)
            vo.wait_until("GitHub would refuse")
            d = dot(PASS).move_to(push_ar.get_start())
            self.add(d)
            self.play(bounce(d, course.get_left() + LEFT * 0.2, run_time=1.0))
            self.play(FadeOut(d), FadeIn(no, scale=1.4), push_ar.animate.set_color(ERR), run_time=0.5)
            self.remove(d)
            vo.wait_until("permission denied")
            self.play(Indicate(no.text, color=ERR, scale_factor=1.08), run_time=0.6)

        # ========================================================== 5. a repository you own
        course_to = course.copy().move_to([-3.2, 2.2, 0])
        fork = repo_box("fork it on GitHub", None, GITHUB, mono_top=False).move_to([-3.2, 0.75, 0])
        new = repo_box("new empty repo", None, GITHUB, mono_top=False).move_to([3.2, 0.75, 0])
        fork_ar = arrow(course_to.get_bottom(), fork.get_top(), color=S.GREY, stroke=2.5, buff=0.08)
        fork_lab = label("fork", 20, S.GREY).next_to(fork_ar, RIGHT, buff=0.15)
        fork_chip = grey_chip("Actions tab → enable workflows").next_to(fork, DOWN, buff=0.2)
        new_chips = VGroup(grey_chip("empty: no README · no license · no .gitignore"),
                           grey_chip("HTTPS + token? it needs the workflow scope")).arrange(DOWN, buff=0.12)
        new_chips.next_to(new, DOWN, buff=0.2)
        for g, x in ((fork_chip, -3.2), (new_chips, 3.2)):
            g.move_to([x, g.get_center()[1], 0])
        cc = note_card([(SET_URL[0], INK, "mono"), (SET_URL[1], INK, "mono")], size=22)
        cc.move_to([-1.3, -1.75, 0])
        shown = shown_tag().next_to(cc, RIGHT, buff=0.3).align_to(cc, UP)
        turn = your_turn().next_to(shown, DOWN, buff=0.18).align_to(shown, LEFT)
        you = substring(cc.body[1], "<you>")
        sign = grey_chip("asked to sign in? a personal access token or gh auth login · never your password")
        sign.move_to([0, -3.1, 0])
        with self.voiceover(SAY[5]) as vo:
            gone = VGroup(laptop_g, push_ar, no, t)
            self.play(FadeOut(gone), course.animate.move_to(course_to), run_time=0.7)
            self.remove(gone, *gone.get_family())
            vo.wait_until("Either fork the course's repository")
            self.play(GrowArrow(fork_ar), FadeIn(fork_lab), FadeIn(fork, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("and enable workflows")
            self.play(FadeIn(fork_chip, shift=UP * 0.15), run_time=0.4)
            self.play(Indicate(fork_chip.text, color=INK, scale_factor=1.06), run_time=0.5)
            vo.wait_until("or create a new empty repository")
            self.play(FadeIn(new, shift=DOWN * 0.2), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in new_chips], lag_ratio=0.4), run_time=0.7)
            vo.wait_until("Either way, run git remote set-url origin")
            self.play(FadeIn(cc, shift=UP * 0.2), FadeIn(shown, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("with your own address")
            self.play(you.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(you, color=TURN, scale_factor=1.15), run_time=0.5)
            vo.wait_until("Pause and set yours up")
            self.play(FadeIn(turn, shift=LEFT * 0.1), FadeIn(sign, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, turn)
            self.wait(1.2)
            self.play(Indicate(sign.text, color=INK, scale_factor=1.04), run_time=0.8)   # unspoken advice: hold it
            self.wait(1.5)

        # ========================================================== 6. the stand-in
        yours = repo_box("your repository", None, GITHUB, mono_top=False).move_to([4.3, 1.75, 0])
        stand = grey_chip("stand-in for your GitHub repository").next_to(yours, DOWN, buff=0.2)
        stand.align_to(yours, RIGHT)
        t = term(P_LAPTOP, rows=7)
        with self.voiceover(SAY[6]) as vo:
            rest = VGroup(course, fork_ar, fork_lab, fork_chip, new_chips, cc, shown, turn, sign)
            self.play(FadeOut(rest), FadeOut(fork.text), FadeOut(new.text),
                      ReplacementTransform(VGroup(fork.frame, new.frame), yours.frame), run_time=0.8)
            self.play(FadeIn(yours.text), run_time=0.3)
            self.remove(fork, new, yours.frame, yours.text)
            self.add(yours)
            self.remove(rest, *rest.get_family())
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("This recording machine can't push")
            ini = type_capture(self, t, C20, type_time=1.2)[0]
            mark_extra(self, t, ini)
            out(self, t, C20.at(2), wrap=True, run_time=0.5)
            vo.wait_until("so an empty repository on the same machine")
            su = type_capture(self, t, C21, type_time=1.2)[0]
            mark_extra(self, t, su)
            vo.wait_until("stands in for yours")
            bare_prompt(self, t)
            self.play(FadeIn(stand, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, stand)
            vo.wait_until("From now on we just say your repository")
            self.play(Indicate(yours.text, color=GITHUB, scale_factor=1.1), run_time=0.7)

        # ========================================================== 7. git push: run 1
        lap2 = laptop_icon(1.5).move_to([-4.6, ART_Y, 0])
        yours_to = yours.copy().move_to([3.2, ART_Y, 0])
        same = grey_chip("on GitHub: more lines first, same last line")
        with self.voiceover(SAY[7]) as vo:
            clear_bar(self, t)
            self.play(FadeOut(stand), track(tr, 6, False), run_time=0.4)
            self.remove(stand)
            vo.wait_until("Now the README's git push")
            ps = type_capture(self, t, C22, type_time=0.4)[0]
            pushed = out(self, t, [(C22.line(2), S.GREY), (C22.line(3), PASS)], run_time=0.4)
            under_term(t, same)
            self.play(FadeIn(same, shift=DOWN * 0.15), run_time=0.4)
            vo.wait_until("New branch, main to main")
            self.play(Indicate(pushed[-1], color=PASS, scale_factor=1.05), run_time=0.7)
            vo.wait_until("This push is the event")
            self.play(FadeOut(same), run_time=0.3)
            self.remove(same)
            resize(self, t, 3, run_time=0.6)
            ar = route(lap2.get_right() + RIGHT * 0.1, yours_to.get_left() + LEFT * 0.1)
            self.play(FadeIn(lap2, shift=RIGHT * 0.2), yours.animate.move_to(yours_to), run_time=0.6)
            dd = dot(PASS).move_to(ar.get_start())
            self.add(dd)
            self.play(GrowArrow(ar), dd.animate.move_to(ar.get_end() + LEFT * 0.15), run_time=0.8)
            sp = spark().move_to(yours_to.get_corner(UR) + np.array([0.1, 0.1, 0]))
            ev = route_chip("event · run 1", mono_font=False).next_to(yours_to, UP, buff=0.3)
            self.play(FadeOut(dd, scale=0.3), FadeIn(sp, scale=0.4), FadeIn(ev, shift=DOWN * 0.15),
                      Indicate(yours.frame, color=ROUTE, scale_factor=1.04), run_time=0.6)
            self.remove(dd)
            self.add(yours)
            vo.wait_until("and run 1 starts now")
            img = image_chip().next_to(yours_to, DOWN, buff=0.3)
            self.play(FadeIn(img, shift=DOWN * 0.2), run_time=0.6)
            self.play(Indicate(img.text, color=IMAGE, scale_factor=1.08), run_time=0.5)
            vo.wait_until("Pause and push yours")
            turn7 = beside(turn_row(), ps, buff=0.4)
            pin(self, ps, turn7)
            flash_tag(self, turn7)

        # ========================================================== 8. on a fork: no run 1
        lap_to = lap2.copy().move_to([-4.6, 2.0, 0])
        fk = repo_box("your fork", None, GITHUB, mono_top=False).move_to([-0.8, 2.0, 0])
        # the empty-commit route (exercise-checks C3: b8458ff..<new>  main -> main); not in the README
        ec = note_card([(EMPTY_COMMIT[0], INK, "mono"), (EMPTY_COMMIT[1], INK, "mono")], size=22)
        ec.move_to([0, -0.62, 0]).align_to(np.array([-6.2, 0, 0]), LEFT)
        ec_tag = shown_tag("not in README · shown, not run").next_to(ec, UP, buff=0.18).align_to(ec, LEFT)
        ec_turn = your_turn().next_to(ec, RIGHT, buff=0.35)
        assert ec_turn.get_right()[0] <= 6.5 and ec.get_bottom()[1] >= -1.3, (ec_turn.get_right(), ec.get_bottom())
        with self.voiceover(SAY[8]) as vo:
            gone = VGroup(ar, sp, ev, img, yours)
            self.play(FadeOut(gone), lap2.animate.move_to(lap_to), run_time=0.6)
            self.remove(gone, *gone.get_family())
            vo.wait_until("On a fork")
            self.play(FadeIn(fk, shift=DOWN * 0.2), VGroup(*[m for r in pushed for m in r.family_members_with_points()
                                if not isinstance(m, Rectangle)]).animate.set_opacity(0.35), run_time=0.5)
            ghost = route(lap2.get_right() + RIGHT * 0.1, fk.get_left() + LEFT * 0.1, color=S.GREY, dashed=True)
            self.play(Create(ghost), run_time=0.6)
            vo.wait_until("so git push says everything up to date")
            upd = grey_chip("Everything up-to-date · no run").next_to(fk, DOWN, buff=0.3)
            self.play(FadeIn(upd, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(upd.text, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("To get run 1 anyway")
            unpin(self, ps, turn7, FadeIn(ec, shift=UP * 0.2), FadeIn(ec_tag, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("git commit, allow empty")
            self.play(Indicate(substring(ec.body[0], "--allow-empty"), color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("then git push")
            self.play(Indicate(ec.body[1], color=TURN, scale_factor=1.1), FadeIn(ec_turn, shift=LEFT * 0.1),
                      run_time=0.6)
            flash_tag(self, ec_turn)
            vo.wait_until("Or wait")
            nxt = dashed_chip("or wait: first run in part 2")
            nxt.move_to([0, upd.get_center()[1], 0]).align_to(np.array([6.4, 0, 0]), RIGHT)
            assert nxt.get_left()[0] >= upd.get_right()[0] + 0.6, (nxt.get_left(), upd.get_right())
            nxt_ar = route(upd.get_right() + RIGHT * 0.1, nxt.get_left() + LEFT * 0.1, color=S.GREY, dashed=True)
            self.play(Create(nxt_ar), run_time=0.5)
            self.play(FadeIn(nxt, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and your first run then comes")
            self.play(Indicate(nxt.text, color=PAST, scale_factor=1.06), run_time=0.7)
        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
