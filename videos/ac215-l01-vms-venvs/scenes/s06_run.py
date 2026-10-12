"""S06 · Run it, and read the traceback (README step 9, then an extra run with a typo).

Beats (script.md "## S06", one voiceover block each):
 0  TRACKER A9. The house terminal (12 rows) types `python3 cli.py`; the `3` is ringed YELLOW and a
    row tag under it says plain `python` doesn't exist here. expected/10-run-default.txt lines 2-15
    print as they are named (banner line by line, arguments, input, output); the Output line turns
    GREEN with an `expected output` tag. GREY note "red error? keep watching". ▶ your turn sits on
    the terminal frame: the 14 output rows have scrolled the command itself away.
 1  The es and fr runs (each folds onto 3 rows: the quoted text can't be split). On the es command
    `-t`, `-s`, `-d` are underlined with GREY labels "text", "source", "destination" as they are
    named; expected/11-run-es.txt and 12-run-fr.txt lines 12-15; ▶ your turn and "copy from the
    README, quotes included" beside the fr command (its quotes flash YELLOW); both Output lines
    turn GREEN with `expected output` tags.
 2  The terminal clears, grows to 13 rows, gets `real capture · 2026-10-12` on its frame, types
    `python3 cli.py` -> debian12-part-a/10-run-default.txt lines 14-15, …, 24-26, …, 42 (wrap); the
    traceback prints RED-tinted and its last line (3 rows) lights up RED; on "Let's read it" a
    YELLOW reading bar sweeps down the traceback.
 3  V8. Lines 24 and 42 lift out of the terminal (which fades) into two full-width RED boxes at
    20 pt; line 26 lifts into the PINK text of a downward chain arrow between them. Legends
    "1 · the cause" / "2 · the wrapper" appear as the narration names them; a YELLOW eye goes from
    box 2 up to box 1, with a GREY note "on your screen: scroll up".
 4  Zoom on box 1: box 2 and the chain leave, box 1 drops; "429" ringed YELLOW, chip "HTTP 429 =
    too many requests". Above it S02's V6 replays: PINK "HTTPS GET" from the BLUE VM to the BLUE
    translate.googleapis.com cloud; a RED arrow comes back, labelled by the 429 flying up from the
    box. "Nothing on the VM was broken": a GREEN check in the VM.
 5  Both boxes back (compact) with CODE(cli.py: 32-37) full width under them: line 32 lights on
    "catches anything", 33-36 on "a friendlier message" (box 2's text answers); `from error`
    underlines PINK and flies up to label the PINK chain arrow.
 6  TRACKER A9 · extra. The boxes shrink away; a fresh 13-row terminal types `python3 cli.py -t
    hello -d xx` (extra; folds onto 2 rows); `xx` underlines RED; 14-badlang.txt lines 14-15, …,
    21-23, …, 39 (wrap); line 21 lights up RED; then V8 updates: lines 21, 23 and 39 lift into the
    boxes; "network/IP" underlines RED with a RED "network?" tag on box 2's bottom edge; a GREY
    "erratum · cli.py lines 32–37" tag under box 2 (BRIEF erratum 5); a GREY chip "valid codes:
    README.md · table at the bottom".
 7  Three chips at right under "if you hit a 429": wait and retry · a VM in another region · run it
    on your laptop. At left, `Input: I love cheese` (debian12-part-a/10-run-default.txt line 14)
    with a GREEN check, "got this far → your packages work", and a GREY note "can't open file
    'cli.py'? → cd simple-translate". Fade out to an empty frame.

Every terminal line comes from capture(...); every code line from excerpt("cli.py", a, b).
The terminals scroll with calm_scroll() (rows leaving the top fade in place instead of sliding up
over the title bar), a scene-local stand-in until devops.Terminal._make_room does the same.
"""

import textwrap
import types

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (OUTPUT, TERM_BG, box, check_mark, chip, cloud, code_panel,
                              code_span, glyph_range, label, line_bar, line_pitch, machine_box, mono,
                              mono_line, substring, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, ERR, INK, LAPTOP, LOOKUP, NARRATION, P_REPO, TURN, VENV, capture, excerpt,
                    extra_tag, recorded_tag, term, tracker_a, your_turn)

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ commands (README spelling)
RUN = "python3 cli.py"
RUN_ES = 'python3 cli.py -t "Good morning. It is a good morning for cheese." -s "en" -d "es"'
RUN_FR = 'python3 cli.py -t "Good afternoon. Would you like some cheese?" -s "en" -d "fr"'
BADLANG = "python3 cli.py -t hello -d xx"                  # extra: not in the README

# ------------------------------------------------------------------ real outputs (pick index = file line - 1)
_exp = capture("10-run-default", "expected")
assert _exp.cmd == RUN
EXP_OUT = _exp.pick((1, 14))                               # file lines 2-15
assert EXP_OUT[12].startswith("Input:") and EXP_OUT[13].startswith("Output:")
_es = capture("11-run-es", "expected")
assert _es.cmd == RUN_ES
ES_OUT = _es.pick((11, 14))                                # file lines 12-15
_fr = capture("12-run-fr", "expected")
assert _fr.cmd == RUN_FR
FR_OUT = _fr.pick((11, 14))                                # file lines 12-15
assert ES_OUT[3].startswith("Output:") and FR_OUT[3].startswith("Output:")

_run = capture("10-run-default")                           # debian12-part-a: the real 429
assert _run.cmd == RUN
OUT_429 = _run.pick(13, 14, (23, 25), 41)                  # file lines 14-15, …, 24-26, …, 42
L14, L24, L26, L42 = (_run.lines[n - 2] for n in (14, 24, 26, 42))
assert L14 == "Input: I love cheese" and L24.startswith("Exception: Unexpected status code")
assert L26.startswith("The above exception") and L42.startswith("RuntimeError:")
_bad = capture("14-badlang")
assert _bad.cmd == BADLANG
OUT_BAD = _bad.pick(13, 14, (20, 22), 38)                  # file lines 14-15, …, 21-23, …, 39
B21, B23, B39 = (_bad.lines[n - 2] for n in (21, 23, 39))
assert B21 == "ValueError: invalid destination language" and B23 == L26 and B39 == L42

# ------------------------------------------------------------------ colours and layout
TINT = interpolate_color(ManimColor(OUTPUT), ManimColor(ERR), 0.55)   # traceback rows, RED-tinted
BOTTOM = -3.5                    # terminal bottom edge
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
PT = 20                          # V8 box text
PITCH = line_pitch(PT)
BOX_W = 12.6
X_TEXT = -BOX_W / 2 + 0.22       # left edge of the box text
PAD_T, PAD_B = 0.3, 0.2          # PAD_T leaves room under the legend tag on the top edge
LEGEND_UP = 0.06                 # the legend tag sits a little above the box's top edge
Y3 = 1.5                         # box 1 top (beats 3 and 6)
GAP3 = 1.1                       # room between the boxes for the chain arrow and line 26
DY4 = -0.6                       # beat 4: the V6 picture and box 1 sit this much lower
Y4 = 0.1 + DY4                   # box 1 top while the V6 picture is above it (beat 4)
Y5 = 2.45                        # box 1 top with the code panel under the boxes (beat 5)
GAP5 = 0.55
CHAIN_X = -2.9                   # x of the chain arrow (right of box 2's legend)
WRAP = 66                        # the RuntimeError line folds at spaces into 3 rows of <= 66


def _calm_make_room(self, scene, n_new: int, run_time: float = 0.45) -> None:
    """Terminal scrolling, scene-local: the rows leaving the top fade out where they are
    (devops' version slides them up across the title bar and above the box), then the rest
    moves up. Bound onto this scene's terminals with calm_scroll()."""
    overflow = len(self.lines) + n_new - self.rows
    if overflow <= 0:
        return
    gone = VGroup(*self.lines.submobjects[:overflow])
    stay = VGroup(*self.lines.submobjects[overflow:])
    anims = [FadeOut(gone, rate_func=lambda a: smooth(min(1.0, a / 0.4)))]
    if len(stay):
        anims.append(stay.animate(rate_func=lambda a: smooth(max(0.0, (a - 0.3) / 0.7)))
                     .shift(UP * self.pitch * overflow))
    scene.play(*anims, run_time=run_time)
    for m in gone:
        self.lines.remove(m)


def calm_scroll(t):
    t._make_room = types.MethodType(_calm_make_room, t)
    return t


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def caption_extra(tr, on: bool = True):
    """The tracker caption with (or without) ' · extra' while a non-README command is on screen."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    new = label(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY}) if on else \
        label(s, tr.size, tr.hi_color)
    new.next_to(tr.dots, RIGHT, buff=0.25)
    return Transform(tr.caption, new)


def under(g, color, y=None, stroke=4, pad=0.03) -> Line:
    y = g.get_bottom()[1] - 0.06 if y is None else y
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def line_under(line, sub, color, stroke=4):
    """Underline substring `sub` of a mono row, under the row's descenders."""
    return under(substring(line, sub), color, y=line.strut.get_bottom()[1] - 0.01, stroke=stroke)


def row_bar(rows, color, opacity=0.18, width=None, x=None) -> Rectangle:
    """A translucent bar behind one or more mono rows (their struts)."""
    top = rows[0].strut.get_top()[1] + 0.02
    bot = rows[-1].strut.get_bottom()[1] - 0.02
    if width is None:
        left = min(r.strut.get_left()[0] for r in rows) - 0.06
        right = max(r.strut.get_right()[0] for r in rows) + 0.06
        width, x = right - left, (left + right) / 2
    return Rectangle(width=width, height=top - bot, stroke_width=0).set_fill(color, opacity) \
        .move_to([x, (top + bot) / 2, 0])


def row_tag(parts, color=S.GREY, size: float = 22) -> VGroup:
    """A tag that fits inside one terminal row. parts: a string, or (text, 'mono'|'label') pairs."""
    if isinstance(parts, str):
        parts = [(parts, "label")]
    t = VGroup(*[mono(x, size, color) if k == "mono" else label(x, size, color) for x, k in parts])
    t.arrange(RIGHT, buff=0.12)
    h = 0.37
    b = RoundedRectangle(width=t.width + 0.36, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def beside(mob, line, buff=0.45, min_x=None):
    """Put `mob` right of mono row `line`, centred on the row (left edge at least min_x)."""
    x = line.strut.get_right()[0] + buff
    if min_x is not None:
        x = max(x, min_x)
    return mob.move_to([x + mob.width / 2, line.strut.get_center()[1], 0])


def on_frame(mob, t, right_pad=0.35):
    """A tag sitting on the terminal's top edge, at the right (clear of the centred title)."""
    return mob.move_to([t.box.get_right()[0] - right_pad - mob.width / 2, t.box.get_top()[1], 0])


def row_y(t, i: int) -> float:
    """Centre y of terminal row i."""
    return t._slot(i)[1] - mono_line(" ", t.size).strut.height / 2


def glyphs_of(rows) -> VGroup:
    return VGroup(*[g for r in rows for g in r.glyphs])


# ------------------------------------------------------------------ V8 · the chained traceback
def err_rows(texts, size=PT) -> VGroup:
    """Rows of an exception message; the exception's class name (before the first ':') in RED."""
    rows = VGroup()
    for i, s in enumerate(texts):
        t2c = {f"[0:{s.index(':') + 1}]": ERR} if i == 0 and ":" in s else None
        r = mono_line(s, size, INK, t2c=t2c)
        r.shift(np.array([X_TEXT, -i * PITCH, 0]) - r.strut.get_corner(UL))
        rows.add(r)
    return rows


def err_box(texts, legend: str) -> VGroup:
    """A full-width RED box holding an exception (top edge at y = 0); its legend tag sits on the
    top edge at the left. .frame .rows .legend"""
    rows = err_rows(texts)
    strut_h = rows[0].strut.height
    h = PAD_T + (len(texts) - 1) * PITCH + strut_h + PAD_B
    frame = box(BOX_W, h, ERR, fill_opacity=0.08).move_to([0, -h / 2, 0])
    rows.shift(DOWN * PAD_T)
    lg = tag(legend, ERR)
    lg.move_to([frame.get_left()[0] + 0.3 + lg.width / 2, LEGEND_UP, 0])
    g = VGroup(frame, rows, lg)
    g.frame, g.rows, g.legend = frame, rows, lg
    return g


def chain_text(s: str) -> VGroup:
    """'The above exception was the direct cause / of the following exception:' in PINK, 2 rows."""
    i = s.index(" of the following")
    rows = VGroup(mono_line(s[:i], PT, LOOKUP), mono_line(s[i + 1:], PT, LOOKUP))
    rows[1].shift(rows[0].strut.get_corner(UL) + DOWN * PITCH - rows[1].strut.get_corner(UL))
    return rows


def chain_arrow(top: float, bottom: float) -> Arrow:
    return Arrow([CHAIN_X, top, 0], [CHAIN_X, bottom, 0], buff=0.1, color=LOOKUP, stroke_width=5,
                 tip_length=0.2, max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=20)


def v8(top_text, bottom_texts, chain_s, y_top=Y3, gap=GAP3):
    """Box 1 (the cause), the chain (arrow + line 26's words) and box 2 (the wrapper)."""
    b1 = err_box(top_text, "1 · the cause").shift(UP * y_top)
    b2 = err_box(bottom_texts, "2 · the wrapper")
    b2.shift(UP * (b1.frame.get_bottom()[1] - gap))
    arr = chain_arrow(b1.frame.get_bottom()[1], b2.frame.get_top()[1])
    ct = chain_text(chain_s)
    ct.shift(np.array([CHAIN_X + 0.4, (b1.frame.get_bottom()[1] + b2.frame.get_top()[1]) / 2, 0])
             - np.array([ct.get_left()[0], ct.get_center()[1], 0]))
    return b1, arr, ct, b2


def eye_glyph(w: float = 0.62, color=TURN) -> VGroup:
    up = ArcBetweenPoints(LEFT * w / 2, RIGHT * w / 2, angle=-2.0)
    dn = ArcBetweenPoints(LEFT * w / 2, RIGHT * w / 2, angle=2.0)
    lids = VGroup(up, dn).set_stroke(color, 3.5)
    iris = Circle(radius=w * 0.2).set_stroke(color, 2.5)
    pupil = Circle(radius=w * 0.09).set_stroke(width=0).set_fill(color, 1)
    return VGroup(lids, iris, pupil)


def mixed(parts, color=S.GREY, size: float = 22) -> VGroup:
    """A line mixing house text and mono: parts = [(text, 'mono'|'label'), ...]."""
    g = VGroup(*[mono(x, size, color) if k == "mono" else label(x, size, color) for x, k in parts])
    return g.arrange(RIGHT, buff=0.12)


def boxed(g, color=S.GREY, pad_x=0.24, pad_y=0.14, fill_opacity=0.12) -> VGroup:
    """A chip around any group (border in its colour, faint tint)."""
    b = box(g.width + 2 * pad_x, g.height + 2 * pad_y, color, fill_opacity=fill_opacity,
            radius=(g.height + 2 * pad_y) / 2.6)
    g.move_to(b)
    out = VGroup(b, g)
    out.box, out.text = b, g
    return out


# ------------------------------------------------------------------ the scene
class RunIt(VoiceScene):
    # ------------------------------------------------------------- terminal helpers (as in S04)
    def pin(self, line, mob, run_time=0.4, anim=None, behind=False):
        """Show `mob` beside a terminal row and make it part of that row (it scrolls with it)."""
        self.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
        return self.attach(line, mob, behind)

    def attach(self, line, mob, behind=False):
        """Make `mob` part of terminal row `line` (re-adding the row: animating a substring of a
        row splits it out of the scene's list, and a mark added to it would not be drawn)."""
        self.remove(mob)
        if behind:
            line.submobjects.insert(0, mob)
        else:
            line.add(mob)
        self.add(line)
        return mob

    def unpin(self, pairs, run_time=0.3, *extra):
        """Fade out pinned marks and take them off their rows."""
        self.play(*[FadeOut(m) for _, m in pairs], *extra, run_time=run_time)
        for line, m in pairs:
            if m in line.submobjects:
                line.remove(m)

    def resize(self, t, rows, run_time=0.8, extra=()):
        """Grow or shrink the (empty) terminal to `rows`, bottom edge fixed."""
        ref = term(prompt=t.prompt, rows=rows)
        ref.shift(np.array([-ref.box.get_center()[0], BOTTOM - ref.box.get_bottom()[1], 0]))
        self.play(Transform(t.box, ref.box), Transform(t.bar, ref.bar), t.dots.animate.move_to(ref.dots),
                  t.title.animate.move_to(ref.title), *extra, run_time=run_time)
        t.rows = rows
        return t

    def lift(self, rows_from, rows_to, fade, *extra, run_time=1.2):
        """Glyphs of terminal rows lift out: everything else in `fade` (the terminal) fades first,
        then copies of the rows fly to their new rows (with `extra`). rows_from / rows_to: lists
        of lists of mono rows."""
        srcs, tgts = [], []
        for a, b in zip(rows_from, rows_to):
            srcs.append(glyphs_of(a).copy())
            tgts.append(glyphs_of(b))
        self.add(*srcs)
        self.play(FadeOut(fade), run_time=0.5)
        self.play(*[Transform(s, d) for s, d in zip(srcs, tgts)], *extra, run_time=run_time)
        self.remove(*srcs)

    # ------------------------------------------------------------- the scene
    def construct(self):
        assert len(SAY) == 8, f"S06 has {len(SAY)} SAY lines; this scene times 8"

        tr = place_tracker(tracker_a(8))
        t = calm_scroll(term(prompt=P_REPO, rows=12))
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
        cw = t.max_chars

        # ========================================================== 0 · python3 cli.py (expected)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.6)
            self.play(tr.goto(9), run_time=0.5)
            vo.wait_until("Type python3")
            cmd0 = t.type(self, RUN, 0.7)

            vo.wait_until("with the 3")
            i3 = len(P_REPO) + 1 + RUN.index("3")
            three = glyph_range(cmd0, i3, i3 + 1)
            ring = Circle(radius=0.2, color=TURN, stroke_width=3).move_to(three)
            self.play(three.animate.set_color(TURN), Create(ring), run_time=0.6)
            self.attach(cmd0, ring)

            vo.wait_until("since plain python")
            py_note = row_tag([("python", "mono"), ("alone doesn't exist here", "label")])
            py_x = substring(cmd0, "python3").get_left()[0] - 0.18
            py_note.move_to([py_x + py_note.width / 2, row_y(t, 1), 0])
            self.pin(cmd0, py_note, anim=FadeIn(py_note, shift=UP * 0.1), run_time=0.5)

            vo.wait_until("You should see the banner")
            t.print(self, EXP_OUT[0:8], run_time=1.5, lag=0.35)          # file lines 2-9
            # each line arrives as it is named (the words come ~1 s apart: no extra beats here)
            vo.wait_until("the arguments")
            t.print(self, EXP_OUT[8:11], run_time=0.5)                   # file lines 10-12
            vo.wait_until("your input")
            t.print(self, EXP_OUT[11:13], run_time=0.4)                  # file lines 13-14
            vo.wait_until("and the output")
            out0 = t.print(self, EXP_OUT[13:14], run_time=0.35)[0]       # file line 15
            gbar0 = row_bar([out0], VENV, 0.2)
            self.play(FadeIn(gbar0), out0.glyphs.animate.set_color(VENV), run_time=0.45)
            self.attach(out0, gbar0, behind=True)
            vo.wait_until("I love cheese, in Italian")
            self.play(Indicate(substring(out0, "Adoro il formaggio"), color=INK, scale_factor=1.05),
                      run_time=0.8)
            exp0 = beside(row_tag("expected output"), out0)
            self.pin(out0, exp0, run_time=0.4)

            vo.wait_until("If you get a long red error")
            banner_row = t.lines[2]
            red_note = row_tag("red error? keep watching")
            red_note.move_to([t.box.get_right()[0] - 0.35 - red_note.width / 2,
                              banner_row.strut.get_center()[1], 0])
            self.pin(banner_row, red_note, run_time=0.5)
            vo.wait_until("don't change anything")
            self.play(Indicate(red_note.text, color=S.WHITE, scale_factor=1.12), run_time=0.8)
            vo.wait_until("we'll read ours together")
            self.play(Wiggle(red_note, scale_value=1.06, rotation_angle=0.015 * TAU), run_time=0.9)

            vo.wait_until("Pause and try it")
            yt0 = on_frame(your_turn(), t)
            self.play(FadeIn(yt0, shift=DOWN * 0.1), run_time=0.4)

        # ========================================================== 1 · the es and fr runs
        with self.voiceover(SAY[1]) as vo:
            es = t.type(self, RUN_ES, 1.9)
            ra, rb, rc = es.rows
            assert rc.text.strip() == '-d "es"', es.rows

            vo.wait_until("Dash t gives")
            s_t = '-t "Good morning. It is a good morning for cheese."'
            ul_t = line_under(rb, s_t, S.GREY, stroke=3)
            lab_t = label("text", 22, S.GREY).move_to([substring(rb, s_t[3:]).get_center()[0],
                                                       rc.strut.get_center()[1], 0])
            self.play(Create(ul_t), FadeIn(lab_t, shift=UP * 0.1), FadeOut(yt0),
                      Indicate(substring(rb, "-t"), color=INK, scale_factor=1.3), run_time=0.6)
            vo.wait_until("dash s")
            ul_s = line_under(rb, '-s "en"', S.GREY, stroke=3)
            lab_s = label("source", 22, S.GREY).move_to([substring(rb, '-s "en"').get_center()[0],
                                                         rc.strut.get_center()[1], 0])
            self.play(Create(ul_s), FadeIn(lab_s, shift=UP * 0.1),
                      Indicate(substring(rb, "-s"), color=INK, scale_factor=1.3), run_time=0.6)
            vo.wait_until("dash d")
            ul_d = line_under(rc, '-d "es"', S.GREY, stroke=3)
            lab_d = beside(label("destination", 22, S.GREY), rc, buff=0.35)
            self.play(Create(ul_d), FadeIn(lab_d, shift=LEFT * 0.1),
                      Indicate(substring(rc, "-d"), color=INK, scale_factor=1.3), run_time=0.6)
            opt_marks = [(rb, ul_t), (rb, ul_s), (rc, lab_t), (rc, lab_s), (rc, ul_d), (rc, lab_d)]
            for row, m in opt_marks:                  # they scroll with the command
                self.attach(row, m)
            es_out = t.print(self, ES_OUT, run_time=0.5)                  # file lines 12-15
            ex_es = beside(row_tag("expected output"), es_out[-1])
            self.pin(es_out[-1], ex_es, run_time=0.3)

            vo.wait_until("Copy them from the README")
            self.unpin(opt_marks, 0.3)
            fr = t.type(self, RUN_FR, 1.1)
            fc = fr.rows[-1]
            yt1 = beside(your_turn(), fc)
            copy_note = beside(row_tag("copy from the README, quotes included"), fc,
                               min_x=yt1.get_right()[0] + 0.3)
            quotes = VGroup(*[g for r in fr.rows for i, ch in enumerate(r.text) if ch == '"'
                              for g in glyph_range(r, i, i + 1)])
            vo.wait_until("quotes included")
            self.play(FadeIn(copy_note, shift=LEFT * 0.1),
                      *[Indicate(q, color=TURN, scale_factor=1.8) for q in quotes], run_time=0.7)
            self.attach(fc, copy_note)
            vo.wait_until("pause to run both")
            self.pin(fc, yt1, run_time=0.4)
            fr_out = t.print(self, FR_OUT, run_time=0.4)                  # file lines 12-15
            ex_fr = beside(row_tag("expected output"), fr_out[-1])
            self.pin(fr_out[-1], ex_fr, run_time=0.3)
            marks1 = [(es_out[-1], ex_es), (fr_out[-1], ex_fr)]

            vo.wait_until("One comes back in Spanish")
            for o, k in ((es_out[-1], 0), (fr_out[-1], 1)):
                if k:
                    vo.wait_until("the other in French")
                gb = row_bar([o], VENV, 0.2)
                self.play(FadeIn(gb), o.glyphs.animate.set_color(VENV), run_time=0.4)
                self.attach(o, gb, behind=True)
                self.play(Indicate(VGroup(*o.glyphs[7:]), color=INK, scale_factor=1.04), run_time=0.6)

        # ========================================================== 2 · the real run: a 429
        rec = recorded_tag("real capture · 2026-10-12")
        lines429 = []
        for s in OUT_429:
            col = S.GREY if s == "…" else (OUTPUT if s.startswith("Input:") else TINT)
            lines429.append((s, col))

        with self.voiceover(SAY[2]) as vo:
            self.unpin(marks1 + [(fc, yt1), (fc, copy_note)], 0.3)
            t.clear(self, run_time=0.4)
            self.resize(t, 13, run_time=0.7)
            on_frame(rec, t)
            self.play(FadeIn(rec, shift=DOWN * 0.1), run_time=0.5)
            cmd2 = t.type(self, RUN, 0.7)

            vo.wait_until("Google refused")
            out2 = t.print(self, lines429, wrap=True, run_time=1.8, lag=0.1)
            assert len(t.lines) == 13, len(t.lines)
            r24, r26, r42 = list(out2[3:5]), list(out2[6:8]), list(out2[9:12])
            assert "".join(r.text for r in r24) == L24 and "".join(r.text for r in r42) == L42
            assert "".join(r.text for r in r26) == L26

            vo.wait_until("ended in this long")
            bar42 = row_bar(r42, ERR, 0.2, width=t.box.width - 0.3, x=t.box.get_center()[0])
            self.play(FadeIn(bar42), glyphs_of(r42).animate.set_color(ERR), run_time=0.7)
            self.play(Indicate(glyphs_of(r42), color=ERR, scale_factor=1.03), run_time=0.8)

            vo.wait_until("Let's read it")
            # a reading bar sweeps down the traceback, row by row
            sweep = Rectangle(width=t.box.width - 0.3, height=t.pitch, stroke_width=0).set_fill(TURN, 0.16)
            sweep.move_to([t.box.get_center()[0], out2[1].strut.get_center()[1], 0])
            self.play(FadeIn(sweep), run_time=0.25)
            self.play(sweep.animate.move_to([t.box.get_center()[0], out2[8].strut.get_center()[1], 0]),
                      run_time=2.0, rate_func=linear)
            self.play(FadeOut(sweep), run_time=0.3)
            self.remove(sweep)

        # ========================================================== 3 · V8: two errors, chained
        wrap42 = textwrap.wrap(L42, WRAP)
        assert len(wrap42) == 3
        b1, arr3, ct3, b2 = v8([L24], wrap42, L26)
        eye = eye_glyph()
        eye_start = np.array([5.65, b2.frame.get_center()[1], 0])
        eye_end = np.array([5.65, b1.frame.get_top()[1] + 0.4, 0])
        eye.move_to(eye_start)
        scroll_note = label("on your screen: scroll up", 22, S.GREY)
        scroll_note.move_to([eye_end[0] - 0.55 - scroll_note.width / 2, eye_end[1], 0])

        with self.voiceover(SAY[3]) as vo:
            self.lift([r24, r42, r26], [b1.rows, b2.rows, ct3], VGroup(t, rec, bar42),
                      FadeIn(b1.frame), FadeIn(b2.frame), run_time=1.2)
            self.add(b1.frame, b1.rows, b2.frame, b2.rows, ct3)
            vo.wait_until("two errors")
            self.play(Indicate(b1.frame, color=ERR, scale_factor=1.02),
                      Indicate(b2.frame, color=ERR, scale_factor=1.02), run_time=0.9)

            vo.wait_until("The line between them")
            self.play(GrowArrow(arr3), Indicate(ct3, color=LOOKUP, scale_factor=1.05), run_time=0.9)
            vo.wait_until("the first one directly")
            self.play(FadeIn(b1.legend, scale=0.8), run_time=0.5)
            vo.wait_until("caused the second")
            self.play(FadeIn(b2.legend, scale=0.8),
                      ShowPassingFlash(arr3.copy().set_stroke(width=9), time_width=0.6), run_time=0.8)

            vo.wait_until("Most people read only")
            self.play(FadeIn(eye, scale=0.6), run_time=0.5)
            self.play(Indicate(b2.rows, color=ERR, scale_factor=1.02), run_time=0.8)
            vo.wait_until("just the wrapper")
            self.play(Indicate(b2.legend.text, color=ERR, scale_factor=1.2), run_time=0.8)

            vo.wait_until("Scroll up to the first")
            self.play(eye.animate.move_to(eye_end), FadeIn(scroll_note, shift=UP * 0.2), run_time=1.0)
            vo.wait_until("that's the cause")
            self.play(Indicate(b1.legend.text, color=TURN, scale_factor=1.2),
                      Circumscribe(b1.frame, color=TURN, buff=0.05, stroke_width=3), run_time=1.0)

        # ========================================================== 4 · the cause: HTTP 429
        d429 = substring(b1.rows[0], "429")
        ring429 = Ellipse(width=d429.width + 0.5, height=0.6, color=TURN, stroke_width=4)
        vm = machine_box("VM", "ac215-l01", width=3.3, height=1.75, color=CLOUD)
        vm.move_to([-6.3 + vm.width / 2, 2.62 + DY4 - vm.height / 2, 0])
        app = mono("cli.py", 22, INK).move_to(vm.body).shift(LEFT * 0.35)
        ok = check_mark(0.36, VENV).next_to(app, RIGHT, buff=0.3)
        gcl = cloud(2.4, CLOUD).move_to([4.3, vm.body.get_center()[1] + 0.12, 0])
        host = mono("translate.googleapis.com", 20, CLOUD).next_to(gcl, DOWN, buff=0.15)
        y_get, y_ret = gcl.get_center()[1] + 0.25, gcl.get_center()[1] - 0.3
        x_vm, x_cl = vm.get_right()[0] + 0.05, gcl.get_left()[0] + 0.12
        get = Arrow([x_vm, y_get, 0], [x_cl, y_get, 0], buff=0, color=LOOKUP, stroke_width=5,
                    tip_length=0.22, max_tip_length_to_length_ratio=0.1)
        get_l = mono("HTTPS GET", 22, LOOKUP).next_to(get, UP, buff=0.12)
        ret = Arrow([x_cl, y_ret, 0], [x_vm, y_ret, 0], buff=0, color=ERR, stroke_width=5,
                    tip_length=0.22, max_tip_length_to_length_ratio=0.1)
        ret_l = mono("429", 26, ERR).next_to(ret, DOWN, buff=0.12)
        v6 = VGroup(vm, app, gcl, host)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(b2, arr3, ct3, eye, scroll_note), shift=DOWN * 0.3), run_time=0.5)
            self.play(b1.animate.shift(DOWN * (Y3 - Y4)), run_time=0.7)
            ring429.move_to(d429)
            chip429 = chip("HTTP 429 = too many requests", ERR, size=24)
            chip429.move_to([np.clip(d429.get_center()[0], -6.3 + chip429.width / 2, 6.3 - chip429.width / 2),
                             b1.frame.get_bottom()[1] - 0.55, 0])
            vo.wait_until("status code 429")
            self.play(Create(ring429), d429.animate.set_color(TURN), run_time=0.7)
            vo.wait_until("too many requests")
            self.play(FadeIn(chip429, shift=UP * 0.15), run_time=0.6)

            vo.wait_until("Google's unofficial")
            self.play(FadeIn(v6, shift=DOWN * 0.15), run_time=0.7)
            self.play(GrowArrow(get), FadeIn(get_l, shift=UP * 0.1), run_time=0.9)
            vo.wait_until("was rate-limiting")
            self.play(GrowArrow(ret), TransformFromCopy(d429, ret_l), run_time=1.0)
            vo.wait_until("as it often does")
            for _ in range(2):
                self.play(ShowPassingFlash(get.copy().set_stroke(width=9), time_width=0.5), run_time=0.6)
                self.play(ShowPassingFlash(ret.copy().set_stroke(width=9), time_width=0.5),
                          Indicate(ret_l, color=ERR, scale_factor=1.2), run_time=0.6)
            vo.wait_until("Nothing on the VM")
            self.play(Create(ok), Indicate(vm.frame, color=CLOUD, scale_factor=1.04), run_time=0.8)

        # ========================================================== 5 · the wrapper: cli.py 32-37
        b2.shift(UP * (Y5 - b1.frame.get_height() - GAP5 - b2.frame.get_top()[1]))
        arr5 = chain_arrow(Y5 - b1.frame.get_height(), b2.frame.get_top()[1])
        p32 = code_panel(excerpt("cli.py", 32, 37), "cli.py", first_line=32, font_size=22)
        p32.move_to([0, b2.frame.get_bottom()[1] - 0.18 - p32.height / 2, 0])
        bar32 = line_bar(p32.code, 0)
        _b33, _b36 = line_bar(p32.code, 1), line_bar(p32.code, 4)     # one bar over lines 33-36
        bars_msg = Rectangle(width=_b33.width, height=_b33.get_top()[1] - _b36.get_bottom()[1], stroke_width=0) \
            .set_fill(TURN, 0.16).move_to([_b33.get_center()[0], (_b33.get_top()[1] + _b36.get_bottom()[1]) / 2, 0])
        fe = code_span(p32.code, 5, "from error")
        fe_ul = Line(fe.get_corner(DL) + DOWN * 0.08, fe.get_corner(DR) + DOWN * 0.08, color=LOOKUP,
                     stroke_width=4)
        fe_lab = mono("from error", PT, LOOKUP)
        fe_lab.move_to([CHAIN_X + 0.35 + fe_lab.width / 2, arr5.get_center()[1], 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(v6, ok, get, get_l, ret, ret_l, chip429, ring429)),
                      d429.animate.set_color(INK), run_time=0.5)
            self.play(b1.animate.shift(UP * (Y5 - Y4)), run_time=0.6)
            self.play(FadeIn(b2, shift=UP * 0.3), GrowArrow(arr5), run_time=0.7)
            vo.wait_until("the app's own wrapper")
            self.play(Indicate(b2.legend.text, color=ERR, scale_factor=1.2),
                      Indicate(b2.frame, color=ERR, scale_factor=1.02), run_time=0.9)
            vo.wait_until("lines 32 to 37")
            self.play(FadeIn(p32, shift=UP * 0.3), run_time=0.8)
            self.play(Indicate(p32.header, color=INK, scale_factor=1.1), run_time=0.7)

            vo.wait_until("It catches anything")
            self.play(FadeIn(bar32), Indicate(code_span(p32.code, 0, "except Exception"), color=TURN,
                                              scale_factor=1.08), run_time=0.8)
            vo.wait_until("raises a friendlier")
            self.play(FadeOut(bar32), FadeIn(bars_msg), run_time=0.5)
            self.play(Indicate(b2.rows, color=INK, scale_factor=1.02), run_time=0.7)
            vo.wait_until("chained to the original")
            self.play(Create(fe_ul), fe.animate.set_color(LOOKUP), FadeOut(bars_msg), run_time=0.4)
            self.play(TransformFromCopy(fe, fe_lab), Indicate(arr5, color=LOOKUP, scale_factor=1.15),
                      run_time=0.8)

        # ========================================================== 6 · a typo, the same wrapper
        t2 = calm_scroll(term(prompt=P_REPO, rows=13))
        t2.shift(np.array([-t2.box.get_center()[0], BOTTOM - t2.box.get_bottom()[1], 0]))
        rec2 = on_frame(recorded_tag("real capture · 2026-10-12"), t2)
        lines_bad = []
        for s in OUT_BAD:
            col = S.GREY if s == "…" else (OUTPUT if s.startswith("Input:") else TINT)
            lines_bad.append((s, col))
        wrap39 = textwrap.wrap(B39, WRAP)
        c1, arr6, ct6, c2 = v8([B21], wrap39, B23)
        net = substring(c2.rows[1], "network/IP")
        net_ul = under(net, ERR, y=c2.rows[1].strut.get_bottom()[1] - 0.01)
        net_q = tag("network?", ERR)                 # on box 2's bottom edge, mirroring its legend
        net_q.move_to([c2.frame.get_right()[0] - 0.3 - net_q.width / 2, c2.frame.get_bottom()[1], 0])
        errat = tag("erratum · cli.py lines 32–37", S.GREY)
        errat.move_to([c2.frame.get_left()[0] + 0.3 + errat.width / 2, c2.frame.get_bottom()[1] - 0.45, 0])
        codes = boxed(mixed([("valid codes:", "label"), ("README.md", "mono"),
                             ("· table at the bottom", "label")], S.GREY, 24))
        codes.move_to([0, c2.frame.get_bottom()[1] - 1.3, 0])

        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(b1, b2, arr5, fe_lab, p32, fe_ul)
            self.play(FadeOut(gone, scale=0.5), caption_extra(tr), run_time=0.7)
            self.play(FadeIn(t2), FadeIn(rec2), run_time=0.6)
            vo.wait_until("This extra command")
            bad = t2.type(self, BADLANG, 1.2)
            bc = bad.rows[-1]
            xt = beside(extra_tag(), bc)
            self.pin(bc, xt, run_time=0.4)

            vo.wait_until("x x isn't")
            xx = substring(bc, "xx")
            xx_ul = line_under(bc, "xx", ERR)
            self.play(Create(xx_ul), xx.animate.set_color(ERR), run_time=0.5)
            self.attach(bc, xx_ul)
            out6 = t2.print(self, lines_bad, wrap=True, run_time=1.1, lag=0.1)
            assert len(t2.lines) == 13, len(t2.lines)
            q21, q23, q39 = [out6[3]], list(out6[5:7]), list(out6[8:11])
            assert q21[0].text == B21 and "".join(r.text for r in q39) == B39

            vo.wait_until("The first error says")
            bar21 = row_bar(q21, ERR, 0.2, width=t2.box.width - 0.3, x=t2.box.get_center()[0])
            self.play(FadeIn(bar21), q21[0].glyphs.animate.set_color(ERR), run_time=0.5)
            self.play(Indicate(q21[0].glyphs, color=ERR, scale_factor=1.08), run_time=0.7)
            self.lift([q21, q39, q23], [c1.rows, c2.rows, ct6], VGroup(t2, rec2, bar21),
                      FadeIn(c1.frame), FadeIn(c2.frame), FadeIn(c1.legend), FadeIn(c2.legend),
                      GrowArrow(arr6), run_time=1.2)
            self.add(c1, c2, ct6, arr6)

            vo.wait_until("But the last line")
            self.play(Indicate(c2.frame, color=ERR, scale_factor=1.02), run_time=0.7)
            vo.wait_until("blames the network")
            self.play(Create(net_ul), net.animate.set_color(ERR), FadeIn(net_q, scale=0.7), run_time=0.7)
            vo.wait_until("because the same wrapper")
            self.play(ShowPassingFlash(arr6.copy().set_stroke(width=9), time_width=0.6),
                      Indicate(c2.legend.text, color=ERR, scale_factor=1.2), run_time=0.9)
            self.play(Indicate(c1.rows, color=ERR, scale_factor=1.06), run_time=0.8)

            vo.wait_until("A small flaw")
            self.play(FadeIn(errat, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("not in your setup")
            self.play(Indicate(errat.text, color=S.WHITE, scale_factor=1.1), run_time=0.8)

            vo.wait_until("The valid codes")
            self.play(FadeIn(codes, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("at the bottom of the README")
            self.play(Indicate(codes.text[1], color=S.WHITE, scale_factor=1.15), run_time=0.8)

        # ========================================================== 7 · what to do
        head = mixed([("if you hit a", "label"), ("429", "mono")], INK, 28)
        head[1].set_color(ERR)
        fixes = VGroup(chip("wait and retry", S.GREY, size=26),
                       chip("a VM in another region", CLOUD, size=26),
                       chip("run it on your laptop", LAPTOP, size=26)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        right = VGroup(head, fixes).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        right.move_to([3.55, -0.2, 0])

        inp_line = mono_line(L14, 24, OUTPUT)            # debian12-part-a/10-run-default.txt line 14
        inp_box = RoundedRectangle(width=inp_line.width + 0.6, height=inp_line.height + 0.4, corner_radius=0.12,
                                   stroke_color=S.GREY_DARK, stroke_width=2).set_fill(TERM_BG, 1)
        inp_line.move_to(inp_box)
        inp = VGroup(inp_box, inp_line)
        tick = check_mark(0.4, VENV).next_to(inp, RIGHT, buff=0.3)
        works = mixed([("got this far", "label"), ("→", "mono"), ("your packages work", "label")], VENV, 26)
        cant = VGroup(mixed([("can't open file", "label"), ("'cli.py'?", "mono")], S.GREY, 22).arrange(RIGHT, buff=0.2),
                      mixed([("→", "mono"), ("cd simple-translate", "mono")], S.GREY, 22)) \
            .arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        left = VGroup(VGroup(inp, tick), works, cant).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        left.move_to([-3.4, 0, 0]).align_to(right, UP)          # the two columns share a top line

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(c1, c2, ct6, arr6, net_ul, net_q, errat, codes)), caption_extra(tr, False),
                      run_time=0.6)
            self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
            for i, phrase in enumerate(("wait and retry", "try another region", "or run it on your laptop")):
                vo.wait_until(phrase)
                self.play(FadeIn(fixes[i], shift=LEFT * 0.2), run_time=0.5)

            vo.wait_until("If you got as far")
            self.play(FadeIn(inp, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("the imports worked")
            self.play(Create(tick), FadeIn(works, shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(cant, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("when the first error")
            self.play(Indicate(head[1], color=ERR, scale_factor=1.3), run_time=0.7)
            vo.wait_until("only the network said no")
            self.play(Indicate(fixes, color=S.WHITE, scale_factor=1.04), run_time=0.9)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
