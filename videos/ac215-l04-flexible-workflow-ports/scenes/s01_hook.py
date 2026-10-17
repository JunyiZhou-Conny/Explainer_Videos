"""S01 · Build or pull? Whose localhost? (cold open of AC215 L4).

Beats (script.md "## S01", one voiceover block each):
0. Black frame, no tracker. A 13-row laptop terminal (prompt student@laptop:~/AC215/mega-pipeline/
   generate_text$) types `./docker-shell.sh run` on the row under the long prompt and replays
   mega-laptop/76-run-registry-b.txt lines 2-5, …, 15-16, 19-25 (wrap): line 4 "Local image not
   found, using image from registry..." prints YELLOW, line 20 "Python 3.8.17" YELLOW, line 25
   (the ImportError) RED with `genai` underlined; the GREY tag "the Gemini library" sits after the
   traceback's `from google import genai`, right above it. GREY tag top right: "no local image of
   generate_text". At "Inside, Python" the frame turns TEAL, title "container · generate_text"
   (enter_container, as in S06/S08), before the container's `python --version` is typed.
1. The TEAL terminal shrinks to a 3-row strip (lines 20 and 25 stay). Above it the V1 teaser: at left a
   GREEN recipe card holding generate_text/Dockerfile · line 2 (`3.14` pulses); at right the BLUE
   "Docker Hub" shelf (illustration) with the sealed TEAL box, the PINK signpost
   dlops/mega-pipeline-generate-text:latest aiming at it and a GREY chip "pushed 2025-02-18";
   "3.8.17" pulses in the strip with the box; a YELLOW "?" pulses between card and box.
2. Cut. A 6-row laptop terminal (its prompt student@laptop:~/AC215/port_toy$ waiting) along the
   bottom; above it a GREY laptop glyph at left and two TEAL boxes, gateway (low) and processor
   (high, a door ":9200" on its left wall). `curl --max-time 3 http://localhost:9200/health` -> port-laptop/23
   line 2 RED, while a dashed PINK arrow from the laptop to the door turns RED, gets a cross and a
   RED dot bounces back. `docker exec gateway curl http://processor:9200/health` -> 24: "…", 5;
   a PINK arrow labelled "processor" grows from gateway to the door, and it and "ok" turn GREEN.
3. Both pictures become glyph-only thumbnails (left: shelf, box, signpost; right: the two boxes
   and the laptop), each pulsing as its question writes in under it, 26 pt YELLOW, "Part 1" over
   "Where did that image come from?" and "Part 2" over "Whose localhost is it?".
4. The questions clear. Layout preview: the tracker ("README › Get the Code · starting fresh", 2
   dots) in a pulsing YELLOW ring; the code panel transcribe_audio/docker-shell.sh · lines 7–8
   slides in, its header ringed; a 5-row laptop strip (GREY tag "preview") types `git clone
   --branch flexible-workflow https://github.com/dlops-io/mega-pipeline.git` (folds) + ▶ your
   turn, then, at the repo prompt, `git branch; git log --oneline -1` + extra (5 rows: the README
   clone folds onto 3).
5. The preview clears. Checklist card (28 pt rows): "every command:" + the guide path (GREY), then
   "part 1: Tutorial 0 + a Google Cloud project with billing" over "+ gcloud logged in" (GREEN
   tick, GOLD coin), "part 2: only Docker" (GREEN tick).
6. GREY card "recorded 14 October 2026 · Linux" over the panel port-laptop/00-env.txt lines 4–5
   ("docker version · docker compose version"), "engine 29.8.2" pulses and the GREY tag "at the
   time of recording" appears; two GREY chips (a tiny prompt glyph each): "macOS: zsh, % · some
   messages worded differently", "Windows: Git BASH"; a GREY note "the commands and ports: the
   same" with a GREEN tick.
7. A dashed BLUE cloud with a GREY cross, caption "no Google account · no key in this recording";
   three GREY chips write in as named: "the command" · "the real no-key error" · "with your key,
   look for". Everything fades to an empty frame.
"""

import numpy as np
from common import (
    CLOUD,
    COST,
    CTR,
    ERR,
    INK,
    LAPTOP,
    LOOKUP,
    NARRATION,
    P_REPO,
    P_TOY,
    P_WS,
    TURN,
    VENV,
    BuildOrPull,
    bare_prompt,
    beside,
    capture,
    door,
    enter_container,
    extra_tag,
    grey_tag,
    log_panel,
    note,
    p_comp,
    pin,
    preview_tag,
    recorded_tag,
    resize,
    split_prompt,
    src_panel,
    term,
    tracker,
    type_cmd,
    under,
    your_turn,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    DashedLine,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    Polygon,
    RoundedRectangle,
    Text,
    Transform,
    VGroup,
    VMobject,
    Write,
    there_and_back,
)

from explainer import style as S
from explainer.devops import (
    box,
    check_mark,
    chip,
    cloud,
    cross_mark,
    label,
    laptop,
    mono,
    substring,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real captures
RUN = capture("76", "mega-laptop")                    # 76-run-registry-b.txt
assert RUN.cmd == "./docker-shell.sh run", RUN.cmd
assert RUN.line(4).startswith("Local image not found"), RUN.line(4)
assert RUN.line(20) == "Python 3.8.17", RUN.line(20)
assert RUN.line(24).strip() == "from google import genai", RUN.line(24)
assert RUN.line(25).startswith("ImportError: cannot import name 'genai' from 'google'"), RUN.line(25)
P_GEN = p_comp("generate_text")
CURL = capture("23", "port-laptop")                   # 23-curl-9200.txt
assert CURL.cmd == "curl --max-time 3 http://localhost:9200/health", CURL.cmd
assert CURL.line(2).startswith("curl: (7) Failed to connect to localhost:9200"), CURL.line(2)
EXEC = capture("24", "port-laptop")                   # 24-exec-processor.txt
assert EXEC.cmd == "docker exec gateway curl http://processor:9200/health", EXEC.cmd
assert EXEC.line(5) == "ok", EXEC.line(5)
ENV = capture("00", "port-laptop")                    # 00-env.txt
assert ENV.line(2).startswith("2026-10-14") and ENV.line(3).startswith("Linux"), ENV.lines[:2]
assert "engine 29.8.2" in ENV.line(4) and ENV.line(5) == "Docker Compose version v5.6.0", ENV.lines
CLONE = capture("01", "mega-laptop")                  # 01-clone.txt (the README's command)
assert CLONE.cmd == "git clone --branch flexible-workflow https://github.com/dlops-io/mega-pipeline.git"
BRANCH = capture("03", "mega-laptop")                 # 03-x-branch.txt (extra)
assert BRANCH.cmd == "git branch; git log --oneline -1", BRANCH.cmd

TAG_NAME = "dlops/mega-pipeline-generate-text:latest"
GUIDE = "MLOps_Learning · guides/L04-containers-2b-flexible-workflow-ports.md"
Q1 = ("Part 1", "Where did that image come from?")
Q2 = ("Part 2", "Whose localhost is it?")


# ------------------------------------------------------------------ small helpers
def clear_stage(scene, *anims, run_time: float = 0.6):
    """Fade out everything on screen (together with `anims`), then drop it from the scene."""
    old = list(scene.mobjects)
    if old:
        scene.play(FadeOut(Group(*old)), *anims, run_time=run_time)
        scene.remove(*old)
    elif anims:
        scene.play(*anims, run_time=run_time)


def above_right(tg: VGroup, t) -> VGroup:
    """Sit tag tg just above terminal t's top-right corner."""
    return tg.next_to(t.box, UP, buff=0.12).align_to(t.box, RIGHT).shift(LEFT * 0.2)


def glyph_copy(m) -> VGroup:
    """A copy of m without any text (shapes and colours only: a thumbnail)."""
    c = m.copy()

    def strip(x):
        for s in list(x.submobjects):
            if isinstance(s, Text) or hasattr(s, "pt"):
                x.remove(s)
            else:
                strip(s)
    strip(c)
    return c


def pulse(m, color: str = TURN, k: float = 1.08):
    """A there-and-back emphasis for shapes: strokes take `color` and the shape grows a little;
    fills stay (Indicate would paint a filled frame solid)."""
    return m.animate(rate_func=there_and_back).scale(k).set_stroke(color)


def text_span(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of substring `sub` of a Text built from string `s` (spaces have no glyphs)."""
    i = s.index(sub)
    a, n = len("".join(s[:i].split())), len("".join(sub.split()))
    return VGroup(*t[a:a + n])


def recipe_holder(panel, color: str = VENV, pad: float = 0.3, fold: float = 0.26) -> VGroup:
    """The GREEN recipe card (folded top-right corner) holding a code panel (header included)."""
    w, h = panel.width + 2 * pad, panel.height + 2 * pad
    fr = Polygon([-w / 2, h / 2, 0], [w / 2 - fold, h / 2, 0], [w / 2, h / 2 - fold, 0], [w / 2, -h / 2, 0],
                 [-w / 2, -h / 2, 0], stroke_color=color, stroke_width=3).set_fill(color, 0.08)
    crease = VMobject(stroke_color=color, stroke_width=2).set_points_as_corners(
        [[w / 2 - fold, h / 2, 0], [w / 2 - fold, h / 2 - fold, 0], [w / 2, h / 2 - fold, 0]])
    g = VGroup(fr, crease).move_to(panel)
    g.frame = fr
    return g


def prompt_glyph(color: str = S.GREY, w: float = 0.42) -> VGroup:
    """A tiny terminal window with a '>_' prompt drawn in lines (no text)."""
    h = w * 0.72
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color=color,
                          stroke_width=2.5).set_fill(S.BG, 1)
    x0, y0 = -w * 0.28, h * 0.08
    chev = VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners(
        [[x0, y0 + h * 0.15, 0], [x0 + w * 0.13, y0, 0], [x0, y0 - h * 0.15, 0]])
    cur = Line([x0 + w * 0.2, y0 - h * 0.2, 0], [x0 + w * 0.42, y0 - h * 0.2, 0], color=color,
               stroke_width=2.5)
    return VGroup(fr, chev, cur)


def coin_glyph(r: float = 0.17, color: str = COST) -> VGroup:
    """A GOLD coin (billing): a disc with an inner ring."""
    outer = Dot(radius=r, color=color, fill_opacity=0.35).set_stroke(color, 2.5, opacity=1)
    inner = RoundedRectangle(width=r * 1.1, height=r * 1.1, corner_radius=r * 0.55, stroke_color=color,
                             stroke_width=2)
    return VGroup(outer, inner)


def icon_chip(icon, s: str, color: str = S.GREY, size: float = 22) -> VGroup:
    """A GREY chip holding a small glyph and a short serif text. .box .text .icon"""
    t = label(s, size, INK)
    row = VGroup(icon, t).arrange(RIGHT, buff=0.18)
    h = max(row.height, mono("|", size).height) + 0.26
    b = box(row.width + 0.5, h, color, fill_opacity=0.12, radius=h / 2.6)
    row.move_to(b)
    g = VGroup(b, row)
    g.box, g.text, g.icon = b, t, icon
    return g


def question(part: tuple[str, str]) -> VGroup:
    """'Part 1' over 'Where did that image come from?', 26 pt YELLOW."""
    return VGroup(label(part[0], 26, TURN), label(part[1], 26, TURN)).arrange(DOWN, buff=0.14)


def route_arrow(a, b, color: str = LOOKUP) -> Arrow:
    """A PINK route arrow (house stroke)."""
    return Arrow(a, b, buff=0, color=color, stroke_width=5, max_tip_length_to_length_ratio=0.12)


# ------------------------------------------------------------------ the port_toy picture (beat 2)
def toy_picture():
    """The laptop (GREY, left), gateway (TEAL, low) and processor (TEAL, high) with its door
    ":9200" on its left wall. Returns (shapes, texts, parts dict)."""
    pr = box(3.0, 1.45, CTR, fill_opacity=0.07).move_to([4.15, 2.3, 0])
    pr_n = mono("processor", 22, CTR).move_to(pr.get_corner(UP + LEFT) + np.array([0.55, -0.3, 0]),
                                              aligned_edge=LEFT)
    dr = door(0.32, 0.5, CTR).move_to([pr.get_left()[0], pr.get_center()[1] - 0.2, 0])
    dr_l = mono(":9200", 22, CTR).next_to(dr, RIGHT, buff=0.12)
    gw = box(2.8, 1.05, CTR, fill_opacity=0.07).move_to([-0.35, 0.75, 0])
    gw_n = mono("gateway", 22, CTR).move_to(gw)
    lp = laptop(1.35, LAPTOP)
    lp.shift(np.array([-5.05, dr.get_center()[1], 0]) - lp.screen.get_center())
    lp_l = label("your laptop", 22, LAPTOP).next_to(lp, DOWN, buff=0.14)
    shapes = VGroup(lp, gw, pr, dr)
    texts = VGroup(lp_l, gw_n, pr_n, dr_l)
    return shapes, texts, {"laptop": lp, "gateway": gw, "processor": pr, "door": dr, "door_label": dr_l}


# ------------------------------------------------------------------ the scene
class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)

        # ========================================================== 0. the stale image
        t = term(P_GEN, rows=13)
        nolocal = above_right(grey_tag("no local image of generate_text"), t)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(t), run_time=0.6)
            type_cmd(self, t, RUN.cmd, type_time=0.9)
            vo.wait_until("on a laptop that never")
            self.play(FadeIn(nolocal, shift=DOWN * 0.1), run_time=0.5)
            t.print(self, RUN.at((2, 3)), wrap=True, run_time=0.5)
            vo.wait_until("with no local image")
            t.print(self, [(RUN.line(4), TURN)], wrap=True, run_time=0.5)
            vo.wait_until("it pulls one")
            t.print(self, RUN.at(5, "…", (15, 16)), wrap=True, run_time=0.9)
            vo.wait_until("Inside, Python")
            # inside the container now: TEAL frame, title "container · generate_text" (as in S06/S08);
            # the prompt is the capture's own pipenv prompt, not CTR_PROMPT's
            self.play(*enter_container(t, "generate_text", split_prompt(RUN.line(19))[0]), run_time=0.4)
            type_cmd(self, t, RUN.typed(19), type_time=0.6)
            l20 = t.print(self, [(RUN.line(20), TURN)], run_time=0.4)[0]
            vo.wait_until("and the Gemini")
            t.set_prompt(split_prompt(RUN.line(21))[0])
            type_cmd(self, t, RUN.typed(21), type_time=0.6)
            tb = t.print(self, RUN.at((22, 24)), run_time=0.4)
            l25 = t.print(self, [(RUN.line(25), ERR)], wrap=True, run_time=0.4)
            genai = substring(l25[0], "genai")
            ul = under(genai, TURN)
            pin(self, l25[0], ul, anim=Create(ul), run_time=0.4)
            gem = beside(grey_tag("the Gemini library"), t, tb[2])
            pin(self, tb[2], gem, run_time=0.4)

        # ========================================================== 1. recipe card vs. frozen box
        panel = src_panel("mega-pipeline/generate_text/Dockerfile", 2)
        card = recipe_holder(panel)
        cardg = VGroup(card, panel)
        cardg.move_to([-6.45 + cardg.width / 2, 0.8, 0])
        v1 = BuildOrPull(tag_name=TAG_NAME, show=("hub", "hub_tag", "box", "post", "pointer"))
        v1.shift(np.array([6.42 - v1.parts["hub_tag"].get_right()[0], 0.8, 0]))
        stick_x = v1.post[-1].get_center()[0]
        # the date chip hangs between the signpost's stick and its pointer, above the box
        pushed = chip("pushed 2025-02-18", S.GREY, size=20, pad_x=0.14)
        y_c = (v1.box.get_top()[1] + v1.post.board.get_bottom()[1]) / 2
        ps, pe = v1.pointer.get_start(), v1.pointer.get_end()
        x_ptr = ps[0] + (pe[0] - ps[0]) * (ps[1] - y_c) / (ps[1] - pe[1])
        pushed.move_to([(stick_x + x_ptr) / 2, y_c, 0])
        assert pushed.get_left()[0] > stick_x + 0.05 and pushed.get_right()[0] < x_ptr - 0.05
        gap_l, gap_r = cardg.get_right()[0], v1.hub_shelf.get_left()[0]
        qm = label("?", 72, TURN).move_to([(gap_l + gap_r) / 2, cardg.get_center()[1], 0])
        assert qm.get_left()[0] > gap_l + 0.1 and qm.get_right()[0] < gap_r - 0.1, (gap_l, gap_r, qm.width)
        v1_pic = VGroup(v1.hub_shelf, v1.box, v1.post, v1.pointer)     # for the thumbnail (beat 3)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(nolocal), run_time=0.3)
            self.remove(nolocal)
            resize(self, t, 3, keep=[l20, l25[0], l25[1]], run_time=0.7)
            self.play(FadeIn(cardg, shift=RIGHT * 0.4), run_time=0.7)
            vo.wait_until("says Python 3.14")
            self.play(Indicate(panel.span(2, "3.14"), color=TURN, scale_factor=1.3), run_time=0.8)
            vo.wait_until("This image was built")
            self.play(FadeIn(v1, shift=LEFT * 0.3), run_time=0.8)
            vo.wait_until("in February 2025")
            self.play(FadeIn(pushed, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("with Python 3.8")
            self.play(Indicate(substring(l20, "3.8.17"), color=TURN, scale_factor=1.25),
                      pulse(v1.box, TURN, 1.06), run_time=0.9)
            vo.wait_until("Where did it come from")
            self.play(Write(qm), run_time=0.5)
            self.play(qm.animate(rate_func=there_and_back).scale(1.3), run_time=0.7)

        # ========================================================== 2. whose localhost?
        shapes, texts, P = toy_picture()
        net = VGroup(shapes, texts)
        t2 = term(P_TOY, rows=6)
        dr = P["door"]
        y_d = dr.get_center()[1]
        a0 = np.array([P["laptop"].get_right()[0] + 0.12, y_d, 0])
        a1 = np.array([dr.get_left()[0] - 0.08, y_d, 0])
        lap_arrow = DashedLine(a0, a1, color=LOOKUP, stroke_width=4, dash_length=0.14)
        # the cross sits on the dashed route well before the door, clear of the gateway's arrowhead,
        # which lands on the door's lower-left corner
        no_cross = cross_mark(0.3, ERR).move_to(a1 + LEFT * 0.45)
        back = Dot(a1, radius=0.08, color=ERR)
        gw = P["gateway"]
        g_arrow = route_arrow(gw.get_right() + np.array([0.08, 0.2, 0]), dr.get_corner(DOWN + LEFT) + np.array([-0.04, 0.04, 0]))
        assert g_arrow.get_top()[1] < no_cross.get_bottom()[1] - 0.04 or \
            g_arrow.get_right()[0] > no_cross.get_right()[0] + 0.1, "arrowhead touches the cross"
        g_lab = mono("processor", 22, LOOKUP).next_to(g_arrow.point_from_proportion(0.4), UP + LEFT, buff=0.1)

        with self.voiceover(SAY[2]) as vo:
            clear_stage(self, run_time=0.4)
            self.play(FadeIn(t2), FadeIn(net, lag_ratio=0.1), run_time=1.0)
            bare_prompt(self, t2)                    # the prompt waits while the picture is named
            vo.wait_until("a server listening")
            self.play(pulse(dr, TURN, 1.15), Indicate(P["door_label"], color=TURN, scale_factor=1.1), run_time=0.8)
            type_cmd(self, t2, CURL.cmd, type_time=1.4)
            vo.wait_until("The laptop can't reach it")
            self.play(Create(lap_arrow), run_time=0.6)
            out = t2.print(self, [(CURL.line(2), ERR)], run_time=0.3)[0]
            self.play(lap_arrow.animate.set_color(ERR), FadeIn(no_cross, scale=0.6),
                      MoveAlongPath(back, Line(a1, a0)), run_time=0.8)
            self.remove(back)
            del out
            vo.wait_until("another container, asking")
            type_cmd(self, t2, EXEC.cmd, type_time=1.3)
            self.play(GrowArrow(g_arrow), FadeIn(g_lab), run_time=0.7)
            vo.wait_until("gets a reply")
            ok = t2.print(self, EXEC.at("…", 5), run_time=0.4)[1]
            self.play(ok.animate.set_color(VENV), g_arrow.animate.set_color(VENV),
                      pulse(dr, VENV, 1.3), run_time=0.7)

        # ========================================================== 3. two puzzles
        thumb_l = glyph_copy(v1_pic)
        y_th = 0.85                                   # thumbnails over questions, centred in the frame
        thumb_l.scale(min(4.6 / thumb_l.width, 2.3 / thumb_l.height)).move_to([-3.3, y_th, 0])
        net_shapes = VGroup(shapes, lap_arrow, no_cross, g_arrow)
        k_r = min(5.8 / net_shapes.width, 2.3 / net_shapes.height)
        q1 = question(Q1).move_to([-3.3, -1.35, 0])
        q2 = question(Q2).move_to([3.4, -1.35, 0]).align_to(q1, UP)

        with self.voiceover(SAY[3]) as vo:
            self.add(net_shapes)
            drop = VGroup(texts, g_lab)
            # the labels shrink with their shapes while they fade (no label left floating mid-move)
            c_net = net_shapes.get_center()
            pic = VGroup(net_shapes, drop)
            pic_end = pic.copy().scale(k_r, about_point=c_net).shift(np.array([3.4, y_th, 0]) - c_net)
            pic_end[1].set_opacity(0)
            self.play(FadeOut(t2), Transform(pic, pic_end), run_time=0.8)
            pic.remove(drop)
            self.remove(t2, pic, drop, texts, g_lab)
            net.remove(texts)
            self.add(net_shapes)
            self.play(FadeIn(thumb_l, scale=1.4), run_time=0.5)
            vo.wait_until("Part 1")
            self.play(Write(q1), pulse(thumb_l), run_time=1.0)
            vo.wait_until("and should you build")
            self.play(thumb_l.animate(rate_func=there_and_back).shift(UP * 0.15), run_time=0.7)
            vo.wait_until("Part 2")
            self.play(Write(q2), pulse(net_shapes), run_time=1.0)

        # ========================================================== 4. how to follow along
        tr = tracker("F")
        x0, y0 = -6.59, 3.59
        x1, y1 = tr.get_right()[0] + 0.18, tr.get_bottom()[1] - 0.14
        ring_ = RoundedRectangle(width=x1 - x0, height=y0 - y1, corner_radius=0.12, stroke_color=TURN,
                                 stroke_width=3).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        code = src_panel("mega-pipeline/transcribe_audio/docker-shell.sh", 7, 8)
        code.shift(np.array([-6.3 - code.get_left()[0], 2.15 - code.get_top()[1], 0]))
        # ring the header without touching the panel below it (the gap is only 0.1)
        hx0, hx1 = code.header.get_left()[0] - 0.1, code.header.get_right()[0] + 0.1
        hy0, hy1 = code.header.get_bottom()[1] - 0.035, code.header.get_top()[1] + 0.08
        head_ring = RoundedRectangle(width=hx1 - hx0, height=hy1 - hy0, corner_radius=0.08, stroke_color=TURN,
                                     stroke_width=3).move_to([(hx0 + hx1) / 2, (hy0 + hy1) / 2, 0])
        assert head_ring.get_bottom()[1] > code.code.get_top()[1] + 0.05
        t4 = term(P_WS, rows=5)
        prev = above_right(preview_tag(), t4)

        with self.voiceover(SAY[4]) as vo:
            clear_stage(self, FadeIn(tr, shift=DOWN * 0.2), run_time=0.7)
            self.play(Create(ring_), run_time=0.5)
            for _ in range(2):
                self.play(ring_.animate(rate_func=there_and_back).set_stroke(width=7), run_time=0.6)
            vo.wait_until("code panels show")
            self.play(FadeOut(ring_), FadeIn(code, shift=RIGHT * 0.6), run_time=0.8)
            self.remove(ring_)
            vo.wait_until("file and line numbers")
            self.play(Create(head_ring), run_time=0.6)
            vo.wait_until("Pause at the yellow")
            self.play(FadeOut(head_ring), FadeIn(t4), FadeIn(prev), run_time=0.5)
            self.remove(head_ring)
            cl = type_cmd(self, t4, CLONE.cmd, type_time=1.0)
            pin(self, cl, beside(your_turn(), t4, cl))
            vo.wait_until("gray extra tags")
            t4.set_prompt(P_REPO)
            br = type_cmd(self, t4, BRANCH.cmd, type_time=0.7)
            xt = pin(self, br, beside(extra_tag(), t4, br))
            vo.wait_until("the README doesn't have")
            self.play(pulse(xt, S.WHITE, 1.15), run_time=0.8)

        # ========================================================== 5. what you need
        foot = VGroup(label("every command:", 26, S.GREY), mono(GUIDE, 21, S.GREY)) \
            .arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        rows = VGroup()
        texts5 = [("part 1: Tutorial 0 + a Google Cloud project with billing", "+ gcloud logged in"),
                  ("part 2: only Docker", None)]
        for s, s2 in texts5:
            slot = box(0.42, 0.42, S.GREY, fill_opacity=0.0, radius=0.07, stroke=2)
            mark = check_mark(0.4, VENV).move_to(slot)
            line1 = label(s, 28, INK).next_to(slot, RIGHT, buff=0.32)
            words = VGroup(line1)
            if s2:
                words.add(label(s2, 28, INK).next_to(line1, DOWN, buff=0.18, aligned_edge=LEFT))
            r = VGroup(slot, mark, words)
            r.slot, r.mark, r.text, r.line1 = slot, mark, words, line1
            rows.add(r)
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        coin = coin_glyph(0.19).next_to(rows[0].line1, RIGHT, buff=0.25)
        body = VGroup(foot, VGroup(rows, coin)).arrange(DOWN, buff=0.65, aligned_edge=LEFT)
        frame5 = box(body.width + 0.9, body.height + 0.8, S.GREY, fill_opacity=0.04).move_to(body)
        VGroup(frame5, body).move_to([0, 0.2, 0])
        assert frame5.get_left()[0] > -6.6 and frame5.get_right()[0] < 6.6, frame5.width
        billing = text_span(rows[0].line1, texts5[0][0], "with billing")

        def tick(r):
            return AnimationGroup(Create(r.mark), FadeIn(r.text, shift=RIGHT * 0.15))

        with self.voiceover(SAY[5]) as vo:
            clear_stage(self, run_time=0.4)
            self.play(FadeIn(frame5), *[Create(r.slot) for r in rows], FadeIn(foot, shift=UP * 0.15),
                      run_time=0.8)
            self.play(Indicate(foot[1], color=TURN, scale_factor=1.04), run_time=0.8)
            vo.wait_until("Part 1 needs")
            self.play(tick(rows[0]), run_time=0.8)
            vo.wait_until("with billing")
            self.play(FadeIn(coin, scale=0.5), Indicate(billing, color=COST, scale_factor=1.08), run_time=0.7)
            vo.wait_until("part 2 needs only")
            self.play(tick(rows[1]), run_time=0.8)

        # ========================================================== 6. what we recorded on
        env = log_panel(ENV.at(4, 5), "docker version · docker compose version", width=10.6)
        head6 = label("recorded 14 October 2026 · Linux", 24, S.GREY)
        inner6 = VGroup(head6, env).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        frame6 = box(inner6.width + 0.7, inner6.height + 0.6, S.GREY, fill_opacity=0.04).move_to(inner6)
        card6 = VGroup(frame6, inner6).move_to([0, 1.55, 0])
        engine = substring(env.rows[0], "engine 29.8.2")
        rec = recorded_tag().move_to(env.header).align_to(env.frame, RIGHT)
        rec.shift(UP * (env.frame.get_top()[1] + 0.05 - rec.get_bottom()[1]))     # clear of the panel's edge
        c_mac = icon_chip(prompt_glyph(), "macOS: zsh, % · some messages worded differently")
        c_win = icon_chip(prompt_glyph(), "Windows: Git BASH")
        VGroup(c_mac, c_win).arrange(RIGHT, buff=0.4).move_to([0, -0.85, 0])
        same = VGroup(check_mark(0.3, VENV), note("the commands and ports: the same", size=22)) \
            .arrange(RIGHT, buff=0.2).move_to([0, -1.85, 0])

        with self.voiceover(SAY[6]) as vo:
            clear_stage(self, run_time=0.4)
            self.play(FadeIn(card6, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("with Docker Engine")
            self.play(Indicate(engine, color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("at the time of recording")
            self.play(FadeIn(rec, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("On a Mac")
            self.play(LaggedStart(FadeIn(c_mac, shift=UP * 0.2), FadeIn(c_win, shift=UP * 0.2),
                                  lag_ratio=0.45), run_time=0.9)
            vo.wait_until("the prompt and a few")
            self.play(pulse(c_mac.icon, TURN, 1.3), pulse(c_win.icon, TURN, 1.3), run_time=0.8)
            vo.wait_until("the commands and ports")
            self.play(FadeIn(same, shift=UP * 0.15), run_time=0.6)

        # ========================================================== 7. the honest limit
        sky = DashedVMobject(cloud(5.2, CLOUD, fill_opacity=0.0), num_dashes=64, dashed_ratio=0.55)
        sky.set_stroke(CLOUD, 3).move_to([0, 1.75, 0])
        xx = cross_mark(0.9, S.GREY, stroke=7).move_to(sky.get_center() + DOWN * 0.1)
        cap7 = label("no Google account · no key in this recording", 24, S.GREY).next_to(sky, DOWN, buff=0.3)
        chips = VGroup(*[chip(s, S.GREY, size=22) for s in
                         ("the command", "the real no-key error", "with your key, look for")])
        chips.arrange(RIGHT, buff=0.45).move_to([0, -1.6, 0])
        seps = VGroup(*[label("·", 26, S.GREY).move_to((chips[i].get_right() + chips[i + 1].get_left()) / 2)
                        for i in range(2)])

        with self.voiceover(SAY[7]) as vo:
            clear_stage(self, run_time=0.5)
            self.play(Create(sky), run_time=0.9)
            vo.wait_until("we had no Google")
            self.play(Create(xx), FadeIn(cap7, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("Wherever the code")
            self.play(Indicate(sky, color=CLOUD, scale_factor=1.05), run_time=0.8)
            vo.wait_until("you'll see the command")
            self.play(FadeIn(chips[0], shift=UP * 0.2), run_time=0.5)
            vo.wait_until("the real error")
            self.play(FadeIn(seps[0]), FadeIn(chips[1], shift=UP * 0.2), run_time=0.5)
            vo.wait_until("and what to look for")
            self.play(FadeIn(seps[1]), FadeIn(chips[2], shift=UP * 0.2), run_time=0.5)

        clear_stage(self, run_time=0.8)

