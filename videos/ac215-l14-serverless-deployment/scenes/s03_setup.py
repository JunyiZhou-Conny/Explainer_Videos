"""S03 · Before you begin: project, region, clone — tracker [BB] 1 → 5, no lecture tag (README only).

Beats (script.md "## S03"; one voiceover block each):
0. TRACKER [BB] 1. CONSOLE (README:28-31, `illustration`): a top bar with a project picker; two
   fields side by side, display name "My Course Project" and project ID `YOUR_PROJECT_ID`; on "the
   ID" the ID field rings YELLOW + chip "no spaces · the command boxes need this one". TRACKER [BB] 2:
   four GREY checks (README:32-34) and the GREY chip "restricted? ask course staff first".
1. TRACKER [BB] 3. A plain GREY "regions" line (no map) with two pins: solid BLUE
   `northamerica-northeast2 · Toronto`, dashed BLUE `us-central1 · speech model · part 3`; a GREY
   chip "two different settings" between them.
2. The worksheet (README card, lines 46–55) breaks into seven BLUE name cards along the bottom
   (the two account cards with a badge outline, two blank bucket cards "you choose · part 4"),
   one per spoken name.
3. TRACKER [BB] 4. Full-width terminal `laptop`, prompt `student@laptop:~$`. README card (lines
   38–39) + GREY chip "the README spells no command". `git clone …` (extra: its spelling) →
   laptop/01: 2; `cd serverless-deployment` → no output, the prompt changes; TRACKER [BB] 4 · extra:
   `git log -1 --format='%H %ci %s'` (extra) → laptop/02: 2 (wrapped), the hash head and
   `2026-10-22` YELLOW; ▶ your turn on the title bar.
4. TRACKER [BB] 4 · extra. `ls` (extra) → laptop/03: 2–12; the 2025 root files dim GREY, row tags
   "erratum · don't build this Dockerfile" (Dockerfile row) + "2025 files · the README never uses
   them" (cli.py row; one long chip ran into the panel edge);
   `tutorial` YELLOW. `ls tutorial …` (extra) → laptop/04: 32–34, 13–21; function/'s two files GREEN
   + "part 1", app/'s Dockerfile and translation_demo TEAL + "the image of parts 2–4".
5. TRACKER [BB] 5. Title → `laptop · gcloud`. README card (lines 66–72). TRACKER [BB] 5 · extra:
   `gcloud auth list` (extra) → gcloud/03: 3 GREY. `gcloud auth login` (README:74), no output panel,
   GREY chip "browser sign-in · no output shown". A GREY card "gcloud's own login" with a PURPLE
   gcloud chip; an outlined dashed card "the app's identity · part 3" stays empty.
6. TRACKER [BB] 5. The seven exports (laptop/05 lines 1–7, type_time 0.3 each, to keep up with the words), then the echo
   (extra) → laptop/05: 9–11. `YOUR_PROJECT_ID` of line 1 pulses YELLOW + "put your real project ID
   here"; `${PROJECT_ID}` in lines 6–7 and `YOUR_PROJECT_ID` in the echoed emails turn PINK, joined
   by a PINK thread (a PINK underline that travels from each source to its echoed value). ▶ your turn.
7. The terminal shrinks to a 3-row strip. A GREY card: "This recording machine: no Google account ·
   no project"; three lines write in, one per phrase (gcloud boxes / console `illustration` / cloud
   results `recorded`). Everything fades: empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from explainer import style as S

SAY = NARRATION["S03"]

DISPLAY_NAME = "My Course Project"           # script.md S03 (the README gives no display name)
CHECKS = ("billing enabled", "create Cloud Run resources", "create service accounts", "create buckets")
CLONE = "git clone https://github.com/dlops-io/serverless-deployment.git"
LS_TUTORIAL = "ls tutorial tutorial/function tutorial/app tutorial/app/translation_demo"
ROOT_OLD = ("Dockerfile", "cli.py", "docker-entrypoint.sh", "docker-shell.sh", "main.py", "pyproject.toml",
            "uv.lock")
WS_ROWS = (("Function service", FUNCTION), ("Web service", SERVICE), ("Web runtime account", RUNTIME_SA),
           ("Job", JOB), ("Job runtime account", JOB_SA),
           ("Input bucket", "A globally unique name you choose in part 4"),
           ("Output bucket", "A second globally unique name you choose in part 4"))


# ------------------------------------------------------------------ pictures of this scene
def caret(color=S.GREY, s: float = 0.14) -> Polygon:
    """A small down-pointing triangle (the picker's menu mark)."""
    return Polygon([-s, s * 0.5, 0], [s, s * 0.5, 0], [0, -s * 0.6, 0], stroke_width=0).set_fill(color, 1)


def field(lbl: str, value: str, field_w: float) -> VGroup:
    """A console field: GREY label above a dark input box holding a mono value. .label .box .value"""
    lt = label(lbl, 20, S.GREY)
    vt = mono(value, 22, INK)
    b = RoundedRectangle(width=field_w, height=vt.height + 0.34, corner_radius=0.06, stroke_color=S.GREY_DARK,
                         stroke_width=1.5).set_fill(TERM_BG, 1)
    vt.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.2)
    lt.next_to(b, UP, buff=0.12, aligned_edge=LEFT)
    g = VGroup(lt, b, vt)
    g.label, g.box, g.value = lt, b, vt
    return g


def project_console() -> VGroup:
    """The schematic project selector (README:28-31): top bar with a picker, the two fields side by
    side. .frame .picker .name .pid"""
    frame = RoundedRectangle(width=11.6, height=2.55, corner_radius=0.14, stroke_color=S.GREY_DARK,
                             stroke_width=2).set_fill(PANEL, 1)
    bar_y = frame.get_top()[1] - 0.6
    sep = Line([frame.get_left()[0] + 0.15, bar_y, 0], [frame.get_right()[0] - 0.15, bar_y, 0],
               color=S.GREY_DARK, stroke_width=1.5)
    pk_t = label(DISPLAY_NAME, 20, INK)
    pk_c = caret()
    pk_row = VGroup(pk_t, pk_c).arrange(RIGHT, buff=0.18)
    pk_b = RoundedRectangle(width=pk_row.width + 0.4, height=0.42, corner_radius=0.08, stroke_color=S.GREY,
                            stroke_width=1.5)
    pk_row.move_to(pk_b)
    picker = VGroup(pk_b, pk_row)
    pk_lbl = label("project", 20, S.GREY)
    head = VGroup(pk_lbl, picker).arrange(RIGHT, buff=0.2)
    head.move_to([frame.get_left()[0] + 0.3 + head.width / 2, (frame.get_top()[1] + bar_y) / 2, 0])
    name = field("display name", DISPLAY_NAME, 4.6)
    pid = field("project ID", PROJECT_PH, 4.6)
    VGroup(name, pid).arrange(RIGHT, buff=0.8, aligned_edge=UP)
    VGroup(name, pid).move_to([frame.get_center()[0], (bar_y + frame.get_bottom()[1]) / 2 - 0.02, 0])
    g = VGroup(frame, sep, head, name, pid)
    g.frame, g.picker, g.name, g.pid = frame, picker, name, pid
    return g


def check_row(text: str) -> VGroup:
    """A GREY check + its words (README:32-34)."""
    return VGroup(check_glyph(0.28, S.GREY, 4), label(text, 22, INK)).arrange(RIGHT, buff=0.2)


def worksheet_body() -> VGroup:
    """README:46-55 as a two-column table (settings label font, values mono). .values (the 7 values)"""
    intro = label("Use these names as a worksheet.", 22, INK)
    keys = [label(k, 20, S.GREY) for k, _ in WS_ROWS]
    vals = [mono(v, 20, INK) if "_" in v or "-" in v and " " not in v else label(v, 20, INK) for _, v in WS_ROWS]
    kx = max(k.width for k in keys) + 0.35
    rows = VGroup()
    for k, v in zip(keys, vals):
        v.next_to(k, RIGHT, buff=0).align_to(k, LEFT).shift(RIGHT * kx)
        rows.add(VGroup(k, v))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    for k, v in zip(keys, vals):                      # re-align the value column after arrange
        v.move_to([k.get_left()[0] + kx + v.width / 2, k.get_center()[1], 0])
    body = VGroup(intro, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    body.values = vals
    return body


def identity_card(text: str, icon=None, dashed: bool = False) -> VGroup:
    """S03's two login cards: GREY outline, a line of words, an optional icon left of them."""
    t = label(text, 22, INK if not dashed else S.GREY)
    inner = VGroup(icon, t).arrange(RIGHT, buff=0.25) if icon is not None else VGroup(t)
    fr = outline_box(inner.width + 0.6, 0.8, S.GREY, solid=not dashed, fill_opacity=0.08)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.text = fr, t
    return g


def recolor(glyphs, color):
    """ANIMs: colour glyphs one by one (never animate the substring group itself: split trap)."""
    return [g.animate.set_color(color) for g in glyphs]


class BeforeYouBegin(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S03"] == 8, len(SAY)

        # ========================================================== 0. project, billing, permissions
        tr = tracker_bb(1)
        con = project_console().move_to([0, 1.25, 0])
        ill = illustration_tag().move_to(con.frame.get_corner(UR) + np.array([-0.95, 0, 0]))
        id_ring = ring(con.pid.box, TURN, buff=0.07, stroke=4)
        id_chip = grey_chip("no spaces · the command boxes need this one", color=TURN)
        id_chip.next_to(con.pid.box, DOWN, buff=0.22).align_to(con.pid.box, RIGHT)
        checks = VGroup(*[check_row(s) for s in CHECKS])
        checks.arrange_in_grid(rows=2, cols=2, buff=(0.9, 0.3), col_alignments="ll")
        checks.move_to([0, -1.7, 0])
        staff = grey_chip("restricted? ask course staff first").move_to([0, -2.95, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(con, scale=0.97), FadeIn(ill), run_time=0.8)
            vo.wait_until("Select your course project")
            self.play(Indicate(con.picker, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("and check its project ID")
            self.play(Create(id_ring), Indicate(con.pid.value, color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("not just its display name")
            self.play(Indicate(con.name.value, color=S.GREY, scale_factor=1.04), run_time=0.7)
            vo.wait_until("the command boxes need the ID")
            self.play(FadeIn(id_chip, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Confirm billing is on")
            self.play(track(tr, 2), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in checks], lag_ratio=0.35), run_time=1.6)
            vo.wait_until("if not")
            self.play(FadeIn(staff, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 1. the region
        line_y = 0.5
        rline = Line([-6.2, line_y, 0], [6.2, line_y, 0], color=S.GREY, stroke_width=3)
        rword = label("regions", 22, S.GREY).next_to(rline, UP, buff=0.15).align_to(rline, LEFT)
        p1 = region_pin(f"{REGION} · {REGION_CITY}")
        p2 = region_pin(f"{SPEECH_LOCATION} · speech model · part 3", dashed=True)
        for p, x in ((p1, -3.45), (p2, 3.2)):
            p.pin.move_to([x, line_y + 0.27, 0])        # the tip stands on the line
            p.text.next_to(p.pin, DOWN, buff=0.45).set_x(x)
        two = grey_chip("two different settings").move_to([0, line_y - 1.75, 0])
        two_l = arrow(two.get_left() + LEFT * 0.05, p1.text.get_bottom() + DOWN * 0.08 + RIGHT * 1.2)
        two_r = arrow(two.get_right() + RIGHT * 0.05, p2.text.get_bottom() + DOWN * 0.08 + LEFT * 1.2)

        with self.voiceover(SAY[1]) as vo:
            old = VGroup(con, ill, id_ring, id_chip, checks, staff)
            self.play(FadeOut(old), track(tr, 3), run_time=0.6)
            self.play(Create(rline), FadeIn(rword), run_time=0.7)
            vo.wait_until("the README uses Toronto")
            self.play(FadeIn(p1.pin, shift=DOWN * 0.3), FadeIn(p1.text, shift=UP * 0.1), run_time=0.7)
            self.play(each(list(substring_text(p1.text, REGION_CITY)), CLOUD, scale=1.15, lag=0.08), run_time=0.7)
            vo.wait_until("The speech model later uses")
            self.play(FadeIn(p2.pin, shift=DOWN * 0.3), FadeIn(p2.text, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("a separate setting")
            self.play(FadeIn(two, shift=UP * 0.1), GrowArrow(two_l), GrowArrow(two_r), run_time=0.7)

        # ========================================================== 2. the worksheet
        body = worksheet_body()
        ws = readme_card((46, 55), body)
        ws.move_to([0, 2.75 - ws.height / 2, 0])
        strip = worksheet_strip()
        cards = strip.cards
        rows2 = VGroup(VGroup(*[cards[k] for k in ("function", "web service", "web account")]).arrange(RIGHT, buff=0.2),
                       VGroup(*[cards[k] for k in ("job", "job account", "input", "output")]).arrange(RIGHT, buff=0.12))
        rows2.arrange(DOWN, buff=0.2)                    # two rows (the helper's wrap leaves one card alone)
        strip.move_to([0, BOTTOM + strip.height / 2 + 0.05, 0])
        order = (("the function", ["function"], [0]), ("the web service", ["web service"], [1]),
                 ("the job", ["job"], [3]), ("two runtime accounts", ["web account", "job account"], [2, 4]),
                 ("and two buckets", ["input", "output"], [5, 6]))

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(rline, rword, p1, p2, two, two_l, two_r)), run_time=0.5)
            self.play(FadeIn(ws, shift=DOWN * 0.2), run_time=0.7)
            for phrase, keys, idx in order:
                vo.wait_until(phrase)
                self.play(*[TransformFromCopy(body.values[i], cards[k]) for k, i in zip(keys, idx)],
                          *[Indicate(body.values[i], color=CLOUD, scale_factor=1.05) for i in idx], run_time=0.8)
            self.play(FadeOut(ws, shift=UP * 0.2), run_time=0.6)

        # ========================================================== 3. clone (extra spelling) + git log
        t = laptop_term(9, P_HOME)
        rc = readme_card((38, 39), "Clone or download the repository.\n"
                                   "Use the repository root as the working directory …")
        rc.move_to([-6.5, 2.75, 0], aligned_edge=UL)
        no_cmd = grey_chip("the README spells no command").next_to(rc, RIGHT, buff=0.3)
        c01, c02 = capture("laptop/01"), capture("laptop/02")
        assert c01.cmd == CLONE, c01.cmd

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(strip, shift=DOWN * 0.2), track(tr, 4), run_time=0.6)
            self.play(FadeIn(t), FadeIn(rc, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(no_cmd, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("clone the repository")
            ln = type_cmd(self, t, c01.cmd, type_time=1.2)
            out(self, t, c01.at(2))
            vo.wait_until("so our git clone is extra")
            pin(self, ln.rows[0] if hasattr(ln, "rows") else ln,
                beside(extra_row("its spelling"), ln.rows[0] if hasattr(ln, "rows") else ln))
            vo.wait_until("and so is the git log")
            type_cmd(self, t, "cd serverless-deployment", type_time=0.45)
            cd_prompt(self, t, P_REPO)
            self.play(track(tr, 4, True), run_time=0.4)
            lg = type_cmd(self, t, c02.cmd, type_time=0.7)
            pin(self, lg, beside(extra_row(), lg))
            rows = out(self, t, c02.at(2), wrap=True)
            self.play(*recolor(substring(rows[0], DIGEST_HEAD), TURN),
                      *recolor(substring(rows[0], "2026-10-22"), TURN), run_time=0.6)
            self.add(t)
            vo.wait_until("Pause and clone it")
            yt = on_bar(t, turn_row())
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)

        # ========================================================== 4. extra listings: old root, tutorial/
        c03, c04 = capture("laptop/03"), capture("laptop/04")
        assert c04.cmd == LS_TUTORIAL, c04.cmd

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(rc), FadeOut(no_cmd), FadeOut(yt), run_time=0.4)
            t.clear(self)
            resize(self, t, 13)
            ln = type_cmd(self, t, c03.cmd, type_time=0.3)
            pin(self, ln, beside(extra_row(), ln))
            ls = out(self, t, c03.at((2, 12)), run_time=0.9)
            by_name = {r.text: r for r in ls}
            vo.wait_until("including main.py and a Dockerfile")
            self.play(*[a for n in ROOT_OLD for a in recolor(by_name[n].glyphs, S.GREY)], run_time=0.7)
            self.add(t)
            et = beside(row_tag("erratum · don't build this Dockerfile", S.GREY), by_name["Dockerfile"], min_x=-2.6)
            pin(self, by_name["Dockerfile"], et)
            note_ = beside(row_tag("2025 files · the README never uses them", S.GREY), by_name["cli.py"], min_x=-2.6)
            pin(self, by_name["cli.py"], note_)
            vo.wait_until("don't build them")
            flash_tag(self, et, INK)
            vo.wait_until("Today's work sits under tutorial")
            self.play(*recolor(by_name["tutorial"].glyphs, TURN), run_time=0.5)
            self.add(t)
            type_cmd(self, t, c04.cmd, type_time=0.9)
            xb = on_bar(t, extra_row())
            self.play(FadeIn(xb, shift=LEFT * 0.1), run_time=0.3)
            vo.wait_until("function for part 1")
            fn = out(self, t, c04.at((32, 34)), run_time=0.4)
            p1t = beside(row_tag("part 1", OWN), fn[0], min_x=-1.0)
            pin(self, fn[0], p1t, run_time=0.5,       # colour and chip in one move (keeps up with the words)
                anim=AnimationGroup(FadeIn(p1t, shift=LEFT * 0.1), *[a for r in fn[1:] for a in recolor(r.glyphs, OWN)]))
            self.add(t)
            vo.wait_until("app for the image")
            app = out(self, t, c04.at((13, 21)), run_time=0.6)
            names = {r.text: r for r in app}
            imt = beside(row_tag("the image of parts 2–4", IMAGE), app[0], min_x=-1.0)
            pin(self, app[0], imt, run_time=0.5,
                anim=AnimationGroup(FadeIn(imt, shift=LEFT * 0.1), *recolor(names["Dockerfile"].glyphs, IMAGE),
                                    *recolor(names["translation_demo"].glyphs, IMAGE)))
            self.add(t)

        # ========================================================== 5. terminal setup: gcloud's own login
        rc2 = readme_card((66, 72), "Terminal setup — run once before using any gcloud command boxes")
        rc2.move_to([-6.5, 2.72, 0], aligned_edge=UL).shift(DOWN * 0.15)
        c03g = capture("gcloud/03")
        login = readme(74)
        assert login == "gcloud auth login", login
        own = identity_card("gcloud's own login", tool_chip("gcloud"))
        app_id = identity_card("the app's identity · part 3", dashed=True)
        VGroup(own, app_id).arrange(RIGHT, buff=0.6).move_to([0, 1.0, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(xb), run_time=0.3)
            t.clear(self)
            resize(self, t, 6, extra=[track(tr, 5, True)], run_time=0.6)
            self.play(retitle(t, T_GCLOUD), FadeIn(rc2, shift=DOWN * 0.15), run_time=0.5)
            la = type_cmd(self, t, c03g.cmd, type_time=0.5)
            pin(self, la, beside(extra_row(), la))
            nores = out(self, t, c03g.at(3), color=S.GREY)
            vo.wait_until("starting with gcloud auth login")
            self.play(track(tr, 5), run_time=0.3)
            lo = type_cmd(self, t, login, type_time=0.6)
            bs = grey_chip("browser sign-in · no output shown")
            under_term(t, bs)
            self.play(FadeIn(bs, shift=DOWN * 0.1), each(list(substring(lo, "login")), TURN, lag=0.1), run_time=0.7)
            self.add(t)
            vo.wait_until("an extra auth list shows no accounts yet")
            self.play(Indicate(nores[0], color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("It logs in the gcloud tool")
            self.play(FadeIn(own, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the app's identity comes in part 3")
            self.play(FadeIn(app_id, shift=UP * 0.15), run_time=0.6)

        # ========================================================== 6. the seven exports
        c05 = capture("laptop/05")

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(rc2, own, app_id, bs)), run_time=0.4)
            t.clear(self)
            resize(self, t, 13, run_time=0.6)
            typed = []
            for i, row in enumerate(c05.cmd_lines[:7]):
                typed.append(type_cmd(self, t, row, type_time=0.3))
                if i == 0:
                    r0 = _row_with(typed[0], PROJECT_PH)
                    self.play(*recolor(substring(r0, PROJECT_PH), TURN), run_time=0.4)
                    self.add(t)
                    pin(self, r0, beside(row_tag("put your real project ID here", TURN), r0))
            self.play(track(tr, 5, True), run_time=0.3)
            ec = type_cmd(self, t, c05.cmd_lines[7], type_time=0.4)
            pin(self, _last(ec), beside(extra_row(), _last(ec)))
            em = out(self, t, c05.at((9, 11)))
            srcs = [substring(_row_with(typed[k], "${PROJECT_ID}"), "${PROJECT_ID}") for k in (5, 6)]
            dsts = [substring(em[k], PROJECT_PH) for k in (0, 1)]
            u_src = [under(g, ROUTE, stroke=3) for g in srcs]
            u_dst = [under(g, ROUTE, stroke=3) for g in dsts]
            threads = VGroup(*u_src, *u_dst)
            self.play(*[a for g in srcs for a in recolor(g, ROUTE)], *[Create(u) for u in u_src], run_time=0.5)
            self.add(t, *u_src)                           # re-seat the terminal, keep the marks over it
            self.play(*[TransformFromCopy(a, b, path_arc=-0.5) for a, b in zip(u_src, u_dst)],
                      *[a for g in dsts for a in recolor(g, ROUTE)], run_time=0.9)
            self.add(t, threads)
            # the pause view: the seven exports in one place (the 13-row terminal has scrolled three off)
            sheet = exports_card(c05.cmd_lines[:7])
            sheet.move_to([0, -1.3, 0], aligned_edge=DOWN)
            assert sheet.get_top()[1] < 2.85, sheet.get_top()      # clear of the tracker
            pid_tag = row_tag("put your real project ID here", TURN)
            pid_tag.next_to(sheet.rows[0], RIGHT, buff=0.45)
            yt2 = turn_row().move_to(sheet.head).align_to(sheet.frame, RIGHT).shift(LEFT * 0.28)
            vo.wait_until("Pause and run them")
            self.play(FadeOut(threads), run_time=0.25)
            resize(self, t, 3, keep=list(em), extra=[FadeIn(sheet, shift=DOWN * 0.15)], run_time=0.7)
            self.play(FadeIn(pid_tag, shift=LEFT * 0.1), FadeIn(yt2, shift=LEFT * 0.1),
                      *recolor(substring(sheet.rows[0], PROJECT_PH), TURN), run_time=0.4)
            flash_tag(self, yt2, TURN)
        self.wait(1.2)                                    # hold the pause view a beat

        # ========================================================== 7. about this recording
        head = label("This recording machine: no Google account · no project", 28, INK)
        rows7 = [
            VGroup(label("gcloud boxes", 24, INK), label("→", 24, S.GREY),
                   label("run to their first honest error", 24, INK)),
            VGroup(label("console", 24, INK), label("→", 24, S.GREY), label("drawn", 24, INK), illustration_tag()),
            VGroup(label("cloud results", 24, INK), label("→", 24, S.GREY),
                   label("quoted from the README's recording", 24, INK), recorded_tag()),
        ]
        for r in rows7:
            r.arrange(RIGHT, buff=0.2)
        lines7 = VGroup(*rows7).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        inner = VGroup(head, lines7).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        frame7 = outline_box(inner.width + 0.9, inner.height + 0.8, S.GREY, solid=True, fill_opacity=0.08)
        frame7.fill.set_fill(S.GREY_DARKER, 1)
        inner.move_to(frame7)
        about = VGroup(frame7, inner).move_to([0, 0.75, 0])
        phrases = ("every gcloud box runs", "the console is drawn", "and cloud results come from")

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(sheet, pid_tag, yt2)), track(tr, 5), run_time=0.5)
            vo.wait_until("this machine has no Google account")
            self.play(FadeIn(frame7, scale=0.97), FadeIn(head, shift=DOWN * 0.1), run_time=0.7)
            for r, ph in zip(rows7, phrases):
                vo.wait_until(ph)
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(0.6)
            self.play(FadeOut(about), FadeOut(t), FadeOut(tr), run_time=0.8)
        self.wait(0.3)


# ------------------------------------------------------------------ small helpers
DIGEST_HEAD = "46cc62fd8b1a"
FOLD_AT = 66                                    # characters a 20 pt card row holds inside the frame


def export_rows(cmds) -> list[str]:
    """The exports as card rows: one row each, or (too long for a row) folded after '=' with a
    trailing backslash and the value on the next row, unindented, so the two rows join back to the
    same shell command."""
    rows = []
    for c in cmds:
        if len(c) <= FOLD_AT:
            rows.append(c)
        else:
            name, value = c.split("=", 1)
            assert len(value) <= FOLD_AT, c
            rows += [name + "=\\", value]
    return rows


def exports_card(cmds) -> VGroup:
    """README:75-81 (= laptop/05 lines 1-7) as a GREY README card, 20 pt mono, the long values folded
    after '=' (GREY backslash); ${PROJECT_ID} PINK, as the thread left it. .frame .head .rows"""
    texts = export_rows(cmds)
    assert "".join(r[:-1] if r.endswith("\\") else r + "\n" for r in texts) == "\n".join(cmds) + "\n"
    rows = VGroup(*[mono_line(r, 20, INK) for r in texts]).arrange(DOWN, aligned_edge=LEFT, buff=0.03)
    for r in rows:
        if r.text.endswith("\\"):
            substring(r, "\\").set_color(S.GREY)
        if "${PROJECT_ID}" in r.text:
            substring(r, "${PROJECT_ID}").set_color(ROUTE)
    card_ = readme_card((75, 81), rows)
    card_.rows = rows
    return card_


def _last(line):
    """The last row of a typed line (a folded command has several)."""
    return line.rows[-1] if hasattr(line, "rows") else line


def _row_with(line, sub: str):
    """The row of a typed line (folded or not) whose text contains `sub`."""
    for r in (line.rows if hasattr(line, "rows") else [line]):
        if sub in r.text:
            return r
    raise KeyError(sub)


def substring_text(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` inside a plain Text (spaces have no glyphs)."""
    s = t.text if hasattr(t, "text") else ""
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])
