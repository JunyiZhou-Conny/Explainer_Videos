"""S09 · Pulumi: desired state, not steps (AC215 L20). No tracker (script.md: S09 has none).
Lecture: 20 · 17 (beats 0-1), 20 · 14 (beats 2-5), 20 · 15 (beat 6), 20 · 16 (beats 7-8).

Beats (script.md "## S09", one voiceover block each):
0. LECTURE 20 · 17. S08's tower of 21 command blocks returns small on the left (GREY, 'steps'); on
   "Each Pulumi program" it Transforms into a GREEN card on the right, 'what should exist': 'a
   firewall: port 80', 'a VM', 'a disk'. On "One firewall rule" the card Transforms into
   CODE(src/deployment/deploy_single_vm/create_instance.py: 51–62). One part lights per phrase: line 51
   `gcp.compute.Firewall(` PURPLE + chip 'constructor'; line 52 `"allow-http"` YELLOW + chip 'logical
   name'; lines 53–61 a GREEN bar and brace 'arguments', then `ports=["80"]`, `source_ranges=["0.0.0.0/0"]`,
   `target_tags=["http-server"]` PINK, one per phrase.
1. LECTURE (held). The chips leave (the colours stay in the code). A GREY-dashed card beside the
   panel, 'lecture's example · slide 17': `Bucket(` / `name,` / `location,` / `website )` with the same
   three coloured bars (no code). On "Running this line" the card leaves, a GREY stamp 'registered'
   lands beside line 51 and an empty BLUE cloud outline appears with a GREY 'nothing created yet'.
2. LECTURE 20 · 14. V4 EngineLoop: the GREY 'Your Machine' box with the PURPLE 'pulumi CLI' and
   `__main__.py`; on "runs your program" the CLI pulses and the resource cards drop into the GREEN
   'desired' tree, which flashes on "a tree of resources".
3. LECTURE (held). The 'state' tree (GREEN, with the small BLUE bucket) and 'reality' (BLUE) slide in;
   the bucket flashes on "from your bucket"; on "The refresh flag" a PINK sweep lines the stale state
   card up with reality.
4. LECTURE (held). On "Then it compares" the desired and state trees flash; on "each difference" the
   glyphs pop (+ ~ - +-) and the plan row fills; each glyph and its plan twin flash on its phrase.
5. LECTURE (held). On "Finally it calls the providers" the plan travels down the PINK arrow to the four
   PURPLE plugs (gcp, docker-build, docker, command), which light, and the BLUE arrow carries the calls
   into reality. On "The banner on the slide" the banner writes under the picture.
6. LECTURE 20 · 15. V4 turns into its compact form on the left. A card of seven commands ('pulumi' +
   new · up · preview · destroy · stack · config · refresh); stack, config, preview, up, destroy light
   YELLOW one by one; refresh is YELLOW-outlined with a chip 'as the --refresh flag'; new turns GREY
   with a chip 'both projects already exist'.
7. LECTURE 20 · 16. The card leaves, V4 (compact) moves down. A wide strip
   `pulumi up --stack dev --refresh -y`; `up` PURPLE ('preview, ask, apply'), `--stack dev` GREEN
   ('which environment'), `--refresh` PINK ('sync state with reality first') light on their phrases;
   V4 replays the refresh sweep.
8. LECTURE (held). `-y` lights YELLOW; a GREY dialog 'Do you want to perform this update?' with
   yes / no pops; a YELLOW pointer travels from `-y` and clicks 'yes'; a RED-outlined chip 'your chance
   to check the plan' appears and fades. On "Preview stops" a second strip
   `pulumi preview --stack dev --refresh` appears, V4 shows the plan glyphs and a GREY stop sign
   'nothing applied'.
9. The strips leave; V4 back at full size, all three trees identical, the plan box empty, the
   providers dark. PONDER(8 s).
10. The trees glow GREEN together, a GREEN 'desired = state = reality' line, the plan says 'no
   changes'; the arrow and plugs stay dark. A YELLOW sticky 'hold that thought: S13' bottom right.
   Fade; empty frame.

Deviations from SHOW:
- Beat 1: the chips of beat 0 leave before the bucket card comes (the colours stay in the code), so
  the panel, the card and later the cloud stay within three groups; the stamp sits right of line 51
  (the line is the panel's widest but one, no room inside it).
- Beat 6: 'V4 shrinks left' is a Transform into EngineLoop(compact=True) (text never scales below 1).
- Beats 7-8: the compact V4 sits under the strips; its plan is its glyph column (the compact piece has
  no plan box), and the stop sign 'nothing applied' stands right of the trees.
- Beat 9: the full V4 is rebuilt around the compact trees (machine box, an empty plan box, dark
  provider plugs and a dark arrow) so that nothing on screen during the timer shows the answer.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _panel

SAY = NARRATION["S09"]

SRC = "src/deployment/deploy_single_vm/create_instance.py"
KEYS = ("desired", "state", "reality")

# the code panel's highlighted parts (k = file line - 51), asserted against the source
PARTS = {"ctor": (0, "gcp.compute.Firewall("), "name": (1, '"allow-http"'),
         "ports": (6, 'ports=["80"]'), "src": (9, 'source_ranges=["0.0.0.0/0"]'),
         "tags": (10, 'target_tags=["http-server"]')}
_lines = excerpt(SRC, 51, 62).split("\n")
for _k, _s in PARTS.values():
    assert _s in _lines[_k], (_k, _s, _lines[_k])
assert "Firewall(" in _lines[0] and _lines[-1].strip() == ")"


def heads_and_cards(e) -> list:
    """The trees of an EngineLoop as one ordered list (heads, then cards row by row), + its bucket."""
    out_ = [e.heads[k] for k in KEYS]
    for k in KEYS:
        out_ += list(e.cards[k])
    return out_


def seat_trees(e, with_bucket: bool = True):
    """Make the three trees (and the state bucket) parts of `e` without playing anything."""
    for m in heads_and_cards(e):
        e.add(m)
    if with_bucket:
        e.bucket = pail(0.45, CLOUD, rim=OWN).next_to(e.heads["state"], RIGHT, buff=0.18)
        e.add(e.bucket)
    e.stale = None


def cmd_strip(s: str, size: float = 28) -> VGroup:
    """A command on a dark strip (not a terminal: the README's command decoded). .line .frame"""
    ln = mono_line(s, size, INK)
    fr = RoundedRectangle(width=ln.width + 0.7, height=ln.height + 0.42, corner_radius=0.12,
                          stroke_color=S.GREY, stroke_width=2.5).set_fill(PANEL, 1)
    ln.move_to(fr)
    g = VGroup(fr, ln)
    g.frame, g.line = fr, ln
    return g


def stop_sign(text: str = "nothing applied") -> VGroup:
    """The GREY stop sign of EngineLoop.preview_stop, free-standing."""
    oct_ = Circle(radius=0.22, stroke_color=S.GREY, stroke_width=3).set_fill(tint(S.GREY, 0.3), 1)
    bar = Line(LEFT * 0.12, RIGHT * 0.12, color=INK, stroke_width=5)
    return VGroup(VGroup(oct_, bar), label(text, 20, S.GREY)).arrange(RIGHT, buff=0.12)


def pointer(color=TURN) -> Polygon:
    """A YELLOW mouse pointer (tip at its top-left point)."""
    pts = [[0, 0, 0], [0, -0.5, 0], [0.12, -0.39, 0], [0.22, -0.6, 0], [0.31, -0.56, 0], [0.21, -0.35, 0],
           [0.37, -0.35, 0]]
    return Polygon(*pts, stroke_color=color, stroke_width=2).set_fill(color, 1)


def button(s: str, color=S.GREY) -> VGroup:
    t = label(s, 22, INK)
    b = RoundedRectangle(width=max(1.1, t.width + 0.5), height=0.5, corner_radius=0.08, stroke_color=color,
                         stroke_width=2.5).set_fill(PANEL, 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def note2(rows, color=S.GREY, size: float = 20) -> VGroup:
    """A small two-row chip (outline in `color`)."""
    t = VGroup(*[label(r, size, INK) if isinstance(r, str) else r for r in rows]).arrange(DOWN, buff=0.08)
    b = RoundedRectangle(width=t.width + 0.45, height=t.height + 0.3, corner_radius=0.14, stroke_color=color,
                         stroke_width=2.5).set_fill(tint(color, 0.12), 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


class DesiredState(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S09"] == 11, len(SAY)
        self.camera.background_color = S.BG

        # ------------------------------------------------------------ 0 · what should exist (slide 17)
        with self.voiceover(SAY[0]) as vo:
            ref = lref("17")
            blocks = VGroup(*[Rectangle(width=1.6, height=0.1, stroke_color=S.GREY, stroke_width=1.5)
                              .set_fill(tint(S.GREY, 0.45), 1) for _ in range(21)])
            blocks.arrange(UP, buff=0.03).move_to([-4.6, 0.0, 0])
            base = Line(blocks.get_corner(DL) + LEFT * 0.2 + DOWN * 0.06,
                        blocks.get_corner(DR) + RIGHT * 0.2 + DOWN * 0.06, color=S.GREY, stroke_width=3)
            steps_t = label("steps", 24, S.GREY).next_to(base, DOWN, buff=0.2)
            self.play(FadeIn(ref), LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in blocks], lag_ratio=0.04),
                      FadeIn(base), FadeIn(steps_t), run_time=1.0)

            want = card(["a firewall: port 80", "a VM", "a disk"], color=OWN, size=28, head="what should exist")
            want.frame.set_stroke(OWN)
            want.move_to([2.6, 0.0, 0])
            vo.wait_until("Each Pulumi program")
            self.play(ReplacementTransform(VGroup(blocks, base), want.frame),
                      ReplacementTransform(steps_t, want[1]), run_time=1.1)
            self.remove(want.frame, want[1])
            self.add(want)
            vo.wait_until("not what to do")
            self.play(Indicate(want.head, color=OWN, scale_factor=1.12), run_time=0.7)

            p = code(SRC, 51, 62, dedent=True)
            p.move_to(ORIGIN)
            p.shift(np.array([-6.4 - p.code.get_left()[0], 2.75 - p.get_top()[1], 0]))
            vo.wait_until("One firewall rule")
            self.play(FadeTransform(want, p), run_time=1.1)

            cx = p.code.get_right()[0] + 0.45

            def span(key):
                k, s = PARTS[key]
                return code_span(p.code, k, s)

            ctor = span("ctor")
            ctor_chip = tool_chip("constructor", mono_font=False)
            ctor_chip.move_to([cx + ctor_chip.width / 2, ctor.get_center()[1], 0])
            vo.wait_until("a constructor")
            self.play(ctor.animate.set_color(TOOL), FadeIn(ctor_chip, shift=LEFT * 0.2), run_time=0.6)
            self.add(p)
            self.play(Indicate(ctor, color=TOOL, scale_factor=1.06), run_time=0.6)
            self.add(p)

            name = span("name")
            name_chip = chip("logical name", TURN, size=20)
            name_chip.move_to([ctor_chip.get_right()[0] + 0.3 + name_chip.width / 2, name.get_center()[1] - 0.12, 0])
            lead = Line(name.get_right() + RIGHT * 0.25, name_chip.get_left() + LEFT * 0.08, color=TURN,
                        stroke_width=2.5)
            lead.put_start_and_end_on(np.array([name.get_right()[0] + 0.35, name.get_center()[1], 0]),
                                      np.array([name_chip.get_left()[0] - 0.08, name.get_center()[1], 0]))
            vo.wait_until("a logical name")
            self.play(name.animate.set_color(TURN), Create(lead), FadeIn(name_chip, shift=LEFT * 0.2), run_time=0.6)
            self.add(p)

            arg_lines = VGroup(*[p.code.code_lines[k] for k in range(2, 11)])
            arg_bar = Rectangle(width=p.code.background.width - 0.12, height=arg_lines.height + 0.16,
                                stroke_width=0).set_fill(OWN, 0.12).move_to(
                [p.code.background.get_center()[0], arg_lines.get_center()[1], 0])
            brace = Brace(arg_lines, RIGHT, buff=0.15, color=OWN)
            brace.move_to([cx + brace.width / 2 - 0.1, arg_lines.get_center()[1] - 0.05, 0])
            args_t = label("arguments", 24, OWN).next_to(brace, RIGHT, buff=0.15)
            vo.wait_until("and arguments")
            self.play(FadeIn(arg_bar), GrowFromCenter(brace), FadeIn(args_t, shift=LEFT * 0.2), run_time=0.7)
            pinks = []
            for key, ph in (("ports", "port 80"), ("src", "from anywhere"), ("tags", "for VMs tagged")):
                sp = span(key)
                pinks.append(sp)
                vo.wait_until(ph)
                rg = ring(sp, ROUTE, buff=0.06)
                self.play(sp.animate.set_color(ROUTE), Create(rg), run_time=0.5)
                self.add(p)
                self.play(FadeOut(rg), run_time=0.3)

        # ------------------------------------------------------------ 1 · the bucket, and nothing created yet
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(ctor_chip), FadeOut(name_chip), FadeOut(lead), FadeOut(brace), FadeOut(args_t), FadeOut(arg_bar),
                      run_time=0.5)
            rows = [("Bucket(", TOOL), ("  name,", TURN), ("  location,", OWN), ("  website )", OWN)]
            body = VGroup(*[mono_line(s, 24, INK) for s, _ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            bars = VGroup(
                Line(body[0].get_corner(UL), body[0].get_corner(DL), color=TOOL, stroke_width=6),
                Line(body[1].get_corner(UL), body[1].get_corner(DL), color=TURN, stroke_width=6),
                Line(body[2].get_corner(UL), body[3].get_corner(DL), color=OWN, stroke_width=6))
            bars.shift(LEFT * 0.18)
            hd = label("lecture's example · slide 17", 20, S.GREY)
            inner = VGroup(hd, VGroup(bars, body)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            fr = outline_box(inner.width + 0.6, inner.height + 0.5, PAST, solid=False)
            bucket_card = VGroup(fr, inner)
            fr.move_to([cx + fr.width / 2 + 0.1, 0.4, 0])
            inner.move_to(fr)
            vo.wait_until("bucket example")
            self.play(FadeIn(fr), FadeIn(hd), run_time=0.5)
            self.play(LaggedStart(*[AnimationGroup(Create(b_), FadeIn(r_)) for b_, r_ in
                                    zip(bars, [body[0], body[1], VGroup(body[2], body[3])])], lag_ratio=0.35),
                      run_time=1.2)
            vo.wait_until("the same shape")
            shape = VGroup(ring(ctor, TOOL, buff=0.06), ring(name, TURN, buff=0.06),
                           ring(VGroup(*[p.code.code_lines[k] for k in range(2, 11)]), OWN, buff=0.06),
                           ring(body[0], TOOL, buff=0.06), ring(body[1], TURN, buff=0.06),
                           ring(VGroup(body[2], body[3]), OWN, buff=0.06))
            self.play(LaggedStart(*[Create(r_) for r_ in shape], lag_ratio=0.15), run_time=0.9)
            self.play(FadeOut(shape), run_time=0.4)

            stamp = tag("registered", S.GREY, size=22).rotate(6 * DEGREES)
            stamp.move_to([cx + stamp.width / 2 + 0.05, ctor.get_center()[1] + 0.02, 0])
            sky = cloud_shape(None, CLOUD, cloud_w=2.6)
            sky.shape.set_fill(opacity=0)
            sky.move_to([cx + 1.6, -0.5, 0])
            empty_t = label("nothing created yet", 22, S.GREY).next_to(sky, DOWN, buff=0.2)
            vo.wait_until("Running this line")
            self.play(FadeOut(bucket_card), run_time=0.4)
            self.play(FadeIn(stamp, scale=1.6), Indicate(p.code.code_lines[0], color=TOOL, scale_factor=1.03),
                      run_time=0.6)
            self.add(p)
            self.play(Create(sky.shape), run_time=0.7)
            self.play(FadeIn(empty_t, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("the constructor only")
            self.play(stamp.animate(rate_func=there_and_back).scale(1.18), run_time=0.7)

        # ------------------------------------------------------------ 2 · slide 14: program -> desired
        with self.voiceover(SAY[2]) as vo:
            ref14 = lref("14")
            self.play(FadeOut(p), FadeOut(stamp), FadeOut(sky), FadeOut(empty_t), FadeOut(ref), run_time=0.6)
            e = EngineLoop()
            self.play(FadeIn(ref14), run_time=0.3)
            e.machine(self)
            vo.wait_until("the command line tool")
            self.play(Indicate(e.cli, color=TOOL, scale_factor=1.12), run_time=0.6)
            vo.wait_until("runs your program")
            self.play(Indicate(e.file, color=OWN, scale_factor=1.08), run_time=0.5)
            e.run(self)
            vo.wait_until("a tree of resources")
            tr = ring(VGroup(e.heads["desired"], *e.cards["desired"]), OWN, buff=0.15, stroke=4)
            self.play(Create(tr), Indicate(e.heads["desired"], color=OWN), run_time=0.9)
            e.heal(self)
            self.play(FadeOut(tr), run_time=0.4)

        # ------------------------------------------------------------ 3 · state and reality, --refresh
        with self.voiceover(SAY[3]) as vo:
            vo.wait_until("Pulumi also loads")
            e.trees(self, stale=1)
            vo.wait_until("from your bucket")
            self.play(Indicate(e.bucket, color=CLOUD, scale_factor=1.3), run_time=0.6)
            e.heal(self)
            vo.wait_until("The refresh flag")
            e.refresh(self, run_time=1.2)
            sr = ring(VGroup(e.cards["state"][1], e.cards["reality"][1]), OWN, buff=0.1, stroke=4)
            self.play(Create(sr), run_time=0.5)
            self.play(FadeOut(sr), run_time=0.4)

        # ------------------------------------------------------------ 4 · diff -> plan
        with self.voiceover(SAY[4]) as vo:
            vo.wait_until("Then it compares")
            cmp_r = VGroup(*[ring(VGroup(e.heads[k], *e.cards[k]), OWN, buff=0.15, stroke=4)
                             for k in ("desired", "state")])
            self.play(LaggedStart(*[Create(r_) for r_ in cmp_r], lag_ratio=0.3), run_time=0.9)
            self.play(FadeOut(cmp_r), run_time=0.4)
            vo.wait_until("each difference")
            gl = e.diff(self, ("+", "~", "-", "+-"), run_time=0.9)
            plan_row = e.plan.row
            self.play(Indicate(plan_row, color=INK, scale_factor=1.15), run_time=0.5)
            e.heal(self)
            for i, ph in enumerate(("plus to create", "tilde to update", "minus to delete", "plus minus")):
                vo.wait_until(ph)
                col = GLYPH_COL[("+", "~", "-", "+-")[i]]
                self.play(Indicate(gl[i], color=col, scale_factor=1.6), Indicate(plan_row[i], color=col,
                                                                                 scale_factor=1.5), run_time=0.6)
                e.heal(self)

        # ------------------------------------------------------------ 5 · providers, the banner
        with self.voiceover(SAY[5]) as vo:
            vo.wait_until("Finally it calls")
            e.apply(self, run_time=1.4)
            vo.wait_until("which make the API calls")
            self.play(Indicate(e.flow, color=ROUTE, scale_factor=1.05), run_time=0.7)
            e.heal(self)
            vo.wait_until("The banner on the slide")
            e.banner(self, run_time=0.8)
            vo.wait_until("Pulumi manages")
            self.play(Indicate(e.banner_m, color=INK, scale_factor=1.06), run_time=0.8)
            e.heal(self)

        # ------------------------------------------------------------ 6 · slide 15: seven commands
        with self.voiceover(SAY[6]) as vo:
            ref15 = lref("15")
            ce = EngineLoop(compact=True)
            seat_trees(ce)
            ce.shift(np.array([-3.15, 0.0, 0]) - ce.ref.get_center())
            src = heads_and_cards(e) + [e.bucket]
            tgt = heads_and_cards(ce) + [ce.bucket]
            src_set = set(src)
            others = [m for m in e.submobjects if m not in src_set]
            self.remove(e)
            self.add(*e.submobjects)
            self.play(*[ReplacementTransform(a, b) for a, b in zip(src, tgt)], *[FadeOut(m) for m in others],
                      FadeOut(ref14), FadeIn(ref15), run_time=1.0)
            self.remove(*tgt, *others)
            self.add(ce)

            names = ("new", "up", "preview", "destroy", "stack", "config", "refresh")
            hd = mono("pulumi", 24, TOOL)
            rws = VGroup(*[mono_line(n, 24, INK) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
            inner = VGroup(hd, rws).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            rws.shift(RIGHT * 0.3)
            frame = box(inner.width + 0.9, inner.height + 0.6, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
            frame.move_to([0.45 + frame.width / 2, 0.0, 0])
            inner.move_to(frame)
            cmds = VGroup(frame, inner)
            vo.wait_until("seven commands")
            self.play(FadeIn(frame), FadeIn(hd), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rws],
                                                              lag_ratio=0.12), run_time=1.0)
            vo.wait_until("The tutorial uses five")
            five = [names.index(n) for n in ("stack", "config", "preview", "up", "destroy")]
            hls = VGroup()
            for i in five:
                hls.add(hl_bar(rws[i], TURN, 0.22, buff=0.08))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(hls[j]), rws[i].animate.set_color(TURN))
                                    for j, i in enumerate(five)], lag_ratio=0.5),
                      run_time=max(1.2, vo.until("with refresh only") - 0.1))
            r_i = names.index("refresh")
            r_ring = ring(rws[r_i], TURN, buff=0.08)
            r_chip = grey_chip("as the --refresh flag")
            nx = frame.get_right()[0] + 0.25
            r_chip.move_to([nx + r_chip.width / 2, rws[r_i].get_center()[1], 0])
            vo.wait_until("with refresh only")
            self.play(Create(r_ring), FadeIn(r_chip, shift=LEFT * 0.2), run_time=0.6)
            n_chip = note2(["both projects", "already exist"])
            n_chip.move_to([nx + n_chip.width / 2, rws[0].get_center()[1] - 0.1, 0])
            vo.wait_until("The command new")
            self.play(rws[0].glyphs.animate.set_color(S.GREY).set_opacity(0.6), FadeIn(n_chip, shift=LEFT * 0.2),
                      run_time=0.6)
            vo.wait_until("because both projects")
            self.play(Indicate(n_chip, color=S.GREY, scale_factor=1.06), run_time=0.6)

        # ------------------------------------------------------------ 7 · slide 16: pulumi up decoded
        with self.voiceover(SAY[7]) as vo:
            ref16 = lref("16")
            strip = cmd_strip("pulumi up --stack dev --refresh -y")
            strip.move_to([0, 2.15, 0])
            ln = strip.line
            self.play(FadeOut(cmds), FadeOut(hls), FadeOut(r_ring), FadeOut(r_chip), FadeOut(n_chip),
                      FadeOut(ref15), FadeIn(ref16), ce.animate.shift(np.array([0.25, -2.0, 0])), run_time=0.8)
            vo.wait_until("pulumi up, stack dev")
            self.play(FadeIn(strip.frame), LaggedStart(*[FadeIn(gl_) for gl_ in ln.glyphs], lag_ratio=0.08), run_time=1.3)
            self.remove(ln)
            self.add(strip)

            def lab(sub, text, color, y):
                g = substring(ln, sub)
                t = label(text, 22, color)
                t.move_to([g.get_center()[0], y, 0])
                keep_inside(t)
                tick = Line([g.get_center()[0], strip.frame.get_bottom()[1] - 0.05, 0],
                            [g.get_center()[0], t.get_top()[1] + 0.08, 0], color=color, stroke_width=2.5)
                return g, VGroup(tick, t)

            g_up, l_up = lab("up", "preview, ask, apply", TOOL, 1.15)
            g_st, l_st = lab("--stack dev", "which environment", OWN, 0.45)
            g_rf, l_rf = lab("--refresh", "sync state with reality first", ROUTE, 1.15)
            assert l_up[1].get_right()[0] < l_rf[1].get_left()[0] - 0.2
            for g, l_, col, ph in ((g_up, l_up, TOOL, "Up previews"), (g_st, l_st, OWN, "Stack dev picks"),
                                   (g_rf, l_rf, ROUTE, "Refresh syncs")):
                vo.wait_until(ph)
                self.play(g.animate.set_color(col), Create(l_[0]), FadeIn(l_[1], shift=DOWN * 0.1), run_time=0.6)
                self.add(strip)
            ce.stale = 1
            sc = ce.cards["state"][1]
            self.play(sc.box.animate.set_stroke(S.GREY).set_fill(tint(S.GREY, 0.12), 1),
                      sc.text.animate.set_color(S.GREY), run_time=0.4)
            ce.heal(self)
            ce.refresh(self, run_time=1.0)

        # ------------------------------------------------------------ 8 · -y, and preview
        with self.voiceover(SAY[8]) as vo:
            g_y = substring(ln, "-y")
            self.play(FadeOut(l_up), FadeOut(l_st), FadeOut(l_rf), g_y.animate.set_color(TURN), run_time=0.5)
            self.add(strip)
            ybar = ring(g_y, TURN, buff=0.08)
            self.play(Create(ybar), run_time=0.4)
            dlg = box(5.6, 2.1, S.GREY, fill=PANEL, fill_opacity=1).move_to([3.5, -1.85, 0])
            q = label("Do you want to perform this update?", 22, INK)
            q.move_to(dlg.get_top() + DOWN * 0.5)
            yes, no = button("yes"), button("no")
            VGroup(yes, no).arrange(RIGHT, buff=0.4).move_to(dlg.get_center() + DOWN * 0.4)
            dialog = VGroup(dlg, q, yes, no)
            vo.wait_until("answers yes")
            self.play(FadeIn(dialog, scale=0.95), run_time=0.6)
            ptr = pointer().move_to(g_y.get_center() + DOWN * 0.45 + RIGHT * 0.15, aligned_edge=UL)
            self.play(FadeIn(ptr), run_time=0.3)
            self.play(ptr.animate.move_to(yes.get_center() + RIGHT * 0.3 + DOWN * 0.05, aligned_edge=UL),
                      run_time=0.9)
            self.play(yes.box.animate.set_fill(tint(TURN, 0.5), 1).set_stroke(TURN), run_time=0.3)
            chance = chip("your chance to check the plan", ERR, size=22, fill_opacity=0.12)
            chance.next_to(dlg, UP, buff=0.25).align_to(dlg, RIGHT)
            vo.wait_until("and skips your chance")
            self.play(FadeIn(chance, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(chance, color=ERR, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Step 3 shows")
            self.play(chance.animate.set_opacity(0.25), run_time=0.8)
            strip2 = cmd_strip("pulumi preview --stack dev --refresh")
            strip2.move_to([0, 1.05, 0])
            vo.wait_until("Preview stops")
            self.play(FadeOut(dialog), FadeOut(ptr), FadeOut(chance), FadeIn(strip2, shift=DOWN * 0.15),
                      run_time=0.6)
            g_pv = substring(strip2.line, "preview")
            self.play(g_pv.animate.set_color(TOOL), run_time=0.3)
            self.add(strip2)
            ce.diff(self, ("+", "~", None, None), run_time=0.6)
            stop = stop_sign().move_to([2.2, ce.cards["desired"].get_center()[1], 0])
            self.play(FadeIn(stop, shift=LEFT * 0.15), run_time=0.5)

        # ------------------------------------------------------------ 9 · the question (full V4 again)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(strip), FadeOut(ybar), FadeOut(strip2), FadeOut(stop), FadeOut(ref16), run_time=0.5)
            ce.clear_glyphs(self)
            e2 = EngineLoop()
            seat_trees(e2)
            src = heads_and_cards(ce) + [ce.bucket]
            tgt = heads_and_cards(e2) + [e2.bucket]
            others = [m for m in ce.submobjects if m not in set(src)]
            self.remove(ce)
            self.add(*ce.submobjects)
            self.play(*[ReplacementTransform(a, b) for a, b in zip(src, tgt)], *[FadeOut(m) for m in others],
                      run_time=0.9)
            self.remove(*tgt, *others)
            self.add(e2)
            e2.machine(self, run_time=0.5)
            pf = _panel(3.8, 0.75, S.GREY, 0.05).move_to(e2.p(-4.3, -1.98))
            pt = label("plan", 20, S.GREY).move_to(e2.p(-6.0, -1.98), aligned_edge=LEFT)
            plan = VGroup(pf, pt)
            plan.row = VGroup()
            plan.add(plan.row)
            plugs = VGroup(*[tool_chip(n) for n in PROVIDERS]).arrange(RIGHT, buff=0.22).move_to(e2.p(2.3, -1.98))
            plugs.set_opacity(0.35)
            dark = route(pf.get_right(), plugs.get_left()).set_opacity(0.3)
            e2.show(self, plan, plugs, dark, run_time=0.6)
            e2.plan = plan
            vo.wait_until("What should the plan")
            self.play(Indicate(pf, color=TURN, scale_factor=1.05), run_time=0.7)
            e2.heal(self)
        card_p = ponder(self, "You run pulumi up again,\nchanged nothing.\nWhat should the plan show?", 8)

        # ------------------------------------------------------------ 10 · in sync: no changes
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(card_p), run_time=0.5)
            vo.wait_until("Desired equals state")
            e2.in_sync(self, run_time=0.8)
            eq = label("desired = state = reality", 24, OWN).move_to(e2.p(-1.6, -3.0))
            glow = VGroup(*[ring(VGroup(e2.heads[k], *e2.cards[k]), OWN, buff=0.15, stroke=5) for k in KEYS])
            self.play(LaggedStart(*[Create(g_) for g_ in glow], lag_ratio=0.2), FadeIn(eq, shift=UP * 0.1),
                      run_time=1.0)
            self.play(FadeOut(glow), run_time=0.5)
            vo.wait_until("so there is no difference")
            self.play(Indicate(e2.plan.row, color=S.GREY, scale_factor=1.2), run_time=0.7)
            e2.heal(self)
            vo.wait_until("and nothing is created")
            self.play(Indicate(dark, color=S.GREY, scale_factor=1.05), run_time=0.7)
            e2.heal(self)
            note_s = sticky("hold that thought: S13").move_to([4.85, -3.0, 0])
            vo.wait_until("Hold that thought")
            self.play(FadeIn(note_s, shift=UP * 0.15, scale=0.8), run_time=0.6)
            self.play(Indicate(note_s, color=TURN, scale_factor=1.08), run_time=0.6)

        self.play(FadeOut(e2), FadeOut(eq), FadeOut(note_s), run_time=0.6)
        self.wait(0.3)
