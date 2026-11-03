"""S10 · A name is not localhost (AC215 L10) — no tracker (every command is an extra);
`Lecture 10 · slides 5–6, 10` top right, whole scene.

Beats (script.md, ## S10; one voiceover block each):
0. V4 (TwoArrows): one Chroma box, two arrows in. A GREY `extra` tag top left on "every command in
   this scene is an extra". CODE(llm-rag/cli.py: 30–31) above the picture; the loader's PINK
   `llm-rag-chromadb:8000` along the llm-rag-network street (the two values flash PINK in the
   panel), then the browser's GREY `localhost:8000` through the wall door `8000→8000`. A YELLOW
   double arrow with '?' between the two labels on "Why can they not swap?".
1. The running map (AppMap.at("S10"), lifted 0.12 so a 4-row 20 pt strip fits under it). Each TEAL
   house grows its own loop 'localhost'; then a phone book under each street: llm-rag-network lists
   llm-rag-chromadb, cheese-app-network lists llm-rag-analysis-api-service. The strip (second
   terminal, P_API) types `docker network inspect cheese-app-network` (extra, bar) → TERM(40: 30–37;
   lines 31 and 33 cut with the house '…'), line 35's address ringed YELLOW, caption on the bar 'the
   API's IP address on its street · yours will differ'. The browser looks around; a GREY dashed
   book with '?' beside it.
2. The house loops but the API's leave. `docker exec … llm-rag-chromadb:8000 …` (laptop/41's
   command, soft-wrapped: its spaces are inside quotes) → TERM(41: 47; wrap) RED, 'Name or service
   not known' ringed RED. On the map a PINK magnifier from the API house searches its street's
   phone book: a RED cross.
3. The API house pulses with a YELLOW '?'. PONDER (8 s), card over the left of the map.
4. `docker network connect cheese-app-network llm-rag-chromadb` → TERM(42: no output). On the map
   the Chroma house grows a second PINK door, an arc onto cheese-app-network, and its name joins
   that street's phone book. The same exec → TERM(43: 2) GREEN; a GREEN check in the book and a
   dot rides from the API along the street and the arc to Chroma. The localhost variant
   (laptop/44's command) → TERM(44: 45) RED; a dot runs round the API's own loop, RED cross.
5. `docker network disconnect cheese-app-network llm-rag-chromadb` → TERM(45: no output); the
   second door and the book entry vanish, caption 'back to the tutorial's state' on the bar. Map
   and strip leave. README card (line 127, "it does not connect to ChromaDB" underlined). The
   erratum card: CODE(frontend-ai-chatbot/next.config.js: 19–25, 20 pt), line 23's destination
   dimmed RED, tag `erratum`, caption 'no such container here · use localhost:9000/docs' and
   'README.md · line 149'. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer.components import ponder_card

from common import (CONTAINERS, ERR, IMAGE, INK, NARRATION, P_API, PASS, ROUTE, SAY_COUNT, T_SECOND, TURN,
                    AppMap, TwoArrows, bare_prompt, capture, check_mark, code, code_span, cut,
                    erratum_tag, extra_row, extra_tag, flash_tag, label, line_bar, lref, magnifier, mono,
                    note, on_bar, out, readme, readme_card, ring, substring, term, type_cmd, under)
from explainer.devops import cross_mark
from explainer import style as S

SAY = NARRATION["S10"]
PONDER_3 = ("You want the API itself to query Chroma.\nWhat URL does it use, and what must change\n"
            "on the map for that name to resolve?")


# ------------------------------------------------------------------ local helpers
def soft_type(scene, t, cmd: str, type_time: float | None = None):
    """Type a command whose spaces are all inside quotes (laptop/41, 43, 44): it soft-wraps at the
    terminal's edge, as a terminal shows a long typed line; the rows join back to exactly the
    prompt and the command (S05/S09's helper)."""
    full = t.prompt + " " + cmd
    n = t.max_chars
    rows = [full[i:i + n] for i in range(0, len(full), n)]
    assert "".join(rows) == full and all(len(r) <= n for r in rows)
    assert len(rows) <= t.rows, (len(rows), t.rows)
    t.fold = lambda text, first_prefix=0: list(rows)
    try:
        return type_cmd(scene, t, cmd, type_time)
    finally:
        del t.fold


def drop(scene, *mobs, anims=(), run_time: float = 0.3):
    """Plays: free overlays fade and leave the scene."""
    scene.play(FadeOut(VGroup(*mobs)), *anims, run_time=run_time)
    scene.remove(*mobs)


def ponder_at(scene, question: str, seconds: float, card_w: float, center) -> VGroup:
    """pause_and_ponder, placed (over the left of the map, the API house stays visible); opaque so
    the map does not ghost through (S08 critic)."""
    pc = ponder_card(question, width=card_w).move_to(center)
    pc[0].set_fill(opacity=1)
    scene.play(FadeIn(pc, scale=0.95), run_time=0.6)
    bar = pc[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return pc


def book_slot(m: AppMap) -> VGroup:
    """Where a phone book would be for the laptop floor: a GREY dashed book outline with '?'."""
    fr = DashedVMobject(RoundedRectangle(width=0.62, height=0.52, corner_radius=0.06), num_dashes=16,
                        dashed_ratio=0.55).set_stroke(S.GREY, 2.5)
    q = label("?", 32, S.GREY).move_to(fr)
    g = VGroup(fr, q)
    return g.next_to(m.browser, RIGHT, buff=0.3)


class TwoAddresses(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S10"] == 6, len(SAY)
        ref = lref("5–6, 10")

        # ========================================================== 0. one server, two addresses
        ta = TwoArrows().move_to([0, -1.25, 0])
        cli = code("llm-rag/cli.py", 30, 31).move_to([0, 2.15, 0])
        xt0 = extra_tag("every command here is an extra").move_to([0, 0, 0])
        xt0.move_to([-6.55 + xt0.width / 2, 3.58 - xt0.height / 2, 0])
        host = code_span(cli.code, 0, '"llm-rag-chromadb"')
        port = code_span(cli.code, 1, "8000")
        swap = swap_bracket(ta.pink_text, ta.grey_text, 4.1)
        q0 = label("?", 40, TURN).next_to(swap, RIGHT, buff=0.2)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ta, shift=UP * 0.2), FadeIn(ref), run_time=0.9)
            vo.wait_until("every command in this scene")
            self.play(FadeIn(xt0, shift=DOWN * 0.15), run_time=0.4)
            flash_tag(self, xt0, INK)
            vo.wait_until("The loader dials the database")
            self.play(FadeIn(cli, shift=DOWN * 0.15), Indicate(ta.loader.text, color=INK, scale_factor=1.2),
                      run_time=0.7)
            self.play(ta.dial())
            vo.wait_until("llm-rag-chromadb, port 8000")
            self.play(each_flash([host, port], ROUTE), Indicate(ta.pink_text, color=ROUTE, scale_factor=1.1),
                      run_time=1.0)
            vo.wait_until("Your browser will ring")
            self.play(ta.ring_())
            vo.wait_until("through a door in the laptop wall")
            self.play(Indicate(ta.door.text, color=INK, scale_factor=1.15), run_time=0.8)
            vo.wait_until("One server, two addresses")
            self.play(Indicate(ta.chroma.text, color=INK, scale_factor=1.25), run_time=0.7)
            self.play(each_flash([ta.pink_text, ta.grey_text], INK), run_time=0.8)
            vo.wait_until("Why can they not swap?")
            self.play(Create(swap), FadeIn(q0, shift=LEFT * 0.1), run_time=0.7)

        # ========================================================== 1. own localhost, phone books, inspect
        m = AppMap.at("S10").shift(UP * 0.12)
        loops = {k: m.house_loop(k, with_label=False) for k in ("chroma", "loader", "frontend", "api")}
        own = note("every house: its own localhost", IMAGE)   # the loops' one label (above the tubes)
        own.move_to([(m.header.get_right()[0] + m.drawer.get_left()[0]) / 2, m.header.get_center()[1], 0])
        pb_rag = book(m, "llm-rag", [CONTAINERS["chroma"]])
        pb_api = book(m, "cheese-app", [CONTAINERS["api"]])
        t = term(P_API, rows=4, title=T_SECOND, size=20)
        xb = on_bar(t, extra_row())
        c40 = capture("40")
        rows40 = c40.at((30, 37))
        rows40[1] = cut(rows40[1], '"ed21c759d782')
        rows40[3] = cut(rows40[3], '"25d3cc6d441a')
        slot = book_slot(m)

        with self.voiceover(SAY[1]) as vo:
            old = VGroup(ta, ta.pink, ta.pink_text, ta.grey, ta.grey_text, cli, swap, q0, xt0)
            self.play(FadeOut(old, scale=0.7), run_time=0.6)
            self.remove(old, *old)
            self.play(FadeIn(m, scale=1.05), run_time=0.8)
            vo.wait_until("Each container is its own house")
            self.play(LaggedStart(*[FadeIn(lp, scale=0.6) for lp in loops.values()], lag_ratio=0.25),
                      FadeIn(own, shift=DOWN * 0.1), run_time=1.2)
            vo.wait_until("Inside a container, localhost means")
            ap = loops["api"][0]
            dot = Dot(radius=0.06, color=IMAGE).move_to(ap.get_start())
            self.play(FadeIn(dot, scale=0.5), run_time=0.2)
            self.play(MoveAlongPath(dot, ap), Indicate(own, color=INK, scale_factor=1.08), run_time=1.0)
            self.play(FadeOut(dot), Indicate(m.houses["api"].text, color=INK, scale_factor=1.2), run_time=0.6)
            self.remove(dot)
            vo.wait_until("Names work through Docker DNS")
            doors = VGroup(m.doors["8000"], m.doors["9000"])      # the books lie over the wall's doors
            self.play(FadeIn(pb_rag, shift=DOWN * 0.15), FadeOut(doors), run_time=0.6)
            self.remove(doors, *doors)
            self.play(FadeIn(pb_api, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("IP addresses change")
            self.play(each_flash([pb_rag.rows[0], pb_api.rows[0]], INK), run_time=1.0)
            vo.wait_until("This extra inspect shows")
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(xb), run_time=0.5)
            type_cmd(self, t, c40.cmd, type_time=0.6)
            out(self, t, rows40, run_time=1.2, chunk=4)
            r35 = t.find('"IPv4Address": "172.19.0.2/16"')
            g35 = ring(substring(r35, "172.19.0.2/16"), TURN, buff=0.05)
            cap1 = VGroup(note("the API's IP address on its street", INK), note("yours will differ", INK))
            cap1.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            cap1.move_to([r35.glyphs.get_right()[0] + 0.6 + cap1.width / 2, 0, 0]).align_to(r35.glyphs, UP)
            self.play(Create(g35), Indicate(m.houses["api"].text, color=TURN, scale_factor=1.2), run_time=0.7)
            vo.wait_until("Yours will differ")
            self.play(FadeIn(cap1, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("dial names, not IP addresses")
            self.play(Indicate(pb_api.rows[0], color=ROUTE, scale_factor=1.1), run_time=0.8)
            vo.wait_until("And your laptop is not on any street")
            br = m.browser
            self.play(Rotate(br, angle=0.18), rate_func=there_and_back, run_time=0.6)
            self.play(Rotate(br, angle=-0.18), rate_func=there_and_back, run_time=0.6)
            vo.wait_until("that name means nothing")
            self.play(FadeIn(slot, scale=0.8), run_time=0.6)
            self.play(Indicate(slot[1], color=INK, scale_factor=1.3), run_time=0.7)

        # ========================================================== 2. the proof: a name off the street
        c41, c43, c44 = capture("41"), capture("43"), capture("44")
        lens = magnifier(0.2).move_to(m.houses["api"].body.get_center())
        spot = np.array([pb_api.get_right()[0] - 0.5, pb_api.head.get_center()[1], 0])   # the head row's free end
        x41 = cross_mark(0.3, ERR).move_to(spot)

        with self.voiceover(SAY[2]) as vo:
            drop(self, g35, cap1, slot, own, loops["chroma"], loops["loader"], loops["frontend"], run_time=0.5)
            vo.wait_until("From inside the API container")
            soft_type(self, t, c41.cmd, type_time=1.0)
            self.play(Indicate(m.houses["api"].text, color=INK, scale_factor=1.2), run_time=0.5)
            vo.wait_until("The answer: name or service")
            out(self, t, [(s, ERR) for s in [c41.line(47)]], wrap=True, run_time=0.4)
            hit = t.find("Name or service")
            g47 = ring(substring(hit, "Name or service"), ERR, buff=0.05)
            self.play(Create(g47), run_time=0.4)
            vo.wait_until("The API's street has no entry")
            self.play(FadeIn(lens, scale=0.6), run_time=0.3)
            self.play(lens.animate.move_to(spot), run_time=0.8)
            self.play(Indicate(pb_api.rows[0], color=INK, scale_factor=1.08), run_time=0.5)
            self.play(FadeOut(lens), Create(x41), run_time=0.4)
            self.remove(lens)

        # ========================================================== 3. ponder
        api_h = m.houses["api"]
        q3 = label("?", 44, TURN).move_to([api_h.get_right()[0] + 0.35, api_h.body.get_center()[1] + 0.1, 0])

        with self.voiceover(SAY[3]) as vo:
            drop(self, x41, g47, run_time=0.4)
            self.play(FadeIn(q3, scale=0.6), run_time=0.4)
            self.play(Indicate(api_h.text, color=TURN, scale_factor=1.3), Indicate(q3, color=TURN, scale_factor=1.3),
                      run_time=0.9)
            vo.wait_until("What address would it use")
            self.play(Indicate(api_h.text, color=TURN, scale_factor=1.3), Indicate(q3, color=TURN, scale_factor=1.3),
                      run_time=0.9)
            vo.wait_until("what must change on the map")
            self.play(Indicate(pb_api, color=TURN, scale_factor=1.06),
                      Indicate(m.streets["cheese-app"].band, color=TURN, scale_factor=1.04), run_time=1.0)
        pc = ponder_at(self, PONDER_3, 8, 6.9, [-2.95, 0.95, 0])

        # ========================================================== 4. connect: a second door; the name answers
        ch = m.houses["chroma"]
        d2 = door_mark()                                   # outside the wall: clear of the name
        d2.move_to([ch.body.get_right()[0] + d2.width / 2 + 0.02, ch.body.get_center()[1] - 0.06, 0])
        band = m.streets["cheese-app"].band
        end = np.array([band.get_left()[0] + 0.12, band.get_top()[1], 0])
        # over the loader's roof, under the GREEN tube lane: a second door onto cheese-app-network
        a = d2.get_right() + RIGHT * 0.02
        spur = CubicBezier(a, a + np.array([0.3, 1.1, 0]), np.array([-2.4, a[1] + 1.1, 0]), end,
                           color=ROUTE, stroke_width=4)
        tip = Dot(radius=0.07, color=ROUTE).move_to(end)
        pb_both = book(m, "cheese-app", [CONTAINERS["api"], CONTAINERS["chroma"]])
        c42, c45 = capture("42"), capture("45")
        ok43 = check_mark(0.3, PASS).move_to([pb_both.get_right()[0] - 0.35, pb_both.rows[1].get_center()[1], 0])
        x44 = cross_mark(0.26, ERR).next_to(loops["api"][0], RIGHT, buff=0.1)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(pc), FadeOut(q3), run_time=0.5)
            self.remove(pc, q3)
            vo.wait_until("with an extra docker network connect")
            type_cmd(self, t, c42.cmd, type_time=0.7)
            bare_prompt(self, t)
            self.play(FadeIn(d2, scale=0.5), run_time=0.4)
            self.play(Create(spur), FadeIn(tip, scale=0.5), run_time=0.8)
            self.play(Transform(pb_api[0], pb_both[0]),
                      FadeIn(pb_both.rows[1], shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("and the same name answers")
            soft_type(self, t, c43.cmd, type_time=0.8)
            r43 = out(self, t, [(c43.line(2), PASS)], run_time=0.3)[0]
            g43 = ring(r43.glyphs, PASS, buff=0.06)
            self.play(Create(g43), Create(ok43), run_time=0.5)
            vo.wait_until("Docker DNS works on a shared street")
            dot = Dot(radius=0.08, color=ROUTE).move_to(api_h.body.get_left() + LEFT * 0.05)
            self.play(FadeIn(dot, scale=0.5), run_time=0.2)
            self.play(dot.animate.move_to([api_h.body.get_left()[0] - 0.1, band.get_center()[1], 0]), run_time=0.3)
            self.play(dot.animate.move_to(end + DOWN * 0.15), run_time=0.7)
            self.play(MoveAlongPath(dot, spur.copy().reverse_points()), run_time=0.8)
            self.play(FadeOut(dot), Indicate(ch.text, color=INK, scale_factor=1.25), run_time=0.6)
            self.remove(dot)
            vo.wait_until("And localhost 8000, from inside the API?")
            drop(self, g43, run_time=0.2)
            soft_type(self, t, c44.cmd, type_time=0.8)
            vo.wait_until("Connection refused.")
            out(self, t, [(c44.line(45), ERR)], run_time=0.3)
            hit = t.find("Connection refused")
            g44 = ring(substring(hit, "Connection refused"), ERR, buff=0.05)
            ap = loops["api"][0]
            dot = Dot(radius=0.06, color=ERR).move_to(ap.get_start())
            self.play(Create(g44), FadeIn(dot, scale=0.5), run_time=0.4)
            self.play(MoveAlongPath(dot, ap), run_time=0.9)
            vo.wait_until("Inside the API, nothing listens")
            self.play(FadeOut(dot), Create(x44), Indicate(api_h.text, color=ERR, scale_factor=1.2), run_time=0.7)
            self.remove(dot)

        # ========================================================== 5. disconnect; README; the erratum
        r127 = readme(127)
        assert "it does not connect to ChromaDB." in r127 and r127.startswith("***Setup**: build and start")
        l1 = label("Setup: build and start the API server. It generates embeddings", 22, INK)
        l2a = label("and calls the LLM;", 22, INK)
        l2b = label("it does not connect to ChromaDB.", 22, INK)
        l2 = VGroup(l2a, l2b).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        rc = readme_card(127, VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.12), quote=True)
        rc.move_to([0, 2.35, 0])
        ul = under(l2b, TURN, stroke=3)
        nc = code("frontend-ai-chatbot/next.config.js", 19, 25, font_size=20).move_to([-0.9, -0.35, 0])
        er = erratum_tag().next_to(nc, RIGHT, buff=0.25).align_to(nc, UP)
        dest = code_span(nc.code, 4, '"http://rag-system-api-service:9000/docs"')
        src_l = code_span(nc.code, 1, '"/docs"')
        bar23 = line_bar(nc.code, 4, ERR)
        cap6 = VGroup(note("no such container here · use", INK, size=22), mono("localhost:9000/docs", 22, INK))
        cap6.arrange(RIGHT, buff=0.15).move_to([-0.9, -2.45, 0])
        src149 = note("README.md · line 149").next_to(cap6, DOWN, buff=0.15)
        assert "localhost:9000/docs" in readme(149)

        with self.voiceover(SAY[5]) as vo:
            drop(self, g44, x44, run_time=0.3)
            type_cmd(self, t, c45.cmd, type_time=0.7)
            bl = bare_prompt(self, t)
            cap5 = note("back to the tutorial's state", INK)
            cap5.move_to([bl.strut.get_right()[0] + 0.6 + cap5.width / 2, bl.strut.get_center()[1], 0])
            self.play(Uncreate(spur), FadeOut(d2), FadeOut(tip), FadeOut(ok43), FadeOut(pb_both.rows[1]),
                      Transform(pb_api[0], book(m, "cheese-app", [CONTAINERS["api"]])[0]),
                      FadeIn(cap5, shift=LEFT * 0.15), run_time=0.7)   # caption with the revert: it holds ~2 s
            self.remove(spur, d2, tip, ok43, pb_both.rows[1])
            vo.wait_until("that shortcut")
            gone = [x for x in self.mobjects if x is not ref]
            self.play(FadeOut(Group(*gone)), run_time=0.6)
            self.remove(*gone)
            self.play(FadeIn(rc, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("because the browser makes every call")
            self.play(Create(ul), run_time=0.6)
            vo.wait_until("One small slip")
            self.play(FadeIn(nc, shift=UP * 0.15), FadeIn(er, shift=LEFT * 0.15), run_time=0.7)
            flash_tag(self, er, ERR)
            vo.wait_until("forwards its docs path")
            self.play(Indicate(src_l, color=INK, scale_factor=1.15), run_time=0.7)
            vo.wait_until("to a container name")
            self.play(FadeIn(bar23), dest.animate.set_color(ERR).set_opacity(0.6), run_time=0.7)
            vo.wait_until("For the API docs")
            self.play(FadeIn(cap6, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(cap6[1], color=PASS, scale_factor=1.12), run_time=0.7)
            vo.wait_until("as the README says")
            self.play(FadeIn(src149, shift=UP * 0.1), run_time=0.5)

        self.wait(0.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)


def each_flash(pieces, color, scale: float = 1.15):
    """Animation: flash scattered pieces one after another."""
    return LaggedStart(*[Indicate(p, color=color, scale_factor=scale) for p in pieces], lag_ratio=0.35)


def door_mark() -> VGroup:
    """Chroma's second door (PINK: a door onto a street)."""
    fr = RoundedRectangle(width=0.22, height=0.32, corner_radius=0.04, stroke_color=ROUTE, stroke_width=3)
    fr.set_fill(ROUTE, 0.2)
    return VGroup(fr)


def swap_bracket(top, bottom, x: float) -> VGroup:
    """A YELLOW two-headed bracket right of the picture, from label `top` to label `bottom`
    (it never crosses the houses): 'can these two swap?'."""
    y1, y2 = top.get_center()[1], bottom.get_center()[1]
    a1, a2 = top.get_right() + RIGHT * 0.15, bottom.get_right() + RIGHT * 0.15
    spine = Line([x, y1, 0], [x, y2, 0], color=TURN, stroke_width=3)
    t1 = Arrow([x, y1, 0], a1, buff=0, color=TURN, stroke_width=3, tip_length=0.18,
               max_tip_length_to_length_ratio=0.3)
    t2 = Arrow([x, y2, 0], a2, buff=0, color=TURN, stroke_width=3, tip_length=0.18,
               max_tip_length_to_length_ratio=0.3)
    return VGroup(spine, t1, t2)


def book(m: AppMap, k: str, names) -> VGroup:
    """Street k's phone book, right under its band (buff 0.03, so it clears the browser's top);
    llm-rag's ends 0.12 left of its street, cheese-app's 0.26 right of its own: the two never touch."""
    g = m.phone_book(k, names)
    band = m.streets[k].band
    g.next_to(band, DOWN, buff=0.03).align_to(band, RIGHT)
    g.shift(RIGHT * (0.26 if k == "cheese-app" else -0.12))
    return g
