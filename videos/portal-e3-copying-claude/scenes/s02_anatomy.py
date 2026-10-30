"""S02 · The parts of a chat page

1. The empty page; each part named as it is said: empty state, suggestion chips, composer, model menu,
   send key (which morphs into the stop key). Names: NN/g, Material, chat-UI kits (SOURCES.md).
2. The page after one turn (demo 01's first message, verbatim); named: user bubble, answer column,
   action row, scroll-to-bottom, disclaimer line.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (NARRATION, USER_C, clear, empty_page, sans, send_key, turn_page, zh)

SAY = NARRATION["S02"]
LABEL_X = 0.9   # names start here, right of the page


def name_tag(scene, target, text, y, zh_text=None, color=USER_C):
    """A name on the dark canvas at height y, with a line back to the part of the page."""
    words = sans(text, 26, color)
    lab = VGroup(words, zh(zh_text, 22, S.GREY)).arrange(RIGHT, buff=0.25) if zh_text else words
    lab.move_to([LABEL_X + lab.width / 2, y, 0])
    start = target.get_right() + RIGHT * 0.05
    start[1] = min(max(start[1], target.get_bottom()[1]), target.get_top()[1])
    end = lab.get_left() + LEFT * 0.12
    ln = Line(start, end, color=color, stroke_width=2)
    dot = Dot(start, radius=0.05, color=color)
    scene.play(Create(ln), FadeIn(dot), FadeIn(lab, shift=LEFT * 0.1), run_time=0.45)
    return VGroup(ln, dot, lab)


class Anatomy(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- before the first message
        with self.voiceover(SAY[0]) as vo:
            page = empty_page(6.0, 6.6).move_to(LEFT * 3.6)
            self.play(FadeIn(page), run_time=0.6)
            vo.wait_until("The empty state")
            t1 = name_tag(self, page.frame, "empty state", 3.0, "空白页")
            vo.wait_until("Suggestion chips")
            t2 = name_tag(self, page.chips, "suggestion chips", page.chips.get_center()[1], "建议")
            vo.wait_until("The composer")
            t3 = name_tag(self, page.composer.placeholder, "composer", page.composer.get_top()[1] - 0.1, "输入框")
            vo.wait_until("a model menu")
            t4 = name_tag(self, page.composer.menu, "model menu", page.composer.get_center()[1] - 0.15, "模型菜单")
            vo.wait_until("the send key")
            t5 = name_tag(self, page.composer.key, "send key", page.composer.get_bottom()[1] - 0.35, "发送键")
            vo.wait_until("turns into a stop key")
            stop = send_key(stop=True).move_to(page.composer.key)
            stop_lab = sans("→ stop key while you wait", 22, S.GREY).next_to(t5[2], RIGHT, buff=0.2)
            if stop_lab.get_right()[0] > 6.5:
                stop_lab.next_to(t5[2], DOWN, buff=0.12).align_to(t5[2], LEFT)
            self.play(Transform(page.composer.key, stop), FadeIn(stop_lab), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- after one turn
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            page2 = turn_page(6.0, 7.0).move_to(LEFT * 3.6)
            src = sans("a live turn, redrawn · text from demo 01", 20, S.GREY).move_to([LABEL_X + 2.6, -3.35, 0])
            self.play(FadeIn(page2.frame), FadeIn(page2.bar), FadeIn(page2.composer), FadeIn(page2.fine),
                      FadeIn(src), run_time=0.5)
            vo.wait_until("in a bubble")
            self.play(FadeIn(page2.bubble, shift=LEFT * 0.2), run_time=0.4)
            name_tag(self, page2.bubble, "user bubble", page2.bubble.get_center()[1], "用户气泡")
            vo.wait_until("full width without a box")
            self.play(FadeIn(page2.think), FadeIn(page2.answer, shift=UP * 0.1), run_time=0.5)
            name_tag(self, page2.answer, "answer column", page2.answer.get_center()[1], "回答")
            vo.wait_until("an action row")
            self.play(FadeIn(page2.actions), run_time=0.3)
            name_tag(self, page2.actions, "action row", page2.actions.get_center()[1] + 0.05, "复制 · 重新回答")
            vo.wait_until("a round button")
            self.play(FadeIn(page2.down, scale=1.2), run_time=0.3)
            name_tag(self, page2.down, "scroll-to-bottom", page2.down.get_center()[1] - 0.2, "回到最新")
            vo.wait_until("the disclaimer")
            name_tag(self, page2.fine, "disclaimer line", page2.fine.get_center()[1] - 0.1, "免责声明")
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
