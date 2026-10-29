"""S16 · Tear down, recap, and what's next (README "7 · Additional Resources": the CLI help and the
end-of-lecture reflection; the teardown, all extras; the lecture's action boundary filled in; five
test-yourself questions; what comes next). Lecture: 22.

Beats (script.md "## S16", one voiceover block each):
0  TRACKER Res 1. The container terminal (11 rows, TEAL, GREEN title-bar tag "offline · free") at
   the container prompt types `python cli.py --help` -> container/90 lines 2–3, …, 21–22 (cut at
   the row's end with …, as the script's TERM rule says), then the prompt. On "every option in one
   place" a YELLOW outline runs round the usage rows.
1  The terminal shrinks to the 3-row strip (the command, the usage row, the prompt). Above it a
   card redrawn from README.md · lines 807–814 (header, "What persists between commands?", tag
   expected): a GREEN SQLite cylinder "persists" / "runs, events, traces · live memory" (on "stay in
   SQLite"); a GREY box "one process" / "inventory · mock orders · approval tickets · pending
   workflows" (on "Inventory", its title flashes on "last for one process"); inside it a smaller
   GREY box "one session" / "tasks · history" (on "tasks and history").
2  The card leaves; TRACKER Down 1; the S02 stage badge (glyph only) fades in top right; the
   terminal grows back to 11 rows. On "Type exit" the GREY chip "a second container shell open? exit
   it too" (band above the terminal); `exit` (extra) -> laptop/07 line 28; the frame turns GREY,
   title `laptop`, prompt `student@laptop:~/AC215/agent-harness$`. On "it was started" (the SAY
   names --rm before docker ps -a) the chip gives way to the GREY caption "started with --rm
   (docker-shell.sh · line 23): the container deleted itself", and in the badge the TEAL container
   fades out with its mounts, its no-ports mark and its HTTPS line (the laptop folders and the
   cloud stay); on "so nothing is left" TRACKER Down 2 and `docker ps -a` (extra) -> laptop/13
   line 2 (only the header row).
3  TRACKER Down 3. `ls -la outputs/ outputs/reports/; git status --short; git status --short
   --ignored | grep outputs` (extra; folds onto three rows) -> laptop/14 lines 2, 10–11, 13–14, …,
   23 (YELLOW), 24 (11 rows with the command). On "Its trace database" `observability.sqlite`
   turns PINK and underlined, and the band shows the GREY tag "your prompts and outputs · keys
   redacted" over the GREY source "formaggio/operations/observability.py · line 30". On "delete it"
   the YELLOW tag "your copy" beside `?? prompts/shop_assistant_v2.md` and the GREY tag "git-ignored
   (.gitignore · line 64)" beside `!! outputs/`.
4  TRACKER Down 4. `docker image rm agent-harness` (extra) -> laptop/15 lines 2–3 (3 cut at the
   row's end with ` …`); on "frees most" the GREY chip "frees up to 1.77 GB · base image stays" (its
   end flashes on "the base image"). On "Then close the terminal" the GOLD key in the badge
   flashes inside a GOLD ring and fades; the terminal, the chip
   and the badge fade; the static GREY "your turn" card (header "teardown · every step an extra"):
   `exit` (in each container shell) · `docker ps -a` · `docker image rm agent-harness` · "delete
   outputs/ when done" · "key: not in files, commits or shell history · close its terminal · watch
   your OpenAI usage" · "Colab: Runtime › Disconnect and delete runtime" (tag illustration) · GREEN
   "offline · free", ▶ your turn. The key row's "not in files, commits or shell history" flashes
   on "keep it out of files", its "watch your OpenAI usage" on "and watch your usage", the Colab
   row on "In Colab", the ▶ tag on "Pause". Hold 2 s.
5  LECTURE 22. The card fades; V1's action boundary full size (no move arrows), every GREEN cell
   filled with the recap texts; each row lights YELLOW (its pill, and its GREEN text flashes) as the
   SAY names it: control, tools, context & memory, verification, sub agents.
6  The light goes out; the BLUE cells dim (outline, fill and text; their header stays and
   flashes); on "On the right" the
   GREEN cells brighten and their header flashes; on "and where it matters" the GREEN texts of
   Control flow (the graph's manager review) and Tools (approval on save) move left and two YELLOW
   "a human decides" stamps land at those cells' right ends.
7  TRACKER Res 2. The table's texts and the stamps fade, then the table shrinks to a glyph-only
   copy bottom right (the lecture tag stays with it). A card redrawn from README.md · lines 820–826
   ("End-of-lecture reflection", tag expected): the five questions, each after its concept in bold;
   on "Pick one run" the GREY caption "pick one run you did" under it.
8  The card, the caption, the small table and the lecture tag leave. "Test yourself"; the five
   recap questions build one numbered list that stays, each writing in with a YELLOW badge as the
   SAY reads its short form (the previous badge turns GREY; the last one on "Pause and try
   them"); on "answers are in" the GREY caption "answers in exercises.md" under the list. Hold 3 s.
9  The list leaves. Two GREY dashed cards: "L08 · fine-tuning on Agent Platform (formerly Vertex
   AI) · a service account again" (its middle flashes on "formerly Vertex AI") and, on "Lecture 9",
   "L09 · testing code with pytest · 281 offline unittest tests to copy" (its end flashes on
   "these 281 tests"); on "and are a good model" the footer "study guide and exercises:
   MLOps_Learning · guides/L07-agents-2-harness.md" and the GREY chip "if a step fails: README ›
   Troubleshooting (lines 828–839)". Hold 3 s; everything fades to an empty frame.

Deviations from SHOW (see the scene report): the terminal has 11 rows, not 12, so the band above it
holds the observability tag and its source on two rows (one row would be 13.6 wide) and clears the
badge; laptop/14's four `ls -la` rows are 65–74 characters, so each is folded to
"<permissions>  … <size> <date> <name>" (the "1 student student" columns become a GREY …: the line's
own text, `Capture.fold` checks it), or the file names, which the beat is about, would be cut off;
in the badge the container's mounts, its no-ports mark and its HTTPS line fade with it (arrows into
an empty spot would read as a running container); the turn card has a GREY header "teardown · every
step an extra" instead of three `extra` tags; the reflection card quotes the README's five questions
in full (they fit at 20 pt, and a viewer answering them needs the whole question); recap question 2
spells "labeled" (script.md: American spelling on screen).
"""

import re

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Circumscribe,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    RoundedRectangle,
    Text,
    VGroup,
)

from common import *  # noqa: F401,F403
from common import _header_text, _md_text
from explainer import style as S
from explainer.devops import box, chip, label, line_pitch, mono, step_badge, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S16"]

# ------------------------------------------------------------------ the real captures (file line numbers)
HELP = capture("container/90")
SHELL = capture("laptop/07")
PS = capture("laptop/13")
OUTS = capture("laptop/14")
RMI = capture("laptop/15")
assert HELP.cmd == "python cli.py --help", HELP.cmd
assert HELP.line(2).startswith("usage: cli.py [-h]") and HELP.line(22) == "recorded steps."
assert SHELL.cut_before(27, " exit") == P_CTR and SHELL.typed(27) == "exit" and SHELL.line(28) == "exit"
assert PS.cmd == "docker ps -a" and len(PS.lines) == 1 and PS.line(2).startswith("CONTAINER ID")
LS_CMD = "ls -la outputs/ outputs/reports/; git status --short; git status --short --ignored | grep outputs"
assert OUTS.cmd == LS_CMD, OUTS.cmd
assert OUTS.line(2) == "outputs/:" and OUTS.line(23) == "?? prompts/shop_assistant_v2.md" and OUTS.line(24) == "!! outputs/"
assert RMI.cmd == "docker image rm agent-harness" and RMI.line(2) == "Untagged: agent-harness:latest"
RM3 = RMI.line(3)[:63] + " …"                   # cut at the row's end (65 columns) with " …"
assert RMI.line(3).startswith(RM3[:-2]) and len(RM3) == 65


def ls_fold(n: int) -> str:
    """An `ls -la` row of laptop/14 in one 65-column row: '<permissions>  … <size> <date> <name>'
    (the link count, owner and group become a GREY '…'; the size stays right-aligned)."""
    s = OUTS.line(n)
    m = re.fullmatch(r"(\S{10})  1 student student(\s+\d+ \w{3} \d\d \d\d:\d\d \S+)", s)
    assert m, s
    return OUTS.fold(n, n, f"{m.group(1)}  …{m.group(2)}")


LS_ROWS = {n: ls_fold(n) for n in (10, 11, 13, 14)}
assert all(len(r) <= 65 for r in LS_ROWS.values()), LS_ROWS
assert LS_ROWS[14].endswith(" observability.sqlite")

# ------------------------------------------------------------------ sources (checked)
assert "--rm" in source_line("docker-shell.sh", 23)
assert source_line(".gitignore", 64) == "outputs/"
OBS_PY = "formaggio/operations/observability.py"
assert "redaction" in source_line(OBS_PY, 30)
_R = readme(807, 814)
assert "Persist in `outputs/observability.sqlite`" in _R[2] and "Persist in `outputs/customer_memory.sqlite`" in _R[3]
assert _R[6].startswith("| Inventory changes, mock orders, approval tickets, and pending workflows | In memory for the current process")
assert _R[7].startswith("| Harness task list and conversation history | Current session")
REFLECT = []                                    # README.md 822-826: (concept, its question)
for _ln in readme(822, 826):
    _m = re.fullmatch(r"\d\. \*\*(.+?):\*\* (.+)", _ln)
    assert _m, _ln
    REFLECT.append((_m.group(1), _m.group(2)))
assert [c for c, _ in REFLECT] == ["Context Engineering", "Agent Harness", "Skills", "Agent Systems", "Evaluation"]
assert "Choose one completed run" in readme(820, 820)[0]
assert readme(828, 828)[0] == "## Troubleshooting" and readme(839, 839)[0].startswith("| Changes to host")

# the recap questions (script.md S16; BRIEF.md "Recap questions"; exercises.md Part A)
QUESTIONS = [
    'Name three things `.without("trace")` does not remove.',
    "Why does retrieved context enter as a user message labeled “data, not instructions” — and what "
    "still decides whether a cart is valid?",
    "What is a manager approval bound to, and why was `request-2` blocked although it was approved?",
    "Of tasks, history, memory, approval and audit, which can authorize an action — and who writes "
    "memory here?",
    "Your fixture batch passed 4/4. What does that establish, and what doesn't it?",
]
Q_ANCHORS = ("What survives", "Why does retrieved", "What is an approval", "Which state", "And what does")

# ------------------------------------------------------------------ layout
T_ROWS = 11                                       # the terminal (top 1.79): the band above holds two rows
TRACK_BOTTOM = 2.925
BAND_Y = (strip_top(T_ROWS) + TRACK_BOTTOM) / 2   # one chip row between tracker and terminal
BAND_HI, BAND_LO = 2.58, 2.05                     # two rows (beat 3)
BADGE_W = 3.0
X_LEFT = -6.3
MINI = np.array([4.95, -2.6, 0])                  # the shrunk action boundary (bottom right)


# ------------------------------------------------------------------ small helpers (S14's idiom)
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


def inside(m, x0: float = -6.55, x1: float = 6.55, y0: float = -3.55, y1: float = 3.55):
    assert m.get_left()[0] >= x0 and m.get_right()[0] <= x1 and m.get_bottom()[1] >= y0 and m.get_top()[1] <= y1, \
        (m.get_corner(DOWN + LEFT), m.get_corner(UP + RIGHT))


def apart(a, b, gap: float = 0.06):
    """Assert that the bounding boxes of a and b are at least `gap` apart (no overlap)."""
    ok = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
          or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    assert ok, (a.get_corner(DOWN + LEFT), a.get_corner(UP + RIGHT), b.get_corner(DOWN + LEFT), b.get_corner(UP + RIGHT))


def fit(scene, t, rows: int, keep=None, tags=(), run_time: float = 0.8):
    """resize(), with the title-bar tags riding along on the bar (S08's / S13's / S14's idiom)."""
    y = strip_top(rows) - t.bar_h / 2
    title, t.title = t.title, None
    try:
        resize(scene, t, rows, keep=keep, run_time=run_time,
               extra=[title.animate.set_y(y), *[m.animate.set_y(y) for m in tags]])
    finally:
        t.title = title


def pin_tag(scene, t, line, tag_, run_time: float = 0.35):
    """beside() + pin(): a tag right after a line's text (its last row when folded)."""
    beside(tag_, t, line)
    return pin(scene, line, tag_, run_time=run_time)


def row_tag(s: str, color: str = S.GREY) -> VGroup:
    """A tag beside a terminal row whose pill is lower than the row pitch, so the tags of two
    neighbouring rows never touch (common.time_tag's fix; the shared tag() pill is 0.49 high, the
    pitch 0.44). .box .text"""
    g = tag(s, color, size=CAPTION)
    h = line_pitch(TERM_PT) - 0.08
    if g.box.height > h:
        b = RoundedRectangle(width=g.box.width, height=h, corner_radius=h / 2, stroke_color=color,
                             stroke_width=2).set_fill(S.BG, 0.92).move_to(g.box)
        g.submobjects[g.submobjects.index(g.box)] = b
        g.box = b
        g.text.move_to(b)
    return keep_size(g)


def flash(mob, color: str = TURN, k: float = 1.08):
    """Indicate on TEXT (never on a filled backing that would hide it)."""
    return Indicate(mob, color=color, scale_factor=k)


def text_glyphs(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of `sub` in a Text built from `s` with disable_ligatures=True (one submobject per
    character, spaces included)."""
    i = s.index(sub)
    return VGroup(*t.submobjects[i:i + len(sub)])


def plain(s: str, size: float = CAPTION, color: str = INK, bold_upto: int = 0) -> Text:
    """Serif text, one submobject per character (spaces included); the first `bold_upto`
    characters bold."""
    kw = {"t2w": {f"[0:{bold_upto}]": "BOLD"}} if bold_upto else {}
    t = S.text(s, size, color, disable_ligatures=True, **kw)
    assert len(t.submobjects) == len(s), (s, len(t.submobjects))
    return t


def glyph_chip(s: str, color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """devops.chip()'s look (border, faint tint, WHITE text) with a plain() text, so a narrated
    part of it can flash on its own. .box .text .s"""
    t = plain(s, size, INK)
    h = mono("|", size).height + 2 * 0.12
    b = box(t.width + 2 * 0.24, h, color, fill_opacity=0.16, radius=h / 2.6)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text, g.s = b, t, s
    return g


def texts_of(m) -> list:
    """Every text in m's family (Text, or a mono_line row): fade them before shapes shrink."""
    return [x for x in m.get_family() if isinstance(x, Text) or hasattr(x, "pt")]


def titled_box(title: str, body: str, color: str, w: float, h: float, title_color: str = S.GREY) -> VGroup:
    """A GREY (or `color`) box: a bold title row and a body row, top-left inside. .frame .title .body"""
    fr = box(w, h, color, fill=S.BG, fill_opacity=0.9, stroke=2.5, radius=0.14)
    tt = sans(title, CAPTION, title_color, weight="BOLD")
    bd = label(body, CAPTION, INK)
    tt.move_to(fr.get_corner(UP + LEFT) + np.array([0.25 + tt.width / 2, -0.22 - tt.height / 2, 0]))
    bd.next_to(tt, DOWN, buff=0.16, aligned_edge=LEFT)
    g = VGroup(fr, tt, bd)
    g.frame, g.title, g.body = fr, tt, bd
    return g


def wrap_md(s: str, size: float, width: float) -> list:
    """Greedy wrap at spaces, measured as _md_text draws it (`code` mono); an em dash stays at the
    end of its row (it never starts one) and a “quoted phrase” stays on one row."""
    nb = "\u00a0"
    s = s.replace(" — ", nb + "— ")
    s = re.sub(r"“[^”]*”", lambda m: m.group(0).replace(" ", nb), s)
    rows, cur = [], ""
    for w in s.split(" "):
        trial = f"{cur} {w}" if cur else w
        if cur and _md_text(trial.replace(nb, " "), size).width > width:
            rows.append(cur)
            cur = w
        else:
            cur = trial
    rows.append(cur)
    return [r.replace(nb, " ") for r in rows]


# ------------------------------------------------------------------ pictures
def persists_card() -> VGroup:
    """Beat 1: README.md · lines 807–814 redrawn. .head .cyl .cyl_label .proc .sess"""
    head = VGroup(_header_text("README.md · lines 807–814"),
                  label("“What persists between commands?”", CAPTION, S.GREY), expected_tag())
    head.arrange(RIGHT, buff=0.22)
    place(head, left=X_LEFT, top=2.85)
    cyl = cylinder(1.3, 1.25)
    cyl.move_to([-4.75, 1.2, 0])
    cl = VGroup(sans("persists", CAPTION, HARNESS, weight="BOLD"),
                label("runs, events, traces ·", CAPTION, INK), label("live memory", CAPTION, INK))
    cl.arrange(DOWN, buff=0.08)
    cl.next_to(cyl, DOWN, buff=0.22)
    proc = titled_box("one process", "inventory · mock orders · approval tickets · pending workflows",
                      S.GREY, 8.6, 2.55)
    place(proc, right=6.3, top=2.05)
    sess = titled_box("one session", "tasks · history", S.GREY, 3.8, 1.1)
    place(sess, right=proc.frame.get_right()[0] - 0.3, bottom=proc.frame.get_bottom()[1] + 0.3)
    g = VGroup(head, cyl, cl, proc, sess)
    g.head, g.cyl, g.cyl_label, g.proc, g.sess = head, cyl, cl, proc, sess
    return g


def reflection_card() -> VGroup:
    """Beat 7: README.md · lines 820–826, the five questions in full. .frame .rows .header"""
    rows = VGroup()
    for concept, q in REFLECT:
        s = f"{concept}: {q}"
        rows.add(plain(s, CAPTION, INK, bold_upto=len(concept) + 1))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    fr = box(rows.width + 0.6, rows.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    head = VGroup(_header_text("README.md · lines 820–826"),
                  label("“End-of-lecture reflection”", CAPTION, S.GREY), expected_tag())
    head.arrange(RIGHT, buff=0.22)
    head.next_to(fr, UP, buff=0.1).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header = fr, rows, head
    return g


def question_list(size: float = 24, width: float = 11.7) -> tuple:
    """Beat 8: the five recap questions, numbered, laid out under the title. Returns (title,
    blocks); each block has .badge .rows."""
    title = sans("Test yourself", 26, INK, weight="BOLD")
    place(title, left=X_LEFT, top=2.72)
    blocks = []
    y = title.get_bottom()[1] - 0.3
    x_text = X_LEFT + 0.65
    for i, q in enumerate(QUESTIONS, start=1):
        rows = VGroup(*[_md_text(r, size, INK) for r in wrap_md(q, size, width)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        place(rows, left=x_text, top=y)
        b = step_badge(i, TURN, size=22, radius=0.22)
        b.move_to([X_LEFT + 0.2, rows[0].get_center()[1], 0])
        blk = VGroup(b, rows)
        blk.badge, blk.rows = b, rows
        blocks.append(blk)
        y = rows.get_bottom()[1] - 0.4
    return title, blocks


def next_card(code: str, text: str, w: float = 11.8) -> VGroup:
    """Beat 9: a GREY dashed card for a coming lecture: "L08 · …". .frame .text .s"""
    s = f"{code} · {text}"
    t = plain(s, 22, INK, bold_upto=len(code))
    fr = box(w, t.height + 0.55, FUTURE, dashed=True, stroke=2.5, radius=0.16)
    t.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.35)
    g = VGroup(fr, t)
    g.frame, g.text, g.s = fr, t, s
    return g


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0 · python cli.py --help
        tr = tracker("Res", 1)
        t = term(P_CTR, rows=T_ROWS, container=True)
        ft = frame_tags(t, offline_tag())
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t), FadeIn(ft), run_time=0.6)
            bare_prompt(self, t)
            vo.wait_until("python cli.py")
            c0 = type_cmd(self, t, HELP.cmd, 1.0)
            o0 = show(self, t, HELP, 2, 3, "…", 21, 22, run_time=0.5)
            p0 = bare_prompt(self, t)
            vo.wait_until("every option in one place")
            self.play(Circumscribe(VGroup(o0[0], o0[1]), color=TURN, buff=0.08, fade_out=True,
                                   stroke_width=4), run_time=1.2)

        # ========================================================== 1 · what persists between commands
        card1 = persists_card()
        for m in card1:
            inside(m)
        apart(card1.head, tr, 0.05)
        apart(card1.cyl_label, card1.proc, 0.2)
        assert card1.cyl_label.get_bottom()[1] > STRIP_TOP + 0.15 and card1.proc.get_bottom()[1] > STRIP_TOP + 0.15
        apart(card1.proc.body, card1.sess, 0.1)
        with self.voiceover(SAY[1]) as vo:
            fit(self, t, 3, keep=[c0, o0[0], p0], tags=ft)
            self.play(FadeIn(card1.head), FadeIn(card1.cyl, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("stay in SQLite")
            self.play(FadeIn(card1.cyl_label, shift=UP * 0.08), run_time=0.4)
            self.play(flash(card1.cyl_label[0], HARNESS, 1.15), run_time=0.5)
            vo.wait_until("Inventory")
            self.play(FadeIn(card1.proc, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("last for one process")
            self.play(flash(card1.proc.title, TURN, 1.15), run_time=0.6)
            vo.wait_until("tasks and history")
            self.play(FadeIn(card1.sess, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("for one session")
            self.play(flash(card1.sess.title, TURN, 1.15), run_time=0.6)

        # ========================================================== 2 · exit; docker ps -a
        badge = Stage().badge(BADGE_W)
        place(badge, right=6.45, top=3.55)
        ctr_parts = ("container", "mount_app", "mount_secrets", "port", "https")
        chip2 = chip("a second container shell open? exit it too", S.GREY, size=CAPTION)
        place(chip2, left=X_LEFT, cy=BAND_Y)
        cap2 = _md_text("started with `--rm` (`docker-shell.sh` · line 23): the container deleted itself",
                        CAPTION, S.GREY)
        place(cap2, left=X_LEFT, cy=BAND_Y)
        for m in (chip2, cap2):
            inside(m)
            apart(m, badge, 0.05)
            apart(m, tr, 0.0)
            assert m.get_bottom()[1] > strip_top(T_ROWS) + 0.05
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(card1), run_time=0.4)
            tr = switch_section(self, tr, "Down", 1)
            self.play(FadeIn(badge), run_time=0.5)
            fit(self, t, T_ROWS, tags=ft)
            vo.wait_until("Type exit")
            self.play(FadeIn(chip2, shift=DOWN * 0.1), run_time=0.4)
            cx = type_cmd(self, t, SHELL.typed(27), 0.4)
            pin_tag(self, t, cx, extra_tag(), run_time=0.3)
            show(self, t, SHELL, 28, run_time=0.3)
            self.play(*leave_container(t), run_time=0.6)
            bare_prompt(self, t)
            vo.wait_until("it was started")              # the --rm caption on "started with dash dash rm"
            self.play(FadeOut(chip2), run_time=0.3)       # old out, then new in (same place)
            self.play(FadeIn(cap2, shift=DOWN * 0.08), *badge.parts_out(*ctr_parts), run_time=0.6)
            vo.wait_until("so nothing is left")          # the command on "docker ps dash a"
            self.play(tr.goto(2), run_time=0.5)
            cp = type_cmd(self, t, PS.cmd, 0.6)
            pin_tag(self, t, cp, extra_tag(), run_time=0.3)
            show(self, t, PS, 2, run_time=0.4)
            bare_prompt(self, t)

        # ========================================================== 3 · outputs/ stays on the laptop
        obs_tag = tag("your prompts and outputs · keys redacted", S.GREY)
        place(obs_tag, left=X_LEFT, cy=BAND_HI)
        obs_src = _header_text(f"{OBS_PY} · line 30")
        place(obs_src, left=X_LEFT + 0.2, cy=BAND_LO)
        for m in (obs_tag, obs_src):
            inside(m)
            apart(m, badge, 0.05)
            apart(m, tr, 0.0)
        apart(obs_tag, obs_src, 0.04)
        assert obs_src.get_bottom()[1] > strip_top(T_ROWS) + 0.05
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(cap2), tr.goto(3), run_time=0.5)
            cl = type_cmd(self, t, LS_CMD, 1.6)
            pin_tag(self, t, cl, extra_tag(), run_time=0.3)
            o3 = show(self, t, OUTS, 2, *[(LS_ROWS[n], OUTPUT) for n in (10, 11, 13, 14)], "…",
                      (OUTS.line(23), TURN), 24, run_time=0.6)
            assert len(o3) == 8 and o3[4].text == LS_ROWS[14] and o3[7].text == OUTS.line(24)
            vo.wait_until("Its trace database")
            obs = substring(o3[4], "observability.sqlite")
            ul = under(obs, LOOKUP, stroke=3)
            self.play(obs.animate.set_color(LOOKUP), FadeIn(obs_tag, shift=DOWN * 0.08), run_time=0.5)
            pin(self, o3[4], ul, run_time=0.4, anim=Create(ul))
            self.play(FadeIn(obs_src, shift=DOWN * 0.08), run_time=0.4)
            vo.wait_until("delete it when")
            tg7, tg6 = row_tag("git-ignored (.gitignore · line 64)"), row_tag("your copy", TURN)
            pin_tag(self, t, o3[7], tg7, run_time=0.4)
            pin_tag(self, t, o3[6], tg6, run_time=0.4)
            assert tg6.get_bottom()[1] > tg7.get_top()[1] + 0.02

        # ========================================================== 4 · docker image rm; the your-turn card
        chip4 = glyph_chip("frees up to 1.77 GB · base image stays")
        place(chip4, left=X_LEFT, cy=BAND_Y)
        apart(chip4, badge, 0.05)
        key_s = "key: not in files, commits or shell history · close its terminal · watch your OpenAI usage"
        tc = turn_card([("exit", "in each container shell"), "docker ps -a", RMI.cmd,
                        ["delete", "`outputs/`", "when done"], Prose(key_s),
                        Prose("Colab: Runtime › Disconnect and delete runtime"),
                        (Prose("offline · free"), HARNESS)],
                       header="teardown · every step an extra")
        colab_row = tc.rows[5]
        key_row = plain(key_s, CAPTION, INK)            # the same row, one glyph per character, so
        key_row.move_to(tc.rows[4]).align_to(tc.rows[4], LEFT)   # its narrated parts can flash
        tc.rows.submobjects[4] = key_row
        ill = illustration_tag().next_to(colab_row, RIGHT, buff=0.3)
        assert ill.get_right()[0] < tc.frame.get_right()[0] - 0.2
        tc.add(ill)
        place(tc, cx=0, cy=-0.35)
        inside(tc)
        apart(tc, tr, 0.05)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(obs_tag), FadeOut(obs_src), tr.goto(4), run_time=0.5)
            cr = type_cmd(self, t, RMI.cmd, 1.0)
            pin_tag(self, t, cr, extra_tag(), run_time=0.3)
            show(self, t, RMI, 2, (RM3, OUTPUT), run_time=0.4)
            vo.wait_until("frees most")
            self.play(FadeIn(chip4, shift=DOWN * 0.08), run_time=0.4)
            vo.wait_until("the base image")
            self.play(flash(text_glyphs(chip4.text, chip4.s, "base image stays"), TURN, 1.06), run_time=0.7)
            vo.wait_until("Then close the terminal")
            key_b = badge.parts["key"]                  # tiny in the badge: a GOLD ring finds it
            self.play(flash(key_b, COST, 1.8),
                      Circumscribe(key_b, shape=Circle, color=COST, buff=0.12, stroke_width=3, fade_out=True),
                      run_time=0.9)
            self.play(*badge.parts_out("key"), run_time=0.5)
            self.play(FadeOut(VGroup(t, ft, chip4, badge)), run_time=0.5)
            self.play(FadeIn(tc, scale=0.97), run_time=0.6)
            vo.wait_until("keep it out of files")
            self.play(flash(text_glyphs(key_row, key_s, "not in files, commits or shell history"), TURN, 1.04),
                      run_time=0.8)
            vo.wait_until("and watch your usage")
            self.play(flash(text_glyphs(key_row, key_s, "watch your OpenAI usage"), TURN, 1.06), run_time=0.8)
            vo.wait_until("In Colab")
            self.play(flash(colab_row, TURN, 1.06), run_time=0.8)
            vo.wait_until("Pause, and tear down")
            self.play(flash(tc.tag.text, TURN, 1.2), run_time=0.6)
        self.wait(2)                                    # ▶ beat: hold the frame

        # ========================================================== 5 · the action boundary, filled in
        ab = ActionBoundary(moves=False).fill_recap()
        place(ab, cx=0, top=2.72)
        lr = lref("22")
        inside(ab)
        apart(ab, tr, 0.0)
        apart(ab, lr, 0.0)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(tc), run_time=0.5)
            self.play(FadeIn(ab), FadeIn(lr), run_time=0.8)
            for name, phrase in (("control", "budgets and the graph"), ("tools", "schemas, the audit"),
                                 ("context", "the packet, the capsule"), ("verify", "Cart Check and revalidation"),
                                 ("sub", "narrow tools and separate")):
                vo.wait_until(phrase)
                self.play(ab.light(name), flash(ab.green_texts[name], TURN, 1.04), run_time=0.6)

        # ========================================================== 6 · the model proposes; the harness decides
        with self.voiceover(SAY[6]) as vo:
            # dim the BLUE cells: outline, fill AND text fade (common's dim_side raises the 0.1 fill
            # to 0.35, so the "dimmed" cells read as filled, brighter boxes over faint text)
            dims = []
            for n, c in ab.blues.items():
                dims.append(c.frame.animate.set_stroke(opacity=0.35).set_fill(opacity=0.03))
                if ab.blue_texts.get(n) is not None:
                    dims.append(ab.blue_texts[n].animate.set_opacity(0.35))
            self.play(ab.unlight(), *dims, flash(ab.head_blue, CLOUD, 1.1), run_time=0.8)
            vo.wait_until("On the right")
            self.play(*[ab.greens[n].frame.animate.set_stroke(HARNESS, 4).set_fill(HARNESS, 0.16)
                        for n in ab.greens], flash(ab.head_green, HARNESS, 1.1), run_time=0.8)
            vo.wait_until("and where it matters")
            st1, an1 = ab.stamp_human("control")
            st2, an2 = ab.stamp_human("tools")
            self.play(*an1, *an2, run_time=0.5)
            self.play(FadeIn(st1, scale=1.25), FadeIn(st2, scale=1.25), run_time=0.5)

        # ========================================================== 7 · the README's reflection questions
        refl = reflection_card()
        place(refl, cx=0, top=2.78)
        pick = note("pick one run you did")
        place(pick, left=refl.frame.get_left()[0] + 0.1, top=refl.frame.get_bottom()[1] - 0.18)
        inside(refl)
        apart(refl, tr, 0.0)
        apart(refl, lr, 0.0)
        k = 3.2 / ab.width
        with self.voiceover(SAY[7]) as vo:
            tr = switch_section(self, tr, "Res", 2)
            words = [m for m in texts_of(ab)]
            self.play(*[m.animate.set_opacity(0) for m in words], FadeOut(st1), FadeOut(st2), run_time=0.35)
            for m in words:                              # gone for good: shapes only shrink (no tiny text)
                ab._unparent(m)
            self.play(ab.animate.scale(k).move_to(MINI), run_time=0.6)
            apart(ab, refl, 0.1)
            apart(ab, pick, 0.1)
            self.play(FadeIn(refl, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Pick one run")
            self.play(FadeIn(pick, shift=UP * 0.08), run_time=0.5)

        # ========================================================== 8 · test yourself
        title, blocks = question_list()
        ans = note("answers in exercises.md")
        place(ans, left=X_LEFT + 0.65, top=blocks[-1].rows.get_bottom()[1] - 0.3)
        for m in (title, *blocks, ans):
            inside(m)
        apart(title, tr, 0.05)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(refl, pick, ab, lr)), run_time=0.5)
            self.play(FadeIn(title, shift=DOWN * 0.08), run_time=0.4)
            for i, phrase in enumerate(Q_ANCHORS):
                vo.wait_until(phrase)
                anims = [FadeIn(blocks[i], shift=RIGHT * 0.12)]
                if i:
                    b = blocks[i - 1].badge
                    anims += [b[0].animate.set_stroke(S.GREY), b[1].animate.set_color(S.GREY)]
                self.play(*anims, run_time=0.5)
            vo.wait_until("Pause and try them")
            b = blocks[-1].badge
            self.play(b[0].animate.set_stroke(S.GREY), b[1].animate.set_color(S.GREY), run_time=0.5)
            vo.wait_until("answers are in")
            self.play(FadeIn(ans, shift=UP * 0.08), run_time=0.5)
        self.wait(3)                                    # time to read the five questions

        # ========================================================== 9 · what's next
        c8 = next_card("L08", "fine-tuning on Agent Platform (formerly Vertex AI) · a service account again")
        c9 = next_card("L09", "testing code with pytest · 281 offline unittest tests to copy")
        place(c8, cx=0, top=2.45)
        place(c9, cx=0, top=c8.get_bottom()[1] - 0.35)
        foot = VGroup(label("study guide and exercises:", CAPTION, S.GREY), mono(GUIDE, CAPTION, INK))
        foot.arrange(RIGHT, buff=0.2)
        place(foot, cx=0, top=c9.get_bottom()[1] - 0.6)
        trouble = chip("if a step fails: README › Troubleshooting (lines 828–839)", S.GREY, size=CAPTION)
        place(trouble, cx=0, top=foot.get_bottom()[1] - 0.35)
        VGroup(c8, c9, foot, trouble).set_y(-0.1)
        for m in (c8, c9, foot, trouble):
            inside(m)
        apart(c8, tr, 0.1)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(title, *blocks, ans)), run_time=0.5)
            self.play(FadeIn(c8, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("formerly Vertex AI")
            self.play(flash(text_glyphs(c8.text, c8.s, "(formerly Vertex AI)"), TURN, 1.06), run_time=0.7)
            vo.wait_until("Lecture 9 tests")
            self.play(FadeIn(c9, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("these 281 tests")
            self.play(flash(text_glyphs(c9.text, c9.s, "281 offline unittest tests to copy"), TURN, 1.05),
                      run_time=0.8)
            vo.wait_until("and are a good model")
            self.play(FadeIn(foot, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(trouble, shift=UP * 0.08), run_time=0.5)
        self.wait(3)
        self.play(FadeOut(VGroup(c8, c9, foot, trouble, tr)), run_time=0.8)
        self.wait(0.3)
