"""S04 · Clone, and run the app (README Part 1, tracker A1 -> A5).

Beats (script.md, ## S04; one voiceover block each):
0. TRACKER A1 appears with a YELLOW pulse. Laptop terminal (student@laptop:~$) under a README card
   (`README.md · line 20`, "Clone or download from your repository") and the GREY caption "the
   README gives no address; this is the repo". It types the clone (folds) -> laptop/01: 2, then
   `cd cheese-app-ci-cd`; the prompt changes and flashes. `▶ your turn` on the cd row.
1. TRACKER A1 · extra. `ls -la` (extra row tag) -> laptop/03: 5–17. Rings in turn: tests (17),
   pytest.ini (15), .pre-commit-config.yaml (8), Dockerfile (9); GREY caption "three test folders
   live under tests/" beside the tests row.
2. TRACKER A2. `sh docker-shell.sh` -> part1-01: 2–3, …, 17, …, 31–33 and the bare container
   prompt; "at the time of recording" beside the 59.0 s row; `▶ your turn`. The terminal shrinks to
   a 3-row strip; the prompt is copied large and splits into app / 44b7ce455073 / /app with labels.
3. TRACKER A3. uvicorn at the container prompt (capture line 34) -> 35–40, "Application startup
   complete." GREEN. TRACKER A4: strip + a schematic browser (tag `illustration`) with the three
   README URLs as tabs, `▶ your turn`. TRACKER A4 · extra: the browser becomes a laptop terminal
   that types the three curls (each row tagged `extra`, caption "the browser's evidence") ->
   part1-02: 2, part1-03: 2, part1-04: 2 (wrap); the server strip prints 41, 42, 43 (wrap).
4. The distance output enlarges to {"x":3.0,"y":4.0,"distance":5.0,"message":…}; README card
   line 90 with tag `erratum`; CODE(service.py: 45–48) with the `"distance": result` row barred.
5. TRACKER A5. The server terminal returns: 44–49 (^C), `exit` (line 51), laptop prompt. Strip;
   CODE(docker-shell.sh: 15–16) with --rm; TRACKER A5 · extra: `docker ps -a` -> part1-05: 2
   (squeeze), header only; the --rm chip flies beside it. GREY laptop folder, TEAL image box, a
   crossed dashed arrow, caption "not mounted · --reload watches the copy inside". Fade out.

Deviations (reported to the coordinator): the terminals are 20 pt (72 characters a row) so that
ls's .pre-commit-config.yaml row fits; ls -la rows are re-aligned with single spaces like a normal
`ls -la` (the capture's ls pads wider; every field kept); BuildKit's padding before the timing
column is collapsed to two spaces (squeeze-style); the three curl cards are one laptop terminal
(three full-width terminals do not fit above the strip, and a half-width card cannot hold the
commands at 20 pt); CODE(service.py) is 45–48, not 45–50 (line 49 is 79 characters, wider than the
frame at 20 pt, as in S01); the curl captures glue `[exit 0]` to the JSON line: it is cut off.
"""

import re

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer.scene import VoiceScene
from explainer import style as S

from common import (ERR, IMAGE, INK, LAPTOP, NARRATION, P_LAPTOP, P_LAPTOP_HOME, PASS, T_LAPTOP,
                    TOOL, TURN, BOTTOM, bare_prompt, beside, capture, cd_prompt, chip, code,
                    code_span, cross_mark, cut, erratum_tag, extra_row, folder_glyph, file_glyph,
                    illustration_tag, istep, label, line_bar, line_pitch, mono, mono_line, note,
                    outline_box, PANEL, pin, readme, readme_card, resize, ring, squeeze, substring, term,
                    time_row, track, tracker, turn_row, type_cmd, under, unpin, your_turn, MONO)

SAY = NARRATION["S04"]
PT = 20                                   # terminal size: 72 characters a row (see docstring)
SERVICE = "cheese-app-ci-cd/src/api-service/api/service.py"
SHELL = "cheese-app-ci-cd/docker-shell.sh"


def strip_top(rows: int = 3) -> float:
    """Top edge of a `rows`-row 20 pt terminal standing on BOTTOM."""
    return BOTTOM + rows * line_pitch(PT) + 0.85


def ls_align(lines: list[str]) -> list[str]:
    """`ls -la` rows re-aligned the way ls itself prints them (single spaces, numbers right-aligned);
    every field of the capture is kept."""
    rows = [ln.split(None, 8) for ln in lines]
    w = [max(len(r[j]) for r in rows) for j in range(8)]
    out = [f"{r[0]} {r[1]:>{w[1]}} {r[2]:<{w[2]}} {r[3]:<{w[3]}} {r[4]:>{w[4]}} {r[5]} {r[6]:>{w[6]}} "
           f"{r[7]} {r[8]}" for r in rows]
    assert all(a.split() == b.split() for a, b in zip(lines, out))
    return out


def gutter(s: str) -> str:
    """A BuildKit row with its padding before the timing column collapsed to two spaces."""
    t = re.sub(r" {3,}", "  ", s.rstrip())
    assert t.split() == s.split()
    return t


def find_in(line, sub: str) -> VGroup:
    """The glyphs of `sub` in a typed line, or in whichever row of a folded command holds it."""
    for row in getattr(line, "rows", [line]):
        if sub in row.text:
            return substring(row, sub)
    raise KeyError(sub)


def json_line(name: str) -> str:
    """The curl captures have no newline after the JSON: their `[exit 0]` is glued to line 2."""
    s = capture(name).line(2)
    assert s.endswith("[exit 0]"), s
    return s[: s.rindex("[exit")]


class RunTheApp(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)
        clone, ls, shell = capture("01"), capture("03"), capture("part1-01")
        assert shell.cmd == readme(73)

        # ================================================== 0. clone, cd
        tr = tracker("A", 1)
        t = term(P_LAPTOP_HOME, rows=5, title=T_LAPTOP, size=PT)
        card = readme_card(20, "Clone or download from your repository", quote=True)
        card.move_to([0, 1.55, 0])
        gap = note("the README gives no address; this is the repo", S.GREY, 22)
        gap.next_to(card, DOWN, buff=0.35)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), run_time=0.8)
            self.play(Indicate(tr.dots[0], color=TURN, scale_factor=1.8),
                      Indicate(tr.caption, color=TURN, scale_factor=1.08), run_time=0.9)
            vo.wait_until("The README says")
            self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("without an address")
            self.play(FadeIn(gap, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("so here is the repo")
            type_cmd(self, t, clone.cmd, type_time=1.4)
            t.print(self, clone.at(2), run_time=0.4)
            vo.wait_until("then cd into")
            cd_line = type_cmd(self, t, "cd cheese-app-ci-cd", type_time=0.7)
            cd_prompt(self, t, P_LAPTOP)
            vo.wait_until("Pause and run both")
            yt = beside(turn_row(), cd_line)
            pin(self, cd_line, yt)
            self.play(Indicate(yt, color=TURN, scale_factor=1.15), run_time=0.7)

        # ================================================== 1. ls -la (extra)
        rows = ls_align(ls.at((5, 17)))
        with self.voiceover(SAY[1]) as vo:
            unpin(self, cd_line, yt)
            self.play(FadeOut(VGroup(card, gap), shift=UP * 0.2), run_time=0.5)
            self.remove(card, gap)
            resize(self, t, 14, keep=1)
            ls_line = type_cmd(self, t, ls.cmd, type_time=0.4)
            xt = beside(extra_row(), ls_line)
            pin(self, ls_line, xt, anim=AnimationGroup(FadeIn(xt, shift=LEFT * 0.1), track(tr, extra=True)))
            vo.wait_until("Everything today is here")
            out = t.print(self, rows, run_time=1.0, lag=0.08)
            by_name = {r.text.split()[-1]: r for r in out}
            marks = []
            plan = (("tests", INK, "three test folders"), ("pytest.ini", TOOL, "a pytest config"),
                    (".pre-commit-config.yaml", TOOL, "a pre-commit config"),
                    ("Dockerfile", IMAGE, "and the Dockerfile"))
            for name, col, anchor in plan:
                glyphs = substring(by_name[name], name)
                rg = ring(glyphs, col, buff=0.07)
                vo.wait_until(anchor)
                anims = [Create(rg), glyphs.animate.set_color(col)]
                if marks:
                    anims.append(marks[-1].animate.set_stroke(opacity=0.45))
                if name == "tests":
                    cap = VGroup(note("three test folders", S.GREY, 20), note("live under tests/", S.GREY, 20))
                    cap.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
                    row = by_name["tests"]
                    cap.next_to(row.strut, RIGHT, buff=0.5).align_to(row.strut, DOWN).shift(DOWN * 0.05)
                    cap.set_x(rg.get_right()[0] + 0.45 + cap.width / 2)
                    anims.append(FadeIn(cap, shift=LEFT * 0.15))
                self.play(*anims, run_time=0.6)
                marks.append(rg)
            self.play(Indicate(by_name["Dockerfile"], color=IMAGE, scale_factor=1.04), run_time=0.8)

        # ================================================== 2. sh docker-shell.sh
        app_prompt, uvicorn_cmd = shell.istep(34)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(*marks, cap)), run_time=0.4)
            self.remove(*marks, cap)
            resize(self, t, 10, keep=0, extra=(track(tr, 2, extra=False),))
            sh_line = type_cmd(self, t, shell.cmd, type_time=0.8)
            vo.wait_until("It builds the image")
            build = t.print(self, [shell.line(2), gutter(shell.line(3))], run_time=0.5)
            t.print(self, ["…", gutter(shell.line(17)), "…"], run_time=0.9, lag=0.3)
            vo.wait_until("about a minute")
            tt = beside(time_row(), build[1])
            pin(self, build[1], tt)
            self.play(Indicate(substring(build[1], "59.0s"), color=INK, scale_factor=1.2), run_time=0.7)
            vo.wait_until("and drops you into a shell")
            t.print(self, shell.at((31, 33)), run_time=0.6)
            t.set_prompt(app_prompt)
            box_line = bare_prompt(self, t)
            self.play(Indicate(substring(box_line, app_prompt), color=IMAGE, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Pause and run it")
            yt = beside(turn_row(), sh_line)
            pin(self, sh_line, yt)
            self.play(Indicate(yt, color=TURN, scale_factor=1.15), run_time=0.7)

            # the prompt, large, splitting into its three parts
            parts = [("app", "user"), ("@", "sep"), ("44b7ce455073", "user"), (":", "sep"),
                     ("/app", "path"), ("$", "sep")]
            colours = {"user": S.GREEN, "path": S.BLUE, "sep": INK}
            big = VGroup(*[mono_line(s, 40, colours[k]) for s, k in parts]).arrange(RIGHT, buff=0.02)
            big.move_to([0, 1.75, 0])
            app_p, id_p, path_p = big[0], big[2], big[4]
            seps = VGroup(big[1], big[3], big[5])

            def caption(*lines):
                return VGroup(*[label(s, 22, INK) for s in lines]).arrange(DOWN, buff=0.1)

            lab_app = caption("a user the Dockerfile created", "not root")
            lab_id = caption("the container's ID", "new every run")
            lab_path = caption("the working folder")
            targets = {0: -4.3, 2: 0.2, 4: 4.5}
            vo.wait_until("Read the prompt")
            resize(self, t, 3)
            self.play(TransformFromCopy(substring(box_line, app_prompt), big), run_time=1.0)
            vo.wait_until("the user is app")
            self.play(*[big[i].animate.set_x(x) for i, x in targets.items()], FadeOut(seps), run_time=0.8)
            self.remove(seps)
            for lab, part in ((lab_app, app_p), (lab_id, id_p), (lab_path, path_p)):
                lab.next_to(part, DOWN, buff=0.45)
            self.play(FadeIn(lab_app, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("not root")
            self.play(Indicate(lab_app[1], color=INK, scale_factor=1.15), run_time=0.7)
            vo.wait_until("and the ID changes every run")
            self.play(FadeIn(lab_id, shift=UP * 0.15), Indicate(id_p, color=S.GREEN, scale_factor=1.08),
                      run_time=0.8)
            self.play(FadeIn(lab_path, shift=UP * 0.15), run_time=0.6)

        # ================================================== 3. uvicorn; the browser; three curls
        prompt_group = VGroup(app_p, id_p, path_p, lab_app, lab_id, lab_path)
        browser = self.browser()
        illus = illustration_tag().next_to(browser[0], UP, buff=0.12).align_to(browser[0], RIGHT)
        turn_tag = your_turn().next_to(browser[0], RIGHT, buff=0.25).align_to(browser[0], DOWN)
        curl_t = term(P_LAPTOP_HOME, rows=8, title=T_LAPTOP, size=PT, place=False)
        curl_t.shift(np.array([-curl_t.box.get_center()[0], strip_top(3) + 0.15 - curl_t.box.get_bottom()[1], 0]))
        evidence = note("the browser's evidence", S.GREY, 20)
        evidence.move_to([4.2, curl_t.box.get_top()[1] + 0.27, 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(prompt_group), run_time=0.5)
            self.remove(prompt_group)
            resize(self, t, 11, extra=(track(tr, 3),))
            uv_line = istep(self, t, shell.line(34), type_time=1.6)
            assert uvicorn_cmd == readme(82)
            flags = []
            for flag, anchor in (("--host 0.0.0.0", "host 0.0.0.0"), ("--port 9000", "port 9000"),
                                 ("--reload", "with reload")):
                vo.wait_until(anchor)
                rg = ring(find_in(uv_line, flag), INK, buff=0.06, stroke=2.5)
                self.play(Create(rg), run_time=0.45)
                flags.append(rg)
            started = t.print(self, shell.at((35, 40)), run_time=1.0, lag=0.12)
            vo.wait_until("When it says application startup complete")
            done = substring(started[-1], "Application startup complete.")
            self.play(done.animate.set_color(PASS), FadeOut(VGroup(*flags)), run_time=0.4)
            self.remove(*flags)
            self.play(Indicate(done, color=PASS, scale_factor=1.08), run_time=0.7)
            vo.wait_until("open the three README URLs")
            resize(self, t, 3, extra=(track(tr, 4),))
            self.play(FadeIn(browser[0]), FadeIn(illus, shift=DOWN * 0.1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(tab, shift=RIGHT * 0.2) for tab in browser[1]], lag_ratio=0.3),
                      run_time=1.0)
            vo.wait_until("pause and do it")
            self.play(FadeIn(turn_tag, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(turn_tag, color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("Here three curl calls")
            self.play(FadeTransform(VGroup(browser, illus, turn_tag), curl_t), FadeIn(evidence),
                      track(tr, extra=True), run_time=0.8)
            self.remove(browser, illus, turn_tag)
            outs = []
            for k, (name, access) in enumerate((("part1-02", 41), ("part1-03", 42), ("part1-04", 43))):
                cap_k = capture(name)
                ln = type_cmd(self, curl_t, cap_k.cmd, type_time=0.6)
                pin(self, ln, beside(extra_row(), ln), run_time=0.25)
                outs.append(curl_t.print(self, [json_line(name)], run_time=0.35, wrap=k == 2))
                t.print(self, shell.at(access), run_time=0.35, wrap=k == 2)

        # ================================================== 4. the erratum: a JSON object, not 5.0
        dist = outs[2]
        big_json = mono(cut(json_line("part1-04"), '"message":') + "}", 28, INK).move_to([0, 2.15, 0])
        span = big_json[big_json.text.index('"distance"'): big_json.text.index('"distance"') + 14]
        r_card = readme_card(90, "Calculate Euclidean distance (returns 5.0)")
        r_card.move_to([0, 0.75, 0])
        err = erratum_tag().next_to(r_card, RIGHT, buff=0.2)
        panel = code(SERVICE, 45, 48)
        panel.move_to([0, 0, 0]).shift(UP * (-0.45 - panel.get_top()[1]))
        bar = line_bar(panel.code, 3, INK, 0.16)
        dspan = code_span(panel.code, 3, '"distance": result')

        with self.voiceover(SAY[4]) as vo:
            for m in dist:
                curl_t.lines.remove(m)
            self.play(FadeTransform(dist, big_json), FadeOut(curl_t), FadeOut(evidence), FadeOut(t),
                      run_time=1.0)
            self.remove(curl_t, evidence, t)
            vo.wait_until("the README says")
            self.play(FadeIn(r_card, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(err, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Really it returns a JSON object")
            self.play(Indicate(big_json, color=INK, scale_factor=1.04), FadeIn(panel, shift=UP * 0.2),
                      run_time=0.8)
            vo.wait_until("whose distance field is 5.0")
            uline = under(span, INK, stroke=4)
            self.play(Create(uline), FadeIn(bar), run_time=0.6)
            self.play(Indicate(span, color=INK, scale_factor=1.1), Indicate(dspan, color=INK, scale_factor=1.1),
                      run_time=0.8)
            vo.wait_until("as the code shows")
            self.play(Indicate(dspan, color=INK, scale_factor=1.12), run_time=0.8)
        self.wait(1.2)

        # ================================================== 5. ^C, exit, --rm, not mounted
        crop = code(SHELL, 15, 16)
        crop.move_to([0, 1.2, 0])
        rm = code_span(crop.code, 0, "--rm")
        rm_ring = ring(rm, IMAGE, buff=0.06)
        ps = capture("part1-05")
        header = squeeze(ps.at(2))

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(big_json, uline, r_card, err, panel, bar)), run_time=0.5)
            self.remove(big_json, uline, r_card, err, panel, bar)
            self.play(FadeIn(t), track(tr, 5, extra=False), run_time=0.5)
            resize(self, t, 9)
            stop = t.print(self, shell.at((44, 49)), run_time=0.8, lag=0.1)
            self.play(Indicate(substring(stop[0], "^C"), color=INK, scale_factor=1.5), run_time=0.5)
            vo.wait_until("then type exit")
            istep(self, t, shell.line(51), type_time=0.4)
            t.set_prompt(P_LAPTOP)
            bare_prompt(self, t)
            vo.wait_until("Because the shell script used")
            resize(self, t, 3)
            self.play(FadeIn(crop, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("dash dash rm")
            self.play(Create(rm_ring), rm.animate.set_color(IMAGE), run_time=0.6)
            vo.wait_until("an extra docker ps dash a,")
            ps_line = type_cmd(self, t, ps.cmd, type_time=0.6)
            xt = beside(extra_row(), ps_line)
            pin(self, ps_line, xt, anim=AnimationGroup(FadeIn(xt, shift=LEFT * 0.1), track(tr, extra=True)))
            vo.wait_until("confirms it")
            head = t.print(self, header, run_time=0.4)[0]
            flag = chip("--rm", IMAGE, size=20, font=MONO)
            beside(flag, head, buff=0.5)
            self.play(TransformFromCopy(rm, flag), run_time=0.9)
            self.play(Indicate(flag, color=IMAGE, scale_factor=1.15), run_time=0.6)

            # not mounted: the laptop's folder and the copy inside the image
            folder = folder_glyph(1.0, LAPTOP)
            f_name = mono("cheese-app-ci-cd", 20, INK)
            f_who = note("your laptop", S.GREY, 20)
            f_file = VGroup(file_glyph(0.36, LAPTOP), mono("service.py", 20, INK)).arrange(RIGHT, buff=0.12)
            lap = VGroup(folder, f_name, f_who, f_file).arrange(DOWN, buff=0.18)
            lap.move_to([-4.2, 1.0, 0])
            img_box = outline_box(4.6, 2.7, IMAGE, solid=True, fill_opacity=0.08)
            img_title = mono("cheese-app-api-service", 20, IMAGE)
            inner = VGroup(folder_glyph(0.5, IMAGE), mono("/app", 22, INK)).arrange(RIGHT, buff=0.15)
            inner_note = note("a copy, baked in at build", S.GREY, 20)
            img_body = VGroup(img_title, inner, inner_note).arrange(DOWN, buff=0.25)
            img = VGroup(img_box, img_body)
            img_box.move_to([3.6, 1.0, 0])
            img_body.move_to(img_box)
            a, b = lap.get_right() + RIGHT * 0.3, img_box.get_left() + LEFT * 0.25
            link = DashedLine(a, b, dash_length=0.16, color=S.GREY, stroke_width=3)
            link.add_tip(tip_length=0.2)
            cross = cross_mark(0.42, ERR).move_to(link.get_center())
            mount_cap = note("not mounted · --reload watches the copy inside", S.GREY, 22)
            mount_cap.move_to([0, strip_top(3) + 0.42, 0])

            vo.wait_until("One warning that pays off soon")
            self.play(FadeOut(VGroup(crop, rm_ring)), run_time=0.4)
            self.remove(crop, rm_ring)
            self.play(FadeIn(lap, shift=RIGHT * 0.2), FadeIn(img, shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("your files are not mounted")
            self.play(Create(link), run_time=0.7)
            self.play(FadeIn(cross, scale=1.4), run_time=0.4)
            vo.wait_until("The reload flag watches")
            self.play(FadeIn(mount_cap, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(inner, color=IMAGE, scale_factor=1.12), run_time=0.8)
            vo.wait_until("so an edit on your laptop")
            self.play(Wiggle(f_file, scale_value=1.15), run_time=0.8)
            vo.wait_until("changes nothing")
            self.play(Indicate(cross, color=ERR, scale_factor=1.3), run_time=0.6)
            vo.wait_until("until you rebuild")
            self.play(Indicate(img_box, color=IMAGE, scale_factor=1.04), run_time=0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)

    # ------------------------------------------------------------------ pieces
    def browser(self) -> VGroup:
        """A schematic browser (no logos): a window with the three README URLs (lines 88–90) as
        vertical tabs. [0] = window, [1] = the three tabs."""
        win_w, win_h, bar_h = 10.2, 3.5, 0.5
        frame = RoundedRectangle(width=win_w, height=win_h, corner_radius=0.14, stroke_color=S.GREY,
                                 stroke_width=2).set_fill(PANEL, 1)
        bar = Line(frame.get_corner(UL) + DOWN * bar_h, frame.get_corner(UR) + DOWN * bar_h,
                   color=S.GREY_DARK, stroke_width=2)
        dots = VGroup(*[Dot(radius=0.055, color=S.GREY_DARK) for _ in range(3)]).arrange(RIGHT, buff=0.1)
        dots.move_to(frame.get_corner(UL) + np.array([0.35, -bar_h / 2, 0]))
        window = VGroup(frame, bar, dots)
        urls = [re.search(r"`([^`]+)`", readme(n)).group(1) for n in (88, 89, 90)]
        tabs = VGroup()
        for u in urls:
            text = mono(u, 20, INK)
            pill = RoundedRectangle(width=win_w - 0.8, height=0.62, corner_radius=0.12, stroke_color=S.GREY,
                                    stroke_width=1.5).set_fill(S.BG, 1)
            text.move_to(pill).align_to(pill, LEFT).shift(RIGHT * 0.3)
            tabs.add(VGroup(pill, text))
        tabs.arrange(DOWN, buff=0.22)
        g = VGroup(window, tabs)
        tabs.move_to(frame).shift(DOWN * bar_h / 2)
        g.move_to([-0.95, 0.55, 0])
        return g
