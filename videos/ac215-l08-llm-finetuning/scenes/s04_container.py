"""S04 · The dataset-creator container (README "Dataset › Run Container", steps 1-4, and extras).
Lecture: none (no lecture tag).

Beats (script.md "## S04", one voiceover block each):
 0  TRACKER DsRun 1. Full-width laptop terminal (12 rows, ~/AC215$): `cd llm-finetuning/dataset-creator`
    (no output), the prompt becomes .../dataset-creator$. TRACKER DsRun 2: `sh docker-shell.sh` with
    ▶ your turn -> laptop/07 lines 3 (cut after "FINISHED"), 9, 12, 15, 16, …, 20 (BuildKit padding
    squeezed, times as GREY tags); the base image python:3.12-slim-bookworm ORANGE, uv PURPLE;
    45.1s YELLOW with the GREY tag "fast network · expect a few minutes"; a GREY chip in the top band:
    "source: not found? → bash docker-shell.sh (shown in a minute)".
 1  The terminal shrinks to a 3-row strip (the typed command and line 20). CODE(dataset-creator/
    docker-shell.sh: 8, 13, 16–22, folded, 20 pt, line 19 wrapped) on the right; each named line
    lights and its picture is pulled out of it to the left (TransformFromCopy): 8 -> env.dev glyph
    + GREY arrow; 13 -> TEAL image box; 16 -> TEAL container box; 17, 18 -> the PINK mounts
    `dataset-creator → /app`, `secrets → /secrets` (GOLD dashed key outline, empty). On "Three
    variables" the panel fades, the picture moves to the centre and lines 19–21 become three chips
    GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT, GCS_BUCKET_NAME (arrows into the container);
    `--rm` (kept from line 16) becomes the GREY tag "removed on exit" on the container.
 2  The picture fades; the terminal grows back (10 rows): laptop/07 lines 21–26 and the prompt
    app@6f5113cdb660:/app$ (line 27 cut before " exit"); frame TEAL, title "container ·
    llm-dataset-creator". "activated" underlined YELLOW with the GREY erratum tag "printed before
    the activation line" (line 26 flashes); "no (app) prefix" beside the prompt. Extra card "which
    Python, which settings" -> dataset-creator/00 lines 5, 9–11 (/.venv/bin/python GREEN). A new
    prompt: the container id flashes, GREY tag "your id will differ".
 3  TRACKER DsRun 3. GREY chip "README.md · line 69 · a Prerequisites tip, run inside the
    container". `ls -la /secrets` with ▶ -> dataset-creator/01 lines 2–4; a GREY dashed ghost row
    "with a key: llm-service-account.json" under it; the "." flashes.
 4  TRACKER DsRun 4. The terminal grows to 12 rows. `python cli.py --help` with ▶ ->
    dataset-creator/04 lines 2–10; the three flags light in turn; GREY caption "no key needed yet:
    the clients look for credentials on their first call"; the prompt returns and flashes. 2 s hold.
 5  The first terminal steps aside; a second terminal (8 rows, "laptop · second terminal",
    .../dataset-creator$, GREY `extra` on its title bar) slides in in its place; tracker " · extra".
    `dash docker-shell.sh` -> laptop/20 line 2 RED; RED stamp "Debian · Ubuntu · WSL: sh is dash",
    GREEN fix chip `bash docker-shell.sh`, GREY note "macOS: sh works". `cd ..`;
    `sh dataset-creator/docker-shell.sh` -> laptop/21 line 2 (wrapped) RED; stamp "run it from inside
    the folder", fix chip "cd into the folder first · README.md:68"; `cd dataset-creator`. A RED card
    (no terminal): a second `sh docker-shell.sh` while one runs -> Conflict (laptop/11 lines 21–24)
    · use the laptop shell, or exit first.
 6  The traps clear. `docker images` (extra) -> laptop/09 line 2 cut after "DISK USAGE", line 3 cut
    after "1.64GB"; 1.64GB YELLOW. Under the terminal the TEAL image block: ORANGE base slab
    python:3.12-slim-bookworm, GREEN /.venv slab with the chip "133 packages · 587 MB"
    (dataset-creator/02) and GREY dashed chips chromadb, langchain + GREY erratum tag "never
    imported here", a thin TEAL /app layer on top. The second terminal slides away and the
    first comes back at the container prompt; everything fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    ReplacementTransform,
    RoundedRectangle,
    TransformFromCopy,
    VGroup,
)

from common import *  # noqa: F401,F403
from common import _drop_bare, _mixed_row, _with_header
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ the real captures (file line numbers)
BUILD = capture("laptop/07")
assert BUILD.cmd == "sh docker-shell.sh", BUILD.cmd
assert "Building 45.1s (11/11) FINISHED" in BUILD.line(3), BUILD.line(3)
assert "python:3.12-slim-bookworm" in BUILD.line(9) and "uv sync" in BUILD.line(15), BUILD.lines
assert BUILD.line(23) == "Environment ready! Virtual environment activated.", BUILD.line(23)
assert BUILD.line(26) == "Activating virtual environment...", BUILD.line(26)
assert BUILD.cut_before(27, " exit") == P_CTR_DC, BUILD.line(27)
WHO = capture("dataset-creator/00")            # (extra card, never typed) which python, which settings
assert WHO.line(5) == "/.venv/bin/python", WHO.line(5)
assert WHO.line(11).startswith("GOOGLE_APPLICATION_CREDENTIALS=/secrets/"), WHO.line(11)
LS = capture("dataset-creator/01")
assert LS.cmd == "ls -la /secrets" and LS.line(2) == "total 0", LS.lines
HELP = capture("dataset-creator/04")
assert HELP.cmd == "python cli.py --help", HELP.cmd
DASH = capture("laptop/20")
assert DASH.cmd == "dash docker-shell.sh" and "source: not found" in DASH.line(2), DASH.lines
WRONG = capture("laptop/21")
assert WRONG.cmd == "sh dataset-creator/docker-shell.sh" and "../env.dev" in WRONG.line(2), WRONG.lines
AGAIN = capture("laptop/11")                   # the Conflict card's source (not printed)
assert "Conflict." in AGAIN.line(21) and "already in use" in AGAIN.line(21) + AGAIN.line(22), AGAIN.lines
IMG = capture("laptop/09")
assert IMG.cmd == "docker images" and "1.64GB" in IMG.line(3), IMG.lines
PKG = capture("dataset-creator/02")            # 133 packages, 587M, chromadb and langchain installed
assert PKG.line(13) == "packages in /.venv: 133" and PKG.line(14).startswith("587M"), PKG.lines
assert PKG.line(2).startswith("chromadb ") and PKG.line(6).startswith("langchain "), PKG.lines

CD1 = "cd llm-finetuning/dataset-creator"        # README.md:83 "make sure you are inside" (no output)
CD_UP = "cd .."                                  # (extra) navigation, no output
CD_DC = "cd dataset-creator"                     # (extra) navigation, no output
assert source_line("README.md", 68).find("Always `cd` into the container folder") >= 0
assert "ls -la /secrets" in source_line("README.md", 69)

# ------------------------------------------------------------------ layout
T_ROWS_MID = 10                 # beats 2-3: room for the extra card / README chip above the terminal
PANEL_RIGHT, PANEL_TOP = 6.45, 3.45   # beat 1's code panel: right of the tracker (x >= -1.9)
PIC_LEFT, PIC_W = -6.45, 5.0     # beat 1's picture, left of the panel
GAP_Y = STRIP_TOP + 0.12


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


def flash(mob, color: str = TURN, k: float = 1.15):
    return Indicate(mob, color=color, scale_factor=k)


def code_row(p, n: int, k: int = 0):
    return p.code.code_lines[p.rows_of(n)[k]]


def tinted_box(w: float, h: float, color: str, opacity: float = 0.1, stroke: float = 3,
               dashed: bool = False) -> VGroup:
    fr = box(w, h, color, fill=S.BG, fill_opacity=1.0, radius=0.12, stroke=stroke, dashed=dashed)
    tint = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_width=0).set_fill(color, opacity)
    g = VGroup(fr, tint)
    g.frame = fr
    return g


def mixed_chip(parts, color: str = S.GREY) -> VGroup:
    """A chip holding one row that mixes mono (`code`) and serif pieces."""
    row = _mixed_row(parts)
    fr = box(row.width + 0.4, row.height + 0.26, color, fill=S.BG, fill_opacity=0.95, radius=0.1)
    row.move_to(fr)
    g = VGroup(fr, row)
    g.frame, g.row = fr, row
    return g


def mount_row(host: str, path: str, x_arrow: float, with_key: bool = False) -> VGroup:
    """GREY host folder (+ an empty GOLD key outline) -> PINK arrow -> TEAL container path."""
    h = mono(host, CAPTION, LAPTOP)
    parts = [h]
    if with_key:
        k = key_outline(0.24).next_to(h, RIGHT, buff=0.15)
        parts.append(k)
    left = VGroup(*parts)
    a = Arrow([x_arrow, 0, 0], [x_arrow + 0.5, 0, 0], buff=0, color=LOOKUP, stroke_width=4,
              tip_length=0.16, max_tip_length_to_length_ratio=0.3)
    left.set_y(0)
    p = mono(path, CAPTION, CTR).next_to(a, RIGHT, buff=0.12)
    g = VGroup(left, a, p)
    g.host, g.arrow, g.path = left, a, p
    g.key = parts[1] if with_key else None
    return g


class DatasetContainer(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · steps 1-2: cd, sh docker-shell.sh
        tr = tracker("DsRun", 1)
        t = term(P_WS, rows=12, title=LAPTOP_TITLE)
        chip0 = mixed_chip(["`source: not found`", "?", "→", "`bash docker-shell.sh`", "(shown in a minute)"])
        chip0.move_to([CHIP_RIGHT - chip0.width / 2, TOPCHIP_Y, 0])
        assert chip0.get_top()[1] < tr.get_bottom()[1] - 0.03 or chip0.get_left()[0] > tr.get_right()[0]
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            bare_prompt(self, t)
            vo.wait_until("go into the dataset-creator")
            type_cmd(self, t, CD1, 0.8)
            cd_prompt(self, t, P_DC, run_time=0.7)
            vo.wait_until("Step 2")
            self.play(tr.goto(2), run_time=0.5)
            sh = type_cmd(self, t, BUILD.cmd, 0.6)
            yt0 = beside(your_turn(), t, sh)
            pin(self, sh, yt0, run_time=0.4)
            vo.wait_until("The first build")
            out0 = print_build(self, t, [BUILD.cut(3, "FINISHED"), BUILD.squeeze(9), BUILD.squeeze(12),
                                         BUILD.squeeze(15), BUILD.squeeze(16), "…", BUILD.squeeze(20)],
                               run_time=1.2)
            r3, r9, r15, r20 = out0[0], out0[1], out0[3], out0[6]
            self.play(substring(r9, "python:3.12-slim-bookworm").animate.set_color(SYSTEM),
                      substring(r15, "uv").animate.set_color(TOOL), run_time=0.5)
            vo.wait_until("Here it took")
            s45 = substring(r3, "45.1s")
            self.play(s45.animate.set_color(TURN), run_time=0.3)
            self.play(flash(s45, TURN, 1.2), run_time=0.5)
            vo.wait_until("expect a few minutes")
            pin(self, r3, beside(grey_tag("fast network · expect a few minutes"), t, r3, buff=0.4), run_time=0.4)
            vo.wait_until("If you see")
            self.play(FadeIn(chip0, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("the fix is coming")
            self.play(flash(chip0.row, TURN, 1.04), run_time=0.7)

        # ========================================================== 1 · what the script does
        p = src_panel("dataset-creator/docker-shell.sh", [8, 13, (16, 22)], size=20, wrap={19: ["$GOOGLE"]})
        # the header drops " · line 19 wrapped" to fit right of the tracker (the GREY ↪ shows the wrap)
        _with_header(p, "dataset-creator/docker-shell.sh · lines 8–22 (folded)")
        place(p, right=PANEL_RIGHT, top=PANEL_TOP)
        assert p.get_left()[0] > tr.get_right()[0] + 0.1 and p.get_bottom()[1] > STRIP_TOP + 0.05, p.get_corner(DOWN + LEFT)
        bars = {n: p.bar(n, c, 0.2) for n, c in ((8, S.GREY), (13, CTR), (16, CTR), (17, LOOKUP), (18, LOOKUP),
                                                 (19, S.GREY), (20, S.GREY), (21, S.GREY))}
        pic_right = PIC_LEFT + PIC_W
        assert pic_right < p.get_left()[0] - 0.15
        cx = PIC_LEFT + PIC_W / 2
        # env.dev -> image -> container (built in place, left of the panel)
        env = file_row("env.dev", INK)
        place(env, left=PIC_LEFT + 0.25, cy=2.5)
        img = tinted_box(PIC_W, 0.62, CTR)
        place(img, left=PIC_LEFT, cy=1.5)
        img_t = VGroup(label("image", CAPTION, S.GREY), mono("llm-dataset-creator", CAPTION, CTR)).arrange(RIGHT, buff=0.2)
        img_t.move_to(img)
        image = VGroup(img, img_t)
        a_env = Arrow(env.glyph.get_bottom() + DOWN * 0.04, [env.glyph.get_center()[0], img.get_top()[1] + 0.04, 0],
                      buff=0, color=S.GREY, stroke_width=3, tip_length=0.14, max_tip_length_to_length_ratio=0.4)
        ctr = tinted_box(PIC_W, 2.0, CTR, 0.06)
        place(ctr, left=PIC_LEFT, top=0.72)
        ctr_t = label("container", CAPTION, CTR).move_to(ctr.get_corner(UP + LEFT), aligned_edge=UP + LEFT) \
            .shift(np.array([0.22, -0.14, 0]))
        container = VGroup(ctr, ctr_t)
        a_run = Arrow([cx, img.get_bottom()[1] - 0.04, 0], [cx, ctr.get_top()[1] + 0.04, 0], buff=0, color=CTR,
                      stroke_width=3, tip_length=0.14, max_tip_length_to_length_ratio=0.4)
        x_arrow = PIC_LEFT + 0.25 + mono("dataset-creator", CAPTION).width + 0.12
        m1 = mount_row("dataset-creator", "/app", x_arrow)
        m2 = mount_row("secrets", "/secrets", x_arrow, with_key=True)
        for m, y in ((m1, -0.05), (m2, -0.75)):
            m.shift(UP * y)
            m.host.align_to(ctr, LEFT).shift(RIGHT * 0.25)
        assert m2.path.get_right()[0] < ctr.get_right()[0] - 0.1, (m2.path.get_right(), ctr.get_right())
        assert ctr.get_bottom()[1] > STRIP_TOP + 0.08 and env.get_top()[1] < tr.get_bottom()[1] - 0.05
        for m in (img_t, ctr_t, m1, m2):           # text above the boxes' opaque fill, whatever the add order
            m.set_z_index(2)
        picture = VGroup(env, a_env, image, a_run, container, m1, m2)
        # the final layout: the picture moves right, the three -e chips sit beside the container
        dx = 1.0
        names = ["GOOGLE_APPLICATION_CREDENTIALS", "GCP_PROJECT", "GCS_BUCKET_NAME"]
        chips = VGroup(*[chip(nm, S.GREY, size=CAPTION, font=MONO) for nm in names])
        chips.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        place(chips, left=pic_right + dx + 0.8, cy=ctr.get_center()[1])
        assert chips.get_right()[0] < 6.4, chips.get_right()
        c_arrows = VGroup(*[Arrow(c.get_left() + LEFT * 0.06, [pic_right + dx + 0.04, c.get_center()[1], 0],
                                  buff=0, color=S.GREY, stroke_width=3, tip_length=0.13,
                                  max_tip_length_to_length_ratio=0.3) for c in chips])
        spans = [p.span(19, names[0]), p.span(20, names[1]), p.span(21, names[2])]
        rm_tag = grey_tag("removed on exit")
        rm_tag.move_to(ctr_t).align_to(ctr, RIGHT).shift(LEFT * 0.2 + RIGHT * dx)
        rm_tag.set_z_index(5)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(chip0), run_time=0.3)
            resize(self, t, 3, keep=[sh.rows[0], sh.rows[1], r20], run_time=0.6)
            self.play(FadeIn(p, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("It reads env.dev")
            self.play(FadeIn(bars[8]), TransformFromCopy(code_row(p, 8), env), run_time=0.7)
            self.play(GrowArrow(a_env), run_time=0.35)
            vo.wait_until("builds the image")
            # the box first, so the text lands on top of its opaque fill
            self.play(FadeIn(bars[13]), FadeIn(img), TransformFromCopy(code_row(p, 13), img_t), run_time=0.7)
            vo.wait_until("and runs it")
            self.play(FadeIn(bars[16]), GrowArrow(a_run), FadeIn(ctr), TransformFromCopy(code_row(p, 16), ctr_t),
                      run_time=0.8)
            vo.wait_until("this folder becomes")
            self.play(FadeIn(bars[17]), TransformFromCopy(code_row(p, 17), m1), run_time=0.7)
            vo.wait_until("and your secrets folder")
            self.play(FadeIn(bars[18]), TransformFromCopy(code_row(p, 18), m2), run_time=0.7)
            self.play(flash(m2.key, KEY, 1.3), run_time=0.5)
            vo.wait_until("Three variables")
            rm = p.span(16, "--rm").copy().set_z_index(5)
            self.add(rm)
            self.play(*[FadeIn(bars[n]) for n in (19, 20, 21)], run_time=0.3)
            # --rm parks in the container's title row (where its tag will be) while the panel leaves
            self.play(*[TransformFromCopy(s, c) for s, c in zip(spans, chips)], rm.animate.move_to(rm_tag),
                      FadeOut(VGroup(p, *bars.values())), picture.animate.shift(RIGHT * dx), run_time=1.0)
            self.play(*[GrowArrow(a) for a in c_arrows], run_time=0.5)
            vo.wait_until("The dash dash rm")
            self.play(flash(rm, TURN, 1.2), run_time=0.5)
            self.play(ReplacementTransform(rm, rm_tag), run_time=0.8)

        # ========================================================== 2 · the banner, read kindly; the extra check
        xc = extra_card("which Python, which settings")
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(picture, chips, c_arrows, rm_tag)), run_time=0.5)
            resize(self, t, T_ROWS_MID, run_time=0.6)
            place(xc, right=6.4, cy=(t.box.get_top()[1] + 2.9) / 2)
            assert xc.get_left()[0] > tr.get_right()[0] + 0.1 or xc.get_top()[1] < tr.get_bottom()[1]
            ban = t.print(self, BUILD.out((21, 26)), run_time=0.8)
            r22, r23, r26 = ban[1], ban[2], ban[5]
            assert r23.text == BUILD.line(23) and r26.text == BUILD.line(26), (r23.text, r26.text)
            anims = enter_container(t, "dc")
            pr = bare_prompt(self, t)
            self.play(*anims, run_time=0.6)
            vo.wait_until("it says activated")
            act = substring(r23, "activated")
            ua = under(act, TURN, stroke=3)
            self.play(act.animate.set_color(TURN), run_time=0.3)
            pin(self, r23, ua, run_time=0.3, anim=Create(ua))
            err = erratum_tag("printed before the activation line")
            err.move_to(r22.strut).set_x(act.get_center()[0])
            if err.get_right()[0] > t.box.get_right()[0] - 0.12:
                err.align_to(t.box, RIGHT).shift(LEFT * 0.12)
            pin(self, r22, err, run_time=0.4, anim=FadeIn(err, shift=DOWN * 0.08))
            vo.wait_until("before the activation line")
            self.play(flash(r26.glyphs, TURN, 1.04), run_time=0.7)
            vo.wait_until("and the prompt never")
            noapp = beside(note("no (app) prefix"), t, pr, buff=0.4)
            pin(self, pr, noapp, run_time=0.4)
            self.play(flash(glyph_range(pr, 0, 3), TURN, 1.3), run_time=0.6)
            vo.wait_until("Both are harmless")
            self.play(flash(err.text, TURN, 1.05), flash(noapp, TURN, 1.05), run_time=0.7)
            vo.wait_until("an extra check")
            self.play(FadeIn(xc, shift=DOWN * 0.1), caption_extra(tr, True), run_time=0.5)
            out2 = show(self, t, WHO, 5, (9, 11), run_time=0.6)
            r5 = out2[0]
            vo.wait_until("Python comes from")
            self.play(substring(r5, "/.venv").animate.set_color(VENV), run_time=0.3)
            self.play(flash(r5.glyphs, VENV, 1.08), run_time=0.6)
            vo.wait_until("and your settings arrived")
            self.play(*[flash(r.glyphs, TURN, 1.04) for r in out2[1:]], run_time=0.8)
            vo.wait_until("The part after app")
            self.play(FadeOut(xc), caption_extra(tr, False), run_time=0.4)
            pr2 = bare_prompt(self, t)
            cid = substring(pr2, P_CTR_DC.split("@")[1].split(":")[0])
            self.play(flash(cid, LOOKUP, 1.2), run_time=0.6)
            uid = under(cid, LOOKUP, stroke=3)
            pin(self, pr2, uid, run_time=0.3, anim=Create(uid))
            pin(self, pr2, beside(differ_tag(), t, pr2, buff=0.4), run_time=0.4)

        # ========================================================== 3 · step 3: ls -la /secrets
        # The README's numbered list has 3 steps (--help is its 3.); the tracker (and SAY) count the
        # :69 tip as step 3, so its caption says so in GREY and keeps --help tied to the README's 3.
        readme_no = {3: " · README tip", 4: " · README's step 3"}

        def _cap(k, _tr=tr):
            s = f"step {k} of {len(_tr.steps)}: {_tr.steps[k - 1]}"
            suf = readme_no.get(k, "")
            c = label(s + suf, _tr.size, _tr.hi_color, t2c={suf.strip(): S.GREY} if suf else None)
            return c.next_to(_tr.dots, RIGHT, buff=0.25)
        plain_caption, tr._caption = tr._caption, _cap
        c69 = readme_chip("README.md · line 69 · a Prerequisites tip, run inside the container")
        place(c69, right=6.4, cy=(t.box.get_top()[1] + 2.9) / 2)
        with self.voiceover(SAY[3]) as vo:
            self.play(tr.goto(3), FadeIn(c69, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("ls dash la")
            lsl = type_cmd(self, t, LS.cmd, 0.6)
            pin(self, lsl, beside(your_turn(), t, lsl), run_time=0.4)
            out3 = show(self, t, LS, (2, 4), run_time=0.5)
            vo.wait_until("With a key")
            t._make_room(self, 1)
            ghost = VGroup(note("with a key:"), ghost_file(KEY_FILE)).arrange(RIGHT, buff=0.2)
            slot = t._slot(len(t.lines))
            place(ghost, left=slot[0], cy=slot[1] - t.pitch / 2)
            gbox = box(ghost.width + 0.3, t.pitch - 0.04, S.GREY, dashed=True, radius=0.08, fill_opacity=0)
            gbox.move_to(ghost)
            ghost_row = VGroup(gbox, ghost)
            self.play(FadeIn(ghost_row, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Ours shows only")
            dot = out3[1]
            self.play(flash(glyph_range(dot, len(dot.text) - 1), TURN, 1.6), run_time=0.7)

        # ========================================================== 4 · step 4: python cli.py --help; ▶
        cap4 = note("no key needed yet: the clients look for credentials on their first call")
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(c69, ghost_row)), tr.goto(4), run_time=0.5)
            resize(self, t, 12, run_time=0.5)
            place(cap4, left=-1.6, cy=TOPCHIP_Y)
            if cap4.get_right()[0] > 6.45:
                place(cap4, right=6.45)
            hl = type_cmd(self, t, HELP.cmd, 0.6)
            pin(self, hl, beside(your_turn(), t, hl), run_time=0.4)
            out4 = show(self, t, HELP, (2, 10), run_time=0.7)
            vo.wait_until("Three flags")
            for n, flag in ((8, "--generate"), (9, "--prepare"), (10, "--upload")):
                row = out4[n - 2]
                self.play(substring(row, flag).animate.set_color(TURN), run_time=0.25)
                self.play(flash(substring(row, flag), TURN, 1.15), run_time=0.45)
            vo.wait_until("It works without a key")
            self.play(FadeIn(cap4, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("because the code only looks")
            self.play(flash(cap4, TURN, 1.04), run_time=0.8)
            vo.wait_until("Pause")
            pr4 = bare_prompt(self, t)
            self.play(flash(glyph_range(pr4, 0, len(P_CTR_DC)), TURN, 1.1), run_time=0.8)
        self.wait(2)                                    # ▶ beat: hold the frame

        # ========================================================== 5 · two traps from a second terminal
        t2 = term(P_DC, rows=8, title=SECOND, top=2.78)
        ft = frame_tags(t2, extra_tag())
        y_tr = [t2.box.get_bottom()[1] - 0.45, t2.box.get_bottom()[1] - 1.15, t2.box.get_bottom()[1] - 1.85]
        st1 = stamp("Debian · Ubuntu · WSL: sh is dash", ERR, angle=0.0)
        fx1 = fix_chip("bash docker-shell.sh", font=MONO)
        mac = note("macOS: sh works")
        trap1 = VGroup(st1, fx1, mac).arrange(RIGHT, buff=0.35)
        place(trap1, left=-6.3, cy=y_tr[0])
        st2 = stamp("run it from inside the folder", ERR, angle=0.0)
        fx2 = fix_chip("cd into the folder first · README.md:68")
        trap2 = VGroup(st2, fx2).arrange(RIGHT, buff=0.35)
        place(trap2, left=-6.3, cy=y_tr[1])
        conflict = mixed_chip(["a second", "`sh docker-shell.sh`", "while one runs →", "`Conflict.`",
                               "· use the laptop shell, or", "`exit`", "first"], ERR)
        place(conflict, cx=0, cy=y_tr[2])
        for m in (trap1, trap2, conflict):
            assert m.get_right()[0] < 6.5 and m.get_bottom()[1] > -3.58, (m.get_right(), m.get_bottom())
        with self.voiceover(SAY[5]) as vo:
            # the first terminal steps aside (it comes back at the end, still at the container prompt)
            tr._caption = plain_caption          # " · README's step 3" leaves before " · extra" comes
            self.play(FadeOut(cap4), FadeOut(t, shift=DOWN * 0.2), tr.goto(4), run_time=0.4)
            self.play(FadeIn(t2, shift=DOWN * 0.3), FadeIn(ft), caption_extra(tr, True), run_time=0.6)
            bare_prompt(self, t2)
            vo.wait_until("On Debian")
            type_cmd(self, t2, DASH.cmd, 0.6)
            e1 = show(self, t2, DASH, 2, default=ERR, run_time=0.4)
            vo.wait_until("sh is dash")
            self.play(FadeIn(st1, scale=1.15), run_time=0.4)
            vo.wait_until("which has no source")
            self.play(flash(substring(e1[0], "source: not found"), ERR, 1.08), run_time=0.6)
            vo.wait_until("run bash docker-shell.sh")
            self.play(FadeIn(fx1, shift=UP * 0.1), FadeIn(mac), run_time=0.5)
            vo.wait_until("And from the repository root")
            bare_prompt(self, t2)
            type_cmd(self, t2, CD_UP, 0.3)
            cd_prompt(self, t2, P_REPO, run_time=0.5)
            type_cmd(self, t2, WRONG.cmd, 0.6)
            show(self, t2, WRONG, 2, wrap=True, default=ERR, run_time=0.4)
            vo.wait_until("the script cannot find")
            self.play(FadeIn(st2, scale=1.15), run_time=0.4)
            vo.wait_until("cd into the folder first")
            self.play(FadeIn(fx2, shift=UP * 0.1), run_time=0.4)
            bare_prompt(self, t2)
            type_cmd(self, t2, CD_DC, 0.4)
            cd_prompt(self, t2, P_DC, run_time=0.5)
            self.play(FadeIn(conflict, shift=UP * 0.1), run_time=0.5)
        self.wait(0.8)

        # ========================================================== 6 · docker images: what the 1.64 GB holds
        blk_top, blk_bot = t2.box.get_bottom()[1] - 0.15, -3.5
        frame6 = tinted_box(12.8, blk_top - blk_bot, CTR, 0.05)
        place(frame6, cx=0, top=blk_top)
        title6 = VGroup(mono("llm-dataset-creator", CAPTION, CTR), label("image", CAPTION, S.GREY))
        title6.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        place(title6, left=frame6.get_left()[0] + 0.25, cy=frame6.get_center()[1])
        x0, x1 = title6.get_right()[0] + 0.35, frame6.get_right()[0] - 0.2
        sw = x1 - x0
        # layers, bottom to top in Dockerfile order: base image, /.venv (uv sync), /app (the code)
        base = tinted_box(sw, 0.4, SYSTEM, 0.18, stroke=2.5)
        base_t = mono("python:3.12-slim-bookworm", CAPTION, SYSTEM)
        venv = tinted_box(sw, 1.12, VENV, 0.14, stroke=2.5)
        app = tinted_box(sw, 0.34, CTR, 0.14, stroke=2.5)
        app_t = mono("/app", CAPTION, CTR)
        VGroup(app, venv, base).arrange(DOWN, buff=0.04)
        stack = VGroup(app, venv, base)
        place(stack, left=x0, cy=frame6.get_center()[1])
        place(base_t, left=x0 + 0.25, cy=base.get_center()[1])
        base_n = note("base image").next_to(base_t, RIGHT, buff=0.3)
        place(app_t, left=x0 + 0.25, cy=app.get_center()[1])
        app_n = note("your code").next_to(app_t, RIGHT, buff=0.3)
        v_t = mono("/.venv", CAPTION, VENV)
        v_c = chip("133 packages · 587 MB", VENV, size=CAPTION)
        row_a = VGroup(v_t, v_c).arrange(RIGHT, buff=0.3)
        dch = VGroup(*[concept_box(n, h=0.4) for n in ("chromadb", "langchain")]).arrange(RIGHT, buff=0.2)
        e6 = erratum_tag("never imported here")
        row_b = VGroup(dch, e6).arrange(RIGHT, buff=0.3)
        place(row_a, left=x0 + 0.25, cy=venv.get_center()[1] + 0.26)
        place(row_b, left=x0 + 0.25, cy=venv.get_center()[1] - 0.27)
        for m in (row_a, row_b, base_n, app_n):
            assert m.get_right()[0] < x1 - 0.1, m.get_right()
        assert frame6.get_bottom()[1] >= -3.56 and stack.get_top()[1] < blk_top - 0.05, (stack.height, blk_top)
        assert row_a.get_top()[1] < venv.get_top()[1] - 0.04 and row_b.get_bottom()[1] > venv.get_bottom()[1] + 0.04
        with self.voiceover(SAY[6]) as vo:
            # the two narrated traps leave; the (unnarrated) Conflict card stays a little longer to be read
            self.play(FadeOut(VGroup(trap1, trap2)), conflict.animate.move_to([0, y_tr[0], 0]), run_time=0.5)
            vo.wait_until("docker images")
            type_cmd(self, t2, IMG.cmd, 0.5)
            out6 = t2.print(self, [IMG.cut(2, "DISK USAGE"), IMG.cut(3, "1.64GB")], run_time=0.4)
            gb = substring(out6[1], "1.64GB")
            self.play(gb.animate.set_color(TURN), run_time=0.3)
            self.play(flash(gb, TURN, 1.2), run_time=0.5)
            self.play(FadeOut(conflict), run_time=0.3)
            self.play(FadeIn(frame6), FadeIn(title6), run_time=0.4)
            vo.wait_until("The lockfile installs")
            self.play(FadeIn(base), FadeIn(base_t), FadeIn(base_n), run_time=0.4)
            self.play(FadeIn(venv, shift=DOWN * 0.15), FadeIn(row_a), run_time=0.5)
            self.play(FadeIn(app, shift=DOWN * 0.15), FadeIn(app_t), FadeIn(app_n), run_time=0.4)
            vo.wait_until("among them")
            self.play(FadeIn(dch, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("which this code never imports")
            self.play(FadeIn(e6, shift=LEFT * 0.1), run_time=0.4)
            self.play(flash(e6.text, TURN, 1.05), run_time=0.6)
        self.wait(0.8)
        block = VGroup(frame6, title6, stack, base_t, base_n, app_t, app_n, row_a, row_b)
        self.play(FadeOut(t2, shift=UP * 0.4), FadeOut(ft, shift=UP * 0.4), FadeOut(block),
                  caption_extra(tr, False), run_time=0.7)
        self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(VGroup(tr, t)), run_time=0.7)
        self.wait(0.3)
