"""S07 · Checking the spoken answer (services/voice/nova_sonic/text_eval.py, READ IN CODE).

1. A test call → two transcripts → text_eval compares with a person's reference answer: word error rate of
   the caller's words, word cosine of the answer, required / forbidden phrases, whether a lookup ran and
   returned passages.
2. Word cosine = angle between two bags of word counts. Trap (made-up example): $4,855 vs $5,855 → 0.93
   with his text_cosine. RAG_RANKING_CHUNKING_VOICE_EVAL.md: "Similarity is not correctness".
3. The gold file today: 1 question, marked a starter; the notes ask for 20–30 checked ones.
"""

from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.scene import VoiceScene

from common import (BAD_C, CODE_C, DATA_C, MARCO_C, NARRATION, OK_C, QUERY_C, container, mark_bad, mono, sans,
                    serif, source_tag, text_panel)

SAY = NARRATION["S07"]
A = "For 2026 the monthly income limit for one person is $4,855."
B = "For 2026 the monthly income limit for one person is $5,855."


def bag(sentence: str) -> dict:
    import re
    from collections import Counter
    return Counter(re.findall(r"[\w']+", sentence.casefold()))


def cosine(a: dict, b: dict) -> float:
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    na = sum(v * v for v in a.values()) ** 0.5
    nb = sum(v * v for v in b.values()) ** 0.5
    return dot / (na * nb)


class TextEval(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- what text_eval compares
        with self.voiceover(SAY[0]) as vo:
            hdr = VGroup(sans("THE FOURTH DIAL: CHECKING ANSWERS", 22, MARCO_C), mono("text_eval.py", 22, S.GREY),
                         source_tag("code")).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
            self.play(FadeIn(hdr), run_time=0.6)
            caller = text_panel(["CALLER (transcript)", "… does Medicaid pay", "for someone to come", "to the house …"],
                                size=20, colors={0: S.GREY})
            agent = text_panel(["ASSISTANT (transcript)", "New Jersey Medicaid", "may cover help with", "daily activities …"],
                               size=20, colors={0: S.GREY}, border=CODE_C)
            tr = VGroup(caller, agent).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3)
            vo.wait_until("A test call produces")
            self.play(FadeIn(caller, shift=RIGHT * 0.15), run_time=0.6)
            self.play(FadeIn(agent, shift=RIGHT * 0.15), run_time=0.6)
            ev = container("text_eval", "compares", width=2.3, name_size=26).move_to(DOWN * 0.3 + LEFT * 0.35)
            gold = VGroup(person_icon(S.WHITE, height=0.45),
                          text_panel(["REFERENCE ANSWER", "written by a person"], size=20, colors={0: S.GREY}, border=OK_C)
                          ).arrange(RIGHT, buff=0.15).next_to(ev, UP, buff=0.6)
            a1 = Arrow(tr.get_right(), ev.get_left(), buff=0.12, color=S.GREY, stroke_width=3)
            a2 = Arrow(gold.get_bottom(), ev.get_top(), buff=0.1, color=OK_C, stroke_width=3)
            vo.wait_until("A script compares")
            self.play(FadeIn(ev), GrowArrow(a1), run_time=0.7)
            self.play(FadeIn(gold), GrowArrow(a2), run_time=0.7)
            checks = VGroup(*[VGroup(Dot(radius=0.05, color=QUERY_C), serif(t, 24)).arrange(RIGHT, buff=0.15) for t in
                              ["shared words with the reference (word cosine)",
                               "required and forbidden phrases",
                               "did the agent look anything up?",
                               "did the lookup return passages?",
                               "how well the caller's words were heard (WER)"]]
                            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            room = 7.0 - 0.3 - (ev.get_right()[0] + 0.6)
            if checks.width > room:
                checks.scale_to_fit_width(room)
            checks.next_to(ev, RIGHT, buff=0.6)
            assert tr.get_right()[0] < ev.get_left()[0] - 0.3, "transcripts overlap text_eval"
            a3 = Arrow(ev.get_right(), checks.get_left(), buff=0.1, color=S.GREY, stroke_width=3)
            vo.wait_until("shared words")
            self.play(GrowArrow(a3), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in checks], lag_ratio=0.3), run_time=2.0)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the word-cosine trap
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            sa = VGroup(sans("REFERENCE", 18, OK_C), serif(A, 28)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            sb = VGroup(sans("ANSWER", 18, CODE_C), serif(B, 28)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            sents = VGroup(sa, sb).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(UP, buff=0.6)
            tag = VGroup(source_tag("inferred", "made-up example")).next_to(sents, RIGHT, buff=0.3).align_to(sents, UP)
            if tag.get_right()[0] > 7.0:
                tag.next_to(sents, DOWN, buff=0.2).align_to(sents, RIGHT)
            self.play(FadeIn(sa), FadeIn(sb), FadeIn(tag), run_time=0.8)
            vo.wait_until("this time over word counts")
            ba, bb = bag(A), bag(B)
            words = list(dict.fromkeys(list(ba) + list(bb)))

            def row(b, col):
                return VGroup(*[VGroup(mono(w, 20, S.WHITE if b.get(w, 0) else S.GREY_DARK),
                                       mono(str(b.get(w, 0)), 22, col if b.get(w, 0) else S.GREY_DARK)).arrange(DOWN, buff=0.06)
                                for w in words]).arrange(RIGHT, buff=0.26)

            ra, rb = row(ba, OK_C), row(bb, CODE_C)
            bags = VGroup(VGroup(sans("WORD COUNTS", 18, S.GREY)), ra, rb).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            if bags.width > 13:
                bags.scale_to_fit_width(13)
            bags.move_to(DOWN * 0.5)
            self.play(FadeIn(bags[0]), FadeIn(ra), run_time=0.8)
            self.play(FadeIn(rb), run_time=0.8)
            vo.wait_until("That has a trap")
            diff = [i for i, w in enumerate(words) if ba.get(w, 0) != bb.get(w, 0)]
            boxes = VGroup(*[SurroundingRectangle(VGroup(ra[i], rb[i]), color=BAD_C, buff=0.08) for i in diff])
            self.play(Create(boxes), run_time=0.7)
            val = cosine(ba, bb)
            res = VGroup(mono(f"word cosine = {val:.2f}", 34, QUERY_C), serif("almost the same", 26, S.GREY),
                         mono("→", 30, S.GREY), serif("wrong number", 30, BAD_C)).arrange(RIGHT, buff=0.25)
            res.to_edge(DOWN, buff=1.2)
            self.play(FadeIn(res[:2]), run_time=0.7)
            self.play(FadeIn(res[2:]), run_time=0.6)
            vo.wait_until("Marco's notes say it plainly")
            q = VGroup(source_tag("notes"), serif('"Similarity is not correctness"', 30, MARCO_C)).arrange(RIGHT, buff=0.25)
            q.to_edge(DOWN, buff=0.4)
            self.play(FadeIn(q), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- the gold file today
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            gold = text_panel(['evaluation/medicaid_voice_gold.json',
                               '{',
                               '  "reference_question": "Hi my mother lives in New Jersey does',
                               '      Medicaid pay for someone to come to the house to help her",',
                               '  "reference_answer": "New Jersey Medicaid may cover help with …',
                               '      Eligibility cannot be promised …",',
                               '  "required_phrases": [],',
                               '  "prohibited_phrases": ["guaranteed eligible", "automatically qualified"]',
                               '}'], size=20, colors={0: S.GREY}, t2c={"prohibited_phrases": BAD_C})
            if gold.width > 12.5:
                gold.scale_to_fit_width(12.5)
            gold.move_to(UP * 0.9)
            one = VGroup(mono("1", 44, QUERY_C), serif("reference answer today", 28)).arrange(RIGHT, buff=0.2)
            one.next_to(gold, DOWN, buff=0.4).align_to(gold, LEFT)
            self.play(FadeIn(gold, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(one), run_time=0.5)
            vo.wait_until("marked as a starter")
            note = VGroup(source_tag("notes"), serif('"a starter, not a reviewed legal reference"', 24, S.GREY)
                          ).arrange(RIGHT, buff=0.2).next_to(one, RIGHT, buff=0.6)
            self.play(FadeIn(note), run_time=0.6)
            vo.wait_until("Real testing needs")
            need = VGroup(serif("needed:", 28, S.GREY), mono("20–30", 36, QUERY_C), serif("checked reference answers", 28)
                          ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(need, shift=UP * 0.1), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
