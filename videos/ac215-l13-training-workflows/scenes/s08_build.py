"""S08 · The cockpit that won't build: two one-line fixes — tracker D1 → D2 (+ rows fix 1, fix 2), lecture_ref 24.

Beats (script.md, ## S08; one voiceover block each):
0. V1 (MAP_AT S08): cockpit → bucket → Vertex AI flash on the three spoken stages, then dim; tracker D1,
   lref 24, GREY chip "the build itself is tutorial-only" under the cockpit. Laptop terminal (~) with
   "same terminal as your export · new terminal? export again first": cd model-training. README card
   93–94 (the README's own [REPLACE …] notes) + "replace this with yours" ×2 + "project ID, not its
   name · keep gs://". The card leaves, the terminal grows; the sed of 20 (soft-wrapped; editor chip,
   GNU/macOS) → 20:2–6, lines 5–6 GREEN; ▶ your turn.
1. A kind card tagged erratum: README cards 100–101 and 110, chip "the README's listing is not the
   file · edit docker-shell.sh itself". Then CODE(docker-shell.sh: 13–24): 14 YELLOW, 17 GREY, 18–19
   TEAL with two GREY → TEAL notes under the panel ("your code → /app", "secrets → /secrets"), the four
   -e lines one note, "no -p · it serves nothing" on the docker run line.
2. D2: README card 114–115; sh docker-shell.sh, ▶ your turn → 21: 23, …, 65–70 (RED), …, 166 (RED), …,
   181–188 (184–185 RED); "22 packages · all 404"; CODE(docker-shell.sh: 3) flashes on "set dash e".
3. The terminal shrinks to a strip; V1's laptop corner (cockpit lit) appears and cracks RED. PONDER 8 s.
4. CODE(Dockerfile: 1–2), line 2 YELLOW; the ORANGE base band "bullseye · Debian 11"; the mirror card
   (dated, at the time of recording). D · extra fix 1: the sed of 22 in the strip (extra + editor chip)
   → 22:2–3, line 3 GREEN, shown large as "your new line 2"; the base relabels "bookworm · Debian 12",
   one crack goes; ▶ your turn.
5. D2: the terminal grows; a 14-step counter; sh docker-shell.sh → 23: 330, …, 344–348 (348 YELLOW),
   …, 356 (RED), …, 372–378 (376 RED); steps 2–7 tick GREEN, 8 RED; "renamed by Google · no Kubernetes
   plugin needed here"; ▶ your turn.
6. D · extra fix 2: strip + V1 corner; the sed of 24 → 24:2–4, line 4 GREEN, shown large as "your new
   line 37"; the ORANGE apt layer relabels google-cloud-cli, the last crack goes; ▶ your turn. Then the
   terminal grows: git diff --stat; git diff Dockerfile (extra) → 25: 2–4, …, 11–12, …, 20–21; line 4
   YELLOW.
7. D2: sh docker-shell.sh, ▶ your turn → 26: 3 (at the time of recording; "much slower emulated on
   Apple Silicon"), …, 19, …, 32, 34–36 (35 RED wrap, "the honest no-key state"). The terminal shrinks
   to a strip; the V1 cockpit becomes solid TEAL.
8. 26: 37–41 in the strip ("x86_64 on a Mac too · built for amd64"; versions tagged at the time of
   recording), the prompt root@<id>:/app# + "root · the id changes every run". Erratum:
   CODE(docker-entrypoint.sh: 13–19), lines 13 and 19 YELLOW, "a label, not a fact". Fade out.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F403
from explainer import style as S

SAY = NARRATION["S08"]
PONDER_DEBIAN = ("Every error is a 404 from a Debian mirror,\nand your internet works. Which line of\n"
                 "the Dockerfile picks your Debian?")
CORNER = ("laptop", "cockpit", "secrets", "key")       # the V1 pieces this scene works on


def corner_map(**kw) -> TrainingMap:
    """V1 as S08 starts, cut down to the laptop corner (the cockpit, secrets/, the W&B key), lit."""
    m = TrainingMap.at("S08", **kw)
    for k in MAP_KEYS:
        if k not in CORNER and m.parts[k] in m.submobjects:
            m.remove(m.parts[k])
    for k in CORNER:
        m._apply(k, True)
    return m


def layered_map(apt_text: str) -> TrainingMap:
    """The laptop corner after fix 1, with the ORANGE apt layer between the house and the Debian base
    (the base band, secrets/ and the key chip step down to make room)."""
    m = corner_map(base="bookworm · Debian 12")
    y0 = m.base.get_center()[1]
    m.base.shift(DOWN * 0.37)
    m.parts["secrets"].shift(DOWN * 0.3)
    m.parts["key"].shift(DOWN * 0.3)
    m.apt = band(apt_text, SYSTEM, 2.85, 0.34, 20).move_to([m.base.get_center()[0], y0, 0])
    m.add(m.apt)
    return m


def glyphs_of(text_mob, sub: str):
    """The glyphs of `sub` inside a label()/mono() Text (Text drops spaces from its submobjects)."""
    s = text_mob.original_text
    i = s.index(sub)
    a = len(s[:i].replace(" ", ""))
    n = len(sub.replace(" ", ""))
    return VGroup(*text_mob[a:a + n])


def readme_split(first: int, last: int) -> str:
    """README lines first..last with each bracketed note moved to its own indented row (text unchanged)."""
    rows = []
    for ln in readme(first, last).split("\n"):
        if " [" in ln:
            i = ln.index(" [")
            rows += [ln[:i], "    " + ln[i + 1:]]
        else:
            rows.append(ln)
    return "\n".join(rows)


def step_counter(n: int = 14, size: float = 20) -> VGroup:
    """A small counter of the build's 14 steps: GREY boxes numbered 1 … 14. .boxes .head"""
    head = label("build steps", size, S.GREY)
    boxes = VGroup()
    for i in range(1, n + 1):
        b = RoundedRectangle(width=0.5, height=0.42, corner_radius=0.06, stroke_color=S.GREY_DARK, stroke_width=2)
        b.set_fill(S.BG, 1)
        boxes.add(VGroup(b, mono(str(i), size, S.GREY).move_to(b)))
    boxes.arrange(RIGHT, buff=0.08)
    g = VGroup(head, boxes).arrange(RIGHT, buff=0.3)
    g.boxes, g.head = boxes, head
    return g


def mark_step(box, color):
    """Animation: one counter box fills with `color` and its number turns WHITE."""
    return AnimationGroup(box[0].animate.set_fill(color, 0.55).set_stroke(color), box[1].animate.set_color(INK))


def big_line(caption: str, text: str, size: float = 26) -> VGroup:
    """'your new line N' over the line itself, large and GREEN. .cap .text"""
    cap = label(caption, 22, S.GREY)
    t = mono(text, size, OWNED)
    g = VGroup(cap, t).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    g.cap, g.text = cap, t
    return g


def note_beside(p, k: int, mob, buff: float = 0.45):
    """Put `mob` right of line k (0-based) of code panel p."""
    ln = p.code.code_lines[k]
    return mob.move_to([ln.get_right()[0] + buff + mob.width / 2, ln.get_center()[1], 0])


def flow_note(src: str, dst: str) -> VGroup:
    """A GREY → TEAL note: the host path on the left, the container path on the right."""
    a = grey_chip(src)
    b = chip(dst, IMAGE, size=20, font=MONO)
    ar = Arrow(LEFT * 0.35, RIGHT * 0.35, buff=0, color=IMAGE, stroke_width=3, tip_length=0.14,
               max_tip_length_to_length_ratio=0.5)
    return VGroup(a, ar, b).arrange(RIGHT, buff=0.12)


class TwoFixes(VoiceScene):
    def keep_only(self, *keep, run_time=0.6, shift=UP * 0.2):
        fam = {id(x) for k in keep for x in k.get_family()}
        gone = [m for m in self.mobjects if not any(id(x) in fam for x in m.get_family())]
        if gone:
            self.play(FadeOut(Group(*gone), shift=shift), run_time=run_time)
            self.remove(*gone)

    def construct(self):
        assert len(SAY) == SAY_COUNT["S08"] == 9, len(SAY)
        c20, c21, c22, c23 = capture("20"), capture("21"), capture("22"), capture("23")
        c24, c25, c26 = capture("24"), capture("25"), capture("26")
        assert c26.cmd == "sh docker-shell.sh" and c26.cmd in readme(115)
        assert c22.line(3) == "FROM python:3.13-slim-bookworm"
        grey = S.GREY

        # ========================================================== 0. part 2's purpose; edit docker-shell.sh (D1)
        tr = tracker_d(1)
        ref = lref("24")
        assert tr.caption.get_right()[0] < ref.get_left()[0]
        mp = TrainingMap.at("S08")
        tut = grey_chip("the build itself is tutorial-only")
        tut.move_to([-6.5 + tut.width / 2, -1.8, 0])
        t = laptop_term(5)
        same = grey_chip("same terminal as your export · new terminal? export again first")
        same.next_to(t.box, UP, buff=0.15).align_to(t.box, RIGHT)
        rc93 = readme_card((93, 94), body=readme_split(93, 94), size=20)
        rc93.move_to([-6.3 + rc93.width / 2, 2.75 - rc93.height / 2, 0])
        rows93 = rc93.body
        assert README_BUCKET in rows93[0].original_text and "ac215-project" in rows93[2].original_text
        rp1 = replace_chip().next_to(rows93[0], RIGHT, buff=0.35)
        rp2 = replace_chip().next_to(rows93[2], RIGHT, buff=0.35).align_to(rp1, LEFT)
        pid = grey_chip("project ID, not its name · keep gs://")
        pid.next_to(rp2, DOWN, buff=0.2).align_to(rp1, LEFT)
        ed = grey_chip("our editor; use yours · this sed -i is GNU syntax · macOS sed: sed -i ''")
        ed.next_to(t.box, UP, buff=0.15).align_to(t.box, RIGHT)
        assert pid.get_right()[0] < 6.55 and rc93.get_bottom()[1] > same.get_top()[1] + 0.05
        assert pid.get_bottom()[1] > max(ed.get_top()[1], same.get_top()[1]) + 0.05, (pid.get_bottom(), ed.get_top())

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(mp), FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.8)
            vo.wait_until("build the cockpit")
            self.play(mp.light("laptop", "cockpit", run_time=0.4), FadeIn(tut, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(mp.parts["cockpit"][2], color=IMAGE, scale_factor=1.12), run_time=0.5)
            vo.wait_until("pack the code")
            self.play(mp.light("gcp", "bucket", run_time=0.4), run_time=0.5)
            self.play(Indicate(mp.parts["bucket"][1], color=CLOUD, scale_factor=1.1), run_time=0.5)
            vo.wait_until("send one job")
            self.play(mp.light("vertex", run_time=0.4), run_time=0.5)
            self.play(Indicate(mp.parts["vertex"][1], color=CLOUD, scale_factor=1.12), run_time=0.5)
            self.play(mp.unlight("laptop", "cockpit", "gcp", "bucket", "vertex", run_time=0.6), run_time=0.6)
            vo.wait_until("Put your bucket and project")
            self.play(FadeOut(VGroup(mp, tut), shift=UP * 0.2), run_time=0.5)
            self.remove(mp, tut)
            self.play(FadeIn(t), FadeIn(same, shift=UP * 0.1), run_time=0.5)
            type_cmd(self, t, "cd model-training", type_time=0.5)
            cd_prompt(self, t, P_REPO, run_time=0.4)
            self.play(FadeIn(rc93, shift=DOWN * 0.15), run_time=0.5)
            self.play(each([glyphs_of(rows93[1], rows93[1].original_text.strip()),
                            glyphs_of(rows93[3], rows93[3].original_text.strip())], TURN, scale=1.06),
                      FadeIn(rp1, shift=LEFT * 0.1), FadeIn(rp2, shift=LEFT * 0.1), run_time=0.8)
            vo.wait_until("lines 8 and 9 of docker-shell.sh")
            self.play(FadeIn(pid, shift=UP * 0.1), run_time=0.4)
            self.play(FadeOut(same, shift=UP * 0.1), FadeIn(ed, shift=UP * 0.1), run_time=0.4)
            self.remove(same)
            type_cmd(self, t, c20.cmd, type_time=1.4, soft=True)
            o20 = out(self, t, [c20.line(2), c20.line(3), c20.line(4), (c20.line(5), OWNED), (c20.line(6), OWNED)],
                      run_time=0.5)
            vo.wait_until("pause and edit yours")
            yt0 = beside(turn_row(), o20[-1])
            pin(self, o20[-1], yt0, run_time=0.3)
            flash_tag(self, yt0, TURN, run_time=0.6)

        # ========================================================== 1. erratum: the README's listing; the real script
        rcA = readme_card((100, 101), size=20)
        rcB = readme_card(110, body=readme(110), size=20)
        notf = grey_chip("the README's listing is not the file · edit docker-shell.sh itself")
        inner = VGroup(rcB, rcA, notf).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        kind = RoundedRectangle(width=inner.width + 0.7, height=inner.height + 0.7, corner_radius=0.18,
                                stroke_color=grey, stroke_width=2.5).set_fill(S.BG, 1)
        kind.move_to([0, 2.6 - kind.height / 2, 0])
        inner.move_to(kind)
        er = erratum_tag()
        er.move_to([kind.get_right()[0] - 0.4 - er.width / 2, kind.get_top()[1], 0])
        assert er.get_top()[1] < 2.85 and kind.get_bottom()[1] > -3.5, (er.get_top(), kind.get_bottom())
        brk = glyphs_of(rcB.body[0], "[MAKE SURE YOU HAVE THIS VARIABLE SET]")
        p = code("docker-shell.sh", 13, 24)
        p.move_to([0, 2.72 - p.height / 2, 0])
        b14, b17 = line_bar(p.code, 1, TURN, 0.22), line_bar(p.code, 4, grey, 0.22)
        b18, b19 = line_bar(p.code, 5, IMAGE, 0.2), line_bar(p.code, 6, IMAGE, 0.2)
        n18 = flow_note("your code", "/app")
        n19 = flow_note("secrets", "/secrets")
        VGroup(n18, n19).arrange(RIGHT, buff=0.6).next_to(p, DOWN, buff=0.25).align_to(p.code, LEFT).shift(RIGHT * 0.3)
        assert n19.get_bottom()[1] > -3.55, n19.get_bottom()
        env = grey_chip("four -e: key path, project, bucket, W&B key")
        env.move_to([6.35 - env.width / 2, p.code.code_lines[10].get_center()[1], 0])
        nop = note_beside(p, 4, grey_chip("no -p · it serves nothing"))
        for m_ in (n18, n19, env, nop):
            assert m_.get_right()[0] < 6.55, m_.get_right()
        assert env.get_left()[0] > p.code.code_lines[9].get_right()[0] + 0.1, env.get_left()

        with self.voiceover(SAY[1]) as vo:
            self.keep_only(tr, ref)
            self.play(FadeIn(kind), FadeIn(er, shift=DOWN * 0.1), FadeIn(rcB, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(rcA, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("It has notes in brackets")
            self.play(Create(under(brk, TURN, stroke=3)), each(list(brk), TURN, scale=1.08, lag=0.03), run_time=0.9)
            vo.wait_until("an older line for Apple chips")
            self.play(Indicate(rcA.body, color=TURN, scale_factor=1.03), run_time=0.8)
            vo.wait_until("so edit the script itself")
            self.play(FadeIn(notf, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("It builds for amd64")
            self.keep_only(tr, ref, run_time=0.4)
            self.play(FadeIn(p, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(b14), Indicate(code_span(p.code, 1, "--platform=linux/amd64"), color=TURN,
                                            scale_factor=1.06), run_time=0.6)
            self.play(FadeIn(b17), run_time=0.3)
            vo.wait_until("mounts your code and secrets")
            self.play(FadeIn(b18), FadeIn(n18, shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(b19), FadeIn(n19, shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(env, shift=RIGHT * 0.15), run_time=0.4)
            self.play(FadeIn(nop, shift=RIGHT * 0.15), run_time=0.4)

        # ========================================================== 2. sh docker-shell.sh fails at step 2 (D2)
        rc114 = readme_card((114, 115), size=20)
        rc114.move_to([-6.3 + rc114.width / 2, 2.75 - rc114.height / 2, 0])
        t = laptop_term(8, P_REPO)
        se = code("docker-shell.sh", 3)
        all404 = grey_chip("22 packages · all 404")
        right_x = 6.4
        all404.move_to([right_x - all404.width / 2, 2.5, 0])
        se.move_to([right_x - se.width / 2, 1.55, 0])
        assert rc114.get_right()[0] < min(se.get_left()[0], all404.get_left()[0]) - 0.15
        assert se.get_bottom()[1] > t.box.get_top()[1] + 0.05, (se.get_bottom(), t.box.get_top())

        with self.voiceover(SAY[2]) as vo:
            self.keep_only(tr, ref, run_time=0.4)
            self.play(track(tr, 2), FadeIn(rc114, shift=DOWN * 0.1), FadeIn(t), run_time=0.6)
            ln = type_cmd(self, t, c21.cmd, type_time=0.6)
            vo.wait_until("pause and run it")
            yt = beside(turn_row(), ln)
            pin(self, ln, yt, run_time=0.3)
            flash_tag(self, yt, TURN, run_time=0.6)
            vo.wait_until("Today it fails at step 2 of 14")
            o1 = out(self, t, [c21.line(23), ("…", grey)], wrap=True, run_time=0.4)
            self.play(Indicate(substring(o1[0], "[ 2/14]"), color=ERR, scale_factor=1.25), run_time=0.7)
            vo.wait_until("All 22 packages")
            out(self, t, [(c21.line(n), ERR) for n in range(65, 71)] + [("…", grey)], wrap=True, run_time=0.6)
            self.play(FadeIn(all404, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("the build stops at line 18")
            out(self, t, [(c21.line(166), ERR), ("…", grey)], wrap=True, run_time=0.3)
            fr = [c21.line(181), c21.line(182), c21.line(183), (c21.line(184), ERR), (c21.line(185), ERR),
                  c21.line(186), c21.line(187)]
            o3 = out(self, t, fr, wrap=True, run_time=0.6)
            self.play(Indicate(substring(o3[0], "Dockerfile:18"), color=ERR, scale_factor=1.2), run_time=0.6)
            out(self, t, [c21.line(188)], wrap=True, run_time=0.4)
            vo.wait_until("The script's set dash e")
            self.play(FadeIn(se, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(code_span(se.code, 0, "set -e"), color=TURN, scale_factor=1.2), run_time=0.7)
            vo.wait_until("before docker run")
            self.play(Create(ring(se.code, TURN, buff=0.08)), run_time=0.5)
            assert len(o3)

        # ========================================================== 3. the strip, the cracked cockpit, PONDER
        cm = corner_map()
        cr = cm.crack()

        with self.voiceover(SAY[3]) as vo:
            self.keep_only(tr, ref, t, *t.lines, run_time=0.4)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(cm, shift=UP * 0.1), run_time=0.6)
            self.play(Create(cr[0]), Create(cr[1]), run_time=0.7)
            vo.wait_until("Every error says 404")
            self.play(Indicate(cm.parts["cockpit"][2], color=ERR, scale_factor=1.1), run_time=0.7)
        card5 = ponder(self, PONDER_DEBIAN, seconds=8)

        # ========================================================== 4. line 2, the base; fix 1 (extra)
        df = code("Dockerfile", 1, 2, cuts={1: "official Python image"})
        df.move_to([-3.0 + df.width / 2, 2.0, 0])
        b2 = line_bar(df.code, 1, TURN, 0.22)
        mirror = card(["on 2026-10-23 its security mirror lists", "packages it no longer serves ·",
                       "they are on archive.debian.org"], size=20)
        mirror.next_to(df, DOWN, buff=0.3).align_to(df, LEFT)
        mtag = recording_tag().next_to(mirror, RIGHT, buff=0.2).align_to(mirror, DOWN)
        assert mtag.get_right()[0] < 6.55 and mirror.get_bottom()[1] > -1.35, (mtag.get_right(), mirror.get_bottom())
        ed2 = grey_chip("our editor; use yours · macOS sed: sed -i ''")
        ed2.move_to([6.4 - ed2.width / 2, -1.1, 0])
        nl2 = big_line("your new line 2", c22.line(3))
        nl2.move_to([-2.9 + nl2.width / 2, 1.3, 0])

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card5), run_time=0.4)
            self.remove(card5)
            self.play(FadeIn(df, shift=LEFT * 0.15), run_time=0.5)
            self.play(FadeIn(b2), Indicate(code_span(df.code, 1, "python:3.13-slim-bullseye"), color=TURN,
                                           scale_factor=1.08), run_time=0.7)
            vo.wait_until("Bullseye is Debian 11")
            self.play(cm.relabel_base("bullseye · Debian 11"), run_time=0.6)
            self.play(Indicate(cm.base.text, color=SYSTEM, scale_factor=1.1), run_time=0.6)
            vo.wait_until("at the time of recording")
            self.play(FadeIn(mirror, shift=UP * 0.1), FadeIn(mtag), run_time=0.6)
            vo.wait_until("The first fix, an extra")
            self.play(FadeOut(VGroup(mirror, mtag), shift=DOWN * 0.1), track(tr, 2, extra="fix 1"), run_time=0.5)
            self.remove(mirror, mtag)
            ex4 = on_bar(t, extra_row())
            self.play(FadeIn(ex4), FadeIn(ed2, shift=UP * 0.1), run_time=0.4)
            type_cmd(self, t, c22.cmd, type_time=1.0)
            o22 = out(self, t, [c22.line(2), (c22.line(3), OWNED)], run_time=0.4)
            vo.wait_until("switches the base to bookworm")
            src = substring(o22[-1], c22.line(3)).copy()
            self.play(FadeOut(VGroup(df, b2), shift=UP * 0.1), ReplacementTransform(src, nl2.text),
                      FadeIn(nl2.cap), run_time=0.9)
            self.remove(df, b2)
            self.play(cm.relabel_base("bookworm · Debian 12"), FadeOut(cr[0]), run_time=0.7)
            vo.wait_until("pause and make it")
            yt4 = beside(turn_row(), o22[-1])
            pin(self, o22[-1], yt4, run_time=0.3)
            flash_tag(self, yt4, TURN, run_time=0.6)

        # ========================================================== 5. run it again: step 8 (D2)
        sc = step_counter()
        sc.move_to([-6.3 + sc.width / 2, 2.45, 0])
        ren = grey_chip("renamed by Google · no Kubernetes plugin needed here")
        ren.move_to([6.4 - ren.width / 2, 1.6, 0])

        with self.voiceover(SAY[5]) as vo:
            gone = VGroup(cm, cr[1], nl2, ed2, ex4)
            self.play(FadeOut(gone, shift=UP * 0.15), track(tr, 2), run_time=0.5)
            self.remove(gone, *gone)
            resize(self, t, 9, run_time=0.5)
            self.play(FadeIn(sc, shift=DOWN * 0.1), run_time=0.4)
            self.play(mark_step(sc.boxes[0], S.GREY), run_time=0.3)
            ln5 = type_cmd(self, t, c23.cmd, type_time=0.5)
            yt5 = beside(turn_row(), ln5)
            pin(self, ln5, yt5, run_time=0.3)
            flash_tag(self, yt5, TURN, run_time=0.6)
            vo.wait_until("Now it stops at step 8")
            self.play(LaggedStart(*[mark_step(sc.boxes[i], PASS) for i in range(1, 7)], lag_ratio=0.3), run_time=1.0)
            o5 = out(self, t, [c23.line(330), ("…", grey)], wrap=True, run_time=0.4)
            self.play(mark_step(sc.boxes[7], ERR), Indicate(substring(o5[0], "[ 8/14]"), color=ERR, scale_factor=1.25),
                      run_time=0.7)
            vo.wait_until("google-cloud-sdk has no installation candidate")
            out(self, t, [c23.line(n) for n in range(344, 348)] + [(c23.line(348), TURN), ("…", grey),
                                                                   (c23.line(356), ERR)], wrap=True, run_time=0.6)
            vo.wait_until("google-cloud-cli replaces it")
            self.play(Indicate(substring(t.find("  google-cloud-cli"), "google-cloud-cli"), color=TURN,
                               scale_factor=1.2), run_time=0.6)
            out(self, t, [("…", grey)] + [c23.line(n) for n in range(372, 376)] + [(c23.line(376), ERR),
                                                                                c23.line(377), c23.line(378)],
                wrap=True, run_time=0.6)
            vo.wait_until("Google renamed its apt package")
            self.play(FadeIn(ren, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 6. fix 2 (extra); the diff (extra)
        cm2 = layered_map("apt · google-cloud-sdk")
        cr1 = cm.crack()[1]
        apt_new = band("apt · google-cloud-cli", SYSTEM, 2.85, 0.34, 20).move_to(cm2.apt)
        nl37 = big_line("your new line 37", c24.line(4).strip(), size=22)
        nl37.move_to([-2.9 + nl37.width / 2, 1.5, 0])
        assert nl37.get_right()[0] < 6.55, nl37.get_right()
        ed3 = grey_chip("our editor; use yours · macOS sed: sed -i ''")
        ed3.move_to([6.4 - ed3.width / 2, -1.1, 0])

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(sc, ren), shift=UP * 0.15), track(tr, 2, extra="fix 2"), run_time=0.5)
            self.remove(sc, ren, *sc, *ren)
            resize(self, t, 3, run_time=0.5)
            self.play(FadeIn(cm2, shift=UP * 0.1), FadeIn(cr1), run_time=0.5)
            self.play(Indicate(cm2.apt.text, color=ERR, scale_factor=1.1), run_time=0.6)
            ex6 = on_bar(t, extra_row())
            self.play(FadeIn(ex6), FadeIn(ed3, shift=UP * 0.1), run_time=0.4)
            type_cmd(self, t, c24.cmd, type_time=1.0, soft=True)
            o24 = out(self, t, [c24.line(2), c24.line(3), (c24.line(4), OWNED)], run_time=0.4)
            vo.wait_until("on line 37")
            src = substring(o24[-1], c24.line(4).strip()).copy()
            self.play(ReplacementTransform(src, nl37.text), FadeIn(nl37.cap), run_time=0.8)
            self.play(Transform(cm2.apt, apt_new), FadeOut(cr1), run_time=0.7)
            vo.wait_until("pause and make it")
            yt6 = beside(turn_row(), o24[-1])
            pin(self, o24[-1], yt6, run_time=0.3)
            flash_tag(self, yt6, TURN, run_time=0.6)
            vo.wait_until("An extra git diff")
            gone = VGroup(cm2, nl37, ed3, ex6)
            self.play(FadeOut(gone, shift=UP * 0.15), run_time=0.4)
            self.remove(gone, *gone)
            resize(self, t, 10, run_time=0.5)
            ex6b = on_bar(t, extra_row())
            self.play(FadeIn(ex6b), run_time=0.3)
            type_cmd(self, t, c25.cmd, type_time=0.6)
            o25 = out(self, t, c25.at((2, 4)) + [("…", grey), (c25.line(11), grey), (c25.line(12), OWNED), ("…", grey),
                                                 (c25.line(20), grey), (c25.line(21), OWNED)], wrap=True, run_time=0.7)
            vo.wait_until("your two values")
            stat = substring(o25[2], c25.line(4).strip())
            self.play(stat.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(substring(o25[1], "docker-shell.sh"), color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("the two fixes")
            self.play(each([substring(t.find("+FROM"), "+FROM python:3.13-slim-bookworm"),
                            substring(t.find("+    apt-get"), "google-cloud-cli")], OWNED, scale=1.08), run_time=0.8)
            vo.wait_until("and nothing else")
            self.play(Create(ring(stat, TURN, buff=0.07)), run_time=0.5)

        # ========================================================== 7. the third run builds (D2); the cockpit is solid
        slow = grey_chip("much slower emulated on Apple Silicon")
        slow.move_to([6.4 - slow.width / 2, 2.45, 0])
        honest = grey_chip("the honest no-key state")
        honest.move_to([6.4 - honest.width / 2, 1.85, 0])
        cm3 = layered_map("apt · google-cloud-cli")

        with self.voiceover(SAY[7]) as vo:
            self.keep_only(tr, ref, t, *t.lines, ex6b, run_time=0.3)
            self.play(FadeOut(ex6b), track(tr, 2), run_time=0.4)
            self.remove(ex6b)
            ln7 = type_cmd(self, t, c26.cmd, type_time=0.5)
            yt7 = beside(turn_row(), ln7)
            pin(self, ln7, yt7, run_time=0.3)
            flash_tag(self, yt7, TURN, run_time=0.6)
            vo.wait_until("it builds")
            o7 = out(self, t, [squash(BUILD_LINE)], run_time=0.4)
            tt = on_bar(t, time_row())
            self.play(FadeIn(tt), run_time=0.3)
            self.play(Indicate(substring(o7[0], "FINISHED"), color=PASS, scale_factor=1.2), run_time=0.6)
            vo.wait_until("longer on Apple Silicon")
            self.play(FadeIn(slow, shift=DOWN * 0.1), run_time=0.4)
            out(self, t, [("…", grey), c26.line(19), ("…", grey), squash(c26.line(32))], wrap=True, run_time=0.5)
            vo.wait_until("The banner says running")
            ob = out(self, t, [c26.line(34)], run_time=0.3)
            self.play(Indicate(substring(ob[0], c26.line(34)), color=INK, scale_factor=1.1), run_time=0.5)
            vo.wait_until("then gcloud cannot open the key file")
            out(self, t, [(c26.line(35), ERR)], wrap=True, run_time=0.5)
            vo.wait_until("our missing key")
            self.play(FadeIn(honest, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("With yours, this line confirms")
            self.play(Indicate(substring(t.find("activate-service-account"), "activate-service-account"), color=INK,
                               scale_factor=1.08), run_time=0.7)
            vo.wait_until("The script carries on anyway")
            o36 = out(self, t, [c26.line(36)], run_time=0.3)
            self.play(Indicate(substring(o36[0], c26.line(36)), color=INK, scale_factor=1.06), run_time=0.5)
            vo.wait_until("because the entrypoint has no set dash e")
            self.play(FadeOut(VGroup(slow, honest, tt), shift=UP * 0.1), run_time=0.3)
            self.remove(slow, honest, tt)
            resize(self, t, 3, run_time=0.5)
            self.play(FadeIn(cm3, shift=UP * 0.1), run_time=0.5)
            self.play(cm3.solid(), run_time=0.8)

        # ========================================================== 8. the banner's last lines; erratum: activated
        mac = grey_chip("x86_64 on a Mac too · built for amd64")
        mac.move_to([6.4 - mac.width / 2, -1.1, 0])
        rid = grey_chip("root · the id changes every run")
        rid.move_to([6.4 - rid.width / 2, -1.1, 0])
        ep = code("docker-entrypoint.sh", 13, 19)
        ep.move_to([0, 2.72 - ep.height / 2, 0])
        b13, b19 = line_bar(ep.code, 0, TURN, 0.22), line_bar(ep.code, 6, TURN, 0.22)
        er8 = erratum_tag().move_to(ep.header).align_to(ep.code, RIGHT).shift(LEFT * 0.1)
        fact = grey_chip("a label, not a fact", size=22)
        fact.next_to(ep, DOWN, buff=0.15).align_to(ep, RIGHT)
        assert fact.get_bottom()[1] > t.box.get_top()[1] + 0.05, (fact.get_bottom(), t.box.get_top())

        with self.voiceover(SAY[8]) as vo:
            o37 = out(self, t, [c26.line(37)], run_time=0.3)
            self.play(Indicate(substring(o37[0], "x86_64"), color=TURN, scale_factor=1.2), FadeIn(mac, shift=UP * 0.1),
                      run_time=0.6)
            vo.wait_until("the versions are on screen")
            o38 = out(self, t, [c26.line(38), c26.line(39), c26.line(40)], run_time=0.5)
            tp, tu = beside(time_row(), o38[1]), beside(time_row(), o38[2])
            self.play(FadeIn(tp), FadeIn(tu), run_time=0.4)
            attach(self, o38[1], tp)
            attach(self, o38[2], tu)
            out(self, t, [c26.line(41)], run_time=0.3)
            t.set_prompt(P_COCKPIT)
            bare_prompt(self, t)
            self.play(FadeOut(mac), FadeIn(rid, shift=UP * 0.1), run_time=0.4)
            self.remove(mac)
            vo.wait_until("A small slip")
            self.play(FadeOut(VGroup(cm3, rid), shift=UP * 0.15), run_time=0.4)
            self.remove(cm3, rid)
            self.play(FadeIn(ep, shift=UP * 0.1), FadeIn(er8), run_time=0.5)
            vo.wait_until("activated is printed")
            self.play(FadeIn(b13), Indicate(code_span(ep.code, 0, "activated"), color=TURN, scale_factor=1.1),
                      run_time=0.6)
            vo.wait_until("before the activation")
            self.play(FadeIn(b19), Indicate(code_span(ep.code, 6, "source"), color=TURN, scale_factor=1.1),
                      run_time=0.6)
            vo.wait_until("a label, not a fact")
            self.play(FadeIn(fact, shift=UP * 0.1), run_time=0.5)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
