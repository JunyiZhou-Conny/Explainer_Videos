"""S06 · CORS: the bouncer, configured on the bucket — tracker C1 → C4, `lref("13")` on the CLI container.

Beats (script.md, ## S06; one voiceover block each):
0. TRACKER C1 (tracker C appears), a GREY chip 'tutorial only' where the lecture tag would sit. V3:
   the page island (http://localhost:8080) and the BLUE bucket island (https://storage.googleapis.com),
   scheme · host · port chips light; the GREY bouncer at the browser's door (chip: L10's Chroma
   bouncer, now on a bucket); on "the page's own code" the CORS-mode note; a package without
   Access-Control-Allow-Origin → RED X, the tile stays broken; the empty rule slot on the bucket.
1. Kind erratum card: README.md lines 153, 157 quoted; "reverse DNS lookup" struck through in GREY →
   'the browser's same-origin rule + a response header'; "must be done programmatically" → GREY chip.
2. TRACKER C1: CODE(docker-shell-CLI.sh: 23), cheese-app-data-demo RED; the sed edit (laptop/40 line 1,
   'our editor; use yours') → 40:2–3, your-bucket-placeholder GREEN, ▶. TRACKER C2: README card
   line 165 ('the README names the script'); sh docker-shell-CLI.sh → 41: 3 (squashed), …, 26–31;
   aarch64 chip on 27, 'at the time of recording' on 29–30; lref 13; the prompt becomes
   app@5bf8945fb887:/app$ ('yours will differ'); the strip shrinks and V7's second TEAL house lights. ▶.
3. V1: the CLI house joins the street; CODE(docker-shell-CLI.sh: 15–25): 17 PINK, 24 YELLOW
   ('a name, not localhost · scene 7'), 19 YELLOW ('mounted by folder name · keep it data-labeling').
4. TRACKER C3: python cli.py -c → 41: 33–34, …, 65–66 (66 RED), ▶. TRACKER C4: python cli.py -m →
   41: 68–69, …, 100–101 (101 RED), ▶. CODE(cli.py: 22–33 → 23–34): 23 YELLOW ('no key path · ADC,
   as in L10'), 26–33 GREEN, 34 YELLOW.
5. Recorded cards (cli.py:40 + :26–33; cli.py:47–72, Cors YELLOW). V3: the rule card sticks on the
   bucket, the next package carries the header and is waved in, the tile fills; the OPTIONS knock
   with 'maxAgeSeconds: 3600', 'preflights only · a plain GET has none'.
6. The broken grid again (illustration). PONDER 8 s.
7. Suspect 1: CODE(:23), 41:66 flashes small, chips; the rule card flies to your other bucket;
   'check with python cli.py -m'. Suspect 2: refresh arrow, 'hard refresh · or a private window'.
   curl strolls past with no bouncer: 'CORS is not access control · no signed URL → still refused'.
   Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S06"]
PONDER_Q = "You ran cli.py -c and refreshed:\nstill broken thumbnails.\nTwo suspects?"
CLI_SH = "data-labeling/docker-shell-CLI.sh"
CLI_PY = "data-labeling/cli.py"
PROMPT_CLI = "app@5bf8945fb887:/app$"
README_153 = ("GCP buckets restrict access from domains that can't be resolved",
              "via reverse DNS lookup.")
README_157 = ("there's no direct way to configure CORS for this use case through",
              "the GCP web interface—it must be done programmatically.")
REC_CORS = ("set_cors_configuration()",
            "Set CORS policies for bucket <your bucket> is [{'origin': ['*'],",
            "'method': ['GET'], 'responseHeader': ['Content-Type',",
            "'Access-Control-Allow-Origin'], 'maxAgeSeconds': 3600}]")
REC_META = ("view_bucket_metadata()", "ID: …", "Name: …", "…", "Cors: […]", "…")


def drop(scene, *mobs) -> None:
    """Take mobjects and their whole families off the scene (a scrolled terminal is split into parts)."""
    fam = []
    for m in mobs:
        fam.extend(m.get_family())
    scene.remove(*fam)


def glyphs(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` inside a label/mono Text (its .text drops spaces; so do its glyphs)."""
    flat, key = t.text.replace(" ", ""), sub.replace(" ", "")
    i = flat.index(key)
    return VGroup(*t.submobjects[i:i + len(key)])


def mono_card(lines, colours=None, size: float = 20) -> VGroup:
    """A GREY card of mono rows (the recorded prints). .frame .rows"""
    colours = colours or {}
    rows = VGroup(*[mono(s, size, colours.get(i, INK)) for i, s in enumerate(lines)])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    fr = RoundedRectangle(width=rows.width + 0.6, height=rows.height + 0.45, corner_radius=0.14,
                          stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


def broken_page() -> VGroup:
    """The page with eight broken thumbnails (illustration). .win .grid"""
    win = window("localhost:8080", 5.4, 3.4).move_to([0, 0.35, 0])
    grid = VGroup(*[tile(None, 0.7, LAPTOP, broken=True) for _ in range(8)]).arrange_in_grid(rows=2, cols=4,
                                                                                           buff=0.3)
    grid.move_to(win.content)
    g = VGroup(win, grid)
    g.win, g.grid = win, grid
    return g


def ill_tag(og) -> VMobject:
    """The `illustration` tag under V3's schematic page window (left edge, clear of packages and curl)."""
    return illustration_tag().next_to(og.page, DOWN, buff=0.15).align_to(og.page, LEFT)


def refresh_arrow(r: float = 0.32, color=TURN) -> VMobject:
    """A circular refresh arrow."""
    a = Arc(radius=r, start_angle=PI * 0.6, angle=-PI * 1.6, color=color, stroke_width=5)
    a.add_tip(tip_length=0.16, tip_width=0.16)
    return a


class CorsOnTheBucket(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S06"] == 8, len(SAY)

        # ========================================================== 0. two origins, the bouncer, no header
        tr = tracker("C", 1)
        tut = grey_chip("tutorial only · no lecture slide on CORS")
        tut.move_to([6.5 - tut.width / 2, 3.25, 0])
        og = OriginGate()
        left = VGroup(og.page, og.tile, og.origin_l, *og.parts_l.values())
        right = VGroup(og.bucket, og.origin_r, *og.parts_r.values())
        il0 = ill_tag(og)
        chroma = grey_chip("L10: the Chroma bouncer · now on a bucket").move_to([0, -2.85, 0])
        mode = card(["Label Studio's page fetches the photo in CORS mode → the browser checks",
                     "a plain image tag would not"], size=20).move_to([0, -2.85, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(tut), run_time=0.6)
            self.play(FadeIn(left, shift=RIGHT * 0.3), FadeIn(il0), run_time=0.7)
            self.play(Indicate(og.origin_l, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("the photo from Google's storage address")
            self.play(FadeIn(right, shift=LEFT * 0.3), run_time=0.7)
            self.play(Indicate(og.origin_r, color=CLOUD, scale_factor=1.06), run_time=0.6)
            vo.wait_until("a different origin")
            self.play(og.differ())
            vo.wait_until("When the page's own code")
            self.play(FadeIn(og.bouncer, shift=UP * 0.2), FadeIn(chroma, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(og.bouncer, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("as Label Studio does")
            self.play(FadeOut(chroma), FadeIn(mode, shift=UP * 0.15), run_time=0.6)
            drop(self, chroma)
            vo.wait_until("your browser hands the answer over")
            pk, x = og.deliver(self, header=False)
            vo.wait_until("Google adds that header")
            rg = ring(og.slot, TURN, buff=0.1)
            self.play(Create(rg), Indicate(og.bucket.title, color=CLOUD, scale_factor=1.06), run_time=0.7)
            vo.wait_until("its own CORS rule")
            self.play(FadeOut(rg), run_time=0.4)
            self.play(Indicate(og.tile, color=ERR, scale_factor=1.15), run_time=0.6)

        # ========================================================== 1. a small slip in the README
        body = VGroup(*[label(s, 22, INK) for s in (README_153 + README_157)]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.12)
        body[2].shift(DOWN * 0.15)
        body[3].shift(DOWN * 0.15)
        assert " ".join(README_153) in readme(153) and " ".join(README_157) in readme(157)
        rc = readme_card(153, body, quote=True).move_to([0, 1.25, 0])
        hd = label("· lines 153, 157", CAPTION, S.GREY).move_to(rc.head[1], aligned_edge=LEFT)
        rc.head[1].become(hd)
        er = erratum_tag().next_to(rc.frame, UP, buff=0.12).align_to(rc.frame, RIGHT)
        dns = glyphs(body[1], "reverse DNS lookup")
        prog = glyphs(body[3], "must be done programmatically")
        fix = VGroup(label("reverse DNS lookup", 24, S.GREY), label("→", 24, S.GREY),
                     label("the browser's same-origin rule + a response header", 24, INK)).arrange(RIGHT, buff=0.2)
        fix.move_to([0, -1.35, 0])
        fix_st = strike(fix[0], S.GREY, 3)
        nochip = grey_chip("no CORS editor in the console · gcloud storage buckets update --cors-file also works")
        nochip.move_to([0, -2.35, 0])

        with self.voiceover(SAY[1]) as vo:
            gone = VGroup(og, pk, x, mode, tut, il0)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(rc, shift=UP * 0.2), FadeIn(er), run_time=0.6)
            vo.wait_until("the README blames")
            st = strike(dns, S.GREY, 3)
            self.play(Indicate(dns, color=INK, scale_factor=1.06), run_time=0.5)
            self.play(Create(st), dns.animate.set_color(S.GREY), run_time=0.5)
            vo.wait_until("but the cause")
            self.play(FadeIn(fix[0]), Create(fix_st), run_time=0.4)
            self.play(FadeIn(fix[1], shift=RIGHT * 0.2), FadeIn(fix[2], shift=RIGHT * 0.2), run_time=0.6)
            self.play(Indicate(fix[2], color=INK, scale_factor=1.05), run_time=0.6)
            u = under(prog, S.GREY, stroke=3)
            self.play(Create(u), FadeIn(nochip, shift=UP * 0.15), run_time=0.6)

        # ========================================================== 2. edit line 23, run docker-shell-CLI.sh
        c40, c41 = capture("40"), capture("41")
        p23 = code(CLI_SH, 23).move_to([0, 2.15, 0])
        demo = code_span(p23.code, 0, BUCKET1)
        t = term(P_LABELING, rows=10, size=20)
        ed = on_bar(t, editor_row())
        r165 = readme_card(165, "Run `docker-shell-CLI.sh`", size=20)
        assert "Run `docker-shell-CLI.sh`" in readme(165)
        names = grey_chip("the README names the script")
        top = VGroup(r165, names).arrange(RIGHT, buff=0.3).move_to([0, 2.2, 0])
        ref = lref("13")
        out41 = c41.at(3, "…", (26, 31))
        out41[0] = squash(out41[0])

        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(rc, er, fix, fix_st, st, u, nochip)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(p23, shift=DOWN * 0.15), FadeIn(t), run_time=0.6)
            self.play(demo.animate.set_color(ERR), run_time=0.4)
            self.play(Indicate(demo, color=ERR, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Put your bucket name")
            self.play(FadeIn(ed, shift=LEFT * 0.1), run_time=0.3)
            type_cmd(self, t, c40.cmd, type_time=1.6, soft=True)
            r40 = out(self, t, c40.at((2, 3)), run_time=0.5)
            ph = substring(r40[0], BUCKET)
            self.play(ph.animate.set_color(PASS), run_time=0.4)
            yt1 = beside(turn_row(), r40[0])
            pin(self, r40[0], yt1)
            flash_tag(self, yt1, TURN)
            vo.wait_until("then run it with sh")
            self.play(FadeOut(VGroup(p23, ed)), FadeOut(VGroup(*t.lines)), track(tr, 2), run_time=0.5)
            drop(self, p23, ed, *t.lines)
            for m in list(t.lines):
                t.lines.remove(m)
            self.play(FadeIn(r165, shift=DOWN * 0.15), FadeIn(names, shift=LEFT * 0.15), FadeIn(ref), run_time=0.6)
            ln = type_cmd(self, t, c41.cmd, type_time=0.6)
            r41 = out(self, t, out41, run_time=1.2)
            t.set_prompt(PROMPT_CLI)
            pr = bare_prompt(self, t)
            vo.wait_until("The ID in the prompt")
            pid = substring(pr, "5bf8945fb887")
            dif = beside(row_tag("yours will differ"), pr)
            self.play(Indicate(pid, color=INK, scale_factor=1.1), FadeIn(dif, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("and Apple Silicon")
            arch = r41[3]
            ach = beside(row_tag("aarch64 on Apple Silicon"), arch)
            self.play(Indicate(substring(arch, "x86_64"), color=INK, scale_factor=1.12),
                      FadeIn(ach, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("where this machine says x86")
            v29, v30 = r41[5], r41[6]
            br = Brace(VGroup(v29.strut, v30.strut), RIGHT, buff=0.1, color=S.GREY)
            br.move_to([v30.strut.get_right()[0] + 0.3, (v29.get_center()[1] + v30.get_center()[1]) / 2, 0])
            tm = time_row().next_to(br, RIGHT, buff=0.12)
            self.play(each([substring(v29, "Python 3.12.15"), substring(v30, "uv 0.13.5")], INK, scale=1.08, lag=0.3),
                      GrowFromCenter(br), FadeIn(tm, shift=LEFT * 0.1), run_time=0.9)
            vo.wait_until("Pause and do both")
            marks = VGroup(dif, ach, br, tm, r165, names)
            self.play(FadeOut(marks), run_time=0.4)
            drop(self, marks)
            resize(self, t, 3, run_time=0.6)
            m = PipelineMap.at("S06")
            self.play(FadeIn(m), run_time=0.6)
            self.play(m.light("cli"), run_time=0.7)
            yt2 = on_bar(t, turn_row())
            self.play(FadeIn(yt2, shift=LEFT * 0.1), run_time=0.3)
            flash_tag(self, yt2, TURN)

        # ========================================================== 3. same street, a name, the folder name
        sm = StationMap(laid=True, lit=("studio", "cli"))
        pn = code(CLI_SH, 15, 25, cuts={20: '"/secrets/'}).move_to([0, 0.2, 0])
        b17 = line_bar(pn.code, 17 - 15, ROUTE, 0.28)
        b19 = line_bar(pn.code, 19 - 15, TURN, 0.22)
        b24 = line_bar(pn.code, 24 - 15, TURN, 0.22)
        ch24 = grey_chip("a name, not localhost · scene 7")
        ch19 = grey_chip("mounted by folder name · keep it data-labeling")
        chips = VGroup(ch24, ch19).arrange(RIGHT, buff=0.4).next_to(pn, DOWN, buff=0.22)

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(m, t, yt2)
            self.play(FadeOut(gone), FadeOut(VGroup(*t.lines)), run_time=0.5)
            drop(self, gone, *t.lines)
            self.play(FadeIn(sm), run_time=0.6)
            vo.wait_until("joins the same street")
            self.play(sm.join_cli(), run_time=0.8)
            self.play(Indicate(sm.street.text, color=ROUTE, scale_factor=1.08), run_time=0.6)
            vo.wait_until("and calls Label Studio by name")
            self.play(FadeOut(sm), FadeOut(sm.cli), run_time=0.4)
            drop(self, sm, sm.cli)
            self.play(FadeIn(pn, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(b17), Indicate(code_span(pn.code, 2, NETWORK), color=ROUTE, scale_factor=1.05),
                      run_time=0.6)
            self.play(FadeIn(b24), FadeIn(ch24, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(code_span(pn.code, 9, "data-label-studio"), color=TURN, scale_factor=1.08),
                      run_time=0.6)
            vo.wait_until("It mounts the repo")
            self.play(FadeIn(b19), FadeIn(ch19, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(code_span(pn.code, 4, "../data-labeling"), color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("so keep that name")
            self.play(Indicate(ch19.text, color=INK, scale_factor=1.05), run_time=0.6)

        # ========================================================== 4. cli.py -c, -m: ADC looks for the key
        t4 = term(PROMPT_CLI, rows=12)
        o_c = c41.at((33, 34), "…", (65, 66))
        o_m = c41.at((68, 69), "…", (100, 101))
        p1 = code(CLI_PY, 22, 33, cuts={30: '"Content-Type",'}).move_to([0, 0.35, 0])
        p2 = code(CLI_PY, 23, 34, cuts={30: '"Content-Type",'})
        p2.move_to(p1)
        adc = grey_chip("no key path · ADC, as in L10").next_to(p1, DOWN, buff=0.22)

        def bars(p, first, k23, rule_from, rule_to, k34=None):
            bs = [line_bar(p.code, k23, TURN, 0.22)]
            bs += [line_bar(p.code, k, PASS, 0.16) for k in range(rule_from - first, rule_to - first + 1)]
            if k34 is not None:
                bs.append(line_bar(p.code, k34, TURN, 0.22))
            return bs

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(pn, b17, b19, b24, chips)
            self.play(FadeOut(gone), FadeIn(t4), track(tr, 3), run_time=0.6)
            drop(self, gone)
            l_c = istep(self, t4, c41.line(32), type_time=0.5)
            rc_ = out(self, t4, o_c, wrap=True, run_time=0.8)
            yc = beside(turn_row(), l_c)
            pin(self, l_c, yc)
            vo.wait_until("then dash m")
            unpin(self, l_c, yc)
            self.play(track(tr, 4), run_time=0.4)
            l_m = istep(self, t4, c41.line(67), type_time=0.5)
            rm_ = out(self, t4, o_m, wrap=True, run_time=0.8)
            ym = beside(turn_row(), l_m)
            pin(self, l_m, ym)
            vo.wait_until("pause and run them")
            flash_tag(self, ym, TURN)
            vo.wait_until("Here both stop")
            err_c, err_m = rc_[-2:], rm_[-2:]
            self.play(VGroup(*err_c, *err_m).animate.set_color(ERR), run_time=0.5)
            vo.wait_until("file not found")
            self.play(each([substring(err_c[-1], "was not found."), substring(err_m[-1], "was not found.")], ERR,
                           scale=1.08, lag=0.3), run_time=0.8)
            vo.wait_until("because ADC looks for the key")
            gone = VGroup(t4)
            self.play(FadeOut(gone), FadeOut(VGroup(*t4.lines)), run_time=0.5)
            drop(self, t4, *t4.lines)
            bs1 = bars(p1, 22, 1, 26, 33)
            self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(bs1[0]), FadeIn(adc, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(code_span(p1.code, 1, "storage.Client()"), color=TURN, scale_factor=1.06),
                      run_time=0.6)
            vo.wait_until("The code builds one rule")
            self.play(LaggedStart(*[FadeIn(b) for b in bs1[1:]], lag_ratio=0.1), run_time=0.7)
            vo.wait_until("any origin")
            self.play(Indicate(code_span(p1.code, 28 - 22, '"*"'), color=PASS, scale_factor=1.25), run_time=0.5)
            vo.wait_until("GET only")
            self.play(Indicate(code_span(p1.code, 29 - 22, '"GET"'), color=PASS, scale_factor=1.2), run_time=0.5)
            vo.wait_until("max age one hour")
            self.play(Indicate(code_span(p1.code, 31 - 22, "3600"), color=PASS, scale_factor=1.25), run_time=0.5)
            vo.wait_until("and patches the bucket")
            bs2 = bars(p2, 23, 0, 26, 33, 11)
            pitch = p1.code.code_lines[1].get_center()[1] - p1.code.code_lines[2].get_center()[1]
            self.play(FadeOut(VGroup(p1, *bs1), shift=UP * pitch), FadeIn(VGroup(p2, *bs2[:-1]), shift=UP * pitch),
                      run_time=0.6)
            drop(self, p1, *bs1)
            self.play(FadeIn(bs2[-1]), Indicate(code_span(p2.code, 11, "bucket.patch()"), color=TURN,
                                                 scale_factor=1.08), run_time=0.7)

        # ========================================================== 5. with a real key; the header arrives
        k1 = mono_card(REC_CORS)
        k2 = mono_card(REC_META, colours={4: TURN})
        k1.move_to([0, 1.55, 0])
        k2.next_to(k1, DOWN, buff=0.5).align_to(k1, LEFT)
        g1 = recorded_tag("recorded · cli.py:40 + :26–33").next_to(k1, UP, buff=0.1).align_to(k1, RIGHT)
        g2 = recorded_tag("recorded · cli.py:47–72").move_to(k2).align_to(k1, RIGHT).align_to(k2, UP)
        og2 = OriginGate()
        rule = og2.rule()
        il5 = ill_tag(og2)

        with self.voiceover(SAY[5]) as vo:
            gone = VGroup(p2, *bs2, adc, ref)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            vo.wait_until("dash c prints the rule")
            self.play(FadeIn(k1, shift=UP * 0.2), FadeIn(g1), run_time=0.6)
            self.play(Indicate(k1.rows[1], color=INK, scale_factor=1.03), run_time=0.6)
            vo.wait_until("and dash m prints")
            self.play(FadeIn(k2, shift=UP * 0.2), FadeIn(g2), run_time=0.6)
            self.play(Indicate(k2.rows[4], color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("Now the header arrives")
            gone = VGroup(k1, k2, g1, g2)
            self.play(FadeOut(gone), run_time=0.4)
            drop(self, gone)
            self.play(FadeIn(og2), FadeIn(il5), FadeIn(rule, shift=UP * 0.2), run_time=0.6)
            og2.stick(self, rule, run_time=0.8)
            pk2, ck = og2.deliver(self, header=True)
            vo.wait_until("The max age")
            pf = og2.preflight()
            self.play(Create(pf.line), FadeIn(pf.knock), run_time=0.7)
            self.play(FadeIn(pf.max_age, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("which a plain image request")
            self.play(FadeIn(pf.caption, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(pf.caption, color=INK, scale_factor=1.05), run_time=0.6)

        # ========================================================== 6. Ponder: still broken?
        bp = broken_page()
        ill = illustration_tag().next_to(bp.win, DOWN, buff=0.2).align_to(bp.win, RIGHT)

        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(og2, pk2, ck, pf, rule, il5)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(bp.win), FadeIn(ill), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in bp.grid], lag_ratio=0.1), run_time=0.8)
            vo.wait_until("still broken")
            self.play(each(list(bp.grid[:4]), ERR, scale=1.12, lag=0.15), run_time=0.8)
        pc = ponder(self, PONDER_Q, seconds=8, center=(0, -0.55))

        # ========================================================== 7. two suspects; curl never met a bouncer
        s1 = label("suspect 1 · the rule missed your bucket", 24, TURN)
        s1.move_to([6.5 - s1.width / 2, 3.25, 0])
        s2 = label("suspect 2 · cached answers", 24, TURN).move_to(s1, aligned_edge=RIGHT)
        q23 = code(CLI_SH, 23).move_to([0, 1.6, 0])
        e66 = VGroup(*[mono(x if isinstance(x, str) else x[0], 20, ERR) for x in soft([capture("41").line(66)], 66)])
        e66.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(q23, DOWN, buff=0.45)
        untouched = grey_chip("an untouched README name fails outright: not your bucket").next_to(e66, DOWN, buff=0.4)
        og3 = OriginGate()
        ob = og3.other_bucket()
        rule3 = og3.rule().move_to(og3.slot)
        il7 = ill_tag(og3)
        chk = grey_chip("check with python cli.py -m").move_to([-2.3, -2.75, 0])
        ra = refresh_arrow().move_to(og3.page.content).shift(LEFT * 1.3)
        hard = grey_chip("hard refresh · or a private window").move_to([0, -2.75, 0])
        nac = grey_chip("CORS is not access control · no signed URL → still refused").move_to([0.8, -3.2, 0])

        with self.voiceover(SAY[7]) as vo:
            gone = VGroup(pc, bp, ill)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(s1, shift=LEFT * 0.2), FadeIn(q23, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(code_span(q23.code, 0, BUCKET1), color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Dash c failed")
            self.play(FadeIn(e66, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(e66, color=ERR, scale_factor=1.04), FadeIn(untouched, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("or line 23 names")
            gone = VGroup(q23, e66, untouched)
            self.play(FadeOut(gone), run_time=0.4)
            drop(self, gone)
            self.play(FadeIn(og3), FadeIn(il7), FadeIn(rule3), FadeIn(ob, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("another bucket of yours")
            self.play(rule3.animate.move_to(ob.slot), run_time=1.0)
            self.play(Indicate(og3.slot, color=TURN, scale_factor=1.05), run_time=0.5)
            vo.wait_until("dash m shows")
            self.play(FadeIn(chk, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(chk.text, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Two: your browser")
            gone = VGroup(ob, rule3, chk)
            self.play(FadeOut(gone), FadeTransform(s1, s2), run_time=0.6)
            drop(self, gone)
            self.play(Create(ra), run_time=0.6)
            vo.wait_until("hard refresh")
            self.play(Rotate(ra, angle=-2 * PI), FadeIn(hard, shift=UP * 0.15), run_time=0.9)
            vo.wait_until("And curl never met")
            self.play(FadeOut(VGroup(ra, hard, s2)), run_time=0.4)
            drop(self, ra, hard, s2)
            fig = og3.curl_walk(self, run_time=2.0)
            vo.wait_until("CORS is a browser rule")
            self.play(FadeIn(nac, shift=UP * 0.15), Indicate(og3.bouncer, color=INK, scale_factor=1.1), run_time=0.7)
            self.play(Indicate(nac.text, color=INK, scale_factor=1.05), run_time=0.7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
