"""S02 · One container, no ports (README "Setup › Start container", steps 1-4, and six extras).
Lecture: none (no lecture tag).

Beats (script.md "## S02", one voiceover block each):
 0  No tracker. CODE(docker-shell.sh: 23–29) along the bottom (20 pt) builds the stage above it
    (V-S02 Stage, rescaled so both fit): the GREY laptop `~/AC215` with `agent-harness/` and the
    dashed `secrets/` ("empty"); line 23 lights TEAL -> the container `agent-harness` (user app,
    /.venv); 24 PINK -> mount `agent-harness → /app` ("live: your edits show inside"); 25 PINK ->
    `secrets → /secrets` (+ "· nothing reads it"); 26–27 dim, GREY "unused today"; 28 GOLD -> the
    key `-e OPENAI_API_KEY` and a GOLD arrow carrying a key into the container; the crossed-out
    port "no -p · no ports"; one PINK HTTPS line to the BLUE cloud "OpenAI".
 1  The stage shrinks to a glyph-only badge (top right). TRACKER Start · extra. Laptop terminal
    (10 rows, prompt ~/AC215$): `git clone …` (extra) -> laptop/01 line 2; `cd agent-harness`
    (extra), the prompt becomes ~/AC215/agent-harness$; chip README.md · line 92 (excerpt) "on your
    host machine, from agent-harness". The terminal clears: `ls -a` (extra) -> laptop/03 lines
    4–20 in three columns of <= 6 rows; a GREY dashed ghost `docs/` "not in the repo".
 2  TRACKER Start 1. `mkdir -p ../secrets` (no output); `ls -la ..; ls -A ../secrets | wc -l`
    (extra) -> laptop/05 lines 5–7, `agent-harness` and `secrets` flash, `0` gets the GREY tag
    "empty"; the badge's secrets/ pulses; chip README.md · line 155 "No GCP service-account setup
    is required". ▶ on a static card (`mkdir -p ../secrets`: the row is too long for the tag).
    Hold 2 s.
 3  TRACKER Start 2. The terminal clears: `export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"` (no output);
    the placeholder gets a YELLOW box, caption "replace it with your key · or skip the line
    offline (README.md · line 104)"; a GOLD key beside the command; GREY note "typed exactly as
    written here · act 1 shows the result".
 4  TRACKER Start 3. The terminal grows to 12 rows: `bash docker-shell.sh` -> laptop/07 lines 2
    (cut), 3, …, 9, 12 cut after "RUN set -ex;", 13–16, … (BuildKit padding squeezed); line 14
    GREEN, "uv" PURPLE. "38.2s" flashes with a GREY tag "ours"; python:3.13-slim-bookworm turns
    ORANGE with the ORANGE tag "base image" and a GREY tag "pre-pulled here" (on the "…" row above
    it: line 9 fills its row); GREY chip "first build: + the base image · a minute or more".
 5  The terminal shrinks to the strip (lines 14–16, the three build steps); CODE(Dockerfile:
    42–48) above it: 42 GREEN "the lockfile first", 45 GREEN, 48 GREY "the code last", lit in
    build order, each with its strip row.
 6  The panel leaves; the terminal grows back: laptop/07 lines 21–26, the prompt
    app@13a6188396ca:/app$ (line 27 cut before " exit"): TEAL frame, title "container ·
    agent-harness". The terminal shrinks to a strip (23, 26, the prompt); CODE(docker-entrypoint.sh:
    6–12) above it: line 6 boxed GREY with the GREY tag "erratum · says activated…", line 12
    GREEN "…activates here". 13a6188396ca underlined PINK, GREY tag "container ID · your numbers
    will differ".
 7  The panel leaves. Chip README.md · line 108 (excerpt) "Run every remaining command inside
    the container, from /app"; it fades; the static ▶ card (export · bash docker-shell.sh · →
    app@…:/app$ · GREEN "offline · free"); the strip's prompt flashes. Hold 2 s.
 8  The card fades; the first terminal dims and a second terminal (10 rows, "laptop · second
    terminal") slides in over it. TRACKER Start 3 · extra. `docker ps` (extra) -> laptop/08
    lines 2–3 split at column 56 (two stacked halves); a YELLOW box over PORTS and its empty cell,
    caption "nothing published". `docker images` (extra) -> laptop/09 line 2 cut after "DISK
    USAGE", line 3 cut after "1.77GB"; 1.77GB underlined; GREY note "the agent framework installs
    every integration".
 9  `docker inspect … | grep -E …` (extra; four rows that paste back as one command: see
    INSPECT_ROWS) -> laptop/10 line 4 only, the earlier output scrolls up; a GOLD underline on
    OPENAI_API_KEY=YOUR_OPENAI_API_KEY, GREY caption "stored in the container's configuration ·
    with a real key, treat it as sensitive".
10  TRACKER Start 4. The second terminal shrinks to the strip; the badge grows back (upper right,
    glyph only; the mounts, folders, port and the first key fade so the key story reads): the
    container's GOLD key "old", a new GOLD key "new" on the laptop. CODE(docker-shell.sh: 13–15)
    above the strip, line 15 YELLOW, GREY chip "no -e here"; a PINK `docker exec` arrow enters
    the container, the new key stays behind (small RED ✕); README.md · line 110 (excerpt) "not
    automatically forwarded by docker exec".
11  The panel and the stage leave; the second terminal grows back (13 rows) and clears: `bash
    docker-shell.sh` -> laptop/12 lines 2–3 joined (wrapped), 4–9 folded; the frame turns TEAL;
    `read -rsp "OpenAI API key: " OPENAI_API_KEY` -> "OpenAI API key: " with the GREY caption
    "type your key here · nothing shows" and a GOLD key dropping in; `export OPENAI_API_KEY`;
    `printf '\\n'` -> an empty line; `echo ${#OPENAI_API_KEY}` (extra) -> 19, caption "its length ·
    never its value · 0 means empty". The terminal fades; the static ▶ card "only if you changed
    the key while the container ran:". Hold 2 s, fade to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    Rectangle,
    RoundedRectangle,
    VGroup,
)

from common import *  # noqa: F401,F403
from common import _drop_bare, _type_rows  # explicit fold of the docker inspect line (see INSPECT_ROWS)
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S02"]

# ------------------------------------------------------------------ the real captures (file line numbers)
CLONE = capture("laptop/01")
assert CLONE.cmd == "git clone https://github.com/dlops-io/agent-harness.git", CLONE.cmd
LS = capture("laptop/03")
assert LS.cmd == "ls -a" and LS.line(4) == ".git" and LS.line(20) == "uv.lock", LS.lines
MKDIR = capture("laptop/04")
assert MKDIR.cmd == "mkdir -p ../secrets" and not MKDIR.lines, MKDIR.lines
WS = capture("laptop/05")
assert WS.cmd == "ls -la ..; ls -A ../secrets | wc -l" and WS.line(7) == "0", WS.lines
EXPORT = capture("laptop/06")
assert EXPORT.cmd == f'export {KEY_VAR}="{KEY_PLACEHOLDER}"' and not EXPORT.lines, EXPORT.cmd
BUILD = capture("laptop/07")
assert BUILD.cmd == "bash docker-shell.sh", BUILD.cmd
assert "Building 38.2s (11/11) FINISHED" in BUILD.line(3), BUILD.line(3)
assert BUILD.line(23) == "Environment ready! Virtual environment activated.", BUILD.line(23)
assert BUILD.cut_before(27, " exit") == P_CTR, BUILD.line(27)
PS = capture("laptop/08")
assert PS.cmd == "docker ps", PS.cmd
IMG = capture("laptop/09")
assert IMG.cmd == "docker images", IMG.cmd
ENV = capture("laptop/10")
assert ENV.line(4) == f"{KEY_VAR}={KEY_PLACEHOLDER}", ENV.line(4)
AGAIN = capture("laptop/12")
assert AGAIN.cmd == "bash docker-shell.sh", AGAIN.cmd
READ = AGAIN.typed(10)
assert READ == 'read -rsp "OpenAI API key: " OPENAI_API_KEY', READ
KEY_ASK, KEY_P, KEY_EXPORT = split_prompt_inside(AGAIN.line(11))
assert KEY_ASK == "OpenAI API key: " and KEY_P == P_CTR and KEY_EXPORT == "export OPENAI_API_KEY"
assert AGAIN.typed(12) == "printf '\\n'" and AGAIN.line(13) == "", AGAIN.line(12)
assert AGAIN.typed(14) == "echo ${#OPENAI_API_KEY}" and AGAIN.line(15) == "19", AGAIN.line(14)
AGAIN_FOLD = AGAIN.fold(4, 9, "Container is running!!! … Activating virtual environment...")

CD = "cd agent-harness"                       # (extra) navigation only: run_steps.sh runs in the clone

# The docker inspect line is 155 characters with a 64-character quoted regex and no space in it:
# the house fold (4-space indent) would have to break inside the quotes. These four rows paste
# back as the one command: three continuation rows end in " \" outside any quotes, and the regex
# row starts at column 0 (a continuation row needs no indent) so it fits the 65 columns.
INSPECT_ROWS = [
    f"{P_REPO} docker inspect \\",
    "    agent-harness --format \\",
    "    '{{range .Config.Env}}{{println .}}{{end}}' | grep -E \\",
    "'^(OPENAI_API_KEY|GCP_PROJECT|GOOGLE_APPLICATION_CREDENTIALS)='",
]
assert all(len(r) <= 65 for r in INSPECT_ROWS), [len(r) for r in INSPECT_ROWS]


def _unfold(rows) -> str:
    """The rows as the shell joins them (a trailing ' \\' + newline + leading spaces -> one space)."""
    out = rows[0][len(P_REPO) + 1:]
    for r in rows[1:]:
        out = out[:-2] + " " + r.lstrip()
    return out


assert _unfold(INSPECT_ROWS) == ENV.cmd, _unfold(INSPECT_ROWS)

# README phrases (exact sub-strings, backticks and bold dropped)
R92 = "on your host machine, from agent-harness"            # README.md:92
R108 = "Run every remaining command inside the container, from /app"   # README.md:108
R155 = "No GCP service-account setup is required"            # README.md:155
assert "on your host machine**, from `agent-harness`" in source_line("README.md", 92)
assert "Run every remaining command inside the container, from `/app`" in source_line("README.md", 108)
assert R155 in source_line("README.md", 155)

# ------------------------------------------------------------------ layout
T_ROWS = 10                    # the laptop terminal in beats 1-3 (top 1.38: two band rows above)
BUILD_ROWS = 12                # the build and the banner (top 2.19)
BAND1_Y, BAND2_Y = 1.85, 2.5   # rows of the band between a 10-row terminal and the tracker
BADGE_W = 2.4
BADGE_C = np.array([6.45 - BADGE_W / 2, 3.12, 0])    # top right (no lecture tag in this scene)
GAP_Y = STRIP_TOP + 0.12       # the lowest y a picture above the 3-row strip uses


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


def at_right(mob, t, line, pad: float = 0.15):
    """mob at the right end of terminal row `line` (a row whose text leaves room there)."""
    row = line.rows[0] if hasattr(line, "rows") else line
    mob.move_to(row.strut).align_to(t.box, RIGHT).shift(LEFT * pad)
    return mob


def code_row(p, n: int):
    """The (first) code row of file line n in a src_panel."""
    return p.code.code_lines[p.rows_of(n)[0]]


def after_code(mob, p, n: int, buff: float = 0.45):
    """mob just right of file line n's text in a src_panel, on that row."""
    r = code_row(p, n)
    mob.next_to(r, RIGHT, buff=buff)
    mob.set_y(r.get_center()[1])
    return mob


def outline(mob, color: str = S.GREY, pad: float = 0.08, stroke: float = 3):
    """An unfilled rounded box around mob (not added)."""
    return RoundedRectangle(width=mob.width + 2 * pad, height=mob.height + 2 * pad, corner_radius=0.08,
                            stroke_color=color, stroke_width=stroke).set_fill(opacity=0).move_to(mob)


def cell_box(top_row, bottom_row, a: int, b: int, color: str = TURN, pad: float = 0.05):
    """An outline over columns a..b (exclusive) of two stacked terminal rows (a header and its cell)."""
    from explainer.devops import cell_width
    cw = cell_width(top_row.pt)
    x0 = grid_x0(top_row) + a * cw
    y_top = top_row.strut.get_top()[1] + pad
    y_bot = bottom_row.strut.get_bottom()[1] - pad
    r = RoundedRectangle(width=(b - a) * cw + 2 * pad, height=y_top - y_bot, corner_radius=0.07,
                         stroke_color=color, stroke_width=3).set_fill(opacity=0)
    r.move_to([x0 + (b - a) * cw / 2, (y_top + y_bot) / 2, 0])
    return r


def ls_columns(cap, first: int = 4, last: int = 20, per_col: int = 6) -> list[str]:
    """`ls -a` as it prints in a wide terminal: the names (file lines first..last, the capture's
    order) down three columns of <= per_col rows, each column two spaces wider than its longest name."""
    names = [cap.line(n) for n in range(first, last + 1)]
    cols = [names[i:i + per_col] for i in range(0, len(names), per_col)]
    widths = [max(len(s) for s in c) + 2 for c in cols]
    rows = []
    for i in range(per_col):
        cells = [c[i].ljust(w) if i < len(c) else "" for c, w in zip(cols, widths)]
        rows.append("".join(cells).rstrip())
    assert sorted(" ".join(rows).split()) == sorted(names)
    return rows


def flash(mob, color: str = TURN, k: float = 1.15):
    return Indicate(mob, color=color, scale_factor=k)


class OneContainer(VoiceScene):
    def construct(self):
        assert len(SAY) == 12, len(SAY)

        # ========================================================== 0 · the stage, built from docker-shell.sh
        p0 = src_panel("docker-shell.sh", 23, 29, size=20)
        place(p0, cx=0, bottom=-3.45)
        stage = Stage(show=())
        avail = 3.55 - (p0.get_top()[1] + 0.15)
        k0 = min(1.0, avail / stage.height)
        stage.rescale(k0)
        place(stage, cx=0, top=3.55)
        # rescaled, the stage keeps its text size: "live: your edits show inside" would end under the
        # mount arrow, so it sits a little lower (still between agent-harness/ and secrets/)
        stage.parts["mount_app"][1].shift(DOWN * 0.15)
        # my additions to the stage (members, so they shrink and grow with it)
        sec_note = stage.parts["secrets"][2]                       # "empty"
        nreads = note("· nothing reads it").next_to(sec_note, RIGHT, buff=0.12)
        stage.part("nreads", nreads, shown=False)
        venv = stage.ctr_rows[3]                                    # "/.venv"
        k_in = key_glyph(0.24, KEY)
        k_in.next_to(venv, DOWN, buff=0.2).align_to(venv, LEFT).shift(RIGHT * 0.05)
        stage.part("k_in", k_in, shown=False)
        kp = stage.parts["key"]
        k_arr = Arrow(kp.get_right() + RIGHT * 0.12, k_in.get_left() + LEFT * 0.06, buff=0, color=KEY,
                      stroke_width=3, tip_length=0.15, max_tip_length_to_length_ratio=0.2)
        stage.part("k_arrow", k_arr, shown=False)
        bars0 = {n: p0.bar(n, c, 0.22) for n, c in ((23, CTR), (24, LOOKUP), (25, LOOKUP), (28, KEY))}
        unused = note("unused today")
        after_code(unused, p0, 27)
        with self.voiceover(SAY[0]) as vo:
            stage.reveal(self, "laptop", run_time=0.6, extra=[FadeIn(p0, shift=UP * 0.15)])
            stage.reveal(self, "repo", run_time=0.5)
            vo.wait_until("with an empty secrets")
            stage.reveal(self, "secrets", run_time=0.5)
            vo.wait_until("One container mounts both")
            stage.reveal(self, "container", run_time=0.6, extra=[FadeIn(bars0[23])])
            stage.reveal(self, "mount_app", run_time=0.6, extra=[FadeIn(bars0[24])])
            stage.reveal(self, "mount_secrets", "nreads", run_time=0.6, extra=[FadeIn(bars0[25])])
            vo.wait_until("your key goes in")
            self.play(*[code_row(p0, n).animate.set_opacity(0.35) for n in (26, 27)], FadeIn(unused),
                      run_time=0.4)
            stage.reveal(self, "key", run_time=0.5, extra=[FadeIn(bars0[28])])
            stage.reveal(self, "k_arrow", run_time=0.5, anim=GrowArrow)
            stage.reveal(self, "k_in", run_time=0.4)
            vo.wait_until("no port is published")
            stage.reveal(self, "port", run_time=0.6)
            self.play(flash(stage.parts["port"][0], TURN, 1.3), run_time=0.7)
            vo.wait_until("and the app's only call out")
            stage.reveal(self, "https", run_time=0.7)
            stage.reveal(self, "cloud", run_time=0.6)

        # ========================================================== 1 · two extras: clone, cd; ls -a
        tr = tracker("Start", None)
        t = term(P_WS, rows=T_ROWS, title=LAPTOP_TITLE)
        c92 = readme_chip("README.md · line 92 (excerpt)", R92)
        place(c92, left=-6.3, cy=BAND2_Y)
        ls_rows = ls_columns(LS)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(p0, unused, *bars0.values())), FadeIn(tr, shift=DOWN * 0.25),
                      run_time=0.5)
            stage.shrink(self, width=BADGE_W, center=BADGE_C, run_time=0.9)
            self.play(FadeIn(t, shift=UP * 0.2), caption_extra(tr, True), run_time=0.5)
            vo.wait_until("git clone")
            cl = type_cmd(self, t, CLONE.cmd, 1.0)
            ex1 = at_right(extra_tag(), t, cl)
            pin(self, cl.rows[0], ex1, run_time=0.3)
            t.print(self, CLONE.at(2), run_time=0.4)
            vo.wait_until("then change into")
            cdl = type_cmd(self, t, CD, 0.5)
            pin(self, cdl, beside(extra_tag(), t, cdl), run_time=0.3)
            cd_prompt(self, t, P_REPO, run_time=0.7)
            vo.wait_until("where every setup")
            self.play(FadeIn(c92, shift=DOWN * 0.1), run_time=0.5)
            self.play(flash(c92.phrase, TURN, 1.04), run_time=0.7)
            vo.wait_until("A listing shows")
            self.play(FadeOut(c92), run_time=0.3)
            t.clear(self)
            lsl = type_cmd(self, t, LS.cmd, 0.3)
            pin(self, lsl, beside(extra_tag(), t, lsl), run_time=0.3)
            lrows = t.print(self, ls_rows, run_time=0.5)
            bare_prompt(self, t)
            vo.wait_until("that matters later")
            ghost = ghost_file("docs/")
            gnote = note("not in the repo")
            gg = VGroup(ghost, gnote).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            place(gg, left=max(r.get_right()[0] for r in lrows) + 0.7, cy=lrows[2].strut.get_bottom()[1])
            self.play(FadeIn(gg, shift=LEFT * 0.15), run_time=0.5)

        # ========================================================== 2 · step 1: mkdir -p ../secrets
        c155 = readme_chip("README.md · line 155", R155)
        place(c155, left=-6.3, cy=BAND2_Y)
        card2 = turn_card([MKDIR.cmd])
        place(card2, right=6.2, bottom=t.box.get_top()[1] + 0.12)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(gg), tr.goto(1), run_time=0.5)
            type_cmd(self, t, MKDIR.cmd, 0.6)
            bare_prompt(self, t)
            vo.wait_until("one level up")
            wsl = type_cmd(self, t, WS.cmd, 1.0)
            pin(self, wsl, beside(extra_tag(), t, wsl), run_time=0.3)
            out2 = show(self, t, WS, (5, 7), run_time=0.5)
            r5, r6, r7 = out2
            self.play(flash(substring(r5, "agent-harness")), flash(substring(r6, "secrets")), run_time=0.7)
            vo.wait_until("Nothing reads it")
            pin(self, r7, beside(grey_tag("empty"), t, r7), run_time=0.4)
            bare_prompt(self, t)
            sec_badge = VGroup(stage.parts["secrets"][0], stage.parts["secrets"][1][0])
            self.play(Indicate(sec_badge, color=TURN, scale_factor=1.6), run_time=0.8)
            vo.wait_until("so no service account")
            self.play(FadeIn(c155, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Pause and run it")
            self.play(FadeIn(card2, shift=UP * 0.1), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame

        # ========================================================== 3 · step 2: export the key
        cap3 = VGroup(label("replace it with your key · or skip the line offline", CAPTION, INK),
                      note("(README.md · line 104)")).arrange(RIGHT, buff=0.18)
        place(cap3, left=-6.25, cy=BAND2_Y)
        cap3b = note("typed exactly as written here · act 1 shows the result")
        place(cap3b, left=-6.25, cy=BAND1_Y)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(c155, card2)), tr.goto(2), run_time=0.5)
            t.clear(self)
            ex = type_cmd(self, t, EXPORT.cmd, 1.0)
            exr = ex.rows[-1] if hasattr(ex, "rows") else ex
            kg3 = beside(key_glyph(0.26, KEY), t, exr, buff=0.35)
            pin(self, exr, kg3, run_time=0.4, anim=FadeIn(kg3, shift=LEFT * 0.15))
            bare_prompt(self, t)
            vo.wait_until("Replace the placeholder")
            a = exr.text.index(KEY_PLACEHOLDER)
            pbox = col_box(exr, a, a + len(KEY_PLACEHOLDER), TURN)
            pin(self, exr, pbox, run_time=0.5, anim=Create(pbox))
            self.play(FadeIn(cap3[0], shift=DOWN * 0.1), FadeIn(cap3[1]), run_time=0.5)
            vo.wait_until("or skip this line")
            self.play(flash(cap3[0], TURN, 1.03), run_time=0.8)
            vo.wait_until("We typed it as written")
            self.play(FadeIn(cap3b, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("act 1 shows")
            self.play(flash(kg3, TURN, 1.3), run_time=0.7)

        # ========================================================== 4 · step 3: bash docker-shell.sh
        b_lines = BUILD.out(BUILD.line(2), BUILD.squeeze(3), "…", BUILD.squeeze(9),
                            BUILD.cut(12, "RUN set -ex;"), BUILD.squeeze(13), (BUILD.squeeze(14), HARNESS),
                            BUILD.squeeze(15), BUILD.squeeze(16), "…")
        chip4 = chip("first build: + the base image · a minute or more", S.GREY, size=CAPTION)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(cap3, cap3b)), tr.goto(3), run_time=0.5)
            resize(self, t, BUILD_ROWS, run_time=0.5)
            place(chip4, left=-6.3, cy=(t.box.get_top()[1] + tr.get_bottom()[1]) / 2)
            vo.wait_until("bash docker-shell.sh")
            type_cmd(self, t, BUILD.cmd, 0.7)
            vo.wait_until("builds the image")
            out4 = t.print(self, b_lines, run_time=0.9, lag=0.12)
            r3, rdots, r9, r14, r15, r16 = out4[1], out4[2], out4[3], out4[6], out4[7], out4[8]
            self.play(substring(r15, "uv").animate.set_color(TOOL), run_time=0.4)
            vo.wait_until("Ours took 38 seconds")
            s38 = substring(r3, "38.2s")
            self.play(s38.animate.set_color(TURN), flash(s38, TURN, 1.2), run_time=0.6)
            pin(self, r3, beside(grey_tag("ours"), t, r3, buff=0.35), run_time=0.4)
            vo.wait_until("with the base image")
            img = substring(r9, "python:3.13-slim-bookworm")
            base = tag("base image", SYSTEM)
            base.move_to(rdots.strut).set_x(img.get_center()[0])
            pre = grey_tag("pre-pulled here")
            pre.move_to(rdots.strut).next_to(base, LEFT, buff=0.2)
            self.play(img.animate.set_color(SYSTEM), run_time=0.4)
            pin(self, rdots, base, run_time=0.4, anim=FadeIn(base, shift=DOWN * 0.08))
            pin(self, rdots, pre, run_time=0.4)
            vo.wait_until("your first build")
            self.play(FadeIn(chip4, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("so expect")
            self.play(flash(chip4, TURN, 1.04), run_time=0.8)

        # ========================================================== 5 · the Dockerfile: the lockfile before the code
        p5 = src_panel("Dockerfile", 42, 48)
        place(p5, cx=0, bottom=GAP_Y)
        bars5 = [p5.bar(42, HARNESS, 0.22), p5.bar(45, HARNESS, 0.22), p5.bar(48, S.GREY, 0.22)]
        n42 = after_code(label("the lockfile first", CAPTION, HARNESS), p5, 42)
        n48 = after_code(label("the code last", CAPTION, S.GREY), p5, 48)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(chip4), run_time=0.3)
            resize(self, t, 3, keep=[r14, r15, r16], run_time=0.6)
            self.play(FadeIn(p5, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("from the lockfile")
            self.play(FadeIn(bars5[0]), FadeIn(n42, shift=LEFT * 0.1), flash(r14, HARNESS, 1.03), run_time=0.6)
            vo.wait_until("before it copies")
            self.play(FadeIn(bars5[1]), flash(r15, TURN, 1.03), run_time=0.5)
            self.play(FadeIn(bars5[2]), FadeIn(n48, shift=LEFT * 0.1), flash(r16, TURN, 1.03), run_time=0.5)
            vo.wait_until("the layer trick")
            self.play(*[flash(b, TURN, 1.02) for b in bars5], run_time=0.8)

        # ========================================================== 6 · the banner's slip; the container ID
        p6 = src_panel("docker-entrypoint.sh", 6, 12)
        place(p6, cx=0, bottom=GAP_Y)
        box6 = outline(code_row(p6, 6), S.GREY, pad=0.07)
        err6 = erratum_tag("says activated…")
        place(err6, right=p6.code.get_right()[0], cy=p6.header.get_center()[1])
        bar12 = p6.bar(12, HARNESS, 0.22)
        n12 = after_code(label("…activates here", CAPTION, HARNESS), p6, 12)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(p5, n42, n48, *bars5)), run_time=0.4)
            resize(self, t, BUILD_ROWS, run_time=0.6)
            ban = t.print(self, BUILD.at((21, 26)), run_time=0.6)
            r23, r26 = ban[2], ban[5]
            t.set_prompt(P_CTR)
            pr = bare_prompt(self, t)
            self.play(*enter_container(t), run_time=0.6)
            self.play(flash(substring(r23, "activated"), TURN, 1.2), run_time=0.6)
            vo.wait_until("before the script")
            resize(self, t, 3, keep=[r23, r26, pr], run_time=0.6)
            self.play(FadeIn(p6, shift=UP * 0.15), run_time=0.5)
            self.play(Create(box6), FadeIn(err6, shift=DOWN * 0.08), run_time=0.5)
            self.play(FadeIn(bar12), FadeIn(n12, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("a harmless slip")
            self.play(flash(err6, TURN, 1.08), run_time=0.6)
            vo.wait_until("After the at sign")
            cid = substring(pr, CTR_ID)
            ucid = under(cid, LOOKUP, stroke=4)
            self.play(flash(cid, LOOKUP, 1.15), run_time=0.6)
            pin(self, pr, ucid, run_time=0.4, anim=Create(ucid))
            pin(self, pr, beside(grey_tag("container ID · your numbers will differ"), t, pr, buff=0.3), run_time=0.4)
            self.play(cid.animate.set_color(LOOKUP), run_time=0.3)

        # ========================================================== 7 · inside the container from now on; ▶
        c108 = readme_chip("README.md · line 108 (excerpt)", R108)
        place(c108, cx=0, cy=0.7)
        card7 = turn_card([(EXPORT.cmd, "your key · or skip it offline"), BUILD.cmd,
                           ["→", "`app@…:/app$`"], (Prose("offline · free"), HARNESS)])
        place(card7, cx=0, cy=(2.7 + GAP_Y) / 2 - 0.1)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(p6, box6, err6, bar12, n12)), run_time=0.4)
            self.play(FadeIn(c108, shift=DOWN * 0.1), run_time=0.5)
            self.play(flash(c108.phrase, TURN, 1.03), run_time=0.8)
            vo.wait_until("Pause, run steps")
            self.play(FadeOut(c108), run_time=0.3)
            self.play(FadeIn(card7, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and wait for this prompt")
            self.play(flash(glyph_range(pr, 0, len(P_CTR)), TURN, 1.12), run_time=0.8)
        self.wait(2)                                    # ▶ beat: hold the frame

        # ========================================================== 8 · a second terminal: docker ps, docker images
        t2 = term(P_REPO, rows=T_ROWS, title=SECOND)
        ps_rows = [*PS.split_at(2, 56)[:1], *PS.split_at(3, 56)[:1], PS.split_at(2, 56)[1], PS.split_at(3, 56)[1]]
        n8 = note("the agent framework installs every integration")
        place(n8, left=-6.25, cy=BAND1_Y)
        with self.voiceover(SAY[8]) as vo:
            veil = Rectangle(width=t.box.width + 0.08, height=t.box.height + 0.08).set_stroke(width=0)
            veil.set_fill(S.BG, 0.7).move_to(t.box)
            self.play(FadeOut(card7), FadeIn(veil), run_time=0.5)
            self.play(FadeIn(t2, shift=UP * 0.4), run_time=0.6)
            self.remove(t, veil)                        # covered by the second terminal
            bare_prompt(self, t2)
            self.play(caption_extra(tr, True), run_time=0.4)
            vo.wait_until("Docker ps")
            psl = type_cmd(self, t2, PS.cmd, 0.4)
            pin(self, psl, beside(extra_tag(), t2, psl), run_time=0.3)
            out8 = t2.print(self, ps_rows, run_time=0.5)
            rc, rd = out8[2], out8[3]
            bare_prompt(self, t2)
            vo.wait_until("no ports")
            a, b = rc.text.index("PORTS"), rc.text.index("NAMES") - 1
            assert rd.text[a:b].strip() == "", rd.text
            pbx = cell_box(rc, rd, a, b, TURN)
            self.play(Create(pbx), substring(rc, "PORTS").animate.set_color(TURN), run_time=0.5)
            nothing = beside(note("nothing published"), t2, rd, buff=0.4)
            self.play(FadeIn(nothing, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("Docker images")
            iml = type_cmd(self, t2, IMG.cmd, 0.5)
            pin(self, iml, beside(extra_tag(), t2, iml), run_time=0.3)
            out8b = t2.print(self, [IMG.cut(2, "DISK USAGE"), IMG.cut(3, "1.77GB")], run_time=0.4)
            ri = out8b[1]
            bare_prompt(self, t2)
            vo.wait_until("1.77 gigabytes")
            gb = substring(ri, "1.77GB")
            ugb = under(gb, TURN, stroke=4)
            self.play(flash(gb, TURN, 1.2), run_time=0.6)
            pin(self, ri, ugb, run_time=0.4, anim=Create(ugb))
            vo.wait_until("since the framework")
            self.play(FadeIn(n8, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 9 · docker inspect: the key in the configuration
        cap9 = note("stored in the container's configuration · with a real key, treat it as sensitive")
        place(cap9, left=-6.25, cy=BAND1_Y)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(n8, pbx, nothing)), substring(rc, "PORTS").animate.set_color(OUTPUT),
                      run_time=0.4)
            _drop_bare(self, t2)
            ins = _type_rows(self, t2, INSPECT_ROWS, len(P_REPO) + 1, 1.6, len(ENV.cmd))
            pin(self, ins.rows[0], at_right(extra_tag(), t2, ins.rows[0]), run_time=0.3)
            out9 = show(self, t2, ENV, 4, run_time=0.4)
            rk = out9[0]
            bare_prompt(self, t2)
            vo.wait_until("in the container's configuration")
            uk = under(rk.glyphs, KEY, stroke=4)
            self.play(flash(substring(rk, KEY_VAR), KEY, 1.12), run_time=0.6)
            pin(self, rk, uk, run_time=0.4, anim=Create(uk))
            vo.wait_until("treat a real key")
            self.play(FadeIn(cap9, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 10 · step 4: docker exec doesn't bring a new key
        p10 = src_panel("docker-shell.sh", 13, 15, size=20, wrap=True)
        place(p10, left=-6.3, bottom=GAP_Y)
        bar15 = p10.bar(15, TURN, 0.22)
        noe = grey_tag("no -e here")
        after_code(noe, p10, 15, buff=0.25)
        if noe.get_right()[0] > 6.45:                      # no room after line 15: on the header row
            place(noe, right=p10.code.get_right()[0], cy=p10.header.get_center()[1])
        q110 = quote_card(110, lines=["not automatically forwarded", "by `docker exec`"],
                          header="README.md · line 110 (excerpt)", expected=False)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(cap9), tr.goto(4), run_time=0.5)
            resize(self, t2, 3, run_time=0.6)
            # the badge grows back, glyph only; what isn't about the key fades so the key story reads
            top = 3.52
            bottom = p10.get_top()[1] + 0.12
            h10 = top - bottom
            w10 = h10 * stage.width / stage.height
            c10 = np.array([6.4 - w10 / 2, (top + bottom) / 2, 0])
            stage.hide(self, "mount_app", "mount_secrets", "repo", "secrets", "nreads", "port", "key", "k_arrow",
                       run_time=0.3)
            self.play(stage.animate.scale(w10 / stage.width).move_to(c10), run_time=0.8)
            zone = stage.parts["laptop"][0]
            frame = stage.ctr.frame
            old = label("old", CAPTION, KEY).next_to(k_in, RIGHT, buff=0.12)
            nk = key_glyph(0.26, KEY)
            nk_t = label("new", CAPTION, KEY)
            nkg = VGroup(nk, nk_t).arrange(RIGHT, buff=0.12)
            place(nkg, left=zone.get_left()[0] + 0.3, cy=k_in.get_center()[1])
            vo.wait_until("when you changed the key")
            self.play(FadeIn(old, shift=LEFT * 0.08), flash(k_in, TURN, 1.4), run_time=0.5)
            self.play(FadeIn(nkg, scale=1.2), run_time=0.5)
            vo.wait_until("the script then only")
            self.play(FadeIn(p10, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(bar15), FadeIn(noe, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("docker exec")
            y_ex = frame.get_center()[1] + 0.12
            dx = Arrow([zone.get_left()[0] + 0.35, y_ex, 0], [frame.get_left()[0] + 0.05, y_ex, 0], buff=0,
                       color=LOOKUP, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.2)
            dx_t = mono("docker exec", CAPTION, LOOKUP).next_to(dx, UP, buff=0.08).align_to(dx, LEFT)
            self.play(GrowArrow(dx), FadeIn(dx_t), run_time=0.6)
            vo.wait_until("which doesn't bring")
            xm = cross_mark(0.2, ERR, 4).next_to(nk_t, RIGHT, buff=0.15)
            self.play(Create(xm), flash(nkg, ERR, 1.15), run_time=0.6)
            place(q110, left=-6.3, top=tr.get_bottom()[1] - 0.3)
            self.play(FadeIn(q110, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 11 · step 4's three lines; ▶
        card11 = turn_card([BUILD.cmd, READ, KEY_EXPORT, AGAIN.typed(12), Prose("keep working in this shell"),
                            (Prose("offline · free"), HARNESS)],
                           header="only if you changed the key while the container ran:", width=9.0)
        place(card11, cx=0, cy=-0.2)
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(VGroup(stage, old, nkg, xm, dx, dx_t, p10, bar15, noe, q110)), run_time=0.5)
            t2.clear(self, run_time=0.2)
            resize(self, t2, 13, run_time=0.6)
            vo.wait_until("shell in from")
            type_cmd(self, t2, AGAIN.cmd, 0.6)
            t2.print(self, [AGAIN.join(2, 3), AGAIN_FOLD], wrap=True, run_time=0.5)
            t2.set_prompt(P_CTR)
            bare_prompt(self, t2)
            self.play(*enter_container(t2), run_time=0.5)
            vo.wait_until("type the README's")
            type_cmd(self, t2, READ, 0.9)
            ask = t2.print(self, [(KEY_ASK, OUTPUT)], run_time=0.3)[0]
            vo.wait_until("the key goes in hidden")
            hid = beside(note("type your key here · nothing shows"), t2, ask, buff=0.2)
            kd = key_glyph(0.26, KEY)
            kd.next_to(hid, RIGHT, buff=0.3).set_y(ask.strut.get_center()[1])
            pin(self, ask, hid, run_time=0.4, anim=FadeIn(hid, shift=LEFT * 0.1))
            pin(self, ask, kd, run_time=0.5, anim=FadeIn(kd, shift=DOWN * 0.6))
            vo.wait_until("and out of your history")
            t2.set_prompt(KEY_P)
            type_cmd(self, t2, KEY_EXPORT, 0.5)
            session(self, t2, AGAIN, 12, 13, type_time=0.4, out_time=0.2)
            vo.wait_until("Keep working")
            ech = session(self, t2, AGAIN, 14, type_time=0.5)[14]
            pin(self, ech, beside(extra_tag(), t2, ech), run_time=0.3)
            r19 = show(self, t2, AGAIN, 15, run_time=0.3)[0]
            pin(self, r19, beside(note("its length · never its value · 0 means empty"), t2, r19, buff=0.4),
                run_time=0.4)
            vo.wait_until("Pause here")
            self.play(FadeOut(t2), run_time=0.4)
            self.play(FadeIn(card11, shift=UP * 0.1), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tr, card11)), run_time=0.6)
        self.wait(0.3)
