"""S02 · Two stations, two buckets — the running map (V7) built, the recall quiz, clone + secrets.

Beats (script.md, ## S02; one voiceover block each):
0. No tracker. GREY `Lecture 11 · slides 4–6, 8–12` for the whole scene. Slide 6 redrawn
   (V7 .slide6_big): Unlabeled (six blank tiles) → the RED 'How do we do this?' arrow → Labeled
   (brie, gouda, parmigiano, gruyere) → GREY-dashed 'training · L13'. On "graded against" a GREY
   one-line card (slide 4); on "The model's mistakes" a GREY loop arrow training → Labeled.
1. Slide 6 shrinks into the thin strip; the stations build underneath as named: the labeling
   station (hollow TEAL houses on the planned street, 'command line / container' caption) ↔ BLUE
   bucket 1 (lights); the versioning station in GREY outlines (DVC house, bucket 2 with the GREY
   chip 'a new bucket or part 1's, scene 10', the repo with its flag stubs, Colab 'view versions');
   the GREY-dashed bridge, 'not connected / in the code / exercise E7'.
2. Slide 8's recall quiz: three GREY chips under the map; PONDER (8 s).
3. The answer (slides 10–12): 'Docker network' flies to the street, which lights PINK
   (data-labeling-network), a PINK arc from the CLI house to Label Studio by name; 'cloud
   credentials' flies to the GREEN secrets/ drawer + GOOGLE_APPLICATION_CREDENTIALS, GREEN pipes
   into every house; 'Docker Compose' flies to a GREY-dashed blanket over both houses, 'the README's
   Extra'; both houses light together.
4. Tracker A1. The map leaves; a full-width laptop terminal (20 pt: laptop/03's rows need 72
   characters) under README.md · line 14. `git clone …` → laptop/01:2, `cd data-labeling`; ▶ your
   turn on the output row; GREY chip over the terminal's right end (not spoken): laptop/00:4–6 +
   'at the time of recording'. README.md · line 18 card, `erratum`, chip 'now: Settings › Resources'.
5. Tracker A1 · extra; the terminal grows to 11 rows. `git log -1 --format='%H %ci'` → 02:2 (hash,
   then date ringed); `ls -la` → 03:2–19 (whitespace re-aligned only); the scripts (14–16), cli.py
   (10), then the three PNGs (9, 11, 17) flash; pipeline-flow.png ringed GREY with a GREY chip over
   the terminal (not spoken).
6. Tracker A2. 7-row terminal: `cd ..`, `mkdir secrets` (GREY chip 'the README shows a tree, not a
   command'), README.md · lines 37–40 card top right, ▶ your turn; `tree -L 1 .` (extra) → 05:2–6
   with the chip 'no tree? ls shows the same'; the two trees match folder for folder. The terminal
   leaves, the map returns (as S03 finds it: all outlines) and 'secrets' settles into V7 as the
   GREEN secrets/ drawer, outside every repo. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (ENV_VAR, IMAGE, INK, KEY, NARRATION, P_LABELING, P_LAPTOP_HOME, SAY_COUNT, TURN,
                    PipelineMap, beside, capture, card, cd_prompt, dashed_chip, each, erratum_tag, extra_row,
                    flash_tag, grey_chip, lit_house, lref, mono, out, outline_box, pin, ponder, readme,
                    readme_card, resize, ring, route, row_tag, substring, term, track, tracker, turn_row,
                    type_cmd, unpin)
from explainer import style as S

SAY = NARRATION["S02"]
TERM_PT = 20      # laptop/03's rows are 80 characters; re-aligned with one-space gutters they need 72 (20 pt)
PONDER_Q = "Docker network, cloud credentials,\nDocker Compose: where will each\none show up today?"
SLIDE4 = "labels = ground truth · labeled mistakes → the next version"


def realign(lines: list[str]) -> list[str]:
    """`ls -la` rows with their whitespace re-aligned (one-space gutters, numbers right-justified);
    the words are unchanged (asserted). 'total 696' stays as it is."""
    rows = [ln.split() for ln in lines]
    table = [r for r in rows if len(r) == 9]
    w = [max(len(r[j]) for r in table) for j in range(9)]
    right = {1, 4, 6}                                   # links, size, day
    res = []
    for ln, r in zip(lines, rows):
        if len(r) != 9:
            res.append(ln)
            continue
        cells = [r[j].rjust(w[j]) if j in right else r[j].ljust(w[j]) for j in range(8)] + [r[8]]
        s = " ".join(cells)
        assert s.split() == ln.split(), (s, ln)
        res.append(s)
    return res


def hollow_teal(h: VGroup) -> VGroup:
    """A copy of map house `h` drawn hollow TEAL (a container image not yet running)."""
    c = h.copy()
    for p in (c.body, c.roof):
        p.set_stroke(IMAGE).set_fill(S.BG, 1)
    if c.text is not None:
        c.text.set_color(IMAGE)
    return c


class TwoStations(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S02"] == 7, len(SAY)

        ref = lref("4–6, 8–12")
        m = PipelineMap.at("S02")
        big = m.slide6_big
        unl, a1, q, lab, a2, trn = big.unlabeled, big.arrows[0], big.question, big.labeled, big.arrows[1], big.training
        s4 = card([SLIDE4], size=22).move_to([0, -1.75, 0])
        loop = CurvedArrow(trn.get_top() + UP * 0.08, lab[0].get_top() + UP * 0.05 + RIGHT * 0.3, angle=PI / 3,
                           color=S.GREY, stroke_width=3, tip_length=0.18)

        # ========================================================== 0. slide 6: unlabeled → ? → labeled → training
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("The lecture draws unlabeled")
            self.play(Create(unl[0]), FadeIn(unl[2]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(x, scale=0.8) for x in unl[1]], lag_ratio=0.12), run_time=0.8)
            vo.wait_until("then labeled ones")
            self.play(Create(lab[0]), FadeIn(lab[2]), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in lab.rows], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("then training")
            self.play(GrowArrow(a2), FadeIn(trn, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("and the arrow in between")
            self.play(GrowArrow(a1), run_time=0.6)
            self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(q, color=S.RED, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Labels are the ground truth")
            self.play(each(list(lab.rows), INK, scale=1.12, lag=0.15), run_time=1.0)
            vo.wait_until("graded against")
            self.play(FadeIn(s4, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("The model's mistakes")
            self.play(Create(loop), run_time=1.0)
            vo.wait_until("go into the next dataset version")
            self.play(Indicate(lab[2], color=INK, scale_factor=1.15), run_time=0.7)

        # ========================================================== 1. the two stations, as the code builds them
        for k in ("studio", "cli"):
            m.houses[k].become(hollow_teal(m.houses[k]))
        b2chip = grey_chip("a new bucket or part 1's, scene 10")
        b2chip.next_to(m.bucket2, DOWN, buff=0.2)
        br = m.bridge

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(s4, loop)), run_time=0.5)
            self.remove(s4, loop)
            # slide 6 shrinks into the thin strip: frames become the chips' outlines, the words re-set
            # (common's to_strip() morphs a frame into a whole chip, which smears its word)
            st = m.slide6
            self.play(FadeOut(VGroup(unl[1], unl[2], lab.rows, lab[2])),
                      FadeOut(unl[0], target_position=st.items[0], scale=0.4),
                      FadeIn(st.items[0].box, target_position=unl[0], scale=2.0),
                      ReplacementTransform(lab[0], st.items[2].box),
                      ReplacementTransform(trn, st.items[3]), ReplacementTransform(q, st.items[1]),
                      ReplacementTransform(VGroup(a1, a2), VGroup(*[x for x in st if isinstance(x, Arrow)])),
                      run_time=1.2)
            self.play(FadeIn(st.items[0].text), FadeIn(st.items[2].text), run_time=0.4)
            self.remove(*big.get_family(), *st.get_family())
            self.add(st)
            vo.wait_until("Part 1 is the labeling station")
            self.play(FadeIn(m.lab), run_time=0.6)
            vo.wait_until("Label Studio")
            self.play(FadeIn(m.street), FadeIn(m.houses["studio"], shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("and a small command line container")
            self.play(FadeIn(m.houses["cli"], shift=DOWN * 0.15), FadeIn(m.cli_caption), run_time=0.6)
            vo.wait_until("with one bucket")
            self.play(FadeIn(m.bucket1, shift=LEFT * 0.2), run_time=0.5)
            self.play(m.light("bucket1"), run_time=0.6)
            self.play(each([d.text for d in m.bucket1.drawers.values()], INK, scale=1.08), run_time=0.7)
            vo.wait_until("Part 2 is the versioning station")
            self.play(FadeIn(m.ver), run_time=0.6)
            vo.wait_until("one DVC container")
            self.play(FadeIn(m.houses["dvc"], shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("a bucket with two folders")
            self.play(FadeIn(m.bucket2, shift=LEFT * 0.2), run_time=0.5)
            self.play(FadeIn(b2chip, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("your own GitHub repo")
            self.play(FadeIn(m.repo, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("and Colab to view versions")
            self.play(FadeIn(m.colab, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("The code does not connect")
            self.play(Create(br.line), run_time=0.6)
            self.play(Create(VGroup(br[1], br[2])), run_time=0.5)
            vo.wait_until("exercise E7 does")
            self.play(FadeIn(br.caption, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(br.caption[2], color=INK, scale_factor=1.12), run_time=0.6)
            # the map is one piece on the scene from here
            self.remove(m.lab, m.ver, m.street, *m.houses.values(), m.bucket1, m.bucket2, m.repo, m.colab,
                        br.line, br[1], br[2], br.caption)
            self.add(m)

        # ========================================================== 2. the recall quiz (slide 8)
        quiz = VGroup(grey_chip("Docker network"), grey_chip("cloud credentials"), grey_chip("Docker Compose"))
        quiz.arrange(RIGHT, buff=0.6).move_to([0, -2.3, 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(b2chip), run_time=0.4)
            self.remove(b2chip)
            for c, anchor in zip(quiz, ("Docker network", "cloud credentials", "Docker Compose")):
                vo.wait_until(anchor)
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.4)
            vo.wait_until("where will each one")
            self.play(each([c.text for c in quiz], TURN, scale=1.1, lag=0.2), run_time=1.0)
        pc = ponder(self, PONDER_Q, seconds=8, center=(0, 0.75))

        # ========================================================== 3. the answer: each chip to its spot
        hs, hc = m.houses["studio"], m.houses["cli"]
        by_name = route(np.array([hc.get_top()[0] - 0.15, hc.get_top()[1] + 0.02, 0]),
                        np.array([hs.get_top()[0] + 0.25, hs.get_top()[1] - 0.04, 0]), arc=0.8)
        env = mono(ENV_VAR, 20, KEY).move_to([-6.44, -1.75, 0], aligned_edge=LEFT)
        x0, x1 = hs.get_left()[0] - 0.06, hc.get_right()[0] + 0.06
        y0, y1 = m.street.band.get_bottom()[1] - 0.03, hs.get_top()[1] + 0.1     # houses and their street
        blanket = outline_box(x1 - x0, y1 - y0, S.GREY, solid=False).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        extra_lbl = dashed_chip("the README's Extra")
        extra_lbl.move_to([env.get_right()[0] + 0.3, -1.75, 0], aligned_edge=LEFT)
        # the lead leaves the blanket and runs in the gaps between the station frames (a line down
        # through the versioning station read as Compose belonging to part 2)
        lead_x = blanket.get_right()[0] - 0.3          # inside the blanket, above the gap
        gap_y = (m.lab.get_bottom()[1] + m.ver.get_top()[1]) / 2
        gap_x = (m.ver.get_right()[0] + m.bucket2.get_left()[0]) / 2
        assert m.ver.get_top()[1] < gap_y < m.lab.get_bottom()[1] and m.ver.get_right()[0] < gap_x < m.bucket2.get_left()[0]
        assert extra_lbl.get_left()[0] + 0.3 < gap_x < extra_lbl.get_right()[0] - 0.3
        lead_path = VMobject().set_points_as_corners([[lead_x, y0, 0], [lead_x, gap_y, 0], [gap_x, gap_y, 0],
                                                      [gap_x, extra_lbl.get_top()[1] + 0.04, 0]])
        lead = DashedVMobject(lead_path.set_stroke(S.GREY, 2), num_dashes=24, dashed_ratio=0.5)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(pc), run_time=0.5)
            self.remove(pc)
            vo.wait_until("The network lets")
            self.play(quiz[0].animate.move_to(m.street.band), run_time=0.8)
            self.play(FadeOut(quiz[0], scale=0.8), m.light("street"), run_time=0.7)
            self.remove(quiz[0])
            vo.wait_until("call Label Studio by name")
            self.play(Create(by_name), run_time=0.8)
            self.play(Indicate(hs.text, color=INK, scale_factor=1.15), run_time=0.6)
            vo.wait_until("The credentials are one key file")
            cx = max(m.secrets.get_center()[0], -6.5 + quiz[1].width / 2)
            self.play(FadeOut(by_name), quiz[1].animate.move_to([cx, m.secrets.get_center()[1], 0]), run_time=0.8)
            self.remove(by_name)
            self.play(FadeOut(quiz[1], scale=0.8), FadeIn(m.secrets, scale=1.1), FadeIn(env, shift=UP * 0.15),
                      run_time=0.6)
            self.remove(quiz[1])
            vo.wait_until("mounted into every container")
            self.play(FadeOut(m.cli_caption), run_time=0.3)
            self.remove(m.cli_caption)
            self.play(LaggedStart(m.pipe_on("studio"), m.pipe_on("cli"), m.pipe_on("dvc"), lag_ratio=0.3),
                      run_time=1.4)
            vo.wait_until("And Compose")
            self.play(quiz[2].animate.move_to(blanket), run_time=0.8)
            self.play(FadeOut(quiz[2], scale=0.8), Create(blanket.frame), run_time=0.7)
            self.play(Create(lead), FadeIn(extra_lbl, shift=UP * 0.15), run_time=0.6)
            self.remove(quiz[2])
            vo.wait_until("which starts both containers together")
            self.play(Transform(hs, lit_house(hs)), Transform(hc, lit_house(hc)), run_time=0.7)

        # ========================================================== 4. tracker A1: clone, cd, Docker memory
        tr = tracker("A", 1)
        t = term(P_LAPTOP_HOME, rows=5, size=TERM_PT)
        clone = capture("01")
        assert clone.cmd == "git clone https://github.com/dlops-io/data-labeling", clone.cmd
        r14 = readme(14).lstrip("* ")
        assert clone.cmd.split()[-1] in r14
        card14 = readme_card(14, r14).move_to([0, 2.0, 0])
        env_lines = capture("00").at(4, 5, 6)
        assert [s.split()[-1] if "client" not in s else s.split()[2].rstrip(",") for s in env_lines] == \
            ["29.8.2", "v5.6.0", "2.54.0"], env_lines
        envchip = row_tag("Docker 29.8.2 · Compose v5.6.0 · git 2.54.0 · at the time of recording")
        envchip.move_to([t.box.get_right()[0] - envchip.width / 2, t.box.get_top()[1] + 0.3, 0])
        r18 = readme(18)
        assert "Docker>Preferences>Resources" in r18 and "> 4GB" in r18
        card18 = readme_card(18, "Docker>Preferences>Resources … > 4GB")
        et = erratum_tag()
        now = grey_chip("now: Settings › Resources")
        row18 = VGroup(card18, et, now).arrange(RIGHT, buff=0.3).move_to([0, 0.55, 0])
        row18.align_to(card14, LEFT)

        with self.voiceover(SAY[4]) as vo:
            rest = [x for x in self.mobjects if x is not ref]
            self.play(FadeOut(Group(*rest)), run_time=0.7)
            self.remove(*rest)
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), FadeIn(card14, shift=DOWN * 0.15), run_time=0.7)
            self.play(FadeIn(envchip, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("Clone the data-labeling repo")
            type_cmd(self, t, clone.cmd, type_time=1.0)
            got = out(self, t, clone.at(2))
            vo.wait_until("and move into it")
            type_cmd(self, t, "cd data-labeling", type_time=0.5)
            cd_prompt(self, t, P_LABELING)
            vo.wait_until("pause and run it")
            yt = beside(turn_row(), got[0])
            pin(self, got[0], yt)
            flash_tag(self, yt, TURN)
            vo.wait_until("Give Docker more than")
            self.play(FadeIn(card18, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("as the README asks")
            self.play(FadeIn(et, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, et, INK)
            vo.wait_until("the setting is now under")
            self.play(FadeIn(now, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(now.text, color=INK, scale_factor=1.1), run_time=0.6)

        # ========================================================== 5. extras: the commit, the listing
        log, ls = capture("02"), capture("03")
        assert log.cmd == "git log -1 --format='%H %ci'" and ls.cmd == "ls -la", (log.cmd, ls.cmd)
        listing = realign(ls.at((2, 19)))
        assert max(len(s) for s in listing) <= t.max_chars
        head = log.at(2)[0]
        commit, date = head.split()[0], head.split()[1]
        assert commit.startswith("03c3e277") and date == "2025-10-20", head
        flow_chip = grey_chip("a version of this map, one bucket · no README links it")

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(card14, row18, envchip)), track(tr, extra=True), run_time=0.5)
            self.remove(card14, row18, envchip)
            resize(self, t, 11)
            ln = type_cmd(self, t, log.cmd, type_time=0.8)
            xt = beside(extra_row(), ln)
            pin(self, ln, xt)
            row = out(self, t, [head])[0]
            vo.wait_until("this video's commit")
            r1 = ring(substring(row, commit), TURN)
            self.play(Create(r1), run_time=0.5)
            vo.wait_until("from October 2025")
            r2 = ring(substring(row, date), TURN)
            self.play(ReplacementTransform(r1, r2), run_time=0.5)
            vo.wait_until("an extra listing")
            self.play(FadeOut(r2), run_time=0.3)
            self.remove(r1, r2)
            ln2 = type_cmd(self, t, ls.cmd, type_time=0.4)
            xt2 = beside(extra_row(), ln2)
            pin(self, ln2, xt2)
            out(self, t, listing, run_time=1.0, chunk=3)
            vo.wait_until("shows the scripts")
            scripts = ("docker-shell-CLI.sh", "docker-shell-compose.sh", "docker-shell.sh")
            # look-here flashes in place: the rows are white (an INK flash only scaled, and the long names
            # grew over the time column)
            self.play(each([substring(t.find(n), n) for n in scripts], TURN, scale=1.0, lag=0.2), run_time=0.9)
            vo.wait_until("cli.py")
            self.play(Indicate(substring(t.find("cli.py"), "cli.py"), color=TURN, scale_factor=1.0), run_time=0.6)
            vo.wait_until("and three pictures")
            pngs = ("cheeses-labels.png", "data-labeling-flow.png", "pipeline-flow.png")
            self.play(each([substring(t.find(n), n) for n in pngs], TURN, scale=1.0, lag=0.25), run_time=1.0)
            pf = ring(substring(t.find("pipeline-flow.png"), "pipeline-flow.png"), S.GREY)
            flow_chip.move_to([pf.get_center()[0] - 0.6, t.box.get_top()[1] + 0.42, 0])
            flow_chip.shift(LEFT * max(0, flow_chip.get_right()[0] - 6.4))
            self.play(Create(pf), FadeIn(flow_chip, shift=DOWN * 0.15), run_time=0.6)
            self.wait(1.2)

        # ========================================================== 6. tracker A2: the secrets folder, beside the repo
        mk, tree = capture("04"), capture("05")
        assert mk.cmd == "mkdir secrets" and mk.lines == [] and tree.cmd == "tree -L 1 .", (mk.cmd, tree.cmd)
        tree_rows = [readme(n) for n in (37, 38, 39, 40)]
        assert tree_rows[1:3] == ["|-data-labeling", "|-secrets"], tree_rows
        body = VGroup(*[mono(s, 22, S.GREY if s == "```" else INK) for s in tree_rows]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        card37 = readme_card((37, 40), body)
        m6 = PipelineMap.at("S02")

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(pf, flow_chip)), track(tr, 2, extra=False), run_time=0.5)
            self.remove(pf, flow_chip)
            resize(self, t, 7, keep=2)
            vo.wait_until("Next, the secrets folder")
            type_cmd(self, t, "cd ..", type_time=0.3)
            cd_prompt(self, t, P_LAPTOP_HOME)
            lm = type_cmd(self, t, mk.cmd, type_time=0.5)
            nt = beside(grey_chip("the README shows a tree, not a command"), lm)
            pin(self, lm, nt)
            vo.wait_until("beside the repo")
            card37.move_to([6.4 - card37.width / 2, t.box.get_top()[1] + 0.2 + card37.height / 2, 0])
            self.play(FadeIn(card37, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("never inside it")
            self.play(each([body[1], body[2]], INK, scale=1.1, lag=0.3), run_time=0.8)
            vo.wait_until("Pause and make it")
            unpin(self, lm, nt)
            yt2 = beside(turn_row(), lm)
            pin(self, lm, yt2)
            flash_tag(self, yt2, TURN)
            vo.wait_until("an extra tree view")
            unpin(self, lm, yt2)
            self.play(track(tr, extra=True), run_time=0.4)
            lt = type_cmd(self, t, tree.cmd, type_time=0.4)
            tc = beside(grey_chip("no tree? ls shows the same"), lt)
            pin(self, lt, tc)
            out(self, t, tree.at((2, 6)))
            vo.wait_until("matches the README")
            for name, rw in (("data-labeling", body[1]), ("secrets", body[2])):
                g = substring(t.find("── " + name), name)
                self.play(Indicate(g, color=TURN, scale_factor=1.15), Indicate(rw, color=TURN, scale_factor=1.1),
                          run_time=0.6)

        # the terminal leaves; the map returns as S03 finds it, and secrets/ settles into it
        sec = substring(t.find("└── secrets"), "secrets").copy()
        self.add(sec)
        keep = {id(x) for x in (ref, sec, *tr.get_family())}
        others = [x for x in self.mobjects if id(x) not in keep]
        self.play(FadeOut(Group(*others)), track(tr, extra=False), run_time=0.6)
        self.remove(*others)
        self.play(FadeIn(m6), FadeIn(m6.slide6), run_time=0.8)
        self.play(sec.animate.move_to(m6.secrets.text).set_color(INK), run_time=0.9)
        self.play(FadeIn(m6.secrets.box), FadeOut(sec), FadeIn(m6.secrets[1]), run_time=0.5)
        self.remove(sec, m6.secrets.box, m6.secrets[1])
        self.add(m6.secrets)
        self.play(Indicate(m6.secrets.text, color=KEY, scale_factor=1.2), run_time=0.7)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
