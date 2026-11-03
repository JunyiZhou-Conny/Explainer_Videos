"""S14 · One more photo: what moves? — tracker K1 → K4; `lref("20")` the whole scene.

Beats (script.md, ## S14; one voiceover block each):
0. TRACKER K1 appears. Console `illustration` (README.md 336–341): a schematic window on
   your-bucket-placeholder/images/ with four blank tiles; a fifth flies in; ▶ your turn beside it.
   A 3-row strip (20 pt) under it, tag `extra · stand-in` on its bar: the `sudo cp … && ls -la` copy
   (folds) → 103: 5–9, line 9 `Image_5.jpg` YELLOW. GREY chip "gcsfuse caches listings · wait a
   little · ls first".
1. V5's shelf: four filled aisles (5b ba 91, 5b twice) and the 89/ manifest; Image_5 waits outside.
   PONDER (8 s).
2. TRACKER K2. Answer chip; V5 fades, the terminal grows: `sh docker-shell.sh` (re-entry 104: 27–28,
   …, 41–42) + chip "same entrypoint errors as before"; `ls cheese_dataset` (extra) → 46;
   `dvc add cheese_dataset` → 48 (edge-wrapped), 50, 52; ▶; `cat cheese_dataset.dvc` (extra) →
   58–63, 59–61 YELLOW; GREY chip "the class v21: 3280f8f9….dir · a different fifth photo" (120:10).
   The terminal shrinks, V5 returns: Image_5 → 54081d12… on 54/, the manifest 6b342844….dir on 6b/.
3. TRACKER K3. `dvc push` → 65–67 (65 squashed), 67 RED, ▶; `extra · local remote`:
   `dvc push -r standin` → 71–73, `2 files pushed` YELLOW. V5: the four old photo slips light
   "already on the shelf"; chip "2 pushed, not 6".
4. TRACKER K4. `exit` (104: 74–75), host prompt. V6 as S13 left it (two beads, dataset_v20, the v20
   manifest and four blobs). git status → 105: 2–6 (6 YELLOW); git add . (no output); git commit →
   107: 2–3 (third bead); git tag … (no output; flag dataset_v21 plants); git push --atomic … typed,
   no output panel; ▶; the v21 rope fans to five blobs, four shared. Extras (terminal grows, V6 out):
   git diff → 110: 7–15, 8–13 YELLOW; git log → 111: 2–4 (`tag: dataset_v21` GREEN, "our hashes ·
   yours differ"); git tag -n → 112: 2–3.
5. TRACKER K4 · extra. RED kind card: starter README line 148 (+ erratum tag); the strip types the
   remote add (extra; folds) → 113: 2 RED; README card line 372 "Do not add it again here."
6. TRACKER K4 · extra · stand-in. V6 back; `git checkout dataset_v20 -- …` → 114: 2, cursor on
   dataset_v20; re-entry 115; `dvc checkout` → 49; `ls` → 51 (four GREEN); `exit`; `git checkout
   main -- …` (no output), cursor on dataset_v21; re-entry 117; `dvc checkout` → 49; `ls` → 51 (five
   GREEN). A GREY `.dvc/cache` box feeds the folder (not dvc_store/). On "With a real mount", V6 goes
   and a GREY card says what a real mount does. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S14"]
DV = "data-versioning"
STARTER = "data-versioning@data-versioning-ac215"
PONDER_Q = "Four photos already in dvc_store.\nYou add one. How many objects\nwill dvc push upload?"
FUSE_NOTE = "gcsfuse caches listings · wait a little · ls first"
ANSWER = "two: the new photo + a new manifest"
CLASS_NOTE = f"the class v21: {short(CLASS_V21['md5'])} · a different fifth photo"
SHELF_NOTE = "already on the shelf"
COUNT_NOTE = "2 pushed, not 6"
REAL_MOUNT = ("real mount: dvc checkout writes to images/ in your bucket",
              "v20 deletes Image_5.jpg there · main writes it back")


def edge(s: str, n: int) -> list[str]:
    """A progress-bar line soft-wrapped at the row edge, as a real terminal shows it (text unchanged)."""
    return [s[i:i + n] for i in range(0, len(s), n)]


def band_mid(t) -> float:
    return (PIC_TOP + t.box.get_top()[1] + 0.12) / 2


def console(t) -> VGroup:
    """The schematic console on images/ (README 336–341): four blank tiles in a row, a slot for the
    fifth. .win .tiles .slot"""
    win = window(f"{BUCKET}/images/", 11.8, 2.2)
    win.move_to([0, band_mid(t) + 0.35, 0])
    row = VGroup(*[tile(n, 0.62, CLOUD) for n in IMAGES]).arrange(RIGHT, buff=0.32)
    row.move_to(win.content)
    tiles, slot = VGroup(*row[:4]), row[4]
    g = VGroup(win, tiles)
    g.win, g.tiles, g.slot = win, tiles, slot
    return g


class SecondVersion(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S14"] == 7, len(SAY)
        c103, c104, c105, c106, c107 = capture("103"), capture("104"), capture("105"), capture("106"), capture("107")
        c108, c110, c111, c112, c113 = capture("108"), capture("110"), capture("111"), capture("112"), capture("113")
        c114, c115, c116, c117 = capture("114"), capture("115"), capture("116"), capture("117")
        assert c104.istep(47)[1] == readme(351, DV) and c104.istep(64)[1] == readme(357, DV)
        for c, n in ((c105, 365), (c106, 366), (c107, 367), (c108, 368)):
            assert c.cmd == readme(n, DV), (c.cmd, readme(n, DV))
        push_cmd = readme(369, DV)                                 # typed, no output panel (109 is the sandbox's)
        assert push_cmd == "git push --atomic origin main dataset_v21"
        assert c113.cmd in readme(148, STARTER)
        assert "Do not add it again here." in readme(372, DV)
        y, r, g = TURN, ERR, PASS

        # ========================================================== 0. K1: one more photo into images/
        ref = lref("20")
        tr = tracker("K", 1)
        t = term(P_VERSIONING, rows=3, size=20)
        con = console(t)
        ill = illustration_tag().next_to(con.win, UP, buff=0.12).align_to(con.win, RIGHT)
        five = con.slot.copy()
        yt0 = your_turn().next_to(con.win, DOWN, buff=0.15).align_to(con.win, RIGHT)
        fuse = grey_chip(FUSE_NOTE)
        sb0 = on_bar(t, standin_row())

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.6)
            vo.wait_until("Upload a few more photos")
            self.play(FadeIn(con.win), FadeIn(ill), LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in con.tiles],
                                                                 lag_ratio=0.15), run_time=0.9)
            self.play(FadeIn(five, shift=UP * 0.9, scale=0.8), run_time=1.0)
            self.play(Indicate(five.text, color=CLOUD, scale_factor=1.12), run_time=0.5)
            vo.wait_until("our stand-in copies in one")
            self.play(FadeIn(t), FadeIn(sb0, shift=LEFT * 0.1), track(tr, 1, extra="stand-in"), run_time=0.5)
            type_cmd(self, t, c103.cmd, type_time=1.0)
            rows103 = out(self, t, c103.at((5, 8)) + [(c103.line(9), y)], run_time=0.6)
            self.play(Indicate(rows103[-1], color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("With a real bucket")
            fuse.next_to(con.win, DOWN, buff=0.15).align_to(con.win, LEFT)
            self.play(FadeIn(fuse, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("so list before you add")
            self.play(Indicate(fuse.text, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Pause and upload")
            self.play(FadeIn(yt0, shift=LEFT * 0.15), FadeOut(sb0), track(tr, 1), run_time=0.5)
            self.remove(sb0)
            flash_tag(self, yt0, TURN)

        # ========================================================== 1. the shelf as it stands; ponder
        hs = HashShelf()
        hs.remove(*[hs.tiles[n] for n in IMAGES[:4]])
        filed = []
        for h in [MD5[n] for n in IMAGES[:4]] + [V20["md5"]]:
            a = h[:2]
            s = slip(h[2:8] + "…" + (".dir" if h.endswith(".dir") else ""))
            s.move_to(hs._slot(a, s))
            hs.slips[a].append(s)
            filed.append(s)
        photo_slips, man20 = filed[:4], filed[4]
        aisles = [hs.rows[a] for a in dict.fromkeys(h[:2] for h in [MD5[n] for n in IMAGES[:4]] + [V20["md5"]])]
        t5 = hs.tiles[IMAGES[4]]

        with self.voiceover(SAY[1]) as vo:
            pic = VGroup(con.win, con.tiles, five, ill, fuse, yt0)
            self.play(FadeOut(pic), run_time=0.5)
            self.remove(*pic.get_family())
            self.play(FadeIn(hs.rack), FadeIn(VGroup(*aisles)), FadeIn(hs.machine), run_time=0.6)
            vo.wait_until("Four photos are already")
            self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.15) for s in photo_slips], lag_ratio=0.2), run_time=1.0)
            self.play(FadeIn(man20, shift=RIGHT * 0.15), run_time=0.4)
            vo.wait_until("and you add one")
            self.play(FadeIn(t5, shift=RIGHT * 0.3), run_time=0.5)
            self.play(Indicate(t5.frame, color=INK, scale_factor=1.1), run_time=0.5)
        pcard = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 2. K2: re-enter, ls, dvc add, cat
        ans = grey_chip(ANSWER).move_to([-3.6, -0.65, 0])
        rchip = reentry_chip()
        cls = grey_chip(CLASS_NOTE)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(pcard), run_time=0.4)
            self.remove(pcard)
            self.play(FadeIn(ans, shift=UP * 0.1), Indicate(t5.frame, color=INK, scale_factor=1.1), run_time=0.6)
            self.play(Indicate(hs.machine.frame, color=TOOL, scale_factor=1.05), run_time=0.5)
            vo.wait_until("Start the container again")
            shelf = VGroup(hs.rack, *aisles, hs.machine, *filed, t5, ans)
            self.play(FadeOut(shelf), track(tr, 2), run_time=0.5)
            self.remove(*shelf.get_family())
            resize(self, t, 11, run_time=0.5)
            reenter(self, t, "104", type_time=0.3)
            rchip.next_to(t.box, UP, buff=0.15).align_to(t.box, RIGHT)
            self.play(FadeIn(rchip, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("list the folder")
            xb = on_bar(t, extra_row())
            self.play(FadeIn(xb, shift=LEFT * 0.1), track(tr, 2, extra=True), run_time=0.3)
            istep(self, t, c104.line(45), type_time=0.2)
            out(self, t, c104.at(46), run_time=0.3)
            vo.wait_until("and add it")
            self.play(FadeOut(xb), track(tr, 2), run_time=0.3)
            self.remove(xb)
            ln_add = istep(self, t, c104.line(47), type_time=0.3)
            out(self, t, [*edge(c104.line(48), t.max_chars), c104.line(50), c104.line(52)], run_time=0.5)
            vo.wait_until("pause and run them")
            yt2 = beside(turn_row(), ln_add)
            pin(self, ln_add, yt2)
            flash_tag(self, yt2, TURN)
            vo.wait_until("It gives 5 files")
            unpin(self, ln_add, yt2)
            self.play(FadeIn(xb, shift=LEFT * 0.1), track(tr, 2, extra=True), run_time=0.3)
            istep(self, t, c104.line(57), type_time=0.2)
            rows_cat = out(self, t, [c104.line(58)] + [(x, y) for x in c104.at((59, 61))] + c104.at((62, 63)),
                           run_time=0.5)
            self.play(Indicate(rows_cat[3], color=TURN, scale_factor=1.08), run_time=0.5)
            vo.wait_until("a new manifest fingerprint")
            self.play(Indicate(rows_cat[1], color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("The class version 21")
            cls.next_to(t.box, UP, buff=0.15).align_to(t.box, RIGHT)
            self.play(FadeOut(rchip), FadeIn(cls, shift=DOWN * 0.1), run_time=0.5)
            self.remove(rchip)
            vo.wait_until("because its fifth photo")
            self.play(Indicate(cls.text, color=INK, scale_factor=1.04), run_time=0.6)
            # back to the shelf: the fifth photo and the new manifest are filed
            self.play(FadeOut(VGroup(cls, xb)), track(tr, 2), run_time=0.4)
            self.remove(cls, xb)
            resize(self, t, 3, run_time=0.5)
            back = VGroup(hs.rack, *aisles, hs.machine, *filed, t5)
            self.play(FadeIn(back), run_time=0.5)
            new_photo = hs.hash_photo(self, IMAGES[4])
            man21 = hs._file(self, V21["md5"][:2], V21["md5"][2:8] + "….dir")

        # ========================================================== 3. K3: dvc push, the local remote
        on_shelf = note(SHELF_NOTE, S.GREY, 20)
        count = grey_chip(COUNT_NOTE)

        with self.voiceover(SAY[3]) as vo:
            self.play(track(tr, 3), run_time=0.4)
            ln_push = istep(self, t, c104.line(64), type_time=0.3)
            vo.wait_until("pause and run it")
            yt3 = beside(turn_row(), ln_push)
            pin(self, ln_push, yt3)
            flash_tag(self, yt3, TURN)
            out(self, t, [squash(c104.line(65)), c104.line(66), (c104.line(67), r)], run_time=0.5)
            self.play(Indicate(t.lines[-1], color=ERR, scale_factor=1.04), run_time=0.5)
            vo.wait_until("Here the local stand-in")
            lb = on_bar(t, local_row())
            self.play(FadeIn(lb, shift=LEFT * 0.1), track(tr, 3, extra="local remote"), run_time=0.4)
            istep(self, t, c104.line(70), type_time=0.4)
            vo.wait_until("2 files pushed")
            rows73 = out(self, t, [squash(c104.line(71)), c104.line(72), (c104.line(73), y)], run_time=0.5)
            self.play(Indicate(rows73[-1], color=TURN, scale_factor=1.08),
                      Indicate(new_photo.text, color=HASH, scale_factor=1.15),
                      Indicate(man21.text, color=HASH, scale_factor=1.15), run_time=0.7)
            vo.wait_until("because the four old photos")
            on_shelf.move_to([hs.rack.frame.get_right()[0] - 0.2 - on_shelf.width / 2,
                              hs.rack.head.get_center()[1], 0])
            self.play(each([s.text for s in photo_slips], PASS, scale=1.12), FadeIn(on_shelf), run_time=1.0)
            self.play(*[s.text.animate.set_color(PASS) for s in photo_slips], run_time=0.4)
            count.move_to([-0.4, -0.75, 0])
            self.play(FadeIn(count, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("That is the saved space")
            self.play(Indicate(count.text, color=INK, scale_factor=1.1), Indicate(ref, color=INK, scale_factor=1.05),
                      run_time=0.8)

        # ========================================================== 4. K4: git ×5, v21 on the rope; extras
        tg = TagRope()
        for i in (0, 1, 2):
            tg.beads[i].set_z_index(1)
        v6_base = [tg.line, tg.beads[0], tg.beads[1], tg.bead_labels[0], tg.bead_labels[1], tg.flags["dataset_v20"],
                   tg.store, tg.dirs["v20"], *[tg.blobs[n] for n in IMAGES[:4]]]
        rope = tg.rope("v21")
        dch = differ_chip("our hashes · yours differ")

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(hs.rack, *aisles, hs.machine, *filed, new_photo, man21, t5, on_shelf, count, lb)
            for a in (V21["md5"][:2], MD5[IMAGES[4]][:2]):
                gone.add(hs.rows[a])
            self.play(FadeOut(gone), track(tr, 4), run_time=0.5)
            self.remove(*gone.get_family())
            istep(self, t, c104.line(74), type_time=0.2)
            out(self, t, c104.at(75), run_time=0.2)
            t.set_prompt(P_VERSIONING)
            bare_prompt(self, t)
            self.play(FadeIn(VGroup(*v6_base)), run_time=0.6)
            vo.wait_until("status shows only")
            type_cmd(self, t, c105.cmd, type_time=0.3)
            r105 = out(self, t, c105.at((2, 5)) + [(c105.line(6), y)], run_time=0.5)
            vo.wait_until("the pointer file changed")
            self.play(Indicate(r105[-1], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("then add")
            type_cmd(self, t, c106.cmd, type_time=0.2)
            bare_prompt(self, t)
            vo.wait_until("commit")
            type_cmd(self, t, c107.cmd, type_time=0.5, soft=True)
            out(self, t, c107.at((2, 3)), run_time=0.4)
            self.play(tg.bead(2), run_time=0.5)
            vo.wait_until("tag dataset v21")
            type_cmd(self, t, c108.cmd, type_time=0.6, soft=True)
            bare_prompt(self, t)
            self.play(tg.plant("dataset_v21"), run_time=0.6)
            vo.wait_until("and push")
            ln_gp = type_cmd(self, t, push_cmd, type_time=0.5)
            vo.wait_until("Pause and run them")
            yt4 = beside(turn_row(), ln_gp)
            pin(self, ln_gp, yt4)
            flash_tag(self, yt4, TURN)
            self.play(FadeIn(tg.dirs["v21"]), FadeIn(tg.blobs[IMAGES[4]]), run_time=0.4)
            self.play(Create(rope.main), run_time=0.6)
            self.play(LaggedStart(*[Create(f) for f in rope.fans], lag_ratio=0.15), run_time=0.7)
            self.play(each([tg.blobs[n].text for n in IMAGES[:4]], PASS, scale=1.12), run_time=0.8)
            vo.wait_until("An extra diff")
            unpin(self, ln_gp, yt4)
            v6_all = VGroup(*v6_base, tg.beads[2], tg.bead_labels[2], tg.flags["dataset_v21"], tg.dirs["v21"],
                            tg.blobs[IMAGES[4]], rope)
            self.play(FadeOut(v6_all), track(tr, 4, extra=True), run_time=0.4)
            self.remove(*v6_all.get_family())
            resize(self, t, 11, run_time=0.5)
            xb4 = on_bar(t, extra_row())
            self.play(FadeIn(xb4, shift=LEFT * 0.1), run_time=0.3)
            type_cmd(self, t, c110.cmd, type_time=0.4)
            r110 = out(self, t, [c110.line(7)] + [(x, y) for x in c110.at((8, 13))] + c110.at((14, 15)), run_time=0.6)
            vo.wait_until("the whole change in three lines")
            self.play(each(list(r110[1:4]), ERR, scale=1.04), run_time=0.7)
            self.play(each(list(r110[4:7]), PASS, scale=1.04), run_time=0.7)
            type_cmd(self, t, c111.cmd, type_time=0.3)
            r111 = out(self, t, c111.at((2, 4)), run_time=0.4)
            dch.next_to(t.box, UP, buff=0.15).align_to(t.box, RIGHT)
            self.play(substring(r111[0], "tag: dataset_v21").animate.set_color(PASS),
                      substring(r111[1], "tag: dataset_v20").animate.set_color(PASS),
                      FadeIn(dch, shift=DOWN * 0.1), run_time=0.5)
            type_cmd(self, t, c112.cmd, type_time=0.2)
            r112 = out(self, t, c112.at((2, 3)), run_time=0.4)
            self.play(Indicate(r112[1], color=PASS, scale_factor=1.04), run_time=0.6)

        # ========================================================== 5. K4 · extra: the old README's remote add
        old = VGroup(label("Add a remote origin", 22, INK),
                     mono("git remote add origin", 22, INK),
                     mono(f"git@github.com:{GH_USER}/data-versioning.git", 22, INK)).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.12)
        c148 = readme_card(148, old, size=22, repo="starter")
        c148.frame.set_stroke(ERR)
        err = erratum_tag()
        note372 = VGroup(label("You only need to run git remote add origin ... once,", 22, INK),
                         label("when you first create your repository.", 22, INK),
                         label("Do not add it again here.", 22, TURN)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        c372 = readme_card(372, note372, quote=True, size=22, repo=DV)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(dch, xb4)), run_time=0.3)
            self.remove(dch, xb4)
            resize(self, t, 3, keep=0, run_time=0.5)
            bare_prompt(self, t)
            top = t.box.get_top()[1] + 0.15
            VGroup(c148, c372).arrange(DOWN, buff=0.3).move_to([0, (PIC_TOP + top) / 2, 0])
            err.move_to([c148.frame.get_right()[0] - 0.25 - err.width / 2, c148.head.get_center()[1], 0])
            self.play(FadeIn(c148, shift=DOWN * 0.15), FadeIn(err), run_time=0.6)
            vo.wait_until("adds the remote again")
            self.play(Indicate(old[1], color=ERR, scale_factor=1.05), run_time=0.6)
            xb5 = on_bar(t, extra_row())
            self.play(FadeIn(xb5, shift=LEFT * 0.1), run_time=0.3)
            type_cmd(self, t, c113.cmd, type_time=0.8)
            vo.wait_until("That fails")
            r113 = out(self, t, [(c113.line(2), r)], run_time=0.4)
            vo.wait_until("remote origin already exists")
            self.play(Indicate(r113[0], color=ERR, scale_factor=1.06), run_time=0.6)
            vo.wait_until("The pinned README")
            self.play(FadeIn(c372, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(note372[2], color=TURN, scale_factor=1.06), run_time=0.7)

        # ========================================================== 6. K4 · extra · stand-in: time travel on disk
        v6_back = VGroup(tg.line, *tg.beads, *tg.bead_labels, tg.flags["dataset_v20"], tg.flags["dataset_v21"],
                         tg.store, tg.dirs["v20"], tg.dirs["v21"], *tg.blobs.values())
        cache = VGroup(mono(".dvc/cache", 22, LAPTOP), label("your disk", 20, S.GREY)).arrange(DOWN, buff=0.1)
        cfr = RoundedRectangle(width=cache.width + 0.7, height=cache.height + 0.4, corner_radius=0.14,
                               stroke_color=LAPTOP, stroke_width=3).set_fill(LAPTOP, 0.07)
        cache.move_to(cfr)
        cbox = VGroup(cfr, cache).move_to([-3.4, 0.0, 0])
        real = card([label(s, 22, INK) for s in REAL_MOUNT], size=22)
        cur = Polygon([0, 0, 0], [-0.14, -0.26, 0], [0.14, -0.26, 0], stroke_color=S.GREY,
                      stroke_width=2).set_fill(S.GREY, 0.8)

        def under_bead(i):
            return [tg.beads[i].get_x(), tg.bead_labels[i].get_bottom()[1] - 0.1 - cur.height / 2, 0]

        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(c148, c372, err, xb5)
            self.play(FadeOut(gone), track(tr, 4, extra="stand-in"), run_time=0.5)
            self.remove(*gone.get_family())
            sb6 = on_bar(t, standin_row())
            self.play(FadeIn(v6_back), FadeIn(sb6, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("check out the old pointer file")
            type_cmd(self, t, c114.cmd, type_time=0.6)
            out(self, t, c114.at(2), run_time=0.3)
            cur.move_to(under_bead(1))
            self.play(FadeIn(cur, shift=UP * 0.2), Indicate(tg.flags["dataset_v20"].text, color=POINTER), run_time=0.6)
            vo.wait_until("run dvc checkout")
            reenter(self, t, "115", type_time=0.2)
            istep(self, t, c115.line(45), type_time=0.2)
            out(self, t, c115.at(49), run_time=0.3)
            vo.wait_until("and the folder holds four photos")
            istep(self, t, c115.line(50), type_time=0.2)
            r51 = out(self, t, [(c115.line(51), g)], run_time=0.3)
            self.play(Indicate(r51[0], color=PASS, scale_factor=1.05),
                      each([tg.blobs[n].text for n in IMAGES[:4]], PASS, scale=1.1), run_time=0.7)
            vo.wait_until("Back to main")
            istep(self, t, c115.line(52), type_time=0.1)
            out(self, t, c115.at(53), run_time=0.2)
            t.set_prompt(P_VERSIONING)
            type_cmd(self, t, c116.cmd, type_time=0.5)
            bare_prompt(self, t)
            self.play(cur.animate.move_to(under_bead(2)), Indicate(tg.flags["dataset_v21"].text, color=POINTER),
                      run_time=0.6)
            vo.wait_until("and five")
            reenter(self, t, "117", type_time=0.2)
            istep(self, t, c117.line(45), type_time=0.2)
            out(self, t, c117.at(49), run_time=0.3)
            istep(self, t, c117.line(50), type_time=0.2)
            r51b = out(self, t, [(c117.line(51), g)], run_time=0.3)
            vo.wait_until("from the cache on disk")
            dn = arrow(cbox.get_bottom(), np.array([cbox.get_x(), t.box.get_top()[1] + 0.05, 0]), LAPTOP, stroke=4)
            self.play(FadeIn(cbox, shift=UP * 0.1), run_time=0.4)
            self.play(GrowArrow(dn), Indicate(r51b[0], color=PASS, scale_factor=1.05), run_time=0.6)
            self.play(Indicate(cache[0], color=INK, scale_factor=1.1), run_time=0.5)
            vo.wait_until("With a real mount")
            v6_gone = VGroup(v6_back, cur, cbox, dn)
            self.play(FadeOut(v6_gone), run_time=0.5)
            self.remove(*v6_gone.get_family())
            real.move_to([0, band_mid(t), 0])
            self.play(FadeIn(real, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("so checkout deletes")
            self.play(Indicate(real.body[1], color=INK, scale_factor=1.04), run_time=0.7)

        self.wait(1.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
