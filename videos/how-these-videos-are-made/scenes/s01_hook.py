"""S01 · Made by something that can't watch it (the reference scene of this video).

Beats: a paused frame of an early tic-tac-toe draft, re-rendered from the old code (A03): the
formula line reads "4 × 3 × 2" and then a GREEN 12 -> ponder: what went wrong? -> the 12 was a
running count: it glides down under the board, counting on, and the frame cross-fades to the
real fixed frame (A01's moment, 23.0 s, from the final render) -> RED tag "the math was right /
the layout was wrong" -> the reviewer who caught it: a faded-BLUE icon that turns out to be an AI
(A10, qa_round1.txt line 30) -> the team row (user, agent, sub-agents), the three things they
made, and the motif of the whole video: headphones and play button struck through in RED ->
the five chapters of this video, each formed from what was just on screen.

Idioms for the other scenes: colours and helpers from common.py only; real images through
Player.show()/exhibit() with their tag and caption; anchors on sentence starts; the ponder card
comes in on "Pause" (ponder_in) and drains after the block (ponder_drain); text is never scaled
below 20 pt (shrink the pictures, fade or rebuild the text); what became what is a Transform.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AGENT, BUG, EXCERPTS, MEASURED, NARRATION, OPEN, SUB_AGENT_TEXT, TOOL, USER, bug_tag,
                    cant_hear_or_play, caption, chip, dim, emphasize, fade_out_all, gather, gloss, label,
                    play_button, ponder_drain, ponder_in, pulse, rerender_tag, role_icon, speech_bubble,
                    split_chip, sub_agent_cluster, tag, undim, video_player, zh)

SAY = NARRATION["S01"]

# The two frames share one layout (same scene, same code path for the board), cropped alike to
# the picture's content: old = re-render of 8a922bf at 720p (A03), new = final 1080p render (A01's
# 23.0 s moment, full resolution instead of the 480 px contact-sheet tile).
OLD, OLD_CROP = "old_s03_tally_12.png", (0, 32, 1152, 684)           # 1280 x 720
NEW, NEW_CROP = "ttt_s03_frame_23.0.png", (0, 48, 1728, 1026)       # 1920 x 1080
OLD_12 = (1000, 326, 1043, 359)        # the GREEN "12" on the formula line (old px)
OLD_FORMULA = (630, 326, 831, 361)     # "4 × 3 × 2" (old px)
NEW_19 = (610, 960, 645, 991)          # "19" of "ghost endings counted: 19" (new px)
NEW_TALLY = (99, 930, 645, 1001)       # the whole tally line (new px)
PATCH = "#0D0E13"                      # the frames' background colour (sampled)

SCREEN_W = 8.6
PLAYER_Y = 0.35
ASIDE = RIGHT * 1.75                   # where the player moves when the reviewer comes in

DRAFT_CAPTION = "from a draft of 'Why are there exactly 255,168 games of tic-tac-toe?' · made for ages 11 to 14"
FINAL_CAPTION = "real frame · tic-tac-toe video, scene 3 (final render)"


def tag_on_top(t, frame):
    """A tag straddling the top edge of a frame, at its right end."""
    return t.move_to(frame.get_corner(UR) + np.array([-t.width / 2 - 0.2, 0, 0]))


class Hook(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- a paused frame of a draft
        player = video_player(SCREEN_W, aspect=OLD_CROP[2] / (OLD_CROP[3] - OLD_CROP[1]), progress=0.03)
        player.move_to(UP * PLAYER_Y)
        old = player.show(OLD, crop=OLD_CROP)
        rtag = tag_on_top(rerender_tag(), player.screen)
        cap = caption(DRAFT_CAPTION, 22).next_to(player, DOWN, buff=0.22)
        play = play_button(0.3, TOOL).move_to(player.pause)
        play[0].set_stroke(width=0)                          # paused: just the triangle

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(player.frame), FadeIn(old), run_time=0.9)
            self.play(FadeIn(VGroup(player.pause, player.bar, player.done, player.knob)), run_time=0.4)
            self.play(player.knob.animate.move_to(player.at(0.31)),
                      player.done.animate.put_start_and_end_on(player.bar.get_start(), player.at(0.31)),
                      run_time=1.2, rate_func=smooth)
            vo.wait_until("a paused frame")
            self.play(ReplacementTransform(player.pause, play), FadeIn(rtag, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("about tic-tac-toe")
            self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("Look at the line")
            line_box = old.px_box(OLD_FORMULA[0], OLD_FORMULA[1], OLD_12[2], OLD_12[3])
            self.play(emphasize(line_box, run_time=1.1))
            vo.wait_until("4 times 3")
            self.play(emphasize(old.px_box(*OLD_FORMULA), run_time=1.0))
            vo.wait_until("and then 12")
            self.play(emphasize(old.px_box(*OLD_12), run_time=0.9))

        # ---------------------------------------------------------- ponder
        shown = (player.frame, old, play, player.bar, player.done, player.knob, rtag, cap)
        with self.voiceover(SAY[1]) as vo:
            self.play(*dim(*shown, opacity=0.4), run_time=0.5)
            vo.wait_until("Pause")
            card = ponder_in(self, "If you were 12,\nwhat would you think went wrong?")
        ponder_drain(self, card, 6)

        # ---------------------------------------------------------- it was a running count
        new = player.show(NEW, crop=NEW_CROP)
        a, b = old.px(*OLD_12[:2]), old.px(*OLD_12[2:])
        twelve_h = abs(a[1] - b[1])
        start = (a + b) / 2
        c, d = new.px(*NEW_19[:2]), new.px(*NEW_19[2:])
        end = (c + d) / 2
        patch = Rectangle(width=abs(b[0] - a[0]) + 0.12, height=twelve_h + 0.12, stroke_width=0) \
            .set_fill(PATCH, 1).move_to(start)
        count = ValueTracker(0.0)

        def running_count():                                 # 12 -> 19 while it glides down
            t = count.get_value()
            n = DecimalNumber(12 + round(7 * t), num_decimal_places=0, color=MEASURED)
            n.scale_to_fit_height(twelve_h)
            p = start + (end - start) * t + np.array([0, 0.9 * np.sin(PI * t), 0]) * 0.3
            return n.move_to(p)

        ftag = tag_on_top(tag("real frame, after the fix", TOOL), player.screen)
        fcap = caption(FINAL_CAPTION, 22).next_to(player, DOWN, buff=0.22)
        spot = new.px_box(*[v * 1.5 for v in OLD_12])          # where the 12 sat, in the new frame
        old_spot = RoundedRectangle(width=spot.width + 0.2, height=spot.height + 0.16, corner_radius=0.06,
                                    stroke_color=BUG, stroke_width=3).move_to(spot)
        red = bug_tag("the math was right\nthe layout was wrong")
        red.move_to(new.px(1440, 690)).align_to(player.screen, RIGHT).shift(LEFT * 0.12)
        red_arrow = Arrow(red.get_top() + RIGHT * (old_spot.get_x() - red.get_x()), old_spot.get_bottom(),
                          buff=0.05, color=BUG, stroke_width=4, tip_length=0.16, max_tip_length_to_length_ratio=0.4)
        tally = new.px_box(*NEW_TALLY)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(card), *undim(*shown), run_time=0.6)
            self.play(emphasize(old.px_box(OLD_FORMULA[0], OLD_FORMULA[1], OLD_12[2], OLD_12[3]), run_time=1.2))
            vo.wait_until("The 12 was")
            moving = always_redraw(running_count)
            self.add(patch, moving)
            self.play(count.animate.set_value(1.0), run_time=2.0, rate_func=smooth)
            moving.clear_updaters()
            self.play(FadeIn(new), FadeOut(old), FadeOut(patch), FadeOut(moving),
                      FadeTransform(rtag, ftag), FadeTransform(cap, fcap), run_time=1.1)
            g = gloss("a running count,\nnow under the board", tally, RIGHT, length=0.6)
            g.text.shift(UP * 0.14)
            self.play(GrowArrow(g.arrow), FadeIn(g.text, shift=LEFT * 0.1), run_time=0.8)
            vo.wait_until("The layout lied")
            self.play(Create(old_spot), run_time=0.4)
            self.play(FadeIn(red, scale=0.9), GrowArrow(red_arrow), run_time=0.6)

            # the reviewer who caught it
            vo.wait_until("And the reviewer")
            frame_parts = gather(self, player.frame, new, play, player.bar, player.done, player.knob, ftag, g,
                                 old_spot, red, red_arrow)
            self.play(frame_parts.animate.shift(ASIDE), FadeOut(fcap), run_time=0.9)
            reviewer = role_icon("sub", 1.25)
            badge = reviewer.badge
            reviewer.remove(badge)
            reviewer.move_to([-4.75, -0.55, 0])
            badge.move_to(reviewer.person.get_corner(DR) + np.array([0.02, 0.12, 0]))
            bubble = speech_bubble(EXCERPTS["A10"]["s01_bubble"].replace(" read ", " read\n", 1)
                                   .replace(" … ", " …\n", 1).replace("look like ", "look like\n", 1),
                                   chars=40, tail=DOWN, tail_shift=-0.12)
            bubble.next_to(reviewer, UP, buff=0.12).set_x(-4.3)
            bubble.shift(RIGHT * (reviewer.person.get_x() + 0.1 - bubble.tail.get_vertices()[2][0]))
            self.play(FadeIn(reviewer, shift=RIGHT * 0.4), run_time=0.6)
            self.play(FadeIn(bubble, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("It was an AI")
            who = label("a simulated 12-year-old\n(an AI reviewer)", 24, SUB_AGENT_TEXT).next_to(reviewer, DOWN, buff=0.25)
            self.play(FadeIn(badge, scale=1.6), run_time=0.5)
            self.play(FadeIn(who, shift=UP * 0.1), Indicate(badge, color=S.WHITE, scale_factor=1.25), run_time=0.9)

        # ---------------------------------------------------------- the strange part: who made it
        user = role_icon("user", 1.25).move_to([-3.4, 0.25, 0])
        agent = role_icon("agent", 1.25).move_to([0.25, 0.25, 0])
        subs = sub_agent_cluster(7, 0.42, cols=4).move_to([3.95, 0.25, 0])
        user_l = label("the user", 26, USER).next_to(user, DOWN, buff=0.25)
        agent_l = label("the agent: Claude Code", 26, AGENT).next_to(agent, DOWN, buff=0.25)
        subs_l = label("sub-agents", 26, SUB_AGENT_TEXT).next_to(subs, DOWN, buff=0.25).match_y(agent_l)
        made = VGroup(chip("script"), chip("animation code"), chip("checks")).arrange(RIGHT, buff=0.3)
        made.move_to([2.1, -2.35, 0])        # low: clear of the chapter slots that come next
        glyphs = cant_hear_or_play(0.72, gap=0.6).move_to([2.95, 1.85, 0])   # clear of the title that comes next
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(ftag, g, old_spot, red, red_arrow, bubble, who, badge, reviewer)), run_time=0.5)
            thumb = gather(self, player.frame, new, play, player.bar, player.done, player.knob)
            self.play(thumb.animate.scale(0.27).move_to([-5.15, 2.75, 0]), run_time=0.9)
            self.play(FadeIn(user, shift=UP * 0.2), FadeIn(user_l), run_time=0.6)
            vo.wait_until("made by AI agents")
            self.play(FadeIn(agent, shift=UP * 0.2), FadeIn(agent_l),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in subs.icons], lag_ratio=0.08),
                      FadeIn(subs.badge), FadeIn(subs_l), run_time=1.0)
            for k, phrase in enumerate(("the script", "the animation code", "and the checks")):
                vo.wait_until(phrase)
                src = agent if k != 1 else subs
                self.play(FadeIn(made[k], target_position=src.get_center(), scale=0.4), run_time=0.6)
            vo.wait_until("And none of them")
            self.play(FadeOut(thumb), FadeIn(glyphs[0][0], shift=DOWN * 0.15), run_time=0.6)
            self.remove(thumb)
            self.play(Create(glyphs[0][1]), run_time=0.4)
            vo.wait_until("or press play")
            self.play(FadeIn(glyphs[1][0], shift=DOWN * 0.15), run_time=0.5)
            self.play(Create(glyphs[1][1]), run_time=0.4)
            vo.wait_until("So how do they know")
            self.play(LaggedStart(*[emphasize(m, run_time=0.7) for m in made], lag_ratio=0.3), run_time=1.4)

        # ---------------------------------------------------------- what this video covers
        title = label("How these videos are made", 48).move_to(UP * 2.95)
        ys = [1.75, 0.8, -0.15, -1.1, -2.05]
        chapters = [
            chip("the pipeline", TOOL, size=30),
            split_chip("who did what", USER, AGENT, size=30),
            chip("how it's checked", MEASURED, size=30),
            chip("the Chinese versions", TOOL, size=30, icon=zh("中", 28)),
            chip("what still needs a human", OPEN, size=30, dashed=True),
        ]
        for ch, y in zip(chapters, ys):
            ch.move_to([0, y, 0])
        sources = [(made[0], made[1]), (user, agent, subs), (made[2],), None, None]
        anchors = ["the pipeline", "who did what", "how work gets", "the Chinese versions", "what still needs"]

        with self.voiceover(SAY[4]) as vo:
            sources[4] = gather(self, glyphs[0][0], glyphs[0][1], glyphs[1][0], glyphs[1][1])
            self.play(Write(title), FadeOut(VGroup(user_l, agent_l, subs_l)), run_time=0.9)
            for ch, src, phrase in zip(chapters, sources, anchors):
                vo.wait_until(phrase)
                if isinstance(src, tuple):
                    src = gather(self, *src)
                if src is None:
                    self.play(FadeIn(ch, shift=UP * 0.2), run_time=0.6)
                else:
                    # the struck glyphs arc round the right of the column on their way to the last slot
                    self.play(ReplacementTransform(src, ch, path_arc=-PI / 2 if ch is chapters[4] else 0),
                              run_time=0.8 if ch is chapters[4] else 0.7)
                self.play(pulse(ch, 1.08, run_time=0.45))
        self.wait(0.6)
        fade_out_all(self)
