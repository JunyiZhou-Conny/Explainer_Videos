"""S04 · The turn at 9:21 (decision 0004; commit 8f13b18, Tue 21:21 Boston = Wed 09:21 Beijing; when the call
   itself was made is not recorded)

1. A word-list engine: some urgent symptoms slip through, some harmless words trip it, a patch here breaks
   something there. 0004: 「词表（keyword spotting）同时有漏判和误报，越补越多，补一处又会坏另一处。」
2. The new shape: a demo first, evaluation later; the model judges; the checker on its output is the only safety
   layer. 0004, written by the agent, records it as the owner's decision; the rules engine and the experiments stay in the repo, 「不再推进」.
3. Ponder: the checker is made of word rules too.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, MODEL_C, NARRATION, OURS_C, USER_C, clear, link, mark_bad, model_box,
                    ours_box, ponder_zh, quote_panel, sans, tag_box, zh)

SAY = NARRATION["S04"]


class Turn(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- word lists
        with self.voiceover(SAY[0]) as vo:
            when = VGroup(sans("Tue 21:21 Boston · commit 8f13b18", 30, USER_C), sans("Wed 09:21 Beijing · the date decision 0004 uses", 22, S.GREY)
                          ).arrange(DOWN, buff=0.08).move_to(UP * 3.0)
            self.play(FadeIn(when), run_time=0.5)
            vo.wait_until("matched words")
            engine = tag_box("rules", "word lists", "match a symptom → urgency", MODEL_C, width=4.2).move_to(UP * 0.6)
            self.play(FadeIn(engine), run_time=0.4)
            ins = VGroup(zh("胸口发闷", 24), zh("喘不上气", 24), zh("不想吃饭", 24)).arrange(DOWN, buff=0.35).move_to(LEFT * 4.6 + UP * 0.6)
            illus = sans("illustration", 20, S.GREY).next_to(ins, DOWN, buff=0.2)
            self.play(FadeIn(ins), FadeIn(illus), run_time=0.4)
            vo.wait_until("missed things")
            miss = VGroup(mark_bad(0.25, DANGER_C), sans("missed: said another way", 22, DANGER_C)).arrange(RIGHT, buff=0.15)
            miss.move_to(RIGHT * 4.2 + UP * 1.4)
            self.play(FadeIn(miss), Indicate(ins[1], color=DANGER_C, scale_factor=1.05), run_time=0.6)
            vo.wait_until("flagged the wrong things")
            fa = VGroup(mark_bad(0.25, DANGER_C), sans("false alarm: a harmless word", 22, DANGER_C)).arrange(RIGHT, buff=0.15)
            fa.move_to(RIGHT * 4.2 + UP * 0.4)
            self.play(FadeIn(fa), Indicate(ins[2], color=DANGER_C, scale_factor=1.05), run_time=0.6)
            vo.wait_until("every patch")
            q = quote_panel("词表（keyword spotting）同时有漏判和误报，越补越多，补一处又会坏另一处。", "decision 0004",
                            width=10.6, size=26).move_to(DOWN * 2.3)
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the model judges; the checker guards
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(ins, illus, miss, fa, q)), engine.animate.set_opacity(0.3).move_to(LEFT * 4.3 + DOWN * 2.6),
                      run_time=0.5)
            shelved = sans("kept in the repo · 「不再推进」", 22, S.GREY).next_to(engine, UP, buff=0.12)
            vo.wait_until("you decided")
            q2 = quote_panel("Junyi 2026-10-28 决定：先做能演示的 MVP，评估以后再做。紧急程度和去处交给推理模型判断，不再由确定性规则或正则词表决定。",
                             "decision 0004 · written by the agent", width=11.6, size=24, color=USER_C).move_to(UP * 1.4)
            self.play(FadeIn(q2, shift=DOWN * 0.1), run_time=0.6)
            m = model_box("the model", "judges urgency and where to go", width=4.4).move_to(LEFT * 3.2 + DOWN * 0.6)
            c = ours_box("the checker", "the only safety layer", width=3.4).move_to(RIGHT * 2.2 + DOWN * 0.6)
            arr = link(m, c, S.GREY, label="its output", label_size=20)
            vo.wait_until("the model judges")
            self.play(FadeIn(m, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("the checker on its output")
            self.play(Create(arr), FadeIn(c, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("stay in the repository")
            self.play(FadeIn(shelved), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- ponder
        with self.voiceover(SAY[2]) as vo:
            self.play(*[mob.animate.set_opacity(0.15) for mob in self.mobjects], run_time=0.4)
            card = ponder_zh(self, "The checker is word rules too. What would make it less of a whack-a-mole?",
                             "检查器本身也是词规则。怎样才能不再按下葫芦浮起瓢？", seconds=4.0)
        self.wait(3.5)
        clear(self)
