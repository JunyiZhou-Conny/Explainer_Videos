"""S08 · --predict: 150,528 numbers per photo (README A › Prepare, deploy, predict, step 3; the V3
TwoPipes left pipe returns; LECTURE 15 · 13 in blocks 1–2 only; the TF Serving stand-in; the hook
of S01 answered).

Beats (script.md "## S08", one voiceover block each):
 0  TRACKER A3 3. 13-row terminal (20 pt) at (app) app@<id>:/app$, `▶ your turn` on its title bar;
    types `python cli.py --predict` -> TERM(laptop/29: 52–54, 60 wrap, 61–63 wrap, …, 73–75 wrap).
    53 RED with the chip "no deploy · no file" beside 54; on "falls back" 60–63 print, the endpoint
    name on 63 turns GREY with a ring and the chip "fallback name" beside its second row; 62 RED.
    On "fails five times" … 73–75 print, 74 RED, both errors flash. On "Pause" the turn tag
    flashes and the GREY chip "fails with keys? the endpoint must be InService · README A:190–191"
    comes in above the terminal.
 1  The terminal goes. LECTURE 15 · 13 with V3's left pipe (built, shifted up, never scaled): photo,
    the two gears, the TEAL cube with three edge labels (224, 224, 3), the PINK wire, the endpoint.
    The photo rides through the gears into the cube on "resizes it"; the edge labels flash on "224
    by 224" and "3 color channels"; the cube rides the wire on "How many numbers". PONDER (8 s).
 2  LECTURE (held). The card goes; the edge labels fly together into the YELLOW counter, which
    runs to 150,528. On "Python writes each one as text": a copy of the cube turns into a long PINK
    ribbon of digits under the pipe, labelled {"instances": [ … ]}, with the chip "JSON text · a
    few MB per photo". On "A signature that takes bytes": the GREY-dashed alternative "bytes-in
    signature (the trainer, part 2) · sends the JPEG itself". Pipe, ribbon and lecture tag go.
 3  {"predictions": [[p0, p1, p2, p3]]} top left; its four tokens turn into four GREEN bars (the
    real brie-1 numbers of laptop/47:25) with their indices. CODE(cli.py: 230–234, dedented, 234 cut)
    at the bottom: 232 `np.argmax` PURPLE; a PURPLE "np.argmax" arrow lands on the tallest bar and
    its index rings YELLOW. On "looks it up" the panel gives way to CODE(cli.py: 36–43, 42 cut):
    lines 41–42 YELLOW; the four map entries write in under the bars on their words, "brie" ringed.
 4  TRACKER A3 3 · extra · local stand-in, not SageMaker. 11-row host terminal (prompt
    student@laptop:~/model-deployment-aws$, title-bar tag "extra · a second terminal on your
    laptop"): `docker pull tensorflow/serving:2.13.1` -> TERM(laptop/45: 26–27). On "The AWS serving
    image runs TensorFlow Serving" a TEAL box "tensorflow/serving 2.13 (public image)" and a GREY-
    dashed chip "the AWS serving image runs TF Serving too" above the terminal. laptop/46's line 1
    (folds) -> TERM(laptop/46: 5 from "NodeDef…" cut, 7 from "SavedModel load" cut, 9 from
    "Successfully loaded", 15 from "Exporting HTTP/REST", 20–21): 5 ORANGE with the chip "ignored
    attribute · loads anyway", 7's "success: OK" GREEN; on "It loads version 1" "version: 1" and
    "AVAILABLE" GREEN.
 5  The box and chip go; the terminal grows to 13 rows. laptop/47's line 1 (cut) -> TERM(laptop/47:
    21 wrap GREY, 23–26 wrap, 28–31 wrap); four small GREEN bars beside each `[…] k` row; brie and
    gruyere flash on their words.
 6  TERM(laptop/47: 33–36 wrap): 33 YELLOW, 36 RED, the 0.977 bar towers in RED; GREY chip
    "released model · its metrics file: accuracy 0.724" above the terminal.
 7  TRACKER A3 3. The hook returns: RECORDED(expected/md-predict-readme.txt: 7–8, 12–15) on top, a
    3-row strip with TERM(laptop/47: 43, 45–46) (title-bar tag "extra · local stand-in, not
    SageMaker") below; a big YELLOW "3" beside the recorded `[…] 0` row and a big "4" beside the
    stand-in's `[…] 3` row. Between them a small GREEN-dashed artifact slot: on "different
    artifact" the GREY-dashed "3-class model · 0 = gouda" card slides out and the GREEN "4-class model
    (v1 release) · 0 = parmigiano (cli.py:42)" slides in; the top panel dims as the bottom lights;
    `erratum` beside the slot.
 8  TRACKER A3 3 · extra. The card and slot go; the strip types `docker rm -f cheese-serving`
    -> TERM(laptop/48: 2). The TEAL stand-in box appears over it and dissolves. Fade to empty.
"""

import re

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S08"]
SIZE = 20                                     # terminal font: 72 characters a row

# ------------------------------------------------------------------ the real sources (checked)
C29, C45, C46, C47, C48 = (capture(n) for n in ("29", "45", "46", "47", "48"))
CMD29 = C29.typed(35)
assert CMD29 == "python cli.py --predict", CMD29
OUT29A = C29.at((52, 54))
assert OUT29A[1].startswith("Error: endpoint_config.json not found"), OUT29A
L60 = C29.line(60)
assert L60.startswith("image_files: ['data/brie-1.jpg'"), L60
OUT29B = C29.at((61, 63))
ENDPOINT = "'model-mobilenetv2-train-base-True-v1-endpoint'"
assert OUT29B[1] == "Error invoking endpoint: Unable to locate credentials" and ENDPOINT in OUT29B[2], OUT29B
OUT29C = C29.at((73, 75))
assert OUT29C[1] == OUT29B[1] and OUT29C[2] == OUT29B[2], OUT29C
assert "InService" in readme(191, "A") and "Predictions Fail" in readme(190, "A")

assert C45.cmd == "docker pull tensorflow/serving:2.13.1", C45.cmd
OUT45 = C45.at((26, 27))
assert OUT45[1] == "docker.io/tensorflow/serving:2.13.1", OUT45
assert C46.cmd.startswith("docker run -d --name cheese-serving") and "tensorflow/serving:2.13.1" in C46.cmd
L46_5 = cut(from_phrase(C46.line(5), "NodeDef mentions attribute debug_name"), "debug_name")
L46_7 = cut(from_phrase(C46.line(7), "SavedModel load"), n=72)
L46_9 = from_phrase(C46.line(9), "Successfully loaded")
L46_15 = from_phrase(C46.line(15), "Exporting HTTP/REST")
OUT46_J = C46.at((20, 21))
assert "success: OK" in L46_7 and L46_9.endswith("{name: cheese version: 1}") and '"AVAILABLE"' in OUT46_J[1]

CMD47 = cut(C47.cmd, n=72 - len(P_MD) - 1)                     # script.md: (extra; cut)
assert C47.cmd.startswith(CMD47[:-1]) and len(P_MD) + 1 + len(CMD47) <= 72
L47_21 = C47.line(21)
assert L47_21.startswith("[capture stand-in] endpoint"), L47_21
OUT47_B = C47.at((23, 26))      # brie-1
OUT47_G = C47.at((28, 31))      # gruyere-1
OUT47_P = C47.at((33, 36))      # parmigiano-1 -> brie
OUT47_H = C47.at(43, 45, 46)    # gouda-2 (the hook reprise)
assert OUT47_B[0] == "Image: data/brie-1.jpg" and OUT47_G[0] == "Image: data/gruyere-1.jpg"
assert OUT47_P[0] == "Image: data/parmigiano-1.jpg" and OUT47_P[3].split() == ["Label:", "brie"], OUT47_P
assert OUT47_H[0] == "Image: data/gouda-2.jpeg" and OUT47_H[1].endswith("] 3"), OUT47_H

C48_OUT = C48.at(2)
assert C48.cmd == "docker rm -f cheese-serving" and C48_OUT == ["cheese-serving"]

REC = recorded((7, 8), (12, 15))
assert REC[0] == "Image: data/brie-2.jpg" and REC[4].endswith("] 0") and REC[5].split() == ["Label:", "gouda"], REC

NUM_RE = re.compile(r"\d\.\d+")


def nums(row: str) -> list[float]:
    """The probabilities of a printed `[…] k` row."""
    return [float(x) for x in NUM_RE.findall(row)]


B_VALS, G_VALS, P_VALS = nums(OUT47_B[2]), nums(OUT47_G[2]), nums(OUT47_P[2])
assert len(B_VALS) == len(G_VALS) == len(P_VALS) == 4 and max(P_VALS) > 0.97
assert len(nums(REC[4])) == 3 and len(nums(OUT47_H[1])) == 4

assert "np.argmax(prediction)" in excerpt("A/cli.py", 232, 232)
assert '"index2label": {"0": "parmigiano", "1": "gruyere", "2": "brie", "3": "gouda"}' in excerpt("A/cli.py", 42, 42)
assert 'payload = {"instances": [arr.tolist()]}' in excerpt("A/cli.py", 225, 225)


def fixed_tracker(key: str, step: int, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (common.py's head arrange() centres
    it at y 0; the workaround of S01, S03-S07; requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def faded(m, k: float):
    """A copy of `m` with every member's own fill and stroke opacity scaled by k (Transform target)."""
    c = m.copy()
    for a, b in zip(c.family_members_with_points(), m.family_members_with_points()):
        a.set_fill(opacity=b.get_fill_opacity() * k).set_stroke(opacity=b.get_stroke_opacity() * k)
    return c


def row_with(rows, sub: str):
    """The printed terminal row that contains `sub`."""
    for r in rows:
        if sub in r.text:
            return r
    raise ValueError(f"{sub!r} not printed: {[r.text for r in rows]}")


def on_baseline(t: Text, x: float, y: float) -> Text:
    """Centre a one-word label on x with its baseline (the bottom of its first letter without a
    descender) at y, so that words with and without descenders sit on one line."""
    j = next(i for i, ch in enumerate(t.text) if ch in "aceimnorsuvwxz")
    t.move_to([x, t.get_center()[1], 0])
    return t.shift(UP * (y - t[j].get_bottom()[1]))


def model_card(text: str, color, dashed: bool) -> VGroup:
    """A one-line artifact card for the slot of block 7. .frame .text"""
    t = label(text, 20, INK if not dashed else S.GREY)
    fr = outline_box(t.width + 0.5, 0.52, color, solid=not dashed, fill_opacity=0.12)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


class AskTheEndpoint(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S08"] == 9, len(SAY)
        self.bar_tags = []

        # ========================================================== 0. --predict: no endpoint, no keys
        tr = fixed_tracker("A3", 3)
        t = term(P_APP, rows=13, size=SIZE)
        self.t = t
        turn = on_bar(t, turn_row())
        keys = grey_chip("fails with keys? the endpoint must be InService · README A:190–191")
        under_term(t, keys)
        assert keys.get_top()[1] < PIC_TOP and keys.get_left()[0] > -6.6, keys.get_top()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.6)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.06), run_time=0.6)
            type_cmd(self, t, CMD29, type_time=0.9)
            self.bar(turn)
            vo.wait_until("Ours finds no endpoint config")
            ra = out(self, t, [OUT29A[0], (OUT29A[1], ERR), OUT29A[2]], run_time=0.5)
            nofile = beside(row_tag("no deploy · no file", ERR), ra[2], buff=0.35)
            assert nofile.get_right()[0] < t.box.get_right()[0] - 0.05, nofile.get_right()
            pin(self, ra[2], nofile)
            self.play(Indicate(substring(ra[1], "endpoint_config.json"), color=ERR, scale_factor=1.12),
                      run_time=0.6)
            self.reseat()
            vo.wait_until("and falls back to a default name")
            rb = out(self, t, [L60, OUT29B[0], (OUT29B[1], ERR), OUT29B[2]], wrap=True, run_time=0.6)
            r63 = row_with(rb, ENDPOINT)
            name = substring(r63, ENDPOINT)
            self.play(name.animate.set_color(S.GREY), run_time=0.3)
            self.reseat()
            rg = ring(name, S.GREY, buff=0.04)
            r63b = rb[-1]
            assert r63b.text == "exists and is in service", r63b.text
            fb = beside(row_tag("fallback name"), r63b, buff=0.35)
            self.play(Create(rg), run_time=0.4)
            pin(self, r63b, fb)
            attach(self, r63, rg)
            vo.wait_until("It picks five photos")
            r60 = row_with(rb, "image_files")
            self.play(Indicate(substring(r60, "image_files"), color=TURN, scale_factor=1.12), run_time=0.7)
            self.reseat()
            vo.wait_until("and fails five times")
            rc = out(self, t, ["…", OUT29C[0], (OUT29C[1], ERR), OUT29C[2]], wrap=True, run_time=0.6)
            e1, e2 = row_with(rb, "Unable to locate"), row_with(rc, "Unable to locate")
            vo.wait_until("unable to locate credentials")
            self.play(Indicate(substring(e1, "Unable to locate credentials"), color=ERR, scale_factor=1.08),
                      Indicate(substring(e2, "Unable to locate credentials"), color=ERR, scale_factor=1.08),
                      run_time=0.8)
            self.reseat()
            vo.wait_until("Pause and run yours")
            flash_tag(self, turn, color=TURN)
            self.play(FadeIn(keys, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 1. V3 left pipe + PONDER
        v = TwoPipes(built=True)
        v.shift(UP * 1.2)
        assert v.get_top()[1] < PIC_TOP, v.get_top()
        lt = lref("13")
        cb = v.cube_g[0]
        e_top = label("224", 20, IMAGE).next_to(cb.front, UP, buff=0.42)
        e_side = label("224", 20, IMAGE).next_to(cb, RIGHT, buff=0.1).shift(UP * 0.3)
        e_dep = label("3", 20, IMAGE).move_to(cb.get_corner(UR) + np.array([0.12, 0.12, 0]))
        edges = [e_top, e_side, e_dep]
        assert e_side.get_right()[0] < v.ep[0].get_left()[0] - 0.3, e_side.get_right()
        q = ("--predict resizes one photo to\n224 × 224 with 3 color channels.\n"
             "How many numbers travel to the\nendpoint for that one photo?")

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(t), FadeOut(keys), *self.unbar_anims(), run_time=0.5)
            self.remove(t)
            self.play(FadeIn(v), FadeIn(lt, shift=LEFT * 0.1), run_time=0.8)
            self.play(Indicate(v.photo, color=TURN, scale_factor=1.12), run_time=0.6)
            v.heal(self)
            vo.wait_until("The client resizes it")
            ph = v.photo[0].copy()
            self.add(ph)
            self.play(ph.animate.move_to(v.gear_list[0]), Rotate(v.gear_list[0], PI / 2), run_time=0.6)
            self.play(ph.animate.move_to(v.gear_list[1]), Rotate(v.gear_list[1], PI / 2), run_time=0.5)
            self.play(ph.animate.scale(0.6).move_to(cb), Indicate(cb, color=IMAGE, scale_factor=1.08),
                      run_time=0.5)
            self.remove(ph)
            v.heal(self)
            vo.wait_until("to 224 by 224")
            v.show(self, e_top, e_side, anims=[FadeIn(e_top, shift=DOWN * 0.1), FadeIn(e_side, shift=LEFT * 0.1)],
                   run_time=0.5)
            vo.wait_until("with 3 color channels")
            v.show(self, e_dep, anims=[FadeIn(e_dep, scale=1.5)], run_time=0.4)
            self.play(Indicate(e_dep, color=TURN, scale_factor=1.4), run_time=0.6)
            v.heal(self)
            vo.wait_until("How many numbers travel")
            rider = cb.copy()
            self.add(rider)
            self.play(rider.animate.scale(0.5).move_to(v.door), run_time=0.9)
            self.play(FadeOut(rider), Indicate(v.door, color=TURN, scale_factor=1.1), run_time=0.4)
            self.remove(rider)
            v.heal(self)
        card_p = ponder(self, q, 8, center=(0, -1.35))

        # ========================================================== 2. 150,528 floats, as JSON text
        rib_lab = mono('{"instances": [ … ]}', 22, ROUTE)
        rib_lab.move_to([-6.4 + rib_lab.width / 2, -0.55, 0])
        rib_fr = outline_box(12.8, 0.62, ROUTE, solid=True, fill_opacity=0.1)
        rib_fr.move_to([0, -1.2, 0])
        rib_txt = mono("0.4313725…, 0.4352941…, …", 22, ROUTE)
        rib_txt.move_to(rib_fr).align_to(rib_fr, LEFT).shift(RIGHT * 0.3)
        dots = VGroup(*[Dot(radius=0.045, color=ROUTE) for _ in range(9)]).arrange(RIGHT, buff=0.32)
        dots.next_to(rib_txt, RIGHT, buff=0.45)
        ribbon = VGroup(rib_fr, rib_txt, dots)
        few = chip("JSON text · a few MB per photo", ROUTE, size=22)
        few.move_to([6.4 - few.width / 2, -1.95, 0])
        jp = file_glyph(0.42, INK)
        alt_t = label("bytes-in signature (the trainer, part 2) · sends the JPEG itself", 22, PAST)
        alt_row = VGroup(jp, alt_t).arrange(RIGHT, buff=0.25)
        alt_fr = outline_box(alt_row.width + 0.6, 0.72, PAST, solid=False)
        alt_row.move_to(alt_fr)
        alt = VGroup(alt_fr, alt_row)
        alt.move_to([-6.4 + alt.width / 2, -2.9, 0])
        assert rib_lab.get_top()[1] < v.get_bottom()[1] - 0.1, (rib_lab.get_top(), v.get_bottom())
        assert dots.get_right()[0] < rib_fr.get_right()[0] - 0.2 and alt.get_right()[0] < 6.5
        assert few.get_bottom()[1] > alt.get_top()[1] + 0.05 or few.get_left()[0] > alt.get_right()[0], few.get_bottom()

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(card_p), run_time=0.4)
            self.remove(card_p)
            vo.wait_until("224 times 224")
            self.play(each(edges, TURN, scale=1.4, lag=0.35), run_time=1.2)
            v.heal(self)
            for m in edges:
                v._detach(m)
            self.add(*edges)
            counter = mono("0", 26, TURN).next_to(cb, UP, buff=0.25)
            self.play(*[m.animate.move_to(counter).set_opacity(0) for m in edges], FadeIn(counter), run_time=0.5)
            self.remove(*edges, counter)
            v.add(counter)
            v.heal(self)
            anchor = counter.get_center().copy()
            assert f"{FLOATS:,}" == "150,528"

            def upd(m, a):
                m.become(mono(f"{int(round(a * FLOATS)):,}", 26, TURN).move_to(anchor))

            vo.wait_until("one hundred fifty thousand")
            self.play(UpdateFromAlphaFunc(counter, upd), run_time=2.2, rate_func=rate_functions.ease_out_cubic)
            self.play(Indicate(counter, color=TURN, scale_factor=1.2), run_time=0.6)
            v.heal(self)
            self.play(Indicate(v.cube_g[1], color=IMAGE, scale_factor=1.15), run_time=0.7)
            v.heal(self)
            vo.wait_until("Python writes each one as text")
            src = cb.copy()
            self.add(src)
            self.play(ReplacementTransform(src, rib_fr), FadeIn(rib_lab, shift=DOWN * 0.1), run_time=0.8)
            self.play(Write(rib_txt), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15), run_time=1.1)
            vo.wait_until("so a few megabytes per photo")
            self.play(FadeIn(few, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(few.text if hasattr(few, "text") else few, color=ROUTE, scale_factor=1.08),
                      run_time=0.6)
            vo.wait_until("A signature that takes bytes")
            self.play(Create(alt_fr), FadeIn(alt_row, shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("would send the JPEG itself")
            self.play(Indicate(jp, color=INK, scale_factor=1.3), run_time=0.6)

        # ========================================================== 3. four probabilities, argmax, the map
        shape = mono_line('{"predictions": [[p0, p1, p2, p3]]}', 22, ROUTE)
        shape.move_to([-6.4 + shape.width / 2, 2.45, 0])
        toks = [substring(shape, f"p{i}") for i in range(4)]
        BASE = 1.0
        bg = bars(B_VALS, 0.45, 2.3, OWN, hi=None, buff=1.75)
        bg.move_to([1.4, BASE + bg.height / 2, 0]).align_to([0, BASE, 0], DOWN)
        hi = int(np.argmax(B_VALS))
        idx = VGroup(*[mono(str(i), 22, INK).move_to([b.get_center()[0], BASE - 0.25, 0]) for i, b in enumerate(bg)])
        names = VGroup(*[on_baseline(label(n, 22, TURN), b.get_center()[0], BASE - 0.75) for n, b in zip(LABELS, bg)])
        am = mono("np.argmax", 20, TOOL)
        am.move_to([bg[hi].get_right()[0] + 0.25 + am.width / 2, bg[hi].get_top()[1] - 0.05, 0])
        am_arrow = Arrow(am.get_left() + LEFT * 0.04, bg[hi].get_corner(UR) + RIGHT * 0.04, buff=0, color=TOOL,
                         stroke_width=4, tip_length=0.16)
        assert am.get_top()[1] < PIC_TOP and bg.get_top()[1] < shape.get_bottom()[1] - 0.1, \
            (am.get_top(), bg.get_top(), shape.get_bottom())
        assert am.get_bottom()[1] > bg[hi + 1].get_top()[1] + 0.1 and am.get_right()[0] < 6.5, am.get_bottom()
        assert names.get_right()[0] < 6.5 and all(names[k + 1].get_left()[0] > names[k].get_right()[0] + 0.3
                                                  for k in range(3)), [n.get_left() for n in names]
        p2 = code("A/cli.py", 230, 234, font_size=20, dedent=True, cuts={234: "[str(prediction_index)]"})
        p2.move_to([0, -3.5 + p2.height / 2, 0])
        p1 = code("A/cli.py", 36, 43, font_size=20, cuts={41: '"brie": 2,', 42: '"2": "brie",'})
        p1.move_to([0, -3.5 + p1.height / 2, 0])
        assert p1.get_top()[1] < names.get_bottom()[1] - 0.08, (p1.get_top(), names.get_bottom())
        b232 = line_bar(p2.code, 2, TOOL, 0.25)
        b41 = line_bar(p1.code, 5, TURN, 0.2)
        b42 = line_bar(p1.code, 6, TURN, 0.3)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(v), FadeOut(ribbon), FadeOut(rib_lab), FadeOut(few), FadeOut(alt), FadeOut(lt),
                      run_time=0.6)
            self.remove(v)
            self.play(FadeIn(shape, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("a list of four probabilities")
            self.play(*[ReplacementTransform(tk.copy(), b) for tk, b in zip(toks, bg)], run_time=0.9)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in idx], lag_ratio=0.2), run_time=0.6)
            vo.wait_until("The code takes the largest")
            self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("with arg max")
            self.play(FadeIn(b232), code_span(p2.code, 2, "np.argmax").animate.set_color(TOOL), run_time=0.4)
            self.add(p2, b232)
            self.play(FadeIn(am, shift=DOWN * 0.1), GrowArrow(am_arrow), bg[hi].animate.set_color(TURN),
                      run_time=0.6)
            rg_i = ring(idx[hi], TURN, buff=0.08)
            self.play(Create(rg_i), run_time=0.4)
            vo.wait_until("and looks it up")
            self.play(FadeOut(p2), FadeOut(b232), FadeIn(p1, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(b41), FadeIn(b42), run_time=0.3)
            self.add(p1, b41, b42)
            for k, ph in enumerate(("0 parmigiano", "1 gruyere", "2 brie", "3 gouda")):
                vo.wait_until(ph)
                self.play(Write(names[k]), Indicate(idx[k], color=TURN, scale_factor=1.3), run_time=0.45)
            rg_n = ring(names[hi], TURN, buff=0.08)
            self.play(Create(rg_n), run_time=0.4)

        # ========================================================== 4. the TF Serving stand-in
        t = term(P_MD, rows=11, size=SIZE)
        self.t = t
        second = on_bar(t, row_tag("extra · a second terminal on your laptop"))
        teal = image_block("tensorflow/serving 2.13 (public image)", box_w=5.6)
        teal.move_to([-6.4 + teal.width / 2, 2.15, 0])
        same = dashed_chip("the AWS serving image runs TF Serving too")
        same.move_to([6.4 - same.width / 2, 2.15, 0])
        assert teal.get_bottom()[1] > t.box.get_top()[1] + 0.1 and teal.get_top()[1] < PIC_TOP
        assert same.get_left()[0] > teal.get_right()[0] + 0.15, (same.get_left(), teal.get_right())

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(shape, bg, idx, names, am, am_arrow, rg_i, rg_n, p1, b41, b42)),
                      run_time=0.6)
            self.play(track(tr, 3, "local stand-in, not SageMaker"), FadeIn(t), run_time=0.6)
            self.bar(second)
            type_cmd(self, t, C45.cmd, type_time=0.8)
            out(self, t, OUT45, run_time=0.4)
            vo.wait_until("The AWS serving image runs TensorFlow Serving")
            self.play(FadeIn(teal, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(same, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("so we started the public Serving")
            type_cmd(self, t, C46.cmd, type_time=1.3)
            r5 = out(self, t, [(L46_5, SHARED)], run_time=0.3)
            ign = beside(row_tag("ignored attribute · loads anyway", SHARED), r5[0], buff=0.35)
            pin(self, r5[0], ign)
            r7 = out(self, t, [L46_7, L46_9, L46_15], run_time=0.5)
            self.play(substring(r7[0], "success: OK").animate.set_color(OWN), run_time=0.3)
            self.reseat()
            rj = out(self, t, OUT46_J, run_time=0.3)
            vo.wait_until("It loads version 1")
            self.play(substring(r7[1], "version: 1").animate.set_color(OWN),
                      substring(rj[1], '"AVAILABLE"').animate.set_color(OWN), run_time=0.4)
            self.reseat()
            self.play(Indicate(substring(r7[1], "version: 1"), color=OWN, scale_factor=1.2),
                      Indicate(substring(rj[1], '"AVAILABLE"'), color=OWN, scale_factor=1.2), run_time=0.7)
            self.reseat()

        # ========================================================== 5. the same predict(): four numbers
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(teal), FadeOut(same), run_time=0.4)
            resize(self, t, 13, keep=2, extra=[self.bar_tags[0].animate.shift(UP * t.pitch * 2)])
            type_cmd(self, t, CMD47, type_time=0.8)
            out(self, t, [(L47_21, S.GREY)], wrap=True, run_time=0.4)
            vo.wait_until("Brie comes back brie")
            rB = out(self, t, OUT47_B, wrap=True, run_time=0.5)
            self.minibars(rB, B_VALS)
            self.play(Indicate(substring(rB[-1], "brie"), color=OWN, scale_factor=1.3), run_time=0.5)
            self.reseat()
            vo.wait_until("and gruyere comes back gruyere")
            rG = out(self, t, OUT47_G, wrap=True, run_time=0.5)
            self.minibars(rG, G_VALS)
            self.play(Indicate(substring(rG[-1], "gruyere"), color=OWN, scale_factor=1.3), run_time=0.5)
            self.reseat()
            vo.wait_until("four numbers each")
            self.play(Indicate(rB.mb, color=OWN, scale_factor=1.25), Indicate(rG.mb, color=OWN, scale_factor=1.25),
                      run_time=0.7)
            self.reseat()

        # ========================================================== 6. parmigiano comes back brie
        acc = grey_chip("released model · its metrics file: accuracy 0.724")
        under_term(t, acc)
        assert acc.get_top()[1] < PIC_TOP, acc.get_top()

        with self.voiceover(SAY[6]) as vo:
            rP = out(self, t, [(OUT47_P[0], TURN), OUT47_P[1], OUT47_P[2], (OUT47_P[3], ERR)], wrap=True,
                     run_time=0.5)
            self.minibars(rP, P_VALS, max_h=0.62, hi_color=ERR)
            vo.wait_until("at 98 percent")
            self.play(Indicate(rP.mb.bar_list[2], color=ERR, scale_factor=1.15),
                      Indicate(substring(rP[-2], "0.97726506"), color=ERR, scale_factor=1.15), run_time=0.8)
            self.reseat()
            vo.wait_until("That is a real mistake")
            self.play(Indicate(rP[-1], color=ERR, scale_factor=1.06), run_time=0.7)
            self.reseat()
            vo.wait_until("Its own metrics file")
            self.play(FadeIn(acc, shift=DOWN * 0.1), run_time=0.5)
            flash_tag(self, acc, color=INK)

        # ========================================================== 7. the hook, answered
        rec = recorded_card([(7, 8), (12, 15)], size=20, wrap=72)
        rec.move_to([-6.4 + rec.width / 2, 2.6 - rec.frame.height / 2, 0])
        s = term(P_MD, rows=3, size=SIZE)
        self.t2 = s
        sb = on_bar(s, row_tag("extra · local stand-in, not SageMaker"))
        slot = outline_box(7.4, 0.78, OWN, solid=False)
        slot.move_to([-6.4 + 1.25 + slot.width / 2, (rec.frame.get_bottom()[1] + s.box.get_top()[1]) / 2, 0])
        slot_l = label("artifact", 20, OWN).next_to(slot, LEFT, buff=0.2)
        old_c = model_card("3-class model · 0 = gouda", S.GREY, True).move_to(slot)
        new_c = model_card("4-class model (v1 release) · 0 = parmigiano (cli.py:42)", OWN, False).move_to(slot)
        old_c.shift(LEFT * (old_c.get_left()[0] - slot.get_left()[0] - 0.15))
        new_c.shift(LEFT * (new_c.get_left()[0] - slot.get_left()[0] - 0.15))
        err7 = erratum_tag().next_to(slot, RIGHT, buff=0.3)
        assert slot.get_bottom()[1] > s.box.get_top()[1] + 0.05 and slot.get_top()[1] < rec.frame.get_bottom()[1] - 0.05, \
            (slot.get_bottom(), slot.get_top(), s.box.get_top(), rec.frame.get_bottom())
        assert new_c.get_right()[0] < slot.get_right()[0] - 0.05 and err7.get_right()[0] < 6.55, \
            (new_c.get_right(), slot.get_right(), err7.get_right())
        assert rec.tag.get_left()[0] > tr.get_right()[0] + 0.2 or rec.tag.get_top()[1] < TRACK_BOTTOM
        r14 = rec.rows[4]
        big3 = label("3", 40, TURN).next_to(r14, RIGHT, buff=0.6)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(t), FadeOut(acc), *self.unbar_anims(), track(tr, 3), run_time=0.6)
            self.remove(t)
            self.play(FadeIn(rec, shift=DOWN * 0.1), FadeIn(s), run_time=0.6)
            self.bar(sb)
            self.t = s
            rH = out(self, s, OUT47_H, run_time=0.5)
            vo.wait_until("Same code, different artifact")
            big4 = label("4", 40, TURN).next_to(rH[1], RIGHT, buff=0.6)
            self.play(FadeIn(big3, scale=1.4), FadeIn(big4, scale=1.4), run_time=0.5)
            self.play(Create(slot), FadeIn(slot_l), FadeIn(old_c, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("the README output came from an older model")
            self.play(Indicate(old_c.text, color=S.GREY, scale_factor=1.06), Indicate(rec.tag.text, color=INK),
                      run_time=0.7)
            vo.wait_until("with three classes")
            self.play(Indicate(big3, color=TURN, scale_factor=1.3), run_time=0.5)
            vo.wait_until("and another label order")
            self.play(Indicate(rec.rows[5], color=TURN, scale_factor=1.1), Indicate(rec.rows[4], color=TURN,
                      scale_factor=1.05), run_time=0.6)
            self.add(rec, big3)                 # re-seat the card; the big 3 stays on top of its fill
            vo.wait_until("A small gap")
            self.play(old_c.animate.shift(LEFT * 1.0).set_opacity(0), run_time=0.5)
            self.remove(old_c)
            self.play(FadeIn(new_c, shift=LEFT * 0.6), Transform(rec, faded(rec, 0.35)),
                      FadeIn(err7, shift=LEFT * 0.1), run_time=0.7)
            self.add(big3)
            vo.wait_until("expect four numbers")
            self.play(Indicate(big4, color=TURN, scale_factor=1.3), run_time=0.5)
            vo.wait_until("and index 0 is parmigiano")
            self.play(Indicate(new_c.text, color=OWN, scale_factor=1.06), run_time=0.7)

        # ========================================================== 8. remove the stand-in
        teal8 = image_block("tensorflow/serving 2.13 (public image)", box_w=5.6)
        teal8.move_to([0, 0.2, 0])

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(rec, big3, big4, slot, slot_l, new_c, err7)), track(tr, 3, True),
                      run_time=0.6)
            self.play(FadeIn(teal8, shift=DOWN * 0.1), run_time=0.4)
            ln = type_cmd(self, s, C48.cmd, type_time=0.7)
            out(self, s, C48_OUT, run_time=0.3)
            vo.wait_until("It never touched AWS")
            self.play(FadeOut(teal8, scale=0.5), run_time=0.8)
        self.play(FadeOut(s), *self.unbar_anims(), FadeOut(tr), run_time=0.7)
        self.remove(s)
        self.wait(0.3)

    # ------------------------------------------------------------------ helpers
    def minibars(self, rows, values, max_h: float = 0.3, hi_color=TURN):
        """Four small bars beside the `[…] k` row of a printed result (pinned: they scroll with it).
        The tallest in hi_color. Stores them as rows.mb."""
        row = row_with(rows, "] ")
        hi = int(np.argmax(values))
        b = bars(values, 0.16, max_h, OWN, hi=hi, hi_color=hi_color, buff=0.07)
        b.move_to([row.strut.get_right()[0] + 0.45 + b.width / 2, 0, 0])
        b.align_to(row.strut, DOWN).shift(UP * 0.04)
        assert b.get_right()[0] < self.t.box.get_right()[0] - 0.1, b.get_right()
        self.play(LaggedStart(*[GrowFromEdge(m, DOWN) for m in b], lag_ratio=0.15), run_time=0.5)
        attach(self, row, b)
        rows.mb = b
        return b

    def bar(self, tg):
        """Show a title-bar tag (on_bar) and remember it, so it fades with the terminal."""
        self.play(FadeIn(tg), run_time=0.3)
        self.bar_tags.append(tg)

    def unbar_anims(self):
        tgs, self.bar_tags = self.bar_tags, []
        return [FadeOut(tg) for tg in tgs]

    def reseat(self):
        """Re-seat the terminal as one mobject (split trap) and keep its bar tags on top."""
        self.add(self.t, *self.bar_tags)
