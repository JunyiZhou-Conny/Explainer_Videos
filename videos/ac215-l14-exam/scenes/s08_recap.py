"""S08 · Seven rules for Tuesday (recap of the AC215 L14 exam edition). Lecture: 14 · 16; 15 · 16–17.

Beats (script.md "## S08", one voiceover block each):
0. The exam map (slots 1-5 filled) fades in at the top and expands into seven GREY-outlined rule
   rows: slot 1 -> row 1, slot 2 -> rows 2-3, slot 3 -> row 4, slot 4 -> row 5, slot 5 -> rows 6-7.
   Each row carries its number and set-piece icon (recap_icon: V1's strips, V2's meters, the
   cold-start puff, V3's grid, V4's doors, V5's gear, V6's plug), dimmed while the row is empty.
   At "One" row 1's text writes in (its icon brightens); at "If it listens" the icon's service bar
   pulses, at "if it runs and exits" its job bar. Row 2 at "Two", row 3 at "Three"; at "and zero
   idle cost" the puff icon pulses.
1. Row 4 at "Four" ("function = source + requirements + entry point (Google builds the image) ·
   service = your image"); the grid icon pulses at "a service is your own image". Row 5 at "Five"
   ("who may call (public access) ≠ who it runs as (service account · no key)"); the doors icon
   pulses at "needs no key".
2. Row 6 at "Six" ("preprocess at the endpoint: one deployment updates or rolls back every
   client"); row 7 at "Seven" ("register the serving function (`serve`) = preprocess, then model ·
   the platform calls the name you register"). At "because the platform" all seven row outlines
   glow YELLOW once, top to bottom.
3. lref(15, "16–17"). The list shrinks left: each row becomes a compact row (number, icon, a short
   20 pt label), x -6.5..-1.6. Right: a two-column card (our drawing of the comparison's last row,
   header "rule of thumb"), "Vertex AI Online Prediction · serve a trained model in production"
   (column written in at "Vertex AI to serve") vs "Cloud Run · ML as part of a broader app" (at
   "Cloud Run when"). At "And remember the costs" the tag swaps to lref(14, "16") and three GREY
   chips "vendor lock-in", "cold starts", "harder debugging" write in under the card as named; at
   "cold starts" compact row 3 (the puff) pulses too.
4. Everything fades except a small GREY line "AC215 · Lecture 14 · exam edition" in the middle; at
   "Good luck" it pulses gently, then fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    RoundedRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    there_and_back,
)

from explainer import style as S
from explainer.scene import VoiceScene

from common import (
    CAPTION,
    CLOUD,
    COST,
    INK,
    SANS,
    NARRATION,
    SAFE_X,
    SAFE_Y,
    TURN,
    ExamMap,
    box,
    chip,
    fit_rows,
    guard,
    lref,
    lref_swap,
    recap_icon,
    sans,
)

SAY = NARRATION["S08"]

RULES = (
    "read the lifecycle: listens → service · runs and exits → job (on demand or Cloud Scheduler)",
    "idle time costs only what is always on (a VM · min instances ≥ 1)",
    "pay-per-use bills invocations + execution time · zero idle cost buys cold starts",
    "function = source + requirements + entry point (Google builds the image) · service = your image",
    "who may call (public access) ≠ who it runs as (service account · no key)",
    "preprocess at the endpoint: one deployment updates or rolls back every client",
    "register the serving function (`serve`) = preprocess, then model · "
    "the platform calls the name you register",
)
SHORT = (
    "service or job",
    "idle: always-on pays",
    "pay per use · cold starts",
    "function vs service",
    "who calls ≠ runs as",
    "preprocess at endpoint",
    "register serve",
)
SLOT_OF_ROW = (1, 2, 2, 3, 4, 5, 5)          # which exam-map slot each rule row grows from

ROW_X0, ROW_X1 = -6.5, 6.5                   # the full list
TEXT_X = -4.75                               # rule text starts here
TEXT_W = ROW_X1 - 0.2 - TEXT_X
LIST_TOP = 3.45
ROW_GAP = 0.1
CMP_X0, CMP_X1 = -6.5, -1.55                 # the compact list (beat 3)
CMP_H, CMP_GAP = 0.6, 0.14
CARD_X0, CARD_X1 = -1.2, 6.5                 # the comparison card
DIM_ICON = 0.35


def inside_frame(*mobs):
    for m in mobs:
        guard(m.get_left()[0] >= -SAFE_X - 1e-6 and m.get_right()[0] <= SAFE_X + 1e-6,
              f"x out of frame: {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f}")
        guard(m.get_bottom()[1] >= -SAFE_Y - 1e-6 and m.get_top()[1] <= SAFE_Y + 1e-6,
              f"y out of frame: {m.get_bottom()[1]:.2f}..{m.get_top()[1]:.2f}")


def apart(a, b, gap: float = 0.05):
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    guard(sep, "overlap")


def build_rows():
    """The seven full rows: .frame .num .icon .text per row (not added)."""
    texts = [fit_rows(r, TEXT_W, 22) for r in RULES]
    heights = [max(0.64, t.height + 0.26) for t in texts]
    rows = VGroup()
    total = sum(heights) + ROW_GAP * (len(heights) - 1)
    y = min(LIST_TOP, total / 2)                 # centred vertically (the map is gone)
    for k, (t, h) in enumerate(zip(texts, heights), start=1):
        fr = RoundedRectangle(width=ROW_X1 - ROW_X0, height=h, corner_radius=0.12, stroke_color=S.GREY,
                              stroke_width=2).set_fill(opacity=0)
        fr.move_to([(ROW_X0 + ROW_X1) / 2, y - h / 2, 0])
        num = S.text(str(k), CAPTION + 4, INK, font=SANS, weight="BOLD")
        num.move_to([ROW_X0 + 0.32, fr.get_center()[1], 0])
        ic = recap_icon(k)
        ic.move_to([ROW_X0 + 1.15, fr.get_center()[1], 0])
        t.move_to([TEXT_X + t.width / 2, fr.get_center()[1], 0])
        r = VGroup(fr, num, ic, t)
        r.frame, r.num, r.icon, r.text = fr, num, ic, t
        rows.add(r)
        y -= h + ROW_GAP
    return rows


def compact_rows():
    """Beat 3: the same seven rows, short (frame, num, icon, short label) at the left."""
    n = len(SHORT)
    total = n * CMP_H + (n - 1) * CMP_GAP
    top = total / 2 - 0.25
    out = VGroup()
    for k, s in enumerate(SHORT, start=1):
        cy = top - CMP_H / 2 - (k - 1) * (CMP_H + CMP_GAP)
        fr = RoundedRectangle(width=CMP_X1 - CMP_X0, height=CMP_H, corner_radius=0.1, stroke_color=S.GREY,
                              stroke_width=2).set_fill(opacity=0).move_to([(CMP_X0 + CMP_X1) / 2, cy, 0])
        num = S.text(str(k), CAPTION + 4, INK, font=SANS, weight="BOLD").move_to([CMP_X0 + 0.28, cy, 0])
        ic = recap_icon(k, h=0.34).move_to([CMP_X0 + 0.95, cy, 0])
        t = sans(s, CAPTION, INK)
        t.move_to([CMP_X0 + 1.55 + t.width / 2, cy, 0])
        guard(t.get_right()[0] <= CMP_X1 - 0.1, f"compact label {s!r} too wide")
        r = VGroup(fr, num, ic, t)
        r.frame, r.num, r.icon, r.text = fr, num, ic, t
        out.add(r)
    return out


def compare_card():
    """Our drawing of the comparison's last row (Lecture 15, slides 16–17): two BLUE columns."""
    w = CARD_X1 - CARD_X0
    col_w = (w - 0.6) / 2
    head = sans("rule of thumb", CAPTION, S.GREY)
    cols = VGroup()
    for title, body in (("Vertex AI Online Prediction", "serve a trained model in production"),
                        ("Cloud Run", "ML as part of a broader app")):
        t = fit_rows(title, col_w - 0.3, 24, CLOUD)
        b = fit_rows(body, col_w - 0.3, 22, INK)
        cols.add(VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.22))
    body_h = max(c.height for c in cols)
    h = head.height + body_h + 0.85
    fr = box(w, h, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    fr.move_to([(CARD_X0 + CARD_X1) / 2, 0, 0])
    head.move_to(fr.get_corner(UP + LEFT) + np.array([0.3 + head.width / 2, -0.2 - head.height / 2, 0]))
    top = head.get_bottom()[1] - 0.25
    xs = (CARD_X0 + 0.3, CARD_X0 + 0.3 + col_w + 0.3)
    for c, x in zip(cols, xs):
        c.move_to([x + c.width / 2, top - c.height / 2, 0])
    sep = Line([xs[1] - 0.18, top + 0.05, 0], [xs[1] - 0.18, fr.get_bottom()[1] + 0.2, 0],
               color=S.GREY_DARK, stroke_width=2)
    g = VGroup(fr, head, sep, cols)
    g.frame, g.head, g.sep, g.cols = fr, head, sep, cols
    return g


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == 5, len(SAY)

        m = ExamMap(filled=(1, 2, 3, 4, 5))
        rows = build_rows()
        inside_frame(rows)
        guard(rows[-1].frame.get_bottom()[1] >= -SAFE_Y, "rule list too tall")
        for a, b in zip(rows[:-1], rows[1:]):
            apart(a.frame, b.frame, 0.05)
        for r in rows:
            guard(r.text.get_left()[0] >= r.icon.get_right()[0] + 0.15, "icon reaches the rule text")
            guard(r.text.get_right()[0] <= r.frame.get_right()[0] - 0.1, "rule text leaves its row")

        # ========================================================== 0. map -> seven rows; rules 1-3
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(m, shift=DOWN * 0.1), run_time=0.6)
            grow = []
            for k, r in enumerate(rows):
                slot = m.slots[SLOT_OF_ROW[k] - 1]
                grow.append(TransformFromCopy(slot.frame, r.frame))
                r.icon.set_opacity(DIM_ICON)
                r.num.set_opacity(DIM_ICON)
            self.play(FadeOut(m, shift=UP * 0.2), LaggedStart(*grow, lag_ratio=0.08), run_time=1.3)
            self.play(LaggedStart(*[FadeIn(VGroup(r.num, r.icon)) for r in rows], lag_ratio=0.08), run_time=0.7)

            def write(r):
                return [FadeIn(r.text, shift=RIGHT * 0.15), r.icon.animate.set_opacity(1),
                        r.num.animate.set_opacity(1), r.frame.animate.set_stroke(S.GREEN, 2.5)]

            vo.wait_until("One")
            self.play(*write(rows[0]), run_time=0.8)
            vo.wait_until("If it listens")
            self.play(Indicate(rows[0].icon[0:2], color=TURN, scale_factor=1.3), run_time=0.8)
            vo.wait_until("if it runs and exits")
            self.play(Indicate(rows[0].icon[2:4], color=TURN, scale_factor=1.3), run_time=0.8)
            vo.wait_until("Two")
            self.play(*write(rows[1]), run_time=0.8)
            vo.wait_until("always on")
            self.play(Indicate(rows[1].icon, color=COST, scale_factor=1.25), run_time=0.7)
            vo.wait_until("Three")
            self.play(*write(rows[2]), run_time=0.8)
            vo.wait_until("and zero idle cost")
            self.play(Indicate(rows[2].icon, color=TURN, scale_factor=1.3), run_time=vo.remaining(0.8))

        # ========================================================== 1. rules 4-5
        with self.voiceover(SAY[1]) as vo:
            vo.wait_until("Four")
            self.play(*write(rows[3]), run_time=0.8)
            vo.wait_until("and Google builds the image")
            self.play(Indicate(rows[3].icon[0:2], color=TURN, scale_factor=1.3), run_time=0.7)
            vo.wait_until("a service is your own image")
            self.play(Indicate(rows[3].icon[2:4], color=TURN, scale_factor=1.3), run_time=0.7)
            vo.wait_until("Five")
            self.play(*write(rows[4]), run_time=0.8)
            vo.wait_until("needs no key")
            self.play(Indicate(rows[4].icon, color=TURN, scale_factor=1.3), run_time=vo.remaining(0.8))

        # ========================================================== 2. rules 6-7, all rows glow
        with self.voiceover(SAY[2]) as vo:
            vo.wait_until("Six")
            self.play(*write(rows[5]), run_time=0.8)
            vo.wait_until("rolls back every client")
            self.play(Indicate(rows[5].icon, color=TURN, scale_factor=1.3), run_time=0.7)
            vo.wait_until("Seven")
            self.play(*write(rows[6]), run_time=0.8)
            vo.wait_until("because the platform")
            glow = VGroup(*[r.frame.copy().set_fill(opacity=0).set_stroke(TURN, 6, opacity=0) for r in rows])
            self.add(glow)
            self.play(LaggedStart(*[g.animate(rate_func=there_and_back).set_stroke(opacity=1) for g in glow],
                                  lag_ratio=0.12), run_time=2.0)
            self.remove(glow)
            vo.wait_until("the name you register")
            self.play(Indicate(rows[6].icon, color=TURN, scale_factor=1.3), run_time=vo.remaining(0.8))

        # ========================================================== 3. which to use; slide 16's costs
        small = compact_rows()
        for r in small:
            r.frame.set_stroke(S.GREEN, 2.5)
        card = compare_card()
        chips = VGroup(*[chip(s, S.GREY, CAPTION + 2) for s in ("vendor lock-in", "cold starts", "harder debugging")])
        chips.arrange(RIGHT, buff=0.25)
        chips.next_to(card, DOWN, buff=0.45)
        chips.set_x((CARD_X0 + CARD_X1) / 2)
        lr_probe = lref(15, "16–17")
        inside_frame(small, card, chips)
        apart(card, chips, 0.2)
        guard(small.get_right()[0] + 0.25 <= card.get_left()[0], "compact list reaches the card")
        guard(card.get_top()[1] <= lr_probe.get_bottom()[1] - 0.3, "card reaches the lecture tag")
        guard(chips.width <= CARD_X1 - CARD_X0, "chips wider than the card")

        with self.voiceover(SAY[3]) as vo:
            shrink = []
            for r, s in zip(rows, small):
                shrink += [Transform(r.frame, s.frame), Transform(r.num, s.num), Transform(r.icon, s.icon),
                           FadeOut(r.text, shift=LEFT * 0.3), FadeIn(s.text, shift=LEFT * 0.3)]
            self.play(*shrink, run_time=1.3)
            lr = lref_swap(self, None, 15, "16–17")
            vo.wait_until("rule of thumb")
            self.play(FadeIn(card.frame), FadeIn(card.head), FadeIn(card.sep), run_time=0.6)
            vo.wait_until("Vertex AI to serve")
            self.play(FadeIn(card.cols[0], shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("Cloud Run when")
            self.play(FadeIn(card.cols[1], shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("And remember the costs")
            lr = lref_swap(self, lr, 14, "16")
            vo.wait_until("vendor lock-in")
            self.play(FadeIn(chips[0], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("cold starts")
            self.play(FadeIn(chips[1], shift=UP * 0.1), Indicate(rows[2].icon, color=TURN, scale_factor=1.3), run_time=0.7)
            vo.wait_until("harder debugging")
            self.play(FadeIn(chips[2], shift=UP * 0.1), run_time=vo.remaining(0.5))

        # ========================================================== 4. sign-off
        sign = sans("AC215 · Lecture 14 · exam edition", CAPTION + 2, S.GREY)
        with self.voiceover(SAY[4]) as vo:
            rest = [mob for mob in self.mobjects]
            self.play(*[FadeOut(mob) for mob in rest], FadeIn(sign, shift=UP * 0.1), run_time=1.2)
            vo.wait_until("Good luck")
            self.play(Indicate(sign, color=INK, scale_factor=1.05), run_time=vo.remaining(1.0))
        self.wait(0.8)
        self.play(FadeOut(sign), run_time=0.8)
        self.wait(0.3)
