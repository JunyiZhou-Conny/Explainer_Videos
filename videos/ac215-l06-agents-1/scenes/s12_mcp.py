"""S12 · Tools you didn't write: MCP (lecture slides 51–53; dlops-io/llm-agent-google-adk
3-mcp-tools README "Install Node" / "Ask agent"; Colab · Cheese Quiz › Tools, MCP).

Beats (script.md "## S12", one voiceover block each):
0. LECTURE 51. No tracker. V7's three bins write in (slide 51, our words): "data · fetch",
   "action · change something", "orchestration · hand work to an agent". GREY tool chips drop in
   as each family is named: get_book_by_author, web_search, read_file -> data; finalize_itinerary
   and send_email (each with its GREY source tag "trip planner" / "newsletter" under it) ->
   action; research_facts, researcher_agent -> orchestration. The narrated examples light up
   YELLOW (get_book_by_author; finalize_itinerary, then send_email).
1. LECTURE 52. The bins leave; ServiceFan: one agent box with four tool pills, ten GREY wires fan
   out to ten service boxes ("email · SMTP/IMAP" … "messages · messaging API", no brands). A GREY
   caption "Do you see a problem?" under the agent. In the 5 s of silence after the SAY, a GREY
   "custom code" block grows on each wire, one after another, and the counter "10 integrations"
   ticks up from 0.
2. LECTURE 53. The custom blocks ripple once; then the wires, the blocks, the caption and the
   counter fade, the PINK trunk "same protocol" (a line, never a box) grows from the agent; the
   agent becomes the "MCP host" with PINK "clients" ports; an "MCP server" adapter clicks onto each
   service.
3. "same protocol" flashes PINK. The other seven services, their adapters and branches fade; the
   trunk splits into three separate PINK plugs, each its own connection from its own client port:
   "stdio · a child process", "HTTPS · a remote URL", "HTTP · a thread on :8001", while three
   service + adapter pairs (files, maps, chat: the same top-to-bottom order as their targets, so no
   pair crosses another) rise into the three servers (filesystem PURPLE, remote BLUE, FastMCP
   PURPLE); the label fades into the caption "one protocol · one connection per server". The
   lecture tag stays.
4. Plug 1 flashes YELLOW, then the picture and the lecture tag leave. TRACKER Mcp 1. A README card
   (3-mcp-tools/README.md · lines 56–63, tag expected), not typed: brew install node (macOS) ·
   sudo apt install nodejs npm (Ubuntu) · Windows: nodejs.org, a GREY chip under it "Ubuntu 22.04's
   apt Node is v12: too old for MCP servers · use nodejs.org (recorded with v24.22.0)", with a
   4-row strip (laptop · second terminal); on "Install Node" the strip types `node --version; npx
   --version` (tag extra) -> adk-laptop/34 lines 2–3, tag "at the time of recording". 2 s hold to
   read them.
5. The card and the strip leave. CODE(3-mcp-tools/agent.py: 20–29) at 20 pt in the left two
   thirds (header "3-mcp-tools/agent.py · lines 20–29 · your copy: mcp_tools/agent.py"; lines 24
   and 28 wrapped): lines 23–24 PURPLE as the server starts, line 28 YELLOW (tool_filter) at the
   end. Right third, on the GREY laptop: the PURPLE ADK process (MCPToolset), a PURPLE child
   process "npx … server-filesystem", and between them the PINK stdio pipe, a small envelope going
   down and back up.
6. The panel and the picture leave. The extra card "ask the agent's own toolset for its tools · no
   model involved" (top right) and a 4-row strip (laptop · second terminal) print adk-laptop/35
   lines 21 ("on stdio" PINK), 30 (folded at its last space, so the three names stay whole), 31
   cut after "14 [" + "…]". V7's sieve: 14 GREY tool
   chips fall onto `tool_filter` ("14" underlined YELLOW); write_file and edit_file flash and bounce
   off RED; list_directory, read_file, search_files pass GREEN (line 30 underlined GREEN).
   TRACKER Mcp 2: the sieve and the card leave; a GREY card "with your key:" — pick mcp_tools ·
   ask "List files in this directory" → a list_directory call in the Events tab, and the five
   entries below, plus [DIR] .adk (the session folder: picking the agent in the dev UI creates
   it, adk-laptop/29 line 42; capture 35 is a script run without it); the strip grows to 7 rows
   and prints lines 32 (cut), 33–37. 2 s hold to read them.
7. TRACKER CQ-Tools 1. A BLUE Colab frame (Cheese Quiz, illustration) in the left 10.25 units.
   RECORDED(c50: 3–6) small (name masked) + tag recorded · the staff's last saved run; caption
   "step 1: a Python function with @function_tool (cell 48)"; GREY chip "Colab disconnected? rerun
   Prerequisites first". TRACKER CQ-Tools 2: they leave; CODE(cell-54: 2, 10–13, 26–27) folded at
   20 pt (header "Cheese Quiz · cell 54 · lines 2–27 (folded)", URL masked; lines 2, 13, 26
   wrapped; line 17, a lone ")", folded away so 12 rows fit beside the picture): lines 11 and 13
   PINK; line 27 YELLOW with the YELLOW tag "not tools=". The picture: a short PINK HTTPS line from
   the frame's edge to a BLUE "remote MCP server" box at the top right.
8. The panel leaves; the Colab frame shrinks to the top left and the HTTPS line stretches across.
   Under it, the extra card as one row (common.extra_card's look) lists the four requests: a
   browser's plain GET · initialize · tools/list · tools/call, each lit YELLOW in turn. A 3-row
   strip (laptop · second terminal) prints
   mcp-remote/01 lines 2 and 10 (wrap; the glued "[exit 0]" marker dropped): HTTP/2 406 RED,
   "Client must accept text/event-stream" RED, while a GREY "GET" envelope bounces off the server
   (RED tag "406"). The strip leaves; three PINK envelopes travel the line (on "initialize", "list
   tools", "call"), each returning with an excerpt card below: initialize -> "protocolVersion":
   "2025-06-18" … "version":"1.16.0" (02 line 3); tools/list -> "name":"‹instructor›_fun_fact_mcp"
   (03 line 3); tools/call -> the "fact" text of 04 line 3, tag "your numbers will differ" + "a new
   fact each call". 1.5 s hold to read them.
9. TRACKER CQ-Tools 3. The picture and the cards leave; the Colab frame grows back.
   CODE(cell-57: 2, 5–6, 11, 14) folded (header "Cheese Quiz · cell 57 · lines 2–14 (folded)",
   subtitle "Build your own MCP Server (Optional)", names masked, line 11 without its emoji): line
   2 PURPLE (FastMCP), "in a background thread" underlined PURPLE, "port=8001" boxed GREEN; then
   "port 8000" in line 11 underlined RED with the GREY erratum chip "the comment says port 8000",
   and RECORDED(c57: 3) as a one-row output box, "8000" underlined RED, GREY tag "saved from an
   older version of the cell". Then the panel leaves: RECORDED(c59: 3–10) prints on the left
   (tag recorded · the staff's last saved run) beside the picture on the right: a PURPLE agent ·
   client and a PURPLE FastMCP thread on PINK 127.0.0.1:8001, inside the BLUE Colab VM, an
   envelope travelling between them; the three "Fun Fact Tool Called" rows flash PURPLE. No SAY
   covers the log, so it prints quickly (about 4 s after the voice).
10. The three plugs side by side (stacked rows): in each, a BLUE model chip only emits a small
   BLUE call card into a PURPLE client, and the clients do all the talking: PINK envelopes along
   the PINK lines (stdio, HTTPS, HTTP · :8001) to the servers. Then ▶ on a static GREY card (no
   GREY "your turn" header: the YELLOW ▶ tag says it, as on the other ▶ cards): no Node? brew
   install node · or nodejs.org · node --version; npx --version (extra) · dev UI: pick mcp_tools,
   ask "List files in this directory" (with your key) · Cheese Quiz › Tools, MCP: every cell (Build
   your own MCP Server is optional) · GREY "first run times out? warm the npx cache once:" ·
   npx -y @modelcontextprotocol/server-filesystem . (Ctrl+C, then retry; digest G12) · GOLD "OpenAI
   calls · paid". Hold 2 s; everything fades: empty frame.
"""

from contextlib import contextmanager

import common
import numpy as np
from common import (
    CLOUD,
    COST,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MASK,
    MCP_KEPT,
    NARRATION,
    P_ADK,
    SECOND,
    SERVICES,
    TOOL,
    TURN,
    CallCounter,
    Prose,
    ServiceFan,
    Sieve,
    ToolBins,
    _mono_rows,
    _with_header,
    beside,
    capture,
    card_rows,
    colab_frame,
    differ_tag,
    erratum_tag,
    excerpt,
    expected_tag,
    extra_tag,
    grey_tag,
    laptop_zone,
    lref,
    lref_swap,
    mini_envelope,
    model_chip,
    note,
    output_box,
    pin,
    readme_card,
    recording_tag,
    saved_run_tag,
    src_panel,
    strip_top,
    switch_section,
    term,
    tracker,
    turn_card,
    type_cmd,
    under,
    unname,
    your_copy,
    your_turn,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    FadeTransform,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    Transform,
    VGroup,
    Wiggle,
)

from explainer import style as S
from explainer.devops import (
    CAPTION,
    MONO,
    box,
    chip,
    label,
    mono,
    substring,
    tag,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S12"]
assert len(SAY) == 11, len(SAY)

# ------------------------------------------------------------------ the real captures and sources
NODE = capture("34", "adk-laptop")                  # extra: node and npx versions
assert NODE.cmd == "node --version; npx --version", NODE.cmd
assert NODE.at(2, 3) == ["v24.22.0", "11.19.1"], NODE.at(2, 3)

TS = capture("35", "adk-laptop")                    # extra: the agent's own toolset, no model
ON_STDIO = TS.line(21)
assert ON_STDIO == "Secure MCP Filesystem Server running on stdio", ON_STDIO
SEES = TS.line(30)
assert SEES == "tools the agent sees: ['list_directory', 'read_file', 'search_files']", SEES
_k30 = SEES.rfind(" ", 0, 66)                       # 69 characters: fold at the last space that fits,
SEES_ROWS = [SEES[:_k30], SEES[_k30 + 1:]]          # so the three kept names stay whole
assert SEES_ROWS == ["tools the agent sees: ['list_directory', 'read_file',", "'search_files']"], SEES_ROWS
OFFERS = TS.cut(31, "14 [") + "…]"
assert OFFERS == "tools the server offers: 14 […]", OFFERS
LISTED = TS.line(32)
assert LISTED.startswith("list_directory ") and LISTED.endswith("/mcp_tools ->"), LISTED
ENTRIES = TS.at((33, 37))
assert len(ENTRIES) == 5 and ENTRIES[1] == "[FILE] README.md", ENTRIES

GET = capture("01", "mcp-remote")                   # extra: what a browser's plain GET gets
GET_STATUS = GET.line(2).rstrip()
assert GET_STATUS == "HTTP/2 406", GET.line(2)
_g10 = GET.line(10)
assert _g10.endswith("}}[exit 0]"), _g10            # the output had no final newline: drop the marker
GET_BODY = _g10[:-len("[exit 0]")]
NOT_ACC = "Client must accept text/event-stream"
assert NOT_ACC in GET_BODY, GET_BODY
INIT = capture("02", "mcp-remote").line(3)          # extra: initialize
LIST = capture("03", "mcp-remote").line(3)          # extra: tools/list
CALL = capture("04", "mcp-remote").line(3)          # extra: tools/call
INIT_Q = ['"protocolVersion":"2025-06-18",', '… "version":"1.16.0"']
LIST_Q = ['"name":"' + MASK + '_fun_fact_mcp"']
CALL_Q = ['"fact":"Fresh cheeses (ricotta, chèvre) soften', 'but don’t stretch like mozzarella."']

C50 = capture("expected/colab-cheese-quiz-c50-tools-called.txt")
C50_ROWS = C50.at((3, 6))
assert C50_ROWS[0] == "Tools called:" and C50_ROWS[1].startswith("1. " + MASK), C50_ROWS
C57 = capture("expected/colab-cheese-quiz-c57-fastmcp-server.txt")
C57_ROW = C57.line(3)
assert C57_ROW == "FastMCP server starting on http://127.0.0.1:8000/mcp", C57_ROW
C59 = capture("expected/colab-cheese-quiz-c59-local-mcp.txt")
C59_ROWS = C59.at((3, 10))
assert C59_ROWS[0].endswith('"POST /mcp HTTP/1.1" 200 OK') and len(C59_ROWS) == 8, C59_ROWS
assert all(C59_ROWS[k] == MASK + " Fun Fact Tool Called" for k in (2, 4, 6)), C59_ROWS

AGENT = "llm-agent-google-adk/3-mcp-tools/agent.py"
assert excerpt(AGENT, 23, 23).strip() == "command='npx',"
assert excerpt(AGENT, 28, 28).strip().startswith("tool_filter=['read_file', 'list_directory'")
README = "llm-agent-google-adk/3-mcp-tools/README.md"
assert excerpt(README, 57, 57) == "brew install node" and excerpt(README, 60, 60) == "sudo apt install nodejs npm"
assert excerpt(README, 56, 56) == "# macOS" and excerpt(README, 59, 59) == "# Ubuntu"
assert excerpt(README, 63, 63) == "# Download from https://nodejs.org/"
CELL54 = "colab/cheese-quiz/cell-54.py"
assert excerpt(CELL54, 27, 27).strip() == "mcp_servers=mcp_servers,"
assert excerpt(CELL54, 17, 17).strip() == ")"      # the lone parenthesis the fold leaves out
CELL57 = "colab/cheese-quiz/cell-57.py"
assert excerpt(CELL57, 14, 14).strip() == 'mcp.run(transport="http", host="127.0.0.1", port=8001)'
SECTION57 = "Build your own MCP Server (Optional)"
assert "Build your own MCP Server" in excerpt("colab/cheese-quiz/cell-55.md", 1, 1)

assert excerpt(AGENT, 24, 24).strip().startswith("args=['-y', '@modelcontextprotocol/server-filesystem'")
WARM = "npx -y @modelcontextprotocol/server-filesystem ."    # digest G12: warm the npx cache once
NO_NODE = ("no Node?", "brew install node", "· or nodejs.org")   # README lines 57 and 63
TURN_ROWS = [
    NO_NODE,                                         # a serif + mono row: built in turn_card_tight()
    (NODE.cmd, "extra"),
    Prose("dev UI: pick mcp_tools, ask “List files in this directory” · with your key"),
    Prose("Cheese Quiz › Tools, MCP: every cell (Build your own MCP Server is optional)"),
    (Prose("first run times out? warm the npx cache once:"), S.GREY),
    (WARM, "Ctrl+C, then retry"),
    (Prose("OpenAI calls · paid"), COST),
]
# beat 4: the version the capture used, under the README card's apt line
APT_NOTE = (f"Ubuntu 22.04's apt Node is v12: too old for MCP servers · use nodejs.org "
            f"(recorded with {NODE.at(2, 3)[0]})")

# ------------------------------------------------------------------ layout
STRIP4_TOP = strip_top(4)
BINS_H = 2.5                       # tall enough for two chips with their source tags under them
BINS_Y = -0.75 - (BINS_H - 2.25) / 2   # the bins' centre (their top stays at y = 0.375)
PLUG_YS = (0.8, 0.0, -0.8)         # beat 3: the three plugs
X_HOST = -3.7                      # the host box's right edge (ServiceFan's agent box)
SRV_X0 = 3.15                      # the services' left edge (ServiceFan)
CF_TOP = 2.55                      # the Colab frame's top edge (its tab clears the tracker, as in S02)
PANEL_TOP = 2.15                   # a panel inside the Colab frame starts under the frame's tab
CF7_R = 3.45                       # beat 7: the Colab frame's right edge
SRV_BOX = (4.7, 6.5, 1.95)         # the remote server box: left, right, centre y (beats 7–8)
CF8_R = -1.6                       # beat 8: the shrunken frame's right edge
CF8_BOTTOM = 1.35
ROW_YS = (2.35, 1.53, 0.71)        # beat 10: the three plugs, stacked (the 7-row ▶ card fits under them)
KEEP = tuple(SERVICES.index(s) for s in ("files · File I/O", "maps · Maps API", "chat · chat API"))
# beat 3: the pairs that rise into the filesystem, remote and FastMCP servers. files must be one
# (filesystem); the other two sit below it, so the three keep their top-to-bottom order and no pair
# crosses another on its way up ("an API · REST" is above files: it would pass through it)


# ------------------------------------------------------------------ small helpers
def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def lag_play(scene, anims, owner=None, lag_ratio=0.3, run_time=1.0, extra=()):
    """Play a LaggedStart, then take its wrapper group off the scene. `owner` (the group that holds
    the animated members) goes on the scene first, so its members are never added on their own
    (a FadeIn starts them transparent)."""
    if owner is not None:
        scene.add(owner)
    g = LaggedStart(*anims, lag_ratio=lag_ratio)
    scene.play(g, *extra, run_time=run_time)
    unwrap(scene, [g])


def unwrap(scene, anims):
    """Put back in its place, member by member, the wrapper Group an AnimationGroup / LaggedStart
    added to the scene (Scene.add absorbed its members, so removing the wrapper alone would take
    them off the scene too). Nested groups as well."""
    for a in anims:
        if not isinstance(a, AnimationGroup):
            continue
        g = a.group
        if g in scene.mobjects:
            i = scene.mobjects.index(g)
            scene.mobjects[i:i + 1] = list(g.submobjects)
        unwrap(scene, a.animations)


def play_drop(scene, *anims, **kw):
    """scene.play, then unwrap the AnimationGroup / LaggedStart wrappers."""
    scene.play(*anims, **kw)
    unwrap(scene, anims)


def settle(scene, owner):
    """After its members were faded in one by one: keep only `owner` on the scene (its members
    would otherwise stay there on their own and come back after the owner fades out)."""
    fam = set(owner.get_family())
    scene.mobjects = [m for m in scene.mobjects if m not in fam]
    scene.add(owner)


def mixed_row(words, size=CAPTION):
    """One card row of serif words with a mono command among them: (serif, `mono`, serif)."""
    a, cmd, b = words
    return VGroup(label(a, size, INK), mono(cmd, size, INK), label(b, size, INK)).arrange(RIGHT, buff=0.15)


def turn_card_tight(rows, buff=0.15):
    """common.turn_card's static ▶ card (no GREY header: the YELLOW ▶ tag says "your turn") with its
    rows closer together than turn_card's fixed 0.2, so seven rows fit under beat 10's plug rows; a
    row may also be a (serif, mono, serif) triple, which turn_card's rows cannot hold. Every other
    row is built by turn_card itself. .frame .rows .tag"""
    items = VGroup()
    for r in rows:
        if isinstance(r, tuple) and len(r) == 3:
            items.add(mixed_row(r))
            continue
        c = turn_card([r], header=None)
        m = c.rows[0]
        c.rows.remove(m)
        items.add(m)
    items.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    fr = box(items.width + 0.6, items.height + 0.6, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    items.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    tg = your_turn().move_to(fr.get_corner(UP + RIGHT)).shift(LEFT * 1.0)
    g = VGroup(fr, items, tg)
    g.frame, g.rows, g.tag = fr, items, tg
    return g


def explode(scene, group):
    """Take a VGroup's members onto the scene as separate mobjects (so each can morph or fade on
    its own without the group snapping it back later). Returns the members."""
    mems = list(group.submobjects)
    scene.remove(group)
    for m in mems:
        group.remove(m)
    scene.add(*mems)
    return mems


def text_box(rows, color, w=None, h=None, size=CAPTION, fill=0.12, stroke=2.5):
    """A rounded box in `color` holding rows of text: "`mono`" rows in mono, the rest sans/serif
    (a (text, colour) pair colours one row). .frame .rows"""
    items = VGroup()
    for r in rows:
        s, col = (r, INK) if isinstance(r, str) else r
        if len(s) > 1 and s.startswith("`") and s.endswith("`"):
            items.add(mono(s[1:-1], size, col))
        else:
            items.add(label(s, size, col))
    items.arrange(DOWN, buff=0.08)
    fr = box(max(w or 0, items.width + 0.4), max(h or 0, items.height + 0.3), color, fill=color,
             fill_opacity=fill, radius=0.12, stroke=stroke)
    items.move_to(fr)
    g = VGroup(fr, items)
    g.frame, g.rows = fr, items
    return g


def quote_card(rows, header, line, size=CAPTION):
    """An excerpt card of one or two rows: each row (a leading '…' marks skipped text) must be an
    exact sub-string of `line`; two rows without '…' must also be adjacent in it. GREY frame, mono
    rows, a GREY header above. .frame .rows .header"""
    src = unname(line)
    pieces = [r.lstrip("…").strip() for r in rows]
    for p in pieces:
        assert p and p in src, (p, src[:120])
    if len(rows) == 2 and not rows[1].startswith("…"):
        assert " ".join(pieces) in src, " ".join(pieces)
    rs = _mono_rows(rows, size, INK)
    fr = box(rs.width + 0.5, rs.height + 0.34, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.1)
    fr.move_to(rs)
    hd = note(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.08)
    g = VGroup(fr, rs, hd)
    g.frame, g.rows, g.header = fr, rs, hd
    return g


def req_strip():
    """Beat 8's extra card as one row (common.extra_card's look): the four requests, the `extra` tag
    and "an extra check · in the study guide" above. .items (lit one by one) .frame .header"""
    items = [label("a browser's plain GET", CAPTION, INK)] + \
        [mono(s, CAPTION, INK) for s in ("initialize", "tools/list", "tools/call")]
    row = []
    for k, it in enumerate(items):
        if k:
            row.append(label("·", CAPTION, S.GREY))
        row.append(it)
    r = VGroup(*row).arrange(RIGHT, buff=0.22)
    fr = box(r.width + 0.6, r.height + 0.36, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    r.move_to(fr)
    hd = VGroup(extra_tag(), note("an extra check · in the study guide")).arrange(RIGHT, buff=0.2)
    hd.next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, r, hd)
    g.items, g.frame, g.header = items, fr, hd
    return g


def call_glyph(color=CLOUD):
    """The model's call as a small BLUE card ({…}): it only writes calls."""
    t = mono("{…}", CAPTION, INK)
    fr = box(t.width + 0.3, t.height + 0.2, color, fill=color, fill_opacity=0.25, radius=0.08)
    t.move_to(fr)
    return VGroup(fr, t)


def solid_bar(p, lines, color, opacity):
    """One translucent bar over all the rows of the given (adjacent) file lines of a src_panel.
    p.bar() draws a bar per row, and on a wrapped line the neighbouring bars overlap in a brighter
    seam; this spans the same rows in a single rectangle."""
    rows = VGroup(*[b for n in lines for b in p.bar(n, color, opacity)])
    top, bot = rows.get_top()[1], rows.get_bottom()[1]
    r = Rectangle(width=rows.width, height=top - bot, stroke_width=0).set_fill(color, opacity)
    return r.move_to([rows.get_center()[0], (top + bot) / 2, 0])


def code_row(p, n, k=0):
    """The k-th code row of file line n in a src_panel."""
    return p.code.code_lines[p.rows_of(n)[k]]


def span_box(span, color, buff=0.06, stroke=3):
    return box(span.width + 2 * buff + 0.08, span.height + 2 * buff + 0.06, color, fill_opacity=0.08,
               radius=0.06, stroke=stroke).move_to(span)


@contextmanager
def drop_chars(chars):
    """cell-57 line 11 starts with the ZWJ emoji 🏃‍♀️: common.strip_emoji drops the runner and the
    joiners but keeps the ♀ (the mono font has that glyph), which is not part of the line's text.
    Drop it too while that panel is built (script.md: line 11 printed without its emoji)."""
    orig = common.dropped_chars

    def patched(s):
        return sorted(set(orig(s)) | ({c for c in chars if c in s} if orig(s) else set()))
    common.dropped_chars = patched
    try:
        yield
    finally:
        common.dropped_chars = orig


def plug_row(model, client, transport, server, srv_color, y):
    """Beat 10: one plug as a row: BLUE model chip | PURPLE client | PINK line + transport | server.
    .model .client .line .label .server .y"""
    m = model_chip(model)
    place(m, left=-6.45, cy=y)
    c = text_box([client], TOOL, w=2.4, h=0.5)
    place(c, left=-3.75, cy=y)
    s = text_box([server], srv_color, w=4.2, h=0.5)
    place(s, right=6.45, cy=y)
    ar = Line([m.get_right()[0] + 0.1, y, 0], [c.get_left()[0] - 0.1, y, 0], color=S.GREY, stroke_width=2)
    ln = Line([c.get_right()[0], y, 0], [s.get_left()[0], y, 0], color=LOOKUP, stroke_width=4)
    lb = label(transport, CAPTION, LOOKUP).next_to(ln, UP, buff=0.06)
    g = VGroup(m, ar, c, ln, lb, s)
    g.model, g.arrow, g.client, g.line, g.label, g.server, g.y = m, ar, c, ln, lb, s, y
    return g


class McpPlugs(VoiceScene):
    def construct(self):
        # ============================================================ 0 · three families (slide 51)
        with self.voiceover(SAY[0]) as vo:
            ref = lref("51")
            bins = ToolBins(bin_h=BINS_H)
            bins.shift(UP * (BINS_Y - bins.bin("data").shape.get_center()[1]))
            names = ("data", "action", "orchestration")
            self.play(FadeIn(ref), run_time=0.4)
            lag_play(self, [FadeIn(bins.bin(n), shift=UP * 0.2) for n in names], owner=bins,
                     lag_ratio=0.35, run_time=1.6)

            def fresh(name):
                return chip(name, S.GREY, size=CAPTION, font=MONO)

            d_chips = [fresh(n) for n in ("get_book_by_author", "web_search", "read_file")]
            a_chips = []
            for n, src in (("finalize_itinerary", "trip planner"), ("send_email", "newsletter")):
                c = fresh(n)
                tg = tag(src, S.GREY, size=CAPTION).next_to(c, DOWN, buff=0.06)
                a_chips.append(VGroup(c, tg))
            o_chips = [fresh(n) for n in ("research_facts", "researcher_agent")]
            start_y = bins.get_top()[1] + 0.2
            for grp, nm in ((d_chips, "data"), (a_chips, "action"), (o_chips, "orchestration")):
                y = start_y
                for c in grp:                       # a column above the bin, first chip lowest
                    c.move_to([bins.bin(nm).shape.get_center()[0], y + c.height / 2, 0])
                    y += c.height + 0.12
            # the action bin holds two chips with their source tags under them (own slots)
            a_shape = bins.bin("action").shape
            a_top = a_shape.get_top()[1] - 0.12
            a_ys = [a_top - a_chips[0].height / 2, a_top - a_chips[0].height * 1.5 - 0.14]

            def drop_in(nm, grp, ys=None):
                anims = []
                for k, c in enumerate(grp):
                    if ys is None:
                        anims.append(bins.drop(c, nm))
                    else:
                        anims.append(c.animate.move_to([a_shape.get_center()[0], ys[k], 0]))
                title = bins.bin(nm).title[0]
                self.play(Indicate(title, color=TURN, scale_factor=1.15),
                          *[FadeIn(c, shift=DOWN * 0.25) for c in grp], run_time=0.6)
                lag_play(self, anims[::-1], lag_ratio=0.25, run_time=0.9)   # lowest chip first: no crossing

            vo.wait_until("Data tools fetch")
            drop_in("data", d_chips)
            vo.wait_until("like our book searches")        # the narrated example lights up
            self.play(Indicate(d_chips[0], color=TURN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("action tools change")
            drop_in("action", a_chips, a_ys)
            vo.wait_until("like finalizing a trip")
            self.play(Indicate(a_chips[0], color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("or sending email")
            self.play(Indicate(a_chips[1], color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("orchestration tools hand")
            drop_in("orchestration", o_chips)

        # ============================================================ 1 · ten wires (slide 52)
        fan = ServiceFan(show=("agent", "pills"))
        ask = label("Do you see a problem?", 22, S.GREY)
        ask.move_to([fan.agent_frame.get_center()[0], fan.agent_frame.get_bottom()[1] - 0.45, 0])
        counter = CallCounter(0, unit="integration", color=INK)
        counter.move_to(ask.get_center() + DOWN * 0.6)
        with self.voiceover(SAY[1]) as vo:
            ref52 = lref("52")
            self.play(FadeOut(bins), *[FadeOut(c) for c in d_chips + a_chips + o_chips], FadeOut(ref),
                      FadeIn(ref52), run_time=0.5)
            ref = ref52
            self.play(FadeIn(fan), run_time=0.6)
            play_drop(self, *fan.parts_in("wires", anim=lambda m: LaggedStart(*[Create(w) for w in m],
                                                                                lag_ratio=0.12)),
                      *fan.parts_in("services", anim=lambda m: LaggedStart(
                          *[FadeIn(s, shift=LEFT * 0.2) for s in m], lag_ratio=0.12)),
                      run_time=2.0)
            vo.wait_until("The lecture asks")
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.6)
        # 5 s of silence: a custom block on every wire, the counter ticks to 10
        self.play(FadeIn(counter), run_time=0.3)
        play_drop(self, LaggedStart(*[fan.custom_in(i) for i in range(10)], lag_ratio=0.4),
                  counter.count_to(10, run_time=4.0), run_time=4.0)
        self.wait(0.7)

        # ============================================================ 2 · MCP (slide 53)
        customs = fan.parts["customs"]
        with self.voiceover(SAY[2]) as vo:
            ref = lref_swap(self, ref, "53", run_time=0.4)
            play_drop(self, LaggedStart(*[Indicate(c, color=ERR, scale_factor=1.12) for c in customs],
                                        lag_ratio=0.08),
                      Indicate(counter, color=ERR, scale_factor=1.1), run_time=1.4)
            vo.wait_until("MCP, the Model")
            play_drop(self, *fan.parts_out("wires", "customs"), FadeOut(ask), FadeOut(counter),
                      *fan.parts_in("trunk", anim=lambda m: LaggedStart(
                          Create(m[0]), LaggedStart(*[Create(b) for b in m[1]], lag_ratio=0.05),
                          FadeIn(m[2]), lag_ratio=0.4)),
                      run_time=1.4)
            vo.wait_until("a host with clients")
            self.play(*fan.parts_in("host"), run_time=0.7)
            vo.wait_until("and an MCP server for each")
            play_drop(self, *fan.parts_in("adapters", anim=lambda m: LaggedStart(
                *[FadeIn(a, scale=1.3) for a in m], lag_ratio=0.1)), run_time=1.3)

        # ============================================================ 3 · one connection per server
        with self.voiceover(SAY[3]) as vo:
            trunk_line, branches, same = fan.parts["trunk"].submobjects
            vo.wait_until("is a shared protocol")
            self.play(Indicate(same, color=LOOKUP, scale_factor=1.25), Wiggle(trunk_line, scale_value=1.05),
                      run_time=1.0)
            vo.wait_until("In code, each server")
            # take the fan apart: each piece morphs or fades on its own from here on
            parts = {n: fan.parts[n] for n in ("agent", "pills", "services", "wires", "customs", "host",
                                                "trunk", "adapters")}
            self.remove(fan)
            for part in parts.values():
                fan.remove(part)
            self.add(*[parts[n] for n in ("agent", "pills", "services", "host", "trunk", "adapters")])
            cover, host_t, ports, clients = explode(self, parts["host"])
            explode(self, parts["trunk"])
            adapters = explode(self, parts["adapters"])
            services = explode(self, parts["services"])
            twigs = explode(self, branches)
            new_ports = VGroup(*[Dot(radius=0.07, color=LOOKUP).move_to([X_HOST, y, 0]) for y in PLUG_YS])
            plugs = VGroup(*[Line([X_HOST, y, 0], [SRV_X0, y, 0], color=LOOKUP, stroke_width=4)
                             for y in PLUG_YS])
            srv_specs = (("MCP server · filesystem", TOOL), ("MCP server · remote", CLOUD),
                         ("MCP server · FastMCP", TOOL))
            servers = VGroup(*[text_box([(t, INK)], c, w=3.4, h=0.5).move_to([4.85, y, 0])
                               for (t, c), y in zip(srv_specs, PLUG_YS)])
            p_labels = VGroup(*[label(t, CAPTION, LOOKUP).next_to(plugs[k], UP, buff=0.06)
                                for k, t in enumerate(("stdio · a child process", "HTTPS · a remote URL",
                                                       "HTTP · a thread on :8001"))])
            cap3 = label("one protocol · one connection per server", 22, S.GREY)
            cap3.move_to([0.4, -1.75, 0])
            # first the seven services the tutorial does not use leave, with their adapters and branches
            others = [k for k in range(len(services)) if k not in KEEP]
            self.play(*[FadeOut(m) for k in others for m in (adapters[k], services[k], twigs[k])],
                      run_time=0.7)
            # then the trunk splits into three plugs, and each kept service with its adapter rises
            # into its server: the service's frame becomes the server's frame, its name fades into
            # the server's name (same size: no glyph scramble), and the "MCP server" adapter slides
            # in onto the words "MCP server" of that name
            pieces = [trunk_line.copy() for _ in PLUG_YS]
            self.remove(trunk_line)
            self.add(*pieces)
            morph = [ReplacementTransform(p, q) for p, q in zip(pieces, plugs)]
            for k, srv_k in zip(KEEP, servers):
                s_box, s_lab = explode(self, services[k])
                words = srv_k.rows.get_left() + RIGHT * adapters[k][1].width / 2
                morph += [FadeOut(twigs[k]), ReplacementTransform(s_box, srv_k.frame),
                          FadeTransform(s_lab, srv_k.rows, stretch=False),
                          FadeOut(adapters[k], target_position=words)]
            self.play(*morph, ReplacementTransform(ports, new_ports),
                      FadeTransform(same, cap3, stretch=False), run_time=1.4)
            lag_play(self, [FadeIn(lb, shift=UP * 0.1) for lb in p_labels], lag_ratio=0.35, run_time=1.2)
        plug_pic = VGroup(parts["agent"], parts["pills"], cover, host_t, clients, new_ports, plugs, servers,
                          p_labels, cap3)

        # ============================================================ 4 · plug 1: install Node
        rd_rows = [VGroup(mono("brew install node", CAPTION, INK), note("(macOS)")).arrange(RIGHT, buff=0.25),
                   VGroup(mono("sudo apt install nodejs npm", CAPTION, INK), note("(Ubuntu)")).arrange(RIGHT, buff=0.25),
                   label("Windows: nodejs.org", CAPTION, INK)]
        rd = readme_card("3-mcp-tools/README.md · lines 56–63", rd_rows)
        ex = expected_tag().next_to(rd.header, RIGHT, buff=0.25)
        rd.add(ex)
        place(rd, cx=0, top=2.05)
        # a viewer on Ubuntu 22.04 (WSL too) gets Node 12 from apt: too old for the MCP servers
        apt = chip(APT_NOTE, S.GREY, size=CAPTION, fill_opacity=0.08)
        place(apt, cx=0, top=rd.frame.get_bottom()[1] - 0.2)
        assert apt.get_bottom()[1] > STRIP4_TOP + 0.12 and apt.width < 12.8, (apt.get_bottom(), apt.width)
        with self.voiceover(SAY[4]) as vo:
            self.play(Indicate(plugs[0], color=TURN, scale_factor=1.0), Indicate(p_labels[0], color=TURN),
                      run_time=0.7)
            tr = tracker("Mcp", 1)
            self.play(FadeOut(plug_pic), FadeOut(ref), FadeIn(tr, shift=DOWN * 0.25), run_time=0.6)
            t4 = term(P_ADK, rows=4, title=SECOND, top=STRIP4_TOP)
            self.play(FadeIn(rd, shift=DOWN * 0.15), FadeIn(t4, shift=UP * 0.3), run_time=0.5)
            self.play(FadeIn(apt, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Install Node")
            cmd = type_cmd(self, t4, NODE.cmd)
            pin(self, cmd, beside(extra_tag(), t4, cmd), run_time=0.3)
            out = t4.print(self, NODE.at(2, 3), run_time=0.4)
            pin(self, out[0], beside(recording_tag(), t4, out[0]), run_time=0.3)
        self.wait(2.0)                    # the two versions, their tag and the apt note stay up to be read

        # ============================================================ 5 · plug 1: the stdio child process
        pa = src_panel(AGENT, 20, 29, size=20, wrap={24: ["/server-filesystem'"], 28: ["'list_directory'"]})
        _with_header(pa, "3-mcp-tools/agent.py · lines 20–29", subtitle=your_copy(AGENT))
        place(pa, left=-6.5, top=2.6)
        bars_npx = solid_bar(pa, (23, 24), TOOL, 0.22)
        bar_tf = solid_bar(pa, (28,), TURN, 0.22)
        zl, zr = pa.code.get_right()[0] + 0.25, 6.5
        z_top = pa.code.get_top()[1]
        zone = laptop_zone(zr - zl, z_top + 3.35, caption="your laptop")
        place(zone, left=zl, top=z_top)
        zc = (zl + zr) / 2
        adk = text_box(["ADK process", "`MCPToolset`"], TOOL, w=zr - zl - 0.5).move_to([zc, 1.3, 0])
        kid = text_box([("child process", S.GREY), "`npx …`", "`server-filesystem`"], TOOL,
                       w=zr - zl - 0.5).move_to([zc, -1.55, 0])
        pipe = Line(adk.get_bottom() + DOWN * 0.05, kid.get_top() + UP * 0.05, color=LOOKUP, stroke_width=8)
        pipe_l = label("stdio", 22, LOOKUP).next_to(pipe, RIGHT, buff=0.36)   # clear of the envelope
        env5 = mini_envelope(None, LOOKUP, w=0.42).move_to(pipe.get_top() + DOWN * 0.3)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(rd), FadeOut(apt), FadeOut(t4), run_time=0.4)
            self.play(FadeIn(pa, shift=UP * 0.15), FadeIn(zone), FadeIn(adk, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("starts a filesystem server")
            self.play(FadeIn(bars_npx), run_time=0.5)
            self.play(FadeIn(kid, shift=DOWN * 0.3), run_time=0.7)
            vo.wait_until("as a child process")
            self.play(Indicate(kid.rows[0], color=TOOL, scale_factor=1.15), run_time=0.7)
            vo.wait_until("talking over standard")
            self.play(Create(pipe), FadeIn(pipe_l), run_time=0.7)
            self.play(FadeIn(env5, scale=0.6), run_time=0.2)
            self.play(env5.animate.move_to(pipe.get_bottom() + UP * 0.3), run_time=0.8)
            self.play(env5.animate.move_to(pipe.get_top() + DOWN * 0.3), run_time=0.8)
            self.play(FadeOut(env5, scale=0.6), FadeIn(bar_tf), run_time=0.5)

        # ============================================================ 6 · the toolset's own list; the sieve
        xc = card_rows(["“ask the agent's own toolset for its tools · no model involved”"])
        xh = VGroup(extra_tag(), note("an extra check · in the study guide")).arrange(RIGHT, buff=0.2)
        xh.next_to(xc.frame, UP, buff=0.08).align_to(xc.frame, LEFT).shift(RIGHT * 0.1)
        xc.add(xh)
        place(xc, right=6.5, top=3.55)
        t6 = term(P_ADK, rows=4, title=SECOND)
        sv = Sieve()
        place(sv, cx=0, top=xc.frame.get_bottom()[1] - 0.15)
        # the `tool_filter` label sits under the mesh's right end, where sift() puts the kept row:
        # move it to the right of that row (same arithmetic as Sieve.sift)
        kept_w = VGroup(*[sv.chips[n].copy() for n in MCP_KEPT]).arrange(RIGHT, buff=0.3).width
        tf_lab = sv.parts["sieve"][1]
        tf_lab.move_to([sv.mesh.get_center()[0] + kept_w / 2 + 0.35 + tf_lab.width / 2,
                        sv.mesh.get_bottom()[1] - 0.6, 0])
        assert tf_lab.get_right()[0] < 6.5, tf_lab.get_right()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(pa), FadeOut(bars_npx), FadeOut(bar_tf), FadeOut(zone), FadeOut(adk),
                      FadeOut(kid), FadeOut(pipe), FadeOut(pipe_l), run_time=0.5)
            self.play(FadeIn(xc, shift=DOWN * 0.15), FadeIn(t6, shift=UP * 0.3), run_time=0.6)
            r21 = t6.print(self, [ON_STDIO], run_time=0.4)
            self.play(substring(r21[0], "on stdio").animate.set_color(LOOKUP), run_time=0.3)
            r30 = t6.print(self, SEES_ROWS, run_time=0.4)
            r31 = t6.print(self, [OFFERS], run_time=0.3)
            vo.wait_until("The server offers 14")
            u14 = under(substring(r31[0], "14"), TURN)
            self.play(FadeIn(sv.parts["chips"], shift=DOWN * 0.3), Create(u14), run_time=0.6)
            self.play(FadeIn(sv.parts["sieve"]), run_time=0.4)
            self.add(sv)
            self.play(*sv.fall(), run_time=0.7)
            vo.wait_until("including write and edit")
            self.play(*[Indicate(sv.chips[n], color=ERR, scale_factor=1.12) for n in ("write_file", "edit_file")],
                      run_time=0.7)
            vo.wait_until("and the filter lets three")
            self.play(*sv.sift(), run_time=1.0)
            u30 = VGroup(*[under(r, DATA) for r in r30])
            self.play(Create(u30), run_time=0.4)
            vo.wait_until("With your key")
            # the narrated card first (over the 7-row terminal's top edge), then the entries it names
            key = card_rows([
                VGroup(label("pick", CAPTION, INK), mono("mcp_tools", CAPTION, INK),
                       label("· ask “List files in this directory”", CAPTION, INK)).arrange(RIGHT, buff=0.12),
                VGroup(label("→ a", CAPTION, INK), mono("list_directory", CAPTION, INK),
                       label("call in the Events tab,", CAPTION, INK)).arrange(RIGHT, buff=0.12),
                # picking the agent creates its session folder first (adk-laptop/29 line 42 for
                # baseline): your listing has a sixth entry that the script run below does not
                VGroup(label("and the five entries below, plus", CAPTION, INK), mono("[DIR] .adk", CAPTION, INK),
                       label("(the session folder)", CAPTION, INK)).arrange(RIGHT, buff=0.12),
            ], header="with your key:")
            place(key, left=-6.4, bottom=strip_top(7) + 0.2)
            self.play(tr.goto(2), FadeOut(sv), FadeOut(xc), FadeOut(u14), FadeOut(u30), run_time=0.5)
            self.play(FadeIn(key, shift=DOWN * 0.15), run_time=0.5)
            common.resize(self, t6, 7, run_time=0.5)
            assert abs(t6.box.get_top()[1] - strip_top(7)) < 0.02, t6.box.get_top()
            t6.print(self, [LISTED] + ENTRIES, run_time=0.6)
        self.wait(2.0)                    # the card and the five entries stay up to be read

        # ============================================================ 7 · plug 2: a remote server by URL
        w7 = CF7_R + 6.5
        cf = colab_frame("Cheese Quiz", width=w7, top=CF_TOP)
        cf.shift(RIGHT * (CF7_R - cf.frame.get_right()[0]))
        ob = output_box(C50_ROWS, header="Cheese Quiz · cell 50 · output")
        sv50 = saved_run_tag().next_to(ob.header, RIGHT, buff=0.25)
        g50 = VGroup(ob, sv50)
        place(g50, left=-6.1, top=PANEL_TOP - 0.1)
        step1 = VGroup(note("step 1: a Python function with"), mono("@function_tool", CAPTION, S.GREY),
                       note("(cell 48)")).arrange(RIGHT, buff=0.12)
        place(step1, left=-6.0, top=ob.frame.get_bottom()[1] - 0.25)
        disc = chip("Colab disconnected? rerun Prerequisites first", S.GREY, size=CAPTION, fill_opacity=0.08)
        place(disc, left=-6.0, top=step1.get_bottom()[1] - 0.45)
        p54 = src_panel(CELL54, [2, (10, 13), (26, 27)], size=20,
                        wrap={2: ['"https'], 13: ["# MCP"], 26: ["mcp_servers (not"]})
        _with_header(p54, "Cheese Quiz · cell 54 · lines 2–27 (folded)")
        place(p54, left=-6.2, top=PANEL_TOP)
        pink = VGroup(p54.bar(11, LOOKUP, 0.3), solid_bar(p54, (13,), LOOKUP, 0.3))
        yel = p54.bar(27, TURN, 0.22)
        nt = tag("not tools=", TURN, size=CAPTION)
        r27 = code_row(p54, 27)
        nt.next_to(r27, RIGHT, buff=0.4)
        sl, sr, sy = SRV_BOX
        srv = text_box(["remote", "MCP server"], CLOUD, w=sr - sl, h=1.0).move_to([(sl + sr) / 2, sy, 0])
        https7 = Line([CF7_R, sy, 0], [sl, sy, 0], color=LOOKUP, stroke_width=4)
        https_l = label("HTTPS", CAPTION, LOOKUP).next_to(https7, UP, buff=0.08)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(t6), FadeOut(key), run_time=0.4)
            tr = switch_section(self, tr, "CQ-Tools", 1, run_time=0.6)
            self.play(FadeIn(cf), run_time=0.5)
            vo.wait_until("After a first tool")
            self.play(FadeIn(g50, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(step1, shift=UP * 0.1), FadeIn(disc, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the notebook connects")
            self.play(tr.goto(2), FadeOut(g50), FadeOut(step1), FadeOut(disc), run_time=0.5)
            self.play(FadeIn(p54, shift=UP * 0.15), FadeIn(srv, shift=LEFT * 0.2), run_time=0.6)
            self.play(Create(https7), FadeIn(https_l), FadeIn(pink), run_time=0.6)
            vo.wait_until("passed as MCP servers")
            self.play(FadeIn(yel), FadeIn(nt, shift=LEFT * 0.15), run_time=0.6)

        # ============================================================ 8 · four requests, with curl
        cf8 = colab_frame("Cheese Quiz", width=CF8_R + 6.5, top=CF_TOP, bottom=CF8_BOTTOM)
        cf8.shift(RIGHT * (CF8_R - cf8.frame.get_right()[0]))
        https8 = Line([CF8_R, sy, 0], [sl, sy, 0], color=LOOKUP, stroke_width=4)
        https8_l = label("HTTPS", CAPTION, LOOKUP).next_to(https8, UP, buff=0.2)   # the envelopes pass under it
        req = req_strip()
        place(req, left=-6.4, top=CF8_BOTTOM - 0.12)
        t8 = term(P_ADK, rows=3, title=SECOND)
        q_init = quote_card(INIT_Q, "initialize · reply (excerpt)", INIT)
        q_list = quote_card(LIST_Q, "tools/list · reply (excerpt)", LIST)
        q_call = quote_card(CALL_Q, "tools/call · reply (excerpt)", CALL)
        place(q_init, left=-6.4, top=req.frame.get_bottom()[1] - 0.3)
        place(q_list, left=q_init.get_right()[0] + 0.4, top=q_init.get_top()[1])
        place(q_call, left=-6.4, top=q_init.get_bottom()[1] - 0.2)
        dif = VGroup(differ_tag(), note("a new fact each call")).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        place(dif, left=q_call.get_right()[0] + 0.35, cy=q_call.frame.get_center()[1])
        assert q_list.get_right()[0] < 6.5 and dif.get_right()[0] < 6.5 and q_call.get_bottom()[1] > -3.5
        a_pt, b_pt = np.array([CF8_R + 0.35, sy, 0]), np.array([sl - 0.35, sy, 0])
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(p54), FadeOut(pink), FadeOut(yel), FadeOut(nt), run_time=0.4)
            self.play(Transform(cf, cf8), Transform(https7, https8), Transform(https_l, https8_l), run_time=1.0)
            self.play(FadeIn(req, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("A browser's plain request")
            self.play(FadeIn(t8, shift=UP * 0.3), req.items[0].animate.set_color(TURN), run_time=0.5)
            env_g = mini_envelope("GET", S.GREY, w=0.45)
            env_g.move_to(a_pt + DOWN * 0.2)
            self.play(FadeIn(env_g, scale=0.6), run_time=0.25)
            self.play(env_g.animate.move_to(b_pt + DOWN * 0.2), run_time=0.8)
            st = t8.print(self, [(GET_STATUS, ERR)], run_time=0.3)
            r406 = tag("406", ERR, size=CAPTION).next_to(srv, DOWN, buff=0.15)
            self.play(FadeIn(r406, scale=1.3), env_g.animate.move_to(a_pt + DOWN * 0.2).set_color(ERR),
                      run_time=0.8)
            vo.wait_until("the server is up")
            body = t8.print(self, [GET_BODY], wrap=True, run_time=0.4)
            hit = [r for r in body if NOT_ACC in r.text]
            assert hit, [r.text for r in body]
            self.play(substring(hit[0], NOT_ACC).animate.set_color(ERR), FadeOut(env_g), run_time=0.5)
            assert st[0].text == GET_STATUS
            vo.wait_until("Then initialize")
            self.play(FadeOut(t8), FadeOut(r406), req.items[0].animate.set_color(INK), run_time=0.4)
            for k, (cue, card) in enumerate((("Then initialize", q_init), ("list tools", q_list),
                                             ("call: one tool", q_call))):
                vo.wait_until(cue)
                env = mini_envelope(None, LOOKUP, w=0.45).move_to(a_pt)
                self.play(FadeIn(env, scale=0.6), req.items[k + 1].animate.set_color(TURN), run_time=0.15)
                self.play(env.animate.move_to(b_pt), run_time=0.32)
                self.play(env.animate.move_to(a_pt), run_time=0.32)
                self.play(FadeOut(env), FadeIn(card, shift=DOWN * 0.2), req.items[k + 1].animate.set_color(INK),
                          run_time=0.35)
            vo.wait_until("one cheese fact per call")
            self.play(FadeIn(dif, shift=UP * 0.1), run_time=0.5)
        self.wait(1.5)                    # the three replies stay up to be read

        # ============================================================ 9 · plug 3: your own FastMCP server
        cf9 = colab_frame("Cheese Quiz", top=CF_TOP, bottom=-3.56)
        with drop_chars("♀"):
            p57 = src_panel(CELL57, [2, (5, 6), 11, 14], strip_emoji=True)
        assert "♀" not in p57.code.source and "# Run the server over HTTP on port 8000" in p57.code.source
        _with_header(p57, "Cheese Quiz · cell 57 · lines 2–14 (folded)", subtitle=SECTION57)
        place(p57, cx=0, top=PANEL_TOP)
        bar2 = p57.bar(2, TOOL, 0.22)
        u_thr = under(p57.span(11, "in a background thread"), TOOL, stroke=3)
        b8001 = span_box(p57.span(14, "port=8001"), DATA)
        u8000 = under(p57.span(11, "port 8000"), ERR, stroke=4)
        err = erratum_tag("the comment says port 8000")
        place(err, left=p57.span(11, "port 8000").get_left()[0] - 0.3, top=p57.code.get_bottom()[1] - 0.1)
        ob57 = output_box([C57_ROW], header="Cheese Quiz · cell 57 · saved output")
        old = grey_tag("saved from an older version of the cell").next_to(ob57.header, RIGHT, buff=0.25)
        g57 = VGroup(ob57, old)
        place(g57, left=-6.1, top=err.get_bottom()[1] - 0.12)
        assert g57.get_bottom()[1] > -3.43, g57.get_bottom()
        u57 = under(substring(ob57.rows[0], "8000"), ERR, stroke=4)
        # the picture after the panel: c59's log beside the thread inside the Colab VM
        ob59 = output_box(C59_ROWS, header="Cheese Quiz · cell 59 · output")
        sv59 = saved_run_tag().next_to(ob59.header, RIGHT, buff=0.25)
        g59 = VGroup(ob59, sv59)
        place(g59, left=-6.1, top=PANEL_TOP - 0.05)
        px = (ob59.frame.get_right()[0] + 6.45) / 2
        pw = 6.3 - ob59.frame.get_right()[0] - 0.3
        cli9 = text_box(["agent · client", ("Agents SDK", S.GREY)], TOOL, w=pw).move_to([px, 1.2, 0])
        fm9 = text_box(["FastMCP server", ("in a thread", S.GREY)], TOOL, w=pw).move_to([px, -1.35, 0])
        port9 = mono("127.0.0.1:8001", CAPTION, LOOKUP)
        port9.next_to(fm9, DOWN, buff=0.15)
        http9 = Line(cli9.get_bottom() + DOWN * 0.05, fm9.get_top() + UP * 0.05, color=LOOKUP, stroke_width=4)
        http9_l = label("HTTP", CAPTION, LOOKUP).next_to(http9, RIGHT, buff=0.35)
        with self.voiceover(SAY[9]) as vo:
            self.play(tr.goto(3), FadeOut(req), FadeOut(q_init), FadeOut(q_list), FadeOut(q_call), FadeOut(dif),
                      FadeOut(srv), FadeOut(https7), FadeOut(https_l), run_time=0.5)
            self.play(Transform(cf, cf9), run_time=0.7)
            self.play(FadeIn(p57, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("runs its own FastMCP server")
            self.play(FadeIn(bar2), run_time=0.5)
            vo.wait_until("in a thread")
            self.play(Create(u_thr), run_time=0.5)
            vo.wait_until("on port 8001")
            self.play(Create(b8001), run_time=0.5)
            vo.wait_until("A small slip")
            self.play(Create(u8000), run_time=0.5)
            vo.wait_until("the comment above says")
            self.play(FadeIn(err, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and so does an older")
            self.play(FadeIn(g57, shift=UP * 0.1), run_time=0.6)
            self.play(Create(u57), run_time=0.4)
            vo.wait_until("saved output")
            self.wait(vo.remaining(0.05) + 0.4)
            # no narration covers c59's log: keep this silent stretch short (it moves throughout)
            self.play(FadeOut(p57), FadeOut(bar2), FadeOut(u_thr), FadeOut(b8001), FadeOut(u8000), FadeOut(err),
                      FadeOut(g57), FadeOut(u57), run_time=0.4)
            self.play(FadeIn(cli9), FadeIn(fm9), FadeIn(port9), Create(http9), FadeIn(http9_l),
                      FadeIn(sv59), FadeIn(ob59.frame), FadeIn(ob59.rule), FadeIn(ob59.header), run_time=0.6)
            env9 = mini_envelope(None, LOOKUP, w=0.42).move_to(http9.get_top() + DOWN * 0.3)
            self.play(FadeIn(env9, scale=0.6), run_time=0.2)
            for k in range(0, len(C59_ROWS), 2):
                self.play(FadeIn(ob59.rows[k]), env9.animate.move_to(http9.get_bottom() + UP * 0.3), run_time=0.3)
                self.play(FadeIn(ob59.rows[k + 1]), env9.animate.move_to(http9.get_top() + DOWN * 0.3),
                          run_time=0.3)
            self.play(FadeOut(env9), Indicate(ob59.rows[2], color=TOOL, scale_factor=1.04),
                      Indicate(ob59.rows[4], color=TOOL, scale_factor=1.04),
                      Indicate(ob59.rows[6], color=TOOL, scale_factor=1.04), run_time=0.6)
            settle(self, g59)

        # ============================================================ 10 · who does the talking; your turn
        rows = VGroup(
            plug_row("Gemini", "ADK client", "stdio", "`npx … server-filesystem`", TOOL, ROW_YS[0]),
            plug_row("gpt-4o", "Agents SDK client", "HTTPS", "remote MCP server", CLOUD, ROW_YS[1]),
            plug_row("gpt-4o", "Agents SDK client", "HTTP · :8001", "FastMCP thread", TOOL, ROW_YS[2]),
        )
        card = turn_card_tight(TURN_ROWS)
        place(card, cx=0, bottom=-3.5)
        assert card.width < 12.6, card.width
        assert card.get_top()[1] < rows.get_bottom()[1] - 0.12, (card.get_top(), rows.get_bottom())
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(cf), FadeOut(g59), FadeOut(cli9), FadeOut(fm9), FadeOut(port9), FadeOut(http9),
                      FadeOut(http9_l), run_time=0.5)
            lag_play(self, [FadeIn(r, shift=RIGHT * 0.2) for r in rows], owner=rows, lag_ratio=0.25,
                     run_time=1.0)
            vo.wait_until("your client process")
            self.play(*[Indicate(r.client, color=TOOL, scale_factor=1.08) for r in rows], run_time=0.6)
            hang = DOWN * 0.1                # the envelopes ride just under the line, clear of its label
            envs = [mini_envelope(None, LOOKUP, w=0.38).move_to(r.line.get_left() + RIGHT * 0.35 + hang)
                    for r in rows]
            self.play(*[FadeIn(e, scale=0.6) for e in envs], run_time=0.2)
            self.play(*[e.animate.move_to(r.line.get_right() + LEFT * 0.35 + hang) for e, r in zip(envs, rows)],
                      run_time=0.8)
            self.play(*[e.animate.move_to(r.line.get_left() + RIGHT * 0.35 + hang) for e, r in zip(envs, rows)],
                      run_time=0.8)
            self.play(*[FadeOut(e) for e in envs], run_time=0.2)
            vo.wait_until("MCP gives the model")
            calls = [call_glyph() for r in rows]
            for c, r in zip(calls, rows):
                place(c, left=r.model.get_right()[0] + 0.12, cy=r.y)
            self.play(*[FadeIn(c, shift=RIGHT * 0.2) for c in calls],
                      *[Indicate(r.model, color=CLOUD, scale_factor=1.08) for r in rows], run_time=0.5)
            self.play(*[c.animate.move_to(r.client.get_left() + LEFT * (c.width / 2 + 0.06))
                        for c, r in zip(calls, rows)], run_time=0.8)
            vo.wait_until("it still only writes")
            self.play(*[Indicate(c, color=CLOUD, scale_factor=1.2) for c in calls], run_time=0.6)
            self.play(*[FadeOut(c, scale=0.6, target_position=r.client) for c, r in zip(calls, rows)],
                      *[Indicate(r.client, color=TOOL, scale_factor=1.06) for r in rows], run_time=0.6)
            vo.wait_until("Pause, and run")
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(rows), FadeOut(card), FadeOut(tr), run_time=0.8)
        self.wait(0.3)
