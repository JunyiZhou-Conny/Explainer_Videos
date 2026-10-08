"""S05 · The audio is the clock.

Beats: the real say line of the tic-tac-toe video (A15, script.md line 44) in a script card, a
small GREY screen beside it, and under them the real code that narrates it (A16, s01_hook.py lines
115-122, the toolkit's code style, clipped at the panel edge where a faded line runs on) -> the
voice is made first: an ORANGE clip bar grows under the say line; the animation waits for words:
the three quoted phrases in the code turn ORANGE and fly up as anchor pins onto the clip (at that
clip's real sentence starts); a playhead runs along it, and when it reaches "A hundred" / "A
million" the same words light up in the say line and "100?" / "1,000,000?" appear on the screen
(the strings the code fades in) -> the real 23-second clip of tic-tac-toe scene 3, second say line
(A18 envelope), revealed one sentence at a time, its ends labelled "0 s" / "23 s", GREEN ticks at
its five sentence starts (A17), "sentence starts: exact" -> it moves up (the end labels go); its first 5.2 s zoom out of it; the first sentence's
words appear in their natural widths, then spread into equal character cells over the zoomed
audio (the toolkit's guess), and ORANGE pins (dashed YELLOW: estimated) drop at "counted those"
and "as if the players" -> ponder: the 7 cells of "362,880" lift into a strip of 7 boxes under the
card, "example" in a second strip -> the "example" strip goes (no time is claimed for it); the
zoom comes back, the 7 boxes drop into their cells and stretch to the speech recognizer's GREEN
word bars (A19: "362" 0.24-1.56 s, ",880" 1.56-3.26 s), pushing "counted those" to where it is
really spoken; the estimated pin slides from 1.42 s to the measured 3.26 s and turns GREEN,
leaving a RED gap "+1.8 s" -> the words "counted those" fly into the real line that waits for them
(A20, s03_stop.py line 317) under its own comment (lines 90-92); shift=2.2 glows ORANGE, a GREEN
counter counts the hand-set shifts (about 20) -> the real line of voice.py that calls the online
voice (A21, line 463): it could hand back "audio" and "word times"; .save() keeps only the audio
(dashed YELLOW note).

Every number on screen is checked in _check() (runs on import) against the assets: the clip, its
sentence marks, the character estimate (1.42 s), the recognizer's word times, the +1.8 s gap, the
7 characters, and the real code lines.

Helpers defined here (not in common.py): glyphs_of(), glyphs_of_code(), wave_poly(), clipped_panel()
(a code panel cut at a column, like an editor window), glow(), say_card(), cell_strip(), collect()
(gather that also lifts parts animated in one by one), adopt().
"""

import json
import textwrap

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.scene import VoiceScene

from common import (AUDIO, BUG, EXCERPTS, INK, MEASURED, NARRATION, PANEL, TOOL,
                    anchor_pin, asset_text, box, bug_tag, caption, chip, code_block, code_span, emphasize,
                    fade_out_all, label, load_envelope, measured_badge, mono, open_tag, ponder_drain, pulse,
                    source_caption, video_player)

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real material (assets/)
SAY44 = EXCERPTS["A15"]["say_line_44"]                           # "Take a guess. A hundred? ..."
HOOK = textwrap.dedent(asset_text(EXCERPTS["A16"]["anchors_file"]))   # s01_hook.py lines 115-122
HOOK_FIRST = 115
HOOK_ANCHORS = [(3, '"A hundred"'), (5, '"A million"'), (7, '"Pause the video"')]   # (line, string)
# Sentence starts of that say line in the tic-tac-toe render (s, of a 5.995 s clip): its marks in
# videos/tictactoe-255168/build/media_h/s01_hook/.../Hook.subs.json. Used only to place the pins on
# the schematic clip bar (no time is written on screen).
SAY44_MARKS = [(0, 0.0), (14, 1.323), (25, 2.539), (36, 3.733)]
SAY44_DUR = 5.995

BLOCK = json.loads(asset_text("ttt_s03_say1_marks.json"))        # A17: tic-tac-toe S03, SAY[1]
CLIP_T = BLOCK["end"] - BLOCK["start"]                           # 23.019 s
MARKS = BLOCK["marks"]                                           # (character offset, s)
SENT1 = BLOCK["text"][:MARKS[1][0]]                              # first sentence (+ its space)
SEC_PER_CHAR = MARKS[1][1] / MARKS[1][0]                         # 8.533 s / 96 characters
ENV_T, ENV_V = load_envelope()                                   # A18, one value per 20 ms


def _words():
    """A19: (start, end, word) from the speech recognizer, this video's run on that clip."""
    out = []
    for row in asset_text("ttt_s03_say1_words.txt").splitlines():
        a, b, w = row.split(None, 2)
        out.append((float(a), float(b), w.strip()))
    return out


WORDS = _words()
W362, W880, WCOUNTED = WORDS[2], WORDS[3], WORDS[4]
ANCHOR = "counted those"
EST = SENT1.index(ANCHOR) * SEC_PER_CHAR                         # the toolkit's estimate, 1.42 s
ANCHOR2 = "as if the players"
EST2 = SENT1.index(ANCHOR2) * SEC_PER_CHAR                       # 4.62 s
NUMBER = "362,880"
NUM_AT = SENT1.index(NUMBER)                                     # character offset 8
WINDOW_CHARS = 58                                                # "But our ... anyway, as if "
Z_T = WINDOW_CHARS * SEC_PER_CHAR                                # the zoom shows 0 .. 5.155 s
GAP = WCOUNTED[0] - EST                                          # +1.84 s

SHIFT_LINE = asset_text(EXCERPTS["A20"]["shift_file"]).strip()   # s03_stop.py line 317
COMMENT = asset_text(EXCERPTS["A20"]["comment_file"])            # s03_stop.py lines 90-92
SHIFTS = EXCERPTS["A20"]["shifts_in_scene"]                      # 20 -> "about 20"
VOICE_LINE = asset_text(EXCERPTS["A21"]["file"]).strip()         # voice.py line 463
VOICE_SHOWN = "edge_tts.Communicate(text, self.voice, rate=rate).save(str(out))"   # SHOW line's excerpt

QUESTION = "362,880 has 7 characters,\nas many as the word 'example'.\nSay both out loud.\nHow much longer is the number?"


def _check():
    # A15/A16: the say line and the code that waits for its words
    assert asset_text("ttt_script_line44.md").strip() == "SAY: " + SAY44
    for k, s in HOOK_ANCHORS:
        assert HOOK.splitlines()[k].strip() == f"vo.wait_until({s})"
    assert HOOK.splitlines()[0] == "with self.voiceover(SAY[2]) as vo:"
    assert [SAY44.index(p) for p in ("A hundred", "A million", "Pause the video")] == [o for o, _ in SAY44_MARKS[1:]]
    # A17: a 23-second block, five exact sentence starts, the estimate of "counted those"
    assert abs(CLIP_T - EXCERPTS["A17"]["clip"]["duration"]) < 0.002 and round(CLIP_T) == 23
    assert MARKS == EXCERPTS["A17"]["marks"] and len(MARKS) == 5
    assert SENT1.index(ANCHOR) == EXCERPTS["A17"]["estimate_counted_those"]["offset"] == 16
    assert round(EST, 2) == EXCERPTS["A17"]["estimate_counted_those"]["seconds"] == 1.42
    assert ENV_T[-1] <= CLIP_T and len(ENV_T) > 1100
    # A19: the recognizer's word times, as the SHOW line puts them
    assert (W362, W880) == ((0.24, 1.56, "362"), (1.56, 3.26, ",880"))
    assert WCOUNTED[:2] == (3.26, 4.0) and WCOUNTED[2] == "counted"
    assert f"+{GAP:.1f} s" == "+1.8 s"
    assert len(NUMBER) == len("example") == 7 and SENT1[NUM_AT:NUM_AT + 7] == NUMBER
    assert SENT1[WINDOW_CHARS - 6:WINDOW_CHARS] == "as if " and EST2 < Z_T
    # A20/A21: the real lines
    assert SHIFT_LINE == EXCERPTS["A20"]["shift_line"] and "shift=2.2" in SHIFT_LINE
    assert '"362,880" lasts ~3 s but is only 7 characters' in COMMENT.splitlines()[2]
    assert SHIFTS == 20
    assert VOICE_LINE == EXCERPTS["A21"]["line"] and VOICE_SHOWN in VOICE_LINE


_check()

# ------------------------------------------------------------------ layout
ZX0, ZX1 = -6.2, 6.2                 # the audio drawings (full clip and zoom)
CELL = (ZX1 - ZX0) / WINDOW_CHARS    # one character of the guess, 0.214 units
FULL_Y, FULL_H = 0.2, 1.6            # the full clip, first in the middle ...
TOP_Y, TOP_H = 2.62, 0.6             # ... then in the top band
ZW_Y, ZW_H = -0.62, 1.5              # the zoomed audio
ZW_TOP = ZW_Y + ZW_H / 2
ROW_Y = 1.15                         # the characters of the guess
BAR_Y = -1.66                        # the recognizer's word bars
VMAX = float(ENV_V.max())


def full_x(t: float) -> float:
    return ZX0 + (ZX1 - ZX0) * t / CLIP_T


def zoom_x(t: float) -> float:
    return ZX0 + (ZX1 - ZX0) * t / Z_T


# ------------------------------------------------------------------ helpers (this scene only)
def glyphs_of(t: Text, s: str, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of substring `sub` in a Text built from string s (spaces have no glyphs)."""
    i = -1
    for _ in range(occurrence + 1):
        i = s.find(sub, i + 1)
    assert i >= 0, (sub, s)
    start = len("".join(s[:i].split()))
    return VGroup(*t[start:start + len("".join(sub.split()))])


def wave_poly(t0: float, t1: float, x0: float, x1: float, y: float, height: float,
              color: str = AUDIO, gamma: float = 0.6) -> VMobject:
    """A filled, mirrored waveform of the A18 envelope between t0 and t1 (s), drawn from x0 to x1
    (same loudness scale for every part, so pieces of one clip match)."""
    sel = (ENV_T >= t0 - 1e-6) & (ENV_T <= t1 + 1e-6)
    tt, vv = ENV_T[sel], ENV_V[sel]
    xs = x0 + (tt - t0) / (t1 - t0) * (x1 - x0)
    hh = np.maximum((vv / VMAX) ** gamma * height / 2, 0.012)
    top = [[x, y + h, 0] for x, h in zip(xs, hh)]
    bot = [[x, y - h, 0] for x, h in zip(xs[::-1], hh[::-1])]
    m = VMobject(stroke_width=0).set_points_as_corners(top + bot + [top[0]])
    return m.set_fill(color, 0.85)


def clipped_panel(source: str, path: str, first_line: int, cols: int, font_size: float = 24,
                  dim: float = 1.0, fade: int = 6, note: str = "") -> VGroup:
    """A real excerpt in the house code style, cut at `cols` columns like an editor window: glyphs
    beyond it are dropped and the last `fade` columns fade out, so a long faded line visibly runs
    on past the panel edge. Lines are dimmed to `dim`. .code .caption"""
    c = code_block(source, font_size)
    lines = source.split("\n")
    adv = 0.2001855 * font_size / 24                     # DejaVu Sans Mono advance
    clipped = False
    for k, ln in enumerate(lines):
        cols_k = [j for j, ch in enumerate(ln) if not ch.isspace()]
        glyphs = c.code_lines[k]
        assert len(cols_k) == len(glyphs), (k, ln)
        drop = [g for g, j in zip(glyphs, cols_k) if j >= cols]
        for g, j in zip(glyphs, cols_k):
            if cols - fade <= j < cols:
                g.set_opacity(dim * (cols - j) / (fade + 1))
            elif j < cols:
                g.set_opacity(dim)
        if drop:
            clipped = True
            glyphs.remove(*drop)
    if clipped:
        bg = c.background
        pad = c.code_lines.get_left()[0] - bg.get_left()[0]
        right = c.code_lines.get_left()[0] + cols * adv + pad * 0.5
        new = RoundedRectangle(width=right - bg.get_left()[0], height=bg.height, corner_radius=0.15,
                               stroke_color=S.GREY_DARK, stroke_width=2).set_fill(S.GREY_DARKER, 1)
        new.align_to(bg, LEFT).match_y(bg)
        c.remove(bg)
        c.add_to_back(new)
        c.background = new
    n = len(lines)
    span = f"line {first_line}" if n == 1 else f"lines {first_line}–{first_line + n - 1}"
    cap = caption(f"{path} · {span}{note}").next_to(c, DOWN, buff=0.12).align_to(c, LEFT)
    g = VGroup(c, cap)
    g.code, g.caption = c, cap
    return g


def glow(code: Code, glyphs: VGroup, color: str = AUDIO, opacity: float = 0.28) -> RoundedRectangle:
    """A soft rounded highlight behind some code glyphs, inserted into the code block just above
    its background (so it sits under the text). Starts invisible: animate set_fill(opacity=...)."""
    r = RoundedRectangle(width=glyphs.width + 0.16, height=max(glyphs.height, 0.2) + 0.16,
                         corner_radius=0.07, stroke_width=0).set_fill(color, 0).move_to(glyphs)
    code.submobjects.insert(1, r)
    r.glow_opacity = opacity
    return r


def say_card(text: str, split: str, size: float = 26, width: float = 8.9) -> VGroup:
    """The say line as it stands in script.md: 'SAY:' and the line (wrapped in two at `split`), an
    ORANGE side bar (spoken word for word), and room under the text for its voice clip.
    .box .bar .say .lines (Text of each half, with .src); clip_y() and text_x() after placing it"""
    a, b = text.split(split, 1)
    a, b = a + split.rstrip(), b.lstrip()
    l1, l2 = label(a, size), label(b, size)
    l1.src, l2.src = a, b
    lines = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    say = mono("SAY:", 24, AUDIO)
    h = lines.height + 1.25
    bx = box(width, h, TOOL, fill=PANEL, fill_opacity=1, radius=0.16)
    bar = Rectangle(width=0.09, height=h - 0.3, stroke_width=0).set_fill(AUDIO, 1)
    bar.move_to(bx.get_left() + RIGHT * 0.2)
    say.move_to(bx.get_corner(UL) + np.array([0.4 + say.width / 2, -0.3 - say.height / 2, 0]))
    lines.next_to(say, RIGHT, buff=0.22, aligned_edge=UP).shift(UP * 0.02)
    g = VGroup(bx, bar, say, lines)
    g.box, g.bar, g.say, g.lines = bx, bar, say, lines
    g.clip_y = lambda: bx.get_bottom()[1] + 0.32
    g.text_x = lambda: (lines.get_left()[0], max(l1.get_right()[0], l2.get_right()[0]))
    return g


def glyphs_of_code(code: Code, k: int, line: str, sub: str) -> VGroup:
    """The glyphs of `sub` in line k of a code block (line = that line's source text)."""
    i = line.find(sub)
    assert i >= 0, sub
    start = len("".join(line[:i].split()))
    return VGroup(*code.code_lines[k][start:start + len("".join(sub.split()))])


def collect(scene, *mobs) -> Group:
    """Make several on-screen things ONE top-level group (like common.gather, but each thing's
    whole family leaves the top level first: parts that came on screen one by one, e.g. through
    their own FadeIn or a ReplacementTransform, would otherwise stay behind after a FadeOut)."""
    for m in mobs:
        scene.remove(*m.get_family())
    g = Group(*mobs)
    scene.add(g)
    return g


def adopt(scene, g):
    """Put g on screen as one top-level mobject in place of its parts (after per-part animations)."""
    scene.remove(*g.get_family())
    scene.add(g)
    return g


def cell_strip(chars: str, size: float = 34, side: float = 0.78, buff: float = 0.12,
               color: str = TOOL) -> VGroup:
    """Equal boxes, one character in each (the ponder's strips). .boxes .chars; strip[k] = (box, char)."""
    cells = VGroup()
    for ch in chars:
        b = box(side, side, color, fill_opacity=0.1, radius=0.08)
        t = label(ch, size, INK).move_to(b)
        if ch == ",":
            t.shift(DOWN * side * 0.12)
        cells.add(VGroup(b, t))
    cells.arrange(RIGHT, buff=buff)
    cells.boxes = VGroup(*[c[0] for c in cells])
    cells.chars = VGroup(*[c[1] for c in cells])
    return cells


class AudioClock(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- the animation waits for words
        card = say_card(SAY44, "A million? ")
        card.move_to([-6.05 + card.width / 2, 3.47 - card.height / 2, 0])
        card_cap = caption("tic-tac-toe video · script.md · line 44").next_to(card, DOWN, buff=0.1) \
            .align_to(card, LEFT)
        l1, l2 = card.lines
        word_glyphs = [glyphs_of(l1, l1.src, "A hundred?"), glyphs_of(l1, l1.src, "A million?")]
        x0, x1 = card.text_x()
        clip_y = card.clip_y()
        clip = RoundedRectangle(width=x1 - x0, height=0.13, corner_radius=0.06, stroke_width=0) \
            .set_fill(AUDIO, 0.9).move_to([(x0 + x1) / 2, clip_y, 0])
        voice_l = label("voice", 24, AUDIO).move_to([card.say.get_x(), clip_y, 0])

        def clip_at(t):
            return np.array([x0 + (x1 - x0) * t / SAY44_DUR, clip_y, 0])

        pins = VGroup()
        for _, t in SAY44_MARKS[1:]:
            p = anchor_pin(AUDIO, 0.42)
            p.shift(clip_at(t) + UP * 0.05 - p[1].get_bottom())
            pins.add(p)
        head = VGroup(Line(DOWN * 0.2, UP * 0.2, color=INK, stroke_width=3),
                      Triangle(stroke_width=0).set_fill(INK, 1).scale(0.08).rotate(PI).move_to(UP * 0.24))
        head.move_to(clip_at(0) + UP * 0.03)

        player = video_player(2.6, progress=0.0)
        player.move_to([6.05 - player.width / 2, card.get_y() - 0.05, 0])
        player_cap = caption("on screen").next_to(player, DOWN, buff=0.1).align_to(player, LEFT)
        guess = [label("100?", 30), label("1,000,000?", 30)]
        guess[0].move_to(player.screen.get_center() + UP * 0.33)
        guess[1].move_to(player.screen.get_center() + DOWN * 0.33)

        hook = clipped_panel(HOOK, "tic-tac-toe video · scenes/s01_hook.py", HOOK_FIRST, cols=58, dim=0.35)
        hook.move_to([0, 0, 0]).align_to([-6.05, 0, 0], LEFT)
        hook.align_to([0, min(card_cap.get_bottom()[1], player_cap.get_bottom()[1]) - 0.18, 0], UP)
        code = hook.code
        strings = [code_span(code, k, s) for k, s in HOOK_ANCHORS]

        def progress(t):            # the player's scrubber follows the playhead
            f = t / SAY44_DUR
            return [head.animate.move_to(clip_at(t) + UP * 0.03),
                    player.knob.animate.move_to(player.at(f)),
                    player.done.animate.put_start_and_end_on(player.bar.get_start(), player.at(max(f, 0.01)))]

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(hook, shift=UP * 0.3), FadeIn(player), FadeIn(player_cap), run_time=0.9)
            vo.wait_until("In this pipeline")
            self.play(FadeIn(card, shift=DOWN * 0.15), FadeIn(card_cap), run_time=0.8)
            vo.wait_until("the voice is made first")
            self.play(GrowFromEdge(clip, LEFT), FadeIn(voice_l, shift=RIGHT * 0.1), run_time=1.0)
            vo.wait_until("waits for words")
            self.play(*[VGroup(*[g for g in code.code_lines[k] if g not in s]).animate.set_opacity(1)
                        for (k, _), s in zip(HOOK_ANCHORS, strings)],
                      *[s.animate.set_color(AUDIO).set_opacity(1) for s in strings], run_time=0.5)
            self.play(LaggedStart(*[TransformFromCopy(s, p) for s, p in zip(strings, pins)], lag_ratio=0.2),
                      run_time=1.2)
            vo.wait_until("This code says")
            self.play(code.code_lines[0].animate.set_opacity(1), FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
            self.play(emphasize(code.code_lines[0], run_time=0.8))
            vo.wait_until("when the narration reaches")
            self.play(*progress(SAY44_MARKS[1][1]), run_time=vo.until("A hundred"), rate_func=linear)
            self.play(word_glyphs[0].animate.set_color(AUDIO), Indicate(pins[0], color=S.WHITE, scale_factor=1.3),
                      Indicate(strings[0], color=S.WHITE, scale_factor=1.12), run_time=0.6)
            vo.wait_until("show a hundred")
            self.play(code.code_lines[4].animate.set_opacity(1), FadeIn(guess[0], scale=0.8), run_time=0.5)
            vo.wait_until("When it reaches")
            self.play(*progress(SAY44_MARKS[2][1]), run_time=vo.until("A million"), rate_func=linear)
            self.play(word_glyphs[1].animate.set_color(AUDIO), Indicate(pins[1], color=S.WHITE, scale_factor=1.3),
                      Indicate(strings[1], color=S.WHITE, scale_factor=1.12), run_time=0.6)
            vo.wait_until("show a million")
            self.play(code.code_lines[6].animate.set_opacity(1), FadeIn(guess[1], scale=0.8), run_time=0.5)

        # ---------------------------------------------------------- the real clock: sentence starts
        part_a = wave_poly(0, Z_T, ZX0, full_x(Z_T), FULL_Y, FULL_H)   # the zoom window
        part_b = wave_poly(Z_T - 0.02, CLIP_T, full_x(Z_T - 0.02), ZX1, FULL_Y, FULL_H)
        ticks = VGroup(*[Line([full_x(t), FULL_Y - FULL_H / 2 - 0.12, 0], [full_x(t), FULL_Y + FULL_H / 2 + 0.12, 0],
                              color=MEASURED, stroke_width=4) for _, t in MARKS])
        cover = Rectangle(width=ZX1 - ZX0 + 0.1, height=FULL_H + 0.1, stroke_width=0).set_fill(S.BG, 1) \
            .move_to([0, FULL_Y, 0])
        badge = measured_badge("sentence starts: exact", 24)
        badge.next_to(ticks, UP, buff=0.2).align_to([ZX1, 0, 0], RIGHT)
        ends_y = FULL_Y - FULL_H / 2 - 0.12 - 0.1               # the clip's two ends, under the ticks:
        ends = VGroup(label("0 s", 24, TOOL), label(f"{round(CLIP_T)} s", 24, TOOL))   # "23 s" (A17)
        ends[0].next_to([ZX0, ends_y, 0], DOWN, buff=0).align_to([ZX0, 0, 0], LEFT)
        ends[1].next_to([ZX1, ends_y, 0], DOWN, buff=0).align_to([ZX1, 0, 0], RIGHT)
        src2 = source_caption("drawn from the real audio and its sentence marks · tic-tac-toe video, scene 3, "
                              "its second say line")
        squash = TOP_H / FULL_H                                # the full clip, moved up into the top band
        top_half = (FULL_H / 2 + 0.12) * squash
        top_badge_pos = np.array([ZX1 - badge.width / 2, TOP_Y + top_half + 0.1 + badge.height / 2, 0])

        zoom = wave_poly(0, Z_T, ZX0, ZX1, ZW_Y, ZW_H)
        zoom_tick = Line([ZX0, ZW_Y - ZW_H / 2 - 0.1, 0], [ZX0, ROW_Y + 0.25, 0], color=MEASURED, stroke_width=4)
        window = Rectangle(width=full_x(Z_T) - ZX0, height=2 * top_half, stroke_color=TOOL, stroke_width=2.5) \
            .move_to([(ZX0 + full_x(Z_T)) / 2, TOP_Y, 0])

        shown = SENT1[:WINDOW_CHARS].rstrip()                  # "But our 362,880 ... anyway, as if"
        natural = label(shown, 26).move_to([0, ROW_Y, 0]).align_to([ZX0, 0, 0], LEFT)
        spread = mono(shown, 24)
        spread.move_to([0, ROW_Y, 0]).align_to([ZX0, 0, 0], LEFT)
        cols = [j for j, ch in enumerate(shown) if not ch.isspace()]
        assert len(cols) == len(spread) == len(natural)
        for g, j in zip(spread, cols):                         # every character gets the same width
            g.shift(RIGHT * (ZX0 + (j + 0.5) * CELL - g.get_center()[0]))
        ruler = VGroup(*[Line([ZX0 + k * CELL, ROW_Y - 0.31, 0], [ZX0 + k * CELL, ROW_Y - 0.21, 0],
                              color=TOOL, stroke_width=1.5) for k in range(WINDOW_CHARS + 1)])
        a1 = glyphs_of(spread, shown, ANCHOR)
        a2 = glyphs_of(spread, shown, "as if")
        num = glyphs_of(spread, shown, NUMBER)
        est_pins = VGroup()
        for t in (EST, EST2):
            p = anchor_pin(AUDIO, 0.6, estimated=True)
            p.shift(np.array([zoom_x(t), ZW_TOP + 0.04, 0]) - p[1].get_bottom())
            est_pins.add(p)
        guess_tag = open_tag("inside a sentence: estimated from character counts")
        guess_tag.move_to([ZX1 - guess_tag.width / 2, ROW_Y + 0.62, 0])

        with self.voiceover(SAY[1]) as vo:
            beat1 = collect(self, hook, card, card_cap, clip, voice_l, pins, head, player, player_cap, *guess)
            self.play(FadeOut(beat1, shift=UP * 0.3), run_time=0.6)
            self.add(part_a, part_b, cover)
            steps = MARKS[1:] + [(None, CLIP_T)]
            for k, (_, t) in enumerate(steps):                  # one sentence at a time
                right = cover.get_right()[0]
                w = max(0.001, right - full_x(t))
                with_it = [FadeIn(src2), FadeIn(ends[0])] if k == 0 else \
                    [FadeIn(ends[1])] if k == len(steps) - 1 else []
                self.play(cover.animate.stretch_to_fit_width(w, about_edge=RIGHT), *with_it, run_time=0.3,
                          rate_func=smooth)
                self.wait(1 / 15)
            self.remove(cover)
            vo.wait_until("so every sentence")
            self.play(LaggedStart(*[GrowFromCenter(t) for t in ticks], lag_ratio=0.15), run_time=0.9)
            vo.wait_until("known exactly")
            self.play(FadeIn(badge, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Inside a sentence")
            full = collect(self, part_a, part_b, ticks)
            self.play(full.animate.stretch_to_fit_height(2 * top_half).move_to([0, TOP_Y, 0]),
                      badge.animate.move_to(top_badge_pos), *[FadeOut(e) for e in ends], run_time=0.7)
            self.play(Create(window), TransformFromCopy(part_a, zoom), TransformFromCopy(ticks[0], zoom_tick),
                      run_time=0.9)
            vo.wait_until("the toolkit has to guess")
            self.play(FadeIn(natural, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(guess_tag, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("It assumes")
            # serif -> mono glyphs: a cross-fade while they move (a morph between fonts is unreadable midway)
            self.play(*[FadeTransform(a, b) for a, b in zip(natural, spread)], run_time=1.2)
            adopt(self, spread)
            self.play(LaggedStart(*[Create(r) for r in ruler], lag_ratio=0.02), run_time=0.5)
            self.play(a1.animate.set_color(AUDIO), a2.animate.set_color(AUDIO),
                      LaggedStart(*[FadeIn(p, shift=DOWN * 0.35) for p in est_pins], lag_ratio=0.3), run_time=0.8)

        # ---------------------------------------------------------- ponder: 7 characters each
        q = ponder_card(QUESTION)
        q.move_to([0, 3.5 - q.height / 2, 0])
        num_strip = cell_strip(NUMBER).move_to([0, -1.45, 0])
        ex_strip = cell_strip("example").move_to([0, -2.55, 0])
        lifted = num.copy()
        rest = [g for g in spread if g not in num]
        zoom_view = [zoom, zoom_tick, ruler, *rest, est_pins, guess_tag]

        with self.voiceover(SAY[2]) as vo:
            vo.wait_until("Pause")
            self.add(lifted)
            self.remove(*num)
            self.play(FadeOut(collect(self, full, badge, window, src2, *zoom_view)),
                      lifted.animate.arrange(RIGHT, buff=0.42).move_to(num_strip), run_time=0.5)
            self.play(FadeIn(q, scale=0.95), run_time=0.5)
            vo.wait_until("The number on screen")
            self.play(*[FadeTransform(a, b) for a, b in zip(lifted, num_strip.chars)],
                      LaggedStart(*[Create(b) for b in num_strip.boxes], lag_ratio=0.1), run_time=0.9)
            adopt(self, num_strip)
            vo.wait_until("as many as")
            self.play(*[TransformFromCopy(a, b) for a, b in zip(num_strip.boxes, ex_strip.boxes)],
                      LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in ex_strip.chars], lag_ratio=0.1), run_time=0.9)
            adopt(self, ex_strip)
            vo.wait_until("Say both")
            self.play(pulse(num_strip, 1.06), run_time=0.5)
            self.play(pulse(ex_strip, 1.06), run_time=0.5)
            vo.wait_until("How much longer")
            self.play(emphasize(num_strip.boxes, run_time=0.9, circle=True))
        ponder_drain(self, q, 8)

        # ---------------------------------------------------------- measured: about three seconds
        est_cells = VGroup()                                   # the 7 characters, as the toolkit times them
        for k, ch in enumerate(NUMBER):
            x = ZX0 + (NUM_AT + k + 0.5) * CELL
            b = Rectangle(width=CELL - 0.03, height=0.42, stroke_color=TOOL, stroke_width=1.5).set_fill(S.BG, 0) \
                .move_to([x, ROW_Y, 0])
            est_cells.add(VGroup(b, num[k].copy().set_color(INK)))
        measured = VGroup()                                    # ... and as the recognizer heard them
        spans = [(W362[0], W362[1], 3), (W880[0], W880[1], 4)]
        for t0, t1, n in spans:
            w = (zoom_x(t1) - zoom_x(t0)) / n
            for k in range(n):
                xa = zoom_x(t0) + k * w
                b = RoundedRectangle(width=w - 0.06, height=0.52, corner_radius=0.06, stroke_color=MEASURED,
                                     stroke_width=2.5).set_fill(MEASURED, 0.1).move_to([xa + w / 2, ROW_Y, 0])
                measured.add(b)
        meas_chars = VGroup(*[label(ch, 30, INK).move_to(b) for ch, b in zip(NUMBER, measured)])
        meas_chars[3].shift(DOWN * 0.1)
        bars, bar_labels = VGroup(), VGroup()
        for t0, t1, w in (W362, W880, WCOUNTED):
            r = RoundedRectangle(width=zoom_x(t1) - zoom_x(t0) - 0.05, height=0.14, corner_radius=0.06,
                                 stroke_width=0).set_fill(MEASURED, 1)
            r.move_to([(zoom_x(t0) + zoom_x(t1)) / 2, BAR_Y, 0])
            bars.add(r)
            bar_labels.add(mono(w, 24, MEASURED).next_to(r, DOWN, buff=0.14))
        guides = VGroup(*[Line([zoom_x(t), BAR_Y + 0.1, 0], [zoom_x(t), ROW_Y - 0.3, 0], color=MEASURED,
                               stroke_width=2, stroke_opacity=0.45) for t in (W362[0], W880[0], WCOUNTED[0])])
        brace = Brace(measured, UP, buff=0.08, color=MEASURED)
        about3 = label("about 3 s", 26, MEASURED).next_to(brace, UP, buff=0.08)
        cap4 = source_caption(EXCERPTS["A19"]["caption"])
        others = [g for g in rest if g not in a1]               # every guessed character but the anchor
        push = zoom_x(W880[0]) - (ZX0 + (NUM_AT + 3) * CELL)    # after step 1: ",880" starts at 1.56 s
        to_measured = zoom_x(WCOUNTED[0]) - (ZX0 + SENT1.index(ANCHOR) * CELL)
        pin = est_pins[0]
        green_pin = anchor_pin(MEASURED, 0.6)
        green_pin.shift(np.array([zoom_x(WCOUNTED[0]), ZW_TOP + 0.04, 0]) - green_pin[1].get_bottom())
        y_gap = pin[0].get_y()
        gap_line = Line([zoom_x(EST), y_gap, 0], [zoom_x(WCOUNTED[0]), y_gap, 0], color=BUG, stroke_width=4)
        gap_ends = VGroup(*[Line([x, y_gap - 0.14, 0], [x, y_gap + 0.14, 0], color=BUG, stroke_width=4)
                            for x in (zoom_x(EST), zoom_x(WCOUNTED[0]))])
        gap_tag = bug_tag(f"+{GAP:.1f} s", 24).move_to(gap_line)

        with self.voiceover(SAY[3]) as vo:
            back = [zoom, zoom_tick, ruler, *rest, pin]
            for g in others:
                g.set_opacity(0.3)
            ruler.set_opacity(0.6)
            # clear the card first (the boxes would pass through its text), then the zoom comes back
            self.play(FadeOut(q), FadeOut(ex_strip, shift=DOWN * 0.2), run_time=0.4)
            self.play(FadeIn(Group(*back)), FadeIn(cap4),
                      *[ReplacementTransform(a, b) for a, b in zip(num_strip, est_cells)], run_time=0.8)
            collect(self, a1)
            vo.wait_until("three hundred")
            step1 = []
            for k in range(3):                                 # "362" takes its measured time ...
                step1 += [ReplacementTransform(est_cells[k][0], measured[k]),
                          FadeTransform(est_cells[k][1], meas_chars[k])]   # mono -> serif: fade, don't morph
            step1 += [est_cells[k].animate.shift(RIGHT * push) for k in range(3, 7)]   # ... and pushes the rest
            self.play(*step1, FadeOut(collect(self, *others, ruler)), a1.animate.shift(RIGHT * push),
                      GrowFromEdge(bars[0], LEFT), FadeIn(bar_labels[0]), Create(guides[0]), Create(guides[1]),
                      run_time=1.2)
            vo.wait_until("eight hundred")
            step2 = []
            for k in range(3, 7):
                step2 += [ReplacementTransform(est_cells[k][0], measured[k]),
                          FadeTransform(est_cells[k][1], meas_chars[k])]
            self.play(*step2, a1.animate.shift(RIGHT * (to_measured - push)), GrowFromEdge(bars[1], LEFT),
                      FadeIn(bar_labels[1]), Create(guides[2]), run_time=1.1)
            vo.wait_until("Far longer")
            self.play(GrowFromCenter(brace), FadeIn(about3, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("So the toolkit")
            self.play(Indicate(pin, color=S.WHITE, scale_factor=1.25), run_time=0.8)
            vo.wait_until("for the words right after")
            self.play(GrowFromEdge(bars[2], LEFT), FadeIn(bar_labels[2]), run_time=0.6)
            vo.wait_until("lands almost")
            self.add(gap_ends[0])
            self.play(pin.animate.shift(RIGHT * (zoom_x(WCOUNTED[0]) - zoom_x(EST))), Create(gap_line),
                      run_time=0.8, rate_func=linear)
            self.add(gap_ends[1])
            self.play(ReplacementTransform(pin, green_pin), FadeIn(gap_tag, scale=0.9), run_time=0.4)

        # ---------------------------------------------------------- the fix so far: by hand
        comment = clipped_panel(COMMENT, "tic-tac-toe video · scenes/s03_stop.py", 90, cols=66, font_size=22)
        for k in (0, 1):
            for gl in comment.code.code_lines[k]:
                gl.set_opacity(gl.get_fill_opacity() * 0.35)
        comment.move_to([0, 2.45 - comment.height / 2, 0])
        fix = clipped_panel(SHIFT_LINE, "tic-tac-toe video · scenes/s03_stop.py", 317, cols=60, font_size=24)
        fix.move_to([0, 0, 0]).align_to(comment, LEFT).align_to([0, comment.get_bottom()[1] - 0.3, 0], UP)
        fcode = fix.code
        target = code_span(fcode, 0, ANCHOR)
        shift_span = code_span(fcode, 0, "shift=2.2")
        shift_glow = glow(fcode, shift_span)
        ghost = target.copy().set_color(AUDIO)
        target.set_opacity(0)
        why = glyphs_of_code(comment.code, 2, COMMENT.splitlines()[2], '"362,880" lasts ~3 s but is only 7 characters')
        counter_l = label("hand-set shifts in this one scene: about", 24, INK)
        counter_n = DecimalNumber(0, num_decimal_places=0, font_size=30, color=MEASURED)
        cbody = VGroup(counter_l, counter_n).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        cbox = box(cbody.width + 0.6, cbody.height + 0.36, MEASURED, fill_opacity=0.1, radius=0.18)
        cbody.move_to(cbox)
        counter = VGroup(cbox, cbody)
        counter.next_to(fix, DOWN, buff=0.3).align_to(fix, LEFT)
        counter_n.add_updater(lambda m: m.next_to(counter_l, RIGHT, buff=0.15).align_to(counter_l, DOWN))

        voice = clipped_panel(VOICE_SHOWN, "the toolkit · explainer/voice.py", 463, cols=80, font_size=22,
                              note=" (part of the line) · the online voice, used for Chinese")
        vcode = voice.code
        comm_span = code_span(vcode, 0, "edge_tts.Communicate(text, self.voice, rate=rate)")
        save_span = code_span(vcode, 0, ".save(str(out))")
        out_audio = chip("audio", AUDIO, 24)
        out_words = chip("word times", AUDIO, 24)
        outs = VGroup(out_audio, out_words).arrange(RIGHT, buff=0.4)
        note = open_tag("this service can send word times · only the audio is kept")

        with self.voiceover(SAY[4]) as vo:
            # "The fix so far ...": the gap that needs fixing stays readable a moment longer (the ponder's
            # answer only finished appearing at the very end of the previous block)
            self.play(Circumscribe(VGroup(gap_ends, gap_tag), color=S.WHITE, buff=0.12, time_width=0.5),
                      run_time=0.8)
            self.play(FadeOut(collect(self, zoom, zoom_tick, green_pin, gap_line, gap_ends, gap_tag, measured,
                                      meas_chars, bars, bar_labels, guides, brace, about3, cap4)), run_time=0.4)
            a1.set_z_index(3)                                  # fly over the panel, not under it
            self.play(FadeIn(fix), ReplacementTransform(a1, ghost), FadeIn(comment, shift=DOWN * 0.15), run_time=0.8)
            target.set_opacity(1).set_color(AUDIO)
            self.remove(ghost)
            vo.wait_until("this one scene carries")
            self.play(FadeIn(counter, shift=UP * 0.1), run_time=0.4)
            self.play(ChangeDecimalToValue(counter_n, SHIFTS), run_time=1.2, rate_func=smooth)
            self.play(emphasize(why, run_time=0.9))
            vo.wait_until("the biggest")
            self.play(shift_glow.animate.set_fill(opacity=shift_glow.glow_opacity), shift_span.animate.set_color(AUDIO),
                      run_time=0.5)
            self.play(Circumscribe(shift_span, color=S.WHITE, buff=0.08, run_time=0.9))

            # the voice that could tell the time of every word
            vo.wait_until("Yet the online voice")
            counter_n.clear_updaters()
            stay = collect(self, fix, counter)
            dy = 2.85 - fix.get_top()[1]                     # the kept line moves up to the top
            voice.move_to([0, 0, 0]).align_to(comment, LEFT).align_to([0, stay.get_bottom()[1] + dy - 0.55, 0], UP)
            outs.next_to(voice, DOWN, buff=0.45).align_to(voice, LEFT).shift(RIGHT * 0.4)
            note.next_to(outs, DOWN, buff=0.4).align_to(voice, LEFT)
            # the comment leaves first: its caption would cross the line moving up
            self.play(FadeOut(comment, shift=UP * 0.2), run_time=0.35)
            self.play(stay.animate.shift(UP * dy), run_time=0.5)
            self.play(FadeIn(voice, shift=UP * 0.3), run_time=0.7)
            vo.wait_until("can send a time")
            self.play(emphasize(comm_span, run_time=0.8))
            self.play(LaggedStart(*[FadeIn(o, target_position=comm_span.get_center(), scale=0.5) for o in outs],
                                  lag_ratio=0.35), run_time=1.0)
            vo.wait_until("The toolkit keeps")
            self.play(Circumscribe(save_span, color=S.WHITE, buff=0.08), Indicate(out_audio, color=S.WHITE),
                      out_words.animate.shift(DOWN * 0.25).set_opacity(0.2), FadeIn(note, shift=UP * 0.1), run_time=0.9)
        self.wait(1.6)
        fade_out_all(self)

