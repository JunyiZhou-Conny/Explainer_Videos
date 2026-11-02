"""S06 · Autoscaling meets the connection budget (V5: slots, pools, the max-replicas rule).
Lecture: L16 43–45, 52, 55, 67.

Beats (script.md "## S06", one voiceover block each):
 0  LECTURE 16 · 52. Slide 52's four boxes (Autoscaler): Signal → PURPLE Policy (target · min · max)
    → Desired count → Capacity. A GRAY traffic line rises; the desired count ticks 3 → 4 → 5; the
    YELLOW caption "Downstream limits still bound the result." writes in.
 1  The boxes fold into a PURPLE autoscaler strip on top (left). Right: the BLUE database panel of
    100 socket slots (SlotGrid, `illustration`). ORANGE plugs fill row 0 (10 slots), labelled
    "admin console 4 · batch job 6".
 2  Replica 1 (TEAL, GREEN "pool 20") appears beside its two grid rows and plugs 20 PINK pipes in.
    CODE(cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py: 56–57) at the bottom, line 57 lit,
    the GRAY chip "the course's vector DB client · stands in for a SQL connection pool" above it.
 3  The panel leaves; the autoscaler stamps out replicas 2, 3, 4 (count 2 → 4), each plugs 20 pipes
    (90 used). Replica 5: 10 pipes reach the last free row, 10 hit full slots and spark RED;
    "too many connections"; its requests turn RED while its GRAY CPU gauge reads low.
 4  Replica 5 leaves. The rule assembles from the picture: the grid title → "limit", the ORANGE row
    → "other clients", replica 1's pool → "connections per replica", inside mono ⌊( … ) ÷ … ⌋ with
    YELLOW "round down"; below it ⌊(100 − 10) ÷ 20⌋ = ⌊4.5⌋ = 4 piece by piece. The strip's max
    turns to 4; a YELLOW cap line draws under replica 4 across the grid.
 5  LECTURE 16 · 45, 55, 67. The formula leaves. Three GRAY chips (slides 45, 55, 67) at the bottom;
    three relief valves on the left: "connection pooler or smaller pools" and "bigger DB tier" (GOLD
    price tag) light GREEN, "raise max only" turns RED.
 6  The canvas clears. PONDER P3 (McqCard, `illustration`): the stem is read; the 10 s timer after.
 7  Reveal: B fills YELLOW ✓ with the note 30 + 10 × 15 = 180 ≤ 200.
 8  RED reasons under A, C (GOLD price tag beside it), D as the SAY reaches each; the card fades.
 9  TAKEAWAY, row by row as spoken (the rule in words, "rounded down": the serif has no ⌊ ⌋ and a
    mono span cannot wrap across rows); then an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    GrowFromPoint,
    Indicate,
    LaggedStart,
    Line,
    ShowPassingFlash,
    VGroup,
    VMobject,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S06"]

RAG = "cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py"
assert source_line(RAG, 57).startswith("client = chromadb.HttpClient("), source_line(RAG, 57)
assert source_line(RAG, 56).strip() == "# Connect to chroma DB", source_line(RAG, 56)

LIMIT, OTHERS, POOL = 100, 10, 20          # V5 illustration numbers (script.md "V5 numbers")
assert max_replicas(LIMIT, OTHERS, POOL) == 4
assert formula_text(LIMIT, OTHERS, POOL) == "⌊(100 − 10) ÷ 20⌋ = ⌊4.5⌋ = 4"
# P3 (script.md "P3 numbers"): pools of 15, others 30, 10 replicas -> 180 needed; smallest tier 200
assert 30 + 10 * 15 == 180 and 150 < 180 <= 200 < 250 and max_replicas(100, 30, 15) < 10

STEM = ("Each API replica opens a pool of **15** connections. Other clients hold **30**. At peak the "
        "service needs **10** replicas. Which is the smallest database tier that works?")
OPTIONS = ["150 connections",
           "200 connections",
           "250 connections",
           "keep the 100-connection tier and raise the autoscaler maximum to 10"]
TAKEAWAY = ("DB connection limit given → max replicas = (limit − other clients) ÷ connections per "
            "replica, rounded down · "
            "set it as the max: the autoscaler doesn't know the DB limit")

SAFE_L, SAFE_R, SAFE_B, SAFE_T = -6.6, 6.6, -3.6, 3.6
REP_W, REP_H = 2.8, 0.5


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def inside(m, name="", t=SAFE_T):
    guard(m.get_left()[0] >= SAFE_L and m.get_right()[0] <= SAFE_R and m.get_bottom()[1] >= SAFE_B
          and m.get_top()[1] <= t, f"{name} outside the safe frame: {m.get_left()}, {m.get_right()}, "
          f"{m.get_bottom()}, {m.get_top()}")


def apart(a, b, name="", buff=0.03):
    """a and b must not overlap (bounding boxes)."""
    ok = (a.get_right()[0] + buff <= b.get_left()[0] or b.get_right()[0] + buff <= a.get_left()[0]
          or a.get_top()[1] + buff <= b.get_bottom()[1] or b.get_top()[1] + buff <= a.get_bottom()[1])
    guard(ok, f"overlap: {name}")


def flash(mob, color=TURN, k=1.12, run_time=0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def outline_flash(fr, color=TURN):
    """A light running round a card's outline (Indicate would flood a filled card with colour)."""
    ring_ = fr.copy().set_fill(opacity=0).set_stroke(color, width=6, opacity=1)
    return ShowPassingFlash(ring_, time_width=0.6)


def boxed(mobs, color, pad_x=0.35, pad_y=0.22, fill_opacity=0.95):
    """mobs on a rounded card of `color` (dark fill)."""
    body = mobs if isinstance(mobs, VGroup) else VGroup(mobs)
    fr = box(body.width + 2 * pad_x, body.height + 2 * pad_y, color, fill=S.BG, fill_opacity=fill_opacity)
    fr.move_to(body)
    g = VGroup(fr, body)
    g.frame, g.body = fr, body
    return g


def rep_bar(i, pool=POOL):
    """A replica as one slim row (its height matches two grid rows, so its pipes run level):
    TEAL frame, "replica i", GREEN pool pill. .frame .pool .name; pipes start at the right edge."""
    fr = box(REP_W, REP_H, CTR, fill=S.BG, fill_opacity=0.95, stroke=3, radius=0.1)
    nm = label(f"replica {i}", CAPTION, INK)
    pill = RoundedRectangle(width=1.15, height=0.34, corner_radius=0.08, stroke_color=OWN, stroke_width=2) \
        .set_fill(OWN, 0.25)
    pt = label(f"pool {pool}", CAPTION, OWN).move_to(pill)
    place(nm, left=fr.get_left()[0] + 0.18, cy=fr.get_center()[1])
    pool_g = VGroup(pill, pt)
    place(pool_g, right=fr.get_right()[0] - 0.12, cy=fr.get_center()[1])
    g = VGroup(fr, nm, pool_g)
    g.frame, g.name, g.pool = fr, nm, pool_g
    return g


class ConnectionBudget(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0 · slide 52: signal → policy → count
        au = Autoscaler(count=3, max_="?")
        au.move_to([0, 0.95, 0])
        cap0 = au.caption()
        inside(au, "autoscaler", t=3.05)
        traffic_l = note("traffic")
        sx = au.boxes["signal"].get_center()[0]
        pts = [[sx - 1.4 + 0.4 * k, y, 0] for k, y in
               enumerate((-3.15, -2.95, -3.0, -2.55, -2.6, -2.05, -2.1, -1.6, -1.45))]
        place(traffic_l, left=sx + 2.15, bottom=-3.25)
        segs = []
        for a, b in ((0, 3), (3, 6), (6, 9)):
            seg = VMobject(stroke_color=S.GREY, stroke_width=4).set_points_as_corners(pts[a:b + 1] if b < 9 else pts[a:])
            segs.append(seg)
        base = Line([sx - 1.5, -3.3, 0], [sx + 2.0, -3.3, 0], color=S.GREY, stroke_width=2, stroke_opacity=0.6)
        graph = VGroup(base, *segs, traffic_l)
        feed = arrow_([sx, -1.2, 0], [sx, au.boxes["signal"].get_bottom()[1] - 0.06, 0], S.GREY, stroke=3)
        inside(graph, "traffic graph")
        apart(graph, cap0, "traffic / caption")
        apart(feed, cap0, "feed arrow / caption")
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, None, 16, "52")
            vo.wait_until("An autoscaler")
            self.play(FadeIn(au, shift=RIGHT * 0.15, lag_ratio=0.1), run_time=1.4)
            self.play(Create(base), FadeIn(traffic_l), run_time=0.5)
            vo.wait_until("measures a signal")
            self.play(Create(segs[0]), flash(au.boxes["signal"], TURN, 1.05), run_time=0.8)
            vo.wait_until("applies a policy")
            self.play(flash(au.boxes["policy"], TOOL, 1.06), run_time=0.7)
            self.play(Create(segs[1]), GrowArrow(feed), run_time=0.7)
            self.play(*au.set_count(4), run_time=0.5)
            vo.wait_until("and asks for")
            self.play(Create(segs[2]), run_time=0.7)
            self.play(*au.set_count(5), flash(au.boxes["capacity"], TURN, 1.05), run_time=0.6)
            vo.wait_until("But downstream")
            self.play(FadeIn(cap0, shift=UP * 0.1), run_time=0.7)
            self.play(flash(cap0, TURN, 1.05), run_time=0.6)

        # ========================================================== 1 · the database: 100 slots, others hold 10
        strip_t = label("autoscaler", CAPTION + 2, TOOL)
        strip_max = label("max = ?", CAPTION, INK)
        strip_cnt = mono("replicas: 0", CAPTION, TURN)
        strip_body = VGroup(gear(0.2), strip_t, strip_cnt, strip_max).arrange(RIGHT, buff=0.22)
        strip = boxed(strip_body, TOOL, pad_x=0.25, pad_y=0.12)
        place(strip, left=-6.4, top=3.05)

        sg = SlotGrid(cell=0.30)
        place(sg, right=6.4, top=3.05)
        ill = illustration_tag()
        place(ill, cx=sg.frame.get_center()[0], top=sg.frame.get_bottom()[1] - 0.06)
        others = label("admin console 4 · batch job 6", CAPTION, SHARED)
        row0 = sg.slot(0).get_center()[1]
        place(others, right=sg.frame.get_left()[0] - 0.2, cy=row0 + 0.02)
        inside(sg, "slot grid", t=3.05)
        inside(strip, "strip", t=3.1)
        apart(sg, lr, "grid / lecture tag")
        apart(strip, others, "strip / others label")
        apart(others, sg.title, "others label / grid title")
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(graph, feed, cap0)), run_time=0.5)
            self.play(FadeTransform(au, strip), run_time=0.9)
            vo.wait_until("The database accepts")
            self.play(FadeIn(sg, shift=LEFT * 0.2), FadeIn(ill), run_time=0.8)
            vo.wait_until("here 100")
            self.play(flash(sg.title, CLOUD, 1.1), LaggedStart(*[flash(s, TURN, 1.4, 0.3) for s in sg.slots[::11]],
                                                                lag_ratio=0.1), run_time=1.0)
            vo.wait_until("Other clients")
            idx_o, an = sg.fill(OTHERS, SHARED)
            self.play(*an, run_time=0.9)
            vo.wait_until("an admin console")
            self.play(FadeIn(others, shift=RIGHT * 0.1), run_time=0.6)
            self.play(flash(VGroup(*[sg.plugs[k] for k in range(4)]), SHARED, 1.3), run_time=0.5)
            vo.wait_until("a batch job")
            self.play(flash(VGroup(*[sg.plugs[k] for k in range(4, 10)]), SHARED, 1.3), run_time=0.6)

        # ========================================================== 2 · a replica plugs in its pool; the course's client
        def band_y(k):
            """Centre y of grid rows 2k-1 and 2k (replica k's 20 slots)."""
            return (sg.slot(10 * (2 * k - 1)).get_center()[1] + sg.slot(10 * 2 * k).get_center()[1]) / 2

        rep_x = sg.frame.get_left()[0] - 1.25 - REP_W / 2
        reps = []
        for k in range(1, 5):
            r = rep_bar(k)
            r.move_to([rep_x, band_y(k), 0])
            reps.append(r)
        for a, b in zip(reps, reps[1:]):
            apart(a, b, "replica rows")
        apart(reps[0], others, "replica 1 / others label")
        apart(reps[0], strip, "replica 1 / strip")

        panel = src_panel(RAG, 56, 57, wrap={57: ["host=", "port="]})
        place(panel, cx=0, bottom=-3.48)
        bar57 = panel.bar(57)
        chroma = panel.span(57, "chromadb.HttpClient")
        stand = grey_chip("the course's vector DB client · stands in for a SQL connection pool")
        place(stand, left=-6.4, top=panel.get_top()[1] + 0.12 + stand.height)
        place(stand, bottom=panel.get_top()[1] + 0.12)
        inside(panel, "code panel")
        apart(panel, ill, "panel / grid tag")
        apart(panel, sg, "panel / grid")
        apart(stand, sg, "chip / grid")
        apart(stand, reps[0], "chip / replica 1")
        apart(stand, panel, "chip / panel", buff=0.05)
        cnt1 = mono("replicas: 1", CAPTION, TURN).move_to(strip_cnt, aligned_edge=LEFT)
        cur = cnt1
        with self.voiceover(SAY[2]) as vo:
            vo.wait_until("Each replica opens")
            self.play(GrowFromPoint(reps[0], strip.get_center()), *swap_text(strip_body, strip_cnt, cnt1), run_time=0.8)
            idx, an = sg.fill(POOL, OWN)
            pipes1 = sg.pipes(reps[0].frame.get_right(), idx)
            self.play(Create(pipes1, lag_ratio=0.04), run_time=1.0)
            self.play(*an, flash(reps[0].pool, OWN, 1.15), run_time=0.7)
            vo.wait_until("In the course app")
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("creates its own")
            self.play(FadeIn(bar57), run_time=0.5)
            self.play(flash(panel.span(57, "client"), TURN, 1.15), run_time=0.6)
            vo.wait_until("That client is ChromaDB")
            self.play(chroma.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("standing in here")
            self.play(FadeIn(stand, shift=UP * 0.1), run_time=0.6)
            self.play(flash(reps[0].pool, OWN, 1.15), run_time=0.6)

        # ========================================================== 3 · replicas 2-4 fill the slots; 5 cannot connect
        r5 = rep_bar(5)
        r5.move_to([rep_x, sg.slot(90).get_center()[1] - 0.15, 0])
        r5_free = [sg.slot(i) for i in range(90, 100)]
        r5_full = [sg.slot(i) for i in range(80, 90)]
        start5 = r5.frame.get_right()
        p5_ok = VGroup(*[Line(start5, s.get_center(), color=ROUTE, stroke_width=1.5, stroke_opacity=0.7)
                         for s in r5_free])
        p5_bad = VGroup(*[Line(start5, s.get_center(), color=ERR, stroke_width=1.5, stroke_opacity=0.8)
                          for s in r5_full])
        sparks = VGroup(*[spark(0.1).move_to(s) for s in r5_full[::3]])
        gauge = cpu_gauge(0.12, w=0.7)
        place(gauge, left=r5.get_left()[0], top=r5.get_bottom()[1] - 0.12)
        tmc = label("too many connections", CAPTION, ERR)
        place(tmc, left=gauge.get_right()[0] + 0.3, cy=gauge.get_center()[1])
        req_y = r5.get_center()[1]
        reqs = VGroup(*[arrow_([-6.1, req_y + d, 0], [r5.get_left()[0] - 0.08, req_y + d, 0], S.GREY, stroke=3)
                        for d in (0.11, -0.11)])
        req_l = note("requests")
        place(req_l, left=-6.1, bottom=req_y + 0.2)
        inside(VGroup(r5, gauge, tmc, reqs, req_l), "replica 5 group")
        apart(r5, reps[3], "replica 5 / 4", buff=0.02)
        apart(tmc, ill, "too many / grid tag")
        apart(tmc, sg, "too many / grid")
        apart(req_l, reps[3], "requests label / replica 4")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(panel, bar57, stand)), run_time=0.5)
            pipes = [pipes1]
            for k in (1, 2, 3):
                nxt = mono(f"replicas: {k + 1}", CAPTION, TURN).move_to(cur, aligned_edge=LEFT)
                self.play(GrowFromPoint(reps[k], strip.get_center()), *swap_text(strip_body, cur, nxt), run_time=0.6)
                cur = nxt
                idx, an = sg.fill(POOL, OWN)
                pk = sg.pipes(reps[k].frame.get_right(), idx)
                pipes.append(pk)
                self.play(Create(pk, lag_ratio=0.03), *an, run_time=0.8)
            vo.wait_until("until the slots run out")
            self.play(flash(VGroup(*sg.plugs[10:]), OWN, 1.08), run_time=0.7)
            vo.wait_until("The next replica")
            self.play(GrowFromPoint(r5, strip.get_center()), run_time=0.6)
            self.play(Create(p5_ok, lag_ratio=0.04), Create(p5_bad, lag_ratio=0.04), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(s, scale=0.4) for s in sparks], lag_ratio=0.15),
                      r5.frame.animate.set_stroke(ERR), p5_ok.animate.set_stroke(ERR, opacity=0.5), run_time=0.6)
            self.play(FadeIn(tmc, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("though its processor")
            self.play(FadeIn(gauge), GrowArrow(reqs[0]), GrowArrow(reqs[1]), FadeIn(req_l), run_time=0.6)
            self.play(reqs.animate.set_color(ERR), flash(gauge, TURN, 1.15), run_time=0.7)

        # ========================================================== 4 · the rule, read off the picture
        y1, y2 = -1.6, -2.85
        lb_ = formula("⌊(", 26, TURN)
        t_lim = label("limit", 26, CLOUD)
        mid1 = formula(" − ", 26)
        t_oth = label("other clients", 26, SHARED)
        mid2 = formula(") ÷ ", 26)
        t_per = label("connections per replica", 26, OWN)
        rb_ = formula("⌋", 26, TURN)
        row1 = VGroup(lb_, t_lim, mid1, t_oth, mid2, t_per, rb_).arrange(RIGHT, buff=0.1)
        for m in (t_lim, t_oth, t_per):
            m.match_y(mid1)
        row1.move_to([0, y1, 0])
        rnd = label("round down", CAPTION, TURN)
        place(rnd, right=row1.get_right()[0], top=row1.get_bottom()[1] - 0.12)
        f_a = formula("⌊(100 − 10) ÷ 20⌋", 26)
        f_b = formula("= ⌊4.5⌋", 26)
        f_c = formula("= 4", 26, TURN)
        row2 = VGroup(f_a, f_b, f_c).arrange(RIGHT, buff=0.25)
        row2.move_to([0, y2, 0])
        cap_y = (sg.slot(80).get_center()[1] + sg.slot(90).get_center()[1]) / 2
        cap = Line([reps[3].get_left()[0] - 0.1, cap_y, 0], [sg.frame.get_right()[0], cap_y, 0],
                   color=TURN, stroke_width=4)
        cap_l = label("max = 4", CAPTION, TURN)
        place(cap_l, right=cap.get_left()[0] - 0.15, cy=cap_y)
        new_max = label("max = 4", CAPTION, TURN).move_to(strip_max, aligned_edge=LEFT)
        inside(VGroup(row1, rnd, row2, cap_l), "formula")
        apart(row1, ill, "formula row 1 / grid tag")
        apart(rnd, row2, "round down / row 2")
        apart(cap_l, reps[3], "cap label / replica 4")
        guard(cap_y < reps[3].get_bottom()[1], "cap line must sit under replica 4")
        assert "".join(m.text for m in (f_a, f_b, f_c)).replace(" ", "") == \
            formula_text(LIMIT, OTHERS, POOL).replace(" ", "")
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(r5, p5_ok, p5_bad, sparks, gauge, tmc, reqs, req_l)), run_time=0.6)
            vo.wait_until("So read the rule")
            self.play(FadeIn(VGroup(lb_, mid1, mid2, rb_)), run_time=0.5)
            vo.wait_until("100 slots")
            self.play(FadeTransform(sg.title.copy(), t_lim), flash(sg.frame, CLOUD, 1.03), run_time=0.8)
            self.play(FadeIn(f_a[0:5]), run_time=0.4)
            vo.wait_until("minus 10")
            self.play(FadeTransform(VGroup(*sg.plugs[:10]).copy(), t_oth), run_time=0.8)
            self.play(FadeIn(f_a[5:8]), run_time=0.4)
            vo.wait_until("leaves 90")
            self.play(flash(f_a[2:8], TURN, 1.1), run_time=0.6)
            vo.wait_until("Divide by 20")
            self.play(FadeTransform(reps[0].pool.copy(), t_per), run_time=0.8)
            self.play(FadeIn(f_a[8:]), run_time=0.4)
            self.play(FadeIn(f_b, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("A replica cannot")
            self.play(flash(VGroup(lb_, rb_), TURN, 1.3), FadeIn(rnd, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("so round down")
            self.play(FadeIn(f_c, shift=RIGHT * 0.1), run_time=0.5)
            self.play(flash(f_c, TURN, 1.3), run_time=0.5)
            vo.wait_until("and set 4")
            self.play(*swap_text(strip_body, strip_max, new_max), outline_flash(strip.frame, TOOL), run_time=0.7)
            self.play(Create(cap), FadeIn(cap_l, shift=RIGHT * 0.1), run_time=0.8)

        # ========================================================== 5 · relief valves; lecture chips
        chips = VGroup(grey_chip("pending work when capacity lags (45)"),
                       grey_chip("concurrency changes downstream pressure (55)"),
                       grey_chip("pooling is the team's job (67)")).arrange(DOWN, buff=0.16)
        chips.move_to([0, -2.25, 0])
        vw = 4.6
        valves = []
        for text in ("connection pooler or smaller pools", "bigger DB tier", "raise max only"):
            t = label(text, CAPTION, INK)
            fr = box(vw, 0.55, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.12)
            place(t, left=fr.get_left()[0] + 0.25, cy=fr.get_center()[1])
            v = VGroup(fr, t)
            v.frame, v.text = fr, t
            valves.append(v)
        vg = VGroup(*valves).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        place(vg, left=-6.4, top=2.2)
        ptag = price_tag()
        place(ptag, right=valves[1].frame.get_right()[0] - 0.2, cy=valves[1].get_center()[1])
        inside(VGroup(chips, vg), "valves / chips")
        apart(vg, strip, "valves / strip")
        apart(vg, reps[0], "valves / replicas")
        apart(vg, cap_l, "valves / cap label")
        apart(chips, ill, "chips / grid tag")
        apart(chips, cap_l, "chips / cap label")
        apart(ptag, valves[1].text, "price tag / valve text")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(row1, rnd, row2)), run_time=0.5)
            lr = lref_swap(self, lr, 16, "45, 55, 67")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(v, shift=RIGHT * 0.15) for v in valves], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("add a connection pooler")
            self.play(valves[0].frame.animate.set_stroke(OWN), valves[0].text.animate.set_color(OWN), run_time=0.5)
            vo.wait_until("or shrink each pool")
            self.play(outline_flash(valves[0].frame, OWN), flash(valves[0].text, OWN, 1.06), run_time=0.7)
            vo.wait_until("or buy a bigger")
            self.play(valves[1].frame.animate.set_stroke(OWN), valves[1].text.animate.set_color(OWN),
                      FadeIn(ptag, scale=0.6), run_time=0.6)
            vo.wait_until("Raising the maximum")
            self.play(valves[2].frame.animate.set_stroke(ERR), valves[2].text.animate.set_color(ERR), run_time=0.5)
            self.play(outline_flash(valves[2].frame, ERR), flash(valves[2].text, ERR, 1.06), run_time=0.7)

        # ========================================================== 6 · PONDER P3
        card = McqCard(STEM, OPTIONS, answer="B", seconds=10)
        inside(card, "ponder card")
        everything = VGroup(strip, sg, ill, others, *reps, *pipes, cap, cap_l, vg, ptag, chips)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(everything), FadeOut(lr), run_time=0.7)
            vo.wait_until("Third question")
            self.play(FadeIn(card, scale=0.97), run_time=0.6)
            vo.wait_until("Which is the smallest")
            self.play(flash(card.stem[-1], TURN, 1.04), run_time=0.7)
        bar = card.bar                     # the 10 s timer drains in silence (as mcq_ponder does)
        self.play(bar.animate(rate_func=lambda t: t).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=card.seconds)
        bar.set_stroke(opacity=0)

        # ========================================================== 7 · reveal: B
        with self.voiceover(SAY[7]) as vo:
            self.play(*card.right("`30 + 10 × 15 = 180 ≤ 200`"), run_time=0.7)
            vo.wait_until("Ten pools")
            self.play(flash(card.reasons["B"], OWN, 1.06), run_time=0.6)
            vo.wait_until("That fits")
            self.play(flash(card.rows["B"], TURN, 1.04), run_time=0.6)

        # ========================================================== 8 · why not A, C, D
        with self.voiceover(SAY[8]) as vo:
            vo.wait_until("A, 150")
            self.play(*card.wrong("A", "150 holds the pools, not the 30 others · `180 > 150`"), run_time=0.7)
            vo.wait_until("C, 250")
            self.play(*card.wrong("C", "works, but 200 already fits"), run_time=0.7)
            ctag = price_tag()
            place(ctag, left=card.reasons["C"].get_right()[0] + 0.25, cy=card.reasons["C"].get_center()[1])
            guard(ctag.get_right()[0] <= card.frame.get_right()[0] - 0.2, "price tag inside the card")
            self.play(FadeIn(ctag, scale=0.6), run_time=0.4)
            vo.wait_until("a higher maximum")
            self.play(*card.wrong("D", "a higher max adds no connections · `180 > 100`"), run_time=0.7)
        self.play(FadeOut(card), FadeOut(ctag), run_time=0.6)

        # ========================================================== 9 · takeaway
        tk = takeaway(TAKEAWAY)
        inside(tk, "takeaway")
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeIn(VGroup(tk.frame, tk.head)), run_time=0.5)
            vo.wait_until("If the question")
            self.play(FadeIn(tk.rows[0], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("rounded down")
            self.play(flash(tk.rows[0], TURN, 1.03), run_time=0.6)
            vo.wait_until("And set it")
            self.play(FadeIn(tk.rows[1], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("does not know")
            self.play(flash(tk.rows[1], TURN, 1.03), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(tk), run_time=0.6)
        self.wait(0.3)
