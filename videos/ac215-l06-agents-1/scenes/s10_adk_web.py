"""S10 · adk web and the folder names (dlops-io/llm-agent-google-adk README "Running Agents",
steps 1–2). Lecture: none (no lecture tag).

Beats (script.md "## S10", one voiceover block each):
0. TRACKER RunAg 1. The laptop terminal (full width, 12 rows, prompt …/llm-agent-google-adk$; the
   repository root in the prompt flashes) types `uv run adk web` -> adk-laptop/15 lines 2–3 joined, 10–11 joined, 13 cut after "[Y/n]:" (wrap);
   GREY tag "erratum · not in the README" beside the question.
1. "This is OFF by default." underlined GREY; [Y/n] boxed YELLOW, the capital Y flashes, YELLOW tag
   "Enter = yes"; after a 0.6 s pause the terminal types `n` (as captured); a GREY chip "uv run adk
   telemetry disable · change it later" in the band right of the tracker (`uv run`, as every adk
   command here: adk lives only in the project's .venv, so the bare form is "command not found").
2. 15 lines 34–38, 41 (cut); the URL on line 41 turns PINK. TRACKER RunAg 2: the terminal shrinks
   to the 3-row strip; a GREY browser (illustration) opens at localhost:8000 with the dev UI's agent
   field, and its address becomes localhost:8000/dev-ui/. TRACKER · extra: a second strip (laptop ·
   second terminal) slides over the server strip and types the extra `curl -s -o /dev/null -w …`
   (folded under its prompt) -> 16 line 2; "/dev-ui/" PINK in the strip and underlined PINK in the
   address bar.
3. The page's agent dropdown opens with the seven entries; the second strip types the extra `curl
   -s http://localhost:8000/list-apps; echo` -> 17 line 2 (cut: the page shows all seven); the
   nested entries' ".subfolder" parts flash YELLOW, GREY note "nested: folder.subfolder". The cursor picks
   1-baseline (YELLOW); the row turns RED and a RED banner in the page shows the detail text of 18
   line 2 (word-wrapped), "valid Python identifiers" flashes. The second strip slides away; the
   server strip prints 15 lines 44–45 joined (wrap), "404 Not Found" RED.
4. Why, as a picture (illustration), in place of the browser: a GREY folder 1-baseline/ holding
   agent.py -> a PURPLE arrow "adk web" -> a GREY chip app name = "1-baseline" (the folder's name
   flashes and fades in there) -> the check card "Python identifier?" with its two rules, and under it the GREY
   tag "ADK 2.12 checks when it loads the agent · 1.27.5 checks later, in App(name=…)"; the leading
   1 and the - turn RED, a RED cross on each rule.
5. A RED dashed "what if · just watch" frame; the server strip hides (one strip at a time); a 4-row
   strip inside types the extra `uv add "google-adk>=1.8.0,<1.28"` -> 21 lines 7–8 (1.27.5 flashes);
   `uv run adk web` (24's command); the page's dropdown shows the four folders of 25 line 2 (GREEN);
   picking 1-baseline -> 24 line 131, 132–133 joined cut after "underscores." (wrap) RED, the row
   turns RED; "Invalid app name" flashes at "as an invalid app name". The extra `git checkout pyproject.toml; uv sync --upgrade-package google-adk` -> 27
   lines 8–9 ("2.12.0" flashes; held 1.2 s so the proof can be read). The frame closes; the server
   strip returns with the GREY caption "back in your terminal".
6. TRACKER RunAg 1 · extra. The caption leaves as the terminal grows (13 rows): Ctrl+C -> 15 lines 46, 49–51 ("^C"
   flashes), the prompt returns; the extra `mv 1-baseline baseline; …; ls` (folded under the
   prompt, so only the bare prompt scrolls away) with the tags "extra" and "fix · not in the README"
   -> 28 lines 2–12; baseline, custom_agent, mcp_tools GREEN.
7. `uv run adk web` (29's command); the terminal shrinks to the strip; TRACKER RunAg 2: the browser
   again (localhost:8000/dev-ui/), reloaded with the dropdown open on its seven entries; TRACKER ·
   extra: the second strip types the list-apps curl -> 30 line 2 (cut); the cursor picks baseline,
   GREEN; a GREY card beside the list "this video: baseline, mcp_tools / custom_agent as code · 2, 4,
   6: exercises.md". At "The log says" the page, the card and the strip leave, then the terminal
   grows (9 rows) and the card returns under the tracker (it stays there, readable, until the
   next beat): 29 lines 36–37 joined, 38–39 joined, 40 (wrap); the root .env path PINK in a PINK box, PINK tag "the root .env" above the
   terminal; "baseline.agent" and "200 OK" GREEN.
8. The terminal shrinks to the strip. GREY chip in the band right of the tracker "git status: 3
   folders deleted, 3 new · fine for your copy (teardown)" (adk-laptop/39); two erratum cards write
   in: QUICKSTART.md · line 24 `uv run adk web 1-baseline/agent.py` (expected) -> 19 line 5 RED;
   2-litellm/README.md · line 74 `uv run adk` (expected) -> 20 line 2 + "prints help · starts
   nothing". "is a file." flashes at "where a folder is expected".
9. A RED dashed "what if · just watch" frame, note "llm-rag's Chroma still on port 8000"; a picture
   (illustration): Chroma (TEAL) holds 127.0.0.1:8000 (PINK); the 4-row strip types `uv run adk
   web` -> 36 line 21 (wrap) RED, adk web's arrow to :8000 gets a RED cross. GREY chip "docker
   compose down · in llm-rag · frees port 8000"; TRACKER · extra: `uv run adk web --port 8080`
   (extra) -> 37 line 34 (cut), 8080 PINK, a PINK :8080 port with a GREEN check (held 1 s). The frame closes;
   back in the viewer's terminal (the strip), ▶ on a static GREY card (Ctrl+C · the mv line · uv
   run adk web · reload localhost:8000, pick baseline). Hold 2 s. Fade to an empty frame.
"""

import json
import textwrap

import numpy as np
from common import (
    CTR,
    DATA,
    DEV_UI,
    ERR,
    INK,
    LOOKUP,
    NARRATION,
    P_ADK,
    RENAMES,
    STRIP_TOP,
    TOOL,
    TURN,
    Prose,
    _drop_bare,
    _type_rows,
    apps,
    bare_prompt,
    beside,
    capture,
    caption_extra,
    col_box,
    covers_text,
    erratum_tag,
    excerpt,
    expected_tag,
    extra_tag,
    fix_tag,
    fold_cmd,
    grey_tag,
    grid_x0,
    illustration_tag,
    note,
    pin,
    resize,
    second_terminal,
    strip_top,
    term,
    tracker,
    turn_card,
    type_cmd,
    under,
    what_if_frame,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    UL,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    RoundedRectangle,
    Transform,
    VGroup,
    smooth,
    squish_rate_func,
    there_and_back,
)

from explainer import style as S
from explainer.devops import (
    CAPTION,
    MONO,
    PANEL,
    TERM_BG,
    box,
    browser_window,
    cell_width,
    check_mark,
    chip,
    cross_mark,
    file_glyph,
    folder_glyph,
    glyph_range,
    label,
    mono,
    mono_line,
    substring,
    tag,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S10"]

# ------------------------------------------------------------------ the real captures and sources
WEB = capture("15", "adk-laptop")                  # the first `uv run adk web`
assert WEB.cmd == "uv run adk web", WEB.cmd
Q_ROW = WEB.join(2, 3)
assert Q_ROW.endswith("collect pseudonymized usage data?"), Q_ROW
OFF_ROW = WEB.join(10, 11)
assert OFF_ROW.startswith("This is OFF by default.") and "'adk telemetry disable'" in OFF_ROW, OFF_ROW
YN = WEB.cut(13, "[Y/n]:")
assert WEB.line(13) == YN + " n", WEB.line(13)     # the capture answered n
URL8000 = "http://127.0.0.1:8000"
assert URL8000 in WEB.line(41) and "Uvicorn running" in WEB.line(41), WEB.line(41)
LOG404 = WEB.join(44, 45)
assert "/dev/apps/1-baseline/build_graph" in LOG404 and LOG404.endswith("404 Not Found"), LOG404
assert WEB.line(46).startswith("^C") and "shutting down" in WEB.line(50), (WEB.line(46), WEB.line(50))

DEVUI = capture("16", "adk-laptop")                # extra: the redirect to the dev UI
assert DEVUI.line(2) == "307 -> http://localhost:8000/dev-ui/", DEVUI.line(2)
assert DEV_UI == "localhost:8000/dev-ui/"
LIST1 = capture("17", "adk-laptop")                # extra: the dropdown's entries
assert LIST1.cmd == "curl -s http://localhost:8000/list-apps; echo", LIST1.cmd
APPS1 = apps(LIST1.line(2))
assert len(APPS1) == 7 and APPS1[0] == "1-baseline", APPS1
SEL = capture("18", "adk-laptop")                  # extra: what the page gets when 1-baseline is picked
DETAIL = json.loads(SEL.line(2))["detail"]
assert DETAIL.startswith("Invalid agent name: '1-baseline'.") and "valid Python identifiers" in DETAIL

QS = capture("19", "adk-laptop")                   # QUICKSTART.md's form
assert QS.cmd == "uv run adk web 1-baseline/agent.py" == excerpt("llm-agent-google-adk/QUICKSTART.md", 24, 24)
QS_ERR = QS.line(5)
assert QS_ERR == "Error: Invalid value for '[AGENTS_DIR]': Directory '1-baseline/agent.py' is a file."
NOWEB = capture("20", "adk-laptop")                # the module READMEs' form
assert NOWEB.cmd == "uv run adk" == excerpt("llm-agent-google-adk/2-litellm/README.md", 74, 74)
assert NOWEB.line(2) == "Usage: adk [OPTIONS] COMMAND [ARGS]...", NOWEB.line(2)

PIN_ADD = capture("21", "adk-laptop")              # what if: an older ADK
assert PIN_ADD.cmd == 'uv add "google-adk>=1.8.0,<1.28"', PIN_ADD.cmd
assert PIN_ADD.at(7, 8) == [" - google-adk==2.12.0", " + google-adk==1.27.5"], PIN_ADD.at(7, 8)
PINNED = capture("24", "adk-laptop")
assert PINNED.cmd == "uv run adk web", PINNED.cmd
assert PINNED.line(131).endswith("1 validation error for App"), PINNED.line(131)
_j = PINNED.join(132, 133)
PINNED_ERR = _j[:_j.index("underscores.") + len("underscores.")]
assert "Invalid app name '1-baseline': must be a valid identifier" in PINNED_ERR, PINNED_ERR
APPS_PINNED = apps(capture("25", "adk-laptop").line(2))
assert APPS_PINNED == ["1-baseline", "2-litellm", "3-mcp-tools", "5-custom-agent"], APPS_PINNED
UNDO = capture("27", "adk-laptop")
assert UNDO.cmd == "git checkout pyproject.toml; uv sync --upgrade-package google-adk", UNDO.cmd
assert UNDO.at(8, 9) == [" - google-adk==1.27.5", " + google-adk==2.12.0"], UNDO.at(8, 9)

REN = capture("28", "adk-laptop")                  # the fix: rename the folders
assert REN.cmd == "mv 1-baseline baseline; mv 3-mcp-tools mcp_tools; mv 5-custom-agent custom_agent; ls"
assert all(n in REN.lines for n in RENAMES.values()), REN.lines
WEB2 = capture("29", "adk-laptop")                 # `uv run adk web` after the rename
assert WEB2.cmd == "uv run adk web", WEB2.cmd
ROOT_ENV = "/home/student/AC215/llm-agent-google-adk/.env"
ENV_LOG = WEB2.join(36, 37)
assert ENV_LOG.endswith("Loaded .env file for baseline at " + ROOT_ENV), ENV_LOG
AGENT_LOG = WEB2.join(38, 39)
assert AGENT_LOG.endswith("Found root_agent in baseline.agent"), AGENT_LOG
assert WEB2.line(40).endswith('"GET /dev/apps/baseline/build_graph HTTP/1.1" 200 OK'), WEB2.line(40)
LIST2 = capture("30", "adk-laptop")
assert LIST2.cmd == LIST1.cmd, LIST2.cmd
APPS2 = apps(LIST2.line(2))
assert len(APPS2) == 7 and "baseline" in APPS2 and "1-baseline" not in APPS2, APPS2

GIT = capture("39", "adk-laptop")                  # git status after the rename
_gone = {ln.split()[1].split("/")[0] for ln in GIT.lines if ln.startswith(" D ")}
_new = {ln.split()[1].rstrip("/") for ln in GIT.lines if ln.startswith("?? ") and ln.endswith("/")}
assert _gone == set(RENAMES) and _new == set(RENAMES.values()), (_gone, _new)

BUSY = capture("36", "adk-laptop")                 # what if: llm-rag's Chroma still on port 8000
assert BUSY.cmd.endswith("; uv run adk web"), BUSY.cmd
assert BUSY.line(21).endswith("address already in use") and "[Errno 98]" in BUSY.line(21), BUSY.line(21)
P8080 = capture("37", "adk-laptop")
assert P8080.cmd == "uv run adk web --port 8080", P8080.cmd
assert "Uvicorn running on http://127.0.0.1:8080" in P8080.line(34), P8080.line(34)

MV_CARD = "mv 1-baseline baseline; mv 3-mcp-tools mcp_tools; \\\n    mv 5-custom-agent custom_agent; ls"
assert MV_CARD.replace(" \\\n    ", " ") == REN.cmd

# ------------------------------------------------------------------ layout
TOP_Y = 2.78                  # nothing above this but the tracker band
GAP_Y = STRIP_TOP + 0.14      # the lowest y a picture above the 3-row strip may use
STRIP4_TOP = strip_top(4)     # the what-if strips have 4 rows (a folded command + 2 output lines)
WI_TOP = 2.6                  # what_if_frame's top edge (its title tag straddles it)
PITCH = 0.35                  # the dropdown's row pitch


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


def attach(scene, row, *mobs):
    """Make mobs (already on screen) part of terminal row `row`: they scroll and fade with it."""
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def rows_with(rows, sub: str):
    """The printed rows (mono_lines) whose text contains `sub`."""
    hits = [r for r in rows if sub in getattr(r, "text", "")]
    assert hits, (sub, [getattr(r, "text", "") for r in rows])
    return hits


def type_under(scene, t, cmd: str, type_time=None):
    """Type a command that cannot share a row with the long ADK prompt: the prompt stays alone on its
    row and the command folds under it (4-space indent, " \\"), so when the output scrolls the
    terminal, only the bare prompt row leaves and the whole command stays readable (type_cmd would
    start it after the prompt and lose its first words to the scroll)."""
    _drop_bare(scene, t)
    rows, hard = fold_cmd("    " + cmd, t.max_chars, 4)
    assert not hard, rows
    return _type_rows(scene, t, [t.prompt] + rows, len(t.prompt), type_time, len(cmd))


def last_row(line):
    return line.rows[-1] if hasattr(line, "rows") else line


def grey_chip(parts, color: str = S.GREY) -> VGroup:
    """A one-line GREY chip of mixed parts: "`mono`" pieces in mono, others as GREY notes."""
    items = []
    for p in parts:
        if p.startswith("`") and p.endswith("`"):
            items.append(mono(p[1:-1], CAPTION, INK))
        else:
            items.append(note(p))
    row = VGroup(*items).arrange(RIGHT, buff=0.14)
    fr = box(row.width + 0.44, row.height + 0.26, color, fill=S.BG, fill_opacity=0.92, radius=0.12)
    fr.move_to(row)
    g = VGroup(fr, row)
    g.frame, g.row = fr, row
    return g


def cursor(h: float = 0.4) -> Polygon:
    """A mouse pointer (white, dark rim); its tip is the top-left corner."""
    pts = [(0, 0), (0, -1), (0.27, -0.75), (0.45, -1.12), (0.6, -1.05), (0.43, -0.69), (0.76, -0.69)]
    return Polygon(*[np.array([x * h, y * h, 0.0]) for x, y in pts], stroke_color=S.BG,
                   stroke_width=2).set_fill(INK, 1)


def tip_to(cur, menu, name: str):
    """The shift that puts the cursor's tip on dropdown row `name`, just right of its text and of
    the next row's text, so the pointer's body (it hangs down-right, over the next row) hides no
    entry."""
    i = menu.entries.index(name)
    row = menu.rows[i]
    x = row.glyphs.get_right()[0] + 0.15
    if i + 1 < len(menu.rows):
        x = max(x, menu.rows[i + 1].glyphs.get_right()[0] + 0.1)
    x = min(x, menu.lst.get_right()[0] - 0.4)
    target = np.array([x, row.strut.get_center()[1] - 0.04, 0.0])
    return target - cur.get_corner(UL)


def pin_with(scene, line, mob, *others, run_time: float = 0.4):
    """pin() that plays other animations alongside the tag's FadeIn (same rules: the tag must not
    cover its row's text; it becomes part of the row, so it scrolls and fades with it)."""
    row = last_row(line)
    assert not covers_text(mob, row), "the tag would cover its row's text"
    scene.play(FadeIn(mob, shift=LEFT * 0.1), *others, run_time=run_time)
    scene.remove(mob)
    row.add(mob)
    scene.add(row)
    return mob


def click(cur):
    """The cursor presses (a short squeeze about its tip)."""
    return cur.animate(rate_func=there_and_back).scale(0.8, about_point=cur.get_corner(UL))


class AgentMenu(VGroup):
    """The dev UI's agent dropdown (illustration), compact: the field "Select an agent ▾" and the
    open list of entries (mono, 20 pt, from a captured list-apps line). The house Dropdown (3.6
    tall for seven entries) does not fit in a browser above the 3-row strip. Built at ORIGIN.
    .field .lst (list box) .rows .entries .row(name) .pick(name, colour) -> (outline, [anims])
    .recolor(name, outline, colour) -> [anims]"""

    def __init__(self, entries, color: str = INK, size: float = CAPTION, pitch: float = PITCH,
                 min_w: float = 3.6, **kw):
        super().__init__(**kw)
        rows = VGroup()
        for i, e in enumerate(entries):
            r = mono_line(e, size, color)
            r.shift(np.array([0.0, -i * pitch, 0.0]) - r.strut.get_corner(UL))
            rows.add(r)
        self.w = max(min_w, max(r.glyphs.width for r in rows) + 0.6)
        fbox = RoundedRectangle(width=self.w, height=0.46, corner_radius=0.08, stroke_color=S.GREY,
                                stroke_width=2).set_fill(TERM_BG, 1)
        head = label("Select an agent", size, S.GREY)
        caret = label("▾", size, S.GREY)
        head.move_to(fbox).align_to(fbox, LEFT).shift(RIGHT * 0.2)
        caret.move_to(fbox).align_to(fbox, RIGHT).shift(LEFT * 0.2)
        self.field = VGroup(fbox, head, caret)
        self.lst = RoundedRectangle(width=self.w, height=rows.height + 0.3, corner_radius=0.08,
                                    stroke_color=S.GREY_DARK, stroke_width=2).set_fill(PANEL, 1)
        self.lst.next_to(fbox, DOWN, buff=0.06)
        rows.move_to(self.lst).align_to(self.lst, LEFT).shift(RIGHT * 0.3)
        self.rows, self.entries = rows, list(entries)
        self.add(self.field, self.lst, rows)

    def row(self, name: str):
        return self.rows[self.entries.index(name)]

    def pick(self, name: str, color: str = TURN):
        r = self.row(name)
        hl = RoundedRectangle(width=self.w - 0.16, height=r.strut.height + 0.08, corner_radius=0.06,
                              stroke_color=color, stroke_width=2.5).set_fill(color, 0.12)
        hl.move_to([self.lst.get_center()[0], r.strut.get_center()[1], 0])
        return hl, [Create(hl), r.glyphs.animate.set_color(color)]

    def recolor(self, name: str, hl, color: str):
        r = self.row(name)
        return [hl.animate.set_stroke(color).set_fill(color, 0.12), r.glyphs.animate.set_color(color)]


def browser(top: float, bottom: float, width: float = 12.6, url: str = DEV_UI) -> VGroup:
    """The GREY browser (illustration) from `top` to `bottom`, centred; tag inside the page, top right.
    .frame .address .content .tag"""
    br = browser_window(url, width=width, height=top - bottom)
    place(br, cx=0, top=top)
    tg = illustration_tag()
    place(tg, right=br.content.get_right()[0] - 0.05, top=br.content.get_top()[1] - 0.02)
    br.add(tg)
    br.tag = tg
    return br


def menu_in(br, menu):
    """Put the dropdown at the page's top left."""
    return place(menu, left=br.content.get_left()[0] + 0.2, top=br.content.get_top()[1] - 0.02)


def error_banner(text: str, width_chars: int = 36) -> VGroup:
    """The page's RED error banner: the detail text, word-wrapped, mono. .rows .frame"""
    lines = textwrap.wrap(text, width_chars)
    rows = VGroup()
    for i, s in enumerate(lines):
        r = mono_line(s, CAPTION, INK)
        r.shift(np.array([0.0, -i * PITCH, 0.0]) - r.strut.get_corner(UL))
        rows.add(r)
    fr = box(rows.width + 0.5, rows.height + 0.34, ERR, fill=ERR, fill_opacity=0.14, radius=0.1)
    fr.move_to(rows)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


def why_picture() -> VGroup:
    """Why the name is refused (illustration): the folder -> adk web -> the app's name -> the check.
    .folder .fname .arrow .alabel .chip .cline .down .card .rule1 .rule2 .x1 .x2 .tag .ill"""
    g = VGroup()
    fg = folder_glyph(0.42, S.GREY)
    fname = mono_line("1-baseline/", 22, INK)
    top = VGroup(fg, fname).arrange(RIGHT, buff=0.16)
    fglyph = file_glyph(0.34, S.GREY)
    fpy = mono("agent.py", 22, INK)
    sub = VGroup(fglyph, fpy).arrange(RIGHT, buff=0.14)
    sub.next_to(top, DOWN, buff=0.18).align_to(top, LEFT).shift(RIGHT * 0.5)
    folder = VGroup(top, sub)
    place(folder, left=-6.2, cy=1.45)
    cline = mono_line('app name = "1-baseline"', 22, INK)
    cfr = box(cline.width + 0.5, cline.strut.height + 0.3, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    cfr.move_to(cline)
    chip_ = VGroup(cfr, cline)
    place(chip_, left=-1.05)
    chip_.set_y(fname.strut.get_center()[1])
    arrow = Arrow([fname.get_right()[0] + 0.2, chip_.get_y(), 0], [chip_.get_left()[0] - 0.08, chip_.get_y(), 0],
                  color=TOOL, stroke_width=5, buff=0.0, max_tip_length_to_length_ratio=0.12)
    alabel = mono("adk web", CAPTION, TOOL).next_to(arrow, UP, buff=0.1)
    # the check
    title = label("Python identifier?", 22, INK)
    r1 = label("letters, digits, underscores only", CAPTION, INK)
    r2 = label("no leading digit", CAPTION, INK)
    body = VGroup(title, r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    card = box(body.width + 1.3, body.height + 0.42, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    card.move_to(body).shift(RIGHT * 0.4)
    body.align_to(card, LEFT).shift(RIGHT * 0.3)
    check = VGroup(card, body)
    place(check, cx=chip_.get_x(), top=chip_.get_bottom()[1] - 0.55)
    down = Arrow(chip_.get_bottom() + DOWN * 0.04, card.get_top() + UP * 0.04, color=S.GREY, stroke_width=4,
                 buff=0.0, max_tip_length_to_length_ratio=0.3)
    x1 = cross_mark(0.24, ERR).next_to(r1, RIGHT, buff=0.3)
    x2 = cross_mark(0.24, ERR).move_to([x1.get_x(), r2.get_y(), 0])
    why_tag = grey_tag("ADK 2.12 checks when it loads the agent · 1.27.5 checks later, in App(name=…)")
    place(why_tag, cx=0, bottom=GAP_Y + 0.08)
    VGroup(folder, arrow, alabel, chip_, down, check, x1, x2).shift(RIGHT * 1.1)   # centred
    ill = illustration_tag()
    place(ill, right=6.4, top=TOP_Y)
    g.add(folder, arrow, alabel, chip_, down, check, x1, x2, why_tag, ill)
    g.folder, g.fname, g.arrow, g.alabel, g.chip, g.cline = folder, fname, arrow, alabel, chip_, cline
    g.down, g.card, g.title, g.rule1, g.rule2, g.x1, g.x2 = down, check, title, r1, r2, x1, x2
    g.tag, g.ill = why_tag, ill
    return g


def slip_card(where: str, cmd: str, out_rows, note_: str | None = None) -> VGroup:
    """One tutorial slip: the README's command in a mono chip headed `where` (tags expected and
    erratum), and under it, after a GREY arrow, what it prints here on a dark output panel.
    out_rows: [(text, colour)]. .chip .head .tags .arrow .out .note"""
    c = chip(cmd, S.GREY, size=CAPTION, font=MONO)
    head = note(where).next_to(c, UP, buff=0.08).align_to(c, LEFT).shift(RIGHT * 0.08)
    tags = VGroup(expected_tag(), erratum_tag()).arrange(RIGHT, buff=0.15).next_to(c, RIGHT, buff=0.2)
    rows = VGroup()
    for i, (s, col) in enumerate(out_rows):
        r = mono_line(s, CAPTION, col)
        r.shift(np.array([0.0, -i * 0.36, 0.0]) - r.strut.get_corner(UL))
        if "↪" in s:
            substring(r, "↪").set_color(S.GREY)
        rows.add(r)
    panel = RoundedRectangle(width=rows.width + 0.5, height=rows.height + 0.26, corner_radius=0.1,
                             stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(TERM_BG, 1)
    panel.move_to(rows)
    out = VGroup(panel, rows)
    arrow = label("→", 22, S.GREY)
    VGroup(arrow, out).arrange(RIGHT, buff=0.2)
    VGroup(arrow, out).next_to(c, DOWN, buff=0.2).align_to(c, LEFT).shift(RIGHT * 0.3)
    arrow.set_y(rows[0].strut.get_center()[1])
    g = VGroup(head, c, tags, arrow, out)
    g.head, g.chip, g.tags, g.arrow, g.out, g.rows, g.note = head, c, tags, arrow, out, rows, None
    if note_:
        n = note(note_).next_to(panel, RIGHT, buff=0.3)
        n.set_y(rows[-1].strut.get_center()[1])
        g.add(n)
        g.note = n
    return g


def clash_picture() -> VGroup:
    """What if llm-rag's Chroma still holds port 8000 (illustration): Chroma (TEAL) holds
    127.0.0.1:8000 (PINK); adk web (PURPLE) reaches for it and is refused (RED cross); with --port
    8080 it takes 127.0.0.1:8080 (GREEN check). .chroma .p8000 .hold .adk .try_ .x .p8080 .ok .okc .ill"""
    y1, y2 = 1.45, 0.15
    chroma = chip("llm-rag-chromadb", CTR, size=CAPTION, font=MONO).move_to([-4.3, y1, 0])
    p8000 = chip("127.0.0.1:8000", LOOKUP, size=CAPTION, font=MONO).move_to([0.0, y1, 0])
    adk = chip("adk web", TOOL, size=CAPTION, font=MONO).move_to([4.5, y1, 0])
    hold = Line(chroma.get_right() + RIGHT * 0.06, p8000.get_left() + LEFT * 0.06, color=CTR, stroke_width=5)
    hl = note("holds it").next_to(hold, UP, buff=0.1)
    try_ = Arrow(adk.get_left() + LEFT * 0.06, p8000.get_right() + RIGHT * 0.06, color=TOOL, stroke_width=4,
                 buff=0.0, max_tip_length_to_length_ratio=0.12)
    x = cross_mark(0.3, ERR).move_to(try_.get_center())
    p8080 = chip("127.0.0.1:8080", LOOKUP, size=CAPTION, font=MONO).move_to([0.0, y2, 0])
    ok = Arrow(adk.get_bottom() + DOWN * 0.06 + LEFT * 0.2, p8080.get_right() + RIGHT * 0.06, color=TOOL,
               stroke_width=4, buff=0.0, max_tip_length_to_length_ratio=0.1)
    okc = check_mark(0.3, DATA).next_to(p8080, LEFT, buff=0.25)
    ill = illustration_tag()
    place(ill, left=-6.1, top=WI_TOP - 0.3)
    g = VGroup(chroma, p8000, hold, hl, adk, try_, x, p8080, ok, okc, ill)
    g.chroma, g.p8000, g.hold, g.hl, g.adk, g.try_, g.x = chroma, p8000, hold, hl, adk, try_, x
    g.p8080, g.ok, g.okc, g.ill = p8080, ok, okc, ill
    return g


class AdkWeb(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0 · uv run adk web: a question first
        tr = tracker("RunAg", 1)
        t = term(P_ADK, rows=12, title="laptop")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t, shift=UP * 0.2), run_time=0.8)
            p0 = bare_prompt(self, t)
            vo.wait_until("from the repository root")
            root_dir = glyph_range(p0, P_ADK.index("~"), len(P_ADK) - 1)
            self.play(Indicate(root_dir, color=TURN, scale_factor=1.03), run_time=0.9)   # no overlap with ":" / "$"
            vo.wait_until("uv run ADK web")
            type_cmd(self, t, WEB.cmd, 0.7)
            vo.wait_until("First, version 2.12")
            q = t.print(self, [Q_ROW], wrap=True, run_time=0.4)
            off = t.print(self, [OFF_ROW], wrap=True, run_time=0.4)
            yn = t.print(self, [YN], run_time=0.3)[0]
            vo.wait_until("a question the README doesn't mention")
            er = beside(erratum_tag("not in the README"), t, q[-1], buff=0.35)
            pin(self, q[-1], er, run_time=0.4)
            vo.wait_until("may Google collect usage data?")
            self.play(Indicate(substring(q[-1], "usage data?"), color=TURN, scale_factor=1.1), run_time=0.8)

        # ========================================================== 1 · Enter answers yes; we typed n
        cw = cell_width(t.size)
        tchip = grey_chip(["`uv run adk telemetry disable`", "· change it later"])   # adk is in .venv only
        place(tchip, right=6.4, cy=2.62)
        with self.voiceover(SAY[1]) as vo:
            offr = off[0]
            u_off = under(substring(offr, "This is OFF by default."), S.GREY, stroke=3)
            self.play(Create(u_off), run_time=0.6)
            attach(self, offr, u_off)
            vo.wait_until("but the capital Y")
            a = YN.index("[Y/n]")
            ybox = col_box(yn, a, a + 5, TURN)
            self.play(Create(ybox), run_time=0.4)
            attach(self, yn, ybox)
            self.play(Indicate(glyph_range(yn, a + 1, a + 2), color=TURN, scale_factor=1.6), run_time=0.6)
            ent = tag("Enter = yes", TURN)
            ent.move_to([grid_x0(yn) + (len(YN) + 2) * cw + 0.3 + ent.width / 2,
                         yn.strut.get_center()[1], 0])
            pin(self, yn, ent, run_time=0.4)
            vo.wait_until("Answer as you like")
            self.wait(0.6)                              # the capture's answer comes after a beat
            full = mono_line(WEB.line(13), t.size, INK)
            full.shift(yn.strut.get_corner(UL) - full.strut.get_corner(UL))
            n_key = glyph_range(full, len(YN) + 1)
            self.play(FadeIn(n_key), run_time=0.2)
            attach(self, yn, n_key)
            vo.wait_until("change it later")
            self.play(FadeIn(tchip, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 2 · the server starts; open the browser
        br = browser(TOP_Y, GAP_Y, url="localhost:8000")
        menu = menu_in(br, AgentMenu(APPS1))
        with self.voiceover(SAY[2]) as vo:
            ban = t.print(self, WEB.at((34, 38), 41), run_time=0.7)
            l41 = ban[-1]
            vo.wait_until("on port 8000")
            url = substring(l41, URL8000)
            self.play(url.animate.set_color(LOOKUP), run_time=0.3)
            self.play(Indicate(url, color=LOOKUP, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Step 2:")
            self.play(FadeOut(tchip), run_time=0.3)
            resize(self, t, 3, run_time=0.6, extra=[tr.goto(2)])
            vo.wait_until("open localhost 8000")
            self.play(FadeIn(br, shift=UP * 0.1), FadeIn(menu.field), run_time=0.6)
            new_addr = mono(DEV_UI, CAPTION, S.GREY)
            new_addr.move_to(br.address).align_to(br.address, LEFT)
            self.play(Transform(br.address, new_addr), run_time=0.5)
            vo.wait_until("an extra curl")
            self.play(caption_extra(tr, True), run_time=0.3)
            t2 = second_terminal(self, P_ADK, rows=3, top=STRIP_TOP, run_time=0.4)
            c16 = type_under(self, t2, DEVUI.cmd, 1.2)
            pin(self, last_row(c16), beside(extra_tag(), t2, c16), run_time=0.3)
            o16 = t2.print(self, [DEVUI.line(2)], run_time=0.3)[0]
            vo.wait_until("the redirect to the dev UI")
            u_addr = under(new_addr[-8:], LOOKUP, stroke=3)
            self.play(substring(o16, "/dev-ui/").animate.set_color(LOOKUP), Create(u_addr), run_time=0.6)

        # ========================================================== 3 · the dropdown; 1-baseline is refused
        banner = error_banner(DETAIL)
        place(banner, right=br.content.get_right()[0] - 0.1, top=br.tag.get_bottom()[1] - 0.25)
        nested = [menu.row(e) for e in APPS1 if "." in e]
        mods = [substring(r, r.text[r.text.index("."):]) for r in nested]
        nest_note = note("nested: folder.subfolder")
        place(nest_note, left=menu.get_right()[0] + 0.3)
        nest_note.set_y(nested[-1].strut.get_center()[1])
        cur = cursor()
        place(cur, left=menu.get_right()[0] + 0.6, top=menu.field.get_bottom()[1] - 0.1)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(menu.lst), LaggedStart(*[FadeIn(r, shift=DOWN * 0.05) for r in menu.rows],
                                                     lag_ratio=0.15), run_time=0.9)
            c17 = type_cmd(self, t2, LIST1.cmd, 0.8)
            pin(self, last_row(c17), beside(extra_tag(), t2, c17), run_time=0.3)
            t2.print(self, [LIST1.line(2)], run_time=0.3)              # cut: the page shows all seven
            vo.wait_until("nested ones included")
            self.play(*[m.animate.set_color(TURN) for m in mods], FadeIn(nest_note, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Pick 1 baseline")
            self.play(*[m.animate.set_color(INK) for m in mods], FadeOut(nest_note), FadeIn(cur), run_time=0.4)
            self.play(cur.animate.shift(tip_to(cur, menu, "1-baseline")), run_time=0.6)
            hl3, anims = menu.pick("1-baseline", TURN)
            self.play(*anims, click(cur), run_time=0.4)
            vo.wait_until("and the page refuses")
            self.play(FadeIn(banner, shift=LEFT * 0.15), *menu.recolor("1-baseline", hl3, ERR), run_time=0.6)
            vo.wait_until("agent names must be valid")
            vp = [r for r in banner.rows if "valid Python" in r.text]
            idf = [r for r in banner.rows if r.text.startswith("identifiers")]
            self.play(*[Indicate(substring(r, "valid Python"), color=ERR, scale_factor=1.1) for r in vp],
                      *[Indicate(substring(r, "identifiers"), color=ERR, scale_factor=1.1) for r in idf],
                      run_time=0.8)
            self.play(FadeOut(t2, shift=DOWN * 0.3), caption_extra(tr, False), run_time=0.5)
            l404 = t.print(self, [LOG404], wrap=True, run_time=0.4)
            self.play(substring(l404[-1], "404 Not Found").animate.set_color(ERR), run_time=0.4)

        # ========================================================== 4 · why: the folder name becomes the app name
        why = why_picture()
        one = glyph_range(why.cline, why.cline.text.index('"') + 1, why.cline.text.index('"') + 2)
        dash = glyph_range(why.cline, why.cline.text.index("-"), why.cline.text.index("-") + 1)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(br, menu, hl3, banner, cur, u_addr)), run_time=0.5)
            self.play(FadeIn(why.folder, shift=RIGHT * 0.15), FadeIn(why.ill), run_time=0.5)
            vo.wait_until("Each folder name")
            self.play(GrowArrow(why.arrow), FadeIn(why.alabel), run_time=0.6)
            self.play(FadeIn(why.chip[0]), FadeIn(substring(why.cline, "app name =")),
                      # the folder name flashes in place and fades in on the code line (a flying copy
                      # crossed its own name and "app name =")
                      Indicate(substring(why.fname, "1-baseline"), color=TURN, scale_factor=1.1),
                      FadeIn(substring(why.cline, "1-baseline"), rate_func=squish_rate_func(smooth, 0.3, 1.0)),
                      FadeIn(glyph_range(why.cline, len(why.cline.text) - 1)),
                      FadeIn(glyph_range(why.cline, why.cline.text.index('"'), why.cline.text.index('"') + 1)),
                      run_time=0.8)
            self.add(why.chip)
            vo.wait_until("and an identifier holds only")
            self.play(GrowArrow(why.down), FadeIn(why.card[0]), FadeIn(why.title), run_time=0.5)
            self.play(FadeIn(why.rule1, shift=RIGHT * 0.1), FadeIn(why.tag, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("never starting with a digit")
            self.play(FadeIn(why.rule2, shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("The name 1 baseline breaks both rules")
            self.play(one.animate.set_color(ERR), dash.animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(one, color=ERR, scale_factor=1.6), Indicate(dash, color=ERR, scale_factor=1.6),
                      FadeIn(why.x1, scale=1.3), FadeIn(why.x2, scale=1.3), run_time=0.8)

        # ========================================================== 5 · what if: an older ADK
        wf = what_if_frame(top=WI_TOP)
        tw = term(P_ADK, rows=4, title="laptop")
        br5 = browser(WI_TOP - 0.32, STRIP4_TOP + 0.14, width=12.3)
        menu5 = menu_in(br5, AgentMenu(APPS_PINNED, color=DATA))
        cur5 = cursor()
        place(cur5, left=menu5.get_right()[0] + 0.6, top=menu5.field.get_bottom()[1] - 0.1)
        back = note("back in your terminal")
        place(back, left=-6.25, bottom=STRIP_TOP + 0.15)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(why), FadeOut(t), run_time=0.35)
            self.play(Create(wf.frame), FadeIn(wf.title), FadeIn(tw, shift=UP * 0.2), caption_extra(tr, True),
                      run_time=0.5)
            bare_prompt(self, tw)
            c21 = type_cmd(self, tw, PIN_ADD.cmd, 0.7)
            o21 = tw.print(self, PIN_ADD.at(7, 8), run_time=0.3)
            pin_with(self, c21, beside(extra_tag(), tw, c21),
                     Indicate(substring(o21[1], "1.27.5"), color=TURN, scale_factor=1.2), run_time=0.5)
            vo.wait_until("lists only the four folders")
            type_cmd(self, tw, PINNED.cmd, 0.4)
            self.play(FadeIn(br5, shift=UP * 0.1), FadeIn(menu5), run_time=0.5)
            vo.wait_until("but picking one still fails")
            self.play(FadeIn(cur5), cur5.animate.shift(tip_to(cur5, menu5, "1-baseline")), run_time=0.5)
            hl5, anims = menu5.pick("1-baseline", TURN)
            self.play(*anims, click(cur5), run_time=0.35)
            e24 = tw.print(self, [(PINNED.line(131), ERR), (PINNED_ERR, ERR)], wrap=True, run_time=0.5)
            self.play(*menu5.recolor("1-baseline", hl5, ERR), run_time=0.4)
            vo.wait_until("as an invalid app name")
            bad = [r for r in e24 if "Invalid app name" in r.text]
            self.play(*[Indicate(substring(r, "Invalid app name"), color=ERR, scale_factor=1.1) for r in bad],
                      run_time=0.7)
            vo.wait_until("So a version pin doesn't help")
            c27 = type_cmd(self, tw, UNDO.cmd, 0.8)
            pin(self, last_row(c27), beside(extra_tag(), tw, c27), run_time=0.3)
            o27 = tw.print(self, UNDO.at(8, 9), run_time=0.4)
            # "we undid ours": hold the proof (2.12.0 is back) before the frame closes
            self.play(Indicate(substring(o27[1], "2.12.0"), color=TURN, scale_factor=1.2), run_time=0.7)
            self.wait(0.5)
            self.play(FadeOut(VGroup(wf, tw, br5, menu5, hl5, cur5)), run_time=0.5)
            self.play(FadeIn(t), FadeIn(back, shift=UP * 0.1), caption_extra(tr, False), run_time=0.5)

        # ========================================================== 6 · the fix: rename the folders
        with self.voiceover(SAY[6]) as vo:
            self.play(tr.goto(1), run_time=0.5)
            self.play(caption_extra(tr, True), run_time=0.3)
            vo.wait_until("which isn't in the README either")
            # the caption is gone before the growing frame reaches it (the rows slid through it)
            resize(self, t, 13, run_time=0.7, extra=[FadeOut(back, rate_func=squish_rate_func(smooth, 0.0, 0.2))])
            vo.wait_until("Stop the server with control C")
            stop = t.print(self, WEB.at(46, (49, 51)), run_time=0.6)
            self.play(Indicate(substring(stop[0], "^C"), color=TURN, scale_factor=1.5), run_time=0.6)
            bare_prompt(self, t)
            vo.wait_until("then drop each leading number")
            cmv = type_under(self, t, REN.cmd, 1.5)
            lr = last_row(cmv)
            ex6 = beside(extra_tag(), t, cmv)
            fx6 = fix_tag().next_to(ex6, RIGHT, buff=0.15)
            assert fx6.get_right()[0] < t.box.get_right()[0] - 0.1, fx6.get_right()
            self.play(FadeIn(ex6, shift=LEFT * 0.1), FadeIn(fx6, shift=LEFT * 0.1), run_time=0.3)
            attach(self, lr, ex6, fx6)
            out6 = t.print(self, REN.at((2, 12)), run_time=0.7)
            vo.wait_until("and turn hyphens into underscores")
            new = [r for r in out6 if r.text in RENAMES.values()]
            assert len(new) == 3, [r.text for r in out6]
            self.play(*[r.glyphs.animate.set_color(DATA) for r in new], run_time=0.6)

        # ========================================================== 7 · start again, pick baseline: it loads
        br7 = browser(TOP_Y, GAP_Y)
        menu7 = menu_in(br7, AgentMenu(APPS2))
        cur7 = cursor()
        place(cur7, left=menu7.get_right()[0] + 0.6, top=menu7.field.get_bottom()[1] - 0.1)
        card7 = VGroup(note("this video: baseline, mcp_tools"),
                       note("custom_agent as code · 2, 4, 6: exercises.md")).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.12)
        fr7 = box(card7.width + 0.5, card7.height + 0.36, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
        fr7.move_to(card7)
        card7 = VGroup(fr7, card7)
        place(card7, left=menu7.get_right()[0] + 0.5, bottom=menu7.get_bottom()[1])
        card7_up = card7.copy()               # where the card waits while the log prints: under the tracker
        place(card7_up, left=-6.2, top=TOP_Y - 0.05)
        with self.voiceover(SAY[7]) as vo:
            self.play(caption_extra(tr, False), run_time=0.15)
            type_cmd(self, t, WEB2.cmd, 0.4)
            # the page reloads with the dropdown open (the entries of 30 line 2)
            resize(self, t, 3, run_time=0.5, extra=[tr.goto(2), FadeIn(br7, shift=UP * 0.1), FadeIn(menu7),
                                                    FadeIn(cur7)])
            t7 = second_terminal(self, P_ADK, rows=3, top=STRIP_TOP, run_time=0.25)
            c30 = type_cmd(self, t7, LIST2.cmd, 0.4)
            t7.print(self, [LIST2.line(2)], run_time=0.2)
            pin_with(self, c30, beside(extra_tag(), t7, c30), caption_extra(tr, True),
                     cur7.animate.shift(tip_to(cur7, menu7, "baseline")), run_time=0.35)
            hl7, anims = menu7.pick("baseline", DATA)
            self.play(*anims, click(cur7), FadeIn(card7, shift=LEFT * 0.1), run_time=0.3)
            vo.wait_until("The log says")
            # old panels out, then new in (one half each). Out: the page, the card beside the list and
            # the second strip, its text first, then its frame, so the server strip under it shows
            # through an empty frame (dissolved whole, the two strips' rows mixed). In: the terminal
            # grows and the card returns under the tracker. (Done at once, the growing terminal rose
            # under the leaving strip and the card sat on the fading page: final review.)
            frame7 = [m for m in t7.submobjects if m is not t7.lines and m is not t7.title]
            self.play(FadeOut(VGroup(br7, menu7, hl7, cur7, card7)), caption_extra(tr, False),
                      FadeOut(VGroup(*frame7), rate_func=squish_rate_func(smooth, 0.5, 1.0)),
                      # added last, so the text is drawn above the strip's (opaque) frame
                      FadeOut(VGroup(t7.lines, t7.title), rate_func=squish_rate_func(smooth, 0.0, 0.5)),
                      run_time=0.25)
            card7.move_to(card7_up)
            resize(self, t, 9, run_time=0.25, extra=[FadeIn(card7, shift=DOWN * 0.1)])
            log = t.print(self, [ENV_LOG, AGENT_LOG, WEB2.line(40)], wrap=True, run_time=0.3)
            env_row = rows_with(log, ROOT_ENV)[0]
            a = env_row.text.index(ROOT_ENV)
            pbox = col_box(env_row, a, a + len(ROOT_ENV), LOOKUP)
            root = tag("the root .env", LOOKUP)
            place(root, right=pbox.get_right()[0], bottom=t.box.get_top()[1] + 0.2)
            self.play(substring(env_row, ROOT_ENV).animate.set_color(LOOKUP), Create(pbox),
                      FadeIn(root, shift=DOWN * 0.1), run_time=0.6)
            attach(self, env_row, pbox)
            vo.wait_until("and found the root agent")
            ag = rows_with(log, "baseline.agent")[0]
            ok = rows_with(log, "200 OK")[0]
            self.play(substring(ag, "baseline.agent").animate.set_color(DATA),
                      substring(ok, "200 OK").animate.set_color(DATA), run_time=0.4)
            self.play(Indicate(substring(ag, "baseline.agent"), color=DATA, scale_factor=1.1), run_time=0.7)

        # ========================================================== 8 · git status; two more slips
        git = grey_chip(["`git status:`", "3 folders deleted, 3 new · fine for your copy (teardown)"])
        place(git, left=-3.0, cy=3.2)
        slip_a = slip_card("QUICKSTART.md · line 24", QS.cmd,
                           [(QS_ERR[:QS_ERR.index(" Directory")], ERR),
                            ("  ↪ " + QS_ERR[QS_ERR.index("Directory"):], ERR)])
        place(slip_a, left=-6.2, top=TOP_Y)
        slip_b = slip_card("2-litellm/README.md · line 74", NOWEB.cmd, [(NOWEB.line(2), INK)],
                           note_="prints help · starts nothing")
        place(slip_b, left=-6.2, top=slip_a.get_bottom()[1] - 0.4)
        VGroup(slip_a, slip_b).set_x(0)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(root), FadeOut(card7), run_time=0.3)
            resize(self, t, 3, run_time=0.5, extra=[FadeIn(git, shift=DOWN * 0.1)])
            vo.wait_until("the quick start passes a file")
            self.play(FadeIn(VGroup(slip_a.head, slip_a.chip, slip_a.tags), shift=RIGHT * 0.1), run_time=0.5)
            self.play(FadeIn(VGroup(slip_a.arrow, slip_a.out), shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("where a folder is expected")
            self.play(Indicate(substring(slip_a.rows[1], "is a file."), color=ERR, scale_factor=1.1), run_time=0.7)
            vo.wait_until("and the module READMEs drop")
            self.play(FadeIn(VGroup(slip_b.head, slip_b.chip, slip_b.tags), shift=RIGHT * 0.1), run_time=0.5)
            self.play(FadeIn(VGroup(slip_b.arrow, slip_b.out), shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("so it only prints help")
            self.play(FadeIn(slip_b.note, shift=LEFT * 0.1), run_time=0.5)

        # ========================================================== 9 · what if port 8000 is taken; ▶
        wf9 = what_if_frame(top=WI_TOP, note_="llm-rag's Chroma still on port 8000")
        tw9 = term(P_ADK, rows=4, title="laptop")
        clash = clash_picture()
        compose = grey_chip(["`docker compose down`", "· in llm-rag · frees port 8000"])
        place(compose, left=-6.1, top=clash.p8080.get_bottom()[1] - 0.2)
        card = turn_card([("Ctrl+C", "stop the server"), (MV_CARD, "extra"), WEB2.cmd,
                          Prose("reload localhost:8000 · pick baseline")], header=None)
        place(card, cx=0, cy=(TOP_Y + GAP_Y) / 2)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(git, slip_a, slip_b)), FadeOut(t), run_time=0.5)
            self.play(Create(wf9.frame), FadeIn(wf9.title), FadeIn(wf9.note), FadeIn(tw9, shift=UP * 0.2),
                      run_time=0.7)
            bare_prompt(self, tw9)
            self.play(FadeIn(VGroup(clash.chroma, clash.p8000, clash.hold, clash.hl, clash.ill)), run_time=0.5)
            vo.wait_until("they clash")
            type_cmd(self, tw9, PINNED.cmd, 0.5)
            self.play(FadeIn(clash.adk), GrowArrow(clash.try_), run_time=0.5)
            vo.wait_until("the web server stopped")
            busy = tw9.print(self, [(BUSY.line(21), ERR)], wrap=True, run_time=0.4)
            self.play(FadeIn(clash.x, scale=1.3), run_time=0.4)
            vo.wait_until("address already in use")         # spoken ~1.3 s after "stopped"
            self.play(Indicate(substring(busy[-1], "address already in use"), color=ERR, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("Run docker compose down first")
            self.play(FadeIn(compose, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("or add dash dash port 8080")
            self.play(caption_extra(tr, True), run_time=0.2)
            c37 = type_cmd(self, tw9, P8080.cmd, 0.5)
            l34 = tw9.print(self, [P8080.line(34)], run_time=0.3)[0]
            pin_with(self, c37, beside(extra_tag(), tw9, c37),
                     substring(l34, "http://127.0.0.1:8080").animate.set_color(LOOKUP), FadeIn(clash.p8080),
                     GrowArrow(clash.ok), FadeIn(clash.okc, scale=1.3), run_time=0.5)
            self.wait(1.0)                              # the :8080 success state stays readable
            vo.wait_until("Pause, and get the dev UI open")
            self.play(FadeOut(VGroup(wf9, tw9, clash, compose)), caption_extra(tr, False), run_time=0.45)
            self.play(FadeIn(t), FadeIn(back, shift=UP * 0.1), FadeIn(card, shift=UP * 0.15), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tr, t, card, back)), run_time=0.8)
        self.wait(0.3)
