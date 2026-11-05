"""S09 · --delete: turn off the meter (README A › Clean Up, steps 1–3; V5 ThreeObjects torn down;
LECTURE 15 · 11, 41 for the meter-and-DELETE picture only). End of part 1.

Beats (script.md "## S09", one voiceover block each):
 0  TRACKER A4 1 fades in (new section "README A › Clean Up", 3 dots). Lecture tag "Lecture 15 ·
    slides 11, 41" with the picture: V5's endpoint (plate `…-endpoint-<timestamp>`, the
    ml.m5.xlarge rack) and a large GOLD cost dial that keeps sweeping; a GOLD word card "DELETE"
    (no image) stamps beside it. On "three ways" the word card and the lecture tag go; GREY chip
    "three ways · pick one" (README A:154, 159, 166 are alternatives); CONSOLE("SageMaker ›
    Endpoints", A:154-157) tagged `illustration`: the row "your endpoint" gets its tick on "select
    yours", the Delete button pulses on "Delete" (no ▶ your turn: that sits on way 3).
 1  TRACKER A4 2. GREY chip top right "in the container, or a second terminal on your laptop"; a
    README card (README.md · lines 161–163, chip A; the long middle line folds with ' \\' like a
    terminal row); a 6-row terminal (20 pt) at student@laptop:~/model-deployment-aws$ types
    `aws sagemaker delete-endpoint --endpoint-name <your-endpoint-name>` -> TERM(laptop/31: 2–3)
    RED; `<` and `>` ringed RED; RED chip "the shell reads < as a redirection" + `erratum`.
 2  TRACKER A4 2 · extra: `aws sagemaker delete-endpoint --endpoint-name cheese-endpoint-placeholder`
    -> TERM(laptop/32: 3 wrap) RED. TRACKER A4 2. The README card turns into three numbered chips
    "1 endpoint · 2 endpoint config · 3 model" on "Delete in this order"; the README's other two lines
    are typed as written (brackets faded and crossed out GREY, QA 15:15) on "its configuration" / "the model"; GREY chips
    "your own name · needs your account · no output shown" and "names: aws sagemaker
    list-endpoint-configs · aws sagemaker list-models".
 3  TRACKER A4 3. A fresh 7-row terminal at (app) app@<id>:/app$ types `python cli.py --delete` ->
    TERM(laptop/30: 52, …, 74, 79, …, 260); 79 and 260 RED; GREY chip "the only way that also
    removes the tarball" with the README card (A:171–174, up the whole terminal beat, QA 14:46),
    pulsed with ▶ your turn. On "With keys" the terminal goes and V5 comes
    back in its deployed state (Model card, endpoint configuration, endpoint with its dial); a code
    strip under it follows the clean-up line by line: cli.py 258–259 as the endpoint goes (the meter
    stops), 272–273 as the configuration goes, 285–286 as the Model card goes, 290–291 as the
    tarball goes.
 4  Two endpoint plates side by side, both with GOLD dials sweeping: `…-endpoint-<t1>` (older) and
    `…-endpoint-<t2>` (newer); CODE(cli.py: 163–167) small under them (line 166 YELLOW); the GREY
    `endpoint_config.json` card sits between them with no arrow yet. PONDER(6 s) after the block.
 5  The card draws its arrow to <t2> only; the newer plate and its meter go; the older one keeps
    sweeping, RED ring + "forgotten", GREY chip "its config and model are already gone · it still
    bills" (cli.py:268–286). TRACKER A4 3 · extra: a strip types `aws sagemaker list-endpoints`
    (GREY chip "extra · needs your account · no output shown"); README card line 176.
 6  Everything clears (the tracker too) to V5's empty endpoint slot with its GOLD dial stopped where
    the forgotten one was; under it the four GREY stage tiles of S01 with a person at a CLI each
    (V6); the YELLOW question card "four commands by hand for one model · who runs all four stages,
    in order, every time?". Fade to an empty frame. End of part 1.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)
from manim.animation.animation import prepare_animation

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S09"]

# ------------------------------------------------------------------ the real sources (checked)
C30 = capture("30")
CMD30 = C30.typed(35)
assert CMD30 == "python cli.py --delete", CMD30
OUT30 = [C30.line(52), "…", unbox(C30.line(74)), unbox(C30.line(79)), "…", C30.line(260)]
assert OUT30[0] == "Delete endpoint, model, and S3 artifacts", OUT30[0]
assert OUT30[2] == "/app/cli.py:270 in delete", OUT30[2]
assert OUT30[3].startswith("❱ 270") and "paginator.paginate()" in OUT30[3], OUT30[3]
assert OUT30[5] == "NoCredentialsError: Unable to locate credentials", OUT30[5]

C31 = capture("31")
README_CLI = readme_rows(161, 163, "A")
assert len(README_CLI) == 3 and C31.cmd == README_CLI[0], (README_CLI, C31.cmd)
OUT31 = C31.at(2, 3)
assert "syntax error near unexpected token" in OUT31[0], OUT31

C32 = capture("32")
assert C32.cmd == "aws sagemaker delete-endpoint --endpoint-name cheese-endpoint-placeholder", C32.cmd
OUT32 = C32.at(3)
assert "Unable to locate credentials" in OUT32[0], OUT32

assert "Using AWS Console" in readme(154, "A") and "SageMaker > Endpoints" in readme(155, "A")
assert "Select your endpoint" in readme(156, "A") and "Delete" in readme(157, "A")
R171 = [readme(n, "A").replace("`", "") for n in range(171, 175)]
assert R171[0] == "It will attempt to delete:" and R171[3].startswith("- The S3 artifacts"), R171
README_176 = readme(176, "A")
assert README_176 == "Make sure to confirm in your AWS console to avoid charges.", README_176
assert "S3 artifacts" in readme(174, "A")
assert "delete_endpoint(EndpointName=endpoint_name)" in excerpt("A/cli.py", 259, 259)
assert "if model_name in name:" in excerpt("A/cli.py", 273, 273)
assert "delete_model(ModelName=model_name)" in excerpt("A/cli.py", 286, 286)
assert 'prefix = f"{BEST_MODEL}/"' in excerpt("A/cli.py", 291, 291)
assert '-endpoint-{ts}' in excerpt("A/cli.py", 166, 166)

SIZE = 20                  # terminal font: 72 characters a row
S_TOP = 0.45               # V5 shift (as in S07): the Model card's top at 2.78
PONDER_Q = "You ran --deploy twice,\nthen --delete once.\nHow many endpoints still bill?"
QUESTION = "four commands by hand for one model\nwho runs all four stages, in order, every time?"


def fixed_tracker(key: str, step: int, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (the workaround of S01, S03-S08;
    requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


class _Quiet:
    """A stand-in scene that plays nothing: V5's PLAYS methods build their parts here instantly, so
    the piece can come back in its S07 end state (Model, configuration, endpoint) with one FadeIn."""

    def __init__(self):
        self.mobjects = []

    def add(self, *ms):
        for m in ms:
            if m in self.mobjects:
                self.mobjects.remove(m)
            self.mobjects.append(m)
        return self

    def remove(self, *ms):
        for m in ms:
            if m in self.mobjects:
                self.mobjects.remove(m)
        return self

    def get_mobject_family_members(self):
        return [m for top in self.mobjects for m in top.get_family()]

    def replace(self, old, new):
        self.remove(old)
        self.add(new)

    def play(self, *anims, **kw):
        for a in anims:
            a = prepare_animation(a)
            a._setup_scene(self)
            a.begin()
            a.finish()
            a.clean_up_from_scene(self)


def deployed_v5() -> ThreeObjects:
    """V5 as S07 left it: the BLUE Model card (artifact, container, role), the endpoint
    configuration card, the endpoint plate with its machine and GOLD dial."""
    v = ThreeObjects(slots=True)
    v.shift(UP * S_TOP)
    q = _Quiet()
    v.model_card(q)
    v.fill_role(q)
    v.solidify(q)
    v.deploy(q)
    v.meter(q)
    return v


def rows_card(rows, lines, repo: str = "A") -> VGroup:
    """A README card whose body is mono command rows (20 pt)."""
    body = VGroup(*[mono(s, 20, INK) for s in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    return readme_card(lines, body, repo)


def strike_brackets(scene, line, color=S.GREY):
    """PLAYS: strike the '<' and '>' of every placeholder in a typed (maybe folded) line; the strikes
    become parts of their rows (they scroll with them)."""
    marks, glyphs = [], []
    for row in rows_of(line):
        for i, ch in enumerate(row.text):
            if ch in "<>":
                g = glyph_range(row, i, i + 1)
                c, h, w = g.get_center(), g.height * 0.75 + 0.06, g.width * 0.5 + 0.04   # a bold cross
                for sx in (1, -1):
                    s_ = Line(c + np.array([-sx * w, h, 0]), c + np.array([sx * w, -h, 0]), color=color,
                              stroke_width=6)
                    marks.append((row, s_))
                glyphs.append(g)
    assert marks, line
    # QA 15:15: a thin slash read as a normal '<' '>'; the brackets now fade out under a bold cross
    scene.play(*[Create(s_) for _, s_ in marks], *[g.animate.set_opacity(0.18) for g in glyphs], run_time=0.5)
    for row, s_ in marks:
        attach(scene, row, s_)
    return [s_ for _, s_ in marks]


class TurnOffTheMeter(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S09"] == 7, len(SAY)

        # ========================================================== 0. the meter, DELETE, way 1
        tr = fixed_tracker("A4", 1)
        lt = lref("11, 41")
        ep0 = endpoint_plate(meter=False, plate_w=4.1)
        dial0 = CostDial(0.9, caption="cost")
        col_h = ep0.height + 0.35 + dial0.height
        ep0.move_to([-6.45 + ep0.width / 2, 0.35 + col_h / 2 - ep0.height / 2, 0])
        dial0.move_to([ep0.plate.get_center()[0], ep0.get_bottom()[1] - 0.35 - dial0.height / 2, 0])
        word = label("DELETE", 60, COST)
        word_fr = outline_box(word.width + 0.9, word.height + 0.6, COST, solid=True, fill_opacity=0.12)
        word.move_to(word_fr)
        word_c = VGroup(word_fr, word).move_to([2.3, 0.35, 0])
        three = grey_chip("three ways · pick one")
        form = console_form("SageMaker › Endpoints", [("check", "your endpoint", False), ("button", "Delete")],
                            form_w=7.6)
        form.move_to([6.45 - form.width / 2, 0.15, 0])
        three.move_to([form.get_left()[0] + three.width / 2, form.get_top()[1] + 0.3 + three.height / 2, 0])
        ill = illustration_tag()
        ill.move_to([form.get_right()[0] - 0.2 - ill.width / 2, form.get_bottom()[1], 0])
        assert three.get_top()[1] < PIC_TOP and dial0.get_bottom()[1] > -3.5, (three.get_top(), dial0.get_bottom())
        assert form.get_left()[0] > ep0.get_right()[0] + 0.3 and word_c.get_left()[0] > ep0.get_right()[0] + 0.3

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.2), run_time=0.6)
            self.play(Indicate(tr.head, color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("The lecture warns")
            self.play(FadeIn(ep0, shift=DOWN * 0.2), FadeIn(dial0), FadeIn(lt), run_time=0.7)
            dial0.run(self, 0.35, vo.until("and the slides shout", minimum=0.5))
            self.play(FadeIn(word_c, scale=1.6), dial0.sweep(0.06), run_time=0.45)
            self.play(Indicate(word, color=COST, scale_factor=1.12), dial0.sweep(0.1), run_time=0.7)
            dial0.run(self, 0.15, vo.until("The README gives three ways", minimum=0.4))
            self.play(FadeOut(word_c), FadeOut(lt), dial0.sweep(0.05), run_time=0.5)
            self.play(FadeIn(three, shift=DOWN * 0.1), dial0.sweep(0.05), run_time=0.5)
            dial0.run(self, 0.1, vo.until("Way 1, the console", minimum=0.4))
            self.play(FadeIn(form, shift=LEFT * 0.2), FadeIn(ill), dial0.sweep(0.06), run_time=0.6)
            vo.wait_until("SageMaker, Endpoints")
            self.play(Indicate(form.title_text, color=TURN, scale_factor=1.06), dial0.sweep(0.06), run_time=0.7)
            vo.wait_until("select yours")
            row = form.rows[0]
            self.play(row.tick.animate.set_opacity(1), Indicate(row.text, color=TURN, scale_factor=1.06),
                      dial0.sweep(0.05), run_time=0.6)
            vo.wait_until("Delete.")
            self.play(form.press(1), dial0.sweep(0.05), run_time=0.8)

        # ========================================================== 1. way 2: the AWS CLI, as written
        dial0.freeze()
        t = term(P_MD, rows=6, size=SIZE)
        rc = rows_card([README_CLI[0], "aws sagemaker delete-endpoint-config \\",
                        "    --endpoint-config-name <your-endpoint-config-name>", README_CLI[2]], (161, 163))
        rc.body[2].shift(RIGHT * 4 * cell_width(SIZE))      # the folded row's indent (mono drops spaces)
        rc.move_to([-6.45 + rc.width / 2, 2.75 - rc.height / 2, 0])
        where = grey_chip("in the container, or a second terminal on your laptop")
        where.move_to([6.45 - where.width / 2, 3.22, 0])
        assert where.get_left()[0] > tr.get_right()[0] + 0.2, (where.get_left(), tr.get_right())
        gap_y = (rc.get_bottom()[1] + t.box.get_top()[1]) / 2
        redir = err_chip("the shell reads < as a redirection", mono_font=False)
        err1 = erratum_tag()
        VGroup(redir, err1).arrange(RIGHT, buff=0.25).move_to([0, gap_y, 0])
        VGroup(redir, err1).align_to(t.box, RIGHT)
        assert rc.get_bottom()[1] - t.box.get_top()[1] > redir.height + 0.1, (rc.get_bottom(), t.box.get_top())

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(ep0), FadeOut(dial0), FadeOut(three), FadeOut(form), FadeOut(ill),
                      track(tr, 2), run_time=0.6)
            self.remove(dial0)
            self.play(FadeIn(rc, shift=DOWN * 0.15), FadeIn(t), FadeIn(where, shift=LEFT * 0.1), run_time=0.6)
            self.play(LaggedStart(*[Indicate(r, color=TURN, scale_factor=1.03) for r in rc.body], lag_ratio=0.25),
                      run_time=1.0)
            vo.wait_until("Typed exactly as written")
            l31 = type_cmd(self, t, C31.cmd, type_time=1.0)
            vo.wait_until("the first one is a shell error")
            out(self, t, [(s, ERR) for s in OUT31], wrap=True, run_time=0.6)
            vo.wait_until("the angle brackets are placeholders")
            last = rows_of(l31)[-1]
            rings = [ring(substring(last, ch), ERR, buff=0.05, stroke=3) for ch in ("<", ">")]
            self.play(*[Create(r) for r in rings], run_time=0.5)
            for r in rings:
                attach(self, last, r)
            vo.wait_until("and the shell takes them as a redirection")
            self.play(FadeIn(redir, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(err1, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, redir)

        # ========================================================== 2. your own names; the order
        nums = VGroup(grey_chip("1 endpoint"), grey_chip("2 endpoint config"), grey_chip("3 model"))
        nums.arrange(RIGHT, buff=0.35).move_to([-6.45 + nums.width / 2, 2.45, 0])
        own = grey_chip("your own name · needs your account · no output shown")
        names = VGroup(label("names:", 20, S.GREY), mono("aws sagemaker list-endpoint-configs", 20, INK),
                       label("·", 20, S.GREY), mono("aws sagemaker list-models", 20, INK)).arrange(RIGHT, buff=0.15)
        names_c = VGroup(box(names.width + 0.5, names.height + 0.3, S.GREY, fill_opacity=0.1), names)
        names.move_to(names_c[0])
        names_c.move_to([-6.45 + names_c.width / 2, nums.get_bottom()[1] - 0.25 - names_c.height / 2, 0])
        own.move_to([-6.45 + own.width / 2, names_c.get_bottom()[1] - 0.22 - own.height / 2, 0])
        assert names_c.get_right()[0] < 6.55 and own.get_bottom()[1] > t.box.get_top()[1] + 0.1, \
            (names_c.get_right(), own.get_bottom(), t.box.get_top())

        with self.voiceover(SAY[2]) as vo:
            self.play(track(tr, 2, extra=True), Indicate(substring(rows_of(l31)[-1], "<your-endpoint-name>"),
                                                         color=TURN, scale_factor=1.06), run_time=0.7)
            self.add(t)
            vo.wait_until("type your own names")
            type_cmd(self, t, C32.cmd, type_time=1.0)
            vo.wait_until("Ours then fails")
            self.play(FadeOut(redir), FadeOut(err1), run_time=0.3)    # its ringed row has scrolled away
            o32 = out(self, t, [(s, ERR) for s in OUT32], wrap=True, run_time=0.6)
            vo.wait_until("no credentials")
            self.play(Indicate(substring(o32[0], "NoCredentials"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.add(t)
            self.play(track(tr, 2), run_time=0.4)
            vo.wait_until("Delete in this order")
            self.play(FadeOut(where), FadeOut(rc, shift=UP * 0.2), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in nums], lag_ratio=0.3),
                      FadeIn(names_c, shift=DOWN * 0.1), run_time=0.7)
            self.play(Indicate(nums[0], color=TURN, scale_factor=1.08), run_time=0.5)
            vo.wait_until("then its configuration")
            l2 = type_cmd(self, t, README_CLI[1], type_time=0.8)
            strike_brackets(self, l2)
            self.play(Indicate(nums[1], color=TURN, scale_factor=1.08), FadeIn(own, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("then the model")
            l3 = type_cmd(self, t, README_CLI[2], type_time=0.7)
            strike_brackets(self, l3)
            self.play(Indicate(nums[2], color=TURN, scale_factor=1.08), run_time=0.6)

        # ========================================================== 3. way 3: python cli.py --delete
        t3 = term(P_APP, rows=7, size=SIZE)
        only = grey_chip("the only way that also removes the tarball")
        only.move_to([6.45 - only.width / 2, 3.22, 0])
        rc3 = readme_card((171, 174), "\n".join(R171), "A", size=20)
        rc3.move_to([-6.45 + rc3.width / 2, 2.75 - rc3.height / 2, 0])
        assert rc3.get_bottom()[1] > t3.box.get_top()[1] + 0.1 and only.get_left()[0] > 0, \
            (rc3.get_bottom(), t3.box.get_top(), only.get_left())
        v = deployed_v5()
        assert v.get_top()[1] < PIC_TOP + 0.01, v.get_top()
        card_bottom = v.card.frame.get_bottom()[1]
        right_limit = min(v.ep.plate.get_left()[0], v.ep.rack.get_left()[0], v.dial.get_left()[0]) - 0.2

        def strip(a: int, b: int, cuts=None):
            p = code("A/cli.py", a, b, font_size=20, dedent=True, cuts=cuts)
            p.move_to([-6.45 + p.width / 2, (card_bottom - 0.2 - 3.5) / 2, 0])
            assert p.get_right()[0] < right_limit and p.get_bottom()[1] > -3.58, (a, p.get_right(), right_limit)
            return p

        p_ep, p_cfg, p_mod, p_art = strip(258, 259, {259: "EndpointName="}), strip(272, 273), strip(285, 286), strip(290, 291)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(t), FadeOut(nums), FadeOut(own), FadeOut(names_c),
                      track(tr, 3), run_time=0.6)
            self.remove(t)
            self.play(FadeIn(t3), FadeIn(rc3, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(only, shift=UP * 0.1), Indicate(rc3.body, color=INK, scale_factor=1.02),
                      run_time=0.5)     # QA 14:46: the chip stays up the whole terminal beat, not 1.5 s
            l30 = type_cmd(self, t3, CMD30, type_time=0.8)
            vo.wait_until("stops at its first SageMaker call")
            r30 = out(self, t3, [OUT30[0], OUT30[1], OUT30[2], (OUT30[3], ERR), OUT30[4], (OUT30[5], ERR)],
                      run_time=0.7)
            self.play(Indicate(substring(r30[3], "paginator.paginate()"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.add(t3)
            vo.wait_until("Pause and run it")
            pin(self, l30, beside(turn_row(), l30))
            self.play(Indicate(only, color=TURN, scale_factor=1.05), run_time=0.5)
            vo.wait_until("With keys")
            self.play(FadeOut(t3), FadeOut(only), FadeOut(rc3), run_time=0.5)
            self.remove(t3)
            self.play(FadeIn(v), FadeIn(p_ep, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("it deletes the endpoint named")
            self.play(Indicate(v.ep.text, color=TURN, scale_factor=1.08), v.dial.sweep(0.1), run_time=0.6)
            v.heal(self)
            v.delete(self, "endpoint", run_time=0.7)
            vo.wait_until("Then come matching configurations")
            self.play(ReplacementTransform(p_ep, p_cfg), run_time=0.5)
            v.delete(self, "config", run_time=0.6)
            vo.wait_until("and the model, by naming convention")
            self.play(ReplacementTransform(p_cfg, p_mod), run_time=0.5)
            v.delete(self, "model", run_time=0.6)
            vo.wait_until("then the tarball in S3")
            self.play(ReplacementTransform(p_mod, p_art), run_time=0.5)
            v.delete(self, "artifact", run_time=0.7)

        # ========================================================== 4. two deploys, one delete (ponder)
        ep1 = endpoint_plate("…-endpoint-<t1>", plate_w=3.4)
        ep2 = endpoint_plate("…-endpoint-<t2>", plate_w=3.4)
        ep1.move_to([-6.45 + ep1.width / 2, 2.55 - ep1.height / 2, 0])
        ep2.move_to([6.45 - ep2.width / 2, 2.55 - ep2.height / 2, 0])
        old_c, new_c = label("older", 20, S.GREY), label("newer", 20, S.GREY)
        old_c.next_to(ep1.dial, RIGHT, buff=0.3)
        new_c.next_to(ep2.dial, RIGHT, buff=0.3)
        js = file_card("endpoint_config.json")
        js.move_to([0, ep1.plate.get_center()[1] - 0.55, 0])
        assert js.get_left()[0] > ep1.get_right()[0] + 0.2 and js.get_right()[0] < ep2.get_left()[0] - 0.2, \
            (ep1.get_right(), js.get_left(), js.get_right(), ep2.get_left())
        p4 = code("A/cli.py", 163, 167, font_size=20, dedent=True)
        p4.move_to([0, -3.5 + p4.height / 2, 0])
        assert p4.get_top()[1] < ep1.get_bottom()[1] - 0.1, (p4.get_top(), ep1.get_bottom())
        ts_bar = line_bar(p4.code, 1, TURN, 0.22)
        name_bar = line_bar(p4.code, 3, TURN, 0.22)

        with self.voiceover(SAY[4]) as vo:
            v.dial.freeze()
            last_turns = v.dial.tracker.get_value()
            self.play(FadeOut(v), FadeOut(p_art), run_time=0.5)
            self.remove(v)
            vo.wait_until("Each deploy makes a new endpoint")
            self.play(FadeIn(p4, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(ep1, shift=DOWN * 0.2), FadeIn(old_c), run_time=0.6)
            self.play(FadeIn(ts_bar), ep1.dial.sweep(0.08), run_time=0.5)
            vo.wait_until("with a new timestamp")
            self.play(FadeIn(ep2, shift=DOWN * 0.2), FadeIn(new_c), ep1.dial.sweep(0.08), run_time=0.6)
            self.play(FadeIn(name_bar), ep1.dial.sweep(0.06), ep2.dial.sweep(0.06), run_time=0.5)
            vo.wait_until("but the JSON file keeps only the last name")
            self.play(FadeIn(js, shift=UP * 0.15), ep1.dial.sweep(0.06), ep2.dial.sweep(0.06), run_time=0.6)
            vo.wait_until("You ran deploy twice")
            self.play(Indicate(ep1.text, color=COST, scale_factor=1.06), Indicate(ep2.text, color=COST, scale_factor=1.06),
                      ep1.dial.sweep(0.08), ep2.dial.sweep(0.08), run_time=0.9)
            vo.wait_until("How many endpoints still bill")
            self.play(FadeOut(p4), FadeOut(ts_bar), FadeOut(name_bar), ep1.dial.sweep(0.05), ep2.dial.sweep(0.05),
                      run_time=0.5)
            self.play(ep1.dial.sweep(0.1), ep2.dial.sweep(0.1), run_time=max(0.5, vo.remaining()))
        card_p = ponder(self, PONDER_Q, seconds=6, center=(0, -1.6))
        assert card_p.get_top()[1] < min(old_c.get_bottom()[1], ep1.dial.get_bottom()[1]) - 0.15, (card_p.get_top(), old_c.get_bottom())

        # ========================================================== 5. one: the older endpoint bills on
        to2 = arrow(js.box.get_right(), ep2.plate.get_left(), S.GREY, buff=0.1)
        ring1 = ring(VGroup(ep1.plate, ep1.rack, ep1.machine, ep1.dial), ERR, buff=0.1, stroke=4)
        forgot = label("forgotten", 24, ERR).next_to(ring1, RIGHT, buff=0.3).align_to(ring1, UP)
        gone_c = card(["its config and model are already gone", "it still bills"], size=20,
                      head="cli.py:268–286")
        gone_c.next_to(forgot, RIGHT, buff=0.3).align_to(ring1, UP)
        t5 = term(P_MD, rows=3, size=SIZE)
        r176 = readme_card(176, README_176, "A")
        r176.move_to([6.45 - r176.width / 2, gone_c.get_bottom()[1] - 0.15 - r176.height / 2, 0])
        chk = grey_chip("extra · needs your account · no output shown")
        chk.move_to([t5.box.get_left()[0] + chk.width / 2, t5.box.get_top()[1] + 0.12 + chk.height / 2, 0])
        assert chk.get_top()[1] < r176.get_bottom()[1] - 0.05 or chk.get_right()[0] < r176.get_left()[0] - 0.2, \
            (chk.get_top(), r176.get_bottom())
        assert r176.get_bottom()[1] > t5.box.get_top()[1] + 0.05, (r176.get_bottom(), t5.box.get_top())
        assert ring1.get_top()[1] < TRACK_BOTTOM - 0.02, ring1.get_top()
        assert gone_c.get_bottom()[1] > r176.get_top()[1] + 0.1 and r176.get_left()[0] > ring1.get_right()[0] + 0.1, \
            (gone_c.get_bottom(), r176.get_top(), r176.get_left(), ring1.get_right())
        assert gone_c.get_right()[0] < 6.55, gone_c.get_right()

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(card_p), run_time=0.5)
            self.remove(card_p)
            self.play(GrowArrow(to2), ep1.dial.sweep(0.05), ep2.dial.sweep(0.05), run_time=0.6)
            vo.wait_until("Delete removes only")
            self.play(Indicate(ep2.text, color=TURN, scale_factor=1.08), ep1.dial.sweep(0.05), ep2.dial.sweep(0.05),
                      run_time=0.6)
            vo.wait_until("the endpoint the file names")
            ep2.dial.freeze()
            self.play(FadeOut(ep2), FadeOut(new_c), FadeOut(to2), FadeOut(js), ep1.dial.sweep(0.08), run_time=0.7)
            self.remove(ep2)
            vo.wait_until("The older one keeps running")
            self.play(Create(ring1), FadeIn(forgot, shift=LEFT * 0.1), ep1.dial.sweep(0.08), run_time=0.7)
            self.play(FadeIn(gone_c, shift=UP * 0.1), ep1.dial.sweep(0.06), run_time=0.5)
            vo.wait_until("Check with")
            self.play(FadeIn(t5), track(tr, 3, extra=True), ep1.dial.sweep(0.05), run_time=0.5)
            l5 = type_cmd(self, t5, "aws sagemaker list-endpoints", type_time=0.8)
            self.play(FadeIn(chk, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and confirm in the console")
            self.play(FadeIn(r176, shift=UP * 0.15), ep1.dial.sweep(0.06), run_time=0.6)
            self.play(Indicate(r176.body, color=INK, scale_factor=1.04), ep1.dial.sweep(0.06), run_time=0.7)
            ep1.dial.run(self, 0.05, max(0.4, vo.remaining()))

        # ========================================================== 6. end of part 1: who runs it all?
        ep1.dial.freeze()
        v6 = ThreeObjects(slots=False)
        d6 = np.array([-ThreeObjects.XS[2], 2.1 - ThreeObjects.Y, 0])
        v6.shift(d6)
        for m in (*v6.slot_list, *v6.slot_caps):   # slots=False: the unadded slots don't move with the piece
            m.shift(d6)
        stopped = CostDial(0.5, caption=None)
        stopped.tracker.set_value(last_turns)
        stopped.needle.update()
        stopped.freeze()
        stopped.face.set_stroke(S.GREY)
        stopped.move_to(v6.p(ThreeObjects.XS[2] + 2.5, ThreeObjects.Y))
        stop_c = label("stopped", 20, S.GREY).next_to(stopped, RIGHT, buff=0.2)
        w = ManualToPipeline(people=True)
        w.shift(DOWN * 0.4)
        qc = question_card(QUESTION, size=24)
        qc.move_to([0, -3.5 + qc.height / 2, 0])
        assert w.get_bottom()[1] > qc.get_top()[1] + 0.1, (w.get_bottom(), qc.get_top())
        assert w.get_top()[1] < v6.slot_list[2].get_bottom()[1] - 0.2, (w.get_top(), v6.slot_list[2].get_bottom())

        with self.voiceover(SAY[6]) as vo:
            self.play(*[FadeOut(m) for m in (ep1, old_c, ring1, forgot, gone_c, t5, r176, chk, tr)],
                      run_time=0.7)
            self.remove(ep1, t5, tr)
            v6.show(self, v6.slot_list[2], run_time=0.6)
            self.play(FadeIn(stopped), FadeIn(stop_c), run_time=0.5)
            vo.wait_until("You ran four commands by hand")
            self.play(Indicate(v6.slot_list[2], color=CLOUD, scale_factor=1.04), run_time=0.7)
            v6.heal(self)
            vo.wait_until("The Cheese App has four stages")
            self.play(LaggedStart(*[FadeIn(VGroup(tl, pp), shift=UP * 0.2) for tl, pp in zip(w.tiles, w.people)],
                                  lag_ratio=0.25), FadeIn(w.links), run_time=1.2)
            self.add(w)
            vo.wait_until("Who runs all of them")
            self.play(FadeIn(qc, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(qc.body[1], color=TURN, scale_factor=1.04), run_time=0.8)

        self.play(*[FadeOut(m) for m in (v6, stopped, stop_c, w, qc)], run_time=0.8)
        self.remove(v6, stopped, stop_c, w, qc)
