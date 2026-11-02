"""S05 · Build once, configure at startup (V4: one image, many startups; secrets injected, never baked).
Lecture: L16 17, 21–22, 29; L10 42–43.

Beats (script.md "## S05", one voiceover block each):
 0  LECTURE 16 · 17, 29. Slide 29's three numbered steps redrawn (AWS chip): (1) a GREY "source +
    Dockerfile" card with `docker build -t myapp:v1.4 .` → "1 · build + push" → the TEAL image
    myapp:v1.4 with its digest stamp lands on the TEAL registry shelf "ECR"; (2) "2 · deploy · pull +
    start myapp:v1.4" into the BLUE private app subnet (a TEAL FastAPI task running myapp:v1.4);
    (3) a browser request reaches it through the ALB. The digest stamp flashes on "No rebuild".
 1  LECTURE 16 · 21. The canvas clears but the image, which rides a conveyor through dev, staging,
    prod; the digest stamp never changes (a YELLOW ✓ under each stop). At each stop a TEAL container
    starts and a GREEN runtime-value card plugs in (dev APP_ENV=dev · LOG_LEVEL=debug ·
    FEATURE_FLAG=true; prod APP_ENV=prod · LOG_LEVEL=info · FEATURE_FLAG=false); LOG_LEVEL lights.
 2  LECTURE 16 · 22. The prod container grows; a BLUE secret manager on the left; a PINK path
    "authorized delivery · workload identity" carries a GOLD key into the process environment (a
    GREEN os.getenv(…) chip), not into the image. A GREY strip "Never place secrets in: source code,
    container images, or Git" and a chip "grant only the secrets this workload needs".
 3  LECTURE 10 · 42. CODE(cheese-app-v2/src/api-service/docker-shell.sh: 23, 25, 27, 29–33) (folded)
    on top, lines 25 and 29 lit; below it the laptop half: the GREY laptop's secrets/ folder with a
    GOLD key, a PINK -v tunnel to /secrets in the TEAL container (the key copies through), and the
    env label GOOGLE_APPLICATION_CREDENTIALS=/secrets/…json written out of line 29 snaps onto the file.
 4  The laptop half fades; the panel becomes lines 30–33 on top; CODE(…/llm_rag_utils.py: 18–25)
    below, lines 19, 24, 25 lit; the names GCP_PROJECT, CHROMADB_HOST, CHROMADB_PORT fly in PINK from
    lines 30, 32, 33 to them; os.environ lights. Then the top panel fades.
 5  The panel turns into PANEL(cheese-app-v2/README.md: 25) (wrapped), the clause "we do not want any
    secure information in Git" lit YELLOW; below, the repo folder cheese-app-v2/ (in Git) and the
    secrets/ folder with the key beside it, outside it.
 6  LECTURE 16 · 22. Contrast (illustration): a GREY Dockerfile card "ENV LLM_API_KEY=…" builds an
    image; its layer stack is X-rayed (the key on the config card glows RED); a GREY docker inspect
    chip reads it; three copies fly to laptop, CI runner, prod host, each with the RED key. RED chips
    "rotate key → rebuild", then "dev image ≠ prod image".
 7  The canvas clears. PONDER P2 (McqCard, illustration): the stem is read; 10 s timer after.
 8  Reveal: D fills YELLOW ✓ with the GREEN note; the RED reason under A.
 9  RED reasons under B and C; the card fades.
10  TAKEAWAY, row by row as spoken; then an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    Transform,
    VGroup,
    Write,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S05"]

SHELL = "cheese-app-v2/src/api-service/docker-shell.sh"
RAG = "cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py"
assert source_line(SHELL, 25).strip() == '-v "$SECRETS_DIR":/secrets \\', source_line(SHELL, 25)
assert "GOOGLE_APPLICATION_CREDENTIALS=/secrets/" in source_line(SHELL, 29), source_line(SHELL, 29)
assert "-e GCP_PROJECT=$GCP_PROJECT" in source_line(SHELL, 30)
assert "-e CHROMADB_HOST=$CHROMADB_HOST" in source_line(SHELL, 32)
assert "-e CHROMADB_PORT=$CHROMADB_PORT" in source_line(SHELL, 33)
assert source_line(RAG, 19) == 'GCP_PROJECT = os.environ["GCP_PROJECT"]', source_line(RAG, 19)
assert source_line(RAG, 24) == 'CHROMADB_HOST = os.environ["CHROMADB_HOST"]', source_line(RAG, 24)
assert source_line(RAG, 25) == 'CHROMADB_PORT = os.environ["CHROMADB_PORT"]', source_line(RAG, 25)
README_CLAUSE = "we do not want any secure information in Git"
assert README_CLAUSE in readme_lines("cheese-app-v2", 25)[0]
assert IMAGE == "myapp:v1.4"

STEM = ("A teammate adds `ENV LLM_API_KEY=…` to the Dockerfile and pushes the image to the team's "
        "**private** registry. Which statement is true?")
OPTIONS = ["Safe: only the team can reach the registry",
           "Safe, as long as `.env` is in `.gitignore`",
           "A risk only for the production image",
           "Anyone who can pull the image can read the key"]
TAKEAWAY = ("same image promoted dev → staging → prod · environment values and authorized secrets "
            "injected at startup → never rebuild per environment, never bake a secret")

SAFE_L, SAFE_R, SAFE_B, SAFE_T = -6.6, 6.6, -3.6, 3.6


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def inside(m, name="", t=SAFE_T):
    guard(m.get_left()[0] >= SAFE_L and m.get_right()[0] <= SAFE_R and m.get_bottom()[1] >= SAFE_B
          and m.get_top()[1] <= t, f"{name} outside the safe frame: {m.get_left()}, {m.get_right()}, "
          f"{m.get_bottom()}, {m.get_top()}")


def apart(a, b, name="", buff=0.03):
    """a and b must not overlap (bounding boxes)."""
    ok = (a.get_right()[0] + buff <= b.get_left()[0] or b.get_right()[0] + buff <= a.get_left()[0]
          or a.get_top()[1] + buff <= b.get_bottom()[1] or b.get_top()[1] + buff <= a.get_bottom()[1])
    guard(ok, f"overlap: {name}")


def within(a, b, name=""):
    """a's bounding box lies inside b's."""
    guard(a.get_left()[0] >= b.get_left()[0] and a.get_right()[0] <= b.get_right()[0]
          and a.get_bottom()[1] >= b.get_bottom()[1] and a.get_top()[1] <= b.get_top()[1],
          f"{name} not inside")


def flash(mob, color=TURN, k=1.12, run_time=0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def badge_label(n, text, color=INK):
    """A numbered step (slide 29): YELLOW badge + its words."""
    b = step_badge(n, TURN, size=CAPTION, radius=0.2)
    t = label(text, CAPTION, color).next_to(b, RIGHT, buff=0.12)
    return VGroup(b, t)


def boxed(mobs, color, pad_x=0.35, pad_y=0.22, fill_opacity=0.95):
    """mobs on a rounded card of `color` (dark fill)."""
    body = mobs if isinstance(mobs, VGroup) else VGroup(mobs)
    fr = box(body.width + 2 * pad_x, body.height + 2 * pad_y, color, fill=S.BG, fill_opacity=fill_opacity)
    fr.move_to(body)
    g = VGroup(fr, body)
    g.frame, g.body = fr, body
    return g


def mini_image(bad=True):
    """A small image (three TEAL slabs) with its config key on top (RED when baked in)."""
    slabs = VGroup(*[box(1.0, 0.13, CTR, fill_opacity=0.25 + 0.1 * k, radius=0.03, stroke=2)
                     for k in range(3)]).arrange(DOWN, buff=0.04)
    k = key_glyph(0.2, ERR if bad else KEY).next_to(slabs, UP, buff=0.06)
    return VGroup(slabs, k)


class BuildOnce(VoiceScene):
    def construct(self):
        assert len(SAY) == 11, len(SAY)

        # ========================================================== 0 · slide 29: build once, deploy that tag
        chip_aws = aws_chip()
        place(chip_aws, left=-6.45, top=3.55)
        src = mono_card(["docker build \\", f"  -t {IMAGE} ."], S.GREY, header="source + Dockerfile")
        place(src, left=-6.35, cy=1.55)
        img = image_glyph(IMAGE)
        shelf = Line([2.55, 0, 0], [6.35, 0, 0], color=CTR, stroke_width=6)
        shelf.set_y(0.75)
        shelf_l = label("ECR · registry", CAPTION, CTR)
        place(shelf_l, cx=shelf.get_center()[0], top=shelf.get_bottom()[1] - 0.08)
        place(img, cx=shelf.get_center()[0], bottom=shelf.get_top()[1] + 0.06)
        y1 = src.frame.get_center()[1]
        a1 = arrow_([src.frame.get_right()[0] + 0.05, y1, 0], [shelf.get_left()[0] - 0.1, y1, 0], CTR)
        s1 = badge_label(1, "build + push")
        place(s1, cx=a1.get_center()[0], bottom=a1.get_top()[1] + 0.12)
        img_from = img.copy().shift(LEFT * 1.6)

        sub = box(6.0, 2.35, CLOUD, fill_opacity=0.08, stroke=3)
        place(sub, right=6.35, bottom=-3.3)
        sub_l = VGroup(padlock(0.24), label(f"private app subnet · {APP_CIDR}", CAPTION, INK)).arrange(RIGHT, buff=0.12)
        place(sub_l, left=sub.get_left()[0] + 0.2, top=sub.get_top()[1] - 0.12)
        task = boxed(VGroup(label("FastAPI", CAPTION, INK), mono(IMAGE, CAPTION, CTR)).arrange(DOWN, buff=0.06),
                     CTR, pad_x=0.3, pad_y=0.15)
        place(task, right=sub.get_right()[0] - 0.35, bottom=sub.get_bottom()[1] + 0.3)
        x2 = shelf.get_right()[0] - 0.55
        a2 = arrow_([x2, shelf_l.get_bottom()[1] - 0.08, 0], [x2, sub.get_top()[1] + 0.04, 0], CTR)
        s2 = badge_label(2, f"deploy · pull + start {IMAGE}")
        place(s2, right=a2.get_left()[0] - 0.15, cy=a2.get_center()[1])

        alb = boxed(label("ALB", CAPTION, INK), CLOUD, pad_x=0.3, pad_y=0.18)
        place(alb, right=sub.get_left()[0] - 0.55, cy=task.get_center()[1])
        brw = browser_glyph(1.3)
        place(brw, left=-6.35, cy=task.get_center()[1] + 0.15)
        brw_l = label("browser", CAPTION, BROWSER)
        place(brw_l, cx=brw.get_center()[0], top=brw.get_bottom()[1] - 0.08)
        a3 = arrow_(brw.get_right(), alb.get_left(), ROUTE)
        s3 = badge_label(3, "HTTPS request")
        place(s3, cx=a3.get_center()[0], bottom=a3.get_top()[1] + 0.12)
        a4 = arrow_(alb.get_right(), task.get_left(), ROUTE)
        dot = Dot(radius=0.09, color=TURN).move_to(brw.get_right())

        canvas0 = VGroup(src, img, shelf, shelf_l, a1, s1, sub, sub_l, task, a2, s2, alb, brw, brw_l, a3, s3, a4)
        inside(canvas0, "slide 29 canvas", t=3.05)
        inside(chip_aws, "AWS chip")
        apart(chip_aws, src, "AWS chip / source card")
        apart(s1, img, "step 1 / image")
        apart(s1, src, "step 1 / source card")
        apart(img, a1, "image / build arrow")
        apart(s2, sub, "step 2 / subnet")
        apart(s2, shelf_l, "step 2 / shelf label")
        apart(s2, src, "step 2 / source card")
        apart(sub_l, task, "subnet label / task")
        apart(s3, src, "step 3 / source card")
        apart(s3, alb, "step 3 / ALB")
        apart(alb, sub, "ALB / subnet")
        apart(brw_l, s3, "browser label / step 3")
        guard(a3.get_length() >= 0.8 and a4.get_length() >= 0.4, "request arrows too short")
        tease = image_glyph(IMAGE, w=3.0)
        tease.move_to([0, 0.2, 0])
        t_key = key_glyph(0.36).move_to(tease.slabs[1])
        t_cap = note("a key inside the image?")
        place(t_cap, cx=0, top=tease.get_bottom()[1] - 0.25)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tease, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the key inside")
            self.play(FadeIn(t_key, scale=0.5), FadeIn(t_cap), run_time=0.5)
            self.play(t_key.animate.set_stroke(ERR).set_fill(ERR, 0.5), flash(tease.slabs, ERR, 1.05), run_time=0.7)
            vo.wait_until("First, how a release")
            self.play(FadeOut(VGroup(tease, t_key, t_cap)), run_time=0.4)
            lr = lref_swap(self, None, 16, "17, 29")
            self.play(FadeIn(chip_aws), FadeIn(src, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("Build the image once")
            self.play(GrowArrow(a1), FadeIn(s1), Create(shelf), FadeIn(shelf_l), run_time=0.8)
            self.play(FadeTransform(src.rows.copy(), img_from), run_time=0.7)
            vo.wait_until("push it with")
            self.play(img_from.animate.move_to(img), run_time=0.8)
            self.remove(img_from)
            self.add(img)
            self.play(flash(img.name, TURN, 1.12), run_time=0.5)
            vo.wait_until("and every deployment")
            self.play(GrowArrow(a2), FadeIn(s2), Create(sub), FadeIn(sub_l), run_time=0.8)
            self.play(FadeTransform(img.copy(), task), run_time=0.8)
            vo.wait_until("that exact version")
            self.play(flash(task[1][1], TURN, 1.15), flash(img.name, TURN, 1.12), run_time=0.7)
            self.play(FadeIn(brw), FadeIn(brw_l), FadeIn(alb), run_time=0.5)
            vo.wait_until("No rebuild")
            self.play(GrowArrow(a3), FadeIn(s3), GrowArrow(a4), run_time=0.6)
            self.add(dot)
            self.play(dot.animate.move_to(alb.get_left()), run_time=0.5)
            self.play(dot.animate.move_to(task.get_left()), flash(img.stamp, TURN, 1.12), run_time=0.5)
            self.play(FadeOut(dot), flash(task, OWN, 1.06), run_time=0.4)

        # ========================================================== 1 · slide 21: one immutable image, runtime values
        conv = ImageConveyor()
        conv.shift(UP * 0.8)
        head = note("one immutable image")
        place(head, left=-6.35, top=3.0)
        x_l = conv.labels
        checks = [conv.check(i) for i in range(3)]
        ctrs, cards = [], []
        vals = [["APP_ENV=dev", "LOG_LEVEL=debug", "FEATURE_FLAG=true"],
                ["APP_ENV=staging", "…"],
                ["APP_ENV=prod", "LOG_LEVEL=info", "FEATURE_FLAG=false"]]
        for i in range(3):
            c = boxed(mono("container", CAPTION, CTR), CTR, pad_x=0.5, pad_y=0.1)
            place(c, cx=conv.stop_point(i)[0], top=checks[i].get_bottom()[1] - 0.12)
            v = value_card(vals[i])
            place(v, cx=c.get_center()[0], top=c.get_bottom()[1] - 0.12)
            ctrs.append(c)
            cards.append(v)
            inside(VGroup(c, v), f"container {i}")
            apart(c, checks[i], f"container {i} / check")
        for i in range(2):
            apart(cards[i], cards[i + 1], f"value cards {i}/{i + 1}")
            apart(ctrs[i], ctrs[i + 1], f"containers {i}/{i + 1}")
        img_at0 = img.copy()
        img_at0.shift(np.array([conv.stop_point(0)[0] - img.get_center()[0],
                                conv.stop_point(0)[1] + 0.08 - img.get_bottom()[1], 0]))
        inside(img_at0, "image on the belt", t=3.05)
        apart(head, img_at0, "head / image")
        apart(img_at0, x_l, "image / stop labels")
        lvl = [cards[0].rows[1], cards[2].rows[1]]
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(src, shelf, shelf_l, a1, s1, sub, sub_l, task, a2, s2, alb, brw, brw_l,
                                     a3, s3, a4, chip_aws)), run_time=0.6)
            lr = lref_swap(self, lr, 16, "21")
            self.play(FadeIn(conv), FadeIn(head), img.animate.move_to(img_at0), run_time=0.9)
            self.play(flash(img.stamp, TURN, 1.15), run_time=0.6)
            vo.wait_until("It moves from")
            self.play(FadeIn(checks[0], scale=0.6), FadeIn(ctrs[0], shift=DOWN * 0.15), run_time=0.5)
            self.play(conv.carry(img, 1, run_time=0.9))
            self.play(FadeIn(checks[1], scale=0.6), FadeIn(ctrs[1], shift=DOWN * 0.15), run_time=0.5)
            self.play(conv.carry(img, 2, run_time=0.9))
            self.play(FadeIn(checks[2], scale=0.6), FadeIn(ctrs[2], shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("its digest never")
            self.play(flash(img.stamp, TURN, 1.18), *[flash(c, TURN, 1.3) for c in checks], run_time=0.8)
            vo.wait_until("What differs")
            self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.25) for v in cards], lag_ratio=0.4), run_time=1.3)
            vo.wait_until("log level debug")
            self.play(lvl[0].animate.set_color(TURN).scale(1.1), run_time=0.4)
            self.play(lvl[0].animate.scale(1 / 1.1), run_time=0.3)
            vo.wait_until("info in production")
            self.play(lvl[1].animate.set_color(TURN).scale(1.1), run_time=0.4)
            self.play(lvl[1].animate.scale(1 / 1.1), run_time=0.3)

        # ========================================================== 2 · slide 22: secrets injected at startup
        big = container_box(f"{IMAGE} · prod", w=4.6, h=2.5)
        place(big, right=6.35, cy=1.05)
        env_l = note("process environment")
        getenv = boxed(mono("os.getenv(…)", CAPTION, OWN), OWN, pad_x=0.25, pad_y=0.12)
        VGroup(env_l, getenv).arrange(DOWN, buff=0.15)
        place(env_l, left=big.frame.get_left()[0] + 0.3, top=big.body_top() - 0.1)
        place(getenv, left=env_l.get_left()[0], top=env_l.get_bottom()[1] - 0.15)
        key_spot = [getenv.get_right()[0] + 0.55, getenv.get_center()[1], 0]
        sm = secret_manager()
        place(sm, left=-6.35, cy=big.frame.get_center()[1] - 0.25)
        path = arrow_(sm.get_right() + RIGHT * 0.05, [big.frame.get_left()[0] - 0.05, sm.get_center()[1], 0], ROUTE)
        p_up = label("authorized delivery", CAPTION, ROUTE)
        place(p_up, cx=path.get_center()[0], bottom=path.get_top()[1] + 0.1)
        p_dn = label("workload identity", CAPTION, ROUTE)
        place(p_dn, cx=path.get_center()[0], top=path.get_bottom()[1] - 0.1)
        key_fly = key_glyph(0.3).move_to(sm.key)
        never = boxed(label("Never place secrets in: source code, container images, or Git", CAPTION + 2, INK),
                      S.GREY, pad_x=0.4, pad_y=0.2)
        place(never, cx=0, top=big.frame.get_bottom()[1] - 0.45)
        grant = grey_chip("grant only the secrets this workload needs")
        place(grant, cx=0, top=never.get_bottom()[1] - 0.3)
        k_end = key_fly.copy().move_to(key_spot)
        within(k_end, big.frame, "key in the container")
        apart(k_end, getenv, "key / getenv chip")
        within(getenv, big.frame, "getenv chip in the container")
        inside(VGroup(big, sm, never, grant, p_up, p_dn), "slide 22 canvas", t=3.05)
        apart(p_up, sm, "path label / secret manager")
        apart(p_up, big, "path label / container")
        apart(p_dn, big, "path label / container")
        apart(never, big, "never strip / container")
        guard(path.get_length() >= 1.5, "delivery path too short")
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(conv, head, img, *checks, ctrs[0], ctrs[1], cards[0], cards[1], cards[2])),
                      run_time=0.6)
            lr = lref_swap(self, lr, 16, "22")
            self.play(ReplacementTransform(ctrs[2], big), run_time=0.8)
            self.play(FadeIn(env_l), FadeIn(getenv, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("A secret manager")
            self.play(FadeIn(sm, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("delivers the key")
            self.play(GrowArrow(path), FadeIn(p_up), run_time=0.7)
            self.add(key_fly)
            self.play(key_fly.animate.move_to(key_spot), run_time=1.1)
            self.play(flash(getenv, OWN, 1.1), run_time=0.5)
            vo.wait_until("only to the workload")
            self.play(FadeIn(p_dn, shift=UP * 0.1), flash(big.frame, CTR, 1.03), run_time=0.7)
            self.play(FadeIn(grant, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Never place secrets")
            self.play(FadeIn(never, shift=UP * 0.15), run_time=0.6)
            self.play(flash(never.body, INK, 1.04), run_time=0.7)

        # ========================================================== 3 · L10 slide 42: the laptop version
        sh = src_panel(SHELL, [23, 25, 27, (29, 33)])
        place(sh, cx=0, top=3.05)
        inside(sh, "docker-shell panel", t=3.05)
        sec_sp = sh.span(25, "/secrets")
        bar25, bar29 = sh.bar(25), sh.bar(29)
        gac_sp = sh.span(29, "GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json")
        strip_top = sh.get_bottom()[1] - 0.18
        strip_h = strip_top - (-3.5)
        lap = laptop_zone(w=3.0, h=strip_h, caption="your laptop")
        place(lap, left=-6.4, top=strip_top)
        h_dir = VGroup(folder_glyph(0.26, LAPTOP), mono("secrets/", CAPTION, INK)).arrange(RIGHT, buff=0.1)
        h_key = key_glyph(0.26)
        h_row = VGroup(h_dir, h_key).arrange(RIGHT, buff=0.18)
        place(h_row, left=lap.frame.get_left()[0] + 0.25, top=strip_top - 0.3)
        ctr = container_box("container", w=8.05, h=strip_h)
        place(ctr, right=6.4, top=strip_top)
        ctr.title.align_to(ctr.frame, RIGHT).shift(LEFT * 0.3)
        c_dir = VGroup(folder_glyph(0.26, CTR), mono("/secrets/", CAPTION, INK)).arrange(RIGHT, buff=0.1)
        c_file = VGroup(file_glyph(0.3, S.GREY), mono("…json", CAPTION, INK)).arrange(RIGHT, buff=0.1)
        c_row = VGroup(c_dir, c_file).arrange(RIGHT, buff=0.3)
        place(c_row, left=ctr.frame.get_left()[0] + 0.3, cy=h_row.get_center()[1])
        c_key = key_glyph(0.22).next_to(c_file, RIGHT, buff=0.15)
        env = mono("GOOGLE_APPLICATION_CREDENTIALS=/secrets/…json", CAPTION, OWN)
        place(env, left=ctr.frame.get_left()[0] + 0.3, top=c_row.get_bottom()[1] - 0.22)
        n_eq = len("GOOGLE_APPLICATION_CREDENTIALS=")
        env_path = env[n_eq:]
        tun = tunnel([lap.frame.get_right()[0] + 0.02, h_row.get_center()[1], 0],
                     [ctr.frame.get_left()[0] - 0.02, h_row.get_center()[1], 0], "-v")
        within(env, ctr.frame, "env label in the container")
        within(VGroup(c_row, c_key), ctr.frame, "secrets row in the container")
        within(h_row, lap.frame, "host secrets in the laptop")
        apart(h_row, lap.caption, "host secrets / laptop caption")
        apart(VGroup(c_row, c_key), ctr.title, "container row / title")
        apart(env, c_row, "env label / secrets row")
        inside(VGroup(lap, ctr, tun), "laptop half")
        guard(lap.get_bottom()[1] >= -3.55 and strip_h >= 1.45, f"laptop strip too short ({strip_h:.2f})")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(big, env_l, getenv, key_fly, sm, path, p_up, p_dn, never, grant)), run_time=0.6)
            lr = lref_swap(self, lr, 10, "42")
            self.play(FadeIn(sh, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("The run script mounts")
            self.play(FadeIn(bar25), sec_sp.animate.set_color(TURN), run_time=0.5)
            self.play(FadeIn(lap), FadeIn(h_row), FadeIn(ctr), run_time=0.6)
            vo.wait_until("at slash secrets")
            self.play(FadeIn(tun.line), FadeIn(tun[1]), FadeTransform(sec_sp.copy(), tun.label), run_time=0.7)
            kc = h_key.copy()
            self.add(kc)
            self.play(FadeIn(c_row), kc.animate.move_to(c_key), run_time=0.9)
            vo.wait_until("and points Google")
            self.play(FadeIn(bar29), gac_sp.animate.set_color(OWN), run_time=0.5)
            self.play(FadeTransform(gac_sp.copy(), env), run_time=0.9)
            vo.wait_until("inside the container")
            snap = env_path.copy()
            self.play(snap.animate.move_to(c_file[1]).set_opacity(0.0), c_file[1].animate.set_color(OWN),
                      env_path.animate.set_color(TURN), run_time=0.8)
            self.remove(snap)
            self.play(flash(c_file, OWN, 1.2), flash(env_path, TURN, 1.08), run_time=0.7)
        sh_bars = [bar25, bar29]

        # ========================================================== 4 · the app reads os.environ at startup
        sh2 = src_panel(SHELL, 30, 33)
        place(sh2, left=sh.get_left()[0], top=3.05)
        rag = src_panel(RAG, 18, 25)
        place(rag, left=sh2.get_left()[0], top=sh2.get_bottom()[1] - 0.35)
        inside(VGroup(sh2, rag), "env panels", t=3.05)
        apart(sh2, rag, "shell lines / rag panel")
        apart(sh2, lr, "shell lines / lecture tag")
        names = [("GCP_PROJECT", 30, 19), ("CHROMADB_HOST", 32, 24), ("CHROMADB_PORT", 33, 25)]
        srcs = [sh2.span(a, n) for n, a, _ in names]
        dsts = [rag.span(b, n) for n, _, b in names]
        envs = [rag.span(b, "os.environ") for _, _, b in names]
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(lap, h_row, ctr, c_row, kc, env, tun, *sh_bars)), run_time=0.6)
            self.play(FadeTransform(sh, sh2), run_time=0.9)
            self.play(FadeIn(rag, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("ChromaDB host")
            rag_bars = []
            for s_, d_, (_, _, b) in zip(srcs, dsts, names):
                fly = s_.copy().set_color(ROUTE)
                self.play(s_.animate.set_color(ROUTE), run_time=0.2)
                rb = rag.bar(b, ROUTE)
                rag_bars.append(rb)
                self.play(fly.animate.move_to(d_), FadeIn(rb), run_time=0.6)
                self.remove(fly)
                self.play(d_.animate.set_color(ROUTE), run_time=0.2)
            vo.wait_until("The app reads them")
            self.play(*[e.animate.set_color(TURN) for e in envs], run_time=0.5)
            self.play(*[flash(e, TURN, 1.15) for e in envs], run_time=0.7)
            vo.wait_until("when it starts")
            self.play(FadeOut(sh2), run_time=0.6)
            self.play(flash(VGroup(*envs), TURN, 1.08), run_time=0.6)

        # ========================================================== 5 · README: no secure information in Git
        rd = readme_panel("cheese-app-v2", 25)
        place(rd, cx=0, top=3.05)
        inside(rd, "README panel", t=3.05)
        clause = rd.clause(25, README_CLAUSE)
        repo = box(4.4, 2.2, S.GREY, fill_opacity=0.04, stroke=2.5)
        place(repo, left=-5.6, top=rd.get_bottom()[1] - 0.5)
        repo_h = VGroup(folder_glyph(0.26, S.GREY), mono("cheese-app-v2/", CAPTION, INK)).arrange(RIGHT, buff=0.1)
        place(repo_h, left=repo.get_left()[0] + 0.25, top=repo.get_top()[1] - 0.2)
        repo_rows = VGroup(file_row("src/"), file_row("README.md")).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        place(repo_rows, left=repo_h.get_left()[0] + 0.35, top=repo_h.get_bottom()[1] - 0.15)
        git_t = grey_tag("in Git")
        place(git_t, right=repo.get_right()[0] - 0.2, bottom=repo.get_bottom()[1] + 0.15)
        sec = VGroup(folder_glyph(0.3, LAPTOP), mono("secrets/", CAPTION, INK), key_glyph(0.26)).arrange(RIGHT, buff=0.14)
        place(sec, left=repo.get_right()[0] + 1.4, cy=repo_h.get_center()[1])
        sec_note = VGroup(note("same level, outside the repo"), note("never committed")).arrange(DOWN, buff=0.06,
                                                                                              aligned_edge=LEFT)
        place(sec_note, left=sec.get_left()[0], top=sec.get_bottom()[1] - 0.2)
        level = Line([repo.get_left()[0], repo.get_top()[1] + 0.22, 0], [sec.get_right()[0], repo.get_top()[1] + 0.22, 0],
                     color=S.GREY, stroke_width=2)
        lvl_l = note("same parent folder")
        place(lvl_l, left=sec.get_right()[0] + 0.15, cy=level.get_center()[1])
        inside(VGroup(repo, sec, sec_note, lvl_l), "folders")
        apart(level, rd, "level line / README panel")
        apart(lvl_l, rd, "level label / README panel")
        apart(repo_rows, git_t, "repo rows / git tag")
        apart(sec_note, repo, "secrets note / repo")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(*rag_bars)), FadeTransform(rag, rd), run_time=0.9)
            vo.wait_until("we do not want")
            self.play(clause.animate.set_color(TURN), run_time=0.8)
            self.play(flash(clause, TURN, 1.04), run_time=0.7)
            vo.wait_until("The key lives")
            self.play(FadeIn(repo), FadeIn(repo_h), FadeIn(repo_rows), FadeIn(git_t), run_time=0.6)
            self.play(Create(level), FadeIn(lvl_l), FadeIn(sec, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("never inside it")
            self.play(FadeIn(sec_note, shift=UP * 0.1), flash(sec[2], KEY, 1.3), run_time=0.7)

        # ========================================================== 6 · the wrong way: a key baked into the image
        df = illustration_card(["ENV LLM_API_KEY=…"], header="Dockerfile")
        place(df, left=-6.35, top=2.85)
        st = LayerStack()
        place(st, left=df.frame.get_left()[0], top=df.frame.get_bottom()[1] - 0.55)
        a_bake = arrow_([df.frame.get_center()[0], df.frame.get_bottom()[1] - 0.02, 0],
                        [df.frame.get_center()[0], st.get_top()[1] + 0.02, 0], CTR, stroke=3, buff=0.02)
        insp = grey_chip("docker inspect", font=MONO)
        place(insp, left=st.get_right()[0] + 0.4, cy=st.config[0].get_center()[1])
        insp_a = arrow_(insp.get_left(), st.config[0].get_right(), S.GREY, stroke=3, buff=0.05)
        dests = VGroup(*[boxed(label(t, CAPTION, INK), S.GREY, pad_x=0.3, pad_y=0.14)
                         for t in ("laptop", "CI runner", "prod host")])
        for d in dests:
            d.frame.stretch_to_fit_width(2.4)
        dests.arrange(DOWN, buff=0.35)
        place(dests, right=6.35, top=2.85)
        minis = [mini_image() for _ in range(3)]
        for m, d in zip(minis, dests):
            place(m, right=d.get_left()[0] - 0.25, cy=d.get_center()[1])
        rot = boxed(label("rotate key → rebuild", CAPTION, ERR), ERR, pad_x=0.3, pad_y=0.14)
        neq = boxed(mono("dev image ≠ prod image", CAPTION, ERR), ERR, pad_x=0.3, pad_y=0.14)
        VGroup(rot, neq).arrange(DOWN, buff=0.25, aligned_edge=RIGHT)
        place(VGroup(rot, neq), right=6.35, bottom=-3.3)
        inside(VGroup(df, st, insp, dests, *minis, rot, neq), "contrast canvas", t=3.05)
        apart(df, lr, "Dockerfile card / lecture tag")
        apart(dests, lr, "destinations / lecture tag")
        apart(insp, minis[1], "inspect chip / image copy")
        apart(insp, minis[0], "inspect chip / image copy 0")
        for m in minis:
            apart(m, st, "image copy / layer stack")
        apart(VGroup(rot, neq), dests, "chips / destinations")
        apart(VGroup(rot, neq), insp, "chips / inspect chip")
        apart(VGroup(rot, neq), st, "chips / layer stack")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(rd, repo, repo_h, repo_rows, git_t, sec, sec_note, level, lvl_l)), run_time=0.6)
            lr = lref_swap(self, lr, 16, "22")
            vo.wait_until("Now the wrong way")
            self.play(FadeIn(df, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Bake the key")
            self.play(GrowArrow(a_bake), FadeIn(st.layers, shift=UP * 0.15), run_time=0.7)
            self.play(FadeTransform(df.rows.copy(), st.config), run_time=0.8)
            vo.wait_until("and anyone who can pull")
            self.play(*st.xray(), run_time=0.8)
            self.play(FadeIn(insp, shift=LEFT * 0.1), GrowArrow(insp_a), run_time=0.6)
            self.play(flash(st.key, ERR, 1.4), flash(insp, INK, 1.06), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(d, shift=LEFT * 0.1) for d in dests], lag_ratio=0.2), run_time=0.6)
            starts = [m.copy().move_to(st.config[0]).set_opacity(0.0) for m in minis]
            for m0, m in zip(starts, minis):
                m.save_state()
                m.become(m0)
            self.play(LaggedStart(*[m.animate.restore() for m in minis], lag_ratio=0.25), run_time=1.3)
            vo.wait_until("Rotating it")
            self.play(FadeIn(rot, shift=UP * 0.1), run_time=0.5)
            self.play(*[flash(m[1], ERR, 1.3) for m in minis], run_time=0.6)
            vo.wait_until("and per environment")
            self.play(FadeIn(neq, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("what you tested")
            self.play(flash(neq, ERR, 1.06), run_time=0.7)

        # ========================================================== 7 · PONDER P2
        card = McqCard(STEM, OPTIONS, answer="D", seconds=10)
        inside(card, "ponder card")
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(df, st, a_bake, insp, insp_a, dests, *minis, rot, neq)), FadeOut(lr),
                      run_time=0.6)
            vo.wait_until("A teammate bakes")
            self.play(FadeIn(card, scale=0.97), run_time=0.6)
            vo.wait_until("Which statement")
            self.play(flash(card.stem[-1], TURN, 1.04), run_time=0.7)
        bar = card.bar                     # the 10 s timer drains in silence (as mcq_ponder does)
        self.play(bar.animate(rate_func=lambda t: t).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=card.seconds)
        bar.set_stroke(opacity=0)

        # ========================================================== 8 · reveal: D; why not A
        with self.voiceover(SAY[8]) as vo:
            self.play(*card.right("inject at startup from a secret store"), run_time=0.7)
            vo.wait_until("and changing the key")
            self.play(flash(card.rows["D"][1], TURN, 1.04), run_time=0.6)
            vo.wait_until("A, the private registry")
            self.play(*card.wrong("A", "private = many people and machines · copied to every host"), run_time=0.7)

        # ========================================================== 9 · why not B, C
        with self.voiceover(SAY[9]) as vo:
            self.play(*card.wrong("B", "the key is in the Dockerfile → in Git and in the image"), run_time=0.7)
            vo.wait_until("C fails too")
            self.play(*card.wrong("C", "dev images leak too · per-environment images break build once"),
                      run_time=0.7)
            vo.wait_until("and separate images")
            self.play(flash(card.rows["D"], TURN, 1.04), run_time=0.7)
        self.play(FadeOut(card), run_time=0.6)

        # ========================================================== 10 · takeaway
        tk = takeaway(TAKEAWAY)
        inside(tk, "takeaway")
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeIn(VGroup(tk.frame, tk.head)), run_time=0.5)
            vo.wait_until("how to move")
            self.play(FadeIn(tk.rows[0], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("the same image")
            self.play(flash(tk.rows[0], TURN, 1.03), run_time=0.6)
            vo.wait_until("Environment values")
            self.play(FadeIn(tk.rows[1], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("Never rebuild")
            self.play(flash(tk.rows[1], TURN, 1.03), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(tk), run_time=0.6)
        self.wait(0.3)
