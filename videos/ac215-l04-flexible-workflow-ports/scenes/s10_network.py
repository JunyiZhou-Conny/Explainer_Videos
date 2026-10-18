"""S10 · Two little computers, one network (port_toy README: Prerequisites, Step 1 steps 1-2,
Handy commands step 4; V6 first).

Beats (script.md "## S10", one voiceover block each):
 0  No tracker. Left: part 1's relay in miniature (MiniRelay: five TEAL boxes over the BLUE
    cabinet), PINK arrows box -> drawer -> box draw themselves while a token hops along them; GREY
    README card mega-pipeline · README.md · line 142 ("… components will communicate indirectly
    by / writing their outputs to storage, …") above it. On "Port toy makes …" the left half dims;
    right: TEAL boxes `gateway` and `processor` joined by a direct PINK arrow; README chip
    README.md · line 24 "only need Docker"; a GREY browser glyph and a PINK arrow to the gateway;
    the GREY card port_toy · README.md · line 52 (Browser → localhost:8090 → Gateway →
    processor:9200 → Processor) across the bottom, its two halves underlined YELLOW as they are
    said; a PINK packet "hello" rides browser -> gateway -> processor and turns into "HELLO".
 1  V6 (ToyNet). Everything else leaves; the two boxes grow into the glass boxes and the browser
    moves into the laptop's corner; the GREY laptop outline "your laptop" appears. On "with its
    own localhost": each box's TEAL localhost loop appears and a dot circles it (it glows YELLOW),
    and the laptop's third GREY loop does the same. On "full set of ports": a port strip
    1 … 65535 in each box. Both strips light 9100 at once (YELLOW cell + number), GREY caption
    "each box: its own ports · both could use 9100" (the real processor listens on 9200: the
    picture says "could", it does not give the processor 9100). The GREY tag "Lecture 4 · slide 33"
    (lecture_ref, top right) arrives with the laptop outline. On "The lecture calls this" each
    glass box's frame flashes TEAL on its own; on "each container is isolated" both localhost
    loops are indicated (SLIDES.md S10 i, ii).
 2  The 9100 lights go out. A TEAL rail draws itself under the boxes, labelled "user-defined
    network"; a PINK phone-book glyph sits on it and its two blank lines (_____ → _______)
    rise out of the book glyph to their place between the boxes; GREY note "Docker's default
    network: no phone book (exercises)". The tag becomes "Lecture 4 · slide 34" in the first play;
    the PINK label "Docker DNS" (slide 34's term) arrives with the book glyph, under it, in the row
    of "user-defined network" (SLIDES.md S10 iii). Tag and label leave with V6 in beat 3; the
    label is taken out of the piece before beat 6 (the ID chip lands on its spot).
 3  TRACKER P0/1 (port_toy README › Prerequisites). V6 leaves; the 12-row terminal `laptop` at
    student@laptop:~/AC215$ with the GREY caption "your workspace" at the row's right end (the
    path flashes YELLOW). `docker run hello-world` -> port-laptop/01 lines 2-3, …, 7 (on "It pulls
    a tiny image"), then 9-10, … (line 10 cut with …); "Hello from Docker!" turns GREEN.
 4  TRACKER P1/1. The terminal clears; README chip README.md · line 81 "Clone or download" in the
    top band, the workspace path flashes. `git clone https://github.com/dlops-io/port_toy.git`
    (on the row under the prompt) -> 02 line 2; GREY caption "the README links the repo but
    prints no clone command" on the prompt row; the chip flashes. `cd port_toy` -> no output, the
    prompt becomes student@laptop:~/AC215/port_toy$ (the new part flashes YELLOW). ▶ your turn.
 5  TRACKER P1/1 · extra. The terminal shrinks to the 3-row strip (the ▶ rides along on its row
    and fades when the strip is cleared for the listing); above it the README's tree (README.md ·
    lines 59–69, comments GREY). `ls gateway processor` (extra) is typed and lifts into a GREY
    command chip with an `extra` tag in the card's header row (right-aligned with the card), where
    it stays until the card leaves in beat 6. -> 04 lines 11-18 in three batches, the strip
    cleared in place before each (11-13 · 14-15 · 16-18), each held ~0.9 s; a GREEN check lands
    in the tree beside each folder and file as it prints. `git log --oneline -1` (extra) -> 04
    line 19; `d190c71` is boxed GREY and lifts into a GREY chip in the top band, right of the
    tracker, with the GREY tag "the pinned commit".
 6  TRACKER P1/2. The tree and the hash's box leave; V6 returns above the strip (the ToyNet
    moves up 0.55 while hidden). `docker network create toynet`; the word toynet flies from the
    command onto the rail and replaces "user-defined network" (the commit chip leaves now) ->
    05 line 2 on "Docker prints the new network's ID"; the first 12 characters of the ID fly
    onto the rail as a TEAL chip `cedc0ad9fdee…`, GREY tag "your numbers will differ" under the picture; a YELLOW flash runs
    along the rail and both boxes pulse ("the rail both containers will plug into").
 7  TRACKER PH/4 (Handy commands). V6 leaves; the terminal grows to 8 rows (the last command and
    its ID stay). `docker network ls` -> 06 lines 2-6: `toynet` turns TEAL in a TEAL box; a GREY
    bracket "built in" on bridge, host, none. ▶ your turn beside `docker network ls`. Fade out to
    an empty frame.

Deviations from SHOW (and why):
- Beat 0: the part 1 card quotes README.md line 142 only (the sentence the narration paraphrases),
  so its header says "line 142", not "lines 140–142". It is a two-row card above the relay, not a
  one-line chip: a one-line chip with the quoted phrase is wider than the half frame. The
  README.md:24 chip quotes the exact sub-string "only need Docker" (the README says "You only need
  Docker Desktop."), headed "README.md · line 24" (with "port_toy ·" it is wider than the right
  half); the line-52 card says port_toy. The "hello" packet and its capitals are this scene's own
  illustration of "forwards your text … turns it into capitals" (no terminal, nothing captured).
- Beat 1: the boxes' strips and loops are registered here as extra hidden parts of ToyNet so they
  appear after the boxes have grown; ToyNet's dashed wall (V7's street doors, S11) is taken out
  of this scene's copy: nothing on screen explains it yet. The caption adds "· both could use
  9100" to SHOW's "each box: its own ports": port_toy's processor listens on 9200 (README.md:55),
  and a bare 9100 lit in the box named processor read as its real port (QA 18:36).
- Beat 2: the phone book's "two blank lines" are drawn as `_____ → _______` (blank name, blank
  address), at the place where S13's entries will be written.
- Beat 4: the README chip quotes "Clone or download" (README.md:81 starts "Clone or download the
  repository"): with the full phrase the chip is wider than the room right of the tracker.
- Beat 5: the 3-row strip, not a taller terminal: the README's tree (9 rows) needs the 4.1 units
  above the strip. "the pinned commit" does not fit beside `d190c71 …` in its row (the line is 55
  characters), so the hash is boxed in the row and lifted into a chip in the top band (right of
  the tracker), where the tag sits; the checked tree stays up until beat 6. The ls output (8
  lines) does not fit the strip: it prints in three batches, and the strip is cleared in place
  before each (a house scroll of 2–3 rows dragged them over the strip's title bar and the
  card's border, and scrolled the command out after half a second), so the command is pinned as
  a chip by the card instead (QA 19:12). Batches keep the processor listing whole: gateway:,
  Dockerfile, gateway.py · index.html, (blank) · processor:, Dockerfile, processor.py. Both chips
  in the top right are slim (pad 0.08) and right-aligned with the card, one above the other.
- Beat 6: the ID chip carries the first 12 characters + "…" (the short ID `docker network ls`
  prints); the full 64-character line is in the strip. The tag sits under the laptop outline (no
  room on the rail). No ghost plugs: the gateway's plug would cross the chip; the rail flash and
  the two boxes' pulse carry "both containers will plug into" (S11 plugs them in).
- Beat 7: the ▶ sits beside `docker network ls` (beside `docker network create toynet` it would
  cover the command: that row is 61 characters); both commands stay on screen.
"""

from common import (
    CTR,
    INK,
    LAPTOP,
    LOOKUP,
    NARRATION,
    P_TOY,
    P_WS,
    TURN,
    MiniRelay,
    ToyNet,
    _header_text,
    bare_prompt,
    beside,
    caption_extra,
    capture,
    cd_prompt,
    differ_tag,
    excerpt,
    extra_tag,
    grey_tag,
    note,
    pin,
    readme_card,
    readme_chip,
    resize,
    switch_section,
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
    UL,
    UP,
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromPoint,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    ReplacementTransform,
    ShowPassingFlash,
    Succession,
    Transform,
    TransformFromCopy,
    VGroup,
    VMobject,
    smooth,
)

from explainer import style as S
from explainer.devops import (
    CAPTION,
    MONO,
    box,
    check_mark,
    chip,
    glyph_range,
    lecture_ref,
    line_pitch,
    mono,
    mono_line,
    substring,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S10"]
assert len(SAY) == 8, len(SAY)

# ------------------------------------------------------------------ captures (file line numbers)
HELLO = capture("01", "port-laptop")
assert HELLO.cmd == "docker run hello-world"
PULL = HELLO.at(2, 3, "…", 7)                       # TERM 2–3, …, 7
GREET = HELLO.at(9, 10, "…")                        # TERM 9–10, … (line 10 is cut with …)
assert GREET[0] == "Hello from Docker!"
CLONE = capture("02", "port-laptop")
assert CLONE.cmd == "git clone https://github.com/dlops-io/port_toy.git"
CD = capture("03", "port-laptop")
assert CD.cmd == "cd port_toy" and not CD.lines
LS = capture("04", "port-laptop")
LS_CMD, LOG_CMD = "ls gateway processor", "git log --oneline -1"
assert LS.cmd.split("; ")[1:] == [LS_CMD, LOG_CMD], LS.cmd   # `ls -a` is not shown, not typed
LS_GW, LS_PR = LS.at((11, 14)), LS.at((15, 18))
LOG = LS.line(19)
assert LS_GW[0] == "gateway:" and LS_PR[1] == "processor:" and LOG.startswith("d190c71 ")
NET = capture("05", "port-laptop")
assert NET.cmd == "docker network create toynet"
NET_ID = NET.line(2)
ID_SHORT = NET_ID[:12]
NLS = capture("06", "port-laptop")
assert NLS.cmd == "docker network ls"
NLS_OUT = NLS.at((2, 6))
assert NLS_OUT[4].startswith(ID_SHORT) and " toynet " in NLS_OUT[4]
assert [r.split()[1] for r in NLS_OUT[1:4]] == ["bridge", "host", "none"]

# ------------------------------------------------------------------ README sources
TOY = "port_toy/README.md"
R24 = excerpt(TOY, 24, 24)
PH24 = "only need Docker"
assert PH24 in R24
R52 = excerpt(TOY, 52, 52)
assert R52 == "Browser → localhost:8090 → Gateway → processor:9200 → Processor"
SEG1 = "Browser → localhost:8090 → Gateway"
SEG2 = "processor:9200 → Processor"
PH81 = "Clone or download"
assert excerpt(TOY, 81, 81).startswith(PH81 + " the [repository]")
TREE = excerpt(TOY, 60, 68).split("\n")
assert TREE[0] == "port_toy/" and TREE[-1].startswith("    └── processor.py")
L142 = excerpt("mega-pipeline/README.md", 142, 142).replace("**", "")
Q142 = ["… components will communicate indirectly by", "writing their outputs to storage, …"]
assert "components will communicate indirectly by writing their outputs to storage," in L142

# ------------------------------------------------------------------ layout
NET_DY = 0.2             # ToyNet built around y=0 (outline -1.5..1.4): beats 1-2, -1.3..1.6
NET_UP = 0.55            # beat 6, above the 3-row strip: outline -0.75..2.15
P20 = line_pitch(CAPTION)
Y_ROW = 0.1              # beat 0: the right-hand row (arrows, packet)
TREE_BOTTOM = -1.30      # the tree card's frame sits on this (the strip's top is -1.44)
HASH_Y = 3.30            # beat 5: the commit chip's row (the ls chip's row is under it)
SLIM = 0.08              # beat 5: the two chips' vertical padding (two rows fit above the card)


def relay_routes(relay) -> VGroup:
    """PINK arrows drawer 0 -> box 0 -> drawer 1 -> box 1 … -> drawer 5 (every hop via the bucket)."""
    out = VGroup()
    kw = {"buff": 0.04, "color": LOOKUP, "stroke_width": 3, "max_tip_length_to_length_ratio": 0.22,
          "max_stroke_width_to_length_ratio": 8}
    for j in range(5):
        d0, b, d1 = relay.drawers[j], relay.boxes[j], relay.drawers[j + 1]
        out.add(Arrow(d0.get_top() + RIGHT * 0.1, b.get_bottom() + LEFT * 0.16, **kw))
        out.add(Arrow(b.get_bottom() + RIGHT * 0.16, d1.get_top() + LEFT * 0.1, **kw))
    return out


def relay_hop(relay, run_time: float):
    """A white token along the routes: drawer 0 -> box 0 -> drawer 1 … (scene-owned token)."""
    tok = Dot(radius=0.07, color=INK).move_to(relay.drawers[0])
    stops = []
    for j in range(5):
        stops += [relay.boxes[j].get_center(), relay.drawers[j + 1].get_center()]
    per = run_time / len(stops)
    prev, steps = relay.drawers[0].get_center(), []
    for q in stops:
        steps.append(MoveAlongPath(tok, Line(prev, q), rate_func=smooth, run_time=per))
        prev = q
    return tok, Succession(*steps)


def mini_box(name: str, x0: float, x1: float, top: float, bot: float) -> VGroup:
    """A TEAL box in ToyNet's style (frame + name top-left inside). .frame .name"""
    fr = box(x1 - x0, top - bot, CTR, fill_opacity=0.07).move_to([(x0 + x1) / 2, (top + bot) / 2, 0])
    nm = mono(name, CAPTION, CTR).move_to([x0 + 0.18, top - 0.24, 0], aligned_edge=LEFT)
    g = VGroup(fr, nm)
    g.frame, g.name = fr, nm
    return g


def solid_chip(text: str, color: str, size: float = CAPTION) -> VGroup:
    """A mono chip with an opaque dark fill (it sits on a line). .box .text"""
    t = mono(text, size, INK)
    b = box(t.width + 0.44, t.height + 0.24, color, fill=S.BG, fill_opacity=1.0, radius=0.12)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def card52() -> VGroup:
    """README.md:52 as a GREY card in readme_card's look; .row is a mono_line (to underline its two
    halves). The frame is drawn at its final width (stretching a rounded box distorts its corners)."""
    row = mono_line(R52, CAPTION, INK)
    fr = box(row.width + 0.6, row.strut.height + 0.32, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    row.move_to(fr)
    head = _header_text("port_toy · README.md · line 52").next_to(fr, UP, buff=0.08)
    head.align_to(fr, LEFT).shift(RIGHT * 0.1)
    c = VGroup(fr, row, head)
    c.frame, c.row, c.header = fr, row, head
    return c


def tree_card():
    """README.md lines 60–68 (the fenced tree of lines 59–69) as a GREY card: names in INK, tree
    glyphs and comments GREY. .rows (mono_lines) .frame .header; .check_at(i) -> a GREEN check
    just after the name of row i (not added)."""
    rows = VGroup()
    for i, s in enumerate(TREE):
        a = len(s) - len(s.lstrip("│├└─ "))
        k = s.find("#")
        t2c = {f"[0:{a}]": S.GREY} if a else {}
        if k >= 0:
            t2c[f"[{k}:]"] = S.GREY
        ln = mono_line(s, CAPTION, INK, t2c=t2c or None)
        ln.shift([0, -i * P20, 0] - ln.strut.get_corner(UL))
        rows.add(ln)
    fr = box(max(r.strut.width for r in rows) + 0.7, len(TREE) * P20 + 0.4, S.GREY, fill=S.BG,
             fill_opacity=0.95, radius=0.14)
    fr.move_to(rows).align_to(rows, LEFT).shift(LEFT * 0.3)
    fr.shift(UP * (rows.get_top()[1] + 0.2 - fr.get_top()[1]))
    head = _header_text("README.md · lines 59–69").next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header = fr, rows, head

    def check_at(i: int):
        s = TREE[i]
        name = s.lstrip("│├└─ ").split()[0]
        end = s.index(name) + len(name)
        row = g.rows[i]
        c = check_mark(0.26, S.GREEN)
        c.next_to(glyph_range(row, end - 1, end), RIGHT, buff=0.14).set_y(row.strut.get_center()[1])
        return c

    g.check_at = check_at
    return g


def wipe(scene, t, run_time: float = 0.25) -> None:
    """Clear the strip in place: every row fades where it is (nothing slides over the title bar)
    and is forgotten, so the next print starts on the first row (S16's wipe)."""
    gone = list(t.lines.submobjects)
    if gone:
        scene.play(FadeOut(VGroup(*gone)), run_time=run_time)
    for m in gone:
        t.lines.remove(m)
        scene.remove(m)


def glyph_box(row, sub: str, color: str) -> VMobject:
    """A box around the glyphs of `sub` in a terminal row, the row's full height (not added)."""
    g = substring(row, sub)
    b = box(g.width + 0.2, row.strut.height + 0.04, color, fill_opacity=0.0, radius=0.06, stroke=3)
    return b.move_to([g.get_center()[0], row.strut.get_center()[1], 0])


def blank_line(width_l: float = 1.0, width_r: float = 1.4) -> VGroup:
    """One blank phone-book line: ____ → ______ (PINK)."""
    a = Line(LEFT * width_l / 2, RIGHT * width_l / 2, color=LOOKUP, stroke_width=3)
    arr = mono("→", CAPTION, LOOKUP)
    b = Line(LEFT * width_r / 2, RIGHT * width_r / 2, color=LOOKUP, stroke_width=3)
    g = VGroup(a, arr, b).arrange(RIGHT, buff=0.18)
    arr.shift(UP * 0.1)
    return g


class TwoComputers(VoiceScene):
    def construct(self):
        # ------------------------------------------------------------ the set piece (V6), prepared
        net = ToyNet(show=("zone", "boxes"))
        net.parts["zone"].remove(net.wall)                 # V7's wall: S11 explains the doors
        for name, b in net.boxes.items():                  # strips and loops appear after the boxes
            net.part(f"{name}_strip", b.strip, shown=False, into=b)
            net.part(f"{name}_loop", b.loop, shown=False, into=b)
            net.part(f"{name}_ll", b.loop_label, shown=False, into=b)
        lp_loop, lp_ll = net.laptop_loop
        net.part("lp_loop", lp_loop, shown=False, into=net.parts["zone"])
        net.part("lp_ll", lp_ll, shown=False, into=net.parts["zone"])
        net.shift(UP * NET_DY)
        under_net = net.parts["outline"].get_bottom()[1]

        # ------------------------------------------------------------ 0. part 1: via the bucket; port_toy: direct
        relay = MiniRelay().move_to([-3.4, 0.1, 0])
        routes = relay_routes(relay)
        c142 = readme_card("mega-pipeline · README.md · line 142", Q142)
        c142.move_to([0, 0, 0]).shift([-6.45 - c142.get_left()[0], 3.45 - c142.get_top()[1], 0])
        gw0 = mini_box("gateway", 1.75, 3.65, 0.95, -0.35)
        pr0 = mini_box("processor", 4.5, 6.4, 0.95, -0.35)
        brw0 = VGroup(net.browser.copy(), net.browser_label.copy())
        brw0[0].move_to([0.72, Y_ROW, 0])
        brw0[1].next_to(brw0[0], DOWN, buff=0.12)
        a_bg = Arrow([1.06, Y_ROW, 0], [1.72, Y_ROW, 0], buff=0, color=LOOKUP, stroke_width=5,
                     max_tip_length_to_length_ratio=0.35)
        a_gp = Arrow([3.68, Y_ROW, 0], [4.47, Y_ROW, 0], buff=0, color=LOOKUP, stroke_width=5,
                     max_tip_length_to_length_ratio=0.3)
        ch24 = readme_chip("README.md · line 24", PH24)
        ch24.move_to([0, 3.15, 0]).align_to([6.45, 0, 0], RIGHT)
        c52 = card52()
        c52.move_to([0, -2.55, 0])
        u_seg1 = under(substring(c52.row, SEG1), TURN)
        u_seg2 = under(substring(c52.row, SEG2), TURN)
        pkt = solid_chip("hello", LOOKUP).move_to(brw0[0])
        caps = mono("HELLO", CAPTION, INK)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(relay), FadeIn(c142, shift=DOWN * 0.15), run_time=0.6)
            tok, hop = relay_hop(relay, 2.6)
            self.play(LaggedStart(*[Create(a) for a in routes], lag_ratio=0.55, run_time=2.6), hop)
            if hop.group in self.mobjects:              # the Succession's wrapper group
                self.remove(hop.group)
                self.add(tok)
            vo.wait_until("Port toy makes two containers talk directly")
            left = VGroup(relay, routes, c142)
            self.play(FadeOut(tok), left.animate.fade(0.7), FadeIn(gw0), FadeIn(pr0), run_time=0.7)
            self.play(GrowArrow(a_gp), run_time=0.6)
            vo.wait_until("and needs only Docker")
            self.play(FadeIn(ch24, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("a gateway serves a web page")
            self.play(FadeIn(brw0), GrowArrow(a_bg), FadeIn(c52, shift=UP * 0.15), run_time=0.7)
            self.play(Create(u_seg1), Indicate(gw0.frame, color=CTR, scale_factor=1.04), run_time=0.6)
            vo.wait_until("and forwards your text")
            self.play(FadeIn(pkt, scale=0.6), run_time=0.3)
            self.play(pkt.animate.move_to([2.7, Y_ROW, 0]), run_time=0.7)
            self.play(pkt.animate.move_to([5.45, Y_ROW, 0]), Create(u_seg2), run_time=0.9)
            vo.wait_until("which turns it into capitals")
            caps.move_to(pkt.text)
            self.play(ReplacementTransform(pkt.text, caps), Indicate(pr0.frame, color=CTR, scale_factor=1.04),
                      run_time=0.8)

        # ------------------------------------------------------------ 1. each box: its own localhost, its own ports
        boxes_t = {n: VGroup(net.boxes[n].frame.copy(), net.boxes[n].name.copy()) for n in net.boxes}
        brw_t = VGroup(net.browser.copy(), net.browser_label.copy())
        cap_ports = note("each box: its own ports · both could use 9100").move_to([1.95, under_net - 0.45, 0])
        lref33, lref34 = lecture_ref(4, "33"), lecture_ref(4, "34")   # top right (SLIDES.md S10 i)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(relay, routes, c142, ch24, c52, u_seg1, u_seg2, a_bg, a_gp, pkt)),
                      run_time=0.5)
            self.play(Transform(gw0, boxes_t["gateway"]), Transform(pr0, boxes_t["processor"]),
                      Transform(brw0, brw_t), run_time=1.1)
            self.remove(gw0, pr0, brw0)
            self.add(net)                               # its visible parts sit where the copies landed
            self.play(*net.parts_in("outline", "laptop_label"), FadeIn(lref33, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("with its own localhost")
            self.play(*net.parts_in("gateway_loop", "gateway_ll", "processor_loop", "processor_ll",
                                    "lp_loop", "lp_ll"), run_time=0.35)
            d1, l1 = net.loopback("gateway", run_time=1.0)
            d2, l2 = net.loopback("processor", run_time=1.0)
            d3 = Dot(radius=0.07, color=LOOKUP).move_to(lp_loop[0].get_start())
            self.play(*l1, *l2, MoveAlongPath(d3, lp_loop[0], run_time=1.0),
                      lp_loop.animate(run_time=1.0).set_color(TURN), lp_ll.animate(run_time=1.0).set_color(TURN))
            vo.wait_until("and its own full set of ports")
            # the loops calm down as the strips arrive (both on "full set of ports", not after it)
            self.play(FadeOut(d1), FadeOut(d2), FadeOut(d3), net.unloop("gateway"), net.unloop("processor"),
                      lp_loop.animate.set_color(LAPTOP), lp_ll.animate.set_color(LAPTOP),
                      *net.parts_in("gateway_strip", "processor_strip",
                                    anim=lambda m: FadeIn(m, shift=UP * 0.1)), run_time=0.7)
            vo.wait_until("Two containers can both use port 9100")
            n1, a1 = net.light_port("gateway", 9100)
            n2, a2 = net.light_port("processor", 9100)
            self.play(*a1, *a2, run_time=0.8)
            vo.wait_until("without any clash")
            self.play(FadeIn(cap_ports, shift=UP * 0.1), Indicate(n1, color=TURN), Indicate(n2, color=TURN),
                      run_time=0.8)
            # the bridge (SLIDES.md S10 ii): each glass box's frame flashes on its own (nothing joins
            # them yet), on "a network namespace"; then both localhost loops on "isolated"
            vo.wait_until("The lecture calls this")
            self.wait(0.7)        # "The lecture calls this" takes ~1 s: the flash runs on "a network namespace"
            self.play(*[ShowPassingFlash(net.boxes[n].frame.copy().set_stroke(CTR, 9, opacity=1).set_fill(opacity=0),
                                         time_width=0.5) for n in net.boxes], run_time=1.9)
            vo.wait_until("each container is isolated")
            # loop and label each grow about their own centre (as one group, the loop crossed the frame);
            # the label grows less, so its "l" does not touch the loop at the peak
            self.play(*[Indicate(net.boxes[n].loop, color=TURN, scale_factor=1.12) for n in net.boxes],
                      *[Indicate(net.boxes[n].loop_label, color=TURN, scale_factor=1.05) for n in net.boxes],
                      run_time=1.0)

        # ------------------------------------------------------------ 2. a network you create: a rail and a phone book
        udn = note("user-defined network", CTR).next_to(net.rail, DOWN, buff=0.05).align_to(net.rail, LEFT)
        mid_x = net.book_lines[0].get_center()[0]
        blanks = VGroup(blank_line(), blank_line())
        blanks[0].move_to([mid_x, net.book_lines[0].get_center()[1], 0])
        blanks[1].move_to([mid_x, net.book_lines[1].get_center()[1], 0])
        no_book = note("Docker's default network: no phone book (exercises)").move_to(cap_ports)
        # slide 34's term under the book glyph, in udn's row (udn ends at x ≈ 0.47)
        dns_l = note("Docker DNS", LOOKUP).align_to(udn, UP).set_x(net.parts["book"].get_center()[0])
        assert dns_l.get_left()[0] > udn.get_right()[0] + 0.3
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(n1), FadeOut(n2), FadeOut(cap_ports), net.unlight_port("gateway", 9100),
                      net.unlight_port("processor", 9100), ReplacementTransform(lref33, lref34), run_time=0.5)
            self.play(*net.parts_in("rail", anim=Create), run_time=1.0)
            net.attach(self, udn, anims=[FadeIn(udn, shift=UP * 0.1)], run_time=0.5)
            vo.wait_until("with a phone book")
            net.attach(self, dns_l, anims=[*net.parts_in("book"), FadeIn(dns_l, shift=UP * 0.1)], run_time=0.5)
            self.play(Indicate(net.parts["book"], color=LOOKUP, scale_factor=1.3), run_time=0.6)
            vo.wait_until("that turns container names into addresses")
            # the two blank lines rise out of the book glyph to where S13 writes the entries
            bc = net.parts["book"].get_center()
            net.attach(self, blanks, anims=[LaggedStart(*[GrowFromPoint(b, bc) for b in blanks], lag_ratio=0.4)],
                       extra=[Indicate(net.parts["book"], color=LOOKUP, scale_factor=1.15)], run_time=1.2)
            # GrowFromPoint put each line on the scene by itself; re-adding the piece takes those
            # top-level copies off (else they outlive FadeOut(net) and show through in beats 3-6)
            self.add(net)
            vo.wait_until("Docker's default network has none")
            self.play(FadeIn(no_book, shift=UP * 0.1), run_time=0.6)

        # ------------------------------------------------------------ 3. Prerequisites: docker run hello-world
        tr = tracker("P0", 1)
        t = term(P_WS, rows=12, title="laptop")
        cap_ws = note("your workspace")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(net), FadeOut(no_book), FadeOut(lref34), run_time=0.3)
            self.play(FadeIn(tr), FadeIn(t), run_time=0.3)
            ln0 = bare_prompt(self, t)
            cap_ws.set_y(ln0.strut.get_center()[1]).align_to(t.box, RIGHT).shift(LEFT * 0.35)
            self.play(FadeIn(cap_ws), Indicate(glyph_range(ln0, P_WS.index("~"), len(P_WS) - 1),
                                               color=TURN, scale_factor=1.1), run_time=0.4)
            vo.wait_until("docker run hello-world checks")
            ln = type_cmd(self, t, HELLO.cmd)
            self.remove(cap_ws)                          # it now scrolls / fades with its row
            ln.add(cap_ws)
            vo.wait_until("It pulls a tiny image")
            t.print(self, PULL, run_time=0.6)
            vo.wait_until("and prints hello from Docker")
            out = t.print(self, GREET, run_time=0.5)
            self.play(out[0].animate.set_color(S.GREEN), run_time=0.5)

        # ------------------------------------------------------------ 4. Step 1 · Get the code: clone, cd
        ch81 = readme_chip("README.md · line 81", PH81)
        ch81.move_to([0, 3.2, 0]).align_to([6.52, 0, 0], RIGHT)
        cap_cl = note("the README links the repo but prints no clone command")
        with self.voiceover(SAY[4]) as vo:
            tr = switch_section(self, tr, "P1", 1)
            t.clear(self)
            vo.wait_until("From your workspace folder")
            lb = bare_prompt(self, t)
            self.play(FadeIn(ch81, shift=DOWN * 0.15),
                      Indicate(glyph_range(lb, P_WS.index("~"), len(P_WS) - 1), color=TURN, scale_factor=1.1),
                      run_time=0.6)
            g = type_cmd(self, t, CLONE.cmd, type_time=1.85)     # done before "the README says …"
            t.print(self, CLONE.lines, run_time=0.4)
            vo.wait_until("the README says clone or download")
            p_row = g.rows[0]
            cap_cl.next_to(p_row.glyphs, RIGHT, buff=0.4).set_y(p_row.strut.get_center()[1])
            self.play(FadeIn(cap_cl, shift=LEFT * 0.1), Indicate(ch81.phrase, color=TURN, scale_factor=1.08),
                      run_time=0.6)
            self.remove(cap_cl)                          # pinned: it fades with its row
            p_row.add(cap_cl)
            vo.wait_until("Then cd into port toy")
            ln_cd = type_cmd(self, t, CD.cmd)
            cd_prompt(self, t, P_TOY, color=TURN)
            vo.wait_until("Pause and run them")
            yt = beside(your_turn(), t, ln_cd)
            pin(self, ln_cd, yt)

        # ------------------------------------------------------------ 5. two extra checks: the tree, the pinned commit
        card = tree_card()
        card.shift(UP * (TREE_BOTTOM - card.frame.get_bottom()[1]))
        card.shift(RIGHT * (-card.get_center()[0]))
        checks = {i: card.check_at(i) for i in range(2, 9)}
        # the ls command stays readable all beat: a GREY chip + `extra` in the card's header row
        lschip = chip(LS_CMD, S.GREY, size=CAPTION, font=MONO, pad_y=SLIM)
        lsg = VGroup(lschip, extra_tag()).arrange(RIGHT, buff=0.25).align_to(card.frame, RIGHT)
        lsg.shift(UP * (card.frame.get_top()[1] + 0.06 - lsg.get_bottom()[1]))
        assert lsg.get_left()[0] > card.header.get_right()[0] + 0.5
        # three batches (the strip has 3 rows), the strip cleared in place before each
        batches = ((LS_GW[:3], (2, 3, 4), 0.55), (LS_GW[3:] + LS_PR[:1], (5,), 0.45),
                   (LS_PR[1:], (6, 7, 8), 0.55))
        assert LS_PR[0] == "" and LS_PR[1] == "processor:"
        with self.voiceover(SAY[5]) as vo:
            # the ▶ rides along on its row and fades with it when the strip is cleared
            resize(self, t, 3, keep=2, run_time=0.5,
                   extra=[FadeIn(card, shift=UP * 0.15), FadeOut(ch81), caption_extra(tr, True)])
            ln_ls = type_cmd(self, t, LS_CMD, type_time=0.5)
            etag = beside(extra_tag(), t, ln_ls)
            self.add(lschip.box)                         # under the text that lands in it
            self.play(FadeIn(etag, shift=LEFT * 0.1), TransformFromCopy(substring(ln_ls, LS_CMD), lschip.text),
                      FadeIn(lschip.box), FadeIn(lsg[1], shift=LEFT * 0.1), run_time=0.45)
            self.remove(etag)                            # pinned: it fades with its row
            ln_ls.add(etag)
            for k, (lines, rows, rt) in enumerate(batches):
                wipe(self, t)
                t.print(self, lines, run_time=rt)
                self.play(LaggedStart(*[Create(checks[i]) for i in rows], lag_ratio=0.4), run_time=0.3)
                if k < len(batches) - 1:
                    self.wait(0.3)                       # each batch holds ~0.9 s before the next wipe
            vo.wait_until("and git log shows")
            ln_log = type_cmd(self, t, LOG_CMD, type_time=0.5)
            pin(self, ln_log, beside(extra_tag(), t, ln_log), run_time=0.25)
            row = t.print(self, [LOG], run_time=0.35)[0]
            hbox = glyph_box(row, "d190c71", S.GREY)
            hchip = chip("d190c71", S.GREY, size=CAPTION, font=MONO, pad_y=SLIM)
            htag = grey_tag("the pinned commit")
            VGroup(hchip, htag).arrange(RIGHT, buff=0.25).move_to([0, HASH_Y, 0]).align_to(card.frame, RIGHT)
            assert htag.get_bottom()[1] > lsg.get_top()[1] + 0.1 and htag.get_top()[1] < 3.6
            self.add(hchip.box)                          # under the text that lands in it
            self.play(Create(hbox), TransformFromCopy(glyph_range(row, 0, 7), hchip.text), FadeIn(hchip.box),
                      FadeIn(htag, shift=LEFT * 0.1), run_time=0.6)

        # ------------------------------------------------------------ 6. Step 1 · Create network: the rail gets its name
        net.shift(UP * NET_UP)                          # (invisible since beat 3) above the strip
        net.remove(dns_l)                               # beat 2's label: the ID chip lands on its spot
        idchip = solid_chip(ID_SHORT + "…", CTR).move_to([0.2, net.rail.get_center()[1], 0])
        dtag = differ_tag().move_to([0.2, net.parts["outline"].get_bottom()[1] - 0.36, 0])
        with self.voiceover(SAY[6]) as vo:
            # the hash's box goes now (its row scrolls); the commit chip stays until the rail is named
            self.play(FadeOut(card), *[FadeOut(c) for c in checks.values()], FadeOut(hbox), FadeOut(lsg),
                      tr.goto(2), run_time=0.3)
            self.play(FadeIn(net), run_time=0.3)        # one after the other: a cross-fade muddles both
            ln_net = type_cmd(self, t, NET.cmd, type_time=1.0)
            fly = substring(ln_net, "toynet").copy()
            rl = net.parts["rail_label"]
            net.detach(self, udn, anims=[FadeOut(udn)],
                       extra=[Transform(fly, mono("toynet", CAPTION, CTR).move_to(rl)), FadeOut(hchip),
                              FadeOut(htag)], run_time=0.5)
            self.play(FadeOut(fly), *net.parts_in("rail_label"), run_time=0.15)
            vo.wait_until("Docker prints the new network's ID")
            idl = t.print(self, [NET_ID], run_time=0.4)[0]
            self.add(idchip.box)                         # under the text that lands in it
            self.play(TransformFromCopy(glyph_range(idl, 0, 12), idchip.text), FadeIn(idchip.box), run_time=0.7)
            self.play(FadeIn(dtag, shift=UP * 0.1), run_time=0.3)
            vo.wait_until("that's the rail both containers will plug into")
            flash = net.rail.copy().set_stroke(TURN, 10, opacity=1)
            self.play(ShowPassingFlash(flash, time_width=0.5),
                      *[Indicate(net.boxes[n].frame, color=CTR, scale_factor=1.03) for n in net.boxes],
                      run_time=1.2)

        # ------------------------------------------------------------ 7. Handy commands · List networks
        with self.voiceover(SAY[7]) as vo:
            new = tracker("PH", 4)
            self.play(FadeOut(tr, shift=UP * 0.25), FadeIn(new, shift=DOWN * 0.25), FadeOut(net),
                      FadeOut(idchip), FadeOut(dtag), run_time=0.8)
            tr = new
            resize(self, t, 8, keep=2)
            ln_nls = type_cmd(self, t, NLS.cmd)
            out = t.print(self, NLS_OUT, run_time=0.5)
            vo.wait_until("lists it")
            tn = substring(out[4], "toynet")
            tbox = glyph_box(out[4], "toynet", CTR)
            self.play(tn.animate.set_color(CTR), Create(tbox), run_time=0.6)
            vo.wait_until("beside Docker's three built-in networks")
            x = max(out[k].glyphs.get_right()[0] for k in (1, 2, 3)) + 0.3
            top, bot = out[1].strut.get_top()[1] + 0.02, out[3].strut.get_bottom()[1] - 0.02
            br = VMobject(stroke_color=S.GREY, stroke_width=3)
            br.set_points_as_corners([[x - 0.1, top, 0], [x, top, 0], [x, bot, 0], [x - 0.1, bot, 0]])
            bt = grey_tag("built in").next_to(br, RIGHT, buff=0.2)
            self.play(Create(br), FadeIn(bt, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Pause, and create yours")
            pin(self, ln_nls, beside(your_turn(), t, ln_nls))
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        self.wait(0.2)
