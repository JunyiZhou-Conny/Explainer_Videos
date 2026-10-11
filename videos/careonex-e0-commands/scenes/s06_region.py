"""S06 · Where in the world: the region.

A simple world panel (a lat/long grid, no coastlines) with a few AWS regions as dots; us-east-1
(Northern Virginia) lit; the line `$env:AWS_DEFAULT_REGION = "us-east-1"`; tags READ IN CODE
(every service defaults to us-east-1) and TEAM NOTES (Nova 2 Sonic enabled there).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import AWS_C, NARRATION, QUERY_C, big_line, mono, sans, serif, source_tag

SAY = NARRATION["S06"]

# (code, place, longitude, latitude): a few real AWS regions, roughly placed
REGIONS = [("us-east-1", "N. Virginia", -77.5, 38.9, DOWN), ("us-west-2", "Oregon", -120.5, 45.6, UP),
           ("eu-west-1", "Ireland", -6.3, 53.3, UP), ("ap-northeast-1", "Tokyo", 139.7, 35.7, UP),
           ("ap-southeast-2", "Sydney", 151.2, -33.9, DOWN), ("sa-east-1", "São Paulo", -46.6, -23.5, DOWN),
           ("ap-south-1", "Mumbai", 72.9, 19.1, DOWN)]


class Region(VoiceScene):
    def construct(self):
        with self.voiceover(SAY[0]) as vo:
            line = big_line('$env:AWS_DEFAULT_REGION = "us-east-1"', 28).to_edge(UP, buff=0.45)
            self.play(FadeIn(line, shift=DOWN * 0.2), run_time=0.7)
            W, H = 11.0, 4.6
            box = Rectangle(width=W, height=H, stroke_color=S.GREY_DARK).move_to(DOWN * 0.7)
            grid = VGroup(*[Line(box.get_top() + RIGHT * (x - W / 2), box.get_bottom() + RIGHT * (x - W / 2),
                                 color=S.GREY_DARKER, stroke_width=1) for x in [W * i / 8 for i in range(1, 8)]],
                          *[Line(box.get_left() + UP * (y - H / 2), box.get_right() + UP * (y - H / 2),
                                 color=S.GREY_DARKER, stroke_width=1) for y in [H * i / 4 for i in range(1, 4)]])
            lab = sans("SOME AWS REGIONS (EACH A SEPARATE SET OF DATA CENTERS)", 20, S.GREY).next_to(box, UP, buff=0.1).align_to(box, LEFT)

            def at(lon, lat):
                return box.get_center() + RIGHT * (lon / 180 * W / 2) + UP * (lat / 90 * H / 2)

            dots = VGroup()
            for code, place, lon, lat, side in REGIONS:
                d = Dot(at(lon, lat), radius=0.09, color=AWS_C if code == "us-east-1" else S.GREY)
                t = VGroup(mono(code, 20, AWS_C if code == "us-east-1" else S.GREY),
                           serif(place, 20, S.GREY)).arrange(DOWN, buff=0.03).next_to(d, side, buff=0.1)
                dots.add(VGroup(d, t))
            self.play(Create(box), FadeIn(grid), FadeIn(lab), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(d, scale=0.7) for d in dots], lag_ratio=0.12), run_time=1.6)
            vo.wait_until("The team's models")
            ring = Circle(radius=0.32, color=QUERY_C, stroke_width=4).move_to(dots[0][0])
            self.play(Create(ring), Flash(dots[0][0], color=QUERY_C), run_time=1.0)
            tags = VGroup(VGroup(source_tag("code"), serif("every CareOneX service defaults to us-east-1", 22, S.GREY)).arrange(RIGHT, buff=0.25),
                          VGroup(source_tag("notes"), serif("Nova 2 Sonic is enabled for the team there", 22, S.GREY)).arrange(RIGHT, buff=0.25)
                          ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_edge(DOWN, buff=0.3)
            self.play(FadeIn(tags), run_time=0.7)
            vo.wait_until("so every program")
            self.play(Indicate(line, color=QUERY_C, scale_factor=1.03), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
