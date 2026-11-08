"""S09 · Five containers on one network — tracker B 9 (done) → 10 · extra → 10 → 11 · extra
(README 105–132). No lecture tag (script.md has no LECTURE mark in S09). V7 VmLayout, V3's badge.

Beats (script.md "## S09"; one voiceover block each):
0. TRACKER B 9 with a GREEN ✓ and a GREY chip "done before step 8". README(107–111) card (20 pt),
   under it a 3-row laptop strip with laptop/45 line 3 (GREY, cut after the path) and line 6
   (GREEN, wrapped). The card shrinks into the tracker caption; the strip leaves.
1. TRACKER B 10 · extra. A small server picture (BLUE frame "EC2 server": a TEAL loader and a TEAL
   vector-db with an ORANGE `latest` chip). CODE(deploy-setup-containers.yml: 148–152), line 151's
   image ORANGE, then the panel shrinks to a chip in the left column ("line 151" + ORANGE
   chromadb/chroma:latest); a 6-row laptop strip (20 pt; bar tags "second laptop terminal",
   "extra") types laptop/60 line 1 (folded) → 60: 28 (+ "at the time of recording"), 29 (from
   its "message" on, RED). The `latest` chip flips to `1.0.0`; the loader's PINK request
   /api/v1/heartbeat comes back RED `410`.
2. TRACKER B 10 · extra. The strip types laptop/61 line 1 → 61: 40, 41 (GREEN). The chip swaps to
   GREEN `0.5.18`, the request comes back GREEN `200`. The left chip becomes the erratum action
   card ("edit line 151 → chromadb/chroma:0.5.18 · before you run step 10 · as
   docker-compose.yml:25"), which then joins the "your edits" checklist as a row.
3. TRACKER B 10 · extra. The strip leaves; CODE(…: 164–166) with `-it` RED in its place; the panel
   shrinks to a left chip ("line 165" + `docker run --rm -it`); a 4-row strip types laptop/66 line
   1 → 66: 2 RED (wrapped). GREY chip "untested under Ansible"; on "drop dash I T" `-it` is struck.
4. TRACKER B 10. ▶ your turn. Toolbox terminal (prompt laptop/46: 35) types README 116 →
   TBX(46: 42 msg) RED; V4 PlayRecap from line 45 (unreachable=1 RED).
5. TRACKER B 10. GREY caption "what success looks like" (top right, kept through block 7).
   CODE(…: 36–44) alone (dest and `mode: 0600` lit), then it shrinks into a file on V7's server
   (`aws-credentials`, chip `0600`, the WHITE badge); counter "badge · copy 2 on the server · + the
   API container's environment"; a badge copy rides into a GREY dashed `env` slot where the API
   will run. Then, one per phrase: V7's PINK `appnetwork`, the disk with `persistent` and
   `chromadb`, a PINK login arrow to a BLUE `ECR` box.
6. TRACKER B 10. CODE(…: 101–104) → ReplacementTransform → CODE(…: 106–114); a fork drawing under
   it: `DOCKER_TAG` set → PINK "that tag"; empty → GREEN `.docker-tag`; GREY note "laptop run: the
   file · CI run: the extra variable wins (S14)".
7. TRACKER B 10. V7 back with the ECR box: three TEAL image cubes ride from ECR to the frontend,
   loader and api slots; TEAL `frontend :3000`; `vector-db :8000` with GREEN `0.5.18` + "your pin";
   the loader fills the vector-db's disk folder and vanishes (--rm); `api-service :9000` with GOLD
   cost_tag("Bedrock · per token"); ':3000 :8000 :9000' painted inside the wall, no hole.
8. TRACKER B 11. README(120–132) card, all six commands verbatim; "from the GCP console"
   underlined RED; erratum tag "on AWS: ssh -i <your key>.pem ubuntu@<EXTERNAL_IP> or EC2 Instance
   Connect"; ▶ your turn on the card's top edge while `sudo docker container ls` turns YELLOW; the
   other commands light in turn.
9. TRACKER B 11 · extra. Laptop terminal (20 pt, bar tag "extra · stand-in on the laptop") types
   laptop/63 line 1 → 63: 2, 3 (cut after the 80 mapping), 4, 5; the IMAGE column YELLOW; then
   laptop/64 line 1 → 64: 4, 5, 6 (address and timestamp cropped to '…'). GREY chip "nginx: after
   the next step". Fade; empty frame.

Deviations from SHOW: blocks 1–3 draw their own small server (V7 is 7.0 x 4.4 and cannot share the
frame with a strip; its text cannot be scaled below 20 pt). Block 1's panel is shown before the
strip opens, then folds into a chip. Block 1 prints line 29 from its "message" on (one row in a
6-row strip). Block 2's checklist starts with one summary row for S05's edits ("S05 · your
earlier edits", ticked) rather than all five. Block 3 replaces the strip by the panel and opens a
fresh 4-row strip after it (no room for both). Block 5's panel cannot stand next to V7 (8.7 wide);
it is shown alone, then shrinks into the file on the server. Block 6 fades V7 out (the 106–114
panel is 11.7 wide) and brings it back in block 7. Block 7 parks the three ECR images on their
containers' slots (frontend, loader, api-service); Chroma's image comes from Docker Hub, not ECR.
Block 8's ▶ your turn sits on the README card's top edge (the card's rows are ~0.34 apart, so a tag
beside `sudo docker container ls` would touch lines 120 and 123); that row turns YELLOW instead.
Block 9 uses a 20 pt terminal (11 rows) and cuts 63's nginx line after the first port mapping.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S09"]

SC = "src/deployment/deploy-setup-containers.yml"
C45, C60, C61, C66 = capture("45"), capture("60"), capture("61"), capture("66")
C63, C64 = capture("63"), capture("64")
X46 = toolbox_capture("46")
CMD10 = readme(116)
T20 = 20

# ------------------------------------------------------------------ the real sources (checked)
assert X46.cmd == CMD10 == "ansible-playbook deploy-setup-containers.yml -i inventory.yml"
assert excerpt(SC, 151, 151).strip() == 'image: "chromadb/chroma:latest"'
assert excerpt(SC, 165, 165).strip() == "shell: docker run --rm -it"
assert excerpt(SC, 43, 43).strip() == 'dest: "/srv/secrets/aws-credentials"'
assert excerpt(SC, 44, 44).strip() == "mode: 0600"
assert excerpt(SC, 103, 103).strip() == "docker_tag: \"{{ lookup('env', 'DOCKER_TAG') }}\""
assert excerpt(SC, 109, 109).strip() == 'shell: "cat .docker-tag"'
assert excerpt("src/vector-db/docker-compose.yml", 25, 25).strip() == "image: chromadb/chroma:0.5.18"
assert C45.at(3)[0].startswith("    # ansible_ssh_private_key_file:") and "/root/.ssh/ac215_2024.pem" in C45.at(3)[0]
assert "/secrets/ac215_2024.pem" in C45.at(6)[0] and not C45.at(6)[0].lstrip().startswith("#")
assert C60.at(28) == ['"1.0.0"'] and C60.line(29).endswith("HTTP 410")
assert C61.at(40) == ['"0.5.18"'] and C61.line(41).endswith("HTTP 200")
assert C66.cmd == "docker run --rm -it nginx:stable true" and C66.exit == 1
assert C66.line(2).startswith("cannot attach stdin to a TTY-enabled container")
MSG46 = X46.msg(42)
assert MSG46[0] == "fatal: [EXTERNAL_IP]: UNREACHABLE! =>" and "Could not resolve hostname external_ip" in MSG46[1]
assert X46.recap()[1]["unreachable"] == 1
assert C63.line(2).split() == ["NAMES", "IMAGE", "PORTS"]
assert C64.line(4).endswith("ready for start up") and '"GET /api/newsletters' in C64.line(5)
assert readme(120).startswith("You can SSH into the server from the GCP console")

SECOND = "second laptop terminal"
L29 = from_phrase(C60.line(29), '"message"')
L63_3 = cut(C63.line(3), "80->80/tcp,")


# ------------------------------------------------------------------ helpers of this scene
def drop_all(scene, *mobs, run_time: float = 0.4, shift=ORIGIN):
    scene.play(*[FadeOut(m, shift=shift) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


def find_row(rows, sub):
    hits = [r for r in rows if sub in r.text]
    assert hits, (sub, [r.text for r in rows])
    return hits[0]


def bar_tags(t: Terminal, *tags, gap: float = 0.15) -> VGroup:
    """Row tags on the terminal's title bar, right to left from its right end (FadeIn yourself)."""
    x = t.box.get_right()[0] - 0.15
    for tg in tags:
        tg.move_to([x - tg.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])
        x -= tg.width + gap
    return VGroup(*tags)


def glyphs_of(text: Text, s: str, sub: str) -> VGroup:
    """The glyphs of `sub` inside a label Text built from string s (spaces carry no glyph)."""
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*text[a:a + n])


def left_col(m, top: float = 2.6, left: float = -6.5):
    return m.move_to([left + m.width / 2, top - m.height / 2, 0])


class SmallServer(VGroup):
    """Blocks 1–3: a small BLUE 'EC2 server' with a TEAL loader and a TEAL vector-db, a version chip
    above the vector-db and a request lane under both. Frame x -0.6 .. 6.4, y 0.0 .. 2.6."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.frame = box(7.0, 2.6, CLOUD, fill_opacity=0.05).move_to([2.9, 1.3, 0])
        self.title = label("EC2 server", 20, CLOUD)
        self.title.move_to(self.frame.get_corner(UL) + np.array([0.25 + self.title.width / 2, -0.3, 0]))
        self.loader = crate("loader", box_w=1.9, box_h=0.9, sub="--rm").move_to([0.75, 1.3, 0])
        self.vdb = crate("vector-db", box_w=1.9, box_h=0.9, sub=":8000").move_to([4.9, 1.3, 0])
        self.add(self.frame, self.title, self.loader, self.vdb)
        self.ver = None
        self.answer = None

    def version(self, scene, text: str, color=SHARED, run_time: float = 0.5):
        c = chip(text, color, size=20, font=MONO).move_to([self.vdb.get_x(), 2.27, 0])
        if self.ver is None:
            scene.play(FadeIn(c, shift=DOWN * 0.1), run_time=run_time)
        else:
            old = self.ver
            scene.play(FadeOut(old, shift=UP * 0.15), FadeIn(c, shift=UP * 0.15), run_time=run_time)
            self.remove(old)
            scene.remove(old)
        self.add(c)
        self.ver = c
        return c

    def request(self, scene, path: str, result: str, ok: bool, run_time: float = 1.6):
        if self.answer is not None:
            scene.play(FadeOut(self.answer), run_time=0.25)
            self.remove(self.answer)
            scene.remove(self.answer)
        q = route_chip(path)
        y = 0.42
        start = [self.loader.get_right()[0] - 0.3 + q.width / 2 - 0.6, y, 0]
        end = [self.vdb.get_left()[0] + 0.3 - q.width / 2 + 0.6, y, 0]
        q.move_to(start)
        scene.play(FadeIn(q, shift=RIGHT * 0.2), run_time=run_time * 0.15)
        scene.play(q.animate.move_to(end), run_time=run_time * 0.35)
        ans = chip(result, PASS if ok else ERR, size=20, font=MONO).move_to(end)
        scene.play(ReplacementTransform(q, ans), Indicate(self.vdb.text, color=ROUTE), run_time=run_time * 0.2)
        scene.play(ans.animate.move_to([self.loader.get_x() + 0.5, y, 0]), run_time=run_time * 0.3)
        self.add(ans)
        self.answer = ans
        return ans


def code_chip(head: str, body_parts) -> VGroup:
    """A left-column chip for a folded code panel: a GREY head line and a mono line made of
    (text, colour) parts. .head .body .parts"""
    hd = label(head, 20, S.GREY)
    parts = VGroup(*[mono(s, 20, c) for s, c in body_parts]).arrange(RIGHT, buff=0.16)
    inner = VGroup(hd, parts).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    fr = box(inner.width + 0.5, inner.height + 0.36, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.head, g.body, g.parts = fr, hd, parts, parts
    return g


class SetupContainers(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S09"] == 10, len(SAY)

        # ========================================================== 0. step 9: done before step 8
        tr = tracker_b(9)
        ck9 = check_mark(0.3, OWN, stroke=4).next_to(tr.caption, RIGHT, buff=0.2)
        done = grey_chip("done before step 8").next_to(ck9, RIGHT, buff=0.2)
        rp = readme_panel(107, 111, size=20)
        rp.move_to([0, 2.7 - rp.height / 2, 0])
        st0 = term(P_LAPTOP, rows=3, size=T20)
        inv = grey_chip("inventory.yml · after the switch (S08)").next_to(st0.box, UP, buff=0.15).align_to(st0.box, LEFT)
        assert rp.get_bottom()[1] > inv.get_top()[1] + 0.1, (rp.get_bottom(), inv.get_top())
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(rp, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(st0, shift=UP * 0.15), FadeIn(inv), run_time=0.4)
            o0 = out(self, st0, [(cut(C45.at(3)[0], '.pem"'), S.GREY), (C45.at(6)[0].rstrip(), OWN)], wrap=True,
                     run_time=0.6)
            vo.wait_until("done before step 8")
            self.play(Create(ck9), FadeIn(done, shift=LEFT * 0.1), run_time=0.5)
            self.play(Indicate(VGroup(*o0[1:]), color=OWN, scale_factor=1.02), run_time=0.7)
            self.play(FadeOut(rp, target_position=tr.caption.get_center(), scale=0.2),
                      FadeOut(st0), FadeOut(inv), Indicate(tr.caption, color=TURN, scale_factor=1.05), run_time=0.8)
            self.remove(rp, st0, inv, *o0)

        # ========================================================== 1. extra: Chroma latest answers 410
        sv = SmallServer()
        p151 = code(SC, 148, 152, font_size=T20)
        p151.move_to([0, -3.45 + p151.height / 2, 0])
        c151 = code_chip("line 151 · image", [("chromadb/chroma:latest", SHARED)])
        left_col(c151, top=2.55)
        t = term(P_LAPTOP, rows=6, size=T20)
        tags1 = bar_tags(t, extra_row(), row_tag(SECOND))
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(ck9), FadeOut(done), track(tr, 10, True), run_time=0.5)
            self.play(FadeIn(sv, shift=DOWN * 0.1), run_time=0.6)
            sv.version(self, "latest")
            vo.wait_until("The playbook starts Chroma")
            self.play(FadeIn(p151, shift=UP * 0.15), run_time=0.5)
            img = code_span(p151.code, 3, "chromadb/chroma:latest")
            self.play(*[g.animate.set_color(SHARED) for g in img], Indicate(sv.ver.text, color=SHARED), run_time=0.6)
            vo.wait_until("at the time of recording")
            self.play(ReplacementTransform(p151, c151), run_time=0.7)
            self.play(FadeIn(t, shift=UP * 0.15), FadeIn(tags1), run_time=0.4)
            type_capture(self, t, C60, type_time=1.2)
            o28 = out(self, t, C60.at(28), run_time=0.3)
            pin(self, o28[0], beside(time_row(), o28[0]))
            sv.version(self, "1.0.0")
            vo.wait_until("which answers the old API")
            o29 = out(self, t, [(L29, ERR)], run_time=0.3)
            sv.request(self, "/api/v1/heartbeat", "410", ok=False)
            self.play(Indicate(substring(o29[0], "HTTP 410"), color=ERR, scale_factor=1.15), run_time=0.6)

        # ========================================================== 2. extra: 0.5.18 answers 200
        act = VGroup(label("edit line 151 → chromadb/chroma:0.5.18", 20, INK),
                     label("before you run step 10", 20, INK),
                     label("as docker-compose.yml:25", 20, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        act_fr = box(act.width + 0.5, act.height + 0.55, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        act.move_to(act_fr).shift(DOWN * 0.06)
        act_tg = erratum_tag()
        act_tg.move_to(act_fr.get_corner(UL) + np.array([0.3 + act_tg.width / 2, 0, 0]))
        action = VGroup(act_fr, act, act_tg)
        left_col(action, top=2.55)
        edits = Checklist("your edits", ["S05 · your earlier edits"], color=OWN, tag_text=None)
        left_col(edits, top=2.55)
        with self.voiceover(SAY[2]) as vo:
            type_capture(self, t, C61, type_time=1.2)
            o40 = out(self, t, [C61.at(40)[0], (C61.at(41)[0], PASS)], run_time=0.4)
            vo.wait_until("which answers 200")
            sv.version(self, "0.5.18", OWN)
            sv.request(self, "/api/v1/heartbeat", "200", ok=True)
            self.play(Indicate(substring(o40[1], "HTTP 200"), color=PASS, scale_factor=1.15), run_time=0.5)
            vo.wait_until("So change line 151")
            self.play(FadeOut(c151, shift=UP * 0.1), FadeIn(action, shift=UP * 0.1), run_time=0.6)
            self.remove(c151)
            flash_tag(self, act_tg)
            self.play(FadeOut(action), FadeIn(edits), run_time=0.5)
            self.remove(action)
            edits.tick(self, 0)
            edits.add_row(self, "line 151 → chromadb/chroma:0.5.18")

        # ========================================================== 3. extra: docker run -it without a terminal
        p165 = code(SC, 164, 166, font_size=T20)
        p165.move_to([0, -3.45 + p165.height / 2, 0])
        c165 = code_chip("line 165 · the loader", [("docker run --rm", INK), ("-it", ERR)])
        left_col(c165, top=2.55)
        unt = grey_chip("untested under Ansible").next_to(c165, DOWN, buff=0.2).align_to(c165, LEFT)
        t3 = term(P_LAPTOP, rows=4, size=T20)
        tags3 = bar_tags(t3, extra_row(), row_tag(SECOND))
        with self.voiceover(SAY[3]) as vo:
            drop_all(self, t, tags1, edits, sv.answer, run_time=0.4)
            sv.remove(sv.answer)
            sv.answer = None
            self.play(FadeIn(p165, shift=UP * 0.15), Indicate(sv.loader.text, color=IMAGE), run_time=0.6)
            self.play(*[g.animate.set_color(ERR) for g in code_span(p165.code, 1, "-it")], run_time=0.4)
            vo.wait_until("which Docker refuses")
            self.play(ReplacementTransform(p165, c165), run_time=0.6)
            self.play(FadeIn(t3, shift=UP * 0.15), FadeIn(tags3), run_time=0.4)
            type_capture(self, t3, C66, type_time=0.8)
            out(self, t3, [(C66.line(2), ERR)], wrap=True, run_time=0.4)
            vo.wait_until("We couldn't test")
            self.play(FadeIn(unt, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("if that task fails")
            st_it = strike(c165.parts[1], ERR)
            self.play(Create(st_it), c165.parts[1].animate.set_opacity(0.5), run_time=0.6)

        # ========================================================== 4. step 10: unreachable again
        t4 = toolbox_term("46", rows=8)
        with self.voiceover(SAY[4]) as vo:
            drop_all(self, sv, c165, st_it, unt, t3, tags3, run_time=0.4)
            self.play(track(tr, 10), FadeIn(t4, shift=UP * 0.2), run_time=0.5)
            cmd4 = type_cmd(self, t4, CMD10, type_time=1.4)
            turn4 = beside(turn_row(), cmd4)
            pin(self, cmd4, turn4)
            vo.wait_until("Pause and run it")
            flash_tag(self, turn4)
            vo.wait_until("Ours is unreachable")
            o4 = out(self, t4, [(s, ERR) for s in MSG46], wrap=True, run_time=0.6)
            self.play(Indicate(substring(find_row(o4, "external_ip"), "external_ip"), color=ERR, scale_factor=1.15),
                      run_time=0.6)
            rc = play_recap("46")
            y = t4._slot(len(t4.lines))[1] - 0.3
            rc.move_to([t4.box.get_center()[0], y - rc.height / 2 + 0.1, 0])
            assert rc.get_bottom()[1] > t4.box.get_bottom()[1] + 0.05
            self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.4)
            self.play(rc.flash("unreachable"), run_time=0.7)
            vo.wait_until("here is what it does")
            self.play(Indicate(t4.box, color=S.GREY, scale_factor=1.0), run_time=0.5)

        # ========================================================== 5. on a real server: keys, network, disk, ECR
        cap = note("what success looks like")
        cap.move_to([6.5 - cap.width / 2, 2.58, 0])
        p36 = code(SC, 36, 44, font_size=T20)
        p36.move_to([0, (2.3 - 3.4) / 2, 0])
        v = VmLayout()
        fname = mono("aws-credentials", 20, INK)
        fg = file_glyph(0.4, OWN)
        mode = grey_chip("0600", mono_font=True)
        badge = badge_glyph(0.42)
        frow = VGroup(fg, fname, mode).arrange(RIGHT, buff=0.15)
        frow.move_to([-2.75 + frow.width / 2, 1.2, 0])
        badge.next_to(frow, DOWN, buff=0.15).align_to(frow, LEFT).shift(RIGHT * 0.1)
        cnt = note("badge · copy 2 on the server · + the API container's environment")
        cnt.move_to([0.5, -2.75, 0])
        env = outline_box(1.9, 0.9, S.GREY, solid=False).move_to(v.slots["api"])
        env_t = mono("env", 20, S.GREY).move_to(env).shift(LEFT * 0.45)
        ecr = VGroup(box(1.9, 0.9, CLOUD, fill_opacity=0.1, radius=0.18), label("ECR", 22, CLOUD))
        ecr[1].move_to(ecr[0])
        ecr.move_to([5.4, 0.9, 0])
        with self.voiceover(SAY[5]) as vo:
            drop_all(self, t4, rc, run_time=0.4)
            self.play(FadeIn(cap), FadeIn(p36, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("a file only root can open")
            b43, b44 = line_bar(p36.code, 7, TURN), line_bar(p36.code, 8, TURN)
            self.play(FadeIn(b43), FadeIn(b44), run_time=0.4)
            self.play(Indicate(code_span(p36.code, 8, "0600"), color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("a second copy on the server")
            self.play(FadeOut(VGroup(p36, b43, b44), target_position=frow.get_center(), scale=0.3),
                      FadeIn(v), run_time=0.6)
            self.remove(p36, b43, b44)
            v.wall(self, run_time=0.5)
            self.play(FadeIn(frow, shift=DOWN * 0.1), FadeIn(badge, scale=0.6), run_time=0.5)
            self.play(FadeIn(cnt, shift=UP * 0.1), Indicate(badge, color=INK, scale_factor=1.25), run_time=0.6)
            vo.wait_until("and hands them to the API container")
            self.play(FadeIn(env), FadeIn(env_t), run_time=0.4)
            b2 = badge.copy()
            self.play(b2.animate.move_to(env.get_center() + RIGHT * 0.35), run_time=0.8)
            vo.wait_until("It creates a Docker network")
            v.engine(self, run_time=0.3)
            v.network(self)
            self.play(Indicate(v.net.text, color=ROUTE, scale_factor=1.1), run_time=0.5)
            vo.wait_until("and two folders")
            v.disk(self)
            vo.wait_until("and logs in to E C R")
            self.play(FadeIn(ecr, shift=LEFT * 0.1), run_time=0.4)
            login = route(v.engine_label.get_right() + RIGHT * 0.05, ecr[0].get_left(), arc=-0.3, stroke=4)
            self.play(Create(login), run_time=0.6)
            self.play(Indicate(ecr[1], color=CLOUD, scale_factor=1.15), run_time=0.5)

        # ========================================================== 6. which tag: the environment or the file
        p101 = code(SC, 101, 104, font_size=T20)
        p101.move_to([0, 2.3 - p101.height / 2, 0])
        p106 = code(SC, 106, 114, font_size=T20)
        p106.move_to([0, 2.3 - p106.height / 2, 0])
        fy = (p106.get_bottom()[1] - 3.45) / 2
        src = route_chip("DOCKER_TAG", mono_font=True).move_to([-5.0, fy, 0])
        envset = route_chip("that tag").move_to([-0.8, fy + 0.45, 0])
        fileset = VGroup(file_glyph(0.34, OWN), mono(".docker-tag", 20, OWN)).arrange(RIGHT, buff=0.1)
        file_fr = box(fileset.width + 0.4, 0.45, OWN, fill_opacity=0.12)
        fileset.move_to(file_fr)
        fileb = VGroup(file_fr, fileset).move_to([-0.8, fy - 0.45, 0])
        a_set = arrow(src.get_right(), envset.get_left(), ROUTE)
        a_file = arrow(src.get_right(), fileb.get_left(), OWN)
        l_set = label("set", 20, ROUTE).next_to(a_set.get_center(), UP, buff=0.12)
        l_emp = label("empty", 20, OWN).next_to(a_file.get_center(), DOWN, buff=0.12)
        fork = VGroup(src, a_set, a_file, envset, fileb, l_set, l_emp)
        whence = VGroup(label("laptop run: the file", 20, S.GREY),
                        label("CI run: the extra variable wins (S14)", 20, S.GREY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
        wh_fr = outline_box(whence.width + 0.5, whence.height + 0.4, S.GREY, solid=False)
        whence.move_to(wh_fr)
        wh = VGroup(wh_fr, whence).move_to([6.45 - (whence.width + 0.5) / 2, fy, 0])
        assert wh.get_left()[0] > fileb.get_right()[0] + 0.2 and envset.get_right()[0] < wh.get_left()[0]
        with self.voiceover(SAY[6]) as vo:
            drop_all(self, v, frow, badge, b2, env, env_t, cnt, ecr, login, run_time=0.4)
            self.play(FadeIn(p101, shift=UP * 0.15), FadeIn(src), run_time=0.5)
            vo.wait_until("a docker tag variable")
            self.play(*[g.animate.set_color(ROUTE) for g in code_span(p101.code, 2, "lookup('env', 'DOCKER_TAG')")],
                      run_time=0.4)
            self.play(GrowArrow(a_set), FadeIn(l_set), FadeIn(envset, shift=RIGHT * 0.1), run_time=0.6)
            self.play(Indicate(envset.text, color=ROUTE, scale_factor=1.1), run_time=0.5)
            vo.wait_until("otherwise, the dot docker tag file")
            self.play(ReplacementTransform(p101, p106), run_time=0.7)
            self.play(*[g.animate.set_color(OWN) for g in code_span(p106.code, 3, "cat .docker-tag")],
                      GrowArrow(a_file), FadeIn(l_emp), FadeIn(fileb, shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("From your laptop")
            self.play(FadeIn(wh, shift=LEFT * 0.1), Circumscribe(fileb, color=OWN, buff=0.08), run_time=0.8)
            self.play(Indicate(whence[0], color=INK, scale_factor=1.05), run_time=0.5)

        # ========================================================== 7. on a real server: pull, start, load, start
        cubes = VGroup(*[cube_glyph(0.45) for _ in range(3)]).arrange(RIGHT, buff=0.1).move_to(ecr[0])
        bed = cost_tag("Bedrock · per token")
        with self.voiceover(SAY[7]) as vo:
            drop_all(self, p106, fork, wh, run_time=0.4)
            self.play(FadeIn(v), FadeIn(ecr), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cubes], lag_ratio=0.2), run_time=0.5)
            o = v._o()
            dst = [v.slots["frontend"] + o, v.slots["loader"] + o, v.slots["api"] + o]
            self.play(LaggedStart(*[c.animate.move_to(d) for c, d in zip(cubes, dst)], lag_ratio=0.25), run_time=1.2)
            vo.wait_until("and starts the frontend")
            self.play(FadeOut(cubes[0], scale=1.4), run_time=0.3)
            self.remove(cubes[0])
            v.container(self, "frontend")
            self.play(Indicate(v.containers["frontend"].sub, color=INK, scale_factor=1.15), run_time=0.5)
            vo.wait_until("and Chroma on 8000")
            v.container(self, "vectordb")
            pin_c = v.version(self, "vectordb", "0.5.18", OWN)
            yp = label("your pin", 20, OWN).next_to(pin_c, LEFT, buff=0.15)
            self.play(FadeIn(yp, shift=RIGHT * 0.1), run_time=0.3)
            vo.wait_until("A throwaway container")
            self.play(FadeOut(cubes[1], scale=1.4), run_time=0.3)
            self.remove(cubes[1])
            v.container(self, "loader", run_time=0.4)
            v.loader_run(self, run_time=2.0)
            vo.wait_until("then the API starts")
            self.play(FadeOut(cubes[2], scale=1.4), run_time=0.3)
            self.remove(cubes[2])
            v.container(self, "api")
            bed.move_to([v.containers["api"].get_x(), -2.75, 0])
            self.play(FadeIn(bed, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("The security group")
            v.ports_inside(self)
            self.play(Indicate(v.sg.line, color=CLOUD, scale_factor=1.0),
                      each([v.inner_ports[i] for i in range(3)], S.GREY), run_time=0.9)

        # ========================================================== 8. step 11: look around on the server
        tr11 = tracker_b(11)
        rp8 = readme_panel(120, 132)
        rp8.move_to([0, 2.55 - rp8.height / 2, 0])
        r120 = rp8.rows[120]
        assert isinstance(r120, Text), type(r120)
        gcp = glyphs_of(r120, readme_lines(120, 120)[0][1], "from the GCP console")
        ul = under(gcp, ERR)
        e8 = VGroup(label("on AWS:", 20, INK), mono("ssh -i <your key>.pem ubuntu@<EXTERNAL_IP>", 20, ROUTE),
                    label("or EC2 Instance Connect", 20, INK)).arrange(RIGHT, buff=0.2)
        e8_fr = box(e8.width + 0.6, e8.height + 0.6, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        e8.move_to(e8_fr).shift(DOWN * 0.06)
        e8_tg = erratum_tag()
        e8_tg.move_to(e8_fr.get_corner(UL) + np.array([0.3 + e8_tg.width / 2, 0, 0]))
        et8 = VGroup(e8_fr, e8, e8_tg)
        et8.next_to(rp8, DOWN, buff=0.45)
        assert et8.width < 13.1 and et8.get_bottom()[1] > -3.5, (et8.width, et8.get_bottom())
        r122 = rp8.rows[122]
        turn8 = your_turn()      # on the card's top edge: the rows are too close for a tag beside row 122
        turn8.move_to([rp8.frame.get_right()[0] - 0.3 - turn8.width / 2, rp8.frame.get_top()[1], 0])
        with self.voiceover(SAY[8]) as vo:
            drop_all(self, v, ecr, cap, bed, yp, run_time=0.4)
            self.play(ReplacementTransform(tr, tr11), FadeIn(rp8, shift=UP * 0.15), run_time=0.6)
            tr = tr11
            vo.wait_until("Where the README says")
            self.play(Create(ul), Indicate(gcp, color=ERR, scale_factor=1.06), run_time=0.7)
            vo.wait_until("use S S H")
            self.play(FadeIn(et8, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, e8_tg)
            vo.wait_until("Then list containers")
            self.play(FadeIn(turn8, shift=DOWN * 0.1), r122.animate.set_color(TURN), run_time=0.5)
            self.play(Indicate(r122, color=TURN, scale_factor=1.05), run_time=0.5)
            vo.wait_until("follow logs")
            self.play(each([rp8.rows[n] for n in (123, 124, 125)], TURN, scale=1.04), run_time=0.9)
            vo.wait_until("or open a shell")
            self.play(each([rp8.rows[n] for n in (130, 131)], TURN, scale=1.04), run_time=0.7)

        # ========================================================== 9. the stand-in on the laptop
        t9 = term(P_LAPTOP, rows=11, size=T20)
        tg9 = bar_tags(t9, standin_row())
        later = under_term(t9, grey_chip("nginx: after the next step"))
        with self.voiceover(SAY[9]) as vo:
            drop_all(self, rp8, ul, et8, turn8, run_time=0.4)
            self.play(track(tr, 11, True), FadeIn(t9, shift=UP * 0.2), FadeIn(tg9), run_time=0.5)
            type_capture(self, t9, C63, type_time=0.9)
            o63 = out(self, t9, [C63.line(2), L63_3, C63.line(4).rstrip(), C63.line(5).rstrip()], run_time=0.5)
            vo.wait_until("The image column")
            img_cells = [substring(o63[0], "IMAGE"), substring(o63[1], "nginx:stable"),
                         substring(o63[2], "python:3.12-slim-bookworm"), substring(o63[3], "python:3.12-slim-bookworm")]
            self.play(*[g.animate.set_color(TURN) for cell in img_cells for g in cell], run_time=0.5)
            self.play(each(img_cells, TURN, scale=1.06), run_time=0.8)
            type_capture(self, t9, C64, type_time=0.7)
            o64 = out(self, t9, [C64.line(4), from_phrase(C64.line(5), '"GET'), from_phrase(C64.line(6), '"GET')],
                      run_time=0.5)
            vo.wait_until("The nginx lines")
            self.play(FadeIn(later, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(VGroup(o64[1], o64[2]), color=S.GREY, scale_factor=1.03), run_time=0.7)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.remove(*self.mobjects)
        self.wait(0.3)
