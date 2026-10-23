"""S04 · Two filesystems, one folder (AC215 L10) — tracker A3 → A4, `Lecture 10 · slides 38, 42`.

Beats (script.md, ## S04; one voiceover block each):
0. V3 (SecretsPortalRig) tree at the bottom, the README's own step (README.md · line 56) on top; a
   YELLOW '?' where the folder goes. CODE(api-service/docker-shell.sh: 6–11, 20 pt) replaces the
   card, line 8 lit; the PINK cursor starts at api-service/ ('$(pwd)'), hops '..' '..' to AC215/ and
   lands on secrets/ (GREEN), each hop underlining its piece of line 8.
1. CODE(19–27) replaces the first panel: line 23 (`-v "$SECRETS_DIR":/secrets`, host part GREY,
   container part TEAL). On "inside the container" the panel narrows to lines 23–24 at the bottom,
   the portal rises (tree + TEAL container), the GREEN tube connects, captions 'host path' /
   'container path'. Line 24 lights; GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json
   (line 10's value, noted) appears in the box; a PINK pointer snaps onto the key file; the GREY
   'Google library' chip reads it; a GREEN dot runs the tube on "Two filesystems, one folder".
2. CODE(llm-rag/docker-compose.yml: 10–12), line 11; the cursor climbs again from llm-rag/ (two
   hops, underlining '../' '../'), the tube redraws. GREY note 'slides: ../secrets · L11's repos sit
   one level shallower'.
3. TRACKER A3 · extra: the running map (AppMap.at("S04")) over a 3-row strip; `mkdir ../secrets`
   (laptop/04, extra; GREY bar tag 'the README shows a tree, not a command'); the GREEN secrets/
   drawer appears on the map. TRACKER A3: a GREY file slides from Downloads into secrets/ and is
   renamed llm-service-account.json (`illustration`); 'Check that name' rings it, a struck RED
   `.json.json` below. TRACKER A4 · extra: the strip grows; `cd ..`, `tree -L 2 .` (laptop/05: 2–11)
   beside the README card (README.md · lines 60–67), folder-for-folder YELLOW links, README.md
   dimmed; GREY chip 'no tree? …'; `ls -la secrets` (laptop/06: 2–5, the long row soft-wrapped),
   the name ringed GREEN, GREY chip 'not .json.json · llm-finetuning README.md:67', `▶ your turn`.
4. CODE(.gitignore: 1–7), lines 6–7 GREY bars, a RED dashed slot under line 7, 'no rule for secrets/'.
5. The tree with the key inside the repo (RED rows, RED outline), no AC215/secrets/. PONDER 1 (8 s)
   on the right, the tree stays visible.
6. Replay: the TEAL box; the cursor climbs to AC215/; the empty GREEN folder pops ('created by
   Docker, empty'); the tube carries nothing, '/secrets/' is empty; the env var points at an empty
   RED dashed slot; laptop/33:162's DefaultCredentialsError (2 rows, RED) under it. Then the box
   side goes and the key inside the repo flashes RED with 'inside a git tree · no rule protects it'.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer.components import ponder_card

from common import (ERR, IMAGE, INK, KEY, LAPTOP, NARRATION, P_LAPTOP_HOME, P_REPO, ROUTE, SAY_COUNT, TURN,
                    AppMap, SecretsPortalRig, beside, bare_prompt, capture, cd_prompt, code, code_span,
                    cut, each, err_chip, excerpt, extra_row, file_glyph, folder_glyph, grey_chip,
                    flash_tag, illustration_tag, label, line_bar, lref, mono, mono_line, note, on_bar, out, pin,
                    readme, readme_card, resize, ring, row_tag, strike, substring, term, track, tracker,
                    type_cmd, under, unpin, your_turn)
from explainer import style as S

SAY = NARRATION["S04"]
SHELL = "cheese-app-v0/api-service/docker-shell.sh"
COMPOSE = "cheese-app-v0/llm-rag/docker-compose.yml"
PONDER_1 = ("You save the key inside the repo,\ncheese-app-v0/secrets/llm-service-account.json,\n"
            "then run sh docker-shell.sh from api-service/.\nWhat is in /secrets, and what happens\n"
            "on the first embedding call?")
STEP_56 = "7. Copy this JSON file into the **secrets** folder and rename it to `llm-service-account.json`."


# ------------------------------------------------------------------ local pieces
def step_card() -> VGroup:
    """README.md · line 56 in the README's own words (markdown emphasis dropped). .secrets"""
    assert readme(56) == STEP_56, readme(56)
    sec = mono("secrets", 24, KEY)
    r1 = VGroup(label("7. Copy this JSON file into the", 26, INK), sec, label("folder", 26, INK))
    r1.arrange(RIGHT, buff=0.14)
    r2 = VGroup(label("and rename it to", 26, INK), mono("llm-service-account.json", 24, INK),
                label(".", 26, INK)).arrange(RIGHT, buff=0.12)
    for r in (r1, r2):
        for m in r[1:]:
            m.align_to(r[0], DOWN)
    r2[2].shift(LEFT * 0.08)
    body = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    g = readme_card(56, body)
    g.secrets = sec
    return g


def tree_card() -> VGroup:
    """README.md · lines 60–67: the README's tree (lines 61–66), comments cut with a GREY '…'.
    .rows (6 mono_lines: cheese-app-v0, llm-rag, api-service, frontend-ai-chatbot, secrets, key)"""
    rows = VGroup()
    for n in range(61, 67):
        s = excerpt("cheese-app-v0/README.md", n, n)
        if "#" in s:
            s = cut(s, "# ")
            rows.add(mono_line(s, 20, INK, t2c={"# …": S.GREY}))
        else:
            rows.add(mono_line(s, 20, INK))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    g = readme_card((60, 67), rows)
    g.rows = rows
    return g


def hop(sp, name, span=None, color=ROUTE):
    """One '..' hop of the cursor to tree row `name`: returns (ring target, '..' label, underline of
    `span` in a code line or None, the animations that show them) for the caller to play."""
    tgt = sp.cursor_on(name, color)
    dots = mono("..", 20, color).next_to(tgt, RIGHT, buff=0.2)
    anims = [FadeIn(dots, shift=UP * 0.15)]
    u = None
    if span is not None:
        u = under(span, color, stroke=3)
        anims.append(Create(u))
    return tgt, dots, u, anims


def ponder_right(scene, question: str, seconds: float, card_w: float, center) -> VGroup:
    """pause_and_ponder, placed: the card sits right of the tree so the tree stays readable."""
    pc = ponder_card(question, width=card_w).move_to(center)
    scene.play(FadeIn(pc, scale=0.95), run_time=0.6)
    bar = pc[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return pc


def clear_but(scene, *keep, anims=(), run_time: float = 0.6):
    """Plays: everything on screen fades except the families of `keep` (the tracker and the lecture
    tag; a track() animation may have split the tracker into parts on the scene), then `keep` is
    re-added whole."""
    ids = {id(f) for k in keep for f in k.get_family()}
    drop = [x for x in scene.mobjects if not any(id(f) in ids for f in x.get_family())]
    scene.play(FadeOut(Group(*drop)), *anims, run_time=run_time)
    scene.remove(*drop)
    scene.add(*keep)


class SecretsPortal(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S04"] == 7, len(SAY)

        # ========================================================== 0. which secrets folder? line 8
        tr = tracker("A", 3)
        ref = lref("38, 42")
        sp = SecretsPortalRig()
        rows = sp.tree.rows
        sp.tree.shift(DOWN * 2.05)                       # tree low, the card / panel above it
        sp.caption.next_to(rows[0], RIGHT, buff=0.9)
        shown = VGroup(*rows[:5])
        sec_rows = VGroup(rows[5], rows[6])
        q = label("?", 40, TURN).move_to(rows[5].name_text).align_to(rows[5].name_text, LEFT)
        sc = step_card().move_to([0, 1.3, 0])
        p1 = code(SHELL, 6, 11, font_size=20)
        p1.move_to([0, 2.78 - p1.height / 2, 0])
        bar8 = line_bar(p1.code, 2, TURN)
        s_pwd = code_span(p1.code, 2, "$(pwd)")
        s_up = [code_span(p1.code, 2, "/..", 0), code_span(p1.code, 2, "/..", 1)]
        s_sec = code_span(p1.code, 2, "secrets/")

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.6)
            self.play(FadeIn(sc, shift=DOWN * 0.2), FadeIn(shown), FadeIn(sp.caption), run_time=0.9)
            self.play(Indicate(sc.secrets, color=KEY, scale_factor=1.2), run_time=0.7)
            vo.wait_until("Which one?")
            self.play(FadeIn(q, scale=0.6), run_time=0.5)
            vo.wait_until("The API's script answers")
            self.play(FadeOut(sc, shift=UP * 0.2), FadeIn(p1, shift=DOWN * 0.2), run_time=0.8)
            self.play(FadeIn(bar8), run_time=0.4)
            vo.wait_until("The path starts where you run it")
            cur = sp.cursor_on("api-service/")
            pwd = mono("$(pwd)", 20, ROUTE).next_to(cur, RIGHT, buff=0.2)
            u_pwd = under(s_pwd, ROUTE, stroke=3)
            self.play(Create(cur), FadeIn(pwd, shift=LEFT * 0.1), Create(u_pwd), run_time=0.7)
            vo.wait_until("It climbs up twice")
            hops, unders = VGroup(), VGroup(u_pwd)
            for i, name in enumerate(("cheese-app-v0/", "AC215/")):
                tgt, dots, u, anims = hop(sp, name, s_up[i])
                if i == 0:
                    anims.append(FadeOut(pwd))
                self.play(Transform(cur, tgt), *anims, run_time=0.6)
                hops.add(dots)
                unders.add(u)
            self.remove(pwd)
            vo.wait_until("and lands on the secrets folder")
            self.play(FadeOut(q), FadeIn(sec_rows, shift=RIGHT * 0.2), run_time=0.5)
            u_sec = under(s_sec, KEY, stroke=3)
            unders.add(u_sec)
            self.play(Transform(cur, ring(rows[5], ROUTE, buff=0.07)), FadeOut(hops), Create(u_sec), run_time=0.6)
            self.remove(hops)
            self.play(cur.animate.set_stroke(KEY), Indicate(rows[5].name_text, color=KEY, scale_factor=1.1),
                      run_time=0.6)
            vo.wait_until("beside the repo")
            sib = DashedLine(rows[1].glyph.get_bottom() + DOWN * 0.05, rows[5].glyph.get_top() + UP * 0.05,
                             color=TURN, stroke_width=3, dash_length=0.08)
            self.play(Create(sib), each([rows[1].name_text, rows[5].name_text], TURN, scale=1.12, lag=0.3),
                      run_time=1.0)
            vo.wait_until("not inside it")
            self.play(Indicate(rows[1].name_text, color=INK, scale_factor=1.08), run_time=0.6)

        # ========================================================== 1. the mount and the variable
        p2 = code(SHELL, 19, 27, font_size=20).move_to([0, 0.3, 0])
        bar23 = line_bar(p2.code, 4, KEY)
        host_span = code_span(p2.code, 4, '"$SECRETS_DIR"')
        cont_span = code_span(p2.code, 4, ":/secrets")[1:]
        win = code(SHELL, 23, 24, font_size=20)
        win.move_to([0, -3.5 + win.height / 2, 0])
        # the portal, raised (box and tree) so captions and the narrow panel fit under it
        up = 2.05 + 0.55
        sp.box.shift(UP * 0.55)
        lift = VGroup(sp.tree, sp.caption)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(p1, bar8, unders, cur, sib)), FadeOut(lift), run_time=0.6)
            self.remove(p1, bar8, unders, cur, sib)
            lift.shift(UP * up)                          # off screen: move freely
            sp.host_cap.next_to(sp.tree, DOWN, buff=0.28).align_to(sp.tree, LEFT)
            sp.cont_cap.next_to(sp.box.frame, DOWN, buff=0.18).align_to(sp.box.frame, LEFT)
            self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Then a dash v flag mounts")
            self.play(FadeIn(bar23), run_time=0.4)
            vo.wait_until("that host folder")
            u_host = under(host_span, S.GREY, stroke=3)
            self.play(Create(u_host), Indicate(host_span, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("at slash secrets")
            u_cont = under(cont_span, IMAGE, stroke=3)
            self.play(Create(u_cont), Indicate(cont_span, color=IMAGE, scale_factor=1.15), run_time=0.6)
            vo.wait_until("inside the container")
            others = VGroup(*[p2.code.code_lines[i] for i in range(len(p2.code.code_lines)) if i not in (4, 5)])
            self.play(FadeOut(others), FadeOut(VGroup(bar23, u_host, u_cont)),
                      ReplacementTransform(p2.code.background, win.code.background),
                      FadeTransform(p2.header, win.header),
                      ReplacementTransform(p2.code.code_lines[4], win.code.code_lines[0]),
                      ReplacementTransform(p2.code.code_lines[5], win.code.code_lines[1]),
                      FadeIn(lift), FadeIn(sp.box), run_time=1.0)
            self.remove(p2, others, bar23, u_host, u_cont)
            self.add(win)
            self.play(sp.connect(), run_time=0.9)
            self.play(FadeIn(sp.host_cap, shift=UP * 0.1), FadeIn(sp.cont_cap, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("The Google application credentials variable")
            bar24 = line_bar(win.code, 1, ROUTE)
            lab = sp.env_label()
            v10 = note("line 10's value").next_to(lab, DOWN, buff=0.14).align_to(lab, LEFT)
            self.play(FadeIn(bar24), FadeIn(lab, shift=UP * 0.3), run_time=0.7)
            self.play(FadeIn(v10, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("which tells Google's library")
            ptr = Arrow(lab[1].get_right() + RIGHT * 0.05, sp.box.file.get_right() + RIGHT * 0.15, buff=0.05,
                        color=ROUTE, stroke_width=3, tip_length=0.16, path_arc=1.2,
                        max_tip_length_to_length_ratio=0.3)
            self.play(Create(ptr), run_time=0.6)
            edge = sp.box.lib.box.copy().set_fill(opacity=0)
            self.play(Indicate(sp.box.lib.text, color=INK, scale_factor=1.15),
                      edge.animate(rate_func=there_and_back).set_stroke(width=4), run_time=0.7)
            self.remove(edge)
            vo.wait_until("points to slash secrets")
            self.play(Indicate(lab[1][:8], color=IMAGE, scale_factor=1.2),
                      Indicate(sp.box.mount[1], color=KEY, scale_factor=1.15), run_time=0.8)
            vo.wait_until("a path inside the container")
            self.play(Indicate(sp.cont_cap, color=IMAGE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("Two filesystems, one folder")
            dot = Dot(sp.tube_mob.core.get_start(), radius=0.09, color=KEY)
            self.play(FadeIn(dot), Indicate(sp.host_cap, color=INK, scale_factor=1.15), run_time=0.4)
            self.play(MoveAlongPath(dot, sp.tube_mob.core), run_time=0.9)
            self.play(FadeOut(dot), Indicate(sp.cont_cap, color=IMAGE, scale_factor=1.15), run_time=0.5)
            self.remove(dot)
            vo.wait_until("only makes sense after the mount")
            bar23w = line_bar(win.code, 0, KEY)
            self.play(FadeIn(bar23w), sp.tube_mob[0].animate(rate_func=there_and_back).set_stroke(width=26),
                      run_time=0.9)

        # ========================================================== 2. the compose file: same portal
        p3 = code(COMPOSE, 10, 12)
        p3.move_to([-6.4 + p3.width / 2, -3.5 + p3.height / 2, 0])
        bar11 = line_bar(p3.code, 1, KEY)
        c_up = [code_span(p3.code, 1, "../", 0), code_span(p3.code, 1, "../", 1)]
        c_sec = code_span(p3.code, 1, "secrets", 0)
        slide = VGroup(note("slides: ../secrets"), note("L11's repos sit one level shallower"))
        slide.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        slide.move_to([0.5 + slide.width / 2, p3.get_center()[1], 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(win, bar24, bar23w, lab, v10, ptr)), run_time=0.5)
            self.remove(win, bar24, bar23w, lab, v10, ptr)
            self.play(FadeIn(p3, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(bar11), run_time=0.4)
            vo.wait_until("from its own folder")
            old_tube = sp.tube_mob
            cur = sp.cursor_on("llm-rag/")
            here = note("compose file here", ROUTE).next_to(cur, RIGHT, buff=0.2)
            self.play(FadeOut(old_tube), Create(cur), FadeIn(here, shift=LEFT * 0.1), run_time=0.7)
            self.remove(old_tube)
            vo.wait_until("up two levels")
            hops, unders = VGroup(), VGroup()
            for i, name in enumerate(("cheese-app-v0/", "AC215/")):
                tgt, dots, u, anims = hop(sp, name, c_up[i])
                if i == 0:
                    anims.append(FadeOut(here))
                self.play(Transform(cur, tgt), *anims, run_time=0.6)
                hops.add(dots)
                unders.add(u)
            self.remove(here)
            vo.wait_until("same secrets")
            u_s = under(c_sec, KEY, stroke=3)
            self.play(Transform(cur, ring(rows[5], ROUTE, buff=0.07)), Create(u_s), run_time=0.6)
            self.play(cur.animate.set_stroke(KEY), sp.connect(), run_time=0.9)
            vo.wait_until("The lecture's slide climbs only once")
            self.play(FadeIn(slide, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("because its repos sit")
            self.play(Indicate(slide[1], color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Always count the climbs")
            self.play(each([*unders, *hops], TURN, scale=1.25, lag=0.25), run_time=1.4)

        # ========================================================== 3. make it, place it, check it
        m = AppMap.at("S04")
        strip = term(P_REPO, rows=3)
        mk = capture("04")
        tree_cap, ls_cap = capture("05"), capture("06")
        assert mk.cmd == "mkdir ../secrets" and not mk.lines, mk.cmd
        dl = VGroup(folder_glyph(0.5, LAPTOP), label("Downloads", 24, LAPTOP)).arrange(DOWN, buff=0.15)
        dl.move_to([-4.6, 0.55, 0])
        sf = VGroup(folder_glyph(0.5, KEY), mono("secrets/", 24, KEY)).arrange(DOWN, buff=0.15)
        sf.move_to([-0.9, 0.55, 0])
        beside_repo = note("~/secrets/ · beside cheese-app-v0/").next_to(sf, DOWN, buff=0.25)
        f_icon = file_glyph(0.5, LAPTOP).next_to(dl[0], UP, buff=0.05)
        f_lab = label("the downloaded key", 22, S.GREY).next_to(f_icon, RIGHT, buff=0.3)
        landing = sf[0].get_center() + UP * 0.12
        ill = illustration_tag().move_to([5.4, -0.95, 0])

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(sp.tree, sp.caption, sp.box, sp.tube_mob, sp.host_cap, sp.cont_cap, cur, unders, u_s,
                          hops, p3, bar11, slide)
            self.play(FadeOut(gone), track(tr, 3, extra=True), run_time=0.6)
            self.remove(gone)
            self.play(FadeIn(m, scale=1.1), FadeIn(strip, shift=UP * 0.2), run_time=0.8)
            ln = type_cmd(self, strip, mk.cmd, type_time=0.8)
            xt = beside(extra_row(), ln)
            pin(self, ln, xt)
            bar_note = on_bar(strip, row_tag("the README shows a tree, not a command"))
            self.play(FadeIn(bar_note, shift=LEFT * 0.1), run_time=0.4)
            bare_prompt(self, strip)
            self.play(FadeIn(m.drawer, scale=0.6), run_time=0.6)
            self.play(Indicate(m.drawer.text, color=KEY, scale_factor=1.25), run_time=0.7)
            vo.wait_until("then move the download in")
            self.play(FadeOut(m), FadeOut(m.drawer), FadeOut(bar_note), track(tr, 3), run_time=0.5)
            self.remove(m, m.drawer, bar_note)
            self.play(FadeIn(dl), FadeIn(sf), FadeIn(beside_repo), FadeIn(ill), FadeIn(f_icon, shift=UP * 0.2),
                      FadeIn(f_lab), run_time=0.6)
            path = ArcBetweenPoints(f_icon.get_center(), landing, angle=-0.7)
            self.play(MoveAlongPath(f_icon, path), f_lab.animate.next_to(sf[0], RIGHT, buff=0.45), run_time=1.1)
            vo.wait_until("and rename it")
            new_name = mono("llm-service-account.json", 24, KEY).next_to(sf[0], RIGHT, buff=0.45)
            self.play(FadeTransform(f_lab, new_name), f_icon.animate.set_color(KEY), run_time=0.8)
            vo.wait_until("Check that name")
            nr = ring(new_name, TURN, buff=0.1)
            self.play(Create(nr), run_time=0.5)
            vo.wait_until("hidden extensions")
            bad = mono("llm-service-account.json.json", 24, ERR).next_to(new_name, UP, buff=0.55)
            bad.align_to(new_name, LEFT)
            bad_x = strike(bad)
            hid = note("hidden extensions").next_to(bad, UP, buff=0.12).align_to(bad, LEFT)
            self.play(FadeIn(bad, shift=DOWN * 0.15), FadeIn(hid), run_time=0.5)
            self.play(Create(bad_x), run_time=0.4)
            vo.wait_until("An extra tree view")
            pic = VGroup(dl, sf, beside_repo, ill, f_icon, new_name, nr, bad, bad_x, hid)
            unpin(self, ln, xt, FadeOut(pic), track(tr, 4, extra=True), run_time=0.5)
            self.remove(pic)
            resize(self, strip, 11)
            ln_cd = type_cmd(self, strip, "cd ..", type_time=0.4)
            cd_prompt(self, strip, P_LAPTOP_HOME)
            ln_tree = type_cmd(self, strip, tree_cap.cmd, type_time=0.6)
            xt2 = beside(extra_row(), ln_tree)
            pin(self, ln_tree, xt2)
            t_rows = out(self, strip, tree_cap.at((2, 11)))
            tc = tree_card()
            tc.move_to([strip.box.get_right()[0] - 0.15 - tc.width / 2, 0.0, 0])
            tc.align_to(t_rows[1].strut, UP).shift(UP * 0.2)
            self.play(FadeIn(tc, shift=LEFT * 0.2), run_time=0.5)
            self.play(t_rows[2].animate.fade(0.65), run_time=0.4)          # README.md: not in the README's tree
            vo.wait_until("Pause and match it")
            links = VGroup()
            for ri, ci in ((1, 0), (3, 2), (4, 3), (5, 1), (6, 4), (7, 5)):
                a = t_rows[ri].glyphs.get_right() + RIGHT * 0.12
                b = tc.rows[ci].get_left() + LEFT * 0.1
                lk = Line(a, b, color=TURN, stroke_width=2.5)
                links.add(lk)
                self.play(Create(lk), Indicate(t_rows[ri].glyphs, color=TURN, scale_factor=1.06),
                          Indicate(tc.rows[ci], color=TURN, scale_factor=1.06), run_time=0.4)
            chk = grey_chip("no tree? ls -la secrets (next line) checks the same thing")
            chk.move_to([strip.box.get_left()[0] + chk.width / 2, 2.3, 0])
            self.play(FadeIn(chk, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeOut(VGroup(tc, links)), run_time=0.4)
            self.remove(tc, links)
            ln_ls = type_cmd(self, strip, ls_cap.cmd, type_time=0.4)
            xt3 = beside(extra_row(), ln_ls)
            pin(self, ln_ls, xt3)
            out(self, strip, ls_cap.at((2, 5)), wrap=True)
            name_row = strip.find("llm-service-account.json")
            assert name_row.text.strip() == "llm-service-account.json", name_row.text
            nring = ring(substring(name_row, "llm-service-account.json"), KEY, buff=0.07)
            self.play(Create(nring), run_time=0.5)
            chk2 = grey_chip("not .json.json · llm-finetuning README.md:67")
            chk2.move_to(chk, aligned_edge=LEFT)
            yt = your_turn().next_to(chk2, RIGHT, buff=0.4)
            self.play(FadeOut(chk), FadeIn(chk2), FadeIn(yt, shift=LEFT * 0.1), run_time=0.5)
            self.remove(chk)
            flash_tag(self, yt, TURN)

        # ========================================================== 4. the quiet trap: .gitignore
        gi = code("cheese-app-v0/.gitignore", 1, 7).move_to([0, 0.55, 0])
        bars = VGroup(line_bar(gi.code, 5, S.GREY, 0.3), line_bar(gi.code, 6, S.GREY, 0.3))
        l7 = gi.code.code_lines[6]
        slot = ring(Rectangle(width=max(l7.width, 2.6), height=l7.height + 0.1), ERR, buff=0.06, dashed=True)
        slot.move_to(l7, aligned_edge=LEFT).shift(DOWN * 0.95)
        no_rule = label("no rule for secrets/", 24, ERR).next_to(slot, RIGHT, buff=0.35)

        with self.voiceover(SAY[4]) as vo:
            clear_but(self, tr, ref, anims=[track(tr, 4)])
            self.play(FadeIn(gi, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("the repo's gitignore")
            self.play(FadeIn(bars), run_time=0.5)
            vo.wait_until("has no rule for secrets")
            self.play(Create(slot), FadeIn(no_rule, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("Nothing protects a key")
            self.play(Indicate(no_rule, color=ERR, scale_factor=1.1),
                      slot.animate(rate_func=there_and_back).set_stroke(width=5), run_time=0.9)

        # ========================================================== 5. ponder 1: the key inside the repo
        sk = SecretsPortalRig(key_inside=True)
        krows = sk.tree.rows
        sk.caption.next_to(krows[0], RIGHT, buff=0.9)
        bad_ring = ring(VGroup(krows[5], krows[6]), ERR, buff=0.08)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(gi, bars, slot, no_rule)), run_time=0.5)
            self.remove(gi, bars, slot, no_rule)
            self.play(FadeIn(sk.tree), FadeIn(sk.caption), run_time=0.8)
            vo.wait_until("Suppose you save the key inside the repo")
            self.play(Create(bad_ring), run_time=0.6)
            vo.wait_until("in cheese-app-v0 slash secrets")
            self.play(each([krows[5].name_text, krows[6].name_text], ERR, scale=1.08, lag=0.3), run_time=0.8)
            vo.wait_until("and run the API script from api-service")
            self.play(Indicate(krows[3].name_text, color=ROUTE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("What is in slash secrets")
            self.play(Indicate(krows[0].name_text, color=TURN, scale_factor=1.1), run_time=0.7)
        pc = ponder_right(self, PONDER_1, 8, 7.0, [3.05, 0.25, 0])

        # ========================================================== 6. replay: an empty folder, an error
        a, b = capture("33").line(162).split(": ", 1)
        err = VGroup(mono(a + ":", 20, ERR), mono(b, 20, ERR)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        err.move_to([6.3 - err.width / 2, -2.55, 0])
        src = note("laptop/33 · line 162 · the API's own run").next_to(err, DOWN, buff=0.15).align_to(err, LEFT)
        empty = note("empty").next_to(sk.box.mount, RIGHT, buff=0.3)
        hole = ring(sk.box.file, ERR, buff=0.08, dashed=True)
        protect = err_chip("inside a git tree · no rule protects it", mono_font=False)
        protect.next_to(krows[6], RIGHT, buff=0.3)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(pc), FadeIn(sk.box), run_time=0.6)
            self.remove(pc)
            cur2 = sk.climb(self)
            vo.wait_until("Docker does not complain")
            sk.pop_empty(self)
            vo.wait_until("So slash secrets is empty")
            self.play(sk.connect(), run_time=0.8)
            self.play(FadeIn(empty, shift=LEFT * 0.1), Indicate(sk.box.mount[1], color=KEY, scale_factor=1.15),
                      run_time=0.6)
            vo.wait_until("and the first embedding call fails")
            lab2 = sk.env_label()
            ptr2 = Arrow(lab2[1].get_right() + RIGHT * 0.05, hole.get_right() + RIGHT * 0.05, buff=0.05,
                         color=ROUTE, stroke_width=3, tip_length=0.16, path_arc=1.2,
                         max_tip_length_to_length_ratio=0.3)
            self.play(FadeIn(lab2, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Create(ptr2), Create(hole), run_time=0.6)
            vo.wait_until("with a default credentials error")
            self.play(FadeIn(err, shift=UP * 0.15), Indicate(sk.box.lib.text, color=ERR, scale_factor=1.15),
                      run_time=0.7)
            self.play(FadeIn(src), run_time=0.4)
            vo.wait_until("Meanwhile your key sits")
            side = VGroup(sk.box, sk.tube_mob, lab2, ptr2, hole, empty, cur2, sk.ghost_chip)
            self.play(FadeOut(side), run_time=0.6)
            self.remove(side)
            self.play(FadeIn(protect, shift=LEFT * 0.15), bad_ring.animate.set_stroke(width=5), run_time=0.6)
            vo.wait_until("nothing protects")
            self.play(each([krows[6].name_text, protect.text], ERR, scale=1.1, lag=0.3), run_time=0.9)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)

