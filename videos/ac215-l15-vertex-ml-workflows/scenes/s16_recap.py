"""S16 · Tear down, recap, test yourself — no tracker; lecture tags slide 41 (beats 0–2, with the
DELETE card and the clean-up card) and slide 40 (beat 3, with the recipe-to-factory chain only).
Ends part 2 on an empty frame.

Beats (script.md "## S16"; one voiceover block each):
0. LECTURE 15 · 41. The GOLD "DELETE" word card returns small (top left). The GOLD clean-up card
   (cost tag "billed until deleted") builds line by line: item 1 "aws sagemaker list-endpoints →
   delete every endpoint: Part A's timestamped ones, cheese-app-endpoint, cheese-app-endpoint-…;
   then their endpoint configurations and models" writes in clause by clause and ticks.
1. LECTURE (held). Items 2 (empty and delete both buckets), 3 (the two ECR repositories) and 4 (the
   sagemaker-deploy-model-lambda-… functions and cheese-pipeline) write in and tick as spoken.
2. Items 5 (access keys; users and roles) and 6 (the two domains, any sagemaker-<region>-<account>
   bucket) tick; a silent GREY item 7 "optional · your laptop: docker image rm the ~4 GB
   model-deployment-cli-aws and the cheese-app-* images · persistent-folder". The card and the
   DELETE card collapse into a GOLD corner icon (top left); the lecture tag fades with them.
3. LECTURE 15 · 40. Slide 40's chain writes along the top in one move (recipe → … → factory, "your
   Python = the recipe", "SageMaker Pipelines runs it"), then fades with the tag. Five text-free
   thumbnails of today's set pieces appear in a row, each tile lighting YELLOW as it is named: V1
   (key on the laptop, hard hat in the cloud), V2 (star ≠ pin), V3 (the two pipes), V5 (three
   pieces + meter), V8 (steps joined by PINK reference edges).
4. Under the thumbnails, Part A's mini-chain: --prepare (slide 12 · steps 1 and 3) → --deploy
   (steps 4–5) → --predict → --delete, each with a small V4/V5 icon, lighting as named.
5. Clear (the corner icon goes too). YELLOW heading "Test yourself · 1/5" and question card 1.
6. Card 1 Transforms into card 2, card 2 into card 3, on the sentence starts.
7. Card 3 → 4 → 5 on the sentence starts; card 5 fades; a GREY pointer card "answers:
   exercises.md · study guide" and a GREY-dashed "L23 · trigger the pipeline from GitHub Actions".
   Fade to empty.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S16"]

CARD_LEFT = -6.45
CARD_TOP = 2.88            # the clean-up card's top edge (the DELETE card sits above it, top left)

# one row per spoken clause (so a highlight marks exactly the clause being said); code in mono
QUESTIONS = (
    (("Your laptop and the SageMaker endpoint both reach S3.",),
     ("Which identity does each use?",),
     ("And why do Option 2's exported keys",),
     ("never reach the Part A container?",)),
    (("Name the three things", ("--deploy", "m"), "creates."),
     ("Which is the address,",),
     ("and which bills while nobody calls it?",)),
    (("Where does preprocessing sit in Part A,",),
     ("and where in the Part B trainer?",),
     ("Give the lecture's two reasons to put it in the model.",)),
    (("Which lines make", ("ModelTraining", "m"), "wait for", ("DataProcessor", "m"), "?"),
     ("What would a literal", ("s3://…/tfrecords", "m"), "string change?")),
    (("Which two one-line fixes did today's tutorial need,",),
     ("and which one would an Apple-silicon Mac not need?",)),
)
Q_W = 12.4                 # every question card has this width, so card k → k+1 morphs only in height


def parts_row(*parts, size: float = 20, base=INK) -> VGroup:
    """A row of pieces: str → label in `base`; (s, 'm') → mono in `base`; (s, colour) → label in colour."""
    ms = []
    for p in parts:
        if isinstance(p, str):
            ms.append(label(p, size, base))
        elif p[1] == "m":
            ms.append(mono(p[0], size, base))
        else:
            ms.append(label(p[0], size, p[1]))
    g = VGroup(*ms)
    for a, b in zip(ms, ms[1:]):
        punct = b.original_text[:1] in ",:;?."
        b.next_to(a, RIGHT, buff=0.04 if punct else 0.12)
        if punct:
            b.align_to(a, DOWN)
        else:
            b.set_y(ms[0].get_y())     # a word after a punctuation mark returns to the row's centre line
    return g


def clean_card() -> VGroup:
    """BRIEF "Teardown checklist (S16)" as a GOLD card. .rows .items (7 groups) .tick_rows .frame .head"""
    n = lambda k: (k, COST)  # noqa: E731
    g7 = S.GREY
    rows = [
        parts_row(n("1"), ("aws sagemaker list-endpoints", "m"), "→ delete every endpoint:"),
        parts_row("Part A's timestamped ones,", ("cheese-app-endpoint", "m"), ",", ("cheese-app-endpoint-…", "m"),
                  ";"),
        parts_row("then their endpoint configurations and models"),
        parts_row(n("2"), "empty and delete both buckets"),
        parts_row(n("3"), "delete the two ECR repositories"),
        parts_row(n("4"), "delete the", ("sagemaker-deploy-model-lambda-…", "m"), "functions"),
        parts_row("and", ("cheese-pipeline", "m")),
        parts_row(n("5"), "deactivate and delete the access keys;"),
        parts_row("delete users and roles you no longer need"),
        parts_row(n("6"), "check the SageMaker AI domain and the Unified Studio domain,"),
        parts_row("and any", ("sagemaker-<region>-<account>", "m"), "bucket the SDK may have made"),
        parts_row(("7", g7), "optional · your laptop:", ("docker image rm", "m"), "the 4 GB", base=g7),
        parts_row(("model-deployment-cli-aws", "m"), "and the", ("cheese-app-*", "m"), "images ·",
                  ("persistent-folder", "m"), base=g7),
    ]
    c = card(rows, COST, size=20, buff=0.11, head="Clean up · before you leave")
    for k in (1, 2, 6, 8, 10, 12):
        rows[k].shift(RIGHT * 0.27)
    fr = c.frame
    wide = outline_box(fr.width + 0.5, fr.height, COST, solid=True, fill_opacity=0.08)
    wide.fill.set_fill(S.GREY_DARKER, 1)
    wide.move_to(fr).align_to(fr, LEFT)
    c.remove(fr)
    c.submobjects.insert(0, wide)
    c.frame = wide
    c.rows = rows
    c.items = [VGroup(*rows[0:3]), VGroup(rows[3]), VGroup(rows[4]), VGroup(*rows[5:7]),
               VGroup(*rows[7:9]), VGroup(*rows[9:11]), VGroup(*rows[11:13])]
    c.tick_rows = [rows[i] for i in (0, 3, 4, 5, 7, 9)]
    return c


def qcard(rows_spec, size: float = 28) -> VGroup:
    """A YELLOW question card like common.question_card, but with mono code spans. .frame .body"""
    rows = VGroup(*[parts_row(*r, size=size) for r in rows_spec]).arrange(DOWN, buff=0.2)
    frame = RoundedRectangle(width=Q_W, height=rows.height + 0.7, corner_radius=0.16, stroke_color=TURN,
                             stroke_width=3).set_fill(S.BG, 1)
    rows.move_to(frame)
    g = VGroup(frame, rows)
    g.frame, g.body = frame, rows
    return g


def corner_icon() -> VGroup:
    """A text-free GOLD clean-up icon: a small card with three lines and a tick."""
    fr = RoundedRectangle(width=0.62, height=0.78, corner_radius=0.08, stroke_color=COST,
                          stroke_width=3).set_fill(COST, 0.12)
    ls = VGroup(*[Line(LEFT * 0.18, RIGHT * 0.18, color=COST, stroke_width=3) for _ in range(3)])
    ls.arrange(DOWN, buff=0.14).move_to(fr).shift(LEFT * 0.06)
    tk = check_glyph(0.26, OWN).move_to(fr.get_corner(UR) + np.array([0.02, -0.02, 0]))
    return VGroup(fr, ls, tk)


def hard_hat(color=ROLE) -> VGroup:
    dome = Arc(radius=0.17, start_angle=0, angle=PI, color=color, stroke_width=3).set_fill(color, 0.6)
    brim = Line(LEFT * 0.25, RIGHT * 0.25, color=color, stroke_width=4).next_to(dome, DOWN, buff=0.0)
    return VGroup(dome, brim)


def pushpin(color=PIN) -> VGroup:
    head = Circle(radius=0.17, stroke_color=color, stroke_width=3).set_fill(color, 0.6)
    needle = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.38, color=color, stroke_width=4)
    return VGroup(head, needle)


def thumbs() -> list:
    """Five text-free thumbnails: V1, V2, V3, V5, V8 (each about 1.9 × 1.0)."""
    # V1 · a key on the laptop, a role badge (hard hat) in the cloud
    lp = laptop_glyph(1.0, LAPTOP)
    kg = key_glyph(0.5, KEY).move_to(lp.screen)
    hb = RoundedRectangle(width=0.75, height=0.6, corner_radius=0.1, stroke_color=CLOUD,
                          stroke_width=3).set_fill(CLOUD, 0.15)
    hh = hard_hat().move_to(hb)
    v1 = VGroup(VGroup(lp, kg), VGroup(hb, hh)).arrange(RIGHT, buff=0.3)
    # V2 · a star is not a pin
    st = Star(n=5, outer_radius=0.3, inner_radius=0.13, stroke_color=SHARED, stroke_width=3).set_fill(SHARED, 0.5)
    ne = label("≠", 30, INK)
    v2 = VGroup(st, ne, pushpin()).arrange(RIGHT, buff=0.3)
    # V3 · two pipes: preprocessing in the client, or inside the model
    r1 = RoundedRectangle(width=0.55, height=0.36, corner_radius=0.06, stroke_color=CLOUD, stroke_width=3)
    p1 = VGroup(gear(0.14), Arrow(LEFT * 0.25, RIGHT * 0.25, buff=0, color=S.GREY, stroke_width=3,
                                  tip_length=0.12), r1).arrange(RIGHT, buff=0.1)
    r2 = RoundedRectangle(width=0.55, height=0.36, corner_radius=0.06, stroke_color=CLOUD, stroke_width=3)
    g2 = gear(0.12).move_to(r2)
    p2 = VGroup(Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=S.GREY, stroke_width=3, tip_length=0.12),
                VGroup(r2, g2)).arrange(RIGHT, buff=0.1)
    p2.align_to(p1, RIGHT)
    v3 = VGroup(p1, p2).arrange(DOWN, buff=0.18, aligned_edge=RIGHT)
    # V5 · three pieces behind an endpoint (model → configuration → endpoint, the meter under it)
    bx = [RoundedRectangle(width=0.42, height=0.5, corner_radius=0.06, stroke_color=CLOUD, stroke_width=3)
          .set_fill(CLOUD, 0.12) for _ in range(3)]
    trio = VGroup(*bx).arrange(RIGHT, buff=0.2)
    rk = rack(0.38).move_to(bx[2])
    trio_arrows = VGroup(*[Line(bx[i].get_right(), bx[i + 1].get_left(), color=S.GREY, stroke_width=3)
                           for i in range(2)])
    mt = meter_icon(0.7).next_to(trio, DOWN, buff=0.15).align_to(bx[2], RIGHT)
    v5 = VGroup(trio, trio_arrows, rk, mt)
    # V8 · step boxes joined by PINK reference edges
    sb = [RoundedRectangle(width=0.42, height=0.32, corner_radius=0.06, stroke_color=INK, stroke_width=2.5)
          for _ in range(3)]
    VGroup(*sb).arrange(RIGHT, buff=0.3)
    sb[1].shift(DOWN * 0.25)
    sb[2].shift(DOWN * 0.5)
    ed = VGroup(*[Arrow(sb[i].get_right(), sb[i + 1].get_left(), buff=0.03, color=EDGE, stroke_width=3,
                        tip_length=0.12) for i in range(2)])
    v8 = VGroup(*sb, ed)
    return [v1, v2, v3, v5, v8]


def tiles(contents, tile_w: float = 2.3, tile_h: float = 1.45, gap: float = 0.25) -> VGroup:
    """Each content centred in a GREY rounded tile; tiles in a row. .frames .contents"""
    frames = []
    for c in contents:
        fr = RoundedRectangle(width=tile_w, height=tile_h, corner_radius=0.14, stroke_color=S.GREY,
                              stroke_width=2.5)     # no fill: an animated frame is drawn on top
        c.move_to(fr)
        frames.append(fr)
    gs = [VGroup(f, c) for f, c in zip(frames, contents)]
    row = VGroup(*gs).arrange(RIGHT, buff=gap)
    row.frames, row.contents = frames, list(contents)
    return row


def mini_icon(kind: str) -> VGroup:
    """Text-free icons for Part A's four commands (V4 tarball, V5 trio, request bars, stopped meter)."""
    if kind == "prepare":
        return VGroup(file_icon(None, OWN, h=0.42))
    if kind == "deploy":
        bx = [RoundedRectangle(width=0.3, height=0.36, corner_radius=0.05, stroke_color=CLOUD, stroke_width=3)
              .set_fill(CLOUD, 0.12) for _ in range(3)]
        return VGroup(*bx).arrange(RIGHT, buff=0.1)
    if kind == "predict":
        return bars((0.15, 0.2, 0.85, 0.15), bar_w=0.12, max_h=0.42, hi=2)
    m = meter_icon(0.6)
    m.fill_bar.stretch(0.02, 0, about_edge=LEFT)
    return VGroup(m)


class TeardownRecap(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S16"] == 8, len(SAY)
        # ~4 GB: laptop/26 and laptop/49 (docker images: model-deployment-cli-aws 4.01GB)
        assert "4.01GB" in capture("26").at(3)[0] and "model-deployment-cli-aws" in capture("26").at(3)[0]

        # ========================================================== 0. DELETE returns; item 1
        r41 = lref("41")
        word = label("DELETE", 30, COST)
        word_fr = outline_box(word.width + 0.45, word.height + 0.26, COST, solid=True, fill_opacity=0.12)
        word.move_to(word_fr)
        dele = VGroup(word_fr, word)
        dele.move_to([CARD_LEFT + dele.width / 2, 3.55 - dele.height / 2, 0])
        cc = clean_card()
        cc.move_to([CARD_LEFT + cc.width / 2, CARD_TOP - cc.height / 2, 0])
        assert cc.get_bottom()[1] > -3.55 and cc.get_right()[0] < 6.55, (cc.get_bottom(), cc.get_right())
        assert dele.get_bottom()[1] > CARD_TOP + 0.03, dele.get_bottom()
        ctag = cost_tag("billed until deleted")
        # on the card's top edge, left of the lecture tag (which sits top right, just above the edge)
        ctag.move_to([r41.get_left()[0] - 0.3 - ctag.width / 2, cc.frame.get_top()[1], 0])
        assert ctag.get_top()[1] < r41.get_bottom()[1] - 0.05 or ctag.get_right()[0] < r41.get_left()[0] - 0.1
        assert ctag.get_left()[0] > cc.head.get_right()[0] + 0.3, (ctag.get_left(), cc.head.get_right())
        tick_x = cc.frame.get_right()[0] - 0.35
        ticks = [check_glyph(0.28).move_to([tick_x, r.get_center()[1], 0]) for r in cc.tick_rows]
        for r in cc.tick_rows:
            assert r.get_right()[0] < tick_x - 0.25, (r.get_right(), tick_x)

        def write(item, run_time=0.5):
            return LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in item], lag_ratio=0.35, run_time=run_time)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(r41), FadeIn(dele, scale=1.4), run_time=0.6)
            self.play(Indicate(word, color=INK, scale_factor=1.1), run_time=0.5)
            self.play(FadeIn(VGroup(cc.frame, cc.head), shift=DOWN * 0.1), FadeIn(ctag), run_time=0.6)
            vo.wait_until("List your endpoints")
            self.play(FadeIn(cc.rows[0], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(cc.rows[0][1], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("the timestamped ones")
            self.play(FadeIn(cc.rows[1], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("Then delete their configurations")
            self.play(FadeIn(cc.rows[2], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Create(ticks[0]), run_time=0.4)

        # ========================================================== 1. buckets, ECR, Lambdas + pipeline
        with self.voiceover(SAY[1]) as vo:
            self.play(write(cc.items[1]), run_time=0.5)
            self.play(Create(ticks[1]), run_time=0.4)
            vo.wait_until("Delete the two ECR")
            self.play(write(cc.items[2]), run_time=0.5)
            self.play(Create(ticks[2]), run_time=0.4)
            vo.wait_until("the deploy Lambda functions")
            self.play(write(cc.items[3], run_time=0.8))
            self.play(Create(ticks[3]), run_time=0.4)

        # ========================================================== 2. keys, users, roles, domains; collapse
        icon = corner_icon().move_to([CARD_LEFT + 0.35, 3.15, 0])
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(cc.rows[7], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Create(ticks[4]), run_time=0.4)
            vo.wait_until("and the users and roles")
            self.play(FadeIn(cc.rows[8], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("Finally, check")
            self.play(write(cc.items[5], run_time=0.7))
            vo.wait_until("and the Unified Studio domain")
            self.play(Indicate(cc.rows[9], color=COST, scale_factor=1.03), run_time=0.6)
            self.play(Create(ticks[5]), run_time=0.4)
        self.play(write(cc.items[6], run_time=0.8))          # GREY item 7: silent, optional
        self.play(Indicate(ctag, color=COST, scale_factor=1.15), run_time=0.8)
        self.play(ReplacementTransform(VGroup(cc, ctag, *ticks, dele), icon), FadeOut(r41), run_time=1.0)

        # ========================================================== 3. slide 40's chain; five thumbnails
        r40 = lref("40")
        c_rec = chip("recipe", OWN, size=26).move_to([-3.4, 2.62, 0])
        c_fac = chip("factory", CLOUD, size=26).move_to([3.4, 2.62, 0])
        c_dots = label("…", 30, S.GREY).move_to([0, 2.62, 0])
        c_a1 = arrow(c_rec.get_right(), c_dots.get_left() + LEFT * 0.15, buff=0.15)
        c_a2 = arrow(c_dots.get_right() + RIGHT * 0.15, c_fac.get_left(), buff=0.15)
        chain_row = VGroup(c_rec, c_a1, c_dots, c_a2, c_fac)
        s_rec = label("your Python = the recipe", 22, INK).next_to(c_rec, DOWN, buff=0.2)
        s_fac = label("SageMaker Pipelines runs it", 22, INK).next_to(c_fac, DOWN, buff=0.2)
        assert s_rec.get_right()[0] < s_fac.get_left()[0] - 0.5, (s_rec.get_right(), s_fac.get_left())
        chain = VGroup(chain_row, s_rec, s_fac)
        assert chain.get_left()[0] > icon.get_right()[0] + 0.2 and chain.get_right()[0] < 6.5, chain.get_right()
        assert chain_row.get_top()[1] < r40.get_bottom()[1] - 0.05 or chain_row.get_right()[0] < r40.get_left()[0]
        th = tiles(thumbs())
        th.move_to([0, 0.9, 0])
        assert th.get_left()[0] > -6.55 and th.get_right()[0] < 6.55, th.width
        assert th.get_top()[1] < s_rec.get_bottom()[1] - 0.15, (th.get_top(), s_rec.get_bottom())

        def light(k, prev=None):
            anims = [th.frames[k].animate.set_stroke(TURN, 4),
                     th.contents[k].animate(rate_func=there_and_back).scale(1.15)]
            if prev is not None:
                anims.append(th.frames[prev].animate.set_stroke(S.GREY, 2.5))
            return AnimationGroup(*anims, run_time=0.7)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(r40), Write(chain_row), FadeIn(s_rec, shift=UP * 0.1), FadeIn(s_fac, shift=UP * 0.1),
                      run_time=1.2)
            vo.wait_until("your Python is the recipe")
            self.play(c_rec.animate(rate_func=there_and_back).scale(1.12), Indicate(s_rec, color=OWN, scale_factor=1.05),
                      run_time=0.7)
            vo.wait_until("and SageMaker Pipelines runs it")
            self.play(c_fac.animate(rate_func=there_and_back).scale(1.12), Indicate(s_fac, color=CLOUD, scale_factor=1.05),
                      run_time=0.7)
            vo.wait_until("Today's pictures")
            self.play(FadeOut(chain), FadeOut(r40), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.15) for g in th], lag_ratio=0.15), run_time=1.0)
            vo.wait_until("a key on the laptop")
            self.play(light(0))
            vo.wait_until("A star is not a pin")
            self.play(light(1, 0))
            vo.wait_until("Preprocessing sits")
            self.play(light(2, 1))
            vo.wait_until("Three pieces stand")
            self.play(light(3, 2))
            vo.wait_until("and references draw the edges")
            self.play(light(4, 3))

        # ========================================================== 4. Part A in four commands
        kinds = ("prepare", "deploy", "predict", "delete")
        notes = ("slide 12 · steps 1 and 3", "steps 4–5", None, None)
        xs = (-4.8, -1.6, 1.6, 4.8)
        nodes, chips_, icons_, notes_ = [], [], [], []
        for k, x in zip(kinds, xs):
            ch = chip(f"--{k}", S.GREY, size=22, font=MONO).move_to([x, -1.75, 0])
            ic = mini_icon(k).next_to(ch, UP, buff=0.22)
            parts = [ic, ch]
            chips_.append(ch)
            icons_.append(ic)
            nt = None
            if notes[len(nodes)]:
                nt = label(notes[len(nodes)], 20, S.GREY).next_to(ch, DOWN, buff=0.18)
                parts.append(nt)
            notes_.append(nt)
            nodes.append(VGroup(*parts))
        links = [arrow(chips_[i].get_right(), chips_[i + 1].get_left(), buff=0.15) for i in range(3)]
        for nd in nodes:
            assert nd.get_left()[0] > -6.55 and nd.get_right()[0] < 6.55 and nd.get_bottom()[1] > -3.5, nd.get_corner(DL)
            assert nd.get_top()[1] < th.get_bottom()[1] - 0.15, (nd.get_top(), th.get_bottom())
        assert links[0].get_length() > 0.3, links[0].get_length()
        with self.voiceover(SAY[4]) as vo:
            self.play(th.frames[4].animate.set_stroke(S.GREY, 2.5), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(VGroup(c, i), shift=UP * 0.15) for c, i in zip(chips_, icons_)],
                                  lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.3),
                      run_time=1.2)
            for i, anchor in enumerate(("Prepare packs the model", "deploy builds the model",
                                        "Predict sends the numbers", "and delete turns off the meter")):
                vo.wait_until(anchor)
                col = COST if i == 3 else TURN
                anims = [chips_[i].box.animate.set_stroke(col, 4),
                         icons_[i].animate(rate_func=there_and_back).scale(1.3)]
                if notes_[i] is not None:
                    anims.append(FadeIn(notes_[i], shift=UP * 0.1))
                if i == 1:
                    anims.append(th.contents[3].animate(rate_func=there_and_back).scale(1.12))
                if i == 3:
                    anims.append(icons_[3][0].fill_bar.animate.set_fill(S.GREY, 0.8))
                self.play(*anims, run_time=0.7)
                self.add(chips_[i])        # the box was animated alone: put the chip's text back on top

        # ========================================================== 5-7. test yourself
        head = label("Test yourself", 30, TURN)
        heads = [label(f"· {k + 1}/5", 30, TURN) for k in range(5)]
        head.move_to([-6.4, 2.6, 0], aligned_edge=LEFT)
        for h in heads:
            h.next_to(head, RIGHT, buff=0.2).align_to(head, DOWN)
        qcards = [qcard(q).move_to([0, 0.2, 0]) for q in QUESTIONS]
        for q in qcards:
            assert q.body.width < q.frame.width - 0.5 and q.get_left()[0] > -6.55, q.body.width
        # progress dots under the card: done = GREY, current = YELLOW, ahead = outline only
        dots = VGroup(*[Circle(radius=0.11, stroke_color=S.GREY, stroke_width=2.5) for _ in range(5)])
        dots.arrange(RIGHT, buff=0.35).move_to([0, -2.3, 0])
        assert dots.get_top()[1] < min(q.get_bottom()[1] for q in qcards) - 0.4
        dots[0].set_fill(TURN, 1).set_stroke(TURN)
        cur = qcards[0]
        cur_h = heads[0]

        def to_card(k):
            """The frame and the counter morph; the question text swaps (a morph would scramble it)."""
            nonlocal cur, cur_h
            nxt_c = qcards[k]
            anims = [ReplacementTransform(cur.frame, nxt_c.frame),
                     FadeOut(cur.body, shift=UP * 0.2), FadeIn(nxt_c.body, shift=UP * 0.2),
                     ReplacementTransform(cur_h, heads[k]),
                     dots[k - 1].animate.set_fill(S.GREY, 1).set_stroke(S.GREY),
                     dots[k].animate.set_fill(TURN, 1).set_stroke(TURN)]
            cur, cur_h = nxt_c, heads[k]
            return AnimationGroup(*anims, run_time=0.8)

        def mark(k, *rows):
            return Indicate(VGroup(*[qcards[k].body[r] for r in rows]), color=TURN, scale_factor=1.04,
                            run_time=0.8)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(Group(th, *nodes, *links, icon)), run_time=0.6)
            self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(heads[0], shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Your laptop and the endpoint")
            self.play(FadeIn(qcards[0], shift=UP * 0.15), FadeIn(dots, lag_ratio=0.15), run_time=0.7)
            vo.wait_until("which identity does each use")
            self.play(mark(0, 1))
            vo.wait_until("And why do the option 2 exports")
            self.play(mark(0, 2, 3))

        with self.voiceover(SAY[6]) as vo:
            vo.wait_until("Name the three things")
            self.play(to_card(1))
            vo.wait_until("Which one is the address")
            self.play(mark(1, 1))
            vo.wait_until("and which one bills")
            self.play(mark(1, 2))
            vo.wait_until("Where does preprocessing sit")
            self.play(to_card(2))
            vo.wait_until("and in the part 2 trainer")
            self.play(mark(2, 1))
            vo.wait_until("and why move it into the model")
            self.play(mark(2, 2))

        ans = card(["answers: exercises.md · study guide"], S.GREY, size=22)
        nxt = dashed_chip("L23 · trigger the pipeline from GitHub Actions", size=22)
        VGroup(ans, nxt).arrange(DOWN, buff=0.45).move_to([0, -0.1, 0])
        with self.voiceover(SAY[7]) as vo:
            vo.wait_until("Which lines make training")
            self.play(to_card(3))
            vo.wait_until("Which two one-line fixes")
            self.play(to_card(4))
            vo.wait_until("and which would an Apple silicon Mac")
            self.play(mark(4, 1))
            vo.wait_until("The answers are in the exercises")
            self.play(FadeOut(cur, shift=UP * 0.2), FadeOut(cur_h), FadeOut(head), FadeOut(dots), run_time=0.5)
            self.play(FadeIn(ans, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("and lecture 23 triggers")
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(VGroup(ans, nxt)), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
