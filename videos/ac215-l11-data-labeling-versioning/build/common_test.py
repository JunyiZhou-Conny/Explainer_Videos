"""Workbench for scenes/common.py (scratch, not a scene of the video): plays every set piece's
methods once so explainer.check / preview catch runtime errors, OUT and SMALL before scene agents
rely on them.
    python -m explainer.check videos/ac215-l11-data-labeling-versioning/build/common_test.py Bench --tts silent
    python -m explainer.preview videos/ac215-l11-data-labeling-versioning/build/common_test.py Bench --every 3"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scenes"))

from manim import *  # noqa: E402,F403

from common import *  # noqa: E402,F403


def clear(scene):
    if scene.mobjects:
        scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.3)
        scene.remove(*scene.mobjects)


class Bench(Scene):
    def construct(self):
        self.v7()
        self.v1()
        self.v2()
        self.v3()
        self.v4()
        self.v5()
        self.v6()
        self.glyphs()
        self.terminals()
        self.code_and_tags()

    # ------------------------------------------------------------------ V7 · the running map
    def v7(self):
        m = PipelineMap.at("S02")
        big = m.slide6_big
        self.play(FadeIn(big))
        self.play(FadeIn(m), m.to_strip())
        self.play(FadeIn(m.cli_caption))
        self.play(FadeOut(m.cli_caption))
        self.play(m.light("street", "studio", "cli", "bucket1"), FadeIn(m.secrets))
        self.play(m.pipe_on("studio"), m.pipe_on("cli"), m.pipe_on("dvc"))
        self.play(m.light("labeled", "dvc", "bucket2", "repo", "fuse", "remote"))
        self.play(m.light("flag_v20", "flag_v21", "colab"))
        self.play(m.unlight("fuse"))
        self.play(m.light("fuse"))
        clear(self)
        m2 = PipelineMap.at("S16")
        tr = tracker_l(1)
        self.play(FadeIn(m2), FadeIn(m2.tower), FadeIn(tr))
        marks = [m2.mark(k) for k in ("door", "ticket", "rule", "bouncer", "envelope", "fuse", "shelf", "rope")]
        self.play(LaggedStart(*[FadeIn(k, scale=0.6) for k in marks], lag_ratio=0.15))
        self.play(m2.all_dark())
        clear(self)

    # ------------------------------------------------------------------ V1 · StationMap
    def v1(self):
        tr = tracker_b(1)
        ref = lref("7, 13–14")
        sm = StationMap()
        strip = term(P_LABELING, rows=3)
        self.play(FadeIn(tr), FadeIn(ref), FadeIn(sm), FadeIn(strip))
        self.play(sm.lay(), sm.open_door(), track(tr, 2))
        self.play(sm.pipe_on("db"))
        self.play(sm.pipe_on("secrets"))
        self.play(sm.stick("login"), sm.stick("key path"))
        self.play(sm.tip_over(), sm.alert(ROOT))
        self.play(sm.stand_up(), sm.alert(LAPTOP))
        self.play(sm.join_cli(), sm.light("cli"))
        self.play(sm.pipe_on("cli"))
        type_cmd(self, strip, capture("11").cmd)
        out(self, strip, cols(capture("11").at((2, 3)), ["STATUS", "PORTS", "NAMES"]))
        clear(self)
        sm = StationMap(laid=True, lit=("studio", "cli"), shown=("cli", "door", "browser", "db"))
        self.play(FadeIn(sm))
        b = sm.call("browser")
        n = sm.call("name")
        self.play(Create(b), Create(n))
        loc = sm.call("local")
        self.play(FadeIn(loc), FadeIn(sm.phone()))
        self.play(FadeIn(loc.cross))
        clear(self)
        sm = StationMap(laid=True, lit=("studio", "cli"), shown=("cli", "door", "db"))
        bl, od, gh = sm.blanket(), sm.order(), sm.ghost()
        self.play(FadeIn(sm), Create(bl.box), FadeIn(bl.text))
        self.play(GrowArrow(od.arrow) if isinstance(od.arrow, Arrow) else Create(od.arrow), FadeIn(od.watch))
        self.play(sm.darken("studio"), FadeIn(gh))
        clear(self)

    # ------------------------------------------------------------------ V2 · SignedTicket
    def v2(self):
        st = SignedTicket()
        self.play(FadeIn(st))
        ar = st.reach(self)
        cs = st.cards()
        self.play(st.fan(cs))
        hd = st.hand()
        self.play(FadeIn(hd))
        rl = st.relay()
        self.play(Create(rl.route))
        self.play(Create(rl.strike))
        self.play(FadeOut(VGroup(rl, hd, ar, *cs[7:])))
        self.play(FadeIn(st.bouncer))
        tk = st.stamp(self)
        st.walk(self, tk)
        clear(self)
        st = SignedTicket()
        self.play(FadeIn(st))
        env = st.envelope_to_db(self)
        st.copy_out(self, env)
        clear(self)

    # ------------------------------------------------------------------ V3 · OriginGate
    def v3(self):
        og = OriginGate()
        self.play(FadeIn(og))
        self.play(og.differ())
        pk, x = og.deliver(self, header=False)
        self.play(FadeOut(VGroup(pk, x)))
        rc = og.rule()
        self.play(FadeIn(rc))
        og.stick(self, rc)
        og.deliver(self, header=True)
        pf = og.preflight()
        self.play(Create(pf.line), FadeIn(pf.knock), FadeIn(pf.max_age), FadeIn(pf.caption))
        clear(self)
        og = OriginGate()
        ob = og.other_bucket()
        self.play(FadeIn(og), FadeIn(ob))
        rc = og.rule().move_to(og.slot)
        self.play(FadeIn(rc))
        self.play(rc.animate.move_to(ob.slot))
        og.curl_walk(self)
        clear(self)

    # ------------------------------------------------------------------ V4 · FuseMount + MountLayers
    def v4(self):
        tr = tracker_i(3, extra="row")
        fm = FuseMount()
        strip = term(P_VERSIONING, rows=3)
        self.play(FadeIn(tr), FadeIn(fm), FadeIn(strip))
        self.play(fm.stage(0))
        fm.authenticate(self)
        sn = fm.side_note()
        self.play(FadeIn(sn))
        self.play(fm.stage(1), fm.mount(), FadeOut(sn))
        self.play(FadeIn(fm.sign()))
        self.play(fm.stage(2), fm.bind_on())
        self.play(fm.stage(3), fm.use())
        fm.fetch(self)
        io = fm.inside_only()
        self.play(FadeIn(io))
        clear(self)
        fm = FuseMount()
        self.play(FadeIn(fm))
        fm.broken(self)
        clear(self)
        mc = mount_chips().move_to([0, 1.0, 0])
        mc.implicit.next_to(mc, DOWN, buff=0.3)
        self.play(FadeIn(mc), FadeIn(mc.implicit))
        clear(self)
        ml = MountLayers()
        self.play(FadeIn(ml))
        self.play(ml.light_v())
        self.play(ml.light_fuse())
        self.play(ml.light_inner(), FadeIn(ml.photos()))
        self.play(ml.dark())
        clear(self)
        ml = MountLayers()
        self.play(FadeIn(ml), Create(ml.absent()), FadeIn(ml.v_pipe), FadeIn(ml.v_label))
        clear(self)

    # ------------------------------------------------------------------ V5 · HashShelf
    def v5(self):
        tr = tracker_j(3, extra="stand-in")
        hs = HashShelf()
        strip = term("root@d5bf95465b66:/app#", rows=3)
        self.play(FadeIn(tr), FadeIn(hs), FadeIn(strip))
        for n in IMAGES[:4]:
            hs.hash_photo(self, n)
        self.play(FadeOut(VGroup(*[hs.tiles[n] for n in IMAGES[:4]])))
        mf = hs.manifest()
        self.play(FadeIn(mf))
        hs.hash_manifest(self, mf, predict=True)
        pc = hs.pointer(predict=True)
        self.play(FadeIn(pc))
        hs.confirm(self, pc)
        gb = hs.git_box(pc)
        self.play(FadeIn(gb))
        e = hs.empty_run(self)
        self.play(e.box.animate.set_stroke(S.GREY), e.text.animate.set_color(S.GREY))
        self.play(FadeOut(VGroup(pc, gb)))
        hs.second(self)
        clear(self)
        hs = HashShelf()
        mf = hs.manifest()
        self.play(FadeIn(hs.machine), FadeIn(hs.rack), FadeIn(mf))
        self.play(hs.rename(mf))
        hs.hash_manifest(self, mf, predict=False)
        clear(self)

    # ------------------------------------------------------------------ V6 · TagRope
    def v6(self):
        tr = tracker_j(5)
        tg = TagRope()
        self.play(FadeIn(tr), FadeIn(tg))
        self.play(tg.bead(1))
        self.play(tg.plant("dataset_v20"))
        self.play(tg.zoom())
        r = tg.rope("v20")
        self.play(FadeIn(tg.dirs["v20"]), *[FadeIn(tg.blobs[n]) for n in r.names])
        self.play(Create(r.main))
        self.play(LaggedStart(*[Create(f) for f in r.fans], lag_ratio=0.2))
        self.play(FadeOut(tg.card), FadeOut(r))
        self.play(tg.bead(2))
        self.play(tg.plant("dataset_v21"))
        r2 = tg.rope("v21")
        self.play(FadeIn(tg.dirs["v21"]), FadeIn(tg.blobs[IMAGES[4]]))
        self.play(Create(r2.main), *[Create(f) for f in r2.fans])
        self.play(tg.hop("dataset_v20"))
        self.play(tg.hop("dataset_v21"))
        self.play(FadeOut(r2), FadeOut(tg.cursor))
        tg.pull(self, "v20")
        clear(self)
        tg = TagRope()
        self.play(FadeIn(tg), FadeIn(tg.beads[1:]), FadeIn(tg.bead_labels[1:]), FadeIn(tg.colab),
                  FadeIn(tg.dirs["v21"]))
        tg.stop_at_manifest(self)
        gh = tg.ghost()
        self.play(FadeIn(gh))
        self.play(FadeIn(VGroup(*tg.blobs.values())))
        tg.burn(self)
        clear(self)
        hm = tg.homes()
        si = tg.silhouette().move_to([0, -2.4, 0])
        self.play(FadeIn(hm), FadeIn(si))
        clear(self)

    # ------------------------------------------------------------------ glyphs and cards
    def glyphs(self):
        g = VGroup(tile("Image_1.jpg"), tile(None, broken=True), tile(None, filled=True), annotation(),
                   hourglass(), wax_seal(), bouncer(), stopwatch(), bead(), key_glyph(), lock_glyph(),
                   door_glyph(), bricks(), machine()).arrange_in_grid(rows=2, buff=0.4).move_to([0, 2.0, 0])
        g2 = VGroup(url_ticket(), flag(), flag("dataset_v25", S.GREY, dashed=True), sticky("login"),
                    slip(short(MD5["Image_1.jpg"])), blob(V20["md5"])).arrange_in_grid(rows=2, buff=0.4)
        g2.move_to([0, -0.2, 0])
        g3 = VGroup(task_cards(), house("data-label-cli", 2.1, lit=True), house(None, dashed=True),
                    browser_glyph(), VGroup(drawer("cheeses_labeled/"), drawer("database", LAPTOP, mono_font=False)
                                            ).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=0.35).move_to([0, -2.6, 0])
        self.play(FadeIn(g), FadeIn(g2), FadeIn(g3))
        clear(self)
        v = vault(BUCKET1, ("cheeses_unlabeled/", "cheeses_labeled/")).move_to([-4.2, 1.6, 0])
        w = window(PAGE_ORIGIN, 5.0, 2.4).move_to([2.6, 1.6, 0])
        pw = page_window().move_to([-4.2, -1.6, 0])
        pb = phone_book(list(CONTAINERS.values())).move_to([0.6, -1.6, 0])
        s1 = street(1.8, 6.4, -2.9, laid=False)
        self.play(FadeIn(v), FadeIn(w), FadeIn(illustration_tag().next_to(w, UP, buff=0.1)), FadeIn(pw),
                  FadeIn(pb), FadeIn(s1))
        self.play(lay_street(s1))
        clear(self)
        pc = pointer_card(short(V21["md5"]), V21["size"], V21["nfiles"]).move_to([-3.2, 0.5, 0])
        mc = manifest_card(IMAGES).move_to([3.0, 0.5, 0])
        self.play(FadeIn(pc), FadeIn(mc))
        self.play(each(list(mc.md5s.values()), HASH))
        clear(self)

    # ------------------------------------------------------------------ terminals
    def terminals(self):
        tr = tracker_a(1)
        t = laptop_term(8, P_LAPTOP_HOME)
        self.play(FadeIn(tr), FadeIn(t))
        ln = type_cmd(self, t, capture("01").cmd)
        out(self, t, capture("01").at(2))
        pin(self, ln, beside(turn_row(), ln))
        cd_prompt(self, t, P_LABELING)
        ln = type_cmd(self, t, capture("02").cmd)
        out(self, t, capture("02").at(2), wrap=True)
        xt = beside(extra_row(), ln)
        pin(self, ln, xt, anim=AnimationGroup(FadeIn(xt), track(tr, extra=True)))
        ln = type_cmd(self, t, capture("40").cmd, soft=True)
        out(self, t, capture("40").at((2, 3)))
        eb = on_bar(t, editor_row())
        self.play(FadeIn(eb))
        self.play(FadeOut(eb))
        ln = type_cmd(self, t, capture("41").cmd)
        out(self, t, squash(capture("41").at(3)) + capture("41").at("…", (26, 31)), wrap=True)
        istep(self, t, capture("41").line(32))
        out(self, t, capture("41").at((33, 34), "…", (65, 66)), wrap=True)
        resize(self, t, 4)
        clear(self)
        t = term(P_VERSIONING, rows=6)
        self.play(FadeIn(t), FadeIn(tracker_j(3, extra="stand-in")))
        reenter(self, t, "93")
        ch = reentry_chip().next_to(t.box, UP, buff=0.12).align_to(t.box, RIGHT)
        cn = container_note().next_to(t.box, UP, buff=0.12).align_to(t.box, LEFT)
        self.play(FadeIn(ch), FadeIn(cn))
        bare_prompt(self, t)
        clear(self)
        c = colab_term(4)
        s2 = second_term(3, P_TODAY, T_TODAY).shift(UP * 2.6)
        self.play(FadeIn(c), FadeIn(s2))
        type_cmd(self, c, capture("C13").cmd)
        out(self, c, capture("C13").at(5), wrap=True)
        type_cmd(self, s2, capture("120").cmd)
        out(self, s2, capture("120").at((2, 4)))
        clear(self)

    # ------------------------------------------------------------------ code panels, cards, tags
    def code_and_tags(self):
        p1 = code("data-labeling/docker-shell.sh", 12, 23, font_size=20,
                  cuts={21: 'GOOGLE_APPLICATION_CREDENTIALS="'}).move_to([0, 0.4, 0])
        self.play(FadeIn(p1), FadeIn(line_bar(p1.code, 19 - 12, TURN)))
        clear(self)
        p2 = code("data-labeling/cli.py", 23, 34, cuts={30: '"Content-Type",'}).move_to([0, 0.4, 0])
        rc = readme_card(165, "Run `docker-shell-CLI.sh`", size=20).next_to(p2, DOWN, buff=0.2)
        self.play(FadeIn(p2), FadeIn(rc))
        clear(self)
        ep = code("data-versioning@data-versioning-ac215/docker-entrypoint.sh", 8, 13,
                  cuts={8: "activate-service-account", 10: "gcsfuse"}).move_to([0, 1.4, 0])
        self.play(FadeIn(ep))
        clear(self)
        sr = source_rows("data-versioning@data-versioning-ac215/docker-entrypoint.sh", 10).move_to([0, 1.5, 0])
        nb = code("colab/notebook-1RRQ1SlH.cells.txt", 10, 13, shown="notebook · cell 0").move_to([0, -1.2, 0])
        self.play(FadeIn(sr), FadeIn(nb))
        clear(self)
        c1 = VGroup(your_turn(), extra_tag(), standin_tag(), local_tag(), stand_in_label(), illustration_tag(),
                    recorded_tag("recorded · cli.py:40 + :26–33"), recording_tag(), erratum_tag(), preview_tag(),
                    editor_tag(), cost_tag()).arrange_in_grid(cols=2, buff=0.25).move_to([0, 0.2, 0])
        self.play(FadeIn(c1))
        flash_tag(self, c1[-1], COST)
        clear(self)
        c2 = VGroup(grey_chip("the README shows a tree, not a command"), dashed_chip("training · L13"),
                    tool_chip("dvc"), err_chip("Exited (1)"), fake_chip(), differ_chip(),
                    file_card(KEY_FILE, KEY), turn_row(), extra_row("Linux"), standin_row(), local_row(),
                    time_row(), editor_row(), cost_row(), strip_head("POST /api/storages/gcs/validate · stand-in"),
                    tag_on(Dot(), "x")).arrange_in_grid(cols=2, buff=0.22).move_to([0, 0.0, 0])
        self.play(FadeIn(c2))
        clear(self)
        hc = card(["This recording machine has no Google account, no bucket,",
                   "no browser and no SSH route to GitHub."], head="one honest note")
        self.play(FadeIn(hc))
        clear(self)
        pc = ponder(self, "Four photos already in dvc_store.\nYou add one. How many objects\nwill dvc push upload?",
                    seconds=1)
        self.play(FadeOut(pc))
        qp = quick_predict(self, "The zip held 42 files.\nHow many tasks?", seconds=1)
        self.play(FadeOut(qp))
        self.remove(*self.mobjects)
