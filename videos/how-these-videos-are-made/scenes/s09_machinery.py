"""S09 · Bugs in the machinery.

Beats: the answer to S08's ponder. The real fixed frame (A04, the Chinese tic-tac-toe final cut at
11:43, commit 68d6c23) comes back where S08 left its reconstruction; a WHITE box on its subtitle
band, and the band zooms out of the frame into a large strip (the same pixels, cropped) whose 。
pulses WHITE -> the cue splits into two layers: "content: the translation" (the two real Chinese
sentences, 不是。 and 电脑能做的，不只是统计对局。, GREEN ✓) and "tool: the subtitle merger" (a diagram
of the merge: the short cue 不是。 is merged into the next one and its 。 falls out, RED ✗; the
merged text is the old cue as both QA reviewers quoted it), and the real fix commit subject (A35,
cd67aa4) -> that commit card becomes the next one (A35, 5be60d7) at the top; under it a diagram of
three scenes on a time line: the scene code is edited after its movie was made, so the movie is
"older than source" (RED), and a plain build stitches the old movies into the final video anyway
-> the file dates: a faded-BLUE reviewer's note from the privacy video's newcomer review (A44) and
the BLUE agent's own date pair (A44: Explore.mp4 · Oct 5, 23:24 vs s06_explore.py · committed Oct 6,
00:05), into which the diagram's second row turns -> the commit card's text becomes the commit's
next sentence (the fix, real), the RED tag becomes a GREEN date check, and the real voice stamp of a
Chinese scene render (A31) with a GREEN tag -> the Chinese privacy video's QA in three lanes (A32):
reviewers (4 groups × director + simulated grad student) with 103 findings, coloured by kind as in
S07 (1 wrong, 21 confusing, 81 polish) -> 4 fixers with 75 changes -> 4 skeptical verifiers with
12 corrections; one change leaves the fixers' lane as a card ("claimed: ×1.12, within the limit"),
reaches the verifiers' lane and bounces back with the RED measured value ("measured: ×1.153, over
the 15 % limit").

Squares are one per finding / change / correction (DATA: counts from the run record); which
findings led to which changes is not on record, so none is mapped to another.

Every number and quote on screen is checked in _check() (runs on import) against the assets.

Helpers defined here (not in common.py): collect() and glyphs_of() (as in s08), movie_icon(),
cue_box(), commit_card(), dated_file(), qa_square(), square_grid(), lane_icons().
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.scene import VoiceScene

from common import (AGENT, BUG, EXCERPTS, INK, MEASURED, NARRATION, PANEL, PROJECT, SUB_AGENT, SUB_AGENT_TEXT,
                    TOOL, ai_badge, asset, asset_text, box, bug_tag, caption, check_mark, code_block, cross_mark,
                    emphasize, exhibit, fade_out_all, file_icon, label, measured_badge, mono, pen, role_icon,
                    source_caption, speech_bubble, tag, zh)

SAY = NARRATION["S09"]

# ------------------------------------------------------------------ the real material (assets/)
A30, A31, A32, A35, A44 = EXCERPTS["A30"], EXCERPTS["A31"], EXCERPTS["A32"], EXCERPTS["A35"], EXCERPTS["A44"]
FRAME_PNG = "ttt_zh_1143.png"                       # A04: 1920 x 1080, commit 68d6c23, at 703.0 s
CUE_FIXED, CUE_OLD = A30["after"], A30["before"]    # 不是。电脑能做的，不只是统计对局 / without the 。
NO = CUE_FIXED[:3]                                  # 不是。  (the translation's own sentence)
REST = CUE_FIXED[3:]                                # 电脑能做的，不只是统计对局 (the cue drops the final 。)
TRANSLATION = [NO, REST + "。"]                     # the two Chinese sentences (tic-tac-toe g3.yaml, S09)
FIX_SUBJECT = A35["cd67aa4"].split("; ")[0] + "; …"   # "Subtitles: keep sentence punctuation in merged cues; …"
STALE_MSG = A35["5be60d7"]
FIX_MSG = A35["5be60d7_next"]
REVIEWER_NOTE = A44["reviewer"]                     # "The renders are older than the source."
MOVIE_NAME, MOVIE_DATE = A44["agent_pair"]["movie"].split(" · ")
CODE_NAME, CODE_DATE = A44["agent_pair"]["source"].split(" · ")
STAMP = asset_text(A31["file"])                     # {"speed": 1.0, "tts": "edge", "voice": "zh-CN-XiaoyiNeural"}
FIND, FIXES, CORR = A32["findings"], A32["fixer_changes"]["total"], A32["verifier_corrections"]["total"]
CLAIMED, MEASURED_NOTE = A32["bounce"].split(" · ")

FRAME_CAP = "real frame · Chinese tic-tac-toe final cut · 11:43"
ZOOM_CAP = FRAME_CAP + " · its subtitle band, zoomed in"
TR_CAP = "real translation · tic-tac-toe video, i18n/zh/narration/g3.yaml"
MERGE_CAP = "diagram · the old cue text, as both AI reviewers quoted it"
FIX_CAP = "the fix · real commit subject (cd67aa4, Oct 6)"
STALE_CAP = "real commit message (5be60d7, Oct 6)"
STAMP_CAP = A31["caption"]                          # "voice stamp of a Chinese scene render (tic-tac-toe scene 3)"
QA_SRC = "data · Chinese privacy video's reviews"


def _check():
    assert CUE_FIXED == "不是。电脑能做的，不只是统计对局" and CUE_OLD == NO[:2] + REST
    assert A30["english"] == "No. A computer can do more than count."
    tr = PROJECT.parent / "tictactoe-255168" / "i18n" / "zh" / "narration" / "g3.yaml"
    if tr.exists():                                 # the translation itself, when the repo has it
        assert all(f'- "{s}"' in tr.read_text(encoding="utf-8") for s in TRANSLATION), TRANSLATION
    assert A35["cd67aa4"] == "Subtitles: keep sentence punctuation in merged cues; clause-aligned English; 2-line cues"
    assert FIX_SUBJECT == "Subtitles: keep sentence punctuation in merged cues; …"
    assert STALE_MSG == ("A plain build used to reuse any existing scene movie, so edited scenes were silently "
                         "stitched from stale renders.")
    assert FIX_MSG.startswith("Now a scene is rendered when its movie is missing or older than its file")
    assert REVIEWER_NOTE == "The renders are older than the source."
    assert A44["reviewer_caption"] == "a reviewer · privacy video, Oct 4"
    assert A44["agent_caption"] == "the agent · tic-tac-toe, Oct 6"
    assert (MOVIE_NAME, MOVIE_DATE, CODE_NAME, CODE_DATE) == ("Explore.mp4", "Oct 5, 23:24", "s06_explore.py",
                                                              "committed Oct 6, 00:05")
    assert STAMP == A31["text"] == '{"speed": 1.0, "tts": "edge", "voice": "zh-CN-XiaoyiNeural"}'
    assert STAMP_CAP == "voice stamp of a Chinese scene render (tic-tac-toe scene 3)"
    assert (FIND["total"], FIND["wrong"], FIND["confusing"], FIND["polish"]) == (103, 1, 21, 81)
    assert FIND["wrong"] + FIND["confusing"] + FIND["polish"] == FIND["total"]
    assert A32["groups"] == 4 and FIXES == 75 == sum(A32["fixer_changes"]["by_group"])
    assert CORR == 12 == sum(A32["verifier_corrections"]["by_group"])
    assert CLAIMED == "claimed: ×1.12, within the limit"
    assert MEASURED_NOTE == "measured: ×1.153, over the 15 % limit"
    assert "x1.12" in A32["bounce_src"] and "x1.153" in A32["bounce_src"]
    asset(FRAME_PNG)


_check()

# ------------------------------------------------------------------ layout
# S08 left its reconstructed frame here: the A04 picture, FRAME_W wide, left edge FRAME_X0, top
# FRAME_TOP. The real frame comes back at the same place, now with its own (real) subtitle band.
FRAME_CROP = (120, 20, 1800, 1080)
FRAME_W, FRAME_X0, FRAME_TOP = 7.6, -6.35, 2.75
BAND_PX = (645, 978, 1273, 1074)       # the subtitle band (both lines), the zoom's crop
ZH_PX = (680, 988, 1238, 1028)         # the Chinese line
DOT_PX = (754, 1013, 764, 1022)        # its 。
ZOOM_W, ZOOM_Y = 9.4, 2.66
ROW_W = 12.8                           # the two layers
CONTENT_Y, TOOL_Y = 0.8, -0.92
CUE_X0 = -2.75                        # where the cue text starts in both layers
CJK = 28
COMMIT1_Y = -2.62
MARK_X = 5.75                          # the ✓ / ✗

COMMIT2_Y = 2.8
LEGEND_Y = 1.5
ROWS_Y = (0.68, -0.32, -1.32)
AXIS_Y, AXIS_X = -2.12, (-4.85, 1.95)
CODE_X0, MOVIE_X, CODE_X1 = -4.05, -2.45, 1.1
SLOTS_X, SLOT_W, SLOT_H = 4.6, 1.02, 0.64
HOP_ARC = 4 * np.arctan(0.55 / ((CODE_X1 - CODE_X0) / 2))   # path_arc whose sagitta is 0.55 (rows are 1.0 apart)
REV_Y, AGENT_Y = 1.0, -0.88
ICON_X = -5.55

COL_X = (-4.35, 0.0, 4.35)
TITLE_Y, ICONS_Y, SUB_Y = 3.1, 2.45, 1.72
GRID_BOTTOM, COUNT_Y, BREAK_Y = -1.0, -1.38, -1.76
SQ, SQ_BUFF, SQ_COLS = 0.22, 0.07, 13
CARD_Y, CARD_X, WALL_X = -2.72, 1.6, 5.85


# ------------------------------------------------------------------ helpers (this scene only)
def collect(scene, *mobs) -> Group:
    """Make several on-screen things ONE top-level group (each thing's whole family leaves the top
    level first, so no part that came on screen by itself stays behind)."""
    for m in mobs:
        scene.remove(*m.get_family())
    g = Group(*mobs)
    scene.add(g)
    return g


def glyphs_of(t: Text, s: str, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of substring `sub` in a Text built from string s (whitespace has no glyphs)."""
    flat, want = "".join(s.split()), "".join(sub.split())
    assert len(t.submobjects) == len(flat), (len(t.submobjects), len(flat), s)
    start = -1
    for _ in range(occurrence + 1):
        start = flat.find(want, start + 1)
    assert start >= 0, (sub, s)
    return VGroup(*t[start:start + len(want)])


def movie_icon(height: float = 0.5, color: str = TOOL) -> VGroup:
    """A scene movie (a file, so GREY): a film frame with sprocket holes and a play triangle."""
    w, h = height * 1.3, height
    frame = RoundedRectangle(width=w, height=h, corner_radius=h * 0.12, stroke_color=color,
                             stroke_width=2.5).set_fill(PANEL, 1)
    holes = VGroup()
    for y in (h / 2 - h * 0.13, -h / 2 + h * 0.13):
        for k in range(5):
            holes.add(Square(h * 0.1, stroke_width=0).set_fill(color, 0.9)
                      .move_to([-w / 2 + w * (k + 0.5) / 5, y, 0]))
    tri = Triangle(stroke_width=0).set_fill(color, 1).rotate(-PI / 2).scale_to_fit_height(h * 0.36)
    tri.move_to(ORIGIN).shift(RIGHT * h * 0.03)
    return VGroup(frame, holes, tri)


def cue_box(s: str, size: float = CJK, fill: str = "#050608", color: str = S.GREY_DARK) -> VGroup:
    """A subtitle cue (or a sentence card): Chinese text on a dark box. .box .text"""
    t = zh(s, size, INK)
    b = box(t.width + 0.4, max(t.height, 0.36) + 0.3, color, fill=fill, fill_opacity=1, radius=0.08, stroke=2)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text, g.string = b, t, s
    return g


def commit_card(lines: list[str], size: float = 24, width: float | None = None) -> VGroup:
    """A real commit message on a GREY card (its hash and date go in a caption). .box .text"""
    t = VGroup(*[label(s, size, INK) for s in lines]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    b = box(width or t.width + 0.6, t.height + 0.36, TOOL, fill=PANEL, fill_opacity=1, radius=0.12)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def dated_file(icon, name: str, date: str, slot: float = 0.6) -> VGroup:
    """'[icon] Explore.mp4 · Oct 5, 23:24': the file name in monospace, its date in the house font.
    The icon is centred in a fixed slot, so the names of stacked rows start in one column."""
    n = mono(name, 24, INK)
    d = label("· " + date, 24, INK)
    d.next_to(n, RIGHT, buff=0.18)
    d.shift(UP * (n[0].get_bottom()[1] - d[1].get_bottom()[1]))      # same baseline
    icon.move_to(n.get_left() + LEFT * (0.16 + slot / 2)).match_y(n)
    row = VGroup(icon, n, d)
    row.icon, row.name, row.date = icon, n, d
    return row


def qa_square(kind: str, side: float = SQ) -> VMobject:
    """One QA item, coloured as in S07: a wrong finding RED, a confusing one RED outline, polish GREY;
    a fixer's change GREY (lighter); a verifier's correction GREEN (a measured check)."""
    col, op = {"wrong": (BUG, 0.85), "confusing": (BUG, 0.16), "polish": (TOOL, 0.12),
               "change": (TOOL, 0.45), "correction": (MEASURED, 0.85)}[kind]
    return box(side, side, col, fill_opacity=op, stroke=2, radius=0.04)


def square_grid(kinds: list[str], x: float, bottom: float) -> VGroup:
    """Squares in rows of SQ_COLS, filled from the bottom row up (so the lanes read as columns of a
    chart); the first square is bottom-left."""
    step = SQ + SQ_BUFF
    width = SQ_COLS * step - SQ_BUFF
    g = VGroup()
    for i, k in enumerate(kinds):
        r, c = divmod(i, SQ_COLS)
        g.add(qa_square(k).move_to([x - width / 2 + SQ / 2 + c * step, bottom + SQ / 2 + r * step, 0]))
    return g


def lane_icons(groups: int, per_group: int, height: float = 0.4) -> VGroup:
    """Faded-BLUE sub-agent icons in groups (one AI badge for the lane)."""
    gs = VGroup(*[VGroup(*[person_icon(SUB_AGENT, height) for _ in range(per_group)]).arrange(RIGHT, buff=0.05)
                  for _ in range(groups)]).arrange(RIGHT, buff=0.22)
    b = ai_badge(0.4, SUB_AGENT_TEXT).next_to(gs, RIGHT, buff=0.08).align_to(gs, DOWN).shift(DOWN * 0.04)
    g = VGroup(gs, b)
    g.people, g.badge = gs, b
    return g


class Machinery(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- beat 1: a tool bug, not a translation bug
        pic = exhibit(FRAME_PNG, width=FRAME_W, crop=FRAME_CROP)
        pic.move_to([FRAME_X0 + FRAME_W / 2, FRAME_TOP - pic.height / 2, 0])
        pic_cap = caption(FRAME_CAP, 22).next_to(pic, DOWN, buff=0.16).align_to(pic, LEFT)
        band_on_pic = pic.px_box(*BAND_PX)
        zh_on_pic = pic.px_box(*ZH_PX)
        look = SurroundingRectangle(zh_on_pic, color=S.WHITE, buff=0.05, stroke_width=3, corner_radius=0.04)

        zoom = exhibit(FRAME_PNG, width=ZOOM_W, crop=BAND_PX).move_to([0, ZOOM_Y, 0])
        zoom_cap = caption(ZOOM_CAP, 20).next_to(zoom, DOWN, buff=0.12).align_to(zoom, RIGHT)
        dot = zoom.px_box(*DOT_PX)
        start_scale = band_on_pic.width / zoom.width

        # the two layers
        def layer(y: float, h: float, name: str) -> VGroup:
            b = box(ROW_W, h, TOOL, fill=PANEL, fill_opacity=0.55, radius=0.14, stroke=2).move_to([0, y, 0])
            t = label(name.replace(": ", ":\n"), 26, INK, line_spacing=0.85).move_to(b).align_to(b, LEFT)
            t.shift(RIGHT * 0.3)
            g = VGroup(b, t)
            g.box, g.name = b, t
            return g

        content = layer(CONTENT_Y, 0.98, "content: the translation")
        tool = layer(TOOL_Y, 1.22, "tool: the subtitle merger")
        sent = VGroup(cue_box(TRANSLATION[0], fill=PANEL, color=TOOL), cue_box(TRANSLATION[1], fill=PANEL, color=TOOL))
        sent.arrange(RIGHT, buff=0.22).move_to([0, CONTENT_Y, 0]).align_to([CUE_X0, 0, 0], LEFT)
        tr_cap = caption(TR_CAP, 20).next_to(content.box, DOWN, buff=0.08).align_to(content.box, RIGHT)
        ok = check_mark(0.46).move_to([MARK_X, CONTENT_Y, 0])
        dot_tr = glyphs_of(sent[0].text, NO, "。")

        cues = VGroup(cue_box(NO), cue_box(REST)).arrange(RIGHT, buff=0.22)
        cues.move_to([0, TOOL_Y + 0.12, 0]).align_to([CUE_X0, 0, 0], LEFT)
        merged = cue_box(CUE_OLD).move_to(cues).align_to(cues, LEFT)
        dot_cue = glyphs_of(cues[0].text, NO, "。")
        bad = cross_mark(0.46).move_to([MARK_X, TOOL_Y, 0])
        merge_cap = caption(MERGE_CAP, 20).next_to(tool.box, DOWN, buff=0.08).align_to(tool.box, RIGHT)
        fix1 = commit_card([FIX_SUBJECT]).move_to([0, COMMIT1_Y, 0])
        fix1_cap = caption(FIX_CAP, 20).next_to(fix1, DOWN, buff=0.1).align_to(fix1, RIGHT)
        assert sent.get_right()[0] < ok.get_left()[0] - 0.3 and cues.get_right()[0] < bad.get_left()[0] - 0.3
        assert content.name.get_right()[0] < CUE_X0 - 0.2 and tool.name.get_right()[0] < CUE_X0 - 0.2
        assert zoom_cap.get_bottom()[1] > content.box.get_top()[1] + 0.08
        assert tr_cap.get_bottom()[1] > tool.box.get_top()[1] + 0.04
        assert merge_cap.get_bottom()[1] > fix1.get_top()[1] + 0.06 and fix1_cap.get_bottom()[1] > -3.55

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(pic), FadeIn(pic_cap, shift=UP * 0.1), run_time=0.7)
            self.play(Create(look), run_time=0.45)
            vo.wait_until("The translation had")
            zoom.scale(start_scale).move_to(band_on_pic)
            self.add(zoom)
            self.play(zoom.animate.scale(1 / start_scale).move_to([0, ZOOM_Y, 0]), FadeOut(pic), FadeOut(look),
                      FadeTransform(pic_cap, zoom_cap), run_time=1.0)
            self.play(TransformFromCopy(zoom.frame, content.box), FadeIn(content.name, shift=DOWN * 0.15),
                      LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in sent], lag_ratio=0.3),
                      FadeIn(tr_cap), run_time=0.9)
            vo.wait_until("after that no")
            self.play(Circumscribe(dot, Circle, color=S.WHITE, buff=0.12, run_time=0.9),
                      Flash(dot.get_center(), color=S.WHITE, line_length=0.14, flash_radius=0.3, run_time=0.9),
                      Indicate(dot_tr, color=S.WHITE, scale_factor=1.8, run_time=0.9))
            self.play(Create(ok), run_time=0.4)

            vo.wait_until("but the subtitle tool")
            self.play(TransformFromCopy(content.box, tool.box), FadeIn(tool.name, shift=DOWN * 0.15),
                      LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cues], lag_ratio=0.3), run_time=0.8)
            vo.wait_until("dropped it")
            self.play(dot_cue.animate.set_color(BUG).scale(1.5), run_time=0.45)
            vo.wait_until("when it merged")
            # the short cue is merged into the next one; its 。 falls out
            keep_no = glyphs_of(cues[0].text, NO, NO[:2])
            self.remove(dot_cue)
            fall = dot_cue.copy()
            self.add(fall)
            box_b = cues[1].box
            self.play(ReplacementTransform(cues[0].box, merged.box),
                      box_b.animate.become(merged.box.copy().set_opacity(0)),
                      ReplacementTransform(keep_no, glyphs_of(merged.text, CUE_OLD, NO[:2])),
                      ReplacementTransform(cues[1].text, glyphs_of(merged.text, CUE_OLD, REST)),
                      fall.animate.shift(DOWN * 0.62 + RIGHT * 0.15).rotate(-PI / 3).set_opacity(0),
                      run_time=1.1)
            self.remove(box_b, fall)
            self.play(Create(bad), FadeIn(merge_cap), run_time=0.45)
            vo.wait_until("into the next")
            self.play(FadeIn(fix1, shift=UP * 0.15), FadeIn(fix1_cap), run_time=0.6)
            vo.wait_until("Tool bugs")
            self.play(emphasize(tool.name), Indicate(bad, color=S.WHITE, scale_factor=1.25), run_time=0.8)
            vo.wait_until("look like content")
            self.play(emphasize(content.name), Circumscribe(zoom.frame, color=S.WHITE, buff=0.06, time_width=0.5),
                      run_time=1.0)

        # ---------------------------------------------------------- beat 2: stale scene movies
        msg1 = commit_card(["A plain build used to reuse any existing scene movie, so edited",
                            "scenes were silently stitched from stale renders."])
        msg2 = commit_card(["Now a scene is rendered when its movie is missing or older than its file,",
                            "the shared scene helpers, script.md, video.yaml, assets or the toolkit."])
        assert " ".join(t.original_text for t in msg1.text) == STALE_MSG
        assert " ".join(t.original_text for t in msg2.text) == FIX_MSG
        wide = max(msg1.box.width, msg2.box.width)
        msg1 = commit_card([t.original_text for t in msg1.text], width=wide).move_to([0, COMMIT2_Y, 0])
        msg2 = commit_card([t.original_text for t in msg2.text], width=wide).move_to([0, COMMIT2_Y, 0])
        msg1.text.align_to(msg1.box, LEFT).shift(RIGHT * 0.3)
        msg2.text.align_to(msg2.box, LEFT).shift(RIGHT * 0.3)
        msg_cap = caption(STALE_CAP, 20).next_to(msg1, DOWN, buff=0.1).align_to(msg1, RIGHT)
        assert msg1.box.width < 13.0

        # the diagram: three scenes on a time line
        legend = VGroup(file_icon(0.42), label("scene code", 22, TOOL), movie_icon(0.36),
                        label("scene movie", 22, TOOL)).arrange(RIGHT, buff=0.16)
        legend[2].shift(RIGHT * 0.3)
        legend[3].shift(RIGHT * 0.3)
        legend.move_to([0, LEGEND_Y, 0]).align_to([-6.2, 0, 0], LEFT)
        names = VGroup(*[label(f"scene {k + 1}", 24, TOOL).move_to([-5.75, y, 0]) for k, y in enumerate(ROWS_Y)])
        codes = VGroup(*[file_icon(0.5).move_to([CODE_X0, y, 0]) for y in ROWS_Y])
        movies = VGroup(*[movie_icon(0.48).move_to([MOVIE_X, y, 0]) for y in ROWS_Y])
        axis = Arrow([AXIS_X[0], AXIS_Y, 0], [AXIS_X[1], AXIS_Y, 0], buff=0, color=TOOL, stroke_width=3,
                     tip_length=0.18, max_tip_length_to_length_ratio=0.05)
        early = caption("earlier", 22).next_to(axis.get_start(), DOWN, buff=0.12).align_to(axis, LEFT)
        late = caption("later", 22).next_to(axis.get_end(), DOWN, buff=0.12).align_to(axis, RIGHT)
        pens = VGroup(*[pen(0.5).next_to(codes[k], UR, buff=-0.08) for k in (1, 2)])
        stale = VGroup(*[bug_tag("older than source").next_to(movies[k], RIGHT, buff=0.18) for k in (1, 2)])
        assert all(t.get_right()[0] < CODE_X1 - 0.35 for t in stale)

        slots = VGroup(*[RoundedRectangle(width=SLOT_W, height=SLOT_H, corner_radius=0.06, stroke_color=TOOL,
                                          stroke_width=2).set_fill(PANEL, 1) for _ in range(3)])
        slots.arrange(RIGHT, buff=0.08).move_to([SLOTS_X, ROWS_Y[1], 0])
        slots_l = label("final video", 24, INK).next_to(slots, UP, buff=0.18)
        plain = caption("plain build", 22).next_to(slots, DOWN, buff=0.18)
        segs = VGroup()
        for k, s in enumerate(slots):
            seg = VGroup(s.copy().set_stroke(BUG if k else TOOL, 3), movie_icon(0.4).move_to(s))
            if k:
                seg[0].set_fill(BUG, 0.14)
            segs.add(seg)
        assert slots.get_right()[0] < 6.45 and slots.get_left()[0] > CODE_X1 + 0.6

        # the file dates (A44): a reviewer's note and the agent's own date check
        reviewer = role_icon("sub", 0.95).move_to([ICON_X, REV_Y, 0])
        note = speech_bubble(REVIEWER_NOTE, chars=60, tail=LEFT)
        note.next_to(reviewer, RIGHT, buff=0.15).shift(UP * 0.12)
        note_cap = caption(A44["reviewer_caption"], 20).next_to(note.box, DOWN, buff=0.1).align_to(note.box, LEFT)
        agent = role_icon("agent", 0.95).move_to([ICON_X, AGENT_Y, 0])
        movie_row = dated_file(movie_icon(0.4), MOVIE_NAME, MOVIE_DATE)
        code_row = dated_file(file_icon(0.42), CODE_NAME, CODE_DATE)
        pair = VGroup(movie_row, code_row).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        pair.next_to(agent, RIGHT, buff=0.35).match_y(agent)
        older = bug_tag("older than source").next_to(movie_row, RIGHT, buff=0.3)
        pair_cap = caption(A44["agent_caption"], 20).next_to(pair, DOWN, buff=0.14).align_to(pair, LEFT)
        assert older.get_right()[0] < 6.45 and code_row.get_right()[0] < 6.45
        assert note_cap.get_bottom()[1] > agent.get_top()[1] + 0.25
        assert reviewer.get_top()[1] < msg_cap.get_bottom()[1] - 0.15

        # the fix: a date check, and the voice stamp
        lift = (REV_Y - AGENT_Y) * UP
        fresh = measured_badge("older than its sources → render again", 22)
        stamp = code_block(STAMP, 24, language="json").move_to([0, -1.25, 0])
        stamp_cap = caption(STAMP_CAP, 20).next_to(stamp, DOWN, buff=0.12).align_to(stamp, LEFT)
        voice_tag = measured_badge("every render now records its voice", 22)
        voice_tag.next_to(stamp, UP, buff=0.14).align_to(stamp, RIGHT)
        assert stamp.width < 12.8 and stamp_cap.get_bottom()[1] > -3.55

        # pad: the voice stamp and its tag come in on "or its voice", 1.5 s before the clip ends;
        # hold them long enough to read before the next beat clears the stage
        with self.voiceover(SAY[1], pad=1.3) as vo:
            gone = collect(self, zoom, zoom_cap, content, sent, tr_cap, ok, tool.box, merged, bad, merge_cap)
            self.play(FadeOut(gone), FadeOut(tool.name, shift=UP * 0.2),
                      ReplacementTransform(fix1.box, msg1.box), FadeTransform(fix1.text, msg1.text),
                      FadeTransform(fix1_cap, msg_cap), run_time=1.0)
            vo.wait_until("a plain build")
            self.play(FadeIn(legend), FadeIn(names), GrowArrow(axis), FadeIn(early), FadeIn(late),
                      LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in codes], lag_ratio=0.15), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in movies], lag_ratio=0.15), run_time=0.7)
            vo.wait_until("reuse old")
            self.play(FadeIn(slots), FadeIn(slots_l), FadeIn(plain), run_time=0.5)
            self.play(LaggedStart(*[Indicate(m, color=S.WHITE, scale_factor=1.15) for m in movies], lag_ratio=0.2),
                      run_time=0.8)

            vo.wait_until("so edited scenes")
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in pens], lag_ratio=0.25), run_time=0.4)
            # a low hop (peak ~0.55 above its row): it clears the movie icon but never reaches the row
            # above, so it can't read as scene 1 (or 2) being edited mid-flight
            hop = -HOP_ARC
            for k in (1, 2):
                self.bring_to_front(codes[k])
            self.bring_to_front(*pens)
            self.play(*[codes[k].animate(path_arc=hop).shift(RIGHT * (CODE_X1 - CODE_X0)) for k in (1, 2)],
                      *[p.animate(path_arc=hop).shift(RIGHT * (CODE_X1 - CODE_X0)) for p in pens], run_time=0.9)
            self.play(FadeOut(collect(self, *pens)), LaggedStart(*[FadeIn(t, scale=0.8) for t in stale], lag_ratio=0.25),
                      run_time=0.55)
            vo.wait_until("quietly stitched")
            flying = VGroup(*[m.copy() for m in movies])
            self.add(flying)
            self.play(LaggedStart(*[ReplacementTransform(f, s) for f, s in zip(flying, segs)], lag_ratio=0.2),
                      run_time=1.1)
            vo.wait_until("out-of-date footage")
            self.play(*[Indicate(segs[k], color=BUG, scale_factor=1.1) for k in (1, 2)], run_time=0.7)

            # the file dates gave it away
            vo.wait_until("The file dates")
            gone2 = collect(self, legend, names, codes[0], codes[2], movies[0], movies[2], stale[1], axis, early, late,
                            slots, slots_l, plain, segs)
            self.play(FadeOut(gone2), FadeIn(reviewer, shift=RIGHT * 0.3), run_time=0.7)
            self.play(FadeIn(note, shift=UP * 0.12), FadeIn(note_cap), run_time=0.5)
            vo.wait_until("gave it away")
            self.play(ReplacementTransform(movies[1], movie_row.icon), ReplacementTransform(codes[1], code_row.icon),
                      ReplacementTransform(stale[0], older), FadeIn(agent, shift=RIGHT * 0.3), run_time=0.9)
            self.play(FadeIn(VGroup(movie_row.name, movie_row.date, code_row.name, code_row.date), shift=LEFT * 0.15),
                      FadeIn(pair_cap), run_time=0.6)
            vo.wait_until("the movies were older")
            # one box per date: a single box round both would sweep across the RED tag
            self.play(Indicate(note.text, color=S.WHITE, scale_factor=1.06),
                      *[Circumscribe(d, color=S.WHITE, buff=0.07) for d in (movie_row.date, code_row.date)],
                      run_time=1.0)

            # the fix
            vo.wait_until("Now a scene")
            agent_side = collect(self, agent, pair, older, pair_cap)
            self.play(FadeOut(collect(self, reviewer, note, note_cap), shift=UP * 0.2),
                      agent_side.animate.shift(lift), FadeTransform(msg1.text, msg2.text), run_time=1.0)
            fresh.next_to(movie_row, RIGHT, buff=0.25)
            assert fresh.get_right()[0] < 6.45, fresh.get_right()
            vo.wait_until("whenever it's older")
            self.play(ReplacementTransform(older, fresh), run_time=0.8)
            self.play(Circumscribe(msg2.text, color=S.WHITE, buff=0.08, time_width=0.4), run_time=1.1)
            vo.wait_until("or its voice")
            self.play(LaggedStart(AnimationGroup(FadeIn(stamp, shift=UP * 0.2), FadeIn(stamp_cap)),
                                  FadeIn(voice_tag, scale=0.9), lag_ratio=0.45), run_time=0.95)

        # ---------------------------------------------------------- beat 3: the fixes get checked too
        titles = VGroup(label("reviewers", 28, SUB_AGENT_TEXT), label(f"{A32['groups']} fixers", 28, SUB_AGENT_TEXT),
                        label(f"{A32['groups']} skeptical verifiers", 28, SUB_AGENT_TEXT))
        for t, x in zip(titles, COL_X):                    # one baseline (the first glyphs sit on it)
            t.move_to([x, TITLE_Y, 0])
            t.shift(UP * (TITLE_Y - 0.12 - t[0].get_bottom()[1]))
        flow = VGroup(*[Arrow(a.get_right() + RIGHT * 0.2, b.get_left() + LEFT * 0.2, buff=0, color=TOOL, stroke_width=3,
                              tip_length=0.16, max_tip_length_to_length_ratio=0.12)
                        for a, b in zip(titles, titles[1:])])
        crews = VGroup(lane_icons(A32["groups"], 2), lane_icons(A32["groups"], 1), lane_icons(A32["groups"], 1))
        for c, x in zip(crews, COL_X):
            c.move_to([x, ICONS_Y, 0])
        sub = label(f"{A32['groups']} groups × (director +\nsimulated grad student)", 22, SUB_AGENT_TEXT,
                    line_spacing=0.9)
        sub.move_to([COL_X[0], SUB_Y, 0])
        kinds = ["wrong"] * FIND["wrong"] + ["confusing"] * FIND["confusing"] + ["polish"] * FIND["polish"]
        g_find = square_grid(kinds, COL_X[0], GRID_BOTTOM)
        g_fix = square_grid(["change"] * FIXES, COL_X[1], GRID_BOTTOM)
        g_cor = square_grid(["correction"] * CORR, COL_X[2], GRID_BOTTOM)
        polish = VGroup(*g_find[FIND["wrong"] + FIND["confusing"]:])
        c_find = label(f"{FIND['total']} findings:", 26, INK).move_to([COL_X[0], COUNT_Y, 0])
        brk = VGroup(label(f"{FIND['wrong']} wrong", 22, BUG), label("·", 22, TOOL),
                     label(f"{FIND['confusing']} confusing", 22, BUG), label("·", 22, TOOL),
                     label(f"{FIND['polish']} polish", 22, TOOL)).arrange(RIGHT, buff=0.12)   # as S07: polish GREY
        brk.move_to([COL_X[0], BREAK_Y, 0])
        c_fix = label(f"{FIXES} changes", 26, INK).move_to([COL_X[1], COUNT_Y, 0])
        c_cor = label(f"{CORR} corrections", 26, INK).move_to([COL_X[2], COUNT_Y, 0])
        for c in (c_find, c_cor):                          # one baseline with "75 changes" (digits sit on it)
            c.shift(UP * (c_fix[0].get_bottom()[1] - c[0].get_bottom()[1]))
        qa_src = source_caption(QA_SRC)
        assert g_find.get_top()[1] < sub.get_bottom()[1] - 0.08 and sub.get_top()[1] < crews[0].get_bottom()[1] - 0.08
        assert crews[0].get_left()[0] > -6.5 and crews[0].get_right()[0] < flow[0].get_end()[0] + 2.0
        assert g_find.get_right()[0] < g_fix.get_left()[0] - 0.4 and g_fix.get_right()[0] < g_cor.get_left()[0] - 0.4

        # the change card that bounces back
        head = caption("one passage · Chinese narration time ÷ English", 20)
        claim = label(CLAIMED, 24, INK)
        meas = label(MEASURED_NOTE, 24, BUG)
        body = VGroup(head, claim, meas).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        big_b = box(body.width + 0.5, body.height + 0.34, TOOL, fill=PANEL, fill_opacity=1, radius=0.12)
        body.move_to(big_b)
        VGroup(big_b, body).move_to([CARD_X, CARD_Y, 0])
        two = VGroup(head, claim)
        card_b = box(big_b.width, two.height + 0.34, TOOL, fill=PANEL, fill_opacity=1, radius=0.12)
        card_b.align_to(big_b, UP).match_x(big_b)
        card = VGroup(card_b, head, claim)                  # the card before it is checked (two lines)
        src_sq = g_fix[FIXES - 1]                           # one change, top right of the fixers' squares
        wall = Line(UP * 0.48, DOWN * 0.48, color=MEASURED, stroke_width=6)
        wall.move_to([WALL_X, card_b.get_y() - 0.08, 0])
        gate = VGroup(wall, check_mark(0.34).next_to(wall, UP, buff=0.08))
        dx = wall.get_x() - card_b.get_right()[0] - 0.05
        assert big_b.get_bottom()[1] > -3.55 and big_b.get_top()[1] < c_fix.get_bottom()[1] - 0.25
        assert big_b.get_left()[0] > brk.get_right()[0] + 0.2
        assert qa_src.get_right()[0] < big_b.get_left()[0] - 0.15 or qa_src.get_top()[1] < big_b.get_bottom()[1] - 0.05
        assert card_b.get_right()[0] + dx < 6.5 and dx > 0.4
        assert gate.get_top()[1] < c_cor.get_bottom()[1] - 0.15, (gate.get_top(), c_cor.get_bottom())

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(collect(self, *self.mobjects)), run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(t, shift=DOWN * 0.15), FadeIn(c, shift=DOWN * 0.15))
                                    for t, c in zip(titles, crews)], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a) for a in flow], lag_ratio=0.5), run_time=1.1)
            vo.wait_until("For the Chinese")
            self.play(FadeIn(qa_src), FadeIn(sub, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("video, reviewers")
            self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in g_find], lag_ratio=0.02),
                      Indicate(crews[0].people, color=S.WHITE, scale_factor=1.06), run_time=1.4)
            self.play(FadeIn(c_find, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("points, most")
            self.play(FadeIn(brk, shift=UP * 0.1), run_time=0.5)
            self.play(polish.animate.set_fill(INK, 0.5), Indicate(brk[4], color=S.WHITE, scale_factor=1.15), run_time=0.6)
            self.play(polish.animate.set_fill(TOOL, 0.12), run_time=0.4)
            vo.wait_until("polish, and fixers")
            self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in g_fix], lag_ratio=0.02),
                      Indicate(crews[1].people, color=S.WHITE, scale_factor=1.08), run_time=1.2)
            self.play(FadeIn(c_fix, shift=UP * 0.1), run_time=0.4)

            vo.wait_until("Then skeptical")
            scan = Line(UP * (g_fix.height / 2 + 0.15), DOWN * (g_fix.height / 2 + 0.15), color=MEASURED,
                        stroke_width=5).move_to([g_fix.get_right()[0] + 0.12, g_fix.get_y(), 0])
            self.play(Indicate(crews[2].people, color=S.WHITE, scale_factor=1.08), FadeIn(scan), run_time=0.6)
            self.play(scan.animate.set_x(g_fix.get_left()[0] - 0.12), run_time=1.1, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeOut(scan), run_time=0.3)
            vo.wait_until("work, and made")
            self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in g_cor], lag_ratio=0.08), run_time=0.8)
            self.play(FadeIn(c_cor, shift=UP * 0.1), run_time=0.4)

            vo.wait_until("One fixer said")
            # the change leaves the fixers' squares (between the count labels), then opens into its card
            traveler = src_sq.copy()
            self.play(Indicate(src_sq, color=S.WHITE, scale_factor=1.6), run_time=0.5)
            self.add(traveler)
            self.play(traveler.animate.move_to(card_b.get_center()), run_time=0.45, rate_func=rate_functions.ease_in_out_sine)
            self.play(ReplacementTransform(traveler, card_b), FadeIn(VGroup(head, claim), scale=0.6), run_time=0.5)
            self.remove(card_b, head, claim)
            self.add(card)
            vo.wait_until("now fit its")
            self.play(FadeIn(gate), card.animate.shift(RIGHT * dx), run_time=0.9, rate_func=rate_functions.ease_in_quad)
            vo.wait_until("It didn't")
            self.play(card.animate(rate_func=rate_functions.ease_out_back).shift(LEFT * dx),
                      Flash(wall.get_center(), color=MEASURED, line_length=0.2, flash_radius=0.4),
                      Indicate(crews[2].people, color=S.WHITE, scale_factor=1.08), run_time=0.6)
            self.play(ReplacementTransform(card_b, big_b), FadeIn(meas, shift=UP * 0.1), run_time=0.5)
        self.play(Circumscribe(meas, color=S.WHITE, buff=0.06, time_width=0.5), run_time=1.0)
        self.wait(0.6)
        fade_out_all(self)
