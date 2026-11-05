"""S03 · A user, a role and a bucket — tracker A1 1 → 5, then A2 1 → 2; no lecture tag (script.md
v2 has no LECTURE mark in this scene). V1 IdentityBadges is built here.

Beats (script.md "## S03"; one voiceover block each):
0. TRACKER A1 1. Full-width 20 pt terminal `laptop`, prompt student@laptop:~$. README card (A:9–10)
   + GREY chip "the README spells no command". `git clone …` → laptop/10: 2 (typed on the first
   sentence; its row tag extra lands on "so our git clone is extra"); ▶ your turn on the output row
   on "Pause and clone it". `cd model-deployment-aws` → the prompt changes. TRACKER A1 1 ·
   extra: `git log -1 --format='%H %ci %s'` (extra, on the title bar) → laptop/11: 2 to "#1 from"
   (wrapped), then `…`; `077f4dbc7b13` YELLOW; chip "main · the commit we follow".
1. TRACKER A1 1 · extra. The card goes, the terminal clears and grows to 12 rows. `ls -la; ls data`
   (extra) → laptop/12: 7–10, 12–13, …, then 15–22 as two columns (names only). The CLI, Dockerfile,
   Pipfile and photo names flash on their words; line 13 YELLOW + row tag "already executable".
2. The terminal fades. TRACKER A1 2. CONSOLE "Services" (A:12–16, illustration): three GREY checks
   tick in; GREY chip "labels from the README · if yours differ, look for the same field". TRACKER
   A1 3; on "Then" the form transforms into CONSOLE "IAM › Users · Create user" (A:21–30): user name
   types in; three ORANGE policy chips; on "broader" an ORANGE flag beside IAMFullAccess; the button
   row "Create access keys · save both" pulses; on "save both" the GREY laptop + ~/.aws drawer
   (V1's laptop) appears at the left and the GREY key card drops in.
3. TRACKER A1 4. The laptop side steps aside. CONSOLE "IAM › Roles · Create role" (A:36–42) at the
   left: trusted entity SageMaker, two ORANGE policy chips, role name. The BLUE cloud draws at the
   right and the BLUE SageMakerExecutionRole badge forms in it. On "Copy its A R N": README card
   (A:43, the ARN folded on two rows, digits GREY) + chip "AWS documentation placeholder" right of
   it, under the cloud.
4. V1 IdentityBadges built: the form goes, the laptop (key in the drawer) and the border return;
   PINK request arrow "signed by the user" carries the key card; the dashed "endpoint · later" box
   appears in the cloud and puts the badge on; on "stays" the key bounces off the border.
5. TRACKER A1 5. The laptop side leaves (V1 keeps its cloud at the right: shifted, never scaled).
   CONSOLE "S3 · Create bucket" (A:50–52) at the left with the README's ORANGE "[REPLACE …]" note;
   ▶ your turn; GREY chip "unique across all AWS accounts"; a BLUE bucket joins the cloud; GOLD
   cost tag under the cloud. On "as the README warns" the form column becomes a RED README card
   (A:56–58).
6. Everything goes. TRACKER A2 1 (section swap). Full-width terminal (prompt …/model-deployment-aws).
   `aws configure` → laptop/13: 3 (wrapped), 5–8; chip "newer than the README · at the time of
   recording" over the tip; lines 5–6 GREY + row tag "paste your two keys here · we have none";
   `us-east-1` and `json` YELLOW. ▶ your turn.
7. TRACKER A2 1 · extra. `ls -la ~/.aws; cat ~/.aws/config` (extra) → laptop/14: 5–8; a GREY ~/.aws
   drawer above the terminal holds one `config` card + chip "no credentials file: no keys typed".
   The terminal clears: `aws sts get-caller-identity` (extra · the who-am-I call) → laptop/15: 3
   wrapped, RED; GREEN chip "with your keys: your account id"; ▶ your turn.
8. TRACKER A2 2. The drawer goes, the terminal clears and grows. The three README exports and the
   who-am-I check (extra, laptop/16 line 4) → laptop/16: 6 wrapped, RED.
9. The terminal goes. V1 returns: laptop + drawer (config + key), TEAL container; CODE
   docker-shell.sh 22–28 (20 pt, three lines cut) at the right, lines lighting with the arrows:
   line 24's PINK -v arrow (plus a visible PINK arc drawer → /home/app/.aws) copies the drawer in; three GREY export cards; lines 25–27 YELLOW as the
   three PINK -e arrows pass; on "So exported keys" the two key cards hit the wall and drop.
   `erratum` tag + card "use option 1 · or add -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY · in
   docker-shell.sh, before $IMAGE_NAME" right after the fall (line 28 lights); a 2 s hold; fade to empty.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _small_file
from explainer import style as S

SAY = NARRATION["S03"]

TS = 20                                          # this scene's terminals: 72 characters a row (ls -la)
CLONE_URL_ROW = "https://github.com/dlops-io/model-deployment-aws.git"
PHOTOS_SPLIT = 4                                 # ls data as two columns of four names


# ------------------------------------------------------------------ helpers of this scene
def tterm(prompt: str, rows: int) -> Terminal:
    return term(prompt, rows, size=TS)


def ls_align(lines) -> list[str]:
    """Re-align `ls -la` rows with one-space gutters (the size column right-aligned), as GNU ls
    prints them: busybox pads each column wide and the rows would not fit. Words unchanged."""
    out_ = []
    parts = [ln.split() for ln in lines]
    w = max(len(p[4]) for p in parts)
    for p in parts:
        perm, links, owner, group, size, mon, day, hm = p[:8]
        name = " ".join(p[8:])
        out_.append(f"{perm} {links} {owner} {group} {size:>{w}} {mon} {day:>2} {hm} {name}")
    return out_


def recolor(glyphs, color):
    """ANIMs, glyph by glyph (never animate a substring group itself: split trap)."""
    return [g.animate.set_color(color) for g in glyphs]


def trk(key: str, step=None, extra=False) -> ReadmeTracker:
    """common.tracker() with its head put back above the dots: tracker() re-arranges the head
    with VGroup.arrange (which centres it), so the 'README A › …' line lands near y 0 (reported to
    the coordinator; common.py is shared and not edited here)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    return place_tracker(tr)


def place_chips(f, chips):
    """Put each policy chip over its hidden check-row text (call after the form is placed)."""
    rows = [r for r in f.rows if getattr(r, "kind", "") == "check"]
    for r, c in zip(rows, chips):
        c.move_to(r.text, aligned_edge=LEFT).shift(LEFT * 0.05)
    return chips


def checks_form(title, rows_spec, path=None, form_w=8.6, chip_color=SHARED):
    """console_form whose ('check', name) rows show their name as a policy chip (ORANGE, AWS-managed)
    instead of plain text; ticks GREY. Returns (form, chips) — the chips are separate mobjects placed
    over the hidden texts (FadeIn them on their phrase)."""
    f = console_form(title, rows_spec, form_w=form_w, path=path)
    chips = VGroup()
    for r in f.rows:
        if getattr(r, "kind", "") == "check":
            r.tick.set_color(S.GREY).set_opacity(0)    # ticked together with its chip (no bare ticks)
            c = chip(r.text.text, chip_color, size=20, font=MONO)
            c.move_to(r.text, aligned_edge=LEFT).shift(LEFT * 0.05)
            r.text.set_opacity(0)
            chips.add(c)
    return f, chips


def tick_in(f):
    """ANIMs: the ticks of the form's policy rows appear (with their chips)."""
    return [r.tick.animate.set_opacity(1) for r in f.rows if getattr(r, "kind", "") == "check"]


def seat(scene, t, *over):
    """Re-seat terminal t as one mobject after animating loose glyphs (split trap), then put the
    tags that sit on it (title-bar tags, chips over its box) back in front of its opaque box."""
    scene.add(t)
    for m in over:
        if m in scene.mobjects:
            scene.bring_to_front(m)


def top_right_tag(f, tg, dx: float = 0.25):
    """A tag sitting on the form's top edge, right end."""
    return tg.move_to([f.frame.get_right()[0] - dx - tg.width / 2, f.frame.get_top()[1], 0])


class UserRoleBucket(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S03"] == 10, len(SAY)

        # ========================================================== 0. clone + the commit we follow
        tr = trk("A1", 1)
        t = tterm(P_HOME, 9)
        rd = readme_card((9, 10), "Clone the github repository\nClone or download from here", repo="A")
        rd.move_to([-6.5 + rd.width / 2, 1.75, 0])
        no_cmd = grey_chip("the README spells no command").next_to(rd, RIGHT, buff=0.4)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), run_time=0.7)
            self.play(FadeIn(rd, shift=DOWN * 0.1), run_time=0.6)
            c10 = capture("10")
            ln = type_cmd(self, t, c10.cmd, type_time=1.0)
            o10 = out(self, t, c10.at(2), run_time=0.4)
            vo.wait_until("The README says clone or download")
            self.play(Indicate(rd.body[1], color=TURN, scale_factor=1.05), run_time=0.8)
            self.play(FadeIn(no_cmd, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("so our git clone is extra")
            pin(self, ln, beside(extra_row(), ln))
            vo.wait_until("and so is the git log")
            type_cmd(self, t, "cd model-deployment-aws", type_time=0.4)
            cd_prompt(self, t, P_MD)
            self.play(track(tr, 1, True), run_time=0.4)
            c11 = capture("11")
            ln11 = type_cmd(self, t, c11.cmd, type_time=0.7)
            ex11 = on_bar(t, extra_row())
            o11 = out(self, t, [cut(c11.line(2), "#1 from", ellipsis=""), "…"], wrap=True, run_time=0.5)
            assert o11[0].text.startswith("077f4dbc7b13") and o11[1].text.endswith("#1 from")
            main = row_tag("main · the commit we follow")
            beside(main, o11[-1], buff=0.3)
            self.play(*recolor(glyph_range(o11[0], 0, 12), TURN), FadeIn(ex11), FadeIn(main, shift=LEFT * 0.1),
                      run_time=0.5)
            seat(self, t, ex11, main)
            vo.wait_until("Pause and clone it")
            turn = beside(turn_row(), o10[0], buff=0.4)
            pin(self, o10[0], turn)

        # ========================================================== 1. the extra listing
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(rd), FadeOut(no_cmd), FadeOut(main), FadeOut(ex11), run_time=0.4)
            t.clear(self)
            resize(self, t, 12)
            c12 = capture("12")
            ln12 = type_cmd(self, t, c12.cmd, type_time=0.6)
            pin(self, ln12, beside(extra_row(), ln12))
            top = ls_align(c12.at((7, 10), (12, 13)))
            photos = c12.at((15, 22))
            cols = [f"{a:<17}{b}" for a, b in zip(photos[:PHOTOS_SPLIT], photos[PHOTOS_SPLIT:])]
            rows = out(self, t, top + ["…"] + cols, run_time=1.0)
            vo.wait_until("the CLI, a Dockerfile")
            names = [substring(rows[3], "cli.py"), substring(rows[0], "Dockerfile"),
                     substring(rows[1], "Pipfile")]
            self.play(LaggedStart(*[Indicate(g, color=TURN, scale_factor=1.1) for g in names], lag_ratio=0.5),
                      run_time=1.6)
            self.add(t)
            vo.wait_until("eight sample photos")
            self.play(LaggedStart(*[Indicate(r, color=TURN, scale_factor=1.04) for r in rows[7:]], lag_ratio=0.25),
                      run_time=1.2)
            self.add(t)
            vo.wait_until("and docker-shell.sh")
            ds = rows[5]
            assert ds.text.endswith("docker-shell.sh")
            self.play(*recolor(ds, TURN), run_time=0.5)
            perm = ring(glyph_range(ds, 0, 10), TURN, buff=0.05, stroke=2.5)
            self.play(Create(perm), run_time=0.4)
            attach(self, ds, perm)
            ae = beside(row_tag("already executable", TURN), rows[6], buff=0.4)
            pin(self, rows[6], ae, run_time=0.5)

        # ========================================================== 2. services, the IAM user, the keys
        sf = console_form("Services", [("check", "Amazon S3", False), ("check", "Amazon SageMaker", False),
                                       ("check", "AWS IAM", False)], form_w=8.6, path="AWS Console")
        for r in sf.rows:
            r.tick.set_color(S.GREY)
        sf.move_to([2.2, 0.75, 0])
        ill = illustration_tag()
        top_right_tag(sf, ill)
        lbl = grey_chip("labels from the README · if yours differ, look for the same field")
        lbl.next_to(sf, DOWN, buff=0.35).align_to(sf, RIGHT)

        uf, pols = checks_form("Create user", [("User name", ""), ("note", "Attach the following policies:"),
                                               ("check", "AmazonS3FullAccess"),
                                               ("check", "AmazonSageMakerFullAccess"),
                                               ("check", "IAMFullAccess"),
                                               ("button", "Create access keys · save both")],
                               path="IAM › Users")
        uf.move_to([2.2, -0.45, 0])
        place_chips(uf, pols)
        broad = chip("broader than this code needs", SHARED, size=20)
        broad.next_to(pols[2], RIGHT, buff=0.3)
        flag_ln = Line(pols[2].get_right(), broad.get_left(), color=SHARED, stroke_width=3)

        v = IdentityBadges(parts=())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(t), track(tr, 2, False), run_time=0.6)
            self.remove(t)
            self.play(FadeIn(sf, shift=UP * 0.1), FadeIn(ill), run_time=0.6)
            self.play(FadeIn(lbl, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Check that you can use")
            self.play(LaggedStart(*[r.tick.animate.set_opacity(1) for r in sf.rows], lag_ratio=0.6), run_time=1.8)
            vo.wait_until("Then create an IAM user")
            self.play(track(tr, 3), FadeOut(lbl), ReplacementTransform(sf, uf),
                      ill.animate.move_to(top_right_tag(uf, ill.copy()).get_center()), run_time=0.9)
            self.bring_to_front(ill)
            self.play(uf.fill(0, USER_A), run_time=0.8)
            vo.wait_until("with three policies")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in pols], lag_ratio=0.4), *tick_in(uf),
                      run_time=1.2)
            vo.wait_until("The third is broader")
            self.play(Create(flag_ln), FadeIn(broad, shift=LEFT * 0.1), Indicate(pols[2], color=SHARED),
                      run_time=0.8)
            vo.wait_until("Create access keys")
            self.play(uf.press(5), run_time=0.8)
            vo.wait_until("save both")
            v.show(self, v.laptop, anims=[FadeIn(v.laptop, shift=RIGHT * 0.2)], run_time=0.5)
            v.add_key(self)

        # ========================================================== 3. the execution role
        rf, rpols = checks_form("Create role", [("Trusted entity", "SageMaker"),
                                                ("check", "AmazonSageMakerFullAccess"),
                                                ("check", "AmazonS3FullAccess"),
                                                ("Role name", "")],
                                path="IAM › Roles", form_w=6.6)
        rf.move_to([-6.55 + rf.width / 2, 2.5 - rf.height / 2, 0])
        rf.rows[0].value.set_opacity(0)
        place_chips(rf, rpols)
        rill = top_right_tag(rf, illustration_tag())
        acct = mono_line(f"arn:aws:iam::{README_ACCOUNT}:", 20, INK, t2c={README_ACCOUNT: S.GREY})
        acct2 = mono_line(f"role/{ROLE_A}", 20, INK)
        arn_body = VGroup(acct, acct2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        arn = readme_card(43, arn_body, repo="A")
        arn.move_to([-6.55 + arn.width / 2, rf.get_bottom()[1] - 0.25 - arn.height / 2, 0])
        doc = grey_chip("AWS documentation placeholder").next_to(arn, RIGHT, buff=0.25).align_to(arn, DOWN)
        doc.set_y(-3.48 + doc.height / 2)            # under the cloud's bottom edge (y -2.7)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(uf), FadeOut(pols), FadeOut(broad), FadeOut(flag_ln), FadeOut(ill),
                      track(tr, 4), run_time=0.5)
            v.drop(self, v.laptop, v.key, run_time=0.4)
            self.play(FadeIn(rf, shift=UP * 0.1), FadeIn(rill), run_time=0.6)
            v.show(self, v.cloud, anims=[Create(v.cloud[0])], run_time=0.6)
            self.play(rf.fill(3, ROLE_A), run_time=0.9)
            v.role(self, ROLE_A, 0)
            vo.wait_until("trusted by SageMaker")
            self.play(rf.fill(0, "SageMaker"), run_time=0.5)
            self.play(Indicate(rf.rows[0].value, color=CLOUD), run_time=0.6)
            vo.wait_until("with the SageMaker and S3 policies")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in rpols], lag_ratio=0.4), *tick_in(rf),
                      run_time=1.0)
            vo.wait_until("Copy its A R N")
            self.play(FadeIn(arn, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(substring(acct, README_ACCOUNT), color=S.GREY, scale_factor=1.08),
                      FadeIn(doc, shift=UP * 0.1), run_time=0.7)
            self.add(arn)

        # ========================================================== 4. why two identities (V1)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(rf), FadeOut(rpols), FadeOut(rill), FadeOut(arn), FadeOut(doc), run_time=0.5)
            v.show(self, v.laptop, v.key, v.border, run_time=0.7)
            vo.wait_until("Your laptop signs each request")
            req = v.request(self, "signed by the user", run_time=1.6)
            vo.wait_until("and the endpoint you create later")
            v.endpoint(self, "endpoint · later", dashed=True)
            worn = v.wear(self, 0)
            vo.wait_until("The key stays on your laptop")
            v.key_stays(self, run_time=1.2)
            self.play(Indicate(v.key, color=S.GREY, scale_factor=1.08), run_time=0.6)

        # ========================================================== 5. the bucket + never commit keys
        bf = console_form("Create bucket", [("Bucket name", BUCKET_A), ("note", "[REPLACE WITH YOUR"),
                                            ("note", "UNIQUE BUCKET NAME]"), ("button", "Create bucket")],
                          path="S3", form_w=6.6)
        for r in (bf.rows[1], bf.rows[2]):
            r.text.set_color(SHARED)
        bf.move_to([-6.55 + bf.width / 2, 2.5 - bf.height / 2, 0])
        bill = top_right_tag(bf, illustration_tag())
        bturn = your_turn().next_to(bf.rows[3], RIGHT, buff=0.5)
        uniq = grey_chip("unique across all AWS accounts").next_to(bf, DOWN, buff=0.3).align_to(bf, LEFT)
        bk = bucket(BUCKET_A).move_to(v.p(3.5, -0.1))
        cost = cost_tag("S3 storage · while files exist · check the pricing page").move_to([0, -3.2, 0])
        warn_body = VGroup(label("SECURITY WARNING", 22, ERR),
                           label("NEVER hardcode AWS credentials directly", 22, INK),
                           label("in scripts or commit them to Git!", 22, INK),
                           label("If you see credentials in any script files,", 22, INK),
                           label("remove them immediately.", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        warn = readme_card((56, 58), warn_body, repo="A")
        warn.frame.set_stroke(ERR, width=3)
        warn.move_to([-6.55 + warn.width / 2, 0.3, 0])

        with self.voiceover(SAY[5]) as vo:
            v.drop(self, v.laptop, v.key, v.border, req, v.job, worn, extra=[track(tr, 5)], run_time=0.6)
            self.play(FadeIn(bf, shift=UP * 0.1), FadeIn(bill), run_time=0.6)
            self.play(FadeIn(bturn, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("create a bucket with a name of your own")
            self.play(Indicate(bf.rows[0].value, color=TURN), Indicate(bf.rows[1].text, color=SHARED),
                      Indicate(bf.rows[2].text, color=SHARED), run_time=0.9)
            v.show(self, bk, anims=[FadeIn(bk, shift=DOWN * 0.3)], run_time=0.6)
            vo.wait_until("because bucket names are unique")
            self.play(FadeIn(uniq, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Storage bills")
            self.play(FadeIn(cost, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("And as the README warns")
            self.play(FadeOut(bf), FadeOut(bill), FadeOut(bturn), FadeOut(uniq), run_time=0.4)
            self.play(FadeIn(warn, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("never put keys in a script")
            self.play(Indicate(warn_body[1], color=ERR, scale_factor=1.04), run_time=0.8)
            vo.wait_until("and never commit them to Git")
            self.play(Indicate(warn_body[2], color=ERR, scale_factor=1.04), run_time=0.8)

        # ========================================================== 6. aws configure
        t = tterm(P_MD, 8)
        with self.voiceover(SAY[6]) as vo:
            v.drop(self, v.cloud, *v.badges, bk, extra=[FadeOut(warn), FadeOut(cost)], run_time=0.5)
            v.badges.clear()
            tr = swap_tracker(self, tr, trk("A2", 1), FadeIn(t))
            c13 = capture("13")
            type_cmd(self, t, c13.cmd, type_time=0.6)
            vo.wait_until("Then come four prompts")
            tip = out(self, t, c13.at(3), wrap=True, color=S.GREY)
            newer = under_term(t, grey_chip("newer than the README · at the time of recording"))
            self.play(FadeIn(newer, shift=DOWN * 0.1), run_time=0.4)
            p = out(self, t, [(s, S.GREY) for s in c13.at(5, 6)] + c13.at(7, 8), run_time=0.8, lag=0.3)
            vo.wait_until("You paste your two keys")
            self.play(Indicate(p[0], color=TURN, scale_factor=1.04), Indicate(p[1], color=TURN, scale_factor=1.04),
                      run_time=0.8)
            seat(self, t, newer)
            vo.wait_until("We have none")
            keys = beside(row_tag("paste your two keys here · we have none"), p[0], buff=0.4)
            pin(self, p[0], keys)
            vo.wait_until("then type")
            self.play(*recolor(substring(p[2], "us-east-1"), TURN), run_time=0.4)
            self.play(*recolor(substring(p[3], "json"), TURN), run_time=0.4)
            seat(self, t, newer)
            tturn = on_bar(t, turn_row())
            self.play(FadeIn(tturn), run_time=0.4)

        # ========================================================== 7. two extras: ~/.aws + who am I
        dr = drawer(drawer_w=2.6).move_to([5.1, 1.55, 0])
        cfg = _small_file("config").move_to(dr.slot(0))
        nocred = grey_chip("no credentials file: no keys typed")
        nocred.next_to(dr, LEFT, buff=0.35).align_to(dr, DOWN)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(tturn), FadeOut(newer), track(tr, 1, True), run_time=0.4)
            t.clear(self)
            c14 = capture("14")
            ln14 = type_cmd(self, t, c14.cmd, type_time=0.8)
            ex14 = on_bar(t, extra_row())
            self.play(FadeIn(ex14), run_time=0.3)
            vo.wait_until("only the config file exists")
            o14 = out(self, t, c14.at((5, 8)), run_time=0.8)
            self.play(FadeIn(dr, shift=DOWN * 0.1), run_time=0.4)
            self.play(TransformFromCopy(substring(o14[0], "config"), cfg), run_time=0.7)
            seat(self, t, ex14, dr, cfg)
            vo.wait_until("since we typed no keys")
            self.play(FadeIn(nocred, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("and the who am I call")
            self.play(FadeOut(ex14), run_time=0.2)
            t.clear(self)
            c15 = capture("15")
            ln15 = type_cmd(self, t, c15.cmd, type_time=0.7)
            ex15 = on_bar(t, row_tag("extra · the who-am-I call"))
            self.play(FadeIn(ex15), run_time=0.3)
            e15 = out(self, t, c15.at(3), wrap=True, color=ERR)
            vo.wait_until("With your keys")
            yours = ok_chip("with your keys: your account id")
            yours.move_to([e15[-1].strut.get_left()[0] + yours.width / 2, e15[-1].strut.get_bottom()[1] - 0.45, 0])
            self.play(FadeIn(yours, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Pause and make yours print it")
            tturn = turn_row().next_to(yours, RIGHT, buff=0.4)
            self.play(FadeIn(tturn, shift=LEFT * 0.1), run_time=0.4)

        # ========================================================== 8. option 2: three exports
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(dr), FadeOut(cfg), FadeOut(nocred), FadeOut(yours), FadeOut(tturn), FadeOut(ex15),
                      track(tr, 2), run_time=0.5)
            t.clear(self)
            resize(self, t, 10)
            c16 = capture("16")
            vo.wait_until("three exports in your shell")
            rows16 = []
            for row in c16.cmd_lines[:3]:
                rows16.append(type_cmd(self, t, row, type_time=0.45))
            ln_sts = type_cmd(self, t, c16.cmd_lines[3], type_time=0.5)
            ex16 = on_bar(t, row_tag("extra · line 4"))
            self.play(FadeIn(ex16), track(tr, 2, True), run_time=0.3)
            vo.wait_until("AWS rejects our placeholder key")
            e16 = out(self, t, c16.at(6), wrap=True, color=ERR)
            inv = substring(e16[-1], "invalid") if "invalid" in e16[-1].text else substring(e16[-2], "invalid")
            inv_ul = under(inv, ERR)
            self.play(Create(inv_ul), run_time=0.4)
            seat(self, t, ex16, inv_ul)

        # ========================================================== 9. the -v drawer vs the -e wall
        cp = code("A/docker-shell.sh", 22, 28, font_size=20,
                  cuts={22: "docker run", 26: "-e S3_MODELS_BUCKET_NAME", 27: "-e SAGEMAKER_ROLE"})
        cp.move_to([6.5 - cp.width / 2, 0.9, 0])
        bars_ = {k: line_bar(cp.code, k - 22, TURN, 0.22) for k in (24, 25, 26, 27)}
        err_t = erratum_tag()
        r1 = VGroup(label("or add", 22, INK), mono("-e AWS_ACCESS_KEY_ID", 20, ROUTE)).arrange(RIGHT, buff=0.15)
        r2 = VGroup(label("or add", 22, INK).set_opacity(0), mono("-e AWS_SECRET_ACCESS_KEY", 20, ROUTE)) \
            .arrange(RIGHT, buff=0.15)
        r3 = VGroup(label("in docker-shell.sh, before", 22, INK), mono("$IMAGE_NAME", 20, INK)) \
            .arrange(RIGHT, buff=0.15)
        fix_rows = [label("use option 1", 22, INK), r1, r2, r3]
        bar28 = line_bar(cp.code, 6, TURN, 0.22)
        fix = card(fix_rows)
        fix.next_to(cp, DOWN, buff=0.45).align_to(cp, RIGHT)
        err_t.next_to(fix, UP, buff=0.08).align_to(fix, LEFT)

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(t), FadeOut(ex16), FadeOut(inv_ul), run_time=0.5)
            self.remove(t, ex16, inv_ul)
            v.show(self, v.laptop, v.key, run_time=0.5)
            v.add_config(self)
            self.play(FadeIn(cp, shift=LEFT * 0.1), run_time=0.5)
            v.container(self, IMAGE_A)
            self.play(FadeIn(bars_[24]), run_time=0.3)
            # the piece's own -v arrow is very short here (drawer and container nearly touch): a visible
            # PINK arc from the ~/.aws drawer up into the container's /home/app/.aws row goes with it
            vv = route(v.drawer.frame.get_corner(UR) + np.array([-0.35, 0.02, 0]),
                       v.box_c.frame.get_top() + np.array([-1.5, -0.78, 0]), arc=-0.6)
            v.show(self, vv, anims=[GrowArrow(vv)], run_time=0.5)
            v.mount(self)
            vo.wait_until("the script passes only the region")
            self.play(FadeOut(bars_[24]), run_time=0.2)
            cards = v.exports(self)
            self.play(*[FadeIn(bars_[k]) for k in (25, 26, 27)], run_time=0.4)
            env = v.env_pass(self, run_time=1.4)
            # the region export is the one that passes: its card moves up over the -e arrows (out of
            # the two key cards' fall path, right of the first card, left of the code panel); the '-e'
            # flag moves to the arrows' right so the falling secret-key card does not cross it
            arrs, tag_e = env[:3], env[-1]
            reg = cards[2].copy()
            reg.move_to([cp.get_left()[0] - 0.15 - reg.width / 2, cards[1].get_top()[1] + 0.08 + reg.height / 2, 0])
            self.play(cards[2].animate.move_to(reg), tag_e.animate.next_to(arrs[-1], RIGHT, buff=0.12),
                      run_time=0.5)
            vo.wait_until("So exported keys fall off at the wall")
            v.fall_off(self, cards[:2], run_time=1.4)
            # the fix card comes in as soon as the keys have fallen (not on the last words), so the
            # two flags and where they go stay readable; it then holds before the scene's fade
            self.play(FadeIn(err_t, shift=DOWN * 0.1), FadeIn(fix, shift=UP * 0.1),
                      *[FadeOut(bars_[k]) for k in (25, 26, 27)], run_time=0.6)
            vo.wait_until("Use option 1")
            self.play(Indicate(fix_rows[0], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("or add the keys with dash e")
            self.play(Indicate(fix_rows[1][1], color=ROUTE, scale_factor=1.06),
                      Indicate(fix_rows[2][1], color=ROUTE, scale_factor=1.06), FadeIn(bar28), run_time=0.8)
            self.play(Indicate(fix_rows[3][1], color=TURN, scale_factor=1.06), run_time=0.6)
        self.wait(2.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.remove(*self.mobjects)
        self.wait(0.3)
