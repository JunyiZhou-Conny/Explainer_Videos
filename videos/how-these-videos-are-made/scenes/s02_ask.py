"""S02 · What the user asked for.

Beats: the user (PINK), a researcher whose pile of papers grows faster than a clock ticks ->
the pile and the user move to the corner; a lineage row of GREY paper-style cards, 3Blue1Brown ->
Manim -> Manim Community Edition -> a BLUE card "explainers built by an AI agent", with the
Karpathy line (A05, as quoted) feeding the last card -> the user's own words come out of the user
icon as PINK quote cards (A06), "cognitive offloading" turns RED -> those two cards slide up
small, their captions merge into one; card 3 (a mentor), card 3b (never isolated) pointing at
the privacy video's real lineage map (A07, cropped to the map), card 4 (the next step) with
"interactive" in a dashed YELLOW outline + "idea · not built yet" -> the cards clear, the map
thumbnail stays and becomes request 1's picture; four PINK request cards (summaries) drop onto a
UTC date axis at their real request times (quotes.yaml `requests`), request 2 with A08.

Helpers defined here (not in common.py): broken() (line breaks in a quote without touching its
words), quote_glyphs() (the glyphs of a word in a quote card, to colour or outline it),
paper_pile(), lineage_card(), request_card().
"""

import datetime as dt

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import connect
from explainer.scene import VoiceScene

from common import (AGENT, BUG, DICTATED, IDEA, INK, NARRATION, PANEL, QUOTES, SUMMARIZED, TOOL, USER,
                    ai_badge, caption, clock, dim, emphasize, exhibit, fade_out_all, gather, label,
                    open_outline, open_tag, pulse, quote_card, role_icon, time_axis)

SAY = NARRATION["S02"]

# Real frames (1920 x 1080), cropped to the part the SHOW line points at. The map is cropped to its
# four papers (Warner 1965 -> disclosure control -> Sweeney 1997 -> Evfimievski 2003, the lanes
# between them), without the lane names and the year axis, so the names stay legible at MAP_W.
MAP, MAP_CROP = "dp_0230.png", (334, 80, 1750, 342)         # privacy video at 2:30: the lineage map
TTT, TTT_CROP = "ttt_0530.png", (60, 318, 1660, 771)        # tic-tac-toe video at 5:30: explore() + board
MAP_W = 6.8                                                 # the map in SAY[2] (as wide as the right half allows)

QUOTE_SIZE = 28
SMALL_F = 0.72                     # 28 pt cards slid up small -> 20.2 pt (never below 20)
CORNER_F = 0.78                    # 26 pt "the user" label in the corner -> 20.3 pt
MARK = "#FF00FE"                   # probe colour, never drawn
MAP_CAPTION = "papers are never isolated · the privacy video at 2:30"


def aspect(crop) -> float:
    """height / width of a pixel crop (x0, y0, x1, y1)."""
    return (crop[3] - crop[1]) / (crop[2] - crop[0])


# ------------------------------------------------------------------ helpers (this scene only)
def broken(text: str, *after: str) -> str:
    """`text` with a line break in place of the space after each given substring: the quoted
    words stay exactly as written (quote_card keeps explicit breaks)."""
    out = text
    for a in after:
        i = out.index(a) + len(a)
        assert out[i] == " ", (a, out[i:i + 6])
        out = out[:i] + "\n" + out[i + 1:]
    assert out.replace("\n", " ") == text
    return out


def quote_glyphs(card, word: str, size: float = QUOTE_SIZE) -> VGroup:
    """The glyphs of `word` inside a quote card's text. A twin of the text is built with the word
    coloured by t2c and the coloured glyphs are matched by index, so ligatures ('ffl' in
    'offloading') can't shift the count. Empty if the word isn't there (another language)."""
    q = card.quote
    try:
        twin = label(q.original_text, size, INK, line_spacing=1.0, t2c={word: MARK})
    except Exception:                                   # noqa: BLE001 (translated build)
        return VGroup()
    if len(twin.submobjects) != len(q.submobjects):
        return VGroup()
    mark = ManimColor(MARK).to_rgb()
    idx = [i for i, g in enumerate(twin.submobjects) if np.allclose(g.get_fill_color().to_rgb(), mark, atol=0.02)]
    return VGroup(*[q.submobjects[i] for i in idx])


def around(m, buff: float = 0.06) -> Rectangle:
    """An invisible rectangle over m (to Circumscribe a few glyphs)."""
    return Rectangle(width=m.width + 2 * buff, height=m.height + 2 * buff, stroke_width=0).move_to(m)


def paper_sheet(w: float = 0.92, h: float = 1.2) -> VGroup:
    """One GREY paper: a page with a title line and text lines."""
    page = RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color=TOOL, stroke_width=2)
    page.set_fill(PANEL, 1)
    left = -w * 0.32
    rows = VGroup()
    for k, frac in enumerate((0.38, 0.64, 0.64, 0.5, 0.64, 0.42)):
        y = h * 0.32 - k * h * 0.12 - (0.04 if k else 0)
        rows.add(Line([left, y, 0], [left + w * frac, y, 0], stroke_width=3 if k == 0 else 2, color=TOOL))
    return VGroup(page, rows.move_to(page).align_to(page, LEFT).shift(RIGHT * w * 0.18))


def paper_pile(n: int = 16, dy: float = 0.09) -> VGroup:
    """A pile of n papers, bottom first (deterministic jitter)."""
    rng = np.random.default_rng(7)
    pile = VGroup()
    for k in range(n):
        p = paper_sheet().rotate(rng.uniform(-0.09, 0.09))
        p.shift(RIGHT * rng.uniform(-0.06, 0.06) + UP * k * dy)
        pile.add(p)
    return pile


def tick(t: float) -> float:
    """A clock tick: the hand jumps in the first quarter of the step, then rests."""
    return smooth(min(1.0, t / 0.25))


def lineage_card(name: str, idea: str | None = None, color: str = TOOL, name_color: str = INK,
                 height: float | None = None) -> VGroup:
    """A paper_card-style card (bold name, one idea), left-aligned. .frame"""
    nm = label(name, 24, name_color, weight="BOLD", line_spacing=0.9)
    body = VGroup(nm)
    if idea:
        body.add(label(idea, 22, INK, line_spacing=0.9))
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    frame = RoundedRectangle(width=body.width + 0.4, height=height or body.height + 0.44, corner_radius=0.15,
                             stroke_color=color, stroke_width=2.5).set_fill(S.GREY_DARKER, 0.95)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.2)
    g = VGroup(frame, body)
    g.frame = frame
    return g


def fit_text(s: str, size: float, max_w: float, color: str = INK):
    """s word-wrapped to max_w (measured, not counted), as one left-aligned Text."""
    lines, cur = [], ""
    for w in s.split(" "):
        t = f"{cur} {w}".strip()
        if cur and label(t, size).width > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    return label("\n".join(lines), size, color, line_spacing=0.95)


def when(req) -> str:
    d = dt.date.fromisoformat(req["date"])
    return f"{d.strftime('%b')} {d.day} · {req['utc']} UTC"


def request_card(req, width: float, thumb_cap: str | None = None, thumb_aspect: float = 0.3) -> VGroup:
    """A PINK request card (a summary, not a quote): number, UTC time, the summary, and an empty
    slot for a real thumbnail (.slot, height = width * thumb_aspect, with its caption). .box .slot"""
    num = label(str(req["n"]), 30, USER, weight="BOLD")
    t = caption(when(req), 20)
    head = VGroup(num, t).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
    body = fit_text(req["text"], 22, width - 0.42)
    parts = VGroup(head, body)
    slot = None
    if thumb_cap:
        sw = width - 0.42
        slot = Rectangle(width=sw, height=sw * thumb_aspect, stroke_width=0).set_fill(opacity=0)
        cap = caption(thumb_cap, 20)
        parts.add(VGroup(slot, cap).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
    parts.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    b = RoundedRectangle(width=width, height=parts.height + 0.4, corner_radius=0.18, stroke_color=USER,
                         stroke_width=2.5).set_fill(USER, 0.12)
    parts.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.21)
    g = VGroup(b, parts)
    g.box, g.slot = b, slot
    return g


class TheAsk(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- one person, more papers than time
        user = role_icon("user", 1.25).move_to([-2.5, 0.3, 0])
        user_l = label("the user", 26, USER).next_to(user, DOWN, buff=0.25)
        pile = paper_pile(16)
        pile.move_to([-0.3, 0, 0]).align_to(user_l, DOWN).shift(UP * 0.05)
        clk = clock(0.55).move_to([2.1, 0.3, 0])

        # the lineage row (DIAGRAM) and the Karpathy line (REAL A05, as quoted)
        specs = [("3Blue1Brown", "explainer videos\nanimated with code", TOOL, INK),
                 ("Manim", "the Python library\nwritten for them", TOOL, INK),
                 ("Manim\nCommunity\nEdition", "v0.21.0,\nused here", TOOL, INK),
                 ("explainers built\nby an AI agent", None, AGENT, AGENT)]
        h = max(lineage_card(*sp).frame.height for sp in specs)
        cards = [lineage_card(*sp, height=h) for sp in specs]
        row = VGroup(*cards).arrange(RIGHT, buff=0.55).move_to([0, -1.2, 0])
        badge = ai_badge(0.42)
        badge.move_to(cards[3].frame.get_corner(UR) + np.array([-badge.width / 2 - 0.15, 0, 0]))
        cards[3].add(badge)
        arrows = [connect(cards[k].frame, cards[k + 1].frame, buff=0.06) for k in range(3)]
        karp = quote_card(QUOTES["karpathy"]["screen"].replace("bespoke ", "bespoke\n", 1)
                          .replace("generated ", "generated\n", 1), cap=None, color=TOOL, size=26, chars=60)
        karp.move_to([0, 2.05, 0]).align_to(cards[3].frame, RIGHT)
        kcap_text = QUOTES["captions"]["karpathy"].replace(", ", ",\n", 1).replace(" request ", " request\n", 1)
        kcap = caption(kcap_text, 20).next_to(karp.box, DOWN, buff=0.12).align_to(karp.box, LEFT)
        kx = cards[3].frame.get_right()[0] - 1.1          # clear of the caption (left) and the AI badge (right)
        k_arrow = Arrow([kx, karp.box.get_bottom()[1], 0], [kx, cards[3].frame.get_top()[1], 0], buff=0.08,
                        color=TOOL, stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.3)
        corner_at = np.array([-5.15, 2.45, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(user, shift=UP * 0.2), FadeIn(user_l), run_time=0.8)
            vo.wait_until("a researcher")
            self.play(FadeIn(clk, scale=0.8), run_time=0.4)
            for k in range(4):                      # four papers land for every tick of the clock
                self.play(Rotate(clk.minute, -PI / 6, about_point=clk.face.get_center(), rate_func=tick),
                          LaggedStart(*[FadeIn(p, shift=DOWN * 0.35) for p in pile[4 * k:4 * k + 4]],
                                      lag_ratio=0.3),
                          run_time=0.85)
            vo.wait_until("The look comes")
            corner = gather(self, user, user_l, *pile)
            self.play(FadeOut(clk, scale=0.8), corner.animate.scale(CORNER_F).move_to(corner_at), run_time=0.8)
            self.play(FadeIn(cards[0], shift=RIGHT * 0.3), run_time=0.6)
            vo.wait_until("whose videos")
            self.play(GrowArrow(arrows[0]), FadeIn(cards[1], shift=RIGHT * 0.3), run_time=0.8)
            vo.wait_until("where every frame")
            self.play(GrowArrow(arrows[1]), FadeIn(cards[2], shift=RIGHT * 0.3), run_time=0.8)
            vo.wait_until("The idea for this")
            self.play(GrowArrow(arrows[2]), FadeIn(cards[3], shift=RIGHT * 0.3), run_time=0.8)
            vo.wait_until("came from a post")
            self.play(FadeIn(karp, shift=DOWN * 0.2), run_time=0.8)
            self.play(GrowArrow(k_arrow), run_time=0.5)
            vo.wait_until("as quoted")
            self.play(FadeIn(kcap, shift=UP * 0.1), pulse(corner, 1.08, run_time=0.7), run_time=0.7)

        # ---------------------------------------------------------- the user's own words
        c1 = quote_card(broken(QUOTES["s02_card1"]["screen"], "… it takes", "pain … to"), DICTATED,
                        size=QUOTE_SIZE, chars=80)
        c2 = quote_card(broken(QUOTES["s02_card2"]["screen"], "at the same", "a lot of"), DICTATED,
                        size=QUOTE_SIZE, chars=80)
        speaker_at = np.array([-5.45, 0.15, 0])
        c1.move_to([0, 1.35, 0]).align_to([-4.35, 0, 0], LEFT)
        c2.move_to([0, -1.25, 0]).align_to([-4.35, 0, 0], LEFT)
        offload = quote_glyphs(c2, "cognitive offloading")

        with self.voiceover(SAY[1]) as vo:
            lineage = gather(self, *cards, *arrows, karp, kcap, k_arrow)
            speaker = VGroup(user, user_l)
            self.play(FadeOut(lineage, shift=DOWN * 0.3), FadeOut(pile, shift=DOWN * 0.2),
                      speaker.animate.scale(1 / CORNER_F).move_to(speaker_at), run_time=0.9)
            vo.wait_until("our brain is")
            self.play(FadeIn(c1, target_position=user.get_center(), scale=0.3), run_time=0.8)
            vo.wait_until("AI is patient")
            self.play(FadeIn(c2, target_position=user.get_center(), scale=0.3), run_time=0.8)
            vo.wait_until("cognitive offloading")
            if len(offload):
                self.play(offload.animate.set_color(BUG), run_time=0.5)
                self.play(Indicate(offload, color=BUG, scale_factor=1.12), run_time=0.8)

        # ---------------------------------------------------------- a mentor, a map, the next step
        # cards 1 and 2 (and their speaker) slide up small into one row
        s_user, s1, s2 = (VGroup(user, user_l).copy().scale(CORNER_F),
                          VGroup(c1.box, c1.quote).copy().scale(SMALL_F),
                          VGroup(c2.box, c2.quote).copy().scale(SMALL_F))
        top = VGroup(s_user, s1, s2).arrange(RIGHT, buff=0.32).move_to([0, 2.72, 0])
        shared_cap = caption(DICTATED).move_to([0, -3.38, 0]).align_to([6.35, 0, 0], RIGHT)

        c3 = quote_card(broken(QUOTES["s02_card3"]["screen"], "explainer video"), None, size=QUOTE_SIZE, chars=80)
        c3.move_to([0, 0.95, 0]).align_to([-6.3, 0, 0], LEFT)
        c3b = quote_card(QUOTES["s02_card3b"]["screen"], None, size=24, chars=80)
        c3b.next_to(c3, DOWN, buff=0.2).align_to(c3, LEFT)
        # the map sits between cards 3 and 3b, right of them, as wide as the right half allows
        thumb = exhibit(MAP, width=MAP_W, crop=MAP_CROP)
        thumb.move_to([0, 0.6, 0]).align_to([6.45, 0, 0], RIGHT)
        tcap = caption(MAP_CAPTION, 20)
        if tcap.width > thumb.width:
            tcap = caption(MAP_CAPTION.replace(" · ", "\n"), 20)
        tcap.next_to(thumb, DOWN, buff=0.12).align_to(thumb, LEFT)
        # low on the map's left edge, so the arrow passes under card 3's corner
        link = Arrow(c3b.box.get_right(), thumb.frame.get_corner(DL) + UP * 0.2, buff=0.12, color=TOOL,
                     stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.25)
        c4 = quote_card(broken(QUOTES["s02_card4"]["screen"], "I feel like it's", "something interactive,"),
                        None, size=QUOTE_SIZE, chars=80)
        c4.move_to([0, -2.1, 0]).align_to([-6.3, 0, 0], LEFT)
        # the comma touches the word, so the outline takes it in (an outline edge through it reads badly)
        inter = quote_glyphs(c4, "interactive,")
        if not len(inter):
            inter = quote_glyphs(c4, "interactive")
        make = quote_glyphs(c4, "actually create")

        with self.voiceover(SAY[2]) as vo:
            # card 1 leaves first; card 2 swings round below-right of it, so they never cross
            self.play(Transform(VGroup(user, user_l), s_user),
                      LaggedStart(Transform(VGroup(c1.box, c1.quote), s1),
                                  Transform(VGroup(c2.box, c2.quote), s2, path_arc=0.7), lag_ratio=0.35),
                      FadeOut(c1.caption), ReplacementTransform(c2.caption, shared_cap),     # one caption for all the cards
                      run_time=1.2)
            self.play(*dim(c1.box, c1.quote, c2.box, c2.quote, opacity=0.5),
                      FadeIn(c3, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("showing how papers")
            self.play(FadeIn(thumb, shift=LEFT * 0.2), FadeIn(tcap, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("because they're never")
            self.play(FadeIn(c3b, shift=UP * 0.15), run_time=0.5)
            self.play(GrowArrow(link), run_time=0.5)
            vo.wait_until("And video is only")
            self.play(FadeIn(c4, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("something interactive")
            itag = open_tag(IDEA)
            if len(inter):                          # the word itself, outlined, its tag right beside it
                outline = open_outline(inter, buff=0.07, stroke=3)
                itag.next_to(outline, RIGHT, buff=0.3)
                self.play(Create(outline), run_time=0.6)
            else:                                   # word not found (a translated build): tag the card
                outline = VMobject()
                itag.next_to(c4.box, RIGHT, buff=0.2)
            self.play(FadeIn(itag, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("where the learner")
            if len(make):
                self.play(emphasize(around(make), run_time=1.1))

        # ---------------------------------------------------------- then came four requests
        reqs = QUOTES["requests"]
        W, GAP = 3.15, 0.12
        # each thumbnail slot takes its own picture's aspect (the map is a wide strip, A08 is not)
        caps = {1: ("privacy video · 2:30", aspect(MAP_CROP)), 2: ("tic-tac-toe video · 5:30", aspect(TTT_CROP))}
        rcards = [request_card(r, W, *caps.get(r["n"], (None,))) for r in reqs]
        VGroup(*rcards).arrange(RIGHT, buff=GAP, aligned_edge=DOWN).move_to([0, 0, 0])
        base_y = -2.35
        for rc in rcards:
            rc.shift(UP * (base_y - rc.get_bottom()[1]))
        ttt = exhibit(TTT, width=rcards[1].slot.width, crop=TTT_CROP).move_to(rcards[1].slot)
        rcards[1] = Group(rcards[1], ttt)
        rcards[1].box = rcards[1][0].box
        axis = time_axis("2026-10-04 00:00", "2026-10-08 00:00", width=12.0).move_to([0, -2.9, 0])
        days = VGroup()
        for d in range(4, 9):                       # midnight ticks, day names in the middle of each day
            x = axis.x_of(f"2026-10-{d:02d} 00:00")
            days.add(Line([x, -3.02, 0], [x, -2.78, 0], color=TOOL, stroke_width=2))
            if d < 8:
                days.add(caption(f"Oct {d}", 20).move_to([axis.x_of(f"2026-10-{d:02d} 12:00"), -3.24, 0]))
        pins = []
        for r, rc in zip(reqs, rcards):
            p = axis.point(f"{r['date']} {r['utc']}")
            dot = Dot(p, radius=0.07, color=USER)
            lead = Line(rc.box.get_bottom(), p, color=USER, stroke_width=2.5)
            pins.append(VGroup(lead, dot))
        heading = label(SUMMARIZED, 26, TOOL)
        user_at = np.array([-5.75, 2.78, 0])
        anchors = ["A privacy paper", "A tic-tac-toe video", "Chinese versions of both", "And this video"]

        with self.voiceover(SAY[3]) as vo:
            speaker = VGroup(user, user_l)
            others = gather(self, c1.box, c1.quote, c2.box, c2.quote, shared_cap, c3, c3b, link, c4, tcap,
                            itag, *([outline] if len(inter) else []))
            heading.next_to(speaker.copy().move_to(user_at), RIGHT, buff=0.35).shift(UP * 0.1)
            self.play(FadeOut(others, shift=UP * 0.3), speaker.animate.move_to(user_at), run_time=0.8)
            self.play(Create(axis.line), FadeIn(days), FadeIn(heading, shift=RIGHT * 0.2), run_time=0.8)
            for k, (rc, pin, phrase) in enumerate(zip(rcards, pins, anchors)):
                vo.wait_until(phrase)
                anims = [FadeIn(rc, shift=DOWN * 0.7)]
                if k == 0:                          # the map from a moment ago is request 1's picture
                    anims.append(thumb.animate.scale_to_fit_width(rc.slot.width).move_to(rc.slot))
                self.play(*anims, run_time=0.8)
                self.play(Create(pin[0]), FadeIn(pin[1], scale=0.5), run_time=0.45)
                if k == 0:                          # "which the user hadn't read"
                    vo.wait_until("which the user")
                    self.play(pulse(speaker, 1.1, run_time=0.7))
                if k == 2:                          # "of both"
                    self.play(*[emphasize(rcards[j].box, circle=True, run_time=0.9) for j in (0, 1)])
            self.play(pulse(rcards[3], 1.05, run_time=0.6))
        self.wait(0.4)
        fade_out_all(self)

