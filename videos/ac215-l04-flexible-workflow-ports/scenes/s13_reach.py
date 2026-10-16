"""S13 · Who can reach whom (port_toy README › Step 2 "Check the ports", steps 1-3; Handy
commands 5 and 1; V6 + V7).

Beats (script.md "## S13", one voiceover block each):
 0  TRACKER P2/1. Terminal (12 rows, `laptop`, port_toy prompt) types `docker ps` and prints
    port-laptop/16 lines 2-4 wrapped at 65 (the PORTS column lands on each line's second row).
    The gateway's `127.0.0.1:8090->9100/tcp` turns YELLOW; `127.0.0.1`, `8090` and `9100` flash as
    they are named; README chip `README.md · line 230` "The host port comes first" in the top
    band. The processor's empty PORTS cell gets a dashed YELLOW box (the header's PORTS flashes)
    and a GREY tag "listening ≠ published" under it.
 1  TRACKER P2/1 · extra. The terminal shrinks to 6 rows (cleared) and types the three-column
    `docker ps --format …` (extra) under the prompt -> 17 lines 2-4; above it the README's sample
    (expected/port_toy-docker-ps.txt lines 2-4, header "README.md · lines 204–206", tag
    `expected`) in the terminal's own column grid; a GREEN "=" writes beside each row as the
    matching terminal row flashes.
 2  V6+V7 (ToyNet: laptop zone, street door 127.0.0.1:8090 with the PINK -p route into room
    :9100, both boxes on the toynet rail, room :9200, the blank phone book) fills the upper half.
    "What does the 127.0.0.1 do?": the door's `127.0.0.1` turns YELLOW. README chip
    `README.md · line 239` "-p 8090:9100"; the extra `docker run … -p 8090:9100 …` is typed (its
    -p flag PINK), the ID prints and a dashed TEAL box `gateway-all` (with its own room :9100)
    appears between the boxes. A dashed PINK request arrow runs from it toward the laptop's door.
    "Docker refuses": 18 line 3 prints wrapped; `Bind for 127.0.0.1:8090 failed: port is already
    allocated` turns RED, the arrow turns RED and stops on a cross, the door flashes RED. "our
    gateway holds 8090": the PINK route flashes; caption "host doors collide / rooms never do"
    under the ghost box (the three rooms unchanged). `docker rm gateway-all` (extra) -> 19 line
    2 with the GREY tag "created anyway · remove it"; the ghost box fades.
 3  `docker run … -p 8091:9100 …` (extra) -> 20 line 2; `gateway-all` returns as a solid box
    plugged into the rail, and the second street door `0.0.0.0:8091` opens on the wall. The
    three-column ps (extra) -> 21 lines 2-5: `0.0.0.0:8091->9100/tcp` YELLOW, the door's label
    flashes; GREY tag "yours may also list [::]:8091 (IPv6)" in the top band. "other machines":
    the outside machines and their dashed route to that door. "Remove it": `docker rm -f
    gateway-all` (extra) -> 21 line 6; the box, the door and the machines leave. "That's why the
    README writes 127.0.0.1": the first door's `127.0.0.1` flashes and the route from the
    laptop's own browser lights up (only the laptop reaches that door).
 4  TRACKER P2/2. The terminal clears. `curl http://localhost:8090` (the route from the browser
    lights up) -> 22 lines 2-7, …, 154-155 (cut). `curl --max-time 3 http://localhost:9200/health`
    -> 23 line 2 RED; V7's dashed ":9200 ?" arrow from the laptop stops at the wall and turns RED
    with a cross. README chip `README.md · line 262` "nothing else is using port 9200".
 5  TRACKER P2/3. The terminal clears. `docker exec gateway curl http://processor:9200/health`;
    its `processor` turns PINK as it is named and a PINK packet leaves the gateway, runs along
    the rail and enters the processor's room :9200 (which flashes). 24 lines 2-5 print: the GREY
    tag "curl's progress meter" sits in the blank left part of the meter's middle row, `ok`
    turns GREEN and the room flashes GREEN.
 6  The terminal leaves. Both boxes' localhost loops dim, a GREY "?" beside each. The command
    chip (two rows, folded as a shell command) appears under the picture with `localhost` boxed
    YELLOW. After the block: PONDER(6 s) card at the bottom right (the picture shows no answer).
 7  The card and the chip leave, the terminal returns. `docker exec gateway curl --max-time 3
    http://localhost:9200/health` -> 25: `…` (the progress meter), lines 5-6 joined and wrapped,
    RED. "Inside the gateway, localhost is the gateway itself": only now the gateway's loop
    glows YELLOW as a packet dot circles it; "nothing there listens on 9200": the dot turns RED
    with a cross. "the second puzzle": README chip `README.md · line 290` "localhost means the
    gateway" in the band and a YELLOW tick "puzzle 2" by the gateway; "each container has its
    own localhost": the three loops (laptop, gateway, processor) flash. TRACKER P2/3 · extra:
    `docker exec gateway curl -s http://localhost:9100 | head -4` (extra) -> 26 lines 2-5; the dot
    lands on the gateway's own room :9100, which flashes GREEN with a GREEN tick.
 8  TRACKER PH/5. "So how did the name work?": the phone book flashes. V6/V7 fade while the
    terminal (cleared) grows to 13 rows; `docker network inspect toynet` -> 28 lines 4, …, 16, …,
    32, …, 35, …, 39, …, 42, …; `gateway` / `172.19.0.3/16` and `processor` / `172.19.0.2/16`
    turn PINK, then `172.19.0.0/16`. The terminal shrinks to 6 rows keeping those five lines, V6
    returns, and the names and addresses fly into the phone book (TransformFromCopy):
    `processor → 172.19.0.2`, `gateway → 172.19.0.3`.
 9  TRACKER PH/5 · extra. The terminal clears. `docker exec gateway cat /etc/resolv.conf`
    (extra) -> 29: …, 6, … with `127.0.0.11` PINK; each box gets its dashed PINK line to the phone
    book, labelled `127.0.0.11`. `docker exec gateway getent hosts processor gateway` (extra) ->
    29 lines 13-14 (PINK) as the book's entries flash. GREY note "addresses may change on
    restart · names stay" in the band; the names in the book flash.
10  TRACKER PH/1. The terminal clears. `docker exec -it gateway sh`: the frame turns TEAL
    (`container · gateway`), the session 29b lines 2-6 replays (`hostname`, `ls`, `exit` typed at
    `#`); `3bf0f65d0cf0` gets the GREY tag "= the gateway's container ID (docker ps)"; `exit`
    returns to the laptop. "One aside": V6 leaves; PANEL(27 line 2, cut) headed `docker exec
    processor curl --version | head -1` + `extra`, with the GREY tag "erratum · README.md line
    294: the processor doesn't need curl · it has it anyway" under it. "Pause": the terminal
    gives way to the static GREY your-turn card with the five commands; ▶ your turn on it. Fade
    out to an empty frame.

Deviations from SHOW (and why):
- Beat 1: the terminal shrinks to 6 rows here, not in beat 2: the README's sample needs the room
  above the terminal (above 12 rows there are 0.7 units), and beat 2 needs 6 rows anyway. The
  sample is drawn above the terminal (in the terminal's character grid, so the columns line up),
  not beside it: the terminal is full width.
- Beats 2-10: ToyNet is squashed vertically to 0.95 (shapes only; texts and glyphs keep their
  size, S11's helper): unsquashed, its 3.08 units exactly fill the space between the tracker
  band and the 6-row terminal, with no gap.
- Beat 2: "a second PINK arrow aims at the laptop's door 8090" is drawn from a dashed `gateway-all`
  box (the container docker created anyway, between the two boxes, with its own room :9100, so
  "rooms never do" collide is visible) along the lane above the gateway box to the laptop's
  wall, and stops right above the door's column with a RED cross while the door flashes RED: a
  route into the door itself would cross the gateway's room and the existing -p route. Terminal
  scrolls of two or more rows fade the leaving rows in place before the rest slide up
  (soft_scroll), so nothing slides over the picture. The ID line and the command scroll out of the
  6-row terminal when the 5-row error prints (the error and its RED tail stay).
- Beats 2-4: long outputs (the error, the HTML page) scroll their command out of the 6-row
  strip; the final your-turn card lists the README commands as typed.
- Beat 3: the IPv6 tag sits in the top band (the ps rows leave 11 columns, the tag is 5 units).
- Beat 4 / 7: the README chips quote a shorter exact part of their line ("nothing else is using
  port 9200", "localhost means the gateway"): the SHOW's phrases make chips of 8.4 and 7.7 units,
  and the band right of the tracker is 7.2.
- Beat 5: the progress-meter tag sits in the blank left half of the meter's middle row (the rows
  are full to column 65).
- Beat 6: the command chip sits under the picture, folded on two rows as a shell command, left of
  the ponder card: above the picture there is only the tracker band, and one 11.5-unit row plus
  the card do not fit under it. The terminal leaves for the ponder and returns in beat 7.
- Beat 7: "the packet loops back" is a PINK dot circling the gateway's loop (ToyNet.loopback);
  "where no :9200 door exists" is the dot turning RED with a cross; it then hops to room :9100.
- Beat 8: the terminal grows to 13 rows, not 12: the command plus the 12 listed lines.
- Beats 8 and 10: the picture leaves before the terminal grows (or the panel arrives) and returns
  after the terminal has shrunk, and the terminal leaves before the your-turn card takes its
  place, so no two of them cross mid-move.
- Beat 10: V6 leaves when the panel arrives (it fills the upper half); the panel's header is the
  command in mono plus an `extra` tag (a header string would set the command in serif).
"""

import numpy as np
from common import (
    CTR,
    ERR,
    INK,
    LOOKUP,
    NARRATION,
    P_SH,
    P_TOY,
    TERM_PT,
    TURN,
    VENV,
    ToyNet,
    _keep,
    _save_op,
    _set_op,
    beside,
    caption_extra,
    capture,
    col_box,
    door,
    enter_container,
    erratum_tag,
    excerpt,
    expected_tag,
    extra_tag,
    grey_tag,
    leave_container,
    log_panel,
    note,
    pin,
    readme_chip,
    resize,
    session,
    strip_top,
    switch_section,
    term,
    tracker,
    turn_card,
    type_cmd,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    Polygon,
    ShowPassingFlash,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
    VMobject,
    linear,
)

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import (
    CAPTION,
    box,
    cell_width,
    check_mark,
    cross_mark,
    mono,
    mono_line,
    substring,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S13"]
assert len(SAY) == 11, len(SAY)

# ------------------------------------------------------------------ captures (file line numbers)
PL = "port-laptop"
C16, C17, C18, C19 = (capture(n, PL) for n in ("16", "17", "18", "19"))
C20, C21, C22, C23 = (capture(n, PL) for n in ("20", "21", "22", "23"))
C24, C25, C26, C27 = (capture(n, PL) for n in ("24", "25", "26", "27"))
C28, C29, C29B = (capture(n, PL) for n in ("28", "29", "29b"))
EXP = capture("port_toy-docker-ps", "expected")
PS_FMT, RM_F = C21.cmd.split("; ")                 # one `$` line, typed as two commands
assert PS_FMT == C17.cmd and RM_F == "docker rm -f gateway-all", C21.cmd
RESOLV, GETENT = C29.cmd.split("; ")
assert RESOLV == "docker exec gateway cat /etc/resolv.conf" and GETENT.endswith("hosts processor gateway")
assert C16.cmd == "docker ps" and C22.cmd == "curl http://localhost:8090"
assert C23.cmd == "curl --max-time 3 http://localhost:9200/health"
assert C24.cmd == "docker exec gateway curl http://processor:9200/health"
assert C25.cmd == "docker exec gateway curl --max-time 3 http://localhost:9200/health"
assert C26.cmd == "docker exec gateway curl -s http://localhost:9100 | head -4"
assert C28.cmd == "docker network inspect toynet" and C29B.cmd == "docker exec -it gateway sh"
GW_MAP = "127.0.0.1:8090->9100/tcp"
ZERO_MAP = "0.0.0.0:8091->9100/tcp"
BIND = "Bind for 127.0.0.1:8090 failed: port is already allocated"
assert BIND in C18.line(3) and ZERO_MAP in C21.line(3) and GW_MAP in C16.line(3)
assert C24.line(5) == "ok" and C29B.line(3) == "3bf0f65d0cf0"
assert C28.line(16).strip() == '"Subnet": "172.19.0.0/16",'
assert '"gateway"' in C28.line(32) and "172.19.0.3/16" in C28.line(35)
assert '"processor"' in C28.line(39) and "172.19.0.2/16" in C28.line(42)
ERR25 = C25.join(5, 6)                              # one line the capture terminal wrapped at 80
assert ERR25.endswith("Could not connect to server"), ERR25

# ------------------------------------------------------------------ README phrases
TOY = "port_toy/README.md"


def readme_has(n: int, phrase: str) -> str:
    assert phrase in excerpt(TOY, n, n).replace("`", ""), (n, phrase)
    return phrase


PH230 = readme_has(230, "The host port comes first")
PH239 = readme_has(239, "-p 8090:9100")
PH262 = readme_has(262, "nothing else is using port 9200")
PH290 = readme_has(290, "localhost means the gateway")
assert "processor image does not need it" in excerpt(TOY, 294, 294)
assert excerpt(TOY, 204, 206).split("\n") == EXP.at(2, 3, 4)
PONDER_Q = "Same command,\nbut localhost instead of processor.\nWhat answers?"
PONDER_ROWS = ["docker exec gateway curl --max-time 3 \\", "    http://localhost:9200/health"]
assert " ".join(r.strip(" \\") for r in PONDER_ROWS) == C25.cmd

# ------------------------------------------------------------------ layout
TOP = 2.86                     # top of anything under the tracker (its bottom is 2.905)
BAND_Y = 3.2                   # the top band, right of the tracker
BAND_R = 6.5
T6_TOP = strip_top(6)          # -0.23
K_NET = 0.95                   # ToyNet's vertical squash
CW = cell_width(TERM_PT)


# ------------------------------------------------------------------ helpers
def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def band(m, right: float = BAND_R):
    """Right-aligned in the top band (beside the tracker)."""
    return m.move_to([0, BAND_Y, 0]).align_to([right, 0, 0], RIGHT)


def row_tag(t, line, mob, buff: float = 0.3):
    """Position `mob` right after the text of the first row of `line` (a folded command's rows)
    that leaves room for it inside the terminal; None when none does."""
    rows = line.rows if hasattr(line, "rows") else [line]
    for row in rows:
        end = row.glyphs.get_right()[0] if len(row.glyphs) else row.strut.get_left()[0]
        if end + buff + mob.width < t.box.get_right()[0] - 0.12:
            mob.next_to(row.glyphs if len(row.glyphs) else row.strut, RIGHT, buff=buff)
            mob.set_y(row.strut.get_center()[1])
            mob.row = row
            return mob
    return None


def type_extra(scene, t, cmd: str, type_time: float | None = None):
    """Type an extra command (not in the README) and pin a GREY `extra` tag beside it."""
    ln = type_cmd(scene, t, cmd, type_time=type_time)
    tg = row_tag(t, ln, extra_tag())
    assert tg is not None, cmd
    pin(scene, tg.row, tg, run_time=0.25)
    return ln


def soft_scroll(t):
    """Scroll this terminal as resize() drops lines: when two or more rows must leave, they fade
    where they are first, then the rest slide up. (Terminal's own scroll slides the leaving rows
    up by the whole overflow while they fade: above the 6-row strip they would cross the picture.)
    One row still scrolls the house way (it only rises into the title bar)."""
    house = t._make_room

    def make_room(scene, n_new: int, run_time: float = 0.35) -> None:
        overflow = len(t.lines) + n_new - t.rows
        if overflow <= 1:
            house(scene, n_new, run_time)
            return
        gone = VGroup(*t.lines.submobjects[:overflow])
        stay = VGroup(*t.lines.submobjects[overflow:])
        scene.play(FadeOut(gone), run_time=0.15)
        for m in gone:
            t.lines.remove(m)
            scene.remove(m)
        if len(stay):
            scene.play(stay.animate.shift(UP * t.pitch * overflow), run_time=0.25)

    t._make_room = make_room
    return t


def unit(m):
    """Mark a mobject to keep its shape when the ToyNet is squashed (as S11)."""
    m.squash_unit = True
    return m


def squash(net: ToyNet, k: float):
    """Shrink a ToyNet vertically by k about its centre: frames, lines and gaps shrink, every text,
    tag and glyph (door, loop, browser, arrow tip, chip) keeps its size and shape (S11's helper)."""
    for b in net.boxes.values():
        unit(b.loop)
    unit(net.laptop_loop[0])
    unit(net.browser)
    for d in list(net.doors.values()) + list(net.rooms.values()):
        unit(d.frame)
    unit(net.parts["map"][1])
    unit(net.aim_chip)
    unit(net.parts["laptop_label"])
    for m in net.parts["outside"][:2]:
        unit(m)
    units = []

    def walk(m):
        if getattr(m, "squash_unit", False) or getattr(m, "keep_size", False) or \
                isinstance(m, Text) or hasattr(m, "pt"):
            units.append(m)
            return
        for s in m.submobjects:
            walk(s)

    for s in net.submobjects:
        walk(s)
    c = net.get_center()
    net.stretch(k, 1, about_point=c)
    for u in units:
        u.stretch(1 / k, 1)
    return net


def build_net() -> ToyNet:
    net = ToyNet(show=("outline", "laptop_label", "zone", "boxes", "rail", "rail_label", "plug_gateway",
                       "plug_processor", "book", "door", "room_gateway", "room_processor", "map"))
    squash(net, K_NET)
    outline = net.parts["outline"]
    net.shift([0, T6_TOP + 0.1 - outline.get_bottom()[1], 0])
    assert net.parts["laptop_label"].get_top()[1] <= TOP + 0.005, net.parts["laptop_label"].get_top()[1]
    assert net.get_left()[0] >= -6.58 and net.get_right()[0] <= 6.58
    return net


def ghost_box(net: ToyNet, dashed: bool = True) -> VGroup:
    """The extra container `gateway-all` between the two boxes: a TEAL box (dashed while it only
    exists, solid once it runs and is plugged into the rail) with its own room :9100.
    .frame .room .name .plug (None when dashed)"""
    g_fr = net.boxes["gateway"].frame
    x0 = g_fr.get_right()[0] + 0.32
    x1 = net.rooms["processor"].frame.get_left()[0] - 0.3
    h = 0.66
    top = g_fr.get_top()[1] - 0.1
    fr = box(x1 - x0, h, CTR, fill_opacity=0.07, dashed=dashed)
    fr.move_to([(x0 + x1) / 2, top - h / 2, 0])
    rd = door(0.3, 0.46, CTR).move_to([x0, fr.get_center()[1], 0])
    rl = mono(":9100", CAPTION, CTR).next_to(rd, RIGHT, buff=0.08)
    nm = mono("gateway-all", CAPTION, CTR).next_to(rl, RIGHT, buff=0.22)
    assert nm.get_right()[0] < x1 - 0.08, (nm.get_right()[0], x1)
    g = VGroup(fr, rd, rl, nm)
    g.frame, g.room, g.name, g.plug = fr, VGroup(rd, rl), nm, None
    if not dashed:
        px = x0 + 0.62
        g.plug = Line([px, fr.get_bottom()[1], 0], [px, net.rail.get_center()[1], 0], color=CTR, stroke_width=5)
        g.add_to_back(g.plug)
    return _keep(g)


def request_arrow(net: ToyNet, ghost: VGroup) -> VGroup:
    """gateway-all asks for street door 8090: a dashed PINK arrow from its box, up to the lane
    above the gateway box and left to the laptop's wall, ending right above the door's column
    (the door itself sits under the -p route). .line .tip .end"""
    g_fr = net.boxes["gateway"].frame
    lane = (g_fr.get_top()[1] + net.parts["outline"].get_top()[1]) / 2
    x0 = ghost.frame.get_left()[0] + 0.3
    x_end = net.wall.get_center()[0] + 0.1
    path = VMobject(stroke_color=LOOKUP, stroke_width=4)
    path.set_points_as_corners([[x0, ghost.frame.get_top()[1] + 0.02, 0], [x0, lane, 0], [x_end + 0.16, lane, 0]])
    dashed = DashedVMobject(path, num_dashes=26, dashed_ratio=0.6)
    end = np.array([x_end, lane, 0])
    tip = Polygon(end, end + np.array([0.2, 0.1, 0]), end + np.array([0.2, -0.1, 0]),
                  stroke_width=0).set_fill(LOOKUP, 1)
    g = VGroup(dashed, tip)
    g.line, g.tip, g.end = dashed, tip, end
    return g


def flash_path(mob, color: str = TURN, width: float = 8):
    return ShowPassingFlash(mob.copy().set_stroke(color, width), time_width=0.5)


def fold_chip(rows) -> VGroup:
    """A command shown, not typed, folded on rows as a shell command (GREY mono chip). .rows"""
    lines = VGroup(*[mono_line(r, CAPTION, INK) for r in rows])
    for i, ln in enumerate(lines):
        ln.shift(np.array([0, -i * 0.36, 0]) - ln.strut.get_corner(UP + LEFT))
    fr = box(lines.width + 0.5, lines.height + 0.32, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    fr.move_to(lines)
    g = VGroup(fr, lines)
    g.frame, g.rows = fr, lines
    return _keep(g)


def frame_ring(mob, color: str = TURN, pad: float = 0.05):
    from common import ring
    return ring(mob, color, buff=pad, stroke=3)


def fade_to(m, k: float | None, attr: str = "_lop"):
    """Transform: every member of m to k of its full opacity (k=None: back to full). Unlike
    set_opacity it leaves an arc's empty fill empty."""
    if k is not None and getattr(m, "_lop_saved", False) is False:
        _save_op(m, attr)
        m._lop_saved = True
    target = m.copy()
    _set_op(target, k, attr)
    return Transform(m, target)


def other_machine_dot(route) -> tuple:
    """A GREY dot that travels the outside machines' dashed route to the second door."""
    dashes = list(route.submobjects)
    path = VMobject().set_points_as_corners([d.get_start() for d in dashes] + [dashes[-1].get_end()])
    d = Dot(path.get_start(), radius=0.07, color=S.GREY)
    return d, MoveAlongPath(d, path, rate_func=linear)


def show_part(net: ToyNet, name: str):
    """Mark a hidden ToyNet part shown (its opacities restored) before it is drawn by a transform
    (as ToyNet.open_room does)."""
    m = net.parts[name]
    _set_op(m)
    net._flag(m, False)
    return m


class WhoCanReach(VoiceScene):
    def construct(self):
        # ============================================================ 0 · docker ps: mapping vs empty
        tr = tracker("P2", 1)
        t = soft_scroll(term(P_TOY, rows=12))
        ch230 = band(readme_chip("README.md · line 230", PH230))
        assert ch230.get_left()[0] > tr.get_right()[0] + 0.12

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Docker ps shows")
            type_cmd(self, t, C16.cmd)
            ps = t.print(self, C16.at(2, 3, 4), wrap=True, run_time=0.6)
            hd_b, gw_b, pr_b = ps[1], ps[3], ps[5]
            assert gw_b.text.find(GW_MAP) == 20 and hd_b.text.find("PORTS") == 20, gw_b.text
            gw_map = substring(gw_b, GW_MAP)
            vo.wait_until("the gateway's mapping")
            self.play(gw_map.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("host side first")
            self.play(FadeIn(ch230, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("127.0.0.1, port 8090")
            self.play(flash(substring(gw_b, "127.0.0.1"), TURN, 1.2), run_time=0.6)
            vo.wait_until("port 8090, to")
            self.play(flash(substring(gw_b, "8090"), TURN, 1.3), run_time=0.6)
            vo.wait_until("to 9100")
            self.play(flash(substring(gw_b, "9100"), TURN, 1.3), run_time=0.6)
            vo.wait_until("The processor's PORTS column")
            pbox = col_box(pr_b, 20, 20 + len(GW_MAP), TURN, dashed=True)
            pin(self, pr_b, pbox, anim=Create(pbox), run_time=0.5)
            self.play(flash(substring(hd_b, "PORTS"), TURN, 1.15), run_time=0.6)
            vo.wait_until("listening, but not published")
            ltag = grey_tag("listening ≠ published")
            ltag.move_to([pbox.get_center()[0], pr_b.strut.get_center()[1] - t.pitch - 0.02, 0])
            self.play(FadeIn(ltag, shift=UP * 0.1), run_time=0.5)

        # ============================================================ 1 · the README's three columns
        with self.voiceover(SAY[1], pad=1.4) as vo:     # the matched rows stay a moment
            self.play(FadeOut(ch230), FadeOut(ltag), caption_extra(tr, True), run_time=0.35)
            resize(self, t, 6, keep=[], run_time=0.5)
            type_extra(self, t, C17.cmd, type_time=1.3)
            out17 = t.print(self, C17.at(2, 3, 4), run_time=0.4)
            exp = log_panel(EXP.at(2, 3, 4), "README.md · lines 204–206", width=0.5 + 54 * CW, size=TERM_PT)
            text_left = t._slot(0)[0]
            exp.shift([text_left - exp.rows[0].strut.get_left()[0], T6_TOP + 0.5 - exp.frame.get_bottom()[1], 0])
            etag = expected_tag().next_to(exp.header, RIGHT, buff=0.3)
            eqs = VGroup(*[mono("=", TERM_PT, VENV).move_to([exp.frame.get_right()[0] + 0.4, r.strut.get_center()[1], 0])
                           for r in exp.rows])
            self.play(FadeIn(exp, shift=DOWN * 0.1), FadeIn(etag), run_time=0.45)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(e, scale=1.4), flash(o, VENV, 1.03))
                                    for e, o in zip(eqs, out17)], lag_ratio=0.35), run_time=1.0)

        # ============================================================ 2 · 127.0.0.1 left out: door 8090 is taken
        net = build_net()
        d1, d2 = net.doors["door"], net.doors["door2"]
        d1_ip = VGroup(*d1.label.submobjects[:9])           # "127.0.0.1" of "127.0.0.1:8090"
        ghost = ghost_box(net, dashed=True)
        req = request_arrow(net, ghost)
        xcross = cross_mark(0.16, ERR).move_to(req.end + LEFT * 0.04)     # fits the lane under the outline
        g_fr = net.boxes["gateway"].frame
        cap = note("host doors collide\nrooms never do")
        mid_x = (g_fr.get_right()[0] + net.rooms["processor"].frame.get_left()[0]) / 2
        cap.move_to([mid_x, (ghost.frame.get_bottom()[1] + net.parts["book"].get_top()[1]) / 2, 0])
        ch239 = band(readme_chip("README.md · line 239", PH239))
        map_line = net.parts["map"][0]

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(exp), FadeOut(etag), FadeOut(eqs), FadeIn(net), run_time=0.8)
            self.play(d1_ip.animate.set_color(TURN), flash(d1.frame, TURN, 1.2), run_time=0.7)
            vo.wait_until("This extra run leaves it out")
            self.play(FadeIn(ch239, shift=DOWN * 0.1), run_time=0.4)
            run18 = type_extra(self, t, C18.cmd, type_time=1.6)
            self.play(substring(run18.rows[1], "-p 8090:9100").animate.set_color(LOOKUP), run_time=0.3)
            t.print(self, [C18.line(2)], run_time=0.3)
            self.play(Create(ghost.frame), FadeIn(VGroup(ghost.room, ghost.name)), run_time=0.6)
            vo.wait_until("asking for door 8090 on every address")
            self.play(Create(req.line), run_time=0.7)
            self.play(FadeIn(req.tip, scale=0.5), flash(d1.label[9:], TURN, 1.2), run_time=0.4)
            vo.wait_until("Docker refuses")
            err = t.print(self, [C18.line(3)], wrap=True, run_time=0.5)
            assert err[3].text.endswith("Bind for 127.0.0.1:8090 failed: port is alrea"), err[3].text
            bind = VGroup(substring(err[3], "Bind for 127.0.0.1:8090 failed: port is alrea"),
                          substring(err[4], "dy allocated"))
            self.play(bind.animate.set_color(ERR), req.animate.set_color(ERR), Create(xcross),
                      flash(d1.frame, ERR, 1.25), run_time=0.8)
            vo.wait_until("our gateway holds 8090")
            self.play(flash_path(map_line, LOOKUP), flash(d1.label[10:], TURN, 1.25), run_time=0.9)
            self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("The container was still created")
            rm19 = type_extra(self, t, C19.cmd, type_time=0.7)
            o19 = t.print(self, [C19.line(2)], run_time=0.3)
            ctag = beside(grey_tag("created anyway · remove it"), t, o19[0])
            pin(self, o19[0], ctag, run_time=0.4)
            self.play(FadeOut(ghost), FadeOut(req), FadeOut(xcross), run_time=0.5)
        del rm19

        # ============================================================ 3 · door 8091 on every address
        ghost2 = ghost_box(net, dashed=False)
        ipv6 = band(grey_tag("yours may also list [::]:8091 (IPv6)"))
        assert ipv6.get_left()[0] > tr.get_right()[0] + 0.12
        outside = net.parts["outside"]

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(ch239), FadeOut(cap), d1_ip.animate.set_color(INK), run_time=0.4)
            run20 = type_extra(self, t, C20.cmd, type_time=1.4)
            self.play(substring(run20.rows[1], "-p 8091:9100").animate.set_color(LOOKUP), run_time=0.3)
            t.print(self, [C20.line(2)], run_time=0.3)
            self.play(Create(ghost2.frame), Create(ghost2.plug), FadeIn(VGroup(ghost2.room, ghost2.name)),
                      *net.parts_in("door2"), run_time=0.7)
            vo.wait_until("and the mapping shows 0.0.0.0")
            type_extra(self, t, PS_FMT, type_time=1.1)
            o21 = t.print(self, C21.at((2, 5)), run_time=0.4)
            zero = substring(o21[1], ZERO_MAP)
            self.play(zero.animate.set_color(TURN), flash(d2.label, TURN, 1.15), FadeIn(ipv6, shift=DOWN * 0.1),
                      run_time=0.7)
            vo.wait_until("every address")
            self.play(flash(d2.frame, TURN, 1.3), flash(substring(o21[1], "0.0.0.0"), TURN, 1.2), run_time=0.7)
            vo.wait_until("so other machines")
            self.play(*net.parts_in("outside"), run_time=0.6)
            visitor, walk = other_machine_dot(outside[2])
            self.add(visitor)
            self.play(walk, run_time=1.0)
            self.play(flash(d2.frame, TURN, 1.3), FadeOut(visitor), run_time=0.5)
            vo.wait_until("Remove it.")
            type_extra(self, t, RM_F, type_time=0.8)
            t.print(self, [C21.line(6)], run_time=0.3)
            self.play(FadeOut(ghost2), *net.parts_out("door2", "outside"), FadeOut(ipv6), run_time=0.6)
            vo.wait_until("That's why the README writes")
            self.play(d1_ip.animate.set_color(TURN), flash(d1.frame, TURN, 1.25), run_time=0.7)
            vo.wait_until("this laptop only")
            self.play(flash_path(map_line, TURN), flash(net.browser, TURN, 1.2), run_time=0.9)

        # ============================================================ 4 · from the laptop
        ch262 = band(readme_chip("README.md · line 262", PH262))
        assert ch262.get_left()[0] > tr.get_right()[0] + 0.12, ch262.get_left()[0]

        with self.voiceover(SAY[4]) as vo:
            self.play(tr.goto(2), d1_ip.animate.set_color(INK), run_time=0.5)
            t.clear(self)
            type_cmd(self, t, C22.cmd)
            self.play(flash_path(map_line, LOOKUP), flash(net.rooms["gateway"], CTR, 1.2), run_time=0.8)
            t.print(self, C22.at((2, 6)), run_time=0.5)             # a chunk at most as tall as the strip
            t.print(self, C22.at(7, "…", 154, 155), run_time=0.5)
            vo.wait_until("Curl on 9200")
            type_cmd(self, t, C23.cmd, type_time=1.4)
            t.print(self, [(C23.line(2), ERR)], run_time=0.3)
            bounce, (b1, b2) = net.bounce_from_laptop()
            self.play(b1)
            vo.wait_until("your laptop has no door to it")
            self.play(b2)
            vo.wait_until("unless something else of yours")
            self.play(FadeIn(ch262, shift=DOWN * 0.1), run_time=0.5)

        # ============================================================ 5 · from inside the gateway, by name
        room_p = net.rooms["processor"]
        with self.voiceover(SAY[5]) as vo:
            self.play(tr.goto(3), FadeOut(ch262), FadeOut(bounce), run_time=0.5)
            t.clear(self)
            ex24 = type_cmd(self, t, C24.cmd, type_time=1.7)
            vo.wait_until("asking for the name processor")
            pk = net.packet()
            self.play(substring(ex24.rows[1], "processor").animate.set_color(LOOKUP), FadeIn(pk, scale=0.6),
                      run_time=0.5)
            self.play(net.travel(pk, run_time=1.6))
            vo.wait_until("on port 9200")
            self.play(flash(room_p, CTR, 1.25), run_time=0.6)
            vo.wait_until("The answer: ok.")
            o24 = t.print(self, C24.at((2, 5)), run_time=0.4)
            mtag = grey_tag("curl's progress meter")
            mtag.move_to(o24[1].strut).align_to(o24[1].strut, LEFT).shift(RIGHT * 0.05)
            assert mtag.get_right()[0] < substring(o24[1], "Dload").get_left()[0] - 0.15
            pin(self, o24[1], mtag, run_time=0.3)
            self.play(o24[3].animate.set_color(VENV), FadeOut(pk), flash(room_p, VENV, 1.25), run_time=0.6)

        # ============================================================ 6 · ponder: localhost instead
        gw, pr = net.boxes["gateway"], net.boxes["processor"]
        qs = VGroup(*[mono("?", TERM_PT, S.GREY).next_to(b.loop_label, RIGHT, buff=0.1) for b in (gw, pr)])
        for q, b in zip(qs, (gw, pr)):
            assert q.get_right()[0] < b.frame.get_right()[0] - 0.03
        chip = fold_chip(PONDER_ROWS)
        q = ponder_card(PONDER_Q, width=5.55, size=22)
        q.move_to([6.5 - q.width / 2, -3.42 + q.height / 2, 0])
        chip.move_to([-6.5 + chip.width / 2, q.get_center()[1] + 0.3, 0])
        assert q.get_top()[1] < net.get_bottom()[1] - 0.15 and q.get_left()[0] > chip.get_right()[0] + 0.12
        lh = substring(chip.rows[1], "localhost")
        lh_ring = frame_ring(lh, TURN)
        dims = [gw.loop, gw.loop_label, pr.loop, pr.loop_label]

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(t), *[fade_to(m, 0.35) for m in dims], FadeIn(qs), run_time=0.7)
            vo.wait_until("The same command")
            self.play(FadeIn(chip, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("with localhost instead of processor")
            self.play(Create(lh_ring), lh.animate.set_color(TURN), run_time=0.6)
        self.play(FadeIn(q, scale=0.95), run_time=0.6)
        bar = q[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=6)

        # ============================================================ 7 · nothing: localhost is the gateway itself
        tick2 = VGroup(check_mark(0.28, TURN), note("puzzle 2", TURN)).arrange(RIGHT, buff=0.12)
        tick2.move_to([g_fr.get_right()[0] + 0.3 + tick2.width / 2, gw.loop.get_center()[1], 0])
        ch290 = band(readme_chip("README.md · line 290", PH290))
        assert ch290.get_left()[0] > tr.get_right()[0] + 0.12, ch290.get_left()[0]
        room_g = net.rooms["gateway"]
        gtick = check_mark(0.3, VENV).next_to(room_g, RIGHT, buff=0.2)
        loops3 = [net.laptop_loop, VGroup(gw.loop, gw.loop_label), VGroup(pr.loop, pr.loop_label)]

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(q), FadeOut(chip), FadeOut(lh_ring), FadeIn(t), run_time=0.5)
            type_cmd(self, t, C25.cmd, type_time=1.4)
            t.print(self, ["…", (ERR25, ERR)], wrap=True, run_time=0.4)
            vo.wait_until("Inside the gateway, localhost is")
            self.play(fade_to(gw.loop, None), fade_to(gw.loop_label, None), FadeOut(qs[0]), run_time=0.4)
            dot, loop_anims = net.loopback("gateway")
            self.add(dot)
            self.play(*loop_anims)
            vo.wait_until("and nothing there listens on 9200")
            xg = cross_mark(0.24, ERR).move_to(dot)
            self.play(dot.animate.set_color(ERR), Create(xg), run_time=0.5)
            vo.wait_until("That's the second puzzle")
            self.play(FadeIn(ch290, shift=DOWN * 0.1), FadeIn(tick2, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("each container has its own localhost")
            self.play(fade_to(pr.loop, None), fade_to(pr.loop_label, None), FadeOut(qs[1]), run_time=0.4)
            self.play(*[flash(m, TURN, 1.15) for m in loops3], run_time=0.9)
            vo.wait_until("An extra check")
            self.play(caption_extra(tr, True), FadeOut(xg), dot.animate.set_color(LOOKUP), run_time=0.4)
            type_extra(self, t, C26.cmd, type_time=1.4)
            t.print(self, C26.at((2, 5)), run_time=0.4)
            vo.wait_until("localhost returns the page")
            self.play(dot.animate.move_to(room_g.frame), run_time=0.6)
            self.play(flash(room_g, VENV, 1.3), Create(gtick), FadeOut(dot), run_time=0.7)

        # ============================================================ 8 · docker network inspect: the addresses
        book0, book1 = net.book_lines
        with self.voiceover(SAY[8]) as vo:
            self.play(flash(net.parts["book"], LOOKUP, 1.4), FadeOut(tick2), FadeOut(gtick), FadeOut(ch290),
                      net.unloop("gateway"), run_time=0.8)
            vo.wait_until("From the handy commands")
            tr = switch_section(self, tr, "PH", 5, run_time=0.6)
            self.play(FadeOut(net), run_time=0.4)        # first the picture goes, then the terminal grows
            resize(self, t, 13, keep=[], run_time=0.6)
            type_cmd(self, t, C28.cmd, type_time=1.0)
            ins = t.print(self, C28.at(4, "…", 16, "…", 32, "…", 35, "…", 39, "…", 42, "…"), run_time=0.6)
            l16, l32, l35, l39, l42 = ins[2], ins[4], ins[6], ins[8], ins[10]
            vo.wait_until("shows an address for each container")
            n_gw, a_gw = substring(l32, "gateway"), substring(l35, "172.19.0.3/16")
            n_pr, a_pr = substring(l39, "processor"), substring(l42, "172.19.0.2/16")
            self.play(*[m.animate.set_color(LOOKUP) for m in (n_gw, a_gw, n_pr, a_pr)], run_time=0.6)
            vo.wait_until("on toynet's own subnet")
            self.play(substring(l16, "172.19.0.0/16").animate.set_color(LOOKUP), run_time=0.5)
            resize(self, t, 6, keep=[l16, l32, l35, l39, l42], run_time=0.7)
            self.play(FadeIn(net), run_time=0.5)
            show_part(net, "book0")
            show_part(net, "book1")
            self.play(TransformFromCopy(VGroup(n_pr, substring(l42, "172.19.0.2")), book0),
                      TransformFromCopy(VGroup(n_gw, substring(l35, "172.19.0.3")), book1), run_time=1.1)

        # ============================================================ 9 · Docker's phone book at 127.0.0.11
        dns_g = net.parts["dns_gateway"]
        addr = band(note("addresses may change on restart · names stay"))
        assert addr.get_left()[0] > tr.get_right()[0] + 0.12
        with self.voiceover(SAY[9]) as vo:
            self.play(caption_extra(tr, True), run_time=0.3)
            t.clear(self)
            type_extra(self, t, RESOLV, type_time=1.4)
            o29 = t.print(self, C29.at("…", 6, "…"), run_time=0.4)
            vo.wait_until("Docker's built-in phone book")
            self.play(*net.parts_in("dns_processor", "dns_gateway", anim=Create), flash(net.parts["book"], LOOKUP, 1.3),
                      run_time=0.8)
            vo.wait_until("at 127.0.0.11")
            self.play(substring(o29[1], "127.0.0.11").animate.set_color(LOOKUP), flash(dns_g[1], LOOKUP, 1.2),
                      run_time=0.6)
            vo.wait_until("which turns names into")
            type_extra(self, t, GETENT, type_time=1.5)
            o29b = t.print(self, [(C29.line(13), LOOKUP), (C29.line(14), LOOKUP)], run_time=0.4)
            self.play(flash(book0, LOOKUP, 1.08), flash(book1, LOOKUP, 1.08), run_time=0.7)
            vo.wait_until("Addresses can change")
            self.play(FadeIn(addr, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("names stay")
            self.play(flash(VGroup(*book0[:9]), TURN, 1.15), flash(VGroup(*book1[:7]), TURN, 1.15),
                      run_time=0.7)
        del o29b

        # ============================================================ 10 · a shell inside; the processor has curl; your turn
        panel = log_panel([C27.line(2)], "x", width=12.6)
        panel.remove(panel.header)
        head = VGroup(mono(C27.cmd, CAPTION, S.GREY), extra_tag()).arrange(RIGHT, buff=0.3)
        panel.shift([0 - panel.frame.get_center()[0], 2.25 - panel.frame.get_top()[1], 0])
        head.next_to(panel.frame, UP, buff=0.1).align_to(panel.frame, LEFT).shift(RIGHT * 0.12)
        assert head.get_top()[1] <= TOP, head.get_top()[1]
        err_tag = erratum_tag("README.md line 294: the processor doesn't need curl · it has it anyway")
        err_tag.next_to(panel.frame, DOWN, buff=0.25).align_to(panel.frame, LEFT)
        card = turn_card([C16.cmd, C22.cmd, C23.cmd, C24.cmd, C25.cmd])
        card.shift([0 - card.frame.get_center()[0], -3.45 - card.frame.get_bottom()[1], 0])
        assert card.get_top()[1] < err_tag.get_bottom()[1] - 0.15, (card.get_top()[1], err_tag.get_bottom()[1])

        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(addr), tr.goto(1), run_time=0.5)
            t.clear(self)
            type_cmd(self, t, C29B.cmd, type_time=1.0)
            self.play(*enter_container(t, "gateway", P_SH), flash(gw.frame, CTR, 1.04), run_time=0.6)
            sh = session(self, t, C29B, 2, 3)
            vo.wait_until("its hostname is the container ID")
            idtag = beside(grey_tag("= the gateway's container ID (docker ps)"), t, sh[3])
            pin(self, sh[3], idtag, run_time=0.4)
            session(self, t, C29B, 4, 5, 6)
            self.play(*leave_container(t, P_TOY), run_time=0.5)
            vo.wait_until("One aside")
            self.play(FadeOut(net), run_time=0.4)
            self.play(FadeIn(panel, shift=DOWN * 0.1), FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("has curl too")
            self.play(flash(substring(panel.rows[0], "curl 8.14.1"), TURN, 1.12), run_time=0.7)
            vo.wait_until("though the README implies")
            self.play(FadeIn(err_tag, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Pause, and test from both sides")
            self.play(FadeOut(t), run_time=0.35)          # the card takes the terminal's place
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.5)
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        self.wait(0.2)
