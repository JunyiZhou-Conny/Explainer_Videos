"""S07 · Reviewers who pretend.

Beats: the review loop: the BLUE agent hands a "draft video" (a GREY player with its ORANGE sound
track) towards two faded-BLUE reviewers, tagged "fresh agents · didn't build it"; the picture
becomes the real contact sheet (A01) and the sound becomes "subtitles = the sound"; "a role" comes
from the agent and turns into the two labels, "director" and "a simulated 12-year-old"; a real
line of the round-1 QA prompt for the simulated kid (A42) -> the kid's note (A10, qa_round1.txt
line 38) in a speech bubble -> the bubble shrinks into one of the 30 round-1 issues (A10, coloured
by kind: 3 wrong, 13 confusing, 14 polish, in the order of the notes); the "12 on the formula
line" item (line 30) is pulled out, glows and goes back; the 30 go into a BLUE "fix round" and 30
come out of it for round 2: 25 fixed (GREEN), 5 partly fixed (dashed YELLOW) (the record doesn't
say which ones, so none is mapped to a round-1 square), plus 18 new or remaining notes; the score
card with both caveats (dashed YELLOW) -> the round-1 director and its "wrong" note carry over
into the frozen shuffle: four real frames 0.2 s apart re-rendered from the old code (A03), the
board the same in all four while the counter (zoomed in) reads 5, 5, 6, 7; the note becomes the
RED tag "frozen" -> the strip moves up; under it the real old line (A25) with `.animate` RED; a
diagram of one mark with one "next spot" note: four planned moves fly out of `.animate` into the
note, each overwriting the last, so the mark jumps straight to the last spot -> the real fix
(A26, line 203) with `lambda` GREEN: each move is written into the note as it plays, and the mark
visits every spot -> the real "after" frames (A02), GREEN rings on the marks that moved -> four
mini scene cards of the privacy video (diagram): "Dan" in scenes 3-4, "Dev" in 5-6, a RED ≠; a
faded-BLUE cross-scene reviewer bar sweeps across and the names settle on "Dan"; five differently
drawn budget bars collapse into one shared drawing (A38).

Every number and quote on screen is checked in _check() (runs on import) against the assets.

Helpers defined here (not in common.py): collect() (like common.gather, but each part's whole
family leaves the top level first, as in s05), glyphs_of(), clipped_panel() (a code panel cut at a
column like an editor window, as in s05), dim_code_panel(), frame_strip() (real frames, each a
board crop with the same frame's counter zoomed in beside it), equals_sign(), issue_square(),
number_chip(), scene_card(), budget_variants().
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.scene import VoiceScene

from common import (AGENT, BUG, EXCERPTS, INK, MEASURED, NARRATION, OPEN, PANEL, SUB_AGENT, SUB_AGENT_TEXT,
                    TOOL, asset, asset_text, box, bug_tag, caption, chip, code_block, code_span, emphasize,
                    exhibit, fade_out_all, label, load_envelope, mono, open_outline, rerender_tag, role_icon,
                    source_caption, speech_bubble, tag, video_player, waveform, wrap)

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real material (assets/)
A03, A10, A38, A42 = EXCERPTS["A03"], EXCERPTS["A10"], EXCERPTS["A38"], EXCERPTS["A42"]
FUNNEL = A10["funnel"]
KID_NOTE = A10["r1_line38_bubble"]                       # "… couldn't work out what X0 meant (X's zeroth move?)"
LINE30 = A10["r1_line30"]
TWELVE = "4 × 3 × 2      12"                             # as line 30 quotes the paused frame
SCORE = "simulated kid: 8/10 → 8.5/10"
CAVEATS = A10["score_caveats"].split(" · ")

OLD_SRC = asset_text(EXCERPTS["A25"]["file"]).splitlines()      # s03_stop.py at 8a922bf, lines 280-282
OLD_LINE = OLD_SRC[0].strip()                                    # line 280
FIX_SRC = asset_text(EXCERPTS["A26"]["file"]).splitlines()      # s03_stop.py lines 200-203
FIX_LINE = FIX_SRC[3].strip()                                    # line 203
DOCSTRING = EXCERPTS["A26"]["docstring"]                         # "The `.animate`s are made only when the step plays."

# Real frames, cropped alike: the old 720p re-render (A03) and the final 1080p render (A02) share
# one layout at a 1.5 ratio. Each tile is the board, with the same frame's GREEN counter zoomed in
# beside it (in the old layout the counter sat far to the right, on the formula line).
OLD_FRAMES = A03["frozen_frames"]["files"]
OLD_COUNTS = A03["frozen_frames"]["counter"]                     # 5, 5, 6, 7
NEW_FRAMES = [f"ttt_s03_moving_{t}.png" for t in ("19.6", "19.8", "20.0", "20.2")]
OLD_BOARD, OLD_COUNT = (55, 190, 441, 576), (995, 316, 1047, 368)
NEW_BOARD, NEW_COUNT = (82, 285, 661, 864), (585, 949, 637, 1001)
OLD_GHOSTS = [(128.7, 381), (367.3, 381), (128.7, 501), (248, 501)]          # the 4 dashed marks (old px)
NEW_COL, NEW_ROW = (192.7, 372.0, 551.3), (393.7, 573.0, 752.3)              # square centres (new px)
MOVED = [[], [(0, 2), (1, 2)], [(0, 2), (1, 2)], [(0, 1), (0, 2)]]          # squares (col, row) that changed

# round 1, in the order of qa_round1.txt: the kind of each of the 30 notes (the kid's, then the director's)
R1_KINDS = (["confusing"] * 7 + ["wrong", "confusing"] + ["polish"] * 8 + ["wrong", "wrong"]
            + ["confusing"] * 5 + ["polish"] * 6)
R1_LINES = [25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89,
            124, 128, 132, 136, 140, 144, 148, 152, 156, 160, 164, 168, 172]
ORDER = sorted(range(30), key=lambda i: (["wrong", "confusing", "polish"].index(R1_KINDS[i]), i))
SLOT = {R1_LINES[i]: k for k, i in enumerate(ORDER)}             # file line -> slot in the grid
KID_X0, TWELVE_ITEM, FROZEN_ITEM = SLOT[37], SLOT[29], SLOT[124]  # the X0 note, the 12, the frozen shuffle


def _check():
    assert A42["text"].startswith("go through the contact sheets") and A42["text"].endswith("that is the video.")
    assert KID_NOTE == "… couldn't work out what X0 meant (X's zeroth move?)"
    assert f"'{TWELVE}'" in LINE30
    qa1 = asset_text("qa_round1.txt").splitlines()
    assert "couldn't work out what X0 meant (X's zeroth move?)" in qa1[37]          # line 38
    assert TWELVE in qa1[29]                                                        # line 30
    kinds = [ln.split("][")[1].split("]")[0] for ln in qa1 if ln.startswith("[")]
    assert kinds == R1_KINDS and [i + 1 for i, ln in enumerate(qa1) if ln.startswith("[")] == R1_LINES
    assert qa1[123].startswith("[S03][wrong]") and "does not play" in qa1[124]      # the frozen shuffle
    assert qa1[28].startswith("[S03][confusing]") and qa1[36].startswith("[S01][confusing]")
    r1 = FUNNEL["round1"]
    assert (r1["issues"], r1["wrong"], r1["confusing"], r1["polish"]) == (30, 3, 13, 14)
    assert [R1_KINDS.count(k) for k in ("wrong", "confusing", "polish")] == [3, 13, 14]
    r2 = FUNNEL["round2"]
    assert (r2["fixed"], r2["partly"], r2["wrong"], r2["new_or_remaining"]) == (25, 5, 0, 18)
    qa2 = asset_text("qa_round2.txt")
    assert "25 are fixed and 5 are partly fixed" in qa2 and sum(ln.startswith("[") for ln in qa2.splitlines()) == 18
    assert A10["r1_score"] == "about 8/10" and A10["r2_score"] == "8.5/10" and "8.5/10" in qa2
    assert CAVEATS == ["a model's guess, not a real child's", "the second kid had read the first one's notes"]
    assert OLD_LINE == "steps.append(([ghosts[start[cur[p]]].animate(path_arc=arc)"
    assert FIX_LINE == "return lambda: [m.animate(path_arc=path_arc).move_to(p) for m, p in moves]"
    assert DOCSTRING in FIX_SRC[2]
    assert OLD_COUNTS == [5, 5, 6, 7] and A03["frozen_frames"]["t"] == [20.6, 20.8, 21.0, 21.2]
    assert A38["src"] == "privacy video, whole-video QA notes" and "'Dev' to 'Dan'" in A38["rename"]
    assert A38["budget_bar"] == "is drawn five different ways"
    for f in OLD_FRAMES + NEW_FRAMES + ["ttt_s03_sheet_01.png"]:
        asset(f)


_check()

# ------------------------------------------------------------------ layout
ROW_Y = 1.15                         # beat 1: the review loop
X_AGENT, X_DRAFT, X_GOT, X_DIR, X_KID = -5.6, -3.4, -1.0, 2.2, 4.7
R1_X, R2_X, GRID_Y, HEAD_Y = -3.85, 3.85, 1.45, 2.85
BIG_H, SMALL_H = 2.2, 1.35           # frame tiles: big view, then the before/after rows
SHRINK = SMALL_H / BIG_H
BIG_HEAD_Y, BIG_Y = 2.05, 0.15       # the frozen frames, big
TOP_HEAD_Y, TOP_STRIP_Y, OLD_CODE_Y = 3.2, 2.13, 1.0
LOW_HEAD_Y, LOW_STRIP_Y, FIX_CODE_Y = 0.0, -1.05, -2.2
NOTE_Y, SPOT_Y = -0.15, -1.2         # the diagram, in the lower band before the "after" row comes
START_X, SPOTS_X = -4.75, (-2.6, -0.85, 0.9, 2.65)
SIDE_X = 5.45                        # "4 frames, 0.2 s apart", right of the small strips


# ------------------------------------------------------------------ helpers (this scene only)
def collect(scene, *mobs) -> Group:
    """Make several on-screen things ONE top-level group: each thing's whole family leaves the top
    level first (parts animated in one by one would otherwise stay behind after a FadeOut)."""
    for m in mobs:
        scene.remove(*m.get_family())
    g = Group(*mobs)
    scene.add(g)
    return g


def glyphs_of(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of substring `sub` in a Text built from string s (whitespace, line breaks
    included, has no glyphs, so `sub` may run across a line break)."""
    flat, want = "".join(s.split()), "".join(sub.split())
    start = flat.find(want)
    assert start >= 0, (sub, s)
    return VGroup(*t[start:start + len(want)])


def tighten(c: Code, pad_y: float = 0.16) -> Code:
    """Give a one-line code panel a slimmer background (same colours and corners, less padding above
    and below the line), so two panels and two frame strips fit on one screen."""
    bg = c.background
    new = RoundedRectangle(width=bg.width, height=c.code_lines.height + 2 * pad_y, corner_radius=0.15,
                           stroke_color=S.GREY_DARK, stroke_width=2).set_fill(S.GREY_DARKER, 1)
    new.move_to([bg.get_x(), c.code_lines.get_y(), 0])
    c.remove(bg)
    c.add_to_back(new)
    c.background = new
    return c


def clipped_panel(source: str, path: str, first_line: int, cols: int, font_size: float = 22,
                  fade: int = 6, note: str = "") -> VGroup:
    """A one-line real excerpt in the house code style, cut at `cols` columns like an editor window:
    glyphs beyond it are dropped and the last `fade` columns fade out, so the line visibly runs on
    past the panel edge. .code .caption"""
    c = code_block(source, font_size)
    cols_k = [j for j, ch in enumerate(source) if not ch.isspace()]
    glyphs = c.code_lines[0]
    assert len(cols_k) == len(glyphs), source
    drop = [g for g, j in zip(glyphs, cols_k) if j >= cols]
    for g, j in zip(glyphs, cols_k):
        if cols - fade <= j < cols:
            g.set_opacity((cols - j) / (fade + 1))
    if drop:
        glyphs.remove(*drop)
        bg = c.background
        pad = c.code_lines.get_left()[0] - bg.get_left()[0]
        adv = 0.2001855 * font_size / 24                      # DejaVu Sans Mono advance
        right = c.code_lines.get_left()[0] + cols * adv + pad * 0.5
        new = RoundedRectangle(width=right - bg.get_left()[0], height=bg.height, corner_radius=0.15,
                               stroke_color=S.GREY_DARK, stroke_width=2).set_fill(S.GREY_DARKER, 1)
        new.align_to(bg, LEFT).match_y(bg)
        c.remove(bg)
        c.add_to_back(new)
        c.background = new
    tighten(c)
    cap = caption(f"{path} · line {first_line}{note}").next_to(c, DOWN, buff=0.1).align_to(c, LEFT)
    g = VGroup(c, cap)
    g.code, g.caption = c, cap
    return g


def dim_code_panel(source: str, path: str, first_line: int, font_size: float = 22, dim: float = 0.4) -> VGroup:
    """A one-line real excerpt (the whole line) in the house style, faded but for what we point at.
    .code .caption"""
    c = code_block(source, font_size)
    for g in c.code_lines[0]:
        g.set_opacity(dim)
    tighten(c)
    cap = caption(f"{path} · line {first_line}").next_to(c, DOWN, buff=0.1).align_to(c, LEFT)
    g = VGroup(c, cap)
    g.code, g.caption = c, cap
    return g


class Strip(Group):
    """frame_strip(): .tiles, each a Group(board, count) with .board and .count (Exhibits)."""


def frame_strip(names, board_crop, count_crop, height: float = BIG_H, gap: float = 0.42) -> Strip:
    """Four real frames side by side: each the board, with that frame's counter zoomed in beside it."""
    tiles = []
    for n in names:
        board = exhibit(n, height=height, crop=board_crop)
        count = exhibit(n, height=height * 0.28, crop=count_crop)
        count.next_to(board, RIGHT, buff=height * 0.045)
        t = Group(board, count)
        t.board, t.count = board, count
        tiles.append(t)
    s = Strip(*tiles).arrange(RIGHT, buff=gap)
    s.tiles = tiles
    return s


def equals_sign(width: float = 0.22, color: str = BUG, stroke: float = 5) -> VGroup:
    """'=' drawn as two strokes (it scales with the strip; no font size to shrink)."""
    return VGroup(*[Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=stroke).shift(UP * dy)
                    for dy in (0.06, -0.06)])


def issue_square(kind: str, side: float = 0.36) -> VMobject:
    """One QA note: wrong = RED, confusing = RED outline, polish = GREY; round 2: fixed = GREEN,
    partly fixed = dashed YELLOW (still open); note = GREY (round 2's new or remaining notes)."""
    if kind == "partly":
        return box(side, side, OPEN, dashed=True, stroke=3, radius=0.06)
    col, op = {"wrong": (BUG, 0.85), "confusing": (BUG, 0.16), "polish": (TOOL, 0.12),
               "fixed": (MEASURED, 0.85), "pending": (TOOL, 0.0), "note": (TOOL, 0.12)}[kind]
    return box(side, side, col, fill_opacity=op, stroke=2.5, radius=0.06)


def number_chip(k: int, size: float = 28) -> VGroup:
    """A planned move: the number of the spot it goes to, on a small GREY card."""
    t = label(str(k), size, INK)
    b = box(0.5, 0.5, TOOL, fill=PANEL, fill_opacity=1, radius=0.08)
    t.move_to(b)
    return VGroup(b, t)


def scene_card(n: int, name: str, width: float = 2.9, height: float = 2.2) -> VGroup:
    """A mini scene of the privacy video (a diagram): 'scene n' and a few table rows, one with a
    person's name. .box .name .row .builder (a faded-BLUE icon standing on the card's top edge)"""
    b = box(width, height, TOOL, fill=PANEL, fill_opacity=1, radius=0.16)
    head = label(f"scene {n}", 24, S.GREY).move_to(b.get_corner(UL) + np.array([0.22, -0.32, 0]), aligned_edge=LEFT)
    rows = VGroup(*[RoundedRectangle(width=width - 0.5, height=0.44, corner_radius=0.07, stroke_color=S.GREY_DARK,
                                     stroke_width=1.5).set_fill(S.BG, 1) for _ in range(3)])
    rows.arrange(DOWN, buff=0.08).next_to(head, DOWN, buff=0.2).match_x(b)
    for k in (0, 2):                                     # the other rows: no names, just their shape
        rows[k].add(Line(rows[k].get_left() + RIGHT * 0.6, rows[k].get_left() + RIGHT * 1.5,
                         stroke_width=4, color=S.GREY_DARK))
    who = VGroup(person_icon(S.GREY, 0.3), label(name, 26, INK)).arrange(RIGHT, buff=0.16)
    who.move_to(rows[1]).align_to(rows[1], LEFT).shift(RIGHT * 0.18)
    builder = role_icon("sub", 0.62).person
    builder.next_to(b, UP, buff=0.06).align_to(b, RIGHT).shift(LEFT * 0.3)
    g = VGroup(b, head, rows, who)
    g.box, g.name, g.builder, g.row = b, who[1], builder, rows[1]
    return g


def budget_variants(width: float = 1.75):
    """Five ways of drawing one 'privacy budget' bar (a diagram, in GREY), and the one shared drawing."""
    h = 0.3
    v1 = VGroup(Rectangle(width=width, height=h, stroke_color=TOOL, stroke_width=2.5),
                *[Rectangle(width=(width - 0.36) / 8, height=h - 0.1, stroke_width=0).set_fill(TOOL, 0.9)
                  for _ in range(5)])
    v1[1:].arrange(RIGHT, buff=0.04).align_to(v1[0], LEFT).shift(RIGHT * 0.04)
    v2 = VGroup(RoundedRectangle(width=width, height=h * 1.2, corner_radius=h * 0.6, stroke_color=TOOL,
                                 stroke_width=2.5),
                RoundedRectangle(width=width * 0.6, height=h * 1.2, corner_radius=h * 0.6, stroke_width=0)
                .set_fill(INK, 0.55))
    v2[1].align_to(v2[0], LEFT)
    v3 = VGroup(Line(LEFT * width / 2, RIGHT * width / 2, color=TOOL, stroke_width=3),
                Dot(radius=0.1, color=INK).shift(RIGHT * width * 0.1))
    v4 = VGroup(*[Circle(radius=0.14, stroke_color=TOOL, stroke_width=2.5).set_fill(TOOL, 0.9 if k < 3 else 0)
                  for k in range(5)]).arrange(RIGHT, buff=0.12)
    v5 = VGroup(Rectangle(width=0.34, height=0.9, stroke_color=TOOL, stroke_width=2.5),
                Rectangle(width=0.34, height=0.54, stroke_width=0).set_fill(TOOL, 0.8))
    v5[1].align_to(v5[0], DOWN)
    shared_w = 2.8
    shared = VGroup(Rectangle(width=shared_w, height=0.32, stroke_color=TOOL, stroke_width=2.5),
                    *[Rectangle(width=(shared_w - 0.36) / 8, height=0.22, stroke_width=0).set_fill(TOOL, 0.9)
                      for _ in range(8)])
    shared[1:].arrange(RIGHT, buff=0.04).move_to(shared[0])
    return VGroup(v1, v2, v3, v4, v5), shared


class Reviewers(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- beat 1: the review loop
        agent = role_icon("agent", 1.15).move_to([X_AGENT, ROW_Y, 0])
        agent_l = label("the agent", 24, AGENT).next_to(agent, DOWN, buff=0.22)
        director = role_icon("sub", 1.15).move_to([X_DIR, ROW_Y, 0])
        kid = role_icon("sub", 1.15).move_to([X_KID, ROW_Y, 0])
        fresh = tag("fresh agents · didn't build it", SUB_AGENT_TEXT, size=24)
        fresh.move_to([(X_DIR + X_KID) / 2, 2.55, 0])

        player = video_player(1.7, progress=0.55).move_to([X_DRAFT, ROW_Y + 0.3, 0])
        _, env = load_envelope()
        track = waveform(env[:420], width=1.7, height=0.3, step=3).next_to(player, DOWN, buff=0.14)
        draft_l = label("draft video", 24, TOOL).next_to(track, DOWN, buff=0.16)
        draft = VGroup(player, track, draft_l)
        hand = Arrow([X_AGENT + 0.62, ROW_Y + 0.3, 0], [X_DRAFT - 1.05, ROW_Y + 0.3, 0], buff=0, color=AGENT,
                     stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.35)

        sheet = exhibit("ttt_s03_sheet_01.png", width=2.0).move_to([X_GOT, 2.2, 0])
        sheet_l = caption("contact sheets", 22).next_to(sheet, DOWN, buff=0.08)
        subs = chip("subtitles = the sound", TOOL, 24).move_to([X_GOT, 0.78, 0])
        role = chip("a role", SUB_AGENT_TEXT, 24).move_to([X_GOT, 0.02, 0])
        got = VGroup(sheet.frame, sheet_l, subs, role)
        feed = Arrow([got.get_right()[0] + 0.12, ROW_Y, 0], [X_DIR - 0.62, ROW_Y, 0], buff=0, color=TOOL,
                     stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.35)
        sheet_src = source_caption("real contact sheet · tic-tac-toe video, scene 3")
        hand2 = Arrow([X_AGENT + 0.62, ROW_Y, 0], [got.get_left()[0] - 0.14, ROW_Y, 0], buff=0, color=AGENT,
                      stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.1)
        dir_l = label("director", 24, SUB_AGENT_TEXT).next_to(director, DOWN, buff=0.22)
        kid_l = label("a simulated 12-year-old", 24, SUB_AGENT_TEXT).next_to(kid, DOWN, buff=0.22)
        kid_l2 = caption("sharp but ordinary", 22).next_to(kid_l, DOWN, buff=0.08)

        prompt_text = label("“" + wrap(A42["text"], 56).replace("\n", "\n ") + "”", 24, INK, line_spacing=1.0)
        prompt_box = box(prompt_text.width + 0.6, prompt_text.height + 0.45, TOOL, fill=PANEL, fill_opacity=1)
        prompt_text.move_to(prompt_box)
        prompt_cap = caption(A42["caption"], 20).next_to(prompt_box, DOWN, buff=0.1).align_to(prompt_box, RIGHT)
        prompt = VGroup(prompt_box, prompt_text, prompt_cap).move_to([-1.2, -2.0, 0])
        the_video = glyphs_of(prompt_text, prompt_text.original_text, "that is the video.")
        to_kid = DashedLine(prompt_box.get_corner(UR) + LEFT * 0.5, kid_l2.get_bottom() + DOWN * 0.08,
                            color=TOOL, stroke_width=2, dash_length=0.08)

        bubble = speech_bubble(KID_NOTE, chars=30, tail=UP, tail_shift=0.22)
        bubble.move_to([3.6, -1.55, 0])
        bubble.shift(np.array([X_KID - bubble.tail.get_vertices()[2][0], 0, 0]))
        x0 = glyphs_of(bubble.text, bubble.text.original_text, "X0")
        src1 = source_caption("QA notes, round 1 · tic-tac-toe video (qa_round1.txt, line 38)")
        assert kid_l.get_right()[0] < 6.5 and bubble.get_right()[0] < 6.5

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(agent, shift=UP * 0.2), FadeIn(agent_l), run_time=0.6)
            vo.wait_until("the reviewers")
            self.play(LaggedStart(FadeIn(director, shift=UP * 0.2), FadeIn(kid, shift=UP * 0.2), lag_ratio=0.3),
                      run_time=0.8)
            vo.wait_until("fresh agents")
            self.play(FadeIn(fresh, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("didn't build")
            self.play(GrowArrow(hand), FadeIn(draft, target_position=agent.get_center(), scale=0.3), run_time=0.9)

            vo.wait_until("They get the stills")
            self.play(player.animate.move_to(sheet).scale(sheet.width / player.width).set_opacity(0),
                      FadeIn(sheet, scale=player.width / sheet.width), run_time=0.9)
            self.remove(player)
            self.play(FadeIn(sheet_l), FadeIn(sheet_src), run_time=0.3)
            vo.wait_until("the subtitles")
            self.play(ReplacementTransform(track, subs.box), FadeIn(subs.text), draft_l.animate.set_opacity(0),
                      ReplacementTransform(hand, hand2), run_time=0.9)
            self.remove(draft_l)
            self.play(GrowArrow(feed), FadeIn(prompt, shift=UP * 0.2), run_time=0.7)
            self.play(emphasize(the_video, run_time=0.7))

            vo.wait_until("and a role")
            self.play(FadeIn(role, target_position=agent.get_center(), scale=0.4), run_time=0.7)
            vo.wait_until("a director")
            self.play(TransformFromCopy(role, dir_l, path_arc=-PI / 6), run_time=0.7)
            vo.wait_until("or a simulated")
            self.play(TransformFromCopy(role, kid_l, path_arc=-PI / 6), run_time=0.8)
            vo.wait_until("sharp but ordinary")
            self.play(FadeIn(kid_l2, shift=UP * 0.1), Create(to_kid), run_time=0.7)

            vo.wait_until("That simulated kid")
            self.play(FadeOut(collect(self, prompt, to_kid, sheet_src), shift=DOWN * 0.2), run_time=0.5)
            self.play(FadeIn(bubble, shift=UP * 0.15), FadeIn(src1), run_time=0.7)
            vo.wait_until("like move labels")
            self.play(Circumscribe(x0, color=S.WHITE, buff=0.06, run_time=1.0))

        # ---------------------------------------------------------- beat 2: round 1 -> fix round -> round 2
        grid1 = VGroup(*[issue_square(R1_KINDS[i]) for i in ORDER]).arrange_in_grid(rows=3, cols=10, buff=0.1)
        grid1.move_to([R1_X, GRID_Y, 0])
        r1_icons = VGroup(role_icon("sub", 0.8), role_icon("sub", 0.8)).arrange(RIGHT, buff=0.25)
        r1_head = VGroup(r1_icons, label("round 1", 28)).arrange(RIGHT, buff=0.3).move_to([R1_X, HEAD_Y, 0])
        r1_kid, r1_dir = r1_icons
        r1 = FUNNEL["round1"]
        leg1a = label(f"{r1['issues']} issues:", 26)
        leg1b = label(f"{r1['wrong']} wrong · {r1['confusing']} confusing · {r1['polish']} polish", 24,
                      t2c={"3 wrong": BUG, "13 confusing": BUG, "14 polish": TOOL})
        leg1 = VGroup(leg1a, leg1b).arrange(DOWN, buff=0.1).next_to(grid1, DOWN, buff=0.3)

        fix = chip("fix round", AGENT, 26).move_to([0, GRID_Y, 0])
        a_in = Arrow(grid1.get_right() + RIGHT * 0.08, fix.get_left() + LEFT * 0.05, buff=0, color=TOOL,
                     stroke_width=3, tip_length=0.15, max_tip_length_to_length_ratio=0.4)
        grid2 = VGroup(*[issue_square("pending") for _ in range(30)]).arrange_in_grid(rows=3, cols=10, buff=0.1)
        grid2.move_to([R2_X, GRID_Y, 0])
        a_out = Arrow(fix.get_right() + RIGHT * 0.05, grid2.get_left() + LEFT * 0.08, buff=0, color=TOOL,
                      stroke_width=3, tip_length=0.15, max_tip_length_to_length_ratio=0.4)
        fixed_sq = VGroup(*[issue_square("fixed").move_to(grid2[k]) for k in range(25)])
        partly_sq = VGroup(*[issue_square("partly").move_to(grid2[k]) for k in range(25, 30)])
        r2_dir = role_icon("sub", 0.8)
        r2_head = VGroup(r2_dir, label("round 2", 28)).arrange(RIGHT, buff=0.3).move_to([R2_X, HEAD_Y, 0])
        r2 = FUNNEL["round2"]
        leg2a = label("a fresh director re-checked all 30:", 24)
        leg2b = label(f"{r2['fixed']} fixed · {r2['partly']} partly fixed · {r2['wrong']} wrong", 24,
                      t2c={"25 fixed": MEASURED, "5 partly fixed": OPEN, "0 wrong": BUG})
        leg2 = VGroup(leg2a, leg2b).arrange(DOWN, buff=0.1).next_to(grid2, DOWN, buff=0.3)
        notes = VGroup(*[issue_square("note", 0.24) for _ in range(r2["new_or_remaining"])])
        notes.arrange_in_grid(rows=2, cols=9, buff=0.08).next_to(leg2, DOWN, buff=0.3)
        notes_l = label(f"+ {r2['new_or_remaining']} new or remaining notes", 24, TOOL).next_to(notes, DOWN, buff=0.12)

        twelve_t = label("“" + wrap(TWELVE, 40) + "”", 28, INK)
        twelve_b = box(twelve_t.width + 0.5, twelve_t.height + 0.36, BUG, fill_opacity=0.16, radius=0.1)
        twelve_t.move_to(twelve_b)
        twelve_c = caption("round 1 · qa_round1.txt, line 30", 20).next_to(twelve_b, DOWN, buff=0.1)
        twelve = VGroup(twelve_b, twelve_t, twelve_c).move_to([R1_X, -1.35, 0])

        score_lines = VGroup(label(SCORE, 26), *[label(c, 22, TOOL) for c in CAVEATS]).arrange(DOWN, buff=0.1)
        score_box = open_outline(score_lines, buff=0.22)
        score = VGroup(score_box, score_lines)
        score.move_to([0, -2.55, 0]).align_to([6.45, 0, 0], RIGHT)
        src2 = source_caption("QA notes of the tic-tac-toe video, rounds 1 and 2")

        with self.voiceover(SAY[1]) as vo:
            out1 = collect(self, agent, agent_l, hand2, sheet, sheet_l, subs, role, feed, fresh, dir_l,
                           kid_l, kid_l2, src1)
            target = grid1[KID_X0]
            others = [grid1[k] for k in range(30) if k != KID_X0]
            self.play(FadeOut(out1), ReplacementTransform(director, r1_dir), ReplacementTransform(kid, r1_kid),
                      FadeIn(r1_head[1]), ReplacementTransform(bubble, target), FadeIn(src2),
                      LaggedStart(*[FadeIn(s, scale=0.4) for s in others], lag_ratio=0.03), run_time=1.2)
            self.play(FadeIn(leg1, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("including that 12")
            slot = grid1[TWELVE_ITEM]
            hole = slot.copy().set_fill(opacity=0).set_stroke(opacity=0.35)
            self.add(hole)
            self.play(ReplacementTransform(slot, twelve_b), FadeIn(twelve_t, target_position=slot), run_time=0.8)
            self.play(FadeIn(twelve_c), emphasize(twelve_b, run_time=1.0, circle=True))

            vo.wait_until("In round two")
            back = issue_square("confusing").move_to(hole)
            self.play(ReplacementTransform(twelve_b, back), FadeOut(twelve_t, target_position=hole),
                      FadeOut(twelve_c), run_time=0.7)
            self.remove(hole)
            grid1.submobjects[TWELVE_ITEM] = back
            self.play(FadeIn(r2_head, shift=DOWN * 0.15), GrowArrow(a_in), FadeIn(fix, scale=0.8), run_time=0.6)
            vo.wait_until("a fresh director")
            self.play(Indicate(r2_dir, color=S.WHITE, scale_factor=1.15), run_time=0.6)
            flying = [s.copy() for s in grid1]
            self.play(LaggedStart(*[s.animate.move_to(fix).scale(0.2).set_opacity(0) for s in flying],
                                  lag_ratio=0.02), run_time=0.9)
            self.remove(*flying)
            self.play(GrowArrow(a_out), LaggedStart(*[FadeIn(s, target_position=fix, scale=0.2) for s in grid2],
                                                   lag_ratio=0.02), run_time=0.9)
            vo.wait_until("25 were fixed")
            self.play(LaggedStart(*[ReplacementTransform(grid2[k], fixed_sq[k]) for k in range(25)], lag_ratio=0.03),
                      FadeIn(leg2a), run_time=1.0)
            vo.wait_until("and 5 only partly")
            self.play(*[ReplacementTransform(grid2[k], partly_sq[k - 25]) for k in range(25, 30)],
                      FadeIn(leg2b, shift=UP * 0.1), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(n, scale=0.4) for n in notes], lag_ratio=0.03), FadeIn(notes_l), run_time=0.8)
        self.play(FadeIn(score, shift=UP * 0.15), run_time=0.6)
        self.wait(1.4)

        # ---------------------------------------------------------- beat 3: the frozen shuffle
        before = frame_strip(OLD_FRAMES, OLD_BOARD, OLD_COUNT).move_to([0, BIG_Y, 0])
        signs = VGroup()
        for a, b in zip(before.tiles, before.tiles[1:]):
            signs.add(equals_sign().move_to([(a.get_right()[0] + b.get_left()[0]) / 2, a.board.get_y(), 0]))
        b_icon = role_icon("sub", 0.72)
        b_word = label("before", 28)
        frozen = bug_tag("frozen", 24)
        head = VGroup(b_icon, b_word, frozen).arrange(RIGHT, buff=0.25)
        head.move_to([0, BIG_HEAD_Y, 0]).align_to([-6.45, 0, 0], LEFT)
        rr = rerender_tag().move_to([0, BIG_HEAD_Y, 0]).align_to([6.45, 0, 0], RIGHT)
        assert head.get_right()[0] + 0.4 < rr.get_left()[0]
        under = before.get_bottom()[1] - 0.3
        b_side = caption("4 frames, 0.2 s apart", 22).move_to([0, under, 0]).align_to(before, RIGHT)
        b_side_small = caption("4 frames,\n0.2 s apart", 22).move_to([SIDE_X, TOP_STRIP_Y, 0])
        zoom_cap = caption("counter, zoomed in", 20).move_to([before.tiles[0].count.get_x(), under, 0])
        zoom_line = Line(zoom_cap.get_top() + UP * 0.05, before.tiles[0].count.get_bottom() + DOWN * 0.05,
                         color=TOOL, stroke_width=2)
        ghost_boxes = [before.tiles[0].board.px_box(x - 48, y - 48, x + 48, y + 48) for x, y in OLD_GHOSTS]

        old = dim_code_panel(OLD_LINE, "tic-tac-toe video · scenes/s03_stop.py at 8a922bf", 280)
        old.move_to([0, OLD_CODE_Y, 0])
        animate_span = code_span(old.code, 0, ".animate")

        spots = VGroup(*[box(0.7, 0.7, TOOL, fill_opacity=0.06, radius=0.08).move_to([x, SPOT_Y, 0])
                         for x in SPOTS_X])
        nums = VGroup(*[caption(str(k + 1), 22).next_to(s, UP, buff=0.1) for k, s in enumerate(spots)])
        rail = DashedLine([START_X, SPOT_Y, 0], [SPOTS_X[-1], SPOT_Y, 0], color=S.GREY_DARK, stroke_width=2,
                          dash_length=0.1)
        start_dot = Dot([START_X, SPOT_Y, 0], radius=0.05, color=S.GREY_DARK)
        ghost = DashedVMobject(Circle(radius=0.27), num_dashes=14, dashed_ratio=0.55).set_stroke(TOOL, 4)
        ghost.move_to([START_X, SPOT_Y, 0])
        note_l = label("next spot:", 26, INK)
        slot_b = box(0.6, 0.56, TOOL, fill=S.BG, fill_opacity=1, radius=0.08)
        note_body = VGroup(note_l, slot_b).arrange(RIGHT, buff=0.18)
        note_box = box(note_body.width + 0.4, note_body.height + 0.24, TOOL, fill=PANEL, fill_opacity=1)
        note_body.move_to(note_box)
        note = VGroup(note_box, note_body).move_to([START_X + 0.55, NOTE_Y, 0])
        pinline = Line(note_box.get_bottom() + LEFT * 0.55, ghost.get_top(), color=TOOL, stroke_width=2)
        dia_cap = caption("one mark, four moves\n(a diagram)", 22).move_to([4.9, SPOT_Y, 0])
        diagram = VGroup(rail, start_dot, spots, nums, pinline, note, ghost, dia_cap)

        fixp = clipped_panel(FIX_LINE, "tic-tac-toe video · scenes/s03_stop.py", 203, cols=64,
                             note=" (part of the line)")
        fixp.move_to([0, FIX_CODE_Y, 0])
        fixp.align_to(old, LEFT)
        doc = caption(f"its docstring: “{DOCSTRING}”", 20).next_to(fixp.caption, DOWN, buff=0.06) \
            .align_to(fixp.caption, LEFT)
        lambda_span = code_span(fixp.code, 0, "lambda")
        for g in fixp.code.code_lines[0]:
            g.set_opacity(g.get_fill_opacity() * 0.55)

        after = frame_strip(NEW_FRAMES, NEW_BOARD, NEW_COUNT).scale(SHRINK).move_to([0, LOW_STRIP_Y, 0])
        a_word = label("after", 28).move_to([0, LOW_HEAD_Y, 0]).align_to(b_word, LEFT)
        a_tag = tag("real frames, after the fix", TOOL).move_to([0, LOW_HEAD_Y, 0]).align_to(rr, RIGHT)
        a_side = caption("4 frames,\n0.2 s apart", 22).move_to([SIDE_X, LOW_STRIP_Y, 0])
        rings = VGroup()
        for k, moved in enumerate(MOVED):
            for c, r in moved:
                p = after.tiles[k].board.px(NEW_COL[c], NEW_ROW[r])
                rings.add(Circle(radius=0.2, color=MEASURED, stroke_width=4).move_to(p))
        lift = TOP_HEAD_Y - BIG_HEAD_Y
        # the before/after screen: nothing may overlap (heights measured, not guessed)
        top_bottom, low_top, low_bottom = (TOP_STRIP_Y - SMALL_H / 2, LOW_STRIP_Y + SMALL_H / 2,
                                           LOW_STRIP_Y - SMALL_H / 2)
        assert TOP_HEAD_Y - 0.25 > TOP_STRIP_Y + SMALL_H / 2 and old.code.get_top()[1] < top_bottom - 0.08
        assert old.caption.get_bottom()[1] > a_tag.get_top()[1] + 0.05 and a_tag.get_bottom()[1] > low_top + 0.08
        assert fixp.code.get_top()[1] < low_bottom - 0.08 and doc.get_bottom()[1] > -3.55
        assert note.get_top()[1] < old.caption.get_bottom()[1] - 0.05
        assert spots.get_bottom()[1] > fixp.code.get_top()[1] + 0.15

        with self.voiceover(SAY[2]) as vo:
            red = grid1[FROZEN_ITEM]
            gone = [r1_kid, r1_head[1], *[s for s in grid1 if s is not red], leg1, fix, a_in, a_out, r2_head,
                    *fixed_sq, *partly_sq, leg2, notes, notes_l, score, src2]
            self.play(FadeOut(collect(self, *gone)), run_time=0.6)
            self.play(ReplacementTransform(r1_dir, b_icon), red.animate.move_to(frozen).scale(0.8),
                      FadeIn(b_word, shift=RIGHT * 0.1), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in before.tiles], lag_ratio=0.12),
                      FadeIn(rr), FadeIn(b_side), run_time=0.9)

            vo.wait_until("The scene should shuffle")
            self.play(FadeIn(zoom_cap), Create(zoom_line), run_time=0.3)
            self.play(LaggedStart(*[Circumscribe(gb, color=S.WHITE, shape=Circle, buff=0.02, run_time=0.8)
                                    for gb in ghost_boxes], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("but the board froze")
            self.play(LaggedStart(*[GrowFromCenter(s) for s in signs], lag_ratio=0.3),
                      ReplacementTransform(red, frozen.box), FadeIn(frozen.text), run_time=0.9)
            vo.wait_until("while the counter")
            self.play(LaggedStart(*[Circumscribe(t.count.frame, color=S.WHITE, buff=0.05, run_time=0.6)
                                    for t in before.tiles], lag_ratio=0.35), run_time=1.6)

            vo.wait_until("The cause is")
            top = collect(self, *before.tiles, signs)
            head_now = collect(self, b_icon, b_word, frozen, rr)
            self.play(top.animate.scale(SHRINK).move_to([0, TOP_STRIP_Y, 0]), head_now.animate.shift(UP * lift),
                      ReplacementTransform(b_side, b_side_small), FadeOut(collect(self, zoom_cap, zoom_line)),
                      run_time=0.9)
            self.play(FadeIn(old, shift=UP * 0.2), run_time=0.6)
            self.play(animate_span.animate.set_color(BUG).set_opacity(1), run_time=0.4)

            vo.wait_until("every move was prepared")
            self.play(FadeIn(diagram, shift=UP * 0.15), run_time=0.6)
            prev = None
            for k in range(4):                                  # all four written before any plays
                c = number_chip(k + 1).move_to(animate_span).scale(0.6)
                self.add(c)
                anims = [c.animate(path_arc=-PI / 5).move_to(slot_b).scale(1 / 0.6)]
                if prev is not None:
                    anims.append(prev.animate.shift(DOWN * 0.45 + RIGHT * 0.35).set_color(BUG).set_opacity(0))
                self.play(*anims, run_time=0.42)
                if prev is not None:
                    self.remove(prev)
                prev = c
            vo.wait_until("so each overwrote")
            self.play(Circumscribe(slot_b, color=S.WHITE, buff=0.06, run_time=0.7))
            self.play(ghost.animate(path_arc=-PI / 3).move_to(spots[3]), run_time=0.7)
            self.play(*[s.animate.set_stroke(BUG) for s in spots[:3]], run_time=0.4)

            vo.wait_until("Now each move")
            self.play(FadeIn(fixp, shift=UP * 0.2), FadeIn(doc, shift=UP * 0.2), FadeOut(prev),
                      ghost.animate.move_to([START_X, SPOT_Y, 0]),
                      *[s.animate.set_stroke(TOOL) for s in spots[:3]], run_time=0.5)
            self.play(lambda_span.animate.set_color(MEASURED).set_opacity(1), run_time=0.25)
            prev = None
            for k in range(4):                                  # each written just as it plays
                c = number_chip(k + 1).move_to(lambda_span).scale(0.6)
                self.add(c)
                anims = [c.animate(path_arc=PI / 5).move_to(slot_b).scale(1 / 0.6)]
                if prev is not None:
                    anims.append(FadeOut(prev, shift=DOWN * 0.2))
                self.play(*anims, run_time=0.26)
                self.play(ghost.animate(path_arc=-PI / 2.5).move_to(spots[k]),
                          spots[k].animate.set_stroke(INK), run_time=0.3)
                prev = c

        # the real frames after the fix
        self.play(FadeOut(collect(self, diagram, prev), shift=DOWN * 0.15), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in after.tiles], lag_ratio=0.12),
                  FadeIn(a_word), FadeIn(a_tag), FadeIn(a_side), run_time=0.8)
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), run_time=0.8)
        self.wait(1.1)

        # ---------------------------------------------------------- beat 4: drift across scenes
        names = ["Dan", "Dan", "Dev", "Dev"]
        cards = VGroup(*[scene_card(n, nm) for n, nm in zip((3, 4, 5, 6), names)]).arrange(RIGHT, buff=0.3)
        cards.move_to([0, 0.8, 0])
        builders = VGroup(*[c.builder.next_to(c.box, UP, buff=0.06).align_to(c.box, RIGHT).shift(LEFT * 0.3)
                            for c in cards])
        name_m = [c.name for c in cards]
        for m in name_m:
            m.set_opacity(0)
        neq = S.math(r"\neq", size=56, color=BUG).move_to(
            [(cards[1].get_right()[0] + cards[2].get_left()[0]) / 2, cards[1].row.get_y(), 0])
        built_l = caption("each scene built by its own agent", 22).next_to(builders, UP, buff=0.18)
        bar_y = -0.95
        bar = RoundedRectangle(width=cards.width, height=0.62, corner_radius=0.2, stroke_color=SUB_AGENT_TEXT,
                               stroke_width=2.5).set_fill(SUB_AGENT, 0.45).move_to([0, bar_y, 0])
        bar_l = label("cross-scene reviewer (whole-video QA pass)", 24, INK).move_to(bar).shift(RIGHT * 0.4)
        rider = role_icon("sub", 0.78)
        rider.move_to([bar.get_left()[0] + 0.45, bar_y + 0.02, 0])
        dans = [label("Dan", 26, INK).move_to(name_m[k]).align_to(name_m[k], LEFT) for k in (2, 3)]
        variants, shared = budget_variants()
        variants.arrange(RIGHT, buff=0.55).move_to([0, -2.2, 0])
        for v in variants:
            v.match_y(variants)
        var_l = label("one budget bar, “drawn five different ways”", 24, TOOL).move_to([0, -2.95, 0])
        shared.move_to([0, -2.2, 0])
        shared_l = VGroup(label("one shared drawing:", 24, TOOL), mono("common.budget_bar()", 22, TOOL)) \
            .arrange(RIGHT, buff=0.18).match_y(var_l)
        src4 = source_caption(A38["src"])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(collect(self, *self.mobjects)), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.15), run_time=1.0)
            vo.wait_until("In the privacy video")
            self.play(FadeIn(src4), run_time=0.4)
            vo.wait_until("agents building")
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in builders], lag_ratio=0.15),
                      FadeIn(built_l), run_time=0.9)
            vo.wait_until("named the same person")
            self.play(*[m.animate.set_opacity(1) for m in name_m[:2]], run_time=0.5)
            self.play(*[Indicate(m, color=S.WHITE) for m in name_m[:2]], run_time=0.6)
            vo.wait_until("and Dev")
            self.play(*[m.animate.set_opacity(1) for m in name_m[2:]], run_time=0.5)
            self.play(FadeIn(neq, scale=0.6), *[Indicate(m, color=S.WHITE) for m in name_m[2:]], run_time=0.6)

            vo.wait_until("Only a reviewer")
            self.play(FadeIn(rider, shift=RIGHT * 0.2), run_time=0.3)
            sweep = 1.8
            end_x = bar.get_right()[0] - 0.45
            t_hit = [(cards[k].get_x() - bar.get_left()[0]) / bar.width * sweep - 0.15 for k in (2, 3)]
            self.play(GrowFromEdge(bar, LEFT, rate_func=linear),
                      rider.animate(rate_func=linear).move_to([end_x, bar_y + 0.02, 0]),
                      Succession(Wait(t_hit[0]), ReplacementTransform(name_m[2], dans[0], run_time=0.3)),
                      Succession(Wait(t_hit[1]), ReplacementTransform(name_m[3], dans[1], run_time=0.3)),
                      Succession(Wait(t_hit[0]), FadeOut(neq, run_time=0.3)),
                      run_time=sweep)
            self.play(FadeIn(bar_l), run_time=0.4)
            vo.wait_until("could catch that")
            self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.15) for v in variants], lag_ratio=0.12),
                      FadeIn(var_l), run_time=0.8)
        self.play(*[ReplacementTransform(v, shared.copy()) for v in variants],
                  ReplacementTransform(var_l, shared_l), run_time=1.0)
        self.wait(1.4)
        fade_out_all(self)
