"""S07 · nginx: one public door (AC215 L20). No tracker in beats 0-3; TRACKER [M] 13 (beats 4-5),
14 (beat 6), 15 (beats 7-12). Lecture: 20 · 8, 24 (beat 0 only, while V1 is on screen).

Beats (script.md "## S07", one voiceover block each):
0. lecture_ref(20, "8, 24"). V1 MasterDiagram, manual variant: laptop, Docker Hub, the VM with its
   three TEAL boxes and three PINK doors 3000, 9000, 8000 on its top wall; slide 8's stage chips with
   '4 Web server' YELLOW. A GREY browser above flips between '…:3000' and '…:9000' (one PINK arrow to
   each door). The TEAL nginx box drops in at the top of the VM, the PINK 'HTTP 80' door lands on it,
   the browser's two addresses merge into one 'http://<VM IP>/', and the request arrows draw in.
1. CODE(nginx.conf: 35–44) left; V3 ProxyRoute right. A PINK tile '/api-service/status' slides in;
   line 35 lights YELLOW as the '^~ /api-service/' signpost does, the tile moves under it, and the
   'api-service:9000' target flashes.
2. Line 37 `proxy_pass http://api-service:9000/;` YELLOW; its final '/' pulses PINK with the label
   'this one character'. V3: the scissors snip '/api-service' off the tile, which walks on to the
   target as '/status'.
3. The panel scrolls to CODE(nginx.conf: 46–55); line 47 lights, a '/' tile turns toward the '/'
   signpost, line 48 lights and the tile reaches 'frontend:3000'. A small GREEN phone book (V2) under
   the panel: 'names on cheese-app-network' with api-service and frontend glowing.
4. TRACKER [M] 13. A tall `cheese-app-vm` terminal types the README's echo block (vm/44: 1–58) as a
   fast scroll (ten rows per play, _Batch) → (no output). The terminal shrinks to a 3-row strip; a README card (README.md ·
   lines 165–167, mono, verbatim) and a small card for README:156's `echo '`. A PINK arc joins the
   outer quote to the first inner quote ('the quote closes here'); the unquoted stretch turns GREY
   ('outside quotes'), its variables shrink to nothing ('empty variables'). TRACKER [M] 13 · extra:
   the echo card and arc leave, the README card moves up and the strip grows to 6 rows (command,
   '58 …' and line 6 together); it types vm/45 (extra) → TERM(vm/45: 2, 6–8) and the card's remains
   FadeTransform onto line 6's `log_format  main   - []  $`, RED.
5. The strip grows; `sudo docker logs nginx 2>&1 | tail -6` (extra) → TERM(vm/51: 3–7) RED, with a
   GREY note above the strip 'output from after nginx runs · next step' (vm/51 was captured after
   vm/46: no container 'nginx' exists yet at this point of the README). GREY
   `erratum` tag and a GREEN fix card (no capture): `cat > conf/nginx/nginx.conf <<'EOF'` · "paste
   the README's text between the quotes" · `EOF`, each row lit on its word.
6. TRACKER [M] 14. V2 (cable, phone book, vector DB, API, frontend) over a 4-row strip that types the
   nginx `docker run` (folds) → TERM(vm/46: 2, …, 36–38); the nginx box plugs in with door 80. TRACKER
   [M] 14 · extra: V2 leaves, the strip grows (the run's output stays above), `sudo docker container
   ls` (extra) → TERM(vm/47: 2–6,
   PORTS and NAMES columns), the four PORTS cells PINK one by one.
7. TRACKER [M] 15. A GREY illustration browser at `http://<Your VM IP Address>/` with a schematic
   home page ('Formaggio' title bar, hero block, footer row); a GREY dashed chip 'VM instances ·
   External IP column' (illustration) points at the address bar. TRACKER [M] 15 · extra: the strip
   types vm/48 (extra, folds) → TERM(vm/48: 2–3, 10): 200 OK GREEN, Server: nginx, Formaggio YELLOW.
8. The strip types vm/49 (extra, folds) → TERM(vm/49: 2, 9) GREEN; V3's scissors replay small beside
   the reply (a '/api-service/' tile loses its prefix). YELLOW '▶ your turn' beside the browser.
9. The browser and strip fade. V2 at full size: four boxes, doors 8000 9000 3000 80, S04's fence with
   unlabelled gates and a YELLOW '?' at the 9000 spot; a GREY laptop outside sends a PINK arrow
   '…:9000' that stops in front of the fence. PONDER (8 s).
10. The gates get their labels (80, 443 PINK; 22 GREY, 'gate 22 · SSH (default rule)'), the tags
   http-server / https-server tie to 80 / 443; the laptop's '…:9000' bounces off the closed spot
   (RED); the VM's 9000 door pulses ('open on the VM'); GREY caption 'open on the VM · shut at the
   fence'; a knock on 80 glows GREEN and walks on to nginx.
11. The fence leaves; V2 moves up over a 4-row strip; S01's puzzle sticky returns small (top right).
   nginx's lookup arrow to the book, YELLOW boxes on the frontend and api-service lines; the frontend
   stops (GREY, its line and box erased, its route goes); TERM(vm/58: 5–6) (frontend YELLOW, nginx RED; GREY 'from the
   opening' chip, not typed); the lookup comes back with a RED '?', nginx RED, its door barred, the
   strip prints vm/58:10 RED (wrapped) and the route to api-service (and its line's box) fades RED.
12. TRACKER [M] 15 · extra: the strip types vm/59 (folds) → TERM(vm/59: 4–6, 9) with 'Up 3 seconds'
   and '-> 200' GREEN; frontend and nginx turn TEAL again and the routes reconnect. A GREY 'no restart
   policy' tag under api-service, frontend and nginx; a GREEN '--restart always · README:96' chip by
   the vector DB. Fade; empty frame.

Deviations from SHOW (and why):
- Beat 0: the VM's 'Compute Instance (VM)' title moves to the VM's bottom-left corner so the three
  wall doors fit on the top wall; the confused browser is one window whose address flips between the
  two ports (two windows did not fit above the VM).
- Beats 1-3: the code panels are drawn with tabs as two spaces and lines 36/38-41 (46-55: 49-52) cut
  with a GREY '…' (`proxy_set_header…`), so panel and ProxyRoute fit side by side (the panel holds
  the README's text otherwise unchanged). The header keeps the full path.
- Beat 4: the README card shows README:165-167 dedented by four spaces (the common indent); the outer
  `echo '` is a second small card (README:156) above it. Lines 166-167 dim with line 165 (they turn
  into whitespace and ';' too). `"$request"` shrinks with the three named variables (the shell drops
  it as well; otherwise the remains would not match line 6).
- Beat 6: vm/47's rows are 148 characters wide; the strip prints them from the PORTS column on, with a
  GREY '…' for the cropped left part (CONTAINER ID, IMAGE, COMMAND, CREATED, STATUS).
- Beat 10: the '22 · SSH (default rule)' text is a GREY note below the tags (the gate plate itself
  shows '22'; no room beside the gate next to the laptop).
- Beat 11: V2 moves up (and its 'cheese-app-vm' title sits inside the VM, bottom right) so a 4-row
  strip fits under it; the RED `[emerg] host not found in upstream "frontend"` stamp is the strip's
  own vm/58:10 line (RED), because the shared nginx_fail() puts a one-line stamp under the piece,
  where the strip is; the lookup / '?' / RED box / barred door are drawn here with the piece's parts.
  The browser arrow to the barred door is left out (the fence and outsider left with beat 10).
- Beat 12: the 'no restart policy' tag is one tag under the three boxes with a GREY bracket, and the
  README:96 note is a GREEN chip left of the VM (three tags under the boxes did not fit).
"""

import textwrap

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real sources (checked)
NGINX = "src/deployment/nginx-conf/nginx/nginx.conf"
V44, V45, V46, V47 = capture("vm/44"), capture("vm/45"), capture("vm/46"), capture("vm/47")
V48, V49, V51, V58, V59 = capture("vm/48"), capture("vm/49"), capture("vm/51"), capture("vm/58"), capture("vm/59")

assert excerpt(NGINX, 35, 35).strip() == "location ^~ /api-service/ {"
assert excerpt(NGINX, 37, 37).strip() == "proxy_pass http://api-service:9000/;"
assert excerpt(NGINX, 47, 47).strip() == "location / {"
assert excerpt(NGINX, 48, 48).strip() == "proxy_pass http://frontend:3000;"
assert len(V44.cmd_lines) == 58 and V44.cmd_lines[0] == "echo 'user  nginx;"
assert V44.cmd_lines[-1] == "' > conf/nginx/nginx.conf" and V44.lines == []
assert readme(156) == "echo 'user  nginx;" and readme(213) == "' > conf/nginx/nginx.conf"
README_LOG = textwrap.dedent(excerpt("README.md", 165, 167)).split("\n")
assert README_LOG[0].startswith("log_format  main  '$remote_addr - $remote_user [$time_local]")
assert V45.cmd.startswith("wc -l conf/nginx/nginx.conf; sed -n '7,13p'")
assert V45.line(2) == "58 conf/nginx/nginx.conf" and V45.line(6) == "    log_format  main   - []  $"
assert V45.line(7).strip() == "$" and V45.line(8).strip() == ";$"
assert V46.cmd == ("sudo docker run -d --name nginx -v $(pwd)/conf/nginx/nginx.conf:/etc/nginx/nginx.conf "
                   "-p 80:80 --network cheese-app-network nginx:stable") == readme(219)
assert V46.line(2) == "Unable to find image 'nginx:stable' locally" and V46.line(36).startswith("Digest: sha256:")
assert V46.line(37) == "Status: Downloaded newer image for nginx:stable" and re.fullmatch(r"[0-9a-f]{64}", V46.line(38))
assert V47.cmd == "sudo docker container ls" and "PORTS" in V47.line(2)
COL = V47.line(2).index("PORTS")
PORT_ROWS = [V47.line(n)[COL:] for n in range(2, 7)]
assert [r.split()[0] for r in PORT_ROWS[1:]] == ["0.0.0.0:80->80/tcp", "0.0.0.0:3000->3000/tcp",
                                                "0.0.0.0:9000->9000/tcp", "0.0.0.0:8000->8000/tcp"], PORT_ROWS
assert V48.cmd.startswith("curl -s -i http://localhost/ | head -8;")
assert V48.line(2) == "HTTP/1.1 200 OK" and V48.line(3) == "Server: nginx" and V48.line(10) == "<title>Formaggio</title>"
assert V49.cmd.startswith("curl -s -i http://localhost/api-service/; echo;")
assert V49.line(2) == "HTTP/1.1 200 OK" and V49.line(9) == '{"message":"Welcome to AC215"}'
assert V51.cmd == "sudo docker logs nginx 2>&1 | tail -6" and all(V51.line(n) == "-[]" for n in range(3, 8))
assert V58.line(5).startswith("nginx ") and "Exited (1)" in V58.line(5)
assert V58.line(6).startswith("frontend ") and "Exited (0)" in V58.line(6)
assert V58.line(10) == 'nginx: [emerg] host not found in upstream "frontend" in /etc/nginx/nginx.conf:48'
assert V59.cmd.startswith("sudo docker start frontend nginx;")
assert V59.line(4).startswith("NAMES") and V59.line(5).startswith("nginx ") and "Up 3 seconds" in V59.line(5)
assert V59.line(6).startswith("frontend ") and "Up 3 seconds" in V59.line(6)
assert V59.line(9) == "http://localhost/ -> 200"
assert readme(96).strip() == "--restart always \\"
STICKY = "The API is up.\nWhy is its address dead?"          # S01's puzzle sticky (s01_hook.STICKY)
PONDER_Q = "Port 9000 is published on the VM.\nFrom your laptop, does\nhttp://<VM IP>:9000/ answer?"

NB_UP = np.array([0.6, 0.75, 0])        # V2 over a 4-row strip (its title moved inside the VM)


# ------------------------------------------------------------------ helpers
def conf_panel(a: int, b: int, cuts: dict):
    """CODE(nginx.conf: a–b): the repo's lines, tabs drawn as two spaces, common indent removed, the
    long proxy_set_header lines cut with a GREY '…'. Header: the full path."""
    lines = textwrap.dedent(excerpt(NGINX, a, b)).expandtabs(2).split("\n")
    for n, after in cuts.items():
        lines[n - a] = cut(lines[n - a], after)
    p = code_panel("\n".join(lines), NGINX, a, "text", font_size=20)
    for n in cuts:
        code_span(p.code, n - a, "…").set_color(S.GREY)
    p.shift(np.array([-6.55 - p.code.get_left()[0], 2.3 - p.code.get_top()[1], 0]))
    return p


def wall_door(md, port: str, x: float):
    return door(port).move_to(md.p(x, 1.15))


def prebuild(nb, keys):
    """V2 with `keys` already plugged in (no animation), as S05/S06 left it."""
    for key in keys:
        b = nb._box(key)
        x = nb.SLOT_X[key]
        pl = Line(nb.p(x, -0.35), nb.p(x, -1.2), color=OWN, stroke_width=4)
        d = door(PORTS[key]).move_to(nb.p(x, 1.7))
        i = len(nb._rows)
        e = label(nb.BOOK[key], 20, INK).move_to(nb.p(2.95, nb._row_y(i)), aligned_edge=LEFT)
        nb._rows.append(key)
        nb.boxes[key], nb.plugs[key], nb.doors[key], nb.entries[key] = b, pl, d, e
        nb.add(pl, b, d, e)
    vb = nb.boxes["vdb"].frame
    c = vb.get_center()
    dots = VGroup(*[Dot(radius=0.05, color=CONTAINER).move_to(c + np.array([-0.55 + 0.1 * i, -0.36, 0]))
                    for i in range(12)])
    nb.data.add(*dots)
    nb.add(nb.data)
    nb.title.move_to(nb.p(5.55, -1.48), aligned_edge=RIGHT)


def mini_book():
    """V2's phone book, small: 'names on cheese-app-network', two entries. .entries"""
    hd = VGroup(label("names on", 20, S.GREY), mono(NETWORK, 20, OWN)).arrange(RIGHT, buff=0.15)
    es = VGroup(label(C_API, 20, INK), label(C_FRONT, 20, INK)).arrange(RIGHT, buff=0.6)
    inner = VGroup(hd, es).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    fr = RoundedRectangle(width=inner.width + 0.5, height=inner.height + 0.4, corner_radius=0.12,
                          stroke_color=OWN, stroke_width=2.5).set_fill(tint(OWN, 0.06), 1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.entries = es
    return g


class _Batch:
    """Stands in for the scene while a chunk of rows is typed: collects each row's typing play (and
    the adds that follow it) so the whole chunk types in ONE play. The fast vm/44 scroll then takes
    the same time at every frame rate (a 0.035 s play per row stretched to one frame, 0.067 s, in the
    15 fps preview and pushed the beat 2.7 s past its narration)."""

    def __init__(self, scene):
        self._s, self.anims, self.adds = scene, [], []

    def play(self, *anims, **kw):
        self.anims.extend(anims)

    def add(self, *mobs):
        self.adds.extend(mobs)

    def remove(self, *mobs):
        self._s.remove(*mobs)

    def __getattr__(self, k):
        return getattr(self._s, k)


def url_tile(prefix: str, rest: str):
    """A small PINK URL tile whose prefix can be snipped off. .bg .pre .rest"""
    full = mono(prefix + rest, 20, INK)
    pre, rst = VGroup(*full[:len(prefix)]), VGroup(*full[len(prefix):])
    bg = RoundedRectangle(width=full.width + 0.3, height=0.44, corner_radius=0.08, stroke_color=ROUTE,
                          stroke_width=3).set_fill(tint(ROUTE, 0.25), 1)
    full.move_to(bg)
    g = VGroup(bg, pre, rst)
    g.bg, g.pre, g.rest = bg, pre, rst
    return g


class OnePublicDoor(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 13, len(SAY)

        def xtag(t, ln, mob=None):
            """'extra' beside the typed line when it fits, else on the title bar. Returns a remover."""
            mob = mob or extra_row()
            beside(mob, ln)
            if mob.get_right()[0] < 6.55:
                pin(self, ln, mob)
                return lambda: unpin(self, ln, mob)
            on_bar(t, mob)
            self.play(FadeIn(mob), run_time=0.3)
            t.add(mob)                       # part of the terminal: stays above its box

            def rm():
                t.remove(mob)
                self.play(FadeOut(mob), run_time=0.25)
                self.remove(mob)
            return rm

        rm_x = lambda: None  # noqa: E731

        def glow(row, sub, color, scale=1.1, holder=None):
            g = substring(row, sub)
            self.play(g.animate.set_color(color), run_time=0.3)
            self.play(Indicate(g, color=color, scale_factor=scale), run_time=0.5)
            self.add(holder if holder is not None else t)
            return g

        # ========================================================== 0. stage 4: one address
        md = MasterDiagram(manual=True, built=("laptop", "registry", "push", "pull", "gcp", "vm", "disk",
                                               "front", "api", "vdb"))
        md.parts["vm"].title.move_to(md.p(0.78, -2.15), aligned_edge=LEFT)
        assert md.parts["vm"].title.get_right()[0] < md.parts["vdb"].frame.get_left()[0] - 0.05
        doors = {"front": wall_door(md, "3000", 1.4), "api": wall_door(md, "9000", 2.45),
                 "vdb": wall_door(md, "8000", 3.5)}
        ref = lref("8, 24")
        cb = mini_browser("http://<VM IP>:3000/").move_to(md.p(2.45, 2.15))
        alt = mini_browser("http://<VM IP>:9000/").move_to(cb)
        a3 = route(cb.get_bottom() + LEFT * 1.05, doors["front"].get_top())
        a9 = route(cb.get_bottom(), doors["api"].get_top())
        qm = label("?", 26, TURN).next_to(cb, LEFT, buff=0.15)
        assert cb.get_top()[1] < ref.get_bottom()[1] - 0.2
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(md), FadeIn(ref), run_time=0.6)
            md.show(self, *doors.values(), anims=[GrowFromCenter(d) for d in doors.values()], run_time=0.5)
            md.stage_chips(self, run_time=0.4)
            self.play(md.light_stage(4), run_time=0.4)
            self.play(FadeIn(cb, shift=DOWN * 0.2), GrowArrow(a3), run_time=0.5)
            self.play(Transform(cb, alt), ReplacementTransform(a3, a9), FadeIn(qm), run_time=0.6)
            vo.wait_until("A reverse proxy gives the browser one address")
            md.box(self, "nginx")
            md.door(self, on="nginx")
            new_b = md._make("browser", url="http://<VM IP>/")
            self.play(ReplacementTransform(cb, new_b), FadeOut(a9), FadeOut(qm), run_time=0.8)
            self.remove(new_b, a9, qm)
            md.parts["browser"] = new_b
            md.add(new_b)
            md.heal(self)
            vo.wait_until("nginx listens on port 80")
            self.play(Indicate(md.parts["door80"], color=ROUTE, scale_factor=1.2), run_time=0.6)
            md.heal(self)
            vo.wait_until("and forwards each request inside the VM")
            md.routes(self)

        # ========================================================== 1. location ^~ /api-service/
        p1 = conf_panel(35, 44, {36: "# Remove the rewrite", 38: "proxy_set_header", 39: "proxy_set_header",
                                 40: "proxy_set_header", 41: "proxy_set_header"})
        pr = ProxyRoute()
        pr.shift(RIGHT * (0.62 - pr.get_left()[0]) + DOWN * 0.5)
        assert p1.code.get_right()[0] < pr.get_left()[0] - 0.25 and pr.get_right()[0] < 6.55, \
            (p1.code.get_right(), pr.get_left(), pr.get_right())
        assert p1.header.get_bottom()[1] > pr.p(0, 1.92)[1] + 0.05
        bar35 = line_bar(p1.code, 0, TURN)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(md), FadeOut(ref), run_time=0.5)
            self.remove(md, ref)
            self.play(FadeIn(p1, shift=RIGHT * 0.2), FadeIn(pr), run_time=0.6)
            vo.wait_until("the location block on line 35")
            self.play(FadeIn(bar35), run_time=0.4)
            pr.enter(self)
            vo.wait_until("catches paths that start with slash api service")
            self.play(Indicate(code_span(p1.code, 0, "^~ /api-service/"), color=TURN, scale_factor=1.08),
                      run_time=0.5)
            self.add(p1, bar35)
            pr.match(self, "api")
            vo.wait_until("It passes them to api service on port 9000")
            self.play(pr.light_target("api"), run_time=0.7)
            pr.heal(self)

        # ========================================================== 2. one slash
        bar37 = line_bar(p1.code, 2, TURN)
        slash = code_span(p1.code, 2, "/;")[0]
        one = label("this one character", 20, ROUTE)
        one.move_to([slash.get_center()[0] - 0.15 - one.width / 2, p1.code.code_lines[3].get_center()[1], 0])
        assert one.get_left()[0] > code_span(p1.code, 3, "…").get_right()[0] + 0.25
        pointer = Arrow(one.get_right() + RIGHT * 0.02, slash.get_bottom() + DOWN * 0.03, buff=0.02,
                        color=ROUTE, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        with self.voiceover(SAY[2]) as vo:
            vo.wait_until("Look at the end of that address")
            self.play(FadeOut(bar35), FadeIn(bar37), run_time=0.4)
            vo.wait_until("one slash")
            self.play(slash.animate.set_color(ROUTE), run_time=0.2)
            self.play(Indicate(slash, color=ROUTE, scale_factor=2.0), FadeIn(one), GrowArrow(pointer),
                      run_time=0.7)
            self.add(p1, bar37, one, pointer)
            vo.wait_until("With it, nginx swaps the matched prefix for that slash")
            pr.snip(self)
            vo.wait_until("so slash api service slash status reaches the API")
            pr.arrive(self)
            self.play(Indicate(slash, color=ROUTE, scale_factor=1.8), run_time=0.6)
            self.add(p1, bar37, one, pointer)
            vo.wait_until("as just slash status")
            self.play(Indicate(pr.tile, color=ROUTE, scale_factor=1.15), pr.light_target("api"), run_time=0.8)
            pr.heal(self)

        # ========================================================== 3. location /: the frontend
        p2 = conf_panel(46, 55, {49: "proxy_set_header", 50: "proxy_set_header", 51: "proxy_set_header",
                                 52: "proxy_set_header"})
        assert p2.code.get_right()[0] < pr.get_left()[0] - 0.25
        bar47 = line_bar(p2.code, 1, TURN)
        bar48 = line_bar(p2.code, 2, TURN)
        book = mini_book()
        book.move_to([-6.55 + book.width / 2, p2.code.get_bottom()[1] - 0.25 - book.height / 2, 0])
        assert book.get_bottom()[1] > -3.55 and book.get_right()[0] < pr.get_left()[0] - 0.1
        with self.voiceover(SAY[3]) as vo:
            pr.reset(self)
            self.play(FadeOut(VGroup(p1, bar37, one, pointer), shift=UP * 0.6), FadeIn(p2, shift=UP * 0.6),
                      run_time=0.7)
            self.remove(p1, bar37, one, pointer)
            self.play(FadeIn(bar47), run_time=0.3)
            pr.enter(self, "/")
            pr.match(self, "front")
            vo.wait_until("the frontend on 3000")
            self.play(FadeOut(bar47), FadeIn(bar48), run_time=0.4)
            pr.arrive(self)
            vo.wait_until("Both targets are container names")
            self.play(FadeIn(book, shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(book.entries[0], color=OWN, scale_factor=1.15), pr.light_target("api", OWN),
                      run_time=0.7)
            self.play(Indicate(book.entries[1], color=OWN, scale_factor=1.15), pr.light_target("front", OWN),
                      run_time=0.7)
            pr.heal(self)

        # ========================================================== 4. the echo eats the log format
        trk = tracker_m(13)
        t = vm_term(13)
        assert t.box.get_top()[1] < TRACK_BOTTOM - 0.05, t.box.get_top()
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(p2, bar48, book, pr)), FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t, shift=UP * 0.2),
                      run_time=0.5)
            self.remove(p2, bar48, book, pr)
            type_cmd(self, t, V44.cmd_lines[0], type_time=0.5)
            rows = V44.cmd_lines[1:]
            per_chunk = 10
            for i in range(0, len(rows), per_chunk):
                ch = rows[i:i + per_chunk]
                room(self, t, sum(max(1, -(-len(r) // t.max_chars)) for r in ch), run_time=0.17)
                b = _Batch(self)
                for r in ch:
                    type_cmd(b, t, r, type_time=0.03, prompt=False, soft=True)
                assert len(b.anims) == sum(1 for r in ch if r.strip()), len(b.anims)   # blank rows: no play
                self.play(LaggedStart(*b.anims, lag_ratio=1.0), run_time=0.3)
                self.add(*b.adds)
            bare_prompt(self, t)
            vo.wait_until("But the file holds single quotes too")
            resize(self, t, 3, run_time=0.5)
            # the README card (165-167, verbatim) and the outer echo (156)
            log_rows = VGroup(*[mono_line(s, 20, INK) for s in README_LOG]).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.12)
            rc = readme_card((165, 167), log_rows)
            rc.move_to([0, t.box.get_top()[1] + 0.2 + rc.height / 2, 0])
            ec = readme_card(156, VGroup(mono_line(readme(156), 20, INK)))
            r0 = log_rows[0]
            i1 = README_LOG[0].index("'")
            i2 = README_LOG[0].rindex("'")
            q_close = glyph_range(r0, i1, i1 + 1)
            q_open = substring(ec.body[0], "'")
            # the outer quote sits right above the inner one: the arc is short and clears both headers
            ec.move_to([0, rc.get_top()[1] + 0.25 + ec.height / 2, 0])
            ec.shift(RIGHT * (q_close.get_center()[0] + 0.35 - q_open.get_center()[0]))
            assert rc.get_left()[0] > -6.6 and rc.get_right()[0] < 6.6, (rc.get_left(), rc.get_right())
            assert ec.get_top()[1] < TRACK_BOTTOM - 0.05 and ec.get_left()[0] > -6.55, (ec.get_top(), ec.get_left())
            self.play(FadeIn(rc, shift=UP * 0.2), FadeIn(ec, shift=UP * 0.2), run_time=0.5)
            arc = ArcBetweenPoints(q_open.get_bottom() + DOWN * 0.05, q_close.get_top() + UP * 0.05, angle=-PI / 2)
            arc.set_stroke(ROUTE, 4)
            closes = label("the quote closes here", 20, ROUTE)
            closes.next_to(ec, RIGHT, buff=0.4).align_to(ec, DOWN).shift(UP * 0.05)
            self.play(Create(arc), q_open.animate.set_color(ROUTE), q_close.animate.set_color(ROUTE), run_time=0.6)
            self.play(FadeIn(closes, shift=LEFT * 0.1), run_time=0.4)
            self.add(rc, ec, arc)
            vo.wait_until("so the shell eats the log format")
            outside = glyph_range(r0, i1 + 1, i2)
            oq = label("outside quotes", 20, S.GREY)
            oq.move_to([outside.get_center()[0], rc.head.get_center()[1], 0])
            self.play(outside.animate.set_color(S.GREY), log_rows[1].animate.set_color(S.GREY),
                      log_rows[2].animate.set_color(S.GREY), FadeIn(oq), run_time=0.5)
            empties = [substring(r0, v) for v in ("$remote_addr", "$remote_user", "$time_local", '"$request"')]
            ev = label("empty variables", 20, S.GREY).move_to(oq)
            self.play(*[g.animate.scale(0.01) for g in empties], Transform(oq, ev), run_time=0.7)
            for g in empties:
                for m in g:
                    m.set_opacity(0)
            self.add(rc, oq, arc)
            # the quote story is told: the outer-echo card and the arc leave, the README card moves up
            # and the strip grows to 6 rows, so the vm/45 command, '58 …' and line 6 share the screen
            self.play(FadeOut(VGroup(ec, arc, closes)), track(trk, 13, True), run_time=0.4)
            self.remove(ec, arc, closes)
            resize(self, t, 6, run_time=0.5,
                   extra=[VGroup(rc, oq).animate.shift(UP * (ec.get_top()[1] - rc.get_top()[1]))])
            assert rc.get_bottom()[1] > t.box.get_top()[1] + 0.1, (rc.get_bottom(), t.box.get_top())
            wc = type_capture(self, t, V45, type_time=0.35)[-1]
            rm_x = xtag(t, wc)
            o45 = out(self, t, V45.at(2, 6, 7, 8), run_time=0.4)
            assert wc in t.lines.submobjects or rows_of(wc)[0] in t.lines.submobjects   # command still on screen
            row6 = [r for r in o45 if "log_format" in r.text][0]
            vo.wait_until("and leaves a dash and two brackets")
            remains = VGroup(*substring(r0, "log_format  main  "), *substring(r0, "-"), *substring(r0, "[$time_local]")[:1],
                             *substring(r0, "[$time_local]")[-1:])
            target = substring(row6, "log_format  main   - []")
            landing = target.copy().set_color(ERR)
            # a straight fade-morph onto line 6 (TransformMatchingShapes sent a stray copy off the left edge)
            self.play(FadeTransform(remains.copy(), landing), run_time=0.8)
            target.set_color(ERR)
            self.remove(landing)
            self.add(t)

        # ========================================================== 5. useless logs; the heredoc fix
        fix_rows = [mono_line("cat > conf/nginx/nginx.conf <<'EOF'", 22, INK),
                    label("paste the README's text between the quotes", 22, INK),
                    mono_line("EOF", 22, INK)]
        fix = card(fix_rows, color=OWN)
        er = erratum_tag()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(rc, oq)), run_time=0.4)
            self.remove(rc, oq)
            rm_x()
            resize(self, t, 7, run_time=0.5)
            lg = type_capture(self, t, V51, type_time=0.5)[0]
            rm_x = xtag(t, lg)
            # vm/51 was captured after the next step's `docker run` (no container 'nginx' exists yet)
            later = under_term(t, row_tag("output from after nginx runs · next step"))
            self.play(FadeIn(later, shift=DOWN * 0.1), run_time=0.3)
            vo.wait_until("but the access logs are useless")
            out(self, t, [(s, ERR) for s in V51.at((3, 7))], run_time=0.5)
            vo.wait_until("Write it with a quoted heredoc instead")
            fix.move_to([0.3, later.get_top()[1] + 0.3 + fix.height / 2, 0])
            er.next_to(fix, LEFT, buff=0.3).align_to(fix, UP)
            assert fix.get_top()[1] < TRACK_BOTTOM - 0.05 and er.get_left()[0] > -6.55, (fix.get_top(), er.get_left())
            self.play(FadeIn(er), FadeIn(fix, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("cat, the same text")
            self.play(Indicate(fix_rows[0], color=OWN, scale_factor=1.06), run_time=0.5)
            self.play(Indicate(fix_rows[1], color=OWN, scale_factor=1.04), run_time=0.5)
            vo.wait_until("then E O F")
            self.play(Indicate(fix_rows[2], color=OWN, scale_factor=1.3), run_time=0.5)
            self.add(fix)

        # ========================================================== 6. run nginx; four containers
        nb = NamePhoneBook(built=True)
        prebuild(nb, ("vdb", "api", "front"))
        nb.shift(NB_UP)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(fix, er, later)), track(trk, 14), run_time=0.4)
            self.remove(fix, er, later)
            rm_x()
            t.clear(self, run_time=0.3)
            resize(self, t, 4, run_time=0.5)
            assert nb.vm.get_bottom()[1] > t.box.get_top()[1] + 0.05, (nb.vm.get_bottom(), t.box.get_top())
            self.play(FadeIn(nb), run_time=0.4)
            run = type_capture(self, t, V46, type_time=0.6)
            out(self, t, [V46.line(2), "…"], run_time=0.3)
            vo.wait_until("publishing port 80")
            nb.plug(self, "nginx")
            out(self, t, [(V46.crop(36, "sha256:42c68eab", "…"), S.GREY), V46.line(37), (V46.line(38), S.GREY)],
                run_time=0.4)
            vo.wait_until("The container list shows four")
            self.play(track(trk, 14, True), FadeOut(nb), run_time=0.4)
            self.remove(nb)
            resize(self, t, 7, run_time=0.4)
            ls = type_capture(self, t, V47, type_time=0.4)[0]
            rm_x = xtag(t, ls)
            tbl = out(self, t, ["…  " + r for r in PORT_ROWS], run_time=0.5)
            for r in tbl:
                substring(r, "…").set_color(S.GREY)
            for k in range(4):
                self.play(substring(tbl[k + 1], PORT_ROWS[k + 1].split()[0]).animate.set_color(ROUTE),
                          run_time=0.25)
            self.add(t)

        # ========================================================== 7. open the site
        br = Browser(f"http://{VM_IP_PH}/", win_w=6.4, win_h=2.85)
        hero = RoundedRectangle(width=4.6, height=0.8, corner_radius=0.08, stroke_color=S.GREY,
                                stroke_width=2).set_fill(S.GREY_DARKER, 1)
        foot = VGroup(*[Line(LEFT * 0.4, RIGHT * 0.4, color=S.GREY_DARK, stroke_width=4) for _ in range(4)])
        foot.arrange(RIGHT, buff=0.3)
        page = [label("Formaggio", 24, INK), hero, foot]
        ill_b = illustration_tag()
        ipc = dashed_chip("VM instances · External IP column", S.GREY)
        ill_c = illustration_tag()
        with self.voiceover(SAY[7]) as vo:
            self.play(track(trk, 15), run_time=0.4)
            rm_x()
            t.clear(self, run_time=0.3)
            resize(self, t, 6, run_time=0.5)
            br.move_to([-6.45 + br.win_w / 2, t.box.get_top()[1] + 0.2 + br.win_h / 2, 0])
            assert br.frame.get_top()[1] < TRACK_BOTTOM - 0.05, br.frame.get_top()
            ill_b.next_to(br.frame, RIGHT, buff=0.25).align_to(br.frame, DOWN)
            ipc.move_to([br.frame.get_right()[0] + 0.45 + ipc.width / 2, br.field.get_center()[1], 0])
            assert ipc.get_right()[0] < 6.55, ipc.get_right()
            ill_c.next_to(ipc, DOWN, buff=0.12).align_to(ipc, LEFT)
            point = Arrow(ipc.get_left(), br.field.get_right() + LEFT * 0.05, buff=0.05, color=S.GREY,
                          stroke_width=3, max_tip_length_to_length_ratio=0.3)
            self.play(FadeIn(br), FadeIn(ill_b), run_time=0.5)
            vo.wait_until("from the VM instances list")
            self.play(FadeIn(ipc, shift=LEFT * 0.2), FadeIn(ill_c), GrowArrow(point), run_time=0.6)
            self.play(Indicate(br.address, color=ROUTE, scale_factor=1.06), run_time=0.5)
            br.heal(self)
            vo.wait_until("and the home page appears")
            br.fill(self, page, buff=0.2)
            vo.wait_until("On the VM, curl agrees")
            self.play(track(trk, 15, True), run_time=0.3)
            cr = type_capture(self, t, V48, type_time=0.35)[-1]
            rm_x = xtag(t, cr)
            o48 = out(self, t, [(V48.line(2), OWN), V48.line(3), V48.line(10)], run_time=0.4)
            vo.wait_until("served by nginx")
            glow(o48[1], "nginx", CONTAINER)
            vo.wait_until("title Formaggio")
            glow(o48[2], "Formaggio", TURN, 1.15)

        # ========================================================== 8. /api-service/: the prefix was cut
        yt = your_turn()
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(ipc, ill_c, point)), run_time=0.3)
            self.remove(ipc, ill_c, point)
            rm_x()
            c49 = type_capture(self, t, V49, type_time=0.35)[-1]
            rm_x = xtag(t, c49)
            o49 = out(self, t, [(V49.line(2), OWN), (V49.line(9), OWN)], run_time=0.4)
            vo.wait_until("the prefix was cut on the way")
            tile = url_tile("/api-service", "/")
            tile.move_to([o49[1].get_right()[0] + 0.6 + tile.width / 2, o49[1].strut.get_center()[1], 0])
            sc = scissors(0.4).move_to([tile.pre.get_right()[0] + 0.03, tile.get_top()[1] + 0.25, 0])
            self.play(FadeIn(tile, shift=LEFT * 0.2), run_time=0.4)
            self.play(FadeIn(sc, shift=DOWN * 0.15), run_time=0.25)
            self.play(sc.animate.shift(DOWN * 0.3), run_time=0.25)
            nbg = RoundedRectangle(width=tile.rest.width + 0.3, height=0.44, corner_radius=0.08, stroke_color=ROUTE,
                                   stroke_width=3).set_fill(tint(ROUTE, 0.25), 1).move_to(tile.rest)
            self.play(VGroup(tile.bg, tile.pre).animate.shift(DOWN * 0.3 + LEFT * 0.2).set_opacity(0),
                      FadeIn(nbg), FadeOut(sc), run_time=0.6)
            self.remove(tile.bg, tile.pre, sc)
            self.remove(tile)
            snipped = VGroup(nbg, tile.rest)
            self.add(snipped)
            vo.wait_until("Pause and open your site")
            yt.next_to(br.frame, RIGHT, buff=0.3).align_to(br.frame, UP).shift(DOWN * 0.3)
            self.play(FadeIn(yt, shift=LEFT * 0.2), run_time=0.4)
            flash_tag(self, yt, TURN)

        # ========================================================== 9. ponder: port 9000 from outside?
        nb.shift(-NB_UP)
        wait9 = None
        with self.voiceover(SAY[9]) as vo:
            rm_x()
            self.play(FadeOut(VGroup(br, ill_b, yt, snipped, t)), track(trk, 15), run_time=0.5)
            self.remove(br, ill_b, yt, snipped, t)
            self.play(FadeIn(nb), run_time=0.5)
            nb.routes(self, run_time=0.6)
            nb.fence(self, labels=False)
            spot = nb.gates["closed"]
            q9 = label("?", 26, TURN).next_to(spot, RIGHT, buff=0.12)
            nb.show(self, q9, run_time=0.3)
            vo.wait_until("Port 9000 is published on the VM")
            self.play(Indicate(nb.doors["api"], color=ROUTE, scale_factor=1.25), run_time=0.7)
            nb.heal(self)
            vo.wait_until("Does it answer from your laptop")
            nb.outsider(self, "laptop")
            stop_at = spot.get_left() + LEFT * 0.45
            wa = route(nb.outside.get_right() + RIGHT * 0.05, stop_at)
            wt = mono("…:9000", 20, ROUTE).next_to(nb.outside, UP, buff=0.12)
            nb.show(self, wa, wt, anims=[GrowArrow(wa), FadeIn(wt)], run_time=0.6)
            wait9 = (wa, wt)
        pc = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 10. no: shut at the fence
        cap = label("open on the VM · shut at the fence", 22, S.GREY).move_to([0.8, -3.15, 0])
        ssh = label("gate 22 · SSH (default rule)", 20, S.GREY)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            nb.gate_labels(self)
            vo.wait_until("The two ticks opened only 80 and 443")
            nb.tags(self)
            ssh.next_to(nb.tag_chips, RIGHT, buff=0.4)
            assert ssh.get_right()[0] < 6.55, ssh.get_right()
            nb.show(self, ssh, run_time=0.4)
            vo.wait_until("no rule opens 9000")
            nb.drop(self, *wait9, q9, run_time=0.3)
            kn = nb.knock(self, "9000", text="…:9000")
            vo.wait_until("Port 9000 is open on the VM")
            self.play(Indicate(nb.doors["api"], color=ROUTE, scale_factor=1.25), run_time=0.7)
            nb.heal(self)
            vo.wait_until("but shut at the network edge")
            self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("one public door")
            nb.drop(self, kn, run_time=0.3)
            kn = nb.knock(self, "80", text="…:80")

        # ========================================================== 11. the puzzle: start-time lookup
        note_ = sticky(STICKY)
        note_.move_to([6.5 - note_.width / 2, 3.5 - note_.height / 2, 0])
        s = vm_term(4)
        fo = grey_chip("from the opening")
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(cap), track(trk, 15, True), run_time=0.3)
            self.remove(cap)
            nb.drop(self, kn, ssh, nb.fence_line, nb.tag_chips, nb.ties, nb.outside,
                    *[g for g in nb.gates.values()], run_time=0.5)
            self.play(nb.animate.shift(NB_UP), FadeIn(s, shift=UP * 0.2), FadeIn(note_, shift=LEFT * 0.3),
                      run_time=0.7)
            nb.heal(self)
            assert nb.vm.get_bottom()[1] > s.box.get_top()[1] + 0.05, (nb.vm.get_bottom(), s.box.get_top())
            assert nb.vm.get_top()[1] < note_.get_bottom()[1] - 0.05, (nb.vm.get_top(), note_.get_bottom())
            on_bar(s, fo)
            self.play(FadeIn(fo), run_time=0.3)
            vo.wait_until("The web server looks up frontend and api service once")
            nf = nb.boxes["nginx"].frame
            look = route(nf.get_right(), nb.book[0].get_left() + UP * 0.1)
            hl = {k: SurroundingRectangle(nb.entries[k], color=TURN, buff=0.06, stroke_width=3)
                  for k in ("front", "api")}
            nb.show(self, look, anims=[GrowArrow(look)], run_time=0.4)
            nb.show(self, hl["front"], anims=[Create(hl["front"])], extra=[nb.light_entry("front")], run_time=0.5)
            nb.show(self, hl["api"], anims=[Create(hl["api"])], extra=[nb.light_entry("api")], run_time=0.5)
            vo.wait_until("With the frontend stopped")
            r_front, r_api = nb.routes_g[0], nb.routes_g[1]
            nb.drop(self, r_front, hl["front"], run_time=0.3)
            nb.stop(self, "front")
            out(self, s, [(V58.line(5), OUTPUT), (V58.line(6), TURN)], run_time=0.4)
            vo.wait_until("the restart fails that lookup and exits")
            qx = label("?", 26, ERR).next_to(look, UP, buff=0.05)
            d80 = nb.doors["nginx"]
            bar = Line(d80.get_left() + LEFT * 0.05, d80.get_right() + RIGHT * 0.05, color=ERR, stroke_width=7)
            nb.show(self, qx, bar, anims=[FadeIn(qx), Create(bar)], run_time=0.5,
                    extra=[look.animate.set_color(ERR), nf.animate.set_stroke(ERR).set_fill(tint(ERR, 0.2), 1)])
            r5 = s.lines[-2]
            self.play(r5.animate.set_color(ERR), run_time=0.3)
            out(self, s, [(V58.line(10), ERR)], wrap=True, run_time=0.4)
            vo.wait_until("taking the API route with it")
            self.play(r_api.animate.set_color(ERR), hl["api"].animate.set_color(ERR), run_time=0.3)
            nb.heal(self)
            nb.drop(self, r_api, hl["api"], run_time=0.6)
            nb.routes_g = None

        # ========================================================== 12. start order; restart policy
        bracket = Line(nb.p(-2.06, -0.55), nb.p(2.44, -0.55), color=S.GREY, stroke_width=3)
        nrp = tag("no restart policy", S.GREY).move_to(nb.p(0.19, -0.82))
        ra = ok_chip("--restart always", mono_font=True)
        ra.move_to([-6.45 + ra.width / 2, nb.boxes["vdb"].get_center()[1] + 0.25, 0])
        r96 = label("README:96", 20, S.GREY).next_to(ra, DOWN, buff=0.12).align_to(ra, LEFT)
        tie = Line(ra.get_right(), nb.boxes["vdb"].frame.get_left(), color=OWN, stroke_width=3)
        assert ra.get_right()[0] < nb.vm.get_left()[0] - 0.1, (ra.get_right(), nb.vm.get_left())
        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(note_), FadeOut(fo), run_time=0.4)
            self.remove(note_, fo)
            c59 = type_capture(self, s, V59, type_time=0.35)[-1]
            rm_x = xtag(s, c59)
            nb.start(self, "front")
            vo.wait_until("then nginx")
            nb.drop(self, qx, bar, look, run_time=0.3)
            self.play(nf.animate.set_stroke(CONTAINER).set_fill(tint(CONTAINER, 0.18), 1), run_time=0.4)
            nb.heal(self)
            vo.wait_until("and the site answers 200 again")
            o59 = out(self, s, V59.at(4, 5, 6, 9), run_time=0.5)
            self.play(*[substring(r, "Up 3 seconds").animate.set_color(OWN) for r in o59[1:3]],
                      substring(o59[3], "200").animate.set_color(OWN), run_time=0.4)
            self.add(s)
            nb.routes(self, run_time=0.6)
            vo.wait_until("Start order matters")
            self.play(nb.boxes["front"].frame.animate(rate_func=there_and_back).set_stroke(TURN, 6), run_time=0.6)
            self.play(nb.boxes["nginx"].frame.animate(rate_func=there_and_back).set_stroke(TURN, 6), run_time=0.6)
            nb.heal(self)
            vo.wait_until("and so does a restart policy")
            nb.show(self, bracket, nrp, anims=[Create(bracket), FadeIn(nrp, shift=UP * 0.1)], run_time=0.5)
            vo.wait_until("which only the vector database command has")
            nb.show(self, ra, r96, tie, anims=[FadeIn(ra, shift=RIGHT * 0.2), FadeIn(r96), Create(tie)],
                    run_time=0.6)
            self.play(nb.boxes["vdb"].frame.animate(rate_func=there_and_back).set_stroke(OWN, 6), run_time=0.7)
            nb.heal(self)

        rm_x()
        self.play(FadeOut(VGroup(trk, s, nb)), run_time=0.6)
        self.remove(trk, s, nb)
        self.wait(0.3)
