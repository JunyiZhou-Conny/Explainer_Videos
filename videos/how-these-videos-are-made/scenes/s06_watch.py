"""S06 · Checking without eyes or ears.

Beats: the motif of S01 comes back (the BLUE agent under the GREY headphones and play button, each
struck through in RED) beside the ponder card: you can't hear it, you can't press play, how would
you check a video? -> the agent's answer, as two rows: the struck play button -> a little grid of
pictures (time into pictures), the struck headphones -> a GREY chip "subtitles ·
speech-recognizer transcripts" (sound into text) -> the play button becomes a GREY player that
renders a quick draft; the little grid opens into 16 empty slots and the stills drop out of the
player one by one into them (each tile is cut from the real contact sheet, A01) -> the real sheet
in its GREY frame, "16 stills · one every 2 seconds · time burned in yellow"; the agent looks at it
along a GREY sight line that walks along the yellow timestamps (a WHITE box on each, a loupe that
makes the first four readable), then over the whole grid -> between stills: the two tiles at
18.933 s and 21.000 s lift out to the ends of a little time axis; a "?" in the gap becomes four
ticks, and four real frames 0.2 s apart (A02: 19.6, 19.8, 20.0, 20.2 s) drop from them into a
strip; GREEN rings mark the ghost marks that moved since the frame before -> the rings become two
GREEN check chips in a column: (1) "lint, without drawing a frame" opens the real lint output on
tic-tac-toe scene 3 (A22: clean, "OK") and its three flags as a legend (output format, with a
small drawing of each), then folds back; (2) "the scenes check themselves" opens _check_numbers()
(A23, s03_stop.py lines 62-72), one assert line glowing GREEN, a GREEN counter "82 checks in the
tic-tac-toe scenes · most of them on the numbers", and the numbers inside the asserts light up.

Everything shown as real is checked in _check() (runs on import): the sheet's tile layout and its
yellow timestamps, which squares of the four frames changed (the GREEN rings), the lint lines,
the three flags, the code lines and the count of 82.

Helpers defined here (not in common.py): glyphs_of(), clipped_panel() and collect()/adopt() (as in
s05_clock.py), tile_box(), ts_box(), wait_for() (an anchor with a hand-set shift, measured with a
speech-recognizer pass over this scene's clips; English only), sight_line(), mini_grid(),
mini_screen(), flag_picto(), flag_chip().
"""

import numpy as np
from manim import *

from explainer import i18n
from explainer import style as S
from explainer.components import ponder_card
from explainer.scene import VoiceScene

from common import (AGENT, EXCERPTS, INK, MEASURED, NARRATION, TOOL, asset, asset_text, box, cant_hear_or_play,
                    caption, chip, code_block, code_span, emphasize, exhibit, fade_out_all, label, measured_badge,
                    mono, ponder_drain, role_icon, source_caption, terminal, video_player)

SAY = NARRATION["S06"]

QUESTION = "You can't hear the video,\nand you can't press play.\nHow would you check it?"

# ------------------------------------------------------------------ the real material (assets/)
SHEET = "ttt_s03_sheet_01.png"          # A01: 1950 x 1110, 4 x 4 tiles of 480 x 270, padding and margin 6
TILE_W, TILE_H, PAD = 480, 270, 6
# the times burned in yellow on the 16 tiles (read off the sheet, in tile order)
TILE_TIMES = ["00:00:00.933", "00:00:02.933", "00:00:04.933", "00:00:06.933", "00:00:08.933", "00:00:10.933",
              "00:00:12.933", "00:00:14.933", "00:00:16.933", "00:00:18.933", "00:00:21.000", "00:00:23.000",
              "00:00:25.000", "00:00:27.000", "00:00:29.000", "00:00:30.999"]
TS = (10, 5, 109, 15)                   # the yellow digits inside a tile (px, tile coordinates)
BEFORE, AFTER = 9, 10                   # the stills at 18.933 s and 21.000 s: A02's frames lie between them

FRAMES = [(f"ttt_s03_moving_{t}.png", t) for t in ("19.6", "19.8", "20.0", "20.2")]   # A02, 1920 x 1080
FRAME_CROP = (82, 292, 662, 1008)       # the board and the "ghost endings counted" line
SQUARE = {(r, c): (192 + 180 * c, 394 + 180 * r) for r in range(3) for c in range(3)}   # square centres (px)
# squares whose ghost mark changed since the frame before (checked in _check): the shuffle moves on
MOVED = [[], [(2, 0), (2, 1)], [(2, 0), (2, 1)], [(1, 0), (2, 0)]]

A22, A23 = EXCERPTS["A22"], EXCERPTS["A23"]
LINT_CMD = "$ python -m explainer.check …/s03_stop.py GamesStop"   # "…": the path, cut (ASSETS.md A22)
LINT_LINES = A22["tool_lines"]          # ["end at 99.9s; 0 visible mobject(s) left on screen", "OK"]
FLAGS = A22["flags"]                    # ["OUT · off screen", "SMALL · under 20 points", "LEFT · still on ..."]
CHECKS = asset_text(A23["file"])        # s03_stop.py lines 62-72, _check_numbers()
CHECKS_FIRST = 62
GLOW_LINE = 7                           # line 69: factorial(4) == 24 ... factorial(9) == 362_880
NUMBERS = [(7, "24"), (7, "362_880"), (8, "== 8"), (9, "1_440")]   # numbers inside the asserts
N_ASSERTS = A23["asserts_in_ttt_scenes"]                          # 82


def tile_box(k: int) -> tuple:
    r, c = divmod(k, 4)
    x0, y0 = PAD + c * (TILE_W + PAD), PAD + r * (TILE_H + PAD)
    return (x0, y0, x0 + TILE_W, y0 + TILE_H)


def ts_box(k: int, pad: tuple = (0, 0, 0, 0)) -> tuple:
    x0, y0, _, _ = tile_box(k)
    return (x0 + TS[0] - pad[0], y0 + TS[1] - pad[1], x0 + TS[2] + pad[2], y0 + TS[3] + pad[3])


def _check():
    from PIL import Image
    im = np.asarray(Image.open(asset(SHEET)).convert("RGB")).astype(int)
    assert im.shape[:2] == (1110, 1950)
    yellow = (im[:, :, 0] > 180) & (im[:, :, 1] > 180) & (im[:, :, 2] < 100)
    for k in range(16):                                   # every tile carries its time, in the same spot
        x0, y0, x1, y1 = tile_box(k)
        ys, xs = np.nonzero(yellow[y0:y0 + 60, x0:x1])
        assert (xs.min(), ys.min(), xs.max(), ys.max()) == TS, k
        assert (im[y0 - 1, x0:x1] == 255).all()           # white padding above each tile
    t = [float(s.split(":")[-1]) for s in TILE_TIMES]
    assert t[BEFORE] < float(FRAMES[0][1]) and float(FRAMES[-1][1]) < t[AFTER]
    assert all(TILE_TIMES[k].endswith(f"{t[k]:.3f}") for k in (BEFORE, AFTER))   # the axis-end labels
    # A02: which ghost marks moved between neighbouring frames (the GREEN rings)
    fs = [np.asarray(Image.open(asset(f)).convert("L")).astype(int) for f, _ in FRAMES]
    for a in range(1, 4):
        def changed(rc):
            x, y = SQUARE[rc]
            d = fs[a][y - 60:y + 60, x - 60:x + 60] - fs[a - 1][y - 60:y + 60, x - 60:x + 60]
            return int((np.abs(d) > 40).sum())
        assert all(changed(rc) > 1000 for rc in MOVED[a]), a
        assert all(changed((0, c)) < 50 for c in range(3))  # X's winning row never moves
        assert changed((1, 2)) < 50 and changed((2, 2)) < 50   # nor the O at 4, nor the ghost at 9
    # A22: the lint output (clean) and its flags; A23: the asserts and their count
    lint = asset_text(A22["file"])
    assert all(s in lint.splitlines() for s in LINT_LINES) and LINT_LINES[-1] == "OK"
    assert "explainer.check" in LINT_CMD and "s03_stop.py GamesStop" in LINT_CMD
    assert [f.split(" · ")[0] for f in FLAGS] == ["OUT", "SMALL", "LEFT"]
    lines = CHECKS.splitlines()
    assert len(lines) == 11 and lines[0] == "def _check_numbers():"
    assert lines[GLOW_LINE].strip() == "assert factorial(4) == 24 and NINE_FACTORIAL == factorial(9) == 362_880"
    assert sum(ln.strip().startswith("assert") for ln in lines) == 7
    assert all(s in lines[k] for k, s in NUMBERS)
    assert N_ASSERTS == 82


_check()

# ------------------------------------------------------------------ layout
SHEET_W = 10.7                           # the contact sheet: right edge 6.5, top 3.5
SHEET_C = np.array([6.5 - SHEET_W / 2, 3.5 - SHEET_W * 1110 / 1950 / 2, 0])
TILE_UW = SHEET_W * TILE_W / 1950        # one tile on screen
AGENT_SPOT = np.array([-5.55, -1.45, 0])
PLAYER_SPOT = np.array([-5.45, 2.0, 0])
LOUPE_W = 2.3

STRIP_Y = -0.05                          # the four frames
FRAME_W = 2.85
FRAME_X = [-4.725, -1.575, 1.575, 4.725]
AXIS_Y = 2.88                            # the little time axis between the two stills
STILL_W = 2.3
STILL_X = 5.45
AX0, AX1 = -STILL_X + STILL_W / 2 + 0.12, STILL_X - STILL_W / 2 - 0.12

LEFT_X = -6.4                            # S06's last beat: left edge of the chips and excerpts


# ------------------------------------------------------------------ helpers (this scene only)
def glyphs_of(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of substring `sub` in a Text built from string s (spaces have no glyphs)."""
    i = s.find(sub)
    assert i >= 0, (sub, s)
    start = len("".join(s[:i].split()))
    return VGroup(*t[start:start + len("".join(sub.split()))])


def collect(scene, *mobs) -> Group:
    """Make several on-screen things ONE top-level group (each thing's whole family leaves the top
    level first, so no part that came on screen by itself stays behind)."""
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


def clipped_panel(source: str, path: str, first_line: int, cols: int, font_size: float = 20,
                  dim: float = 0.3, fade: int = 6, keep=()) -> VGroup:
    """A real excerpt in the house code style, cut at `cols` columns like an editor window (glyphs
    beyond it are dropped, the last `fade` columns fade out), every line but `keep` dimmed to `dim`.
    Same idea as s05_clock.py's clipped_panel. .code .caption"""
    c = code_block(source, font_size)
    lines = source.split("\n")
    adv = 0.2001855 * font_size / 24                     # DejaVu Sans Mono advance
    clipped = False
    for k, ln in enumerate(lines):
        cols_k = [j for j, ch in enumerate(ln) if not ch.isspace()]
        glyphs = c.code_lines[k]
        assert len(cols_k) == len(glyphs), (k, ln)
        o = 1.0 if k in keep else dim
        drop = [g for g, j in zip(glyphs, cols_k) if j >= cols]
        for g, j in zip(glyphs, cols_k):        # only a line that runs on past the edge fades out
            g.set_opacity(o * (cols - j) / (fade + 1) if drop and cols - fade <= j < cols else o)
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
    cap = caption(f"{path} · lines {first_line}–{first_line + n - 1}").next_to(c, DOWN, buff=0.12).align_to(c, LEFT)
    g = VGroup(c, cap)
    g.code, g.caption = c, cap
    return g


def wait_for(scene, vo, phrase: str, shift: float = 0.0) -> None:
    """vo.wait_until(phrase), moved by `shift` seconds. The toolkit places a phrase by its characters
    inside the sentence, which runs up to 0.9 s late in SAY[3]'s long middle sentence (a pause after
    "frame,"). The shifts are hand-set from a speech-recognizer pass over this scene's clips (word
    starts); in another language version the clip differs, so they are not applied there."""
    t = vo.clip.time_of(phrase)
    if t is None:
        vo.wait_until(phrase)                       # logs "voiceover anchor not found"
        return
    left = t + (0.0 if i18n.active() else shift) - vo.elapsed
    if left > 1 / 60:
        scene.wait(left)


def sight_line(a, b, n: int = 26) -> VMobject:
    """The agent 'looking': a GREY dashed line (a fixed number of dashes, so it moves smoothly)."""
    return DashedVMobject(Line(a, b), num_dashes=n, dashed_ratio=0.55).set_stroke(TOOL, 2.5, opacity=0.9)


def mini_grid(w: float = 1.5) -> VGroup:
    """A small 4 x 4 grid of GREY frames: 'pictures'."""
    cw = (w - 3 * 0.06) / 4
    cells = VGroup(*[Rectangle(width=cw, height=cw * 9 / 16, stroke_color=TOOL, stroke_width=2)
                     .set_fill(TOOL, 0.12) for _ in range(16)])
    return cells.arrange_in_grid(rows=4, cols=4, buff=0.06)


def mini_screen(w: float = 0.95) -> RoundedRectangle:
    return RoundedRectangle(width=w, height=w * 9 / 16, corner_radius=0.05, stroke_color=TOOL, stroke_width=2.5)


def flag_picto(kind: str) -> VGroup:
    """A small drawing of what each lint flag means (a DIAGRAM, no text)."""
    scr = mini_screen()
    if kind == "OUT":         # something hanging over the edge of the frame
        sq = Square(0.24, stroke_width=0).set_fill(INK, 0.9).move_to(scr.get_right() + RIGHT * 0.04)
        return VGroup(scr, sq)
    if kind == "SMALL":       # a line of normal text and a tiny one
        big = Line(LEFT * 0.28, RIGHT * 0.28, stroke_width=7, color=INK).move_to(scr.get_center() + UP * 0.08)
        tiny = Line(LEFT * 0.08, RIGHT * 0.08, stroke_width=2, color=INK).move_to(scr.get_center() + DOWN * 0.12)
        return VGroup(scr, big, tiny)
    sq = Square(0.2, stroke_width=0).set_fill(INK, 0.9).move_to(scr.get_center() + UP * 0.02)   # LEFT behind
    bar = Line(scr.get_corner(DL) + DOWN * 0.13, scr.get_corner(DR) + DOWN * 0.13, stroke_width=3, color=TOOL)
    knob = Dot(bar.get_end(), radius=0.05, color=TOOL)
    return VGroup(scr, sq, bar, knob)


def flag_chip(flag: str) -> VGroup:
    """'OUT · off screen' as a GREY chip: the flag word in the code font, the meaning in house text."""
    key, meaning = flag.split(" · ", 1)
    body = VGroup(mono(key, 22, INK), label("· " + meaning, 24, INK)).arrange(RIGHT, buff=0.12)
    # one baseline for the code word and the words (the first letter after "·" sits on it; a
    # descender such as the p of "points" must not lift or drop the line), the same in every chip
    body[0].align_to(body[1][1], DOWN)
    b = box(body.width + 0.5, 0.56, TOOL, fill_opacity=0.12, radius=0.2)
    ref = label("Hgy", 24)
    body.move_to(b)
    body.shift(UP * (b.get_center()[1] + ref[0].get_bottom()[1] - ref.get_center()[1] - body[1][1].get_bottom()[1]))
    g = VGroup(b, body)
    g.key = key
    return g


class Watching(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- ponder: no ears, no play button
        agent = role_icon("agent", 1.3).move_to([-4.35, -0.75, 0])
        agent_l = label("the agent", 26, AGENT).next_to(agent, DOWN, buff=0.22)
        glyphs = cant_hear_or_play(0.85, gap=0.75).move_to([-4.35, 1.35, 0])
        (hp, hp_x), (pl, pl_x) = glyphs

        with self.voiceover(SAY[0]) as vo:
            vo.wait_until("Pause")
            card = ponder_card(QUESTION, width=7.4).move_to([2.55, 0.25, 0])
            self.play(FadeIn(card, scale=0.95), run_time=0.6)      # as ponder_in, beside the motif
            vo.wait_until("Suppose you")
            self.play(FadeIn(agent, shift=UP * 0.2), FadeIn(agent_l), FadeIn(hp, shift=DOWN * 0.15), run_time=0.6)
            self.play(Create(hp_x), run_time=0.35)
            vo.wait_until("and you can't press play")
            self.play(FadeIn(pl, shift=DOWN * 0.15), run_time=0.45)
            self.play(Create(pl_x), run_time=0.35)
            vo.wait_until("How would you check")
            adopt(self, glyphs)
            self.play(Indicate(glyphs, color=S.WHITE, scale_factor=1.12), run_time=0.9)
        ponder_drain(self, card, 8)

        # ---------------------------------------------------------- time into pictures, sound into text
        row_a, row_b = 1.3, -1.2
        g_x = -3.65
        grid_icon = mini_grid(1.5).move_to([-0.55, row_a, 0])
        pics_l = label("pictures", 24, TOOL).next_to(grid_icon, DOWN, buff=0.16)
        arrow_a = Arrow([g_x + 0.62, row_a, 0], [grid_icon.get_left()[0] - 0.15, row_a, 0], buff=0, color=TOOL,
                        stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.3)
        text_chip = chip("subtitles · speech-recognizer transcripts", TOOL, 26)
        text_chip.move_to([0, row_b, 0]).align_to(grid_icon, LEFT)
        arrow_b = Arrow([g_x + 0.62, row_b, 0], [text_chip.get_left()[0] - 0.15, row_b, 0], buff=0, color=TOOL,
                        stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.3)

        agent2 = role_icon("agent", 1.1).move_to([-5.65, -0.3, 0])      # new icons, not scaled: the AI
        agent3 = role_icon("agent", 1.0).move_to(AGENT_SPOT)            # badge's text stays at 20 pt
        player = video_player(1.75, progress=0.0).move_to(PLAYER_SPOT)
        draft_l = label("a quick draft", 24, TOOL).next_to(player, DOWN, buff=0.12)   # as "pictures"
        sheet = exhibit(SHEET, width=SHEET_W).move_to(SHEET_C)
        targets = [sheet.px_box(*tile_box(k)) for k in range(16)]
        slots = VGroup(*[Rectangle(width=r.width, height=r.height, stroke_color=TOOL, stroke_width=2)
                         .set_fill(TOOL, 0.08).move_to(r) for r in targets])
        tiles = [exhibit(SHEET, width=TILE_UW, crop=tile_box(k)).image for k in range(16)]
        f = player.screen.width / TILE_UW
        for t in tiles:
            t.scale(f).move_to(player.screen)
        stack = Group(*reversed(tiles))      # the first still on top: the screen shows each next one
        src1 = source_caption("real contact sheet · tic-tac-toe video, scene 3")
        cap_s = "16 stills · one every 2 seconds · time burned in yellow"
        cap_t = caption(cap_s, 24).next_to(sheet, DOWN, buff=0.2).align_to(sheet, RIGHT)
        cap_parts = [glyphs_of(cap_t, cap_s, p) for p in
                     ("16 stills", "· one every 2 seconds", "· time burned in yellow")]

        w0 = player.screen.width
        launch = player.screen.get_center()
        ends_t = [r.get_center() for r in targets]
        step, dur = 0.052, 0.17                              # in units of the whole flight
        for k, t in enumerate(tiles):
            t.set_z_index(1 + (16 - k) / 100)                # the next still to leave is on top

        def fly(_, alpha):
            for k, t in enumerate(tiles):
                a = smooth(float(np.clip((alpha - k * step) / dur, 0, 1)))
                t.scale_to_fit_width(w0 + (TILE_UW - w0) * a)
                t.move_to(launch + (ends_t[k] - launch) * a + UP * 0.6 * np.sin(PI * a))
                t.set_z_index(3 if 0 < a < 1 else (0 if a >= 1 else t.z_index))

        with self.voiceover(SAY[1]) as vo:
            pl_g, hp_g = glyphs[1], glyphs[0]
            adopt(self, pl_g)
            adopt(self, hp_g)
            self.play(FadeOut(card), FadeOut(agent_l),
                      ReplacementTransform(agent, agent2),
                      pl_g.animate.move_to([g_x, row_a, 0]), hp_g.animate.move_to([g_x, row_b, 0]), run_time=0.8)
            vo.wait_until("turn time into pictures")
            self.play(GrowArrow(arrow_a), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in grid_icon], lag_ratio=0.05),
                      FadeIn(pics_l), run_time=0.8)
            vo.wait_until("and sound into text")
            self.play(GrowArrow(arrow_b), run_time=0.35)
            self.play(FadeIn(text_chip, shift=RIGHT * 0.4), run_time=0.6)

            vo.wait_until("The toolkit renders")
            arrow_p = Arrow(player.frame.get_right() + RIGHT * 0.12, grid_icon.get_left() + LEFT * 0.15, buff=0,
                            color=TOOL, stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.3)
            self.play(FadeTransform(pl_g, player), Transform(arrow_a, arrow_p), FadeIn(draft_l, shift=UP * 0.1),
                      run_time=0.8)          # the draft (time) still points at the pictures
            # the draft is on the player's screen while it renders (not a blank screen)
            self.play(player.done.animate(rate_func=linear).put_start_and_end_on(player.bar.get_start(), player.at(1.0)),
                      player.knob.animate(rate_func=linear).move_to(player.at(1.0)),
                      FadeIn(stack, rate_func=lambda t: smooth(min(1.0, 3 * t))), run_time=1.0)

            vo.wait_until("and tiles a still")
            self.play(FadeOut(VGroup(hp_g, arrow_b, text_chip, pics_l, arrow_a)),
                      *[ReplacementTransform(a, b) for a, b in zip(grid_icon, slots)],
                      ReplacementTransform(agent2, agent3), run_time=0.7)
            self.play(UpdateFromAlphaFunc(stack, fly), run_time=1.9)
            self.add(sheet)
            self.play(FadeIn(sheet), FadeOut(slots), FadeOut(VGroup(player, draft_l)), FadeIn(src1),
                      FadeIn(cap_parts[0]), run_time=0.45)
            self.remove(stack)
            self.play(FadeIn(cap_parts[1], shift=LEFT * 0.1), run_time=0.35)

            # the agent looks at the image, reading the times burned into it
            vo.wait_until("An agent can look")
            eye = agent3.person[0].get_center() + np.array([0.1, 0.03, 0])
            hl = [SurroundingRectangle(sheet.px_box(*ts_box(k)), color=S.WHITE, buff=0.045, stroke_width=2.5,
                                       corner_radius=0.03) for k in range(16)]
            loupes = []
            for k in range(4):
                lp = exhibit(SHEET, width=LOUPE_W, crop=ts_box(k, (8, 4, 8, 5)))
                lp.next_to(hl[k], DOWN, buff=0.1).align_to(hl[k], LEFT).shift(LEFT * 0.05)
                lp.image.set_z_index(2)
                lp.frame.set_z_index(2)
                loupes.append(lp)
            look = sight_line(eye, hl[0].get_left())
            self.play(Create(look), Create(hl[0]), FadeIn(loupes[0], shift=DOWN * 0.1),
                      FadeIn(cap_parts[2], shift=LEFT * 0.1), run_time=0.55)
            box_ = hl[0]
            for k in range(1, 4):
                self.play(box_.animate.move_to(hl[k]), look.animate.become(sight_line(eye, hl[k].get_left())),
                          FadeOut(loupes[k - 1]), FadeIn(loupes[k]), run_time=0.36)
            vo.wait_until("so this is how")
            self.play(FadeOut(loupes[3]), run_time=0.25)
            pts = [hl[k].get_center() for k in range(3, 16)]   # then over the whole grid, in time order
            half_w = hl[0].width / 2

            def sweep(_, alpha):
                x = alpha * (len(pts) - 1)
                i = min(int(x), len(pts) - 2)
                c = pts[i] + (pts[i + 1] - pts[i]) * smooth(x - i)
                box_.move_to(c)
                look.become(sight_line(eye, c + LEFT * half_w))

            self.play(UpdateFromAlphaFunc(VGroup(box_, look), sweep), run_time=max(0.8, vo.remaining() - 0.1),
                      rate_func=linear)

        # ---------------------------------------------------------- between stills: frames 0.2 s apart
        lift = [exhibit(SHEET, width=TILE_UW, crop=tile_box(k)) for k in (BEFORE, AFTER)]
        for lt, k in zip(lift, (BEFORE, AFTER)):
            lt.move_to(targets[k])
        outline = VGroup(*[SurroundingRectangle(lt, color=S.WHITE, buff=0.03, stroke_width=4) for lt in lift])
        ends = [np.array([-STILL_X, AXIS_Y, 0]), np.array([STILL_X, AXIS_Y, 0])]
        axis = Line([AX0, AXIS_Y, 0], [AX1, AXIS_Y, 0], color=TOOL, stroke_width=3)
        t0, t1 = (float(TILE_TIMES[k].split(":")[-1]) for k in (BEFORE, AFTER))
        tick_x = [AX0 + (AX1 - AX0) * (float(t) - t0) / (t1 - t0) for _, t in FRAMES]
        ticks = VGroup(*[Line([x, AXIS_Y - 0.14, 0], [x, AXIS_Y + 0.14, 0], color=INK, stroke_width=3) for x in tick_x])
        gap_q = label("?", 40, INK).move_to([(AX0 + AX1) / 2, AXIS_Y + 0.35, 0])
        # the two stills' own burned-in times, at the ends of the axis (so the strip reads as "between them")
        end_l = VGroup(label(f"{t0:.3f} s", 24, INK).next_to([AX0, AXIS_Y, 0], UP, buff=0.16, aligned_edge=LEFT),
                       label(f"{t1:.3f} s", 24, INK).next_to([AX1, AXIS_Y, 0], UP, buff=0.16, aligned_edge=RIGHT))
        end_l[0].align_to([AX0, 0, 0], LEFT)
        end_l[1].align_to([AX1, 0, 0], RIGHT)
        frames = [exhibit(fn, width=FRAME_W, crop=FRAME_CROP).move_to([x, STRIP_Y, 0])
                  for (fn, _), x in zip(FRAMES, FRAME_X)]
        fans = VGroup(*[Line([x, AXIS_Y - 0.14, 0], fr.get_top() + UP * 0.04, color=TOOL, stroke_width=2,
                             stroke_opacity=0.5) for x, fr in zip(tick_x, frames)])
        times = VGroup(*[label(f"{t} s", 24, INK).next_to(fr, DOWN, buff=0.16) for (_, t), fr in zip(FRAMES, frames)])
        cap2_s = "frames 0.2 s apart: did anything move?"
        cap2 = label(cap2_s, 28, INK).move_to([0, -2.62, 0])
        cap2_parts = [glyphs_of(cap2, cap2_s, "frames 0.2 s apart:"), glyphs_of(cap2, cap2_s, "did anything move?")]
        src2 = source_caption("real frames 0.2 s apart and two stills of the contact sheet · tic-tac-toe video, scene 3")
        rings = VGroup()
        for a in range(1, 4):
            for rc in MOVED[a]:
                p = frames[a].px(*SQUARE[rc])
                rings.add(Circle(radius=0.27, color=MEASURED, stroke_width=4).move_to(p))

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(look, box_, cap_t)), *[FadeIn(lt) for lt in lift],
                      sheet.image.animate.set_opacity(0.25), Create(outline), run_time=0.7)
            vo.wait_until("things can go wrong")
            gone = collect(self, sheet, agent3, src1)
            self.play(FadeOut(gone), FadeOut(outline),
                      *[lt.animate.scale(STILL_W / TILE_UW).move_to(e) for lt, e in zip(lift, ends)], run_time=0.9)
            self.play(Create(axis), FadeIn(end_l, shift=UP * 0.1), FadeIn(gap_q, scale=0.6), run_time=0.6)
            # the "?" (what happens between stills) stays while "so to check motion" is spoken
            vo.wait_until("it grabs frames")
            self.play(FadeOut(gap_q, target_position=ticks.get_center() + UP * 0.2, scale=0.4),
                      LaggedStart(*[GrowFromCenter(t) for t in ticks], lag_ratio=0.2), run_time=0.5)
            self.play(LaggedStart(*[AnimationGroup(Create(fn), FadeIn(fr, target_position=[x, AXIS_Y, 0], scale=0.15))
                                    for fn, fr, x in zip(fans, frames, tick_x)], lag_ratio=0.25),
                      FadeIn(src2), run_time=0.9)
            vo.wait_until("a fifth of a second")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in times], lag_ratio=0.15),
                      FadeIn(cap2_parts[0]), run_time=0.8)
            wait_for(self, vo, "If they're all the same", -0.25)
            self.play(FadeIn(cap2_parts[1], shift=LEFT * 0.1), run_time=0.4)
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), run_time=0.9)
            wait_for(self, vo, "nothing moved", -0.25)
            self.play(LaggedStart(*[Indicate(r, color=S.WHITE, scale_factor=1.2) for r in rings], lag_ratio=0.08),
                      run_time=0.6)

        # ---------------------------------------------------------- measured: lint and the scenes' own checks
        chip1 = measured_badge("lint, without drawing a frame", 26)
        chip2 = measured_badge("the scenes check themselves", 26)
        chip1.move_to([LEFT_X + chip1.width / 2, 3.05, 0])
        chip2.move_to([LEFT_X + chip2.width / 2, 2.3, 0])

        term = terminal([(LINT_CMD, TOOL), ("…", TOOL), (LINT_LINES[0], INK), (LINT_LINES[1], MEASURED)], size=22)
        term.move_to([0, 0, 0]).align_to([LEFT_X, 0, 0], LEFT).align_to([0, 1.7, 0], UP)
        rows = term.lines
        left_span = glyphs_of(rows[2], LINT_LINES[0], "0 visible mobject(s) left on screen")
        flags = VGroup(*[flag_chip(fl) for fl in FLAGS]).arrange(RIGHT, buff=0.45)
        ok = rows[3]
        ok_arrow = Arrow([term.box.get_right()[0] + 0.62, ok.get_y(), 0], [term.box.get_right()[0] + 0.08, ok.get_y(), 0],
                         buff=0, color=TOOL, stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.35)
        ok_gloss = label("nothing flagged\nin this run", 24, TOOL).next_to(ok_arrow, RIGHT, buff=0.12)
        flags.move_to([(LEFT_X + ok_gloss.get_right()[0]) / 2, -2.2, 0])    # centred under terminal + gloss
        pictos = VGroup(*[flag_picto(fl.key) for fl in flags])
        for p, fl in zip(pictos, flags):                    # every little screen at the same height
            p.shift(fl.get_top() + UP * (0.3 + p[0].height / 2) - p[0].get_center())
        src3 = source_caption("real lint output · tic-tac-toe video, scene 3 · “…” marks cuts (the path, Manim's own warnings)")
        lint_view = [term, flags, pictos, ok_arrow, ok_gloss]

        panel = clipped_panel(CHECKS, "tic-tac-toe video · scenes/s03_stop.py", CHECKS_FIRST, cols=75, keep=())
        code = panel.code
        panel.move_to([0, 0, 0]).align_to([LEFT_X, 0, 0], LEFT).align_to([0, 1.7, 0], UP)
        glow_bar = Rectangle(width=code.background.width - 0.12, height=code.code_lines[GLOW_LINE].height + 0.16,
                             stroke_width=0).set_fill(MEASURED, 0).move_to(
            [code.background.get_center()[0], code.code_lines[GLOW_LINE].get_center()[1], 0])
        code.submobjects.insert(1, glow_bar)
        nums = [code_span(code, k, s.replace("== ", "")) if s.startswith("== ") else code_span(code, k, s)
                for k, s in NUMBERS]
        n_num = DecimalNumber(0, num_decimal_places=0, font_size=56, color=MEASURED)
        n_text = VGroup(label("checks in the tic-tac-toe scenes", 24, INK),
                        label("most of them on numbers", 24, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        room = VGroup(DecimalNumber(88, num_decimal_places=0, font_size=56), n_text).arrange(RIGHT, buff=0.28)
        n_box = box(room.width + 0.6, room.height + 0.4, MEASURED, fill_opacity=0.1, radius=0.18)
        room.move_to(n_box)              # the box has room for two digits; the count starts at 0
        n_num.next_to(n_text, LEFT, buff=0.28)
        counter = VGroup(n_box, n_num, n_text)
        counter.move_to([6.45 - counter.width / 2, 2.67, 0])
        n_num.add_updater(lambda m: m.next_to(n_text, LEFT, buff=0.28))       # grows to the left as it counts

        with self.voiceover(SAY[3]) as vo:
            strip = collect(self, *lift, axis, end_l, ticks, fans, *frames, times, cap2, src2)
            self.play(FadeOut(strip), run_time=0.5)              # the GREEN rings stay: they were a measurement
            # each ring (a measured change) becomes the check mark of a GREEN check chip, which then opens
            marks = [chip1.icon.copy() for _ in range(3)] + [chip2.icon.copy() for _ in range(3)]
            self.play(*[ReplacementTransform(r, m) for r, m in zip(rings, marks)], run_time=0.8)
            self.remove(*marks)
            for c in (chip1, chip2):
                c.box.set_z_index(-1)                            # the box fades in under its check mark
                self.add(c.icon)
            self.play(*[FadeIn(c.box, scale=0.9) for c in (chip1, chip2)],
                      *[FadeIn(c.text, shift=LEFT * 0.15) for c in (chip1, chip2)], run_time=0.5)
            for c in (chip1, chip2):
                adopt(self, c)
                c.box.set_z_index(0)

            wait_for(self, vo, "A checker called", -0.25)
            self.play(Indicate(chip1[1], color=S.WHITE, scale_factor=1.04),       # text and check, not the box
                      FadeIn(VGroup(term.box, term[1], term[2]), target_position=chip1.get_center(), scale=0.2),
                      run_time=0.7)
            self.play(AddTextLetterByLetter(rows[0], run_time=0.7))
            wait_for(self, vo, "runs each scene", -0.4)
            self.play(FadeIn(rows[1]), FadeIn(rows[2], shift=UP * 0.1), FadeIn(src3), run_time=0.6)
            wait_for(self, vo, "without drawing", -0.5)
            self.play(FadeIn(rows[3], scale=1.3), run_time=0.4)
            # the run is clean: say so before the flags come in, so they read as a legend, not findings
            self.play(GrowArrow(ok_arrow), FadeIn(ok_gloss, shift=LEFT * 0.1), run_time=0.5)
            wait_for(self, vo, "and flags anything", -0.3)      # on "flags"
            self.play(LaggedStart(*[Create(p[0]) for p in pictos], lag_ratio=0.25), run_time=0.8)
            wait_for(self, vo, "off screen", -0.7)
            self.play(FadeIn(flags[0], shift=UP * 0.15), FadeIn(VGroup(*pictos[0][1:]), scale=0.5), run_time=0.5)
            wait_for(self, vo, "text that's too small", -0.5)
            self.play(FadeIn(flags[1], shift=UP * 0.15), FadeIn(VGroup(*pictos[1][1:]), scale=0.5), run_time=0.5)
            wait_for(self, vo, "or objects left behind", -0.5)
            self.play(FadeIn(flags[2], shift=UP * 0.15), FadeIn(VGroup(*pictos[2][1:]), scale=0.5),
                      emphasize(left_span, run_time=0.8), run_time=0.8)
            self.play(Indicate(ok, color=S.WHITE), Indicate(ok_gloss, color=S.WHITE, scale_factor=1.05), run_time=0.6)

            wait_for(self, vo, "And the tic-tac-toe scenes", -0.25)
            view = collect(self, *lint_view)
            self.play(FadeOut(view, target_position=chip1.get_center(), scale=0.1), FadeOut(src3), run_time=0.6)
            self.play(Indicate(chip2[1], color=S.WHITE, scale_factor=1.04),
                      FadeIn(panel, target_position=chip2.get_center(), scale=0.15), run_time=0.8)
            wait_for(self, vo, "check themselves", -0.3)
            self.play(code.code_lines[GLOW_LINE].animate.set_opacity(1), glow_bar.animate.set_fill(opacity=0.2),
                      run_time=0.6)
            wait_for(self, vo, "with 82 checks", -0.3)        # the count reaches 82 as "checks" is said
            self.play(FadeIn(VGroup(n_box, n_text), shift=LEFT * 0.2), FadeIn(n_num), run_time=0.3)
            self.play(ChangeDecimalToValue(n_num, N_ASSERTS), run_time=0.8, rate_func=smooth)
            adopt(self, counter)
            vo.wait_until("most of them")
            self.play(LaggedStart(*[n.animate.set_color(MEASURED).set_opacity(1) for n in nums], lag_ratio=0.2),
                      emphasize(n_text[1], run_time=1.0), run_time=1.0)
            self.play(LaggedStart(*[Indicate(n, color=S.WHITE, scale_factor=1.12) for n in nums], lag_ratio=0.2),
                      run_time=1.0)
        n_num.clear_updaters()
        self.wait(0.8)
        fade_out_all(self)
