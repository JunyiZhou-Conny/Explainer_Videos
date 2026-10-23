"""S02 · One laptop, three containers, one cloud — the running map (V6) built piece by piece.

Beats (script.md, ## S02; one voiceover block each):
0. Tracker A (step 1) appears; GREY `Lecture 10 · slides 5–6, 11` for the whole scene. The map is
   built piece by piece: the laptop frame ('your laptop') with its inner wall; the loopback loop
   'localhost · 127.0.0.1'; the two streets as GREY dashed outlines with a GREY 'planned' note
   under each; the hollow TEAL houses (chroma + loader on llm-rag-network, API and frontend on
   cheese-app-network: the map's four houses, S01's decision); a brief light-up shows what lighting
   means, then they go hollow again (nothing runs yet).
1. The browser on the laptop floor; the public street and the BLUE Google building, its IAM guard
   flashes. Calls draw in: loader → Google, loader → chroma; API → Google; browser → frontend, API,
   chroma (PINK, to the wall gaps where the doors will be). No API ↔ chroma arrow: under the map a
   GREY struck chip 'API ↔ chroma' and README.md · line 127's own words.
2. The map leaves; a full-width laptop terminal (20 pt: see beat 3) under a README card (lines 43–44:
   the narration names both prerequisites) with the GREY note 'no address given; this is the repo'.
   `git clone …` → laptop/01:2; `cd cheese-app-v0` → the prompt becomes ~/cheese-app-v0. GREY chip
   on the title bar 'Docker 29.8.2 · at the time of recording' (laptop/00:4). ▶ your turn.
3. The terminal shrinks to a 3-row strip and the map returns above it. Tracker gains ' · extra'.
   `git log -1 --format='%H %ci'` → laptop/02:2 (hash, then date ringed); `ls -la` → laptop/03:2–11
   (whitespace re-aligned only: the capture's rows are 76 wide); llm-rag, api-service,
   frontend-ai-chatbot are ringed in turn and a TEAL chip flies from each to its house(s).
4. The strip leaves; under the map an erratum card: a GREY dashed miniature 'cloud machine' with a
   'web server' house, crossed out; caption 'the app's home page animates the hosted version · its
   deployment/ folder was deleted in 2bc29dd'. The local map above flashes; fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, IMAGE, INK, MONO, NARRATION, P_LAPTOP_HOME, P_REPO, ROUTE, SAY_COUNT, TURN,
                    AppMap, beside, capture, cd_prompt, chip, each, erratum_tag, extra_row, flash_tag, house,
                    label, lref, mono, note, on_bar, out, outline_box, pin, readme, readme_card, resize, ring,
                    row_tag, strike, substring, term, track, tracker, turn_row, type_cmd)
from explainer import style as S

SAY = NARRATION["S02"]
TERM_PT = 20          # laptop/03's rows are 76 characters; even re-aligned (67) they need 20 pt (72 a row)


def realign(lines: list[str]) -> list[str]:
    """`ls -la` rows with their whitespace re-aligned (one-space gutters, numbers right-justified);
    the words are unchanged (asserted). 'total 56' stays as it is."""
    rows = [ln.split() for ln in lines]
    table = [r for r in rows if len(r) == 9]
    w = [max(len(r[j]) for r in table) for j in range(9)]
    right = {1, 4, 6}                                   # links, size, day
    out_ = []
    for ln, r in zip(lines, rows):
        if len(r) != 9:
            out_.append(ln)
            continue
        cells = [r[j].rjust(w[j]) if j in right else r[j].ljust(w[j]) for j in range(8)] + [r[8]]
        s = " ".join(cells)
        assert s.split() == ln.split(), (s, ln)
        out_.append(s)
    return out_


def hosted_mini() -> VGroup:
    """The deleted hosted setup as a GREY dashed miniature: a web-server house on a cloud machine
    (the frame), named underneath so the cross never covers the words."""
    frame = outline_box(2.2, 1.0, S.GREY, solid=False)
    srv = house(None, 1.0, 0.62, color=S.GREY, dashed=True)
    srv.move_to(frame.get_bottom() + UP * 0.16, aligned_edge=DOWN)
    cap = label("a web server on a cloud machine", 20, S.GREY).next_to(frame, DOWN, buff=0.12)
    g = VGroup(frame, srv, cap)
    g.frame, g.cap, g.server = frame, cap, srv
    return g


class TheMap(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S02"] == 5, len(SAY)

        tr = tracker("A", 1)
        ref = lref("5–6, 11")

        # ========================================================== 0. the laptop, its streets, its houses
        m = AppMap.at("S02")
        streets = [m.streets["llm-rag"], m.streets["cheese-app"]]
        planned = VGroup(*[note("planned").move_to([st.band.get_right()[0] - 0.75, 0.47, 0]) for st in streets])
        hs = m.houses

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.8)
            vo.wait_until("First, the map")
            self.play(Create(m.frame), FadeIn(m.header), run_time=1.0)
            self.play(Create(m.wall), run_time=0.6)
            vo.wait_until("Your laptop is one house")
            self.play(Indicate(m.header, color=INK, scale_factor=1.2), run_time=0.8)
            vo.wait_until("every house has its own loopback")
            self.play(Create(m.loop[0]), FadeIn(m.loop[1], shift=RIGHT * 0.15), run_time=0.8)
            vo.wait_until("which always means this machine")
            self.play(Indicate(m.loop[1], color=INK, scale_factor=1.12), run_time=0.8)
            vo.wait_until("Docker lays two private streets")
            self.play(*[Create(st.band) for st in streets], run_time=0.9)
            vo.wait_until("one per network")
            self.play(*[FadeIn(VGroup(st.mask, st.text)) for st in streets], run_time=0.6)
            self.play(FadeIn(planned, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the vector database")
            self.play(FadeIn(hs["chroma"], shift=DOWN * 0.2), FadeIn(hs["loader"], shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("the API server")
            self.play(FadeIn(hs["api"], shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("and the web frontend")
            self.play(FadeIn(hs["frontend"], shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("Each house lights up")
            self.play(LaggedStart(*[m.light(k) for k in ("chroma", "loader", "frontend", "api")], lag_ratio=0.25),
                      run_time=1.2)
            self.play(LaggedStart(*[m.darken(k) for k in ("chroma", "loader", "frontend", "api")], lag_ratio=0.15),
                      run_time=0.9)

        # ========================================================== 1. browser, Google, who calls whom
        calls_l = [m.call("loader", "google"), m.call("loader", "chroma")]
        call_a = m.call("api", "google")
        calls_b = [m.call("browser", k) for k in ("frontend", "api", "chroma")]
        no_arrow = chip("API ↔ chroma", S.GREY, size=22, text_color=S.GREY, font=MONO)
        cross = strike(no_arrow.text, S.GREY, stroke=4)
        q127 = readme(127)
        words = "it does not connect to ChromaDB."
        assert words in q127, q127
        rc = readme_card(127, label(f"“… {words}”", 24, INK), quote=True)
        quote_row = VGroup(VGroup(no_arrow, cross), rc).arrange(RIGHT, buff=0.5).move_to([-0.9, -2.35, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(planned), FadeIn(m.browser, shift=UP * 0.3), run_time=0.8)
            vo.wait_until("outside every street")
            self.play(Indicate(m.browser.text, color=INK, scale_factor=1.2), run_time=0.8)
            vo.wait_until("Across the public street")
            self.play(FadeIn(m.public), run_time=0.6)
            self.play(FadeIn(m.google, shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("with a guarded door")
            self.play(Indicate(m.google.guard[1], color=CLOUD, scale_factor=1.3),
                      Indicate(m.google.door, color=CLOUD, scale_factor=1.2), run_time=0.8)
            vo.wait_until("Now, who calls whom?")
            self.play(each([hs[k].text for k in ("chroma", "loader", "frontend", "api")] + [m.browser.text],
                           TURN, scale=1.15, lag=0.12), run_time=1.0)
            vo.wait_until("The loader calls Google")
            self.play(Create(calls_l[0]), run_time=0.9)
            vo.wait_until("and the database")
            self.play(Create(calls_l[1]), run_time=0.6)
            vo.wait_until("The API calls Google")
            self.play(Create(call_a), run_time=0.8)
            vo.wait_until("Your browser calls everything else")
            self.play(LaggedStart(*[Create(c) for c in calls_b], lag_ratio=0.3), run_time=1.2)
            vo.wait_until("And the API never talks")
            self.play(Indicate(hs["api"].text, color=INK, scale_factor=1.25),
                      Indicate(hs["chroma"].text, color=INK, scale_factor=1.25), run_time=0.8)
            self.play(FadeIn(no_arrow, shift=UP * 0.15), run_time=0.5)
            self.play(Create(cross), run_time=0.4)
            vo.wait_until("the README says so itself")
            self.play(FadeIn(rc, shift=LEFT * 0.2), run_time=0.6)
            self.play(Indicate(rc.body, color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("Part 2 shows why")
            self.play(each([c.line for c in calls_b] + [m.browser.text], ROUTE, scale=1.12, lag=0.15), run_time=1.0)

        # ========================================================== 2. time to type: the clone
        shown_map = VGroup(m.frame, m.header, m.wall, m.loop, *streets, *hs.values(), m.browser, m.public,
                           m.google, *calls_l, call_a, *calls_b)
        t = term(P_LAPTOP_HOME, rows=5, size=TERM_PT)
        card43 = readme_card((43, 44), "\n".join(readme(n).lstrip("- ") for n in (43, 44)))
        card43.move_to([0, 1.1, 0])
        noaddr = note("no address given; this is the repo").next_to(card43, DOWN, buff=0.22).align_to(card43, LEFT)
        ver = capture("00").line(4)
        assert ver.startswith("Docker client 29.8.2"), ver
        dk = on_bar(t, row_tag(f"Docker {ver.split()[2].rstrip(',')} · at the time of recording"))
        clone = capture("01")

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(shown_map, quote_row)), run_time=0.7)
            self.remove(shown_map, quote_row)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("The README's prerequisites")
            self.play(FadeIn(card43, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("have Docker installed")
            self.play(Indicate(card43.body[0], color=INK, scale_factor=1.06), FadeIn(dk, shift=LEFT * 0.15),
                      run_time=0.8)
            vo.wait_until("and clone this repository")
            self.play(Indicate(card43.body[1], color=INK, scale_factor=1.06), run_time=0.8)
            vo.wait_until("The README gives no address")
            self.play(FadeIn(noaddr, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("so here is the repo's address")
            type_cmd(self, t, clone.cmd, type_time=1.4)
            got = out(self, t, clone.at(2))
            yt = beside(turn_row(), got[0])
            pin(self, got[0], yt)
            vo.wait_until("Pause, and clone it")
            flash_tag(self, yt, TURN)
            type_cmd(self, t, "cd cheese-app-v0", type_time=0.6)
            cd_prompt(self, t, P_REPO)

        # ========================================================== 3. extras: the commit, one folder per house
        m2 = AppMap.at("S02")
        log, ls = capture("02"), capture("03")
        assert log.cmd == "git log -1 --format='%H %ci'" and ls.cmd == "ls -la", (log.cmd, ls.cmd)
        xt = extra_row()
        listing = realign(ls.at((2, 11)))
        targets = {"llm-rag": (("chroma", "loader"), (hs["chroma"].get_center()[0] + hs["loader"].get_center()[0]) / 2),
                   "api-service": (("api",), hs["api"].get_center()[0]),
                   "frontend-ai-chatbot": (("frontend",), hs["frontend"].get_center()[0])}
        chip_y = 2.12

        def fly(name):
            """Ring the folder's name in its row, fly a TEAL chip from it to its house(s)."""
            g = substring(t.find(name), name)
            rg = ring(g, IMAGE)
            keys, x = targets[name]
            c = chip(name, IMAGE, size=20, font=MONO).move_to(g)
            self.play(Create(rg), run_time=0.35)
            self.play(FadeIn(c, scale=1.1), run_time=0.25)
            self.play(c.animate.move_to([x, chip_y, 0]), run_time=0.8)
            self.play(*[Indicate(m2.houses[k].text, color=INK, scale_factor=1.25) for k in keys],
                      FadeOut(c, shift=DOWN * 0.25), FadeOut(rg), run_time=0.7)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(card43, noaddr, dk)), run_time=0.5)
            self.remove(card43, noaddr, dk)
            resize(self, t, 3, extra=(FadeIn(m2),))
            on_bar(t, xt)                                   # the bar has moved: place the tag now
            self.play(track(tr, extra=True), FadeIn(xt, shift=LEFT * 0.1), run_time=0.5)
            type_cmd(self, t, log.cmd, type_time=0.9)
            got = out(self, t, log.at(2))
            row = got[0]
            vo.wait_until("the commit this video uses")
            r_hash = ring(substring(row, log.at(2)[0].split()[0]), TURN)
            self.play(Create(r_hash), run_time=0.5)
            vo.wait_until("from October 8th")
            r_date = ring(substring(row, "2026-10-08"), TURN)
            self.play(ReplacementTransform(r_hash, r_date), run_time=0.5)
            vo.wait_until("if yours is newer")
            self.play(FadeOut(r_date), run_time=0.3)
            self.remove(r_date)
            type_cmd(self, t, ls.cmd, type_time=0.4)
            out(self, t, listing, run_time=1.0, chunk=2)    # 2-row chunks: the strip never blanks
            vo.wait_until("shows llm-rag")
            fly("llm-rag")
            vo.wait_until("api-service")
            fly("api-service")
            vo.wait_until("frontend-ai-chatbot")
            fly("frontend-ai-chatbot")
            vo.wait_until("one folder per house")
            self.play(each([m2.houses[k].text for k in ("chroma", "loader", "frontend", "api")], IMAGE,
                           scale=1.2, lag=0.12), run_time=0.9)

        # ========================================================== 4. erratum: the hosted version is gone
        mini = hosted_mini()
        et = erratum_tag()
        l1 = label("the app's home page animates the hosted version", 22, INK)
        l2 = VGroup(label("its", 22, INK), mono("deployment/", 22, INK), label("folder was deleted in", 22, INK),
                    mono("2bc29dd", 22, INK)).arrange(RIGHT, buff=0.14)
        for w in l2:
            w.align_to(l2[0], DOWN)
        l2[1].shift(DOWN * 0.07)                        # 'p', 'y' descend: sit the word on the baseline
        text_col = VGroup(et, l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        body = VGroup(mini, text_col).arrange(RIGHT, buff=0.55)
        frame = RoundedRectangle(width=body.width + 0.7, height=body.height + 0.4, corner_radius=0.16,
                                 stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        frame.move_to([0, -2.45, 0])
        body.move_to(frame)
        x1 = Line(mini.frame.get_corner(UL), mini.frame.get_corner(DR), color=S.GREY, stroke_width=5)
        x2 = Line(mini.frame.get_corner(DL), mini.frame.get_corner(UR), color=S.GREY, stroke_width=5)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(t, xt)), track(tr, extra=False), run_time=0.6)
            self.remove(t, xt)
            vo.wait_until("One small gap")
            self.play(FadeIn(frame, shift=UP * 0.15), FadeIn(et), run_time=0.6)
            vo.wait_until("The app's own home page")
            self.play(FadeIn(l1, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("with a web server")
            self.play(Create(mini.frame), FadeIn(mini.cap), run_time=0.7)
            self.play(FadeIn(mini.server, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("The files for that setup")
            self.play(Create(x1), Create(x2), run_time=0.6)
            self.play(FadeIn(l2, shift=RIGHT * 0.15), run_time=0.6)
            flash_tag(self, et, INK)
            vo.wait_until("You are running the local version")
            self.play(m2.frame.animate(rate_func=there_and_back).set_stroke(TURN, 6),
                      Indicate(m2.header, color=TURN, scale_factor=1.2), run_time=1.0)
            vo.wait_until("this map draws exactly")
            self.play(each([m2.houses[k].text for k in ("chroma", "loader", "frontend", "api")] + [m2.browser.text],
                           INK, scale=1.15, lag=0.1), run_time=1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
