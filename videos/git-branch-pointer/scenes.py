"""Why is a git branch almost free? — Swiss scenes.

Narration and exact budgets come from plan.json. The visual vocabulary is the shared
swiss style contract; the commit-graph pieces (nodes, parent arrows, branch tags) are
this episode's own teaching diagrams. All content stays above y = -2.45 so the reserved
caption band (bottom 170 px) stays clear — the style check measures this.
"""
import json
import os
from pathlib import Path
from manim import *
from explainer.scene import VoiceScene
from explainer.styles import swiss
from explainer.styles.swiss import (PAPER, INK, RED, GRAY, FAINT,
                                    label, at, left, line, card, folder, arrow)

swiss.setup_fonts()
config.background_color = PAPER

MONO = "DejaVu Sans Mono"
SHA_MAIN = "88adfade790f726ed5b1b0941043708ec9fed18e"   # real: origin/main after PR #10
SHA_PARENT_A = "6b697f98b7542e44977b14f6fcb6da363863998d"  # real parents of that merge
SHA_PARENT_B = "7548c0756c4dba2879c04f2ef6c0373016097684"


def mono(s, size=26, color=INK):
    return Text(s, font=MONO, font_size=size, color=color)


def commit_node(name, x, y, accent=False):
    """A commit: a small plate carrying its abbreviated name."""
    plate = RoundedRectangle(corner_radius=0.08, width=1.18, height=0.72,
                             stroke_color=RED if accent else INK, stroke_width=2,
                             fill_color=PAPER, fill_opacity=1).move_to([x, y, 0])
    tag = Text(name, font=MONO, font_size=22, color=RED if accent else INK).move_to([x, y, 0])
    return VGroup(plate, tag)


def parent_arrow(child, parent, color=GRAY):
    """Child commits point at their parents (left)."""
    return Arrow(child.get_left(), parent.get_right(), buff=.08, color=color,
                 stroke_width=3, max_tip_length_to_length_ratio=.18)


def branch_tag(name, node, dy=1.05, color=RED, head=False, x_off=0.0):
    """A branch is a pointer: a small label with an arrow down to its commit. `x_off`
    shifts the label sideways (diagonal arrow) so stacked tags never cross each other."""
    x, y = node.get_center()[0], node.get_top()[1]
    anchor = y if dy > 0 else node.get_bottom()[1]
    box = Rectangle(width=max(1.1, .32 * len(name) + .4), height=.52, stroke_color=color,
                    stroke_width=2, fill_color=PAPER, fill_opacity=1)\
        .move_to([x + x_off, anchor + dy, 0])
    start = box.get_bottom() if dy > 0 else box.get_top()
    end = [x, y + .06, 0] if dy > 0 else [x, node.get_bottom()[1] - .06, 0]
    text = Text(name, font=MONO, font_size=24, color=color).move_to(box.get_center())
    tip = Arrow(start, end, buff=.04, color=color, stroke_width=3,
                max_tip_length_to_length_ratio=.3)
    group = VGroup(box, text, tip)
    if head:
        ring = SurroundingRectangle(box, color=INK, stroke_width=2, buff=.09)
        head_label = Text("HEAD", font=MONO, font_size=18, color=INK)\
            .next_to(ring, UP, buff=.08)
        group.add(ring, head_label)
    return group


def ponder(zh, en, y=-1.1):
    """A pause-and-ponder card: the episode's thinking beats."""
    frame = Rectangle(width=9.4, height=1.9, stroke_color=RED, stroke_width=3,
                      fill_color=PAPER, fill_opacity=1).move_to([0, y, 0])
    q = at("想一想 / PAUSE AND PONDER", 0, y + .55, 22, RED, bold=True)
    z = at(zh, 0, y + .08, 30, INK, 8.8)
    e = at(en, 0, y - .5, 24, GRAY, 8.8)
    return VGroup(frame, q, z, e)


class EpisodeScene(VoiceScene):
    pad_after_clip = .18
    total = "07"

    def setup(self):
        super().setup()
        self.camera.background_color = PAPER
        plan = json.loads(Path(os.environ["EPISODE_PLAN"]).read_text())
        self.spec = next(s for s in plan["scenes"] if s["id"].upper() == self.__class__.__name__)

    def header(self, name):
        ident = self.spec["id"][1:]
        self.add(line(-6.3, 3.42, 6.3, 3.42),
                 left("CONNY / EXPLAINER STUDIES", -6.3, 3.67, 15),
                 at(f"{ident} / {self.total}", 5.85, 3.67, 16, RED))
        self.play(FadeIn(left(name, -6.3, 2.85, 44, INK, 12.5, True), shift=UP * .10), run_time=.4)
        self.add(left(self.spec["title_zh"], -6.3, 2.34, 21, GRAY))

    def say(self, i):
        return self.voiceover(self.spec["lines"][i]["en"])

    def cue(self, vo, f, *anims, run_time=.65):
        delay = vo.duration * f - vo.elapsed
        if delay > .04:
            self.wait(delay)
        self.play(*anims, run_time=run_time)

    def finish(self):
        remaining = self.spec["duration"] - self.renderer.time
        if remaining > .37:
            self.wait(remaining - .30)
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.30)
        elif remaining > .015:
            self.wait(remaining)


class S01(EpisodeScene):
    def construct(self):
        self.header("One command, no copy")
        repo = folder("Explainer_Videos/", -3.6, .8, 4.4)
        size = at("0.5 GB of history", -3.6, -.15, 24, GRAY)
        with self.say(0) as vo:
            self.cue(vo, .12, FadeIn(repo, shift=UP * .1), FadeIn(size))
            cmd = Rectangle(width=5.6, height=.9, stroke_color=INK, stroke_width=2,
                            fill_color=PAPER, fill_opacity=1).move_to([3.1, .8, 0])
            cmdtext = mono("$ git branch idea", 30).move_to(cmd.get_center())
            vo.wait_until("create a branch")
            self.play(Create(cmd), Write(cmdtext), run_time=.8)
        with self.say(1) as vo:
            done = at("done.", 3.1, -.15, 34, RED, bold=True)
            self.cue(vo, .08, FadeIn(done))
            ghost = folder("copy of everything?", -3.6, -1.6, 4.4, color=GRAY)
            ghost.set_opacity(.35)
            vo.wait_until("copied the project")
            cross = line(-5.5, -2.1, -1.7, -1.1, RED, 5)
            self.play(FadeIn(ghost), run_time=.5)
            self.play(Create(cross), run_time=.5)
        with self.say(2) as vo:
            dim = VGroup(*[m for m in self.mobjects if isinstance(m, VMobject)])
            self.cue(vo, .2, dim.animate.set_opacity(.15), run_time=.6)
            self.play(FadeIn(ponder("git 最少要记下什么，才能记住一个分支？",
                                    "What is the smallest thing git could store?", y=-1.55),
                             shift=UP * .1), run_time=.5)
        self.finish()


class S02(EpisodeScene):
    def construct(self):
        self.header("The whole branch is 41 bytes")
        with self.say(0) as vo:
            tree = VGroup(
                left(".git/", -5.9, 1.3, 30, INK),
                left("refs/", -5.3, .75, 30, INK),
                left("heads/", -4.7, .2, 30, INK),
                left("idea", -4.1, -.35, 32, RED, bold=True),
            )
            rails = VGroup(line(-5.75, 1.1, -5.75, -.35, FAINT), line(-5.15, .55, -5.15, -.35, FAINT),
                           line(-4.55, 0, -4.55, -.35, FAINT))
            self.cue(vo, .3, FadeIn(rails), *[FadeIn(t, shift=RIGHT * .1) for t in tree], run_time=1.0)
        with self.say(1) as vo:
            file_card = Rectangle(width=8.2, height=1.5, stroke_color=INK, stroke_width=2,
                                  fill_color=PAPER, fill_opacity=1).move_to([2.0, .55, 0])
            sha = mono(SHA_MAIN, 24)
            if sha.width > 7.0:
                sha.scale_to_fit_width(7.0)
            sha.move_to(file_card.get_center() + UP * .25 + LEFT * .3)
            nl = mono("\\n", 24, GRAY).next_to(sha, RIGHT, buff=.12)
            self.cue(vo, .05, Create(file_card), run_time=.5)
            self.play(Write(sha), FadeIn(nl), run_time=1.2)
            brace_chars = line(-1.75, .05, 5.25, .05, RED, 3)
            n40 = at("40 characters", 1.3, -.35, 26, RED)
            n1 = at("+ 1 newline", 5.2, -.35, 26, GRAY)
            vo.wait_until("Forty-one bytes")
            big = at("41 bytes", 2.0, 1.7, 56, RED, bold=True)
            self.play(FadeIn(big, shift=UP * .1), run_time=.6)
            self.play(Create(brace_chars), FadeIn(n40), FadeIn(n1), run_time=.8)
        with self.say(2) as vo:
            msg = at("复制了 0 个文件 · zero files copied", .9, -1.5, 30, INK, bold=True)
            self.cue(vo, .3, FadeIn(msg))
        self.finish()


class S03(EpisodeScene):
    def construct(self):
        self.header("Commits are the real graph")
        xs = [-4.2, -1.4, 1.4]
        nodes = [commit_node(n, x, -.3) for n, x in zip(["a1f3c2", "5d08b7", "c99e41"], xs)]
        snaps = [card("snapshot", "all your files", x, 1.3, 2.4, 1.2) for x in xs]
        with self.say(0) as vo:
            self.cue(vo, .12, FadeIn(nodes[0], shift=UP * .1))
            vo.wait_until("snapshot of your files")
            self.play(FadeIn(snaps[0], shift=DOWN * .1),
                      Create(line(xs[0], .7, xs[0], .1, FAINT)), run_time=.7)
            vo.wait_until("name of its parent")
            self.play(FadeIn(nodes[1]), FadeIn(snaps[1], shift=DOWN * .1),
                      Create(line(xs[1], .7, xs[1], .1, FAINT)), run_time=.6)
            self.play(Create(parent_arrow(nodes[1], nodes[0])), run_time=.6)
        with self.say(1) as vo:
            self.cue(vo, .1, FadeIn(nodes[2]), FadeIn(snaps[2], shift=DOWN * .1),
                     Create(line(xs[2], .7, xs[2], .1, FAINT)))
            self.play(Create(parent_arrow(nodes[2], nodes[1])), run_time=.6)
            every = at("每个版本都在图里 · every version lives here", -1.4, -1.5, 26, GRAY)
            vo.wait_until("every version")
            self.play(FadeIn(every), run_time=.5)
        with self.say(2) as vo:
            tag = branch_tag("idea", nodes[2], dy=-.95)
            tag.shift(DOWN * .9 + RIGHT * 2.6)
            target = branch_tag("idea", nodes[2], dy=-.95)
            note = at("只是指过去 · just points", 4.3, -.3, 24, RED)
            self.cue(vo, .2, FadeIn(tag))
            vo.wait_until("points at one node")
            self.play(Transform(tag, target), FadeIn(note), run_time=.9)
        self.finish()


class S04(EpisodeScene):
    def construct(self):
        self.header("Committing moves one pointer")
        xs = [-4.6, -2.0, .6]
        nodes = [commit_node(n, x, -.55) for n, x in zip(["a1f3c2", "5d08b7", "c99e41"], xs)]
        arrows = [parent_arrow(nodes[1], nodes[0]), parent_arrow(nodes[2], nodes[1])]
        main_tag = branch_tag("main", nodes[2], dy=1.0, color=GRAY)
        idea_tag = branch_tag("idea", nodes[2], dy=1.75, head=True, x_off=1.9)
        with self.say(0) as vo:
            self.add(*nodes, *arrows)
            self.cue(vo, .1, FadeIn(main_tag), FadeIn(idea_tag))
            vo.wait_until("remembers that")
            self.play(Indicate(idea_tag[3], color=INK, scale_factor=1.15), run_time=.8)
        with self.say(1) as vo:
            new = commit_node("f7d2a9", 3.2, -.55, accent=True)
            vo.wait_until("stores the new snapshot")
            self.play(FadeIn(new, shift=UP * .12), run_time=.5)
            vo.wait_until("records its parent")
            self.play(Create(parent_arrow(new, nodes[2], color=RED)), run_time=.6)
            vo.wait_until("moves exactly one pointer")
            self.play(Transform(idea_tag, branch_tag("idea", new, dy=2.0, head=True)), run_time=1.0)
        with self.say(2) as vo:
            self.cue(vo, .1, Indicate(main_tag, color=GRAY, scale_factor=1.06), run_time=.8)
            f1 = mono("heads/main: c99e41…", 22, GRAY).move_to([-3.4, -1.95, 0])
            f2 = mono("heads/idea: f7d2a9…", 22, RED).move_to([1.6, -1.95, 0])
            vo.wait_until("two small files")
            self.play(FadeIn(f1), FadeIn(f2), run_time=.6)
        with self.say(3) as vo:
            dim = VGroup(*[m for m in self.mobjects if isinstance(m, VMobject)])
            over = ponder("「在某个分支上」到底是什么意思？",
                          "If a branch is a pointer, what does 'being on it' mean?", y=-1.0)
            self.cue(vo, .2, dim.animate.set_opacity(.15), run_time=.6)
            self.play(FadeIn(over, shift=UP * .1), run_time=.5)
        self.finish()


class S05(EpisodeScene):
    def construct(self):
        self.header("Switching is moving HEAD")
        xs = [-3.4, -.8]
        c3 = commit_node("c99e41", xs[0], -.4)
        c4 = commit_node("f7d2a9", xs[1], -.4, accent=True)
        pa = parent_arrow(c4, c3)
        main_tag = branch_tag("main", c3, dy=1.0, color=GRAY)
        idea_tag = branch_tag("idea", c4, dy=1.0, head=True)
        self.add(c3, c4, pa, main_tag, idea_tag)
        with self.say(0) as vo:
            cmd = mono("$ git switch main", 26).move_to([3.6, 1.6, 0])
            self.cue(vo, .05, FadeIn(cmd))
            vo.wait_until("moves HEAD back")
            self.play(Transform(idea_tag, branch_tag("idea", c4, dy=1.0)),
                      Transform(main_tag, branch_tag("main", c3, dy=1.0, color=GRAY, head=True)),
                      run_time=1.0)
            wd = folder("working folder", 3.6, -.6, 3.6)
            vo.wait_until("rebuilds your working folder")
            self.play(FadeIn(wd, shift=UP * .1), Indicate(c3, color=GRAY), run_time=.8)
        with self.say(1) as vo:
            keep = at("idea 还在：41 字节原封不动", -2.0, -1.9, 28, INK)
            self.cue(vo, .25, FadeIn(keep), Indicate(idea_tag, color=RED, scale_factor=1.08))
        self.finish()


class S06(EpisodeScene):
    def construct(self):
        self.header("A merge is one commit with two parents")
        base = commit_node("c99e41", -4.6, 0.0)
        m1 = commit_node("2b61e0", -2.2, .85)
        i1 = commit_node("f7d2a9", -2.2, -.95, accent=True)
        a1 = parent_arrow(m1, base)
        a2 = parent_arrow(i1, base)
        main_tag = branch_tag("main", m1, dy=.95, color=GRAY, head=True)
        idea_tag = branch_tag("idea", i1, dy=-.85)
        self.add(base, m1, i1, a1, a2, main_tag, idea_tag)
        with self.say(0) as vo:
            merge = commit_node("88adfa", .4, 0.0, accent=True)
            vo.wait_until("one new commit")
            self.play(FadeIn(merge, shift=UP * .12), run_time=.5)
            vo.wait_until("from main")
            self.play(Create(parent_arrow(merge, m1, color=GRAY)), run_time=.55)
            vo.wait_until("from idea")
            self.play(Create(parent_arrow(merge, i1, color=RED)), run_time=.55)
            self.play(Transform(main_tag, branch_tag("main", merge, dy=1.5, color=GRAY, head=True)),
                      run_time=.8)
        with self.say(1) as vo:
            proof = VGroup(
                mono("$ git cat-file commit 88adfa…", 21, GRAY),
                mono(f"tree 5478920…", 21, INK),
                mono(f"parent {SHA_PARENT_A[:12]}…", 21, INK),
                mono(f"parent {SHA_PARENT_B[:12]}…", 21, RED),
            ).arrange(DOWN, aligned_edge=LEFT, buff=.14).move_to([4.0, -.35, 0])
            box = SurroundingRectangle(proof, color=INK, stroke_width=2, buff=.22)
            real = at("本仓库的真实提交 · real commit, this repo", 4.0, .95, 20, GRAY)
            self.cue(vo, .15, Create(box), FadeIn(proof), FadeIn(real), run_time=1.0)
        with self.say(2) as vo:
            vo.wait_until("one node")
            self.play(Indicate(VGroup(base, m1, i1), color=GRAY, scale_factor=1.03), run_time=.8)
        self.finish()


class S07(EpisodeScene):
    def construct(self):
        self.header("Recap: pointers all the way")
        cards = VGroup(
            card("41 bytes", "a branch = a pointer", -4.2, .7, 3.8, 1.7, accent=True),
            card("the graph", "commits + parents", 0, .7, 3.8, 1.7),
            card("merge", "one commit, 2 parents", 4.2, .7, 3.8, 1.7),
        )
        with self.say(0) as vo:
            self.cue(vo, .1, FadeIn(cards[0], shift=UP * .1))
            vo.wait_until("real graph")
            self.play(FadeIn(cards[1], shift=UP * .1), run_time=.5)
        with self.say(1) as vo:
            arrow_demo = arrow([-1.2, -.7, 0], [.4, -.7, 0])
            self.cue(vo, .1, Create(arrow_demo))
            vo.wait_until("two parents")
            self.play(FadeIn(cards[2], shift=UP * .1), run_time=.5)
        with self.say(2) as vo:
            do_it = Rectangle(width=9.8, height=1.1, stroke_color=RED, stroke_width=3,
                              fill_color=PAPER, fill_opacity=1).move_to([0, -1.7, 0])
            path = mono(".git/refs/heads/<your-branch>", 28, RED).move_to(do_it.get_center())
            vo.wait_until("your own eyes")
            self.play(Create(do_it), Write(path), run_time=1.0)
        self.finish()
