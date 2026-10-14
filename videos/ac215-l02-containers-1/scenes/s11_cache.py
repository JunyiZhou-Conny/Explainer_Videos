"""S11 · The layer cache (TRACKER A16 · extra for the whole scene; V5 full: CacheChain + Parcel + Sieve).

Beats (script.md "## S11", one voiceover block each):
 0  Concept first, no terminal. Boxes 3 and 4 (`[3/4] COPY . ./`, `[4/4] RUN uv sync`) appear and
    flash RED on "rerun"; at "caches every build step" boxes 1 and 2 join them and every box drops a
    domino. At "its parent step" thin TEAL arrows grow from each box to the next box's badge spot, at
    "and its instruction" from each box up to its own spot; at "are unchanged" they merge into four
    TEAL fingerprint badges. "For COPY, the checksum": a small GREY parcel (PINK tape, "build
    context") docks above COPY's badge and feeds it a third arrow. "The first step that changes":
    box 2's instruction flickers YELLOW, its badge turns RED, dominoes 2, 3, 4 topple on "runs
    again" / "every step after it"; then they stand back up and the badge returns to TEAL.
 1  The parcel leaves; the chain rises and closes up (badges sit on the box lids) above an 8-row
    terminal that types `docker build --progress=plain -t simple-translate -f Dockerfile .` (extra;
    row tag "extra · full log", `--progress=plain` underlined) -> laptop/38: 23 (cut after
    `apt-get update &&`), 24, 26–27, 29–30. "FROM reuses the base": box 1 gets a TEAL "reused"
    stamp; "and the three steps … all say CACHED": the three CACHED words turn TEAL as boxes 2–4 get
    TEAL CACHED stamps; the standing dominoes pulse on "nothing runs".
 2  The terminal shrinks to the 3-row strip. The parcel returns under COPY and enlarges (.git/,
    .git/index, cli.py, Dockerfile); cli.py lights YELLOW and CODE(cli.py: 49) docks beside it
    (YELLOW bar). The four boxes pulse on "Which of the four steps". PONDER (8 s): the card covers
    the strip.
 3  "on line 49": the panel header pulses; `cheese` morphs into a YELLOW `brie`. The strip types
    `git diff` (extra) -> laptop/39: 10–11 (- RED, + GREEN). "a different checksum": a RED
    fingerprint rises from cli.py into COPY's badge, which turns RED.
 4  The parcel and panel leave; the strip grows to 8 rows: `docker build --progress=plain …` (extra)
    -> laptop/40: 23 (cut), 24 (stamps 1–2 pulse, CACHED TEAL), then on "so COPY runs" 26–27 (stamp 3
    falls, domino 3 topples RED), on "and uv sync after it" 29–30 wrapped (stamp 4 falls, domino 4
    topples), on "Python download and all" a PURPLE "35.9 MiB" download arrow fires into box 4
    (`35.9MiB` underlined PURPLE), then "…", 36.
 5  The dominoes stand back up as the terminal shrinks to the strip; the parcel and panel return.
    `git checkout -q cli.py` (extra; run_steps.sh line 139) -> no output; `brie` morphs back to
    `cheese`, cli.py dims. "Same files": COPY's badge flickers TEAL but stays RED. The picture leaves,
    the terminal grows to 8 rows: `docker build --progress=plain …` (extra) -> laptop/41: 26–27, 29–30
    (wrap); the RED wave topples dominoes 3 and 4 again. "Git rewrote its own index file": the
    terminal shrinks to the strip (rows 26, 27, 29), the parcel returns, `.git/index` flips YELLOW,
    `.git/` pulses, a RED fingerprint rises from it into COPY's badge.
 6  The strip leaves, the dominoes stand up, boxes 3–4 pulse ("the question from part 1"). The
    `Dockerfile` glyph flips YELLOW; a RED fingerprint rises into COPY's badge; GREY caption
    "Dockerfile steps 4 and 5: every edit to the Dockerfile changed the parcel"; tag "erratum ·
    expected while learning".
 7  The chain and the parcel settle lower (the parcel's title moves to its left); tag "a pattern for
    your own projects / not the course solution" top right. "put the slow steps first": uv sync
    pulses. "copy only the files uv sync needs": `COPY . ./` steps out of the row and a new
    `[3/5] COPY pyproject.toml README.md ./` box splits off it, left of `RUN uv sync` (renumbered
    [4/5]); "then copy the rest": the old box slides under uv sync to the end as [5/5] and a fifth
    domino stands up. The `.dockerignore` card (tag "illustration · a file you'd
    add") returns with `.git`, `.venv`, `secrets/` (GREEN) and `Dockerfile` slides in YELLOW; a dashed
    sieve over the parcel turns solid GREEN and catches `.git/`, `.git/index` and `Dockerfile`.
    `cli.py` lights YELLOW, a RED fingerprint rises into the last badge, only the last domino
    topples; boxes 1–4 get "reused"/CACHED stamps, uv sync's pulses. GREY footnote "full
    Dockerfile: exercises.md". Fade out to an empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import code_panel, code_span, line_bar
from explainer.scene import VoiceScene

from common import (BUILD_PLAIN, ERR, IMAGE, INK, LAPTOP, LAPTOP_DIR, NARRATION, ROUTE, STRIP_ROWS, TERMINAL,
                    TOOL, TURN, VENV, CacheChain, Parcel, Sieve, attach, bare_prompt, beside, box, capture,
                    code, cut, erratum_tag, excerpt, file_glyph, fingerprint, illustration_tag, label,
                    laptop_term, mono, pin, resize, row_tag, stand_in_tag, substring, type_cmd, tracker_a,
                    under)

SAY = NARRATION["S11"]
PONDER_Q = "You change one word in cli.py and rebuild.\nWhich of the four steps run again?"

STEPS4 = ["[1/4] FROM", "[2/4] RUN apt…uv", "[3/4] COPY . ./", "[4/4] RUN uv sync"]
STEPS5 = ["[1/5] FROM", "[2/5] RUN apt…uv", "[3/5] COPY pyproject.toml\nREADME.md ./", "[4/5] RUN uv sync",
          "[5/5] COPY . ./"]
NAMES = (".git/", ".git/index", "cli.py", "Dockerfile")
GIT_DIFF = "git diff"
GIT_CHECKOUT = "git checkout -q cli.py"          # run_steps.sh line 139 (no capture: it prints nothing)
assert f"\n  {GIT_CHECKOUT}\n" in (TERMINAL / "run_steps.sh").read_text()

# ------------------------------------------------------------------ real outputs (file line numbers)
C38 = capture("38", LAPTOP_DIR)                       # laptop/38-rebuild-same.txt
assert C38.cmd == BUILD_PLAIN, C38.cmd
OUT38 = [cut(C38.line(23), "apt-get update &&"), *C38.at(24, (26, 27), (29, 30))]
assert [OUT38[k].endswith("CACHED") for k in (1, 3, 5)] == [True] * 3 and "[3/4] COPY . ./" in OUT38[2], OUT38

C39 = capture("39", LAPTOP_DIR)                       # laptop/39-edit-cli.txt
assert C39.cmd == GIT_DIFF, C39.cmd
DIFF = C39.at(10, 11)
assert DIFF[0].startswith("-") and "I love cheese" in DIFF[0] and "I love brie" in DIFF[1], DIFF

C40 = capture("40", LAPTOP_DIR)                       # laptop/40-rebuild-edited.txt
assert C40.cmd == BUILD_PLAIN, C40.cmd
OUT40_A = [cut(C40.line(23), "apt-get update &&"), C40.line(24)]          # [2/4] … CACHED
OUT40_B = C40.at((26, 27))                                                 # [3/4] COPY . ./ · DONE 0.0s
OUT40_C = C40.at(29, 30)                                                   # [4/4] RUN uv sync · Downloading (35.9MiB)
OUT40_D = C40.at("…", 36)                                                  # Installed 11 packages
assert OUT40_A[1] == "#6 CACHED" and OUT40_B[1] == "#7 DONE 0.0s" and "(35.9MiB)" in OUT40_C[1], (OUT40_B, OUT40_C)
assert "Installed 11 packages" in OUT40_D[1]

C41 = capture("41", LAPTOP_DIR)                       # laptop/41-rebuild-restored.txt
assert C41.cmd == BUILD_PLAIN, C41.cmd
OUT41 = C41.at((26, 27), (29, 30))
assert OUT41[1] == "#7 DONE 0.0s" and "(35.9MiB)" in OUT41[3], OUT41

LINE49 = excerpt("cli.py", 49, 49)                    # '        default="I love cheese",'
assert LINE49.strip() == 'default="I love cheese",', LINE49
BRIE49 = LINE49.replace("I love cheese", "I love brie")

# ------------------------------------------------------------------ layout
LID = 0.12            # badge centre above its box's lid (compact chain: a seal on the lid)
LIFT = 0.8            # beat 0: badge centre above the box (room for the feed arrows)
GAP_C, GAP_G = 0.4, 0.55          # box bottom -> domino top (compact, beat 0)
BOTTOM_C = 1.58       # compact chain: box bottoms (badge tops 2.77, domino bottoms 0.73: above an 8-row terminal)
BOTTOM_G = -0.7       # beat 0: box bottoms
BOTTOM_5 = 1.28       # beat 7: the five-step chain (its 3-line box is 0.3 taller)
PARCEL_TOP = 0.5      # the parcel (title included) under the chain, beats 2-6
DIP = 1.35            # beat 7: how far COPY . ./ steps out of the row (under the new box, above the parcel)
FRAME_TOP_7 = -1.0   # beat 7: the parcel's box top (lower, under the sieve; its title moves left)
CARD = (12.7, 2.3, np.array([0.0, -2.35, 0.0]))   # the ponder card over the strip (w, h, centre)


def lay(ch: CacheChain, box_bottom: float, lift: float, gap: float) -> CacheChain:
    """Place a chain's parts: every box's bottom at `box_bottom` (x kept), each badge `lift` above
    its own box's lid, the dominoes in one row with tops `gap` under the boxes."""
    for b in ch.boxes:
        b.shift(UP * (box_bottom - b.frame.get_bottom()[1]))
    for b, bd in zip(ch.boxes, ch.badges):
        bd.move_to([b.get_center()[0], b.frame.get_top()[1] + lift, 0])
    for b, d in zip(ch.boxes, ch.dominoes):
        d.move_to([b.get_center()[0], box_bottom - gap - d.height / 2, 0])
    return ch


def mini_parcel(w: float = 2.1, h: float = 0.56) -> VGroup:
    """S06's build context as a small icon: a GREY box with PINK tape and six file glyphs. .frame .tape .files"""
    fr = box(w, h, LAPTOP, fill_opacity=0.1)
    tape = VGroup(Line(fr.get_corner(UL) + DOWN * 0.07, fr.get_corner(UR) + DOWN * 0.07, color=ROUTE, stroke_width=5),
                  Line(fr.get_corner(DL) + UP * 0.07, fr.get_corner(DR) + UP * 0.07, color=ROUTE, stroke_width=5))
    files = VGroup(*[file_glyph(0.22, LAPTOP) for _ in range(6)]).arrange(RIGHT, buff=0.1).move_to(fr)
    g = VGroup(fr, tape, files)
    g.frame, g.tape, g.files = fr, tape, files
    return g


def pulse(mob, color=None, scale: float = 1.08, run_time: float = 0.6, rate=there_and_back):
    """A pulse that recolours strokes only and comes back (Indicate would fill the chain's opaque
    boxes, badges and tags with its colour)."""
    a = mob.animate(rate_func=rate, run_time=run_time).scale(scale)
    return a.set_stroke(color) if color is not None else a


def unlight(p: Parcel, name: str, run_time: float = 0.4):
    """Animation: parcel item `name` back to its GREY glyph and white name."""
    it = p.items[name]
    fo = 0.35 if name.endswith("/") else 0.2
    return AnimationGroup(it.glyph.animate.set_stroke(S.GREY).set_fill(S.GREY, fo),
                          it.name_text.animate.set_color(INK), run_time=run_time)


def dockerignore_card(lines=(".git", ".venv", "secrets/"), size: float = 22) -> VGroup:
    """The .dockerignore file you'd add (S10's card, a little smaller to fit a fourth line): mono
    white header, GREEN lines. .frame .head .rows"""
    head = mono(".dockerignore", size, INK)
    rows = VGroup(*[mono(s, size, VENV) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    inner = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    fr = box(3.0, inner.height + 0.5 + 0.48, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(fr).align_to(fr, UL).shift(np.array([0.3, -0.25, 0]))
    g = VGroup(fr, inner)
    g.frame, g.head, g.rows = fr, head, rows
    return g


# ------------------------------------------------------------------ the scene
class LayerCache(VoiceScene):
    # ---- helpers that play
    def ponder_over(self, question: str, seconds: float) -> VGroup:
        """pause_and_ponder's card and draining timer, sized to cover the strip (the picture above it
        stays visible). Returns the card (removed at the start of the next block)."""
        w, h, c = CARD
        card = ponder_card(question, width=w)
        fr, head, q, bar = card
        fr.become(RoundedRectangle(width=w, height=h, corner_radius=0.2, stroke_color=TURN, stroke_width=3)
                  .set_fill(S.BG, 1).move_to(c))
        VGroup(head, q).move_to(fr).shift(UP * 0.12)
        bar.put_start_and_end_on(fr.get_corner(DL) + np.array([0.3, 0.25, 0]),
                                 fr.get_corner(DR) + np.array([-0.3, 0.25, 0]))
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=seconds)
        return card

    def fly(self, start, badge, color=ERR, run_time: float = 0.7, extra=()):
        """A fingerprint in `color` rises from `start` (a point or mobject) into `badge`, which takes
        its colour (the step's cache key changed)."""
        p0 = start if isinstance(start, np.ndarray) else start.get_center()
        fp = fingerprint(0.17, color).move_to(p0)
        self.play(FadeIn(fp, scale=0.4), *extra, run_time=0.25)
        self.play(fp.animate(path_arc=-0.6).move_to(badge), run_time=run_time)
        self.play(FadeOut(fp, scale=1.6), badge.animate.set_stroke(color),
                  Flash(badge, color=color, line_length=0.14, flash_radius=0.3), run_time=0.45)

    def swap(self, holder, top, old: VGroup, new: VGroup, extra=(), extra_mobs=(), run_time: float = 0.7) -> None:
        """Morph glyphs `old` (children of `holder`, inside `top`) into `new`, then make the new glyphs
        children of `holder`, so `top` fades and moves as one piece afterwards (`extra_mobs`: wrappers
        that the extra animations put on the scene, taken off again)."""
        old_list = list(old.submobjects)
        self.play(ReplacementTransform(old, new), *extra, run_time=run_time)
        holder.remove(*old_list)
        self.remove(new)
        holder.add(*new.submobjects)
        for m in extra_mobs:
            self.remove(m)
        self.add(top)

    def construct(self):
        assert len(SAY) == 8, f"S11 has {len(SAY)} SAY lines; this scene times 8"

        tr = tracker_a(16, extra=True)
        ch = CacheChain(STEPS4, box_h=0.9, domino_h=0.45)
        ch.set_x(0)
        lay(ch, BOTTOM_G, LIFT, GAP_G)
        feeds = [ch.feeds(i) for i in range(4)]
        parents = VGroup(*[feeds[i][0] for i in range(1, 4)])
        instrs = VGroup(*[f[-1] for f in feeds])
        b3 = ch.badges[2]
        mini = mini_parcel()
        mini.move_to([b3.get_center()[0], b3.get_top()[1] + 0.62 + mini.height / 2, 0])
        mini_t = label("build context", 20, ROUTE).next_to(mini, RIGHT, buff=0.25)
        feed_p = Arrow(mini.get_bottom(), b3.get_top(), buff=0.06, stroke_width=2.5, tip_length=0.12,
                       max_tip_length_to_length_ratio=0.35, color=IMAGE)
        run_txt = ch.boxes[1].text[1]                    # "RUN apt…uv"

        # ========================================================== 0 · the rule, concept first
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.4)
            self.play(LaggedStart(FadeIn(ch.boxes[2], shift=UP * 0.15), FadeIn(ch.boxes[3], shift=UP * 0.15),
                                  lag_ratio=0.3), run_time=0.8)
            vo.wait_until("rerun")
            self.play(*[pulse(ch.boxes[k], ERR, 1.08, 1.4, there_and_back_with_pause) for k in (2, 3)])
            vo.wait_until("Docker caches")
            self.play(LaggedStart(FadeIn(ch.boxes[0], shift=RIGHT * 0.2), FadeIn(ch.boxes[1], shift=RIGHT * 0.2),
                                  lag_ratio=0.35), run_time=0.7)
            vo.wait_until("every build step")
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.35) for d in ch.dominoes], lag_ratio=0.25),
                      run_time=1.0)
            vo.wait_until("its parent step")
            self.play(LaggedStart(*[GrowArrow(a) for a in parents], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("and its instruction")
            self.play(LaggedStart(*[GrowArrow(a) for a in instrs], lag_ratio=0.2),
                      LaggedStart(*[Indicate(b.text[-1], color=INK, scale_factor=1.12) for b in ch.boxes],
                                  lag_ratio=0.2), run_time=0.9)
            vo.wait_until("are unchanged")
            merge = []
            for i in range(4):
                c = ch.badges[i].get_center()
                merge += [FadeOut(a, target_position=c, scale=0.2) for a in feeds[i]]
            self.play(*merge, LaggedStart(*[FadeIn(bd, scale=0.3) for bd in ch.badges], lag_ratio=0.15),
                      run_time=0.9)
            self.add(ch)
            vo.wait_until("For COPY")
            self.play(FadeIn(mini, shift=DOWN * 0.3), FadeIn(mini_t, shift=DOWN * 0.3), run_time=0.6)
            vo.wait_until("the checksum")
            self.play(GrowArrow(feed_p), Indicate(mini.files, color=INK, scale_factor=1.15), run_time=0.6)
            vo.wait_until("must match too")
            self.play(pulse(b3, INK, 1.5, 0.7), Indicate(feed_p, color=IMAGE), run_time=0.7)
            vo.wait_until("The first step that changes")
            self.play(run_txt.animate.set_color(TURN), Wiggle(run_txt, scale_value=1.15), run_time=0.6)
            self.play(ch.badge(1, ERR), Flash(ch.badges[1], color=ERR, line_length=0.14, flash_radius=0.3),
                      run_time=0.45)
            vo.wait_until("runs again")
            self.play(ch.topple(1, 1), run_time=0.5)
            vo.wait_until("every step after it")
            self.play(ch.topple(2, 3), run_time=0.85)
            self.wait(0.2)
            self.play(ch.stand_up(), ch.badge(1, IMAGE), run_txt.animate.set_color(INK), run_time=0.5)

        # ========================================================== 1 · rebuild, nothing changed: all CACHED
        t = laptop_term(8)
        ch.generate_target()
        lay(ch.target, BOTTOM_C, LID, GAP_C)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(mini, mini_t, feed_p), shift=UP * 0.2), MoveToTarget(ch), FadeIn(t),
                      run_time=0.8)
            bare_prompt(self, t)
            c1 = type_cmd(self, t, BUILD_PLAIN, 1.5)
            r1a, r1b = c1.rows
            pin(self, r1a, beside(row_tag("extra · full log"), r1a), run_time=0.3)
            vo.wait_until("the extra flag")
            g_flag = substring(r1b, "--progress=plain")
            u_flag = under(g_flag, TURN, y=r1b.strut.get_bottom()[1] - 0.01)
            self.play(Create(u_flag), Indicate(g_flag, color=TURN, scale_factor=1.12), run_time=0.6)
            attach(self, r1b, u_flag)
            o1 = t.print(self, OUT38, run_time=0.7, lag=0.12)
            vo.wait_until("FROM reuses")
            s0 = ch.stamp(0, "reused")
            self.play(FadeIn(s0, scale=1.4), pulse(ch.boxes[0], IMAGE, 1.05, 0.5))
            vo.wait_until("and the three steps")
            cached = [substring(o1[k], "CACHED") for k in (1, 3, 5)]
            stamps = [ch.stamp(k) for k in (1, 2, 3)]
            self.play(LaggedStart(*[AnimationGroup(g.animate.set_color(IMAGE), FadeIn(s, scale=1.4))
                                    for g, s in zip(cached, stamps)], lag_ratio=0.5), run_time=1.6)
            vo.wait_until("nothing runs")
            self.play(pulse(VGroup(*ch.dominoes), INK, 1.1, 0.7))

        # ========================================================== 2 · predict (ponder)
        parcel = Parcel(NAMES, extra=0)
        panel = code("cli.py", 49)
        src = panel.code
        gap = 0.35
        left = -(panel.width + gap + parcel.width) / 2
        parcel.shift(np.array([left + panel.width + gap - parcel.get_left()[0], PARCEL_TOP - parcel.get_top()[1], 0]))
        panel.shift(np.array([left - panel.get_left()[0], parcel.frame.get_center()[1] - src.get_center()[1], 0]))
        bar49 = line_bar(src, 0, TURN, 0.18)
        seed = mini_parcel().move_to([ch.boxes[2].get_center()[0], parcel.frame.get_center()[1], 0])
        names = VGroup(*[it.name_text for it in parcel.items.values()])
        glyphs = VGroup(*[it.glyph for it in parcel.items.values()])

        with self.voiceover(SAY[2]) as vo:
            resize(self, t, STRIP_ROWS, run_time=0.7)
            vo.wait_until("You change one word")
            self.play(FadeIn(seed, scale=0.6), run_time=0.4)
            self.play(ReplacementTransform(seed.frame, parcel.frame), ReplacementTransform(seed.tape, parcel.tape),
                      FadeTransform(seed.files, glyphs), run_time=0.7)
            self.play(FadeIn(names), FadeIn(parcel.title, shift=DOWN * 0.1), run_time=0.4)
            self.add(parcel)
            vo.wait_until("in cli.py")
            self.play(parcel.light("cli.py", TURN), run_time=0.4)
            self.play(FadeIn(panel, shift=RIGHT * 0.3), run_time=0.5)
            self.play(FadeIn(bar49), Indicate(parcel.items["cli.py"], color=TURN, scale_factor=1.15), run_time=0.5)
            panel.add(bar49)                             # the bar moves and fades with the panel
            vo.wait_until("Which of the four")
            self.play(LaggedStart(*[pulse(b, TURN, 1.08) for b in ch.boxes], lag_ratio=0.3), run_time=1.4)
        card = self.ponder_over(PONDER_Q, 8)

        # ========================================================== 3 · cheese -> brie, git diff
        line = src.code_lines[0]
        alt = code_panel(BRIE49, "cli.py", 49, "python")
        alt.shift(line[0].get_center() - alt.code.code_lines[0][0].get_center())
        g_cheese = code_span(src, 0, "cheese")
        cheese_back = g_cheese.copy()
        g_tail = code_span(src, 0, '",')
        tail_home = g_tail.get_center().copy()
        g_brie = code_span(alt.code, 0, "brie").copy().set_color(TURN)
        tail_brie = code_span(alt.code, 0, '",').get_center()

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            vo.wait_until("on line 49")
            self.play(Indicate(panel.header, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("I love cheese to")
            self.swap(line, panel, g_cheese, g_brie, extra=[g_tail.animate.move_to(tail_brie)], extra_mobs=[g_tail],
                      run_time=0.8)
            u_brie = under(g_brie, TURN, y=g_brie.get_bottom()[1] - 0.08)
            self.play(Create(u_brie), Indicate(g_brie, color=TURN, scale_factor=1.2), run_time=0.5)
            panel.add(u_brie)
            vo.wait_until("The git diff")
            c3 = type_cmd(self, t, GIT_DIFF, 0.4)
            pin(self, c3, beside(row_tag("extra"), c3), run_time=0.25)
            t.print(self, [(DIFF[0], ERR), (DIFF[1], VENV)], run_time=0.4, lag=0.2)
            vo.wait_until("the build context now")
            self.play(Indicate(parcel.title, color=ROUTE, scale_factor=1.2),
                      Indicate(parcel.frame, color=ROUTE, scale_factor=1.03), run_time=0.6)
            vo.wait_until("a different checksum")
            self.fly(parcel.items["cli.py"].glyph, ch.badges[2])

        # ========================================================== 4 · rebuild: COPY and uv sync rerun
        b4 = ch.boxes[3]
        dl = Arrow([6.45, b4.get_center()[1], 0], [b4.frame.get_right()[0] + 0.06, b4.get_center()[1], 0], buff=0,
                   color=TOOL, stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.2)
        dl_t = mono("35.9 MiB", 20, TOOL).next_to(dl, UP, buff=0.1)
        picture = VGroup(parcel, panel)

        with self.voiceover(SAY[4]) as vo:
            resize(self, t, 8, extra=[FadeOut(picture)], run_time=0.6)
            c4 = type_cmd(self, t, BUILD_PLAIN, 1.1)
            pin(self, c4.rows[0], beside(row_tag("extra"), c4.rows[0]), run_time=0.25)
            vo.wait_until("FROM and the apt")
            o4a = t.print(self, OUT40_A, run_time=0.4, lag=0.2)
            self.play(substring(o4a[1], "CACHED").animate.set_color(IMAGE),
                      *[pulse(ch.stamps[k], IMAGE, 1.15) for k in (0, 1)], run_time=0.6)
            vo.wait_until("But the checksum")
            self.play(pulse(ch.badges[2], ERR, 1.6, 0.7))
            vo.wait_until("so COPY runs")
            o4b = t.print(self, OUT40_B, run_time=0.3, lag=0.2)
            self.play(ch.topple(2, 2), FadeOut(ch.stamps.pop(2), shift=DOWN * 0.3),
                      Indicate(substring(o4b[1], "DONE"), color=INK, scale_factor=1.2), run_time=0.5)
            vo.wait_until("and uv sync after it")
            o4c = t.print(self, OUT40_C, run_time=0.35, lag=0.2, wrap=True)
            self.play(ch.topple(3, 3), FadeOut(ch.stamps.pop(3), shift=DOWN * 0.3), run_time=0.5)
            vo.wait_until("Python download")
            r_mib = o4c[-1]
            assert r_mib.text.startswith("35.9MiB"), r_mib.text
            g_mib = substring(r_mib, "35.9MiB")
            u_mib = under(g_mib, TOOL, y=r_mib.strut.get_bottom()[1] - 0.01)
            self.play(GrowArrow(dl), FadeIn(dl_t, shift=LEFT * 0.2), Create(u_mib), g_mib.animate.set_color(TOOL),
                      run_time=0.5)
            attach(self, r_mib, u_mib)
            self.play(pulse(b4, TOOL, 1.06, 0.5))
            t.print(self, OUT40_D, run_time=0.3, lag=0.2)

        # ========================================================== 5 · git checkout: the cache still doesn't come back
        with self.voiceover(SAY[5]) as vo:
            resize(self, t, STRIP_ROWS, extra=[ch.stand_up(), FadeOut(VGroup(dl, dl_t))], run_time=0.7)
            self.play(FadeIn(picture, shift=UP * 0.1), run_time=0.4)
            c5 = type_cmd(self, t, GIT_CHECKOUT, 0.6)
            pin(self, c5, beside(row_tag("extra"), c5), run_time=0.25)
            bare_prompt(self, t)
            panel.remove(u_brie)
            self.swap(line, panel, g_brie, cheese_back, extra=[g_tail.animate.move_to(tail_home), FadeOut(u_brie),
                                                                unlight(parcel, "cli.py")], extra_mobs=[g_tail], run_time=0.7)
            vo.wait_until("Same files")
            self.play(pulse(ch.badges[2], IMAGE, 1.5, 0.7))           # the hoped-for match flickers, stays RED
            resize(self, t, 8, extra=[FadeOut(picture)], run_time=0.6)
            c5b = type_cmd(self, t, BUILD_PLAIN, 1.0)
            pin(self, c5b.rows[0], beside(row_tag("extra"), c5b.rows[0]), run_time=0.25)
            vo.wait_until("No: COPY")
            o5 = t.print(self, OUT41, run_time=0.5, lag=0.15, wrap=True)
            self.play(ch.topple(2, 3), Wiggle(ch.badges[2], scale_value=1.3), run_time=0.85)
            vo.wait_until("Git rewrote")
            resize(self, t, STRIP_ROWS, keep=[o5[0], o5[1], o5[2]], run_time=0.6)
            self.play(FadeIn(parcel, shift=UP * 0.1), run_time=0.4)
            self.play(parcel.light(".git/index", TURN), run_time=0.4)
            self.play(Indicate(parcel.items[".git/index"], color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("inside the hidden git folder")
            self.play(Indicate(parcel.items[".git/"], color=TURN, scale_factor=1.25), run_time=0.7)
            vo.wait_until("and that folder")
            self.play(Indicate(parcel.title, color=ROUTE, scale_factor=1.2),
                      Indicate(parcel.frame, color=ROUTE, scale_factor=1.03), run_time=0.6)
            self.fly(parcel.items[".git/index"].glyph, ch.badges[2])

        # ========================================================== 6 · that was part 1's question
        caption = label("Dockerfile steps 4 and 5: every edit to the Dockerfile changed the parcel", 22, S.GREY)
        caption.move_to([0, parcel.get_bottom()[1] - 0.55, 0]).align_to(parcel.frame, RIGHT)
        err = erratum_tag("erratum · expected while learning").next_to(caption, DOWN, buff=0.35)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(t), ch.stand_up(), unlight(parcel, ".git/index"), run_time=0.6)
            self.play(LaggedStart(*[pulse(ch.boxes[k], INK, 1.08) for k in (2, 3)],
                                  lag_ratio=0.3), run_time=0.9)
            vo.wait_until("Your Dockerfile")
            self.play(parcel.light("Dockerfile", TURN), run_time=0.4)
            self.play(Indicate(parcel.items["Dockerfile"], color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("so every edit")
            self.fly(parcel.items["Dockerfile"].glyph, ch.badges[2])
            self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("While you follow")
            self.play(FadeIn(err, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("that's expected")
            self.play(pulse(err, None, 1.1, 0.6))

        # ========================================================== 7 · the pattern for your own projects
        # the picture settles lower (room for the tag on top and the sieve under the chain)
        dy7 = FRAME_TOP_7 - parcel.frame.get_top()[1]
        pf = parcel.frame.copy().shift(UP * dy7)
        pattern = stand_in_tag("a pattern for your own projects", "not the course solution")
        pattern.move_to([6.45 - pattern.width / 2, 3.45 - pattern.height / 2, 0])
        five = CacheChain(STEPS5, box_h=0.9, domino_h=0.45, gap=0.3)
        five.set_x(0)
        lay(five, BOTTOM_5, LID, GAP_C)
        sieve = Sieve(pf.width, 0.8, color=S.GREY)
        sieve.title.set_opacity(0)                       # the card names the file
        sieve.move_to([pf.get_center()[0], pf.get_top()[1] + 0.25 + sieve.frame.height / 2, 0])
        sieve.title.next_to(sieve.frame, UP, buff=0.1).align_to(sieve.frame, LEFT)
        di = dockerignore_card()
        di.move_to([-6.35 + di.width / 2, sieve.frame.get_top()[1] - di.height / 2, 0])
        new_row = mono("Dockerfile", 22, TURN).next_to(di.rows, DOWN, buff=0.16, aligned_edge=LEFT)
        di_tag = illustration_tag("illustration · a file you'd add").next_to(di, DOWN, buff=0.22).align_to(di, LEFT)
        foot = label("full Dockerfile: exercises.md", 20, S.GREY)
        foot.move_to([pf.get_right()[0] - foot.width / 2, di_tag.get_center()[1], 0])
        catch_y = sieve.frame.get_center()[1]
        mapping = {0: 0, 1: 1, 2: 4, 3: 3}

        def catch(name):
            """Animation: parcel item `name` rises into the sieve and stays there, GREY."""
            it = parcel.items[name]
            self.bring_to_front(it)
            return it.animate.shift(UP * (catch_y - it.get_center()[1])).set_color(S.GREY)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(caption, err)), FadeOut(VGroup(*ch.stamps.values())), ch.badge(2, IMAGE),
                      unlight(parcel, "Dockerfile"), run_time=0.5)
            ch.stamps.clear()
            ch.generate_target()
            lay(ch.target, BOTTOM_5, LID, GAP_C)
            parcel.generate_target()
            parcel.target.shift(UP * dy7)
            parcel.target.title.next_to(parcel.target.frame, LEFT, buff=0.3)
            self.play(MoveToTarget(ch), MoveToTarget(parcel), run_time=0.6)
            self.play(FadeIn(pattern, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("put the slow steps first")
            self.play(pulse(ch.boxes[3], TURN, 1.08, 0.8))
            vo.wait_until("copy only the files")
            # COPY . ./ steps out of the row; the others take their five-step places
            cp = VGroup(ch.boxes[2], ch.badges[2], ch.dominoes[2])
            self.play(*[Transform(part[i], fpart[mapping[i]]) for i in (0, 1, 3)
                        for part, fpart in ((ch.boxes, five.boxes), (ch.badges, five.badges),
                                            (ch.dominoes, five.dominoes))],
                      cp.animate.shift(DOWN * DIP), run_time=0.8)
            # the small COPY of the files uv sync needs splits off it, left of RUN uv sync
            self.play(GrowFromPoint(five.boxes[2], ch.boxes[2].get_center()), FadeIn(five.badges[2], scale=0.3),
                      run_time=0.6)
            vo.wait_until("run it,")
            self.play(pulse(five.boxes[3], TURN, 1.08))
            vo.wait_until("then copy the rest")
            # the rest of the COPY goes to the end of the row, under uv sync; a fifth domino stands up
            self.play(Transform(ch.boxes[2], five.boxes[4]), Transform(ch.badges[2], five.badges[4]),
                      Transform(ch.dominoes[2], five.dominoes[4]), run_time=1.0)
            self.play(GrowFromEdge(five.dominoes[2], DOWN), run_time=0.4)
            self.remove(*ch.get_family())                # also splits the wrappers (cp, the dominoes) holding them
            self.add(five)
            vo.wait_until("A dockerignore")
            self.play(FadeIn(di, shift=RIGHT * 0.2), FadeIn(di_tag, shift=RIGHT * 0.2), FadeIn(sieve, shift=DOWN * 0.2),
                      run_time=0.6)
            self.play(sieve.solidify(VENV), run_time=0.5)
            self.play(sieve.mesh.animate.set_stroke(opacity=0.4), run_time=0.2)
            vo.wait_until("the git folder")
            self.play(catch(".git/"), catch(".git/index"), run_time=0.6)
            vo.wait_until("any local venv")
            self.play(Indicate(di.rows[1], color=VENV, scale_factor=1.25), run_time=0.6)
            vo.wait_until("and the Dockerfile")
            self.play(FadeIn(new_row, shift=LEFT * 0.4), run_time=0.4)
            self.play(catch("Dockerfile"), run_time=0.6)
            vo.wait_until("Now an edit")
            self.play(parcel.light("cli.py", TURN), run_time=0.4)
            self.fly(parcel.items["cli.py"].glyph, five.badges[4], run_time=0.8)
            vo.wait_until("reruns only the last")
            st = [five.stamp(0, "reused")] + [five.stamp(k) for k in (1, 2, 3)]
            self.play(five.topple(4, 4), LaggedStart(*[FadeIn(s, scale=1.4) for s in st], lag_ratio=0.15),
                      run_time=0.9)
            self.play(pulse(st[3], IMAGE, 1.2))
            self.play(FadeIn(foot, shift=UP * 0.1), run_time=0.4)

        self.wait(0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
