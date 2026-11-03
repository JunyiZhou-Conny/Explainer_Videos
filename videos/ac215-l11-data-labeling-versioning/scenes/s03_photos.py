"""S03 · A key, 21 photos and a bucket — tracker A3 → A6, `lref("5–6, 11")` the whole scene.

Beats (script.md, ## S03; one voiceover block each):
0. TRACKER A3. Schematic console (`illustration`) with README:44–50's steps, a YELLOW pointer walks
   them: IAM & Admin → Service accounts · Create service account · data-service-account · Grant …
   Cloud Storage → Storage Admin · KEYS → ADD Key (Create New Key) → JSON. A JSON file drops into the
   GREEN secrets/ box and is renamed data-service-account.json. On "every bucket in the project" a
   GREY chip under the role. ▶ your turn.
1. TRACKER A3 · extra. `ls -la secrets` (06: 2–5, the long row folds); the file name ringed (never its
   size); a GREY `stand-in` row tag + "explained at Source storage" (S05 explains it at step B5,
   the name its tracker shows; the video shows no scene numbers).
2. TRACKER A4. README card (lines 62–65) above the terminal. The README's link with curl (07: 2,
   3720496 ringed), then `unzip` (08: 2–9, …, 44–45); the __MACOSX twin rows flash GREY. ▶ your turn.
3. The two folders side by side, counts hidden ('? files'). QUICK(4 s).
4. TRACKER A4 · extra. On "21." the image folder's count turns 21. The extra count (09: 2–4, …, 11,
   …, 23–29): 23 and 29 `21` and line 11 `Image_3.png` ringed YELLOW. The terminal shrinks to a strip;
   the 21 twins drop into a RED bin "discard · don't upload"; a broken task flickers; a small GREY
   funnel 'curation' sorts the 21 images into "keep".
5. TRACKER A4 · extra. md5sum … ; wc -c … (20 pt, folds) → 09b: 2–12, GREY chip "macOS: md5 -r";
   the five md5s underline one by one; line 2's md5 gets a PINK ring and the pin "part 2".
6. TRACKER A5. Console (`illustration`, README:67–72): Create bucket · your-bucket-placeholder,
   (REPLACE WITH YOUR BUCKET NAME), Keep the defaults → the two folders. TRACKER A6 (README:76): 21
   blank tiles fly into cheeses_unlabeled/. ▶ your turn. V7: BLUE bucket 1 lights; GOLD cost tag.
   Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S03"]
ROLE_NOTE = "project-wide · this tutorial needs object read/write + storage.buckets.update (for CORS)"
COST_NOTE = "storage starts here · ≈ 3.8 MB · a fraction of a cent a month · check the pricing page"
QUICK_Q = "The zip held 42 files.\nHow many tasks (one item to label each)\nshould Label Studio make?"


def curl_fold(t, cmd: str):
    """t.fold for c07's curl: ' \\' before the URL and before '&&'; the 76-character URL is longer
    than a 22 pt row (65), so it soft-wraps once, after 'v4.0/', with no marker inside it (a ' \\'
    there would split the URL). Rows join back to the exact command, asserted."""
    head, rest = cmd.split(" https://", 1)
    url, tail = rest.split(" && ", 1)
    url = "https://" + url
    cut = url.index("/cheeses_unlabeled.zip") + 1

    def fold(text: str, first_prefix: int = 0) -> list[str]:
        rows = [text[:first_prefix] + head + " \\", "    " + url[:cut], url[cut:] + " \\", "    && " + tail]
        assert all(len(r) <= t.max_chars for r in rows), rows
        joined = rows[0][:-2] + " " + rows[1][4:] + rows[2][:-2] + " " + rows[3][4:]
        assert joined == text, (joined, text)
        return rows
    return fold


def arrow_word() -> Text:
    return label("→", 22, S.GREY)


def console_row(*parts) -> VGroup:
    """One console step: words (str → label, INK) and mobjects in a row."""
    ms = [label(p, 22, INK) if isinstance(p, str) else p for p in parts]
    return VGroup(*ms).arrange(RIGHT, buff=0.18)


def folder_box(name: str, items: VGroup, box_w: float = 5.6) -> VGroup:
    """A GREY laptop folder: folder glyph + mono name, a row of items, a GREY '? files' chip.
    .frame .head .items .chip"""
    head = VGroup(folder_glyph(0.3, LAPTOP), mono(name, 22, INK)).arrange(RIGHT, buff=0.16)
    ch = grey_chip("? files")
    body = VGroup(head, items, ch).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    items.shift(RIGHT * 0.3)
    fr = RoundedRectangle(width=box_w, height=body.height + 0.55, corner_radius=0.16, stroke_color=LAPTOP,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, body)
    g.frame, g.head, g.items, g.chip = fr, head, items, ch
    return g


def bin_glyph(bin_w: float = 1.9, bin_h: float = 1.1, color=ERR) -> VMobject:
    """An open-topped bin (no text)."""
    w, h = bin_w / 2, bin_h / 2
    return VMobject(stroke_color=color, stroke_width=3.5).set_points_as_corners(
        [[-w, h, 0], [-w * 0.8, -h, 0], [w * 0.8, -h, 0], [w, h, 0]])


def funnel_glyph(f_w: float = 1.1, color=S.GREY) -> VMobject:
    w = f_w / 2
    return VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
        [[-w, 0.35, 0], [-0.1, -0.15, 0], [-0.1, -0.5, 0], [0.1, -0.5, 0], [0.1, -0.15, 0], [w, 0.35, 0]])


class KeyAndPhotos(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S03"] == 7, len(SAY)

        # ========================================================== 0. the service account and its key
        tr = tracker("A", 3)
        ref = lref("5–6, 11")
        win = window("console.cloud.google.com", 12.4, 3.75).move_to([0, 0.85, 0])
        ill = illustration_tag().move_to([0, -1.42, 0]).align_to(win, RIGHT)
        x0 = win.get_left()[0] + 0.85
        role = label("Storage Admin", 22, INK)
        json_w = label("JSON", 22, INK)
        steps = [
            console_row("IAM & Admin", arrow_word(), "Service accounts"),
            console_row("Create service account", label("·", 22, S.GREY), mono(SA_NAME, 22, INK)),
            console_row("Grant this service account access to project:"),
            console_row("Cloud Storage", arrow_word(), role),
            console_row(mono("KEYS", 22, INK), arrow_word(), "ADD Key (Create New Key)", arrow_word(), json_w),
        ]
        for s, y in zip(steps, (1.95, 1.45, 0.95, 0.5, -0.6)):
            s.move_to([x0, y, 0], aligned_edge=LEFT)
        role_chip = grey_chip(ROLE_NOTE).move_to([x0, -0.05, 0], aligned_edge=LEFT)
        ptr = label("▶", 22, TURN)

        def ptr_at(i):
            return ptr.copy().next_to(steps[i], LEFT, buff=0.25)

        ptr.move_to(ptr_at(0))
        sec_box = outline_box(8.0, 0.9, KEY, solid=True).move_to([-2.1, -2.6, 0])
        sec_lbl = mono("secrets/", 22, KEY).move_to(sec_box).align_to(sec_box, LEFT).shift(RIGHT * 0.3)
        sec = VGroup(sec_box, sec_lbl)
        fg = file_glyph(0.42, KEY)
        ftxt = mono("JSON", 22, INK)
        jfile = VGroup(fg, ftxt).arrange(RIGHT, buff=0.15).next_to(steps[4], RIGHT, buff=0.4)
        land = np.array([sec_lbl.get_right()[0] + 0.5 + jfile.width / 2, sec_box.get_center()[1], 0])
        named = mono(KEY_FILE, 22, INK)
        yt = your_turn().move_to([4.75, -2.6, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.6)
            vo.wait_until("In the console")
            self.play(FadeIn(win, scale=0.97), FadeIn(ill), run_time=0.7)
            self.play(FadeIn(steps[0], shift=RIGHT * 0.2), FadeIn(ptr), run_time=0.6)
            vo.wait_until("create a service account named")
            self.play(FadeIn(steps[1], shift=RIGHT * 0.2), ptr.animate.move_to(ptr_at(1)), run_time=0.6)
            self.play(Indicate(steps[1][2], color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("with the Storage Admin role")
            self.play(FadeIn(steps[2], shift=RIGHT * 0.2), FadeIn(steps[3], shift=RIGHT * 0.2),
                      ptr.animate.move_to(ptr_at(3)), run_time=0.7)
            self.play(Indicate(role, color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("Then create one JSON key")
            self.play(FadeIn(steps[4], shift=RIGHT * 0.2), ptr.animate.move_to(ptr_at(4)), run_time=0.7)
            self.play(Indicate(json_w, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("saved in your secrets folder")
            self.play(FadeIn(sec, shift=UP * 0.15), FadeIn(jfile, scale=0.8), run_time=0.6)
            self.play(jfile.animate.move_to(land), run_time=0.9)
            named.move_to(ftxt, aligned_edge=LEFT)
            self.play(FadeTransform(ftxt, named), run_time=0.8)
            jfile.remove(ftxt)
            jfile.add(named)
            vo.wait_until("This role is broader")
            self.play(ptr.animate.move_to(ptr_at(3)), Indicate(role, color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("it covers every bucket")
            self.play(FadeIn(role_chip, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("Pause and create yours")
            self.play(FadeIn(yt, shift=LEFT * 0.2), ptr.animate.move_to(ptr_at(4)), run_time=0.5)
            flash_tag(self, yt, TURN)

        # ========================================================== 1. extra: the key is in place
        t = term(P_LAPTOP_HOME, rows=8)
        c06 = capture("06")

        with self.voiceover(SAY[1]) as vo:
            old = VGroup(win, ill, *steps, role_chip, ptr, sec, jfile, yt)
            self.play(FadeOut(old), run_time=0.5)
            self.remove(old, *old)
            self.play(FadeIn(t), track(tr, 3, extra=True), run_time=0.6)
            ln = type_cmd(self, t, c06.cmd, type_time=0.6)
            xt = beside(extra_row(), ln)
            pin(self, ln, xt)
            out(self, t, c06.at((2, 5)), wrap=True)
            frow = t.find(KEY_FILE)
            fring = ring(substring(frow, KEY_FILE), TURN)
            self.play(Create(fring), run_time=0.5)
            vo.wait_until("a stand-in")
            st = beside(row_tag("stand-in", S.GREY), frow)
            pin(self, frow, st)
            cap5 = note("explained at Source storage").next_to(st, RIGHT, buff=0.25)
            self.play(FadeIn(cap5, shift=LEFT * 0.1), run_time=0.4)
            attach(self, frow, cap5)
            flash_tag(self, st, INK)

        # ========================================================== 2. download and extract
        rc = readme_card((62, 65), "Download the unlabeled data from here\nExtract the zip file")
        rc.move_to([-6.5, 2.72, 0], aligned_edge=UL)
        curl_chip = grey_chip("the README's link, with curl")
        unz_chip = grey_chip("the README says extract")
        curl_chip.move_to([rc.get_right()[0] + 0.4, rc.get_center()[1] + 0.3, 0], aligned_edge=LEFT)
        unz_chip.next_to(curl_chip, DOWN, buff=0.18, aligned_edge=LEFT)
        c07, c08 = capture("07"), capture("08")

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(fring), track(tr, 4), FadeIn(rc, shift=DOWN * 0.2), run_time=0.6)
            self.remove(fring)
            unpin(self, frow, cap5)
            unpin(self, frow, st)
            unpin(self, ln, xt)
            self.play(Indicate(rc.body[0], color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("we use curl")
            self.play(FadeIn(curl_chip, shift=LEFT * 0.2), run_time=0.4)
            t.fold = curl_fold(t, c07.cmd)
            try:
                cl = type_cmd(self, t, c07.cmd, type_time=1.2)
            finally:
                del t.fold
            wtag = beside(row_tag("one URL · wrapped, no space"), cl.rows[2])
            pin(self, cl.rows[2], wtag)
            zrows = out(self, t, c07.at(2), wrap=True)
            zring = ring(substring(zrows[0], "3720496"), TURN)
            vo.wait_until("and a browser works too")
            self.play(Create(zring), run_time=0.5)
            vo.wait_until("Then extract the zip")
            unpin(self, cl.rows[2], wtag, FadeOut(zring), Indicate(rc.body[1], color=INK, scale_factor=1.04),
                  FadeIn(unz_chip, shift=LEFT * 0.2), run_time=0.6)
            self.remove(zring)
            type_cmd(self, t, c08.cmd, type_time=0.5)
            out(self, t, c08.at((2, 9), "…", (44, 45)), chunk=4)
            vo.wait_until("Pause and do both")
            ty = on_bar(t, turn_row())
            self.play(FadeIn(ty, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, ty, TURN)
            vo.wait_until("Notice that every image")
            twins = [r for r in t.lines if "__MACOSX" in getattr(r, "text", "")]
            imgs = [r for r in t.lines if "inflating: cheeses_unlabeled/" in getattr(r, "text", "")]
            self.play(each(imgs, INK, scale=1.03, lag=0.2), run_time=1.0)
            self.play(each(twins, S.GREY, scale=1.05, lag=0.25), run_time=1.2)

        # ========================================================== 3. two folders, counts hidden
        im_items = VGroup(*[tile(None, 0.55, LAPTOP) for _ in range(4)], label("…", 26, S.GREY))
        im_items.arrange(RIGHT, buff=0.25)
        tw_items = VGroup(*[file_glyph(0.5, S.GREY) for _ in range(4)], label("…", 26, S.GREY))
        tw_items.arrange(RIGHT, buff=0.42)
        fold_l = folder_box("cheeses_unlabeled/", im_items).move_to([-3.45, 0.3, 0])
        fold_r = folder_box("__MACOSX/cheeses_unlabeled/", tw_items, box_w=6.3).move_to([3.45, 0.3, 0])

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(t, rc, curl_chip, unz_chip, ty)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone, *t.lines)
            self.play(FadeIn(fold_l, shift=RIGHT * 0.3), FadeIn(fold_r, shift=LEFT * 0.3), run_time=0.8)
            vo.wait_until("the zip held 42 files")
            self.play(each([fold_l.chip.text, fold_r.chip.text], INK, scale=1.15, lag=0.3), run_time=0.9)
            vo.wait_until("How many tasks")
            self.play(each(list(fold_l.items[:4]), TURN, scale=1.1, lag=0.15), run_time=1.0)
        qcard = quick_predict(self, QUICK_Q)

        # ========================================================== 4. 21: curation
        c09 = capture("09")
        t = term(P_LAPTOP_HOME, rows=10)
        n_img = grey_chip("21 files", color=TURN).move_to(fold_l.chip, aligned_edge=LEFT)
        n_mac = grey_chip("21 files").move_to(fold_r.chip, aligned_edge=LEFT)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(qcard), FadeTransform(fold_l.chip, n_img), FadeTransform(fold_r.chip, n_mac), run_time=0.6)
            self.remove(qcard)
            fold_l[1].remove(fold_l.chip)
            fold_r[1].remove(fold_r.chip)
            vo.wait_until("An extra count shows")
            fl = VGroup(fold_l, fold_r, n_img, n_mac)
            self.play(FadeOut(fl), FadeIn(t), track(tr, 4, extra=True), run_time=0.6)
            self.remove(fl, *fl)
            xb = on_bar(t, extra_row())
            self.play(FadeIn(xb, shift=LEFT * 0.1), run_time=0.3)
            type_cmd(self, t, c09.cmd, type_time=1.0)
            out(self, t, c09.at((2, 4), "…", 11, "…", 23))
            r23 = t.lines[-1]
            g23 = ring(substring(r23, "21"), TURN)
            self.play(Create(g23), run_time=0.4)
            vo.wait_until("one of them a PNG")
            g11 = ring(substring(t.find("Image_3.png"), "Image_3.png"), TURN)
            self.play(Create(g11), run_time=0.5)
            vo.wait_until("plus 21 Mac metadata files")
            self.play(FadeOut(VGroup(g23, g11)), run_time=0.3)
            self.remove(g23, g11)
            out(self, t, c09.at((24, 29)), run_time=0.5)
            g29 = ring(substring(t.lines[-1], "21"), TURN)
            self.play(Create(g29), run_time=0.4)
            vo.wait_until("Upload only the images")
            self.play(FadeOut(VGroup(g29, xb)), run_time=0.3)
            self.remove(g29, xb)
            resize(self, t, 3, run_time=0.6)
            imgs = VGroup(*[tile(None, 0.36, LAPTOP) for _ in range(21)]).arrange_in_grid(rows=3, cols=7, buff=0.1)
            imgs.move_to([-4.0, 1.7, 0])
            twins = VGroup(*[file_glyph(0.3, S.GREY) for _ in range(21)]).arrange_in_grid(rows=3, cols=7,
                                                                                          buff=(0.2, 0.08))
            twins.move_to([-4.0, -0.35, 0])
            l_img = mono("cheeses_unlabeled/", 20, INK).next_to(imgs, UP, buff=0.15)
            l_mac = mono("__MACOSX/cheeses_unlabeled/", 20, S.GREY).next_to(twins, UP, buff=0.15)
            l_mac.align_to(twins, LEFT)
            l_img.align_to(imgs, LEFT)
            bn = bin_glyph().move_to([4.3, -0.5, 0])
            bn_l = label("discard · don't upload", 22, ERR).next_to(bn, UP, buff=0.15)
            keep = outline_box(2.4, 1.2, LAPTOP, solid=True).move_to([4.3, 1.75, 0])
            keep_l = label("keep", 22, INK).next_to(keep, UP, buff=0.1)
            self.play(FadeIn(VGroup(imgs, l_img), shift=DOWN * 0.15), FadeIn(VGroup(twins, l_mac), shift=UP * 0.15),
                      run_time=0.6)
            self.play(Create(bn), FadeIn(bn_l), run_time=0.5)
            self.play(LaggedStart(*[f.animate.move_to(bn.get_center() + DOWN * 0.15).set_opacity(0) for f in twins],
                                  lag_ratio=0.04), FadeOut(l_mac), run_time=1.4)
            self.remove(twins, l_mac)
            vo.wait_until("or you get 21 broken tasks")
            bt = tile(None, 0.6, ERR, broken=True).move_to([1.2, -0.35, 0])
            bt_l = note("a broken task", ERR).next_to(bt, DOWN, buff=0.12)
            self.play(FadeIn(VGroup(bt, bt_l), scale=0.9), run_time=0.5)
            self.play(Wiggle(bt, scale_value=1.1), run_time=0.7)
            vo.wait_until("The lecture calls this curation")
            fun = funnel_glyph().move_to([1.2, 1.85, 0])
            fun_l = label("curation", 22, S.GREY).next_to(fun, UP, buff=0.12)
            self.play(FadeOut(VGroup(bt, bt_l)), Create(fun), FadeIn(fun_l), Create(keep), FadeIn(keep_l),
                      run_time=0.7)
            self.remove(bt, bt_l)
            vo.wait_until("dropping junk")
            self.play(imgs.animate.scale(0.35).move_to(fun.get_center() + UP * 0.1), FadeOut(l_img), run_time=0.8)
            self.remove(l_img)
            self.play(imgs.animate.scale(2.0).move_to(keep), run_time=0.8)

        # ========================================================== 5. extra: fingerprints, planted for part 2
        c9b = capture("09b")
        t2 = term(P_LAPTOP_HOME, rows=12, size=20)
        mchip = grey_chip("macOS: md5 -r").move_to([0, t2.box.get_top()[1] + 0.38, 0]).align_to(t2.box, RIGHT)

        with self.voiceover(SAY[5]) as vo:
            pic = VGroup(t, imgs, bn, bn_l, keep, keep_l, fun, fun_l)
            self.play(FadeOut(pic), run_time=0.5)
            self.remove(pic, *pic, *t.lines)
            self.play(FadeIn(t2), run_time=0.4)
            xb2 = on_bar(t2, extra_row())
            self.play(FadeIn(xb2, shift=LEFT * 0.1), FadeIn(mchip, shift=DOWN * 0.1), run_time=0.4)
            type_cmd(self, t2, c9b.cmd, type_time=1.4)
            out(self, t2, c9b.at((2, 6)), run_time=0.6)
            hrows = [t2.find(MD5[n]) for n in IMAGES]
            vo.wait_until("computed from its bytes alone")
            uls = [under(substring(r, r.text[:32]), HASH, stroke=3) for r in hrows]
            self.play(LaggedStart(*[Create(u) for u in uls], lag_ratio=0.35), run_time=1.6)
            vo.wait_until("Same bytes, same string")
            self.play(each([substring(r, r.text[:32]) for r in hrows], HASH, scale=1.04, lag=0.2), run_time=1.2)
            vo.wait_until("change one byte")
            self.play(FadeOut(VGroup(*uls)), run_time=0.3)
            self.remove(*uls)
            out(self, t2, c9b.at((7, 12)), run_time=0.6)
            self.play(each([substring(r, r.text[:32]) for r in hrows[1:]], INK, scale=1.04, lag=0.15),
                      run_time=1.0)
            vo.wait_until("Remember the first one")
            first = hrows[0]
            h1 = substring(first, MD5["Image_1.jpg"])
            g1 = ring(h1, HASH)
            self.play(Create(g1), run_time=0.6)
            attach(self, first, g1)
            p2 = beside(row_tag("part 2", HASH), first, buff=0.3)
            pin(self, first, p2)
            flash_tag(self, p2, HASH)

        # ========================================================== 6. the bucket, the upload, the cost
        win2 = window("console.cloud.google.com/storage/browser", 12.4, 4.9).move_to([0, 0.3, 0])
        ill2 = illustration_tag().move_to([0, -2.62, 0]).align_to(win2, RIGHT)
        bx0 = win2.get_left()[0] + 0.5
        field = mono(BUCKET, 22, INK)
        fbox = RoundedRectangle(width=field.width + 0.5, height=0.46, corner_radius=0.08, stroke_color=CLOUD,
                                stroke_width=2).set_fill(TERM_BG, 1)
        field.move_to(fbox)
        r1 = VGroup(label("Create bucket", 22, INK), VGroup(fbox, field)).arrange(RIGHT, buff=0.3)
        r1.move_to([bx0, 1.85, 0], aligned_edge=LEFT)
        r2 = label("(REPLACE WITH YOUR BUCKET NAME)", 22, S.GREY).move_to([bx0, 1.3, 0], aligned_edge=LEFT)
        glob = grey_chip("bucket names are global").next_to(r2, RIGHT, buff=0.35)
        r3 = VGroup(check_mark(0.3, CLOUD), label("Keep the defaults", 22, INK)).arrange(RIGHT, buff=0.2)
        r3.move_to([bx0, 0.75, 0], aligned_edge=LEFT)
        bk = vault(BUCKET, ("cheeses_unlabeled/", "cheeses_labeled/"), CLOUD, 20, vault_w=4.4)
        bk.move_to([3.2, -0.95, 0])
        drs = [bk.drawers["cheeses_unlabeled/"], bk.drawers["cheeses_labeled/"]]
        up = VGroup(*[tile(None, 0.34, LAPTOP) for _ in range(21)]).arrange_in_grid(rows=3, cols=7, buff=0.1)
        up.move_to([-3.4, -1.05, 0])
        up_l = mono("cheeses_unlabeled/", 20, S.GREY).next_to(up, UP, buff=0.15).align_to(up, LEFT)
        yt2 = your_turn().move_to([0, -2.62, 0]).align_to(win2, LEFT)
        m = PipelineMap.at("S03")
        cost = cost_tag(COST_NOTE).move_to([0, -2.1, 0])

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(t2, xb2, mchip)), run_time=0.5)
            self.remove(t2, xb2, mchip, *t2.lines)
            self.play(FadeIn(win2, scale=0.97), FadeIn(ill2), track(tr, 5), run_time=0.7)
            self.play(FadeIn(r1, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("with a name of your own")
            self.play(FadeIn(r2, shift=RIGHT * 0.2), Indicate(field, color=CLOUD, scale_factor=1.06), run_time=0.7)
            vo.wait_until("since names are global")
            self.play(FadeIn(glob, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and keep the defaults")
            self.play(FadeIn(r3, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Add two folders")
            self.play(FadeIn(bk.frame), FadeIn(bk.title), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.15) for d in drs], lag_ratio=0.4), run_time=0.9)
            vo.wait_until("and upload the 21 images")
            self.play(FadeIn(VGroup(up, up_l), shift=UP * 0.15), track(tr, 6), run_time=0.6)
            dst = drs[0].get_center()
            self.play(LaggedStart(*[x.animate.move_to(dst).scale(0.3).set_opacity(0) for x in up], lag_ratio=0.05),
                      FadeOut(up_l), run_time=1.6)
            self.remove(up, up_l)
            self.play(Indicate(drs[0].text, color=CLOUD, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Pause and set it up")
            self.play(FadeIn(yt2, shift=RIGHT * 0.2), run_time=0.4)
            flash_tag(self, yt2, TURN)
            vo.wait_until("A gold tag")
            con = VGroup(win2, ill2, r1, r2, glob, r3, bk, yt2)
            self.play(FadeOut(con), FadeIn(m), run_time=0.8)
            self.remove(con, *con)
            self.play(m.light("bucket1"), run_time=0.8)
            vo.wait_until("storage starts here")
            self.play(FadeIn(cost, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, cost, COST)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
