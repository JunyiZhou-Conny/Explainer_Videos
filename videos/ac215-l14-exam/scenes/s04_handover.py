"""S04 · Function or container: what you hand over (AC215 L14 exam edition). Lecture: 14 · 10–12, 14–15.

Beats (script.md "## S04", one voiceover block each):
0. The exam map (slots 1, 2 filled) fades in, slot 3 activates ("3 · what you hand over") and
   pulses; lref(14, "10"). At "The lecture deploys" V3 builds: the GREEN "Simple Translate App"
   block, its four arrows, the 2×2 grid (rows virtual machine / serverless, columns a code file /
   a container). At "Earlier lectures" the VM cells tick with GREY "Lecture 1" / "Lecture 2"
   chips; at "Today fills" the two serverless cells light YELLOW.
1. lref(14, "11–12"). The serverless-file cell zooms open (the grid goes). The three GREEN items
   (main.py, requirements.txt, the name tag "entry point: hello_http") slide in as a row along the
   top. At "The file is main.py" CODE(tutorial/function/main.py: 7–12); at "an HTTP handler" line 7
   lit PURPLE, line 8 lit GREEN; at "which reads the text" lines 9–11 lit PINK. Then
   CODE(tutorial/function/requirements.txt: 1–2) under it.
2. The requirements panel goes; CODE(README.md: 150–151) comes in under main.py. The name tag
   pulses, a PINK copy of its name flies onto line 8's `hello_http` (both ringed PINK). At "Not the
   file name" "not the filename or service name" is underlined YELLOW.
3. The panels go; the items return to the BuildLine column. At "Cloud Build installs" they flow
   into the PURPLE Cloud Build box, a TEAL image comes out (excerpt chip README.md line 214); at
   "and publishes an image" it drops onto the BLUE Artifact Registry shelf (chip line 215), and the
   dashed BLUE instance runs it: the PURPLE functions-framework reaches for `def hello_http` (GREEN
   arrow). At "This happens once" the chip of line 216 "at build time, not on every request".
4. The chips go; the call arrow pulses. At "Type main" the tag flips to "entry point: main", the
   arrow snaps RED; at "and there is nothing" `def hello_http` flashes RED (nothing called main);
   at "The function build fails" the RED "function build failed" chip; at "and its build logs" the
   excerpt chip README.md line 1038 "Build logs, runtime, requirements, entry point". The tag flips
   back to hello_http, GREEN again.
5. A GREY slide-11 chip "…without managing servers or containers"; at "You do not manage one"
   "managing" is underlined YELLOW; at "but Google still builds one" a TEAL container outline fades
   in around the running function ("a container, built for you"). At "And the slides" the GREY
   chip "Cloud Function" (slides 11–12) with an arrow to the excerpt chip README.md line 99 "Cloud
   Run → Services and select Write a function".
6. Everything but the map goes; lref(14, "14–15"). The serverless-container cell zooms open: the
   PINK image URL chip; at "Deploying it builds nothing" an arrow straight to a dashed BLUE revision
   (TEAL "your image" inside) past a GREY struck-out "Cloud Build"; at "the image was built
   beforehand" the excerpt chip README.md lines 273–274 "Deploy one revision from an existing
   container image". At "Its Dockerfile picks" CODE(tutorial/app/Dockerfile: 1, 2, 11, 12 folded),
   line 1 lit ORANGE; at "the default port" line 2 lit GREEN and the ear "listening on :8080"; at
   "and the startup command" line 12 lit GREEN (line 11 EXPOSE stays unlit); at "You control all
   three" the three lit lines pulse.
7. The service's revision moves right; the function's instance comes back on the left. Each gets a
   PINK "HTTPS URL" chip with an arrow. At "The function takes new inputs" the function's chip
   becomes the excerpt chip README.md line 163 (the query string) and CODE(main.py: 9–11) comes in
   under the instances; text=, src=, dest= light in turn and PINK copies fly into lines 9–11. At
   "with no redeploy" `fr` becomes `el` (no build animation; the header says "dest changed as line
   166 says") and the excerpt chip README.md line 171
   "the same endpoint accepts different inputs without a redeploy" replaces the panel.
8. The two instances slide together into one dashed BLUE instance with a TEAL container; at "A
   function is a container" the caption; at "On the quiz" the GREEN exam-rule card (line 1), at
   "Your own image" line 2; it shrinks into map slot 3. Everything fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    VGroup,
    Write,
)

from explainer import style as S
from explainer.scene import VoiceScene

from common import (
    CAPTION,
    CLOUD,
    CTR,
    ERR,
    IMAGE,
    INK,
    NARRATION,
    OWN,
    ROUTE,
    SAFE_X,
    SAFE_Y,
    SYSTEM,
    TOOL,
    TURN,
    BuildLine,
    ExamMap,
    HandoverGrid,
    RuleCard,
    _arrow,
    _save_op,
    _set_op,
    chip,
    ear_chip,
    excerpt_chip,
    guard,
    instance_box,
    late_in,
    label,
    lref,
    lref_swap,
    mono,
    ring,
    source_line,
    src_panel,
    strike,
    under,
    swap_text,
    url_chip,
)

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ the real sources (checked)
README = "README.md"
MAIN = "tutorial/function/main.py"
REQS = "tutorial/function/requirements.txt"
DOCKER = "tutorial/app/Dockerfile"
assert source_line(MAIN, 7).strip() == "@functions_framework.http"
assert source_line(MAIN, 8).strip() == "def hello_http(request):"
assert all("request.args.get" in source_line(MAIN, n) for n in (9, 10, 11))
assert source_line(REQS, 1).startswith("functions-framework==")
assert "Function entry point" in source_line(README, 150) and "hello_http" in source_line(README, 150)
assert "not the filename or service name" in source_line(README, 151)
B214 = "configures the Functions Framework, and publishes an application"
B215 = "image in Artifact Registry"
B216 = "at build time, not on every request"
assert B214 in source_line(README, 214) and B215 in source_line(README, 215)
assert B216 in source_line(README, 216)          # "**build time**" (the loader drops the "**")
LOGS = "Build logs, runtime, requirements, entry point"
assert "Function build fails" in source_line(README, 1038) and LOGS in source_line(README, 1038)
CONSOLE = "Cloud Run → Services and select Write a function"
assert CONSOLE in source_line(README, 99)
L273, L274 = source_line(README, 273), source_line(README, 274)
DEPLOY = "Deploy one revision from an existing container image"
assert DEPLOY in L273.strip() + " " + L274.strip()
assert source_line(DOCKER, 1).strip() == "FROM python:3.12-slim-bookworm"
assert "PORT=8080" in source_line(DOCKER, 2)
assert source_line(DOCKER, 11).strip() == "EXPOSE 8080"
assert source_line(DOCKER, 12).startswith("CMD ")
QUERY = "?text=Good%20afternoon%20everyone&src=en&dest=fr"
assert QUERY in source_line(README, 163)
assert "`dest=fr` to `dest=el`" in source_line(README, 166)
SAME = "the same endpoint accepts different inputs without a redeploy"
assert SAME in source_line(README, 171)

# the lecture's own words (deck text: slide 11 bullet, slides 11-12 product name)
SLIDE11 = "without managing servers or containers"

RULE_TOP = "source + requirements + entry point → function (Google builds the image)"
RULE_BOTTOM = "your image · OS libraries · startup command → Cloud Run service"

TOP_BAND = 2.55          # content stays below the active slot's label


def inside_frame(*mobs):
    for m in mobs:
        guard(m.get_left()[0] >= -SAFE_X - 1e-6 and m.get_right()[0] <= SAFE_X + 1e-6,
              f"x out of frame: {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f}")
        guard(m.get_bottom()[1] >= -SAFE_Y - 1e-6 and m.get_top()[1] <= SAFE_Y + 1e-6,
              f"y out of frame: {m.get_bottom()[1]:.2f}..{m.get_top()[1]:.2f}")


def below_band(*mobs):
    for m in mobs:
        guard(m.get_top()[1] <= TOP_BAND + 1e-6, f"reaches the map's label: top {m.get_top()[1]:.2f}")


def apart(a, b, gap: float = 0.05):
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    guard(sep, f"overlap: {a.get_corner(DOWN + LEFT)} {a.get_corner(UP + RIGHT)} / "
               f"{b.get_corner(DOWN + LEFT)} {b.get_corner(UP + RIGHT)}")


def hide_now(piece, *names):
    """Start these shown-by-default parts of a set piece invisible (revealed later with parts_in)."""
    for n in names:
        m = piece.parts[n]
        _save_op(m)
        _set_op(m, 0)
        piece._flag(m, True)


def text_glyphs(t, s: str, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of `sub` in a one-line Text `t` built from string `s` (spaces have no glyphs)."""
    i = -1
    for _ in range(occurrence + 1):
        i = s.find(sub, i + 1)
    assert i >= 0, (sub, s)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def slide_chip(text: str, where: str):
    """A GREY lecture chip: the slide's words in quotes, then the slide number(s)."""
    s = f"“{text}” · {where}"
    c = chip(s, S.GREY, size=CAPTION)
    c.s = s
    return c


def zoom_out_of(cell, target_w: float = 12.8, target_h: float = 4.6, y: float = -0.4):
    """The grid cell grows into the work area and fades (the 'zoom open')."""
    z = cell.copy()
    z.set_stroke(TURN, 3)
    tgt = cell.copy().set_stroke(TURN, 3, opacity=0)
    for sm in tgt.get_family():
        sm.set_fill(opacity=0)
    tgt.stretch_to_fit_width(target_w).stretch_to_fit_height(target_h).move_to([0, y, 0])
    return z, tgt


class WhatYouHandOver(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0. four ways to deploy one app
        m = ExamMap(filled=(1, 2))
        lr = lref(14, "10")
        hg = HandoverGrid()
        hide_now(hg, "arrows", "cells", "heads")
        heads = hg.parts["heads"]          # 0 a code file, 1 a container, 2 virtual machine, 3 serverless
        inside_frame(hg)
        below_band(hg)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(m), FadeIn(lr), run_time=0.6)
            self.play(*m.activate(3), run_time=0.5)
            self.play(m.pulse(3), run_time=0.8)
            vo.wait_until("The lecture deploys")
            self.play(FadeIn(hg.parts["app"], shift=RIGHT * 0.2), run_time=0.6)
            self.play(*hg.parts_in("arrows", anim=Create), run_time=1.0)
            self.play(*hg.parts_in("cells", "heads"), run_time=0.8)
            vo.wait_until("virtual machine or serverless")
            self.play(Indicate(VGroup(heads[2], heads[3]), color=CLOUD, scale_factor=1.08), run_time=0.8)
            vo.wait_until("code file or container")
            self.play(Indicate(VGroup(heads[0], heads[1]), color=INK, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Earlier lectures")
            self.play(*hg.tick(0, 0, "Lecture 1"), *hg.tick(0, 1, "Lecture 2"), run_time=0.8)
            vo.wait_until("Today fills")
            self.play(*hg.light(1, 0), *hg.light(1, 1), run_time=0.6)
            self.play(Indicate(heads[3], color=TURN, scale_factor=1.12), m.pulse(3), run_time=vo.remaining(0.6))

        # ========================================================== 1. a function: three things you hand over
        bl = BuildLine(show=("items",))
        items = bl.parts["items"]
        home_pos = items.copy().arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        home_pos.move_to(items.get_center())     # (the column BuildLine built, for beat 3)
        f_main, f_req, tag = items[0], items[1], bl.tag
        # the items as a row along the top while the panels are up (back to the column in beat 3)
        items.arrange(RIGHT, buff=0.5, center=False, aligned_edge=DOWN)
        items.move_to([-6.45 + items.width / 2, 2.17, 0])
        hide_now(bl, "items")
        pmain = src_panel(MAIN, 7, 12, size=20)
        pmain.move_to([-6.45 + pmain.width / 2, 1.8 - pmain.height / 2, 0])
        preq = src_panel(REQS, 1, 2, size=20)
        preq.move_to([-6.45 + preq.width / 2, pmain.get_bottom()[1] - 0.12 - preq.height / 2, 0])
        inside_frame(items, pmain, preq)
        below_band(items)
        apart(items, pmain, 0.04)
        apart(pmain, preq, 0.05)
        bars7 = pmain.bar(7, TOOL, 0.22)
        bars8 = pmain.bar(8, OWN, 0.22)
        bars911 = VGroup(*[pmain.bar(n, ROUTE, 0.2) for n in (9, 10, 11)])
        z, ztgt = zoom_out_of(hg.parts["cells"][2])
        with self.voiceover(SAY[1]) as vo:
            lr = lref_swap(self, lr, 14, "11–12")
            self.add(z)
            self.play(FadeOut(hg), z.animate.become(ztgt), run_time=0.9)
            self.remove(z)
            self.add(bl)
            bl.parts_in("items")          # (flags and opacity back; each item fades in below)
            self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.15) for x in (f_main, f_req, tag)],
                                  lag_ratio=0.5), run_time=1.6)
            vo.wait_until("The file is main.py")
            self.play(FadeIn(pmain, shift=UP * 0.1), Indicate(f_main, color=OWN), run_time=0.7)
            vo.wait_until("an HTTP handler")
            self.play(FadeIn(bars7), run_time=0.4)
            self.play(FadeIn(bars8), Indicate(tag, color=OWN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("which reads the text")
            self.play(LaggedStart(*[FadeIn(b) for b in bars911], lag_ratio=0.4), run_time=1.0)
            self.play(FadeIn(preq, shift=UP * 0.1), Indicate(f_req, color=OWN), run_time=vo.remaining(0.6))

        # ========================================================== 2. the entry point is a function name
        p150 = src_panel(README, 150, 151, size=20)
        p150.move_to([-6.45 + p150.width / 2, pmain.get_bottom()[1] - 0.1 - p150.height / 2, 0])
        inside_frame(p150)
        apart(pmain, p150, 0.04)
        span8 = pmain.span(8, "hello_http")
        fly = tag.name.copy().set_color(ROUTE)
        r_tag = ring(tag.name, ROUTE, buff=0.07)
        r_8 = ring(span8, ROUTE, buff=0.06)
        u_a = under(p150.span(151, "not the filename or"), TURN)
        u_b = under(p150.span(151, "service name."), TURN)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(preq), run_time=0.4)
            self.play(FadeIn(p150, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(tag, color=ROUTE, scale_factor=1.08), Create(r_tag), run_time=0.7)
            self.add(fly)
            self.play(fly.animate.move_to(span8).set_opacity(0.0), run_time=1.0)
            self.remove(fly)
            self.play(Create(r_8), span8.animate.set_color(ROUTE), run_time=0.5)
            vo.wait_until("Not the file name")
            self.play(Create(u_a), Create(u_b), run_time=0.8)
            self.play(Indicate(r_8, color=ROUTE), Indicate(r_tag, color=ROUTE), run_time=vo.remaining(0.6))

        # ========================================================== 3. Google builds: once, at build time
        c214 = excerpt_chip(B214, f"{README} · line 214 (excerpt)", line=source_line(README, 214))
        c215 = excerpt_chip(B215, f"{README} · line 215 (excerpt)", line=source_line(README, 215))
        c216 = excerpt_chip(B216, f"{README} · line 216 (excerpt)", line=source_line(README, 216))
        c214.move_to([-6.45 + c214.width / 2, -1.85, 0])
        VGroup(c215, c216).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        VGroup(c215, c216).move_to([-6.45 + VGroup(c215, c216).width / 2, -3.05, 0])
        hl216 = c216.text
        inside_frame(c214, c215, c216, bl)
        for c in (c214, c215, c216):
            for k in ("items", "build", "shelf", "instance"):
                apart(c, bl.parts[k], 0.08)
        apart(c214, c215, 0.06)
        apart(c214, c216, 0.06)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(pmain, p150, bars7, bars8, bars911, u_a, u_b, r_8, r_tag)),
                      run_time=0.5)
            # one at a time (tag first, then requirements.txt, then main.py): no text crosses another
            self.play(LaggedStart(*[x.animate.move_to(home_pos[k]) for k, x in ((2, tag), (1, f_req), (0, f_main))],
                                  lag_ratio=0.7), run_time=1.2)
            vo.wait_until("Cloud Build installs")
            self.play(*bl.build(), FadeIn(c214, shift=UP * 0.1), run_time=1.8)
            vo.wait_until("and publishes an image")
            self.play(*bl.publish(), FadeIn(c215, shift=UP * 0.1), run_time=0.8)
            self.play(*bl.run(), run_time=1.2)
            vo.wait_until("This happens once")
            self.play(FadeIn(c216, shift=UP * 0.1), run_time=0.6)
            self.play(hl216.animate.set_color(TURN), Indicate(bl.parts["build"], color=TOOL, scale_factor=1.06),
                      run_time=0.8)
            self.wait(vo.remaining(0.3))

        # ========================================================== 4. the wrong name: the build fails
        c1038 = excerpt_chip(LOGS, f"{README} · line 1038 (excerpt) · Function build fails",
                             line=source_line(README, 1038))
        c1038.move_to([-6.45 + c1038.width / 2, -3.0, 0])
        inside_frame(c1038)
        apart(c1038, bl.parts["fail"], 0.08)
        apart(c1038, bl.parts["shelf"], 0.08)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(c214, c215, c216)), run_time=0.5)
            self.play(Indicate(bl.call_arrow, color=OWN, scale_factor=1.15), Indicate(tag, color=OWN), run_time=1.0)
            vo.wait_until("Type main")
            to_main = bl.set_entry("main")
            to_main = to_main[:-1]                 # (the RED chip comes at "The function build fails")
            _set_op(bl.parts["fail"], 0)
            self.play(*to_main, run_time=0.8)
            vo.wait_until("and there is nothing")
            self.play(Indicate(bl.fn_chip, color=ERR, scale_factor=1.06), run_time=0.9)
            vo.wait_until("The function build fails")
            self.play(*late_in(bl, "fail"), run_time=0.5)
            vo.wait_until("and its build logs")
            self.play(FadeIn(c1038, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.3, vo.remaining(0.3) - 1.0))
            self.play(*bl.set_entry("hello_http"), run_time=vo.remaining(0.6))

        # ========================================================== 5. no container to manage, one is still built
        s11 = slide_chip(f"…{SLIDE11}", "slide 11")
        s11.move_to([-6.45 + s11.width / 2, 1.85, 0])
        u_man = under(text_glyphs(s11.text, s11.s, "managing"), TURN)
        teal = ring(VGroup(bl.parts["framework"], bl.parts["fn"]), CTR, buff=0.1, stroke=4)
        teal_lab = label("a container, built for you", CAPTION, CTR).next_to(bl.instance, UP, buff=0.14)
        sfn = slide_chip("Cloud Function", "slides 11–12")
        sfn.move_to([-6.45 + sfn.width / 2, -1.75, 0])
        c99 = excerpt_chip(CONSOLE, f"{README} · line 99 (excerpt) · today", line=source_line(README, 99))
        c99.move_to([6.5 - c99.width / 2, -2.95, 0])
        a99 = _arrow(sfn.get_right() + RIGHT * 0.08, c99.chip.get_left() + LEFT * 0.04, S.GREY, 3, buff=0.02)
        inside_frame(s11, teal_lab, sfn, c99)
        below_band(s11, teal_lab)
        apart(s11, teal_lab)
        apart(s11, bl.parts["items"])
        apart(teal_lab, bl.parts["image"])
        guard(teal.get_top()[1] <= bl.instance.get_top()[1] + 1e-6 and
              teal.get_bottom()[1] >= bl.instance.get_bottom()[1] - 1e-6, "the TEAL container leaves the instance")
        for c in (sfn, c99):
            apart(c, bl.parts["shelf"], 0.08)
            apart(c, bl.parts["items"], 0.08)
            apart(c, bl.instance, 0.08)
        apart(sfn, c99)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(c1038), FadeIn(s11, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("You do not manage one")
            self.play(Create(u_man), run_time=0.6)
            vo.wait_until("but Google still builds one")
            self.play(Create(teal), FadeIn(teal_lab, shift=DOWN * 0.1), run_time=0.9)
            self.play(Indicate(bl.parts["build"], color=TOOL, scale_factor=1.06), run_time=0.7)
            vo.wait_until("And the slides")
            self.play(FadeIn(sfn, shift=RIGHT * 0.1), run_time=0.5)
            self.play(Create(a99), FadeIn(c99, shift=UP * 0.1), run_time=vo.remaining(0.7))

        # ========================================================== 6. a service: hand over a finished image
        z2, z2tgt = zoom_out_of(hg.parts["cells"][3])
        url = url_chip(IMAGE)
        url.move_to([-6.45 + url.width / 2, 2.1, 0])
        rev = instance_box(3.0, 1.5, inner=True).move_to([4.9, 0.55, 0])
        rev_img = label("your image", CAPTION, INK).move_to(rev.inner)
        rev_lab = label("revision", CAPTION, CLOUD).next_to(rev, LEFT, buff=0.15).align_to(rev, DOWN)
        svc = VGroup(rev, rev_img)
        a_url = _arrow(url.get_corner(DOWN + RIGHT) + LEFT * 0.35, rev.get_top() + LEFT * 0.4, ROUTE, 4)
        nob = chip("Cloud Build", S.GREY, size=CAPTION).move_to([2.3, 1.42, 0])
        nob_x = strike(nob)
        c273 = excerpt_chip(DEPLOY, f"{README} · lines 273–274 (excerpt)", line=L273.strip() + " " + L274.strip())
        c273.move_to([-6.45 + c273.width / 2, 0.5, 0])
        pdock = src_panel(DOCKER, [1, 2, 11, 12], size=20)
        pdock.move_to([-6.45 + pdock.width / 2, -0.78 - pdock.height / 2, 0])
        ear = ear_chip().next_to(rev, DOWN, buff=0.12)
        d1 = pdock.bar(1, SYSTEM, 0.25)
        d2 = pdock.bar(2, OWN, 0.22)
        d12 = pdock.bar(12, OWN, 0.22)
        inside_frame(url, rev, rev_lab, nob, c273, pdock, ear)
        below_band(url)
        for a, b in ((url, rev), (url, nob), (nob, c273), (c273, rev), (c273, rev_lab), (pdock, ear),
                     (pdock, rev), (c273, pdock), (ear, rev), (rev_lab, nob), (url, rev_lab)):
            apart(a, b, 0.04)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(s11, u_man, teal, teal_lab, sfn, a99, c99)), FadeOut(bl), run_time=0.6)
            lr = lref_swap(self, lr, 14, "14–15")
            self.add(z2)
            self.play(z2.animate.become(z2tgt), run_time=0.8)
            self.remove(z2)
            self.play(FadeIn(url, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("Deploying it builds nothing")
            self.play(FadeIn(nob), Create(a_url), run_time=0.6)
            self.play(Create(nob_x), nob.animate.set_opacity(0.5), FadeIn(svc), FadeIn(rev_lab), run_time=0.7)
            vo.wait_until("the image was built beforehand")
            self.play(FadeIn(c273, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Its Dockerfile picks")
            self.play(FadeIn(pdock, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(d1), Indicate(pdock.span(1, "python:3.12-slim-bookworm"), color=SYSTEM), run_time=0.6)
            vo.wait_until("the default port")
            self.play(FadeIn(d2), FadeIn(ear, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("and the startup command")
            self.play(FadeIn(d12), run_time=0.5)
            vo.wait_until("You control all three")
            self.play(Indicate(VGroup(d1, d2, d12), color=TURN, scale_factor=1.02), run_time=vo.remaining(0.6))

        # ========================================================== 7. both are called through a URL
        fbl = BuildLine(show=("instance", "framework", "fn", "call"))
        for k in ("items", "build", "image", "shelf", "fail"):     # (only the running instance is used)
            fbl.remove(fbl.parts[k])
        fbl.shift(LEFT * 9.25)
        f_lab = label("Cloud Run function", CAPTION, CLOUD).next_to(fbl.instance, UP, buff=0.1)
        svc_tgt_c = np.array([4.9, 0.0, 0])
        s_lab = label("Cloud Run service", CAPTION, CLOUD)
        s_lab.move_to(svc_tgt_c + UP * (rev.height / 2 + 0.1 + s_lab.height / 2))
        h_f = url_chip("HTTPS URL").move_to([fbl.instance.get_center()[0], 1.98, 0])
        h_s = url_chip("HTTPS URL").move_to([svc_tgt_c[0], 1.98, 0])
        a_f = _arrow(h_f.get_bottom(), f_lab.get_top(), ROUTE, 4, buff=0.05)
        a_s = _arrow(h_s.get_bottom(), s_lab.get_top(), ROUTE, 4, buff=0.05)
        q = excerpt_chip(QUERY, f"{README} · line 163", color=ROUTE, frame=ROUTE, line=source_line(README, 163))
        q.move_to([-6.45 + q.width / 2, 2.0, 0])
        p911 = src_panel(MAIN, 9, 11, size=20)
        p911.move_to([0, -1.3 - p911.height / 2, 0])
        c171 = excerpt_chip(SAME, f"{README} · line 171 (excerpt)", line=source_line(README, 171))
        c171.move_to([0, -2.1, 0])
        el = mono("el", CAPTION, TURN)
        fr_g = text_glyphs(q.text, QUERY, "fr")
        el.move_to(fr_g).align_to(fr_g, DOWN)
        q_hd = excerpt_chip(QUERY, f"{README} · line 163, dest changed as line 166 says").header
        q_hd.move_to(q.header, aligned_edge=LEFT)
        inside_frame(q_hd)
        rev_after = VGroup(svc, ear)
        shift_s = svc_tgt_c - rev.get_center()
        inside_frame(fbl, f_lab, s_lab, h_f, h_s, q, p911, c171)
        below_band(q, h_f, h_s)
        apart(q, f_lab, 0.06)
        apart(q, h_s, 0.1)
        apart(p911, fbl.instance, 0.08)
        guard(ear.get_bottom()[1] + shift_s[1] >= p911.get_top()[1] + 0.05 or
              ear.get_left()[0] + shift_s[0] >= p911.get_right()[0] + 0.05, "the ear reaches the main.py panel")
        apart(c171, fbl.instance, 0.08)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(url, a_url, nob, nob_x, c273, pdock, d1, d2, d12)), run_time=0.5)
            self.play(rev_after.animate.shift(shift_s), FadeOut(rev_lab), run_time=0.7)
            self.add(fbl)
            self.play(FadeIn(fbl, shift=RIGHT * 0.3), FadeIn(f_lab), FadeIn(s_lab), run_time=0.7)
            self.play(FadeIn(h_f), FadeIn(h_s), Create(a_f), Create(a_s), run_time=0.7)
            vo.wait_until("The function takes new inputs")
            self.play(FadeOut(h_f), FadeOut(a_f), FadeIn(q, shift=DOWN * 0.1), FadeIn(p911, shift=UP * 0.1),
                      run_time=0.6)
            flows = []
            for key, n in (("text=Good%20afternoon%20everyone", 9), ("src=en", 10), ("dest=fr", 11)):
                g = text_glyphs(q.text, QUERY, key)
                cp = g.copy()
                flows.append((g, cp, p911.span(n, "request.args.get")))
            for g, cp, tgt in flows:
                self.add(cp)
                self.play(g.animate.set_color(TURN), cp.animate.move_to(tgt).set_opacity(0), run_time=0.4)
                self.remove(cp)
                self.play(Indicate(tgt, color=ROUTE, scale_factor=1.1), run_time=0.25)
            vo.wait_until("with no redeploy")
            self.play(fr_g.animate.set_opacity(0), FadeIn(el), FadeOut(p911), *swap_text(q, q.header, q_hd),
                      run_time=0.6)
            self.play(FadeIn(c171, shift=UP * 0.1), Indicate(fbl.instance, color=CLOUD, scale_factor=1.03),
                      run_time=vo.remaining(0.6))
        self.wait(1.2)          # (a short block: let the line-171 chip be read before the merge)

        # ========================================================== 8. the same thing in the end -> map slot 3
        one = instance_box(3.6, 2.0, inner=True).move_to([0, 0.55, 0])
        one_lab = label("container", CAPTION, INK).move_to(one.inner)
        cap = label("a function is a container you did not write", 26, INK).next_to(one, DOWN, buff=0.3)
        rule = RuleCard(RULE_TOP, RULE_BOTTOM)
        inside_frame(one, cap, rule)
        below_band(one)
        apart(cap, rule, 0.08)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(q, el, c171, h_s, a_s, f_lab, s_lab, ear)), FadeOut(lr), run_time=0.6)
            self.play(fbl.animate.shift(RIGHT * (one.get_center()[0] - fbl.instance.get_center()[0])
                                        + UP * (one.get_center()[1] - fbl.instance.get_center()[1])),
                      svc.animate.move_to(one), run_time=1.0)
            self.play(FadeOut(fbl), FadeOut(svc), FadeIn(one), FadeIn(one_lab), run_time=0.7)
            vo.wait_until("A function is a container")
            self.play(Write(cap), run_time=1.0)
            vo.wait_until("On the quiz")
            self.play(rule.frame_in(), run_time=0.4)
            self.play(rule.line_in(0), run_time=0.6)
            vo.wait_until("Your own image")
            self.play(rule.line_in(1), run_time=vo.remaining(0.6))
        self.wait(0.8)
        self.play(FadeOut(VGroup(one, one_lab, cap)), run_time=0.5)
        rule.shrink_into(self, m, 3)
        self.play(m.pulse(3), run_time=0.7)
        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
        self.wait(0.3)
