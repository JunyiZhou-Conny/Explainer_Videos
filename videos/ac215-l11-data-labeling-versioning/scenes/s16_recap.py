"""S16 · Monitoring, teardown and recap — `lref("25, 35–36, 38–40")` the whole scene. Ends part 2.

Beats (script.md, ## S16; one voiceover block each):
0. No tracker. Slide 36 redrawn: three question cards (left) and three GREY dashed tool chips in a
   shuffled row below them: Delta Lake / Iceberg · DVC · lakeFS. QUICK 4 s.
1. The chips land beside their questions in the spoken order: DVC ("uses git") · lakeFS ("its own
   history") · Delta Lake / Iceberg ("table versions"). Slide 35's GREY line "no single standard";
   a GREY chip "Milestone 2 accepts a light tool like this one".
2. Monitoring, slides only: V7 (`PipelineMap.at("S16")`) with the GREY dashed watchtower rising, chip
   "this lecture has no monitoring tutorial · slides only"; the map leaves, the tower stays: slide 38's
   five reasons as GREY chips, slide 39's three approaches in one line, slide 40's tools as plain text;
   the YELLOW line "versioning: what changed · monitoring: that something changed".
3. The recap on V7, all dark at first; pieces relight one sentence at a time with their recap badges
   (door, ticket · rule, bouncer · envelope, fuse · shelf, rope). On "Monday's photos" S01's YELLOW
   caption returns small: "which photos ✓ tag · which labels → E7". Then everything unlit.
4. "Test yourself": five questions one at a time (24 pt, ≤ 3 lines), each with a small picture;
   earlier ones collapse into a label list at left.
5. The list fades. TRACKER L1 → L3 in a 10-row laptop terminal at ~/data-versioning: 150 (squeeze),
   151 (2–8, [y/N] y, 9, …, 20), 152 (IMAGE, DISK USAGE; 2.73GB YELLOW + "at the time of recording");
   ▶ your turn. Then the GOLD shutdown checklist card, a line or two per sentence (dvc_store/ RED).
6. Footer cards (exercises.md; the study guide) and the GREY dashed "Next" card (L13). Empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S16"]
QUICK_Q = ("Which images trained this model? · Can I test\nnew images first? · What did this table hold?\n"
           "Which tool answers each?")
QUESTIONS = ("Which images trained this model?", "Can I test new images before everyone uses them?",
             "What did this table hold before the change?")
TOOLS = ("DVC", "lakeFS", "Delta Lake / Iceberg")              # in question order
HOW = ("uses git", "its own history", "table versions")
SHUFFLED = (2, 0, 1)                                          # the column's order: Delta, DVC, lakeFS
NO_TUTORIAL = "this lecture has no monitoring tutorial · slides only"
REASONS = ("quality", "freshness", "drift: suddenly far more photos of one cheese", "cost", "the broken step")
APPROACHES = "three approaches: rules · anomaly detection · lineage + metadata"
OBS_TOOLS = "tools on the slides: Monte Carlo · Datadog · Soda"
RECAP_CAPTION = "which photos ✓ tag · which labels → E7"
TEST_Q = ("Who fetches the photos, and why does that make\nthe bucket need a CORS rule?\nWhy does curl never notice?",
          "cli.py reaches Label Studio at\ndata-label-studio:8080, you at localhost:8080.\nWhy can't they swap?",
          "What is inside cheese_dataset.dvc, and which\nfield changes if you rename one photo?",
          "After dvc add and dvc push, name the\nthree places the photo bytes sit.",
          "You delete gs://…/dvc_store but keep GitHub\nand its tags. What does\ndvc get --rev dataset_v20 do now?")
TEST_MONO = (("curl",), ("cli.py", "data-label-studio:8080", "localhost:8080"), ("cheese_dataset.dvc",),
             ("dvc add", "dvc push"), ("gs://…/dvc_store", "dvc get --rev dataset_v20"))
TEST_LABELS = ("who fetches · CORS", "two addresses", "the pointer", "three homes", "the warehouse")
IMAGE_RM = ("docker image rm data-label-cli data-version-cli \\", "  heartexlabs/label-studio:latest")
STUDY = "MLOps_Learning · guides/L11-data-labeling-versioning.md"


def drop(scene, *mobs) -> None:
    """Take mobjects and their whole families off the scene."""
    fam = []
    for m in mobs:
        fam.extend(m.get_family())
    scene.remove(*fam)


def row_with(rows, sub: str, occurrence: int = 0):
    """The printed terminal row (of `rows`) whose text contains `sub`."""
    return [r for r in rows if sub in r.text][occurrence]


def parts_row(*parts, size: float = 20) -> VGroup:
    """A row of label/mono pieces: str → label INK; (s, 'mono') → mono INK; (s, 'mono', colour) → mono;
    (s, colour) → label in that colour."""
    ms = []
    for p in parts:
        if isinstance(p, str):
            ms.append(label(p, size, INK))
        elif len(p) == 3:
            ms.append(mono(p[0], size, p[2]))
        elif p[1] == "mono":
            ms.append(mono(p[0], size, INK))
        else:
            ms.append(label(p[0], size, p[1]))
    g = VGroup(*ms)
    for a, b in zip(ms, ms[1:]):                  # punctuation hugs the word before it
        punct = b.original_text[:1] in ",:;"
        b.next_to(a, RIGHT, buff=0.04 if punct else 0.12)
    return g


def question_card(s: str, card_w: float) -> VGroup:
    """One of slide 36's example questions as a GREY card, `card_w` wide, left-aligned text."""
    t = label(s, 24, INK)
    fr = RoundedRectangle(width=card_w, height=0.8, corner_radius=0.14, stroke_color=S.GREY,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    t.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def test_text(i: int) -> Text:
    """Recap question i (0-based) at 24 pt, code words in mono."""
    return label(TEST_Q[i], 24, INK, t2f={w: MONO for w in TEST_MONO[i]}, line_spacing=0.9)


def thumb(i: int) -> VGroup:
    """The small picture under recap question i (glyphs only, no answer written on it)."""
    if i == 0:
        return VGroup(url_ticket("Image_1.jpg"), bouncer(0.8)).arrange(RIGHT, buff=0.9)
    if i == 1:
        st = house(CONTAINERS["studio"], 2.3, 0.82)
        cli = house(CONTAINERS["cli"], 1.84, 0.72)
        br = browser_glyph(None, 0.9)
        row = VGroup(br, st, cli).arrange(RIGHT, buff=1.3, aligned_edge=DOWN)
        a1 = arrow(br.get_right(), st.get_left() + DOWN * 0.15, S.GREY)
        a2 = route(cli.get_left() + DOWN * 0.15, st.get_right() + DOWN * 0.15)
        return VGroup(row, a1, a2)
    if i == 2:
        return pointer_card()
    if i == 3:
        boxes = VGroup(*[RoundedRectangle(width=1.7, height=1.0, corner_radius=0.14, stroke_color=c,
                                          stroke_width=3).set_fill(c, 0.07) for c in (CLOUD, LAPTOP, CLOUD)])
        boxes.arrange(RIGHT, buff=0.35)
        qs = VGroup(*[label("?", 30, S.GREY).move_to(b) for b in boxes])
        return VGroup(boxes, qs)
    f = flag("dataset_v20")
    ghost = outline_box(2.2, 1.0, S.GREY, solid=False)
    gt = mono("dvc_store/", 20, S.GREY).move_to(ghost)
    VGroup(f, VGroup(ghost, gt)).arrange(RIGHT, buff=2.2, aligned_edge=DOWN)
    y = f.pole.get_bottom()[1] + 0.2
    rope = DashedLine([f.pole.get_x() + 0.05, y, 0], [ghost.get_left()[0] - 0.7, y, 0], color=ROUTE, stroke_width=3)
    return VGroup(f, VGroup(ghost, gt), rope)


def checklist() -> VGroup:
    """The GOLD shutdown checklist card (script S16, BRIEF 'Costs and teardown'). .rows (13) .frame .head"""
    m = "mono"
    rows = [
        parts_row("containers and the labeling network: already gone (scene 8)"),
        parts_row("keeping bucket 1? in", ("data-labeling", m), "run, in order:"),
        parts_row(("sh docker-shell.sh", m), "·", ("sh docker-shell-CLI.sh", m), "·"),
        parts_row(("python cli.py -r", m), "·", ("exit", m), ("(cli.py:35–38)", S.GREY),
                  "· deleting the bucket removes its rule too"),
        parts_row(("docker-volumes/label-studio", m), "· delete only when done with the project (sudo on Linux)"),
        parts_row("buckets bill until deleted:", ("cheeses_unlabeled/", m), "·", ("cheeses_labeled/", m), "·",
                  ("images/", m)),
        parts_row("never", ("dvc_store/", m, ERR), "while a tag should still work"),
        parts_row((".dvc/cache", m), "· safe to delete once pushed"),
        parts_row("delete the key and its JSON in secrets when the course is done"),
        parts_row(("(IAM › Service accounts › Keys)", S.GREY)),
        parts_row(("optional, frees about 6 GB:", S.GREY)),
        parts_row((IMAGE_RM[0], m, S.GREY)),
        parts_row((IMAGE_RM[1], m, S.GREY)),
    ]
    c = card(rows, color=COST, size=20, buff=0.14, head="shutdown list")
    for k in (2, 3, 9, 12):                         # continuation rows, indented (Text drops leading spaces)
        rows[k].shift(RIGHT * 0.4)
    c.rows = rows
    return c


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S16"] == 7, len(SAY)
        c150, c151, c152 = capture("150"), capture("151"), capture("152")
        dv = "data-versioning"
        assert c150.cmd in readme(410, dv) and c151.cmd in readme(418, dv) and c152.cmd in readme(424, dv)
        assert '"-r"' in excerpt("data-labeling/cli.py", 144, 144)
        assert "bucket.cors = []" in excerpt("data-labeling/cli.py", 35, 38)

        # ========================================================== 0. quick predict: three questions, three tools
        ref = lref("25, 35–36, 38–40")
        ys = (1.75, 0.65, -0.45)
        cw = max(label(s, 24).width for s in QUESTIONS) + 0.5
        qc = [question_card(s, cw).move_to([-6.45 + cw / 2, y, 0]) for s, y in zip(QUESTIONS, ys)]
        chips = [dashed_chip(s, size=20) for s in TOOLS]
        VGroup(*[chips[j] for j in SHUFFLED]).arrange(RIGHT, buff=0.8).move_to([0, -1.75, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), run_time=0.5)
            vo.wait_until("three questions")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in qc], lag_ratio=0.25), run_time=1.0)
            vo.wait_until("three tools")
            self.play(LaggedStart(*[FadeIn(chips[j], shift=LEFT * 0.3) for j in SHUFFLED], lag_ratio=0.25),
                      run_time=0.9)
            vo.wait_until("Match Delta Lake")
            self.play(Indicate(chips[2].text, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("DVC, and lakeFS")
            self.play(Indicate(chips[0].text, color=INK, scale_factor=1.15), run_time=0.5)
            self.play(Indicate(chips[1].text, color=INK, scale_factor=1.15), run_time=0.5)
        qp = quick_predict(self, QUICK_Q, seconds=4)

        # ========================================================== 1. the answers; no single standard
        hows = [note(s, S.GREY, 20) for s in HOW]
        std = label("no single standard: pick by your data, its size and your platform", 24, S.GREY)
        std.move_to([0, -1.75, 0])
        ms = grey_chip("Milestone 2 accepts a light tool like this one", size=22).move_to([0, -2.6, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(qp), run_time=0.4)
            self.remove(qp)
            for k, anchor in enumerate(("DVC, lakeFS", "lakeFS, then", "then the table formats")):
                vo.wait_until(anchor)
                c = chips[k]
                tgt = np.array([qc[k].frame.get_right()[0] + 0.22 + c.width / 2, ys[k], 0])
                hows[k].next_to(tgt + RIGHT * c.width / 2, RIGHT, buff=0.2)
                self.play(c.animate.move_to(tgt), qc[k].frame.animate.set_stroke(INK), run_time=0.7)
                self.play(FadeIn(hows[k], shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("There is no single standard")
            self.play(FadeIn(std, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("your project milestone accepts")
            self.play(FadeIn(ms, shift=UP * 0.15), run_time=0.6)
            flash_tag(self, ms, INK)

        # ========================================================== 2. monitoring, slides only
        m2 = PipelineMap.at("S16")
        tw = m2.tower
        nt = dashed_chip(NO_TUTORIAL, size=20)
        nt.move_to([tw.get_left()[0] - 0.3 - nt.width / 2, 2.55, 0])
        rs = [grey_chip(s, size=22) for s in REASONS]
        r1 = VGroup(*rs[:3]).arrange(RIGHT, buff=0.3)
        r2 = VGroup(*rs[3:]).arrange(RIGHT, buff=0.3)
        VGroup(r1, r2).arrange(DOWN, buff=0.3).move_to([0, 0.6, 0])
        ap = label(APPROACHES, 24, S.GREY).move_to([0, -0.75, 0])
        ot = label(OBS_TOOLS, 22, S.GREY).move_to([0, -1.35, 0])
        yl = VGroup(label("versioning: what changed", 30, TURN), label("·", 30, TURN),
                    label("monitoring: that something changed", 30, TURN)).arrange(RIGHT, buff=0.3)
        yl.move_to([0, -2.35, 0])

        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(*qc, *chips, *hows, std, ms)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(m2), run_time=0.7)
            vo.wait_until("ends with monitoring")
            self.play(FadeIn(tw, shift=UP * 0.5), run_time=0.8)
            self.play(FadeIn(nt, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("watch quality")
            self.play(FadeOut(m2), run_time=0.5)
            drop(self, m2)
            self.add(tw)
            self.play(FadeIn(rs[0], shift=UP * 0.15), run_time=0.35)
            for k, anchor in ((1, "freshness"), (2, "drift"), (3, "cost and"), (4, "broken steps")):
                vo.wait_until(anchor)
                self.play(FadeIn(rs[k], shift=UP * 0.15), run_time=0.35)
            self.play(Indicate(rs[2].text, color=INK, scale_factor=1.06), run_time=0.6)
            self.play(FadeIn(ap, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(ot, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Versioning tells you")
            self.play(FadeIn(yl[0], shift=UP * 0.15), run_time=0.5)
            vo.wait_until("monitoring tells you")
            self.play(FadeIn(yl[1]), FadeIn(yl[2], shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(tw[0], color=INK, scale_factor=1.1), run_time=0.6)

        # ========================================================== 3. the recap on one map
        m = PipelineMap.at("S16", lit=())
        mk = {k: m.mark(k) for k in ("door", "ticket", "rule", "bouncer", "envelope", "fuse", "shelf", "rope")}
        cap = label(RECAP_CAPTION, 26, TURN).move_to([0, -2.25, 0])

        def badge(*keys):
            return LaggedStart(*[FadeIn(mk[k], scale=0.6) for k in keys], lag_ratio=0.3, run_time=0.6)

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(tw, nt, r1, r2, ap, ot, yl)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(m), run_time=0.6)
            vo.wait_until("Label Studio runs in a container")
            self.play(m.light("studio", "street"), run_time=0.7)
            self.play(badge("door"))
            vo.wait_until("and signs tickets")
            self.play(m.light("bucket1"), run_time=0.6)
            self.play(badge("ticket"))
            vo.wait_until("A rule on the bucket")
            self.play(badge("rule"))
            vo.wait_until("the browser")
            self.play(badge("bouncer"))
            vo.wait_until("Labels are small notes")
            self.play(m.light("labeled", "cli"), run_time=0.6)
            self.play(badge("envelope"))
            vo.wait_until("a mounted bucket feeds DVC")
            self.play(m.light("dvc", "bucket2", "fuse"), run_time=0.8)
            self.play(badge("fuse"))
            vo.wait_until("Photos are filed by fingerprint")
            self.play(m.light("remote"), run_time=0.6)
            self.play(badge("shelf"))
            vo.wait_until("a tag pins the list")
            self.play(m.light("flag_v20", "flag_v21", "repo"), run_time=0.6)
            self.play(badge("rope"))
            vo.wait_until("So Monday's photos")
            self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("with one dvc get")
            self.play(m.light("colab"), run_time=0.6)
            self.play(Indicate(m.colab.text, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("their labels join")
            self.play(Indicate(m.bridge.caption, color=TURN, scale_factor=1.08), run_time=0.8)
            marks = VGroup(*mk.values())
            self.play(m.all_dark(), FadeOut(marks), run_time=1.0)
            drop(self, marks)

        # ========================================================== 4. test yourself
        head = label("Test yourself", 32, INK).move_to([-6.3, 2.55, 0], aligned_edge=LEFT)
        ul = under(head, TURN, stroke=3, pad=0.1)
        QX = 1.9                                     # the question column's centre
        qs = [test_text(i) for i in range(5)]
        ths = [thumb(i) for i in range(5)]
        for q, th in zip(qs, ths):
            q.move_to([QX, 1.55, 0])
            q.shift(UP * (2.3 - q.get_top()[1]))
            th.move_to([QX, -1.25, 0])
        lbls = [VGroup(label(f"{i + 1}", 22, TURN), label(s, 22, INK)).arrange(RIGHT, buff=0.2)
                for i, s in enumerate(TEST_LABELS)]
        for i, lb in enumerate(lbls):
            lb.move_to([-6.3, 1.6 - i * 0.55, 0], aligned_edge=LEFT)

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(m, cap)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(head, shift=DOWN * 0.15), Create(ul), run_time=0.6)
            for i, anchor in enumerate(("One: who fetches", "Two: why can't", "Three: what is in",
                                        "Four: where do", "Five: without")):
                vo.wait_until(anchor)
                if i:                                # the old question leaves before the new one lands
                    self.play(FadeOut(VGroup(qs[i - 1], ths[i - 1]), shift=LEFT * 0.4),
                              FadeIn(lbls[i - 1], shift=LEFT * 0.4), run_time=0.35)
                    drop(self, qs[i - 1], ths[i - 1])
                self.play(FadeIn(qs[i], shift=UP * 0.2), FadeIn(ths[i], shift=UP * 0.2), run_time=0.45)
            self.play(Indicate(ths[4][2], color=ROUTE, scale_factor=1.1), run_time=0.7)
            self.play(FadeIn(lbls[4], shift=LEFT * 0.4), run_time=0.5)

        # ========================================================== 5. cleanup and the shutdown list
        tr = tracker("L", 1)
        t = term(P_VERSIONING, rows=10)
        gone = VGroup(head, ul, qs[4], ths[4], *lbls)
        self.play(FadeOut(gone), run_time=0.5)
        drop(self, gone)
        self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), run_time=0.5)
        type_cmd(self, t, c150.cmd, type_time=0.35)
        out(self, t, squeeze(c150.at(2)), run_time=0.3)
        ck = checklist()
        ck.move_to([0, -0.35, 0])
        ct = cost_tag("storage bills until deleted")
        ct.move_to(ck.frame.get_corner(UR) + np.array([-0.3 - ct.width / 2, 0, 0]))
        red = ring(ck.rows[6], ERR, buff=0.06)
        # prune runs before the voice, so docker image ls has printed when it says "pause"
        self.play(track(tr, 2), run_time=0.3)
        type_cmd(self, t, c151.cmd, type_time=0.4)
        out(self, t, c151.at((2, 7)), run_time=0.4)
        q = c151.line(8)
        ask = q[:q.index("[y/N]") + len("[y/N]")]
        assert q == ask + " y"
        ask_ln = out(self, t, [ask], run_time=0.2)[0]
        self.wait(0.4)
        yln = mono_line(q, t.size, OUTPUT)
        yln.shift(ask_ln.strut.get_corner(UL) - yln.strut.get_corner(UL))
        yg = yln.glyphs[-1].set_color(TURN)
        self.play(FadeIn(yg, scale=1.6), run_time=0.2)
        self.play(yg.animate.set_color(OUTPUT), run_time=0.2)
        attach(self, ask_ln, yg)
        out(self, t, [c151.line(9), "…", c151.line(20)], run_time=0.3)

        with self.voiceover(SAY[5]) as vo:
            self.play(track(tr, 3), run_time=0.25)
            type_cmd(self, t, c152.cmd, type_time=0.25)
            r152 = out(self, t, cols(c152.at((2, 5)), ["IMAGE", "DISK USAGE"]), run_time=0.3)
            dvr = row_with(r152, "data-version-cli")
            self.play(substring(dvr, "2.73GB").animate.set_color(TURN), run_time=0.3)
            pin(self, dvr, beside(time_row(), dvr, buff=0.4), run_time=0.3)
            vo.wait_until("pause and run them")
            yt = on_bar(t, turn_row())
            self.play(FadeIn(yt), run_time=0.3)
            flash_tag(self, yt, TURN)
            vo.wait_until("remove its CORS rule")
            gone = VGroup(t, yt, *t.lines)
            self.play(FadeOut(gone), run_time=0.4)
            drop(self, gone)
            self.play(FadeIn(ck.frame), FadeIn(ck.head), FadeIn(ck.rows[0], shift=RIGHT * 0.2), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in ck.rows[1:4]], lag_ratio=0.3),
                      run_time=0.6)
            self.play(Indicate(ck.rows[3][1], color=TURN, scale_factor=1.1), run_time=0.6)
            self.play(FadeIn(ck.rows[4], shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Buckets cost money")
            self.play(FadeIn(ck.rows[5], shift=RIGHT * 0.2), FadeIn(ct, shift=DOWN * 0.1), run_time=0.5)
            flash_tag(self, ct, COST)
            vo.wait_until("but never delete the DVC store")
            self.play(FadeIn(ck.rows[6], shift=RIGHT * 0.2), Create(red), run_time=0.6)
            self.play(Indicate(ck.rows[6][1], color=ERR, scale_factor=1.12), run_time=0.6)
            vo.wait_until("a tag is only a pointer")
            self.play(FadeIn(ck.rows[7], shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Delete the key")
            self.play(FadeIn(ck.rows[8], shift=RIGHT * 0.2), FadeIn(ck.rows[9], shift=RIGHT * 0.2), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in ck.rows[10:]], lag_ratio=0.3),
                      run_time=0.8)

        # ========================================================== 6. footer and next
        f1 = card([parts_row("Answers:", ("exercises.md", "mono"), size=24)], size=24)
        f2 = card([label("Study guide + every command:", 24, INK), mono(STUDY, 22, INK)], size=24)
        nx = card([label("Next · L13", 24, INK),
                   label("trains on the labeled cheeses from a prepared zip", 22, S.GREY),
                   parts_row(("swap that download for", S.GREY), ("dvc get --rev", "mono", S.GREY),
                             ("to make a run reproducible", S.GREY), size=22)],
                  color=FUTURE, size=24, dashed=True)
        f1.move_to([0, 2.05, 0])
        f2.move_to([0, 0.75, 0])
        nx.move_to([0, -1.3, 0])

        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(ck, ct, red, tr)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            vo.wait_until("Answers are in the exercises")
            self.play(FadeIn(f1, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(f2, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Lecture 13 trains")
            self.play(FadeIn(nx, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("a tagged version")
            self.play(Indicate(nx.body[2][1], color=INK, scale_factor=1.1), run_time=0.7)

        self.wait(0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
