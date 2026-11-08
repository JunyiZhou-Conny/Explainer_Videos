"""S05 · Starting the toolbox: three surprises — tracker B 1 → 3 (README › Deployment Steps, README
74–77). No lecture tag (script.md has no LECTURE mark in S05). Persistent group: the GREEN "your
edits" checklist (top right, above the terminal: at most 2 rows visible, older ticked rows slide off
the top; it gains a row on each fix and leaves at block 11).

Beats (script.md "## S05"; one voiceover block each):
 0  TRACKER B 1. `laptop` terminal (12 rows) at student@laptop:~/cheese-app-aws$; ▶ your turn; types
    `cd src/deployment` (no output), the prompt becomes P_LAPTOP; `pwd; ls -a` → laptop/20: 2, 8,
    12–16, 19–21; the playbooks flash, `inventory.yml` and `docker-shell.sh` turn YELLOW. GREY chip
    above the terminal, once: "your prompt shows your own user".
 1  TRACKER B 1. The terminal goes; CODE(docker-shell.sh: 10–21) (12-line limit: line 9 is the
    comment above): line 10 YELLOW bar, line 13 (the `<<<` here-string) PINK bar, the two variable
    names on 14–15 flash; line 17 ORANGE bar + ORANGE chip "hard-coded · masked".
 2  TRACKER B 2 · extra. A 4-row strip: `bash docker-shell.sh` (extra) → laptop/21: 2 (wrapped) RED.
    Above it the path ladder: deployment → src → cheese-app-aws → student → /home/secrets ✗, one
    GREY "../" step per dot-dot (each lights in the error row), the fourth lands RED.
 3  TRACKER B 2. The ladder's third step turns GREEN ("~/secrets ✓"), then the ladder goes; README(76)
    card; ▶ your turn (title bar); the terminal grows; the README's sed edit (laptop/22, folded; cut + chip) →
    22: 3, 5; line 3 GREEN; GREY chip "sed is our editor · use yours". The card leaves into the
    tracker; the checklist is born with row 1 "docker-shell.sh:10 · ../../../secrets", ticked.
 4  TRACKER B 3. The terminal clears; `sh docker-shell.sh` → laptop/23: 2 RED, "13" ringed.
 5  TRACKER B 3 · extra. `ls -l /bin/sh; head -1 docker-shell.sh` (extra) → laptop/24: 2–3, `dash` RED;
    the terminal shrinks to a 4-row strip (the folded command and both lines); an inset of docker-shell.sh:13 with `<<<` ringed RED,
    "here-string"; `#!/bin/bash` GREEN; checklist row 2 "Linux: bash docker-shell.sh" + erratum tag.
 6  TRACKER B 3 · extra. The inset goes, the terminal grows (8 rows): `bash docker-shell.sh` (extra)
    → laptop/25: 3, …, 20 (cut), 28 (wrapped), 34; 20, 28, 34 RED; "at the time of recording" on the
    title bar; checklist row 2 ticked. Beside line 28 a GREY tag "this curl: baltocdn.com/helm ·
    Dockerfile:33" (laptop/25: 41): the ERROR header names pkgs.k8s.io, whose curl passed (23).
 7  TRACKER B 3 · extra. → laptop/25: …, 49 RED; the terminal shrinks to a 3-row strip (20, 34, 49);
    CODE(docker-shell.sh: 3–4) above it, `#set -e` YELLOW + GREY chip "commented out"; the ERROR row
    flashes on "Check the build output".
 8  TRACKER B 3 · extra. Strip and panel go; CODE(Dockerfile: 31–37): 33–34 struck RED, `helm` on 36
    struck RED; the panel slides into checklist row 3 "Dockerfile · drop Helm (33–34, 36)" (row 1
    slides off); a 20 pt terminal (9 rows): the extra sed && git diff (laptop/27, folded) → 27: 10–11,
    13–14 (cut; RED -, GREEN +); `bash docker-shell.sh` → laptop/28: 3, 33, "FINISHED" GREEN, row 3
    ticked.
 9  TRACKER B 3 · extra. The terminal becomes the toolbox (prompt and title from laptop/28: 35);
    `ls -la /secrets; pwd; ls` → 28: 36–38, ringed RED "empty"; the terminal shrinks to a 3-row strip;
    CODE(docker-shell.sh: 26) slides in, its four `../` RED; erratum chip "README: not mentioned"; on
    "The prompt ID changes" a GREY chip on the title bar "changes every start", the id underlined.
10  TRACKER B 3 · extra. `exit` (from 28: 42–43; GREY chip "exit the toolbox"); prompt back to
    P_LAPTOP, title `laptop`; checklist rows 4 "docker-shell.sh:26 · three ../" and 5
    "docker-shell.sh:17 · your account ID"; the extra sed (laptop/30, folded) → 30: 2–4: line 3
    ORANGE, line 4 GREEN (row 4 ticked); GREY chip "your account ID: aws sts get-caller-identity".
11  TRACKER B 3. The checklist leaves; a fresh 13-row terminal: ▶ your turn; `bash docker-shell.sh`
    → "[+] Building … FINISHED" (31: 3, GREY); the toolbox prompt (31: 35) and its command → 31: 36,
    39–42, 44–45 (43, AWS_CA_BUNDLE, cropped): the .pem and the CSV GREEN, GREY chip "yours:
    ac215_2024.pem", the four AWS_ names flash; V3: the badge glyph slides from the CSV row into a
    small TEAL crate "cheese-app-deployment". Fade; empty frame.

Folds (laptop/22, 27, 30): fold_rows breaks only at spaces outside quotes, so every row types back as
shell; a quoted sed expression longer than a row is cut with '…' and the GREY chip "cut to fit · full
command: study guide" goes with it (on an empty last row, beside the command's last row, or on the
title bar, wherever it covers nothing).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real sources (checked)
C20, C21, C22, C23, C24 = capture("20"), capture("21"), capture("22"), capture("23"), capture("24")
C25, C27, C28, C30, C31 = capture("25"), capture("27"), capture("28"), capture("30"), capture("31")
X28, X31 = toolbox_capture("28"), toolbox_capture("31")
DS = "src/deployment/docker-shell.sh"
CD = "cd src/deployment"
assert readme(75) == "- Go to src/deployment folder", readme(75)
assert C20.cmd == "pwd; ls -a" and C20.line(2) == "/home/student/cheese-app-aws/src/deployment"
assert C20.line(19) == "docker-shell.sh" and C20.line(20) == "inventory.yml"
assert C21.cmd == "bash docker-shell.sh" and C21.exit == 1
assert C21.line(2) == f"Error: AWS credentials file not found at ../../../../secrets/{CSV_NAME}"
assert 'CSV_FILE="../../../secrets/deployment-ac215-user_accessKeys.csv"' in readme(76)
assert C22.cmd.startswith("sed -i 's|^CSV_FILE=.*|") and C22.line(3) == f'CSV_FILE="../../../secrets/{CSV_NAME}"'
assert C23.cmd == "sh docker-shell.sh" and "sh docker-shell.sh" in readme(77)
assert C23.line(2) == "docker-shell.sh: 13: Syntax error: redirection unexpected"
assert C24.cmd == "ls -l /bin/sh; head -1 docker-shell.sh" and C24.line(2).endswith("/bin/sh -> dash")
assert C24.line(3) == "#!/bin/bash"
assert C25.cmd == "bash docker-shell.sh" and "ERROR [ 9/15]" in C25.line(20)
assert "curl: (60) SSL certificate problem" in C25.line(28) and C25.line(34).endswith("gpg: no valid OpenPGP data found.")
assert C25.line(41).lstrip().startswith("33 | >>>     curl https://baltocdn.com/helm/signing.asc")
assert C25.line(49) == "Unable to find image 'cheese-app-deployment:latest' locally"
assert C27.cmd.endswith("Dockerfile && git diff Dockerfile")
assert C27.line(10).startswith("-    curl https://baltocdn.com/helm/signing.asc")
assert C27.line(14).startswith("+    apt-get install -y --no-install-recommends kubectl python3.9")
assert C28.cmd == "bash docker-shell.sh" and "(20/20) FINISHED" in C28.line(3)
assert X28.prompt == "root@b0ed47a6a572:/app#" and X28.cmd == "ls -la /secrets; pwd; ls"
assert C30.cmd.startswith("sed -i -e 's|^export SECRETS_DIR=.*|")
assert C30.line(3).strip() == f'export AWS_ACCOUNT_ID="{ACCOUNT}"'
assert C30.line(4) == "export SECRETS_DIR=$(pwd)/../../../secrets/"
assert X31.cmd == "ls -la /secrets; env | grep ^AWS_ | cut -d= -f1 | sort"
assert X31.line(39).endswith(PEM_README) and X31.line(40).endswith(CSV_NAME)
assert excerpt(DS, 4, 4) == "#set -e" and excerpt(DS, 26, 26) == "export SECRETS_DIR=$(pwd)/../../../../secrets/"
assert excerpt(DS, 17, 17).strip() == f'export AWS_ACCOUNT_ID="{ACCOUNT}"'

ROWS = ["docker-shell.sh:10 · ../../../secrets", None, "Dockerfile · drop Helm (33–34, 36)",
        "docker-shell.sh:26 · three ../", "docker-shell.sh:17 · your account ID"]
CK_RIGHT, CK_TOP = 6.5, 2.75
T20 = 20


# ------------------------------------------------------------------ helpers of this scene
def recolor(glyphs, color):
    """ANIMs, glyph by glyph (never animate a substring group itself)."""
    return [g.animate.set_color(color) for g in glyphs]


def split_outside(cmd: str) -> list[str]:
    """The command's words: split at single spaces outside quotes only (a quoted sed expression is
    one word, its inner spaces kept). An option `-e` is glued to the expression that follows."""
    words, cur, q = [], "", None
    for ch in cmd:
        if q:
            q = None if ch == q else q
            cur += ch
        elif ch in "\"'":
            q = ch
            cur += ch
        elif ch == " ":
            words.append(cur)
            cur = ""
        else:
            cur += ch
    words.append(cur)
    assert " ".join(words) == cmd and all(words), cmd
    glued = []
    for w in words:
        if glued and glued[-1] == "-e":
            glued[-1] += " " + w
        else:
            glued.append(w)
    return glued


def fold_rows(t: Terminal, cmd: str, prefix: int) -> list[str]:
    """The command split into terminal rows the house way: a break only at a space OUTSIDE quotes,
    ' \\' at the end of every row but the last, continuation rows indented by 4, so every row types
    back as shell. Never inside a quoted expression (a backslash-newline inside single quotes is
    kept literally and breaks the edit). A word too long for a whole continuation row (a long sed
    expression) gets a row of its own, cut with '…'; the caller labels it (cut_tag). .cut on the
    returned list: True when a row was cut."""
    limit = t.max_chars
    words = split_outside(cmd)
    rows, cur, avail, was_cut = [], "", limit - prefix, False
    for k, w in enumerate(words):
        last = k == len(words) - 1
        need = len(w) + (0 if last else 2)
        if not cur and len(w) + 2 > limit - 4 and not (last and len(w) <= limit - 4):
            assert rows, cmd
            rows.append(w[:limit - 4 - 3] + "… \\")
            was_cut, avail = True, limit - 4
            continue
        if cur and len(cur) + 1 + need > avail:
            rows.append(cur + " \\")
            cur, avail = "", limit - 4
            if len(w) + 2 > avail and not (last and len(w) <= avail):
                rows.append(w[:avail - 3] + "… \\")
                was_cut = True
                continue
        cur = f"{cur} {w}" if cur else w
    if cur:
        rows.append(cur)
    else:
        rows[-1] = rows[-1][:-2]
    res = FoldRows([rows[0]] + ["    " + r for r in rows[1:]])
    res.cut = was_cut
    assert len(rows[0]) <= limit - prefix and all(len(r) <= limit for r in res), res
    return res


class FoldRows(list):
    cut = False


CUT_TEXT = "cut · full command: study guide"


def cut_tag(scene, t: Terminal, line=None):
    """PLAYS: the GREY tag for a command cut to fit. line given: pinned beside that row (it scrolls
    with it); else right-aligned on the terminal's last (empty) row, a member of t. Returns it."""
    tg = row_tag(CUT_TEXT)
    if line is not None:
        return pin(scene, line, beside(tg, line, buff=0.4), run_time=0.3)
    y = t._slot(t.rows - 1)[1] - t.pitch / 2 + 0.03
    assert len(t.lines) < t.rows
    tg.move_to([t.box.get_right()[0] - 0.25 - tg.width / 2, y, 0])
    scene.play(FadeIn(tg, shift=LEFT * 0.1), run_time=0.3)
    scene.remove(tg)
    t.add(tg)  # a member of t, drawn over its box (drop it with drop_tags)
    scene.add(t)
    return tg


def type_folded(scene, t: Terminal, cmd: str, type_time: float = 0.5) -> VGroup:
    """PLAYS: type `cmd` at t's prompt, folded with fold_rows. Returns a VGroup with .rows and .cut."""
    rows = fold_rows(t, cmd, len(t.prompt) + 1)
    lines = [type_cmd(scene, t, rows[0], type_time=type_time)]
    for r in rows[1:]:
        lines.append(type_cmd(scene, t, r, type_time=type_time, prompt=False))
    g = VGroup(*lines)
    g.rows, g.text, g.cut = lines, " ".join(ln.text for ln in lines), rows.cut
    return g


def bar_tags(scene, t: Terminal, *tags, left: bool = False):
    """PLAYS: row tags on t's title bar, right to left from its right end (left=True: left to right
    after the window dots). They become members of t (drawn over its box). Returns them."""
    y = t.box.get_top()[1] - t.bar_h / 2
    if left:
        x = t.dots.get_right()[0] + 0.3
        for tg in tags:
            tg.move_to([x + tg.width / 2, y, 0])
            x += tg.width + 0.15
    else:
        x = t.box.get_right()[0] - 0.15
        for tg in tags:
            tg.move_to([x - tg.width / 2, y, 0])
            x -= tg.width + 0.15
    scene.play(*[FadeIn(tg, shift=LEFT * 0.1) for tg in tags], run_time=0.4)
    for tg in tags:
        scene.remove(tg)
        t.add(tg)
    scene.add(t)
    return list(tags)


def drop_tags(scene, t: Terminal, tags, *extra, run_time: float = 0.3):
    """PLAYS: title-bar tags (and anything in `extra`, animations) leave; they stop being t's members."""
    for tg in tags:
        if tg in t.submobjects:
            t.remove(tg)
    scene.play(*[FadeOut(tg) for tg in tags], *extra, run_time=run_time)
    scene.remove(*tags)


def drop_all(scene, *mobs, run_time: float = 0.3):
    scene.play(*[FadeOut(m) for m in mobs], run_time=run_time)
    scene.remove(*mobs)


def clear_term(scene, t: Terminal, run_time: float = 0.3):
    gone = list(t.lines)
    for m in gone:
        t.lines.remove(m)
    if gone:
        scene.play(FadeOut(VGroup(*gone)), run_time=run_time)
        scene.remove(*gone)


def find_row(rows, sub):
    hits = [r for r in rows if sub in r.text]
    assert hits, (sub, [r.text for r in rows])
    return hits[0]


def place_ck(ck):
    return ck.shift(np.array([CK_RIGHT - ck.frame.get_right()[0], CK_TOP - ck.frame.get_top()[1], 0]))


def ck_scroll(scene, ck: Checklist, run_time: float = 0.5):
    """PLAYS: the oldest (ticked) row slides off the top; the card closes the gap (top fixed)."""
    r0, r1 = ck.rows[0], ck.rows[1]
    dy = r0.get_center()[1] - r1.get_center()[1]
    new_fr = box(ck.card_w, ck.frame.height - dy, ck.edge_color, fill=S.GREY_DARKER, fill_opacity=1)
    new_fr.align_to(ck.frame, UP).align_to(ck.frame, LEFT)
    ck.rows.remove(r0)
    scene.play(FadeOut(r0, shift=UP * 0.15), ck.rows.animate.shift(UP * dy), Transform(ck.frame, new_fr),
               run_time=run_time)
    scene.remove(r0, *r0.get_family())
    ck._reseat(scene)


def row_bash():
    g = VGroup(label("Linux: bash, not sh", 20, INK), erratum_tag()).arrange(RIGHT, buff=0.18)
    return g


class StartToolbox(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S05"] == 12, len(SAY)

        # ========================================================== 0. go to the deployment folder
        tr = tracker_b(1)
        t = term(P_REPO, rows=12)
        own = under_term(t, grey_chip("your prompt shows your own user"))
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(own, shift=DOWN * 0.1), run_time=0.4)
            ln = type_cmd(self, t, CD, type_time=0.7)
            pin(self, ln, beside(turn_row(), ln))
            cd_prompt(self, t, P_LAPTOP)
            type_capture(self, t, C20, type_time=0.5)
            rows = out(self, t, C20.at(2, 8, (12, 16), (19, 21)), run_time=0.7)
            vo.wait_until("Here are the playbooks")
            books = [r for r in rows if r.text.startswith("deploy-")]
            self.play(each([r.glyphs for r in books], OWN, scale=1.06, lag=0.12), run_time=1.0)
            self.add(t)
            vo.wait_until("the inventory")
            inv = find_row(rows, "inventory.yml")
            self.play(*recolor(inv.glyphs, TURN), run_time=0.4)
            vo.wait_until("and docker shell")
            dsh = find_row(rows, "docker-shell.sh")
            self.play(*recolor(dsh.glyphs, TURN), run_time=0.4)
            self.play(Indicate(dsh.glyphs, color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(t)

        # ========================================================== 1. open the script
        p1 = code(DS, 10, 21, font_size=T20, trim=70)
        p1.move_to([0, (PIC_TOP - 3.4) / 2 + 0.1, 0])
        b10 = line_bar(p1.code, 0, TURN, 0.22)
        b13 = line_bar(p1.code, 3, ROUTE, 0.25)
        b17 = line_bar(p1.code, 7, SHARED, 0.25)
        masked = shared_chip("hard-coded · masked")
        masked.move_to([p1.get_right()[0] - 0.3 - masked.width / 2, p1.code.code_lines[7].get_center()[1], 0])
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(t), FadeOut(own), run_time=0.5)
            self.remove(t, own)
            self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(b10), run_time=0.4)
            p1.add(b10)
            vo.wait_until("It splits the second line")
            self.play(FadeIn(b13), run_time=0.4)
            p1.add(b13)
            self.play(Circumscribe(code_span(p1.code, 3, "<<<"), color=ROUTE, buff=0.06), run_time=0.8)
            self.play(each([code_span(p1.code, 4, "AWS_ACCESS_KEY_ID", 0),
                            code_span(p1.code, 5, "AWS_SECRET_ACCESS_KEY", 0)], ROUTE, scale=1.1, lag=0.4),
                      run_time=1.0)
            vo.wait_until("Line 17 hard codes")
            self.play(FadeIn(b17), *recolor(code_span(p1.code, 7, ACCOUNT), SHARED), run_time=0.5)
            p1.add(b17)
            self.play(FadeIn(masked, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("a placeholder here")
            self.play(Indicate(masked.text, color=SHARED, scale_factor=1.1), run_time=0.7)

        # ========================================================== 2. run it as cloned: one level too far
        t = term(P_LAPTOP, rows=4)
        names = ["deployment", "src", "cheese-app-aws", "student", "/home/secrets ✗"]
        chips = [grey_chip(n, size=22, mono_font=True) for n in names[:4]] + [err_chip(names[4], size=22, mono_font=True)]
        for c, (x, y) in zip(chips, [(4.9, -0.6), (2.6, 0.18), (0.3, 0.96), (-2.1, 1.74), (-4.5, 2.45)]):
            c.move_to([x, y, 0])
        steps = []
        for i in range(4):
            a = arrow(chips[i].get_corner(UL) + RIGHT * 0.25, chips[i + 1].get_corner(DR) + LEFT * 0.25,
                      S.GREY, buff=0.08)
            lb = mono("../", 20, S.GREY).next_to(a.get_center(), DL, buff=0.06)
            steps.append(VGroup(a, lb))
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(p1), FadeOut(masked), track(tr, 2, True), run_time=0.5)
            self.remove(p1, masked)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.4)
            type_folded(self, t, C21.cmd, type_time=0.5)
            ex = bar_tags(self, t, extra_row())
            vo.wait_until("and it stops")
            err = out(self, t, [(s, ERR) for s in soft(C21.at(2), t.max_chars)], run_time=0.5)
            vo.wait_until("Four dot dots")
            path_row = find_row(err, "../../../../")
            self.play(FadeIn(chips[0], shift=UP * 0.1), run_time=0.4)
            for i in range(4):
                u = under(substring(path_row, "../", i), ERR if i == 3 else ROUTE, stroke=4)
                self.play(Create(u), GrowArrow(steps[i][0]), FadeIn(steps[i][1]), run_time=0.4)
                attach(self, path_row, u)
                self.play(FadeIn(chips[i + 1], shift=UP * 0.1), run_time=0.35)
            vo.wait_until("one level too far")
            self.play(Indicate(chips[4].text, color=ERR, scale_factor=1.12), run_time=0.8)

        # ========================================================== 3. step 2: three levels up
        rd = readme_panel(76, 76, size=T20)
        rd.move_to([-6.5 + rd.width / 2, 2.8 - rd.height / 2, 0])
        found = ok_chip("~/secrets ✓", mono_font=True).move_to(chips[3])
        ck_w = max(Checklist("your edits", [r if r else row_bash()], color=OWN, tag_text=None).frame.width
                   for r in ROWS)
        ck = Checklist("your edits", [ROWS[0]], color=OWN, tag_text=None, card_w=ck_w)
        place_ck(ck)
        with self.voiceover(SAY[3]) as vo:
            drop_tags(self, t, ex, FadeOut(VGroup(chips[4], steps[3])), track(tr, 2), run_time=0.4)
            self.remove(chips[4], steps[3])
            self.play(FadeTransform(chips[3], found), run_time=0.5)
            vo.wait_until("with sed or your editor")
            self.play(FadeOut(VGroup(*chips[:3], *steps[:3], found)), run_time=0.4)
            self.remove(*chips[:3], *steps[:3], found)
            clear_term(self, t)
            resize(self, t, 9, extra=[FadeIn(rd, shift=DOWN * 0.15)], run_time=0.6)
            tt = bar_tags(self, t, turn_row())
            tt += bar_tags(self, t, row_tag("sed is our editor · use yours"), left=True)
            assert type_folded(self, t, C22.cmd, type_time=0.4).cut
            res = out(self, t, [(s, OUTPUT) for s in soft(C22.at(3, 5), t.max_chars)], run_time=0.5)
            cut22 = cut_tag(self, t)
            vo.wait_until("Now the file is found")
            line3 = find_row(res, "CSV_FILE=")
            self.play(*recolor(line3.glyphs, OWN), run_time=0.4)
            self.play(Indicate(line3.glyphs, color=OWN, scale_factor=1.05), run_time=0.6)
            self.add(t)
            self.play(FadeOut(rd, target_position=tr.caption.get_center()), run_time=0.6)
            self.remove(rd)
            self.play(FadeIn(ck, shift=LEFT * 0.2), run_time=0.5)
            ck.tick(self, 0)

        # ========================================================== 4. step 3: sh, as written
        with self.voiceover(SAY[4]) as vo:
            drop_tags(self, t, tt + [cut22], track(tr, 3), run_time=0.5)
            clear_term(self, t)
            type_folded(self, t, C23.cmd, type_time=0.6)
            vo.wait_until("Surprise 1")
            e23 = out(self, t, [(C23.at(2)[0], ERR)], run_time=0.4)[0]
            vo.wait_until("a syntax error on line 13")
            r13 = ring(substring(e23, "13"), ERR, buff=0.07)
            self.play(Create(r13), run_time=0.4)
            attach(self, e23, r13)
            vo.wait_until("redirection unexpected")
            self.play(Indicate(substring(e23, "redirection unexpected"), color=ERR, scale_factor=1.06), run_time=0.7)
            self.add(t)

        # ========================================================== 5. extra: sh is dash
        inset = code(DS, 13, 13, font_size=T20, trim=70)
        inset.move_to([0, 0.25, 0])
        here = code_span(inset.code, 0, "<<<")
        here_ring = ring(here, ERR, buff=0.08)
        here_lb = label("here-string", 20, ERR)
        here_lb.move_to([here_ring.get_center()[0], inset.get_bottom()[1] - 0.08 - here_lb.height / 2, 0])
        with self.voiceover(SAY[5]) as vo:
            self.play(track(tr, 3, True), run_time=0.4)
            ln24 = type_folded(self, t, C24.cmd, type_time=0.6)
            ex = bar_tags(self, t, extra_row())
            o24 = out(self, t, C24.at(2, 3), run_time=0.4)
            vo.wait_until("S H is dash")
            dash = substring(o24[0], "dash")
            self.play(*recolor(dash, ERR), run_time=0.3)
            self.play(Indicate(dash, color=ERR, scale_factor=1.2), run_time=0.6)
            self.add(t)
            vo.wait_until("which has no here string")
            drop_tags(self, t, ex, run_time=0.2)
            resize(self, t, 4, keep=[*ln24.rows, *o24], run_time=0.5)
            ex = bar_tags(self, t, extra_row())
            self.play(FadeIn(inset, shift=UP * 0.15), run_time=0.4)
            self.play(Create(here_ring), FadeIn(here_lb, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("And typing S H skips")
            self.play(*recolor(o24[1].glyphs, OWN), run_time=0.4)
            self.play(Indicate(o24[1].glyphs, color=OWN, scale_factor=1.12), run_time=0.6)
            self.add(t)
            vo.wait_until("On a Mac")
            ck.add_row(self, row_bash())

        # ========================================================== 6. surprise 2: the Helm key
        b_lines = [squeeze_spaces(C25.at(3)[0].rstrip()), "…", cut(C25.line(20), "pkgs.k8s.io")]
        with self.voiceover(SAY[6]) as vo:
            drop_tags(self, t, ex, FadeOut(VGroup(inset, here_ring, here_lb)), run_time=0.4)
            self.remove(inset, here_ring, here_lb)
            clear_term(self, t, run_time=0.2)
            resize(self, t, 8, run_time=0.5)
            type_folded(self, t, C25.cmd, type_time=0.5)
            ex = bar_tags(self, t, extra_row(), time_row())
            ck.tick(self, 1)
            o25 = out(self, t, b_lines, run_time=0.5)
            vo.wait_until("the build stops at step 9")
            e20 = o25[-1]
            self.play(*recolor(e20.glyphs, ERR), run_time=0.4)
            self.play(Indicate(substring(e20, "ERROR [ 9/15]"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.add(t)
            vo.wait_until("Curl can't verify")
            o28 = out(self, t, [(s, ERR) for s in soft([C25.line(28)], t.max_chars)], run_time=0.4)
            pin(self, o28[-1], beside(row_tag([("this curl:", "label"), ("baltocdn.com/helm", "mono"),
                                               ("· Dockerfile:33", "label")]), o28[-1], buff=0.4))
            vo.wait_until("so no signing key arrives")
            o34 = out(self, t, [(C25.line(34), ERR)], run_time=0.4)[0]
            self.play(Indicate(substring(o34, "gpg: no valid OpenPGP data found."), color=ERR, scale_factor=1.06),
                      run_time=0.7)
            self.add(t)

        # ========================================================== 7. set -e is commented out
        p3 = code(DS, 3, 4)
        p3.move_to([0, (STRIP_TOP + 0.78) / 2 + 0.05, 0])
        setx = code_span(p3.code, 1, "#set -e")
        cmt = row_tag("commented out")
        cmt.move_to([setx.get_right()[0] + 0.4 + cmt.width / 2, setx.get_center()[1], 0])
        with self.voiceover(SAY[7]) as vo:
            o49 = out(self, t, ["…", (C25.line(49), ERR)], run_time=0.5)[-1]
            self.play(Indicate(o49.glyphs, color=ERR, scale_factor=1.05), run_time=0.6)
            self.add(t)
            vo.wait_until("set dash e is commented out")
            drop_tags(self, t, ex, run_time=0.2)
            resize(self, t, 3, keep=[e20, o34, o49], run_time=0.5)
            ex = bar_tags(self, t, extra_row())
            self.play(FadeIn(p3, shift=UP * 0.15), run_time=0.4)
            self.play(*recolor(setx, TURN), FadeIn(cmt, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("so it runs an image")
            self.play(Indicate(o49.glyphs, color=ERR, scale_factor=1.06), run_time=0.7)
            self.add(t)
            vo.wait_until("Check the build output")
            self.play(Circumscribe(e20.glyphs, color=TURN, buff=0.06), run_time=0.9)
            self.add(t)

        # ========================================================== 8. drop Helm, the toolbox builds
        p8 = code("src/deployment/Dockerfile", 31, 37, font_size=T20, trim=70)
        p8.move_to([0, (0.73 + BOTTOM) / 2, 0])
        s33 = strike(p8.code.code_lines[2], ERR)
        s34 = strike(p8.code.code_lines[3], ERR)
        s36 = strike(code_span(p8.code, 5, "helm"), ERR)
        diff = [(cut(C27.line(10), "signing.asc"), ERR), (cut(C27.line(11), 'all main"'), ERR),
                (cut(C27.line(13), "kubectl helm"), ERR), (cut(C27.line(14), "kubectl python3.9"), OWN)]
        built = [(squeeze_spaces(C28.line(3).rstrip()), OUTPUT), (squeeze_spaces(C28.line(33).rstrip()), OUTPUT)]
        with self.voiceover(SAY[8]) as vo:
            drop_tags(self, t, ex, FadeOut(VGroup(p3, cmt)), FadeOut(t), run_time=0.5)
            self.remove(p3, cmt, t)
            self.play(FadeIn(p8, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Your laptop may")
            self.play(Indicate(code_span(p8.code, 2, "baltocdn.com"), color=ERR, scale_factor=1.1), run_time=0.7)
            vo.wait_until("No playbook uses Helm")
            self.play(Create(s33), Create(s34), run_time=0.6)
            p8.add(s33, s34)
            vo.wait_until("and the word helm")
            self.play(Create(s36), run_time=0.4)
            p8.add(s36)
            vo.wait_until("and the toolbox builds")
            ck_scroll(self, ck)
            self.play(FadeOut(p8, target_position=ck.frame.get_bottom() + DOWN * 0.2), run_time=0.5)
            self.remove(p8)
            ck.add_row(self, ROWS[2])
            t = term(P_LAPTOP, rows=9, size=T20)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.4)
            l27 = type_folded(self, t, C27.cmd, type_time=0.35)
            assert l27.cut
            cut_tag(self, t, l27)
            ex = bar_tags(self, t, extra_row())
            out(self, t, diff, run_time=0.5)
            type_folded(self, t, C28.cmd, type_time=0.5)
            o28b = out(self, t, built, run_time=0.4)
            fin = substring(o28b[0], "FINISHED")
            self.play(*recolor(fin, OWN), run_time=0.3)
            ck.tick(self, 1)

        # ========================================================== 9. surprise 3: /secrets is empty
        p26 = code(DS, 26, 26)
        p26.move_to([-6.5 + p26.width / 2, (STRIP_TOP + 0.78) / 2 - 0.1, 0])
        dots26 = [code_span(p26.code, 0, "../", i) for i in range(4)]
        e_chip = erratum_tag("erratum · README: not mentioned")
        e_chip.next_to(p26, UP, buff=0.12).align_to(p26, LEFT)
        with self.voiceover(SAY[9]) as vo:
            drop_tags(self, t, ex, run_time=0.2)
            set_toolbox(self, t, X28.prompt)
            run9 = type_cmd(self, t, X28.cmd, type_time=0.6)
            e9 = out(self, t, X28.at((36, 38)), run_time=0.4)
            vo.wait_until("slash secrets is empty")
            r9 = ring(VGroup(e9[0].glyphs, e9[2].glyphs), ERR, buff=0.08)
            emp = row_tag("empty", ERR).next_to(r9, RIGHT, buff=0.25)
            self.play(Create(r9), FadeIn(emp), run_time=0.5)
            vo.wait_until("Line 26 has")
            self.play(FadeOut(r9), FadeOut(emp), run_time=0.2)
            self.remove(r9, emp)
            resize(self, t, 3, keep=[run9, e9[1], e9[2]], run_time=0.5)
            r9 = ring(VGroup(e9[1].glyphs, e9[2].glyphs), ERR, buff=0.06)
            emp = row_tag("empty", ERR).next_to(r9, RIGHT, buff=0.25)
            self.play(FadeIn(p26, shift=RIGHT * 0.2), Create(r9), FadeIn(emp), run_time=0.5)
            attach(self, e9[2], r9)
            attach(self, e9[2], emp)
            self.play(LaggedStart(*[AnimationGroup(*recolor(d, ERR)) for d in dots26], lag_ratio=0.3),
                      run_time=0.9)
            vo.wait_until("so Docker mounted an empty folder")
            self.play(FadeIn(e_chip, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("The prompt ID changes")
            pid = substring(run9, X28.prompt.split("@")[1].split(":")[0])
            idl = under(pid, S.GREY, stroke=3)
            self.play(Create(idl), run_time=0.3)
            attach(self, run9, idl)
            idc = bar_tags(self, t, row_tag("changes every start"), left=True)
            self.play(Indicate(pid, color=INK, scale_factor=1.1), run_time=0.6)
            self.add(t)

        # ========================================================== 10. fix 26 and 17, back on the laptop
        assert X28.raw[42 - 1] == f"{X28.prompt} exit" and X28.line(43) == "exit"
        sts = grey_chip("your account ID: aws sts get-caller-identity")
        with self.voiceover(SAY[10]) as vo:
            e9[2].remove(r9, emp)
            run9.remove(idl)
            drop_tags(self, t, idc, FadeOut(VGroup(p26, e_chip, r9, emp, idl)), run_time=0.3)
            self.remove(p26, e_chip, r9, emp, idl)
            ck_scroll(self, ck, run_time=0.35)
            ck.add_row(self, ROWS[3], run_time=0.35)
            xl = type_cmd(self, t, "exit", type_time=0.25)
            pin(self, xl, beside(row_tag("exit the toolbox"), xl, buff=0.4), run_time=0.25)
            out(self, t, X28.at(43), run_time=0.2)
            t.set_prompt(P_LAPTOP)
            retitle(self, t, T_LAPTOP, run_time=0.3)
            resize(self, t, 9, run_time=0.4)
            vo.wait_until("and put your own account ID")
            ck_scroll(self, ck, run_time=0.35)
            ck.add_row(self, ROWS[4], run_time=0.35)
            assert type_folded(self, t, C30.cmd, type_time=0.2).cut
            ex = bar_tags(self, t, extra_row())
            ex += bar_tags(self, t, row_tag(CUT_TEXT), left=True)
            o30 = out(self, t, C30.at(2, 3, 4), run_time=0.35)
            self.play(*recolor(substring(o30[1], ACCOUNT), SHARED), *recolor(o30[2].glyphs, OWN), run_time=0.35)
            vo.wait_until("AWS S T S get caller identity")
            sts.next_to(t.box, UP, buff=0.12).align_to(t.box, LEFT)
            self.play(FadeIn(sts, shift=DOWN * 0.1), run_time=0.4)
            ck.tick(self, 0)
            vo.wait_until("once your keys work")
            self.play(Indicate(sts.text, color=INK, scale_factor=1.06), run_time=0.7)

        # ========================================================== 11. run it again: the toolbox works
        t11 = term(P_LAPTOP, rows=12, size=T20)
        aws = X31.at((41, 45))
        assert aws == ["AWS_ACCESS_KEY_ID", "AWS_ACCOUNT_ID", "AWS_DEFAULT_REGION", "AWS_SECRET_ACCESS_KEY"], aws
        box_c = crate(T_TOOLBOX)
        box_c = crate(T_TOOLBOX, box_w=box_c.frame.width + 0.9)
        box_c.text.shift(RIGHT * 0.4)
        with self.voiceover(SAY[11]) as vo:
            drop_tags(self, t, ex, FadeOut(t), FadeOut(ck), FadeOut(sts), track(tr, 3), run_time=0.6)
            self.remove(t, ck, sts)
            self.play(FadeIn(t11, shift=UP * 0.2), run_time=0.4)
            type_folded(self, t11, C31.cmd, type_time=0.5)
            turn = bar_tags(self, t11, turn_row())[0]
            out(self, t11, [(squeeze_spaces(C31.line(3).rstrip()), S.GREY)], run_time=0.4)
            set_toolbox(self, t11, X31.prompt)
            type_folded(self, t11, X31.cmd, type_time=0.5)
            files = out(self, t11, soft(X31.at(36, 39, 40), t11.max_chars), run_time=0.5)
            env = out(self, t11, aws, run_time=0.5)
            vo.wait_until("both files are there")
            pem = find_row(files, PEM_README)
            csv = find_row(files, CSV_NAME)
            self.play(*recolor(substring(pem, PEM_README), OWN), *recolor(substring(csv, CSV_NAME), OWN), run_time=0.5)
            vo.wait_until("yours named")
            pem_g = substring(pem, PEM_README)
            pr = ring(pem_g, S.GREY, buff=0.06)
            under_pem = find_row(files, "-rw-r--r--")
            yours = row_tag(f"yours: {PEM_CODE}")
            yours.move_to([min(pr.get_center()[0], t11.box.get_right()[0] - 0.15 - yours.width / 2),
                           under_pem.strut.get_center()[1], 0])
            self.play(Create(pr), FadeIn(yours, shift=UP * 0.1), run_time=0.5)
            attach(self, pem, pr)
            attach(self, under_pem, yours)
            vo.wait_until("and four AWS variables")
            self.play(each([n.glyphs for n in env], IMAGE, scale=1.08, lag=0.2), run_time=1.0)
            self.add(t11)
            box_c.move_to([3.4, env[1].get_bottom()[1] - 0.05, 0])
            badge = badge_glyph(0.42).next_to(substring(csv, CSV_NAME), RIGHT, buff=0.3)
            self.play(FadeIn(box_c, shift=LEFT * 0.15), FadeIn(badge, scale=0.6), run_time=0.5)
            self.play(badge.animate.move_to(box_c.frame.get_left() + RIGHT * 0.5), run_time=0.9)
            vo.wait_until("Pause, and get to this prompt")
            flash_tag(self, turn)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.remove(*self.mobjects)
        self.wait(0.3)
