"""S01 · Five containers, one bucket (cold open of AC215 L3).

Beats (script.md "## S01", one voiceover block each):
0. Black frame. V1 teaser (Relay, no labels; the dashed bonus drawer without its name): five
   TEAL boxes over six BLUE drawers. A white waveform token drops into drawer 1 ("on the left"),
   rises into box 1 and comes out as a short page into drawer 2; box 2 makes it a long page in
   drawer 3; there it splits: one copy through box 3 into drawer 4 as a wave, the other through
   box 4 into drawer 5 as an FR page, then through box 5 into drawer 6 as a wave. No arrow ever
   joins two boxes. The picture dims; YELLOW "How do they cooperate?" and "Who pays?" write in
   above it, one after the other.
1. The questions and the relay fade. A two-column card, headers "L2" (GREY) and "L3" (YELLOW);
   the four GREY L2 cells write in; on each phrase a copy of the left cell becomes its right
   cell behind a small GREY arrow: "a given Dockerfile" -> "you write the Dockerfile";
   "one image" -> "five images" (five small TEAL boxes); "no mount" -> "a bind mount into your
   laptop" (GREY folder, PINK route, TEAL box); "no key" -> "a shared bucket + a
   service-account key" (a BLUE drawer on "shared bucket", a GOLD key on "service account key").
2. Layout preview. A README.md page glyph and a GREY "this video" frame side by side; on "The
   tracker" the page flies to the top-left corner and becomes the ReadmeTracker ("README ›
   Clone this Repository", 2 dots, none lit) in a pulsing YELLOW ring; the code panel
   transcribe_audio/cli.py · lines 18–20 slides in, its header ringed YELLOW on "file and line
   numbers"; the 3-row laptop strip (GREY tag "preview") types `git clone
   https://github.com/dlops-io/mega-pipeline.git` (it folds onto two rows) + ▶ your turn, then
   `ls` + extra (no output: a preview).
3. The preview clears. Checklist card; each row writes in with a GREEN tick as it is said:
   "Tutorial 0: Docker Desktop + uv" (the tools PURPLE) · "the course key, from Canvas" (GOLD
   key glyph) · "your team's group name". Footer, two lines: "every command:" over
   "MLOps_Learning · guides/L03-containers-2-mega-pipeline.md" (guide path, then repo name pulse).
4. A TEAL container strip (container · transcribe_audio, prompt app@5b4d4981ec25:/app$, GREY tag
   "preview") types `python cli.py --download`. GREY caption "recorded without the course key";
   a dashed BLUE cloud draws itself; the typed command pulses on "you'll see the command"; the
   GREY card "with your key, look for" slides in in front of the cloud, two placeholder bars
   writing in; on "not its output" a dashed empty box draws itself where the output would print.
5. The picture fades; the strip leaves the container (GREY frame, title laptop, prompt
   student@laptop:~$). A GREY laptop glyph captioned "Debian 12 · Python 3.11.2"
   (laptop/00-laptop.txt lines 2, 6); `docker version` + extra -> 01-docker-version.txt lines
   2–3; `29.8.2` pulses, GREY tag "at the time of recording" beside it. Two GREY chips "macOS:
   zsh, %" and "Windows: Git BASH", then a PURPLE "Docker Desktop" chip under them; the prompt
   pulses on "the prompt differs", the typed command on "the commands are the same". Fade out
   to an empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import box, check_mark, chip, cloud, folder_glyph, glyph_range, label, laptop, mono, \
    substring
from explainer.scene import VoiceScene

from common import (CLOUD, COST, CTR, INK, LAPTOP, LOOKUP, NARRATION, P_HOME, TOOL, TURN, VENV, Relay,
                    beside, capture, extra_tag, key_glyph, leave_container, pin, preview_tag, recorded_tag,
                    src_panel, term, tracker, your_turn)

SAY = NARRATION["S01"]

CLONE = capture("03-clone")
assert CLONE.cmd == "git clone https://github.com/dlops-io/mega-pipeline.git", CLONE.cmd
DV = capture("01-docker-version")
assert DV.cmd == "docker version", DV.cmd
assert DV.line(3).split()[-1] == "29.8.2", DV.line(3)
LAP = capture("00-laptop")                      # head -4 /etc/os-release; python3 --version; ...
assert "Debian GNU/Linux 12" in LAP.line(2) and LAP.line(6) == "Python 3.11.2"
MACHINE = f"Debian 12 · {LAP.line(6)}"
DOWNLOAD = "python cli.py --download"           # the Quick Reference's long form (BRIEF.md)
GUIDE = "MLOps_Learning · guides/L03-containers-2-mega-pipeline.md"

# the L2 -> L3 card (script.md S01, block 1)
L2 = ["a given Dockerfile", "one image", "no mount", "no key"]
L3 = ["you write the Dockerfile", "five images", "a bind mount into your laptop",
      "a shared bucket + a service-account key"]
CHECKS = [("Tutorial 0: Docker Desktop + uv", {"Docker Desktop": TOOL, "uv": TOOL}),
          ("the course key, from Canvas", {}),
          ("your team's group name", {})]

_FLAT = set("acdehiklmnorstuvwxzABCDEFHIKLMNORSTUVWXZ0123456789")   # glyphs sitting on the baseline


# ------------------------------------------------------------------ small pictures
def on_baseline(t: Text, s: str, y: float) -> Text:
    """Shift Text t (built from string s) so that its baseline sits at y (rows with and without
    descenders then line up)."""
    chars = [c for c in s if not c.isspace()]
    for i, c in enumerate(chars):
        if c in _FLAT:
            t.shift(UP * (y - t[i].get_bottom()[1]))
            break
    return t


def text_span(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of substring `sub` of a Text built from string `s` (spaces have no glyphs)."""
    i = s.index(sub)
    a, n = len("".join(s[:i].split())), len("".join(sub.split()))
    return VGroup(*t[a:a + n])


def clear_stage(scene, *anims, run_time: float = 0.6):
    """Fade out everything on screen (together with `anims`), then drop it from the scene."""
    old = list(scene.mobjects)
    if old:
        scene.play(FadeOut(Group(*old)), *anims, run_time=run_time)
        scene.remove(*old)
    elif anims:
        scene.play(*anims, run_time=run_time)


def this_video(w: float = 4.4, h: float = 2.5) -> VGroup:
    """'this video': a GREY player frame with a play triangle and a progress bar, captioned."""
    frame = box(w, h, S.GREY, fill_opacity=0.05)
    play = Triangle(stroke_width=0).set_fill(S.GREY, 0.9).rotate(-PI / 2).scale(0.28).move_to(frame)
    bar = Line(frame.get_corner(DL) + np.array([0.3, 0.3, 0]), frame.get_corner(DR) + np.array([-0.3, 0.3, 0]),
               color=S.GREY_DARK, stroke_width=4)
    done = Line(bar.get_start(), bar.point_from_proportion(0.04), color=S.GREY, stroke_width=4)
    cap = label("this video", 26, S.GREY).next_to(frame, DOWN, buff=0.2)
    return VGroup(frame, play, bar, done, cap)


def readme_page(w: float = 3.0, h: float = 3.3) -> VGroup:
    """The README as a page glyph (never a screenshot): its file name, the repo, a few bars."""
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=S.GREY,
                             stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    name = mono("README.md", 24, INK).move_to(frame.get_top() + DOWN * 0.42)
    repo = mono("mega-pipeline", 20, S.GREY).next_to(name, DOWN, buff=0.12)
    lines = VGroup(*[Line(LEFT * f * (w - 0.7) / 2, RIGHT * f * (w - 0.7) / 2, color=S.GREY_DARK,
                          stroke_width=6) for f in (1, 0.8, 0.95, 0.6, 1, 0.7)])
    lines.arrange(DOWN, buff=0.24, aligned_edge=LEFT)
    lines.next_to(repo, DOWN, buff=0.3).align_to(frame, LEFT).shift(RIGHT * 0.35)
    return VGroup(frame, name, repo, lines)


def mini_boxes(n: int = 5) -> VGroup:
    """n small TEAL boxes (images / containers)."""
    return VGroup(*[RoundedRectangle(width=0.34, height=0.3, corner_radius=0.06, stroke_color=CTR,
                                     stroke_width=2.5).set_fill(CTR, 0.15) for _ in range(n)]) \
        .arrange(RIGHT, buff=0.09)


def mini_route() -> VGroup:
    """A laptop folder (GREY), the PINK -v route, a container (TEAL). .route"""
    fold = folder_glyph(0.28, LAPTOP)
    route = Line(LEFT * 0.45, RIGHT * 0.45, color=LOOKUP, stroke_width=4)
    ends = VGroup(Dot(route.get_start(), radius=0.05, color=LOOKUP), Dot(route.get_end(), radius=0.05, color=LOOKUP))
    ctr = RoundedRectangle(width=0.42, height=0.34, corner_radius=0.06, stroke_color=CTR,
                           stroke_width=2.5).set_fill(CTR, 0.15)
    g = VGroup(fold, VGroup(route, ends), ctr).arrange(RIGHT, buff=0.06)
    g.fold, g.route, g.ctr = fold, g[1], ctr
    return g


def mini_drawer() -> VGroup:
    """One BLUE bucket drawer with its handle."""
    fr = RoundedRectangle(width=0.62, height=0.42, corner_radius=0.06, stroke_color=CLOUD,
                          stroke_width=2.5).set_fill(CLOUD, 0.15)
    handle = RoundedRectangle(width=0.22, height=0.05, corner_radius=0.025, stroke_width=0) \
        .set_fill(CLOUD, 0.9).move_to(fr.get_top() + DOWN * 0.1)
    return VGroup(fr, handle)


def look_for_card(w: float = 5.0) -> VGroup:
    """The GREY "with your key, look for" card with two placeholder bars (S01 shows the form,
    not items). .frame .title .bars"""
    title = label("with your key, look for", 22, S.GREY)
    fr = box(w, 1.75, S.GREY, fill=S.BG, fill_opacity=0.94, radius=0.12)
    title.move_to(fr.get_corner(UL) + np.array([0.28, -0.32, 0]), aligned_edge=LEFT)
    bars = VGroup()
    for i, f in enumerate((0.72, 0.52)):
        y = fr.get_top()[1] - 0.86 - i * 0.44
        x0 = fr.get_left()[0] + 0.3
        bars.add(Line([x0, y, 0], [x0 + f * (w - 0.6), y, 0], color=S.GREY, stroke_width=9,
                      stroke_opacity=0.55))
    g = VGroup(fr, title, bars)
    g.frame, g.title, g.bars = fr, title, bars
    return g


# ------------------------------------------------------------------ the scene
class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)

        # ========================================================== 0. the relay teaser
        relay = Relay(labels=False).move_to(DOWN * 0.3)
        relay.bonus.text.set_opacity(0)         # the dashed seventh drawer: no name yet
        tok = relay.token_at(0, "wave")
        qs = VGroup(label("How do they cooperate?", 40, TURN), label("Who pays?", 40, TURN))
        qs.arrange(RIGHT, buff=1.3).move_to([0, 2.95, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(relay, lag_ratio=0.08), run_time=1.3)
            self.play(FadeIn(tok, shift=DOWN * 0.5),
                      Indicate(relay.drawers[0].frame, color=CLOUD, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Five programs")
            [tok] = relay.run(self, [(tok, 0)], run_time=1.9)
            [tok] = relay.run(self, [(tok, 1)], run_time=1.9)
            vo.wait_until("in English")
            tc, td = relay.run(self, [(tok, 2), (tok.copy(), 3)], run_time=2.2)
            [te] = relay.run(self, [(td, 4)], run_time=1.9)
            vo.wait_until("So how do they")
            self.play(relay.dim_to(0.3), tc.animate.set_opacity(0.3), te.animate.set_opacity(0.3),
                      Write(qs[0]), run_time=0.9)
            vo.wait_until("and who pays")
            self.play(Write(qs[1]), run_time=0.7)

        # ========================================================== 1. what changes since L2
        x_l, x_r, y_head = -6.1, -2.05, 1.88
        ys = [0.98, 0.02, -0.94, -1.9]
        frame = box(12.9, 5.15, S.GREY, fill_opacity=0.03).move_to([0, -0.22, 0])
        h2 = label("L2", 32, S.GREY, weight=BOLD)
        h3 = label("L3", 32, TURN, weight=BOLD)
        on_baseline(h2.move_to([x_l, 0, 0], aligned_edge=LEFT), "L2", y_head - 0.13)
        on_baseline(h3.move_to([x_r, 0, 0], aligned_edge=LEFT), "L3", y_head - 0.13)
        rule = Line([-6.2, 1.45, 0], [6.2, 1.45, 0], color=S.GREY_DARK, stroke_width=2)
        lefts = [on_baseline(label(s, 26, S.GREY).move_to([x_l, 0, 0], aligned_edge=LEFT), s, y - 0.1)
                 for s, y in zip(L2, ys)]
        rights = [on_baseline(label(s, 26, INK).move_to([x_r, 0, 0], aligned_edge=LEFT), s, y - 0.1)
                  for s, y in zip(L3, ys)]
        arrows = [Arrow([-3.05, y, 0], [-2.3, y, 0], buff=0, color=S.GREY, stroke_width=3,
                        max_tip_length_to_length_ratio=0.3) for y in ys]
        imgs = mini_boxes().next_to(rights[1], RIGHT, buff=0.3).set_y(ys[1])
        route = mini_route().next_to(rights[2], RIGHT, buff=0.3).set_y(ys[2])
        drawer = mini_drawer().next_to(rights[3], RIGHT, buff=0.25).set_y(ys[3])
        key = key_glyph(0.32).next_to(drawer, RIGHT, buff=0.18).set_y(ys[3])

        def morph(i, *extra, run_time=0.9):
            self.play(TransformFromCopy(lefts[i], rights[i]), GrowArrow(arrows[i]), *extra,
                      run_time=run_time)

        with self.voiceover(SAY[1]) as vo:
            clear_stage(self, FadeIn(frame), FadeIn(h2), FadeIn(h3), Create(rule), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in lefts], lag_ratio=0.3),
                      run_time=1.0)
            vo.wait_until("you write the Dockerfile")
            morph(0)
            vo.wait_until("and you build five")
            morph(1, LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in imgs], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("A bind mount")
            morph(2, FadeIn(route.fold), FadeIn(route.ctr))
            vo.wait_until("a window into")
            self.play(Create(route.route), run_time=0.7)
            vo.wait_until("and the containers reach")
            morph(3)
            vo.wait_until("through a shared bucket")
            self.play(FadeIn(drawer, shift=UP * 0.15),
                      Indicate(text_span(rights[3], L3[3], "shared bucket"), color=CLOUD,
                               scale_factor=1.06), run_time=0.8)
            vo.wait_until("and a service account key")
            self.play(FadeIn(key, shift=LEFT * 0.15),
                      Indicate(text_span(rights[3], L3[3], "service-account key"), color=COST,
                               scale_factor=1.06), run_time=0.8)

        # ========================================================== 2. how to follow along
        page = readme_page().move_to([2.6, 0.25, 0])
        video = this_video().move_to([-2.5, 0.25, 0])
        tr = tracker("R")                        # where S03 pins it: left -6.5, top 3.5
        ring = RoundedRectangle(width=tr.width + 0.16, height=tr.height + 0.16, corner_radius=0.12,
                                stroke_color=TURN, stroke_width=3).move_to(tr)
        panel = src_panel("transcribe_audio/cli.py", 18, 20)
        panel.shift([-6.3 - panel.get_left()[0], 1.9 - panel.get_top()[1], 0])
        head_ring = SurroundingRectangle(panel.header, color=TURN, buff=0.08, corner_radius=0.08,
                                         stroke_width=3)
        t = term(P_HOME, rows=3)
        prev = preview_tag()
        prev.move_to([t.box.get_right()[0] - 0.35 - prev.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])

        with self.voiceover(SAY[2]) as vo:
            clear_stage(self, FadeIn(page, shift=LEFT * 0.6), run_time=0.8)
            vo.wait_until("beside this video")
            self.play(FadeIn(video, shift=RIGHT * 0.3), run_time=0.6)
            vo.wait_until("The tracker")
            # the README page flies up to the corner and becomes the tracker
            self.play(page.animate.scale(0.25).move_to(tr).set_opacity(0),
                      FadeIn(tr, target_position=page.get_center(), scale=0.8),
                      FadeOut(video), run_time=1.0)
            self.remove(video, page)
            self.play(Create(ring), run_time=0.5)
            for _ in range(2):
                self.play(ring.animate(rate_func=there_and_back).set_stroke(width=6), run_time=0.6)
            vo.wait_until("code panels show")
            self.play(FadeOut(ring), FadeIn(panel, shift=RIGHT * 0.6), run_time=0.8)
            self.remove(ring)
            vo.wait_until("file and line numbers")
            self.play(Create(head_ring), run_time=0.6)
            vo.wait_until("Pause at the yellow")
            self.play(FadeOut(head_ring), FadeIn(t), FadeIn(prev), run_time=0.5)
            self.remove(head_ring)
            cl = t.type(self, CLONE.cmd, type_time=0.9)
            pin(self, cl, beside(your_turn(), t, cl))
            vo.wait_until("a gray extra tag")
            ls = t.type(self, "ls", type_time=0.3)
            xt = pin(self, ls, beside(extra_tag(), t, ls))
            vo.wait_until("not in the README")
            self.play(Indicate(xt, color=S.WHITE, scale_factor=1.12), run_time=0.8)

        # ========================================================== 3. before you start
        pitch, y0 = 0.74, 1.35
        rows = VGroup()
        for i, (s, t2c) in enumerate(CHECKS):
            y = y0 - i * pitch
            slot = box(0.36, 0.36, S.GREY, fill_opacity=0.0, radius=0.06, stroke=2).move_to([-4.3, y, 0])
            mark = check_mark(0.34, VENV).move_to(slot)
            txt = label(s, 28, INK, t2c=t2c).next_to(slot, RIGHT, buff=0.3)
            on_baseline(txt, s, y - 0.11)
            row = VGroup(slot, mark, txt)
            row.slot, row.mark, row.text = slot, mark, txt
            rows.add(row)
        gold = key_glyph(0.34).next_to(rows[1].text, RIGHT, buff=0.3).set_y(rows[1].slot.get_y())
        body = VGroup(rows, gold)
        card = box(body.width + 0.9, body.height + 0.8, S.GREY, fill_opacity=0.04).move_to(body)
        VGroup(card, body).move_to([0, 0.9, 0])
        foot = VGroup(label("every command:", 22, S.GREY), mono(GUIDE, 22, INK)).arrange(DOWN, buff=0.16)
        foot.move_to([0, -1.25, 0])
        guide_path = VGroup(*foot[1][len("MLOps_Learning·"):])        # glyphs: no spaces
        repo_name = VGroup(*foot[1][:len("MLOps_Learning")])

        def tick(r):
            return AnimationGroup(Create(r.mark), FadeIn(r.text, shift=RIGHT * 0.15))

        with self.voiceover(SAY[3]) as vo:
            clear_stage(self, FadeIn(card), *[Create(r.slot) for r in rows], run_time=0.8)
            self.play(tick(rows[0]), run_time=0.8)
            vo.wait_until("for Docker Desktop")
            tools = text_span(rows[0].text, CHECKS[0][0], "Docker Desktop + uv")
            self.play(Indicate(tools, color=TOOL, scale_factor=1.08), run_time=0.8)
            vo.wait_until("the course key from Canvas")
            self.play(tick(rows[1]), FadeIn(gold, shift=LEFT * 0.15), run_time=0.8)
            vo.wait_until("and your group name")
            self.play(tick(rows[2]), run_time=0.8)
            vo.wait_until("Every command")
            self.play(FadeIn(foot, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("in the study guide")
            self.play(Indicate(guide_path, color=S.WHITE, scale_factor=1.05), run_time=0.8)
            vo.wait_until("in the MLOps Learning repo")
            self.play(Indicate(repo_name, color=S.WHITE, scale_factor=1.1), run_time=0.8)

        # ========================================================== 4. the honest limit
        t4 = term(component="transcribe_audio", rows=3)
        prev4 = preview_tag()
        prev4.move_to([t4.box.get_right()[0] - 0.35 - prev4.width / 2, t4.box.get_top()[1] - t4.bar_h / 2, 0])
        sky = cloud(6.4, CLOUD, fill_opacity=0.0)
        sky = DashedVMobject(sky, num_dashes=70, dashed_ratio=0.55).set_stroke(CLOUD, 3)
        sky.move_to([0, 0.95, 0])
        caption = label("recorded without the course key", 24, S.GREY).move_to([0, 3.05, 0])
        lf = look_for_card().move_to([0, 0.45, 0])
        hole = box(t4.box.width - 0.45, 2 * t4.pitch, S.GREY, dashed=True, radius=0.08)
        hole.move_to(t4._slot(1) + np.array([-0.1 + hole.width / 2, 0.03 - hole.height / 2, 0]))

        with self.voiceover(SAY[4]) as vo:
            clear_stage(self, FadeIn(t4), FadeIn(prev4), run_time=0.7)
            vo.wait_until("we recorded without")
            self.play(FadeIn(caption, shift=DOWN * 0.15), run_time=0.5)
            cmd4 = t4.type(self, DOWNLOAD, type_time=0.9)
            vo.wait_until("so wherever the code")
            self.play(Create(sky), run_time=1.1)
            vo.wait_until("you'll see the command")
            self.play(Indicate(glyph_range(cmd4, len(t4.prompt) + 1), color=TURN, scale_factor=1.06),
                      run_time=0.8)
            vo.wait_until("and what to look for")
            self.play(FadeIn(VGroup(lf.frame, lf.title), shift=UP * 0.2), run_time=0.5)
            self.play(LaggedStart(*[Create(b) for b in lf.bars], lag_ratio=0.5), run_time=0.7)
            vo.wait_until("not its output")
            self.play(Create(hole), run_time=0.7)

        # ========================================================== 5. what we recorded on
        lap = laptop(2.5, LAPTOP).move_to([-3.1, 0.95, 0])
        mach = label(MACHINE, 26, S.GREY).next_to(lap, DOWN, buff=0.3)
        c_mac = chip("macOS: zsh, %", S.GREY, size=24)
        c_win = chip("Windows: Git BASH", S.GREY, size=24)
        oses = VGroup(c_mac, c_win).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([2.7, 1.25, 0])
        dd = chip("Docker Desktop", TOOL, size=24).next_to(oses, DOWN, buff=0.45).align_to(oses, LEFT)

        with self.voiceover(SAY[5]) as vo:
            old = VGroup(sky, caption, lf, hole, prev4)
            self.play(FadeOut(old), FadeOut(t4.lines), *leave_container(t4, P_HOME), run_time=0.7)
            self.remove(old, *t4.lines)
            for m in list(t4.lines):
                t4.lines.remove(m)
            vo.wait_until("on a Debian 12 laptop")
            self.play(FadeIn(lap, shift=UP * 0.15), FadeIn(mach, shift=UP * 0.15), run_time=0.8)
            dv = t4.type(self, DV.cmd, type_time=0.6)
            pin(self, dv, beside(extra_tag(), t4, dv), run_time=0.3)
            vo.wait_until("with Docker Engine 29")
            out = t4.print(self, DV.at((2, 3)), run_time=0.5)
            v29 = substring(out[1], "29.8.2")
            self.play(Indicate(v29, color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("at the time of recording")
            pin(self, out[1], beside(recorded_tag(), t4, out[1]), run_time=0.5)
            vo.wait_until("On a Mac or Windows")
            self.play(LaggedStart(FadeIn(c_mac, shift=LEFT * 0.2), FadeIn(c_win, shift=LEFT * 0.2),
                                  lag_ratio=0.4), run_time=0.8)
            vo.wait_until("the prompt differs")
            self.play(Indicate(glyph_range(dv, 0, len(P_HOME)), color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("and Docker Desktop")
            self.play(FadeIn(dd, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the commands are the same")
            self.play(Indicate(glyph_range(dv, len(P_HOME) + 1), color=TURN, scale_factor=1.08), run_time=0.8)

        clear_stage(self, run_time=0.8)

