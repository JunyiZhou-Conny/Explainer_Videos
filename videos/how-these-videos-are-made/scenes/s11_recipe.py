"""S11 · A recipe, and a request (the last scene).

Beats: a GREY recipe card writes itself, one line per spoken sentence, each line in its semantic
colour with a small glyph of the same colour in front of it (PINK person, GREY script page, ORANGE
clock whose hand sweeps round, two faded-BLUE reviewers, a GREEN check that gets a second check on
"check the fixes", a GREY chain of files) -> "above all, the goal": the card folds away, its heading
"A recipe" becomes "the goal" and its PINK person grows into the user, from whom the PINK quote card
of S02 comes back (A06, quotes.yaml `s11_goal`, exact, with the dictated caption); "cognitive
offloading" turns RED as in S02, and the two halves of the goal get a WHITE Circumscribe as they are
spoken -> the request: the tic-tac-toe playground (A34, real screenshot, GREY frame) on the left; on
the right the BLUE agent under S01's GREY headphones, struck through in RED, "this video was made
the same way", and under it a dashed YELLOW outline "checked by measuring · the agent that made it
can't listen to it" with the tag "not yet verified" -> on "You can." the headphones (without the
strike) lift off the motif onto a PINK person, "you"; under it a GREY chip "something sounded wrong?
say so, with the time", whose clock hand sweeps on "with the time"; a PINK arrow, "feedback", runs
from the chip up to the open outline (the outline stays dashed: nothing has been heard yet) ->
everything fades out (the end of the video).

Helpers defined here (not in common.py): broken() and marked_glyphs() (as s02's broken() and
quote_glyphs(): line breaks in a quote without touching its words, and the glyphs of a phrase in
a Text, matched through a t2c twin so ligatures can't shift the count), around(), recipe_glyph(),
worn_headphones().
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.scene import VoiceScene

from common import (AUDIO, BUG, DICTATED, INK, MEASURED, NARRATION, PANEL, QUOTES, SUB_AGENT,
                    SUB_AGENT_TEXT, TITLES, TOOL, USER, box, cant_hear_or_play, caption, check_mark, chip,
                    clock, exhibit, fade_out_all, file_icon, gather, label, open_outline,
                    open_tag, pulse, quote_card, role_icon)

SAY = NARRATION["S11"]

# ------------------------------------------------------------------ the recipe (script.md S11, SHOW 1)
RECIPE = [
    ("1 · a human picks the learner and the question", USER),
    ("2 · script first, as code", TOOL),
    ("3 · let the audio be the clock", AUDIO),
    ("4 · independent reviewers, including a simulated viewer", SUB_AGENT_TEXT),   # faded BLUE, readable
    ("5 · measure what you can't perceive, and check the fixes", MEASURED),
    ("6 · keep every step in a file", TOOL),
]
LINE_ANCHORS = ["A human picks", "Write the script", "Let the audio", "Use independent", "Measure what",
                "And keep every"]
RECIPE_SIZE = 28
SLOT_W = 1.05                      # the glyph column of the card

# ------------------------------------------------------------------ the goal (A06, exact)
GOAL = QUOTES["s11_goal"]["screen"]
QUOTE_SIZE = 28
MARK = "#FF00FE"                   # probe colour of marked_glyphs(), never drawn

# ------------------------------------------------------------------ the request (A34)
PLAYGROUND, PG_CROP = "ttt_playground.png", (96, 8, 1184, 742)    # 1280 x 800: title, board and counter
PG_CAPTION = "real screenshot · the tic-tac-toe playground\na small web page to try the idea yourself"
MADE = "this video was made the same way"
OPEN_LINES = ("checked by measuring", "the agent that made it", "can't listen to it")
ASK = "something sounded wrong?\nsay so, with the time"


# ------------------------------------------------------------------ helpers (this scene only)
def broken(text: str, *after: str) -> str:
    """`text` with a line break in place of the space after each given substring: the quoted
    words stay exactly as written (quote_card keeps explicit breaks)."""
    out = text
    for a in after:
        i = out.index(a) + len(a)
        assert out[i] == " ", (a, out[i:i + 6])
        out = out[:i] + "\n" + out[i + 1:]
    assert out.replace("\n", " ") == text
    return out


def marked_glyphs(t: Text, phrase: str, size: float, **kw) -> VGroup:
    """The glyphs of `phrase` inside Text t (built with label(..., size, **kw)). A twin is built
    with the phrase coloured by t2c and the coloured glyphs are matched by index. Empty if the
    phrase isn't there (a translated build)."""
    try:
        twin = label(t.original_text, size, INK, t2c={phrase: MARK}, **kw)
    except Exception:                                   # noqa: BLE001 (translated build)
        return VGroup()
    if len(twin.submobjects) != len(t.submobjects):
        return VGroup()
    mark = ManimColor(MARK).to_rgb()
    idx = [i for i, g in enumerate(twin.submobjects) if np.allclose(g.get_fill_color().to_rgb(), mark, atol=0.02)]
    return VGroup(*[t.submobjects[i] for i in idx])


def around(m, buff: float = 0.08) -> Rectangle:
    """An invisible rectangle over m (to Circumscribe a few glyphs)."""
    return Rectangle(width=m.width + 2 * buff, height=m.height + 2 * buff, stroke_width=0).move_to(m)


def recipe_glyph(k: int) -> VGroup:
    """The small glyph in front of recipe line k, in the line's colour."""
    if k == 0:                                          # a human
        return person_icon(USER, 0.5)
    if k == 1:                                          # the script, a file
        return file_icon(0.52, TOOL)
    if k == 2:                                          # the audio is the clock
        return clock(0.25, AUDIO, stroke=3)
    if k == 3:                                          # independent reviewers
        return VGroup(person_icon(SUB_AGENT, 0.44), person_icon(SUB_AGENT, 0.44)).arrange(RIGHT, buff=0.07)
    if k == 4:                                          # measure; a second check comes with "check the fixes"
        return VGroup(check_mark(0.34), check_mark(0.34)).arrange(RIGHT, buff=0.04)
    return VGroup(*[file_icon(0.36, TOOL) for _ in range(3)]).arrange(RIGHT, buff=0.08)   # every step, a file


def worn_headphones(person: VGroup, color: str = TOOL, stroke: float = 6) -> VGroup:
    """Headphones ON a person_icon's head: VGroup(band, VGroup(cup, cup)), the same structure as
    common.headphones(), so one turns smoothly into the other."""
    head = person[0]
    r = head.width / 2
    c = head.get_center()
    R = r * 1.3
    band = Arc(radius=R, start_angle=0, angle=PI, arc_center=c, stroke_color=color, stroke_width=stroke)
    cups = VGroup(*[RoundedRectangle(width=r * 0.55, height=r * 1.05, corner_radius=r * 0.22, stroke_width=0)
                    .set_fill(color, 1).move_to(c + np.array([sx * R, -r * 0.12, 0])) for sx in (-1, 1)])
    return VGroup(band, cups)


class Recipe(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- a recipe card writes itself
        lines = [label(s, RECIPE_SIZE, col) for s, col in RECIPE]
        glyphs = [recipe_glyph(k) for k in range(6)]
        slots = [Rectangle(width=SLOT_W, height=0.56, stroke_width=0).set_fill(opacity=0) for _ in range(6)]
        rows = VGroup(*[VGroup(sl, ln).arrange(RIGHT, buff=0.28) for sl, ln in zip(slots, lines)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(TITLES["Recipe"].split(",")[0], 40, INK)            # "A recipe"
        rule = Line(LEFT, RIGHT, color=TOOL, stroke_width=2)
        body = VGroup(head, rule, rows).arrange(DOWN, buff=0.3)
        rule.set_width(rows.width).align_to(rows, LEFT)
        head.align_to(rows, LEFT)
        card = box(body.width + 1.0, body.height + 0.8, TOOL, fill=PANEL, fill_opacity=0.9, radius=0.25)
        body.move_to(card)
        VGroup(card, body).move_to(ORIGIN)
        for g, sl in zip(glyphs, slots):
            g.move_to(sl)
        checks = glyphs[4]
        files = glyphs[5]
        clk = glyphs[2]

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(card, scale=0.96), run_time=0.6)
            self.play(Write(head), Create(rule), run_time=0.9)
            for k, phrase in enumerate(LINE_ANCHORS):
                vo.wait_until(phrase)
                if k == 4:                                  # one check now, the second one later
                    pop = Create(checks[0])
                elif k == 5:                                # a chain of files, one per step
                    pop = LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15) for f in files], lag_ratio=0.3)
                else:
                    pop = FadeIn(glyphs[k], scale=0.6)
                anims = [pop, Write(lines[k])]
                if k == 2:                                  # the clock's hand sweeps round once
                    anims.append(Rotate(clk.minute, -TAU, about_point=clk.face.get_center()))
                self.play(*anims, run_time=1.3 if k in (0, 3, 4) else 1.0)
                if k == 4:
                    vo.wait_until("and check the fixes")
                    self.play(Create(checks[1]), run_time=0.5)
                    self.play(Indicate(checks, color=S.WHITE, scale_factor=1.2), run_time=0.6)
            self.play(LaggedStart(*[pulse(g, 1.25, run_time=0.5) for g in glyphs], lag_ratio=0.15), run_time=1.0)

        # ---------------------------------------------------------- above all, the goal
        user = role_icon("user", 1.25).move_to([-5.45, 0.25, 0])
        user_l = label("the user", 26, USER).next_to(user, DOWN, buff=0.25)
        q = quote_card(broken(GOAL, "offloading;", "help us", "accessible,", "some sort of"), DICTATED,
                       size=QUOTE_SIZE, chars=80)
        q.move_to([0, 0.25, 0]).align_to([-4.35, 0, 0], LEFT)
        offload = marked_glyphs(q.quote, "cognitive offloading", QUOTE_SIZE, line_spacing=1.0)
        reach = marked_glyphs(q.quote, "make knowledge more accessible", QUOTE_SIZE, line_spacing=1.0)
        learn = marked_glyphs(q.quote, "the same level of learning", QUOTE_SIZE, line_spacing=1.0)
        goal_head = label("the goal", 40, INK).next_to(q.box, UP, buff=0.45).align_to(q.box, LEFT)

        with self.voiceover(SAY[1]) as vo:
            rest = gather(self, card, rule, *lines, *glyphs[1:])
            self.play(FadeOut(rest, scale=0.94), ReplacementTransform(glyphs[0], user.person),
                      ReplacementTransform(head, goal_head), run_time=1.0)
            self.add(user)
            self.play(FadeIn(user_l, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("As the user put it")
            self.play(FadeIn(VGroup(q.box, q.quote), target_position=user.get_center(), scale=0.3), run_time=0.9)
            self.play(FadeIn(q.caption, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("cognitive offloading")
            if len(offload):                                # as in S02: the words the goal argues against
                self.play(offload.animate.set_color(BUG), run_time=0.5)
                self.play(Indicate(offload, color=BUG, scale_factor=1.1), run_time=0.7)
            vo.wait_until("It should make")
            if len(reach):                                  # a whole phrase: the box is drawn in full, then fades
                self.play(Circumscribe(around(reach), color=S.WHITE, fade_out=True, buff=0.02), run_time=1.5)
            vo.wait_until("and still let you")
            if len(learn):
                self.play(Circumscribe(around(learn), color=S.WHITE, fade_out=True, buff=0.02), run_time=1.5)
            self.play(pulse(VGroup(user, user_l), 1.08, run_time=0.7))

        # ---------------------------------------------------------- the request: you can listen
        pg = exhibit(PLAYGROUND, width=5.0, crop=PG_CROP).move_to([-3.95, 0.4, 0])
        pg_cap = caption(PG_CAPTION, 20).next_to(pg, DOWN, buff=0.15).align_to(pg, LEFT)

        agent = role_icon("agent", 1.1).move_to([-0.45, 1.0, 0])
        motif = cant_hear_or_play(0.62)[0]                 # GREY headphones + RED strike
        motif.next_to(agent, UP, buff=0.3)
        hp, hp_x = motif
        made = label(MADE, 26, INK).move_to([0, 2.2, 0]).align_to([0.45, 0, 0], LEFT)
        o_lines = VGroup(label(OPEN_LINES[0], 24, MEASURED), *[label(s, 24, INK) for s in OPEN_LINES[1:]])
        o_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        o_lines.next_to(made, DOWN, buff=0.42).align_to(made, LEFT).shift(RIGHT * 0.16)
        o_box = open_outline(o_lines, buff=0.16)
        o_tag = open_tag().next_to(o_box, RIGHT, buff=0.15)

        you = role_icon("user", 1.1).move_to([-0.45, -1.75, 0])
        you_l = label("you", 26, USER).next_to(you, DOWN, buff=0.2)
        worn = worn_headphones(you.person)
        ask_clock = clock(0.2, TOOL, stroke=3)
        ask = chip(ASK, TOOL, 24, icon=ask_clock)
        ask.move_to([0, -1.75, 0]).align_to(o_box, LEFT)
        when = marked_glyphs(ask.text, "with the time", 24)
        fb_x = o_box.get_center()[0]
        feedback = Arrow([fb_x, ask.get_top()[1] + 0.06, 0], [fb_x, o_box.get_bottom()[1] - 0.06, 0], buff=0.04,
                         color=USER, stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.3)
        fb_l = label("feedback", 24, USER).next_to(feedback, RIGHT, buff=0.18)

        with self.voiceover(SAY[2]) as vo:
            goal = gather(self, user, user_l, goal_head, q)
            self.play(FadeOut(goal, shift=LEFT * 0.4), run_time=0.7)
            self.play(FadeIn(pg, shift=RIGHT * 0.3), FadeIn(pg_cap), run_time=0.8)
            vo.wait_until("This video was made")
            self.play(FadeIn(agent, shift=UP * 0.2), Write(made), run_time=1.0)
            vo.wait_until("so it has the same")
            self.play(FadeIn(hp, shift=DOWN * 0.15), run_time=0.5)
            self.play(Create(hp_x), run_time=0.4)
            vo.wait_until("the agent that made it")
            self.play(Create(o_box), FadeIn(o_lines, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(o_tag, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("You can")
            lifted = hp.copy()
            self.play(FadeIn(you, shift=UP * 0.2), FadeIn(you_l), Transform(lifted, worn, path_arc=-0.6),
                      run_time=1.0)
            self.play(Indicate(VGroup(you, lifted), color=S.WHITE, scale_factor=1.1), run_time=0.6)
            vo.wait_until("If anything sounded")
            self.play(FadeIn(ask, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("say so, with the time")
            self.play(Rotate(ask_clock.minute, -TAU, about_point=ask_clock.face.get_center()),
                      *([Indicate(when, color=S.WHITE, scale_factor=1.15)] if len(when) else []), run_time=1.1)
            vo.wait_until("That's exactly")
            self.play(GrowArrow(feedback), FadeIn(fb_l, shift=UP * 0.1), run_time=0.8)
            self.play(Indicate(o_box, color=S.WHITE, scale_factor=1.04), run_time=0.8)
        self.wait(1.0)
        fade_out_all(self, run_time=1.2)
