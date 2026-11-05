"""S05 · Files for the browser: the simple frontend (AC215 L18, part 1). No tracker in beat 0; then
tracker [F] "README › Frontend App (Simple) Container" 1 → 6, then [C1] "README › Docker Cleanup"
(cheese-app-v1) 1 → 4. Lecture: 18 · 16–17 (Frontend) in beat 0, 18–23 (Frontend) in beats 3–4.

Beats (script.md "## S05", one voiceover block each):
0. lecture_ref 16–17. On "a page" a GREY page outline; on "splits" it gives way to three cards that
   fan out one by one: "HTML · structure", "CSS · style", "JavaScript · behavior", the third with
   the PURPLE badge "the only programming language of the three". On "In version 1" the cards go and
   CODE(index.html: 4–12) and CODE(index.html: 74–75) come in at the left; each card becomes a GREY
   chip beside its line ("HTML" at <title> (10), "CSS" at the styles.css link (11), "JavaScript" at
   <script src="main.js"> (74)) and the line gets a GREY ring.
1. Lecture tag off. Tracker [F] 1. A README card (README.md · line 75) over a `laptop · new
   terminal` (prompt ~) that types `cd cheese-app-v1/frontend-simple` → a19:2 RED (wrapped); on
   "Same slip" the card takes the tag "erratum · add src/" and flashes RED, tracker 1 · extra, it
   types `cd cheese-app-v1/src/frontend-simple && ls` (row tag extra) → a20:2–7.
2. Tracker [F] 2; the card becomes README.md · lines 78–82 (Run sh docker-shell.sh · Start Web Server
   · run http-server from the docker shell); the prompt becomes ~/cheese-app-v1/src/frontend-simple;
   ▶ your turn on the bar on
   "pause"; it types `sh docker-shell.sh` → a20b:3 (cut), …, 28–29 (cut). Tracker [F] 3: at the
   container prompt of a20b:30 it types `http-server` → a20b:31, 33, 37, 45–47; 37 `Cache: 3600
   seconds` YELLOW; on "The addresses it prints" a GREY brace "container addresses" at 46–47; on "your
   laptop uses 8080" the card goes and a small picture comes in above the terminal: the laptop wall's PINK door 8080 piped to the
   container's door 8080.
3. Tracker [F] 4, lecture_ref 18–23. V1 RequestTrace (browser localhost:8080, illustration; the laptop
   with the TEAL cheese-app-frontend-simple box, PURPLE http-server, and its /app folder of GREEN file
   icons index.html, main.js, styles.css). Hops 1–3; hop 4's caption "4 the function runs" turns into
   "4 a file is read" (S03's caption left as a GREY ghost) while index.html flashes; hop 5: the
   index.html file rides the response arrow back; hop 6: the page shows "Formaggio.me is here!" and
   its subtitle. ▶ your turn beside the illustration tag on "Pause". Then the hops clear and a 4-row
   `laptop · second tab` strip types a21 (extra) → a21:2–4 (cache-control YELLOW), 5–7.
4. Tracker [F] 4 · extra. The strip types a22 (extra) → a22:2–4, line 2 YELLOW; a dashed GREY arrow
   leaves the page toward a GREY door 9000 (on the laptop's wall) with a "?" and the dashed chip
   "part 2".
5. Lecture tag off. Tracker [F] 5. V1 goes; the strip shrinks to 3 rows; the README card (README.md ·
   lines 86–95) with `erratum`: <body>, the welcome line and </body> RED with the RED note "an old
   whole body · would drop the page and its script tag" beside </body>, the <p> rows GREEN. On "Add only the
   paragraph" the card goes, the GREY chip "your editor", the strip grows to 10 rows and types
   `git -C ~/cheese-app-v1 diff -- src/frontend-simple/index.html` (row tag extra) → a23:15–23, the
   + lines GREEN.
6. Tracker [F] 6. The terminal shrinks to 6 rows; a GREY browser drawing (illustration) at
   localhost:8080 shows the hero, a GREY reload sweep runs and the new paragraph appears under it
   (YELLOW, then WHITE). The strip types a24 (extra) → a24:2–4, line 3 YELLOW; then a25 (extra) →
   a25:2–3, `max-age=3600` YELLOW with the row tag "hard refresh · or http-server -c-1".
7. Tracker [C1] 1 · extra. The browser goes; the `second tab` (7 rows) types a26 (extra) → a26:2–4
   (wrapped at spaces), chip "check: both still running". Tracker [C1] 2: a 3-row `laptop` strip
   above prints a03:62 (^C), types exit at a03:69's prompt, prints a03:70; then the `laptop · new
   terminal` strip does the same with a20b:57–58, 60, 61. The strips go; the tab types
   `docker container ls` → a30:2; a26's table (its two running rows) slides into that empty header
   and vanishes, and the rows close up; the chip becomes "--rm: they removed themselves".
8. Tracker [C1] 3: the tab grows to 10 rows and types `docker system prune` → a31:2–8 (`[y/N] y`
   YELLOW), …, 17. Tracker [C1] 4: `docker image ls` → a32:2–8 (cut after DISK USAGE). Fade; empty
   frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real sources (checked)
A03 = capture("a03")
A19 = capture("a19")
A20 = capture("a20")
A20B = capture("a20b")
A21 = capture("a21")
A22 = capture("a22")
A23 = capture("a23")
A24 = capture("a24")
A25 = capture("a25")
A26 = capture("a26")
A30 = capture("a30")
A31 = capture("a31")
A32 = capture("a32")
assert A19.cmd == "cd cheese-app-v1/frontend-simple", A19.cmd
assert A19.line(2).endswith("No such file or directory"), A19.line(2)
assert A20.cmd == "cd cheese-app-v1/src/frontend-simple && ls", A20.cmd
assert A20.at((2, 7)) == ["Dockerfile", "assets", "docker-shell.sh", "index.html", "main.js", "styles.css"]
assert A20B.cmd == "sh docker-shell.sh", A20B.cmd
assert A20B.line(3).startswith("[+] Building 8.8s (9/9) FINISHED"), A20B.line(3)
assert "naming to docker.io/library/cheese-app-frontend-simple:latest" in A20B.line(28)
assert "unpacking to docker.io/library/cheese-app-frontend-simple:latest" in A20B.line(29)
assert at_prompt(A20B, 30)[1] == "http-server", A20B.line(30)
assert A20B.line(31) == "Starting up http-server, serving ./" and A20B.line(33) == "http-server version: 14.1.1"
assert A20B.line(37) == "Cache: 3600 seconds", A20B.line(37)
assert A20B.line(45) == "Available on:" and A20B.at(46, 47) == ["  http://127.0.0.1:8080", "  http://172.18.0.3:8080"]
assert A20B.at(57, 58) == ["^C", "http-server stopped."], A20B.at(57, 58)
assert at_prompt(A20B, 60)[1] == "exit" and A20B.line(61) == "exit"
assert A03.line(62) == "^C" and at_prompt(A03, 69)[1] == "exit" and A03.line(70) == "exit"
assert A21.at(2, 3) == ["HTTP/1.1 200 OK", "cache-control: max-age=3600"], A21.lines
assert "<title>Formaggio.me</title>" in A21.line(5) and "Formaggio.me is here!" in A21.line(6)
assert A21.line(7).strip() == '<script src="main.js"></script>', A21.line(7)
assert A22.line(2) == "37:// Sample Podcast Data (This would normally come from an API)", A22.line(2)
assert A23.cmd_lines[-1] == "git -C ~/cheese-app-v1 diff -- src/frontend-simple/index.html", A23.cmd_lines
assert [A23.line(n)[0] for n in (19, 20, 21)] == ["+"] * 3, A23.at((19, 21))
assert "placeholder for the awesome" in A24.line(3), A24.line(3)
assert A25.at(2, 3) == ["HTTP/1.1 200 OK", "cache-control: max-age=3600"], A25.lines
assert A26.line(3).startswith("cheese-app-frontend-simple") and A26.line(4).startswith("cheese-app-api-service")
assert A30.cmd == "docker container ls" and A30.line(2).startswith("CONTAINER ID"), A30.lines
assert A31.cmd == "docker system prune" and A31.line(8).endswith("[y/N] y"), A31.line(8)
assert A31.line(17) == "Total reclaimed space: 290.8kB", A31.line(17)
assert A32.cmd == "docker image ls" and "DISK USAGE" in A32.line(2), A32.line(2)

HTML = f"{V1}/src/frontend-simple/index.html"
assert excerpt(HTML, 10, 10).strip() == "<title>Formaggio.me</title>"
assert excerpt(HTML, 11, 11).strip() == '<link rel="stylesheet" href="styles.css">'
assert excerpt(HTML, 74, 74).strip() == '<script src="main.js"></script>'
assert excerpt(HTML, 44, 44).strip() == '<p class="hero-subtitle">Discover the world of cheese through AI</p>'
README_86_95 = excerpt(f"{V1}/README.md", 86, 95).split("\n")
assert README_86_95[2] == "```" and README_86_95[3] == "<body>" and README_86_95[8] == "</body>", README_86_95

EMOJI = "🧀"                    # drawn pages and cards drop it (the fonts here have no mono emoji)
HERO = "Formaggio.me is here!"            # a21:6, the h1 (without its emoji)
SUB = "Discover the world of cheese through AI"   # index.html:44 (a23:18)
NEW = "This is a placeholder for the awesome cheese identification app"   # a23:20, a24:3
assert HERO in A21.line(6) and SUB in A23.line(18) and NEW in A23.line(20)


def _readme_body() -> VGroup:
    """README.md 86–95 as the card shows it: the two instructions (markdown stripped) and the code
    block's six rows in mono with their indentation (the fence lines dropped, the emoji dropped)."""
    r = README_86_95
    rows = [label(md_plain(r[0]).lstrip("- "), 20, INK), label(md_plain(r[1]).lstrip("- "), 20, INK)]
    code_rows = [s.replace(EMOJI + " ", "") for s in r[3:9]]
    rows += [mono_line(s, 20, INK) for s in code_rows]
    g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    for m in g[2:]:                       # mono rows: the strut's left edge carries the indentation
        m.shift(RIGHT * (g[0].get_left()[0] - m.strut.get_left()[0]))
    return g


def _lang_card(name: str, role: str) -> VGroup:
    """One of beat 0's three cards: 'HTML' over 'structure'."""
    t = VGroup(label(name, 30, INK), label(role, 24, S.GREY)).arrange(DOWN, buff=0.12)
    fr = RoundedRectangle(width=3.4, height=t.height + 0.6, corner_radius=0.16, stroke_color=S.GREY,
                          stroke_width=3).set_fill(S.GREY_DARKER, 1)
    t.move_to(fr)
    return VGroup(fr, t)


def _strut_row(t: Terminal, text: str):
    """The terminal row (on screen now) whose text is exactly `text`."""
    for ln in t.lines:
        if getattr(ln, "text", None) == text:
            return ln
    raise KeyError(text)


def mark_extra(scene, t: Terminal, line):
    """PLAYS: the row tag 'extra' beside a typed command, or on the terminal's title bar when the
    command's last row leaves no room (then it rides the bar until replaced). Returns the tag."""
    tg = beside(extra_row(), line, buff=0.4)
    if tg.get_right()[0] <= t.box.get_right()[0] - 0.1:
        clear_bar(scene, t)
        pin(scene, line, tg)
        return tg
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


def clear_bar(scene, t: Terminal):
    """PLAYS: the title-bar tag (if any) leaves."""
    old = getattr(t, "bar_tag", None)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), run_time=0.3)
        t.bar_tag = None


class StaticPages(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S05"] == 9, len(SAY)

        # ========================================================== 0. HTML, CSS, JavaScript; index.html links all three
        ref0 = lref("16–17 (Frontend)")
        page = browser_icon(2.2, name="a page", size=22).move_to([0, 0.5, 0])
        cards = [_lang_card("HTML", "structure"), _lang_card("CSS", "style"), _lang_card("JavaScript", "behavior")]
        for c, x in zip(cards, (-4.2, -0.2, 3.8)):
            c.move_to([x, 0.6, 0])
        badge = tool_chip("the only programming language of the three", mono_font=False)
        badge.next_to(cards[2], DOWN, buff=0.25)
        badge.shift(LEFT * max(0.0, badge.get_right()[0] - 6.45))
        assert badge.get_right()[0] < SAFE_X - 0.05, badge.get_right()
        p1 = code(HTML, 4, 12, font_size=20, shown="frontend-simple/index.html",
                  cuts={6: '<meta name="viewport"', 7: '<meta http-equiv="Cache-Control"'})
        p2 = code(HTML, 74, 75, font_size=20, shown="frontend-simple/index.html")
        p1.move_to([-6.45 + p1.width / 2, 2.8 - p1.height / 2, 0])
        p2.next_to(p1, DOWN, buff=0.3).align_to(p1, LEFT)
        assert p2.get_bottom()[1] > -3.55, p2.get_bottom()
        assert p1.get_right()[0] < ref0.get_left()[0] - 0.1 or p1.get_top()[1] < ref0.get_bottom()[1] - 0.05
        spans = [code_span(p1.code, 6, "<title>Formaggio.me</title>"),
                 code_span(p1.code, 7, '<link rel="stylesheet" href="styles.css">'),
                 code_span(p2.code, 0, '<script src="main.js"></script>')]
        rings = [ring(s, S.GREY, buff=0.06) for s in spans]
        chip_x = max(p1.get_right()[0], p2.get_right()[0]) + 0.35
        chips = [grey_chip(s, 22) for s in ("HTML", "CSS", "JavaScript")]
        for c, s in zip(chips, spans):
            c.move_to([chip_x + c.width / 2, s.get_y(), 0])
        chips[1].shift(RIGHT * (chips[0].width + 0.35))          # CSS beside HTML: the rows are 0.37 apart
        ties = [DashedLine(r.get_right(), c.get_left(), color=S.GREY, stroke_width=2, dash_length=0.08)
                for r, c in zip(rings, chips)]
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref0), run_time=0.4)
            vo.wait_until("a page")
            self.play(FadeIn(page, scale=0.9), run_time=0.6)
            vo.wait_until("The lecture splits a page")
            self.play(page.animate.scale(1.08), rate_func=there_and_back, run_time=0.6)
            for i, (c, cue) in enumerate(zip(cards, ("HTML for structure", "CSS for style",
                                                     "and JavaScript for behavior"))):
                vo.wait_until(cue)
                gone = [FadeOut(page, scale=1.1)] if i == 0 else []
                self.play(FadeIn(c, shift=UP * 0.25, scale=0.8), *gone, run_time=0.6)
            self.play(FadeIn(badge, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(badge.text, color=TOOL, scale_factor=1.06), run_time=0.6)
            vo.wait_until("In version 1")
            self.play(FadeOut(badge), run_time=0.3)
            self.play(FadeIn(p1, shift=RIGHT * 0.2), FadeIn(p2, shift=RIGHT * 0.2),
                      *[ReplacementTransform(c, ch) for c, ch in zip(cards, chips)], run_time=1.0)
            vo.wait_until("links all three")
            for r, tie in zip(rings, ties):
                self.play(Create(r), Create(tie), run_time=0.45)

        # ========================================================== 1. step 1: the README's path misses src again
        trk = tracker_f(1)
        t = term(P_LAPTOP, rows=9, title=T_NEW, size=20)
        card1 = readme_card(75, readme_lines(75, 75, V1), size=20, name=f"{V1}/README.md")
        card1.move_to([-6.45 + card1.width / 2, t.box.get_top()[1] + 0.3 + card1.height / 2, 0])
        assert card1.get_top()[1] < TRACK_BOTTOM - 0.1 and card1.get_right()[0] < SAFE_X, card1.get_corner(UR)
        slip = erratum_tag("erratum · add src/")
        slip.move_to(card1.frame.get_corner(UR) + np.array([-slip.width / 2 - 0.2, 0, 0]))
        card2 = readme_card((78, 82), readme_lines(78, 82, V1), size=20, name=f"{V1}/README.md")
        card2.move_to([-6.45 + card2.width / 2, t.box.get_top()[1] + 0.3 + card2.height / 2, 0])
        assert card2.get_top()[1] < TRACK_BOTTOM - 0.1 and card2.get_right()[0] < SAFE_X, card2.get_corner(UR)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(p1, p2, *chips, *rings, *ties)), FadeOut(ref0), run_time=0.5)
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t), run_time=0.5)
            self.play(FadeIn(card1, shift=DOWN * 0.15), run_time=0.5)
            type_capture(self, t, A19, type_time=0.8)
            out(self, t, [(A19.line(2), ERR)], wrap=True, run_time=0.4)
            vo.wait_until("Same slip")
            self.play(FadeIn(slip, scale=0.9), track(trk, 1, extra=True),
                      Indicate(card1.body, color=ERR, scale_factor=1.03), run_time=0.6)
            ln2 = type_capture(self, t, A20, type_time=0.8)[0]
            mark_extra(self, t, ln2)
            out(self, t, A20.at((2, 7)), run_time=0.5)
            self.add(t)

        # ========================================================== 2. steps 2 and 3: docker-shell.sh, http-server
        build = [(cut(A20B.line(3), "FINISHED"), S.GREY), "…",
                 cut(A20B.line(28), "cheese-app-frontend-simple:latest"),
                 cut(A20B.line(29), "cheese-app-frontend-simple:latest")]
        # the picture above the terminal: the laptop's door 8080 piped to the container's door 8080
        lapf = RoundedRectangle(width=6.6, height=1.85, corner_radius=0.14, stroke_color=LAPTOP,
                                stroke_width=3).set_fill(S.BG, 1).move_to([2.95, 1.75, 0])
        lapt = label("your laptop", 20, LAPTOP).next_to(lapf.get_corner(UR), DL, buff=0.1)
        cb = cbox(("cheese-app-", "frontend-simple"), 3.4, 0.84).move_to([4.15, 1.45, 0])
        d_out = door("8080").move_to([lapf.get_left()[0], cb.get_y(), 0])
        d_in = door("8080", color=CONTAINER).next_to(cb, LEFT, buff=0)
        pipe = Line(d_out.get_right(), d_in.get_left(), color=ROUTE, stroke_width=6)
        assert pipe.get_length() > 0.5, pipe.get_length()
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(slip), ReplacementTransform(card1, card2), track(trk, 2), run_time=0.6)
            cd_prompt(self, t, P_V1_FRONT)
            vo.wait_until("pause")
            turn = on_bar(t, turn_row())
            self.play(FadeIn(turn, shift=LEFT * 0.1), run_time=0.4)
            t.add(turn)
            vo.wait_until("run sh docker-shell.sh")
            type_capture(self, t, A20B, type_time=0.6)
            out(self, t, build, run_time=0.5)
            vo.wait_until("then http-server")
            self.play(track(trk, 3), run_time=0.4)
            type_at(self, t, A20B, 30, type_time=0.5)
            vo.wait_until("It serves this folder")
            out(self, t, A20B.at(31, 33), run_time=0.4)
            vo.wait_until("with a one-hour cache")
            out(self, t, [(A20B.line(37), TURN)], run_time=0.4)
            vo.wait_until("The addresses it prints")
            addr = out(self, t, A20B.at((45, 47)), run_time=0.5)
            br = Brace(VGroup(addr[1], addr[2]), RIGHT, color=S.GREY, buff=0.15)
            br_t = label("container addresses", 20, S.GREY).next_to(br, RIGHT, buff=0.12)
            self.play(GrowFromCenter(br), FadeIn(br_t), run_time=0.5)
            vo.wait_until("your laptop uses 8080")
            assert lapf.get_bottom()[1] > t.box.get_top()[1] + 0.05, (lapf.get_bottom(), t.box.get_top())
            self.play(FadeOut(card2), FadeIn(VGroup(lapf, lapt)), FadeIn(cb), FadeIn(d_in), run_time=0.5)
            self.play(FadeIn(d_out, scale=1.3), Create(pipe), run_time=0.7)
            self.play(Indicate(d_out, color=TURN, scale_factor=1.15), run_time=0.6)

        # ========================================================== 3. step 4: the lecture's first trip: a file comes back
        ref1 = lref("18–23 (Frontend)")
        tr = RequestTrace("localhost:8080", rows=("front",), front="simple", cable=False,
                          browser_w=4.0).shift(UP * 0.84)
        net = tr.net
        fbox = net.boxes["front"]
        ill = illustration_tag().next_to(tr.browser, UP, buff=0.03).align_to(tr.browser, LEFT)
        assert ill.get_top()[1] < TRACK_BOTTOM - 0.05, ill.get_top()
        files = VGroup(*[file_icon(n, OWN) for n in ("index.html", "main.js", "styles.css")])
        files.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        folder = RoundedRectangle(width=files.width + 0.5, height=files.height + 0.75, corner_radius=0.1,
                                  stroke_color=CONTAINER, stroke_width=2.5).set_fill(tint(CONTAINER), 1)
        folder.next_to(fbox, DOWN, buff=0.3).align_to(fbox, RIGHT).shift(LEFT * 0.15)
        f_t = mono("/app", 20, CONTAINER).move_to(folder.get_top() + DOWN * 0.22).align_to(folder, LEFT).shift(RIGHT * 0.2)
        files.next_to(f_t, DOWN, buff=0.14, aligned_edge=LEFT)
        f_tie = Line(net.inner["front"].get_bottom(), folder.get_top(), color=CONTAINER, stroke_width=3)
        app_dir = VGroup(f_tie, folder, f_t, files)
        assert folder.get_bottom()[1] > net.frame.get_bottom()[1] + 0.1, (folder.get_bottom(), net.frame.get_bottom())
        turn4 = your_turn().next_to(ill, RIGHT, buff=0.2)
        tab = term(P_LAPTOP, rows=4, title=T_TAB, size=20)
        assert tab.box.get_top()[1] < net.frame.get_bottom()[1] - 0.01, (tab.box.get_top(), net.frame.get_bottom())
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(t, br, br_t, lapf, lapt, cb, d_in, d_out, pipe)), track(trk, 4), run_time=0.6)
            self.play(FadeIn(tr), FadeIn(ill), FadeIn(ref1), run_time=0.7)
            tr.show(self, *app_dir, anims=[Create(f_tie), FadeIn(folder), FadeIn(f_t),
                                           LaggedStart(*[FadeIn(f, shift=DOWN * 0.1) for f in files], lag_ratio=0.2)],
                    run_time=0.8)
            vo.wait_until("open localhost 8080")
            self.play(Indicate(tr.browser.address, color=ROUTE, scale_factor=1.15), run_time=0.6)
            tr.heal(self)
            vo.wait_until("the lecture's first trip")
            tr.hop(self, 1, "front", run_time=0.6)
            tr.hop(self, 2, "front", run_time=0.6)
            tr.hop(self, 3, "front", run_time=0.6)
            vo.wait_until("the request reaches http-server")
            tr.hop(self, 4, "front", run_time=0.7)
            ghost = label("4 the function runs · S03, the API", 20, S.GREY)
            ghost.move_to(tr.caption.get_center() + DOWN * 0.5)
            self.play(TransformFromCopy(tr.caption, ghost), run_time=0.5)
            tr.set_caption(self, "4 a file is read", run_time=0.5)
            self.play(Indicate(files[0], color=TURN, scale_factor=1.15), run_time=0.6)
            tr.heal(self)
            vo.wait_until("a file comes back")
            arr5 = tr.hop(self, 5, "front", run_time=0.7)
            fly = file_icon(None, OWN).move_to(files[0].glyph)     # the glyph only: a label would cross hop 5's circle
            self.add(fly)
            self.play(fly.animate.move_to(arr5.get_start()), run_time=0.5)
            self.play(MoveAlongPath(fly, arr5.copy()), run_time=0.8)
            vo.wait_until("and the browser draws it")
            self.play(FadeOut(fly, scale=0.6, target_position=tr.browser.at(0, 0)), run_time=0.3)
            self.remove(fly)
            gap = Rectangle(width=0.1, height=0.3, stroke_width=0, fill_opacity=0)
            tr.browser.fill(self, [gap, label(HERO, 24, INK), label("Discover the world of cheese", 20, S.GREY),
                                   label("through AI", 20, S.GREY)])
            tr.hop(self, 6, run_time=0.6)
            vo.wait_until("Pause and open it")
            self.play(FadeIn(turn4, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, turn4, TURN)
        # the same request from a terminal (extra), after the voice: the viewer has paused here
        tr.clear_hops(self, run_time=0.4)
        self.play(FadeOut(ghost), FadeIn(tab, shift=UP * 0.2), run_time=0.5)
        ln21 = type_capture(self, tab, A21, type_time=1.0)[0]
        mark_extra(self, tab, ln21)
        o21 = out(self, tab, [(A21.line(2), OWN), A21.line(3)], run_time=0.4)
        self.play(substring(o21[1], "max-age=3600").animate.set_color(TURN), run_time=0.4)
        self.add(tab)
        self.wait(0.5)
        out(self, tab, A21.at((4, 7)), run_time=0.5)
        self.wait(0.4)

        # ========================================================== 4. extra: main.js holds sample data; part 2 adds the API
        d9 = door("9000", color=S.GREY)
        d9.move_to([net.wall_x(), net.p(0, 0)[1] - 0.2, 0])
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(turn4), track(trk, 4, extra=True), run_time=0.4)
            ln22 = type_capture(self, tab, A22, type_time=0.9)[0]
            mark_extra(self, tab, ln22)
            vo.wait_until("the podcasts are sample data")
            out(self, tab, [(A22.line(2), TURN), A22.line(3)], run_time=0.5)
            vo.wait_until("Part 2 adds")
            out(self, tab, [A22.line(4)], run_time=0.3)
            start = tr.browser.at(0.55, -0.45)
            a9 = DashedVMobject(Arrow(start, d9.get_left() + LEFT * 0.03, buff=0.04, color=S.GREY, stroke_width=4,
                                      tip_length=0.18, max_tip_length_to_length_ratio=0.35),
                                num_dashes=9).set_stroke(S.GREY, 4)
            q9 = label("?", 26, S.GREY).next_to(d9, RIGHT, buff=0.18)      # clear of the wall line
            p2c = dashed_chip("part 2").next_to(q9, RIGHT, buff=0.22)
            assert p2c.get_right()[0] < folder.get_left()[0] - 0.1, (p2c.get_right(), folder.get_left())
            tr.show(self, d9, a9, q9, p2c, anims=[FadeIn(d9), Create(a9), FadeIn(q9), FadeIn(p2c)], run_time=0.9)

        # ========================================================== 5. step 5: add only the paragraph
        body = _readme_body()
        card5 = readme_card((86, 95), body, name=f"{V1}/README.md")
        card5.move_to([-6.45 + card5.width / 2, 2.75 - card5.height / 2, 0])
        etag = erratum_tag().move_to(card5.frame.get_corner(UR) + LEFT * 0.9)
        bad_rows = [body[2], body[3], body[7]]
        good_rows = [body[4], body[5], body[6]]
        enote = row_tag("an old whole body · would drop the page and its script tag", ERR)
        enote.next_to(body[7], RIGHT, buff=0.5)            # beside '</body>' (the rows above it are short)
        assert enote.get_left()[0] > body[6].get_right()[0] + 0.2 and enote.get_right()[0] < card5.get_right()[0]
        ed = editor_chip()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(tr), FadeOut(ill), FadeOut(ref1), track(trk, 5), run_time=0.6)
            resize(self, tab, 3, run_time=0.5)
            assert card5.get_bottom()[1] > tab.box.get_top()[1] + 0.05, (card5.get_bottom(), tab.box.get_top())
            assert card5.get_right()[0] < SAFE_X and card5.get_top()[1] < TRACK_BOTTOM, card5.get_corner(UR)
            vo.wait_until("add a paragraph")
            self.play(FadeIn(card5, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("A small note")
            self.play(FadeIn(etag, scale=0.9), run_time=0.4)
            vo.wait_until("is an old whole body")
            self.play(*[r.animate.set_color(ERR) for r in bad_rows], run_time=0.6)
            vo.wait_until("and pasting it would drop")
            self.play(FadeIn(enote, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Add only the paragraph")
            self.play(*[r.animate.set_color(OWN) for r in good_rows], run_time=0.5)
            self.play(Indicate(VGroup(*good_rows), color=OWN, scale_factor=1.04), run_time=0.6)
            self.play(FadeOut(VGroup(card5, etag, enote)), run_time=0.4)
            resize(self, tab, 13, run_time=0.6)
            under_term(tab, ed)
            self.play(FadeIn(ed, shift=DOWN * 0.1), run_time=0.4)
            ln23 = type_capture(self, tab, A23, type_time=1.0)[0]
            mark_extra(self, tab, ln23)
            diff = [(s, OWN) if s.startswith("+") and not s.startswith("+++") else s
                    for s in A23.at((15, 23))]
            out(self, tab, diff, wrap=True, run_time=0.7)
            self.add(tab)
            assert ed.get_bottom()[1] > tab.box.get_top()[1] and ed.get_top()[1] < TRACK_BOTTOM, ed.get_top()
            self.wait(0.4)

        # ========================================================== 6. step 6: refresh; main.js may need a hard refresh
        bw = Browser("localhost:8080", win_w=6.4, win_h=2.85)
        bw.move_to([-6.45 + bw.win_w / 2 + 2.2, 2.75 - 2.85 / 2, 0])
        ill6 = illustration_tag().next_to(bw.frame, LEFT, buff=0.15).align_to(bw.frame, UP)
        hero = [label(HERO, 24, INK), label(SUB, 20, S.GREY)]
        new_rows = [label("This is a placeholder for the awesome", 20, TURN),
                    label("cheese identification app", 20, TURN)]
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(ed), track(trk, 6), run_time=0.4)
            resize(self, tab, 6, run_time=0.5)
            assert bw.frame.get_bottom()[1] > tab.box.get_top()[1] + 0.05, (bw.frame.get_bottom(), tab.box.get_top())
            self.play(FadeIn(bw), FadeIn(ill6), run_time=0.5)
            bw.fill(self, hero, run_time=0.4)
            vo.wait_until("refresh")
            bw.reload(self, run_time=0.6)
            rows = bw._rows(hero + new_rows, False, INK, 0.14)
            for m, ref in zip(new_rows, rows[2:]):
                m.move_to(ref)
            bw.show(self, *new_rows, anims=[FadeIn(m, shift=DOWN * 0.1) for m in new_rows], into=bw.rows,
                    run_time=0.5)
            ln24 = type_capture(self, tab, A24, type_time=0.9)[0]
            mark_extra(self, tab, ln24)
            out(self, tab, [A24.line(2), (A24.line(3), TURN), A24.line(4)], wrap=True, run_time=0.5)
            self.play(*[m.animate.set_color(INK) for m in new_rows], run_time=0.4)
            vo.wait_until("Edits to main dot js")
            ln25 = type_capture(self, tab, A25, type_time=0.9)[0]
            mark_extra(self, tab, ln25)
            o25 = out(self, tab, A25.at(2, 3), run_time=0.4)
            vo.wait_until("because http-server lets the browser")
            self.play(substring(o25[1], "max-age=3600").animate.set_color(TURN), run_time=0.4)
            self.add(tab)
            hard = row_tag("hard refresh · or http-server -c-1")
            pin(self, o25[1], beside(hard, o25[1], buff=0.5))
            flash_tag(self, hard, S.GREY)
            self.add(tab)

        # ========================================================== 7. clean up: stop both, the list is empty
        trk2 = tracker_c1(1, extra=True)
        check = grey_chip("check: both still running")
        rm_chip = grey_chip("--rm: they removed themselves")
        with self.voiceover(SAY[7]) as vo:
            gone_lines = list(tab.lines)
            for m in gone_lines:
                tab.lines.remove(m)
            swap_tracker(self, trk, trk2, FadeOut(bw), FadeOut(ill6), FadeOut(VGroup(*gone_lines)))
            self.remove(*gone_lines)
            trk = trk2
            resize(self, tab, 7, run_time=0.4)
            ln26 = type_capture(self, tab, A26, type_time=0.45)
            mark_extra(self, tab, ln26[0])
            o26 = out(self, tab, A26.at((2, 4)), wrap=True, run_time=0.3)
            under_term(tab, check)
            self.play(FadeIn(check, shift=DOWN * 0.1), run_time=0.3)
            # the two servers' own terminals, one after the other, above the tab, each held ~2 s
            vo.wait_until("press Control C")
            self.play(track(trk, 2), run_time=0.4)
            prev = None          # two stacked 3-row strips do not fit above the tab: one after the other,
            for k, (title, cap, lines_a, n_exit, last) in enumerate(((T_LAPTOP, A03, [62], 69, 70),
                                                                     (T_NEW, A20B, [57, 58], 60, 61))):
                s = term(container_prompt(cap, n_exit), rows=3, title=title, size=20, place=False)
                s.shift(np.array([0, check.get_top()[1] + 0.12 - s.box.get_bottom()[1], 0]))
                assert s.box.get_bottom()[1] > check.get_top()[1] + 0.05 and s.box.get_top()[1] < TRACK_BOTTOM - 0.05
                gone = [FadeOut(prev, shift=UP * 0.15)] if prev is not None else []
                self.play(FadeIn(s, shift=DOWN * 0.15), *gone, run_time=0.3)
                out(self, s, [(cap.line(n), ERR if cap.line(n) == "^C" else OUTPUT) for n in lines_a],
                    run_time=0.25)
                type_at(self, s, cap, n_exit, type_time=0.25)
                out(self, s, [cap.line(last)], run_time=0.25)
                self.wait(1.0 if k == 0 else 0.8)      # each held ~2 s: the follow-along action is readable
                prev = s
            vo.wait_until("The container list is then empty")
            self.play(FadeOut(prev, shift=UP * 0.15), run_time=0.3)
            clear_bar(self, tab)
            type_capture(self, tab, A30, type_time=0.6)
            hdr = out(self, tab, A30.at(2), run_time=0.4)[0]
            data = [m for m in o26 if m in tab.lines.submobjects]
            for m in data:
                tab.lines.remove(m)
            self.play(*[m.animate.move_to(hdr).set_opacity(0) for m in data], run_time=0.7)
            self.remove(*data)
            self.play(*[ln.animate.shift(tab._slot(i) - ln.strut.get_corner(UL))
                        for i, ln in enumerate(tab.lines)], run_time=0.4)
            self.add(tab)
            self.play(ReplacementTransform(check, rm_chip.move_to(check).align_to(check, RIGHT)), run_time=0.5)
            self.add(tab)
            flash_tag(self, rm_chip, S.GREY)
            self.wait(0.6)

        # ========================================================== 8. prune, then what stays
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(rm_chip), track(trk, 3), run_time=0.4)
            resize(self, tab, 10, run_time=0.5)
            type_capture(self, tab, A31, type_time=0.6)
            o31 = out(self, tab, A31.at((2, 8)), run_time=0.5)
            self.play(substring(o31[-1], "[y/N] y").animate.set_color(TURN), run_time=0.4)
            self.add(tab)
            out(self, tab, [A31.line(9), "…", A31.line(17)], run_time=0.4)
            vo.wait_until("the image list")
            self.play(track(trk, 4), run_time=0.4)
            type_capture(self, tab, A32, type_time=0.5)
            out(self, tab, [cut(A32.line(n), "DISK USAGE" if n == 2 else "MB") for n in range(2, 9)], run_time=0.6)
            self.wait(0.8)

        self.play(FadeOut(tab), FadeOut(trk), run_time=0.7)
        self.remove(*self.mobjects)
        self.wait(0.3)
