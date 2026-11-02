"""S03 · Private subnets, route tables and NAT (V2: the route lookup and the NAT notebook).
Lecture: L16 5–7, 9, 12–16, 28.

Beats (script.md "## S03", one voiceover block each):
 0  LECTURE 16 · 5, 15–16. A BLUE VPC box 10.0.0.0/16 with a small gate on its edge; the CIDR
    ruler writes in below (32 bit cells, 16 BLUE "fixed", 16 white "vary"), counter 2¹⁶ = 65,536;
    the bar shifts to 24 fixed cells, counter 2⁸ = 256.
 1  The ruler fades; the box grows into the VPC of the lecture's picture and splits into three
    subnets as said: public 10.0.1.0/24 (ALB, NAT Gateway), private app 10.0.2.0/24 (padlock,
    TEAL FastAPI tasks), private data 10.0.3.0/24 (padlock, PostgreSQL 10.0.3.7); the Internet
    Gateway on the edge and the ORANGE internet. GREY chip "the lecture's picture · the cheese app
    repos contain no network config".
 2  LECTURE 16 · 13. The map dims; two route tables side by side (PINK rows): the first rows pulse
    together ("same"), the default rows' gateways flash YELLOW ("the only difference").
 3  Slide 13's caption as a GREY strip under the tables; then the private table shrinks onto the
    first FastAPI task as its route card and the map comes back.
 4  A YELLOW packet 10.0.2.5:52134 → 10.0.3.7:5432; both route rows light, the /16 row gets a
    thick YELLOW bar "longer prefix wins"; the packet runs on the PINK local path to the database
    (GREEN ✓).
 5  LECTURE 16 · 14. A packet 10.0.2.5:52134 → 34.x:443: only the 0.0.0.0/0 row lights; the
    packet goes to the NAT Gateway; the PINK NAT notebook opens beside it with one line; the
    source flashes YELLOW and becomes NAT-IP:61001; the packet leaves through the Internet Gateway.
 6  The reply 34.x:443 → NAT-IP:61001 returns; the notebook line glows; the destination becomes
    10.0.2.5:52134; the reply reaches the task (✓). An ORANGE packet → NAT-IP:62000 finds no
    line: RED, dropped ("no line → dropped"). The padlocks flash: the private subnets stay private.
 7  The NAT Gateway turns RED ("down"). A new LLM packet and an ORANGE → package mirror:443 packet
    follow the default row and stall RED at the dead hop; a database packet still runs on the
    local route (✓) and an ALB → task request still arrives (✓).
 8  The canvas clears. PONDER P1 (McqCard, `illustration`): the stem is read; 10 s timer after.
 9  Reveal: C fills YELLOW ✓ with the GREEN note; the RED reason under A.
10  RED reasons under B and D; the card fades.
11  TAKEAWAY, row by row as spoken; then an empty frame.
"""

import numpy as np
from manim import (
    AnimationGroup,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    VGroup,
    Write,
    linear,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S03"]

assert VPC_CIDR == "10.0.0.0/16" and PUB_CIDR == "10.0.1.0/24" and APP_CIDR == "10.0.2.0/24"
assert DATA_CIDR == "10.0.3.0/24" and TASK_IP == "10.0.2.5" and DB_IP == "10.0.3.7"
assert EPHEMERAL == "52134" and NAT_PORT == "61001" and LLM_DST == "34.x:443"

STEM = ("A worker in a **private** subnet must download model weights from a public website at startup. "
        "Nobody on the internet may open a connection to it. Where should its route for `0.0.0.0/0` point?")
OPTIONS = ["the Internet Gateway, and give the worker a public IP", "the local route",
           "a NAT Gateway in a public subnet", "the load balancer"]
TAKEAWAY = ("private subnet → `0.0.0.0/0` goes to NAT · "
            "NAT carries only connections that start inside, replies come back, nothing uninvited gets in · "
            "NAT down → internet calls fail, VPC-internal traffic (DB) still works")

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


def flash(mob, color=TURN, k=1.12, run_time=0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def at(p, x, y):
    """A copy of packet p moved so its centre is at (x, y): for layout checks."""
    return p.copy().move_to([x, y, 0])


def unwrap(scene, anim):
    """Remove the wrapper groups an AnimationGroup (and the ones nested in it, as in Packet.drop's
    Succession) leaves on the scene, so a dropped packet does not come back."""
    if isinstance(anim, AnimationGroup):
        if anim.group in scene.mobjects:
            scene.remove(anim.group)
        for a in anim.animations:
            unwrap(scene, a)


def gate_glyph(h: float = 0.9) -> VGroup:
    """A small community gate: two BLUE posts and a GREY bar between them (vertical, on an edge)."""
    p1 = Rectangle(width=0.14, height=0.14, stroke_color=CLOUD, stroke_width=2).set_fill(CLOUD, 0.8)
    p2 = p1.copy().shift(DOWN * h)
    bar_ = Line(p1.get_bottom(), p2.get_top(), color=S.GREY, stroke_width=5)
    return VGroup(bar_, p1, p2)


class RouteAndNat(VoiceScene):
    def construct(self):
        assert len(SAY) == 12, len(SAY)
        # the database packet's lane (under task 2) and the NAT lanes (above / right of NAT)
        y_db, y_nat, y_task = -2.62, -0.70, -1.10

        # ========================================================== 0 · one block of addresses: CIDR
        mini = box(6.4, 1.9, CLOUD, fill_opacity=0.03, stroke=3, radius=0.2).move_to([0.4, 1.55, 0])
        mt = VGroup(label("VPC", CAPTION + 2, CLOUD), mono(VPC_CIDR, 26, CLOUD)).arrange(RIGHT, buff=0.25)
        mt.move_to(mini)
        gate = gate_glyph(0.9).move_to(mini.get_left())
        cr = CidrRuler(16)
        place(cr, cx=0, top=-0.15)
        inside(cr, "CIDR ruler")
        apart(cr, mini, "ruler / VPC box")
        a_llm = fix_chip("language model API · timeout", ERR)
        a_db = fix_chip("database · answers", OWN)
        alarm = VGroup(bell(0.45), a_llm, a_db).arrange(RIGHT, buff=0.35)
        place(alarm, cx=0, cy=-1.6)
        inside(alarm, "alarm")
        apart(alarm, mini, "alarm / VPC box")
        slash = mt[1][-3:]                       # "/16"
        ul16 = under(slash)
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, None, 16, "5, 15–16")
            self.play(Create(mini), FadeIn(gate), run_time=0.8)
            self.play(Write(mt), FadeIn(alarm[0], scale=0.7), run_time=0.8)
            self.play(FadeIn(a_llm, shift=UP * 0.1), Indicate(alarm[0], color=ERR), run_time=0.6)
            self.play(FadeIn(a_db, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("A VPC is one block")
            self.play(FadeOut(alarm, shift=DOWN * 0.15), flash(mt[1], CLOUD, 1.1), run_time=0.7)
            self.play(mini.animate.set_stroke(width=7), run_time=0.5)
            self.play(mini.animate.set_stroke(width=3), run_time=0.5)
            vo.wait_until("The slash counts")
            self.play(Create(ul16), slash.animate.set_color(TURN), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cr.cells], lag_ratio=0.04),
                      run_time=1.4)
            vo.wait_until("Slash 16 leaves")
            self.play(FadeIn(cr.fixed), flash(VGroup(*cr.cells[:16]), CLOUD, 1.05), run_time=0.6)
            self.play(FadeIn(cr.vary), flash(VGroup(*cr.cells[16:]), INK, 1.05), run_time=0.6)
            self.play(Write(cr.counter), run_time=0.6)
            vo.wait_until("Slash 24 leaves")
            self.play(*cr.set_prefix(24), run_time=0.9)
            self.play(flash(cr.counter, TURN, 1.12), run_time=0.6)

        # ========================================================== 1 · three subnets
        vm = VpcMap(show=())
        vbox = vm.boxes["vpc"]
        vt = vm.parts["vpc"][1]
        chip = grey_chip("the lecture's picture · the cheese app repos contain no network config")
        place(chip, left=-6.45, top=3.55)
        inside(chip, "picture chip")
        apart(chip, lr, "picture chip / lecture tag")
        apart(chip, vm.boxes["vpc"], "picture chip / VPC")
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(cr), FadeOut(ul16), run_time=0.5)
            self.add(vm)
            self.play(mini.animate.stretch_to_fit_width(vbox.width).stretch_to_fit_height(vbox.height)
                      .move_to(vbox), mt.animate.move_to(vt), gate.animate.move_to(vm.boxes["igw"]).set_opacity(0),
                      run_time=1.0)
            self.play(FadeOut(VGroup(mini, mt, gate)), *vm.parts_in("vpc", "internet", "igw"), FadeIn(chip),
                      run_time=0.5)
            vo.wait_until("A public one")
            self.play(*vm.parts_in("public"), run_time=0.5)
            self.play(*vm.parts_in("alb", "nat"), run_time=0.5)
            vo.wait_until("A private app subnet")
            self.play(*vm.parts_in("app"), run_time=0.5)
            self.play(*vm.parts_in("tasks"), flash(vm.parts["app"][2], CLOUD, 1.4), run_time=0.6)
            vo.wait_until("A private data subnet")
            self.play(*vm.parts_in("data"), run_time=0.5)
            self.play(*vm.parts_in("db"), flash(vm.parts["data"][2], CLOUD, 1.4), run_time=0.6)

        # ========================================================== 2 · two route tables
        t_pub = RouteTable(((VPC_CIDR, "local route"), ("0.0.0.0/0", "Internet Gateway")),
                           title="public subnet route table")
        t_prv = RouteTable(((VPC_CIDR, "local route"), ("0.0.0.0/0", "NAT Gateway")),
                           title="private subnet route table")
        tables = VGroup(t_pub, t_prv).arrange(RIGHT, buff=1.1, aligned_edge=DOWN)
        place(tables, cx=0, top=2.55)
        inside(tables, "route tables", t=3.05)
        same = label("same", CAPTION, S.GREY)
        same.move_to([(t_pub.get_right()[0] + t_prv.get_left()[0]) / 2, t_pub.rows[0].get_center()[1], 0])
        guard(same.width <= 1.0, "'same' wider than the gap")
        diff = label("the only difference", 24, TURN)
        place(diff, cx=0, top=tables.get_bottom()[1] - 0.3)
        with self.voiceover(SAY[2]) as vo:
            lr = lref_swap(self, lr, 16, "13")
            self.play(vm.dim_to(0.18), run_time=0.5)
            self.play(FadeIn(t_pub, shift=UP * 0.15), FadeIn(t_prv, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("Both send")
            self.play(*t_pub.light(0, ROUTE), *t_prv.light(0, ROUTE), FadeIn(same), run_time=0.5)
            self.play(flash(t_pub.rows[0], ROUTE, 1.05), flash(t_prv.rows[0], ROUTE, 1.05), run_time=0.7)
            self.play(*t_pub.unlight(0), *t_prv.unlight(0), run_time=0.4)
            vo.wait_until("The only difference")
            self.play(*t_pub.light(1), *t_prv.light(1), run_time=0.5)
            self.play(Write(diff), run_time=0.6)
            vo.wait_until("A public subnet sends")
            self.play(t_pub.gw[1].animate.set_color(TURN), *t_pub.flash_gateway(1), run_time=0.7)
            vo.wait_until("a private subnet to")
            self.play(t_prv.gw[1].animate.set_color(TURN), *t_prv.flash_gateway(1), run_time=0.7)

        # ========================================================== 3 · necessary, not sufficient; the route card
        strip = concept_box("route = necessary, not sufficient · public IP + firewall rules also decide")
        place(strip, cx=0, top=diff.get_bottom()[1] - 0.35)
        inside(strip, "slide 13 strip")
        rc = RouteTable(compact=True)
        rc.move_to(vm.route_spot())
        inside(rc, "route card")
        apart(rc, vm.boxes["task"], "route card / task")
        apart(rc, vm.parts["app"][1], "route card / app subnet header")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(diff), FadeIn(strip, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the machine also needs")
            self.play(flash(strip, INK, 1.04), run_time=0.7)
            self.play(t_pub.gw[1].animate.set_color(INK), t_prv.gw[1].animate.set_color(INK),
                      *t_pub.unlight(1), *t_prv.unlight(1), run_time=0.4)
            self.play(FadeOut(VGroup(t_pub, strip, same)), vm.undim(), run_time=0.6)
            self.play(ReplacementTransform(t_prv, rc), run_time=1.0)
            self.play(flash(vm.boxes["task"], CTR, 1.08), run_time=0.5)

        # ========================================================== 4 · the database: longest prefix wins
        pk_db = Packet(f"{TASK_IP}:{EPHEMERAL}", f"{DB_IP}:5432")
        app_l = vm.boxes["app"].get_left()[0]
        db_x0 = app_l + 0.1 + pk_db.width / 2
        db_x1 = vm.boxes["data"].get_right()[0] - 0.08 - pk_db.width / 2
        guard(db_x1 - db_x0 >= 0.6, "database packet has no room to move")
        to_db = pk_db.travel([[db_x0, y_db, 0], [db_x1, y_db, 0]], run_time=1.2)
        for x in (db_x0, db_x1):
            apart(at(pk_db, x, y_db), vm.boxes["task2"], "db packet / task 2")
            apart(at(pk_db, x, y_db), vm.parts["db"], "db packet / PostgreSQL")
        bar0 = rc.bar(0, thick=True)
        wins = VGroup(label("longer", CAPTION, TURN), label("prefix wins", CAPTION, TURN)).arrange(DOWN, buff=0.04)
        place(wins, cx=vm.boxes["data"].get_center()[0], cy=rc.rows[0].get_center()[1] + 0.05)
        apart(wins, vm.parts["data"][1], "prefix label / data header")
        apart(wins, vm.parts["db"], "prefix label / PostgreSQL")
        guard(wins.get_left()[0] >= vm.boxes["data"].get_left()[0] + 0.05
              and wins.get_right()[0] <= vm.boxes["data"].get_right()[0] - 0.05, "prefix label wider than the subnet")
        wins_ar = arrow_(wins.get_left() + LEFT * 0.05, rc.frame.get_right() + RIGHT * 0.05 + UP * 0.2, TURN, stroke=3)
        local = arrow_(vm.boxes["task"].get_right(), vm.boxes["db"].get_left(), ROUTE)
        ok_db = tick_mark(0.34).next_to(vm.boxes["db"], UP, buff=0.12)
        apart(ok_db, vm.parts["data"][1], "db tick / data header")
        with self.voiceover(SAY[4]) as vo:
            for f in (pk_db.src, pk_db.dst):
                f.set_color(TURN)
            self.play(FadeIn(pk_db, shift=RIGHT * 0.2), flash(vm.boxes["task2"], CTR, 1.0), run_time=0.5)
            self.play(*pk_db.settle(), flash(pk_db.dst, TURN, 1.15), run_time=0.6)
            vo.wait_until("matches both rows")
            self.play(*rc.light(0), *rc.light(1), run_time=0.6)
            vo.wait_until("and the most specific")
            self.play(FadeIn(bar0), *rc.unlight(1), run_time=0.5)
            self.play(FadeIn(wins, shift=LEFT * 0.1), GrowArrow(wins_ar), run_time=0.6)
            vo.wait_until("The packet stays inside")
            self.play(GrowArrow(local), to_db, run_time=1.2)
            self.play(FadeIn(ok_db, scale=0.6), flash(vm.boxes["db"], OWN, 1.1), run_time=0.6)
        self.play(FadeOut(VGroup(pk_db, ok_db, wins, wins_ar, bar0)), *rc.unlight(0), run_time=0.5)

        # ========================================================== 5 · the LLM API: default row → NAT
        nat_c = vm.anchor("nat")
        pk = Packet(f"{TASK_IP}:{EPHEMERAL}", LLM_DST)
        task_x = vm.anchor("task")[0]
        p_task = [task_x, y_task, 0]
        p_nat = [nat_c[0], y_nat, 0]
        to_nat = pk.travel([p_task, p_nat], run_time=1.3)
        apart(at(pk, *p_task[:2]), vm.parts["tasks"][2], "LLM packet / task IP")
        apart(at(pk, *p_task[:2]), vm.boxes["task2"], "LLM packet / task 2")
        apart(at(pk, *p_nat[:2]), vm.boxes["alb"], "LLM packet / ALB")
        apart(at(pk, *p_nat[:2]), vm.boxes["nat"], "LLM packet / NAT")
        p_out = [-4.0, 0.5, 0]
        nb = NatNotebook(slots=1, width=5.6)
        place(nb, right=vm.boxes["task2"].get_left()[0] - 0.1, bottom=-3.5)
        apart(nb, vm.boxes["nat"], "notebook / NAT")
        apart(nb, vm.boxes["task2"], "notebook / task 2")
        inside(nb, "NAT notebook")
        with self.voiceover(SAY[5]) as vo:
            lr = lref_swap(self, lr, 16, "14")
            self.play(FadeIn(pk, shift=DOWN * 0.15), flash(vm.boxes["task"], CTR, 1.05), run_time=0.5)
            self.play(flash(pk.dst, SHARED, 1.15), run_time=0.5)
            vo.wait_until("matches only the default row")
            self.play(*rc.light(1), run_time=0.5)
            self.play(*rc.flash_gateway(1), run_time=0.6)
            vo.wait_until("so it goes to")
            self.play(to_nat)
            self.play(flash(vm.boxes["nat"], CLOUD, 1.1), run_time=0.5)
            vo.wait_until("NAT rewrites")
            self.play(*pk.set_src(f"NAT-IP:{NAT_PORT}"), run_time=0.7)
            vo.wait_until("writes the mapping")
            self.play(FadeIn(nb, shift=UP * 0.15), run_time=0.5)
            self.play(*nb.add_line(f"{TASK_IP}:{EPHEMERAL}", f"NAT-IP:{NAT_PORT}"), run_time=0.6)
            vo.wait_until("and sends it out")
            self.play(*pk.settle(), run_time=0.3)
            self.play(pk.travel([p_nat, [-3.2, y_nat, 0], p_out], run_time=1.2))
            self.play(FadeOut(pk, shift=LEFT * 0.6), flash(vm.boxes["igw"], CLOUD, 1.1), run_time=0.5)

        # ========================================================== 6 · the reply comes back; the stranger is dropped
        rp = Packet(LLM_DST, f"NAT-IP:{NAT_PORT}", slot=len(f"{TASK_IP}:{EPHEMERAL}"))
        back_in = rp.travel([p_out, [-3.2, y_nat, 0], p_nat], run_time=1.2)
        apart(at(rp, *p_task[:2]), vm.parts["tasks"][2], "reply / task IP")
        ok_task = tick_mark(0.34).next_to(vm.boxes["task"], RIGHT, buff=0.15)
        apart(ok_task, rc, "task tick / route card")
        st = Packet("", f"NAT-IP:{int(NAT_PORT) + 999}", color=SHARED)
        st_in = st.travel([[-5.2, 0.5, 0], [-3.2, y_nat, 0], p_nat], run_time=1.2)
        miss = VGroup(mono("no line", CAPTION, ERR), mono("→ dropped", CAPTION, ERR)).arrange(DOWN, buff=0.06)
        miss.move_to([nat_c[0], y_nat, 0])
        apart(miss, vm.boxes["alb"], "miss note / ALB")
        apart(miss, vm.boxes["nat"], "miss note / NAT")
        guard(miss.get_left()[0] >= vm.boxes["public"].get_left()[0] + 0.05
              and miss.get_right()[0] <= vm.boxes["public"].get_right()[0] - 0.05, "miss note wider than the subnet")
        locks = VGroup(vm.parts["app"][2], vm.parts["data"][2])
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(rp), run_time=0.3)
            self.play(back_in)
            vo.wait_until("NAT finds the line")
            self.play(*nb.glow(0), run_time=0.7)
            self.play(*rp.set_dst(f"{TASK_IP}:{EPHEMERAL}"), run_time=0.7)
            vo.wait_until("and hands it")
            self.play(*rp.settle(), run_time=0.3)
            self.play(rp.travel([p_nat, p_task], run_time=1.2))
            self.play(FadeIn(ok_task, scale=0.6), run_time=0.4)
            self.play(FadeOut(rp), FadeOut(ok_task), run_time=0.4)
            vo.wait_until("A packet nobody asked")
            self.play(FadeIn(st), run_time=0.3)
            self.play(st_in)
            sp = spark(0.18).next_to(st.frame, DOWN, buff=0.04)
            self.play(FadeIn(sp, scale=0.5), Indicate(nb.frame, color=ERR, scale_factor=1.02), run_time=0.5)
            gone = st.drop()
            self.play(FadeOut(sp), gone, run_time=0.8)
            unwrap(self, gone)
            self.play(FadeIn(miss, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("NAT only carries")
            self.play(flash(nb.lines[0], TURN, 1.06), run_time=0.7)
            vo.wait_until("Nothing uninvited")
            self.play(LaggedStart(*[flash(m, CLOUD, 1.5) for m in locks], lag_ratio=0.3), run_time=0.9)

        # ========================================================== 7 · NAT fails: egress breaks, the VPC still works
        pk2 = Packet(f"{TASK_IP}:{EPHEMERAL}", LLM_DST)
        stall1 = pk2.travel([p_task, p_nat], run_time=1.2)
        mir = Packet("", "package mirror:443", color=SHARED)
        y_mir = -1.29
        m_x1 = vm.boxes["nat"].get_right()[0] + 0.12 + mir.width / 2
        m_x0 = vm.anchor("task2")[0] + 0.4
        stall2 = mir.travel([[m_x0, vm.anchor("task2")[1], 0], [m_x0, y_mir, 0], [m_x1, y_mir, 0]], run_time=1.2)
        apart(at(mir, m_x1, y_mir), vm.boxes["task2"], "mirror packet / task 2")
        apart(at(mir, m_x1, y_mir), vm.parts["tasks"][2], "mirror packet / task IP")
        apart(at(mir, m_x1, y_mir), at(pk2, *p_nat[:2]), "mirror packet / stalled LLM packet")
        apart(at(pk2, *p_nat[:2]), vm.parts["down"], "stalled packet / down chip")
        sp1 = spark(0.18).move_to([nat_c[0], vm.boxes["nat"].get_top()[1] + 0.02, 0])
        sp2 = spark(0.18).move_to([vm.boxes["nat"].get_right()[0] + 0.06, y_mir, 0])
        pk_db2 = Packet(f"{TASK_IP}:{EPHEMERAL}", f"{DB_IP}:5432")
        db2 = pk_db2.travel([[db_x0, y_db, 0], [db_x1, y_db, 0]], run_time=1.2)
        apart(at(pk_db2, db_x0, y_db), at(mir, m_x1, y_mir), "db packet / mirror packet")
        ok_db2 = tick_mark(0.34).next_to(vm.boxes["db"], UP, buff=0.12)
        ab = Packet("", f"{TASK_IP}:8000")
        y_ab = vm.anchor("task")[1]
        ab_x1 = vm.boxes["task"].get_left()[0] - 0.1 - ab.width / 2
        ab_x0 = ab_x1 - 0.9
        ab_go = ab.travel([[ab_x0, y_ab, 0], [ab_x1, y_ab, 0]], run_time=1.0)
        for x in (ab_x0, ab_x1):
            apart(at(ab, x, y_ab), vm.boxes["alb"], "ALB request / ALB")
            apart(at(ab, x, y_ab), at(pk2, *p_nat[:2]), "ALB request / stalled LLM packet")
            apart(at(ab, x, y_ab), rc, "ALB request / route card")
        ok_ab = tick_mark(0.34).next_to(vm.boxes["task"], RIGHT, buff=0.15)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(nb, miss)), *rc.unlight(1), run_time=0.5)
            self.play(*vm.nat_down(), run_time=0.7)
            vo.wait_until("Every call to the internet")
            self.play(FadeIn(pk2), *rc.light(1), run_time=0.4)
            self.play(stall1)
            self.play(FadeIn(sp1, scale=0.5), *pk2.recolor(ERR), pk2.dst.animate.set_color(ERR), run_time=0.5)
            self.play(FadeIn(mir), run_time=0.3)
            self.play(stall2)
            self.play(FadeIn(sp2, scale=0.5), *mir.recolor(ERR), mir.dst.animate.set_color(ERR), run_time=0.5)
            vo.wait_until("But the database packet")
            self.play(*rc.unlight(1), *rc.light(0, OWN), FadeIn(pk_db2), run_time=0.4)
            self.play(db2, flash(local, OWN, 1.03, run_time=1.2))
            self.play(FadeIn(ok_db2, scale=0.6), run_time=0.4)
            vo.wait_until("and the load balancer still")
            self.play(FadeIn(ab, shift=RIGHT * 0.2), flash(vm.boxes["alb"], CLOUD, 1.08), run_time=0.5)
            self.play(ab_go)
            self.play(FadeIn(ok_ab, scale=0.6), run_time=0.4)
            vo.wait_until("That is the first alarm")
            self.play(flash(VGroup(pk2, mir), ERR, 1.05), flash(vm.parts["down"], ERR, 1.2), run_time=0.8)

        # ========================================================== 8 · PONDER P1
        card = McqCard(STEM, OPTIONS, answer="C", seconds=10)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(vm, rc, local, pk2, mir, sp1, sp2, pk_db2, ok_db2, ab, ok_ab, chip)),
                      FadeOut(lr), run_time=0.6)
            self.play(FadeIn(card, scale=0.97), run_time=0.6)
            vo.wait_until("Where should its default")
            self.play(flash(card.stem[-1], TURN, 1.04), run_time=0.7)
        bar = card.bar                     # the 10 s timer drains in silence (as mcq_ponder does)
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=card.seconds)
        bar.set_stroke(opacity=0)

        # ========================================================== 9 · reveal: C; why not A
        with self.voiceover(SAY[9]) as vo:
            self.play(*card.right("out + replies back · nothing uninvited in"), run_time=0.7)
            vo.wait_until("A, the Internet Gateway")
            self.play(*card.wrong("A", "makes the subnet public · a direct inbound path, guarded only by firewall rules"),
                      run_time=0.7)

        # ========================================================== 10 · why not B, D
        with self.voiceover(SAY[10]) as vo:
            self.play(*card.wrong("B", "local covers only 10.0.0.0/16 · the website is outside"), run_time=0.7)
            vo.wait_until("D fails")
            self.play(*card.wrong("D", "brings requests in to targets · not a way out"), run_time=0.7)
        self.play(FadeOut(card), run_time=0.6)

        # ========================================================== 11 · takeaway
        tk = takeaway(TAKEAWAY)
        inside(tk, "takeaway")
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeIn(VGroup(tk.frame, tk.head)), FadeIn(tk.rows[0], shift=RIGHT * 0.15), run_time=0.7)
            vo.wait_until("NAT only carries")
            self.play(FadeIn(tk.rows[1], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("And if NAT is down")
            self.play(FadeIn(tk.rows[2], shift=RIGHT * 0.15), run_time=0.5)
            self.play(flash(tk.rows[2], TURN, 1.03), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(tk), run_time=0.6)
        self.wait(0.3)
