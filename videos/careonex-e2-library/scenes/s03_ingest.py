"""S03 · data and ingest → raw/.

1. data ensures the bucket: a dashed GREEN bucket `ac215-program-kb-<account-id>` with chips
   versioned · encrypted · public access blocked · public documents only.
2. Two name spaces: `ac215-*` (course, GREEN) and `careonex-*` (production, RED). The team's
   permission set holds `arn:aws:s3:::ac215-*`; its arrow to careonex-* is blocked.
3. ingest per row: download → sha256 → compare with the hash stored on the S3 object. One document
   unchanged (skip), one changed (upload a new version into raw/).
4. raw/nj_doas/nj_doas_jacc.html and its sidecar .metadata.json (real fields, from
   careonex_data.catalog.metadata_attributes).
5. snapshots/<date>-85f84fda/manifest.json (85f84fda = first 8 hex of the source list's sha256).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BAD_C, CODE_C, DATA_C, NARRATION, OK_C, PERSON_C, QUERY_C, chip, container,
                    doc_glyph, link, mark_bad, mark_ok, mono, sans, serif, source_tag, store, text_panel, what_is)

SAY = NARRATION["S03"]


class Ingest(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the bucket
        with self.voiceover(SAY[0]) as vo:
            s3card = what_is("S3", ["Amazon's file storage", "bucket = one top-level folder", "object = one file inside it"],
                             width=5.4, size=26).move_to(LEFT * 3.3 + UP * 0.3)
            folder = VGroup(sans("A BUCKET", 22, DATA_C),
                            VGroup(*[VGroup(doc_glyph(DATA_C, 0.42, 0.56), mono(n, 20)).arrange(DOWN, buff=0.08)
                                     for n in ("a.pdf", "b.html", "c.md")]).arrange(RIGHT, buff=0.4))
            folder.arrange(DOWN, buff=0.25)
            fbox = SurroundingRectangle(folder[1], buff=0.3, corner_radius=0.15, color=DATA_C)
            folder = VGroup(folder, fbox).move_to(RIGHT * 3.2 + UP * 0.3)
            olab = serif("each file = an object", 22, S.GREY).next_to(fbox, DOWN, buff=0.2)
            self.play(FadeIn(s3card, shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(folder), FadeIn(olab), run_time=0.8)
            vo.wait_until("The first container")
            self.play(FadeOut(VGroup(s3card, folder, olab)), run_time=0.6)
            data = container("data", "ensure-buckets", width=2.8, name_size=32, sub_size=22).move_to(LEFT * 4.6 + UP * 0.6)
            bucket = RoundedRectangle(width=6.6, height=3.4, corner_radius=0.25, stroke_color=DATA_C, stroke_width=3)
            bucket = DashedVMobject(bucket, num_dashes=70).move_to(RIGHT * 2.3 + UP * 0.6)
            bname = mono("ac215-program-kb-<account-id>", 26, DATA_C).next_to(bucket, UP, buff=0.15)
            btag = sans("S3 BUCKET", 22, DATA_C).next_to(bname, UP, buff=0.08)
            arrow = link(data, bucket, S.GREY, label="create if missing", label_size=22)
            self.play(FadeIn(data, shift=RIGHT * 0.2), run_time=0.7)
            self.play(GrowArrow(arrow.arrow), FadeIn(arrow.label), Create(bucket), FadeIn(bname), FadeIn(btag),
                      run_time=1.4)
            chips = VGroup(chip("keeps old versions", DATA_C, 24), chip("encrypted", DATA_C, 24),
                           chip("public access blocked", DATA_C, 24)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            chips.move_to(bucket).shift(UP * 0.45)
            vo.wait_until("It keeps old versions")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.35), run_time=1.6)
            vo.wait_until("public documents only")
            docs = VGroup(*[doc_glyph(DATA_C, 0.36, 0.48, lines=3) for _ in range(6)]).arrange(RIGHT, buff=0.12)
            docs.next_to(chips, DOWN, buff=0.35)
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.15) for d in docs], lag_ratio=0.15), run_time=1.0)
            vo.wait_until("No caller information")
            caller = VGroup(chip("caller name, phone, intake", BAD_C, 22, mono_font=False))
            caller.next_to(bucket, DOWN, buff=0.45)
            self.play(FadeIn(caller, shift=UP * 0.2), run_time=0.5)
            self.play(caller.animate.shift(UP * 0.25), run_time=0.4)
            x = mark_bad(0.4).move_to(caller)
            self.play(Create(x), caller.animate.set_opacity(0.4), run_time=0.5)
            ntag = source_tag("notes", "services/data/README.md").to_corner(DL, buff=0.35)
            self.play(FadeIn(ntag), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- ac215-* vs careonex-*
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(data, arrow, bucket, bname, btag, chips, docs, caller, x, ntag)), run_time=0.7)
            course = VGroup(sans("COURSE", 22, DATA_C), mono("ac215-*", 34, DATA_C),
                            mono("ac215-program-kb-…", 22, S.WHITE), mono("ac215-program-vectors-…", 22, S.WHITE),
                            mono("ac215-program-kb (KB)", 22, S.WHITE)).arrange(DOWN, buff=0.15)
            prod = VGroup(sans("PRODUCTION", 22, BAD_C), mono("careonex-*", 34, BAD_C),
                          serif("the company's own buckets", 24, S.WHITE)).arrange(DOWN, buff=0.15)
            cbox = SurroundingRectangle(course, buff=0.3, corner_radius=0.2, color=DATA_C)
            pbox = SurroundingRectangle(prod, buff=0.3, corner_radius=0.2, color=BAD_C)
            VGroup(VGroup(cbox, course), VGroup(pbox, prod)).arrange(RIGHT, buff=4.2).shift(DOWN * 0.6)
            VGroup(cbox, course).move_to(LEFT * 3.6 + DOWN * 0.9)
            VGroup(pbox, prod).move_to(RIGHT * 3.6 + DOWN * 0.9)
            role = VGroup(sans("TEAM PERMISSION SET · S3 PART", 22, PERSON_C), mono("AC215", 32, PERSON_C)).arrange(DOWN, buff=0.08)
            role.move_to(UP * 2.4)
            policy = text_panel(['"Resource": ["arn:aws:s3:::ac215-*", "arn:aws:s3:::ac215-*/*"]'], size=22,
                                border=S.GREY_DARK)
            policy.next_to(role, DOWN, buff=0.25)
            self.play(FadeIn(role, shift=DOWN * 0.2), FadeIn(policy), run_time=0.9)
            self.play(FadeIn(VGroup(cbox, course)), FadeIn(VGroup(pbox, prod)), run_time=0.9)
            vo.wait_until("The team's S3 permissions")
            ok = link(policy, cbox, OK_C, stroke=4)
            self.play(Indicate(policy.rows[0], color=QUERY_C), GrowArrow(ok.arrow), run_time=1.2)
            vo.wait_until("so nothing")
            blocked = link(policy, pbox, BAD_C, stroke=4)
            wall = mark_bad(0.55).move_to(blocked.arrow.point_from_proportion(0.5))
            self.play(GrowArrow(blocked.arrow), run_time=0.6)
            self.play(Create(wall), Wiggle(VGroup(pbox, prod), scale_value=1.03), run_time=0.9)
            ptag = source_tag("notes", "TEAM_SETUP.md, the AC215 policy").to_corner(DL, buff=0.35)
            self.play(FadeIn(ptag), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- ingest: hash, compare, skip or upload
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(role, policy, cbox, course, pbox, prod, ok, blocked, wall, ptag)), run_time=0.7)
            ing = container("ingest", "same image as data", width=3.0, name_size=32, sub_size=22).to_edge(UP, buff=0.5)
            self.play(FadeIn(ing, shift=DOWN * 0.2), run_time=0.6)
            heads = VGroup(serif("download", 26, S.GREY), serif("sha256 of the bytes", 26, S.GREY),
                           serif("hash stored in S3", 26, S.GREY), serif("result", 26, S.GREY))
            xs = [-4.45, -1.4, 1.6, 4.85]
            for h, x in zip(heads, xs):
                h.move_to([x, 1.25, 0])
            self.play(LaggedStart(*[FadeIn(h) for h in heads], lag_ratio=0.2), run_time=1.0)
            cases = [("nj_doas_pace_flyer_en.pdf", "eec27455…", "eec27455…", True),
                     ("nj_doas_jacc.html", "c5befe69…", "none yet", False)]
            for k, (fname, new, old, same) in enumerate(cases):
                y = 0.2 - k * 1.5
                f = VGroup(doc_glyph(DATA_C, 0.42, 0.56), mono(fname, 20, S.WHITE)).arrange(DOWN, buff=0.1).move_to([xs[0], y, 0])
                h = mono(new, 26, QUERY_C).move_to([xs[1], y, 0])
                o = mono(old, 26, S.WHITE).move_to([xs[2], y, 0])
                eq = mono("=" if same else "≠", 34, OK_C if same else BAD_C).move_to([(xs[1] + xs[2]) / 2, y, 0])
                res = (chip("unchanged · skip", S.GREY, 24, mono_font=False) if same
                       else chip("first run · upload", DATA_C, 24, mono_font=False)).move_to([xs[3], y, 0])
                self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.6)
                self.play(TransformFromCopy(f[0], h), run_time=0.7)
                self.play(FadeIn(o), run_time=0.5)
                self.play(FadeIn(eq, scale=1.4), run_time=0.4)
                self.play(FadeIn(res, shift=LEFT * 0.2), run_time=0.5)
                if k == 0:
                    vo.wait_until("Otherwise")
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- raw/ + sidecar
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            key = VGroup(store("raw/nj_doas/nj_doas_jacc.html", "the page, byte for byte", tag="S3 object",
                               width=6.0, name_size=21, sub_size=22),
                         store("raw/nj_doas/nj_doas_jacc.html.metadata.json", "its sidecar", tag="S3 object",
                               width=6.0, name_size=21, sub_size=22)).arrange(DOWN, buff=0.3)
            key.move_to(LEFT * 3.5 + UP * 0.2)
            self.play(FadeIn(key[0], shift=DOWN * 0.2), run_time=0.7)
            self.play(FadeIn(key[1], shift=DOWN * 0.2), run_time=0.7)
            sidecar = text_panel([
                '{"metadataAttributes": {',
                '  "source_id": "nj_doas",',
                '  "program": "JACC",',
                '  "year": 2026,',
                '  "jurisdiction": "NJ",',
                '  "effective_date": "2026-09-28",',
                '  "county": "all",',
                '  "source_url": "https://www.nj.gov/…",',
                '  "sha256": "c5befe69…",  …',
                '}}'], size=20, border=DATA_C)
            sidecar.move_to(RIGHT * 3.25 + UP * 0.2)
            self.play(TransformFromCopy(key[1].frame, sidecar.bg), FadeIn(sidecar.rows, lag_ratio=0.1), run_time=1.4)
            vo.wait_until("Later, search can filter")
            for k in (2, 3):
                self.play(sidecar.rows[k].animate.set_color(QUERY_C), run_time=0.4)
            filt = chip('later: filter program = "JACC"', QUERY_C, 24).next_to(key, DOWN, buff=0.45)
            self.play(FadeIn(filt, shift=DOWN * 0.15), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 5 ---------------------------------------------------------------- the manifest
        with self.voiceover(SAY[4]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            path = mono("snapshots/<run date>-85f84fda/manifest.json", 28, DATA_C).move_to(UP * 2.6)
            sub = serif("85f84fda = start of the source list's hash", 22, S.GREY).next_to(path, DOWN, buff=0.12)
            man = text_panel([
                '{"snapshot_id": "<run date>-85f84fda",',
                ' "items": [',
                '  {"key": "raw/nj_doas/nj_doas_jacc.html",',
                '   "status": "uploaded", "version_id": "…"},',
                '  {"key": "raw/nj_doas/nj_doas_pace_flyer_en.pdf",',
                '   "status": "unchanged"},',
                '  … 20 items',
                ' ]}'], size=22, border=DATA_C).next_to(sub, DOWN, buff=0.3)
            self.play(FadeIn(path), FadeIn(sub), run_time=0.7)
            self.play(FadeIn(man, shift=UP * 0.2), run_time=0.9)
            vo.wait_until("That manifest")
            ver = chip("= the version of the whole dataset", DATA_C, 26, mono_font=False).next_to(man, RIGHT, buff=0.3)
            if ver.get_right()[0] > 6.5:
                ver.next_to(man, DOWN, buff=0.25)
            self.play(FadeIn(ver, shift=LEFT * 0.2), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
