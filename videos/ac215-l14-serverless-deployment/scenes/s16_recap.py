"""S16 · Clean up, and what serverless costs — tracker [CU] 1 → 4 (beats 0–3), then no tracker; lecture
tags slide 16 (beats 5–7) and slide 9 (beat 8). Ends part 2 on an empty frame.

Beats (script.md "## S16"; one voiceover block each):
0. TRACKER [CU] 1 appears. The GOLD checklist card (README.md · lines 1020–1028, GOLD cost tag "billed
   until deleted"); item 1 "download what you want to keep" writes in and ticks. [CU] 2: item 2 "delete
   translate-function, translation-demo, then the job translation-audio"; the three BLUE worksheet
   cards fly in on the right and dissolve one by one as they are named; item 2 ticks.
1. [CU] 3: item 3 "delete the objects and buckets, then the two runtime accounts once detached"; two
   BLUE buckets, then the two runtime badges, dissolve. [CU] 4: item 4 "the function's image in
   Artifact Registry": V3's shelf returns with the function's TEAL image, GOLD tag "still billed as
   storage"; the image is removed. YELLOW ▶ your turn beside the checklist.
2. Beside the card, a GOLD card "what the README's list leaves out" (tag erratum): "soft-deleted files:
   recoverable and billable for the retention period" (docs/lifecycle.md:176-177), "the build leaves
   source archives and logs" (docs/lifecycle.md:205-210), GREEN "keep the shared public image · others
   use it" (README:1027-1028). Under both, GREY "optional · on your laptop · not typed" with three
   GREY mono chips (gcloud auth application-default revoke · rm -rf ~/fn-venv · docker image rm <the
   public image>), tag extra.
3. [CU] 4. README card (README.md · lines 1035–1046, Symptom | Check; long checks cut with "…"), GREY
   chip "stuck? start here"; a second GREY chip, silent: "optional: a scripted separate practice stack
   · its own names · its clean up removes only its own · gcloud/20" (README:1061-1064,
   docs/lifecycle.md:3-4). Fade out (tracker too).
4. No tracker. V1 DeployGrid complete (L1/L2 ticks, today, part chips, service | job split), centred.
   On "a file" the file cell's lid lifts on its TEAL box ("by Cloud Build") and the Part 1 chip
   pulses. On "one image" chips 2–4 pulse; the service half's instance shrinks to zero and back
   (scales to zero), then the job half pulses and a small GREEN receipt ribbon lands on it.
5. Lecture 14 · slide 16. The grid slides right; slide 16's three cons hang under the serverless row
   as RED cards. "Cold starts": GREEN answer "min instances ≥ 1 / warmth for money"; on the left V2's
   always-on instance (a min instances slider 0 → 1, a faint instance over the whole time, its GOLD
   drip "billed while idle").
6. "Limited control and debugging": GREEN answer "three places / to look"; on the left the where-to-look
   card, its three slots filling and lighting as named: build logs · Part 1, service logs · Parts 1, 3,
   job logs + manifest · Part 4.
7. "Vendor lock-in": on the left two GREY laptop icons "functions-framework ran here", "the image ran
   here"; BLUE chips "console", "IAM", "Cloud Build" under "the Google-specific parts"; GREEN answer
   "the image and framework / ran on your laptop".
8. Lecture 14 · slide 9. The grid and cons shrink away; slide 9's braces return on a GREY timeline
   under "serverless": LAST WEEK (L13) and TODAY (L14) dim, the NEXT brace lights GREY-dashed "L15 ·
   Vertex AI endpoint · for a trained model · pipelines".
9.–13. "Test yourself" (YELLOW heading, "question k of 5", answers in exercises.md): one YELLOW
   question card at a time with a small text-free picture that pulses once on its phrase: V1 grid
   outline (cells empty) · V2 meter that ticks · a two-door V6 icon (each door pulses on its phrase) ·
   a small chip row (pulses on "eleven") · three small RED con cards (pulse in turn) + GREY chip
   "answers: exercises.md". Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _door
from explainer.devops import laptop

SAY = NARRATION["S16"]

LEFT_X = -4.15             # centre of the free column left of the grid (beats 5-7), x in [-6.55, -1.75]
GRID_RIGHT = 0.5           # the grid's shift in beats 5-7 (its row headers start at x -1.55)
GRID_CENTRE = -1.9         # the grid's shift in beat 4 (centred)
CHECK_W = 7.0              # widest Check text in the troubleshooting card

QUESTIONS = (
    "Place Parts 1 and 2 on the lecture's 2×2:\nwhat do you hand over, and who\nbuilds the image in each case?",
    "Which two settings make the meter run\nwhile nobody is using the app, and\nwhat does min instances buy you?",
    "Who may call it, and who it runs as:\nwhich setting answers each, and\nwhy is no key file needed?",
    "Why does the job set a command\nand eleven separate arguments,\nand what happens with neither?",
    "Name the lecture's three downsides\nof serverless, and what this tutorial\ngives you for each.",
)
CONS = ("cold starts", "limited control\nand debugging", "vendor lock-in")
EXTRA_CMDS = ("gcloud auth application-default revoke", "rm -rf ~/fn-venv")
PRACTICE = ("optional: a scripted separate practice stack · its own names ·",
            "its clean up removes only its own · gcloud/20")


def parts_row(*parts, size: float = 20) -> VGroup:
    """A row of pieces: str → label INK; (s, 'm') → mono INK; (s, colour) → label in that colour."""
    ms = []
    for p in parts:
        if isinstance(p, str):
            ms.append(label(p, size, INK))
        elif p[1] == "m":
            ms.append(mono(p[0], size, INK))
        else:
            ms.append(label(p[0], size, p[1]))
    g = VGroup(*ms)
    for a, b in zip(ms, ms[1:]):
        punct = b.original_text[:1] in ",:;"
        b.next_to(a, RIGHT, buff=0.04 if punct else 0.12)
        if punct:
            b.align_to(a, DOWN)
    return g


def checklist() -> VGroup:
    """The README's clean-up list (README:1020-1028) as a GOLD card. .rows (7) .items (4 groups of rows)
    .ticks (4 tick positions) .frame .head"""
    n = lambda k: (k, COST)  # noqa: E731
    rows = [
        parts_row(n("1"), "download what you want to keep"),
        parts_row(n("2"), "delete", (FUNCTION, "m"), (",", INK)),
        parts_row((SERVICE, "m"), (",", INK), "then the job"),
        parts_row((JOB, "m")),
        parts_row(n("3"), "delete the objects and buckets, then the two"),
        parts_row("runtime accounts once detached"),
        parts_row(n("4"), "the function's image in Artifact Registry"),
    ]
    c = card(rows, COST, size=20, buff=0.16, head="Clean up · README.md · lines 1020–1028")
    for k in (2, 3, 5):
        rows[k].shift(RIGHT * 0.27)
    # widen the frame so a tick fits right of the widest row
    fr = c.frame
    wide = outline_box(fr.width + 0.55, fr.height, COST, solid=True, fill_opacity=0.08)
    wide.fill.set_fill(S.GREY_DARKER, 1)
    wide.move_to(fr).align_to(fr, LEFT)
    c.remove(fr)
    c.submobjects.insert(0, wide)
    c.frame = wide
    c.rows = rows
    c.items = [VGroup(rows[0]), VGroup(rows[1], rows[2], rows[3]), VGroup(rows[4], rows[5]), VGroup(rows[6])]
    c.tick_rows = [rows[i] for i in (0, 1, 4, 6)]
    return c


def fit_words(s: str, max_w: float, size: float = 20) -> str:
    """Cut s at a word boundary (adding ' …') until label(s) is at most max_w wide."""
    if label(s, size).width <= max_w:
        return s
    words = s.split(" ")
    while words and label(" ".join(words) + " …", size).width > max_w:
        words.pop()
    return " ".join(words).rstrip(",;") + " …"


def trouble_card() -> VGroup:
    """README.md · lines 1035–1046 (Symptom | Check), markdown stripped; long checks cut with '…'."""
    rows = []
    for n in range(1037, 1047):
        cells = [c.strip() for c in readme(n).strip().strip("|").split("|")]
        assert len(cells) == 2, cells
        rows.append([c.replace("`", "").replace("**", "") for c in cells])
    head = [c.strip() for c in readme(1035).strip().strip("|").split("|")]
    assert head == ["Symptom", "Check"], head
    x2, pitch = 4.9, 0.37
    body = VGroup(label("Symptom", 20, S.GREY).move_to(ORIGIN, aligned_edge=LEFT),
                  label("Check", 20, S.GREY).move_to([x2, 0, 0], aligned_edge=LEFT))
    for i, (sy, ck) in enumerate(rows):
        y = -(i + 1) * pitch
        body.add(label(sy, 20, INK).move_to([0, y, 0], aligned_edge=LEFT))
        body.add(label(fit_words(ck, CHECK_W), 20, INK).move_to([x2, y, 0], aligned_edge=LEFT))
    return readme_card((1035, 1046), body)


def ribbon(w: float = 0.62, color=OWN) -> VMobject:
    """A text-free GREEN receipt ribbon (manifest.json's 'complete')."""
    h = w * 0.42
    return Polygon([-w / 2, h / 2, 0], [w / 2 - 0.1, h / 2, 0], [w / 2, 0, 0], [w / 2 - 0.1, -h / 2, 0],
                   [-w / 2, -h / 2, 0], stroke_color=color, stroke_width=3).set_fill(color, 0.35)


def bracket(x0: float, x1: float, y: float, color, dashed: bool) -> VMobject:
    """Slide 9's brace as a squared bracket under [x0, x1] at y, pointing down (as S02 draws it)."""
    xm, d = (x0 + x1) / 2, 0.16
    m = VMobject(stroke_color=color, stroke_width=3)
    m.set_points_as_corners([[x0, y, 0], [x0, y - d, 0], [xm - d, y - d, 0], [xm, y - 2 * d, 0],
                             [xm + d, y - d, 0], [x1, y - d, 0], [x1, y, 0]])
    if dashed:
        m = DashedVMobject(m, num_dashes=int((x1 - x0) * 6), dashed_ratio=0.55).set_stroke(color, 3)
    return m


def week_card(head: str, rows, color, dashed: bool, x: float, y: float) -> VGroup:
    txt = S.GREY if dashed else INK
    c = card([label(r, 20, txt) for r in rows], color, size=20, dashed=dashed, head=head, card_w=3.6)
    if not dashed:
        c.frame.frame.set_stroke(color, 3)
        c.head.set_color(color)
    c.move_to([x, y, 0])
    return c


def dim(m, f: float = 0.4) -> None:
    """Fade a group to f of its current opacities (fill and stroke separately; empty fills stay empty)."""
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=sm.get_stroke_opacity() * f)
        sm.set_fill(opacity=sm.get_fill_opacity() * f)


def doors_icon() -> VGroup:
    """A small text-free V6 icon: a BLUE service box with a door on each side. .left .right"""
    sb = RoundedRectangle(width=2.4, height=1.4, corner_radius=0.12, stroke_color=CLOUD,
                          stroke_width=3).set_fill(CLOUD, 0.08)
    dl, dr = _door(S.GREY, 0.7).move_to(sb.get_left()), _door(S.GREY, 0.7).move_to(sb.get_right())
    g = VGroup(sb, dl, dr)
    g.left, g.right = dl, dr
    return g


class CleanUpRecap(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S16"] == 14, len(SAY)
        assert readme(1018) == "## Clean up after the tutorial"
        assert readme(1020) == "1. Download any results you want to keep."
        assert "delete the function and web service you created, then delete" in readme(1021)
        assert "delete your tutorial input/output objects and buckets" in readme(1023)
        assert "after they are no longer attached to resources." in readme(1025)
        assert "leaves an image in Artifact Registry" in readme(1026)
        assert "the shared\n   public tutorial image available for others" in excerpt("README.md", 1027, 1028)
        assert "recoverable and billable during that period" in excerpt("docs/lifecycle.md", 176, 177)
        assert "build logs, source archives and images" in excerpt("docs/lifecycle.md", 205, 205)
        assert "practice stack" in excerpt("README.md", 1061, 1064) and "separate practice stack" in \
            excerpt("docs/lifecycle.md", 3, 4)
        assert capture("gcloud/20").cmd_lines[0].startswith("python tutorial/spin_up.py")

        # ========================================================== 0. download, delete the three runtimes
        tr = tracker_cu(1)
        cl = checklist()
        cl.move_to([-6.5 + cl.width / 2, 2.72 - cl.height / 2, 0])
        assert cl.get_top()[1] < TRACK_BOTTOM - 0.05, cl.get_top()
        ctag = cost_tag("billed until deleted")
        ctag.move_to(cl.frame.get_corner(UR) + np.array([-ctag.width / 2 - 0.25, 0, 0]))
        ticks = [check_glyph(0.28).move_to([cl.frame.get_right()[0] - 0.35, r.get_center()[1], 0])
                 for r in cl.tick_rows]
        rx = (cl.get_right()[0] + 6.55) / 2          # centre of the column right of the card
        rw = 6.55 - cl.get_right()[0]
        ws = [worksheet_card(FUNCTION, "function"), worksheet_card(SERVICE, "web service"),
              worksheet_card(JOB, "job")]
        VGroup(*ws).arrange(DOWN, buff=0.3).move_to([rx, 0.9, 0])
        assert max(w.width for w in ws) < rw - 0.3, rw
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(VGroup(cl.frame, cl.head), shift=DOWN * 0.1), FadeIn(ctag), run_time=0.6)
            vo.wait_until("Step 1")
            self.play(FadeIn(cl.items[0], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Create(ticks[0]), run_time=0.4)
            vo.wait_until("Step 2")
            self.play(track(tr, 2), FadeIn(cl.items[1], shift=RIGHT * 0.15), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(w, shift=LEFT * 0.6) for w in ws], lag_ratio=0.25), run_time=0.8)
            for w, anchor in zip(ws, ("delete translate-function", "and translation-demo", "then the job")):
                vo.wait_until(anchor)
                self.play(Indicate(w.text, color=INK, scale_factor=1.08), run_time=0.4)
                self.play(FadeOut(w, scale=0.4), run_time=0.45)
            self.play(Create(ticks[1]), run_time=0.4)

        # ========================================================== 1. buckets, accounts, the leftover image
        bks = VGroup(bucket(IN_BUCKET, 0.8), bucket(OUT_BUCKET, 0.8)).arrange(DOWN, buff=0.3)
        bdg = VGroup(badge(RUNTIME_SA), badge(JOB_SA)).arrange(DOWN, buff=0.25)
        VGroup(bks, bdg).arrange(DOWN, buff=0.4).move_to([rx, 0.55, 0])
        assert bdg.width < rw - 0.2 and bdg.get_bottom()[1] > -3.4, (bdg.width, rw)
        shelf = registry_shelf(True, shelf_w=2.6).move_to([rx, 0.9, 0])
        stag = cost_tag("still billed as storage").next_to(shelf, DOWN, buff=0.35)
        yt = your_turn().next_to(cl, RIGHT, buff=0.35).align_to(cl, DOWN)
        with self.voiceover(SAY[1]) as vo:
            self.play(track(tr, 3), FadeIn(cl.items[2], shift=RIGHT * 0.15), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.4) for b in bks], lag_ratio=0.3), run_time=0.7)
            vo.wait_until("and the two runtime accounts")
            self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.4) for b in bdg], lag_ratio=0.3), run_time=0.7)
            vo.wait_until("once nothing uses them")
            self.play(LaggedStart(*[FadeOut(b, scale=0.4) for b in bks], lag_ratio=0.3), run_time=0.6)
            self.play(LaggedStart(*[FadeOut(b, scale=0.4) for b in bdg], lag_ratio=0.3), run_time=0.6)
            self.play(Create(ticks[2]), run_time=0.4)
            vo.wait_until("Step 4")
            self.play(track(tr, 4), FadeIn(cl.items[3], shift=RIGHT * 0.15), run_time=0.6)
            self.play(FadeIn(shelf, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("still there after the service is gone")
            self.play(FadeIn(stag, shift=UP * 0.1), run_time=0.5)
            flash_tag(self, stag)
            self.play(FadeOut(shelf.image, shift=UP * 0.5), FadeOut(stag), run_time=0.6)
            self.play(Create(ticks[3]), run_time=0.4)
            vo.wait_until("Pause and delete them all now")
            self.play(FadeOut(VGroup(shelf.board, shelf.text)), FadeIn(yt, shift=LEFT * 0.15), run_time=0.5)
            flash_tag(self, yt)

        # ========================================================== 2. what the README's list leaves out
        add_rows = [
            label("soft-deleted files: recoverable and", 20, INK),
            label("billable for the retention period", 20, INK),
            label("the build leaves source archives and logs", 20, INK),
            label("keep the shared public image · others use it", 20, OWN),
        ]
        adds = card(add_rows, COST, size=20, buff=0.16, head="what the README's list leaves out")
        adds.move_to([rx, 0, 0]).align_to(cl, UP)
        etag = erratum_tag()
        etag.move_to(adds.frame.get_corner(UR) + np.array([-etag.width / 2 - 0.25, 0, 0]))
        assert adds.get_right()[0] < 6.55 and adds.get_left()[0] > cl.get_right()[0] + 0.15, (cl.get_right(), adds.width)
        gl = VGroup(label("optional · on your laptop · not typed", 20, S.GREY), extra_tag())
        gl.arrange(RIGHT, buff=0.25)
        ch1 = VGroup(*[grey_chip(s, mono_font=True) for s in EXTRA_CMDS]).arrange(RIGHT, buff=0.2)
        dk_t = VGroup(mono("docker image rm \\", 20, INK), mono("  " + IMAGE_REF, 20, INK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        dk_b = box(dk_t.width + 0.5, dk_t.height + 0.3, S.GREY, fill_opacity=0.16, radius=0.14)
        dk_t.move_to(dk_b)
        dk = VGroup(dk_b, dk_t)
        xb = VGroup(gl, ch1, dk).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        xb.move_to([-6.45 + xb.width / 2, 0, 0]).align_to(cl, LEFT)
        xb.shift(UP * (cl.get_bottom()[1] - 0.25 - xb.get_top()[1]))
        assert xb.get_bottom()[1] > -3.5 and xb.get_right()[0] < 6.55, xb.get_corner(DR)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(yt), FadeIn(adds.frame), FadeIn(adds.head), FadeIn(etag), run_time=0.6)
            vo.wait_until("Soft-deleted files")
            self.play(FadeIn(VGroup(*add_rows[:2]), shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("the build also leaves")
            self.play(FadeIn(add_rows[2], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("And keep the shared public image")
            self.play(FadeIn(add_rows[3], shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in [*ch1, dk]], lag_ratio=0.3), run_time=0.9)
        self.wait(1.2)

        # ========================================================== 3. stuck? the troubleshooting table
        tc = trouble_card()
        tc.move_to([0, 2.72 - tc.height / 2, 0])
        assert tc.get_top()[1] < TRACK_BOTTOM - 0.05 and tc.width < 13.0, (tc.get_top(), tc.width)
        stuck = grey_chip("stuck? start here")
        stuck.move_to([tc.frame.get_right()[0] - 0.3 - stuck.width / 2, tc.head.get_center()[1] - 0.05, 0])
        prac = card(PRACTICE, S.GREY, size=20, buff=0.1)
        prac.next_to(tc, DOWN, buff=0.25).align_to(tc, LEFT)
        assert prac.get_bottom()[1] > -3.5 and prac.get_right()[0] < 6.55, prac.get_corner(DR)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(cl, ctag, *ticks, adds, etag, xb)), run_time=0.5)
            vo.wait_until("The README ends with")
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(stuck, shift=RIGHT * 0.15), run_time=0.4)
            vo.wait_until("of symptoms and checks")
            self.play(Indicate(tc.body[0], color=TURN, scale_factor=1.1),
                      Indicate(tc.body[1], color=TURN, scale_factor=1.1), run_time=0.7)
        self.play(FadeIn(prac, shift=UP * 0.1), run_time=0.5)
        self.wait(2.2)

        # ========================================================== 4. the whole map
        g = DeployGrid(built=True, sketch=False)
        g.shift(RIGHT * GRID_CENTRE)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(tc, stuck, prac, tr)), run_time=0.5)
            self.play(FadeIn(g, shift=UP * 0.15), run_time=0.6)
            g.tick_vm(self, run_time=0.5)
            g.today(self, run_time=0.4)
            g.split_job(self, run_time=0.5)
            g.parts(self, run_time=0.6)
            vo.wait_until("Part 1 handed over a file")
            self.play(g.pulse_part(0), run_time=0.6)
            g.open_lid(self, "by Cloud Build", run_time=1.0)
            vo.wait_until("and Cloud Build made the image")
            self.play(Indicate(g.lid[1].text, color=INK, scale_factor=1.12), run_time=0.6)
            self.add(g)
            vo.wait_until("Parts 2 to 4 handed over one image")
            self.play(LaggedStart(g.pulse_part(1), g.pulse_part(2), g.pulse_part(3), lag_ratio=0.25),
                      self.cells_light(g), run_time=1.0)
            vo.wait_until("a service that scales to zero")
            s_inst = g.split.service[0]
            self.play(Indicate(g.split.service[1], color=TURN, scale_factor=1.15), run_time=0.5)
            self.play(s_inst.animate(rate_func=there_and_back).scale(0.05), run_time=1.2)
            vo.wait_until("and a job that exits with a receipt")
            self.play(Indicate(g.split.job[2], color=TURN, scale_factor=1.15), run_time=0.5)
            rb = ribbon().move_to(g.split.job[0].get_center() + UP * 0.02)
            g.show(self, rb, anims=[FadeIn(rb, shift=DOWN * 0.3, scale=1.4)], run_time=0.6)

        # ========================================================== 5. slide 16: cold starts
        r16 = lref("16")
        sld = Slider("min instances", (0, 1))
        sld.move_to([LEFT_X, 1.55, 0])
        inst = instance(3.8, 0.55)
        inst.move_to([LEFT_X, 0.55, 0])
        inst_l = label("always on", 20, INK).next_to(inst, UP, buff=0.12).align_to(inst, LEFT)
        drip = Rectangle(width=3.8, height=0.14, stroke_width=0).set_fill(COST, 0.85)
        drip.next_to(inst, DOWN, buff=0.14)
        drip_l = label("billed while idle", 20, COST).next_to(drip, DOWN, buff=0.14).align_to(drip, LEFT)
        mini = VGroup(sld, inst, inst_l, drip, drip_l)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeIn(r16), g.animate.shift(RIGHT * (GRID_RIGHT - GRID_CENTRE)), run_time=0.8)
            vo.wait_until("three downsides")
            g.cons(self, CONS, run_time=1.2)
            assert mini.get_left()[0] > -6.55 and mini.get_right()[0] < g.con_cards[0].get_left()[0] - 0.1
            vo.wait_until("Cold starts")
            self.play(Indicate(g.con_cards[0].body, color=ERR, scale_factor=1.12), run_time=0.6)
            vo.wait_until("a minimum of 1")
            self.play(FadeIn(sld, shift=RIGHT * 0.15), run_time=0.4)
            self.play(sld.to(1), run_time=0.6)
            self.play(FadeIn(inst), FadeIn(inst_l), run_time=0.4)
            self.play(GrowFromEdge(drip, LEFT, rate_func=linear), FadeIn(drip_l), run_time=1.4)
            vo.wait_until("for money")
            a0 = g.answer(self, 0, "min instances ≥ 1\nwarmth for money")
            assert a0.get_bottom()[1] > -3.55, a0.get_bottom()

        # ========================================================== 6. limited control: where to look
        wl = WhereToLook(card_w=4.8)
        wl.move_to([LEFT_X, 0.75, 0])
        assert wl.get_left()[0] > -6.6 and wl.get_right()[0] < g.con_cards[0].get_left()[0] - 0.05, wl.get_right()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(mini), Indicate(g.con_cards[1].body, color=ERR, scale_factor=1.08), run_time=0.6)
            self.play(FadeIn(wl, shift=RIGHT * 0.15), run_time=0.5)
            for i, (anchor, text) in enumerate((("the build logs", "build logs · Part 1"),
                                                ("the service logs", "service logs · Parts 1, 3"),
                                                ("and the job's logs and manifest", "job logs + manifest · Part 4"))):
                vo.wait_until(anchor)
                wl.fill(self, i, text, run_time=0.5)
            g.answer(self, 1, "3 places to look")

        # ========================================================== 7. vendor lock-in: what ran where
        def ran_here(text, t2c=None):
            lp = laptop(0.8, LAPTOP)
            t = label(text, 20, INK, t2c=t2c or {})
            return VGroup(lp, t).arrange(RIGHT, buff=0.25)

        ff = ran_here("functions-framework ran here", {"functions-framework": TOOL})
        im = ran_here("the image ran here", {"image": IMAGE})
        gg = VGroup(label("the Google-specific parts", 20, CLOUD),
                    VGroup(*[chip(s, CLOUD, size=20) for s in ("console", "IAM", "Cloud Build")]).arrange(
                        RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        lk = VGroup(ff, im, gg).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        lk.move_to([LEFT_X, 0.7, 0]).align_to(wl, LEFT)
        assert lk.get_right()[0] < g.con_cards[0].get_left()[0] - 0.05, lk.get_right()
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(wl), Indicate(g.con_cards[2].body, color=ERR, scale_factor=1.12), run_time=0.6)
            vo.wait_until("the image and the Functions Framework")
            self.play(FadeIn(im, shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(ff, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("only the console")
            self.play(FadeIn(gg[0]), FadeIn(gg[1][0], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the permissions and the build")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in gg[1][1:]], lag_ratio=0.4), run_time=0.6)
            g.answer(self, 2, "the image ran\non your laptop")

        # ========================================================== 8. slide 9: next lecture
        r9 = lref("9")
        yt9 = 1.0
        tline = Arrow([-6.4, yt9, 0], [6.45, yt9, 0], buff=0, color=S.GREY, stroke_width=3, tip_length=0.2)
        word = label("serverless", 24, S.GREY).move_to([0, yt9 + 0.45, 0])
        spans = ((-6.2, -2.15, PAST, True, "LAST WEEK", ("Vertex AI", "training job", "L13")),
                 (-1.85, 1.85, TURN, False, "TODAY", ("Cloud Run functions", "Cloud Run", "L14")),
                 (2.15, 6.2, PAST, True, "NEXT", ("L15 · Vertex AI endpoint", "for a trained model", "pipelines")))
        weeks = []
        for x0, x1, col, dsh, head, rws in spans:
            br = bracket(x0, x1, yt9 - 0.15, col, dsh)
            wc = week_card(head, rws, col, dsh, (x0 + x1) / 2, yt9 - 1.75)
            weeks.append(VGroup(br, wc))
        for w in weeks[:2]:
            dim(w)
        nxt = weeks[2]
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(g, lk), scale=0.3), FadeOut(r16), FadeIn(r9), run_time=0.7)
            self.remove(g)
            self.play(GrowArrow(tline), FadeIn(word, shift=DOWN * 0.1), FadeIn(weeks[0]), FadeIn(weeks[1]),
                      run_time=0.6)
            vo.wait_until("a Vertex AI endpoint")
            self.play(Create(nxt[0]), FadeIn(nxt[1], shift=DOWN * 0.15), run_time=0.7)
            self.play(nxt[1].head.animate.set_color(INK), nxt[1].body.animate.set_color(INK), run_time=0.4)
            vo.wait_until("then pipelines")
            self.play(Indicate(nxt[1].body[2], color=INK, scale_factor=1.12), run_time=0.7)

        # ========================================================== 9-13. test yourself
        head = label("Test yourself", 30, TURN).move_to([-6.4, 2.75, 0], aligned_edge=LEFT)
        qcards = [question_card(q, 26, card_w=8.4).move_to([-2.2, 0.15, 0]) for q in QUESTIONS]
        counters = [label(f"question {k + 1} of 5 · answers in exercises.md", 22, S.GREY) for k in range(5)]
        for c in counters:
            c.next_to(head, RIGHT, buff=0.4).align_to(head, DOWN)
        IX, IY = 4.45, 0.15
        icons = []
        gi = grid_icon(0.95).move_to([IX, IY, 0])
        icons.append(gi)
        mi = meter_icon(1.9).move_to([IX, IY, 0])
        icons.append(mi)
        di = doors_icon().move_to([IX, IY, 0])
        icons.append(di)
        cr = chip_row(ARGS_SHORT, max_w=4.0)
        cr.rows.move_to([IX, IY, 0])
        cr.rows.shift(LEFT * max(0.0, cr.rows.get_right()[0] - 6.45))
        icons.append(cr)
        cc = VGroup(*[card([s.replace("\n", " ")], ERR, size=20) for s in CONS]).arrange(DOWN, buff=0.18)
        cc.move_to([IX, IY, 0])
        icons.append(cc)
        for ic in icons:
            (ic.rows if ic is cr else ic).shift(LEFT * max(0.0, ic.get_right()[0] - 6.45))
        for q, ic in zip(qcards, icons):
            assert q.get_right()[0] < ic.get_left()[0] - 0.2 and ic.get_right()[0] < 6.55, (q.get_right(), ic.get_corner(DR))
        ans = grey_chip("answers: exercises.md").next_to(qcards[4], DOWN, buff=0.35)
        assert ans.get_bottom()[1] > -3.5
        anchors = ("One:", "Two:", "Three:", "Four:", "Five:")
        cur_q = cur_i = None
        for k in range(5):
            with self.voiceover(SAY[9 + k]) as vo:
                if k == 0:
                    self.play(FadeOut(VGroup(tline, word, *weeks)), FadeOut(r9), FadeIn(head, shift=DOWN * 0.1),
                              FadeIn(counters[0]), run_time=0.7)
                    vo.wait_until(anchors[0])
                    self.play(FadeIn(qcards[0], shift=UP * 0.15), FadeIn(gi), run_time=0.6)
                else:
                    self.play(FadeOut(cur_q, shift=LEFT * 0.4), FadeOut(cur_i), FadeOut(counters[k - 1]),
                              FadeIn(qcards[k], shift=LEFT * 0.4), FadeIn(icons[k]), FadeIn(counters[k]),
                              run_time=0.7)
                cur_q, cur_i = qcards[k], icons[k]
                if k == 0:
                    vo.wait_until("What do you hand over")
                    self.play(Indicate(gi, color=TURN, scale_factor=1.15), run_time=0.8)
                elif k == 1:
                    vo.wait_until("make the meter run")
                    self.play(mi.fill_bar.animate(rate_func=there_and_back).stretch(1.8, 0, about_edge=LEFT),
                              run_time=1.0)
                elif k == 2:
                    vo.wait_until("who may call it")
                    self.play(Indicate(di.left, color=TURN, scale_factor=1.25), run_time=0.7)
                    vo.wait_until("and who it runs as")
                    self.play(Indicate(di.right, color=TURN, scale_factor=1.25), run_time=0.7)
                elif k == 3:
                    vo.wait_until("eleven separate arguments")
                    self.play(each([c.text for c in cr.chips], TURN, scale=1.06, lag=0.08), run_time=1.2)
                else:
                    vo.wait_until("name the lecture's three downsides")
                    self.play(each([c.body for c in cc], ERR, scale=1.12, lag=0.4), run_time=1.4)
                    self.play(FadeIn(ans, shift=UP * 0.1), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)

    def cells_light(self, g):
        """ANIM: the container·serverless cell's frame flashes (the one image of Parts 2–4)."""
        fr = g.cells[1][1].frame
        return fr.animate(rate_func=there_and_back).set_stroke(INK, 5)
