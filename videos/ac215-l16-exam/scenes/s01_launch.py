"""S01 · Launch day: three alarms (cold open, the hook).
Lecture: L16 71; L10 4. No code. Tag `illustration` while the invented launch morning is on screen.

Beats (script.md "## S01", one voiceover block each):
 0  Cold open, no lecture tag. GREY laptop (bottom left) holding a TEAL container "cheese app"; a
    GREY clock chip "launch morning · 8:00" top left, the `illustration` tag top right. On "This
    morning" our redrawing of L16 slide 71 (+ slide 16's NAT Gateway) draws: a GREY browser on top,
    the BLUE VPC with a public subnet (NAT Gateway at the edge, ALB), a private app subnet and a
    private data subnet (PostgreSQL); the ORANGE outside LLM API beyond the edge. A GREY curved
    arrow carries the container into the app subnet, where it becomes three TEAL FastAPI tasks; the
    laptop leaves. On "three alarms" the clock chip pulses.
 1  Alarm 1: a RED bell over the NAT Gateway (wiggles). A YELLOW packet leaves a task through the
    NAT Gateway towards the LLM API and dies RED half way. Callout: a GREY chat bubble "asking the
    language model…" whose clock hand turns and goes RED "timeout"; under it "chat history" — a
    packet from a task reaches the database, GREEN ✓.
 2  Alarm 2: a RED bell over the browser. Callout: a big GREY browser window, "page" with a GREEN ✓,
    the "Predict" button with a spinner that turns into a RED "Network Error"; beside it a small GREY
    laptop thumbnail "developer's laptop" with the same button and a GREEN ✓.
 3  Alarm 3: the clock chip swaps to "9:00". The GREY traffic arrow browser → ALB doubles
    ("traffic ×2"); a PURPLE "autoscaler · 3 → 6" chip; three new TEAL replicas pop in under the
    first three. Packets from the newcomers: the fourth reaches the database (GREEN ✓), the fifth
    and sixth spark RED at it; both turn RED and a RED mono "too many connections" label brackets
    them, a low GREY CPU gauge beside it. A RED bell over the app subnet.
 4  The quieter fourth problem, no bell: a TEAL image "myapp:v1.4" on a GREY registry shelf; a
    YELLOW scan line X-rays it into its layers; a GOLD key glows inside the top layer, outlined RED.
 5  The map's words fade and its shapes shrink to a thumbnail at the top (the three RED bells still
    on it). The plan builds left to right as the SAY names each item: addresses (house + door),
    routes and NAT (two PINK rows), the browser (GREY window), configuration (TEAL image + GREEN
    cards), capacity (grid of slots), the database (BLUE cylinder); a GREY arrow under them.
 6  All of that leaves. LECTURE 16 · 71 specimen tag in top right, pulses once; a GREY code-panel
    header specimen `cheese-app-v0/api-service/docker-shell.sh · lines 19–27` pulses once; the GREY
    chip "no live runs · concepts, not clicks". Then an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arc,
    ArcBetweenPoints,
    Circle,
    CurvedArrow,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    Rotate,
    RoundedRectangle,
    Square,
    VGroup,
    Wiggle,
    Create,
    linear,
    there_and_back,
)

from common import *  # noqa: F401,F403
from common import _header_text, _poly
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S01"]
assert len(SAY) == 7, len(SAY)
assert "Within an hour" in SAY[0] and "Predict button" in SAY[2] and "too many connections" in SAY[3]

# ------------------------------------------------------------------ layout (the map sits on top)
VPC_X0, VPC_X1, VPC_Y0, VPC_Y1 = -4.7, 6.45, -0.95, 1.85
SUB_Y0, SUB_Y1 = -0.8, 1.5
HEAD_Y = 1.22
ROW1, ROW2 = 0.55, -0.35          # the replica rows in the app subnet
REP_X = (-0.2, 1.15, 2.5)
BOTTOM_TOP = -1.2                  # the callout band: y -1.2 .. -3.45


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
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


def inside(m, msg="out of the safe frame"):
    guard(m.get_left()[0] >= -6.6 and m.get_right()[0] <= 6.6 and m.get_bottom()[1] >= -3.6
          and m.get_top()[1] <= 3.6, msg)
    return m


def apart(a, b, msg):
    """guard: the two boxes do not overlap."""
    ok = (a.get_right()[0] <= b.get_left()[0] or b.get_right()[0] <= a.get_left()[0]
          or a.get_top()[1] <= b.get_bottom()[1] or b.get_top()[1] <= a.get_bottom()[1])
    guard(ok, msg)


def replica_box(i=None):
    fr = box(1.2, 0.5, CTR, fill_opacity=0.15, stroke=3, radius=0.08)
    t = label("FastAPI", CAPTION, INK).move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def clock_icon(r=0.24, color=S.GREY):
    face = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    hour = Line(ORIGIN_, UP * r * 0.5, stroke_color=color, stroke_width=3)
    minute = Line(ORIGIN_, RIGHT * r * 0.75, stroke_color=color, stroke_width=3)
    g = VGroup(face, hour, minute)
    g.face, g.hour, g.minute = face, hour, minute
    return g


ORIGIN_ = np.array([0.0, 0.0, 0.0])


def spinner(r=0.17, color=S.GREY):
    return Arc(radius=r, start_angle=0, angle=1.5 * PI, stroke_color=color, stroke_width=4)


def pulse(m, k=1.1):
    """Grow and shrink back once (Indicate would tint a chip's dark fill and hide its text)."""
    return m.animate(rate_func=there_and_back).scale(k)


def packet_dot(color=TURN):
    return Dot(radius=0.09, color=color)


def build_map():
    """Our redrawing of L16 slide 71 (+ slide 16's NAT Gateway). Returns (map group, words, parts)."""
    p = {}
    words = VGroup()
    vpc = box(VPC_X1 - VPC_X0, VPC_Y1 - VPC_Y0, CLOUD, fill_opacity=0.03, stroke=3, radius=0.2)
    vpc.move_to([(VPC_X0 + VPC_X1) / 2, (VPC_Y0 + VPC_Y1) / 2, 0])
    vtag = tag(f"VPC · {VPC_CIDR}", CLOUD, size=CAPTION)
    vtag.move_to([VPC_X1 - 0.35 - vtag.width / 2, VPC_Y1, 0])
    p["vpc"] = vpc
    words.add(vtag)
    subs = VGroup()
    heads = {}
    for k, (x0, x1, name, lock) in {
        "public": (-4.5, -1.25, "public subnet", False),
        "app": (-1.05, 3.35, "private app", True),
        "data": (3.55, 6.3, "private data", True),
    }.items():
        sb = box(x1 - x0, SUB_Y1 - SUB_Y0, CLOUD, fill_opacity=0.05 if k == "public" else 0.02, stroke=2.5,
                 radius=0.14).move_to([(x0 + x1) / 2, (SUB_Y0 + SUB_Y1) / 2, 0])
        ht = label(name, CAPTION, CLOUD)
        ht.move_to([x0 + 0.18 + ht.width / 2, HEAD_Y, 0])
        subs.add(sb)
        words.add(ht)
        heads[k] = ht
        if lock:
            pl = padlock(0.28).next_to(ht, RIGHT, buff=0.14)
            subs.add(pl)
        p[k] = sb
    nat = box(1.4, 0.78, CLOUD, fill_opacity=0.15, stroke=3).move_to([-3.72, -0.25, 0])
    natt = VGroup(label("NAT", CAPTION, INK), label("Gateway", CAPTION, INK)).arrange(DOWN, buff=0.02).move_to(nat)
    alb = box(1.5, 0.62, CLOUD, fill_opacity=0.15, stroke=3).move_to([-2.1, 0.55, 0])
    albt = label("ALB", CAPTION, INK).move_to(alb)
    p["nat"], p["alb"] = nat, alb
    words.add(natt, albt)
    reps = VGroup(*[replica_box().move_to([x, ROW1, 0]) for x in REP_X])
    p["reps"] = reps
    db = cylinder(None, None, CLOUD, w=1.25, h=0.62).move_to([4.92, 0.42, 0])
    dbt = label("PostgreSQL", CAPTION, INK).next_to(db, DOWN, buff=0.1)
    p["db"] = db
    words.add(dbt)
    llm = internet_cloud(1.3, None).move_to([-5.75, 0.45, 0])
    llmt = VGroup(label("LLM", CAPTION, SHARED), label("API", CAPTION, SHARED)).arrange(DOWN, buff=0.02)
    llmt.next_to(llm, DOWN, buff=0.08)
    p["llm"] = llm
    words.add(llmt)
    brw = browser_glyph(1.1).move_to([-2.1, 2.5, 0])
    brt = label("browser", CAPTION, BROWSER).next_to(brw, RIGHT, buff=0.15)
    p["browser"] = brw
    words.add(brt)
    p["brt"] = brt
    a_in = Line(brw.get_bottom() + DOWN * 0.05, alb.get_top() + UP * 0.05, color=S.GREY, stroke_width=3)
    a_task = Line(alb.get_right() + RIGHT * 0.04, reps[0].get_left() + LEFT * 0.04, color=S.GREY, stroke_width=3)
    p["a_in"], p["a_task"] = a_in, a_task
    shapes = VGroup(vpc, subs, nat, alb, db, llm, brw, a_in, a_task)
    p["shapes"] = shapes
    # labels, reps and the shapes do not collide
    for a, b, m in ((heads["public"], alb, "public header / ALB"), (heads["public"], nat, "public header / NAT"),
                    (heads["app"], reps[0], "app header / replica"), (dbt, heads["data"], "db label / header"),
                    (vtag, heads["data"], "VPC tag / data header"), (brt, vtag, "browser label / VPC tag")):
        apart(a, b, m)
    guard(dbt.get_bottom()[1] >= SUB_Y0 + 0.05, "PostgreSQL label below its subnet")
    guard(llmt.get_left()[0] >= -6.6, "LLM API label out of frame")
    guard(a_in.get_center()[0] > heads["public"].get_right()[0] + 0.1, "traffic arrow crosses the header")
    return VGroup(shapes, reps, words), words, p


class LaunchDay(VoiceScene):
    def construct(self):
        mp, words, P = build_map()
        inside(mp, "map out of frame")
        reps = P["reps"]

        clock = VGroup(grey_chip("launch morning · 8:00"))
        place(clock, left=-6.55, top=3.55)
        itag = illustration_tag()
        place(itag, right=6.55, top=3.55)

        # the laptop with the app (bottom left)
        lap = laptop(2.4)
        ctr = container_box("cheese app", w=1.9, h=0.62)
        ctr.move_to(lap.screen)
        lapt = label("laptop · last week", CAPTION, LAPTOP)
        lap_g = VGroup(lap, ctr, lapt)
        lapt.next_to(lap, DOWN, buff=0.1)
        place(lap_g, left=-6.3, bottom=-3.4)
        guard(lap_g.get_top()[1] <= BOTTOM_TOP, "laptop overlaps the map")

        # ------------------------------------------------------------ beat 0
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(clock, shift=DOWN * 0.1), FadeIn(itag), run_time=0.6)
            self.play(FadeIn(lap), FadeIn(lapt), run_time=0.6)
            self.play(FadeIn(ctr, scale=0.8), run_time=0.5)
            vo.wait_until("This morning")
            self.play(LaggedStart(Create(P["vpc"]), FadeIn(VGroup(P["shapes"][1])),
                                  FadeIn(VGroup(P["nat"], P["alb"], P["db"], P["llm"], P["browser"])),
                                  lag_ratio=0.3), run_time=1.2)
            self.play(FadeIn(words), Create(P["a_in"]), Create(P["a_task"]), run_time=0.8)
            arc = CurvedArrow(ctr.get_top() + UP * 0.05, reps[1].get_bottom() + DOWN * 0.08,
                              angle=-PI / 3, color=S.GREY, stroke_width=3)
            self.play(Create(arc), run_time=0.6)
            mover = ctr.copy()
            path = ArcBetweenPoints(ctr.get_center(), reps[1].get_center(), angle=-PI / 3)
            self.play(MoveAlongPath(mover, path), run_time=1.0)
            self.play(FadeOut(mover, scale=0.6), FadeOut(arc),
                      LaggedStart(*[GrowFromCenter(r) for r in reps], lag_ratio=0.25), run_time=0.9)
            vo.wait_until("Within an hour")
            self.play(FadeOut(lap_g), run_time=0.5)
            self.play(pulse(clock, 1.12), run_time=0.8)

        # ------------------------------------------------------------ beat 1: NAT
        bell1 = bell(0.42).move_to([-3.72, 0.5, 0])
        apart(bell1, P["alb"], "bell 1 / ALB")
        out_pts = [reps[0].get_left() + DOWN * 0.15, [-1.15, 0.4, 0], [-1.15, -0.25, 0],
                   P["nat"].get_right(), P["nat"].get_left(), [-5.05, 0.1, 0]]
        out_path = VGroup(_poly(out_pts[:4], ROUTE, 3), _poly(out_pts[4:], ROUTE, 3))   # not across NAT's words
        db_pts = [reps[2].get_right(), P["db"].get_left()]
        bub = RoundedRectangle(width=4.1, height=0.62, corner_radius=0.3, stroke_color=S.GREY, stroke_width=2.5) \
            .set_fill(PANEL, 1)
        bubt = label("asking the language model…", CAPTION, INK).move_to(bub)
        tail = Line(bub.get_corner(DOWN + LEFT) + RIGHT * 0.45, bub.get_corner(DOWN + LEFT) + RIGHT * 0.2 + DOWN * 0.22,
                    color=S.GREY, stroke_width=2.5)
        ck = clock_icon().next_to(bub, RIGHT, buff=0.3)
        tout = label("timeout", CAPTION, ERR).next_to(ck, RIGHT, buff=0.15)
        tout.set_opacity(0)
        hist = label("chat history", CAPTION, INK)
        hcyl = cylinder(None, None, CLOUD, w=0.5, h=0.3)
        hok = check_mark(0.32, OWN)
        hrow = VGroup(hcyl, hist, hok).arrange(RIGHT, buff=0.22)
        hok.set_opacity(0)
        call1 = VGroup(VGroup(bub, bubt, tail), ck, tout, hrow)
        hrow.next_to(bub, DOWN, buff=0.45).align_to(bub, LEFT)
        place(call1, left=-5.6, top=BOTTOM_TOP - 0.2)
        inside(call1, "alarm 1 callout")
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(bell1, scale=1.4), run_time=0.5)
            self.play(Wiggle(bell1), run_time=0.8)
            vo.wait_until("Chat answers")
            self.play(FadeIn(call1[0], shift=UP * 0.1), FadeIn(ck), run_time=0.5)
            d1 = packet_dot().move_to(out_pts[0])
            self.play(FadeIn(d1), Create(out_path), run_time=0.6)
            self.play(MoveAlongPath(d1, _poly(out_pts[:-1] + [[-4.75, 0.0, 0]], ROUTE)), run_time=1.6,
                      rate_func=linear)
            self.play(Rotate(ck.minute, -2 * PI, about_point=ck.face.get_center()), run_time=1.2, rate_func=linear)
            self.play(d1.animate.set_color(ERR).scale(0.3).set_opacity(0),
                      out_path.animate.set_stroke(ERR, opacity=0.6),
                      *[m.animate.set_stroke(ERR) for m in ck], tout.animate.set_opacity(1), run_time=0.6)
            self.remove(d1)
            vo.wait_until("Yet the saved")
            self.play(FadeIn(VGroup(hcyl, hist), shift=UP * 0.1), run_time=0.5)
            d2 = packet_dot().move_to(db_pts[0])
            self.add(d2)
            self.play(d2.animate.move_to(db_pts[1]), run_time=0.9)
            ok_db = check_mark(0.32, OWN).next_to(P["db"], RIGHT, buff=0.08)
            self.play(FadeOut(d2), FadeIn(ok_db), hok.animate.set_opacity(1), run_time=0.5)
        self.play(FadeOut(call1), FadeOut(ok_db), FadeOut(out_path), run_time=0.5)

        # ------------------------------------------------------------ beat 2: browser
        bell2 = bell(0.42).next_to(P["browser"], LEFT, buff=0.25)
        win = RoundedRectangle(width=4.6, height=1.95, corner_radius=0.1, stroke_color=BROWSER, stroke_width=2.5) \
            .set_fill(PANEL, 1)
        wbar = Line(win.get_corner(UP + LEFT) + DOWN * 0.25, win.get_corner(UP + RIGHT) + DOWN * 0.25,
                    color=BROWSER, stroke_width=2)
        wdots = VGroup(*[Dot(radius=0.04, color=BROWSER) for _ in range(3)]).arrange(RIGHT, buff=0.07)
        wdots.move_to(win.get_corner(UP + LEFT) + np.array([0.28, -0.125, 0]))
        pg_ok = check_mark(0.3, OWN)
        pg_t = label("page", CAPTION, INK)
        pg = VGroup(pg_ok, pg_t).arrange(RIGHT, buff=0.15)
        pg.move_to(win.get_corner(UP + LEFT) + np.array([0.3 + pg.width / 2, -0.62, 0]))
        btn = RoundedRectangle(width=1.45, height=0.5, corner_radius=0.12, stroke_color=INK, stroke_width=2) \
            .set_fill(S.GREY, 0.25)
        btnt = label("Predict", CAPTION, INK).move_to(btn)
        button = VGroup(btn, btnt).move_to(win.get_corner(DOWN + LEFT) + np.array([0.3 + 0.725, 0.5, 0]))
        page_g = VGroup(win, wbar, wdots, pg, button)
        dev = laptop(2.2)
        dbtn = RoundedRectangle(width=0.95, height=0.36, corner_radius=0.1, stroke_color=INK, stroke_width=2) \
            .set_fill(S.GREY, 0.25)
        dbt = label("Predict", CAPTION, INK)
        dbtn.stretch_to_fit_width(dbt.width + 0.2)
        dbt.move_to(dbtn)
        dbutton = VGroup(dbtn, dbt).move_to(dev.screen).shift(LEFT * 0.22)
        dok = check_mark(0.28, OWN).next_to(dbutton, RIGHT, buff=0.1)
        devt = label("developer's laptop", CAPTION, LAPTOP).next_to(dev, DOWN, buff=0.1)
        dev_g = VGroup(dev, dbutton, dok, devt)
        dok.set_opacity(0)
        call2 = VGroup(page_g, dev_g)
        place(page_g, left=-4.6, top=BOTTOM_TOP - 0.15)
        place(dev_g, left=page_g.get_right()[0] + 1.0, cy=page_g.get_center()[1])
        inside(call2, "alarm 2 callout")
        spin = spinner().next_to(button, RIGHT, buff=0.3)
        nerr = label("Network Error", CAPTION, ERR).next_to(button, RIGHT, buff=0.25)
        guard(nerr.get_right()[0] <= win.get_right()[0] - 0.1, "Network Error leaves the window")
        guard(dbutton.width + dok.width + 0.1 <= dev.screen.width - 0.05, "dev laptop button too wide")
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(bell2, scale=1.4), run_time=0.5)
            self.play(Wiggle(bell2), run_time=0.8)
            vo.wait_until("The page loads")
            self.play(FadeIn(VGroup(win, wbar, wdots), shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(pg, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("but the Predict")
            self.play(FadeIn(button), FadeIn(spin), run_time=0.4)
            self.play(Indicate(btn, color=TURN, scale_factor=1.05),
                      Rotate(spin, -4 * PI, about_point=spin.get_arc_center()), run_time=1.4, rate_func=linear)
            self.play(FadeOut(spin), FadeIn(nerr), btn.animate.set_stroke(ERR), run_time=0.5)
            vo.wait_until("On the developer")
            self.play(FadeIn(VGroup(dev, dbutton, devt), shift=LEFT * 0.1), run_time=0.6)
            self.play(Indicate(dbtn, color=TURN, scale_factor=1.05), run_time=0.6)
            self.play(dok.animate.set_opacity(1), run_time=0.4)
        self.play(FadeOut(call2), FadeOut(nerr), run_time=0.5)

        # ------------------------------------------------------------ beat 3: capacity
        c9 = grey_chip("launch morning · 9:00")
        place(c9, left=-6.55, top=3.55)
        a_in2 = P["a_in"].copy().shift(RIGHT * 0.3)
        traffic = label("traffic ×2", CAPTION, S.GREY).next_to(P["brt"], DOWN, buff=0.12).align_to(P["brt"], LEFT)
        guard(traffic.get_bottom()[1] >= VPC_Y1 + 0.02, "traffic label touches the VPC")
        auto = chip("autoscaler · 3 → 6", TOOL, size=CAPTION)
        place(auto, left=1.0, cy=2.3)
        apart(auto, P["brt"], "autoscaler chip / browser label")
        new = VGroup(*[replica_box().move_to([x, ROW2, 0]) for x in REP_X])
        bell3 = bell(0.42).move_to([3.0, HEAD_Y, 0])
        lane = -0.68
        trips = [[n.get_bottom(), [n.get_bottom()[0], lane, 0], [4.15, lane, 0], P["db"].get_left() + DOWN * 0.1]
                 for n in new]
        tmc = mono("too many connections", CAPTION, ERR)
        br = Line([new[1].get_left()[0], -1.2, 0], [new[2].get_right()[0], -1.2, 0], color=ERR, stroke_width=3)
        ticks = VGroup(*[Line([x, -1.2, 0], [x, -1.05, 0], color=ERR, stroke_width=3)
                         for x in (new[1].get_left()[0], new[2].get_right()[0])])
        tmc.next_to(br, DOWN, buff=0.12)
        cpu = cpu_gauge(0.12)
        cpu.next_to(tmc, RIGHT, buff=0.5)
        cap_g = VGroup(br, ticks, tmc, cpu)
        inside(cap_g, "alarm 3 labels")
        with self.voiceover(SAY[3]) as vo:
            self.play(*swap_text(clock, clock[0], c9), run_time=0.7)
            vo.wait_until("traffic doubles")
            self.play(Create(a_in2), FadeIn(traffic, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("and the autoscaler")
            self.play(FadeIn(auto, shift=DOWN * 0.1), run_time=0.5)
            self.play(LaggedStart(*[GrowFromCenter(n) for n in new], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("The newest ones")
            dots = [packet_dot().move_to(t[0]) for t in trips]
            self.add(dots[0])
            self.play(MoveAlongPath(dots[0], _poly(trips[0])), run_time=1.0)
            ok4 = check_mark(0.3, OWN).move_to([new[0].get_x(), -1.2, 0])   # on the bracket's row, under it
            self.play(FadeOut(dots[0]), FadeIn(ok4), run_time=0.4)
            self.add(dots[1], dots[2])
            self.play(MoveAlongPath(dots[1], _poly(trips[1])), MoveAlongPath(dots[2], _poly(trips[2])), run_time=0.9)
            sp = spark().move_to(P["db"].get_left())
            self.play(FadeIn(sp, scale=1.6), *[d.animate.set_color(ERR) for d in dots[1:]],
                      *[n.frame.animate.set_stroke(ERR).set_fill(ERR, 0.15) for n in new[1:]], run_time=0.5)
            self.play(FadeOut(sp), *[FadeOut(d) for d in dots[1:]], Create(br), Create(ticks),
                      FadeIn(tmc, shift=UP * 0.1), FadeIn(bell3, scale=1.4), run_time=0.6)
            vo.wait_until("while their processors")
            self.play(FadeIn(cpu, shift=LEFT * 0.1), run_time=0.5)
            self.play(Indicate(cpu, color=S.GREY, scale_factor=1.1), Wiggle(bell3), run_time=0.9)
        self.play(FadeOut(cap_g), FadeOut(auto), FadeOut(ok4), run_time=0.5)

        # ------------------------------------------------------------ beat 4: the key in the image
        lay_names = ["base OS", "Python + packages", "app code"]
        layers = VGroup(*[layer_bar(t, 3.6, 0.36, CTR, size=CAPTION) for t in reversed(lay_names)])
        kg = key_glyph(0.24)
        kt = mono("ENV API_KEY=…", CAPTION, INK)
        top_l = VGroup(box(3.6, 0.36, CTR, fill_opacity=0.2, radius=0.08), VGroup(kg, kt).arrange(RIGHT, buff=0.15))
        top_l[1].move_to(top_l[0])
        stack = VGroup(top_l, *layers).arrange(DOWN, buff=0.0)
        for m in [top_l[1], *[L.text for L in layers]]:
            m.set_opacity(0)
        name = mono(IMAGE, CAPTION, CTR)
        shelf = Line(LEFT * 2.6, RIGHT * 2.6, color=S.GREY, stroke_width=4)
        shelf_t = label("registry", CAPTION, S.GREY)
        img = VGroup(name, stack).arrange(DOWN, buff=0.36)      # the layers spread 0.24 up
        img_g = VGroup(img, shelf, shelf_t)
        shelf.next_to(stack, DOWN, buff=0.06)
        shelf_t.next_to(shelf, LEFT, buff=0.2)
        place(img_g, cx=0.4, bottom=-3.4)
        guard(img_g.get_top()[1] <= BOTTOM_TOP + 0.05, "image overlaps the map")
        inside(img_g, "image group")
        scan = Line(LEFT * 1.95, RIGHT * 1.95, color=TURN, stroke_width=5).move_to(stack.get_top())
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeIn(img_g, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("The production key")
            self.add(scan)
            self.play(scan.animate.move_to(stack.get_bottom()),
                      stack.animate.arrange(DOWN, buff=0.08).align_to(shelf, DOWN).shift(UP * 0.06),
                      run_time=1.0)
            self.play(FadeOut(scan), *[L.text.animate.set_opacity(1) for L in layers],
                      *[L.box.animate.set_fill(CTR, 0.05) for L in layers], top_l[1].animate.set_opacity(1),
                      run_time=0.6)
            self.play(top_l[0].animate.set_stroke(ERR, 4), kg.animate.set_fill(KEY, 0.9), run_time=0.5)
            self.play(Indicate(kg, color=KEY, scale_factor=1.5), run_time=0.9)
        guard(name.get_bottom()[1] > stack.get_top()[1], "image name overlaps its layers")

        # ------------------------------------------------------------ beat 5: the plan
        bells = VGroup(bell1, bell2, bell3)
        thumb = VGroup(P["shapes"], reps, new, a_in2, bells)
        icons = [self._icon(k) for k in range(6)]
        names = ["addresses", "routes and NAT", "the browser", "configuration", "capacity", "the database"]
        xs = [-5.3 + 2.12 * k for k in range(6)]
        items = VGroup()
        for k, (ic, nm) in enumerate(zip(icons, names)):
            ic.move_to([xs[k], 0.05, 0])
            t = label(nm, CAPTION, INK).next_to(ic, DOWN, buff=0.18).set_y(-0.85)
            items.add(VGroup(ic, t))
        for k in range(5):
            apart(items[k][1], items[k + 1][1], f"plan labels {k}/{k + 1}")
        order = Line([-6.2, -1.45, 0], [6.2, -1.45, 0], color=S.GREY, stroke_width=3).add_tip(tip_length=0.2)
        inside(VGroup(items, order), "plan row")
        cues = ["We go from addresses", "to routes and NAT", "to the browser", "to configuration", "to capacity",
                "finally to the database"]
        with self.voiceover(SAY[5]) as vo:
            rep_words = VGroup(*[r.text for r in (*reps, *new)])
            self.play(FadeOut(words), FadeOut(rep_words), FadeOut(itag), FadeOut(clock), FadeOut(img_g),
                      FadeOut(traffic), run_time=0.6)
            for r in (*reps, *new):                   # out of their boxes for good (no snap-back on scale)
                r.remove(r.text)
            self.play(thumb.animate.scale(0.5).move_to([0, 2.4, 0]), run_time=1.0)
            guard(thumb.get_top()[1] <= 3.55, "thumbnail out of frame")
            vo.wait_until("one mechanism")
            self.play(LaggedStart(*[pulse(b, 1.6) for b in bells], lag_ratio=0.5), run_time=1.6)
            for k, c in enumerate(cues):
                vo.wait_until(c)
                self.play(FadeIn(items[k], shift=UP * 0.15), run_time=0.45)
            self.play(Create(order), run_time=0.6)
        guard(thumb.get_bottom()[1] >= items.get_top()[1] + 0.2, "thumbnail touches the plan")

        # ------------------------------------------------------------ beat 6: how to read the tags
        lr = lref(16, "71")
        hdr = _header_text("cheese-app-v0/api-service/docker-shell.sh · lines 19–27")
        hdr_t = label("a code panel quotes the repo", CAPTION, S.GREY)
        spec = VGroup(hdr, hdr_t).arrange(DOWN, buff=0.15).move_to([0, 0.6, 0])
        live = grey_chip("no live runs · concepts, not clicks").move_to([0, -1.0, 0])
        pointer = arrow_(lr.get_left() + LEFT * 1.6 + DOWN * 0.5, lr.get_left() + LEFT * 0.08, S.GREY, stroke=3)
        inside(VGroup(lr, spec, live), "beat 6")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(thumb), FadeOut(items), FadeOut(order), run_time=0.6)
            self.play(FadeIn(lr), Create(pointer), run_time=0.6)
            self.play(pulse(lr, 1.15), run_time=0.8)
            vo.wait_until("behind each idea")
            self.play(FadeIn(spec, shift=UP * 0.1), FadeOut(pointer), run_time=0.6)
            self.play(pulse(hdr, 1.08), run_time=0.8)
            vo.wait_until("Nothing here")
            self.play(FadeIn(live, shift=UP * 0.1), run_time=0.5)
            self.play(pulse(live, 1.08), run_time=0.7)
        self.play(FadeOut(VGroup(lr, spec, live)), run_time=0.7)
        self.wait(0.3)

    # ---------------------------------------------------------------- the plan's six icons
    @staticmethod
    def _icon(k):
        if k == 0:                                    # addresses: a house with a door
            h = house("x")
            dr = RoundedRectangle(width=0.22, height=0.36, corner_radius=0.03, stroke_color=CLOUD, stroke_width=3) \
                .set_fill(S.BG, 1)
            dr.align_to(h.body, DOWN).match_x(h.body)
            return VGroup(h.shape, dr)
        if k == 1:                                    # routes and NAT: two PINK rows
            rows = VGroup(*[RoundedRectangle(width=1.5, height=0.32, corner_radius=0.06, stroke_color=ROUTE,
                                             stroke_width=3).set_fill(ROUTE, 0.15) for _ in range(2)])
            rows.arrange(DOWN, buff=0.1)
            divs = VGroup(*[Line(r.get_top(), r.get_bottom(), color=ROUTE, stroke_width=2).shift(LEFT * 0.15)
                            for r in rows])
            return VGroup(rows, divs)
        if k == 2:                                    # the browser
            return browser_glyph(1.2)
        if k == 3:                                    # configuration: a TEAL image + GREEN cards
            slabs = VGroup(*[RoundedRectangle(width=0.9, height=0.18, corner_radius=0.04, stroke_color=CTR,
                                              stroke_width=2).set_fill(CTR, 0.2 + 0.1 * j) for j in range(3)])
            slabs.arrange(DOWN, buff=0.05)
            cards = VGroup(*[RoundedRectangle(width=0.5, height=0.32, corner_radius=0.04, stroke_color=OWN,
                                              stroke_width=2).set_fill(OWN, 0.2) for _ in range(2)])
            cards.arrange(DOWN, buff=0.06)
            return VGroup(slabs, cards).arrange(RIGHT, buff=0.18)
        if k == 4:                                    # capacity: a grid of slots
            return VGroup(*[Square(0.2, stroke_color=CLOUD, stroke_width=2)
                            .set_fill(ROUTE if j < 9 else CLOUD, 0.6 if j < 9 else 0.05)
                            for j in range(15)]).arrange_in_grid(3, 5, buff=0.06)
        return cylinder(None, None, CLOUD, w=0.95, h=0.6)        # the database
