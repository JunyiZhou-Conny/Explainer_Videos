"""S15 · One-command deploy (README C5-C6, two extras, the errata about the deployed image; V6 pull, V4 coda).

Beats (script.md "## S15", one voiceover block each):
 0  S14 ended on an empty frame: TRACKER C4 fades in with the VM terminal (12 rows, `ssh · ac215-l02`) and
    moves to C5, with GREY `Lecture 2 · slides 70–71` (lecture_ref, standard top right; "Then the deploy"
    to the end of the beat: pull and run, the pull from a registry; above the shelf's title, not on it).
    "sudo docker run": it types `sudo docker run --rm -ti dlops/simple-translate` (README.md
    line 215; folds); "dlops slash simple-translate": the name turns TEAL and pulses. "Pause and run it": ▶
    your turn. "The image isn't on this VM yet": vm-debian12/06: 2-4, …, 10-12 (hash12), `Unable to find
    image` underlined YELLOW. "so Docker pulls it": the terminal shrinks to the strip; V6 above it: the
    BLUE Docker Hub shelf (top right, `dlops/simple-translate` on its board, seven small slabs) and the
    BLUE VM `ac215-l02` (left: S14's two bars, "Linux kernel" with "user space · Debian" on it, PURPLE
    `dockerd` on user space); a PINK route curves down from the shelf to the VM. "from Docker Hub"
    (through "seven layers"): seven copies of the shelf's slabs ride the route and stack up on `dockerd`,
    bottom-up (the shelf keeps its copy). "then starts a container": the TEAL glass slab (writable layer,
    main process) lands on top and the strip shows the container's own prompt `root@c7c280390994:/#`
    (line 13).
 1  TRACKER C6. The picture goes, and the lecture tag with it; the strip grows back to 12 rows; at line
    13's prompt it types `python cli.py` (README.md line 218) -> vm-debian12/06: 16-20, 24 (wrap), 26-27.
    "and its defaults": `text='I love cheese'` underlined YELLOW; "comes back in Italian": `Output: Adoro il
    formaggio` turns GREEN and pulses. "Pause and run it": ▶ your turn. "No clone, no pip, no uv":
    top right, above the terminal, three dashed GREY chips `git clone` `pip` `uv` appear as named;
    "just Docker and one image": a PURPLE `docker` chip + a small TEAL image glyph.
 2  TRACKER C6 · extra. It types `python --version`; the chips go as its row tag `extra` comes -> line 29;
    "why 3.14.7": `3.14.7` underlined YELLOW; "when the recipe says 3.12": GREY row tag "the
    recipe: python:3.12". "The same reason as in our build": the strip shrinks (3 rows); V4 coda above
    it: the number line with the GREEN `>=3.13` band; our GREEN dot drops in above the line (`3.15.0` /
    "our build · uv 0.13.0"). "built on September 16": GREY source chip vm-debian12/08: 3 (cut after
    the date) under its own command as GREY mono caption: vm-debian12/08 line 1 without `uname -m; `
    (folded by hand onto 2 rows, see INSPECT_ROWS; row tag "extra · on the VM"), the date underlined
    YELLOW; "with uv 0.12.15": source chip vm-debian12/10: 8 (caption at its right "the image's
    `.venv/pyvenv.cfg`": the command comes in beat 5), `0.12.15` underlined. The command's two rows
    span the frame above the band label, so both chips stay left of it.
    "the newest stable Python that uv knew in the range": the band and its label pulse;
    "was 3.14.7": a second GREEN dot lands in the band below the line (`3.14.7` / "dlops image · uv
    0.12.15"). "Our build today got 3.15.0": our dot pulses.
 3  The source chips go; "two Pythons": both dots pulse. "Nothing in the recipe is pinned": the line and
    the strip go (TRACKER C6: the extra command is off screen); three GREY chips at the left, each with
    where it comes from: `pip install uv` (Dockerfile.txt · line 19), `requires-python = ">=3.13"`
    (pyproject.toml · line 6), a dashed `uv.lock` (the repo's top level). They light YELLOW in turn as
    named, with "unpinned", "open-ended", "not in the repo ·" ("each build writes its own" on those words).
    "An image freezes all that": the TEAL image stack fades in at the right (`dlops/simple-translate`),
    copies of the three chips shrink into its uv and uv sync slabs, an ice glaze and a TEAL snowflake
    "frozen at build time" settle on it; "ship the image": the caption "ship the image, not the recipe"
    (centred, below the column).
 4  TRACKER C6. The picture goes as the strip comes back, without its marks (script.md: "Full
    terminal"; growing it for one line and shrinking it 1.4 s later would only churn); at line 30's
    prompt it types `exit` -> line 31, and the VM prompt returns. "One more small mismatch": README
    card `README.md · line 205` ("… pull the image you pushed in step 3, and run it.") above the
    strip; "the README promises": the strip fades (the cards need the frame; the group is centred
    under the tracker), "pull the image you pushed in step 3" underlined YELLOW, tag `erratum`;
    "this command runs the instructor's": README card line 215 (the command), `dlops/simple-translate`
    underlined YELLOW. "Your image is": its prefix is copied down into a GREEN chip (text, not run)
    `sudo docker run --rm -ti <USER NAME>/simple-translate-ac215` with `<USER NAME>` YELLOW (GREY
    caption "your image · not run here"); "once it's built for amd64": GREY tag "Intel/AMD laptop:
    already amd64 · Apple Silicon Mac: rebuild first (see Platforms)" (S13: an Intel/AMD build is
    already linux/amd64; only an arm64 build needs the rebuild).
 5  TRACKER C6 · extra. The cards go; the strip comes back and grows to 8 rows (5 in script.md: the
    three command rows and five output rows all stay on screen until the output is read); it types
    `sudo docker run --rm dlops/simple-translate -c 'wc -c cli.py; grep -n Translator cli.py; ls -l
    .venv/bin/python; cat .venv/pyvenv.cfg'` (row tag `extra`; folded by hand at spaces, see IMG_ROWS)
    -> vm-debian12/10: 2-4, …, 8; `uv = 0.12.15` underlined YELLOW with the GREY row tag "where
    `uv 0.12.15` came from" (the source of beat 2's chip). "its cli.py is the older one": the strip
    shrinks to its five output rows (2 more than the house strip; the picture above sits higher)
    while line 4 is copied up above CODE(cli.py: 25) (caption "in the image · dlops/simple-translate",
    `async` over `async`; the panel is right-aligned so the line's `25:` fits), tag "erratum · the
    published image lags the repo"; "without raise exception equals True": `Translator()` underlined
    YELLOW in the image's line, `raise_exception=True` underlined GREEN in the repo's. "If Google
    refuses a request": GREY note "if Google refuses a request: this version prints your input back";
    "That's not a Docker problem": GREY tag "not a Docker problem".
 6  TRACKER C5. Everything else goes. A GREY card "if the pull itself fails:" with
    vm-debian13/06-docker-run-rate-limited: 3 (wrap, RED), `toomanyrequests` underlined RED; tag
    "real capture · Debian 13 · 2026-10-13". "Docker Hub limits": "pull rate limit"
    underlined YELLOW, GREY note "anonymous pulls: a limit per network address";
    "a classroom can hit": note pulses. "Wait a while": GREEN chip; "or log in first": GREEN chip
    `sudo docker login -u <USER NAME>` (`<USER NAME>` YELLOW). Fade out to an empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.devops import MONO, OUTPUT, TERM_BG, code_span, lecture_ref, line_pitch
from explainer.scene import VoiceScene

from common import (CLOUD, DEPLOY, ERR, EXIT, IMAGE, INK, LAPTOP, LAPTOP_DIR, NARRATION, P_VM, REPO_ENTRIES,
                    STRIP_ROWS, STRIP_TOP, SYSTEM, TOOL, TURN, VENV, VM12, VM13, VM_HOST, Glass, LayerStack,
                    RegistryShelf, VersionLine, attach, bare_prompt, beside, box, capture, code, cut,
                    docker_chip, erratum_tag, excerpt, glyph_range, hash12, istep, label, mini_stack, mono, mono_line,
                    pin, readme_card, real_capture_tag, resize, route, row_tag, substring, tag, track,
                    tracker_c, type_cmd, under, unpin, vm_term, your_turn)

SAY = NARRATION["S15"]

# ------------------------------------------------------------------ real outputs (file line numbers)
C06 = capture("06", VM12)                         # vm-debian12/06-docker-run.txt
assert C06.cmd == DEPLOY and C06.exit == 0, C06.cmd
OUT_PULL = [hash12(s) for s in C06.at((2, 4), "…", (10, 12))]
assert OUT_PULL[0] == "Unable to find image 'dlops/simple-translate:latest' locally", OUT_PULL[0]
assert OUT_PULL[5] == "Digest: sha256:2454010bcf64…", OUT_PULL[5]
assert OUT_PULL[6].startswith("Status: Downloaded newer image"), OUT_PULL[6]
assert sum(s.endswith(": Pull complete") for s in C06.raw) == 7     # seven layers
L13, L28, L30 = C06.line(13), C06.line(28), C06.line(30)
CPROMPT = C06.istep(13)[0]
assert C06.istep(13) == ("root@c7c280390994:/#", "python cli.py"), L13
assert C06.istep(28)[1] == "python --version" and C06.istep(30)[1] == EXIT
OUT_CLI = C06.at((16, 20), 24, (26, 27))
assert OUT_CLI[5].startswith("Arguments: Namespace(text='I love cheese'") and len(OUT_CLI[5]) > 65
assert OUT_CLI[6] == "Input: I love cheese" and OUT_CLI[7] == "Output: Adoro il formaggio", OUT_CLI
V_DLOPS = C06.line(29)
assert V_DLOPS == "Python 3.14.7", V_DLOPS
EXIT_ECHO = C06.line(31)
assert EXIT_ECHO == "exit"

C08 = capture("08", VM12)                         # vm-debian12/08-platform.txt (extra)
assert "sudo docker image inspect dlops/simple-translate" in C08.cmd, C08.cmd
CREATED = cut(C08.line(3), "2026-09-16")
assert CREATED == "linux/amd64 created 2026-09-16…", CREATED
# the chip's own command: line 1 without `uname -m; ` (its x86_64 is line 2, not on the chip), folded by
# hand outside the quotes (house style " \" + 4-space indent), so the rows paste back as one command
assert C08.cmd.startswith("uname -m; "), C08.cmd
INSPECT = C08.cmd[len("uname -m; "):]
INSPECT_ROWS = ["sudo docker image inspect dlops/simple-translate \\",
                "    --format '{{.Os}}/{{.Architecture}} created {{.Created}}'"]
assert " ".join([INSPECT_ROWS[0][:-2], INSPECT_ROWS[1][4:]]) == INSPECT, INSPECT

C10 = capture("10", VM12)                         # vm-debian12/10-image-files.txt (extra)
IMG_CMD = C10.cmd
assert IMG_CMD == ("sudo docker run --rm dlops/simple-translate -c 'wc -c cli.py; grep -n Translator cli.py; "
                   "ls -l .venv/bin/python; cat .venv/pyvenv.cfg'"), IMG_CMD
UV_CFG = C10.line(8)
assert UV_CFG == "uv = 0.12.15", UV_CFG
OUT_IMG = C10.at((2, 4), "…", 8)                  # line 8: the source of beat 2's uv chip
assert OUT_IMG[2] == "25:    async with Translator() as translator:" and OUT_IMG[4] == UV_CFG, OUT_IMG
# The quoted script is 83 characters: longer than a row, so Terminal.fold (which never breaks inside
# quotes) would cut it mid-word. Folded by hand at spaces, house style (" \" + 4-space indent): inside
# the quotes the " \" + newline reaches the image's bash, which reads it as a line continuation, so the
# rows still paste back as a working command.
IMG_ROWS = [f"{P_VM} sudo docker run --rm \\",
            "    dlops/simple-translate -c 'wc -c cli.py; grep -n Translator \\",
            "    cli.py; ls -l .venv/bin/python; cat .venv/pyvenv.cfg'"]
assert " ".join([IMG_ROWS[0][:-2], IMG_ROWS[1][4:-2], IMG_ROWS[2][4:]]) == f"{P_VM} {IMG_CMD}"
assert max(len(r) for r in IMG_ROWS) <= 65

_OURS = capture("33", LAPTOP_DIR)                  # laptop/33-inside.txt: our image's Python and uv
assert "Python 3.15.0" in _OURS.raw and "uv = 0.13.0" in _OURS.raw, _OURS.path

RATE = capture("06-docker-run-rate-limited", VM13)
assert RATE.cmd == DEPLOY and RATE.exit == 125, RATE.cmd
RATE_LINE = RATE.line(3)
assert RATE_LINE.startswith("docker: Error response from daemon: toomanyrequests: You have reached your "
                            "unauthenticated pull rate limit."), RATE_LINE

# ------------------------------------------------------------------ the tutorial's own lines
R205 = excerpt("README.md", 205, 205)
assert "pull the image you pushed in step 3, and run it." in R205, R205
Q205 = "… pull the image you pushed in step 3, and run it."
assert excerpt("README.md", 215, 215) == f"* `{DEPLOY}`"
assert excerpt("README.md", 218, 218) == "* `python cli.py`"
MINE = "sudo docker run --rm -ti <USER NAME>/simple-translate-ac215"
PIN_UV = excerpt("Dockerfile.txt", 19, 19).strip()
PIN_PY = excerpt("pyproject.toml", 6, 6).strip()
assert PIN_UV == "pip install uv" and PIN_PY == 'requires-python = ">=3.13"', (PIN_UV, PIN_PY)
assert "uv.lock" not in REPO_ENTRIES
CLI25 = excerpt("cli.py", 25, 25)
assert CLI25 == "    async with Translator(raise_exception=True) as translator:", CLI25
LOGIN = "sudo docker login -u <USER NAME>"

# ------------------------------------------------------------------ layout
ROWS = 12                                  # the full VM terminal (top edge at y 2.19)
VM_C, VM_W, VM_H = np.array([-3.6, 0.72, 0]), 5.2, 4.0      # beat 0: the VM, above the strip
STACK_X, STACK_W = -3.0, 2.6               # the image stack inside the VM
BAR_H, VM_K = 0.36, 0.8                    # the VM's two bars; its stack at 0.8 x H_STACK (room for the bars)
SHELF_C, SHELF_W, SHELF_H = np.array([4.4, 1.45, 0]), 3.6, 1.5
H_STACK = [0.1] * 4 + [0.3, 0.3, 0.5]      # V6's seven slabs (as S12): four base, apt/pip, COPY, uv sync
FILLS = [SYSTEM] * 5 + [LAPTOP, VENV]
AX_Y = 0.25                                # beat 2: the number line (S07: 0.45; room for the chips)
CHIPS_TOP = 2.58                           # beat 2: the source chips' top (the tracker ends at 2.9)
COL_TOP = 2.45                             # beat 3: the recipe column's top
IMG_STRIP = 3 + len(OUT_IMG)               # beat 5: the strip while the folded extra is typed and read
IMG_KEEP = len(OUT_IMG)                    # beat 5: then it keeps the five output rows
STRIP5_TOP = STRIP_TOP + (IMG_KEEP - STRIP_ROWS) * line_pitch(22)   # that strip's top edge
RIGHT_X, LEFT_X = 6.4, -6.3


# ------------------------------------------------------------------ small builders
def pulse(m, factor: float = 1.15):
    """A tag's pulse: grow and settle back (Indicate would flood an opaque tag with its colour)."""
    return m.animate(rate_func=there_and_back).scale(factor)


def text_span(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of `sub` in a Text built from string `s` (Text drops spaces)."""
    i = s.index(sub)
    a, n = len("".join(s[:i].split())), len("".join(sub.split()))
    return VGroup(*t[a:a + n])


def vm_box() -> VGroup:
    """The BLUE VM (S14's picture, taller): frame, title top-left, S14's two bars (slide 12's stack: the
    Linux kernel, user space · Debian on it), PURPLE dockerd on user space under the image's spot.
    .frame .title .kernel .user .dockerd .floor_y"""
    f = box(VM_W, VM_H, CLOUD, fill_opacity=0.06).move_to(VM_C)
    t = label(f"VM · {VM_HOST}", 22, CLOUD)
    t.move_to(f.get_corner(UL) + np.array([0.25 + t.width / 2, -0.3, 0]))
    kr = RoundedRectangle(width=VM_W - 0.4, height=BAR_H, corner_radius=0.06, stroke_color=S.GREY,
                          stroke_width=2).set_fill(S.GREY, 0.22)
    kr.move_to([f.get_center()[0], f.get_bottom()[1] + 0.1 + BAR_H / 2, 0])
    kt = label("Linux kernel", 20, INK).move_to(kr)
    ub = kr.copy().next_to(kr, UP, buff=0.06)
    ut = label("user space · Debian", 20, INK).move_to(ub)
    dk = box(STACK_W, 0.42, TOOL, fill_opacity=0.18).move_to([STACK_X, ub.get_top()[1] + 0.31, 0])
    dt = mono("dockerd", 20, TOOL).move_to(dk)
    g = VGroup(f, t, VGroup(kr, kt), VGroup(ub, ut), VGroup(dk, dt))
    g.frame, g.title, g.kernel, g.user, g.dockerd = f, t, g[2], g[3], g[4]
    g.floor_y = dk.get_top()[1] + 0.06
    return g


def small_slabs(slab_w: float = 1.3, k: float = 0.55, gap: float = 0.025) -> VGroup:
    """The image as seven small slabs (V2 fills, TEAL outlines), bottom-up, heights k x H_STACK."""
    out = VGroup()
    for f, h in zip(FILLS, H_STACK):
        hh = max(0.055, h * k)
        out.add(RoundedRectangle(width=slab_w, height=hh, corner_radius=min(0.04, hh / 2.5), stroke_color=IMAGE,
                                 stroke_width=2).set_fill(f, 0.5))
    return out.arrange(UP, buff=gap)


def hub_shelf() -> VGroup:
    """V6 · Docker Hub as S12's BLUE shelf (one board, door on the left), titled 'Docker Hub' over the
    TEAL repository name, with the image's seven small slabs standing on the board. .shelf .slabs"""
    sh = RegistryShelf("x", shelf_w=SHELF_W, shelf_h=SHELF_H, boards=1)
    sh.remove(sh.title)
    sh.shift(SHELF_C - sh.frame.get_center())
    title = VGroup(label("Docker Hub", 22, CLOUD), mono("dlops/simple-translate", 20, IMAGE))
    title.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(sh.frame, UP, buff=0.12).align_to(sh.frame, LEFT)
    sh.title = title
    sh.add(title)
    slabs = small_slabs().move_to(sh.spot(0, 1, 3), aligned_edge=DOWN)
    g = VGroup(sh, slabs)
    g.shelf, g.slabs = sh, slabs
    return g


def dashed_chip(s: str, size: float = 20, color=S.GREY) -> VGroup:
    """Something that is not there: GREY mono text in a dashed GREY chip."""
    t = mono(s, size, color)
    h = mono("|", size).height + 0.24
    b = box(t.width + 0.48, h, color, radius=h / 2.6, dashed=True)
    t.move_to(b)
    return VGroup(b, t)


def out_chip(s: str, size: float = 20) -> VGroup:
    """A captured output line on a small dark terminal-like chip. .frame .line"""
    ln = mono_line(s, size, OUTPUT)
    fr = RoundedRectangle(width=ln.strut.width + 0.4, height=ln.strut.height + 0.22, corner_radius=0.1,
                          stroke_color=S.GREY, stroke_width=2).set_fill(TERM_BG, 1)
    ln.move_to(fr)
    g = VGroup(fr, ln)
    g.frame, g.line = fr, ln
    return g


def captioned(caption: VGroup, body: VGroup, buff: float = 0.1) -> VGroup:
    """A caption (GREY, small) above `body`, left-aligned. .caption .body"""
    caption.next_to(body, UP, buff=buff).align_to(body, LEFT).shift(RIGHT * 0.08)
    g = VGroup(caption, body)
    g.caption, g.body = caption, body
    return g


def cmd_rows(rows, size: float = 20, color=S.GREY) -> VGroup:
    """A folded command as GREY mono rows at a terminal's pitch (a source chip's caption)."""
    out = VGroup(*[mono_line(s, size, color) for s in rows])
    for a, b in zip(out, out[1:]):
        b.shift(a.strut.get_corner(UL) + DOWN * line_pitch(size) - b.strut.get_corner(UL))
    return out


def side_captioned(body: VGroup, caption: VGroup, buff: float = 0.25) -> VGroup:
    """A caption (GREY, small) right of `body`, centred on it. .caption .body"""
    caption.next_to(body, RIGHT, buff=buff)
    g = VGroup(body, caption)
    g.caption, g.body = caption, body
    return g


def grey_words(*parts, size: float = 20) -> Text:
    """A GREY caption from (text, 'mono'|'label') parts: one Text (mono parts by t2f), one baseline."""
    s = " ".join(p for p, _ in parts)
    return label(s, size, S.GREY, t2f={p: MONO for p, k in parts if k == "mono"})


def recipe_chip(s: str, dashed: bool = False, size: float = 22) -> VGroup:
    """A recipe item as a GREY chip, mono text; a dashed one is absent. .frame .text"""
    t = mono(s, size, S.GREY if dashed else INK)
    h = mono("|", size).height + 0.26
    fr = box(t.width + 0.5, h, S.GREY, fill_opacity=0.1, radius=0.1, dashed=dashed)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def snowflake(r: float = 0.3, color=IMAGE, stroke: float = 3) -> VGroup:
    """A six-armed frost glyph."""
    g = VGroup()
    for k in range(6):
        a = k * TAU / 6 + TAU / 4
        d = np.array([np.cos(a), np.sin(a), 0])
        g.add(Line(ORIGIN, d * r))
        p = d * r * 0.58
        for s in (1, -1):
            b = np.array([np.cos(a + s * 0.85), np.sin(a + s * 0.85), 0])
            g.add(Line(p, p + b * r * 0.36))
    return g.set_stroke(color, stroke)


def green_chip(s: str, size: float = 22, font: str | None = None, t2c=None) -> VGroup:
    """A GREEN 'do this' chip. Mono text (font=MONO) is a mono_line, so placeholders can be coloured.
    .frame .text"""
    t = mono_line(s, size, INK, t2c=t2c) if font == MONO else label(s, size, INK)
    hgt = (t.strut.height if font == MONO else mono("|", size).height) + 0.24
    fr = box(t.width + 0.5, hgt, VENV, fill_opacity=0.16, radius=hgt / 2.6)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def fail_card(rows, size: float = 22) -> VGroup:
    """The GREY 'if the pull itself fails:' card: a GREY header over RED capture rows (TERM_BG).
    .frame .head .rows"""
    head = label("if the pull itself fails:", size, S.GREY)
    lines = VGroup(*[mono_line(s, size, ERR) for s in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    inner = VGroup(head, lines).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    fr = RoundedRectangle(width=inner.width + 0.6, height=inner.height + 0.4, corner_radius=0.12,
                          stroke_color=S.GREY, stroke_width=2.5).set_fill(TERM_BG, 1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.head, g.rows = fr, head, lines
    return g


def wrap65(s: str, n: int = 65) -> list[str]:
    """Terminal.print(wrap=True)'s folding: cut at the edge every n characters."""
    return [s[i:i + n] for i in range(0, len(s), n)]


# ------------------------------------------------------------------ the scene
class Deploy(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, f"S15 has {len(SAY)} SAY lines; this scene times 7"

        # ========================================================== 0 · C5: pull and start
        tr = tracker_c(4)
        t = vm_term(ROWS)
        vm = vm_box()
        hub = hub_shelf()
        st = LayerStack(stack_w=STACK_W)
        st.floor.move_to([STACK_X, vm.floor_y, 0])
        slabs = [st.make(None, f, h * VM_K) for f, h in zip(FILLS, H_STACK)]
        glass = Glass(glass_w=STACK_W, process="main process").on(st)
        assert glass.dot_label.get_top()[1] < vm.frame.get_top()[1] - 0.12, "the glass label leaves the VM"
        assert glass.slab.get_top()[1] < vm.title.get_bottom()[1] - 0.12, "the glass slab runs into the title"
        assert vm.kernel.get_bottom()[1] > vm.frame.get_bottom()[1] + 0.05 and \
            vm.frame.get_bottom()[1] > STRIP_TOP + 0.1, "the VM's bars leave the frame / the VM meets the strip"
        assert glass.dot_label.get_left()[0] > vm.title.get_right()[0] + 0.3, "glass label runs into the title"
        assert hub.shelf.title.get_left()[0] > tr.get_right()[0] + 0.3 or \
            hub.shelf.title.get_bottom()[1] > tr.get_top()[1], "the shelf title runs into the tracker"
        assert vm.frame.get_top()[1] < tr.get_bottom()[1] - 0.1, "the VM runs into the tracker"
        path = route(hub.shelf.frame.get_left() + np.array([-0.2, -0.15, 0]),
                     np.array([vm.frame.get_right()[0] + 0.25, 0.7, 0]), arc=-0.6)
        # slides 70-71 (pull and run; pull downloads from a registry): standard top right, from "Then the
        # deploy" until the picture goes in beat 1; the shelf's title stays under it
        lref = lecture_ref(2, "70–71")
        assert lref.get_bottom()[1] > hub.shelf.title.get_top()[1] + 0.15, "lecture tag on the shelf's title"
        assert lref.get_left()[0] > tr.get_right()[0] + 0.3, "lecture tag runs into the tracker"

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.6)
            self.play(track(tr, 5), FadeIn(lref, shift=DOWN * 0.1), run_time=0.5)
            bare_prompt(self, t)
            vo.wait_until("sudo docker run")
            c0 = type_cmd(self, t, DEPLOY, 2.0)
            r0 = c0.rows[1]
            vo.wait_until("dlops slash simple-translate")
            name = substring(r0, "dlops/simple-translate")
            self.play(name.animate.set_color(IMAGE), run_time=0.3)
            self.play(Indicate(name, color=IMAGE, scale_factor=1.04), run_time=0.6)
            self.add(r0)
            vo.wait_until("Pause and run it")
            yt0 = beside(your_turn(), r0, buff=0.4)
            pin(self, r0, yt0, run_time=0.4)
            self.play(pulse(yt0), run_time=0.6)
            vo.wait_until("The image isn't on this VM yet")
            out0 = t.print(self, OUT_PULL, run_time=0.7, lag=0.08)
            u0 = under(substring(out0[0], "Unable to find image"), TURN)
            self.play(Create(u0), run_time=0.4)
            attach(self, out0[0], u0)
            vo.wait_until("so Docker pulls it")
            resize(self, t, STRIP_ROWS, run_time=0.6)
            self.play(FadeIn(VGroup(vm, hub), shift=UP * 0.15), Create(path), run_time=0.7)
            # the ride starts on "from Docker Hub" and spans "seven layers", so the glass slab lands
            # on "then starts a container" (0.9 s after "seven layers": too short for the ride alone)
            vo.wait_until("from Docker Hub")
            parcels = [s.copy() for s in hub.slabs]
            self.add(*parcels)
            rides = []
            for p, sl in zip(parcels, slabs):
                rides.append(Succession(p.animate(run_time=0.2).move_to(path.get_start()),
                                        MoveAlongPath(p, path, run_time=0.55),
                                        Transform(p, sl.box.copy(), run_time=0.35)))
            self.play(LaggedStart(*rides, lag_ratio=0.2), run_time=1.9)
            self.remove(*parcels)
            st.accept(self, *slabs)
            vo.wait_until("then starts a container")
            t.set_prompt(CPROMPT)
            bare_prompt(self, t)
            self.play(FadeIn(glass, shift=DOWN * 0.25), FadeOut(path), run_time=0.6)
            self.play(Indicate(glass.dot, color=IMAGE, scale_factor=1.8), run_time=0.5)

        # ========================================================== 1 · C6: python cli.py
        nos = VGroup(label("no", 22, S.GREY), dashed_chip("git clone"), label("· no", 22, S.GREY), dashed_chip("pip"),
                     label("· no", 22, S.GREY), dashed_chip("uv")).arrange(RIGHT, buff=0.12)
        just = VGroup(label("just", 22, INK), docker_chip("docker", 20), label("+ one image", 22, IMAGE),
                      mini_stack(tuple(FILLS), glyph_w=0.6, slab_h=0.05, gap=0.02)).arrange(RIGHT, buff=0.15)
        nos.move_to([RIGHT_X - nos.width / 2, 3.2, 0])
        just.move_to([RIGHT_X - just.width / 2, 2.6, 0])
        assert nos.get_left()[0] > tr.get_right()[0] + 0.3 and just.get_bottom()[1] > 2.3

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(vm, hub, st, glass, lref)), track(tr, 6), run_time=0.5)
            resize(self, t, ROWS, run_time=0.7)
            vo.wait_until("python cli.py")
            c1 = istep(self, t, L13, 0.6)
            out1 = t.print(self, OUT_CLI, run_time=0.8, lag=0.06, wrap=True)
            r_arg, r_out = t.find("Arguments:"), t.find("Output:")
            vo.wait_until("and its defaults")
            u1 = under(substring(r_arg, "text='I love cheese'"), TURN)
            self.play(Create(u1), run_time=0.5)
            attach(self, r_arg, u1)
            vo.wait_until("comes back in Italian")
            self.play(r_out.glyphs.animate.set_color(VENV), run_time=0.4)
            self.play(Indicate(r_out.glyphs, color=VENV, scale_factor=1.08), run_time=0.7)
            self.add(r_out)
            vo.wait_until("Pause and run it")
            yt1 = beside(your_turn(), c1, buff=0.4)
            pin(self, c1, yt1, run_time=0.4)
            self.play(pulse(yt1), run_time=0.6)
            vo.wait_until("No clone")
            self.play(FadeIn(nos[:2], shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("no pip")
            self.play(FadeIn(nos[2:4], shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("no uv")
            self.play(FadeIn(nos[4:], shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("just Docker")
            self.play(FadeIn(just[:2], shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and one image")
            self.play(FadeIn(just[2:], shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(just[3], color=IMAGE, scale_factor=1.3), run_time=0.6)
        del out1

        # ========================================================== 2 · C6 · extra: python --version, V4 coda
        vl = VersionLine(10, 16, lo=13, line_w=11.0)
        vl.shift(UP * AX_Y)
        band_full = vl.band.copy()
        ours = vl.dot2(15, "3.15.0", "our build · uv 0.13.0", VENV, above=True)
        theirs = vl.dot2(14, "3.14.7", "dlops image · uv 0.12.15", VENV, above=False)
        assert ours.text.get_top()[1] < vl.band_label.get_bottom()[1] - 0.05, "our label runs into the band label"
        assert theirs.text.get_bottom()[1] > -1.3, "the dlops label runs into the strip"
        # chip A: the date under its own command (GREY mono rows, the output in the command's first column);
        # the command's long row spans the frame above the band label. Chip B: its caption at its right
        # (the ticks leave no room for one above it)
        cmd_a = cmd_rows(INSPECT_ROWS)
        body_a = out_chip(CREATED).next_to(cmd_a, DOWN, buff=0.1)
        body_a.shift(RIGHT * (cmd_a[0].strut.get_left()[0] - body_a.line.strut.get_left()[0]))
        chip_a = VGroup(cmd_a, body_a)
        chip_a.shift(np.array([LEFT_X - body_a.frame.get_left()[0], CHIPS_TOP - cmd_a.get_top()[1], 0]))
        x_a = beside(row_tag("extra · on the VM"), cmd_a[0], buff=0.35)
        chip_a.add(x_a)
        chip_a.caption, chip_a.body = VGroup(cmd_a, x_a), body_a
        chip_b = side_captioned(out_chip(UV_CFG), grey_words(("the image's", "label"), (".venv/pyvenv.cfg", "mono")))
        chip_b.next_to(body_a, DOWN, buff=0.18).align_to(body_a, LEFT)
        bl = vl.band_label
        assert cmd_a.get_bottom()[1] > bl.get_top()[1] + 0.2, (cmd_a.get_bottom(), bl.get_top())
        assert body_a.get_right()[0] < bl.get_left()[0] - 0.2, body_a.get_corner(DR)
        # chip B sits under the band label's row, left of our dot's label
        assert chip_b.get_top()[1] < bl.get_bottom()[1] - 0.15 and chip_b.get_right()[0] < ours.text.get_left()[0] - 0.4, \
            chip_b.get_corner(UR)
        assert chip_b.get_bottom()[1] > vl.ticks.get_top()[1] + 0.2, (chip_b.get_bottom(), vl.ticks.get_top())
        assert max(cmd_a.get_right()[0], x_a.get_right()[0]) < 6.5, (cmd_a.get_right(), x_a.get_right())
        assert chip_a.get_top()[1] < tr.get_bottom()[1] - 0.25, "the chips crowd the tracker"
        assert theirs.text.get_bottom()[1] > STRIP_TOP + 0.2, "the dlops label runs into the strip"

        with self.voiceover(SAY[2]) as vo:
            unpin(self, [(c1, yt1), (r_arg, u1)], 0.3, track(tr, 6, extra=True))
            bare_prompt(self, t)
            c2 = istep(self, t, L28, 0.6)
            x2 = beside(row_tag("extra"), c2, buff=0.4)
            pin(self, c2, x2, run_time=0.3, anim=AnimationGroup(FadeIn(x2, shift=LEFT * 0.1),
                                                                 FadeOut(VGroup(nos, just))))
            r_v = t.print(self, [V_DLOPS], run_time=0.3)[0]
            bare_prompt(self, t)
            vo.wait_until("why 3.14.7")
            v_g = substring(r_v, "3.14.7")
            u2 = under(v_g, TURN)
            self.play(Create(u2), Indicate(v_g, color=TURN, scale_factor=1.2), run_time=0.6)
            attach(self, r_v, u2)
            vo.wait_until("when the recipe says 3.12")
            rec = beside(row_tag([("the recipe:", "label"), ("python:3.12", "mono")]), r_v, buff=0.5)
            pin(self, r_v, rec, run_time=0.4)
            vo.wait_until("The same reason as in our build")
            resize(self, t, STRIP_ROWS, run_time=0.6)
            vl.band.stretch_to_fit_width(0.01).align_to(band_full, LEFT)
            self.play(Create(vl.axis), LaggedStart(*[FadeIn(tk, shift=UP * 0.1) for tk in vl.ticks], lag_ratio=0.1),
                      Transform(vl.band, band_full), FadeIn(vl.band_label, shift=RIGHT * 0.2), run_time=0.9)
            self.play(FadeIn(ours.dot, shift=DOWN * 0.6), FadeIn(ours.text, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("This image was built on September 16")
            self.play(LaggedStart(FadeIn(chip_a.caption, shift=RIGHT * 0.15), FadeIn(body_a, shift=RIGHT * 0.15),
                                  lag_ratio=0.45), run_time=0.8)
            d_g = substring(body_a.line, "2026-09-16")
            ua = under(d_g, TURN)
            self.play(Create(ua), Indicate(d_g, color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("with uv 0.12.15")
            self.play(FadeIn(chip_b, shift=RIGHT * 0.15), run_time=0.5)
            u_g = substring(chip_b.body.line, "0.12.15")
            ub = under(u_g, TURN)
            self.play(Create(ub), Indicate(u_g, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("the newest stable Python")
            self.play(Indicate(vl.band_label, color=VENV, scale_factor=1.06),
                      vl.band.animate(rate_func=there_and_back).set_fill(VENV, 0.55), run_time=0.9)
            vo.wait_until("in the range was 3.14.7")
            self.play(FadeIn(theirs.dot, shift=DOWN * 0.8), run_time=0.5, rate_func=rate_functions.ease_out_cubic)
            self.play(FadeIn(theirs.text, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(theirs.dot, color=VENV, scale_factor=1.8), run_time=0.5)
            vo.wait_until("Our build today got 3.15.0")
            self.play(Indicate(ours.dot, color=VENV, scale_factor=1.8), Indicate(ours.top, color=VENV, scale_factor=1.15),
                      run_time=0.8)

        # ========================================================== 3 · nothing pinned: ship the image
        items = []
        for head, body, note in (
                (grey_words(("Dockerfile.txt", "mono"), ("· line 19", "label")), recipe_chip(PIN_UV), ["unpinned"]),
                (grey_words(("pyproject.toml", "mono"), ("· line 6", "label")), recipe_chip(PIN_PY), ["open-ended"]),
                (grey_words(("simple-translate/", "mono"), ("· the repo", "label")), recipe_chip("uv.lock", dashed=True),
                 ["not in the repo ·", "each build writes its own"])):
            it = captioned(head, body)
            nt = VGroup(*[label(s, 22, S.GREY) for s in note]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            nt.next_to(body, RIGHT, buff=0.3)
            it.note = nt
            items.append(it)
        col = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        col.move_to([LEFT_X + col.width / 2, 0, 0]).align_to(np.array([0, COL_TOP, 0]), UP)
        for it in items:
            it.note.next_to(it.body, RIGHT, buff=0.3)
        col_low = min(col.get_bottom()[1], items[2].note.get_bottom()[1])
        img = LayerStack(stack_w=2.4)
        img.floor.move_to([4.4, -0.35, 0])
        for f, h in zip(FILLS, H_STACK):
            img.slabs.add(img.make(None, f, h))
        img._pending.clear()
        img_name = mono("dlops/simple-translate", 20, IMAGE).next_to(img.floor, DOWN, buff=0.18)
        glaze = RoundedRectangle(width=2.4 + 0.3, height=img.slabs.height + 0.3, corner_radius=0.12,
                                 stroke_color=IMAGE, stroke_width=3).set_fill(INK, 0.08).move_to(img.slabs)
        frost = VGroup(snowflake(0.28), label("frozen at build time", 22, IMAGE)).arrange(RIGHT, buff=0.2)
        frost.next_to(glaze, UP, buff=0.22)
        moral = label("ship the image, not the recipe", 28, INK, t2c={"the image": IMAGE})
        # the strip leaves with the number line (the recipe needs the room; nothing in the terminal is
        # read in this beat), so the caption sits well below the column instead of on its last note
        moral.move_to([0, col_low - 0.5 - moral.height / 2, 0])
        assert col_low > moral.get_top()[1] + 0.4, (col_low, moral.get_top())
        assert moral.get_top()[1] < img_name.get_bottom()[1] - 0.3 and moral.get_bottom()[1] > -2.6
        assert col.get_top()[1] < tr.get_bottom()[1] - 0.35, "the column crowds the tracker"
        assert max(it.note.get_right()[0] for it in items) < img_name.get_left()[0] - 0.3
        assert frost.get_top()[1] < 3.0 and frost.get_right()[0] < 6.5, frost.get_corner(UR)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(chip_a, chip_b, ua, ub)), run_time=0.4)
            vo.wait_until("two Pythons")
            self.play(Indicate(ours.dot, color=VENV, scale_factor=1.8), Indicate(theirs.dot, color=VENV, scale_factor=1.8),
                      Indicate(ours.top, color=VENV, scale_factor=1.15), Indicate(theirs.top, color=VENV, scale_factor=1.15),
                      run_time=0.9)
            vo.wait_until("Nothing in the recipe is pinned")
            # the extra command leaves the frame with the strip, so the tracker drops " · extra"
            self.play(FadeOut(VGroup(vl, ours, theirs)), FadeOut(t), track(tr, 6), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.15) for it in items], lag_ratio=0.2), run_time=0.8)
            for it, phrase in zip(items, ("pip installs the latest uv", "the Python range is open",
                                          "and the repo has no uv.lock")):
                vo.wait_until(phrase)
                self.play(it.body.frame.animate.set_stroke(TURN), Indicate(it.body.text, color=TURN, scale_factor=1.1),
                          FadeIn(it.note[0], shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("so each build writes its own")
            self.play(FadeIn(items[2].note[1], shift=LEFT * 0.1), run_time=0.5)
            self.play(Indicate(items[2].note[1], color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("An image freezes all that")
            self.play(FadeIn(VGroup(img, img_name), shift=LEFT * 0.2), run_time=0.5)
            into = [(items[0], img.slabs[4]), (items[1], img.slabs[6]), (items[2], img.slabs[6])]
            ghosts = [it.body.copy() for it, _ in into]
            self.play(*[g.animate.scale(0.2).move_to(s).set_opacity(0) for g, (_, s) in zip(ghosts, into)],
                      *[it.body.frame.animate.set_stroke(S.GREY) for it in items], run_time=0.9)
            self.remove(*ghosts)
            self.play(FadeIn(glaze, scale=1.05), FadeIn(frost, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("ship the image")
            self.play(FadeIn(moral, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(moral, color=INK, scale_factor=1.06), run_time=0.7)

        # ========================================================== 4 · exit, and the README's slip
        c205 = readme_card(205, label(Q205, 22, INK), quote=True)
        c215 = readme_card(215, mono_line(DEPLOY, 22, INK))
        cards = VGroup(c205, c215).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cards.move_to([LEFT_X + cards.width / 2, 0, 0]).align_to(np.array([0, 2.68, 0]), UP)
        err4 = erratum_tag().next_to(c205.frame, RIGHT, buff=0.35)
        mine = green_chip(MINE, 22, MONO, t2c={"<USER NAME>": TURN})
        mine_cap = label("your image · not run here", 20, S.GREY)
        mine.next_to(c215, DOWN, buff=0.75).align_to(c215, LEFT)
        mine_cap.next_to(mine, UP, buff=0.1).align_to(mine, LEFT).shift(RIGHT * 0.1)
        amd = tag("Intel/AMD laptop: already amd64 · Apple Silicon Mac: rebuild first (see Platforms)", S.GREY)
        amd.next_to(mine, DOWN, buff=0.25).align_to(mine, RIGHT)
        pic4 = VGroup(cards, err4, mine, mine_cap, amd)
        pic4.shift(UP * ((2.7 + -3.35) / 2 - pic4.get_center()[1]))
        assert pic4.get_top()[1] < 2.75 and pic4.get_bottom()[1] > -3.4 and mine.get_right()[0] < 6.5, pic4.get_corner(DR)
        assert amd.get_left()[0] > -6.5, amd.get_left()
        assert c205.get_bottom()[1] > STRIP_TOP + 0.4, "the first card shares the frame with the strip"
        pre = len("sudo docker run --rm -ti ")
        assert MINE[:pre] == DEPLOY[:pre]

        # pad: the amd64 tag (12 words) comes on the last clause; hold it a moment before the cards go
        with self.voiceover(SAY[4], pad=1.2) as vo:
            for line, m in [(c2, x2), (r_v, u2), (r_v, rec)]:      # the strip comes back without its marks
                line.remove(m)
            self.play(FadeOut(VGroup(col, *[it.note for it in items], img, img_name, glaze, frost, moral)),
                      FadeIn(t), run_time=0.5)
            istep(self, t, L30, 0.3)
            t.print(self, [EXIT_ECHO], run_time=0.2)
            t.set_prompt(P_VM)
            bare_prompt(self, t)
            # the VM prompt stays readable until "the README promises": the first card fits above the strip
            vo.wait_until("One more small mismatch")
            self.play(FadeIn(c205, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("the README promises")
            promise = text_span(c205.body, Q205, "pull the image you pushed in step 3")
            u205 = under(promise, TURN)
            self.play(FadeOut(t), Create(u205), FadeIn(err4, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("but this command runs the instructor's")
            self.play(FadeIn(c215, shift=DOWN * 0.15), run_time=0.5)
            dl = substring(c215.body, "dlops/simple-translate")
            u215 = under(dl, TURN)
            self.play(Create(u215), Indicate(dl, color=TURN, scale_factor=1.0), run_time=0.7)
            vo.wait_until("Your image is")
            self.play(FadeIn(mine.frame), TransformFromCopy(glyph_range(c215.body, 0, pre), glyph_range(mine.text, 0, pre)),
                      FadeIn(mine_cap, shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(glyph_range(mine.text, pre), shift=RIGHT * 0.15), run_time=0.5)
            self.add(mine)
            vo.wait_until("your user name")
            ph = substring(mine.text, "<USER NAME>")
            self.play(Indicate(ph, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Run it with the same command")
            self.play(Indicate(mine.text, color=VENV, scale_factor=1.04), run_time=0.7)
            self.add(mine)
            vo.wait_until("once it's built for amd64")
            self.play(FadeIn(amd, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 5 · C6 · extra: the image lags the repo
        repo25 = code("cli.py", 25)
        img_line = mono_line(OUT_IMG[2], 22, OUTPUT)
        img_box = RoundedRectangle(width=img_line.strut.width + 0.5, height=img_line.strut.height + 0.24,
                                   corner_radius=0.1, stroke_color=S.GREY, stroke_width=2).set_fill(TERM_BG, 1)
        # FadeIn (an introducer) adds the opaque box after the TransformFromCopy's line: keep it underneath
        img_box.set_z_index(-1)
        img_cap = grey_words(("in the image ·", "label"), ("dlops/simple-translate", "mono"))
        err5 = erratum_tag("erratum · the published image lags the repo")
        # bottom-up above the 5-row strip: the note row, the repo's line, the image's line, its caption
        NOTE5 = "if Google refuses a request: this version prints your input back"
        note5 = label(NOTE5, 22, S.GREY)
        nodock = tag("not a Docker problem", S.GREY)
        row5 = VGroup(note5, nodock).arrange(RIGHT, buff=0.35)
        row5.move_to([0, STRIP5_TOP + 0.16 + row5.height / 2, 0])
        # right-aligned: the image line starts 7 cells left of `async`
        repo25.move_to([RIGHT_X - repo25.width / 2, row5.get_top()[1] + 0.22 + repo25.height / 2, 0])
        # the image's line sits above the repo's, `async` over `async`, clear of the panel's `cli.py` header
        img_line.shift(UP * (repo25.get_top()[1] + 0.16 + img_box.height / 2 - img_line.strut.get_center()[1]))
        img_line.shift(RIGHT * (code_span(repo25.code, 0, "async")[0].get_left()[0]
                                - substring(img_line, "async")[0].get_left()[0]))
        img_box.move_to(img_line.strut).align_to(img_line.strut, LEFT).shift(LEFT * 0.25)
        img_cap.next_to(img_box, UP, buff=0.1).align_to(img_box, LEFT).shift(RIGHT * 0.08)
        err5.move_to([RIGHT_X - err5.width / 2, img_cap.get_y(), 0])
        src5 = row_tag([("where", "label"), ("uv 0.12.15", "mono"), ("came from", "label")])
        assert row5.get_bottom()[1] > STRIP5_TOP + 0.15 and row5.width < 12.8, (row5.get_bottom(), row5.width)
        assert repo25.get_bottom()[1] > row5.get_top()[1] + 0.2, (repo25.get_bottom(), row5.get_top())
        assert img_box.get_bottom()[1] > repo25.get_top()[1] + 0.12, (img_box.get_bottom(), repo25.get_top())
        assert err5.get_left()[0] > img_cap.get_right()[0] + 0.3 and img_cap.get_top()[1] < 2.6, img_cap.get_top()
        assert err5.get_top()[1] < tr.get_bottom()[1] - 0.1 or err5.get_left()[0] > tr.get_right()[0] + 0.3
        assert img_box.get_left()[0] > -6.55 and repo25.get_left()[0] > -6.55

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(c205, c215, err4, u205, u215, mine, mine_cap, amd)), FadeIn(t),
                      track(tr, 6, extra=True), run_time=0.4)
            resize(self, t, IMG_STRIP, run_time=0.4)
            t.fold = lambda text, first_prefix=0: list(IMG_ROWS)
            c5 = type_cmd(self, t, IMG_CMD, 1.8)
            del t.fold
            x5 = beside(row_tag("extra"), c5.rows[0], buff=0.4)
            pin(self, c5.rows[0], x5, run_time=0.3)
            out5 = t.print(self, OUT_IMG, run_time=0.6, lag=0.1)
            r25, r_uv = out5[2], out5[4]
            # line 8 is where beat 2's `uv = 0.12.15` chip came from
            u_uv = under(substring(r_uv, UV_CFG), TURN)
            beside(src5, r_uv, buff=0.4)
            self.play(Create(u_uv), FadeIn(src5, shift=LEFT * 0.1), run_time=0.5)
            attach(self, r_uv, u_uv)
            attach(self, r_uv, src5)
            vo.wait_until("its cli.py is the older one")
            # the strip keeps the five output lines (rows do not move: same bottom, same pitch) while
            # line 4 is copied up into the image's line
            resize(self, t, IMG_KEEP, run_time=0.7,
                   extra=[FadeIn(img_box), FadeIn(img_cap), TransformFromCopy(r25, img_line)])
            self.play(FadeIn(repo25, shift=UP * 0.15), FadeIn(err5, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("without raise exception equals True")
            old = substring(img_line, "Translator()")
            new = code_span(repo25.code, 0, "raise_exception=True")
            u_old, u_new = under(old, TURN), under(new, VENV)
            self.play(Create(u_old), Indicate(old, color=TURN, scale_factor=1.1), run_time=0.6)
            self.play(Create(u_new), Indicate(new, color=VENV, scale_factor=1.08), run_time=0.7)
            # re-add the split rows, then the underlines: the code panel's opaque box would hide u_new
            self.add(img_line, repo25, u_old, u_new)
            vo.wait_until("If Google refuses a request")
            self.play(FadeIn(note5, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("quietly prints your input back")
            self.play(Indicate(text_span(note5, NOTE5, "prints your input back"), color=INK, scale_factor=1.06),
                      run_time=0.7)
            self.add(note5)
            vo.wait_until("That's not a Docker problem")
            self.play(FadeIn(nodock, shift=LEFT * 0.1), run_time=0.4)
            self.play(pulse(nodock), run_time=0.6)

        # ========================================================== 6 · if the pull itself fails
        rows6 = wrap65(RATE_LINE)
        card6 = fail_card(rows6)
        card6.move_to([0, 2.05 - card6.height / 2, 0])
        rc6 = real_capture_tag("real capture · Debian 13 · 2026-10-13")
        note6 = label("anonymous pulls: a limit per network address", 22, S.GREY)
        row6 = VGroup(note6, rc6)
        note6.next_to(card6.frame, DOWN, buff=0.3).align_to(card6.frame, LEFT).shift(RIGHT * 0.1)
        rc6.next_to(card6.frame, DOWN, buff=0.3).align_to(card6.frame, RIGHT)
        note6.match_y(rc6)                       # one row: the note centred on the tag
        assert note6.get_right()[0] < rc6.get_left()[0] - 0.3, "the note runs into the tag"
        wait6 = green_chip("wait a while", 22)
        or6 = label("or", 22, S.GREY)
        login6 = green_chip(LOGIN, 22, MONO, t2c={"<USER NAME>": TURN})
        fix6 = VGroup(wait6, or6, login6).arrange(RIGHT, buff=0.3).move_to([0, -2.1, 0])
        assert card6.frame.width < 12.9 and fix6.get_top()[1] < row6.get_bottom()[1] - 0.3

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(t, img_box, img_cap, img_line, u_old, repo25, u_new, err5, note5, nodock)),
                      track(tr, 5), run_time=0.5)
            self.play(FadeIn(card6, shift=DOWN * 0.15), FadeIn(rc6, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("with too many requests")
            tm = substring(card6.rows[0], "toomanyrequests")
            u6 = under(tm, ERR, y=card6.rows[0].strut.get_bottom()[1] - 0.02)
            self.play(Create(u6), Indicate(tm, color=ERR, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Docker Hub limits")      # also matches the reworded line proposed by the ASR review
            lim_row = next(r for r in card6.rows if "pull rate limit" in r.text)
            lim = substring(lim_row, "pull rate limit")
            ul = under(lim, TURN, y=lim_row.strut.get_bottom()[1] - 0.02)
            self.play(Create(ul), FadeIn(note6, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("which a classroom can hit")
            self.play(Indicate(note6, color=INK, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Wait a while")
            self.play(FadeIn(wait6, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("or log in first")
            self.play(FadeIn(or6), FadeIn(login6, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("with sudo docker login")
            self.play(Indicate(substring(login6.text, "<USER NAME>"), color=TURN, scale_factor=1.15), run_time=0.6)
            self.add(login6)

        # ========================================================== end · empty frame
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.2)
