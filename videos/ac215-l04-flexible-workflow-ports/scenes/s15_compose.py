r"""S15 · Compose: the same app, declared (port_toy README › Step 4, steps 1, 2 and 5; V8, then V6).

Beats (script.md "## S15", one voiceover block each):
 0  TRACKER P4/1. V8 (ComposeMap) in two columns: on "Step 4" the left column's GREY chips (Step 1's
    five by-hand commands, folded at <= 36 characters) write in; on "The README shows an excerpt" the
    README chip `README.md · lines 432–446` "an excerpt" appears in the right column; on "open the
    whole docker-compose.yml" CODE(port_toy/docker-compose.yml: 11–25, comments cut) drops in above it
    (header `docker-compose.yml · lines 11–25 · comment cut`). On "Almost every flag" every flag of
    the chips flashes YELLOW in turn.
 1  The README chip goes. Each flag's copy lifts off its chip and flies to its YAML key, which gets a
    GREEN bar as it lands: on "Dash dash name" `--name gateway` -> `container_name: gateway` (13); on
    "and the build command" `docker build` and `./gateway` -> `build: ./gateway` (14); on "Dash p"
    `-p 127.0.0.1:8090:9100` -> the `ports:` value (15–16); on "dash e" the two `-e` flags ->
    `environment:` (19–21); on "and the network is named" `--network toynet` -> `networks: - toynet`
    (24–25), then the panel swaps to CODE(port_toy/docker-compose.yml: 27–39), `docker network create
    toynet` lands on `name: toynet` (37–39) and the processor's flags fly the same way (`--name`,
    `docker build ./processor`, `-e PORT=9200`, `--network`). Last, `-t toy-gateway`, `-t
    toy-processor`, both `-d` and the two image names stay behind, dimmed, with the GREY tag "no home:
    Compose names the image itself" under the panel.
 2  The tag goes; the panel swaps back to lines 11–25 and its GREEN bars return. On "the volumes key"
    `volumes:` / `- ./gateway:/app` (17–18) get a GREEN outline and the GREEN tag "live-mount the
    gateway's folder"; on "and the depends on key" `depends_on:` / `- processor` (22–23) get theirs
    and the tag "start the processor first" (the first tag gives way; both outlines stay). On "All of
    step 1 collapses" the left column's chips fold into one PURPLE chip `docker compose up`, which
    flashes on "docker compose up".
 3  The panel goes; the terminal (full width, 13 rows, `laptop`, student@laptop:~/AC215/port_toy$)
    rises and the PURPLE chip slides onto its first row, where `docker compose up` is typed ->
    port-laptop/47 lines 3, …, 21–24, …, 31, 39 (BuildKit rows, times as GREY tags). On "all from the
    cache" the CACHED rows turn GREEN; on "and names them after the folder and the service"
    `port_toy-processor` and `port_toy-gateway` are boxed YELLOW and the GREY tag "folder name +
    service name" sits under them; on "port toy, dash gateway" `port_toy` and `-gateway` flash.
 4  The terminal shrinks to 7 rows (the two naming rows stay) and V6 builds above it as the output
    continues: 47 line 43 `[+] up 5/5` YELLOW, then each `✔` row (time as a GREY tag) ticks its part
    of V6: the two images (TEAL boxes `port_toy-gateway`, `port_toy-processor` at the left), the
    `toynet` rail, the processor box, the gateway box (a white tick on each). On "and prints both
    banners" lines 49–51; on "each line prefixed with its service" the prefixes `processor  |` and
    `gateway    |` turn TEAL while each box flashes. The app keeps running (no prompt). On "Pause and
    run it" the static GREY your-turn card (`docker compose up`, ▶ your turn) under the images.
 5  V6 and the card go; the first terminal shrinks to the 3-row strip (still running). A compact
    PAGE(port-laptop/49) (address bar `localhost:8090`, reply card) drops in with the README chip
    `README.md · line 460` "Open http://localhost:8090" in the top band and REPLY(49: 2) under it; the
    address and the reply flash. On "In a second terminal" the page goes and a second terminal (`laptop
    · second terminal`, 7 rows) slides in above the strip: `student@laptop:~$`, the `~` flashes YELLOW
    with the GREY caption "new terminal: cd here first", "· Compose reads the file in the current
    folder" joins it on that clause, then the prompt reads student@laptop:~/AC215/port_toy$. On
    "There, docker compose ps" TRACKER P4/2, `docker compose ps` -> 48 lines 2–4 (wrap), the PORTS
    header and `127.0.0.1:8090->9100/tcp` boxed YELLOW.
 6  TRACKER P4/2 · extra: `docker network ls` (GREY `extra` tag) -> 50 lines 2–6, `toynet` TEAL with
    the GREY tag "created by Compose". On "and compose exec reaches the processor" TRACKER P4/2:
    `docker compose exec gateway curl http://processor:9200/health` (folded at a space with ` \`) ->
    51 line 2 `ok` GREEN with the GREY tag "no progress meter: compose exec gives curl a terminal",
    and the GREY caption "the README's table writes curl ...: this is step 2's command" above the
    terminal; on "ok" the `ok` flashes.
 7  The second terminal and the caption go. The README's comparison table (`README.md · lines
    478–484`) as a two-column card "By hand" | "With Compose", its five rows writing in. On "In the
    first terminal" the card goes, the first terminal grows back to 7 rows and 47 lines 52–54 appear
    under the banners: the page's two `POST` lines and the health check's `GET /health`, YELLOW.
 8  TRACKER P4/5 with the GREY caption "the README does this at the end of Step 4 · here: the
    foreground app" under the tracker. On "press Control C" the key caps Ctrl + C drop in and press
    -> 47 line 55 `Gracefully Stopping...` (it flashes on "Compose says it's stopping gracefully").
    On "but it takes about 20 seconds" a GREY stopwatch "≈ 20 s" sweeps a third of a turn in 3 s
    while lines 56–61 print, `gateway exited with code 137` and `processor exited with code 137` RED.
 9  The key caps, the stopwatch and the caption go; V6 (both TEAL boxes, the rail) returns above the
    terminal. On "Python, each container's first process" the GREY caption "Python = the first
    process"; on "ignores the polite stop signal" a GREY envelope "stop" reaches the gateway's wall,
    wiggles and fades (ignored). On "So Docker waits 10 seconds" a GREY 10 s clock in the gap sweeps;
    on "then kills it" a RED "kill" stamp lands on the gateway. Then the same for the processor
    (envelope, clock, stamp), and the RED chip "137 = 128 + 9: killed" between the boxes.
10  On "Exit code 137 means killed" both `137`s in the terminal and the chip flash. The prompt returns
    and on "Docker compose ps dash a" `docker compose ps -a` -> 52 lines 2–4 (wrap), both `Exited
    (137)` boxed YELLOW; on "both containers exited" the stamps, envelopes and chip go and V6's boxes
    turn GREY (they stay, the rail stays); they flash on "but they're still there".
11  `docker compose down` -> 53 lines 2–5: as each `✔ … Removed` row prints, its part of V6 dissolves
    (gateway box, processor box, the rail). On "and nothing is left in ps dash a" `docker compose ps
    -a` -> 54 line 2 (the header alone, flashed). On "Control C stops" the README chip `README.md ·
    line 519` "Ctrl+C … leaves them in place." under the tracker. On "Pause, and run the whole cycle"
    the static GREY your-turn card (`docker compose up` then Ctrl+C, `docker compose ps -a`, `docker
    compose down`, `docker compose ps -a`) at the right. Everything fades to an empty frame.

Deviations from SHOW (and why):
- Beat 0: the README chip sits under the code panel, not under its header: the 15 code rows fill the
  right column from the header down, and the chip (5.4 wide) would cover them.
- Beat 1: the processor's `-t toy-processor` / `-d` and both image names (the run commands' last
  word) are dimmed with the gateway's `-t` / `-d`: they have no home either, and leaving them bright
  would suggest they do. The tag sits under the panel (the left column is full).
- Beat 2: the GREEN bars of the gateway's flags return with the panel (swap() drops them), so the two
  outlined keys read as the only ones without a by-hand ancestor. The two tags share the slot under
  the panel (one at a time; both outlines stay), so no leader line crosses the other outline.
- Beat 4: V6 is the 7-row layout of beats 8–11 (no room above a 13-row terminal); the terminal shows
  the naming rows, then lines 43–51 scroll through it. The ✔ rows' images are two TEAL sealed boxes
  labelled with the image names at V6's left. The `▶ your turn` sits on a static card: the command
  has scrolled away by the time the SAY says "pause".
- Beat 5: the second terminal has 7 rows, not 10: above the 3-row strip there are 4.2 units, and the
  GREY caption of beat 6 needs a row above it. The README chip quotes the link text only ("Open
  http://localhost:8090"): the whole sentence is 9.4 wide, wider than the top band.
- Beat 7: the comparison card leaves when the first terminal grows (card + terminal don't fit
  together); its `rm -f` cell wraps onto two lines, as the README's cell joins two commands.
- Beats 8–11: the first terminal has 7 rows, not 6: lines 55–61 (7 lines) stay on screen together,
  and `docker compose ps -a` stays with its 6 wrapped rows. V6 is drawn at 0.92 (text at full size)
  so it fits above it.
- Beat 9: the clocks sit in the gap between the boxes (the gateway's at its left, the processor's at
  its right); the chip "137 = 128 + 9: killed" is RED (exit code 137 is RED in the terminal).
- Beat 11: the `▶ your turn` is on a static card (the cycle's first commands have scrolled away);
  V6's parts dissolve one per `Removed` row, the order of the output.

Critic pass (fixes, kept as rules for this file):
- Beat 1: each flag copy turns GREEN on its way and fades out as it reaches its YAML span (flight()),
  instead of landing on top of the YAML text; the processor's five flights are staggered (lag 0.18).
- Beat 3: the PURPLE chip stays in front while the terminal fades in (it vanished under the
  terminal's fill until bring_to_front), and the bare prompt shows before it slides onto the row,
  so it lands where the command is typed.
- Every scroll of more than one row goes through room(): the leaving lines fade in place, then the
  rest slide up (Terminal's own scroll slid fading lines out over V6 and the title bar).
- Beat 9: the "kill" stamp spans the box's whole port strip (a small stamp half-covered `65535`);
  the RED chip sits 0.12 higher so it clears the processor's envelope.
- Beat 10: the stopped boxes' port cells turn GREY with the frame and labels (stop_box leaves them
  TEAL), so the whole box reads as stopped.
"""

import numpy as np
from common import (
    CTR,
    ERR,
    INK,
    NARRATION,
    P_HOME,
    P_TOY,
    STRIP_TOP,
    TOOL,
    TURN,
    VENV,
    ComposeMap,
    PortPage,
    ReplyStrip,
    Stopwatch,
    ToyNet,
    _drop_bare,
    _header_text,
    _keep,
    _set_op,
    bare_prompt,
    beside,
    build_row,
    caption_extra,
    capture,
    check_mark,
    col_box,
    envelope,
    excerpt,
    extra_tag,
    grey_tag,
    keycaps,
    note,
    page_reply,
    pin,
    place_time,
    readme_chip,
    resize,
    sealed_box,
    source_text,
    stamp,
    strip_top,
    table_card,
    term,
    time_tag,
    tracker,
    turn_card,
    type_cmd,
)
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
    ManimColor,
    UpdateFromAlphaFunc,
    VGroup,
    Wiggle,
    interpolate_color,
    linear,
    smooth,
)

from explainer import style as S
from explainer.devops import (
    MONO,
    OUTPUT,
    box,
    cell_width,
    chip,
    glyph_range,
    mono,
    mono_line,
    substring,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S15"]
assert len(SAY) == 12, len(SAY)

# ------------------------------------------------------------------ captures (file line numbers)
PL = "port-laptop"
TOY = "port_toy/README.md"
C47, C48, C49, C50, C51, C52, C53, C54 = (capture(n, PL) for n in ("47", "48", "49", "50", "51", "52", "53",
                                                                     "54"))
UP_CMD = C47.cmd
assert UP_CMD == "docker compose up" == excerpt(TOY, 455, 455)
PS = C48.cmd
assert PS == "docker compose ps" and f"`{PS}`" in excerpt(TOY, 480, 480)
NET_LS = C50.cmd
assert NET_LS == "docker network ls"
EXEC = C51.cmd
assert EXEC == "docker compose exec gateway curl http://processor:9200/health"
assert "`docker compose exec gateway curl ...`" in excerpt(TOY, 481, 481)
assert "docker exec gateway curl http://processor:9200/health" == excerpt(TOY, 273, 273)   # step 2's
PS_A = C52.cmd
assert PS_A == "docker compose ps -a" == C54.cmd == excerpt(TOY, 524, 524)
DOWN_CMD = C53.cmd
assert DOWN_CMD == "docker compose down" == excerpt(TOY, 512, 512)
assert "This is an excerpt" in excerpt(TOY, 446, 446) and excerpt(TOY, 432, 432) == "```yaml"
assert "Open [http://localhost:8090](http://localhost:8090)" in excerpt(TOY, 460, 460)
assert excerpt(TOY, 519, 519) == "`Ctrl+C` stops the containers but leaves them in place."
assert "press `Ctrl+C`" in excerpt(TOY, 507, 507)
R49 = page_reply(C49, 2)
assert R49["upper"] == "HELLO FROM THE LAPTOP"

# docker compose up: the build view (beat 3), then the up rows (beat 4), the requests (7), Ctrl+C (8)
B_ROWS = C47.at(3, "…", (21, 24), "…", 31, 39)
assert all("CACHED" in C47.line(n) for n in (21, 22, 23, 24))
assert "port_toy-processor" in C47.line(31) and "port_toy-gateway" in C47.line(39)
assert C47.line(43) == "[+] up 5/5"
UP_ROWS = {44: "img_gateway", 45: "img_processor", 46: "rail", 47: "processor", 48: "gateway"}
for _n, _w in ((44, "Image port_toy-gateway"), (45, "Image port_toy-processor"), (46, "Network toynet"),
               (47, "Container processor"), (48, "Container gateway")):
    assert _w in C47.line(_n), (_n, C47.line(_n))
assert C47.line(50).startswith("processor  | ") and C47.line(51).startswith("gateway    | ")
assert '"POST / HTTP/1.1"' in C47.line(52) and '"POST / HTTP/1.1"' in C47.line(53)
assert '"GET /health HTTP/1.1"' in C47.line(54)
assert C47.line(55).startswith("Gracefully Stopping...")
assert C47.line(59) == "gateway exited with code 137" and C47.line(61) == "processor exited with code 137"
# docker compose ps (wrapped at 65): the PORTS column sits in each line's second row
PORTS_COL = C48.line(2).index("PORTS")
assert PORTS_COL == C48.line(3).index("127.0.0.1:8090->9100/tcp") and PORTS_COL >= 65
EXITED_COL = C52.line(3).index("Exited (137)")
assert EXITED_COL == C52.line(4).index("Exited (137)") and 65 <= EXITED_COL < 130 - 12
assert "toynet" in C50.line(6) and C51.line(2) == "ok"
DOWN_ROWS = {3: "gateway", 4: "processor", 5: "rail"}
for _n, _w in ((3, "Container gateway"), (4, "Container processor"), (5, "Network toynet")):
    assert _w in C53.line(_n) and "Removed" in C53.line(_n)
assert C54.line(2).split() == ["NAME", "IMAGE", "COMMAND", "SERVICE", "CREATED", "STATUS", "PORTS"]

# the README's comparison table (README.md lines 478–484)
assert excerpt(TOY, 478, 478).split("|")[1].strip() == "By hand"
assert excerpt(TOY, 478, 478).split("|")[2].strip() == "With Compose"
TABLE_SRC = [[c.strip() for c in excerpt(TOY, n, n).split("|")[1:3]] for n in range(480, 485)]
assert TABLE_SRC == [["`docker ps`", "`docker compose ps`"],
                     ["`docker exec gateway curl ...`", "`docker compose exec gateway curl ...`"],
                     ["`docker rm -f gateway processor` and `docker network rm toynet`", "`docker compose down`"],
                     ["`-p` on `docker run`", "`ports:` in YAML"],
                     ["`-e` on `docker run`", "`environment:` in YAML"]], TABLE_SRC
assert "docker-compose.yml" in source_text(TOY)

# V8 flights: (chip, flag, file line, YAML sub-string); bars: the lines that get a GREEN bar
G_FLAGS = [(4, "--name gateway"), (4, "--network toynet"), (4, "-p 127.0.0.1:8090:9100"),
           (4, "-e PROCESSOR_HOST=processor"), (4, "-e PROCESSOR_PORT=9200"), (2, "./gateway"),
           (3, "--name processor"), (3, "--network toynet"), (3, "-e PORT=9200"), (1, "./processor"),
           (0, "toynet")]
NO_HOME = [(2, "-t toy-gateway"), (4, "-d"), (4, "toy-gateway"), (1, "-t toy-processor"), (3, "-d"),
           (3, "toy-processor")]
GW_BARS = (13, 14, 15, 16, 19, 20, 21, 24, 25)

# ------------------------------------------------------------------ layout
TOP = 2.84                        # top of anything under the tracker (its bottom is 2.905)
X_L, X_R = -6.45, 6.45
T7 = strip_top(7)                 # 0.17: V6 sits on a 7-row terminal
BAND_Y = 3.2                      # the top band, right of the tracker (its right edge is -0.45)
T2_TOP = 2.36                     # the second terminal (7 rows) above the 3-row strip


# ------------------------------------------------------------------ small helpers
def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.shift(RIGHT * (cx - m.get_center()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.shift(UP * (cy - m.get_center()[1]))
    return m


def glyph_box(line, sub: str, color: str = TURN, pad: float = 0.04, occurrence: int = 0):
    """A box around the glyphs of `sub` in a mono line, as tall as the row (not added)."""
    g = substring(line, sub, occurrence)
    r = box(g.width + 2 * pad + 0.04, line.strut.height + 0.04, color, fill_opacity=0.0, radius=0.06,
            stroke=3)
    return r.move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def mixed(s: str, mono_parts=(), size: float = 20, color: str = S.GREY):
    """A one-line caption in the house serif whose `mono_parts` use the code font."""
    return _keep(S.text(s, size, color, t2f={p: MONO for p in mono_parts}))


def row_split(s: str, width: int):
    """A progress row -> (text, time | None): BuildKit's `=>` rows and Compose's `✔` rows lose
    their time field (it becomes a GREY tag at the row's end); other rows are cut at the row."""
    s = s.rstrip()
    if s.lstrip().startswith("✔"):
        head, _, tm = s.rpartition(" ")
        assert tm.endswith("s") and tm[:-1].replace(".", "").isdigit(), s
        txt = head.rstrip()
        return (txt if len(txt) <= width else txt[:width - 1] + "…"), tm
    if s.lstrip().startswith("=>"):
        return build_row(s, width)
    return (s if len(s) <= width + 7 else s[:width + 6] + "…"), None


def n_rows(t, lines, wrap: bool = False) -> int:
    """The rows Terminal.print will use for `lines` (str or (str, colour))."""
    n = 0
    for x in lines:
        s = x if isinstance(x, str) else x[0]
        n += max(1, -(-len(s) // t.max_chars)) if wrap else 1
    return n


def room(scene, t, n_new: int, run_time: float = 0.4) -> None:
    """Make room for `n_new` rows when more than one row must go: the leaving lines fade where they
    are, then the rest slide up (Terminal's own scroll slides them out over the picture above the
    terminal). A one-row scroll is left to the terminal."""
    overflow = len(t.lines) + n_new - t.rows
    if overflow <= 1:
        return
    gone = VGroup(*t.lines.submobjects[:overflow])
    stay = VGroup(*t.lines.submobjects[overflow:])
    scene.play(FadeOut(gone), run_time=run_time * 0.45)
    for m in gone.submobjects:
        t.lines.remove(m)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * overflow), run_time=run_time * 0.55)


def out_rows(scene, t, rows: list, run_time: float = 0.5, lag: float = 0.12, extra=(),
             scroll_time: float = 0.25) -> VGroup:
    """Print rows (capture lines, "…", or (line, colour)); a progress row's time becomes a GREY
    time tag at the row's right end, part of the row (.time_tag). `extra` animations play with the
    rows. Returns the new lines."""
    items = []
    for r in rows:
        s, col = (r, OUTPUT) if isinstance(r, str) else r
        txt, tm = ("…", None) if s == "…" else row_split(s, t.max_chars - 7)
        items.append((txt, col, tm))
    room(scene, t, len(items))
    t._make_room(scene, len(items), run_time=scroll_time)
    new = VGroup()
    for txt, col, tm in items:
        ln = mono_line(txt, t.size, col)
        t._place(ln, len(t.lines))
        ln.time_tag = None
        if tm:
            tg = time_tag(tm)
            place_time(tg, t, ln)
            ln.add(tg)
            ln.time_tag = tg
        t.lines.add(ln)
        new.add(ln)
    scene.play(LaggedStart(*[FadeIn(m) for m in new], lag_ratio=lag), *extra, run_time=run_time)
    return new


def type_extra(scene, t, cmd: str, type_time: float | None = None):
    """Type an extra command (not in the README) with a GREY `extra` tag pinned beside it."""
    ln = type_cmd(scene, t, cmd, type_time=type_time)
    tg = beside(extra_tag(), t, ln, buff=0.4)
    pin(scene, ln, tg, run_time=0.25)
    return ln


def tag_after(t, line, mob, buff: float = 0.4):
    """`mob` beside a terminal row's text (pin it to scroll with the row)."""
    return beside(mob, t, line, buff=buff)


def show_member(mob, run_time: float = 0.35):
    """Fade in a hidden member of a set piece (one box of ToyNet's 'boxes' part)."""
    _set_op(mob)
    return FadeIn(mob, run_time=run_time)


def v6(show) -> ToyNet:
    """V6 for this scene: ToyNet at 0.92 (text at full size), its rail label just above a 7-row
    terminal, the processor box at the right edge; the laptop zone left of the gateway is free."""
    net = ToyNet(show=show)
    net.rescale(0.92)
    dx = X_R - 0.05 - net.boxes["processor"].frame.get_right()[0]
    dy = (T7 + 0.12) - net.parts["rail_label"].get_bottom()[1]
    net.shift([dx, dy, 0])
    assert net.boxes["gateway"].frame.get_top()[1] < TOP - 0.05, net.boxes["gateway"].frame.get_top()[1]
    return net


def image_row(name: str) -> VGroup:
    """A built image in V6's laptop zone: a TEAL sealed box and its name. .box .text"""
    sb = sealed_box(0.5, CTR)
    t = mono(name, 20, CTR).next_to(sb, RIGHT, buff=0.15)
    g = VGroup(sb, t)
    g.box, g.text = sb, t
    return g


def tick(at) -> VGroup:
    """A white tick (a ✔ row done) centred on a point."""
    return check_mark(0.28, INK, 5).move_to(at)


def kill_stamp(b) -> VGroup:
    """The RED "kill" stamp of a ToyNet box, as wide as its port strip so it covers the whole strip
    (a small stamp left "1 ▯▯▯ …35" showing, a broken number)."""
    k = stamp("kill", angle=0)
    k.frame.stretch_to_fit_width(b.strip.width + 0.12).set_fill(S.BG, 1)
    k.text.move_to(k.frame)
    return k.rotate(0.05).move_to(b.strip)


def flight(cp, tgt) -> UpdateFromAlphaFunc:
    """A flag copy flies to `tgt` (a YAML span) in one piece, turning GREEN on the way and fading
    out as it arrives, so it never sits on top of the YAML text (a glyph morph read as scrambled
    shapes mid-flight)."""
    start, end = cp.get_center().copy(), tgt.get_center().copy()

    def step(m, a):
        m.move_to(start + (end - start) * smooth(a))
        m.set_color(interpolate_color(ManimColor(INK), ManimColor(VENV), min(1.0, a / 0.5)))
        m.set_opacity(1.0 if a < 0.55 else max(0.0, 1.0 - (a - 0.55) / 0.35))

    return UpdateFromAlphaFunc(cp, step, rate_func=linear)


def fly(scene, cm: ComposeMap, flights, bars, run_time: float = 1.1, extra=(), lag: float = 0.0) -> VGroup:
    """Copies of flags lift off their chips and fly to their YAML spans (flight(): GREEN on the
    way, gone as they land), then the lines in `bars` get a GREEN bar each. flights: [(chip, flag,
    file line, YAML sub)]; lag > 0 staggers the flights. Leaves no copy or wrapper group in the
    scene; returns the bars, scene-owned and drawn above the panel (cm.bars would sit under a
    panel that swap() re-added)."""
    copies, moves = [], []
    for i, sub, line, sub_yaml in flights:
        cp = cm.flag(i, sub).copy()
        copies.append(cp)
        moves.append(flight(cp, cm.panel.span(line, sub_yaml)))
    if lag and len(moves) > 1:
        lg = LaggedStart(*moves, lag_ratio=lag)
        scene.play(lg, *extra, run_time=run_time * 0.8 * (1 + lag * (len(moves) - 1)))
        scene.remove(lg.group)
    else:
        scene.play(*moves, *extra, run_time=run_time * 0.8)
    scene.remove(*copies)
    new_bars = VGroup(*[cm.panel.bar(n, VENV, 0.22) for n in bars])
    scene.play(FadeIn(new_bars), run_time=run_time * 0.25)
    return new_bars


def mixed_cell(s: str, mono_parts) -> VGroup:
    return mixed(s, mono_parts, 20, INK)


def compare_card() -> VGroup:
    """README.md lines 478–484 as a two-column card; mixed cells keep the README's code spans in
    the code font, the rm -f cell on two lines. .cells .frame .heads"""
    rows = [["`docker ps`", "`docker compose ps`"],
            ["`docker exec gateway curl ...`", "`docker compose exec gateway curl ...`"],
            [VGroup(mono("docker rm -f gateway processor", 20, INK),
                    mixed_cell("and docker network rm toynet", ["docker network rm toynet"]))
             .arrange(DOWN, aligned_edge=LEFT, buff=0.1), "`docker compose down`"],
            [mixed_cell("-p on docker run", ["-p", "docker run"]), mixed_cell("ports: in YAML", ["ports:"])],
            [mixed_cell("-e on docker run", ["-e", "docker run"]),
             mixed_cell("environment: in YAML", ["environment:"])]]
    return table_card(["By hand", "With Compose"], rows, buff=0.14)


class ComposeUp(VoiceScene):
    def construct(self):
        # ============================================================ 0 · the file, beside Step 1
        tr = tracker("P4", 1)
        cm = ComposeMap()
        rc432 = readme_chip("README.md · lines 432–446", "an excerpt")
        bg = cm.panel.code.background
        place(rc432, cx=bg.get_center()[0], top=cm.panel.get_bottom()[1] - 0.22)
        nohome = grey_tag("no home: Compose names the image itself")
        place(nohome, cx=bg.get_center()[0], top=cm.panel.get_bottom()[1] - 0.22)
        assert rc432.get_bottom()[1] > -3.6 and nohome.get_right()[0] < 6.6
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1),
                      LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cm.chips], lag_ratio=0.18),
                      run_time=1.4)
            vo.wait_until("The README shows an excerpt")
            self.play(FadeIn(rc432, shift=UP * 0.1), run_time=0.5)
            self.play(flash(rc432.phrase, TURN, 1.08), run_time=0.6)
            vo.wait_until("open the whole docker-compose.yml")
            self.play(FadeIn(cm.panel, shift=DOWN * 0.2), run_time=0.8)
            self.remove(*cm.chips, cm.panel)
            self.add(cm)
            vo.wait_until("Almost every flag")
            self.play(LaggedStart(*[flash(cm.flag(i, s), TURN, 1.1, 0.6) for i, s in G_FLAGS], lag_ratio=0.15),
                      run_time=2.0)

        # ============================================================ 1 · each flag finds its key
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(rc432), run_time=0.3)
            gb = [fly(self, cm, [(4, "--name gateway", 13, "container_name: gateway")], [13])]
            vo.wait_until("and the build command becomes build")
            gb.append(fly(self, cm, [(2, "docker build", 14, "build:"), (2, "./gateway", 14, "./gateway")], [14]))
            vo.wait_until("Dash p becomes ports")
            gb.append(fly(self, cm, [(4, "-p 127.0.0.1:8090:9100", 16, '"127.0.0.1:8090:9100"')], [15, 16]))
            vo.wait_until("dash e becomes environment")
            gb.append(fly(self, cm, [(4, "-e PROCESSOR_HOST=processor", 20, "PROCESSOR_HOST: processor"),
                                     (4, "-e PROCESSOR_PORT=9200", 21, 'PROCESSOR_PORT: "9200"')], [19, 20, 21]))
            vo.wait_until("and the network is named")
            gb.append(fly(self, cm, [(4, "--network toynet", 25, "- toynet")], [24, 25], run_time=0.9))
            self.play(*cm.swap("processor", run_time=0.6), FadeOut(VGroup(*gb), run_time=0.3))
            pb = [fly(self, cm, [(0, "toynet", 39, "toynet")], [37, 38, 39],
                      extra=[flash(cm.flag(0, "docker network create"), VENV, 1.06)])]
            pb.append(fly(self, cm, [(3, "--name processor", 28, "container_name: processor"),
                                     (1, "docker build", 29, "build:"), (1, "./processor", 29, "./processor"),
                                     (3, "-e PORT=9200", 31, 'PORT: "9200"'),
                                     (3, "--network toynet", 33, "- toynet")], [28, 29, 30, 31, 32, 33],
                      lag=0.18))
            self.play(*[cm.dim_flag(i, s, 0.3) for i, s in NO_HOME], FadeIn(nohome, shift=UP * 0.1),
                      run_time=0.6)

        # ============================================================ 2 · two new keys; one command
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(*pb), run_time=0.3), *cm.swap("gateway", run_time=0.8), run_time=0.8)
            gbars = VGroup(*[cm.panel.bar(n, VENV, 0.22) for n in GW_BARS])
            self.play(FadeIn(gbars), run_time=0.4)
            vo.wait_until("the volumes key mounts")
            o1 = cm.outline(17, 18, "live-mount the gateway's folder")
            self.play(FadeOut(nohome, run_time=0.3), run_time=0.3)
            self.play(Create(o1.frame), Create(o1.line), FadeIn(o1.tag, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("and the depends on key")
            o2 = cm.outline(22, 23, "start the processor first")
            self.play(FadeOut(VGroup(o1.tag, o1.line)), Create(o2.frame), Create(o2.line),
                      FadeIn(o2.tag, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("All of step 1 collapses")
            up_chip, anims = cm.collapse()
            self.play(*anims)
            vo.wait_until("docker compose up")
            self.play(flash(up_chip, TOOL, 1.12, 0.8))

        # ============================================================ 3 · compose up: the build view
        t = term(P_TOY, rows=13, title="laptop")
        x_txt = t._slot(0)[0] + (len(P_TOY) + 1) * cell_width(t.size)     # where the command is typed
        probe = mono_line("x", t.size)
        row0_y = t._slot(0)[1] - probe.strut.height / 2
        with self.voiceover(SAY[3]) as vo:
            cm.remove(up_chip)
            self.add_foreground_mobject(up_chip)    # the terminal fades in under it, not over it
            self.play(FadeOut(VGroup(cm.panel, gbars, o1.frame, o2.frame, o2.tag, o2.line)), FadeIn(t),
                      run_time=0.6)
            assert not len(cm.chips) and not len(cm.bars)
            bare_prompt(self, t)                    # the chip lands after the waiting prompt
            self.play(up_chip.animate.shift([x_txt - up_chip.text.get_left()[0],
                                             row0_y - up_chip.text.get_center()[1], 0]), run_time=0.5)
            self.play(FadeOut(up_chip), run_time=0.2)
            type_cmd(self, t, UP_CMD, type_time=0.6)
            vo.wait_until("Compose builds both images")
            b = out_rows(self, t, B_ROWS, run_time=0.8)
            cached, n_proc, n_gw = VGroup(*b[2:6]), b[7], b[8]
            vo.wait_until("all from the cache")
            self.play(*[r.glyphs.animate.set_color(VENV) for r in cached], run_time=0.5)
            self.play(LaggedStart(*[flash(substring(r, "CACHED"), VENV, 1.15, 0.5) for r in cached],
                                  lag_ratio=0.15), run_time=0.8)
            vo.wait_until("and names them after the folder and the service")
            bx_p = glyph_box(n_proc, "port_toy-processor")
            bx_g = glyph_box(n_gw, "port_toy-gateway")
            fs = grey_tag("folder name + service name")
            fs.move_to([bx_g.get_center()[0], t._slot(len(t.lines))[1] - probe.strut.height / 2, 0])
            self.play(Create(bx_p), Create(bx_g), run_time=0.5)
            self.play(FadeIn(fs, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("port toy, dash gateway")
            self.play(flash(substring(n_gw, "port_toy"), TURN, 1.15, 0.6))
            self.play(flash(substring(n_gw, "-gateway"), TURN, 1.15, 0.6))

        # ============================================================ 4 · up 5/5: V6 builds; the banners
        net = v6(show=())
        gf, pf = net.boxes["gateway"].frame, net.boxes["processor"].frame
        zone_r = gf.get_left()[0] - 0.3
        img_g, img_p = image_row("port_toy-gateway"), image_row("port_toy-processor")
        place(img_g, left=X_L + 0.05, cy=TOP - 0.38)
        place(img_p, left=X_L + 0.05, cy=TOP - 0.92)
        assert img_p.get_right()[0] < zone_r, (img_p.get_right()[0], zone_r)
        card4 = turn_card([UP_CMD], header=None)
        place(card4, left=X_L + 0.05)
        card4.shift(UP * (img_p.get_bottom()[1] - 0.42 - card4.frame.get_top()[1]))
        assert card4.frame.get_bottom()[1] > T7 + 0.1 and card4.get_right()[0] < zone_r
        rail = net.rail
        ticks = {"img_gateway": tick(img_g.box.get_center()), "img_processor": tick(img_p.box.get_center()),
                 "rail": tick([(gf.get_right()[0] + pf.get_left()[0]) / 2, rail.get_start()[1] + 0.26, 0]),
                 "processor": tick(pf.get_corner(UP + RIGHT) + np.array([-0.3, -0.28, 0])),
                 "gateway": tick(gf.get_corner(UP + RIGHT) + np.array([-0.3, -0.28, 0]))}
        reveal = {"img_gateway": lambda: [FadeIn(img_g)], "img_processor": lambda: [FadeIn(img_p)],
                  "rail": lambda: net.parts_in("rail", "rail_label"),
                  "processor": lambda: [show_member(net.boxes["processor"]), *net.parts_in("plug_processor")],
                  "gateway": lambda: [show_member(net.boxes["gateway"]), *net.parts_in("plug_gateway")]}
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(bx_p, bx_g, fs)), run_time=0.3)
            resize(self, t, 7, keep=2, run_time=0.5)
            self.add(net)
            out_rows(self, t, [(C47.line(43), TURN)], run_time=0.3)
            for n, key in UP_ROWS.items():
                out_rows(self, t, [C47.line(n)], run_time=0.4,
                         extra=[*reveal[key](), FadeIn(ticks[key], scale=1.4)], scroll_time=0.2)
            net._flag(net.parts["boxes"], False)
            vo.wait_until("and prints both banners")
            ban = out_rows(self, t, C47.at((49, 51)), run_time=0.5, scroll_time=0.25)
            vo.wait_until("each line prefixed with its service")
            pre_p = glyph_range(ban[1], 0, len("processor  |"))
            pre_g = glyph_range(ban[2], 0, len("gateway    |"))
            self.play(pre_p.animate.set_color(CTR), flash(pf, CTR, 1.04, 0.6), run_time=0.6)
            self.play(pre_g.animate.set_color(CTR), flash(gf, CTR, 1.04, 0.6), run_time=0.6)
            vo.wait_until("Pause and run it")
            self.play(FadeIn(card4, shift=UP * 0.1), run_time=0.5)

        # ============================================================ 5 · the page; a second terminal; ps
        pg = PortPage(8090, reply=R49, compact=True, ports=False)
        pg.shift([0 - pg.frame.get_center()[0], (TOP - 0.5) - pg.frame.get_top()[1], 0])
        rs = ReplyStrip(C49.line(2))
        rs.shift([0 - rs.frame.get_center()[0], (STRIP_TOP + 0.16) - rs.frame.get_bottom()[1], 0])
        assert rs.get_top()[1] < pg.frame.get_bottom()[1] - 0.05, (rs.get_top()[1], pg.frame.get_bottom()[1])
        rc460 = readme_chip("README.md · line 460", "Open http://localhost:8090")
        place(rc460, right=6.55, cy=BAND_Y)
        assert rc460.get_left()[0] > tr.get_right()[0] + 0.1, rc460.get_left()[0]
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(net, img_g, img_p, card4, *ticks.values())), run_time=0.4)
            resize(self, t, 3, run_time=0.5)
            self.play(FadeIn(pg, shift=DOWN * 0.15), FadeIn(rc460, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(rs, shift=UP * 0.1), flash(pg.address, TURN, 1.1), run_time=0.5)
            self.play(flash(pg.reply_value.glyphs, TURN, 1.06), flash(rs.span("HELLO FROM THE LAPTOP"), TURN, 1.06),
                      run_time=0.7)
            vo.wait_until("In a second terminal")
            self.wait(0.4)
            self.play(FadeOut(VGroup(pg, rs, rc460)), run_time=0.4)
            t2 = term(P_HOME, rows=7, title="laptop · second terminal", top=T2_TOP)
            assert t2.box.get_bottom()[1] > STRIP_TOP + 0.08, t2.box.get_bottom()[1]
            self.play(FadeIn(t2, shift=DOWN * 0.3), run_time=0.5)
            home = bare_prompt(self, t2)
            tilde = glyph_range(home, P_HOME.index("~"), P_HOME.index("~") + 1)
            cap_a = note("new terminal: cd here first")
            cap_b = note("· Compose reads the file in the current folder")
            caps = VGroup(cap_a, cap_b).arrange(RIGHT, buff=0.12)
            beside(caps, t2, home, buff=0.5)
            assert caps.get_left()[0] > home.glyphs.get_right()[0] + 0.15
            self.play(Indicate(tilde, color=TURN, scale_factor=1.4), FadeIn(cap_a), run_time=0.8)
            vo.wait_until("Compose reads the file in the current folder")
            self.play(FadeIn(cap_b, shift=LEFT * 0.1), run_time=0.5)
            self.wait(0.8)
            _drop_bare(self, t2)
            t2.set_prompt(P_TOY)
            ln2 = bare_prompt(self, t2)
            self.play(FadeOut(caps), Indicate(glyph_range(ln2, P_TOY.index(":") + 1, len(P_TOY) - 1), color=TURN,
                                              scale_factor=1.05), run_time=0.6)
            vo.wait_until("There, docker compose ps")
            self.play(tr.goto(2), run_time=0.4)
            type_cmd(self, t2, PS, type_time=0.5)
            ps = t2.print(self, C48.at((2, 4)), wrap=True, run_time=0.5)
            c0 = PORTS_COL - 65
            b_head = col_box(ps[1], c0, c0 + len("PORTS"))
            b_val = col_box(ps[3], c0, c0 + len("127.0.0.1:8090->9100/tcp"))
            self.play(Create(b_head), Create(b_val), glyph_range(ps[3], c0, c0 + 24).animate.set_color(TURN),
                      run_time=0.5)
            for row, bb in ((ps[1], b_head), (ps[3], b_val)):
                self.remove(bb)
                row.add(bb)

        # ============================================================ 6 · network ls (extra); compose exec
        cap6 = mixed("the README's table writes curl ...: this is step 2's command", ["curl ..."])
        place(cap6, left=X_L + 0.05, cy=(T2_TOP + 2.906) / 2)
        assert cap6.get_top()[1] < 2.9 and cap6.get_bottom()[1] > T2_TOP
        with self.voiceover(SAY[6]) as vo:
            self.play(caption_extra(tr, True), run_time=0.3)
            type_extra(self, t2, NET_LS, type_time=0.5)
            room(self, t2, n_rows(t2, C50.at((2, 6))))
            nl = t2.print(self, C50.at((2, 6)), run_time=0.5)
            tn = nl[4]
            by = tag_after(t2, tn, grey_tag("created by Compose"))
            self.play(substring(tn, "toynet").animate.set_color(CTR), run_time=0.4)
            pin(self, tn, by)
            vo.wait_until("and compose exec reaches the processor")
            self.play(caption_extra(tr, False), run_time=0.3)
            room(self, t2, 2)                       # the prompt row + the command row
            type_cmd(self, t2, EXEC, type_time=1.0)
            ok = t2.print(self, [(C51.line(2), VENV)], run_time=0.35)[0]
            meter = tag_after(t2, ok, grey_tag("no progress meter: compose exec gives curl a terminal"))
            pin(self, ok, meter)
            self.play(FadeIn(cap6, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("ok")
            self.play(flash(ok.glyphs, VENV, 1.3), run_time=0.6)

        # ============================================================ 7 · the README's table; the log
        card7 = compare_card()
        hd7 = _header_text("README.md · lines 478–484")
        place(card7, cx=0, top=TOP - 0.42)
        hd7.next_to(card7.frame, UP, buff=0.08).align_to(card7.frame, LEFT).shift(RIGHT * 0.12)
        assert card7.frame.get_bottom()[1] > STRIP_TOP + 0.1 and card7.width < 12.9, card7.width
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(t2, cap6)), run_time=0.4)
            self.play(FadeIn(VGroup(card7.frame, *card7.heads, card7.submobjects[1], hd7)), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(VGroup(*r), shift=RIGHT * 0.1) for r in card7.cells], lag_ratio=0.45),
                      run_time=2.6)
            vo.wait_until("In the first terminal")
            self.play(FadeOut(VGroup(card7, hd7)), run_time=0.4)
            resize(self, t, 7, run_time=0.5)
            req = t.print(self, C47.at((52, 54)), run_time=0.5)
            self.play(substring(req[0], "POST").animate.set_color(TURN), substring(req[1], "POST").animate.set_color(TURN),
                      substring(req[2], "GET /health").animate.set_color(TURN), run_time=0.5)

        # ============================================================ 8 · Ctrl+C: about 20 seconds
        cap8a = note("the README does this at the end of Step 4")
        cap8b = note("· here: the foreground app")
        cap8 = VGroup(cap8a, cap8b).arrange(RIGHT, buff=0.12)
        place(cap8, left=X_L + 0.05, cy=TOP - 0.25)
        kc = keycaps("Ctrl", "C")
        place(kc, cx=-1.2, cy=(T7 + TOP - 0.5) / 2)
        sw = Stopwatch("≈ 20 s")
        place(sw, cx=3.2, cy=(T7 + TOP - 0.5) / 2)
        with self.voiceover(SAY[8]) as vo:
            self.play(tr.goto(5), FadeIn(cap8a, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("we stop it now")
            self.play(FadeIn(cap8b, shift=LEFT * 0.1), t.box.animate.set_stroke(TURN, 3), run_time=0.5)
            self.play(flash(VGroup(*[ln.glyphs for ln in t.lines]), TURN, 1.02, 0.8))
            self.play(t.box.animate.set_stroke(S.GREY_DARK, 2), run_time=0.4)
            vo.wait_until("press Control C")
            self.play(FadeIn(kc, shift=DOWN * 0.25), run_time=0.4)
            self.play(kc.animate.shift(DOWN * 0.12).scale(0.95), run_time=0.15)
            self.play(kc.animate.shift(UP * 0.12).scale(1 / 0.95), run_time=0.15)
            self.play(flash(kc, TURN, 1.06, 0.4))
            grace = t.print(self, [C47.line(55)], run_time=0.35)[0]
            vo.wait_until("Compose says it's stopping gracefully")
            self.play(flash(substring(grace, "Gracefully Stopping..."), TURN, 1.06), run_time=0.7)
            vo.wait_until("but it takes about 20 seconds")
            self.play(FadeIn(sw), run_time=0.3)
            t.print(self, [C47.line(56)], run_time=0.25)
            self.play(sw.sweep(1 / 6, 1.4))
            room(self, t, 3, run_time=0.3)
            t.print(self, [C47.line(57), C47.line(58), (C47.line(59), ERR)], run_time=0.35)
            self.play(sw.sweep(1 / 6, 1.4))
            room(self, t, 2, run_time=0.3)
            t.print(self, [C47.line(60), (C47.line(61), ERR)], run_time=0.35)
            sw.freeze()

        # ============================================================ 9 · the polite signal, then kill
        net9 = v6(show=("boxes", "rail", "rail_label", "plug_gateway", "plug_processor"))
        gf, pf = net9.boxes["gateway"].frame, net9.boxes["processor"].frame
        mid_y = gf.get_center()[1]
        cap9 = note("Python = the first process")
        place(cap9, left=X_L + 0.05, cy=TOP - 0.3)
        env1 = envelope("stop")
        place(env1, left=X_L + 0.3, cy=mid_y - 0.2)
        env1_at = gf.get_left()[0] - 0.08 - env1.frame.get_right()[0]
        clk1 = Stopwatch("10 s")
        place(clk1, cx=gf.get_right()[0] + 0.75, cy=mid_y)
        clk2 = Stopwatch("10 s")
        place(clk2, cx=pf.get_left()[0] - 1.85, cy=mid_y)
        env2 = envelope("stop")
        place(env2, cx=pf.get_left()[0] - 1.0, cy=mid_y - 0.2)
        env2_at = pf.get_left()[0] - 0.08 - env2.frame.get_right()[0]
        k1, k2 = kill_stamp(net9.boxes["gateway"]), kill_stamp(net9.boxes["processor"])
        for k, fr in ((k1, gf), (k2, pf)):
            assert fr.get_left()[0] + 0.02 < k.get_left()[0] and k.get_right()[0] < fr.get_right()[0] - 0.02
        c137 = _keep(chip("137 = 128 + 9: killed", ERR, size=22, text_color=ERR))
        place(c137, cx=(gf.get_right()[0] + pf.get_left()[0]) / 2, cy=gf.get_top()[1] - 0.33)
        assert c137.get_left()[0] > gf.get_right()[0] + 0.1 and c137.get_right()[0] < pf.get_left()[0] - 0.1
        assert c137.get_bottom()[1] > env2.frame.get_top()[1] + 0.08, (c137.get_bottom()[1], env2.frame.get_top()[1])
        assert clk2.get_left()[0] > clk1.get_right()[0] + 0.3
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(kc, sw, cap8)), FadeIn(net9), run_time=0.6)
            self.play(FadeIn(cap9, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("ignores the polite stop signal")
            self.play(FadeIn(env1, shift=RIGHT * 0.2), run_time=0.3)
            self.play(env1.animate.shift(RIGHT * env1_at), run_time=0.9)
            self.play(Wiggle(env1, scale_value=1.15, rotation_angle=0.05), run_time=0.6)
            self.play(env1.animate.set_opacity(0.35), run_time=0.3)
            vo.wait_until("unless it's written to catch it")
            self.play(flash(cap9, S.GREY, 1.06), run_time=0.6)
            vo.wait_until("So Docker waits 10 seconds per container")
            self.play(FadeIn(clk1), run_time=0.3)
            self.play(clk1.sweep(1 / 6, 1.2))
            clk1.freeze()
            vo.wait_until("then kills it")
            self.play(FadeIn(k1, scale=1.25), run_time=0.35)
            self.play(FadeOut(clk1), FadeIn(env2, shift=RIGHT * 0.2), run_time=0.3)
            self.play(env2.animate.shift(RIGHT * env2_at), run_time=0.6)
            self.play(Wiggle(env2, scale_value=1.15, rotation_angle=0.05), run_time=0.5)
            self.play(env2.animate.set_opacity(0.35), FadeIn(clk2), run_time=0.3)
            self.play(clk2.sweep(1 / 6, 1.0))
            clk2.freeze()
            self.play(FadeIn(k2, scale=1.25), run_time=0.35)
            self.play(FadeOut(clk2), FadeIn(c137, shift=UP * 0.1), run_time=0.4)

        # ============================================================ 10 · 137; ps -a: still there
        with self.voiceover(SAY[10]) as vo:
            r59, r61 = t.find("gateway exited with code 137"), t.find("processor exited with code 137")
            self.play(flash(substring(r59, "137"), ERR, 1.3), flash(substring(r61, "137"), ERR, 1.3),
                      flash(c137, ERR, 1.08), run_time=0.8)
            self.play(FadeOut(cap9), run_time=0.3)
            bare_prompt(self, t)
            vo.wait_until("Docker compose ps dash a")
            type_cmd(self, t, PS_A, type_time=0.5)
            room(self, t, n_rows(t, C52.at((2, 4)), wrap=True))
            pa = t.print(self, C52.at((2, 4)), wrap=True, run_time=0.5)
            e0 = EXITED_COL - 65
            bxs = [col_box(pa[k], e0, e0 + len("Exited (137)")) for k in (3, 5)]
            self.play(*[Create(b) for b in bxs], run_time=0.5)
            for k, bb in zip((3, 5), bxs):
                self.remove(bb)
                pa[k].add(bb)
            vo.wait_until("both containers exited")
            self.play(FadeOut(VGroup(k1, k2, c137, env1, env2)), net9.stop_box("gateway"), net9.stop_box("processor"),
                      *[net9.boxes[n].cells.animate.set_stroke(S.GREY).set_fill(S.GREY, 0.12)
                        for n in ("gateway", "processor")], run_time=0.7)
            vo.wait_until("but they're still there")
            self.play(flash(gf, S.GREY, 1.04), flash(pf, S.GREY, 1.04), run_time=0.7)

        # ============================================================ 11 · down: removed; the cycle
        rc519 = readme_chip("README.md · line 519", "Ctrl+C … leaves them in place.")
        place(rc519, left=X_L + 0.05, cy=TOP - 0.3)
        card11 = turn_card([(UP_CMD, "then Ctrl+C"), PS_A, DOWN_CMD, PS_A], header=None)
        place(card11, right=X_R, top=TOP - 0.3)
        card11.shift(UP * (TOP - 0.3 - card11.frame.get_top()[1]))
        assert card11.frame.get_bottom()[1] > T7 + 0.08, card11.frame.get_bottom()[1]
        assert card11.get_left()[0] > rc519.get_right()[0] + 0.2, (card11.get_left()[0], rc519.get_right()[0])
        gone = {"gateway": lambda: [net9.boxes["gateway"].animate.set_opacity(0), *net9.parts_out("plug_gateway")],
                "processor": lambda: [net9.boxes["processor"].animate.set_opacity(0),
                                      *net9.parts_out("plug_processor")],
                "rail": lambda: net9.parts_out("rail", "rail_label")}
        with self.voiceover(SAY[11]) as vo:
            type_cmd(self, t, DOWN_CMD, type_time=0.5)
            out_rows(self, t, [C53.line(2)], run_time=0.3)
            for n, key in DOWN_ROWS.items():
                out_rows(self, t, [C53.line(n)], run_time=0.5, extra=gone[key](), scroll_time=0.2)
            vo.wait_until("and nothing is left in ps dash a")
            type_cmd(self, t, PS_A, type_time=0.5)
            hdr = t.print(self, [C54.line(2)], run_time=0.3)[0]
            self.play(flash(hdr.glyphs, TURN, 1.04), run_time=0.6)
            vo.wait_until("Control C stops")
            self.play(FadeIn(rc519, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("down removes")
            self.play(flash(rc519.phrase, TURN, 1.05), run_time=0.6)
            vo.wait_until("Pause, and run the whole cycle")
            self.play(FadeIn(card11, shift=UP * 0.1), run_time=0.5)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        self.wait(0.2)
