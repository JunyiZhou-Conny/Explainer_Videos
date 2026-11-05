"""S13 · Command, arguments and the job's badge — tracker [4.2] 1 → 5 (+ gcloud alternative at
step 2), then tracker [4.3] 1 → 9 (+ extra at step 5, extra · Docker's analogue at step 4, gcloud
alternative at step 9); lecture_ref 14 in block 11, with the V7 job strip (slide 14's service | job).

Beats (script.md "## S13"; one voiceover block each):
0. TRACKER [4.2] 1 appears. CONSOLE (README:679-682, illustration) "IAM & Admin →
   Service Accounts · Create service account": the worksheet card `translation-audio-job` flies into
   the ID field. [4.2] 2: the form gives way to V6 BadgeBoard (the web badge with its two ORANGE
   project roles, the two BLUE buckets); the job badge forms with the same two roles; its email
   (two rows) appears under it ("note its email").
1. [4.2] 3: a veiled CONSOLE dialog "YOUR_INPUT_BUCKET → Permissions · Grant access": New principals
   = the job email, Role = Storage Object Viewer, Save; the dialog leaves and the GREEN grant
   "Viewer → input" ties the job badge to the input bucket only. [4.2] 4: the same on the output
   bucket with Storage Object Creator → GREEN "Creator → output"; GREY chip "create · not list,
   open or overwrite". [4.2] 5: GREY chip under the web badge "no bucket chip · its audio goes
   straight to the browser".
2. The web badge leaves; README card (README.md · lines 692–694, Checkpoint) top left; a GREY "you"
   bottom left sends three thin GREY arrows "upload", "execute", "see results". ▶ your turn.
3. [4.2] 2 · gcloud alternative: terminal `laptop · gcloud` (20 pt) types README:711-721 verbatim
   (eleven rows), no output panel (GREY chip). The lecture tag leaves.
4. TRACKER [4.3] 1 (swap). A GREY "you" sends a GREY arrow "Service Account User" to the job badge
   (README:733-735). CONSOLE "Cloud Run → Jobs · Deploy container" → "Create job" (README:737-745):
   [4.3] 2 the image URL (GREY dashed chip "the same image as part 2", PINK thread); [4.3] 3 Job
   name `translation-audio`, region, Number of tasks 1.
5. [4.3] 4: CONSOLE "Edit Container · Settings": `python` types into Container command and becomes
   a WHITE chip (Enter). V7 CommandSlots appears under it (ENTRYPOINT: [] · CMD: [python -m
   translation_demo serve], laptop/16:11-12); the python chip drops into the empty ENTRYPOINT slot;
   GREY chip "gcloud help: --command = Entrypoint" (gcloud/07:23).
6. [4.3] 5: the form folds to its "Container arguments" row at the bottom; the block rises. `-m`
   types, then the old CMD lifts out of its slot and fades GREY; the eleven chips fill the slot one
   at a time while they are named (gs:// values PINK, placeholders YELLOW, chip "replace with
   yours"); then python + the eleven slide together into one PINK argv conveyor; GREY chip "no
   shell · one chip = one argv element" (README:750-753).
7. CONSOLE sequence: [4.3] 6 "Variables & Secrets" (the three rows of README:772-776, chip "select
   Done after all three"); [4.3] 7 "Task capacity" (timeout 5, minute, retries 0, 512 MiB, CPU 1,
   tasks 1; README:778-780) + GOLD cost tag; [4.3] 8 "Security · Service account" = the job email,
   chip "choose by email · the selector shows the name"; [4.3] 9 "Execute job immediately"
   unchecked, Create. ▶ your turn.
8. [4.3] 5 · extra. V7 replay: python + the eleven chips melt into ONE fat chip; a 5-row `laptop`
   terminal types laptop/44 line 1 (extra, soft-wrapped) → TERM(laptop/44: 2 from
   "(ModuleNotFoundError", wrap) RED; the leading space of the module name and its cut at
   "passage" ring RED. The terminal gives way to README card (README.md · lines 751–752).
9. V7 resets: ENTRYPOINT [] empty again, the eleven chips (gs:// shortened) in the CMD slot.
   PONDER (8 s) under the block.
10. [4.3] 4 · extra · Docker's analogue: `-m` slides into the program slot and turns RED. 5-row
    terminal: laptop/45 line 1 (extra, folds) → TERM(laptop/45: 2 from "exec:", wrap) RED, row tag
    "exit 127", title-bar tag "extra · Docker's analogue".
11. The third case: V7 LifecycleStrips (job strip), with LECTURE 14 · 14 until block 12; the image's own `serve` lights, `batch` dims;
    the job strip grows an ear, never reaches its edge and hits the RED wall "task timeout 5 min";
    README card (README.md · line 1044).
12. [4.3] 9 · gcloud alternative: terminal `laptop · gcloud` (20 pt) types README:816-821 verbatim,
    no output panel; the --args value splits at its commas into the eleven chips above it; GREY
    chip "gcloud help: --command = Entrypoint" (gcloud/07:23). Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _field_box

SAY = NARRATION["S13"]

FORM_UL = np.array([-6.45, 2.72, 0])                 # forms hang from here, under the tracker
REGION_VALUE = f"{REGION} ({REGION_CITY})"         # as S08 fills it
PONDER_Q = ("You fill all eleven argument chips but leave Container command empty.\n"
            "What does the container try to run?")      # script.md's 3 rows as 2: the block stays visible
HELP_CHIP = "gcloud help: --command = Entrypoint"    # gcloud/07:22-23


def form_at(f: VGroup) -> VGroup:
    return f.move_to(FORM_UL, aligned_edge=UL)


def ill_for(f: VGroup) -> VGroup:
    """The illustration tag on the form's top edge, right end."""
    tg = illustration_tag()
    return tg.move_to(f.frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))


def wide_form(title: str, rows, wide_label: str, wide_value: str, at: int = 0, path: str | None = None) -> VGroup:
    """console_form with one long field (the image URL, an account email) on its own row under its
    label (as S08's image_form): a 60-character value does not fit beside a label column."""
    vw = mono(wide_value, 20).width
    f = console_form(title, rows, form_w=vw + 1.2, path=path)
    items = f.rows
    lt = label(wide_label, 20, S.GREY)
    fb = _field_box(vw + 0.4, 20)
    vt = mono("|", 20).set_opacity(0)
    fb.next_to(lt, DOWN, buff=0.12, aligned_edge=LEFT)
    vt.move_to(fb).align_to(fb, LEFT).shift(RIGHT * 0.15)
    row = VGroup(lt, fb, vt)
    row.label, row.field, row.value, row.kind = lt, fb, vt, "field"
    items.submobjects.insert(at, row)
    items.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    frame, sep, head = f.frame, f[1], f[2]
    body = VGroup(head, items).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    frame.stretch_to_fit_height(body.height + 0.6)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    sep.move_to([frame.get_center()[0], head.get_bottom()[1] - 0.15, 0])
    return f


def groups_of(rows):
    """README rows grouped into commands (a row after a trailing '\\' continues)."""
    groups, cur = [], []
    for r in rows:
        cur.append(r)
        if not r.rstrip().endswith("\\"):
            groups.append(cur)
            cur = []
    assert not cur, groups
    return groups


def row_with(lines, sub):
    """The first terminal row among typed/printed lines whose text contains `sub`."""
    for ln in lines:
        for r in rows_of(ln):
            if sub in getattr(r, "text", ""):
                return r
    raise ValueError(sub)


class CommandAndArgs(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S13"] == 13, len(SAY)
        assert "`translation-audio-job`" in readme(680)
        assert "Storage Object Viewer" in readme(685) and "Storage Object Creator" in readme(687)
        assert readme(692).startswith("**Checkpoint:**") and readme(694).endswith("read results.")
        assert readme(742) == IMAGE_REF and "`translation-audio`" in readme(745)
        assert "`python`" in readme(747) and "Do not paste the whole block" in readme(751)
        assert readme(1044).startswith("| Job starts a server instead of finishing")
        assert "--command=python" in readme(818) and readme(819).strip().startswith("--args=")
        c44, c45, c07 = capture("laptop/44"), capture("laptop/45"), capture("gcloud/07")
        assert c44.k == 1 and c45.k == 1 and c44.exit == 1 and c45.exit == 127
        assert "--command" in c07.line(22) and c07.line(23).strip().startswith("Entrypoint for the container image")
        rows_42 = readme_rows(711, 721)
        rows_43 = readme_rows(816, 821)
        assert len(rows_42) == 11 and len(rows_43) == 6

        # ========================================================== 0. its own identity: create, two roles, email
        tr = tracker_42(1)
        ref = lref("14")
        f0 = form_at(console_form("Create service account",
                                  [("Service account ID", ""), ("button", "Create and continue")],
                                  form_w=8.0, path="IAM & Admin → Service Accounts"))
        ill0 = ill_for(f0)
        ws = worksheet_card(JOB_SA, "job account").move_to([-2.45, -1.2, 0])
        board = BadgeBoard()
        at = JOB_EMAIL.index("@") + 1
        em = VGroup(label("its email", 20, S.GREY), mono(JOB_EMAIL[:at], 20, INK),
                    mono(JOB_EMAIL[at:], 20, INK)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        em.move_to([-6.3, -2.35, 0], aligned_edge=UL)
        assert em.get_bottom()[1] > -3.55 and em.get_right()[0] < 1.0, em.get_corner(DR)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(f0, shift=UP * 0.1), FadeIn(ill0), run_time=0.5)
            vo.wait_until("Create translation-audio-job")
            self.play(FadeIn(ws, shift=UP * 0.2), run_time=0.4)
            self.play(ws.animate.move_to(f0.rows[0].field).set_opacity(0), f0.fill(0, JOB_SA), run_time=0.9)
            self.remove(ws)
            self.play(f0.press(1), run_time=0.5)
            vo.wait_until("give it the same two project roles")
            self.play(track(tr, 2), FadeOut(VGroup(f0, ill0)), run_time=0.5)
            self.play(FadeIn(board), run_time=0.5)
            board.job_badge(self, run_time=0.9)
            self.play(Indicate(board.job.roles, color=SHARED, scale_factor=1.05),
                      Indicate(board.web.roles, color=SHARED, scale_factor=1.05), run_time=0.7)
            vo.wait_until("and note its email")
            self.play(FadeIn(em, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 1. per-bucket grants; the web account needs neither
        veil = Rectangle(width=13.1, height=6.4, stroke_width=0).set_fill(S.BG, 0.82).move_to([0, -0.36, 0])

        def grant_form(bkt):
            f = wide_form("Grant access", [("Role", ""), ("button", "Save")], "New principals", JOB_EMAIL,
                          path=f"{bkt} → Permissions")
            return f.move_to([0, -0.3, 0])
        g_in, g_out = grant_form(IN_BUCKET), grant_form(OUT_BUCKET)
        ill_in, ill_out = ill_for(g_in), ill_for(g_out)
        assert g_in.frame.get_top()[1] < TRACK_BOTTOM - 0.05 and g_in.width < 13.0
        with self.voiceover(SAY[1]) as vo:
            self.play(track(tr, 3), FadeOut(em), run_time=0.4)
            self.play(FadeIn(veil), FadeIn(g_in, shift=UP * 0.1), FadeIn(ill_in), run_time=0.5)
            self.play(g_in.fill(0, JOB_EMAIL), run_time=0.7)
            vo.wait_until("Storage Object Viewer on the input")
            self.play(g_in.fill(1, "Storage Object Viewer", OWN), run_time=0.6)
            self.play(g_in.press(2), run_time=0.4)
            self.play(FadeOut(VGroup(g_in, ill_in, veil)), run_time=0.35)
            board.grant(self, "input", run_time=0.7)
            vo.wait_until("and Storage Object Creator on the output")
            self.play(track(tr, 4), FadeIn(veil), FadeIn(g_out, shift=UP * 0.1), FadeIn(ill_out), run_time=0.45)
            self.play(g_out.fill(0, JOB_EMAIL), run_time=0.45)
            self.play(g_out.fill(1, "Storage Object Creator", OWN), run_time=0.5)
            self.play(g_out.press(2), run_time=0.35)
            self.play(FadeOut(VGroup(g_out, ill_out, veil)), run_time=0.35)
            cre = board.grant(self, "output", run_time=0.7)
            vo.wait_until("which adds files")
            note = grey_chip("create · not list, open or overwrite")
            note.next_to(cre, DOWN, buff=0.2)
            note.shift(RIGHT * (board.buckets["output"].get_left()[0] - 0.2 - note.get_right()[0]))
            assert note.get_top()[1] < board.job.roles.get_bottom()[1] - 0.1 or \
                note.get_left()[0] > board.job.roles.get_right()[0] + 0.1, note.get_corner(UL)
            assert note.get_bottom()[1] > -3.55
            board.show(self, note, run_time=0.5)
            self.play(Indicate(note.text, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("The web account needs neither")
            self.play(track(tr, 5), run_time=0.4)
            web_note = board.web_note(self, run_time=0.5)
            self.play(Indicate(board.web.badge.text, color=CLOUD, scale_factor=1.06), run_time=0.6)

        # ========================================================== 2. checkpoint: your own identity needs rights too
        body2 = ("Checkpoint: … Your own console/CLI identity\n"     # three rows: the card stays
                 "needs separate permission to upload passages,\n"   # left of the Viewer grant
                 "launch executions, and read results.")
        rc = readme_card((692, 694), body2, size=20).move_to(FORM_UL, aligned_edge=UL)
        me = you("you").move_to([-5.7, -2.65, 0])
        verbs = ("upload", "execute", "see results")
        arrows, words = VGroup(), VGroup()
        for k, w in enumerate(verbs):
            y = -2.15 - 0.5 * k
            a = Arrow(me.figure.get_right() + RIGHT * 0.1, [-3.6, y, 0], buff=0.05, color=S.GREY,
                      stroke_width=2.5, tip_length=0.15, max_tip_length_to_length_ratio=0.12)
            arrows.add(a)
            words.add(label(w, 20, S.GREY).next_to([-3.6, y, 0], RIGHT, buff=0.15))
        yt = your_turn()
        assert rc.get_right()[0] < board.grants["input"][1].get_left()[0] - 0.15, (rc.get_right(), board.grants["input"][1].get_left())
        assert rc.get_right()[0] < 6.5 and rc.get_bottom()[1] > board.job.badge.get_top()[1] + 0.05, rc.get_corner(DR)
        assert words.get_top()[1] < board.job.roles.get_bottom()[1] - 0.1, (words.get_top(), board.job.roles.get_bottom())
        with self.voiceover(SAY[2]) as vo:
            board.drop(self, board.web, web_note, run_time=0.5)
            self.play(FadeIn(rc, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Your own identity")
            self.play(FadeIn(me, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("to upload, execute and see results")
            for a, w in zip(arrows, words):
                self.play(GrowArrow(a), FadeIn(w, shift=RIGHT * 0.1), run_time=0.45)
            self.play(Indicate(rc.body[1:], color=TURN, scale_factor=1.03), run_time=0.7)
            vo.wait_until("Pause and create the account")
            yt.next_to(words, RIGHT, buff=0.6).align_to(words, DOWN)
            assert yt.get_right()[0] < board.grants["output"][1].get_left()[0] + 2.5
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)

        # ========================================================== 3. the gcloud alternative (README:711-721)
        gt = term(P_REPO, 14, T_GCLOUD, size=20)
        assert gt.box.get_top()[1] < TRACK_BOTTOM - 0.05, gt.box.get_top()
        npc = no_panel_chip()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(board, rc, me, arrows, words, yt)), track(tr, 2, "gcloud"), run_time=0.6)
            self.play(FadeIn(gt, shift=UP * 0.15), run_time=0.4)
            typed = []
            for g in groups_of(rows_42):
                typed += type_lines(self, gt, g, type_time=0.9 / len(g))
            npc.move_to([6.5 - npc.width / 2, (gt.box.get_top()[1] + TRACK_BOTTOM) / 2 - 0.05, 0])
            if npc.get_left()[0] < tr.get_right()[0] + 0.2 or npc.get_bottom()[1] < gt.box.get_top()[1]:
                under_term(gt, npc)
            self.play(FadeIn(npc, shift=DOWN * 0.1), run_time=0.4)
            self.wait(0.6)

        # ========================================================== 4. Service Account User; Create job
        tr43 = tracker_43(1)
        me4 = you("you").move_to([-4.8, 0.2, 0])
        jb = badge(JOB_SA).move_to([2.6, 0.35, 0])
        sau = Arrow(me4.figure.get_right() + RIGHT * 0.1, jb.get_left(), buff=0.1, color=S.GREY, stroke_width=3,
                    tip_length=0.2)
        sau_t = label("Service Account User", 20, S.GREY).next_to(sau, UP, buff=0.12)
        jobs = form_at(console_form("Jobs", [("button", "Deploy container")], form_w=8.0, path="Cloud Run"))
        ill_j = ill_for(jobs)
        cj = form_at(wide_form("Create job", [("Job name", ""), ("Region", ""), ("Number of tasks", "")],
                               "Container image URL", IMAGE_REF, path="Cloud Run → Jobs"))
        ill_c = ill_for(cj)
        assert cj.frame.get_bottom()[1] > -2.6 and cj.frame.get_right()[0] < 6.55, cj.frame.get_corner(DR)
        same = dashed_chip("the same image as part 2").move_to([0, -3.05, 0])
        same.align_to(cj.frame, LEFT)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(gt, npc)), run_time=0.5)
            self.remove(gt)
            tr43 = swap_tracker(self, tr, tr43)
            vo.wait_until("attaching this account again")
            self.play(FadeIn(me4, shift=UP * 0.1), FadeIn(jb, scale=0.8), run_time=0.5)
            vo.wait_until("takes your Service Account User")
            self.play(GrowArrow(sau), FadeIn(sau_t, shift=UP * 0.1), run_time=0.7)
            self.play(Indicate(sau_t, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("In Cloud Run, Jobs")
            self.play(FadeOut(VGroup(me4, jb, sau, sau_t)), run_time=0.4)
            self.play(FadeIn(jobs, shift=UP * 0.1), FadeIn(ill_j), run_time=0.4)
            vo.wait_until("Deploy container opens Create job")
            self.play(jobs.press(0), run_time=0.6)
            self.play(FadeOut(VGroup(jobs, ill_j)), FadeIn(cj, shift=UP * 0.1), FadeIn(ill_c), run_time=0.6)
            self.play(Indicate(cj.title_text, color=TURN, scale_factor=1.06), run_time=0.5)
            vo.wait_until("The same image")
            self.play(track(tr43, 2), FadeIn(same, shift=UP * 0.1), run_time=0.4)
            self.play(cj.fill(0, IMAGE_REF), run_time=0.8)
            v = cj.rows[0].value
            thread = CubicBezier(same.get_top() + UP * 0.05, same.get_top() + np.array([0.6, 1.0, 0]),
                                 v.get_bottom() + np.array([-0.6, -0.8, 0]), v.get_bottom() + DOWN * 0.08)
            thread.set_stroke(ROUTE, 3)
            self.play(Create(thread), Indicate(v, color=ROUTE, scale_factor=1.03), run_time=0.6)
            vo.wait_until("the name translation-audio")
            self.play(track(tr43, 3), FadeOut(thread), run_time=0.3)
            self.play(cj.fill(1, JOB), run_time=0.6)
            self.play(cj.fill(2, REGION_VALUE), run_time=0.6)
            vo.wait_until("1 task")
            self.play(cj.fill(3, "1", TURN), run_time=0.4)

        # ========================================================== 5. Container command: python fills ENTRYPOINT
        fs = form_at(console_form("Edit Container · Settings",      # README:746-747: how to reach it
                                  [("Container command", ""), ("Container arguments", "")], form_w=7.6,
                                  path="Containers, Connections, Security → Containers"))
        # beside the form, not on its top edge: step 4's long tracker caption ends over that edge
        ill_s = illustration_tag().next_to(fs.frame, RIGHT, buff=0.2).align_to(fs.frame, UP)
        assert ill_s.get_top()[1] < TRACK_BOTTOM - 0.05 and ill_s.get_right()[0] < 6.55, ill_s.get_corner(UR)
        cs = CommandSlots(slot_w=8.6)
        cs.shift(np.array([0, fs.frame.get_bottom()[1] - 0.25 - cs.block.get_top()[1], 0]))
        assert cs.block.get_bottom()[1] > -3.55, cs.block.get_bottom()
        py = chip_row(["python"]).chips[0]
        py.move_to(fs.rows[0].field).align_to(fs.rows[0].field, LEFT).shift(RIGHT * 0.12)
        hc = grey_chip(HELP_CHIP).next_to(fs.frame, RIGHT, buff=0.2).align_to(fs.frame, DOWN)
        assert hc.get_right()[0] < 6.55, hc.get_right()
        with self.voiceover(SAY[5]) as vo:
            self.play(track(tr43, 4), FadeOut(VGroup(cj, ill_c, same)), run_time=0.5)
            self.play(FadeIn(fs, shift=UP * 0.1), FadeIn(ill_s), run_time=0.5)
            vo.wait_until("Container command: python")
            self.play(fs.fill(0, "python"), run_time=0.6)
            vo.wait_until("then Enter to make a chip")
            self.play(ReplacementTransform(fs.rows[0].value, py), run_time=0.5)
            fs.rows[0].value = py
            fs.rows[0].add(py)
            self.add(fs, ill_s)
            self.play(Indicate(py.text, color=TURN, scale_factor=1.15), run_time=0.5)
            vo.wait_until("It fills the entrypoint slot")
            self.play(FadeIn(cs, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(cs.entry_content, color=TURN, scale_factor=1.4), run_time=0.5)
            cs.set_command(self, "python", run_time=0.7)
            vo.wait_until("which this image left empty")
            self.play(FadeIn(hc, shift=LEFT * 0.1), Indicate(cs.entry_name, color=TURN, scale_factor=1.1),
                      run_time=0.6)

        # ========================================================== 6. eleven argument chips take CMD's place; argv
        fa = console_form("Edit Container · Settings", [("Container arguments", "")], form_w=7.4)
        fa.move_to([-6.45, -1.68, 0], aligned_edge=UL)
        ill_a = illustration_tag().next_to(fa.frame, RIGHT, buff=0.2).align_to(fa.frame, UP)
        enter = grey_chip("one value, then Enter · eleven times").next_to(fa.frame, RIGHT, buff=0.2)
        enter.align_to(fa.rows[0].field, DOWN)
        assert enter.get_right()[0] < 6.55, enter.get_right()
        up = 2.75 - cs.block.get_top()[1]
        assert fa.frame.get_bottom()[1] > -3.55, fa.frame.get_bottom()
        with self.voiceover(SAY[6]) as vo:
            self.play(track(tr43, 5), FadeOut(VGroup(hc, fs, ill_s)), cs.animate.shift(UP * up), run_time=0.7)
            self.play(FadeIn(fa, shift=UP * 0.1), FadeIn(ill_a), run_time=0.4)
            self.play(fa.fill(0, "-m"), FadeIn(enter, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("each its own chip")
            self.play(Indicate(fa.rows[0].value, color=INK, scale_factor=1.3), run_time=0.6)
            vo.wait_until("they take the command slot")
            cs.clear_cmd(self, run_time=0.8)
            assert cs.block.get_top()[1] < PIC_TOP
            vo.wait_until("Dash m")
            v6 = fa.rows[0].value
            fa.rows[0].remove(v6)
            self.play(FadeOut(v6), run_time=0.2)
            chips = cs.add_args(self, ARGS, run_time=6.2)
            assert cs.block.get_bottom()[1] > fa.frame.get_top()[1] + 0.05, (cs.block.get_bottom(), fa.frame.get_top())
            ry = chip("replace with yours", TURN, size=20)      # under the block, beside the form's tag
            ry.move_to([6.45 - ry.width / 2, ill_a.get_center()[1], 0])
            assert ry.get_left()[0] > ill_a.get_right()[0] + 0.2 and ry.get_top()[1] < cs.block.get_bottom()[1] - 0.05
            self.play(FadeIn(ry, shift=LEFT * 0.1),
                      *[Indicate(c.text, color=TURN, scale_factor=1.05) for c in chips if c.value.startswith("gs://")],
                      run_time=0.6)
            vo.wait_until("Each chip is one item")
            self.play(FadeOut(VGroup(fa, ill_a, ry, enter)), run_time=0.4)
            for c in [cs.command_chip, *cs.arg_chips]:     # above the slots conveyor() fades (they
                c.set_z_index(5)                           # are re-added on top and would veil them)
            cs.conveyor(self, run_time=1.1)
            ns = grey_chip("no shell · one chip = one argv element").next_to(cs.block, DOWN, buff=0.3)
            assert ns.get_bottom()[1] > -3.55
            self.play(FadeIn(ns, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 7. variables, timeout and retries, account, Create
        fv = form_at(console_form("Variables & Secrets",
                                  [("ENABLE_SPEECH", ""), ("GOOGLE_CLOUD_PROJECT", ""),
                                   ("GOOGLE_CLOUD_LOCATION", ""), ("button", "Done")],
                                  form_w=8.6, path="Edit Container"))
        ill_v = ill_for(fv)
        dn = grey_chip("select Done after all three").next_to(fv, DOWN, buff=0.3).align_to(fv, LEFT)
        fc = form_at(console_form("Task capacity",
                                  [("Task timeout", ""), ("Time unit", ""),
                                   ("Number of retries per failed task", ""), ("Memory", "512 MiB"),
                                   ("CPU", "1"), ("Number of tasks", "1")], form_w=8.6, path="Edit Container"))
        ill_c2 = ill_for(fc)
        cost = cost_tag("retries repeat paid work · keep 0 · a 5-min ceiling")
        cost.next_to(fc, DOWN, buff=0.2).align_to(fc, LEFT)
        assert cost.get_bottom()[1] > -3.55 and cost.get_right()[0] < 6.55, cost.get_corner(DR)
        fsec = form_at(wide_form("Security", [], "Service account", JOB_EMAIL, path="Create job"))
        ill_sec = ill_for(fsec)
        sel = grey_chip("choose by email · the selector shows the name").next_to(fsec, DOWN, buff=0.3)
        sel.align_to(fsec, LEFT)
        fcr = form_at(console_form("Create job", [("check", "Execute job immediately", False),
                                                  ("button", "Create")], form_w=8.6))
        ill_cr = ill_for(fcr)
        yt7 = your_turn().next_to(fcr, DOWN, buff=0.3).align_to(fcr, LEFT)
        with self.voiceover(SAY[7]) as vo:
            self.play(track(tr43, 6), FadeOut(VGroup(cs, ns)), run_time=0.5)
            self.remove(cs)
            self.play(FadeIn(fv, shift=UP * 0.1), FadeIn(ill_v), run_time=0.4)
            self.play(fv.fill(0, "true"), run_time=0.35)
            self.play(fv.fill(1, "Your project ID"), run_time=0.45)
            self.play(fv.fill(2, SPEECH_LOCATION), run_time=0.4)
            self.play(fv.press(3), FadeIn(dn, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a task timeout of 5 minutes")
            self.play(track(tr43, 7), FadeOut(VGroup(dn, fv, ill_v)), FadeIn(fc, shift=UP * 0.1), FadeIn(ill_c2),
                      run_time=0.6)
            self.play(fc.fill(0, "5", TURN), fc.fill(1, "minute"), run_time=0.5)
            vo.wait_until("and 0 retries")
            self.play(fc.fill(2, "0", TURN), run_time=0.4)
            vo.wait_until("because a retry repeats paid work")
            self.play(FadeIn(cost, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(cost.text, color=COST, scale_factor=1.04), run_time=0.6)
            vo.wait_until("On Security")
            self.play(track(tr43, 8), FadeOut(VGroup(cost, fc, ill_c2)), FadeIn(fsec, shift=UP * 0.1),
                      FadeIn(ill_sec), run_time=0.6)
            vo.wait_until("choose the job's account by its email")
            self.play(fsec.fill(0, JOB_EMAIL), run_time=0.8)
            self.play(FadeIn(sel, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Leave Execute job immediately unchecked")
            self.play(track(tr43, 9), FadeOut(VGroup(sel, fsec, ill_sec)), FadeIn(fcr, shift=UP * 0.1),
                      FadeIn(ill_cr), run_time=0.6)
            self.play(Indicate(fcr.rows[0].mark, color=TURN, scale_factor=1.5), run_time=0.6)
            vo.wait_until("then select Create")
            self.play(fcr.press(1), run_time=0.6)
            vo.wait_until("pause and build it")
            self.play(FadeIn(yt7, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, yt7, TURN)

        # ========================================================== 8. one fat chip: python looks for a module
        cs2 = CommandSlots(slot_w=8.6)
        cs2.shift(UP * (2.75 - cs2.block.get_top()[1]))
        t8 = term(P_REPO, 4, T_LAPTOP, size=20)
        ex8 = on_bar(t8, extra_row())
        rc8 = readme_card((751, 752), "Do not paste the whole block\ninto one argument field.", size=22)
        with self.voiceover(SAY[8]) as vo:
            self.play(track(tr43, 5, True), FadeOut(VGroup(fcr, ill_cr, yt7)), run_time=0.5)
            self.play(FadeIn(cs2), run_time=0.4)
            cs2.set_command(self, "python", run_time=0.4)
            cs2.add_args(self, ARGS, run_time=0.9)
            vo.wait_until("Paste all eleven into one chip")
            fat = cs2.one_chip(self, run_time=1.0)
            assert cs2.block.get_bottom()[1] > t8.box.get_top()[1] + 0.2, (cs2.block.get_bottom(), t8.box.get_top())
            self.play(Indicate(fat.rows, color=TURN, scale_factor=1.03), run_time=0.5)
            vo.wait_until("and Python looks for a module")
            self.play(FadeIn(t8, shift=UP * 0.15), FadeIn(ex8), run_time=0.4)
            type_cmd(self, t8, c44.cmd, type_time=1.2, soft=True)    # soft-wrapped like a real terminal
            errs = out(self, t8, [from_phrase(c44.line(2), "(ModuleNotFoundError")], wrap=True, color=ERR,
                       run_time=0.5)
            vo.wait_until("The name is cut at the first dot")
            lead = ring(substring(row_with(errs, "named '"), "' t", ), ERR, buff=0.05)
            endr = ring(substring(row_with(errs, "passage'"), "passage'"), ERR, buff=0.05)
            self.play(Create(lead), run_time=0.4)
            self.play(Create(endr), run_time=0.4)
            self.add(t8, lead, endr)
            self.play(Indicate(endr, color=ERR, scale_factor=1.08), run_time=0.6)
            rc8.move_to([0, (t8.box.get_top()[1] + BOTTOM) / 2, 0])
            self.play(FadeOut(VGroup(t8, ex8, lead, endr)), FadeIn(rc8, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(rc8.body, color=TURN, scale_factor=1.04), run_time=0.8)

        # ========================================================== 9. the other mistake: no command (PONDER)
        with self.voiceover(SAY[9]) as vo:
            vo.wait_until("You fill all eleven argument chips")
            self.play(FadeOut(rc8), run_time=0.4)
            cs2.reset(self, ARGS_SHORT, run_time=1.0)
            self.play(Indicate(VGroup(*[c.text for c in cs2.arg_chips]), color=TURN, scale_factor=1.03), run_time=0.6)
            vo.wait_until("but leave Container command empty")
            self.play(Indicate(cs2.entry_content, color=TURN, scale_factor=1.6),
                      Indicate(cs2.entry_name, color=TURN, scale_factor=1.1), run_time=0.8)
        pc = ponder(self, PONDER_Q, 8, center=(0, -2.28), width=12.6)
        assert pc.get_top()[1] < cs2.block.get_bottom()[1] - 0.05, (pc.get_top(), cs2.block.get_bottom())

        # ========================================================== 10. -m becomes the program; Docker's analogue
        t10 = term(P_REPO, 4, T_LAPTOP, size=20)
        assert cs2.block.get_bottom()[1] > t10.box.get_top()[1] + 0.2, (cs2.block.get_bottom(), t10.box.get_top())
        an = on_bar(t10, row_tag("extra · Docker's analogue"))
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            vo.wait_until("The arguments replace the default command")
            self.play(Indicate(cs2.cmd_name, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("with no entrypoint, dash m becomes the program")
            # by hand (CommandSlots.no_command's chip move is overridden by its colour animations)
            first = cs2.arg_chips[0]
            tgt = first.copy().move_to(cs2.entry_slot).align_to(cs2.entry_slot, LEFT).shift(RIGHT * 0.15)
            prog = label("program?", 20, ERR)
            prog.next_to(tgt, RIGHT, buff=0.3)
            cs2.drop(self, cs2.entry_content, extra=[first.animate.move_to(tgt)], run_time=0.7)
            self.play(first[0].animate.set_stroke(ERR), first[1].animate.set_color(ERR), run_time=0.4)
            cs2.heal(self)
            cs2.show(self, prog, run_time=0.4)
            vo.wait_until("Docker's version fails")
            self.play(track(tr43, 4, "Docker's analogue"), FadeIn(t10, shift=UP * 0.15), FadeIn(an), run_time=0.5)
            type_cmd(self, t10, c45.cmd, type_time=1.1, soft=True)
            e10 = out(self, t10, [from_phrase(c45.line(2), "exec:")], wrap=True, color=ERR, run_time=0.4)
            x127 = beside(row_tag("exit 127", ERR), e10[-1])
            pin(self, e10[-1], x127)
            vo.wait_until("executable not found")
            self.play(Indicate(substring(e10[-1], "executable file not found"), color=ERR, scale_factor=1.05),
                      run_time=0.6)
            self.add(t10)
            self.wait(1.0)

        # ========================================================== 11. nothing changed: a server until the timeout
        ls = LifecycleStrips(show=("job",))
        js = ls.job_strip
        for m in (js.segs, js.edge, js.exit_label):        # no batch run to show: endless() drops them
            m.set_opacity(0)
        srv = ls.cmds[0].copy()                             # 'serve' takes the job row's 'batch' place
        both = grey_chip("command and arguments left as the image's default: serve")
        both.next_to(ls.image, RIGHT, buff=0.4)
        assert both.get_right()[0] < 6.55, both.get_right()
        rc11 = readme_card(1044, "Job starts a server instead of finishing · Command python and\n"
                                 "separate batch arguments", size=20)
        rc11.move_to([0, BOTTOM + rc11.height / 2 + 0.02, 0])
        with self.voiceover(SAY[11]) as vo:
            self.play(track(tr43, 4), FadeOut(VGroup(cs2, t10, an)), run_time=0.6)
            self.remove(cs2, t10)
            self.play(FadeIn(ls), FadeIn(both, shift=LEFT * 0.1), FadeIn(ref, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("the job starts the web server")
            self.play(Indicate(ls.cmds[0], color=TURN, scale_factor=1.3), run_time=0.6)
            self.add(srv)
            self.play(srv.animate.move_to(ls.cmds[1]).align_to(ls.cmds[1], LEFT),
                      ls.cmds[1].animate.set_opacity(0), run_time=0.6)
            ls.add(srv)
            ls.endless(self, run_time=2.6)
            assert rc11.get_top()[1] < ls.wall[1].get_bottom()[1] - 0.05, (rc11.get_top(), ls.wall[1].get_bottom())
            vo.wait_until("until the timeout fails it")
            self.play(Indicate(ls.wall[0], color=ERR, scale_factor=1.2), Indicate(ls.wall[1], color=ERR, scale_factor=1.1),
                      FadeIn(rc11, shift=UP * 0.1), run_time=0.7)

        # ========================================================== 12. the gcloud alternative (README:816-821)
        gt12 = term(P_REPO, 10, T_GCLOUD, size=20)
        hc12 = grey_chip(HELP_CHIP)
        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(VGroup(ls, both, rc11, ref)), track(tr43, 9, "gcloud"), run_time=0.5)
            self.remove(ls)
            self.play(FadeIn(gt12, shift=UP * 0.15), run_time=0.4)
            typed12 = type_lines(self, gt12, rows_43, type_time=0.45)
            vo.wait_until("the same eleven values")
            args_rows = [r for r in rows_of(typed12[3])]
            cr = chip_row(ARGS_SHORT, max_w=12.6)          # the --args value split at its commas (gs:// elided)
            cr.rows.move_to([-6.45 + cr.rows.width / 2, gt12.box.get_top()[1] + 0.25 + cr.rows.height / 2, 0])
            assert cr.rows.get_top()[1] < TRACK_BOTTOM - 0.05, (cr.rows.get_top(), gt12.box.get_top())
            rgs = [ring(VGroup(*args_rows), ROUTE, buff=0.05)]
            self.play(*[Create(r) for r in rgs], run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cr.chips], lag_ratio=0.15), run_time=1.2)
            vo.wait_until("with command python")
            cmdrow = row_with(typed12, "--command=python")
            rp = ring(substring(cmdrow, "--command=python"), TURN, buff=0.04)
            hc12.move_to([0, cr.rows.get_center()[1], 0])      # takes the chips' place: no room for both
            self.play(Create(rp), run_time=0.4)
            self.play(FadeOut(VGroup(*cr.chips), shift=UP * 0.2), FadeIn(hc12, shift=UP * 0.2), run_time=0.6)
            self.add(gt12, *rgs, rp)
            self.wait(0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
