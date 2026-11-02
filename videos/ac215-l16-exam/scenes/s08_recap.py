"""S08 · Seven rules for the quiz (the recap).
Lecture: L16 71, 75–80 (tags: 14, 71 for the whole picture; 80 for the decision order).

Beats (script.md "## S08", one voiceover block each):
 0  Seven empty rule rows fill the frame: a YELLOW badge 1-7 and an empty thumbnail slot each. Row 1
    writes in: its thumbnail (V1's DNS -> ALB path: browser, BLUE load balancer, TEAL task) draws in
    about a second, then the rule "`localhost` = the machine the code runs on · `10.x` /
    `172.16–31.x` / `192.168.x` private · public → DNS → load balancer :443 → target :8000". On
    "The public reaches" a YELLOW dot runs the thumbnail's path.
 1  Row 2 (the route card: two PINK rows, the lower one barred YELLOW) "VPC = CIDR block cut into
    subnets · most specific route wins · `0.0.0.0/0` → IGW (public) or NAT (private)"; row 3 (the NAT
    notebook with its one-way arrow) "NAT carries only connections that start inside · NAT down →
    internet fails, DB still works".
 2  Row 4 (the two paths: a GREY browser outside a dashed BLUE VPC, a PINK arrow in) "browser is
    outside the VPC → public HTTPS endpoint, never `localhost` / `10.x`"; row 5 (the conveyor: one
    TEAL image on a belt with three stops) "one image promoted · values + secrets at startup · never
    in image, source or Git".
 3  Row 6 (the slot grid) "max replicas = ⌊(limit − other clients) ÷ per replica⌋ · set it as the
    max"; row 7 (the triptych: GREEN table + PINK vector -> BLUE cylinder) "relational + vector in one
    DB → PostgreSQL + pgvector". All seven rows glow YELLOW once.
 4  LECTURE 16 · 14, 71. The rule texts fade; the badges and thumbnails stay as a column at the left.
    Right: slide 71's complete picture redrawn plus slide 14's NAT Gateway in the public subnet: CDN
    (static files) -> browser; browser -> ALB (public subnet) -> FastAPI tasks (private app) ->
    PostgreSQL + pgvector (private data); NAT Gateway -> internet for calls out. Three RED alarm
    bells from S01 sit on it (NAT, browser, app subnet); a YELLOW scan line X-rays the TEAL image
    under the VPC: no key inside (GREEN tick). Packets run each path as the SAY names it and the
    bells turn GREEN one by one.
 5  LECTURE 16 · 80. Everything fades. A row of five numbered steps "trace the request · name the
    contract · choose the boundary · select a service · measure and revise"; step 1 glows YELLOW.
    Everything fades except a small GREY line "AC215 · Lecture 16 · exam edition", then an empty
    frame.
"""

import numpy as np
from manim import (
    DashedVMobject,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    RoundedRectangle,
    ShowPassingFlash,
    Square,
    Transform,
    VGroup,
    linear,
    there_and_back,
)

from common import *  # noqa: F401,F403
from common import _poly
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S08"]
assert len(SAY) == 6, len(SAY)
assert SAY[0].startswith("Seven rules") and "every alarm fixed" in SAY[4] and "Trace the request" in SAY[5]

RULES = [
    "`localhost` = the machine the code runs on · `10.x` / `172.16–31.x` / `192.168.x` private · "
    "public → DNS → load balancer `:443` → target `:8000`",
    "VPC = CIDR block cut into subnets · most specific route wins · `0.0.0.0/0` → IGW (public) or NAT (private)",
    "NAT carries only connections that start inside · NAT down → internet fails, DB still works",
    "browser is outside the VPC → public HTTPS endpoint, never `localhost` / `10.x`",
    "one image promoted · values + secrets at startup · never in image, source or Git",
    "max replicas = `⌊(limit − other clients) ÷ per replica⌋` · set it as the max",
    "relational + vector in one DB → PostgreSQL + pgvector",
]
STEPS = ["trace the request", "name the contract", "choose the boundary", "select a service", "measure and revise"]

COL_X0 = -6.45          # badges' left edge
ROW_W = 12.85           # rule_row width: the text column ends at x ~6.4


def inside(m, msg="out of the safe frame"):
    guard(m.get_left()[0] >= -6.6 and m.get_right()[0] <= 6.6 and m.get_bottom()[1] >= -3.6
          and m.get_top()[1] <= 3.6, msg)
    return m


def apart(a, b, msg):
    """guard: the two boxes do not overlap."""
    ok = (a.get_right()[0] <= b.get_left()[0] or b.get_right()[0] <= a.get_left()[0]
          or a.get_top()[1] <= b.get_bottom()[1] or b.get_top()[1] <= a.get_bottom()[1])
    guard(ok, msg)


def pulse(m, k=1.1):
    return m.animate(rate_func=there_and_back).scale(k)


# ------------------------------------------------------------------ thumbnails (no text; <= 1.3 x 0.8)
def _rr(w, h, col, fill=0.15, sw=3, r=0.06):
    return RoundedRectangle(width=w, height=h, corner_radius=r, stroke_color=col, stroke_width=sw).set_fill(col, fill)


def thumb_dns():
    """V1: browser -> load balancer -> task."""
    b = browser_glyph(0.9)
    alb = _rr(0.7, 0.42, CLOUD)
    t = _rr(0.55, 0.42, CTR)
    g = VGroup(b, alb, t).arrange(RIGHT, buff=0.45)
    a1 = Line(b.get_right(), alb.get_left(), color=ROUTE, stroke_width=4)
    a2 = Line(alb.get_right(), t.get_left(), color=ROUTE, stroke_width=4)
    out = VGroup(g, a1, a2)
    out.path = [b.get_center(), alb.get_center(), t.get_center()]
    return out


def thumb_routes():
    """V2: a route card, the matching row barred YELLOW."""
    rows = VGroup(*[_rr(1.6, 0.36, ROUTE) for _ in range(2)]).arrange(DOWN, buff=0.12)
    divs = VGroup(*[Line(r.get_top(), r.get_bottom(), color=ROUTE, stroke_width=2).shift(RIGHT * 0.15)
                    for r in rows])
    bar = _rr(1.75, 0.46, TURN, fill=0.0, sw=4).move_to(rows[1])
    out = VGroup(rows, divs, bar)
    out.bar = bar
    return out


def thumb_nat():
    """V2: the NAT notebook, an arrow out only."""
    card = _rr(1.1, 0.8, ROUTE, fill=0.08)
    lines = VGroup(*[Line(LEFT * 0.38, RIGHT * 0.38, color=ROUTE, stroke_width=3) for _ in range(3)])
    lines.arrange(DOWN, buff=0.16).move_to(card)
    arr = Line(card.get_right() + RIGHT * 0.08, card.get_right() + RIGHT * 0.75, color=ROUTE,
               stroke_width=5).add_tip(tip_length=0.22)
    out = VGroup(card, lines, arr)
    out.arr = arr
    return out


def thumb_paths():
    """V3: the browser outside the VPC, a request into the VPC's front door."""
    b = browser_glyph(0.9)
    vpc = dashed_box(1.1, 0.9)
    g = VGroup(b, vpc).arrange(RIGHT, buff=0.55)
    a = Line(b.get_right(), vpc.get_left(), color=ROUTE, stroke_width=5).add_tip(tip_length=0.2)
    out = VGroup(g, a)
    out.arr = a
    return out


def dashed_box(w, h):
    return DashedVMobject(_rr(w, h, CLOUD, fill=0.05, r=0.1), num_dashes=22)


def thumb_conveyor():
    """V4: one image on a belt with three stops."""
    belt = Line(LEFT * 1.0, RIGHT * 1.0, color=S.GREY, stroke_width=5)
    stops = VGroup(*[Dot(belt.point_from_proportion(p), radius=0.07, color=S.GREY) for p in (0.08, 0.5, 0.92)])
    slabs = VGroup(*[_rr(0.5, 0.13, CTR, fill=0.2 + 0.15 * k, sw=2, r=0.03) for k in range(3)])
    slabs.arrange(DOWN, buff=0.04).next_to(stops[0], UP, buff=0.08)
    out = VGroup(belt, stops, slabs)
    out.img, out.stops = slabs, stops
    return out


def thumb_grid():
    """V5: the connection slots, most of them plugged."""
    return VGroup(*[Square(0.2, stroke_color=CLOUD, stroke_width=2)
                    .set_fill(ROUTE if j < 12 else (SHARED if j < 15 else CLOUD), 0.65 if j < 15 else 0.05)
                    for j in range(18)]).arrange_in_grid(3, 6, buff=0.06)


def thumb_db():
    """V6: a GREEN table and a PINK vector into one BLUE cylinder."""
    tbl = VGroup(_rr(0.55, 0.16, OWN, fill=0.5, sw=2, r=0.02),
                 *[_rr(0.55, 0.14, OWN, fill=0.1, sw=2, r=0.02) for _ in range(2)]).arrange(DOWN, buff=0.03)
    vec = VGroup(*[Line(ORIGIN_, np.array([np.cos(a), np.sin(a), 0]) * 0.28, color=ROUTE, stroke_width=3)
                   for a in (0.3, 1.1, 1.9)])
    vec.add(Dot(ORIGIN_, radius=0.05, color=ROUTE))
    left = VGroup(tbl, vec).arrange(DOWN, buff=0.08)
    cyl = cylinder(None, None, CLOUD, w=0.6, h=0.42)
    g = VGroup(left, cyl).arrange(RIGHT, buff=0.4)
    a = Line(left.get_right(), cyl.get_left(), color=S.GREY, stroke_width=3).add_tip(tip_length=0.15)
    return VGroup(g, a)


ORIGIN_ = np.array([0.0, 0.0, 0.0])
THUMBS = [thumb_dns, thumb_routes, thumb_nat, thumb_paths, thumb_conveyor, thumb_grid, thumb_db]


# ------------------------------------------------------------------ the whole picture (beat 4)
VX0, VX1, VY0, VY1 = -4.25, 6.45, -1.95, 1.55
SY0, SY1 = -1.8, 1.15
HEAD_Y = 0.85


def build_picture():
    p = {}
    vpc = box(VX1 - VX0, VY1 - VY0, CLOUD, fill_opacity=0.03, stroke=3, radius=0.2)
    vpc.move_to([(VX0 + VX1) / 2, (VY0 + VY1) / 2, 0])
    vtag = tag(f"VPC · {VPC_CIDR}", CLOUD, size=CAPTION)
    vtag.move_to([VX1 - 0.3 - vtag.width / 2, VY1, 0])
    heads, subs = {}, VGroup()
    for k, (x0, x1, name, lock) in {"public": (-4.1, -1.3, "public subnet", False),
                                     "app": (-1.1, 2.6, "private app", True),
                                     "data": (2.8, 6.3, "private data", True)}.items():
        sb = box(x1 - x0, SY1 - SY0, CLOUD, fill_opacity=0.05 if k == "public" else 0.02, stroke=2.5,
                 radius=0.14).move_to([(x0 + x1) / 2, (SY0 + SY1) / 2, 0])
        ht = label(name, CAPTION, CLOUD)
        ht.move_to([x0 + 0.15 + ht.width / 2, HEAD_Y, 0])
        hg = VGroup(ht)
        if lock:
            hg.add(padlock(0.28).next_to(ht, RIGHT, buff=0.14))
        subs.add(sb)
        heads[k] = hg
        p[k] = sb
    alb = box(1.3, 0.55, CLOUD, fill_opacity=0.15, stroke=3).move_to([-2.05, 0.1, 0])
    albt = label("ALB", CAPTION, INK).move_to(alb)
    nat = box(1.5, 0.8, CLOUD, fill_opacity=0.15, stroke=3).move_to([-2.85, -1.1, 0])
    natt = VGroup(label("NAT", CAPTION, INK), label("Gateway", CAPTION, INK)).arrange(DOWN, buff=0.02).move_to(nat)
    tasks = VGroup(*[box(0.55, 0.5, CTR, fill_opacity=0.18, stroke=3, radius=0.08) for _ in range(3)])
    tasks.arrange(RIGHT, buff=0.15).move_to([0.75, 0.1, 0])
    taskt = label("FastAPI tasks", CAPTION, INK)
    taskt.move_to([0.25 + taskt.width / 2, -0.55, 0])
    db = cylinder(None, None, CLOUD, w=1.15, h=0.58).move_to([3.55, 0.15, 0])
    dbt = label("PostgreSQL", CAPTION, INK).next_to(db, DOWN, buff=0.12)
    pgv = chip("+ pgvector", TOOL, size=CAPTION).next_to(db, RIGHT, buff=0.22)
    brw = browser_glyph(1.0).move_to([-2.05, 2.4, 0])
    brt = label("browser", CAPTION, BROWSER).next_to(brw, LEFT, buff=0.2)
    cdn = box(2.7, 0.6, CLOUD, fill_opacity=0.12, stroke=3)
    cdnt = label("static files · CDN", CAPTION, INK)
    cdn.stretch_to_fit_width(cdnt.width + 0.4)
    cdn.move_to([brw.get_right()[0] + 0.85 + cdn.width / 2, 2.4, 0])
    cdnt.move_to(cdn)
    net = internet_cloud(1.25, None).move_to([-2.85, -2.75, 0])
    nett = label("internet · LLM API", CAPTION, SHARED).next_to(net, RIGHT, buff=0.2)
    # paths
    a_cdn = arrow_(cdn.get_left(), brw.get_right(), ROUTE, stroke=3)
    a_alb = arrow_(brw.get_bottom(), alb.get_top(), ROUTE, stroke=3)
    a_task = arrow_(alb.get_right(), tasks[0].get_left(), ROUTE, stroke=3)
    a_db = arrow_(tasks[2].get_right(), db.get_left() + DOWN * 0.05, ROUTE, stroke=3)
    nat_pts = [tasks[0].get_bottom() + DOWN * 0.04, [tasks[0].get_x(), -1.1, 0], nat.get_right() + RIGHT * 0.06]
    p_nat = _poly(nat_pts, ROUTE, 3)
    a_out = arrow_(nat.get_bottom(), net.get_top(), ROUTE, stroke=3)
    # bells (S01's alarms): NAT, browser, app subnet
    b_nat = bell(0.4).move_to([-3.75, -0.2, 0])
    b_brw = bell(0.4).next_to(brw, UP, buff=0.12)
    b_cap = bell(0.4).move_to([2.15, HEAD_Y, 0])
    # the image under the VPC, x-rayed
    slabs = VGroup(*[_rr(1.5, 0.17, CTR, fill=0.15 + 0.1 * k, sw=2, r=0.04) for k in range(3)]).arrange(DOWN, buff=0.05)
    imgn = mono(IMAGE, CAPTION, CTR).next_to(slabs, LEFT, buff=0.25)
    nokey = VGroup(tick_mark(0.28), label("no key inside", CAPTION, OWN)).arrange(RIGHT, buff=0.12)
    nokey.next_to(slabs, RIGHT, buff=0.3)
    img = VGroup(imgn, slabs, nokey)
    img.move_to([3.4, -2.75, 0])
    shapes = VGroup(vpc, subs, alb, nat, tasks, db, brw, cdn, net)
    words = VGroup(vtag, *heads.values(), albt, natt, taskt, dbt, pgv, brt, cdnt, nett)
    paths = VGroup(a_cdn, a_alb, a_task, a_db, p_nat, a_out)
    p.update(dict(vpc=vpc, alb=alb, nat=nat, tasks=tasks, db=db, brw=brw, cdn=cdn, net=net, pgv=pgv,
                  a_cdn=a_cdn, a_alb=a_alb, a_task=a_task, a_db=a_db, p_nat=p_nat, a_out=a_out,
                  bells=VGroup(b_nat, b_brw, b_cap), img=img, slabs=slabs, nokey=nokey, imgn=imgn,
                  nat_pts=nat_pts))
    # layout guards
    for a, b, m in ((heads["public"], alb, "public header / ALB"), (heads["public"], b_nat, "public header / bell"),
                    (b_nat, nat, "bell / NAT"), (b_nat, alb, "bell / ALB"),
                    (heads["app"], tasks, "app header / tasks"), (heads["app"], b_cap, "app header / bell"),
                    (taskt, tasks, "task label / tasks"), (dbt, heads["data"], "db label / header"),
                    (pgv, heads["data"], "pgvector / header"), (vtag, heads["data"], "VPC tag / data header"),
                    (brt, b_brw, "browser label / bell"), (cdnt, b_brw, "cdn / bell"),
                    (nett, img, "internet label / image"), (taskt, p_nat, "task label / NAT path")):
        apart(a, b, m)
    guard(a_alb.get_center()[0] - 0.12 > heads["public"].get_right()[0] + 0.05, "browser -> ALB arrow crosses the header")
    guard(pgv.get_right()[0] <= 6.2, "pgvector chip leaves the data subnet")
    guard(dbt.get_bottom()[1] >= SY0 + 0.05, "PostgreSQL label below its subnet")
    guard(taskt.get_right()[0] <= 2.5, "task label leaves the app subnet")
    guard(img.get_left()[0] >= nett.get_right()[0] + 0.2, "image strip touches the internet label")
    pic = VGroup(shapes, words, paths, p["bells"], img)
    return pic, p


class Recap(VoiceScene):
    def construct(self):
        # ------------------------------------------------------------ the seven rows
        rows = VGroup(*[rule_row(i + 1, RULES[i], THUMBS[i](), width=ROW_W) for i in range(7)])
        rows.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        rows.move_to([0, 0, 0]).align_to([COL_X0, 0, 0], LEFT)
        inside(rows, "rule rows out of frame")
        for i in range(6):
            apart(rows[i], rows[i + 1], f"rule rows {i + 1}/{i + 2}")
        for r in rows:
            guard(r.text.get_right()[0] <= 6.5, "rule text too wide")
        guides = VGroup(*[Line([r.slot.get_right()[0] + 0.25, r.badge.get_y(), 0], [6.3, r.badge.get_y(), 0],
                               color=S.GREY, stroke_width=1.5, stroke_opacity=0.35) for r in rows])
        slots = VGroup(*[_rr(1.3, 0.8, S.GREY, fill=0.0, sw=1.5, r=0.08).move_to(r.slot) for r in rows])
        slots.set_stroke(opacity=0.45)

        def write_row(i):
            r = rows[i]
            return [Create(r.thumb, run_time=1.0), FadeOut(slots[i]), FadeOut(guides[i]),
                    LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in r.text], lag_ratio=0.35, run_time=1.0)]

        # ------------------------------------------------------------ beat 0
        with self.voiceover(SAY[0]) as vo:
            self.play(LaggedStart(*[FadeIn(VGroup(r.badge, s, g)) for r, s, g in zip(rows, slots, guides)],
                                  lag_ratio=0.15), run_time=1.4)
            vo.wait_until("One")
            self.play(Indicate(rows[0].badge, color=TURN), run_time=0.5)
            self.play(*write_row(0))
            vo.wait_until("The public reaches")
            dot = Dot(radius=0.07, color=TURN).move_to(rows[0].thumb.path[0])
            self.play(FadeIn(dot), run_time=0.2)
            self.play(MoveAlongPath(dot, _poly(rows[0].thumb.path, TURN)), run_time=1.3, rate_func=linear)
            self.play(FadeOut(dot), Indicate(rows[0].thumb[0][2], color=TURN), run_time=0.5)

        # ------------------------------------------------------------ beat 1
        with self.voiceover(SAY[1]) as vo:
            self.play(Indicate(rows[1].badge, color=TURN), run_time=0.5)
            self.play(*write_row(1))
            vo.wait_until("most specific")
            self.play(pulse(rows[1].thumb.bar, 1.1), run_time=0.7)
            vo.wait_until("Three")
            self.play(Indicate(rows[2].badge, color=TURN), run_time=0.5)
            self.play(*write_row(2))
            vo.wait_until("If it fails")
            self.play(ShowPassingFlash(rows[2].thumb.arr.copy().set_stroke(TURN, 7), time_width=0.6), run_time=0.9)

        # ------------------------------------------------------------ beat 2
        with self.voiceover(SAY[2]) as vo:
            self.play(Indicate(rows[3].badge, color=TURN), run_time=0.5)
            self.play(*write_row(3))
            vo.wait_until("so it calls")
            self.play(ShowPassingFlash(rows[3].thumb.arr.copy().set_stroke(TURN, 7), time_width=0.6), run_time=0.8)
            vo.wait_until("Five")
            self.play(Indicate(rows[4].badge, color=TURN), run_time=0.5)
            self.play(*write_row(4))
            th = rows[4].thumb
            for k in (1, 2):
                self.play(th.img.animate.next_to(th.stops[k], UP, buff=0.08), run_time=0.5)

        # ------------------------------------------------------------ beat 3
        with self.voiceover(SAY[3]) as vo:
            self.play(Indicate(rows[5].badge, color=TURN), run_time=0.5)
            self.play(*write_row(5))
            vo.wait_until("rounded down")
            self.play(Indicate(rows[5].text, color=TURN, scale_factor=1.03), run_time=0.7)
            vo.wait_until("Seven")
            self.play(Indicate(rows[6].badge, color=TURN), run_time=0.5)
            self.play(*write_row(6))
            self.play(LaggedStart(*[Indicate(r.text, color=TURN, scale_factor=1.03) for r in rows],
                                  lag_ratio=0.18), run_time=2.0)

        # ------------------------------------------------------------ beat 4: the whole picture
        pic, P = build_picture()
        inside(pic, "picture out of frame")
        col = VGroup(*[VGroup(r.badge, r.thumb) for r in rows])
        guard(col.get_right()[0] <= pic.get_left()[0] - 0.1, "rule column touches the picture")
        lr = lref(16, "14, 71")
        for m in (P["cdn"], P["vpc"], *P["bells"], P["brw"]):
            apart(lr, m, "lecture tag / picture")
        shapes, words, paths, bells, img = pic
        green = VGroup(*[bell(0.4, OWN).move_to(b) for b in bells])
        scan = Line(LEFT * 0.85, RIGHT * 0.85, color=TURN, stroke_width=5).move_to(P["slabs"].get_top())

        def run(points, t=1.0):
            d = Dot(radius=0.09, color=TURN).move_to(points[0])
            self.add(d)
            self.play(MoveAlongPath(d, _poly(points, TURN)), run_time=t, rate_func=linear)
            self.remove(d)

        with self.voiceover(SAY[4]) as vo:
            self.play(*[FadeOut(r.text) for r in rows], FadeIn(lr), run_time=0.6)
            self.play(LaggedStart(Create(P["vpc"]), FadeIn(VGroup(*shapes[1:])), FadeIn(words), lag_ratio=0.3),
                      run_time=1.2)
            self.play(LaggedStart(*[Create(m) for m in paths], lag_ratio=0.15), FadeIn(bells, scale=1.3),
                      FadeIn(VGroup(P["imgn"], P["slabs"])), run_time=1.0)
            vo.wait_until("every alarm")
            self.add(scan)
            self.play(scan.animate.move_to(P["slabs"].get_bottom()), run_time=0.7)
            self.play(FadeOut(scan), FadeIn(P["nokey"], shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Static files")
            self.play(ShowPassingFlash(P["a_cdn"].copy().set_stroke(TURN, 7), time_width=0.7), run_time=0.7)
            vo.wait_until("requests through")
            run([P["brw"].get_bottom(), P["alb"].get_center(), P["tasks"][0].get_center()], 0.9)
            self.play(Transform(bells[1], green[1]), run_time=0.5)
            vo.wait_until("tasks in the private")
            self.play(Indicate(P["tasks"], color=TURN, scale_factor=1.08), Transform(bells[2], green[2]),
                      run_time=0.7)
            vo.wait_until("PostgreSQL in the data")
            run([P["tasks"][2].get_center(), P["db"].get_center()], 0.6)
            self.play(Indicate(P["pgv"], color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("and NAT for calls")
            run(P["nat_pts"] + [P["nat"].get_center(), P["net"].get_center()], 1.0)
            self.play(Transform(bells[0], green[0]), run_time=0.5)

        # ------------------------------------------------------------ beat 5: the decision order
        steps = VGroup()
        xs = [-5.1 + 2.55 * k for k in range(5)]
        for k, s in enumerate(STEPS):
            b = step_badge(k + 1, TURN if k == 0 else S.GREY, radius=0.26)
            t = fit_rows(s, 2.3, 22, align=ORIGIN).next_to(b, DOWN, buff=0.2)
            g = VGroup(b, t).move_to([xs[k], 0.4, 0])
            g.badge, g.text = b, t
            steps.add(g)
        arrows = VGroup(*[arrow_(steps[k].badge.get_right(), steps[k + 1].badge.get_left(), S.GREY, stroke=3)
                          for k in range(4)])
        for k in range(4):
            apart(steps[k], steps[k + 1], f"steps {k + 1}/{k + 2}")
        halo = _rr(steps[0].width + 0.4, steps[0].height + 0.35, TURN, fill=0.08, sw=4, r=0.15).move_to(steps[0])
        sign = label("AC215 · Lecture 16 · exam edition", CAPTION, S.GREY).move_to([0, -2.6, 0])
        inside(VGroup(steps, arrows, halo, sign), "steps out of frame")
        for k in range(4):
            guard(arrows[k].get_length() > 0.3, "step arrows too short")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pic), FadeOut(col), run_time=0.6)
            lr = lref_swap(self, lr, 16, "80")
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in steps], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("Trace the request")
            self.play(Create(halo), steps[0].text.animate.set_color(TURN), run_time=0.6)
            self.play(Indicate(steps[0].badge, color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("Good luck")
            self.play(FadeOut(VGroup(steps, arrows, halo)), FadeOut(lr), FadeIn(sign, shift=UP * 0.1), run_time=0.7)
        self.wait(0.8)
        self.play(FadeOut(sign), run_time=0.6)
        self.wait(0.3)


