"""S07 · A project, two keys and a bucket — tracker C1 → C7, lecture_ref 25 (part-1 close).

Beats (script.md, ## S07; one voiceover block each):
0. C1: README card (line 17) + "the README links the repo · we use git clone"; versions chip (00:4–5,
   at the time of recording). Laptop terminal: git clone (01:2), ▶ your turn, cd model-training.
   C1 · extra: git log (02:2; hash and date YELLOW, "the course pin"), ls -la (03:7–23 as mode · size ·
   date · name; the five .sh rows, cli.py and package YELLOW, the six PNG rows GREY + chip).
1. C2: schematic console (illustration): search "Vertex AI API" → ENABLE → "API enabled", ▶ your turn.
   C3: the quota page with the README's labels (filter, the T4 row, regions with us-central1 YELLOW +
   "cli.sh's region · line 14"), the EDIT QUOTAS → new limit → NEXT → name → SUBMIT REQUEST flow,
   README card 43–44, "cli.sh runs on CPU today · the request is for later", ▶ your turn.
2. C4: cd .. → mkdir secrets ("the README shows a tree, not a command") → C4 · extra: tree -L 1 .
   (05:2–6) under README card 55–58; ▶ your turn. The terminal shrinks to a strip; V1's GREEN
   secrets/ drawer lights beside the laptop's repo.
3. C5: console (illustration, README 62–64): Create · model-trainer, the three role chips, Actions ⋮ →
   Manage keys → JSON → Create; a key file drops into secrets/ as model-trainer.json; ▶ your turn.
   C5 · extra: ls -la secrets (06:2–5), the file name ringed, `stand-in`.
4. The honest card, three lines on their sentences; two chips on "named sources".
5. C6: console "Create bucket · your-bucket-placeholder" + README card 71 + "replace this with yours",
   ▶ your turn. C6 · extra: the two curl checks (07: 5, …, 15 · 08: 5 wrap, …, 17) with "the README's
   name · taken · replace this with yours". V1's bucket takes the placeholder name; the GOLD tag.
6. C7: W&B page (illustration, key as dots, Copy), README card 80; export … ; echo (10:2) with the
   placeholder chip, ▶ your turn, `extra` on the echo, `40` + the 40-character note, the optional
   read -rs chip (extra · not captured). V1: the GREEN key chip settles in the laptop.
7. The old terminal closes; a new one slides in ('laptop · new terminal'). PONDER 6 s.
8. echo ${#WANDB_KEY} (11:2) → 0 RED. Part-1 close on V1 (Colab lit, repo lane dashed, key chip,
   bucket named, the hollow cockpit flickers) + "next: the cockpit — and today it won't build".
"""

import re

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F403
from common import _poly
from explainer import style as S

SAY = NARRATION["S07"]
PONDER_ENV = "You exported the key, closed the terminal,\nopened a new one. What does\necho ${#WANDB_KEY} print?"
YELLOW_ROWS = (9, 10, 11, 16, 17, 18, 19)      # 03: the five .sh files, cli.py, package/
PNG_ROWS = (12, 13, 14, 15, 21, 23)            # 03: four quota screenshots, the diagram, the W&B shot


def ls_cols(lines):
    """`ls -la` rows as mode · size · date · name (links/owner/group dropped: the rows are 73–84
    characters, the frame holds 65); text of each kept field unchanged, sizes right-aligned."""
    rows = [ln.split(None, 8) for ln in lines]
    w = max(len(r[4]) for r in rows)
    return [f"{r[0]}  {r[4].rjust(w)}  {r[5]} {r[6]} {r[7]}  {r[8]}" for r in rows]


def top_left(m, x=-6.3, y=2.7):
    m.shift(np.array([x - m.get_left()[0], y - m.get_top()[1], 0]))
    return m


def ill_in(con):
    """The illustration tag inside a console's header row, right end."""
    t = illustration_tag()
    return t.move_to(con.frame.get_corner(UR) + np.array([-0.2 - t.width / 2, -0.32, 0]))


def button(s, color=CLOUD, size=20):
    return chip(s, color, size=size, font=MONO, fill_opacity=0.22)


def tick_box(on=True, color=TURN):
    b = Square(0.26, stroke_color=color, stroke_width=2.5)
    g = VGroup(b)
    if on:
        g.add(check_mark(0.22, color, 4).move_to(b))
    return g


class KeysAndBucket(VoiceScene):
    def keep_only(self, *keep, run_time=0.6, shift=UP * 0.2):
        gone = [m for m in self.mobjects if m not in keep]
        if gone:
            self.play(FadeOut(Group(*gone), shift=shift), run_time=run_time)
            self.remove(*gone)

    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 9, len(SAY)
        c00, c01, c02, c03 = capture("00"), capture("01"), capture("02"), capture("03")
        assert c00.line(4).startswith("Docker client 29.8.2") and c00.line(5).endswith("2.54.0")

        # ========================================================== 0. clone (C1), the two extras
        tr = tracker_c(1)
        ref = lref("25")
        t = laptop_term(6)
        docker_v = re.search(r"client (\S+),", c00.line(4)).group(1)
        git_v = c00.line(5).split()[-1]
        ver = grey_chip(f"Docker {docker_v} · git {git_v} · at the time of recording")
        ver.next_to(t.box, UP, buff=0.12).align_to(t.box, RIGHT)
        rc17 = top_left(readme_card(17))
        how = grey_chip("the README links the repo · we use git clone")
        how.next_to(rc17, DOWN, buff=0.2).align_to(rc17, LEFT)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(t), run_time=0.6)
            self.play(FadeIn(rc17, shift=UP * 0.15), FadeIn(ver), FadeIn(how, shift=UP * 0.15), run_time=0.6)
            type_cmd(self, t, c01.cmd, type_time=1.0)
            o1 = out(self, t, c01.at(2), run_time=0.4)
            vo.wait_until("move into it")
            type_cmd(self, t, "cd model-training", type_time=0.5)
            cd_prompt(self, t, P_REPO, run_time=0.5)
            vo.wait_until("pause and run it")
            yt = beside(turn_row(), o1[-1])
            pin(self, o1[-1], yt, run_time=0.3)
            flash_tag(self, yt, TURN, run_time=0.6)
            vo.wait_until("Two extras show")
            self.play(FadeOut(VGroup(rc17, how, ver), shift=UP * 0.2), track(tr, 1, extra=True), run_time=0.5)
            self.remove(rc17, how, ver)
            resize(self, t, 11, run_time=0.6)
            ex = on_bar(t, extra_row())
            type_cmd(self, t, c02.cmd, type_time=0.8)
            self.play(FadeIn(ex), run_time=0.3)
            lg = out(self, t, c02.at(2), wrap=True, run_time=0.4)
            vo.wait_until("the course pin")
            hsh, day = c02.line(2).split()[:2]
            self.play(substring(lg[0], hsh).animate.set_color(TURN), substring(lg[0], day).animate.set_color(TURN),
                      run_time=0.5)
            pinc = beside(row_tag("the course pin"), lg[-1])
            pin(self, lg[-1], pinc, run_time=0.3)
            vo.wait_until("the repo's files")
            type_cmd(self, t, c03.cmd, type_time=0.4)
            rows03 = ls_cols(c03.at((7, 23)))
            items = []
            for n, s in zip(range(7, 24), rows03):
                items.append((s, TURN) if n in YELLOW_ROWS else (s, S.GREY) if n in PNG_ROWS else s)
            out(self, t, items, run_time=1.0, lag=0.06)
            png = grey_chip("screenshots and a diagram · redrawn in this video")
            png.next_to(t.box, UP, buff=0.12).align_to(t.box, RIGHT)
            self.play(FadeIn(png, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 1. Vertex AI API (C2), GPU quota (C3)
        api = console(("search", "Vertex AI API"), 8.0, 2.9).move_to([-1.2, 0.95, 0])
        api_ill = ill_in(api)
        box_ = RoundedRectangle(width=4.2, height=0.5, corner_radius=0.1, stroke_color=S.GREY, stroke_width=2)
        q = mono("Vertex AI API", 22, INK)
        search = VGroup(box_, q.move_to(box_).align_to(box_, LEFT).shift(RIGHT * 0.2))
        en = button("ENABLE")
        top_row = VGroup(search, en).arrange(RIGHT, buff=0.4)
        top_row.move_to(api.content).align_to(api.content, UP).shift(DOWN * 0.3)
        done = VGroup(check_mark(0.3, PASS), label("API enabled", 22, INK)).arrange(RIGHT, buff=0.18)
        done.next_to(top_row, DOWN, buff=0.45).align_to(top_row, LEFT)
        yt1 = your_turn().next_to(api.frame, RIGHT, buff=0.3).align_to(api.frame, DOWN)

        quota = console(("IAM & Admin", "Quotas"), 8.6, 3.75).move_to([-1.95, 0.85, 0])
        q_ill = ill_in(quota)
        flt = VGroup(label("Filter", 20, S.GREY), chip("Quota: Custom model training", S.GREY, size=20, font=MONO))
        flt.arrange(RIGHT, buff=0.2)
        t4 = label("Custom model training Nvidia T4 GPUs per region", 20, INK)
        t4_box = RoundedRectangle(width=t4.width + 0.4, height=0.5, corner_radius=0.08, stroke_color=S.GREY,
                                  stroke_width=2)
        t4row = VGroup(t4_box, t4.move_to(t4_box))
        uc = VGroup(tick_box(True, TURN), mono(REGION, 22, TURN)).arrange(RIGHT, buff=0.2)
        few = label("Select a few regions", 20, S.GREY)
        reg = VGroup(uc, few).arrange(RIGHT, buff=0.5)
        qcol = VGroup(flt, t4row, reg).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        qcol.move_to(quota.content).align_to(quota.content, LEFT).align_to(quota.content, UP).shift(
            RIGHT * 0.25 + DOWN * 0.25)
        ucc = grey_chip("cli.sh's region · line 14").next_to(reg, DOWN, buff=0.25).align_to(reg, LEFT)
        steps = ["EDIT QUOTAS", "new limit", "NEXT", "name", "SUBMIT REQUEST"]
        fchips = VGroup(*[button(s, CLOUD) if s.isupper() else grey_chip(s) for s in steps])
        fchips.arrange(DOWN, buff=0.24).move_to([4.6, 1.0, 0])
        flow = VGroup()
        for i, c in enumerate(fchips):
            flow.add(c)
            if i < len(fchips) - 1:
                flow.add(Arrow(c.get_bottom(), fchips[i + 1].get_top(), buff=0.02, color=S.GREY, stroke_width=2,
                               tip_length=0.1, max_tip_length_to_length_ratio=0.6))
        assert flow.get_top()[1] < 2.8 and flow.get_bottom()[1] > -1.15, flow.get_top()
        assert quota.get_right()[0] < flow.get_left()[0] - 0.2
        assert qcol.get_right()[0] < quota.frame.get_right()[0] - 0.2
        rc43 = readme_card((43, 44), size=20)
        top_left(rc43, -6.3, -1.45)
        cpu = card(["cli.sh runs on CPU today ·", "the request is for later"], size=20)
        cpu.next_to(rc43, RIGHT, buff=0.3).align_to(rc43, UP)
        yt1b = your_turn().next_to(cpu, DOWN, buff=0.25).align_to(cpu, LEFT)
        assert cpu.get_right()[0] < 6.5 and yt1b.get_bottom()[1] > -3.5, (cpu.get_right(), yt1b.get_bottom())

        with self.voiceover(SAY[1]) as vo:
            self.keep_only(tr, ref)
            self.play(track(tr, 2), FadeIn(api, shift=UP * 0.15), FadeIn(api_ill), run_time=0.6)
            vo.wait_until("enable the Vertex AI API")
            self.play(FadeIn(box_), run_time=0.2)
            self.play(AddTextLetterByLetter(q), run_time=0.6)
            self.play(FadeIn(en, scale=0.9), run_time=0.3)
            self.play(Indicate(en.text, color=CLOUD, scale_factor=1.15), run_time=0.5)
            self.play(FadeIn(done, shift=RIGHT * 0.15), run_time=0.4)
            self.play(FadeIn(yt1, shift=LEFT * 0.15), run_time=0.3)
            vo.wait_until("Then request GPU quota")
            old = VGroup(api, api_ill, box_, q, en, done, yt1)
            self.play(FadeOut(old, shift=UP * 0.2), track(tr, 3), run_time=0.5)
            self.remove(old, *old)
            self.play(FadeIn(quota, shift=UP * 0.15), FadeIn(q_ill), run_time=0.5)
            vo.wait_until("an allowance per region")
            self.play(Indicate(quota.crumbs[-1], color=CLOUD), run_time=0.6)
            vo.wait_until("Filter for custom model training")
            self.play(FadeIn(flt, shift=RIGHT * 0.15), run_time=0.4)
            vo.wait_until("pick T4 GPUs")
            self.play(FadeIn(t4row, shift=UP * 0.1), run_time=0.4)
            self.play(t4_box.animate.set_stroke(TURN, 3), run_time=0.3)
            vo.wait_until("include us-central1")
            self.play(FadeIn(reg, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("where cli.sh runs")
            self.play(FadeIn(ucc, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("set a new limit and submit")
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.1) for m in flow], lag_ratio=0.25), run_time=1.4)
            vo.wait_until("Pause and do both")
            self.play(FadeIn(rc43, shift=UP * 0.15), run_time=0.4)
            self.play(FadeIn(yt1b, shift=UP * 0.1), run_time=0.3)
            flash_tag(self, yt1b, TURN, run_time=0.6)
            vo.wait_until("Approval may take hours")
            self.play(Indicate(rc43.body, color=INK, scale_factor=1.03), run_time=0.7)
            vo.wait_until("cli.sh runs on CPU without it")
            self.play(FadeIn(cpu, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 2. the secrets folder (C4)
        t = laptop_term(7, P_REPO)
        rc55 = readme_card((55, 58), body=VGroup(mono("|-model-training", 22, INK), mono("|-secrets", 22, INK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12))
        rc55.next_to(t.box, UP, buff=0.3).align_to(t.box, LEFT).shift(RIGHT * 0.1)
        c04, c05 = capture("04"), capture("05")
        mp = TrainingMap.at("S07")

        with self.voiceover(SAY[2]) as vo:
            self.keep_only(tr, ref)
            self.play(track(tr, 4), FadeIn(t), run_time=0.5)
            type_cmd(self, t, "cd ..", type_time=0.3)
            cd_prompt(self, t, P_LAPTOP, run_time=0.4)
            vo.wait_until("beside the repo")
            mk = type_cmd(self, t, c04.cmd, type_time=0.4)
            ch4 = beside(row_tag("the README shows a tree, not a command"), mk)
            pin(self, mk, ch4, run_time=0.3)
            bare_prompt(self, t)
            vo.wait_until("never inside it")
            self.play(track(tr, 4, extra=True), FadeIn(rc55, shift=UP * 0.15), run_time=0.4)
            tl = type_cmd(self, t, c05.cmd, type_time=0.3)
            pin(self, tl, beside(extra_row(), tl), run_time=0.2)
            o5 = out(self, t, c05.at((2, 6)), run_time=0.4)
            self.play(each([o5[1], o5[2]], TURN, scale=1.05), each(list(rc55.body), TURN, scale=1.05), run_time=0.7)
            vo.wait_until("pause and make it")
            yt2 = beside(turn_row(), o5[2])
            pin(self, o5[2], yt2, run_time=0.3)
            flash_tag(self, yt2, TURN, run_time=0.5)
            self.play(FadeOut(rc55), run_time=0.3)
            self.remove(rc55)
            resize(self, t, 3, run_time=0.5)
            self.play(FadeIn(mp), run_time=0.5)
            self.play(mp.light("secrets"), run_time=0.5)
            self.play(Indicate(mp.parts["secrets"].text, color=KEY, scale_factor=1.1), run_time=0.5)

        # ========================================================== 3. the service account and its key (C5)
        sa = console(("IAM & Admin", "Service accounts"), 8.4, 3.95).move_to([-2.1, 0.75, 0])
        sa_ill = ill_in(sa)
        create = VGroup(label("Create service account", 22, INK), chip(SA_NAME, KEY, size=22, font=MONO))
        create.arrange(RIGHT, buff=0.25)
        roles = VGroup(*[chip(r, S.GREY, size=20) for r in SA_ROLES])
        VGroup(roles[0], roles[1]).arrange(RIGHT, buff=0.15)
        roles[2].next_to(roles[0], DOWN, buff=0.12, aligned_edge=LEFT)
        menu = notebook_menu(("Actions ⋮", "Manage keys", "JSON", "Create"), size=20)
        sacol = VGroup(create, roles, menu).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        sacol.move_to(sa.content).align_to(sa.content, LEFT).align_to(sa.content, UP).shift(RIGHT * 0.25 + DOWN * 0.25)
        assert sacol.get_right()[0] < sa.frame.get_right()[0] - 0.15, sacol.get_right()
        sdr = drawer("secrets/", KEY, 22, glyph=True, mono_font=True, drawer_w=3.0).move_to([4.6, -0.2, 0])
        fdl = file_card("private key · JSON", KEY).move_to([4.6, 1.6, 0])
        fkey = file_card(KEY_FILE, KEY).move_to(sdr.get_center() + DOWN * 0.75)
        yt3 = your_turn().next_to(fkey, DOWN, buff=0.25)
        assert fdl.get_right()[0] < 6.6 and fkey.get_right()[0] < 6.6 and fkey.get_left()[0] > sa.get_right()[0]
        assert sacol.get_bottom()[1] > sa.frame.get_bottom()[1] + 0.1, sacol.get_bottom()
        c06 = capture("06")

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(mp), track(tr, 5), run_time=0.5)
            self.remove(mp)
            self.play(FadeIn(sa, shift=UP * 0.15), FadeIn(sa_ill), run_time=0.5)
            vo.wait_until("a service account called model trainer")
            self.play(FadeIn(create, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("with Storage Admin")
            for r, anchor in zip(roles, ("with Storage Admin", "AI Platform Admin", "Vertex AI Administrator")):
                vo.wait_until(anchor)
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
            vo.wait_until("and one JSON key")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in menu], lag_ratio=0.2), run_time=0.9)
            self.play(FadeIn(sdr), FadeIn(fdl, shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("saved in secrets")
            self.play(fdl.animate.move_to(fkey), run_time=0.7)
            self.play(FadeOut(fdl), FadeIn(fkey), run_time=0.4)
            self.remove(fdl)
            vo.wait_until("Pause and create yours")
            self.play(FadeIn(yt3, shift=UP * 0.1), run_time=0.3)
            flash_tag(self, yt3, TURN, run_time=0.6)
            old = VGroup(sa, sa_ill, create, roles, menu, sdr, fkey, yt3)
            self.play(FadeOut(old, shift=UP * 0.2), track(tr, 5, extra=True), run_time=0.5)
            self.remove(old, *old)
            resize(self, t, 6, run_time=0.5)
            lsd = type_cmd(self, t, c06.cmd, type_time=0.4)
            pin(self, lsd, beside(extra_row(), lsd), run_time=0.2)
            o6 = out(self, t, [c06.line(2)] + ls_cols(c06.at((3, 5))), run_time=0.5)
            kr = ring(substring(o6[-1], KEY_FILE), TURN, buff=0.05)
            self.play(Create(kr), run_time=0.4)
            si = beside(row_tag("stand-in"), o6[-1])
            pin(self, o6[-1], si, run_time=0.3)

        # ========================================================== 4. one honest note
        lines = ["This recording machine has no Google credentials,", "no W&B account, no GPU and no browser.",
                 "The key in that listing is an obviously invalid stand-in,",
                 "moved out before the first container start.",
                 "Every cloud step shows the failure a misplaced key gives."]
        hc = card(lines, head="one honest note", size=24).move_to([0, 0.75, 0])
        chips4 = VGroup(recorded_tag("recorded · source named"), standin_tag()).arrange(RIGHT, buff=0.35)
        chips4.next_to(hc, DOWN, buff=0.35)
        assert hc.get_top()[1] < 2.8 and chips4.get_bottom()[1] > -3.5

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(t, *t.lines, kr), shift=DOWN * 0.2), track(tr, 5), run_time=0.6)
            self.remove(t, *t.lines, kr)
            self.play(FadeIn(hc.frame), FadeIn(hc.head), run_time=0.5)
            vo.wait_until("This recording machine")
            self.play(FadeIn(hc.body[0], shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(hc.body[1], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("The key in that listing")
            self.play(FadeIn(hc.body[2], shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(hc.body[3], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("So each cloud step")
            self.play(FadeIn(hc.body[4], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("successes come from named sources")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips4], lag_ratio=0.3), run_time=0.7)

        # ========================================================== 5. a bucket with your own name (C6)
        bk = console(("Cloud Storage", "Create bucket"), 7.6, 2.4).move_to([-2.6, 1.45, 0])
        bk_ill = ill_in(bk)
        nm_box = RoundedRectangle(width=4.4, height=0.5, corner_radius=0.1, stroke_color=CLOUD, stroke_width=2)
        nm = mono(BUCKET, 22, INK).move_to(nm_box).align_to(nm_box, LEFT).shift(RIGHT * 0.2)
        brow = VGroup(label("Name", 22, S.GREY), VGroup(nm_box, nm), button("CREATE")).arrange(RIGHT, buff=0.3)
        brow.move_to(bk.content).shift(UP * 0.05)
        assert brow.get_right()[0] < bk.frame.get_right()[0] - 0.15
        rc71 = readme_card(71, size=20)
        rc71.next_to(bk, DOWN, buff=0.3).align_to(bk, LEFT)
        rp = replace_chip().next_to(rc71, DOWN, buff=0.15).align_to(rc71, RIGHT)
        assert rc71.get_right()[0] < 6.5, rc71.get_right()
        yt5 = your_turn().next_to(bk.frame, RIGHT, buff=0.3).align_to(bk.frame, DOWN)
        c07, c08 = capture("07"), capture("08")
        tb = term(P_LAPTOP, rows=9, size=20)
        cost = cost_tag("the bucket stores your tarball (tiny) and any experiment folders\n"
                        "see the Cloud Storage pricing page")
        cost.move_to([0, -2.45, 0])

        with self.voiceover(SAY[5]) as vo:
            self.keep_only(tr, ref)
            self.play(track(tr, 6), FadeIn(bk, shift=UP * 0.15), FadeIn(bk_ill), run_time=0.6)
            self.play(FadeIn(brow[0]), FadeIn(nm_box), FadeIn(brow[2]), run_time=0.4)
            vo.wait_until("with your own name")
            self.play(AddTextLetterByLetter(nm), run_time=0.8)
            self.play(FadeIn(rc71, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(rp, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("pause and create it")
            self.play(Indicate(brow[2].text, color=CLOUD), FadeIn(yt5, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("Two extras show why")
            old = VGroup(bk, bk_ill, brow, nm, yt5)
            rc_top = VGroup(rc71, rp)
            self.play(FadeOut(old, shift=UP * 0.2), track(tr, 6, extra=True),
                      rc_top.animate.shift(np.array([0, 2.75 - rc71.get_top()[1], 0])), run_time=0.6)
            self.remove(old, *old)
            self.play(FadeIn(tb), run_time=0.4)
            exb = on_bar(tb, extra_row())
            type_cmd(self, tb, c07.cmd, type_time=1.0)
            self.play(FadeIn(exb), run_time=0.2)
            vo.wait_until("our placeholder returns 404")
            o7 = out(self, tb, c07.at(5, "…") + [(c07.line(15), ERR)], run_time=0.5)
            vo.wait_until("it exists nowhere")
            self.play(Indicate(o7[-1], color=ERR, scale_factor=1.08), run_time=0.5)
            vo.wait_until("while the README's name")
            type_cmd(self, tb, c08.cmd, type_time=0.9)
            vo.wait_until("returns 401")
            out(self, tb, c08.at(5), wrap=True, run_time=0.5)
            o8b = out(self, tb, ["…", (c08.line(17), ERR)], run_time=0.3)
            vo.wait_until("it belongs to someone else")
            tk = beside(row_tag("the README's name · taken · replace this with yours"), o8b[-1])
            pin(self, o8b[-1], tk, run_time=0.4)
            vo.wait_until("A gold tag")
            self.keep_only(tr, ref, run_time=0.5)
            self.play(FadeIn(mp), run_time=0.5)
            self.play(mp.name_bucket(), run_time=0.7)
            self.play(FadeIn(cost, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("the bucket stores your code")
            flash_tag(self, cost, COST)

        # ========================================================== 6. the W&B key, exported in the host shell (C7)
        wb = console(("User settings", "API keys"), 7.0, 2.3).move_to([-2.8, 1.55, 0])
        wb_ill = ill_in(wb)
        dots = mono("·" * 24, 22, S.GREY)
        kbox = RoundedRectangle(width=dots.width + 0.4, height=0.5, corner_radius=0.1, stroke_color=S.GREY,
                                stroke_width=2)
        keyrow = VGroup(VGroup(kbox, dots.move_to(kbox)), button("Copy", S.GREY)).arrange(RIGHT, buff=0.3)
        keyrow.move_to(wb.content).shift(UP * 0.05)
        rc80 = readme_card(80)
        rc80.next_to(wb, DOWN, buff=0.3).align_to(wb, LEFT)
        c10, c11 = capture("10"), capture("11")
        assert WANDB_KEY_PH in c10.cmd
        t6 = laptop_term(5)
        ph = grey_chip("README: ... = your key · ours: an obvious placeholder")
        why = card(["40: the placeholder's length · the check: not 0",
                    "and the trainer's pinned wandb 0.15.11 accepts only 40",
                    "(scene 11: 84:14, 87:14)"], size=20)
        rs = VGroup(card(["keep it out of your shell history:",
                          mono("read -rs WANDB_KEY && export WANDB_KEY", 20, INK), "(bash, zsh)"], size=20),
                    extra_tag("not captured")).arrange(RIGHT, buff=0.25, aligned_edge=UP)

        with self.voiceover(SAY[6]) as vo:
            self.keep_only(tr, ref)
            self.play(track(tr, 7), FadeIn(wb, shift=UP * 0.15), FadeIn(wb_ill), run_time=0.6)
            vo.wait_until("copy your W and B key")
            self.play(FadeIn(keyrow), run_time=0.4)
            self.play(Indicate(keyrow[1].text, color=INK), run_time=0.5)
            self.play(FadeIn(rc80, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("and export it in the terminal")
            old = VGroup(wb, wb_ill, keyrow)
            self.play(FadeOut(old, shift=UP * 0.2), rc80.animate.shift(np.array([0, 2.75 - rc80.get_top()[1], 0])),
                      run_time=0.5)
            self.remove(old, *old)
            ph.next_to(rc80, DOWN, buff=0.25).align_to(rc80, LEFT)
            self.play(FadeIn(t6), FadeIn(ph, shift=UP * 0.1), run_time=0.4)
            exl = type_cmd(self, t6, c10.cmd, type_time=1.2)
            vo.wait_until("Pause and do it")
            yt6 = beside(turn_row(), exl)
            pin(self, exl, yt6, run_time=0.3)
            flash_tag(self, yt6, TURN, run_time=0.5)
            vo.wait_until("An extra echo")
            ech = substring(exl.rows[-2], "echo") if hasattr(exl, "rows") else substring(exl, "echo")
            ex6 = on_bar(t6, extra_row())
            self.play(FadeIn(ex6), track(tr, 7, extra=True), Indicate(ech, color=INK), run_time=0.6)
            o10 = out(self, t6, c10.at(2), run_time=0.3)
            vo.wait_until("40 for our placeholder")
            r40 = ring(substring(o10[0], c10.line(2)), TURN, buff=0.06)
            self.play(Create(r40), run_time=0.4)
            vo.wait_until("It must not be zero")
            top_left(why, rc80.get_left()[0], 2.75)
            rs.next_to(why, DOWN, buff=0.2).align_to(why, LEFT)
            self.play(FadeOut(VGroup(rc80, ph), shift=UP * 0.2), FadeIn(why, shift=UP * 0.15), run_time=0.6)
            self.remove(rc80, ph)
            vo.wait_until("accepts exactly 40")
            self.play(Indicate(why.body[1], color=KEY, scale_factor=1.03), FadeIn(rs, shift=UP * 0.1), run_time=0.7)
            self.play(FadeOut(VGroup(why, rs)), FadeOut(r40), run_time=0.4)
            self.remove(why, rs, r40)
            resize(self, t6, 3, run_time=0.5)
            self.play(FadeIn(mp), run_time=0.4)
            self.play(mp.light("laptop"), mp.reveal("key"), run_time=0.6)
            self.play(mp.unlight("laptop"), run_time=0.4)

        # ========================================================== 7. a new terminal (ponder)
        nt = new_term(3)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(mp), run_time=0.4)
            self.remove(mp)
            vo.wait_until("closed that terminal")
            self.play(FadeOut(VGroup(t6, *t6.lines, ex6), shift=DOWN * 0.3), run_time=0.5)
            self.remove(t6, *t6.lines, ex6)
            vo.wait_until("and opened a new one")
            nt.shift(RIGHT * 14)
            self.play(nt.animate.shift(LEFT * 14), run_time=0.7)
            vo.wait_until("What does the same echo")
            bare_prompt(self, nt)
        pc = ponder(self, PONDER_ENV, seconds=6, center=(0, 0.8))

        # ========================================================== 8. zero; part 1 is done
        dash = VGroup()
        hr = mp.parts["cockpit"].body.get_right()[0]
        bl = mp.parts["bucket"][0].get_left()[0]
        vl = mp.parts["vertex"][0].get_left()[0]
        dash.add(_poly([[hr + 0.12, 0.6, 0], [bl - 0.05, 0.6, 0]], S.GREY, 3, dashed=True))
        dash.add(_poly([[hr + 0.12, 0.3, 0], [-3.1, 0.3, 0], [-3.1, -1.0, 0], [vl - 0.05, -1.0, 0]], S.GREY, 3,
                       dashed=True))
        nxt = label("next: the cockpit — and today it won't build", 26, INK).move_to([0, -2.3, 0])
        ckp = mp.parts["cockpit"]

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            ex8 = on_bar(nt, extra_row())
            type_cmd(self, nt, c11.cmd, type_time=0.6)
            self.play(FadeIn(ex8), run_time=0.2)
            o11 = out(self, nt, [(c11.line(2), ERR)], run_time=0.3)
            zero = substring(o11[0], c11.line(2))
            self.play(Indicate(zero, color=ERR, scale_factor=1.3), run_time=0.6)
            vo.wait_until("exists only in that shell")
            self.play(Create(ring(zero, ERR, buff=0.08)), run_time=0.4)
            vo.wait_until("Part 1 is done")
            self.keep_only(tr, ref, run_time=0.5, shift=DOWN * 0.2)
            self.play(FadeIn(mp), run_time=0.6)
            self.play(Create(dash[0]), Create(dash[1]), run_time=0.8)
            vo.wait_until("the key is set")
            self.play(Indicate(mp.parts["key"], color=KEY, scale_factor=1.15), run_time=0.6)
            vo.wait_until("the bucket has a name")
            self.play(Indicate(mp.parts["bucket"][1], color=CLOUD, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Next, we build the cockpit")
            for _ in range(2):
                self.play(mp.light("cockpit", run_time=0.25))
                self.play(mp.unlight("cockpit", run_time=0.25))
            vo.wait_until("today it won't build")
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
