"""S15 · From the terminal, then the helper — tracker [4.5] (not lit) → 1 → 4, then tracker [4.6]
1 · extra → 1 → 2. No lecture_ref.

Beats (script.md "## S15"; one voiceover block each):
0. TRACKER [4.5] appears, no step lit yet. README card (README.md · lines 911–914): "Your signed-in
   user needs permission to execute the job with overrides (run.jobs.run and
   run.jobs.runWithOverrides) …". V6 echo: a GREY "you" sends a thin GREY arrow "run with overrides
   · yours" to the BLUE job card; under the job its badge with its own chips (the two ORANGE
   project roles, the two GREEN bucket grants), GREY note "not the badge's".
   GREY chip under the card: the role to ask for, Cloud Run Jobs Executor With Overrides (README:726).
1. [4.5] 1: GREY chip "console only so far? run Terminal setup first" (README:921-922); terminal
   `laptop · gcloud` (20 pt) types the two exports (README:925-926 = gcloud/09:1-2). [4.5] 2: README
   card (README.md · line 929) + GREY chip "short · under 5,000 characters" (README:900-901); it
   types `cp tutorial/app/examples/passage.txt ./passage.txt` (row tag `extra · or write your
   own`, run_steps.sh:281) → (no output); on "Export both bucket names" the two export rows flash;
   then the upload (gcloud/09:3-4) → TERM(gcloud/09: 5 wrap) RED.
2. [4.5] 3: the terminal clears and types README:939-942 verbatim (dedented; the --args row
   soft-wraps), no output panel (GREY chip), `▶ your turn` on the title bar. V7 CommandSlots (the
   saved job: python + the eleven chips) replaces it; the row of chips lifts out and the README's
   override row drops in, run-002 / es YELLOW. A GREY dashed "saved job" card below still shows
   `--dest` `fr` `gs://…/run-001/`. Ghost replay: `--dest es` leaves a gap; a copy of the saved
   card's `--dest fr` slides towards it and is stopped by a RED bar "no merge"; a GREY dashed chip
   "dest = fr (default)" fills the gap; GREY note "left out → the program's default (--dest = fr,
   __main__.py:18), not the job's saved value" (gcloud/08: "an execution will be created with the
   input values").
3. [4.5] 4: terminal types README:948-950 (mkdir + cp), no output panel. RECORDED(expected/
   part4-job-recorded.txt: 12), tag `recorded · README:963-964`.
4. Swap to TRACKER [4.6] 1 · extra. A 14-row terminal types gcloud/11 lines 1-4 (row tag `extra` on
   the --dry-run row) → TERM(gcloud/11: 5 wrap, 6 wrap, 7, 8 wrap); the three `$ gcloud` lines get
   PURPLE number tags 1, 2, 3 and flash as they are named; the run id goes GREY, title-bar tag
   "UTC time + 12 random hex · yours will differ"; V8's prefix tabs (top right, both buckets):
   `run-001/` `run-002/` and a fresh `run-<time>-<hex>/`.
5. [4.6] 1: terminal clears, types gcloud/10 lines 1-4 → TERM(gcloud/10: 5 wrap, 6 wrap, 7, 9, 11,
   13, 14 wrap; blank lines dropped); line 5's `$ gcloud storage cp` PURPLE + PURPLE chip "prints
   each command first"; run id GREY + "yours will differ"; line 14 RED. ▶ your turn on the title
   bar; on "Pause and run it" the terminal clears and retypes the command (all 5 rows visible) for the
   your-turn; GREY chip "README.md · line 1002 · bucket names, without gs://".
6. [4.6] 2: a local results folder (illustration) with the attempt's three files; speech.wav plays
   as a small waveform. RECORDED(expected/part4-job-recorded.txt: 13), tag `recorded ·
   README:992-993`; CODE(tutorial/run_job.py: 66–72) dedented, 20 pt, lines 67–72 YELLOW bars;
   the GREEN receipt flashes. GREY chip (README:1006-1008) "the helper needs Python + signed-in
   gcloud · the job gets ADC from its badge". Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

import textwrap

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S15"]

RUN_JOB = "tutorial/run_job.py"
MAIN_PY = "tutorial/app/translation_demo/__main__.py"
RUN_ID = "run-20261104-093455-9d593d979e7f"          # gcloud/11 (dry run)
RUN_ID_10 = "run-20261104-093454-e2f3270ddd46"       # gcloud/10 (for real)
CP_SAMPLE = "cp tutorial/app/examples/passage.txt ./passage.txt"   # the capture's own step (extra)


def dedent_rows(rows):
    """README rows inside a numbered list carry the list's indent: drop it (continuations keep 2)."""
    return textwrap.dedent("\n".join(rows)).split("\n")


def override_args():
    """The eleven values of README:941's --args, the shell variables as their README placeholders."""
    s = readme(941)
    val = s.split('--args="', 1)[1].split('"', 1)[0]
    vals = val.replace("$INPUT_BUCKET", IN_BUCKET).replace("$OUTPUT_BUCKET", OUT_BUCKET).split(",")
    assert len(vals) == 11 and vals[8] == "es" and "run-002" in vals[4] and "run-002" in vals[10], vals
    return tuple(vals)


def bars_for(panel, ks, color=TURN, opacity=0.16):
    """One translucent bar over the consecutive code lines ks (0-based) of a code panel."""
    ks = list(ks)
    a, b = line_bar(panel.code, ks[0], color, opacity), line_bar(panel.code, ks[-1], color, opacity)
    top, bot = a.get_top()[1], b.get_bottom()[1]
    return VGroup(Rectangle(width=a.width, height=top - bot, stroke_width=0).set_fill(color, opacity)
                  .move_to([a.get_center()[0], (top + bot) / 2, 0]))


def waveform(n: int = 13, w: float = 1.5, h: float = 0.5, color=INK) -> VGroup:
    """A small text-free waveform (deterministic heights)."""
    hs = [0.3, 0.55, 0.8, 0.45, 1.0, 0.65, 0.35, 0.75, 0.95, 0.5, 0.7, 0.4, 0.25]
    g = VGroup(*[Line(ORIGIN, UP * h * hs[i % len(hs)], color=color, stroke_width=4) for i in range(n)])
    g.arrange(RIGHT, buff=(w - n * 0.03) / max(1, n - 1), aligned_edge=ORIGIN)
    for b in g:
        b.move_to([b.get_center()[0], 0, 0])
    return g


class FromTheTerminal(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S15"] == 7, len(SAY)
        assert readme(911).startswith("Your signed-in user needs permission to execute the job **with overrides**")
        assert "`run.jobs.run` and `run.jobs.runWithOverrides`" in readme(912)
        assert "expand **Terminal setup**" in readme(921)
        assert "**Cloud Run Jobs Executor With" in readme(726) and readme(727).startswith("Overrides**")
        assert readme(929).startswith("2. Save a new short UTF-8 passage as `passage.txt` on your laptop")
        assert "limited to 5,000" in readme(900) and readme(901).startswith("characters")
        assert "the\njob's saved defaults still point to the first French example" in excerpt("README.md", 954, 955)
        assert "`Downloaded results` only after finding" in excerpt("README.md", 992, 993).replace("\n", " ")
        assert "Supply bucket **names**, without `gs://`" in readme(1002)
        assert "Python and a signed-in gcloud CLI are enough" in readme(1006)
        assert 'batch.add_argument("--dest", default="fr")' in excerpt(MAIN_PY, 18, 18)
        c08 = capture("gcloud/08")
        assert "an execution will be created with the input values" in " ".join(c08.lines)
        c09 = capture("gcloud/09")
        assert c09.k == 4 and c09.exit == 1
        assert c09.cmd_lines[:2] == dedent_rows(readme_rows(925, 926))
        assert c09.cmd_lines[2:] == dedent_rows(readme_rows(932, 933))
        assert c09.line(5).startswith("ERROR: (gcloud) The project property must be set")
        rows_x = dedent_rows(readme_rows(939, 942))
        assert len(rows_x) == 4 and rows_x[0] == 'gcloud run jobs execute "$JOB_NAME" \\' and rows_x[3] == "  --wait"
        rows_d = dedent_rows(readme_rows(948, 950))
        assert rows_d[0] == "mkdir -p results" and len(rows_d) == 3
        c11, c10 = capture("gcloud/11"), capture("gcloud/10")
        assert c11.k == 4 and c11.cmd_lines[3].endswith("--dry-run") and c11.exit == 0
        assert [s.rstrip(" \\") for s in c11.cmd_lines[:3]] == [s.rstrip(" \\") for s in readme_rows(975, 977)]
        assert c10.cmd_lines == readme_rows(975, 978) and c10.exit == 1
        assert RUN_ID in c11.line(5) and RUN_ID_10 in c10.line(5)
        assert c10.line(14).startswith("Helper stopped") and c10.line(8) == c10.line(10) == c10.line(12) == ""
        new_args = override_args()

        # ========================================================== 0. a permission of yours
        tr = tracker_45()
        body0 = VGroup(
            label("Your signed-in user needs permission to execute the job with overrides", 22, INK,
                  t2c={"with overrides": TURN}),
            VGroup(label("(", 22, INK), mono("run.jobs.run", 20, INK), label("and", 22, INK),
                   mono("run.jobs.runWithOverrides", 20, INK), label(") …", 22, INK)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        k0 = body0[0].text.index("withoverrides")
        wo = VGroup(*body0[0].submobjects[k0:k0 + len("withoverrides")])
        rc0 = readme_card((911, 914), body0)
        rc0.move_to([0, 2.75 - rc0.height / 2, 0])
        assert rc0.get_top()[1] < TRACK_BOTTOM - 0.02 or rc0.get_left()[0] > tr.get_right()[0], rc0.get_top()
        # the role to ask for (README:726-727, section 4.2's restricted-project note)
        role0 = grey_chip("role to ask for: Cloud Run Jobs Executor With Overrides · README:726")
        role0.next_to(rc0, DOWN, buff=0.18).align_to(rc0, LEFT)
        assert role0.get_right()[0] < 6.55 and role0.get_left()[0] > -6.6, role0.get_corner(DR)
        job = worksheet_card(JOB, "job").move_to([1.5, 0.15, 0])
        bdg = badge(JOB_SA).next_to(job, DOWN, buff=0.3)
        roles = VGroup(*[chip(r, SHARED, size=20) for r in BadgeBoard.ROLES]).arrange(RIGHT, buff=0.14)
        grants = VGroup(ok_chip("Viewer → input"), ok_chip("Creator → output")).arrange(RIGHT, buff=0.14)
        own = VGroup(roles, grants).arrange(DOWN, buff=0.14).next_to(bdg, DOWN, buff=0.14)
        side = VGroup(job, bdg, own)
        side.move_to([2.3, (role0.get_bottom()[1] - 0.3 + BOTTOM + 0.1) / 2, 0])
        me = you("you").move_to([-5.4, job.get_center()[1] - 0.1, 0])
        ar0 = arrow(me.figure.get_right() + RIGHT * 0.1, job.get_left() + LEFT * 0.1, S.GREY, stroke=3)
        lab0 = label("run with overrides · yours", 20, S.GREY).next_to(ar0, UP, buff=0.12)
        notb = label("not the badge's", 20, S.GREY).next_to(ar0, DOWN, buff=0.12)
        assert side.get_top()[1] < role0.get_bottom()[1] - 0.2 and own.get_bottom()[1] > -3.55, side.get_top()
        assert own.get_right()[0] < 6.55 and own.get_left()[0] > ar0.get_left()[0], own.get_corner(DR)
        assert lab0.get_right()[0] < job.get_left()[0] - 0.05 and notb.get_right()[0] < own.get_left()[0] - 0.05
        assert lab0.get_top()[1] < role0.get_bottom()[1] - 0.15, (lab0.get_top(), role0.get_bottom())
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(rc0, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("First, a permission of yours")
            self.play(Indicate(wo, color=TURN, scale_factor=1.1), run_time=0.8)
            self.add(rc0)
            vo.wait_until("running a job with overrides")
            self.play(FadeIn(me), FadeIn(job, shift=LEFT * 0.1), run_time=0.5)
            self.play(GrowArrow(ar0), FadeIn(lab0, shift=UP * 0.05), run_time=0.7)
            self.play(FadeIn(role0, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("separate from the job account")
            self.play(FadeIn(bdg, scale=0.9), LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in [*roles, *grants]],
                                                          lag_ratio=0.25), run_time=1.0)
            self.play(FadeIn(notb, shift=DOWN * 0.05), Indicate(own, color=INK, scale_factor=1.04), run_time=0.7)

        # ========================================================== 1. setup, a passage, the upload
        t = term(P_REPO, 8, T_GCLOUD, size=20)
        setup = grey_chip("console only so far? run Terminal setup first")
        setup.move_to([-6.4 + setup.width / 2, 2.4, 0])
        rc1 = readme_card(929, "Save a new short UTF-8 passage as passage.txt\non your laptop")
        rc1.move_to([-6.4 + rc1.width / 2, (setup.get_bottom()[1] + t.box.get_top()[1]) / 2, 0])
        short = grey_chip("short · under 5,000 characters").next_to(rc1, RIGHT, buff=0.35)
        assert short.get_right()[0] < 6.55 and rc1.get_bottom()[1] > t.box.get_top()[1] + 0.12, rc1.get_bottom()
        assert setup.get_top()[1] < TRACK_BOTTOM - 0.05 and setup.get_bottom()[1] > rc1.get_top()[1] + 0.12
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(rc0, role0, me, ar0, lab0, notb, side)), track(tr, 1), run_time=0.6)
            self.play(FadeIn(setup, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Run the terminal setup first")
            self.play(FadeIn(t, shift=UP * 0.15), run_time=0.4)
            ex = type_lines(self, t, c09.cmd_lines[:2], type_time=0.5)
            vo.wait_until("Save a short passage")
            self.play(track(tr, 2), FadeIn(rc1, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("under 5,000 characters")
            self.play(FadeIn(short, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("as passage dot txt")
            self.play(Indicate(rc1, color=INK, scale_factor=1.04), run_time=0.7)
            self.add(rc1)
            vo.wait_until("or copy the sample")
            cpl = type_cmd(self, t, CP_SAMPLE, type_time=0.6)
            tag1 = beside(row_tag("extra · or write your own"), cpl, buff=0.15)
            assert tag1.get_right()[0] < t.box.get_right()[0] - 0.1, (tag1.get_right(), t.box.get_right())
            pin(self, cpl, tag1)
            bare_prompt(self, t)
            vo.wait_until("Export both bucket names")
            self.play(each([*ex], TURN, scale=1.04, lag=0.3), run_time=0.8)
            self.add(t)
            vo.wait_until("and upload it under run")
            type_lines(self, t, c09.cmd_lines[2:], type_time=0.6)
            vo.wait_until("it stops at the placeholder again")
            out(self, t, [c09.line(5)], wrap=True, color=ERR, run_time=0.5)

        # ========================================================== 2. execute with overrides
        npc2 = under_term(t, no_panel_chip())
        yt2 = on_bar(t, turn_row())
        # the saved job: python + the eleven chips (S13's state), built in place (no animation)
        cs = CommandSlots(slot_w=8.6)
        py = chip_row(["python"]).chips[0]
        cs._in_slot(py, cs.entry_slot)
        cs.remove(cs.entry_content, cs.cmd_content)
        cs.entry_content, cs.command_chip, cs.cmd_content = py, py, None
        cr = chip_row(ARGS, max_w=cs.slot_w - 0.3)
        need = max(0.52, cr.rows.height + 0.24)
        top = cs.cmd_slot.get_top()[1]
        cs.cmd_slot.become(cs._slot(cs.slot_w, need).move_to([cs.cmd_slot.get_center()[0], top - need / 2, 0]))
        btop = cs.block.get_top()[1]
        bh = (btop - (top - need)) + 0.35
        cs.block.become(RoundedRectangle(width=cs.block.width, height=bh, corner_radius=0.14, stroke_color=IMAGE,
                                         stroke_width=3).set_fill(IMAGE, 0.1).move_to([cs.block.get_center()[0],
                                                                                       btop - bh / 2, 0]))
        cr.rows.move_to(cs.cmd_slot).align_to(cs.cmd_slot, LEFT).shift(RIGHT * 0.15)
        cs.arg_chips = VGroup(*cr.chips)
        cs.add(py, *cr.chips)
        cs.shift(UP * (2.72 - cs.block.get_top()[1]))
        # the saved job card (behind) and the place for the note
        saved_chips = chip_row(["--dest", "fr", "…/run-001/"])
        saved_chips.chips[2].text.set_color(ROUTE)
        saved = card([saved_chips.rows], head="the saved job", dashed=True)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(setup, rc1, short)), track(tr, 3), run_time=0.5)
            t.clear(self, run_time=0.3)
            type_lines(self, t, rows_x, type_time=0.42)
            self.play(FadeIn(npc2, shift=DOWN * 0.1), FadeIn(yt2), run_time=0.4)
            vo.wait_until("They replace the whole argument list")
            self.play(FadeOut(VGroup(t, npc2, yt2)), run_time=0.4)
            self.remove(t)
            self.play(FadeIn(cs, shift=DOWN * 0.1), run_time=0.5)
            # the saved values first (run-001, fr), so the swap shows what became what
            self.play(each([cs.arg_chips[i].text for i in (4, 8, 10)], INK, scale=1.12, lag=0.15),
                      run_time=0.6)
            self.add(cs)
            # sizes now known: the new row grows the slot only if it wraps differently
            cs.swap_args(self, new_args, hi=(4, 8, 10), run_time=1.2)
            assert cs.block.get_bottom()[1] > -1.6, cs.block.get_bottom()
            saved.move_to([-6.4 + saved.width / 2, BOTTOM + 0.08 + saved.height / 2, 0])
            assert saved.get_top()[1] < cs.block.get_bottom()[1] - 0.15 and saved.get_bottom()[1] > -3.55
            vo.wait_until("a new path and Spanish")
            hi = [cs.arg_chips[i] for i in (4, 8, 10)]
            self.play(each([c.text for c in hi], TURN, scale=1.08, lag=0.3),
                      *[c.box.animate(rate_func=there_and_back).set_stroke(width=5) for c in hi], run_time=1.0)
            cs.heal(self)
            vo.wait_until("The saved job still says French")
            self.play(FadeIn(saved, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(saved_chips.chips[1].text, color=INK, scale_factor=1.3), run_time=0.6)
            vo.wait_until("and a flag you leave out")
            d0, d1 = cs.arg_chips[7], cs.arg_chips[8]
            gap, gap_w = VGroup(d0, d1).get_center(), VGroup(d0, d1).width
            cs.drop(self, d0, d1, run_time=0.5, shift=UP * 0.3)
            ghost = VGroup(saved_chips.chips[0].copy(), saved_chips.chips[1].copy())
            yb_ = cs.block.get_bottom()[1] - 0.07
            wall = Line([gap[0] - 1.0, yb_, 0], [gap[0] + 1.0, yb_, 0], color=ERR, stroke_width=6)
            stop = np.array([gap[0], yb_ - ghost.height / 2 - 0.1, 0])
            nm = label("no merge", 20, ERR).move_to(stop + RIGHT * (ghost.width / 2 + 0.25))
            nm.shift(RIGHT * nm.width / 2)
            assert nm.get_right()[0] < 6.55, nm.get_right()
            assert stop[0] - ghost.width / 2 > saved.get_right()[0] + 0.1 or \
                stop[1] - ghost.height / 2 > saved.get_top()[1] + 0.05, (stop, saved.get_corner(UR))
            self.play(Create(wall), FadeIn(nm), run_time=0.4)
            self.play(ghost.animate.move_to(stop), run_time=0.7)
            self.play(ghost.animate.shift(DOWN * 0.35).set_opacity(0), run_time=0.4)
            self.remove(ghost)
            dflt = dashed_chip("default: fr", S.GREY).move_to(gap)
            note = VGroup(label("left out → the program's default", 20, S.GREY),
                          VGroup(label("(", 20, S.GREY), mono("--dest", 20, S.GREY), label("= fr,", 20, S.GREY),
                                 mono("__main__.py:18", 20, S.GREY), label("),", 20, S.GREY)).arrange(RIGHT, buff=0.08),
                          label("not the job's saved value", 20, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            note.move_to([6.45 - note.width / 2, saved.get_center()[1], 0])
            assert note.get_left()[0] > saved.get_right()[0] + 0.2, (note.get_left(), saved.get_right())
            assert dflt.width < gap_w + 0.1, (dflt.width, gap_w)
            self.play(FadeOut(VGroup(wall, nm)), FadeIn(dflt, shift=UP * 0.2), FadeIn(note, shift=LEFT * 0.1),
                      run_time=0.6)
            self.play(Indicate(dflt.text, color=INK, scale_factor=1.15), run_time=0.7)
            self.wait(0.7)

        # ========================================================== 3. download run-002
        for m in list(t.lines):
            t.lines.remove(m)
        t3 = term(P_REPO, 6, T_GCLOUD, size=20)
        npc3 = under_term(t3, no_panel_chip())
        rec12 = recorded_card("part4-job-recorded", 12, "README:963-964")
        rec12.move_to([0, (npc3.get_top()[1] + 2.8) / 2, 0])
        assert rec12.get_bottom()[1] > npc3.get_top()[1] + 0.15 and rec12.get_top()[1] < 2.85, rec12.get_top()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(cs, saved, dflt, note)), track(tr, 4), run_time=0.5)
            self.remove(cs)
            self.play(FadeIn(t3, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("make the results folder")
            type_lines(self, t3, rows_d[:1], type_time=0.4)
            vo.wait_until("and copy run zero zero two down")
            type_lines(self, t3, rows_d[1:], type_time=0.7)
            self.play(FadeIn(npc3, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("The README's recording")
            self.play(FadeIn(rec12, shift=DOWN * 0.1), run_time=0.6)
            flash_tag(self, rec12.tag, S.GREY)

        # ========================================================== 4. the helper: an extra dry run
        t4 = term(P_REPO, 14, T_GCLOUD, size=20)
        tr46 = tracker_46(1, True)
        o11 = soft(c11.at(5), 72) + soft(c11.at(6), 67) + c11.at(7) + soft(c11.at(8), 72)
        assert len(o11) == 14, len(o11)
        diff4 = on_bar(t4, row_tag("yours will differ"))
        assert diff4.get_left()[0] > t4.title.get_right()[0] + 0.15, diff4.get_left()
        tabs = bucket(None, 0.36)
        tab_items = []
        for s, col in (("run-001/", ROUTE), ("run-002/", ROUTE), ("run-<UTC time>-<hex>/", TURN)):
            tx = mono(s, 20, col)
            bx = RoundedRectangle(width=tx.width + 0.4, height=0.42, corner_radius=0.08, stroke_color=col,
                                  stroke_width=2).set_fill(S.BG, 1)
            tab_items.append(VGroup(bx, tx.move_to(bx)))
        strip = VGroup(tabs, *tab_items).arrange(RIGHT, buff=0.14)
        strip.move_to([6.45 - strip.width / 2, 3.12, 0])
        assert strip.get_left()[0] > tr46.get_right()[0] + 0.2, (strip.get_left(), tr46.get_right())
        assert strip.get_bottom()[1] > t4.box.get_top()[1] + 0.1, (strip.get_bottom(), t4.box.get_top())
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(t3, npc3, rec12)), run_time=0.5)
            self.remove(t3)
            tr = swap_tracker(self, tr, tr46)
            self.play(FadeIn(t4, shift=UP * 0.15), run_time=0.4)
            cmd4 = type_capture(self, t4, c11, type_time=0.45)
            pin(self, cmd4[-1], beside(extra_row(), cmd4[-1], buff=0.3))
            vo.wait_until("An extra dry run")
            rows4 = out(self, t4, o11, run_time=1.2, lag=0.05)
            nums = []
            for k, n in enumerate((0, 3, 10)):
                row = rows4[n]
                assert row.text.startswith("$ gcloud"), row.text
                for g in substring(row, "$ gcloud"):
                    g.set_color(TOOL)
                nt = beside(row_tag(str(k + 1), TOOL), row, buff=0.2)
                pin(self, row, nt, run_time=0.25)
                nums.append(nt)
            vo.wait_until("It uploads to a fresh run folder")
            flash_tag(self, nums[0], TOOL)
            vo.wait_until("named by the time")
            ids = [g for r in rows4 if RUN_ID in r.text for g in substring(r, RUN_ID)]
            self.play(*[g.animate.set_color(S.GREY) for g in ids], FadeIn(diff4), run_time=0.6)
            self.add(t4, diff4)
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.15) for m in strip], lag_ratio=0.25), run_time=0.9)
            vo.wait_until("executes with the eleven arguments")
            flash_tag(self, nums[1], TOOL)
            vo.wait_until("and downloads")
            flash_tag(self, nums[2], TOOL)

        # ========================================================== 5. for real: it stops at the first failure
        o10 = soft(c10.at(5), 72) + soft(c10.at(6), 72) + c10.at(7, 9, 11, 13) + soft(c10.at(14), 72)
        tool5 = tool_chip("prints each command first")
        tool5.move_to([6.45 - tool5.width / 2, 3.12, 0])
        rdm = VGroup(mono("README.md", 20, S.GREY), label("· line 1002 · bucket", 20, S.GREY),
                     label("names", 20, INK), label(", without", 20, S.GREY), mono("gs://", 20, S.GREY))
        rdm.arrange(RIGHT, buff=0.1)
        for m in rdm[1:]:
            m.align_to(rdm[0], DOWN)
        rbox = RoundedRectangle(width=rdm.width + 0.4, height=0.5, corner_radius=0.25, stroke_color=S.GREY,
                                stroke_width=2).set_fill(S.BG, 0.92)
        rdm.move_to(rbox)
        rchip = VGroup(rbox, rdm).move_to([6.45 - (rdm.width + 0.4) / 2, 3.12, 0])
        assert rchip.get_left()[0] > tr46.get_right()[0] + 0.15, rchip.get_left()
        assert tool5.get_left()[0] > tr46.get_right()[0] + 0.15
        diff5 = on_bar(t4, row_tag("yours will differ"))
        yt5 = on_bar(t4, turn_row())
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(strip, diff4)), track(tr, 1), run_time=0.5)
            t4.clear(self, run_time=0.3)
            vo.wait_until("it prints each gcloud command")
            type_capture(self, t4, c10, type_time=0.35)
            rows5 = out(self, t4, o10, run_time=1.0, lag=0.05)
            r5 = [r for r in rows5 if r.text.startswith("$ gcloud storage cp")][0]
            ids5 = [g for r in rows5 if RUN_ID_10 in r.text for g in substring(r, RUN_ID_10)]
            self.play(*[g.animate.set_color(TOOL) for g in substring(r5, "$ gcloud storage cp")],
                      *[g.animate.set_color(S.GREY) for g in ids5],
                      FadeIn(tool5, shift=DOWN * 0.1), FadeIn(diff5), run_time=0.6)
            self.add(t4, diff5)
            vo.wait_until("and stops at the first failure")
            last = list(rows5[-2:])
            assert last[0].text.startswith("Helper stopped") and last[1].text == "run.", [r.text for r in last]
            self.play(*[r.animate.set_color(ERR) for r in last], run_time=0.4)
            self.play(each(last, ERR, scale=1.03, lag=0.2), run_time=0.7)
            self.add(t4, diff5)
            vo.wait_until("Pause and run it")
            # the whole command back on screen (its first rows scrolled off under the output)
            self.play(FadeOut(tool5), FadeOut(diff5), run_time=0.3)
            t4.clear(self, run_time=0.3)
            cmd5 = type_capture(self, t4, c10, type_time=0.25)
            assert all(r.get_top()[1] < t4.box.get_top()[1] - t4.bar_h for r in cmd5), "command scrolled"
            self.play(FadeIn(rchip, shift=DOWN * 0.1), FadeIn(yt5, shift=LEFT * 0.1), run_time=0.5)
            flash_tag(self, yt5, TURN)
            self.wait(1.0)

        # ========================================================== 6. open the results; the receipt again
        # phase A: the local results folder (an illustration) with the attempt's three files
        fold = VGroup(folder_glyph(0.38, LAPTOP), mono("results/run-…/<attempt>/", 20, INK)).arrange(RIGHT, buff=0.12)
        fls = VGroup(*[file_icon(n, OWN if n == "manifest.json" else INK) for n in AttemptFolders.FILES])
        fls.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fls.next_to(fold, DOWN, buff=0.35).align_to(fold, LEFT).shift(RIGHT * 0.4)
        wav = waveform().next_to(fls[1], RIGHT, buff=0.35)
        pic = VGroup(fold, fls, wav).move_to([0, 0.4, 0])
        ill6 = illustration_tag().next_to(pic, RIGHT, buff=0.6).align_to(fold, UP)
        # phase B: the RECORDED line on top, the code under it, the folder row at the bottom
        rec13 = recorded_card("part4-job-recorded", 13, "README:992-993", size=22)
        rec13.move_to([0, 2.72 - rec13.height / 2, 0])
        cp6 = code(RUN_JOB, 66, 72, font_size=20, dedent=True,
                   cuts={68: "json.loads(p.read_text())", 69: "is_file() and", 71: "raise ValueError("})
        cp6.move_to([0, rec13.get_bottom()[1] - 0.25 - cp6.height / 2, 0])
        yb = bars_for(cp6, range(1, 7))
        row_y = (cp6.get_bottom()[1] + BOTTOM) / 2
        fold_b = fold.copy().move_to([-6.4 + fold.width / 2, row_y, 0])
        man_b = fls[2].copy().next_to(fold_b, RIGHT, buff=0.5)
        rcp = receipt().next_to(man_b, RIGHT, buff=0.3)
        ill6_b = ill6.copy().move_to([6.45 - ill6.width / 2, row_y, 0])
        assert rcp.get_right()[0] < ill6_b.get_left()[0] - 0.2, (rcp.get_right(), ill6_b.get_left())
        assert cp6.get_bottom()[1] > fold_b.get_top()[1] + 0.15 and fold_b.get_bottom()[1] > -3.55, cp6.get_bottom()
        assert pic.get_top()[1] < TRACK_BOTTOM - 0.2 and ill6.get_right()[0] < 6.55
        chip6 = grey_chip("the helper needs Python + signed-in gcloud · the job gets ADC from its badge")
        chip6.move_to(cp6.code.background)
        assert chip6.width < 13.0, chip6.width
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(t4, rchip, yt5)), track(tr, 2), run_time=0.6)
            self.remove(t4)
            vo.wait_until("open the result folder")
            self.play(FadeIn(fold, shift=DOWN * 0.1), FadeIn(ill6), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.15) for f in fls], lag_ratio=0.3), run_time=0.8)
            vo.wait_until("and play speech dot wav")
            self.play(Indicate(fls[1], color=TURN, scale_factor=1.1), FadeIn(wav), run_time=0.5)
            self.play(LaggedStart(*[b.animate(rate_func=there_and_back).stretch(1.8, 1) for b in wav],
                                  lag_ratio=0.12), run_time=1.4)
            vo.wait_until("The helper prints downloaded results")
            self.play(FadeOut(VGroup(fls[0], fls[1], wav)), fold.animate.move_to(fold_b),
                      fls[2].animate.move_to(man_b), ill6.animate.move_to(ill6_b), run_time=0.7)
            self.play(FadeIn(rec13, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(cp6, shift=UP * 0.1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(b) for b in yb], lag_ratio=0.15), run_time=0.8)
            vo.wait_until("the receipt again")
            self.play(FadeIn(rcp, scale=1.3), run_time=0.5)
            flash_tag(self, rcp, OWN)
        self.play(FadeOut(VGroup(cp6, yb)), FadeIn(chip6, scale=0.95), run_time=0.6)
        self.wait(1.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
