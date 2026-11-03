"""S13 · A pointer in git, the bytes in a bucket — tracker J4 → J6; `lref("22–23, 25, 33")` the whole scene.

Beats (script.md, ## S13; one voiceover block each):
0. TRACKER J4. S12's container session (root@1d462befbcdd:/app#) continues: `dvc push` → 95: 72–74
   (72 squashed), 74 RED, ▶ your turn. Tag `extra · local remote` (title bar + tracker suffix):
   `dvc remote add --local standin …` (no output; the prompt returns), `dvc push -r standin` →
   95: 79–81, `5 files pushed` YELLOW; chip "4 photos + 1 manifest · any remote prints this summary".
1. The terminal shrinks to a 3-row strip. `.dvc/cache` (GREY) and `dvc_store/` (BLUE, `illustration`)
   side by side, both listing files/md5/ 5b/ ba/ 91/ 5b/ 89/…dir (95:65–69); each slip copies across
   under a PURPLE `dvc push`. GOLD cost tag. Then V6's three homes, one per anchor; GREY chip
   "slide 33: no local copy · DVC keeps one" under the cache; on "never overwrites" S08's YELLOW
   parked card flies in and gets a GREEN check.
2. TRACKER J5. README card (data-versioning README line 312); `exit` (95: 82–83) and the host prompt.
   The terminal grows: `git status` → 96: 2–18 (5–7 GREEN, 12 YELLOW, 13–14 + row tag "our two
   edits", 18 YELLOW); `git add .` (no output); `git commit -m …` → 98: 2–7 + chip "6 small text
   files · no photos"; CODE(starter .gitignore: 3) `/cheese_dataset` GREEN + GREY chip
   ".dvc/cache: ignored by .dvc/.gitignore". No ▶ here.
3. TRACKER J5. 3-row strip under V6's git line (two beads). `git tag -a …` (no output; the flag
   plants on "a permanent name"); `git push --atomic origin main dataset_v20` typed, no output panel;
   GREY card (branch and tag together, or neither · Tags on GitHub); ▶. TRACKER J5 · extra:
   `git log --oneline --decorate` → 101: 2–3, `tag: dataset_v20` GREEN, chip "our hashes · yours
   differ"; the strip grows: `git show dataset_v20:cheese_dataset.dvc` → 102: 2–7.
4. TRACKER J5 · extra. The second terminal strip (20 pt): the `diff … && echo identical` (121: 2,
   GREEN). The class repo's card (120: 2–7) and ours merge; S01's PINK line lands on ours. The strip
   closes. V6: dvc_store/ with the .dir and four blobs; the PINK rope from the card's md5 to the .dir,
   fanning out; GREY line (slide 25): "git keeps the fingerprint of the list of fingerprints".
5. Erratum: README card line 321 ("this tag is taken") + chip "only in a fork · after rm -rf .git and
   git init, no tags exist". The README's table (256–260). TRACKER J6: GREY note "Colab: view
   dataset_v20 → scene 15 views both versions" (README 324–328). Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S13"]
DV = "data-versioning"
STARTER = "data-versioning@data-versioning-ac215"
PUSH_CHIP = "4 photos + 1 manifest · any remote prints this summary"
COST_NOTE = "a second copy of the photos now bills · a fraction of a cent a month"
SLIDE33 = "slide 33: no local copy · DVC keeps one"
PARKED_Q = "how do you freeze which photos a model saw?"          # S08's parked card, verbatim
ATOMIC = ("on your machine:", "branch and tag arrive together, or neither",
          "the tag appears under Tags on GitHub")
FORK = "only in a fork · after rm -rf .git and git init, no tags exist"
TRICK = "slide 25, one level deeper: git keeps the fingerprint of the list of fingerprints"
COLAB_NOTE = "Colab: view dataset_v20 → scene 15 views both versions"
PUSHED = [IMAGES[0], IMAGES[1], IMAGES[2], IMAGES[3]]            # the order of the script's SHOW line


def s13_words(*parts, size: float = 20, color=INK) -> VGroup:
    """One row of label/mono pieces: plain strings label font; ('x', 'mono') mono; ('x', colour) label in colour."""
    ms = []
    for p in parts:
        if isinstance(p, tuple):
            ms.append(mono(p[0], size, color) if p[1] == "mono" else label(p[0], size, p[1]))
        else:
            ms.append(label(p, size, color))
    return VGroup(*ms).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)


def shelf_box(title: str, colour, box_w: float = 4.6) -> VGroup:
    """A drawn store (the cache or dvc_store/): title, 'files/md5/', five rows 'aa/ [md5…]' in the
    order of the script's SHOW line (5b ba 91 5b 89….dir). .frame .title .sub .rows .slips"""
    tt = mono(title, 22, colour)
    sub = mono("files/md5/", 20, S.GREY)
    rows, slips = VGroup(), VGroup()
    for h in [MD5[n] for n in PUSHED] + [V20["md5"]]:
        a = mono(aisle(h), 20, HASH)
        s = slip(short(h))
        rows.add(VGroup(a, s).arrange(RIGHT, buff=0.2))
        slips.add(s)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    body = VGroup(tt, sub, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    rows.shift(RIGHT * 0.35)
    fr = RoundedRectangle(width=box_w, height=body.height + 0.34, corner_radius=0.16, stroke_color=colour,
                          stroke_width=3).set_fill(colour, 0.07)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, body)
    g.frame, g.title, g.sub, g.rows, g.slips = fr, tt, sub, rows, slips
    return g


def readme_table(size: float = 20) -> VGroup:
    """README.md 256–260 (data-versioning): the Tool / What it tracks table, its own words."""
    rows = (("Tool", "What it tracks", S.GREY), ("Git", "Code and small DVC metadata files", TOOL),
            ("DVC", "Large dataset files", TOOL), ("GCS", "The remote location where DVC stores dataset versions", CLOUD))
    for (a, b, _), n in zip(rows, (256, 258, 259, 260)):
        assert readme(n, DV) == f"| {a} | {b} |", readme(n, DV)
    left = [label(a, size + 2, c) for a, _, c in rows]
    right = [label(b, size + 2, INK if i else S.GREY) for i, (_, b, _) in enumerate(rows)]
    lw = max(m.width for m in left)
    grid = VGroup()
    for i, (l_, r_) in enumerate(zip(left, right)):
        yy = -i * 0.58
        l_.move_to([0, yy, 0], aligned_edge=LEFT)
        r_.move_to([lw + 0.6, yy, 0], aligned_edge=LEFT)
        grid.add(VGroup(l_, r_))
    rule = Line(grid[0].get_corner(DL) + DOWN * 0.11, grid[0].get_corner(DL) + DOWN * 0.11 + RIGHT * grid.width,
                color=S.GREY, stroke_width=2)
    g = VGroup(grid, rule)
    g.rows = list(grid)
    return g


class PointerAndBytes(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S13"] == 6, len(SAY)
        c95, c96, c98 = capture("95"), capture("96"), capture("98")
        c97, c99, c101, c102, c121 = capture("97"), capture("99"), capture("101"), capture("102"), capture("121")
        assert c95.istep(71)[1] == "dvc push" == readme(303, DV)
        for c, n in ((c96, 315), (c97, 316), (c98, 317), (c99, 318)):
            assert c.cmd == readme(n, DV), (c.cmd, readme(n, DV))
        push_cmd = readme(319, DV)                                     # typed, no output panel (100 is the sandbox's)
        assert push_cmd == "git push --atomic origin main dataset_v20"

        # ========================================================== 0. J4: dvc push, then the local remote
        ref = lref("22–23, 25, 33")
        tr = tracker("J", 4)
        t = term(c95.istep(71)[0], rows=9, size=20)
        pchip = grey_chip(PUSH_CHIP).next_to(t.box, UP, buff=0.15).align_to(t.box, RIGHT)
        y, r = TURN, ERR

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(t), run_time=0.6)
            ln = istep(self, t, c95.line(71), type_time=0.4)
            vo.wait_until("Pause and run it")
            yt = beside(turn_row(), ln)
            pin(self, ln, yt)
            flash_tag(self, yt, TURN)
            vo.wait_until("Here it fails")
            r74 = out(self, t, [squash(c95.line(72)), c95.line(73), (c95.line(74), r)], run_time=0.6)
            self.play(Indicate(r74[-1], color=ERR, scale_factor=1.03), run_time=0.6)
            vo.wait_until("To show what a push uploads")
            lt = on_bar(t, local_row())
            self.play(FadeIn(lt, shift=LEFT * 0.1), track(tr, 4, extra="local remote"), run_time=0.5)
            istep(self, t, c95.line(77), type_time=1.0)
            bare_prompt(self, t)
            vo.wait_until("an extra push goes")
            istep(self, t, c95.line(78), type_time=0.5)
            vo.wait_until("5 files pushed")
            r81 = out(self, t, [squash(c95.line(79)), c95.line(80), (c95.line(81), y)], run_time=0.6)
            self.play(Indicate(r81[-1], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("the four photos and the manifest")
            self.play(FadeIn(pchip, shift=DOWN * 0.1), run_time=0.5)
            flash_tag(self, pchip, INK)

        # ========================================================== 1. the cache's mirror, the three homes
        cache = shelf_box(".dvc/cache", LAPTOP).move_to([-3.9, 0.0, 0]).align_to(np.array([0, 2.75, 0]), UP)
        store = shelf_box("dvc_store/", CLOUD).move_to([3.9, 0.0, 0]).align_to(np.array([0, 2.75, 0]), UP)
        ill = illustration_tag()
        ill.move_to([store.frame.get_right()[0] - 0.2 - ill.width / 2, store.title.get_center()[1], 0])
        dvc_chip = tool_chip("dvc push").move_to([0, 1.6, 0])
        dvc_arrow = arrow(np.array([-1.3, 1.05, 0]), np.array([1.3, 1.05, 0]), TOOL, stroke=4)
        bill = cost_tag(COST_NOTE).move_to([0, (cache.get_bottom()[1] - 1.62) / 2, 0])
        tg = TagRope()
        hm = tg.homes().move_to([0, 0.3, 0])
        s33 = grey_chip(SLIDE33).next_to(hm.cache, DOWN, buff=0.18)
        pk = card([label(PARKED_Q, 24, TURN)], TURN).move_to([0, 2.02, 0])
        tick = check_mark(0.45, PASS, 7).next_to(pk, RIGHT, buff=0.3)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(pchip, lt)), track(tr, 4), run_time=0.4)
            self.remove(pchip, lt)
            unpin(self, ln, yt)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(cache, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("the DVC store now mirrors the cache")
            self.play(FadeIn(store.frame), FadeIn(store.title), FadeIn(store.sub), FadeIn(ill),
                      GrowArrow(dvc_arrow), FadeIn(dvc_chip), run_time=0.6)
            self.play(LaggedStart(*[TransformFromCopy(a, b) for a, b in zip(cache.rows, store.rows)],
                                  lag_ratio=0.25), run_time=1.6)
            vo.wait_until("A gold tag")
            self.play(FadeIn(bill, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, bill, COST)
            vo.wait_until("So the bytes now sit in three places")
            mirror = VGroup(cache, store, ill, dvc_chip, dvc_arrow, bill)
            self.play(FadeOut(mirror), run_time=0.5)
            self.remove(*mirror.get_family())
            self.play(LaggedStart(*[Create(h.frame) for h in hm], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("the images folder you upload to")
            self.play(FadeIn(hm.images[1], shift=UP * 0.2), run_time=0.6)
            vo.wait_until("and the cache on your disk")
            self.play(FadeIn(hm.cache[1], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(s33, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("The third is the DVC store")
            self.play(FadeIn(hm.store[1], shift=UP * 0.2), run_time=0.6)
            vo.wait_until("named by its fingerprint")
            self.play(Indicate(hm.store.title, color=CLOUD, scale_factor=1.1), run_time=0.6)
            vo.wait_until("The images folder can change")
            self.play(Indicate(hm.images[1][2], color=INK, scale_factor=1.15), run_time=0.7)
            vo.wait_until("the DVC store never overwrites")
            self.play(Indicate(hm.store[1][2], color=INK, scale_factor=1.15),
                      FadeIn(pk, shift=DOWN * 0.4, scale=0.9), run_time=0.8)
            self.play(Create(tick), run_time=0.5)
            vo.wait_until("because new bytes get a new name")
            self.play(Indicate(pk.body, color=TURN, scale_factor=1.03), run_time=0.7)

        # ========================================================== 2. J5: outside the container, git
        c312 = readme_card(312, VGroup(
            s13_words("Run these commands", ("outside the container,", TURN), size=24),
            s13_words("from your local", (DV, "mono"), "folder:", size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18),
            size=20, repo=DV).move_to([0, 0.6, 0])
        assert "outside the container" in readme(312, DV)
        gi = code(f"{STARTER}/.gitignore", 3, 3)
        gi_chip = grey_chip(".dvc/cache: ignored by .dvc/.gitignore")
        c_chip = grey_chip("6 small text files · no photos")
        g = PASS

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(hm, s33, pk, tick)), track(tr, 5), run_time=0.6)
            self.remove(hm, s33, pk, tick)
            self.play(FadeIn(c312, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(c312.body[0][1], color=TURN, scale_factor=1.06), run_time=0.6)
            istep(self, t, c95.line(82), type_time=0.3)
            out(self, t, c95.at(83), run_time=0.3)
            cd_prompt(self, t, P_VERSIONING)
            vo.wait_until("Here, git status shows")
            self.play(FadeOut(c312), run_time=0.4)
            self.remove(c312)
            resize(self, t, 12, run_time=0.6)
            type_cmd(self, t, c96.cmd, type_time=0.3)
            r1 = out(self, t, [c96.line(2), c96.line(3), c96.line(4), (c96.line(5), g), (c96.line(6), g),
                               (c96.line(7), g), c96.line(8)], run_time=0.6)
            vo.wait_until("that dvc init already staged")
            self.play(each(list(r1[3:6]), PASS, scale=1.04), run_time=0.8)
            r2 = out(self, t, [c96.line(n) for n in range(9, 12)] + [(c96.line(12), y)]
                     + [c96.line(n) for n in range(13, 18)] + [(c96.line(18), y)], run_time=0.7)
            vo.wait_until("the new pointer file")
            self.play(Indicate(r2[-1], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and your two edits")
            ed = beside(row_tag("our two edits"), r2[5], buff=0.6)
            pin(self, r2[5], ed)
            self.play(each([r2[4], r2[5]], INK, scale=1.04), run_time=0.6)
            vo.wait_until("Add and commit")
            unpin(self, r2[5], ed)
            resize(self, t, 8, keep=2, run_time=0.5)
            type_cmd(self, t, c97.cmd, type_time=0.2)
            bare_prompt(self, t)
            ln98 = type_cmd(self, t, c98.cmd, type_time=0.6, soft=True)
            r98 = out(self, t, c98.at((2, 7)), run_time=0.5)
            vo.wait_until("6 small text files")
            c_chip.next_to(t.box, UP, buff=0.15).align_to(t.box, RIGHT)
            self.play(FadeIn(c_chip, shift=DOWN * 0.1), Indicate(r98[1], color=INK, scale_factor=1.03),
                      run_time=0.6)
            vo.wait_until("because the git ignore file")
            gi.move_to([-2.6, (PIC_TOP + t.box.get_top()[1] + 0.12) / 2 + 0.25, 0])
            gi_chip.next_to(gi, RIGHT, buff=0.4)
            self.play(FadeIn(gi, shift=DOWN * 0.15), run_time=0.5)
            self.play(code_span(gi.code, 0, "/cheese_dataset").animate.set_color(PASS), run_time=0.5)
            vo.wait_until("excludes the dataset folder")
            self.play(Indicate(code_span(gi.code, 0, "/cheese_dataset"), color=PASS, scale_factor=1.12),
                      FadeIn(gi_chip, shift=LEFT * 0.1), run_time=0.7)

        # ========================================================== 3. J5: tag, push; extra log + show
        for i in (0, 1):
            tg.beads[i].set_z_index(1)
        base = VGroup(tg.line, tg.beads[0], tg.bead_labels[0])
        fl = tg.flags["dataset_v20"]
        atom = card([label(ATOMIC[0], 20, S.GREY), label(ATOMIC[1], 20, INK), label(ATOMIC[2], 20, INK)],
                    size=20).move_to([3.3, 1.35, 0])

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(gi, gi_chip, c_chip)
            self.play(FadeOut(gone), run_time=0.4)
            self.remove(*gone.get_family())
            resize(self, t, 3, run_time=0.5)
            self.play(Create(tg.line), FadeIn(tg.beads[0], scale=0.5), FadeIn(tg.bead_labels[0]), run_time=0.6)
            self.play(tg.bead(1), run_time=0.5)
            ln99 = type_cmd(self, t, c99.cmd, type_time=0.6, soft=True)
            vo.wait_until("a permanent name")
            bare_prompt(self, t)
            self.play(tg.plant("dataset_v20"), run_time=0.7)
            self.play(Indicate(fl.text, color=POINTER, scale_factor=1.12), run_time=0.5)
            vo.wait_until("and push the branch and the tag together")
            lnp = type_cmd(self, t, push_cmd, type_time=0.6)
            vo.wait_until("atomic means both arrive")
            self.play(FadeIn(atom, shift=LEFT * 0.2), run_time=0.5)
            self.play(Indicate(atom.body[1], color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("Pause and run them")
            yt3 = beside(turn_row(), lnp)
            pin(self, lnp, yt3)
            flash_tag(self, yt3, TURN)
            vo.wait_until("An extra log shows the tag")
            unpin(self, lnp, yt3)
            self.play(FadeOut(atom), track(tr, 5, extra=True), run_time=0.4)
            self.remove(atom)
            type_cmd(self, t, c101.cmd, type_time=0.4)
            r101 = out(self, t, c101.at((2, 3)), wrap=True, run_time=0.4)
            self.play(substring(r101[0], "tag: dataset_v20").animate.set_color(PASS), run_time=0.4)
            dch = differ_chip("our hashes · yours differ").next_to(t.box, UP, buff=0.15).align_to(t.box, RIGHT)
            self.play(FadeIn(dch, shift=DOWN * 0.1), Indicate(fl.text, color=POINTER, scale_factor=1.1),
                      run_time=0.5)
            vo.wait_until("which pins these six lines")
            self.play(FadeOut(dch), run_time=0.3)
            self.remove(dch)
            resize(self, t, 8, keep=0, run_time=0.5)
            type_cmd(self, t, c102.cmd, type_time=0.4)
            r102 = out(self, t, c102.at((2, 7)), run_time=0.6)
            self.play(Indicate(r102[1], color=HASH, scale_factor=1.04), run_time=0.6)

        # ========================================================== 4. extra: the class tag's card is ours
        t2 = term(P_LAPTOP_HOME, rows=3, title=T_SECOND, size=20)
        ours = tg.card                                     # at its home under the v20 bead
        theirs = pointer_card(short(V20["md5"]), V20["size"], V20["nfiles"])
        assert c121.cmd and capture("120").at((2, 7)) == c95.at((58, 63)) == c102.at((2, 7))
        theirs.move_to(ours).set_x(2.6)
        lab_t = dashed_chip("class repo · dataset_v20").next_to(theirs, UP, buff=0.15)
        hook = mono(HOOK_LINE, 20, HASH).move_to([2.6, 0.0, 0])
        md5_row = ours.lines[1]
        x2 = on_bar(t2, extra_row())
        rope = None
        trick = note(TRICK, S.GREY, 22).move_to([0, -2.2, 0])

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(t, *t.lines)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(*gone.get_family())
            self.play(FadeIn(t2), FadeIn(x2), FadeIn(ours, shift=DOWN * 0.3), FadeIn(theirs, shift=DOWN * 0.3),
                      FadeIn(lab_t), run_time=0.7)
            type_cmd(self, t2, c121.cmd, type_time=1.4)
            vo.wait_until("identical")
            r121 = out(self, t2, [(c121.line(2), PASS)], run_time=0.4)
            self.play(Indicate(r121[0], color=PASS, scale_factor=1.15), run_time=0.5)
            vo.wait_until("same bytes, same fingerprint")
            self.play(FadeOut(lab_t), theirs.animate.move_to(ours), run_time=0.8)
            self.play(FadeOut(theirs), run_time=0.3)
            self.remove(theirs)
            self.play(FadeIn(hook, shift=DOWN * 0.3), run_time=0.4)
            land = np.array([ours.get_right()[0] + 0.35 + hook.width / 2, ours.fields["md5"].get_center()[1], 0])
            self.play(hook.animate.move_to(land), run_time=0.6)
            self.play(FadeOut(hook, target_position=ours.fields["md5"].get_center(), scale=0.6),
                      Indicate(ours.fields["md5"], color=HASH, scale_factor=1.15), run_time=0.7)
            vo.wait_until("on any machine")
            gone = VGroup(t2, x2, *t2.lines)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(*gone.get_family())
            vo.wait_until("That is the whole trick")
            d20 = tg.dirs["v20"]
            blobs = [tg.blobs[n] for n in IMAGES[:4]]
            self.play(FadeIn(tg.store), FadeIn(d20), LaggedStart(*[FadeIn(b) for b in blobs], lag_ratio=0.15),
                      run_time=0.8)
            vo.wait_until("git keeps the fingerprint")
            self.play(FadeIn(trick, shift=UP * 0.1), Indicate(ours.fields["md5"], color=HASH, scale_factor=1.12),
                      run_time=0.7)
            self.play(Indicate(d20.text, color=HASH, scale_factor=1.15), run_time=0.6)
            vo.wait_until("A rope leads from the tag")
            rope = tg.rope("v20")
            self.play(Indicate(fl.text, color=POINTER, scale_factor=1.12), run_time=0.5)
            self.play(Create(rope.main), run_time=0.9)
            vo.wait_until("to the bytes in your bucket")
            self.play(LaggedStart(*[Create(f) for f in rope.fans], lag_ratio=0.2), run_time=0.8)
            self.play(each(blobs, HASH, scale=1.1), run_time=0.8)

        # ========================================================== 5. erratum, the README's table, J6
        quote = VGroup(label("The name-tag of the dataset might not be 'dataset_v20' for you", 24, INK),
                       s13_words("as", ("this tag is taken.", TURN), size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        assert "this tag is taken" in readme(321, DV)
        c321 = readme_card(321, quote, quote=True, size=24, repo=DV).move_to([0, 0.3, 0])
        err = erratum_tag().next_to(c321, UP, buff=0.15).align_to(c321, RIGHT)
        fork = grey_chip(FORK).next_to(c321, DOWN, buff=0.3)
        tbl = readme_table(24)
        ctbl = readme_card((256, 260), tbl, size=24, repo=DV).move_to([0, 0.5, 0])
        cn = note(COLAB_NOTE, S.GREY, 26)
        cn_head = label("README.md · lines 324–328", 20, S.GREY)
        colab_n = VGroup(cn_head, cn).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0, -2.2, 0])

        with self.voiceover(SAY[5]) as vo:
            v6 = VGroup(tg.line, tg.beads[0], tg.beads[1], tg.bead_labels[0], tg.bead_labels[1], fl, ours,
                        tg.store, tg.dirs["v20"], *[tg.blobs[n] for n in IMAGES[:4]], rope, trick)
            self.play(FadeOut(v6), track(tr, 5), run_time=0.6)
            self.remove(*v6.get_family())
            self.play(FadeIn(c321, shift=DOWN * 0.15), FadeIn(err), run_time=0.6)
            self.play(Indicate(quote[1][1], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("that applies only to a fork")
            self.play(FadeIn(fork, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and your fresh repo has no tags")
            self.play(Indicate(fork.text, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Its table sums it up")
            gone = VGroup(c321, err, fork)
            self.play(FadeOut(gone, shift=UP * 0.2), run_time=0.5)
            self.remove(*gone.get_family())
            self.play(FadeIn(ctbl, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("git holds code")
            self.play(Indicate(tbl.rows[1], color=TOOL, scale_factor=1.04), run_time=0.6)
            vo.wait_until("DVC tracks the dataset")
            self.play(Indicate(tbl.rows[2], color=TOOL, scale_factor=1.04), run_time=0.6)
            vo.wait_until("the bucket stores the versions")
            self.play(Indicate(tbl.rows[3], color=CLOUD, scale_factor=1.04), run_time=0.6)
            self.play(track(tr, 6), FadeIn(colab_n, shift=UP * 0.15), run_time=0.6)

        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
