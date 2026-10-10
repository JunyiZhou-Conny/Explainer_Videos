"""S01 · Two halves.

1. The system map builds: the top half (source list → five containers → S3 prefixes → Knowledge
   Base), then the bottom half (caller → voice ↔ Nova 2 Sonic; voice → lookup_program_info →
   retrieve → Knowledge Base).
2. The bottom half dims; the top half is outlined; the map leaves; the episode title.
3. A caller's question (YELLOW) and the passage that answers it (the JACC page, verbatim), with
   "$4,855 for an individual" lit; "answer from memory" is struck out.
4. The passage shrinks to a dot "1 of 232", which drops into the Knowledge Base of the returning
   map; a token runs the chain from the source list to the Knowledge Base.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AWS_C, BAD_C, CODE_C, DATA_C, NARRATION, QUERY_C, chip, mono, serif, strike,
                    system_map, text_panel, token)

SAY = NARRATION["S01"]

# The JACC page, as extracted by the team's code (videos/careonex-series/checks), verbatim.
JACC_LINES = [
    "Who is eligible for JACC?",
    "- Is 60 years of age or older",
    "- Resides within the community (not in a facility)",
    "- Meets financial eligibility requirements:",
    "  - Having a monthly income that is not greater than",
    "    365% of the Federal poverty level ($4,855 for an",
    "    individual; $6,582 for a married couple in 2026).",
]


class TwoHalves(VoiceScene):
    def construct(self):
        m = system_map()
        P, L = m.part, m.links
        chain = ["catalog", "data", "ingest", "extract", "chunk", "kb-sync"]
        prefixes = ["snapshots/", "raw/", "text/", "chunks/", "config/"]

        # 1 ---------------------------------------------------------------- build the map
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(m.h1, shift=RIGHT * 0.2), run_time=0.6)
            steps = []
            for a, b in zip(chain, chain[1:] + [None]):
                steps.append(FadeIn(P[a], shift=DOWN * 0.15))
                if b:
                    steps.append(GrowArrow(L[f"{a}>{b}"].arrow))
            self.play(LaggedStart(*steps, lag_ratio=0.35), run_time=2.6)
            self.play(Create(P["bucket"][0]), FadeIn(P["bucket"].label),
                      LaggedStart(*[AnimationGroup(GrowArrow(L[f"{a}>{b}"].arrow), FadeIn(P[b]))
                                    for a, b in zip(chain[1:], prefixes)], lag_ratio=0.25), run_time=2.0)
            self.play(GrowArrow(L["chunks>kb"].arrow), FadeIn(P["kb"], shift=DOWN * 0.15), run_time=1.0)
            vo.wait_until("One half talks")
            self.play(FadeIn(m.h2, shift=RIGHT * 0.2), FadeIn(P["caller"]), run_time=0.7)
            self.play(GrowArrow(L["caller>voice"].arrow), FadeIn(P["voice"]), run_time=0.7)
            self.play(GrowArrow(L["voice>nova"].arrow), FadeIn(P["nova"]), run_time=0.7)
            self.play(GrowArrow(L["voice>tools"].arrow), FadeIn(P["tools"]),
                      GrowArrow(L["tools>retrieve"].arrow), FadeIn(P["retrieve"]),
                      GrowArrow(L["retrieve>kb"].arrow), run_time=1.2)
            vo.wait_until("The other half")
            self.play(Indicate(m.build, scale_factor=1.02, color=WHITE), run_time=1.2)

        # 2 ---------------------------------------------------------------- this episode
        with self.voiceover(SAY[1]) as vo:
            self.play(m.answer.animate.set_opacity(0.15), run_time=0.8)
            outline = SurroundingRectangle(VGroup(m.build, P["kb"]), buff=0.12, corner_radius=0.2,
                                           color=WHITE, stroke_width=2)
            self.play(Create(outline), run_time=1.0)
            self.wait(1.0)
            self.play(FadeOut(m), FadeOut(outline), run_time=0.8)
            ep = serif("E2", 40, S.GREY)
            name = serif("Building the library", 64)
            sub = serif("5 containers · 20 documents → 232 passages", 32, S.GREY)
            card = VGroup(ep, name, sub).arrange(DOWN, buff=0.3)
            self.play(FadeIn(ep, shift=UP * 0.2), Write(name), run_time=1.4)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.8)
            self.wait(max(0.3, vo.remaining() - 0.8))
            self.play(FadeOut(card), run_time=0.7)

        # 3 ---------------------------------------------------------------- why a library
        with self.voiceover(SAY[2]) as vo:
            q = chip("What is the JACC income limit for one person?", QUERY_C, size=28, mono_font=False)
            q.to_edge(UP, buff=0.7)
            caller = serif("a caller asks", 24, S.GREY).next_to(q, LEFT, buff=0.3)
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(caller), run_time=1.0)
            panel = text_panel(JACC_LINES, size=24, colors={0: S.GREY}, border=DATA_C,
                               t2c={"$4,855 for an": QUERY_C, "individual;": QUERY_C})
            panel.next_to(q, DOWN, buff=0.6)
            tag = chip("JACC page · nj.gov · 2026", DATA_C, size=22).next_to(panel, DOWN, buff=0.25).align_to(panel, RIGHT)
            arrow = Arrow(q.get_bottom(), panel.get_top(), buff=0.08, color=S.GREY, stroke_width=3)
            self.play(GrowArrow(arrow), FadeIn(panel, shift=UP * 0.2), run_time=1.2)
            self.play(FadeIn(tag), run_time=0.6)
            vo.wait_until("It is not allowed")
            box = SurroundingRectangle(VGroup(panel.rows[5], panel.rows[6]), color=QUERY_C, buff=0.06,
                                       corner_radius=0.06, stroke_width=2)
            self.play(Create(box), run_time=0.8)
            mem = chip("answer from memory", BAD_C, size=24, mono_font=False)
            mem.next_to(panel, DOWN, buff=0.25).align_to(panel, LEFT)
            self.play(FadeIn(mem), run_time=0.6)
            st = strike(mem, BAD_C)
            self.play(Create(st), run_time=0.6)
            vo.wait_until("because these numbers")
            self.play(Indicate(VGroup(panel.rows[6]), color=QUERY_C), run_time=1.2)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- one of 232
        with self.voiceover(SAY[3]) as vo:
            dot = Dot(radius=0.12, color=DATA_C).move_to(panel)
            others = VGroup(q, caller, arrow, tag, mem, box, st)
            self.play(FadeOut(others), ReplacementTransform(panel, dot), run_time=1.0)
            one = mono("1 of 232", 26, DATA_C).next_to(dot, RIGHT, buff=0.2)
            self.play(FadeIn(one), run_time=0.5)
            m2 = system_map()
            m2.answer.set_opacity(0.15)
            self.play(FadeIn(m2.build), FadeIn(m2.part["kb"]), FadeIn(m2.links["chunks>kb"]),
                      FadeIn(m2.answer), dot.animate.move_to(m2.part["kb"].frame.get_center()),
                      FadeOut(one), run_time=1.4)
            self.play(Flash(m2.part["kb"].frame, color=DATA_C, flash_radius=1.0), FadeOut(dot), run_time=0.7)
            vo.wait_until("Let's follow")
            path = [m2.part[k].frame.get_center() for k in chain] + [m2.part["chunks/"].get_center(),
                                                                      m2.part["kb"].frame.get_center()]
            t = token(DATA_C, 0.15).move_to(path[0])
            halo = always_redraw(lambda: Circle(radius=0.28, color=DATA_C, stroke_width=3).move_to(t))
            self.play(FadeIn(t), FadeIn(halo), run_time=0.3)
            for b in path[1:]:
                self.play(t.animate.move_to(b), run_time=0.5, rate_func=smooth)
            halo.clear_updaters()
            self.play(Flash(m2.part["kb"].frame, color=AWS_C, flash_radius=1.0), FadeOut(t), FadeOut(halo),
                      run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.8))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
