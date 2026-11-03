"""S08 · Both containers in one file, and a clean exit — tracker E1 → E2, then F1 → F4,
`lref("12")` the whole scene. Ends part 1.

Beats (script.md, ## S08; one voiceover block each):
0. TRACKER E1. README card (lines 218–229) over a 6-row terminal. At S07's last prompt
   (app@eb57c56e6715) 42:73 `exit` → 74; laptop prompt. `docker stop data-label-studio` (bar chip
   "README: docker stop <container_name_or_id>") → 50:2; `docker ps` → 51:2 squeezed (empty); ▶.
   TRACKER E2: `sh docker-shell-compose.sh` (bar chip "the README names the script"; a GREY card
   "docker-compose: not found? …") → 52:26 GREY (row tag "harmless"), …, 30 RED, wrapped. The
   terminal shrinks to a 3-row strip under V1: the stopped house is a GREY dashed ghost still
   holding its name tag.
1. TRACKER E2 · extra: `docker rm data-label-studio` → 53:2; the ghost vanishes; ▶ comes with the
   compose re-run (one checkpoint). TRACKER E2: compose again → 54:28–30 (padding squashed), 29–30
   YELLOW; V1: Label Studio lit again, the CLI house joins, the compose file drapes over both; README
   card line 95 (the stray line) + chip "the stray line, explained" (unspoken).
2. TRACKER E2 · extra: at app@ce215fc4f7a5 54:37 `echo $GCS_BUCKET_NAME` → 38 RED; CODE
   docker-compose.yml:13–18 (dedent, 20 pt), line 17 RED, tag `erratum`, chip "edit this one too".
3. TRACKER E2 · extra: 54:39 `python cli.py -p -k …` (obviously fake) → 40–41, …, 123–124 RED in an
   8-row terminal; strip again under CODE docker-compose.yml:19–20, which becomes V1's order arrow +
   stopwatch "started"; 54:125 the wait loop (folds), 126 `{"status": "UP"}` then the prompt and the
   typed command on the same row, 127–130 (`1 Cheese labels` GREEN); V1's database drawer pulses:
   "same folder".
4. TRACKER F1 · extra: 54:131 `exit` → 132; the one-off house leaves; `docker ps` → 55 (STATUS,
   PORTS, NAMES), "still Up". TRACKER F1–F4 in a 10-row terminal: 60, 61, 62 ([y/N] then y; 10 GREY,
   13 YELLOW), 63 (IMAGE, DISK USAGE; "at the time of recording"); ▶. Strip keeps 62:12–13; on V1 the
   stopped house, its door and the street go; the drawer stays; chip "next time: docker-shell.sh
   first".
5. The empty lot, the GREY drawer dimmed. PONDER 6 s.
6. TRACKER F4 · extra: `sudo ls -la docker-volumes/label-studio` → 64:2–9 (columns re-aligned the way
   ls does, single spaces), `label_studio.sqlite3` GREEN, owner `1001` ORANGE + chip "hence sudo".
   Part-1 close on V7 (PipelineMap.at("S08")): the pruned houses and street unlight, bucket 1 and its
   labeled drawer stay lit; a photo in cheeses_unlabeled/ changes under its name; the YELLOW parked
   card; the versioning half flashes ("part 2"). Fade to an empty frame (end of part 1).
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S08"]
PONDER_Q = "After docker system prune,\nis your labeled project gone?"
STOP_CHIP = "README: docker stop <container_name_or_id>"
NAMES_CHIP = "the README names the script"
STRAY_CHIP = "the stray line, explained"
EDIT_CHIP = "edit this one too"
NET_CHIP = "next time: docker-shell.sh first"
PARKED = ("your labels are safe", "the photos they point at can change",
          "how do you freeze which photos a model saw?")


def drop(scene, *mobs) -> None:
    """Take mobjects and their whole families off the scene (a scrolled terminal is split into parts
    on the scene; a faded part left there snaps back at full opacity)."""
    fam = []
    for m in mobs:
        fam.extend(m.get_family())
    scene.remove(*fam)


def row_with(rows, sub: str, occurrence: int = 0):
    """The printed terminal row (of `rows`) whose text contains `sub`."""
    hits = [r for r in rows if sub in r.text]
    return hits[occurrence]


def ls_align(lines: list[str]) -> list[str]:
    """`ls -la` rows re-aligned the way ls itself pads (single spaces; counts, sizes and days right-
    aligned): the capture is padded wider than a 65-character row. Text unchanged but for spaces."""
    head, rows = lines[0], [s.split() for s in lines[1:]]
    right = {1, 4, 6}
    w = [max(len(r[j]) for r in rows) for j in range(len(rows[0]))]
    out = [head] + [" ".join(c.rjust(w[j]) if j in right else c.ljust(w[j]) for j, c in enumerate(r)).rstrip()
                    for r in rows]
    for a, b in zip(lines, out):
        assert a.split() == b.split(), (a, b)
    return out


def readme_compose_card() -> VGroup:
    """README.md lines 218–229 (data-labeling): the compose script and the stop / ps note."""
    r1 = label("You can now stop all containers and run them", 20, INK)
    r2 = VGroup(label("together using", 20, INK), mono("docker-shell-compose.sh", 20, INK)).arrange(RIGHT, buff=0.15)
    r3 = VGroup(label("To stop a running Docker container: …", 20, INK))
    r4 = mono("docker stop <container_name_or_id>", 20, INK)
    r5 = VGroup(label("… which you can find by running:", 20, INK), mono("docker ps", 20, INK)).arrange(RIGHT, buff=0.15)
    body = VGroup(r1, r2, r3, r4, r5).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    c = readme_card((218, 229), body)
    c.rows = (r1, r2, r3, r4, r5)
    return c


def compose_hint() -> VGroup:
    """GREY card: the Compose v2 spelling of the script's last line, for a machine without the
    `docker-compose` binary (docker-shell-compose.sh:11)."""
    return card([label("docker-compose: not found?", 20, INK), mono("docker compose run --rm", 20, INK),
                 mono("  --service-ports data-label-cli", 20, INK)], size=20, buff=0.1)


class ComposeAndClean(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S08"] == 7, len(SAY)
        c42, c50, c51, c52, c53, c54 = (capture(n) for n in ("42", "50", "51", "52", "53", "54"))
        c55, c60, c61, c62, c63, c64 = (capture(n) for n in ("55", "60", "61", "62", "63", "64"))
        assert c50.cmd in readme(225).replace("<container_name_or_id>", "data-label-studio")
        assert c51.cmd in readme(229) and c60.cmd in readme(243) and c62.cmd in readme(245)
        assert c63.cmd in readme(246) and "docker-shell-compose.sh" in readme(218)

        # ========================================================== 0. exit, stop, ps; the name conflict
        tr = tracker("E", 1)
        ref = lref("12")
        rc = readme_compose_card()
        rc.move_to([-6.35 + rc.width / 2, 1.42, 0])
        hint = compose_hint()
        hint.move_to([6.35 - hint.width / 2, 1.42, 0])
        t = term(P_LABELING, rows=6)
        sm = StationMap(laid=True, lit=("studio", "cli"), shown=("door", "db"))
        sm.add(sm.pipes["db"])
        sm.remove(sm.studio)                          # stopped: only its ghost holds the name
        gh = sm.ghost()
        gh.tag.next_to(gh.house, RIGHT, buff=0.15).align_to(gh.house, DOWN).shift(UP * 0.1)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.6)
            self.play(FadeIn(rc, shift=UP * 0.15), FadeIn(t), run_time=0.6)
            vo.wait_until("runs both containers from one compose file")
            self.play(Indicate(rc.rows[1][1], color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Leave the command line container with exit")
            istep(self, t, c42.line(73), type_time=0.4)
            out(self, t, c42.at(74), run_time=0.3)
            t.set_prompt(P_LABELING)
            vo.wait_until("stop Label Studio")
            type_cmd(self, t, c50.cmd, type_time=0.9)
            ch0 = on_bar(t, row_tag(STOP_CHIP))
            self.play(FadeIn(ch0, shift=LEFT * 0.1), Indicate(rc.rows[3], color=INK, scale_factor=1.06),
                      run_time=0.6)
            out(self, t, c50.at(2), run_time=0.3)
            vo.wait_until("and check with docker ps")
            type_cmd(self, t, c51.cmd, type_time=0.4)
            r51 = out(self, t, squeeze(c51.at(2)), run_time=0.3)
            self.play(Indicate(rc.rows[4][1], color=INK, scale_factor=1.1), run_time=0.5)
            vo.wait_until("pause and do it")
            yt0 = on_bar(t, turn_row())
            self.play(FadeOut(ch0), FadeIn(yt0), run_time=0.4)
            flash_tag(self, yt0, TURN)
            vo.wait_until("Then run sh docker-shell-compose.sh")
            ch1 = on_bar(t, row_tag(NAMES_CHIP))
            self.play(FadeOut(yt0), FadeIn(ch1), track(tr, 2), run_time=0.5)
            type_cmd(self, t, c52.cmd, type_time=0.8)
            self.play(FadeIn(hint, shift=LEFT * 0.15), Indicate(rc.rows[1][1], color=TURN, scale_factor=1.06),
                      run_time=0.6)
            vo.wait_until("Here it stops on a name conflict")
            r26 = out(self, t, [(x, S.GREY) for x in c52.at(26)], wrap=True, run_time=0.6)
            pin(self, r26[-1], beside(row_tag("harmless"), r26[-1]))
            r30 = out(self, t, ["…"] + [(x, ERR) for x in c52.at(30)], wrap=True, run_time=0.8)
            conf = substring(row_with(r30, "Conflict."), "Conflict.")
            self.play(Indicate(conf, color=ERR, scale_factor=1.15), run_time=0.6)
            vo.wait_until("docker stop leaves the container behind")
            gone = VGroup(rc, hint, ch1)
            self.play(FadeOut(gone), run_time=0.4)
            drop(self, gone)
            resize(self, t, 3, keep=list(r30[1:4]))
            self.play(FadeIn(sm), run_time=0.6)
            self.play(FadeIn(gh, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("still holding its name")
            nm = substring(row_with(r30, '"/data-label-studio"'), '"/data-label-studio"')
            self.play(Indicate(gh.tag.text, color=INK, scale_factor=1.15), Indicate(nm, color=ERR, scale_factor=1.1),
                      run_time=0.8)

        # ========================================================== 1. docker rm; compose again
        bl = sm.blanket()
        c95 = readme_card(95, mono(readme(95), 20, INK))
        c95.move_to([6.1 - c95.width / 2, -0.66, 0])
        stray = grey_chip(STRAY_CHIP).next_to(c95, LEFT, buff=0.25)

        with self.voiceover(SAY[1]) as vo:
            xt1 = on_bar(t, extra_row())
            self.play(track(tr, 2, extra=True), FadeIn(xt1), run_time=0.5)
            type_cmd(self, t, c53.cmd, type_time=0.8)
            out(self, t, c53.at(2), run_time=0.3)
            vo.wait_until("frees the name")
            self.play(FadeOut(gh, scale=0.9), run_time=0.7)
            drop(self, gh)
            vo.wait_until("pause, remove it")
            self.play(Indicate(sm.street.text, color=ROUTE, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and run the compose script again")
            self.play(FadeOut(xt1), track(tr, 2), run_time=0.4)
            self.remove(xt1)
            type_cmd(self, t, c54.cmd, type_time=0.7)
            yt1 = on_bar(t, turn_row())
            self.play(FadeIn(yt1), run_time=0.3)
            flash_tag(self, yt1, TURN)
            vo.wait_until("This time Compose creates Label Studio")
            r28 = out(self, t, squash(c54.at(28)), run_time=0.3)
            self.play(FadeIn(sm.studio, scale=0.95), run_time=0.6)
            sm.add(sm.studio)
            vo.wait_until("plus a one-off command line container")
            r29 = out(self, t, [(x, TURN) for x in c54.at((29, 30))], run_time=0.5)
            self.play(sm.join_cli(), run_time=0.7)
            self.play(Create(bl.box), FadeIn(bl.text, shift=DOWN * 0.1), run_time=0.8)
            self.play(FadeIn(c95, shift=LEFT * 0.15), FadeIn(stray, shift=LEFT * 0.15), run_time=0.6)
            self.play(Indicate(c95.body, color=TURN, scale_factor=1.08), run_time=0.6)

        # ========================================================== 2. compose keeps its own bucket name
        p17 = code("data-labeling/docker-compose.yml", 13, 18, dedent=True, font_size=20).move_to([0, 0.75, 0])
        bar17 = line_bar(p17.code, 17 - 13, ERR, opacity=0.25)
        err17 = erratum_tag()
        chip17 = grey_chip(EDIT_CHIP)
        VGroup(err17, chip17).arrange(RIGHT, buff=0.3).next_to(p17, DOWN, buff=0.22).align_to(p17, RIGHT)

        with self.voiceover(SAY[2]) as vo:
            xt2 = on_bar(t, extra_row())
            self.play(FadeOut(yt1), FadeIn(xt2), track(tr, 2, extra=True), run_time=0.5)
            self.remove(yt1)
            istep(self, t, c54.line(37), type_time=0.7)
            vo.wait_until("prints the README's bucket name")
            r38 = out(self, t, [(x, ERR) for x in c54.at(38)], run_time=0.4)
            self.play(Indicate(r38[0], color=ERR, scale_factor=1.1), run_time=0.6)
            vo.wait_until("compose keeps its own copy")
            gone = VGroup(sm, sm.cli, bl, c95, stray)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(p17, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("on line 17 of docker-compose.yml")
            self.play(FadeIn(bar17), code_span(p17.code, 17 - 13, '"cheese-app-data-demo"').animate.set_color(ERR),
                      run_time=0.6)
            self.play(FadeIn(err17, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("so edit it too")
            self.play(FadeIn(chip17, shift=LEFT * 0.15), run_time=0.5)
            flash_tag(self, err17, INK)

        # ========================================================== 3. depends_on: started, not ready
        p19 = code("data-labeling/docker-compose.yml", 19, 20).move_to([0, 0.75, 0])
        bar19 = line_bar(p19.code, 0, TURN, opacity=0.2)
        od = sm.order()
        same = grey_chip("same folder").next_to(sm.db, RIGHT, buff=0.3)
        loop_cmd = c54.istep(125)[1]
        assert loop_cmd == "until curl -s http://data-label-studio:8080/health; do sleep 2; done"

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(p17, bar17, err17, chip17, xt2)
            self.play(FadeOut(gone), run_time=0.4)
            drop(self, gone)
            resize(self, t, 8)
            xt2 = on_bar(t, extra_row())
            self.play(FadeIn(xt2), run_time=0.3)
            ln39 = istep(self, t, c54.line(39), type_time=1.0)
            fk = beside(row_tag("obviously fake"), ln39, buff=0.3)
            pin(self, ln39, fk)
            vo.wait_until("And the first call is refused")
            r40 = out(self, t, [c54.line(40)] + [(x, ERR) for x in c54.at(41)] + ["…"]
                      + [(x, ERR) for x in c54.at((123, 124))], wrap=True, run_time=1.0)
            cr = row_with(r40, "ConnectionError")
            self.play(Indicate(substring(cr, "ConnectionError"), color=ERR, scale_factor=1.12), run_time=0.6)
            vo.wait_until("the depends on setting")
            keep = [r for r in r40 if r.text in {s for s in soft(c54.at(124), t.max_chars)}][:3]
            self.play(FadeOut(xt2), run_time=0.2)
            self.remove(xt2)
            resize(self, t, 3, keep=keep)
            self.play(FadeIn(p19, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(bar19), run_time=0.3)
            vo.wait_until("starts Label Studio first")
            self.play(FadeOut(VGroup(p19, bar19), scale=0.6, target_position=od.arrow.get_center()),
                      FadeIn(VGroup(sm, sm.cli, bl)), run_time=0.7)
            drop(self, p19, bar19)
            self.play(GrowArrow(od.arrow), run_time=0.7)
            vo.wait_until("but does not wait until it listens")
            self.play(FadeIn(od.watch, scale=0.8), run_time=0.5)
            self.play(Indicate(od.watch.text, color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("After an extra wait loop")
            xt3 = on_bar(t, extra_row())
            self.play(FadeIn(xt3), run_time=0.3)
            istep(self, t, c54.line(125), type_time=1.2)
            up, rest = c54.line(126).split("app@", 1)
            p_cli = t.prompt
            t.set_prompt(up + "app@" + rest.split(" ", 1)[0])
            ln126 = type_cmd(self, t, rest.split(" ", 1)[1], type_time=1.0)
            first = ln126.rows[0] if hasattr(ln126, "rows") else ln126
            glyph_range(first, 0, len(up)).set_color(OUTPUT)
            t.set_prompt(p_cli)
            vo.wait_until("project 1 is back")
            r127 = out(self, t, [c54.line(127), c54.line(128), (c54.line(129), PASS), c54.line(130)], wrap=True,
                       run_time=0.6)
            ok = substring(row_with(r127, "1 Cheese labels"), "1 Cheese labels")
            self.play(Indicate(ok, color=PASS, scale_factor=1.12), run_time=0.6)
            vo.wait_until("because the same folder is mounted")
            self.play(FadeIn(same, shift=LEFT * 0.1), each([sm.db.text, sm.pipes["db"]], INK, scale=1.1, lag=0.3),
                      run_time=1.0)

        # ========================================================== 4. Label Studio keeps running; cleanup
        tr_f = tracker("F", 1, extra=True)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(xt3, same)), run_time=0.3)
            self.remove(xt3, same)
            tr = swap_tracker(self, tr, tr_f)
            istep(self, t, c54.line(131), type_time=0.3)
            out(self, t, c54.at(132), run_time=0.3)
            t.set_prompt(P_LABELING)
            gone = VGroup(sm.cli, bl, od)
            xt4 = on_bar(t, extra_row())
            self.play(FadeOut(gone, shift=RIGHT * 0.3), FadeIn(xt4), run_time=0.5)
            drop(self, gone)
            type_cmd(self, t, c55.cmd, type_time=0.35)
            r55 = out(self, t, cols(c55.at((2, 3)), ["STATUS", "PORTS", "NAMES"]), run_time=0.4)
            upr = substring(r55[1], "Up 33 seconds")
            self.play(upr.animate.set_color(TURN), Indicate(sm.studio.text,
                                                            color=IMAGE, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Then the README's cleanup")
            gone = VGroup(sm, xt4)
            self.play(FadeOut(gone), run_time=0.4)
            drop(self, gone)
            resize(self, t, 10, keep=3, extra=(track(tr, 1),), run_time=0.6)
            type_cmd(self, t, c60.cmd, type_time=0.4)
            out(self, t, cols(c60.at((2, 3)), ["STATUS", "PORTS", "NAMES"]), run_time=0.4)
            vo.wait_until("stop, prune")
            self.play(track(tr, 2), run_time=0.3)
            type_cmd(self, t, c61.cmd, type_time=0.4)
            out(self, t, c61.at(2), run_time=0.3)
            self.play(track(tr, 3), run_time=0.3)
            type_cmd(self, t, c62.cmd, type_time=0.4)
            out(self, t, c62.at((2, 7)), run_time=0.4)
            q = c62.line(8)
            ask = q[:q.index("[y/N]") + len("[y/N]")]
            assert q == ask + " y"
            ask_ln = out(self, t, [ask], run_time=0.3)[0]
            self.wait(0.5)
            yl = mono_line(q, t.size, OUTPUT)
            yl.shift(ask_ln.strut.get_corner(UL) - yl.strut.get_corner(UL))
            yg = yl.glyphs[-1].set_color(TURN)
            self.play(FadeIn(yg, scale=1.6), run_time=0.2)
            self.play(yg.animate.set_color(OUTPUT), run_time=0.2)
            attach(self, ask_ln, yg)
            r62 = out(self, t, [c62.line(9), (c62.line(10), S.GREY), c62.line(11), c62.line(12),
                                (c62.line(13), TURN), "…", c62.line(24)], run_time=0.6)
            net = row_with(r62, NETWORK)
            vo.wait_until("and list the images")
            self.play(track(tr, 4), run_time=0.3)
            type_cmd(self, t, c63.cmd, type_time=0.4)
            r63 = out(self, t, cols(c63.at((2, 4)), ["IMAGE", "DISK USAGE"]), run_time=0.4)
            pin(self, r63[1], beside(time_row(), r63[1], buff=0.4))
            vo.wait_until("pause and run them")
            yt4 = on_bar(t, turn_row())
            self.play(FadeIn(yt4), run_time=0.3)
            flash_tag(self, yt4, TURN)
            vo.wait_until("The prune also removed the network")
            self.play(FadeOut(yt4), run_time=0.3)
            self.remove(yt4)
            keep = [r62[3], net]
            resize(self, t, 3, keep=keep)
            sm.studio.become(lit_house(sm.studio, False))      # stopped (61), then pruned (62)
            self.play(FadeIn(sm), run_time=0.5)
            lot = VGroup(sm.studio, sm.door, sm.street, sm.pipes["db"])
            self.play(Indicate(sm.street.text, color=TURN, scale_factor=1.08), Indicate(net, color=TURN, scale_factor=1.06),
                      run_time=0.6)
            self.play(FadeOut(lot, shift=DOWN * 0.1), run_time=0.7)
            for m in lot:
                sm.remove(m)
            drop(self, lot)
            nc = grey_chip(NET_CHIP).move_to([1.2, 0.4, 0])
            vo.wait_until("so next time run docker-shell.sh first")
            self.play(FadeIn(nc, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 5. ponder: is the project gone?
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(t), FadeOut(VGroup(*t.lines)), run_time=0.5)
            drop(self, t, *t.lines)
            self.play(Indicate(nc.text, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("is your labeled project gone")
            self.play(FadeOut(nc), sm.db.animate.fade(0.5), run_time=0.6)
            drop(self, nc)
            self.play(Indicate(sm.db.text, color=INK, scale_factor=1.1), run_time=0.6)
        pc = ponder(self, PONDER_Q, seconds=6, center=(0, 0.4))

        # ========================================================== 6. the database survived; part 1 closes
        t6 = term(P_LABELING, rows=10)
        hs = grey_chip("hence sudo").next_to(t6.box, UP, buff=0.15).align_to(t6.box, RIGHT)
        m = PipelineMap.at("S08")
        unl = m.bucket1.drawers["cheeses_unlabeled/"]
        ph_a = tile(None, 0.7, CLOUD)
        ph_b = tile(None, 0.7, CLOUD, filled=True)
        pk = VGroup(*[label(s, 24, TURN) for s in PARKED]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        pframe = RoundedRectangle(width=pk.width + 0.7, height=pk.height + 0.5, corner_radius=0.16,
                                  stroke_color=TURN, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        pframe.move_to([0, -2.45, 0])
        pk.move_to(pframe)
        ph_a.next_to(pframe, RIGHT, buff=0.6)
        ph_b.move_to(ph_a)

        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(pc, sm)
            self.play(FadeOut(gone), track(tr, 4, extra=True), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(t6), run_time=0.4)
            ln64 = type_cmd(self, t6, c64.cmd, type_time=0.9)
            xt6 = on_bar(t6, extra_row())
            self.play(FadeIn(xt6), run_time=0.3)
            vo.wait_until("The database file is still in the mounted folder")
            r64 = out(self, t6, ls_align(c64.at((2, 9))), run_time=0.7)
            db = row_with(r64, "label_studio.sqlite3")
            self.play(substring(db, "label_studio.sqlite3").animate.set_color(PASS), run_time=0.5)
            self.play(Indicate(substring(db, "label_studio.sqlite3"), color=PASS, scale_factor=1.1), run_time=0.6)
            self.play(substring(db, "1001").animate.set_color(ROOT), FadeIn(hs, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("and prune never touches folders you mount")
            path = substring(rows_of(ln64)[-1], "docker-volumes/label-studio")
            self.play(Create(under(path, INK, stroke=3)), run_time=0.6)
            vo.wait_until("But the photos they point at can change")
            gone = VGroup(t6, hs, xt6)
            self.play(FadeOut(gone), FadeOut(VGroup(*t6.lines)), run_time=0.5)
            drop(self, gone, *t6.lines)
            self.play(FadeIn(m), run_time=0.6)
            self.play(m.unlight("studio", "cli", "street"), FadeIn(pframe), FadeIn(pk[0], shift=UP * 0.1),
                      run_time=0.8)
            self.play(Indicate(m.bucket1.drawers["cheeses_labeled/"].text, color=INK, scale_factor=1.08),
                      run_time=0.6)
            self.play(FadeIn(ph_a, scale=0.6), FadeIn(pk[1], shift=UP * 0.1),
                      Indicate(unl.text, color=CLOUD, scale_factor=1.08), run_time=0.6)
            vo.wait_until("same name, new picture")
            self.play(ReplacementTransform(ph_a, ph_b), run_time=0.6)
            self.play(Indicate(ph_b, color=CLOUD, scale_factor=1.25), run_time=0.5)
            vo.wait_until("So how do you freeze")
            self.play(FadeIn(pk[2], shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(pk[2], color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("That is part 2")
            self.play(Indicate(m.ver.text, color=INK, scale_factor=1.15), run_time=0.7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
