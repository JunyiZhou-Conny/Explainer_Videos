"""S04 · The browser lives outside the VPC (V3: two paths, three URLs, one front door).
Lecture: L16 23–24, 27, 30–32, 62–64, 71; L10 11.

Beats (script.md "## S04", one voiceover block each):
 0  LECTURE 16 · 30, 62–64. V3 (TwoPaths, the lecture's picture with AWS names): the BLUE VPC on
    the right (public subnet with the ALB, private app subnet with "FastAPI tasks ×3"), the GREY
    visitor's laptop with a browser top left, the BLUE static host / CDN app.example.com bottom
    left. Path 1: HTML, CSS, JS fly from the static host into the browser and unpack; the JS gear
    turns on the visitor's laptop.
 1  YELLOW traces run round the VPC border and the visitor's laptop; slide 64's caption in GREY;
    a PINK "API requests" arrow from the laptop to the ALB (the front door).
 2  The canvas dims; CODE(.env.development: 4) over CODE(src/services/Common.js: 2), both lit;
    a PINK arrow from the variable on line 4 to process.env.NEXT_PUBLIC_BASE_API_URL on line 2;
    localhost:9000 lights.
 3  Race, version 1: the panels leave, the lit URL becomes the browser's request packet
    "→ localhost:9000"; it runs to the laptop's edge, the edge flashes, and it lands at the
    visitor's own empty door ":9000 · nothing listens": RED spark, the URL turns RED.
 4  Version 2: the destination swaps to 10.0.2.5:8000; the packet wanders along the laptop's edge
    and evaporates RED (GREY note: private address, no route on the internet); the ORANGE internet
    and the VPC never see it. Version 3: "→ api.example.com": PINK DNS lookup arrows to the
    internet and back, the packet crosses to the ALB, a PINK arrow on to a task, GREEN ticks.
 5  LECTURE 16 · 32, 24. The V3 canvas leaves; the development line turns into
    CODE(.env.production: 2), /api lit. Below it slide 32's layout B (tag lecture's picture):
    browser → one public front door app.example.com → "/" Next.js server, "/api/*" FastAPI
    10.0.2.5:8000.
 6  The panel leaves, the front door moves up; slide 24's two rule cards write in under it
    (Nginx = ALB rule, YELLOW "="); 10.0.2.5 inside a small BLUE VPC outline; GREY chip
    "separate static host → name the public API address".
 7  The 10.0.2.5 pulses YELLOW inside the BLUE outline; a RED ✗ chip "never in browser code"
    beside the browser.
 8  The rule cards leave; a JS file glyph lands in the browser with the GREY chip
    "NEXT_PUBLIC_… → compiled in at build time · every visitor downloads it". The BLUE NAT Gateway
    appears below the front door with a one-way PINK "out only" arrow; an inbound arrow from the
    browser bounces off it RED.
 9  The canvas fades. TAKEAWAY, row by row as spoken; then an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circumscribe,
    Create,
    FadeIn,
    FadeOut,
    Line,
    FadeTransform,
    GrowArrow,
    Indicate,
    LaggedStart,
    ReplacementTransform,
    VGroup,
    Write,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S04"]

assert TASK_IP == "10.0.2.5" and API_HOST == "api.example.com" and APP_HOST == "app.example.com"
DEV = "cheese-app-v0/frontend-ai-chatbot/env.development"
PROD = "cheese-app-v0/frontend-ai-chatbot/env.production"
JS = "cheese-app-v0/frontend-ai-chatbot/src/services/Common.js"
assert source_line(DEV, 4) == "NEXT_PUBLIC_BASE_API_URL=http://localhost:9000", source_line(DEV, 4)
assert source_line(PROD, 2) == "NEXT_PUBLIC_BASE_API_URL=/api", source_line(PROD, 2)
assert "process.env.NEXT_PUBLIC_BASE_API_URL" in source_line(JS, 2), source_line(JS, 2)

TAKEAWAY = ("code runs in the browser → it is outside the VPC → call the public HTTPS endpoint "
            "(ALB / domain), never `localhost` or `10.x` · NAT doesn't help inbound")

SAFE_L, SAFE_R, SAFE_B, SAFE_T = -6.6, 6.6, -3.6, 3.6


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


def within(a, b, name=""):
    """a's bounding box lies inside b's."""
    guard(a.get_left()[0] >= b.get_left()[0] and a.get_right()[0] <= b.get_right()[0]
          and a.get_bottom()[1] >= b.get_bottom()[1] and a.get_top()[1] <= b.get_top()[1],
          f"{name} not inside")


def flash(mob, color=TURN, k=1.12, run_time=0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def outline_flash(mob, color=TURN, run_time=0.8):
    """A ring traced round mob (Indicate would paint a filled card solid)."""
    return Circumscribe(mob, color=color, buff=0.08, run_time=run_time)


def at(p, x, y):
    """A copy of mobject p moved so its centre is at (x, y): for layout checks."""
    return p.copy().move_to([x, y, 0])


def unwrap(scene, anim):
    """Remove the wrapper groups an AnimationGroup (and the ones nested in it) leaves on the scene."""
    grp = getattr(anim, "group", None)
    if grp is not None and grp in scene.mobjects:
        scene.remove(grp)
    for a in getattr(anim, "animations", []):
        unwrap(scene, a)


class BrowserOutside(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0 · two trips
        tp = TwoPaths(show=())
        zone = tp.vzone.frame
        chip_aws = aws_chip()
        place(chip_aws, left=-6.45, top=3.55)
        inside(chip_aws, "AWS chip")
        apart(chip_aws, tp, "AWS chip / canvas")
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, None, 16, "30, 62–64")
            self.add(tp)
            self.play(*tp.parts_in("vpc"), FadeIn(chip_aws), run_time=0.7)
            self.play(*tp.parts_in("alb", "tasks"), run_time=0.6)
            vo.wait_until("Loading a page")
            self.play(*tp.parts_in("visitor"), run_time=0.6)
            self.play(*tp.parts_in("static"), run_time=0.6)
            vo.wait_until("First the browser")
            self.play(*tp.parts_in("files"), run_time=0.6)
            self.play(*tp.deliver(run_time=1.4))
            vo.wait_until("Then that JavaScript")
            self.play(*tp.unpack(), run_time=0.6)
            self.play(tp.spin(1.0, run_time=1.4))
            vo.wait_until("and calls the API")
            self.play(tp.spin(0.6, run_time=1.0), flash(tp.parts["alb"], CLOUD, 1.06, run_time=1.0))

        # ========================================================== 1 · outside the VPC
        cap = VGroup(note("Static delivery stays outside the VPC;"),
                     note("application requests enter at the ALB.")).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        place(cap, left=-6.35, cy=-0.75)
        inside(cap, "slide 64 caption")
        apart(cap, zone, "caption / laptop")
        apart(cap, tp.static, "caption / static host")
        guard(cap.get_right()[0] <= tp.vpc_box.get_left()[0] - 0.1, "caption runs into the VPC")
        y_req = tp.alb.get_center()[1]
        req = arrow_([zone.get_right()[0] + 0.02, y_req, 0], [tp.alb.get_left()[0] - 0.02, y_req, 0], ROUTE)
        req_l = VGroup(label("API", CAPTION, ROUTE), label("requests", CAPTION, ROUTE)).arrange(DOWN, buff=0.04)
        place(req_l, cx=(zone.get_right()[0] + tp.vpc_box.get_left()[0]) / 2, top=req.get_bottom()[1] - 0.08)
        apart(req_l, cap, "request label / caption")
        apart(req_l, zone, "request label / laptop")
        apart(req_l, tp.vpc_box, "request label / VPC")
        with self.voiceover(SAY[1]) as vo:
            self.play(*tp.outline(), run_time=1.6)
            self.play(FadeIn(cap[0], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Static files never")
            self.play(flash(tp.static, CLOUD, 1.06), tp.spin(0.5, run_time=0.8))
            vo.wait_until("and every API request")
            self.play(FadeIn(cap[1], shift=UP * 0.1), run_time=0.5)
            self.play(GrowArrow(req), FadeIn(req_l), run_time=0.8)
            vo.wait_until("the front door")
            self.play(flash(tp.parts["alb"], TURN, 1.1, run_time=0.8))

        # ========================================================== 2 · the course app's development URL
        dev = src_panel(DEV, 4)
        js = src_panel(JS, 2, wrap=True)
        VGroup(dev, js).arrange(DOWN, buff=0.9)
        place(dev, cx=0)
        place(js, cx=0)
        VGroup(dev, js).set_y(0)
        inside(VGroup(dev, js), "dev panels", t=3.05)
        var4 = dev.span(4, "NEXT_PUBLIC_BASE_API_URL")
        url4 = dev.span(4, "http://localhost:9000")
        var2 = js.span(2, "process.env.NEXT_PUBLIC_BASE_API_URL")
        apart(dev, js, "dev panel / Common.js panel")
        # an elbow: down from line 4's variable, right above Common.js's header, down onto line 2's
        y_mid = (dev.get_bottom()[1] + js.header.get_top()[1]) / 2
        x_dn = min(max(var2.get_center()[0], js.header.get_right()[0] + 0.3), var2.get_right()[0] - 0.3)
        guard(x_dn >= js.header.get_right()[0] + 0.2, "link would cross the Common.js header")
        guard(dev.get_bottom()[1] - js.header.get_top()[1] >= 0.3, "no room for the link between the panels")
        x_up = var4.get_center()[0]
        link = VGroup(Line([x_up, var4.get_bottom()[1] - 0.05, 0], [x_up, y_mid, 0], color=ROUTE, stroke_width=4),
                      Line([x_up, y_mid, 0], [x_dn, y_mid, 0], color=ROUTE, stroke_width=4),
                      arrow_([x_dn, y_mid + 0.02, 0], [x_dn, var2.get_top()[1] + 0.04, 0], ROUTE, stroke=4, buff=0))
        dev_bar, js_bar = dev.bar(4), js.bar(2)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(cap, req, req_l)), tp.dim_to(0.12), run_time=0.6)
            self.play(FadeIn(dev, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("In development")
            self.play(FadeIn(dev_bar), run_time=0.4)
            vo.wait_until("the frontend takes")
            self.play(FadeIn(js, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(js_bar), run_time=0.4)
            vo.wait_until("from next public")
            self.play(Create(link, lag_ratio=1.0), var4.animate.set_color(ROUTE), var2.animate.set_color(ROUTE), run_time=0.8)
            vo.wait_until("and that variable says")
            self.play(url4.animate.set_color(TURN), run_time=0.4)
            self.play(flash(url4, TURN, 1.12), run_time=0.7)
            vo.wait_until("On the developer")
            self.play(flash(url4, OWN, 1.08), run_time=0.8)

        # ========================================================== 3 · version 1: localhost
        y_row = 0.85
        pk = Packet("", "localhost:9000", color=LAPTOP, slot=len(API_HOST))
        x_start = -6.35 + pk.width / 2
        dr = door(":9000", LAPTOP, h=0.5, label_side=UP)
        place(dr, right=zone.get_right()[0] - 0.12, cy=y_row + 0.15)
        dr_note = VGroup(label("nothing", CAPTION, S.GREY), label("listens", CAPTION, S.GREY)) \
            .arrange(DOWN, buff=0.02, aligned_edge=RIGHT)
        place(dr_note, right=dr.get_right()[0], bottom=dr.get_top()[1] + 0.04)
        x_end = dr.frame.get_left()[0] - 0.1 - pk.width / 2
        guard(x_end - x_start >= 0.4, "localhost packet has no room to move")
        p0, p1 = [x_start, y_row, 0], [x_end, y_row, 0]
        for x in (x_start, x_end):
            within(at(pk, x, y_row), zone, "localhost packet in the laptop")
            apart(at(pk, x, y_row), tp.browser, "packet / browser")
            apart(at(pk, x, y_row), tp.vzone.caption, "packet / laptop caption")
            apart(at(pk, x, y_row), tp.gear_, "packet / gear")
        apart(dr, tp.parts["gear"], "door / gear")
        apart(dr_note, tp.parts["visitor"][2], "door note / page URL")
        apart(dr_note, tp.parts["gear"], "door note / gear")
        within(VGroup(dr, dr_note), zone, "door in the laptop")
        edge = zone.copy().set_stroke(TURN, 6).set_fill(opacity=0)
        with self.voiceover(SAY[3]) as vo:
            pk.move_to(p0)
            self.play(FadeOut(VGroup(js, link, js_bar)), run_time=0.4)
            self.play(FadeTransform(url4.copy(), pk), FadeOut(VGroup(dev, dev_bar)), tp.undim(), run_time=1.0)
            vo.wait_until("and localhost means")
            self.play(pk.travel([p0, [x_end + 0.4, y_row, 0]], run_time=1.0, clamp=False),
                      FadeIn(edge, rate_func=lambda t: np.sin(np.pi * t)), run_time=1.0)
            self.remove(edge)
            self.play(pk.travel([[x_end + 0.4, y_row, 0], p1], run_time=0.5, clamp=False))
            self.play(FadeIn(dr), run_time=0.5)
            vo.wait_until("Nothing listens there")
            self.play(FadeIn(dr_note, shift=DOWN * 0.1), run_time=0.5)
            sp = spark(0.2).move_to(dr.frame.get_left() + LEFT * 0.05)
            vo.wait_until("so the request fails")
            self.play(FadeIn(sp, scale=0.4), *pk.recolor(ERR), pk.dst.animate.set_color(ERR), run_time=0.6)
            vo.wait_until("That is the second alarm")
            self.play(outline_flash(pk, ERR), FadeOut(sp), run_time=0.8)

        # ========================================================== 4 · version 2: 10.0.2.5; version 3: the public name
        cl = internet_cloud(1.6, "internet")
        gap_x = (zone.get_right()[0] + tp.vpc_box.get_left()[0]) / 2
        place(cl, cx=gap_x, top=2.75)
        apart(cl, zone, "internet / laptop")
        apart(cl, tp.vpc_box, "internet / VPC")
        apart(cl, chip_aws, "internet / AWS chip")
        why = VGroup(mono(f"{TASK_IP} · private address", CAPTION, ERR),
                     note("no route to it on the internet")).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        place(why, left=-6.35, top=zone.get_bottom()[1] - 0.25)
        apart(why, tp.static, "why note / static host")
        guard(why.get_right()[0] <= tp.vpc_box.get_left()[0] - 0.1, "why note runs into the VPC")
        x_edge = zone.get_right()[0] - 0.08 - pk.width / 2
        wander = [p1, [x_edge, y_row, 0], [x_edge - 0.5, y_row + 0.08, 0], [x_edge, y_row, 0],
                  [x_edge - 0.3, y_row + 0.04, 0], [x_edge, y_row, 0]]
        for p in wander:
            within(at(pk, p[0], p[1]), zone, "wandering packet in the laptop")
            apart(at(pk, p[0], p[1]), tp.vzone.caption, "wandering packet / caption")
            apart(at(pk, p[0], p[1]), tp.gear_, "wandering packet / gear")
        pv = Packet("", API_HOST, color=TURN)
        xv0 = -6.35 + pv.width / 2
        y_alb = tp.alb.get_center()[1]
        xv1 = tp.alb.get_left()[0] - 0.06 - pv.width / 2
        apart(at(pv, xv0, y_row), tp.browser, "public packet / browser")
        apart(at(pv, xv0, y_row), tp.vzone.caption, "public packet / caption")
        apart(at(pv, xv1, y_alb), cl, "public packet / internet")
        apart(at(pv, xv1, y_alb), why, "public packet / why note")
        pv_start = at(pv, xv0, y_row)
        dns_a = arrow_(pv_start.get_corner(UP + RIGHT) + LEFT * 0.75, cl.shape.get_left() + UP * 0.05,
                       ROUTE, stroke=3, buff=0.04)
        dns_b = arrow_(cl.shape.get_left() + DOWN * 0.25 + RIGHT * 0.05, pv_start.get_corner(UP + RIGHT) + LEFT * 0.1,
                       ROUTE, stroke=3, buff=0.04)
        apart(dns_b, cl.label, "DNS answer arrow / internet label")
        dns_l = mono("DNS", CAPTION, ROUTE)
        place(dns_l, cx=gap_x, top=cl.label.get_bottom()[1] - 0.1)
        apart(dns_l, dns_b, "DNS label / answer arrow")
        apart(dns_l, tp.vpc_box, "DNS label / VPC")
        apart(dns_l, tp.parts["gear"], "DNS label / gear")
        apart(dns_l, tp.parts["visitor"][2], "DNS label / page URL")
        to_task = arrow_(tp.alb.get_right(), tp.tasks[0].get_left(), ROUTE, stroke=4)
        ok_alb = tick_mark(0.34).move_to(tp.tasks[0])
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(dr, dr_note)), *pk.recolor(LAPTOP), pk.dst.animate.set_color(INK),
                      FadeIn(cl), run_time=0.6)
            self.play(pk.travel([p1, p0], run_time=0.7, clamp=False))
            vo.wait_until("Swap in the private")
            self.play(*pk.set_dst(TASK_IP + ":8000"), run_time=0.7)
            vo.wait_until("and the request never")
            self.play(pk.travel(wander, run_time=2.2, clamp=False))
            gone = pk.drop()
            self.play(gone, run_time=0.8)
            unwrap(self, gone)
            vo.wait_until("that address means")
            self.play(FadeIn(why, shift=UP * 0.1), run_time=0.5)
            self.play(flash(tp.vpc_box, CLOUD, 1.02, run_time=0.8), flash(cl, SHARED, 1.06, run_time=0.8))
            vo.wait_until("The public HTTPS name")
            pv.move_to([xv0, y_row, 0])
            self.play(FadeOut(why), FadeIn(pv, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("DNS")
            self.play(GrowArrow(dns_a), FadeIn(dns_l), run_time=0.6)
            self.play(flash(cl, ROUTE, 1.08, run_time=0.4))
            self.play(GrowArrow(dns_b), run_time=0.5)
            vo.wait_until("the load balancer")
            self.play(pv.travel([[xv0, y_row, 0], [xv1, y_alb, 0]], run_time=1.0, clamp=False),
                      FadeOut(VGroup(dns_a, dns_b, dns_l)), run_time=1.0)
            self.play(flash(tp.alb, CLOUD, 1.1), run_time=0.5)
            vo.wait_until("then a task")
            self.play(GrowArrow(to_task), run_time=0.5)
            self.play(FadeIn(ok_alb, scale=0.5), *pv.recolor(OWN), run_time=0.5)

        # ========================================================== 5 · production: a relative path, layout B
        prod = src_panel(PROD, 2)
        dev2 = src_panel(DEV, 4)
        place(prod, cx=0, top=2.95)
        dev2.move_to(prod)
        inside(prod, "production panel", t=3.05)
        api_sp = prod.span(2, "/api")
        prod_bar = prod.bar(2)
        fd = FrontDoor()
        place(fd, cx=0, top=prod.get_bottom()[1] - 0.55)
        inside(fd, "front door")
        tag_fd = lecture_pic_tag()
        place(tag_fd, left=-6.45, top=3.55)          # top left, clear of the lecture tag (top right)
        apart(tag_fd, prod, "picture tag / panel")
        apart(tag_fd, lr, "picture tag / lecture tag")
        apart(tag_fd, fd.next, "picture tag / Next.js box")
        apart(fd, prod, "front door / panel")
        a_in, (a_root, l_root), (a_api, l_api) = fd.arrows
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(tp, cl, pv, ok_alb, to_task, chip_aws)), run_time=0.6)
            lr = lref_swap(self, lr, 16, "32, 24")
            self.play(FadeIn(dev2), run_time=0.4)
            self.play(ReplacementTransform(dev2, prod), run_time=0.9)
            self.play(FadeIn(prod_bar), api_sp.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("A relative path")
            self.play(FadeIn(fd.browser), FadeIn(fd.door), FadeIn(tag_fd), run_time=0.6)
            self.play(GrowArrow(a_in), run_time=0.6)
            vo.wait_until("That works when")
            self.play(flash(fd.door, CLOUD, 1.08), run_time=0.6)
            self.play(GrowArrow(a_root), FadeIn(l_root), FadeIn(fd.next), run_time=0.7)
            vo.wait_until("the lecture's layout B")
            self.play(outline_flash(tag_fd, INK), run_time=0.6)
            vo.wait_until("and routes slash api")
            self.play(GrowArrow(a_api), FadeIn(l_api), FadeIn(fd.api), run_time=0.7)
            self.play(flash(l_api, TURN, 1.2), flash(api_sp, TURN, 1.2), run_time=0.7)

        # ========================================================== 6 · slide 24's rule, twice
        fd_y = 3.0 - fd.height / 2
        rc = RuleCards()
        place(rc, left=-6.35, bottom=-3.3)
        sep = VGroup(label("separate static host", CAPTION, S.GREY), label("→ name the public", CAPTION, S.GREY),
                     label("API address", CAPTION, S.GREY)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        sep_box = box(sep.width + 0.4, sep.height + 0.3, S.GREY, fill=S.BG, fill_opacity=0.95)
        sep_box.move_to(sep)
        sep_g = VGroup(sep_box, sep)
        place(sep_g, right=6.45, cy=rc.alb.get_center()[1])
        inside(rc, "rule cards")
        inside(sep_g, "separate-host chip")
        apart(sep_g, rc, "separate-host chip / rule cards")
        fd_at = fd.copy().set_y(fd_y)
        apart(rc, fd_at, "rule cards / front door")
        inside(fd_at, "front door (up)", t=3.05)
        apart(fd_at, lr, "front door / lecture tag")
        apart(tag_fd, fd_at, "picture tag / front door (up)")
        apart(sep_g, fd_at, "separate-host chip / front door")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(prod, prod_bar)), run_time=0.5)
            self.play(fd.animate.set_y(fd_y), run_time=0.7)
            self.play(FadeIn(rc.nginx, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("as an Nginx proxy pass")
            self.play(outline_flash(rc.nginx, OWN), run_time=0.6)
            vo.wait_until("or a load balancer")
            self.play(Write(rc.eq), FadeIn(rc.alb, shift=UP * 0.15), run_time=0.7)
            self.play(Create(rc.vpc), run_time=0.5)
            vo.wait_until("With a separate static host")
            self.play(FadeIn(sep_g, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("the public API address")
            self.play(outline_flash(sep_g, INK), run_time=0.7)

        # ========================================================== 7 · the private address lives in the proxy
        never = VGroup(x_mark(0.28), label("never in browser code", CAPTION, ERR)).arrange(RIGHT, buff=0.12)
        never_box = box(never.width + 0.35, never.height + 0.25, ERR, fill=S.BG, fill_opacity=0.95)
        never_box.move_to(never)
        never_g = VGroup(never_box, never)
        place(never_g, left=-6.45, top=fd.browser.get_bottom()[1] - 0.2)
        inside(never_g, "never chip")
        apart(never_g, fd.browser, "never chip / browser")
        apart(never_g, rc, "never chip / rule cards")
        apart(never_g, a_in, "never chip / browser arrow")
        apart(never_g, fd.door, "never chip / front door")
        with self.voiceover(SAY[7]) as vo:
            self.play(rc.ip.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("in the proxy")
            self.play(flash(rc.ip, TURN, 1.25), rc.vpc.animate.set_stroke(width=5), run_time=0.8)
            vo.wait_until("inside the VPC")
            self.play(flash(rc.vpc, CLOUD, 1.3), run_time=0.7)
            vo.wait_until("Never in browser code")
            self.play(FadeIn(never_g, shift=RIGHT * 0.15), outline_flash(fd.browser, ERR), run_time=0.7)

        # ========================================================== 8 · NEXT_PUBLIC is public; NAT does not help inbound
        jsf = VGroup(file_glyph(0.42, TURN), mono("JS", CAPTION, TURN)).arrange(DOWN, buff=0.04)
        jsf_to = fd.browser.page.get_center()
        jsf.move_to([-5.2, -1.0, 0])
        pub = VGroup(mono("NEXT_PUBLIC_…", CAPTION, INK), label("→ compiled in at build time", CAPTION, S.GREY),
                     label("every visitor downloads it", CAPTION, S.GREY)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        pub_box = box(pub.width + 0.4, pub.height + 0.3, S.GREY, fill=S.BG, fill_opacity=0.95)
        pub_box.move_to(pub)
        pub_g = VGroup(pub_box, pub)
        place(pub_g, left=-6.45, bottom=-3.3)
        inside(pub_g, "public chip")
        apart(pub_g, fd.door, "public chip / front door")
        apart(pub_g, a_in, "public chip / browser arrow")
        nat = box(2.0, 0.85, CLOUD, fill_opacity=0.15, stroke=3)
        natt = VGroup(label("NAT", CAPTION, INK), label("Gateway", CAPTION, INK)).arrange(DOWN, buff=0.03)
        nat_g = VGroup(nat, natt)
        place(nat_g, cx=fd.door.get_center()[0] + 0.9, cy=-2.3)
        natt.move_to(nat)
        out_ar = arrow_(nat.get_right(), nat.get_right() + RIGHT * 2.2, ROUTE)
        out_l = label("out only", CAPTION, ROUTE)
        place(out_l, cx=out_ar.get_center()[0], bottom=out_ar.get_top()[1] + 0.06)
        in_ar = arrow_(fd.browser.frame.get_corner(DOWN + RIGHT) + np.array([0.05, -0.08, 0]),
                       nat.get_corner(UP + LEFT) + np.array([0.15, 0.02, 0]), S.GREY, stroke=4, buff=0.02)
        in_l = label("inbound", CAPTION, S.GREY)
        place(in_l, right=in_ar.get_center()[0] - 0.2, top=in_ar.get_center()[1] - 0.1)
        apart(in_l, pub_g, "inbound label / public chip")
        s0, s1 = in_ar.get_start(), in_ar.get_end()
        y_top = pub_g.get_top()[1]
        x_at = s0[0] + (s1[0] - s0[0]) * (y_top - s0[1]) / (s1[1] - s0[1]) if s1[1] < y_top < s0[1] else s1[0]
        guard(x_at >= pub_g.get_right()[0] + 0.1, "inbound arrow crosses the public chip")
        nat_all = VGroup(nat_g, out_ar, out_l, in_ar, in_l)
        inside(nat_all, "NAT row")
        apart(VGroup(nat_g, out_ar, out_l), pub_g, "NAT row / public chip")
        apart(VGroup(nat_g, out_ar, out_l), fd_at, "NAT row / front door")
        apart(in_l, fd, "inbound label / front door")
        guard(in_ar.get_length() >= 0.8, "inbound arrow too short")
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(rc, sep_g, never_g)), run_time=0.6)
            vo.wait_until("Next public variables")
            self.play(FadeIn(jsf, shift=UP * 0.1), run_time=0.4)
            self.play(jsf.animate.move_to(jsf_to), run_time=0.9)
            self.play(FadeIn(pub_g, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("public by design")
            self.play(flash(pub[0], TURN, 1.12), outline_flash(fd.browser, INK), run_time=0.7)
            vo.wait_until("And NAT does not help")
            self.play(FadeIn(nat_g), run_time=0.5)
            self.play(GrowArrow(out_ar), FadeIn(out_l), run_time=0.6)
            vo.wait_until("it only carries")
            self.play(GrowArrow(in_ar), FadeIn(in_l), run_time=0.7)
            sp2 = spark(0.2).move_to(nat.get_left() + LEFT * 0.08)
            self.play(FadeIn(sp2, scale=0.4), in_ar.animate.set_color(ERR), flash(nat, ERR, 1.06), run_time=0.6)
            self.play(FadeOut(sp2), FadeOut(in_ar, shift=(in_ar.get_start() - in_ar.get_end()) * 0.25),
                      in_l.animate.set_color(ERR), run_time=0.6)

        # ========================================================== 9 · takeaway
        tk = takeaway(TAKEAWAY)
        inside(tk, "takeaway")
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(fd, tag_fd, jsf, pub_g, nat_g, out_ar, out_l, in_l)), FadeOut(lr),
                      run_time=0.6)
            self.play(FadeIn(VGroup(tk.frame, tk.head)), FadeIn(tk.rows[0], shift=RIGHT * 0.15), run_time=0.7)
            vo.wait_until("it is outside the VPC")
            self.play(flash(tk.rows[0][0], TURN, 1.3), run_time=0.6)
            vo.wait_until("Call the public")
            self.play(flash(tk.rows[0], TURN, 1.03), run_time=0.6)
            vo.wait_until("never localhost")
            self.play(Circumscribe(tk.rows[0][1], color=ERR, buff=0.06), run_time=0.9)
            vo.wait_until("NAT does not help inbound")
            self.play(FadeIn(tk.rows[1], shift=RIGHT * 0.15), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(tk), run_time=0.6)
        self.wait(0.3)
