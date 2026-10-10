"""S09 · Boxes: docker compose up --build retrieve.

1. An image = a frozen box with layers (python:3.12-slim · uv · retrieve's libraries · retrieve's
   code), from services/retrieve/Dockerfile; a container = a running copy. READ IN CODE.
2. The command, each word explained in turn: docker compose (reads docker-compose.yml: 7 services) ·
   up · --build · retrieve.
3. The running retrieve container: a FastAPI web server with GET /health and POST /retrieve on port
   8080, connected to the laptop's port 8080 (`ports: "8080:8080"`). READ IN CODE.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CODE_C, DATA_C, NARRATION, PERSON_C, QUERY_C, big_line, container, laptop, mono, sans, serif,
                    source_tag, text_panel)

SAY = NARRATION["S09"]


class Docker(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- image vs container
        with self.voiceover(SAY[0]) as vo:
            layers = ["python 3.12 (slim Linux)", "uv (installs Python libraries)", "retrieve's libraries (FastAPI, boto3 …)",
                      "retrieve's own code"]
            boxes = VGroup(*[VGroup(Rectangle(width=5.4, height=0.55, stroke_color=CODE_C, stroke_width=2)
                                    .set_fill(CODE_C, 0.08 + 0.06 * i),
                                    serif(t, 22)) for i, t in enumerate(layers)])
            for b in boxes:
                b[1].move_to(b[0])
            boxes.arrange(UP, buff=0)
            img = VGroup(sans("IMAGE: A FROZEN BOX", 22, CODE_C), boxes).arrange(DOWN, buff=0.2).move_to(LEFT * 3.4 + UP * 0.9)
            src = VGroup(mono("services/retrieve/Dockerfile", 20, S.GREY), source_tag("code")).arrange(RIGHT, buff=0.25)
            src.next_to(img, DOWN, buff=0.25).align_to(img, LEFT)
            self.play(FadeIn(img[0]), LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in boxes], lag_ratio=0.3), run_time=1.6)
            self.play(FadeIn(src), run_time=0.4)
            vo.wait_until("A container is")
            run = container("retrieve", "running", width=3.6, name_size=30, sub_size=22).move_to(RIGHT * 3.4 + UP * 1.3)
            arrow = Arrow(img.get_right(), run.frame.get_left(), buff=0.2, color=S.GREY, stroke_width=3)
            al = serif("start a copy", 22, S.GREY).next_to(arrow, UP, buff=0.08)
            dot = Dot(radius=0.09, color=S.GREEN).next_to(run.name, RIGHT, buff=0.3)
            self.play(GrowArrow(arrow), FadeIn(al), FadeIn(run, shift=LEFT * 0.2), run_time=0.9)
            self.play(FadeIn(dot), Flash(dot, color=S.GREEN), run_time=0.6)
            vo.wait_until("It runs the same")
            same = VGroup(*[VGroup(laptop(1.3, 0.85, l), ) for l in ("Marco", "you", "a server")]).arrange(RIGHT, buff=0.35)
            same.move_to(DOWN * 2.3)
            sl = serif("the same box runs anywhere", 24, S.GREY).next_to(same, DOWN, buff=0.15)
            same.add(sl)
            self.play(LaggedStart(*[FadeIn(x) for x in same], lag_ratio=0.3), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the command, word by word
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            words = VGroup(mono("docker compose", 40), mono("up", 40), mono("--build", 40), mono("retrieve", 40)
                           ).arrange(RIGHT, buff=0.45).move_to(UP * 2.3)
            self.play(FadeIn(words), run_time=0.7)
            expl = ["reads docker-compose.yml", "start it", "rebuild the image first", "only this service"]
            exps = VGroup()
            for w, e in zip(words, expl):
                u = Underline(w, color=QUERY_C, buff=0.06)
                t = serif(e, 24, QUERY_C).next_to(u, DOWN, buff=0.15 if len(exps) % 2 == 0 else 0.75)
                exps.add(VGroup(u, t))
            yml = text_panel(["services:", "  data:", "  ingest:", "  extract:", "  chunk:", "  kb-sync:",
                              "  retrieve:   ← this one", "  voice:"], size=20, colors={6: QUERY_C})
            yml.move_to(DOWN * 1.4 + LEFT * 3.6)
            anchors = ["Docker compose reads", "The word up", "The option build", "And retrieve picks"]
            for k, a in enumerate(anchors):
                vo.wait_until(a)
                self.play(words[k].animate.set_color(QUERY_C), FadeIn(exps[k], shift=UP * 0.1), run_time=0.6)
                if k == 0:
                    self.play(FadeIn(yml, shift=UP * 0.15), run_time=0.6)
                if k == 2:
                    hammer = serif("Marco's newest code goes in", 24, S.GREY).move_to(RIGHT * 2.6 + DOWN * 1.2)
                    self.play(FadeIn(hammer), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- a web server on port 8080
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            lap = laptop(12.4, 5.2, "the laptop").move_to(DOWN * 0.1)
            box = RoundedRectangle(width=6.0, height=3.2, corner_radius=0.15, stroke_color=CODE_C, stroke_width=3).set_fill(CODE_C, 0.06)
            box.move_to(lap.screen).shift(LEFT * 2.2)
            bt = VGroup(sans("CONTAINER", 20, CODE_C), mono("retrieve", 30), serif("a small web server (FastAPI)", 22, S.GREY)
                        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(box.get_corner(UL), DR, buff=0.2)
            doors = VGroup(mono("GET  /health", 24, S.WHITE), mono("POST /retrieve", 24, QUERY_C)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            doors.next_to(bt, DOWN, buff=0.35).align_to(bt, LEFT)
            self.play(Create(lap.screen), FadeIn(lap[1]), FadeIn(lap.label), run_time=0.8)
            self.play(FadeIn(box), FadeIn(bt), run_time=0.7)
            self.play(FadeIn(doors), run_time=0.7)
            vo.wait_until("It listens on port 8080")
            p_in = VGroup(Circle(radius=0.45, color=QUERY_C, stroke_width=3), mono("8080", 20, QUERY_C))
            p_in[1].move_to(p_in[0])
            p_in.move_to(box.get_right())
            p_out = p_in.copy().move_to(lap.screen.get_right() + LEFT * 1.0)
            pl = serif("port = a numbered door", 24, QUERY_C).next_to(p_in, DOWN, buff=0.3).shift(RIGHT * 1.0)
            self.play(FadeIn(p_in, scale=1.3), FadeIn(pl), run_time=0.8)
            vo.wait_until("The Docker file connects")
            pipe = Line(p_in.get_right(), p_out.get_left(), color=QUERY_C, stroke_width=6)
            pmap = mono('ports: "8080:8080"', 22, S.GREY).next_to(pipe, UP, buff=0.15)
            self.play(Create(pipe), FadeIn(p_out), FadeIn(pmap), run_time=1.0)
            tag = source_tag("code", "docker-compose.yml, retrieve's app.py").next_to(lap, DOWN, buff=0.15)
            if tag.get_bottom()[1] < -3.6:
                tag.to_edge(DOWN, buff=0.3)
            self.play(FadeIn(tag), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
