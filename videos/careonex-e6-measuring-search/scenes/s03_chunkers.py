"""S03 · Three ways to cut, three test libraries.

1. One document cut three ways (READ IN CODE):
   A legacy (v2, E2's chunker): ~1,600-character pieces, up to 2,800; short sections can be merged.
   B section-safe (v4): every piece belongs to one heading; tables repeat their header row; 120 chars of
     prose overlap.
   C hierarchical: children of ~950 characters are searched; each points to a parent of up to 2,400.
2. Three staging Knowledge Bases (masked IDs), the main library untouched; C = the ID in E0.
3. 25 questions × 3 libraries × top 5 = 375 passages, graded by hand (real grades, provisional).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AWS_C, CHUNKERS, METRICS, NARRATION, OK_C, QUERY_C, aws, dim, mono, sans, serif,
                    source_tag)

SAY = NARRATION["S03"]
GRADE_C = {0: S.GREY_DARK, 1: S.GOLD, 2: OK_C}
# The document: (heading, length) blocks, the same in all three columns
SECTIONS = [("# JACC", 0.5), ("## Eligibility", 1.1), ("## Services", 1.6), ("## Cost", 0.35), ("## How to apply", 0.75)]


def document(width: float, color: str) -> VGroup:
    blocks = VGroup()
    for i, (h, ln) in enumerate(SECTIONS):
        r = Rectangle(width=width, height=ln, stroke_width=0).set_fill(color, 0.10 + 0.08 * (i % 2))
        lab = mono(h, 16, S.GREY).move_to(r).align_to(r, UP + LEFT).shift(DOWN * 0.06 + RIGHT * 0.08)
        blocks.add(VGroup(r, lab))
    blocks.arrange(DOWN, buff=0)
    frame = SurroundingRectangle(blocks, buff=0, stroke_color=S.GREY_DARK, stroke_width=2)
    g = VGroup(blocks, frame)
    g.blocks = blocks
    return g


def cut(doc, y: float, color: str) -> Line:
    return Line(doc.get_left() + RIGHT * -0.1, doc.get_right() + RIGHT * 0.1, stroke_color=color,
                stroke_width=4).set_y(y)


class Chunkers(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- one document, three cuts
        with self.voiceover(SAY[0]) as vo:
            cols = VGroup()
            for key, letter, name, col in CHUNKERS:
                head = VGroup(mono(letter, 40, col), serif(name, 28, col)).arrange(RIGHT, buff=0.2)
                doc = document(2.4, col)
                cols.add(VGroup(head, doc).arrange(DOWN, buff=0.25))
            cols.arrange(RIGHT, buff=1.7).move_to(UP * 0.35)
            hdr = VGroup(sans("THE SAME DOCUMENT, CUT THREE WAYS", 22, QUERY_C), source_tag("code")).arrange(RIGHT, buff=0.3)
            hdr.to_edge(UP, buff=0.35)
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(c[1]) for c in cols], lag_ratio=0.15), run_time=1.0)
            vo.wait_until("Marco compared three chunkers")
            self.play(LaggedStart(*[FadeIn(c[0], shift=DOWN * 0.1) for c in cols], lag_ratio=0.2), run_time=0.9)

            # A: fixed-size pieces, cut wherever the size says (a cut can fall inside a section; short ones merge)
            vo.wait_until("A is the original one")
            dA = cols[0][1]
            top, bot = dA.get_top()[1], dA.get_bottom()[1]
            cutsA = VGroup(*[cut(dA, top - f * (top - bot), CHUNKERS[0][3]) for f in (0.36, 0.72)])
            notesA = VGroup(serif("pieces of ~1,600 characters", 20), serif("(max 2,800)", 20, S.GREY),
                            serif("short sections can be merged", 20, S.GREY)).arrange(DOWN, buff=0.05)
            notesA.next_to(dA, DOWN, buff=0.2)
            self.play(LaggedStart(*[Create(c) for c in cutsA], lag_ratio=0.3), FadeIn(notesA), run_time=1.0)

            # B: a cut at every heading; the table's header row travels with each piece
            vo.wait_until("B never merges")
            dB = cols[1][1]
            cutsB = VGroup(*[cut(dB, b.get_bottom()[1], CHUNKERS[1][3]) for b in dB.blocks[:-1]])
            notesB = VGroup(serif("one heading per piece", 20), serif("tables repeat the row", 20, S.GREY),
                            serif("that names the programs", 20, S.GREY)).arrange(DOWN, buff=0.05)
            notesB.next_to(dB, DOWN, buff=0.2)
            self.play(LaggedStart(*[Create(c) for c in cutsB], lag_ratio=0.15), FadeIn(notesB), run_time=1.0)

            # C: small children (searched) inside larger parents (context)
            vo.wait_until("C makes small passages")
            dC = cols[2][1]
            kids = VGroup()
            for b in dC.blocks:
                r = b[0]
                n = max(1, round(r.height / 0.38))
                for k in range(n):
                    h = r.height / n
                    kids.add(Rectangle(width=r.width * 0.42, height=h * 0.8, stroke_color=CHUNKERS[2][3], stroke_width=2)
                             .set_fill(CHUNKERS[2][3], 0.35)
                             .move_to([r.get_right()[0] - r.width * 0.25, r.get_top()[1] - h * (k + 0.5), 0]))
            parents = VGroup(*[SurroundingRectangle(b[0], buff=0.0, stroke_color=S.WHITE, stroke_width=2.5) for b in dC.blocks])
            notesC = VGroup(serif("children ~950 characters: searched", 20),
                            serif("parent ≤ 2,400 characters:", 20, S.GREY), serif("added for context", 20, S.GREY)
                            ).arrange(DOWN, buff=0.05)
            notesC.next_to(dC, DOWN, buff=0.2)
            self.play(LaggedStart(*[FadeIn(k, scale=0.7) for k in kids], lag_ratio=0.05), run_time=1.0)
            self.play(Create(parents), FadeIn(notesC), run_time=0.9)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- three test libraries
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            ids = {"legacy": "3C45······", "section": "FJBD······", "hierarchical": "UYC7······"}
            kbs = VGroup()
            for key, letter, name, col in CHUNKERS:
                kb = aws("staging knowledge base", ids[key], f"{letter} · {name}", width=3.6, name_size=26, sub_size=22)
                kb.frame.set_stroke(col, 3)
                kbs.add(kb)
            kbs.arrange(RIGHT, buff=0.45).move_to(UP * 1.2)
            main = dim(aws("bedrock knowledge base", "ac215-program-kb", "the main library: untouched", width=4.6,
                           name_size=24, sub_size=22), 0.55).move_to(DOWN * 1.3 + LEFT * 3.4)
            self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.15) for k in kbs], lag_ratio=0.25), run_time=1.5)
            vo.wait_until("left the main one untouched")
            self.play(FadeIn(main), run_time=0.7)
            vo.wait_until("Library C is the one")
            e0 = VGroup(sans("E0, TERMINAL 1", 18, S.GREY),
                        mono('$env:CAREONEX_KB_ID = "UYC7······"', 24, QUERY_C)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            e0.move_to(DOWN * 1.3 + RIGHT * 3.0)
            arr = Arrow(e0.get_top(), kbs[2].get_bottom(), buff=0.12, color=QUERY_C, stroke_width=4)
            self.play(FadeIn(e0, shift=UP * 0.15), run_time=0.7)
            self.play(GrowArrow(arr), Indicate(kbs[2].frame, color=QUERY_C), run_time=0.9)
            note = VGroup(source_tag("code"), serif("IDs shortened here on purpose", 20, S.GREY)
                          ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(note), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- 375 hand grades
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            grades = METRICS["chunking"]["grades"]
            qids = list(grades)
            cell, gap = 0.17, 0.03
            blocks = VGroup()
            for key, letter, name, col in CHUNKERS:
                grid = VGroup()
                for qi, q in enumerate(qids):
                    for r, g in enumerate(grades[q][key]):
                        sq = Square(cell, stroke_width=0).set_fill(GRADE_C[g] if g is not None else S.BG, 1)
                        sq.move_to([r * (cell + gap), -qi * (cell + gap), 0])
                        grid.add(sq)
                lab = VGroup(mono(letter, 28, col), serif(name, 22, col)).arrange(RIGHT, buff=0.12)
                blocks.add(VGroup(lab, grid).arrange(DOWN, buff=0.15))
            blocks.arrange(RIGHT, buff=0.9).move_to(DOWN * 0.15 + LEFT * 2.0)
            sums = VGroup(mono("25 questions", 30), mono("× 3 libraries", 30), mono("× top 5", 30),
                          mono("= 375 passages", 32, QUERY_C)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            sums.next_to(blocks, RIGHT, buff=0.9).shift(UP * 0.9)
            legend = VGroup(*[VGroup(Square(0.22, stroke_width=0).set_fill(GRADE_C[k], 1), serif(t, 22, S.GREY)).arrange(RIGHT, buff=0.12)
                              for k, t in [(0, "0 no help"), (1, "1 partly"), (2, "2 answers it")]]
                            ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(sums, DOWN, buff=0.45).align_to(sums, LEFT)
            rowlab = serif("one row = one question", 22, S.GREY).rotate(PI / 2).next_to(blocks, LEFT, buff=0.3)
            self.play(LaggedStart(*[FadeIn(b[0]) for b in blocks], lag_ratio=0.2), FadeIn(rowlab), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(sq) for b in blocks for sq in b[1]], lag_ratio=0.004), run_time=2.2)
            self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.15) for s in sums], lag_ratio=0.3), FadeIn(legend), run_time=1.4)
            vo.wait_until("The team's notes call")
            prov = VGroup(source_tag("notes"), mono('"manually/provisionally', 22, S.GOLD), mono(' graded"', 22, S.GOLD)
                          ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            prov.next_to(legend, DOWN, buff=0.45).align_to(sums, LEFT)
            self.play(FadeIn(prov), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
