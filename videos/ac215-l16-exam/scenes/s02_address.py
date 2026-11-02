"""S02 · From localhost to a front door (V1: the same container on a different street).
Lecture: L10 4–11; L16 3–4, 8–11, 18–20, 27, 59.

Beats (script.md "## S02", one voiceover block each):
 0  LECTURE 10 · 9. The GREY laptop holds the sealed TEAL api-service container: PURPLE uvicorn
    chip, TEAL FastAPI box with its door :9000, three interface sockets on the container wall.
    Under it CODE(cheese-app-v0/api-service/docker-entrypoint.sh: 6–9), line 7 lit, the excerpt
    `--host 0.0.0.0 --port 9000` underlined YELLOW. 0.0.0.0 draws a YELLOW bracket around every
    socket; then a RED ring closes around only 127.0.0.1, chip "loopback · only this container";
    both dissolve.
 1  The panel becomes CODE(cheese-app-v0/api-service/docker-shell.sh: 19–27) (folded: 19, 20, 27),
    line 20 lit. The container wall flashes (sealed); the GREY door "laptop :9000" and the PINK -p
    tunnel draw to FastAPI's door; the browser appears and a GREY packet "→ localhost:9000" walks
    browser → laptop door → tunnel → FastAPI (GREEN ✓).
 2  The panel becomes PANEL(cheese-app-v0/README.md: 173–175), lines 174–175 lit; localhost:3200
    and localhost:9000 underline as said. A GREY label "localhost = this machine" writes beside
    the laptop with an arrow onto it.
 3  LECTURE 16 · 4, 8. Laptop and panel leave. A street of BLUE houses with numbers (one house
    with doors :8000 and :5432); "IP address = street address → picks the machine", "port = door →
    picks the service"; the private-range table (RFC 1918) with 34.120.45.67 under "public"; a RED
    note "not routed on the internet".
 4  LECTURE 16 · 4, 18. A small GREY laptop with the TEAL FastAPI box (door :9000) dissolves; the
    box lands in the BLUE VPC's private app subnet, its door swaps to :8000, the address 10.0.2.5
    writes; GREY chip "lecture: :8000 · course repo: :9000". An ORANGE packet "→ 10.0.2.5" from
    the internet hits the VPC's edge and evaporates RED ("no route to 10.x").
 5  LECTURE 10 · 11. L10 slide 11's table: address · who can reach it · getting traffic in; the
    laptop column swaps cell by cell to the cloud's.
 6  LECTURE 16 · 27. Slide 27's numbered DNS path (browser, public resolver 1.1.1.1, Route 53, ALB
    api-alb in 10.0.1.0/24), steps 1–5 as said; a GREY packet "→ ALB-IP:443" rides step 5.
 7  LECTURE 16 · 11, 20, 26. Zoom inside the VPC: public subnet with the ALB, private app subnet
    with the gate (security group) and the task 10.0.2.5 :8000. The HTTPS envelope opens at the
    ALB ("TLS ends here") and a new envelope "ALB 10.0.1.x → 10.0.2.5:8000" (both fields YELLOW,
    then settled) reaches the gate; rule "allow · TCP 8000 · source: ALB" writes, the gate flashes
    GREEN, the packet reaches the door (✓). An ORANGE stranger packet sparks RED at the gate and
    evaporates; the reply walks back through the gate with GREEN "stateful: reply allowed".
 8  LECTURE 16 · 20, 59. Two cards: "administrative access · SSH → the machine", "client access ·
    HTTPS → the service". A GREY neighbors strip: EC2 / ALB / NAT Gateway, each GCP name (Compute
    Engine, Cloud Load Balancing, Cloud NAT) slides in under its AWS twin as said.
 9  TAKEAWAY, row by row as spoken; then an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    VectorizedPoint,
    VGroup,
    Write,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S02"]

# ------------------------------------------------------------------ the real sources
ENTRY = "cheese-app-v0/api-service/docker-entrypoint.sh"
SHELL = "cheese-app-v0/api-service/docker-shell.sh"
assert "--host 0.0.0.0 --port 9000" in source_line(ENTRY, 7), source_line(ENTRY, 7)
assert source_line(ENTRY, 6).startswith("uvicorn_server()"), source_line(ENTRY, 6)
assert source_line(SHELL, 19).startswith("docker run"), source_line(SHELL, 19)
assert source_line(SHELL, 20).strip() == "-p 9000:9000 \\", source_line(SHELL, 20)
assert source_line(SHELL, 27).strip() == "$IMAGE_NAME", source_line(SHELL, 27)
_rd = readme_lines("cheese-app-v0", 173, 175)
assert "localhost:3200" in _rd[1] and "localhost:9000" in _rd[2], _rd
assert PORT_REPO == 9000 and PORT_LECTURE == 8000 and TASK_IP == "10.0.2.5"

TAKEAWAY = ("`localhost` → the machine the code runs on · `10.x` → private, unreachable from the internet · "
            "public clients → DNS name → load balancer `:443` → private target `:8000`")

# ------------------------------------------------------------------ layout helpers
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


def apart(a, b, name="", buff=0.04):
    """a and b must not overlap (bounding boxes)."""
    ok = (a.get_right()[0] + buff <= b.get_left()[0] or b.get_right()[0] + buff <= a.get_left()[0]
          or a.get_top()[1] + buff <= b.get_bottom()[1] or b.get_top()[1] + buff <= a.get_bottom()[1])
    guard(ok, f"overlap: {name}")


def flash(mob, color=TURN, k=1.12, run_time=0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def gone(scene, mob):
    """Take `mob` and any Group an AnimationGroup built around its parts off the scene (Packet.drop()
    plays a Succession: its FadeOut does not remove, and its RED AnimationGroup leaves a Group)."""
    fam = set(mob.get_family())
    for m in list(scene.mobjects):
        if m is mob or (fam & set(m.get_family()) and type(m).__name__ == "Group"):
            scene.remove(m)


def task_glyph(port: str, w: float = 1.9) -> VGroup:
    """The TEAL FastAPI task: a box and its door on the left (label below). .box .door .name"""
    bx = box(w, 0.75, CTR, fill_opacity=0.15, stroke=3)
    nm = label("FastAPI", CAPTION, INK).move_to(bx)
    dr = door(port, CTR, h=0.5, label_side=DOWN)
    dr.shift(bx.get_left() + LEFT * 0.38 - dr.frame.get_center())
    g = VGroup(bx, nm, dr)
    g.box, g.door, g.name = bx, dr, nm
    return g


def subnet(w: float, h: float, name: str, cidr: str, lock: bool) -> VGroup:
    """A BLUE subnet box with its name and CIDR at the top. .frame .head"""
    fr = box(w, h, CLOUD, fill_opacity=0.05 if not lock else 0.02, stroke=2.5, radius=0.14)
    hd = VGroup(label(name, CAPTION, CLOUD), mono(cidr, CAPTION, S.GREY)).arrange(DOWN, buff=0.04)
    hd.move_to(fr.get_top() + DOWN * (hd.height / 2 + 0.15))
    g = VGroup(fr, hd)
    if lock:
        g.add(padlock(0.3).next_to(hd[0], RIGHT, buff=0.15))
    g.frame, g.head = fr, hd
    return g


class LaptopToCloud(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0 · uvicorn on 0.0.0.0:9000
        lh = LaptopHost(show=("zone", "ctr", "uvicorn", "api", "sockets"))
        place(lh, left=-6.35, top=3.45)
        inside(lh, "laptop")
        p0 = src_panel(ENTRY, 6, 9, wrap=True, focus=7)
        place(p0, cx=0, top=-0.55)
        inside(p0, "entrypoint panel")
        apart(lh, p0, "laptop / entrypoint panel")
        bar0 = p0.bar(7)
        ul0 = under(p0.span(7, "--host 0.0.0.0 --port 9000"))
        b_all = lh.bind_all()
        b_lo = lh.bind_loopback()
        br_bot = lh.parts["browser"].get_bottom()[1]
        if b_all.text.get_top()[1] > br_bot - 0.08:      # the helper centres it on the sockets: under the browser
            b_all.text.shift(DOWN * (b_all.text.get_top()[1] - br_bot + 0.08))
        inside(b_all, "0.0.0.0 bracket")
        apart(b_all.text, lh.parts["browser"], "0.0.0.0 text / browser")
        apart(b_lo.chip, p0, "loopback chip / panel")
        lr = None
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, 10, "9")
            self.play(FadeIn(lh, shift=RIGHT * 0.2), run_time=0.8)
            vo.wait_until("In the course app")
            self.play(flash(lh.parts["uvicorn"], TOOL, 1.15), run_time=0.6)
            self.play(FadeIn(p0, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(bar0), run_time=0.4)
            vo.wait_until("on host")
            self.play(Create(ul0), run_time=0.6)
            self.play(flash(lh.api_door, TURN, 1.2), run_time=0.6)
            vo.wait_until("That host means")
            self.play(Create(b_all.bracket), run_time=0.5)
            self.play(Write(b_all.text), LaggedStart(*[flash(s, TURN, 1.4) for s in lh.sockets], lag_ratio=0.3),
                      run_time=1.0)
            vo.wait_until("Bound to")
            self.play(b_all.animate.set_opacity(0.3), Create(b_lo.ring), run_time=0.6)
            self.play(FadeIn(b_lo.chip, shift=UP * 0.1), run_time=0.5)
            self.play(flash(lh.loopback_label, ERR, 1.15), run_time=0.6)
        self.play(FadeOut(b_all), FadeOut(b_lo), run_time=0.5)

        # ========================================================== 1 · -p 9000:9000: the tunnel
        p1 = src_panel(SHELL, [19, 20, 27], focus=20)
        place(p1, cx=0, top=-0.55)
        inside(p1, "docker-shell panel")
        apart(lh, p1, "laptop / docker-shell panel")
        bar1 = p1.bar(20)
        pk = Packet("", "localhost:9000", color=LAPTOP)
        trip = pk.travel(lh.request_points(), run_time=2.0, lead="icon")
        ok1 = tick_mark(0.34).next_to(lh.api_door, UP, buff=0.12)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(p0, bar0, ul0), shift=DOWN * 0.2), run_time=0.5)
            self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.6)
            ctr = lh.parts["ctr"].frame
            self.play(ctr.animate.set_stroke(width=7), run_time=0.4)
            self.play(ctr.animate.set_stroke(width=3), run_time=0.4)
            vo.wait_until("Dash p")
            self.play(FadeIn(bar1), *lh.parts_in("host_door"), run_time=0.6)
            self.play(*lh.parts_in("tunnel", anim=Create), run_time=0.8)
            vo.wait_until("is the tunnel")
            self.play(*lh.parts_in("browser"), run_time=0.5)
            self.play(FadeIn(pk), run_time=0.3)
            self.play(trip)
            self.play(FadeIn(ok1, scale=0.6), flash(lh.api_door, OWN, 1.2), run_time=0.6)
        self.play(FadeOut(pk), FadeOut(ok1), run_time=0.4)

        # ========================================================== 2 · the README: localhost = this machine
        p2 = readme_panel("cheese-app-v0", 173, 175, focus=(174, 175))
        place(p2, cx=0, top=-0.55)
        inside(p2, "README panel")
        apart(lh, p2, "laptop / README panel")
        ul_a = under(p2.clause(174, "localhost:3200"))
        ul_b = under(p2.clause(175, "localhost:9000"))
        this = label("localhost = this machine", 26, LAPTOP)
        place(this, left=lh.get_right()[0] + 1.0, cy=lh.get_center()[1] + 0.4)
        inside(this, "localhost label", t=3.05)
        pt = arrow_(this.get_left() + LEFT * 0.1, [lh.get_right()[0] + 0.05, this.get_center()[1], 0], LAPTOP)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p1, bar1), shift=DOWN * 0.2), run_time=0.5)
            self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("localhost 3200")
            self.play(Create(ul_a), run_time=0.5)
            vo.wait_until("it calls the API")
            self.play(Create(ul_b), run_time=0.5)
            self.play(flash(lh.api_door, TURN, 1.2), run_time=0.6)
            vo.wait_until("Localhost always means")
            self.play(Write(this), run_time=0.8)
            self.play(GrowArrow(pt), lh.parts["zone"].frame.animate.set_stroke(INK, 4), run_time=0.6)
            self.play(lh.parts["zone"].frame.animate.set_stroke(LAPTOP, 2.5), run_time=0.5)

        # ========================================================== 3 · IP = street address, port = door
        st = Street()
        place(st, cx=-0.6, top=2.95)
        inside(st, "street", t=3.05)
        l_ip = label("IP address = street address → picks the machine", 24, INK)
        l_port = label("port = door → picks the service", 24, INK)
        VGroup(l_ip, l_port).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        place(VGroup(l_ip, l_port), left=st.get_left()[0], top=st.get_bottom()[1] - 0.3)
        empty = VectorizedPoint()
        tb = table_card(["private (RFC 1918)", "public"],
                        [[f"`{PRIVATE_RANGES[0]}`", f"`{PUBLIC_IP}`"], [f"`{PRIVATE_RANGES[1]}`", empty],
                         [f"`{PRIVATE_RANGES[2]}`", VectorizedPoint()]],
                        header_colors=[S.GREY, SHARED])
        place(tb, left=st.get_left()[0], top=l_port.get_bottom()[1] - 0.3)
        inside(tb, "range table")
        nr = label("not routed on the internet", 24, ERR)
        place(nr, left=tb.get_right()[0] + 0.4, cy=tb.cells[1][0].get_center()[1])
        inside(nr, "not-routed note")
        pr_col = VGroup(*[tb.cells[r][0] for r in range(3)])
        nr_ar = arrow_(nr.get_left() + LEFT * 0.08, [tb.cells[1][0].get_right()[0] + 0.2, nr.get_center()[1], 0], ERR)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(lh, p2, ul_a, ul_b, this, pt)), run_time=0.5)
            lr = lref_swap(self, lr, 16, "4, 8")
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.2) for h in st.houses], lag_ratio=0.15),
                      Create(st.road), run_time=1.0)
            self.play(FadeIn(l_ip, shift=RIGHT * 0.15),
                      LaggedStart(*[flash(h.label, TURN, 1.15) for h in st.houses], lag_ratio=0.12), run_time=1.0)
            vo.wait_until("and a port picks")
            self.play(FadeIn(st.doors, scale=0.7), run_time=0.5)
            self.play(FadeIn(l_port, shift=RIGHT * 0.15), flash(st.doors, TURN, 1.2), run_time=0.7)
            vo.wait_until("Addresses that start")
            self.play(FadeIn(VGroup(tb.frame, tb[1], *tb.heads)), run_time=0.5)
            for r in range(3):
                self.play(FadeIn(tb.cells[r][0], shift=RIGHT * 0.1), run_time=0.35)
            self.play(FadeIn(tb.cells[0][1], shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("The internet does not")
            self.play(Write(nr), GrowArrow(nr_ar), run_time=0.7)
            self.play(flash(pr_col, ERR, 1.08), run_time=0.6)

        # ========================================================== 4 · the same container in the VPC: 10.0.2.5
        vm = VpcMap(show=())
        aws = aws_chip()
        place(aws, left=-6.45, top=3.5)
        inside(aws, "aws chip")
        mini = laptop_zone(3.6, 2.0, "your laptop")
        tg = task_glyph(":9000")
        mini.move_to([-1.5, 0.2, 0])
        tg.move_to(mini.frame.get_center() + UP * 0.25)
        target = np.array([2.0, -0.15, 0])               # the task box's centre in the app subnet
        tg_end = tg.copy()
        tg_end.shift(target - tg_end.box.get_center())
        guard(tg_end.door.frame.get_left()[0] >= vm.boxes["app"].get_left()[0] + 0.25, "task door outside the app subnet")
        ip = mono(TASK_IP, CAPTION, S.GREY).next_to(tg_end.box, DOWN, buff=0.1)
        apart(ip, tg_end.door.label, "IP / door label")
        port_chip = card_rows([("lecture: :8000", S.GREY), ("course repo: :9000", S.GREY)])
        place(port_chip, cx=vm.boxes["app"].get_center()[0], top=ip.get_bottom()[1] - 0.45)
        guard(port_chip.get_left()[0] >= vm.boxes["app"].get_left()[0] + 0.05
              and port_chip.get_right()[0] <= vm.boxes["app"].get_right()[0] - 0.05, "port chip wider than the subnet")
        stranger = Packet("", TASK_IP, color=SHARED)
        edge_x = vm.boxes["vpc"].get_left()[0]
        s0 = np.array([-6.35, -0.75, 0])
        s1 = np.array([edge_x - 0.15, -0.75, 0])
        hop = stranger.travel([s0, s1], run_time=1.4, lead="icon")
        x_edge = x_mark(0.34).move_to([edge_x, -0.75, 0])
        no_route = VGroup(label("no route", 24, ERR), label("to 10.x", 24, ERR)).arrange(DOWN, buff=0.08)
        place(no_route, left=-6.45, top=-1.25)
        guard(no_route.get_right()[0] <= edge_x - 0.1, "no-route note crosses the VPC edge")
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(st, l_ip, l_port, tb, nr, nr_ar)), run_time=0.5)
            lr = lref_swap(self, lr, 16, "4, 18")
            self.play(FadeIn(mini), FadeIn(tg, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("into the cloud")
            self.play(FadeOut(mini), run_time=0.4)
            self.add(vm)
            self.play(*vm.parts_in("internet", "vpc", "app"), FadeIn(aws), run_time=0.7)
            self.play(tg.animate.shift(target - tg.box.get_center()), run_time=1.0)
            self.play(*swap_text(tg.door, tg.door.label, tg_end.door.label.copy().set_color(CTR)), run_time=0.5)
            vo.wait_until("Inside the private network")
            self.play(Write(ip), flash(vm.parts["app"][2], CLOUD, 1.3), run_time=0.8)
            self.play(FadeIn(port_chip, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("A packet from the internet")
            self.play(FadeIn(stranger), run_time=0.3)
            self.play(hop)
            self.play(stranger.drop(), Create(x_edge), run_time=0.8)
            gone(self, stranger)
            vo.wait_until("nobody out there")
            self.play(FadeIn(no_route, shift=UP * 0.1), flash(x_edge, ERR, 1.3), run_time=0.7)
        beat4 = VGroup(vm, tg, ip, port_chip, x_edge, no_route)

        # ========================================================== 5 · L10 slide 11: laptop vs cloud
        rt = ReachTable()
        place(rt, cx=0, cy=0.3)
        inside(rt, "reach table", t=3.05)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(beat4), FadeOut(aws), run_time=0.5)
            lr = lref_swap(self, lr, 10, "11")
            self.play(FadeIn(rt, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("On the laptop")
            self.play(flash(rt.cells[1], LAPTOP, 1.05), run_time=0.7)
            vo.wait_until("In the cloud")
            self.play(*rt.to_cloud(0), run_time=0.7)
            vo.wait_until("a firewall starts closed")
            self.play(*rt.to_cloud(1), run_time=0.7)
            vo.wait_until("a load balancer lets")
            self.play(*rt.to_cloud(2), run_time=0.7)
            self.play(flash(rt.cells[2], CLOUD, 1.05), run_time=0.6)

        # ========================================================== 6 · L16 slide 27: the numbered DNS path
        dp = DnsPath(show=())
        place(dp, cx=0, cy=0.0)
        inside(dp, "dns path", t=3.05)
        apart(aws, dp, "aws chip / dns path")
        pk6 = Packet("", "ALB-IP:443", color=BROWSER)
        a5 = dp.arrows[4]
        end6 = dp.node("alb").get_left() + LEFT * (pk6.width / 2 + 0.12) + UP * 0.45
        start6 = a5.get_start() + RIGHT * (pk6.width / 2) + UP * 0.45
        ride = pk6.travel([start6, end6], run_time=1.4)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(rt), run_time=0.5)
            lr = lref_swap(self, lr, 16, "27")
            self.add(dp)
            self.play(*dp.parts_in("nodes"), FadeIn(aws), run_time=0.7)
            self.play(*dp.step(1), run_time=0.6)
            vo.wait_until("the resolver asks")
            self.play(*dp.step(2), run_time=0.6)
            vo.wait_until("public address comes back")
            self.play(*dp.step(3), run_time=0.6)
            self.play(*dp.step(4), run_time=0.6)
            vo.wait_until("Then the browser connects")
            self.play(*dp.step(5), run_time=0.6)
            self.play(FadeIn(pk6), run_time=0.3)
            self.play(ride)
            self.play(flash(dp.node("alb"), CLOUD, 1.1), run_time=0.5)

        # ========================================================== 7 · inside the VPC: ALB -> gate -> task
        pub = subnet(4.0, 5.7, "public subnet", PUB_CIDR, False)
        app = subnet(8.75, 5.7, "private app subnet", APP_CIDR, True)
        place(pub, left=-6.45, top=2.4)
        place(app, right=6.45, top=2.4)
        alb = box(2.2, 0.85, CLOUD, fill_opacity=0.15, stroke=3).move_to([pub.get_center()[0], -0.5, 0])
        albt = VGroup(label("ALB", CAPTION, INK), mono(ALB_NAME, CAPTION, CLOUD)).arrange(DOWN, buff=0.03).move_to(alb)
        task = task_glyph(":8000")
        task.shift(np.array([5.15, -0.5, 0]) - task.box.get_center())
        ip7 = mono(TASK_IP, CAPTION, S.GREY).next_to(task.box, DOWN, buff=0.1)
        gate = Gate()
        gx = 0.9
        gate.bar.stretch_to_fit_height(3.05).move_to([gx, -0.66, 0])
        place(gate.rule, cx=1.75, top=gate.bar.get_bottom()[1] - 0.1)
        guard(gate.rule.get_left()[0] >= app.frame.get_left()[0] + 0.1, "rule chip crosses the subnet edge")
        guard(gate.rule.get_bottom()[1] >= app.frame.get_bottom()[1] + 0.08, "rule chip below the subnet")
        tls = grey_chip("TLS ends here")
        place(tls, cx=alb.get_center()[0], top=alb.get_bottom()[1] - 0.2)
        lane = 0.4
        https = Packet("", "ALB-IP:443", color=BROWSER)
        h_in = https.travel([[-7.5, lane, 0], [alb.get_center()[0], lane, 0]], run_time=1.0)
        req = Packet("ALB 10.0.1.x", f"{TASK_IP}:8000", color=TURN)
        rw = req.width
        req.move_to([pub.frame.get_left()[0] + 0.1 + rw / 2, lane, 0])
        to_gate = req.travel([req.get_center(), [gx - 0.12 - rw / 2, lane, 0]], run_time=1.0)
        to_door = req.travel([[gx - 0.12 - rw / 2, lane, 0], [task.door.frame.get_left()[0] - 0.1 - rw / 2, lane, 0]],
                             run_time=1.0)
        apart(req.copy().move_to([gx - 0.12 - rw / 2, lane, 0]), alb, "request packet / ALB")
        ok7 = tick_mark(0.34).next_to(task.door.frame, UP, buff=0.15)
        sy = -1.98
        strg = Packet("stranger", f"{TASK_IP}:8000", color=SHARED)
        sw = strg.width
        s_hop = strg.travel([[pub.frame.get_left()[0] + 0.1 + sw / 2, sy, 0], [gx - 0.12 - sw / 2, sy, 0]], run_time=1.1)
        apart(strg.copy().move_to([gx - 0.12 - sw / 2, sy, 0]), tls, "stranger / TLS chip")
        apart(strg.copy().move_to([gx - 0.12 - sw / 2, sy, 0]), alb, "stranger / ALB")
        rep = Packet(f"{TASK_IP}:8000", "ALB 10.0.1.x", color=TURN)
        rpw = rep.width
        r_start = [min(task.door.frame.get_left()[0] - 0.1 - rpw / 2, 6.5 - rpw / 2), lane, 0]
        r_end = [alb.get_center()[0] + 0.2, lane, 0]
        back = rep.travel([r_start, r_end], run_time=1.6)
        state = fix_chip("stateful: reply allowed")
        place(state, cx=gx + 0.6, bottom=lane + 0.45)
        guard(state.get_top()[1] <= app.head.get_bottom()[1] - 0.05, "stateful chip under the subnet header")
        guard(state.get_left()[0] >= app.frame.get_left()[0] + 0.05, "stateful chip crosses the subnet edge")
        zoom = VGroup(pub, app, alb, albt, task, ip7, gate.bar)
        inside(zoom, "VPC zoom", t=3.05)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(dp, pk6)), run_time=0.5)
            lr = lref_swap(self, lr, 16, "11, 20, 26")
            self.play(FadeIn(VGroup(pub, app)), run_time=0.5)
            self.play(FadeIn(VGroup(alb, albt)), FadeIn(task), FadeIn(ip7), Create(gate.bar), run_time=0.6)
            self.play(FadeIn(https), run_time=0.2)
            self.play(h_in)
            self.play(FadeOut(https, scale=1.4), FadeIn(tls, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("sends its own request")
            for f in (req.src, req.dst):
                f.set_color(TURN)
            self.play(FadeIn(req, shift=RIGHT * 0.2), run_time=0.4)
            self.play(to_gate)
            self.play(*req.settle(), run_time=0.3)
            vo.wait_until("a security group allows")
            self.play(FadeIn(gate.rule, shift=UP * 0.1), run_time=0.5)
            self.play(*gate.flash(True), run_time=0.6)
            self.play(to_door)
            self.play(FadeIn(ok7, scale=0.6), run_time=0.4)
            self.play(FadeOut(req), run_time=0.3)
            vo.wait_until("packet bounces")
            self.play(FadeIn(strg), run_time=0.2)
            self.play(s_hop)
            sp = strg.spark_at()
            self.play(FadeIn(sp, scale=0.5), *gate.flash(False), run_time=0.5)
            self.play(FadeOut(sp), strg.drop(), run_time=0.8)
            gone(self, strg)
            vo.wait_until("and the reply goes back")
            self.play(FadeOut(ok7), FadeIn(rep), run_time=0.3)
            self.play(back)
            vo.wait_until("because the firewall remembers")
            self.play(FadeIn(state, shift=UP * 0.1), *gate.flash(True), run_time=0.6)
        beat7 = VGroup(pub, app, alb, albt, task, ip7, gate, tls, rep, state, aws)

        # ========================================================== 8 · SSH vs HTTPS; the GCP neighbors
        c_ssh = card_rows([("administrative access", S.GREY), "`SSH` → the machine"], width=4.6)
        c_web = card_rows([("client access", S.GREY), "`HTTPS` → the service"], width=4.6)
        VGroup(c_ssh, c_web).arrange(RIGHT, buff=0.8)
        place(VGroup(c_ssh, c_web), cx=0, top=2.75)
        cols_x = (-2.6, 1.0, 4.6)
        aws_names = ("EC2", "ALB", "NAT Gateway")
        gcp_names = ("Compute Engine", "Cloud Load Balancing", "Cloud NAT")
        notes = ("slide 59", "", "not on the slides")
        y_aws, y_gcp, y_note = -0.75, -1.55, -2.2
        strip = box(12.6, 2.45, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
        strip.move_to([0, (y_aws + y_note) / 2, 0])
        rl_aws = label("the lecture (AWS)", CAPTION, S.GREY)
        rl_gcp = label("Google Cloud", CAPTION, S.GREY)
        place(rl_aws, left=strip.get_left()[0] + 0.3, cy=y_aws)
        place(rl_gcp, left=strip.get_left()[0] + 0.3, cy=y_gcp)
        a_row = VGroup(*[label(n, 24, CLOUD).move_to([x, y_aws, 0]) for n, x in zip(aws_names, cols_x)])
        g_row = VGroup(*[label(n, 24, INK).move_to([x, y_gcp, 0]) for n, x in zip(gcp_names, cols_x)])
        n_row = VGroup(*[label(n or "·", CAPTION, S.GREY).move_to([x, y_note, 0]) for n, x in zip(notes, cols_x)])
        links = VGroup(*[Line([x, y_aws - 0.2, 0], [x, y_gcp + 0.22, 0], color=S.GREY, stroke_width=2)
                         for x in cols_x])
        for i in range(3):
            guard(g_row[i].width <= 3.4, "GCP name too wide for its column")
        apart(rl_gcp, g_row[0], "row label / Compute Engine")
        inside(VGroup(strip, c_ssh, c_web), "neighbors", t=3.05)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(beat7), run_time=0.5)
            lr = lref_swap(self, lr, 16, "20, 59")
            self.play(FadeIn(c_ssh, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("while clients reach")
            self.play(FadeIn(c_web, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("The lecture draws")
            self.play(FadeIn(strip), FadeIn(rl_aws), LaggedStart(*[FadeIn(a) for a in a_row], lag_ratio=0.2),
                      run_time=0.8)
            vo.wait_until("On Google Cloud")
            self.play(FadeIn(rl_gcp), run_time=0.3)
            for i, phrase in enumerate((None, "Cloud Load Balancing", "and Cloud NAT")):
                if phrase:
                    vo.wait_until(phrase)
                self.play(Create(links[i]), FadeIn(g_row[i], shift=UP * 0.3),
                          *([FadeIn(n_row[i])] if notes[i] else []), run_time=0.5)

        # ========================================================== 9 · takeaway
        tk = takeaway(TAKEAWAY)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(c_ssh, c_web, strip, rl_aws, rl_gcp, a_row, g_row, links,
                                     *[n_row[i] for i in (0, 2)])), FadeOut(lr), run_time=0.5)
            self.play(FadeIn(VGroup(tk.frame, tk.head)), FadeIn(tk.rows[0], shift=RIGHT * 0.15), run_time=0.7)
            vo.wait_until("A 10 dot")
            self.play(FadeIn(tk.rows[1], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("Public clients")
            self.play(FadeIn(tk.rows[2], shift=RIGHT * 0.15), run_time=0.5)
            self.play(flash(tk.rows[2], TURN, 1.03), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(tk), run_time=0.6)
        self.wait(0.3)
