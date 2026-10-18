"""S12 · Send a message: ports on the wire (port_toy README › Step 1, step 7 "Send a message";
V7's ticket).

Beats (script.md "## S12", one voiceover block each):
 0  TRACKER P1/6 -> P1/7. Right: PAGE(port-laptop/14) builds in three moments while a GREY
    README card at the left (README.md · lines 147–149, the three numbered steps as the README
    renders them) lights the step being done YELLOW: the address `localhost:8090` types itself;
    the input "hello from the laptop" types itself and Send is clicked; the reply card
    `HELLO FROM THE LAPTOP` and the port card fade in (the reply value flashes), and the three
    port lines turn YELLOW one after the other as the SAY names them.
 1  The card leaves. REPLY(14: 2) in a GREY strip at the bottom left (wrapped where a 56-column
    strip wraps, which is the field boundary after `"listen_port": 9200,`), tag "captured reply ·
    curl stood in for the Send button" above its left end; the tag and Send flash. Each JSON
    value gets a thin GREY box and a YELLOW copy of it rises into its place on the page, which
    gets the same box (upper -> reply card, listen_port -> line 2, sender_port -> line 3,
    gateway_out_port -> line 1).
 2  The page, the strip and the boxes fade; its first two port lines stay and rise above the
    picture as V7 fades in full width (ToyNet as S11 left it: laptop zone, street door, the PINK
    -p route into room :9100, both boxes on the toynet rail, room :9200, the dashed aim to
    `processor : 9200` on the rail); line 2 (`processor listening on port 9200`) is YELLOW while
    the SAY names it. "the destination": room :9200, the aim chip and line 2's 9200 flash.
    "But every connection has two ends": line 2 leaves, GREY caption "every connection has two
    ends, each with a port", room :9200 flashes PINK (this end). "the gateway's side": a dashed
    PINK slot "?" opens on the gateway's right wall and line 1 (`gateway sent from port 55620`)
    turns YELLOW. "Its operating system picked": a GREY gear appears in the gateway and turns
    while line 1's `55620` flies into the slot and becomes the PINK ticket; the ticket flashes
    and line 1 fades. "stapled it to the packet": a PINK packet slides out of the gateway's
    wall and a copy of the ticket lands on it, stapled.
 3  The aim chip's copy flies into room :9200 (the aim fades); the packet runs down to the rail,
    along it and up to the processor's door, and both tickets (the gateway's own, the one the
    processor received) pulse GREEN; "because nothing rewrites it": the packet's route flashes.
    Then the laptop side of V7 and the caption fade and the two boxes on the rail (with the gear
    and both tickets) move to the lower half. "Line 38 of the gateway": README chip README.md ·
    lines 161–169 "ephemeral source port" under the tracker; CODE(gateway/gateway.py: 32–38,
    comment cut) above: line 33 (connects by name) PINK bar, line 38 YELLOW bar with
    `getsockname()[1]` underlined, the gateway's ticket flashes; it gives way to
    CODE(processor/processor.py: 28–33, comment cut), line 32 YELLOW bar with
    `self.client_address[1]` underlined, the packet's ticket flashes.
 4  V7, the panel and the chip leave while the first packet (55620, dimmed, GREY "first send")
    and the gear move to the left column; then the page returns as it was (reply 14), with the
    strip REPLY(14) under it. Send is clicked: PAGE(15) — the port card's numbers turn into
    55634, the strip's text into REPLY(15: 2), and the gear prints a new PINK ticket 55634 onto a new packet ("send again");
    the new ticket and the page's two 55634 flash. Tag "your numbers will differ".
 5  The page and the rest leave except the page's glyph-only miniature diagram, which then
    zooms into the readable page_diagram (`localhost:8090 → :9100`, `out :55634 → dst :9200`);
    8090 turns YELLOW. Excerpt chip `const hostPort = location.port` (gateway/index.html · line 87
    (excerpt)) top left, `location.port` YELLOW, tag "read from the address bar", a YELLOW arrow
    from it to 8090. A GREY thought bubble "which door?" under the gateway box. A static GREY
    your-turn card (the browser steps + "leave both running: Step 2 inspects them") with
    ▶ your turn. Fade out to an empty frame.

Deviations from SHOW (and why):
- Beat 0: the README source is a three-row card, not a one-line chip: there is no terminal, the
  card fills the empty left half beside the page, and each row lights while the page does that
  step. The README's Markdown (`[http://localhost:8090](…)`, `**Send**`) is shown as rendered.
- Beat 1: the links are matched GREY boxes plus a YELLOW copy of each value rising into its
  place, not persistent lines: a 9.8-wide strip under a 6.6-wide page puts every straight line
  across the page's other rows, and the second row's lines across the first row's text.
- Beats 2–3: the destination tag is the aim chip `processor : 9200` on the rail (as common.py
  draws it); the packet carries only its ticket (a packet with both tags would not fit between
  the boxes). The chip's copy flies into room :9200 as the packet sets off, so the rail is clear.
  The PINK packet is this scene's own (the ticket rides on it; ToyNet.packet() is a bare body).
- Beat 2: SHOW lifts `55620` off the page before V7 is drawn, which would put the gateway's
  number on screen while the SAY speaks of the processor's 9200. Instead the first two port
  lines stay above the picture: line 2 is lit while the SAY names 9200, and line 1's `55620`
  flies into the gateway's slot when the SAY says the operating system picked it.
- Beat 3: the boxes move to the lower half at full size instead of shrinking: Piece.rescale keeps
  every label at 20 pt, and at the scale that fits under the 7-line panel the labels of V7 ran
  into each other (browser / 127.0.0.1:8090, 65535 / the cells, the localhost loops). The
  laptop side (outline, browser, street door, -p route) fades for this part, which frees the room.
- Beat 4: the page returns in its beat-1 state and then sends, so the change 55620 -> 55634 is
  seen on the page, in the strip and on a new packet beside the old one.
- Beat 5: the ▶ sits on a static your-turn card (the page has been replaced by the diagram), which
  carries SHOW's caption as its second row.
- Layout: the page's illustration tag sits under the window's right end, not above it, and the
  window's top is just under the tracker's first row: the strip's 22 pt tag is 7 wide and runs
  under the window's left edge, so the window has to end above it.
- Workarounds for common.py (requests filed in the report): PortPage's 5-digit port values
  touch the port card's right border, so each page's port lines are shifted 0.1 left; and
  PortPage.fill()'s first call drops glyphs, so the beat-0 page is built filled and its reply /
  ports parts are hidden with _hidden() and faded in with parts_in().
"""

import numpy as np
from common import (
    CTR,
    INK,
    LOOKUP,
    NARRATION,
    TURN,
    PortPage,
    Prose,
    ReplyStrip,
    ToyNet,
    _hidden,
    _keep,
    capture,
    differ_tag,
    excerpt,
    excerpt_chip,
    gear,
    grey_tag,
    note,
    page_diagram,
    page_reply,
    readme_card,
    readme_chip,
    ring,
    src_panel,
    thought,
    tracker,
    turn_card,
    under,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    TAU,
    UP,
    AddTextLetterByLetter,
    Arrow,
    Create,
    DashedLine,
    DashedVMobject,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    MoveAlongPath,
    ReplacementTransform,
    Restore,
    Rotate,
    RoundedRectangle,
    ShowPassingFlash,
    Transform,
    TransformFromCopy,
    VGroup,
    VMobject,
    linear,
    there_and_back,
)

from explainer import style as S
from explainer.devops import CAPTION, cell_width, glyph_range, mono, substring
from explainer.scene import VoiceScene

SAY = NARRATION["S12"]
assert len(SAY) == 6, len(SAY)

# ------------------------------------------------------------------ captures (file line numbers)
C14, C15 = capture("14", "port-laptop"), capture("15", "port-laptop")
R14, R15 = page_reply(C14, 2), page_reply(C15, 2)
LINE14, LINE15 = C14.line(2), C15.line(2)
assert R14 == {"upper": "HELLO FROM THE LAPTOP", "listen_port": 9200, "sender_port": 55620,
               "gateway_out_port": 55620}, R14
assert R15["gateway_out_port"] == R15["sender_port"] == 55634 and R15["listen_port"] == 9200
OUT1, OUT2 = str(R14["gateway_out_port"]), str(R15["gateway_out_port"])

# ------------------------------------------------------------------ sources
TOY = "port_toy/README.md"
assert excerpt(TOY, 147, 149).split("\n") == ["1. Open [http://localhost:8090](http://localhost:8090).",
                                              "2. Type a message.", "3. Click **Send**."]
README_ROWS = ["1. Open http://localhost:8090.", "2. Type a message.", "3. Click Send."]  # as rendered
PH161 = "ephemeral source port"
assert PH161 in excerpt(TOY, 161, 169).replace("**", "")
GW, PR = "port_toy/gateway/gateway.py", "port_toy/processor/processor.py"
assert "HTTPConnection(PROCESSOR_HOST, PROCESSOR_PORT)" in excerpt(GW, 33, 33)
assert "getsockname()[1]" in excerpt(GW, 38, 38)
assert "self.client_address[1]" in excerpt(PR, 32, 32)
L87 = excerpt("port_toy/gateway/index.html", 87, 87)
HOSTPORT = "const hostPort = location.port"
assert HOSTPORT in L87

# ------------------------------------------------------------------ layout
PAGE_RIGHT, PAGE_TOP = 6.5, 3.1        # the page's window (its illustration tag sits under it)
STRIP_COLS = 56                        # the strip wraps after `"listen_port": 9200, `
STRIP_W = 0.5 + (STRIP_COLS + 0.5) * cell_width(CAPTION)
STRIP_BOTTOM = -3.56
assert LINE14[STRIP_COLS:].startswith('"sender_port"')
LOW_TOP = -0.98                        # beat 3: the top of the boxes in the lower half
LAPTOP_SIDE = ("outline", "laptop_label", "zone", "door", "map")   # faded for the lower half
PAIR_TOP, PAIR_RIGHT = 2.55, 6.3       # beat 2: the two port lines kept from the page
DIAG_Y = -0.05                         # beat 5: the centre line of the diagram's boxes


def place_page(pg: PortPage) -> PortPage:
    """Right half, window top at PAGE_TOP (just under the tracker's first row); the illustration
    tag under the window's right end, so the strip's tag (which runs under the window's left
    edge) clears the window; port lines 0.1 left (the 5-digit values otherwise touch the port
    card's right border)."""
    pg.port_box.shift(LEFT * 0.1)
    pg.tag.next_to(pg.frame, DOWN, buff=0.08).align_to(pg.frame, RIGHT)
    pg.shift([PAGE_RIGHT - pg.frame.get_right()[0], PAGE_TOP - pg.frame.get_top()[1], 0])
    return pg


def place_strip(text: str) -> ReplyStrip:
    """REPLY at the bottom left (left of and under the page), its tag above its left end."""
    st = ReplyStrip(text, width=STRIP_W)
    assert [r.text for r in st.rows] == [text[:STRIP_COLS], text[STRIP_COLS:]], [r.text for r in st.rows]
    st.tag.next_to(st.frame, UP, buff=0.05).align_to(st.frame, LEFT)
    st.shift([-6.5 - st.frame.get_left()[0], STRIP_BOTTOM - st.frame.get_bottom()[1], 0])
    return st


def ticket(num: str) -> VGroup:
    """V7's ephemeral-port ticket: a PINK ticket (perforated stub at its left) with the number.
    .frame .text"""
    t = mono(num, CAPTION, LOOKUP)
    fr = RoundedRectangle(width=t.width + 0.55, height=0.42, corner_radius=0.06, stroke_color=LOOKUP,
                          stroke_width=2.5).set_fill(S.BG, 1)
    x = fr.get_left()[0] + 0.17
    perf = DashedLine([x, fr.get_top()[1], 0], [x, fr.get_bottom()[1], 0], color=LOOKUP, stroke_width=2,
                      dash_length=0.05)
    t.move_to(fr).shift(RIGHT * 0.09)
    g = VGroup(fr, perf, t)
    g.frame, g.text = fr, t
    return _keep(g)


def packet_body(w: float = 1.62, h: float = 0.6) -> VMobject:
    """A PINK packet (the ticket gets stapled onto it)."""
    return RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=LOOKUP,
                            stroke_width=3).set_fill(LOOKUP, 0.45)


def staple(tk: VGroup) -> VMobject:
    """A small staple across the ticket's top edge, over its stub."""
    c = tk.frame.get_corner(UP + LEFT) + RIGHT * 0.33
    m = VMobject(stroke_color=INK, stroke_width=3.5)
    m.set_points_as_corners([c + np.array([-0.09, -0.07, 0]), c + np.array([-0.09, 0.07, 0]),
                             c + np.array([0.09, 0.07, 0]), c + np.array([0.09, -0.07, 0])])
    return m


def slot(w: float, h: float = 0.42) -> VGroup:
    """The gateway's end of the connection, still without a port: a dashed PINK slot with "?"."""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=LOOKUP, stroke_width=2.5)
    dashed = DashedVMobject(fr, num_dashes=22, dashed_ratio=0.55)
    q = mono("?", CAPTION, LOOKUP).move_to(fr)
    g = VGroup(dashed, q)
    g.frame, g.q = dashed, q
    return g


def pulse(tk: VGroup, color: str) -> list:
    """A ticket pulses `color` (its outline and number, there and back; its dark fill stays).
    A list, not an AnimationGroup: the group's wrapper would draw the frame over the number."""
    return [tk.frame.animate(rate_func=there_and_back).set_stroke(color, 5),
            Indicate(tk.text, color=color, scale_factor=1.25)]


def text_glyphs(t, s: str, sub: str) -> VGroup:
    """Glyphs of `sub` in a one-line Text `t` that shows `s` (Text has no glyphs for spaces)."""
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


class SendMessage(VoiceScene):
    def construct(self):
        # ============================================================ 0 · open, type, Send
        tr = tracker("P1", 6)
        # built filled and then hidden: PortPage.fill()'s first call (become) drops glyphs
        pg = place_page(PortPage(8090, reply=R14))
        _hidden(pg.parts["reply"])
        _hidden(pg.parts["ports"])
        inp = next(m for m in pg.submobjects if any(s is pg.send for s in m.submobjects))
        field_text = inp[0][1]
        inp[0].remove(field_text)                   # typed in on "type a message"
        addr = pg.address
        pg.frame.remove(addr)                       # typed in on "open localhost 8090"
        card = readme_card("README.md · lines 147–149", README_ROWS)
        card.shift([-6.45 - card.get_left()[0], 2.72 - card.get_top()[1], 0])
        rows = card.rows

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.4)
            self.play(tr.goto(7), FadeIn(card, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("open localhost 8090")
            self.play(FadeIn(pg), rows[0].animate.set_color(TURN), run_time=0.5)
            self.play(AddTextLetterByLetter(addr, time_per_char=0.06))
            self.remove(addr)
            pg.frame.add(addr)
            vo.wait_until("type a message")
            self.play(rows[0].animate.set_color(INK), rows[1].animate.set_color(TURN), run_time=0.3)
            self.play(AddTextLetterByLetter(field_text, time_per_char=0.045))
            self.remove(field_text)
            inp[0].add(field_text)
            vo.wait_until("and click Send")
            self.play(rows[1].animate.set_color(INK), rows[2].animate.set_color(TURN), pg.click(),
                      run_time=0.6)
            vo.wait_until("The reply comes back")
            self.play(*pg.parts_in("reply", "ports"), rows[2].animate.set_color(INK), run_time=0.8)
            self.play(Indicate(pg.reply_value.glyphs, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("with three port numbers")
            pcard = pg.parts["ports"]
            self.play(Indicate(pcard[0], color=TURN, scale_factor=1.03), run_time=0.7)
            lines = pg.port_lines
            vo.wait_until("where the gateway sent from")
            self.play(lines[0].glyphs.animate.set_color(TURN), run_time=0.4)
            vo.wait_until("where the processor listened")
            self.play(lines[0].glyphs.animate.set_color(INK), lines[1].glyphs.animate.set_color(TURN),
                      run_time=0.4)
            vo.wait_until("and where it saw")
            self.play(lines[1].glyphs.animate.set_color(INK), lines[2].glyphs.animate.set_color(TURN),
                      run_time=0.4)

        # ============================================================ 1 · the captured reply
        strip = place_strip(LINE14)
        assert strip.tag.get_top()[1] < pg.frame.get_bottom()[1] - 0.06, (strip.tag.get_top()[1], pg.frame.get_bottom()[1])
        assert strip.frame.get_right()[0] < pg.tag.get_left()[0] - 0.3
        r1, r2 = strip.rows
        pairs = [(substring(r1, R14["upper"]), pg.reply_value.glyphs),
                 (substring(r1, "9200"), pg.value("listen_port")),
                 (substring(r2, OUT1, 0), pg.value("sender_port")),
                 (substring(r2, OUT1, 1), pg.value("gateway_out_port"))]
        rings_src = [ring(a, S.GREY, buff=0.035, stroke=2) for a, _ in pairs]
        rings_dst = [ring(b, S.GREY, buff=0.035, stroke=2) for _, b in pairs]

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(card, shift=LEFT * 0.15), lines[2].glyphs.animate.set_color(INK),
                      FadeIn(strip, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("so curl sent the same request")
            self.play(Indicate(strip.tag.text, color=INK, scale_factor=1.06),
                      Indicate(pg.send, color=TURN, scale_factor=1.15), run_time=0.9)
            vo.wait_until("this is the reply it got")
            self.play(LaggedStart(*[Create(r) for r in rings_src], lag_ratio=0.2), run_time=0.6)
            copies = [a.copy().set_color(TURN) for a, _ in pairs]
            self.play(LaggedStart(*[Transform(c, b.copy().set_color(TURN)) for c, (_, b) in zip(copies, pairs)],
                                  lag_ratio=0.22), run_time=1.3)
            self.play(*[Create(r) for r in rings_dst], *[FadeOut(c) for c in copies], run_time=0.5)

        # ============================================================ 2 · the ticket
        net = ToyNet(show=("outline", "laptop_label", "zone", "boxes", "rail", "rail_label",
                           "plug_gateway", "plug_processor", "door", "room_gateway", "room_processor",
                           "map", "aim"))
        g_fr, p_fr = net.boxes["gateway"].frame, net.boxes["processor"].frame
        line1, line2 = lines[0], lines[1]
        val1, val2 = glyph_range(line1, 30), glyph_range(line2, 30)
        pair = VGroup(line1, line2)
        tk = ticket(OUT1)
        sl = slot(tk.frame.width)
        sl.move_to([g_fr.get_right()[0] + 0.12 + sl.width / 2, g_fr.get_top()[1] - 0.32, 0])
        tk.move_to(sl)
        gr = gear(0.22).move_to([g_fr.get_right()[0] - 0.42, g_fr.get_top()[1] - 0.36, 0])
        cap = note("every connection has two ends, each with a port")
        cap.move_to([(g_fr.get_left()[0] + p_fr.get_right()[0]) / 2, net.parts["outline"].get_bottom()[1] - 0.45, 0])
        body = packet_body()
        body.move_to([g_fr.get_right()[0] + 0.15 + body.width / 2, g_fr.get_bottom()[1] + 0.45, 0])

        with self.voiceover(SAY[2]) as vo:
            # the page goes; its first two port lines stay and rise above the picture
            for ln in (line1, line2):
                pg.port_box.remove(ln)
            self.add(line1, line2)
            self.play(FadeOut(pg), FadeOut(strip), *[FadeOut(r) for r in rings_src + rings_dst],
                      line2.glyphs.animate.set_color(TURN), run_time=0.6)
            up = np.array([PAIR_RIGHT - pair.get_right()[0], PAIR_TOP - pair.get_top()[1], 0])
            self.play(pair.animate.shift(up), FadeIn(net), run_time=0.8)
            assert pair.get_bottom()[1] > net.get_top()[1] + 0.2, (pair.get_bottom()[1], net.get_top()[1])
            vo.wait_until("the destination")
            self.play(Indicate(net.rooms["processor"], color=TURN, scale_factor=1.25),
                      Indicate(net.aim_chip[1], color=TURN, scale_factor=1.12),
                      Indicate(val2, color=TURN, scale_factor=1.2), run_time=0.9)
            vo.wait_until("But every connection has two ends")
            self.play(FadeIn(cap, shift=UP * 0.1), FadeOut(line2), run_time=0.5)
            self.play(Indicate(net.rooms["processor"].frame, color=LOOKUP, scale_factor=1.3), run_time=0.6)
            vo.wait_until("so the gateway's side needs a port too")
            self.play(Create(sl.frame), FadeIn(sl.q), line1.glyphs.animate.set_color(TURN), run_time=0.6)
            vo.wait_until("Its operating system picked")
            self.play(FadeIn(gr, scale=0.5), run_time=0.4)
            # the gear turns and the page's 55620 lands in the slot as the gateway's PINK ticket
            self.add(tk.frame, tk[1])                # under the number that flies into it
            self.play(Rotate(gr, TAU / 2), FadeOut(sl.q), FadeIn(tk.frame), FadeIn(tk[1]),
                      TransformFromCopy(val1, tk.text), run_time=1.0)
            self.remove(sl.frame, tk.frame, tk[1], tk.text)
            self.add(tk)
            self.wait(0.6)
            self.play(Indicate(tk.text, color=LOOKUP, scale_factor=1.2), FadeOut(line1), run_time=0.7)
            vo.wait_until("and stapled it to the packet")
            self.play(FadeIn(body, shift=RIGHT * 0.3), run_time=0.4)
            tk2 = tk.copy()
            self.add(tk2)                            # above the packet it lands on
            self.play(tk2.animate.move_to(body), run_time=0.6)
            st = staple(tk2)
            self.play(Create(st), run_time=0.3)
            pk = _keep(VGroup(body, tk2, st))
            self.remove(body, tk2, st)
            self.add(pk)

        # ============================================================ 3 · it arrives; the code
        rd = net.rooms["processor"].frame
        rail_y = net.rail.get_center()[1]
        x_up = rd.get_left()[0] - 0.06 - pk.width / 2
        path = VMobject().set_points_as_corners([pk.get_center(), [pk.get_x(), rail_y, 0], [x_up, rail_y, 0],
                                                 [x_up, rd.get_center()[1], 0]])
        chip_copy = net.aim_chip.copy()
        gwp = src_panel(GW, 32, 38, cut_comments=True, size=CAPTION)
        prp = src_panel(PR, 28, 33, cut_comments=True, size=CAPTION)
        ch161 = readme_chip("README.md · lines 161–169", PH161)
        ch161.shift([-6.5 - ch161.get_left()[0], 2.84 - ch161.get_top()[1], 0])
        for p in (gwp, prp):
            p.shift([-6.45 - p.get_left()[0], ch161.get_bottom()[1] - 0.1 - p.get_top()[1], 0])
        assert gwp.get_bottom()[1] > LOW_TOP + 0.08, gwp.get_bottom()[1]

        with self.voiceover(SAY[3]) as vo:
            self.add(chip_copy)
            self.play(*net.parts_out("aim"), chip_copy.animate.scale(0.4).move_to(net.rooms["processor"].frame).set_opacity(0),
                      Indicate(net.rooms["processor"].label, color=LOOKUP, scale_factor=1.3), run_time=0.6)
            self.remove(chip_copy)
            self.play(MoveAlongPath(pk, path, rate_func=linear), run_time=1.4)
            # the processor reads the same number: both ends' tickets pulse GREEN
            self.play(*pulse(tk, S.GREEN), *pulse(tk2, S.GREEN), run_time=0.8)
            vo.wait_until("because nothing rewrites it")
            flash = path.copy().set_stroke(LOOKUP, 6)
            self.play(ShowPassingFlash(flash, time_width=0.6), run_time=0.9)

            # the laptop side fades; the two boxes, the rail, the gear and both tickets move down
            self.play(*net.parts_out(*LAPTOP_SIDE), FadeOut(cap), run_time=0.4)
            seen = VGroup(net.boxes["gateway"], net.boxes["processor"], net.rooms["gateway"],
                          net.parts["rail_label"], net.rail, tk, gr, pk)          # geometry only
            v = np.array([-(seen.get_left()[0] + seen.get_right()[0]) / 2, LOW_TOP - seen.get_top()[1], 0])
            self.play(*[m.animate.shift(v) for m in (net, tk, gr, pk)], run_time=0.8)
            vo.wait_until("Line 38 of the gateway")
            self.play(FadeIn(ch161, shift=DOWN * 0.1), FadeIn(gwp, shift=DOWN * 0.1), run_time=0.5)
            b33 = gwp.bar(33, LOOKUP, 0.2)
            b38 = gwp.bar(38, TURN, 0.2)
            u38 = under(gwp.span(38, "getsockname()[1]"), TURN, stroke=3)
            self.play(FadeIn(b33), FadeIn(b38), Create(u38), *pulse(tk, TURN),
                      run_time=0.7)

            vo.wait_until("line 32 of the processor")
            b32 = prp.bar(32, TURN, 0.2)
            u32 = under(prp.span(32, "self.client_address[1]"), TURN, stroke=3)
            self.play(FadeOut(VGroup(gwp, b33, b38, u38), shift=UP * 0.1), FadeIn(prp, shift=UP * 0.1),
                      run_time=0.6)
            self.play(FadeIn(b32), Create(u32), *pulse(tk2, TURN), run_time=0.7)

        # ============================================================ 4 · send again
        pg2 = place_page(PortPage(8090, reply=R14))
        strip2 = place_strip(LINE14)
        strip3 = place_strip(LINE15)
        old_at = np.array([-3.3, 1.45, 0])
        new_at = np.array([-3.3, 0.45, 0])
        gr_at = np.array([-1.35, new_at[1], 0])
        n_old = note("first send").move_to([0, old_at[1], 0]).align_to([-6.4, 0, 0], LEFT)
        n_new = note("send again").move_to([0, new_at[1], 0]).align_to([-6.4, 0, 0], LEFT)
        tk_new = ticket(OUT2)
        body2 = packet_body().move_to(new_at)
        tk_new.move_to(body2)
        st_new = staple(tk_new)
        tk_new.save_state()
        tk_new.scale(0.2).move_to(gr_at)
        dtag = differ_tag().next_to(body2, DOWN, buff=0.3)

        with self.voiceover(SAY[4]) as vo:
            # the gear and the first packet go to the left column first (so the packet never
            # crosses the page as it comes back), then the page and the strip return and Send
            self.play(FadeOut(net), FadeOut(VGroup(prp, b32, u32)), FadeOut(ch161), FadeOut(tk),
                      gr.animate.move_to(gr_at), pk.animate.move_to(old_at).fade(0.55), FadeIn(n_old),
                      run_time=0.6)
            self.play(FadeIn(pg2), FadeIn(strip2), run_time=0.5)
            self.play(pg2.click(), run_time=0.4)
            vo.wait_until("and the number changes")
            self.play(*pg2.fill(R15), Transform(strip2.rows, strip3.rows), Rotate(gr, TAU / 2),
                      FadeIn(body2, shift=RIGHT * 0.2), FadeIn(n_new), run_time=0.9)
            self.add(tk_new)                          # above the new packet
            self.play(Restore(tk_new), run_time=0.6)
            self.play(Create(st_new), run_time=0.3)
            vo.wait_until("a new connection")
            self.play(Indicate(tk_new.text, color=TURN, scale_factor=1.2),
                      Indicate(pg2.value("gateway_out_port"), color=TURN, scale_factor=1.2),
                      Indicate(pg2.value("sender_port"), color=TURN, scale_factor=1.2), run_time=0.9)
            vo.wait_until("Yours will differ")
            self.play(FadeIn(dtag, shift=UP * 0.1), run_time=0.5)
        pk_new = VGroup(body2, tk_new, st_new)

        # ============================================================ 5 · the page reads its own address bar
        pd = page_diagram("8090", OUT2, "9200")
        pd.shift([0, DIAG_Y - pd.boxes.get_center()[1], 0])
        glyph = pg2.parts["diagram"]
        frames = VGroup(*[b[0] for b in pd.boxes])
        texts = VGroup(*[b[1] for b in pd.boxes])
        ec = excerpt_chip(HOSTPORT, "gateway/index.html · line 87 (excerpt)", line=L87)
        ec.shift([-6.4 - ec.get_left()[0], 2.78 - ec.get_top()[1], 0])
        lp = text_glyphs(ec.text, HOSTPORT, "location.port")
        rtag = grey_tag("read from the address bar").next_to(ec.chip, RIGHT, buff=0.3)
        arr = Arrow(lp.get_bottom() + DOWN * 0.04, pd.host.get_top() + UP * 0.06, buff=0, color=TURN,
                    stroke_width=4, max_tip_length_to_length_ratio=0.25)
        # the thought bubble hangs under the gateway box, its two small circles rising to it
        bub = thought("which door?")
        gbox = pd.boxes[1][0]
        VGroup(bub.frame, bub.text).move_to([gbox.get_center()[0] + 0.5, gbox.get_bottom()[1] - 0.48
                                             - bub.frame.height / 2, 0])
        bub[2].move_to([gbox.get_center()[0] + 0.08, bub.frame.get_top()[1] + 0.13, 0])
        bub[3].move_to([gbox.get_center()[0] + 0.0, bub[2].get_top()[1] + 0.1, 0])
        tc = turn_card([Prose("in your browser: localhost:8090 · type a message · Send"),
                        Prose("leave both running: Step 2 inspects them")])
        tc.shift([0 - tc.frame.get_center()[0], -3.45 - tc.frame.get_bottom()[1], 0])
        assert bub.get_bottom()[1] > tc.get_top()[1] + 0.15, (bub.get_bottom()[1], tc.get_top()[1])

        with self.voiceover(SAY[5]) as vo:
            # everything but the page's miniature diagram leaves; the miniature grows into the diagram
            pg2.remove(glyph)
            self.add(*glyph)
            self.play(FadeOut(pg2), FadeOut(strip2), FadeOut(pk), FadeOut(pk_new), FadeOut(gr), FadeOut(dtag),
                      FadeOut(n_old), FadeOut(n_new), run_time=0.5)
            self.play(ReplacementTransform(glyph[0], frames), ReplacementTransform(glyph[1], pd[1]),
                      run_time=1.0)
            self.play(FadeIn(texts), FadeIn(pd.labels), run_time=0.6)
            vo.wait_until("shows 8090")
            self.play(pd.host.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(pd.host, color=TURN, scale_factor=1.25), run_time=0.6)
            vo.wait_until("by reading its own address bar")
            self.play(FadeIn(ec, shift=DOWN * 0.1), run_time=0.5)
            self.play(lp.animate.set_color(TURN), FadeIn(rtag, shift=LEFT * 0.1), run_time=0.5)
            self.play(Create(arr), run_time=0.5)
            vo.wait_until("The container can't know")
            self.play(FadeIn(bub, scale=0.8), Indicate(gbox, color=CTR, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Pause, send a message")
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.6)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        self.wait(0.2)
