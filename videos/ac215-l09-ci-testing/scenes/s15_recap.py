"""S15 · Tear down, recap, and what's next (README "Docker Cleanup", tracker F1 -> F3; the last scene).

Beats (script.md, ## S15; one voiceover block each):
0. TRACKER F1 (tracker F appears). A 10-row `laptop` terminal at 20 pt (the squeezed `docker image
   ls` table is 69 columns: 22 pt holds 65). `docker container ls` (README.md line 571) ->
   clean-01: 2 (squeezed), header only. A README card `README.md · line 572` "Stop any container
   that is running" above the terminal, with the GREY chip "nothing to stop here". TRACKER F2:
   `docker system prune` (README:573, `▶ your turn`) -> clean-02: 2–7, then line 8 cut after
   `[y/N]`, a beat, the typed `y` (YELLOW flash); `…` (9–25 skipped) and 26: `95.17MB` ringed and
   `at the time of recording` beside it. TRACKER F3: the terminal clears; `docker image ls`
   (README:574) -> clean-03: 2–4 squeezed (line 5, the capture-only `python:3.11-slim-bookworm`
   row, is never printed: Capture.line() refuses it); the two cheese image names ringed TEAL.
   `pre-commit uninstall` (extra; the tracker caption gains " · extra") -> clean-04: 2. The
   terminal leaves; a GREY `laptop · babykev` card: `.venv/` (GREEN file card) is struck out on
   "delete the venv"; the BLUE model chip `Qwen/Qwen2.5-0.5B` with "~1 GB · Hugging Face cache"
   (ASSETS.md:230) and "if you ran the smoke", struck out too. The card leaves; a laptop glyph
   with a five-arch turnstile on its screen, GREEN "nothing billable today" and GREY "the gate
   lives on your laptop" (the GOLD rule, said once): the arches pass GREEN on that phrase.
1. Tracker and laptop leave. "Test yourself" (YELLOW underline) top-left; one question at a time
   at 26 pt (<= 3 lines) on the right, each under a YELLOW number badge, with a text-free icon
   from its set piece: Q1 the nested boxes (unit, integration, the GREEN dashed hermetic border,
   the BLUE system box, the PINK wire to a BLUE server; they light in turn on "file by file");
   Q2 a GREEN headline bar over four GREY dashed skip dots (the bar pulses on "What does pytest
   actually print", each dot on "hermetic"). When a question is replaced, its badge flies into the
   list at the left and turns GREY; its one-line label fades in: "three kinds" · "silent skip".
2. Q3 the hand-over chain (git commit chip, hook file, PURPLE pre-commit, TEAL config file, a
   nine-arch turnstile; the hook file flashes on "actually create", the chain lights down on
   "every clone"); Q4 an envelope runs into an arch that turns YELLOW (black's "modified") and
   bounces back; Q5 the built 6x6 mask (MaskGrid "ones") whose rows 5–6 get RED boxes on "a wrong
   mask", and a GREEN coverage bar sweeps every row on "coverage blind". Labels: "the hook file"
   · "modified by black" · "properties over coverage".
3. The list stays at left. Footer cards: "Answers: exercises.md" (under the list) and "Study guide
   + every command:" github.com/JunyiZhou-Conny/MLOps_Learning · guides/L09-ci-testing-precommit.md
   (right). A GREY dashed "Next" card: a key glyph runs into the `detect-private-key` arch, which
   turns RED and sends it back ("L10: credentials"); a BLUE server with a turnstile whose arches
   pass GREEN ("L21: this repo's checks on GitHub") and a GREY `--no-verify` chip that is struck
   out RED. Everything fades to an empty frame (end of part 2).

Deviations (reported to the coordinator):
- No lecture tag: neither the SHOW lines nor the BRIEF name slides for S15.
- The terminal is 20 pt (clean-03 squeezed is 69 columns) and clears before `docker image ls`, so
  the prune's rows never scroll over the tracker.
- The babykev cleanup and the "nothing billable" line are said only in the SHOW; they get a small
  card (".venv/", the model with ASSETS.md's "~1 GB") and a laptop-with-gate picture, so something
  moves while they are said. No GOLD tag (BRIEF: nothing billable, GOLD unused on screen).
- The question texts are the SHOW's, in the label font (no mono spans); Q2 keeps 'pass' in quotes.
- The "Test yourself" title heads the label list (one group), not a separate card.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer import style as S
from explainer.devops import laptop as laptop_glyph, server as server_glyph

from common import (CLOUD, ERR, FUTURE, HERMETIC, IMAGE, INK, INTEG, LAPTOP, NARRATION, OUTPUT,
                    P_LAPTOP, SEG_SIX, SYSTEM_TEST, TOOL, TURN, UNIT, VENV, ROUTE, Arch,
                    MaskGrid, TestDot, Turnstile, ask, attach, beside, box, capture, envelope,
                    extra_row, file_card, file_glyph, grey_chip, label, mono, mono_line,
                    outline_box, pin, readme, readme_card, ring, squeeze, steady, strike, substring, term,
                    time_row, track, tracker, turn_row, type_cmd)

SAY = NARRATION["S15"]

# ------------------------------------------------------------------ the real captures
LS = capture("clean-01")                      # laptop/clean-01-container-ls.txt
assert readme(571) == f"* Run `{LS.cmd}`", LS.cmd
LS_HEAD = squeeze(LS.at(2))                   # header only: nothing is running
assert LS.lines == [LS.line(2)] and LS_HEAD[0].startswith("CONTAINER ID"), LS.lines
STOP = readme(572)
assert STOP == "* Stop any container that is running", STOP

PRUNE = capture("clean-02")                   # laptop/clean-02-prune.txt (typed y)
assert readme(573) == f"* Run `{PRUNE.cmd}`", PRUNE.cmd
PRUNE_WARN = PRUNE.at((2, 7))                 # WARNING! … unused build cache, ""
PRUNE_ASK = ask(PRUNE.line(8))                # cut after [y/N]; the y is typed
assert PRUNE.line(8) == PRUNE_ASK + " y", PRUNE.line(8)
PRUNE_TOTAL = PRUNE.line(26)
assert PRUNE_TOTAL == "Total reclaimed space: 95.17MB", PRUNE_TOTAL
assert PRUNE.line(9) == "Deleted build cache objects:" and PRUNE.line(25) == ""

IMG = capture("clean-03")                     # laptop/clean-03-image-ls.txt
assert readme(574) == f"* Run `{IMG.cmd}`", IMG.cmd
IMG_ROWS = squeeze(IMG.at((2, 4)))            # line 5 (python:3.11-slim-bookworm) is capture-only
assert "python" not in " ".join(IMG_ROWS) and len(IMG_ROWS) == 3, IMG_ROWS
assert all(len(r) <= 72 for r in IMG_ROWS), [len(r) for r in IMG_ROWS]
IMG_NAMES = ("cheese-app-api-service:latest", "cheese-app-api:local")

UNINSTALL = capture("clean-04")               # laptop/clean-04-uninstall.txt (extra)
assert UNINSTALL.cmd == "pre-commit uninstall", UNINSTALL.cmd
UN_OUT = UNINSTALL.at(2)
assert UN_OUT == ["pre-commit uninstalled"], UN_OUT

MODEL = "Qwen/Qwen2.5-0.5B"                   # ASSETS.md:53 (smoke.py:25), ~1 GB (ASSETS.md:230)
GUIDE_REPO = "github.com/JunyiZhou-Conny/MLOps_Learning"
GUIDE_PATH = "guides/L09-ci-testing-precommit.md"

# ------------------------------------------------------------------ the recap (script.md S15)
QUESTIONS = [   # (lines as shown, the list label)
    (["What runs in a unit, an integration and a", "system test of this repo — file by file?"],
     "three kinds"),
    (["The system tests ‘pass’ with no server. What", "does pytest actually print — and are those",
      "four tests hermetic?"], "silent skip"),
    (["What does pre-commit install actually create,", "and why must every clone run it",
      "(or just setup) again?"], "the hook file"),
    (["black says Failed — files were modified.", "Is your code broken, and what do you do next?"],
     "modified by black"),
    (["babykev had 94% coverage and a wrong mask.", "What kind of test finally saw the bug —",
      "and why was coverage blind?"], "properties over coverage"),
]

# ------------------------------------------------------------------ layout
TERM_SIZE = 20
LIST_X = -6.3                 # left edge of the title and the label list
LIST_TOP = 3.4
ROW_GAP = 0.62
Q_X = -1.75                   # left edge of the question block (badge), right edge 6.5
Q_TOP = 3.3
ICON_C = [2.4, -0.85, 0]      # centre of the question's icon
Q_SIZE, L_SIZE = 26, 22


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.shift(RIGHT * (cx - m.get_center()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.shift(UP * (cy - m.get_center()[1]))
    return m


def badge(n: int, color=TURN) -> VGroup:
    """A number in a ring (the question's number; GREY once it is in the list). .c .t"""
    c = Circle(radius=0.27, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    t = steady(str(n), 24, color).move_to(c)        # fixed extent: every digit sits alike
    g = VGroup(c, t)
    g.c, g.t = c, t
    return g


def question(n: int) -> VGroup:
    """Badge + the question's lines (26 pt), top-left at (Q_X, Q_TOP). .badge .text"""
    lines, _ = QUESTIONS[n - 1]
    text = VGroup(*[label(s, Q_SIZE, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    b = badge(n)
    place(b, left=Q_X, top=Q_TOP)
    place(text, left=Q_X + 0.8, top=Q_TOP + 0.02)
    g = VGroup(b, text)
    g.badge, g.text = b, text
    return g


def list_slot(n: int) -> np.ndarray:
    """Centre of the list badge for question n."""
    return np.array([LIST_X + 0.27, LIST_TOP - 1.25 - (n - 1) * ROW_GAP, 0])


# ------------------------------------------------------------------ text-free icons (built at size)
def icon_kinds() -> VGroup:
    """Q1 · V2's nested boxes without words: unit (GREEN) inside integration (TEAL) inside the GREEN
    dashed hermetic border, all inside the BLUE system box, whose PINK wire runs past the border to
    a BLUE server. .unit .integ .border .system .server .wire"""
    system = outline_box(6.4, 2.9, SYSTEM_TEST, solid=True, fill_opacity=0.06, stroke=3)
    border = outline_box(3.9, 2.2, HERMETIC, solid=False, stroke=3)
    integ = outline_box(3.2, 1.6, INTEG, solid=True, fill_opacity=0.08, stroke=3)
    unit = outline_box(1.3, 0.8, UNIT, solid=True, fill_opacity=0.15, stroke=3)
    border.move_to(system).align_to(system, LEFT).shift(RIGHT * 0.3)
    integ.move_to(border)
    unit.move_to(integ).shift(RIGHT * 0.65 + DOWN * 0.15)
    server = RoundedRectangle(width=1.0, height=0.62, corner_radius=0.1, stroke_color=SYSTEM_TEST,
                              stroke_width=3).set_fill(SYSTEM_TEST, 0.3)
    server.move_to([system.get_right()[0] - 0.85, integ.get_center()[1], 0])
    wire = Line(integ.get_right(), server.get_left(), color=ROUTE, stroke_width=4)
    g = VGroup(system, border, integ, unit, wire, server)
    g.unit, g.integ, g.border, g.system, g.server, g.wire = unit, integ, border, system, server, wire
    return g


def icon_skip() -> VGroup:
    """Q2 · a GREEN headline bar (pytest's green summary) over four GREY dashed skip dots. .bar .dots"""
    bar = RoundedRectangle(width=4.2, height=0.42, corner_radius=0.21, stroke_color=VENV,
                           stroke_width=3).set_fill(VENV, 0.55)
    dots = VGroup(*[TestDot(SYSTEM_TEST, r=0.34, state="skip") for _ in range(4)]).arrange(RIGHT, buff=0.55)
    g = VGroup(bar, dots).arrange(DOWN, buff=0.6)
    g.bar, g.dots = bar, dots
    return g


def icon_chain() -> VGroup:
    """Q3 · V5 without words: git commit (GREY chip) -> the hook file (GREY) -> pre-commit (PURPLE
    chip) -> the config file (TEAL) -> a nine-arch turnstile. .links .hook .turnstile"""
    git = RoundedRectangle(width=1.3, height=0.42, corner_radius=0.16, stroke_color=LAPTOP,
                           stroke_width=3).set_fill(LAPTOP, 0.16)
    hook = file_glyph(0.62, LAPTOP)
    tool = RoundedRectangle(width=1.3, height=0.42, corner_radius=0.16, stroke_color=TOOL,
                            stroke_width=3).set_fill(TOOL, 0.18)
    config = file_glyph(0.62, IMAGE)
    col = VGroup(git, hook, tool, config).arrange(DOWN, buff=0.34)
    arrows = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.05, color=S.GREY, stroke_width=3,
                            tip_length=0.14, max_tip_length_to_length_ratio=0.5)
                      for a, b in zip(col, col[1:])])
    ts = Turnstile(9, None, arch_w=0.34, arch_h=0.85, gap=0.1)
    ts.next_to(col, RIGHT, buff=0.9).align_to(config, DOWN)
    drop = Arrow(config.get_right(), [ts.get_left()[0], config.get_center()[1], 0], buff=0.08,
                 color=S.GREY, stroke_width=3, tip_length=0.15)
    links = VGroup(git, arrows[0], hook, arrows[1], tool, arrows[2], config, drop)
    g = VGroup(links, ts)
    g.links, g.hook, g.turnstile, g.arrows = links, hook, ts, VGroup(*arrows, drop)
    return g


def icon_amber() -> VGroup:
    """Q4 · an envelope (no name) before one arch, which will turn YELLOW and send it back.
    .env .arch .floor"""
    arch = Arch(arch_w=1.1, arch_h=2.0)
    env = envelope("x", env_w=1.5, env_h=0.95)
    env.remove(env.text)
    env.next_to(arch, LEFT, buff=1.8).align_to(arch, DOWN).shift(UP * 0.35)
    floor = Line(env.get_corner(DL) + LEFT * 0.3 + DOWN * 0.35, arch.get_corner(DR) + RIGHT * 0.4,
                 color=S.GREY_DARK, stroke_width=3)
    home = Dot(env.get_center(), radius=0.001).set_opacity(0)   # moves with the icon
    g = VGroup(home, floor, arch, env)
    g.env, g.arch, g.floor, g.home = env, arch, floor, home
    return g


def icon_mask() -> MaskGrid:
    """Q5 · the mask step-05 built (all ones over question 1 for rows 5–6), no numbers, no band."""
    return MaskGrid(SEG_SIX, "ones", cell=0.46, numbers=False, band=False)


def key_glyph(color=FUTURE) -> VGroup:
    """A key: a ring bow, a shaft and two bits (text-free)."""
    bow = Circle(radius=0.2, stroke_color=color, stroke_width=4)
    shaft = Line(bow.get_right(), bow.get_right() + RIGHT * 0.75, color=color, stroke_width=4)
    end = shaft.get_end()
    bits = VGroup(Line(end, end + DOWN * 0.2, color=color, stroke_width=4),
                  Line(end + LEFT * 0.22, end + LEFT * 0.22 + DOWN * 0.14, color=color, stroke_width=4))
    return VGroup(bow, shaft, bits)


# ------------------------------------------------------------------ terminal helpers
def type_answer(scene, t, ln, line_text: str, key: str = "y"):
    """The answer keystroke after the question row `ln`: it appears after the bracket and flashes
    YELLOW, then stays as part of the row."""
    y = mono_line(line_text + " " + key, t.size, OUTPUT)
    y.shift(ln.strut.get_corner(UL) - y.strut.get_corner(UL))
    yg = y.glyphs[-1].set_color(TURN)
    scene.play(FadeIn(yg, scale=1.6), run_time=0.25)
    scene.play(Indicate(yg, color=TURN, scale_factor=1.8), run_time=0.5)
    scene.play(yg.animate.set_color(INK), run_time=0.2)
    attach(scene, ln, yg)
    return yg


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == 4, len(SAY)

        # ========================================================== 0. tear down
        tr = tracker("F", 1)
        t = term(P_LAPTOP, rows=10, size=TERM_SIZE)
        card = readme_card(572, STOP[2:])
        chip_ = grey_chip("nothing to stop here")
        VGroup(card, chip_).arrange(RIGHT, buff=0.4)
        place(VGroup(card, chip_), cx=0, cy=(t.box.get_top()[1] + 2.75) / 2)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), run_time=0.8)
            vo.wait_until("The README's Docker cleanup")
            type_cmd(self, t, LS.cmd)
            vo.wait_until("shows nothing running")
            head = t.print(self, LS_HEAD)
            self.play(Indicate(head[0], color=INK, scale_factor=1.03), run_time=0.7)
            vo.wait_until("so nothing to stop")
            self.play(FadeIn(card, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(chip_, shift=LEFT * 0.15), run_time=0.4)

            vo.wait_until("Then docker system prune")
            self.play(FadeOut(VGroup(card, chip_)), track(tr, 2), run_time=0.5)
            self.remove(card, chip_)
            ln = type_cmd(self, t, PRUNE.cmd)
            pin(self, ln, beside(turn_row(), ln))
            t.print(self, PRUNE_WARN, run_time=0.6, lag=0.1)
            ask_ln = t.print(self, [PRUNE_ASK], run_time=0.3)[0]
            vo.wait_until("type y")
            type_answer(self, t, ask_ln, PRUNE_ASK)
            vo.wait_until("about 95 megabytes")
            rows = t.print(self, ["…", PRUNE_TOTAL], run_time=0.4)
            total = rows[1]
            mb = substring(total, "95.17MB")
            mb_ring = ring(mb, TURN)
            self.play(Create(mb_ring), run_time=0.5)
            attach(self, total, mb_ring)
            vo.wait_until("at the time of recording")
            pin(self, total, beside(time_row(), total))

            vo.wait_until("A final docker image ls")
            t.clear(self)
            self.play(track(tr, 3), run_time=0.4)
            type_cmd(self, t, IMG.cmd)
            out = t.print(self, IMG_ROWS, run_time=0.5)
            vo.wait_until("shows the two cheese images")
            names = VGroup(*[substring(r, s) for r, s in zip(out[1:], IMG_NAMES)])
            img_ring = ring(names, IMAGE, buff=0.1)
            self.play(Create(img_ring), run_time=0.6)
            attach(self, out[1], img_ring)

            vo.wait_until("One extra undoes the hook")
            un = type_cmd(self, t, UNINSTALL.cmd)
            xt = beside(extra_row(), un)
            pin(self, un, xt, anim=AnimationGroup(FadeIn(xt, shift=LEFT * 0.1), track(tr, 3, extra=True)))
            vo.wait_until("pre-commit uninstall.")
            t.print(self, UN_OUT, run_time=0.4)

            # babykev, said only: a small card of what to delete
            venv = file_card(".venv/", VENV, size=22)
            model = VGroup(mono(MODEL, 22, INK), label("~1 GB · Hugging Face cache", 22, S.GREY))
            model.arrange(RIGHT, buff=0.3)
            mbox = box(model.width + 0.5, model.height + 0.4, CLOUD, fill_opacity=0.1)
            model.move_to(mbox)
            model_card = VGroup(mbox, model)
            smoke = label("if you ran the smoke", 20, S.GREY)
            body = VGroup(venv, VGroup(model_card, smoke).arrange(DOWN, buff=0.15, aligned_edge=LEFT))
            body.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            head_b = mono("laptop · babykev", 20, S.GREY)
            inner = VGroup(head_b, body).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            frame = box(inner.width + 0.8, inner.height + 0.7, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
            inner.move_to(frame)
            bk = VGroup(frame, head_b, venv)
            VGroup(frame, inner).move_to([0, -0.3, 0])
            s_venv = strike(venv, S.GREY, stroke=5)
            s_model = strike(model_card, S.GREY, stroke=5)

            vo.wait_until("On the babykev side")
            self.play(FadeOut(t), run_time=0.5)
            self.remove(t)
            self.play(FadeIn(bk, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("delete the venv")
            self.play(Create(s_venv), venv.animate.fade(0.55), run_time=0.6)
            vo.wait_until("and if you ran the smoke")
            self.play(FadeIn(smoke, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("the roughly 1 gigabyte model")
            self.play(FadeIn(model_card, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("in the Hugging Face cache")
            self.play(Create(s_model), model_card.animate.fade(0.55), run_time=0.6)

            # nothing billable: the whole gate is on the laptop
            lap = laptop_glyph(4.4, LAPTOP)
            gate = Turnstile(5, None, arch_w=0.42, arch_h=1.0, gap=0.16)
            gate.move_to(lap.screen)
            lap_g = VGroup(lap, gate).move_to([0, 0.55, 0])
            free = label("nothing billable today", 28, VENV)
            where = label("the gate lives on your laptop", 24, S.GREY)
            caps = VGroup(free, where).arrange(DOWN, buff=0.18).next_to(lap_g, DOWN, buff=0.4)
            vo.wait_until("Nothing today was billable")
            self.play(FadeOut(VGroup(frame, head_b, venv, s_venv, model_card, s_model, smoke)), run_time=0.5)
            self.remove(frame, head_b, venv, s_venv, model_card, s_model, smoke)
            self.play(FadeIn(lap_g, shift=UP * 0.15), FadeIn(free, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("the gate lives on your laptop")
            self.play(FadeIn(where, shift=UP * 0.1), gate.mark_all(["pass"] * 5, run_time=1.0))
            vo.wait_until("and that is the point")
            self.play(Indicate(free, color=VENV, scale_factor=1.08), run_time=0.8)

        # ========================================================== 1. test yourself: Q1, Q2
        title = label("Test yourself", 32, INK)
        place(title, left=LIST_X, top=LIST_TOP)
        uline = Line(title.get_corner(DL) + DOWN * 0.1, title.get_corner(DR) + DOWN * 0.1, color=TURN,
                     stroke_width=4)
        listed = VGroup()                  # badges and labels in the list (grows)

        def ask_q(n, icon):
            q = question(n)
            place(icon, cx=ICON_C[0], cy=ICON_C[1])
            self.play(FadeIn(q.badge, scale=0.8), FadeIn(q.text, shift=LEFT * 0.2), run_time=0.6)
            self.play(FadeIn(icon, shift=UP * 0.15), run_time=0.6)
            return q

        def file_away(q, icon, n, *extra):
            """The question leaves; its badge flies to the list and turns GREY; its label appears."""
            nb = badge(n, S.GREY).move_to(list_slot(n))
            lab = steady(QUESTIONS[n - 1][1], L_SIZE, S.GREY)    # descenders don't shift the row
            lab.next_to(nb, RIGHT, buff=0.22)
            self.play(FadeOut(q.text, shift=LEFT * 0.3), FadeOut(icon), *extra, run_time=0.5)
            self.remove(icon)
            self.play(ReplacementTransform(q.badge, nb), run_time=0.6)
            self.play(FadeIn(lab, shift=RIGHT * 0.15), run_time=0.35)
            listed.add(nb, lab)

        kinds = icon_kinds()
        skip = icon_skip()
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(tr, lap_g, caps)), run_time=0.6)
            self.remove(tr, lap_g, caps)
            self.play(FadeIn(title, shift=DOWN * 0.1), Create(uline), run_time=0.6)
            vo.wait_until("One:")
            q1 = ask_q(1, kinds)
            vo.wait_until("file by file")
            for part, col in ((kinds.unit, UNIT), (kinds.integ, INTEG), (kinds.system, SYSTEM_TEST)):
                self.play(part.fill.animate.set_fill(col, 0.4), run_time=0.35)
                self.play(part.fill.animate.set_fill(col, 0.08), run_time=0.35)
            self.play(Indicate(kinds.server, color=SYSTEM_TEST, scale_factor=1.12), run_time=0.5)

            vo.wait_until("Two:")
            file_away(q1, kinds, 1)
            q2 = ask_q(2, skip)
            vo.wait_until("What does pytest actually print")
            self.play(skip.bar.animate.set_fill(VENV, 0.9), run_time=0.4)
            self.play(skip.bar.animate.set_fill(VENV, 0.55), run_time=0.4)
            vo.wait_until("are those four tests hermetic")
            for d in skip.dots:
                self.play(Indicate(d.ring, color=INK, scale_factor=1.2), run_time=0.3)

        # ========================================================== 2. Q3, Q4, Q5
        chain = icon_chain()
        amber = icon_amber()
        mask = icon_mask()
        with self.voiceover(SAY[2]) as vo:
            vo.wait_until("Three:")
            file_away(q2, skip, 2)
            q3 = ask_q(3, chain)
            vo.wait_until("actually create")
            self.play(Indicate(chain.hook, color=TURN, scale_factor=1.25), run_time=0.8)
            vo.wait_until("why must every clone run it again")
            self.play(LaggedStart(*[Indicate(a, color=TURN, scale_factor=1.1) for a in chain.arrows],
                                  lag_ratio=0.3), run_time=1.0)
            self.play(chain.turnstile.mark_all(["pass"] * 9, run_time=0.8))

            vo.wait_until("Four:")
            file_away(q3, chain, 3)
            q4 = ask_q(4, amber)
            vo.wait_until("files were modified")
            a = amber.arch
            home = amber.home.get_center().copy()
            self.play(amber.env.animate.move_to([a.get_left()[0] - amber.env.width / 2 + 0.3, home[1], 0]),
                      a.to("modified"), run_time=0.6)
            self.play(Indicate(a.lamp, color=TURN, scale_factor=1.6), run_time=0.4)
            self.play(amber.env.animate(path_arc=0.7).move_to(home), run_time=0.7)
            vo.wait_until("what do you do next")
            self.play(Indicate(a.frame, color=TURN, scale_factor=1.06), run_time=0.7)

            vo.wait_until("Five:")
            file_away(q4, amber, 4)
            q5 = ask_q(5, mask)
            boxes = VGroup(mask.row_box(4), mask.row_box(5))
            vo.wait_until("a wrong mask")
            self.play(Create(boxes), run_time=0.6)
            vo.wait_until("why was coverage blind")
            sweep = Rectangle(width=VGroup(*mask.cells[0]).width + 0.2, height=mask.cell * 0.9,
                              stroke_width=0).set_fill(VENV, 0.35).move_to(VGroup(*mask.cells[0]))
            self.play(FadeIn(sweep), run_time=0.2)
            self.play(sweep.animate.move_to(VGroup(*mask.cells[5])), run_time=1.2, rate_func=linear)
            self.play(FadeOut(sweep), run_time=0.3)
            self.remove(sweep)
            self.add(boxes)
            self.play(Indicate(boxes, color=ERR, scale_factor=1.04), run_time=0.6)

        # ========================================================== 3. answers, guide, next
        ans = VGroup(label("Answers:", 22, INK), mono("exercises.md", 22, INK)).arrange(RIGHT, buff=0.2)
        ans_box = box(ans.width + 0.6, ans.height + 0.5, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        ans.move_to(ans_box)
        ans_card = VGroup(ans_box, ans)
        place(ans_card, left=LIST_X, bottom=-3.4)
        guide = VGroup(label("Study guide + every command:", 22, INK), mono(GUIDE_REPO, 20, INK),
                       mono(GUIDE_PATH, 20, INK)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        guide_box = box(8.2, guide.height + 0.5, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        place(guide, left=guide_box.get_left()[0] + 0.3, cy=guide_box.get_center()[1])
        guide_card = VGroup(guide_box, guide)
        place(guide_card, right=6.5, bottom=-3.4)

        # the Next card: right column, above the guide card
        nxt_top, nxt_bottom = 3.4, guide_card.get_top()[1] + 0.3
        nxt_frame = outline_box(8.2, nxt_top - nxt_bottom, FUTURE, solid=False, fill_opacity=0)
        place(nxt_frame, right=6.5, top=nxt_top)
        nxt_head = label("Next", 24, S.GREY)
        place(nxt_head, left=nxt_frame.get_left()[0] + 0.35, top=nxt_top - 0.22)
        mid = (nxt_head.get_bottom()[1] + nxt_bottom) / 2
        # row 1 · L10: a key runs into detect-private-key and is sent back
        key = key_glyph()
        pk = Arch(arch_w=0.6, arch_h=1.05)
        pk_name = mono("detect-private-key", 20, S.GREY)
        l10 = label("L10: credentials", 22, S.GREY)
        place(pk, left=nxt_frame.get_left()[0] + 2.75, bottom=mid + 0.55)
        place(key, right=pk.get_left()[0] - 1.0, cy=pk.get_bottom()[1] + 0.4)
        place(pk_name, cx=pk.get_center()[0], top=pk.get_bottom()[1] - 0.1)
        place(l10, left=pk.get_right()[0] + 1.0, cy=pk.get_center()[1])
        key_home = key.get_center().copy()
        row1 = VGroup(key, pk, pk_name, l10)
        # row 2 · L21: the same checks on a BLUE server, where --no-verify does not get past
        srv = server_glyph(1.0, 3, CLOUD)
        ci = Turnstile(5, None, arch_w=0.36, arch_h=0.8, gap=0.12)
        l21 = label("L21: this repo’s checks on GitHub", 22, S.GREY)
        place(l21, left=nxt_frame.get_left()[0] + 0.45, top=mid - 0.1)
        place(srv, left=nxt_frame.get_left()[0] + 0.45, top=l21.get_bottom()[1] - 0.25)
        place(ci, left=srv.get_right()[0] + 0.3, bottom=srv.get_bottom()[1])
        nv = grey_chip("--no-verify", mono_font=True)
        place(nv, left=ci.get_right()[0] + 0.6, cy=srv.get_center()[1])
        nv_strike = strike(nv, ERR)
        row2 = VGroup(srv, ci, l21)

        with self.voiceover(SAY[3]) as vo:
            file_away(q5, mask, 5, FadeOut(boxes))
            self.remove(boxes)
            vo.wait_until("The answers are in the exercises")
            self.play(FadeIn(ans_card, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("every command is in the study guide")
            self.play(FadeIn(guide_card, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Next lecture brings cloud credentials")
            self.play(FadeIn(nxt_frame), FadeIn(nxt_head), run_time=0.5)
            self.play(FadeIn(row1, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("where the detect private keys hook")
            self.play(key.animate.move_to([pk.get_left()[0] - key.width / 2 + 0.15, key_home[1], 0]),
                      run_time=0.5)
            self.play(pk.to("fail"), run_time=0.3)
            self.play(Indicate(pk.lamp, color=ERR, scale_factor=1.6), run_time=0.4)
            self.play(key.animate(path_arc=0.6).move_to(key_home), run_time=0.6)
            vo.wait_until("And in lecture 21")
            self.play(FadeIn(row2, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("this very repo's checks run on GitHub")
            self.play(ci.mark_all(["pass"] * 5, run_time=0.9))
            vo.wait_until("where nobody can walk past them")
            self.play(FadeIn(nv, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("with dash dash no verify")
            self.play(Create(nv_strike), run_time=0.4)

        self.wait(0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
