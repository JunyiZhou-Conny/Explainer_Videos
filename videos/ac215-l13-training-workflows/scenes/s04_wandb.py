"""S04 · Runs on a shared axis (notebook B) — tracker B1 → B6, lecture_ref 12–13, 16–17.

Beats (script.md, ## S04; one voiceover block each):
0. Tracker B1 + lref. GREY chip (not spoken) "open notebook B · save a copy · GPU runtime (cell 3)".
   Cell 5 (nbB:37) with `-U` lit; the Colab stand-in strip (tracker "B1 · extra · local stand-in")
   types C05's command and prints C05:2 (cut), 4–5, then C05b's extra check: `0.31.0` YELLOW with
   `at the time of recording`; GREY chip "stored run: 0.22.2" (nbB:773). ▶ your turn.
1. B2: chip "cells 7–32 …", cell 16 (nbB:373–375, the two download lines elided around the URL);
   line 375 struck GREY + chip "about 510 MB you never use · you may delete this line". ▶ your turn.
2. B3: a W&B page illustration (User settings → API keys, the key as dots); Colab's secrets panel
   (illustration): name `WandB` (from nbB:605), value dots, "Notebook access" switched on. ▶ your
   turn. Cell 34 (nbB:603–606, 614–615; 606 and 615 cut at the frame, the team masked `<team>`).
3. B4: cell 38 (nbB:697 YELLOW, 773, 781). ▶ your turn. V2: the wandb.ai building, notebook B's five
   run names slide into the BLUE project frame `cheese-app-demo`, every row grows a GREY-dashed
   slot over one shared epoch axis (1 … 25).
4. Only the 2_block slot draws its recorded sparklines (nbB:1010–1014); the other four stay ghosts.
   "Compare": cell 38's and cell 42's model.fit side by side (nbB:710–716, 940–945). PONDER 6 s.
5. Line 715 lights YELLOW (cell 42 has no such line); the ledger returns over cell 38's model.fit
   (nbB:710 … 715, 782) and a PURPLE callback pipe runs from model.fit to the 2_block slot only;
   NB(B:782) cut small + chip "deprecated · harmless here"; summary nbB:1016, 1021; the four slots
   stay ghosts; chip "system charts = …".
6. The two MobileNet rows collapse under `mobilenetv2_train_base` (nbB:1629, URL masked), chip "tell
   runs apart by run id"; an `extra` cell `wandb.finish()` after cell 52 (tracker "B4 · extra").
7. B5: cell 55 (name · epochs · accuracy) slides in beside cell 54 (S01's two tables): B's winner
   YELLOW, the fine-tuned epochs 15 vs 10 glow ("not like for like"); both frozen rows ring YELLOW
   (67.24% · 68.97%), chip "same settings · 15 epochs · 2 photos apart", S03's ruler unit returns;
   chip "run cells 55–60 too · pause at the next step".
8. B6: cell 13 (nbB:254, 257: the instructors' bucket and project ringed, "replace this with yours"),
   chip "edited? run cell 13 again"; cell 64 (nbB:1819–1820), chip "cells 64 and 66: no stored
   output"; slide-16 chip (not spoken); ▶ your turn. V1: notebook B → wandb.ai lights. Fade out.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F403
from explainer import style as S

SAY = NARRATION["S04"]
PONDER_CURVES = "Five runs in one project, but only one\nhas loss and accuracy curves.\nWhat do the other four lack?"
TOP = 2.75                     # pictures stay under the tracker / lecture tag
LEFT_X = -6.35
DOTS = "••••••••••••"            # a key is always a row of dots (never key material)


def top_left(m, x=LEFT_X, y=TOP):
    """Place m with its top-left corner at (x, y)."""
    m.shift(np.array([x - m.get_left()[0], y - m.get_top()[1], 0]))
    return m


def quoted_cell(which: str, items, size: float = 20, indent: int | None = None, pad: float = 0.3) -> VGroup:
    """A schematic notebook cell (BLUE frame, header 'notebook B · cell n', `illustration` inside the
    header row) for lines notebook_cell() cannot hold: items are extract line numbers, (n, how) with
    `how` as elide() takes it, or '…'. indent=k re-indents an indented line to k spaces (the two
    model.fit panels side by side). Text comes from nb_line() (masked). .frame .header .rows .ill .line(n)"""
    texts, ns = [], []
    for it in items:
        if isinstance(it, str):
            texts.append(it)
            ns.append(None)
            continue
        n, how = (it, None) if isinstance(it, int) else it
        s = nb_line(which, n)
        if how is not None:
            s = elide(s, how)
        if indent is not None and s.startswith(" "):
            s = " " * indent + s.lstrip(" ")
        texts.append(s)
        ns.append(n)
    pitch = line_pitch(size)
    rows = VGroup()
    index = {}
    for i, (n, s) in enumerate(zip(ns, texts)):
        r = mono_line(s, size, INK)
        r.shift(np.array([-r.strut.get_left()[0], -i * pitch - r.strut.get_center()[1], 0]))
        rows.add(r)
        if n is not None:
            index[n] = r
        k = r.text.find("…")
        while k >= 0:
            glyph_range(r, k, k + 1).set_color(S.GREY)
            k = r.text.find("…", k + 1)
    first = next(n for n in ns if n is not None)
    head = label(f"notebook {which} · cell {nb_cell(which, first)}", CAPTION, S.GREY)
    ill = illustration_tag()
    w = max(rows.width + 2 * pad, head.width + ill.width + 0.9)
    fr = RoundedRectangle(width=w, height=rows.height + 0.85, corner_radius=0.14, stroke_color=CLOUD,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    head.move_to(fr.get_corner(UL) + np.array([0.25 + head.width / 2, -0.3, 0]))
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * pad).align_to(fr, DOWN).shift(UP * 0.15)
    ill.move_to(fr.get_corner(UR) + np.array([-0.15 - ill.width / 2, -0.3, 0]))
    g = VGroup(fr, head, rows, ill)
    g.frame, g.header, g.rows, g.ill = fr, head, rows, ill
    g.line = lambda n: index[n]
    return g


def toggle_switch(on: bool = False) -> VGroup:
    """A schematic on/off switch (GREY off, GREEN on). .track .knob"""
    tr_ = RoundedRectangle(width=0.62, height=0.32, corner_radius=0.16, stroke_color=PASS if on else S.GREY,
                           stroke_width=2).set_fill(PASS if on else S.GREY_DARK, 0.5 if on else 0.3)
    kn = Circle(radius=0.11, stroke_width=0).set_fill(INK, 1)
    kn.move_to(tr_.get_center() + RIGHT * (0.15 if on else -0.15))
    g = VGroup(tr_, kn)
    g.track, g.knob = tr_, kn
    return g


def secrets_panel() -> VGroup:
    """Colab's key-icon panel, drawn (illustration): a secret named WandB (the name nbB:605 asks for),
    its value as dots, and the 'Notebook access' switch (off). .frame .name .value .switch .ill"""
    key_name = nb_line("B", 605).split("'")[1]
    assert key_name == "WandB", key_name
    head = VGroup(key_glyph(0.6), label("Colab · Secrets", 22, INK)).arrange(RIGHT, buff=0.25)
    sw = toggle_switch(False)
    acc = VGroup(sw, label("Notebook access", 20, INK)).arrange(RIGHT, buff=0.2)
    nm = VGroup(label("Name", 20, S.GREY), mono(key_name, 22, INK)).arrange(RIGHT, buff=0.3)
    val = VGroup(label("Value", 20, S.GREY), mono(DOTS, 22, S.GREY)).arrange(RIGHT, buff=0.3)
    body = VGroup(head, acc, nm, val).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    fr = RoundedRectangle(width=body.width + 0.8, height=body.height + 0.6, corner_radius=0.14,
                          stroke_color=CLOUD, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    body.move_to(fr)
    ill = illustration_tag().next_to(fr, UP, buff=0.08).align_to(fr, RIGHT)
    g = VGroup(fr, body, ill)
    g.frame, g.name, g.value, g.switch, g.ill = fr, nm[1], val[1], sw, ill
    return g


def wandb_page() -> VGroup:
    """The W&B settings page, drawn (illustration): User settings → API keys, the key as dots."""
    w = window(WB_HOST, win_w=5.9, win_h=2.7)
    path = notebook_menu(("User settings", "API keys"), size=20)
    key = VGroup(label("API key", 20, S.GREY), mono(DOTS, 22, S.GREY)).arrange(RIGHT, buff=0.3)
    body = VGroup(path, key).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
    body.move_to(w.content)
    ill = illustration_tag().next_to(w.frame, UP, buff=0.08).align_to(w.frame, RIGHT)
    g = VGroup(w, body, ill)
    g.path, g.key, g.ill = path, key, ill
    return g


def finish_cell() -> VGroup:
    """The extra cell the narration adds after cell 52: `wandb.finish()` (not in the notebook)."""
    head = label("new cell · after cell 52", CAPTION, S.GREY)
    code_ = mono("wandb.finish()", 22, INK)
    body = VGroup(head, code_).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    fr = RoundedRectangle(width=body.width + 0.9, height=body.height + 0.6, corner_radius=0.14,
                          stroke_color=CLOUD, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    body.move_to(fr)
    tg = extra_tag().next_to(fr, UP, buff=0.08).align_to(fr, RIGHT)
    g = VGroup(fr, body, tg)
    g.frame, g.code, g.tag = fr, code_, tg
    return g


class SharedAxis(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S04"] == 9, len(SAY)
        assert nb_cell("B", 37) == 5 and nb_cell("B", 603) == 34 and nb_cell("B", 697) == 38
        assert nb_cell("B", 940) == 42 and nb_cell("B", 1629) == 52 and nb_cell("B", 254) == 13

        # ========================================================== 0. setup (B1): cell 5, the stand-in
        tr = tracker_b(1)
        ref = lref("12–13, 16–17")
        open_chip = grey_chip("open notebook B · save a copy · GPU runtime (cell 3)")
        top_left(open_chip)
        c5 = notebook_cell("B", 37, size=22)
        top_left(c5, y=open_chip.get_bottom()[1] - 0.55)
        dash_u = c5.sub(37, "-U")
        stored = grey_chip("stored run: " + nb_line("B", 773).split()[-1])
        assert stored.text.original_text.endswith("0.22.2")
        stored.next_to(c5.frame, RIGHT, buff=0.45).align_to(c5.frame, DOWN)
        yt0 = your_turn().next_to(c5.frame, RIGHT, buff=0.45).align_to(c5.frame, UP)
        strip = colab_term(rows=3)
        st_tag = standin_tag().next_to(strip.box, UP, buff=0.12).align_to(strip.box, RIGHT)
        c05, c05b = capture("C05"), capture("C05b")
        warn = cut(c05.line(2), "can result in")

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref, shift=DOWN * 0.15), run_time=0.7)
            self.play(FadeIn(open_chip, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Its first cell installs it")
            self.play(FadeIn(c5, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("the dash U flag")
            self.play(dash_u.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(dash_u, color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("whatever is newest")
            self.play(FadeIn(strip), FadeIn(st_tag, shift=LEFT * 0.15), track(tr, 1, extra="local stand-in"),
                      run_time=0.6)
            type_cmd(self, strip, c05.cmd)
            out(self, strip, [warn] + c05.at((4, 5)), run_time=0.8)
            vo.wait_until("An extra check")
            ln = type_cmd(self, strip, c05b.cmd)
            xr = beside(extra_row(), ln, buff=0.35)
            pin(self, ln, xr)
            vo.wait_until("shows 0.31.0")
            v = out(self, strip, [(c05b.line(2), TURN)], run_time=0.4)
            assert c05b.line(2) == "0.31.0"
            tm = beside(time_row(), v[-1], buff=0.35)
            pin(self, v[-1], tm)
            vo.wait_until("while the stored run used 0.22.2")
            self.play(FadeIn(stored, shift=LEFT * 0.2), run_time=0.5)
            self.play(Indicate(stored.text, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Pause and run it")
            self.play(FadeIn(yt0, shift=LEFT * 0.2), run_time=0.4)
            flash_tag(self, yt0, TURN)

        # ========================================================== 1. data cells (B2): an unused 510 MB zip
        same = grey_chip("cells 7–32: the same data and pipelines as notebook A")
        top_left(same)
        c16 = quoted_cell("B", [373, (374, ('download_file("', "/releases/", '.zip",')),
                                (375, ('download_file("', "/releases/", '.zip",'))])
        top_left(c16, y=same.get_bottom()[1] - 0.45)
        r375 = c16.line(375)
        zip_ = substring(r375, "experiments.zip")
        st = strike(r375, S.GREY, stroke=3)
        zip_chip = grey_chip("about 510 MB you never use · you may delete this line")
        zip_chip.next_to(c16.frame, DOWN, buff=0.35).align_to(c16.frame, LEFT)
        yt1 = your_turn().next_to(zip_chip, DOWN, buff=0.3).align_to(zip_chip, LEFT)

        with self.voiceover(SAY[1]) as vo:
            old = VGroup(open_chip, c5, stored, yt0, strip, st_tag, *strip.lines)
            self.play(FadeOut(old, shift=DOWN * 0.2), track(tr, 2), run_time=0.7)
            self.remove(old, *old)
            self.play(FadeIn(same, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("but one also downloads a zip")
            self.play(FadeIn(c16, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(zip_, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("of about 510 megabytes")
            self.play(FadeIn(zip_chip, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("You may delete that line")
            self.play(Create(st), r375.animate.set_opacity(0.45), run_time=0.7)
            vo.wait_until("then pause and run them")
            self.play(FadeIn(yt1, shift=UP * 0.15), run_time=0.4)
            flash_tag(self, yt1, TURN)

        # ========================================================== 2. the key (B3): W&B page, Colab secret, cell 34
        page = wandb_page()
        top_left(page, y=TOP - 0.45)
        sec = secrets_panel()
        sec.move_to([6.35 - sec.width / 2, 0, 0])
        sec.shift(UP * (TOP - sec.get_top()[1]))
        yt2 = your_turn().next_to(sec.frame, DOWN, buff=0.35).align_to(sec.frame, RIGHT)
        c34 = notebook_cell("B", (603, 606), (614, 615), size=20,
                            cuts={606: "wandb.login(key=wandb_key)", 615: "(<team>)"})
        top_left(c34, -c34.width / 2, TOP - 0.4)
        on_sw = toggle_switch(True).move_to(sec.switch)

        with self.voiceover(SAY[2]) as vo:
            old = VGroup(same, c16, st, zip_chip, yt1)
            self.play(FadeOut(old, shift=UP * 0.2), track(tr, 3), run_time=0.6)
            self.remove(old, *old)
            vo.wait_until("Copy your API key")
            self.play(FadeIn(page, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("from the user settings")
            self.play(each(page.path.items, INK, scale=1.06, lag=0.3), run_time=0.9)
            self.play(Indicate(page.key, color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("In Colab, open the key icon")
            self.play(FadeIn(sec, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("named exactly as on screen")
            nr = ring(sec.name, TURN, buff=0.07)
            self.play(sec.name.animate.set_color(TURN), Create(nr), run_time=0.6)
            vo.wait_until("with notebook access on")
            self.play(Transform(sec.switch, on_sw), run_time=0.5)
            vo.wait_until("Pause and add yours")
            self.play(FadeIn(yt2, shift=UP * 0.15), run_time=0.4)
            flash_tag(self, yt2, TURN)
            vo.wait_until("Cell 34 signs in with it")
            old = VGroup(page, sec, nr, yt2)
            self.play(FadeOut(old, shift=UP * 0.2), run_time=0.5)
            self.remove(old, *old)
            self.play(FadeIn(c34, shift=UP * 0.2), run_time=0.6)
            self.play(c34.sub(605, "'WandB'").animate.set_color(TURN), run_time=0.4)
            self.play(each([c34.line(614), c34.line(615)], INK, scale=1.03, lag=0.3), run_time=0.9)

        # ========================================================== 3. five training cells (B4): runs in one project
        c38 = notebook_cell("B", 697, 773, 781, size=20, hi={697: TURN})
        top_left(c38, -c38.width / 2, TOP - 0.4)
        yt3 = your_turn().next_to(c38, DOWN, buff=0.3).align_to(c38.frame, LEFT)
        bld = building(WB_HOST, bw=12.6, bh=5.9)
        bld.remove(bld[3])                     # no columns: the ledger sits in the hall
        bld.move_to([0, -3.5, 0], aligned_edge=DOWN)
        led = RunLedger("B", columns=("name",), frame=False, tag_=False, header="project · " + WB_PROJECT_NB,
                        row_h=0.43)
        led.remove(led.heads)
        led.header.set_color(CLOUD)
        slots = led.slots(slot_w=3.4)
        proj_body = VGroup(led.header, *led.rows, slots)
        led.move_to([-1.05, -0.95, 0])         # riders: the slots follow
        proj_body = VGroup(led.header, *led.rows, slots)
        proj = RoundedRectangle(width=proj_body.width + 0.7, height=proj_body.height + 0.5, corner_radius=0.14,
                                stroke_color=CLOUD, stroke_width=2.5).move_to(proj_body)
        i2 = led.find("2_block")
        assert (i2, led.rows[0].name, led.rows[1].name) == (2, "mobilenetv2_train_base_False",
                                                             "mobilenetv2_train_base_True")

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(c34, shift=UP * 0.2), track(tr, 4), run_time=0.6)
            self.remove(c34)
            self.play(FadeIn(c38, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("pause and run the five training cells")
            self.play(FadeIn(yt3, shift=UP * 0.15), run_time=0.4)
            flash_tag(self, yt3, TURN)
            vo.wait_until("Each starts its run with wandb init")
            self.play(Indicate(c38.line(697), color=TURN, scale_factor=1.05), run_time=0.7)
            vo.wait_until("in one project, cheese app demo")
            self.play(each([c38.sub(697, WB_PROJECT_NB), c38.sub(781, WB_PROJECT_NB)], TURN, scale=1.08, lag=0.4),
                      run_time=1.0)
            vo.wait_until("In the ledger")
            self.play(FadeOut(VGroup(c38, yt3), shift=UP * 0.2), FadeIn(bld), run_time=0.7)
            self.remove(c38, yt3)
            self.play(Create(proj), FadeIn(led.header), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.5) for r in led.rows], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("five runs on one shared epoch axis")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in slots.boxes], lag_ratio=0.15),
                      run_time=0.9)
            self.play(Create(slots.axis[0]), FadeIn(slots.axis[1:]), run_time=0.7)

        # ========================================================== 4. only one slot draws; compare; ponder
        cv = RunLedger.curves(slots.boxes[i2])
        r2 = led.ring_row(i2, TURN)
        ghosts = [slots.boxes[i] for i in range(5) if i != i2]
        fit38 = quoted_cell("B", list(range(710, 717)), indent=2)
        fit42 = quoted_cell("B", list(range(940, 946)), indent=2)
        pair = VGroup(fit38, fit42).arrange(RIGHT, buff=0.25, aligned_edge=UP)
        top_left(pair, -pair.width / 2, TOP - 0.15)
        assert pair.width <= 13.1, pair.width

        with self.voiceover(SAY[4]) as vo:
            vo.wait_until("only the two block run shows curves")
            self.play(Create(r2), run_time=0.5)
            self.play(Create(cv), run_time=1.4)
            self.play(each(ghosts, S.GREY, scale=1.04, lag=0.2), run_time=1.0)
            vo.wait_until("Compare its model fit call")
            proj_all = VGroup(bld, proj, led.header, *led.rows, slots, cv, r2)
            self.play(FadeOut(proj_all, shift=DOWN * 0.3), run_time=0.6)
            self.remove(proj_all, *proj_all)
            self.play(FadeIn(fit38, shift=RIGHT * 0.2), FadeIn(fit42, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("Something to ponder")
            self.play(each([fit38.line(710), fit42.line(940)], INK, scale=1.04, lag=0.3), run_time=0.8)
        pc = ponder(self, PONDER_CURVES, seconds=6)

        # ========================================================== 5. the answer: a callback; the pipe
        l715 = fit38.line(715)
        none42 = dashed_chip("no callbacks= line")
        none42.next_to(fit42.frame, DOWN, buff=0.3).align_to(fit42.frame, LEFT)
        # the ledger returns higher (no building), over cell 38's model.fit at the bottom
        dx, dy = LEFT_X - led.rows[0].frame.get_left()[0], TOP - led.header.get_top()[1]
        led.shift(np.array([dx, dy, 0]))
        for m in (slots, cv, r2):
            m.shift(np.array([dx, dy, 0]))
        low = notebook_cell("B", 710, "…", 715, 782, size=20, tag_=False, cuts={782: "WandbCallback is deprecated"})
        low.move_to([0, BOTTOM, 0], aligned_edge=DOWN)
        rec = nb_recorded_tag("B").next_to(low.frame, UP, buff=0.08).align_to(low.ill, LEFT).shift(LEFT * 0.15)
        rec.shift(RIGHT * (low.ill.get_left()[0] - 0.15 - rec.get_right()[0]))
        assert slots.axis.get_bottom()[1] > low.ill.get_top()[1] or slots.axis.get_right()[0] < low.ill.get_left()[0]
        low_out = VGroup(low.well, *low.out_rows)
        low_code = VGroup(low.frame, low.header, low.ill, *low.code_rows)
        fit_g = low.sub(710, "model.fit")
        slot2 = slots.boxes[i2]
        gx = slot2.get_left()[0] - 0.13          # the gap between the row frames and the slots
        ya = (slots.axis.get_bottom()[1] + low.frame.get_top()[1]) / 2 + 0.05
        ya = max(ya, low.frame.get_top()[1] + 0.2)
        pts = [fit_g.get_top() + UP * 0.05, [fit_g.get_center()[0], ya, 0], [gx, ya, 0],
               [gx, slot2.get_center()[1], 0], slot2.get_left() + LEFT * 0.03]
        cb = pipe(pts, TOOL, 4)
        dep = grey_chip("deprecated · harmless here")
        dep.move_to([low.frame.get_right()[0] - 0.3 - dep.width / 2, low.out_rows[0].get_center()[1], 0])
        acc, vacc = run_summary("accuracy"), run_summary("val_accuracy")
        assert (acc, vacc) == ("0.72436", "0.45192")
        summ = VGroup(*[VGroup(mono(k, 20, S.GREY), mono(x, 20, INK)).arrange(RIGHT, buff=0.25)
                        for k, x in (("accuracy", acc), ("val_accuracy", vacc))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.15)
        for row in summ:
            row[1].align_to(summ[1][1], LEFT)
        summ_tag = nb_recorded_tag("B")
        summ_g = VGroup(summ, summ_tag).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rx = slots.boxes[0].get_right()[0] + 0.45
        summ_g.move_to([rx + summ_g.width / 2, slot2.get_center()[1] - 0.1, 0])
        sys_card = card(["system charts =", "the machine's CPU · GPU · memory", "over time"], size=20)
        sys_card.move_to([rx + sys_card.width / 2, 0, 0]).align_to(led.header, UP)
        assert sys_card.get_right()[0] < 6.6 and summ_g.get_right()[0] < 6.6, (sys_card.get_right(), summ_g.get_right())
        assert sys_card.get_bottom()[1] > summ_g.get_top()[1], "system card over the summary"

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            vo.wait_until("A callback")
            self.play(l715.animate.set_color(TURN), FadeIn(none42, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(l715, color=TURN, scale_factor=1.04), run_time=0.6)
            vo.wait_until("code that model fit calls after every epoch")
            self.play(FadeOut(VGroup(fit38, fit42, none42), shift=UP * 0.2), run_time=0.5)
            self.remove(fit38, fit42, none42)
            self.play(FadeIn(VGroup(led.header, *led.rows, slots, cv), shift=DOWN * 0.2), FadeIn(low_code, shift=UP * 0.2),
                      run_time=0.7)
            self.play(low.line(715).animate.set_color(TURN), run_time=0.3)
            self.play(Create(cb), run_time=1.0)
            vo.wait_until("Only the two block cell passes")
            r2 = led.ring_row(i2, TURN)
            self.play(Create(r2), run_time=0.5)
            self.play(FadeIn(low_out), FadeIn(rec), run_time=0.5)
            self.play(FadeIn(dep, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("so only its loss and accuracy arrive")
            for _ in range(2):
                dot = Dot(radius=0.08, color=TOOL).move_to(pts[0])
                self.play(MoveAlongPath(dot, cb.core), run_time=0.8, rate_func=linear)
                self.remove(dot)
            self.play(FadeIn(summ_g, shift=LEFT * 0.2), Indicate(cv, color=INK, scale_factor=1.03), run_time=0.7)
            vo.wait_until("Without one, wandb init gives you system charts")
            self.play(FadeIn(sys_card, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("never your curves")
            self.play(each(ghosts, S.GREY, scale=1.04, lag=0.15), run_time=1.0)

        # ========================================================== 6. one shared name; the run nobody finishes
        lab, collapse = led.collapse(0, 1, "mobilenetv2_train_base")
        c52 = notebook_cell("B", 1629, size=20, wrap=True)
        c52.move_to([LEFT_X + c52.width / 2, 0, 0]).align_to(low.frame, DOWN).shift(UP * c52.tag.height)
        url = c52.sub(1629, "runs/…")
        id_chip = grey_chip("tell runs apart by run id")
        id_chip.next_to(c52.frame, RIGHT, buff=0.4).align_to(c52.frame, UP)
        fin = finish_cell()
        fin.move_to([6.35 - fin.width / 2, 0, 0]).align_to(c52.frame, DOWN)

        with self.voiceover(SAY[6]) as vo:
            old = VGroup(low, rec, dep, cb, sys_card, summ_g, r2)
            self.play(FadeOut(old), run_time=0.5)
            self.remove(old, *old)
            vo.wait_until("Both MobileNet runs share one name")
            self.play(collapse, run_time=1.0)
            self.play(FadeIn(c52, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("so tell them apart by run ID")
            self.play(FadeIn(id_chip, shift=LEFT * 0.15), run_time=0.4)
            ur = ring(url, TURN, buff=0.05)
            self.play(Create(ur), run_time=0.5)
            vo.wait_until("No cell finishes the last run")
            self.play(FadeOut(VGroup(id_chip, ur)), run_time=0.4)
            self.remove(id_chip, ur)
            self.play(FadeIn(fin, shift=LEFT * 0.2), track(tr, 4, extra=True), run_time=0.6)
            vo.wait_until("an extra")
            flash_tag(self, fin.tag, INK)
            self.play(Indicate(fin.code, color=INK, scale_factor=1.05), run_time=0.6)

        # ========================================================== 7. cell 55 (B5): the second table
        ta = RunLedger("A", frame=False)
        tb = RunLedger("B", frame=False)
        ta.move_to([-3.35, 0, 0])
        tb.move_to([3.35, 0, 0])
        dy7 = TOP - max(ta.get_top()[1], tb.get_top()[1])
        ta.shift(UP * dy7)
        tb.shift(UP * dy7)
        ft, fz = "mobilenetv2_train_base_True", "mobilenetv2_train_base_False"
        ia_t, ib_t, ia_f, ib_f = ta.find(ft), tb.find(ft), ta.find(fz), tb.find(fz)
        assert (ia_t, ib_t, ia_f, ib_f) == (0, 1, 1, 0)
        assert (ta.cell(ia_f, "accuracy").original_text, tb.cell(ib_f, "accuracy").original_text) == ("67.24%", "68.97%")
        assert (ta.cell(ia_t, "epochs").original_text, tb.cell(ib_t, "epochs").original_text) == ("15", "10")
        win_b = tb.ring_row(0, TURN)
        ep = [ta.cell(ia_t, "epochs"), tb.cell(ib_t, "epochs")]
        ep_r = [ring(e, S.GREY, buff=0.07) for e in ep]
        unfair = grey_chip("not like for like")
        frozen_a = ta.ring_row(ia_f, TURN)
        same_c = grey_chip("same settings · 15 epochs · 2 photos apart")
        unit = VGroup(label("1 photo = 0.86 points", 22, INK), mono("(1/116)", 20, S.GREY)).arrange(RIGHT, buff=0.2)
        more = grey_chip("run cells 55–60 too · pause at the next step")
        chips7 = VGroup(unfair, same_c, unit, more).arrange(DOWN, buff=0.28)
        chips7.next_to(VGroup(ta, tb), DOWN, buff=0.4)
        assert chips7.get_bottom()[1] > -3.55, chips7.get_bottom()

        with self.voiceover(SAY[7]) as vo:
            old = VGroup(led.header, *led.rows, slots, cv, lab, c52, fin)
            self.play(FadeOut(old, shift=UP * 0.2), track(tr, 5), run_time=0.6)
            self.remove(old, *old)
            vo.wait_until("Cell 55 builds the second table")
            self.play(FadeIn(ta, shift=RIGHT * 0.3), run_time=0.5)
            self.play(FadeIn(tb, shift=LEFT * 1.2), run_time=0.8)
            vo.wait_until("from the opening")
            self.play(Create(win_b), run_time=0.6)
            vo.wait_until("The fine-tuned MobileNet trained 10 epochs here")
            self.play(each(ep, INK, scale=1.15, lag=0.4), *[Create(r) for r in ep_r], run_time=1.0)
            vo.wait_until("not a fair comparison")
            self.play(FadeIn(unfair, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Now the frozen MobileNet")
            self.play(FadeOut(VGroup(*ep_r)), Create(frozen_a), Indicate(win_b, color=TURN, scale_factor=1.02),
                      run_time=0.7)
            self.remove(*ep_r)
            vo.wait_until("with the same settings and epochs")
            self.play(FadeIn(same_c, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("67.24 in notebook A")
            self.play(Indicate(ta.cell(ia_f, "accuracy"), color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("68.97 here")
            self.play(Indicate(tb.cell(ib_f, "accuracy"), color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("Two photos apart by chance alone")
            self.play(FadeIn(unit, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the size of the winning margin")
            self.play(Indicate(same_c.text, color=TURN, scale_factor=1.05), run_time=0.7)
            self.play(FadeIn(more, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 8. upload (B6); V1: notebook B → wandb.ai
        c13 = notebook_cell("B", 254, "…", 257, size=20)
        top_left(c13, y=TOP - 0.4)
        names = [c13.sub(254, '"cheese-app-models"'), c13.sub(257, '"ac215-project"')]
        nrings = [ring(nm, TURN, buff=0.04, stroke=2.5) for nm in names]
        rchips = [replace_chip() for _ in names]
        for rc, nm in zip(rchips, names):
            rc.move_to([6.35 - rc.width / 2, nm.get_center()[1], 0])
        rchips[0].next_to(c13.frame, UP, buff=0.12).align_to(c13.frame, RIGHT).shift(LEFT * (c13.ill.width + 0.3))
        rchips[1].next_to(c13.frame, DOWN, buff=0.12).align_to(c13.frame, RIGHT)
        again = grey_chip("edited? run cell 13 again").next_to(c13.frame, DOWN, buff=0.12).align_to(c13.frame, LEFT)
        c64 = notebook_cell("B", 1819, 1820, size=20)
        top_left(c64, y=again.get_bottom()[1] - 0.6)
        no_out = grey_chip("cells 64 and 66: no stored output").next_to(c64.frame, RIGHT, buff=0.4)
        slide16 = grey_chip("the lecture's dashboard screenshot shows an earlier project · yours says cheese")
        slide16.next_to(c64.frame, DOWN, buff=0.35).align_to(c64.frame, LEFT)
        yt8 = your_turn().next_to(no_out, DOWN, buff=0.3).align_to(no_out, LEFT)
        assert slide16.get_right()[0] < 6.6 and slide16.get_bottom()[1] > -3.55
        mp = TrainingMap.at("S04")

        with self.voiceover(SAY[8]) as vo:
            old = VGroup(ta, tb, win_b, frozen_a, chips7)
            self.play(FadeOut(old, shift=UP * 0.2), track(tr, 6), run_time=0.6)
            self.remove(old, *old)
            self.play(FadeIn(c13, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("edit the bucket and project")
            self.play(*[Create(r) for r in nrings], *[FadeIn(c, shift=LEFT * 0.15) for c in rchips], run_time=0.7)
            vo.wait_until("and run cell 13 again")
            self.play(FadeIn(again, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("then run cells 64 and 66")
            self.play(FadeIn(c64, shift=UP * 0.2), FadeIn(no_out, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("pause and do it")
            self.play(FadeIn(yt8, shift=UP * 0.15), FadeIn(slide16, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, yt8, TURN)

        old = VGroup(c13, *nrings, *rchips, again, c64, no_out, slide16, yt8)
        self.play(FadeOut(old, shift=UP * 0.2), FadeIn(mp), run_time=0.8)
        self.remove(old, *old)
        self.play(mp.light("nbB"), run_time=0.5)
        self.play(mp.light("laneB", "wandb"), run_time=0.8)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
