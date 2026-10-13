"""S09 · Installing uv (part 2 starts: a fresh VM, then uv, then PATH).

Beats (script.md "## S09", one voiceover block each):
 0  TRACKER B1. A schematic create form (illustration) fills fast; Create -> the instance row; a new
    GOLD dial starts sweeping ("billed per second while running"). The part-1 VM with its ORANGE
    jars fades under a RED cross ("not this one"); GREY note "name taken? ...". TRACKER B2: the
    browser becomes the terminal (10 rows); the dial shrinks to a badge top-right and keeps sweeping
    for the rest of the scene (the VM exists). ▶ your turn beside the prompt.
 1  TRACKER B3 -> B6: the four commands as a fast montage with real outputs; ▶ your turn after cd;
    GREY note "no python3-pip this time" with a struck-through ORANGE chip.
 2  TRACKER B7. `curl -LsSf ... | sh` typed (two rows), not run; four flag labels hang under -LsSf.
 3  `| sh` turns PINK; the script flows from the URL into a PURPLE `sh`; two GREY notes (official
    installer; README line 81: other ways).
 4  The terminal grows to 12 rows; Enter -> real installer output (05-uv-install.txt lines 2-10);
    ▶ your turn; `uv 0.13.0` tagged "at the time of recording"; uv and uvx drop into ~/.local/bin.
 5  TRACKER B7 · extra. `uv --version` -> RED "command not found" (+ "your shell may print -bash:").
 6  V3: the terminal shrinks to a 3-row strip; PATH doors above it; the uv figure knocks on each door
    -> "command not found" under the row.
 7  PANEL installer lines 8-10 (line 10 YELLOW) + README card line 83; TRACKER B8; `source ...`
    typed in the strip; the doors return with PANEL ~/.local/bin/env line 9 and a PURPLE
    ~/.local/bin door slides in at the far left. ▶ your turn.
 8  TRACKER B8 · extra. `uv --version` and `which uv` (07-uv-version.txt); the figure walks in
    through the PURPLE door.
 9  Two shell bubbles (illustration): sh env changes a child shell that pops (RED cross); source
    changes this shell (GREEN check). PANEL the installer's lines in ~/.profile and ~/.bashrc.
10  A PURPLE uv chip absorbs five GREY chips (python -m venv, pip, pip-tools, pyenv, pipx). Fade out.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (CAPTION, MONO, OUTPUT, box, browser_window, check_mark, chip,
                              code_block, code_span, cross_mark, file_glyph, folder_glyph, form_rows,
                              glyph_range, label, line_bar, machine_box, mono, mono_line, substring,
                              tag)
from explainer.components import person_icon
from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, INK, LOOKUP, NARRATION, P_HOME, P_REPO, SYSTEM, TURN, UV,
                    CostDial, PathDoors, capture, illustration_tag, jars, term,
                    tracker_b, your_turn)

SAY = NARRATION["S09"]
PB = "debian12-part-b"

# ------------------------------------------------------------------ commands (README spelling)
APT_UPDATE = "sudo apt-get update"
APT_GIT = "sudo apt install git"
CLONE = "git clone https://github.com/dlops-io/simple-translate.git"
CD = "cd simple-translate"
CURL = "curl -LsSf https://astral.sh/uv/install.sh | sh"
SOURCE = "source $HOME/.local/bin/env"

# ------------------------------------------------------------------ real outputs
_apt = capture("01-apt-update", PB)
APT_OUT = [s + " Done" if s.startswith(("Reading package lists...", "Building dependency tree...",
                                        "Reading state information...")) else s
           for s in _apt.pick(1, (7, 8))]                                     # file lines 2, …, 8-9
_git = capture("02-git", PB)
GIT_HEAD = _git.pick((24, 26))                                                # file lines 25-27
GIT_ASK = _git.pick(27)[0]                                                    # file line 28
GIT_ASK = GIT_ASK[:GIT_ASK.index("[Y/n]") + len("[Y/n]")]                     # cut after [Y/n]
# capture() reads with universal newlines, so apt's mid-line \r progress rows split into extra
# lines: file lines 160-161 are the last two body lines (checked here).
GIT_TAIL = _git.pick((-2, -1))
assert GIT_TAIL[0].startswith("Setting up git (") and GIT_TAIL[1].startswith("Processing triggers")
CLONE_OUT = capture("03-clone", PB).pick(1)                                   # file line 2
_inst = capture("05-uv-install", PB)
INSTALL_OUT = _inst.pick((1, 9))                                              # file lines 2-10
PANEL_LAST = _inst.pick((7, 9))                                               # file lines 8-10
MISSING = capture("06-uv-missing", PB).pick(1)[0]                             # file line 2
_ver = capture("07-uv-version", PB)
UV_VERSION, WHICH_UV = _ver.pick(1)[0], _ver.pick(2)[0]                       # file lines 2, 3
_path = capture("12-python-before", PB).pick((2, 7))                          # file lines 3-8
assert _path[0] == "/home/student/.local/bin"
assert _path[1:4] == ["/usr/local/bin", "/usr/bin", "/bin"] and "games" in _path[4] + _path[5]
_startup = capture("26-startup-files", PB)
STARTUP = _startup.pick((3, 4))                                               # file lines 4-5
ENV_EXPORT = _startup.pick(13)[0].strip()                                     # file line 14
assert ENV_EXPORT.startswith("export PATH=")

# ------------------------------------------------------------------ layout
BOTTOM = -3.5            # terminal bottom edge
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
DOOR_TOP = 2.25          # top of the PATH door frames
BADGE = np.array([6.12, 3.18, 0])
RATE = 1 / 80            # dial turns per second while the VM exists


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def caption_extra(tr, on: bool = True):
    """The tracker caption with (or without) ' · extra' while a non-README command is on screen."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    new = label(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY}) if on else \
        label(s, tr.size, tr.hi_color)
    new.next_to(tr.dots, RIGHT, buff=0.25)
    return Transform(tr.caption, new)


def short_extra():
    return tag("extra", S.GREY)


def header_text(header) -> VGroup:
    """A panel header: a string, or a list of pieces where paths (starting with ~ or /) are set in
    the code font, like code_panel's own header."""
    parts = [header] if isinstance(header, str) else header
    ms = [mono(p, CAPTION, S.GREY) if p.startswith(("~", "/")) else label(p, CAPTION, S.GREY)
          for p in parts]
    return VGroup(*ms).arrange(RIGHT, buff=0.14)          # centred, like code_panel's header


def panel(lines: list[str], header, language: str = "text", size: float = 22) -> VGroup:
    """A capture shown as a panel (same look as code_panel), header naming where it comes from."""
    c = code_block("\n".join(lines), language, font_size=size)
    h = header_text(header)
    h.next_to(c, UP, buff=0.1).align_to(c, LEFT).shift(RIGHT * 0.12)
    g = VGroup(c, h)
    g.code, g.header = c, h
    return g


def readme_card(line_no: int, body: VGroup, width: float | None = None) -> VGroup:
    head = VGroup(mono("README.md", CAPTION, S.GREY), label(f"· line {line_no}", CAPTION, S.GREY))
    head.arrange(RIGHT, buff=0.12)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    frame = box(width or inner.width + 0.5, inner.height + 0.36, S.GREY, fill=S.GREY_DARKER,
                fill_opacity=1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.25)
    g = VGroup(frame, inner)
    g.frame, g.body = frame, body
    return g


def code_tag(parts, color: str = S.GREY, size: float = 22) -> VGroup:
    """tag() with some pieces in the code font: parts = [(text, is_code), ...]. A lone '.' in
    the house serif is easy to miss; in the code font (and white) it reads as the command."""
    ms = [mono(s, size + 4, INK) if code else label(s, size, color) for s, code in parts]
    t = VGroup(*ms).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
    h = mono("|", size).height + 0.16
    b = RoundedRectangle(width=t.width + 0.4, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def mini_doors(n: int = 4) -> VGroup:
    return VGroup(*[mini_door(S.GREY) for _ in range(n)]).arrange(RIGHT, buff=0.12)


def mini_door(color) -> VGroup:
    f = RoundedRectangle(width=0.4, height=0.6, corner_radius=0.04, stroke_color=color,
                         stroke_width=2.5).set_fill(color, 0.15 if color == S.GREY else 0.4)
    k = Dot(radius=0.03, color=color).move_to(f.get_right() + LEFT * 0.08)
    return VGroup(f, k)


def figure(word: str = "uv") -> VGroup:
    """The walking command: a small PINK figure carrying the word."""
    p = person_icon(LOOKUP, 0.42)
    w = mono(word, 26, LOOKUP)
    g = VGroup(p, w).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
    g.person, g.word = p, w
    return g


class InstallUv(VoiceScene):
    # ------------------------------------------------------------- terminal helpers
    def bare_prompt(self, t):
        """The prompt returns (no output): a prompt line with nothing typed yet."""
        ln = t.type(self, "", type_time=0)
        ln.bare = True
        return ln

    def type_cmd(self, t, cmd, type_time=None, fast=False):
        """Type at the waiting prompt (replacing a bare prompt line if there is one). fast: scroll
        in 0.15 s instead of the terminal's 0.35 s (the montage)."""
        if len(t.lines) and getattr(t.lines[-1], "bare", False):
            last = t.lines[-1]
            self.remove(last, *last.submobjects)
            t.lines.remove(last)
        if fast:
            p = t.prompt + " "
            t._make_room(self, len(t.fold(p + cmd, first_prefix=len(p))), run_time=0.15)
        return t.type(self, cmd, type_time)

    def fast_print(self, t, lines, run_time=0.25):
        t._make_room(self, len(lines), run_time=0.15)
        return t.print(self, lines, run_time=run_time)

    def pin(self, line, mob, run_time=0.4, anim=None, behind=False):
        """Show `mob` beside a terminal line and make it part of that line (it scrolls with it).
        The line is re-added as one piece (an earlier Indicate on some of its glyphs splits it)."""
        self.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
        self.remove(mob)
        if behind:
            line.submobjects.insert(0, mob)
        else:
            line.add(mob)
        self.add(line)
        return mob

    def unpin_done(self, pairs):
        for line, m in pairs:
            if m in line.submobjects:
                line.remove(m)

    def answer_yes(self, t, text, pause=0.6):
        ln = self.fast_print(t, [text], run_time=0.2)[0]
        self.wait(pause)
        y = mono_line(text + " Y", t.size, OUTPUT)
        y.shift(ln.strut.get_corner(UL) - y.strut.get_corner(UL))
        yg = y.glyphs[-1].set_color(INK)
        self.play(FadeIn(yg), run_time=0.12)
        self.remove(yg)
        ln.add(yg)
        self.add(ln)
        return ln

    def resize(self, t, rows, run_time=0.8, extra=()):
        """Grow or shrink the terminal to `rows` (bottom edge fixed); it keeps its last lines."""
        ref = term(prompt=t.prompt, rows=rows)
        ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0],
                            BOTTOM - ref.box.get_bottom()[1], 0]))
        n_keep = min(len(t.lines), rows)
        kept = t.lines.submobjects[len(t.lines) - n_keep:]
        gone = t.lines.submobjects[:len(t.lines) - n_keep]
        anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar),
                 t.dots.animate.move_to(ref.dots), t.title.animate.move_to(ref.title)]
        for i, ln in enumerate(kept):
            anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UL)))
        if gone:            # clear the dropped lines first, so they never slide over the title bar
            self.play(FadeOut(VGroup(*gone)), run_time=0.25)
            run_time = max(0.3, run_time - 0.25)
            for ln in gone:
                t.lines.remove(ln)
        self.play(*anims, *extra, run_time=run_time)
        t.rows = rows
        return t

    def construct(self):
        assert len(SAY) == 11, f"S09 has {len(SAY)} SAY lines; this scene times 11"

        tr = place_tracker(tracker_b(1))

        # ========================================================== 0 · a fresh VM
        url = "console.cloud.google.com/compute/instances"
        br = browser_window(url, width=9.1, height=5.8).move_to([-1.95, -0.45, 0])
        ill = illustration_tag().next_to(br.frame, UP, buff=0.08).align_to(br.frame, RIGHT)
        fields = [("Name", "ac215-l01"), ("Region", "us-central1"), ("Zone", "us-central1-a"),
                  ("Machine type", "e2-small"), ("Boot disk", "Debian GNU/Linux 12 (bookworm)"),
                  ("External IPv4", "Ephemeral")]
        form = form_rows(fields, width=8.6, size=22, buff=0.1)
        ftitle = label("Create an instance", 26)
        create = chip("Create", CLOUD, size=22)
        page = VGroup(ftitle, form, create).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        page.move_to(br.content).align_to(br.content, LEFT).shift(RIGHT * 0.2)
        for r in form.rows:
            r.value.set_opacity(0)

        # the instance list after Create (a smaller page)
        br2 = browser_window(url, width=8.8, height=2.5)
        br2.move_to([TRACK_LEFT + 4.4, 2.45 - 1.25, 0])
        ill2 = illustration_tag().next_to(br2.frame, UP, buff=0.08).align_to(br2.frame, RIGHT)
        vmhead = label("VM instances", 26)
        ok = check_mark(0.28, S.GREEN)
        vm_name = mono("ac215-l01", 22)
        vm_zone = mono("us-central1-a", 22, S.GREY)
        ssh = chip("SSH", CLOUD, size=22)
        inst = VGroup(ok, vm_name, vm_zone, ssh).arrange(RIGHT, buff=0.4)
        listing = VGroup(vmhead, inst).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        listing.move_to(br2.content).align_to(br2.content, LEFT).shift(RIGHT * 0.25)

        dial = CostDial(radius=0.55, caption="cost").move_to([4.4, 0.75, 0])
        bill = tag("billed per second while running", COST, size=20).next_to(dial, DOWN, buff=0.25)

        old = machine_box("part-1 VM", width=2.9, height=1.8, color=S.GREY)
        shelf = Line(LEFT * 1.1, RIGHT * 1.1, color=SYSTEM, stroke_width=4)
        jj = VGroup(*jars(5, SYSTEM)).arrange(RIGHT, buff=0.1).next_to(shelf, UP, buff=0.03)
        VGroup(shelf, jj).move_to(old.body)
        old.add(shelf, jj)
        old.move_to([-4.95, -1.55, 0])
        cross = cross_mark(1.0, ERR, stroke=8).move_to(jj)      # over the jars: the title stays legible
        not_this = label("not this one", 26, ERR).next_to(old, RIGHT, buff=0.4).shift(UP * 0.45)
        taken = VGroup(label("name taken?", 24, S.GREY),
                       label("the old VM is still being deleted", 24, S.GREY))
        taken.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(not_this, DOWN, buff=0.35,
                                                                 aligned_edge=LEFT)

        t = term(prompt=P_HOME, rows=10)
        t.shift(np.array([0 - t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
        badge = CostDial(radius=0.3, caption=None).move_to(BADGE)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(br), FadeIn(ill), run_time=0.7)
            self.play(FadeIn(page, shift=UP * 0.1), run_time=0.5)
            # the six rows fill at double speed
            for r in form.rows:
                r.value.set_opacity(1)
                self.play(ShowIncreasingSubsets(r.value, rate_func=linear), run_time=0.33)
            vo.wait_until("and the meter")
            self.play(Indicate(create, color=S.WHITE, scale_factor=1.15), run_time=0.4)
            self.play(Transform(br, br2), Transform(ill, ill2),
                      FadeOut(page, scale=0.5, target_position=br2.content.get_center()),
                      run_time=0.7)
            dial.tracker.add_updater(lambda m, dt: m.increment_value(dt * RATE))
            self.add(dial.tracker)
            self.play(FadeIn(listing, shift=DOWN * 0.1), FadeIn(dial, scale=0.8), run_time=0.6)
            self.play(FadeIn(bill, shift=UP * 0.1), run_time=0.4)

            vo.wait_until("Fresh matters")
            self.play(FadeIn(old, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("never sees pip")
            # fade() scales each part's own opacity (set_opacity would fill the invisible .body)
            self.play(Create(cross), old.animate.fade(0.55), FadeIn(not_this), run_time=0.8)

            vo.wait_until("Create it and SSH in")
            self.play(Indicate(inst, color=S.WHITE, scale_factor=1.06), run_time=0.8)
            vo.wait_until("if the name is taken")
            self.play(FadeIn(taken, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("still being deleted")
            self.play(Indicate(taken[1], color=S.WHITE, scale_factor=1.06), run_time=0.8)

            vo.wait_until("so wait a minute")
            self.play(tr.goto(2), Indicate(ssh, color=S.WHITE, scale_factor=1.25), run_time=0.5)
            badge.tracker.set_value(dial.tracker.get_value())
            dial.tracker.clear_updaters()
            self.remove(dial.tracker)
            badge.tracker.add_updater(lambda m, dt: m.increment_value(dt * RATE))
            self.add(badge.tracker)
            self.play(ReplacementTransform(br.frame, t.box),
                      FadeOut(VGroup(*[m for m in br.submobjects if m is not br.frame]), ill, listing),
                      FadeOut(VGroup(old, cross, not_this, taken, bill)),
                      FadeOut(dial, target_position=BADGE, scale=0.5), FadeIn(badge),
                      FadeIn(VGroup(t.bar, t.dots, t.title), rate_func=lambda a: smooth(max(0, a * 3 - 2))),
                      run_time=0.9)
            p0 = self.bare_prompt(t)
            vo.wait_until("Pause until")
            yt = your_turn().next_to(p0.strut, RIGHT, buff=0.35)
            self.pin(p0, yt, run_time=0.4)

        # ========================================================== 1 · the same four commands
        nopip_l = label("no python3-pip this time", 24, S.GREY)
        nopip_c = chip("sudo apt install python3-pip", SYSTEM, size=22, font=MONO)
        nopip = VGroup(nopip_l, nopip_c).arrange(RIGHT, buff=0.3)
        nopip.move_to([0, 2.25, 0]).align_to([TRACK_LEFT, 0, 0], LEFT)
        strike = Line(nopip_c.get_left() + RIGHT * 0.1, nopip_c.get_right() + LEFT * 0.1,
                      color=S.WHITE, stroke_width=3)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(yt), tr.goto(3), run_time=0.25)
            self.unpin_done([(p0, yt)])
            self.type_cmd(t, APT_UPDATE, 0.35, fast=True)
            self.fast_print(t, APT_OUT)
            self.play(tr.goto(4), run_time=0.2)
            self.type_cmd(t, APT_GIT, 0.35, fast=True)
            self.fast_print(t, GIT_HEAD)
            self.answer_yes(t, GIT_ASK, pause=0.6)                # script: [Y/n], 0.6 s, Y
            self.fast_print(t, ["…", *GIT_TAIL])
            self.play(tr.goto(5), run_time=0.2)
            self.type_cmd(t, CLONE, 0.6, fast=True)
            self.fast_print(t, CLONE_OUT, run_time=0.2)
            self.play(tr.goto(6), run_time=0.2)
            self.type_cmd(t, CD, 0.3, fast=True)
            t.set_prompt(P_REPO)
            t._make_room(self, 1, run_time=0.15)
            p1 = self.bare_prompt(t)
            path = substring(p1, "~/simple-translate")
            self.play(Indicate(path, color=CLOUD, scale_factor=1.15), run_time=0.5)
            yt = your_turn().next_to(p1.strut, RIGHT, buff=0.35)
            self.pin(p1, yt, run_time=0.4)
            self.play(FadeIn(nopip_l, shift=DOWN * 0.1), FadeIn(nopip_c, shift=DOWN * 0.1), run_time=0.4)
            self.play(Create(strike), nopip_c.animate.fade(0.5), run_time=0.4)

        # ========================================================== 2 · curl and its flags
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(yt), FadeOut(nopip), FadeOut(strike), tr.goto(7), run_time=0.4)
            self.unpin_done([(p1, yt)])
            t.clear(self)
            cmd = t.type(self, CURL, type_time=1.6)
            r0, r1 = cmd.rows
            curl_w = substring(r0, "curl")
            letters = [glyph_range(r1, i, i + 1) for i in (5, 6, 7, 8)]          # L s S f
            texts = ["follow redirects", "silent", "but still show errors", "fail on HTTP errors"]
            y0 = r1.strut.get_bottom()[1]
            x_text = letters[3].get_center()[0] + 0.55
            notes = []
            for k, (lt, s) in enumerate(zip(letters, texts)):
                depth = 4 - k                                                  # f nearest, L deepest
                y = y0 - 0.12 - depth * 0.46
                x = lt.get_center()[0]
                lead = VMobject(stroke_color=S.GREY, stroke_width=2.5).set_points_as_corners(
                    [[x, y0 - 0.06, 0], [x, y, 0], [x_text - 0.15, y, 0]])
                flag = mono("-" + "LsSf"[k], 24, TURN)
                desc = label(s, 26, INK)
                lab = VGroup(flag, desc).arrange(RIGHT, buff=0.22)
                lab.move_to([x_text, y, 0], aligned_edge=LEFT)
                flag.align_to(desc, DOWN).shift(DOWN * 0.02)
                notes.append((lt, lead, lab))
            vo.wait_until("First, curl")
            self.play(Indicate(curl_w, color=TURN, scale_factor=1.3), run_time=0.8)
            for (lt, lead, lab), phrase in zip(notes, ["follows redirects", "stays quiet",
                                                       "but shows errors", "and fails"]):
                vo.wait_until(phrase)
                self.play(lt.animate.set_color(TURN), Create(lead), FadeIn(lab, shift=RIGHT * 0.1),
                          run_time=0.5)
            vo.wait_until("instead of handing")
            self.play(Indicate(notes[3][2], color=TURN, scale_factor=1.08), run_time=0.9)

        # ========================================================== 3 · the pipe
        pipe = substring(r1, "| sh")
        pipe_box = SurroundingRectangle(pipe, buff=0.07, corner_radius=0.06, color=LOOKUP, stroke_width=3)
        url_g = substring(r1, "https://astral.sh/uv/install.sh")
        row_y = y0 - 0.85
        script = VGroup(file_glyph(0.5, S.GREY), mono("install.sh", 22, S.GREY)).arrange(RIGHT, buff=0.15)
        script.move_to([url_g.get_center()[0], row_y, 0])
        sh = chip("sh", UV, size=26, font=MONO).move_to([pipe.get_center()[0] + 0.9, row_y, 0])
        sh_cap = label("the shell runs it", 22, S.GREY).next_to(sh, RIGHT, buff=0.25)
        flow = Arrow(script.get_right(), sh.get_left(), buff=0.15, color=LOOKUP, stroke_width=4,
                     max_tip_length_to_length_ratio=0.15, tip_length=0.2)
        link = DashedLine(pipe_box.get_bottom(), sh.get_top(), color=LOOKUP, stroke_width=2.5,
                          dash_length=0.08)
        note1 = label("official installer · you can open the URL and read it first", 24, S.GREY)
        note1.move_to([0, row_y - 0.85, 0]).align_to(t.lines[0], LEFT)
        tip = VGroup(label("other ways: pip, brew  ·  this VM has no pip", 24, INK),
                     label("→", 24, INK), label("use curl", 24, INK)).arrange(RIGHT, buff=0.15)
        card81 = readme_card(81, tip)
        card81.next_to(note1, DOWN, buff=0.3, aligned_edge=LEFT)

        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(VGroup(lead, lab)) for _, lead, lab in notes],
                      *[lt.animate.set_color(INK) for lt, _, _ in notes], run_time=0.4)
            self.play(pipe.animate.set_color(LOOKUP), Create(pipe_box), run_time=0.6)
            vo.wait_until("it hands the script")
            self.play(FadeIn(script, target_position=url_g.get_center(), scale=0.6), run_time=0.6)
            self.play(GrowArrow(flow), FadeIn(sh, scale=0.8), Create(link), run_time=0.6)
            moving = script[0].copy()
            self.play(moving.animate.move_to(sh).scale(0.6), run_time=0.8)
            self.play(FadeOut(moving), Indicate(sh, color=S.WHITE, scale_factor=1.2),
                      FadeIn(sh_cap, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("so you're running code")
            self.play(Indicate(url_g, color=TURN, scale_factor=1.05), run_time=0.9)    # look here
            vo.wait_until("official installer")
            self.play(FadeIn(note1, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("which you can read first")
            self.play(FadeIn(card81, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 4 · run it
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(script, sh, sh_cap, flow, link, note1, card81, pipe_box)),
                      pipe.animate.set_color(INK), run_time=0.4)
            self.resize(t, 12, run_time=0.6)
            out = t.print(self, INSTALL_OUT, run_time=0.8, wrap=True)
            yt = your_turn().next_to(r0.strut, RIGHT, buff=0.35)
            self.pin(r0, yt, run_time=0.4)

            vo.wait_until("version 0.13.0")
            l_dl = t.find("downloading uv")
            ver = substring(l_dl, "uv 0.13.0")
            ul = Line(ver.get_corner(DL) + DOWN * 0.07, ver.get_corner(DR) + DOWN * 0.07,
                      color=S.GREY, stroke_width=3)
            # recorded_tag()'s text at 20 pt, so it stays inside the terminal beside a 46-column line
            rec = tag("at the time of recording", S.GREY, size=20).next_to(l_dl.strut, RIGHT, buff=0.3)
            assert rec.get_right()[0] < t.box.get_right()[0] - 0.05, rec.get_right()
            self.pin(l_dl, ul, run_time=0.3, anim=Create(ul))
            self.pin(l_dl, rec, run_time=0.5)

            vo.wait_until("and uvx")
            l_to = t.find("installing to")
            hl = SurroundingRectangle(l_to.strut, buff=0.05, corner_radius=0.05, stroke_width=0) \
                .set_fill(TURN, 0.2)
            l_uv, l_uvx = line_eq(t, "  uv"), line_eq(t, "  uvx")
            c_uv = chip("uv", UV, size=22, font=MONO).move_to(substring(l_uv, "uv"))
            c_uvx = chip("uvx", UV, size=22, font=MONO).move_to(substring(l_uvx, "uvx"))
            room = c_uv.width + c_uvx.width + 0.1
            folder = folder_glyph(1.45, UV)
            folder.stretch_to_fit_width(max(folder.width, room + 0.4))       # both chips fit inside
            fname = mono("~/.local/bin", 24, UV)
            fold = VGroup(fname, folder).arrange(RIGHT, buff=0.3)
            fold.move_to([0, (l_to.strut.get_bottom()[1] + t.find("everything").strut.get_bottom()[1]) / 2, 0])
            fold.align_to([6.0, 0, 0], RIGHT)
            self.play(FadeIn(fold, shift=LEFT * 0.2), run_time=0.5)
            self.pin(l_to, hl, run_time=0.3, behind=True)
            spot_uv = folder[1].get_center() + RIGHT * (-room / 2 + c_uv.width / 2)
            spot_uvx = folder[1].get_center() + RIGHT * (room / 2 - c_uvx.width / 2)
            vo.wait_until("into dot local")
            self.play(FadeIn(c_uv, scale=0.6), FadeIn(c_uvx, scale=0.6), run_time=0.3)
            self.play(c_uv.animate.move_to(spot_uv), c_uvx.animate.move_to(spot_uvx),
                      path_arc=-0.6, run_time=0.9)
            self.play(Indicate(fname, color=S.WHITE, scale_factor=1.15), run_time=0.6)

        # ========================================================== 5 · uv: command not found
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(yt, rec, ul, hl, fold, c_uv, c_uvx)), caption_extra(tr), run_time=0.4)
            self.unpin_done([(r0, yt), (l_dl, rec), (l_dl, ul), (l_to, hl)])
            ln = self.type_cmd(t, "uv --version", 0.6)
            ex = short_extra().next_to(ln.strut, RIGHT, buff=0.35)
            self.pin(ln, ex, run_time=0.3)
            vo.wait_until("Command not found")
            err = t.print(self, [(MISSING, ERR)], run_time=0.3)[0]
            bash = tag("your shell may print -bash:", S.GREY).next_to(err.strut, RIGHT, buff=0.4)
            self.pin(err, bash, run_time=0.4)
            vo.wait_until("But we just")
            self.play(Indicate(t.find("installing to"), color=S.WHITE, scale_factor=1.05), run_time=1.0)

        # ========================================================== 6 · PATH doors
        doors = PathDoors([*_path[1:4], "…"], door_w=0.6, door_h=1.3,      # file lines 4-6, then
                          gap=0.35, size=24)                                 # one … for the games
        doors.shift(UP * (DOOR_TOP - doors.doors[0].frame.get_top()[1]))
        path_lbl = mono("PATH", 26, LOOKUP).next_to(doors.doors[0].frame, LEFT, buff=0.4)
        row4 = VGroup(path_lbl, doors)
        row4.shift(RIGHT * (0 - row4.get_center()[0]))
        lr_y = doors.get_bottom()[1] - 0.22

        def lr_arrow():
            a = Arrow(LEFT, RIGHT, color=LOOKUP, stroke_width=4, buff=0, tip_length=0.18,
                      max_tip_length_to_length_ratio=0.05)
            a.put_start_and_end_on(np.array([doors.get_left()[0], lr_y, 0]),
                                   np.array([doors.get_right()[0], lr_y, 0]))
            return a

        lr = lr_arrow()
        fig = figure("uv").next_to(doors.doors[0].frame, UP, buff=0.12)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(ex), FadeOut(bash), run_time=0.3)
            self.unpin_done([(ln, ex), (err, bash)])
            self.resize(t, 3, run_time=0.8)
            vo.wait_until("a list of folders")
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in doors.doors], lag_ratio=0.2),
                      FadeIn(path_lbl), run_time=1.0)
            vo.wait_until("left to right")
            # the figure starts walking as the words say "left to right"; the four knocks are
            # budgeted to end when "None contains uv" is spoken
            self.play(GrowArrow(lr), FadeIn(fig, shift=DOWN * 0.2), run_time=0.5)
            per = max(0.45, vo.until("None contains uv") / len(doors.doors))
            for i, d in enumerate(doors.doors):
                if i:
                    prev = doors.doors[i - 1].frame
                    self.play(fig.animate.next_to(d.frame, UP, buff=0.12),
                              prev.animate.set_stroke(S.GREY), run_time=per * 0.4)
                d.frame.set_stroke(LOOKUP)
                self.play(Wiggle(d.frame, scale_value=1.04, rotation_angle=0.015 * TAU,
                                 n_wiggles=2 if per >= 0.6 else 1), run_time=per * 0.6)
            nf = label("command not found", 26, ERR).next_to(lr, DOWN, buff=0.2)
            vo.wait_until("None contains uv")
            self.play(fig.animate.set_color(ERR), FadeIn(nf, shift=UP * 0.1),
                      doors.doors[-1].frame.animate.set_stroke(S.GREY), run_time=0.5)
            vo.wait_until("the shell only knows")
            self.play(Indicate(path_lbl, color=S.WHITE, scale_factor=1.25),
                      Indicate(t.find("uv --version"), color=S.WHITE, scale_factor=1.03), run_time=1.0)

        # ========================================================== 7 · source the env file
        pnl = panel(PANEL_LAST, "uv installer · its last lines", size=20)
        pnl.move_to([0, 1.75, 0])
        bar10 = line_bar(pnl.code, 2, TURN, opacity=0.22)
        body83 = VGroup(label("Reload your shell or run:", 24, INK), mono(SOURCE, 24, INK)).arrange(RIGHT, buff=0.2)
        card83 = readme_card(83, body83).next_to(pnl, DOWN, buff=0.35).align_to(pnl, LEFT)
        reload_ul = Line(body83[0].get_corner(DL), body83[0].get_corner(DR), color=S.GREY, stroke_width=3) \
            .shift(DOWN * 0.08)
        src_ul = Line(body83[1].get_corner(DL), body83[1].get_corner(DR), color=TURN, stroke_width=3) \
            .shift(DOWN * 0.08)
        rnote = VGroup(label("reload = a new SSH window,", 24, S.GREY), label("back in your home folder:", 24, S.GREY),
                       mono("cd simple-translate", 24, S.GREY))
        rnote.arrange(RIGHT, buff=0.15)
        rnote.next_to(card83, DOWN, buff=0.25).align_to(card83, LEFT)

        env = panel([ENV_EXPORT], ["~/.local/bin/env", "· line 9"], language="bash", size=22)
        new_door = doors._door("~/.local/bin", UV)
        gap = doors.gap
        new_w = new_door.frame.width
        total = path_lbl.width + 0.4 + new_w + gap + doors.width
        left0 = -total / 2 + path_lbl.width + 0.4             # the new door's left edge
        new_door.shift(np.array([left0 - new_door.frame.get_left()[0],
                                 DOOR_TOP - new_door.frame.get_top()[1], 0]))
        shift_old = left0 + new_w + gap - doors.doors[0].frame.get_left()[0]
        env.move_to([0, -0.62, 0]).align_to(new_door.frame, LEFT)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(fig, nf, doors, path_lbl, lr)), run_time=0.5)
            self.play(FadeIn(pnl, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("and step 8")
            self.play(tr.goto(8), FadeIn(card83, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("reload your shell")
            self.play(Create(reload_ul), run_time=0.5)
            vo.wait_until("or source the env file")
            self.play(FadeIn(bar10), Create(src_ul), run_time=0.6)
            vo.wait_until("A reload means")
            self.play(FadeIn(rnote, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("back in your home")
            self.play(Indicate(rnote[1], color=CLOUD, scale_factor=1.1), run_time=0.8)
            vo.wait_until("so you'd cd")
            self.play(Indicate(rnote[2], color=S.WHITE, scale_factor=1.1),
                      run_time=0.9)
            vo.wait_until("Sourcing is quicker")
            self.play(FadeOut(VGroup(reload_ul, rnote)), run_time=0.3)
            src_ln = self.type_cmd(t, SOURCE, 0.8, fast=True)
            t._make_room(self, 1, run_time=0.15)
            self.bare_prompt(t)                                   # → (no output)
            self.play(FadeOut(VGroup(pnl, bar10, card83, src_ul)),
                      FadeIn(doors), FadeIn(path_lbl), FadeIn(lr),
                      FadeIn(env, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("it puts that folder")
            env_part = env.code.code_lines[0]
            lr_new = Arrow(LEFT, RIGHT, color=LOOKUP, stroke_width=4, buff=0, tip_length=0.18,
                           max_tip_length_to_length_ratio=0.05)
            lr_new.put_start_and_end_on(np.array([left0, lr_y, 0]),
                                        np.array([doors.get_right()[0] + shift_old, lr_y, 0]))
            # the row makes room while the PURPLE door slides in from the left (one motion)
            self.play(doors.doors.animate.shift(RIGHT * shift_old), Transform(lr, lr_new),
                      path_lbl.animate.next_to(new_door.frame, LEFT, buff=0.4),
                      FadeIn(new_door, shift=RIGHT * 0.8, rate_func=lambda a: smooth(max(0, a * 1.6 - 0.6))),
                      run_time=0.7)
            self.remove(new_door)                       # it now lives inside the row
            doors.doors.submobjects.insert(0, new_door)
            vo.wait_until("first in PATH")
            self.play(Indicate(new_door.label, color=S.WHITE, scale_factor=1.15),
                      Indicate(env_part, color=UV, scale_factor=1.04), run_time=0.6)
            vo.wait_until("Pause and run")
            # the source line fills all 65 columns: the tag sits on the row above, at its end,
            # and a YELLOW underline ties it to the command
            yt = your_turn()
            yt.move_to([6.2 - yt.width / 2, src_ln.strut.get_center()[1] + t.pitch, 0])
            cmd_g = substring(src_ln, SOURCE)
            src_u = Line(cmd_g.get_corner(DL) + DOWN * 0.07, cmd_g.get_corner(DR) + DOWN * 0.07,
                         color=TURN, stroke_width=3)
            self.pin(src_ln, src_u, run_time=0.3, anim=Create(src_u))
            self.pin(src_ln, yt, run_time=0.4)

        # ========================================================== 8 · it works
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(yt), FadeOut(src_u), caption_extra(tr), run_time=0.3)
            self.unpin_done([(src_ln, yt), (src_ln, src_u)])
            l1 = self.type_cmd(t, "uv --version", 0.5)
            ex1 = short_extra().next_to(l1.strut, RIGHT, buff=0.35)
            self.pin(l1, ex1, run_time=0.25)
            t.print(self, [UV_VERSION], run_time=0.3)
            fig2 = figure("uv").next_to(new_door.frame, UP, buff=0.12)
            self.play(FadeIn(fig2, shift=DOWN * 0.2), run_time=0.3)
            self.play(fig2.animate.move_to(new_door.frame).scale(0.85),
                      new_door.frame.animate.set_fill(UV, 0.4), run_time=0.6)
            vo.wait_until("and which uv")
            l2 = self.type_cmd(t, "which uv", 0.4)
            ex2 = short_extra().next_to(l2.strut, RIGHT, buff=0.35)
            self.pin(l2, ex2, run_time=0.25)
            wl = t.print(self, [WHICH_UV], run_time=0.3)[0]
            part = substring(wl, "/home/student/.local/bin")
            self.play(part.animate.set_color(UV), Indicate(new_door.label, color=S.WHITE, scale_factor=1.15),
                      run_time=0.7)

        # ========================================================== 9 · why source, not sh
        top_y = 2.45
        t_sh = mono("sh $HOME/.local/bin/env", 24, INK).move_to([-3.35, top_y, 0])
        t_src = mono(SOURCE, 24, INK).move_to([3.35, top_y, 0])
        ill9 = illustration_tag().move_to([5.0, -0.6, 0])

        def bubble(title, w, h, color=S.GREY):
            b = box(w, h, color, fill_opacity=0.06)
            tt = label(title, 22, S.GREY).move_to(b.get_corner(UL), aligned_edge=UL).shift(np.array([0.2, -0.12, 0]))
            row = VGroup(mono("PATH", 22, LOOKUP), mini_doors(4)).arrange(RIGHT, buff=0.25)
            row.move_to(b).shift(DOWN * 0.15 + LEFT * 0.1)
            g = VGroup(b, tt, row)
            g.frame, g.title, g.row = b, tt, row
            return g

        parent_l = bubble("your shell", 5.2, 1.5).move_to([-3.35, 1.2, 0])
        child = bubble("child shell (sh)", 4.4, 1.4).move_to([-2.75, -0.42, 0])
        parent_r = bubble("your shell", 5.2, 1.5).move_to([3.35, 1.2, 0])
        spawn = Line(parent_l.frame.get_bottom() + RIGHT * 0.6, child.frame.get_top() + RIGHT * 0.0,
                     color=S.GREY, stroke_width=2.5)

        def door_in(g):
            d = mini_door(UV)
            first = g.row[1][0]
            d.move_to(first)
            return d

        with self.voiceover(SAY[9]) as vo:
            # `which uv` (extra) stays in the strip, so the caption keeps " · extra" until it goes
            self.play(FadeOut(VGroup(fig2, doors, path_lbl, lr, env)), run_time=0.5)
            self.play(FadeIn(t_sh), FadeIn(t_src), FadeIn(ill9), FadeIn(parent_l), FadeIn(parent_r),
                      run_time=0.7)
            vo.wait_until("Plain sh")
            self.play(Create(spawn), FadeIn(child, shift=DOWN * 0.3, scale=0.8), run_time=0.6)
            dc = door_in(child)
            self.play(child.row[1].animate.shift(RIGHT * 0.52), run_time=0.3)
            dc.shift(UP * 0.9).set_opacity(0)
            self.play(dc.animate.shift(DOWN * 0.9).set_opacity(1), run_time=0.4)
            vo.wait_until("that exits at once")
            self.play(FadeOut(VGroup(child, dc), scale=1.25), FadeOut(spawn), run_time=0.5)
            xl = cross_mark(0.45, ERR, stroke=7).next_to(parent_l.row, RIGHT, buff=0.3)
            self.play(Create(xl), Indicate(parent_l.row, color=S.WHITE, scale_factor=1.05), run_time=0.6)
            vo.wait_until("source changes this one")
            dr = door_in(parent_r)
            self.play(parent_r.row[1].animate.shift(RIGHT * 0.52), run_time=0.3)
            dr.shift(UP * 0.9).set_opacity(0)
            self.play(dr.animate.shift(DOWN * 0.9).set_opacity(1), run_time=0.4)
            ck = check_mark(0.45, S.GREEN, stroke=7).next_to(parent_r.row[1], RIGHT, buff=0.3)
            self.play(Create(ck), run_time=0.4)

            st = panel(STARTUP, ["~/.profile", "line 29 ·", "~/.bashrc", "line 115 · added by the installer"],
                       size=24)
            st.move_to([0, 1.2, 0])
            dots_ul = SurroundingRectangle(VGroup(_dot_part(st.code, 0), _dot_part(st.code, 1)), buff=0.08,
                                           corner_radius=0.06, stroke_color=TURN, stroke_width=2.5) \
                .set_fill(TURN, 0.12)
            # the note sits right under the highlighted column, its dot in the code font
            dot_note = code_tag([(".", True), ("means source", False)])
            dot_note.next_to(st, DOWN, buff=0.3).align_to(dots_ul, LEFT)
            new_ssh = tag("a new SSH session finds uv too", S.GREY).align_to(st, LEFT).match_y(dot_note)
            assert new_ssh.get_right()[0] < dot_note.get_left()[0] - 0.4
            vo.wait_until("The installer also")
            self.play(FadeOut(VGroup(t_sh, t_src, ill9, parent_l, parent_r, dr, xl, ck)), run_time=0.5)
            self.play(FadeIn(st, shift=UP * 0.1), run_time=0.6)
            self.play(Create(dots_ul), FadeIn(dot_note), run_time=0.6)
            vo.wait_until("so next time")
            self.play(FadeIn(new_ssh, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("uv is found by itself")
            self.play(Indicate(t.find("/home/student/.local/bin/uv"), color=UV, scale_factor=1.06), run_time=1.0)

        # ========================================================== 10 · what uv replaces
        core = chip("uv", UV, size=60, font=MONO).move_to([0, 0.1, 0])
        tools = [("python -m venv", "makes a venv"), ("pip", "installs packages"),
                 ("pip-tools", "locking"), ("pyenv", "installs Pythons"), ("pipx", "installs tools")]
        spots = [[-4.3, 1.55, 0], [4.3, 1.55, 0], [4.3, -1.5, 0], [0, -2.55, 0], [-4.3, -1.5, 0]]
        items = []
        for (name, what), p in zip(tools, spots):
            c = chip(name, S.GREY, size=28, font=MONO)
            w = label(what, 22, S.GREY).next_to(c, DOWN, buff=0.12)
            items.append(VGroup(c, w).move_to(p))
        one = label("one fast tool", 28, UV).next_to(core, DOWN, buff=0.3)

        with self.voiceover(SAY[10]) as vo:
            # the `uv` of `which uv`'s answer stays behind and becomes the big uv chip
            uv_word = substring(wl, "uv").copy()
            self.add(uv_word)
            self.play(FadeOut(VGroup(st, dots_ul, dot_note, new_ssh)), FadeOut(t.box), FadeOut(t.bar),
                      FadeOut(t.dots), FadeOut(t.title), FadeOut(t.lines), caption_extra(tr, False),
                      run_time=0.6)
            self.play(ReplacementTransform(uv_word, core.text), FadeIn(core.box, scale=0.6), run_time=0.7)
            self.remove(core.text, core.box)
            self.add(core)
            vo.wait_until("One fast tool")
            self.play(FadeIn(one, shift=UP * 0.1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g, shift=(core.get_center() - g.get_center()) * -0.08) for g in items],
                                  lag_ratio=0.15), run_time=1.0)
            for g, phrase in zip(items, ["the venv module", "pip,", "pip-tools", "pyenv", "and pipx"]):
                vo.wait_until(phrase)
                self.play(g.animate.move_to(core).scale(0.2).set_opacity(0),
                          core.animate(rate_func=there_and_back).scale(1.15), run_time=0.6)
                self.remove(g)
            self.play(Indicate(one, color=S.WHITE, scale_factor=1.1), run_time=min(0.8, vo.remaining(0.5)))

        badge.tracker.clear_updaters()
        self.remove(badge.tracker)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)


def line_eq(t, s):
    """The latest terminal line whose text is exactly `s`."""
    for ln in reversed(t.lines.submobjects):
        if getattr(ln, "text", None) == s:
            return ln
    raise KeyError(s)


def _dot_part(code, k):
    """The `. "$HOME/.local/bin/env"` part of grep output line k (after 'file:line:')."""
    line = code.source.split("\n")[k]
    sub = line[line.index(':', line.index(':') + 1) + 1:]
    return code_span(code, k, sub)
