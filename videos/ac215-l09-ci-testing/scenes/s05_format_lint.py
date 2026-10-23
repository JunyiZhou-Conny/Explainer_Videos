"""S05 · Formatter vs linter (README Part 2, tracker B1 -> B6).

Beats (script.md, ## S05; one voiceover block each):
0. TRACKER B1 appears; `Lecture 9 · slides 29–31` (top right, until the funnel). Concept card: a
   PURPLE chip "formatter · rewrites" over `def power(base,exponent):` (utils.py:7); a PURPLE loop
   arrow carries the line back onto itself tidied (`def power(base, exponent):`), caption "one
   layout · never changes behavior". A PURPLE chip "linter · reports" with an arrow to a RED list
   of this repo's own findings, one per kind as the narration names it: style (E231, utils.py:7),
   likely bug (F401, 8eb63fc service.py:10), needs a person (E501 147 > 120, digest:194). On
   "Format first, then lint" the badges 1 and 2 land on the chips and the E231 row is struck: the
   formatter already fixed it.
1. TRACKER B1. 20 pt terminal types README:106 -> part2-01: 2, …, 26–27, …, 59. `CACHED` TEAL,
   `naming to … cheese-app-api:local` underlined, `▶ your turn`.
2. TRACKER B2. README:109 (folds) -> part2-02: 2–5, lines 4–5 RED, `▶ your turn`. The terminal
   shrinks to a 3-row strip holding the two findings; CODE(utils.py: 7–14) above it: the comma of
   line 7 and the three blank lines before line 13 RED; GREY chip "left messy on purpose".
3. TRACKER B3. README:112 (folds) -> part2-03: 2–3, …, 12–13, …, 21, 39, …, 42. Line 42 highlights,
   a YELLOW "2?" beside it, `▶ your turn`; then a GREY row tag "no width → 88" on the command and
   line 39 (service.py) ringed.
4. V4 ribbon: service.py:15 as 95 cells; a post at 88 folds it to three rows, the post slides to
   120 and it unfolds; the loop runs twice. Card (tag `erratum`): hook + CI 120
   (.pre-commit-config.yaml:34,43) · this README command: black's default 88 · host flake8
   default: 79. After the SAY, the loop holds for a 5-second silent beat (not a PONDER).
5. TRACKER B4. README:118 -> part2-04: 2–5, …, 37 (wrap). ORANGE row tag "on the host" beside the
   command (it then moves into the terminal's title bar, so `▶ your turn` can take the row);
   black-26.10.1 and flake8-7.4.1 ringed and copied above the terminal as ORANGE chips with the
   tag `at the time of recording`; the GREY PEP 668 chip under them.
6. TRACKER B5: README:121 -> part2-05: 2–4 (wrap); `E501 … (95 > 79` RED, row tag "flake8's
   default: 79". TRACKER B6: README:124 -> part2-06: …, 19, 37, …, 40 (wrap). `▶ your turn` on each.
7. The funnel: CODE(8eb63fc-service.py: 7–13), line 10 `import os` RED; a RED bar "8 findings"
   (flake8 at 120, digest:190) shrinks to 2 as a PURPLE broom labelled `black` sweeps the panel;
   the survivors as RED chips (F401, E501); GREY caption "the class fixed these two by hand".

Deviations (reported to the coordinator): terminals are 20 pt (72 characters a row, as in S04) so
the tags fit beside commands; CODE(8eb63fc-service.py) is 7–13, not 7–14 (line 14 is 95 characters,
wider than the frame at >= 20 pt); the PEP 668 chip sits above the terminal (under the version
chips), since a chip under the command row would cover output; "on the host" moves into the title
bar when `▶ your turn` takes the command row (both do not fit beside it).
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer.scene import VoiceScene
from explainer import style as S

from common import (BOTTOM, ERR, HOST, IMAGE, INK, NARRATION, P_LAPTOP, PASS, TOOL, TURN, T_LAPTOP, beside,
                    capture, chip, code, code_span, erratum_tag, finding_chip, grey_chip, hl_bar,
                    label, line_bar, line_pitch, mono, note, pin, readme, recording_tag, ring,
                    row_tag, resize, step_badge, strike, substring, term, tool_chip, track, tracker,
                    turn_row, type_cmd, under, unpin, lref, FindingsFunnel, Ribbon, MONO)

SAY = NARRATION["S05"]
PT = 20                                       # terminal size: 72 characters a row
UTILS = "cheese-app-ci-cd/src/api-service/api/utils.py"
MESSY = "cheese-app-ci-cd-history/8eb63fc-service.py"


def strip_top20(rows: int) -> float:
    """Top edge of a `rows`-row 20 pt terminal standing on BOTTOM."""
    return BOTTOM + rows * line_pitch(PT) + 0.85


def text_span(t, s: str, sub: str) -> VGroup:
    """The glyphs of `sub` in a Text built from `s` (Text has no glyphs for spaces)."""
    i = s.index(sub)
    start = len(s[:i].replace(" ", ""))
    return VGroup(*t[start:start + len(sub.replace(" ", ""))])


def tail(row) -> VGroup:
    """The glyphs after the last '/' of a wrapped path row (the file name's first part)."""
    return substring(row, row.text[row.text.rindex("/") + 1:])


def find_in(line, sub: str) -> VGroup:
    """The glyphs of `sub` in a typed line, or in whichever row of a folded command holds it."""
    for row in getattr(line, "rows", [line]):
        if sub in row.text:
            return substring(row, sub)
    raise KeyError(sub)


def detach(scene, line, mob):
    """Take a pinned tag off its row without fading it (it stays on the scene on its own)."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    if mob in row.submobjects:
        row.remove(mob)
    scene.add(mob)
    return mob


def broom(label_text: str = "black") -> VGroup:
    """A PURPLE broom (handle, binding, fanned bristles) with a mono tool chip on the handle."""
    handle = Line([0, 1.5, 0], [0, -0.55, 0], color=TOOL, stroke_width=7)
    binding = RoundedRectangle(width=0.62, height=0.2, corner_radius=0.06, stroke_color=TOOL,
                               stroke_width=3).set_fill(TOOL, 0.6).move_to([0, -0.62, 0])
    bristles = VGroup(*[Line([0.26 * u, -0.72, 0], [0.62 * u, -1.55, 0], color=TOOL, stroke_width=4)
                        for u in np.linspace(-1, 1, 9)])
    name = tool_chip(label_text, size=22).move_to([0, 0.55, 0])
    g = VGroup(handle, binding, bristles, name)
    g.name = name
    return g


class FormatterLinter(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)
        build, f8, blk = capture("part2-01"), capture("part2-02"), capture("part2-03")
        pip, f8_local, blk_local = capture("part2-04"), capture("part2-05"), capture("part2-06")
        for cap, n in ((build, 106), (f8, 109), (blk, 112), (pip, 118), (f8_local, 121), (blk_local, 124)):
            assert cap.cmd == readme(n), (cap.cmd, n)

        # ================================================== 0. concept: rewrites vs reports
        tr = tracker("B", 1)
        ref = lref("29–31")
        lx, rx = -3.45, 3.35
        f_chip = tool_chip("formatter · rewrites", size=24).move_to([lx, 1.95, 0])
        l_chip = tool_chip("linter · reports", size=24).move_to([rx, 1.95, 0])
        messy = mono("def power(base,exponent):", 24, INK).move_to([lx, 0.55, 0])
        tidy = mono("def power(base, exponent):", 24, INK).move_to([lx, 0.55, 0])
        comma = text_span(messy, "def power(base,exponent):", ",")
        a = np.array([messy.get_right()[0] + 0.1, messy.get_bottom()[1] - 0.12, 0])
        b = np.array([messy.get_left()[0] - 0.1, messy.get_bottom()[1] - 0.12, 0])
        loop = CurvedArrow(a, b, angle=-2.2, color=TOOL, stroke_width=4, tip_length=0.2)
        same = note("one layout · never changes behavior", S.GREY, 22)
        same.next_to(loop, DOWN, buff=0.3).set_x(lx)
        kinds = (("style", "E231", "missing whitespace after ','"),
                 ("likely bug", "F401", "'os' imported but unused"),
                 ("needs a person", "E501", "line too long (147 > 120 characters)"))
        items = []
        for kind, c, msg in kinds:
            k_lab = note(kind, S.GREY, 20)
            fc = finding_chip(c, msg)
            items.append(VGroup(k_lab, fc).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        f_list = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        f_list.next_to(l_chip, DOWN, buff=0.75).set_x(rx)
        l_arrow = Arrow(l_chip.get_bottom(), f_list.get_top(), buff=0.1, color=TOOL, stroke_width=4,
                        tip_length=0.2, max_tip_length_to_length_ratio=0.35)
        b1 = step_badge(1, TURN).next_to(f_chip, LEFT, buff=0.15)
        b2 = step_badge(2, TURN).next_to(l_chip, LEFT, buff=0.15)
        e231 = items[0][1]
        e231_x = strike(e231, PASS, stroke=4)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.8)
            self.play(Indicate(tr.dots[0], color=TURN, scale_factor=1.8),
                      Indicate(tr.caption, color=TURN, scale_factor=1.08), run_time=0.9)
            vo.wait_until("two tools not to confuse")
            self.play(FadeIn(f_chip, shift=DOWN * 0.2), FadeIn(l_chip, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("A formatter rewrites code")
            self.play(Indicate(f_chip, color=TOOL, scale_factor=1.06), FadeIn(messy, shift=UP * 0.15),
                      run_time=0.8)
            self.play(comma.animate.set_color(ERR), run_time=0.4)
            self.play(Create(loop), run_time=0.9)
            self.play(TransformMatchingShapes(messy, tidy), run_time=0.9)
            vo.wait_until("never changes behavior")
            self.play(FadeIn(same, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("A linter only reports")
            self.play(Indicate(l_chip, color=TOOL, scale_factor=1.06), GrowArrow(l_arrow), run_time=0.8)
            for item, anchor in zip(items, ("style issues", "likely bugs", "things needing a person")):
                vo.wait_until(anchor)
                self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Format first")
            self.play(FadeIn(b1, scale=1.4), Indicate(f_chip, color=TURN, scale_factor=1.06), run_time=0.6)
            self.play(Create(e231_x), e231.animate.set_opacity(0.4), run_time=0.6)
            vo.wait_until("then lint")
            self.play(FadeIn(b2, scale=1.4), Indicate(VGroup(items[1], items[2]), color=ERR, scale_factor=1.04),
                      run_time=0.8)
        self.wait(0.6)

        # ================================================== 1. docker build (all CACHED)
        concept = VGroup(f_chip, l_chip, tidy, loop, same, f_list, l_arrow, b1, b2, e231_x)
        t = term(P_LAPTOP, rows=12, title=T_LAPTOP, size=PT)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(concept), run_time=0.6)
            self.remove(concept, *concept.get_family())
            self.play(FadeIn(t), run_time=0.5)
            b_line = type_cmd(self, t, build.cmd, type_time=1.2)
            vo.wait_until("cheese-app-api tagged local")
            self.play(Indicate(find_in(b_line, "cheese-app-api:local"), color=INK, scale_factor=1.1),
                      run_time=0.7)
            out = t.print(self, build.at(2, "…", (26, 27), "…", 59), run_time=0.9, lag=0.15)
            cached = substring(out[3], "CACHED")
            naming = substring(out[5], "cheese-app-api:local")
            vo.wait_until("Every step says CACHED")
            self.play(cached.animate.set_color(IMAGE), run_time=0.4)
            self.play(Indicate(cached, color=IMAGE, scale_factor=1.25), run_time=0.7)
            vo.wait_until("the shell script already built")
            u_name = under(naming, INK, stroke=3)
            self.play(Create(u_name), run_time=0.6)
            vo.wait_until("Pause and run it")
            yt = beside(turn_row(), b_line)
            pin(self, b_line, yt)
            self.play(Indicate(yt, color=TURN, scale_factor=1.15), run_time=0.7)

        # ================================================== 2. flake8 in the image
        panel = code(UTILS, 7, 14)
        panel.move_to([0, (strip_top20(3) + 0.15 + 2.8) / 2, 0])
        p_comma = code_span(panel.code, 0, ",")
        y9 = panel.code.code_lines[2].get_center()[1]
        y13 = panel.code.code_lines[6].get_center()[1]
        pitch = (y9 - y13) / 4
        blanks = VGroup(*[Rectangle(width=panel.code.background.width - 0.12, height=pitch * 0.82,
                                    stroke_width=0).set_fill(ERR, 0.22)
                          .move_to([panel.code.background.get_center()[0], y9 - pitch * j, 0])
                          for j in (1, 2, 3)])
        c_ring = ring(p_comma, ERR, buff=0.06)
        messy_chip = grey_chip("left messy on purpose")
        messy_chip.move_to([panel.code.background.get_right()[0] - 0.25 - messy_chip.width / 2,
                            panel.code.code_lines[7].get_center()[1], 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(u_name), track(tr, 2), run_time=0.5)
            self.remove(u_name)
            f_line = type_cmd(self, t, f8.cmd, type_time=1.4)
            marks = []
            for sub, anchor in (("flake8", "flake8,"), ("--max-line-length=120", "max line length 120"),
                                ("api/", "on the api folder")):
                vo.wait_until(anchor)
                rg = ring(find_in(f_line, sub), INK, buff=0.05, stroke=2.5)
                self.play(Create(rg), run_time=0.4)
                marks.append(rg)
            vo.wait_until("Pause and run it")
            self.play(FadeOut(VGroup(*marks)), run_time=0.3)
            self.remove(*marks)
            yt2 = beside(turn_row(), f_line.rows[0])       # row 2 is too long for the tag
            pin(self, f_line.rows[0], yt2)
            self.play(Indicate(yt2, color=TURN, scale_factor=1.15), run_time=0.6)
            f_out = t.print(self, f8.at((2, 5)), run_time=0.7)
            vo.wait_until("Two findings in utils.py")
            self.play(f_out[2].animate.set_color(ERR), f_out[3].animate.set_color(ERR), run_time=0.5)
            resize(self, t, 3, keep=[f_out[2], f_out[3]])
            self.play(FadeIn(panel, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("a missing space after a comma")
            self.play(Create(c_ring), p_comma.animate.set_color(ERR),
                      Indicate(substring(f_out[2], "E231"), color=ERR, scale_factor=1.2), run_time=0.7)
            vo.wait_until("too many blank lines")
            self.play(FadeIn(blanks, lag_ratio=0.3), Indicate(substring(f_out[3], "E303"), color=ERR,
                                                               scale_factor=1.2), run_time=0.8)
            vo.wait_until("mess left on purpose")
            self.play(FadeIn(messy_chip, shift=LEFT * 0.15), run_time=0.6)

        # ================================================== 3. black --check --diff in the image
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(panel, c_ring, blanks, messy_chip)), run_time=0.5)
            self.remove(panel, c_ring, blanks, messy_chip)
            resize(self, t, 12, extra=(track(tr, 3),))
            k_line = type_cmd(self, t, blk.cmd, type_time=1.3)
            vo.wait_until("in check and diff mode")
            cd_ring = ring(find_in(k_line, "--check --diff"), INK, buff=0.05, stroke=2.5)
            self.play(Create(cd_ring), run_time=0.5)
            vo.wait_until("Pause and run it")
            yt3 = beside(turn_row(), k_line.rows[0])
            pin(self, k_line.rows[0], yt3, anim=AnimationGroup(FadeIn(yt3, shift=LEFT * 0.1), FadeOut(cd_ring)))
            self.remove(cd_ring)
            k_out = t.print(self, blk.at((2, 3), "…", (12, 13), "…", 21, 39, "…", 42), run_time=1.2, lag=0.12)
            vo.wait_until("It reports 2 files")
            last = k_out[-1]
            bar42 = hl_bar(last, TURN, 0.22)
            self.play(FadeIn(bar42), run_time=0.4)
            q = beside(row_tag("2?", TURN), last, buff=0.3)
            vo.wait_until("not one")
            pin(self, last, q)
            self.play(Indicate(q, color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("gives black no width")
            unpin(self, k_line.rows[0], yt3)
            nw = beside(row_tag("no width → 88", S.GREY), k_line)
            pin(self, k_line, nw)
            vo.wait_until("its default of 88")
            self.play(Indicate(nw, color=INK, scale_factor=1.12), run_time=0.7)
            vo.wait_until("also folds a 95 character line")
            svc = k_out[-3]
            s_ring = ring(substring(svc, "/app/api/service.py"), INK, buff=0.05, stroke=2.5)
            self.play(Create(s_ring), run_time=0.5)
            self.play(Indicate(substring(svc, "service.py"), color=INK, scale_factor=1.12), run_time=0.7)

        # ================================================== 4. the ribbon: 88 folds, 120 unfolds
        rb = Ribbon()
        rb.set_y(1.25)
        r_name = VGroup(mono("service.py:15", 22, INK), note("· 95 characters", S.GREY, 22))
        r_name.arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        r_name.move_to([rb.x0 + r_name.width / 2, rb.y0 + 0.75, 0])
        post = rb.post(88, color=INK)
        rows = [
            VGroup(label("hook + CI: 120", 22, INK), mono(".pre-commit-config.yaml:34,43", 20, S.GREY)),
            VGroup(label("this README command: black's default 88", 22, INK)),
            VGroup(label("host flake8 default: 79", 22, INK)),
        ]
        for r in rows:
            r.arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        frame = RoundedRectangle(width=body.width + 0.8, height=body.height + 0.55, corner_radius=0.16,
                                 stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        card = VGroup(frame, body)
        frame.move_to([0, -1.85, 0])
        body.move_to(frame)
        err = erratum_tag().next_to(frame, UP, buff=0.1).align_to(frame, RIGHT)

        def loop88():
            self.play(rb.move_post(post, 88), run_time=0.8)
            self.play(rb.fold(run_time=1.0))

        def loop120():
            self.play(rb.move_post(post, 120), run_time=0.8)
            self.play(rb.unfold(run_time=1.0))

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(t), FadeOut(q), FadeOut(bar42), FadeOut(s_ring), FadeOut(nw), run_time=0.6)
            self.remove(t, q, bar42, s_ring, nw)
            vo.wait_until("Watch the trap")
            self.play(FadeIn(rb, shift=UP * 0.2), FadeIn(r_name, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("At width 88")
            self.play(FadeIn(post, shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("black folds that line into three")
            self.play(rb.fold(run_time=1.0))
            vo.wait_until("at 120")
            loop120()
            vo.wait_until("The hook and CI here both use 120")
            self.play(FadeIn(frame), FadeIn(rows[0], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("several README commands pass no width")
            self.play(FadeIn(rows[1], shift=UP * 0.15), FadeIn(err, shift=DOWN * 0.1), run_time=0.6)
            loop88()
            vo.wait_until("so the same file gets different answers")
            self.play(FadeIn(rows[2], shift=UP * 0.15), run_time=0.5)
            loop120()
            vo.wait_until("Always pass 120")
            self.play(Indicate(post, color=INK, scale_factor=1.15), Indicate(rows[0][0], color=INK,
                                                                              scale_factor=1.08), run_time=0.8)
        # the silent beat: the loop holds (5 s, not a PONDER card)
        loop88()
        self.wait(0.7)
        loop120()
        self.wait(0.7)

        # ================================================== 5. Option B: pip install on the host
        t = term(P_LAPTOP, rows=9, title=T_LAPTOP, size=PT, width=13.0)   # room for the turn tags
        band_hi, band_lo = 2.25, 1.35
        pep = grey_chip("pip refuses? (PEP 668, Homebrew/Debian) → any venv, or pipx · study guide")
        pep.move_to([0, band_lo, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(rb, r_name, post, card, err)), track(tr, 4), run_time=0.7)
            self.remove(rb, r_name, post, card, err)
            self.play(FadeIn(t), run_time=0.5)
            vo.wait_until("Option B runs the same checks")
            p_line = type_cmd(self, t, pip.cmd, type_time=1.0)
            vo.wait_until("install black and flake8 with pip")
            p_out = t.print(self, pip.at((2, 5), "…", 37), run_time=0.9, lag=0.12, wrap=True)
            host = beside(row_tag("on the host", HOST), p_line)
            vo.wait_until("on the host")
            pin(self, p_line, host)
            self.play(Indicate(host, color=HOST, scale_factor=1.15), run_time=0.6)
            vo.wait_until("26.10.1")
            done = p_out[5]
            vb = substring(done, "black-26.10.1")
            vf = substring(done, "flake8-7.4.1")
            rb1, rf1 = ring(vb, HOST, buff=0.05, stroke=2.5), ring(vf, HOST, buff=0.05, stroke=2.5)
            cb = chip("black-26.10.1", HOST, size=22, font=MONO)
            cf = chip("flake8-7.4.1", HOST, size=22, font=MONO)
            rec = recording_tag()
            vers = VGroup(cb, cf, rec).arrange(RIGHT, buff=0.35).move_to([0, band_hi, 0])
            self.play(Create(rb1), Create(rf1), run_time=0.5)
            self.play(TransformFromCopy(vb, cb), TransformFromCopy(vf, cf), run_time=0.9)
            vo.wait_until("at the time of recording")
            self.play(FadeIn(rec, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("Pause and run it")
            # the host tag moves into the title bar; the command row takes the turn tag
            detach(self, p_line, host)
            bar_y = t.box.get_top()[1] - t.bar_h / 2
            yt5 = beside(turn_row(), p_line)
            self.play(host.animate.move_to([t.box.get_right()[0] - 0.2 - host.width / 2, bar_y, 0]),
                      run_time=0.6)
            pin(self, p_line, yt5)
            self.play(Indicate(yt5, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("If pip refuses")
            self.play(FadeIn(pep, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("use any lecture 3 virtual environment")
            self.play(Indicate(pep.text, color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("the study guide has the one-liner")
            self.play(Indicate(pep, color=S.GREY, scale_factor=1.06), run_time=0.8)

        # ================================================== 6. flake8 and black on the host
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(vers, pep, rb1, rf1)), run_time=0.4)
            self.remove(vers, pep, rb1, rf1)
            grow = (14 - t.rows) * line_pitch(PT)
            resize(self, t, 14, keep=0, extra=(host.animate.shift(UP * grow), track(tr, 5)))
            l5 = type_cmd(self, t, f8_local.cmd, type_time=0.8)
            yt6 = beside(turn_row(), l5, buff=0.3)
            pin(self, l5, yt6)
            vo.wait_until("The local flake8")
            o5 = t.print(self, f8_local.at((2, 4)), run_time=0.7, wrap=True)
            vo.wait_until("at its default of 79")
            e501 = VGroup(substring(o5[0], "E501"), substring(o5[0], "(95 > 79"))
            dflt = beside(row_tag("flake8's default: 79", S.GREY), o5[1])
            self.play(e501.animate.set_color(ERR), run_time=0.4)
            pin(self, o5[1], dflt)
            vo.wait_until("adds a third finding")
            self.play(Indicate(e501, color=ERR, scale_factor=1.15), run_time=0.7)
            vo.wait_until("local black")
            self.play(track(tr, 6), run_time=0.4)
            l6 = type_cmd(self, t, blk_local.cmd, type_time=0.9)
            yt7 = beside(turn_row(), l6)
            pin(self, l6, yt7)
            o6 = t.print(self, blk_local.at("…", 19, 37, "…", 40), run_time=0.9, lag=0.12, wrap=True)
            vo.wait_until("the same two files changed")
            names = []
            for row in o6:                         # the file names, over their wrapped rows
                if row.text.startswith("would reformat"):
                    names.append(tail(row))
                elif not row.text.startswith(("…", "2 files")):
                    names.append(row.glyphs)
            r_files = VGroup(*[under(g, INK, stroke=3) for g in names])
            self.play(Create(r_files), run_time=0.6)
            self.play(Indicate(o6[-1], color=INK, scale_factor=1.04), run_time=0.7)
        self.wait(1.0)

        # ================================================== 7. the funnel: what a formatter can fix
        panel2 = code(MESSY, 7, 13)
        panel2.move_to([0, 0, 0]).shift(UP * (3.3 - panel2.get_top()[1]))
        imp_k = 10 - 7
        imp = code_span(panel2.code, imp_k, "import os")
        imp_bar = line_bar(panel2.code, imp_k, ERR, 0.22)
        ff = FindingsFunnel([8, 2], ["flake8 at 120", "after black"], bar_w=6.5)
        ff.move_to([-0.9, -0.55, 0])
        sweeper = broom()
        p_mid = panel2.code.background.get_center()[1]
        sweeper.move_to([-5.7, p_mid, 0])
        survivors = VGroup(finding_chip("F401", "'os' imported but unused"),
                           finding_chip("E501", "a 147-character line · a string black must not break"))
        survivors.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([0, -2.15, 0])
        by_hand = note("the class fixed these two by hand", S.GREY, 22)
        by_hand.next_to(survivors, DOWN, buff=0.22)
        term_stuff = VGroup(t, host, ref, tr, r_files)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(term_stuff), run_time=0.7)
            self.remove(term_stuff, *term_stuff.get_family())
            self.play(FadeIn(panel2, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("On the messy service.py")
            self.play(Indicate(panel2.header, color=INK, scale_factor=1.08), FadeIn(ff, shift=UP * 0.15),
                      run_time=0.8)
            self.play(FadeIn(imp_bar), imp.animate.set_color(ERR), run_time=0.5)
            vo.wait_until("black sweeps away almost every finding")
            self.play(FadeIn(sweeper, shift=RIGHT * 0.3), run_time=0.4)
            self.play(sweeper.animate.set_x(5.7), ff.step(run_time=1.6), run_time=1.8, rate_func=smooth)
            self.play(FadeOut(sweeper, shift=RIGHT * 0.3), run_time=0.4)
            self.remove(sweeper)
            vo.wait_until("exactly 2 survive")
            self.play(Indicate(ff.count, color=ERR, scale_factor=1.15), run_time=0.7)
            vo.wait_until("an unused import")
            self.play(TransformFromCopy(imp, survivors[0]), run_time=0.9)
            vo.wait_until("which a formatter cannot delete")
            self.play(Indicate(imp, color=ERR, scale_factor=1.15), run_time=0.7)
            vo.wait_until("a long quoted sentence")
            self.play(FadeIn(survivors[1], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("The class fixed both by hand")
            self.play(FadeIn(by_hand, shift=UP * 0.15), run_time=0.6)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
