r"""S14 · Change the ports (port_toy README › Step 3, steps 1–4; V7's slider).

Beats (script.md "## S14", one voiceover block each):
 0  TRACKER P3/1. V7 at the top (ToyNet squashed to 0.83 as in S11: the laptop's GREY street door
    `127.0.0.1:8090` with a small slider under its port, the PINK -p route into the gateway's TEAL
    room `:9100`, the processor's room `:9200`, the gateway's dashed aim `processor : 9200` on the
    toynet rail). Terminal (full width, 7 rows, `laptop`, student@laptop:~/AC215/port_toy$). On
    "First the street door" the door flashes. `docker rm -f gateway` -> port-laptop/30 line 2: the
    gateway's box, room, plug, door, slider, route and aim fade to a ghost. The README's five rows
    with `-p 127.0.0.1:8095:9100` are typed under the prompt -> 31 line 6 (the ID): the box, room,
    plug, aim, door and slider come back (the door still reads 8090). On "port 8095" `8095` is
    boxed YELLOW while the slider's knob slides right, the door's label turns 8090 -> 8095 and the
    route redraws. On "The room inside stays 9100" `9100` is boxed TEAL and the room flashes.
 1  The terminal shrinks to the strip (the -p row and the two -e rows stay) while V7 leaves and
    (overlapping) a compact PAGE(32) with its port card (address `localhost:8095`, 47520 · 9200 · 47520) at the
    right, REPLY(32: 2) in the left column (the line broken at its fields, tag "captured reply ·
    curl stood in for the Send button"); the address flashes. TRACKER P3/1 · extra: the reply
    leaves and the page folds its port card (address bar + reply card stay) while the terminal
    grows to 7 rows; it types `curl --max-time 3 http://localhost:8090` (extra, GREY tag) -> 33
    line 2, RED; then `docker ps --format 'table {{.Image}}\t{{.Ports}}\t{{.Names}}'` (extra) -> 35
    lines 2–4, `127.0.0.1:8095->9100/tcp` YELLOW. On "Pause and move your gateway's door": the page
    leaves, the terminal shrinks to 5 rows (docker ps's prompt row with its extra tag, the command,
    its output) and the static GREY your-turn card (`docker rm -f gateway` · the run's five rows ·
    open localhost:8095) appears above it, ▶ your turn on it.
 2  The card leaves and the terminal shrinks to the strip (docker ps's output). A GREY README card
    `README.md · lines 357–363` (the heading and lines 359, 361,
    363 as rendered) at the left; at the right, a small V7-style picture: the laptop's dashed wall
    with door `127.0.0.1:8090` held by a GREY box "another app" (its room `:9100`), then door
    `127.0.0.1:8095` leading to the TEAL gateway (room `:9100`). README rows light YELLOW as the
    SAY paraphrases them; on "Doors on the laptop must be unique" both door numbers flash; on
    "rooms inside containers never collide" both `:9100` rooms flash and the GREY caption "rooms
    never collide" appears.
 3  TRACKER P3/1 · extra. The card and the picture leave; the strip types `docker logs gateway`
    (extra) -> 34 line 2; `open http://localhost:8090` underlines RED and lifts into an excerpt chip
    `open http://localhost:8090` (header `gateway/gateway.py · line 53 (excerpt)`) with the tag
    `erratum` beside it; on "hard-coded" `8090` underlines RED and a GREY note "a hard-coded string"
    appears; on "Trust docker ps" two GREEN chips "trust docker ps" · "trust the page's diagram".
 4  TRACKER P3/2. The chips leave; the terminal is cleared into 7 rows while V7 (door now 8095)
    returns above it. `docker rm -f processor` -> 36 line 2: the processor's box, room and plug fade
    to a ghost. The README's two rows with `-e PORT=9300` -> 37 line 3: the processor comes back,
    `PORT=9300` is boxed TEAL as its room turns `:9200` -> `:9300`. On "The README says" the
    terminal shrinks to the strip (the two rows and the ID stay), V7 settles above it, and the
    README chip `README.md · line 380` "Send a message from the browser. It should fail." drops in
    above V7; on "it should fail" the gateway's aim, still `processor : 9200`, turns RED and pulses
    (border and text only: the chip's fill stays dark).
 5  V7 and the chip leave; the compact PAGE(32) returns exactly as it was (old reply, port card).
    On "It does": the address bar is clicked (Send), nothing on the page moves. On "The page has
    no error handling": the tag `erratum · no error handling` / `index.html lines 95–100` in the
    left column; on "so nothing on it changes" a GREY tag "the page doesn't change" sits on the
    page's bottom edge; on "the captured request" REPLY(38: 3) in RED in the left column.
 6  TRACKER P3/2 · extra. The page, the tags and the reply leave; the strip grows into an 11-row
    terminal (cleared) and types `docker logs gateway` (extra) -> 39 lines 2–5 (5 wrapped), …,
    25–26, …, 55. On "it found the processor by name" line 25 (`File "/app/gateway.py", line 34,
    in do_POST`) turns YELLOW; on "but the connection was refused" line 55 turns RED. On "nobody
    listens on 9200 anymore" the terminal shrinks to 4 rows (lines 25, 26, …, 55) and the GREY
    cheat-sheet card `README.md · lines 551–552` appears above it: `Connection refused` · "nothing
    is listening at that address and port", with a GREEN tick "the name resolved" beside it; on
    "A wrong name fails differently" a dashed GREY row `could not resolve host` · "a wrong name ·
    see the exercises".
 7  The terminal and the card leave; V7 returns at the top (processor room `:9300`, the gateway's
    RED aim `processor : 9200`); on "Which one setting" two chips under the boxes: the gateway's
    `PROCESSOR_PORT=9200` and the processor's `PORT=9300` (GREY notes under them). PONDER (6 s),
    card at the bottom; the picture above it does not show the answer.
 8  TRACKER P3/3. The card leaves while the gateway's chip flashes YELLOW; the chips leave and a
    7-row terminal rises under V7. `docker rm -f gateway` -> 41 line 2 (the gateway fades to a
    ghost); the README's five rows with `-p 127.0.0.1:8090:9100` and `-e PROCESSOR_PORT=9300` -> 42
    line 6; the gateway (with its door and slider) comes back, `PROCESSOR_PORT=9300` is boxed GREEN
    as the aim re-aims at `processor : 9300` in PINK; the slider slides back to 8090 and the route
    redraws. On "and the
    message goes through" the terminal shrinks to the strip (the -p row and the two -e rows stay),
    V7 leaves, PAGE(43) (compact, port card) at the right with `processor listening on port 9300`
    YELLOW, REPLY(43: 2) in the left column with `"listen_port": 9300,` YELLOW. On "No image was
    rebuilt" a GREY card "no rebuild · configuration only" / "README.md · lines 404–409" under the
    reply. On "Pause and fix yours" the page, the reply and that card give way to the static GREY
    your-turn card (`docker rm -f gateway` · the run's five rows · open localhost:8090 and send a
    message), ▶ your turn on it.
 9  The your-turn card leaves; the strip's `PROCESSOR_PORT=9300` lifts into a chip
    (the gateway's, left) and `PORT=9300` (the processor's, right) appears; a GREEN "=" links them
    and the caption "the two settings must agree" sits under it; the two chips flash as named.
10  TRACKER P3/4. The chips and the strip's rows leave; the terminal grows to 7 rows under V7. `docker rm -f
    gateway processor` -> 44 lines 2–3: both boxes (and the door, route, aim and slider) dissolve;
    `docker network rm toynet` -> 45 line 2: the rail dissolves. TRACKER P3/4 · extra: the rest of
    V7 leaves and the terminal grows to 10 rows; `docker ps -a` (extra) -> 46 lines 2–3 (wrap),
    `hello-world` boxed YELLOW; `docker network ls` (extra) -> 46 lines 4–7, GREY tag "no toynet".
    On "Skip this" the RED excerpt chip `Conflict. The container name "/processor" is already in
    use` (header `docker compose up · if the old containers remain (excerpt)`, from 68 lines 8–9
    joined) drops in above the terminal, the GREY caption "if you skip this: Compose wants these
    names" right of the tracker. On "Pause and clean up" the static GREY your-turn card (the two
    README commands, the two extras tagged) replaces the terminal and the tracker caption drops
    " · extra". Fade out to an empty frame.

Deviations from SHOW (and why):
- The terminal under V7 has 7 rows (top y 0.17), not 8 (top 0.58), and V7 is S11's 0.83 vertical
  squash (2.6 tall), not 2.3: at 2.3 units the ToyNet's labels collide (box name over room label,
  room over port strip), and a 7-row terminal is exactly the prompt + the README's five rows + the
  ID, the configuration S11 used for the same run. The `docker rm` line scrolls away as the run is
  typed (it is on the your-turn cards).
- The README's multi-row runs are typed on the rows under the long prompt, indented 4 (as S11):
  the prompt plus their first row is longer than a terminal row.
- Beat 1: the two extras are typed in a 7-row terminal under the page folded to its reply card,
  not in the strip: in a 3-row strip docker ps's command would scroll away the moment its three
  output lines print. Under the your-turn card the terminal keeps 5 rows (docker ps's prompt row
  with the extra tag, the command, its output); for that the card has no GREY "your turn" header
  note (the ▶ your turn tag on its corner says it) and sits 0.2 higher.
- Every extra command has the GREY `extra` tag beside it (script conventions); docker ps's command
  row is a full 65 characters, so its tag sits after the prompt on the row above (as S13).
- `docker rm -f` of a container is drawn: its box (and what it owns: the door, the route, the
  aim) fades to a ghost and comes back with the new `docker run`; the slider moves when the door
  returns. SHOW only names the slider; the ghost makes "remove, start again" visible.
- Beats 1, 5, 8: the compact PAGE shows its port card (as SHOW asks), so it is 3.9 tall; the
  REPLY strip then cannot sit under it above the strip and goes into the left column (5.7 wide),
  broken at its fields (`{"upper":` / `"HELLO FROM THE LAPTOP",` / one key per row), not at a
  fixed column; REPLY(38) is broken at the space before "server". The reply tag and the erratum
  tag are two-row tags (each is 7+ units on one row).
- Beat 2: the README card quotes the heading (357) and lines 359, 361 and 363 as rendered, broken
  into rows of at most 58 characters; the picture uses V7's vocabulary but is its own drawing
  (the ToyNet has no place for a second app at a laptop door). "another app" is GREY with a GREY
  room (not ours); the gateway's is TEAL.
- Beat 4: the README chip (9.3 wide) cannot sit beside the tracker or over a 7-row terminal, so
  the terminal shrinks to the strip and V7 moves down under the chip (as S11 beat 4). The aim
  turns RED after the chip, on "it should fail" (SHOW lists it before the chip): typing the two
  commands fills the first sentence, and the RED aim is what "it should fail" predicts.
- Beat 5: the compact page has no Send button; the click is the address bar's flash.
- Beat 6: the cheat-sheet card (9.4 wide) does not fit above an 11-row terminal (1.1 units), so the
  terminal shrinks to the four lines it explains once both are highlighted. Row 1 quotes the
  README's "nothing is listening at that address and port"; row 2 is SHOW's "a wrong name ·
  see the exercises" in a dashed box.
- Beat 7: V7 stays at S11's squash (not full size), so the chips and the ponder card fit under it.
- Beat 8: the ▶ sits on a static your-turn card, not on the strip's run line: the strip holds only
  three of the run's five rows and not the docker rm (script conventions: a ▶ never sits on a
  frame that cannot be read when paused).
- Beat 10: after the clean-up the rest of V7 leaves and the terminal grows to 10 rows, so `docker
  ps -a` (wrapped) and `docker network ls` are both on screen with their commands; the RED chip
  sits above the 10 rows and its caption in the top band right of the tracker. The closing ▶ sits
  on a static your-turn card (the clean-up commands scrolled away).
"""

import re

import numpy as np
from common import (
    CTR,
    ERR,
    INK,
    LAPTOP,
    LOOKUP,
    NARRATION,
    P_TOY,
    STRIP_TOP,
    TURN,
    VENV,
    PortPage,
    Prose,
    ToyNet,
    _header_text,
    _keep,
    bare_prompt,
    caption_extra,
    capture,
    door,
    erratum_tag,
    excerpt,
    excerpt_chip,
    extra_tag,
    fix_chip,
    grey_tag,
    note,
    page_reply,
    pin,
    readme_chip,
    resize,
    sans,
    strip_top,
    term,
    tracker,
    turn_card,
    type_cmd,
    under,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UL,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    RoundedRectangle,
    ShowIncreasingSubsets,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
    linear,
    there_and_back,
)

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import (
    CAPTION,
    MONO,
    OUTPUT,
    TAG,
    TERM_BG,
    box,
    cell_width,
    check_mark,
    chip,
    glyph_range,
    label,
    line_pitch,
    mono,
    mono_line,
    substring,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S14"]
assert len(SAY) == 11, len(SAY)

# ------------------------------------------------------------------ captures (file line numbers)
PL = "port-laptop"
TOY = "port_toy/README.md"
C30, C31, C32, C33 = (capture(n, PL) for n in ("30", "31", "32", "33"))
C34, C35, C36, C37 = (capture(n, PL) for n in ("34", "35", "36", "37"))
C38, C39, C41, C42 = (capture(n, PL) for n in ("38", "39", "41", "42"))
C43, C44, C45, C46, C68 = (capture(n, PL) for n in ("43", "44", "45", "46", "68"))

RM_GW = C30.cmd
assert RM_GW == "docker rm -f gateway" == excerpt(TOY, 340, 340) == C41.cmd
RUN_8095 = [C31.cmd] + C31.at((2, 5))                    # the README's five rows
assert RUN_8095 == excerpt(TOY, 346, 350).split("\n"), RUN_8095
RM_PR = C36.cmd
assert RM_PR == "docker rm -f processor" == excerpt(TOY, 370, 370)
RUN_9300P = [C37.cmd, C37.line(2)]                      # the README's two rows
assert RUN_9300P == excerpt(TOY, 376, 377).split("\n"), RUN_9300P
RUN_9300G = [C42.cmd] + C42.at((2, 5))
assert RUN_9300G == excerpt(TOY, 395, 399).split("\n"), RUN_9300G
RM_BOTH, NET_RM = C44.cmd, C45.cmd
assert [RM_BOTH, NET_RM] == excerpt(TOY, 416, 417).split("\n")
CURL_8090 = C33.cmd
PS_SHORT = C35.cmd
assert PS_SHORT == "docker ps --format 'table {{.Image}}\\t{{.Ports}}\\t{{.Names}}'"
LOGS_GW = C34.cmd
assert LOGS_GW == "docker logs gateway" == C39.cmd
assert C46.cmd == "docker ps -a; docker network ls"
PS_A, NET_LS = "docker ps -a", "docker network ls"   # the capture's `;` line, typed as two commands
R32, R43 = page_reply(C32, 2), page_reply(C43, 2)
assert R32["listen_port"] == 9200 and R32["sender_port"] == R32["gateway_out_port"] == 47520
assert R43["listen_port"] == 9300 and R43["upper"] == "HELLO FROM THE LAPTOP"
assert C38.line(2) == "" and C38.line(3) == "curl: (52) Empty reply from server"
LOG_LINE = C34.line(2)
OPEN_8090 = "open http://localhost:8090"
assert OPEN_8090 in LOG_LINE
CONFLICT = 'Conflict. The container name "/processor" is already in use'
L68 = C68.join(8, 9)                                     # the capture terminal wrapped it at 80 columns
assert CONFLICT in L68

# ------------------------------------------------------------------ sources
GW_PY = "port_toy/gateway/gateway.py"
L53 = excerpt(GW_PY, 53, 53)
assert OPEN_8090 in L53
assert excerpt(TOY, 380, 380) == "Send a message from the browser. It should fail."
README_357 = ["When would you change the host port?",
              "Suppose another application already uses host port 8090.",
              "You cannot publish both applications on the same host",
              "address and port. Choose another host port, such as 8095.",
              "The containers can still use the same internal port.",
              "Each container has its own network environment."]
_src357 = excerpt(TOY, 357, 363).replace("`", "").replace("### ", "")
assert " ".join(README_357[2:4]) in _src357 and all(r in _src357 for r in README_357[:2] + README_357[4:])
assert "The two settings must agree" in excerpt(TOY, 404, 409)
assert "without rebuilding the images" in excerpt(TOY, 404, 409)
_src551 = excerpt(TOY, 551, 552)
CHEAT_A = "nothing is listening at that address and port"
assert "`Connection refused`" in _src551 and CHEAT_A in _src551 and "`could not resolve host`" in _src551
assert "const response = await fetch" in excerpt("port_toy/gateway/index.html", 95, 100)

# ------------------------------------------------------------------ layout
TOP = 2.86                        # top of anything under the tracker (its bottom is 2.905)
K_NET = 0.83                      # ToyNet's vertical squash (as S11)
T7_TOP = strip_top(7)             # 0.17: a 7-row terminal under V7
P20 = line_pitch(CAPTION)
PAGE_TOP = 2.85                   # the page's window top (its illustration tag sits above, right)
COL_L, COL_R = -6.45, -0.75       # the left column beside the page
COL_TOP = 2.74                    # its top (0.17 under the tracker's caption)
CAP_GREY = S.GREY


# ------------------------------------------------------------------ helpers
def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def flash_chip(c, color: str, k: float = 1.1, run_time: float = 0.7):
    """Flash a chip with an opaque fill (the ToyNet's aim chip: [0] frame, [1] text): its border
    and text pulse in `color` while the fill stays dark (Indicate would paint the fill over the
    text)."""
    fr, tx = c[0], c[1]
    return AnimationGroup(fr.animate(rate_func=there_and_back).set_stroke(color, width=5).scale(k),
                          Indicate(tx, color=color, scale_factor=k), run_time=run_time)


def glyph_box(line, sub: str, color: str = TURN, pad: float = 0.04, occurrence: int = 0):
    """A box around the glyphs of `sub` in a mono line, as tall as the row (not added)."""
    g = substring(line, sub, occurrence)
    r = box(g.width + 2 * pad + 0.04, line.strut.height + 0.04, color, fill_opacity=0.0, radius=0.06,
            stroke=3)
    return r.move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def type_rows(scene, t, rows: list[str], type_time: float = 2.0):
    """The README's rows of a multi-line command typed under the long prompt (as S11): the prompt
    alone on its row, then each README row indented 4 (continuations keep their own 2 spaces).
    Returns a VGroup with .rows (rows[0] is the prompt row)."""
    from common import _drop_bare
    _drop_bare(scene, t)
    texts = [t.prompt] + ["    " + r for r in rows]
    assert all(len(s) <= t.max_chars for s in texts), texts
    t._make_room(scene, len(texts))
    out = []
    for k, s in enumerate(texts):
        ln = mono_line(s, t.size, INK, t2c=t._prompt_colors(t.prompt) if k == 0 else None)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        out.append(ln)
    scene.add(out[0])
    typed = VGroup(*[g for r in out[1:] for g in glyph_range(r, 0)])
    scene.play(ShowIncreasingSubsets(typed, rate_func=linear), run_time=type_time)
    for r in out:
        scene.add(r)
    g = VGroup(*out)
    g.rows = out
    return g


def type_extra(scene, t, cmd: str, type_time: float | None = None):
    """Type an extra command (not in the README) and pin a GREY `extra` tag beside it: after the
    command's last row when there is room, else after the prompt on the row above (as S13)."""
    ln = type_cmd(scene, t, cmd, type_time=type_time)
    tg = extra_tag()
    rows = ln.rows if hasattr(ln, "rows") else [ln]
    for row in reversed(rows):
        end = row.glyphs.get_right()[0] if len(row.glyphs) else row.strut.get_left()[0]
        if end + 0.3 + tg.width < t.box.get_right()[0] - 0.12:
            tg.next_to(row.glyphs if len(row.glyphs) else row.strut, RIGHT, buff=0.3)
            tg.set_y(row.strut.get_center()[1])
            pin(scene, row, tg, run_time=0.25)
            return ln
    raise AssertionError(cmd)


def unit(m):
    """Mark a mobject to keep its shape when the ToyNet is squashed."""
    m.squash_unit = True
    return m


def squash(net: ToyNet, k: float):
    """Shrink a ToyNet vertically by k about its centre: frames, lines and gaps shrink, every text,
    tag and glyph (door, loop, browser, arrow tip, chip) keeps its size and shape (as S11)."""
    for b in net.boxes.values():
        unit(b.loop)
    unit(net.laptop_loop[0])
    unit(net.browser)
    for d in list(net.doors.values()) + list(net.rooms.values()):
        unit(d.frame)
    unit(net.parts["map"][1])
    unit(net.aim_chip)
    unit(net.parts["laptop_label"])
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


def slider(lab) -> VGroup:
    """V7's slider under a street door's label: a GREY track under the port digits and a YELLOW
    knob at its left end (8090); .to(right) moves the knob to the right end (8095). .track .knob"""
    digits = VGroup(*lab.submobjects[-4:])
    y = lab.get_bottom()[1] - 0.13
    x0, x1 = digits.get_left()[0] - 0.02, digits.get_right()[0] + 0.02
    track = Line([x0, y, 0], [x1, y, 0], color=S.GREY, stroke_width=3)
    ends = VGroup(*[Line([x, y - 0.06, 0], [x, y + 0.06, 0], color=S.GREY, stroke_width=2.5) for x in (x0, x1)])
    knob = RoundedRectangle(width=0.11, height=0.22, corner_radius=0.04, stroke_width=0).set_fill(TURN, 1)
    knob.move_to([x0 + 0.06, y, 0])
    g = VGroup(track, ends, knob)
    g.track, g.knob, g.x0, g.x1 = track, knob, x0 + 0.06, x1 - 0.06
    return _keep(g)


def ghost_of(m, k: float = 0.15):
    """A copy of m with every opacity scaled by k (the target of a fade-to-ghost Transform)."""
    c = m.copy()
    for f in c.get_family():
        if hasattr(f, "get_fill_opacity"):
            f.set_fill(opacity=f.get_fill_opacity() * k, family=False)
            f.set_stroke(opacity=f.get_stroke_opacity() * k, family=False)
    return c


def tag2(lines: list[str], color: str = S.GREY) -> VGroup:
    """A house tag (22 pt, opaque dark fill) with two rows of text, for tags wider than a column."""
    tx = VGroup(*[label(s, TAG, color) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    b = RoundedRectangle(width=tx.width + 0.4, height=tx.height + 0.22, corner_radius=0.18,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    tx.move_to(b)
    g = VGroup(b, tx)
    g.box, g.text = b, tx
    return _keep(g)


def reply_rows(text: str, cols: int) -> list[str]:
    """A captured reply broken at spaces into rows of at most `cols`: a JSON reply at its fields
    (after each ', ', a long field also after its ': '), other text greedily at words."""
    if text.startswith("{"):
        out = []
        for p in re.split(r"(?<=,) ", text):
            out += [p] if len(p) <= cols else p.split(": ", 1)
            if len(p) > cols:
                out[-2] += ":"
        assert all(len(r) <= cols for r in out), out
        return out
    rows, cur = [], ""
    for w in text.split(" "):
        if cur and len(cur) + 1 + len(w) > cols:
            rows.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return rows + [cur]


def reply_strip(text: str, width: float = COL_R - COL_L, color: str = OUTPUT) -> VGroup:
    """REPLY in the left column: the captured line in a GREY strip, broken by reply_rows (nothing
    retyped: the rows join back into the line with single spaces), the two-row tag "captured reply
    · curl stood in for the Send button" above it. .frame .rows .tag"""
    cols = int((width - 0.5) / cell_width(CAPTION))
    rows_s = reply_rows(text, cols)
    assert " ".join(rows_s) == text
    rows = VGroup()
    for i, s in enumerate(rows_s):
        ln = mono_line(s, CAPTION, color)
        ln.shift(np.array([0, -i * P20, 0]) - ln.strut.get_corner(UL))
        rows.add(ln)
    fr = RoundedRectangle(width=width, height=len(rows_s) * P20 + 0.3, corner_radius=0.12,
                          stroke_color=S.GREY, stroke_width=2).set_fill(TERM_BG, 1)
    fr.move_to(rows).align_to(rows, LEFT).shift(LEFT * 0.25)
    tg = tag2(["captured reply ·", "curl stood in for the Send button"])
    tg.next_to(fr, UP, buff=0.1).align_to(fr, LEFT)
    g = VGroup(fr, rows, tg)
    g.frame, g.rows, g.tag = fr, rows, tg
    g.shift([COL_L - fr.get_left()[0], COL_TOP - tg.get_top()[1], 0])
    return g


def place_page(pg: PortPage) -> PortPage:
    """The compact page at the right, window top at PAGE_TOP; port lines 0.1 left (the 5-digit
    values otherwise touch the port card's right border, as S12 found)."""
    if pg.port_lines:
        pg.port_box.shift(LEFT * 0.1)
    pg.shift([6.5 - pg.frame.get_right()[0], PAGE_TOP - pg.frame.get_top()[1], 0])
    return pg


def readme_rows_card(where: str, rows: list[str]) -> VGroup:
    """A GREY README card (rows serif, the README's words as rendered), header above. .frame .rows"""
    rs = VGroup(*[label(s, CAPTION, INK) for s in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
    fr = box(rs.width + 0.5, rs.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    rs.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    hd = _header_text(where).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, rs, hd)
    g.frame, g.rows, g.header = fr, rs, hd
    return g


def doors_picture() -> VGroup:
    """Beat 2: the laptop's dashed wall with two street doors, each leading to a room :9100 —
    door 127.0.0.1:8090 held by a GREY "another app", door 127.0.0.1:8095 the TEAL gateway's.
    .doors[i] (.frame .label) .rooms[i] (.frame .label) .boxes[i] .arrows[i] .wall"""
    wall_x, ys = 3.85, (1.75, 0.1)
    bx0, bx1 = 4.65, 6.45
    wall = DashedLine([wall_x, 2.55, 0], [wall_x, -0.7, 0], color=LAPTOP, stroke_width=3, dash_length=0.12)
    lap = note("your laptop").next_to(wall, UP, buff=0.08).align_to(wall, RIGHT).shift(LEFT * 0.1)
    doors, rooms, boxes, arrows = [], [], [], []
    for (host, name, col), y in zip((("127.0.0.1:8090", "another app", S.GREY),
                                     ("127.0.0.1:8095", "gateway", CTR)), ys):
        d = door(0.34, 0.56, LAPTOP).move_to([wall_x, y, 0])
        dl = mono(host, CAPTION, INK).next_to(d, LEFT, buff=0.12)
        dg = VGroup(d, dl)
        dg.frame, dg.label = d, dl
        fr = box(bx1 - bx0, 1.3, col, fill_opacity=0.07).move_to([(bx0 + bx1) / 2, y + 0.18, 0])
        nm = (sans(name, CAPTION, col) if name == "another app" else mono(name, CAPTION, col))
        nm.move_to([0, fr.get_top()[1] - 0.24, 0]).align_to(fr, RIGHT).shift(LEFT * 0.18)
        rd = door(0.3, 0.46, col).move_to([bx0, y, 0])
        rl = mono(":9100", CAPTION, col).next_to(rd, RIGHT, buff=0.08)
        rg = VGroup(rd, rl)
        rg.frame, rg.label = rd, rl
        ar = Arrow([wall_x + 0.17, y, 0], [bx0 - 0.15, y, 0], buff=0, color=LOOKUP, stroke_width=5,
                   max_tip_length_to_length_ratio=0.45)
        doors.append(dg)
        rooms.append(rg)
        boxes.append(VGroup(fr, nm))
        arrows.append(ar)
    g = VGroup(wall, lap, *boxes, *rooms, *doors, *arrows)
    g.wall, g.lap, g.doors, g.rooms, g.boxes, g.arrows = wall, lap, doors, rooms, boxes, arrows
    return g


def setting_chip(text: str, owner: str) -> VGroup:
    """A setting shown as a GREY mono chip, a GREY note naming its container left of it.
    .chip (.box .text) .note"""
    c = chip(text, S.GREY, size=CAPTION, font=MONO)
    n = note(owner)
    g = VGroup(n, c).arrange(RIGHT, buff=0.2)
    g.chip, g.note = c, n
    return _keep(g)


def no_rebuild_chip() -> VGroup:
    """Beat 8: a GREY chip "no rebuild · configuration only", headed by its source
    README.md · lines 404–409. .chip .header"""
    c = chip("no rebuild · configuration only", S.GREY, size=CAPTION)
    hd = _header_text("README.md · lines 404–409").next_to(c, UP, buff=0.08).align_to(c, LEFT).shift(RIGHT * 0.08)
    g = VGroup(c, hd)
    g.chip, g.header = c, hd
    return _keep(g)


def cheat_card() -> VGroup:
    """Beat 6: the GREY cheat-sheet card README.md · lines 551–552: `Connection refused` · the
    README's "nothing is listening at that address and port"; a dashed GREY row `could not
    resolve host` · "a wrong name · see the exercises" (hidden until written). .row_a .row_b .frame"""
    ra = VGroup(mono("Connection refused", CAPTION, ERR), label("· " + CHEAT_A, CAPTION, INK))
    ra.arrange(RIGHT, buff=0.15)
    rb_t = VGroup(mono("could not resolve host", CAPTION, S.GREY),
                  label("· a wrong name · see the exercises", CAPTION, S.GREY)).arrange(RIGHT, buff=0.15)
    rb_b = box(rb_t.width + 0.3, rb_t.height + 0.22, S.GREY, dashed=True, stroke=2)
    rb = VGroup(rb_b, rb_t.move_to(rb_b))
    rows = VGroup(ra, rb).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    ra.shift(RIGHT * 0.15)
    fr = box(rows.width + 0.6, rows.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    rows.move_to(fr)
    hd = _header_text("README.md · lines 551–552").next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, hd, ra, rb)
    g.frame, g.row_a, g.row_b, g.header = fr, ra, rb, hd
    return g


class ChangePorts(VoiceScene):
    def ponder_at(self, question: str, seconds: float, bottom: float):
        """pause_and_ponder's card and draining timer, its bottom edge at `bottom` (the picture
        above stays readable). Returns the card (removed at the start of the next block)."""
        card = ponder_card(question)
        card.move_to([0, bottom + card.height / 2, 0])
        card[0].set_fill(S.BG, 1)
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=seconds)
        return card

    def fade_to_ghost(self, mobs, run_time: float = 0.5):
        """Play: the mobs fade to a ghost (a removed container). Returns their full-opacity copies,
        for restore()."""
        backs = [m.copy() for m in mobs]
        self.play(*[Transform(m, ghost_of(m)) for m in mobs], run_time=run_time)
        return backs

    def construct(self):
        # ============================================================ V7, built once (as S11 left it)
        net = ToyNet(show=("outline", "laptop_label", "zone", "boxes", "rail", "rail_label", "plug_gateway",
                           "plug_processor", "door", "room_gateway", "room_processor", "map", "aim"))
        squash(net, K_NET)
        outline = net.parts["outline"]
        net.shift(UP * (T7_TOP + 0.08 - outline.get_bottom()[1]))
        assert net.parts["laptop_label"].get_top()[1] <= TOP, net.parts["laptop_label"].get_top()[1]
        d1 = net.doors["door"]
        sl = slider(d1.label)
        net.part("slider", sl)
        gw_box, pr_box = net.boxes["gateway"], net.boxes["processor"]
        gw_room, pr_room = net.rooms["gateway"], net.rooms["processor"]
        gw_owned = [gw_box, gw_room, net.plugs["gateway"], net.parts["aim"]]
        door_owned = [d1, sl, net.parts["map"]]
        pr_owned = [pr_box, pr_room, net.plugs["processor"]]
        up_low = (STRIP_TOP + 0.08) - outline.get_bottom()[1]      # V7 just above the 3-row strip

        # ============================================================ 0 · the street door: 8090 -> 8095
        tr = tracker("P3", 1)
        t = term(P_TOY, rows=7, title="laptop")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(net), FadeIn(t), run_time=0.7)
            bare_prompt(self, t)
            vo.wait_until("First the street door")
            self.play(flash(d1.frame, TURN, 1.3), flash(d1.label, TURN, 1.08), run_time=0.8)
            vo.wait_until("remove the gateway")
            type_cmd(self, t, RM_GW, type_time=0.8)
            t.print(self, [C30.line(2)], run_time=0.3)
            backs_gw = self.fade_to_ghost(gw_owned + door_owned)
            vo.wait_until("and start it again")
            run1 = type_rows(self, t, RUN_8095, type_time=2.0)
            t.print(self, [C31.line(6)], run_time=0.35)
            self.play(*[Transform(m, b) for m, b in zip(gw_owned + [d1, sl], backs_gw[:6])], run_time=0.6)
            vo.wait_until("port 8095")
            p_row = run1.rows[2]
            b95 = glyph_box(p_row, "8095", TURN)
            pin(self, p_row, b95, run_time=1.0,
                anim=AnimationGroup(Create(b95), net.set_door("127.0.0.1:8095"), sl.knob.animate.set_x(sl.x1),
                                    Transform(net.parts["map"], backs_gw[6])))
            vo.wait_until("The room inside stays 9100")
            b91 = glyph_box(p_row, "9100", CTR)
            pin(self, p_row, b91, anim=Create(b91), run_time=0.4)
            self.play(flash(gw_room, CTR, 1.3), run_time=0.8)

        # ============================================================ 1 · the page on 8095; two extra checks
        pg1 = place_page(PortPage(8095, reply=R32, compact=True, ports=True))
        pg1s = place_page(PortPage(8095, reply=R32, compact=True, ports=False))   # the same page, port card folded
        assert pg1s.frame.get_bottom()[1] > strip_top(7) + 0.25
        rp1 = reply_strip(C32.line(2))
        assert rp1.frame.get_bottom()[1] > STRIP_TOP + 0.1 and pg1.frame.get_bottom()[1] > STRIP_TOP + 0.1
        assert rp1.frame.get_right()[0] < pg1.frame.get_left()[0] - 0.15
        # no "your turn" header (the ▶ tag says it): the card sits high enough that 5 rows fit under
        # it, so docker ps keeps its prompt row with the extra tag
        card1 = turn_card([RM_GW, "\n".join(RUN_8095), Prose("in your browser: open localhost:8095")],
                          header=None)
        for row in card1.rows[1][1:]:                    # the README's continuation rows keep their 2 spaces
            row.shift(RIGHT * 2 * cell_width(CAPTION))
        card1.shift([0 - card1.frame.get_center()[0], strip_top(5) + 0.17 - card1.frame.get_bottom()[1], 0])
        assert card1.frame.get_top()[1] < TOP - 0.1 and card1.tag.get_top()[1] < 3.1, card1.get_top()[1]
        with self.voiceover(SAY[1], pad=1.2) as vo:
            keep = [run1.rows[2], run1.rows[3], run1.rows[4]]
            # V7 leaves while the page and the reply arrive (no empty frame between them)
            resize(self, t, 3, keep=keep, run_time=1.0,
                   extra=[LaggedStart(FadeOut(net), AnimationGroup(FadeIn(pg1, shift=LEFT * 0.15),
                                                                   FadeIn(rp1, shift=RIGHT * 0.15)),
                                      lag_ratio=0.45)])
            self.play(flash(pg1.address, TURN, 1.1), flash(pg1.reply_value.glyphs, TURN, 1.06), run_time=0.8)
            vo.wait_until("Two extra checks")
            # the reply leaves, the page folds its port card: room for a 7-row terminal
            resize(self, t, 7, run_time=0.6,
                   extra=[FadeOut(rp1), Transform(pg1.frame, pg1s.frame), *pg1.parts_out("ports"),
                          caption_extra(tr, True)])
            type_extra(self, t, CURL_8090, type_time=1.0)
            t.print(self, [(C33.line(2), ERR)], run_time=0.35)
            vo.wait_until("and docker ps shows")
            type_extra(self, t, PS_SHORT, type_time=1.3)
            ps = t.print(self, C35.at((2, 4)), run_time=0.4)
            m95 = substring(ps[1], "127.0.0.1:8095->9100/tcp")
            self.play(m95.animate.set_color(TURN), run_time=0.4)
            vo.wait_until("Pause and move")
            # 5 rows: docker ps (its prompt row with the extra tag, the command) and its output stay
            resize(self, t, 5, run_time=0.5, extra=[FadeOut(pg1), caption_extra(tr, False)])
            self.play(FadeIn(card1, shift=UP * 0.15), run_time=0.5)

        # ============================================================ 2 · why: another app holds 8090
        rc = readme_rows_card("README.md · lines 357–363", README_357)
        rc.shift([-6.45 - rc.frame.get_left()[0], TOP - 0.2 - rc.get_top()[1], 0])   # header clear of the tracker
        pic = doors_picture()
        assert rc.frame.get_right()[0] < pic.doors[0].label.get_left()[0] - 0.15, \
            (rc.frame.get_right()[0], pic.doors[0].label.get_left()[0])
        cap2 = note("rooms never collide").next_to(VGroup(*pic.boxes), DOWN, buff=0.18)
        cap2.align_to(VGroup(*pic.boxes), RIGHT)
        assert cap2.get_bottom()[1] > STRIP_TOP + 0.08 and rc.frame.get_bottom()[1] > STRIP_TOP + 0.08
        rows = rc.rows
        with self.voiceover(SAY[2]) as vo:
            resize(self, t, 3, run_time=0.6, extra=[FadeOut(card1), FadeIn(rc, shift=DOWN * 0.1)])
            self.play(rows[0].animate.set_color(TURN), run_time=0.3)
            vo.wait_until("Another app on your laptop")
            self.play(rows[0].animate.set_color(INK), rows[1].animate.set_color(TURN),
                      Create(pic.wall), FadeIn(pic.lap), run_time=0.5)
            self.play(FadeIn(pic.boxes[0]), FadeIn(pic.rooms[0]), FadeIn(pic.doors[0]), run_time=0.6)
            self.play(Create(pic.arrows[0]), run_time=0.4)
            self.play(FadeIn(pic.doors[1]), FadeIn(pic.boxes[1]), FadeIn(pic.rooms[1]), run_time=0.6)
            self.play(Create(pic.arrows[1]), run_time=0.4)
            vo.wait_until("Doors on the laptop must be unique")
            self.play(rows[1].animate.set_color(INK), rows[2].animate.set_color(TURN),
                      rows[3].animate.set_color(TURN), run_time=0.4)
            nums = [VGroup(*d.label.submobjects[-4:]) for d in pic.doors]
            self.play(*[flash(n, TURN, 1.25) for n in nums], *[flash(d.frame, TURN, 1.2) for d in pic.doors],
                      run_time=0.9)
            vo.wait_until("rooms inside containers never collide")
            self.play(rows[2].animate.set_color(INK), rows[3].animate.set_color(INK),
                      rows[4].animate.set_color(TURN), rows[5].animate.set_color(TURN), run_time=0.4)
            self.play(*[flash(r, TURN, 1.25) for r in pic.rooms], FadeIn(cap2, shift=UP * 0.1), run_time=0.9)

        # ============================================================ 3 · erratum: the log's hard-coded 8090
        ec = excerpt_chip(OPEN_8090, "gateway/gateway.py · line 53 (excerpt)", line=L53)
        ec.move_to([-0.6, 1.45, 0])
        et = erratum_tag().next_to(ec.chip, RIGHT, buff=0.3)
        u_ec = under(VGroup(*ec.text.submobjects[-4:]), ERR, 4)
        hc = note("a hard-coded string").next_to(ec.chip, DOWN, buff=0.22).align_to(ec.chip, RIGHT)
        trust = VGroup(fix_chip("trust docker ps"), fix_chip("trust the page's diagram")).arrange(RIGHT, buff=0.6)
        trust.move_to([-0.6, -0.25, 0])
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(rc, pic, cap2)), caption_extra(tr, True), run_time=0.5)
            type_extra(self, t, LOGS_GW, type_time=0.8)
            lg = t.print(self, [C34.line(2)], run_time=0.35)[0]
            vo.wait_until("still says open localhost 8090")
            src = substring(lg, OPEN_8090)
            u_lg = under(src, ERR, 3)
            pin(self, lg, u_lg, anim=Create(u_lg), run_time=0.4)
            self.play(src.animate.set_color(ERR), run_time=0.3)
            self.play(FadeIn(ec.chip[0]), FadeIn(ec.header), TransformFromCopy(src, ec.text), run_time=0.9)
            self.remove(ec.chip[0], ec.header, ec.text)
            self.add(ec)
            self.play(FadeIn(et, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("That text is hard-coded")
            self.play(Create(u_ec), FadeIn(hc, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Trust docker ps")
            self.play(FadeIn(trust[0], shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(trust[1], shift=UP * 0.1), run_time=0.4)

        # ============================================================ 4 · the processor's port: 9200 -> 9300
        net.shift(UP * (T7_TOP + 0.08 - outline.get_bottom()[1]))      # (off screen) back to the top
        ch380 = readme_chip("README.md · line 380", "Send a message from the browser. It should fail.", max_w=9.6)
        ch380.move_to([0, TOP - 0.25 - ch380.height / 2, 0])
        with self.voiceover(SAY[4]) as vo:
            resize(self, t, 7, keep=[], run_time=0.6,
                   extra=[FadeIn(net), FadeOut(VGroup(ec, et, u_ec, hc, trust)), tr.goto(2)])
            vo.wait_until("remove it")
            type_cmd(self, t, RM_PR, type_time=0.7)
            t.print(self, [C36.line(2)], run_time=0.3)
            backs_pr = self.fade_to_ghost(pr_owned, run_time=0.35)
            run2 = type_rows(self, t, RUN_9300P, type_time=1.0)
            t.print(self, [C37.line(3)], run_time=0.3)
            self.play(*[Transform(m, b) for m, b in zip(pr_owned, backs_pr)], run_time=0.35)
            pr_row = run2.rows[2]
            b93 = glyph_box(pr_row, "PORT=9300", CTR)
            pin(self, pr_row, b93, anim=AnimationGroup(Create(b93), net.set_room("processor", ":9300")),
                run_time=0.8)
            vo.wait_until("The README says")
            resize(self, t, 3, keep=[run2.rows[1], run2.rows[2], t.lines[-1]], run_time=0.7,
                   extra=[net.animate.shift(UP * up_low)])
            assert net.parts["laptop_label"].get_top()[1] < ch380.get_bottom()[1] - 0.1
            self.play(FadeIn(ch380, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("it should fail")
            # the gateway still aims at 9200: it turns RED as the README predicts the failure
            self.play(net.set_aim(None, ERR), run_time=0.6)
            self.play(flash_chip(net.aim_chip, ERR), run_time=0.7)

        # ============================================================ 5 · it fails quietly
        pg5 = place_page(PortPage(8095, reply=R32, compact=True, ports=True))
        er5 = tag2(["erratum · no error handling", "index.html lines 95–100"])
        er5.move_to([0, 0, 0]).shift([COL_L - er5.get_left()[0], COL_TOP - er5.get_top()[1], 0])
        nc5 = grey_tag("the page doesn't change").move_to([pg5.frame.get_center()[0], pg5.frame.get_bottom()[1], 0])
        rp5 = reply_strip(C38.line(3), color=ERR)
        rp5.shift(DOWN * (COL_TOP - (er5.get_bottom()[1] - 0.35)))
        assert rp5.frame.get_bottom()[1] > STRIP_TOP + 0.1
        assert nc5.get_bottom()[1] > STRIP_TOP + 0.08
        with self.voiceover(SAY[5]) as vo:
            self.play(LaggedStart(FadeOut(VGroup(net, ch380)), FadeIn(pg5, shift=LEFT * 0.15), lag_ratio=0.4),
                      run_time=0.8)
            vo.wait_until("It does, but quietly")
            self.play(pg5.click(), run_time=0.6)
            self.wait(0.4)
            vo.wait_until("The page has no error handling")
            self.play(FadeIn(er5, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("so nothing on it changes")
            self.play(FadeIn(nc5, shift=UP * 0.1), flash(pg5.reply_value.glyphs, S.GREY, 1.04), run_time=0.7)
            vo.wait_until("the captured request")
            self.play(FadeIn(rp5, shift=RIGHT * 0.15), run_time=0.6)
            self.play(flash(rp5.rows, ERR, 1.06), run_time=0.7)

        # ============================================================ 6 · the gateway's log: Connection refused
        cc = cheat_card()
        tick = check_mark(0.26, VENV)
        res = label("the name resolved", CAPTION, VENV)
        tick_g = VGroup(tick, res).arrange(RIGHT, buff=0.12)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(pg5, er5, nc5, rp5)), caption_extra(tr, True), run_time=0.5)
            resize(self, t, 11, keep=[], run_time=0.6)
            type_extra(self, t, LOGS_GW, type_time=0.7)
            body = [C39.line(2), C39.line(3), C39.line(4), C39.line(5), "…", C39.line(25), C39.line(26), "…",
                    C39.line(55)]
            out = t.print(self, body, wrap=True, run_time=0.8)
            assert len(t.lines) == 11, len(t.lines)
            l25, l26, ell2, l55 = out[-4], out[-3], out[-2], out[-1]
            assert l25.text == C39.line(25) and l55.text == C39.line(55)
            vo.wait_until("it found the processor by name")
            self.play(l25.glyphs.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("but the connection was refused")
            self.play(l55.glyphs.animate.set_color(ERR), run_time=0.5)
            self.play(flash(substring(l55, "Connection refused"), ERR, 1.08), run_time=0.6)
            vo.wait_until("nobody listens on 9200 anymore")
            resize(self, t, 4, keep=[l25, l26, ell2, l55], run_time=0.6)
            mid = (TOP + strip_top(4)) / 2
            cc.shift([COL_L - cc.frame.get_left()[0], mid - (cc.get_top()[1] + cc.get_bottom()[1]) / 2, 0])
            tick_g.next_to(cc.frame, RIGHT, buff=0.25).set_y(cc.row_a.get_center()[1])
            assert tick_g.get_right()[0] < 6.55 and cc.frame.get_bottom()[1] > t.box.get_top()[1] + 0.2
            self.play(FadeIn(cc.frame), FadeIn(cc.header), FadeIn(cc.row_a), run_time=0.5)
            self.play(Create(tick), FadeIn(res, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("A wrong name fails differently")
            self.play(FadeIn(cc.row_b, shift=UP * 0.1), run_time=0.5)

        # ============================================================ 7 · ponder: which setting?
        net.shift(UP * (T7_TOP + 0.08 - outline.get_bottom()[1]))      # (off screen) back to the top
        ch_gw = setting_chip("PROCESSOR_PORT=9200", "gateway")
        ch_pr = setting_chip("PORT=9300", "processor")
        y_ch = net.parts["outline"].get_bottom()[1] - 0.2 - ch_gw.chip.height / 2
        ch_gw.move_to([gw_box.frame.get_center()[0], 0, 0]).shift(UP * (y_ch - ch_gw.chip.get_center()[1]))
        ch_pr.move_to([pr_box.frame.get_center()[0], 0, 0]).shift(UP * (y_ch - ch_pr.chip.get_center()[1]))
        ch_pr.shift(LEFT * max(0, ch_pr.get_right()[0] - 6.45))
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(t, cc, tick_g)), caption_extra(tr, False), FadeIn(net), run_time=0.7)
            vo.wait_until("Which one setting")
            self.play(FadeIn(ch_gw, shift=UP * 0.1), FadeIn(ch_pr, shift=UP * 0.1), run_time=0.6)
            self.play(flash(pr_room, CTR, 1.2), flash_chip(net.aim_chip, ERR), run_time=0.8)
        pc = self.ponder_at("Which one setting fixes it?\nAnd does any image need rebuilding?", 6,
                            bottom=-3.45)
        assert pc.get_top()[1] < ch_gw.get_bottom()[1] - 0.05, (pc.get_top()[1], ch_gw.get_bottom()[1])

        # ============================================================ 8 · the fix: the gateway's PROCESSOR_PORT
        t8 = term(P_TOY, rows=7, title="laptop")
        # the checkpoint's commands (rm + the five rows) are not all in the strip: the ▶ sits on a card
        card8 = turn_card([RM_GW, "\n".join(RUN_9300G),
                           Prose("in your browser: open localhost:8090 and send a message")])
        for row in card8.rows[1][1:]:                    # the README's continuation rows keep their 2 spaces
            row.shift(RIGHT * 2 * cell_width(CAPTION))
        card8.shift([0 - card8.frame.get_center()[0], TOP - 0.05 - card8.get_top()[1], 0])
        assert card8.frame.get_bottom()[1] > STRIP_TOP + 0.15, card8.frame.get_bottom()[1]
        with self.voiceover(SAY[8], pad=1.0) as vo:
            self.play(FadeOut(pc), flash(ch_gw.chip, TURN, 1.12), tr.goto(3), run_time=0.7)
            self.play(FadeOut(VGroup(ch_gw, ch_pr)), FadeIn(t8, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Remove the gateway")
            type_cmd(self, t8, RM_GW, type_time=0.6)
            t8.print(self, [C41.line(2)], run_time=0.25)
            backs_gw = self.fade_to_ghost(gw_owned + door_owned, run_time=0.35)
            run3 = type_rows(self, t8, RUN_9300G, type_time=1.1)
            t8.print(self, [C42.line(6)], run_time=0.3)
            self.play(*[Transform(m, b) for m, b in zip(gw_owned + [d1, sl], backs_gw[:6])], run_time=0.4)
            pp_row = run3.rows[4]
            b_pp = glyph_box(pp_row, "PROCESSOR_PORT=9300", VENV)
            # "with 9300": the aim re-aims; "back on 8090": the slider slides back (lagged, one move)
            pin(self, pp_row, b_pp, run_time=1.2,
                anim=LaggedStart(AnimationGroup(Create(b_pp), net.set_aim("processor : 9300", LOOKUP),
                                                flash(pr_room, CTR, 1.2)),
                                 AnimationGroup(net.set_door("127.0.0.1:8090"), sl.knob.animate.set_x(sl.x0),
                                                Transform(net.parts["map"], backs_gw[6])),
                                 lag_ratio=0.5))
            vo.wait_until("and the message goes through")
            pg8 = place_page(PortPage(8090, reply=R43, compact=True, ports=True))
            rp8 = reply_strip(C43.line(2))
            keep = [run3.rows[2], run3.rows[3], run3.rows[4]]
            resize(self, t8, 3, keep=keep, run_time=1.0,
                   extra=[LaggedStart(FadeOut(net), AnimationGroup(FadeIn(pg8, shift=LEFT * 0.15),
                                                                   FadeIn(rp8, shift=RIGHT * 0.15)),
                                      lag_ratio=0.45)])
            lis = pg8.value("listen_port")
            self.play(pg8.port_lines[1].glyphs.animate.set_color(TURN),
                      substring(rp8.rows[2], '"listen_port": 9300,').animate.set_color(TURN), run_time=0.5)
            vo.wait_until("No image was rebuilt")
            nr = no_rebuild_chip()
            nr.shift([COL_L - nr.chip.get_left()[0], rp8.frame.get_bottom()[1] - 0.14 - nr.get_top()[1], 0])
            assert nr.get_bottom()[1] > STRIP_TOP + 0.08 and nr.get_right()[0] < pg8.frame.get_left()[0] - 0.1
            self.play(FadeIn(nr, shift=UP * 0.1), flash(lis, TURN, 1.2), run_time=0.6)
            vo.wait_until("Pause and fix yours")
            self.play(FadeOut(VGroup(pg8, rp8, nr)), FadeIn(card8, shift=UP * 0.15), run_time=0.6)

        # ============================================================ 9 · the two settings must agree
        g9 = setting_chip("PROCESSOR_PORT=9300", "gateway")
        p9 = setting_chip("PORT=9300", "processor")
        eq = mono("=", 40, VENV)
        row9 = VGroup(g9, eq, p9).arrange(RIGHT, buff=0.7)
        eq.match_y(g9.chip)
        row9.move_to([0, 1.2, 0])
        cap9 = note("the two settings must agree").next_to(row9, DOWN, buff=0.35)
        src9 = substring(pp_row, "PROCESSOR_PORT=9300")
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(card8), run_time=0.4)
            self.play(FadeIn(g9.chip[0]), TransformFromCopy(src9, g9.chip.text), FadeIn(g9.note),
                      FadeIn(p9, shift=UP * 0.1), run_time=0.8)
            self.remove(g9.chip[0], g9.chip.text, g9.note, p9)
            self.add(g9, p9)
            self.play(FadeIn(eq, scale=0.6), FadeIn(cap9, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the processor's PORT")
            self.play(flash(p9.chip, VENV, 1.1), run_time=0.6)
            vo.wait_until("and the gateway's processor port")
            self.play(flash(g9.chip, VENV, 1.1), run_time=0.6)

        # ============================================================ 10 · clean up before Compose
        ec10 = excerpt_chip(CONFLICT, "docker compose up · if the old containers remain (excerpt)", color=ERR,
                            frame=ERR, line=L68)
        cap10 = note("if you skip this: Compose wants these names")
        card10 = turn_card([RM_BOTH, NET_RM, (PS_A, "extra"), (NET_LS, "extra")])
        card10.shift([0 - card10.frame.get_center()[0], 0.3 - card10.frame.get_center()[1], 0])
        with self.voiceover(SAY[10], pad=1.2) as vo:
            strip = list(t8.lines.submobjects)          # the strip's rows leave with the chips
            self.play(FadeOut(VGroup(g9, p9, eq, cap9)), FadeOut(VGroup(*strip)), tr.goto(4), run_time=0.5)
            for ln in strip:
                t8.lines.remove(ln)
                self.remove(ln)
            resize(self, t8, 7, keep=[], run_time=0.6, extra=[FadeIn(net)])
            vo.wait_until("remove both containers")
            type_cmd(self, t8, RM_BOTH, type_time=0.7)
            t8.print(self, C44.at((2, 3)), run_time=0.3)
            self.play(*net.parts_out("boxes", "room_gateway", "room_processor", "plug_gateway", "plug_processor",
                                     "door", "slider", "map", "aim"), run_time=0.6)
            vo.wait_until("then the network")
            type_cmd(self, t8, NET_RM, type_time=0.6)
            t8.print(self, [C45.line(2)], run_time=0.25)
            self.play(*net.parts_out("rail", "rail_label"), run_time=0.5)
            vo.wait_until("An extra check")
            resize(self, t8, 10, keep=[], run_time=0.6, extra=[FadeOut(net), caption_extra(tr, True)])
            type_extra(self, t8, PS_A, type_time=0.5)
            ps_a = t8.print(self, C46.at(2, 3), wrap=True, run_time=0.4)
            type_extra(self, t8, NET_LS, type_time=0.6)
            nls = t8.print(self, C46.at((4, 7)), run_time=0.4)
            hw = next(r for r in ps_a if "hello-world" in r.text)
            b_hw = glyph_box(hw, "hello-world", TURN)
            no_tn = grey_tag("no toynet").next_to(nls[2], RIGHT, buff=0.5).set_y((nls[1].get_y() + nls[2].get_y()) / 2)
            no_tn.set_x(3.6)
            self.play(Create(b_hw), FadeIn(no_tn, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Skip this")
            ec10.shift([0 - ec10.chip.get_center()[0], (t8.box.get_top()[1] + 0.2) - ec10.chip.get_bottom()[1], 0])
            assert ec10.header.get_top()[1] < TOP, ec10.header.get_top()[1]
            cap10.move_to([0, 3.2, 0]).align_to([6.45, 0, 0], RIGHT)       # the top band, over the chip
            assert cap10.get_left()[0] > tr.get_right()[0] + 0.3
            self.play(FadeIn(ec10, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(cap10), flash(ec10.text, ERR, 1.04), run_time=0.6)
            vo.wait_until("Pause and clean up")
            self.play(FadeOut(VGroup(t8, b_hw, no_tn, ec10, cap10)), caption_extra(tr, False), run_time=0.4)
            self.play(FadeIn(card10, shift=UP * 0.15), run_time=0.5)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        self.wait(0.2)

