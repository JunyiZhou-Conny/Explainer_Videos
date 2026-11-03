"""S10 · A bucket that looks like a folder — no tracker (opening), then tracker H1 → H3, I1;
`lref("21, 27–34")` the whole scene.

Beats (script.md, ## S10; one voiceover block each):
0. No tracker. Slide 21's two cards redrawn: 'Bucket · objects with names + metadata' → '+ tools' →
   'Data lake · the same bucket, plus tools' with five tool ticks; 'return to earlier versions'
   lights. Then a bucket's object list (`illustration`): folders images/ and dvc_store/ melt into
   the PINK shared prefixes of images/Image_1.jpg, images/Image_2.jpg, dvc_store/files/….
1. TRACKER H1. README card (lines 140–144) over a 3-row strip; `cd ..` → prompt ~. The strip grows:
   `tree …` (extra; folds) → 84: 2–3, …, 18–26; data-versioning and secrets/data-service-account.json
   highlighted; GREY chip 'no tree? ls shows the same'. TRACKER H2: the S03 console (`illustration`),
   short: data-service-account, Storage Admin, JSON key (README 148–170); no ▶.
2. TRACKER H3. Console (`illustration`, README 174–187): bucket your-bucket-placeholder (chip 'a new
   bucket, or part 1's'), Create folder dvc_store/ and images/. TRACKER H3 · extra row: erratum card
   (README line 338) + caption; four blank tiles Image_1–4.jpg fly into images/ (`illustration`);
   GOLD cost tag 'images/: a few hundred kB'; ▶ your turn; then V7's second BLUE bucket lights
   (held through the pause: the narration leaves only ~1 s between the folders and "A small gap").
3. TRACKER I1. `cd data-versioning` (no output). CODE(starter docker-shell.sh 5–10) lines 7–9 RED,
   with a GREY README note (lines 201–205) on it (no room for a card beside the panel). The strip grows: the sed edit typed (editor tag) →
   85: 2–7, lines 4–6 GREEN; GREY chip over lines 5–6 'passed in · read by nothing' + erratum tag;
   ▶ your turn.
4. README card (215–230). V4 (FuseMount) built stage by stage over a strip of the starter's
   docker-entrypoint.sh lines 8, 10 (whole, two rows) and 13: Authenticate (key into line 10's
   --key-file; line 8's GREY side note), Bucket Mounting (gcsfuse pipe from the whole bucket),
   Connecting the Application (mount --bind), Using the Data (dvc chip; fetch).
5. Slide 34's chips over line 10 (+ 'two hyphens, full variable name'), the dashed --implicit-dirs
   'not passed here' RED; the object list returns, the images/ marker object glows, only images/
   shows as a folder under /mnt/gcs_data. GREY notes (not spoken): disks → bucket; slide 33.
6. MountLayers: -v (GREY) lights on 'dash v', the inner mount --bind (PINK) on 'the inner one'; the
   host's cheese_dataset/ stays dark.
7. CODE(starter docker-shell.sh 17–27, 20 pt): 18–20 ORANGE, 21 GREY, 22 GREEN, 23 YELLOW + chip.
   Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S10"]
DV = "data-versioning"
STARTER = "data-versioning@data-versioning-ac215"
ENTRY = f"{STARTER}/docker-entrypoint.sh"
SHELL = f"{STARTER}/docker-shell.sh"
TICKS = ("add new data", "find data", "decide who may use it", "prepare it for analysis or training",
         "return to earlier versions")                                   # slide 21's five checks
OBJECTS = (("images/", "Image_1.jpg"), ("images/", "Image_2.jpg"), ("dvc_store/", "files/…"))
ERRATUM_NOTE = "but no step uploads the first ones · today's README (2515e5e) adds that sentence"
GIT_CHIP = "configure git first, or Docker creates a directory here"


def arrow_word(size: float = 22) -> Text:
    return label("→", size, S.GREY)


def console_row(*parts, size: float = 22) -> VGroup:
    """One console step: words (str → label, INK) and mobjects in a row."""
    ms = [label(p, size, INK) if isinstance(p, str) else p for p in parts]
    return VGroup(*ms).arrange(RIGHT, buff=0.18)


def slide_card(title: str, lines, card_w: float, card_h: float, color=CLOUD) -> VGroup:
    """One of slide 21's rounded cards: a title and short lines. .frame .title .lines"""
    tt = label(title, 30, INK)
    ls = VGroup(*[label(s, 22, S.GREY) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    inner = VGroup(tt, ls).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    fr = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.2, stroke_color=color,
                          stroke_width=3).set_fill(S.GREY_DARKER, 1)
    inner.move_to(fr).align_to(fr, LEFT).align_to(fr, UP).shift(RIGHT * 0.35 + DOWN * 0.3)
    g = VGroup(fr, inner)
    g.frame, g.title, g.lines = fr, tt, ls
    return g


def object_row(prefix: str, rest: str, size: float = 20) -> VGroup:
    """An object name as one mono line, its prefix PINK. .prefix .rest"""
    ln = mono_line(prefix + rest, size, INK, t2c={f"[0:{len(prefix)}]": ROUTE})
    ln.prefix = glyph_range(ln, 0, len(prefix))
    ln.rest = glyph_range(ln, len(prefix), len(prefix) + len(rest))
    return ln


def object_list(rows, title: str = "the bucket's objects", list_w: float = 5.2) -> VGroup:
    """A BLUE frame holding object-name rows (mono). .frame .title .rows"""
    tt = label(title, 20, CLOUD)
    col = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    inner = VGroup(tt, col).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    fr = RoundedRectangle(width=list_w, height=inner.height + 0.45, corner_radius=0.16, stroke_color=CLOUD,
                          stroke_width=3).set_fill(CLOUD, 0.06)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, inner)
    g.frame, g.title, g.rows = fr, tt, col
    return g


class BucketAsFolder(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S10"] == 8, len(SAY)
        ref = lref("21, 27–34")

        # ========================================================== 0. bucket vs data lake; prefixes
        bk = slide_card("Bucket", ["objects with names", "+ metadata"], 3.6, 1.9).move_to([-4.55, 0.25, 0])
        tl = label("+ tools", 24, S.GREY)
        ta = Arrow(LEFT * 0.6, RIGHT * 0.6, buff=0, color=S.GREY, stroke_width=3, tip_length=0.18)
        tools = VGroup(tl, ta).arrange(DOWN, buff=0.1).move_to([-1.7, 0.25, 0])
        ticks = VGroup()
        for s in TICKS:
            ticks.add(VGroup(check_mark(0.26, S.GREY), label(s, 22, INK)).arrange(RIGHT, buff=0.2))
        ticks.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        lake = slide_card("Data lake", ["the same bucket, plus tools"], 6.6, 3.95).move_to([3.0, 0.25, 0])
        ticks.next_to(lake.lines, DOWN, buff=0.28).align_to(lake.lines, LEFT)
        last = ticks[-1]
        last_bar = hl_bar(last, TURN, 0.2, buff=0.08)

        # the folder view (left) and the flat object list (right)
        fv_rows = []
        groups = {}
        for pre, rest in OBJECTS:
            if pre not in groups:
                groups[pre] = (drawer(pre, CLOUD, 22), [])
            groups[pre][1].append(mono(rest, 22, INK))
        fv = VGroup()
        for pre, (dr, files) in groups.items():
            fs = VGroup(*files).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            blk = VGroup(dr, fs).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            fs.shift(RIGHT * 0.6)
            fv.add(blk)
            fv_rows.append((dr, files))
        fv.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.6, 0.0, 0])
        fv_head = label("what the console draws", 20, S.GREY).next_to(fv, UP, buff=0.3).align_to(fv, LEFT)
        rows0 = [object_row(p, r, 22) for p, r in OBJECTS]
        ol = object_list(rows0, "what the bucket stores", 5.6).move_to([3.4, 0.0, 0])
        ill0 = illustration_tag().next_to(ol.frame, DOWN, buff=0.2).align_to(ol.frame, RIGHT)
        flat_chip = grey_chip("one flat list of names").next_to(ol.frame, DOWN, buff=0.2).align_to(ol.frame, LEFT)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(bk.frame, scale=0.95), FadeIn(bk.title), run_time=0.7)
            vo.wait_until("A bucket stores named objects")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in bk.lines], lag_ratio=0.3), run_time=0.8)
            vo.wait_until("Add tools")
            self.play(FadeIn(tl, shift=UP * 0.1), GrowArrow(ta), run_time=0.6)
            self.play(FadeIn(lake.frame, scale=0.95), FadeIn(lake.title), FadeIn(lake.lines), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ticks], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("like versioning")
            self.play(FadeIn(last_bar), last[0].animate.set_color(TURN), last[1].animate.set_color(TURN),
                      *[r.animate.set_opacity(0.55) for r in ticks[:-1]], run_time=0.6)
            vo.wait_until("and the lecture calls it a data lake")
            self.play(Indicate(lake.title, color=CLOUD, scale_factor=1.1), run_time=0.7)
            vo.wait_until("Its folders are only shared name prefixes")
            gone = VGroup(bk, tools, lake, ticks, last_bar)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone)
            self.play(FadeIn(fv_head), LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in fv], lag_ratio=0.3),
                      run_time=0.8)
            self.play(FadeIn(ol.frame), FadeIn(ol.title), FadeIn(ill0), run_time=0.5)
            anims = []
            k = 0
            for dr, files in fv_rows:
                for f in files:
                    row = rows0[k]
                    anims.append(TransformFromCopy(dr.text, row.prefix))
                    anims.append(ReplacementTransform(f, row.rest))
                    k += 1
            self.play(*anims, *[dr.animate.set_opacity(0.25) for dr, _ in fv_rows], run_time=1.4)
            self.remove(*[r.prefix for r in rows0], *[r.rest for r in rows0])
            self.add(*rows0)
            self.play(FadeOut(VGroup(*[dr for dr, _ in fv_rows], fv_head)), FadeIn(flat_chip, shift=UP * 0.1),
                      run_time=0.6)
            vo.wait_until("which sets a trap")
            self.play(each([r.prefix for r in rows0], ROUTE, scale=1.15), run_time=0.9)

        # ========================================================== 1. H1: the secrets folder; H2: reuse the key
        tr = tracker("H", 1)
        t = term(P_VERSIONING, rows=3)
        mid = (PIC_TOP + t.box.get_top()[1] + 0.12) / 2
        c140 = readme_card((140, 144), VGroup(*[mono(readme(n, DV), 22, INK) for n in (141, 142, 143)]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1), repo=DV).move_to([0, mid, 0])
        c84 = capture("84")
        tree_out = c84.at((2, 3), "…", (18, 26))
        no_tree = grey_chip("no tree? ls shows the same")

        win = window("console.cloud.google.com", 12.4, 3.6).move_to([0, mid, 0])
        ill1 = illustration_tag().move_to(win.get_corner(DR) + np.array([-1.0, 0.4, 0]))
        x0 = win.get_left()[0] + 0.85
        same = [check_mark(0.3, PASS) for _ in range(3)]
        steps = [
            console_row("IAM & Admin", arrow_word(), "Service accounts", label("·", 22, S.GREY), mono(SA_NAME, 22, INK)),
            console_row("Cloud Storage", arrow_word(), "Storage Admin"),
            console_row(mono("KEYS", 22, INK), arrow_word(), "ADD Key", arrow_word(), "JSON", arrow_word(),
                        mono(f"secrets/{KEY_FILE}", 22, INK)),
        ]
        for s, ck, y in zip(steps, same, (1.6, 1.0, 0.4)):
            s.move_to([x0, y, 0], aligned_edge=LEFT)
            ck.next_to(s, LEFT, buff=0.25)
        r148 = note("README.md · lines 148–170 · the same as part 1").move_to([x0, -0.3, 0], aligned_edge=LEFT)
        for m in (*steps, *same, r148):
            m.shift(UP * (mid - 0.75 - 0.1))

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(ol, ill0, flat_chip)), run_time=0.5)
            self.remove(ol, ill0, flat_chip, *rows0)
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), FadeIn(c140, shift=DOWN * 0.15), run_time=0.6)
            type_cmd(self, t, "cd ..", type_time=0.3)
            cd_prompt(self, t, P_LAPTOP_HOME)
            vo.wait_until("already sits beside this repo")
            self.play(Indicate(c140.body[1], color=INK), Indicate(c140.body[2], color=KEY), run_time=0.8)
            vo.wait_until("as an extra tree view shows")
            self.play(FadeOut(c140, shift=UP * 0.15), track(tr, extra=True), run_time=0.4)
            self.remove(c140)
            resize(self, t, 13, run_time=0.6)
            ln84 = type_cmd(self, t, c84.cmd, type_time=0.8)
            xt = on_bar(t, extra_row())
            self.play(FadeIn(xt, shift=LEFT * 0.1), run_time=0.3)
            out(self, t, tree_out, run_time=0.7)
            dv = t.find("├── data-versioning")
            js = t.find("data-service-account.json")
            sc = t.find("└── secrets")
            bars = [hl_bar(substring(dv, "data-versioning"), TURN, 0.3),
                    hl_bar(substring(sc, "secrets"), KEY, 0.3),
                    hl_bar(substring(js, "data-service-account.json"), KEY, 0.3)]
            self.play(*[FadeIn(b) for b in bars], run_time=0.5)
            for b, row in zip(bars, (dv, sc, js)):
                row.submobjects.insert(0, b)
            beside(no_tree, js, buff=1.0)
            self.play(FadeIn(no_tree, shift=LEFT * 0.15), run_time=0.4)
            self.play(each([dv, sc, js], INK, scale=1.05, lag=0.3), run_time=1.0)
            vo.wait_until("The README wants the same service account and key")
            self.play(FadeOut(VGroup(no_tree, xt)), track(tr, 2), run_time=0.4)
            self.remove(no_tree, xt)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(win, scale=0.97), FadeIn(ill1), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in steps], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("so reuse both")
            self.play(LaggedStart(*[Create(c) for c in same], lag_ratio=0.25), FadeIn(r148), run_time=0.8)
            self.play(Indicate(steps[0][-1], color=INK, scale_factor=1.06), run_time=0.6)

        # ========================================================== 2. H3: two folders; the missing upload
        win2 = window("console.cloud.google.com/storage/browser", 12.4, 3.6).move_to([0, mid, 0])
        ill2 = illustration_tag().move_to(win2.get_corner(DR) + np.array([-1.0, 0.4, 0]))
        bx0 = win2.get_left()[0] + 0.5
        field = mono(BUCKET, 22, INK)
        fbox = RoundedRectangle(width=field.width + 0.5, height=0.46, corner_radius=0.08, stroke_color=CLOUD,
                                stroke_width=2).set_fill(TERM_BG, 1)
        field.move_to(fbox)
        top_y = win2.content.get_top()[1]
        b1 = VGroup(label("Bucket", 22, INK), VGroup(fbox, field)).arrange(RIGHT, buff=0.3)
        b1.move_to([bx0, top_y - 0.45, 0], aligned_edge=LEFT)
        either = grey_chip("a new bucket, or part 1's").next_to(b1, DOWN, buff=0.2).align_to(b1, LEFT)
        cf = [console_row("Create folder", arrow_word(), mono(n, 22, INK)) for n in ("dvc_store/", "images/")]
        for i, r in enumerate(cf):
            r.move_to([bx0, top_y - 1.6 - i * 0.55, 0], aligned_edge=LEFT)
        r174 = note("README.md · lines 174–187").move_to([bx0, win2.get_bottom()[1] + 0.35, 0], aligned_edge=LEFT)
        vb = vault(BUCKET, ("dvc_store/", "images/"), CLOUD, 20, vault_w=4.2)
        vb.move_to([3.35, win2.content.get_center()[1] + 0.15, 0])
        m = PipelineMap.at("S10")

        c338 = readme_card(338, VGroup(label("Upload a few additional images to the", 22, INK),
                                       VGroup(mono("images", 22, INK), label("folder in your GCS bucket:", 22, INK))
                                       .arrange(RIGHT, buff=0.12, aligned_edge=DOWN)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.12), repo=DV)
        assert "Upload a few additional images" in readme(338, DV)
        c338.move_to([-6.45 + c338.width / 2, 1.85, 0])
        ert = erratum_tag().next_to(c338, RIGHT, buff=0.25).align_to(c338, UP)
        cap = VGroup(*[note(x) for x in ERRATUM_NOTE.split(" · ")]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        cap.next_to(c338, DOWN, buff=0.15).align_to(c338, LEFT)
        vb2 = vault(BUCKET, ("images/", "dvc_store/"), CLOUD, 20, vault_w=4.2).move_to([4.2, 0.25, 0])
        tiles = VGroup(*[tile(n, 0.55, LAPTOP) for n in IMAGES[:4]]).arrange(RIGHT, buff=0.3)
        tiles.move_to([-2.4, -0.45, 0])
        ill3 = illustration_tag().next_to(tiles, DOWN, buff=0.15).align_to(tiles, LEFT)
        cost = cost_tag("images/: a few hundred kB").next_to(vb2, DOWN, buff=0.2)
        yt = your_turn().next_to(ill3, RIGHT, buff=0.3)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(win, ill1, *steps, *same, r148)), track(tr, 3), run_time=0.5)
            self.remove(win, ill1, *steps, *same, r148)
            self.play(FadeIn(win2, scale=0.97), FadeIn(ill2), FadeIn(b1, shift=RIGHT * 0.2), run_time=0.7)
            self.play(FadeIn(either, shift=UP * 0.1), FadeIn(vb.frame), FadeIn(vb.title), run_time=0.5)
            vo.wait_until("create two folders in the console")
            self.play(FadeIn(cf[0], shift=RIGHT * 0.2), FadeIn(r174), run_time=0.5)
            vo.wait_until("DVC store and images")
            self.play(FadeIn(vb.drawers["dvc_store/"], shift=DOWN * 0.15), run_time=0.4)
            self.play(FadeIn(cf[1], shift=RIGHT * 0.2), FadeIn(vb.drawers["images/"], shift=DOWN * 0.15),
                      run_time=0.5)
            self.play(Indicate(vb.title, color=CLOUD, scale_factor=1.06), run_time=0.6)
            vo.wait_until("A small gap")
            con = VGroup(win2, ill2, b1, either, *cf, r174, vb)
            self.play(FadeOut(con), run_time=0.5)
            self.remove(con, *con)
            self.play(FadeIn(c338, shift=DOWN * 0.15), FadeIn(ert), run_time=0.6)
            flash_tag(self, ert, INK)
            vo.wait_until("yet later it says to add more")
            self.play(Indicate(c338.body[0], color=INK, scale_factor=1.04), FadeIn(cap, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("So upload Image 1 through Image 4")
            self.play(FadeIn(vb2, shift=LEFT * 0.15), track(tr, 3, extra="row"), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in tiles], lag_ratio=0.15), FadeIn(ill3),
                      run_time=0.8)
            dst = vb2.drawers["images/"].get_center()
            self.play(LaggedStart(*[x.animate.move_to(dst).scale(0.4).set_opacity(0) for x in tiles],
                                  lag_ratio=0.15), run_time=1.4)
            self.remove(tiles, *tiles)
            self.play(Indicate(vb2.drawers["images/"].text, color=CLOUD, scale_factor=1.1),
                      FadeIn(cost, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Pause and do it")
            self.play(FadeIn(yt, shift=RIGHT * 0.15), run_time=0.4)
            flash_tag(self, yt, TURN)
            # the running map: the second BLUE bucket lights (held through the pause)
            gone = VGroup(c338, ert, cap, vb2, ill3, cost, yt)
            self.play(FadeOut(gone), FadeIn(m), run_time=0.7)
            self.remove(gone, *gone)
            self.play(m.light("bucket2"), run_time=0.8)
            self.play(each([m.bucket2.drawers["dvc_store/"].text, m.bucket2.drawers["images/"].text], CLOUD,
                           scale=1.1, lag=0.4), run_time=1.1)

        # ========================================================== 3. I1: cd data-versioning; edit docker-shell.sh
        tr_i = tracker("I", 1)
        assert readme(202, DV).startswith("export GCS_BUCKET_NAME=") and readme(204, DV).startswith("export GCP_ZONE=")
        p5 = code(SHELL, 5, 10, cuts={10: '"/secrets/'}).move_to([0, mid - 0.15, 0])
        n201 = note("README.md · lines 201–205: replace with your own").next_to(p5, UP, buff=0.12).align_to(p5, RIGHT)
        bars5 = [line_bar(p5.code, k, ERR) for k in (2, 3, 4)]
        c85 = capture("85")
        o85 = c85.at((2, 7))
        o85[-1] = cut(o85[-1], '"/secrets/')
        yt3 = turn_row()
        ed = None

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(m), run_time=0.4)
            self.remove(m)
            tr = swap_tracker(self, tr, tr_i)
            type_cmd(self, t, "cd data-versioning", type_time=0.35)
            cd_prompt(self, t, P_VERSIONING, run_time=0.4)
            self.play(FadeIn(p5, shift=UP * 0.15), FadeIn(n201), run_time=0.5)
            vo.wait_until("replace the bucket, project and zone")
            self.play(LaggedStart(*[FadeIn(b) for b in bars5], lag_ratio=0.3), run_time=0.8)
            self.play(Indicate(n201, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Only the bucket name is ever used")
            self.play(FadeOut(VGroup(p5, n201, *bars5)), run_time=0.35)
            self.remove(p5, n201, *bars5)
            resize(self, t, 11, run_time=0.5)
            ed = on_bar(t, editor_row())
            self.play(FadeIn(ed, shift=LEFT * 0.1), run_time=0.3)
            type_cmd(self, t, c85.cmd, type_time=1.4, soft=True)
            r85 = out(self, t, o85, run_time=0.5)
            self.play(*[r85[k].animate.set_color(PASS) for k in (2, 3, 4)], run_time=0.4)
            unused = VGroup(grey_chip("passed in · read by nothing"), erratum_tag()).arrange(RIGHT, buff=0.12)
            ymid = (r85[3].strut.get_center()[1] + r85[4].strut.get_center()[1]) / 2
            xr = max(substring(r, r.text).get_right()[0] for r in (r85[3], r85[4]))
            unused.move_to([min(xr + 0.4, 6.5 - unused.width) + unused.width / 2, ymid, 0])
            self.play(FadeIn(unused, shift=LEFT * 0.15), run_time=0.6)
            self.play(Indicate(substring(r85[2], BUCKET), color=PASS, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Pause and edit it")
            beside(yt3, r85[2], buff=0.5)
            self.play(FadeIn(yt3, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt3, TURN)

        # ========================================================== 4. the entrypoint's four stages
        c215 = readme_card((215, 230), "The project includes a file named docker-entrypoint.sh.\n"
                                       "For this container, it:\n"
                                       "· Mounts your GCS bucket inside the container.\n"
                                       "· Connects the bucket’s images folder to: /app/cheese_dataset",
                           size=22, repo=DV)
        assert "Mounts your GCS bucket inside the container." in readme(223, DV)
        c215.move_to([0, 1.2, 0])
        fm = FuseMount()
        # the entrypoint strip under V4: lines 8 (cut), 10 (whole, two rows) and 13
        pitch = line_pitch(20)
        x_num, x_txt, y0 = -6.1, -5.5, -1.82
        l8 = mono_line(cut(excerpt(ENTRY, 8, 8), "activate-service-account"), 20, S.GREY)
        r10 = source_rows(ENTRY, 10, size=20, width=69, color=S.GREY)
        l10a, l10b = r10.rows
        l13 = mono_line(excerpt(ENTRY, 13, 13), 20, S.GREY)
        rows = [l8, l10a, l10b, l13]
        for i, r in enumerate(rows):
            r.shift(np.array([x_txt, y0 - i * pitch, 0]) - r.strut.get_corner(UL))
        nums = VGroup()
        for n, r in ((8, l8), (10, l10a), (13, l13)):
            nums.add(mono(str(n), 20, S.GREY_DARK).move_to([x_num, r.strut.get_center()[1], 0]))
        head = VGroup(mono("starter · docker-entrypoint.sh", 20, S.GREY)).move_to(
            [6.1, l8.strut.get_center()[1], 0], aligned_edge=RIGHT)
        sframe = RoundedRectangle(width=12.7, height=4 * pitch + 0.3, corner_radius=0.12, stroke_color=S.GREY_DARK,
                                  stroke_width=2).set_fill(TERM_BG, 1)
        sframe.move_to([0, y0 - 2 * pitch, 0])
        strip = VGroup(sframe, nums, head, *rows)
        key_span = substring(l10a, "--key-file=$GOOGLE_APPLICATION_CREDENTIALS")
        sn = fm.side_note()

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(t, ed, yt3, unused)
            self.play(FadeOut(gone), FadeIn(c215, shift=DOWN * 0.15), run_time=0.6)
            self.remove(gone, t, *t.lines)
            vo.wait_until("The entrypoint runs the four stages")
            self.play(Indicate(c215.body[2], color=INK, scale_factor=1.03), run_time=0.6)
            self.play(FadeOut(c215, shift=UP * 0.15), FadeIn(fm), FadeIn(strip), run_time=0.7)
            self.remove(c215)
            self.play(LaggedStart(*[Indicate(g.text, color=INK, scale_factor=1.08) for g in fm.stages], lag_ratio=0.2),
                      run_time=1.0)
            vo.wait_until("Authenticate with the key")
            self.play(fm.stage(0), l8.animate.set_color(INK), l10a.animate.set_color(INK), run_time=0.5)
            k = fm.key[0].copy()
            self.play(k.animate.move_to(key_span.get_top() + UP * 0.3), run_time=0.7)
            self.play(FadeOut(k), key_span.animate.set_color(KEY), run_time=0.3)
            self.play(FadeIn(sn, shift=RIGHT * 0.1), l8.animate.set_color(S.GREY), run_time=0.5)
            vo.wait_until("Mount the whole bucket")
            self.play(fm.stage(1), FadeOut(sn), run_time=0.5)
            self.remove(sn)
            self.play(fm.mount(), substring(l10a, "gcsfuse").animate.set_color(TOOL),
                      substring(l10a, "$GCS_BUCKET_NAME").animate.set_color(CLOUD),
                      l10b.animate.set_color(ROUTE), run_time=0.9)
            vo.wait_until("with gcsfuse")
            self.play(each([fm.bucket.drawers["images/"], fm.bucket.drawers["dvc_store/"]], CLOUD, scale=1.06),
                      run_time=0.8)
            vo.wait_until("Bind its images folder")
            self.play(fm.stage(2), l13.animate.set_color(INK), run_time=0.5)
            self.play(fm.bind_on(), substring(l13, "/mnt/gcs_data/images").animate.set_color(ROUTE),
                      substring(l13, "/app/cheese_dataset").animate.set_color(ROUTE), run_time=0.9)
            vo.wait_until("cheese dataset")
            self.play(Indicate(fm.app.text, color=ROUTE, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Then use the data")
            self.play(fm.stage(3), fm.use(), run_time=0.6)
            vo.wait_until("while each file is fetched")
            got = fm.fetch(self)

        # ========================================================== 5. slide 34's chips; the trap
        mc = mount_chips()
        mc.move_to([0, 0.95, 0])
        target = VGroup(l10a, l10b).copy()
        target.move_to([0, 2.2, 0])
        hy = grey_chip("two hyphens, full variable name")
        imp = VGroup(mc.implicit, label("not passed here", 22, ERR)).arrange(RIGHT, buff=0.25)
        imp.move_to([-6.4 + imp.width / 2, -0.2, 0])
        hy.move_to([6.4 - hy.width / 2, -0.2, 0])
        marker = object_row("images/", "", 20)
        marker_note = note("empty object · made by Create folder")
        rows5 = [object_row(p, r, 20) for p, r in OBJECTS]
        ol5 = object_list([marker, *rows5], "the bucket's objects", 6.7)
        ol5.move_to([-2.95, -1.85, 0])
        marker_note.next_to(marker, RIGHT, buff=0.4)
        glow = hl_bar(marker, ROUTE, 0.3, buff=0.08)
        mnt = drawer("/mnt/gcs_data/", ROUTE, 22, glyph=False)
        sub = drawer("images/", ROUTE, 22)
        mv = VGroup(mnt, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        sub.shift(RIGHT * 0.5)
        mv_head = label("what gcsfuse shows", 20, S.GREY)
        mview = VGroup(mv_head, mv).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -1.6, 0])
        notes5 = VGroup(note("slides: disks → here: a bucket"),
                        note("slide 33: no local copy → DVC keeps one in .dvc/cache (scene 13)"))
        notes5.arrange(RIGHT, buff=0.6).move_to([0, -3.3, 0])

        with self.voiceover(SAY[5]) as vo:
            keep = VGroup(l10a, l10b)
            gone = VGroup(fm, sframe, nums, head, l8, l13, got)
            self.play(FadeOut(gone), *[FadeOut(x) for x in (fm.gcsfuse, fm.gcsfuse_label, fm.bind, fm.bind_label,
                                                              fm.dvc)], run_time=0.6)
            self.remove(gone, *gone, fm.gcsfuse, fm.gcsfuse_label, fm.bind, fm.bind_label, fm.dvc)
            self.play(Transform(keep, target), run_time=0.7)
            vo.wait_until("The lecture takes the mount line apart")
            self.play(Indicate(l10a, color=INK, scale_factor=1.02), run_time=0.6)
            spans = [substring(l10a, "gcsfuse"), substring(l10a, "--key-file=$GOOGLE_APPLICATION_CREDENTIALS"),
                     substring(l10a, "$GCS_BUCKET_NAME"), substring(l10b, "/mnt/gcs_data")]
            cols = (TOOL, KEY, CLOUD, ROUTE)
            uls = [under(s, c, stroke=3) for s, c in zip(spans, cols)]
            for i, anchor in enumerate(("tool, key file", "key file, bucket", "bucket, mount point", "mount point")):
                vo.wait_until(anchor)
                self.play(FadeIn(mc.chips[i], shift=UP * 0.15), Create(uls[i]), run_time=0.4)
                if i == 1:
                    self.play(FadeIn(hy, shift=LEFT * 0.1), run_time=0.3)
            vo.wait_until("One flag is not passed")
            self.play(FadeIn(imp[0], shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(imp[1], shift=RIGHT * 0.1), FadeIn(notes5, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("so gcsfuse only shows folders the console made")
            self.play(FadeIn(ol5.frame), FadeIn(ol5.title), *[FadeIn(r) for r in rows5], run_time=0.6)
            self.play(FadeIn(mv_head), FadeIn(mnt, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("which leave a marker object")
            self.play(FadeIn(marker, shift=RIGHT * 0.15), FadeIn(glow), FadeIn(marker_note), run_time=0.6)
            self.play(TransformFromCopy(marker.prefix, sub.text), FadeIn(sub.box), FadeIn(sub.glyph),
                      rows5[2].animate.set_color(S.GREY_DARK), run_time=0.9)
            vo.wait_until("That was the trap")
            self.play(Indicate(sub.text, color=ROUTE, scale_factor=1.12), run_time=0.8)

        # ========================================================== 6. two bind mounts, two layers
        ml = MountLayers()
        ml.shift(DOWN * 0.45)

        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(keep, *uls, *mc.chips, hy, imp, ol5, marker, glow, marker_note, mview, notes5)
            self.play(FadeOut(gone), run_time=0.6)
            self.remove(gone, *gone.get_family())
            self.play(FadeIn(ml, scale=1.25), run_time=0.9)
            vo.wait_until("Note the two bind mounts")
            self.play(ml.light_fuse(), run_time=0.8)
            vo.wait_until("dash v joins")
            self.play(ml.light_v(), run_time=0.8)
            self.play(Indicate(ml.app.frame, color=IMAGE, scale_factor=1.03),
                      Indicate(ml.host.frame, color=LAPTOP, scale_factor=1.03), run_time=0.7)
            vo.wait_until("and the inner one")
            self.play(ml.light_inner(), run_time=0.8)
            self.play(ml.dark(), Indicate(ml.app_data.text, color=ROUTE, scale_factor=1.08), run_time=0.7)

        # ========================================================== 7. docker run's flags
        p17 = code(SHELL, 17, 27, font_size=20).move_to([0, 0.35, 0])
        b_sys = [line_bar(p17.code, k, SYSTEM, 0.22) for k in (1, 2, 3)]
        b21 = line_bar(p17.code, 4, S.GREY, 0.2)
        b22 = line_bar(p17.code, 5, KEY, 0.2)
        b23 = line_bar(p17.code, 6, TURN, 0.22)
        gchip = chip(GIT_CHIP, TURN, size=20).next_to(p17, DOWN, buff=0.3)

        with self.voiceover(SAY[7]) as vo:
            mlx = VGroup(ml, ml.v_pipe, ml.v_label, ml.inner, ml.inner_label, ml.fuse)
            self.play(FadeOut(mlx), run_time=0.5)
            self.remove(mlx, *mlx.get_family())
            self.play(FadeIn(p17, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Mounting needs the fuse device")
            self.play(FadeIn(b_sys[2]), code_span(p17.code, 3, "/dev/fuse").animate.set_color(SYSTEM), run_time=0.5)
            vo.wait_until("hence the privileged flag")
            self.play(FadeIn(b_sys[0]), FadeIn(b_sys[1]), code_span(p17.code, 1, "--privileged").animate.set_color(SYSTEM),
                      code_span(p17.code, 2, "SYS_ADMIN").animate.set_color(SYSTEM), run_time=0.6)
            vo.wait_until("The script also mounts your repo")
            self.play(FadeIn(b21), run_time=0.4)
            vo.wait_until("secrets and git config")
            self.play(FadeIn(b22), run_time=0.4)
            self.play(FadeIn(b23), run_time=0.4)
            vo.wait_until("Set up git before the first run")
            self.play(FadeIn(gchip, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(code_span(p17.code, 6, "~/.gitconfig"), color=TURN, scale_factor=1.1), run_time=0.7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
