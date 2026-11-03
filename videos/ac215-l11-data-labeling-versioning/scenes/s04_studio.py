"""S04 · A whole web app in one docker run — tracker B1 → B4, `lref("7, 13–14")` the whole scene.

Beats (script.md, ## S04; one voiceover block each):
0. TRACKER B1. The ready-made image (docker-shell.sh:24's name, TEAL) becomes a lit house; slide 7's
   why as one GREY line. CODE(docker-shell.sh: 5–9, 20 pt, line 6 cut after '|| '): line 6 YELLOW
   with a GREY sticky note 'inspect … || create · L10's shape'; line 9 GREY.
1. V1 builds over CODE(docker-shell.sh: 12–23): each flag's line peels off the panel into the row
   under the map and becomes a part: -d the TEAL house (the lecture's 'Label Studio Container'
   morphs into data-label-studio; the prompt returns), --network the PINK street, -p the door
   (chip 'publish the port'), the two -v pipes (GREY database drawer, GREEN secrets/), the -e lines
   the 'login' and 'key path' notes. The window then scrolls one line (13–24) to show the image.
2. TRACKER B1. Full terminal: cd data-labeling (prompt changes), sh docker-shell.sh → 10: 2–3, …,
   70–72 (72 'yours will differ'), ▶ your turn. TRACKER B2: README card (lines 91–97, line 95
   dimmed), docker container ls → 11 (columns STATUS · PORTS · NAMES), Up / port GREEN, ▶.
3. TRACKER B2 · extra. Map + 3-row strip; '+25 s' chip; docker container ls -a → 12, Exited (1) RED,
   the house tips over. PONDER(6 s).
4. TRACKER B2 · extra. docker logs … → 13: 4–12 (line 5 RED, 8 and the owner root YELLOW); the strip
   shrinks under the map, the drawer ORANGE; ls -la … → 14: 2–6 (root ORANGE); docker run --rm
   --entrypoint id … → 15: 2 (uid=1001 YELLOW).
5. TRACKER B1 · extra · Linux. sudo chown … → 16: 2–5 (1001 GREEN), drawer GREY; TRACKER B1
   sh docker-shell.sh → 17: 2–3 (▶); TRACKER B2 docker container ls → 18, Up GREEN, house stands.
6. TRACKER B2 · extra. docker logs … | grep … → 19: 10–13, 16, 20–21 (box YELLOW + 'at the time
   of recording'); curl …/health → 20: 2; curl -s -o … → 21: 2.
7. TRACKER B3: schematic login page (illustration) + CODE(docker-shell.sh: 19–20), ▶. TRACKER B4:
   wizard (illustration, README 110–115), the four choices, ▶. Stand-in server side (output only,
   tag extra · stand-in): 23: 2, 24: 2–7 (email), 28: 6 cut after the label config (id 1, title,
   the four choices). Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S04"]
SH = "data-labeling/docker-shell.sh"
WHY = "a labeling tool in your own container · no outside labeling service sees your data"
IMAGE_NAME = "heartexlabs/label-studio:latest"          # docker-shell.sh:24
PONDER_Q = "It said Up.\nNow it says Exited (1).\nWhere do you look first?"
PEEL_Y = -2.0                                            # first row of the peel zone under V1
PEEL_X = -6.3
DS_COLS = ["STATUS", "PORTS", "NAMES"]
TIP = 0.2                                                # the house leans when it exits


def peel_note(n) -> Text:
    s = f"docker-shell.sh · line {n}" if isinstance(n, int) else f"docker-shell.sh · lines {n}"
    return note(s, S.GREY).move_to([6.3, -3.3, 0], aligned_edge=RIGHT)


def readme_check_card() -> VGroup:
    """README.md lines 91–97: line 91's sentence (two rows), then the expected table (94–96) with
    the columns STATUS · PORTS · NAMES kept, line 95 dimmed. .rows95 .ok_rows"""
    s91 = readme(91)
    k = s91.index(" You should")
    words = VGroup(label(s91[:k], 20, INK), label(s91[k + 1:], 20, INK)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.1)
    hdr, row = cols([readme(94), readme(96)], DS_COLS)
    tbl = VGroup(mono(hdr, 20, S.GREY), mono(readme(95), 20, S.GREY_DARK), mono(row, 20, INK))
    tbl.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    body = VGroup(words, tbl).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    c = readme_card((91, 97), body, size=20)
    c.table, c.row = tbl, tbl[2]
    return c


def wizard_row(*parts, size: float = 22) -> VGroup:
    ms = [label(p, size, INK) if isinstance(p, str) else p for p in parts]
    return VGroup(*ms).arrange(RIGHT, buff=0.16)


def arrow_word(size: float = 22) -> Text:
    return label("→", size, S.GREY)


def choice_chip(word: str) -> VGroup:
    t = mono(word, 22, INK)
    fr = RoundedRectangle(width=t.width + 0.36, height=t.height + 0.26, corner_radius=0.1,
                          stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


class StudioInABox(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S04"] == 8, len(SAY)

        # ========================================================== 0. a ready-made image, your own container
        tr = tracker("B", 1)
        ref = lref("7, 13–14")
        img = mono(IMAGE_NAME, 24, IMAGE).move_to([0, 1.9, 0])
        img_l = note("a ready-made image", S.GREY).next_to(img, UP, buff=0.15)
        hs = house(CONTAINERS["studio"], 3.0, 1.2, lit=True).move_to([0, -0.5, 0], aligned_edge=DOWN)
        hs_l = note("your own container", S.GREY).next_to(hs, DOWN, buff=0.15)
        why = label(WHY, 22, S.GREY).move_to([0, -1.75, 0])
        p59 = code(SH, 5, 9, font_size=20, cuts={6: "|| "}).move_to([0, 0.9, 0])
        bar6 = line_bar(p59.code, 1, TURN)
        bar9 = line_bar(p59.code, 4, S.GREY)
        stk = sticky("inspect … || create · L10's shape").next_to(p59, DOWN, buff=0.35).align_to(p59, RIGHT)
        stk.shift(LEFT * 0.4)
        rm_l = note("an old data-label-studio is removed first", S.GREY).next_to(p59, DOWN, buff=0.35)
        rm_l.align_to(p59, LEFT).shift(RIGHT * 0.4)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.6)
            vo.wait_until("from a ready-made image")
            self.play(FadeIn(img, shift=DOWN * 0.15), FadeIn(img_l), run_time=0.6)
            vo.wait_until("in your own container")
            self.play(FadeIn(hs, shift=DOWN * 0.5), FadeIn(hs_l), Indicate(img, color=IMAGE, scale_factor=1.04),
                      run_time=0.8)
            vo.wait_until("so no outside labeling service")
            self.play(FadeIn(why, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("Its script creates the network")
            old = VGroup(img, img_l, hs, hs_l, why)
            self.play(FadeOut(old), FadeIn(p59, shift=UP * 0.15), run_time=0.7)
            self.remove(old, *old)
            self.play(FadeIn(bar6), run_time=0.4)
            vo.wait_until("only if it is missing")
            self.play(FadeIn(stk, scale=1.2), run_time=0.5)
            self.play(Indicate(code_span(p59.code, 1, "||"), color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("and removes any old container")
            self.play(FadeIn(bar9), FadeIn(rm_l, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 1. one docker run, flag by flag
        p12 = code(SH, 12, 23, cuts={21: '"/secrets/'}).move_to([0, -0.3, 0])
        p24 = code(SH, 13, 24, cuts={21: '"/secrets/'}).move_to([0, -0.3, 0])
        sm = StationMap(laid=False, lit=("studio",))
        skel = VGroup(sm.frame, sm.header, sm.street, sm.wall)
        hshape = VGroup(sm.studio.body, sm.studio.roof)
        lsc = label("Label Studio Container", 22, S.GREY).next_to(sm.studio, UP, buff=0.25)

        def peel(ks):
            """Copies of panel rows (k = file line − 12) stacked in the peel zone under the map."""
            rows = VGroup(*[p12.code.code_lines[k].copy() for k in ks])
            for i, r in enumerate(rows):
                r.move_to([PEEL_X, PEEL_Y - i * 0.45, 0], aligned_edge=LEFT)
            return rows

        def swap_peel(old_rows, old_note, ks, n, extra=()):
            new_rows, new_note = peel(ks), peel_note(n)
            self.play(FadeOut(old_rows, shift=UP * 0.2), FadeOut(old_note), FadeIn(new_rows, shift=UP * 0.2),
                      FadeIn(new_note), *extra, run_time=0.5)
            self.remove(old_rows, old_note)
            return new_rows, new_note

        prm = mono(P_LABELING, 20, LAPTOP).move_to([PEEL_X, PEEL_Y - 0.55, 0], aligned_edge=LEFT)
        prm_c = grey_chip("the prompt returns · it runs in the background").next_to(prm, RIGHT, buff=0.35)
        pub = grey_chip("publish the port").move_to([-1.7, -0.55, 0])

        with self.voiceover(SAY[1]) as vo:
            old = VGroup(p59, bar6, bar9, stk, rm_l)
            self.play(FadeOut(old), FadeIn(p12, shift=UP * 0.15), run_time=0.7)
            self.remove(old, *old)
            vo.wait_until("flag by flag")
            bars = [line_bar(p12.code, k, TURN) for k in (0, 2, 3, 4, 5)]
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.3), run_time=1.0)
            self.play(FadeOut(VGroup(*bars[1:])), run_time=0.3)
            self.remove(*bars[1:])
            vo.wait_until("The flag dash d")
            rows = p12.code.code_lines[0].copy()
            self.add(rows)
            nt = peel_note(12)
            self.play(FadeOut(VGroup(p12, bars[0])), FadeIn(skel),
                      rows.animate.move_to([PEEL_X, PEEL_Y, 0], aligned_edge=LEFT), FadeIn(nt), run_time=0.9)
            self.remove(p12, bars[0])
            rows = VGroup(rows)
            self.play(FadeIn(hshape, shift=UP * 0.6), FadeIn(lsc, shift=UP * 0.3), run_time=0.7)
            self.play(FadeTransform(lsc, sm.studio.text), run_time=0.8)
            self.remove(skel, hshape, *skel, *hshape, sm.studio.text)
            self.add(sm)
            self.play(FadeIn(prm, shift=UP * 0.1), FadeIn(prm_c, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and the network flag")
            self.play(FadeOut(VGroup(prm, prm_c)), run_time=0.3)
            self.remove(prm, prm_c)
            rows, nt = swap_peel(rows, nt, [2], 14)
            self.play(sm.lay(), run_time=0.8)
            self.play(Indicate(sm.street.text, color=ROUTE, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Then dash p")
            rows, nt = swap_peel(rows, nt, [3], 15)
            vo.wait_until("publishes the port")
            self.play(sm.open_door(), run_time=0.6)
            self.play(FadeIn(pub, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("Two dash v flags")
            rows, nt = swap_peel(rows, nt, [4, 5], "16–17", extra=[FadeOut(pub)])
            self.remove(pub)
            self.play(sm.pipe_on("db"), Indicate(rows[0], color=INK, scale_factor=1.03), run_time=0.9)
            vo.wait_until("and your secrets")
            self.play(sm.pipe_on("secrets"), Indicate(rows[1], color=KEY, scale_factor=1.03), run_time=0.9)
            vo.wait_until("the dash e lines")
            rows, nt = swap_peel(rows, nt, [7, 8, 9], "19–21")
            vo.wait_until("set the login")
            self.play(sm.stick("login"), Indicate(VGroup(rows[0], rows[1]), color=INK, scale_factor=1.03),
                      run_time=0.6)
            vo.wait_until("and key path")
            self.play(sm.stick("key path"), Indicate(rows[2], color=INK, scale_factor=1.03), run_time=0.6)
            # the window scrolls one line: the whole command, down to the image it runs
            mapall = VGroup(sm, sm.door, sm.db, sm.secrets, sm.pipes["db"], sm.pipes["secrets"],
                            *sm.notes.values())
            self.play(FadeOut(mapall), FadeOut(VGroup(rows, nt)), run_time=0.5)
            self.remove(mapall, *mapall, rows, nt)
            self.play(FadeIn(p24, shift=UP * 0.15), run_time=0.5)
            b24 = line_bar(p24.code, 11, IMAGE, opacity=0.25)
            self.play(FadeIn(b24), Indicate(code_span(p24.code, 11, IMAGE_NAME), color=IMAGE, scale_factor=1.04),
                      run_time=0.8)

        # ========================================================== 2. run it; the README's check
        t = term(P_LAPTOP_HOME, rows=6, size=20)
        c10, c11 = capture("10"), capture("11")
        rc = readme_check_card().move_to([0, 1.25, 0])
        rc.dim_95 = rc.table[1]

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p24, b24)), FadeIn(t), run_time=0.6)
            self.remove(p24, b24)
            type_cmd(self, t, "cd data-labeling", type_time=0.4)
            cd_prompt(self, t, P_LABELING)
            vo.wait_until("Pause and run")
            l10 = type_cmd(self, t, c10.cmd, type_time=0.4)
            yt = beside(turn_row(), l10)
            pin(self, l10, yt)
            flash_tag(self, yt, TURN)
            vo.wait_until("it pulls the image")
            unpin(self, l10, yt)
            out(self, t, c10.at((2, 3), "…", (70, 72)), wrap=True, run_time=0.8)
            dc = on_bar(t, differ_chip())
            idrow = t.lines[-1]
            self.play(FadeIn(dc, shift=LEFT * 0.1), Indicate(idrow, color=INK, scale_factor=1.02), run_time=0.6)
            vo.wait_until("Then the README")
            self.play(FadeOut(dc), FadeIn(rc, shift=DOWN * 0.2), track(tr, 2), run_time=0.7)
            self.remove(dc)
            l11 = type_cmd(self, t, c11.cmd, type_time=0.4)
            yt2 = beside(turn_row(), l11)
            pin(self, l11, yt2)
            out(self, t, cols(c11.at((2, 3)), DS_COLS), run_time=0.5)
            r11 = t.lines[-1]
            vo.wait_until("up, port 8080 published")
            self.play(substring(r11, "Up Less than a second").animate.set_color(PASS),
                      substring(r11, "0.0.0.0:8080->8080/tcp").animate.set_color(PASS),
                      Indicate(rc.row, color=PASS, scale_factor=1.03), run_time=0.7)
            flash_tag(self, yt2, TURN)

        # ========================================================== 3. 25 seconds later: Exited (1)
        mapall = VGroup(sm, sm.door, sm.db, sm.secrets, sm.pipes["db"], sm.pipes["secrets"], *sm.notes.values())
        t3 = term(P_LABELING, rows=3, size=20)
        late = grey_chip("+25 s").move_to([5.6, -0.85, 0])
        tip_pivot = sm.studio.body.get_corner(DR).copy()
        c12 = capture("12")

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(t, rc, yt2)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone, *t.lines)
            self.play(FadeIn(mapall), FadeIn(t3), track(tr, 2, extra=True), run_time=0.7)
            vo.wait_until("25 seconds later")
            self.play(FadeIn(late, shift=DOWN * 0.1), run_time=0.4)
            flash_tag(self, late, INK)
            vo.wait_until("with an extra dash a")
            xb = on_bar(t3, extra_row())
            self.play(FadeIn(xb, shift=LEFT * 0.1), run_time=0.3)
            type_cmd(self, t3, c12.cmd, type_time=0.4)
            out(self, t3, cols(c12.at((2, 3)), DS_COLS), run_time=0.5)
            r12 = t3.lines[-1]
            vo.wait_until("exited")
            self.play(substring(r12, "Exited (1) 25 seconds ago").animate.set_color(ERR),
                      Rotate(sm.studio, angle=-TIP, about_point=tip_pivot), run_time=0.8)
            self.play(sm.darken("studio"), run_time=0.5)
        pc = ponder(self, PONDER_Q, seconds=6)

        # ========================================================== 4. the logs: uid 1001 vs root
        c13, c14, c15 = capture("13"), capture("14"), capture("15")

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(pc), FadeOut(VGroup(mapall, late)), FadeOut(xb), run_time=0.5)
            self.remove(pc, mapall, *mapall, late, xb)
            resize(self, t3, 11, run_time=0.6)
            xb = on_bar(t3, extra_row())
            self.play(FadeIn(xb, shift=LEFT * 0.1), run_time=0.3)
            vo.wait_until("The logs")
            type_cmd(self, t3, c13.cmd, type_time=0.5)
            out(self, t3, [c13.line(4), (c13.line(5), ERR), *c13.at((6, 7)), (c13.line(8), TURN),
                           *c13.at((9, 12))], wrap=True, run_time=0.8)
            vo.wait_until("its data folder is not writable")
            self.play(Indicate(t3.find("not writable"), color=ERR, scale_factor=1.03), run_time=0.6)
            vo.wait_until("It runs as user 1001")
            self.play(Indicate(t3.find("UID"), color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("but Docker created")
            own = t3.find("drwxr-sr-x")
            self.play(substring(own, "root").animate.set_color(TURN), run_time=0.5)
            self.play(FadeOut(xb), run_time=0.2)
            self.remove(xb)
            resize(self, t3, 3, run_time=0.5)
            self.play(FadeIn(mapall), run_time=0.5)
            self.play(sm.alert(ROOT), run_time=0.6)
            self.play(Indicate(sm.db.text, color=ROOT, scale_factor=1.12), run_time=0.5)
            type_cmd(self, t3, c14.cmd, type_time=0.4)
            out(self, t3, c14.at((2, 6)), run_time=0.5, chunk=3)
            r14 = t3.find("label-studio")
            self.play(substring(r14, "root").animate.set_color(ROOT), run_time=0.4)
            type_cmd(self, t3, c15.cmd, type_time=0.4)
            out(self, t3, c15.at(2), run_time=0.3)
            self.play(substring(t3.lines[-1], "uid=1001").animate.set_color(TURN), run_time=0.4)

        # ========================================================== 5. the Linux fix: chown to 1001
        c16, c17, c18 = capture("16"), capture("17"), capture("18")
        mac = grey_chip("Docker Desktop for Mac normally avoids this").move_to([6.1, -0.85, 0], aligned_edge=RIGHT)

        with self.voiceover(SAY[5]) as vo:
            xl = on_bar(t3, extra_row("Linux"))
            self.play(track(tr, 1, extra="Linux"), FadeIn(xl, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Docker Desktop for Mac")
            self.play(FadeIn(mac, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Give the folder")
            type_cmd(self, t3, c16.cmd, type_time=0.6)
            out(self, t3, c16.at((2, 5)), run_time=0.5, chunk=3)
            r16 = t3.lines[-1]
            self.play(substring(r16, "1001").animate.set_color(PASS), sm.alert(LAPTOP), run_time=0.6)
            vo.wait_until("run the script again")
            self.play(FadeOut(VGroup(xl, mac)), track(tr, 1), run_time=0.3)
            self.remove(xl, mac)
            l17 = type_cmd(self, t3, c17.cmd, type_time=0.3)
            yt3 = beside(turn_row(), l17)
            pin(self, l17, yt3)
            out(self, t3, c17.at((2, 3)), run_time=0.4)
            vo.wait_until("and now it stays up")
            unpin(self, l17, yt3)
            self.play(track(tr, 2), run_time=0.3)
            type_cmd(self, t3, c18.cmd, type_time=0.3)
            out(self, t3, cols(c18.at((2, 3)), DS_COLS), run_time=0.4)
            r18 = t3.lines[-1]
            self.play(substring(r18, "Up About a minute").animate.set_color(PASS),
                      Rotate(sm.studio, angle=TIP, about_point=tip_pivot), run_time=0.8)
            self.play(sm.light("studio"), run_time=0.5)
            vo.wait_until("On Linux, pause")
            yt4 = on_bar(t3, turn_row())
            self.play(FadeIn(yt4, shift=LEFT * 0.1), run_time=0.3)
            flash_tag(self, yt4, TURN)

        # ========================================================== 6. extra checks: the update box, health
        c19, c20, c21 = capture("19"), capture("20"), capture("21")
        box = [(c19.line(n).rstrip(), TURN) for n in range(10, 14)]

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(mapall), FadeOut(yt4), track(tr, 2, extra=True), run_time=0.5)
            self.remove(mapall, *mapall, yt4)
            resize(self, t3, 11, run_time=0.6)
            xb = on_bar(t3, extra_row())
            self.play(FadeIn(xb, shift=LEFT * 0.1), run_time=0.3)
            type_cmd(self, t3, c19.cmd, type_time=0.6)
            vo.wait_until("the logs show a box")
            out(self, t3, box + [c19.line(16), *c19.at((20, 21))], run_time=0.8)
            vo.wait_until("offering version 1.23.2")
            up = t3.find("Update available")
            self.play(Indicate(substring(up, "1.23.2"), color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("which ran 1.23.0")
            self.play(Indicate(substring(up, "1.23.0"), color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("at the time of recording")
            tt = beside(time_row(), up)
            pin(self, up, tt)
            vo.wait_until("The tag is latest")
            type_cmd(self, t3, c20.cmd, type_time=0.4)
            out(self, t3, c20.at(2), run_time=0.3)
            self.play(substring(t3.lines[-1], '"UP"').animate.set_color(PASS), run_time=0.3)
            type_cmd(self, t3, c21.cmd, type_time=0.5)
            out(self, t3, c21.at(2), run_time=0.3)

        # ========================================================== 7. log in, create the project; the stand-ins
        win = window("http://localhost:8080/", 7.2, 2.7).move_to([-1.9, 1.3, 0])
        ill = illustration_tag().next_to(win, RIGHT, buff=0.3).align_to(win, UP)
        form = form_rows([("Email", LOGIN[0]), ("Password", LOGIN[1])], width=6.2)
        form.move_to(win.content).shift(UP * 0.05)
        p1920 = code(SH, 19, 20).move_to([0, -2.4, 0])
        ytl = your_turn().next_to(win, RIGHT, buff=0.3).align_to(win, DOWN)

        wiz = window("http://localhost:8080/", 12.4, 4.2).move_to([0, 0.05, 0])
        ill2 = illustration_tag().next_to(wiz, UP, buff=0.1).align_to(wiz, RIGHT)
        x0 = wiz.get_left()[0] + 0.5
        r1 = wizard_row("Create Project", arrow_word(), "name", arrow_word(), "skip Data Import", arrow_word(),
                        "Labeling Setup")
        tpl = label("Computer Vision > Image Classification", 22, INK)
        r2 = wizard_row("Template:", tpl)
        chips = VGroup(*[choice_chip(c) for c in CHOICES]).arrange(RIGHT, buff=0.25)
        r3 = wizard_row("Choices:", chips)
        save = choice_chip("Save")
        save.text.become(label("Save", 22, INK).move_to(save.text))
        r4 = wizard_row(save)
        for r, y in zip((r1, r2, r3, r4), (1.0, 0.3, -0.45, -1.2)):
            r.move_to([x0, y, 0], aligned_edge=LEFT)
        rmw = note("README.md · lines 110–115").move_to([0, -2.6, 0]).align_to(wiz, LEFT)
        ytw = your_turn().move_to([0, -2.6, 0]).align_to(wiz, RIGHT)

        t7 = term(P_LABELING, rows=8, size=20)
        heads = {"23": "POST /user/login/ · stand-in", "24": "GET /api/current-user/whoami · stand-in",
                 "28": "POST /api/projects · stand-in"}

        def head(k):
            return strip_head(heads[k]).next_to(t7.box, UP, buff=0.15).align_to(t7.box, LEFT)

        c23, c24, c28 = capture("23"), capture("24"), capture("28")
        l28 = cut(c28.line(6), '</View>"')

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(t3, xb, tt)), track(tr, 3), run_time=0.5)
            self.remove(t3, xb, tt, *t3.lines)
            self.play(FadeIn(win, scale=0.97), FadeIn(ill), run_time=0.6)
            self.play(FadeIn(form, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and log in with the username")
            self.play(FadeIn(p1920, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("from lines 19 and 20")
            b19, b20 = line_bar(p1920.code, 0, TURN), line_bar(p1920.code, 1, TURN)
            self.play(FadeIn(b19), Indicate(form[0].value, color=TURN, scale_factor=1.06), run_time=0.5)
            self.play(FadeIn(b20), Indicate(form[1].value, color=TURN, scale_factor=1.1), run_time=0.5)
            self.play(FadeIn(ytl, shift=LEFT * 0.15), run_time=0.3)
            flash_tag(self, ytl, TURN)
            vo.wait_until("Create a project")
            gone = VGroup(win, ill, form, p1920, b19, b20, ytl)
            self.play(FadeOut(gone), track(tr, 4), run_time=0.5)
            self.remove(gone, *gone)
            self.play(FadeIn(wiz, scale=0.97), FadeIn(ill2), FadeIn(rmw, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(r1, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("with the image classification template")
            self.play(FadeIn(r2, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(tpl, color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("with the choices brie")
            self.play(FadeIn(r3[0]), FadeIn(chips[0], scale=1.2), run_time=0.4)
            for c, w in zip(chips[1:], CHOICES[1:]):
                vo.wait_until(w)
                self.play(FadeIn(c, scale=1.2), run_time=0.3)
            self.play(FadeIn(r4, shift=RIGHT * 0.2), run_time=0.3)
            vo.wait_until("Pause and do it")
            self.play(FadeIn(ytw, shift=LEFT * 0.15), run_time=0.3)
            flash_tag(self, ytw, TURN)
            vo.wait_until("Underneath")
            gone = VGroup(wiz, ill2, r1, r2, r3, r4, rmw, ytw)
            h = head("23")
            self.play(FadeOut(gone), FadeIn(t7), FadeIn(h), track(tr, 3, extra="stand-in"), run_time=0.6)
            self.remove(gone, *gone)
            sb = on_bar(t7, standin_row())
            self.play(FadeIn(sb, shift=LEFT * 0.1), run_time=0.3)
            out(self, t7, c23.at(2), run_time=0.3)
            vo.wait_until("we are logged in")
            self.play(Indicate(t7.lines[-1], color=INK, scale_factor=1.03), run_time=0.5)
            h2 = head("24")
            self.play(FadeTransform(h, h2), run_time=0.4)
            out(self, t7, c24.at((2, 7)), run_time=0.6)
            em = t7.find('"email"')
            self.play(substring(em, '"email": "student@example.com"').animate.set_color(TURN), run_time=0.5)
            vo.wait_until("and project 1 holds")
            h3 = head("28")
            self.play(FadeTransform(h2, h3), track(tr, 4, extra="stand-in"), run_time=0.4)
            rows28 = out(self, t7, [l28], wrap=True, run_time=0.6)
            hl = [substring(rows28[0], '"id":1'), substring(rows28[0], '"title":"Cheese')]
            hl.append(substring(rows28[1], 'labels"'))
            self.play(*[m.animate.set_color(TURN) for m in hl], run_time=0.5)
            vo.wait_until("the four cheeses")
            ch = []
            for w in CHOICES:
                r = next(r for r in rows28 if f'\\"{w}\\"' in r.text)
                ch.append(substring(r, f'\\"{w}\\"'))
            self.play(each(ch, TURN, scale=1.1, lag=0.2), run_time=1.0)
            self.play(*[m.animate.set_color(TURN) for m in ch], run_time=0.3)
        self.wait(1.2)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
