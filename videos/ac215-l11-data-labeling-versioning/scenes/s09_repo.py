"""S09 · A repo of your own, from the starter — concept opening (no tracker), then tracker G1 → G5;
`lref("20, 23, 26", low=True)` the whole scene.

Beats (script.md, ## S09; one voiceover block each):
0. No tracker. S08's YELLOW parked card returns alone ("how do you freeze which photos a model
   saw?"), then shrinks to the top-left edge. On "Git alone" a GREY sketch: one repo, three clones,
   each dragging a growing stack of photo versions. Slide 23's four approaches as four rows; the
   file-based row lights GREEN; on "git versions a small file" V6's 2 s GREY silhouette (chip
   "scene 13"); on "The tool is DVC" the PURPLE chip "DVC · today", then slide 20's five reasons as a
   card ("save space" YELLOW, chip "scene 14").
1. TRACKER G1. 10-row laptop terminal (20 pt: 72's squeezed table is 71 characters) at
   student@laptop:~/data-labeling$ beside README card line 136; `cd ..` → prompt ~; the GREY pin
   card (README @ b240b1a …); 70: 2 (squeeze), 71: 2–8 [y/N] y, 9, 72: 2–4 (squeeze); ▶ your turn.
2. TRACKER G2: the SSH clone (README:81, folds), no output panel, bar tag "this machine has no SSH
   route to GitHub"; README card line 84; TRACKER G2 · extra: the HTTPS clone → 74: 2, ▶ your
   turn. TRACKER G3: cd data-versioning → prompt; TRACKER G3 · extra: git log -1 … → 75: 2,
   `23762e49` and `2025-10-20` highlighted (not spoken).
3. Erratum: CODE(data-versioning@2515e5e/README.md: 76–82), tag `erratum`, line 78 over line 81
   RED. Second strip `laptop · second clone in ~/today` (extra): 131 clone → 131: 2; prompt
   ~/today/data-versioning; the strip grows, `ls -A` → 137: 2–12, `.dvc`, `.dvcignore`,
   `cheese_dataset.dvc` RED + chip "came with the clone". The strip closes; the first terminal
   returns.
4. TRACKER G3. README card line 104; rm -rf .git → (no output); git init → 77: 2, …, 15 (wrapped);
   ▶ your turn; `master` YELLOW. TRACKER G3 · extra: ls -A → 78: 2–9, chip "no .dvc/ · no class tags".
5. TRACKER G4: the GitHub new-repository form (`illustration`, README 106–110) over a 3-row strip,
   ▶ your turn. TRACKER G5: 79 → (no output), 80 (folds) → (no output) + the GREY HTTPS-origin card
   (`illustration`, not spoken), 81 → (no output), 82: 2–3 (hash: "yours will differ"), git push
   typed with no output panel; GREY card "on your machine: …7 files on main"; ▶ your turn; V7 over
   a 3-row strip, the repo box lights. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S09"]
DV = "data-versioning"
PARKED_Q = "how do you freeze which photos a model saw?"
APPROACHES = ("full snapshots", "table-based (logs, snapshots)", "object store (its own history)",
              "file-based (hashes + metadata, git keeps the history)")      # slide 23, script.md S09
REASONS = ("track changes", "roll back", "audit", "collaborate", "save space")  # slide 20
PIN_LINE = "README @ b240b1a · the course pin · the study guide links it"
PIN_URL = "github.com/dlops-io/data-versioning/blob/b240b1a/README.md"
NO_SSH = "this machine has no SSH route to GitHub"
HTTPS_ORIGIN = f"https://github.com/{GH_USER}/data-versioning.git"
SEVEN = "on your machine: your repo on GitHub shows these 7 files on main"
TS = 20                       # the main terminal's size (72 characters a row)
MAIN_ROWS = 10


def words(*parts, size: float = 20, color=INK) -> VGroup:
    """One row of label/mono pieces: plain strings are label font, ('x', 'mono') pieces mono."""
    ms = []
    for p in parts:
        if isinstance(p, tuple):
            ms.append(mono(p[0], size, color))
        else:
            ms.append(label(p, size, color))
    return VGroup(*ms).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)


def ask_line(s: str, bracket: str = "[y/N]") -> str:
    """The prompt line cut right after its bracket (the answer is typed separately)."""
    return s[:s.index(bracket) + len(bracket)]


def type_answer(scene, t, ln, key: str = "y") -> VGroup:
    """The answer keystroke after question row `ln`: the key appears after the bracket, flashes
    YELLOW, settles WHITE and joins the row."""
    y = mono_line(ln.text + " " + key, t.size, OUTPUT)
    y.shift(ln.strut.get_corner(UL) - y.strut.get_corner(UL))
    yg = y.glyphs[-1].set_color(TURN)
    scene.play(FadeIn(yg, scale=1.6), run_time=0.2)
    scene.play(Indicate(yg, color=TURN, scale_factor=1.8), run_time=0.45)
    scene.play(yg.animate.set_color(INK), run_time=0.2)
    attach(scene, ln, yg)
    return yg


def clone_sketch() -> VGroup:
    """'Git alone': one GREY repo box, three clone boxes under it, each with an (empty) stack spot.
    .repo .clones .arrows .spots (four anchor points: repo + three clones, right of each box)"""
    def bx(word):
        fr = RoundedRectangle(width=2.0, height=0.8, corner_radius=0.12, stroke_color=S.GREY, stroke_width=2.5)
        fr.set_fill(S.GREY_DARKER, 1)
        t = label(word, 22, INK).move_to(fr)
        g = VGroup(fr, t)
        g.frame = fr
        return g

    repo = bx("git repo").move_to([-1.0, 1.2, 0])
    clones = VGroup(*[bx("clone") for _ in range(3)])
    for c, x in zip(clones, (-5.0, -1.0, 3.0)):
        c.move_to([x, -1.4, 0])
    arrows = VGroup(*[arrow(repo.frame.get_bottom(), c.frame.get_top(), S.GREY) for c in clones])
    g = VGroup(repo, clones, arrows)
    g.repo, g.clones, g.arrows = repo, clones, arrows
    g.spots = [m.frame.get_right() + RIGHT * 0.55 for m in (repo, *clones)]
    return g


def version_tile(i: int, spot) -> VGroup:
    """Photo version i (0, 1, 2) stacked at `spot`: each newer copy sits up and right of the last."""
    return tile(None, 0.5, LAPTOP).move_to(spot + np.array([0.25 + i * 0.16, 0.05 + i * 0.12, 0]))


def approaches_card() -> VGroup:
    """Slide 23's four approaches, one row each (GREY bullets). .rows .texts"""
    rows, texts = [], []
    for s in APPROACHES:
        dot = Dot(radius=0.06, color=S.GREY)
        t = label(s, 24, INK)
        rows.append(VGroup(dot, t).arrange(RIGHT, buff=0.22))
        texts.append(t)
    c = card(rows, S.GREY, card_w=11.6, head="four ways to version data", buff=0.22)
    c.rows, c.texts = rows, texts
    return c


def reasons_card() -> VGroup:
    """Slide 20's five reasons in one row; 'save space' is .last."""
    items = [label(s, 24, INK) for s in REASONS]
    row = VGroup()
    for i, m in enumerate(items):
        row.add(m)
        if i < len(items) - 1:
            row.add(label("·", 24, S.GREY))
    row.arrange(RIGHT, buff=0.22)
    c = card([row], S.GREY, head="why version data")
    c.items, c.last = items, items[-1]
    return c


def github_form() -> VGroup:
    """The schematic GitHub new-repository page (README 106–110): name, Private, three empty boxes.
    .win .name .private .boxes"""
    win = window("github.com/new", 7.6, 3.9)
    name = VGroup(label("Repository name", 22, S.GREY),
                  VGroup(RoundedRectangle(width=3.2, height=0.48, corner_radius=0.06, stroke_color=S.GREY_DARK,
                                          stroke_width=1.5).set_fill(TERM_BG, 1))).arrange(RIGHT, buff=0.3)
    nv = mono(DV, 22, INK).move_to(name[1]).align_to(name[1], LEFT).shift(RIGHT * 0.15)
    name[1].add(nv)
    radio = VGroup(Circle(radius=0.12, stroke_color=INK, stroke_width=2),
                   Dot(radius=0.065, color=INK))
    priv = VGroup(radio, label("Private", 22, INK)).arrange(RIGHT, buff=0.2)
    boxes = VGroup()
    for s in ("Add a README file", "Add .gitignore", "Choose a license"):
        sq = Square(0.26, stroke_color=S.GREY, stroke_width=2)
        boxes.add(VGroup(sq, label(s, 22, INK)).arrange(RIGHT, buff=0.2))
    body = VGroup(name, priv, *boxes).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    body.move_to(win.content).align_to(win.content, LEFT).shift(RIGHT * 0.45)
    g = VGroup(win, body)
    g.win, g.name, g.private, g.boxes = win, name, priv, boxes
    return g


class YourOwnRepo(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S09"] == 6, len(SAY)

        # ========================================================== 0. part 2 opens: why not git alone
        ref = lref("20, 23, 26", low=True)
        q_big = card([label(PARKED_Q, 32, TURN)], TURN).move_to([0, 0.3, 0])
        q_small = label(PARKED_Q, 22, TURN).move_to([-6.5, 3.38, 0], aligned_edge=LEFT)
        sk = clone_sketch()
        stacks = [VGroup(*[version_tile(i, sp) for sp in sk.spots]) for i in range(3)]
        ap = approaches_card().move_to([0, 1.15, 0])
        si = TagRope().silhouette().move_to([-0.6, -2.2, 0])
        si_chip = grey_chip("scene 13").next_to(si, RIGHT, buff=0.5)
        dvc = tool_chip("DVC · today")
        rc = reasons_card().move_to([0, -2.25, 0])
        rc_chip = grey_chip("scene 14").next_to(rc.frame, DOWN, buff=0.12).align_to(rc.frame, RIGHT)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(q_big, scale=0.95), FadeIn(ref), run_time=0.8)
            self.play(Indicate(q_big.body, color=TURN, scale_factor=1.04), run_time=0.8)
            vo.wait_until("Git alone")
            self.play(ReplacementTransform(q_big.body[0], q_small), FadeOut(q_big.frame), run_time=0.7)
            self.play(FadeIn(sk.repo, scale=0.9), run_time=0.4)
            self.play(LaggedStart(*[GrowArrow(a) for a in sk.arrows], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in sk.clones], lag_ratio=0.2),
                      run_time=0.8)
            vo.wait_until("every photo version")
            for st in stacks:
                self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.12) for m in st], lag_ratio=0.1), run_time=0.45)
            vo.wait_until("into every clone")
            self.play(each(list(sk.clones), S.GREY, scale=1.06), run_time=0.8)
            vo.wait_until("Of the lecture's four approaches")
            self.play(FadeOut(VGroup(sk, *stacks)), run_time=0.5)
            self.remove(sk, *stacks)
            self.play(FadeIn(ap.frame), FadeIn(ap.head), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in ap.rows], lag_ratio=0.3), run_time=1.4)
            vo.wait_until("we build the file-based one")
            last = ap.rows[-1]
            band = hl_bar(last, PASS, 0.18, buff=0.1)
            self.play(FadeIn(band), last[1].animate.set_color(PASS), last[0].animate.set_color(PASS),
                      *[r.animate.set_opacity(0.55) for r in ap.rows[:-1]], run_time=0.6)
            vo.wait_until("git versions a small file")
            self.play(FadeIn(si, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(si_chip), Indicate(si[0][1], color=INK), run_time=0.6)
            vo.wait_until("and a bucket holds the photos")
            self.play(Indicate(si[0][2], color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("The tool is DVC")
            dvc.next_to(ap.frame, UP, buff=-0.62).align_to(ap.frame, RIGHT).shift(LEFT * 0.3)
            dvc.move_to([dvc.get_center()[0], last.get_center()[1] + 0.62, 0])
            self.play(FadeIn(dvc, scale=1.2), FadeOut(VGroup(si, si_chip)), run_time=0.6)
            self.remove(si, si_chip)
            self.play(FadeIn(rc, shift=UP * 0.2), run_time=0.5)
            self.play(rc.last.animate.set_color(TURN), FadeIn(rc_chip, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 1. G1: cd .., clean Docker
        tr = tracker("G", 1)
        t = term(P_LABELING, rows=MAIN_ROWS, size=TS)
        band_top, band_bot = 2.8, t.box.get_top()[1] + 0.12
        mid = (band_top + band_bot) / 2

        c136 = readme_card(136, words("Create a folder named", ("secrets", "mono"), "next to your",
                                      (DV, "mono"), "folder."), size=20, repo=DV)
        c136.move_to([0, mid, 0])
        pin_card = card([label(PIN_LINE, 20, INK), mono(PIN_URL, 20, S.GREY)], S.GREY, size=20, buff=0.1)
        pin_card.move_to([0, mid, 0]).align_to(np.array([-6.5, 0, 0]), LEFT)
        c70, c71, c72 = capture("70"), capture("71"), capture("72")
        assert c70.cmd in readme(57, DV) and c71.cmd in readme(65, DV) and c72.cmd in readme(71, DV)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(ap, band, dvc, rc, rc_chip, q_small)), run_time=0.5)
            self.remove(ap, band, dvc, rc, rc_chip, q_small)
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), run_time=0.6)
            self.play(FadeIn(c136, shift=DOWN * 0.15), run_time=0.5)
            type_cmd(self, t, "cd ..", type_time=0.3)
            ln = cd_prompt(self, t, P_LAPTOP_HOME)
            vo.wait_until("sits beside data-labeling and secrets")
            self.play(Indicate(c136.body[1], color=INK), Indicate(c136.body[3], color=INK), run_time=0.8)
            vo.wait_until("The data-versioning README")
            self.play(FadeOut(c136, shift=UP * 0.15), FadeIn(pin_card, shift=DOWN * 0.15), run_time=0.6)
            self.remove(c136)
            vo.wait_until("the same three cleanup commands")
            type_cmd(self, t, c70.cmd, type_time=0.5)
            out(self, t, squeeze(c70.at(2)), run_time=0.3)
            type_cmd(self, t, c71.cmd, type_time=0.5)
            out(self, t, c71.at((2, 7)), run_time=0.5)
            q = out(self, t, [ask_line(c71.line(8))], run_time=0.2)[-1]
            self.wait(0.6)
            type_answer(self, t, q)
            out(self, t, c71.at(9), run_time=0.3)
            ln72 = type_cmd(self, t, c72.cmd, type_time=0.5)
            out(self, t, squeeze(c72.at((2, 4))), run_time=0.4)
            vo.wait_until("Pause and run them")
            yt = beside(turn_row(), ln72)
            pin(self, ln72, yt)
            flash_tag(self, yt, TURN)

        # ========================================================== 2. G2: clone the starter, G3: move in
        ssh = readme(81, DV)
        c74, c75 = capture("74"), capture("75")
        bar_tag = on_bar(t, row_tag(NO_SSH))
        c84 = readme_card(84, "This command uses SSH. You need to add your public SSH key to GitHub first.\n"
                              "Alternatively, you can clone with HTTPS.", size=20, repo=DV)
        c84.move_to([0, mid, 0])
        dim84 = c84.body[0]

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(pin_card, shift=UP * 0.15), track(tr, 2), run_time=0.5)
            self.remove(pin_card)
            unpin(self, ln72, yt)
            ln_ssh = type_cmd(self, t, ssh, type_time=1.2)
            vo.wait_until("Its SSH command needs your key")
            self.play(FadeIn(c84, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("and this machine has no SSH route")
            self.play(FadeIn(bar_tag, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, bar_tag, INK)
            vo.wait_until("So the same branch comes over HTTPS")
            self.play(dim84.animate.set_opacity(0.45), Indicate(c84.body[1], color=INK, scale_factor=1.04),
                      track(tr, extra=True), run_time=0.7)
            ln74 = type_cmd(self, t, c74.cmd, type_time=1.0)
            xt = beside(extra_row(), ln74)
            pin(self, ln74, xt)
            r74 = out(self, t, c74.at(2), run_time=0.3)[-1]
            vo.wait_until("Pause, clone it")
            yt = beside(turn_row(), r74)
            pin(self, r74, yt)
            flash_tag(self, yt, TURN)
            vo.wait_until("and move in")
            self.play(FadeOut(VGroup(c84, bar_tag)), track(tr, 3), run_time=0.5)
            self.remove(c84, bar_tag)
            assert readme(89, DV) == "cd data-versioning"
            type_cmd(self, t, "cd data-versioning", type_time=0.4)
            cd_prompt(self, t, P_VERSIONING)
            ln75 = type_cmd(self, t, c75.cmd, type_time=0.5)
            xt2 = beside(extra_row(), ln75)
            pin(self, ln75, xt2, anim=AnimationGroup(FadeIn(xt2, shift=LEFT * 0.1), track(tr, extra=True)))
            r75 = out(self, t, c75.at(2), run_time=0.3)[-1]
            h1 = hl_bar(substring(r75, "23762e49"), TURN, 0.3)
            h2 = hl_bar(substring(r75, "2025-10-20"), TURN, 0.3)
            self.play(FadeIn(h1), FadeIn(h2), run_time=0.4)
            r75.submobjects.insert(0, h1)
            r75.submobjects.insert(0, h2)

        # ========================================================== 3. erratum: today's README says main
        p = code("data-versioning@2515e5e/README.md", 76, 82)
        s2 = second_term(3, P_TODAY, T_TODAY)
        p.move_to([0, (PIC_TOP + s2.box.get_top()[1] + 0.15) / 2, 0])
        er = erratum_tag()      # on the header row, right end (above the panel: the lref's corner)
        er.move_to([p.get_right()[0] - er.width / 2, p.header.get_center()[1], 0])
        bar78 = line_bar(p.code, 78 - 76, TURN)
        bar81 = line_bar(p.code, 81 - 76, ERR)
        c131, c137 = capture("131"), capture("137")
        red = (".dvc", ".dvcignore", "cheese_dataset.dvc")
        ls_lines = [(s, ERR) if s in red else s for s in c137.at((2, 12))]

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(t), FadeIn(p, shift=UP * 0.2), track(tr, extra=False), run_time=0.7)
            self.remove(t)
            self.play(FadeIn(er, shift=LEFT * 0.1), FadeIn(bar78), run_time=0.5)
            vo.wait_until("it now says to clone main")
            self.play(FadeIn(bar81), Indicate(code_span(p.code, 81 - 76, "main"), color=ERR, scale_factor=1.2),
                      run_time=0.8)
            vo.wait_until("That branch brings")
            self.play(FadeIn(s2, shift=UP * 0.2), track(tr, extra=True), run_time=0.5)
            type_cmd(self, s2, c131.cmd, type_time=0.9)
            out(self, s2, c131.at(2), run_time=0.3)
            cd_prompt(self, s2, P_TODAY_DV)
            vo.wait_until("as an extra second clone shows")
            self.play(FadeOut(VGroup(p, er, bar78, bar81)), run_time=0.4)
            self.remove(p, er, bar78, bar81)
            resize(self, s2, 12, keep=1, run_time=0.6)
            ln_ls = type_cmd(self, s2, c137.cmd, type_time=0.3)
            out(self, s2, ls_lines, run_time=0.6)
            hit = s2.find(".dvcignore")
            came = grey_chip("came with the clone")
            beside(came, hit, buff=1.2)
            self.play(FadeIn(came, shift=LEFT * 0.15),
                      each([s2.find(".dvc"), hit, s2.find("cheese_dataset.dvc")], ERR, scale=1.08), run_time=0.9)
            vo.wait_until("This video follows the course's pinned README")
            flash_tag(self, came, INK)
            vo.wait_until("the starter branch, plus one fix")
            self.play(FadeOut(VGroup(s2, came)), run_time=0.35)
            self.remove(s2, came)
            self.play(FadeIn(t), track(tr, 3, extra=False), run_time=0.45)

        # ========================================================== 4. G3: rm -rf .git, git init
        c104 = readme_card(104, words("Why remove", (".git", "mono"), "? The cloned repository is connected "
                                      "to the original class repository."), size=20, repo=DV)
        c104.move_to([0, mid, 0])
        c76, c77, c78 = capture("76"), capture("77"), capture("78")
        assert c76.cmd == readme(95, DV) and c77.cmd == readme(101, DV)
        no_dvc = grey_chip("no .dvc/ · no class tags")
        no_dvc.move_to([0, mid, 0]).align_to(np.array([6.5, 0, 0]), RIGHT)

        with self.voiceover(SAY[4]) as vo:
            unpin(self, ln75, xt2)
            self.play(FadeIn(c104, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("Remove the old git history")
            type_cmd(self, t, c76.cmd, type_time=0.4)
            bare_prompt(self, t)
            vo.wait_until("and start fresh with git init")
            ln77 = type_cmd(self, t, c77.cmd, type_time=0.3)
            out(self, t, c77.at(2, "…", 15), wrap=True, run_time=0.6)
            vo.wait_until("Pause and run both")
            yt3 = beside(turn_row(), ln77)
            pin(self, ln77, yt3)
            flash_tag(self, yt3, TURN)
            vo.wait_until("Git's hint mentions master")
            hm = t.find("'master'")
            hb = hl_bar(substring(hm, "master"), TURN, 0.3)
            self.play(FadeIn(hb), substring(hm, "master").animate.set_color(TURN), run_time=0.5)
            hm.submobjects.insert(0, hb)
            vo.wait_until("which is why the branch gets renamed next")
            self.play(Indicate(substring(hm, "master"), color=TURN, scale_factor=1.15), run_time=0.6)
            # extra, not spoken: the clean start
            self.play(FadeOut(c104), track(tr, extra=True), run_time=0.4)
            self.remove(c104)
            unpin(self, ln77, yt3)
            ln78 = type_cmd(self, t, c78.cmd, type_time=0.3)
            xt3 = beside(extra_row(), ln78)
            pin(self, ln78, xt3)
            out(self, t, c78.at((2, 9)), run_time=0.6)
            self.play(FadeIn(no_dvc, shift=DOWN * 0.15), run_time=0.5)
            flash_tag(self, no_dvc, INK)

        # ========================================================== 5. G4 new repo, G5 first push, V7
        form = github_form()
        ill = illustration_tag()
        yt4 = your_turn()
        c79, c80, c81, c82 = capture("79"), capture("80"), capture("81"), capture("82")
        assert [c.cmd for c in (c79, c80, c81, c82)] == [readme(n, DV) for n in range(121, 125)]
        push = readme(125, DV)
        https_card = card([words("no SSH key? use", (HTTPS_ORIGIN, "mono")),
                           label("as origin · GitHub asks for a token, not your password", 20, INK)],
                          S.GREY, size=20, buff=0.1)
        seven = card([label(SEVEN, 22, INK)], S.GREY)
        m = PipelineMap.at("S09")

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(no_dvc), track(tr, 4, extra=False), run_time=0.5)
            self.remove(no_dvc)
            unpin(self, ln78, xt3)
            resize(self, t, 3, run_time=0.6)
            form.move_to([-0.9, (PIC_TOP + t.box.get_top()[1] + 0.15) / 2, 0])
            ill.next_to(form, RIGHT, buff=0.2).align_to(form, UP)
            yt4.next_to(ill, DOWN, buff=0.25).align_to(ill, LEFT)
            self.play(FadeIn(form, shift=UP * 0.2), FadeIn(ill), run_time=0.7)
            vo.wait_until("private repo called data-versioning")
            self.play(Indicate(form.name[1], color=INK, scale_factor=1.05),
                      Indicate(form.private, color=INK, scale_factor=1.08), run_time=0.8)
            vo.wait_until("with no README")
            self.play(each(list(form.boxes), INK, scale=1.06, lag=0.25), run_time=1.0)
            self.play(FadeIn(yt4, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("Then the five commands")
            self.play(FadeOut(VGroup(form, ill, yt4)), track(tr, 5), run_time=0.5)
            self.remove(form, ill, yt4)
            resize(self, t, 9, run_time=0.5)
            https_card.move_to([0, (2.8 + t.box.get_top()[1] + 0.12) / 2, 0])
            ill2 = illustration_tag().move_to(https_card.frame.get_corner(UR) + np.array([-1.1, 0, 0]))
            type_cmd(self, t, c79.cmd, type_time=0.4)
            bare_prompt(self, t)
            vo.wait_until("add your repo as origin")
            type_cmd(self, t, c80.cmd, type_time=0.8)
            bare_prompt(self, t)
            self.play(FadeIn(https_card, shift=DOWN * 0.15), FadeIn(ill2), run_time=0.5)
            vo.wait_until("add, commit")
            type_cmd(self, t, c81.cmd, type_time=0.2)
            bare_prompt(self, t)
            type_cmd(self, t, c82.cmd, type_time=0.4)
            r82 = out(self, t, c82.at((2, 3)), run_time=0.4)
            dc = beside(differ_chip(), r82[0], buff=0.4)
            pin(self, r82[0], dc)
            vo.wait_until("and push")
            ln_push = type_cmd(self, t, push, type_time=0.4)
            vo.wait_until("Pause and run them")
            yt5 = beside(turn_row(), ln_push)
            pin(self, ln_push, yt5)
            seven.move_to(https_card)
            self.play(FadeOut(VGroup(https_card, ill2)), FadeIn(seven, shift=DOWN * 0.15), run_time=0.5)
            self.remove(https_card, ill2)
            flash_tag(self, yt5, TURN)
            vo.wait_until("Your repo now shows the 7 files on main")
            self.play(Indicate(seven.body, color=INK, scale_factor=1.03), run_time=0.6)
            self.play(FadeOut(seven), run_time=0.3)
            self.remove(seven)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(m), run_time=0.6)
            self.play(m.light("repo"), run_time=0.8)
            self.play(Indicate(m.repo, color=LAPTOP, scale_factor=1.06), run_time=0.7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
