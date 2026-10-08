"""S10 · What to improve next.

Beats: a board of four empty slots under its rule, "the biggest gaps sit where measuring runs
out": a GREEN row of the measured checks of S06-S09 (lint, asserts, frame fingerprints, speech
recognizer) runs out, and the dashed YELLOW stretch beyond it becomes card 1, "only people can do
this", which slides into slot 1 -> S01's motif (the agents under the RED-struck headphones): a PINK
person comes in and the headphones move onto their head, the strike falls away; four open items
(dashed YELLOW bullets) build beside them (fact sheet 6) -> card 1 opens into two columns: PINK
"decided by the user", BLUE "decided by the agent · worth a second look", each agent's call in a
dashed YELLOW outline -> the columns fold back into tab 1; card 2, "engineering", slides into slot
2 and three index cards come out of it (each with the "idea · not built yet" tag); the stage beside
them shows one at a time: (a) the real LANGUAGES.md line (A36) -> Azure (0 clips when the script
was written) -> 417 sentence dots re-voiced and re-timed; (b) S05's clip (A18 envelope, A19 word
bars): the estimated pin (1.42 s) snaps onto the measured word (3.26 s) and turns GREEN, and the
real hand-set shift (A20, line 317) is struck out; (c) GREEN bars of scene code per minute (400,
310) shrink as a two-shelf rack of shared parts fills, the cut-off part dashed YELLOW; a footnote
card (the black frame of the privacy video's part 2) -> card 3, "subtitles that understand
sentences": a long example cue (this scene's own last sentence) is cut by GREY hand-written rules
in the wrong place ("and the / rules"); the first review round in squares (19 of 21 fixed, its
own report; 11 RED regressions) and the round-3/4 and Chinese-privacy facts (as of the script);
then a GREY sentence parser proposes the cut after "cuts,", the rules turn GREEN and check it, and
the words reflow -> card 4, "interactivity": the user's own words from S02 (card 4, "interactive"
outlined), then a real tic-tac-toe frame in a player, apart from the two real playground
screenshots (A33, A34) -> pausing: the tic-tac-toe video's last ponder question appears in the
player, its playground docks beside it in one window (dashed YELLOW, "idea · not built yet"),
"same state", "answer saved" -> the card folds into tab 4, the full board pulses, everything fades.

Every number and real string on screen is checked in _check() (runs on import) against the
assets and the script's show lines.

Helpers defined here (not in common.py): collect() (as in s09), glyphs_like() (as s02's quote_glyphs),
wave_poly() (as in s05), dashed_card(), slot(), tab_card(), bullet(), open_item(), cue_line(),
word_groups(), solid_chip(), squares(), ponder_question().
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.scene import VoiceScene

from common import (AGENT, AUDIO, BUG, DICTATED, EXCERPTS, IDEA, INK, MEASURED, NARRATION, OPEN, PANEL, PROJECT,
                    QUOTES, SANS, SUB_AGENT_TEXT, TOOL, USER, anchor_pin, asset, asset_text, box, cant_hear_or_play,
                    caption, check_mark, chip, code_block, code_span, dim, exhibit, fade_out_all, label,
                    load_envelope, measured_badge, mono, open_outline, open_tag, play_button, pulse, quote_card,
                    role_icon, sub_agent_cluster, undim, video_player)

SAY = NARRATION["S10"]

# ------------------------------------------------------------------ the words on screen (script.md S10)
# Show-line texts, with line breaks for the layout only (each is checked against its one-line
# original in _check()).
RULE = "the biggest gaps sit where measuring runs out"
CARD_TITLES = ["only people can do this", "engineering", "subtitles that understand sentences", "interactivity"]
CHECKS = ["lint", "asserts", "frame fingerprints", "speech recognizer"]       # the GREEN checks of S06-S09

OPEN_ITEMS = [                                       # card 1, fact sheet 6 (not yet verified)
    "no recorded human review of the narration yet,\nEnglish or Chinese",
    "English narration: checked by a speech recognizer\nfor this video, no human listening yet",
    "every test viewer on record: an AI persona",
    "learning not measured: no quiz, no data",
]
USER_HEAD, AGENT_HEAD = "decided by the user", "decided by the agent · worth a second look"
USER_CALLS = ["the topics", "the audiences", "Chinese, code-switched", "this video"]
AGENT_CALLS = [
    "privacy video: 24 min, not the 12–15\nits own README prompt suggests → also cut into 2 parts",
    "Chinese voice: the top scorer was male and English-first\n→ a native Mandarin female voice, to match the English\n"
    "(another female voice scored about as well)",
    "which English words to keep:\nargued by simulated Chinese readers",
    "small edits to the user's program",
]

ENG_TITLES = ["A licensed Chinese voice", "Word-level timing", "Shared parts"]
A36 = EXCERPTS["A36"]
LICENCE = A36["licence"]                             # "the free Edge endpoint is not licensed for published videos"
LICENCE_SHOWN = "“the free Edge endpoint\nis not licensed for\npublished videos”"
LICENCE_CAP = "real · docs/LANGUAGES.md · line 60"
AZURE = "Azure AI Speech:\nsame voices, licensed"
CLIPS_WHEN_WRITTEN = A36["azure_clips_when_written"]                 # 0 (live value: see script.md)
CLIPS = f"clips made when this\nscript was written: {CLIPS_WHEN_WRITTEN}"
PAIRS = EXCERPTS["A27"]["sentence_pairs"]["total"]                   # 417
REVOICE = f"switching re-voices all\n{PAIRS} sentences, then\nre-times them"
SHIFT_LINE = EXCERPTS["A20"]["shift_line"]           # wait_for(self, vo, "counted those", shift=2.2)
SHIFT_CAP = "tic-tac-toe video · scenes/s03_stop.py · line 317"
TIMING_NOTE = "then delete the hand-set shifts ·\nadd a lint for sync, overlaps and dead air"
WAVE_CAP = "clip from “The audio is the clock” · word times: a speech recognizer"
CODE_HEAD = "scene code per minute of video:"
LINES_PER_MIN = [(400, "about 400 lines (tic-tac-toe)"), (310, "about 310 (privacy)")]
PARTS = [["board", "game tree", "counter"], ["code panel", "paper card"]]
FOOT = "also: the English privacy video, part 2, opens on a black frame, voice at 0.088 s → add a lead-in"

# card 3: the first review round (narrated) and the later state, as the script had it when written
SUB_HEAD = "rule-based rewrite, first review round:"
SUB_FIXED, SUB_ISSUES, SUB_REGRESSIONS = 19, 21, 11
SUB_FIXED_L = f"{SUB_FIXED} of {SUB_ISSUES} issues fixed (its own report)"
SUB_REG_L = f"reviewers found {SUB_REGRESSIONS} regressions"
# Live values (script.md "Live values": subtitle tool, Chinese privacy final cut): refresh these
# two lines, worded as the script's show line, right before the final render.
SUB_LATER = ("four rounds in all: 49 tests\n"
             "· rule tuning stopped at diminishing returns (its commit note)")
ZH_PRIVACY = "privacy video, Chinese: final cut rendered with the new subtitles"
CUE = "A sentence parser could propose the cuts, and the rules could check them."   # this scene's own words
CUE_WORDS = CUE.split()
BAD_SPLIT, GOOD_SPLIT = CUE_WORDS.index("rules"), CUE_WORDS.index("and")          # "… and the | rules …"
CUE_CAP = "example cue (diagram): this scene's own last sentence"

# card 4
FRAME_PNG, FRAME_CAP = "ttt_0530.png", "real frame · tic-tac-toe video, 5:30"
LAPLACE_PNG, TTT_PNG = "dp_playground.png", "ttt_playground.png"
PG_CAP = "real screenshots · the two playgrounds"
TTT_BOARD_PX = (138, 244, 462, 568)                  # the board in ttt_playground.png (1280 x 800)
PONDER_Q = "Which first move for X leads to the MOST different games:\ncorner, edge, or center?"   # tic-tac-toe s08
PONDER_SHOWN = "Which first move for X leads\nto the MOST different games:\ncorner, edge, or center?"
MERGE_CAP = "diagram · the tic-tac-toe video's last ponder, opening its playground"

# S05's clip (A17-A19): the estimate of "counted those" and the measured words around it
EST = EXCERPTS["A17"]["estimate_counted_those"]["seconds"]          # 1.42 s
ENV_T, ENV_V = load_envelope()                                       # A18, one value per 20 ms
WIN_T = 4.4                                                          # the part of the clip drawn


def _words():
    out = []
    for row in asset_text("ttt_s03_say1_words.txt").splitlines():
        a, b, w = row.split(None, 2)
        out.append((float(a), float(b), w.strip()))
    return out


WORDS = {}
for _a, _b, _w in _words():
    WORDS.setdefault(_w, (_a, _b))                   # the first time each word is heard
BARS = [("362", WORDS["362"]), (",880", WORDS[",880"]), ("counted", WORDS["counted"])]


def _one_line(s: str) -> str:
    return s.replace("\n", " ")


def _check():
    # card 1 and its columns: the show lines' words, only re-broken
    assert [_one_line(s) for s in OPEN_ITEMS] == [
        "no recorded human review of the narration yet, English or Chinese",
        "English narration: checked by a speech recognizer for this video, no human listening yet",
        "every test viewer on record: an AI persona", "learning not measured: no quiz, no data"]
    assert _one_line(AGENT_CALLS[0]) == ("privacy video: 24 min, not the 12–15 its own README prompt suggests → "
                                         "also cut into 2 parts")
    assert _one_line(AGENT_CALLS[1]) == ("Chinese voice: the top scorer was male and English-first → a native "
                                         "Mandarin female voice, to match the English (another female voice "
                                         "scored about as well)")
    assert _one_line(AGENT_CALLS[2]) == "which English words to keep: argued by simulated Chinese readers"
    # card 2: the real line, the live 0, the 417 sentence pairs, S05's clip and shift
    assert _one_line(LICENCE_SHOWN) == f"“{LICENCE}”" and LICENCE == "the free Edge endpoint is not licensed for published videos"
    assert CLIPS_WHEN_WRITTEN == 0 and _one_line(CLIPS) == "clips made when this script was written: 0"
    assert PAIRS == 417 == EXCERPTS["A27"]["sentence_pairs"]["tictactoe"] + EXCERPTS["A27"]["sentence_pairs"]["privacy"]
    assert _one_line(REVOICE) == "switching re-voices all 417 sentences, then re-times them"
    assert _one_line(TIMING_NOTE) == "then delete the hand-set shifts · add a lint for sync, overlaps and dead air"
    assert SHIFT_LINE == asset_text("code/ttt_s03_stop_317.py").strip() and "shift=2.2" in SHIFT_LINE
    assert EST == 1.42 and WORDS["362"] == (0.24, 1.56) and WORDS[",880"] == (1.56, 3.26)
    assert WORDS["counted"] == (3.26, 4.0) and WORDS["counted"][1] < WIN_T <= ENV_T[-1]
    # card 3: the counts of the first review round (ASSETS "Other numbers"), the example cue
    assert (SUB_FIXED, SUB_ISSUES, SUB_REGRESSIONS) == (19, 21, 11)
    assert SAY[3].endswith(CUE) and CUE_WORDS[BAD_SPLIT - 2:BAD_SPLIT] == ["and", "the"]
    # card 4: the user's words, the real ponder question of the tic-tac-toe video
    q4 = QUOTES["s02_card4"]
    assert q4["open"] == "interactive" and "interactive" in q4["screen"]
    assert _one_line(PONDER_SHOWN) == _one_line(PONDER_Q)
    ttt = PROJECT.parent / "tictactoe-255168"
    if (ttt / "script.md").exists():
        assert "Which first move for X leads to the MOST different games: corner, edge, or center?" in \
            (ttt / "script.md").read_text(encoding="utf-8")
    for name in (FRAME_PNG, LAPLACE_PNG, TTT_PNG):
        asset(name)


_check()

# ------------------------------------------------------------------ layout
TITLE_Y = 3.3                        # the board: its rule ...
TAB_Y, TAB_H, TAB_SIZE, TAB_PAD, TAB_GAP = 2.62, 0.5, 22, 0.2, 0.1      # ... and its four slots
TOP = 2.2                            # top of the stage under the board
CHECKS_Y = 0.15                      # the GREEN checks row of the opening
LEFT_X = -6.3                        # left edge of most content
LIST_X = -1.85                       # card 1: the open items
ICON_Y = -0.35                       # card 1: the people row
HEAD_Y = 1.72                        # card 1, columns: the headers
INDEX_X, INDEX_W = -4.45, 3.95       # card 2: the index cards ...
INDEX_Y = (1.45, 0.12, -1.21)
STAGE_X0, STAGE_X1 = -2.25, 6.45     # ... and the stage beside them
FOOT_Y = -3.3


# ------------------------------------------------------------------ helpers (this scene only)
def collect(scene, *mobs) -> Group:
    """Make several on-screen things ONE top-level group (each thing's whole family leaves the top
    level first, so no part that came on screen by itself stays behind)."""
    for m in mobs:
        scene.remove(*m.get_family())
    g = Group(*mobs)
    scene.add(g)
    return g


def dashed_card(width: float, height: float, fill: str = PANEL) -> VGroup:
    """A card with the dashed YELLOW 'still open' outline on a dark fill."""
    under = RoundedRectangle(width=width, height=height, corner_radius=min(0.14, height / 2),
                             stroke_width=0).set_fill(fill, 1)
    return VGroup(under, box(width, height, OPEN, dashed=True, stroke=3))


def slot(width: float, n: int) -> VGroup:
    """An empty slot of the board: a thin GREY outline and its number."""
    r = RoundedRectangle(width=width, height=TAB_H, corner_radius=0.12, stroke_color=S.GREY_DARK, stroke_width=2.5)
    r.set_fill(S.BG, 0)
    num = label(str(n), TAB_SIZE, TOOL).move_to(r)
    g = VGroup(r, num)
    g.frame, g.num = r, num
    return g


def tab_card(title: str, width: float, dashed: bool = False) -> VGroup:
    """A card in its slot: GREY (or dashed YELLOW, card 1) with its title. .frame .text"""
    t = label(title, TAB_SIZE, INK)
    if dashed:
        frame = dashed_card(width, TAB_H)
    else:
        frame = box(width, TAB_H, TOOL, fill=PANEL, fill_opacity=1, radius=0.12)
    t.move_to(frame)
    g = VGroup(frame, t)
    g.frame, g.text = frame, t
    return g


def bullet(size: float = 0.24) -> VMobject:
    """A dashed YELLOW square: an item that is still open."""
    return box(size, size, OPEN, dashed=True, stroke=2.5, radius=0.04)


def open_item(s: str, t2c: dict | None = None, size: float = 24) -> VGroup:
    """A bullet and a (pre-broken) text, top-aligned."""
    t = label(s, size, INK, line_spacing=0.9, t2c=t2c or {})
    b = bullet()
    b.next_to(t, LEFT, buff=0.25).align_to(t, UP).shift(DOWN * 0.04)
    g = VGroup(b, t)
    g.bullet, g.text = b, t
    return g


def wave_poly(t0: float, t1: float, x0: float, x1: float, y: float, height: float,
              color: str = AUDIO, gamma: float = 0.6) -> VMobject:
    """A filled, mirrored waveform of the A18 envelope between t0 and t1 (s), drawn from x0 to x1."""
    sel = (ENV_T >= t0 - 1e-6) & (ENV_T <= t1 + 1e-6)
    tt, vv = ENV_T[sel], ENV_V[sel]
    xs = x0 + (tt - t0) / (t1 - t0) * (x1 - x0)
    hh = np.maximum((vv / float(ENV_V.max())) ** gamma * height / 2, 0.012)
    top = [[x, y + h, 0] for x, h in zip(xs, hh)]
    bot = [[x, y - h, 0] for x, h in zip(xs[::-1], hh[::-1])]
    m = VMobject(stroke_width=0).set_points_as_corners(top + bot + [top[0]])
    return m.set_fill(color, 0.85)


def cue_line(words: list[str], size: float = 26) -> Text:
    return S.text(" ".join(words), size, INK, font=SANS)


def word_groups(lines: list[Text], words_per_line: list[list[str]]) -> list[VGroup] | None:
    """The glyphs of each word (in order across the lines) of cue lines built with cue_line(); None
    if a line's glyphs don't match its words (a translated build)."""
    out = []
    for t, ws in zip(lines, words_per_line):
        if len(t.submobjects) != sum(len(w) for w in ws):
            return None
        i = 0
        for w in ws:
            out.append(VGroup(*t.submobjects[i:i + len(w)]))
            i += len(w)
    return out


def solid_chip(s: str, icon=None, size: float = 22) -> VGroup:
    """A GREY chip on an opaque dark fill (it sits on top of a screenshot)."""
    t = label(s, size, INK)
    content = VGroup(icon, t).arrange(RIGHT, buff=0.12) if icon is not None else t
    b = box(content.width + 0.5, max(content.height, 0.3) + 0.26, TOOL, fill=PANEL, fill_opacity=1, radius=0.2)
    content.move_to(b)
    return VGroup(b, content)


def squares(n: int, color: str, fill: float, side: float = 0.24, gap: float = 0.07) -> VGroup:
    g = VGroup(*[box(side, side, color, fill_opacity=fill, stroke=2, radius=0.04) for _ in range(n)])
    return g.arrange(RIGHT, buff=gap)


def ponder_question(width: float = 5.0) -> VGroup:
    """The tic-tac-toe video's last ponder card (the toolkit's card, its real question)."""
    card = ponder_card(PONDER_SHOWN, width=width, size=24)
    return card


MARK = "#FF00FE"                     # probe colour, never drawn


def glyphs_like(t: Text, sub: str, size: float, **kw) -> VGroup:
    """The glyphs of `sub` inside Text t (built with label(t.original_text, size, **kw)). A twin
    with `sub` coloured by t2c is matched by index, so ligatures ('fi' in 'definitely') can't
    shift the count. Empty if `sub` isn't there (a translated build)."""
    try:
        twin = label(t.original_text, size, INK, t2c={sub: MARK}, **kw)
    except Exception:                                   # noqa: BLE001 (translated build)
        return VGroup()
    if len(twin.submobjects) != len(t.submobjects):
        return VGroup()
    mark = ManimColor(MARK).to_rgb()
    idx = [i for i, g in enumerate(twin.submobjects) if np.allclose(g.get_fill_color().to_rgb(), mark, atol=0.02)]
    return VGroup(*[t.submobjects[i] for i in idx])


class WhatNext(VoiceScene):
    def construct(self):
        # ================================================================ the board and its rule
        widths = [label(s, TAB_SIZE).width + 2 * TAB_PAD for s in CARD_TITLES]
        total = sum(widths) + TAB_GAP * 3
        xs, x = [], -total / 2
        for w in widths:
            xs.append(x + w / 2)
            x += w + TAB_GAP
        slots = VGroup(*[slot(w, k + 1).move_to([cx, TAB_Y, 0]) for k, (w, cx) in enumerate(zip(widths, xs))])
        tabs = [tab_card(s, w, dashed=(k == 0)).move_to([cx, TAB_Y, 0])
                for k, (s, w, cx) in enumerate(zip(CARD_TITLES, widths, xs))]
        assert slots.get_left()[0] > -6.55 and slots.get_right()[0] < 6.55
        rule = label(RULE, 30, INK, t2c={"measuring": MEASURED}).move_to([0, TITLE_Y, 0])

        # the measured checks run out
        badges = VGroup(*[measured_badge(s, 24) for s in CHECKS]).arrange(RIGHT, buff=0.22)
        badges.move_to([0, CHECKS_Y + 0.55, 0]).align_to([LEFT_X, 0, 0], LEFT)
        floor = Rectangle(width=badges.width + 0.3, height=0.16, stroke_width=0).set_fill(MEASURED, 0.85)
        floor.next_to(badges, DOWN, buff=0.22).align_to(badges, LEFT).shift(LEFT * 0.15)
        floor_l = label("measured", 24, MEASURED).next_to(floor, DOWN, buff=0.16).align_to(floor, LEFT)
        gap_x0 = floor.get_right()[0] + 0.3
        beyond = dashed_card(6.2 - gap_x0, 1.5).move_to([(gap_x0 + 6.2) / 2, CHECKS_Y + 0.2, 0])
        beyond[0].set_fill(S.BG, 0)
        qmark = label("?", 48, TOOL).move_to(beyond)

        # ================================================================ card 1: what only people can do
        agent = role_icon("agent", 1.05).move_to([-4.15, ICON_Y, 0])
        subs = sub_agent_cluster(4, 0.36, cols=2).move_to([-2.95, ICON_Y - 0.08, 0])
        ears = cant_hear_or_play(0.78)[0].move_to([-3.55, ICON_Y + 1.45, 0])       # (headphones, strike)
        hp, hp_x = ears
        person = role_icon("user", 1.4).move_to([-5.65, ICON_Y - 0.05, 0]).person
        head = person[0]
        worn_h = 0.62 * person.height
        worn = hp.copy().scale_to_fit_height(worn_h)
        band = worn[0]
        worn.shift(head.get_center() + UP * 0.03 - band.get_arc_center())
        items = VGroup(
            open_item(OPEN_ITEMS[0]),
            open_item(OPEN_ITEMS[1], t2c={"checked by a speech recognizer": MEASURED}),
            open_item(OPEN_ITEMS[2], t2c={"an AI persona": SUB_AGENT_TEXT}),
            open_item(OPEN_ITEMS[3]),
        ).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        items.move_to([0, -0.25, 0]).align_to([LIST_X, 0, 0], LEFT)
        assert items.get_right()[0] < 6.45 and items.get_top()[1] < TOP - 0.1
        assert subs.get_right()[0] < items.get_left()[0] - 0.35

        with self.voiceover(SAY[0]) as vo:
            self.play(LaggedStart(*[Create(s.frame) for s in slots], lag_ratio=0.18),
                      LaggedStart(*[FadeIn(s.num) for s in slots], lag_ratio=0.18), run_time=1.1)
            vo.wait_until("The biggest gaps")
            self.play(Write(rule), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in badges], lag_ratio=0.2),
                      GrowFromEdge(floor, LEFT), FadeIn(floor_l), run_time=1.1)
            vo.wait_until("where measuring runs out")
            self.play(Create(beyond[1]), FadeIn(beyond[0]), FadeIn(qmark, scale=0.8), run_time=0.8)
            self.play(Indicate(qmark, color=S.WHITE, scale_factor=1.25), run_time=0.6)

            # the open stretch becomes card 1, in slot 1
            vo.wait_until("First, what only")
            self.play(FadeOut(collect(self, badges, floor, floor_l), shift=LEFT * 0.4),
                      FadeOut(qmark, scale=0.5), FadeOut(slots[0].num),
                      ReplacementTransform(beyond, tabs[0].frame), run_time=0.9)
            self.play(FadeIn(tabs[0].text, scale=0.9), run_time=0.4)
            self.remove(tabs[0].frame, tabs[0].text)         # the card, one top-level object
            self.add(tabs[0])
            # S01's motif: the agents can't hear; the ears go to a person
            self.play(FadeIn(agent, shift=UP * 0.2), FadeIn(subs, shift=UP * 0.2), FadeIn(hp, shift=DOWN * 0.15),
                      run_time=0.6)
            self.play(Create(hp_x), run_time=0.35)
            self.play(FadeIn(person, shift=RIGHT * 0.4), run_time=0.5)
            self.play(Transform(hp, worn, path_arc=0.9), FadeOut(hp_x, shift=DOWN * 0.5), run_time=0.9)
            ears_on = VGroup(person, hp)                        # the person, wearing the headphones
            self.remove(person, hp)
            self.add(ears_on)

            vo.wait_until("There's no recorded")
            self.play(FadeIn(items[0], shift=RIGHT * 0.25), run_time=0.6)
            self.play(Indicate(ears_on, color=S.WHITE, scale_factor=1.06), run_time=0.7)
            self.play(FadeIn(items[1], shift=RIGHT * 0.25), run_time=0.6)
            vo.wait_until("Every test viewer")
            self.play(FadeIn(items[2], shift=RIGHT * 0.25), Indicate(subs, color=S.WHITE, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("and there's no measure")
            self.play(FadeIn(items[3], shift=RIGHT * 0.25), run_time=0.6)
            self.play(LaggedStart(*[Indicate(it.bullet, color=S.WHITE, scale_factor=1.4) for it in items],
                                  lag_ratio=0.2), run_time=1.0)

        # ================================================================ card 1 opens: who decided what
        u_icon = VGroup(person.copy(), hp.copy()).scale_to_fit_height(0.8).move_to([-5.95, HEAD_Y, 0])
        u_head = label(USER_HEAD, 24, USER).next_to(u_icon, RIGHT, buff=0.22)
        a_icon = role_icon("agent", 0.82).move_to([-1.7, HEAD_Y, 0])
        a_head = label(AGENT_HEAD, 24, AGENT).next_to(a_icon, RIGHT, buff=0.3)
        u_calls = VGroup(*[chip(s, USER, 24) for s in USER_CALLS]).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        u_calls.next_to(u_icon, DOWN, buff=0.45).align_to([LEFT_X, 0, 0], LEFT)
        a_text = [label(s, 22, INK, line_spacing=0.8) for s in AGENT_CALLS]
        a_rows = VGroup()
        for t in a_text:                                    # more room left and right than above and below
            a_rows.add(VGroup(box(t.width + 0.42, t.height + 0.28, OPEN, dashed=True, stroke=2.5).move_to(t), t))
        a_rows.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        a_rows.next_to(a_icon, DOWN, buff=0.3).align_to([-2.15, 0, 0], LEFT)
        assert a_rows.get_right()[0] < 6.5 and a_rows.get_bottom()[1] > -3.55, (a_rows.get_right(), a_rows.get_bottom())
        assert u_calls.get_right()[0] < a_rows.get_left()[0] - 0.3 and a_head.get_right()[0] < 6.5
        first = glyphs_like(a_text[0], "24 min", 22, line_spacing=0.8) or a_text[0]

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(collect(self, *items), shift=UP * 0.3), FadeOut(subs, shift=DOWN * 0.2),
                      ReplacementTransform(ears_on, u_icon), ReplacementTransform(agent, a_icon), run_time=0.9)
            self.play(FadeIn(u_head, shift=RIGHT * 0.15),
                      LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in u_calls], lag_ratio=0.2), run_time=0.9)
            vo.wait_until("the agent's own calls")
            self.play(FadeIn(a_head, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("like the length")
            self.play(FadeIn(a_rows[0][1], shift=UP * 0.12), Create(a_rows[0][0]), run_time=0.7)
            self.play(Indicate(first, color=S.WHITE, scale_factor=1.15), run_time=0.6)
            vo.wait_until("and the choice")
            self.play(FadeIn(a_rows[1][1], shift=UP * 0.12), Create(a_rows[1][0]), run_time=0.7)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[1], shift=UP * 0.12), Create(r[0])) for r in a_rows[2:]],
                                  lag_ratio=0.4), run_time=0.9)
        self.play(LaggedStart(*[Circumscribe(r[0], color=S.WHITE, buff=0.04, time_width=0.5) for r in a_rows],
                              lag_ratio=0.25), run_time=1.4)

        # ================================================================ card 2: engineering
        index = []
        for k, (title, y) in enumerate(zip(ENG_TITLES, INDEX_Y)):
            t = label(title, 24, INK)
            tg = open_tag(IDEA)
            body = VGroup(t, tg).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            b = box(INDEX_W, body.height + 0.36, TOOL, fill=PANEL, fill_opacity=1, radius=0.14)
            body.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.2)
            card = VGroup(b, body).move_to([INDEX_X, y, 0])
            card.box, card.title, card.tag = b, t, tg
            index.append(card)
        index = VGroup(*index)
        assert index.get_left()[0] > -6.5 and index.get_right()[0] < STAGE_X0 - 0.15
        assert all(c.title.width < INDEX_W - 0.3 for c in index)

        # (a) a licensed voice
        quote = label(LICENCE_SHOWN, 24, INK, line_spacing=0.9)
        q_box = box(quote.width + 0.5, quote.height + 0.4, TOOL, fill=PANEL, fill_opacity=1, radius=0.12)
        quote.move_to(q_box)
        q_panel = VGroup(q_box, quote).move_to([0, 1.35, 0]).align_to([STAGE_X0, 0, 0], LEFT)
        q_cap = caption(LICENCE_CAP).next_to(q_panel, DOWN, buff=0.12).align_to(q_panel, LEFT)
        az_t = label(AZURE, 24, INK, line_spacing=0.9)
        clips = label(CLIPS, 22, TOOL, line_spacing=0.9)
        az_body = VGroup(az_t, clips).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        az_box = box(az_body.width + 0.5, az_body.height + 0.4, TOOL, fill=PANEL, fill_opacity=1, radius=0.12)
        az_body.move_to(az_box)
        az = VGroup(az_box, az_body).move_to([0, 1.2, 0]).align_to([STAGE_X1 - 0.05, 0, 0], RIGHT)
        arr1 = Arrow(q_panel.get_right(), az.get_left(), buff=0.12, color=TOOL, stroke_width=3, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.3)
        assert az.get_left()[0] - q_panel.get_right()[0] > 0.5, (az.get_left(), q_panel.get_right())
        dots = VGroup(*[Dot(radius=0.042, color=AUDIO) for _ in range(PAIRS)])
        dots.arrange_in_grid(cols=30, buff=0.06).move_to([0, -1.3, 0]).align_to([STAGE_X0 + 0.1, 0, 0], LEFT)
        rv = label(REVOICE, 24, INK, line_spacing=0.9, t2c={str(PAIRS): AUDIO})
        rv.next_to(dots, RIGHT, buff=0.45)
        arr2 = Arrow(az.get_bottom(), [rv.get_x(), rv.get_top()[1], 0], buff=0.12, color=TOOL, stroke_width=3,
                     tip_length=0.18, max_tip_length_to_length_ratio=0.3)
        assert rv.get_right()[0] < 6.5 and dots.get_bottom()[1] > FOOT_Y + 0.4

        # (b) word-level timing (S05's clip)
        wx0, wx1, wy, wh = STAGE_X0 + 0.15, STAGE_X1 - 0.25, 0.74, 1.0

        def tx(t: float) -> float:
            return wx0 + (wx1 - wx0) * t / WIN_T

        wave = wave_poly(0.0, WIN_T, wx0, wx1, wy, wh)
        bar_y = wy - wh / 2 - 0.3
        bars, bar_l = VGroup(), VGroup()
        for w, (a, b) in BARS:
            r = RoundedRectangle(width=tx(b) - tx(a) - 0.05, height=0.13, corner_radius=0.06,
                                 stroke_width=0).set_fill(MEASURED, 1).move_to([(tx(a) + tx(b)) / 2, bar_y, 0])
            bars.add(r)
            bar_l.add(mono(w, 22, MEASURED).next_to(r, DOWN, buff=0.12))
        pin = anchor_pin(AUDIO, 0.5, estimated=True)
        pin.shift(np.array([tx(EST), wy + wh / 2 + 0.05, 0]) - pin[1].get_bottom())
        pin_l = mono("counted those", 22, AUDIO).next_to(pin, UP, buff=0.1)
        green_pin = anchor_pin(MEASURED, 0.5)
        green_pin.shift(np.array([tx(WORDS["counted"][0]), wy + wh / 2 + 0.05, 0]) - green_pin[1].get_bottom())
        wave_cap = caption(WAVE_CAP).next_to(bar_l, DOWN, buff=0.16).align_to([wx0, 0, 0], LEFT)
        code = code_block(SHIFT_LINE.strip(), 20)
        code.move_to([0, -1.58, 0]).align_to([STAGE_X0, 0, 0], LEFT)
        code_cap = caption(SHIFT_CAP).next_to(code, DOWN, buff=0.1).align_to(code, LEFT)
        shift_g = code_span(code, 0, "shift=2.2")
        cut_g = code_span(code, 0, ", shift=2.2")
        glow = SurroundingRectangle(shift_g, buff=0.05, stroke_width=0, corner_radius=0.05).set_fill(AUDIO, 0)
        code.submobjects.insert(1, glow)                    # behind the glyphs, above the panel
        x_line = Line(cut_g.get_left() + LEFT * 0.03, cut_g.get_right() + RIGHT * 0.03, color=BUG, stroke_width=5)
        note = label(TIMING_NOTE, 24, INK, line_spacing=0.9).next_to(code_cap, DOWN, buff=0.22).align_to(code, LEFT)
        assert code.get_right()[0] < 6.5 and note.get_bottom()[1] > -3.5, (code.get_right(), note.get_bottom())
        assert pin_l.get_top()[1] < TOP and wave_cap.get_bottom()[1] > code.get_top()[1] + 0.1, (pin_l.get_top(), wave_cap.get_bottom(), code.get_top())

        # (c) shared parts
        c_head = label(CODE_HEAD, 24, INK).move_to([0, 1.75, 0]).align_to([STAGE_X0, 0, 0], LEFT)
        full_w = 6.2
        lpm_bars, lpm_l, ghosts = VGroup(), VGroup(), VGroup()
        for k, (n, s) in enumerate(LINES_PER_MIN):
            w = full_w * n / LINES_PER_MIN[0][0]
            r = Rectangle(width=w, height=0.24, stroke_width=0).set_fill(MEASURED, 0.85)
            r.move_to([STAGE_X0 + w / 2, 1.08 - k * 0.92, 0])
            lpm_bars.add(r)
            lpm_l.add(label(s, 24, INK).next_to(r, DOWN, buff=0.12).align_to(r, LEFT))
        SHRINK = 0.62
        for r in lpm_bars:
            nw = r.width * SHRINK
            ghosts.add(box(r.width - nw, r.height + 0.02, OPEN, dashed=True, stroke=2, radius=0.02)
                       .move_to([r.get_left()[0] + nw + (r.width - nw) / 2, r.get_y(), 0]))
        shelves, parts = VGroup(), VGroup()
        for k, row in enumerate(PARTS):
            y = -1.3 - k * 0.9
            shelf = Line([STAGE_X0, y, 0], [STAGE_X0 + 6.6, y, 0], color=TOOL, stroke_width=3)
            cs = VGroup(*[chip(s, TOOL, 24) for s in row]).arrange(RIGHT, buff=0.16)
            cs.next_to(shelf, UP, buff=0.04).align_to(shelf, LEFT).shift(RIGHT * 0.15)
            shelves.add(shelf)
            parts.add(*cs)
        shelf_l = caption("shared parts").next_to(shelves[-1], DOWN, buff=0.1).align_to(shelves[-1], LEFT)
        foot_t = label(FOOT, 20, TOOL)
        foot = VGroup(box(foot_t.width + 0.4, foot_t.height + 0.26, TOOL, fill=PANEL, fill_opacity=1, radius=0.1),
                      foot_t).move_to([0, FOOT_Y, 0])
        foot_t.move_to(foot[0])
        assert foot.get_left()[0] > -6.55 and foot.get_right()[0] < 6.55
        assert shelf_l.get_bottom()[1] > foot.get_top()[1] + 0.05 and parts.get_right()[0] < 6.5

        with self.voiceover(SAY[2]) as vo:
            card1 = collect(self, u_icon, u_head, u_calls, a_icon, a_head, a_rows)
            self.play(FadeOut(card1, target_position=tabs[0].get_center(), scale=0.12), *dim(tabs[0], opacity=0.55),
                      FadeOut(slots[1].num), FadeIn(tabs[1], shift=UP * 0.6), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(c, target_position=tabs[1].get_center(), scale=0.3) for c in index],
                                  lag_ratio=0.18), run_time=0.7)
            vo.wait_until("a licensed Chinese voice")
            self.play(Indicate(index[0].title, color=S.WHITE, scale_factor=1.08), index[0].box.animate.set_stroke(INK, 3.5),
                      FadeIn(q_panel, target_position=index[0].get_center(), scale=0.4), FadeIn(q_cap), run_time=0.7)
            vo.wait_until("since the free service")
            self.play(Circumscribe(q_panel, color=S.WHITE, buff=0.06, time_width=0.5), run_time=0.8)
            vo.wait_until("isn't licensed")
            self.play(GrowArrow(arr1), FadeIn(az, shift=LEFT * 0.2), run_time=0.6)
            self.play(Indicate(clips, color=S.WHITE, scale_factor=1.06), run_time=0.45)
            self.play(GrowArrow(arr2), FadeIn(rv, shift=DOWN * 0.15),
                      LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.002), run_time=0.8)

            vo.wait_until("Timing should follow")
            stage_a = collect(self, q_panel, q_cap, arr1, az, arr2, rv, dots)
            self.play(FadeOut(stage_a, target_position=index[0].get_center(), scale=0.15),
                      index[0].box.animate.set_stroke(TOOL, 2.5), run_time=0.4)
            self.play(Indicate(index[1].title, color=S.WHITE, scale_factor=1.08), index[1].box.animate.set_stroke(INK, 3.5),
                      FadeIn(wave, target_position=index[1].get_center(), scale=0.3),
                      LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.25),
                      FadeIn(bar_l), FadeIn(wave_cap), FadeIn(code, shift=UP * 0.15), FadeIn(code_cap), run_time=0.8)
            self.play(FadeIn(pin, shift=DOWN * 0.3), FadeIn(pin_l, shift=DOWN * 0.3), run_time=0.4)
            vo.wait_until("not characters")
            self.play(Wiggle(VGroup(pin, pin_l), scale_value=1.15), glow.animate.set_fill(AUDIO, 0.3), run_time=0.7)
            vo.wait_until("so the hand-set")
            dx = green_pin.get_x() - pin.get_x()
            self.play(pin.animate.shift(RIGHT * dx), pin_l.animate.shift(RIGHT * dx), run_time=0.5,
                      rate_func=rate_functions.ease_in_out_sine)
            self.play(ReplacementTransform(pin, green_pin), pin_l.animate.set_color(MEASURED),
                      Flash(bars[2].get_left(), color=MEASURED, line_length=0.15, flash_radius=0.25),
                      Create(x_line), run_time=0.5)
            self.play(glow.animate.set_fill(AUDIO, 0), cut_g.animate.set_opacity(0.25), FadeIn(note, shift=UP * 0.12),
                      run_time=0.5)

            vo.wait_until("And shared parts")
            stage_b = collect(self, wave, bars, bar_l, green_pin, pin_l, wave_cap, code, code_cap, x_line, note)
            self.play(FadeOut(stage_b, target_position=index[1].get_center(), scale=0.15),
                      index[1].box.animate.set_stroke(TOOL, 2.5), run_time=0.4)
            self.play(Indicate(index[2].title, color=S.WHITE, scale_factor=1.08), index[2].box.animate.set_stroke(INK, 3.5),
                      FadeIn(c_head, shift=DOWN * 0.1),
                      LaggedStart(*[GrowFromEdge(r, LEFT) for r in lpm_bars], lag_ratio=0.3), FadeIn(lpm_l),
                      Create(shelves), FadeIn(shelf_l), run_time=0.7)
            shrink = [r.animate.stretch_to_fit_width(r.width * SHRINK).align_to(r, LEFT) for r in lpm_bars]
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in parts], lag_ratio=0.25), *shrink,
                      LaggedStart(*[Create(g) for g in ghosts], lag_ratio=0.3), run_time=1.5)
        self.play(FadeIn(foot, shift=UP * 0.15), run_time=0.5)
        self.wait(0.7)

        # ================================================================ card 3: subtitles that understand sentences
        long_line = cue_line(CUE_WORDS)
        bad = [CUE_WORDS[:BAD_SPLIT], CUE_WORDS[BAD_SPLIT:]]
        good = [CUE_WORDS[:GOOD_SPLIT], CUE_WORDS[GOOD_SPLIT:]]
        bad_l = VGroup(*[cue_line(ws) for ws in bad]).arrange(DOWN, buff=0.16)
        good_l = VGroup(*[cue_line(ws) for ws in good]).arrange(DOWN, buff=0.16)
        CUE_Y = 0.36
        band_long = Rectangle(width=long_line.width + 0.6, height=long_line.height + 0.5, stroke_width=0)
        band_long.set_fill("#050608", 1).move_to([0.55, CUE_Y, 0])
        long_line.move_to(band_long)
        band_two = Rectangle(width=max(bad_l.width, good_l.width) + 0.7, height=bad_l.height + 0.5, stroke_width=0)
        band_two.set_fill("#050608", 1).move_to([0.55, CUE_Y, 0])
        bad_l.move_to(band_two)
        good_l.move_to(band_two)
        w_long = word_groups([long_line], [CUE_WORDS])
        w_bad = word_groups(list(bad_l), bad)
        w_good = word_groups(list(good_l), good)
        per_word = None not in (w_long, w_bad, w_good)
        if not per_word:                                    # a translated build: whole lines morph
            w_long, w_bad, w_good = [long_line], [VGroup(*bad_l)], [VGroup(*good_l)]
        cue_cap = caption(CUE_CAP).next_to(band_two, DOWN, buff=0.12).align_to(band_two, RIGHT)
        assert band_long.get_left()[0] > -6.5 and band_long.get_right()[0] < 6.5

        def machine_box(top: str, bottom: str, color: str, width: float = 2.9) -> VGroup:
            t = VGroup(label(top, 24, INK), label(bottom, 20, color if color != TOOL else TOOL)).arrange(DOWN, buff=0.08)
            b = box(width, t.height + 0.26, color, fill=PANEL, fill_opacity=1, radius=0.12)
            t.move_to(b)
            g = VGroup(b, t)
            g.box, g.text = b, t
            return g

        MACH_Y = 1.62
        rules0 = machine_box("hand-written rules", "cut each sentence", TOOL).move_to([-1.25, MACH_Y, 0])
        rules1 = machine_box("rules", "checks", MEASURED).move_to(rules0)
        parser = machine_box("sentence parser", "proposes", TOOL).move_to([-4.85, MACH_Y, 0])
        p_arrow = Arrow(parser.get_right(), rules1.get_left(), buff=0.1, color=TOOL, stroke_width=3, tip_length=0.16,
                        max_tip_length_to_length_ratio=0.3)
        cut_x = ((w_long[BAD_SPLIT - 1].get_right()[0] + w_long[BAD_SPLIT].get_left()[0]) / 2 if per_word
                 else long_line.get_x())
        cut = DashedLine([cut_x, long_line.get_top()[1] + 0.16, 0], [cut_x, long_line.get_bottom()[1] - 0.16, 0],
                         color=TOOL, stroke_width=3, dash_length=0.06)
        r_arrow = Arrow(rules0.get_corner(DR) + LEFT * 0.4, cut.get_top(), buff=0.06, color=TOOL, stroke_width=3,
                        tip_length=0.16, max_tip_length_to_length_ratio=0.3)
        mach = VGroup(parser, rules1)
        mach_out = open_outline(mach, buff=0.16, stroke=2.5)
        mach_tag = open_tag(IDEA).next_to(mach_out, RIGHT, buff=0.25)
        assert mach_tag.get_right()[0] < 6.5 and mach_out.get_top()[1] < TOP + 0.05, mach_out.get_top()

        # the bad break, and the parser's proposal
        if per_word:
            under_bad = VGroup(Underline(VGroup(*w_bad[BAD_SPLIT - 2:BAD_SPLIT]), buff=0.06),
                               Underline(w_bad[BAD_SPLIT], buff=0.06)).set_color(BUG).set_stroke(width=4)
            prop_x = (w_bad[GOOD_SPLIT - 1].get_right()[0] + w_bad[GOOD_SPLIT].get_left()[0]) / 2
        else:
            under_bad = Underline(bad_l, buff=0.06).set_color(BUG).set_stroke(width=4)
            prop_x = bad_l[0].get_right()[0] + 0.12
        prop = DashedLine([prop_x, bad_l[0].get_top()[1] + 0.12, 0], [prop_x, bad_l[0].get_bottom()[1] - 0.12, 0],
                          color=TOOL, stroke_width=3, dash_length=0.06)
        ok = check_mark(0.45).next_to(band_two, RIGHT, buff=0.25)

        # the facts underneath
        f_head = label(SUB_HEAD, 24, INK).move_to([0, -0.9, 0]).align_to([LEFT_X, 0, 0], LEFT)
        sq_fix = squares(SUB_ISSUES, TOOL, 0.12)
        sq_fix.next_to(f_head, DOWN, buff=0.22).align_to(f_head, LEFT)
        fixed = VGroup(*sq_fix[:SUB_FIXED])
        sq_reg = squares(SUB_REGRESSIONS, BUG, 0.85)
        sq_reg.next_to(sq_fix, DOWN, buff=0.2).align_to(sq_fix, LEFT)
        lab_x = sq_fix.get_right()[0] + 0.35
        fix_l = label(SUB_FIXED_L, 24, INK).move_to([0, sq_fix.get_y(), 0]).align_to([lab_x, 0, 0], LEFT)
        reg_l = label(SUB_REG_L, 24, BUG).move_to([0, sq_reg.get_y(), 0]).align_to([lab_x, 0, 0], LEFT)
        later = VGroup(label(SUB_LATER, 22, TOOL, line_spacing=0.9), label(ZH_PRIVACY, 22, TOOL))
        later.arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(sq_reg, DOWN, buff=0.3).align_to(f_head, LEFT)
        assert fix_l.get_right()[0] < 6.5 and later.get_right()[0] < 6.5 and later.get_bottom()[1] > -3.58, \
            (fix_l.get_right(), later.get_right(), later.get_bottom())
        assert cue_cap.get_bottom()[1] > f_head.get_top()[1] + 0.05, (cue_cap.get_bottom(), f_head.get_top())

        with self.voiceover(SAY[3]) as vo:
            card2 = collect(self, index, c_head, lpm_bars, lpm_l, ghosts, shelves, shelf_l, parts, foot)
            self.play(FadeOut(card2, target_position=tabs[1].get_center(), scale=0.12), *dim(tabs[1], opacity=0.55),
                      FadeOut(slots[2].num), FadeIn(tabs[2], shift=UP * 0.6), run_time=0.8)
            vo.wait_until("Hand-written rules")
            self.play(FadeIn(rules0, target_position=tabs[2].get_center(), scale=0.3), run_time=0.6)
            self.play(FadeIn(band_long), FadeIn(long_line, shift=UP * 0.1), run_time=0.6)
            self.remove(long_line)                       # the words, one by one, so they can reflow
            self.add(*w_long)
            vo.wait_until("where to cut")
            self.play(GrowArrow(r_arrow), Create(cut), run_time=0.5)
            self.play(ReplacementTransform(band_long, band_two),
                      *[ReplacementTransform(a, b) for a, b in zip(w_long, w_bad)],
                      FadeOut(cut), FadeOut(r_arrow), run_time=1.0)
            self.play(FadeIn(cue_cap), run_time=0.3)

            vo.wait_until("In its first review")
            self.play(FadeIn(f_head, shift=UP * 0.1), LaggedStart(*[FadeIn(s, scale=0.5) for s in sq_fix],
                                                                  lag_ratio=0.05), run_time=0.9)
            vo.wait_until("the newest version fixed")
            self.play(LaggedStart(*[s.animate.set_fill(INK, 0.6) for s in fixed], lag_ratio=0.05),
                      FadeIn(fix_l, shift=LEFT * 0.15), run_time=1.0)
            vo.wait_until("but made 11")
            self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in sq_reg], lag_ratio=0.06),
                      FadeIn(reg_l, shift=LEFT * 0.15), run_time=0.8)
            self.play(Create(under_bad), run_time=0.5)
            self.play(FadeIn(later, shift=UP * 0.1), run_time=0.6)

            vo.wait_until("A sentence parser")
            self.play(FadeIn(parser, shift=RIGHT * 0.3), GrowArrow(p_arrow), run_time=0.6)
            # the whole proposal is the idea: its dashed outline and tag come with it (and stay readable)
            self.play(Create(prop), Indicate(parser.text[1], color=S.WHITE, scale_factor=1.15),
                      Create(mach_out), FadeIn(mach_tag, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("and the rules could")
            self.play(ReplacementTransform(rules0, rules1), run_time=0.5)
            self.play(*[ReplacementTransform(a, b) for a, b in zip(w_bad, w_good)], FadeOut(under_bad),
                      FadeOut(prop), Create(ok), run_time=1.0)
        self.wait(0.5)                                      # the re-cut cue, checked, before the card folds

        # ================================================================ card 4: interactivity
        q4 = QUOTES["s02_card4"]
        qc = quote_card(q4["screen"], DICTATED, size=26, chars=50).move_to([0, -0.4, 0])
        inter = glyphs_like(qc.quote, q4["open"], 26, line_spacing=1.0)
        if len(inter):
            q_out = open_outline(inter, buff=0.07, stroke=3)
        else:                                               # translated build: outline the whole card
            q_out = open_outline(qc.box, buff=0.08)
        q_tag = open_tag(IDEA).next_to(qc.box, UP, buff=0.2).align_to(qc.box, RIGHT)

        player = video_player(5.8, progress=0.42).move_to([-3.25, -0.08, 0])
        frame = player.show(FRAME_PNG)
        frame_cap = caption(FRAME_CAP).next_to(player, DOWN, buff=0.12).align_to(player, LEFT)
        lap = exhibit(LAPLACE_PNG, width=3.9).move_to([3.55, 0.95, 0])
        ttt = exhibit(TTT_PNG, width=3.9).move_to([4.3, -0.95, 0])
        pg_cap = caption(PG_CAP).next_to(ttt, DOWN, buff=0.12).align_to(ttt, RIGHT)
        assert lap.get_top()[1] < TOP and ttt.get_right()[0] < 6.5 and pg_cap.get_bottom()[1] > -3.58
        apart_y = 0.0
        apart = DoubleArrow([player.get_right()[0] + 0.2, apart_y, 0], [lap.get_left()[0] - 0.2, apart_y, 0], buff=0,
                            color=TOOL, stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.25)
        apart_l = label("apart", 24, TOOL).next_to(apart, DOWN, buff=0.12)

        # the merged window: the player's screen and the playground, side by side
        sw = player.screen.width
        page_h = player.screen.height
        page_w = page_h * 1280 / 800
        inner = sw + 0.15 + page_w
        win_w = inner + 0.3
        shift_x = (-win_w / 2 + 0.15 + sw / 2) - player.screen.get_x()
        win_frame = RoundedRectangle(width=win_w, height=player.frame.height, corner_radius=0.18,
                                     stroke_color=TOOL, stroke_width=2.5).set_fill(S.BG, 1)
        win_frame.move_to([0, player.frame.get_y(), 0])
        page_c = np.array([win_w / 2 - 0.15 - page_w / 2, player.screen.get_y(), 0])
        card = ponder_question(sw - 0.4).move_to(player.screen.get_center() + RIGHT * shift_x)
        paused = play_button(0.3, TOOL).move_to(player.pause.get_center() + RIGHT * shift_x)
        paused[0].set_stroke(width=0)
        win_out = open_outline(win_frame, buff=0.12)
        win_tag = open_tag(IDEA)
        win_tag.move_to(win_out.get_corner(UR) + np.array([-win_tag.width / 2 - 0.3, 0, 0]))
        merge_cap = caption(MERGE_CAP).next_to(win_out, DOWN, buff=0.14).align_to(win_out, LEFT)
        same = solid_chip("same state")
        saved = solid_chip("answer saved", icon=check_mark(0.24, INK, 4))
        assert win_out.get_left()[0] > -6.55 and win_out.get_right()[0] < 6.55 and win_out.get_top()[1] < TOP + 0.1
        assert card.height < player.screen.height - 0.2, (card.height, player.screen.height)

        with self.voiceover(SAY[4]) as vo:
            card3 = collect(self, rules1, parser, p_arrow, band_two, *w_good, ok, cue_cap, mach_out, mach_tag,
                            f_head, sq_fix, sq_reg, fix_l, reg_l, later)
            self.play(FadeOut(card3, target_position=tabs[2].get_center(), scale=0.12), *dim(tabs[2], opacity=0.55),
                      FadeOut(slots[3].num), FadeIn(tabs[3], shift=UP * 0.6), run_time=0.8)
            vo.wait_until("closest to the user's")
            self.play(FadeIn(qc, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("interactivity")
            self.play(Create(q_out), FadeIn(q_tag, shift=DOWN * 0.1), run_time=0.6)

            vo.wait_until("The first two videos")
            self.play(FadeOut(collect(self, qc, q_out, q_tag), shift=UP * 0.4),
                      FadeIn(player.frame), FadeIn(frame), FadeIn(player.pause), FadeIn(player.bar),
                      FadeIn(player.done), FadeIn(player.knob), FadeIn(frame_cap), run_time=0.8)
            vo.wait_until("each come with")
            self.play(FadeIn(lap, shift=LEFT * 0.3), run_time=0.5)
            self.play(FadeIn(ttt, shift=LEFT * 0.3), FadeIn(pg_cap), run_time=0.5)
            vo.wait_until("a small web page")
            self.play(Circumscribe(ttt.px_box(*TTT_BOARD_PX), color=S.WHITE, buff=0.05, time_width=0.5), run_time=1.0)
            vo.wait_until("but it sits apart")
            self.play(GrowFromCenter(apart), FadeIn(apart_l), run_time=0.6)
            self.play(Wiggle(apart, scale_value=1.1, run_time=0.7))

            vo.wait_until("Next, pausing")
            shown = collect(self, player.frame, frame, player.pause, player.bar, player.done, player.knob)
            self.play(FadeOut(collect(self, apart, apart_l)), FadeOut(frame_cap),
                      shown.animate.shift(RIGHT * shift_x), run_time=0.6)
            self.remove(shown)
            self.add(player.frame, frame, player.bar, player.done, player.knob, player.pause)
            self.play(ReplacementTransform(player.pause, paused), *dim(frame, opacity=0.3),
                      FadeIn(card, scale=0.95), run_time=0.7)
            vo.wait_until("should open it")
            self.add(ttt)                                    # in front of the window's fill
            self.play(FadeOut(lap, shift=RIGHT * 0.4), FadeOut(pg_cap),
                      ttt.animate.scale_to_fit_height(page_h).move_to(page_c),
                      ReplacementTransform(player.frame, win_frame), run_time=1.0)
            self.play(Create(win_out), FadeIn(win_tag, shift=DOWN * 0.1), FadeIn(merge_cap), run_time=0.6)
            vo.wait_until("in the same state")
            board = ttt.px_box(*TTT_BOARD_PX)
            same.move_to([page_c[0] - page_w / 2 - 0.08, win_frame.get_top()[1] + 0.02, 0])
            link = CurvedArrow(card.get_corner(UR) + LEFT * 0.4, board.get_top() + UP * 0.05, angle=-PI / 3,
                               color=TOOL, stroke_width=3)
            self.play(Create(link), FadeIn(same, scale=0.9),
                      Circumscribe(board, color=S.WHITE, buff=0.04, time_width=0.5), run_time=1.0)
            vo.wait_until("and keep your answer")
            saved.move_to(board.get_bottom() + DOWN * 0.42)
            self.play(FadeIn(saved, scale=0.8), run_time=0.5)
            self.play(pulse(saved, 1.12, run_time=0.6))
        self.wait(0.6)                                      # the finished window, before it folds

        # the card folds into its slot; the full board
        card4 = collect(self, win_frame, frame, player.bar, player.done, player.knob, paused, card, ttt, win_out,
                        win_tag, merge_cap, same, link, saved)
        self.play(FadeOut(card4, target_position=tabs[3].get_center(), scale=0.12),
                  *undim(tabs[0], tabs[1], tabs[2]), run_time=0.7)
        self.play(LaggedStart(*[pulse(t, 1.08, run_time=0.5) for t in tabs], lag_ratio=0.3), run_time=1.1)
        fade_out_all(self)
