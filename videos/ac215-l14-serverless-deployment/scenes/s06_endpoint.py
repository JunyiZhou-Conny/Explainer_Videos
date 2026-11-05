"""S06 · Call it with a query string — tracker [1.3] 1 → 5, then the gcloud alternative; lecture
slides 11, then 16.

Beats (script.md "## S06"; one voiceover block each):
0. TRACKER [1.3] 1 appears. CONSOLE(README:156-157) "service details" with the elided
   `https://translate-function-…run.app` URL (tag `illustration`), its copy icon pulses; beside it
   a GREY-dashed "build details" page with a RED "not here" chip.
1. TRACKER [1.3] 2. The URL flies into a browser bar (`illustration`, no query string);
   RECORDED(part1:3) "Default request: English → Spanish (Bienvenido a AC215)", `recorded ·
   function GIF`. A 4-row strip `laptop · second tab` (TRACKER 2 · extra · local stand-in) types
   the dev/23 curl → TERM(dev/23: 2–3); recording and stand-in flash together on "agrees".
2. TRACKER [1.3] 3, LECTURE 14 · 11. V4 QueryToArgs: the README:163 query string types after the
   URL (PINK); the '?' flashes on "question mark", the string splits at '?' and '&' on
   "ampersands", '%20' melts into spaces on "percent 20"; the three pairs fly into
   CODE(main.py: 9–12) and each default greys out.
3. RECORDED(part1:5) "Bonjour à tous" (`recorded · README:182-183`); the handler shrinks to line 12
   inside a dashed "Google Cloud" outline with an ORANGE arrow to googletrans' public endpoint.
   Strip (TRACKER 3 · extra · local stand-in): dev/25 → 2; TRACKER 4: dev/26, 27, 28 (only the
   dest= value PINK; el at normal speed, hi and zh-cn at 0.6 s a row), an ORANGE pulse out and
   back with each answer; `▶ your turn` beside the last answer.
4. README card (lines 171–173), the checkpoint; on "languages" a GREY `src=en` chip beside a
   struck-through BLUE region pin.
5. TRACKER [1.3] 5. CONSOLE "Observability → Logs" (`illustration`): a log list, one row lit
   (GET 200 · …dest=fr); RECORDED(part1:10), `recorded · function GIF`; the where-to-look card
   returns (slot 1 from S05), slot 2 fills "the service logs".
6. TRACKER 5 · extra · local stand-in. Strip `laptop · second tab`, GREY chip "our first
   recording run · kept on purpose": the zh-cn curl → TERM(dev/provider-timeout/28: 2 wrap) RED.
   The client strip transforms into the server terminal `laptop · dev shell`:
   TERM(dev/provider-timeout/22: 2, …, 25–26, …, 82); line 25's `main.py", line 12, in hello_http`
   YELLOW with a mini main.py line 12 above it as its target; line 82's ReadTimeout RED; GREEN
   chip "retried: 大家下午好" (dev/28: 2).
7. README card (lines 226–229); the handler and the ORANGE arrow to googletrans' endpoint return
   and flash; chips "unofficial", "not Google Cloud's API", "not yours · can rate-limit or change".
8. TRACKER [1.3] 1 · gcloud alternative · replaces 1.1–1.2. Full-width `laptop · gcloud`
   terminal, GREY chip "README:189 · Equivalent gcloud commands …". The deploy box
   (README:195-198) → TERM(gcloud/05: 5–8) RED; GREY chip "first time: may ask to enable APIs
   or create a repository · answer y" (README:191-192); then (extra row tag) `export
   PROJECT_ID=your-project-id` + the same four lines → TERM(gcloud/18: 6–9) RED; GREEN chip
   "--function = the entry point (gcloud help)" with a GREEN ring on `--function=hello_http`.
9. Types `FUNCTION_URL=$(gcloud run services describe …)` (README:200-201), no output; GREY chip
   "needs your project · stores the URL · no output". The strip `laptop · second tab` (TRACKER 3 ·
   gcloud alternative · extra · local stand-in) types dev/24 (stand-in URL row tagged) →
   TERM(dev/24: 5); V4 in reverse, small: the three --data-urlencode values join into the
   query string.
10. LECTURE 14 · 16. The dev shell's server terminal gets `^C` (dev/22: 2), types `cd ../..`
   (extra) and the prompt returns to ~/serverless-deployment. README card (lines 219–223, "More
   detail"); a tiny V2 preview: a dashed instance blinks on at a pulse after a gap, with a grey
   cold-start puff. Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _poly, _soft_fold

SAY = NARRATION["S06"]

HANDLER_CUT = {12: "translate("}          # line 12 cut after 'translate(' (house '…')
TAB_ROWS = 4


# ------------------------------------------------------------------ local helpers
def copy_icon(s: float = 0.22, color=S.GREY) -> VGroup:
    """Two overlapping rounded sheets: the console's copy button (text-free)."""
    a = RoundedRectangle(width=s, height=s * 1.25, corner_radius=0.03, stroke_color=color, stroke_width=2.5)
    b = a.copy().shift(RIGHT * 0.08 + DOWN * 0.08).set_fill(PANEL, 1)
    return VGroup(a, b)


def build_page() -> VGroup:
    """A GREY-dashed 'build details' page (schematic: a title and text-free bars). .title"""
    fr = outline_box(3.0, 2.2, S.GREY, solid=False)
    t = label("build details", 22, S.GREY).move_to(fr.get_top() + DOWN * 0.38)
    bars = VGroup(*[Rectangle(width=w, height=0.12, stroke_width=0).set_fill(S.GREY_DARK, 1)
                    for w in (2.3, 1.7, 2.0, 1.3)]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    bars.next_to(t, DOWN, buff=0.32)
    g = VGroup(fr, t, bars)
    g.title = t
    return g


def logs_panel(panel_w: float = 6.2) -> VGroup:
    """CONSOLE 'Observability → Logs' (README:168-169): a schematic log list, text-free rows except
    the lit one (GET 200 of the French query). .lit"""
    rows = VGroup()
    lit = None
    for k in range(5):
        stamp = Rectangle(width=1.0, height=0.12, stroke_width=0).set_fill(S.GREY_DARK, 1)
        if k == 2:
            body = VGroup(mono("GET", 20, INK), mono("200", 20, OWN), mono("…&dest=fr", 20, ROUTE))
            body.arrange(RIGHT, buff=0.22)
        else:
            body = Rectangle(width=[2.6, 3.2, 1.0, 2.2, 2.9][k], height=0.12, stroke_width=0).set_fill(S.GREY_DARK, 1)
        r = VGroup(stamp, body).arrange(RIGHT, buff=0.3)
        rows.add(r)
        if k == 2:
            lit = r
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    title = label("Observability → Logs", 22, INK)
    inner = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    fr = RoundedRectangle(width=panel_w, height=inner.height + 0.6, corner_radius=0.14,
                          stroke_color=S.GREY_DARK, stroke_width=2).set_fill(PANEL, 1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    bar = Rectangle(width=panel_w - 0.3, height=lit.height + 0.16, stroke_width=0).set_fill(TURN, 0)
    bar.move_to([fr.get_center()[0], lit.get_center()[1], 0])
    g = VGroup(fr, bar, inner)
    g.lit, g.bar, g.frame = lit, bar, fr
    return g


def bar_tag(t: Terminal, kind="local stand-in") -> VGroup:
    """The row-sized 'extra · …' tag on terminal t's title bar, drawn above the terminal (z 3), so
    re-seating the terminal with self.add(t) never hides it."""
    return on_bar(t, extra_row(kind)).set_z_index(3)


def preset_cmd(t: Terminal, cmd: str, soft: bool = True):
    """Place an already-typed command on terminal t without animation (the server that has been
    running since S05): soft-wrapped at the row edge like a real terminal. Returns its rows."""
    p = t.prompt + " "
    texts = _soft_fold(t)(p + cmd) if soft else t.fold(p + cmd, first_prefix=len(p))
    rows = []
    for k, s in enumerate(texts):
        ln = mono_line(s, t.size, INK, t2c=t._prompt_colors(t.prompt) if k == 0 else None)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        rows.append(ln)
    return rows


def dest_value(line) -> VGroup:
    """The glyphs of the dest= value in a typed curl row (the last row of a soft-wrapped command)."""
    row = rows_of(line)[-1]
    i = row.text.rfind("dest=") + len("dest=")
    j = row.text.index("'", i)
    return glyph_range(row, i, j)


def handler_panel():
    """main.py line 12, dedented and cut after 'translate(' (the handler's call)."""
    return code("tutorial/function/main.py", 12, 12, font_size=20, dedent=True, cuts=HANDLER_CUT)


class CallTheEndpoint(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S06"] == 11, len(SAY)

        # ========================================================== 0. copy the URL
        tr = tracker_13(1)
        form = console_form(f"{FUNCTION} · service details", [("URL", FUNCTION_URL)], form_w=9.2)
        form.move_to([-1.75, 0.9, 0])
        field = form.rows[0].field
        cp = copy_icon().next_to(form.rows[0].value, RIGHT, buff=0.3)
        ill = illustration_tag().next_to(form.frame, DOWN, buff=0.15).align_to(form.frame, LEFT)
        bp = build_page().move_to([4.85, 0.9, 0])
        nh = err_chip("not here", mono_font=False).next_to(bp, DOWN, buff=0.2)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), run_time=0.6)
            vo.wait_until("in service details")
            self.play(FadeIn(form, shift=UP * 0.15), FadeIn(cp), FadeIn(ill), run_time=0.7)
            vo.wait_until("copy the URL")
            rg = ring(field, TURN, buff=0.06)
            self.play(Create(rg), run_time=0.5)
            self.play(Indicate(cp, color=TURN, scale_factor=1.4), run_time=0.7)
            self.play(Indicate(cp, color=TURN, scale_factor=1.4), run_time=0.7)
            vo.wait_until("the build page")
            self.play(FadeIn(bp, shift=LEFT * 0.2), run_time=0.6)
            self.play(FadeIn(nh, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(nh.text, color=ERR, scale_factor=1.12), run_time=0.7)

        # ========================================================== 1. default call
        bw = browser_window(FUNCTION_URL, width=8.6, height=0.95).move_to([-1.9, 2.15, 0])
        bill = illustration_tag().next_to(bw.frame, RIGHT, buff=0.25)
        rec3 = recorded_card("part1-function-recorded", 3, "function GIF").move_to([-1.0, 0.45, 0])
        rec3.align_to(bw.frame, LEFT)
        c23 = capture("dev/23")
        tab = tab_term(TAB_ROWS, P_FUNC)
        xtab = bar_tag(tab)
        with self.voiceover(SAY[1]) as vo:
            url_copy = form.rows[0].value.copy()
            self.add(url_copy)
            self.play(FadeOut(VGroup(bp, nh, ill, rg, cp)), FadeOut(form), track(tr, 2), run_time=0.5)
            self.play(FadeIn(VGroup(bw.frame, bw[1], bw[2], bw[3])), FadeIn(bill),
                      ReplacementTransform(url_copy, bw.address), run_time=0.9)
            self.remove(bw.address)
            self.add(bw)
            vo.wait_until("the README's recording")
            self.play(FadeIn(rec3, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Bienvenido")
            self.play(Indicate(rec3.body, color=TURN, scale_factor=1.05), run_time=0.8)
            vo.wait_until("Our local stand-in")
            self.play(FadeIn(tab, shift=UP * 0.2), FadeIn(xtab), track(tr, 2, "local stand-in"), run_time=0.5)
            type_capture(self, tab, c23, type_time=1.4)
            r23 = out(self, tab, c23.at(2, 3), run_time=0.5)
            vo.wait_until("agrees")
            self.play(Indicate(r23[0], color=TURN, scale_factor=1.1),
                      Indicate(rec3.body, color=TURN, scale_factor=1.05), run_time=0.9)
            self.add(tab)

        # ========================================================== 2. V4: the query string
        q = QueryToArgs(show_query=False)
        panel = code("tutorial/function/main.py", 9, 12, font_size=20).move_to([0, -2.3, 0])
        ref11 = lref("11")
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(rec3, xtab)), FadeOut(tab, shift=DOWN * 0.3), run_time=0.4)
            self.remove(*tab.lines)
            self.play(FadeOut(VGroup(bw.frame, bw[1], bw[2], bw[3], bill)),
                      ReplacementTransform(bw.address, q.base), track(tr, 3), FadeIn(ref11), run_time=0.7)
            self.remove(q.base)
            self.add(q)
            vo.wait_until("append the query string")
            q.type_query(self, run_time=1.6)
            vo.wait_until("The question mark")
            hinge = glyph_range(q.query, 0, 1)
            self.play(Indicate(hinge, color=TURN, scale_factor=1.8), run_time=0.7)
            q.heal(self)
            vo.wait_until("ampersands")
            q.split(self, run_time=1.2, hinge_time=0.6)
            vo.wait_until("and percent 20")
            q.melt(self, run_time=1.0)
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("Each pair fills")
            q.into(self, panel, run_time=2.4)

        # ========================================================== 3. Bonjour, then other languages
        hp = handler_panel().move_to([-3.2, 0.25, 0])
        rec5 = recorded_card("part1-function-recorded", 5, "README:182-183").move_to([-1.5, 2.25, 0])
        c25, c26, c27, c28 = (capture(f"dev/{n}") for n in (25, 26, 27, 28))
        tab = tab_term(TAB_ROWS, P_FUNC)
        xtab = bar_tag(tab)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(q), FadeOut(ref11), ReplacementTransform(panel, hp), FadeIn(rec5, shift=DOWN * 0.15),
                      FadeIn(tab, shift=UP * 0.2), FadeIn(xtab), track(tr, 3, "local stand-in"), run_time=0.8)
            type_cmd(self, tab, c25.cmd, type_time=1.0)
            prov = QueryToArgs(show_query=False)
            prov.remove(prov.base)
            pv = prov.provider(self, hp, cloud_at=(3.6, 0.25), run_time=1.0)
            vo.wait_until("and so does the stand-in")
            r25 = out(self, tab, c25.at(2), run_time=0.3)
            self.play(Indicate(r25[0], color=TURN, scale_factor=1.1),
                      Indicate(rec5.body, color=TURN, scale_factor=1.05), run_time=0.7)
            self.add(tab)
            vo.wait_until("Step 4")
            self.play(track(tr, 4, "local stand-in"), run_time=0.4)

            def ask(cap, tt):
                ln = type_cmd(self, tab, cap.cmd, type_time=tt)
                dot = Dot(radius=0.1, color=SHARED).move_to(pv.out_arrow.get_start())
                self.add(dot)
                self.play(*[g.animate.set_color(ROUTE) for g in dest_value(ln)],
                          MoveAlongPath(dot, Line(pv.out_arrow.get_start(), pv.out_arrow.get_end())),
                          run_time=0.25)
                self.add(tab)
                self.play(MoveAlongPath(dot, Line(pv.back_arrow.get_start(), pv.back_arrow.get_end())),
                          run_time=0.2)
                self.remove(dot)
                return out(self, tab, cap.at(2), run_time=0.3)

            ask(c26, 0.7)
            ask(c27, 0.5)
            r28 = ask(c28, 0.5)
            vo.wait_until("Pause and try")
            yt = beside(turn_row(), r28[0], buff=0.6)
            pin(self, r28[0], yt)
            self.wait(1.2)

        # ========================================================== 4. the checkpoint
        ck = readme_card((171, 173), "Checkpoint: the same endpoint accepts different inputs without a redeploy.\n"
                                     "The question mark begins the query string; ampersands separate its parameters.\n"
                                     "The src and dest parameters identify languages, not cloud regions.",
                         size=22).move_to([0, 1.2, 0])
        sc = grey_chip("src=en", mono_font=True)
        pn = region_pin(REGION, CLOUD)
        VGroup(sc, pn).arrange(RIGHT, buff=1.4).move_to([0, -1.1, 0])
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(rec5, prov, hp, xtab)), FadeOut(tab, shift=DOWN * 0.3), run_time=0.5)
            self.remove(*tab.lines)
            self.play(FadeIn(ck, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("one endpoint")
            self.play(ck.body[0].animate.set_color(TURN), ck.body[1].animate.set_opacity(0.4), run_time=0.6)
            vo.wait_until("no redeploy")
            ul = Underline(VGroup(*ck.body[0][-17:-1]), color=TURN, buff=0.04, stroke_width=3)
            self.play(Create(ul), run_time=0.6)
            vo.wait_until("are languages")
            self.play(ck.body[0].animate.set_color(INK), FadeOut(ul), ck.body[2].animate.set_color(TURN),
                      FadeIn(sc, shift=UP * 0.1), FadeIn(pn, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("not regions")
            st = strike(pn, ERR)
            self.play(Create(st), run_time=0.5)
            self.wait(0.6)

        # ========================================================== 5. the logs
        lp = logs_panel().move_to([-3.25, 0.95, 0])
        lill = illustration_tag().next_to(lp.frame, DOWN, buff=0.12).align_to(lp.frame, LEFT)
        wl = WhereToLook(card_w=5.4).move_to([3.55, 0.95, 0])
        w0 = label("the build and start-up logs", 20, INK).move_to(wl.slots[0]).align_to(wl.slots[0], LEFT)
        w0.shift(RIGHT * 0.2)
        wl.slots[0].frame.set_stroke(TURN)
        wl.add(w0)
        wl.texts[0] = w0
        rec10 = recorded_card("part1-function-recorded", 10, "function GIF").move_to([0, -2.35, 0])
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(ck, sc, pn, st)), track(tr, 5), run_time=0.5)
            vo.wait_until("open Observability")
            self.play(FadeIn(lp, shift=UP * 0.15), FadeIn(lill), run_time=0.7)
            self.play(lp.bar.animate.set_fill(TURN, 0.22), run_time=0.6)
            self.play(Indicate(lp.lit, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("The recording found")
            self.play(FadeIn(rec10, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(wl, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("status 200")
            wl.fill(self, 1, "the service logs", run_time=0.6)
            self.play(wl.glow(1), run_time=0.8)
            self.add(wl)

        # ========================================================== 6. the provider timed out once
        p28 = capture("dev/provider-timeout/28")
        p22 = capture("dev/provider-timeout/22")
        tab = tab_term(6, P_FUNC)
        xtab = bar_tag(tab)
        kc = grey_chip("our first recording run · kept on purpose")
        under_term(tab, kc)
        srv = term(P_FUNC, 10, T_DEV, size=20)
        xsrv = bar_tag(srv)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(lp, lill, rec10, wl)), track(tr, 5, "local stand-in"), run_time=0.5)
            self.play(FadeIn(tab, shift=UP * 0.2), FadeIn(xtab), FadeIn(kc, shift=DOWN * 0.1), run_time=0.5)
            type_cmd(self, tab, p28.cmd, type_time=1.2)
            vo.wait_until("the client got status 500")
            r500 = out(self, tab, p28.at(2), wrap=True, color=ERR, run_time=0.5)
            self.play(Indicate(r500[0], color=ERR, scale_factor=1.05), run_time=0.7)
            self.add(tab)
            vo.wait_until("and the server log")
            self.play(FadeOut(tab.lines), FadeOut(kc), FadeOut(xtab), run_time=0.3)
            self.remove(*tab.lines)
            shell_old = VGroup(tab.box, tab.bar, tab.dots, tab.title)
            shell_new = VGroup(srv.box, srv.bar, srv.dots, srv.title)
            self.remove(tab)
            self.add(shell_old)
            self.play(ReplacementTransform(shell_old, shell_new), run_time=0.7)
            self.remove(shell_new, *shell_new)
            self.add(srv)
            cmd_rows = preset_cmd(srv, p22.cmd)
            self.play(*[FadeIn(r) for r in cmd_rows], FadeIn(xsrv), run_time=0.4)
            self.add(srv)
            items = [p22.line(2), "…", p22.line(25), p22.line(26), "…", p22.line(82)]
            rows = srv.print(self, items, wrap=True, run_time=0.8, lag=0.1)
            vo.wait_until("showed the timeout")
            r82 = rows[-1]
            self.play(*[g.animate.set_color(ERR) for g in substring(r82, "ReadTimeout")], run_time=0.5)
            self.add(srv)
            vo.wait_until("raised from line 12")
            r25a = next(r for r in rows if r.text.startswith('  File "/home/student/serverless'))
            r25b = rows[list(rows).index(r25a) + 1]
            yel = list(substring(r25a, 'main.py",')) + list(r25b.glyphs)
            self.play(*[g.animate.set_color(TURN) for g in yel], run_time=0.5)
            self.add(srv)
            mini = handler_panel()
            mini.move_to([-5.95 + mini.width / 2, 1.95, 0])
            l12 = substring(r25b, "line 12")
            xo = srv.box.get_left()[0] - 0.2
            ar = _poly([l12.get_left() + LEFT * 0.08, [xo, l12.get_center()[1], 0],
                        [xo, mini.get_center()[1], 0], [mini.get_left()[0] - 0.04, mini.get_center()[1], 0]],
                       TURN, stroke=3)
            self.play(FadeIn(mini, shift=DOWN * 0.1), Create(ar.line), run_time=0.7)
            self.play(FadeIn(ar.tip_arrow), run_time=0.2)
            mb = line_bar(mini.code, 0, TURN, opacity=0.22)
            self.play(FadeIn(mb), run_time=0.6)
            vo.wait_until("A retry soon after")
            rt = ok_chip("retried: " + capture("dev/28").at(2)[0]).move_to([3.4, 1.95, 0])
            self.play(FadeIn(rt, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(rt.text, color=OWN, scale_factor=1.08), run_time=0.7)

        # ========================================================== 7. the README warns
        warn = readme_card((226, 229), "\n".join(excerpt("README.md", 226, 229).replace("`", "").split("\n")),
                           size=22).move_to([0, 1.45, 0])
        hp2 = handler_panel().move_to([-3.2, -1.45, 0])
        chips = VGroup(grey_chip("unofficial"), grey_chip("not Google Cloud's API"),
                       grey_chip("not yours · can rate-limit or change")).arrange(RIGHT, buff=0.3)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(srv, xsrv, mini, mb, ar, rt)), track(tr, 5), run_time=0.5)
            self.remove(*srv.lines)
            self.play(FadeIn(warn, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the googletrans library")
            self.play(FadeIn(hp2), run_time=0.4)
            prov = QueryToArgs(show_query=False)
            prov.remove(prov.base)
            pv = prov.provider(self, hp2, cloud_at=(3.5, -1.45), run_time=1.2)
            chips.next_to(pv.cloud, DOWN, buff=0.35)
            chips.set_x(0)
            keep_inside(chips)
            vo.wait_until("an unofficial outside service")
            self.play(Indicate(pv.out_arrow, color=SHARED, scale_factor=1.15),
                      Indicate(pv.cloud.shape, color=SHARED, scale_factor=1.06), run_time=0.8)
            prov.heal(self)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.35), run_time=1.2)
            vo.wait_until("so check the logs")
            self.play(Indicate(warn.body[2], color=TURN, scale_factor=1.03),
                      Indicate(warn.body[3], color=TURN, scale_factor=1.03), run_time=1.0)

        # ========================================================== 8. the gcloud alternative: deploy
        gt = term(P_REPO, 10, T_GCLOUD, size=20)
        hc = grey_chip("README:189 · Equivalent gcloud commands — deploy and call the function")
        hc.move_to([gt.box.get_right()[0] - hc.width / 2, 2.4, 0])
        slot2 = np.array([gt.box.get_right()[0], 1.55, 0])
        c05, c18 = capture("gcloud/05"), capture("gcloud/18")
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(warn, prov, hp2, chips)),
                      track(tr, 1, "gcloud alternative · replaces 1.1–1.2"), run_time=0.6)
            self.play(FadeIn(gt, shift=UP * 0.2), FadeIn(hc, shift=DOWN * 0.1), run_time=0.5)
            type_capture(self, gt, c05, type_time=0.55)
            fn_line = gt.find("--function=hello_http")
            vo.wait_until("In a new project")
            fc = grey_chip("first time: may ask to enable APIs or create a repository · answer y")
            fc.move_to(slot2 + LEFT * fc.width / 2)
            self.play(FadeIn(fc, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("answer yes")
            self.play(Indicate(fc.text, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("With the placeholder")
            out(self, gt, [(s, ERR) for s in c05.at(5, 6, 8)], wrap=True, run_time=0.6)
            fnc = ok_chip("--function = the entry point (gcloud help)")
            fnc.move_to(slot2 + LEFT * fnc.width / 2)
            fspan = substring(fn_line, "--function=hello_http")
            frg = ring(fspan, OWN, buff=0.05)
            self.play(FadeOut(fc), run_time=0.3)
            self.play(FadeIn(fnc, shift=DOWN * 0.1), Create(frg), run_time=0.5)
            vo.wait_until("with a real-format ID")
            self.play(FadeOut(frg), run_time=0.2)
            gt.clear(self, run_time=0.3)          # a fresh screen: the second deploy types without scrolling
            ex = type_cmd(self, gt, c18.cmd_lines[0], type_time=0.4)
            xr = beside(row_tag("extra · a valid-format stand-in, still a placeholder"), ex, buff=0.4)
            pin(self, ex, xr, run_time=0.3)
            type_lines(self, gt, c18.cmd_lines[1:], type_time=0.25)
            vo.wait_until("it asks you to sign in")
            out(self, gt, [(s, ERR) for s in c18.at(6, 7, 9)], wrap=True, run_time=0.6)
            self.play(Indicate(gt.find("gcloud auth login"), color=ERR, scale_factor=1.06), run_time=0.7)
            self.add(gt)

        # ========================================================== 9. store the URL, curl the stand-in
        c24 = capture("dev/24")
        tab = tab_term(7, P_FUNC)                 # 7: the soft-wrapped FUNCTION_URL row stays in view
        xtab = bar_tag(tab)
        with self.voiceover(SAY[9]) as vo:
            type_lines(self, gt, readme_rows(200, 201), type_time=0.6)
            npc = no_panel_chip("needs your project · stores the URL · no output")
            npc.move_to(slot2 + LEFT * npc.width / 2)
            self.play(FadeOut(fnc), run_time=0.3)
            self.play(FadeIn(npc, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("the curl lines")
            self.play(FadeOut(VGroup(npc, hc)), FadeOut(gt, shift=DOWN * 0.3),
                      track(tr, 3, "gcloud · local stand-in"), run_time=0.5)
            self.remove(*gt.lines)
            self.play(FadeIn(tab, shift=UP * 0.2), FadeIn(xtab), run_time=0.4)
            u = type_cmd(self, tab, c24.cmd_lines[0], type_time=0.6, soft=True)  # a real terminal soft-wraps; never fold inside FUNCTION_URL
            ut = beside(row_tag("stand-in URL"), u, buff=0.4)
            pin(self, u, ut)
            typed = type_lines(self, tab, c24.cmd_lines[1:], type_time=0.4)
            # V4 in reverse, small: the three --data-urlencode values join into one query string
            texts = ("text=Good afternoon everyone", "src=en", "dest=fr")
            vals = [substring(typed[1], texts[0]), substring(typed[2], texts[1]), substring(typed[2], texts[2])]
            pairs = [mono_line(v, 22, ROUTE) for v in texts]
            for k, pl in enumerate(pairs):
                pl.shift(np.array([-6.2, 2.0 - 0.55 * k, 0]) - pl.strut.get_left())
            cps = [VGroup(*[g.copy() for g in v]) for v in vals]
            self.add(*cps)
            self.play(*[Transform(c, VGroup(*p.glyphs)) for c, p in zip(cps, pairs)], run_time=0.6)
            self.remove(*cps)
            self.add(*pairs)
            qline = mono_line(QUERY, 22, ROUTE)
            qline.shift(np.array([-6.2, 1.45, 0]) - qline.strut.get_left())
            moves, used = [], set()
            for pl, v in zip(pairs, texts):
                enc = v.replace(" ", "%20")
                o = QUERY.index(enc)
                i_src, j = 0, 0
                for ch in v:                      # walk the decoded pair against its encoded form
                    if ch == " ":
                        j += 3
                        continue
                    g_dst = glyph_range(qline, o + j, o + j + 1)[0]
                    moves.append(ReplacementTransform(pl.glyphs[i_src], g_dst))
                    used.add(id(g_dst))
                    i_src += 1
                    j += 1
            rest = [g for g in qline.glyphs if id(g) not in used]
            self.play(*moves, *[FadeIn(g, scale=0.6) for g in rest], run_time=0.8)
            self.remove(*pairs)
            self.add(qline)
            vo.wait_until("and answered")
            r24 = out(self, tab, c24.at(5), run_time=0.4)
            self.play(Indicate(r24[0], color=TURN, scale_factor=1.1), run_time=0.7)
            self.add(tab)

        # ========================================================== 10. More detail: cold starts
        ref16 = lref("16")
        srv = term(P_FUNC, 5, T_DEV, size=20)
        c22 = capture("dev/22")
        preset_cmd(srv, c22.cmd)
        md = readme_card((219, 223), "A cold start initializes an instance of the built application;\n"
                                     "it does not necessarily boot a new VM dedicated to your request.\n"
                                     "…\n"
                                     "There is no fixed inactivity interval to rely on as a\n"
                                     "prediction of the next cold start.", size=22)
        md.shift(np.array([-6.5 - md.get_left()[0], 2.75 - md.get_top()[1], 0]))
        mdh = label("More detail", 20, S.GREY).next_to(md.head, RIGHT, buff=0.25)
        # tiny V2 preview, right of the card
        x0, x1, yax = md.get_right()[0] + 0.45, 6.3, 0.15
        axis = Line([x0, yax, 0], [x1, yax, 0], color=S.GREY, stroke_width=2)
        tl = label("time", 20, S.GREY).next_to(axis, DOWN, buff=0.1).align_to(axis, RIGHT)
        p1x, p2x = x0 + 0.5, x1 - 0.6
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(tab, xtab, qline)), track(tr, 5, "local stand-in"),
                      FadeIn(ref16), run_time=0.5)
            self.remove(*tab.lines)
            self.play(FadeIn(srv, shift=UP * 0.2), run_time=0.4)
            out(self, srv, c22.at(2), run_time=0.3)
            cdl = type_cmd(self, srv, "cd ../..", type_time=0.5)
            cx = beside(extra_row(), cdl, buff=0.2)
            pin(self, cdl, cx)
            cd_prompt(self, srv, P_REPO)
            vo.wait_until("a cold start starts")
            self.play(FadeIn(md, shift=UP * 0.15), FadeIn(mdh), run_time=0.6)
            self.play(Create(axis), FadeIn(tl), run_time=0.5)
            d1 = pulse_dot().move_to([p1x, yax, 0])
            inst1 = instance(0.9, 0.6).next_to(d1, UP, buff=0.25)
            pf = puff(0.16).next_to(inst1, RIGHT, buff=0.12)
            csl = label("cold start", 20, S.GREY).next_to(inst1, UP, buff=0.12)
            self.play(FadeIn(d1, scale=0.5), run_time=0.3)
            self.play(FadeIn(inst1, scale=0.8), FadeIn(pf, scale=0.5), FadeIn(csl), run_time=0.5)
            vo.wait_until("not necessarily a new machine")
            self.play(Indicate(md.body[1], color=TURN, scale_factor=1.03), FadeOut(inst1), FadeOut(pf),
                      FadeOut(csl), run_time=0.9)
            vo.wait_until("No fixed idle time")
            gap = DashedLine([p1x + 0.2, yax + 0.25, 0], [p2x - 0.2, yax + 0.25, 0], color=S.GREY,
                             stroke_width=2)
            qm = label("?", 24, S.GREY).next_to(gap, UP, buff=0.08)
            self.play(Create(gap), FadeIn(qm), Indicate(md.body[3], color=TURN, scale_factor=1.03),
                      run_time=0.9)
            d2 = pulse_dot().move_to([p2x, yax, 0])
            inst2 = instance(0.9, 0.6).next_to(d2, UP, buff=0.25)
            csl2 = csl.copy().next_to(inst2, UP, buff=0.12)
            self.play(FadeIn(d2, scale=0.5), run_time=0.3)
            self.play(FadeIn(inst2, scale=0.8), FadeIn(csl2), run_time=0.5)
            self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
