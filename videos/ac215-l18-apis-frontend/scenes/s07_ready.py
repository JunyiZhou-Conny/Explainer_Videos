"""S07 · Start the API: alive, then ready (AC215 L18, part 1). Tracker [B] "README › Tutorial: Backend
APIs" 1 → 4 (4 · extra in beats 7–8). No lecture tag (script.md gives none for S07).

Beats (script.md "## S07", one voiceover block each):
0. Tracker [B] 1. A README card (README.md · lines 85–86, the README's own words in two rows) over a
   6-row `laptop · new terminal` (prompt ~/cheese-app-v2). It types `cd src/api-service` (b20, no
   output: the prompt changes); tracker [B] 2, `./docker-shell.sh`; ▶ your turn on the bar. On "The
   first build takes a while" b21:2 (PURPLE), 3 (cut, `136.2s` YELLOW), …, 24 (cut).
1. The card goes, the terminal grows to 10 rows: b21:25–28 (row tag "at the time of recording" on
   the Python line), 31–35 with `api_server` and `pytest` GREEN; the GOLD-outlined disk chip "this
   image: 4.2 GB · docker images, extra" (b46:3) above the terminal.
2. The terminal shrinks to a 3-row strip. CODE(api-service/docker-shell.sh: 16–21, line 17 cut):
   lines 16–18 YELLOW on "already runs"; under them the GREY chip "a leftover v1 API counts too ·
   docker ps · docker stop cheese-app-api-service". On "Otherwise" page 2: CODE(docker-shell.sh:
   24–33, line 29 cut) on the left and a small V5 on the right (vector-db box on the GREEN cable
   cheese-app-network); lines 26, 27, 28, 33 light on their phrases; on "publishes 9000" the API box
   comes in behind its PINK door 9000, on "joins the network" its GREEN stub draws.
3. Tracker [B] 3. At b21:37's container prompt the strip types `api_server`. CODE(api-service/
   docker-entrypoint.dev.sh: 12–16, line 13 cut after --reload): line 13 YELLOW, `api.service:app`
   PINK; under it a small V3 icon and the chip "same server, same app address". ▶ your turn on the bar.
4. Panel and icon go; the terminal grows to 9 rows: b21:39 (cut), 40, 43 GREEN at once; then 44–46
   (cut) GREY with a brace "from a background thread".
5. The terminal goes. V6 ProbeLamps at the top (API box, lamps /healthz and /readyz, CNN ring and
   vector-db box wired to the readiness lamp); CODE(api/service.py: 19–23, lines 21–22 cut) below it,
   line 22 YELLOW while the ring starts filling; on "healthz" CODE(service.py: 43–45) under the
   /healthz lamp; on "readyz" CODE(service.py: 48–53): lines 50–51 light with the ring's wire, 53
   with the Chroma wire.
6. Tracker [B] 4. Under V6: a 1-row `laptop · new terminal` strip (the uvicorn log) and a 3-row
   `laptop · second tab` strip. The tab types `curl -s -i http://localhost:9000/healthz` (extra) →
   b22:2, 8: the /healthz lamp GREEN, status 200, the log shows b21:48. Then `curl -s -i
   http://localhost:9000/readyz` (extra) → b23:2, 8 RED: the readiness lamp amber with "503 · CNN
   model is loading", the ring half full; the log scrolls b21:49–60 (503s RED).
7. Tracker [B] 4 · extra. V6 and the log step aside; the tab grows to 7 rows and types b26 → b26:13–14
   (owner columns elided), 18–20, `mobilenetv2_train_base_True.keras` GREEN. Above: a GREY laptop
   with the persistent-folder/ folder; the model file flies into it; chip "downloaded once · reused
   on every start".
8. The drawing goes; the tab (6 rows) types b25 → b25:2–5, the two `[HTTP 404]` RED. Above: a tiny
   route map from api/service.py:1–7: root `/` holding only the two probe lamps, a PINK `/api` branch
   holding everything else. In the tail the map and the tab leave, and RECORDED(expected/
   04-troubleshooting.txt: 9–10, 14), tag "recorded · README:228–229, 233", stands alone (no SAY).
9. Tracker [B] 4. Everything else goes; V6 returns frozen: /healthz GREEN, /readyz amber, the ring
   part-filled. PONDER(8 s) below it.
10. The card leaves. The strips return; the tab types the readyz curl again → b24:2, 8 GREEN, row tag
   "about 9 s later, here"; the log adds b21:61 (GREEN); the ring fills, the readiness lamp turns
   GREEN, Chroma's heartbeat pulses. The strips go; the GREY dashed thought bubble "Kubernetes
   (Lectures 19, 22) can use these": a load balancer fans PINK traffic only to the two GREEN-ready
   boxes of a small stack (not the amber one), and a restart arrow inside the box, left of the liveness
   lamp. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real sources (checked)
B20 = capture("b20")
B21 = capture("b21")
B22 = capture("b22")
B23 = capture("b23")
B24 = capture("b24")
B25 = capture("b25")
B26 = capture("b26")
B46 = capture("b46")


def body(s: str) -> str:
    """A capture's last output line with the recorder's glued '[exit N]' marker taken off (b22–b24:8
    end in '{"ok":true}[exit 0]': curl printed no newline). The marker is never shown."""
    return re.sub(r"\[exit -?\d+\]$", "", s)


def elide_mid(s: str, keep_until: str, resume_at: str) -> str:
    """The capture line with its middle replaced by the house '…' (kept: up to and including
    `keep_until`, then from `resume_at` on)."""
    i = s.index(keep_until) + len(keep_until)
    j = s.index(resume_at, i)
    return s[:i] + " … " + s[j:]


assert B20.cmd == "cd src/api-service" and B20.lines == [], B20.lines
assert B21.cmd == "./docker-shell.sh"
assert B21.line(2) == "Building cheese-app-api-service (Dockerfile.dev)..."
assert B21.line(3).startswith("[+] Building 136.2s (10/10) FINISHED")
assert "unpacking to docker.io/library/cheese-app-api-service:latest" in B21.line(24)
assert B21.at((25, 28)) == ["Container is running!!!", "Architecture: x86_64", "Python version: Python 3.13.18",
                            "UV version: uv 0.13.6 (x86_64-unknown-linux-gnu)"], B21.at((25, 28))
assert [s.strip() for s in B21.at((31, 35))] == ["The following commands are available:", "api_server",
                                                 "Run the API server: http://localhost:9000/api/docs", "pytest",
                                                 "Run the tests"], B21.at((31, 35))
assert at_prompt(B21, 37)[1] == "api_server"
assert B21.line(39).startswith("INFO:     Uvicorn running on http://0.0.0.0:9000")
assert B21.line(40) == "INFO:     Started reloader process [16] using StatReload"
assert B21.line(43) == "INFO:     Application startup complete."
assert B21.line(44).startswith("WARNING: All log messages before absl::InitializeLog()")
assert "oneDNN custom operations are on." in B21.line(45) and "cpu_feature_guard.cc:227]" in B21.line(46)
assert B21.line(48).endswith('"GET /healthz HTTP/1.1" 200 OK') and B21.line(49).endswith("200 OK")
for _n in (50, 51, 52, 53, 54, 55, 58, 59, 60):
    assert B21.line(_n).endswith('"GET /readyz HTTP/1.1" 503 Service Unavailable'), _n
assert B21.line(56).startswith("WARNING: All log messages") and "oneDNN" in B21.line(57)
assert B21.line(61).endswith('"GET /readyz HTTP/1.1" 200 OK')
assert B22.cmd == "curl -s -i http://localhost:9000/healthz" and B22.line(2) == "HTTP/1.1 200 OK"
assert body(B22.line(8)) == '{"ok":true}'
assert B23.cmd == "curl -s -i http://localhost:9000/readyz" and B23.line(2) == "HTTP/1.1 503 Service Unavailable"
assert body(B23.line(8)) == '{"detail":"CNN model is loading"}'
assert B24.cmd == B23.cmd and B24.line(2) == "HTTP/1.1 200 OK" and body(B24.line(8)) == '{"ok":true}'
assert B23.line(3).endswith("13:49:35 GMT") and B24.line(3).endswith("13:49:44 GMT")   # about 9 s
assert B25.at((2, 5)) == ['{"detail":"Not Found"}', "[HTTP 404]", '{"detail":"Not Found"}', "[HTTP 404]"]
assert B26.line(20) == "mobilenetv2_train_base_True.keras" and B26.line(19) == "data_details.json"
assert B26.line(13).endswith("experiment_1760994796") and B26.line(14).endswith("experiment_1760994796.zip")
assert B46.line(3).startswith("cheese-app-api-service:latest") and "4.2GB" in B46.line(3)

RD = f"{V2}/README.md"
README_85 = md_plain(excerpt(RD, 85, 85).strip()) + " " + md_plain(excerpt(RD, 86, 86).strip())
CARD_ROWS = README_85.split(" The first build ")
CARD_ROWS[1] = "The first build " + CARD_ROWS[1]
assert CARD_ROWS == ["1. In a new terminal, from the cheese-app-v2 folder, build and run the container.",
                     "The first build takes a few minutes, because of TensorFlow:"], CARD_ROWS

DS = f"{V2}/src/api-service/docker-shell.sh"
assert excerpt(DS, 16, 16).startswith('if docker ps --format "{{.Names}}" | grep -qx "${IMAGE_NAME}"; then')
assert excerpt(DS, 18, 18).strip() == 'docker exec -it "$IMAGE_NAME" /bin/bash'
assert excerpt(DS, 26, 26).strip() == '-v "$SECRETS_DIR":/secrets:ro \\'
assert excerpt(DS, 27, 27).strip() == '-v "$PERSISTENT_DIR":/persistent \\'
assert excerpt(DS, 28, 28).strip() == "-p 9000:9000 \\"
assert excerpt(DS, 33, 33).strip() == "--network cheese-app-network \\"
EP = f"{V2}/src/api-service/docker-entrypoint.dev.sh"
assert excerpt(EP, 13, 13).strip().startswith("uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload")
SV = f"{V2}/src/api-service/api/service.py"
assert excerpt(SV, 22, 22).strip().startswith("threading.Thread(target=llm_cnn_utils.load_cnn_model")
assert excerpt(SV, 43, 45).split("\n")[0] == '@app.get("/healthz")'
assert excerpt(SV, 50, 51) == ('    if llm_cnn_utils.cnn_model is None:\n'
                               '        raise HTTPException(503, "CNN model is loading")')
assert excerpt(SV, 53, 53).strip() == "llm_rag_utils.chroma_client().heartbeat()"
DOC = excerpt(SV, 1, 7)
assert "Everything the browser calls is under /api; the probes stay at the root." in DOC
API_LEAVES = ("newsletters", "podcasts", "llm", "llm-cnn", "llm-rag", "docs")
for _leaf in API_LEAVES:
    assert f"/api/{_leaf}" in DOC, _leaf
assert "/healthz" in DOC and "/readyz" in DOC

TROUBLE = recorded("04", 9, 10, 14)
assert TROUBLE[0].startswith("/readyz answers 503 with Chroma") and TROUBLE[2].startswith("port is already allocated")


# ------------------------------------------------------------------ local helpers (as in S06)
def mark_extra(scene, t: Terminal, line, kind=None):
    """PLAYS: the row tag 'extra' beside a typed command, or on the title bar when no room."""
    tg = beside(extra_row(kind), line, buff=0.4)
    if tg.get_right()[0] <= t.box.get_right()[0] - 0.1:
        pin(scene, line, tg)
        return tg
    return bar_tag(scene, t, extra_row(kind))


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


def clear_bar(scene, t: Terminal, *extra):
    """PLAYS: the title-bar tag (if any) leaves."""
    old = getattr(t, "bar_tag", None)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), *extra, run_time=0.3)
        t.bar_tag = None
    elif extra:
        scene.play(*extra, run_time=0.3)


def clear_lines(scene, t: Terminal, run_time: float = 0.4):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    if not gone:
        return
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(VGroup(*gone)), run_time=run_time)
    scene.remove(*gone)


def recolor(scene, row, sub: str, color, run_time: float = 0.4):
    """PLAYS: colour `sub` inside terminal row `row`."""
    scene.play(substring(row, sub).animate.set_color(color), run_time=run_time)


def log_cut(n: int, room: int = 72) -> str:
    """A uvicorn access-log line of b21 as the 1-row log strip shows it: whole when it fits, else cut
    right after its status code (the 503 lines)."""
    s = B21.line(n)
    if len(s) <= room or '" ' not in s:
        return s
    return cut(s, '" ' + s.rsplit('" ', 1)[1].split(" ")[0])


def log_line(scene, log: Terminal, item, hold: float = 0.2):
    """PLAYS: one line into the 1-row uvicorn log strip: the old line drifts up and fades while the new
    one fades in on the same row (one cross-fade), then holds briefly so each line can be read."""
    s, col = (item, OUTPUT) if isinstance(item, str) else item
    old = list(log.lines)
    for m in old:
        log.lines.remove(m)
    ln = mono_line(log._cut(s), log.size, col)
    log._place(ln, 0)
    log.lines.add(ln)
    anims = [FadeIn(ln, shift=UP * 0.12)]
    if old:
        anims.append(FadeOut(VGroup(*old), shift=UP * 0.18))
    scene.play(*anims, run_time=0.2)
    if old:
        scene.remove(*old)
    if hold > 0:
        scene.wait(hold)


def k8s_bubble(scene, pl: ProbeLamps, at=(0.0, -2.6), run_time: float = 1.0):
    """PLAYS: ProbeLamps.bubble() with the restart arrow LEFT of the liveness lamp (the shared one puts
    it above the lamp, on the box's title). Returns (bubble, restart arrow, the two traffic arrows)."""
    lb = tool_chip("load balancer", pl.size, mono_font=False)
    bxs = VGroup(*[RoundedRectangle(width=0.7, height=0.3, corner_radius=0.06, stroke_color=c,
                                    stroke_width=3).set_fill(tint(c, 0.25), 1) for c in (OWN, OWN, AMBER)])
    bxs.arrange(DOWN, buff=0.12)
    grp = VGroup(lb, bxs).arrange(RIGHT, buff=1.0)
    arrs = VGroup(*[Arrow(lb.get_right(), b.get_left(), buff=0.06, color=ROUTE, stroke_width=3,
                          tip_length=0.12, max_tip_length_to_length_ratio=0.2) for b in bxs[:2]])
    hd = label("Kubernetes (Lectures 19, 22) can use these", pl.size, S.GREY)
    content = VGroup(hd, VGroup(grp, arrs)).arrange(DOWN, buff=0.18)
    b = thought_bubble(content).move_to(pl.p(*at))
    rs = restart_glyph(0.15).next_to(pl.lamps["healthz"], LEFT, buff=0.08)
    pl.show(scene, b, rs, run_time=run_time, into=pl.marks)
    return b, rs, arrs


def mini_net():
    """Beat 2's small V5: the vector-db box on the GREEN cable; the API box, its door 9000 and its
    stub are built here but shown on their phrases. .vdb .api .door .tunnel .cable .stub_vdb .stub_api .label"""
    g = VGroup()
    vdb = cbox(("cheese-app-", "vector-db"), 2.3, 0.84).move_to([4.75, -0.35, 0])
    api = cbox(("cheese-app-", "api-service"), 2.3, 0.84).move_to([4.75, 1.15, 0])
    cx = 6.25
    cable = Line([cx, 1.5, 0], [cx, -0.7, 0], color=NET, stroke_width=6)
    stub_vdb = Line(vdb.get_right(), [cx, vdb.get_y(), 0], color=NET, stroke_width=5)
    stub_api = Line(api.get_right(), [cx, api.get_y(), 0], color=NET, stroke_width=5)
    lab = mono(NETWORK, 20, NET).next_to(vdb, DOWN, buff=0.42)
    lab.shift(RIGHT * (cx + 0.15 - lab.get_right()[0]))
    dr = door("9000").move_to([3.1, api.get_y(), 0])
    tun = Line(dr.get_right(), api.get_left(), color=ROUTE, stroke_width=4)
    g.add(cable, stub_vdb, vdb, lab)
    g.vdb, g.api, g.door, g.tunnel, g.cable, g.stub_vdb, g.stub_api, g.label = vdb, api, dr, tun, cable, stub_vdb, \
        stub_api, lab
    return g


def route_map() -> VGroup:
    """Beat 8's tiny route map (api/service.py:1–7): root '/' over the two probe lamps; a PINK '/api'
    branch over everything else. .root .lamps .api .leaves .src"""
    root = route_chip("/", 24)
    lamps = lamp_pair(("green", "amber"), buff=0.7)
    left = VGroup(root, lamps).arrange(DOWN, buff=0.35)
    api = route_chip("/api", 24)
    leaves = VGroup(*[route_chip(x, 20) for x in API_LEAVES])
    rows = VGroup(VGroup(*leaves[:3]).arrange(RIGHT, buff=0.25), VGroup(*leaves[3:]).arrange(RIGHT, buff=0.25))
    rows.arrange(DOWN, buff=0.22)
    pen = RoundedRectangle(width=rows.width + 0.4, height=rows.height + 0.3, corner_radius=0.14,
                           stroke_color=ROUTE, stroke_width=2).move_to(rows)
    right = VGroup(api, VGroup(pen, rows)).arrange(DOWN, buff=0.3)
    left.move_to([-4.2, 0, 0]).align_to([0, 2.7, 0], UP)
    right.move_to([1.3, 0, 0]).align_to([0, 2.7, 0], UP)
    ties = VGroup(*[Line(root.get_bottom(), lp.get_top() + UP * 0.02, color=S.GREY, stroke_width=2)
                    for lp in lamps.lamps])
    ties.add(Line(api.get_bottom(), pen.get_top(), color=ROUTE, stroke_width=3))
    src = grey_chip("api/service.py · lines 1–7").next_to(api, RIGHT, buff=0.45)
    assert src.get_right()[0] < SAFE_X - 0.1, src.get_right()
    g = VGroup(ties, left, right, src)
    g.root, g.lamps, g.api, g.leaves, g.src, g.ties, g.pen = root, lamps, api, leaves, src, ties, pen
    return g


class AliveAndReady(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 11, len(SAY)

        # ========================================================== 0. new terminal; cd; docker-shell.sh
        trk = tracker_b(1)
        t = term(P_V2, rows=6, title=T_NEW, size=20)
        rows0 = VGroup(*[label(s, 22, INK) for s in CARD_ROWS]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rc = readme_card((85, 86), rows0)
        rc.move_to([0, (t.box.get_top()[1] + PIC_TOP) / 2, 0])
        assert rc.get_bottom()[1] > t.box.get_top()[1] + 0.1 and rc.get_top()[1] < PIC_TOP, rc.get_top()
        assert rc.width < 2 * SAFE_X - 0.2, rc.width
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), run_time=0.5)
            self.play(FadeIn(rc, shift=UP * 0.15), FadeIn(t), run_time=0.6)
            vo.wait_until("In a new terminal")
            self.play(Indicate(rows0[0], color=TURN, scale_factor=1.03), Indicate(t.title, color=TURN), run_time=0.8)
            vo.wait_until("step 1")
            type_capture(self, t, B20, type_time=0.5)
            cd_prompt(self, t, P_V2_API)
            vo.wait_until("and run docker-shell.sh")
            self.play(track(trk, 2), run_time=0.4)
            type_capture(self, t, B21, type_time=0.4)
            vo.wait_until("The first build takes a while")
            self.play(Indicate(rows0[1], color=TURN, scale_factor=1.03), run_time=0.7)
            o0 = out(self, t, [(B21.line(2), TOOL), cut(B21.line(3), "FINISHED"), "…",
                               cut(B21.line(24), "cheese-app-api-service:latest")], run_time=0.6)
            recolor(self, o0[1], "136.2s", TURN)
            self.add(t)
            vo.wait_until("so pause and start it")
            turn0 = bar_tag(self, t, turn_row())
            flash_tag(self, turn0, TURN)
            self.add(t)

        # ========================================================== 1. the banner: two commands
        dk = disk_chip("this image: 4.2 GB · docker images, extra")
        with self.voiceover(SAY[1]) as vo:
            clear_bar(self, t, FadeOut(rc))
            resize(self, t, 10, run_time=0.5)
            o1 = out(self, t, B21.at((25, 28), (31, 35)), run_time=0.6)
            pin(self, o1[2], beside(time_row(), o1[2], buff=0.5))
            under_term(t, dk, buff=0.14)
            assert dk.get_top()[1] < TRACK_BOTTOM - 0.05, dk.get_top()
            self.play(FadeIn(dk, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("API server and pytest")
            self.play(substring(o1[5], "api_server").animate.set_color(OWN),
                      substring(o1[7], "pytest").animate.set_color(OWN), run_time=0.4)
            self.play(Indicate(substring(o1[5], "api_server"), color=OWN, scale_factor=1.1),
                      Indicate(substring(o1[7], "pytest"), color=OWN, scale_factor=1.1), run_time=0.6)
            self.add(t)

        # ========================================================== 2. what docker-shell.sh does
        p1 = code(DS, 16, 21, font_size=20, shown="api-service/docker-shell.sh", cuts={17: "is already running."})
        p2 = code(DS, 24, 33, font_size=20, shown="api-service/docker-shell.sh", dedent=True,
                  cuts={29: "GOOGLE_APPLICATION_CREDENTIALS="})
        lefty = grey_chip("a leftover v1 API counts too · docker ps · docker stop cheese-app-api-service")
        mn = mini_net()
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(dk), run_time=0.3)
            resize(self, t, 3, run_time=0.5)
            top_y = t.box.get_top()[1]
            p1.move_to([0, 0, 0]).align_to([0, PIC_TOP - 0.05, 0], UP)
            lefty.next_to(p1, DOWN, buff=0.2).align_to(p1, LEFT)
            assert lefty.get_bottom()[1] > top_y + 0.1, (lefty.get_bottom(), top_y)
            self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("if the container already runs")
            bars = VGroup(*[line_bar(p1.code, k, TURN) for k in (0, 1, 2)])
            self.play(FadeIn(bars), run_time=0.5)
            self.add(p1, bars)
            vo.wait_until("it just opens a shell")
            self.play(Indicate(code_span(p1.code, 2, 'docker exec -it "$IMAGE_NAME" /bin/bash'), color=TURN,
                               scale_factor=1.06), run_time=0.6)
            self.add(p1, bars)
            self.play(FadeIn(lefty, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Otherwise")
            p2.move_to([0, 0, 0]).align_to([-6.5, 0, 0], LEFT).align_to([0, PIC_TOP - 0.05, 0], UP)
            assert p2.get_bottom()[1] > top_y + 0.05, (p2.get_bottom(), top_y)
            assert p2.get_right()[0] < mn.door.get_left()[0] - 0.1, (p2.get_right(), mn.door.get_left())
            self.play(FadeOut(VGroup(p1, bars, lefty), shift=UP * 0.2), FadeIn(p2, shift=UP * 0.2), FadeIn(mn),
                      run_time=0.7)
            marks = VGroup()
            for k, phrase in ((2, "mounts secrets"), (3, "mounts your persistent folder"), (4, "publishes 9000"),
                              (9, "and joins the network")):
                vo.wait_until(phrase)
                b = line_bar(p2.code, k, TURN)
                marks.add(b)
                anims = [FadeIn(b)]
                if k == 4:
                    anims += [code_span(p2.code, 4, "-p 9000:9000").animate.set_color(ROUTE)]
                if k == 9:
                    anims += [code_span(p2.code, 9, "--network cheese-app-network").animate.set_color(NET)]
                self.play(*anims, run_time=0.4)
                self.add(p2, marks)
                if k == 4:
                    self.play(FadeIn(mn.api), FadeIn(mn.door), Create(mn.tunnel), run_time=0.6)
                    self.play(mn.door.animate(rate_func=there_and_back).scale(1.15), run_time=0.5)
                if k == 9:
                    self.play(Create(mn.stub_api), run_time=0.6)
                    self.play(Indicate(mn.cable, color=NET, scale_factor=1.03), Indicate(mn.label, color=NET),
                              run_time=0.6)

        # ========================================================== 3. step 2: api_server; the uvicorn line
        p3 = code(EP, 12, 16, font_size=20, shown="api-service/docker-entrypoint.dev.sh", cuts={13: "--reload"})
        icon = server_app_icon(0.9)
        same = grey_chip("same server, same app address")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p2, marks, mn, mn.api, mn.door, mn.tunnel, mn.stub_api)), track(trk, 3),
                      run_time=0.5)
            vo.wait_until("API server")
            type_at(self, t, B21, 37, type_time=0.5)
            vo.wait_until("It is almost the same uvicorn line")
            p3.move_to([0, 0, 0]).align_to([0, PIC_TOP - 0.05, 0], UP)
            row = VGroup(icon, same).arrange(RIGHT, buff=0.35).next_to(p3, DOWN, buff=0.3)
            assert row.get_bottom()[1] > t.box.get_top()[1] + 0.1, (row.get_bottom(), t.box.get_top())
            self.play(FadeIn(p3, shift=UP * 0.15), run_time=0.5)
            b3 = line_bar(p3.code, 1, TURN)
            self.play(FadeIn(b3), run_time=0.4)
            self.add(p3, b3)
            self.play(FadeIn(icon, scale=0.9), FadeIn(same, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("pointing at api dot service colon app")
            tgt = code_span(p3.code, 1, "api.service:app")
            self.play(tgt.animate.set_color(ROUTE), run_time=0.3)
            self.play(Indicate(tgt, color=ROUTE, scale_factor=1.1), run_time=0.6)
            self.add(p3, b3)
            vo.wait_until("Pause and start it")
            turn3 = bar_tag(self, t, turn_row())
            flash_tag(self, turn3, TURN)
            self.add(t)

        # ========================================================== 4. startup complete at once; TensorFlow after
        log4 = [cut(B21.line(39), "0.0.0.0:9000"), B21.line(40), (B21.line(43), OWN),
                (cut(B21.line(44), "WARNING: All log messages"), S.GREY),
                (cut(from_phrase(B21.line(45), "port.cc:153]"), "oneDNN custom operations"), S.GREY),
                (cut(from_phrase(B21.line(46), "cpu_feature_guard.cc:227]"), "TensorFlow binary"), S.GREY)]
        with self.voiceover(SAY[4]) as vo:
            clear_bar(self, t, FadeOut(VGroup(p3, b3, icon, same)))
            resize(self, t, 9, run_time=0.5)
            o4 = out(self, t, log4[:3], run_time=0.5)
            vo.wait_until("arrives at once")
            self.play(Indicate(o4[2], color=OWN, scale_factor=1.04), run_time=0.6)
            self.add(t)
            vo.wait_until("Only after it")
            o4b = out(self, t, log4[3:], run_time=0.6)
            vo.wait_until("from a background thread")
            gl = VGroup(*[r.glyphs for r in o4b])
            br = Brace(gl, RIGHT, color=S.GREY, buff=0.15)
            bt = label("from a background thread", 20, S.GREY).next_to(br, RIGHT, buff=0.15)
            if bt.get_right()[0] > t.box.get_right()[0] - 0.15:
                bt = VGroup(label("from a", 20, S.GREY), label("background thread", 20, S.GREY)).arrange(
                    DOWN, aligned_edge=LEFT, buff=0.08).next_to(br, RIGHT, buff=0.15)
            assert bt.get_right()[0] < t.box.get_right()[0] - 0.1, bt.get_right()
            self.play(GrowFromCenter(br), FadeIn(bt, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("that loads the cheese classifier")
            self.play(Indicate(bt, color=TOOL, scale_factor=1.06), run_time=0.7)

        # ========================================================== 5. the design: V6 and the two probes
        pl = ProbeLamps().shift(UP * 1.4)
        assert pl.get_top()[1] <= PIC_TOP + 0.01, pl.get_top()
        q19 = code(SV, 19, 23, font_size=20, shown="api-service/api/service.py",
                   cuts={21: "while the model loads;", 22: "load_cnn_model,"})
        q43 = code(SV, 43, 45, font_size=20, shown="api-service/api/service.py")
        q48 = code(SV, 48, 53, font_size=20, shown="api-service/api/service.py")
        for q in (q19, q43, q48):
            q.move_to([0, 0, 0]).align_to([0, pl.get_bottom()[1] - 0.15, 0], UP)
            assert q.get_bottom()[1] > -SAFE_Y + 0.05, q.get_bottom()
        q19.align_to([-6.45, 0, 0], LEFT)
        q43.align_to([-6.45, 0, 0], LEFT)
        q48.align_to([-6.45, 0, 0], LEFT)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(br, bt)), FadeOut(t), run_time=0.5)
            self.play(FadeIn(pl), run_time=0.7)
            vo.wait_until("the API answers right away")
            self.play(FadeIn(q19, shift=UP * 0.15), run_time=0.5)
            b19 = line_bar(q19.code, 3, TURN)
            self.play(FadeIn(b19), run_time=0.3)
            self.add(q19, b19)
            vo.wait_until("while the model loads")
            pl.fill_ring(self, 0.15, run_time=1.0)
            self.play(Indicate(pl.ring_label, color=TOOL, scale_factor=1.08), run_time=0.6)
            pl.heal(self)
            vo.wait_until("Two probes")
            self.play(Indicate(pl.labels["healthz"], color=TURN), Indicate(pl.labels["readyz"], color=TURN),
                      run_time=0.6)
            pl.heal(self)
            vo.wait_until("healthz and readyz")
            self.play(FadeOut(VGroup(q19, b19)), FadeIn(q43, shift=UP * 0.1),
                      pl.lamps["healthz"].animate.set_stroke(TURN), run_time=0.5)
            pl.heal(self)
            vo.wait_until("and readyz")
            self.play(FadeOut(q43), FadeIn(q48, shift=UP * 0.1), pl.lamps["healthz"].animate.set_stroke(S.GREY),
                      pl.lamps["readyz"].animate.set_stroke(TURN), run_time=0.5)
            pl.heal(self)
            b50 = VGroup(line_bar(q48.code, 2, TOOL), line_bar(q48.code, 3, TOOL))
            self.play(FadeIn(b50), pl.wire_cnn.animate.set_color(TOOL), run_time=0.5)
            self.add(q48, b50)
            pl.heal(self)
            b53 = line_bar(q48.code, 5, ROUTE)
            self.play(FadeIn(b53), pl.wire_vdb.animate.set_color(ROUTE), run_time=0.5)
            self.add(q48, b50, b53)
            pl.heal(self)
            pl.heartbeat(self, beats=1, run_time=0.8)

        # ========================================================== 6. step 3: curl the two probes
        tab = term(P_LAPTOP, rows=3, title=T_TAB, size=20)
        log = term(P_V2_API, rows=1, title=T_NEW, size=20, place=False)
        log.shift(np.array([-log.box.get_center()[0], tab.box.get_top()[1] + 0.1 - log.box.get_bottom()[1], 0]))
        assert log.box.get_top()[1] < pl.get_bottom()[1] - 0.05, (log.box.get_top(), pl.get_bottom())
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(q48, b50, b53)), pl.wire_cnn.animate.set_color(S.GREY),
                      pl.wire_vdb.animate.set_color(S.GREY), pl.lamps["readyz"].animate.set_stroke(S.GREY),
                      track(trk, 4), run_time=0.5)
            pl.heal(self)
            self.play(FadeIn(log), FadeIn(tab), run_time=0.5)
            vo.wait_until("Step 3")
            l22 = type_capture(self, tab, B22, type_time=0.6)[0]
            mark_extra(self, tab, l22)
            vo.wait_until("healthz says 200")
            o22 = out(self, tab, [(B22.line(2), OWN), body(B22.line(8))], run_time=0.4)
            pl.set(self, "healthz", "green", "200")
            log_line(self, log, (log_cut(48), OWN))
            vo.wait_until("Readyz says 503")
            l23 = type_capture(self, tab, B23, type_time=0.5)[0]
            mark_extra(self, tab, l23)
            out(self, tab, [(B23.line(2), ERR), (body(B23.line(8)), ERR)], run_time=0.4)
            pl.set(self, "readyz", "amber", "503 · CNN model is loading")
            vo.wait_until("CNN model is loading")
            pl.fill_ring(self, 0.5, run_time=1.0)
            for n in [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]:
                if n in (56, 57):
                    s = cut(B21.line(56), "WARNING: All log messages") if n == 56 else \
                        cut(from_phrase(B21.line(57), "port.cc:153]"), "oneDNN custom operations")
                    item = (s, S.GREY)
                else:
                    s = log_cut(n)
                    item = (s, ERR if '" 503' in s else OWN)
                log_line(self, log, item)
        del o22

        # ========================================================== 7. extra: the model lands in your persistent folder
        lap = RoundedRectangle(width=9.0, height=2.2, corner_radius=0.16, stroke_color=LAPTOP,
                               stroke_width=3).set_fill(S.BG, 1).move_to([-1.5, 1.62, 0])
        lap_t = label("your laptop", 20, LAPTOP).next_to(lap.get_corner(UR), DL, buff=0.12)
        fold = VGroup(folder_icon(0.45, LAPTOP), mono("persistent-folder/", 22, INK)).arrange(RIGHT, buff=0.18)
        fold.move_to(lap).align_to(lap, UL).shift(np.array([0.35, -0.3, 0]))
        model = file_card("mobilenetv2_train_base_True.keras", OWN)
        model.move_to([fold.get_left()[0] + 0.7 + model.width / 2, fold.get_y() - 0.68, 0])
        once = grey_chip("downloaded once · reused on every start")
        rst = restart_glyph(0.22, S.GREY)
        orow = VGroup(rst, once).arrange(RIGHT, buff=0.2)
        orow.move_to([0, model.get_y() - 0.6, 0]).align_to(model, LEFT)
        assert lap.get_top()[1] < PIC_TOP and orow.get_bottom()[1] > lap.get_bottom()[1] + 0.05, orow.get_bottom()
        assert model.get_right()[0] < lap.get_right()[0] - 0.1, model.get_right()
        rows26 = [elide_mid(B26.line(13), "drwxr-sr-x", "4096"), elide_mid(B26.line(14), "-rw-r--r--", "9049515"),
                  B26.line(18), B26.line(19), (B26.line(20), OWN)]
        with self.voiceover(SAY[7]) as vo:
            self.play(track(trk, 4, extra=True), FadeOut(pl), FadeOut(log), run_time=0.5)
            clear_bar(self, tab)
            clear_lines(self, tab, run_time=0.3)
            resize(self, tab, 8, run_time=0.5)
            assert tab.box.get_top()[1] < lap.get_bottom()[1] - 0.1, (tab.box.get_top(), lap.get_bottom())
            l26 = type_capture(self, tab, B26, type_time=0.7)[0]
            mark_extra(self, tab, l26)
            vo.wait_until("the model is downloaded once")
            o26 = out(self, tab, rows26, run_time=0.6)
            self.play(FadeIn(lap), FadeIn(lap_t), FadeIn(fold), run_time=0.5)
            src = model.copy().move_to(o26[-1].strut.get_center() + RIGHT * 0.6)
            self.play(Indicate(o26[-1], color=OWN, scale_factor=1.04), run_time=0.5)
            self.add(tab)
            self.play(ReplacementTransform(src, model), run_time=0.8)
            vo.wait_until("and every start reuses it")
            self.play(FadeIn(once, shift=UP * 0.1), Create(rst), run_time=0.6)
            self.play(Rotate(rst, -TAU, about_point=rst.get_center()), run_time=0.8)
            self.wait(0.8)

        # ========================================================== 8. extra: version 1 habits fail; the route map
        rmap = route_map()
        assert rmap.get_top()[1] < PIC_TOP, rmap.get_top()
        rec = quote_card("04", [9, 10, 14], kind="recorded", source="README:228–229, 233", size=20, width_chars=88)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(lap, lap_t, fold, model, once, rst)), run_time=0.4)
            clear_bar(self, tab)
            clear_lines(self, tab, run_time=0.3)
            resize(self, tab, 7, run_time=0.4)
            assert rmap.get_bottom()[1] > tab.box.get_top()[1] + 0.1, (rmap.get_bottom(), tab.box.get_top())
            vo.wait_until("the version 1 habits fail")
            l25 = type_capture(self, tab, B25, type_time=0.8)[0]
            mark_extra(self, tab, l25)
            vo.wait_until("Slash and slash docs answer 404")
            o25 = out(self, tab, [B25.line(2), (B25.line(3), ERR), B25.line(4), (B25.line(5), ERR)], run_time=0.5)
            self.play(Indicate(o25[1], color=ERR, scale_factor=1.08), Indicate(o25[3], color=ERR, scale_factor=1.08),
                      run_time=0.6)
            self.add(tab)
            vo.wait_until("everything the browser calls is under slash api")
            self.play(FadeIn(rmap.api, shift=DOWN * 0.1), run_time=0.4)
            self.play(Create(rmap.ties[2]), Create(rmap.pen), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in rmap.leaves], lag_ratio=0.12), run_time=0.9)
            self.play(FadeIn(rmap.src), run_time=0.3)
            vo.wait_until("and only the probes stay at the root")
            self.play(FadeIn(rmap.root, shift=DOWN * 0.1), run_time=0.4)
            self.play(Create(rmap.ties[0]), Create(rmap.ties[1]), FadeIn(rmap.lamps), run_time=0.6)
            self.play(Indicate(rmap.lamps, color=TURN, scale_factor=1.05), run_time=0.6)
        # the README's own troubleshooting rows, read in the tail (no SAY)
        self.add(rmap)
        clear_bar(self, tab)
        self.play(FadeOut(rmap), FadeOut(tab), run_time=0.5)
        rec.move_to([0, (PIC_TOP - SAFE_Y) / 2, 0])
        assert rec.get_bottom()[1] > -SAFE_Y + 0.05 and rec.get_top()[1] < PIC_TOP + 0.05, rec.get_top()
        self.play(FadeIn(rec, shift=UP * 0.15), run_time=0.5)
        for r in rec.body:
            self.play(Indicate(r, color=INK, scale_factor=1.02), run_time=0.8)
        self.wait(0.8)

        # ========================================================== 9. PONDER: restart or wait?
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(rec), track(trk, 4), run_time=0.5)
            self.play(FadeIn(pl), run_time=0.6)
            vo.wait_until("Healthz says 200")
            self.play(Indicate(pl.statuses["healthz"], color=OWN), run_time=0.6)
            pl.heal(self)
            vo.wait_until("and readyz says 503")
            self.play(Indicate(pl.statuses["readyz"], color=AMBER), run_time=0.6)
            pl.heal(self)
        card = ponder(self, "/healthz says 200, /readyz says 503.\nRestart the container,\nor just wait?", 8,
                      center=(0, -1.8))
        assert card.get_top()[1] < pl.get_bottom()[1] - 0.02 and card.get_bottom()[1] > -SAFE_Y, card.get_bottom()

        # ========================================================== 10. wait: ready; Kubernetes can use both
        tab2 = term(P_LAPTOP, rows=3, title=T_TAB, size=20)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            self.remove(card)
            self.play(FadeIn(log), FadeIn(tab2), run_time=0.5)
            vo.wait_until("about nine seconds later")
            type_capture(self, tab2, B24, type_time=0.5)
            o24 = out(self, tab2, [(B24.line(2), OWN), (body(B24.line(8)), OWN)], run_time=0.4)
            pin(self, o24[1], beside(row_tag("about 9 s later, here"), o24[1], buff=0.5))
            log_line(self, log, (log_cut(61), OWN))
            vo.wait_until("the model is loaded")
            pl.fill_ring(self, 1.0, run_time=0.8)
            vo.wait_until("and Chroma answers")
            pl.heartbeat(self, beats=2, run_time=1.0)
            pl.set(self, "readyz", "green", "200 · ready")
            vo.wait_until("A restart would only start the loading over")
            self.play(FadeOut(tab2), FadeOut(log), run_time=0.5)
            vo.wait_until("Kubernetes")
            bub, rs, arrs = k8s_bubble(self, pl, at=(0.0, -3.0), run_time=1.0)
            assert bub.get_bottom()[1] > -SAFE_Y and bub.get_top()[1] < pl.box.get_bottom()[1] + 0.01, bub.get_top()
            vo.wait_until("restart on liveness")
            self.play(Indicate(pl.lamps["healthz"], color=OWN), Rotate(rs, -TAU, about_point=rs.get_center()),
                      run_time=0.9)
            pl.heal(self)
            vo.wait_until("send traffic on readiness")
            self.play(Indicate(pl.lamps["readyz"], color=OWN), Indicate(arrs, color=ROUTE, scale_factor=1.1),
                      run_time=0.9)
            pl.heal(self)
            self.wait(0.6)

        self.play(FadeOut(pl), FadeOut(trk), run_time=0.7)
        self.wait(0.3)
