"""S01 · Three phone calls, one question (cold open of AC215 L10) — the reference scene for common.py.

Beats (script.md, ## S01; one voiceover block each):
0. Black frame, no tracker. The schematic /chat page (ChatWireframe, tag `illustration`), address
   `localhost:3200/chat`; GREY note 'README.md · line 215' beside the question bubble. On "You ask
   it how Tolminc" the README's example types in; on "An answer appears" five GREY skeleton bars
   grow (no glyphs); on "with ten book passages" the 'References · 10 chunks' drawer opens to ten
   empty GREY rows. No answer text anywhere.
1. Freeze: the page dims and your browser steps out of it (left). Three PINK calls leave it in turn:
   ① ':9000' and ③ ':9000' to a TEAL 'Python server' house, ② ':8000' to a TEAL 'database' house
   (V5 teaser). On "Behind both server calls" two thin BLUE lines run on from the server to the BLUE
   'Google Cloud' building (top right). A YELLOW '?' marks the BLUE lines on "who checks", another
   marks call ② on "how does a web page find".
2. "Zoom out": the picture shrinks away and the V6 skeleton arrives (AppMap.at("S01"): laptop frame,
   two planned streets, four hollow houses, browser, public street, Google). `lecture_ref(10, "4,
   11–13")` top right from here to the end. Three riddle cards drop in under the map, one per
   sentence; each fades to a small label (bottom row; kept for S15's recap) before the next. A
   fourth card, slide 11's flip, after the third: a door with a knocker, "once anything can knock:
   who's allowed in?"; the knocker swings on "once anything can knock".
3. Checklist card (✓ your clone of cheese-app-v0 · ✓ Docker Desktop running · ✓ a GCP project with
   billing + the GOLD cost tag 'this lecture bills'). Layout preview: tracker A (step 1) top-left in
   a YELLOW ring; on "six sections" the ring cycles trackers A–F and returns to A. A 2-row strip
   (GREY tag 'preview', prompt student@laptop:~$) types `git clone https://github.com/dlops-io/
   cheese-app-v0` (laptop/01's command; it folds) with the YELLOW `▶ your turn` row tag, then
   `docker ps` (laptop/22's command) with the GREY `extra` row tag (tracker caption gains ' · extra'),
   then a GREY `recorded` tag above the strip. Tags never stacked. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (COST, IMAGE, INK, LAPTOP, NARRATION, P_LAPTOP_HOME, ROUTE, CLOUD, SAY_COUNT, TURN,
                    AppMap, ChatWireframe, KNOCK, beside, browser_glyph, capture, check_mark, cost_tag,
                    door_glyph, extra_row, flash_tag, google_building, house, illustration_tag, label,
                    lref, mono, note, pin, preview_tag, recorded_tag, riddle_card, riddle_label, route,
                    step_badge, swap_tracker, term, track, tracker, turn_row, type_cmd, unpin)
from explainer import style as S

SAY = NARRATION["S01"]


def tracker_ring(tr, stroke: float = 3, opacity: float = 1.0) -> RoundedRectangle:
    """The YELLOW ring around the tracker's place: fixed top-left corner, as wide as `tr`."""
    x0, y0 = -6.58, 3.58
    x1, y1 = tr.get_right()[0] + 0.2, tr.get_bottom()[1] - 0.1
    r = RoundedRectangle(width=x1 - x0, height=y0 - y1, corner_radius=0.14, stroke_color=TURN,
                         stroke_width=stroke, stroke_opacity=opacity)
    return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def call_label(k: int, port: str) -> VGroup:
    """A numbered PINK call: badge k and its port."""
    return VGroup(step_badge(k, ROUTE), mono(port, 22, ROUTE)).arrange(RIGHT, buff=0.12)


def knock_card() -> VGroup:
    """Slide 11's flip: a door with a knocker, and the question."""
    d = door_glyph(0.5, 0.8, S.GREY)
    knocker = Circle(radius=0.09, stroke_color=TURN, stroke_width=3).move_to(d.frame.get_center() + UP * 0.15)
    t = label(KNOCK, 26, INK)
    row = VGroup(VGroup(d, knocker), t).arrange(RIGHT, buff=0.4)
    fr = RoundedRectangle(width=row.width + 0.7, height=row.height + 0.4, corner_radius=0.14,
                          stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    row.move_to(fr)
    g = VGroup(fr, row)
    g.knocker, g.text = knocker, t
    return g


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S01"] == 4, len(SAY)

        # ========================================================== 0. a cheese chatbot, wireframe only
        cw = ChatWireframe().move_to([0, -0.35, 0])
        tag_ill = illustration_tag().next_to(cw.window, UP, buff=0.1).align_to(cw.window, RIGHT)
        src = note("README.md · line 215").next_to(cw.bubble, LEFT, buff=0.4)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(cw.shell, shift=UP * 0.2), FadeIn(tag_ill), run_time=1.0)
            vo.wait_until("You ask it how Tolminc")
            self.play(cw.type_question(1.4), FadeIn(src, shift=RIGHT * 0.15))
            vo.wait_until("An answer appears")
            self.play(cw.grow_bars(1.0))
            vo.wait_until("with ten book passages")
            self.play(cw.open_drawer(1.0))
            self.play(Indicate(cw.drawer.text, color=INK, scale_factor=1.08), run_time=0.7)

        # ========================================================== 1. three phone calls
        page = VGroup(cw, tag_ill, src)
        br = browser_glyph(name="your browser", glyph_w=1.3).move_to([-5.0, -0.5, 0])
        server = house("Python server", 2.5, 1.0, lit=True).move_to([1.2, 0.65, 0], aligned_edge=DOWN)
        db = house("database", 2.5, 1.0, lit=True).move_to([1.2, -2.35, 0], aligned_edge=DOWN)
        gb = google_building(2.3, 2.3, door=False, meter_=False).move_to([5.2, 0.6, 0], aligned_edge=DOWN)
        start = br.window.get_right() + RIGHT * 0.1
        c1 = route(start + UP * 0.15, server.body.get_left() + UP * 0.12, arc=-0.35)
        c3 = route(start + DOWN * 0.05, server.body.get_left() + DOWN * 0.15, arc=0.3)
        c2 = route(start + DOWN * 0.25, db.body.get_left(), arc=0.25)
        l1 = call_label(1, ":9000").move_to(c1.point_from_proportion(0.5) + UP * 0.45)
        l3 = call_label(3, ":9000").move_to(c3.point_from_proportion(0.55) + DOWN * 0.45 + RIGHT * 0.2)
        l2 = call_label(2, ":8000").move_to(c2.point_from_proportion(0.55) + DOWN * 0.45 + RIGHT * 0.3)
        b1 = Line(server.body.get_right() + UP * 0.12, gb.frame.get_left() + np.array([0.15, 0.55, 0]),
                  color=CLOUD, stroke_width=2.5)
        b3 = Line(server.body.get_right() + DOWN * 0.12, gb.frame.get_left() + np.array([0.15, 0.25, 0]),
                  color=CLOUD, stroke_width=2.5)
        q_who = label("?", 40, TURN).next_to(VGroup(b1, b3), UP, buff=0.15)
        q_find = label("?", 40, TURN).next_to(l2, RIGHT, buff=0.3)

        with self.voiceover(SAY[1]) as vo:
            self.play(page.animate.fade(0.7), run_time=0.6)
            self.play(FadeIn(br, target_position=cw.window.get_center(), scale=0.6), run_time=0.9)
            self.play(FadeOut(page), FadeIn(server), FadeIn(db), run_time=0.6)
            self.remove(page)
            vo.wait_until("Two go to a Python server")
            self.play(Create(c1), FadeIn(l1, scale=0.8), run_time=0.8)
            self.play(Create(c3), FadeIn(l3, scale=0.8), run_time=0.8)
            vo.wait_until("and one goes to a database")
            self.play(Create(c2), FadeIn(l2, scale=0.8), run_time=0.8)
            vo.wait_until("Behind both server calls")
            self.play(FadeIn(gb, shift=LEFT * 0.2), run_time=0.5)
            self.play(Create(b1), Create(b3), run_time=0.8)
            vo.wait_until("So who checks")
            self.play(FadeIn(q_who, shift=DOWN * 0.15), Indicate(gb.text, color=CLOUD, scale_factor=1.1), run_time=0.8)
            vo.wait_until("And how does a web page")
            self.play(FadeIn(q_find, shift=LEFT * 0.15), Indicate(db.text, color=INK, scale_factor=1.12), run_time=0.8)

        # ========================================================== 2. the map, three riddles, the flip
        m = AppMap.at("S01").move_to([0, 0.9, 0])
        ref = lref("4, 11–13")
        old = VGroup(br, server, db, gb, c1, c2, c3, l1, l2, l3, b1, b3, q_who, q_find)
        cards = [riddle_card(i).move_to([0, -2.0, 0]) for i in range(3)]
        labels = VGroup(*[riddle_label(i) for i in range(3)]).arrange(RIGHT, buff=0.9).move_to([0, -3.25, 0])
        knock = knock_card().move_to([0, -2.0, 0])

        def to_label(i):
            """Card i fades to its small label (frame and question out; the code shrinks into place)."""
            c = cards[i]
            self.play(FadeOut(VGroup(c.frame, c.question)), Transform(c.code, labels[i].code),
                      FadeIn(labels[i][1]), run_time=0.7)
            self.remove(c.frame, c.question, c.code)
            self.add(labels[i])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(old, scale=0.55), run_time=0.7)
            self.remove(old)
            self.play(FadeIn(m, scale=1.25), FadeIn(ref), run_time=1.0)
            vo.wait_until("The flag dash p")
            self.play(FadeIn(cards[0], shift=DOWN * 0.3), run_time=0.6)
            vo.wait_until("And localhost 9000")
            to_label(0)
            self.play(FadeIn(cards[1], shift=DOWN * 0.3), run_time=0.6)
            vo.wait_until("And llm-rag-chromadb")
            to_label(1)
            self.play(FadeIn(cards[2], shift=DOWN * 0.3), run_time=0.6)
            self.play(Indicate(m.houses["chroma"].text, color=INK, scale_factor=1.2), run_time=0.8)
            vo.wait_until("Each one gets its answer")
            to_label(2)
            self.play(LaggedStart(*[Indicate(lb[1], color=TURN, scale_factor=1.4) for lb in labels],
                                  lag_ratio=0.25), run_time=1.0)
            vo.wait_until("Then the real question")
            self.play(FadeIn(knock, shift=DOWN * 0.3), run_time=0.6)
            vo.wait_until("once anything can knock")
            self.play(Rotate(knock.knocker, angle=0.6, about_point=knock.knocker.get_top()),
                      rate_func=there_and_back, run_time=0.5)
            self.play(Rotate(knock.knocker, angle=0.6, about_point=knock.knocker.get_top()),
                      rate_func=there_and_back, run_time=0.5)
            self.play(Indicate(knock.text, color=INK, scale_factor=1.05), run_time=0.8)

        # ========================================================== 3. what you need, how to follow
        def row(*parts):
            return VGroup(check_mark(0.32, LAPTOP), *parts).arrange(RIGHT, buff=0.2)

        rows = [row(label("your clone of", 28, INK), mono("cheese-app-v0", 26, INK)),
                row(label("Docker Desktop running", 28, INK)),
                row(label("a GCP project with billing", 28, INK))]
        body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        bill = cost_tag("this lecture bills").next_to(rows[2], RIGHT, buff=0.35)
        frame = RoundedRectangle(width=body.width + bill.width + 1.4, height=body.height + 0.8, corner_radius=0.18,
                                 stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        frame.move_to([0, 0.2, 0])
        body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.5)
        bill.next_to(rows[2], RIGHT, buff=0.35)

        trs = {k: tracker(k, 1) for k in "ABCDEF"}
        tr = trs["A"]
        rng = tracker_ring(tr)
        strip = term(P_LAPTOP_HOME, rows=2, title="laptop")
        prev = preview_tag().next_to(strip.box, UP, buff=0.15).align_to(strip.box, LEFT)
        rec = recorded_tag("recorded · source named").next_to(strip.box, UP, buff=0.15).align_to(strip.box, RIGHT)
        clone, ps = capture("01").cmd, capture("22").cmd

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(m, ref, labels, knock)), run_time=0.6)
            self.remove(m, ref, labels, knock)
            self.play(FadeIn(frame, scale=0.96), run_time=0.4)
            for r, anchor in zip(rows, ("your clone of", "Docker Desktop", "and a Google Cloud project")):
                vo.wait_until(anchor)
                self.play(FadeIn(r, shift=RIGHT * 0.25), run_time=0.5)
            vo.wait_until("This lecture makes real")
            self.play(FadeIn(bill, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("a gold tag marks each one")
            self.play(flash_tag(bill, COST))
            vo.wait_until("The tracker in the top left")
            self.play(FadeOut(VGroup(frame, body, bill)), run_time=0.5)
            self.remove(frame, body, bill)
            self.play(FadeIn(tr, shift=DOWN * 0.15), Create(rng), run_time=0.8)
            vo.wait_until("six sections")
            for k in "BCDEF":
                new = trs[k]
                tr = swap_tracker(self, tr, new, Transform(rng, tracker_ring(new)), run_time=0.4)
            back = tracker("A", 1)
            tr = swap_tracker(self, tr, back, Transform(rng, tracker_ring(back)), run_time=0.5)
            vo.wait_until("A yellow your-turn tag")
            self.play(FadeIn(strip), FadeIn(prev, shift=RIGHT * 0.2), rng.animate.set_stroke(opacity=0.35),
                      run_time=0.6)
            ln1 = type_cmd(self, strip, clone, type_time=1.2)
            yt = beside(turn_row(), ln1)
            pin(self, ln1, yt)
            vo.wait_until("means pause and run it")
            self.play(flash_tag(yt, TURN))
            vo.wait_until("and a gray extra tag")
            unpin(self, ln1, yt)
            ln2 = type_cmd(self, strip, ps, type_time=0.5)
            xt = beside(extra_row(), ln2)
            pin(self, ln2, xt, anim=AnimationGroup(FadeIn(xt, shift=LEFT * 0.1), track(tr, extra=True),
                                                   Transform(rng, tracker_ring(tracker("A", 1, True), opacity=0.35))))
            vo.wait_until("marks a check")
            self.play(flash_tag(xt, INK))
            vo.wait_until("Every command")
            unpin(self, ln2, xt)
            self.play(FadeIn(rec, shift=LEFT * 0.15), FadeOut(rng), run_time=0.6)
            self.remove(rng)
            self.play(flash_tag(rec, INK))

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
