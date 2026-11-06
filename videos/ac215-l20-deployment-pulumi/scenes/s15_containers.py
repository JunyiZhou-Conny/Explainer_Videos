"""S15 · Steps 5–6: containers over SSH, then test (AC215 L20). No tracker in beats 0-11; TRACKER [P] 13
in beats 12-13.

Beats (script.md "## S15", one voiceover block each):
0. Lecture 20 · slide 19. The six-step strip (chips 1-4 ticked, chip 5 'Containers' YELLOW) shrinks
   away. CODE(setup_containers.py: 27-31): the stack name on line 27 PINK, lines 29-31 GREEN. V6
   returns: the pipe 'StackReference · organization/deploy-images/dev' joins a 'deploy-images' card
   to the 'deploy-single-vm' card; the ticket with the timestamp slides down it.
1. CODE(setup_containers.py: 79-90): line 81 PINK, lines 84-85 PURPLE. A GREY laptop (Pulumi + three
   TEAL container cards) and the BLUE VM ('the VM's Docker') joined by a PINK SSH tunnel; the cards
   get GREEN '+' glyphs and copies travel through the tunnel.
2. Lecture 20 · slide 23. V1: the GREY pull arrow registry -> VM; frontend, vector-db 8000,
   api-service 9000; slide 23's 'HTTP 80' ghost flips to 3000 (GREY erratum tag); the dashed loader
   pours and leaves; the GREEN 'appnetwork' cable; a GREY erratum chip 'same mount slip as part 1 …'
   with a dashed ring on vector-db.
3. Lecture 20 · slide 24. A YELLOW chip '6 Web server · setup_webserver.py'; nginx on top, the PINK
   'HTTP 80' door drops onto it, the browser and the request arrows; two GREY doors '3000' and '9000'
   on the GCP wall, struck RED.
4. CODE(setup_webserver.py: 44-55): line 45 YELLOW, line 53 GREEN. A file card nginx.conf: one line
   turns YELLOW; three tiles 'upload · move · restart' replay; a GREY chip 'VM · disk · containers:
   unchanged' stays still.
5. Header 'a successful pulumi up · drawn from the code' + illustration tag over V1: five layers light
   GREEN (fences, disk + VM, the chip '9 provision steps', containers, nginx); then the end card with
   the six export names (__main__.py:29-34), placeholders for the values; instance_ip YELLOW.
6. The ssh_command row expands: CODE(__main__.py: 34) with a GREY erratum tag; a copy of the command
   gets the GREEN insert '-i /secrets/ssh-key-deployment'.
7. Lecture 20 · slides 25–26. V1 again; three RED-dashed callouts with numbered PINK circles on the
   push arrow (1), the pull arrow (2) and the models link (3).
8. LECTURE (held). The two keys hover above the VM, dim. PONDER 8 s.
9. LECTURE (held). The GREEN key lands on the VM and lights; the BLUE key gets a RED chip 'creates
   VMs, disks, buckets' and moves back by the laptop.
10. LECTURE (held). Footnotes: a PINK arrow from the BLUE key to callout 2 and the caption 'Pulumi pulls
   with your deployment credentials'; the badge 'deployment@…' in a GREY dashed 'scopes' fence on the
   VM; a PINK arrow api-service -> Vertex AI with the GREEN key; the GREY chip 'this repo: …'.
11. Lecture 20 · slide 27. Title 'Test the App'; a GREY browser (illustration) at http://<instance_ip>/
   with the footer 'Frontend version · API version' (YELLOW) and a PINK chip 'from /status'; V3 with
   its gates replays /api-service/status: gate 80 opens, the scissors snip, 3000 / 9000 stay shut.
12. TRACKER [P] 13. Terminal cheese-app-vm + GREY chip 'our part 1 stand-in · same names except
   vector-db'. `sudo docker container ls` -> vm/52: 2-6 (from the PORTS column), NAMES cell
   'cheese-app-vector-db' YELLOW + GREY 'Pulumi: vector-db'; `… logs api-service -f` -> vm/53: 2, …,
   26, …, 53-56, 59 (^C YELLOW, 'Control C stops following'; GREY chip on the root path); `… logs
   frontend -f` -> vm/54: 2, 7-9; `… logs nginx -f` -> vm/55: 9-11, 15.
13. `sudo docker exec -it api-service /bin/bash` -> vm/56: 2-6 (the id GREY); `sudo docker exec -it nginx
   /bin/bash` -> vm/57: 2-5 with 'at the time of recording'; a GREY note card on GENERATIVE_MODEL;
   YELLOW '▶ your turn'. Fade; empty frame.

Deviations from SHOW:
- Beat 0: the V6 pipe is drawn without the shelf and crates (the code panel needs the left half): a
  GREEN 'deploy-images' card stands for the images stack at the top of the pipe. The ticket is
  added after the pipe so it travels over the tube (TimestampPipe.pipe() draws the tube over it).
- Beat 0/4/6: code panels use elide/cuts (GREY '…') so a picture fits beside them.
- Beat 1: the picture is a small laptop/VM drawing of our own (V4's '+' glyphs on TEAL cards), not V4.
- Beat 2: the erratum 'dots' are GREY erratum tags / a GREY dashed ring (no dot glyph exists); the
  mount-slip chip sits above the picture (no room inside the VM).
- Beat 3: the strip is not on screen any more (V1 fills the frame), so chip 6 appears alone as a
  YELLOW chip above the picture. The ghost doors sit on the GCP outline's top edge.
- Beat 5: the 'GREY-outlined panel' is the header line + illustration tag over the full-frame V1
  (V1 cannot shrink: text never scales). The end card replaces the picture.
- Beat 7: the bubbles sit beside the picture (bubble 1 and 2 left of GCP, bubble 3 above the models
  pail); a numbered PINK circle marks each spot on the picture, the same number heads its bubble.
- Beat 9/10: the BLUE key 'moves back' to the empty space under the laptop. The amendment caption
  'Pulumi pulls with your deployment credentials' sits in the top band; the 'scopes' fence and the
  badge sit just above the VM's edge, joined to it by a short GREY line; Vertex AI is a BLUE box above
  the VM.
- Beat 11: the V3 picture has no VM outline around it (gates = the VM's firewall doors).
- Beat 12: vm/52's rows are 148 characters wide: printed from the PORTS column on with a GREY '…'
  (as S07 does with vm/47); vm/53:53 and vm/55:9 are wrapped.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S15"]
assert len(SAY) == SAY_COUNT["S15"] == 14

# ------------------------------------------------------------------ the real sources (checked)
SC = "src/deployment/deploy_single_vm/setup_containers.py"
SW = "src/deployment/deploy_single_vm/setup_webserver.py"
SC_SHOWN, SW_SHOWN = "deploy_single_vm/setup_containers.py", "deploy_single_vm/setup_webserver.py"
MAIN = "src/deployment/deploy_single_vm/__main__.py"
assert 'pulumi.StackReference("organization/deploy-images/dev")' in excerpt(SC, 27, 27)
assert all("images_stack.get_output(" in excerpt(SC, n, n) for n in (29, 30, 31))
assert "docker.Provider(" in excerpt(SC, 79, 79)
assert 'f"ssh://{ssh_user}@{ip}"' in excerpt(SC, 81, 81)
assert excerpt(SC, 84, 84).strip() == '"-i",' and excerpt(SC, 85, 85).strip() == '"/secrets/ssh-key-deployment",'
assert 'container_path="/chroma/chroma"' in excerpt(SC, 153, 153)
assert 'checksum = file_checksum("../nginx-conf/nginx/nginx.conf")' in excerpt(SW, 45, 45)
assert excerpt(SW, 53, 53).strip() == "triggers=[nginx_conf_asset, checksum],"
assert excerpt(SW, 66, 66).strip() == excerpt(SW, 53, 53).strip()           # move: same trigger
assert "triggers=[nginx_conf_asset, checksum]" in excerpt(SW, 111, 111)     # restart: same trigger
assert [excerpt(MAIN, n, n).split('"')[1] for n in range(29, 35)] == list(EXPORTS)
assert 'f"ssh {ssh_user}@{ip}"' in excerpt(MAIN, 34, 34)

V52, V53, V54, V55, V56, V57 = (capture(f"vm/{n}") for n in (52, 53, 54, 55, 56, 57))
assert V52.cmd == readme(373) == "sudo docker container ls"
assert V53.cmd == readme(374) == "sudo docker container logs api-service -f"
assert V54.cmd == readme(375) == "sudo docker container logs frontend -f"
assert V55.cmd == readme(376) == "sudo docker container logs nginx -f"
assert V56.cmd == readme(381) == "sudo docker exec -it api-service /bin/bash"
assert V57.cmd == readme(382) == "sudo docker exec -it nginx /bin/bash"
COL = V52.line(2).index("PORTS")
PS_ROWS = ["…  " + V52.line(n)[COL:] for n in range(2, 7)]
assert PS_ROWS[-1].endswith(C_VDB) and PS_ROWS[0].split() == ["…", "PORTS", "NAMES"]
assert V53.line(26) == "Loading CNN Model..." and V53.line(59) == "^C"
assert "Uvicorn running on http://0.0.0.0:9000" in V53.line(53)
assert all('"GET /api-service/' in V53.line(n) for n in (54, 55, 56))
assert V54.line(9) == "^C" and V54.line(8) == "BASE_API_URL: /api-service"
assert V55.line(15) == "^C" and "ready for start up" in V55.line(9)
assert V56.line(5).endswith(":/app$ exit") and V56.line(6) == "exit"
assert V57.line(3) == "nginx version: nginx/1.30.6" and V57.line(5) == "exit"
assert "--root-path /api-service" in capture("vm/37").line(20)

# ------------------------------------------------------------------ small local helpers


def span_bar(code_, k0: int, k1: int, color, opacity: float = 0.2) -> Rectangle:
    """One translucent bar over lines k0..k1 (0-based) of a code_block."""
    top, bot = line_bar(code_, k0, color), line_bar(code_, k1, color)
    h = top.get_top()[1] - bot.get_bottom()[1]
    return Rectangle(width=top.width, height=h, stroke_width=0).set_fill(color, opacity).move_to(
        [top.get_center()[0], (top.get_top()[1] + bot.get_bottom()[1]) / 2, 0])


def green_card(text: str) -> VGroup:
    """A stack card in TimestampPipe's style (GREEN outline, label font)."""
    t = label(text, 20, INK)
    fr = RoundedRectangle(width=t.width + 0.4, height=0.55, corner_radius=0.08, stroke_color=OWN,
                          stroke_width=3).set_fill(tint(OWN, 0.12), 1)
    g = VGroup(fr, t.move_to(fr))
    g.frame = fr
    return g


def num_circle(n: int, r: float = 0.21) -> VGroup:
    c = Circle(radius=r, stroke_color=ROUTE, stroke_width=3).set_fill(S.BG, 1)
    return VGroup(c, label(str(n), 20, ROUTE).move_to(c))


def bubble(n: int, kind: str, text: str, bw: float = 0.0) -> VGroup:
    """Slide 26's callout: RED dashed frame, a numbered PINK circle, the key's file (key colour) and
    what it is for."""
    fname, col = {"deploy": ("deployment.json", CLOUD), "service": ("gcp-service.json", OWN)}[kind]
    top = VGroup(num_circle(n, 0.19), label(text, 20, INK)).arrange(RIGHT, buff=0.14)
    body = VGroup(top, label(fname, 20, col)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    bw = max(bw, body.width + 0.3)
    ob = outline_box(bw, body.height + 0.3, ERR, solid=False, fill_opacity=0.0)
    ob.fill.set_fill(S.BG, 1)
    body.move_to(ob).align_to(ob, LEFT).shift(RIGHT * 0.15)
    g = VGroup(ob, body)
    g.frame, g.body = ob, body
    return g


def ghost_door(port: str) -> VGroup:
    d = door(port, S.GREY, door_w=1.0)
    d.add(Line(d.get_left(), d.get_right(), color=ERR, stroke_width=6))
    return d


def plus(h: float = 0.3) -> VGroup:
    a = h / 2
    return VGroup(Line([-a, 0, 0], [a, 0, 0]), Line([0, -a, 0], [0, a, 0])).set_stroke(OWN, 5)


class ContainersOverSsh(VoiceScene):
    def construct(self):
        # ========================================================== 0. step 5: the StackReference pipe
        ref0 = lref("19")
        ss = six_steps(5)
        ss.move_to([0, 0, 0]).shift(UP * (2.95 - ss.get_top()[1]))
        assert ss.get_top()[1] < ref0.get_bottom()[1] - 0.05
        p0 = code(SC, 27, 31, dedent=True, font_size=20, shown=SC_SHOWN, elide={27: "images_stack = pulumi.",
                                                                29: "images_stack.get_output(",
                                                                30: "images_stack.get_output(",
                                                                31: "images_stack.get_output("},
                  cuts={28: "# Get the image tags"})
        p0.move_to([0, 0, 0]).align_to([-6.4, 0, 0], LEFT).align_to([0, 2.75, 0], UP)
        name27 = code_span(p0.code, 0, '"organization/deploy-images/dev"')
        b29 = span_bar(p0.code, 2, 4, OWN)
        tp = TimestampPipe()
        tp.shift(np.array([-0.15, -1.25, 0]))
        src = green_card("deploy-images").move_to(tp.p(4.95, 2.35))
        assert p0.get_right()[0] < src.get_left()[0] - 0.2, (p0.get_right(), src.get_left())
        assert p0.get_right()[0] < tp.p(4.95, 0)[0] - 1.55, p0.get_right()     # the ticket's left edge
        assert p0.get_bottom()[1] > tp.p(0, -1.6)[1] + 0.1, p0.get_bottom()
        assert tp.p(4.95, -1.95)[1] - 0.28 > -3.55
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref0), FadeIn(ss, shift=DOWN * 0.15), run_time=0.6)
            self.play(ss.light(5), run_time=0.7)
            self.add(ss)
            vo.wait_until("The VM program asks the images stack")
            ss.shrink_away(self, run_time=0.4)
            self.play(FadeIn(p0, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(b29), run_time=0.4)
            self.play(FadeIn(src, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("through a stack reference")
            self.play(name27.animate.set_color(ROUTE), run_time=0.4)
            self.add(p0, b29)
            tp.pipe(self, run_time=0.6)
            tp.ticket(self, run_time=0.6)
            vo.wait_until("So run up in deploy images first")
            self.play(Indicate(src, color=OWN, scale_factor=1.1), run_time=0.6)
            self.play(tp.ticket_m.animate.move_to(tp.p(4.95, -1.05)), run_time=1.0)
            self.play(Indicate(tp.card, color=OWN, scale_factor=1.06), run_time=0.5)
            tp.heal(self)
        self.play(FadeOut(VGroup(p0, b29, tp, src, ref0)), run_time=0.5)
        self.remove(p0, b29, tp, src, ref0)

        # ========================================================== 1. a Docker provider over SSH
        p1 = code(SC, 79, 90, dedent=True, font_size=20, shown=SC_SHOWN, elide={81: "instance_ip.apply(lambda ip: "},
                  cuts={82: "# SSH options"})
        p1.move_to([0, 0, 0]).align_to([-6.4, 0, 0], LEFT).align_to([0, 2.75, 0], UP)
        b81 = line_bar(p1.code, 2, ROUTE, 0.22)
        b84 = span_bar(p1.code, 5, 6, TOOL, 0.25)
        x0 = p1.get_right()[0] + 0.35
        xr = 6.4
        xc = (x0 + xr) / 2
        lap = RoundedRectangle(width=xr - x0, height=2.3, corner_radius=0.14, stroke_color=LAPTOP,
                               stroke_width=3).set_fill(tint(LAPTOP, 0.06), 1).move_to([xc, 1.6, 0])
        lap_t = label("laptop · toolbox", 20, LAPTOP).move_to(lap.get_corner(UL) + np.array([0.15, -0.25, 0]),
                                                              aligned_edge=LEFT)
        pul = tool_chip("Pulumi").move_to([x0 + 0.25, 1.4, 0], aligned_edge=LEFT)
        cards = VGroup(*[box_chip(n) for n in (C_FRONT, C_API, "vector-db")]).arrange(DOWN, buff=0.1,
                                                                                      aligned_edge=LEFT)
        cards.move_to([xr - 0.2, 1.58, 0], aligned_edge=RIGHT)
        assert cards.get_left()[0] > pul.get_right()[0] + 0.45, (cards.get_left(), pul.get_right())
        assert cards.get_top()[1] < lap.get_top()[1] - 0.1 and cards.get_bottom()[1] > lap.get_bottom()[1] + 0.05, \
            (cards.get_top(), cards.get_bottom(), lap.get_top(), lap.get_bottom())
        assert cards.get_left()[0] > lap_t.get_right()[0] + 0.1 or cards.get_top()[1] < lap_t.get_bottom()[1]
        pluses = VGroup(*[plus(0.24).next_to(c, LEFT, buff=0.12) for c in cards])
        vm = RoundedRectangle(width=xr - x0, height=1.35, corner_radius=0.14, stroke_color=CLOUD,
                              stroke_width=3).set_fill(tint(CLOUD, 0.06), 1).move_to([xc, -2.05, 0])
        vm_t = label("the VM", 20, CLOUD).move_to(vm.get_corner(UL) + np.array([0.15, -0.25, 0]), aligned_edge=LEFT)
        dock = tool_chip("Docker").move_to([x0 + 0.25, -2.2, 0], aligned_edge=LEFT)
        slots = VGroup(*[RoundedRectangle(width=0.42, height=0.42, corner_radius=0.06, stroke_color=CONTAINER,
                                          stroke_width=3).set_fill(tint(CONTAINER, 0.25), 1) for _ in range(3)])
        slots.arrange(RIGHT, buff=0.18).move_to([xr - 1.2, -2.2, 0])
        tun_x = xc - 0.35
        tunnel = VGroup(Line([tun_x - 0.13, lap.get_bottom()[1], 0], [tun_x - 0.13, vm.get_top()[1], 0]),
                        Line([tun_x + 0.13, lap.get_bottom()[1], 0], [tun_x + 0.13, vm.get_top()[1], 0])
                        ).set_stroke(ROUTE, 4)
        ssh_l = label("SSH", 22, ROUTE).next_to(tunnel, LEFT, buff=0.2)
        skey = key_icon("ssh", name=False, key_w=0.7).next_to(tunnel, RIGHT, buff=0.2)
        cap1 = label("Pulumi → SSH → the VM's Docker", 20, ROUTE).move_to([xc, -3.2, 0])
        assert cap1.get_left()[0] > x0 - 0.3 and cap1.get_right()[0] < 6.55, (cap1.get_left(), cap1.get_right())
        assert p1.get_bottom()[1] > -3.55, p1.get_bottom()
        pic1 = VGroup(lap, lap_t, pul, cards, vm, vm_t, dock, tunnel, ssh_l, skey, cap1)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("whose host is SSH")
            self.play(FadeIn(b81), Indicate(code_span(p1.code, 2, 'f"ssh://{ssh_user}@{ip}"'), color=ROUTE,
                                                     scale_factor=1.06), run_time=0.7)
            self.add(p1, b81)
            self.play(FadeIn(VGroup(lap, lap_t, pul)), FadeIn(VGroup(vm, vm_t, dock)), run_time=0.5)
            self.play(Create(tunnel), FadeIn(ssh_l), FadeIn(cap1), run_time=0.7)
            vo.wait_until("with your key")
            self.play(FadeIn(b84), FadeIn(skey, shift=LEFT * 0.1), run_time=0.5)
            self.play(Indicate(skey, color=TOOL, scale_factor=1.15), run_time=0.5)
            vo.wait_until("so each container on the VM")
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.15) for c in cards], lag_ratio=0.2), run_time=0.6)
            vo.wait_until("is a resource Pulumi can compare")
            self.play(LaggedStart(*[GrowFromCenter(p) for p in pluses], lag_ratio=0.2), run_time=0.6)
            dots = VGroup(*[pulse_dot(CONTAINER, 0.1).move_to([tun_x, lap.get_bottom()[1], 0]) for _ in range(3)])
            self.play(LaggedStart(*[d.animate.move_to([tun_x, vm.get_top()[1], 0]) for d in dots], lag_ratio=0.3),
                      run_time=1.0)
            self.play(*[ReplacementTransform(d, s) for d, s in zip(dots, slots)], run_time=0.5)
        self.play(FadeOut(VGroup(p1, b81, b84, pic1, pluses, slots)), run_time=0.5)
        self.remove(p1, b81, b84, pic1, pluses, slots)

        # ========================================================== 2. slide 23: three containers
        ref2 = lref("23")
        md = MasterDiagram(built=("laptop", "gcp", "registry", "push", "models", "vm", "disk"))
        er_front = erratum_tag().move_to(md.p(1.95, 0.3))
        net = VGroup(Line(md.p(2.9, -0.62), md.p(4.0, -0.62)),
                     Line(md.p(1.95, -0.98), md.p(1.95, -1.85)),
                     Line(md.p(1.95, -1.85), md.p(4.0, -1.85))).set_stroke(OWN, 5)
        net_l = mono(APPNET, 20, OWN).move_to(md.p(2.95, -1.6))
        slip = grey_chip("same mount slip as part 1: data in /data, not on the disk")
        er_slip = erratum_tag()
        slip_g = VGroup(er_slip, slip).arrange(RIGHT, buff=0.2).move_to([0, 2.15, 0]).align_to([6.4, 0, 0], RIGHT)
        assert slip_g.get_left()[0] > md.p(-3.3, 0)[0], slip_g.get_left()
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(md), FadeIn(ref2), run_time=0.6)
            md.pull(self)
            vo.wait_until("the frontend")
            md.box(self, "front")
            vo.wait_until("the vector database on 8000")
            md.box(self, "vdb")
            vo.wait_until("the API on 9000")
            md.box(self, "api")
            vo.wait_until("The slide puts the frontend on 80")
            md.front_port_fix(self)
            md.show(self, er_front, anims=[FadeIn(er_front, shift=DOWN * 0.1)], run_time=0.4)
            md.loader(self)
            md.show(self, net, net_l, anims=[Create(net), FadeIn(net_l)], run_time=0.7)
            vring = ring(md.parts["vdb"].frame, S.GREY, buff=0.1, dashed=True)
            md.show(self, slip_g, vring, anims=[FadeIn(slip_g, shift=DOWN * 0.1), Create(vring)], run_time=0.6)

        # ========================================================== 3. slide 24: the web server
        ref3 = lref("24")
        c6 = chip("6 Web server · setup_webserver.py", TURN, size=20).move_to([-0.4, 2.2, 0])
        gd3, gd9 = ghost_door("3000").move_to(md.p(0.1, 1.45)), ghost_door("9000").move_to(md.p(1.4, 1.45))
        with self.voiceover(SAY[3]) as vo:
            md.drop(self, slip_g, vring, er_front, extra=[ReplacementTransform(ref2, ref3)], run_time=0.4)
            self.play(FadeIn(c6, shift=DOWN * 0.15), run_time=0.4)
            self.play(Indicate(c6, color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("The nginx container appears on top")
            md.box(self, "nginx")
            vo.wait_until("and port 80 moves onto it")
            md.door(self, on="nginx")
            md.show(self, gd3, gd9, anims=[GrowFromCenter(gd3), GrowFromCenter(gd9)], run_time=0.5)
            br = md.browser(self, f"http://{IP_PH}/")
            assert br.get_left()[0] > c6.get_right()[0] + 0.1 or br.get_top()[1] < c6.get_bottom()[1]
            md.routes(self)
            self.play(*[Indicate(g[1], color=ERR, scale_factor=1.1) for g in (gd3, gd9)], run_time=0.6)
            md.heal(self)
        self.play(FadeOut(VGroup(md, c6, ref3)), run_time=0.5)
        self.remove(md, c6, ref3)

        # ========================================================== 4. the checksum trigger
        p4 = code(SW, 44, 55, dedent=True, font_size=20, shown=SW_SHOWN,
                  elide={45: '"../nginx-conf/nginx/nginx.conf"', 54: "depends_on=[create_nginx_conf_dir]"},
                  cuts={47: "# Copy nginx configuration file"})
        p4.move_to([0, 0, 0]).align_to([-6.4, 0, 0], LEFT).align_to([0, 2.75, 0], UP)
        b45 = line_bar(p4.code, 1, TURN, 0.25)
        b53 = line_bar(p4.code, 9, OWN, 0.25)
        x0 = p4.get_right()[0] + 0.4
        xc = (x0 + 6.4) / 2
        fc = file_card("nginx.conf", OWN).move_to([xc, 2.2, 0])
        flines = VGroup(*[Line(LEFT * 0.9, RIGHT * w, color=S.GREY_DARK, stroke_width=5) for w in (0.9, 0.5, 0.7)])
        flines.arrange(DOWN, buff=0.16, aligned_edge=LEFT).next_to(fc, DOWN, buff=0.22)
        dm = ProvisionDominoes(("upload", "move", "restart"), rows=(3,))
        dm.move_to([-1.3, -2.8, 0])
        rest = dashed_chip("VM, disk, containers: unchanged").move_to([xc, -0.2, 0])
        assert dm.get_top()[1] < p4.get_bottom()[1] - 0.15 and dm.get_bottom()[1] > -3.55, (dm.get_top(), p4.get_bottom())
        assert rest.get_left()[0] > p4.get_right()[0] + 0.1 and rest.get_right()[0] < 6.5, rest.get_right()
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeIn(p4, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("uploaded with a checksum")
            self.play(FadeIn(b45), run_time=0.4)
            self.play(Indicate(code_span(p4.code, 1, "file_checksum("), color=TURN, scale_factor=1.06), run_time=0.6)
            self.add(p4, b45)
            vo.wait_until("as a trigger")
            self.play(FadeIn(b53), run_time=0.4)
            self.play(Indicate(code_span(p4.code, 9, "checksum"), color=OWN, scale_factor=1.1), run_time=0.6)
            self.add(p4, b45, b53)
            self.play(FadeIn(fc), FadeIn(flines), FadeIn(dm), FadeIn(rest), run_time=0.5)
            vo.wait_until("Change nginx dot conf")
            self.play(flines[1].animate.set_color(TURN).put_start_and_end_on(flines[1].get_start(),
                                                                             flines[1].get_end() + RIGHT * 0.6),
                      run_time=0.6)
            self.play(Indicate(fc.text, color=TURN, scale_factor=1.08), run_time=0.5)
            self.add(fc)
            vo.wait_until("and only these steps run again")
            dm.replay(self, [0, 1, 2], per=0.3)
        self.play(FadeOut(VGroup(p4, b45, b53, fc, flines, dm, rest)), run_time=0.5)
        self.remove(p4, b45, b53, fc, flines, dm, rest)

        # ========================================================== 5. illustration: a successful up
        md = MasterDiagram(built=("laptop", "gcp", "registry", "push", "pull", "models", "vm", "disk", "front", "api", "vdb",
                                  "nginx", "door80"))
        md.parts["door80"].move_to(md.p(4.65, 0.84))
        rt = md._make("routes")
        md.parts["routes"] = rt
        md.add(rt)
        head = label("a successful pulumi up · drawn from the code", 22, S.GREY)
        ill5 = illustration_tag()
        hg = VGroup(head, ill5).arrange(RIGHT, buff=0.3).move_to([0, 3.15, 0]).align_to([-6.4, 0, 0], LEFT)
        nine = ok_chip("9 provision steps").move_to(md.p(1.9, -2.85))
        assert nine.get_right()[0] < md.parts["disk"].frame.get_left()[0] - 0.1, nine.get_right()
        ex_rows = VGroup(mono("instance_name", 22, INK),
                         VGroup(mono("instance_ip:", 22, INK), mono(IP_PH, 22, ROUTE)).arrange(RIGHT, buff=0.2),
                         mono("zone", 22, INK), mono("persistent_disk_name", 22, INK),
                         VGroup(mono("ssh_user:", 22, INK), mono(SA_SHORT, 22, TURN)).arrange(RIGHT, buff=0.2),
                         mono("ssh_command", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        endc = card(list(ex_rows), color=OWN, head="Outputs · drawn from the code", size=22)
        endc.move_to([0, 0, 0]).align_to([0, 2.8, 0], UP)
        ill_e = illustration_tag().next_to(endc, RIGHT, buff=0.3).align_to(endc, UP)
        assert endc.get_top()[1] < 2.85 and ill_e.get_right()[0] < 6.5
        layers = [["gcp"], ["disk", "vm"], None, ["front", "api", "vdb"], ["nginx"]]
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeIn(md), FadeIn(hg), run_time=0.6)
            vo.wait_until("So here is what it builds")
            self.play(Indicate(head, color=INK, scale_factor=1.04), run_time=0.5)
            for keys in layers:
                if keys is None:
                    md.show(self, nine, anims=[FadeIn(nine, scale=1.2)], run_time=0.4)
                    continue
                self.play(*[md.light(k, OWN) for k in keys], run_time=0.45)
            self.play(md.parts["door80"].plate.animate.set_stroke(OWN), run_time=0.3)
            md.heal(self)
            vo.wait_until("It ends on six outputs")
            self.play(FadeOut(md), FadeOut(hg), run_time=0.4)
            self.remove(md, hg)
            self.play(FadeIn(endc), FadeIn(ill_e), run_time=0.5)
            vo.wait_until("among them the instance IP")
            self.play(Indicate(ex_rows[1], color=TURN, scale_factor=1.08), run_time=0.7)
            self.add(endc)

        # ========================================================== 6. erratum: the SSH command's key
        p6 = code(MAIN, 34, elide={34: "instance_ip.apply(lambda ip: "})
        p6.move_to([0, -1.65, 0])
        er6 = erratum_tag().next_to(p6, UP, buff=0.12).align_to(p6, RIGHT)
        c_ssh = mono("ssh", 24, INK)
        c_ins = mono("-i /secrets/ssh-key-deployment", 24, OWN)
        c_rest = mono(f"{SA_SHORT}@{IP_PH}", 24, INK)
        full = VGroup(c_ssh.copy(), c_ins, c_rest.copy()).arrange(RIGHT, buff=0.24, aligned_edge=UP).move_to([0, -3.0, 0])
        c_ssh.move_to(full[0])
        c_rest.next_to(c_ssh, RIGHT, buff=0.24).align_to(c_ssh, UP)
        assert full.get_right()[0] < 6.5 and full.get_left()[0] > -6.5, full.get_right()
        bar6 = hl_bar(ex_rows[5], TURN, 0.25)
        link = DashedLine(ex_rows[5].get_bottom() + DOWN * 0.05, p6.get_top() + UP * 0.03, color=S.GREY,
                          stroke_width=3)
        assert p6.get_top()[1] < endc.get_bottom()[1] - 0.3, (p6.get_top(), endc.get_bottom())
        assert er6.get_bottom()[1] > endc.get_bottom()[1] or er6.get_left()[0] > endc.get_right()[0] + 0.1
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(bar6), Indicate(ex_rows[5], color=TURN, scale_factor=1.08), run_time=0.6)
            self.add(endc, bar6)
            self.play(Create(link), FadeIn(p6, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(er6, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("leaves out the key")
            fs = code_span(p6.code, 0, 'f"ssh {ssh_user}@{ip}"')
            self.play(Indicate(fs, color=ERR, scale_factor=1.08), run_time=0.7)
            self.add(p6)
            self.play(FadeIn(VGroup(c_ssh, c_rest), shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Add dash i")
            self.play(c_rest.animate.move_to(full[2]), FadeIn(c_ins, shift=UP * 0.4), run_time=0.8)
            self.play(Indicate(c_ins, color=OWN, scale_factor=1.06), run_time=0.6)
        self.play(FadeOut(VGroup(endc, ill_e, bar6, link, p6, er6, c_ssh, c_ins, c_rest)), run_time=0.5)
        self.remove(endc, ill_e, bar6, link, p6, er6, c_ssh, c_ins, c_rest)

        # ========================================================== 7. slide 26: who needs which key
        ref7 = lref("25–26")
        md._detach(nine)
        for k, col in (("gcp", CLOUD), ("vm", CLOUD), ("disk", CLOUD), ("front", CONTAINER), ("api", CONTAINER),
                       ("vdb", CONTAINER), ("nginx", CONTAINER)):
            md.parts[k].frame.set_stroke(col)
        md.parts["door80"].plate.set_stroke(ROUTE)
        mlink = DashedLine(md.p(-0.7, 0.62), md.p(0.36, 0.62), color=S.GREY, stroke_width=3)
        spots = [md.parts["push"].point_from_proportion(0.55), md.parts["pull"].get_center(), md.p(0.55, 0.62)]
        circles = [num_circle(i + 1).move_to(p) for i, p in enumerate(spots)]
        b1 = bubble(1, "deploy", "create VM, SSH").move_to([-6.55, -0.5, 0], aligned_edge=UL)
        b2 = bubble(2, "service", "read images").move_to([-6.55, -1.66, 0], aligned_edge=UL)
        b3 = bubble(3, "service", "read models").move_to([-1.35, 2.15, 0])
        for b in (b1, b2):
            pa = md.parts["push"]
            for a in np.linspace(0, 1, 41):
                q = pa.point_from_proportion(a)
                if b.get_bottom()[1] - 0.05 < q[1] < b.get_top()[1] + 0.05:
                    assert q[0] > b.get_right()[0] + 0.08, ("push arrow touches a bubble", q, b.get_right())
        assert b2.get_top()[1] < b1.get_bottom()[1] - 0.1, (b2.get_top(), b1.get_bottom())
        assert b3.get_left()[0] > md.parts["laptop"].frame.get_right()[0] + 0.1
        assert b3.get_bottom()[1] > md.parts["gcp"].frame.get_top()[1] + 0.05, b3.get_bottom()
        assert b3.get_top()[1] < ref7.get_bottom()[1] - 0.1
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeIn(md), FadeIn(ref7), run_time=0.6)
            md.show(self, mlink, anims=[Create(mlink)], run_time=0.4)
            vo.wait_until("deployment creates the VM and logs in")
            md.show(self, circles[0], b1, anims=[GrowFromCenter(circles[0]), FadeIn(b1, shift=RIGHT * 0.15)],
                    run_time=0.6)
            vo.wait_until("the narrow key reads images")
            md.show(self, circles[1], b2, anims=[GrowFromCenter(circles[1]), FadeIn(b2, shift=RIGHT * 0.15)],
                    run_time=0.6)
            vo.wait_until("and models")
            md.show(self, circles[2], b3, anims=[GrowFromCenter(circles[2]), FadeIn(b3, shift=DOWN * 0.15)],
                    run_time=0.6)

        # ========================================================== 8. ponder: which key for the VM?
        kd = key_icon("deploy").move_to([2.4, 2.15, 0])
        ks = key_icon("service").move_to([4.9, 2.15, 0])
        assert kd.get_top()[1] < ref7.get_bottom()[1] - 0.05 and ks.get_right()[0] < 6.5
        assert kd.get_bottom()[1] > md.parts["gcp"].frame.get_top()[1] + 0.03, kd.get_bottom()
        assert kd.get_left()[0] > b3.get_right()[0] + 0.1, (kd.get_left(), b3.get_right())
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeIn(kd, shift=DOWN * 0.2), FadeIn(ks, shift=DOWN * 0.2), run_time=0.6)
            self.play(kd.animate.set_opacity(0.45), ks.animate.set_opacity(0.45), run_time=0.4)
            vo.wait_until("Which would you hand the VM")
            self.play(Indicate(md.parts["vm"].frame, color=TURN, scale_factor=1.02), run_time=0.7)
            md.heal(self)
        pc = ponder(self, "The running app needs one key.\nWhich would you hand the VM,\nand why not the other?", 8,
                    center=(1.4, -0.95), width=9.0)
        assert pc.get_left()[0] > b1.get_right()[0] + 0.1, (pc.get_left(), b1.get_right())
        assert pc.get_top()[1] < kd.get_bottom()[1] - 0.05, (pc.get_top(), kd.get_bottom())

        # ========================================================== 9. the narrow key goes on the VM
        on_vm = md.p(1.95, 0.4)
        home = np.array([-5.15, -3.17, 0])
        red_t = VGroup(label("creates VMs,", 20, INK), label("disks, buckets", 20, INK)).arrange(DOWN, buff=0.06)
        red = VGroup(RoundedRectangle(width=red_t.width + 0.4, height=red_t.height + 0.24, corner_radius=0.12,
                                      stroke_color=ERR, stroke_width=3).set_fill(tint(ERR, 0.14), 1), red_t)
        red_t.move_to(red[0])
        red.box, red.text = red[0], red_t
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            self.play(ks.animate.set_opacity(1).move_to(on_vm), run_time=0.8)
            self.remove(ks)
            md.add(ks)                               # on the VM: part of the picture (heal keeps it on top)
            md.heal(self)
            self.play(Indicate(ks.glyph, color=OWN, scale_factor=1.2), run_time=0.6)
            assert ks.get_bottom()[1] > md.parts["front"].frame.get_top()[1] + 0.02, ks.get_bottom()
            assert ks.get_top()[1] < md.parts["vm"].title.get_bottom()[1] + 0.02, ks.get_top()
            vo.wait_until("it cannot create VMs")
            self.play(kd.animate.set_opacity(1), run_time=0.3)
            red.next_to(kd, RIGHT, buff=0.3)
            assert red.get_right()[0] < 6.5, red.get_right()
            self.play(FadeIn(red, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("Deployment can")
            self.play(Indicate(red.text, color=ERR, scale_factor=1.08), run_time=0.6)
            vo.wait_until("which a compromised VM should never hold")
            self.play(kd.animate.move_to(home), red.animate.move_to(home).set_opacity(0), run_time=1.0)
            self.remove(red)
            assert kd.get_top()[1] < b2.get_bottom()[1] - 0.1 and kd.get_bottom()[1] > -3.55, kd.get_top()

        # ========================================================== 10. two footnotes
        c2 = circles[1]
        gy = kd.glyph.get_center()[1]
        reg = md.parts["registry"].frame
        pts = [np.array([kd.glyph.get_right()[0] + 0.12, gy, 0]), np.array([reg.get_left()[0] - 0.4, gy, 0]),
               np.array([reg.get_left()[0] - 0.4, -3.15, 0]), np.array([c2.get_center()[0], -3.15, 0])]
        assert gy < reg.get_bottom()[1] + 0.2 and -3.15 < reg.get_bottom()[1] - 0.1, (gy, reg.get_bottom())
        a_pull = VGroup(*[Line(a, b, color=ROUTE, stroke_width=4) for a, b in zip(pts[:-1], pts[1:])],
                        route(pts[-1], c2.get_bottom() + DOWN * 0.03))
        cap10 = label("Pulumi pulls with your deployment credentials", 20, ROUTE)
        cap10.move_to([-6.4, 3.15, 0], aligned_edge=LEFT)
        badge_t = label("deployment@…", 20, CLOUD)
        badge = VGroup(RoundedRectangle(width=badge_t.width + 0.4, height=0.42, corner_radius=0.1, stroke_color=ERR,
                                        stroke_width=3).set_fill(tint(CLOUD, 0.2), 1), badge_t)
        badge_t.move_to(badge[0])
        badge.move_to([2.35, 2.05, 0])
        fence = ring(badge, S.GREY, buff=0.14, dashed=True)
        sc_l = label("scopes", 20, S.GREY).next_to(fence, LEFT, buff=0.15)
        tie = Line(badge.get_bottom() + DOWN * 0.14, [badge.get_center()[0], md.parts["vm"].frame.get_top()[1], 0],
                   color=S.GREY, stroke_width=3)
        vx = VGroup(RoundedRectangle(width=1.9, height=0.55, corner_radius=0.1, stroke_color=CLOUD,
                                     stroke_width=3).set_fill(tint(CLOUD, 0.15), 1))
        vx.add(label("Vertex AI", 20, INK).move_to(vx[0]))
        vx.move_to([5.3, 2.15, 0])
        api_fr = md.parts["api"].frame
        a_vx = route(np.array([5.72, api_fr.get_top()[1], 0]), np.array([5.72, vx.get_bottom()[1], 0]))
        gk = key_icon("service", name=False, key_w=0.55).move_to([6.15, 1.0, 0])
        repo = grey_chip("this repo: the VM runs as deployment · try the narrow one → exercises")
        repo.move_to([-6.4, 3.15, 0], aligned_edge=LEFT)
        assert repo.get_right()[0] < ref7.get_left()[0] - 0.15, repo.get_right()
        assert cap10.get_right()[0] < ref7.get_left()[0] - 0.15
        assert sc_l.get_left()[0] > b3.get_right()[0] + 0.05, (sc_l.get_left(), b3.get_right())
        assert vx.get_left()[0] > fence.get_right()[0] + 0.15, (vx.get_left(), fence.get_right())
        assert md.parts["nginx"].frame.get_right()[0] < 5.6 and md.parts["door80"].get_right()[0] < 5.6
        with self.voiceover(SAY[10]) as vo:
            vo.wait_until("This repository pulls the images")
            self.play(Succession(*[Create(m) for m in a_pull[:-1]], GrowArrow(a_pull[-1]), run_time=1.0),
                      FadeIn(cap10, shift=DOWN * 0.1), run_time=1.0)
            self.play(Indicate(c2, color=ROUTE, scale_factor=1.25), Indicate(b2.frame.frame, color=ROUTE, scale_factor=1.0),
                      run_time=0.6)
            md.heal(self)
            vo.wait_until("and runs the VM itself as deployment")
            self.play(FadeIn(badge, shift=DOWN * 0.15), Create(tie), run_time=0.6)
            vo.wait_until("capped only by scopes")
            self.play(Create(fence), FadeIn(sc_l), run_time=0.6)
            vo.wait_until("And the API calls Vertex AI")
            self.play(FadeIn(vx), GrowArrow(a_vx), run_time=0.6)
            self.play(FadeIn(gk, scale=1.3), run_time=0.4)
            vo.wait_until("Try the narrow one")
            self.play(ReplacementTransform(cap10, repo), run_time=0.6)
            self.play(Indicate(ks.glyph, color=OWN, scale_factor=1.2), run_time=0.6)
        gone10 = VGroup(md, kd, a_pull, badge, fence, sc_l, tie, vx, a_vx, gk)

        # ========================================================== 11. slide 27: test the app
        ref11 = lref("27")
        title = label("Test the App", 30, INK).move_to([-6.4, 3.15, 0], aligned_edge=LEFT)
        bw = Browser(f"http://{IP_PH}/", win_w=4.7, win_h=3.6)
        bw.move_to([-6.45 + 2.35, 0.2, 0])
        ill11 = illustration_tag().next_to(bw.frame, DOWN, buff=0.15).align_to(bw.frame, LEFT)
        hero = RoundedRectangle(width=3.8, height=0.8, corner_radius=0.08, stroke_color=S.GREY,
                                stroke_width=2).set_fill(S.GREY_DARKER, 1)
        fv, av = label("Frontend version", 20, S.GREY), label("API version", 20, TURN)
        foot = VGroup(fv, av).arrange(RIGHT, buff=0.3)
        page = [label("Formaggio", 24, INK), hero, foot]
        pr = ProxyRoute(gates=True)
        pr.shift(RIGHT * 3.3 + DOWN * 0.1)
        st = route_chip("from /status")
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(VGroup(gone10, repo)), ReplacementTransform(ref7, ref11), run_time=0.5)
            self.remove(gone10, repo)
            self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.4)
            self.play(FadeIn(bw), FadeIn(ill11), run_time=0.5)
            assert bw.frame.get_right()[0] < pr.get_left()[0] - 0.1, (bw.frame.get_right(), pr.get_left())
            assert pr.get_top()[1] < title.get_bottom()[1] - 0.05 and pr.get_right()[0] < 6.5, pr.get_right()
            vo.wait_until("Open your instance IP")
            self.play(Indicate(bw.address, color=ROUTE, scale_factor=1.06), run_time=0.5)
            bw.heal(self)
            bw.fill(self, page, buff=0.25)
            st.next_to(bw.frame, DOWN, buff=0.15).align_to(bw.frame, RIGHT)
            assert st.get_left()[0] > ill11.get_right()[0] + 0.1, (st.get_left(), ill11.get_right())
            self.play(FadeIn(pr), run_time=0.5)
            vo.wait_until("the footer shows the API version")
            self.play(Indicate(av, color=TURN, scale_factor=1.12), FadeIn(st, shift=UP * 0.1), run_time=0.6)
            bw.heal(self)
            pr.enter(self, "/api-service/status", run_time=0.7)
            pr.match(self, "api", run_time=0.5)
            pr.snip(self, run_time=0.7)
            pr.arrive(self, run_time=0.5)
            self.play(*[Indicate(pr.gates[p], color=ERR, scale_factor=1.08) for p in ("3000", "9000")], run_time=0.6)
            pr.heal(self)
        self.play(FadeOut(VGroup(bw, ill11, st, pr, title, ref11)), run_time=0.5)
        self.remove(bw, ill11, st, pr, title, ref11)

        # ========================================================== 12. on the VM: list, follow the logs
        trk = tracker_p(13)
        t = vm_term(10)
        stand = under_term(t, grey_chip("our part 1 stand-in · same names except vector-db"))
        root = under_term(t, grey_chip("uvicorn logs the path with --root-path /api-service added back (vm/37:20)"))
        assert stand.get_top()[1] < TRACK_BOTTOM - 0.05 and root.get_left()[0] > -6.55, root.get_left()
        with self.voiceover(SAY[12]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t, shift=UP * 0.3), run_time=0.6)
            self.play(FadeIn(stand, shift=DOWN * 0.1), run_time=0.4)
            type_capture(self, t, V52, type_time=0.8)
            rows = out(self, t, PS_ROWS, run_time=0.5)
            for r in rows:
                substring(r, "…").set_color(S.GREY)
            vdb = substring(rows[-1], C_VDB)
            self.play(vdb.animate.set_color(TURN), run_time=0.3)
            self.add(t)
            gh = row_tag("Pulumi: vector-db", S.GREY)
            pin(self, rows[-1], beside(gh, rows[-1], buff=0.3), run_time=0.3)
            vo.wait_until("follow each log")
            type_capture(self, t, V53, type_time=0.3)
            out(self, t, V53.at(2, "…", 26, "…", 53), wrap=True, run_time=0.4)
            r54 = [r for r in out(self, t, V53.at((54, 56)), wrap=True, run_time=0.35) if "/api-service" in r.text]
            assert len(r54) == 3
            self.play(FadeOut(stand), FadeIn(root, shift=DOWN * 0.1), run_time=0.4)
            self.remove(stand)
            self.play(*[substring(r, "/api-service").animate.set_color(ROUTE) for r in r54], run_time=0.3)
            self.add(t)
            vo.wait_until("Control C to stop")
            cc = out(self, t, [(V53.line(59), TURN)], run_time=0.25)[0]
            pin(self, cc, beside(row_tag("Control C stops following", TURN), cc, buff=0.3), run_time=0.3)
            self.play(FadeOut(root), run_time=0.3)
            self.remove(root)
            type_capture(self, t, V54, type_time=0.25)
            out(self, t, V54.at(2, (7, 8)) + [(V54.line(9), TURN)], run_time=0.35)
            type_capture(self, t, V55, type_time=0.25)
            out(self, t, V55.at(9, (10, 11)) + [(V55.line(15), TURN)], wrap=True, run_time=0.35)
            vo.wait_until("Our stand-in names the database")
            self.play(FadeIn(stand, shift=DOWN * 0.1), run_time=0.4)
            flash_tag(self, stand, INK)

        # ========================================================== 13. exec; the chat model; your turn
        note = card(["chat: GENERATIVE_MODEL in the four llm_*_utils.py files",
                     "→ a model Vertex AI lists as available",
                     "· then up in deploy_images and deploy_single_vm"], size=20)
        with self.voiceover(SAY[13]) as vo:
            self.play(FadeOut(stand), run_time=0.3)
            self.remove(stand)
            t.clear(self, run_time=0.3)
            type_capture(self, t, V56, type_time=0.35)
            for n in (2, 5):
                ln = type_at(self, t, V56, n, type_time=0.25)
                cid = at_prompt(V56, n)[0].split("@")[1].split(":")[0]
                substring(ln, cid).set_color(S.GREY_DARK)
                self.add(t)
                if n == 2:
                    out(self, t, V56.at((3, 4)), wrap=True, run_time=0.3)
            out(self, t, V56.at(6), run_time=0.2)
            t.set_prompt(P_VM)
            vo.wait_until("and into nginx")
            type_capture(self, t, V57, type_time=0.3)
            ln = type_at(self, t, V57, 2, type_time=0.2)
            substring(ln, at_prompt(V57, 2)[0].split("@")[1].split(":")[0]).set_color(S.GREY_DARK)
            self.add(t)
            vr = out(self, t, [(V57.line(3), CONTAINER)], run_time=0.25)[0]
            pin(self, vr, beside(time_row(), vr, buff=0.4), run_time=0.3)
            ln = type_at(self, t, V57, 4, type_time=0.2)
            substring(ln, at_prompt(V57, 4)[0].split("@")[1].split(":")[0]).set_color(S.GREY_DARK)
            self.add(t)
            out(self, t, V57.at(5), run_time=0.2)
            t.set_prompt(P_VM)
            vo.wait_until("One note")
            resize(self, t, 6, run_time=0.5)
            note.move_to([0, 0, 0]).align_to([-6.3, 0, 0], LEFT)
            note.move_to([note.get_center()[0], (t.box.get_top()[1] + TRACK_BOTTOM) / 2, 0])
            assert note.get_bottom()[1] > t.box.get_top()[1] + 0.05 and note.get_top()[1] < TRACK_BOTTOM - 0.05, \
                (note.get_bottom(), note.get_top(), t.box.get_top())
            self.play(FadeIn(note, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("change it in the API's helper files")
            self.play(Indicate(note.body[0], color=TURN, scale_factor=1.04), run_time=0.6)
            self.add(note)
            vo.wait_until("then run up in both projects")
            yt = on_bar(t, turn_row())
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)
        self.play(FadeOut(VGroup(t, note, yt, trk)), run_time=0.6)
        self.remove(t, note, yt, trk)
        self.wait(0.4)
