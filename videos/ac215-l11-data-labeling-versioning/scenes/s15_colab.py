"""S15 · Time travel from anywhere — tracker J6 (chip 'from scene 13') → K5; `lref("22, 26")` the whole scene.

Beats (script.md, ## S15; one voiceover block each):
0. TRACKER J6 + GREY chip "from scene 13"; V7 (`PipelineMap.at("S15")`) lights Colab on "from anywhere"
   while the tracker turns into K5. Slide 22's term card: time travel · reaching an earlier version ·
   only while its files are kept. V6: `dvc get <repo> cheese_dataset --rev <tag>`; the BLUE Colab box
   clones at the tag, the '.dvc/config · which bucket' chip, the manifest, then the blobs; four blank
   tiles land in Colab.
1. The notebook frame (`illustration`; README 326 / 383, slide 26): cell 5's "Save a copy", the GREY
   newer-copy note (18KYngbv), then cells 7, 9 (chip "keep it: it imports auth"), 11; page 2: cells
   13, 15, 17, verbatim from notebook-1RRQ1SlH.cells.txt. No ▶ yet.
2. Strip `colab stand-in · signed out`, tag `extra`: `dvc --version` → C07b:2 + chips; `dvc list -R …`
   → C13:5 from "Anonymous caller" (wrap), RED, `.dir` YELLOW. The strip shrinks to 3 rows; V6: the
   rope from Colab stops at the class bucket's manifest with a RED 401. Extra laptop strip: 122's
   anonymous listing → 4–5 RED.
3. `recorded` card (cells 13, 15, 17 stored outputs) + chip "the class repo's main · …"; then the
   notebook's edited cells 13 / 15 GREEN (YOUR_GITHUB_USERNAME, dataset_v20), chip "your v20 gives 4",
   the GREY private-repo card (`illustration`, placeholder token), ▶ your turn.
4. Cell 19 in the notebook; the stand-in strip types C19 → the prompt returns. PONDER 6 s.
5. Cell 20 → C20 2–4 RED; C19b (extra) → 2, RED; laptop strip 118 (extra) → 2, 4, 6, the three tag
   names YELLOW; V6's ghost flag dataset_v25, its rope ending in air; the erratum card. Fade out.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S15"]
NB = "colab/notebook-1RRQ1SlH.cells.txt"
DV = "data-versioning"
NB_SIZE = 20
FR_W = 12.6
NEWER = ("today's README links a newer copy of this notebook (18KYngbv)",
         "same cells, pointed at a TA's repo",
         "point them at your repo either way")
PRIVATE_URL = ("https://YOUR_GITHUB_USERNAME:<read-only token>@", "github.com/YOUR_GITHUB_USERNAME/data-versioning")
PONDER_Q = "Cell 19 — dvc get … --quiet\n--rev dataset_v25 — prints nothing.\nDid it work?"


# ------------------------------------------------------------------ notebook drawing (illustration)
def nb_fold(s: str, n: int, indent: int = 4) -> list[str]:
    """A long line broken at its last space that fits n characters (a token longer than a row
    breaks at the edge); continuation rows indented. The text is unchanged."""
    parts, first = [], True
    while len(s) > n - (0 if first else indent):
        w = n - (0 if first else indent)
        k = s.rfind(" ", 0, w + 1)
        if k <= 0:
            parts.append(s[:w])
            s = s[w:]
        else:
            parts.append(s[:k])
            s = s[k + 1:]
        first = False
    parts.append(s)
    return [(" " * indent if i else "") + p for i, p in enumerate(parts)]


def rows_block(items, size: float = NB_SIZE) -> VGroup:
    """(text, colour) items as mono rows: strut left at x 0, row i centred at y -i*pitch."""
    pitch = line_pitch(size)
    g = VGroup()
    for i, (s, c) in enumerate(items):
        r = mono_line(s, size, c)
        r.shift(np.array([-r.strut.get_left()[0], -i * pitch - r.strut.get_center()[1], 0]))
        g.add(r)
    return g


def src(n: int) -> str:
    return excerpt(NB, n, n)


def src_item(n: int, colour=None):
    s = src(n)
    return (s, colour or (S.GREY if s.lstrip().startswith("#") else INK))


def nb_cell(num, items, cell_w: float = 11.05, stroke=S.GREY, size: float = NB_SIZE, gutter: str | None = None):
    """One notebook cell: GREY gutter label 'cell n', a box holding the given (text, colour) lines
    (folded at the box's edge). .num .box .rows .parts (one VGroup of rows per item)."""
    n = int((cell_w - 0.4) / cell_width(size))
    flat, owner = [], []
    for j, (s, c) in enumerate(items):
        for p in nb_fold(s, n):
            flat.append((p, c))
            owner.append(j)
    pitch = line_pitch(size)
    rows = rows_block(flat, size)
    bx = RoundedRectangle(width=cell_w, height=len(flat) * pitch + 0.3, corner_radius=0.1, stroke_color=stroke,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    rows.shift(np.array([bx.get_left()[0] + 0.2, bx.get_top()[1] - 0.15 - pitch / 2, 0]))
    num_l = label(gutter or f"cell {num}", 20, S.GREY)
    num_l.next_to(bx, LEFT, buff=0.2).align_to(bx, UP).shift(DOWN * 0.1)
    g = VGroup(bx, rows, num_l)
    g.box, g.rows, g.num = bx, rows, num_l
    g.parts = [VGroup(*[rows[i] for i in range(len(flat)) if owner[i] == j]) for j in range(len(items))]
    return g


def nb_frame(top: float = 2.75, bottom: float = -3.45) -> VGroup:
    """The schematic notebook window (no screenshot): GREY frame, title 'notebook · 1RRQ1SlH', a rule
    under it, the `illustration` tag on the title row. .frame .title .tag; content starts at .content_top."""
    fr = RoundedRectangle(width=FR_W, height=top - bottom, corner_radius=0.16, stroke_color=LAPTOP,
                          stroke_width=2.5).set_fill(S.BG, 1).move_to([0, (top + bottom) / 2, 0])
    tt = mono(shown_path(NB), 20, S.GREY).move_to([-FR_W / 2 + 0.25, top - 0.3, 0], aligned_edge=LEFT)
    rule = Line([-FR_W / 2, top - 0.6, 0], [FR_W / 2, top - 0.6, 0], color=S.GREY_DARK, stroke_width=2)
    tg_ = illustration_tag()
    tg_.move_to([FR_W / 2 - 0.2 - tg_.width / 2, top - 0.3, 0])
    g = VGroup(fr, rule, tt, tg_)
    g.frame, g.title, g.tag = fr, tt, tg_
    g.content_top = top - 0.8
    return g


def stack(cells, top_y: float, gap: float = 0.2):
    """Place cells top to bottom (their boxes' right edges at the frame's inner right)."""
    y = top_y
    for c in cells:
        c.shift(np.array([FR_W / 2 - 0.2 - c.box.get_right()[0], y - c.box.get_top()[1], 0]))
        y = c.box.get_bottom()[1] - gap
    return VGroup(*cells)


def words(*parts, size: float = 22) -> VGroup:
    """A row of label/mono pieces: str → label INK; (s, 'mono', colour) → mono; (s, colour) → label."""
    ms = []
    for p in parts:
        if isinstance(p, str):
            ms.append(label(p, size, INK))
        elif len(p) == 3:
            ms.append(mono(p[0], size, p[2]))
        else:
            ms.append(label(p[0], size, p[1]))
    return VGroup(*ms).arrange(RIGHT, buff=0.12)


class TimeTravel(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S15"] == 6, len(SAY)
        c07b, c13, c19, c19b, c20 = (capture(k) for k in ("C07b", "C13", "C19", "C19b", "C20"))
        c118, c122 = capture("118"), capture("122")
        assert "Open the [Colab Notebook]" in readme(326, DV) and "Open the [Colab Notebook]" in readme(383, DV)
        assert "1RRQ1SlH" in readme(326, DV) and "1RRQ1SlH" in readme(383, DV)
        assert src(47) == "!pip install dvc dvc-gs" and src(292) == "auth.authenticate_user()"
        assert src(303) == "!dvc list -R https://github.com/dlops-io/data-versioning.git"
        assert src(329).endswith("--rev dataset_v21") and src(362).endswith("--quiet --rev dataset_v25")
        assert src(355) == "Number of items: 5" and src(370) == "Number of items: 3"

        # ========================================================== 0. J6 → K5: time travel, the rope pull
        ref = lref("22, 26")
        tr = tracker("J", 6)
        from13 = grey_chip("from scene 13").next_to(tr.caption, RIGHT, buff=0.3).shift(DOWN * 0.14)
        m = PipelineMap.at("S15")
        term_card = card([label("time travel", 44, TURN), label("reaching an earlier version", 32, INK),
                          label("only while its files are kept", 32, INK)],
                         head="slide 22 · the lecture's term", buff=0.22).move_to([0, 0.2, 0])
        tg = TagRope()
        shown = [tg.beads[1], tg.beads[2], tg.bead_labels[1], tg.bead_labels[2], tg.flags["dataset_v20"],
                 tg.flags["dataset_v21"], tg.dirs["v20"], tg.dirs["v21"], *tg.blobs.values()]
        cmd = VGroup(mono("dvc get", 24, TOOL), mono("<repo> cheese_dataset --rev <tag>", 24, INK))
        cmd.arrange(RIGHT, buff=0.2).move_to([0, -2.55, 0])

        self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(from13, shift=LEFT * 0.1),
                  FadeIn(m), run_time=0.8)
        self.play(Indicate(from13.text, color=INK, scale_factor=1.08), run_time=0.7)

        with self.voiceover(SAY[0]) as vo:
            vo.wait_until("from anywhere")
            self.play(FadeOut(from13), run_time=0.3)
            self.remove(from13)
            tr = swap_tracker(self, tr, tracker("K", 5), m.light("colab"), run_time=0.8)
            self.play(Indicate(m.colab, color=CLOUD, scale_factor=1.06), run_time=0.6)
            vo.wait_until("the lecture's phrase")
            self.play(FadeOut(m), run_time=0.5)
            self.remove(m)
            self.play(FadeIn(term_card, scale=0.96), run_time=0.6)
            vo.wait_until("reaching an earlier version")
            self.play(Indicate(term_card.body[1], color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("which works only while")
            self.play(Indicate(term_card.body[2], color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("The command dvc get")
            self.play(FadeOut(term_card, shift=UP * 0.2), run_time=0.4)
            self.remove(term_card)
            self.play(FadeIn(tg), *[FadeIn(x) for x in shown], FadeIn(cmd, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("with a tag")
            self.play(Indicate(tg.flags["dataset_v20"].text, color=POINTER, scale_factor=1.15),
                      Indicate(cmd[1], color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("It clones the repo")
            tiles = tg.pull(self, "v20")
            self.play(Indicate(tiles, color=CLOUD, scale_factor=1.1), run_time=0.6)

        # ========================================================== 1. the notebook, cell by cell
        v6 = VGroup(tg, *shown, tg.colab, tg.config, tiles, cmd)
        fr1 = nb_frame()
        c326 = card([label("Open the Colab Notebook", 24, INK),
                     mono("colab.research.google.com/drive/1RRQ1SlH…", 20, S.GREY),
                     label("slide 26 links the same notebook", 20, S.GREY)],
                    head="data-versioning · README.md · lines 326 and 383")
        c5 = card([mono(src(41), 20, INK)], head="notebook · cell 5")
        newer = card([label(s, 20, INK if i == 0 else S.GREY) for i, s in enumerate(NEWER)], size=20)
        VGroup(c326, c5, newer).arrange(DOWN, buff=0.25).move_to([0, fr1.content_top - 2.5, 0])
        page1 = stack([nb_cell(7, [src_item(47)]),
                       nb_cell(9, [src_item(n) for n in range(276, 284)]),
                       nb_cell(11, [src_item(291), src_item(292)])], fr1.content_top)
        auth_row = page1[1].parts[6]                      # line 282: from google.colab import auth
        keep = grey_chip("keep it: it imports auth")
        keep.move_to([page1[1].box.get_right()[0] - 0.25 - keep.width / 2, auth_row.get_center()[1], 0])
        page2 = stack([nb_cell(13, [src_item(302), src_item(303)]),
                       nb_cell(15, [src_item(328), src_item(329)]),
                       nb_cell(17, [src_item(352), src_item(353)])], fr1.content_top)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(v6), run_time=0.5)
            self.remove(*v6.get_family())
            self.play(FadeIn(fr1), FadeIn(c326, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("and save a copy")
            self.play(FadeIn(c5, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(newer, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Install DVC")
            gone = VGroup(c326, c5, newer)
            self.play(FadeOut(gone), run_time=0.4)
            self.remove(*gone.get_family())
            self.play(FadeIn(page1[0], shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(page1[0].rows, color=TOOL, scale_factor=1.04), run_time=0.5)
            vo.wait_until("load the libraries")
            self.play(FadeIn(page1[1], shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(keep, shift=LEFT * 0.15), Indicate(auth_row, color=TURN, scale_factor=1.06),
                      run_time=0.6)
            vo.wait_until("and sign in")
            self.play(FadeIn(page1[2], shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(page1[2].parts[1], color=TURN, scale_factor=1.05), run_time=0.5)
            vo.wait_until("Then list a repo")
            self.play(FadeOut(VGroup(page1, keep), shift=UP * 0.3), FadeIn(page2[0], shift=UP * 0.3), run_time=0.6)
            self.remove(*page1.get_family(), *keep.get_family())
            vo.wait_until("fetch a version")
            self.play(FadeIn(page2[1], shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(substring(page2[1].parts[1][-1], "dataset_v21"), color=POINTER, scale_factor=1.1),
                      run_time=0.5)
            vo.wait_until("and count the files")
            self.play(FadeIn(page2[2], shift=UP * 0.15), run_time=0.5)

        # ========================================================== 2. the signed-out stand-in: 401 at the manifest
        t = colab_term(rows=8)
        xt = on_bar(t, extra_row())
        pip_chip = grey_chip("today's pip · the notebook ran 3.63.0")
        tail = c13.line(5)
        tail = tail[tail.index("Anonymous caller"):]
        tg2 = TagRope()
        tg2.dirs["class"] = blob(CLASS_V21["md5"]).move_to(tg2.dirs["v21"])
        cls_chip = dashed_chip("class bucket").next_to(tg2.store.frame, UP, buff=0.12).align_to(tg2.store.frame, RIGHT)
        lt = term(P_LAPTOP_HOME, rows=11, title=T_LAPTOP, size=20)
        lxt = on_bar(lt, extra_row())

        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(fr1, page2)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(*gone.get_family())
            self.play(FadeIn(t), FadeIn(xt), run_time=0.5)
            ln = type_cmd(self, t, c07b.cmd, type_time=0.4)
            vo.wait_until("pip gives it a newer DVC")
            r07 = out(self, t, [c07b.line(2)], run_time=0.3)
            vo.wait_until("3.67.1")
            pip_chip.next_to(t.box, UP, buff=0.15).align_to(t.box, RIGHT)
            ttag = beside(time_row(), r07[0])
            pin(self, r07[0], ttag, anim=AnimationGroup(FadeIn(ttag, shift=LEFT * 0.1), FadeIn(pip_chip, shift=DOWN * 0.1)))
            self.play(Indicate(r07[0], color=INK, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Listing the class repo")
            unpin(self, r07[0], ttag)
            self.play(FadeOut(pip_chip), run_time=0.3)
            self.remove(pip_chip)
            type_cmd(self, t, c13.cmd, type_time=0.8)
            vo.wait_until("fails with")
            r13 = out(self, t, ["…"] + [(s, ERR) for s in soft([tail], t.max_chars)], run_time=0.8)
            dir_row = next(r for r in r13 if ".dir'" in r.text)
            self.play(substring(dir_row, ".dir").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("and look where")
            self.play(FadeOut(xt), run_time=0.2)
            self.remove(xt)
            resize(self, t, 3, run_time=0.6)
            xt = on_bar(t, extra_row())
            self.play(FadeIn(xt), FadeIn(tg2.colab), FadeIn(tg2.store), FadeIn(tg2.dirs["class"]),
                      FadeIn(cls_chip), run_time=0.6)
            vo.wait_until("at the manifest")
            stop = tg2.stop_at_manifest(self, "class")
            vo.wait_until("because DVC fetches the list first")
            self.play(Indicate(tg2.dirs["class"].text, color=TURN, scale_factor=1.15),
                      Indicate(substring(dir_row, ".dir"), color=TURN, scale_factor=1.3), run_time=0.8)
            vo.wait_until("in the rope's order")
            gone = VGroup(t, *t.lines, xt, tg2.colab, tg2.store, tg2.dirs["class"], cls_chip, stop)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(*gone.get_family())
            self.play(FadeIn(lt), FadeIn(lxt), run_time=0.4)
            type_cmd(self, lt, c122.cmd, type_time=0.8, soft=True)
            r122 = out(self, lt, [(s, ERR) for s in soft(c122.at(4, 5), lt.max_chars)], run_time=0.5)
            self.play(Indicate(substring(r122[0], "401"), color=ERR, scale_factor=1.3), run_time=0.6)
            self.wait(1.2)

        # ========================================================== 3. what success looks like; your repo
        def stored(head, rows_):
            return VGroup(label(head, 20, S.GREY), rows_block(rows_)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        lst = []
        for n in range(310, 315):
            lst += [(p, INK) for p in nb_fold(src(n), 48)]
        s13 = stored("cell 13 · stored output", lst)
        s15 = stored("cell 15 · stored output", [(cut(src(331), "0/5"), INK)])
        s17 = stored("cell 17 · stored output", [(src(355), INK)])
        rec = card([s13, s15, s17], size=20, buff=0.28)
        rec.move_to([-6.3 + rec.width / 2, 0, 0]).align_to(np.array([0, 2.2, 0]), UP)
        rtag = recorded_tag("recorded · notebook cells 13, 15, 17 · the instructor's run of the class repo")
        rtag.next_to(rec, UP, buff=0.15).align_to(rec, LEFT)
        main_chip = VGroup(label("the class repo's main", 20, INK), label("the same five files as its v21", 20, S.GREY))
        main_chip.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        mframe = RoundedRectangle(width=main_chip.width + 0.5, height=main_chip.height + 0.36, corner_radius=0.12,
                                  stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
        main_chip.move_to(mframe)
        mchip = VGroup(mframe, main_chip)
        mchip.next_to(rec, RIGHT, buff=0.3).align_to(rec, UP).shift(DOWN * 0.45)

        fr3 = nb_frame()
        e303 = src(303).replace("dlops-io", GH_USER)
        e329 = src(329).replace("dlops-io", GH_USER).replace("dataset_v21", "dataset_v20")
        assert e303 != src(303) and e329.endswith("--rev dataset_v20") and GH_USER in e329
        mine = stack([nb_cell(13, [src_item(302), (e303, INK)], stroke=PASS),
                      nb_cell(15, [src_item(328), (e329, INK)], stroke=PASS)], fr3.content_top)
        edits = [p for r in [*mine[0].parts[1], *mine[1].parts[1]]
                 for k in (GH_USER, "dataset_v20") if k in r.text for p in [substring(r, k)]]
        gives = chip("your v20 gives 4", PASS, size=20).next_to(mine[1].box, DOWN, buff=0.2).align_to(mine[1].box, RIGHT)
        priv = card([label("private repo:", 22, INK), mono_line(PRIVATE_URL[0], 20, INK), mono_line("    " + PRIVATE_URL[1], 20, INK),
                     label("or make it public for this step", 22, S.GREY)], size=20, buff=0.12)
        lift = fr3.content_top - mine[1].box.get_top()[1]          # cell 15 moves up when cell 13 goes
        priv.next_to(gives, DOWN, buff=0.25).align_to(fr3.frame, LEFT).shift(RIGHT * 0.2 + UP * lift)
        pill = illustration_tag().align_to(mine[1].box, RIGHT).align_to(priv, UP)
        token = substring(priv.body[1], "<read-only token>")
        yt = your_turn().align_to(mine[1].box, RIGHT).align_to(priv, DOWN)
        assert pill.get_left()[0] > priv.get_right()[0] + 0.2 and yt.get_left()[0] > priv.get_right()[0] + 0.2

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(lt, *lt.lines, lxt)
            self.play(FadeOut(gone), run_time=0.4)
            self.remove(*gone.get_family())
            self.play(FadeIn(rec, shift=UP * 0.15), FadeIn(rtag), run_time=0.6)
            vo.wait_until("lists five files")
            self.play(each(list(s13[1]), INK, scale=1.04, lag=0.1), run_time=0.8)
            vo.wait_until("the same set as its version 21")
            self.play(FadeIn(mchip, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and counts 5")
            self.play(Indicate(s17[1], color=INK, scale_factor=1.12), Indicate(s15[1], color=INK, scale_factor=1.04),
                      run_time=0.7)
            vo.wait_until("Your account probably cannot access")
            self.play(Indicate(rtag, color=S.GREY, scale_factor=1.03), run_time=0.6)
            vo.wait_until("so use your repo")
            gone = VGroup(rec, rtag, mchip)
            self.play(FadeOut(gone, shift=UP * 0.2), run_time=0.4)
            self.remove(*gone.get_family())
            self.play(FadeIn(fr3), FadeIn(mine, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("replace the address and the tag")
            self.play(*[p.animate.set_color(PASS) for p in edits], run_time=0.6)
            self.play(each(edits, PASS, scale=1.1, lag=0.15), run_time=0.8)
            vo.wait_until("your version 20 gives 4")
            self.play(FadeIn(gives, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Your repo is private")
            self.play(FadeOut(mine[0]), VGroup(mine[1], gives).animate.shift(UP * lift), run_time=0.6)
            self.remove(*mine[0].get_family())
            self.play(FadeIn(priv, shift=UP * 0.15), FadeIn(pill), run_time=0.6)
            vo.wait_until("put an access token in the address")
            self.play(Indicate(token, color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("or make it public")
            self.play(Indicate(priv.body[3], color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Pause and work through it")
            self.play(FadeIn(yt, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, yt, TURN)
            self.wait(1.0)

        # ========================================================== 4. cell 19: quietly, dataset_v25
        fr4 = nb_frame(bottom=-0.85)
        c19c = stack([nb_cell(19, [src_item(361), src_item(362)])], fr4.content_top)[0]
        c20c = stack([nb_cell(20, [src_item(367), src_item(368)])], c19c.box.get_bottom()[1] - 0.2)[0]
        ct = colab_term(rows=4)

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(fr3, mine[1], gives, priv, pill, yt)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(*gone.get_family())
            self.play(FadeIn(fr4), FadeIn(c19c, shift=UP * 0.15), FadeIn(ct), run_time=0.6)
            vo.wait_until("Cell 19 asks quietly")
            self.play(Indicate(substring(c19c.parts[1][-1], "dataset_v25"), color=TURN, scale_factor=1.1),
                      Indicate(substring(next(r for r in c19c.parts[1] if "--quiet" in r.text), "--quiet"),
                               color=TURN, scale_factor=1.1), run_time=0.6)
            type_cmd(self, ct, c19.cmd, type_time=0.9)
            vo.wait_until("and prints nothing")
            bare_prompt(self, ct)
            self.play(Indicate(ct.lines[-1], color=INK, scale_factor=1.2), run_time=0.6)
        card4 = ponder(self, PONDER_Q, seconds=6)

        # ========================================================== 5. the answer; three tags; erratum
        lt5 = term(P_LAPTOP_HOME, rows=5, title=T_LAPTOP, size=20)
        lx5 = on_bar(lt5, extra_row())
        tg3 = TagRope()
        base3 = [tg3.line, tg3.beads[0], tg3.bead_labels[0], tg3.beads[1], tg3.beads[2], tg3.bead_labels[1], tg3.bead_labels[2], tg3.flags["dataset_v20"],
                 tg3.flags["dataset_v21"]]
        gh = tg3.ghost("dataset_v25")
        air = label("nothing to pull", 20, S.GREY).next_to(gh.rope, DOWN, buff=0.12)
        err = card([words(("cell 20's stored", S.GREY), (src(370), "mono", INK), ("(line 370)", S.GREY), size=26),
                    label("is left over from an older run", 26, INK),
                    words(("--quiet", "mono", TURN), "hides errors too", size=26)], size=26)
        err.move_to([0, 0.6, 0])
        etag = erratum_tag().next_to(err, UP, buff=0.15).align_to(err, RIGHT)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(card4), run_time=0.4)
            self.remove(card4)
            vo.wait_until("The next cell fails")
            self.play(FadeIn(c20c, shift=UP * 0.15), run_time=0.4)
            type_cmd(self, ct, c20.cmd, type_time=0.6)
            r20 = out(self, ct, [(s, ERR) for s in soft(c20.at((2, 4)), ct.max_chars)], run_time=0.5)
            vo.wait_until("no such folder")
            self.play(Indicate(next(r for r in r20 if "No such file" in r.text), color=ERR, scale_factor=1.05),
                      run_time=0.6)
            vo.wait_until("Without the quiet flag")
            xt5 = on_bar(ct, extra_row())
            self.play(FadeIn(xt5), run_time=0.3)
            type_cmd(self, ct, c19b.cmd, type_time=0.8)
            vo.wait_until("the error appears")
            r19 = out(self, ct, [(s, ERR) for s in soft(c19b.at(2), ct.max_chars)], run_time=0.5)
            vo.wait_until("unknown Git revision")
            whole = "unknown Git revision 'dataset_v25'"
            keys = (whole,) if any(whole in r.text for r in r19) else ("unknown Git", "revision 'dataset_v25'")
            hits = [substring(r, k) for r in r19 for k in keys if k in r.text]
            self.play(each(hits, ERR, scale=1.1, lag=0.2), run_time=0.8)
            vo.wait_until("The class repo only has tags")
            gone = VGroup(fr4, c19c, c20c, ct, *ct.lines, xt5)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(*gone.get_family())
            self.play(FadeIn(lt5), FadeIn(lx5), *[FadeIn(x) for x in base3], run_time=0.6)
            type_cmd(self, lt5, c118.cmd, type_time=0.6)
            r118 = out(self, lt5, c118.at(2, 4, 6), run_time=0.5)
            self.play(*[substring(r, f"dataset_v{v}").animate.set_color(TURN) for r, v in zip(r118, (20, 21, 30))],
                      run_time=0.6)
            self.play(FadeIn(gh.flag, shift=DOWN * 0.15), run_time=0.5)
            self.play(Create(gh.rope), FadeIn(air, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("v20, v21 and v30")
            self.play(each([substring(r, f"dataset_v{v}") for r, v in zip(r118, (20, 21, 30))], TURN, scale=1.12,
                           lag=0.25), run_time=0.9)
            self.play(Indicate(gh.flag.text, color=S.GREY, scale_factor=1.12), run_time=0.6)
            vo.wait_until("The stored count of 3")
            gone = VGroup(*base3, gh, air)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(*gone.get_family())
            self.play(FadeIn(err, shift=UP * 0.15), FadeIn(etag), run_time=0.6)
            vo.wait_until("is left over from an older run")
            self.play(Indicate(err.body[0][1], color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("the quiet flag hides errors too")
            self.play(Indicate(err.body[2], color=TURN, scale_factor=1.06), run_time=0.7)

        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
