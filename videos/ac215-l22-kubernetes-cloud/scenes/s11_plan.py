"""S11 · deploy_k8s: config and a 23-resource plan (AC215 L22, the full follow-along). TRACKER [C] 1
(beat 0), 2 (beats 1-2), 2 · extra (beat 3), 3 (beat 4), 3 · extra (beats 4-7), 3 (beat 8).
Lecture: 22 · 41 (beat 0 only).

Beats (script.md "## S11", one voiceover block each):
0. TRACKER [C] 1. LECTURE 22 · 41. A GREY README card 'README.md · line 437' ("cd into deploy_k8s from
   the deployment folder") with the GREY chip 'works from either folder' above a 9-row 20 pt toolbox
   terminal ('laptop · toolbox', prompt …:/app/deploy_images# from S10). `cd /app/deploy_k8s` typed
   (tag 'extra · our spelling' on the bar) -> (no output), the prompt becomes …:/app/deploy_k8s#.
   `pulumi stack init dev` -> TERM(b30: 2 wrap) RED; the same command again (extra, local; 'extra'
   beside it) -> TERM(c10: 2) GREEN. The lecture tag fades with the block.
1. TRACKER [C] 2. The card leaves, the terminal grows to 13 rows. The three README config lines
   (README:441–443) typed one by one (b31-1..3, the long two fold), each -> its RED token line (wrap);
   every 'ac215-project' gets a GREY ring as it appears. The three RED lines dim. On "Replace ac215
   project" the GREY default tag "the README's default · change to yours" appears above the terminal
   and the rings flash. TRACKER [C] 2 · extra: the same three again as one quick block (c11-1..3, no
   output, 'extra' on the bar, rings too) and the GREEN chip '✓ local · same three keys'.
2. TRACKER [C] 2. The terminal shrinks to a 3-row strip. CODE(create_cluster.py: 9–12) at the top
   (20 pt; line 9 soft-wrapped after '.get(', a GREY '↪' on its second row): line 9 BLUE bar + its key BLUE, chip
   "→ the nodes' service account (line 50)" (BLUE outline); lines 10–12 GREEN bar + key GREEN, chip
   "→ the API's Kubernetes service account (line 158)" (GREEN outline).
3. TRACKER [C] 2 · extra. The panel leaves, the terminal grows to 13 rows. `pulumi config; pulumi stack
   ls` (extra) -> TERM(c12: 2–10 wrap; 9–10, the stack ls lines, GREY), line 8 masked to sa_000…; lines 4, 6, 7 GREEN (flash on "lists
   your three keys"); lines 3 and 8 GREY with the row tag 'leftovers · unused' beside line 3 (and
   'unused' beside line 8); on "A typo in a key name" the three key names flash YELLOW.
4. TRACKER [C] 3. `pulumi preview --stack dev --refresh` -> TERM(b32: 2 wrap) RED; TRACKER [C] 3 · extra,
   the same (extra on the bar) -> TERM(c13: 7 wrap, 10, …, 31–34, 37–38), line 34 RED; 'line 70'
   flashes RED. Then the terminal shrinks to a 2-row strip holding c13:31 and c13:34, and above it
   CODE(setup_containers.py: 10–13) (line 10 PINK, the stack name PINK) and CODE(setup_containers.py:
   68–71) (line 70 RED; 'tags[0]' flashes RED on "and got nothing").
5. The panels fade. StackPipe S11: the BLUE state bucket with 'deploy_images' (empty GREY outputs box,
   'init + preview only, no up') and 'deploy_k8s'; on "never finished pulumi up" the PINK StackReference
   reaches the empty box and breaks RED; on "Skipping it is safe" a 'pulumi up' stamp fills the box
   with three tags, and the pipe joins GREEN, 'same bucket · up finished' (held ~1.5 s).
6. TRACKER [C] 3 · extra. The bucket fades; a 3-row strip, 'extra' on its bar, the GREY tag
   'placeholder image tags · nothing built' above it (flashes on "with placeholder tags"). On "nothing
   is built" `pulumi preview --stack dev --refresh` is typed; on "Now the real plan appears" TERM(c20:
   8–11, 13–14, 16–33 wrap) scrolls fast, a box-full at a time, and V6 ResourceTree grows above the
   strip in step with the printed lines (network and cluster + pool with 8–11, provider with 16–17,
   identity / ingress / storage with 18–23, app with 24–33). 'the network', 'the cluster' and 'the
   Kubernetes objects' each open their group's member card (the next one closes the last); on "and
   plus 23 to create" the card closes, the stack chip '+1 · the stack itself', TERM(c20: …, 45) YELLOW
   and the counter '+ 23 to create' YELLOW flash together.
7. In V6 the two PINK dashed reads blink in ('StackReference · deploy-images/dev',
   'nginx-ingress-service'). On "In the outputs" the tree leaves, row 45 fades, the terminal grows to
   12 rows and prints TERM(c20: 35–42, 44, 45): line 38 GREEN, the '[unknown]' lines GREY, 45 YELLOW;
   on "the address and the URL" the ip_address and app_url lines flash.
8. TRACKER [C] 3. A YELLOW '▶ your turn' beside c20:45 ('+ 23 to create'). Fade; empty frame.

Deviations from SHOW:
- The terminal is 20 pt throughout (72 characters a row): c20:19–20, :33 and c13:31 are 67–70
  characters, and the config-set commands fold into fewer rows.
- Beat 0: the 'extra · our spelling' tag sits on the terminal's title bar (the cd row has no room
  for it); README:437's words are on a README card with the 'works from either folder' chip.
- Beat 1: the folded config-set rows leave no room beside them for a row-sized default tag, so every
  'ac215-project' is ringed GREY and ONE default tag above the terminal names them all (it appears
  on "Replace ac215 project"; the rings flash with it). The c11 block's 'extra' is on the title bar.
- Beat 2: the two chips sit under the panel with outlines in their line's colour (BLUE / GREEN) so the
  link from line to chip is visible; the panel is 20 pt and soft-wraps line 9 after '.get(' (the
  line is 82 characters), as line 10 is laid out in the file.
- Beat 3: SHOW names c12: 2–8; the typed command also runs `pulumi stack ls`, so its two lines
  (9–10) print GREY after the config table: the viewer who copies the command sees what we saw.
- Beat 4: the panels need the height, so the terminal shrinks to a 2-row strip that keeps c13:31
  ('line 70') and c13:34 (the TypeError); the code panels are stacked above it rather than beside
  (terminals stay full width). Both panels are dedented (20 pt).
- Beat 6: the placeholder tag sits just above the strip (left), not on the bar (the title is there);
  c20:27–28 (the nginx read lines, 99 characters) wrap.
- Beat 7: c20:35–42 come after 45 in the scene's timeline, so row 45 (printed in beat 6 after a '…')
  fades and is printed again after 35–42 and 44: the terminal ends in file order. The tree leaves
  for the outputs (the 12-row terminal needs the frame).
- Beat 8: the preview command has scrolled away, so '▶ your turn' stands beside '+ 23 to create',
  the line the viewer compares with theirs.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S11"]
assert len(SAY) == SAY_COUNT["S11"] == 9

# ------------------------------------------------------------------ the real sources (checked)
B30, C10 = capture("b30"), capture("c10")
B31 = [capture(f"b31-{i}") for i in (1, 2, 3)]
C11 = [capture(f"c11-{i}") for i in (1, 2, 3)]
C12, B32, C13, C20 = capture("c12"), capture("b32"), capture("c13"), capture("c20")

TOKEN_ERR = "error: PULUMI_ACCESS_TOKEN must be set for login during non-interactive CLI sessions"
assert B30.cmd == readme(440) == "pulumi stack init dev" and B30.line(2) == TOKEN_ERR
assert C10.cmd == B30.cmd and C10.line(2) == "Created stack 'dev'"
for i, n in enumerate((441, 442, 443)):
    assert B31[i].cmd == readme(n), (B31[i].cmd, readme(n))
    assert B31[i].line(2) == TOKEN_ERR
    assert C11[i].cmd == B31[i].cmd and C11[i].lines == []
    assert PROJECT_README in B31[i].cmd
assert C12.cmd == "pulumi config; pulumi stack ls"
assert C12.line(3).startswith("setupSSL") and C12.line(4).startswith("gcp:project")
assert C12.line(6).startswith("security:gcp_ksa_service_account_email")
assert C12.line(7).startswith("security:gcp_service_account_email")
assert C12.line(8).startswith("security:ssh_user") and C12.line(8).endswith(SA_MASK)
assert C12.line(9).split() == ["NAME", "LAST", "UPDATE", "RESOURCE", "COUNT"]
assert C12.line(10).split()[0] == "dev*" and len(C12.lines) <= 11, C12.lines
assert B32.cmd == readme(449) == "pulumi preview --stack dev --refresh" and B32.line(2) == TOKEN_ERR
assert C13.cmd == B32.cmd
assert "read pulumi:pulumi:StackReference organization/deploy-images/dev" in C13.line(7)
assert C13.line(10).strip() == "+  gcp:compute:Network cheese-app-vpc create"
assert 'setup_containers.py", line 70, in <lambda>' in C13.line(31)
assert C13.line(32).strip() == "lambda tags: tags[0]"
assert C13.line(34).strip() == "TypeError: 'NoneType' object is not subscriptable"
assert C13.line(37).strip() == "+ 2 to create" and C13.line(38).strip() == "1 errored"
assert C20.cmd == B32.cmd
assert C20.line(8).strip().startswith("+  gcp:compute:Network cheese-app-vpc")
assert C20.line(14).strip().startswith("+  gcp:container:NodePool cheese-app-pool")
assert C20.line(33).strip().startswith("+  kubernetes:networking.k8s.io/v1:Ingress cheese-app-ingress")
assert C20.line(35) == "Outputs:" and 'cluster_name    : "cheese-app-cluster"' in C20.line(38)
assert C20.line(44) == "Resources:" and C20.line(45).strip() == "+ 23 to create"
assert all("[unknown]" in C20.line(n) for n in (36, 37, 39, 40, 41, 42))
assert C20.line(40).strip().startswith("ip_address") and C20.line(36).strip().startswith("app_url")
# which c20 lines bring which V6 group (TREE_GROUPS members by name)
C20_CHUNKS = (((8, 11), ("network", "cluster")), ((13, 14), ()), ((16, 17), ("provider",)),
              ((18, 23), ("identity", "ingress", "storage")), ((24, 33), ("app",)))
for (a, b), _ in C20_CHUNKS:
    for n in range(a, b + 1):
        assert C20.line(n).strip().startswith("+  "), n
_members = {m for g in TREE_GROUPS for m in g[3]}
_named = {C20.line(n).split()[2] for n in [*range(8, 12), 13, 14, *range(16, 27), *range(29, 34)]}
assert _named == _members, _named ^ _members

# sources
README_437 = readme_lines(437, 437)
assert "deploy_k8s" in README_437 and "deployment" in README_437, README_437
CD_K8S = "cd /app/deploy_k8s"
CC = "src/deployment/deploy_k8s/create_cluster.py"
SC = "src/deployment/deploy_k8s/setup_containers.py"
assert 'get("gcp_service_account_email")' in excerpt(CC, 9, 9)
assert '"gcp_ksa_service_account_email"' in excerpt(CC, 11, 11)
assert "service_account=service_account_email" in excerpt(CC, 50, 50)
assert "ksa_service_account_email" in excerpt(CC, 158, 158)
assert 'StackReference("organization/deploy-images/dev")' in excerpt(SC, 10, 10)
assert "frontend_tag = images_stack.get_output" in excerpt(SC, 13, 13)
assert "lambda tags: tags[0]" in excerpt(SC, 70, 70) and "frontend_tag.apply(" in excerpt(SC, 69, 69)

P_IMAGES = toolbox_prompt("/app/deploy_images")
P_K8S = toolbox_prompt("/app/deploy_k8s")
SIZE = 20


def tb(rows: int) -> Terminal:
    """The 20 pt toolbox terminal (72 characters a row), bottom edge at BOTTOM."""
    return term(P_IMAGES, rows, T_TOOLBOX, size=SIZE)


def bar_y(t, rows: int) -> float:
    """The title bar's centre y of terminal t once resized to `rows`."""
    return BOTTOM + rows * t.pitch + 0.85 - t.bar_h / 2


def mark_extra(scene, t, line, tg):
    """PLAYS: a tag beside the command's last row when it fits (pinned: it scrolls with the row;
    returns None), else on the title bar (returns it: the caller fades it)."""
    row = rows_of(line)[-1]
    if row.strut.get_right()[0] + 0.45 + tg.width < t.box.get_right()[0] - 0.12:
        pin(scene, line, beside(tg, line))
        return None
    bar_tag(t, tg)
    scene.play(FadeIn(tg), run_time=0.3)
    return tg


def bar_tag(t, tg):
    """on_bar() plus a z-index: every `scene.add(t)` (re-seating the terminal after an Indicate)
    puts the terminal's filled box on top again, which hid a bar tag added before it."""
    on_bar(t, tg)
    tg.set_z_index(4)
    return tg


def ring_project(scene, line, run_time: float = 0.3):
    """PLAYS: a GREY ring around 'ac215-project' in a typed (maybe folded) command; it scrolls with
    its row. Returns the ring."""
    row = next(r for r in rows_of(line) if PROJECT_README in r.text)
    rg = ring(substring(row, PROJECT_README), S.GREY, buff=0.04, stroke=2.5)
    scene.play(Create(rg), run_time=run_time)
    attach(scene, row, rg)
    return rg


def glyphs_of(row):
    """The glyphs of a terminal row (never its invisible strut)."""
    return VGroup(*[m for m in row.submobjects if m is not row.strut])


def bars_behind(panel, bars, z: int = 1):
    """Draw translucent line bars under a code panel's text (z-order), not over it."""
    panel.code.code_lines.set_z_index(z + 1)
    for b in bars:
        b.set_z_index(z)


def wrapped_code(path: str, a: int, b: int, folds: dict, size: float = 20) -> VGroup:
    """CODE(path: a–b) with long lines soft-wrapped, as an editor shows them (L21's helper): folds =
    {file line: [break after these substrings]}. Continuation rows are indented two columns deeper
    and marked with a GREY '↪'; every character is the file's. .code .header .rows .src_rows"""
    src_rows, rows = [], {}
    for n in range(a, b + 1):
        s = excerpt(path, n, n)
        ind = len(s) - len(s.lstrip())
        parts, rest = [], s
        for cut_after in folds.get(n, []):
            i = rest.index(cut_after) + len(cut_after)
            parts.append(rest[:i].rstrip())
            rest = rest[i:].lstrip()
        parts.append(rest)
        rows[n] = []
        for k, p_ in enumerate(parts):
            rows[n].append(len(src_rows))
            src_rows.append(p_ if k == 0 else " " * (ind + 2) + p_)
    assert "".join("".join(src_rows).split()) == "".join(excerpt(path, a, b).split())
    c = code_block("\n".join(src_rows), "python", size)
    head = VGroup(mono(path, CAPTION, S.GREY), label(f"· lines {a}–{b}", CAPTION, S.GREY)) \
        .arrange(RIGHT, buff=0.14)
    head.next_to(c, UP, buff=0.1).align_to(c, LEFT).shift(RIGHT * 0.12)
    marks = VGroup()
    for n, ks in rows.items():
        for k in ks[1:]:
            marks.add(label("↪", 20, S.GREY).next_to(c.code_lines[k], LEFT, buff=0.18))
    g = VGroup(c, head, marks)
    g.code, g.header, g.rows, g.src_rows = c, head, rows, src_rows
    return g


def span_bar(code_, k0: int, k1: int, color, opacity: float = 0.18):
    """ONE translucent bar over code lines k0..k1 (0-based): no stripes where per-line bars overlap."""
    a, b = line_bar(code_, k0, color, opacity), line_bar(code_, k1, color, opacity)
    top, bot = a.get_top()[1], b.get_bottom()[1]
    return Rectangle(width=a.width, height=top - bot, stroke_width=0).set_fill(color, opacity) \
        .move_to([a.get_x(), (top + bot) / 2, 0])


def fast_out(scene, t, items, per: float = 0.22):
    """PLAYS: a fast scroll: items (text or (text, colour), soft-wrapped) printed a box-full at a
    time; each box-full pushes the previous one up and out in ONE short play. Returns the new rows."""
    items = soft(items, t.max_chars)
    rows = VGroup()
    for i in range(0, len(items), t.rows):
        ch = [(x, OUTPUT) if isinstance(x, str) else x for x in items[i:i + t.rows]]
        over = len(t.lines) + len(ch) - t.rows
        old = list(t.lines.submobjects[:max(0, over)])
        stay = list(t.lines.submobjects[max(0, over):])
        for m in old:
            t.lines.remove(m)
        anims = [FadeOut(m, shift=UP * t.pitch) for m in old]
        anims += [m.animate.shift(UP * t.pitch * len(old)) for m in stay]
        new = []
        for s_, col in ch:
            ln = mono_line(s_, t.size, col)
            t._place(ln, len(t.lines))
            t.lines.add(ln)
            new.append(ln)
        scene.play(*anims, *[FadeIn(m, shift=UP * t.pitch * 0.5) for m in new], run_time=per)
        scene.remove(*old)
        scene.add(t)
        rows.add(*new)
    return rows


def alive(t, mobs):
    """The mobjects (rows, rings) still on terminal t (not scrolled away)."""
    fam = set(t.lines.get_family())
    return [m for m in mobs if m in fam]


class ClusterPlan(VoiceScene):
    def construct(self):
        # ========================================================== 0. cd deploy_k8s, stack init
        trk = tracker_c(1)
        ref = lref("41")
        t = tb(9)
        assert t.box.get_top()[1] < 0.8, t.box.get_top()
        rc = readme_card(437, README_437)
        rc.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, 2.45, 0], UP)
        either = grey_chip("works from either folder")
        either.next_to(rc, RIGHT, buff=0.3)
        assert either.get_right()[0] < 6.5 and rc.get_bottom()[1] > t.box.get_top()[1] + 0.2
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("From the deployment folder")
            self.play(FadeIn(rc, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("change into deploy k8s")
            r_cd = type_cmd(self, t, CD_K8S, type_time=0.5)
            e0 = mark_extra(self, t, r_cd, extra_row("our spelling"))
            self.play(FadeIn(either, shift=LEFT * 0.15), run_time=0.4)
            cd_prompt(self, t, P_K8S, color=TURN, run_time=0.4)
            vo.wait_until("run pulumi stack init dev")
            type_capture(self, t, B30, type_time=0.5)
            e30 = out(self, t, [(B30.line(2), ERR)], wrap=True, run_time=0.3)
            vo.wait_until("the same token error")
            self.play(Indicate(substring(e30[0], "PULUMI_ACCESS_TOKEN"), color=ERR, scale_factor=1.1),
                      run_time=0.6)
            self.add(t)
            vo.wait_until("and on the local backend")
            anims = [FadeOut(e0)] if e0 is not None else []
            if anims:
                self.play(*anims, run_time=0.25)
                self.remove(e0)
            r10 = type_capture(self, t, C10, type_time=0.5)[0]
            e10 = mark_extra(self, t, r10, extra_row())
            g10 = out(self, t, [(C10.line(2), OWN)], run_time=0.3)[0]
            self.play(Indicate(g10, color=OWN, scale_factor=1.08), run_time=0.6)
            self.add(t)
        self.play(FadeOut(ref), FadeOut(rc), FadeOut(either), run_time=0.4)
        self.remove(ref, rc, either)
        if e10 is not None:
            self.play(FadeOut(e10), run_time=0.2)
            self.remove(e10)

        # ========================================================== 1. three config keys (README), then local
        dft = default_tag()
        rings = []
        with self.voiceover(SAY[1]) as vo:
            resize(self, t, 13, extra=[track(trk, 2)], run_time=0.6)
            assert t.box.get_top()[1] < 2.3, t.box.get_top()
            under_term(t, dft)
            assert dft.get_top()[1] < TRACK_BOTTOM - 0.05, dft.get_top()
            errs = []
            for i, phrase in enumerate(("your project", "and two service account emails", "and gcp service")):
                if i:
                    vo.wait_until(phrase)
                ln = type_capture(self, t, B31[i], type_time=0.45)[0]
                rings.append(ring_project(self, ln))
                errs += list(out(self, t, [(B31[i].line(2), ERR)], wrap=True, run_time=0.3))
            live = alive(t, errs)
            self.play(*[glyphs_of(r).animate.set_opacity(0.4) for r in live], run_time=0.4)
            self.add(t)
            vo.wait_until("Replace ac215 project")
            self.play(FadeIn(dft, shift=DOWN * 0.1), run_time=0.4)
            self.play(*[Indicate(r, color=INK, scale_factor=1.15) for r in alive(t, rings)], run_time=0.7)
            self.add(t)
            flash_tag(self, dft, INK, 1.06)
            # the local block (extra): the same three keys, no output
            xb = extra_row()
            bar_tag(t, xb)
            ok = ok_chip("✓ local · same three keys")
            ok.next_to(dft, LEFT, buff=0.3)
            assert ok.get_left()[0] > -6.5 and ok.get_top()[1] < TRACK_BOTTOM - 0.05, ok.get_corner(UL)
            self.play(track(trk, 2, True), FadeIn(xb), FadeIn(ok, shift=DOWN * 0.1), run_time=0.35)
            for c in C11:
                ln = type_capture(self, t, c, type_time=0.15)[0]
                rings.append(ring_project(self, ln, run_time=0.12))
            bare_prompt(self, t)

        # ========================================================== 2. what the two security keys feed
        cp = wrapped_code(CC, 9, 12, {9: [".get("]}, size=SIZE)
        assert cp.rows == {9: [0, 1], 10: [2], 11: [3], 12: [4]}, cp.rows
        assert cp.width < 2 * SAFE_X - 0.1, cp.width
        cp.move_to([0, 0, 0]).align_to([0, 2.7, 0], UP)
        b9 = span_bar(cp.code, 0, 1, CLOUD, 0.25)
        b10 = span_bar(cp.code, 2, 4, OWN, 0.2)
        bars_behind(cp, [b9, b10])
        k9 = code_span(cp.code, 1, '"gcp_service_account_email"')
        k10 = code_span(cp.code, 3, '"gcp_ksa_service_account_email"')
        ch9 = grey_chip("→ the nodes' service account (line 50)", color=CLOUD)
        ch10 = grey_chip("→ the API's Kubernetes service account (line 158)", color=OWN)
        ch9.next_to(cp, DOWN, buff=0.3).align_to(cp, LEFT).shift(RIGHT * 0.2)
        ch10.next_to(ch9, DOWN, buff=0.18).align_to(ch9, LEFT)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(ok), FadeOut(dft), FadeOut(xb), track(trk, 2), run_time=0.4)
            self.remove(ok, dft, xb)
            resize(self, t, 3, run_time=0.5)
            assert ch10.get_bottom()[1] > t.box.get_top()[1] + 0.1, (ch10.get_bottom(), t.box.get_top())
            self.play(FadeIn(cp, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Line 9 takes")
            self.play(FadeIn(b9), k9.animate.set_color(CLOUD), run_time=0.4)
            self.play(Indicate(k9, color=CLOUD, scale_factor=1.06), run_time=0.6)
            vo.wait_until("the nodes run as")
            self.play(FadeIn(ch9, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Line 10 takes")
            self.play(FadeIn(b10), k10.animate.set_color(OWN), run_time=0.4)
            self.play(Indicate(k10, color=OWN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("which the API Pods")
            self.play(FadeIn(ch10, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, ch10, INK, 1.04)

        # ========================================================== 3. pulumi config: keys and leftovers
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(cp, b9, b10, ch9, ch10)), track(trk, 2, True), run_time=0.4)
            self.remove(cp, b9, b10, ch9, ch10)
            resize(self, t, 13, run_time=0.5)
            vo.wait_until("An extra, pulumi config")
            r12 = type_capture(self, t, C12, type_time=0.5)[0]
            e12 = mark_extra(self, t, r12, extra_row())
            spec = [C12.line(2), (C12.line(3), S.GREY), (C12.line(4), OWN), C12.line(5),
                    (C12.line(6), OWN), (C12.line(7), OWN), (C12.line(8), S.GREY),
                    (C12.line(9), S.GREY), (C12.line(10), S.GREY)]
            g12 = out(self, t, spec, wrap=True, run_time=0.6)
            row = {n: next(r for r in g12 if r.text.startswith(C12.line(n)[:20])) for n in (3, 4, 5, 6, 7, 8)}
            keys = [substring(row[n], C12.line(n).split()[0]) for n in (4, 6, 7)]
            vo.wait_until("lists your three keys")
            self.play(*[Indicate(row[n], color=OWN, scale_factor=1.04) for n in (4, 6, 7)], run_time=0.7)
            self.add(t)
            vo.wait_until("and two leftovers")
            lt = row_tag("leftovers · unused")
            pin(self, row[3], beside(lt, row[3]))
            un = row_tag("unused")
            if row[8].strut.get_right()[0] + 0.3 + un.width < t.box.get_right()[0] - 0.12:
                pin(self, row[8], beside(un, row[8], buff=0.3))
            else:
                un = None
            vo.wait_until("setup SSL")
            self.play(Indicate(row[3], color=S.GREY, scale_factor=1.04), run_time=0.6)
            self.add(t)
            vo.wait_until("and an SSH user")
            self.play(Indicate(row[8], color=S.GREY, scale_factor=1.04), run_time=0.6)
            self.add(t)
            vo.wait_until("A typo in a key name")
            self.play(*[k.animate.set_color(TURN) for k in keys], run_time=0.4)
            self.play(*[Indicate(k, color=TURN, scale_factor=1.08) for k in keys], run_time=0.7)
            self.add(t)

        # ========================================================== 4. preview: the TypeError at line 70
        with self.voiceover(SAY[4]) as vo:
            out_anims = [FadeOut(e12)] if e12 is not None else []
            self.play(track(trk, 3), *out_anims, run_time=0.4)
            if e12 is not None:
                self.remove(e12)
            vo.wait_until("Then Preview")
            type_capture(self, t, B32, type_time=0.5)
            out(self, t, [(B32.line(2), ERR)], wrap=True, run_time=0.3)
            vo.wait_until("On the local backend")
            self.play(track(trk, 3, True), run_time=0.3)
            type_capture(self, t, C13, type_time=0.5)
            x13 = extra_row()
            bar_tag(t, x13)
            self.play(FadeIn(x13), run_time=0.25)
            g13 = out(self, t, [C13.line(7), C13.line(10), "…"], wrap=True, run_time=0.4)
            tb13 = out(self, t, [C13.line(31), C13.line(32), C13.line(33), (C13.line(34), ERR)], run_time=0.5)
            out(self, t, [C13.line(37), C13.line(38)], run_time=0.3)
            r31, r34 = tb13[0], tb13[3]
            vo.wait_until("a Python error at line 70")
            l70 = substring(r31, "line 70")
            self.play(l70.animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(l70, color=ERR, scale_factor=1.12), run_time=0.6)
            self.add(t)
            vo.wait_until("none type is not subscriptable")
            self.play(Indicate(r34, color=ERR, scale_factor=1.05), run_time=0.7)
            self.add(t)
            vo.wait_until("The program asked")
            pa = code(SC, 10, 13, font_size=SIZE, dedent=True)
            pb = code(SC, 68, 71, font_size=SIZE, dedent=True)
            pa.move_to([0, 0, 0]).align_to([-6.4, 0, 0], LEFT).align_to([0, 2.75, 0], UP)
            pb.next_to(pa, DOWN, buff=0.12).align_to(pa, LEFT)
            self.play(FadeOut(x13), run_time=0.2)
            self.remove(x13)
            resize(self, t, 2, keep=[r31, r34], run_time=0.5)
            assert pb.get_bottom()[1] > t.box.get_top()[1] + 0.05, (pb.get_bottom(), t.box.get_top())
            ba = line_bar(pa.code, 0, ROUTE, 0.25)
            bars_behind(pa, [ba])
            sref = code_span(pa.code, 0, '"organization/deploy-images/dev"')
            bb = line_bar(pb.code, 2, ERR, 0.28)
            bars_behind(pb, [bb])
            tg0 = code_span(pb.code, 2, "tags[0]")
            self.play(FadeIn(pa, shift=DOWN * 0.1), run_time=0.4)
            self.play(FadeIn(ba), sref.animate.set_color(ROUTE), run_time=0.4)
            self.play(FadeIn(pb, shift=DOWN * 0.1), FadeIn(bb), run_time=0.4)
            vo.wait_until("and got nothing")
            self.play(tg0.animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(tg0, color=ERR, scale_factor=1.15), run_time=0.7)

        # ========================================================== 5. the same state bucket
        sp = StackPipe()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(pa, pb, ba, bb)), run_time=0.4)
            self.remove(pa, pb, ba, bb)
            sp.bucket(self)
            assert sp.get_bottom()[1] > t.box.get_top()[1] + 0.05, (sp.get_bottom(), t.box.get_top())
            vo.wait_until("never finished pulumi up")
            sp.break_pipe(self)
            vo.wait_until("Skipping it is safe")
            sp.fill_outputs(self)
            sp.join(self)
            # the note under the box said 'init + preview only, no up': now it would contradict
            # the filled box, so it becomes what happened
            note = label("after pulumi up", 20, OWN).move_to(sp.out_note)
            self.play(Transform(sp.out_note, note), run_time=0.4)
            assert sp.get_bottom()[1] > t.box.get_top()[1] + 0.05, (sp.get_bottom(), t.box.get_top())

        # ========================================================== 6. the real plan: + 23 to create
        rt = ResourceTree()
        ph = placeholder_tag()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(sp), track(trk, 3, True), run_time=0.4)
            self.remove(sp)
            resize(self, t, 3, run_time=0.4)
            x20 = extra_row()
            bar_tag(t, x20)
            ph.next_to(t.box, UP, buff=0.12).align_to(t.box, LEFT)
            self.play(FadeIn(x20), FadeIn(ph, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("with placeholder tags")
            flash_tag(self, ph, INK, 1.05)
            vo.wait_until("nothing is built")
            type_capture(self, t, C20, type_time=0.35)
            lines_of = lambda a, b: [C20.line(n) for n in range(a, b + 1)]  # noqa: E731
            vo.wait_until("Now the real plan appears")
            fast_out(self, t, lines_of(8, 11))
            rt.group(self, "network", run_time=0.2)
            rt.group(self, "cluster", run_time=0.2)
            assert rt.get_bottom()[1] > ph.get_top()[1] + 0.05, (rt.get_bottom(), ph.get_top())
            fast_out(self, t, lines_of(13, 14))
            fast_out(self, t, lines_of(16, 17))
            rt.group(self, "provider", run_time=0.2)
            vo.wait_until("the network")
            rt.expand(self, "network", run_time=0.3)
            fast_out(self, t, lines_of(18, 23), per=0.18)
            vo.wait_until("the cluster")
            rt.collapse(self, run_time=0.2)
            for k in ("identity", "ingress", "storage"):
                rt.group(self, k, run_time=0.15)
            rt.expand(self, "cluster", run_time=0.3)
            fast_out(self, t, lines_of(24, 33), per=0.18)
            rt.group(self, "app", run_time=0.15)
            vo.wait_until("the Kubernetes objects")
            rt.expand(self, "app", run_time=0.3)
            vo.wait_until("and plus 23 to create")
            rt.collapse(self, run_time=0.2)
            rt.grow(self, lag=0.25)
            g45 = fast_out(self, t, ["…", (C20.line(45), TURN)])
            rt.counter(self, 23)
            self.play(Indicate(rt.count_mob, color=TURN, scale_factor=1.1),
                      Indicate(g45[-1], color=TURN, scale_factor=1.1), run_time=0.6)
            self.add(t)

        # ========================================================== 7. two reads; the outputs
        with self.voiceover(SAY[7]) as vo:
            vo.wait_until("Two more lines are lookups")
            rt.reads(self)
            vo.wait_until("the stack reference")
            a_, b_ = rt.reads_g[1], rt.reads_g[2]
            self.play(Indicate(a_, color=ROUTE, scale_factor=1.06), run_time=0.5)
            self.play(Indicate(b_, color=ROUTE, scale_factor=1.06), run_time=0.5)
            rt.heal(self)
            vo.wait_until("In the outputs")
            last = g45[-1]
            t.lines.remove(last)
            self.play(FadeOut(rt), FadeOut(last), FadeOut(ph), run_time=0.4)
            self.remove(rt, last, ph)
            resize(self, t, 12, extra=[x20.animate.move_to([x20.get_x(), bar_y(t, 12), 0])], run_time=0.5)
            ph.next_to(t.box, UP, buff=0.12).align_to(t.box, RIGHT)
            self.play(FadeIn(ph), run_time=0.3)
            ys = [(C20.line(35), INK)] + [(C20.line(n), OWN if n == 38 else S.GREY) for n in range(36, 43)]
            go = out(self, t, ys + [C20.line(44), (C20.line(45), TURN)], run_time=0.6)
            o_row = {n: go[n - 35] for n in range(35, 43)}
            r45 = go[-1]
            vo.wait_until("only the cluster name is known")
            self.play(Indicate(o_row[38], color=OWN, scale_factor=1.05), run_time=0.7)
            self.add(t)
            vo.wait_until("the address and the URL")
            self.play(Indicate(o_row[40], color=TURN, scale_factor=1.05),
                      Indicate(o_row[36], color=TURN, scale_factor=1.05), run_time=0.8)
            self.add(t)

        # ========================================================== 8. your turn
        with self.voiceover(SAY[8]) as vo:
            self.play(track(trk, 3), FadeOut(x20), run_time=0.4)
            self.remove(x20)
            yt = turn_row()
            pin(self, r45, beside(yt, r45))
            flash_tag(self, yt, TURN)
            vo.wait_until("you should see the same 23")
            self.play(Indicate(substring(r45, "+ 23 to create"), color=TURN, scale_factor=1.12), run_time=0.8)
            self.add(t)
        self.play(FadeOut(VGroup(trk, t, ph)), run_time=0.6)
        self.remove(trk, t, ph)
        self.wait(0.3)
