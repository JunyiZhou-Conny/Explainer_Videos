"""S10 · One command, and a key inside it — tracker F1 → F3 (note) → F2, lecture_ref 22, 24–25.

Beats (script.md, ## S10; one voiceover block each):
0. F1. CODE(cli.sh: 5–19) as two 10-line windows (5–14, 10–19; 20 pt) with a WHITE cursor bar; line 9
   (the GPU image) YELLOW, line 10 a PINK route to the tarball in a small bucket, line 19's
   `--wandb_key=$WANDB_KEY` outlined GREEN; ▶ your turn. Under the window V4 step 3's job-spec card
   assembles one chip per spoken item (TarballTrip.spec()'s chips, words from laptop/40:77); the image
   slot stays dashed until line 31.
1. CODE(cli.sh: 21–37) as two windows (21–30, 28–37): 22–27 GREY (commented), 31 YELLOW (the image
   chip fills in: tf-cpu), 32–37 outlined. Then README cards 152–154 (erratum, "already done in cli.sh ·
   commit 3efb2d5") and 136–142 ("may be out of date · …", not spoken); tracker F3 · already the default.
2. F2. The card collapses into a spec glyph; V1 (TrainingMap.at("S10")): GOLD cost tag, the glyph rides
   the submit route to Vertex AI, a BLUE job tile with a GOLD meter; the key-length chip. Then the
   cockpit (laptop/40, fresh-cockpit chip, README card 150): sh cli.sh → 43 GREEN, 44 RED; ▶ your
   turn; V5 preview: the empty key-file lanyard; F2 · extra gcloud auth list → 58 RED; "with your key"
   chip (no panel).
3. F2 · extra. sh -x cli.sh → 64–66, 69 (YELLOW, then overridden by 76), 75, 76, 77 folded; the strip
   under 77's chips (worker-pool-spec items, --args with the key RED); V5's W&B badge turns RED.
4. The RED badge, large. PONDER 8 s.
5. The answer: a GREY viewer over the badge's shoulder; four GREY chips.
6. F2 · extra. laptop · new terminal: sh docker-shell.sh (70: 34, …, 41), echo ${#WANDB_KEY} → 0 RED,
   the grep → --wandb_key= RED; fix chip. A third strip: sh docker-shell.sh → 71:34 RED; fixed-name chip.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F403
from explainer import style as S

SAY = NARRATION["S10"]
PONDER_KEY = "Your W&B key is now part of the\njob's arguments. Who can read it later?"
C26 = ("--worker-pool-spec=", "accelerator-type", "$ACCELERATOR_TYPE,")
CUTS_A = {9: ('"', "tf-gpu")}
CUTS_B = {14: '"us-central1"', 17: "mobilenetv2,", 18: "mobilenetv2,",
          19: ("mobilenetv2,", "--wandb_key")}


def put_top_left(m, x=-6.45, y=2.72):
    m.shift(np.array([x - m.get_left()[0], y - m.get_top()[1], 0]))
    return m


def fold_line(s: str, n: int) -> list[str]:
    """A long capture line broken into rows of <= n characters: at spaces first, then (inside a
    token with no space) after its last ',' or '/' that fits. The text is unchanged; only the row
    breaks move (a space at a break is dropped, as soft() does)."""
    pieces = []
    for j, tok in enumerate(s.split(" ")):
        first = True
        while len(tok) > n:
            k = max(tok.rfind(",", 0, n), tok.rfind("/", 0, n))
            k = k if k > 0 else n - 1
            pieces.append((tok[:k + 1], " " if (first and j) else ""))
            tok, first = tok[k + 1:], False
        pieces.append((tok, " " if (first and j) else ""))
    rows, cur = [], ""
    for p, sep in pieces:
        if cur and len(cur) + len(sep) + len(p) <= n:
            cur += sep + p
        else:
            if cur:
                rows.append(cur)
            cur = p
    rows.append(cur)
    assert all(len(r) <= n for r in rows), rows
    return rows


def bucket_mini() -> VGroup:
    """A small BLUE bucket holding the GREEN tarball (the target of line 10's route)."""
    t = label("bucket", 20, CLOUD)
    pc = parcel(None, OWNED, 20, 0.42, 0.3)
    inner = VGroup(t, pc).arrange(RIGHT, buff=0.18)
    fr = RoundedRectangle(width=inner.width + 0.4, height=0.5, corner_radius=0.08, stroke_color=CLOUD,
                          stroke_width=2.5).set_fill(CLOUD, 0.1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.parcel_ = pc
    return g


def spec_frame(sp) -> VGroup:
    """V4 step 3 laid out under a code window: the spec chips in four rows (name · machine /
    replicas · image / package + the bucket / module · args), a GREY frame with a 'job spec' tab.
    Returns the frame group (.frame .tab .bucket .rows .slot); the chips are sp.chips."""
    c = sp.chips
    bk = bucket_mini()
    rows = VGroup(VGroup(c[0], c[1]).arrange(RIGHT, buff=0.15),
                  VGroup(c[2], c[3]).arrange(RIGHT, buff=0.15),
                  VGroup(c[4], bk).arrange(RIGHT, buff=0.45),
                  VGroup(c[5], c[6]).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    fr = RoundedRectangle(width=rows.width + 0.5, height=rows.height + 0.3, corner_radius=0.14,
                          stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    rows.move_to(fr).shift(DOWN * 0.02)
    tt = label("job spec · gcloud ai custom-jobs create", 20, S.GREY)
    tab_bg = Rectangle(width=tt.width + 0.2, height=tt.height + 0.06, stroke_width=0).set_fill(S.BG, 1)
    tab = VGroup(tab_bg, tt).move_to(fr.get_corner(UR) + np.array([-0.3 - tt.width / 2, 0, 0]))
    slot = box(c[3].width, c[3].height, S.GREY, dashed=True).move_to(c[3])
    g = VGroup(fr, tab, bk)
    g.frame, g.tab, g.bucket, g.rows, g.slot = fr, tab, bk, rows, slot
    return g


def spec_glyph() -> VGroup:
    """The job spec as a small card glyph (no text): BLUE, PINK and GREEN lines for the machine
    order, the package route and the --args."""
    fr = RoundedRectangle(width=0.7, height=0.52, corner_radius=0.06, stroke_color=S.GREY,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    ls = VGroup(*[Line(LEFT * 0.22, RIGHT * 0.22, stroke_width=4, color=c) for c in (CLOUD, ROUTE, KEY)])
    ls.arrange(DOWN, buff=0.08).move_to(fr)
    return VGroup(fr, ls)


def empty_slot_badge(ref_badge) -> VGroup:
    """Where the key-file badge would hang: a GREY dashed outline with 'model-trainer.json · missing'."""
    fr = box(ref_badge.width, ref_badge.height, S.GREY, dashed=True).move_to(ref_badge)
    t = VGroup(mono(KEY_FILE, 20, S.GREY), label("not loaded", 20, S.GREY)).arrange(DOWN, buff=0.08).move_to(fr)
    return VGroup(fr, t)


class OneCommand(VoiceScene):
    def keep_only(self, *keep, run_time=0.5, shift=UP * 0.2):
        fam = {id(x) for k in keep for x in k.get_family()}
        gone = [m for m in self.mobjects if not any(id(x) in fam for x in m.get_family())]
        if gone:
            self.play(FadeOut(Group(*gone), shift=shift), run_time=run_time)
            self.remove(*gone)

    def construct(self):
        assert len(SAY) == SAY_COUNT["S10"] == 7, len(SAY)
        c40, c70, c71 = capture("40"), capture("70"), capture("71")

        # ========================================================== 0. review cli.sh (F1)
        tr = tracker_f(1)
        ref = lref("22, 24–25")
        assert tracker_f(3, note_="already the default").caption.get_right()[0] < ref.get_left()[0]
        assert tracker_f(2, extra=True).caption.get_right()[0] < ref.get_left()[0]
        assert tr.head.get_right()[0] < ref.get_left()[0] or tr.head.get_bottom()[1] > ref.get_top()[1], \
            (tr.head.get_right(), ref.get_left())
        pa = put_top_left(code("cli.sh", 5, 12, font_size=20, cuts=CUTS_A))
        pb = put_top_left(code("cli.sh", 12, 19, font_size=20, cuts=CUTS_B))
        sp = TarballTrip.spec()
        sf = spec_frame(sp)
        sf_all = VGroup(sf, *sp.chips, sf.slot)
        sf_all.next_to(pa, DOWN, buff=0.12).align_to(pa, LEFT)
        assert sf_all.get_bottom()[1] > -3.58, sf_all.get_bottom()
        yt0 = your_turn()
        yt0.move_to([pa.get_right()[0] - yt0.width / 2 - 0.1, pa.header.get_center()[1], 0])
        cur = line_bar(pa.code, 1, INK, opacity=0.12)
        bar9 = line_bar(pa.code, 4, TURN)
        gpu = code_span(pa.code, 4, "tf-gpu")

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(pa, shift=UP * 0.15), run_time=0.7)
            self.play(FadeIn(sf.frame), FadeIn(sf.tab), run_time=0.4)
            vo.wait_until("pause and open it")
            self.play(FadeIn(yt0, shift=LEFT * 0.15), run_time=0.3)
            flash_tag(self, yt0, TURN, run_time=0.5)
            vo.wait_until("It names the job with random hex")
            self.play(FadeIn(cur), Indicate(code_span(pa.code, 0, "openssl rand -hex 6"), color=INK,
                                            scale_factor=1.06), run_time=0.6)
            self.play(FadeIn(sp.chips[0], shift=RIGHT * 0.2), run_time=0.4)
            vo.wait_until("asks for one n1-standard-4 machine")
            self.play(cur.animate.move_to(line_bar(pa.code, 2, INK)), FadeIn(sp.chips[1], shift=RIGHT * 0.2),
                      run_time=0.5)
            self.play(cur.animate.move_to(line_bar(pa.code, 3, INK)), FadeIn(sp.chips[2], shift=RIGHT * 0.2),
                      run_time=0.5)
            vo.wait_until("and sets a GPU image")
            self.play(FadeOut(cur), FadeIn(bar9), gpu.animate.set_color(TURN), run_time=0.4)
            self.play(Create(sf.slot), Indicate(gpu, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Then it points at your tarball")
            l10 = code_span(pa.code, 5, "$GCS_BUCKET_URI/cheese-app-trainer.tar.gz")
            a = l10.get_right() + RIGHT * 0.1
            b = sf.bucket.get_right() + RIGHT * 0.08
            rt = CurvedArrow(a, b, angle=-1.6, color=ROUTE, stroke_width=4, tip_length=0.18)
            self.play(l10.animate.set_color(ROUTE), Create(rt), FadeIn(sf.bucket), run_time=0.7)
            self.play(FadeIn(sp.chips[4], shift=RIGHT * 0.2), Indicate(sf.bucket.parcel_, color=OWNED,
                                                                        scale_factor=1.3), run_time=0.5)
            vo.wait_until("and the module to run")
            cur = line_bar(pa.code, 6, INK, opacity=0.12)
            self.play(FadeIn(cur), FadeIn(sp.chips[5], shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("and builds the arguments")
            self.play(FadeOut(VGroup(pa, bar9, yt0, cur, rt), shift=UP * 0.3), FadeIn(pb, shift=UP * 0.3),
                      run_time=0.5)
            self.remove(pa, bar9, yt0, cur, rt)
            cur = line_bar(pb.code, 7, INK, opacity=0.12)
            self.play(FadeIn(cur), run_time=0.3)
            vo.wait_until("ending with your W and B key")
            kr = ring(code_span(pb.code, 7, "--wandb_key=$WANDB_KEY"), OWNED, buff=0.06)
            self.play(Create(kr), FadeIn(sp.chips[6], shift=RIGHT * 0.2), run_time=0.6)
            self.play(Indicate(sp.chips[6].text, color=OWNED, scale_factor=1.08), run_time=0.6)

        # ========================================================== 1. the GPU block is commented out (F1 → F3)
        pc = put_top_left(code("cli.sh", 21, 28, font_size=20, cuts={26: C26}))
        pd = put_top_left(code("cli.sh", 30, 37, font_size=20, cuts={31: ('"', "tf-cpu"),
                                                                    36: "machine-type=$MACHINE_TYPE,"}))
        greys = VGroup(*[line_bar(pc.code, k, S.GREY, opacity=0.2) for k in range(1, 7)])
        bar31 = line_bar(pd.code, 1, TURN)
        runs = ring(VGroup(*[pd.code.code_lines[k] for k in range(2, 8)]), INK, buff=0.08)
        r1 = readme_card((152, 154), size=20)
        r2 = readme_card((136, 142), size=20)
        put_top_left(r1, -6.45, 2.65)
        r2.move_to([6.5 - r2.width / 2, 2.65 - r2.height / 2, 0])
        assert r1.get_right()[0] < r2.get_left()[0] - 0.2, (r1.get_right(), r2.get_left())
        err = erratum_tag().next_to(r1, DOWN, buff=0.2).align_to(r1, LEFT)
        done = grey_chip("already done in cli.sh · commit 3efb2d5").next_to(err, RIGHT, buff=0.25)
        stale = grey_chip("may be out of date · check Google's current list")
        stale.next_to(r2, DOWN, buff=0.2).align_to(r2, RIGHT)
        assert stale.get_top()[1] < done.get_bottom()[1] - 0.1 or stale.get_left()[0] > done.get_right()[0]

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(pb, cur, kr), shift=UP * 0.3), FadeIn(pc, shift=UP * 0.3), run_time=0.6)
            self.remove(pb, cur, kr)
            vo.wait_until("the GPU block is commented out")
            self.play(LaggedStart(*[FadeIn(g) for g in greys], lag_ratio=0.15), run_time=0.8)
            self.play(Indicate(pc.code.code_lines[0], color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("and line 31 swaps in the CPU image")
            self.play(FadeOut(VGroup(pc, greys), shift=UP * 0.3), FadeIn(pd, shift=UP * 0.3), run_time=0.5)
            self.remove(pc, greys)
            self.play(FadeIn(bar31), code_span(pd.code, 1, "tf-cpu").animate.set_color(TURN), run_time=0.4)
            self.play(FadeOut(sf.slot), FadeIn(sp.chips[3], shift=UP * 0.15), run_time=0.5)
            self.remove(sf.slot)
            vo.wait_until("so only the CPU command runs")
            self.play(Create(runs), run_time=0.6)
            self.play(Indicate(sp.chips[3].text, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("A small slip")
            self.keep_only(tr, ref, run_time=0.5)
            self.play(FadeIn(r1, shift=UP * 0.15), FadeIn(err, shift=UP * 0.1), run_time=0.6)
            flash_tag(self, err, S.GREY, run_time=0.5)
            vo.wait_until("the README shows GPU first and CPU as optional")
            self.play(Indicate(r1.body[0], color=INK, scale_factor=1.04), FadeIn(r2, shift=LEFT * 0.15),
                      run_time=0.7)
            self.play(FadeIn(stale, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("but the script already runs on CPU")
            self.play(FadeIn(done, shift=LEFT * 0.15), track(tr, 3, note_="already the default"), run_time=0.6)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.06), run_time=0.7)

        # ========================================================== 2. the gold tag, the submit (F2)
        mp = TrainingMap.at("S10")
        ck = mp.parts["cockpit"]
        tile = mp.parts["cpu_tile"]
        glyph = spec_glyph()
        sp2 = TarballTrip.spec()
        sf2 = spec_frame(sp2)
        sf2_all = VGroup(sf2, *sp2.chips).move_to([0, -0.2, 0])
        gold = cost_tag("the job's VM bills while it is up: from provisioning until the script exits\n"
                        "see the Vertex AI pricing page")
        gold.move_to([0, -2.05, 0])
        k40 = grey_chip("scene 9's check: the last number · 40 for wandb 0.15.11")
        k40.next_to(gold, DOWN, buff=0.2)
        assert gold.get_top()[1] < -1.36 and k40.get_bottom()[1] > -3.58, (gold.get_top(), k40.get_bottom())
        words = mp.labels("submit")

        t = term(P_COCKPIT, rows=6)
        fresh = container_note()
        r150 = readme_card(150)
        tb0 = ThreeBadges()
        ghost = empty_slot_badge(tb0.badges[0])
        r150.move_to([6.5 - r150.width / 2, 2.35, 0])
        fresh.next_to(r150, DOWN, buff=0.22).align_to(r150, RIGHT)
        yours = grey_chip("with your key: gcloud reports the job as created")
        yours.move_to([6.5 - yours.width / 2, 0.25, 0])
        assert ghost.get_right()[0] < fresh.get_left()[0] and ghost.get_bottom()[1] > t.box.get_top()[1], \
            (ghost.get_right(), fresh.get_left(), ghost.get_bottom(), t.box.get_top())

        with self.voiceover(SAY[2]) as vo:
            self.keep_only(tr, ref, run_time=0.4)
            self.play(track(tr, 2), FadeIn(sf2_all, scale=0.95), run_time=0.5)
            glyph.move_to(sf2.frame)
            self.play(FadeOut(VGroup(sf2.tab, sf2.bucket, *sp2.chips)), ReplacementTransform(sf2.frame, glyph),
                      run_time=0.6)
            self.remove(sf2, *sp2.chips)
            self.play(FadeIn(mp), glyph.animate.move_to(ck.get_center() + DOWN * 0.05), run_time=0.7)
            vo.wait_until("A gold tag first")
            self.play(FadeIn(gold, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, gold, COST, run_time=0.6)
            vo.wait_until("once the job's machine is provisioned")
            self.play(mp.reveal("submit"), FadeIn(words), mp.light("vertex"), run_time=0.6)
            self.play(travel(glyph, mp.parts["submit"].submobjects[0], run_time=1.0))
            self.play(FadeOut(glyph, scale=0.6), mp.reveal("cpu_tile", run_time=0.6), run_time=0.6)
            self.remove(glyph)
            vo.wait_until("your project pays until the script exits")
            self.play(meter_run(tile.meter), run_time=1.0)
            vo.wait_until("Check that your key length is 40")
            self.play(FadeIn(k40, shift=UP * 0.1), Indicate(mp.parts["key"], color=OWNED, scale_factor=1.1),
                      run_time=0.6)
            vo.wait_until("watch scene 11 before you submit")
            self.play(Indicate(k40.text, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Now sh cli.sh")
            self.keep_only(tr, ref, run_time=0.5)
            self.play(FadeIn(t), FadeIn(r150, shift=LEFT * 0.15), FadeIn(fresh, shift=UP * 0.1), run_time=0.5)
            pl = istep(self, t, c40.line(42), type_time=0.6)
            vo.wait_until("pause and run it")
            yt = beside(turn_row(), pl)
            pin(self, pl, yt, run_time=0.3)
            flash_tag(self, yt, TURN, run_time=0.5)
            vo.wait_until("The first line is real")
            o1 = out(self, t, [(c40.line(43), PASS)], run_time=0.4)
            self.play(Indicate(substring(o1[0], "us-central1"), color=PASS, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Then it stops with no active account")
            o2 = out(self, t, [c40.line(44)], wrap=True, color=ERR, run_time=0.4)
            self.play(Indicate(VGroup(*o2), color=ERR, scale_factor=1.02), run_time=0.5)
            vo.wait_until("because the key never loaded")
            self.add(tb0)
            self.play(tb0.lanyard(0), run_time=0.5)
            self.play(FadeIn(ghost, shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("an extra auth list confirms it")
            ex = on_bar(t, extra_row())
            self.play(track(tr, 2, extra=True), FadeIn(ex), run_time=0.4)
            istep(self, t, c40.line(56), type_time=0.4)
            out(self, t, [(c40.line(58), ERR)], run_time=0.3)
            vo.wait_until("With your key, gcloud reports the job as created")
            self.play(FadeIn(yours, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(yours.text, color=INK, scale_factor=1.04), run_time=0.6)

        # ========================================================== 3. sh -x: the job it tried to send (F2 · extra)
        t3 = term(P_COCKPIT, rows=12)
        ex3 = on_bar(t3, extra_row())
        n = t3.max_chars
        r69 = fold_line(c40.line(69), n)
        r75 = fold_line(c40.line(75), n)
        r76 = fold_line(c40.line(76), n)
        r77 = fold_line(c40.line(77), n)
        key = "--wandb_key=" + WANDB_KEY_PH
        assert r77[-1] == key, r77
        assert "<12 hex>" in c40.line(77) and "<12 hex>" in c40.line(65)
        machine, replicas, image, module = SPEC_CHIPS
        image_short = "executor-image-uri=…" + image.rsplit("/", 1)[1]
        head = VGroup(mono("--worker-pool-spec", 20, INK), note("· the job's machine order", S.GREY))
        head.arrange(RIGHT, buff=0.18)
        c_m, c_r = chip(machine, CLOUD, size=20, font=MONO), chip(replicas, CLOUD, size=20, font=MONO)
        one = note("one machine", S.GREY)
        c_i, c_mod = chip(image_short, IMAGE, size=20, font=MONO), chip(module, CLOUD, size=20, font=MONO)
        args = "--args=" + c40.line(77).split("--args=", 1)[1]
        arows = at_commas(args, 52)
        assert arows[-1] == key, arows
        a_txt = VGroup(*[mono(s, 20, INK) for s in arows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        a_box = RoundedRectangle(width=a_txt.width + 0.45, height=a_txt.height + 0.3, corner_radius=0.1,
                                 stroke_color=KEY, stroke_width=2.5).set_fill(KEY, 0.12)
        a_txt.move_to(a_box)
        a_card = VGroup(a_box, a_txt)
        pic = VGroup(head, VGroup(c_m, c_r, one).arrange(RIGHT, buff=0.15), c_i, c_mod, a_card)
        pic.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        put_top_left(pic, -6.4, 2.7)
        tb = ThreeBadges()
        tb.shift(RIGHT * 0.35)      # badge 2 alone this beat: room for the --args card on its left
        assert tb.badges[2].get_right()[0] < 6.6
        assert pic.get_bottom()[1] > -1.3 and pic.get_right()[0] < tb.badges[2].get_left()[0] - 0.15, \
            (pic.get_bottom(), pic.get_right())

        with self.voiceover(SAY[3]) as vo:
            self.keep_only(tr, ref, run_time=0.4)
            self.play(FadeIn(t3), FadeIn(ex3), run_time=0.4)
            istep(self, t3, c40.line(63), type_time=0.5)
            o3 = out(self, t3, c40.at(64, 65, 66), run_time=0.4)
            vo.wait_until("The GPU image is set")
            o69 = out(self, t3, [(s, TURN) for s in r69], run_time=0.3)
            self.play(Indicate(substring(o69[-1], "tf-gpu"), color=TURN, scale_factor=1.15), run_time=0.5)
            vo.wait_until("then overridden by the CPU image")
            out(self, t3, r75, run_time=0.3)
            o76 = out(self, t3, r76, run_time=0.3)
            self.play(substring(o76[-1], "tf-cpu").animate.set_color(INK), run_time=0.2)
            sts = VGroup(*[strike(r, INK, 3) for r in o69])
            self.play(Create(sts), run_time=0.5)
            self.play(VGroup(*o69).animate.set_color(S.GREY), FadeOut(sts), run_time=0.4)
            self.remove(sts)
            vo.wait_until("Then the full command")
            o77 = out(self, t3, r77, run_time=0.8, lag=0.06)
            vo.wait_until("The worker pool spec is the job's machine order")
            resize(self, t3, 3, run_time=0.6, extra=[ex3.animate.shift(DOWN * 9 * t3.pitch)])
            self.play(FadeIn(head, shift=RIGHT * 0.15), run_time=0.4)
            vo.wait_until("machine type")
            self.play(FadeIn(c_m, shift=RIGHT * 0.15), run_time=0.4)
            vo.wait_until("one replica, meaning one machine")
            self.play(FadeIn(c_r, shift=RIGHT * 0.15), FadeIn(one), run_time=0.4)
            vo.wait_until("image and module")
            self.play(FadeIn(c_i, shift=RIGHT * 0.15), run_time=0.35)
            self.play(FadeIn(c_mod, shift=RIGHT * 0.15), run_time=0.35)
            vo.wait_until("Last come the arguments")
            self.play(FadeIn(a_card, shift=RIGHT * 0.15), run_time=0.5)
            self.add(tb)
            self.play(tb.hang(2), run_time=0.8)
            vo.wait_until("in plain text")
            self.play(a_txt[-1].animate.set_color(ERR), o77[-1].animate.set_color(ERR),
                      a_box.animate.set_stroke(ERR), tb.turn_red(), run_time=0.8)
            self.play(Indicate(a_txt[-1], color=ERR, scale_factor=1.05), run_time=0.6)

        # ========================================================== 4. the RED badge, large · PONDER 8 s
        big = badge(["W&B key", "for wandb.ai", "carried in --args"], ERR, 28, "wandb", mono_first=False)
        big.move_to([0, 1.55, 0])

        with self.voiceover(SAY[4]) as vo:
            self.keep_only(tr, ref, tb, run_time=0.5)
            self.play(FadeOut(tb.badges[2], scale=1.3), FadeOut(tb.strings[2]), FadeIn(big, scale=0.6), run_time=0.7)
            self.remove(tb, *tb.badges, *tb.strings)
            vo.wait_until("Your W and B key is now part")
            self.play(Indicate(big.text, color=ERR, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Who can see it later")
            self.play(Wiggle(big.frame, scale_value=1.03), run_time=0.7)
        pq = ponder(self, PONDER_KEY, seconds=8, center=(0, -1.75))

        # ========================================================== 5. the answer
        viewer = person_icon(S.GREY, 1.0)
        ans = VGroup(grey_chip("anyone who can view jobs in this project (the job spec keeps --args)"),
                     grey_chip("your shell history, if typed inline"),
                     grey_chip("use a dedicated key · rotate it at the end"),
                     grey_chip("Secret Manager: exercises")).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        ans.move_to([0, -1.95, 0])
        assert ans.get_bottom()[1] > -3.58 and ans.width < 13.0, (ans.get_bottom(), ans.width)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pq), big.animate.shift(RIGHT * 0.9), run_time=0.5)
            self.remove(pq)
            viewer.next_to(big, LEFT, buff=0.15).align_to(big, UP).shift(UP * 0.25)
            self.play(FadeIn(viewer, shift=RIGHT * 0.3), run_time=0.6)
            vo.wait_until("Anyone who can view jobs in this project")
            self.play(FadeIn(ans[0], shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(viewer, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("plus your shell history")
            self.play(FadeIn(ans[1], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Use a dedicated key")
            self.play(FadeIn(ans[2], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the exercises use Secret Manager")
            self.play(FadeIn(ans[3], shift=UP * 0.1), run_time=0.5)

        # ========================================================== 6. a key never exported (F2 · extra)
        nt = new_term(9, P_REPO)
        ex6 = on_bar(nt, extra_row())
        fix = grey_chip("fix: exit · export · sh docker-shell.sh")
        fixed = grey_chip("fixed name: model-training-cli")
        st = term(P_REPO, rows=5, title=T_LAPTOP)
        ex7 = on_bar(st, extra_row())
        rows45 = at_commas(c70.line(45), nt.max_chars)
        assert rows45[-1].endswith("--wandb_key="), rows45

        with self.voiceover(SAY[6]) as vo:
            self.keep_only(tr, ref, run_time=0.5)
            self.play(FadeIn(nt), FadeIn(ex6), run_time=0.5)
            type_cmd(self, nt, c70.cmd, type_time=0.6)
            out(self, nt, [c70.line(34), "…", c70.line(41)], run_time=0.4)
            vo.wait_until("Inside, its length is 0")
            istep(self, nt, c70.line(42), type_time=0.5)
            o0 = out(self, nt, [(c70.line(43), ERR)], run_time=0.3)
            self.play(Indicate(o0[0], color=ERR, scale_factor=1.4), run_time=0.5)
            vo.wait_until("and the arguments end with an empty key")
            istep(self, nt, c70.line(44), type_time=0.7)
            o45 = out(self, nt, rows45, run_time=0.4)
            ek = substring(o45[-1], "--wandb_key=")
            self.play(ek.animate.set_color(ERR), run_time=0.4)
            vo.wait_until("So the job would download its data")
            ekr = ring(ek, ERR, buff=0.06)
            self.play(Create(ekr), run_time=0.5)
            vo.wait_until("Exit, export, and start again")
            fix.next_to(nt.box, UP, buff=0.15).align_to(nt.box, RIGHT)
            self.play(FadeIn(fix, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("first exit any old cockpit")
            self.play(FadeOut(ekr), run_time=0.2)
            self.remove(ekr)
            resize(self, nt, 3, run_time=0.5, extra=[ex6.animate.shift(DOWN * 6 * nt.pitch),
                                                       fix.animate.shift(DOWN * 6 * nt.pitch)])
            up = 0.62 - nt.box.get_bottom()[1]
            gap_y = (st.box.get_top()[1] + 0.62) / 2      # between the two strips, below the lecture ref
            self.play(VGroup(nt, *nt.lines, ex6).animate.shift(UP * up), FadeIn(st),
                      fix.animate.move_to([-6.5 + fix.width / 2, gap_y, 0]), run_time=0.5)
            self.play(FadeIn(ex7), run_time=0.2)
            type_cmd(self, st, c71.cmd, type_time=0.5)
            out(self, st, [c71.line(34)], wrap=True, color=ERR, run_time=0.4)
            fixed.move_to([6.5 - fixed.width / 2, gap_y, 0])
            assert fix.get_right()[0] < fixed.get_left()[0] - 0.2, (fix.get_right(), fixed.get_left())
            self.play(FadeIn(fixed, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(fixed.text, color=INK, scale_factor=1.05), run_time=0.5)
        self.wait(0.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
