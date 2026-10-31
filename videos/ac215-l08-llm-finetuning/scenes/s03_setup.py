"""S03 · A key next to the repo (README "Prerequisites": the clone, the service account, the secrets
folder; env.dev as an extra step 4). Lecture: none (no lecture tag).

Beats (script.md "## S03", one voiceover block each):
 0  TRACKER Prereq 1 · extra. The house terminal (6 rows, `laptop`, prompt ~/AC215). Top band:
    README chip README.md · line 33 "Have Docker installed". An extra card "is Docker running"
    above the terminal -> laptop/00 line 4, GREY tag "at the time of recording" beside the card.
    The top chip becomes the GREY chip "README.md · line 34 only links the repository";
    `git clone https://github.com/dlops-io/llm-finetuning.git` (extra; folds under the prompt) ->
    laptop/01 line 2 (the extra tag sits on that output row: the folded command row is full).
    GREY caption "your prompt shows your own user and machine" beside the prompt row, whose
    user@host flashes.
 1  `cd llm-finetuning` (extra) -> no output. The extra card becomes "which commit am I on";
    `git log -1 --format="%h %H%n%cd %s" --date=iso` (the half of laptop/02's command that prints
    the shown lines; QA 03:18) -> laptop/02 line 2 cut after "44ef6f0", line 3; GREY tag "or newer",
    a short hold. The card leaves, the terminal grows to 12 rows keeping the commit lines: `ls -a; ls -a dataset-creator gemini-finetuner` (extra)
    -> laptop/03 lines 6–11 (7 `autotrain-runner` dim GREY), 12, 15–20 folded, 22, 25–30 folded
    (10 rows). dataset-creator and gemini-finetuner underline YELLOW as named; GREY "6 files" tags
    on the two folder headers; on "autotrain" the GREY tag "not part of the README".
 2  TRACKER Prereq 2. The terminal shrinks to the 3-row strip. Above it a schematic console
    (browser frame, tag illustration, no logo): "Create service account", the name field types
    llm-service-account; under "Grant this service account access to project" two BLUE role chips
    drop in, Storage Admin and Agent Platform User (GREY sub-label "formerly Vertex AI User ·
    roles/aiplatform.user"). The page turns to the account: tabs DETAILS / PERMISSIONS / KEYS,
    KEYS lights YELLOW; ADD KEY › Create new key › JSON lights in turn; a GOLD key glyph drops out
    of the form into a GREY "Downloads" folder at right. GREY chip "the same account as L05:
    reuse it" last.
 3  TRACKER Prereq 3. The console fades; the strip clears and grows to 8 rows: `cd ..` (extra) ->
    prompt ~/AC215; `mkdir secrets` -> (no output); `ls -la; ls -la secrets` (extra) -> laptop/06
    lines 2, 5–6, 7–8; the names llm-finetuning and secrets get GREY boxes. Above: GREY chip "move
    the key in · name it exactly llm-service-account.json", then the RED warning chip "not
    llm-service-account.json.json (hidden extensions · README.md:67)". Beside the secrets
    listing's "total 0": a GREY dashed key outline + "ours: empty", which pulses on "Watch".
 4  The chips leave; the terminal shrinks to the strip (the secrets listing stays). V2's laptop
    above it: the GREY laptop ~/AC215/ with two folders side by side, llm-finetuning/
    (dataset-creator/, gemini-finetuner/, env.dev) and secrets/ (GREY dashed key outline). A RED
    "git" arrow from inside the clone runs at secrets/ and bounces off the clone's edge (GREY
    "never committed"). Excerpt chip env.dev · line 5 (excerpt) `SECRETS_DIR=$(pwd)/../../secrets/`;
    a PINK path walks from dataset-creator/ up two folders (".." , "../..") to ~/AC215/secrets/
    while `$(pwd)`, `/../..` and `/secrets/` light PINK in the chip; then the same from
    gemini-finetuner/.
 5  TRACKER Prereq 4 · extra. The picture and the strip leave (no terminal: see "Deviations").
    CODE(env.dev: 4–10) with lines 7, 8, 9 wrapped (12 rows), header tag `extra` + "implied by its
    comments". Lines 6 and 7 light YELLOW, their values underline, GREY note "the repo's
    defaults · change to yours" beside them (SHOW says "README's"; the README never names them);
    on "pass both into the containers" the two lines flash; then the GREY note on line 9 "line 9: its comment says change too · not passed to
    either container · optional".
 6  The panel fades. A GREY dashed card "not in the README, needed": `gcloud services enable …`
    and `gcloud storage buckets create gs://<your-bucket> --location=us-central1` (folded with
    " \\", shown, never typed), `<your-bucket>` in a YELLOW template chip; both end in
    `--project=<your-project>` (YELLOW chips; QA 04:39); GREY caption "bucket names are global ·
    cheese-dataset is the course's" and under it a GREY note: the gcloud CLI, logged in, or the
    console pages. On "Pause here" the card gives way to the
    static GREY your-turn card (▶ your turn), its last line GOLD "a bucket: storage billing,
    cents". Hold 2 s; fade to an empty frame.

Deviations from SHOW (reported to the coordinator):
 - beat 1: the script's fold of laptop/03 lines 15–20 (all six names, two spaces apart) is 82
   characters, wider than a 65-character row; the row shows "Dockerfile  cli.py  …  docker-shell.sh
   pyproject.toml  uv.lock" (their own text, Capture.fold-checked) and a GREY "6 files" tag on each
   folder header says how many there are.
 - beat 5: CODE(env.dev: 4–10) needs 12 rows (lines 7–9 are 71–114 characters), too tall above a
   3-row strip, and `cat env.dev` would run in ~/AC215 after the `cd ..` of beat 3 (no env.dev
   there). The panel takes the frame without a strip and `cat env.dev` is not typed.
 - beat 4: V2's Stage draws the laptop as a vertical tree; SHOW asks for the two folders side by
   side with a clone edge for git to bounce off, so this beat draws its own laptop (same colours).
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
    LaggedStart,
    Line,
    RoundedRectangle,
    ShowIncreasingSubsets,
    Text,
    VGroup,
    VMobject,
    linear,
)

from common import *  # noqa: F401,F403
from common import _drop_bare  # the bare prompt gives way to an extra card's output
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ captures (file line numbers)
ENV = capture("laptop/00")                       # line 4: Docker Engine 29.8.2 …
CLONE = capture("laptop/01")
assert CLONE.cmd == "git clone https://github.com/dlops-io/llm-finetuning.git", CLONE.cmd
GIT = capture("laptop/02")
GIT_LOG = 'git log -1 --format="%h %H%n%cd %s" --date=iso'   # typed: the part of GIT.cmd behind lines 2-3
assert GIT.cmd == GIT_LOG + "; git branch -a", GIT.cmd
LS = capture("laptop/03")
assert LS.cmd == "ls -a; ls -a dataset-creator gemini-finetuner", LS.cmd
MKDIR = capture("laptop/05")
assert MKDIR.cmd == "mkdir secrets" and all(not s for s in MKDIR.lines), MKDIR.lines
LSW = capture("laptop/06")
assert LSW.cmd == "ls -la; ls -la secrets", LSW.cmd

SIX = "Dockerfile  cli.py  …  docker-shell.sh  pyproject.toml  uv.lock"   # 63 characters
FOLD_DC = LS.fold(15, 20, SIX)
FOLD_GF = LS.fold(25, 30, SIX)
assert len(SIX) <= 65

R5 = source_line("env.dev", 5)
SECRETS_SUB = "SECRETS_DIR=$(pwd)/../../secrets/"
assert SECRETS_SUB in R5

GCLOUD_API = "gcloud services enable aiplatform.googleapis.com storage.googleapis.com --project=<your-project>"
GCLOUD_BUCKET = "gcloud storage buckets create gs://<your-bucket> --location=us-central1 --project=<your-project>"
MV_TEMPLATE = "mv ~/Downloads/<downloaded-key>.json secrets/llm-service-account.json"

SAFE = 6.5


# ------------------------------------------------------------------ small helpers
def text_glyphs(t: Text, s: str, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of `sub` in a Text built from string `s` (Text drops whitespace)."""
    i = -1
    for _ in range(occurrence + 1):
        i = s.find(sub, i + 1)
        if i < 0:
            raise ValueError(f"{sub!r} not in {s!r}")
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


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


def inside(m):
    assert m.get_left()[0] >= -6.6 and m.get_right()[0] <= 6.6, (m.get_left(), m.get_right())
    assert m.get_bottom()[1] >= -3.6 and m.get_top()[1] <= 3.6, (m.get_bottom(), m.get_top())
    return m


def pin_beside(scene, t, line, mob, buff=0.3, run_time=0.4):
    beside(mob, t, line, buff=buff)
    return pin(scene, line, mob, run_time=run_time)


def folder_box(title: str, w: float, h: float, color=LAPTOP, dashed: bool = False) -> VGroup:
    fr = box(w, h, color, fill_opacity=0.05, radius=0.14, stroke=2.5, dashed=dashed)
    gl = folder_glyph(0.24, color)
    tt = mono(title, CAPTION, color)
    head = VGroup(gl, tt).arrange(RIGHT, buff=0.12)
    head.move_to(fr.get_corner(UP + LEFT), aligned_edge=UP + LEFT).shift(np.array([0.2, -0.16, 0]))
    g = VGroup(fr, head)
    g.frame, g.head, g.glyph, g.title = fr, head, gl, tt
    return g


def poly_arrow(points, color=LOOKUP, stroke=4) -> VGroup:
    """A PINK polyline ending in a small arrow head (a path that walks)."""
    pts = [np.array(p, dtype=float) for p in points]
    path = VMobject(stroke_color=color, stroke_width=stroke)
    path.set_points_as_corners(pts[:-1] + [pts[-1]])
    head = Arrow(pts[-2], pts[-1], buff=0, color=color, stroke_width=stroke,
                 max_tip_length_to_length_ratio=0.9, tip_length=0.2)
    tip = head.tip
    g = VGroup(path, tip)
    g.path, g.tip = path, tip
    return g


def dashed_card(rows, header: str, color=S.GREY, width=None) -> VGroup:
    body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    w = max(width or 0, body.width + 0.6)
    fr = box(w, body.height + 0.5, color, dashed=True, radius=0.14)
    bg = RoundedRectangle(width=w, height=body.height + 0.5, corner_radius=0.14, stroke_width=0) \
        .set_fill(S.BG, 0.95)
    bg.move_to(fr)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    hd = note(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
    g = VGroup(bg, fr, body, hd)
    g.frame, g.body, g.header = fr, body, hd
    return g


class KeyNextToRepo(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · workspace, Docker, the clone (extra)
        tr = tracker("Prereq", 1)
        t = term(P_WS, rows=6)
        c33 = top_chip("Have Docker installed", where="README.md · line 33")
        c34 = top_chip("README.md · line 34 only links the repository", color=S.GREY)
        ec0 = extra_card("is Docker running")
        place(ec0, left=-6.3, bottom=t.box.get_top()[1] + 0.3)
        rtag = recording_tag()
        place(rtag, left=ec0.frame.get_right()[0] + 0.3, cy=ec0.frame.get_center()[1])
        for m in (ec0, rtag, c33, c34):
            inside(m)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            self.play(caption_extra(tr, True), FadeIn(c33, shift=DOWN * 0.1), run_time=0.5)
            bp = bare_prompt(self, t)
            vo.wait_until("the AC215 folder")
            self.play(Indicate(substring(bp, "~/AC215"), color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("with Docker installed")
            _drop_bare(self, t)
            self.play(FadeIn(ec0, shift=DOWN * 0.1), run_time=0.4)
            o_env = show(self, t, ENV, 4, run_time=0.4)
            self.play(FadeIn(rtag, shift=LEFT * 0.1), run_time=0.35)
            self.play(Indicate(substring(o_env[0], "Docker Engine 29.8.2"), color=TURN, scale_factor=1.05),
                      run_time=0.6)
            vo.wait_until("The README only links")
            self.play(FadeOut(c33, shift=UP * 0.1), run_time=0.3)
            self.play(FadeIn(c34, shift=DOWN * 0.1), run_time=0.3)
            vo.wait_until("so cloning it")
            cl = type_cmd(self, t, CLONE.cmd, 1.2)
            o_cl = show(self, t, CLONE, 2, run_time=0.4)
            pin_beside(self, t, o_cl[0], extra_tag(), run_time=0.35)
            vo.wait_until("Your prompt shows")
            prow = cl.rows[0] if hasattr(cl, "rows") else cl
            ynote = note("your prompt shows your own user and machine")
            pin_beside(self, t, prow, ynote, buff=0.4, run_time=0.4)
            self.play(Indicate(substring(prow, "student@laptop"), color=TURN, scale_factor=1.1), run_time=0.7)

        # ========================================================== 1 · cd, the commit, the six files
        ec1 = extra_card("which commit am I on")
        place(ec1, left=-6.3, bottom=t.box.get_top()[1] + 0.3)
        inside(ec1)
        with self.voiceover(SAY[1]) as vo:
            cd = type_cmd(self, t, "cd llm-finetuning", 0.5)
            pin_beside(self, t, cd, extra_tag(), run_time=0.3)
            t.set_prompt(P_REPO)
            self.play(FadeOut(ec0, shift=UP * 0.1), FadeOut(rtag), FadeIn(ec1, shift=DOWN * 0.1), run_time=0.4)
            type_cmd(self, t, GIT_LOG, 0.5)          # the half of GIT.cmd that prints lines 2-3
            o_git = show(self, t, GIT, GIT.cut(2, "44ef6f0"), 3, run_time=0.4)
            vo.wait_until("yours may be newer")
            pin_beside(self, t, o_git[0], grey_tag("or newer"), run_time=0.35)
            self.wait(0.8)                           # the commit stays readable (QA 03:19)
            # no clear: the terminal grows with the commit lines kept; the ls output scrolls them off
            resize(self, t, 12, run_time=0.5,
                   extra=(FadeOut(ec1, shift=UP * 0.1), FadeOut(c34)))
            ls = type_cmd(self, t, LS.cmd, 0.9)
            pin_beside(self, t, ls, extra_tag(), run_time=0.3)
            vo.wait_until("Inside are two folders")
            out = show(self, t, LS, (6, 6), (LS.line(7), S.GREY), (8, 11), 12, FOLD_DC, 22, FOLD_GF,
                       run_time=0.8)
            assert len(out) == 10 and len(t.lines) == 12, (len(out), len(t.lines))
            r_dc, r_gf, r_auto = out[2], out[4], out[1]
            h_dc, h_gf, f_dc, f_gf = out[6], out[8], out[7], out[9]
            vo.wait_until("dataset-creator and")
            u_dc = under(substring(r_dc, "dataset-creator"))
            self.play(Create(u_dc), run_time=0.35)
            self.remove(u_dc)
            r_dc.add(u_dc)
            vo.wait_until("gemini-finetuner, each")
            u_gf = under(substring(r_gf, "gemini-finetuner"))
            self.play(Create(u_gf), run_time=0.35)
            self.remove(u_gf)
            r_gf.add(u_gf)
            vo.wait_until("each with the same six files")
            six_a, six_b = grey_tag("6 files"), grey_tag("6 files")
            beside(six_a, t, h_dc)
            beside(six_b, t, h_gf)
            self.play(FadeIn(six_a, shift=LEFT * 0.1), FadeIn(six_b, shift=LEFT * 0.1),
                      Indicate(f_dc, color=TURN, scale_factor=1.03),
                      Indicate(f_gf, color=TURN, scale_factor=1.03), run_time=0.7)
            for row, tg in ((h_dc, six_a), (h_gf, six_b)):
                self.remove(tg)
                row.add(tg)
            vo.wait_until("The autotrain folder")
            pin_beside(self, t, r_auto, grey_tag("not part of the README"), run_time=0.4)
            self.play(Indicate(substring(r_auto, "autotrain-runner"), color=S.GREY, scale_factor=1.06),
                      run_time=0.6)

        # ========================================================== 2 · step 2: service account + JSON key (console)
        win = browser_window("console › Service accounts", width=7.9, height=4.05)
        place(win, left=-6.4, top=2.75)
        ill = illustration_tag()
        place(ill, right=win.frame.get_right()[0], bottom=win.frame.get_top()[1] + 0.1)
        ct = win.content
        x0 = ct.get_left()[0] + 0.25
        # page 1: create the account, grant two roles
        p1_title = label("Create service account", LABEL, INK)
        place(p1_title, left=x0, top=ct.get_top()[1] - 0.1)
        f_lab = label("Service account name", CAPTION, S.GREY)
        place(f_lab, left=x0, top=p1_title.get_bottom()[1] - 0.35)
        f_box = RoundedRectangle(width=7.2 - f_lab.width - 0.3, height=0.44, corner_radius=0.06,
                                 stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(TERM_BG, 1)
        place(f_box, left=f_lab.get_right()[0] + 0.3, cy=f_lab.get_center()[1])
        name_val = mono("llm-service-account", CAPTION, INK)
        place(name_val, left=f_box.get_left()[0] + 0.15, cy=f_box.get_center()[1])
        form = VGroup(f_lab, f_box, name_val)
        grant = label("Grant this service account access to project", CAPTION, S.GREY)
        place(grant, left=x0, top=form.get_bottom()[1] - 0.3)
        roles_box = box(7.2, 1.25, S.GREY_DARK, fill_opacity=0.0, dashed=True, radius=0.1)
        place(roles_box, left=x0, top=grant.get_bottom()[1] - 0.14)
        r1 = chip("Storage Admin", CLOUD, size=CAPTION)
        r2 = chip("Agent Platform User", CLOUD, size=CAPTION)
        place(r1, left=roles_box.get_left()[0] + 0.25, top=roles_box.get_top()[1] - 0.16)
        place(r2, left=r1.get_right()[0] + 0.35, top=roles_box.get_top()[1] - 0.16)
        r2_sub = note("formerly Vertex AI User · roles/aiplatform.user")
        place(r2_sub, right=roles_box.get_right()[0] - 0.25, top=r2.get_bottom()[1] - 0.12)
        assert r2_sub.get_bottom()[1] > roles_box.get_bottom()[1] + 0.08 and r2_sub.get_left()[0] > r1.get_left()[0]
        page1 = VGroup(p1_title, form, grant, roles_box, r1, r2, r2_sub)
        # page 2: the account's KEYS tab, ADD KEY › Create new key › JSON
        p2_title = mono("llm-service-account", LABEL, INK)
        place(p2_title, left=x0, top=ct.get_top()[1] - 0.1)
        tabs = VGroup(*[label(s, CAPTION, S.GREY) for s in ("DETAILS", "PERMISSIONS", "KEYS")]) \
            .arrange(RIGHT, buff=0.6)
        place(tabs, left=x0, top=p2_title.get_bottom()[1] - 0.4)
        tab_line = Line([ct.get_left()[0] + 0.1, tabs.get_bottom()[1] - 0.12, 0],
                        [ct.get_right()[0] - 0.1, tabs.get_bottom()[1] - 0.12, 0], color=S.GREY_DARK, stroke_width=2)
        keys_ul = Line(tabs[2].get_corner(DOWN + LEFT) + DOWN * 0.12, tabs[2].get_corner(DOWN + RIGHT) + DOWN * 0.12,
                       color=TURN, stroke_width=5)
        menu = menu_path(["ADD KEY", "Create new key", "JSON"])
        place(menu, left=x0, top=tab_line.get_bottom()[1] - 0.45)
        page2 = VGroup(p2_title, tabs, tab_line, menu)
        # the Downloads folder at right; the reuse chip
        dl_glyph = folder_glyph(0.7, LAPTOP)
        dl_name = label("Downloads", CAPTION, LAPTOP)
        dl = VGroup(dl_glyph, dl_name).arrange(DOWN, buff=0.15)
        place(dl, cx=(win.frame.get_right()[0] + SAFE) / 2, cy=0.9)
        dl_cap = note("on your laptop")
        place(dl_cap, cx=dl.get_center()[0], top=dl.get_bottom()[1] - 0.08)
        reuse = chip("the same account as L05: reuse it", S.GREY, size=CAPTION)
        place(reuse, right=SAFE, top=dl_cap.get_bottom()[1] - 0.45)
        k_drop = key_glyph(0.34)
        for m in (win, ill, page1, page2, dl, dl_cap, reuse):
            inside(m)
        assert reuse.get_left()[0] > win.frame.get_right()[0] + 0.1, reuse.get_left()
        assert roles_box.get_bottom()[1] > win.frame.get_bottom()[1] + 0.15, roles_box.get_bottom()
        assert win.frame.get_bottom()[1] > STRIP_TOP + 0.08
        with self.voiceover(SAY[2]) as vo:
            self.play(tr.goto(2), run_time=0.5)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(win), FadeIn(ill), run_time=0.5)
            self.play(FadeIn(p1_title), FadeIn(VGroup(f_lab, f_box)), run_time=0.4)
            vo.wait_until("Create a service account")
            self.play(ShowIncreasingSubsets(name_val, rate_func=linear), run_time=0.9)
            vo.wait_until("with two roles")
            self.play(FadeIn(grant), Create(roles_box), run_time=0.5)
            vo.wait_until("Storage Admin")
            self.play(FadeIn(r1, shift=DOWN * 0.3), run_time=0.4)
            vo.wait_until("and Agent Platform User")
            self.play(FadeIn(r2, shift=DOWN * 0.3), run_time=0.4)
            vo.wait_until("formerly Vertex AI User")
            self.play(FadeIn(r2_sub, shift=UP * 0.05), run_time=0.4)
            vo.wait_until("Under keys")
            self.play(FadeOut(page1), run_time=0.25)
            self.play(FadeIn(p2_title), FadeIn(tabs), Create(tab_line), run_time=0.35)
            self.play(Create(keys_ul), tabs[2].animate.set_color(TURN), run_time=0.35)
            vo.wait_until("add a JSON key")
            self.play(FadeIn(menu), run_time=0.3)
            for i in range(3):
                self.play(menu.light(i), run_time=0.3)
            vo.wait_until("which downloads to your laptop")
            k_drop.next_to(menu.items[2], UP, buff=0.15)
            self.play(FadeIn(dl), FadeIn(dl_cap), FadeIn(k_drop, scale=0.6), run_time=0.4)
            self.play(k_drop.animate.move_to(dl_glyph.get_center() + UP * 0.05), run_time=0.8)
            vo.wait_until("If you kept the account")
            self.play(FadeIn(reuse, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 3 · step 3: the secrets folder, next to the clone
        MV_S = "move the key in · name it exactly llm-service-account.json"
        chip_mv = chip(MV_S, S.GREY, size=CAPTION)
        WARN_S = "not llm-service-account.json.json (hidden extensions · README.md:67)"
        chip_warn = chip(WARN_S, ERR, size=CAPTION)
        warn = VGroup(warning_sign(0.36, ERR), chip_warn).arrange(RIGHT, buff=0.15)
        with self.voiceover(SAY[3]) as vo:
            self.play(tr.goto(3), FadeOut(VGroup(win, ill, page2, keys_ul, dl, dl_cap, reuse, k_drop)),
                      run_time=0.5)
            t.clear(self, run_time=0.25)
            resize(self, t, 8, run_time=0.5)
            place(chip_mv, left=-6.3, cy=t.box.get_top()[1] + 1.35)
            place(warn, left=-6.3, cy=t.box.get_top()[1] + 0.6)
            inside(chip_mv)
            inside(warn)
            up = type_cmd(self, t, "cd ..", 0.3)
            pin_beside(self, t, up, extra_tag(), run_time=0.25)
            cd_prompt(self, t, P_WS, run_time=0.5)
            vo.wait_until("make a folder called secrets")
            type_cmd(self, t, MKDIR.cmd, 0.5)
            vo.wait_until("next to the repository")
            lw = type_cmd(self, t, LSW.cmd, 0.6)
            pin_beside(self, t, lw, extra_tag(), run_time=0.25)
            o_lw = show(self, t, LSW, 2, (5, 6), (7, 8), run_time=0.5)
            b_repo = col_box(o_lw[1], len(o_lw[1].text) - len("llm-finetuning"), len(o_lw[1].text), LAPTOP)
            b_sec = col_box(o_lw[2], len(o_lw[2].text) - len("secrets"), len(o_lw[2].text), LAPTOP)
            assert o_lw[1].text.endswith("llm-finetuning") and o_lw[2].text.endswith("secrets")
            self.play(Create(b_repo), Create(b_sec), run_time=0.5)
            o_lw[1].add(b_repo)
            o_lw[2].add(b_sec)
            vo.wait_until("Move the key in")
            self.play(FadeIn(chip_mv, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("name it exactly")
            self.play(Indicate(text_glyphs(chip_mv.text, MV_S, "llm-service-account.json"), color=TURN,
                               scale_factor=1.1), run_time=0.7)
            vo.wait_until("with hidden file extensions")
            self.play(FadeIn(warn, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("as dot json dot json")
            self.play(Indicate(text_glyphs(chip_warn.text, WARN_S, ".json.json"), color=ERR, scale_factor=1.15),
                      run_time=0.7)
            vo.wait_until("Ours stays empty")
            empty = VGroup(key_outline(0.3, S.GREY), note("ours: empty")).arrange(RIGHT, buff=0.2)
            pin_beside(self, t, o_lw[3], empty, buff=0.5, run_time=0.45)
            vo.wait_until("Watch what that does")
            self.play(Indicate(empty, color=S.GREY, scale_factor=1.15), run_time=0.8)

        # ========================================================== 4 · why next to it: git never sees it, ../.. finds it
        top_y, bot_y = 2.75, STRIP_TOP + 0.17
        ws = mono("~/AC215/", CAPTION + 2, LAPTOP)
        clone = folder_box("llm-finetuning/", 3.85, 2.55)
        sec = folder_box("secrets/", 2.0, 2.55)
        lap_w = 0.2 + clone.frame.width + 0.2 + sec.frame.width + 0.2
        lap = laptop_zone(w=lap_w, h=top_y - bot_y, caption="your laptop")
        place(lap, left=-6.4, top=top_y)
        place(ws, left=lap.frame.get_left()[0] + 0.25, top=top_y - 0.25)
        place(clone, left=lap.frame.get_left()[0] + 0.2, top=ws.get_bottom()[1] - 0.4)
        rows = VGroup(file_row("dataset-creator/", LAPTOP, LAPTOP), file_row("gemini-finetuner/", LAPTOP, LAPTOP),
                      file_row("env.dev", INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        place(rows, left=clone.frame.get_left()[0] + 0.42, top=clone.head.get_bottom()[1] - 0.3)
        place(sec, left=clone.frame.get_right()[0] + 0.2, top=clone.frame.get_top()[1])
        sec_key = key_outline(0.4, S.GREY)
        place(sec_key, cx=sec.frame.get_center()[0], cy=sec.frame.get_center()[1] - 0.05)
        sec_note = note("ours: empty")
        place(sec_note, cx=sec.frame.get_center()[0], top=sec_key.get_bottom()[1] - 0.18)
        laptop_pic = VGroup(lap, ws, clone, rows, sec, sec_key, sec_note)
        assert rows.get_right()[0] < clone.frame.get_right()[0] - 0.05, rows.get_right()
        assert sec.head.get_right()[0] < sec.frame.get_right()[0] - 0.05
        assert lap.frame.get_right()[0] < 0.1, lap.frame.get_right()
        # git: from inside the clone at secrets/, bounces off the clone's right edge
        edge_x = clone.frame.get_right()[0]
        gy = rows[2].get_center()[1]
        git_lab = label("git", CAPTION, ERR)
        place(git_lab, left=rows[2].get_right()[0] + 0.35, cy=gy)
        g_arrow = Arrow([git_lab.get_right()[0] + 0.1, gy, 0], [edge_x - 0.04, gy, 0], buff=0, color=ERR,
                        stroke_width=5, max_tip_length_to_length_ratio=0.25)
        never = note("never committed")
        place(never, right=edge_x - 0.15, top=gy - 0.26)
        assert never.get_bottom()[1] > clone.frame.get_bottom()[1] + 0.05, (never.get_bottom(), clone.frame.get_bottom())
        assert lap.caption.get_top()[1] < clone.frame.get_bottom()[1] - 0.03, lap.caption.get_top()
        # env.dev line 5 and the walk ../.. to secrets/
        xc = excerpt_chip(SECRETS_SUB, "env.dev · line 5 (excerpt)", line=R5)
        place(xc, right=SAFE, top=2.9)
        assert xc.get_left()[0] > lap.frame.get_right()[0] + 0.05, xc.get_left()
        s_pwd = text_glyphs(xc.text, SECRETS_SUB, "$(pwd)")
        s_up = text_glyphs(xc.text, SECRETS_SUB, "/../..")
        s_sec = text_glyphs(xc.text, SECRETS_SUB, "/secrets/")
        why1 = VGroup(mono("$(pwd)", CAPTION, LOOKUP), note("= where the script runs")).arrange(RIGHT, buff=0.15)
        place(why1, left=lap.frame.get_right()[0] + 0.55, top=xc.chip.get_bottom()[1] - 0.55)
        why2 = VGroup(mono("../..", CAPTION, LOOKUP), note("= two folders up")).arrange(RIGHT, buff=0.15)
        place(why2, left=why1.get_left()[0], top=why1.get_bottom()[1] - 0.35)
        why3 = VGroup(note("both folders reach"), mono("~/AC215/secrets/", CAPTION, LAPTOP)).arrange(RIGHT, buff=0.15)
        place(why3, left=why1.get_left()[0], top=why2.get_bottom()[1] - 0.35)
        for m in (laptop_pic, xc, why1, why2, why3, never):
            inside(m)
        assert xc.get_right()[0] <= SAFE + 0.05 and why3.get_right()[0] <= SAFE + 0.05, (xc.get_right(), why3.get_right())

        y_clone = clone.head.get_center()[1]
        y_ws = ws.get_center()[1]
        up1 = mono("..", CAPTION, LOOKUP)
        place(up1, left=clone.title.get_right()[0] + 0.15, cy=y_clone)
        assert up1.get_right()[0] < clone.frame.get_right()[0] - 0.05, up1.get_right()
        up2 = mono("../..", CAPTION, LOOKUP)
        place(up2, left=ws.get_right()[0] + 0.3, cy=y_ws)

        def walk(row, dx):
            """dataset-creator/ (or gemini-finetuner/) -> .. (llm-finetuning/) -> ../.. (~/AC215/) -> secrets/:
            two straight hops up one lane at the clone's left margin, then across to secrets/."""
            a = row.glyph.get_left() + LEFT * 0.06
            x = clone.frame.get_left()[0] + 0.17 + dx
            leg1 = poly_arrow([a, [x, a[1], 0], [x, clone.head.get_bottom()[1] - 0.05, 0]], stroke=3.5)
            leg2 = poly_arrow([[x, clone.head.get_top()[1] + 0.05, 0], [x, ws.get_bottom()[1] - 0.05, 0]],
                              stroke=3.5)
            tx = sec.glyph.get_center()[0] + dx
            leg3 = poly_arrow([[up2.get_right()[0] + 0.12, y_ws + dx * 0.0, 0], [tx, y_ws, 0],
                               [tx, sec.glyph.get_top()[1] + 0.06, 0]], stroke=3.5)
            return leg1, leg2, leg3

        w_dc = walk(rows[0], 0.0)
        w_gf = walk(rows[1], 0.1)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(chip_mv, warn)), run_time=0.3)
            resize(self, t, 3, run_time=0.5)
            self.play(FadeIn(lap), FadeIn(ws), run_time=0.4)
            self.play(LaggedStart(FadeIn(clone), FadeIn(rows), FadeIn(VGroup(sec, sec_key, sec_note)),
                                  lag_ratio=0.3), run_time=0.8)
            vo.wait_until("A key outside the clone")
            self.play(FadeIn(git_lab), run_time=0.25)
            self.play(GrowArrow(g_arrow), run_time=0.5)
            self.play(Indicate(clone.frame, color=ERR, scale_factor=1.02),
                      g_arrow.animate.put_start_and_end_on(g_arrow.get_start(), g_arrow.get_end() + LEFT * 0.45),
                      run_time=0.4)
            self.play(g_arrow.animate.put_start_and_end_on(g_arrow.get_start(), [edge_x - 0.04, gy, 0]), run_time=0.25)
            self.play(FadeIn(never, shift=UP * 0.05), run_time=0.3)
            vo.wait_until("The env.dev file")
            self.play(FadeIn(xc, shift=LEFT * 0.1), Indicate(rows[2], color=TURN, scale_factor=1.08), run_time=0.5)
            vo.wait_until("looks two folders up")
            self.play(FadeOut(VGroup(git_lab, g_arrow, never)), s_pwd.animate.set_color(LOOKUP),
                      FadeIn(why1), Indicate(rows[0], color=LOOKUP, scale_factor=1.08), run_time=0.5)
            self.play(Create(w_dc[0]), run_time=0.5)
            self.play(FadeIn(up1, shift=LEFT * 0.1), Indicate(clone.title, color=LOOKUP, scale_factor=1.08),
                      run_time=0.4)
            self.play(Create(w_dc[1]), s_up.animate.set_color(LOOKUP), FadeIn(why2), run_time=0.5)
            self.play(FadeIn(up2, shift=LEFT * 0.1), Indicate(ws, color=LOOKUP, scale_factor=1.08), run_time=0.4)
            self.play(Create(w_dc[2]), s_sec.animate.set_color(LOOKUP), run_time=0.5)
            self.play(Indicate(sec_key, color=LOOKUP, scale_factor=1.2), run_time=0.4)
            vo.wait_until("so both container folders")
            self.play(Create(w_gf[0]), Indicate(rows[1], color=LOOKUP, scale_factor=1.08), run_time=0.5)
            self.play(Create(w_gf[1]), run_time=0.4)
            self.play(Create(w_gf[2]), FadeIn(why3), run_time=0.4)
            self.play(Indicate(sec_key, color=LOOKUP, scale_factor=1.2), run_time=0.4)
        pic4 = VGroup(laptop_pic, xc, why1, why2, why3, up1, up2, *w_dc, *w_gf)

        # ========================================================== 5 · extra step 4: env.dev lines 6 and 7
        wrap = {6: ["# CHANGE"], 7: ["# CHANGE"], 9: ['"llm-service', "# CHANGE"]}
        pan = src_panel("env.dev", 4, 10, wrap=wrap, size=20)
        place(pan, left=-6.3, top=2.2)
        ptag = VGroup(extra_tag(), note("implied by its comments")).arrange(RIGHT, buff=0.15)
        place(ptag, right=pan.get_right()[0], bottom=pan.get_top()[1] + 0.1)
        bar6, bar7 = pan.bar(6), pan.bar(7)
        v6 = pan.span(6, '"ac215-project"')
        v7 = pan.span(7, '"cheese-dataset"')
        r7a, r7b = pan.rows_of(7)
        row7a = pan.code.code_lines[r7a]
        row7b = pan.code.code_lines[r7b]
        n67 = tag("the repo's defaults · change to yours", S.GREY, size=CAPTION)
        r6b = pan.code.code_lines[pan.rows_of(6)[1]]
        place(n67, left=v7.get_right()[0] + 0.15, cy=r6b.get_center()[1])
        assert n67.get_right()[0] < pan.get_right()[0] - 0.1, n67.get_right()
        n9 = grey_tag("line 9: its comment says change too · not passed to either container · optional")
        place(n9, left=pan.get_left()[0] + 0.2, top=pan.get_bottom()[1] - 0.25)
        bar9 = pan.bar(9, S.GREY, 0.12)
        for m in (pan, ptag, n67, n9):
            inside(m)
        assert ptag.get_left()[0] > -1.0, ptag.get_left()          # clear of the tracker
        with self.voiceover(SAY[5]) as vo:
            self.play(tr.goto(4), FadeOut(pic4), FadeOut(t), run_time=0.5)
            self.play(caption_extra(tr, True), FadeIn(pan, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("implied by the file")
            self.play(FadeIn(ptag, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("set your own project ID")
            self.play(FadeIn(bar6), v6.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("and bucket name")
            self.play(FadeIn(bar7), v7.animate.set_color(TURN), run_time=0.5)
            self.play(FadeIn(n67, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("The scripts pass both")
            self.play(Indicate(v6, color=TURN, scale_factor=1.1), Indicate(v7, color=TURN, scale_factor=1.1),
                      run_time=0.7)
            self.play(FadeIn(bar9), FadeIn(n9, shift=LEFT * 0.1), run_time=0.5)

        # ========================================================== 6 · APIs + a bucket of your own; your turn
        a2 = "    storage.googleapis.com --project=<your-project>"
        api_rows = [mono("gcloud services enable aiplatform.googleapis.com \\", CAPTION, INK),
                    mono(a2, CAPTION, INK)]
        b1 = "gcloud storage buckets create gs://<your-bucket> \\"
        b2 = "    --location=us-central1 --project=<your-project>"
        bkt_rows = [mono(b1, CAPTION, INK), mono(b2, CAPTION, INK)]
        cw = cell_width(CAPTION)
        rows6 = VGroup(VGroup(*api_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
                       VGroup(*bkt_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        api_rows[1].shift(RIGHT * 4 * cw)              # Text drops the leading spaces of a continuation row
        bkt_rows[1].shift(RIGHT * 4 * cw)
        card6 = dashed_card(list(rows6), "not in the README, needed")
        place(card6, cx=0, cy=0.9)
        yb = text_glyphs(bkt_rows[0], b1, "<your-bucket>")
        yb.set_color(TURN)
        yb_chip = RoundedRectangle(width=yb.width + 0.05, height=yb.height + 0.18, corner_radius=0.08,
                                   stroke_color=TURN, stroke_width=2.5).move_to(yb)
        card6.add(yb_chip)
        # <your-project> (QA 04:39: without a default project both commands fail): YELLOW template chips
        yp_chips = VGroup()
        for row, src in ((api_rows[1], a2), (bkt_rows[1], b2)):
            yp = text_glyphs(row, src, "<your-project>").set_color(TURN)
            yp_chips.add(RoundedRectangle(width=yp.width + 0.05, height=yp.height + 0.18, corner_radius=0.08,
                                          stroke_color=TURN, stroke_width=2.5).move_to(yp))
        card6.body[0].add(yp_chips[0])
        card6.body[1].add(yp_chips[1])
        api_ai = text_glyphs(api_rows[0], "gcloud services enable aiplatform.googleapis.com \\", "aiplatform.googleapis.com")
        api_st = api_rows[1]
        cap6 = note("bucket names are global · cheese-dataset is the course's")
        place(cap6, cx=0, top=card6.frame.get_bottom()[1] - 0.3)
        need6 = VGroup(note("needs the gcloud CLI, logged in (gcloud auth login)"),
                       note("or in the console: APIs & Services › Enable APIs · Cloud Storage › Create bucket")) \
            .arrange(DOWN, buff=0.1)
        place(need6, cx=0, top=cap6.get_bottom()[1] - 0.3)
        mv_cmd = "mv ~/Downloads/<downloaded-key>.json \\\n    secrets/llm-service-account.json"
        tc = turn_card([
            (CLONE.cmd, "extra"),
            Prose("service account (two roles) + JSON key, in the console"),
            MKDIR.cmd,
            (mv_cmd, "a template"),
            Prose("env.dev lines 6–7: your project ID and bucket"),
            Prose("enable the two APIs · create your own bucket"),
            (Prose("a bucket: storage billing, cents"), COST),
        ])
        place(tc, cx=0, cy=-0.25)
        mv_row = tc.rows[3][0]
        tc.rows[3][1].shift(RIGHT * 4 * cw)            # the continuation row and its "a template" note
        tc.rows[3][2].shift(RIGHT * 4 * cw)
        assert tc.rows[3][2].get_right()[0] < tc.frame.get_right()[0] - 0.2
        dk = text_glyphs(mv_row, "mv ~/Downloads/<downloaded-key>.json \\", "<downloaded-key>").set_color(TURN)
        tc.add(RoundedRectangle(width=dk.width + 0.05, height=dk.height + 0.08, corner_radius=0.08,
                                stroke_color=TURN, stroke_width=2.5).move_to(dk))
        for m in (card6, cap6, need6, tc):
            inside(m)
        assert tc.get_top()[1] < 2.9, tc.get_top()
        # the full commands of the card, as README-less extras (checked against the strings above)
        assert GCLOUD_API.split() == ("gcloud services enable aiplatform.googleapis.com " + a2).split()
        assert GCLOUD_BUCKET.split() == (b1.replace("\\", "") + b2).split()
        assert MV_TEMPLATE.split() == mv_cmd.replace("\\", "").split()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(pan, ptag, bar6, bar7, n67, bar9, n9)), run_time=0.4)
            self.play(FadeIn(card6[0]), FadeIn(card6.header), Create(card6.frame), FadeIn(card6.body[0]),
                      run_time=0.6)
            vo.wait_until("the Agent Platform")
            self.play(Indicate(api_ai, color=CLOUD, scale_factor=1.08), run_time=0.6)
            vo.wait_until("and Storage APIs")
            self.play(Indicate(api_st, color=CLOUD, scale_factor=1.08), run_time=0.6)
            vo.wait_until("and a bucket of your own")
            self.play(FadeIn(card6.body[1]), run_time=0.4)
            self.play(Create(yb_chip), run_time=0.35)
            self.play(FadeIn(need6, shift=UP * 0.05), run_time=0.4)
            vo.wait_until("Bucket names are global")
            self.play(FadeIn(cap6, shift=UP * 0.05), run_time=0.4)
            vo.wait_until("and cheese-dataset belongs")
            self.play(Indicate(cap6, color=S.GREY, scale_factor=1.05), Indicate(yb, color=TURN, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("Pause here")
            self.play(FadeOut(VGroup(card6, cap6, need6)), run_time=0.3)
            self.play(FadeIn(tc, shift=UP * 0.1), run_time=0.4)
        self.wait(2)
        self.play(FadeOut(VGroup(tc, tr)), run_time=0.6)
        self.wait(0.3)
