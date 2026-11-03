"""S12 · Files named by their fingerprint — tracker J1 → J3; `lref("20, 23, 25")`.

Beats (script.md, ## S12; one voiceover block each):
0. TRACKER J1. Re-entry (90: 27–28, …, 41–42) + chips 'same entrypoint errors as before' and 'our
   capture: a fresh container for each step'; `dvc init` → 90:46 RED; `ls -A` (extra) → 50–51, .dvc
   and .dvcignore RED, chip 'half-made'. ORANGE picture: 'root' inside the container, 'student' on
   the repo on disk, git's ownership check between them RED.
1. TRACKER J1 · extra · Linux: exit (90:52–53); on the host 91 (rm + ls -A), 92 (safe.directory,
   lines 5–6 GREEN) + the starter docker-shell.sh:23 arrow ~/.gitconfig → /etc/gitconfig. TRACKER
   J1: re-entry (93), `dvc init` → 93:46, 48, 52 + chip 'opt out: dvc config core.analytics false'; ▶.
2. Route T: the `~/today` strip (145): dvc init → 47 RED, remote add → 49–50 (50 RED), cat
   .dvc/config (extra) → 52–55, 55 RED + dashed chip 'the class bucket'. The strip closes.
3. TRACKER J2: README card (line 279); remote add (93:63) → 64; cat .dvc/config (extra) → 66–69
   GREEN; V7: the PINK remote link DVC house → dvc_store/; ▶.
4. V5 as a prediction: four tiles hashed (09b's md5s), filed on 5b/ ba/ 91/ 5b/; the manifest hashed
   to '????????….dir' on '??/'; only that string flies into the blank pointer card; the git box.
5. TRACKER J3: dvc add (93:70) → 71, 73, 75; the machine runs on nothing (d7/, RED); cat → 81–86,
   82–84 RED; S11's YELLOW rule card flashes.
6. TRACKER J3 · extra · stand-in: exit (93:107–108); MountLayers (inner bind absent, -v lit); 94's
   copy → 2–8; re-entry (95); ls (extra) → 46; dvc add → 48, 50, 52; cat → 58–63 (59–61 YELLOW);
   the pointer card's fields fill, ??/ becomes 89/; ▶.
7. TRACKER J3 · extra: find .dvc/cache (95:64) → 65–70, each line lights its aisle; 70 GREY, chip
   'the empty version'.
8. TRACKER J3 · extra: the second terminal (120: 2–7) + the class-clone chip; the class card beside
   ours, both md5 lines ring PINK; S01's PINK line hovers over both. The strip closes.
9. The manifest card alone, Image_2.jpg highlighted. PONDER 8 s.
10. The answer: the relpath rewrites to brie_2.jpg, the .dir rerolls (????????….dir), the ba/ blob,
    size and nfiles stay GREEN; S01's Monday/Friday cards return small with manifests (one md5 row
    differs, no values); misconception card. Fade out.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S12"]
DV = "data-versioning"
STARTER_SHELL = "data-versioning@data-versioning-ac215/docker-shell.sh"
TS = 20                       # terminal size in this scene (72 characters a row)
ROUTE_T = "if you cloned main · rewind to scene 9 · recreate your empty GitHub repo first"
PONDER_Q = "Rename Image_2.jpg → brie_2.jpg,\ndvc add again. Which changes: the photo's\nmd5, the .dir md5, size, nfiles?"
MYTH = ("DVC stores whole files, not diffs", "one changed pixel = a new md5, a new blob")


def words(*parts, size: float = 20, color=INK) -> VGroup:
    """One row of label/mono pieces: plain strings are label font, ('x', 'mono') pieces mono."""
    ms = [mono(p[0], size, color) if isinstance(p, tuple) else label(p, size, color) for p in parts]
    return VGroup(*ms).arrange(RIGHT, buff=0.12)


def above(mob, t, buff: float = 0.18, side=RIGHT):
    """Place mob just above terminal t's top edge, flush with its left or right edge."""
    return mob.next_to(t.box, UP, buff=buff).align_to(t.box, side)


def edge(s: str, n: int = 72) -> list[str]:
    """A progress-bar line soft-wrapped at the row edge, as a real terminal shows it (text unchanged)."""
    return [s[i:i + n] for i in range(0, len(s), n)]


def band_mid(t) -> float:
    return (PIC_TOP + t.box.get_top()[1] + 0.12) / 2


def ownership_picture() -> VGroup:
    """The ORANGE ownership picture: your repo on disk ('owner: student'), the TEAL container ('you
    are root'), git's ownership check between them (RED cross). .disk .box .check .cross .who"""
    disk_fr = RoundedRectangle(width=4.2, height=2.3, corner_radius=0.16, stroke_color=LAPTOP,
                               stroke_width=2.5).set_fill(LAPTOP, 0.04).move_to([-4.2, 0.75, 0])
    disk_t = label("your laptop · on disk", 20, LAPTOP).move_to(disk_fr.get_corner(UL) + np.array([0.2, -0.28, 0]),
                                                                 aligned_edge=LEFT)
    repo = drawer("data-versioning/", LAPTOP).move_to(disk_fr.get_center() + DOWN * 0.05)
    own = grey_chip("owner: student", color=ROOT).next_to(repo, DOWN, buff=0.22)
    box = outline_box(4.2, 2.3, IMAGE, solid=True, fill_opacity=0.05).move_to([4.2, 0.75, 0])
    box_t = mono(CONTAINERS["dvc"], 20, IMAGE).move_to(box.get_corner(UL) + np.array([0.2, -0.28, 0]),
                                                      aligned_edge=LEFT)
    app = drawer("/app", IMAGE).move_to(box.get_center() + DOWN * 0.05)
    who = grey_chip("you: root", color=ROOT).next_to(app, DOWN, buff=0.22)
    git = tool_chip("git").move_to([0, 1.15, 0])
    chk = label("ownership check", 20, ROOT).next_to(git, DOWN, buff=0.15)
    a = Arrow(box.get_left() + DOWN * 0.45, disk_fr.get_right() + DOWN * 0.45, buff=0.1, color=ERR, stroke_width=4,
              tip_length=0.2)
    x = cross_mark(0.45, ERR).move_to([0, a.get_center()[1] - 0.05, 0])
    g = VGroup(disk_fr, disk_t, repo, own, box, box_t, app, who, git, chk, a, x)
    g.disk, g.own, g.box, g.who, g.check, g.arrow, g.cross = VGroup(disk_fr, disk_t, repo), own, \
        VGroup(box, box_t, app), who, VGroup(git, chk), a, x
    return g


def day_card(day: str, odd: int | None = None) -> VGroup:
    """S01's folder card, small, with a manifest: names and PINK md5 bars (no values). `odd`: the
    index of the row whose bar differs (drawn hollow + '≠'). .rows .bars .odd"""
    head = VGroup(mono("cheese_dataset", 20, INK), label(f"· {day}", 20, S.GREY)).arrange(RIGHT, buff=0.12,
                                                                                         aligned_edge=DOWN)
    rows, bars = VGroup(), VGroup()
    for i, n in enumerate(IMAGES[:4]):
        b = RoundedRectangle(width=1.1, height=0.2, corner_radius=0.06, stroke_color=HASH, stroke_width=2)
        b.set_fill(HASH, 0.15 if i == odd else 0.7)
        r = VGroup(b, mono(n, 20, INK)).arrange(RIGHT, buff=0.25)
        rows.add(r)
        bars.add(b)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    fr = RoundedRectangle(width=body.width + 0.5, height=body.height + 0.4, corner_radius=0.14,
                          stroke_color=LAPTOP, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.rows, g.bars = rows, bars
    return g


class Fingerprints(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S12"] == 11, len(SAY)
        c90, c91, c92, c93 = capture("90"), capture("91"), capture("92"), capture("93")
        c94, c95, c120, c145 = capture("94"), capture("95"), capture("120"), capture("145")

        # ========================================================== 0. J1: dvc init stops on Linux
        ref = lref("20, 23, 25")
        tr = tracker("J", 1)
        t = term(P_VERSIONING, rows=9, size=TS)
        re_chip = reentry_chip()
        fresh = container_note()
        xt0 = on_bar(t, extra_row())
        pic = ownership_picture()
        assert c90.istep(45)[1] == readme(269, DV) == "dvc init"

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(t), run_time=0.6)
            reenter(self, t, "90", type_time=0.4)
            above(re_chip, t, side=RIGHT)
            above(fresh, t, side=LEFT)
            self.play(FadeIn(re_chip, shift=UP * 0.1), FadeIn(fresh, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("run dvc init")
            istep(self, t, c90.line(45), type_time=0.3)
            vo.wait_until("On Linux it may stop")
            out(self, t, [(c90.line(46), ERR)], wrap=True, run_time=0.4)
            vo.wait_until("the repository path is not owned")
            self.play(Indicate(substring(t.find("owned by current user"), "owned by current user"), color=ERR, scale_factor=1.12),
                      run_time=0.7)
            self.play(FadeIn(xt0, shift=LEFT * 0.1), track(tr, 1, extra=True), run_time=0.4)
            istep(self, t, c90.line(49), type_time=0.2)
            out(self, t, c90.at((50, 51)), wrap=True, run_time=0.4)
            r50, r51 = t.find("Dockerfile  cheese"), t.find(".dvcignore")
            half = row_tag("half-made", ERR).next_to(xt0, LEFT, buff=0.2)
            self.play(substring(r50, ".dvc").animate.set_color(ERR), substring(r51, ".dvcignore").animate.set_color(ERR),
                      FadeIn(half, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("You are root inside")
            self.play(FadeOut(VGroup(re_chip, fresh, xt0, half)), run_time=0.3)
            self.remove(re_chip, fresh, xt0, half)
            resize(self, t, 3, keep=3, run_time=0.6)
            on_bar(t, half)
            self.add(half)
            self.play(FadeIn(pic.box), FadeIn(pic.who, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("the repo is yours on disk")
            self.play(FadeIn(pic.disk), FadeIn(pic.own, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("so git refuses")
            self.play(FadeIn(pic.check, shift=DOWN * 0.1), GrowArrow(pic.arrow), run_time=0.6)
            self.play(Create(pic.cross), run_time=0.4)
            vo.wait_until("leaving a half-made folder")
            flash_tag(self, half, ERR)

        # ========================================================== 1. the fix (extra · Linux), then J1 works
        p23 = code(STARTER_SHELL, 23)
        g_home = chip("~/.gitconfig", LAPTOP, size=20, font=MONO)
        g_etc = chip("/etc/gitconfig", IMAGE, size=20, font=MONO)
        cfg = VGroup(g_home, g_etc).arrange(RIGHT, buff=1.4)
        a_cfg = Arrow(g_home.get_right(), g_etc.get_left(), buff=0.12, color=S.GREY, stroke_width=3, tip_length=0.18)
        host_n = note("on the host").next_to(g_home, DOWN, buff=0.1)
        box_n = note("inside the container").next_to(g_etc, DOWN, buff=0.1)
        cfg_g = VGroup(cfg, a_cfg, host_n, box_n)
        opt = grey_chip("opt out: dvc config core.analytics false", mono_font=False)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(pic), run_time=0.4)
            self.remove(pic)
            self.play(FadeOut(half), run_time=0.3)
            self.remove(half)
            resize(self, t, 9, run_time=0.5)
            xt1 = on_bar(t, extra_row("Linux"))
            self.play(FadeIn(xt1, shift=LEFT * 0.1), track(tr, 1, extra="Linux"), run_time=0.4)
            istep(self, t, c90.line(52), type_time=0.2)
            out(self, t, c90.at(53), run_time=0.2)
            t.set_prompt(P_VERSIONING)
            vo.wait_until("remove the half-made files")
            type_cmd(self, t, c91.cmd, type_time=0.5)
            out(self, t, c91.at((2, 10)), run_time=0.6)
            vo.wait_until("Then mark slash app")
            type_cmd(self, t, c92.cmd, type_time=0.6)
            out(self, t, c92.at((2, 4)) + [(x, PASS) for x in c92.at((5, 6))], run_time=0.5)
            top = t.box.get_top()[1]
            mid = (PIC_TOP + top) / 2
            p23.move_to([-6.45 + p23.width / 2, mid, 0])
            cfg_g.move_to([6.4 - cfg_g.width / 2, mid, 0])
            self.play(FadeIn(p23, shift=DOWN * 0.1), run_time=0.4)
            self.play(FadeIn(g_home), FadeIn(host_n), run_time=0.3)
            self.play(GrowArrow(a_cfg), FadeIn(g_etc), FadeIn(box_n), run_time=0.5)
            self.play(Indicate(code_span(p23.code, 0, "~/.gitconfig:/etc/gitconfig"), color=TURN, scale_factor=1.06),
                      run_time=0.6)
            vo.wait_until("Start the container again")
            self.play(FadeOut(VGroup(p23, cfg_g, xt1)), track(tr, 1), run_time=0.4)
            self.remove(p23, cfg_g, xt1)
            reenter(self, t, "93", type_time=0.3)
            vo.wait_until("and dvc init works")
            ln46 = istep(self, t, c93.line(45), type_time=0.3)
            out(self, t, [(c93.line(46), PASS), c93.line(48), c93.line(52)], run_time=0.4)
            above(opt, t, side=RIGHT)
            self.play(FadeIn(opt, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Pause and run it")
            yt1 = beside(turn_row(), ln46)
            pin(self, ln46, yt1)
            flash_tag(self, yt1, TURN)

        # ========================================================== 2. Route T, kindly: main stops here
        s2 = term("root@15ddd4810362:/app#", 8, T_TODAY, size=TS)
        rt = grey_chip(ROUTE_T)
        above(rt, s2, side=LEFT)
        xt2 = on_bar(s2, extra_row())
        cls = dashed_chip("the class bucket")

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(t, opt)), run_time=0.4)
            self.remove(t, *t.lines, opt)
            self.play(FadeIn(s2, shift=UP * 0.2), FadeIn(rt, shift=UP * 0.1), run_time=0.5)
            istep(self, s2, c145.line(46), type_time=0.3)
            vo.wait_until("DVC is already set up")
            out(self, s2, [(c145.line(47), ERR)], wrap=True, run_time=0.3)
            vo.wait_until("the remote is refused")
            istep(self, s2, c145.line(48), type_time=0.5)
            out(self, s2, [c145.line(49), (c145.line(50), ERR)], wrap=True, run_time=0.4)
            vo.wait_until("and the config points")
            self.play(FadeIn(xt2, shift=LEFT * 0.1), run_time=0.3)
            istep(self, s2, c145.line(51), type_time=0.2)
            out(self, s2, c145.at((52, 54)) + [(c145.line(55), ERR)], run_time=0.4)
            r55 = s2.find(CLASS_BUCKET)
            beside(cls, r55, buff=0.4)
            pin(self, r55, cls)
            self.play(Indicate(substring(r55, CLASS_BUCKET), color=ERR, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Start from the starter")
            flash_tag(self, rt, INK)
            self.play(FadeOut(VGroup(s2, rt, xt2)), run_time=0.5)
            self.remove(s2, *s2.lines, rt, xt2)

        # ========================================================== 3. J2: dvc remote add
        t = term("root@d5bf95465b66:/app#", rows=6, size=TS)
        c279 = readme_card(279, mono(readme(279, DV), 20, INK), repo=DV)
        xt3 = on_bar(t, extra_row())
        m = PipelineMap.at("S12")
        p63, cmd63 = c93.istep(63)
        assert cmd63 == readme(279, DV).replace("YOUR_BUCKET_NAME", BUCKET)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(t), track(tr, 2), run_time=0.5)
            bare_prompt(self, t)
            c279.move_to([0, band_mid(t), 0])
            self.play(FadeIn(c279, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("point DVC at the DVC store folder")
            self.play(Indicate(c279.body, color=TURN, scale_factor=1.05), run_time=0.6)
            ln63 = istep(self, t, c93.line(63), type_time=0.6)
            out(self, t, c93.at(64), run_time=0.3)
            vo.wait_until("as its default remote")
            self.play(FadeIn(xt3, shift=LEFT * 0.1), track(tr, 2, extra=True), run_time=0.3)
            istep(self, t, c93.line(65), type_time=0.2)
            out(self, t, [(x, PASS) for x in c93.at((66, 69))], run_time=0.4)
            self.play(FadeOut(VGroup(c279, xt3)), track(tr, 2), run_time=0.4)
            self.remove(c279, xt3)
            resize(self, t, 3, keep=3, run_time=0.5)
            self.play(FadeIn(m), run_time=0.6)
            self.play(m.light("remote"), run_time=0.9)
            self.play(Indicate(m.bucket2.drawers["dvc_store/"].text, color=CLOUD, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Pause and add it")
            yt3 = on_bar(t, turn_row())
            self.play(FadeIn(yt3, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt3, TURN)

        # ========================================================== 4. V5 as a prediction, before any dvc add output
        hs = HashShelf()
        tiles = [hs.tiles[n] for n in IMAGES[:4]]
        fp_chip = grey_chip("fingerprint · slide 25")
        md5_chip = chip("md5 · DVC", HASH, size=20)
        chips4 = VGroup(fp_chip, md5_chip).arrange(DOWN, buff=0.12).next_to(hs.machine, DOWN, buff=0.3)
        path_chip = grey_chip("a path, not a meaning")
        dir_chip = grey_chip("the .dir ending marks a folder's list")

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(m, yt3)), run_time=0.5)
            self.remove(m, *m.get_family(), yt3)
            self.play(FadeIn(hs), run_time=0.6)
            self.play(FadeIn(chips4, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("It fingerprints each photo")
            s1 = hs.hash_photo(self, "Image_1.jpg")
            p2 = row_tag("part 2", HASH).next_to(s1, RIGHT, buff=0.2)
            self.play(FadeIn(p2, shift=LEFT * 0.1), run_time=0.3)
            flash_tag(self, p2, HASH)
            vo.wait_until("It files a copy in its cache")
            self.play(FadeOut(p2), run_time=0.2)
            self.remove(p2)
            hs.hash_photo(self, "Image_2.jpg")
            hs.hash_photo(self, "Image_3.jpg")
            vo.wait_until("on a shelf named by the first 2 characters")
            hs.hash_photo(self, "Image_4.jpg")
            r5b = hs.rows["5b"]
            path_chip.move_to([hs.rack.frame.get_right()[0] - path_chip.width / 2 - 0.15,
                               hs.rack.frame.get_bottom()[1] + 0.35, 0])
            self.play(Indicate(r5b.label, color=HASH, scale_factor=1.3), FadeIn(path_chip, shift=UP * 0.1),
                      run_time=0.7)
            vo.wait_until("Then it fingerprints a manifest")
            self.play(FadeOut(VGroup(*tiles)), FadeOut(path_chip), FadeOut(chips4), run_time=0.4)
            hs.remove(*tiles)
            self.remove(*tiles, path_chip, chips4)
            mf = hs.manifest()
            self.play(FadeIn(mf, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("the list of fingerprints and names")
            self.play(each(list(mf.rows), INK, scale=1.06, lag=0.2), run_time=1.0)
            pred = hs.hash_manifest(self, mf, predict=True)
            self.remove(*mf.get_family())
            dir_chip.move_to(chips4[0])
            self.play(FadeIn(dir_chip, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and writes that fingerprint into the pointer file")
            pc = hs.pointer(predict=True)
            md5f = pc.fields["md5"]
            md5f.set_opacity(0)
            self.play(FadeIn(pc, shift=RIGHT * 0.2), run_time=0.5)
            fly = pred.text.copy()
            self.play(fly.animate.move_to(md5f, aligned_edge=LEFT), run_time=0.9)
            md5f.set_opacity(1)
            self.remove(fly)
            self.add(pc)
            vo.wait_until("which stands in for the folder in git")
            gb = hs.git_box(pc)
            self.play(FadeOut(dir_chip), FadeIn(gb.box), run_time=0.5)
            self.remove(dir_chip)
            self.play(FadeIn(gb.text, shift=UP * 0.1), Indicate(pc.head, color=POINTER, scale_factor=1.08), run_time=0.6)

        # ========================================================== 5. J3: the second trap, an empty version
        empty_chip = VGroup(note("the same machine,", INK), note("fed nothing", INK)).arrange(DOWN, buff=0.06)
        rule = card([words(("ls cheese_dataset", "mono"), "before", ("dvc add", "mono"), size=22)], TURN, size=22,
                    head="rule for today")

        def shelf_parts():
            rows = [r for r in hs.rows.values() if r in self.mobjects or r.label in self.mobjects]
            slips = [s for v in hs.slips.values() for s in v]
            return [hs, *rows, *slips, pc, gb]

        with self.voiceover(SAY[5]) as vo:
            self.play(track(tr, 3), run_time=0.4)
            istep(self, t, c93.line(70), type_time=0.3)
            out(self, t, [*edge(c93.line(71)), c93.line(73), c93.line(75)], run_time=0.5)
            vo.wait_until("the mount failed")
            empty_chip.next_to(hs.machine, DOWN, buff=0.25).shift(RIGHT * 0.15)
            self.play(FadeIn(empty_chip, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("so the folder is empty")
            e = hs.empty_run(self)
            vo.wait_until("and dvc add happily makes a version")
            parts = shelf_parts()
            self.play(FadeOut(Group(*parts, empty_chip)), run_time=0.5)
            self.remove(*parts, empty_chip)
            resize(self, t, 8, run_time=0.5)
            istep(self, t, c93.line(80), type_time=0.2)
            out(self, t, [c93.line(81)] + [(x, ERR) for x in c93.at((82, 84))] + c93.at((85, 86)), run_time=0.5)
            vo.wait_until("with zero files")
            self.play(each([substring(t.find("nfiles: 0"), "0"), substring(t.find("size: 0"), "0")], ERR, scale=1.3),
                      run_time=0.7)
            rule.move_to([0, band_mid(t), 0])
            self.play(FadeIn(rule, scale=1.1), run_time=0.5)
            self.play(Indicate(rule.body, color=TURN, scale_factor=1.06), run_time=0.6)

        # ========================================================== 6. the stand-in photos, dvc add again
        ml = MountLayers()
        gone_bind = ml.absent()
        tiles6 = ml.photos(4)
        where = note("where your bucket's images/ would appear").next_to(ml.laptop, DOWN, buff=0.1) \
            .align_to(ml.box, RIGHT)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(rule), run_time=0.3)
            self.remove(rule)
            istep(self, t, c93.line(107), type_time=0.15)
            out(self, t, c93.at(108), run_time=0.15)
            t.set_prompt(P_VERSIONING)
            resize(self, t, 3, keep=1, run_time=0.4)
            xt6 = on_bar(t, extra_row("stand-in"))
            self.play(FadeIn(ml), FadeIn(ml.v_pipe), FadeIn(ml.v_label), Create(gone_bind), run_time=0.6)
            self.play(FadeIn(xt6, shift=LEFT * 0.1), track(tr, 3, extra="stand-in"), run_time=0.4)
            type_cmd(self, t, c94.cmd, type_time=0.8)
            vo.wait_until("our stand-in copies four photos")
            out(self, t, c94.at((2, 8)), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.15) for x in tiles6], lag_ratio=0.2),
                      FadeIn(where, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("which the container sees through the repo mount")
            self.play(Indicate(ml.v_label, color=INK, scale_factor=1.04), ml.v_pipe.animate.set_stroke(width=8),
                      run_time=0.7)
            vo.wait_until("and we add again")
            g6 = VGroup(ml, ml.v_pipe, ml.v_label, gone_bind, tiles6, where, xt6)
            self.play(FadeOut(g6), track(tr, 3), run_time=0.4)
            self.remove(g6, *g6)
            resize(self, t, 10, run_time=0.5)
            reenter(self, t, "95", type_time=0.3)
            xt6b = on_bar(t, extra_row())
            self.play(FadeIn(xt6b, shift=LEFT * 0.1), track(tr, 3, extra=True), run_time=0.3)
            istep(self, t, c95.line(45), type_time=0.2)
            out(self, t, c95.at(46), run_time=0.2)
            self.play(FadeOut(xt6b), track(tr, 3), run_time=0.3)
            self.remove(xt6b)
            istep(self, t, c95.line(47), type_time=0.3)
            out(self, t, [*edge(c95.line(48)), c95.line(50), c95.line(52)], run_time=0.4)
            self.play(FadeIn(xt6b, shift=LEFT * 0.1), track(tr, 3, extra=True), run_time=0.3)
            istep(self, t, c95.line(57), type_time=0.2)
            out(self, t, [c95.line(58)] + [(x, TURN) for x in c95.at((59, 61))] + c95.at((62, 63)), run_time=0.4)
            vo.wait_until("Now the pointer file says 4 files")
            keep = [t.find("- md5: 89db"), t.find("size: 611101"), t.find("nfiles: 4")]
            self.play(FadeOut(xt6b), track(tr, 3, extra="stand-in"), run_time=0.3)
            self.remove(xt6b)
            resize(self, t, 3, keep=keep, run_time=0.5)
            self.play(FadeIn(Group(*parts)), run_time=0.6)
            vo.wait_until("and one fingerprint for the folder")
            hs.confirm(self, pc)
            self.play(Indicate(pc.fields["nfiles"], color=INK, scale_factor=1.3), run_time=0.5)
            vo.wait_until("Pause and add yours")
            yt6 = on_bar(t, turn_row())
            self.play(FadeIn(yt6, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt6, TURN)

        # ========================================================== 7. the real cache listing
        xt7 = on_bar(t, extra_row())
        listing = c95.at((65, 70))
        the_empty = grey_chip("the empty version")

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(yt6), FadeIn(xt7, shift=LEFT * 0.1), track(tr, 3, extra=True), run_time=0.4)
            self.remove(yt6)
            istep(self, t, c95.line(64), type_time=0.3)
            vo.wait_until("The cache shows those shelves")
            for ln in listing[:-1]:
                out(self, t, [ln], run_time=0.25)
                a = ln.split("/md5/")[1][:2]
                self.play(Indicate(hs.rows[a].label, color=HASH, scale_factor=1.35), run_time=0.45)
            vo.wait_until("plus the empty version")
            out(self, t, [(listing[-1], S.GREY)], run_time=0.3)
            the_empty.move_to([hs.rack.frame.get_left()[0] - 0.12 - the_empty.width / 2, e.get_center()[1], 0])
            self.play(e.box.animate.set_stroke(S.GREY), e.text.animate.set_color(S.GREY),
                      hs.rows["d7"].label.animate.set_color(S.GREY), FadeIn(the_empty, shift=LEFT * 0.1), run_time=0.6)
            self.play(Indicate(the_empty.text, color=INK, scale_factor=1.08), run_time=0.5)

        # ========================================================== 8. one line pins 600 kB; the class tag
        s8 = term(P_LAPTOP_HOME, 10, T_SECOND, size=TS)
        clone = card([label("the class repo, cloned as class-data-versioning (extra):", 20, INK),
                      mono("git clone -q", 20, INK),
                      mono("  https://github.com/dlops-io/data-versioning", 20, INK),
                      mono("  class-data-versioning", 20, INK)], S.GREY, size=20, buff=0.08)
        xt8 = on_bar(s8, extra_row())
        cv20 = {k: c120.line(n).split(":", 1)[1].strip() for k, n in (("md5", 3), ("size", 4), ("nfiles", 5))}
        assert cv20 == V20, cv20
        ccard = pointer_card(short(cv20["md5"]), cv20["size"], cv20["nfiles"])
        hook = mono(HOOK_LINE, 26, HASH)
        o_lab = note("ours · 95:58–63")
        c_lab = note("class repo · dataset_v20 · 120:2–7")

        with self.voiceover(SAY[8]) as vo:
            vo.wait_until("So one line pins 600 kilobytes")
            self.play(Indicate(pc.lines[1], color=HASH, scale_factor=1.06), run_time=0.6)
            self.play(Indicate(pc.fields["size"], color=INK, scale_factor=1.3), run_time=0.5)
            vo.wait_until("it fingerprints the list of fingerprints")
            self.play(Indicate(pc.fields["md5"], color=HASH, scale_factor=1.15),
                      Indicate(hs.rows["89"].label, color=HASH, scale_factor=1.3), run_time=0.8)
            vo.wait_until("And the instructor's tag")
            gone = parts + [the_empty, t, xt7]
            self.play(FadeOut(Group(*gone)), run_time=0.5)
            self.remove(*gone, *t.lines)
            clone.move_to([0, band_mid(s8), 0])
            self.play(FadeIn(s8, shift=UP * 0.2), FadeIn(clone, shift=DOWN * 0.1), FadeIn(xt8), run_time=0.5)
            type_cmd(self, s8, c120.cmd, type_time=0.8)
            out(self, s8, c120.at((2, 7)), run_time=0.5)
            keep8 = [s8.find("- md5: 89db"), s8.find("size: 611101"), s8.find("nfiles: 4")]
            self.play(FadeOut(clone), FadeOut(xt8), run_time=0.3)
            self.remove(clone, xt8)
            resize(self, s8, 3, keep=keep8, run_time=0.5)
            xt8 = on_bar(s8, extra_row())
            pc.move_to([-3.3, -0.1, 0])
            self.play(FadeIn(pc, shift=RIGHT * 0.3), FadeIn(xt8), run_time=0.6)
            o_lab.next_to(pc, UP, buff=0.12).align_to(pc, LEFT)
            self.play(FadeIn(o_lab), run_time=0.3)
            ccard.move_to([3.3, -0.1, 0])
            c_lab.next_to(ccard, UP, buff=0.12).align_to(ccard, LEFT)
            self.play(FadeIn(ccard, shift=LEFT * 0.4), FadeIn(c_lab), run_time=0.6)
            vo.wait_until("holds the same fingerprint")
            g1, g2 = ring(pc.lines[1], HASH), ring(ccard.lines[1], HASH)
            self.play(Create(g1), Create(g2), run_time=0.6)
            vo.wait_until("character for character")
            hook.move_to([0, 2.35, 0])
            self.play(FadeIn(hook, shift=DOWN * 0.3), run_time=0.6)
            ul = Underline(hook, color=HASH, buff=0.08)
            self.play(Create(ul), run_time=0.6)
            self.play(FadeOut(VGroup(s8, xt8)), run_time=0.4)
            self.remove(s8, *s8.lines, xt8)

        # ========================================================== 9. Ponder 8
        mf2 = manifest_card(IMAGES[:4]).move_to([0, 0.4, 0])
        n2 = mf2.names["Image_2.jpg"]
        hb = hl_bar(n2, TURN, 0.3)

        with self.voiceover(SAY[9]) as vo:
            g8 = VGroup(pc, ccard, o_lab, c_lab, g1, g2, hook, ul)
            self.play(FadeOut(g8), run_time=0.5)
            self.remove(g8, *g8)
            self.play(FadeIn(mf2, scale=0.95), run_time=0.6)
            vo.wait_until("You give Image 2")
            self.play(FadeIn(hb), Indicate(n2, color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Which changes")
            self.play(Indicate(mf2.head, color=INK, scale_factor=1.05), run_time=0.6)
        pond = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 10. the answer; the reverse; whole files
        old_dir = slip(short(V20["md5"]), HASH)
        new_dir = slip("????????….dir", HASH)
        same_blob = VGroup(slip("ba/" + MD5["Image_2.jpg"][2:8] + "…", PASS), label("same blob", 20, PASS))
        same_size = mono("size: " + V20["size"], 20, PASS)
        same_n = mono("nfiles: " + V20["nfiles"], 20, PASS)
        mon, fri = day_card("Monday"), day_card("Friday", odd=2)
        VGroup(mon, fri).arrange(RIGHT, buff=1.2).move_to([0, -2.3, 0])
        neq = label("≠", 30, TURN).next_to(fri.bars[2], LEFT, buff=0.08)
        rg = ring(fri.bars[2], TURN, buff=0.06)
        myth = card(list(MYTH), S.GREY, size=22)
        myth.move_to([0, 1.2, 0])

        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(pond), mf2.animate.move_to([-3.4, 0.9, 0]), hb.animate.shift(LEFT * 3.4 + UP * 0.5), run_time=0.6)
            self.remove(pond)
            new_name = steady("brie_2.jpg", 20, TURN, mono_font=True).move_to(n2, aligned_edge=LEFT)
            self.play(FadeOut(hb), Transform(n2, new_name), run_time=0.7)
            col = VGroup(VGroup(old_dir, Arrow(LEFT * 0.4, RIGHT * 0.4, color=S.GREY, stroke_width=3,
                                               tip_length=0.16), new_dir).arrange(RIGHT, buff=0.2),
                         same_blob.arrange(RIGHT, buff=0.25), same_size, same_n)
            col.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.9, 0.9, 0])
            vo.wait_until("Only the manifest fingerprint")
            self.play(FadeIn(col[0][0]), run_time=0.3)
            self.play(GrowArrow(col[0][1]), FadeIn(new_dir, shift=LEFT * 0.2), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in col[1:]], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("because one name in the list changed")
            self.play(Indicate(n2, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("The opening's two folders were the reverse")
            self.play(FadeIn(mon, shift=UP * 0.3), FadeIn(fri, shift=UP * 0.3), run_time=0.7)
            vo.wait_until("same names, new bytes")
            self.play(each([r[1] for r in mon.rows] + [r[1] for r in fri.rows], INK, scale=1.05, lag=0.08),
                      run_time=0.8)
            self.play(Create(rg), FadeIn(neq), run_time=0.6)
            vo.wait_until("And DVC stores whole files")
            self.play(FadeOut(VGroup(mf2, col)), run_time=0.4)
            self.remove(mf2, col)
            self.play(FadeIn(myth, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("one changed pixel")
            self.play(Indicate(myth.body[1], color=INK, scale_factor=1.04), run_time=0.7)

        self.wait(0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
