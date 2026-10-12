"""S10 · uv sync: which Python? (part 2: the constraint in pyproject.toml, the Python uv picks).

Beats (script.md "## S10", one voiceover block each):
 0  TRACKER B9. CODE(pyproject.toml: 1-10) (left, 24 pt). Line 2 gets a GREY "remember this" tag;
    a GREEN brace over lines 7-10, "2 dependencies"; one GREEN bar follows the narration over
    lines 8 / 9; `>=` on line 8 underlined GREEN + "range", `==` on line 9 + "exact"; line 6
    YELLOW, its `>=` "range".
 1  The annotations clear (line 6 stays YELLOW). Right column: GREY chip "this VM: Python 3.11.2"
    (debian12-part-b/00-os.txt line 6), a PURPLE `uv sync` chip and three answer chips.
    PONDER(8 s) after the block: the card covers the panel, the answers stay visible beside it.
 2  The panel shrinks to its line 6 and moves up; the answers line up under it; a 5-row terminal
    strip comes up from the bottom: `uv sync` + ▶ your turn -> 08-uv-sync.txt lines 2-5; "fail?"
    and "use 3.11 anyway?" are crossed, "something else?" ticked; (35.9MiB) GREY underline;
    `3.15.0` "at the time of recording"; `.venv` GREEN; GREY note "no pyproject.toml found? ...".
    (The script's "strip grows to 5 rows": there is no strip before this beat, the 10-line panel
    needs the frame, so the 5-row strip slides in; the panel keeps only line 6.)
 3  V4: the strip shrinks to 3 rows (`uv sync`, Downloading, Using); a number line 3.10 ... 3.16;
    the line-6 text flies down to label the GREEN glow from 3.13 on; uv's own folder (GREY dashed,
    empty) then the system Python (the VM chip) are searched (PINK); a dot drops onto 3.11, label
    `3.11.2 · /usr/bin/python3`, and turns RED outside the glow; a GREY toggle shows Debian 12.
 4  A ghost at 3.13 is crossed out; uv's folder fills (`cpython-3.15 -> cpython-3.15.0`, as in
    24-du.txt) and a PURPLE download arrow drops a GREEN-ringed dot onto 3.15: "newest release in
    range", "3.15.0 · uv-managed", "at the time of recording" (the 35.9 MiB is pointed at in the
    strip's real line instead of being repeated); a GREEN `.venv/bin/python` chip
    links to it in two hops (11-venv-bin.txt line 18: python -> .../cpython-3.15-.../python3.15).
 5  The glow's right end becomes an arrow, "no upper limit"; caption "a constraint is not a pin";
    a caption strip steps through 3.14 (ghost) · 3.15.0 (the dot) · newer (ghost).
 6  The toggle flips to Debian 13; the strip shows debian13-part-b/08-uv-sync.txt lines 2-3 with a
    GREY "Debian 13" tag; the RED dot slides into the glow as `3.13.5 · /usr/bin/python3` (GREEN);
    the download arrow, the 3.15.0 dot and the folder retract; the venv link swings to 3.13.5.
 7  The toggle flips back; the strip and the links clear. A PURPLE chip `uv python pin 3.13`
    (extra · not in the README; RED "not now · exercise B2") writes a GREEN `.python-version` card
    (`3.13`); the line settles lower (the strip's room is free); the glow shrinks to the 3.13
    segment, `3.13.x`; GREY note "pin 3.13.5 → one release". Fade out.

Note: a terminal line whose glyphs were animated (Indicate on a substring) is split in the scene's
list; pin() re-adds the line whole so a tag attached to it is drawn.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import (MONO, box, check_mark, chip, code_panel, code_span, cross_mark,
                              file_glyph, folder_glyph, label, line_bar, mono, substring, tag)
from explainer.scene import VoiceScene

from common import (ERR, INK, LOOKUP, NARRATION, P_REPO, TURN, UV, VENV, VersionLine, capture,
                    excerpt, extra_tag, recorded_tag, term, tracker_b, your_turn)

SAY = NARRATION["S10"]
PB, PB13 = "debian12-part-b", "debian13-part-b"

# ------------------------------------------------------------------ real sources and outputs
TOML = excerpt("pyproject.toml", 1, 10)
TOML6 = excerpt("pyproject.toml", 6, 6)
assert TOML6 == 'requires-python = ">=3.13"'

VM_PY = capture("00-os", PB).pick(5)[0]                       # file line 6
assert VM_PY == "Python 3.11.2"
VM_VER = VM_PY.split()[1]
D13_VER = capture("00-os", PB13).pick(5)[0].split()[1]        # file line 6: Python 3.13.5
assert D13_VER == "3.13.5"

_sync = capture("08-uv-sync", PB)
assert _sync.cmd == "uv sync"
SYNC_OUT = _sync.pick((1, 4))                                 # file lines 2-5
assert SYNC_OUT[0].endswith("(35.9MiB)") and SYNC_OUT[2] == "Using CPython 3.15.0"
_sync13 = capture("08-uv-sync", PB13)
SYNC13_OUT = _sync13.pick((1, 2))                             # file lines 2-3
assert SYNC13_OUT[0] == "Using CPython 3.13.5 interpreter at: /usr/bin/python3"

# the venv's python and uv's folder (the two hops of the symlink)
_link = capture("11-venv-bin", PB).pick(17)[0]                # file line 18
assert "python -> /home/student/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/" in _link
_uvdir = capture("24-du", PB).pick((3, 4))                     # file lines 4-5
assert _uvdir == ["cpython-3.15-linux-x86_64-gnu", "cpython-3.15.0-linux-x86_64-gnu"]
assert capture("11-venv-bin", PB13).pick(17)[0].endswith("python -> /usr/bin/python3")

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
BOTTOM = -3.5                    # terminal bottom edge
AX_Y = -0.1                      # the number line
AX_CX = -1.05                    # its centre (pushed left: the right column holds the labels)
AX_W = 10.5
COL_X = 2.3                      # left edge of the right-hand label column (V4)


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def under(m, color, buff=0.06, stroke=3):
    """A line under a group of glyphs."""
    return Line(m.get_corner(DL) + DOWN * buff, m.get_corner(DR) + DOWN * buff, color=color,
                stroke_width=stroke)


def toggle():
    """The GREY 'Debian 12 | Debian 13' switch. .flip(k) -> animations that select side k."""
    a, b = label("Debian 12", 22, INK), label("Debian 13", 22, S.GREY)
    row = VGroup(a, b).arrange(RIGHT, buff=0.55)
    h = a.height + 0.3
    frame = box(row.width + 0.6, h + 0.12, S.GREY, fill_opacity=0.04, radius=(h + 0.12) / 2)
    row.move_to(frame)
    pill = box(a.width + 0.36, h, S.GREY, fill_opacity=0.3, radius=h / 2).move_to(a)
    g = VGroup(frame, pill, row)
    g.sides, g.pill = (a, b), pill

    def flip(k):
        on, off = g.sides[k], g.sides[1 - k]
        return [pill.animate.move_to(on), on.animate.set_color(INK), off.animate.set_color(S.GREY)]

    g.flip = flip
    return g


def uv_folder():
    """uv's own folder for Pythons: header, then either '(empty)' or the two entries of 24-du.txt
    (short names) with the minor-version link between them. .frame .head .empty .entries .link"""
    head = VGroup(folder_glyph(0.3, S.GREY), mono("~/.local/share/uv/python/", 22, S.GREY))
    head.arrange(RIGHT, buff=0.15)
    a, b = mono("cpython-3.15", 22, INK), mono("cpython-3.15.0", 22, INK)
    link = Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=S.GREY, stroke_width=3, tip_length=0.15,
                 max_tip_length_to_length_ratio=0.5)
    entries = VGroup(a, link, b).arrange(RIGHT, buff=0.15)
    inner = VGroup(head, entries).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    empty = label("(empty)", 22, S.GREY).move_to(entries).align_to(entries, LEFT)
    w, h = inner.width + 0.45, inner.height + 0.32
    dashed = box(w, h, S.GREY, dashed=True).move_to(inner)
    solid = box(w, h, UV, fill_opacity=0.06).move_to(inner)
    g = VGroup(dashed, head, empty)
    g.frame, g.solid, g.head, g.empty, g.entries, g.link, g.a, g.b = dashed, solid, head, empty, \
        entries, link, a, b
    g.parts = VGroup(dashed, solid, head, empty, entries)      # everything, for positioning
    return g


def glyphs_of(txt, sub):
    """Glyphs of `sub` in a Text (its submobjects skip spaces)."""
    k = "".join(sub.split())
    i = "".join(txt.text.split()).index(k)
    return VGroup(*txt.submobjects[i:i + len(k)])


def ring_dot(point, fill=UV, ring=VENV):
    d = Dot(point, radius=0.12, color=fill)
    r = Circle(radius=0.2, stroke_color=ring, stroke_width=4).move_to(point)
    return VGroup(d, r)


def ghost(point):
    """A version that may differ: a GREY dashed ring."""
    return DashedVMobject(Circle(radius=0.17, stroke_color=S.GREY, stroke_width=3), num_dashes=10) \
        .move_to(point)


def pin_card():
    """The `.python-version` file `uv python pin 3.13` writes (GREEN: project-owned)."""
    name = VGroup(file_glyph(0.34, VENV), mono(".python-version", 22, VENV)).arrange(RIGHT, buff=0.15)
    body = mono("3.13", 26, INK)
    inner = VGroup(name, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    body.shift(RIGHT * 0.5)
    frame = box(inner.width + 0.5, inner.height + 0.36, VENV, fill_opacity=0.08).move_to(inner)
    g = VGroup(frame, inner)
    g.body = body
    return g


class WhichPython(VoiceScene):
    # ------------------------------------------------------------- helpers
    def pin(self, line, mob, run_time=0.4, anim=None):
        """Show `mob` beside a terminal line and make it part of that line. The line is re-added
        whole: an earlier animation of some of its glyphs (Indicate on a substring) leaves only
        those glyphs in the scene's list, and a submobject added to the line would not be drawn."""
        self.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
        self.remove(mob)
        line.add(mob)
        self.add(line)
        return mob

    def unpin(self, line, mob):
        if mob in line.submobjects:
            line.remove(mob)

    def strip_to(self, t, keep, rows, run_time=0.8):
        """Resize the terminal to `rows` (bottom edge fixed), keeping the lines with indices `keep`
        (in order) and fading the others."""
        ref = term(prompt=t.prompt, rows=rows)
        ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0],
                            BOTTOM - ref.box.get_bottom()[1], 0]))
        lines = list(t.lines.submobjects)
        kept = [lines[i] for i in keep]
        gone = [ln for i, ln in enumerate(lines) if i not in keep]
        anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar),
                 t.dots.animate.move_to(ref.dots), t.title.animate.move_to(ref.title)]
        for j, ln in enumerate(kept):
            anims.append(ln.animate.shift(ref._slot(j) - ln.strut.get_corner(UL)))
        if gone:
            anims.append(FadeOut(VGroup(*gone)))
        self.play(*anims, run_time=run_time)
        for ln in gone:
            t.lines.remove(ln)
        t.lines.submobjects = kept
        t.rows = rows
        return t

    def ponder(self, question, seconds, over):
        """The toolkit's ponder card (pause_and_ponder's look and timer), sized to cover `over` (the
        code panel) so the answer chips beside it stay visible. Returns the card (removed at the
        start of the next block)."""
        card = ponder_card(question, width=over.width)
        fr, head, q, bar = card
        new_fr = RoundedRectangle(width=over.width, height=over.height, corner_radius=0.2,
                                  stroke_color=TURN, stroke_width=3).set_fill(S.BG, 1).move_to(over)
        fr.become(new_fr)
        VGroup(head, q).move_to(new_fr).shift(UP * 0.12)
        bar.put_start_and_end_on(new_fr.get_corner(DL) + np.array([0.3, 0.25, 0]),
                                 new_fr.get_corner(DR) + np.array([-0.3, 0.25, 0]))
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=seconds)
        return card

    # ------------------------------------------------------------- the scene
    def construct(self):
        assert len(SAY) == 8, f"S10 has {len(SAY)} SAY lines; this scene times 8"

        tr = place_tracker(tracker_b(8))

        # ========================================================== 0 · read pyproject.toml
        panel = code_panel(TOML, "pyproject.toml", 1, language="toml", font_size=24)
        panel.move_to([0, -0.35, 0]).align_to([TRACK_LEFT, 0, 0], LEFT)
        code = panel.code
        L = lambda n: code.code_lines[n - 1]                          # file line n
        txt_right = lambda n: L(n).get_right()[0]

        bar2 = line_bar(code, 1, S.GREY, 0.14)
        remember = tag("remember this", S.GREY).move_to(L(2)).align_to([txt_right(2) + 0.45, 0, 0], LEFT)
        dep_rows = VGroup(L(7), L(10))
        brace_ref = Line([code.background.get_right()[0], dep_rows.get_top()[1], 0],
                         [code.background.get_right()[0], dep_rows.get_bottom()[1], 0])
        brace = Brace(brace_ref, RIGHT, color=VENV, buff=0.12)
        deps = label("2 dependencies", 26, VENV).next_to(brace, RIGHT, buff=0.15)
        bar_dep = line_bar(code, 7, VENV, 0.16)                       # follows the narration: 8, 9, 8, 9
        y8, y9 = bar_dep.get_center()[1], line_bar(code, 8).get_center()[1]
        ge8, eq9, ge6 = code_span(code, 7, ">="), code_span(code, 8, "=="), code_span(code, 5, ">=")
        ul8, ul9, ul6 = under(ge8, VENV), under(eq9, VENV), under(ge6, VENV)
        rng8 = tag("range", VENV).move_to(L(8)).align_to([txt_right(8) + 0.45, 0, 0], LEFT)
        exact9 = tag("exact", VENV).move_to(L(9)).align_to([txt_right(9) + 0.45, 0, 0], LEFT)
        rng6 = tag("range", VENV).move_to(L(6)).align_to([txt_right(6) + 0.45, 0, 0], LEFT)
        bar6 = line_bar(code, 5, TURN, 0.22)
        cols8, cols9 = [g.get_color() for g in ge8], [g.get_color() for g in eq9]
        v313 = code_span(code, 5, "3.13")

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.5)
            self.play(tr.goto(9), run_time=0.5)
            vo.wait_until("and it reads")
            self.play(FadeIn(panel, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("so let's read")
            self.play(Indicate(panel.header, color=S.WHITE, scale_factor=1.1), run_time=0.9)
            vo.wait_until("The name is app")
            self.play(FadeIn(bar2), FadeIn(remember, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Two dependencies")
            self.play(GrowFromCenter(brace), FadeIn(deps, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("art, version")
            self.play(FadeIn(bar_dep), run_time=0.4)
            vo.wait_until("and googletrans")
            self.play(bar_dep.animate.set_y(y9), run_time=0.4)
            vo.wait_until("Greater-or-equal")
            self.play(bar_dep.animate.set_y(y8), run_time=0.3)
            self.play(ge8.animate.set_color(VENV), Create(ul8), FadeIn(rng8, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("double equals")
            self.play(bar_dep.animate.set_y(y9), eq9.animate.set_color(VENV), Create(ul9),
                      FadeIn(exact9, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Line 6")
            self.play(FadeOut(bar_dep), FadeIn(bar6), ge6.animate.set_color(VENV), Create(ul6),
                      FadeIn(rng6, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Python 3.13")
            self.play(Indicate(v313, color=TURN, scale_factor=1.3), run_time=1.0)

        # ========================================================== 1 · predict
        col_x = panel.get_right()[0] + 0.3
        vm = chip(f"this VM: {VM_PY}", S.GREY, size=24)
        q = chip("uv sync", UV, size=24, font=MONO)
        qmark = label("?", 30, UV)
        quest = VGroup(q, qmark).arrange(RIGHT, buff=0.18)
        answers = VGroup(*[chip(s, S.GREY, size=24) for s in ("fail?", "use 3.11 anyway?", "something else?")])
        answers.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        right = VGroup(vm, quest, answers).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        right.move_to([0, panel.get_center()[1], 0]).align_to([col_x, 0, 0], LEFT)
        answers.shift(RIGHT * 0.35)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(bar2, remember, brace, deps, ul8, ul9, rng8, exact9)),
                      *[g.animate.set_color(c) for g, c in zip([*ge8, *eq9], [*cols8, *cols9])], run_time=0.5)
            vo.wait_until("This VM has")
            self.play(FadeIn(vm, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("The project asks")
            self.play(Indicate(VGroup(L(6), rng6), color=TURN, scale_factor=1.05), run_time=1.0)
            vo.wait_until("What will")
            self.play(FadeIn(quest, shift=LEFT * 0.15), run_time=0.6)
            for a, phrase in zip(answers, ["Fail", "use 3.11", "or something"]):
                vo.wait_until(phrase)
                self.play(FadeIn(a, shift=DOWN * 0.1), run_time=0.4)

        card = self.ponder("This VM has Python 3.11.\nThe project asks for 3.13 or newer.\nWhat will uv sync do?",
                           8, over=code.background)

        # ========================================================== 2 · uv sync
        p6 = code_panel(TOML6, "pyproject.toml", 6, language="toml", font_size=24)
        p6.move_to([0, 2.05, 0]).align_to([-6.3, 0, 0], LEFT)
        bar6b = line_bar(p6.code, 0, TURN, 0.22)
        vm_to = vm.copy().next_to(p6.code, RIGHT, buff=0.6)
        ans_row = answers.copy().arrange(RIGHT, buff=0.35).move_to([0, 0.75, 0]).align_to([-6.3, 0, 0], LEFT)

        t = term(prompt=P_REPO, rows=5)
        t.shift(np.array([0 - t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
        frame = VGroup(t.box, t.bar, t.dots, t.title)

        note = label("no pyproject.toml found?  →  cd simple-translate", 22, S.GREY,
                     t2f={"pyproject.toml": MONO, "cd simple-translate": MONO}, t2c={"cd simple-translate": INK})
        note.move_to([0, t.box.get_top()[1] + 0.38, 0]).align_to([6.3, 0, 0], RIGHT)

        with self.voiceover(SAY[2]) as vo:
            others = VGroup(*[code.code_lines[k] for k in range(10) if k != 5])
            self.play(FadeOut(card), run_time=0.4)
            self.play(FadeOut(others), FadeOut(VGroup(ul6, rng6, quest)),
                      ReplacementTransform(code.code_lines[5], p6.code.code_lines[0]),
                      ReplacementTransform(code.background, p6.code.background),
                      ReplacementTransform(panel.header, p6.header),
                      ReplacementTransform(bar6, bar6b),
                      vm.animate.move_to(vm_to), Transform(answers, ans_row), run_time=0.9)
            self.remove(panel)
            self.add(p6.code.background, bar6b, p6.code.code_lines, p6.header)
            self.play(FadeIn(frame, shift=UP * 0.6), run_time=0.6)
            cmd = t.type(self, "uv sync", type_time=0.5)
            yt = your_turn().next_to(cmd.strut, RIGHT, buff=0.4)
            self.pin(cmd, yt, run_time=0.4)

            vo.wait_until("Instead of failing")
            out = t.print(self, SYNC_OUT, run_time=0.6)
            xs = [cross_mark(0.34, ERR, stroke=5).move_to(a) for a in answers[:2]]
            ok = check_mark(0.36, S.GREEN, stroke=6).next_to(answers[2], RIGHT, buff=0.12)
            self.play(answers[0].animate.set_opacity(0.4), answers[1].animate.set_opacity(0.4),
                      *[Create(x) for x in xs], run_time=0.5)
            self.play(Create(ok), Indicate(answers[2], color=S.WHITE, scale_factor=1.08), run_time=0.6)
            vo.wait_until("downloads its own")
            mib = substring(out[0], "(35.9MiB)")
            ul_mib = under(mib, S.GREY)
            self.play(Create(ul_mib), Indicate(substring(out[0], "cpython-3.15.0"), color=UV, scale_factor=1.08),
                      run_time=0.8)
            self.remove(ul_mib)
            out[0].add(ul_mib)
            self.add(out[0])
            vo.wait_until("CPython 3.15.0")
            ver = substring(out[2], "3.15.0")
            rec = recorded_tag().next_to(out[2].strut, RIGHT, buff=0.4)
            self.play(Indicate(ver, color=S.WHITE, scale_factor=1.2), run_time=0.6)
            self.pin(out[2], rec, run_time=0.5)

            vo.wait_until("Then it creates")
            venv = substring(out[3], ".venv")
            self.play(FadeOut(VGroup(answers, *xs, ok)), venv.animate.set_color(VENV), run_time=0.5)
            self.play(Indicate(out[3], color=S.WHITE, scale_factor=1.04), run_time=0.9)
            vo.wait_until("If uv can't")
            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("cd into")
            self.play(Indicate(glyphs_of(note, "cd simple-translate"), color=S.WHITE, scale_factor=1.1), run_time=0.9)

        # ========================================================== 3 · V4: the number line
        vl = VersionLine(10, 16, lo=13, width=AX_W, size=22)
        vl.shift(np.array([AX_CX, AX_Y, 0]))
        x = lambda m: vl.point(m)[0]
        band_label = mono(TOML6, 20, VENV)
        band_label.next_to(vl.band, UP, buff=0.25).align_to([6.5, 0, 0], RIGHT)
        tg = toggle().move_to([0, 3.24, 0]).align_to([6.5, 0, 0], RIGHT)
        uvf = uv_folder()
        uvf.parts.shift(np.array([COL_X - 0.2 - uvf.frame.get_right()[0], 1.85 - uvf.entries.get_center()[1], 0]))
        vm_spot = np.array([x(11), 1.15, 0])
        sys_dot = Dot(vm_spot + DOWN * 0.45, radius=0.11, color=S.GREY)
        sys_lab = mono(f"{VM_VER} · /usr/bin/python3", 22, ERR)
        sys_lab.move_to([x(11), AX_Y - 1.08, 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(yt, rec, note)), run_time=0.3)
            self.unpin(cmd, yt)
            self.unpin(out[2], rec)
            self.strip_to(t, [0, 1, 3], rows=3, run_time=0.8)
            vo.wait_until("Picture Python")
            self.play(Create(vl.axis), LaggedStart(*[FadeIn(tk, shift=UP * 0.1) for tk in vl.ticks],
                                                   lag_ratio=0.12), run_time=1.3)
            vo.wait_until("The constraint")
            band_full = vl.band.copy()
            vl.band.stretch_to_fit_width(0.01).align_to(band_full, LEFT)
            self.add(vl.band)
            self.play(Transform(vl.band, band_full),
                      ReplacementTransform(p6.code.code_lines[0], band_label),
                      FadeOut(VGroup(p6.code.background, p6.header, bar6b)), run_time=1.2)
            self.play(vm.animate.move_to(vm_spot), run_time=0.6)

            vo.wait_until("First, uv looks")
            self.play(FadeIn(VGroup(uvf.frame, uvf.head), shift=DOWN * 0.1), run_time=0.6)
            look = SurroundingRectangle(uvf.frame, buff=0.08, color=LOOKUP, stroke_width=4, corner_radius=0.12)
            vo.wait_until("its own downloads")
            self.play(Create(look), run_time=0.5)
            self.play(FadeIn(uvf.empty), run_time=0.4)
            vo.wait_until("then the system")
            look2 = SurroundingRectangle(vm, buff=0.1, color=LOOKUP, stroke_width=4, corner_radius=0.12)
            self.play(Transform(look, look2), run_time=0.6)

            vo.wait_until("Debian's 3.11.2")
            self.play(FadeIn(tg, shift=DOWN * 0.1), FadeIn(sys_dot, scale=0.5), run_time=0.5)
            self.play(sys_dot.animate.move_to(vl.point(11)), run_time=0.6, rate_func=rate_functions.ease_in_quad)
            self.play(FadeIn(sys_lab, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("lands outside")
            self.play(sys_dot.animate.set_color(ERR), FadeOut(look), run_time=0.5)
            vo.wait_until("so it can't")
            sx = cross_mark(0.36, ERR, stroke=6).move_to(vl.point(11, 0.48))
            self.play(Create(sx), Indicate(sys_lab, color=ERR, scale_factor=1.06), run_time=0.8)

        # ========================================================== 4 · uv downloads one
        q13 = ghost(vl.point(13))
        q13m = label("?", 28, S.GREY).next_to(q13, UP, buff=0.12)
        q13x = cross_mark(0.3, ERR, stroke=5).move_to(q13m)
        dl_top = uvf.b.get_bottom() + DOWN * 0.12
        new = ring_dot(vl.point(15))
        drop = Arrow(dl_top, vl.point(15, 0.22), buff=0, color=UV, stroke_width=5, tip_length=0.22,
                     max_tip_length_to_length_ratio=0.2)
        spec1 = label("newest release in range", 24, INK)
        spec2 = VGroup(mono("3.15.0", 24, VENV), label("· uv-managed", 22, UV)).arrange(RIGHT, buff=0.15)
        spec3 = recorded_tag()
        spec = VGroup(spec1, spec2, spec3).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        spec.move_to([0, 1.62, 0]).align_to([COL_X, 0, 0], LEFT)

        vpy = chip(".venv/bin/python", VENV, size=22, font=MONO).move_to(np.array([x(11) - 0.55, 0.95, 0]))
        hop1 = Arrow(vpy.get_top() + RIGHT * 0.9, uvf.a.get_bottom() + LEFT * 0.3, buff=0.1, color=VENV,
                     stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.25)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(vm), run_time=0.4)
            dl_line = t.find("Downloading")
            self.play(Indicate(substring(dl_line, "Downloading cpython-3.15.0"), color=UV, scale_factor=1.04),
                      FadeOut(uvf.frame), FadeIn(uvf.solid), run_time=1.0)
            uvf.frame = uvf.solid
            vo.wait_until("Which one")
            self.play(FadeIn(q13, scale=0.6), FadeIn(q13m, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Not 3.13")
            self.play(Create(q13x), q13m.animate.set_opacity(0.3), run_time=0.4)
            vo.wait_until("but the newest")
            self.play(FadeOut(VGroup(q13, q13m, q13x)), FadeOut(uvf.empty),
                      FadeIn(uvf.entries, shift=DOWN * 0.1), run_time=0.5)
            self.play(GrowArrow(drop), run_time=0.5)
            self.play(FadeIn(new, shift=DOWN * 0.5), FadeIn(spec1, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("which was 3.15.0")
            self.play(FadeIn(spec2, shift=LEFT * 0.1), run_time=0.5)
            self.play(FadeIn(spec3, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("It lives")
            self.play(Indicate(uvf.head[1], color=S.WHITE, scale_factor=1.06),
                      Indicate(uvf.b, color=VENV, scale_factor=1.06), run_time=1.0)
            vo.wait_until("and the venv's")
            self.play(FadeIn(vpy, shift=RIGHT * 0.2), run_time=0.5)
            self.play(GrowArrow(hop1), run_time=0.5)
            self.play(uvf.link.animate.set_color(VENV), Indicate(uvf.a, color=VENV, scale_factor=1.06), run_time=0.5)
            self.play(Indicate(new, color=VENV, scale_factor=1.3), run_time=0.6)

        # ========================================================== 5 · a constraint is not a pin
        end = vl.band.get_right()[0]
        tip_x = 6.45
        ext = Rectangle(width=tip_x - 0.35 - end, height=vl.band.height, stroke_width=0) \
            .set_fill(VENV, 0.3).move_to([(end + tip_x - 0.35) / 2, AX_Y, 0])
        head = Polygon([tip_x - 0.35, AX_Y + 0.27, 0], [tip_x, AX_Y, 0], [tip_x - 0.35, AX_Y - 0.27, 0],
                       stroke_width=0).set_fill(VENV, 0.55)
        nolim = label("no upper limit", 22, VENV).move_to([(end + tip_x) / 2, AX_Y - 0.45, 0])
        big = VGroup(label("a constraint", 36, INK), label("is not a pin", 36, TURN)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        big.move_to([0, 1.95, 0]).align_to([COL_X + 0.15, 0, 0], LEFT)
        steps = [label("before 3.15 existed  →  3.14", 22, S.GREY), label("today  →  3.15.0", 22, INK),
                 label("later  →  newer", 22, S.GREY)]
        for s_ in steps:
            s_.move_to([0, 1.0, 0]).align_to([COL_X + 0.15, 0, 0], LEFT)
        g14, g16 = ghost(vl.point(14)), ghost(vl.point(16))

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(spec), run_time=0.4)
            self.play(FadeIn(ext, shift=LEFT * 0.3), FadeIn(head, shift=LEFT * 0.3), run_time=0.7)
            self.play(FadeIn(nolim, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("a constraint is")
            self.play(FadeIn(big[0], shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(big[1], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Before Python")
            new.save_state()
            self.play(FadeIn(g14, scale=0.6), FadeIn(steps[0], shift=UP * 0.1), new.animate.fade(0.65),
                      run_time=0.6)
            vo.wait_until("gave people")
            self.play(Indicate(g14, color=S.WHITE, scale_factor=1.5), run_time=0.8)
            vo.wait_until("Watch this")
            self.play(FadeOut(steps[0], shift=UP * 0.2), FadeIn(steps[1], shift=UP * 0.2), Restore(new), run_time=0.5)
            self.play(Indicate(new, color=VENV, scale_factor=1.3), run_time=0.6)
            vo.wait_until("something newer")
            self.play(FadeOut(steps[1], shift=UP * 0.2), FadeIn(steps[2], shift=UP * 0.2), FadeIn(g16, scale=0.6),
                      run_time=0.6)
            self.play(Indicate(g16, color=S.WHITE, scale_factor=1.5), run_time=0.8)

        # ========================================================== 6 · Debian 13
        d13_lab = mono(f"{D13_VER} · /usr/bin/python3", 22, ERR).move_to([x(13), AX_Y - 1.08, 0])
        hop13 = Arrow(vpy.get_right() + DOWN * 0.05, vl.point(13) + np.array([-0.12, 0.14, 0]), buff=0.1,
                      color=VENV, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.25)
        d13tag = tag("Debian 13", S.GREY)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(big, steps[2], g14, g16, nolim, sx)), *tg.flip(1), run_time=0.6)
            t.clear(self, run_time=0.3)
            cmd13 = t.type(self, "uv sync", type_time=0.4)
            t.print(self, SYNC13_OUT, run_time=0.5)
            d13tag.next_to(cmd13.strut, RIGHT, buff=0.4)
            self.pin(cmd13, d13tag, run_time=0.4)
            vo.wait_until("Its system Python")
            self.play(sys_dot.animate.move_to(vl.point(13)), ReplacementTransform(sys_lab, d13_lab),
                      run_time=1.2)
            vo.wait_until("is already inside")
            self.play(sys_dot.animate.set_color(VENV).scale(1.2), d13_lab.animate.set_color(VENV),
                      vl.band.animate(rate_func=there_and_back).set_fill(opacity=0.65), run_time=0.8)
            vo.wait_until("with no download")
            self.play(FadeOut(new, shift=UP * 0.6), Uncreate(drop),
                      FadeOut(uvf.solid), FadeOut(uvf.head), FadeOut(uvf.entries), run_time=0.9)
            vo.wait_until("and the venv's")
            self.play(ReplacementTransform(hop1, hop13), run_time=0.9)
            self.play(Indicate(d13_lab, color=S.WHITE, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Same command")
            self.play(Indicate(substring(cmd13, "uv sync"), color=S.WHITE, scale_factor=1.2), run_time=0.7)
            vo.wait_until("different Debian")
            self.play(Indicate(tg.sides[1], color=S.WHITE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("different Python")
            self.play(Indicate(sys_dot, color=VENV, scale_factor=1.5), run_time=0.7)

        # ========================================================== 7 · pin it (not now)
        DY = 0.9                                   # the line settles lower once the strip has gone
        ay7 = AX_Y - DY
        line_parts = VGroup(vl.axis, vl.ticks, vl.band, ext, head, band_label)
        pin_cmd = chip("uv python pin 3.13", UV, size=24, font=MONO)
        ex_tag = extra_tag()
        not_now = tag("not now · exercise B2", ERR)
        row = VGroup(pin_cmd, ex_tag, not_now).arrange(RIGHT, buff=0.3)
        row.move_to([0, 1.75, 0]).align_to([-6.3, 0, 0], LEFT)
        pc = pin_card()
        pc.move_to([pin_cmd.get_center()[0], 0.35, 0])
        writes = Arrow(pin_cmd.get_bottom(), pc.get_top(), buff=0.08, color=UV, stroke_width=4, tip_length=0.18,
                       max_tip_length_to_length_ratio=0.3)
        seg_r = x(14) - 0.3
        seg = Rectangle(width=seg_r - x(13), height=vl.band.height, stroke_width=0).set_fill(VENV, 0.45)
        seg.move_to([(x(13) + seg_r) / 2, ay7, 0])
        seg_lab = mono("3.13.x", 24, VENV).next_to(seg, UP, buff=0.25)
        shrink = Arrow(pc.get_right(), seg_lab.get_left(), buff=0.12, color=VENV,
                       stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.25)
        one = label("pin 3.13.5  →  one release", 22, S.GREY).move_to([0, ay7 - 1.08, 0]).align_to([x(13), 0, 0], LEFT)

        with self.voiceover(SAY[7]) as vo:
            self.play(*tg.flip(0), FadeOut(VGroup(t.box, t.bar, t.dots, t.title, t.lines)),
                      FadeOut(VGroup(vpy, hop13, sys_dot, d13_lab)), run_time=0.8)
            self.play(line_parts.animate.shift(DOWN * DY), run_time=0.8)
            vo.wait_until("The command")
            self.play(FadeIn(pin_cmd, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("not in the README")
            self.play(FadeIn(ex_tag, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("writes a small")
            self.play(Create(writes), FadeIn(pc, shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("dot python version")
            self.play(Indicate(pc.body, color=S.WHITE, scale_factor=1.3), run_time=0.8)
            vo.wait_until("and the range shrinks")
            self.play(GrowArrow(shrink), run_time=0.4)
            self.play(Transform(vl.band, seg), FadeOut(VGroup(ext, head), shift=LEFT * 1.5),
                      band_label.animate.set_opacity(0.35), run_time=1.0)
            self.play(FadeIn(seg_lab, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("the 3.13 series")
            self.play(FadeIn(one, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Don't run it")
            self.play(FadeIn(not_now, shift=LEFT * 0.1), run_time=0.5)
            self.play(Circumscribe(pin_cmd, color=ERR, buff=0.08), run_time=1.0)
            vo.wait_until("and the rest")
            self.play(Wiggle(pc, scale_value=1.05, rotation_angle=0.02 * TAU), run_time=0.9)
            vo.wait_until("It's in the exercises")
            self.play(Indicate(not_now, color=ERR, scale_factor=1.12), run_time=0.9)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
