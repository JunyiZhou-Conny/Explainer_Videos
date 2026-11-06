"""S12 · Production: nginx instead of Vite (AC215 L18, part 2). Tracker [P] "README @ e98fa55 ›
Production images" (caption note "earlier README · extra") 1 → 5; every command here is extra.
Lecture tag: APIs slide 42 (beat 6 only).

Beats (script.md "## S12", one voiceover block each):
0. TRACKER [P] head and the note "earlier README · extra", no step lit until beat 3. V1 (localhost:3000, the frontend and API boxes on the GREEN cable, courier "Vite").
   On "who serves" the Vite courier is struck GREY and a "?" sits beside it; on "Nginx does" the "?"
   becomes a PURPLE "nginx" chip. V1 leaves; the README card (e98fa55 README · lines 197–201) with
   the tag "erratum · removed from today's README", and a GREY chip "files still in main:
   Dockerfile · nginx.conf.template".
1. CODE(frontend-react/Dockerfile: 3–8) and (…: 12–16) stacked (two pages, line 3's platform flag
   elided, line 14 cut): stage 1 PURPLE bars (npm ci, npm run build) with a PURPLE "Node" chip;
   stage 2 TEAL bars (FROM nginx, COPY --from=build) with a TEAL "nginx image" chip; a GREEN
   "dist/" folder rides an arrow from Node to nginx; the Node chip dims.
2. CODE(nginx.conf.template: 11–19) (comments cut): lines 13–14 YELLOW. Right: a small frontend box
   with the "Vite" courier over the API box; on "same rule as Vite" the courier re-labels "nginx" and
   a PINK "/api/…" envelope rides down to the API. Then CODE(…: 23–32): line 31 GREEN, and the page
   addresses /newsletters, /chat → index.html (GREEN); on "only a missing asset" lines 23–26 GREY
   and "/assets/…" → a GREY "404".
3. A 10-row "laptop · new terminal" at the Vite container's prompt; TRACKER [P] 1 on "Stop the dev
   server": d02:88 (^C), d02:91 typed at its
   container prompt, d02:92. TRACKER [P] 2: at ~/cheese-app-v2/src/frontend-react it types
   `docker build -t cheese-app-frontend-react:prod .` → d20: 2, 4, …, 101, 103, 120, …, 123, 133;
   101 and 123 TEAL.
4. TRACKER [P] 3: `docker run --rm --network cheese-app-network -p 8080:80 cheese-app-frontend-react:prod`
   (folds) → d21: 8 (wrapped, YELLOW, chip "API_URL filled in"), 12 (row tag "at the time of
   recording"). The terminal shrinks to 3 rows at the top; TRACKER [P] 4: a 7-row "second tab"
   types d22:1 → 2–6 (wrapped; `Server: nginx/1.31.8` PURPLE), d23:1 → 2–4 (wrapped), d25:1 → 2–4
   (the two `200 text/html` GREEN, `/assets/ 404` GREY).
5. TRACKER [P] 5. The run terminal leaves; the tab becomes a 3-row strip: d27:1 → 2–3. Two bars grow
   over it: dev 331MB (TEAL with a PURPLE "Node" band) and prod 94.8MB (TEAL, thin); a chip
   "no Node, no Vite · files and one proxy rule".
6. LECTURE 18 · 42 (APIs). V1 production: the address becomes localhost:8080, door 3000 → 8080,
   :5173 → :80, frontend-react → frontend-react:prod, the courier Vite → nginx; YELLOW dashed rings
   round the outside, GREEN ring "unchanged" round the API; a GREY chip "slide 42: a domain on 443 ·
   Lecture 20: NGINX in front on a VM, port 80"; the API door and uvicorn pulse GREEN.
7. LECTURE off. A 3-row "laptop · new terminal" strip (tag extra on its bar): d21:27–28; the prod box
   goes dark. The strip becomes the API's "laptop" terminal: b21:613, 620 typed at its container
   prompt, 621; the API box goes dark; a GREY chip "the pytest shell: exit too". The prod box comes
   back alone on the cable, about to start. PONDER (6 s).
8. The card leaves; the browser goes and the laptop slides left. The strip (new terminal) types
   e01:1 (extra) → e01: 11 (from "[emerg]", wrapped, RED; line 8 left out: it would scroll the
   command away); the prod box flashes RED. Before it types, the tracker leaves (beat 8 is extra), the
   picture rises 0.6 into its place and the strip grows to 5 rows: command and error stay together.
   CODE(nginx.conf.template: 14) top right, `proxy_pass ${API_URL};` RED; the API's stub leaves the
   cable; the nginx courier sends "cheese-app-api-service ?" to the network's phone book (only
   cheese-app-vector-db in it): RED "not found". A GREEN chip "start the API first". Fade; empty
   frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S12"]

# ------------------------------------------------------------------ the real sources (checked)
D02 = capture("d02")
D20 = capture("d20")
D21 = capture("d21")
D22 = capture("d22")
D23 = capture("d23")
D25 = capture("d25")
D27 = capture("d27")
E01 = capture("e01")
B21 = capture("b21")

assert D02.line(88) == "^C" and D02.line(92) == "exit", (D02.line(88), D02.line(92))
assert at_prompt(D02, 91)[1] == "exit"
assert D20.cmd == "docker build -t cheese-app-frontend-react:prod ."
assert D20.line(101).endswith("vite v8.3.5 building client environment for production..."), D20.line(101)
assert D20.line(120).endswith("✓ built in 800ms") and D20.line(123).startswith("#14 [stage-1 3/3] COPY --from=build")
assert D20.line(133).endswith("naming to docker.io/library/cheese-app-frontend-react:prod done")
assert D21.cmd == "docker run --rm --network cheese-app-network -p 8080:80 cheese-app-frontend-react:prod"
assert "Running envsubst on" in D21.line(8) and D21.line(12).endswith("nginx/1.31.8")
assert D21.line(27) == "^C" and "signal 2 (SIGINT) received, exiting" in D21.line(28)
assert D22.at((2, 4)) == ["HTTP/1.1 200 OK", "Server: nginx/1.31.8", "Content-Type: text/html"]
assert D23.at(2, 3) == ["HTTP/1.1 200 OK", "Server: nginx/1.31.8"] and '"title":"Spanish Cheese Journey"' in D23.line(4)
D25_ROWS = D25.at((2, 4))
assert [r.split() for r in D25_ROWS] == [["/newsletters", "200", "text/html"],
                                         ["/chat?model=llm-rag", "200", "text/html"],
                                         ["/assets/", "404", "text/html"]], D25_ROWS
assert "331MB" in D27.line(2) and ":latest" in D27.line(2)
assert "94.8MB" in D27.line(3) and ":prod" in D27.line(3)
assert E01.cmd == "timeout 30 docker run --rm --network cheese-app-network -p 8080:80 cheese-app-frontend-react:prod"
assert 'host not found in upstream "cheese-app-api-service"' in E01.line(11) and E01.line(11).endswith("default.conf:14")
assert B21.line(613) == "^C" and at_prompt(B21, 620)[1] == "exit" and B21.line(621) == "exit"

FR = f"{V2}/src/frontend-react"
DOCKERFILE = f"{FR}/Dockerfile"
TPL = f"{FR}/nginx.conf.template"
assert excerpt(DOCKERFILE, 6, 6) == "RUN npm ci" and excerpt(DOCKERFILE, 8, 8) == "RUN npm run build"
assert excerpt(DOCKERFILE, 12, 12) == "FROM nginx:1.31.8-alpine"
assert excerpt(DOCKERFILE, 15, 15) == "COPY --from=build /app/dist /usr/share/nginx/html"
assert excerpt(TPL, 13, 13).strip() == "location /api/ {" and excerpt(TPL, 14, 14).strip() == "proxy_pass ${API_URL};"
assert excerpt(TPL, 31, 31).strip() == "try_files $uri /index.html;"
assert excerpt(TPL, 23, 23).strip() == "location /assets/ {" and excerpt(TPL, 25, 25).strip() == "try_files $uri =404;"
README_BODY = [md_plain(readme(197, V2_E98)),
               *soft([" ".join([readme(198, V2_E98), readme(199, V2_E98)])], 58),
               *soft([md_plain(readme(201, V2_E98))], 58)]
assert README_BODY[0] == "Production images", README_BODY


# ------------------------------------------------------------------ local helpers (as in S10)
def bar_tag(scene, t: Terminal, tg):
    """PLAYS: a row-sized tag on the terminal's title bar (replacing the one there)."""
    old = getattr(t, "bar_tag", None)
    on_bar(t, tg)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    else:
        scene.play(FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    t.add(tg)
    t.bar_tag = tg
    return tg


def clear_lines(scene, t: Terminal, run_time: float = 0.3):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    if not gone:
        return
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(VGroup(*gone)), run_time=run_time)
    scene.remove(*gone)


def recolor(scene, t: Terminal, row, sub: str, color, run_time: float = 0.35):
    """PLAYS: colour `sub` inside terminal row `row` (then re-seat the terminal)."""
    scene.play(substring(row, sub).animate.set_color(color), run_time=run_time)
    scene.add(t)


def mini_pair():
    """Beat 2: a small frontend box with its courier chip ('Vite') over the API box, joined by a
    PINK arrow. .front .courier .api .arrow"""
    front = cbox(("cheese-app-", "frontend-react"), 3.9, 0.84)
    cour = courier_chip("Vite").move_to(front).align_to(front.frame, RIGHT).shift(LEFT * 0.15)
    api = cbox(("cheese-app-", "api-service"), 3.9, 0.84)
    api.next_to(front, DOWN, buff=1.0)
    arr = Arrow(front.get_bottom(), api.get_top(), buff=0.08, color=ROUTE, stroke_width=4, tip_length=0.18)
    g = VGroup(front, cour, arr, api)
    g.front, g.courier, g.api, g.arrow = front, cour, api, arr
    return g


def addr_row(path: str, target) -> VGroup:
    """Beat 2: a PINK page address, an arrow, and what nginx answers."""
    a = route_chip(path)
    ar = Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=S.GREY, stroke_width=3, tip_length=0.14)
    return VGroup(a, ar, target).arrange(RIGHT, buff=0.15)


def tracker_p_fixed(step: int | None) -> ReadmeTracker:
    """tracker_p(step) with its 'README @ e98fa55 › Production images' head put back above the dots.
    common.tracker() re-arranges the head of a 'README @ ref' tracker with VGroup.arrange(), which
    re-centres it at the origin (y 0.13, mid-frame): the head is moved back to where a plain
    tracker keeps it (the same offset over the dots as tracker_r), then the tracker is re-pinned."""
    tr = tracker_p(step)
    ref = tracker_r(1)
    off = ref.head.get_y() - ref.dots.get_y()
    tr.head.shift(UP * (tr.dots.get_y() + off - tr.head.get_y()))
    place_tracker(tr)
    assert abs((tr.head.get_y() - tr.dots.get_y()) - off) < 1e-6 and tr.get_top()[1] <= TRACK_TOP + 1e-6
    assert tr.get_bottom()[1] > TRACK_BOTTOM - 0.05, tr.get_bottom()
    if step is None:
        # no step lit yet (beats 0-2 explain the files): the caption is only the GREY note
        # 'earlier README · extra'; track(trk, 1) cross-fades it to 'step 1 of 5: Stop dev · …'
        tr.remove(tr.caption)
        tr.caption = steady(NOTES["P"], tr.size, S.GREY).next_to(tr.dots, RIGHT, buff=0.25)
        tr.add(tr.caption)
    return tr


class NginxImage(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S12"] == 9, len(SAY)

        # ========================================================== 0. who serves in production? the README card
        trk = tracker_p_fixed(None)
        tr = RequestTrace("localhost:3000", rows=("front", "api"), front="react", courier="Vite", caption=False)
        net = tr.net
        vite = net.courier
        st0 = strike(vite, S.GREY)
        q0 = label("?", 34, TURN)
        x_out = (net.frame.get_right()[0] + SAFE_X) / 2          # right of the laptop
        q0.move_to([x_out, vite.get_y(), 0])
        ng0 = tool_chip("nginx").move_to(q0)
        ar0 = Arrow(q0.get_left() + LEFT * 0.05, vite.get_right(), buff=0.1, color=S.GREY, stroke_width=3,
                    tip_length=0.14)
        assert ng0.get_left()[0] > net.frame.get_right()[0] + 0.1 and ng0.get_right()[0] < SAFE_X - 0.05, ng0.get_corner(DR)
        body0 = "\n".join(README_BODY)
        rc = readme_card((197, 201), body0, name="README.md @ e98fa55")
        rc.head[0].set_color(S.GREY)
        er0 = erratum_tag("erratum · removed from today's README")
        files0 = grey_chip("files still in main: Dockerfile · nginx.conf.template")
        rc.move_to([0, 0.3, 0])
        er0.next_to(rc.frame, UP, buff=0.12).align_to(rc.frame, RIGHT)
        files0.next_to(rc, DOWN, buff=0.45)
        assert rc.width < 2 * SAFE_X - 0.2 and rc.get_top()[1] < TRACK_BOTTOM - 0.05, (rc.width, rc.get_top())
        assert er0.get_top()[1] < TRACK_BOTTOM - 0.05 or er0.get_left()[0] > trk.get_right()[0] + 0.2, \
            (er0.get_corner(UL), trk.get_corner(DR))
        assert files0.get_bottom()[1] > -SAFE_Y, files0.get_bottom()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(tr), run_time=0.8)
            self.play(vite.animate(rate_func=there_and_back).scale(1.15), run_time=0.6)
            tr.heal(self)
            vo.wait_until("so who serves the files")
            self.play(Create(st0), vite.animate.set_opacity(0.45), run_time=0.5)
            tr.heal(self)
            self.play(FadeIn(q0, scale=1.3), GrowArrow(ar0), run_time=0.5)
            self.play(Indicate(q0, color=TURN, scale_factor=1.25), run_time=0.6)
            vo.wait_until("Nginx does")
            self.play(ReplacementTransform(q0, ng0), run_time=0.6)
            vo.wait_until("Today's README dropped")
            self.play(FadeOut(VGroup(tr, st0, ng0, ar0)), run_time=0.5)
            self.play(FadeIn(rc, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(er0, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("but its files are still in main")
            self.play(FadeIn(files0, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(files0.text, color=OWN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("so we run the earlier")
            flash_tag(self, er0, S.GREY)
            vo.wait_until("marked extra")
            self.play(Indicate(trk.caption, color=TURN, scale_factor=1.06), run_time=0.7)
            self.add(trk)

        # ========================================================== 1. the Dockerfile: two stages
        p1a = code(DOCKERFILE, 3, 8, font_size=20, shown="frontend-react/Dockerfile",
                   elide={3: "--platform=$BUILDPLATFORM "})
        p1b = code(DOCKERFILE, 12, 16, font_size=20, shown="frontend-react/Dockerfile",
                   cuts={14: "COPY nginx.conf.template"})
        VGroup(p1a, p1b).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(p1a, p1b).align_to([-6.5, 0, 0], LEFT).align_to([0, PIC_TOP - 0.05, 0], UP)
        assert p1b.get_bottom()[1] > -SAFE_Y + 0.05, p1b.get_bottom()
        right1 = max(p1a.get_right()[0], p1b.get_right()[0])
        node1 = tool_chip("Node", mono_font=False)
        ngx1 = box_chip("nginx image", mono_font=False)
        cx1 = (right1 + SAFE_X) / 2
        node1.move_to([cx1, p1a.code.get_y(), 0])
        ngx1.move_to([cx1, p1b.code.get_y(), 0])
        assert node1.get_left()[0] > right1 + 0.3 and ngx1.get_right()[0] < SAFE_X - 0.1, (right1, ngx1.get_right())
        arr1 = Arrow(node1.get_bottom(), ngx1.get_top(), buff=0.12, color=OWN, stroke_width=4, tip_length=0.18)
        dist1 = VGroup(folder_icon(0.36, OWN), mono("dist/", 20, OWN)).arrange(RIGHT, buff=0.12)
        dist1.next_to(arr1.get_start(), RIGHT, buff=0.15).shift(DOWN * 0.3)
        dist_end = dist1.copy().next_to(arr1.get_end(), RIGHT, buff=0.15).shift(UP * 0.3)
        assert dist1.get_right()[0] < SAFE_X - 0.05, dist1.get_right()
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(rc, er0, files0)), run_time=0.5)
            self.play(FadeIn(p1a, shift=RIGHT * 0.2), FadeIn(p1b, shift=RIGHT * 0.2), run_time=0.7)
            self.play(Indicate(p1a.code.code_lines[0], color=TOOL, scale_factor=1.03),
                      Indicate(p1b.code.code_lines[0], color=CONTAINER, scale_factor=1.03), run_time=0.8)
            self.add(p1a, p1b)
            vo.wait_until("The first builds the app")
            b1 = VGroup(*[line_bar(p1a.code, k, TOOL, opacity=0.25) for k in (3, 5)])
            self.play(FadeIn(b1), FadeIn(node1, shift=LEFT * 0.15), run_time=0.6)
            self.add(p1a, b1)
            vo.wait_until("The second starts from nginx")
            b2 = VGroup(*[line_bar(p1b.code, k, CONTAINER, opacity=0.25) for k in (0, 3)])
            self.play(FadeIn(b2), FadeIn(ngx1, shift=LEFT * 0.15), run_time=0.6)
            self.add(p1b, b2)
            vo.wait_until("and copies in only the built files")
            self.play(code_span(p1b.code, 3, "--from=build").animate.set_color(OWN),
                      code_span(p1b.code, 3, "/app/dist").animate.set_color(OWN), FadeIn(dist1, shift=DOWN * 0.1),
                      run_time=0.5)
            self.add(p1b, b2)
            self.play(GrowArrow(arr1), dist1.animate.move_to(dist_end), node1.animate.set_opacity(0.35),
                      run_time=1.0)
            self.play(Indicate(ngx1, color=CONTAINER, scale_factor=1.08), run_time=0.6)

        # ========================================================== 2. nginx.conf.template: the same /api rule; pages → index.html
        p2a = code(TPL, 11, 19, font_size=20, shown="nginx.conf.template",
                   cuts={11: "# One entrance:", 12: "# A new connection per request,", 17: "120s;", 18: "5m;"},
                   dedent=True)
        p2b = code(TPL, 23, 32, font_size=20, shown="nginx.conf.template",
                   cuts={24: "add_header Cache-Control", 28: "# Everything else is a page:"}, dedent=True)
        for p in (p2a, p2b):
            p.align_to([-6.5, 0, 0], LEFT).align_to([0, PIC_TOP - 0.05, 0], UP)
            assert p.get_bottom()[1] > -SAFE_Y + 0.05, p.get_bottom()
        right2 = max(p2a.get_right()[0], p2b.get_right()[0])
        mp = mini_pair()
        mp.move_to([(right2 + SAFE_X) / 2, 0, 0]).align_to([0, PIC_TOP - 0.1, 0], UP)
        assert mp.get_left()[0] > right2 + 0.25 and mp.get_right()[0] < SAFE_X - 0.05, (right2, mp.get_right())
        env2 = envelope("/api/…", ROUTE)
        env2.move_to([mp.arrow.get_x() - env2.width / 2 - 0.15, mp.front.get_bottom()[1] - 0.06 - env2.height / 2, 0])
        env_dy = (mp.front.get_bottom()[1] - mp.api.get_top()[1]) - env2.height - 0.12
        assert env_dy > 0.1, env_dy
        ng2 = courier_chip("nginx").move_to(mp.courier).align_to(mp.front.frame, RIGHT).shift(LEFT * 0.15)
        rows2 = VGroup(addr_row("/newsletters", ok_chip("index.html", mono_font=True)),
                       addr_row("/chat", ok_chip("index.html", mono_font=True)),
                       addr_row("/assets/…", grey_chip("404", mono_font=True)))
        rows2.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rows2.next_to(mp, DOWN, buff=0.45)
        rows2.shift(RIGHT * ((right2 + SAFE_X) / 2 - rows2.get_x()))
        assert rows2.get_bottom()[1] > -SAFE_Y + 0.05 and rows2.get_right()[0] < SAFE_X - 0.05, rows2.get_corner(DR)
        assert rows2.get_left()[0] > right2 + 0.2, rows2.get_left()
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p1a, p1b, b1, b2, node1, ngx1, dist1, arr1)), run_time=0.5)
            self.play(FadeIn(p2a, shift=RIGHT * 0.2), FadeIn(mp, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("same rule as Vite")
            b3 = VGroup(*[line_bar(p2a.code, k, TURN, opacity=0.25) for k in (2, 3)])
            self.play(FadeIn(b3), run_time=0.4)
            self.add(p2a, b3)
            self.play(ReplacementTransform(mp.courier, ng2), run_time=0.6)
            mp.remove(mp.courier)
            mp.add(ng2)
            mp.courier = ng2
            self.add(mp)
            vo.wait_until("slash api goes to the API container")
            self.play(code_span(p2a.code, 3, "${API_URL}").animate.set_color(ROUTE), FadeIn(env2), run_time=0.4)
            self.add(p2a, b3)
            self.play(env2.animate.shift(DOWN * env_dy),
                      Indicate(mp.arrow, color=ROUTE, scale_factor=1.05), run_time=0.8)
            self.play(FadeOut(env2), Indicate(mp.api.name, color=TURN, scale_factor=1.1), run_time=0.5)
            self.add(mp)
            vo.wait_until("Any other page address")
            self.play(FadeOut(VGroup(p2a, b3)), FadeIn(p2b, shift=UP * 0.15), run_time=0.6)
            b4 = line_bar(p2b.code, 8, OWN, opacity=0.25)
            self.play(FadeIn(b4), code_span(p2b.code, 8, "/index.html").animate.set_color(OWN), run_time=0.5)
            self.add(p2b, b4)
            self.play(LaggedStart(FadeIn(rows2[0], shift=LEFT * 0.15), FadeIn(rows2[1], shift=LEFT * 0.15),
                                  lag_ratio=0.5), run_time=0.9)
            vo.wait_until("so the router can choose")
            self.play(Indicate(rows2[0][2], color=OWN, scale_factor=1.06),
                      Indicate(rows2[1][2], color=OWN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("only a missing asset")
            b5 = VGroup(*[line_bar(p2b.code, k, S.GREY, opacity=0.3) for k in range(0, 4)])
            self.play(FadeIn(b5), FadeIn(rows2[2], shift=LEFT * 0.15), run_time=0.6)
            self.add(p2b, b4, b5)
            self.play(Indicate(rows2[2][2], color=S.GREY, scale_factor=1.12), run_time=0.6)

        # ========================================================== 3. stop the dev server; docker build :prod
        t = term(container_prompt(D02, 90), rows=10, title=T_NEW, size=20)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p2b, b4, b5, mp, rows2)), run_time=0.5)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("Stop the dev server")
            self.play(track(trk, 1), run_time=0.4)
            out(self, t, D02.at(88), run_time=0.3)
            type_at(self, t, D02, 91, type_time=0.4)
            out(self, t, D02.at(92), run_time=0.3)
            t.set_prompt(P_V2_REACT)
            cd_prompt(self, t, P_V2_REACT)
            vo.wait_until("then build the production image")
            self.play(track(trk, 2), run_time=0.4)
            l3 = type_capture(self, t, D20, type_time=0.8)[0]
            pin(self, l3, beside(extra_row(), l3, buff=0.4))
            self.play(Indicate(substring(next(r for r in rows_of(l3) if ":prod" in r.text), ":prod"), color=CONTAINER, scale_factor=1.2), run_time=0.5)
            self.add(t)
            o3 = out(self, t, [*D20.at(2, 4, "…")], run_time=0.4)
            vo.wait_until("Its first stage runs")
            o3b = out(self, t, [(D20.line(101), CONTAINER), *D20.at(103, 120, "…"), (D20.line(123), CONTAINER),
                                D20.line(133)], run_time=0.8)
            self.play(Indicate(o3b[0], color=CONTAINER, scale_factor=1.03), run_time=0.6)
            self.add(t)
            self.play(Indicate(o3b[4], color=CONTAINER, scale_factor=1.03), run_time=0.6)
            self.add(t)
        del o3

        # ========================================================== 4. docker run on the network; curl 8080 (second tab)
        tab = term(P_LAPTOP, rows=7, title=T_TAB, size=20)
        api_url = row_tag("API_URL filled in", TURN)
        with self.voiceover(SAY[4]) as vo:
            self.play(track(trk, 3), run_time=0.4)
            l4 = type_capture(self, t, D21, type_time=0.9)[0]
            vo.wait_until("publishing 8080 to port 80")
            self.play(*[Indicate(g, color=ROUTE, scale_factor=1.15) for g in
                        [substring(r, "8080:80") for r in rows_of(l4) if "8080:80" in r.text]], run_time=0.6)
            self.add(t)
            o4 = out(self, t, [(D21.line(8), TURN)], wrap=True, run_time=0.4)
            o4b = out(self, t, [(D21.line(12), TOOL)], run_time=0.3)
            on_bar(t, api_url)
            self.play(FadeIn(api_url, shift=LEFT * 0.1), run_time=0.3)
            t.add(api_url)
            t.bar_tag = api_url
            pin(self, o4b[0], beside(time_row(), o4b[0], buff=0.4))
            vo.wait_until("Open localhost 8080")
            # the run terminal keeps its last 3 rows and moves to the top; the second tab opens below
            t.remove(api_url)
            self.play(FadeOut(api_url), track(trk, 4), run_time=0.3)
            t.bar_tag = None
            resize(self, t, 3, run_time=0.4)
            self.play(t.animate.shift(UP * (PIC_TOP - t.box.get_top()[1])), FadeIn(tab, shift=UP * 0.2),
                      run_time=0.5)
            assert t.box.get_bottom()[1] > tab.box.get_top()[1] + 0.2, (t.box.get_bottom(), tab.box.get_top())
            type_capture(self, tab, D22, type_time=0.7)
            bar_tag(self, tab, extra_row())
            vo.wait_until("the server is now nginx")
            o5 = out(self, tab, D22.at((2, 6)), wrap=True, run_time=0.5)
            recolor(self, tab, o5[1], "nginx/1.31.8", TOOL)
            self.play(Indicate(o5[1], color=TOOL, scale_factor=1.05), run_time=0.5)
            self.add(tab)
            vo.wait_until("slash api still reaches the API")
            clear_lines(self, tab)
            type_capture(self, tab, D23, type_time=0.8)
            o6 = out(self, tab, D23.at((2, 4)), wrap=True, run_time=0.5)
            recolor(self, tab, o6[0], "200 OK", OWN)
            vo.wait_until("and a deep link still gets the page")
            clear_lines(self, tab)
            type_capture(self, tab, D25, type_time=0.9)
            o7 = out(self, tab, D25_ROWS, run_time=0.5)
            self.play(substring(o7[0], "200 text/html").animate.set_color(OWN),
                      substring(o7[1], "200 text/html").animate.set_color(OWN),
                      substring(o7[2], "404 text/html").animate.set_color(S.GREY), run_time=0.4)
            self.add(tab)
            self.play(Indicate(substring(o7[1], "/chat?model=llm-rag"), color=OWN, scale_factor=1.1), run_time=0.6)
            self.add(tab)
        del o4

        # ========================================================== 5. compare the sizes
        L_DEV = 7.0
        L_PROD = L_DEV * 94.8 / 331
        x0 = -3.2
        y_dev, y_prod = 1.55, 0.35
        dev_bar = Rectangle(width=L_DEV, height=0.6, stroke_color=CONTAINER, stroke_width=3).set_fill(tint(CONTAINER), 1)
        dev_bar.move_to([x0 + L_DEV / 2, y_dev, 0])
        band = Rectangle(width=L_DEV - L_PROD, height=0.6, stroke_color=TOOL, stroke_width=3).set_fill(tint(TOOL, 0.3), 1)
        band.move_to([x0 + L_PROD + (L_DEV - L_PROD) / 2, y_dev, 0])
        band_t = label("Node", 20, INK).move_to(band)
        prod_bar = Rectangle(width=L_PROD, height=0.6, stroke_color=CONTAINER, stroke_width=3).set_fill(tint(CONTAINER), 1)
        prod_bar.move_to([x0 + L_PROD / 2, y_prod, 0])
        n_dev = mono(":latest · dev", 20, INK).next_to([x0, y_dev, 0], LEFT, buff=0.25)
        n_prod = mono(":prod", 20, INK).next_to([x0, y_prod, 0], LEFT, buff=0.25)
        s_dev = mono("331MB", 20, INK).next_to(dev_bar, RIGHT, buff=0.2)
        s_prod = mono("94.8MB", 20, INK).next_to(prod_bar, RIGHT, buff=0.2)
        chip5 = grey_chip("no Node, no Vite · files and one proxy rule").move_to([0.4, -0.75, 0])
        bars = VGroup(dev_bar, band, band_t, prod_bar, n_dev, n_prod, s_dev, s_prod)
        assert n_dev.get_left()[0] > -SAFE_X and s_dev.get_right()[0] < SAFE_X, (n_dev.get_left(), s_dev.get_right())
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(t), track(trk, 5), run_time=0.4)
            clear_lines(self, tab, run_time=0.25)
            # resize() moves the box and bar, not a tag on the bar: the 'extra' tag rides down with them
            ref5 = Terminal(prompt=tab.prompt, width=tab.box.width, rows=3, size=tab.size, title=tab.title.text)
            ref5.shift(UP * (tab.box.get_bottom()[1] - ref5.box.get_bottom()[1]))
            tag5 = tab.bar_tag
            dy5 = (ref5.box.get_top()[1] - tab.bar_h / 2) - tag5.get_y()
            resize(self, tab, 3, extra=[tag5.animate.shift(UP * dy5)], run_time=0.4)
            assert abs(tag5.get_y() - (tab.box.get_top()[1] - tab.bar_h / 2)) < 0.02, (tag5.get_y(), tab.box.get_top())
            assert chip5.get_bottom()[1] > tab.box.get_top()[1] + 0.1, (chip5.get_bottom(), tab.box.get_top())
            vo.wait_until("Compare the sizes")
            type_capture(self, tab, D27, type_time=0.6)
            o8 = out(self, tab, [cut(D27.line(2), "331MB"), cut(D27.line(3), "94.8MB")], run_time=0.4)
            vo.wait_until("331 megabytes")
            recolor(self, tab, o8[0], "331MB", CONTAINER)
            self.play(FadeIn(n_dev), GrowFromEdge(dev_bar, LEFT), run_time=0.7)
            self.play(FadeIn(band), FadeIn(band_t), FadeIn(s_dev), run_time=0.5)
            vo.wait_until("about 95 for production")
            recolor(self, tab, o8[1], "94.8MB", CONTAINER)
            self.play(FadeIn(n_prod), GrowFromEdge(prod_bar, LEFT), run_time=0.6)
            self.play(FadeIn(s_prod), run_time=0.3)
            vo.wait_until("No Node, no Vite")
            self.play(Indicate(band_t, color=TOOL, scale_factor=1.2), run_time=0.5)
            self.play(FadeIn(chip5, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(prod_bar, color=CONTAINER, scale_factor=1.05), run_time=0.6)

        # ========================================================== 6. LECTURE 42: only the outside changes
        ref6 = lref("42 (APIs)")             # common.lref: one slide reads 'slide 42' (top right)
        assert ref6.text.text == "Lecture18·slide42(APIs)", ref6.text.text
        tr6 = RequestTrace("localhost:3000", rows=("front", "api"), front="react", courier="Vite", caption=False)
        tr6.shift(UP * 0.75)
        n6 = tr6.net
        new_door = mono("8080", 20, INK).move_to(n6.doors["front"].text)
        new_port = mono(":80", 20, ROUTE).move_to(n6.ports["front"]).align_to(n6.ports["front"], LEFT)
        old_name = n6.boxes["front"].name[1]
        new_name = mono("frontend-react:prod", 20, INK).move_to(old_name).align_to(old_name, LEFT)
        note6 = grey_chip("slide 42: a domain on 443 · Lecture 20: NGINX in front on a VM, port 80")
        note6.move_to([0, -1.85, 0])
        assert note6.width < 2 * SAFE_X - 0.2, note6.width
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(bars, chip5)), FadeOut(tab), run_time=0.5)
            self.play(FadeIn(tr6), FadeIn(ref6), run_time=0.6)
            vo.wait_until("The lecture's production slide")
            tr6.browser.goto(self, "localhost:8080", run_time=0.4)
            n6.swap(self, n6.doors["front"].text, new_door, run_time=0.4)
            n6.swap(self, n6.ports["front"], new_port, run_time=0.3)
            n6.ports["front"] = new_port
            n6.swap(self, old_name, new_name, run_time=0.4)
            n6.set_courier(self, "nginx", run_time=0.4)
            vo.wait_until("only the outside changes")
            outer, inner, unch = tr6.outside_inside(self, run_time=0.8)
            vo.wait_until("In lecture 20")
            self.play(FadeIn(note6, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("on a cloud machine")
            self.play(Indicate(note6.text, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("on port 80")
            self.play(Indicate(n6.ports["front"], color=ROUTE, scale_factor=1.3), run_time=0.6)
            tr6.heal(self)
            vo.wait_until("the API's code and port stay the same")
            self.play(n6.door_pulse("api", OWN), Indicate(n6.inner["api"], color=OWN, scale_factor=1.15),
                      run_time=0.8)
            tr6.heal(self)
            self.play(Indicate(unch.text, color=OWN, scale_factor=1.1), run_time=0.6)
            tr6.heal(self)

        # ========================================================== 7. extra: stop it and the API; start it again? PONDER
        s7 = term(P_V2_REACT, rows=3, title=T_NEW, size=20)
        assert s7.box.get_top()[1] < tr6.get_bottom()[1] - 0.05, (s7.box.get_top(), tr6.get_bottom())
        s7b = term(container_prompt(B21, 619), rows=3, title=T_LAPTOP, size=20)
        pyt = grey_chip("the pytest shell: exit too")
        with self.voiceover(SAY[7]) as vo:
            tr6.clear_hops(self, run_time=0.4)
            self.play(FadeOut(note6), FadeOut(ref6), run_time=0.4)
            self.play(FadeIn(s7, shift=UP * 0.2), run_time=0.4)
            bar_tag(self, s7, extra_row())
            vo.wait_until("As an extra, stop it")
            out(self, s7, D21.at(27, 28), run_time=0.4)
            self.play(n6.dark("front"), run_time=0.5)
            tr6.heal(self)
            vo.wait_until("stop the API too")
            self.play(FadeOut(s7), run_time=0.25)
            self.play(FadeIn(s7b), run_time=0.25)
            out(self, s7b, B21.at(613), run_time=0.3)
            type_at(self, s7b, B21, 620, type_time=0.3)
            out(self, s7b, B21.at(621), run_time=0.3)
            self.play(n6.dark("api"), run_time=0.5)
            tr6.heal(self)
            pyt.next_to(n6.boxes["api"], DOWN, buff=0.12).align_to(n6.boxes["api"], RIGHT)
            assert pyt.get_bottom()[1] > s7b.box.get_top()[1] + 0.05, pyt.get_bottom()
            self.play(FadeIn(pyt, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and start the production container again")
            self.play(FadeOut(s7b), run_time=0.25)
            for m in list(s7.lines):          # off screen: its old rows go before it comes back
                s7.lines.remove(m)
            self.play(FadeIn(s7), run_time=0.25)
            self.play(n6.normal("front"), run_time=0.5)
            tr6.heal(self)
            self.play(n6.light("front", TURN), run_time=0.4)
            tr6.heal(self)
            vo.wait_until("It will not start")
            self.play(n6.door_pulse("front"), run_time=0.6)
            tr6.heal(self)
            vo.wait_until("So, a quick test")
            self.play(FadeOut(pyt), run_time=0.3)
            self.play(Indicate(n6.courier, color=TOOL, scale_factor=1.2), run_time=0.7)
            tr6.heal(self)
            self.play(Indicate(n6.boxes["api"].name, color=S.GREY, scale_factor=1.1), run_time=0.7)
            tr6.heal(self)
        card7 = ponder(self, "The production frontend container\nwon't start while the API is down.\n"
                             "Why would a page server care?", seconds=6, dim=0.85)   # on the set piece: veil

        # ========================================================== 8. host not found in upstream: start the API first
        p8 = code(TPL, 14, 14, font_size=20, dedent=True, shown="nginx.conf.template")
        ok8 = ok_chip("start the API first", size=22)
        # the strip grows to 5 rows so e01's 3 command rows and its 2 [emerg] rows stay on screen together:
        # the tracker (all 5 README steps done; this beat is extra) leaves and the picture rises into its
        # place, clear of the taller strip
        up8 = 0.6
        assert tr6.get_top()[1] + up8 < SAFE_Y - 0.2, tr6.get_top()
        ref8 = Terminal(prompt=s7.prompt, width=s7.box.width, rows=5, size=s7.size, title=s7.title.text)
        ref8.shift(UP * (s7.box.get_bottom()[1] - ref8.box.get_bottom()[1]))
        assert ref8.box.get_top()[1] < tr6.get_bottom()[1] + up8 - 0.1, (ref8.box.get_top(), tr6.get_bottom())
        tag8 = s7.bar_tag
        dy8 = (ref8.box.get_top()[1] - s7.bar_h / 2) - tag8.get_y()
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(card7), run_time=0.4)
            self.play(FadeOut(trk), tr6.animate.shift(UP * up8), run_time=0.4)
            tr6.heal(self)
            resize(self, s7, 5, extra=[tag8.animate.shift(UP * dy8)], run_time=0.4)
            vo.wait_until("It exits at once")
            l8 = type_capture(self, s7, E01, type_time=0.8)[0]
            pin(self, l8, beside(extra_row(), l8, buff=0.4))
            err11 = from_phrase(E01.line(11), "[emerg]")
            o9 = out(self, s7, [(err11, ERR)], wrap=True, run_time=0.5)
            self.play(n6.light("front", ERR), *[Indicate(r, color=ERR, scale_factor=1.03) for r in o9],
                      run_time=0.7)
            tr6.heal(self)
            self.add(s7)
            vo.wait_until("Nginx looks up the proxy target's name")
            # the browser leaves; the laptop slides left to make room for the config line and the phone book
            tr6.drop(self, tr6.browser, tr6.divider, run_time=0.4)
            dx = -6.45 - n6.doors["front"].get_left()[0]
            self.play(n6.animate.shift(RIGHT * dx), run_time=0.6)
            tr6.heal(self)
            x_r = n6.frame.get_right()[0] + 0.3
            p8.move_to([(x_r + SAFE_X) / 2, 0, 0]).align_to([0, n6.get_top()[1] - 0.05, 0], UP)
            assert p8.get_left()[0] > x_r - 0.01 and p8.get_right()[0] < SAFE_X - 0.05, (p8.get_left(), p8.get_right())
            self.play(FadeIn(p8, shift=LEFT * 0.15), run_time=0.4)
            self.play(code_span(p8.code, 0, "proxy_pass ${API_URL};").animate.set_color(ERR), run_time=0.4)
            self.add(p8)
            book = n6.phone_book(self, entries=((C_VDB, None),),
                                 at=((x_r + SAFE_X) / 2, p8.get_bottom()[1] - 0.25 - 0.55), run_time=0.5)
            assert book.get_left()[0] > x_r - 0.05 and book.get_right()[0] < SAFE_X - 0.05, (book.get_left(), book.get_right())
            q8 = mono(f"{C_API} ?", 20, ROUTE).next_to(book, DOWN, buff=0.15).align_to(book, LEFT)
            look = DashedLine(n6.courier.get_right() + RIGHT * 0.05, book.frame.get_left() + LEFT * 0.05, color=ROUTE,
                              stroke_width=3, dash_length=0.1).add_tip(tip_length=0.14)
            self.play(Create(look), run_time=0.6)
            self.play(FadeIn(q8, shift=DOWN * 0.1), run_time=0.4)
            self.play(n6.book_light(0, TURN), run_time=0.6)
            tr6.heal(self)
            vo.wait_until("and the API is gone")
            n6.unplug(self, "api", run_time=0.5)
            nf = err_chip("not found", mono_font=False).next_to(q8, DOWN, buff=0.12).align_to(q8, LEFT)
            assert nf.get_bottom()[1] > s7.box.get_top()[1] + 0.05, (nf.get_bottom(), s7.box.get_top())
            self.play(q8.animate.set_color(ERR), FadeIn(nf, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Start the API first")
            ok8.next_to(nf, RIGHT, buff=0.3)
            assert ok8.get_right()[0] < SAFE_X - 0.05, ok8.get_right()
            self.play(FadeIn(ok8, shift=LEFT * 0.1), run_time=0.6)
            self.play(Indicate(ok8.text, color=OWN, scale_factor=1.1), run_time=0.6)

        self.play(FadeOut(VGroup(tr6, p8, q8, nf, ok8, look)), FadeOut(s7), run_time=0.7)
        self.wait(0.3)
