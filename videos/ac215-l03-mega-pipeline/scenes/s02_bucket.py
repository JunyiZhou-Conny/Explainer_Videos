"""S02 · The bucket is the message bus (concept scene: no README tracker).

Beats (script.md "## S02", one voiceover block each):
0. A GREY README card (README.md · lines 60–67: lines 61 and 63, quoted) condenses into two
   rows. Top: "production: services call each other's APIs", five small TEAL boxes joined by
   direct GREY arrows (A→B, B→C, B→D over C, D→E); the arrows fade and each gets a GREY cross.
   Bottom: "here: write outputs to shared storage; the next stage reads them", the same boxes
   (copied down) over a small BLUE cabinet; on the words, every box writes into a drawer, then
   reads from one (thin GREY arrows, always box↔drawer).
1. The small row grows into V1 (Relay, standing on the frame's foot). A GREY README card
   (README.md · lines 74–80: the seven prefixes in the README's order, two columns) writes in
   above; letter by letter each prefix flies down into its drawer's two-line label (pipeline
   order, so text_translated/ and text_audios/ cross), output_audios_pp/ into the dashed bonus
   drawer (tag "bonus"); the content icons fade in; the card leaves and V1 rises to the middle;
   tag "illustration" on the cabinet. A's letter and name appear; a copy of the waveform rises
   from input_audios/ into A (A's label dims while it is inside) and comes out as a short page
   into text_prompts/; then B: a long page into text_paragraphs/.
2. "The path splits": two copies of the long page slide out of text_paragraphs/. C's label; one
   copy through C into text_audios/ as a waveform. D's label; the other through D into
   text_translated/ as an FR page; E's label; through E into output_audios/ as a waveform. The
   reads and writes fade in as thin arrows (every one box↔drawer); GREY caption under V1: "every
   arrow goes through a drawer".
3. The caption becomes "you run each one, by hand"; a small GREY hand taps A, then B, then C.
4. Zoom: text_prompts/ grows into one big BLUE drawer while the rest of V1 fades. The PINK object
   name writes across it as it is spoken: text_prompts, /group-01, /input-….txt (each slash
   pulses as it is said); on "one single object name" both slashes pulse again and a PINK
   underline spans the whole name; caption "one object name · no real folders"; tag
   "illustration".
5. The drawer leaves; the PINK name moves to the top. Row A ("A uploads"): CODE(transcribe_audio/
   cli.py: 112) at 20 pt, then under it the excerpt chip of line 108 (20 pt); the parts turn PINK
   and underline as they are said (prefix, group name, file name: each with its part of the name
   pulsing; then "input-*.txt"). Row B ("B downloads", its header under the chip): the excerpt
   chip of generate_text/cli.py line 42, placed so {group_name} is under group_name; three PINK
   connectors join text_prompts ↔ {text_prompts}, group_name ↔ {group_name}, "input-*.txt" ↔
   input-*.txt; then both rows collapse upward into the PINK name.
6. The name opens into SubDrawers (text_prompts/ → the title, group-01/ → the first sub-drawer,
   the file → a page in it); GREY pages (other teams' work) in group-02/, group-03/ and "default
   group"; tag "illustration". A TEAL box with the GREY tag "group_name unchanged" drops a page
   into "default group", which turns and flashes RED; the GREY page under it flashes RED and fades
   (someone else's work). GREY README card README.md · line 124: "Set your group name inside
   cli.py before you run each component."
7. A schematic leaderboard (tag illustration; caption "ac215-mega-pipeline.dlops.io · README.md
   line 54"): a few cells of group-02/03 are lit; on "lights up your row" group-01's row name
   pulses YELLOW and two of its cells light GREEN. Then the leaderboard leaves, V1 returns on the
   frame's foot (all labels, all arrows), and the GOLD tag "billed to the course project" slides in
   under the cabinet.
8. V1 full; the GOLD tag leaves; every read arrow, then every write arrow, pulses YELLOW (look at
   reads and writes; no answer). PONDER(8 s) above V1 (the toolkit's card with less padding so it
   fits over V1; the question on two lines).
9. The card leaves. C's and D's input arrows turn YELLOW and pulse from text_paragraphs/ (the
   drawer pulses), a YELLOW brace "side by side" over C and D; then D's write arrow and E's read
   arrow pulse through text_translated/, a YELLOW clock "waits for D" above E (its hand turns).
   Fade out to an empty frame.

Deviation: in beat 5 the line-112 panel sits above the line-108 chip (SHOW: 108 above 112). The
SAY names 112's parts first (prefix, group name, file name) and 108's last ("only files starting
with input"), and all three connectors run from line 108 to line 42, so 108 sits next to B's chip
and no connector crosses a panel.

Source lines: README.md 54, 61, 63, 74–80, 124; transcribe_audio/cli.py 108 (excerpt) and 112;
generate_text/cli.py 42 (excerpt), all read from assets/source and asserted below.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import PANEL, code_span, cross_mark, glyph_range, label, line_pitch, mono, \
    mono_line, substring
from explainer.scene import VoiceScene

from common import (BONUS_PREFIX, CLOUD, clock_glyph, COST, CTR, ERR, INK, LOOKUP, NARRATION, OUT_KIND, PREFIXES,
                    README_PREFIXES, TURN, WRITES, Leaderboard, Relay, SubDrawers, _set_op, cost_tag,
                    excerpt, illustration_tag, page_token, readme_card, sans, source_text, src_panel)

SAY = NARRATION["S02"]

# ------------------------------------------------------------------ the sources (asserted)
README = source_text("README.md").split("\n")
assert README[60].startswith("In a production pipeline, containerized services talk to each other "
                             "through APIs,"), README[60]
assert "communicate indirectly by writing their outputs to storage**, which the next stage will then " \
       "read as input." in README[62], README[62]
assert [ln.split("`")[1] for ln in README[73:80]] == README_PREFIXES
assert "Set your group name inside `cli.py` before you run each component." in README[123]
assert "ac215-mega-pipeline.dlops.io" in README[53]
README_6067 = ["In a production pipeline, containerized services talk to each other through APIs, …",
               "… components will communicate indirectly by writing their outputs to storage,",
               "which the next stage will then read as input."]
README_124 = "Set your group name inside cli.py before you run each component."

UPLOAD_PATH, UPLOAD_LINE = "transcribe_audio/cli.py", 112
GLOB_LINE = 108
GLOB = 'glob.glob(os.path.join(text_prompts, group_name, "input-*.txt"))'
DOWNLOAD_PATH, DOWNLOAD_LINE = "generate_text/cli.py", 42
MATCH = 'match_glob=f"{text_prompts}/{group_name}/input-*.txt"'
assert excerpt(UPLOAD_PATH, UPLOAD_LINE, UPLOAD_LINE).strip() == \
    "destination_blob_name = os.path.join(text_prompts, group_name, filename)"

OBJECT = "text_prompts/group-01/input-….txt"     # never a real file name: they are not known
PONDER_Q = ("Look at which drawer each stage reads and writes.\n"
            "Which two stages could run at the same time, and which one has to wait?")

RELAY_BOTTOM = -3.5          # V1 on the frame's foot while a card or the ponder needs the band above
CAP_Y = -3.05                # captions under V1 while it stands centred (beats 2-3)


# ------------------------------------------------------------------ small pictures
def unhide(piece, *mobs):
    """Give hidden members of a set piece back their saved opacity (just before a transform or a
    FadeIn brings them in), and mark their parts shown."""
    for m in mobs:
        _set_op(m)
        piece._flag(m, False)


def retip(edges, tip: float):
    """Give every edge arrow of a Relay the same tip length (the shared piece caps a tip at 0.18
    of its arrow's length, so the one long edge, text_paragraphs/ -> D, got a tip twice the size
    of the others'). The edges are hidden members: they stay hidden."""
    for e in edges:
        e.become(Arrow(e.get_start(), e.get_end(), buff=0, stroke_width=2.5, color=S.GREY, tip_length=tip,
                       max_tip_length_to_length_ratio=1, max_stroke_width_to_length_ratio=10))
        _set_op(e, 0)


def excerpt_chip(path: str, n: int, expr: str, header_below: bool = False) -> VGroup:
    """An excerpt chip (script.md conventions): the exact sub-expression of `path` line n in a
    code-panel-styled chip (mono 20), headed "path · line n (excerpt)". .frame .code .header"""
    assert expr in excerpt(path, n, n), (path, n, expr)
    code = mono_line(expr, 20, INK)
    fr = RoundedRectangle(width=code.width + 0.5, height=code.strut.height + 0.3, corner_radius=0.12,
                          stroke_color=S.GREY_DARK, stroke_width=2).set_fill(PANEL, 1)
    code.move_to(fr)
    head = VGroup(mono(path, 20, S.GREY), label(f"· line {n} (excerpt)", 20, S.GREY))
    head.arrange(RIGHT, buff=0.14)
    head.next_to(fr, DOWN if header_below else UP, buff=0.1).align_to(fr, LEFT).shift(RIGHT * 0.12)
    g = VGroup(fr, code, head)
    g.frame, g.code, g.header = fr, code, head
    return g


def row_label(letter: str, words: str) -> VGroup:
    """'A uploads': the component letter TEAL and bold, the verb white (22 pt sans)."""
    return VGroup(sans(letter, 22, CTR, weight=BOLD), sans(words, 22, INK)).arrange(RIGHT, buff=0.1,
                                                                                  aligned_edge=DOWN)


def code_tag(code: str, words: str, color: str = S.GREY) -> VGroup:
    """A GREY tag whose first word is code (mono): "group_name unchanged"."""
    t = VGroup(mono(code, 22, color), label(words, 22, color)).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    h = mono("|", 22).height + 0.16
    b = RoundedRectangle(width=t.width + 0.4, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    return VGroup(b, t)


def hand_glyph(color: str = S.GREY) -> VGroup:
    """A small GREY pointing hand, index finger down; .tip is where it touches."""
    palm = RoundedRectangle(width=0.46, height=0.38, corner_radius=0.12, stroke_color=color,
                            stroke_width=2.5).set_fill(S.BG, 1)
    finger = RoundedRectangle(width=0.14, height=0.42, corner_radius=0.07, stroke_color=color,
                              stroke_width=2.5).set_fill(S.BG, 1)
    finger.next_to(palm, DOWN, buff=-0.1).align_to(palm, LEFT).shift(RIGHT * 0.05)
    knuckles = VGroup(*[RoundedRectangle(width=0.11, height=0.13, corner_radius=0.05, stroke_color=color,
                                         stroke_width=2).set_fill(S.BG, 1) for _ in range(3)])
    knuckles.arrange(RIGHT, buff=0.015).next_to(palm, DOWN, buff=-0.07).align_to(palm, RIGHT).shift(LEFT * 0.03)
    thumb = RoundedRectangle(width=0.13, height=0.28, corner_radius=0.06, stroke_color=color,
                             stroke_width=2.5).set_fill(S.BG, 1).rotate(0.6)
    thumb.move_to(palm.get_left() + np.array([-0.02, -0.02, 0]))
    cuff = Line(palm.get_corner(UL) + DOWN * 0.04 + RIGHT * 0.06, palm.get_corner(UR) + DOWN * 0.04 + LEFT * 0.06,
                color=color, stroke_width=2.5)
    g = VGroup(thumb, palm, knuckles, finger, cuff)
    g.finger = finger
    return g


def hand_tip(hand) -> np.ndarray:
    return hand.finger.get_bottom()


def prod_row(xs, y: float, w: float = 0.72, h: float = 0.6) -> VGroup:
    """'In production': five TEAL boxes calling each other directly (A→B, B→C, B→D, D→E).
    .boxes .arrows"""
    boxes = VGroup(*[RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=CTR,
                                      stroke_width=3).set_fill(CTR, 0.1).move_to([x, y, 0]) for x in xs])
    kw = dict(color=S.GREY, stroke_width=3, buff=0.06, max_tip_length_to_length_ratio=0.35,
              max_stroke_width_to_length_ratio=12)
    arrows = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), **kw),
                    Arrow(boxes[1].get_right(), boxes[2].get_left(), **kw),
                    CurvedArrow(boxes[1].get_top() + RIGHT * 0.15, boxes[3].get_top() + LEFT * 0.15,
                                angle=-PI / 3, color=S.GREY, stroke_width=3, tip_length=0.16),
                    Arrow(boxes[3].get_right(), boxes[4].get_left(), **kw))
    g = VGroup(boxes, arrows)
    g.boxes, g.arrows = boxes, arrows
    return g


def prefix_card() -> VGroup:
    """README.md · lines 74–80: the seven prefixes in the README's order, two columns of mono
    rows (fixed baselines). .items (README order) .frame .header"""
    pitch = line_pitch(20) * 1.12
    items = VGroup(*[mono_line(p, 20, INK) for p in README_PREFIXES])
    for k, it in enumerate(items):
        col, row = divmod(k, 4)
        it.shift(np.array([col * 3.6, -row * pitch, 0]) - it.strut.get_corner(UL))
    fr = RoundedRectangle(width=items.width + 0.6, height=items.height + 0.4, corner_radius=0.12,
                          stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 0.92).move_to(items)
    head = VGroup(mono("README.md", 20, S.GREY), label("· lines 74–80", 20, S.GREY)).arrange(RIGHT, buff=0.12)
    head.next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, items, head)
    g.frame, g.items, g.header = fr, items, head
    return g


def compact_ponder(question: str, width: float = 12.4, size: float = 26) -> VGroup:
    """The toolkit's ponder card (same frame, header, question, timer bar), with less padding so
    it fits in the band above V1. Returns VGroup(frame, header, question, bar)."""
    card = ponder_card(question, width=width, size=size)
    fr, head, q, bar = card
    body = VGroup(head, q).arrange(DOWN, buff=0.18)
    fr.become(RoundedRectangle(width=width, height=body.height + 0.62, corner_radius=0.2,
                               stroke_color=TURN, stroke_width=3).set_fill(S.BG, 0.96))
    body.move_to(fr).shift(UP * 0.12)
    bar.become(Line(fr.get_corner(DL) + RIGHT * 0.3 + UP * 0.2, fr.get_corner(DR) + LEFT * 0.3 + UP * 0.2,
                    color=TURN, stroke_width=4))
    return card


def paint(glyphs, color: str = LOOKUP) -> list:
    """Animations: each glyph of a substring takes `color` (glyph by glyph: an animation of the
    substring's own VGroup would pull the glyphs out of their line)."""
    return [g.animate.set_color(color) for g in glyphs]


def pulse(glyphs, color: str = TURN) -> list:
    """Animations: each glyph of a substring flashes `color` and grows a little, then returns."""
    return [Indicate(g, color=color, scale_factor=1.25) for g in glyphs]


def clear_stage(scene, *anims, run_time: float = 0.6):
    """Fade out everything on screen (together with `anims`), then drop it from the scene."""
    old = list(scene.mobjects)
    if old:
        scene.play(FadeOut(Group(*old)), *anims, run_time=run_time)
        scene.remove(*old)
    elif anims:
        scene.play(*anims, run_time=run_time)


# ------------------------------------------------------------------ the scene
class BucketBus(VoiceScene):
    def route(self, relay, tok, j: int, run_time: float = 2.2):
        """The token rises from its drawer into box j (the box's label dims while it is inside),
        becomes OUT_KIND[j] and drops into drawer WRITES[j], onto that drawer's own icon (where it
        is then dropped: the icon is the same picture)."""
        t1, t2, t3 = run_time * 0.38, run_time * 0.24, run_time * 0.38
        labs = [relay.letters[j], relay.names[j]]
        self.play(tok.animate.move_to(relay.center_of(j)), *[m.animate.set_opacity(0.12) for m in labs],
                  run_time=t1)
        w = WRITES[j]
        assert relay.icons[w].kind == OUT_KIND[j]
        new = relay.icons[w].copy().move_to(relay.center_of(j))       # what drawer w holds
        self.play(Transform(tok, new), Indicate(relay.boxes[j], color=CTR, scale_factor=1.06), run_time=t2)
        self.remove(tok)
        self.add(new)
        self.play(new.animate.move_to(relay.icons[w]), *[m.animate.set_opacity(1) for m in labs],
                  run_time=t3)
        self.play(Indicate(relay.drawers[w].frame, color=CLOUD, scale_factor=1.04), run_time=0.3)
        self.remove(new)

    def lagged(self, *anims, lag_ratio: float = 0.15, run_time: float = 1.0, extra=()):
        """Play a LaggedStart of animations of members (of a set piece, a panel, a line) without the
        wrapper group a LaggedStart normally adds to the scene: added, that group would pull its
        members out of their own parents and split them."""
        grp = LaggedStart(*anims, lag_ratio=lag_ratio, group=Group())
        self.play(grp, *extra, run_time=run_time)
        self.remove(grp.group)

    def show_box(self, relay, j: int, run_time: float = 0.5):
        """Box j gets its big letter and its folder name."""
        unhide(relay, relay.letters[j], relay.names[j])
        self.play(FadeIn(relay.letters[j], scale=1.3), FadeIn(relay.names[j], shift=UP * 0.1),
                  run_time=run_time)

    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0. production vs here
        mini = Relay(width=9, labels=False, bonus=False, box_h=0.7, drawer_h=0.75, gap=0.7)
        retip([*mini.read_edges, *mini.write_edges], 0.13)
        mini.shift(UP * (-0.25 - mini.boxes.get_top()[1]))
        xs = [b.get_x() for b in mini.boxes]
        prod = prod_row(xs, 1.85)
        crosses = VGroup(*[cross_mark(0.2, S.GREY, stroke=4).move_to(a.point_from_proportion(0.5))
                           for a in prod.arrows])
        cap_top = label("production: services call each other's APIs", 26, INK,
                        t2c={"production:": S.GREY}).move_to([0, 3.05, 0])
        bot_a = label("here: write outputs to shared storage;", 26, INK, t2c={"here:": S.GREY})
        bot_b = label("the next stage reads them", 26, INK)
        cap_bot = VGroup(bot_a, bot_b).arrange(RIGHT, buff=0.16, aligned_edge=DOWN).move_to([0, 0.55, 0])
        card = readme_card("README.md · lines 60–67", README_6067, size=22).move_to([0, 0.6, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(card.frame), FadeIn(card.header), *[FadeIn(r, shift=UP * 0.1) for r in card.rows],
                      run_time=0.9)
            self.wait(0.7)
            # the card condenses: its first line becomes the top row, the rest the bottom row
            self.play(ReplacementTransform(card.rows[0], cap_top), ReplacementTransform(card.rows[1], bot_a),
                      ReplacementTransform(card.rows[2], bot_b), FadeOut(card.frame), FadeOut(card.header),
                      run_time=1.0)
            self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in prod.boxes], lag_ratio=0.15), run_time=0.7)
            self.play(LaggedStart(*[Create(a) for a in prod.arrows], lag_ratio=0.25), run_time=0.8)
            vo.wait_until("This tutorial simplifies")
            self.play(prod.arrows.animate.set_opacity(0.3),
                      LaggedStart(*[Create(c) for c in crosses], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("each component writes")
            self.add(mini)                     # cabinet + drawers fade in; the boxes come down from the top row
            self.play(FadeIn(mini.cabinet), FadeIn(mini.drawers),
                      *[TransformFromCopy(prod.boxes[j], mini.boxes[j]) for j in range(5)], run_time=1.0)
            unhide(mini, mini.write_edges)
            self.play(LaggedStart(*[GrowArrow(e) for e in mini.write_edges], lag_ratio=0.15), run_time=0.9)
            vo.wait_until("where the next one reads it")
            unhide(mini, mini.read_edges)
            self.play(LaggedStart(*[GrowArrow(e) for e in mini.read_edges], lag_ratio=0.15), run_time=0.9)
            mini._flag(mini.edges, False)

        # ========================================================== 1. V1: the drawers, A and B
        relay = Relay(labels=False, bonus=False)
        retip([*relay.read_edges, *relay.write_edges], 0.18)
        relay.icons[2].scale(0.86)     # the long page clears its two-line label and the drawer's edge
        relay.shift(UP * (RELAY_BOTTOM - relay.get_bottom()[1]))
        pc = prefix_card().move_to([0, 2.28, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(prod, crosses, cap_top, cap_bot)), ReplacementTransform(mini, relay),
                      run_time=1.2)
            self.play(FadeIn(pc.frame), FadeIn(pc.header), FadeIn(pc.items, lag_ratio=0.08), run_time=0.8)
            # each prefix flies down into its drawer (pipeline order: text_translated/ and
            # text_audios/ cross); output_audios_pp/ into the dashed bonus drawer
            pairs = []
            for i, p in enumerate(PREFIXES):
                src = pc.items[README_PREFIXES.index(p)].glyphs
                dst = [g for t in relay.drawer_labels[i] for g in t]
                assert len(src) == len(dst), p
                pairs += list(zip(src, dst))
            bsrc = pc.items[README_PREFIXES.index(BONUS_PREFIX)].glyphs
            bdst = [g for t in relay.bonus.text for g in t]
            assert len(bsrc) == len(bdst)
            pairs += list(zip(bsrc, bdst))
            # letter by letter: each card letter flies to its place in its drawer's label (no glyph
            # morphing between the two fonts), then the labels take over
            flyers = VGroup(*[a.copy() for a, _ in pairs])
            unhide(relay, relay.bonus.frame)
            self.play(*[f.animate.move_to(b.get_center()) for f, (_, b) in zip(flyers, pairs)],
                      FadeIn(relay.bonus.frame), run_time=1.3)
            unhide(relay, relay.drawer_labels, relay.bonus)
            self.play(FadeOut(flyers), FadeIn(relay.drawer_labels), FadeIn(relay.bonus.text), run_time=0.4)
            vo.wait_until("drawn as a cabinet")
            unhide(relay, relay.icons, relay.parts["bonus_tag"])
            self.play(LaggedStart(*[FadeIn(ic, shift=UP * 0.1) for ic in relay.icons], lag_ratio=0.12),
                      FadeIn(relay.parts["bonus_tag"]), run_time=0.9)
            # the card leaves and V1 rises to the middle of the frame
            rise = -relay.get_center()[1]
            self.play(FadeOut(pc.frame), FadeOut(pc.header), FadeOut(pc.items), relay.animate.shift(UP * rise),
                      run_time=0.8)
            self.remove(pc)
            ill = illustration_tag().next_to(relay.cabinet, DOWN, buff=0.17).align_to(relay.drawers[0].frame, LEFT)
            relay.attach(self, ill, run_time=0.4)
            vo.wait_until("The first stage")
            self.show_box(relay, 0)
            vo.wait_until("turns recordings")
            tok = relay.icons[0].copy()
            self.add(tok)
            self.route(relay, tok, 0, run_time=2.2)
            vo.wait_until("Then B turns")
            self.show_box(relay, 1)
            tok = relay.icons[1].copy()
            self.add(tok)
            self.route(relay, tok, 1, run_time=2.2)

        # ========================================================== 2. the split: C, D, E; the arrows
        every = label("every arrow goes through a drawer", 26, S.GREY).move_to([0, CAP_Y, 0])
        by_hand = label("you run each one, by hand", 26, S.GREY).move_to([0, CAP_Y, 0])

        with self.voiceover(SAY[2]) as vo:
            tc, td = relay.icons[2].copy(), relay.icons[2].copy()
            self.add(tc, td)
            self.play(tc.animate.shift(LEFT * 0.55), td.animate.shift(RIGHT * 0.55),
                      Indicate(relay.drawers[2].frame, color=CLOUD, scale_factor=1.04), run_time=0.9)
            vo.wait_until("C turns")
            self.show_box(relay, 2)
            self.route(relay, tc, 2, run_time=2.0)
            vo.wait_until("D translates")
            self.show_box(relay, 3)
            self.route(relay, td, 3, run_time=1.8)
            relay._flag(relay.letters, False)
            vo.wait_until("and E speaks")
            self.show_box(relay, 4, run_time=0.4)
            relay._flag(relay.letters, False)
            relay._flag(relay.names, False)
            te = relay.icons[4].copy()
            self.add(te)
            self.route(relay, te, 4, run_time=1.6)
            relay.reveal(self, "edges", run_time=0.7, extra=[FadeIn(every, shift=DOWN * 0.1)])

        # ========================================================== 3. nothing triggers anything
        hand = hand_glyph()

        def at_box(j, lift=0.18):
            b = relay.boxes[j]
            return hand.copy().shift(b.get_top() + UP * lift - hand_tip(hand))

        with self.voiceover(SAY[3]) as vo:
            self.play(Transform(every, by_hand), run_time=0.7)
            hand.become(at_box(0))
            self.play(FadeIn(hand, shift=DOWN * 0.2), run_time=0.4)
            for j in range(3):
                if j:
                    self.play(hand.animate.become(at_box(j)), run_time=0.45)
                self.play(hand.animate(rate_func=there_and_back).shift(DOWN * 0.15),
                          Indicate(relay.boxes[j], color=CTR, scale_factor=1.08), run_time=0.55)

        # ========================================================== 4. no folders: one object name
        big_fr = RoundedRectangle(width=10.2, height=2.7, corner_radius=0.18, stroke_color=CLOUD,
                                  stroke_width=3).set_fill(CLOUD, 0.1).move_to([0, 0.45, 0])
        big_handle = RoundedRectangle(width=1.1, height=0.13, corner_radius=0.06, stroke_width=0) \
            .set_fill(CLOUD, 0.9).move_to(big_fr.get_top() + DOWN * 0.26)
        big_label = sans("text_prompts/", 26, INK).move_to(big_fr.get_corner(UL) + np.array([0.3, -0.32, 0]),
                                                           aligned_edge=UL)
        name = mono_line(OBJECT, 30, LOOKUP).move_to(big_fr.get_center() + DOWN * 0.2)
        n_pre = glyph_range(name, 0, 12)                      # text_prompts
        n_s1 = substring(name, "/", 0)
        n_grp = substring(name, "group-01")
        n_s2 = substring(name, "/", 1)
        n_file = substring(name, "input-….txt")
        line_under = Line(name.strut.get_corner(DL) + DOWN * 0.04, name.strut.get_corner(DR) + DOWN * 0.04,
                          color=LOOKUP, stroke_width=4)
        one_name = label("one object name · no real folders", 26, S.GREY).next_to(big_fr, DOWN, buff=0.35)
        ill4 = illustration_tag().next_to(big_fr, DOWN, buff=0.38).align_to(big_fr, RIGHT)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(relay), FadeOut(every), FadeOut(hand),
                      TransformFromCopy(relay.drawers[1], VGroup(big_fr, big_handle)),
                      TransformFromCopy(relay.drawer_labels[1], big_label), run_time=1.3)
            self.play(FadeIn(ill4), run_time=0.4)
            vo.wait_until("a name like")
            self.play(Write(n_pre), run_time=0.8)
            vo.wait_until("slash, group-01")
            self.play(FadeIn(n_s1, scale=1.6), run_time=0.3)
            self.play(Write(n_grp), Indicate(n_s1[0], color=TURN, scale_factor=1.6), run_time=0.8)
            vo.wait_until("slash, input")
            self.play(FadeIn(n_s2, scale=1.6), run_time=0.3)
            self.play(Write(n_file), Indicate(n_s2[0], color=TURN, scale_factor=1.6), run_time=1.0)
            self.remove(n_pre, n_s1, n_grp, n_s2, n_file)
            self.add(name)                                       # the same glyphs, now one group
            vo.wait_until("is one single object name")
            self.play(Indicate(n_s1[0], color=TURN, scale_factor=1.6), Indicate(n_s2[0], color=TURN, scale_factor=1.6),
                      run_time=0.7)
            self.play(Create(line_under), FadeIn(one_name, shift=UP * 0.1), run_time=0.7)

        # ========================================================== 5. the naming contract
        top_y = 3.05
        p112 = src_panel(UPLOAD_PATH, UPLOAD_LINE, UPLOAD_LINE, size=20)
        p112.move_to([0, 0, 0]).align_to([-6.28, 0, 0], LEFT)
        p112.shift(UP * (2.15 - p112.get_top()[1]))
        lab_a = row_label("A", "uploads").move_to(p112.header).align_to(p112.code, RIGHT).shift(LEFT * 0.12)
        c108 = excerpt_chip(UPLOAD_PATH, GLOB_LINE, GLOB)
        c108.align_to(p112.code, LEFT).shift(UP * (p112.get_bottom()[1] - 0.45 - c108.get_top()[1]))
        c42 = excerpt_chip(DOWNLOAD_PATH, DOWNLOAD_LINE, MATCH, header_below=True)
        # B's chip sits under A's so that {group_name} is right under group_name
        dx = substring(c108.code, "group_name").get_x() - substring(c42.code, "{group_name}").get_x()
        c42.shift(np.array([dx, c108.frame.get_bottom()[1] - 1.15 - c42.frame.get_top()[1], 0]))
        lab_b = row_label("B", "downloads").move_to(c42.header).align_to(c42.frame, RIGHT).shift(LEFT * 0.12)
        code = p112.code
        hl_pre = code_span(code, 0, "text_prompts")
        hl_grp = code_span(code, 0, "group_name")
        hl_file = code_span(code, 0, "filename")
        g_pre, g_grp = substring(c108.code, "text_prompts"), substring(c108.code, "group_name")
        g_inp = substring(c108.code, '"input-*.txt"')
        m_pre, m_grp = substring(c42.code, "{text_prompts}"), substring(c42.code, "{group_name}")
        m_inp = substring(c42.code, "input-*.txt")
        u_pre, u_grp, u_file = [Line(m.get_corner(DL) + DOWN * 0.06, m.get_corner(DR) + DOWN * 0.06,
                                     color=LOOKUP, stroke_width=4) for m in (hl_pre, hl_grp, hl_file)]
        u_inp = Line(g_inp.get_corner(DL) + DOWN * 0.07, g_inp.get_corner(DR) + DOWN * 0.07, color=LOOKUP,
                     stroke_width=4)
        links = VGroup(*[Line(a.get_bottom() + DOWN * 0.1, b.get_top() + UP * 0.1, color=LOOKUP, stroke_width=3)
                         for a, b in ((g_pre, m_pre), (g_grp, m_grp), (g_inp, m_inp))])
        dots = VGroup(*[Dot(p, radius=0.05, color=LOOKUP) for ln in links for p in (ln.get_start(), ln.get_end())])
        row_a = VGroup(p112, lab_a, c108, u_pre, u_grp, u_file, u_inp)
        row_b = VGroup(c42, lab_b)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(big_fr, big_handle, big_label, ill4, one_name, line_under)),
                      name.animate.move_to([0, top_y, 0]), run_time=0.8)
            self.play(FadeIn(p112, shift=UP * 0.15), FadeIn(lab_a, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(c108, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("prefix")
            self.play(Create(u_pre), *paint(hl_pre), *pulse(n_pre), run_time=0.6)
            vo.wait_until("group name")
            self.play(Create(u_grp), *paint(hl_grp), *pulse(n_grp), run_time=0.6)
            vo.wait_until("file name")
            self.play(Create(u_file), *paint(hl_file), *pulse(n_file), run_time=0.6)
            vo.wait_until("and only files")
            self.play(Create(u_inp), *paint(g_inp), run_time=0.6)
            vo.wait_until("B downloads")
            self.play(FadeIn(c42, shift=UP * 0.15), FadeIn(lab_b, shift=UP * 0.15), run_time=0.6)
            self.lagged(*[AnimationGroup(Create(ln), *paint(a), *paint(b), group=Group())
                          for ln, a, b in zip(links, (g_pre, g_grp, g_inp), (m_pre, m_grp, m_inp))],
                        lag_ratio=0.35, extra=[FadeIn(dots)], run_time=1.2)
            vo.wait_until("that naming contract")
            self.play(FadeOut(VGroup(row_a, row_b, links, dots), target_position=name.get_center(), scale=0.15),
                      run_time=1.0)
            self.play(Indicate(name, color=LOOKUP, scale_factor=1.06), run_time=0.6)

        # ========================================================== 6. the group name is the namespace
        sd = SubDrawers().move_to([-0.3, 0.35, 0])
        ill6 = illustration_tag().next_to(sd.drawers, DOWN, buff=0.25).align_to(sd.drawers, RIGHT)
        D = sd.default
        mine = page_token().scale(0.85).move_to(sd.slot(0))
        theirs = VGroup(*[page_token(color=S.GREY).scale(0.85).move_to(sd.slot(i)) for i in (1, 2)])
        lost = page_token(color=S.GREY).scale(0.85).move_to(sd.slot(D))
        ghost = RoundedRectangle(width=1.5, height=0.8, corner_radius=0.12, stroke_color=CTR,
                                 stroke_width=3).set_fill(CTR, 0.1)
        ghost.move_to([sd.drawers[D].get_x(), 2.45, 0])
        unchanged = code_tag("group_name", "unchanged").next_to(ghost, LEFT, buff=0.3)
        drop = page_token().scale(0.85).move_to(ghost)
        warn = readme_card("README.md · line 124", [README_124], size=22).move_to([0, -2.25, 0])
        title_glyphs = VGroup(*n_pre, *n_s1)

        with self.voiceover(SAY[6]) as vo:
            self.add(sd)
            self.play(TransformFromCopy(title_glyphs, sd.title), TransformFromCopy(VGroup(*n_grp, *n_s2),
                                                                                  sd.drawers[0].text),
                      TransformFromCopy(n_file, mine), FadeOut(name),
                      *[FadeIn(d.frame) for d in sd.drawers], *[FadeIn(d.text) for d in sd.drawers[1:]],
                      run_time=1.2)
            self.play(FadeIn(theirs, shift=DOWN * 0.1), FadeIn(lost, shift=DOWN * 0.1), FadeIn(ill6), run_time=0.6)
            vo.wait_until("and its default")
            self.play(Indicate(sd.drawers[D].frame, color=S.WHITE, scale_factor=1.06), run_time=0.7)
            vo.wait_until("a component you forgot")
            self.play(FadeIn(ghost, shift=DOWN * 0.2), FadeIn(unchanged, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("writes into the default")
            self.add(drop)
            self.play(drop.animate.move_to(sd.slot(D) + RIGHT * 0.12 + UP * 0.03), run_time=0.8)
            fr = sd.drawers[D].frame                      # SubDrawers.flash, played member by member
            self.play(fr.animate.set_stroke(ERR, 3.5).set_fill(ERR, 0.2), run_time=0.35)
            self.play(Indicate(fr, color=ERR, scale_factor=1.08), run_time=0.6)
            vo.wait_until("maybe over someone")
            self.play(Indicate(lost, color=ERR, scale_factor=1.15), run_time=0.7)
            self.play(lost.animate.set_opacity(0.15), run_time=0.5)
            vo.wait_until("Set it before")
            self.play(FadeIn(warn, shift=UP * 0.2), run_time=0.7)
            self.play(Indicate(warn.rows[0], color=TURN, scale_factor=1.04), run_time=0.8)

        # ========================================================== 7. the leaderboard; who pays
        lb = Leaderboard().move_to([0, 0.35, 0])
        lb_cap = VGroup(mono("ac215-mega-pipeline.dlops.io", 22, S.GREY),
                        label("· README.md line 54", 22, S.GREY)).arrange(RIGHT, buff=0.14)
        lb_cap.next_to(lb, UP, buff=0.45)
        ill7 = illustration_tag().next_to(lb, DOWN, buff=0.35).align_to(lb, RIGHT)
        relay.shift(UP * (RELAY_BOTTOM - relay.get_bottom()[1]))      # off screen: back to the foot
        bill = cost_tag().next_to(relay.cabinet, DOWN, buff=0.17)
        bill.move_to([-1.2, bill.get_y(), 0])

        with self.voiceover(SAY[7]) as vo:
            old = Group(sd, ill6, mine, theirs, lost, ghost, unchanged, drop, warn)
            self.play(FadeOut(old), FadeIn(lb), FadeIn(lb_cap), FadeIn(ill7), run_time=0.8)
            self.remove(old)
            self.play(lb.light(1, 0), lb.light(1, 1), lb.light(2, 0), run_time=0.5)
            vo.wait_until("lights up your row")
            self.play(Indicate(lb.row_names[0], color=TURN, scale_factor=1.15), lb.light(0, 0), run_time=0.6)
            self.play(lb.light(0, 1), run_time=0.4)
            vo.wait_until("Every call")
            self.play(FadeOut(lb), FadeOut(lb_cap), FadeOut(ill7), FadeIn(relay), run_time=0.9)
            self.play(FadeIn(bill, shift=RIGHT * 1.2), run_time=0.7)
            vo.wait_until("not yours")
            self.play(Indicate(bill, color=COST, scale_factor=1.1), run_time=0.7)

        # ========================================================== 8. ponder
        card = compact_ponder(PONDER_Q)
        card.move_to([0, 3.52 - card.height / 2, 0])
        assert card.get_bottom()[1] > relay.get_top()[1] + 0.25

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(bill), run_time=0.4)
            self.remove(bill)
            self.lagged(*[Indicate(e, color=TURN, scale_factor=1.1) for e in relay.read_edges], run_time=1.3)
            self.lagged(*[Indicate(e, color=TURN, scale_factor=1.1) for e in relay.write_edges], run_time=1.3)
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ========================================================== 9. the answer
        boxes = relay.boxes
        brace = Brace(VGroup(boxes[2], boxes[3]), UP, buff=0.12, color=TURN)
        side = label("side by side", 24, TURN).next_to(brace, UP, buff=0.08)
        clock = clock_glyph(0.16, TURN)             # "waits": YELLOW, not the GOLD of money
        waits = label("waits for D", 24, TURN)
        clock_g = VGroup(clock, waits).arrange(RIGHT, buff=0.15)
        clock_g.next_to(boxes[4], UP, buff=0.2)
        cd = [relay.read_edges[2], relay.read_edges[3]]
        de = [relay.write_edges[3], relay.read_edges[4]]

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            self.remove(card)
            self.play(*[e.animate.set_color(TURN) for e in cd],
                      Indicate(relay.drawers[2].frame, color=TURN, scale_factor=1.05), run_time=0.7)
            self.play(*[Indicate(e, color=TURN, scale_factor=1.15) for e in cd], run_time=0.7)
            vo.wait_until("so they could run")
            self.play(GrowFromCenter(brace), FadeIn(side, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("E reads what D writes")
            self.play(*[e.animate.set_color(TURN) for e in de],
                      Indicate(relay.drawers[4].frame, color=TURN, scale_factor=1.05), run_time=0.7)
            self.play(*[Indicate(e, color=TURN, scale_factor=1.15) for e in de], run_time=0.6)
            vo.wait_until("so it waits")
            self.play(FadeIn(clock_g, shift=DOWN * 0.1), run_time=0.5)
            self.play(Rotate(clock[1], angle=-TAU, about_point=clock[0].get_center()), run_time=0.8)

        clear_stage(self, run_time=0.8)
