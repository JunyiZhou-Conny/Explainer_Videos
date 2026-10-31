"""S04 · A database of links (decision 0006 D:43-47, D:81, D:164-188; PR #38 extract.ts:10-20; ../SOURCES.md)

1. Postgres: user → family_link ← user, insurance_card → user; permission checks follow the links. Rejected: MongoDB
   「家长–学生关联、权限检查是典型的关系型查询」, SQLite 「单文件，不适合以后多人同时在线」.
2. One flexible JSON column: each insurance field {value, confidence, source, raw}; pgvector shipped in the image
   (`pgvector/pgvector:pg17`) but not needed today; drizzle-kit migrations, numbered, applied in the same order.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (DB_C, NARRATION, USER_C, WEB_C, clear, mono, option, sans, table_card, zh)

SAY = NARRATION["S04"]


class Database(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- links
        with self.voiceover(SAY[0]) as vo:
            pg = sans("Postgres", 32, DB_C).move_to(UP * 3.1)
            student = table_card("user", ["role: student"], DB_C, 2.6).move_to(LEFT * 4.6 + UP * 1.4)
            parent = table_card("user", ["role: parent"], DB_C, 2.6).move_to(RIGHT * 4.6 + UP * 1.4)
            link = table_card("family_link", ["student → parent", "status"], USER_C, 3.0).move_to(UP * 1.4)
            card = table_card("insurance_card", ["fields (JSON)"], DB_C, 3.0).move_to(LEFT * 4.6 + DOWN * 0.7)
            arrows = VGroup(Arrow(link.get_left(), student.get_right(), color=S.GREY, buff=0.1),
                            Arrow(link.get_right(), parent.get_left(), color=S.GREY, buff=0.1),
                            Arrow(card.get_top(), student.get_bottom(), color=S.GREY, buff=0.1))
            vo.wait_until("Postgres")
            self.play(FadeIn(pg), FadeIn(student), FadeIn(parent), run_time=0.5)
            vo.wait_until("a parent is linked")
            self.play(FadeIn(link), Create(arrows[0]), Create(arrows[1]), FadeIn(card), Create(arrows[2]), run_time=0.8)
            vo.wait_until("follows that link")
            ask = VGroup(sans("may this parent see this card?", 24, USER_C),
                         sans("→ follow the link, then the card", 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            ask.move_to(RIGHT * 2.6 + DOWN * 0.7)
            path = VGroup(Line(parent.get_left(), link.get_right(), color=USER_C, stroke_width=6),
                          Line(link.get_left(), student.get_right(), color=USER_C, stroke_width=6),
                          Line(student.get_bottom(), card.get_top(), color=USER_C, stroke_width=6))
            self.play(FadeIn(ask), Create(path), run_time=1.0)
            lost = VGroup(option("MongoDB", "家长–学生关联、权限检查是典型的关系型查询", False, width=5.8),
                          option("SQLite", "单文件，不适合以后多人同时在线", False, width=5.8)).arrange(RIGHT, buff=0.3)
            lost.move_to(DOWN * 2.6)
            vo.wait_until("MongoDB lost")
            self.play(FadeIn(lost[0]), run_time=0.4)
            vo.wait_until("SQLite")
            self.play(FadeIn(lost[1]), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- a flexible column, an open door, migrations
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            cell = VGroup(mono("memberId", 26, USER_C),
                          VGroup(*[VGroup(mono(k, 22, DB_C), sans(v, 22, S.GREY)).arrange(RIGHT, buff=0.3) for k, v in
                                   [("value", "the text as read"), ("confidence", "how sure the reader was"),
                                    ("source", "front · back · text · user"), ("raw", "the raw text it came from")]]
                                 ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            frame = SurroundingRectangle(cell, color=DB_C, buff=0.3, corner_radius=0.14)
            box = VGroup(frame, cell).move_to(LEFT * 3.3 + UP * 1.4)
            note = sans("one insurance field, one JSON cell", 22, S.GREY).next_to(box, UP, buff=0.15)
            vo.wait_until("flexible on purpose")
            self.play(FadeIn(box), FadeIn(note), run_time=0.6)
            door = VGroup(RoundedRectangle(width=2.6, height=2.0, corner_radius=0.1, stroke_color=S.GREY, stroke_width=2.5),
                          VGroup(mono("pgvector", 24, S.GREY), sans("search by meaning", 20, S.GREY), sans("not needed today", 20, S.GREY)
                                 ).arrange(DOWN, buff=0.08))
            door[1].move_to(door[0])
            door.move_to(RIGHT * 3.6 + UP * 1.4)
            vo.wait_until("an add-on for searching by meaning")
            self.play(FadeIn(door), run_time=0.5)
            vo.wait_until("an open door, not a plan")
            self.play(Rotate(door[0], angle=-0.35, axis=UP, about_point=door[0].get_left()), run_time=0.6)
            files = VGroup(*[VGroup(RoundedRectangle(width=1.0, height=0.6, corner_radius=0.08, stroke_color=WEB_C, stroke_width=2),
                                    mono(f"{i:04d}", 22, WEB_C)) for i in (1, 2, 3)])
            for f in files:
                f[1].move_to(f[0])
            files.arrange(RIGHT, buff=0.2).move_to(LEFT * 2.6 + DOWN * 1.9)
            lab = sans("migration files, numbered", 22, S.GREY).next_to(files, UP, buff=0.15)
            dbs = VGroup(*[VGroup(Circle(radius=0.45, color=DB_C, stroke_width=2.5), sans(t, 20, S.GREY)) for t in ("laptop A", "laptop B")])
            for d in dbs:
                d[1].next_to(d[0], DOWN, buff=0.1)
            dbs.arrange(RIGHT, buff=0.8).move_to(RIGHT * 3.4 + DOWN * 1.9)
            vo.wait_until("numbered migration files")
            self.play(FadeIn(lab), LaggedStart(*[FadeIn(f) for f in files], lag_ratio=0.2), run_time=0.7)
            vo.wait_until("ends up the same")
            arrows = VGroup(*[Arrow(files.get_right(), d.get_left(), color=S.GREY, buff=0.15) for d in dbs])
            same = sans("same tables", 22, DB_C).next_to(dbs, UP, buff=0.15)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), FadeIn(same), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
