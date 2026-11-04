"""S05 · Who touches the bytes? — tracker B5 → B6 → B5, `lref("6–7, 13")` the whole scene.

Beats (script.md, ## S05; one voiceover block each):
0. TRACKER B5. Slide 13 redrawn small in GREY (two containers, the bucket, the browser linked only to
   Label Studio) + chip. Then the source-storage form (`illustration`, README.md 121–134's values):
   Settings → Cloud Storage → Add Source Storage; Storage Type, Title, your-bucket-placeholder,
   cheeses_unlabeled, Import Method `Files - …`, ☑ Treat every bucket object … (GREY chip), ☑ Use
   pre-signed URLs (YELLOW), credentials + project ID empty (GREY chip).
1. The form shrinks to its prefix and Check Connection; the stand-in strip (extra · stand-in)
   prints 30:3 (wrapped), the message RED. The extra listing 29:2–4 (`/secrets` empty). TRACKER B6:
   the target form (README 138–146, cheeses_labeled, a WHITE envelope on "where labels go"), its
   stand-in strip 31:3, the message RED. No ▶ here.
2. The honest card (GREY), three lines on their sentences, then three GREY chips.
3. TRACKER B5. With a real key: Add Storage / Add Target Storage / Sync Storage flash, 21 task cards
   fan out of the BLUE bucket (tag recorded · README.md:136 + the 21 images of laptop/09). Our
   stand-in: 32:2–5 (wrapped) in a full output-only terminal, the three gs:// URIs highlighted,
   "task_count":3 YELLOW + chip "ours: 3 · yours: 21". ▶ your turn.
4. V2 steps 1–2a: reach, 21 cards fan, the browser asks 'task 1?'. PONDER 8 s.
5. V2 steps 2–3: the relay crossed out, the ticket stamped and walked to the vault's door, the key
   stays (GREEN); the photo bounces off the bouncer. Cliff-hanger: broken thumbnails
   (`illustration`) beside README.md · line 151. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S05"]
PONDER_Q = "Label Studio holds the key;\nyour browser never sees it.\nHow can it show a private photo?"
SLIDE_CHIP = "the slide links the browser only to Label Studio"
MISSING_CHIP = "may be missing in newer versions · carry on"
EMPTY_CHIP = "empty = the key the container already has"
NAME_CHIP = "the README's example name · yours differs"
MSG_SRC = "File /secrets/data-service-account.json was not found."
MSG_TGT = "Error validating storage connection"
CALL_SRC = "POST /api/storages/gcs/validate · stand-in"
CALL_TGT = "POST /api/storages/export/gcs/validate · stand-in"
CALL_IMPORT = "POST /api/projects/1/import · stand-in"
HONEST = (("This recording machine has no Google account, no bucket,",
           "no browser and no SSH route to GitHub."),
          ("The key in the folder listings is an obviously invalid stand-in,",
           "moved out before every cloud step."),
          ("Each cloud step shows the failure a misplaced key gives.",))
FORM_X0 = -5.85          # the form's left column (labels); fields start FIELD_DX right of it
FIELD_DX = 4.05


def drop(scene, *mobs) -> None:
    """Take mobjects and their whole families off the scene: a terminal that scrolled (room()) was
    split into parts on the scene, and a faded part left there snaps back at full opacity."""
    fam = []
    for m in mobs:
        fam.extend(m.get_family())
    scene.remove(*fam)


def glyphs(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` inside a label/mono Text (its .text drops spaces; so do its glyphs)."""
    flat, key = t.text.replace(" ", ""), sub.replace(" ", "")
    i = flat.index(key)
    return VGroup(*t.submobjects[i:i + len(key)])


def field_row(lab: str, val: str = "", field_w: float | None = None, val_color=INK) -> VGroup:
    """One form row: GREY label (20 pt), an input box holding a mono value (20 pt).
    Left edge at x 0. .label .field .value"""
    lt = label(lab, 20, S.GREY)
    vt = mono(val, 20, val_color) if val else None
    fw = field_w or ((vt.width + 0.45) if vt is not None else 2.0)
    fd = RoundedRectangle(width=fw, height=0.42, corner_radius=0.06, stroke_color=S.GREY_DARK,
                          stroke_width=1.5).set_fill(TERM_BG, 1)
    lt.move_to([0, 0, 0], aligned_edge=LEFT)
    fd.move_to([FIELD_DX + fw / 2, 0, 0])
    g = VGroup(lt, fd)
    if vt is not None:
        vt.move_to(fd).align_to(fd, LEFT).shift(RIGHT * 0.2)
        g.add(vt)
    g.label, g.field, g.value = lt, fd, vt
    return g


def check_row(lab: str, color=INK) -> VGroup:
    """A ticked checkbox row: box with a tick + label (22 pt). .box .tick .label"""
    bx = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.05, stroke_color=color, stroke_width=2)
    tk = check_mark(0.24, color, stroke=4).move_to(bx)
    lt = label(lab, 22, color).next_to(bx, RIGHT, buff=0.2)
    g = VGroup(bx, tk, lt)
    g.move_to([0, 0, 0], aligned_edge=LEFT)
    g.box, g.tick, g.label = bx, tk, lt
    return g


def button(s: str, color=S.GREY) -> VGroup:
    """A schematic button (label 22 pt in a filled GREY box). .box .text"""
    t = label(s, 22, INK)
    b = RoundedRectangle(width=t.width + 0.5, height=0.5, corner_radius=0.1, stroke_color=color,
                         stroke_width=2).set_fill(S.GREY_DARKER, 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def stand_in_strip(call: str, rows: int = 4):
    """An output-only stand-in strip (never typed): the call as its heading on the title bar,
    'extra · stand-in' at the bar's right end. 4 rows: the whole folded JSON reply fits, so no
    row scrolls away and none starts mid-word. Returns (terminal, heading, tag)."""
    t = term(P_LABELING, rows=rows, title=None)
    hd = strip_head(call).move_to([t.box.get_center()[0] - 0.9, t.box.get_top()[1] - t.bar_h / 2, 0])
    tg = on_bar(t, standin_row())
    return t, hd, tg


def fold_json(s: str, n: int = 65) -> list[str]:
    """A one-line JSON reply folded at its own commas/brackets (text unchanged, only the row breaks
    move: the script's `wrap`), so every row starts on a key or a value, never mid-word."""
    rows = []
    while len(s) > n:
        k = max(s.rfind(",", 0, n), s.rfind("[", 0, n))
        if k <= 0:
            return rows + soft([s], n)
        rows.append(s[:k + 1])
        s = s[k + 1:]
    return rows + [s]


def mini_form(head: str, prefix: str) -> VGroup:
    """The storage form reduced to its prefix and its Check Connection button (illustration).
    .win .head .prefix .btn"""
    win = window("localhost:8080", 8.4, 2.45).move_to([-0.9, 1.5, 0])
    hd = label(head, 22, INK).move_to(win.content).align_to(win.content, UP).shift(DOWN * 0.12)
    hd.align_to(win.frame, LEFT).shift(RIGHT * 0.45)
    pr = field_row("Bucket Prefix", prefix)
    pr.move_to([win.frame.get_left()[0] + 0.45, hd.get_center()[1] - 0.58, 0], aligned_edge=LEFT)
    bt = button("Check Connection").move_to([0, pr.get_center()[1] - 0.6, 0]).align_to(hd, LEFT)
    g = VGroup(win, hd, pr, bt)
    g.win, g.head, g.prefix, g.btn = win, hd, pr, bt
    return g


def slide13() -> VGroup:
    """Slide 13's idea, redrawn small in GREY: the two containers, the bucket, the browser linked
    only to Label Studio. .studio .cli .bucket .browser .link (browser → studio, not added)"""
    st = house(CONTAINERS["studio"], 2.6, 1.0, color=S.GREY).move_to([-1.3, 1.25, 0], aligned_edge=DOWN)
    cl = house(CONTAINERS["cli"], 2.3, 1.0, color=S.GREY).move_to([1.7, -0.05, 0], aligned_edge=DOWN)
    bk = vault("GCS bucket", (), S.GREY, 22, mono_title=False, vault_w=2.4).move_to([4.5, 1.57, 0])
    br = browser_glyph(name="browser", glyph_w=1.1).move_to([-4.6, 1.5, 0])
    l1 = Line(br.window.get_right(), st.body.get_left(), color=S.GREY, stroke_width=3)
    l2 = Line(st.body.get_right(), [bk.frame.get_left()[0], st.body.get_center()[1], 0], color=S.GREY,
              stroke_width=3)
    fr = RoundedRectangle(width=11.2, height=2.85, corner_radius=0.18, stroke_color=S.GREY_DARK,
                          stroke_width=2).move_to([0, 1.25, 0])
    g = VGroup(fr, st, cl, bk, br, l2)
    g.studio, g.cli, g.bucket, g.browser, g.link = st, cl, bk, br, l1     # .link: not added (Create it)
    return g


class WhoTouchesBytes(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S05"] == 6, len(SAY)

        # ========================================================== 0. slide 13, then the source form
        tr = tracker("B", 5)
        ref = lref("6–7, 13")
        sk = slide13()
        sk_lbl = note("slide 13, redrawn").move_to(sk[0]).align_to(sk[0], DL).shift(UP * 0.18 + RIGHT * 0.3)
        sk_chip = grey_chip(SLIDE_CHIP).next_to(sk, DOWN, buff=0.3)

        win = window("localhost:8080", 12.4, 6.0).move_to([0, -0.27, 0])
        y_top = win.frame.get_top()[1] - 0.55
        crumbs = VGroup(label("Settings", 22, INK), label("→", 22, S.GREY), label("Cloud Storage", 22, INK),
                        label("→", 22, S.GREY), label("Add Source Storage", 22, INK)).arrange(RIGHT, buff=0.2)
        crumbs.move_to([FORM_X0, y_top - 0.35, 0], aligned_edge=LEFT)
        ill = illustration_tag().move_to([0, crumbs.get_center()[1], 0]).align_to(win.frame, RIGHT).shift(LEFT * 0.2)
        rows = [field_row("Storage Type", "Google Cloud Storage"),
                field_row("Storage Title", "Cheese Images"),
                field_row("Bucket Name", BUCKET),
                field_row("Bucket Prefix", "cheeses_unlabeled"),
                field_row("Import Method", "Files - …"),
                check_row("Treat every bucket object as a source file"),
                check_row("Use pre-signed URLs", TURN),
                field_row("Google Application Credentials"),
                field_row("Google Project ID")]
        for i, r in enumerate(rows):
            r.move_to([FORM_X0, y_top - 0.95 - 0.5 * i, 0], aligned_edge=LEFT)
        r_type, r_title, r_bucket, r_prefix, r_import, r_treat, r_presign, r_cred, r_pid = rows
        miss = grey_chip(MISSING_CHIP).next_to(r_treat, RIGHT, buff=0.35)
        brace = Brace(VGroup(r_cred.field, r_pid.field), RIGHT, buff=0.12, color=S.GREY)
        empt = grey_chip(EMPTY_CHIP).next_to(brace, RIGHT, buff=0.12)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.6)
            self.play(FadeIn(VGroup(sk, sk_lbl), scale=0.96), run_time=0.7)
            self.play(Create(sk.link), Indicate(sk.browser.window, color=INK, scale_factor=1.08), run_time=0.7)
            self.play(FadeIn(sk_chip, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("and add source storage")
            self.play(FadeOut(VGroup(sk, sk.link, sk_lbl, sk_chip)), run_time=0.4)
            drop(self, sk, sk.link, sk_lbl, sk_chip)
            self.play(FadeIn(win, scale=0.98), FadeIn(ill), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in crumbs], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("Use the README's values")
            self.play(LaggedStart(FadeIn(r_type, shift=RIGHT * 0.15), FadeIn(r_title, shift=RIGHT * 0.15),
                                  lag_ratio=0.4), run_time=0.7)
            self.play(Indicate(r_type.value, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("your bucket")
            self.play(FadeIn(r_bucket, shift=RIGHT * 0.15), run_time=0.4)
            self.play(Indicate(r_bucket.value, color=CLOUD, scale_factor=1.06), run_time=0.5)
            vo.wait_until("the prefix cheeses unlabeled")
            self.play(FadeIn(r_prefix, shift=RIGHT * 0.15), FadeIn(r_import, shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(r_prefix.value, color=CLOUD, scale_factor=1.06), run_time=0.5)
            vo.wait_until("and pre-signed URLs on")
            self.play(FadeIn(r_treat, shift=RIGHT * 0.15), FadeIn(r_presign, shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(r_presign.label, color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("If a checkbox is missing")
            self.play(FadeIn(miss, shift=LEFT * 0.15), Indicate(r_treat.label, color=INK, scale_factor=1.04),
                      run_time=0.6)
            vo.wait_until("Leave the credentials empty")
            self.play(FadeIn(r_cred, shift=RIGHT * 0.15), FadeIn(r_pid, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("that means the key")
            self.play(GrowFromCenter(brace), FadeIn(empt, shift=LEFT * 0.15), run_time=0.6)

        # ========================================================== 1. Check Connection fails; why; target too
        src = mini_form("Add Source Storage", "cheeses_unlabeled")
        ill_m = illustration_tag().next_to(src.win, RIGHT, buff=0.25).align_to(src.win, UP)
        t1, hd1, tg1 = stand_in_strip(CALL_SRC)
        c29, c30, c31 = capture("29"), capture("30"), capture("31")
        lt = term(P_LABELING, rows=5)
        tgt = mini_form("Add Target Storage", "cheeses_labeled")
        ill_t = illustration_tag().next_to(tgt.win, RIGHT, buff=0.25).align_to(tgt.win, UP)
        env = annotation("gouda", 1.1, 0.62, 20).next_to(tgt.prefix, RIGHT, buff=0.4)
        t2, hd2, tg2 = stand_in_strip(CALL_TGT)

        with self.voiceover(SAY[1]) as vo:
            rest = VGroup(crumbs, ill, r_type, r_title, r_bucket, r_import, r_treat, r_presign, r_cred, r_pid,
                          miss, brace, empt)
            self.play(FadeOut(rest), Transform(win, src.win), Transform(r_prefix, src.prefix),
                      FadeIn(src.head), FadeIn(src.btn), FadeIn(ill_m), run_time=0.8)
            drop(self, rest)
            self.play(Indicate(src.btn.text, color=TURN, scale_factor=1.1), FadeIn(t1), FadeIn(hd1),
                      FadeIn(tg1), run_time=0.7)
            vo.wait_until("Here it fails")
            r30 = out(self, t1, fold_json(c30.at(3)[0], t1.max_chars), run_time=0.8)
            msg = substring(r30[-1], MSG_SRC)
            self.play(msg.animate.set_color(ERR), run_time=0.4)
            u30 = under(msg, ERR, stroke=3)
            self.play(Create(u30), run_time=0.4)
            vo.wait_until("An extra listing shows why")
            self.wait(1.5)          # hold the red message: it went RED only ~1.5 s before this sentence
            old = VGroup(win, r_prefix, src.head, src.btn, ill_m, t1, hd1, tg1, u30)
            self.play(FadeOut(old), FadeOut(VGroup(*t1.lines)), FadeIn(lt), run_time=0.5)
            drop(self, old, *t1.lines)
            ln = type_cmd(self, lt, c29.cmd, type_time=0.8)
            xt = beside(extra_row(), ln)
            pin(self, ln, xt)
            out(self, lt, c29.at((2, 4)), run_time=0.5)
            vo.wait_until("inside Label Studio is empty")
            dots = [lt.lines[-2], lt.lines[-1]]
            et = beside(row_tag("empty: no key file", ERR), lt.lines[-3])
            pin(self, lt.lines[-3], et)
            self.play(each([substring(r, r.text.split()[-1]) for r in dots], ERR, scale=1.3, lag=0.3), run_time=0.7)
            vo.wait_until("The target storage")
            self.play(FadeOut(VGroup(lt, *lt.lines)), FadeIn(VGroup(tgt, ill_t)), track(tr, 6), run_time=0.7)
            drop(self, lt, *lt.lines)
            vo.wait_until("where labels go")
            self.play(FadeIn(env, shift=DOWN * 0.3, scale=0.8), run_time=0.5)
            vo.wait_until("with the prefix cheeses labeled")
            self.play(Indicate(tgt.prefix.value, color=CLOUD, scale_factor=1.08), run_time=0.5)
            vo.wait_until("fails too")
            self.play(Indicate(tgt.btn.text, color=TURN, scale_factor=1.1), FadeIn(t2), FadeIn(hd2), FadeIn(tg2),
                      run_time=0.6)
            r31 = out(self, t2, fold_json(c31.at(3)[0], t2.max_chars), run_time=0.8)
            msg2 = substring(r31[-1], MSG_TGT)
            self.play(msg2.animate.set_color(ERR), run_time=0.4)

        # ========================================================== 2. the honest note
        items = [VGroup(*[label(s, 24, INK) for s in ls]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
                 for ls in HONEST]
        hcard = card(items, head="one honest note about this recording", buff=0.32, card_w=11.0)
        hcard.move_to([0, 0.55, 0])
        chips = VGroup(grey_chip("recorded · source named"), grey_chip("extra · stand-in"),
                       grey_chip("extra · local remote")).arrange(RIGHT, buff=0.45)
        chips.next_to(hcard, DOWN, buff=0.45)

        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(tgt, ill_t, env, t2, hd2, tg2)
            self.wait(1.2)          # hold the target's RED message: it turned RED as block 1 ended
            self.play(FadeOut(gone), FadeOut(VGroup(*t2.lines)), run_time=0.5)
            drop(self, gone, *t2.lines)
            self.play(FadeIn(hcard.frame, scale=0.97), FadeIn(hcard.head), run_time=0.6)
            vo.wait_until("This machine has no Google account")
            self.play(FadeIn(items[0], shift=UP * 0.15), run_time=0.7)
            vo.wait_until("no browser")
            self.play(Indicate(glyphs(items[0][1], "no browser"), color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and no SSH route to GitHub")
            self.play(Indicate(glyphs(items[0][1], "no SSH route to GitHub"), color=INK, scale_factor=1.06),
                      run_time=0.7)
            vo.wait_until("The key in the folder listings")
            self.play(FadeIn(items[1], shift=UP * 0.15), run_time=0.7)
            vo.wait_until("moved out before every cloud step")
            self.play(Indicate(items[1][1], color=INK, scale_factor=1.04), run_time=0.7)
            vo.wait_until("So each cloud step here fails")
            self.play(FadeIn(items[2], shift=UP * 0.15), run_time=0.7)
            vo.wait_until("That is the most common mistake")
            mk = glyphs(items[2][0], "a misplaced key")
            u_mk = under(mk, TURN, stroke=3)
            self.play(Create(u_mk), Indicate(mk, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Every success you should expect")
            self.play(FadeIn(chips[0], shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(chips[0].text, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and clicks and uploads are replayed locally")
            self.play(LaggedStart(FadeIn(chips[1], shift=UP * 0.2), FadeIn(chips[2], shift=UP * 0.2), lag_ratio=0.4),
                      run_time=0.8)

        # ========================================================== 3. with a real key: sync; our stand-in: 3
        def panel(head: str, btns) -> VGroup:
            hd = VGroup(label(head[0], 22, INK), label("·", 22, S.GREY), mono(head[1], 20, INK)).arrange(RIGHT, buff=0.15)
            bs = VGroup(*[button(b) for b in btns]).arrange(RIGHT, buff=0.3)
            body = VGroup(hd, bs).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            fr = RoundedRectangle(width=5.9, height=body.height + 0.5, corner_radius=0.14, stroke_color=S.GREY,
                                  stroke_width=2).set_fill(PANEL, 1)
            body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
            g = VGroup(fr, body)
            g.btns = bs
            return g

        p_src = panel(("source", "cheeses_unlabeled"), ("Add Storage", "Sync Storage")).move_to([-3.25, 1.45, 0])
        p_tgt = panel(("target", "cheeses_labeled"), ("Add Target Storage",)).move_to([-3.25, -0.35, 0])
        ill3 = illustration_tag().next_to(p_tgt, DOWN, buff=0.2).align_to(p_tgt, LEFT)
        bk = vault(BUCKET, ("cheeses_unlabeled/", "cheeses_labeled/"), CLOUD, 20, vault_w=4.4).move_to([3.55, 1.75, 0])
        cs = task_cards(21, 0.42, 7).move_to([3.55, -0.05, 0])
        n21 = grey_chip("one task per photo · 21").next_to(cs, DOWN, buff=0.25)
        rec = recorded_tag("recorded · README.md:136 + the 21 images of laptop/09").move_to([0, -2.45, 0])
        rec.align_to(bk, RIGHT)
        c32 = capture("32")
        t3 = term(P_LABELING, rows=9, title=None)
        hd3 = strip_head(CALL_IMPORT).move_to([t3.box.get_center()[0] - 0.9, t3.box.get_top()[1] - t3.bar_h / 2, 0])
        tg3 = on_bar(t3, standin_row())
        ours = grey_chip("ours: 3 · yours: 21", color=TURN).move_to([0, t3.box.get_top()[1] + 0.45, 0])
        ours.align_to(t3.box, RIGHT)
        yt = your_turn().move_to([0, t3.box.get_top()[1] + 0.45, 0]).align_to(t3.box, LEFT)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(hcard, chips, u_mk)), track(tr, 5), run_time=0.6)
            drop(self, hcard, chips, u_mk)
            self.play(FadeIn(p_src, shift=RIGHT * 0.2), FadeIn(p_tgt, shift=RIGHT * 0.2), FadeIn(ill3),
                      FadeIn(bk, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("add both storages")
            self.play(each([p_src.btns[0].text, p_tgt.btns[0].text], TURN, scale=1.1, lag=0.5),
                      FadeIn(rec, shift=UP * 0.15), run_time=1.0)    # the recorded tag up ≥ 4 s
            vo.wait_until("and click sync")
            self.play(Indicate(p_src.btns[1].text, color=TURN, scale_factor=1.12),
                      Indicate(bk.drawers["cheeses_unlabeled/"].text, color=CLOUD, scale_factor=1.06), run_time=0.6)
            src_pt = bk.drawers["cheeses_unlabeled/"].get_center()
            self.play(LaggedStart(*[FadeIn(c, target_position=src_pt, scale=0.5) for c in cs], lag_ratio=0.04),
                      run_time=1.3)
            vo.wait_until("one task per photo")
            self.play(FadeIn(n21, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(n21.text, color=INK, scale_factor=1.08), run_time=0.5)
            vo.wait_until("Our stand-in imports")
            pic = VGroup(p_src, p_tgt, ill3, bk, cs, n21, rec)
            self.play(FadeOut(pic), run_time=0.5)
            drop(self, pic)
            self.play(FadeIn(t3), FadeIn(hd3), FadeIn(tg3), run_time=0.5)
            r32 = out(self, t3, c32.at((2, 5)), wrap=True, run_time=1.2)
            uris = [substring(r, r.text.split('"')[1]) for r in r32 if r.text.startswith('"gs://')]
            vo.wait_until("3 tasks")
            tc = substring(r32[6], '"task_count":3')
            self.play(tc.animate.set_color(TURN), FadeIn(ours, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(tc, color=TURN, scale_factor=1.1), run_time=0.5)
            vo.wait_until("with the same kind of addresses")
            self.play(each(uris, CLOUD, scale=1.04, lag=0.3), run_time=1.2)
            vo.wait_until("Pause, add both")
            self.play(FadeIn(yt, shift=RIGHT * 0.2), run_time=0.4)
            flash_tag(self, yt, TURN)

        # ========================================================== 4. who touches the photos?
        v2 = SignedTicket()
        # the vault is the README's bucket name (script: V2 'cheese-app-data-demo'); the forms said
        # your-bucket-placeholder, so say once that the README's name is an example
        nm = grey_chip(NAME_CHIP).next_to(v2.frame, DOWN, buff=0.25).align_to(v2.vault.frame, RIGHT)  # clear of the laptop frame

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(t3, hd3, tg3, ours, yt)
            self.play(FadeOut(gone), FadeOut(VGroup(*t3.lines)), run_time=0.5)
            drop(self, gone, *t3.lines)
            self.play(FadeIn(v2), run_time=0.8)
            self.play(FadeIn(nm, shift=UP * 0.15), Indicate(v2.vault.title, color=CLOUD, scale_factor=1.06),
                      run_time=0.6)
            vo.wait_until("Label Studio holds the key")
            self.play(Indicate(v2.key, color=KEY, scale_factor=1.15), run_time=0.6)
            vo.wait_until("and lists the bucket")
            ar = v2.reach(self)
            cards = v2.cards()
            self.play(v2.fan(cards))
            vo.wait_until("your browser asks for task 1")
            bub = v2.hand()
            self.play(FadeIn(bub, shift=UP * 0.15), Indicate(v2.browser.window, color=INK, scale_factor=1.06),
                      FadeOut(nm), run_time=0.7)      # nm off before the ponder card half-covers it
            self.remove(nm)
        pc = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 5. a signed ticket; the cliff-hanger
        rl = v2.relay()
        grid = VGroup(*[tile(None, 0.7, LAPTOP, broken=True) for _ in range(8)]).arrange_in_grid(rows=2, cols=4,
                                                                                               buff=0.3)
        pg = window("localhost:8080", 5.4, 3.4).move_to([-3.6, 0.75, 0])
        grid.move_to(pg.content)
        ill5 = illustration_tag().next_to(pg, DOWN, buff=0.2).align_to(pg, RIGHT)
        body = VGroup(label("At this point, you will notice that you", 24, INK),
                      label("can't access the images and instead receive", 24, INK),
                      label("an error message related to CORS.", 24, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rc = readme_card(151, body, quote=True).move_to([3.0, 0.75, 0])
        cors = glyphs(body[2], "CORS")

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            vo.wait_until("does not relay the photos")
            self.play(FadeOut(VGroup(bub, ar, *cards[7:])), run_time=0.4)
            drop(self, bub, ar, *cards[7:])
            self.play(Create(rl.route), run_time=0.6)
            self.play(Create(rl.strike), run_time=0.3)
            vo.wait_until("it signs a web address")
            self.play(FadeOut(rl), run_time=0.3)
            drop(self, rl)
            tk = v2.stamp(self)
            vo.wait_until("permission for one photo")
            self.play(Indicate(tk.text, color=INK, scale_factor=1.1), run_time=0.5)
            vo.wait_until("for a short time")
            self.play(Indicate(tk.glass, color=CLOUD, scale_factor=1.25), run_time=0.6)
            vo.wait_until("Your browser carries that ticket")
            self.play(FadeIn(v2.bouncer), run_time=0.3)
            rt, ph, ck = v2.walk(self, tk)
            vo.wait_until("and the key stays")
            self.play(Indicate(v2.key, color=KEY, scale_factor=1.2), run_time=0.7)
            vo.wait_until("Then the thumbnails break")
            gone = VGroup(v2, v2.bouncer, *cards[:7], tk, rt, ph, ck)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(pg), FadeIn(ill5), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in grid], lag_ratio=0.1), run_time=0.8)
            vo.wait_until("and the README warns you")
            self.play(FadeIn(rc, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("it is CORS")
            self.play(Indicate(cors, color=TURN, scale_factor=1.25), run_time=0.7)
        self.wait(2.0)              # let the README quote be read before the fade (it arrives ~2 s before the end)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
