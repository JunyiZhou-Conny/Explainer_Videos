"""S05 · What runs your function? — tracker [1.2] 4 (no step advances: "under the hood"); lecture
slides 10–11, then 16.

Beats (script.md "## S05"; one voiceover block each):
0. TRACKER [1.2] 4 · under the hood. LECTURE 14 · 10–11. A GREY quote card (slide 11): "without
   managing servers or containers" (tag `erratum`); on "you don't manage them" the word
   "managing" underlines YELLOW; on "builds a container anyway" a TEAL box outline draws itself
   behind the quote.
1. V3 BuildLine: three GREEN inputs (main.py, requirements.txt, entry point: hello_http) slide into
   the PURPLE Cloud Build box (buildpacks · base python312); GREEN stamp "pip install · build time,
   not per request"; a TEAL image drops onto the BLUE Artifact Registry shelf; an arrow from the
   shelf starts the dashed BLUE revision. RECORDED(expected/part1-function-recorded.txt: 12),
   tag `recorded · function GIF`.
2. Zoom into the revision (V3 FunctionInside, `illustration`): PURPLE functions-framework > Flask
   app > gunicorn on a PINK `0.0.0.0:$PORT` ear; a PINK request enters the ear; the GREEN
   `hello_http` name tag's arrow reaches into the GREEN main.py card, finds `def hello_http`, and
   the answer flows back out.
3. Pull back to V1 (from a corner icon): the file · serverless cell's lid lifts, a TEAL box inside
   ("Google built one"); the image on a small Artifact Registry shelf below with a GOLD chip
   "stays after you delete the service · clean up at the end".
4. TRACKER [1.2] 4 · extra · local stand-in. Full-width terminal `laptop · dev shell` (chip "a
   second terminal on the same laptop"): types the dev/20 command → TERM(dev/20: 8–9, …, 14–16);
   types the dev/21 command (folds) → TERM(dev/21: 5–9); GREY versions chip (at the time of
   recording) above the terminal; GREEN row tag "what the build installs".
5. Types `cd tutorial/function` (prompt → …/tutorial/function$), then
   `~/fn-venv/bin/functions-framework --target hello_http`; the terminal stays empty; GREY row tag
   "serving · no log line · log level: error".
6. The terminal shrinks to a strip. V3 static and un-run (Cloud Build dim, no stamp, no image);
   the name tag turns from `hello_http` to `translate` (plain WHITE outline).
   PONDER(8 s) — the question card; nothing moves but the timer.
7. The card leaves. V3 runs: GREEN stamp "requirements installed" + tick, image published, the
   revision starts and turns RED "revision not ready" (GREY chip "README:1038 lists entry point
   under Function build fails"); the `translate` arrow reaches into main.py and snaps RED. Then the
   picture gives way to a `laptop · second tab` terminal (the dev shell still holds the server):
   `timeout 20 ~/fn-venv/bin/functions-framework --target translate` → TERM(dev/29: 2, …, 28 wrap);
   `'translate'` RED and `'hello_http'` GREEN in line 28.
8. The terminal shrinks to line 28; GREY chip "on Cloud Run: /workspace/main.py · in the logs";
   the "where do you look?" card, slot 1 fills "the build and start-up logs". LECTURE 14 · 16.
   Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _poly

SAY = NARRATION["S05"]

PONDER_Q = ("You paste main.py but type translate\nas the entry point. Does the build fail?\n"
            "If not, what fails, and where do you see it?")
VERSIONS = "functions-framework 3.10.2 · Flask 3.1.3 · gunicorn 26.2.0 · at the time of recording"


def quote_card() -> VGroup:
    """Slide 11's phrase on a GREY card. .frame .managing"""
    q = "“without managing servers or containers”"
    words = label(q, 30, INK)
    a = len("“without")                  # glyphs skip spaces: "managing" is glyphs a .. a+8
    c = card([words], head="the lecture, slide 11")
    c.managing = VGroup(*words[a:a + len("managing")])
    return c


def fi_lookup(scene, fi, run_time: float = 2.0):
    """PLAYS: FunctionInside's lookup with the entry tag UNDER the main.py card (its own spot, so it
    covers no box label): the GREEN arrow rises from the tag into `hello_http` of the def line, the
    name lights GREEN, and the answer flows back out of the ear."""
    tgt = substring(fi.card.defline, ENTRY)
    a = arrow(fi.entry.get_top(), tgt.get_bottom(), OWN, stroke=4, buff=0.06)
    fi.show(scene, a, anims=[GrowArrow(a)], run_time=run_time * 0.3)
    scene.play(*[g.animate.set_color(OWN) for g in tgt], run_time=run_time * 0.2)
    fi.heal(scene)
    back = pulse_dot(OWN, r=0.11).move_to(tgt)
    fi.show(scene, back, run_time=0.1)
    if getattr(fi, "dot", None) is not None:          # the request dot parked at gunicorn
        fi.drop(scene, fi.dot, run_time=0.15)
        fi.dot = None
    scene.play(back.animate.move_to(fi.ear.get_left() + LEFT * 0.3), run_time=run_time * 0.4)
    fi.drop(scene, back, run_time=0.2)
    return a


def fail_lookup(scene, b, name: str = "translate", run_time: float = 1.0):
    """PLAYS: the starting revision's lookup arrow (labelled by the entry name) reaches up and over
    into main.py and snaps RED, with a RED cross beside main.py. The route runs ABOVE the build
    line (BuildLine.lookup's route runs under the inputs and crosses the other two cards)."""
    rev, main = b.revision, b.inputs.main
    start = np.array([rev.get_left()[0] + 0.3, rev.get_top()[1] + 0.02, 0])
    y = b.build.frame.get_top()[1] + 0.5
    end = main.get_top() + UP * 0.04
    path = _poly([start, [start[0], y, 0], [end[0], y, 0], end], ERR, stroke=3)
    lab = mono(name, 20, ERR).move_to([(start[0] + end[0]) / 2, y + 0.25, 0])
    b.show(scene, path, lab, anims=[Create(path.line), FadeIn(path.tip_arrow), FadeIn(lab)],
           run_time=run_time * 0.7)
    mk = cross_glyph(0.3).next_to(main, RIGHT, buff=0.15)
    b.show(scene, mk, anims=[Create(mk)], run_time=run_time * 0.3)
    return VGroup(path, lab, mk)


def type_wordwrap(scene, t, cmd: str, type_time: float):
    """PLAYS: type_cmd with a soft wrap at the last space that fits each row (the space stays at the
    row's end, so the rows join back to the exact command, no ' \\'): a path is never cut in two."""
    def fold(text: str, first_prefix: int = 0) -> list[str]:
        n, rows, cur = t.max_chars, [], text
        while len(cur) > n:
            cut = cur.rfind(" ", max(first_prefix - 1, 0) if not rows else 0, n)   # the space after the prompt counts
            cut = n if cut <= 0 else cut + 1
            rows.append(cur[:cut])
            cur = cur[cut:]
        return rows + [cur]
    t.fold = fold
    try:
        ln = type_cmd(scene, t, cmd, type_time=type_time, soft=False)
    finally:
        del t.fold
    if hasattr(ln, "rows"):
        assert "".join(r.text for r in ln.rows) == t.prompt + " " + cmd, "wrap must join back"
    return ln


def low_stamp(scene, b, text: str = "pip install · build time, not per request", run_time: float = 0.5):
    """PLAYS: BuildLine.stamp, but 0.45 under the build box (at the default 0.25 its left end touches
    the corner of the entry-point card)."""
    ch = chip(text, OWN, size=20).next_to(b.build.frame, DOWN, buff=0.45)
    b.stamp_ = ch
    b.show(scene, ch, anims=[FadeIn(ch, scale=1.2)], run_time=run_time)
    return ch


def open_lid_left(scene, g, text: str = "Google built one", run_time: float = 1.2):
    """PLAYS: DeployGrid.open_lid, with the GREY chip LEFT of the cell under its row label (inside the
    cell it covers the top of the dashed instance)."""
    cl = g.cells[1][0]
    inst = cl.glyph[0]
    lid = Line(inst.get_corner(UL), inst.get_corner(UR), color=CLOUD, stroke_width=4)
    box_ = image_block(None, 0.42, 0.32).next_to(cl.what, RIGHT, buff=0.08)
    ch = grey_chip(text).next_to(cl.frame, LEFT, buff=0.2).align_to(cl.frame, DOWN).shift(UP * 0.08)
    g.show(scene, lid, run_time=0.2)
    g.lid = VGroup(box_, ch)
    scene.play(Rotate(lid, angle=0.5, about_point=lid.get_start()), run_time=run_time * 0.4)
    g.show(scene, box_, ch, anims=[GrowFromCenter(box_), FadeIn(ch)], run_time=run_time * 0.4)
    g.drop(scene, lid, run_time=0.2)


class InsideTheFunction(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S05"] == 9, len(SAY)

        # ========================================================== 0. "without managing … containers"
        tr = tracker_12(4, "under the hood")
        ref = lref("10–11")
        qc = quote_card().move_to(UP * 0.3)
        hq = label("What runs your function?", 36, INK).move_to(UP * 2.05)
        er = erratum_tag().next_to(qc.frame, DOWN, buff=0.75).align_to(qc.frame, RIGHT)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), FadeIn(ref), FadeIn(hq, shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(hq, color=INK, scale_factor=1.06), run_time=0.8)
            vo.wait_until("The lecture says")
            self.play(FadeIn(qc, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(er), run_time=0.4)
            vo.wait_until("you don't manage them")
            ul = under(qc.managing, TURN, stroke=5)
            self.play(Create(ul), qc.managing.animate.set_color(TURN), run_time=0.6)
            vo.wait_until("But Google builds")
            tb = RoundedRectangle(width=qc.frame.width + 1.0, height=qc.frame.height + 1.0, corner_radius=0.2,
                                  stroke_color=IMAGE, stroke_width=4).set_fill(IMAGE, 0.06).move_to(qc.frame)
            tb.set_z_index(-1)
            tl = label("container", 22, IMAGE).next_to(tb.get_corner(UL), DR, buff=0.12)
            tl.move_to([tb.get_left()[0] + 0.25 + tl.width / 2, tb.get_top()[1] - 0.3, 0])
            self.play(Create(tb), run_time=1.2)
            self.play(FadeIn(tl, shift=RIGHT * 0.1), run_time=0.4)

        # ========================================================== 1. V3: the build line
        b = BuildLine()
        b.remove(b.revision, b.rev_label)          # the revision appears when Cloud Run starts it
        rec = recorded_card("part1-function-recorded", 12, "function GIF").move_to(DOWN * 2.75)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(hq, qc, er, ul, tb, tl)), run_time=0.5)
            self.play(FadeIn(b), run_time=0.7)
            b.feed(self, run_time=1.3)
            vo.wait_until("It installs the requirements")
            low_stamp(self, b, run_time=0.6)
            vo.wait_until("configures the Functions Framework")
            self.play(Indicate(b.build.frame, color=TOOL, scale_factor=1.05), run_time=0.8)
            b.heal(self)
            vo.wait_until("and publishes an image")
            b.publish(self, run_time=0.9)
            self.play(FadeIn(rec, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Cloud Run starts a revision")
            b.show(self, b.revision, b.rev_label, anims=[Create(b.revision), FadeIn(b.rev_label)], run_time=0.6)
            b.start(self, run_time=0.8)

        # ========================================================== 2. inside the revision
        fi = FunctionInside()
        parts = [fi.framework, fi.flask, fi.gunicorn, fi.ear, fi.wire, fi.entry, fi.card]
        fi.remove(*parts)
        tgt_x = substring(fi.card.defline, ENTRY).get_center()[0]
        fi.entry.next_to(fi.card, DOWN, buff=0.35)
        fi.entry.set_x(tgt_x)
        ill = illustration_tag().next_to(fi.outer, UP, buff=0.1).align_to(fi.outer, RIGHT)
        with self.voiceover(SAY[2]) as vo:
            ghost = b.revision.copy()
            self.add(ghost)
            self.play(FadeOut(b), FadeOut(rec), run_time=0.4)
            self.play(ReplacementTransform(ghost, fi.outer), FadeIn(fi.olabel), FadeIn(ill), run_time=0.9)
            self.remove(fi.outer, fi.olabel)
            self.add(fi)
            vo.wait_until("the Functions Framework runs")
            fi.show(self, fi.framework, anims=[FadeIn(fi.framework, scale=0.96)], run_time=0.6)
            vo.wait_until("a small Flask app")
            fi.show(self, fi.flask, anims=[FadeIn(fi.flask, scale=0.96)], run_time=0.6)
            vo.wait_until("under gunicorn")
            fi.show(self, fi.gunicorn, anims=[FadeIn(fi.gunicorn, scale=0.96)], run_time=0.6)
            vo.wait_until("on every interface")
            fi.show(self, fi.ear, fi.wire, anims=[FadeIn(fi.ear), Create(fi.wire)], run_time=0.6)
            self.play(Indicate(fi.gunicorn.addr, color=ROUTE, scale_factor=1.15), run_time=0.8)
            fi.heal(self)
            vo.wait_until("On each request")
            fi.show(self, fi.card, fi.entry, anims=[FadeIn(fi.card, shift=LEFT * 0.2), FadeIn(fi.entry)],
                    run_time=0.6)
            fi.request(self, run_time=0.8)
            vo.wait_until("it looks up your function")
            fi_lookup(self, fi, run_time=2.0)

        # ========================================================== 3. V1: the file cell has a container
        g = DeployGrid(sketch=False)
        g.move_to(ORIGIN).shift(UP * 0.75)
        icon = grid_icon(0.3).move_to([5.9, -2.8, 0])
        shelf = registry_shelf(True, shelf_w=2.2)
        cell = g.cells[1][0]
        shelf.next_to(cell.frame, DOWN, buff=0.35)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(icon, scale=0.6), run_time=0.4)
            self.play(FadeOut(fi), FadeOut(ill), icon.animate.scale(4).move_to(g.get_center()), run_time=0.8)
            self.play(FadeOut(icon), FadeIn(g), run_time=0.6)
            self.play(g.light(1, 0), run_time=0.5)
            vo.wait_until("has a container inside")
            open_lid_left(self, g, run_time=1.2)
            vo.wait_until("That is why")
            src = g.lid[0]
            ar = arrow(src.get_bottom(), shelf.image.get_top(), IMAGE, buff=0.1)
            self.play(GrowArrow(ar), FadeIn(shelf, shift=DOWN * 0.1), run_time=0.8)
            ct = cost_tag("stays after you delete the service · clean up at the end")
            ct.next_to(shelf, DOWN, buff=0.15)
            keep_inside(ct)
            self.play(FadeIn(ct, shift=LEFT * 0.1), run_time=0.5)

        # ========================================================== 4. the same layer on your laptop
        c20, c21 = capture("dev/20"), capture("dev/21")
        t = dev_term(12)
        ch2 = grey_chip("a second terminal on the same laptop")
        under_term(t, ch2)
        xb = on_bar(t, extra_row("local stand-in"))
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(g, ar, shelf, ct)), FadeOut(ref), track(tr, None, "local stand-in"),
                      run_time=0.6)
            self.play(FadeIn(t), run_time=0.5)
            self.play(FadeIn(ch2, shift=DOWN * 0.1), FadeIn(xb), run_time=0.4)
            type_capture(self, t, c20, type_time=1.4)
            out(self, t, c20.at(8, 9, "…", (14, 16)), run_time=0.6)
            vo.wait_until("The same two pins")
            type_capture(self, t, c21, type_time=1.8)
            rows21 = out(self, t, c21.at((5, 9)), run_time=0.6)
            vo.wait_until("as the build does")
            vch = grey_chip(VERSIONS)
            under_term(t, vch)
            self.play(FadeOut(ch2), FadeIn(vch), run_time=0.4)
            wb = beside(row_tag("what the build installs", OWN), rows21[2], buff=1.0)
            pin(self, rows21[2], wb)

        # ========================================================== 5. start the stand-in: silence
        c22 = capture("dev/22")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(vch), run_time=0.3)
            type_cmd(self, t, "cd tutorial/function", type_time=0.7)
            cd_prompt(self, t, P_FUNC)
            ff = type_wordwrap(self, t, c22.cmd, type_time=1.2)   # wraps at a space: the path stays whole
            vo.wait_until("and it prints nothing")
            cur = Rectangle(width=0.16, height=0.3, stroke_width=0).set_fill(INK, 0.8)
            last = rows_of(ff)[-1]
            cur.move_to([t.box.get_left()[0] + 0.35, last.strut.get_center()[1] - t.pitch, 0])
            self.play(FadeIn(cur), run_time=0.2)
            self.play(cur.animate(rate_func=there_and_back).set_opacity(0.1), run_time=1.0)
            self.play(cur.animate(rate_func=there_and_back).set_opacity(0.1), run_time=1.0)
            vo.wait_until("That silence is normal")
            sv = row_tag("serving · no log line · log level: error")
            sv.move_to([cur.get_right()[0] + 0.4 + sv.width / 2, cur.get_center()[1], 0])
            self.play(FadeIn(sv, shift=LEFT * 0.1), run_time=0.4)
            self.play(cur.animate(rate_func=there_and_back).set_opacity(0.1), run_time=1.0)

        # ========================================================== 6. PONDER: a wrong entry point
        b2 = BuildLine()
        b2.remove(b2.a2)                            # the build has not run: no arrow to the shelf yet
        b2.shift(UP * 1.2)                          # up for the ponder card under it; back to 0.75 in block 7
        b2.build.frame.set_stroke(opacity=0.35).set_fill(opacity=0.04)
        b2.build.text.set_opacity(0.4)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(cur), FadeOut(sv), FadeOut(xb), run_time=0.3)
            resize(self, t, 3, run_time=0.7)
            self.play(FadeIn(b2), run_time=0.7)
            vo.wait_until("type translate")
            b2.set_entry(self, "translate", run_time=0.8)
            vo.wait_until("Does the build fail?")
            self.play(Indicate(b2.inputs.entry.text, color=INK, scale_factor=1.1), run_time=0.8)
            b2.heal(self)
            self.play(FadeOut(t, shift=DOWN * 0.2), run_time=0.4)   # the card sits where the strip was
        pc = ponder(self, PONDER_Q, seconds=8, center=(0, -1.85))

        # ========================================================== 7. the answer
        c29 = capture("dev/29")
        rmc = grey_chip("README:1038 lists entry point under Function build fails")
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(pc), b2.animate.shift(DOWN * 0.45), run_time=0.4)
            self.play(FadeIn(t, shift=UP * 0.2),                  # the dev shell strip, server still running
                      b2.build.frame.animate.set_stroke(opacity=1).set_fill(opacity=0.12),
                      b2.build.text.animate.set_opacity(1), run_time=0.4)
            b2.heal(self)
            b2.feed(self, run_time=1.0)
            st = b2.stamp(self, "requirements installed", run_time=0.5)
            tk = check_glyph(0.28).next_to(st, RIGHT, buff=0.12)
            b2.show(self, tk, anims=[Create(tk)], run_time=0.3)
            b2.show(self, b2.a2, anims=[GrowArrow(b2.a2)], run_time=0.3)
            b2.publish(self, run_time=0.7)
            vo.wait_until("But the deployment fails")
            b2.start(self, run_time=0.6)
            nr = label("revision not ready", 20, ERR).next_to(b2.revision, DOWN, buff=0.15)
            b2.show(self, nr, run_time=0.5, extra=[b2.revision.frame.animate.set_stroke(ERR)])
            rmc.move_to([3.0, -1.12, 0])
            keep_inside(rmc)
            self.play(FadeIn(rmc, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("When the new revision starts")
            fail_lookup(self, b2, run_time=1.2)
            self.wait(0.6)
            t2 = tab_term(8, P_FUNC)
            xb2 = on_bar(t2, extra_row("local stand-in"))
            self.play(FadeOut(VGroup(b2, rmc)), FadeOut(t, shift=DOWN * 0.3), run_time=0.5)
            self.play(FadeIn(t2, shift=UP * 0.2), FadeIn(xb2), run_time=0.5)
            type_wordwrap(self, t2, c29.cmd, type_time=1.3)
            out(self, t2, c29.at(2, "…"), run_time=0.3)
            rows28 = out(self, t2, c29.at(28), wrap=True, run_time=0.5)
            vo.wait_until("a function named translate")
            r_t = next(r for r in rows28 if "'translate'" in r.text)
            self.play(*[gl.animate.set_color(ERR) for gl in substring(r_t, "'translate'")], run_time=0.4)
            self.add(t2, xb2)                       # xb2 last: the title bar would cover it
            vo.wait_until("but it found")
            r_h = next(r for r in rows28 if "'hello_http'" in r.text)
            self.play(*[gl.animate.set_color(OWN) for gl in substring(r_h, "'hello_http'")], run_time=0.4)
            self.add(t2, xb2)

        # ========================================================== 8. where do you look? (1 of 3)
        wl = WhereToLook().move_to([-3.6, 0.95, 0])
        ref16 = lref("16")
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(xb2), run_time=0.2)
            resize(self, t2, 4, run_time=0.6)
            on_bar(t2, xb2)
            oc = grey_chip("on Cloud Run: /workspace/main.py · in the logs")
            under_term(t2, oc)
            self.play(FadeIn(oc, shift=UP * 0.1), FadeIn(xb2), run_time=0.4)
            self.play(FadeIn(wl, shift=RIGHT * 0.2), run_time=0.5)
            wl.fill(self, 0, "the build and start-up logs", run_time=0.6)
            vo.wait_until("That is the first")
            self.play(wl.glow(0), FadeIn(ref16), run_time=0.8)
            self.add(wl)
            self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
