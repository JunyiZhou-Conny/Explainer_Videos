"""S07 · Three images, one timestamp — tracker B 4 → 5 (README › Deployment Steps, README 79–89).
No lecture tag (script.md has no LECTURE mark in S07). V6 TimestampTrail (build half), V4 PlayCard.

Beats (script.md "## S07"; one voiceover block each):
0. TRACKER B 4. README(81–85) card (20 pt: line 81's URL is one word): the URL row flashes on
   "in U S East 1", the three names on "create three empty private repositories"; on "the vector D B tool" it shrinks (Transform)
   into a GREY chip "README.md · lines 81–85" (top left) and the console drawing "ECR › Private registry › Repositories" (illustration) slides in on the right
   with three BLUE rows `<name> · Private` (README order), lit one per name; ▶ your turn on its
   bottom edge. On "Your policy can push" S03's RED dashed chip "no ecr:CreateRepository" returns
   under the README chip.
1. TRACKER B 5. CODE(deploy-docker-images.yml: 2–13) (22 pt, lines trimmed at 64): line 2 YELLOW
   bar, line 9 (the ECR login) PURPLE, line 12 GREEN, then V6's GREEN tag card YYYYmmddHHMMSS is
   stamped out of line 12's `date` and hangs right of line 13 `register: tag` (GREEN).
2. TRACKER B 5. The panel becomes CODE(18–24) (20 pt; `{{ ecr_registry }}` elided as `…`, see
   below): line 21 `path: /frontend-react` PINK + PINK chip "mounted in S06"; the card drops under
   the panel and a PINK thread runs from it to `tag.stdout` on line 23. The panel becomes
   CODE(25–30): line 29 `push: yes` bar. The panel leaves; V6 build layout fades in around the
   card (stamp chip, three TEAL images, BLUE ECR box with three shelves, the registry line); the tag
   clips onto each image and each flies to its shelf (frontend first). The registry line leaves;
   CODE(57–58) (20 pt) under the .docker-tag file: line 58 GREEN bar; the committed tag is struck
   GREY and the card's copy drops in GREEN as <your tag>.
3. TRACKER B 5. The picture leaves; a 12-row toolbox terminal (prompt from laptop/40: 35) types
   `ansible-playbook deploy-docker-images.yml -i inventory.yml` (README 89; folds onto 2 rows);
   ▶ your turn beside it.
4. TBX(laptop/40: 43, 45, 46 msg): PLAY line, TASK line, the fatal head and the two stderr lines,
   RED (wrapped); each flashes on its phrase; line 49 as V4's PlayRecap (failed=1 RED), flashed on
   "The recap says".
5. TRACKER B 5 · extra. The toolbox terminal slides out; a 6-row laptop terminal at P_LAPTOP slides
   in with the GREY chip "second laptop terminal · …" above it; `docker images` (extra, tag on the
   title bar) → laptop/41: 2–4 (columns squeezed); the two image rows flash (toolbox TEAL, base
   ORANGE).
6. TRACKER B 5. No terminal. V4 PlayCard (deploy-docker-images.yml, 11 tasks from laptop/37,
   hosts: localhost) on the left, tiles light GREEN one by one; GREY caption "what success looks
   like · schematic" under it. Right column: the .docker-tag file, the committed 20241121211313
   struck GREY ("the author's last deploy"), GREEN <your tag> under it; a GREEN failed=0 chip.
7. TRACKER B 5 · extra. The picture leaves; a 9-row laptop terminal types `docker system prune -a`
   (extra) → laptop/67: 2–8 (line 8 printed without its [exit 0]: docker printed no newline);
   "[y/N]" ringed, GREY row tag "no answer · nothing removed". The terminal shrinks to a 3-row strip
   (lines 2 and 8); above it a BLUE ECR box with three shelves holds the first set of images, a
   second set slides in, GOLD cost tag "ECR storage · every tag you push" and a GREY note "nothing
   deletes old tags". Fade; empty frame.

Deviations from SHOW: lines 23, 27 and 28 of deploy-docker-images.yml are 76-84 characters and
cannot fit a 12.6-wide panel at 20 pt without cutting off `{{ tag.stdout}}`, the part the beat is
about, so the panels of 18–24 and 25–30 show `{{ ecr_registry }}` elided as `…` (asserted against
the file; the registry itself is spelled out in V6's registry line). CODE(2–13) trims its long
lines (5, 6, 9) at 64 characters. The README card folds into a chip before the console comes in (as
S03 does): card and console cannot share the frame at 20 pt. The PINK thread runs from the tag card
(which carries `register: tag`) to `tag.stdout`, because line 13 is no longer on screen after the
Transform. Block 6's recap row is a single `failed=0` chip, not the five counters: no successful
run was captured, so no other count is shown. Block 7's ECR shelf is drawn locally (V6's build
layout is 4.9 tall and cannot stand over a 3-row strip).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S07"]

DI = "src/deployment/deploy-docker-images.yml"
X40 = toolbox_capture("40")
C41, C67 = capture("41"), capture("67")
CMD = "ansible-playbook deploy-docker-images.yml -i inventory.yml"
ECR_L = "{{ ecr_registry }}"

# ------------------------------------------------------------------ the real sources (checked)
assert readme(89) == CMD and X40.cmd == CMD, X40.cmd
assert [readme(n) for n in (83, 84, 85)] == [f"- {n}" for n in ECR_REPOS]
assert excerpt(DI, 2, 2).strip() == "hosts: localhost"
assert excerpt(DI, 9, 9).strip().startswith('shell: "aws ecr get-login-password')
assert excerpt(DI, 12, 12).strip() == 'shell: "(date +%Y%m%d%H%M%S)"'
assert excerpt(DI, 13, 13).strip() == "register: tag"
assert excerpt(DI, 21, 21).strip() == "path: /frontend-react"
assert excerpt(DI, 23, 23).strip() == 'name: "{{ ecr_registry }}/cheese-app-frontend-react:{{ tag.stdout}}"'
assert excerpt(DI, 29, 29).strip() == "push: yes"
assert excerpt(DI, 58, 58).strip() == "shell: echo {{ tag.stdout}} > .docker-tag"
assert excerpt(DI, 60, 60).strip() == "shell: docker system prune -a"
assert X40.at(43) == ["PLAY [Build docker images and push them to ECR]"]
assert X40.at(45) == ["TASK [Login to AWS ECR]"]
MSG = X40.msg(46)
assert MSG[0] == "fatal: [localhost]: FAILED! =>" and "UnrecognizedClientException" in MSG[1], MSG
assert MSG[2] == "Error: Cannot perform an interactive login from a non TTY device"
assert X40.recap()[1]["failed"] == 1
assert C41.cmd == "docker images" and C41.line(3).startswith("cheese-app-deployment:latest")
assert C41.line(4).startswith("ubuntu:20.04")
assert C67.cmd == "docker system prune -a"
_raw67 = C67.path.read_text().rstrip("\n").split("\n")
assert _raw67[7] == "Are you sure you want to continue? [y/N] [exit 0]", _raw67[7]   # no newline after the question
assert C67.line(8).rstrip() == "Are you sure you want to continue? [y/N]"
TASKS = task_names("deploy-docker-images.yml")
assert len(TASKS) == 11 and TASKS[-1] == "Remove all unused containers"


# ------------------------------------------------------------------ helpers of this scene
def elided(a: int, b: int, font_size: float = 20):
    """CODE(deploy-docker-images.yml: a–b) with every '{{ ecr_registry }}' shown as '…' (the lines
    are 76-84 characters; trimming the end would cut '{{ tag.stdout}}'). Header 'path · lines a–b'."""
    src = excerpt(DI, a, b)
    assert ECR_L in src
    src = src.replace(ECR_L, "…")
    guard(src)
    p = code_panel(src, DI, a, "yaml", font_size=font_size)
    assert p.width <= 12.6, p.width
    return p


def at_top_left(m, left: float = -6.5, top: float = 2.75):
    return m.move_to([left + m.width / 2, top - m.height / 2, 0])


def at_top_right(m, right: float = 6.5, top: float = 2.75):
    return m.move_to([right - m.width / 2, top - m.height / 2, 0])


def edge_tag(frame, tg, dx: float = 0.25):
    """A tag sitting on a frame's bottom edge, right end."""
    return tg.move_to([frame.get_right()[0] - dx - tg.width / 2, frame.get_bottom()[1], 0])


def drop_all(scene, *mobs, run_time: float = 0.4, shift=ORIGIN):
    scene.play(*[FadeOut(m, shift=shift) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


def find_row(rows, sub):
    hits = [r for r in rows if sub in r.text]
    assert hits, (sub, [r.text for r in rows])
    return hits[0]


def ecr_shelf():
    """The BLUE ECR box of block 7: label, three named shelves (README order of IMAGES), one TEAL
    cube per shelf (the first push). .frame .shelves .cubes"""
    fr = box(7.0, 3.3, CLOUD, fill_opacity=0.06)
    t = label("ECR · private repositories", 20, CLOUD).move_to(fr.get_top() + DOWN * 0.3)
    shelves, cubes = VGroup(), VGroup()
    for n in IMAGES:
        bd = Line(LEFT * 3.2, RIGHT * 3.2, color=CLOUD, stroke_width=3)
        nm = mono(n, 20, S.GREY).next_to(bd, UP, buff=0.12).align_to(bd, LEFT).shift(RIGHT * 0.15)
        shelves.add(VGroup(bd, nm))
    shelves.arrange(DOWN, buff=0.42).next_to(t, DOWN, buff=0.4)
    for sh in shelves:
        c = cube_glyph(0.36).next_to(sh[0], UP, buff=0.04)
        c.next_to(sh[1], RIGHT, buff=0.35).align_to(sh[0], DOWN).shift(UP * 0.04)
        cubes.add(c)
    g = VGroup(fr, t, shelves, cubes)
    g.frame, g.shelves, g.cubes = fr, shelves, cubes
    return g


class BuildAndPush(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 8, len(SAY)

        # ========================================================== 0. three empty repositories
        tr = tracker_b(4)
        rp = at_top_left(readme_panel(81, 85, size=20))
        rchip = at_top_left(grey_chip("README.md · lines 81–85"), top=2.55)
        con = console_drawing("ECR › Private registry › Repositories",
                              [("chip", f"{n} · Private", CLOUD) for n in ECR_REPOS])
        at_top_right(con, top=2.55)
        turn0 = edge_tag(con.frame, your_turn())
        nocreate = dashed_chip("no ecr:CreateRepository", color=ERR)
        nocreate.next_to(rchip, DOWN, buff=0.45).align_to(rchip, LEFT)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(rp, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("in U S East 1")
            self.play(Indicate(rp.rows[81], color=CLOUD, scale_factor=1.03), run_time=0.8)
            vo.wait_until("create three empty private repositories")
            self.play(each([rp.rows[n] for n in (83, 84, 85)], TURN, scale=1.05, lag=0.25), run_time=1.2)
            # the card shrinks into its chip (what became what), then the console comes in
            vo.wait_until("the vector D B tool")
            self.play(ReplacementTransform(rp, rchip), run_time=0.5)
            self.play(FadeIn(con, shift=LEFT * 0.2), run_time=0.4)
            self.play(Indicate(con.rows[0].text, color=CLOUD, scale_factor=1.06), run_time=0.4)
            vo.wait_until("the API service")
            self.play(Indicate(con.rows[1].text, color=CLOUD, scale_factor=1.06), run_time=0.5)
            vo.wait_until("and the frontend")
            self.play(Indicate(con.rows[2].text, color=CLOUD, scale_factor=1.06), FadeIn(turn0, shift=UP * 0.1),
                      run_time=0.6)
            vo.wait_until("Your policy can push")
            self.play(FadeIn(nocreate, shift=RIGHT * 0.3), run_time=0.6)
            vo.wait_until("but not create them")
            self.play(Indicate(nocreate.text, color=ERR, scale_factor=1.06), run_time=0.7)

        # ========================================================== 1. the playbook: localhost, login, tag
        p1 = code(DI, 2, 13, trim=64)
        p1.move_to([0, 2.75 - p1.height / 2, 0])
        b2 = line_bar(p1.code, 0, TURN, 0.25)
        b9 = line_bar(p1.code, 9 - 2, TOOL, 0.3)
        b12 = line_bar(p1.code, 12 - 2, OWN, 0.25)
        b13 = line_bar(p1.code, 13 - 2, OWN, 0.25)
        card = tag_card()
        reg13 = code_span(p1.code, 13 - 2, "register: tag")
        card.move_to([p1.code.code_lines[12 - 2].get_right()[0] + 0.5 + card.width / 2, reg13.get_y(), 0])
        # hang it from line 13: its top just under line 12's GREEN bar (it touched the bar)
        card.shift(DOWN * max(0.0, card.get_top()[1] - (b12.get_bottom()[1] - 0.03)))
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(con), FadeOut(rchip), FadeOut(nocreate), FadeOut(turn0), track(tr, 5), run_time=0.6)
            self.remove(con, rchip, nocreate, turn0)
            self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("runs on localhost")
            self.play(FadeIn(b2), Indicate(code_span(p1.code, 0, "localhost"), color=TURN, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("Task 1 logs Docker in")
            self.play(FadeOut(b2), FadeIn(b9), run_time=0.5)
            self.play(Indicate(code_span(p1.code, 9 - 2, "aws ecr get-login-password"), color=TOOL,
                               scale_factor=1.05), run_time=0.8)
            vo.wait_until("Task 2 stamps a tag")
            self.play(FadeOut(b9), FadeIn(b12), run_time=0.5)
            span12 = code_span(p1.code, 12 - 2, "date +%Y%m%d%H%M%S")
            self.play(Indicate(span12, color=OWN, scale_factor=1.08), run_time=0.6)
            self.play(TransformFromCopy(span12, card), run_time=0.9)
            vo.wait_until("and registers it")
            self.play(FadeIn(b13), *[g.animate.set_color(OWN) for g in reg13], run_time=0.5)
            vo.wait_until("so later tasks")
            self.play(Indicate(card, color=OWN, scale_factor=1.06), run_time=0.7)

        # ========================================================== 2. build, push x3, save the tag
        p2 = elided(18, 24)
        p2.move_to([0, 2.75 - p2.height / 2, 0])
        b21 = line_bar(p2.code, 21 - 18, ROUTE, 0.25)
        path21 = code_span(p2.code, 21 - 18, "path: /frontend-react")
        sock = route_chip("mounted in S06", mono_font=False).next_to(path21, RIGHT, buff=0.6)
        tstd = code_span(p2.code, 23 - 18, "tag.stdout")
        card_y = p2.get_bottom()[1] - 0.6
        p3 = elided(25, 30)
        p3.move_to([0, 2.75 - p3.height / 2, 0])
        b29 = line_bar(p3.code, 29 - 25, OWN, 0.25)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(b12, b13)), run_time=0.3)
            self.remove(b12, b13)
            self.play(ReplacementTransform(p1, p2), card.animate.move_to([3.0, card_y, 0]), run_time=0.9)
            vo.wait_until("from slash frontend react")
            self.play(FadeIn(b21), *[g.animate.set_color(ROUTE) for g in path21], run_time=0.5)
            vo.wait_until("the folder the script mounted")
            self.play(FadeIn(sock, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("names the image with that tag")
            thread = route(card.get_top(), tstd.get_bottom() + DOWN * 0.05, arc=0.3, stroke=3)
            self.play(Create(thread), *[g.animate.set_color(OWN) for g in tstd], run_time=0.7)
            vo.wait_until("and pushes it")
            self.play(FadeOut(thread), FadeOut(sock), FadeOut(b21), run_time=0.3)
            self.remove(thread, sock, b21)
            self.play(ReplacementTransform(p2, p3), run_time=0.7)
            self.play(FadeIn(b29), Indicate(code_span(p3.code, 29 - 25, "push: yes"), color=OWN, scale_factor=1.1),
                      run_time=0.7)
            # V6: the picture comes in around the card
            trail = TimestampTrail()
            # the first pushed chip touched the box's label: give it a little air (inside the box)
            trail.ecr.text.shift(UP * 0.08)
            trail.shelves.shift(DOWN * 0.05)
            tgt = tag_card().next_to(trail.stamp_chip, DOWN, buff=0.35)
            others = VGroup(*[m for m in trail.submobjects])
            self.play(FadeOut(p3), FadeOut(b29), run_time=0.4)
            self.remove(p3, b29)
            self.play(FadeIn(others), card.animate.move_to(tgt), run_time=0.7)
            self.remove(others)
            trail.card = card
            self.remove(card)
            trail.keep(self, card)
            trail.clip(self, 0, 0.4)
            trail.push(self, 0, 0.6)
            vo.wait_until("The API and the vector D B tool follow")
            for i in (1, 2):
                trail.clip(self, i, 0.35)
                trail.push(self, i, 0.55)
            vo.wait_until("Last, it saves the tag")
            trail.drop(self, trail.registry, run_time=0.3)
            p58 = code(DI, 57, 58, font_size=20)
            p58.move_to([6.5 - p58.width / 2, -3.55 + p58.height / 2, 0])
            assert p58.get_top()[1] < trail.ecr.frame.get_bottom()[1] - 0.1
            b58 = line_bar(p58.code, 1, OWN, 0.25)
            self.play(FadeIn(p58, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(b58), run_time=0.3)
            vo.wait_until("in a file")
            trail.save(self)
            vo.wait_until("dot docker tag")
            self.play(Indicate(trail.file[1], color=OWN, scale_factor=1.1), run_time=0.6)

        # ========================================================== 3. step 5: run it
        t = toolbox_term("40", rows=12)
        with self.voiceover(SAY[3]) as vo:
            drop_all(self, trail, p58, b58, run_time=0.5)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            cmd = type_cmd(self, t, CMD, type_time=2.2)
            assert " ".join(r.text.rstrip(" \\").strip() for r in cmd.rows).endswith(CMD), [r.text for r in cmd.rows]
            vo.wait_until("Pause and run it")
            turn3 = beside(turn_row(), cmd)
            pin(self, cmd, turn3)
            flash_tag(self, turn3)

        # ========================================================== 4. the first real error
        with self.voiceover(SAY[4]) as vo:
            o1 = out(self, t, [X40.at(43)[0], X40.at(45)[0]], run_time=0.5)
            fatal = out(self, t, [(s, ERR) for s in MSG], wrap=True, run_time=0.8)
            vo.wait_until("at the E C R login")
            self.play(Indicate(o1[1], color=TOOL, scale_factor=1.04), run_time=0.6)
            vo.wait_until("the security token is invalid")
            tok = VGroup(find_row(fatal, "The security"), find_row(fatal, "token included"))
            self.play(Indicate(tok, color=ERR, scale_factor=1.04), run_time=0.8)
            vo.wait_until("The second line follows")
            tty = find_row(fatal, "non TTY device")
            self.play(Indicate(tty, color=ERR, scale_factor=1.04), run_time=0.8)
            vo.wait_until("docker login received an empty password")
            self.play(Circumscribe(tty, color=ERR, buff=0.05), run_time=0.9)
            vo.wait_until("The recap says")
            rc = play_recap("40")
            y = t._slot(len(t.lines))[1] - 0.3
            rc.move_to([t.box.get_center()[0], y - rc.height / 2 + 0.1, 0])
            assert rc.get_bottom()[1] > t.box.get_bottom()[1] + 0.05
            self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.5)
            self.play(rc.flash("failed"), run_time=0.9)

        # ========================================================== 5. extra: no image was built
        lt = laptop_term(6)
        side = grey_chip("second laptop terminal · the toolbox stays open · /app is this folder, edits show up inside at once")
        side.next_to(lt.box, UP, buff=0.2)
        with self.voiceover(SAY[5]) as vo:
            self.remove(*turn3.get_family())
            self.play(FadeOut(t, shift=LEFT * 0.6), FadeOut(rc, shift=LEFT * 0.6), track(tr, 5, True), run_time=0.5)
            self.remove(t, rc)
            self.play(FadeIn(lt, shift=LEFT * 0.4), FadeIn(side, shift=DOWN * 0.1), run_time=0.5)
            type_cmd(self, lt, C41.cmd, type_time=0.4)
            ex5 = on_bar(lt, extra_row())
            self.play(FadeIn(ex5), run_time=0.3)
            imgs = out(self, lt, [squeeze_spaces(s.rstrip()) for s in C41.at(2, 3, 4)], run_time=0.5)
            vo.wait_until("The laptop still holds")
            self.play(*[g.animate.set_color(IMAGE) for g in substring(imgs[1], "cheese-app-deployment:latest")],
                      run_time=0.4)
            vo.wait_until("and its base")
            self.play(*[g.animate.set_color(SHARED) for g in substring(imgs[2], "ubuntu:20.04")], run_time=0.4)

        # ========================================================== 6. what success looks like
        pc = PlayCard(PLAYBOOKS[0], X40.at(43)[0][6:-1], "localhost", TASKS, cols=2)
        at_top_left(pc, top=2.7)
        cap6 = note("what success looks like · schematic").next_to(pc, DOWN, buff=0.2).align_to(pc, LEFT)
        col_x = pc.get_right()[0] + 0.35
        f_row = VGroup(file_glyph(0.42, OWN), mono(".docker-tag", 20, OWN)).arrange(RIGHT, buff=0.15)
        f_row.move_to([col_x + f_row.width / 2, 1.9, 0])
        old = mono(TAG_COMMITTED, 20, INK).next_to(f_row, DOWN, buff=0.3).align_to(f_row, LEFT)
        who = VGroup(note("the author's"), note("last deploy")).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        who.next_to(old, DOWN, buff=0.15).align_to(old, LEFT)
        new = mono("<your tag>", 20, OWN).next_to(who, DOWN, buff=0.35).align_to(old, LEFT)
        ok0 = chip("failed=0", OWN, size=20, font=MONO)
        ok0.move_to([col_x + ok0.width / 2, pc.get_bottom()[1] + ok0.height / 2, 0])
        assert ok0.get_right()[0] < 6.6 and old.get_right()[0] < 6.6, (ok0.get_right(), old.get_right())
        with self.voiceover(SAY[6]) as vo:
            drop_all(self, lt, side, ex5, run_time=0.4)
            self.play(FadeIn(pc, shift=UP * 0.15), FadeIn(cap6), track(tr, 5), run_time=0.6)
            self.play(LaggedStart(*[pc.set_state(i, "ok") for i in range(len(TASKS))], lag_ratio=0.35),
                      run_time=4.0)
            vo.wait_until("three images built on your laptop")
            self.play(each([pc.tiles[i].text for i in (3, 5, 7)], IMAGE, lag=0.25), run_time=1.0)
            vo.wait_until("and pushed")
            self.play(each([pc.tiles[i].text for i in (4, 6, 8)], CLOUD, lag=0.25), run_time=1.0)
            vo.wait_until("and your tag written")
            self.play(FadeIn(f_row), FadeIn(old), Indicate(pc.tiles[9].text, color=OWN), run_time=0.5)
            s_old = strike(old, S.GREY)
            self.play(Create(s_old), old.animate.set_color(S.GREY), FadeIn(who), run_time=0.5)
            self.play(TransformFromCopy(pc.tiles[9].text, new), run_time=0.7)
            vo.wait_until("Look for failed, zero")
            self.play(FadeIn(ok0, shift=UP * 0.1), run_time=0.4)
            self.play(Circumscribe(ok0, color=OWN, buff=0.06), Indicate(ok0.text, color=OWN), run_time=0.9)

        # ========================================================== 7. the prune that removes nothing
        t7 = laptop_term(9)
        shelf = ecr_shelf()
        shelf.move_to([-6.5 + shelf.width / 2, (PIC_TOP - 0.05 + STRIP_TOP + 0.15) / 2, 0])
        cubes2 = VGroup(*[cube_glyph(0.36).next_to(c, RIGHT, buff=0.25) for c in shelf.cubes])
        cost = cost_tag("ECR storage · every tag you push")
        cost.next_to(shelf.frame, RIGHT, buff=0.3).align_to(shelf.frame, UP).shift(DOWN * 0.6)
        nodel = note("nothing deletes old tags").next_to(cost, DOWN, buff=0.3).align_to(cost, LEFT)
        assert cost.get_right()[0] < 6.6, cost.get_right()
        with self.voiceover(SAY[7]) as vo:
            drop_all(self, pc, cap6, f_row, old, s_old, who, new, ok0, run_time=0.5)
            self.play(FadeIn(t7, shift=UP * 0.2), track(tr, 5, True), run_time=0.5)
            type_cmd(self, t7, C67.cmd, type_time=0.5)
            ex7 = on_bar(t7, extra_row())
            self.play(FadeIn(ex7), run_time=0.3)
            pr = out(self, t7, [s.rstrip() for s in C67.at((2, 8))], run_time=0.8)
            q = pr[-1]
            assert q.text.endswith("[y/N]")
            vo.wait_until("Without dash f, it asks")
            rq = ring(substring(q, "[y/N]"), TURN, buff=0.06)
            self.play(Create(rq), run_time=0.5)
            attach(self, q, rq)
            vo.wait_until("gets no answer")
            na = beside(row_tag("no answer · nothing removed"), q, buff=0.4)
            pin(self, q, na)
            vo.wait_until("Every push stores")
            self.play(FadeOut(ex7), run_time=0.2)
            self.remove(ex7)
            resize(self, t7, 3, keep=[pr[0], q], run_time=0.7)
            self.play(FadeIn(shelf, shift=DOWN * 0.15), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.4) for c in cubes2], lag_ratio=0.3),
                      FadeIn(cost, shift=LEFT * 0.15), run_time=1.0)
            vo.wait_until("and nothing deletes old tags")
            self.play(FadeIn(nodel, shift=UP * 0.1), Indicate(shelf.cubes, color=COST, scale_factor=1.1),
                      run_time=0.8)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.remove(*self.mobjects)
        self.wait(0.3)
