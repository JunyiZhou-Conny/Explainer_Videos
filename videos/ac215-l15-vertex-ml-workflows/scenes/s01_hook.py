"""S01 · Three numbers or four? (cold open of AC215 L15, the full follow-along). Lecture: 15 · 11.

Beats (script.md "## S01", one voiceover block each; no tracker until the sample in beat 5):
0. Black frame. Two full-width panels stacked. Top: RECORDED(expected/md-predict-readme.txt: 7-10),
   tag `recorded · README A:137–147` (brie-2, three numbers, `... 2`, `Label:    brie`). Bottom: a
   5-row `laptop` strip printing TERM(laptop/47: 23-26) (brie-1, four numbers, `... 2`, `Label:
   brie`), tag `extra · local stand-in, not SageMaker` on its title bar. Each panel's `Image:` row
   carries a small WHITE photo glyph + its file name (brie-2.jpg / brie-1.jpg) at the row's right;
   on "what cheese is in this photo" both glyphs Indicate (QA 00:00). A YELLOW mono chip above
   the top panel types `python cli.py --predict`. On "Both answers on screen" a GREY chip
   `cli.py · predict()` links both panels; on "And both answers say brie" both `brie`s glow GREEN.
1. The link chip goes; a GREY chip "two brie photos · count the numbers, not the values" holds the
   gap until the question card (QA 00:00: two files, one "this photo"). YELLOW rings count the numbers of each printed predictions list (the
   `[…] 2` row, one row in both panels) while a big YELLOW counter at the panel's right edge ticks
   1, 2, 3 (top) and 1, 2, 3, 4 (bottom); a RED "≠" pulses between the big 3 and 4. A YELLOW
   question card settles between the panels: "What is behind an endpoint?"
2. Panels and card slide away. V5 ThreeObjects preview: three empty slots, each on its phrase
   (GREEN artifact · which model, TEAL container · what runs it, BLUE machine · where it runs).
   On "and who pays" the GOLD meter under the machine starts and lecture_ref(15, "11") fades in
   with it; the empty PINK request lane comes in above the slots. On "while no request arrives" the
   lane flashes "0 requests" while the meter keeps sweeping. Block end: meter and lecture tag fade.
3. The lane goes; the slots slide up and dim (moved, never scaled: text stays >= 20 pt). V6
   ManualToPipeline (no people) below: four GREY stage tiles flicker in, PINK edges snap between
   them, a BLUE "pipeline" frame closes around all four.
4. Clear to a checklist of four GREY chips, one per phrase; a BLUE "first AWS lecture" badge on
   the first chip.
5. The chips fade. Sample YELLOW tracker (README A › Setup Environments · step 1 of 5: Clone repo)
   top-left with a GREY chip "eleven small trackers · two READMEs" under it; a 3-row laptop strip
   (GREY "preview" on its bar, home prompt) types laptop/10's `git clone …` (soft-wrapped) and a
   YELLOW `▶ your turn` row tag pulses beside it (QA 01:00: the first step a viewer can run now;
   `aws configure` needs the S03 keys). On "Every command" a GREY card "study guide: every command + real outputs". Everything
   fades; empty frame.
"""

import re

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources (checked)
TOP = recorded((7, 10))                          # the README's own --predict answer (3 classes)
assert TOP[0] == "Image: data/brie-2.jpg" and TOP[3].startswith("Label:") and "brie" in TOP[3], TOP
LOCAL = capture("laptop/47").at((23, 26))        # the local TF Serving stand-in (4 classes)
assert LOCAL[0] == "Image: data/brie-1.jpg" and LOCAL[3].startswith("Label:") and "brie" in LOCAL[3], LOCAL
NUM_RE = re.compile(r"\d\.\d+")
assert len(NUM_RE.findall(TOP[2])) == 3 and TOP[2].endswith("] 2"), TOP[2]
assert len(NUM_RE.findall(LOCAL[2])) == 4 and LOCAL[2].endswith("] 2"), LOCAL[2]
CLONE = capture("laptop/10")                     # the first step a viewer can run right now
assert CLONE.cmd == "git clone https://github.com/dlops-io/model-deployment-aws.git", CLONE.cmd
CHECKLIST = ("AWS account + billing", "AWS CLI v2", "Docker",
             "both clones: model-deployment-aws · ml-workflow-aws")
CHIP_CUES = ("you need an AWS account", "the AWS CLI", "Docker", "and both repositories")


def text_glyphs(t, sub: str, start: int = 0) -> VGroup:
    """Glyphs of `sub` in a one-line Text (its submobjects skip whitespace)."""
    s = t.text
    i = s.index(sub, start)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def number_glyphs(row, is_text: bool) -> list:
    """The glyph groups of each number in a printed predictions row."""
    out_ = []
    for m in NUM_RE.finditer(row.text):
        if is_text:
            out_.append(text_glyphs(row, m.group(0), m.start()))
        else:
            out_.append(glyph_range(row, m.start(), m.end()))
    return out_


def fixed_tracker(key: str, step: int) -> VGroup:
    """common.tracker() with its head put back above the dots: in common.py the head's
    arrange() re-centres it at y 0 (requested fix in the report)."""
    tr = tracker(key, step)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def photo_tag(name: str) -> VGroup:
    """A small photo glyph + its file name, one terminal row tall."""
    g = VGroup(file_glyph(0.32, INK), mono(name, 20, INK)).arrange(RIGHT, buff=0.14)
    return g


def big(n: int) -> Text:
    return label(str(n), 48, TURN)


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S01"] == 6, len(SAY)

        # ========================================================== 0. two answers, both brie
        top = recorded_card((7, 10), size=20, wrap=72, card_w=12.6)
        top.move_to([0, 3.0 - top.height / 2, 0])
        cmd = chip("python cli.py --predict", TURN, size=20, font=MONO)
        cmd.next_to(top.frame, UP, buff=0.12).align_to(top.frame, LEFT).shift(RIGHT * 0.2)
        t = term(P_MD, rows=5, size=20)
        stand = extra_row("local stand-in, not SageMaker")
        on_bar(t, stand)
        gap_y = (top.frame.get_bottom()[1] + t.box.get_top()[1]) / 2
        link = grey_chip("cli.py · predict()", mono_font=True).move_to([0, gap_y, 0])
        l_up = Line(link.get_top(), [0, top.frame.get_bottom()[1], 0], color=S.GREY, stroke_width=3)
        l_dn = Line(link.get_bottom(), [0, t.box.get_top()[1], 0], color=S.GREY, stroke_width=3)
        assert cmd.get_top()[1] <= 3.55, cmd.get_top()
        assert top.frame.get_bottom()[1] > t.box.get_top()[1] + 1.0, (top.frame.get_bottom(), t.box.get_top())

        X_PHOTO = 4.6                                          # right of each short Image: row
        ph_top = photo_tag("brie-2.jpg").move_to([X_PHOTO, top.rows[0].get_center()[1], 0])
        assert ph_top.get_left()[0] > top.rows[0].get_right()[0] + 0.5 and ph_top.get_right()[0] < top.frame.get_right()[0] - 0.2

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(top.frame), FadeIn(top.body), FadeIn(top.tag), FadeIn(ph_top, shift=LEFT * 0.2),
                      run_time=0.8)
            self.play(FadeIn(t), FadeIn(stand), run_time=0.6)
            rows = out(self, t, LOCAL, wrap=True, run_time=0.8)
            assert len(rows) == 5, [r.text for r in rows]
            ph_bot = photo_tag("brie-1.jpg").move_to([X_PHOTO, rows[0].strut.get_center()[1], 0])
            assert ph_bot.get_left()[0] > rows[0].get_right()[0] + 0.5 and ph_bot.get_right()[0] < t.box.get_right()[0] - 0.2
            self.play(FadeIn(ph_bot, shift=LEFT * 0.2), run_time=0.4)
            vo.wait_until("what cheese is in this photo")
            self.play(Indicate(ph_top, color=TURN, scale_factor=1.2),
                      Indicate(ph_bot, color=TURN, scale_factor=1.2), run_time=0.9)
            self.play(FadeIn(cmd.box), run_time=0.3)
            self.play(ShowIncreasingSubsets(cmd.text, rate_func=linear), run_time=0.9)
            vo.wait_until("Both answers on screen")
            self.play(FadeIn(link, scale=1.1), Create(l_up), Create(l_dn), run_time=0.7)
            vo.wait_until("from the same predict code")
            # the narrated object: one predict() behind both panels (no 4 s still before "brie")
            self.play(Indicate(link, color=S.GREY, scale_factor=1.15),
                      Indicate(cmd.text, color=TURN, scale_factor=1.06), run_time=0.9)
            self.play(l_up.animate(rate_func=there_and_back).set_stroke(width=6),
                      l_dn.animate(rate_func=there_and_back).set_stroke(width=6), run_time=0.8)
            vo.wait_until("And both answers say brie")
            brie_top = text_glyphs(top.rows[3], "brie")
            brie_bot = glyph_range(rows[4], rows[4].text.index("brie"), rows[4].text.index("brie") + 4)
            self.play(brie_top.animate.set_color(OWN), brie_bot.animate.set_color(OWN), run_time=0.4)
            self.add(top, t, stand, ph_top, ph_bot)            # re-seat both panels (split trap)
            self.play(Indicate(brie_top, color=OWN, scale_factor=1.25),
                      Indicate(brie_bot, color=OWN, scale_factor=1.25), run_time=0.9)
            self.add(top, t, stand, ph_top, ph_bot)            # the bar tag stays above the (opaque) box

        # ========================================================== 1. count: three or four?
        list_top, list_bot = top.rows[2], rows[3]
        nums_top = number_glyphs(list_top, True)
        nums_bot = number_glyphs(list_bot, False)
        X_BIG = 5.95
        y_top, y_bot = list_top.get_center()[1], list_bot.strut.get_center()[1]
        q = question_card("What is behind an endpoint?")
        q.move_to([-0.6, gap_y, 0])
        neq = label("≠", 48, ERR).move_to([X_BIG, gap_y, 0])
        # QA 00:00 (narration says "this photo", the panels show two files): the 3-vs-4 is the
        # model, not the photo. Holds the gap until the question card takes it.
        two = grey_chip("two brie photos · count the numbers, not the values").move_to([-0.6, gap_y, 0])
        assert two.get_left()[0] >= -6.5 and two.get_right()[0] < X_BIG - 0.6, (two.get_left(), two.get_right())

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(link), FadeOut(l_up), FadeOut(l_dn), run_time=0.5)
            self.play(FadeIn(two, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("The top answer")
            rings_top, cnt = [], None
            for k, g in enumerate(nums_top, 1):
                r = ring(g, TURN, buff=0.05, stroke=2.5)
                n = big(k).move_to([X_BIG, y_top, 0])
                rings_top.append(r)
                self.play(Create(r), FadeIn(n, scale=1.3) if cnt is None else Transform(cnt, n), run_time=0.45)
                cnt = cnt or n
            big3 = cnt
            vo.wait_until("The bottom one")
            rings_bot, cnt = [], None
            for k, g in enumerate(nums_bot, 1):
                r = ring(g, TURN, buff=0.05, stroke=2.5)
                n = big(k).move_to([X_BIG, y_bot, 0])
                rings_bot.append(r)
                self.play(Create(r), FadeIn(n, scale=1.3) if cnt is None else Transform(cnt, n), run_time=0.45)
                cnt = cnt or n
            big4 = cnt
            vo.wait_until("One model cannot give both")
            self.play(FadeIn(neq, scale=1.4), run_time=0.4)
            self.play(Indicate(neq, color=ERR, scale_factor=1.3), Indicate(big3, color=TURN),
                      Indicate(big4, color=TURN), run_time=0.9)
            vo.wait_until("So which model")
            self.play(FadeOut(two), run_time=0.3)
            self.play(FadeIn(q, shift=UP * 0.2), run_time=0.7)
            self.play(Indicate(q.body, color=TURN, scale_factor=1.06), run_time=0.8)

        # ========================================================== 2. three pieces behind an endpoint
        v = ThreeObjects(slots=False)
        lr = lref("11")
        hook_all = VGroup(top, t, stand, ph_top, ph_bot, cmd, *rings_top, *rings_bot, big3, big4, neq, q)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(hook_all, shift=LEFT * 1.5), run_time=0.8)
            vo.wait_until("an artifact")
            v.slots(self, 0)
            vo.wait_until("a container")
            v.slots(self, 1)
            vo.wait_until("and a machine")
            v.slots(self, 2)
            vo.wait_until("and who pays")
            v.meter(self, run_time=0.5)
            self.play(FadeIn(lr), v.dial.sweep(0.1), run_time=0.5)
            v.lane(self, run_time=0.6)
            v.run(self, 0.25, vo.until("The meter beside", minimum=0.5))
            v.run(self, 0.2, vo.until("while no request", minimum=0.5))
            zc = grey_chip("0 requests").move_to(v.lane_g[0].get_center())
            zc.box.set_fill(S.BG, 1)                           # opaque: the dashed lane must not strike it
            v.zero_chip = zc                                   # (ThreeObjects.zero's chip is see-through)
            v.show(self, zc, run_time=0.3)
            self.play(Indicate(zc.text, color=S.GREY), run_time=0.4)
            v.run(self, 0.35, max(1.6, vo.remaining()))      # "0 requests", the needle still moving
            v.dial.freeze()
            v.drop(self, v.dial, extra=[FadeOut(lr)], run_time=0.5)
            v.dial = None

        # ========================================================== 3. part 2: one pipeline
        w = ManualToPipeline(people=False)
        w.shift(DOWN * 2.35)                                   # tiles at y -1.35; slots move up
        w.links.set_opacity(0)                                 # the PINK chain grows from nothing
        with self.voiceover(SAY[3]) as vo:
            v.drop(self, v.lane_g, v.zero_chip, run_time=0.4)
            v.lane_g = v.zero_chip = None
            self.play(v.animate.shift(UP * 1.6).fade(0.5), run_time=0.8)
            vo.wait_until("The four stages")
            self.play(LaggedStart(*[FadeIn(tl, shift=UP * 0.15) for tl in w.tiles], lag_ratio=0.35), run_time=1.4)
            w.heal(self)
            self.play(LaggedStart(*[Indicate(tl.frame, color=S.GREY, scale_factor=1.04) for tl in w.tiles],
                                  lag_ratio=0.2), run_time=0.8)
            w.heal(self)
            vo.wait_until("become one pipeline")
            w.chain(self, run_time=0.7)
            w.frame(self, run_time=0.8)
            vo.wait_until("that the cloud runs")
            self.play(w.frame_g[0].frame.animate(rate_func=there_and_back).set_stroke(CLOUD, 6),
                      Indicate(w.frame_g[1], color=CLOUD, scale_factor=1.1), run_time=0.9)

        # ========================================================== 4. what you need
        chips = VGroup(*[grey_chip(s, size=24, mono_font=False) for s in CHECKLIST])
        chips.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-0.8, -0.1, 0])
        badge = chip("first AWS lecture", CLOUD, size=22).next_to(chips[0], RIGHT, buff=0.3)
        assert chips.get_left()[0] >= -6.5 and VGroup(chips, badge).get_right()[0] <= 6.5

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(v), FadeOut(w), run_time=0.7)
            for c, cue in zip(chips, CHIP_CUES):
                vo.wait_until(cue)
                self.play(FadeIn(c, shift=RIGHT * 0.3), run_time=0.5)
            vo.wait_until("This is our first lecture on AWS")
            self.play(FadeIn(badge, scale=1.2), run_time=0.5)
            self.play(Indicate(badge.text, color=CLOUD, scale_factor=1.1), run_time=0.8)

        # ========================================================== 5. how to read the video
        tr = fixed_tracker("A1", 1)
        eleven = grey_chip("eleven small trackers · two READMEs").next_to(tr, DOWN, buff=0.25).align_to(tr, LEFT)
        st = strip_term(P_HOME)                               # the clone runs before the folder exists
        prev = row_tag("preview")
        on_bar(st, prev)
        guide = card(["study guide: every command + real outputs"], size=24)
        guide.move_to([0, 0.35, 0])
        assert guide.get_top()[1] < eleven.get_bottom()[1] - 0.2 and guide.get_bottom()[1] > st.box.get_top()[1] + 0.2

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(chips), FadeOut(badge), run_time=0.6)
            self.play(FadeIn(tr, shift=DOWN * 0.2), run_time=0.6)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.06), FadeIn(eleven), run_time=0.8)
            vo.wait_until("and a yellow tag")
            self.play(FadeIn(st), FadeIn(prev), run_time=0.5)
            line = type_cmd(self, st, CLONE.cmd, type_time=0.9, soft=True)
            yt = beside(turn_row(), line)
            pin(self, line, yt)
            flash_tag(self, yt)
            vo.wait_until("Every command")
            self.play(FadeIn(guide, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(guide.body, color=S.GREY, scale_factor=1.05), run_time=0.8)
            self.wait(vo.remaining(0.3))
        self.play(FadeOut(tr), FadeOut(eleven), FadeOut(st), FadeOut(prev), FadeOut(guide), run_time=0.8)
        self.wait(0.3)
