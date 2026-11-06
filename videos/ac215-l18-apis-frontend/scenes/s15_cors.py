"""S15 · Last year's pages: CORS and the preflight (AC215 L18, part 2). Tracker [T24] "README @ branch
2025 › Tutorial (24): Simple Frontend App" (caption "branch 2025 · 14f2a14") 1 → 6, '· extra' in the
last beat. Lecture: 18 · 24–26 (Frontend) from "second trip" (beat 2) to beat 5, 18 · 27 (Frontend) in beats 6–8, off from 9.

Beats (script.md "## S15", one voiceover block each):
0. Tracker [T24] 1. A `laptop · new terminal` (10 rows, prompt student@laptop:~$): `cd
   cheese-app-v2/src/frontend-simple` (c20, no output: the prompt changes); [T24] 2 `sh docker-shell.sh`
   → c21:3 (cut after FINISHED), …; [T24] 3 at the container prompt (c21:19) `http-server` → c21:22
   (with "at the time of recording"), 26, 34–36 (the 8080 URLs PINK). ▶ your turn on the bar.
1. [T24] 4. A 7-row `laptop · second tab` (…/frontend-simple$): c22 (extra) → c22:2–5 (the HTML
   indentation dropped), the two nav links YELLOW. Above it the browser drawing (illustration) at
   localhost:8080/index.html: "Formaggio.me" with the links "Newsletters", "Cheese Assistant", lit on
   "two more pages".
2. [T24] 5, lecture 24–26 (Frontend). The tab grows to 10 rows: c23 → c23:2, 7–8 (axios script, the
   CDN path elided, and newsletters-main.js YELLOW); extra c24 → c24:2–3, `baseURL:
   'http://localhost:9000'` PINK. On "the lecture's second trip" the tab shrinks to a 3-row strip and V1
   comes in above it (localhost:8080/newsletters.html; frontend-simple on 8080 and the API on 9000, no
   cable): the first trip to the 8080 door brings the page back; then the page's own PINK arrow goes
   straight to the 9000 door.
3. The strip goes. Under V1: "page" http · localhost · 8080 and "calls" http · localhost · 9000; the
   two port chips get RED rings and a RED chip "different origin". The ORANGE checkpoint lands on the
   page's arrow, "did the server allow this origin?" above the browser.
4. V1 steps aside for a full `second tab` (10 rows): extra c25 (folds) → c25:2–7 (wrap), both
   access-control-allow-origin: * YELLOW. On "permission granted" the tab shrinks to a strip (the 200,
   content-type, allow-origin rows), V1 returns, the checkpoint opens GREEN and the page fills with the
   first newsletter title (c25:8).
5. A PINK U-turn "307" at the 9000 door; the strip becomes the API's `laptop · new terminal` log
   (c11:79–80, wrapped): 307 PINK, 200 GREEN. In the laptop's free lower band: a GREY card "slides
   24–26: /newsletters · the router: /newsletters/" tagged erratum.
6. [T24] 6, lecture 27 (Frontend). The hops and the card go; a 3-row `second tab`: c26 → c26:2, 4–6
   (chat-main.js YELLOW); the browser goes to chat.html with a text box "How is cheese made?". On "Now
   the browser adds a step" the strip goes and B27's six steps play (captions); on "step zero" they clear
   and a YELLOW 0 with a PINK OPTIONS chip waits in the page.
7. Hop 0: the OPTIONS scout runs to the 9000 door and comes back with the permission slip; only then
   hop 1, the POST, leaves. On "The answer allows" V1 gives way to a 9-row `second tab`: extra c27
   (folds) → c27:2–6; allow-origin, allow-methods, allow-headers (YELLOW) and max-age: 600 (PINK) lit on
   their words.
8. The API's `laptop · new terminal` log (10 rows): c11:81, 82, 85 (wrap), …, 146 → OPTIONS 200 GREEN,
   POST /llm/chats/ 307 PINK, 500 RED. Then a 13-row `second tab`: extra c28 (folds) → c28:2, 6–8,
   13–14 (wrap); over the log (flashed on "the same Gemini error") a GREY tag "recorded without a key · with yours: the retired
   model fails" (S14's erratum: a viewer's own key meets the retired 2025 model, not invalid_grant); line 13 access-control-allow-origin: * YELLOW on the 500 (RED).
9. Lecture off. Two panels with neutral captions: "2025: page on 8080 → API on 9000" (text-free V1
   icon with the ORANGE checkpoint) and "main: page on 3000 → Vite → API" (the courier icon). Under both
   the GREY line "CORS: the browser's rule, about the server's permission · curl and /api/docs never
   see it", curl and /api/docs lit on their words.
10. The panels freeze. PONDER (8 s) over their lower half.
11. The card leaves. "· ask permission" writes on under the left caption, "· one origin" under the
   right; on the right the page's and the call's origin (localhost:3000) slide into one glowing PINK
   label; on the left localhost:8080 and localhost:9000 separate. A GREY chip on the right API box:
   "middleware dropped: nothing needs it".
12. Two 4-row strips: the frontend terminal c21:45–46, `exit` (c21:48), 49 and the API's c11:147,
   152–153, `exit` (c11:154), 155. Tracker '· extra'. A `second tab` (10 rows): extra c30 → c30:2;
   a GREY chip "cd ~/cheese-app-v2", then at student@laptop:~/cheese-app-v2$ extra c31 → c31:2–4 (line
   4 cut after 447b5c3); `git stash pop` typed with the chips "restores your earlier edits, if you want
   them" and "shown without output · not captured". Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S15"]

# ------------------------------------------------------------------ the real sources (checked)
C11 = capture("c11")
C20 = capture("c20")
C21 = capture("c21")
C22 = capture("c22")
C23 = capture("c23")
C24 = capture("c24")
C25 = capture("c25")
C26 = capture("c26")
C27 = capture("c27")
C28 = capture("c28")
C30 = capture("c30")
C31 = capture("c31")

assert C20.cmd == "cd cheese-app-v2/src/frontend-simple" and C20.lines == []
assert C21.cmd == "sh docker-shell.sh" and C21.line(3).startswith("[+] Building 6.6s (9/9) FINISHED")
assert at_prompt(C21, 19) == ("147a04351575:/app#", "http-server")
assert C21.line(22) == "http-server version: 14.1.1" and C21.line(26) == "Cache: 3600 seconds"
assert C21.at((34, 36)) == ["Available on:", "  http://127.0.0.1:8080", "  http://172.18.0.2:8080"]
assert C21.line(45) == "^C" and C21.line(46) == "http-server stopped."
assert at_prompt(C21, 48)[1] == "exit" and C21.line(49) == "exit"
assert C22.cmd.startswith("curl -s -i http://localhost:8080/index.html | grep")
assert C22.line(2) == "HTTP/1.1 200 OK" and C22.line(3).strip() == "<title>Formaggio.me</title>"
assert C22.line(4).strip() == '<a href="/newsletters.html" class="nav-link">Newsletters</a>'
assert C22.line(5).strip() == '<a href="/chat.html" class="nav-link">Cheese Assistant</a>'
assert C23.cmd.startswith("curl -s -i http://localhost:8080/newsletters.html")
assert "axios.min.js" in C23.line(7) and C23.line(8).strip() == '<script src="newsletters-main.js"></script>'
assert C24.line(2) == "newsletters-main.js:3:    baseURL: 'http://localhost:9000',"
assert "/newsletters?limit=" in C24.line(3)
assert C25.cmd.startswith("curl -s -i -L -H 'Origin: http://localhost:8080'")
assert C25.at((2, 7)) == ["HTTP/1.1 307 Temporary Redirect", "location: http://localhost:9000/newsletters/?limit=100",
                          "access-control-allow-origin: *", "HTTP/1.1 200 OK", "content-type: application/json",
                          "access-control-allow-origin: *"]
assert '"title":"Spanish Cheese Journey"' in C25.line(8)
FIRST_TITLE = "Spanish Cheese Journey"                       # c25:8, the first newsletter's title
assert C26.line(2) == "HTTP/1.1 200 OK" and C26.line(6).strip() == '<script src="chat-main.js"></script>'
assert "axios.min.js" in C26.line(4) and "marked.min.js" in C26.line(5)
assert C27.cmd.startswith("curl -s -i -X OPTIONS -H 'Origin: http://localhost:8080'")
assert C27.at((2, 6)) == ["HTTP/1.1 200 OK", "access-control-allow-origin: *",
                          "access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
                          "access-control-max-age: 600", "access-control-allow-headers: content-type,x-session-id"]
assert C28.cmd.startswith("curl -s -i -L -X POST -H 'Origin: http://localhost:8080'")
assert C28.line(2) == "HTTP/1.1 307 Temporary Redirect" and C28.line(6) == "location: http://localhost:9000/llm/chats"
assert C28.line(7) == "access-control-allow-origin: *" and C28.line(8) == "HTTP/1.1 500 Internal Server Error"
assert C28.line(13) == "access-control-allow-origin: *" and C28.line(14).startswith('{"detail":"Failed to generate')
assert '"GET /newsletters?limit=100 HTTP/1.1" 307' in C11.line(79)
assert '"GET /newsletters/?limit=100 HTTP/1.1" 200' in C11.line(80)
assert '"OPTIONS /llm/chats HTTP/1.1" 200' in C11.line(81)
assert '"POST /llm/chats/ HTTP/1.1" 307' in C11.line(82)
assert C11.line(85).startswith("Error generating response: ('invalid_grant")
assert '"POST /llm/chats HTTP/1.1" 500' in C11.line(146)
assert C11.line(147) == "^C" and C11.line(152) == "INFO:     Stopping reloader process [11]"
assert C11.line(153) == "app@c9f05403249e:/app$" and at_prompt(C11, 154)[1] == "exit" and C11.line(155) == "exit"
assert C30.cmd == "docker stop cheese-app-vector-db; docker ps -a" and C30.line(2) == C_VDB
assert C31.cmd == "git checkout -- . && git switch main && git log -1 --format='%h %s'"
assert C31.at(2, 3) == ["Switched to branch 'main'", "Your branch is up to date with 'origin/main'."]
assert C31.line(4).startswith("447b5c3 ")
HEAD_MAIN = cut(C31.line(4), "447b5c3")
assert HEAD_MAIN == "447b5c3…"
STASH_POP = "git stash pop"                                  # script.md: typed, no output (not captured)


def html(s: str) -> str:
    """An HTML source row as grep printed it, without its indentation (the text is unchanged)."""
    return s.strip()


def elide(s: str, mid: str) -> str:
    """`mid` (the first occurrence) replaced by the house '…' (a CDN path that would not fit a row)."""
    assert mid in s, (mid, s)
    return s.replace(mid, "…", 1)


CDN = "cloudflare.com/ajax/libs"
AXIOS_ROW = elide(html(C23.line(7)), CDN)
assert AXIOS_ROW == '<script src="https://cdnjs.…/axios/1.6.2/axios.min.js"></script>', AXIOS_ROW


# ------------------------------------------------------------------ local helpers (as in S14)
def tracker_t24_fixed(step: int, extra=False) -> ReadmeTracker:
    """tracker_t24(step) with its 'README @ branch 2025 › …' head put back above the dots (as S14's
    tracker_t23_fixed): common.tracker() re-arranges a 'README @ ref' head with VGroup.arrange(), which
    re-centres it mid-frame; the head goes back to a plain tracker's offset over the dots."""
    tr = tracker_t24(step, extra)
    ref = tracker_b(1)
    off = ref.head.get_y() - ref.dots.get_y()
    tr.head.shift(UP * (tr.dots.get_y() + off - tr.head.get_y()))
    place_tracker(tr)
    assert abs((tr.head.get_y() - tr.dots.get_y()) - off) < 1e-6 and tr.get_top()[1] <= TRACK_TOP + 1e-6
    assert tr.get_bottom()[1] > TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def bar_tag(scene, t: Terminal, tg):
    """PLAYS: a row-sized tag on the terminal's title bar (replacing the one there)."""
    old = getattr(t, "bar_tag", None)
    on_bar(t, tg)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    else:
        scene.play(FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    scene.remove(tg)
    t.add(tg)
    scene.add(t)                         # the tag lives in the terminal only (it leaves with it)
    t.bar_tag = tg
    return tg


def mark_extra(scene, t: Terminal, line, kind=None):
    """PLAYS: the row tag 'extra' beside a typed command, or on the title bar when no room is left."""
    tg = beside(extra_row(kind), line, buff=0.4)
    if tg.get_right()[0] <= t.box.get_right()[0] - 0.1:
        pin(scene, line, tg)
        return tg
    return bar_tag(scene, t, extra_row(kind))


def clear_bar(scene, t: Terminal, *extra):
    """PLAYS: the title-bar tag (if any) leaves."""
    old = getattr(t, "bar_tag", None)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), *extra, run_time=0.3)
        scene.remove(old)
        t.bar_tag = None
    elif extra:
        scene.play(*extra, run_time=0.3)


def clear_lines(scene, t: Terminal, *extra, run_time: float = 0.4):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(VGroup(*gone)), *extra, run_time=run_time)
    scene.remove(*gone)


def row_with(rows, sub: str):
    """The first terminal row (of `rows`) whose text holds `sub`."""
    for r in rows:
        if sub in r.text:
            return r
    raise ValueError(f"{sub!r} in none of {[r.text for r in rows]}")


def rows_from(rows, sub: str, n: int):
    """`n` consecutive rows starting at the row that holds `sub` (a wrapped capture line)."""
    rows = list(rows)
    i = rows.index(row_with(rows, sub))
    return rows[i:i + n]


def strip_at(prompt: str, rows: int, title: str, bottom: float = BOTTOM) -> Terminal:
    t = term(prompt, rows=rows, title=title, size=20)
    t.shift(UP * (bottom - t.box.get_bottom()[1]))
    return t


def origin_row(name: str, port: str) -> VGroup:
    """'page' / 'calls' + the origin as three PINK chips. .name .origin"""
    nm = label(name, 20, S.GREY)
    o = origin_chips("http", "localhost", port)
    g = VGroup(nm, o).arrange(RIGHT, buff=0.3)
    g.name, g.origin = nm, o
    return g


def scout_hop(scene, tr, sc, bd, text: str, target: str = "api", run_time: float = 1.0):
    """PLAYS hop 0 (as RequestTrace.hop(0)) with the scout chip `sc` and badge `bd` already waiting in
    the page: the same chip leaves and comes back (no fade-out/fade-in of a copy), and the permission
    slip lands a little further left/up than hop(0)'s, clear of the caption row. Returns the slip."""
    net = tr.net
    home = sc.get_center()
    scene.remove(bd)
    tr.marks.add(bd)                     # the badge stays with the hops (clear_hops takes it)
    tr.set_caption(scene, text)
    scene.add(sc)
    scene.play(sc.animate.move_to(net.door_point(target) + LEFT * (sc.width / 2 + 0.12)), run_time=run_time * 0.6)
    scene.play(net.door_pulse(target, ROUTE), run_time=0.4)
    tr.heal(scene)
    scene.add(sc)                        # heal() re-seats the trace on top: the scout stays in front
    back = permission_slip("access-control-allow-origin", 20)
    back.next_to(tr.browser.frame, DOWN, buff=0.12).align_to(tr.browser.frame, LEFT).shift(LEFT * 0.05)
    assert back.get_left()[0] > -SAFE_X and back.get_right()[0] < tr.caption.get_left()[0] - 0.2, \
        (back.get_corner(DR), tr.caption.get_corner(UL))
    scene.play(sc.animate.move_to(home), run_time=run_time * 0.6)
    scene.play(FadeOut(sc), FadeIn(back, shift=UP * 0.1), run_time=0.4)
    scene.remove(sc)
    tr.marks.add(back)
    tr.heal(scene)
    return back


SHIFT_UP = 0.85            # V1 over a 3- or 4-row strip: it spans y -1.15 .. 2.85


class CorsPreflight(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S15"] == 13, len(SAY)

        # ========================================================== 0. Tutorial 24 steps 1-3: http-server
        trk = tracker_t24_fixed(1)
        t0 = term(P_LAPTOP, rows=10, title=T_NEW, size=20)
        assert t0.box.get_top()[1] < TRACK_BOTTOM - 0.1, t0.box.get_top()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t0, shift=UP * 0.2), run_time=0.6)
            bare_prompt(self, t0)
            vo.wait_until("change into")
            type_capture(self, t0, C20, type_time=0.8)
            ln0 = cd_prompt(self, t0, P_V2_SIMPLE)
            vo.wait_until("frontend simple")
            self.play(Indicate(substring(ln0, "cheese-app-v2/src/frontend-simple"), color=LAPTOP, scale_factor=1.08),
                      run_time=0.7)
            self.add(t0)
            vo.wait_until("Steps 2 and 3")
            self.play(track(trk, 2), run_time=0.4)
            type_capture(self, t0, C21, type_time=0.5)
            out(self, t0, [cut(C21.line(3), "FINISHED"), "…"], run_time=0.5)
            vo.wait_until("then http-server")
            self.play(track(trk, 3), run_time=0.4)
            type_at(self, t0, C21, 19, type_time=0.4)
            o0 = out(self, t0, C21.at(22, 26, (34, 36)), run_time=0.6)
            ver = row_with(o0, "14.1.1")
            pin(self, ver, beside(time_row(), ver, buff=0.5))
            urls = [r for r in o0 if r.text.endswith(":8080")]
            assert len(urls) == 2
            self.play(*[substring(r, "8080").animate.set_color(ROUTE) for r in urls], run_time=0.4)
            self.play(*[Indicate(substring(r, "8080"), color=ROUTE, scale_factor=1.2) for r in urls], run_time=0.6)
            self.add(t0)
            vo.wait_until("Pause and start it")
            turn = bar_tag(self, t0, turn_row())
            flash_tag(self, turn, TURN)
            self.add(t0)

        # ========================================================== 1. home page: index.html links two more pages
        tab = strip_at(P_V2_SIMPLE, 7, T_TAB)
        top1 = tab.box.get_top()[1]
        bw1 = Browser("localhost:8080/index.html", win_w=5.4, win_h=PIC_TOP - top1 - 0.3)
        bw1.move_to([-6.45 + bw1.win_w / 2, (top1 + PIC_TOP) / 2 + 0.02, 0])
        assert bw1.get_bottom()[1] > top1 + 0.1 and bw1.get_top()[1] <= PIC_TOP + 0.02, (bw1.get_bottom(), bw1.get_top())
        ill1 = illustration_tag().next_to(bw1.frame, RIGHT, buff=0.25).align_to(bw1.frame, UP)
        links = VGroup(route_chip("Newsletters", mono_font=False), route_chip("Cheese Assistant", mono_font=False))
        links.arrange(RIGHT, buff=0.3)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(t0), track(trk, 4), FadeIn(tab, shift=UP * 0.2), FadeIn(bw1), FadeIn(ill1), run_time=0.6)
            ln = type_capture(self, tab, C22, type_time=0.8)[-1]
            mark_extra(self, tab, ln)
            o1 = out(self, tab, [C22.line(2)] + [html(s) for s in C22.at((3, 5))], run_time=0.5)
            bw1.fill(self, [label("Formaggio.me", 24, INK), links], run_time=0.4)
            vo.wait_until("The landing page")
            nav = [row_with(o1, "Newsletters</a>"), row_with(o1, "Cheese Assistant</a>")]
            self.play(*[r.animate.set_color(TURN) for r in nav], run_time=0.4)
            self.add(tab)
            vo.wait_until("newsletters and chat")
            self.play(Indicate(links[0], color=TURN, scale_factor=1.1), run_time=0.5)
            bw1.heal(self)
            self.play(Indicate(links[1], color=TURN, scale_factor=1.1), run_time=0.5)
            bw1.heal(self)

        # ========================================================== 2. newsletters.html: its script calls 9000 itself
        ref = lref("24–26 (Frontend)")
        tr = RequestTrace("localhost:8080/newsletters.html", rows=("front", "api"), front="simple", cable=False,
                          browser_w=4.8, caption=True).shift(UP * SHIFT_UP)
        net = tr.net
        ill = illustration_tag().next_to(tr.browser, DOWN, buff=0.1).align_to(tr.browser, LEFT)
        assert tr.get_top()[1] < ref.get_bottom()[1] - 0.1 and net.frame.get_left()[0] > trk.get_right()[0] - 2.0
        with self.voiceover(SAY[2]) as vo:
            clear_lines(self, tab, FadeOut(bw1), FadeOut(ill1), run_time=0.4)
            self.play(track(trk, 5), run_time=0.5)
            clear_bar(self, tab)
            resize(self, tab, 10, run_time=0.5)
            ln = type_capture(self, tab, C23, type_time=0.8)[-1]
            o2 = out(self, tab, [C23.line(2), AXIOS_ROW, html(C23.line(8))], run_time=0.5)
            self.play(substring(row_with(o2, "axios.min.js"), "axios.min.js").animate.set_color(TURN),
                      substring(row_with(o2, "newsletters-main.js"), "newsletters-main.js").animate.set_color(TURN),
                      run_time=0.5)
            self.add(tab)
            vo.wait_until("Its script names the API")
            ln = type_capture(self, tab, C24, type_time=0.7)[-1]
            mark_extra(self, tab, ln)
            o3 = out(self, tab, C24.at(2, 3), wrap=True, run_time=0.5)
            base = row_with(o3, "baseURL")
            self.play(substring(base, "baseURL: 'http://localhost:9000'").animate.set_color(ROUTE), run_time=0.4)
            self.play(Indicate(substring(base, "localhost:9000"), color=ROUTE, scale_factor=1.15), run_time=0.6)
            self.add(tab)
            vo.wait_until("This is the lecture's second trip")
            clear_bar(self, tab)
            resize(self, tab, 3, keep=[base] + [r for r in o3 if r is not base][:2], run_time=0.5)
            bar_tag(self, tab, extra_row())
            assert tab.box.get_top()[1] < tr.get_bottom()[1] - 0.05, (tab.box.get_top(), tr.get_bottom())
            self.play(FadeIn(tr), FadeIn(ill), FadeIn(ref), run_time=0.6)     # the tag comes with its picture
            vo.wait_until("the page came from 8080")
            a1 = tr._req_arrow("front")
            tr.show(self, a1, anims=[GrowArrow(a1)], into=tr.marks, run_time=0.5)
            self.play(net.door_pulse("front"), Indicate(net.inner["front"], color=TURN, scale_factor=1.1), run_time=0.6)
            tr.heal(self)
            dot = pulse_dot(ROUTE, 0.1).move_to(a1.get_end())
            self.add(dot)
            self.play(dot.animate.move_to(a1.get_start()), run_time=0.5)
            self.remove(dot)
            tr.browser.fill(self, [label("Newsletters", 24, INK)], run_time=0.4)
            vo.wait_until("and its JavaScript calls")
            self.play(a1.animate.set_stroke(opacity=0.35), run_time=0.3)
            tr.heal(self)
            tr.page_call(self, "api", run_time=0.8)
            self.play(net.door_pulse("api", ROUTE), Indicate(net.inner["api"], color=TURN, scale_factor=1.1),
                      run_time=0.7)
            tr.heal(self)

        # ========================================================== 3. a different origin; the browser's checkpoint
        op = origin_row("page", "8080")
        oc = origin_row("calls", "9000")
        rows3 = VGroup(op, oc).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        x_or = max(op.name.get_right()[0], oc.name.get_right()[0]) + 0.3
        for g in (op, oc):                          # the chips line up whatever the name's width
            g.origin.shift(RIGHT * (x_or - g.origin.get_left()[0]))
        rows3.move_to([-6.45 + rows3.width / 2, (tr.get_bottom()[1] - SAFE_Y) / 2, 0])
        assert rows3.get_top()[1] < tr.get_bottom()[1] - 0.15 and rows3.get_bottom()[1] > -SAFE_Y + 0.05, rows3
        rp, rc = ring(op.origin.port, ERR, buff=0.06), ring(oc.origin.port, ERR, buff=0.06)
        diff = err_chip("different origin", mono_font=False)
        diff.next_to(VGroup(op.origin.port, oc.origin.port), RIGHT, buff=0.45)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(tab), run_time=0.4)
            self.play(Indicate(net.title, color=INK, scale_factor=1.15), run_time=0.6)
            tr.heal(self)
            self.play(FadeIn(op, shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(oc, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("different port")
            self.play(Create(rp), Create(rc), run_time=0.5)
            vo.wait_until("so a different origin")
            self.play(FadeIn(diff, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, diff, ERR)
            vo.wait_until("Now the browser checks")
            g = tr.gate(self, run_time=0.5)
            assert g.text.get_top()[1] < TRACK_BOTTOM - 0.02, g.text.get_top()
            vo.wait_until("did the server allow")
            self.play(Indicate(g.text, color=SHARED, scale_factor=1.06), run_time=0.7)
            tr.heal(self)

        # ========================================================== 4. curl sends what the browser sends: allowed
        tab4 = strip_at(P_V2_SIMPLE, 11, T_TAB)
        assert tab4.box.get_top()[1] < TRACK_BOTTOM - 0.1
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(op, oc, rp, rc, diff)), run_time=0.4)
            self.play(FadeOut(tr), FadeOut(ill), FadeOut(ref), FadeIn(tab4, shift=UP * 0.2), run_time=0.5)  # the tag leaves with its picture
            ln = type_capture(self, tab4, C25, type_time=1.4)[-1]
            bar_tag(self, tab4, extra_row())
            o4 = out(self, tab4, C25.at((2, 7)), wrap=True, run_time=0.6)
            vo.wait_until("The API answers")
            acao = [r for r in o4 if r.text == "access-control-allow-origin: *"]
            assert len(acao) == 2
            self.play(*[r.animate.set_color(TURN) for r in acao], run_time=0.4)
            self.play(*[Indicate(r, color=TURN, scale_factor=1.05) for r in acao], run_time=0.6)
            self.add(tab4)
            vo.wait_until("permission granted")
            keep4 = list(o4)[-3:]
            assert keep4[0].text == "HTTP/1.1 200 OK", [r.text for r in keep4]
            clear_bar(self, tab4)
            resize(self, tab4, 3, keep=keep4, run_time=0.5)
            bar_tag(self, tab4, extra_row())
            self.play(FadeIn(tr), FadeIn(ill), FadeIn(ref), run_time=0.5)  # and comes back with it
            self.play(open_gate(g), run_time=0.6)
            tr.heal(self)
            tr.browser.fill(self, [label("Newsletters", 24, INK), label(FIRST_TITLE, 20, INK), label("…", 20, S.GREY)],
                            run_time=0.4)
            self.play(Indicate(keep4[-1], color=TURN, scale_factor=1.05), run_time=0.5)
            self.add(tab4)

        # ========================================================== 5. 307 then 200: one slash apart
        log5 = strip_at(container_prompt(C11, 153), 4, T_NEW)
        assert log5.box.get_top()[1] < tr.get_bottom()[1] - 0.02, (log5.box.get_top(), tr.get_bottom())
        er_rows = [VGroup(label("slides 24–26:", 20, S.GREY), mono("/newsletters", 20, ROUTE)).arrange(RIGHT, buff=0.15),
                   VGroup(label("the router:", 20, S.GREY), mono("/newsletters/", 20, ROUTE)).arrange(RIGHT, buff=0.15)]
        er_card = card(er_rows, S.GREY, size=20, buff=0.12)
        er_tag = erratum_tag()
        band_top = net.boxes["api"].get_bottom()[1] - 0.1
        band_bot = net.frame.get_bottom()[1] + 0.1
        er_card.move_to([net.boxes["api"].get_center()[0] + 0.3, (band_top + band_bot) / 2 - 0.05, 0])
        er_tag.move_to(er_card.frame.get_corner(UL) + np.array([er_tag.width / 2 + 0.2, 0, 0]))
        assert er_card.get_bottom()[1] > band_bot and er_tag.get_top()[1] < band_top + 0.05, \
            (er_card.get_bottom(), er_tag.get_top(), band_top, band_bot)
        assert er_card.get_right()[0] < net.frame.get_right()[0] - 0.1
        with self.voiceover(SAY[5]) as vo:
            tr.uturn(self, "307", "api", run_time=0.7)
            self.play(FadeOut(tab4), FadeIn(log5, shift=UP * 0.2), run_time=0.5)
            o5 = out(self, log5, C11.at(79, 80), wrap=True, run_time=0.5)
            r307 = row_with(o5, "/newsletters?limit")
            self.play(substring(r307, "307").animate.set_color(ROUTE), run_time=0.4)
            self.add(log5)
            vo.wait_until("then 200")
            r200 = row_with(o5, "/newsletters/?limit")
            self.play(substring(r200, "\" 200").animate.set_color(OWN), run_time=0.4)
            self.add(log5)
            vo.wait_until("the paths differ")
            self.play(FadeIn(er_card, shift=UP * 0.1), FadeIn(er_tag), run_time=0.5)
            self.play(Indicate(er_rows[1][1], color=ROUTE, scale_factor=1.12),
                      Indicate(substring(r200, "/newsletters/"), color=ROUTE, scale_factor=1.1), run_time=0.7)
            self.add(log5)
            vo.wait_until("an extra round trip")
            self.play(Indicate(tr.marks[-1], color=ROUTE, scale_factor=1.15), run_time=0.7)
            tr.heal(self)

        # ========================================================== 6. chat.html; B27's six steps; step zero
        ref6 = lref("27 (Frontend)")
        tab6 = strip_at(P_V2_SIMPLE, 3, T_TAB)
        ask = VGroup(RoundedRectangle(width=3.4, height=0.5, corner_radius=0.1, stroke_color=S.GREY, stroke_width=2)
                     .set_fill(TERM_BG, 1), label("How is cheese made?", 20, INK))
        ask[1].move_to(ask[0]).align_to(ask[0], LEFT).shift(RIGHT * 0.15)
        with self.voiceover(SAY[6]) as vo:
            tr.clear_hops(self, run_time=0.4)
            self.play(FadeOut(VGroup(er_card, er_tag, log5)), FadeOut(ref), FadeIn(ref6), track(trk, 6), run_time=0.5)
            tr.browser.clear(self, run_time=0.2)
            tr.browser.goto(self, "localhost:8080/chat.html", run_time=0.4)
            self.play(FadeIn(tab6, shift=UP * 0.2), run_time=0.3)
            type_capture(self, tab6, C26, type_time=0.7)
            o6 = out(self, tab6, [C26.line(2), elide(html(C26.line(4)), CDN), elide(html(C26.line(5)), CDN),
                                  html(C26.line(6))], run_time=0.5, chunk=3)
            self.play(substring(o6[-1], "chat-main.js").animate.set_color(TURN), run_time=0.4)
            self.add(tab6)
            gap = Rectangle(width=0.1, height=0.75, stroke_width=0, fill_opacity=0)     # the box sits low in the page
            tr.browser.fill(self, [label("Cheese Assistant", 24, INK), gap, ask], run_time=0.4)
            self.play(Indicate(ask[1], color=TURN, scale_factor=1.08), run_time=0.5)
            tr.heal(self)
            vo.wait_until("Now the browser adds")
            self.play(FadeOut(tab6), run_time=0.3)
            tr.trip(self, "api", (1, 2, 3, 4, 5, 6), per=0.45)
            vo.wait_until("step zero")
            tr.clear_hops(self, run_time=0.3)
            # the scout waits in the page where hop 0 starts (the same chip and badge as hop 0's)
            home = tr.browser.at(0.45, 0.2)
            sc0 = route_chip("OPTIONS", 20).move_to(home)
            sc0.box.set_fill(S.BG, 1)
            bd0 = step_badge("0", TURN, size=22, radius=0.22).next_to(sc0, LEFT, buff=0.1)
            bd0[0].set_fill(S.BG, 1)
            self.play(FadeIn(bd0, scale=1.3), FadeIn(sc0), run_time=0.5)
            self.play(Indicate(bd0, color=TURN, scale_factor=1.25), run_time=0.6)

        # ========================================================== 7. the preflight: OPTIONS first, then the POST
        tab7 = strip_at(P_V2_SIMPLE, 11, T_TAB)
        assert tab7.box.get_top()[1] < TRACK_BOTTOM - 0.1
        with self.voiceover(SAY[7]) as vo:
            self.play(ill.animate.next_to(tr.browser, UP, buff=0.1).align_to(tr.browser, LEFT), run_time=0.4)
            self.play(Indicate(ask, color=TURN, scale_factor=1.06), run_time=0.7)
            tr.heal(self)
            self.add(bd0, sc0)                   # heal() re-seats the trace on top: the waiting scout stays in front
            vo.wait_until("makes the browser ask first")
            slip = scout_hop(self, tr, sc0, bd0, "0 OPTIONS first", run_time=1.0)
            self.play(Indicate(slip.text, color=ROUTE, scale_factor=1.05), run_time=0.5)
            tr.heal(self)
            tr.hop(self, 1, "api", text="1 then the POST", run_time=0.6)
            self.play(net.door_pulse("api", ROUTE), run_time=0.6)        # the POST is seen to land
            tr.heal(self)
            vo.wait_until("The answer allows")
            self.play(FadeOut(tr), FadeOut(ill), FadeOut(ref6), FadeIn(tab7, shift=UP * 0.2), run_time=0.5)  # B27 leaves: so does its tag
            type_capture(self, tab7, C27, type_time=1.2)
            bar_tag(self, tab7, extra_row())
            o7 = out(self, tab7, C27.at((2, 6)), wrap=True, run_time=0.5)
            r_or, r_me = row_with(o7, "allow-origin"), row_with(o7, "allow-methods")
            r_age, r_hd = row_with(o7, "max-age"), row_with(o7, "allow-headers")
            self.play(r_or.animate.set_color(TURN), run_time=0.4)
            self.add(tab7)
            vo.wait_until("these methods")
            self.play(Indicate(r_me, color=INK, scale_factor=1.04), run_time=0.6)
            self.add(tab7)
            vo.wait_until("and these two headers")
            self.play(r_hd.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(substring(r_hd, "content-type,x-session-id"), color=TURN, scale_factor=1.1), run_time=0.6)
            self.add(tab7)
            vo.wait_until("for 600 seconds")
            self.play(r_age.animate.set_color(ROUTE), run_time=0.4)
            self.play(Indicate(substring(r_age, "600"), color=ROUTE, scale_factor=1.25), run_time=0.6)
            self.add(tab7)

        # ========================================================== 8. the log: OPTIONS 200, 307, 500; the 500 carries the header
        log8 = strip_at(container_prompt(C11, 153), 10, T_NEW)
        tab8 = strip_at(P_V2_SIMPLE, 13, T_TAB)
        assert tab8.box.get_top()[1] < TRACK_BOTTOM - 0.1, tab8.box.get_top()
        # the recording had no key (invalid_grant); a viewer's key meets S14's retired 2025 model instead.
        # It comes with the log (the Gemini-error window alone is ~2 s) and flashes on "the same Gemini error".
        nokey = under_term(log8, row_tag("recorded without a key · with yours: the retired model fails"))
        assert nokey.get_top()[1] < TRACK_BOTTOM - 0.1 and nokey.get_left()[0] > -SAFE_X, nokey.get_corner(UL)
        log8.add(nokey)                          # it leaves with the log
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(tab7), FadeIn(log8, shift=UP * 0.2), run_time=0.5)
            o8 = out(self, log8, [(C11.line(81), OWN)] + C11.at(82) + soft([C11.line(85)], log8.max_chars)
                     + ["…", (C11.line(146), ERR)], wrap=True, run_time=0.7)
            r81 = row_with(o8, "OPTIONS /llm/chats")
            self.play(Indicate(r81, color=OWN, scale_factor=1.04), run_time=0.5)
            self.add(log8)
            vo.wait_until("then the post bounces")
            r82 = rows_from(o8, "POST /llm/chats/", 2)
            self.play(*[r.animate.set_color(ROUTE) for r in r82], run_time=0.4)
            self.add(log8)
            vo.wait_until("and ends in 500")
            r146 = rows_from(o8, "POST /llm/chats HTTP", 2)
            self.play(*[Indicate(r, color=ERR, scale_factor=1.04) for r in r146], run_time=0.6)
            self.add(log8)
            vo.wait_until("the same Gemini error")
            r85 = rows_from(o8, "Error generating response", 3)
            self.play(*[r.animate.set_color(ERR) for r in r85], run_time=0.4)
            self.play(*[Indicate(r, color=ERR, scale_factor=1.03) for r in r85], run_time=0.6)
            self.add(log8)
            flash_tag(self, nokey, S.GREY)
            self.add(log8)
            vo.wait_until("That 500 carries")
            self.play(FadeOut(log8), FadeIn(tab8, shift=UP * 0.2), run_time=0.5)
            type_capture(self, tab8, C28, type_time=1.4)
            bar_tag(self, tab8, extra_row())
            o8b = out(self, tab8, [C28.line(2)] + C28.at((6, 7)) + [(C28.line(8), ERR), C28.line(13), C28.line(14)],
                      wrap=True, run_time=0.6)
            r13 = [r for r in o8b if r.text == "access-control-allow-origin: *"][-1]
            self.play(r13.animate.set_color(TURN), run_time=0.4)
            self.add(tab8)
            vo.wait_until("so the browser shows")
            self.play(Indicate(r13, color=TURN, scale_factor=1.06), run_time=0.6)
            self.play(*[Indicate(r, color=ERR, scale_factor=1.03) for r in rows_from(o8b, '{"detail"', 3)],
                      run_time=0.6)
            self.add(tab8)

        # ========================================================== 9. CORS in one line: two panels
        pw, ph = 6.35, 4.2
        p_top = PIC_TOP - 0.15
        panels, icons, caps = [], [], []
        for k, (gate_on, text) in enumerate(((True, "2025: page on 8080 → API on 9000"),
                                            (False, "main: page on 3000 → Vite → API"))):
            x = -6.5 + pw / 2 + k * (13.0 - pw)
            fr = outline_box(pw, ph, S.GREY, solid=True, fill_opacity=0.05).move_to([x, p_top - ph / 2, 0])
            ic = trace_icon(1.45, courier=not gate_on, gate=gate_on).move_to([x, fr.get_top()[1] - 0.25 - 0.725, 0])
            cp = label(text, 22, INK).move_to([x, ic.get_bottom()[1] - 0.95, 0])
            panels.append(fr)
            icons.append(ic)
            caps.append(cp)
            assert cp.width < pw - 0.3, (text, cp.width)
        assert panels[0].get_right()[0] < panels[1].get_left()[0] - 0.2 and panels[1].get_right()[0] <= SAFE_X
        assert panels[0].get_top()[1] < TRACK_BOTTOM - 0.05
        tail = VGroup(label("CORS: the browser's rule, about the server's permission ·", 22, S.GREY),
                      VGroup(mono("curl", 22, S.GREY), label("and", 22, S.GREY), mono("/api/docs", 22, S.GREY),
                             label("never see it", 22, S.GREY)).arrange(RIGHT, buff=0.14))
        tail.arrange(DOWN, buff=0.14).move_to([0, (panels[0].get_bottom()[1] - SAFE_Y) / 2, 0])
        assert tail.get_top()[1] < panels[0].get_bottom()[1] - 0.1 and tail.get_bottom()[1] > -SAFE_Y + 0.05, tail
        with self.voiceover(SAY[9]) as vo:
            clear_bar(self, tab8)
            self.play(FadeOut(tab8), *[FadeIn(VGroup(f, i), shift=UP * 0.15) for f, i in zip(panels, icons)],
                      run_time=0.7)
            self.play(*[FadeIn(c) for c in caps], run_time=0.5)
            self.play(FadeIn(tail[0], shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(icons[0][-1], color=SHARED, scale_factor=1.3), run_time=0.6)
            vo.wait_until("curl and the docs page")
            self.play(FadeIn(tail[1], shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(tail[1][0], color=INK, scale_factor=1.15), Indicate(tail[1][2], color=INK, scale_factor=1.1),
                      run_time=0.6)

        # ========================================================== 10. PONDER: what changed?
        with self.voiceover(SAY[10]) as vo:
            self.play(Indicate(caps[0], color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("and this year's React app")
            self.play(Indicate(caps[1], color=TURN, scale_factor=1.06), run_time=0.7)
            for phrase, part in (("the API", 4), ("the browser", 0), ("the origin it calls", 5)):
                vo.wait_until(phrase)
                self.play(*[Indicate(ic[part], color=TURN, scale_factor=1.2) for ic in icons], run_time=1.0)
        card10 = ponder(self, "Last year's page needed CORS.\nThis year's React app does not.\n"
                              "What changed: the API,\nthe browser, or the origin it calls?", 8, center=(0, -1.35),
                      dim=0.85)   # the card sits on the two pictures: the veil dims what its edges would slice

        # ========================================================== 11. the origin: one origin, nothing to permit
        add_l = label("· ask permission", 22, SHARED).next_to(caps[0], DOWN, buff=0.15)
        add_r = label("· one origin", 22, ROUTE).next_to(caps[1], DOWN, buff=0.15)
        ic_l, ic_r = icons
        # left: the page's origin and the call's origin start together, then part
        l8080, l9000 = mono("localhost:8080", 20, ROUTE), mono("localhost:9000", 20, ROUTE)
        y_or = (ic_l.get_bottom()[1] + caps[0].get_top()[1]) / 2
        mid_l = ic_l.get_x()
        l8080.move_to([mid_l, y_or + 0.16, 0])        # together at first (one above the other), then apart
        l9000.move_to([mid_l, y_or - 0.16, 0])
        l8080_to = l8080.copy().move_to([mid_l - 1.35, y_or, 0])
        l9000_to = l9000.copy().move_to([mid_l + 1.35, y_or, 0])
        # right: two labels of the same origin slide into one
        mid_r = ic_r.get_x()
        r_a, r_b = mono("localhost:3000", 20, ROUTE), mono("localhost:3000", 20, ROUTE)
        r_a.move_to([mid_r - 1.35, y_or, 0])
        r_b.move_to([mid_r + 1.35, y_or, 0])
        one = mono("localhost:3000", 22, ROUTE).move_to([mid_r, y_or, 0])
        glow = ring(one, ROUTE, buff=0.1)
        api_box = ic_r[4]
        drop = grey_chip("middleware dropped: nothing needs it")
        drop.next_to(add_r, DOWN, buff=0.15).set_x(mid_r)
        lead = DashedLine(api_box.get_right() + RIGHT * 0.05, [drop.get_right()[0] - 0.3, drop.get_top()[1], 0],
                          color=S.GREY, stroke_width=2, dash_length=0.08)
        assert drop.get_bottom()[1] > panels[1].get_bottom()[1] + 0.05 and drop.get_right()[0] < panels[1].get_right()[0]
        assert l8080_to.get_left()[0] > panels[0].get_left()[0] + 0.05 and r_b.get_right()[0] < panels[1].get_right()[0] - 0.05
        assert add_l.get_bottom()[1] > panels[0].get_bottom()[1] + 0.05
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(card10), run_time=0.4)
            self.play(Write(add_l), Write(add_r), run_time=0.8)
            vo.wait_until("The React page")
            self.play(FadeIn(r_a), FadeIn(r_b), run_time=0.4)
            self.play(Transform(r_a, one), Transform(r_b, one), run_time=0.8)
            self.remove(r_b)
            self.play(Create(glow), Indicate(r_a, color=ROUTE, scale_factor=1.12), run_time=0.6)
            self.play(FadeIn(l8080), FadeIn(l9000), run_time=0.3)
            self.play(Transform(l8080, l8080_to), Transform(l9000, l9000_to), run_time=0.7)
            vo.wait_until("and a proxy forwards")
            self.play(Indicate(ic_r[-1], color=TOOL, scale_factor=1.4), run_time=0.6)
            vo.wait_until("The API then dropped")
            self.play(Create(lead), FadeIn(drop, shift=UP * 0.1), run_time=0.5)
            self.play(api_box.animate(rate_func=there_and_back).set_stroke(TURN, width=6), run_time=0.7)
            self.play(Indicate(drop.text, color=S.GREY, scale_factor=1.06), run_time=0.6)

        # ========================================================== 12. stop both, back to main
        s_front = term(container_prompt(C21, 47), rows=4, title=T_NEW, size=20)
        s_api = strip_at(container_prompt(C11, 153), 5, T_NEW)
        s_front.shift(UP * (s_api.box.get_top()[1] + 0.2 - s_front.box.get_bottom()[1]))
        assert s_front.box.get_top()[1] < TRACK_BOTTOM - 0.1, s_front.box.get_top()
        tab12 = strip_at(P_V2_SIMPLE, 10, T_TAB)
        cd_chip = grey_chip("cd ~/cheese-app-v2", mono_font=True)
        pop_chips = VGroup(grey_chip("restores your earlier edits, if you want them"), no_panel_chip())
        pop_chips.arrange(RIGHT, buff=0.2)
        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(VGroup(*panels, *icons, *caps, tail, add_l, add_r, r_a, glow, l8080, l9000, lead, drop)),
                      FadeIn(s_front, shift=UP * 0.2), FadeIn(s_api, shift=UP * 0.2), run_time=0.6)
            out(self, s_front, C21.at(45, 46), run_time=0.3)
            out(self, s_api, C11.at(147, "…", 152, 153), run_time=0.4)
            type_at(self, s_front, C21, 48, type_time=0.3)
            out(self, s_front, C21.at(49), run_time=0.2)
            type_at(self, s_api, C11, 154, type_time=0.3)
            out(self, s_api, C11.at(155), run_time=0.2)
            vo.wait_until("As extras")
            self.play(FadeOut(s_front), FadeOut(s_api), track(trk, 6, extra=True), run_time=0.5)
            self.play(FadeIn(tab12, shift=UP * 0.2), run_time=0.3)
            ln = type_capture(self, tab12, C30, type_time=0.7)[-1]
            bar_tag(self, tab12, extra_row())
            o12 = out(self, tab12, C30.at(2), run_time=0.3)
            self.play(Indicate(o12[0], color=CONTAINER, scale_factor=1.05), run_time=0.4)
            self.add(tab12)
            vo.wait_until("discard the branch's edits")
            under_term(tab12, cd_chip).align_to(tab12.box, LEFT)
            self.play(FadeIn(cd_chip, shift=DOWN * 0.1), run_time=0.3)
            tab12.set_prompt(P_V2)
            bare_prompt(self, tab12)
            type_capture(self, tab12, C31, type_time=0.8)
            o12b = out(self, tab12, C31.at(2, 3) + [HEAD_MAIN], run_time=0.4)
            self.play(o12b[0].animate.set_color(OWN), run_time=0.3)
            self.add(tab12)
            vo.wait_until("git stash pop")
            type_cmd(self, tab12, STASH_POP, type_time=0.4)
            under_term(tab12, pop_chips).align_to(tab12.box, RIGHT)
            assert pop_chips.get_top()[1] < TRACK_BOTTOM - 0.05 and pop_chips.get_left()[0] > -SAFE_X
            self.play(FadeOut(cd_chip), FadeIn(pop_chips, shift=DOWN * 0.1), run_time=0.4)
            self.wait(1.0)

        self.play(FadeOut(VGroup(tab12, pop_chips)), FadeOut(trk), run_time=0.7)
        self.wait(0.3)
