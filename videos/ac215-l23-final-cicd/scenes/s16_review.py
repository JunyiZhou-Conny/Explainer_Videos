"""S16 · The course on one server, and recap — no tracker. Lecture: 23 · slides 21–37 (beats 0–3).

Beats (script.md "## S16", one voiceover block each):
0. LECTURE 23 · 21–37. V7 at full size as the review board: the BLUE EC2 server (five TEAL
   containers on the PINK appnetwork, the GREEN disk), above it the GREY laptop (TEAL toolbox,
   ~/secrets/ with the WHITE badge and key), BLUE GitHub (runner, vault) and ECR (three cubes).
   WHITE badge copies sit where S13 left them (toolbox, server, api-service, vault).
1. LECTURE (held). Group 1, a YELLOW badge per phrase: "L01–L02 · venvs, VMs, containers" on the
   EC2 box (the containers pulse, a small `pipenv` chip under api-service); "L03 · containers share a
   bucket" on a GREY dashed bucket off the server; "L03–L04 · the senior developer builds and pushes
   by hand" on the laptop, a PINK arrow slides to the runner: "now the runner's job".
2. LECTURE (held). Group 2: "execution" over frontend + api-service, "state" over ECR and the disk
   (thin YELLOW overlays); "L05 · RAG" on the loader, vector-db and the PINK `/llm-rag` chat route;
   "L06–L07 · agents" on the API; GREY dashed "labeling" (L11) and "fine-tuning, LoRA, distillation"
   (L08) off the server, an arrow to a BLUE "Bedrock · ready-made models" box, the API's PINK call to
   it; a TEAL "cheese classifier · .keras" file drops into api-service.
3. LECTURE (held). Group 3: GREY dashed "training jobs, model deployment, pipelines · on AWS: L15's
   SageMaker pipeline" (L13, L15) off the server; "L18 · API + frontend containers"; "L09, L21 · the
   CI loop with release" on the runner; "L20, L22 · routing to services" on nginx (PINK routes).
4. LECTURE off. A small MS5 loop at the top (Test lit GREEN "L21", the keyword chip gives way to
   "every merge to main"); GREY dashed "instance role" over the server (its badge copies vanish, a
   short-lived token appears) and "GitHub OIDC" over the vault (its badges vanish); the wall comes
   back and door 443 turns GREEN: "HTTPS on 443".
5. The recap of this lecture: six small pictures in two rows, each lighting on its phrase: V3's badge
   and key in ~/secrets/; V5's toolbox with its PINK socket to the laptop's Docker; V4's two plays
   (localhost spark, appserver over a PINK SSH arrow); V6's GREEN tag card from `date` to a recreated
   container; V1's two sieves passing one `/run-deploy-app` ribbon; a GOLD broom sweeps the server
   ("by hand"). Fade.
6. "Test yourself" 1 of 5 (answers in exercises.md): the two secrets; ~/secrets/ with the badge and
   key and three unlabelled places whose badge copies blink on "three places".
7. Question 2: a `sh` chip flips to `dash` on "Ubuntu"; the `=9.0.0` file.
8. Question 3: a small toolbox crate with its PINK socket; a spark runs down it on "your laptop".
9. Question 4: a small tag card slides along a short trail from `date` to a container.
10. Question 5: two small sieves, four ribbons drop, `update readme` bounces; V8's two ends (button +
   hand, or the auto ring); GREY chip "answers:
   exercises.md · every command: the study guide". Fade out; empty frame.

Deviations from SHOW: the board's wall (security group) is drawn only in beat 4, where door 443 is
needed: before that the left margin holds the off-server items (bucket, labeling, fine-tuning,
Bedrock, training). The recap's six small pictures sit in two rows of three, not one row: one row
of six cannot keep 20 pt captions. Slide 25's three bands are drawn as the two the narration names
(execution, state). Long badges wrap onto two or three lines so they fit beside their target, and the
off-server items carry their lecture numbers as a YELLOW badge on a GREY dashed box. "HTTPS on 443" is
one GREEN chip at door 443. In question 5 only `update readme` bounces (the other ribbons wait above
the first sieve), so the picture does not answer the question; the RELEASE button with its hand "or"
the GREEN auto ring (V8's two ends, unlabelled) appear on "delivery or deployment".
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

import common as _c
from common import *  # noqa: F401,F403

SAY = NARRATION["S16"]

# ------------------------------------------------------------------ facts the board shows (asserted)
SERVICE = "src/api-service/api/service.py"
CNN = "src/api-service/api/utils/llm_cnn_utils.py"
assert 'prefix="/llm-rag"' in excerpt(SERVICE, 29, 29), excerpt(SERVICE, 29, 29)
assert ".keras" in excerpt(CNN, 146, 146), excerpt(CNN, 146, 146)
assert "bedrock-runtime" in source_text("src/api-service/api/utils/llm_rag_utils.py")
assert KEYWORD == "/run-deploy-app" and JOB_KEY == "/run-"
assert [r[0] for r in RIBBONS] == ["update readme", "fix typo /run-tests", "/run-deploy-app", "\\run-deploy-app"]

Q5_RIBBONS = ("update readme", "fix typo /run-tests", "/RUN-DEPLOY-APP", "\\run-deploy-app")   # script S16 b10
assert [r[0] for r in RIBBONS][:2] == list(Q5_RIBBONS[:2]) and RIBBONS[3][0] == Q5_RIBBONS[3]
O_Y = -1.15                 # the server sits low: frame y -3.45 .. 0.95
TOP_Y = (1.72, 3.05)        # laptop / GitHub / ECR row
LANE_Y = 1.33               # badges between the server and the top row
LEFT_X = -4.9               # centre of the off-server column (x -6.5 .. -3.3)


# ------------------------------------------------------------------ helpers of this scene
class _Quiet:
    """A stand-in scene: lets VmLayout build its parts without playing them (the board then fades
    in in one move)."""

    def __init__(self):
        self.mobjects = []

    def play(self, *a, **k):
        pass


def gone(scene, *mobs, run_time: float = 0.5):
    """FadeOut mobjects that are not members of a piece, and take them off the scene."""
    mobs = [m for m in mobs if m is not None]
    if not mobs:
        return
    scene.play(*[FadeOut(m) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


def badge(*lines, color=TURN, size: float = 20) -> VGroup:
    """A YELLOW review badge (1-3 lines), opaque so it sits ON what it names. .box .text"""
    t = VGroup(*[label(s, size, color) for s in lines]).arrange(DOWN, buff=0.06)
    b = RoundedRectangle(width=t.width + 0.36, height=t.height + 0.2, corner_radius=0.18,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.94)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def offboard(lines, lecture: str) -> VGroup:
    """Something the course taught that is NOT on this server: a GREY dashed box with its lines and
    a YELLOW lecture badge on its top edge."""
    bx = label_box(lines, S.GREY, dashed=True)
    bd = badge(lecture).move_to(bx.get_top())
    g = VGroup(bx, bd)
    g.frame, g.badge = bx, bd
    return g


def words(*parts, size: float = 24, color=INK):
    """One line of mixed text, built as ONE Text so it keeps one baseline: parts are str (house
    font) or ('m', str) (mono). Punctuation parts (',', '?') attach without a space."""
    s, t2f = "", {}
    for p in parts:
        piece = p[1] if isinstance(p, tuple) else p
        if s and not piece[:1] in ",.?:;":
            s += " "
        s += piece
        if isinstance(p, tuple):
            t2f[piece] = MONO
    return label(s, size, color, t2f=t2f)


def qcard(lines, card_w: float = 12.6) -> VGroup:
    """The YELLOW test-yourself card: lines of words(...)."""
    t = VGroup(*[words(*ln) for ln in lines]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    fr = RoundedRectangle(width=card_w, height=t.height + 0.55, corner_radius=0.16, stroke_color=TURN,
                          stroke_width=3).set_fill(S.BG, 0.96)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def token_glyph(r: float = 0.2) -> VGroup:
    """A short-lived credential: a small GREY clock disc."""
    c = Circle(radius=r, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY, 0.15)
    h1 = Line(ORIGIN, UP * r * 0.7, color=S.GREY, stroke_width=2.5)
    h2 = Line(ORIGIN, RIGHT * r * 0.5, color=S.GREY, stroke_width=2.5)
    return VGroup(c, h1, h2)


def bucket_glyph(w: float = 1.1) -> VGroup:
    """A GREY dashed bucket (a cloud storage bucket that is not in this repo)."""
    h = w * 0.8
    body = Polygon([-w / 2, h / 2, 0], [w / 2, h / 2, 0], [w * 0.38, -h / 2, 0], [-w * 0.38, -h / 2, 0])
    d = DashedVMobject(body, num_dashes=22, dashed_ratio=0.55).set_stroke(S.GREY, 2.5)
    rim = DashedVMobject(Ellipse(width=w, height=h * 0.25).move_to([0, h / 2, 0]), num_dashes=14,
                         dashed_ratio=0.55).set_stroke(S.GREY, 2.5)
    return VGroup(d, rim)


TEST_W = label_box("Test · L21", PASS, size=20, pad=0.12).frame.width + 0.0


def mini_loop() -> VGroup:
    """V8's MS5 loop, small: six boxes in a row. .boxes{key} .arrows"""
    boxes = {}
    row = VGroup()
    for k in LOOP_KEYS:
        b = label_box(LOOP_NAMES[k], INK if k != "test" else S.GREY, dashed=(k == "test"), size=20, pad=0.12,
                      box_w=TEST_W if k == "test" else None)
        boxes[k] = b
        row.add(b)
    row.arrange(RIGHT, buff=0.38)
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, stroke_width=3, color=S.GREY,
                            max_tip_length_to_length_ratio=0.35) for a, b in zip(row[:-1], row[1:])])
    g = VGroup(row, arrows)
    g.boxes, g.arrows, g.row = boxes, arrows, row
    return g


def caption(s: str, color=S.GREY) -> Text:
    return label(s, 20, color)


# ------------------------------------------------------------------ the recap's six small pictures
def mini_secrets(h: float = 0.55):
    fr = box(2.6, 1.5, LAPTOP, fill_opacity=0.06)
    t = mono("~/secrets/", 20, LAPTOP).move_to(fr.get_top() + DOWN * 0.3)
    b, k = badge_glyph(h), key_glyph(h)
    VGroup(b, k).arrange(RIGHT, buff=0.45).move_to(fr.get_center() + DOWN * 0.22)
    g = VGroup(fr, t, b, k)
    g.badge, g.key = b, k
    return g


def mini_socket(gap: float = 0.8, shelf_w: float = 2.8, shelf_text: str = "Docker engine"):
    cr = crate("toolbox", box_w=1.8, box_h=0.62)
    shelf = VGroup(Line(LEFT * shelf_w / 2, RIGHT * shelf_w / 2, color=LAPTOP, stroke_width=5),
                   label(shelf_text, 20, LAPTOP))
    shelf[1].next_to(shelf[0], DOWN, buff=0.08)
    shelf.next_to(cr, DOWN, buff=gap)
    sock = Line(cr.get_bottom(), shelf[0].get_center(), color=ROUTE, stroke_width=4)
    g = VGroup(cr, sock, shelf)
    g.crate, g.sock, g.shelf = cr, sock, shelf
    return g


def mini_plays():
    c1 = VGroup(box(1.6, 0.55, OWN, fill_opacity=0.08), mono("localhost", 20, IMAGE))
    c2 = VGroup(box(1.6, 0.55, OWN, fill_opacity=0.08), mono("appserver", 20, CLOUD))
    for c in (c1, c2):
        c[1].move_to(c[0])
    VGroup(c1, c2).arrange(RIGHT, buff=0.25)
    cr = crate("", box_w=0.9, box_h=0.6).next_to(c1, DOWN, buff=0.35)
    srv = box(0.9, 0.6, CLOUD, fill_opacity=0.12).next_to(c2, DOWN, buff=0.35).shift(DOWN * 0.45)
    ssh = route(cr.get_right(), srv.get_left(), stroke=3)
    st = mono("SSH", 20, ROUTE).next_to(ssh.get_center(), UP, buff=0.12)
    g = VGroup(c1, c2, cr, srv, ssh, st)
    g.c1, g.c2, g.crate, g.srv, g.ssh, g.st = c1, c2, cr, srv, ssh, st
    return g


def mini_tag(gap: float = 2.0, card_text: str = "tag"):
    d = mono("date", 20, TOOL)
    cr = crate("", box_w=0.8, box_h=0.6)
    VGroup(d, cr).arrange(RIGHT, buff=gap)
    trail = DashedLine(d.get_right() + RIGHT * 0.12, cr.get_left() + LEFT * 0.1, color=ROUTE, dash_length=0.12)
    card = tag_card(card_text).next_to(d, UP, buff=0.25).align_to(d, LEFT)
    end = card.copy().next_to(cr, UP, buff=0.25).set_opacity(0)     # where the card ends (layout only)
    g = VGroup(d, trail, cr, card, end)
    g.date, g.trail, g.crate, g.card, g.end = d, trail, cr, card, end
    return g


def mini_sieves():
    s1 = _c._sieve(2.8, "", 20)
    s2 = _c._sieve(1.6, "", 20)
    s2.next_to(s1, DOWN, buff=0.45)
    rb = ribbon(KEYWORD).next_to(s1, UP, buff=0.15)
    end = rb.copy().next_to(s2, DOWN, buff=0.12).set_opacity(0)    # where the ribbon ends (layout only)
    g = VGroup(s1, s2, rb, end)
    g.s1, g.s2, g.rb, g.end = s1, s2, rb, end
    return g


def mini_server():
    fr = box(2.4, 1.4, CLOUD, fill_opacity=0.08)
    t = label("EC2", 20, CLOUD).move_to(fr.get_corner(UL) + np.array([0.38, -0.26, 0]))
    cs = VGroup(*[RoundedRectangle(width=0.46, height=0.38, corner_radius=0.06, stroke_color=IMAGE, stroke_width=2.5)
                  .set_fill(IMAGE, 0.3) for _ in range(3)]).arrange(RIGHT, buff=0.16).move_to(fr).shift(DOWN * 0.18)
    g = VGroup(fr, t, cs)
    g.frame, g.cs = fr, cs
    return g


# ================================================================== the scene
class CourseReview(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S16"] == 11, len(SAY)
        board = self.board_build()
        self.board_groups(board)
        self.where_next(board)
        self.recap()
        self.questions()

    # -------------------------------------------------------------- the review board (V7 + laptop, GitHub, ECR)
    def board_build(self):
        q = _Quiet()
        v = VmLayout()
        v.shift(UP * O_Y)
        v.network(q)
        v.disk(q)
        for k in ("nginx", "frontend", "api", "vectordb", "loader"):
            v.container(q, k)
        self.v = v

        # the laptop: ~/secrets/ (badge + key) and the toolbox
        lap_fr = box(3.4, TOP_Y[1] - TOP_Y[0], LAPTOP, fill_opacity=0.05)
        lap_fr.move_to([-6.5 + 1.7, sum(TOP_Y) / 2, 0])
        lap_t = label("laptop", 20, LAPTOP).move_to(lap_fr.get_corner(UL) + np.array([0.5, -0.24, 0]))
        sec_t = mono("~/secrets/", 20, LAPTOP)
        sec_g = VGroup(badge_glyph(0.3), key_glyph(0.3)).arrange(RIGHT, buff=0.25)
        sec = VGroup(sec_t, sec_g).arrange(DOWN, buff=0.12)
        sec.move_to([lap_fr.get_left()[0] + 0.25 + sec.width / 2, lap_fr.get_y() - 0.15, 0])
        tbx = crate("toolbox", box_w=1.3, box_h=0.62).move_to([lap_fr.get_right()[0] - 0.8, lap_fr.get_y() - 0.15, 0])
        tbx_b = badge_glyph(0.26).move_to(tbx.frame.get_corner(UR) + np.array([-0.05, 0.02, 0]))
        lap = VGroup(lap_fr, lap_t, sec, tbx)
        lap.frame, lap.secrets, lap.toolbox = lap_fr, sec, tbx

        # GitHub: the runner and the vault (repository secrets)
        gh_fr = box(3.7, TOP_Y[1] - TOP_Y[0], CLOUD, fill_opacity=0.08, radius=0.2)
        gh_fr.move_to([-2.8 + 1.85, sum(TOP_Y) / 2, 0])
        gh_t = label("GitHub", 20, CLOUD).move_to(gh_fr.get_corner(UL) + np.array([0.55, -0.24, 0]))
        run_i = runner_icon(0.42, lit=True)
        run_t = mono("runner", 20, CLOUD)
        runner = VGroup(run_i, run_t).arrange(RIGHT, buff=0.12)
        runner.move_to([gh_fr.get_left()[0] + 0.2 + runner.width / 2, gh_fr.get_y() - 0.2, 0])
        vault = vault_glyph(0.6).move_to([gh_fr.get_right()[0] - 0.65, gh_fr.get_y() - 0.1, 0])
        vb = VGroup(badge_glyph(0.26), key_glyph(0.26)).arrange(RIGHT, buff=0.12)
        vb.next_to(vault, UP, buff=0.08)
        gh = VGroup(gh_fr, gh_t, runner, vault)
        gh.frame, gh.runner, gh.vault = gh_fr, runner, vault

        # ECR with the three images
        ecr_fr = box(2.0, TOP_Y[1] - TOP_Y[0], CLOUD, fill_opacity=0.08, radius=0.18)
        ecr_fr.move_to([1.2 + 1.0, sum(TOP_Y) / 2, 0])
        ecr_t = label("ECR", 20, CLOUD).move_to(ecr_fr.get_top() + DOWN * 0.26)
        cubes = VGroup(*[cube_glyph(0.34) for _ in range(3)]).arrange(RIGHT, buff=0.2)
        cubes.move_to(ecr_fr.get_center() + DOWN * 0.2)
        ecr = VGroup(ecr_fr, ecr_t, cubes)
        ecr.frame, ecr.cubes = ecr_fr, cubes

        # where the access key's copies sit on the server (S13: aws configure, the api's environment)
        srv_b1 = badge_glyph(0.3).move_to(v.frame.get_corner(UR) + np.array([-0.45, -0.3, 0]))
        api = v.containers["api"]
        srv_b2 = badge_glyph(0.26).move_to(api.frame.get_corner(DR) + np.array([-0.24, 0.2, 0]))
        copies = VGroup(tbx_b, srv_b1, srv_b2, vb)
        self.srv_badges = VGroup(srv_b1, srv_b2)
        self.vault_badges = vb

        ref = lref("21–37")
        self.ref = ref
        conts = [v.containers[k] for k in ("nginx", "frontend", "api", "vectordb", "loader")]
        with self.voiceover(SAY[0]):
            self.play(Create(v.frame), FadeIn(v.title), FadeIn(ref, shift=DOWN * 0.1), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in conts], lag_ratio=0.15),
                      Create(v.net.line), FadeIn(v.net.text), FadeIn(v.disk_box), run_time=1.3)
            self.play(LaggedStart(FadeIn(lap, shift=DOWN * 0.15), FadeIn(gh, shift=DOWN * 0.15),
                                  FadeIn(ecr, shift=DOWN * 0.15), lag_ratio=0.25), run_time=1.1)
            self.play(LaggedStart(*[FadeIn(c, scale=1.3) for c in copies], lag_ratio=0.2), run_time=0.7)
        self.add(v)
        v._reseat(self)
        return {"v": v, "lap": lap, "gh": gh, "ecr": ecr, "copies": copies, "api": api}

    # -------------------------------------------------------------- beats 1-3: every lecture on the board
    def board_groups(self, bd):
        v, lap, gh, ecr = bd["v"], bd["lap"], bd["gh"], bd["ecr"]
        C = v.containers

        # ---- group 1
        b1 = badge("L01–L02 · venvs, VMs, containers").move_to([0.5, LANE_Y, 0])
        pip = grey_chip("pipenv", mono_font=True).next_to(C["api"], DOWN, buff=0.08)
        bucket = bucket_glyph(1.0).move_to([LEFT_X, -1.45, 0])
        bk_t = caption("bucket").next_to(bucket, DOWN, buff=0.1)
        links = VGroup(*[DashedLine(bucket.get_right() + RIGHT * 0.1, p, color=S.GREY, dash_length=0.1)
                         for p in (C["nginx"].get_left() + LEFT * 0.05, C["frontend"].get_left() + LEFT * 0.05)])
        b2 = badge("L03 · containers", "share a bucket").next_to(bucket, UP, buff=0.2)
        b3 = badge("L03–L04 · the senior", "developer builds and", "pushes by hand")
        b3.next_to(lap.frame, DOWN, buff=0.12).align_to(lap.frame, LEFT).shift(RIGHT * 0.15)
        push = route(lap.toolbox.get_right() + RIGHT * 0.05, gh.runner[0].get_left() + LEFT * 0.05, stroke=4)
        now = route_chip("now the runner's job", mono_font=False)
        now.next_to(ecr.frame, RIGHT, buff=0.25).set_y(gh.runner.get_y())
        to_ecr = route(gh.runner.get_right() + RIGHT * 0.05, ecr.cubes.get_left() + LEFT * 0.05, arc=-0.6, stroke=3)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(b1, shift=DOWN * 0.1), run_time=0.5)
            self.play(LaggedStart(*[Indicate(C[k], color=IMAGE, scale_factor=1.06)
                                    for k in ("nginx", "frontend", "api", "vectordb", "loader")], lag_ratio=0.15),
                      run_time=1.3)
            self.play(FadeIn(pip, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("A shared bucket")
            self.play(Create(bucket), FadeIn(bk_t), run_time=0.7)
            self.play(FadeIn(b2, shift=DOWN * 0.1), Create(links), run_time=0.7)
            vo.wait_until("And the images")
            self.play(FadeIn(b3, shift=UP * 0.1), Indicate(lap.toolbox, color=IMAGE, scale_factor=1.08), run_time=0.7)
            self.play(GrowArrow(push), run_time=0.7)
            self.play(FadeIn(now, shift=DOWN * 0.1), Indicate(gh.runner, color=CLOUD, scale_factor=1.15), run_time=0.6)
            self.play(Create(to_ecr), LaggedStart(*[Indicate(c, scale_factor=1.25) for c in ecr.cubes], lag_ratio=0.2),
                      run_time=1.0)

        # ---- group 2
        g1 = [b1, pip, bucket, bk_t, links, b2, b3, push, now, to_ecr]
        fa = C["frontend"]
        ex_box = SurroundingRectangle(VGroup(fa, C["api"]), color=TURN, buff=0.1, stroke_width=2, corner_radius=0.1)
        ex_t = label("execution", 20, TURN).next_to(ex_box, DOWN, buff=0.06)
        st_disk = SurroundingRectangle(v.disk_box, color=TURN, buff=0.06, stroke_width=2, corner_radius=0.1)
        st_ecr = SurroundingRectangle(ecr.frame, color=TURN, buff=0.06, stroke_width=2, corner_radius=0.1)
        st_t1 = label("state", 20, TURN).next_to(st_disk, RIGHT, buff=0.12)
        st_t2 = label("state", 20, TURN).next_to(st_ecr, RIGHT, buff=0.12)
        rag = badge("L05 · RAG").move_to(C["loader"].get_top() + RIGHT * 0.45)
        chat = route_chip("/llm-rag").next_to(C["vectordb"], DOWN, buff=0.1)
        agents = badge("L06–L07 · agents").move_to(C["api"].get_top() + UP * 0.24)
        lab = offboard(["labeling"], "L11").move_to([LEFT_X, 0.45, 0])
        ft = offboard(["fine-tuning,", "LoRA, distillation"], "L08").move_to([LEFT_X, -1.0, 0])
        bed = label_box(["Bedrock", "ready-made models"], CLOUD).move_to([LEFT_X, -2.75, 0])
        ft_arr = arrow(ft.frame.get_bottom(), bed.get_top(), color=S.GREY, buff=0.08)
        call = route(C["api"].get_bottom() + LEFT * 0.55, bed.get_right(), stroke=3)
        keras = VGroup(file_glyph(0.36, IMAGE), label("cheese classifier · .keras", 20, IMAGE)).arrange(RIGHT, buff=0.12)
        keras.move_to([0.5, LANE_Y, 0])
        drop = file_glyph(0.36, IMAGE).move_to(keras[0])
        with self.voiceover(SAY[2]) as vo:
            gone(self, *g1, run_time=0.5)
            self.play(Create(ex_box), FadeIn(ex_t), run_time=0.7)
            vo.wait_until("E C R and the disk")
            self.play(Create(st_disk), Create(st_ecr), FadeIn(st_t1), FadeIn(st_t2), run_time=0.8)
            vo.wait_until("Retrieval")
            gone(self, ex_box, ex_t, st_disk, st_ecr, st_t1, st_t2, run_time=0.4)
            self.play(FadeIn(rag, shift=DOWN * 0.1), Indicate(C["loader"], color=IMAGE, scale_factor=1.06), run_time=0.6)
            self.play(Indicate(C["vectordb"], color=IMAGE, scale_factor=1.06), FadeIn(chat, scale=0.8), run_time=0.7)
            vo.wait_until("agents, lectures")
            self.play(FadeIn(agents, shift=UP * 0.1), Indicate(C["api"], color=IMAGE, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Labeling and fine tuning")
            self.play(FadeIn(lab, shift=RIGHT * 0.15), run_time=0.6)
            self.play(FadeIn(ft, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("the API calls")
            self.play(GrowArrow(ft_arr), FadeIn(bed, shift=UP * 0.1), run_time=0.7)
            self.play(Create(call), run_time=0.7)
            vo.wait_until("plus the cheese classifier")
            self.play(FadeIn(keras, shift=DOWN * 0.1), run_time=0.5)
            self.add(drop)
            self.play(drop.animate.move_to(C["api"].frame.get_corner(DL) + np.array([0.28, 0.22, 0])).scale(0.8),
                      run_time=0.9)

        # ---- group 3
        g2 = [rag, chat, agents, lab, ft, bed, ft_arr, call, keras, drop]
        sm = offboard(["training jobs,", "model deployment,", "pipelines", "on AWS: L15's", "SageMaker pipeline"],
                      "L13, L15").move_to([LEFT_X, -0.9, 0])
        l18 = badge("L18 · API + frontend containers").move_to([1.25, v.net.line.get_y(), 0])
        ci = badge("L09, L21 · the CI loop with release").move_to([gh.runner.get_x() + 1.2, LANE_Y, 0])
        ng = C["nginx"]
        rt = badge("L20, L22 · routing to services").move_to(ng.get_bottom() + DOWN * 0.3 + RIGHT * 0.2)
        r1 = route(ng.get_top() + UP * 0.03, fa.get_left() + LEFT * 0.03, arc=-0.4, stroke=3)
        with self.voiceover(SAY[3]) as vo:
            gone(self, *g2, run_time=0.5)
            self.play(FadeIn(sm, shift=RIGHT * 0.15), run_time=0.7)
            vo.wait_until("The API and frontend")
            self.play(FadeIn(l18, scale=0.9), Indicate(fa, color=IMAGE, scale_factor=1.06),
                      Indicate(C["api"], color=IMAGE, scale_factor=1.06), run_time=0.8)
            vo.wait_until("The C I loop")
            self.play(FadeIn(ci, shift=UP * 0.1), Indicate(gh.runner, color=CLOUD, scale_factor=1.15), run_time=0.8)
            vo.wait_until("Routing")
            self.play(FadeIn(rt, shift=UP * 0.1), Indicate(ng, color=IMAGE, scale_factor=1.06), run_time=0.7)
            self.play(Create(r1), run_time=0.7)
        self.g3 = [sm, l18, ci, rt, r1]

    # -------------------------------------------------------------- beat 4: where next
    def where_next(self, bd):
        v, gh = bd["v"], bd["gh"]
        loop = mini_loop()
        loop.move_to([0, 3.32, 0]).shift(RIGHT * (-6.45 - loop.get_left()[0]))
        kw = route_chip(KEYWORD).next_to(loop, RIGHT, buff=0.3)
        tb = loop.boxes["test"]
        tb_new = label_box("Test · L21", PASS, size=20, pad=0.12, box_w=TEST_W).move_to(tb)
        merge = ok_chip("every merge to main").next_to(loop, RIGHT, buff=0.3)
        role = outline_box(v.frame.width + 0.2, v.frame.height + 0.2, S.GREY).move_to(v.frame)
        role_t = dashed_chip("instance role · short-lived").move_to([2.45, LANE_Y, 0])
        tok = token_glyph(0.2).move_to(self.srv_badges[0])
        vault = gh.vault
        vv = VGroup(vault, self.vault_badges)
        oidc = outline_box(vv.width + 0.3, vv.height + 0.16, S.GREY).move_to(vv)
        oidc_t = dashed_chip("GitHub OIDC").move_to([gh.vault.get_x() - 1.1, LANE_Y, 0])
        with self.voiceover(SAY[4]) as vo:
            gone(self, self.ref, *self.g3, run_time=0.5)
            self.play(FadeIn(loop, shift=DOWN * 0.1), FadeIn(kw, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Put the tests")
            self.play(ReplacementTransform(tb, tb_new), run_time=0.7)
            self.play(Indicate(tb_new, color=PASS, scale_factor=1.1), run_time=0.6)
            vo.wait_until("and deploy every merge")
            self.play(FadeOut(kw, shift=UP * 0.2), FadeIn(merge, shift=UP * 0.2),
                      Indicate(loop.boxes["deploy"], color=PASS, scale_factor=1.1), run_time=0.8)
            vo.wait_until("Replace the copied keys")
            self.play(Create(role.frame), FadeIn(role_t), *[FadeOut(b) for b in self.srv_badges], run_time=0.8)
            self.play(FadeIn(tok, scale=0.5), run_time=0.4)
            vo.wait_until("and O I D C")
            self.play(Create(oidc.frame), FadeIn(oidc_t), FadeOut(self.vault_badges), run_time=0.8)
            vo.wait_until("And add HTTPS")
            v.wall(self, run_time=0.6)
            https = ok_chip("HTTPS on 443").next_to(v.doors[443].text, LEFT, buff=0.2)
            v.door(self, 443, "used", run_time=0.3)
            self.play(FadeIn(https, shift=RIGHT * 0.1), run_time=0.4)
        everything = [m for m in self.mobjects]
        self.play(*[FadeOut(m) for m in everything], run_time=0.6)
        self.clear()

    # -------------------------------------------------------------- beat 5: the recap of this lecture
    def recap(self):
        xs, ys = (-4.35, 0.0, 4.35), (1.6, -1.8)
        slots = VGroup(*[outline_box(4.15, 3.05, S.GREY, solid=False).move_to([xs[i % 3], ys[i // 3], 0])
                         for i in range(6)])
        pics = [mini_secrets(), mini_socket(), mini_plays(), mini_tag(), mini_sieves(), mini_server()]
        caps = ["two secrets", "toolbox · laptop's Docker", "localhost · appserver over SSH",
                "one tag · date to container", "one sentence presses release", "clean up by hand"]
        capm = []
        for i, (p, cs) in enumerate(zip(pics, caps)):
            sl = slots[i]
            c = caption(cs, COST if i == 5 else S.GREY).move_to(sl.get_bottom() + UP * 0.3)
            p.move_to([sl.get_x(), (sl.get_top()[1] + c.get_top()[1]) / 2, 0])
            capm.append(c)
        s, sk, pl, tg, sv, srv = pics
        lit = [None]

        def light(i):
            """ANIMS: slot i turns YELLOW (the one being said), the last one back to GREY."""
            an = [slots[i].frame.animate.set_stroke(TURN, 3)]
            if lit[0] is not None:
                an.append(slots[lit[0]].frame.animate.set_stroke(S.GREY, 2.5))
            lit[0] = i
            return an

        with self.voiceover(SAY[5]) as vo:
            self.play(LaggedStart(*[Create(sl.frame) for sl in slots], lag_ratio=0.12), run_time=1.2)
            vo.wait_until("Two secrets")
            self.play(*light(0), FadeIn(s[0]), FadeIn(s[1]), FadeIn(capm[0]), run_time=0.5)
            self.play(FadeIn(s.badge, shift=DOWN * 0.2), FadeIn(s.key, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("A toolbox")
            self.play(*light(1), FadeIn(sk.crate), FadeIn(sk.shelf), FadeIn(capm[1]), run_time=0.5)
            d = dot(ROUTE, 0.09).move_to(sk.sock.get_start())
            self.play(Create(sk.sock), run_time=0.4)
            self.add(d)
            self.play(d.animate.move_to(sk.sock.get_end()), run_time=0.6)
            self.play(FadeOut(d), Indicate(sk.shelf[0], color=ROUTE), run_time=0.4)
            vo.wait_until("Plays on localhost")
            self.play(*light(2), FadeIn(pl.c1), FadeIn(pl.crate), FadeIn(capm[2]), run_time=0.5)
            sp = spark(TOOL, 0.3).move_to(pl.crate)
            self.play(FadeIn(sp, scale=0.5), run_time=0.4)
            self.play(FadeIn(pl.c2), FadeIn(pl.srv), Create(pl.ssh), FadeIn(pl.st), FadeOut(sp), run_time=0.7)
            d2 = dot(ROUTE, 0.09).move_to(pl.ssh.get_start())
            self.add(d2)
            self.play(MoveAlongPath(d2, pl.ssh), run_time=0.8)
            self.play(FadeOut(d2), Indicate(pl.srv, color=CLOUD), run_time=0.4)
            vo.wait_until("One tag")
            self.play(*light(3), FadeIn(tg.date), Create(tg.trail), FadeIn(tg.crate), FadeIn(capm[3]),
                      FadeIn(tg.card, shift=DOWN * 0.1), run_time=0.6)
            self.play(tg.card.animate.move_to(tg.end), run_time=1.2)
            ghost = outline_box(tg.crate.frame.width, tg.crate.frame.height, S.GREY).move_to(tg.crate)
            self.play(FadeOut(tg.crate), FadeIn(ghost), run_time=0.3)
            new = crate("", box_w=0.8, box_h=0.6).move_to(ghost)
            self.play(FadeOut(ghost), FadeIn(new, scale=1.15), run_time=0.4)
            vo.wait_until("One sentence")
            self.play(*light(4), FadeIn(sv.s1), FadeIn(sv.s2), FadeIn(capm[4]), FadeIn(sv.rb, shift=DOWN * 0.2),
                      run_time=0.5)
            self.play(sv.rb.animate.move_to(sv.end), run_time=1.0)
            self.play(Indicate(sv.rb, color=PASS, scale_factor=1.05), run_time=0.4)
            vo.wait_until("And clean up")
            self.play(*light(5), FadeIn(srv), FadeIn(capm[5]), run_time=0.4)
            br = broom_glyph(0.8, COST).move_to(srv.frame.get_left() + RIGHT * 0.3 + UP * 0.05)
            self.play(FadeIn(br), run_time=0.2)
            self.play(br.animate.move_to(srv.frame.get_right() + LEFT * 0.3 + UP * 0.05),
                      srv.cs.animate.set_opacity(0.15), run_time=0.9)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        self.clear()

    # -------------------------------------------------------------- beats 6-10: test yourself
    def questions(self):
        head = label("Test yourself", 28, TURN).move_to([0, 3.15, 0]).align_to([-6.3, 0, 0], LEFT)
        num = label("1 of 5", 22, S.GREY).next_to(head, RIGHT, buff=0.35).align_to(head, DOWN)
        ans = caption("answers in exercises.md").move_to([0, 3.15, 0]).align_to([6.3, 0, 0], RIGHT).align_to(head, DOWN)
        Q = [
            [["Name the two secrets, what each opens, and three places"],
             ["the access key ends up after one deploy."],
             ["What would an instance role and GitHub OIDC remove?"]],
            [["Why does", ("m", "sh docker-shell.sh"), "fail on Ubuntu but work on a Mac,"],
             ["and what did", ("m", "pip install ansible>=9.0.0"), "actually do?"]],
            [["A", ("m", "hosts: localhost"), "play and a", ("m", "hosts: appserver"), "play:"],
             ["where does each task run, and why can the toolbox's"],
             [("m", "docker build"), "fill your laptop's disk?"]],
            [["Follow one timestamp from", ("m", "date"), "to a running container."],
             ["Where is it written down, and how does the server choose"],
             ["between", ("m", "DOCKER_TAG"), "and", ("m", ".docker-tag"), "?"]],
            [["Which of these deploy:", ("m", "update readme"), ",", ("m", "fix typo /run-tests"), ","],
             [("m", "/RUN-DEPLOY-APP"), ",", ("m", "\\run-deploy-app"), "? In the lecture's words, is this"],
             ["pipeline continuous delivery or continuous deployment?"]],
        ]
        cards = []
        for q in Q:
            c = qcard(q)
            c.move_to([0, 2.65 - c.height / 2, 0])
            cards.append(c)
        VIS_Y = -1.6

        # ---- question 1: the badge, the key, three places
        sec = mini_secrets().move_to([-4.2, VIS_Y, 0])
        places = VGroup(*[outline_box(1.5, 1.0, S.GREY, solid=True, fill_opacity=0.05) for _ in range(3)])
        places.arrange(RIGHT, buff=0.6).move_to([1.6, VIS_Y, 0])
        qmarks = VGroup(*[label("?", 24, S.GREY).move_to(p) for p in places])
        cps = VGroup(*[badge_glyph(0.3).move_to(p.get_corner(UR) + np.array([-0.3, -0.25, 0])) for p in places])
        arrs = VGroup(*[route(sec.get_right() + RIGHT * 0.05, places[0].get_left() + LEFT * 0.05, stroke=3)])
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(num), FadeIn(ans), run_time=0.5)
            vo.wait_until("One:")
            self.play(FadeIn(cards[0], shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(sec), run_time=0.5)
            vo.wait_until("three places")
            self.play(GrowArrow(arrs[0]), FadeIn(places), FadeIn(qmarks), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c, scale=1.4) for c in cps], lag_ratio=0.3), run_time=0.8)
            self.play(LaggedStart(*[Indicate(c, color=TURN, scale_factor=1.4) for c in cps], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("What would")
            self.play(FadeOut(cps, scale=0.6), Indicate(sec.badge, color=TURN, scale_factor=1.2), run_time=0.8)
        vis = [sec, places, qmarks, arrs]

        # ---- question 2: sh -> dash, the =9.0.0 file
        shc = grey_chip("sh", mono_font=True, size=28).move_to([-3.2, VIS_Y + 0.1, 0])
        ub = label("Ubuntu", 24, S.GREY).next_to(shc, UP, buff=0.3)
        dash = chip("dash", SHARED, size=28, font=MONO).move_to(shc)
        f9 = VGroup(file_glyph(1.0, S.GREY), mono("=9.0.0", 28, INK)).arrange(DOWN, buff=0.15).move_to([2.8, VIS_Y, 0])
        with self.voiceover(SAY[7]) as vo:
            gone(self, cards[0], *vis, run_time=0.4)
            self.play(FadeIn(cards[1], shift=UP * 0.1), Transform(num, label("2 of 5", 22, S.GREY).move_to(num)),
                      FadeIn(shc), run_time=0.6)
            vo.wait_until("fail on Ubuntu")
            self.play(FadeIn(ub, shift=DOWN * 0.1), run_time=0.4)
            self.play(ReplacementTransform(shc, dash), run_time=0.7)
            vo.wait_until("And what did")
            self.play(FadeIn(f9, shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(f9[1], color=TURN, scale_factor=1.15), run_time=0.8)
        vis = [ub, dash, f9]

        # ---- question 3: the toolbox's socket
        sk = mini_socket(gap=1.3, shelf_w=3.4).move_to([0, VIS_Y - 0.1, 0])
        spk = dot(ROUTE, 0.1).move_to(sk.sock.get_start())
        with self.voiceover(SAY[8]) as vo:
            gone(self, cards[1], *vis, run_time=0.4)
            self.play(FadeIn(cards[2], shift=UP * 0.1), Transform(num, label("3 of 5", 22, S.GREY).move_to(num)),
                      FadeIn(sk.crate), FadeIn(sk.shelf), run_time=0.6)
            self.play(Create(sk.sock), run_time=0.5)
            vo.wait_until("And why can")
            self.play(Indicate(sk.crate, color=IMAGE, scale_factor=1.1), run_time=0.6)
            vo.wait_until("the disk of your laptop")
            self.add(spk)
            self.play(spk.animate.move_to(sk.sock.get_end()), run_time=0.8)
            self.play(FadeOut(spk), Indicate(sk.shelf, color=ROUTE, scale_factor=1.1), run_time=0.6)
        vis = [sk]

        # ---- question 4: the tag card on its trail
        tg = mini_tag(gap=5.0, card_text=TAG_FMT).move_to([0, VIS_Y, 0])
        with self.voiceover(SAY[9]) as vo:
            gone(self, cards[2], *vis, run_time=0.4)
            self.play(FadeIn(cards[3], shift=UP * 0.1), Transform(num, label("4 of 5", 22, S.GREY).move_to(num)),
                      FadeIn(tg.date), Create(tg.trail), FadeIn(tg.crate), run_time=0.7)
            self.play(FadeIn(tg.card, shift=DOWN * 0.1), run_time=0.5)
            self.play(tg.card.animate.move_to(tg.end), run_time=2.0)
            vo.wait_until("How does")
            self.play(Indicate(tg.card, color=PASS, scale_factor=1.1), run_time=0.7)
        vis = [tg]

        # ---- question 5: two sieves, four ribbons; delivery or deployment
        sx = -1.8
        s1 = _c._sieve(6.0, "", 20).move_to([sx, -1.75, 0])
        s2 = _c._sieve(2.4, "", 20).move_to([sx, -2.7, 0])
        rb = {t: ribbon(t) for t in Q5_RIBBONS}
        grid = VGroup(rb[Q5_RIBBONS[1]], rb[Q5_RIBBONS[2]], rb[Q5_RIBBONS[0]], rb[Q5_RIBBONS[3]])
        grid.arrange_in_grid(2, 2, buff=(0.5, 0.2)).move_to([sx, -0.5, 0])
        up = rb["update readme"]
        btn = release_button(22).move_to([4.6, -0.75, 0])
        hand = hand_glyph(0.7).next_to(btn, UP, buff=0.05)
        orr = caption("or").next_to(btn, DOWN, buff=0.22)
        ring = auto_ring(0.42, PASS, 20).next_to(orr, DOWN, buff=0.22)
        final = grey_chip("answers: exercises.md · every command: the study guide").move_to([0, -3.3, 0])
        with self.voiceover(SAY[10]) as vo:
            gone(self, cards[3], *vis, run_time=0.4)
            self.play(FadeIn(cards[4], shift=UP * 0.1), Transform(num, label("5 of 5", 22, S.GREY).move_to(num)),
                      FadeIn(s1), FadeIn(s2), run_time=0.6)
            vo.wait_until("Update readme")
            self.play(LaggedStart(*[FadeIn(rb[t], shift=DOWN * 0.3) for t in Q5_RIBBONS], lag_ratio=0.45),
                      run_time=3.0)
            home = up.get_center()
            self.play(up.animate.next_to(s1.rim, UP, buff=0.02), run_time=0.4)
            self.play(up.animate.move_to(home), Indicate(s1.rim, color=ERR, scale_factor=1.03), run_time=0.6)
            self.play(Indicate(up, color=ERR, scale_factor=1.05), run_time=0.5)
            vo.wait_until("And is this pipeline")
            self.play(FadeIn(btn), FadeIn(hand, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(orr), FadeIn(ring), run_time=0.5)
            vo.wait_until("Answers are")
            self.play(FadeIn(final, shift=UP * 0.1), FadeOut(ans), run_time=0.5)
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.8)
        self.clear()
        self.wait(0.3)
