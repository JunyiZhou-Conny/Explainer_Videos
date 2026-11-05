"""Workbench for scenes/common.py (scratch, not a scene of the video): plays every set piece's
methods once so explainer.check / preview catch runtime errors, OUT and SMALL before scene agents
rely on them.  python -m explainer.check videos/ac215-l10-cloud-connect/build/common_test.py Bench --tts silent"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scenes"))

from manim import *  # noqa: E402,F403

from common import *  # noqa: E402,F403


def clear(scene):
    if scene.mobjects:
        scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.3)
        scene.remove(*scene.mobjects)


class Bench(Scene):
    def construct(self):
        # ---------------------------------------------------------- V6 · the running map, above a strip
        tr = tracker_b(2)
        ref = lref("9–10")
        self.add(tr, ref)
        m = AppMap.at("S05")
        self.play(FadeIn(m))
        self.play(m.lay("cheese-app"), m.lay("llm-rag"))
        self.play(m.light("chroma"), m.tube_on("loader"))
        self.play(m.open_door("8000"), m.open_door("9000"), m.open_door("3200"), m.light("api"),
                  m.light("frontend"), m.tube_on("api"), track(tr, 3, extra=True))
        calls = VGroup(m.call("browser", "chroma"), m.call("browser", "api"), m.call("browser", "frontend"),
                       m.call("loader", "chroma"), m.call("loader", "google"), m.call("api", "google"))
        self.play(LaggedStart(*[Create(c) for c in calls], lag_ratio=0.2))
        self.play(meter_tick(m.google.meter))
        strip = term(P_LLMRAG, rows=3)
        self.play(FadeIn(strip))
        ln = type_cmd(self, strip, capture("21").cmd)
        out(self, strip, squash(capture("21").at((3, 5))), wrap=False)
        clear(self)
        # map end states + its extras
        m2 = AppMap.at("S15")
        lp = m2.house_loop("api")
        pb = m2.phone_book("cheese-app", [CONTAINERS["api"]])
        self.play(FadeIn(m2), FadeIn(lp), FadeIn(pb))
        self.play(m2.darken("api"))
        clear(self)
        m3 = AppMap.at("S12").move_to([0, 0.5, 0])
        wf = m3.wifi()
        self.play(FadeIn(m3), FadeIn(wf), *[Create(r) for r in wf.reach.values()])
        self.play(m3.brick("9000"))
        clear(self)
        # ---------------------------------------------------------- V1 · the auth chain
        ch = AuthChain(teaser=True).move_to([0, 1.2, 0])
        self.play(FadeIn(ch))
        x = ch.break_at(self)
        self.play(FadeOut(x))
        self.remove(x)
        self.play(ch.reveal(1), ch.reveal(2))
        self.play(ch.light_all())
        self.play(FadeIn(ch.url))
        reqs = ch.staple(3).next_to(ch, DOWN, buff=0.5)
        self.play(FadeIn(reqs))
        ch.mint(self)
        clear(self)
        ap = AdcPlaces().move_to([0.3, 0.2, 0])
        self.play(FadeIn(ap), FadeIn(ap.glass))
        self.play(ap.visit(1))
        self.play(ap.visit(0))
        ap.stop(self, 0)
        box_, an = ap.enclose()
        self.play(an)
        self.play(ap.empty((1, 2)))
        clear(self)
        # ---------------------------------------------------------- V2 · the IAM grid
        g = IamGridRig().move_to([0, 0.6, 0])
        self.play(FadeIn(g))
        self.play(g.drop(g.token("Owner", S.GREY, mono_font=False), 0, 0))
        self.play(g.drop(g.token("roles/aiplatform.user", PASS), 1, 0, 0, 2),
                  g.drop(g.token("Storage Admin", S.GREY, mono_font=False), 1, 0, 1, 2))
        g.fire(self, 1, 0, True, "embed")
        g.fire(self, 1, 1, False, "embed")
        g.fire(self, 1, 2, False, "tuned model")
        self.play(g.pulse_col(2))
        clear(self)
        # ---------------------------------------------------------- V3 · the secrets portal
        sp = SecretsPortalRig()
        self.play(FadeIn(sp.tree), FadeIn(sp.caption))
        cur = sp.climb(self)
        self.play(FadeIn(sp.box), FadeIn(sp.host_cap.next_to(sp.caption, RIGHT, buff=0.3)))
        self.play(sp.connect())
        sp.snap(self)
        clear(self)
        sk = SecretsPortalRig(key_inside=True)
        self.play(FadeIn(sk.tree), FadeIn(sk.caption), FadeIn(sk.box))
        sk.climb(self)
        sk.pop_empty(self)
        self.play(sk.connect())
        sk.snap(self)
        clear(self)
        # ---------------------------------------------------------- V4
        ta = TwoArrows().move_to([0, 0.6, 0])
        self.play(FadeIn(ta))
        self.play(ta.dial())
        self.play(ta.ring_())
        clear(self)
        pd = PortDoor().move_to([0, 0.8, 0])
        self.play(FadeIn(pd))
        pd.tunnel(self)
        self.play(pd.brick())
        clear(self)
        pl = PortLine().move_to([0, 0.5, 0])
        self.play(FadeIn(pl))
        self.play(pl.drop(0), pl.drop(1))
        self.play(pl.note_in())
        clear(self)
        # ---------------------------------------------------------- V5
        cb = CorsBouncer().move_to([0, 0.4, 0])
        self.play(FadeIn(cb))
        cb.send(self, 1)
        cb.cloud(self)
        ok = cb.preflight(self)
        cb.admit(self) if ok else cb.refuse(self)
        cb.send(self, 3)
        clear(self)
        pr = PacketReplay("3300").move_to([0, 0.4, 0])
        self.play(FadeIn(pr))
        pr.replay(self)
        clear(self)
        cb2 = CorsBouncer()
        self.play(FadeIn(cb2))
        self.play(cb2.restamp("3300"))
        clear(self)
        # ---------------------------------------------------------- the chat page
        cw = ChatWireframe(picker="char-split-collection ▾", row_head="book · author · dist").move_to([0, -0.3, 0])
        self.play(FadeIn(cw.shell), FadeIn(illustration_tag().next_to(cw.window, UP, buff=0.1).align_to(cw.window,
                                                                                                         RIGHT)))
        self.play(cw.type_question())
        self.play(cw.grow_bars())
        self.play(cw.open_drawer())
        clear(self)
        cf = ChatWireframe("localhost:3200/agent", fun_fact=True).move_to([0, -0.1, 0])
        self.play(FadeIn(cf.shell))
        self.play(cf.type_question(), cf.grow_bars())
        clear(self)
        # ---------------------------------------------------------- glyphs, riddles, cards
        glyphs = VGroup(key_glyph(), magnifier(), envelope("JWT", sealed=True), desk_glyph(), Ticket(),
                        house("API", lit=True), house("chroma"), door_glyph(), bricks(),
                        browser_glyph(), meter(), lock_glyph()).arrange_in_grid(rows=3, buff=0.35)
        glyphs.move_to([0, 1.0, 0])
        bars = EmbeddingBars().move_to([0, -2.6, 0])
        self.play(FadeIn(glyphs), bars.grow())
        clear(self)
        kc = key_card().move_to([-1.6, 0.3, 0])
        bd = google_building().move_to([5.0, 0.3, 0])
        bdg = badge().move_to([-1.6, -2.7, 0])
        self.play(FadeIn(kc), FadeIn(bd), FadeIn(bdg))
        self.play(Indicate(kc.private_key, color=ERR))
        clear(self)
        rc = VGroup(*[riddle_card(i) for i in range(3)]).arrange(DOWN, buff=0.3).move_to([0, 1.0, 0])
        rl = VGroup(*[riddle_label(i) for i in range(3)]).arrange(RIGHT, buff=0.6).move_to([0, -2.6, 0])
        self.play(FadeIn(rc), FadeIn(rl))
        clear(self)
        # ---------------------------------------------------------- terminals, code, tags
        t = laptop_term(6, P_LAPTOP_HOME)
        self.play(FadeIn(t), FadeIn(tracker_a(5, extra=True)))
        cap = capture("10")
        ln = type_cmd(self, t, cap.cmd)
        yt = on_bar(t, turn_row())
        self.play(FadeIn(yt))
        out(self, t, cap.at(2), wrap=True)
        cap = capture("33")
        istep(self, t, cap.line(34))
        out(self, t, cap.at((35, 41), "…", 162), wrap=True)
        ln2 = type_cmd(self, t, capture("23").cmd)
        out(self, t, capture("23").at(2))
        pin(self, ln2, beside(extra_row(), ln2))
        cd_prompt(self, t, P_REPO)
        resize(self, t, 3)
        clear(self)
        p1 = code("cheese-app-v0/api-service/api/routers/rag.py", 14, 23, cuts={19: "projects/129349313346/",
                                                                              22: "projects/129349313346/"})
        p1.move_to([0, 0.6, 0])
        self.play(FadeIn(p1), FadeIn(line_bar(p1.code, 22 - 14, ERR)))
        clear(self)
        p2 = code("llm-finetuning/gemini-finetuner/cli.py", 89, 96, font_size=20).move_to([0, 1.0, 0])
        rcard = readme_card(215, "Go to http://localhost:3200/chat, pick a collection, and ask a question",
                            size=20).move_to([0, -2.4, 0])
        self.play(FadeIn(p2), FadeIn(rcard))
        clear(self)
        chips_ = VGroup(your_turn(), extra_tag(), recorded_tag("recorded · rag.py:218–223"), recording_tag(),
                        erratum_tag(), illustration_tag(), preview_tag(), editor_tag(), cost_tag(),
                        future_cost_tag()).arrange_in_grid(cols=2, buff=0.25)
        chips_.move_to([0, 0.2, 0])
        self.play(FadeIn(chips_))
        clear(self)
        chips_ = VGroup(grey_chip("not on Docker Hub → built locally"),
                        dashed_chip("L13–L15"), tool_chip("gcloud"), err_chip("DefaultCredentialsError"),
                        file_card("secrets/llm-service-account.json", KEY), cost_row(), editor_row(),
                        time_row()).arrange_in_grid(cols=2, buff=0.25)
        chips_.move_to([0, 0.2, 0])
        self.play(FadeIn(chips_))
        clear(self)
        hc = card(["This recording machine has no Google account.",
                   "The key file in the folder listings is an obviously invalid stand-in.",
                   "It was removed before the cloud steps."], head="one honest note")
        self.play(FadeIn(hc))
        clear(self)
