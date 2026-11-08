"""S13 · The journey of one click (AC215 L22, the full follow-along). TRACKER [C] 4 throughout; the small
AsksChecklist sits top right from the first frame. Lecture: 22 · 5, 21, 38–39 (beat 0), 24, 26 (beat 3).

Beats (script.md "## S13", one voiceover block each):
0. LECTURE 22 · 5, 21, 38–39. DoorsStrip: GREY-dashed 'L20 · one nginx container in front',
   'tic-tac-toe · one LoadBalancer per app' (a BLUE door per app), 'cheese app · one door with a
   receptionist' (one BLUE door, the nginx figure, three PINK paths); each panel flashes on its sentence.
1. The strip leaves. A README card 'README.md · line 457' (top), then V7 RequestJourney builds lane by
   lane (README:459–474 redrawn): Browser → LoadBalancer Service → nginx Ingress Controller → frontend
   ClusterIP 3000 ('/') and api ClusterIP 9000 ('/api-service') → vector-db ClusterIP 8000; the GREEN
   vector-db-loader Job below. Each hop flashes as it is named.
2. The README's dotted arrow appears as a GREY ghost vdb → Job with the 'erratum' tag; on "The data
   flows the other way" it flips into a GREEN dotted Job → vdb arrow, 'one-time load'.
3. LECTURE 22 · 24, 26. The README card leaves. A PINK bubble '<IP>.sslip.io → <IP>' under the
   browser; a packet '<IP>.sslip.io' leaves the browser. A small V1 inset in the top band: BLUE
   'controllers' (lamp) → 'cloud provider API' → the load-balancer door; the lamp and arrows glow GREEN
   as the packet passes the door; the packet lands above nginx; GREY chip 'installed by Helm'.
4. CODE(setup_loadbalancer.py: 79–90) at the bottom (opaque, over the lanes): line 79 'host=host' PINK →
   the routing card's PINK header 'host: <IP>.sslip.io' (top band, above nginx; Indicates on "for that
   host"); line 84 '"/api-service"' YELLOW and line 90 'number=9000' → row '/api-service → api:9000';
   the panel scrolls to (96–104): line 97 '"/"', line 103 'number=3000' → row '/ → frontend:3000'. The
   panel leaves, a dotted PINK line ties the card to nginx; GREY-dashed 'L20 · nginx.conf / by hand'
   (left of the card) turns into 'now generated' (GREEN).
5. A packet '/api-service/status' rides to the api box with its prefix intact; L20's scissors appear
   GREY-dashed under api and are crossed out. CODE(api/service.py: 13) inset bottom-left, GREEN chip
   'ROOT_PATH=/api-service' (setup_containers.py:310–311) above it; the inset swaps to (service.py: 50);
   the api answers a PINK bubble '{"version": "3.0"}' back to the browser.
6. A packet '/' reaches frontend and becomes a GREY page that returns to the browser and spawns a new packet
   '/api-service/…' from the browser to api. CODE(.env.production: 2) inset, the value YELLOW.
7. A PINK packet 'vector-db:8000' rides api → vdb; S08's DNS card flashes bottom-left ('as in part 1 · a Service name → its IP').
8. A packet 'http://<IP>/' (no .sslip.io) rides to nginx; a YELLOW 'What answers?' card. PONDER 4 (8 s).
9. The ponder card leaves. The card's header flashes RED; the packet bounces back as a RED '404'; on "The
   rule matches" a GREY chip 'Host: <IP>' left of the routing card with a RED '≠', the header flashes again. GREEN chip 'app_url · http://<IP>.sslip.io'.
10. The journey leaves; the AsksChecklist grows to the centre, 'Load balancing' ticks YELLOW with the GREY
   note 'cloud LB at the door · nginx · Services across Pods'. Fade; empty frame.

Deviations from SHOW:
- Beat 3: no separate worker-node glyph (the lanes have none; the nginx box is where the packet lands,
  and it is flashed). The V1 inset is drawn here at full text size (MasterDiagram is 12.9 units wide and
  text may never be scaled down), as S12 does; its arrow to the door stops above the packet's waypoint.
- Beat 4: the routing card is built in the scene (same content as RequestJourney.routing_card) and sits
  higher, top band above nginx with a dotted tie, so the 12-line code panel fits under it. The code panel
  covers the lanes for that beat (opaque).
- Beat 5: the two one-line service.py insets appear one after the other in the same spot (two stacked
  would cover the '/api-service' path label).
- Beat 7: S08's DNS card is the tic-tac-toe one (web.default.svc…, the only lookup captured); a GREY
  chip 'as in part 1 · a Service name → its IP' says it is the same mechanism, not the cheese app's address.
- Beat 8: the packet's label is 'http://<IP>/'; the YELLOW 'What answers?' card sits bottom-left, and
  the opaque ponder card covers the lower right lanes (and half of the nginx box) while the timer runs.
- The AsksChecklist starts with S07's state (Failover ticked, its S07 note on the grown card).
- Hops are emphasised by flashing their text (Indicate on a whole hop floods its opaque fill).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S13"]
assert len(SAY) == SAY_COUNT["S13"] == 11

LB_PY = "src/deployment/deploy_k8s/setup_loadbalancer.py"
SVC_PY = "src/api-service/api/service.py"
ENV_FE = "src/frontend-react/.env.production"
CODE_BOTTOM = -3.5
S07_NOTE = "a restart, not a hot standby · keep replicas: 2"   # Failover's note, ticked in S07
BAND_LEFT = -6.5          # bottom-left inset spot (beats 5-7, 9)


def bl(m, y: float = CODE_BOTTOM):
    """Put m in the bottom-left inset spot."""
    return m.move_to([BAND_LEFT + m.width / 2, y + m.height / 2, 0])


def routing_card() -> VGroup:
    """The routing card (RequestJourney.routing_card's content), built row by row in beat 4."""
    hd = mono(f"host: {HOST_PH}", 20, ROUTE)
    r1 = VGroup(mono("/api-service", 20, TURN), label("→", 20, S.GREY), mono("api:9000", 20, INK)).arrange(RIGHT, buff=0.12)
    r2 = VGroup(mono("/", 20, TURN), label("→", 20, S.GREY), mono("frontend:3000", 20, INK)).arrange(RIGHT, buff=0.12)
    inner = VGroup(hd, r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    fr = RoundedRectangle(width=inner.width + 0.5, height=inner.height + 0.4, corner_radius=0.12,
                          stroke_color=ROUTE, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    inner.move_to(fr)
    c = VGroup(fr, inner)
    c.frame, c.head, c.r1, c.r2 = fr, hd, r1, r2
    return c


class OneClick(VoiceScene):
    def construct(self):
        trk = tracker_c(4)
        ac = AsksChecklist(small=True, ticked=(0,), notes={0: S07_NOTE})

        # ========================================================== 0. three ways to open a door
        ref = lref("5, 21, 38–39")
        ds = DoorsStrip()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ac), FadeIn(ref), run_time=0.6)
            ds.build(self, lag=0.5)
            assert ds.get_top()[1] < ac.get_bottom()[1] - 0.1, ds.get_top()
            vo.wait_until("Lecture 20 put")
            self.play(Indicate(ds.panels[0][1], color=S.GREY, scale_factor=1.04), run_time=0.8)
            self.add(ds)
            vo.wait_until("The game opened")
            self.play(Indicate(ds.panels[1][1], color=CLOUD, scale_factor=1.04), run_time=0.8)
            self.add(ds)
            vo.wait_until("The cheese app opens one door")
            self.play(Indicate(ds.panels[2][1], color=TURN, scale_factor=1.04), run_time=0.8)
            self.add(ds)
            vo.wait_until("with a receptionist")
            self.play(Indicate(ds.panels[2][-2], color=TURN, scale_factor=1.25), run_time=0.8)
            self.add(ds)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 1. the README's diagram, as lanes
        rc = readme_card(457, "Here is how the various services communicate\nbetween each other in the "
                              "Kubernetes cluster.")
        rc.move_to([-0.3, 2.15, 0])
        assert rc.get_right()[0] < ac.get_left()[0] - 0.1 and rc.get_top()[1] < trk.get_bottom()[1] - 0.05, rc
        rj = RequestJourney()
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(ds), FadeIn(rc, shift=DOWN * 0.2), run_time=0.6)
            self.remove(ds)
            rj.build(self, lag=0.35)
            assert rc.get_bottom()[1] > rj.hops["front"].get_top()[1] + 0.2
            for key, phrase in (("browser", "browser, load balancer"), ("lb", "load balancer, the nginx"),
                                ("nginx", "the nginx Ingress controller"), ("front", "then the frontend"),
                                ("api", "or the API on 9000"), ("vdb", "and the vector database")):
                vo.wait_until(phrase)
                self.play(Indicate(rj.hops[key].text, color=TURN, scale_factor=1.06), run_time=0.6)
                rj.heal(self)

        # ========================================================== 2. a small slip: the loader arrow
        with self.voiceover(SAY[2]) as vo:
            v, j = rj.hops["vdb"], rj.hops["job"]
            ghost = DashedLine(v.get_bottom(), j.get_top(), color=S.GREY, stroke_width=3, dash_length=0.08)
            ghost.add_tip(tip_length=0.16, tip_width=0.16)
            et = erratum_tag().next_to(ghost, LEFT, buff=0.15)
            vo.wait_until("the README draws the dotted arrow")
            rj.show(self, ghost, et, anims=[Create(ghost), FadeIn(et)], run_time=0.6)
            self.play(Indicate(rc.body, color=S.GREY, scale_factor=1.03), run_time=0.6)
            rj.heal(self)
            vo.wait_until("The data flows the other way")
            good = DashedLine(j.get_top(), v.get_bottom(), color=OWN, stroke_width=3, dash_length=0.08)
            good.add_tip(tip_length=0.16, tip_width=0.16)
            rj.swap(self, ghost, good, run_time=0.7)
            t1 = label("one-time load", 20, OWN).next_to(good, LEFT, buff=0.15)
            rj.swap(self, et, t1, run_time=0.5)
            vo.wait_until("from the Job into the database")
            self.play(Indicate(j.text, color=OWN, scale_factor=1.06), run_time=0.6)
            self.play(Indicate(v.text, color=OWN, scale_factor=1.06), run_time=0.6)
            rj.heal(self)

        # ========================================================== 3. follow one click
        ref = lref("24, 26")
        lbh, ngx = rj.hops["lb"], rj.hops["nginx"]
        cpa = boxed(["cloud provider API"], CLOUD, box_h=0.6).move_to([-3.55, 1.85, 0])
        ctl = boxed(["controllers"], CLOUD, box_h=0.6).move_to([0.9, 1.85, 0])
        lamp = Dot(radius=0.11, color=S.GREY).next_to(ctl, RIGHT, buff=0.15)
        a1 = arrow(ctl.get_left(), cpa.get_right(), S.GREY, buff=0.12)
        a2 = arrow(cpa.get_bottom(), lbh.get_top() + UP * 0.85, S.GREY, buff=0.1)
        cap = label("the controller asks; the cloud makes the door", 20, S.GREY).next_to(VGroup(cpa, ctl), UP, buff=0.15)
        inset = VGroup(cpa, ctl, lamp, a1, a2, cap)
        assert inset.get_right()[0] < ac.get_left()[0] - 0.1, inset.get_right()
        assert cap.get_top()[1] < trk.get_bottom()[1] - 0.05 or cap.get_left()[0] > trk.get_right()[0] + 0.1, cap
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(rc), FadeIn(ref), run_time=0.5)
            self.remove(rc)
            vo.wait_until("Follow one click")
            self.play(Indicate(rj.hops["browser"].text, color=TURN, scale_factor=1.08), run_time=0.6)
            rj.heal(self)
            vo.wait_until("Your IP dot sslip dot io")
            rj.dns(self)
            vo.wait_until("points back to that same IP")
            self.play(Indicate(VGroup(*rj.dns_b.text[-4:]), color=ROUTE, scale_factor=1.25), run_time=0.6)
            rj.heal(self)
            vo.wait_until("with no setup at all")
            self.play(Indicate(rj.dns_b.text, color=ROUTE, scale_factor=1.06), run_time=0.6)
            rj.heal(self)
            vo.wait_until("The packet passes")
            rj.drop(self, rj.dns_b, run_time=0.2)
            pk = rj.send(self, HOST_PH, ["browser", "lb"], per=0.4)
            self.play(FadeIn(VGroup(cpa, ctl, lamp, cap)), run_time=0.4)
            self.play(lamp.animate.set_color(OWN), GrowArrow(a1), run_time=0.4)
            self.play(a1.animate.set_color(OWN), GrowArrow(a2), run_time=0.4)
            self.play(a2.animate.set_color(OWN), Indicate(lbh.text, color=OWN, scale_factor=1.06), run_time=0.4)
            rj.heal(self)
            self.play(pk.animate.move_to(rj._above("nginx", pk)), run_time=0.4)
            vo.wait_until("lands on the nginx controller")
            helm = grey_chip("installed by Helm")
            helm.next_to(ngx, DOWN, buff=0.2)
            helm.shift(RIGHT * (rj.paths[("nginx", "api")][1].get_left()[0] - 0.25 - helm.get_right()[0]))
            assert helm.get_left()[0] > rj.hops["browser"].get_right()[0], helm.get_left()
            self.play(Indicate(ngx.text, color=TURN, scale_factor=1.06), FadeIn(helm, shift=UP * 0.1), run_time=0.6)
            rj.heal(self)
        self.play(FadeOut(ref), FadeOut(inset), FadeOut(helm), run_time=0.4)
        self.remove(ref, inset, helm)

        # ========================================================== 4. the Ingress rule, from code
        p1 = code(LB_PY, 79, 90, dedent=True, font_size=20)
        p1.move_to([0, CODE_BOTTOM + p1.height / 2, 0])
        p2 = code(LB_PY, 96, 104, dedent=True, font_size=20)
        p2.move_to(p1).align_to(p1, UP)
        assert p1.get_top()[1] < ac.get_bottom()[1] - 0.1, p1.get_top()
        back = Rectangle(width=12.9, height=p1.height + 0.15, stroke_width=0).set_fill(S.BG, 1)
        back.move_to([0, p1.get_y(), 0])
        rcard = routing_card()
        rcard.move_to([ngx.get_x(), 0, 0]).align_to(p1, UP).shift(UP * (rcard.height + 0.2))
        assert rcard.get_top()[1] < trk.get_bottom()[1] - 0.02 or rcard.get_left()[0] > trk.get_right()[0], rcard
        assert rcard.get_bottom()[1] > p1.get_top()[1] + 0.1
        tie = DashedLine(rcard.get_bottom(), ngx.get_top() + UP * 0.05, color=ROUTE, stroke_width=2.5,
                         dash_length=0.08)
        l20 = VGroup(dashed_chip("L20 · nginx.conf", size=22), label("by hand", 22, PAST)).arrange(DOWN, buff=0.12)
        l20.next_to(rcard, LEFT, buff=0.3)
        assert l20.get_left()[0] > -6.5 and l20.get_top()[1] < trk.get_bottom()[1] - 0.05, l20
        gen = label("now generated", 22, OWN).move_to(l20[1])
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(pk), FadeIn(back), FadeIn(p1, shift=UP * 0.2), run_time=0.6)
            self.remove(pk)
            vo.wait_until("The Ingress rule starts with the host name")
            h79 = code_span(p1.code, 0, "host=host")
            b79 = line_bar(p1.code, 0, ROUTE)
            self.play(FadeIn(b79), h79.animate.set_color(ROUTE), run_time=0.4)
            self.play(FadeIn(rcard.frame), run_time=0.3)
            self.play(TransformFromCopy(h79, rcard.head), run_time=0.7)
            self.bring_to_front(rcard.head)
            vo.wait_until("for that host")
            self.play(Indicate(rcard.head, color=ROUTE, scale_factor=1.1), run_time=0.6)
            vo.wait_until("slash api service goes to the API")
            h84 = code_span(p1.code, 84 - 79, '"/api-service"')
            b84 = line_bar(p1.code, 84 - 79, TURN)
            self.play(FadeIn(b84), h84.animate.set_color(TURN), run_time=0.4)
            h90 = code_span(p1.code, 90 - 79, "number=9000")
            b90 = line_bar(p1.code, 90 - 79, TURN)
            self.play(FadeIn(b90), h90.animate.set_color(TURN), TransformFromCopy(h84, rcard.r1), run_time=0.7)
            vo.wait_until("every other path to the frontend")
            self.play(FadeOut(VGroup(p1, b79, b84, b90), shift=UP * 0.3), run_time=0.35)
            self.remove(p1, b79, b84, b90)
            self.play(FadeIn(p2, shift=UP * 0.3), run_time=0.35)
            h97 = code_span(p2.code, 97 - 96, 'path="/"')
            b97 = line_bar(p2.code, 97 - 96, TURN)
            h103 = code_span(p2.code, 103 - 96, "number=3000")
            b103 = line_bar(p2.code, 103 - 96, TURN)
            self.play(FadeIn(b97), h97.animate.set_color(TURN), FadeIn(b103), h103.animate.set_color(TURN),
                      run_time=0.5)
            self.play(TransformFromCopy(h97, rcard.r2), run_time=0.7)
            vo.wait_until("The controller follows that rule")
            self.play(FadeOut(VGroup(back, p2, b97, b103)), Create(tie), run_time=0.6)
            self.remove(back, p2, b97, b103)
            self.add(rj)
            self.play(Indicate(ngx.text, color=TURN, scale_factor=1.06), run_time=0.6)
            rj.heal(self)
            vo.wait_until("like the nginx dot conf of lecture 20")
            self.play(FadeIn(l20, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("now generated")
            self.play(FadeOut(l20[1]), FadeIn(gen), run_time=0.5)
            self.remove(l20[1])
            l20.remove(l20[1])
            self.play(Indicate(gen, color=OWN, scale_factor=1.08), run_time=0.6)
        self.play(FadeOut(l20), FadeOut(gen), run_time=0.3)
        self.remove(l20, gen)
        card_g = VGroup(rcard, tie)

        # ========================================================== 5. the prefix is kept
        i13 = bl(code(SVC_PY, 13, font_size=20, shown="src/api-service/api/service.py"))
        i50 = bl(code(SVC_PY, 50, font_size=20, shown="src/api-service/api/service.py"))
        root = ok_chip("ROOT_PATH=/api-service", mono_font=True)
        root.next_to(i13, UP, buff=0.15).align_to(i13, LEFT)
        assert root.get_top()[1] < rj.hops["browser"].get_bottom()[1] - 0.1, root.get_top()
        assert i13.get_right()[0] < rj.hops["api"].get_left()[0], i13.get_right()
        with self.voiceover(SAY[5]) as vo:
            pk = rj.send(self, "/api-service/status", ["browser", "lb", "nginx", "api"], per=0.4)
            vo.wait_until("nothing strips it")
            rj.scissors_crossed(self)
            vo.wait_until("The API mounts itself")
            self.play(FadeIn(i13, shift=UP * 0.2), FadeIn(root, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("under its root path")
            self.play(Indicate(root, color=OWN, scale_factor=1.06),
                      code_span(i13.code, 0, "ROOT_PATH").animate.set_color(OWN), run_time=0.6)
            vo.wait_until("slash api service, so")
            self.play(FadeOut(i13), FadeIn(i50), run_time=0.5)
            self.remove(i13)
            self.play(code_span(i50.code, 0, "ROOT_PATH").animate.set_color(OWN), run_time=0.3)
            vo.wait_until("answers version three point zero")
            rj.drop_packet(self, pk)
            ans = rj.reply(self, "api", '{"version": "3.0"}')
        self.play(FadeOut(ans), FadeOut(i50), FadeOut(root), run_time=0.4)
        self.remove(ans, i50, root)
        rj.drop(self, rj.sc, run_time=0.3)

        # ========================================================== 6. the browser calls the API
        env = bl(code(ENV_FE, 2, font_size=20))
        val = code_span(env.code, 0, "/api-service")
        with self.voiceover(SAY[6]) as vo:
            pk = rj.send(self, "/", ["browser", "lb", "nginx", "front"], per=0.3)
            pg = file_glyph(0.6, S.GREY).move_to(pk)
            self.play(ReplacementTransform(pk, pg), run_time=0.4)
            self.remove(pk)
            self.play(pg.animate.next_to(rj.hops["browser"], UP, buff=0.62), run_time=0.8)
            rj.heal(self)
            vo.wait_until("then your browser calls the API")
            self.play(FadeIn(env, shift=UP * 0.2), val.animate.set_color(TURN), Indicate(pg, color=S.GREY),
                      run_time=0.5)
            pk = rj.send(self, "/api-service/…", ["browser", "lb", "nginx", "api"])
            self.play(FadeOut(pg), run_time=0.2)
            self.remove(pg)
            vo.wait_until("at slash api service")
            self.play(Indicate(val, color=TURN, scale_factor=1.1), run_time=0.5)
        rj.drop_packet(self, pk)
        self.play(FadeOut(env), run_time=0.3)
        self.remove(env)

        # ========================================================== 7. the API reaches Chroma by name
        dc = bl(dns_card(), -3.3)
        s08 = grey_chip("as in part 1 · a Service name → its IP").next_to(dc, UP, buff=0.15).align_to(dc, LEFT)
        assert s08.get_top()[1] < rj.hops["browser"].get_bottom()[1] - 0.1
        assert dc.get_right()[0] < rj.hops["job"].get_left()[0] - 0.1, dc.get_right()
        with self.voiceover(SAY[7]) as vo:
            vo.wait_until("the API reaches Chroma")
            pk = rj.send(self, f"vector-db:{PORTS['vdb']}", ["api", "vdb"], per=0.6)
            vo.wait_until("by its Service name")
            self.play(FadeIn(dc, shift=UP * 0.2), FadeIn(s08, shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(dc[1], color=ROUTE, scale_factor=1.05), run_time=0.7)
            vo.wait_until("on port 8000")
            self.play(Indicate(rj.hops["vdb"].text, color=ROUTE, scale_factor=1.06), run_time=0.6)
            rj.heal(self)
        rj.drop_packet(self, pk)
        self.play(FadeOut(dc), FadeOut(s08), run_time=0.3)
        self.remove(dc, s08)

        # ========================================================== 8. ponder: the bare IP
        qc = question_card("What answers?", size=24)
        bl(qc, -3.3)
        assert qc.get_bottom()[1] > -3.55
        with self.voiceover(SAY[8]) as vo:
            vo.wait_until("Now open the bare IP")
            pk = rj.send(self, f"http://{IP_PH}/", ["browser"], per=0.4)
            vo.wait_until("the same load balancer")
            for k in ("lb", "nginx"):
                self.play(pk.animate.move_to(rj._above(k, pk)), run_time=0.5)
            vo.wait_until("What answers?")
            self.play(FadeIn(qc, scale=0.95), run_time=0.4)
        self.play(FadeOut(qc), run_time=0.3)
        self.remove(qc)
        pw = 8.2
        pc = ponder(self, f"http://{IP_PH}/ — the same load balancer,\nwithout .sslip.io.\nWhat answers?", 8,
                    center=(2.2, -1.92), width=pw)
        assert pc.get_bottom()[1] > -3.55 and pc.get_right()[0] < 6.55 and pc.get_top()[1] < pk.get_bottom()[1] - 0.05, (pc.get_top(), pk.get_bottom())

        # ========================================================== 9. 404: the wrong name
        hc = grey_chip(f"Host: {IP_PH}", mono_font=True)
        ne = label("≠", 28, ERR)
        hg = VGroup(hc, ne).arrange(RIGHT, buff=0.2).next_to(rcard, LEFT, buff=0.2).align_to(rcard.head, UP)
        assert hg.get_left()[0] > -6.5 and hg.get_top()[1] < trk.get_bottom()[1] - 0.05, hg
        url = ok_chip(f"app_url · {APP_URL}", mono_font=True)
        bl(url, -3.3)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            self.play(Indicate(rcard.head, color=ERR, scale_factor=1.1), run_time=0.6)
            bad = rj.reject(self, pk)
            vo.wait_until("The rule matches only that host name")
            self.play(FadeIn(hc, shift=RIGHT * 0.2), run_time=0.4)
            self.play(FadeIn(ne), Indicate(rcard.head, color=ERR, scale_factor=1.1), run_time=0.7)
            vo.wait_until("so the same door")
            self.play(Indicate(lbh.text, color=CLOUD, scale_factor=1.06), run_time=0.6)
            rj.heal(self)
            self.play(Indicate(hc, color=ERR, scale_factor=1.06), run_time=0.6)
            self.play(Indicate(bad.text, color=ERR, scale_factor=1.15), run_time=0.6)
            rj.heal(self)
            vo.wait_until("Use the app URL")
            self.play(FadeIn(url, shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(url, color=OWN, scale_factor=1.05), run_time=0.6)
        self.play(FadeOut(bad), FadeOut(hg), run_time=0.3)
        self.remove(bad, hg)

        # ========================================================== 10. load balancing, ticked
        NOTE = "cloud LB at the door · nginx · Services across Pods"
        probe = AsksChecklist()
        w0 = probe.card.frame.width
        off = probe.card.rows[1].note.get_left()[0] - probe.card.frame.get_left()[0]
        w1 = max(w0, off + max(label(NOTE, 20).width, label(S07_NOTE, 20).width) + 0.4)
        cx = -(w1 - w0) / 2
        assert cx - w0 / 2 > -6.5 and cx - w0 / 2 + w1 < 6.5, (cx, w0, w1)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(rj), FadeOut(card_g), FadeOut(url), run_time=0.5)
            self.remove(rj, card_g, url)
            ac.grow(self, center=(cx, 0.2))
            vo.wait_until("That ticks load balancing")
            fr = ac.card.frame
            wide = RoundedRectangle(width=w1, height=fr.height, corner_radius=0.14, stroke_color=TURN,
                                    stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
            wide.move_to(fr).align_to(fr, LEFT)
            self.play(Transform(fr, wide), run_time=0.4)
            ac.heal(self)
            ac.tick(self, 1, note=NOTE)
            nt = ac.card.rows[1].note
            vo.wait_until("the cloud load balancer at the door")
            self.play(Indicate(nt, color=CLOUD, scale_factor=1.05), run_time=0.6)
            self.add(ac)
            vo.wait_until("each Service spreading requests")
            self.play(Indicate(nt, color=ROUTE, scale_factor=1.05), run_time=0.6)
            self.add(ac)

        self.play(FadeOut(VGroup(trk, ac)), run_time=0.6)
        self.remove(trk, ac)
        self.wait(0.4)
