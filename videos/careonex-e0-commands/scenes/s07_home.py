"""S07 · The strange one: $env:HOME = $HOME.

1. The line, with a question mark.
2. docker-compose.yml: `- ${HOME}/.aws:/home/app/.aws` (READ IN CODE); a tunnel from the laptop folder
   C:\\Users\\Marco\\.aws (with the 8-hour key) into the container's /home/app/.aws.
3. Mac/Linux vs. Windows PowerShell: HOME set vs. empty (the tunnel points at "/.aws", RED); the
   line copies PowerShell's $HOME into the environment. INFERRED, with the reason; note: the team's
   setup guide is written for macOS (TEAM NOTES).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BAD_C, CODE_C, DATA_C, NARRATION, OK_C, QUERY_C, big_line, code_panel, container,
                    mark_bad, mark_ok, mono, sans, serif, source_tag, text_panel)

SAY = NARRATION["S07"]


class Home(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the line
        with self.voiceover(SAY[0]) as vo:
            line = big_line("$env:HOME = $HOME", 44).move_to(UP * 0.4)
            q = mono("?", 72, QUERY_C).next_to(line, RIGHT, buff=0.4)
            self.play(FadeIn(line, scale=0.9), run_time=0.8)
            self.play(FadeIn(q, scale=1.5), run_time=0.5)
            vo.wait_until("It fixes")
            fix = serif("a Windows fix", 32, QUERY_C).next_to(line, DOWN, buff=0.5)
            self.play(FadeIn(fix), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- what Docker needs
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(q), FadeOut(fix), line.animate.scale(0.6).to_corner(UL, buff=0.4), run_time=0.7)
            yml = text_panel(["retrieve:", "  volumes:", "    - ${HOME}/.aws:/home/app/.aws", "    - ./data:/data"],
                             size=24, t2c={"${HOME}": QUERY_C})
            yml.move_to(UP * 1.6)
            src = VGroup(mono("docker-compose.yml (shortened)", 20, S.GREY), source_tag("code")
                         ).arrange(RIGHT, buff=0.3).next_to(yml, DOWN, buff=0.15).align_to(yml, LEFT)
            self.play(FadeIn(yml, shift=DOWN * 0.15), FadeIn(src), run_time=0.9)
            left = VGroup(sans("LAPTOP FOLDER", 20, S.GREY), mono("C:\\Users\\Marco\\.aws", 26, DATA_C),
                          serif("your 8-hour login key", 22, S.GREY)).arrange(DOWN, buff=0.08).move_to(LEFT * 4.0 + DOWN * 1.6)
            box = container("retrieve", "a sealed box", width=3.6, name_size=28, sub_size=22).move_to(RIGHT * 3.6 + DOWN * 1.6)
            inner = mono("/home/app/.aws", 24, DATA_C).next_to(box, DOWN, buff=0.15)
            self.play(FadeIn(left), FadeIn(box), FadeIn(inner), run_time=0.8)
            vo.wait_until("The team's Docker file")
            tunnel = Arrow(left.get_right(), box.frame.get_left(), buff=0.2, color=QUERY_C, stroke_width=6)
            tl = serif("found through HOME", 24, QUERY_C).next_to(tunnel, UP, buff=0.1)
            self.play(GrowArrow(tunnel), FadeIn(tl), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- Mac vs Windows
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(yml, src, left, box, inner, tunnel, tl)), run_time=0.6)
            mac = VGroup(sans("MAC / LINUX", 22, S.GREY), mono("HOME = /Users/marco", 26), mark_ok(0.4),
                         mono("/Users/marco/.aws", 24, DATA_C)).arrange(DOWN, buff=0.25)
            win = VGroup(sans("WINDOWS POWERSHELL", 22, S.GREY), mono("HOME = (not set)", 26, BAD_C), mark_bad(0.34),
                         mono("/.aws  → no login", 24, BAD_C)).arrange(DOWN, buff=0.25)
            VGroup(mac, win).arrange(RIGHT, buff=2.4).move_to(UP * 0.5)
            self.play(FadeIn(mac, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("On Windows it is not")
            self.play(FadeIn(win, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("The line copies")
            fixed = mono("HOME = C:\\Users\\Marco", 26, OK_C).move_to(win[1])
            self.play(Transform(win[1], fixed), win[2].animate.become(mark_ok(0.4).move_to(win[2])),
                      win[3].animate.become(mono("C:\\Users\\Marco\\.aws", 24, DATA_C).move_to(win[3])), run_time=1.0)
            why = VGroup(source_tag("inferred"),
                         serif("from docker-compose.yml and how PowerShell keeps $HOME to itself", 22, S.PURPLE)
                         ).arrange(RIGHT, buff=0.25)
            note = VGroup(source_tag("notes"), serif("the team's setup guide is written for macOS", 22, S.GREY)).arrange(RIGHT, buff=0.25)
            VGroup(why, note).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(why), run_time=0.6)
            vo.wait_until("Only terminal 1")
            self.play(FadeIn(note), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
