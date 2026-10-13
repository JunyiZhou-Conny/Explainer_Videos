"""S13 · Prove the isolation (part 2, extras after step 11; PONDER 4; the V2 shelves twice).

Beats (script.md "## S13", one voiceover block each):
 0  TRACKER B11 · extra. A 7-row terminal at the `(app)` prompt types `deactivate` (extra) -> no
    output; the next prompt has no `(app)` (it pulses). A GREY tag on the old prompt's `(app)`:
    "while active, python3 → .venv too", with the real `python3 -> python` (11-venv-bin.txt line
    19). `python3 -c 'import googletrans'` (extra, two rows; `python3` turns ORANGE: the system's)
    -> 20-isolation.txt lines 2-4, line 4 RED; a GREEN row tag "only in .venv".
 1  V2 above the 3-row strip (the command's two rows + the error line stay): the system python3
    stack of this VM (current folder; GREY band "standard library · 3.11"; the empty ORANGE
    /usr/local shelf; apt's ORANGE shelf with three unnamed jars). To the right, apart, the GREEN
    `.venv/…/site-packages` shelf in its own box, eleven jars, googletrans named. The PINK light
    "import googletrans" sweeps the four shelves top to bottom; the venv box pulses with the GREY
    caption "not on python3's list"; the light turns RED at the bottom ("comes up empty") and the
    error line in the strip pulses. (A found lookup gets a PINK check, a failed one a RED cross.)
 2  `uv run python -c 'import googletrans, sys; print(sys.prefix)'` (extra, two rows) ->
    21-uv-run.txt line 2. `print(sys.prefix)` pulses; the path prints as "It works" is spoken and the
    light jumps into the GREEN box and finds the googletrans jar (PINK check); on "the answer is"
    the path gets a GREEN bar and `.venv` turns GREEN; it pulses on "our dot venv".
 3  Everything but the tracker fades. A faint GREY dashed VM glyph, legend "part-1 VM", tag
    "illustration · what if" (no shelves: they are the answer). Inside: `python3 -c 'import
    googletrans'`, then "python3 (system)" in ORANGE, then a GREY dashed "no .venv".
    PONDER (6 s), card at the bottom.
 4  The glyph opens into the part-1 shelves (full width, short labels): current folder, standard
    library · 3.11, /usr/local/… (pip's) with S05's twelve ORANGE jars, apt's with four. The
    command's `import googletrans` becomes the PINK light's label; it sweeps down and stops on
    pip's shelf; a GREY tag "system-wide" on the shelf (as named); on "user local shelf" the
    googletrans jar gets its name tag and the light's label turns into the real path
    (debian12-part-a/09-where.txt line 2); "every program" pulses the tag.
 5  The part-1 stack slides left to half width (the jars stack in piles to fit); a GREEN venv stack
    (current folder, standard library, .venv/…/site-packages with eleven jars) builds at right,
    behind a dashed divider; its own light runs down its three shelves only and finds googletrans.
    Caption "a venv ignores whatever the system Python has". Fade out to an empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import OUTPUT, box, check_mark, cross_mark, label, mono, mono_line, substring, tag
from explainer.scene import VoiceScene

from common import (ERR, INK, LOOKUP, NARRATION, P_REPO, P_VENV, SYSTEM, VENV, Shelves, capture, jars,
                    name_tag, term, tracker_b)

SAY = NARRATION["S13"]
PA, PB = "debian12-part-a", "debian12-part-b"

# ------------------------------------------------------------------ commands (all extras)
DEACT = "deactivate"
PY3 = "python3 -c 'import googletrans'"
UVRUN = "uv run python -c 'import googletrans, sys; print(sys.prefix)'"

# ------------------------------------------------------------------ real outputs (pick index = file line - 1)
_iso = capture("20-isolation", PB)
assert _iso.cmd == PY3, _iso.cmd
ISO_OUT = _iso.pick((1, 3))                                                  # file lines 2-4
assert ISO_OUT[0].startswith("Traceback") and ISO_OUT[2] == "ModuleNotFoundError: No module named 'googletrans'"

_uv = capture("21-uv-run", PB)
assert _uv.cmd == UVRUN, _uv.cmd
PREFIX = _uv.pick(1)[0]                                                      # file line 2
assert PREFIX == "/home/student/simple-translate/.venv"

_l19 = capture("11-venv-bin", PB).pick(18)[0]                               # file line 19
LINK = _l19[_l19.index("python3 -> python"):]
assert LINK == "python3 -> python", _l19

WHERE_OUT = capture("09-where", PA).pick(1)[0]                               # file line 2
assert WHERE_OUT == "/usr/local/lib/python3.11/dist-packages/googletrans/__init__.py"

# the package lists, so each googletrans jar stands where it really is in its list
VENV_PKGS = [s.strip().lstrip("+ ").split("==")[0] for s in capture("08-uv-sync", PB).pick((8, 18))]
assert len(VENV_PKGS) == 11 and VENV_PKGS[0] == "anyio" and VENV_PKGS[-1] == "idna", VENV_PKGS
GT_VENV = VENV_PKGS.index("googletrans")
_inst = capture("08-pip-break", PA).pick(34)[0]                              # file line 35
assert _inst.startswith("Successfully installed")
PIP_PKGS = _inst.split()[2:]
assert len(PIP_PKGS) == 12
GT_PIP = PIP_PKGS.index("googletrans-4.0.2")

PONDER_Q = "Same import, on your part-1 VM, after deactivate.\nDoes it work?"

# short shelf labels (script.md, V2 layout)
CUR = "(empty) = the current folder"
LOCAL_S = "/usr/local/… (pip's)"
APT_S = "/usr/lib/python3/… (apt's)"
SITE_S = ".venv/…/site-packages"

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
BOTTOM = -3.5                                    # terminal bottom edge
# beats 1-2: system stack (left) above the 3-row strip, the venv box apart at right
B1 = [2.2, 1.2, 0.2, -0.8]                       # board heights (the light on the last clears the strip)
S1_L, S1_R = -6.4, 1.2                           # stack x range
VB_L, VB_R, VB_BOARD = 2.0, 6.4, 0.55            # venv box x range and its board height
# beats 3-5: inside the part-1 VM frame
F_TOP, F_BOT = 2.6, -3.35
B4 = [1.15, -0.2, -1.55, -2.65]                  # board heights (room for a 2-row jar pile + its name tag)
FULL_L, FULL_R = -6.2, 6.2
HALF_L = (-6.25, -0.2)
HALF_R = (0.2, 6.25)
TITLE_Y = 2.1


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def caption_text(tr, extra: bool):
    s = f"step {tr.k} of {len(tr.steps)}: {tr.steps[tr.k - 1]}"
    t = label(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY}) if extra else \
        label(s, tr.size, tr.hi_color)
    return t.next_to(tr.dots, RIGHT, buff=0.25)


def row_tag(s: str, color=S.GREY, size: float = 22, text_color=None) -> VGroup:
    """A tag that fits inside one terminal row (the house tag is taller than a row)."""
    t = label(s, size, text_color or color)
    h = 0.37
    b = RoundedRectangle(width=t.width + 0.36, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def beside(mob, line, buff=0.4):
    """Put `mob` right of terminal row `line`, centred on the row."""
    return mob.move_to([line.strut.get_right()[0] + buff + mob.width / 2, line.strut.get_center()[1], 0])


def row_bar(line, color, opacity=0.22, pad=0.08):
    """A translucent bar behind a terminal row's glyphs."""
    g = line.glyphs
    return Rectangle(width=g.width + 2 * pad, height=line.strut.height + 0.04, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def beam(x0: float, x1: float, board_y: float, text: str = "import googletrans", color=LOOKUP) -> VGroup:
    """The search-light over the shelf whose board is at board_y: a translucent PINK band over the
    shelf, its label riding just under the board (right-aligned, clear of every shelf label).
    .rect .text"""
    r = Rectangle(width=x1 - x0, height=1.0, stroke_width=0).set_fill(color, 0.2)
    r.move_to([(x0 + x1) / 2, board_y + 0.05, 0])
    t = mono(text, 22, color)
    t.move_to([x1 - 0.15 - t.width / 2, board_y - 0.26, 0])
    g = VGroup(r, t)
    g.rect, g.text = r, t
    return g


def stack(paths, x0: float, x1: float, boards, colors: dict, std: str | None = None) -> Shelves:
    """A V2 stack (Shelves) from x0 to x1 with its boards at the given heights. Row 1 becomes the
    GREY 'standard library' band when `std` is given. .boards .texts .band"""
    sh = Shelves(paths, width=x1 - x0, size=22, pitch=boards[0] - boards[1], colors=colors)
    sh.shift(RIGHT * (x0 - sh.rows[0][0].get_left()[0]))
    for row, y in zip(sh.rows, boards):                  # the boards need not be evenly spaced
        row.shift(UP * (y - row[0].get_y()))
    sh.band = None
    if std is not None:
        board, old = sh.rows[1]
        lbl = label(std, 24, S.GREY).next_to(board, UP, buff=0.1).align_to(board, LEFT)
        band = Rectangle(width=x1 - x0, height=0.72, stroke_width=0).set_fill(S.GREY, 0.12)
        band.move_to(board, aligned_edge=DOWN)
        sh.rows[1].remove(old)
        sh.rows[1].add(lbl)
        sh.rows[1].submobjects.insert(0, band)
        sh.band = band
    sh.boards = [r[1] if (std is not None and i == 1) else r[0] for i, r in enumerate(sh.rows)]
    sh.texts = [r[-1] for r in sh.rows]
    return sh


def jar_row(n: int, color, buff: float = 0.12) -> VGroup:
    return VGroup(*jars(n, color)).arrange(RIGHT, buff=buff)


def on_board(g, board, right: float | None = None):
    """Stand a jar group on a board, right-aligned (at the board's end or at x=right)."""
    g.next_to(board, UP, buff=0.04)
    x = board.get_right()[0] if right is None else right
    g.shift(RIGHT * (x - g.get_right()[0]))
    return g


def pile_targets(group: VGroup, top_n: int, board, buff: float = 0.04) -> list:
    """Centres for the jars of `group` stacked in two rows on `board`, right-aligned: the first
    top_n jars on top (centred over the bottom row), the rest below."""
    w, h = group[0].width, group[0].height
    bottom_n = len(group) - top_n
    xr = board.get_right()[0]
    y0 = board.get_y() + 0.04 + h / 2
    out = []
    width_b = bottom_n * w + (bottom_n - 1) * buff
    width_t = top_n * w + (top_n - 1) * buff
    xb0 = xr - width_b + w / 2
    xt0 = xr - width_b / 2 - width_t / 2 + w / 2
    for k in range(len(group)):
        if k < top_n:
            out.append(np.array([xt0 + k * (w + buff), y0 + h + 0.02, 0]))
        else:
            out.append(np.array([xb0 + (k - top_n) * (w + buff), y0, 0]))
    return out


class Isolation(VoiceScene):
    # ------------------------------------------------------------- terminal helpers (as in S12)
    def pin(self, line, mob, run_time=0.4, anim=None, behind=False):
        """Show `mob` beside a terminal line and make it part of that line (it scrolls with it)."""
        self.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
        self.remove(mob)
        if behind:
            line.submobjects.insert(0, mob)
        else:
            line.add(mob)
        self.add(line)
        return mob

    def unpin(self, pairs, run_time=0.3, *extra):
        self.play(*[FadeOut(m) for _, m in pairs], *extra, run_time=run_time)
        for line, m in pairs:
            if m in line.submobjects:
                line.remove(m)

    def bare_prompt(self, t):
        ln = t.type(self, "", type_time=0)
        ln.bare = True
        return ln

    def type_cmd(self, t, cmd, type_time=None):
        """Type at the waiting prompt (replacing a bare prompt line if there is one)."""
        if len(t.lines) and getattr(t.lines[-1], "bare", False):
            last = t.lines[-1]
            self.remove(last, *last.submobjects)
            t.lines.remove(last)
        return t.type(self, cmd, type_time)

    def resize(self, t, rows, keep=None, run_time=0.8, extra=()):
        """Grow or shrink the terminal to `rows` (bottom edge fixed), keeping the lines with indices
        `keep` (default: the last ones that fit), in order; the rest fade."""
        ref = term(prompt=t.prompt, rows=rows)
        ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0],
                            BOTTOM - ref.box.get_bottom()[1], 0]))
        lines = list(t.lines.submobjects)
        if keep is None:
            keep = list(range(max(0, len(lines) - rows), len(lines)))
        kept = [lines[i] for i in keep]
        gone = [ln for i, ln in enumerate(lines) if i not in keep]
        if gone:                                         # nothing slides over a fading line
            self.play(FadeOut(VGroup(*gone)), run_time=0.3)
        anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar),
                 t.dots.animate.move_to(ref.dots), t.title.animate.move_to(ref.title)]
        for j, ln in enumerate(kept):
            anims.append(ln.animate.shift(ref._slot(j) - ln.strut.get_corner(UL)))
        self.play(*anims, *extra, run_time=run_time)
        t.lines.submobjects = kept
        t.rows = rows
        return t

    def flash(self, line, sub, color, scale=1.2, run_time=0.7):
        """Indicate part of a terminal row, then re-add the row whole (an Indicate on some of its
        glyphs puts them at the top level of the scene)."""
        self.play(Indicate(sub, color=color, scale_factor=scale), run_time=run_time)
        self.add(line)

    # ------------------------------------------------------------- the scene
    def construct(self):
        assert len(SAY) == 6, f"S13 has {len(SAY)} SAY lines; this scene times 6"

        tr = place_tracker(tracker_b(11))
        tr.caption.become(caption_text(tr, True))

        # ========================================================== 0 · deactivate; the system python3
        t = term(prompt=P_VENV, rows=7)
        t.shift(np.array([0 - t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
        frame0 = VGroup(t.box, t.bar, t.dots, t.title)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(frame0), run_time=0.7)
            p_old = self.bare_prompt(t)
            self.play(Indicate(substring(p_old, "(app)"), color=VENV, scale_factor=1.25), run_time=0.8)
            self.add(p_old)

            vo.wait_until("Deactivate first")
            l0 = self.type_cmd(t, DEACT, 0.6)
            x0 = row_tag("extra")
            self.pin(l0, beside(x0, l0), run_time=0.3)
            t.set_prompt(P_REPO)
            p_new = self.bare_prompt(t)
            self.play(Indicate(p_new.glyphs, color=S.WHITE, scale_factor=1.06), run_time=0.6)
            self.add(p_new)

            # the GREY tag on the old prompt: while active, python3 is the venv's too
            app = substring(l0, "(app)")
            app_box = SurroundingRectangle(app, buff=0.06, corner_radius=0.05, color=S.GREY, stroke_width=2)
            old_tag = tag("while active, python3 → .venv too", S.GREY)
            old_tag.move_to([-6.25 + old_tag.width / 2, t.box.get_top()[1] + 0.62, 0])
            lead = Line([app.get_x(), app_box.get_top()[1], 0], [app.get_x(), old_tag.get_bottom()[1], 0],
                        color=S.GREY, stroke_width=2)
            ev = VGroup(mono(LINK, 22, OUTPUT), label("in .venv/bin", 22, S.GREY)).arrange(RIGHT, buff=0.2)
            ev.next_to(old_tag, RIGHT, buff=0.4)
            vo.wait_until("while the venv is active")
            self.play(Create(app_box), Create(lead), FadeIn(old_tag, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("even python3")
            self.play(FadeIn(ev, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(ev[0], color=VENV, scale_factor=1.12), run_time=0.7)

            vo.wait_until("Then ask")
            cmd = self.type_cmd(t, PY3, 0.85)
            r0, r1 = cmd.rows
            x1 = beside(row_tag("extra"), r1)
            py3 = substring(r0, "python3")
            vo.wait_until("the system's python3")          # (spoken while the command is typed)
            self.pin(r1, x1, run_time=0.35,
                     anim=AnimationGroup(FadeIn(x1, shift=LEFT * 0.1), py3.animate.set_color(SYSTEM)))
            self.flash(r0, py3, SYSTEM, 1.3, 0.6)

            vo.wait_until("ModuleNotFoundError")
            out = t.print(self, [*ISO_OUT[:2], (ISO_OUT[2], ERR)], run_time=0.6)
            err = out[2]
            p_after = self.bare_prompt(t)
            self.play(Indicate(err, color=ERR, scale_factor=1.05), run_time=0.7)
            self.add(err)
            vo.wait_until("On this VM")
            self.flash(err, substring(err, "'googletrans'"), ERR, 1.2, 0.7)
            vo.wait_until("only in the venv")
            only = row_tag("only in .venv", VENV)
            self.pin(err, beside(only, err), run_time=0.5)

        # ========================================================== 1 · V2: the system's shelves
        sys_st = stack([CUR, "standard library", LOCAL_S, APT_S], S1_L, S1_R, B1, {2: SYSTEM, 3: SYSTEM},
                       std="standard library · 3.11")
        apt_j = on_board(jar_row(3, SYSTEM), sys_st.boards[3])
        vb_board = Line([VB_L + 0.2, VB_BOARD, 0], [VB_R - 0.2, VB_BOARD, 0], color=VENV, stroke_width=5)
        v_jars = on_board(jar_row(11, VENV, 0.06), vb_board)
        v_gt = name_tag(v_jars[GT_VENV], "googletrans", INK, 22)
        v_head = mono(SITE_S, 22, VENV)
        v_head.move_to([VB_L + 0.25 + v_head.width / 2, VB_BOARD + 1.2, 0])
        vb_top, vb_bot = v_head.get_top()[1] + 0.17, VB_BOARD - 0.52
        vb_frame = box(VB_R - VB_L, vb_top - vb_bot, VENV, fill_opacity=0.06)
        vb_frame.move_to([(VB_L + VB_R) / 2, (vb_top + vb_bot) / 2, 0])
        vbox = VGroup(vb_frame, v_head, vb_board, v_jars, v_gt)
        not_list = label("not on python3's list", 22, S.GREY).next_to(vb_frame, DOWN, buff=0.18)
        lt = beam(S1_L - 0.08, S1_R + 0.08, B1[0])

        with self.voiceover(SAY[1]) as vo:
            # the strip keeps the command's two rows and its error line; the rest (and the tags) fade
            # together, then the shelves come in from the top while the terminal shrinks under them
            gone = [ln for ln in t.lines if ln not in (r0, r1, err)]
            self.unpin([(err, only)], 0.35, FadeOut(VGroup(*gone)), FadeOut(VGroup(app_box, lead, old_tag, ev)))
            t.lines.submobjects = [r0, r1, err]
            rows = list(sys_st.rows)
            self.resize(t, 3, run_time=0.9,
                        extra=[LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows[:3]],
                                           FadeIn(VGroup(rows[3], apt_j), shift=DOWN * 0.1), lag_ratio=0.35)])
            self.play(FadeIn(vbox, shift=LEFT * 0.2), run_time=0.5)

            vo.wait_until("scans its own list")
            self.play(FadeIn(lt), run_time=0.3)
            self.play(lt.animate.shift(DOWN * (B1[0] - B1[3])), run_time=2.0, rate_func=linear)
            vo.wait_until("The venv's shelf")
            self.play(Indicate(vb_frame, color=VENV, scale_factor=1.04), FadeIn(not_list, shift=UP * 0.1),
                      run_time=0.8)
            vo.wait_until("comes up empty")
            nf = cross_mark(0.26, ERR, stroke=5).next_to(lt.text, LEFT, buff=0.25)
            self.play(lt.rect.animate.set_fill(ERR, 0.25), lt.text.animate.set_color(ERR), Create(nf), run_time=0.5)
            self.play(Indicate(err, color=ERR, scale_factor=1.05), run_time=0.7)
            self.add(err)

        # ========================================================== 2 · uv run: the venv's python
        lt2 = beam(VB_L + 0.1, VB_R - 0.1, VB_BOARD)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(not_list), run_time=0.3)
            ucmd = self.type_cmd(t, UVRUN, 1.5)
            u0, u1 = ucmd.rows
            x2 = row_tag("extra")
            self.pin(u1, beside(x2, u1), run_time=0.3)
            vo.wait_until("printing where")
            self.flash(u1, substring(u1, "print(sys.prefix)"), S.WHITE, 1.15, 0.8)
            # the output lands as "It works" is spoken (the strip scrolls, then the line fades in: ~0.7 s);
            # the light jumps into the venv's box and finds the jar
            lead_in = vo.time_until("It works") - 0.7
            if lead_in > 1 / 15:
                self.wait(lead_in)
            pre = t.print(self, [PREFIX], run_time=0.35)[0]
            self.play(Transform(lt, lt2), FadeOut(nf), run_time=0.5)
            ok2 = check_mark(0.3, LOOKUP).next_to(lt2.text, LEFT, buff=0.22)
            self.play(Indicate(v_jars[GT_VENV], color=LOOKUP, scale_factor=1.6), Indicate(v_gt, color=VENV),
                      Create(ok2), run_time=0.6)
            vo.wait_until("and the answer is")
            pb = row_bar(pre, VENV, 0.25)
            pv = substring(pre, ".venv")
            self.pin(pre, pb, run_time=0.4, anim=AnimationGroup(FadeIn(pb), pv.animate.set_color(VENV)),
                     behind=True)
            vo.wait_until("our dot venv")
            self.flash(pre, pv, VENV, 1.35, 0.8)

        # ========================================================== 3 · imagine the part-1 VM (PONDER 4)
        vm = DashedVMobject(RoundedRectangle(width=7.6, height=2.9, corner_radius=0.14), num_dashes=70,
                            dashed_ratio=0.55).set_stroke(S.GREY, 2.5).move_to([0, 1.0, 0])
        vm_name = tag("part-1 VM", S.GREY, size=24)
        vm_ill = tag("illustration · what if", S.GREY)

        def on_edge(frame, y_top, x_name, x_ill_right):
            vm_name.move_to([x_name + vm_name.width / 2, y_top, 0])
            vm_ill.move_to([x_ill_right - vm_ill.width / 2, y_top, 0])

        on_edge(vm, vm.get_top()[1], vm.get_left()[0] + 0.45, vm.get_right()[0] - 0.45)
        imp = mono_line(PY3, 26, INK).move_to([0, 1.55, 0])
        imp_py = substring(imp, "python3")
        sys_py = mono("python3 (system)", 24, SYSTEM)
        no_venv_t = mono("no .venv", 24, S.GREY)
        no_venv = VGroup(box(no_venv_t.width + 0.5, no_venv_t.height + 0.3, S.GREY, dashed=True), no_venv_t)
        no_venv_t.move_to(no_venv[0])
        facts = VGroup(sys_py, no_venv).arrange(RIGHT, buff=0.9).move_to([0, 0.45, 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(sys_st, apt_j, vbox, lt, ok2)),
                      FadeOut(VGroup(t.box, t.bar, t.dots, t.title, t.lines)), run_time=0.7)
            for ln in list(t.lines):
                t.lines.remove(ln)
            self.play(Create(vm), FadeIn(vm_name, shift=DOWN * 0.1), FadeIn(vm_ill, shift=DOWN * 0.1),
                      run_time=1.0)
            vo.wait_until("Same import")
            self.play(FadeIn(imp, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("system python3")
            self.play(imp_py.animate.set_color(SYSTEM), FadeIn(sys_py, shift=UP * 0.15), run_time=0.6)
            self.add(imp)
            vo.wait_until("no venv")
            self.play(FadeIn(no_venv, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Does it work")
            self.play(Indicate(imp, color=S.WHITE, scale_factor=1.06), run_time=0.8)

        card = ponder_card(PONDER_Q)
        card.move_to([0, -3.35 + card.height / 2, 0])
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=6)

        # ========================================================== 4 · the part-1 shelves: found
        big = DashedVMobject(RoundedRectangle(width=13.1, height=F_TOP - F_BOT, corner_radius=0.14),
                             num_dashes=150, dashed_ratio=0.55).set_stroke(S.GREY, 2.5)
        big.move_to([0, (F_TOP + F_BOT) / 2, 0])
        p1 = stack([CUR, "standard library", LOCAL_S, APT_S], FULL_L, FULL_R, B4, {2: SYSTEM, 3: SYSTEM},
                   std="standard library · 3.11")
        pip_j = on_board(jar_row(12, SYSTEM), p1.boards[2])
        apt4 = on_board(jar_row(4, SYSTEM), p1.boards[3])
        p_gt = name_tag(pip_j[GT_PIP], "googletrans", INK, 22)
        title_l = mono("python3 (system)", 22, SYSTEM).move_to([0, TITLE_Y, 0]).align_to([FULL_L, 0, 0], LEFT)
        lt4 = beam(FULL_L - 0.08, FULL_R + 0.08, B4[0])
        where = mono(WHERE_OUT, 22, LOOKUP)
        where.move_to([FULL_R - 0.1 - where.width / 2, B4[2] - 0.26, 0])
        sw = tag("system-wide", S.GREY)
        sw.move_to([-0.6, B4[2] + 0.27, 0])
        imp_word = substring(imp, "import googletrans")

        with self.voiceover(SAY[4]) as vo:
            rest = VGroup(*[g for g in imp.glyphs if g not in imp_word.submobjects])
            self.remove(imp)                                  # split: the words that move, the rest that fades
            self.add(rest, imp_word)
            self.play(FadeOut(card), FadeOut(rest), FadeOut(no_venv), run_time=0.4)
            self.play(ReplacementTransform(vm, big),
                      vm_name.animate.move_to([-5.8 + vm_name.width / 2, F_TOP, 0]),
                      vm_ill.animate.move_to([6.05 - vm_ill.width / 2, F_TOP, 0]),
                      ReplacementTransform(sys_py, title_l),
                      ReplacementTransform(imp_word, lt4.text),      # the command's words become the light
                      run_time=1.0)
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in p1.rows], lag_ratio=0.12),
                      FadeIn(pip_j), FadeIn(apt4), run_time=0.7)

            vo.wait_until("sudo pip put")                     # (already spoken: the light sets off at once)
            self.play(FadeIn(lt4.rect), run_time=0.3)
            self.play(lt4.animate.shift(DOWN * (B4[0] - B4[2])), run_time=1.2, rate_func=linear)
            vo.wait_until("system-wide")
            self.play(FadeIn(sw, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("user local shelf")
            self.play(Indicate(p1.texts[2], color=SYSTEM, scale_factor=1.08),
                      Indicate(pip_j[GT_PIP], color=LOOKUP, scale_factor=1.6), FadeIn(p_gt, shift=UP * 0.15),
                      run_time=0.7)
            ok4 = check_mark(0.3, LOOKUP).next_to(where, LEFT, buff=0.22)
            # the light's label becomes the answer: where the import found it (09-where.txt line 2)
            self.play(FadeTransform(lt4.text, where, stretch=False), Create(ok4), run_time=0.6)
            vo.wait_until("every program")
            self.play(Indicate(sw, color=S.WHITE, scale_factor=1.12), run_time=0.8)
            vo.wait_until("Same import")
            self.play(Indicate(title_l, color=SYSTEM, scale_factor=1.08), run_time=0.7)
            vo.wait_until("different answer")
            self.play(Indicate(where, color=LOOKUP, scale_factor=1.04), run_time=0.8)

        # ========================================================== 5 · a venv ignores them
        p1h = stack([CUR, "standard library", LOCAL_S, APT_S], *HALF_L, B4, {2: SYSTEM, 3: SYSTEM},
                    std="standard library · 3.11")
        pip_t = pile_targets(pip_j, 6, p1h.boards[2])
        apt_t = pile_targets(apt4, 2, p1h.boards[3])
        vs = stack([CUR, "standard library", SITE_S], *HALF_R, B4[:3], {2: VENV}, std="standard library")
        vjars = jar_row(11, VENV, 0.04)
        for j, p in zip(vjars, pile_targets(vjars, 5, vs.boards[2])):
            j.move_to(p)
        vs_gt = name_tag(vjars[GT_VENV], "googletrans", INK, 22)
        vs_gt.shift(LEFT * max(0, vs_gt.get_right()[0] - HALF_R[1]))     # keep it over the pile, in frame
        title_r = mono(".venv/bin/python", 22, VENV).move_to([0, TITLE_Y, 0]).align_to([HALF_R[0], 0, 0], LEFT)
        divider = DashedLine([0, TITLE_Y + 0.05, 0], [0, B4[3] - 0.15, 0], color=S.GREY, stroke_width=2,
                             dash_length=0.12)
        lt5 = beam(HALF_R[0] - 0.08, HALF_R[1] + 0.08, B4[0])
        caption = label("a venv ignores whatever the system Python has", 28, INK).move_to([0, -3.03, 0])
        cap_bg = BackgroundRectangle(caption, color=S.BG, fill_opacity=0.9, buff=0.12)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(lt4.rect, where, ok4, p_gt, sw)), run_time=0.4)
            moves = [Transform(p1.rows[i], p1h.rows[i]) for i in range(4)]
            moves += [j.animate.move_to(p) for j, p in zip(pip_j, pip_t)]
            moves += [j.animate.move_to(p) for j, p in zip(apt4, apt_t)]
            self.play(*moves, run_time=1.0)
            self.play(Create(divider), FadeIn(title_r, shift=DOWN * 0.1),
                      LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in vs.rows], lag_ratio=0.15),
                      FadeIn(vjars, shift=LEFT * 0.2), run_time=1.0)
            vo.wait_until("messy part-1 VM")
            self.play(LaggedStart(*[Indicate(j, color=SYSTEM, scale_factor=1.4) for j in pip_j], lag_ratio=0.06),
                      run_time=1.0)
            vo.wait_until("a venv would")
            self.play(Indicate(title_r, color=VENV, scale_factor=1.12), run_time=0.7)
            vo.wait_until("everything sudo pip")
            self.play(Indicate(VGroup(p1.rows[2], p1.rows[3], pip_j, apt4), color=SYSTEM, scale_factor=1.03),
                      run_time=0.9)
            vo.wait_until("because those shelves")
            self.play(FadeIn(lt5), run_time=0.3)
            self.play(lt5.animate.shift(DOWN * (B4[0] - B4[2])), run_time=1.3, rate_func=linear)
            ok5 = check_mark(0.3, LOOKUP).next_to(lt5.text, LEFT, buff=0.22)
            self.play(Indicate(vjars[GT_VENV], color=LOOKUP, scale_factor=1.6), FadeIn(vs_gt, shift=UP * 0.15),
                      Create(ok5), run_time=0.7)
            vo.wait_until("That's the whole lesson")
            self.play(FadeIn(cap_bg), FadeIn(caption, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(caption, color=S.WHITE, scale_factor=1.04), run_time=0.8)

        self.wait(0.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
