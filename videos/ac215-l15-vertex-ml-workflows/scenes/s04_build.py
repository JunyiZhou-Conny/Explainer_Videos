"""S04 · The CLI container: two one-line fixes (README A › Run Container, steps 3-5, two extras,
the V2 StarVsPin set piece). No lecture picture: no lecture tag.

Beats (script.md "## S04", one voiceover block each):
 0  TRACKER A2 3. 10-row laptop terminal (20 pt), prompt ~/model-deployment-aws. Types laptop/17's
    sed (soft-wrapped; `extra` on the title bar; GREY chip "use your editor" above the terminal)
    -> TERM(laptop/17: 4-6; the ARN line wrapped after "role/"). The bucket, the ARN and the region
    turn YELLOW as named; row chip "placeholder account" by the ARN; ▶ your turn by the region.
 1  TRACKER A2 4. `chmod +x docker-shell.sh` -> the prompt returns. TRACKER A2 4 · extra:
    `ls -l docker-shell.sh` (extra) -> TERM(laptop/19: 2), `-rwxr-xr-x` GREEN.
 2  TRACKER A2 5. The terminal shrinks to 8 rows; `sh docker-shell.sh` -> TERM(laptop/20: 19 cut, …,
    35 cut, 36, …, 49 cut); row chip "arm64 variant pulled" on the `…` after line 19; line 36 and
    line 49 RED. Picture above (right): a TEAL arm64 chip (the image's programs) -> a GREY x86_64
    chip (your laptop's CPU), a RED cross on the arrow.
 3  TRACKER A2 5 · extra. CODE(docker-shell.sh: 16-19) on top: line 19 RED bar + chip "M1/2 chip
    macs use this line", line 17 GREEN bar. On "Swap them" the `#` travels from line 17 to line
    19; the laptop/21 sed (extra) is typed -> TERM(laptop/21: 2-4); GREEN row chip "fix 1 · plain
    build line". The panel gives way to three platform chips, one per phrase.
 4  TRACKER A2 5. All picture: CODE(Pipfile: 8-17) left (line 12 tensorflow GREEN bar, line 10
    sagemaker = "*" ORANGE bar); right: CODE(.gitignore: 67-68), line 68 GREY + chip "keeps a lock
    out of the repository"; CODE(Dockerfile: 52-55), line 52 PINK, line 55 ORANGE + chip "the lock
    is made at build time".
 5  The panels dim; PONDER(8 s) card over them.
 6  V2 StarVsPin: number line; on "Star" the whole line lights ORANGE. TRACKER A2 5 · extra · check:
    8-row terminal types laptop/22's command (cut) -> TERM(laptop/22: 4, …, 12, …, 26, …, 35); the
    resolver arrow drops a RED dot at 3.13.1; line 4 YELLOW + "at the time of recording";
    sagemaker==3.13.1 RED; torch and nvidia-cublas ORANGE + row chip "14 CUDA packages".
 7  The terminal clears, types laptop/23's command (cut) -> TERM(laptop/23: 7-8, 9-14); line 8
    flashes, the three errors turn RED as named. The terminal leaves; the two module shelves come in
    under V2; three PURPLE import arrows from cli.py:21-23 reach into the 3.x shelf and turn RED.
 8  A dark scrim over V2; GREY note card "here: … 13 min in pipenv lock, then ran out of disk ·
    not kept as a capture"; a GREY bar crawls while a counter runs to 13 min, RED "disk full"
    stamp. On "On your laptop" a laptop glyph's own bar finishes, then a RED ImportError stamp.
 9  Scrim and card go; the shelves step aside. TRACKER A2 5 · extra: 6-row terminal types laptop/24
    -> TERM(laptop/24: 9-12), line 10 RED, line 11 GREEN. V2: GREEN wall at 3.0, the dot jumps
    back to 2.257.7; the terminal leaves, the shelves return and the imports land GREEN in the 2.x
    shelf; caption "a constraint is not a pin (L1)", chip "fix 2", ▶ your turn.
10  V2 fades. TRACKER A2 5. 12-row terminal types `sh docker-shell.sh` -> TERM(laptop/25: 3, …, 23,
    …, 29-30, 32 wrap, 33; whitespace runs squeezed), line 3 + "at the time of recording", line
    23 YELLOW, line 32 RED; the container prompt (app) app@<id>:/app$ with chip "the id changes
    every run".
11  TRACKER A2 5 · extra. Clear; at the container prompt: python --version; which … -> 36;
    pip list … (folds) -> 45, 47; echo … -> 49 (wrap). Versions + "at the time of recording";
    GREY chip "deprecation warnings ahead: not the error" above the terminal.
12  TRACKER A2 5 · extra. Clear; `python cli.py --help` -> TERM(laptop/25: 73, 75, 78-83); the
    Google words ORANGE, tag `erratum` + chip "kept from the Google version · the commands are
    AWS"; row chip "does nothing" by --test. The terminal turns into a host tab (prompt
    ~/model-deployment-aws): `docker image ls model-deployment-cli-aws` (extra) -> TERM(laptop/26:
    2-3, squeezed), 4.01GB + "at the time of recording". Fade to an empty frame.
"""

import re

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S04"]

PONDER_Q = ("The Pipfile says sagemaker = \"*\".\nThe code worked when it was written.\n"
            "Nobody changed a line. Why does\ncli.py fail at import today?")
SIZE = 20                                     # terminal font: 72 characters a row

# ------------------------------------------------------------------ the real sources (checked)
C17, C18, C19, C20, C21 = (capture(n) for n in ("17", "18", "19", "20", "21"))
C22, C23, C24, C25, C26 = (capture(n) for n in ("22", "23", "24", "25", "26"))
assert C18.cmd == "chmod +x docker-shell.sh" and C19.cmd == "ls -l docker-shell.sh"
assert C20.cmd == "sh docker-shell.sh" == C25.cmd
assert C24.cmd == """sed -i 's/^sagemaker = "\\*"/sagemaker = "<3"/' Pipfile && git diff Pipfile""", C24.cmd
assert C26.cmd == "docker image ls model-deployment-cli-aws"
OUT17 = C17.at((4, 6))
assert OUT17[0].endswith(f'"{BUCKET_A_PH}"') and ROLE_A_PH in OUT17[1] and OUT17[2].endswith(f'"{REGION}"')
_k = OUT17[1].index("role/") + len("role/")
OUT17_ROWS = [OUT17[0], OUT17[1][:_k], OUT17[1][_k:], OUT17[2]]   # the ARN line wrapped after "role/"
assert "".join(OUT17_ROWS[1:3]) == OUT17[1]
OUT19 = C19.at(2)
assert OUT19[0].startswith("-rwxr-xr-x")
OUT20 = [cut(C20.line(19), n=72), "…", cut(C20.line(35), n=72), C20.line(36), "…", cut(C20.line(49), n=72)]
assert "ubuntu:20.04@sha256" in OUT20[0] and OUT20[3].endswith("exec /bin/sh: exec format error")
assert OUT20[5].startswith("ERROR: failed to build")
OUT21 = C21.at((2, 4))
assert OUT21[0] == "docker build -t $IMAGE_NAME -f Dockerfile ." and OUT21[2].startswith("#docker build")
L22 = C22.at(4, "…", 12, "…", 26, "…", 35)
assert L22[0].startswith("185 packages") and "nvidia-cublas" in L22[2] and "sagemaker==3.13.1" in L22[4]
assert "torch==2.8.0" in L22[6]
assert sum("nvidia-" in s for s in C22.at((12, 25))) == 14          # "14 CUDA packages"
L23 = [cut(s, n=72) for s in C23.at((7, 14))]
assert L23[1].startswith("its modules") and L23[3].startswith("ModuleNotFoundError")
assert L23[5].startswith("ImportError") and L23[7].startswith("ModuleNotFoundError")
DIFF24 = C24.at((9, 12))
assert DIFF24[1] == '-sagemaker = "*"' and DIFF24[2] == '+sagemaker = "<3"'


def squeeze(s: str) -> str:
    """Runs of padding spaces (BuildKit's right-aligned timings) squeezed to two."""
    return re.sub(r" {3,}", "  ", s.rstrip())


OUT25 = [squeeze(C25.line(3)), "…", squeeze(C25.line(23)), "…", C25.line(29), C25.line(30)]
assert OUT25[0] == "[+] Building 400.6s (19/19) FINISHED  docker:default", OUT25[0]
assert OUT25[2].endswith("334.7s") and "pipenv lock && pipenv sync" in OUT25[2]
ERR25 = C25.line(32)
assert ERR25.startswith("aws: [ERROR]") and "Unable to locate credentials" in ERR25
LAUNCH25 = C25.line(33)
TYPED = [C25.typed(n) for n in (35, 40, 48, 56)]
assert TYPED[3] == "python cli.py --help"
HELP25 = C25.at(73, 75, (78, 83))
assert HELP25[1] == "Data Collector CLI" and "GCS Bucket" in HELP25[3] and "--test" in HELP25[6]


def squeeze_table(lines) -> list[str]:
    """script.md 'squeeze': the table re-aligned with two-space gutters, the ID and empty columns
    dropped."""
    rows = [re.split(r" {2,}", s.strip()) for s in lines]
    head, body = rows[0], rows[1:]
    keep = [i for i, h in enumerate(head) if h != "ID" and any(i < len(r) and r[i] for r in body)]
    cols = [[r[i] if i < len(r) else "" for i in keep] for r in rows]
    w = [max(len(c[j]) for c in cols) for j in range(len(keep))]
    return ["  ".join(c[j].ljust(w[j]) for j in range(len(keep))).rstrip() for c in cols]


IMG26 = squeeze_table(C26.at(2, 3))
assert IMG26[0].split()[0] == "IMAGE" and "4.01GB" in IMG26[1] and "d3dc546c0eee" not in IMG26[1], IMG26


def fixed_tracker(key: str, step: int, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (common.py's head arrange() centres
    it at y 0; same workaround as S01; requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def cpu_chip(text: str, color, side: float = 1.25) -> VGroup:
    """A processor-chip glyph (square + pins) with a mono name inside. .core .text"""
    core = RoundedRectangle(width=side, height=side, corner_radius=0.08, stroke_color=color,
                            stroke_width=3).set_fill(color, 0.15)
    pins = VGroup()
    for k in range(4):
        off = (k - 1.5) * side / 4.5
        for d in (UP, DOWN, LEFT, RIGHT):
            n = np.array([-d[1], d[0], 0])
            a = core.get_center() + d * side / 2 + n * off
            pins.add(Line(a, a + d * 0.16, color=color, stroke_width=3))
    t = mono(text, 22, INK).move_to(core)
    g = VGroup(pins, core, t)
    g.core, g.text = core, t
    return g


class TwoFixes(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S04"] == 13, len(SAY)
        self.bar_tags = []

        # ========================================================== 0. step 3: edit docker-shell.sh
        tr = fixed_tracker("A2", 3)
        t = term(P_MD, rows=10, size=SIZE)
        self.t = t
        ed = under_term(t, grey_chip("use your editor"))
        ex0 = on_bar(t, extra_row())

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.2), FadeIn(t), run_time=0.6)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.06), run_time=0.5)
            line = type_cmd(self, t, C17.cmd, type_time=2.0)
            self.bar(ex0)
            self.play(FadeIn(ed, shift=DOWN * 0.1), run_time=0.4)
            rows = out(self, t, OUT17_ROWS, run_time=0.6)
            vo.wait_until("with your bucket")
            self.paint(rows[0], BUCKET_A_PH, TURN)
            vo.wait_until("the A R N of your role")
            self.paint(rows[1], "arn:aws:iam", TURN, end_of_row=True)
            self.paint(rows[2], "SageMakerExecutionRole", TURN)
            ph = beside(row_tag("placeholder account"), rows[2])
            pin(self, rows[2], ph)
            vo.wait_until("and your region")
            self.paint(rows[3], REGION, TURN)
            yt = beside(turn_row(), rows[3])
            pin(self, rows[3], yt)
            vo.wait_until("Ours are placeholders")
            flash_tag(self, ph)
            flash_tag(self, yt)

        # ========================================================== 1. step 4: chmod, ls -l
        with self.voiceover(SAY[1]) as vo:
            self.wipe(FadeOut(ed), track(tr, 4), *self.unbar_anims())
            type_cmd(self, t, C18.cmd, type_time=0.8)
            vo.wait_until("prints nothing")
            bp = bare_prompt(self, t)
            self.play(Indicate(bp, color=TURN, scale_factor=1.05), run_time=0.6)
            self.add(t)
            vo.wait_until("An extra listing")
            self.play(track(tr, 4, True), run_time=0.4)
            ln = type_cmd(self, t, C19.cmd, type_time=0.7)
            pin(self, ln, beside(extra_row(), ln))
            r19 = out(self, t, OUT19, run_time=0.4)
            vo.wait_until("was already executable")
            self.paint(r19[0], "-rwxr-xr-x", OWN)
            self.play(Indicate(substring(r19[0], "-rwxr-xr-x"), color=OWN, scale_factor=1.15), run_time=0.7)
            self.add(t)

        # ========================================================== 2. step 5: exec format error
        arm = cpu_chip("arm64", IMAGE).move_to([1.2, 1.85, 0])
        x86 = cpu_chip("x86_64", LAPTOP).move_to([4.9, 1.85, 0])
        arm_l = label("the image's programs", 20, IMAGE).next_to(arm, DOWN, buff=0.2)
        x86_l = label("your laptop's CPU", 20, LAPTOP).next_to(x86, DOWN, buff=0.2)
        go = arrow(arm.core.get_right() + RIGHT * 0.2, x86.core.get_left() + LEFT * 0.2, S.GREY, stroke=4)
        no = cross_glyph(0.42).move_to(go)
        pic = VGroup(arm, arm_l, x86, x86_l, go, no)
        assert pic.get_top()[1] < PIC_TOP and pic.get_bottom()[1] > 0.29 + 0.15, (pic.get_top(), pic.get_bottom())

        with self.voiceover(SAY[2]) as vo:
            self.wipe(track(tr, 5))
            resize(self, t, 8)
            line = type_cmd(self, t, C20.cmd, type_time=0.7)
            vo.wait_until("It pulls the base image")
            r20 = out(self, t, OUT20[:2], run_time=0.5)
            pin(self, r20[1], beside(row_tag("arm64 variant pulled", IMAGE), r20[1]))
            self.play(FadeIn(arm, shift=RIGHT * 0.2), FadeIn(arm_l), run_time=0.6)
            vo.wait_until("then stops at the first RUN line")
            r20b = out(self, t, [OUT20[2], (OUT20[3], ERR)], run_time=0.5)
            vo.wait_until("exec format error")
            self.play(Indicate(substring(r20b[1], "exec format error"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.add(t)
            r20c = out(self, t, ["…", (OUT20[5], ERR)], run_time=0.5)
            vo.wait_until("Our Intel style laptop")
            self.play(FadeIn(x86, shift=LEFT * 0.2), FadeIn(x86_l), GrowArrow(go), run_time=0.7)
            self.play(FadeIn(no, scale=1.6), go.animate.set_color(ERR), run_time=0.5)
            self.play(Indicate(no, color=ERR, scale_factor=1.25), run_time=0.6)

        # ========================================================== 3. fix 1: the plain build line
        p3 = code("A/docker-shell.sh", 16, 19, font_size=20)
        p3.move_to([0, 2.75 - p3.height / 2, 0])
        cl = p3.code.code_lines
        bar19 = line_bar(p3.code, 3, ERR, 0.22)
        bar17 = line_bar(p3.code, 1, OWN, 0.22)
        m12 = grey_chip("M1/2 chip macs use this line").next_to(p3, DOWN, buff=0.12).align_to(p3, RIGHT)
        dx = cl[1][2].get_center()[0] - cl[1][1].get_center()[0]      # one character ('d' -> 'o')
        assert 0.1 < dx < 0.2, dx
        plats = VGroup(grey_chip("Apple silicon Mac: arm64 line works", size=22),
                       grey_chip("Intel Mac / Windows: emulated, slow", size=22),
                       chip("Linux PC: this error", ERR, size=22)).arrange(DOWN, buff=0.25)
        plats.move_to([1.2, 1.45, 0])

        with self.voiceover(SAY[3]) as vo:
            self.wipe(FadeOut(pic), track(tr, 5, True))
            resize(self, t, 7)
            self.play(FadeIn(p3, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("Line 19 is for Apple silicon")
            self.play(FadeIn(bar19), cl[3].animate.set_color(ERR), run_time=0.5)
            self.add(p3, bar19)
            self.play(FadeIn(m12, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and line 17, commented out")
            self.play(FadeIn(bar17), run_time=0.5)
            self.play(Indicate(cl[1], color=OWN, scale_factor=1.04), run_time=0.7)
            self.add(p3, bar19, bar17)
            vo.wait_until("Swap them")
            hash_ = cl[1][0]
            hop = np.array([cl[3][0].get_left()[0] - hash_.get_left()[0],
                            cl[3].get_center()[1] - cl[1].get_center()[1], 0])
            self.play(hash_.animate(path_arc=-PI / 2).shift(hop),
                      VGroup(*cl[1][1:]).animate.shift(LEFT * dx).set_color(INK),
                      VGroup(*cl[3]).animate.shift(RIGHT * dx).set_color("#D9D3B8"),
                      run_time=1.0)
            self.add(p3, bar19, bar17)
            ln = type_cmd(self, t, C21.cmd, type_time=1.8, soft=True)
            ex3 = on_bar(t, extra_row())
            self.bar(ex3)
            r21 = out(self, t, OUT21, run_time=0.5)
            vo.wait_until("fix 1, an extra")
            f1 = beside(row_tag("fix 1 · plain build line", OWN), r21[0])
            pin(self, r21[0], f1)
            flash_tag(self, f1)
            vo.wait_until("On Apple silicon")
            self.play(FadeOut(VGroup(p3, bar19, bar17, m12)), run_time=0.5)
            self.play(FadeIn(plats[0], shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Elsewhere it means slow emulation")
            self.play(FadeIn(plats[1], shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("or this error")
            self.play(FadeIn(plats[2], shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(plats[2].text, color=ERR, scale_factor=1.08), run_time=0.6)

        # ========================================================== 4. the Pipfile: star, no lock
        pf = code("A/Pipfile", 8, 17)
        pf.move_to([-6.45 + pf.width / 2, 2.75 - pf.height / 2, 0])
        pf10 = line_bar(pf.code, 2, SHARED, 0.25)
        pf12 = line_bar(pf.code, 4, OWN, 0.25)
        gi = code("A/.gitignore", 67, 68)
        gi.move_to([-0.95 + gi.width / 2, 2.75 - gi.height / 2, 0])
        gi68 = line_bar(gi.code, 1, S.GREY, 0.3)
        gi_c = grey_chip("keeps a lock out of the repository").next_to(gi, DOWN, buff=0.15).align_to(gi, LEFT)
        df = code("A/Dockerfile", 52, 55, font_size=20, cuts={54: "# Generate Pipfile.lock"})
        df.move_to([6.45 - df.width / 2, 0.3 - df.height / 2, 0])
        df52 = line_bar(df.code, 0, ROUTE, 0.25)
        df55 = line_bar(df.code, 3, SHARED, 0.25)
        df_c = chip("the lock is made at build time", SHARED, size=20).next_to(df, DOWN, buff=0.18).align_to(df, RIGHT)
        assert pf.get_right()[0] < df.get_left()[0] - 0.2 and gi_c.get_right()[0] < 6.55, (pf.get_right(), df.get_left(), gi_c.get_right())
        assert df_c.get_bottom()[1] > -3.5 and gi_c.get_bottom()[1] > df.get_top()[1] + 0.1, (gi_c.get_bottom(), df.get_top())
        panels = VGroup(pf, pf10, pf12, gi, gi68, gi_c, df, df52, df55, df_c)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(plats), FadeOut(t), track(tr, 5), *self.unbar_anims(), run_time=0.6)
            self.remove(t)
            self.play(FadeIn(pf, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("TensorFlow is pinned")
            self.play(FadeIn(pf12), code_span(pf.code, 4, '"==2.18.0"').animate.set_color(OWN), run_time=0.5)
            self.add(pf, pf12)
            vo.wait_until("but SageMaker says star")
            self.play(FadeIn(pf10), code_span(pf.code, 2, '"*"').animate.set_color(SHARED), run_time=0.5)
            self.add(pf, pf12, pf10)
            self.play(Indicate(code_span(pf.code, 2, '"*"'), color=SHARED, scale_factor=1.5), run_time=0.7)
            self.add(pf, pf12, pf10)
            vo.wait_until("Git ignores the lock file")
            self.play(FadeIn(gi, shift=LEFT * 0.2), run_time=0.5)
            self.play(FadeIn(gi68), FadeIn(gi_c, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("and the Dockerfile runs pipenv lock")
            self.play(FadeIn(df, shift=LEFT * 0.2), FadeIn(df52), run_time=0.6)
            self.play(FadeIn(df55), code_span(df.code, 3, "pipenv lock").animate.set_color(SHARED), run_time=0.5)
            self.add(df, df52, df55)
            self.play(FadeIn(df_c, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 5. ponder
        with self.voiceover(SAY[5]) as vo:
            vo.wait_until("The code worked")
            self.play(panels.animate.set_opacity(0.25), run_time=0.8)
            vo.wait_until("Why does cli.py fail")
            self.play(Indicate(pf10, color=SHARED), run_time=0.8)
        card_p = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 6. V2: star is a constraint
        v = StarVsPin().shift(UP * 0.15)
        t = term(P_MD, rows=8, size=SIZE)
        self.t = t
        assert t.box.get_top()[1] < v.ticks.get_bottom()[1] - 0.1, (t.box.get_top(), v.ticks.get_bottom())
        chk = on_bar(t, extra_row("check"))

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(card_p), FadeOut(panels), run_time=0.5)
            self.play(FadeIn(v), run_time=0.6)
            v.star(self, run_time=0.8)
            self.play(Indicate(v.star_label, color=SHARED, scale_factor=1.1), run_time=0.6)
            v.heal(self)
            vo.wait_until("the resolver takes the newest release")
            v.resolve(self, "3.13.1", run_time=1.2)
            vo.wait_until("At the time of recording")
            self.play(FadeIn(t), track(tr, 5, "check"), run_time=0.5)
            self.bar(chk)
            room(self, t, 1)
            t.type(self, C22.cmd, type_time=0.8, wrap=False)
            r22 = out(self, t, [(L22[0], TURN)] + L22[1:], run_time=0.7)
            pin(self, r22[0], beside(time_row(), r22[0]))
            vo.wait_until("that is SageMaker SDK version 3")
            self.paint(r22[4], "sagemaker==3.13.1", ERR)
            self.play(Indicate(v.dot, color=ERR, scale_factor=1.2), run_time=0.6)
            v.heal(self)
            vo.wait_until("with PyTorch")
            self.paint(r22[6], "torch==2.8.0", SHARED, run_time=0.3)
            vo.wait_until("and 14 CUDA packages")
            self.paint(r22[2], "nvidia-cublas-cu12==12.8.4.1", SHARED, run_time=0.3)
            pin(self, r22[2], beside(row_tag("14 CUDA packages", SHARED), r22[2]), run_time=0.3)

        # ========================================================== 7. version 3: the imports find nothing
        with self.voiceover(SAY[7]) as vo:
            self.play(Indicate(v.dot, color=ERR, scale_factor=1.25), run_time=0.8)
            v.heal(self)
            self.reseat()
            self.wipe()
            self.resize(9)
            room(self, t, 1)
            t.type(self, C23.cmd, type_time=0.8, wrap=False)
            r23 = out(self, t, [(x, ERR) if k in (3, 5, 7) else x for k, x in enumerate(L23)], run_time=0.7)
            vo.wait_until("without the modules")
            self.play(Indicate(substring(r23[1], "['ai_registry'"), color=TURN, scale_factor=1.08), run_time=0.7)
            self.reseat()
            vo.wait_until("no tensorflow module")
            self.play(FadeOut(t), *self.unbar_anims(), run_time=0.4)
            self.remove(t)
            v.shelves(self, run_time=0.6)
            vo.wait_until("no serializers")
            v.imports(self, ok=False, run_time=1.4)
            vo.wait_until("The imports find nothing")
            self.play(Indicate(v.import_arrows[1], color=ERR, scale_factor=1.08), run_time=0.8)
            v.heal(self)

        # ========================================================== 8. here: 13 minutes, then no disk
        scrim = Rectangle(width=13.2, height=2.8 + 3.6, stroke_width=0).set_fill(S.BG, 0.95)
        scrim.move_to([0, (2.8 - 3.6) / 2, 0])
        note8 = card(["here: the unpinned build ran 13 min in pipenv lock,",
                      "then ran out of disk · not kept as a capture"], size=24)
        note8.move_to([0, 1.55, 0])
        bar_w = 4.6
        lk = mono("pipenv lock", 22, S.GREY)
        track_l = RoundedRectangle(width=bar_w, height=0.34, corner_radius=0.08, stroke_color=S.GREY,
                                   stroke_width=2).set_fill(S.BG, 1)
        lk.next_to(track_l, UP, buff=0.18).align_to(track_l, LEFT)
        here = VGroup(lk, track_l).move_to([-3.25, -0.55, 0])
        fill_l = Rectangle(width=0.01, height=0.26, stroke_width=0).set_fill(S.GREY, 0.8)
        fill_l.move_to(track_l.get_left() + RIGHT * 0.05, aligned_edge=LEFT)
        minutes = ValueTracker(0)
        cnt = label("0 min", 22, S.GREY).next_to(track_l, DOWN, buff=0.22)

        def upd_cnt(m):
            m.become(label(f"{int(minutes.get_value())} min", 22, S.GREY).next_to(track_l, DOWN, buff=0.22))
        disk = chip("disk full", ERR, size=22, fill_opacity=0.25).next_to(track_l, RIGHT, buff=0.25)
        lap = laptop_glyph(2.0).move_to([3.3, -0.35, 0])
        lap_l = label("on your laptop", 20, S.GREY).next_to(lap, UP, buff=0.15)
        track_r = RoundedRectangle(width=2.6, height=0.34, corner_radius=0.08, stroke_color=S.GREY,
                                   stroke_width=2).set_fill(S.BG, 1).next_to(lap, DOWN, buff=0.3)
        fill_r = Rectangle(width=2.5, height=0.26, stroke_width=0).set_fill(S.GREY, 0.8).move_to(track_r)
        imp = chip("ImportError", ERR, size=22, font=MONO, fill_opacity=0.25).next_to(track_r, DOWN, buff=0.25)
        assert imp.get_bottom()[1] > -3.5 and cnt.get_bottom()[1] > -3.5

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeIn(scrim), run_time=0.5)
            self.play(FadeIn(note8, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(here), FadeIn(cnt), run_time=0.4)
            self.add(fill_l)
            cnt.add_updater(upd_cnt)
            grow = vo.until("then ran out of disk", minimum=1.5)
            self.play(fill_l.animate.stretch_to_fit_width(bar_w - 0.6, about_edge=LEFT),
                      minutes.animate.set_value(13), run_time=grow, rate_func=linear)
            cnt.clear_updaters()
            self.play(FadeIn(disk, scale=1.6), run_time=0.4)
            self.play(Indicate(disk, color=ERR, scale_factor=1.1), run_time=0.5)
            vo.wait_until("On your laptop")
            self.play(FadeIn(lap), FadeIn(lap_l), FadeIn(track_r), run_time=0.5)
            fill_r.stretch_to_fit_width(0.01, about_edge=LEFT)
            fill_r.move_to(track_r.get_left() + RIGHT * 0.05, aligned_edge=LEFT)
            self.add(fill_r)
            self.play(fill_r.animate.stretch_to_fit_width(2.5, about_edge=LEFT),
                      run_time=vo.until("then fail at the first import", minimum=0.8), rate_func=linear)
            vo.wait_until("fail at the first import")
            self.play(FadeIn(imp, scale=1.6), run_time=0.4)
            self.play(Indicate(imp, color=ERR, scale_factor=1.1), run_time=0.5)
        side8 = VGroup(scrim, note8, here, fill_l, cnt, disk, lap, lap_l, track_r, fill_r, imp)

        # ========================================================== 9. fix 2: "<3"
        t = term(P_MD, rows=6, size=SIZE)
        self.t = t
        assert t.box.get_top()[1] < v.ticks.get_bottom()[1] - 0.2
        f2 = ok_chip("fix 2", size=22)
        yt9 = your_turn()

        with self.voiceover(SAY[9]) as vo:
            v.drop(self, v.shelf2, v.shelf3, v.src, v.import_arrows, extra=[FadeOut(side8)], run_time=0.6)
            v.shelf2 = v.shelf3 = v.src = v.import_arrows = None
            self.play(FadeIn(t), track(tr, 5, True), run_time=0.5)
            ln = type_cmd(self, t, C24.cmd, type_time=1.4, soft=True)
            pin(self, ln, beside(extra_row(), ln))
            r24 = out(self, t, [DIFF24[0], (DIFF24[1], ERR), (DIFF24[2], OWN), DIFF24[3]], run_time=0.5)
            vo.wait_until("The resolver stops")
            v.pin(self, run_time=1.6)
            f2.next_to(v.pin_label, RIGHT, buff=0.35)
            v.show(self, f2, run_time=0.4)
            vo.wait_until("and the imports work")
            self.play(FadeOut(t), run_time=0.4)
            self.remove(t)
            v.shelves(self, run_time=0.5)
            self.imports_ok(v)
            vo.wait_until("Pause and make both fixes")
            cap = v.caption(self, run_time=0.4)
            yt9.next_to(cap, RIGHT, buff=0.4)
            keep_inside(yt9)
            v.show(self, yt9, run_time=0.4)
            flash_tag(self, yt9)
            v.heal(self)

        # ========================================================== 10. step 5 again: it builds
        t = term(P_MD, rows=12, size=SIZE)
        self.t = t

        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(v), track(tr, 5), run_time=0.6)
            self.play(FadeIn(t), run_time=0.4)
            type_cmd(self, t, C25.cmd, type_time=0.7)
            r25 = out(self, t, OUT25[:1], run_time=0.4)
            vo.wait_until("It builds in almost 7 minutes")
            self.play(Indicate(substring(r25[0], "400.6s"), color=TURN, scale_factor=1.2), run_time=0.6)
            self.add(t)
            pin(self, r25[0], beside(time_row(), r25[0]))
            vo.wait_until("mostly locking and installing")
            r25b = out(self, t, [OUT25[1], (OUT25[2], TURN), OUT25[3]], run_time=0.5)
            self.play(Indicate(substring(r25b[1], "334.7s"), color=TURN, scale_factor=1.2), run_time=0.6)
            self.add(t)
            vo.wait_until("The AWS check fails")
            out(self, t, OUT25[4:], run_time=0.4)
            out(self, t, [(ERR25, ERR)], wrap=True, run_time=0.4)
            vo.wait_until("but the shell still opens")
            out(self, t, [LAUNCH25], run_time=0.3)
            pl = cd_prompt(self, t, P_APP)
            idc = beside(row_tag("the id changes every run"), pl)
            pin(self, pl, idc)

        # ========================================================== 11. inside: versions and values
        dep = under_term(t, grey_chip("deprecation warnings ahead: not the error"))

        with self.voiceover(SAY[11]) as vo:
            flash_tag(self, idc)
            self.reseat()
            self.wipe(track(tr, 5, True))
            ln = type_cmd(self, t, TYPED[0], type_time=0.9)
            pin(self, ln, beside(extra_row(), ln))
            r36 = out(self, t, C25.at(36), run_time=0.3)
            vo.wait_until("Python 3.9")
            self.play(Indicate(r36[0], color=TURN, scale_factor=1.08), run_time=0.5)
            self.add(t)
            type_cmd(self, t, TYPED[1], type_time=1.2, soft=True)
            r45 = out(self, t, C25.at(45, 47), run_time=0.4)
            vo.wait_until("SageMaker version 2")
            self.paint(r45[0], "2.257.7", OWN)
            pin(self, r45[0], beside(time_row(), r45[0]))
            vo.wait_until("and TensorFlow 2.18")
            self.paint(r45[1], "2.18.0", OWN)
            vo.wait_until("and the three values")
            type_cmd(self, t, TYPED[2], type_time=0.9)
            r49 = out(self, t, C25.at(49), wrap=True, run_time=0.4)
            self.play(*[Indicate(r, color=TURN, scale_factor=1.04) for r in r49], run_time=0.6)
            self.add(t)
            vo.wait_until("Deprecation warnings are not the error")
            self.play(FadeIn(dep, shift=DOWN * 0.1), run_time=0.4)
            flash_tag(self, dep)

        # ========================================================== 12. a small slip; 4 GB
        err_t = erratum_tag()
        kept = grey_chip("kept from the Google version · the commands are AWS")
        tags12 = VGroup(err_t, kept).arrange(RIGHT, buff=0.25)

        with self.voiceover(SAY[12]) as vo:
            self.wipe(FadeOut(dep))
            resize(self, t, 10)
            under_term(t, tags12)
            type_cmd(self, t, TYPED[3], type_time=0.7)
            out(self, t, HELP25[:1], wrap=True, run_time=0.3)
            rh = [None] + list(out(self, t, HELP25[1:], run_time=0.5))     # rh[k] = HELP25[k]
            vo.wait_until("A small slip")
            self.paint(rh[1], "Data Collector CLI", SHARED)
            self.play(FadeIn(tags12, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("GCS bucket")
            self.paint(rh[3], "GCS Bucket", SHARED)
            vo.wait_until("and Vertex AI")
            self.paint_many([(rh[4], "Vertex AI"), (rh[5], "Vertex AI"), (rh[6], "Vertex AI")], SHARED)
            vo.wait_until("and the test flag does nothing")
            dn = beside(row_tag("does nothing", SHARED), rh[6])
            pin(self, rh[6], dn)
            vo.wait_until("The commands are the AWS ones")
            flash_tag(self, kept)
            vo.wait_until("The image is about 4 gigabytes")
            self.wipe(FadeOut(tags12), retitle(t, "laptop · another tab"))
            t.set_prompt(P_MD)
            resize(self, t, 4, run_time=0.5)
            ln = type_cmd(self, t, C26.cmd, type_time=0.7)
            pin(self, ln, beside(extra_row(), ln))
            r26 = out(self, t, IMG26, run_time=0.4)
            self.paint(r26[1], "4.01GB", TURN)
            pin(self, r26[1], beside(time_row(), r26[1]))

        self.play(FadeOut(t), FadeOut(tr), run_time=0.8)
        self.remove(t, tr)
        self.wait(0.3)

    # ------------------------------------------------------------------ helpers
    def bar(self, tg):
        """Show a title-bar tag (on_bar) and remember it, so it fades with the terminal."""
        self.play(FadeIn(tg), run_time=0.3)
        self.bar_tags.append(tg)

    def unbar_anims(self):
        tgs, self.bar_tags = self.bar_tags, []
        return [FadeOut(tg) for tg in tgs]

    def unbar(self):
        a = self.unbar_anims()
        if a:
            self.play(*a, run_time=0.3)

    def resize(self, rows: int):
        """common.resize() with the title-bar tags riding along."""
        dy = (rows - self.t.rows) * self.t.pitch
        resize(self, self.t, rows, extra=[tg.animate.shift(UP * dy) for tg in self.bar_tags])

    def imports_ok(self, v, run_time: float = 1.2):
        """PLAYS: StarVsPin.imports(ok=True) drawn so that no arrow crosses a module chip: GREEN
        arrow from the cli.py:21-23 chip ends at the 2.x shelf's board, and the three modules cli.py
        imports turn GREEN."""
        names = ("tensorflow", "serializers", "get_execution_role")
        targets = [v.shelf2.items[n] for n in names]
        if v.src is None:
            v.src = chip("cli.py:21-23", TOOL, size=20, font=MONO).move_to(v.p(0, -2.2))
            v.show(self, v.src, run_time=0.3)
        board = v.shelf2[2]
        o = v.src.get_left() + RIGHT * 0.15
        end = np.array([board.get_center()[0] + 1.0, board.get_center()[1] - 0.06, 0])
        arrs = VGroup(Arrow(o, end, buff=0.08, color=OWN, stroke_width=4, tip_length=0.18))
        v.show(self, arrs, anims=[GrowArrow(arrs[0])], run_time=run_time * 0.4)
        self.play(*[tg[0].animate.set_stroke(OWN) for tg in targets],
                  *[tg[1].animate.set_color(OWN) for tg in targets], v.src[0].animate.set_stroke(OWN),
                  run_time=run_time * 0.3)
        v.heal(self)
        self.play(*[Indicate(tg[1], color=OWN, scale_factor=1.08) for tg in targets], run_time=run_time * 0.5)
        v.heal(self)
        v.import_arrows = arrs

    def wipe(self, *extra, run_time: float = 0.4):
        """PLAYS: the terminal's rows fade out (with `extra` alongside) and leave it for good."""
        t = self.t
        gone = list(t.lines.submobjects)
        for m in gone:
            t.lines.remove(m)
        if gone or extra:
            self.play(*[FadeOut(m) for m in gone], *extra, run_time=run_time)
        self.remove(*gone)
        self.reseat()

    def reseat(self):
        """Re-seat the terminal as one mobject (split trap) and keep its bar tags on top."""
        self.add(self.t, *self.bar_tags)

    def paint(self, row, sub, color, end_of_row: bool = False, run_time: float = 0.4):
        """Colour substring `sub` of terminal row `row` (end_of_row: from `sub` to the row's end)."""
        if end_of_row:
            i = row.text.index(sub)
            g = glyph_range(row, i)
        else:
            g = substring(row, sub)
        self.play(g.animate.set_color(color), run_time=run_time)
        self.reseat()

    def paint_many(self, pairs, color, run_time: float = 0.5):
        self.play(*[substring(r, s).animate.set_color(color) for r, s in pairs], run_time=run_time)
        self.reseat()
